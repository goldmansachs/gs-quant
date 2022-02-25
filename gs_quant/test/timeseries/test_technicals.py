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


def test_moving_average():
    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 5),
        date(2019, 1, 6),
    ]

    x = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)

    result = moving_average(x)
    expected = pd.Series([3.0, 2.5, 8 / 3, 2.25, 2.4, 3.0], index=dates)
    assert_series_equal(result, expected, obj="Moving average")

    result = moving_average(x, Window(1, 0))
    expected = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)
    assert_series_equal(result, expected, obj="Moving average window 1")

    result = moving_average(x, Window(2, 0))
    expected = pd.Series([3.0, 2.5, 2.5, 2.0, 2.0, 4.5], index=dates)
    assert_series_equal(result, expected, obj="Moving average window 2")

    result = moving_average(x, "2d")
    expected = pd.Series([2.5, 2, 2, 4.5], index=dates[2:])
    assert_series_equal(result, expected, obj="Moving average strdate window")


def test_smoothed_moving_average():
    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 5),
        date(2019, 1, 6),
    ]

    x = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)

    result = smoothed_moving_average(x)
    expected = pd.Series([3.00000, 2.83333, 2.86111, 2.55093, 2.62577, 3.18814], index=dates)
    assert_series_equal(result, expected, obj="Smoothed moving average")

    result = smoothed_moving_average(x, Window(1, 0))
    expected = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)
    assert_series_equal(result, expected, obj="Smoothed moving average window 1")

    result = smoothed_moving_average(x, Window(2, 0))
    expected = pd.Series([3.00000, 2.50000, 2.75000, 1.87500, 2.43750, 4.21875], index=dates)
    assert_series_equal(result, expected, obj="Smoothed moving average window 2")

    result = smoothed_moving_average(x, "2d")
    expected = pd.Series([2.5, 1.75, 2.375, 4.1875], index=dates[2:])
    assert_series_equal(result, expected, obj="Smoothed moving average window strdate")

    result = smoothed_moving_average(x, "1m")
    expected = pd.Series(dtype=float)
    assert_series_equal(result, expected, obj="Smoothed moving average with wider window than series")


def test_macd():
    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 5),
        date(2019, 1, 6),
    ]

    x = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)
    assert (macd(x, 10, 10) == 0).all()

    assert (macd(x, 10, 12, s=1) == macd(x, 10, 12)).all()

    expected = pd.Series([0, -0.166667, 0.027778, -0.282407, 0.093364, 0.624871], index=dates)
    assert_series_equal(macd(x, 2, 3), expected)


def test_bollinger_bands():
    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 5),
        date(2019, 1, 6),
    ]

    x = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)

    expected_low = pd.Series([np.nan, 1.085786, 1.511966, 0.335146, 0.611146, -0.346640], index=dates)
    expected_high = pd.Series([np.nan, 3.914214, 3.821367, 4.164854, 4.188854, 6.346640], index=dates)

    result = bollinger_bands(x)

    low = result[0].squeeze()
    high = result[1].squeeze()

    assert_series_equal(low, expected_low, check_names=False, obj="Bollinger bands low")
    assert_series_equal(high, expected_high, check_names=False, obj="Bollinger bands high")

    result = bollinger_bands(x, "2d")
    print(result)


def test_relative_strength_index():
    dates = [datetime.date(2020, 1, 2),
             datetime.date(2020, 1, 3),
             datetime.date(2020, 1, 6),
             datetime.date(2020, 1, 7),
             datetime.date(2020, 1, 8),
             datetime.date(2020, 1, 9),
             datetime.date(2020, 1, 10),
             datetime.date(2020, 1, 13),
             datetime.date(2020, 1, 14),
             datetime.date(2020, 1, 15),
             datetime.date(2020, 1, 16),
             datetime.date(2020, 1, 17),
             datetime.date(2020, 1, 21),
             datetime.date(2020, 1, 22),
             datetime.date(2020, 1, 23),
             datetime.date(2020, 1, 24),
             datetime.date(2020, 1, 27),
             datetime.date(2020, 1, 28),
             datetime.date(2020, 1, 29),
             datetime.date(2020, 1, 30),
             datetime.date(2020, 1, 31),
             datetime.date(2020, 2, 3)]

    SPX_values = [3257.8501,
                  3234.8501,
                  3246.28,
                  3237.1799,
                  3253.05,
                  3274.7,
                  3265.3501,
                  3288.1299,
                  3283.1499,
                  3289.29,
                  3316.8101,
                  3329.6201,
                  3320.79,
                  3321.75,
                  3325.54,
                  3295.47,
                  3243.6299,
                  3276.24,
                  3273.3999,
                  3283.6599,
                  3225.52,
                  3248.9199]

    target_vals = [66.35899,
                   50.99377,
                   57.63855,
                   56.91475,
                   58.92162,
                   45.88014,
                   50.61763]

    w = 14
    SPX = pd.Series(data=SPX_values, index=dates)
    expected = pd.Series(data=target_vals, index=dates[w + 1:])
    result = relative_strength_index(SPX, w)
    assert_series_equal(result, expected, check_names=False, obj="Relative Strength Index")

    increasing_series = pd.Series(np.arange(1, 23, 1), index=dates)
    expected = pd.Series(data=np.ones(7) * 100, index=dates[15:])
    result = relative_strength_index(increasing_series, w)
    assert_series_equal(result, expected, check_names=False, obj="Relative Strength Index")

    result = relative_strength_index(SPX, "2w")
    print(result)


