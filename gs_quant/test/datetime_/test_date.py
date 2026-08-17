"""
Copyright 2020 Goldman Sachs.
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

from pytest import approx

from gs_quant.common import PricingLocation
from gs_quant.datetime import DayCountConvention, PaymentFrequency, day_count_fraction, has_feb_29, today
from gs_quant.datetime.date import humanize_time_delta


def test_has_feb_29():
    assert not has_feb_29(dt.date(2019, 1, 1), dt.date(2019, 12, 31))
    assert has_feb_29(dt.date(2020, 1, 1), dt.date(2020, 12, 31))
    assert has_feb_29(dt.date(2020, 2, 28), dt.date(2020, 3, 31))
    assert not has_feb_29(dt.date(2020, 2, 29), dt.date(2020, 3, 31))  # first date is exclusive
    assert not has_feb_29(dt.date(2020, 1, 1), dt.date(2020, 2, 28))
    assert has_feb_29(dt.date(2020, 1, 1), dt.date(2020, 2, 29))  # last date is inclusive
    assert has_feb_29(dt.date(2008, 1, 1), dt.date(2020, 12, 31))


def test_today_with_location():
    for location in PricingLocation:
        assert today(location) is not None

    assert today(None) == dt.date.today()


def test_day_count_fraction():
    # 2017 is not a leap year
    start = dt.date(2017, 1, 1)
    end = dt.date(2017, 12, 31)

    assert day_count_fraction(start, end, DayCountConvention.ONE_ONE) == approx(1)
    assert day_count_fraction(start, end, DayCountConvention.ACTUAL_360) == approx(1.011111111111)
    assert day_count_fraction(start, end, DayCountConvention.ACTUAL_365F) == approx(0.997260273973)
    assert day_count_fraction(start, end, DayCountConvention.ACTUAL_365L) == approx(0.997260273973)

    # 2016 is a leap year
    start = dt.date(2015, 11, 12)
    end = dt.date(2017, 12, 15)

    assert day_count_fraction(start, end, DayCountConvention.ONE_ONE) == approx(1)
    assert day_count_fraction(start, end, DayCountConvention.ACTUAL_360) == approx(2.122222222222)
    assert day_count_fraction(start, end, DayCountConvention.ACTUAL_365F) == approx(2.093150684932)

    # End date is not leap year, so should use 365
    assert day_count_fraction(start, end, DayCountConvention.ACTUAL_365L) == approx(2.093150684932)

    # Feb 29 is within range, so should use 366
    assert day_count_fraction(start, end, DayCountConvention.ACTUAL_365L, PaymentFrequency.ANNUALLY) == approx(
        2.087431693989
    )


def test_humanize_time_delta_past():
    assert humanize_time_delta(dt.timedelta(seconds=0)) == "a few seconds ago"
    assert humanize_time_delta(dt.timedelta(seconds=5)) == "a few seconds ago"
    assert humanize_time_delta(dt.timedelta(seconds=9)) == "a few seconds ago"
    assert humanize_time_delta(dt.timedelta(seconds=10)) == "10 seconds ago"
    assert humanize_time_delta(dt.timedelta(seconds=59)) == "59 seconds ago"
    assert humanize_time_delta(dt.timedelta(seconds=60)) == "a minute ago"
    assert humanize_time_delta(dt.timedelta(seconds=119)) == "a minute ago"
    assert humanize_time_delta(dt.timedelta(minutes=2)) == "2 minutes ago"
    assert humanize_time_delta(dt.timedelta(minutes=19)) == "19 minutes ago"
    assert humanize_time_delta(dt.timedelta(minutes=59, seconds=59)) == "59 minutes ago"
    assert humanize_time_delta(dt.timedelta(hours=1)) == "an hour ago"
    assert humanize_time_delta(dt.timedelta(hours=1, minutes=59)) == "an hour ago"
    assert humanize_time_delta(dt.timedelta(hours=2)) == "2 hours ago"
    assert humanize_time_delta(dt.timedelta(hours=23)) == "23 hours ago"
    assert humanize_time_delta(dt.timedelta(days=1)) == "a day ago"
    assert humanize_time_delta(dt.timedelta(days=1, hours=23)) == "a day ago"
    assert humanize_time_delta(dt.timedelta(days=2)) == "2 days ago"
    assert humanize_time_delta(dt.timedelta(days=29)) == "29 days ago"
    assert humanize_time_delta(dt.timedelta(days=30)) == "a month ago"
    assert humanize_time_delta(dt.timedelta(days=59)) == "a month ago"
    assert humanize_time_delta(dt.timedelta(days=60)) == "2 months ago"
    assert humanize_time_delta(dt.timedelta(days=364)) == "12 months ago"
    assert humanize_time_delta(dt.timedelta(days=365)) == "a year ago"
    assert humanize_time_delta(dt.timedelta(days=729)) == "a year ago"
    assert humanize_time_delta(dt.timedelta(days=730)) == "2 years ago"
    assert humanize_time_delta(dt.timedelta(days=365 * 10)) == "10 years ago"


def test_humanize_time_delta_future():
    assert humanize_time_delta(dt.timedelta(seconds=-5)) == "in a few seconds"
    assert humanize_time_delta(dt.timedelta(seconds=-30)) == "in 30 seconds"
    assert humanize_time_delta(dt.timedelta(minutes=-19)) == "in 19 minutes"
    assert humanize_time_delta(dt.timedelta(hours=-3)) == "in 3 hours"
    assert humanize_time_delta(dt.timedelta(days=-1)) == "in a day"
    assert humanize_time_delta(dt.timedelta(days=-5)) == "in 5 days"
    assert humanize_time_delta(dt.timedelta(days=-365)) == "in a year"
