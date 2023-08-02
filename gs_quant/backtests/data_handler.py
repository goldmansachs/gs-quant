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
from typing import Union
from gs_quant.backtests.data_sources import DataManager
from pytz import timezone, utc


class Clock(object):
    def __init__(self):
        self._time = None
        self.reset()

    def update(self, time: dt.datetime):

        compare_time = self._time.replace(tzinfo=None) \
            if time.tzinfo is None or time.tzinfo.utcoffset(time) is None else self._time

        if time < compare_time:
            raise RuntimeError(f'current time is {compare_time}, cannot run backwards to {time}')
        self._time = time

    def reset(self):
        self._time = dt.datetime(1900, 1, 1).replace(tzinfo=utc)

    def time_check(self, state: Union[dt.date, dt.datetime]):
        if isinstance(state, dt.datetime):
            if state.tzinfo is None or state.tzinfo.utcoffset(state) is None:  # timezone naive
                lookahead = state > self._time.replace(tzinfo=None)
            else:
                lookahead = state > self._time
        else:
            lookahead = state > self._time.date()

        if lookahead:
            raise RuntimeError(f'accessing data at {state} not allowed, current time is {self._time}')


class DataHandler(object):
    def __init__(self, data_mgr: DataManager, tz: timezone):
        self._data_mgr = data_mgr
        self._clock = Clock()
        self._tz = tz

    def reset_clock(self):
        self._clock.reset()

    def update(self, state: dt.datetime):
        self._clock.update(state)

    def _utc_time(self, state: Union[dt.date, dt.datetime]):
        # only switch to utc time if the datetime you've been sent is timezone naive
        if isinstance(state, dt.datetime) and (state.tzinfo is None or state.tzinfo.utcoffset(state) is None):
            return self._tz.localize(state).astimezone(utc).replace(tzinfo=None)
        else:
            return state

    def get_data(self, state: Union[dt.date, dt.datetime], *key):
        self._clock.time_check(state)
        return self._data_mgr.get_data(self._utc_time(state), *key)

    def get_data_range(self, start: Union[dt.date, dt.datetime], end: Union[dt.date, dt.datetime], *key):
        self._clock.time_check(end)
        if type(start) is not type(end):
            raise RuntimeError('expect same type for start and end when asking for data range')
        return self._data_mgr.get_data_range(self._utc_time(start), self._utc_time(end), *key)
