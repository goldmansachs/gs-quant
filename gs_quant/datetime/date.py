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

import datetime
from typing import Tuple


def adjust_to_business_date(date: datetime.date, prev: bool=False, calendar=None, weekend_days: Tuple[int]=(5, 6)) -> datetime.date:
    def is_business_date(d: date):
        return not (d.weekday() in weekend_days or (calendar and d in calendar))

    while not is_business_date(date):
        date += datetime.timedelta(days=-1 if prev else 1)

    return date
