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
from unittest import mock

import numpy as np
import pytest
from numpy import int64, float64, object, datetime64

from gs_quant.data import Dataset
from gs_quant.data.utils import construct_dataframe_with_types

test_data = [
    {
        'date': dt.date(2019, 1, 2),
        'assetId': 'MA4B66MW5E27U8P32SB',
        'askPrice': 2529,
        'adjustedAskPrice': 2529,
        'bidPrice': 2442.55,
        'adjustedBidPrice': 2442.55,
        'tradePrice': 2510.03,
        'adjustedTradePrice': 2510.03,
        'openPrice': 2476.96,
        'adjustedOpenPrice': 2476.96,
        'highPrice': 2519.49,
        'lowPrice': 2467.47,
        'adjustedHighPrice': 2519.49,
        'adjustedLowPrice': 2467.47,
        'updateTime': dt.datetime.strptime('2019-01-03T00:53:00Z', '%Y-%m-%dT%H:%M:%SZ')
    }
]
test_types = {
    'date': 'date',
    'assetId': 'string',
    'askPrice': 'number',
    'adjustedAskPrice': 'number',
    'bidPrice': 'number',
    'adjustedBidPrice': 'number',
    'tradePrice': 'number',
    'adjustedTradePrice': 'number',
    'openPrice': 'number',
    'adjustedOpenPrice': 'number',
    'highPrice': 'number',
    'lowPrice': 'number',
    'adjustedHighPrice': 'number',
    'adjustedLowPrice': 'number',
    'updateTime': 'date-time'
}


@mock.patch("gs_quant.data.utils.get_types")
def test_construct_dataframe_with_types(get_types):
    get_types.return_value = test_types
    df = construct_dataframe_with_types(str(Dataset.TR.TREOD), test_data)
    assert np.issubdtype(df.index.dtype, datetime64)
    assert df['adjustedAskPrice'].dtype == int64
    assert df['adjustedBidPrice'].dtype == float64
    assert df['assetId'].dtype == object  # https://pbpython.com/pandas_dtypes.html python str == dtype object
    assert np.issubdtype(df['updateTime'].dtype, datetime64)


if __name__ == "__main__":
    pytest.main(args=["test_utils.py"])
