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
from typing import Tuple, Union

import numpy as np

from gs_quant.data import Dataset


class GsCalendar:

    __CALENDAR_CACHE = {}

    DATE_LOW_LIMIT = dt.date(1952, 1, 1)
    DATE_HIGH_LIMIT = dt.date(2052, 12, 31)
    DEFAULT_WEEK_MASK = '1111100'  # Default to Sat, Sun weekend days

    def __init__(self, calendars: Union[str, Tuple[str, ...]] = ()):
        if isinstance(calendars, str):
            calendars = (calendars,)

        self.__calendars = calendars
        self.__holidays = set()
        self.__business_day_calendars = {}

    @staticmethod
    def get(calendars: Union[str, Tuple]):
        if isinstance(calendars, str):
            calendars = (calendars,)

        return GsCalendar.__CALENDAR_CACHE.setdefault(calendars, GsCalendar(calendars))

    @staticmethod
    def reset():
        GsCalendar.__CALENDAR_CACHE = set()

    def calendars(self) -> Tuple:
        return self.__calendars

    @property
    def holidays(self) -> set:
        if self.__calendars and not self.__holidays:
            dataset = Dataset(Dataset.GS.HOLIDAY)
            for holiday_id in self.__calendars:
                data = dataset.get_data(exchange=holiday_id, start=self.DATE_LOW_LIMIT, end=self.DATE_HIGH_LIMIT)
                if not data.empty:
                    self.__holidays.update(data.index.values.astype('datetime64[D]'))

        return self.__holidays

    def business_day_calendar(self, week_mask: str = None) -> np.busdaycalendar:
        return self.__business_day_calendars.setdefault(week_mask, np.busdaycalendar(
            weekmask=week_mask or self.DEFAULT_WEEK_MASK, holidays=tuple(self.holidays)))
