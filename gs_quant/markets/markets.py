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
from abc import ABC, ABCMeta
import datetime as dt
from typing import Optional, Union

from gs_quant.base import get_enum_value
from gs_quant.common import PricingLocation
from gs_quant.datetime.date import prev_business_date


def closing_market_date(location: Optional[Union[PricingLocation, str]] = None) -> dt.date:
    return prev_business_date(dt.date.today(),
                              calendars=location.value if isinstance(location, PricingLocation) else location)


class Market(ABC):

    def __init__(self, location: Union[str, PricingLocation]):
        self.__location = location if isinstance(location, PricingLocation) else\
            get_enum_value(PricingLocation, location)

    @property
    def location(self):
        return self.__location


class AsOfMarket(Market, metaclass=ABCMeta):

    def __init__(self, location: Union[str, PricingLocation], as_of: Union[dt.date, dt.datetime]):
        super().__init__(location)
        self.__as_of = as_of

    def __eq__(self, other):
        return self.location == other.location and self.__as_of == other.__as_of

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__as_of) ^ hash(self.location)

    def __lt__(self, other):
        return self.location < other.location and self.as_of < self.as_of

    def __repr__(self):
        return '{} ({})'.format(self.as_of, self.location.value)

    @property
    def as_of(self) -> Union[dt.date, dt.datetime]:
        return self.__as_of


class ClosingMarket(AsOfMarket):

    __cache = {}

    def __init__(self, location: Union[str, PricingLocation], date: Optional[dt.date] = None):
        date = date or self.__cache.get(location)
        if date is None:
            date = self.__cache[location] = closing_market_date(location)

        super().__init__(location, date)


class LiveMarket(AsOfMarket):

    def __init__(self, location: Union[str, PricingLocation]):
        # TODO we use 23:59:59.999999 as a sentinel value to indicate live pricing for now. Fix this
        date = closing_market_date(location)
        super().__init__(location, dt.datetime(date.year, date.month, date.day, 23, 59, 59, 999999))

    def __repr__(self):
        return 'LIVE ({})'.format(self.location.value)
