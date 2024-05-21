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


def test_add():
    dates1 = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
    ]

    dates2 = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
    ]

    x = pd.Series([1.0, 1.0, 1.0, 1.0], index=dates1)
    y = pd.Series([1.0, 1.0, 1.0], index=dates2)

    result = algebra.add(x, y, Interpolate.INTERSECT)
    expected = pd.Series([2.0, 2.0, 2.0], index=dates2)
    assert_series_equal(result, expected, obj="Add intersect left")

    result = algebra.add(y, x, Interpolate.INTERSECT)
    expected = pd.Series([2.0, 2.0, 2.0], index=dates2)
    assert_series_equal(result, expected, obj="Add intersect right")

    result = algebra.add(x, y, Interpolate.NAN)
    expected = pd.Series([2.0, 2.0, 2.0, np.nan], index=dates1)
    assert_series_equal(result, expected, obj="Add NaN left")

    result = algebra.add(y, x, Interpolate.NAN)
    expected = pd.Series([2.0, 2.0, 2.0, np.nan], index=dates1)
    assert_series_equal(result, expected, obj="Add NaN right")

    result = algebra.add(x, y, Interpolate.ZERO)
    expected = pd.Series([2.0, 2.0, 2.0, 1.0], index=dates1)
    assert_series_equal(result, expected, obj="Add zero left")

    result = algebra.add(x, y, Interpolate.STEP)
    expected = pd.Series([2.0, 2.0, 2.0, 2.0], index=dates1)
    assert_series_equal(result, expected, obj="Add step right")

    result = algebra.add(x, 1)
    expected = pd.Series([2.0, 2.0, 2.0, 2.0], index=dates1)
    assert_series_equal(result, expected, obj="Add scalar left")

    result = algebra.add(1, x)
    expected = pd.Series([2.0, 2.0, 2.0, 2.0], index=dates1)
    assert_series_equal(result, expected, obj="Add scalar right")

    assert algebra.add(1, 2) == 3


def test_subtract():
    dates1 = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
    ]

    dates2 = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
    ]

    x = pd.Series([1.0, 1.0, 1.0, 1.0], index=dates1)
    y = pd.Series([1.0, 1.0, 1.0], index=dates2)

    result = algebra.subtract(x, y, Interpolate.INTERSECT)
    expected = pd.Series([0.0, 0.0, 0.0], index=dates2)
    assert_series_equal(result, expected, obj="Subtract intersect left")

    result = algebra.subtract(y, x, Interpolate.INTERSECT)
    expected = pd.Series([0.0, 0.0, 0.0], index=dates2)
    assert_series_equal(result, expected, obj="Subtract intersect right")

    result = algebra.subtract(x, y, Interpolate.NAN)
    expected = pd.Series([0.0, 0.0, 0.0, np.nan], index=dates1)
    assert_series_equal(result, expected, obj="Subtract NaN left")

    result = algebra.subtract(y, x, Interpolate.NAN)
    expected = pd.Series([0.0, 0.0, 0.0, np.nan], index=dates1)
    assert_series_equal(result, expected, obj="Subtract NaN right")

    result = algebra.subtract(x, y, Interpolate.ZERO)
    expected = pd.Series([0.0, 0.0, 0.0, 1.0], index=dates1)
    assert_series_equal(result, expected, obj="Subtract zero left")

    result = algebra.subtract(x, y, Interpolate.STEP)
    expected = pd.Series([0.0, 0.0, 0.0, 0.0], index=dates1)
    assert_series_equal(result, expected, obj="Subtract step right")

    result = algebra.subtract(x, 1)
    expected = pd.Series([0.0, 0.0, 0.0, 0.0], index=dates1)
    assert_series_equal(result, expected, obj="Subtract scalar left")

    result = algebra.subtract(1, x)
    expected = pd.Series([0.0, 0.0, 0.0, 0.0], index=dates1)
    assert_series_equal(result, expected, obj="Subtract scalar right")

    assert algebra.subtract(1, 2) == -1


