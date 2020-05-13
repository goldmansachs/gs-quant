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
import copy
import datetime as dt
import logging
import weakref
from abc import ABCMeta
from concurrent.futures import Future, ThreadPoolExecutor
from threading import Lock
from typing import Iterable, Optional, Union

from .markets import ClosingMarket, LiveMarket, Market
from gs_quant.base import Priceable, RiskKey, Scenario
from gs_quant.common import PricingLocation
from gs_quant.context_base import ContextBaseWithDefault
from gs_quant.datetime.date import business_day_offset
from gs_quant.risk import DataFrameWithInfo, ErrorValue, FloatWithInfo, MarketDataScenario, \
    PricingDateAndMarketDataAsOf, \
    ResolvedInstrumentValues, RiskMeasure, RiskPosition, RiskRequest, \
    RiskRequestParameters, SeriesWithInfo, StringWithInfo
from gs_quant.risk import CompositeScenario
from gs_quant.risk.results import MultipleRiskMeasureFuture
from gs_quant.session import GsSession
from gs_quant.target.data import MarketDataCoordinate as __MarketDataCoordinate


_logger = logging.getLogger(__name__)

CacheResult = Union[DataFrameWithInfo, FloatWithInfo, StringWithInfo]


class MarketDataCoordinate(__MarketDataCoordinate):

    def __str__(self):
        return "|".join(f or '' for f in (self.mkt_type, self.mkt_asset, self.mkt_class,
                                          '_'.join(self.mkt_point or ()), self.mkt_quoting_style))


class PricingFuture(Future):

    def __init__(self, pricing_context):
        super().__init__()
        self.__pricing_context = pricing_context

    def result(self, timeout=None):
        """Return the result of the call that the future represents.

        :param timeout: The number of seconds to wait for the result if the future isn't done.
        If None, then there is no limit on the wait time.

        Returns:
            The result of the call that the future represents.

        Raises:
            CancelledError: If the future was cancelled.
            TimeoutError: If the future didn't finish executing before the given timeout.

        Exception: If the call raised then that exception will be raised.
        """
        if not self.done() and PricingContext.current == self.__pricing_context and self.__pricing_context.is_entered:
            raise RuntimeError('Cannot evaluate results under the same pricing context being used to produce them')

        return super().result(timeout=timeout)


