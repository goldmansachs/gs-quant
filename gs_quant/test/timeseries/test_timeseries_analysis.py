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
import numpy as np
from gs_quant.timeseries import *
from datetime import date


def test_first():

    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
    ]

    x = pd.Series([1.0, 2.0, 3.0, 4.0], index=dates)

    result = first(x)
    expected = pd.Series([1.0, 1.0, 1.0, 1.0], index=dates)
    assert_series_equal(result, expected, obj="First")


def test_last():

    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
    ]

    x = pd.Series([1.0, 2.0, 3.0, 4.0], index=dates)

    result = last(x)
    expected = pd.Series([4.0, 4.0, 4.0, 4.0], index=dates)
    assert_series_equal(result, expected, obj="First")


def test_count():

    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
    ]

    x = pd.Series([1.0, 2.0, 3.0, 4.0], index=dates)

    result = count(x)
    expected = pd.Series([1.0, 2.0, 3.0, 4.0], index=dates)
    assert_series_equal(result, expected, obj="Count")


def test_diff():

    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
    ]

    x = pd.Series([1.0, 2.0, 3.0, 4.0], index=dates)

    result = diff(x)
    expected = pd.Series([np.nan, 1.0, 1.0, 1.0], index=dates)
    assert_series_equal(result, expected, obj="Diff")

    result = diff(x, 2)
    expected = pd.Series([np.nan, np.nan, 2.0, 2.0], index=dates)
    assert_series_equal(result, expected, obj="Diff")

    empty = pd.Series([], index=[])
    result = diff(empty)
    assert(len(result) == 0 )



def test_lag():

    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
    ]

    x = pd.Series([1.0, 2.0, 3.0, 4.0], index=dates)

    result = lag(x)
    expected = pd.Series([np.nan, 1.0, 2.0, 3.0], index=dates)
    assert_series_equal(result, expected, obj="Lag")

    result = lag(x, 2)
    expected = pd.Series([np.nan, np.nan, 1.0, 2.0], index=dates)
    assert_series_equal(result, expected, obj="Lag 2")
