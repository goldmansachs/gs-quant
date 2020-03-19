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
from datetime import date

import pytest
from pandas.util.testing import assert_series_equal

from gs_quant.timeseries import *


def test_generate_series():

    x = generate_series(100)

    assert(len(x) == 100)
    assert(x.index[0] == datetime.date.today())
    assert(x[0] == 100)


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
    assert_series_equal(result, expected, obj="std", check_less_precise=True)

    result = std(x, Window(2, 0))
    expected = pd.Series([np.nan, 0.707106, 0.707106, 1.414214, 1.414214, 2.121320], index=dates)
    assert_series_equal(result, expected, obj="std window 2", check_less_precise=True)

    result = std(x, Window('1w', 0))
    expected = pd.Series([np.nan, 0.707106, 0.577350, 0.957427, 0.894427, 1.870828], index=dates)
    assert_series_equal(result, expected, obj="std window 1w", check_less_precise=True)


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
    assert_series_equal(result, expected, obj="var", check_less_precise=True)

    result = var(x, Window(2, 0))
    expected = pd.Series([np.nan, 0.5, 0.5, 2.0, 2.0, 4.5], index=dates)
    assert_series_equal(result, expected, obj="var window 2", check_less_precise=True)

    result = var(x, Window('1w', 0))
    expected = pd.Series([np.nan, 0.500000, 0.333333, 0.916666, 0.800000, 3.500000], index=dates)
    assert_series_equal(result, expected, obj="var window 1w", check_less_precise=True)


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
    assert_series_equal(result, expected, obj="cov", check_less_precise=True)

    result = cov(x, y, Window(2, 0))
    expected = pd.Series([np.nan, 0.850000, 0.549999, 1.7000000, 1.900000, 4.200000], index=dates)
    assert_series_equal(result, expected, obj="cov window 2", check_less_precise=True)

    result = cov(x, y, Window('1w', 0))
    expected = pd.Series([np.nan, 0.850000, 0.466667, 0.950000, 0.825000, 3.375000], index=dates)
    assert_series_equal(result, expected, obj="cov window 1w", check_less_precise=True)


def test_zscores():

    assert_series_equal(zscores(pd.Series()), pd.Series())
    assert_series_equal(zscores(pd.Series(), 1), pd.Series())

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
    assert_series_equal(result, expected, obj="z-score", check_less_precise=True)

    assert_series_equal(result, (x - x.mean()) / x.std(), obj="full series zscore")

    result = zscores(x, Window(2, 0))
    expected = pd.Series([0.0, -0.707107, 0.707107, -0.707107, 0.707107, 0.707107], index=dates)
    assert_series_equal(result, expected, obj="z-score window 2", check_less_precise=True)
    assert_series_equal(zscores(x, Window(5, 5)), zscores(x, 5))

    result = zscores(x, Window('1w', 0))
    expected = pd.Series([0.0, -0.707106, 0.577350, -1.305582, 0.670820, 1.603567], index=dates)
    assert_series_equal(result, expected, obj="z-score window 1w", check_less_precise=True)


def test_winsorize():

    assert_series_equal(winsorize(pd.Series()), pd.Series())

    x = generate_series(10000)
    r = returns(x)

    limit = 1.0

    mu = r.mean()
    sigma = r.std()

    b_upper = mu + sigma * limit * 1.001
    b_lower = mu - sigma * limit * 1.001

    assert(True in r.ge(b_upper).values)
    assert(True in r.le(b_lower).values)

    wr = winsorize(r, limit)

    assert(True not in wr.ge(b_upper).values)
    assert(True not in wr.le(b_lower).values)

    limit = 2.0

    mu = r.mean()
    sigma = r.std()

    b_upper = mu + sigma * limit * 1.001
    b_lower = mu - sigma * limit * 1.001

    assert(True in r.ge(b_upper).values)
    assert(True in r.le(b_lower).values)

    wr = winsorize(r, limit)

    assert(True not in wr.ge(b_upper).values)
    assert(True not in wr.le(b_lower).values)


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

    assert_series_equal(percentiles(pd.Series([]), y), pd.Series([]))
    assert_series_equal(percentiles(x, pd.Series([])), pd.Series([]))
    assert_series_equal(percentiles(x, y, Window(7, 0)), pd.Series([]))

    result = percentiles(x, y, 2)
    expected = pd.Series([50.0, 50.0, 100.0, 75.0], index=dates[2:])
    assert_series_equal(result, expected, obj="percentiles with window length 2")

    result = percentiles(x, y, Window(2, 0))
    expected = pd.Series([100.0, 0.0, 50.0, 50.0, 100.0, 75.0], index=dates)
    assert_series_equal(result, expected, obj="percentiles with window 2 and ramp 0")

    result = percentiles(x, y, Window('1w', 0))
    expected = pd.Series([100.0, 0.0, 33.333333, 25.0, 100.0, 90.0], index=dates)
    assert_series_equal(result, expected, obj="percentiles with window 1w")

    result = percentiles(x)
    expected = pd.Series([50.0, 25.0, 66.667, 12.500, 70.0, 91.667], index=dates)
    assert_series_equal(result, expected, obj="percentiles over historical values", check_less_precise=True)

    result = percentiles(x, y)
    expected = pd.Series([100.0, 0.0, 33.333, 25.0, 100.0, 91.667], index=dates)
    assert_series_equal(result, expected, obj="percentiles without window length", check_less_precise=True)


def test_regression():
    dates = pd.date_range('2019-1-1', periods=6)
    x1 = pd.Series([0.0, 1.0, 4.0, 9.0, 16.0, 25.0], index=dates)
    x2 = pd.Series([0.0, 1.0, 2.0, 3.0, 4.0, 5.0], index=dates)
    y = pd.Series([10.0, 14.0, 20.0, 28.0, 38.0, 50.0], index=dates)

    regression = LinearRegression([x1, x2], y, True)

    np.testing.assert_almost_equal(regression.coefficient(0), 10.0)
    np.testing.assert_almost_equal(regression.coefficient(1), 1.0)
    np.testing.assert_almost_equal(regression.coefficient(2), 3.0)

    with pytest.raises(ValueError):
        regression.coefficient(3)

    np.testing.assert_almost_equal(regression.r_squared(), 1.0)

    assert_series_equal(regression.fitted_values(), y)

    dates_predict = [date(2019, 2, 1), date(2019, 2, 2)]
    predicted = regression.predict([pd.Series([2.0, 3.0], index=dates_predict),
                                    pd.Series([6.0, 7.0], index=dates_predict)])
    expected = pd.Series([30.0, 34.0], index=dates_predict)
    assert_series_equal(predicted, expected)


if __name__ == "__main__":
    pytest.main(args=["test_statistics.py"])
