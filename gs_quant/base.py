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
from concurrent.futures import Future
import pandas as pd
from typing import Union


class EnumBase:
    pass


class Base:

    def __init__(self):
        self.__calced_hash = None

    def _property_changed(self, prop):
        self.__calced_hash = None

    def __hash__(self):
        if self.__calced_hash is None:
            properties = (i for i in dir(self.__class__) if isinstance(getattr(self.__class__, i), property))
            prop = next(properties, None)
            self.__calced_hash = hash(getattr(self, prop)) if prop else 1
            for prop in properties:
                self.__calced_hash ^= hash(getattr(self, prop))

        return self.__calced_hash

    def __eq__(self, other):
        properties = (i for i in dir(self.__class__) if isinstance(getattr(self.__class__, i), property))
        return\
            type(self) == type(other) and\
            (self.__calced_hash is None or other.__calced_hash is None or self.__calced_hash == other.__calced_hash) and\
            all(getattr(self, p) == getattr(other, p) for p in properties)

    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def properties(cls) -> set:
        """The public properties of this class"""
        return set(i for i in dir(cls) if isinstance(getattr(cls, i), property))

    def as_dict(self) -> dict:
        """Dictionary of the public non-null properties and values"""
        properties = self.properties()
        values = [getattr(self, p) for p in properties]
        return dict((p, v) for p, v in zip(properties, values) if v is not None)


class Priceable(Base):

    PROVIDER = None

    def provider(self) -> 'RiskApi':
        if self.PROVIDER is None:
            from gs_quant.api.gs.risk import GsRiskApi
            self.PROVIDER = GsRiskApi

        return self.PROVIDER

    def resolve(self):
        from gs_quant.risk import PricingContext
        PricingContext.current.resolve_fields(self)

    def dollar_price(self) -> Union[float, Future]:
        from gs_quant.risk import DollarPrice
        return self.calc(DollarPrice)

    def price(self) -> Union[float, Future]:
        from gs_quant.risk import Price
        return self.calc(Price)

    def calc(self, risk_measure: 'RiskMeasure') -> Union[pd.DataFrame, Future]:
        from gs_quant.risk import PricingContext
        return PricingContext.current.calc(self, risk_measure)


class Instrument(Priceable):
    pass