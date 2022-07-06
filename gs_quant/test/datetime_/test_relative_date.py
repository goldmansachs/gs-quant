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

from datetime import date as dt
from unittest.mock import Mock

import pytest
from gs_quant.datetime.relative_date import RelativeDate
from testfixtures import Replacer

holiday_calendar = [dt(2021, 1, 18)]


def test_rule_parsing():
    assert RelativeDate('A')._get_rules() == ['A']
    assert RelativeDate('1d')._get_rules() == ['1d']
    assert RelativeDate('-1d')._get_rules() == ['-1d']
    assert RelativeDate('1y-1d')._get_rules() == ['1y', '-1d']
    assert RelativeDate('-1y-1d')._get_rules() == ['-1y', '-1d']
    assert RelativeDate('-1y+1d')._get_rules() == ['-1y', '1d']


# A -> first day of the year
def test_rule_a_():
    date: dt = RelativeDate('A', base_date=dt(2021, 1, 19)).apply_rule()
    assert date == dt(2021, 1, 1)


# b -> Business days
def test_rule_b():
    date: dt = RelativeDate('-1b', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2021, 1, 15)
    date: dt = RelativeDate('+1b', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2021, 1, 20)


# d -> gregorian calendar days
def test_rule_d():
    date: dt = RelativeDate('+1d', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2021, 1, 20)


# e -> end of month
def test_rule_e():
    date: dt = RelativeDate('e', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2021, 1, 31)


# M -> nth Monday
def test_rule_m_():
    date: dt = RelativeDate('1M', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2021, 1, 4)
    date: dt = RelativeDate('4M', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2021, 1, 25)


# T -> nth Tuesday
def test_rule_t_():
    date: dt = RelativeDate('1T', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2021, 1, 5)
    date: dt = RelativeDate('4T', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2021, 1, 26)


# W -> nth Wednesday
def test_rule_w_():
    date: dt = RelativeDate('1W', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2021, 1, 6)
    date: dt = RelativeDate('4W', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2021, 1, 27)


# R -> nth Thursday
def test_rule_r_():
    date: dt = RelativeDate('1R', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2021, 1, 7)
    date: dt = RelativeDate('4R', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2021, 1, 28)


# F -> nth Friday
def test_rule_f_():
    date: dt = RelativeDate('1F', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2021, 1, 1)
    date: dt = RelativeDate('4F', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2021, 1, 22)


# V -> nth Saturday
def test_rule_v_():
    date: dt = RelativeDate('1V', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2021, 1, 2)
    date: dt = RelativeDate('4V', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2021, 1, 23)


# Z -> nth Sunday
def test_rule_z_():
    date: dt = RelativeDate('1Z', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2021, 1, 3)
    date: dt = RelativeDate('4Z', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2021, 1, 24)


# g -> nth week
def test_rule_g():
    date: dt = RelativeDate('1g', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2021, 1, 26)
    date: dt = RelativeDate('3g', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2021, 2, 9)
    date: dt = RelativeDate('-1g', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2021, 1, 12)


# N -> nth Monday relative to given date
def test_rule_n_():
    date: dt = RelativeDate('1N', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2021, 1, 25)


# U -> nth Tuesday relative to given date
def test_rule_u_():
    date: dt = RelativeDate('1U', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2021, 1, 19)


# X -> nth Wednesday relative to given date
def test_rule_x_():
    date: dt = RelativeDate('1X', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2021, 1, 20)


# S -> nth Thursday relative to given date
def test_rule_s_():
    date: dt = RelativeDate('1S', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2021, 1, 21)


# G -> nth Friday relative to given date
def test_rule_g_():
    date: dt = RelativeDate('1G', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2021, 1, 22)


# I -> nth Saturday relative to given date
def test_rule_i_():
    date: dt = RelativeDate('1I', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2021, 1, 23)


# P -> nth Sunday relative to given date
def test_rule_p_():
    date: dt = RelativeDate('1P', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2021, 1, 24)


# w -> weeks offset
def test_rule_w():
    date: dt = RelativeDate('1w', base_date=dt(2022, 3, 30)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2022, 4, 6)


# k -> Relative years with no implicit USD calendar
def test_rule_k():
    date: dt = RelativeDate('1k', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2022, 1, 19)
    date: dt = RelativeDate('-1k', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2020, 1, 20)


# r -> end of year
def test_rule_r():
    date: dt = RelativeDate('r', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2021, 12, 31)


# u -> add business days without implicit USD holidays
def test_rule_u():
    date: dt = RelativeDate('1u', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2021, 1, 20)
    date: dt = RelativeDate('2u', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2021, 1, 21)
    date: dt = RelativeDate('-2u', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2021, 1, 14)


# v -> last business day of the month, gets last business day of month (number is months ahead)
def test_rule_v():
    date: dt = RelativeDate('2v', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2021, 3, 31)


# x -> gets last business day of month (ignores number)
def test_rule_x():
    date: dt = RelativeDate('x', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2021, 1, 29)


# y -> Relative years with the result moved to the next week day if the day falls on a weekend specified by the weekmask
def test_rule_y():
    date: dt = RelativeDate('2y', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2023, 1, 19)
    date: dt = RelativeDate('-2y', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2019, 1, 21)


# Returns four business days after the first business day on or after the 15th calendar day of the month
def test_chaining():
    date: dt = RelativeDate('J+14d+0u+4u', base_date=dt(2021, 1, 19)).apply_rule(holiday_calendar=holiday_calendar)
    assert date == dt(2021, 1, 22)


def mock_holiday_data(*args, **kwargs):
    dq = args[1]
    ccies = dq.as_dict()['where'].get('currency', [])
    base_holidays = [{'date': '2021-12-27', 'currency': 'USD', 'description': "Xmas"}]
    if 'USD' in ccies:
        base_holidays.append({'date': '2022-04-11', 'currency': 'USD', 'description': "Birthday"})
    return base_holidays


test_types = {
    'date': 'date',
    'exchange': 'string',
    'currency': 'string',
    'description': 'string',
    'updateTime': 'date'}


# test holiday calendar logic
def test_currency_holiday_calendars(mocker):
    replace = Replacer()
    replace('gs_quant.api.gs.data.GsDataApi.query_data', Mock(side_effect=mock_holiday_data))
    mocker.patch("gs_quant.api.gs.data.GsDataApi.get_types", return_value=test_types)
    rdate = RelativeDate('-1b', base_date=dt(2022, 4, 12))
    assert dt(2022, 4, 11) == rdate.apply_rule(currencies=[])
    assert dt(2022, 4, 11) == rdate.apply_rule(currencies=['GBP'])
    assert dt(2022, 4, 8) == rdate.apply_rule(currencies=['USD'])
    assert dt(2022, 4, 11) == rdate.apply_rule()  # No longer using USD by default
    replace.restore()


if __name__ == "__main__":
    pytest.main(args=["test_relative_date.py"])
