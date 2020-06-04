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
from gs_quant.base import Priceable, RiskKey
from gs_quant.markets import MarketDataCoordinate, HistoricalPricingContext, PricingCache, PricingContext
from gs_quant.risk import DataFrameWithInfo, DollarPrice, ErrorValue, FloatWithInfo, MarketDataAssets, Price,\
    ResolvedInstrumentValues, RiskMeasure, SeriesWithInfo
from gs_quant.risk.results import MultipleRiskMeasureFuture, PricingFuture

from gs_quant.session import GsSession

from abc import ABCMeta
import copy
import itertools
import logging
from typing import Iterable, Optional, Tuple, Union

__asset_class_and_type_to_instrument = {}
_logger = logging.getLogger(__name__)


class PriceableImpl(Priceable, metaclass=ABCMeta):

    """A priceable, such as a derivative instrument"""

    PROVIDER = None

    def __init__(self):
        super().__init__()
        self.resolution_key: Optional[RiskKey] = None
        self.unresolved: Optional[Priceable] = None

    def __getattribute__(self, name):
        resolved = False

        try:
            resolved = super().__getattribute__('resolution_key') is not None
        except AttributeError:
            pass

        ret = super().__getattribute__(name)

        if ret is None and GsSession.current_is_set and not resolved:
            attr = getattr(super().__getattribute__('__class__'), name, None)
            if attr and isinstance(attr, property):
                resolved_inst = self.resolve(in_place=False)
                if isinstance(resolved_inst, PricingFuture):
                    ret = PricingFuture()
                    resolved_inst.add_done_callback(lambda inst_f: ret.set_result(
                        object.__getattribute__(inst_f.result(), name)))
                else:
                    ret = object.__getattribute__(resolved_inst, name)

        return ret

    def _property_changed(self, prop: str):
        if self._hash_is_calced:
            PricingCache.drop(self)

        super()._property_changed(prop)

        if self.resolution_key and self.unresolved:
            unresolved = self.unresolved
            self.unresolved = None
            self.from_instance(unresolved)
            self.resolution_key = None

    def get_quantity(self) -> float:
        """
        Quantity of the instrument
        """
        return 1

    def resolve(self, in_place: bool = True) -> Optional[Priceable]:
        """
        Resolve non-supplied properties of an instrument

        **Examples**

        >>> from gs_quant.instrument import IRSwap
        >>>
        >>> swap = IRSwap('Pay', '10y', 'USD')
        >>> rate = swap.fixedRate

        rate is None

        >>> swap.resolve()
        >>> rate = swap.fixedRate

        rates is now the solved fixed rate
        """
        def handle_result(result: Optional[Union[ErrorValue, Priceable]]) -> Optional[Priceable]:
            ret = None if in_place else result
            if isinstance(result, ErrorValue):
                _logger.error('Failed to resolve instrument fields: ' + result.error)
                ret = self
            elif result is None:
                _logger.error('Unknown error resolving instrument fields')
                ret = self
            else:
                if in_place:
                    self.unresolved = copy.copy(self)
                    self.from_instance(result)

            return ret

        if in_place and isinstance(PricingContext.current, HistoricalPricingContext):
            raise RuntimeError('Cannot resolve in place under a HistoricalPricingContext')

        return self.calc(ResolvedInstrumentValues, fn=handle_result)

    def dollar_price(self) -> Union[FloatWithInfo, PricingFuture, SeriesWithInfo]:
        """
        Present value in USD

        :return:  a float or a future, depending on whether the current PricingContext is async, or has been entered

        **Examples**

        >>> from gs_quant.instrument import IRCap
        >>>
        >>> cap = IRCap('1y', 'EUR')
        >>> price = cap.dollar_price()

        price is the present value in USD (a float)

        >>> cap_usd = IRCap('1y', 'USD')
        >>> cap_eur = IRCap('1y', 'EUR')
        >>>
        >>> from gs_quant.markets import PricingContext
        >>>
        >>> with PricingContext():
        >>>     price_usd_f = cap_usd.dollar_price()
        >>>     price_eur_f = cap_eur.dollar_price()
        >>>
        >>> price_usd = price_usd_f.result()
        >>> price_eur = price_eur_f.result()

        price_usd_f and price_eur_f are futures, price_usd and price_eur are floats
        """
        return self.calc(DollarPrice)

    def price(self) -> Union[FloatWithInfo, PricingFuture, SeriesWithInfo]:
        """
        Present value in local currency. Note that this is not yet supported on all instruments

        ***Examples**

        >>> from gs_quant.instrument import IRSwap
        >>>
        >>> swap = IRSwap('Pay', '10y', 'EUR')
        >>> price = swap.price()

        price is the present value in EUR (a float)
        """
        return self.calc(Price)

    def coordinates(self) -> Tuple[MarketDataCoordinate, ...]:
        from gs_quant.api.gs.data import GsDataApi

        def coordinates_for_asset(result: DataFrameWithInfo):
            return tuple(itertools.chain.from_iterable(GsDataApi.get_many_coordinates(mkt_type=t,
                                                                                      mkt_asset=a,
                                                                                      return_type=MarketDataCoordinate,
                                                                                      limit=10000)
                                                       for t, a in zip(result.mkt_type, result.mkt_asset)))

        return self.calc(MarketDataAssets, fn=coordinates_for_asset)

    def calc(self, risk_measure: Union[RiskMeasure, Iterable[RiskMeasure]], fn=None)\
            -> Union[DataFrameWithInfo, ErrorValue, FloatWithInfo, Priceable, PricingFuture, SeriesWithInfo,
                     Tuple[MarketDataCoordinate, ...]]:
        """
        Calculate the value of the risk_measure

        :param risk_measure: the risk measure to compute, e.g. IRDelta (from gs_quant.risk)
        :param fn: post-processing function (optional)
        :return: a float or dataframe, depending on whether the value is scalar or structured, or a future thereof
        (depending on how PricingContext is being used)

        **Examples**

        >>> from gs_quant.instrument import IRCap
        >>> from gs_quant.risk import IRDelta
        >>>
        >>> cap = IRCap('1y', 'USD')
        >>> delta = cap.calc(IRDelta)

        delta is a dataframe

        >>> from gs_quant.instrument import EqOption
        >>> from gs_quant.risk import EqDelta
        >>>
        >>> option = EqOption('.SPX', '3m', 'ATMF', 'Call', 'European')
        >>> delta = option.calc(EqDelta)

        delta is a float

        >>> from gs_quant.markets import PricingContext
        >>>
        >>> cap_usd = IRCap('1y', 'USD')
        >>> cap_eur = IRCap('1y', 'EUR')

        >>> with PricingContext():
        >>>     usd_delta_f = cap_usd.calc(IRDelta)
        >>>     eur_delta_f = cap_eur.calc(IRDelta)
        >>>
        >>> usd_delta = usd_delta_f.result()
        >>> eur_delta = eur_delta_f.result()

        usd_delta_f and eur_delta_f are futures, usd_delta and eur_delta are dataframes
        """
        futures = {r: r.pricing_context.calc(self, r)
                   for r in ((risk_measure,) if isinstance(risk_measure, RiskMeasure) else risk_measure)}
        future = MultipleRiskMeasureFuture(futures) if len(futures) > 1 else futures[risk_measure]

        if fn is not None:
            ret = PricingFuture()

            def cb(f):
                try:
                    ret.set_result(fn(f.result()))
                except Exception as e:
                    ret.set_exception(e)

            future.add_done_callback(cb)
            future = ret

        return future.result() if not (PricingContext.current.is_entered or PricingContext.current.is_async) else future
