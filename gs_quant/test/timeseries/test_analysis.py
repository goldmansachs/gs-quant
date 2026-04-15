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

import datetime as dt

import numpy as np
import pandas as pd
import pytest
from gs_quant.errors import MqValueError
from gs_quant.timeseries import (
    first,
    last,
    last_value,
    count,
    Interpolate,
    compare,
    diff,
    lag,
    LagMode,
    repeat,
    smooth_outliers,
    consecutive,
    SignDirection,
)
from gs_quant.timeseries.helper import FREQ_SECOND
from pandas.testing import assert_series_equal


def _normalize_index(idx):
    return idx.as_unit('ns') if hasattr(idx, 'as_unit') else idx


def test_first():
    dates = [
        dt.date(2019, 1, 1),
        dt.date(2019, 1, 2),
        dt.date(2019, 1, 3),
        dt.date(2019, 1, 4),
    ]

    x = pd.Series([1.0, 2.0, 3.0, 4.0], index=dates)

    result = first(x)
    expected = pd.Series([1.0, 1.0, 1.0, 1.0], index=dates)
    assert_series_equal(result, expected, obj="First")


def test_last():
    dates = [
        dt.date(2019, 1, 1),
        dt.date(2019, 1, 2),
        dt.date(2019, 1, 3),
        dt.date(2019, 1, 4),
    ]

    x = pd.Series([1.0, 2.0, 3.0, 4.0], index=dates)

    result = last(x)
    expected = pd.Series([4.0, 4.0, 4.0, 4.0], index=dates)
    assert_series_equal(result, expected, obj="First")

    y = pd.Series([1.0, 2.0, 3.0, np.nan], index=dates)
    result = last(y)
    expected = pd.Series([3.0, 3.0, 3.0, 3.0], index=dates)
    assert_series_equal(result, expected, obj="Last non-NA")


def test_last_value():
    with pytest.raises(MqValueError):
        last_value(pd.Series(dtype=float))

    x = pd.Series([1.0, 2.0, 3.0, 4.0], index=(pd.date_range("2020-01-01", periods=4, freq="D")))
    assert last_value(x) == 4.0

    y = pd.Series([5])
    assert last_value(y) == 5

    y = pd.Series([1.0, 2.0, 3.0, np.nan], index=(pd.date_range("2020-01-01", periods=4, freq="D")))
    assert last_value(y) == 3.0


def test_count():
    dates = [
        dt.date(2019, 1, 1),
        dt.date(2019, 1, 2),
        dt.date(2019, 1, 3),
        dt.date(2019, 1, 4),
    ]

    x = pd.Series([1.0, 2.0, 3.0, 4.0], index=dates)

    result = count(x)
    expected = pd.Series([1.0, 2.0, 3.0, 4.0], index=dates)
    assert_series_equal(result, expected, obj="Count")


def test_compare():
    dates1 = [
        dt.date(2019, 1, 1),
        dt.date(2019, 1, 2),
        dt.date(2019, 1, 3),
        dt.date(2019, 1, 4),
    ]

    dates2 = [
        dt.date(2019, 1, 1),
        dt.date(2019, 1, 2),
        dt.date(2019, 1, 3),
    ]

    x = pd.Series([1.0, 2.0, 2.0, 4.0], index=dates1)
    y = pd.Series([2.0, 1.0, 2.0], index=dates2)

    expected = pd.Series([-1.0, 1.0, 0.0], index=dates2)
    result = compare(x, y, method=Interpolate.INTERSECT)
    assert_series_equal(expected, result, obj="Compare series intersect")

    expected = pd.Series([1.0, -1.0, 0], index=dates2)
    result = compare(y, x, method=Interpolate.INTERSECT)
    assert_series_equal(expected, result, obj="Compare series intersect 2")

    expected = pd.Series([-1.0, 1.0, 0, 0], index=dates1)
    result = compare(x, y, method=Interpolate.NAN)
    assert_series_equal(expected, result, obj="Compare series nan")

    expected = pd.Series([-1.0, 1.0, 0, 1.0], index=dates1)
    result = compare(x, y, method=Interpolate.ZERO)
    assert_series_equal(expected, result, obj="Compare series zero")

    expected = pd.Series([-1.0, 1.0, 0, 1.0], index=dates1)
    result = compare(x, y, method=Interpolate.STEP)
    assert_series_equal(expected, result, obj="Compare series step")

    dates2 = [
        dt.date(2019, 1, 2),
        dt.date(2019, 1, 4),
        dt.date(2019, 1, 6),
    ]

    dates1.append(dt.date(2019, 1, 5))
    xp = pd.Series([1, 2, 3, 4, 5], index=pd.to_datetime(dates1))
    yp = pd.Series([1, 4, 0], index=pd.to_datetime(dates2))
    result = compare(xp, yp, Interpolate.TIME)
    dates1.append(dt.date(2019, 1, 6))
    expected = pd.Series([0.0, 1.0, 1.0, 0.0, 1.0, 0.0], index=pd.to_datetime(dates1))
    assert_series_equal(result, expected, obj="Compare series greater time")