def test_multiply():
    dates1 = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
    ]

    dates2 = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
    ]

    x = pd.Series([1.0, 2.0, 3.0, 4.0], index=dates1)
    y = pd.Series([2.0, 1.5, 2.0], index=dates2)

    result = algebra.multiply(x, y, Interpolate.INTERSECT)
    expected = pd.Series([2.0, 3.0, 6.0], index=dates2)
    assert_series_equal(result, expected, obj="Multiply intersect left")

    result = algebra.multiply(y, x, Interpolate.INTERSECT)
    expected = pd.Series([2.0, 3.0, 6.0], index=dates2)
    assert_series_equal(result, expected, obj="Multiply intersect right")

    result = algebra.multiply(x, y, Interpolate.NAN)
    expected = pd.Series([2.0, 3.0, 6.0, np.nan], index=dates1)
    assert_series_equal(result, expected, obj="Multiply NaN left")

    result = algebra.multiply(y, x, Interpolate.NAN)
    expected = pd.Series([2.0, 3.0, 6.0, np.nan], index=dates1)
    assert_series_equal(result, expected, obj="Multiply NaN right")

    result = algebra.multiply(x, y, Interpolate.ZERO)
    expected = pd.Series([2.0, 3.0, 6.0, 0.0], index=dates1)
    assert_series_equal(result, expected, obj="Multiply zero left")

    result = algebra.multiply(x, y, Interpolate.STEP)
    expected = pd.Series([2.0, 3.0, 6.0, 8.0], index=dates1)
    assert_series_equal(result, expected, obj="Multiply step left")

    result = algebra.multiply(x, 2.0)
    expected = pd.Series([2.0, 4.0, 6.0, 8.0], index=dates1)
    assert_series_equal(result, expected, obj="Multiply scalar left")

    result = algebra.multiply(2.0, x)
    expected = pd.Series([2.0, 4.0, 6.0, 8.0], index=dates1)
    assert_series_equal(result, expected, obj="Multiply scalar right")

    assert algebra.multiply(1, 2) == 2


def test_divide():
    dates1 = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
    ]

    dates2 = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
    ]

    x = pd.Series([1.0, 2.0, 3.0, 4.0], index=dates1)
    y = pd.Series([2.0, 1.0, 2.0], index=dates2)

    result = algebra.divide(x, y, Interpolate.INTERSECT)
    expected = pd.Series([0.5, 2.0, 1.5], index=dates2)
    assert_series_equal(result, expected, obj="Divide intersect left")

    result = algebra.divide(y, x, Interpolate.INTERSECT)
    expected = pd.Series([2.0, 0.5, 2 / 3], index=dates2)
    assert_series_equal(result, expected, obj="Divide intersect right")

    result = algebra.divide(x, y, Interpolate.NAN)
    expected = pd.Series([0.5, 2.0, 1.5, np.nan], index=dates1)
    assert_series_equal(result, expected, obj="Divide NaN left")

    result = algebra.divide(y, x, Interpolate.NAN)
    expected = pd.Series([2.0, 0.5, 2 / 3, np.nan], index=dates1)
    assert_series_equal(result, expected, obj="Divide NaN right")

    result = algebra.divide(x, y, Interpolate.ZERO)
    expected = pd.Series([0.5, 2.0, 1.5, np.inf], index=dates1)
    assert_series_equal(result, expected, obj="Divide zero left")

    result = algebra.divide(x, y, Interpolate.STEP)
    expected = pd.Series([0.5, 2.0, 1.5, 2.0], index=dates1)
    assert_series_equal(result, expected, obj="Divide step left")

    result = algebra.divide(x, 2)
    expected = pd.Series([0.5, 1.0, 1.5, 2.0], index=dates1)
    assert_series_equal(result, expected, obj="Divide scalar left")

    result = algebra.divide(2, x)
    expected = pd.Series([2.0, 1.0, 2 / 3, 0.5], index=dates1)
    assert_series_equal(result, expected, obj="Divide scalar right")

    assert algebra.divide(1, 2) == 0.5

    with pytest.raises(ZeroDivisionError):
        algebra.divide(1, 0)


