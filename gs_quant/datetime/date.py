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
import numpy as np
import calendar as cal
from enum import Enum, IntEnum
from pytz import timezone
from typing import Iterable, Optional, Tuple, Union
from gs_quant.datetime.gscalendar import GsCalendar
from gs_quant.target.common import PricingLocation

DateOrDates = Union[dt.date, Iterable[dt.date]]


class PaymentFrequency(IntEnum):
    """Payment frequency enumeration

    Provides an enumeration of different payment frequencies used to to discount cashflows and accrue interest

    """
    DAILY = 252
    WEEKLY = 52
    SEMI_MONTHLY = 26
    MONTHLY = 12
    SEMI_QUARTERLY = 6
    QUARTERLY = 4
    TRI_ANNUALLY = 3
    SEMI_ANNUALLY = 2
    ANNUALLY = 1


class DayCountConvention(Enum):
    """Day Count Convention enumeration

    Provides an enumeration of different day count conventions for determining how interest accrues over payment periods
    for financial securities

    """

    # Actual/360: Number of days between dates divided by 360
    ACTUAL_360 = "ACTUAL_360"

    # Actual/364: Number of days between dates divided by 364
    ACTUAL_364 = "ACTUAL_364"

    # Actual/365_25: Number of days between dates divided by 365.25
    ACTUAL_365_25 = "ACTUAL_365_25"

    # Actual/365 FIXED: Number of days between dates divided by 365
    ACTUAL_365F = "ACTUAL_365F"

    # Actual/365 LEAP: Number of days between dates divided by 365 or 366 in leap years
    ACTUAL_365L = "ACTUAL_365L"

    # ONE_ONE: Always returns a day count fraction of 1
    ONE_ONE = "ONE_ONE"


def is_business_day(dates: DateOrDates, calendars: Union[str, Tuple[str, ...]] = (), week_mask: Optional[str] = None)\
        -> Union[bool, Tuple[bool, ...]]:
    """
    Determine whether each date in dates is a business day

    :param dates: The input date or dates
    :param calendars: Calendars to use for holidays
    :param week_mask: Which days are considered weekends (defaults to Saturday and Sunday)
    :return: True/False if dates is a single date. A tuple indicating True/False for each date if dates is an iterable

    **Examples**

    >>> import datetime as dt
    >>> is_business_day(dt.date.today())
    >>> is_business_day(dt.date(2019, 7, 4), calendars=('NYSE',))
    """
    calendar = GsCalendar.get(calendars)
    res = np.is_busday(dates, busdaycal=calendar.business_day_calendar(week_mask))
    return tuple(res) if isinstance(res, np.ndarray) else res


def business_day_offset(
        dates: DateOrDates, offsets: Union[int, Iterable[int]],
        roll: str = 'raise', calendars: Union[str, Tuple[str, ...]] = (),
        week_mask: Optional[str] = None) -> DateOrDates:
    """
    Apply offsets to the dates and move to the nearest business date

    :param dates: The input date or dates
    :param offsets: The number of days by which to adjust the dates
    :param roll: Which direction to roll, in order to get to the nearest business date
    :param calendars: Calendars to use for holidays
    :param week_mask: Which days are considered weekends (defaults to Saturday and Sunday)
    :return: A date (if dates is a single date) or tuple of dates, adjusted by the offsets

    **Examples**

    >>> import datetime as dt
    >>> prev_bus_date = business_day_offset(dt.date.today(), -1, roll='forward')
    """
    calendar = GsCalendar.get(calendars)
    res = np.busday_offset(dates, offsets, roll, busdaycal=calendar.business_day_calendar(week_mask)).astype(dt.date)
    return tuple(res) if isinstance(res, np.ndarray) else res


def prev_business_date(
        dates: DateOrDates = dt.date.today(),
        calendars: Union[str, Tuple[str, ...]] = (),
        week_mask: Optional[str] = None) -> DateOrDates:
    """
    Returns the previous business date for a given date or date series, defaulting to today.

    :param dates: The input date or dates, defaults to today
    :param calendars: Calendars to use for holidays
    :param week_mask: Which days are considered weekends (defaults to Saturday and Sunday)
    :return: A date (if dates is a single date) or tuple of dates, adjusted by the offset of one day.

    **Example**

    >>> import datetime as dt
    >>> prev_bus_date = prev_business_date()
    """
    return business_day_offset(dates, -1, roll='forward', calendars=calendars, week_mask=week_mask)


def business_day_count(begin_dates: DateOrDates, end_dates: DateOrDates, calendars: Union[str, Tuple[str, ...]] = (
), week_mask: Optional[str] = None) -> Union[int, Tuple[int, ...]]:
    """
    Determine the number of business days between begin_dates and end_dates

    :param begin_dates: A date or collection of beginning dates
    :param end_dates: A date or collection of end dates
    :param calendars: Calendars to use for holidays
    :param week_mask: Which days are considered weekends (defaults to Saturday and Sunday)
    :return: An int or tuple of ints, representing the number of business days between begin_dates and end_dates

    **Examples**

    >>> import datetime as dt
    >>> today = dt.date.today()
    >>> bus_days = business_day_count(today, today + dt.timedelta(days=7))
    """
    calendar = GsCalendar.get(calendars)
    res = np.busday_count(begin_dates, end_dates, busdaycal=calendar.business_day_calendar(week_mask))
    return tuple(res) if isinstance(res, np.ndarray) else res