def test_diff():
    dates = [
        dt.date(2019, 1, 1),
        dt.date(2019, 1, 2),
        dt.date(2019, 1, 3),
        dt.date(2019, 1, 4),
    ]

    x = pd.Series([1.0, 2.0, 3.0, 4.0], index=dates)

    result = diff(x)
    expected = pd.Series([np.nan, 1.0, 1.0, 1.0], index=dates)
    assert_series_equal(result, expected, obj="Diff")

    result = diff(x, 2)
    expected = pd.Series([np.nan, np.nan, 2.0, 2.0], index=dates)
    assert_series_equal(result, expected, obj="Diff")

    empty = pd.Series(dtype=float)
    result = diff(empty)
    assert len(result) == 0


def test_lag():
    dates = pd.date_range("2019-01-01", periods=4, freq="D")
    x = pd.Series([1.0, 2.0, 3.0, 4.0], index=dates)

    result = lag(x, '1m')
    expected = pd.Series([1.0, 2.0, 3.0, 4.0], index=_normalize_index(pd.date_range("2019-01-31", periods=4, freq="D")))
    expected.index.freq = None
    assert_series_equal(result, expected, obj="Lag 1m")

    result = lag(x, '2d', LagMode.TRUNCATE)
    expected = pd.Series([1.0, 2.0], index=_normalize_index(pd.date_range("2019-01-03", periods=2, freq="D")))
    expected.index.freq = None
    assert_series_equal(result, expected, obj="Lag 2d truncate")

    result = lag(x, mode=LagMode.TRUNCATE)
    expected = pd.Series([np.nan, 1.0, 2.0, 3.0], index=dates)
    expected.index.freq = None
    assert_series_equal(result, expected, obj="Lag")

    result = lag(x, 2, LagMode.TRUNCATE)
    expected = pd.Series([np.nan, np.nan, 1.0, 2.0], index=dates)
    expected.index.freq = None
    assert_series_equal(result, expected, obj="Lag 2")

    result = lag(x, 2, LagMode.EXTEND)
    expected = pd.Series(
        [np.nan, np.nan, 1.0, 2.0, 3.0, 4.0], index=_normalize_index(pd.date_range("2019-01-01", periods=6, freq="D"))
    )
    assert_series_equal(result, expected, obj="Lag 2 Extend")

    result = lag(x, -2, LagMode.EXTEND)
    expected = pd.Series(
        [1.0, 2.0, 3.0, 4.0, np.nan, np.nan], index=_normalize_index(pd.date_range("2018-12-30", periods=6, freq="D"))
    )
    assert_series_equal(result, expected, obj="Lag Negative 2 Extend")

    result = lag(x, 2)
    expected = pd.Series(
        [np.nan, np.nan, 1.0, 2.0, 3.0, 4.0], index=_normalize_index(pd.date_range("2019-01-01", periods=6, freq="D"))
    )
    assert_series_equal(result, expected, obj="Lag 2 Default")

    y = pd.Series([0] * 4, index=pd.date_range('2020-01-01T00:00:00Z', periods=4, freq=FREQ_SECOND))
    with pytest.raises(Exception):
        lag(y, 5, LagMode.EXTEND)

    z = pd.Series([10, 11, 12], index=pd.date_range('2020-02-28', periods=3, freq='D'))
    result = lag(z, '2y')
    expected = pd.Series([10, 12], index=_normalize_index(pd.date_range('2022-02-28', periods=2, freq='D')))
    expected.index.freq = None
    assert_series_equal(result, expected, obj="Lag RDate 2y")

    # Test that business day offsets raise an error
    with pytest.raises(MqValueError, match="Business day offset '1b' is not supported"):
        lag(x, '1b')

    with pytest.raises(MqValueError, match="Business day offset '-2B' is not supported"):
        lag(x, '-2B')


