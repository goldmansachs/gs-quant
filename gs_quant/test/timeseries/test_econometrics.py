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
from unittest.mock import Mock

import pytest
from gs_quant.timeseries import *
from gs_quant.timeseries.econometrics import _get_ratio
from pandas.testing import assert_series_equal
from testfixtures import Replacer


def test_returns():
    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 5),
        date(2019, 1, 6),
    ]

    x = pd.Series(dtype=float)
    assert_series_equal(x, returns(x))

    x = pd.Series([100.0, 101, 103.02, 100.9596, 100.9596, 102.978792], index=dates)

    result = returns(x)
    expected = pd.Series([np.nan, 0.01, 0.02, -0.02, 0.0, 0.02], index=dates)
    assert_series_equal(result, expected, obj="Simple returns default")

    result = returns(x, 1, Returns.SIMPLE)
    expected = pd.Series([np.nan, 0.01, 0.02, -0.02, 0.0, 0.02], index=dates)
    assert_series_equal(result, expected, obj="Simple returns")

    result = returns(x, 2, Returns.SIMPLE)
    expected = pd.Series([np.nan, np.nan, 0.0302, -0.0004, -0.0200, 0.0200], index=dates)
    assert_series_equal(result, expected, obj="Simple returns")

    result = returns(x, 1, Returns.LOGARITHMIC)
    expected = pd.Series([np.nan, 0.009950, 0.019803, -0.020203, 0.0, 0.019803], index=dates)
    assert_series_equal(result, expected, obj="Logarithmic returns", atol=1e-5)

    result = returns(x, 2, Returns.LOGARITHMIC)
    expected = pd.Series([np.nan, np.nan, 0.029753, -0.0004, -0.020203, 0.019803], index=dates)
    assert_series_equal(result, expected, obj="Logarithmic returns", atol=1e-5)

    result = returns(x, 1, Returns.ABSOLUTE)
    expected = pd.Series([np.nan, 1.0, 2.02, -2.0604, 0.0, 2.019192], index=dates)
    assert_series_equal(result, expected, obj="Absolute returns", atol=1e-5)

    result = returns(x, 2, Returns.ABSOLUTE)
    expected = pd.Series([np.nan, np.nan, 3.02, -0.0404, -2.0604, 2.019192], index=dates)
    assert_series_equal(result, expected, obj="Absolute returns", atol=1e-5)

    result = returns(x, '2d', Returns.ABSOLUTE)
    expected = pd.Series([np.nan, np.nan, 3.02, -0.0404, -2.0604, 2.019192], index=pd.DatetimeIndex(dates))
    assert_series_equal(result, expected, obj="Absolute returns with relative date")

    with pytest.raises(MqValueError):
        returns(x, 1, "None")


def test_prices():
    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 5),
        date(2019, 1, 6),
    ]

    r = pd.Series(dtype=float)
    assert_series_equal(r, prices(r))

    r = pd.Series([np.nan, 0.01, 0.02, -0.02, 0.0, 0.02], index=dates)

    result = prices(r)
    expected = pd.Series([1.0, 1.01, 1.0302, 1.009596, 1.009596, 1.02978792], index=dates)
    assert_series_equal(result, expected, obj="Simple price series default")

    result = prices(r, 100)
    expected = pd.Series([100.0, 101, 103.02, 100.9596, 100.9596, 102.978792], index=dates)
    assert_series_equal(result, expected, obj="Simple price series default")

    result = prices(r, 100, Returns.SIMPLE)
    expected = pd.Series([100.0, 101, 103.02, 100.9596, 100.9596, 102.978792], index=dates)
    assert_series_equal(result, expected, obj="Simple price series")

    r = pd.Series([np.nan, 0.009950, 0.019803, -0.020203, 0.0, 0.019803], index=dates)

    result = prices(r, 100, Returns.LOGARITHMIC)
    expected = pd.Series([100.0, 101, 103.02, 100.9596, 100.9596, 102.978792], index=dates)
    assert_series_equal(result, expected, obj="Logarithmic prices series")

    r = pd.Series([np.nan, 1.0, 2.02, -2.0604, 0.0, 2.019192], index=dates)

    result = prices(r, 100, Returns.ABSOLUTE)
    expected = pd.Series([100.0, 101, 103.02, 100.9596, 100.9596, 102.978792], index=dates)
    assert_series_equal(result, expected, obj="Absolute prices series")

    with pytest.raises(MqValueError):
        prices(r, 1, "None")


def test_index():
    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 5),
        date(2019, 1, 6),
    ]

    x = pd.Series([200, 202, 201, 203, 202, 201], index=dates)

    result = index(x)
    expected = pd.Series([1.000, 1.010, 1.005, 1.015, 1.010, 1.005], index=dates)
    assert_series_equal(result, expected, obj="Index series")

    with pytest.raises(MqValueError):
        x = pd.Series(range(6), index=dates)
        result = index(x)


