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

import pandas as pd
import pytest
from pandas.util.testing import assert_series_equal
from ..timeseries.datetime import *
from datetime import date


def test_align():

    dates1 = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 5),
    ]

    dates2 = [
        date(2019, 1, 2),
        date(2019, 1, 4),
        date(2019, 1, 6),
    ]

    x = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0], index=dates1)
    y = pd.Series([20.0, 40.0, 60.0], index=dates2)

    expectedl = pd.Series([2.0, 4.0], index=[date(2019, 1, 2), date(2019, 1, 4)])
    expectedr = pd.Series([20.0, 40.0], index=[date(2019, 1, 2), date(2019, 1, 4)])

    result = align(x, y, Interpolate.INTERSECT)
    assert_series_equal(result[0], expectedl, obj="Align intersect left")
    assert_series_equal(result[1], expectedr, obj="Align intersect left")

    result = align(y, x, Interpolate.INTERSECT)
    assert_series_equal(result[0], expectedr, obj="Align intersect right")
    assert_series_equal(result[1], expectedl, obj="Align intersect right")

    union_dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 5),
        date(2019, 1, 6),
    ]

    expected1 = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0, np.nan], index=union_dates)
    expected2 = pd.Series([np.nan, 20.0, np.nan, 40.0, np.nan, 60.0], index=union_dates)

    result = align(x, y, Interpolate.NAN)
    assert_series_equal(result[0], expected1, obj="Align NaN left")
    assert_series_equal(result[1], expected2, obj="Align NaN left")

    result = align(y, x, Interpolate.NAN)
    assert_series_equal(result[0], expected2, obj="Align NaN right")
    assert_series_equal(result[1], expected1, obj="Align NaN right")

    expected1 = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0, 0.0], index=union_dates)
    expected2 = pd.Series([0.0, 20.0, 0.0, 40.0, 0.0, 60.0], index=union_dates)

    result = align(x, y, Interpolate.ZERO)
    assert_series_equal(result[0], expected1, obj="Align zero left")
    assert_series_equal(result[1], expected2, obj="Align zero left")

    result = align(y, x, Interpolate.ZERO)
    assert_series_equal(result[0], expected2, obj="Align zero right")
    assert_series_equal(result[1], expected1, obj="Align zero right")

    expected1 = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0, 5.0], index=union_dates)
    expected2 = pd.Series([20.0, 20.0, 20.0, 40.0, 40.0, 60.0], index=union_dates)

    result = align(x, y, Interpolate.STEP)
    assert_series_equal(result[0], expected1, obj="Align step left")
    assert_series_equal(result[1], expected2, obj="Align step left")

    result = align(y, x, Interpolate.STEP)
    assert_series_equal(result[0], expected2, obj="Align step left")
    assert_series_equal(result[1], expected1, obj="Align step left")

    with pytest.raises(MqValueError):
        align(x, x, "None")


def test_interpolate():

    dates = [
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 5),
        date(2019, 1, 7),
    ]

    x = pd.Series([2.0, 3.0, 5.0, 7.0], index=dates)

    result = interpolate(x, dates)
    assert_series_equal(result, x, obj="Interpolate series by dates")

    result = interpolate(x, x)
    assert_series_equal(result, x, obj="Interpolate series by series dates")

    result = interpolate(x)
    assert_series_equal(result, x, obj="Interpolate series default")

    select_dates = [
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 7),
    ]

    result = interpolate(x, select_dates)
    expected = pd.Series([2.0, 3.0, 7.0], index=select_dates)
    assert_series_equal(result, expected, obj="Interpolate subset of dates")

    select_dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 4),
        date(2019, 1, 5),
        date(2019, 1, 6),
        date(2019, 1, 7),
        date(2019, 1, 8),
    ]

    intersect_dates = [
        date(2019, 1, 2),
        date(2019, 1, 5),
        date(2019, 1, 7),
    ]

    result = interpolate(x, select_dates, Interpolate.INTERSECT)
    expected = pd.Series([2.0, 5.0, 7.0], index=intersect_dates)
    assert_series_equal(result, expected, obj="Interpolate intersect")

    result = interpolate(x, select_dates, Interpolate.NAN)
    expected = pd.Series([np.nan, 2.0, np.nan, 5.0, np.nan, 7.0, np.nan], index=select_dates)
    assert_series_equal(result, expected, obj="Interpolate nan")

    result = interpolate(x, select_dates, Interpolate.ZERO)
    expected = pd.Series([0.0, 2.0, 0.0, 5.0, 0.0, 7.0, 0.0], index=select_dates)
    assert_series_equal(result, expected, obj="Interpolate zero")

    result = interpolate(x, select_dates, Interpolate.STEP)
    expected = pd.Series([2.0, 2.0, 2.0, 5.0, 5.0, 7.0, 7.0], index=select_dates)
    assert_series_equal(result, expected, obj="Interpolate step dates")

    result = interpolate(x, pd.Series(np.nan, select_dates), Interpolate.STEP)
    expected = pd.Series([2.0, 2.0, 2.0, 5.0, 5.0, 7.0, 7.0], index=select_dates)
    assert_series_equal(result, expected, obj="Interpolate step series")

    xnan = pd.Series([np.nan, 3.0, 5.0, 7.0], index=dates)

    result = interpolate(xnan, select_dates, Interpolate.STEP)
    expected = pd.Series([np.nan, np.nan, np.nan, 5.0, 5.0, 7.0, 7.0], index=select_dates)
    assert_series_equal(result, expected, obj="Interpolate flat nan start")

    with pytest.raises(MqValueError):
        interpolate(x, x, "None")
