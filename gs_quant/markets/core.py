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
from typing import Optional, Union, Mapping

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

    """A context containing markets data parameters, such as as_of date/time and overrides"""

    def __init__(self, as_of: Optional[Union[dt.date, dt.datetime]]=None, location: Optional[str]=None):
        super().__init__()
        self.__as_of = as_of or business_day_offset(dt.date.today(), -1, roll='preceding')
        self.__location = location or 'NYC'

    @property
    def as_of(self) -> Union[dt.date, dt.datetime]:
        """
        As of date/time for market data
        """
        return self.__as_of

    @property
    def location(self) -> str:
        """
        Market data location
        """
        return self.__location
