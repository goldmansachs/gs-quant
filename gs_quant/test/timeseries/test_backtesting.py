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

import datetime

import pandas as pd
import pytest
from pandas.testing import assert_series_equal
from testfixtures import Replacer
from testfixtures.mock import Mock

from gs_quant.timeseries import EdrDataReference
from gs_quant.timeseries.backtesting import Basket, basket_series, MqValueError, MqTypeError, RebalFreq, date, \
    DataContext, np


def test_basket_series():
    dates = [
        datetime.datetime(2019, 1, 1),
        datetime.datetime(2019, 1, 2),
        datetime.datetime(2019, 1, 3),
        datetime.datetime(2019, 1, 4),
        datetime.datetime(2019, 1, 5),
        datetime.datetime(2019, 1, 6),
    ]

    x = pd.Series([100.0, 101, 103.02, 100.9596, 100.9596, 102.978792], index=dates)
    y = pd.Series([100.0, 100, 100, 100, 100, 100], index=dates)

    assert_series_equal(x, basket_series([x], [1]))
    assert_series_equal(x, basket_series([x, x], [0.5, 0.5]))
    assert_series_equal(x, basket_series([x, x, x], [1 / 3, 1 / 3, 1 / 3]))
    assert_series_equal(x, basket_series([x, y], [1, 0]))
    assert_series_equal(y, basket_series([x, y], [0, 1]))
    with pytest.raises(MqValueError):
        basket_series([x, y], [1])
    with pytest.raises(MqTypeError):
        basket_series([1, 2, 3], [1])

    dates = [
        datetime.datetime(2019, 1, 1),
        datetime.datetime(2019, 1, 2),
        datetime.datetime(2019, 1, 3),
        datetime.datetime(2019, 1, 4),
        datetime.datetime(2019, 1, 5),
        datetime.datetime(2019, 1, 6),
        datetime.datetime(2019, 2, 1),
        datetime.datetime(2019, 2, 2),
        datetime.datetime(2019, 2, 3),
        datetime.datetime(2019, 2, 4),
        datetime.datetime(2019, 2, 5),
        datetime.datetime(2019, 2, 6),
    ]
    mreb = pd.Series(
        [100.0, 101, 103.02, 100.9596, 100.9596, 102.978792,
         100.0, 101, 103.02, 100.9596, 100.9596, 102.978792],
        index=dates)
    assert_series_equal(mreb, basket_series([mreb], [1], rebal_freq=RebalFreq.MONTHLY))


def _mock_spot_data():
    dates = pd.date_range(start='2021-01-01', periods=6)
    x = pd.DataFrame({'spot': [100.0, 101, 103.02, 100.9596, 100.9596, 102.978792]}, index=dates)
    x['assetId'] = 'MA4B66MW5E27U9VBB94'
    y = pd.DataFrame({'spot': [100.0, 100, 100, 100, 100, 100]}, index=dates)
    y['assetId'] = 'MA4B66MW5E27UAL9SUX'
    return x.append(y)


def _mock_spot_data_feb():
    dates_feb = pd.date_range(start='2021-02-01', periods=6)
    x = pd.DataFrame({'spot': [100.0, 101.5, 106.02, 100.1, 105.3, 102.9]}, index=dates_feb)
    x['assetId'] = 'MA4B66MW5E27U9VBB94'
    y = pd.DataFrame({'spot': [100.0, 101.5, 100.02, 98.1, 95.3, 93.9]}, index=dates_feb)
    y['assetId'] = 'MA4B66MW5E27UAL9SUX'
    return x.append(y)


