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

from gs_quant.timeseries.datetime import *


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

    xp = x.copy()
    yp = y.copy()
    xp.index = pd.to_datetime(xp.index)
    yp.index = pd.to_datetime(yp.index)
    up = pd.to_datetime(union_dates)

    expected1 = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0, np.nan], index=up)
    expected2 = pd.Series([np.nan, 20.0, 30.0, 40.0, 50.0, 60.0], index=up)

    result = align(xp, yp, Interpolate.TIME)
    assert_series_equal(result[0], expected1, obj="Align time left")
    assert_series_equal(result[1], expected2, obj="Align time left")

    result = align(yp, xp, Interpolate.TIME)
    assert_series_equal(result[0], expected2, obj="Align time right")
    assert_series_equal(result[1], expected1, obj="Align time right")

    a = pd.Series([0, 100, 110], index=pd.DatetimeIndex(['2019-07-01', '2019-07-08', '2019-07-10']))
    b = pd.Series([20, 60, 70], index=pd.DatetimeIndex(['2019-07-02', '2019-07-10', '2019-07-11']))
    result = align(a, b, Interpolate.TIME)

    u_index = a.index.union(b.index)
    assert_series_equal(result[0], pd.Series([0, 100 / 7, 100, 110, np.nan], index=u_index))
    assert_series_equal(result[1], pd.Series([np.nan, 20, 50, 60, 70], index=u_index))

    result = align(x, 3)
    assert_series_equal(result[0], x, obj="Align scalar left")
    assert_series_equal(result[1], pd.Series(3, index=dates1), obj="Align scalar left")

    result = align(3, x)
    assert_series_equal(result[0], pd.Series(3, index=dates1), obj="Align scalar left")
    assert_series_equal(result[1], x, obj="Align scalar right")

    result = align(1, 2)
    assert result[0] == 1
    assert result[1] == 2

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

    x = pd.Series([2.0, 3.0, 5.0, 7.0], index=pd.DatetimeIndex(dates))
    result = interpolate(x, select_dates, Interpolate.STEP)
    expected = pd.Series([2.0, 2.0, 2.0, 5.0, 5.0, 7.0, 7.0], index=pd.DatetimeIndex(select_dates))
    assert_series_equal(result, expected, obj="Interpolate step dates to series with timestamps")

    with pytest.raises(MqValueError, match="Unknown intersection type: None"):
        interpolate(x, x, "None")

    with pytest.raises(MqValueError, match="Cannot perform step interpolation on an empty series"):
        interpolate(pd.Series(), select_dates, Interpolate.STEP)


def test_value():
    dates = [
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 5),
        date(2019, 1, 7),
    ]

    x = pd.Series([2.0, 3.0, 5.0, 7.0], index=dates)

    result = value(x, date(2019, 1, 3))
    assert result == 3.0

    result = value(x, date(2019, 1, 5))
    assert result == 5.0

    result = value(x, date(2019, 1, 4))
    assert result == 3.0

    result = value(x, date(2019, 1, 4), Interpolate.INTERSECT)
    assert result is None

    result = value(x, date(2019, 1, 4), Interpolate.STEP)
    assert result == 3.0

    result = value(x, date(2019, 1, 4), Interpolate.ZERO)
    assert result == 0.0

    result = value(x, date(2019, 1, 4), Interpolate.NAN)
    assert np.isnan(result)


def test_day():
    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
    ]

    x = pd.Series([1.0, 2.0, 3.0, 4.0], index=dates)

    result = day(x)
    expected = pd.Series([1, 2, 3, 4], index=dates)
    assert_series_equal(result, expected, obj="Day")


def test_weekday():
    dates = [
        date(2019, 1, 7),
        date(2019, 1, 8),
        date(2019, 1, 9),
        date(2019, 1, 10),
        date(2019, 1, 11),
        date(2019, 1, 12),
        date(2019, 1, 13),
    ]

    x = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0], index=dates)

    result = weekday(x)
    expected = pd.Series([0, 1, 2, 3, 4, 5, 6], index=dates)
    assert_series_equal(result, expected, obj="Weekday")


def test_month():
    dates = [
        date(2019, 1, 1),
        date(2019, 2, 1),
        date(2019, 3, 1),
        date(2019, 4, 1),
    ]

    x = pd.Series([1.0, 2.0, 3.0, 4.0], index=dates)

    result = month(x)
    expected = pd.Series([1, 2, 3, 4], index=dates)
    assert_series_equal(result, expected, obj="Month")


def test_year():
    dates = [
        date(2019, 1, 1),
        date(2020, 1, 2),
        date(2021, 1, 3),
        date(2022, 1, 4),
    ]

    x = pd.Series([1.0, 2.0, 3.0, 4.0], index=dates)

    result = year(x)
    expected = pd.Series([2019, 2020, 2021, 2022], index=dates)
    assert_series_equal(result, expected, obj="Year")


def test_quarter():
    dates = [
        date(2019, 1, 1),
        date(2019, 4, 1),
        date(2019, 7, 1),
        date(2019, 10, 1),
    ]

    x = pd.Series([1.0, 2.0, 3.0, 4.0], index=dates)

    result = quarter(x)
    expected = pd.Series([1, 2, 3, 4], index=dates)
    assert_series_equal(result, expected, obj="Quarter")


