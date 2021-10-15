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

import numpy as np
from numpy import int64, float64, object, datetime64
import pandas as pd
import pytest

from gs_quant.api.gs.data import GsDataApi
from gs_quant.data import Dataset
from gs_quant.session import GsSession, Environment
from gs_quant.target.data import Format

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
    },
    {
        'date': dt.date(2019, 1, 3),
        'assetId': 'MA4B66MW5E27U8P32SB',
        'askPrice': 2502.34,
        'adjustedAskPrice': 2502.34,
        'bidPrice': 2418.09,
        'adjustedBidPrice': 2418.09,
        'tradePrice': 2447.89,
        'adjustedTradePrice': 2447.89,
        'openPrice': 2491.92,
        'adjustedOpenPrice': 2491.92,
        'highPrice': 2493.14,
        'lowPrice': 2443.96,
        'adjustedHighPrice': 2493.14,
        'adjustedLowPrice': 2443.96,
        'updateTime': dt.datetime.strptime('2019-01-04T00:14:00Z', '%Y-%m-%dT%H:%M:%SZ')
    },
    {
        'date': dt.date(2019, 1, 4),
        'assetId': 'MA4B66MW5E27U8P32SB',
        'askPrice': 2566.52,
        'adjustedAskPrice': 2566.52,
        'bidPrice': 2487.8,
        'adjustedBidPrice': 2487.8,
        'tradePrice': 2531.94,
        'adjustedTradePrice': 2531.94,
        'openPrice': 2474.33,
        'adjustedOpenPrice': 2474.33,
        'highPrice': 2538.07,
        'lowPrice': 2474.33,
        'adjustedHighPrice': 2538.07,
        'adjustedLowPrice': 2474.33,
        'updateTime': dt.datetime.strptime('2019-01-08T00:31:00Z', '%Y-%m-%dT%H:%M:%SZ')
    },
    {
        'date': dt.date(2019, 1, 7),
        'assetId': 'MA4B66MW5E27U8P32SB',
        'askPrice': 2591.75,
        'adjustedAskPrice': 2591.75,
        'bidPrice': 2509.77,
        'adjustedBidPrice': 2509.77,
        'tradePrice': 2549.69,
        'adjustedTradePrice': 2549.69,
        'openPrice': 2535.61,
        'adjustedOpenPrice': 2535.61,
        'highPrice': 2566.16,
        'lowPrice': 2524.56,
        'adjustedHighPrice': 2566.16,
        'adjustedLowPrice': 2524.56,
        'updateTime': dt.datetime.strptime('2019-01-08T00:31:00Z', '%Y-%m-%dT%H:%M:%SZ')
    },
    {
        'date': dt.date(2019, 1, 8),
        'assetId': 'MA4B66MW5E27U8P32SB',
        'askPrice': 2610.52,
        'adjustedAskPrice': 2610.52,
        'bidPrice': 2531.15,
        'adjustedBidPrice': 2531.15,
        'tradePrice': 2574.41,
        'adjustedTradePrice': 2574.41,
        'openPrice': 2568.11,
        'adjustedOpenPrice': 2568.11,
        'highPrice': 2579.82,
        'lowPrice': 2547.56,
        'adjustedHighPrice': 2579.82,
        'adjustedLowPrice': 2547.56,
        'updateTime': dt.datetime.strptime('2019-01-09T00:50:00Z', '%Y-%m-%dT%H:%M:%SZ')
    },
    {
        'date': dt.date(2019, 1, 9),
        'assetId': 'MA4B66MW5E27U8P32SB',
        'askPrice': 2623.09,
        'adjustedAskPrice': 2623.09,
        'bidPrice': 2537.19,
        'adjustedBidPrice': 2537.19,
        'tradePrice': 2584.96,
        'adjustedTradePrice': 2584.96,
        'openPrice': 2580,
        'adjustedOpenPrice': 2580,
        'highPrice': 2595.32,
        'lowPrice': 2568.89,
        'adjustedHighPrice': 2595.32,
        'adjustedLowPrice': 2568.89,
        'updateTime': dt.datetime.strptime('2019-01-10T00:44:00Z', '%Y-%m-%dT%H:%M:%SZ')
    }
]

test_coverage_data = {'results': [{'gsid': 'gsid1'}]}


def test_query_data(mocker):
    mocker.patch("gs_quant.api.gs.data.GsDataApi.query_data", return_value=test_data)
    mocker.patch("gs_quant.api.gs.data.GsDataApi.get_types", return_value=test_types)
    dataset = Dataset(Dataset.TR.TREOD)
    data = dataset.get_data(dt.date(2019, 1, 2), dt.date(2019, 1, 9), assetId='MA4B66MW5E27U8P32SB')
    assert data.equals(GsDataApi.construct_dataframe_with_types(str(Dataset.TR.TREOD), test_data))


