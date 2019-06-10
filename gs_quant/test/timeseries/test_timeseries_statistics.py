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

from pandas.util.testing import assert_series_equal
from gs_quant.timeseries import *
from datetime import date


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
        date(2019, 1, 5),
        date(2019, 1, 6),
    ]

    x = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)

    result = min_(x)
    expected = pd.Series([3.0, 2.0, 2.0, 1.0, 1.0, 1.0], index=dates)
    assert_series_equal(result, expected, obj="Minimum")

    result = min_(x, 1)
    expected = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)
    assert_series_equal(result, expected, obj="Minimum window 1")

    result = min_(x, 2)
    expected = pd.Series([3.0, 2.0, 2.0, 1.0, 1.0, 3.0], index=dates)
    assert_series_equal(result, expected, obj="Minimum window 2")


def test_max():

    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 5),
        date(2019, 1, 6),
    ]

    x = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)

    result = max_(x)
    expected = pd.Series([3.0, 3.0, 3.0, 3.0, 3.0, 6.0], index=dates)
    assert_series_equal(result, expected, obj="Maximum")

    result = max_(x, 1)
    expected = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)
    assert_series_equal(result, expected, obj="Maximum window 1")

    result = max_(x, 2)
    expected = pd.Series([3.0, 3.0, 3.0, 3.0, 3.0, 6.0], index=dates)
    assert_series_equal(result, expected, obj="Maximum window 2")


def test_range():

    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 5),
        date(2019, 1, 6),
    ]

    x = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)

    result = range_(x)
    expected = pd.Series([0.0, 1.0, 1.0, 2.0, 2.0, 5.0], index=dates)
    assert_series_equal(result, expected, obj="Range")

    result = range_(x, 1)
    expected = pd.Series([0.0, 0.0, 0.0, 0.0, 0.0, 0.0], index=dates)
    assert_series_equal(result, expected, obj="Range window 1")

    result = range_(x, 2)
    expected = pd.Series([0.0, 1.0, 1.0, 2.0, 2.0, 3.0], index=dates)
    assert_series_equal(result, expected, obj="Range window 2")


def test_mean():

    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 5),
        date(2019, 1, 6),
    ]

    x = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)

    result = mean(x)
    expected = pd.Series([3.0, 2.5, 8/3, 2.25, 2.4, 3.0], index=dates)
    assert_series_equal(result, expected, obj="Mean")

    result = mean(x, 1)
    expected = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)
    assert_series_equal(result, expected, obj="Mean window 1")

    result = mean(x, 2)
    expected = pd.Series([3.0, 2.5, 2.5, 2.0, 2.0, 4.5], index=dates)
    assert_series_equal(result, expected, obj="Mean window 2")


def test_median():

    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 5),
        date(2019, 1, 6),
    ]

    x = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)

    result = median(x)
    expected = pd.Series([3.0, 2.5, 3.0, 2.5, 3.0, 3.0], index=dates)
    assert_series_equal(result, expected, obj="Median")

    result = median(x, 1)
    expected = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)
    assert_series_equal(result, expected, obj="Median window 1")

    result = median(x, 2)
    expected = pd.Series([3.0, 2.5, 2.5, 2.0, 2.0, 4.5], index=dates)
    assert_series_equal(result, expected, obj="Median window 2")


def test_mode():

    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 5),
        date(2019, 1, 6),
    ]

    x = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)

    result = mode(x)
    expected = pd.Series([3.0, 2.0, 3.0, 3.0, 3.0, 3.0], index=dates)
    assert_series_equal(result, expected, obj="mode")

    result = mode(x, 1)
    expected = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)
    assert_series_equal(result, expected, obj="mode window 1")

    result = mode(x, 2)
    expected = pd.Series([3.0, 2.0, 2.0, 1.0, 1.0, 3.0], index=dates)
    assert_series_equal(result, expected, obj="mode window 2")


def test_sum():

    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 5),
        date(2019, 1, 6),
    ]

    x = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], index=dates)

    result = sum_(x)
    expected = pd.Series([1.0, 3.0, 6.0, 10, 15, 21], index=dates)
    assert_series_equal(result, expected, obj="Summation")

    result = sum_(x, 2)
    expected = pd.Series([1.0, 3.0, 5.0, 7.0, 9.0, 11.0], index=dates)
    assert_series_equal(result, expected, obj="Summation")


