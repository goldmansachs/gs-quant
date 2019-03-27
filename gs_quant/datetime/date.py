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


def is_business_day(dates: DateOrDates, calendars: Union[str, Tuple]=(), week_mask: Optional[str]=None) -> Union[bool, Tuple[bool]]:
    """
    Determine whether each date in dates is a business day

    :param dates: The input date or dates
    :param calendars: Calendars to use for holidays
    :param week_mask: Which days are considered weekends (defaults to Saturday and Sunday)
    :return: True/False if dates is a single date. A tuple indicating True/False for each date if dates is an iterable

    **Examples**

    >>> import datetime as dt
    >>> is_bus_date = is_business_day(dt.date.today())
    """
    calendar = GsCalendar.get(calendars)
    res = np.is_busday(dates, busdaycal=calendar.business_day_calendar(week_mask))
    return tuple(res) if isinstance(res, np.ndarray) else res


def business_day_offset(dates: DateOrDates, offsets: Union[int, Iterable[int]], roll: str= 'raise', calendars: Union[str, Tuple]=(), week_mask: Optional[str]=None) -> DateOrDates:
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


def business_day_count(begin_dates: DateOrDates, end_dates: DateOrDates, calendars: Union[str, Tuple]=(), week_mask: Optional[str]=None) -> Union[int, Tuple[int]]:
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


