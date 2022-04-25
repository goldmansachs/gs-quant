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

import logging
from copy import copy
from datetime import date, datetime
from typing import Union, Optional, List

from pandas import Timestamp

import gs_quant.datetime.rules as rules
from gs_quant.errors import MqValueError
from gs_quant.markets import PricingContext
from gs_quant.markets.securities import ExchangeCode
from gs_quant.target.common import Currency

_logger = logging.getLogger(__name__)


class RelativeDate:
    """
    RelativeDates are objects which provide utilities for getting dates given a relative date rule.
    Some rules require a business day calendar.

    :param rule: Rule to use
    :param base_date: Base date to use (Optional).
    :return: new RelativeDate object

    **Usage**

    Create a RelativeDate object and then call `apply_rule` to get a date back.

    **Examples**

    RelativeDate to return relative previous day:

    >>> my_date: date = RelativeDate('-1d').apply_rule()

    **Documentation**

    Full Documentation and examples can be found here:
    https://developer.gs.com/docs/gsquant/api/datetime.html

    """

    def __init__(self,
                 rule: str,
                 base_date: Optional[date] = None):
        self.rule = rule
        self.base_date_passed_in = False
        if base_date:
            self.base_date = base_date
            self.base_date_passed_in = True
        elif PricingContext.current.is_entered:
            pricing_date = PricingContext.current.pricing_date
            self.base_date = pricing_date
        else:
            self.base_date = date.today()
        self.base_date = self.base_date.date() if isinstance(self.base_date, (datetime, Timestamp)) else self.base_date

    def apply_rule(self,
                   currencies: List[Union[Currency, str]] = None,
                   exchanges: List[Union[ExchangeCode, str]] = None,
                   holiday_calendar: List[date] = None,
                   week_mask: str = '1111100',
                   **kwargs) -> date:
        """
        Applies business date logic on the rule using the given holiday calendars for rules that use business
        day logic. week_mask is based off
        https://numpy.org/doc/stable/reference/generated/numpy.busdaycalendar.weekmask.html.

        :param holiday_calendar: Optional list of date to use for holiday calendar. This parameter takes precedence over
        currencies/exchanges.
        :param currencies: List of currency holiday calendars to use. (GS Internal only)
        :param exchanges: List of exchange holiday calendars to use.
        :param week_mask: String of seven-element boolean mask indicating valid days. Default weekend is Sat and Sun.
        :return: dt.date
        """

        result = copy(self.base_date)

        for rule in self._get_rules():
            result = self.__handle_rule(rule, result, week_mask,
                                        currencies=currencies, exchanges=exchanges, holiday_calendar=holiday_calendar,
                                        **kwargs)

        return result

    def _get_rules(self) -> List[str]:
        rule_list = []
        current_rule = ''
        if not len(self.rule):
            raise MqValueError('Invalid Rule ""')
        current_alpha = self.rule[0].isalpha()
        for c in self.rule:
            is_alpha = c.isalpha()
            if current_alpha and not is_alpha:
                if current_rule.startswith('+'):
                    rule_list.append(current_rule[1:])
                else:
                    rule_list.append(current_rule)
                current_rule = ''
                current_alpha = False
            if is_alpha:
                current_alpha = True
            current_rule += c
        if current_rule.startswith('+'):
            rule_list.append(current_rule[1:])
        else:
            rule_list.append(current_rule)
        return rule_list

    def __handle_rule(self,
                      rule: str,
                      result: date,
                      week_mask: str,
                      currencies: List[Union[Currency, str]] = None,
                      exchanges: List[Union[ExchangeCode, str]] = None,
                      holiday_calendar: List[date] = None,
                      **kwargs) -> date:
        if rule.startswith('-'):
            index = 1
            while index != len(rule) and rule[index].isdigit():
                index += 1
            number = int(rule[1:index]) * -1 if index < len(rule) else 0
            rule_str = rule[index]
        else:
            index = 0
            if not rule[0].isdigit():
                rule_str = rule
                number = 0
            else:
                while index != len(rule) and rule[index].isdigit():
                    index += 1
                if index < len(rule):
                    number = int(rule[0:index])
                    rule_str = rule[index]
                else:
                    rule_str = rule
                    number = 0

        if not rule_str:
            raise MqValueError(f'Invalid rule "{rule}"')

        try:
            rule_class = getattr(rules, f'{rule_str}Rule')
            return rule_class(result,
                              results=result,
                              number=number,
                              week_mask=week_mask,
                              currencies=currencies,
                              exchanges=exchanges,
                              holiday_calendar=holiday_calendar,
                              usd_calendar=kwargs.get('usd_calendar')).handle()
        except AttributeError:
            raise NotImplementedError(f'Rule {rule} not implemented')

    def as_dict(self):
        rdate_dict = {'rule': self.rule}
        if self.base_date_passed_in:
            rdate_dict['baseDate'] = str(self.base_date)
        return rdate_dict


class RelativeDateSchedule:
    """
        RelativeDatesSchedules are objects which wrap a RelativeDate to provide a schedule between two dates
        Some rules require a business day calendar.

        :param rule: Rule to use
        :param base_date: Base date to use (Optional).
        :param end_date: No dates past this date will be returned (Optional).
        :return: new RelativeDateSchedule object

        **Usage**

        Create a RelativeDateSchedule object and then call `apply_rule` to get a date schedule back.

        **Examples**

        RelativeDateSchedule to return a schedule from today to 1w in the future

        >>> my_date: date = RelativeDateSchedule('1w', datetime.date.today(), ).apply_rule()

        """

    def __init__(self,
                 rule: str,
                 base_date: Optional[date] = None,
                 end_date: Optional[date] = None):
        self.rule = rule
        self.base_date_passed_in = False
        if base_date:
            self.base_date = base_date
            self.base_date_passed_in = True
        elif PricingContext.current.is_entered:
            pricing_date = PricingContext.current.pricing_date
            self.base_date = pricing_date.date() if isinstance(pricing_date, (datetime, Timestamp)) else pricing_date
        else:
            self.base_date = date.today()
        self.end_date = end_date

    def apply_rule(self,
                   currencies: List[Union[Currency, str]] = None,
                   exchanges: List[Union[ExchangeCode, str]] = None,
                   holiday_calendar: List[date] = None,
                   week_mask: str = '1111100',
                   **kwargs) -> List[date]:
        """
        Applies business date logic on the rule using the given holiday calendars for rules that use business
        day logic. week_mask is based off
        https://numpy.org/doc/stable/reference/generated/numpy.busdaycalendar.weekmask.html.

        :param holiday_calendar: Optional list of date to use for holiday calendar. This parameter takes precedence over
        currencies/exchanges.
        :param currencies: List of currency holiday calendars to use. (GS Internal only)
        :param exchanges: List of exchange holiday calendars to use.
        :param week_mask: String of seven-element boolean mask indicating valid days. Default weekend is Sat and Sun.
        :return: dt.date
        """

        i = 1
        schedule = [self.base_date]
        while True:
            rule = f'{int(self.rule[:-1]) * i}{self.rule[-1]}'
            result = RelativeDate(rule, self.base_date).apply_rule(currencies, exchanges, holiday_calendar, week_mask,
                                                                   **kwargs)
            if self.end_date is None or result > self.end_date:
                break
            i += 1
            schedule.append(result)

        return schedule

    def as_dict(self):
        rdate_dict = {'rule': self.rule}
        if self.base_date_passed_in:
            rdate_dict['baseDate'] = str(self.base_date)
        rdate_dict['endDate'] = str(self.end_date)
        return rdate_dict
