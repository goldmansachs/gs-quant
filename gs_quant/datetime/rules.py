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

import calendar
import logging
from abc import ABC, abstractmethod
from datetime import date, timedelta
from typing import List, Union

from dateutil.relativedelta import relativedelta, FR, SA, SU, TH, TU, WE, MO
from numpy import busday_offset
from pandas import to_datetime

from gs_quant.datetime.gscalendar import GsCalendar
from gs_quant.markets.securities import ExchangeCode
from gs_quant.common import Currency

_logger = logging.getLogger(__name__)


class RDateRule(ABC):
    result: date
    number: int
    week_mask: str
    currencies: List[Union[Currency, str]] = None
    exchanges: List[Union[ExchangeCode, str]] = None
    holiday_calendar: List[date] = None

    def __init__(self, result: date, **params):
        self.result = result
        self.number = params.get('number')
        self.week_mask = params.get('week_mask')
        self.currencies = params.get('currencies')
        self.exchanges = params.get('exchanges')
        self.holiday_calendar = params.get('holiday_calendar')
        self.usd_calendar = params.get('usd_calendar')
        super().__init__()

    @abstractmethod
    def handle(self) -> date:
        """
        Handle RDate Rule. Use any available class field to compute.
        :return: date
        """
        pass

    def _get_holidays(self) -> List[date]:
        if self.holiday_calendar is not None:
            if self.usd_calendar is None:
                return self.holiday_calendar
            return list(set().union(self.holiday_calendar, self.usd_calendar))
        try:
            currencies = [] if self.currencies is None else [self.currencies] if isinstance(self.currencies,
                                                                                            str) else self.currencies
            exchanges = [] if self.exchanges is None else [self.exchanges] if isinstance(self.exchanges,
                                                                                         str) else self.exchanges
            cal = GsCalendar(exchanges + currencies)
            return cal.holidays
        except Exception as e:
            _logger.warning('Unable to fetch holiday calendar. Try passing your own when applying a rule. {}'.format(e))
            return []

    def _apply_business_days_logic(self, holidays: List[date], offset: int = None, roll: str = 'preceding'):
        if offset is not None:
            offset_to_use = offset
        else:
            offset_to_use = self.number if self.number else 0
        return to_datetime(busday_offset(self.result, offset_to_use, roll,
                                         holidays=holidays, weekmask=self.week_mask)).date()

    def _get_nth_day_of_month(self, calendar_day):
        temp = self.result.replace(day=1)
        adj = (calendar_day - temp.weekday()) % 7
        temp += relativedelta(days=adj)
        temp += relativedelta(weeks=self.number - 1)
        return temp

    def add_years(self, holidays: List[date]):
        self.result = (self.result + relativedelta(years=self.number))
        if self.result.isoweekday() in {6, 7}:
            self.result += timedelta(days=self.result.isoweekday() % 5)
        return self._apply_business_days_logic(holidays, offset=0)

    @staticmethod
    def is_weekend(d: date):
        return False if d.weekday() < 5 else True  # 5 Sat, 6 Sun


class ARule(RDateRule):
    def handle(self) -> date:
        result = self.result.replace(month=1, day=1)
        return result + relativedelta(year=self.number)


class bRule(RDateRule):
    def handle(self) -> date:
        holidays = self._get_holidays()
        roll = 'forward' if self.number <= 0 else 'preceding'
        return self._apply_business_days_logic(holidays, offset=self.number, roll=roll)


class dRule(RDateRule):
    def handle(self) -> date:
        return self.result + relativedelta(days=self.number)


class eRule(RDateRule):
    def handle(self) -> date:
        month_range = calendar.monthrange(self.result.year, self.result.month)
        return self.result.replace(day=month_range[1])


class FRule(RDateRule):
    def handle(self) -> date:
        return self._get_nth_day_of_month(calendar.FRIDAY)


class gRule(RDateRule):
    def handle(self) -> date:
        self.result = self.result + relativedelta(weeks=self.number)
        holidays = self._get_holidays()
        return self._apply_business_days_logic(holidays, offset=0)