def test_floordiv():
    dates1 = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
    ]

    dates2 = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
    ]

    x = pd.Series([1.0, 2.0, 3.0, 4.0], index=dates1)
    y = pd.Series([2.0, 1.0, 2.0], index=dates2)

    result = algebra.floordiv(x, y, Interpolate.INTERSECT)
    expected = pd.Series([0.0, 2.0, 1.0], index=dates2)
    assert_series_equal(result, expected, obj="Floor divide intersect left")

    result = algebra.floordiv(y, x, Interpolate.INTERSECT)
    expected = pd.Series([2.0, 0.0, 0.0], index=dates2)
    assert_series_equal(result, expected, obj="Floor divide intersect right")

    result = algebra.floordiv(x, y, Interpolate.NAN)
    expected = pd.Series([0.0, 2.0, 1.0, np.nan], index=dates1)
    assert_series_equal(result, expected, obj="Floor divide NaN left")

    result = algebra.floordiv(y, x, Interpolate.NAN)
    expected = pd.Series([2.0, 0.0, 0.0, np.nan], index=dates1)
    assert_series_equal(result, expected, obj="Floor divide NaN right")

    result = algebra.floordiv(x, y, Interpolate.ZERO)
    expected = pd.Series([0.0, 2.0, 1.0, np.floor_divide(1.0, 0.0)], index=dates1)
    assert_series_equal(result, expected, obj="Floor divide zero left")

    result = algebra.floordiv(x, y, Interpolate.STEP)
    expected = pd.Series([0.0, 2.0, 1.0, 2.0], index=dates1)
    assert_series_equal(result, expected, obj="Floor divide step left")

    result = algebra.floordiv(x, 2, Interpolate.STEP)
    expected = pd.Series([0.0, 1.0, 1.0, 2.0], index=dates1)
    assert_series_equal(result, expected, obj="Floor divide scalar left")

    result = algebra.floordiv(2, x, Interpolate.STEP)
    expected = pd.Series([2.0, 1.0, 0.0, 0.0], index=dates1)
    assert_series_equal(result, expected, obj="Floor divide scalar right")

    assert algebra.floordiv(3, 2) == 1.0

    with pytest.raises(ZeroDivisionError):
        algebra.floordiv(1, 0)


def test_exp():
    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
    ]

    x = pd.Series([1.0, 2.0, 3.0], index=dates)

    result = algebra.exp(x)
    expected = pd.Series([np.exp(1), np.exp(2), np.exp(3)], index=dates)
    assert_series_equal(result, expected, obj="Exp")


def test_log():
    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
    ]

    x = pd.Series([1.0, 2.0, 3.0], index=dates)

    result = algebra.log(x)
    expected = pd.Series([np.log(1), np.log(2), np.log(3)], index=dates)
    assert_series_equal(result, expected, obj="Log")


def test_power():
    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
    ]

    x = pd.Series([1.0, 2.0, 3.0], index=dates)

    result = algebra.power(x, 2)
    expected = pd.Series([1.0, 4.0, 9.0], index=dates)
    assert_series_equal(result, expected, obj="Pow")


def test_sqrt():
    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
    ]

    x = pd.Series([1.0, 4.0, 9.0], index=dates)

    result = algebra.sqrt(x)
    expected = pd.Series([1.0, 2.0, 3.0], index=dates)
    assert_series_equal(result, expected, obj="Sqrt")

    actual = algebra.sqrt(9)
    assert isinstance(actual, int)
    assert 3 == actual

    assert math.sqrt(10) == algebra.sqrt(10)


def test_abs():
    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
    ]

    x = pd.Series([-1.0, 2.0, -3.0], index=dates)

    result = algebra.abs_(x)
    expected = pd.Series([1.0, 2.0, 3.0], index=dates)
    assert_series_equal(result, expected, obj="Abs")


def test_floor():
    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
    ]

    x = pd.Series([1.0, 2.0, 3.0], index=dates)

    result = algebra.floor(x, 2.0)
    expected = pd.Series([2.0, 2.0, 3.0], index=dates)
    assert_series_equal(result, expected, obj="Floor")


def test_ceil():
    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
    ]

    x = pd.Series([1.0, 2.0, 3.0], index=dates)

    result = algebra.ceil(x, 2.0)
    expected = pd.Series([1.0, 2.0, 2.0], index=dates)
    assert_series_equal(result, expected, obj="Ceil")