def test_basket_price():
    with pytest.raises(MqValueError):
        Basket(['AAPL UW'], [0.1, 0.9], RebalFreq.MONTHLY)

    dates = pd.DatetimeIndex([date(2021, 1, 1), date(2021, 1, 2), date(2021, 1, 3), date(2021, 1, 4), date(2021, 1, 5),
                              date(2021, 1, 6)])
    dates_feb = pd.DatetimeIndex([date(2021, 2, 1), date(2021, 2, 2), date(2021, 2, 3), date(2021, 2, 4),
                                  date(2021, 2, 5), date(2021, 2, 6)])

    replace = Replacer()

    mock_data = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    mock_data.side_effect = [_mock_spot_data(), _mock_spot_data_feb()]

    mock_asset = replace('gs_quant.timeseries.backtesting.GsAssetApi.get_many_assets_data', Mock())
    mock_asset.return_value = [{'id': 'MA4B66MW5E27U9VBB94', 'bbid': 'AAPL UW'},
                               {'id': 'MA4B66MW5E27UAL9SUX', 'bbid': 'MSFT UW'}]

    a_basket = Basket(['AAPL UW', 'MSFT UW'], [0.1, 0.9], RebalFreq.MONTHLY)
    expected = pd.Series([100.0, 100.1, 100.302, 100.09596, 100.09596, 100.297879], index=dates)
    with DataContext('2021-01-01', '2021-01-06'):
        actual = a_basket.price()
    assert_series_equal(actual, expected)

    expected = pd.Series([100.00, 101.50, 100.62, 98.30, 96.30, 94.80], index=dates_feb)
    with DataContext('2021-02-01', '2021-02-06'):
        actual = a_basket.price()
    assert_series_equal(actual, expected)

    mock_asset = replace('gs_quant.timeseries.backtesting.GsAssetApi.get_many_assets_data', Mock())
    mock_asset.return_value = [{'id': 'MA4B66MW5E27U9VBB94', 'bbid': 'AAPL UW'}]
    with pytest.raises(MqValueError):
        Basket(['AAPL UW', 'ABC'], [0.1, 0.9], RebalFreq.MONTHLY).price()

    with pytest.raises(NotImplementedError):
        a_basket.price(real_time=True)

    replace.restore()


def test_basket_average_implied_vol():
    replace = Replacer()

    dates = pd.DatetimeIndex([date(2021, 1, 1), date(2021, 1, 2), date(2021, 1, 3), date(2021, 1, 4), date(2021, 1, 5),
                              date(2021, 1, 6)])

    x = pd.DataFrame({'impliedVolatility': [30.0, 30.2, 29.8, 30.6, 30.1, 30.0]}, index=dates)
    x['assetId'] = 'MA4B66MW5E27U9VBB94'
    y = pd.DataFrame({'impliedVolatility': [20.0, 20.2, 20.3, 20.6, 21.1, 20.0]}, index=dates)
    y['assetId'] = 'MA4B66MW5E27UAL9SUX'
    implied_vol = x.append(y)
    implied_vol.index.name = 'date'

    mock_data = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    mock_data.side_effect = [implied_vol, _mock_spot_data()]

    mock_asset = replace('gs_quant.timeseries.backtesting.GsAssetApi.get_many_assets_data', Mock())
    mock_asset.return_value = [{'id': 'MA4B66MW5E27U9VBB94', 'bbid': 'AAPL UW'},
                               {'id': 'MA4B66MW5E27UAL9SUX', 'bbid': 'MSFT UW'}]

    a_basket = Basket(['AAPL UW', 'MSFT UW'], [0.1, 0.9], RebalFreq.DAILY)
    expected = pd.Series([21.0, 21.2, 21.25, 21.6, 22.0, 21.0], index=dates)
    actual = a_basket.average_implied_volatility('6m', EdrDataReference.DELTA_CALL, 50)
    assert_series_equal(actual, expected)

    with pytest.raises(NotImplementedError):
        a_basket.average_implied_volatility('6m', EdrDataReference.DELTA_CALL, 50, real_time=True)

    replace.restore()


