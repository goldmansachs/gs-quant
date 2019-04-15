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
from typing import Iterable, Optional, Tuple, Union
from gs_quant.datetime.gscalendar import GsCalendar

DateOrDates = Union[dt.date, Iterable[dt.date]]


def is_business_day(dates: DateOrDates, calendars: Union[str, Tuple[str, ...]]=(), week_mask: Optional[str]=None) -> Union[bool, Tuple[bool]]:
    """
    Determine whether each date in dates is a business day

    :param dates: The input date or dates
    :param calendars: Calendars to use for holidays
    :param week_mask: Which days are considered weekends (defaults to Saturday and Sunday)
    :return: True/False if dates is a single date. A tuple indicating True/False for each date if dates is an iterable

    **Examples**

    >>> import datetime as dt
    >>> is_bus_date = is_business_day(dt.date.today())
    >>>
    >>> is_bus_date = is_business_day(dt.date(2019, 7, 4), calendars=('NYSE',))
    """
    calendar = GsCalendar.get(calendars)
    res = np.is_busday(dates, busdaycal=calendar.business_day_calendar(week_mask))
    return tuple(res) if isinstance(res, np.ndarray) else res


def business_day_offset(dates: DateOrDates, offsets: Union[int, Iterable[int]], roll: str= 'raise', calendars: Union[str, Tuple[str, ...]]=(), week_mask: Optional[str]=None) -> DateOrDates:
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
    >>> prev_bus_date = business_day_offset(dt.date.today(), -1, roll='preceding')
    """
    calendar = GsCalendar.get(calendars)
    res = np.busday_offset(dates, offsets, roll, busdaycal=calendar.business_day_calendar(week_mask)).astype(dt.date)
    return tuple(res) if isinstance(res, np.ndarray) else res


def business_day_count(begin_dates: DateOrDates, end_dates: DateOrDates, calendars: Union[str, Tuple[str, ...]]=(), week_mask: Optional[str]=None) -> Union[int, Tuple[int]]:
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


def date_range(begin: Union[int, dt.date], end: Union[int, dt.date], calendars: Union[str, Tuple[str, ...]]=(), week_mask: Optional[str]=None) -> Iterable[dt.date]:
    """
    Construct a range of dates

    :param begin: Beginning date or int. An int will be interpreted as the number of business days before end (which must be a date)
    :param end: End date or int. An int will be interpreted as the number of business days after begin (which must be a date)
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
            return (business_day_offset(end, -i, roll='preceding', calendars=calendars, week_mask=week_mask) for i in range(begin))
        else:
            raise ValueError('end must be a date if begin is an int')
    else:
        raise ValueError('begin must be a date or int')

