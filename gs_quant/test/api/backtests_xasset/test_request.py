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

import dataclasses
import datetime as dt
import json

import pandas as pd

from gs_quant.api.gs.backtests_xasset.request import (
    BasicBacktestRequest,
    DateConfig,
    GenericBacktestRequest,
    RiskRequest,
)
from gs_quant.json_convertors import decode_optional_date_or_time


def test_request_types():
    cls = (RiskRequest, BasicBacktestRequest, GenericBacktestRequest)
    for c in cls:
        assert dataclasses.is_dataclass(c)


def test_date_fields_encode_to_iso_strings():
    """These fields need an explicit encoder. Only dataclasses-json 0.6.5 and later derives one for
    Optional[Union[date, datetime]] from the globally registered date encoder, and a plain date is
    not serializable without it."""
    risk = RiskRequest(start_date=dt.date(2024, 1, 1), end_date=dt.date(2024, 2, 1))
    assert json.loads(risk.to_json()) == {'startDate': '2024-01-01', 'endDate': '2024-02-01'}

    intraday = RiskRequest(start_date=dt.datetime(2024, 1, 1, 14, 30))
    assert json.loads(intraday.to_json()) == {'startDate': '2024-01-01T14:30:00.000Z'}

    backtest = BasicBacktestRequest(dates=DateConfig(dt.date(2024, 1, 1), dt.date(2024, 2, 1)), trades=(), measures=())
    dates = json.loads(backtest.to_json())['dates']
    assert dates['startDate'] == '2024-01-01'
    assert dates['endDate'] == '2024-02-01'


def test_pandas_timestamps_encode_as_datetimes():
    """Without the encoder a Timestamp reaches the fallback json encoder, which sees a datetime and
    emits an epoch float that decode_optional_date_or_time then rejects."""
    request = RiskRequest(start_date=pd.Timestamp('2024-01-01 14:30'))
    assert json.loads(request.to_json()) == {'startDate': '2024-01-01T14:30:00.000Z'}


def test_date_fields_round_trip_preserving_type():
    assert decode_optional_date_or_time('2024-01-01') == dt.date(2024, 1, 1)
    assert decode_optional_date_or_time('2024-01-01T14:30:00.000Z').replace(tzinfo=None) == dt.datetime(
        2024, 1, 1, 14, 30
    )
