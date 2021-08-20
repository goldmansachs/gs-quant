"""
Copyright 2021 Goldman Sachs.
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
import json

import pytz
from gs_quant.json_encoder import JSONEncoder


def test_datetime_serialisation():
    dates = [
        dt.datetime(2021, 8, 10, 10, 39, 19),
        dt.datetime(2021, 8, 10, 10, 39, 19, 59876),
        dt.datetime(2021, 8, 10, 10, 39, 19, tzinfo=pytz.timezone('EST')),
        dt.datetime(2021, 8, 10, 10, 39, 19, tzinfo=pytz.timezone('UTC')),
    ]
    expected = [
        '"2021-08-10T10:39:19.000Z"',
        '"2021-08-10T10:39:19.059Z"',
        '"2021-08-10T10:39:19.000-05:00"',
        '"2021-08-10T10:39:19.000+00:00"',
    ]
    for d, e in zip(dates, expected):
        encoded = json.dumps(d, cls=JSONEncoder)
        assert encoded == e