def test_query_data_types(mocker):
    mocker.patch("gs_quant.api.gs.data.GsDataApi.query_data", return_value=test_data)
    mocker.patch("gs_quant.api.gs.data.GsDataApi.get_types", return_value=test_types)
    dataset = Dataset(Dataset.TR.TREOD)
    data = dataset.get_data(dt.date(2019, 1, 2), dt.date(2019, 1, 9), assetId='MA4B66MW5E27U8P32SB')
    assert data.equals(GsDataApi.construct_dataframe_with_types(str(Dataset.TR.TREOD), test_data))


def test_last_data(mocker):
    mocker.patch("gs_quant.api.gs.data.GsDataApi.last_data", return_value=[test_data[-1]])
    mocker.patch("gs_quant.api.gs.data.GsDataApi.get_types", return_value=test_types)
    dataset = Dataset(Dataset.TR.TREOD)
    data = dataset.get_data_last(dt.date(2019, 1, 9), assetId='MA4B66MW5E27U8P32SB')
    assert data.equals(GsDataApi.construct_dataframe_with_types(str(Dataset.TR.TREOD), ([test_data[-1]])))


def test_get_data_series(mocker):
    field_value_maps = test_data
    mocker.patch("gs_quant.api.gs.data.GsDataApi.get_types", return_value=test_types)
    mocker.patch.object(GsDataApi, 'query_data', return_value=field_value_maps)
    mocker.patch.object(GsDataApi, 'symbol_dimensions', return_value=('assetId',))

    dataset = Dataset(Dataset.TR.TREOD)
    series = dataset.get_data_series('tradePrice', dt.date(2019, 1, 2), dt.date(2019, 1, 9),
                                     assetId='MA4B66MW5E27U8P32SB')

    df = pd.DataFrame(test_data)
    index = pd.to_datetime(df.loc[:, 'date'].values)
    expected = pd.Series(index=index, data=df.loc[:, 'tradePrice'].values)
    expected = expected.rename_axis('date')

    pd.testing.assert_series_equal(series, expected)


def test_get_coverage(mocker):
    mocker.patch("gs_quant.api.gs.data.GsDataApi.get_coverage", return_value=test_coverage_data)
    mocker.patch("gs_quant.api.gs.data.GsDataApi.get_types", return_value={'gsid': 'string'})
    data = Dataset(Dataset.TR.TREOD).get_coverage()
    results = test_coverage_data["results"]
    gsid = GsDataApi.construct_dataframe_with_types(str(Dataset.TR.TREOD), results).get('gsid').get(0)
    assert data["results"][0]["gsid"] == gsid


def test_construct_dataframe_with_types(mocker):
    mocker.patch("gs_quant.api.gs.data.GsDataApi.get_types", return_value=test_types)
    df = GsDataApi.construct_dataframe_with_types(str(Dataset.TR.TREOD), [test_data[0]])
    assert np.issubdtype(df.index.dtype, datetime64)
    assert df['adjustedAskPrice'].dtype == int64
    assert df['adjustedBidPrice'].dtype == float64
    assert df['assetId'].dtype == object  # https://pbpython.com/pandas_dtypes.html python str == dtype object
    assert np.issubdtype(df['updateTime'].dtype, datetime64)


def test_data_series_format(mocker):
    start = dt.date(2019, 1, 2)
    end = dt.datetime(2019, 1, 9)
    df = pd.DataFrame(test_data)
    index = pd.to_datetime(df.loc[:, 'date'].values)
    expected = pd.Series(index=index, data=df.loc[:, 'tradePrice'].values)
    expected = expected.rename_axis('date')

    # mock GsSession and data response
    mocker.patch.object(GsSession.__class__, 'default_value',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mock_response = {
        'requestId': 'qwerty',
        'data': test_data
    }
    mocker.patch.object(GsSession.current, '_post', side_effect=lambda *args, **kwargs: mock_response)
    mocker.patch.object(GsDataApi, 'symbol_dimensions', return_value=('assetId',))
    mocker.patch("gs_quant.api.gs.data.GsDataApi.get_types", return_value=test_types)

    actual = Dataset('TREOD').get_data_series(field='tradePrice', start=start, end=end, assetId='MA4B66MW5E27U8P32SB')
    pd.testing.assert_series_equal(actual, expected)
    assert len(GsSession.current._post.mock_calls) == 1
    name, args, kwargs = GsSession.current._post.mock_calls[0]
    assert kwargs['payload'].format == Format.MessagePack
    assert kwargs['request_headers'] == {'Accept': 'application/msgpack'}
    assert args[0] == '/data/TREOD/query'

    GsSession.current._post.reset_mock()
    actual = Dataset('TREOD').get_data_series(field='tradePrice', start=start, end=end, assetId='MA4B66MW5E27U8P32SB',
                                              format=Format.Json)
    pd.testing.assert_series_equal(actual, expected)
    assert len(GsSession.current._post.mock_calls) == 1
    name, args, kwargs = GsSession.current._post.mock_calls[0]
    assert kwargs['payload'].format == Format.Json
    assert 'request_headers' not in kwargs
    assert args[0] == '/data/TREOD/query'


if __name__ == "__main__":
    pytest.main(args=["test_dataset.py"])