def test_filter():
    dates1 = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4)
    ]

    all_pos = pd.Series([1.0, 1.0, 1.0, 1.0], index=dates1)
    with_null = pd.Series([1.0, np.nan, 1.0, 1.0], index=dates1)
    zero_neg_pos = pd.Series([-1.0, 0.0, 10.0, 1.0], index=dates1)

    result = filter_(all_pos)
    expected = all_pos
    assert_series_equal(result, expected, obj="zap: remove nulls when no nulls are in TS")

    result = filter_(all_pos, FilterOperator.EQUALS, 0)
    expected = all_pos
    assert_series_equal(result, expected, obj="zap: remove 0s when no 0s are in TS")

    result = filter_(with_null)
    expected = pd.Series([1.0, 1.0, 1.0],
                         index=[date(2019, 1, 1),
                                date(2019, 1, 3), date(2019, 1, 4)])
    assert_series_equal(result, expected, obj="zap: remove nulls in TS")

    result = filter_(zero_neg_pos, FilterOperator.EQUALS, 0)
    expected = pd.Series([-1.0, 10.0, 1.0],
                         index=[date(2019, 1, 1),
                                date(2019, 1, 3), date(2019, 1, 4)])
    assert_series_equal(result, expected, obj="zap: remove 0s in TS")

    result = filter_(zero_neg_pos, FilterOperator.GREATER, 0)
    expected = pd.Series([-1.0, 0.0], index=[date(2019, 1, 1), date(2019, 1, 2)])
    assert_series_equal(result, expected, obj="zap: remove positive values in TS")

    result = filter_(zero_neg_pos, FilterOperator.LESS, 0)
    expected = pd.Series([0.0, 10.0, 1.0], index=[date(2019, 1, 2), date(2019, 1, 3), date(2019, 1, 4)])
    assert_series_equal(result, expected, obj="zap: remove negative values in TS")

    result = filter_(zero_neg_pos, FilterOperator.L_EQUALS, 0)
    expected = pd.Series([10.0, 1.0], index=[date(2019, 1, 3), date(2019, 1, 4)])
    assert_series_equal(result, expected, obj="zap: remove values less than or eq to 0 in TS")

    result = filter_(zero_neg_pos, FilterOperator.G_EQUALS, 0)
    expected = pd.Series([-1.0], index=[date(2019, 1, 1)])
    assert_series_equal(result, expected, obj="zap: remove values greater than or eq to 0 in TS")

    result = filter_(zero_neg_pos, FilterOperator.N_EQUALS, 0)
    expected = pd.Series([0.0], index=[date(2019, 1, 2)])
    assert_series_equal(result, expected, obj="zap: remove all values but 0 in TS")

    with pytest.raises(MqValueError):
        filter_(zero_neg_pos, 0, 0)
    with pytest.raises(MqValueError):
        filter_(zero_neg_pos, 0)


def test_filter_dates():
    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4)
    ]

    all_pos = pd.Series([1.0, 1.0, 1.0, 1.0], index=dates)
    with_null = pd.Series([1.0, np.nan, 1.0, 1.0], index=dates)

    result = algebra.filter_dates(all_pos)
    expected = all_pos
    assert_series_equal(result, expected, obj="zap: remove nulls when no nulls are in TS")

    result = algebra.filter_dates(with_null)
    expected = pd.Series([1.0, 1.0, 1.0],
                         index=[date(2019, 1, 1),
                                date(2019, 1, 3), date(2019, 1, 4)])
    assert_series_equal(result, expected, obj="zap: remove nulls in TS")

    result = algebra.filter_dates(all_pos, FilterOperator.EQUALS, date(2019, 1, 2))
    expected = pd.Series([1.0, 1.0, 1.0],
                         index=[date(2019, 1, 1),
                                date(2019, 1, 3), date(2019, 1, 4)])
    assert_series_equal(result, expected, obj="zap: remove date in TS")

    result = algebra.filter_dates(all_pos, FilterOperator.EQUALS, [date(2019, 1, 2), date(2019, 1, 4)])
    expected = pd.Series([1.0, 1.0],
                         index=[date(2019, 1, 1), date(2019, 1, 3)])
    assert_series_equal(result, expected, obj="zap: remove dates in TS")

    result = algebra.filter_dates(all_pos, FilterOperator.GREATER, date(2019, 1, 2))
    expected = pd.Series([1.0, 1.0], index=[date(2019, 1, 1), date(2019, 1, 2)])
    assert_series_equal(result, expected, obj="zap: remove dates after certain date in TS")

    result = algebra.filter_dates(all_pos, FilterOperator.LESS, date(2019, 1, 3))
    expected = pd.Series([1.0, 1.0], index=[date(2019, 1, 3), date(2019, 1, 4)])
    assert_series_equal(result, expected, obj="zap: remove dates before certain date in TS")

    result = algebra.filter_dates(all_pos, FilterOperator.L_EQUALS, date(2019, 1, 2))
    expected = pd.Series([1.0, 1.0], index=[date(2019, 1, 3), date(2019, 1, 4)])
    assert_series_equal(result, expected, obj="zap: remove dates on or before certain date in TS")

    result = algebra.filter_dates(all_pos, FilterOperator.G_EQUALS, date(2019, 1, 3))
    expected = pd.Series([1.0, 1.0], index=[date(2019, 1, 1), date(2019, 1, 2)])
    assert_series_equal(result, expected, obj="zap: remove dates on or after certain date in TS")

    result = algebra.filter_dates(all_pos, FilterOperator.N_EQUALS, date(2019, 1, 2))
    expected = pd.Series([1.0], index=[date(2019, 1, 2)])
    assert_series_equal(result, expected, obj="zap: remove all dates other than certain date in TS")

    result = algebra.filter_dates(all_pos, FilterOperator.N_EQUALS, [date(2019, 1, 2), date(2019, 1, 4)])
    expected = pd.Series([1.0, 1.0], index=[date(2019, 1, 2), date(2019, 1, 4)])
    assert_series_equal(result, expected, obj="zap: remove all dates other than certain dates in TS")

    with pytest.raises(MqValueError):
        algebra.filter_dates(all_pos, 0, 0)
    with pytest.raises(MqValueError):
        algebra.filter_dates(all_pos, 0)
    with pytest.raises(MqValueError):
        algebra.filter_dates(all_pos, FilterOperator.GREATER, [date(2019, 1, 2), date(2019, 1, 4)])


