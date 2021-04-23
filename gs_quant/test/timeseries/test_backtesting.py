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

import pytest
from pandas.testing import assert_series_equal
from gs_quant.timeseries import *
from testfixtures import Replacer
from testfixtures.mock import Mock


def test_basket():
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


def test_basket_constructor():
    with pytest.raises(MqValueError):
        Basket(['AAPL UW'], [0.1, 0.9], RebalFreq.MONTHLY)

    replace = Replacer()

    dates = [
        datetime.datetime(2021, 1, 1),
        datetime.datetime(2021, 1, 2),
        datetime.datetime(2021, 1, 3),
        datetime.datetime(2021, 1, 4),
        datetime.datetime(2021, 1, 5),
        datetime.datetime(2021, 1, 6),
    ]

    x = pd.DataFrame({'spot': [100.0, 101, 103.02, 100.9596, 100.9596, 102.978792]}, index=dates)
    x['assetId'] = 'MA4B66MW5E27U9VBB94'
    y = pd.DataFrame({'spot': [100.0, 100, 100, 100, 100, 100]}, index=dates)
    y['assetId'] = 'MA4B66MW5E27UAL9SUX'
    spot = x.append(y)
    mock_data = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    mock_data.return_value = spot

    mock_asset = replace('gs_quant.timeseries.backtesting.GsAssetApi.get_many_assets_data', Mock())
    mock_asset.return_value = [{'id': 'MA4B66MW5E27U9VBB94'}, {'id': 'MA4B66MW5E27UAL9SUX'}]

    a_basket = Basket(['AAPL UW', 'MSFT UW'], [0.1, 0.9], RebalFreq.MONTHLY)
    expected = pd.Series([100.0, 100.1, 100.302, 100.09596, 100.09596, 100.297879], index=dates)
    actual = a_basket.price()
    assert_series_equal(actual, expected)

    mock_asset = replace('gs_quant.timeseries.backtesting.GsAssetApi.get_many_assets_data', Mock())
    mock_asset.return_value = [{'id': 'MA4B66MW5E27U9VBB94'}]
    with pytest.raises(MqValueError):
        Basket(['AAPL UW', 'ABC'], [0.1, 0.9], RebalFreq.MONTHLY).price()

    with pytest.raises(NotImplementedError):
        a_basket.price(real_time=True)

    replace.restore()


if __name__ == '__main__':
    pytest.main(args=[__file__])
