"""
Copyright 2018 Goldman Sachs.
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

from gs_quant.errors import *

DAYS_IN_YEAR = 365.25
DAYS_IN_WEEK = 7
HOURS_IN_DAY = 24
MINS_IN_HOUR = 60
SECS_IN_MIN = 60

SECS_IN_HOUR = SECS_IN_MIN * MINS_IN_HOUR
MINS_IN_DAY = MINS_IN_HOUR * HOURS_IN_DAY
SECS_IN_DAY = SECS_IN_MIN * MINS_IN_DAY

HOURS_IN_WEEK = HOURS_IN_DAY * DAYS_IN_WEEK
MINS_IN_WEEK = HOURS_IN_WEEK * MINS_IN_HOUR
SECS_IN_WEEK = MINS_IN_WEEK * SECS_IN_HOUR

SECS_IN_YEAR = SECS_IN_MIN * MINS_IN_HOUR * HOURS_IN_DAY * DAYS_IN_YEAR


class Timer:

    def __init__(self, print_on_exit=True, label='Execution'):
        self.print_on_exit = print_on_exit
        self.label = label

    def __enter__(self):
        self.start = dt.datetime.now()

    def __exit__(self, *args):
        self.elapsed = dt.datetime.now() - self.start

        if self.print_on_exit:
            print("{} took {} seconds".format(self.label, self.elapsed.seconds + self.elapsed.microseconds / 1000000))


def to_zulu_string(time: dt.datetime):
    return time.isoformat()[:-3] + 'Z'


def time_difference_as_string(
        time_delta: np.timedelta64,
        resolution: str = 'Second'
) -> str:
    times = [SECS_IN_YEAR, SECS_IN_WEEK, SECS_IN_DAY, SECS_IN_HOUR, SECS_IN_MIN, 1]
    time_strings = ['Year', 'Week', 'Day', 'Hour', 'Minute', 'Second']

    if resolution not in time_strings:
        raise MqValueError('incorrect resolution passed in "s"' % resolution)

    times_mapped = zip(times, time_strings)

    diff: int = abs(time_delta / np.timedelta64(1, 's'))
    result = ''

    for time, time_string in times_mapped:
        m = diff // time
        if m > 0:
            added = time_string
            if m != 1:
                added += 's'

            result += '%d %s ' % (m, added)
            diff -= m * time

        if time_string == resolution:
            break

    return result.strip()
