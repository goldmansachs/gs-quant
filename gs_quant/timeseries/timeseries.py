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

Chart Service will attempt to make public functions (not prefixed with _) from this module available. Such functions
should be fully documented: docstrings should describe parameters and the return value, and provide a 1-line
description. Type annotations should be provided for parameters.
"""

from __future__ import (absolute_import, division, print_function, unicode_literals)
from builtins import *  # requires future
import collections
import math
import numpy
import pandas as pd
import typing as ty
from ..errors import *

Drawdown = collections.namedtuple('Drawdown', ['start', 'end', 'value'])

# annualization factors
_DAILY = 252
_WEEKLY = 52
_SEMI_MONTHLY = 26
_MONTHLY = 12
_QUARTERLY = 4
_SEMI_ANNUALLY = 2
_ANNUALLY = 1


def _drawdown(series):
    # type: (pd.Series) -> Drawdown
    if len(series) < 2:
        raise MqValueError('insufficient data')
    assert series.index.is_monotonic_increasing

    peak = series.max()
    end = series.iloc[-1]
    return Drawdown(series.idxmax(), series.index[-1], (end - peak) / peak) if end != peak else None


def _max_drawdown(series, greatest=False):
    if len(series) < 2:
        raise MqValueError('insufficient data')
    assert series.index.is_monotonic_increasing

    peak = series[0]
    peak_idx = 0
    mdd = 0
    history = []
    start = None
    end = None
    for idx, value in series.iloc[1:].iteritems():
        if value > peak:
            peak = value
            peak_idx = idx
        decline = (value - peak) / peak
        history.append(decline)
        if decline < mdd:
            mdd = decline
            start = peak_idx
            end = idx

    if greatest:
        return Drawdown(start, end, mdd) if mdd < 0 else None
    return pd.Series(data=history, index=series.index[1:])


def max_drawdown(series):
    """
    Calculate maximum drawdown.
    :param series: date-based time series of prices
    :return: date-based time series of maximum drawdown
    """
    return _max_drawdown(series, False)


max_drawdown.__annotations__ = {'series': pd.Series, 'return': pd.Series}


def _get_factor(distances):
    # type: (ty.List[int]) -> int
    mean = numpy.average(distances)
    if mean < 2.1:
        factor = _DAILY
    elif mean <= 6:
        factor = _WEEKLY + ((6 - mean) * (_DAILY - _WEEKLY) / 3.9)
    elif mean < 8:
        factor = _WEEKLY
    elif mean <= 14:
        factor = _SEMI_MONTHLY + ((14 - mean) * (_WEEKLY - _SEMI_MONTHLY) / 6)
    elif mean < 17:
        factor = _SEMI_MONTHLY
    elif mean <= 25:
        factor = _MONTHLY + ((25 - mean) * (_SEMI_MONTHLY - _MONTHLY) / 8)
    elif mean < 35:
        factor = _MONTHLY
    elif mean <= 85:
        factor = _QUARTERLY + ((85 - mean) * (_MONTHLY - _QUARTERLY) / 50)
    elif mean < 97:
        factor = _QUARTERLY
    elif mean <= 364:
        factor = _ANNUALLY + ((364 - mean) * (_QUARTERLY - _ANNUALLY) / 279)
    elif mean < 386:
        factor = _ANNUALLY
    else:
        raise MqValueError('data points are too far apart')
    return factor


def realized_volatility(series, window=0):
    """
    Calculate realized volatility.
    :param series: date-based time series of prices
    :param window: number of days / observations to use when calculating volatility (defaults to length of series)
    :return: date-based time series of realized volatility
    """
    window = window or series.size - 1
    if len(series) < 3:
        raise MqValueError('insufficient data')
    assert series.index.is_monotonic_increasing

    prev_idx = series.index[0]
    prev_value = series[0]
    distances = []
    r = []  # returns
    for idx, value in series.iloc[1:].iteritems():
        d = (idx - prev_idx).days
        if d == 0:
            raise MqValueError('multiple data points on same date')
        distances.append(d)
        r.append(value / prev_value - 1)
        prev_idx = idx
        prev_value = value

    factor = _get_factor(distances)
    vols = []
    for i in range(window, len(r) + 1):
        vols.append(math.sqrt(numpy.var(r[i - window:i], ddof=1) * factor))
    return pd.Series(data=vols, index=series.index[window:])


realized_volatility.__annotations__ = {'series': pd.Series, 'window': int, 'return': pd.Series}


def ind(x):
    """
    Multiplicative series normalization. Divides every value in x by the initial value of x.
    :param x: time series
    :return: normalized time series
    """
    return x / x[0]


ind.__annotations__ = {'x': pd.Series, 'return': pd.Series}
