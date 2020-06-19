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
from typing import Iterable

from gs_quant.base import get_enum_value, InstrumentBase, QuotableBuilder
from gs_quant.common import AssetClass, AssetType, XRef
from gs_quant.priceable import PriceableImpl
from gs_quant.api.gs.parser import GsParserApi

from abc import ABCMeta
from typing import Optional
import inspect


class Instrument(PriceableImpl, InstrumentBase, metaclass=ABCMeta):

    __instrument_mappings = {}

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

                return cls.__asset_class_and_type_to_instrument().get((
                    get_enum_value(AssetClass, values.pop(asset_class_field)),
                    get_enum_value(AssetType, values.pop('type'))), Security)._from_dict(values)

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
            instrument = GsParserApi.get_instrument_from_text_asset_class(text, asset_class)
        try:
            return cls.from_dict(instrument)
        except AttributeError:
            raise ValueError('Invalid instrument specification')

    @staticmethod
    def compose(components: Iterable):
        return {c.resolution_key.date: c for c in components}


class Security(XRef, Instrument):

    """A security, specified by a well-known identifier"""

    def __init__(self,
                 ticker: str = None,
                 bbid: str = None,
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

        super().__init__(ticker=ticker, bbid=bbid, isin=isin, cusip=cusip, prime_id=prime_id)
        self.quantity = quantity

    def get_quantity(self) -> float:
        """
        Quantity of the security
        """
        return self.quantity
