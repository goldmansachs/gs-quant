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
import math
import os
from unittest.mock import Mock

import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_series_equal
from testfixtures import Replacer

from gs_quant.common import Currency as CurrencyEnum
from gs_quant.datetime import DayCountConvention
from gs_quant.errors import MqValueError, MqTypeError, MqError
from gs_quant.markets.securities import Cash
from gs_quant.timeseries import returns, prices, index, change, annualize, volatility, correlation, beta, \
    max_drawdown, Returns, Window, Direction, generate_series, SeriesType, Interpolate, CurveType
from gs_quant.timeseries.econometrics import _get_ratio, excess_returns, RiskFreeRateCurrency, sharpe_ratio, \
    excess_returns_, corr_swap_correlation, vol_swap_volatility


def test_returns():
    dates = [
        dt.date(2019, 1, 1),
        dt.date(2019, 1, 2),
        dt.date(2019, 1, 3),
        dt.date(2019, 1, 4),
        dt.date(2019, 1, 5),
        dt.date(2019, 1, 6),
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
        dt.date(2019, 1, 1),
        dt.date(2019, 1, 2),
        dt.date(2019, 1, 3),
        dt.date(2019, 1, 4),
        dt.date(2019, 1, 5),
        dt.date(2019, 1, 6),
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
        dt.date(2019, 1, 1),
        dt.date(2019, 1, 2),
        dt.date(2019, 1, 3),
        dt.date(2019, 1, 4),
        dt.date(2019, 1, 5),
        dt.date(2019, 1, 6),
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
        dt.date(2019, 1, 1),
        dt.date(2019, 1, 2),
        dt.date(2019, 1, 3),
        dt.date(2019, 1, 4),
        dt.date(2019, 1, 5),
        dt.date(2019, 1, 6),
    ]

    x = pd.Series([200, 202, 201, 203, 202, 201.5], index=dates)

    result = change(x)
    expected = pd.Series([0.0, 2.0, 1.0, 3.0, 2.0, 1.5], index=dates)
    assert_series_equal(result, expected, obj="Change of series", check_series_type=False)


