"""
Copyright 2019 Goldman Sachs.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""
import asyncio
import datetime as dt
import logging
import weakref
from abc import ABCMeta
from concurrent.futures import ThreadPoolExecutor
from inspect import signature
from itertools import zip_longest
from tqdm import tqdm
from typing import Optional, Union

from .markets import CloseMarket, LiveMarket, Market, close_market_date
from gs_quant.base import InstrumentBase, RiskKey, Scenario, get_enum_value
from gs_quant.common import PricingLocation
from gs_quant.context_base import ContextBaseWithDefault
from gs_quant.datetime.date import business_day_offset
from gs_quant.risk import CompositeScenario, DataFrameWithInfo, ErrorValue, FloatWithInfo, MarketDataScenario, \
    RiskMeasure, StringWithInfo
from gs_quant.risk.results import PricingFuture
from gs_quant.session import GsSession
from gs_quant.target.common import PricingDateAndMarketDataAsOf
from gs_quant.target.risk import RiskPosition, RiskRequest, RiskRequestParameters


_logger = logging.getLogger(__name__)

CacheResult = Union[DataFrameWithInfo, FloatWithInfo, StringWithInfo]


class PricingCache(metaclass=ABCMeta):
    """
    Weakref cache for instrument calcs
    """
    __cache = weakref.WeakKeyDictionary()

    @classmethod
    def clear(cls):
        __cache = weakref.WeakKeyDictionary()

    @classmethod
    def get(cls, risk_key: RiskKey, instrument: InstrumentBase) -> Optional[CacheResult]:
        return cls.__cache.get(instrument, {}).get(risk_key)

    @classmethod
    def put(cls, risk_key: RiskKey, instrument: InstrumentBase, result: CacheResult):
        if not isinstance(result, ErrorValue) and not isinstance(risk_key.market, LiveMarket):
            cls.__cache.setdefault(instrument, {})[risk_key] = result

    @classmethod
    def drop(cls, instrument: InstrumentBase):
        if instrument in cls.__cache:
            cls.__cache.pop(instrument)


class PricingContext(ContextBaseWithDefault):

    """
    A context for controlling pricing and market data behaviour
    """

    def __init__(self,
                 pricing_date: Optional[dt.date] = None,
                 market_data_location: Optional[Union[PricingLocation, str]] = None,
                 is_async: bool = False,
                 is_batch: bool = False,
                 use_cache: bool = False,
                 visible_to_gs: Optional[bool] = None,
                 csa_term: Optional[str] = None,
                 timeout: Optional[int] = None,
                 market: Optional[Market] = None,
                 show_progress: Optional[bool] = False):
        """
        The methods on this class should not be called directly. Instead, use the methods on the instruments,
        as per the examples

        :param pricing_date: the date for pricing calculations. Default is today
        :param market_data_location: the location for sourcing market data ('NYC', 'LDN' or 'HKG' (defaults to LDN)
        :param is_async: if True, return (a future) immediately. If False, block (defaults to False)
        :param is_batch: use for calculations expected to run longer than 3 mins, to avoid timeouts.
            It can be used with is_async=True|False (defaults to False)
        :param use_cache: store results in the pricing cache (defaults to False)
        :param visible_to_gs: are the contents of risk requests visible to GS (defaults to False)
        :param csa_term: the csa under which the calculations are made. Default is local ccy ois index

        **Examples**

        To change the market data location of the default context:

        >>> from gs_quant.markets import PricingContext
        >>> import datetime as dt
        >>>
        >>> PricingContext.current = PricingContext(market_data_location='LDN')

        For a blocking, synchronous request:

        >>> from gs_quant.instrument import IRCap
        >>> cap = IRCap('5y', 'GBP')
        >>>
        >>> with PricingContext():
        >>>     price_f = cap.dollar_price()
        >>>
        >>> price = price_f.result()

        For an asynchronous request:

        >>> with PricingContext(is_async=True):
        >>>     price_f = cap.dollar_price()
        >>>
        >>> while not price_f.done:
        >>>     ...
        """
        super().__init__()

        if market and market_data_location and market.location.value is not market_data_location:
            raise ValueError('market.location and market_data_location cannot be different')

        if not market_data_location:
            if not market:
                # use parent context's market_data_location
                if self != self.active_context:
                    market_data_location = self.active_context.market_data_location
                # if no parent but there was a context set previously, use that
                elif self.prior_context:
                    market_data_location = self.prior_context.market_data_location
            else:
                market_data_location = market.location

        self.__pricing_date = pricing_date or (self.prior_context.pricing_date if self.prior_context else
                                               business_day_offset(dt.date.today(), 0, roll='preceding'))
        self.__csa_term = csa_term
        self.__is_async = is_async
        self.__is_batch = is_batch
        self.__timeout = timeout
        self.__use_cache = use_cache
        self.__visible_to_gs = visible_to_gs
        self.__market_data_location = get_enum_value(PricingLocation, market_data_location)
        self.__market = market or CloseMarket(
            date=close_market_date(self.__market_data_location, self.__pricing_date) if pricing_date else None,
            location=self.__market_data_location if market_data_location else None)
        self.__pending = {}
        self.__show_progress = show_progress

    def _on_exit(self, exc_type, exc_val, exc_tb):
        if exc_val:
            raise exc_val
        else:
            self.__calc()

    def __calc(self):
        def run_requests(requests_: list, provider_, create_event_loop: bool):
            if create_event_loop:
                asyncio.set_event_loop(asyncio.new_event_loop())

            results = {}

            try:
                with session:
                    results = provider_.run(requests_, 1000, progress_bar, timeout=self.__timeout)
            except Exception as e:
                results = {k: e for k in self.__pending.keys()}
            finally:
                while self.__pending:
                    (risk_key_, priceable_), future = self.__pending.popitem()
                    result = results.get((risk_key_, priceable_))

                    if result is not None:
                        if self.__use_cache:
                            PricingCache.put(risk_key_, priceable_, result)
                    else:
                        result = ErrorValue(risk_key_, 'No result returned')

                    future.set_result(result)

        # Group requests optimally
        requests_by_provider = {}
        for (key, instrument) in self.__pending.keys():
            requests_by_provider.setdefault(key.provider, {})\
                .setdefault((key.params, key.scenario, key.date, key.market), {})\
                .setdefault(instrument, set())\
                .add(key.risk_measure)

        requests_for_provider = {}
        if requests_by_provider:
            session = GsSession.current
            request_visible_to_gs = session.is_internal() if self.__visible_to_gs is None else self.__visible_to_gs

            for provider, by_params_scenario_date_market in requests_by_provider.items():
                grouped_requests = {}

                for (params, scenario, date, market), positions_by_measures in by_params_scenario_date_market.items():
                    for instrument, risk_measures in positions_by_measures.items():
                        grouped_requests.setdefault((params, scenario, date, market, tuple(sorted(risk_measures))),
                                                    []).append(instrument)

                requests = []

                for (params, scenario, date, market, risk_measures), instruments in grouped_requests.items():
                    for chunk in [tuple(filter(None, i)) for i in zip_longest(*[iter(instruments)] * 1000)]:
                        requests.append(RiskRequest(
                            tuple(RiskPosition(instrument=i, quantity=i.instrument_quantity) for i in chunk),
                            risk_measures,
                            parameters=self._parameters,
                            wait_for_results=not self.__is_batch,
                            scenario=scenario,
                            pricing_and_market_data_as_of=(PricingDateAndMarketDataAsOf(pricing_date=date,
                                                                                        market=market),),
                            request_visible_to_gs=request_visible_to_gs,
                        ))

                requests_for_provider[provider] = requests
            
            show_status = self.__show_progress and\
                (len(requests_for_provider) > 1 or len(next(iter(requests_for_provider.values()))) > 1)
            request_pool = ThreadPoolExecutor(len(requests_for_provider))\
                if len(requests_for_provider) > 1 or self.__is_async else None
            progress_bar = tqdm(total=len(self.__pending), position=0, maxinterval=1) if show_status else None
            completion_futures = []

            for provider, requests in requests_for_provider.items():
                if request_pool:
                    completion_future = request_pool.submit(run_requests, requests, provider, True)
                    if not self.__is_async:
                        completion_futures.append(completion_future)
                else:
                    run_requests(requests, provider, False)

            # Wait on results if not async, so exceptions are surfaced
            if request_pool:
                request_pool.shutdown(False)
                all(f.result() for f in completion_futures)

    def __risk_key(self, risk_measure: RiskMeasure, provider: type) -> RiskKey:
        return RiskKey(provider, self.__pricing_date, self.__market, self._parameters, self._scenario, risk_measure)

    @property
    def _parameters(self) -> RiskRequestParameters:
        return RiskRequestParameters(csa_term=self.__csa_term, raw_results=True)

    @property
    def _scenario(self) -> Optional[MarketDataScenario]:
        scenarios = Scenario.path
        if not scenarios:
            return None

        return MarketDataScenario(scenario=scenarios[0] if len(scenarios) == 1 else
                                  CompositeScenario(scenarios=tuple(reversed(scenarios))))

    @property
    def active_context(self):
        return next((c for c in reversed(PricingContext.path) if c.is_entered), self)

    @property
    def prior_context(self):
        return PricingContext.path[-1] if len(PricingContext.path) else None

    @property
    def is_current(self) -> bool:
        return self == PricingContext.current

    @property
    def is_async(self) -> bool:
        return self.__is_async

    @property
    def is_batch(self) -> bool:
        return self.__is_batch

    @property
    def market(self) -> Market:
        return self.__market

    @property
    def market_data_location(self) -> PricingLocation:
        return self.__market_data_location

    @property
    def csa_term(self) -> str:
        return self._parameters.csa_term

    @property
    def pricing_date(self) -> dt.date:
        """Pricing date"""
        return self.__pricing_date

    @property
    def use_cache(self) -> bool:
        """Cache results"""
        return self.__use_cache

    @property
    def visible_to_gs(self) -> Optional[bool]:
        """Request contents visible to GS"""
        return self.__visible_to_gs

    def clone(self, **kwargs):
        clone_kwargs = {k: getattr(self, k, None) for k in signature(self.__init__).parameters.keys()}
        clone_kwargs.update(kwargs)
        return self.__class__(**clone_kwargs)

    def _calc(self, instrument: InstrumentBase, risk_key: RiskKey) -> PricingFuture:
        future = self.active_context.__pending.get((risk_key, instrument))

        if future is None:
            future = PricingFuture()
            cached_result = PricingCache.get(risk_key, instrument) if self.use_cache else None

            if cached_result is not None:
                future.set_result(cached_result)
            else:
                self.active_context.__pending[(risk_key, instrument)] = future

        if not (self.is_entered or self.is_async):
            self.__calc()

        return future
    
    def calc(self, instrument: InstrumentBase, risk_measure: RiskMeasure) -> PricingFuture:
        """
        Calculate the risk measure for the instrument. Do not use directly, use via instruments

        :param instrument: The instrument
        :param risk_measure: The measure we wish to calculate
        :return: A PricingFuture whose result will be the calculation result

        **Examples**

        >>> from gs_quant.instrument import IRSwap
        >>> from gs_quant.risk import IRDelta
        >>>
        >>> swap = IRSwap('Pay', '10y', 'USD', fixed_rate=0.01)
        >>> delta = swap.calc(IRDelta)
        """
        return self._calc(instrument, self.__risk_key(risk_measure, instrument.provider))