def test_change():
    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 5),
        date(2019, 1, 6),
    ]

    x = pd.Series([200, 202, 201, 203, 202, 201.5], index=dates)

    result = change(x)
    expected = pd.Series([0.0, 2.0, 1.0, 3.0, 2.0, 1.5], index=dates)
    assert_series_equal(result, expected, obj="Change of series", check_series_type=False)


def test_annualize():
    daily_dates = [
        date(2019, 1, 1),
        date(2019, 1, 1),
        date(2019, 1, 1),
    ]

    daily_series = pd.Series([0.01, 0.02, -0.01], index=daily_dates)

    with pytest.raises(MqValueError):
        annualize(daily_series)

    daily_dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 5),
        date(2019, 1, 6),
    ]

    daily_series = pd.Series([0.01, 0.02, -0.01, 0.03, 0, -0.01], index=daily_dates)

    result = annualize(daily_series)
    assert_series_equal(result, daily_series * math.sqrt(252), obj="Annualize daily")

    weekly_dates = [
        date(2019, 1, 1),
        date(2019, 1, 8),
        date(2019, 1, 15),
        date(2019, 1, 22),
        date(2019, 1, 29),
        date(2019, 2, 6),
    ]

    weekly_series = pd.Series([0.01, 0.02, -0.01, 0.03, 0, -0.01], index=weekly_dates)

    result = annualize(weekly_series)
    assert_series_equal(result, weekly_series * math.sqrt(52), obj="Annualize weekly")

    semi_monthly_dates = [
        date(2019, 1, 1),
        date(2019, 1, 15),
        date(2019, 2, 1),
        date(2019, 2, 15),
        date(2019, 3, 1),
        date(2019, 3, 15),
    ]

    semi_monthly_series = pd.Series([0.01, 0.02, -0.01, 0.03, 0, -0.01], index=semi_monthly_dates)

    result = annualize(semi_monthly_series)
    assert_series_equal(result, semi_monthly_series * math.sqrt(26), obj="Annualize semi-monthly")

    monthly_dates = [
        date(2019, 1, 1),
        date(2019, 2, 1),
        date(2019, 3, 1),
        date(2019, 4, 1),
        date(2019, 5, 1),
        date(2019, 6, 1),
    ]

    monthly_series = pd.Series([0.01, 0.02, -0.01, 0.03, 0, -0.01], index=monthly_dates)

    result = annualize(monthly_series)
    assert_series_equal(result, monthly_series * math.sqrt(12), obj="Annualize monthly")

    quarterly_dates = [
        date(2019, 1, 1),
        date(2019, 3, 1),
        date(2019, 6, 1),
        date(2019, 9, 1),
        date(2020, 1, 1),
        date(2020, 3, 1),
    ]

    quarterly_series = pd.Series([0.01, 0.02, -0.01, 0.03, 0, -0.01], index=quarterly_dates)

    result = annualize(quarterly_series)
    assert_series_equal(result, quarterly_series * math.sqrt(4), obj="Annualize quarterly")

    annual_dates = [
        date(2019, 1, 1),
        date(2020, 1, 1),
        date(2021, 1, 1),
        date(2022, 1, 1),
        date(2023, 1, 1),
        date(2024, 1, 1),
    ]

    annual_series = pd.Series([0.01, 0.02, -0.01, 0.03, 0, -0.01], index=annual_dates)

    result = annualize(annual_series)
    assert_series_equal(result, annual_series, obj="Annualize annually")

    invalid_dates = [
        date(2019, 1, 1),
        date(2019, 1, 3),
        date(2019, 1, 6),
        date(2019, 1, 9),
        date(2019, 1, 12),
        date(2019, 1, 13),
    ]

    invalid_series = pd.Series([0.01, 0.02, -0.01, 0.03, 0, -0.01], index=invalid_dates)

    with pytest.raises(MqValueError):
        annualize(invalid_series)


def test_volatility():
    x = pd.Series(dtype=float)
    assert_series_equal(x, volatility(x))

    daily_dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 5),
        date(2019, 1, 6),
    ]

    x = pd.Series([100.0, 101, 103.02, 100.9596, 100.9596, 102.978792], index=daily_dates)

    std = 0.016733200530681527
    vol = std * math.sqrt(252) * 100

    real_vol = volatility(x)
    assert (real_vol[-1] == vol)

    result = volatility(x, w="3d")
    expected = pd.Series([33.04542, 31.74902, 31.74902], index=daily_dates[3:])
    assert_series_equal(result, expected, obj="Volatility strdate")

    result = volatility(x, w="3m")
    expected = pd.Series(dtype=float)
    assert_series_equal(pd.Series(dtype=float), expected, obj="Volatility strdate too large for series")