class NRule(RDateRule):
    def handle(self) -> date:
        return self.result + relativedelta(weekday=MO(self.number))


class GRule(RDateRule):
    def handle(self) -> date:
        return self.result + relativedelta(weekday=FR(self.number))


class IRule(RDateRule):
    def handle(self) -> date:
        return self.result + relativedelta(weekday=SA(self.number))


class JRule(RDateRule):
    def handle(self) -> date:
        return self.result.replace(day=1)


class kRule(RDateRule):
    def handle(self) -> date:
        self.result = self.result + relativedelta(years=self.number)
        while self.week_mask[self.result.isoweekday() - 1] == '0':
            self.result += relativedelta(days=1)
        holidays = self._get_holidays()
        return self._apply_business_days_logic(holidays, offset=0)


class mRule(RDateRule):
    def handle(self) -> date:
        self.result = self.result + relativedelta(months=self.number)
        return self._apply_business_days_logic(self._get_holidays(), offset=0, roll='forward')


class MRule(RDateRule):
    def handle(self) -> date:
        return self._get_nth_day_of_month(calendar.MONDAY)


class PRule(RDateRule):
    def handle(self) -> date:
        return self.result + relativedelta(weekday=SU(self.number))


class rRule(RDateRule):
    def handle(self) -> date:
        return self.result.replace(month=12, day=31) + relativedelta(years=self.number)


class RRule(RDateRule):
    def handle(self) -> date:
        return self._get_nth_day_of_month(calendar.THURSDAY)


class SRule(RDateRule):
    def handle(self) -> date:
        return self.result + relativedelta(weekday=TH(self.number))


class TRule(RDateRule):
    def handle(self) -> date:
        return self._get_nth_day_of_month(calendar.TUESDAY)


class uRule(RDateRule):
    def __init__(self, result: date, **params):
        super().__init__(result, **params)
        self.roll = params.get('roll')

    def handle(self) -> date:
        holidays = self._get_holidays()
        if self.number == 0 and self.roll:
            roll = self.roll
        else:
            roll = 'forward' if self.number <= 0 else 'preceding'
        return self._apply_business_days_logic(holidays, offset=self.number, roll=roll)


class URule(RDateRule):
    def handle(self) -> date:
        return self.result + relativedelta(weekday=TU(self.number))


class vRule(RDateRule):
    def handle(self) -> date:
        self.result = self.result + relativedelta(months=self.number) if self.number else self.result
        month_range = calendar.monthrange(self.result.year, self.result.month)
        self.result = self.result.replace(day=month_range[1])
        holidays = self._get_holidays()
        return self._apply_business_days_logic(holidays, offset=0, roll='backward')


class VRule(RDateRule):
    def handle(self) -> date:
        return self._get_nth_day_of_month(calendar.SATURDAY)


class WRule(RDateRule):
    def handle(self) -> date:
        return self._get_nth_day_of_month(calendar.WEDNESDAY)


class wRule(RDateRule):
    def handle(self) -> date:
        self.result = self.result + relativedelta(weeks=self.number)
        holidays = self._get_holidays()
        return self._apply_business_days_logic(holidays, offset=0)


class xRule(RDateRule):
    def handle(self) -> date:
        month_range = calendar.monthrange(self.result.year, self.result.month)
        self.result = self.result.replace(day=month_range[1])
        holidays = self._get_holidays()
        return self._apply_business_days_logic(holidays, offset=0, roll='backward')


class XRule(RDateRule):
    def handle(self) -> date:
        return self.result + relativedelta(weekday=WE(self.number))


class yRule(RDateRule):
    def handle(self) -> date:
        self.result = self.result + relativedelta(years=self.number)
        while self.week_mask[self.result.isoweekday() - 1] == '0':
            self.result += relativedelta(days=1)
        holidays = self._get_holidays()
        return self._apply_business_days_logic(holidays, offset=0)


class ZRule(RDateRule):
    def handle(self) -> date:
        return self._get_nth_day_of_month(calendar.SUNDAY)
