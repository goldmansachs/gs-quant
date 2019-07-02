import datetime as dt

import pytest
import numpy as np
from numpy import int64, float64, object, datetime64

from gs_quant.data.utils import construct_dataframe_with_types
from gs_quant.target.data import FieldValueMap

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


def test_construct_dataframe_with_types():
    field_value_map_list = [FieldValueMap(**d) for d in test_data]
    df = construct_dataframe_with_types(field_value_map_list)
    assert np.issubdtype(df.index.dtype, datetime64)
    assert df['adjustedAskPrice'].dtype == int64
    assert df['adjustedBidPrice'].dtype == float64
    assert df['assetId'].dtype == object  # https://pbpython.com/pandas_dtypes.html python str == dtype object
    assert np.issubdtype(df['updateTime'].dtype, datetime64)


if __name__ == "__main__":
    pytest.main(args=["test_utils.py"])