def test_smooth_spikes():
    s = pd.Series([1, 3])
    actual = smooth_spikes(s, 0.5)
    assert actual.empty

    sparse_index = pd.to_datetime(['2020-01-01', '2020-01-02', '2020-01-04', '2020-01-07'])
    s = pd.Series([8, 10.0, 8, 6.4], index=sparse_index)
    actual = smooth_spikes(s, 0.25)
    expected = pd.Series([10.0, 8], index=sparse_index[1:3])
    assert_series_equal(actual, expected)

    s = pd.Series([8, 10.1, 8, 6.4], index=sparse_index)
    actual = smooth_spikes(s, 0.25)
    expected = pd.Series([8.0, 8], index=sparse_index[1:3])
    assert_series_equal(actual, expected)

    s = pd.Series([0.1, 1.5, 0.2, 2], index=sparse_index)
    actual = smooth_spikes(s, threshold=1, threshold_type=ThresholdType.absolute)
    expected = pd.Series([0.15, 1.75], index=sparse_index[1:3])
    assert_series_equal(actual, expected)

    s = pd.Series([10.1, 8, 12, 10], index=sparse_index)
    actual = smooth_spikes(s, 1, ThresholdType.absolute)
    expected = pd.Series([11.05, 9], index=sparse_index[1:3])
    assert_series_equal(actual, expected)

    s = pd.Series([1, 2, 3, 4], index=sparse_index)
    actual = smooth_spikes(s, 0.25, ThresholdType.absolute)
    expected = pd.Series([2, 3], index=sparse_index[1:3])
    assert_series_equal(actual, expected)

    s = pd.Series([1, 3, 2, 4], index=sparse_index)
    actual = smooth_spikes(s, 0.5, ThresholdType.absolute)
    expected = pd.Series([1.5, 3.5], index=sparse_index[1:3])
    assert_series_equal(actual, expected)


def test_repeat():
    with pytest.raises(MqError):
        repeat(pd.Series, 0)
    with pytest.raises(MqError):
        repeat(pd.Series, 367)

    sparse_index = pd.to_datetime(['2020-01-01', '2020-01-02', '2020-01-04', '2020-01-07'])
    s = pd.Series([1, 2, 3, 4], index=sparse_index)

    actual = repeat(s)
    expected = pd.Series([1, 2, 2, 3, 3, 3, 4], index=pd.date_range(start='2020-01-01', end='2020-01-07', freq='D'))
    assert_series_equal(actual, expected)

    actual = repeat(s, 2)
    expected = pd.Series([1, 2, 3, 4], index=pd.date_range(start='2020-01-01', end='2020-01-07', freq='2D'))
    assert_series_equal(actual, expected)