def test_correlation():
    x = pd.Series(dtype=float)
    assert_series_equal(pd.Series(dtype=float), correlation(x, x))
    assert_series_equal(pd.Series(dtype=float), correlation(x, x, 1))

    daily_dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 7),
        date(2019, 1, 8),
    ]

    x = pd.Series([100.0, 101, 103.02, 100.9596, 100.9596, 102.978792], index=daily_dates)
    y = pd.Series([100.0, 101, 103.02, 100.9596, 100.9596, 102.978792], index=daily_dates)

    result = correlation(x, y)
    expected = pd.Series([np.nan, np.nan, 1.0, 1.0, 1.0, 1.0], index=daily_dates)

    assert_series_equal(result, expected)

    y = pd.Series([100.0, 102.0, 104.0, 101.0, 100.95, 100.0], index=daily_dates)

    result = correlation(x, y)
    expected = pd.Series([np.nan, np.nan, -1.0, 0.969025, 0.969254, 0.706042], index=daily_dates)

    assert_series_equal(result, expected)

    result = correlation(x, y, Window(2, 0))
    expected = pd.Series([np.nan, np.nan, -1.0000000000000435, 1.0, 0.9999999999999994, -1.0000000000000007],
                         index=daily_dates)

    assert_series_equal(result, expected)

    ret_x = returns(x)
    ret_y = returns(y)

    result = correlation(ret_x, ret_y, Window(2, 0), False)
    values = [
        np.nan,
        np.nan,
        -1.0000000000000435,
        1.0,
        0.9999999999999994,
        -1.0000000000000007
    ]
    expected = pd.Series(values, index=daily_dates)

    assert_series_equal(result, expected)

    result = correlation(x, y, Window('2d', 0))
    expected = pd.Series([np.nan, np.nan, -1.0, 1.0, np.nan, -1.0], index=daily_dates)
    assert_series_equal(result, expected)

    result = correlation(x, y, "2d")
    expected = pd.Series([-1, 1, np.nan, -1], index=daily_dates[2:])
    assert_series_equal(result, expected, obj="Correlation strdate as window")

    result = correlation(x, y, "3m")
    expected = pd.Series(dtype=float, index=[])
    assert_series_equal(result, expected, obj="Correlation strdate as window with too large of window")


def test_beta():
    x = pd.Series(dtype=float)
    assert_series_equal(pd.Series(dtype=float), beta(x, x))
    assert_series_equal(pd.Series(dtype=float), beta(x, x, 1))

    daily_dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 7),
        date(2019, 1, 8),
    ]

    x = pd.Series([100.0, 101, 103.02, 100.9596, 100.9596, 102.978792], index=daily_dates)
    y = pd.Series([100.0, 101, 103.02, 100.9596, 100.9596, 102.978792], index=daily_dates)

    result = beta(x, y)
    expected = pd.Series([np.nan, np.nan, np.nan, 1.0, 1.0, 1.0], index=daily_dates)
    assert_series_equal(result, expected)

    y = pd.Series([100.0, 102.0, 104.0, 101.0, 100.95, 100.0], index=daily_dates)

    result = beta(x, y)
    expected = pd.Series([np.nan, np.nan, np.nan, 0.718146, 0.718919, 0.572201], index=daily_dates)
    assert_series_equal(result, expected)

    result = beta(x, y, Window(2, 0))
    expected = pd.Series([np.nan, np.nan, np.nan, 0.8255252918287954,
                          0.7054398925453326, -2.24327163719368], index=daily_dates)
    assert_series_equal(result, expected)

    ret_x = returns(x)
    ret_y = returns(y)

    result = beta(ret_x, ret_y, Window(2, 0), False)
    expected = pd.Series([np.nan, np.nan, np.nan, 0.8255252918287954,
                          0.7054398925453326, -2.24327163719368], index=daily_dates)
    assert_series_equal(result, expected)

    result = beta(x, y, Window('2d', 0))
    expected = pd.Series([np.nan, np.nan, np.nan, 0.8255252918287954,
                          np.nan, -2.24327163719368], index=daily_dates)
    assert_series_equal(result, expected)

    result = beta(x, y, '2d')
    expected = pd.Series([np.nan, 0.8255252918287954, np.nan, -2.24327163719368], index=daily_dates[2:])
    assert_series_equal(result, expected, obj="beta with strdate window")

    with pytest.raises(MqTypeError):
        beta(x, y, '2d', 1)