def test_product():

    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 5),
        date(2019, 1, 6),
    ]

    x = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], index=dates)

    result = product(x)
    expected = pd.Series([1.0, 2.0, 6.0, 24, 120, 720], index=dates)
    assert_series_equal(result, expected, obj="Product")

    result = product(x, 2)
    expected = pd.Series([1.0, 2.0, 6.0, 12.0, 20.0, 30.0], index=dates)
    assert_series_equal(result, expected, obj="Product")


def test_std():

    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 5),
        date(2019, 1, 6),
    ]

    x = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)

    result = std(x)
    expected = pd.Series([np.nan, 0.707106, 0.577350, 0.957427, 0.894427, 1.673320], index=dates)
    assert_series_equal(result, expected, obj="std", check_less_precise=True)

    result = std(x, 2)
    expected = pd.Series([np.nan, 0.707106, 0.707106, 1.414214, 1.414214, 2.121320], index=dates)
    assert_series_equal(result, expected, obj="std window 2", check_less_precise=True)


def test_var():

    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 5),
        date(2019, 1, 6),
    ]

    x = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)

    result = var(x)
    expected = pd.Series([np.nan, 0.500000, 0.333333, 0.916667, 0.800000, 2.800000], index=dates)
    assert_series_equal(result, expected, obj="var", check_less_precise=True)

    result = var(x, 2)
    expected = pd.Series([np.nan, 0.5, 0.5, 2.0, 2.0, 4.5], index=dates)
    assert_series_equal(result, expected, obj="var window 2", check_less_precise=True)


def test_cov():

    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 5),
        date(2019, 1, 6),
    ]

    x = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)
    y = pd.Series([3.5, 1.8, 2.9, 1.2, 3.1, 5.9], index=dates)

    result = cov(x, y)
    expected = pd.Series([np.nan, 0.850000, 0.466667, 0.950000, 0.825000, 2.700000], index=dates)
    assert_series_equal(result, expected, obj="cov", check_less_precise=True)

    result = var(x, 2)
    expected = pd.Series([np.nan, 0.5, 0.5, 2.0, 2.0, 4.5], index=dates)
    assert_series_equal(result, expected, obj="var window 2", check_less_precise=True)


def test_zscores():

    assert_series_equal(zscores(pd.Series()), pd.Series())
    assert_series_equal(zscores(pd.Series(), 1), pd.Series())

    assert_series_equal(zscores(pd.Series([1])), pd.Series([0.0]))
    assert_series_equal(zscores(pd.Series([1]), 1), pd.Series([0.0]))

    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 5),
        date(2019, 1, 6),
    ]

    x = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)

    result = zscores(x)
    expected = pd.Series([0.000000, -0.597614, 0.000000, -1.195229, 0.000000, 1.792843], index=dates)
    assert_series_equal(result, expected, obj="z-score", check_less_precise=True)

    assert_series_equal(result, (x-x.mean()) / x.std(), obj="full series zscore")

    result = zscores(x, 2)
    expected = pd.Series([0.0, -0.707107, 0.707107, -0.707107, 0.707107, 0.707107], index=dates)
    assert_series_equal(result, expected, obj="z-score window 2", check_less_precise=True)


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


def test_percentile():
    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 5),
        date(2019, 1, 6),
    ]

    x = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)
    y = pd.Series([3.5, 1.8, 2.9, 1.2, 3.1, 6.0], index=dates)

    assert_series_equal(percentile(pd.Series(), y), pd.Series())
    assert_series_equal(percentile(x, pd.Series()), pd.Series())
    assert_series_equal(percentile(x, y, 7), pd.Series())

    result = percentile(x, y, 2)
    expected = pd.Series([0.0, 50.0, 50.0, 100.0, 75.0], index=dates[1:])
    assert_series_equal(result, expected, obj="percentile with window 2")

    result = percentile(x, y)
    expected = pd.Series([100.0, 0.0, 33.333, 25.0, 100.0, 91.667], index=dates)
    assert_series_equal(result, expected, obj="percentile without window length", check_less_precise=True)