def test_annualize():
    daily_dates = [
        dt.date(2019, 1, 1),
        dt.date(2019, 1, 1),
        dt.date(2019, 1, 1),
    ]

    daily_series = pd.Series([0.01, 0.02, -0.01], index=daily_dates)

    with pytest.raises(MqValueError):
        annualize(daily_series)

    daily_dates = [
        dt.date(2019, 1, 1),
        dt.date(2019, 1, 2),
        dt.date(2019, 1, 3),
        dt.date(2019, 1, 4),
        dt.date(2019, 1, 5),
        dt.date(2019, 1, 6),
    ]

    daily_series = pd.Series([0.01, 0.02, -0.01, 0.03, 0, -0.01], index=daily_dates)

    result = annualize(daily_series)
    assert_series_equal(result, daily_series * math.sqrt(252), obj="Annualize daily")

    weekly_dates = [
        dt.date(2019, 1, 1),
        dt.date(2019, 1, 8),
        dt.date(2019, 1, 15),
        dt.date(2019, 1, 22),
        dt.date(2019, 1, 29),
        dt.date(2019, 2, 6),
    ]

    weekly_series = pd.Series([0.01, 0.02, -0.01, 0.03, 0, -0.01], index=weekly_dates)

    result = annualize(weekly_series)
    assert_series_equal(result, weekly_series * math.sqrt(52), obj="Annualize weekly")

    semi_monthly_dates = [
        dt.date(2019, 1, 1),
        dt.date(2019, 1, 15),
        dt.date(2019, 2, 1),
        dt.date(2019, 2, 15),
        dt.date(2019, 3, 1),
        dt.date(2019, 3, 15),
    ]

    semi_monthly_series = pd.Series([0.01, 0.02, -0.01, 0.03, 0, -0.01], index=semi_monthly_dates)

    result = annualize(semi_monthly_series)
    assert_series_equal(result, semi_monthly_series * math.sqrt(26), obj="Annualize semi-monthly")

    monthly_dates = [
        dt.date(2019, 1, 1),
        dt.date(2019, 2, 1),
        dt.date(2019, 3, 1),
        dt.date(2019, 4, 1),
        dt.date(2019, 5, 1),
        dt.date(2019, 6, 1),
    ]

    monthly_series = pd.Series([0.01, 0.02, -0.01, 0.03, 0, -0.01], index=monthly_dates)

    result = annualize(monthly_series)
    assert_series_equal(result, monthly_series * math.sqrt(12), obj="Annualize monthly")

    quarterly_dates = [
        dt.date(2019, 1, 1),
        dt.date(2019, 3, 1),
        dt.date(2019, 6, 1),
        dt.date(2019, 9, 1),
        dt.date(2020, 1, 1),
        dt.date(2020, 3, 1),
    ]

    quarterly_series = pd.Series([0.01, 0.02, -0.01, 0.03, 0, -0.01], index=quarterly_dates)

    result = annualize(quarterly_series)
    assert_series_equal(result, quarterly_series * math.sqrt(4), obj="Annualize quarterly")

    annual_dates = [
        dt.date(2019, 1, 1),
        dt.date(2020, 1, 1),
        dt.date(2021, 1, 1),
        dt.date(2022, 1, 1),
        dt.date(2023, 1, 1),
        dt.date(2024, 1, 1),
    ]

    annual_series = pd.Series([0.01, 0.02, -0.01, 0.03, 0, -0.01], index=annual_dates)

    result = annualize(annual_series)
    assert_series_equal(result, annual_series, obj="Annualize annually")

    invalid_dates = [
        dt.date(2019, 1, 1),
        dt.date(2019, 1, 3),
        dt.date(2019, 1, 6),
        dt.date(2019, 1, 9),
        dt.date(2019, 1, 12),
        dt.date(2019, 1, 13),
    ]

    invalid_series = pd.Series([0.01, 0.02, -0.01, 0.03, 0, -0.01], index=invalid_dates)

    with pytest.raises(MqValueError):
        annualize(invalid_series)


def test_volatility():
    x = pd.Series(dtype=float)
    assert_series_equal(x, volatility(x))

    daily_dates = [
        dt.date(2019, 1, 1),
        dt.date(2019, 1, 2),
        dt.date(2019, 1, 3),
        dt.date(2019, 1, 4),
        dt.date(2019, 1, 5),
        dt.date(2019, 1, 6),
    ]

    x = pd.Series([100.0, 101, 103.02, 100.9596, 100.9596, 102.978792], index=daily_dates)

    std = 0.016733200530681527
    vol = std * math.sqrt(252) * 100

    real_vol = volatility(x)
    assert (real_vol[-1] == vol)

    vol_already_returns = volatility(returns(x), returns_type=None)
    assert_series_equal(vol_already_returns, real_vol, obj="Volatility strdate")

    result = volatility(x, w="3d")
    expected = pd.Series([33.04542, 31.74902, 31.74902], index=daily_dates[3:])
    assert_series_equal(result, expected, obj="Volatility strdate")

    result = volatility(x, w="3m")
    expected = pd.Series(dtype=float)
    assert_series_equal(pd.Series(dtype=float), expected, obj="Volatility strdate too large for series")


