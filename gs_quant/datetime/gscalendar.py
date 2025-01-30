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
import logging
from enum import Enum, EnumMeta
from threading import Lock
from typing import Tuple, Union, List

import numpy as np
from cachetools import TTLCache, cached
from cachetools.keys import hashkey

from gs_quant.common import PricingLocation, Currency
from gs_quant.data import Dataset
from gs_quant.errors import MqRequestError

_logger = logging.getLogger(__name__)

_calendar_cache = TTLCache(maxsize=128, ttl=600)
_coverage_cache = TTLCache(maxsize=128, ttl=3600)


def _split_list(items, predicate) -> Tuple[Tuple[str, ...], Tuple[str, ...]]:
    true_res = []
    false_res = []
    for item in items:
        item_str = item.value if isinstance(item, (Enum, EnumMeta)) else item.upper()
        if predicate(item):
            true_res.append(item_str)
        else:
            false_res.append(item_str)
    return tuple(true_res), tuple(false_res)


class GsCalendar:
    DATE_LOW_LIMIT = dt.date(1952, 1, 1)
    DATE_HIGH_LIMIT = dt.date(2052, 12, 31)
    DEFAULT_WEEK_MASK = '1111100'  # Default to Sat, Sun weekend days

    def __init__(self, calendars: Union[str, PricingLocation, Currency, Tuple[str, ...]] = (), skip_valid_check=True):
        if isinstance(calendars, (str, PricingLocation, Currency)):
            calendars = (calendars,)
        if calendars is None:
            calendars = ()
        self.__calendars = calendars
        self.__business_day_calendars = {}
        self._skip_valid_check = skip_valid_check

    @staticmethod
    def get(calendars: Union[str, Tuple], skip_valid_check=True):
        return GsCalendar(calendars, skip_valid_check)

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

    @cached(_coverage_cache, key=lambda s, d, q: d.id, lock=Lock())
    def _get_dataset_coverage(self, dataset: Dataset, query_key: str):
        coverage_df = dataset.get_coverage()
        coverage = set() if coverage_df.empty else set(coverage_df[query_key])
        return coverage

    def holidays_from_dataset(self, dataset: Dataset, query_key: str, query_values: Tuple[str, ...]) -> List[dt.date]:
        if not len(query_values):
            return []
        coverage = self._get_dataset_coverage(dataset, query_key)
        for item in query_values:
            if item not in coverage:
                if self._skip_valid_check:
                    _logger.warning(
                        f'Ignoring invalid calendar {item}. This will throw in future versions of gs-quant.')
                else:
                    raise ValueError(f'Invalid calendar {item}')
        try:
            data = dataset.get_data(**{query_key: query_values}, start=self.DATE_LOW_LIMIT, end=self.DATE_HIGH_LIMIT)
            if not data.empty:
                return [d.date() for d in data.index.to_pydatetime()]
        except MqRequestError:
            pass
        return []

    @property
    @cached(_calendar_cache, key=lambda s: hashkey(str(s.__calendars)), lock=Lock())
    def holidays(self) -> Tuple[dt.date, ...]:
        currencies, exchanges = _split_list(self.__calendars, GsCalendar.is_currency)
        holidays = self.holidays_from_dataset(Dataset(Dataset.GS.HOLIDAY), 'exchange', exchanges)
        holidays = holidays + self.holidays_from_dataset(Dataset(Dataset.GS.HOLIDAY_CURRENCY), 'currency', currencies)
        holidays = tuple(set(holidays))
        return holidays

    def business_day_calendar(self, week_mask: str = None) -> np.busdaycalendar:
        return self.__business_day_calendars.setdefault(week_mask, np.busdaycalendar(
            weekmask=week_mask or self.DEFAULT_WEEK_MASK, holidays=tuple([np.datetime64(d.isoformat())
                                                                          for d in self.holidays])))
