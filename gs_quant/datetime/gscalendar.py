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
from enum import Enum, EnumMeta

from cachetools import TTLCache
from cachetools.keys import hashkey
import datetime as dt
import numpy as np
from typing import Tuple, Union

from gs_quant.data import Dataset
from gs_quant.errors import MqRequestError
from gs_quant.common import PricingLocation, Currency

_calendar_cache = TTLCache(maxsize=128, ttl=600)


class GsCalendar:
    DATE_LOW_LIMIT = dt.date(1952, 1, 1)
    DATE_HIGH_LIMIT = dt.date(2052, 12, 31)
    DEFAULT_WEEK_MASK = '1111100'  # Default to Sat, Sun weekend days

    def __init__(self, calendars: Union[str, PricingLocation, Currency, Tuple[str, ...]] = ()):
        if isinstance(calendars, (str, PricingLocation, Currency)):
            calendars = (calendars,)
        if calendars is None:
            calendars = ()
        self.__calendars = calendars
        self.__business_day_calendars = {}

    @staticmethod
    def get(calendars: Union[str, Tuple]):
        return GsCalendar(calendars)

    @staticmethod
    def reset():
        _calendar_cache.clear()

    def calendars(self) -> Tuple:
        return self.__calendars

    @staticmethod
    def is_currency(currency: Union[str, PricingLocation, Currency]) -> bool:
        if isinstance(currency, Currency):
            return True
        if isinstance(currency, PricingLocation):
            return False
        try:
            _ = Currency(currency.upper())
            return True
        except (ValueError, AttributeError):
            return False

    @property
    def holidays(self) -> Tuple[dt.date]:
        holidays = []
        cached_data = _calendar_cache.get(hashkey(str(self.__calendars)))
        if cached_data:
            return cached_data
        exchanges = [x.value if isinstance(x, (Enum, EnumMeta)) else x.upper() for x in self.__calendars]
        if len(exchanges):
            try:
                dataset = Dataset(Dataset.GS.HOLIDAY)
                data = dataset.get_data(exchange=exchanges, start=self.DATE_LOW_LIMIT, end=self.DATE_HIGH_LIMIT)
                if not data.empty:
                    holidays = holidays + [d.date() for d in data.index.to_pydatetime()]
            except MqRequestError:
                pass

        currencies = [x.value if isinstance(x, Currency) else x.upper() for x in self.__calendars
                      if GsCalendar.is_currency(x)]
        if len(currencies):
            try:
                dataset = Dataset(Dataset.GS.HOLIDAY_CURRENCY)
                data = dataset.get_data(currency=currencies, start=self.DATE_LOW_LIMIT, end=self.DATE_HIGH_LIMIT)
                if not data.empty:
                    holidays = holidays + [d.date() for d in data.index.to_pydatetime()]
            except MqRequestError:
                pass

        holidays = tuple(set(holidays))
        _calendar_cache[hashkey(str(self.__calendars))] = holidays
        return holidays

    def business_day_calendar(self, week_mask: str = None) -> np.busdaycalendar:
        return self.__business_day_calendars.setdefault(week_mask, np.busdaycalendar(
            weekmask=week_mask or self.DEFAULT_WEEK_MASK, holidays=tuple([np.datetime64(d.isoformat())
                                                                          for d in self.holidays])))