def test_repeat_empty_series():
    # Test case for an empty series
    empty_series = pd.Series(dtype=float)
    result = repeat(empty_series)
    assert result.empty, "The result should be an empty series when input is empty."


def test_lag_empty_series():
    empty_series = pd.Series(dtype=float)
    result = lag(empty_series)
    assert result.empty, "The result should be an empty series when input is empty."


def test_smooth_outliers():
    # Single outlier should be replaced by interpolation
    dates = pd.date_range("2020-01-01", periods=7, freq="D")
    x = pd.Series([10.0, 10.0, 10.0, 100.0, 10.0, 10.0, 10.0], index=dates)
    result = smooth_outliers(x, threshold=0.5)
    assert result.iloc[3] < 20.0, "Single spike should be smoothed"
    assert result.iloc[0] == 10.0
    assert result.iloc[-1] == 10.0

    # Multiple consecutive outliers should all be replaced
    dates = pd.date_range("2020-01-01", periods=10, freq="D")
    x = pd.Series([10.0, 10.0, 10.0, 100.0, 100.0, 100.0, 10.0, 10.0, 10.0, 10.0], index=dates)
    result = smooth_outliers(x, threshold=0.5)
    for i in range(3, 6):
        assert result.iloc[i] < 20.0, f"Consecutive outlier at index {i} should be smoothed"

    # Series with fewer than 3 elements returns a copy
    x = pd.Series([1.0, 2.0], index=pd.date_range("2020-01-01", periods=2, freq="D"))
    result = smooth_outliers(x)
    assert_series_equal(result, x)

    # Series with no outliers should be unchanged
    dates = pd.date_range("2020-01-01", periods=5, freq="D")
    x = pd.Series([10.0, 10.5, 10.0, 10.5, 10.0], index=dates)
    result = smooth_outliers(x)
    assert_series_equal(result, x.astype(float))

    # threshold <= 0 should raise MqValueError
    x = pd.Series([1.0, 2.0, 3.0], index=pd.date_range("2020-01-01", periods=3, freq="D"))
    with pytest.raises(MqValueError, match='threshold must be positive'):
        smooth_outliers(x, threshold=0)
    with pytest.raises(MqValueError, match='threshold must be positive'):
        smooth_outliers(x, threshold=-1.0)

    # Outliers at the edges should be handled (ffill / bfill fallback)
    dates = pd.date_range("2020-01-01", periods=7, freq="D")
    x = pd.Series([200.0, 10.0, 10.0, 10.0, 10.0, 10.0, 200.0], index=dates)
    result = smooth_outliers(x, threshold=0.5)
    assert result.iloc[0] == 10.0
    assert result.iloc[-1] == 10.0

    # Prolonged anomalous regime (sustained dip) should be smoothed.
    # Simulate: 100 days stable at ~1000, 75 days depressed at ~200, 100 days back to ~1000.
    rng = np.random.default_rng(42)
    n_pre, n_dip, n_post = 100, 75, 100
    dates = pd.date_range("2020-01-01", periods=n_pre + n_dip + n_post, freq="D")
    pre = 1000 + rng.normal(0, 1, n_pre)
    dip = 200 + rng.normal(0, 1, n_dip)
    post = 1000 + rng.normal(0, 1, n_post)
    x = pd.Series(np.concatenate([pre, dip, post]), index=dates)
    result = smooth_outliers(x, threshold=0.5)
    # The dip region should be smoothed — values should be much higher than 200
    assert result.iloc[n_pre : n_pre + n_dip].min() > 400, "Prolonged dip should be smoothed"
    # Pre and post regions should be largely unchanged
    pre_diff = (x.iloc[:n_pre] - result.iloc[:n_pre]).abs().max()
    post_diff = (x.iloc[-n_post:] - result.iloc[-n_post:]).abs().max()
    assert pre_diff < 5.0, "Pre-anomaly region should be unchanged"
    assert post_diff < 5.0, "Post-anomaly region should be unchanged"


