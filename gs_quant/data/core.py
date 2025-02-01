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
import re
from enum import Enum

from gs_quant.context_base import ContextBaseWithDefault
from gs_quant.errors import MqTypeError, MqValueError


def _now():
    return datetime.datetime.now(datetime.timezone.utc)


class DataFrequency(Enum):
    """Data Frequency enumeration

    Enumeration of different data frequencies for field subscription

    """

    #: Data subscription for series updating daily.
    DAILY = 'daily'

    #: Data subscription for real-time or intraday series.
    REAL_TIME = 'realTime'

    #: Data subscription for real-time or daily series.
    ANY = 'any'


class DataAggregationOperator:
    MIN = 'min'
    MAX = 'max'
    FIRST = 'first'
    LAST = 'last'


class IntervalFrequency(Enum):
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    YEARLY = 'yearly'


class DataContext(ContextBaseWithDefault):
    def __init__(self, start=None, end=None, interval=None):
        super().__init__()
        self.__start = start
        self.__end = end
        if interval is None:
            self.__interval = None
            return

        if not isinstance(interval, str):
            raise MqTypeError('Interval must be a str.')
        if not re.fullmatch('[1-9]\\d{0,2}[a-z]', interval):
            raise MqValueError('Interval must be a valid str e.g. 1m, 2h, 3d')
        self.__interval = interval

    @staticmethod
    def _get_date(o, default):
        if o is None:
            return default
        elif isinstance(o, datetime.datetime):
            # Note that datetime objects are also instances of date.
            return o.date()
        elif isinstance(o, datetime.date):
            return o
        elif isinstance(o, str):
            loc = o.find('T')
            ds = o[:loc] if loc != -1 else o
            return datetime.datetime.strptime(ds, '%Y-%m-%d').date()
        else:
            raise ValueError(f'{o} is not a valid date.')

    @staticmethod
    def _get_datetime(o, default):
        if o is None:
            return default
        elif isinstance(o, datetime.datetime):
            return o
        elif isinstance(o, datetime.date):
            return datetime.datetime.combine(o, datetime.time(tzinfo=datetime.timezone.utc))
        elif isinstance(o, str):
            tmp = datetime.datetime.strptime(o, '%Y-%m-%dT%H:%M:%SZ')
            return tmp.replace(tzinfo=datetime.timezone.utc)
        else:
            raise ValueError(f'{o} is not a valid date.')

    @property
    def start_date(self):
        return self._get_date(self.__start, datetime.date.today() - datetime.timedelta(days=30))

    @property
    def end_date(self):
        return self._get_date(self.__end, datetime.date.today())

    @property
    def start_time(self):
        return self._get_datetime(self.__start, _now() - datetime.timedelta(days=1))

    @property
    def end_time(self):
        return self._get_datetime(self.__end, _now())

    @property
    def interval(self):
        return self.__interval


if __name__ == '__main__':
    with DataContext(datetime.date(2019, 1, 1), datetime.datetime(2019, 2, 1, tzinfo=datetime.timezone.utc)) as dc:
        print(f'{dc.start_date}, {dc.end_date}')
        print(f'{dc.start_time}, {dc.end_time}')
    with DataContext(None, '2019-01-01T00:00:00Z') as dc2:
        print(f'{dc2.start_date}, {dc2.end_date}')
        print(f'{dc2.start_time}, {dc2.end_time}')
