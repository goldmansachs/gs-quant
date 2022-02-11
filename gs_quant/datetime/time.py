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
import logging

import numpy as np
from gs_quant.errors import *

_logger = logging.getLogger(__name__)

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

    def __init__(self, print_on_exit: bool = True, label: str = 'Execution', threshold: int = None):
        self.__print_on_exit = print_on_exit
        self.__label = label
        self.__threshold = threshold

    def __enter__(self):
        self.__start = dt.datetime.now()

    def __exit__(self, *args):
        self.__elapsed = dt.datetime.now() - self.__start

        if self.__print_on_exit:
            if self.__threshold is None or self.__elapsed.seconds > self.__threshold:
                _logger.warning(
                    f'{self.__label} took {self.__elapsed.seconds + self.__elapsed.microseconds / 1000000} seconds')


class Tracer:
    __stack_depth = 0
    __stack = []

    def __init__(self, label: str = 'Execution', print_on_exit: bool = False, threshold: int = None):
        self.__print_on_exit = print_on_exit
        self.__label = label
        self.__threshold = threshold

    def __enter__(self):
        self.__start = dt.datetime.now()
        self.__index = len(Tracer.__stack)
        Tracer.__stack.append([dt.datetime.now(), 0.0, self.__label, Tracer.__stack_depth])
        Tracer.__stack_depth += 1

    def __exit__(self, *args):
        self.__elapsed = dt.datetime.now() - self.__start
        elapsed_sec = self.__elapsed.seconds + self.__elapsed.microseconds / 1000000
        Tracer.__stack[self.__index][1] = elapsed_sec
        Tracer.__stack_depth -= 1
        if self.__print_on_exit:
            if self.__threshold is None or self.__elapsed.seconds > self.__threshold:
                _logger.warning(f'{self.__label} took {elapsed_sec} seconds')

    @staticmethod
    def reset():
        Tracer.__stack_depth = 0
        Tracer.__stack = []

    @staticmethod
    def print(reset=True):
        lines = []
        total = 0
        for span in Tracer.__stack:
            name = f'{"* " * span[3]}{span[2]}'
            lines.append(f'{name:<50}{span[1] * 1000:>8.1f} ms')
            if span[3] == 0:
                total += span[1] * 1000
        tracing_str = '\n'.join(lines)
        _logger.warning(f'Tracing Info:\n{tracing_str}\n{"-" * 61}\nTOTAL:{total:>52.1f} ms')
        if reset:
            Tracer.reset()


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