def test_exponential_moving_average():

    def ema_by_hand(ts, alpha=0.75):
        R = ts.copy()
        R *= 0
        R[0] = ts[0]
        for i in range(1, len(ts)):
            R[i] = alpha * R[i - 1] + (1 - alpha) * ts[i]
        return R

    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 5),
        date(2019, 1, 6),
    ]

    x = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)

    result = exponential_moving_average(x)
    expected = ema_by_hand(x)
    assert_series_equal(result, expected, obj="Exponential moving average")

    result = exponential_moving_average(x, 0.6)
    expected = ema_by_hand(x, 0.6)
    assert_series_equal(result, expected, obj="Exponential moving average weight 1")

    result = exponential_moving_average(x, 0)
    expected = x
    assert_series_equal(result, expected, obj="Exponential moving average weight 2")


def test_exponential_volatility():
    dates = pd.date_range('2019-1-1', periods=6)
    x = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)
    result = exponential_volatility(x)
    expected = pd.Series([np.nan, np.nan, 935.41, 810.31, 1958.56, 1710.02], index=dates)
    assert_series_equal(result, expected, obj="Exponential volatility")


def test_exponential_spread_volatility():
    dates = pd.date_range('2019-1-1', periods=6)
    x = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)
    result = exponential_spread_volatility(x)
    expected = pd.Series([np.nan, np.nan, 22.4499, 20.5757, 28.6067, 34.2183], index=dates)
    assert_series_equal(result, expected, obj="Exponential spread volatility")


def test_trend():
    short_dates = pd.date_range('2021-01-01', '2021-01-05', freq='D')
    short_x = pd.Series(range(len(short_dates)), index=short_dates)
    with pytest.raises(MqValueError):
        trend(short_x)  # Too few datapoints
    long_dates = pd.date_range('2017-01-01', '2021-01-01', freq='D')
    long_x = pd.Series(range(len(long_dates)), index=long_dates)
    res = trend(long_x)  # Should not be all NaN, make sure it's correct length
    assert len(res) == len(long_x)
    assert np.isclose(res[int(len(res) / 2)], long_x[int(len(res) / 2)], 0.1)
    assert res.notnull().any()
    with pytest.raises(ValueError):
        trend(long_x, SeasonalModel.MULTIPLICATIVE)  # Should not be all NaN, make sure it's correct length
    res = trend(long_x + 1, SeasonalModel.MULTIPLICATIVE)  # Should not be all NaN, make sure it's correct length
    assert len(res) == len(long_x)
    assert np.isclose((res[int(len(res) / 2)] - 1), long_x[int(len(res) / 2)], 0.1)
    assert res.notnull().any()
    with pytest.raises(MqValueError):
        x = pd.Series(range(10))
        trend(x)


def test_seasonality_adjusted():
    # Test that correctly runs with different frequencies
    for pfreq in ['B', 'D', 'W', 'M', 'Q', 'Y']:
        for freq in [Frequency.YEAR, Frequency.QUARTER, Frequency.MONTH, Frequency.WEEK]:
            dates = pd.date_range('2019-01-01', '2021-01-05', freq=pfreq)
            series = pd.Series(range(len(dates)), index=dates) + 1
            try:
                seasonally_adjusted(series, SeasonalModel.ADDITIVE, freq)
                seasonally_adjusted(series, SeasonalModel.MULTIPLICATIVE, freq)
            except MqValueError:
                pass
    with pytest.raises(MqValueError):
        x = pd.Series(range(10))
        seasonally_adjusted(x)


if __name__ == "__main__":
    pytest.main(args=["test_technicals.py"])
