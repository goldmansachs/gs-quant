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
import pandas as pd
from pandas._testing import assert_series_equal

from gs_quant.api.gs.backtests_xasset.json_encoders.response_datatypes.risk_result_encoders import \
    map_result_to_datatype, decode_risk_result
from gs_quant.api.gs.backtests_xasset.response_datatypes.risk_result import RefType, RiskResultsByDate
from gs_quant.api.gs.backtests_xasset.response_datatypes.risk_result_datatypes import FloatWithData, StringWithData, \
    VectorWithData, MatrixWithData


def test_map_result_to_datatype():
    assert map_result_to_datatype(5) == FloatWithData
    assert map_result_to_datatype(5.0) == FloatWithData
    assert map_result_to_datatype("abc") == StringWithData
    assert map_result_to_datatype(pd.Series([])) == VectorWithData
    assert map_result_to_datatype(pd.DataFrame([])) == MatrixWithData


def test_decode_risk_result():
    encoded_series_result_1 = {'index': ('a', 'b', 'c'), 'name': 'test', 'values': (1, 2, 3)}
    encoded_series_result_2 = {'index': ('a', 'b', 'c'), 'name': 'test', 'values': (1, 2, 3)}
    risk_result = {'refs': {'legId': 'uuid_1', 'riskMeasure': 'uuid_2'},
                   'result': {'2024-06-11': {'unit': 'EUR', 'result': encoded_series_result_1, 'type': 'vector'},
                              '2024-06-12': {'unit': 'EUR', 'result': encoded_series_result_2, 'type': 'vector'}}}
    decoded = decode_risk_result(risk_result)
    assert isinstance(decoded, RiskResultsByDate)
    assert decoded.refs == {RefType.LEG_ID: 'uuid_1', RefType.RISK_MEASURE: 'uuid_2'}
    assert isinstance(decoded.result, dict)
    assert len(decoded.result) == 2
    assert isinstance(decoded.result[dt.date(2024, 6, 11)], VectorWithData)
    assert decoded.result[dt.date(2024, 6, 11)].unit == 'EUR'
    assert_series_equal(decoded.result[dt.date(2024, 6, 11)].result,
                        pd.Series(data=[1, 2, 3], index=['a', 'b', 'c'], name='test'))
