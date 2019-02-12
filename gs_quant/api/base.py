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
    def properties(cls) -> tuple:
        """The public properties of this class"""
        return tuple(i for i in dir(cls) if isinstance(getattr(cls, i), property))

    def as_dict(self) -> dict:
        """Dictionary of the public non-null properties and values"""
        properties = self.properties()
        values = [getattr(self, p) for p in properties]
        return dict((p, v) for p, v in zip(properties, values) if v is not None)


class Priceable(Base):

    def price(self):
        from gs_quant.api.risk import PresentValue
        return self.calc(PresentValue)

    def calc(self, risk_measure):
        from gs_quant.api.pricing_context import PricingContext
        result = PricingContext.current.calc(self, risk_measure)
        if not result:
            raise RuntimeError('Failed to price')
        return result[0]

    def market_data_coordinates(self):
        from gs_quant.api.pricing_context import PricingContext
        return PricingContext.current.coordinates([self])


class Instrument(Priceable):
    pass