class PricingCache(metaclass=ABCMeta):
    """
    Weakref cache for instrument calcs
    """
    __cache = weakref.WeakKeyDictionary()

    @classmethod
    def clear(cls):
        __cache = weakref.WeakKeyDictionary()

    @classmethod
    def get(cls, risk_key: RiskKey, priceable: Priceable) -> Optional[CacheResult]:
        return cls.__cache.get(priceable, {}).get(risk_key)

    @classmethod
    def put(cls, risk_key: RiskKey, priceable: Priceable, result: CacheResult):
        if not isinstance(result, ErrorValue) and not isinstance(risk_key.market, LiveMarket):
            cls.__cache.setdefault(priceable, {})[risk_key] = result

    @classmethod
    def drop(cls, priceable: Priceable):
        if priceable in cls.__cache:
            cls.__cache.pop(priceable)


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
                 visible_to_gs: bool = False,
                 csa_term: Optional[str] = None,
                 poll_for_batch_results: Optional[bool] = False,
                 batch_results_timeout: Optional[int] = None,
                 market: Optional[Market] = None
                 ):
        """
        The methods on this class should not be called directly. Instead, use the methods on the instruments,
        as per the examples

        :param pricing_date: the date for pricing calculations. Default is today
        :param market_data_location: the location for sourcing market data ('NYC', 'LDN' or 'HKG' (defaults to LDN)
        :param is_async: if True, return (a future) immediately. If False, block (defaults to False)
        :param is_batch: use for calculations expected to run longer than 3 mins, to avoid timeouts.
            It can be used with is_aync=True|False (defaults to False)
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

        self.__pricing_date = pricing_date or business_day_offset(dt.date.today(), 0, roll='forward')
        self.__csa_term = csa_term
        self.__is_async = is_async
        self.__is_batch = is_batch
        self.__poll_for_batch_results = poll_for_batch_results
        self.__batch_results_timeout = batch_results_timeout
        self.__use_cache = use_cache
        self.__visible_to_gs = visible_to_gs
        self.__market = market
        self.__lock = Lock()
        self.__pending = {}

        if self.__market is None:
            # Do not use self.__class__.current - it will cause a cycle
            default_location = market_data_location or (
                self.__class__.path[0].market_data_location if self.__class__.path else PricingLocation.LDN)
            market_data_date = business_day_offset(self.__pricing_date, -1, roll='preceding') if\
                self.__pricing_date == dt.date.today() else self.__pricing_date

            self.__market = market or ClosingMarket(default_location, market_data_date)

    def _on_exit(self, exc_type, exc_val, exc_tb):
        if exc_val:
            raise exc_val
        else:
            self.__calc()

    def _return_calc_result(self, future):
        if not (self.is_entered or self.__is_async):
            if not future.done():
                self.__calc()

            return future.result()
        else:
            return future

    def _result_future(self) -> PricingFuture:
        return PricingFuture(self.__active_context)

    def __calc(self):
        session = GsSession.current
        requests_by_provider = {}

        def run_requests(requests_: Iterable[RiskRequest], provider_):
            results = {}

            try:
                with session:
                    results = provider_.calc_multi(requests_)
                    if self.__is_batch:
                        results = provider_.get_results(dict(zip(results, requests_)),
                                                        self.__poll_for_batch_results,
                                                        timeout=self.__batch_results_timeout).values()
            except Exception as e:
                results = ({k: e for k in self.__pending.keys()},)
            finally:
                with self.__lock:
                    for result in results:
                        for (risk_key, result_priceable), value in result.items():
                            if self.__use_cache:
                                PricingCache.put(risk_key, result_priceable, value)

                            self.__pending.pop((risk_key, result_priceable)).set_result(value)

        with self.__lock:
            # Group requests optimally
            for (key, priceable) in self.__pending.keys():
                risk_measures, markets_dates = requests_by_provider.setdefault(key.provider, {})\
                    .setdefault((key.params, key.scenario, key.market.location, type(key.market)), {})\
                    .setdefault(priceable, (set(), set()))

                risk_measures.add(key.risk_measure)
                markets_dates.add((key.date, key.market))

        if requests_by_provider:
            num_providers = len(requests_by_provider)
            request_pool = ThreadPoolExecutor(num_providers) if num_providers > 1 or self.__is_async else None

            for provider, by_params_scenario in requests_by_provider.items():
                requests_for_provider = {}

                for (params, scenario, location, _), positions_by_market_measures in by_params_scenario.items():
                    for priceable, (risk_measures, markets_dates) in positions_by_market_measures.items():
                        requests_for_provider.setdefault((params, scenario, location,
                                                          tuple(sorted(risk_measures)),
                                                          tuple(sorted(markets_dates))), []).append(priceable)

                requests = [
                    RiskRequest(
                        tuple(RiskPosition(instrument=p, quantity=p.get_quantity()) for p in priceables),
                        risk_measures,
                        parameters=self.__parameters,
                        wait_for_results=not self.__is_batch,
                        pricing_location=location,
                        scenario=scenario,
                        pricing_and_market_data_as_of=tuple(PricingDateAndMarketDataAsOf(
                            pricing_date=d, market_data_as_of=m.as_of) for d, m in markets_dates),
                        request_visible_to_gs=self.__visible_to_gs
                    )
                    for (params, scenario, location, risk_measures, markets_dates), priceables
                    in requests_for_provider.items()
                ]

                if request_pool:
                    request_pool.submit(run_requests, requests, provider)
                else:
                    run_requests(requests, provider)

            if request_pool:
                request_pool.shutdown(wait=not self.__is_async)

    def __risk_key(self, risk_measure: RiskMeasure, provider: type) -> RiskKey:
        return RiskKey(provider, self.__pricing_date, self.__market, self.__parameters, self.__scenario, risk_measure)

    @property
    def __active_context(self):
        return next((c for c in reversed(PricingContext.path) if c.is_entered), self)

    @property
    def __parameters(self) -> RiskRequestParameters:
        return RiskRequestParameters(csa_term=self.__csa_term, raw_results=True)

    @property
    def __scenario(self) -> Optional[MarketDataScenario]:
        scenarios = Scenario.path
        if not scenarios:
            return None

        return MarketDataScenario(scenario=scenarios[0] if len(scenarios) == 1 else
                                  CompositeScenario(scenarios=tuple(reversed(scenarios))))

    @property
    def market(self) -> Market:
        return self.__market

    @property
    def pricing_date(self) -> dt.date:
        """Pricing date"""
        return self.__pricing_date

    @property
    def market_data_location(self) -> str:
        """Market data location"""
        return self.market.location

    @property
    def use_cache(self) -> bool:
        """Cache results"""
        return self.__use_cache

    @property
    def visible_to_gs(self) -> bool:
        """Request contents visible to GS"""
        return self.__visible_to_gs

    def calc(self, priceable: Priceable, risk_measure: Union[RiskMeasure, Iterable[RiskMeasure]])\
            -> Union[list, DataFrameWithInfo, ErrorValue, FloatWithInfo, Future, MultipleRiskMeasureFuture,
                     SeriesWithInfo]:
        """
        Calculate the risk measure for the priceable instrument. Do not use directly, use via instruments

        :param priceable: The priceable (e.g. instrument)
        :param risk_measure: The measure we wish to calculate
        :return: A float, Dataframe, Series or Future (depending on is_async or whether the context is entered)

        **Examples**

        >>> from gs_quant.instrument import IRSwap
        >>> from gs_quant.risk import IRDelta
        >>>
        >>> swap = IRSwap('Pay', '10y', 'USD', fixed_rate=0.01)
        >>> delta = swap.calc(IRDelta)
        """
        futures = {}

        with self.__active_context.__lock:
            for risk_measure in (risk_measure,) if isinstance(risk_measure, RiskMeasure) else risk_measure:
                risk_key = self.__risk_key(risk_measure, priceable.provider())
                future = self.__active_context.__pending.get((risk_key, priceable))
                cached_result = PricingCache.get(risk_key, priceable) if self.use_cache else None

                if future is None:
                    future = PricingFuture(self.__active_context)
                    if cached_result is not None:
                        future.set_result(cached_result)
                    else:
                        self.__active_context.__pending[(risk_key, priceable)] = future

                futures[risk_measure] = future

        future = MultipleRiskMeasureFuture(futures, result_future=self._result_future())\
            if len(futures) > 1 else futures[risk_measure]

        return self._return_calc_result(future)

    def resolve_fields(self, priceable: Priceable, in_place: bool) -> Optional[Union[Priceable, Future]]:
        """
        Resolve fields on the priceable which were not supplied. Do not use directly, use via instruments

        :param priceable:  The priceable (e.g. instrument)
        :param in_place:   Resolve in place or return a new Priceable

        **Examples**

        >>> from gs_quant.instrument import IRSwap
        >>>
        >>> swap = IRSwap('Pay', '10y', 'USD')
        >>> rate = swap.fixed_rate

        fixedRate is None

        >>> swap.resolve()
        >>> rate = swap.fixed_rate

        fixed_rate is now the solved value
        """
        def check_valid(result_):
            if isinstance(result_, ErrorValue):
                _logger.error('Failed to resolve instrument fields: ' + result_.error)
                return priceable
            elif result_ is None:
                _logger.error('Unknown error resolving instrument fields')
                return priceable
            else:
                return result_

        result = self.calc(priceable, ResolvedInstrumentValues)
        if in_place:
            def handle_result(result_):
                result_ = check_valid(result_)
                if result_ is not priceable:
                    priceable.unresolved = copy.copy(priceable)
                    priceable.from_instance(result_)
                    priceable.resolution_key = result_.resolution_key

            if isinstance(result, Future):
                result.add_done_callback(lambda f: handle_result(f.result()))
            else:
                handle_result(result)
        else:
            if isinstance(result, Future):
                ret = self._result_future()
                result.add_done_callback(lambda f: ret.set_result(check_valid(f.result())))
                return ret
            else:
                return check_valid(result)
