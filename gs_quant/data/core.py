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
from gs_quant.context_base import ContextBaseWithDefault


def _now():
    return datetime.datetime.now(datetime.timezone.utc)


class DataContext(ContextBaseWithDefault):
    def __init__(self, start=None, end=None):
        super().__init__()
        self.__start = start
        self.__end = end

    @staticmethod
    def _get_date(o, default):
        if o is None:
            return default
        elif isinstance(o, datetime.datetime):
            # note that datetime objects are also instances of date
            return o.date()
        elif isinstance(o, datetime.date):
            return o
        elif isinstance(o, str):
            loc = o.find('T')
            ds = o[:loc] if loc != -1 else o
            return datetime.datetime.strptime(ds, '%Y-%m-%d').date()
        else:
            raise ValueError(f'{o} is not a valid date')

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
            raise ValueError(f'{o} is not a valid date')

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


if __name__ == '__main__':
    with DataContext(datetime.date(2019, 1, 1), datetime.datetime(2019, 2, 1, tzinfo=datetime.timezone.utc)) as dc:
        print(f'{dc.start_date}, {dc.end_date}')
        print(f'{dc.start_time}, {dc.end_time}')
    with DataContext(None, '2019-01-01T00:00:00Z') as dc2:
        print(f'{dc2.start_date}, {dc2.end_date}')
        print(f'{dc2.start_time}, {dc2.end_time}')