def test_basket_average_realized_vol():
    replace = Replacer()

    dates = pd.DatetimeIndex([date(2021, 1, 1), date(2021, 1, 2), date(2021, 1, 3), date(2021, 1, 4), date(2021, 1, 5),
                              date(2021, 1, 6)])
    dates_feb = pd.DatetimeIndex([date(2021, 2, 1), date(2021, 2, 2), date(2021, 2, 3), date(2021, 2, 4),
                                 date(2021, 2, 5), date(2021, 2, 6)])

    mock_data = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    mock_data.side_effect = [_mock_spot_data(), _mock_spot_data_feb()]

    mock_asset = replace('gs_quant.timeseries.backtesting.GsAssetApi.get_many_assets_data', Mock())
    mock_asset.return_value = [{'id': 'MA4B66MW5E27U9VBB94', 'bbid': 'AAPL UW'},
                               {'id': 'MA4B66MW5E27UAL9SUX', 'bbid': 'MSFT UW'}]

    a_basket = Basket(['AAPL UW', 'MSFT UW'], [0.1, 0.9], RebalFreq.DAILY)

    expected = pd.Series([np.nan, np.nan, 1.1225, 4.49, 2.245, 2.245], index=dates)
    with DataContext('2021-01-01', '2021-01-06'):
        actual = a_basket.average_realized_volatility('2d')
    assert_series_equal(actual, expected)

    expected = pd.Series([np.nan, np.nan, np.nan, 3.304542, 3.174902, 3.174902], index=dates)
    with DataContext('2021-01-01', '2021-01-06'):
        actual = a_basket.average_realized_volatility('3d')
    assert_series_equal(actual, expected)
    mock_data.assert_called_once()

    expected = pd.Series([np.nan, np.nan, np.nan, 34.698082, 19.719302, 18.860533], index=dates_feb)
    with DataContext('2021-02-01', '2021-02-06'):
        actual = a_basket.average_realized_volatility('3d')
    assert_series_equal(actual, expected)

    with pytest.raises(NotImplementedError):
        a_basket.average_realized_volatility('2d', real_time=True)

    replace.restore()


def _mock_vol_simple():
    return pd.Series([1 for i in range(5)], index=pd.date_range('2021-09-01', '2021-09-05'))


def _mock_data_simple():
    a = pd.Series([1 for i in range(5)], index=pd.date_range('2021-09-01', '2021-09-05'))
    x = pd.DataFrame({'spot': a.tolist()}, index=a.index)
    x['assetId'] = 'XLC_MOCK_MQID'
    y = pd.DataFrame({'spot': a.tolist()}, index=a.index)
    y['assetId'] = 'XLB_MOCK_MQID'
    z = pd.DataFrame({'spot': (a ** 3).tolist()}, index=a.index)
    z['assetId'] = 'SPX_MOCK_MQID'
    return x.append(y).append(z)


def _mock_spot_data_identical():
    dates = pd.date_range(start='2021-01-01', periods=6)
    x = pd.DataFrame({'spot': [100.0, 101, 103.02, 100.9596, 100.9596, 102.978792]}, index=dates)
    x['assetId'] = 'MA4B66MW5E27U9VBB94'
    y = pd.DataFrame({'spot': [100.0, 101, 103.02, 100.9596, 100.9596, 102.978792]}, index=dates)
    y['assetId'] = 'MA4B66MW5E27UAL9SUX'
    return x.append(y)


def _mock_spot_data_corr():
    dates = pd.date_range(start='2021-01-01', periods=6)
    x = pd.DataFrame({'spot': [78, 9, 1003, 17, -12, 5], 'assetId': 'MA4B66MW5E27U9VBB94'}, index=dates)
    y = pd.DataFrame({'spot': [-33, 33, 15, 21, -3, 2], 'assetId': 'MA4B66MW5E27UAL9SUX'}, index=dates)
    z = pd.DataFrame({'spot': [86, 86, 56, 86, 86, 9], 'assetId': 'MA4B66MW5E27UANZH2M'}, index=dates)
    return x.append(y).append(z)