def date_range(begin: Union[int, dt.date],
               end: Union[int, dt.date],
               calendars: Union[str, Tuple[str, ...]] = (),
               week_mask: Optional[str] = None) -> Iterable[dt.date]:
    """
    Construct a range of dates

    :param begin: Beginning date or int. An int will be interpreted as the number of business days before end
        (which must be a date)
    :param end: End date or int. An int will be interpreted as the number of business days after begin
        (which must be a date)
    :param calendars: Calendars to use for holidays
    :param week_mask: Which days are considered weekends (defaults to Saturday and Sunday)
    :return: A generator of dates

    >>> import datetime as dt
    >>> today = dt.date.today()
    >>> dates = tuple(date_range(5, today))
    >>>
    >>> for date in date_range(dt.date(2019, 1, 1), dt.date(2019, 2, 1)):
    >>>     print(date)
    """
    if isinstance(begin, dt.date):
        if isinstance(end, dt.date):
            def f():
                prev = begin
                if prev > end:
                    raise ValueError('begin must be <= end')

                while prev <= end:
                    yield prev
                    prev = business_day_offset(prev, 1, calendars=calendars, week_mask=week_mask)

            return (d for d in f())
        elif isinstance(end, int):
            return (business_day_offset(begin, i, calendars=calendars, week_mask=week_mask) for i in range(end))
        else:
            raise ValueError('end must be a date or int')
    elif isinstance(begin, int):
        if isinstance(end, dt.date):
            return (business_day_offset(end, -i, roll='preceding', calendars=calendars, week_mask=week_mask)
                    for i in range(begin))
        else:
            raise ValueError('end must be a date if begin is an int')
    else:
        raise ValueError('begin must be a date or int')


def today(location: Optional[PricingLocation] = None) -> dt.date:
    if not location:
        return dt.date.today()

    if location == PricingLocation.LDN:
        tz = 'Europe/London'
    elif location == PricingLocation.NYC:
        tz = 'America/New_York'
    elif location == PricingLocation.HKG:
        tz = 'Asia/Hong_Kong'
    elif location == PricingLocation.TKO:
        tz = 'Asia/Tokyo'
    else:
        raise ValueError(f'Unrecognized timezone {location}')

    return dt.datetime.now(timezone(tz)).date()


def has_feb_29(start: dt.date, end: dt.date):
    """
    Determine if date range has a leap day (29Feb)

    :param start: first date
    :param end: second date

    **Usage**

    Determine if a given date range contains a leap day (Feb 29). Used for various day count convention calculations
    which alter behaviour for leap years. Start date is exclusive and end date is inclusive

    **Examples**

    Determine if a given date range contains 29Feb

    >>> start = date(2020, 1, 1)
    >>> end = date(2020, 3, 15)
    >>> has_feb_29(start, end)
    """
    feb_29 = False
    for x in range(1, (end - start).days + 1):
        date = start + dt.timedelta(days=x)
        feb_29 = feb_29 | (date.month == 2 and date.day == 29)

    return feb_29


def day_count_fraction(
        start: dt.date,         # First payment date
        end: dt.date,           # Second payment date
        convention: DayCountConvention = DayCountConvention.ACTUAL_360,
        frequency: PaymentFrequency = PaymentFrequency.MONTHLY
):
    """
    Compute day count fraction between dates

    :param start: first date
    :param end: second date
    :param convention: day count convention
    :param frequency: payment frequency of instrument
    :return: day count fraction between dates per convention

    **Usage**

    Compute day count fraction between dates, based on the value of *convention*. For more information on the available
    day count conventions, see the
    `Day Count Conventions <https://developer.gs.com/docs/gsquant/guides/Dates/1-day-count-conventions>`_ guide.

    **Examples**

    Compute day count fraction between two dates using Actual/360 convention:

    >>> start = date(2015, 11, 12)
    >>> end = date(2017, 12, 15)
    >>> day_count_fraction(start, end, DayCountConvention.ACTUAL_360)

    """

    if convention == DayCountConvention.ACTUAL_360:
        return (end - start).days / 360
    elif convention == DayCountConvention.ACTUAL_364:
        return (end - start).days / 364
    elif convention == DayCountConvention.ACTUAL_365F:
        return (end - start).days / 365
    elif convention == DayCountConvention.ACTUAL_365L:
        if frequency == PaymentFrequency.ANNUALLY:
            days_in_year = 366 if has_feb_29(start, end) else 365
        else:
            days_in_year = 366 if cal.isleap(end.year) else 365
        return (end - start).days / days_in_year
    elif convention == DayCountConvention.ACTUAL_365_25:
        return (end - start).days / 365.25
    elif convention == DayCountConvention.ONE_ONE:
        return 1
    else:
        raise ValueError('Unknown day count convention: ' + convention.value)