def test_volatility_assume_zero_mean():
    dates = pd.date_range(start='2020-01-01', periods=50, freq='D')
    prices = pd.Series([100, 102, 101, 103, 102, 104, 103, 105, 104, 106,
                        105, 107, 106, 108, 107, 109, 108, 110, 109, 111,
                        110, 112, 111, 113, 112, 114, 113, 115, 114, 116,
                        115, 117, 116, 118, 117, 119, 118, 120, 119, 121,
                        120, 122, 121, 123, 122, 124, 123, 125, 124, 126],
                       index=dates)

    window_size = 10

    # zero-mean should give different result than standard volatility
    vol_zero_mean = volatility(prices, w=window_size, assume_zero_mean=True)
    vol_standard = volatility(prices, w=window_size, assume_zero_mean=False)
    assert not np.allclose(vol_zero_mean.dropna(), vol_standard.dropna()), \
        "Zero-mean and standard volatility should differ"

    # manual calc check
    result = volatility(prices, w=window_size, returns_type=Returns.LOGARITHMIC,
                        assume_zero_mean=True)

    log_returns = np.log(prices / prices.shift(1)).dropna()
    last_window_returns = log_returns.iloc[-window_size:].values
    expected_vol = np.sqrt(np.mean(last_window_returns ** 2)) * np.sqrt(252) * 100

    assert abs(result.iloc[-1] - expected_vol) < 0.01, \
        f"Manual calculation mismatch: {result.iloc[-1]} vs {expected_vol}"

    # single value window
    vol_single = volatility(prices, w=1, assume_zero_mean=True)
    assert not vol_single.empty, "Should handle window size of 1"

    # full series (no window)
    vol_full = volatility(prices, returns_type=Returns.LOGARITHMIC, assume_zero_mean=True)
    all_returns = np.log(prices / prices.shift(1)).dropna().values
    expected_full = np.sqrt(np.mean(all_returns ** 2)) * np.sqrt(252) * 100

    assert abs(vol_full.iloc[-1] - expected_full) < 0.01, \
        f"Full series calculation incorrect: {vol_full.iloc[-1]} vs {expected_full}"


def test_volatility_annualization_factor():
    rng = np.random.default_rng(100)
    dates = pd.date_range(start='2025-01-01', periods=252, freq='B')

    # Generate returns with ~20% annual volatility
    daily_vol = 0.20 / np.sqrt(252)
    returns = rng.normal(0, daily_vol, 252)
    prices = pd.Series(100 * np.exp(np.cumsum(returns)), index=dates)

    vol_auto = volatility(prices, returns_type=Returns.LOGARITHMIC)
    vol_252 = volatility(prices, returns_type=Returns.LOGARITHMIC, annualization_factor=252)
    vol_255 = volatility(prices, returns_type=Returns.LOGARITHMIC, annualization_factor=255)

    assert_series_equal(vol_auto, vol_252)

    expected_ratio_255 = np.sqrt(255 / 252)
    actual_ratio_255 = vol_255.iloc[-1] / vol_252.iloc[-1]
    np.testing.assert_almost_equal(actual_ratio_255, expected_ratio_255, decimal=5)

    vol_swap = volatility(prices, returns_type=Returns.LOGARITHMIC,
                          annualization_factor=255, assume_zero_mean=True)

    assert not np.allclose(vol_swap.iloc[-1], vol_255.iloc[-1]), \
        "Zero-mean volatility should differ from standard volatility"

    final_vol = vol_252.iloc[-1]
    assert 15 < final_vol < 25, \
        "Volatility should be around 20%"


def test_vol_swap_volatility():
    rng = np.random.default_rng(100)
    dates = pd.date_range(start='2025-01-01', periods=50, freq='D')
    returns = rng.normal(0, 0.01, 49)
    prices = pd.Series(100 * np.exp(np.cumsum(np.concatenate([[0], returns]))), index=dates)

    # ramp-up must be w - 1
    with pytest.raises(MqTypeError):
        vol_swap_volatility(prices, n_days=Window(22, 0))

    for n_days in [3, 25, 49, 50]:
        # Windows and numbers get treated identically
        pd.testing.assert_series_equal(vol_swap_volatility(prices, n_days=n_days),
                                       vol_swap_volatility(prices, n_days=Window(n_days, n_days - 1)))

    result_wrapper = vol_swap_volatility(prices, n_days=22)
    result_direct = volatility(prices, Window(22, 21), Returns.LOGARITHMIC, 252, True)

    assert_series_equal(result_wrapper, result_direct)

    result_wrapper = vol_swap_volatility(prices, n_days=22, annualization_factor=365)
    result_direct = volatility(prices, Window(22, 21), Returns.LOGARITHMIC, 365, True)

    assert_series_equal(result_wrapper, result_direct)

    result_wrapper = vol_swap_volatility(prices, n_days=22, assume_zero_mean=False)
    result_direct = volatility(prices, Window(22, 21), Returns.LOGARITHMIC, 252, False)

    assert_series_equal(result_wrapper, result_direct)

    result_wrapper = vol_swap_volatility(prices)
    result_direct = volatility(prices, Window(50, 49), Returns.LOGARITHMIC, 252, True)

    assert_series_equal(result_wrapper, result_direct)