def test_day_count_fractions():
    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 5),
        date(2019, 1, 6),
    ]

    x = pd.Series([])
    assert_series_equal(x, day_count_fractions(x))

    x = pd.Series([100.0, 101, 103.02, 100.9596, 100.9596, 102.978792], index=dates)

    result = day_count_fractions(x, DayCountConvention.ACTUAL_360)
    result2 = day_count_fractions(x.index, DayCountConvention.ACTUAL_360)
    dcf = 1 / 360
    expected = pd.Series([np.NaN, dcf, dcf, dcf, dcf, dcf], index=dates)
    assert_series_equal(result, expected, obj="ACT/360")
    assert_series_equal(result2, expected, obj="ACT/360")

    result = day_count_fractions(x, DayCountConvention.ACTUAL_365F)
    dcf = 1 / 365
    expected = pd.Series([np.NaN, dcf, dcf, dcf, dcf, dcf], index=dates)
    assert_series_equal(result, expected, obj="ACT/365")


def test_date_range():
    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 5),
        date(2019, 1, 6),
    ]

    values = [1.0, 2.0, 3.0, 4.0, 5.0, 7.0]
    s0 = pd.Series(values, index=dates)
    s1 = pd.Series(values, index=pd.date_range('2019-01-01', periods=6, freq='D'))

    for x in [s0, s1]:
        assert (date_range(x, 0, 0) == x).all()
        assert (date_range(x, 0, 0, True) == x.iloc[:-2]).all()

        assert date_range(x, 0, date(2019, 1, 3)).index[-1] == date(2019, 1, 3)
        assert (date_range(x, 0, date(2019, 1, 3)) == x.iloc[:3]).all()

        assert date_range(x, date(2019, 1, 3), date(2019, 1, 6)).index[0] == date(2019, 1, 3)
        assert date_range(x, date(2019, 1, 3), date(2019, 1, 6)).index[-1] == date(2019, 1, 6)
        assert (date_range(x, date(2019, 1, 3), date(2019, 1, 6)) == x.iloc[2:6]).all()

    y = pd.Series(values, index=pd.date_range('2020-10-23', periods=6, freq='D'))
    assert (date_range(y, 1, 1, True) == y.iloc[3:5]).all()

    with pytest.raises(MqValueError):
        date_range(pd.Series([1]), 0, 0)

    with pytest.raises(MqTypeError):
        date_range(pd.Series([1]), 0, 0, 'string')


def test_prepend():
    x = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0, 7.0], index=pd.date_range('2019-01-01', "2019-01-06"))
    y = pd.Series([3.1, 4.1, 5.1], index=pd.date_range('2019-01-03', '2019-01-05'))

    assert_series_equal(prepend([]), pd.Series(dtype='float64'), obj='prepend empty')

    assert_series_equal(prepend([x]), x, obj='prepend one series')

    actual = prepend([x, y])
    expected = pd.Series([1.0, 2.0, 3.1, 4.1, 5.1], index=pd.date_range('2019-01-01', '2019-01-05'))
    assert_series_equal(actual, expected, obj='prepend two series')

    x = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0, 7.0], index=pd.date_range('2019-01-01', periods=6, freq='H'))
    y = pd.Series([3.1, 4.1, 5.1], index=pd.date_range('2019-01-01 02:00', periods=3, freq='H'))

    actual = prepend([x, y])
    expected = pd.Series([1.0, 2.0, 3.1, 4.1, 5.1], index=pd.date_range('2019-01-01', periods=5, freq='H'))
    assert_series_equal(actual, expected, obj='prepend two real-time series')


def test_union():
    x = pd.Series([3.1, 4.1, np.nan], index=pd.date_range('2019-01-03', '2019-01-05'))
    y = pd.Series([1.0, np.nan, 3.0, 4.0, 5.0, 6.0], index=pd.date_range('2019-01-01', "2019-01-06"))
    z = pd.Series([60.0, 70.0], index=pd.date_range('2019-01-06', "2019-01-07"))

    assert_series_equal(union([]), pd.Series(dtype='float64'), obj='union empty')

    x.index.freq = None
    assert_series_equal(union([x]), x, obj='union of one series')

    actual = union([x, y, z])
    expected = pd.Series([1.0, np.nan, 3.1, 4.1, 5.0, 6.0, 70], index=pd.date_range('2019-01-01', '2019-01-07'))
    assert_series_equal(actual, expected, obj='union of three series')

    x = pd.Series([3.1, 4.1, np.nan], index=pd.date_range('2019-01-01 02:00', periods=3, freq='H'))
    y = pd.Series([1.0, np.nan, 3.0, 4.0, 5.0, 6.0], index=pd.date_range('2019-01-01', periods=6, freq='H'))

    actual = union([x, y])
    expected = pd.Series([1.0, np.nan, 3.1, 4.1, 5.0, 6.0], index=pd.date_range('2019-01-01', periods=6, freq='H'))
    assert_series_equal(actual, expected, obj='union of two real-time series')


def test_bucketize():
    dates = pd.bdate_range(start='1/1/2021', end='4/23/2021')
    series = pd.Series(range(len(dates)), index=dates)

    actual = bucketize(series, AggregateFunction.MAX, AggregatePeriod.MONTH)
    expected_index = pd.DatetimeIndex([date(2021, 1, 31), date(2021, 2, 28), date(2021, 3, 31), date(2021, 4, 23)])
    expected = pd.Series([20, 40, 63, 80], index=expected_index)
    actual.index.freq = None  # Ignore the index freq
    assert_series_equal(actual, expected, check_index_type=False)


def test_day_count():
    assert day_count(datetime.date(2021, 5, 7), datetime.date(2021, 5, 10)) == 1
    assert day_count(datetime.date(2021, 5, 10), datetime.date(2021, 5, 14)) == 4
    assert day_count(datetime.date(2021, 5, 10), datetime.date(2021, 5, 17)) == 5

    with pytest.raises(MqValueError):
        day_count(datetime.date(2021, 5, 7), '2021-05-10')


if __name__ == "__main__":
    pytest.main(args=["test_datetime.py"])
