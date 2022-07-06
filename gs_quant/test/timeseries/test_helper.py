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
import datetime
from enum import IntEnum
from unittest.mock import Mock

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
from testfixtures import Replace, Replacer

import gs_quant.timeseries as ts
from gs_quant.data import DataContext, Dataset
from gs_quant.errors import MqError, MqRequestError
from unittest.mock import MagicMock
from gs_quant.session import GsSession
from gs_quant.test.api.test_thread_manager import NullContextManager
from gs_quant.timeseries.helper import _create_int_enum, _tenor_to_month, _month_to_tenor, plot_function, \
    plot_measure, plot_method, normalize_window, Window, apply_ramp, check_forward_looking, get_df_with_retries, \
    get_dataset_data_with_retries, _split_where_conditions

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


def test_tenor_to_month():
    with pytest.raises(MqError):
        _tenor_to_month('1d')
    with pytest.raises(MqError):
        _tenor_to_month('2w')
    assert _tenor_to_month('3m') == 3
    assert _tenor_to_month('4y') == 48


def test_month_to_tenor():
    assert _month_to_tenor(36) == '3y'
    assert _month_to_tenor(18) == '18m'


@plot_function
def pf():
    pass


@plot_measure(('xyz',), asset_type=('abc',))
def pm():
    pass


@plot_method
def pmt(arg):
    return arg


def test_decorators():
    assert pf.plot_function
    assert pm.plot_measure
    assert pmt.plot_method
    assert pm.asset_class == ('xyz',)
    assert pm.asset_type == ('abc',)
    assert pm.asset_type_excluded is None
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
    x = ts.generate_series(10)
    w = normalize_window(x, "1h")
    assert w.w == pd.DateOffset(hours=1)
    assert w.r == pd.DateOffset(hours=1)


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


def test_get_df_with_retries():
    start = datetime.date(2020, 12, 1)
    end = datetime.date(2020, 12, 2)
    counter = 0

    def fetch0():
        return pd.DataFrame()

    def fetch1():
        nonlocal counter
        counter += 1
        if counter > 1:
            return pd.DataFrame([['foo'], ['bar']])
        return pd.DataFrame()

    def mock_apply(self, *_args, **_kwargs):
        return self.base_date - datetime.timedelta(days=1)

    with Replace('gs_quant.timeseries.helper.RelativeDate.apply_rule', mock_apply):
        df = get_df_with_retries(fetch0, start, end, 'NYSE')
        assert df.empty
        df = get_df_with_retries(fetch1, start, end, 'NYSE', 0)
        assert df.empty
        df = get_df_with_retries(fetch1, start, end, 'NYSE', 1)
        assert not df.empty
        df = get_df_with_retries(fetch1, start, end, 'NYSE', 2)
        assert not df.empty


def test_forward_looking():
    today = datetime.date.today()
    source = 'plottool'
    with DataContext(today, today + datetime.timedelta(days=1)):
        assert check_forward_looking('1b', None) is None
        assert check_forward_looking(today, None) is None
        assert check_forward_looking(None, None) is None
        assert check_forward_looking('1b', source) is None
        assert check_forward_looking(today, source) is None
        assert check_forward_looking(None, source) is None
    with DataContext(today - datetime.timedelta(days=1), today):
        assert check_forward_looking('1b', None) is None
        assert check_forward_looking(today, None) is None
        assert check_forward_looking(None, None) is None
        assert check_forward_looking('1b', source) is None
        assert check_forward_looking(today, source) is None
        with pytest.raises(MqError):
            check_forward_looking(None, source)


def test_get_dataset_data_with_retries():
    replace = Replacer()
    GsSession.current = MagicMock(return_calue=NullContextManager())
    mock = replace('gs_quant.data.dataset.Dataset.get_data', Mock())
    mock.side_effect = [
        MqRequestError(400, message='Number of rows returned by your query is more than maximum allowed'),
        pd.DataFrame(),
        pd.DataFrame()
    ]

    dataset = Dataset(Dataset.TR.TREOD)
    data = get_dataset_data_with_retries(dataset, start=datetime.date(2000, 1, 2), end=datetime.date(2019, 1, 9),
                                         assetId='MA4B66MW5E27U8P32SB')

    assert_frame_equal(data, pd.DataFrame())

    mock.side_effect = [
        MqRequestError(400, message='Some other error')
    ]

    with pytest.raises(MqRequestError):
        get_dataset_data_with_retries(dataset, start=datetime.date(2000, 1, 2), end=datetime.date(2019, 1, 9),
                                      assetId='MA4B66MW5E27U8P32SB')

    replace.restore()


def test_split_where_conditions():
    where = dict(tenor=['1m', '2m'], strikeReference='delta_call', relativeStrike=25)
    expected = [dict(tenor=['1m'], strikeReference='delta_call', relativeStrike=25),
                dict(tenor=['2m'], strikeReference='delta_call', relativeStrike=25)]
    actual = _split_where_conditions(where)
    assert actual == expected

    where = dict(tenor='1m', strikeReference='delta_call', relativeStrike=25)
    expected = [dict(tenor='1m', strikeReference='delta_call', relativeStrike=25)]
    actual = _split_where_conditions(where)
    assert actual == expected

    where = dict()
    expected = [dict()]
    actual = _split_where_conditions(where)
    assert actual == expected

    where = dict(tenor=['1m', '2m'], strikeReference='delta_call', relativeStrike=[25, 50])
    expected = [dict(tenor=['1m'], strikeReference='delta_call', relativeStrike=[25]),
                dict(tenor=['1m'], strikeReference='delta_call', relativeStrike=[50]),
                dict(tenor=['2m'], strikeReference='delta_call', relativeStrike=[25]),
                dict(tenor=['2m'], strikeReference='delta_call', relativeStrike=[50])
                ]
    actual = _split_where_conditions(where)
    assert actual == expected


if __name__ == "__main__":
    pytest.main(args=["test_helper.py"])