def test_basket_average_realized_vol_wts():
    _mock_vol_simple()

    replace = Replacer()

    mock_data = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    mock_data.side_effect = [_mock_data_simple()]

    mock_asset = replace('gs_quant.timeseries.backtesting.GsAssetApi.get_many_assets_data', Mock())
    mock_asset.return_value = [{'id': 'XLB_MOCK_MQID', 'bbid': 'XLP UP'},
                               {'id': 'XLC_MOCK_MQID', 'bbid': 'XLC UP'}, {'id': 'SPX_MOCK_MQID', 'bbid': 'SPX'}]

    mock_vol = replace('gs_quant.timeseries.backtesting.volatility', Mock())
    mock_vol.side_effect = [_mock_vol_simple(), _mock_vol_simple() * 2, _mock_vol_simple() * 3, _mock_vol_simple() * 4]

    a_basket = Basket(['XLC UP', 'XLP UP', 'SPX'], [0.2, 0.3, 0.5], RebalFreq.DAILY)

    av_realized_vol = a_basket.average_realized_volatility('2d')
    np.testing.assert_approx_equal(av_realized_vol.iloc[0], 1.7)

    replace.restore()


def test_basket_average_realized_corr():
    replace = Replacer()

    dates = pd.DatetimeIndex([date(2021, 1, 1), date(2021, 1, 2), date(2021, 1, 3), date(2021, 1, 4), date(2021, 1, 5),
                              date(2021, 1, 6)])

    mock_data = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    mock_data.side_effect = [_mock_spot_data_identical(), _mock_spot_data_corr(),
                             _mock_spot_data_identical()]

    mock_asset = replace('gs_quant.timeseries.backtesting.GsAssetApi.get_many_assets_data', Mock())
    mock_asset.return_value = [
        {'id': 'MA4B66MW5E27U9VBB94', 'bbid': 'AAPL UW'},
        {'id': 'MA4B66MW5E27UAL9SUX', 'bbid': 'MSFT UW'}]

    a_basket = Basket(['AAPL UW', 'MSFT UW'], [0.1, 0.9], RebalFreq.DAILY)

    # Equal series have correlation of 1
    with DataContext('2021-01-01', '2021-01-06'):
        expected = pd.Series([np.nan, np.nan, 1.0, 1.0, 1.0, 1.0], index=dates)
        result = a_basket.average_realized_correlation('2d')
        assert_series_equal(result, expected)

    mock_asset = replace('gs_quant.timeseries.backtesting.GsAssetApi.get_many_assets_data', Mock())
    mock_asset.return_value = [
        {'id': 'MA4B66MW5E27U9VBB94', 'bbid': 'AAPL UW'},
        {'id': 'MA4B66MW5E27UAL9SUX', 'bbid': 'MSFT UW'},
        {'id': 'MA4B66MW5E27UANZH2M', 'bbid': 'XLP UP'}]

    b_basket = Basket(['AAPL UW', 'MSFT UW', 'XLP UP'], [0.2, 0.3, 0.5], RebalFreq.DAILY)

    # Test with two different series
    with DataContext('2021-01-01', '2021-01-06'):
        result = b_basket.average_realized_correlation('5d')
        expected = pd.Series([np.nan, np.nan, np.nan, np.nan, np.nan, 0.26872959922887607], index=dates)
        assert_series_equal(result, expected)

    # Test correct error being thrown
    mock_asset = replace('gs_quant.timeseries.backtesting.GsAssetApi.get_many_assets_data', Mock())
    mock_asset.return_value = [
        {'id': 'MA4B66MW5E27U9VBB94', 'bbid': 'AAPL UW'},
        {'id': 'MA4B66MW5E27UAL9SUX', 'bbid': 'MSFT UW'},
        {'id': 'MA4B66MW5E27UANZH2M', 'bbid': 'XLP UP'}]

    with pytest.raises(NotImplementedError):
        with DataContext('2021-01-01', '2021-01-09'):
            result = b_basket.average_realized_correlation('5d', real_time=True)
    replace.restore()


if __name__ == '__main__':
    pytest.main(args=[__file__])
