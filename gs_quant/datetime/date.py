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
from typing import Tuple, Union
from gs_quant.datetime.gscalendar import GsCalendar


def is_business_day(dates, calendars: Union[str, Tuple]=(), week_mask: str=None):
    calendar = GsCalendar.get(calendars)
    return np.is_busday(dates, busdaycal=calendar.business_day_calendar(week_mask))


def business_day_offset(dates, offsets, roll: str= 'raise', calendars: Union[str, Tuple]=(), week_mask: str=None):
    calendar = GsCalendar.get(calendars)
    return np.busday_offset(dates, offsets, roll, busdaycal=calendar.business_day_calendar(week_mask)).astype(dt.date)


def business_day_count(begin_dates, end_dates, calendars: Union[str, Tuple]=(), week_mask: str=None):
    calendar = GsCalendar.get(calendars)
    return np.busday_count(begin_dates, end_dates, busdaycal=calendar.business_day_calendar(week_mask))

