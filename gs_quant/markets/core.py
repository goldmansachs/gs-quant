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


import datetime as dt
from typing import Optional, Union

from gs_quant.context_base import ContextBaseWithDefault
from gs_quant.datetime.date import business_day_offset
from gs_quant.target.common import MarketDataCoordinate as __MarketDataCoordinate


class MarketDataCoordinate(__MarketDataCoordinate):

    def __init__(self, *args, **kwargs):
        self.__quotingStyle = kwargs.pop('quotingStyle', None)
        super().__init__(*args, **kwargs)

    def __str__(self):
        return "|".join(f or '' for f in (self.marketDataType, self.marketDataAsset or self.assetId, self.pointClass, '_'.join(self.marketDataPoint), self.field or self.quotingStyle))

    @property
    def quotingStyle(self) -> str:
        """The specific field: bid, mid, rate etc"""
        return self.__quotingStyle

    @quotingStyle.setter
    def quotingStyle(self, value: str):
        self.__quotingStyle = value
        self._property_changed('quotingStyle')


class MarketDataContext(ContextBaseWithDefault):

    """A context for controlling market data source"""

    def __init__(self, as_of: Optional[Union[dt.date, dt.datetime]]=None, location: Optional[str]=None):
        """
        A context for controlling the source of market data used in calculations

        :param as_of: The date or datetime to source market data (N.B., only date is currently supported). Defaults to the previous business day.
        :param location: The location of the market data (LDN, NYC, HKG). Defaults to NYC

        **Examples**

        Set the default market data context:

        >>> import datetime as dt
        >>> MarketDataContext.current = MarketDataContext(as_of=dt.date.today(), location='NYC')

        Use a temporary market data context in conjunction with a PricingContext:

        >>> from gs_quant.instrument import IRCap, IRSwap
        >>> from gs_quant.datetime.date import business_day_offset
        >>> from gs_quant.markets import MarketDataContext
        >>> from gs_quant.risk import PricingContext
        >>> import datetime as dt
        >>>
        >>> swap = IRSwap('Pay', '10y', 'USD')
        >>> cap = IRCap('1y', 'EUR')
        >>> as_of = business_day_offset(dt.date.today(), -2, roll='preceding')
        >>>
        >>> with PricingContext(), MarketDataContext(as_of=as_of, location='LDN'):
        >>>     swap_price_f = swap.price()
        >>>     cap_price_f = cap.price()
        >>>
        >>> swap_price = swap_price_f.result()
        >>> cap_price = cap_price_f.result()
        """
        super().__init__()
        self.__as_of = as_of or business_day_offset(dt.date.today(), -1, roll='preceding')
        self.__location = location or 'NYC'

    @property
    def as_of(self) -> Union[dt.date, dt.datetime]:
        """
        As of date/datetime for market data
        """
        return self.__as_of

    @property
    def location(self) -> str:
        """
        Market data location
        """
        return self.__location
