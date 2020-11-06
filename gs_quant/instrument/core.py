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
from gs_quant.api.gs.parser import GsParserApi
from gs_quant.api.gs.risk import GsRiskApi
from gs_quant.base import get_enum_value, InstrumentBase, QuotableBuilder
from gs_quant.common import AssetClass, AssetType, XRef
from gs_quant.context_base import do_not_serialise
from gs_quant.markets import HistoricalPricingContext, MarketDataCoordinate, PricingCache, PricingContext
from gs_quant.priceable import PriceableImpl
from gs_quant.risk import FloatWithInfo, DataFrameWithInfo, SeriesWithInfo, ResolvedInstrumentValues, RiskMeasure
from gs_quant.risk.results import ErrorValue, MultipleRiskMeasureFuture, PricingFuture
from gs_quant.session import GsSession

from abc import ABCMeta
import datetime as dt
import logging
from typing import Iterable, Optional, Tuple, Union
import inspect

_logger = logging.getLogger(__name__)


class Instrument(PriceableImpl, InstrumentBase, metaclass=ABCMeta):
    PROVIDER = GsRiskApi
    __instrument_mappings = {}

    def __getattribute__(self, name):
        ret = super().__getattribute__(name)
        if ret is not None or name not in self.properties():
            return ret

        attr = getattr(super().__getattribute__('__class__'), name, None)
        if getattr(attr.fget, 'do_not_resolve', False):
            return ret

        resolved = False

        try:
            resolved = super().__getattribute__('resolution_key') is not None
        except AttributeError:
            pass

        if GsSession.current_is_set and not resolved:
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

    @classmethod
    def __asset_class_and_type_to_instrument(cls):
        if not cls.__instrument_mappings:
            import gs_quant.target.instrument as instrument_
            instrument_classes = [c for _, c in inspect.getmembers(instrument_, inspect.isclass) if
                                  issubclass(c, Instrument) and c is not Instrument]

            cls.__instrument_mappings[(AssetClass.Cash, AssetType.Currency)] = instrument_.Forward

            for clazz in instrument_classes:
                instrument = clazz.default_instance()
                cls.__instrument_mappings[(instrument.asset_class, instrument.type)] = clazz

        return cls.__instrument_mappings

    @property
    @do_not_serialise
    def provider(self):
        return self.PROVIDER

    def resolve(self, in_place: bool = True) -> Optional[Union[PriceableImpl, PricingFuture, dict]]:
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

        is_historical = isinstance(PricingContext.current, HistoricalPricingContext)

        def handle_result(result: Optional[Union[ErrorValue, InstrumentBase]]) -> Optional[PriceableImpl]:
            ret = None if in_place else result
            if isinstance(result, ErrorValue):
                _logger.error('Failed to resolve instrument fields: ' + result.error)
                ret = {result.risk_key.date: self} if is_historical else self
            elif result is None:
                _logger.error('Unknown error resolving instrument fields')
                ret = {dt.date.today(): self} if is_historical else self
            elif in_place:
                self.from_instance(result)

            return ret

        if in_place and is_historical:
            raise RuntimeError('Cannot resolve in place under a HistoricalPricingContext')

        return self.calc(ResolvedInstrumentValues, fn=handle_result)

    def calc(self, risk_measure: Union[RiskMeasure, Iterable[RiskMeasure]], fn=None) \
            -> Union[DataFrameWithInfo, ErrorValue, FloatWithInfo, PriceableImpl, PricingFuture,
                     SeriesWithInfo, Tuple[MarketDataCoordinate, ...]]:
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
        future = MultipleRiskMeasureFuture(self, futures) if len(futures) > 1 else futures[
            risk_measure if isinstance(risk_measure, RiskMeasure) else risk_measure[0]]

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

    @classmethod
    def from_dict(cls, values: dict):
        if values:
            if issubclass(cls, QuotableBuilder):
                if 'properties' in values:
                    values.update(values.pop('properties'))
                return cls._from_dict(values)
            elif hasattr(cls, 'asset_class'):
                return cls._from_dict(values)
            else:
                if '$type' in values:
                    from gs_quant_internal import tdapi
                    tdapi_cls = getattr(tdapi, values['$type'].replace('Defn', 'Builder'))
                    if not tdapi_cls:
                        raise RuntimeError('Cannot resolve TDAPI type {}'.format(tdapi_cls))

                    return tdapi_cls.from_dict(values)

                asset_class_field = next((f for f in ('asset_class', 'assetClass') if f in values), None)
                if not asset_class_field:
                    raise ValueError('assetClass/asset_class not specified')
                if 'type' not in values:
                    raise ValueError('type not specified')

                asset_type = values.pop('type')
                asset_class = values.pop(asset_class_field)
                default_type = Security if asset_type in [None, "", "Security"] and asset_class in [None, "",
                                                                                                    "Security"] \
                    else None

                instrument = cls.__asset_class_and_type_to_instrument().get((
                    get_enum_value(AssetClass, asset_class),
                    get_enum_value(AssetType, asset_type)), default_type)

                if instrument is None:
                    raise ValueError('unable to build instrument')

                return instrument._from_dict(values)

    @classmethod
    def from_quick_entry(cls, text: str, asset_class: Optional[AssetClass] = None):
        if not asset_class:
            try:
                inst = cls.default_instance()
                asset_class = inst.asset_class
            except AttributeError:
                pass

        if not asset_class:
            res = GsParserApi.get_instrument_from_text(text)
            if len(res):  # multiple instruments returned
                instrument = res.pop(0)
            else:
                raise ValueError('Could not resolve instrument')
        else:
            instrument = GsParserApi.get_instrument_from_text_asset_class(text, asset_class.value)
        try:
            return cls.from_dict(instrument)
        except AttributeError:
            raise ValueError('Invalid instrument specification')

    @classmethod
    def from_asset_ids(cls, asset_ids: Tuple[str, ...]) -> Tuple[InstrumentBase, ...]:
        from gs_quant.api.gs.assets import GsAssetApi
        instruments = GsAssetApi.get_instruments_for_asset_ids(asset_ids)

        try:
            inst = cls.default_instance()
            asset_class = inst.asset_class
            asset_type = inst.type

            if not all(i.asset_class == asset_class and i.type == asset_type for i in instruments):
                raise ValueError(f'Instrument(s) not all of type {cls.__name__}')
        except AttributeError:
            pass

        return instruments

    @classmethod
    def from_asset_id(cls, asset_id: str) -> InstrumentBase:
        return cls.from_asset_ids((asset_id,))[0]

    @staticmethod
    def compose(components: Iterable):
        return {c.risk_key.date if isinstance(c, ErrorValue) else c.resolution_key.date: c for c in components}


class Security(XRef, Instrument):
    """A security, specified by a well-known identifier"""

    def __init__(self,
                 ticker: str = None,
                 bbid: str = None,
                 ric: str = None,
                 isin: str = None,
                 cusip: str = None,
                 prime_id: str = None,
                 quantity: float = 1):
        """
        Create a security by passing one identifier only and, optionally, a quantity

        :param ticker: Exchange ticker
        :param bbid: Bloomberg identifier
        :param isin: International Security Number
        :param cusip: CUSIP
        :param prime_id: Prime (GS internal) identifier
        :param quantity: Quantity (number of contracts for exchange-traded instruments, notional for bonds)
        """
        if len(tuple(filter(None, (f is not None for f in (ticker, bbid, isin, cusip, prime_id))))) > 1:
            raise ValueError('Only specify one identifier')

        XRef.__init__(self, ticker=ticker, bbid=bbid, ric=ric, isin=isin, cusip=cusip, prime_id=prime_id)
        Instrument.__init__(self, quantity)