def test_consecutive():
    dates = [
        dt.date(2019, 1, 1),
        dt.date(2019, 1, 2),
        dt.date(2019, 1, 3),
        dt.date(2019, 1, 4),
        dt.date(2019, 1, 5),
        dt.date(2019, 1, 6),
    ]

    # Test consecutive positive values
    x = pd.Series([1.0, 2.0, -1.0, 3.0, 4.0, 5.0], index=dates)
    result = consecutive(x, SignDirection.POSITIVE)
    expected = pd.Series([1, 2, 0, 1, 2, 3], index=dates)
    assert_series_equal(result, expected, obj="Consecutive positive")

    # Test consecutive negative values
    x = pd.Series([-1.0, -2.0, 3.0, -4.0, -5.0, -6.0], index=dates)
    result = consecutive(x, SignDirection.NEGATIVE)
    expected = pd.Series([1, 2, 0, 1, 2, 3], index=dates)
    assert_series_equal(result, expected, obj="Consecutive negative")

    # Test default direction is positive
    x = pd.Series([1.0, 2.0, 3.0, -1.0, 5.0, 6.0], index=dates)
    result = consecutive(x)
    expected = pd.Series([1, 2, 3, 0, 1, 2], index=dates)
    assert_series_equal(result, expected, obj="Consecutive default positive")

    # Test all positive
    x = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], index=dates)
    result = consecutive(x, SignDirection.POSITIVE)
    expected = pd.Series([1, 2, 3, 4, 5, 6], index=dates)
    assert_series_equal(result, expected, obj="Consecutive all positive")

    # Test all negative
    x = pd.Series([-1.0, -2.0, -3.0, -4.0, -5.0, -6.0], index=dates)
    result = consecutive(x, SignDirection.NEGATIVE)
    expected = pd.Series([1, 2, 3, 4, 5, 6], index=dates)
    assert_series_equal(result, expected, obj="Consecutive all negative")

    # Test no matching values (all negative, counting positive)
    x = pd.Series([-1.0, -2.0, -3.0, -4.0, -5.0, -6.0], index=dates)
    result = consecutive(x, SignDirection.POSITIVE)
    expected = pd.Series([0, 0, 0, 0, 0, 0], index=dates)
    assert_series_equal(result, expected, obj="Consecutive none positive")

    # Test zeros are neither positive nor negative — should reset the counter
    x = pd.Series([1.0, 2.0, 0.0, 3.0, 4.0, 5.0], index=dates)
    result = consecutive(x, SignDirection.POSITIVE)
    expected = pd.Series([1, 2, 0, 1, 2, 3], index=dates)
    assert_series_equal(result, expected, obj="Consecutive zero resets positive")

    x = pd.Series([-1.0, -2.0, 0.0, -3.0, -4.0, -5.0], index=dates)
    result = consecutive(x, SignDirection.NEGATIVE)
    expected = pd.Series([1, 2, 0, 1, 2, 3], index=dates)
    assert_series_equal(result, expected, obj="Consecutive zero resets negative")

    # Test empty series
    empty = pd.Series(dtype=float)
    result = consecutive(empty)
    assert result.empty, "The result should be an empty series when input is empty."