def test_correlation():
    x = pd.Series(dtype=float)
    assert_series_equal(pd.Series(dtype=float), correlation(x, x))
    assert_series_equal(pd.Series(dtype=float), correlation(x, x, 1))

    daily_dates = [
        dt.date(2019, 1, 1),
        dt.date(2019, 1, 2),
        dt.date(2019, 1, 3),
        dt.date(2019, 1, 4),
        dt.date(2019, 1, 7),
        dt.date(2019, 1, 8),
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


def test_correlation_returns():
    x = generate_series(50, Direction.END_TODAY)
    y = generate_series(50, Direction.END_TODAY)
    base_corr = correlation(x, y)
    corr_simple = correlation(x, y, returns_type=Returns.SIMPLE)
    assert_series_equal(base_corr, corr_simple)

    #  Log returns
    corr_log = correlation(x, y, returns_type=Returns.LOGARITHMIC)
    returns_x = returns(x, type=Returns.LOGARITHMIC)
    returns_y = returns(y, type=Returns.LOGARITHMIC)
    corr_log_manual = correlation(returns_x, returns_y, type_=SeriesType.RETURNS)
    assert_series_equal(corr_log, corr_log_manual)

    # Mixed returns type
    corr_log_abs = correlation(x, y, returns_type=(Returns.LOGARITHMIC, Returns.ABSOLUTE))
    returns_y = returns(y, type=Returns.ABSOLUTE)
    corr_log_manual = correlation(returns_x, returns_y, type_=SeriesType.RETURNS)
    assert_series_equal(corr_log_abs, corr_log_manual)

    # Error cases
    with pytest.raises(MqValueError):
        correlation(x, y, returns_type=[Returns.SIMPLE])
    with pytest.raises(MqTypeError):
        correlation(x, y, returns_type=["simple", "logarithmic"])


def test_corr_swap_correlation():
    assert corr_swap_correlation(pd.Series(), pd.Series()).empty

    num_dates = 10
    dates = pd.to_datetime(pd.date_range(start='2025-01-01', periods=num_dates))
    rng = np.random.default_rng()
    x = pd.Series(rng.random(num_dates), index=dates)
    y = pd.Series(rng.random(num_dates), index=dates)

    # ramp-up must be w - 1
    with pytest.raises(MqTypeError):
        corr_swap_correlation(x, y, n_days=Window(3, 0))

    for n_days in [3, 5, 9, 10]:
        # Windows and numbers get treated identically
        pd.testing.assert_series_equal(corr_swap_correlation(x, y, n_days=n_days),
                                       corr_swap_correlation(x, y, n_days=Window(n_days - 1, n_days - 2)))

    # n_days left unspecified defaults to the number of price dates
    pd.testing.assert_series_equal(corr_swap_correlation(x, y, n_days=num_dates),
                                   corr_swap_correlation(x, y,))

    for window_size in [3, 5, 9]:
        # assume_zero_mean=False should match correlation function
        corr = correlation(x, y, returns_type=Returns.LOGARITHMIC, w=Window(window_size, window_size - 1))
        corr_swap_corr = corr_swap_correlation(x, y, n_days=window_size + 1, assume_zero_mean=False)
        pd.testing.assert_series_equal(corr, corr_swap_corr)

        # assume_zero_mean=True yields correct numbers that are different from assume_zero_mean=False
        zero_mean_corr_swap_corr = corr_swap_correlation(x, y, n_days=window_size + 1)
        assert not np.allclose(corr_swap_corr.values, zero_mean_corr_swap_corr.values, rtol=1e-10)

        zero_mean_corr_swap_corr = zero_mean_corr_swap_corr.iloc[1:]  # drop the first NaN
        assert np.all(zero_mean_corr_swap_corr.between(-1.0, 1.0))
        # manually verify the first valid correlation (originally at index 1, now at iloc[0])
        ret_x = np.log(x / x.shift(1)).dropna()
        ret_y = np.log(y / y.shift(1)).dropna()
        window_x = ret_x.iloc[0:window_size].values
        window_y = ret_y.iloc[0:window_size].values
        denom = len(window_x)
        var_x = np.sum(window_x ** 2) / denom
        var_y = np.sum(window_y ** 2) / denom
        covar = np.sum(window_x * window_y) / denom
        if var_x > 0 and var_y > 0:
            expected_zero_mean_corr = covar / (np.sqrt(var_x) * np.sqrt(var_y))
            actual_zero_mean_corr = zero_mean_corr_swap_corr.iloc[0]
            np.testing.assert_almost_equal(
                actual_zero_mean_corr,
                expected_zero_mean_corr,
                decimal=10,
                err_msg=f"Zero-mean correlation mismatch for window_size={window_size}"
            )


def test_beta():
    x = pd.Series(dtype=float)
    assert_series_equal(pd.Series(dtype=float), beta(x, x))
    assert_series_equal(pd.Series(dtype=float), beta(x, x, 1))

    daily_dates = [
        dt.date(2019, 1, 1),
        dt.date(2019, 1, 2),
        dt.date(2019, 1, 3),
        dt.date(2019, 1, 4),
        dt.date(2019, 1, 7),
        dt.date(2019, 1, 8),
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
        dt.date(2019, 1, 1),
        dt.date(2019, 1, 2),
        dt.date(2019, 1, 3),
        dt.date(2019, 1, 4),
        dt.date(2019, 1, 7),
        dt.date(2019, 1, 8),
    ]
    daily_dates = pd.to_datetime(daily_dates)

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
    np.testing.assert_array_almost_equal(actual.values, expected.values)

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
    np.testing.assert_almost_equal(actual.values, er_df['SR'].values, decimal=5)
    actual = sharpe_ratio(price_df['SPX'], RiskFreeRateCurrency.USD)
    np.testing.assert_almost_equal(actual.values, er_df['SR'].values, decimal=5)
    actual = sharpe_ratio(price_df['SPX'][:], RiskFreeRateCurrency.USD, '1m')
    expected = pd.Series([np.nan, np.nan, np.nan, 8.266434, 6.731811],
                         index=pd.date_range(dt.date(2019, 2, 4), periods=5))
    np.testing.assert_almost_equal(actual[:5].values, expected.values, decimal=5)
    with pytest.raises(MqValueError):
        actual = sharpe_ratio(price_df['SPX'][:], RiskFreeRateCurrency.USD, 22, method=Interpolate.INTERSECT)

    replace.restore()

    actual = _get_ratio(price_df['SPX'], 0.0175, 10, day_count_convention=DayCountConvention.ACTUAL_360)
    np.testing.assert_almost_equal(actual.values, er_df['SR10'].values[10:], decimal=5)

    actual = _get_ratio(er_df['ER'], 0.0175, 0, day_count_convention=DayCountConvention.ACTUAL_360,
                        curve_type=CurveType.EXCESS_RETURNS)
    np.testing.assert_almost_equal(actual.values, er_df['SR'].values, decimal=5)


if __name__ == "__main__":
    pytest.main(args=["test_econometrics.py"])
