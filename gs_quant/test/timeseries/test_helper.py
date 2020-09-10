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

from enum import IntEnum
import pandas as pd
import pytest

import gs_quant.timeseries as ts
from gs_quant.timeseries.helper import _create_int_enum, plot_function, plot_measure, plot_method, normalize_window, \
    Window, apply_ramp

# TODO test the instance of IntEnum when we have any.

WeekDay = _create_int_enum('WeekDay', {'SUNDAY': 1, 'Monday': 2, 'TUESDAY': 3,
                                       'WEDNESDAY': 4, 'THURSDAY': 5, 'Friday': 6, 'SATURDAY': 7})


def test_int_enum():
    assert ['a', 'b', 'c'][WeekDay.MONDAY] == 'c'

    assert len(list(WeekDay)) == 7
    assert len(WeekDay) == 7
    target = 'SUNDAY MONDAY TUESDAY WEDNESDAY THURSDAY FRIDAY SATURDAY'
    target = target.split()
    for i, weekday in enumerate(target, 1):
        e = WeekDay(i)
        assert isinstance(e, IntEnum)
        assert e.name == weekday
        assert e.value == i


@plot_function
def pf():
    pass


@plot_measure(asset_type=('abc',))
def pm():
    pass


@plot_method
def pmt(arg):
    return arg


def test_decorators():
    assert pf.plot_function
    assert pm.plot_measure
    assert pmt.plot_method
    assert pm.asset_class is None
    assert pm.asset_type == ('abc',)
    assert pmt(1, real_time=True) == 1


def test_normalize_window_defaults_window_if_none_passed():
    x = ts.generate_series(10)
    w = normalize_window(x, None)
    assert w.w == 10
    assert w.r == 0


def test_normalize_window_defaults_window_if_passed():
    x = ts.generate_series(10)
    w = normalize_window(x, None, default_window=2)
    assert w.w == 2
    assert w.r == 0


def test_normalize_window_handles_int():
    x = ts.generate_series(10)
    w = normalize_window(x, 5)
    assert w.w == 5
    assert w.r == 5


def test_normalize_window_handles_window_with_no_ramp():
    x = ts.generate_series(10)
    w = normalize_window(x, Window(2, None))
    assert w.w == 2
    assert w.r == 2


def test_normalize_window_handles_window_with_no_size():
    x = ts.generate_series(10)
    w = normalize_window(x, Window(None, 2))
    assert w.w == 10
    assert w.r == 2


def test_normalize_window_handles_ramp_greater_than_series_length():
    with pytest.raises(ValueError):
        x = ts.generate_series(10)
        normalize_window(x, Window(2, 11))


def test_normalize_window_raises_error_on_window_of_size_zero():
    with pytest.raises(ValueError):
        x = ts.generate_series(10)
        normalize_window(x, 0)
    with pytest.raises(ValueError):
        x = ts.generate_series(10)
        normalize_window(x, Window(0, 0))


def test_normalize_window_handles_ramp_of_size_zero():
    x = ts.generate_series(10)
    w = normalize_window(x, Window(2, 0))
    assert w.w == 2
    assert w.r == 0


def test_normalize_window_str():
    x = ts.generate_series(10)
    w = normalize_window(x, Window('1w', '2d'))
    assert w.w == pd.DateOffset(weeks=1)
    assert w.r == pd.DateOffset(days=2)


def test_normalize_window_single_str():
    x = ts.generate_series(10)
    w = normalize_window(x, "2d")
    assert w.w == pd.DateOffset(days=2)
    assert w.r == pd.DateOffset(days=2)
    x = ts.generate_series(90)
    w = normalize_window(x, "3m")
    assert w.w == pd.DateOffset(months=3)
    assert w.r == pd.DateOffset(months=3)


def test_apply_ramp():
    x = ts.generate_series(10)
    y = apply_ramp(x, Window(2, 2))
    assert len(y) == 8


def test_apply_ramp_with_window_greater_than_series_length():
    x = ts.generate_series(10)
    y = apply_ramp(x, Window(11, 2))
    assert len(y) == 0


def test_apply_ramp_dateoffset():
    x = pd.Series(range(10), index=pd.bdate_range('2020-02-17', freq='b', periods=10))
    y = apply_ramp(x, Window(pd.DateOffset(weeks=1), pd.DateOffset(days=1)))
    assert len(y) == 9


def test_apply_ramp_raises_on_edge_cases():
    with pytest.raises(ValueError):
        x = ts.generate_series(10)
        apply_ramp(x, Window(0, 0))
    with pytest.raises(ValueError):
        x = ts.generate_series(10)
        apply_ramp(x, Window(-1, 0))
    with pytest.raises(ValueError):
        x = ts.generate_series(10)
        apply_ramp(x, Window(2, -1))
    with pytest.raises(ValueError):
        x = ts.generate_series(10)
        apply_ramp(x, Window(2, 11))


if __name__ == "__main__":
    pytest.main(args=["test_helper.py"])