def test_and():
    with pytest.raises(MqError):
        and_()
    with pytest.raises(MqError):
        and_(pd.Series(dtype=float))
    with pytest.raises(MqError):
        and_(pd.Series(dtype=float), 1)
    with pytest.raises(MqError):
        and_(pd.Series([2]), pd.Series(dtype=float))
    assert and_(pd.Series(dtype=float), pd.Series(dtype=float)).shape[0] == 0

    a = pd.Series([0, 0, 0, 0, 1, 1, 1, 1])
    b = pd.Series([0, 0, 1, 1, 0, 0, 1, 1])
    c = pd.Series([0, 1, 0, 1, 0, 1, 0, 1])
    assert_series_equal(and_(a, b), pd.Series([0] * 6 + [1] * 2), check_dtype=False)
    assert_series_equal(and_(a, b, c), pd.Series([0] * 7 + [1]), check_dtype=False)
    assert_series_equal(and_(pd.Series([0, 1]), pd.Series(dtype=float)), pd.Series([0] * 2), check_dtype=False)


def test_or():
    with pytest.raises(MqError):
        or_()
    with pytest.raises(MqError):
        or_(pd.Series(dtype=float))
    with pytest.raises(MqError):
        or_(pd.Series(dtype=float), 1)
    with pytest.raises(MqError):
        or_(pd.Series([2]), pd.Series(dtype=float))
    assert or_(pd.Series(dtype=float), pd.Series(dtype=float)).shape[0] == 0

    a = pd.Series([0, 0, 0, 0, 1, 1, 1, 1])
    b = pd.Series([0, 0, 1, 1, 0, 0, 1, 1])
    c = pd.Series([0, 1, 0, 1, 0, 1, 0, 1])
    assert_series_equal(or_(a, b), pd.Series([0] * 2 + [1] * 6), check_dtype=False)
    assert_series_equal(or_(a, b, c), pd.Series([0] + [1] * 7), check_dtype=False)
    assert_series_equal(or_(pd.Series([0, 1]), pd.Series(dtype=float)), pd.Series([0, 1]), check_dtype=False)


def test_not():
    with pytest.raises(MqError):
        not_(pd.Series([2]))
    assert not_(pd.Series(dtype=float)).shape[0] == 0
    assert_series_equal(not_(pd.Series([0, 1])), pd.Series([1, 0]), check_dtype=False)


def test_if():
    with pytest.raises(MqError):
        if_(pd.Series([-1, 0]), 5, 6)
    with pytest.raises(MqError):
        if_(pd.Series([1, 0]), 5, '6')

    flags = pd.Series([0, 1])
    truths = pd.Series([2, 2])

    assert_series_equal(if_(flags, 2, 3), pd.Series([3, 2]))
    assert_series_equal(if_(flags, truths, pd.Series([3, 3])), pd.Series([3, 2]))
    assert_series_equal(if_(flags, truths, pd.Series([3], index=[100])),
                        pd.Series([np.nan, 2]), check_dtype=False)


def test_weighted_average():
    empty = pd.Series(dtype=float)
    with pytest.raises(MqError):
        weighted_sum([empty, 3], [.4, .6])
    with pytest.raises(MqError):
        weighted_sum([empty, empty], [.4, '.6'])
    with pytest.raises(MqError):
        weighted_sum([empty, empty], [.4])

    a = pd.Series([1, 2, 3, 4], index=pd.date_range('2020-01-01', periods=4, freq='D'))
    b = pd.Series([24, 27, 30], index=(pd.date_range('2020-01-01', periods=3, freq='D')))
    actual = weighted_sum([a, b], [.3, .6])
    expected = pd.Series([16.333333, 18.666666, 21], index=pd.date_range('2020-01-01', periods=3))
    expected.index.freq = None
    assert_series_equal(actual, expected)


def test_geometrically_aggregate():
    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 5),
    ]

    x = pd.Series([None, 0.05, 0.04, -0.03, 0.12], index=dates)

    result = geometrically_aggregate(x)
    expected = pd.Series([None, 0.05, 0.09200000000000008, 0.05923999999999996, 0.18634879999999998], index=dates)
    assert_series_equal(result, expected)


if __name__ == '__main__':
    pytest.main(args=["test_algebra.py"])
