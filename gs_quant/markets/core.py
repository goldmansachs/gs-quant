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
import itertools
import logging
import weakref
from abc import ABCMeta
from concurrent.futures import Future, ThreadPoolExecutor
from threading import Lock
from typing import Iterable, Optional, Tuple, Union

from gs_quant.api.risk import RiskApi
from gs_quant.base import Priceable, PricingKey, Scenario
from gs_quant.context_base import ContextBaseWithDefault
from gs_quant.datetime.date import business_day_offset, is_business_day
from gs_quant.risk import DataFrameWithInfo, ErrorValue, FloatWithInfo, MarketDataScenario, \
    PricingDateAndMarketDataAsOf, \
    ResolvedInstrumentValues, RiskMeasure, RiskPosition, RiskRequest, \
    RiskRequestParameters, SeriesWithInfo
from gs_quant.risk.results import MultipleRiskMeasureFuture
from gs_quant.risk import CompositeScenario
from gs_quant.session import GsSession
from gs_quant.target.data import MarketDataCoordinate as __MarketDataCoordinate

_logger = logging.getLogger(__name__)


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


class MarketDataCoordinate(__MarketDataCoordinate):

    def __str__(self):
        return "|".join(f or '' for f in (self.mkt_type, self.mkt_asset, self.mkt_class,
                                          '_'.join(self.mkt_point or ()), self.mkt_quoting_style))


