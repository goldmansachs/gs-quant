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
from gs_quant.base import get_enum_value, InstrumentBase
from gs_quant.common import AssetClass, AssetType, XRef
from gs_quant.priceable import PriceableImpl

from abc import ABCMeta
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
            if hasattr(cls, 'asset_class'):
                return cls._from_dict(values)
            else:
                asset_class_field = next((f for f in ('asset_class', 'assetClass') if f in values), None)
                if not asset_class_field:
                    raise ValueError('assetClass/asset_class not specified')

                return cls.__asset_class_and_type_to_instrument().get((
                    get_enum_value(AssetClass, values.pop(asset_class_field)),
                    get_enum_value(AssetType, values.pop('type'))), Security)._from_dict(values)


class Security(XRef, Instrument):

    """A security, specified by a well-known identifier"""

    def __init__(self,
                 ticker: str=None,
                 bbid: str=None,
                 isin: str=None,
                 cusip: str=None,
                 prime_id: str=None,
                 quantity: float=1):
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
