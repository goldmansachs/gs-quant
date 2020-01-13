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
from gs_quant.base import Priceable, PricingKey
from gs_quant.markets import PricingCache, PricingContext
from gs_quant.risk import DataFrameWithInfo, DollarPrice, ErrorValue, FloatWithInfo, Price, RiskMeasure, SeriesWithInfo
from gs_quant.risk.results import MultipleRiskMeasureFuture

from gs_quant.session import GsSession

from abc import ABCMeta
from concurrent.futures import Future
from typing import Iterable, Optional, Union

__asset_class_and_type_to_instrument = {}


class PriceableImpl(Priceable, metaclass=ABCMeta):

    """A priceable, such as a derivative instrument"""

    PROVIDER = None

    def __init__(self):
        super().__init__()
        self.resolution_key: PricingKey = None
        self.unresolved: Priceable = None

    def __getattribute__(self, name):
        resolved = False

        try:
            resolved = super().__getattribute__('resolution_key') is not None
        except AttributeError:
            pass

        if GsSession.current_is_set and not resolved:
            attr = getattr(super().__getattribute__('__class__'), name, None)
            if attr and isinstance(attr, property) and super().__getattribute__(name) is None:
                self.resolve()

        return super().__getattribute__(name)

    def _property_changed(self, prop: str):
        if self._hash_is_calced:
            PricingCache.drop(self)

        super()._property_changed(prop)

        if self.resolution_key and self.unresolved:
            self.resolution_key = None
            self.from_instance(self.unresolved)
            self.unresolved = None

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
        return PricingContext.current.resolve_fields(self, in_place)

    def dollar_price(self) -> Union[FloatWithInfo, Future, SeriesWithInfo]:
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

    def price(self) -> Union[FloatWithInfo, Future, SeriesWithInfo]:
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

    def calc(self, risk_measure: Union[RiskMeasure, Iterable[RiskMeasure]])\
            -> Union[list, DataFrameWithInfo, ErrorValue, FloatWithInfo, Future, MultipleRiskMeasureFuture,
                     SeriesWithInfo]:
        """
        Calculate the value of the risk_measure

        :param risk_measure: the risk measure to compute, e.g. IRDelta (from gs_quant.risk)
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
        return PricingContext.current.calc(self, risk_measure)
