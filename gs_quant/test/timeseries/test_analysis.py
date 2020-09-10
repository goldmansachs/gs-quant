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


def test_last_value():
    with pytest.raises(MqValueError):
        last_value(pd.Series())

    x = pd.Series([1.0, 2.0, 3.0, 4.0], index=(pd.date_range("2020-01-01", periods=4, freq="D")))
    assert last_value(x) == 4.0

    y = pd.Series([5])
    assert last_value(y) == 5


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
    assert(len(result) == 0)


def test_lag():
    dates = pd.date_range("2019-01-01", periods=4, freq="D")
    x = pd.Series([1.0, 2.0, 3.0, 4.0], index=dates)

    result = lag(x, '1m')
    expected = pd.Series([1.0, 2.0, 3.0, 4.0], index=pd.date_range("2019-01-31", periods=4, freq="D"))
    assert_series_equal(result, expected, obj="Lag 1m")

    result = lag(x, '2d', LagMode.TRUNCATE)
    expected = pd.Series([1.0, 2.0], index=pd.date_range("2019-01-03", periods=2, freq="D"))
    assert_series_equal(result, expected, obj="Lag 2d truncate")

    result = lag(x, mode=LagMode.TRUNCATE)
    expected = pd.Series([np.nan, 1.0, 2.0, 3.0], index=dates)
    assert_series_equal(result, expected, obj="Lag")

    result = lag(x, 2, LagMode.TRUNCATE)
    expected = pd.Series([np.nan, np.nan, 1.0, 2.0], index=dates)
    assert_series_equal(result, expected, obj="Lag 2")

    result = lag(x, 2, LagMode.EXTEND)
    expected = pd.Series([np.nan, np.nan, 1.0, 2.0, 3.0, 4.0], index=pd.date_range("2019-01-01", periods=6, freq="D"))
    assert_series_equal(result, expected, obj="Lag 2 Extend")

    result = lag(x, 2)
    expected = pd.Series([np.nan, np.nan, 1.0, 2.0, 3.0, 4.0], index=pd.date_range("2019-01-01", periods=6, freq="D"))
    assert_series_equal(result, expected, obj="Lag 2 Extend")

    y = pd.Series([0] * 4, index=pd.date_range('2020-01-01T00:00:00Z', periods=4, freq='S'))
    with pytest.raises(Exception):
        lag(y, 5, LagMode.EXTEND)

    z = pd.Series([10, 11, 12], index=pd.date_range('2020-02-28', periods=3, freq='D'))
    result = lag(z, '2y')
    expected = pd.Series([10, 12], index=pd.date_range('2022-02-28', periods=2, freq='D'))
    assert_series_equal(result, expected, obj="Lag RDate 2y")
