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

//Portions copyright Maximilian Boeck. Licensed under Apache 2.0 license
"""

import pytest
from gs_quant.timeseries import *
from gs_quant.timeseries.statistics import Direction
from pandas.testing import assert_series_equal
from scipy.integrate import odeint


def _random_series(days=365, nans=10):
    assert nans < days
    values = np.random.random(days)
    nan_indexes = np.floor(np.random.random(nans) * len(values)).astype(np.int_)
    for i in nan_indexes:
        values[i] = np.nan

    return pd.Series(values, index=pd.date_range(start="2021-01-01", periods=days, freq='D'))


def _rolling_1m_test(fn, pandas_fn: str):
    x = _random_series()
    window = normalize_window(x, Window('1m', 0))
    result = fn(x, window)
    values = (getattr(x.loc[(x.index > idx - window.w) & (x.index <= idx)], pandas_fn)() for idx in x.index)
    expected = pd.Series(values, index=x.index)
    assert_series_equal(result, expected, obj=f"{pandas_fn} with date window 1m")


def test_generate_series():
    x = generate_series(100)

    assert (len(x) == 100)
    assert (x.index[0] == datetime.date.today())
    assert (x.iloc[0] == 100)

    x = generate_series(100, Direction.END_TODAY)
    assert (len(x) == 100)
    assert (x.index[-1] == datetime.date.today())
    assert (x.iloc[0] == 100)


def test_min():
    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 7),
        date(2019, 1, 8),
    ]

    x = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)
    z = pd.Series([2.0, 5.0, 4.0, 0.0, 1.0, 3.0], index=dates)
    result = min_([x, z], Window('2d', 0))
    expected = pd.Series([2.0, 2.0, 2.0, 0.0, 1.0, 1.0], index=dates)
    assert_series_equal(result, expected, obj="Minimum list 2d")

    result = min_(x)
    expected = pd.Series([3.0, 2.0, 2.0, 1.0, 1.0, 1.0], index=dates)
    assert_series_equal(result, expected, obj="Minimum")

    result = min_(x, Window(1, 0))
    expected = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)
    assert_series_equal(result, expected, obj="Minimum window 1")

    result = min_(x, Window(2, 0))
    expected = pd.Series([3.0, 2.0, 2.0, 1.0, 1.0, 3.0], index=dates)
    assert_series_equal(result, expected, obj="Minimum window 2")

    result = min_(x, Window('1w', 0))
    expected = pd.Series([3.0, 2.0, 2.0, 1.0, 1.0, 1.0], index=dates)
    assert_series_equal(result, expected, obj="Minimum with window 1w")

    y = pd.Series([4.0, np.nan, 4.0, 2.0, 2.0, 5.0], index=dates)
    result = min_([x, y], Window(2, 0))
    expected = pd.Series([3.0, 2.0, 2.0, 1.0, 1.0, 2.0], index=dates)
    assert_series_equal(result, expected, obj="Minimum of multiple series")

    result = min_(x, "2d")
    expected = pd.Series([2.0, 1.0, 3.0, 3.0], index=dates[2:])
    assert_series_equal(result, expected, obj="Minimum with strdate window")

    result = min_(x, "1d")
    expected = pd.Series([2.0, 3.0, 1.0, 3.0, 6.0], index=dates[1:])
    assert_series_equal(result, expected, obj="Minimum with strdate window 2")

    ranges = pd.date_range('20220101', periods=6, freq='40min')
    y = pd.Series([4.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=ranges)
    result = min_(y, '2h')
    expected = pd.Series([1.0, 1.0, 1.0], index=ranges[3:])
    assert_series_equal(result, expected, obj="Minimum with string window 2h")

    _rolling_1m_test(min_, 'min')


def test_max():
    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 7),
        date(2019, 1, 8),
    ]

    x = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)
    z = pd.Series([1.0, 0.0, 4.0, 3.5, 7.0, 8.0], index=dates)

    result = max_([x, z], Window('2d', 0))
    expected = pd.Series([3.0, 3.0, 4.0, 4.0, 7.0, 8.0], index=dates)
    assert_series_equal(result, expected, obj="Maximum list 2d")

    result = max_(x)
    expected = pd.Series([3.0, 3.0, 3.0, 3.0, 3.0, 6.0], index=dates)
    assert_series_equal(result, expected, obj="Maximum")

    result = max_(x, Window(1, 0))
    expected = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)
    assert_series_equal(result, expected, obj="Maximum window 1")

    result = max_(x, Window(2, 0))
    expected = pd.Series([3.0, 3.0, 3.0, 3.0, 3.0, 6.0], index=dates)
    assert_series_equal(result, expected, obj="Maximum window 2")

    result = max_(x, Window('2d', 0))
    expected = pd.Series([3.0, 3.0, 3.0, 3.0, 3.0, 6.0], index=dates)
    assert_series_equal(result, expected, obj="Maximum window 1w")

    y = pd.Series([4.0, np.nan, 4.0, 2.0, 2.0, 5.0], index=dates)
    result = max_([x, y], Window(2, 0))
    expected = pd.Series([4.0, 4.0, 4.0, 4.0, 3.0, 6.0], index=dates)
    assert_series_equal(result, expected, obj="Maximum of multiple series")

    s = pd.Series([-3.0, -2.0, 3.0, -1.0, -3.0, 6.0], index=dates)
    t = pd.Series([0, 0], index=dates[0:2])
    result = max_([s, t], 1)
    expected = pd.Series([0.0, 3, 0, 0, 6], index=dates[1:])
    assert_series_equal(result, expected, obj="Maximum with constant")

    ranges = pd.date_range('20220101', periods=6, freq='30min')
    y = pd.Series([4.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=ranges)
    result = max_(y, '1h')
    expected = pd.Series([3.0, 3.0, 3.0, 6.0], index=ranges[2:])
    assert_series_equal(result, expected, obj="Maximum with string window 1h")

    _rolling_1m_test(max_, 'max')


def test_range():
    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 7),
        date(2019, 1, 8),
    ]

    x = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)

    result = range_(x)
    expected = pd.Series([0.0, 1.0, 1.0, 2.0, 2.0, 5.0], index=dates)
    assert_series_equal(result, expected, obj="Range")

    result = range_(x, Window(1, 0))
    expected = pd.Series([0.0, 0.0, 0.0, 0.0, 0.0, 0.0], index=dates)
    assert_series_equal(result, expected, obj="Range window 1")

    result = range_(x, Window(2, 0))
    expected = pd.Series([0.0, 1.0, 1.0, 2.0, 2.0, 3.0], index=dates)
    assert_series_equal(result, expected, obj="Range window 2")

    result = range_(x, Window('1w', 0))
    expected = pd.Series([0.0, 1.0, 1.0, 2.0, 2.0, 5.0], index=dates)
    assert_series_equal(result, expected, obj="Range window 1w")


def test_mean():
    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 7),
        date(2019, 1, 8),
    ]

    x = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)

    result = mean(x)
    expected = pd.Series([3.0, 2.5, 8 / 3, 2.25, 2.4, 3.0], index=dates)
    assert_series_equal(result, expected, obj="Mean")

    result = mean(x, Window(1, 0))
    expected = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)
    assert_series_equal(result, expected, obj="Mean window 1")

    result = mean(x, Window(2, 0))
    expected = pd.Series([3.0, 2.5, 2.5, 2.0, 2.0, 4.5], index=dates)
    assert_series_equal(result, expected, obj="Mean window 2")

    result = mean(x, Window('1w', 0))
    expected = pd.Series([3.0, 2.5, 8 / 3, 2.25, 2.4, 3.0], index=dates)
    assert_series_equal(result, expected, obj="Mean window 1w")

    y = pd.Series([4.0, np.nan, 4.0, 2.0, 2.0, 5.0], index=dates)
    result = mean([x, y], Window(2, 0))
    expected = pd.Series([3.5, 3.0, 3.0, 2.5, 2.0, 4.0], index=dates)
    assert_series_equal(result, expected, obj="Mean of multiple series")

    result = mean([x, y], Window('2d', 0))
    expected = pd.Series([3.5, 3, 3, 2.5, 2.5, 4], index=dates)
    assert_series_equal(result, expected, obj="Mean of multiple series by date offset")

    result = mean(y, Window(2, 0))
    expected = pd.Series([4.0, 4.0, 4.0, 3.0, 2.0, 3.5], index=dates)
    assert_series_equal(result, expected, obj="Mean of single series with nan")


def test_median():
    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 7),
        date(2019, 1, 8),
    ]

    x = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)

    result = median(x)
    expected = pd.Series([3.0, 2.5, 3.0, 2.5, 3.0, 3.0], index=dates)
    assert_series_equal(result, expected, obj="Median")

    result = median(x, Window(1, 0))
    expected = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)
    assert_series_equal(result, expected, obj="Median window 1")

    result = median(x, Window(2, 0))
    expected = pd.Series([3.0, 2.5, 2.5, 2.0, 2.0, 4.5], index=dates)
    assert_series_equal(result, expected, obj="Median window 2")

    result = median(x, Window('1w', 0))
    expected = pd.Series([3.0, 2.5, 3.0, 2.5, 3.0, 3.0], index=dates)
    assert_series_equal(result, expected, obj="Median window 1w")

    _rolling_1m_test(median, 'median')


def test_mode():
    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 7),
        date(2019, 1, 8),
    ]

    x = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)

    result = mode(x)
    expected = pd.Series([3.0, 2.0, 3.0, 3.0, 3.0, 3.0], index=dates)
    assert_series_equal(result, expected, obj="mode")

    result = mode(x, Window(1, 0))
    expected = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)
    assert_series_equal(result, expected, obj="mode window 1")

    result = mode(x, Window(2, 0))
    expected = pd.Series([3.0, 2.0, 2.0, 1.0, 1.0, 3.0], index=dates)
    assert_series_equal(result, expected, obj="mode window 2")

    result = mode(x, Window('1w', 0))
    expected = pd.Series([3.0, 2.0, 3.0, 3.0, 3.0, 3.0], index=dates)
    assert_series_equal(result, expected, obj="Mode window 1w")

    x = _random_series()
    window = normalize_window(x, Window('1m', 0))
    result = mode(x, window)
    values = (stats.mode(x.loc[(x.index > idx - window.w) & (x.index <= idx)]).mode[0] for idx in x.index)
    expected = pd.Series(values, index=x.index)
    assert_series_equal(result, expected, obj="Mode window 1m")


def test_sum():
    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 7),
        date(2019, 1, 8),
    ]

    x = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], index=dates)

    result = sum_(x)
    expected = pd.Series([1.0, 3.0, 6.0, 10, 15, 21], index=dates)
    assert_series_equal(result, expected, obj="Summation")

    result = sum_(x, Window(2, 0))
    expected = pd.Series([1.0, 3.0, 5.0, 7.0, 9.0, 11.0], index=dates)
    assert_series_equal(result, expected, obj="Summation")

    result = sum_(x, Window('1w', 0))
    expected = pd.Series([1.0, 3.0, 6.0, 10.0, 15.0, 20.0], index=dates)
    assert_series_equal(result, expected, obj="Sum window 1w")

    y = pd.Series([4.0, np.nan, 4.0, 2.0, 2.0, 5.0], index=dates)
    result = sum_([x, y], Window(2, 0))
    expected = pd.Series([5.0, 7.0, 9.0, 13.0, 13.0, 18.0], index=dates)
    assert_series_equal(result, expected, obj="Sum of multiple series")

    result = sum_(y, Window('2d', 0))
    expected = pd.Series([4, 4, 4, 6, 2, 7], index=dates, dtype=np.double)
    assert_series_equal(result, expected, obj="Sum with nan input")


def test_product():
    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 7),
        date(2019, 1, 8),
    ]

    x = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], index=dates)

    result = product(x)
    expected = pd.Series([1.0, 2.0, 6.0, 24, 120, 720], index=dates)
    assert_series_equal(result, expected, obj="Product")

    result = product(x, Window(2, 0))
    expected = pd.Series([1.0, 2.0, 6.0, 12.0, 20.0, 30.0], index=dates)
    assert_series_equal(result, expected, obj="Product")

    result = product(x, Window('1w', 0))
    expected = pd.Series([1.0, 2.0, 6.0, 24.0, 120.0, 720.0], index=dates)
    assert_series_equal(result, expected, obj="Product window 1w")

    _rolling_1m_test(product, 'prod')


def test_std():
    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 7),
        date(2019, 1, 8),
    ]

    x = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)

    result = std(x)
    expected = pd.Series([np.nan, 0.707106, 0.577350, 0.957427, 0.894427, 1.673320], index=dates)
    assert_series_equal(result, expected, obj="std")

    result = std(x, Window(2, 0))
    expected = pd.Series([np.nan, 0.707106, 0.707106, 1.414214, 1.414214, 2.121320], index=dates)
    assert_series_equal(result, expected, obj="std window 2")

    result = std(x, Window('1w', 0))
    expected = pd.Series([np.nan, 0.707106, 0.577350, 0.957427, 0.894427, 1.870828], index=dates)
    assert_series_equal(result, expected, obj="std window 1w")

    assert std(pd.Series(dtype=float)).empty


def test_exponential_std():
    def exp_std_calc(ts, alpha=0.75):
        std = ts * 0
        for i in range(1, len(ts)):
            weights = (1 - alpha) * alpha ** np.arange(i, -1, -1)
            weights[0] /= (1 - alpha)
            x = ts.to_numpy()[:i + 1]
            ema = sum(weights * x) / sum(weights)
            debias_fact = sum(weights) ** 2 / (sum(weights) ** 2 - sum(weights ** 2))
            var = debias_fact * sum(weights * (x - ema) ** 2) / sum(weights)
            std.iat[i] = np.sqrt(var)
        std.iat[0] = np.NaN
        return std

    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 7),
        date(2019, 1, 8),
    ]

    x = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)

    result = exponential_std(x)
    expected = exp_std_calc(x)
    assert_series_equal(result, expected, obj="Exponentially weighted standard deviation")

    result = exponential_std(x, 0.8)
    expected = exp_std_calc(x, 0.8)
    assert_series_equal(result, expected, obj="Exponentially weighted standard deviation weight 1")


def test_var():
    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 7),
        date(2019, 1, 8),
    ]

    x = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)

    result = var(x)
    expected = pd.Series([np.nan, 0.500000, 0.333333, 0.916667, 0.800000, 2.800000], index=dates)
    assert_series_equal(result, expected, obj="var")

    result = var(x, Window(2, 0))
    expected = pd.Series([np.nan, 0.5, 0.5, 2.0, 2.0, 4.5], index=dates)
    assert_series_equal(result, expected, obj="var window 2")

    result = var(x, Window('1w', 0))
    expected = pd.Series([np.nan, 0.500000, 0.333333, 0.916666, 0.800000, 3.500000], index=dates)
    assert_series_equal(result, expected, obj="var window 1w")

    _rolling_1m_test(var, 'var')


def test_cov():
    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 7),
        date(2019, 1, 8),
    ]

    x = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)
    y = pd.Series([3.5, 1.8, 2.9, 1.2, 3.1, 5.9], index=dates)

    result = cov(x, y)
    expected = pd.Series([np.nan, 0.850000, 0.466667, 0.950000, 0.825000, 2.700000], index=dates)
    assert_series_equal(result, expected, obj="cov")

    result = cov(x, y, Window(2, 0))
    expected = pd.Series([np.nan, 0.850000, 0.549999, 1.7000000, 1.900000, 4.200000], index=dates)
    assert_series_equal(result, expected, obj="cov window 2")

    result = cov(x, y, Window('1w', 0))
    expected = pd.Series([np.nan, 0.850000, 0.466667, 0.950000, 0.825000, 3.375000], index=dates)
    assert_series_equal(result, expected, obj="cov window 1w")


def test_zscores():
    with pytest.raises(MqValueError):
        zscores(pd.Series(range(5)), "2d")

    assert_series_equal(zscores(pd.Series(dtype=float)), pd.Series(dtype=float))
    assert_series_equal(zscores(pd.Series(dtype=float), 1), pd.Series(dtype=float))

    assert_series_equal(zscores(pd.Series([1])), pd.Series([0.0]))
    assert_series_equal(zscores(pd.Series([1]), Window(1, 0)), pd.Series([0.0]))

    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 7),
        date(2019, 1, 8),
    ]

    x = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)

    result = zscores(x)
    expected = pd.Series([0.000000, -0.597614, 0.000000, -1.195229, 0.000000, 1.792843], index=dates)
    assert_series_equal(result, expected, obj="z-score")

    assert_series_equal(result, (x - x.mean()) / x.std(), obj="full series zscore")

    result = zscores(x, Window(2, 0))
    expected = pd.Series([0.0, -0.707107, 0.707107, -0.707107, 0.707107, 0.707107], index=dates)
    assert_series_equal(result, expected, obj="z-score window 2")
    assert_series_equal(zscores(x, Window(5, 5)), zscores(x, 5))

    result = zscores(x, Window('1w', 0))
    expected = pd.Series([0.0, -0.707106, 0.577350, -1.305582, 0.670820, 1.603567], index=dates)
    assert_series_equal(result, expected, obj="z-score window 1w")

    result = zscores(x, '1w')
    expected = pd.Series([1.603567], index=dates[-1:])
    assert_series_equal(result, expected, obj='z-score window string 1w')

    result = zscores(x, '1m')
    expected = pd.Series(dtype=float, index=[])
    assert_series_equal(result, expected, obj="z-score window too large")


def test_winsorize():
    assert_series_equal(winsorize(pd.Series(dtype=float)), pd.Series(dtype=float))

    x = generate_series(10000)
    # You must use absolute returns here, generate_series uses random absolute returns and as such has a decent chance
    # of going negative on a sample of 10k, if it goes negative the relative return will be garbage and test can fail
    r = returns(x, type=Returns.ABSOLUTE)

    for limit in [1.0, 2.0]:
        mu = r.mean()
        sigma = r.std()

        b_upper = mu + sigma * limit * 1.001
        b_lower = mu - sigma * limit * 1.001

        assert (True in r.ge(b_upper).values)
        assert (True in r.le(b_lower).values)

        wr = winsorize(r, limit)

        assert (True not in wr.ge(b_upper).values)
        assert (True not in wr.le(b_lower).values)


def test_percentiles():
    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 7),
        date(2019, 1, 8),
    ]

    x = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)
    y = pd.Series([3.5, 1.8, 2.9, 1.2, 3.1, 6.0], index=dates)
    y_with_mismatched_index = pd.Series([3.5, 1.8, 2.9, 1.2, 3.1], index=dates[:-1])

    assert_series_equal(percentiles(pd.Series(dtype=float), y), pd.Series(dtype=float))
    assert_series_equal(percentiles(x, pd.Series(dtype=float)), pd.Series(dtype=float))
    assert_series_equal(percentiles(x, y, Window(7, 0)), pd.Series(dtype=float))

    result = percentiles(x, y, 2)
    expected = pd.Series([50.0, 50.0, 100.0, 75.0], index=dates[2:])
    assert_series_equal(result, expected, obj="percentiles with window length 2")

    result = percentiles(x, y, Window(2, 0))
    expected = pd.Series([100.0, 0.0, 50.0, 50.0, 100.0, 75.0], index=dates)
    assert_series_equal(result, expected, obj="percentiles with window 2 and ramp 0")

    result = percentiles(x, y_with_mismatched_index, Window(2, 0))
    expected = pd.Series([100.0, 0.0, 50.0, 50.0, 100.0], index=dates[:-1])
    assert_series_equal(result, expected, obj="percentiles with mismatched y index")

    result = percentiles(x, y, Window('1w', 0))
    expected = pd.Series([100.0, 0.0, 33.333333, 25.0, 100.0, 90.0], index=dates)
    assert_series_equal(result, expected, obj="percentiles with window 1w")

    result = percentiles(x, y, Window('1w', '3d'))
    expected = pd.Series([25.0, 100.0, 90.0], index=dates[3:])
    assert_series_equal(result, expected, obj="percentiles with window 1w and ramp 3d")

    result = percentiles(x, y, Window(5, '3d'))
    expected = pd.Series([25.0, 100.0, 90.0], index=dates[3:])
    assert_series_equal(result, expected, obj="percentiles with window 5 and ramp 3d")

    result = percentiles(x)
    expected = pd.Series([50.0, 25.0, 66.667, 12.500, 70.0, 91.667], index=dates)
    assert_series_equal(result, expected, obj="percentiles over historical values")

    result = percentiles(x, y)
    expected = pd.Series([100.0, 0.0, 33.333, 25.0, 100.0, 91.667], index=dates)
    assert_series_equal(result, expected, obj="percentiles without window length", rtol=1e-3)

    with pytest.raises(ValueError):
        percentiles(x, pd.Series(dtype=float), Window(6, 1))


def test_percentile():
    with pytest.raises(MqError):
        percentile(pd.Series(dtype=float), -1)
    with pytest.raises(MqError):
        percentile(pd.Series(dtype=float), 100.1)
    with pytest.raises(MqTypeError):
        percentile(pd.Series(range(5), index=range(5)), 90, "2d")

    for n in range(0, 101, 5):
        assert percentile(pd.Series(x * 10 for x in range(0, 11)), n) == n

    x = percentile(pd.Series(x for x in range(0, 5)), 50, 2)
    assert_series_equal(x, pd.Series([1.5, 2.5, 3.5], index=pd.RangeIndex(2, 5)))

    x = percentile(pd.Series(dtype=float), 90, "1d")
    assert_series_equal(x, pd.Series(dtype=float), obj="Percentile with empty series")


def test_percentile_str():
    today = datetime.datetime.now()
    days = pd.date_range(today, periods=12, freq='D')
    start = pd.Series([29, 56, 82, 13, 35, 53, 25, 23, 21, 12, 15, 9], index=days)
    actual = percentile(start, 2, '10d')
    expected = pd.Series([12.18, 9.54], index=pd.date_range(today + datetime.timedelta(days=10), periods=2, freq='D'))
    assert_series_equal(actual, expected)

    actual = percentile(start, 50, '1w')
    expected = percentile(start, 50, 7)
    assert_series_equal(actual, expected)


def test_regression():
    x1 = pd.Series([0.0, 1.0, 4.0, 9.0, 16.0, 25.0, np.nan], index=pd.date_range('2019-1-1', periods=7), name='x1')
    x2 = pd.Series([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0], index=pd.date_range('2019-1-1', periods=8))
    y = pd.Series([10.0, 14.0, 20.0, 28.0, 38.0, 50.0, 60.0], index=pd.date_range('2019-1-1', periods=7))

    with pytest.raises(MqTypeError):
        LinearRegression([x1, x2], y, 1)

    regression = LinearRegression([x1, x2], y, True)

    np.testing.assert_almost_equal(regression.coefficient(0), 10.0)
    np.testing.assert_almost_equal(regression.coefficient(1), 1.0)
    np.testing.assert_almost_equal(regression.coefficient(2), 3.0)

    np.testing.assert_almost_equal(regression.r_squared(), 1.0)

    expected = pd.Series([10.0, 14.0, 20.0, 28.0, 38.0, 50.0], index=pd.date_range('2019-1-1', periods=6))
    assert_series_equal(regression.fitted_values(), expected)

    dates_predict = [date(2019, 2, 1), date(2019, 2, 2)]
    predicted = regression.predict([pd.Series([2.0, 3.0], index=dates_predict),
                                    pd.Series([6.0, 7.0], index=dates_predict)])
    expected = pd.Series([30.0, 34.0], index=dates_predict)
    assert_series_equal(predicted, expected)

    np.testing.assert_almost_equal(regression.standard_deviation_of_errors(), 0)


def test_rolling_linear_regression():
    x1 = pd.Series([0.0, 1.0, 4.0, 9.0, 16.0, 25.0, np.nan], index=pd.date_range('2019-1-1', periods=7), name='x1')
    x2 = pd.Series([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0], index=pd.date_range('2019-1-1', periods=8))
    y = pd.Series([10.0, 14.0, 20.0, 28.0, 28.0, 40.0, 60.0], index=pd.date_range('2019-1-1', periods=7))

    with pytest.raises(MqValueError):
        RollingLinearRegression([x1, x2], y, 3, True)

    with pytest.raises(MqTypeError):
        RollingLinearRegression([x1, x2], y, 4, 1)

    regression = RollingLinearRegression([x1, x2], y, 4, True)

    expected = pd.Series([np.nan, np.nan, np.nan, 10.0, 2.5, 19.0], index=pd.date_range('2019-1-1', periods=6))
    assert_series_equal(regression.coefficient(0), expected, check_names=False)

    expected = pd.Series([np.nan, np.nan, np.nan, 1.0, -1.5, 1.0], index=pd.date_range('2019-1-1', periods=6))
    assert_series_equal(regression.coefficient(1), expected, check_names=False)

    expected = pd.Series([np.nan, np.nan, np.nan, 3.0, 12.5, -1.0], index=pd.date_range('2019-1-1', periods=6))
    assert_series_equal(regression.coefficient(2), expected, check_names=False)

    expected = pd.Series([np.nan, np.nan, np.nan, 1.0, 0.964029, 0.901961], index=pd.date_range('2019-1-1', periods=6))
    assert_series_equal(regression.r_squared(), expected, check_names=False)

    expected = pd.Series([np.nan, np.nan, np.nan, 28.0, 28.5, 39.0], index=pd.date_range('2019-1-1', periods=6))
    assert_series_equal(regression.fitted_values(), expected, check_names=False)

    expected = pd.Series([np.nan, np.nan, np.nan, 0.0, 2.236068, 4.472136], index=pd.date_range('2019-1-1', periods=6))
    assert_series_equal(regression.standard_deviation_of_errors(), expected, check_names=False)

def test_si_model():
    n = 1000
    d = 100
    i0 = 100
    s0 = n - i0  
    beta = 0.5

    t = np.linspace(0, d, d)

    def deriv(y, t_loc, n_loc, beta_loc):
        s, i = y
        dsdt = -beta_loc * s * i / n_loc
        didt = beta_loc * s * i / n_loc

        return dsdt, didt

    def get_series(beta_loc):
        # Initial conditions vector
        y0 = s0, i0
        # Integrate the SI equations over the time grid, t.
        ret = odeint(deriv, y0, t, args=(n, beta_loc))
        s, i = ret.T

        dr = pd.date_range(dt.date.today(), dt.date.today() + dt.timedelta(days=d - 1))
        return pd.Series(s, dr), pd.Series(i, dr)

    # Test 'mass action' incidence
    (s, i) = get_series(beta)
    si_mass_action = SIModel(beta, s, i, n, incidence_type='mass_action')

    assert abs(si_mass_action.beta() - beta) < 0.01

    beta = 0.4

    (s, i) = get_series(beta)

    s_predict_mass_action = si_mass_action.predict_s()
    i_predic_mass_action = si_mass_action.predict_i()

    assert s_predict_mass_action.size == d
    assert i_predic_mass_action.size == d

    # Test 'standard' incidence
    (s, i) = get_series(beta)
    si_standard = SIModel(beta, s, i, n, incidence_type='standard')

    assert abs(si_standard.beta() - beta) < 0.01

    beta = 0.4

    (s, i) = get_series(beta)

    s_predict_standard = si_standard.predict_s()
    i_predic_standard = si_standard.predict_i()

    assert s_predict_standard.size == d
    assert i_predic_standard.size == d

    # Test for type error in fit parameter
    with pytest.raises(MqTypeError):
        SIModel(beta, s, i, n, fit=0)

    si_standard_no_fit = SIModel(beta, s, i, n, fit=False, incidence_type='standard')

    assert si_standard_no_fit.beta() == beta

    si1 = SIModel(beta, s, i, n, fit=False, incidence_type='standard')

    with DataContext(end=dt.date.today() + dt.timedelta(days=d - 1)):
        si2 = SIModel(beta, s.iloc[0], i, n, fit=False, incidence_type='standard')

    assert si1.beta() == si1.beta()
    assert (si1.predict_i() == si2.predict_i()).all()
    assert (si1.predict_s() == si2.predict_s()).all()

    # Additional checks for mass action and standard
    assert not (si_mass_action.predict_i() == si_standard.predict_i()).all()
    assert not (si_mass_action.predict_s() == si_standard.predict_s()).all()

def test_sir_model():
    n = 1000
    d = 100
    i0 = 100
    r0 = 0
    s0 = n
    beta = 0.5
    gamma = 0.25

    t = np.linspace(0, d, d)

    def deriv(y, t_loc, n_loc, beta_loc, gamma_loc):
        s, i, r = y
        dsdt = -beta_loc * s * i / n_loc
        didt = beta_loc * s * i / n_loc - gamma_loc * i
        drdt = gamma_loc * i

        return dsdt, didt, drdt

    def get_series(beta_loc, gamma_loc):
        # Initial conditions vector
        y0 = s0, i0, r0
        # Integrate the SIR equations over the time grid, t.
        ret = odeint(deriv, y0, t, args=(n, beta_loc, gamma_loc))
        s, i, r = ret.T

        dr = pd.date_range(dt.date.today(), dt.date.today() + dt.timedelta(days=d - 1))
        return pd.Series(s, dr), pd.Series(i, dr), pd.Series(r, dr)

    (s, i, r) = get_series(beta, gamma)

    sir = SIRModel(beta, gamma, s, i, r, n)

    assert abs(sir.beta() - beta) < 0.01
    assert abs(sir.gamma() - gamma) < 0.01

    beta = 0.4
    gamma = 0.25

    (s, i, r) = get_series(0.4, 0.25)

    s_predict = sir.predict_s()
    i_predict = sir.predict_i()
    r_predict = sir.predict_r()

    assert s_predict.size == d
    assert i_predict.size == d
    assert r_predict.size == d

    with pytest.raises(MqTypeError):
        SIRModel(beta, gamma, s, i, r, n, fit=0)

    sir = SIRModel(beta, gamma, s, i, r, n, fit=False)

    assert sir.beta() == beta
    assert sir.gamma() == gamma

    sir1 = SIRModel(beta, gamma, s, i, r, n, fit=False)

    with DataContext(end=dt.date.today() + dt.timedelta(days=d - 1)):
        sir2 = SIRModel(beta, gamma, s.iloc[0], i, r.iloc[0], n, fit=False)

    assert sir1.beta() == sir1.beta()
    assert sir2.gamma() == sir2.gamma()
    assert (sir1.predict_i() == sir2.predict_i()).all()
    assert (sir1.predict_r() == sir2.predict_r()).all()
    assert (sir1.predict_s() == sir2.predict_s()).all()


def test_seir_model():
    n = 1000
    d = 100
    e0 = 1
    i0 = 1
    r0 = 0
    s0 = n
    beta = 0.5
    gamma = 0.2
    sigma = 1

    t = np.linspace(0, d, d)

    def deriv(y, t_loc, n_loc, beta_loc, gamma_loc, sigma_loc):
        s, e, i, r = y
        dsdt = -beta_loc * s * i / n_loc
        dedt = beta_loc * s * i / n_loc - sigma_loc * e
        didt = sigma_loc * e - gamma * i
        drdt = gamma_loc * i

        return dsdt, dedt, didt, drdt

    def get_series(beta_loc, gamma_loc, sigma_loc):
        # Initial conditions vector
        y0 = s0, e0, i0, r0
        # Integrate the SEIR equations over the time grid, t.
        ret = odeint(deriv, y0, t, args=(n, beta_loc, gamma_loc, sigma_loc))
        s, e, i, r = ret.T

        dr = pd.date_range(dt.date.today(), dt.date.today() + dt.timedelta(days=d - 1))
        return pd.Series(s, dr), pd.Series(e, dr), pd.Series(i, dr), pd.Series(r, dr)

    (s, e, i, r) = get_series(beta, gamma, sigma)

    seir = SEIRModel(beta, gamma, sigma, s, e, i, r, n)

    assert abs(seir.beta() - beta) < 0.01
    assert abs(seir.gamma() - gamma) < 0.01
    assert abs(seir.sigma() - sigma) < 0.01

    s_predict = seir.predict_s()
    e_predict = seir.predict_e()
    i_predict = seir.predict_i()
    r_predict = seir.predict_i()

    assert s_predict.size == d
    assert e_predict.size == d
    assert i_predict.size == d
    assert r_predict.size == d

    with pytest.raises(MqTypeError):
        SEIRModel(beta, gamma, sigma, s, e, i, r, n, fit=0)

    seir = SEIRModel(beta, gamma, sigma, s, e, i, r, n, fit=False)

    assert seir.beta() == beta
    assert seir.gamma() == gamma
    assert seir.sigma() == sigma

    seir1 = SEIRModel(beta, gamma, sigma, s, e, i, r, n, fit=False)

    with DataContext(end=dt.date.today() + dt.timedelta(days=d - 1)):
        seir2 = SEIRModel(beta, gamma, sigma, s.iloc[0], e.iloc[0], i, r.iloc[0], n, fit=False)

    assert seir1.beta() == seir1.beta()
    assert seir2.gamma() == seir2.gamma()
    assert seir2.sigma() == seir2.sigma()
    assert (seir1.predict_i() == seir2.predict_i()).all()
    assert (seir1.predict_e() == seir2.predict_e()).all()
    assert (seir1.predict_r() == seir2.predict_r()).all()
    assert (seir1.predict_s() == seir2.predict_s()).all()


if __name__ == "__main__":
    pytest.main(args=["test_statistics.py"])