def test_max_drawdown():
    daily_dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 7),
        date(2019, 1, 8),
    ]

    series = pd.Series([1, 5, 5, 4, 4, 1], index=daily_dates)

    result = max_drawdown(series)
    expected = pd.Series([0.0, 0.0, 0.0, -0.2, -0.2, -0.8], index=daily_dates)
    assert_series_equal(result, expected, obj="Max drawdown")

    result = max_drawdown(series, Window(2, 0))
    expected = pd.Series([0.0, 0.0, 0.0, -0.2, -0.2, -0.75], index=daily_dates)
    assert_series_equal(result, expected, obj="Max drawdown window 2")

    with pytest.raises(TypeError):
        max_drawdown(pd.Series([1, 5, 5, 4, 4, 1]), Window('2d', 0))
    result = max_drawdown(series, Window('2d', 0))
    expected = pd.Series([0.0, 0.0, 0.0, -0.2, 0.0, -0.75], index=daily_dates)
    assert_series_equal(result, expected, obj="Max drawdown window 2d")


def test_excess_returns():
    replace = Replacer()
    file = os.path.join(os.path.dirname(__file__), '..', 'resources', 'MIDASER_SPX_USD.csv')
    df = pd.read_csv(file)
    df.index = pd.to_datetime(df['Date'])

    market_data = replace('gs_quant.timeseries.econometrics.GsDataApi.get_market_data', Mock())
    data = df.loc[:, ['USD']]
    data = data.rename(columns={'USD': 'spot'})
    market_data.return_value = data

    with pytest.raises(Exception):
        excess_returns(df['SPX'], CurrencyEnum.AED)

    actual = excess_returns(df['SPX'], CurrencyEnum.USD)
    expected = df['MIDASER']
    assert_series_equal(actual, expected, check_names=False)

    plot = excess_returns_(df['SPX'], RiskFreeRateCurrency.USD)
    assert_series_equal(plot, expected, check_names=False)

    actual = excess_returns(df['SPX'], Cash('MABCDE', 'T_SHARPE_USD'))
    assert_series_equal(actual, expected, check_names=False)

    actual = excess_returns(df['SPX'], 0.0175)
    file = os.path.join(os.path.dirname(__file__), '..', 'resources', 'Sharpe_SPX_0175.csv')
    expected = pd.read_csv(file).loc[:, 'ER']
    numpy.testing.assert_array_almost_equal(actual.values, expected.values)

    market_data.return_value = pd.DataFrame()
    with pytest.raises(MqError):
        excess_returns(df['SPX'], CurrencyEnum.USD)

    replace.restore()


def test_sharpe_ratio():
    file = os.path.join(os.path.dirname(__file__), '..', 'resources', 'MIDASER_SPX_USD.csv')
    price_df = pd.read_csv(file)
    price_df.index = pd.to_datetime(price_df['Date'])

    file = os.path.join(os.path.dirname(__file__), '..', 'resources', 'Sharpe_SPX_0175.csv')
    er_df = pd.read_csv(file)
    er_df.index = pd.to_datetime(er_df['Date'])

    replace = Replacer()
    er = replace('gs_quant.timeseries.econometrics.excess_returns', Mock())
    er.return_value = er_df['ER']
    actual = _get_ratio(price_df['SPX'], 0.0175, 0, day_count_convention=DayCountConvention.ACTUAL_360)
    numpy.testing.assert_almost_equal(actual.values, er_df['SR'].values, decimal=5)
    actual = sharpe_ratio(price_df['SPX'], RiskFreeRateCurrency.USD)
    numpy.testing.assert_almost_equal(actual.values, er_df['SR'].values, decimal=5)
    actual = sharpe_ratio(price_df['SPX'][:], RiskFreeRateCurrency.USD, '1m')
    expected = pd.Series([np.nan, np.nan, np.nan, 8.266434, 6.731811],
                         index=pd.date_range(datetime.date(2019, 2, 4), periods=5))
    numpy.testing.assert_almost_equal(actual[:5].values, expected.values, decimal=5)
    with pytest.raises(MqValueError):
        actual = sharpe_ratio(price_df['SPX'][:], RiskFreeRateCurrency.USD, 22, method=Interpolate.INTERSECT)

    replace.restore()

    actual = _get_ratio(price_df['SPX'], 0.0175, 10, day_count_convention=DayCountConvention.ACTUAL_360)
    numpy.testing.assert_almost_equal(actual.values, er_df['SR10'].values[10:], decimal=5)

    actual = _get_ratio(er_df['ER'], 0.0175, 0, day_count_convention=DayCountConvention.ACTUAL_360,
                        curve_type=CurveType.EXCESS_RETURNS)
    numpy.testing.assert_almost_equal(actual.values, er_df['SR'].values, decimal=5)


if __name__ == "__main__":
    pytest.main(args=["test_econometrics.py"])
