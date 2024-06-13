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
import pandas as pd
from numpy import int64
from pandas._testing import assert_series_equal, assert_frame_equal

from gs_quant.api.gs.backtests_xasset.json_encoders.response_datatypes.risk_result_datatype_encoders import \
    encode_series_result, encode_dataframe_result, decode_series_result, decode_dataframe_result


def test_encode_series_result():
    d = {'a': 1, 'b': 2, 'c': 3}
    s = pd.Series(data=d, index=['a', 'b', 'c'], name='test')
    enc = encode_series_result(s)
    assert enc == {'index': ('a', 'b', 'c'), 'name': 'test', 'values': (1, 2, 3)}


def test_encode_dataframe_result():
    df = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), columns=['a', 'b', 'c'])
    enc = encode_dataframe_result(df)
    assert enc == {'index': (0, 1, 2), 'columns': ('a', 'b', 'c'), 'values': ((1, 2, 3), (4, 5, 6), (7, 8, 9))}


def test_decode_series_result():
    enc = {'index': ('2024-06-12', '2024-06-13', '2024-06-14'), 'name': 'test', 'values': (1, 2, 3)}
    s = decode_series_result(enc)
    assert_series_equal(s, pd.Series(data=[1, 2, 3],
                                     index=[dt.date(2024, 6, 12), dt.date(2024, 6, 13), dt.date(2024, 6, 14)],
                                     name='test'))


def test_decode_dataframe_result():
    enc = {'index': ('2024-06-12', '2024-06-13', '2024-06-14'), 'columns': ('a', 'b', 'c'),
           'values': ((1, 2, 3), (4, 5, 6), (7, 8, 9))}
    df = decode_dataframe_result(enc)
    assert_frame_equal(df, pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), columns=['a', 'b', 'c'],
                       index=[dt.date(2024, 6, 12), dt.date(2024, 6, 13), dt.date(2024, 6, 14)], dtype=int64))