class PricingCache(metaclass=ABCMeta):
    """
    Weakref cache for instrument calcs
    """
    __cache = weakref.WeakKeyDictionary()

    @classmethod
    def clear(cls):
        __cache = weakref.WeakKeyDictionary()

    @classmethod
    def missing_pricing_keys(cls,
                             priceable: Priceable,
                             risk_measure: RiskMeasure,
                             pricing_key: Optional[PricingKey] = None) -> Tuple[PricingKey, ...]:
        pricing_key = pricing_key or PricingContext.current.pricing_key

        if priceable in cls.__cache and risk_measure in cls.__cache[priceable]:
            cached = cls.__cache[priceable][risk_measure]
            return tuple(k for k in pricing_key if k not in cached)
        else:
            return pricing_key

    @classmethod
    def get(cls,
            priceable: Priceable,
            risk_measure: RiskMeasure,
            pricing_key: Optional[PricingKey] = None,
            return_partial: bool = False) -> Optional[Union[DataFrameWithInfo, FloatWithInfo, SeriesWithInfo]]:
        if priceable not in cls.__cache or risk_measure not in cls.__cache[priceable]:
            return

        pricing_key = pricing_key or PricingContext.current.pricing_key
        cached = cls.__cache[priceable][risk_measure]

        if len(pricing_key.pricing_market_data_as_of) > 1:
            values = [cached[k] for k in pricing_key if k in cached]
            if values and (return_partial or len(values) == len(pricing_key.pricing_market_data_as_of)):
                return values[0].compose(values, pricing_key)
        else:
            return cached.get(pricing_key)

    @classmethod
    def put(cls,
            priceable: Priceable,
            risk_measure: RiskMeasure,
            result: Union[DataFrameWithInfo, FloatWithInfo, SeriesWithInfo],
            pricing_key: Optional[PricingKey] = None):
        pricing_key = pricing_key or PricingContext.current.pricing_key

        if isinstance(result, (DataFrameWithInfo, FloatWithInfo, SeriesWithInfo)):
            cls.__cache.setdefault(priceable, {}).setdefault(risk_measure, {}).update(
                {k: result.for_pricing_key(k) for k in pricing_key})

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
                 market_data_as_of: Optional[Union[dt.date, dt.datetime]] = None,
                 market_data_location: Optional[str] = None,
                 is_async: bool = False,
                 is_batch: bool = False,
                 use_cache: bool = False,
                 visible_to_gs: bool = False,
                 csa_term: Optional[str] = None,
                 poll_for_batch_results: Optional[bool] = True,
                 batch_results_timeout: Optional[int] = None
                 ):
        """
        The methods on this class should not be called directly. Instead, use the methods on the instruments,
        as per the examples

        :param pricing_date: the date for pricing calculations. Default is today
        :param market_data_as_of: the date/datetime for sourcing market data
        (defaults to 1 business day before pricing_date)
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

        if pricing_date is None:
            pricing_date = dt.date.today()
            while not is_business_day(pricing_date):
                pricing_date -= dt.timedelta(days=1)

        self.__pricing_date = pricing_date
        self.__csa_term = csa_term
        self.__market_data_as_of = market_data_as_of
        # Do not use self.__class__.current - it will cause a cycle
        self.__market_data_location = market_data_location or (
            self.__class__.path[0].market_data_location if self.__class__.path else 'LDN')
        self.__is_async = is_async
        self.__is_batch = is_batch
        self.__poll_for_batch_results = poll_for_batch_results
        self.__batch_results_timeout = batch_results_timeout
        self.__risk_measures_in_scenario_by_provider_and_position = {}
        self.__futures = {}
        self.__use_cache = use_cache
        self.__visible_to_gs = visible_to_gs
        self.__lock = Lock()

    def _on_exit(self, exc_type, exc_val, exc_tb):
        self._calc()

    def _calc(self):
        requests_by_provider = {}
        session = GsSession.current
        batch_result = Future() if self.__is_batch else None

        def run_request(request_: RiskRequest, provider_: RiskApi):
            try:
                with session:
                    results = provider_.calc(request_)
                    handle_results(results, request_, provider_)
            except Exception as e:
                _logger.error(str(e))
                if self.__is_batch:
                    batch_result.set_result(True)

                handle_results(e, request_, provider_)

        def get_batch_results_if_ready(provider_: RiskApi):
            def get_results():
                with self.__lock:
                    provider_requests = {v: k for k, v in requests_by_provider[provider_].items()}

                try:
                    with session:
                        results = provider_.get_results(
                            provider_requests,
                            self.__poll_for_batch_results,
                            timeout=self.__batch_results_timeout)
                        return results, provider_requests, provider_
                except Exception as e:
                    _logger.error(str(e))
                    return e, provider_requests, provider_

            with self.__lock:
                ready = all(v for k, v in requests_by_provider[provider_].items())

            if ready:
                # All requests have been submitted, schedule result retrieval
                if self.__is_async:
                    batch_result_pool = ThreadPoolExecutor(1)
                    batch_result_pool.submit(get_results).add_done_callback(lambda f: handle_results(*f.result()))
                    batch_result_pool.shutdown(wait=False)
                else:
                    handle_results(*get_results())

        def handle_results(result: Union[Exception, dict, str], request_: RiskRequest, provider_: RiskApi):
            if isinstance(result, Exception):
                # Set all the futures for this request to an error value
                if isinstance(request_, dict):
                    # Batch response results, handle each result ...
                    for sub_request in request_.values():
                        self._handle_results({}, sub_request, error=str(result))

                    batch_result.set_result(True)
                else:
                    self._handle_results({}, request_, error=str(result))
            elif isinstance(result, str):
                # It's a result id from a batch request, add it to the dict until we've received all we're expecting
                with self.__lock:
                    requests_by_provider[provider_][request_] = result
                get_batch_results_if_ready(provider_)
            elif isinstance(result, dict):
                if isinstance(request_, dict):
                    # Batch response results, handle each result ...
                    for result_id, sub_result in result.items():
                        handle_results(sub_result, request_[result_id], provider_)

                    # ... and signal completion
                    batch_result.set_result(True)
                else:
                    # A normal response
                    self._handle_results(result, request_)

        with self.__lock:
            # Group requests by risk_measures, positions, scenario - so we can create unique RiskRequest objects
            # Determine how many we will need
            while self.__risk_measures_in_scenario_by_provider_and_position:
                provider, risk_measures_by_scenario =\
                    self.__risk_measures_in_scenario_by_provider_and_position.popitem()
                positions_by_scenario_and_risk_measures = {}
                for position, scenario_to_risk_measures in risk_measures_by_scenario.items():
                    for scenario, risk_measures in scenario_to_risk_measures.items():
                        positions_by_scenario_and_risk_measures.setdefault(scenario, {}).setdefault(
                            tuple(risk_measures), []).append(position)

                for scenario, positions_by_risk_measures in positions_by_scenario_and_risk_measures.items():
                    for risk_measures, positions in positions_by_risk_measures.items():
                        request = RiskRequest(
                            tuple(positions),
                            tuple(sorted(risk_measures, key=lambda m: m.name or m.measure_type.value)),
                            parameters=self.__parameters,
                            wait_for_results=not self.__is_batch,
                            pricing_location=self.__market_data_location,
                            scenario=scenario,
                            pricing_and_market_data_as_of=self._pricing_market_data_as_of,
                            request_visible_to_gs=self.__visible_to_gs
                        )

                        requests_by_provider.setdefault(provider, {})[request] = None

        # We can't use asyncio here until we move to an async HTTP client
        num_requests = len(tuple(itertools.chain.from_iterable(requests_by_provider.values())))
        request_pool = ThreadPoolExecutor(num_requests) if num_requests > 1 or self.__is_async else None

        for provider, requests in requests_by_provider.items():
            for request in requests.keys():
                if request_pool:
                    request_pool.submit(run_request, request, provider)
                else:
                    run_request(request, provider)

        if request_pool:
            request_pool.shutdown(wait=not self.__is_async)

        if batch_result and not self.__is_async:
            batch_result.result()

    def _handle_results(self, results: dict, request: RiskRequest, error: Optional[str] = 'No result returned'):
        with self.__lock:
            for risk_measure in request.measures:
                # Get each risk measure from from the request and the corresponding positions --> futures dict
                positions_for_measure = self.__futures[(request.scenario, risk_measure)]

                # Get the results for this measure
                position_results = results.pop(risk_measure, {})

                for position in request.positions:
                    # Set the result for this position to the returned value or an error if missing
                    result = position_results.get(position, ErrorValue(self.pricing_key, error=error))
                    if self.__use_cache and not isinstance(result, ErrorValue):
                        # Populate the cache
                        PricingCache.put(position.instrument, risk_measure, result)

                        # Retrieve from the cache - this is used by HistoricalPricingContext. We ensure the cache has
                        # all values (in case some had already been computed) then populate the result as the final step
                        result = PricingCache.get(position.instrument, risk_measure)

                    # Set the result for the future
                    positions_for_measure.pop(position).set_result(result)

                if not positions_for_measure:
                    self.__futures.pop((request.scenario, risk_measure))

    @property
    def __parameters(self) -> RiskRequestParameters:
        return RiskRequestParameters(self.__csa_term)

    @property
    def __scenario(self) -> Optional[MarketDataScenario]:
        scenarios = Scenario.path
        if not scenarios:
            return None

        return MarketDataScenario(scenario=scenarios[0] if len(scenarios) == 1 else
                                  CompositeScenario(scenarios=tuple(reversed(scenarios))))

    @property
    def _pricing_market_data_as_of(self) -> Tuple[PricingDateAndMarketDataAsOf, ...]:
        return PricingDateAndMarketDataAsOf(self.pricing_date, self.market_data_as_of),

    @property
    def pricing_date(self) -> dt.date:
        """Pricing date"""
        return self.__pricing_date

    @property
    def market_data_as_of(self) -> Union[dt.date, dt.datetime]:
        """Market data as of"""
        if self.__market_data_as_of:
            return self.__market_data_as_of
        elif self.pricing_date == dt.date.today():
            return business_day_offset(self.pricing_date, -1, roll='preceding')
        else:
            return self.pricing_date

    @property
    def market_data_location(self) -> str:
        """Market data location"""
        return self.__market_data_location

    @property
    def use_cache(self) -> bool:
        """Cache results"""
        return self.__use_cache

    @property
    def visible_to_gs(self) -> bool:
        """Request contents visible to GS"""
        return self.__visible_to_gs

    @property
    def pricing_key(self) -> PricingKey:
        """A key representing information about the pricing environment"""
        return PricingKey(
            self._pricing_market_data_as_of,
            self.__market_data_location,
            self.__parameters,
            self.__scenario)

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
        position = RiskPosition(priceable, priceable.get_quantity())
        multiple_measures = not isinstance(risk_measure, RiskMeasure)
        futures = {}

        with self.__lock:
            for measure in risk_measure if multiple_measures else (risk_measure,):
                scenario = self.__scenario
                measure_future = self.__futures.get((scenario, measure), {}).get(position)

                if measure_future is None:
                    measure_future = PricingFuture(self)
                    if self.__use_cache:
                        cached_result = PricingCache.get(priceable, risk_measure)
                        if cached_result:
                            measure_future.set_result(cached_result)

                    if not measure_future.done():
                        self.__risk_measures_in_scenario_by_provider_and_position.setdefault(
                            priceable.provider(), {}).setdefault(
                            position, {}).setdefault(scenario, set()).add(measure)
                        self.__futures.setdefault((scenario, measure), {})[position] = measure_future

                futures[measure] = measure_future

        future = MultipleRiskMeasureFuture(futures, result_future=PricingFuture(self)) if multiple_measures else\
            futures[risk_measure]

        if not (self.is_entered or self.__is_async):
            if not future.done():
                self._calc()

            return future.result()
        else:
            return future

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
        resolution_key = self.pricing_key

        if priceable.resolution_key:
            if in_place:
                if resolution_key != priceable.resolution_key:
                    _logger.warning(
                        'Calling resolve() on an instrument already resolved under a different PricingContext')

                return
            elif resolution_key == priceable.resolution_key:
                return copy.copy(priceable)

        result = self.calc(priceable, ResolvedInstrumentValues)
        if in_place:
            def handle_result(result_):
                priceable.unresolved = copy.copy(priceable)
                priceable.from_instance(result_)
                priceable.resolution_key = result_.resolution_key

            if isinstance(result, Future):
                result.add_done_callback(lambda f: handle_result(f.result()))
            else:
                handle_result(result)
                return

        return result


class LivePricingContext(PricingContext):

    def __init__(self,
                 market_data_location: Optional[str] = None,
                 is_async: bool = False,
                 is_batch: bool = False,
                 visible_to_gs: bool = False,
                 csa_term: Optional[str] = None
                 ):
        # TODO we use 23:59:59.999999 as a sentinel value to indicate live pricing for now. Fix this
        d = business_day_offset(dt.date.today(), -1, roll='preceding')
        super().__init__(
            pricing_date=dt.date.today(),
            market_data_as_of=dt.datetime(d.year, d.month, d.day, 23, 59, 59, 999999),
            market_data_location=market_data_location,
            is_async=is_async,
            is_batch=is_batch,
            use_cache=False,
            visible_to_gs=visible_to_gs,
            csa_term=csa_term
        )
