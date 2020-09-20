# Copyright 2018 Goldman Sachs.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
#
# Marquee Plot Service will attempt to make public functions (not prefixed with _) from this module available.
# Such functions should be fully documented: docstrings should describe parameters and the return value, and provide
# a 1-line description. Type annotations should be provided for parameters.

import math
from collections import namedtuple

import datetime
import multiprocessing as mp
from multiprocessing import Pool
import numpy
import pandas as pd
from pandas.tseries.offsets import BDay
import scipy.stats.mstats as stats
from scipy.stats import percentileofscore
from scipy.spatial.distance import euclidean
from statsmodels.regression.rolling import RollingOLS
from dtaidistance import dtw
from .algebra import *
import statsmodels.api as sm
from ..models.epidemiology import SIR, SEIR, EpidemicModel
from ..data import DataContext

from typing import Optional, Union, Callable
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import ipywidgets as widgets
from IPython.display import display

"""
Stats library is for basic arithmetic and statistical operations on timeseries.
These include basic algebraic operations, probability and distribution analysis.
Generally not finance-specific routines.
"""


def _concat_series(series: List[pd.Series]):
    curves = []
    constants = {}
    k = 0
    for s in series:
        if s.min() != s.max():
            curves.append(s)
        else:
            constants[f'temp{k}'] = s.min()
            k += 1
    return pd.concat(curves, axis=1).assign(**constants)


@plot_function
def min_(x: Union[pd.Series, List[pd.Series]], w: Union[Window, int, str] = Window(None, 0)) -> pd.Series:
    """
    Minimum value of series over given window

    :param x: series: a timeseries or an array of timeseries

    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value.  If w is a string, it should be a relative date like '1m', '1d', etc.
              Window size defaults to length of series.
    :return: timeseries of minimum value

    **Usage**

    Returns the minimum value of the series over each window.

    If :math:`x` is a series:

    :math:`R_t = min(X_{t-w+1}:X_t)`

    where :math:`w` is the size of the rolling window.


    If :math:`x` is an array of series:

    :math:`R_t = min(X_{1, t-w+1}:X_{n, t})`

    where :math:`w` is the size of the rolling window, and :math:`n` is the number of series.

    If window is not provided, returns the minimum value over the
    full series. If the window size is greater than the available data, will return minimum of available values.

    **Examples**

    Minimum value of price series over the last :math:`22` observations:

    >>> prices = generate_series(100)
    >>> min_(prices, 22)

    **See also**

    :func:`max_`

    """
    if isinstance(x, list):
        x = _concat_series(x).min(axis=1)
    w = normalize_window(x, w)
    assert x.index.is_monotonic_increasing, "series index is monotonic increasing"
    if isinstance(w.w, pd.DateOffset):
        values = [x.loc[(x.index > idx - w.w) & (x.index <= idx)].min() for idx in x.index]
        return apply_ramp(pd.Series(values, index=x.index, dtype=np.dtype(float)), w)
    else:
        return apply_ramp(x.rolling(w.w, 0).min(), w)


@plot_function
def max_(x: Union[pd.Series, List[pd.Series]], w: Union[Window, int, str] = Window(None, 0)) -> pd.Series:
    """
    Maximum value of series over given window

    :param x: series: a timeseries or an array of timeseries
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value.  If w is a string, it should be a relative date like '1m', '1d', etc.
              Window size defaults to length of series.
    :return: timeseries of maximum value

    **Usage**

    Returns the maximum value of the series over each window.

    If :math:`x` is a series:

    :math:`R_t = max(X_{t-w+1}:X_t)`

    where :math:`w` is the size of the rolling window.

    If :math:`x` is an array of series:

    :math:`R_t = max(X_{1, t-w+1}:X_{n, t})`

    where :math:`w` is the size of the rolling window, and :math:`n` is the number of series.

    If window is not provided, returns the maximum value over the full series. If the window size is greater than the
    available data, will return maximum of available values.

    **Examples**

    Maximum value of price series over the last :math:`22` observations:

    >>> prices = generate_series(100)
    >>> max_(prices, 22)

    **See also**

    :func:`min_`

    """
    if isinstance(x, list):
        x = _concat_series(x).max(axis=1)
    w = normalize_window(x, w)
    assert x.index.is_monotonic_increasing, "series index is monotonic increasing"
    if isinstance(w.w, pd.DateOffset):
        values = [x.loc[(x.index > idx - w.w) & (x.index <= idx)].max() for idx in x.index]
        return apply_ramp(pd.Series(values, index=x.index, dtype=np.dtype(float)), w)
    else:
        return apply_ramp(x.rolling(w.w, 0).max(), w)


@plot_function
def range_(x: pd.Series, w: Union[Window, int, str] = Window(None, 0)) -> pd.Series:
    """
    Range of series over given window

    :param x: series: timeseries
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value.  If w is a string, it should be a relative date like '1m', '1d', etc.
              Window size defaults to length of series.
    :return: timeseries of range

    **Usage**

    Returns the range of the series (max - min) over rolling window:

    :math:`R_t = max(X_{t-w+1}:X_t) - min(X_{t-w+1}:X_t)`

    where :math:`w` is the size of the rolling window. If window is not provided, returns the range over the
    full series. If the window size is greater than the available data, will return range of all available values.

    **Examples**

    Range of price series over the last :math:`22` observations:

    >>> prices = generate_series(100)
    >>> range_(prices, 22)

    **See also**

    :func:`min_` :func:`max_`

    """
    w = normalize_window(x, w)
    assert x.index.is_monotonic_increasing, "series index is monotonic increasing"

    max = max_(x, Window(w.w, 0))
    min = min_(x, Window(w.w, 0))

    return apply_ramp(max - min, w)


@plot_function
def mean(x: Union[pd.Series, List[pd.Series]], w: Union[Window, int, str] = Window(None, 0)) -> pd.Series:
    """
    Arithmetic mean of series over given window

    :param x: series: a timeseries or an array of timeseries
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value.  If w is a string, it should be a relative date like '1m', '1d', etc.
              Window size defaults to length of series.
    :return: timeseries of mean value

    **Usage**

    Calculates `arithmetic mean <https://en.wikipedia.org/wiki/Arithmetic_mean>`_ of the series over a rolling window

    If a timeseries is provided:

    :math:`R_t = \\frac{\sum_{i=t-w+1}^{t} X_i}{N}`

    where :math:`N` is the number of observations in each rolling window, :math:`w`.

    If an array of timeseries is provided:

    :math:`R_t = \\frac{\sum_{i=t-w+1}^{t} {\sum_{j=1}^{n}} X_{ij}}{N}`

    where :math:`n` is the number of series, and :math:`N` is the number of observations in each rolling window,
    :math:`w`.

    If window is not provided, computes rolling mean over the full series. If the window size is greater than the
    available data, will return mean of available values.

    **Examples**

    Generate price series and compute mean over :math:`22` observations

    >>> prices = generate_series(100)
    >>> mean(prices, 22)

    **See also**

    :func:`median` :func:`mode`

    """
    if isinstance(x, list):
        x = pd.concat(x, axis=1)
    w = normalize_window(x, w)
    assert x.index.is_monotonic_increasing, "series index is monotonic increasing"
    if isinstance(w.w, pd.DateOffset):
        values = [np.nanmean(x.loc[(x.index > idx - w.w) & (x.index <= idx)]) for idx in x.index]
    else:
        values = [np.nanmean(x.iloc[max(idx - w.w + 1, 0): idx + 1]) for idx in range(0, len(x))]
    return apply_ramp(pd.Series(values, index=x.index, dtype=np.dtype(float)), w)


@plot_function
def median(x: pd.Series, w: Union[Window, int, str] = Window(None, 0)) -> pd.Series:
    """
    Median value of series over given window

    :param x: series: timeseries
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value.  If w is a string, it should be a relative date like '1m', '1d', etc.
              Window size defaults to length of series.
    :return: timeseries of median value

    **Usage**

    Computes the `median <https://en.wikipedia.org/wiki/Median>`_ value over a given window. For each window, this
    function will return the middle value when all elements in the window are sorted. If the number of observations in
    the window is even, will return the average of the middle two values. If the window size is greater than the
    available data, will return median of available values:

    :math:`d = \\frac{w-1}{2}`

    :math:`R_t = \\frac{X_{\lfloor t-d \\rfloor} + X_{\lceil t-d \\rceil}}{2}`

    where :math:`w` is the size of the rolling window. If window is not provided, computes median over the full series

    **Examples**

    Generate price series and compute median over :math:`22` observations

    >>> prices = generate_series(100)
    >>> median(prices, 22)

    **See also**

    :func:`mean` :func:`mode`
    """
    w = normalize_window(x, w)
    assert x.index.is_monotonic_increasing, "series index is monotonic increasing"
    if isinstance(w.w, pd.DateOffset):
        values = [x.loc[(x.index > idx - w.w) & (x.index <= idx)].median() for idx in x.index]
        return apply_ramp(pd.Series(values, index=x.index, dtype=np.dtype(float)), w)
    else:
        return apply_ramp(x.rolling(w.w, 0).median(), w)


@plot_function
def mode(x: pd.Series, w: Union[Window, int, str] = Window(None, 0)) -> pd.Series:
    """
    Most common value in series over given window

    :param x: series: timeseries
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value.  If w is a string, it should be a relative date like '1m', '1d', etc.
              Window size defaults to length of series.
    :return: timeseries of mode value

    **Usage**

    Computes the `mode <https://en.wikipedia.org/wiki/Mode_(statistics)>`_ over a given window. For each window, this
    function will return the most common value of all elements in the window. If there are multiple values with the same
    frequency of occurrence, will return the smallest value.

    If window is not provided, computes mode over the full series.

    **Examples**

    Generate price series and compute mode over :math:`22` observations

    >>> prices = generate_series(100)
    >>> mode(prices, 22)

    **See also**

    :func:`mean` :func:`median`
    """
    w = normalize_window(x, w)
    assert x.index.is_monotonic_increasing, "series index is monotonic increasing"
    if isinstance(w.w, pd.DateOffset):
        values = [stats.mode(x.loc[(x.index > idx - w.w) & (x.index <= idx)]).mode[0] for idx in x.index]
        return apply_ramp(pd.Series(values, index=x.index, dtype=np.dtype(float)), w)
    else:
        return apply_ramp(x.rolling(w.w, 0).apply(lambda y: stats.mode(y).mode, raw=True), w)


@plot_function
def sum_(x: Union[pd.Series, List[pd.Series]], w: Union[Window, int, str] = Window(None, 0)) -> pd.Series:
    """
    Rolling sum of series over given window

    :param x: series: a timeseries or an array of timeseries
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value.  If w is a string, it should be a relative date like '1m', '1d', etc.
              Window size defaults to length of series.
    :return: timeseries of rolling sum

    **Usage**

    Calculate the sum of observations over a given rolling window.

    If :math:`x` is a series:

    :math:`R_t = \sum_{i=t-w+1}^{t} X_i`

    where :math:`w` is the size of the rolling window.

    If :math:`x` is an array of series:

    :math:`R_t = \sum_{i=t-w+1}^{t} \sum_{j=1}^{n} X_{ij}`

    where :math:`w` is the size of the rolling window and :math:`n` is the number of series

    If window is not provided, computes sum over the full series. If the window size is greater than the available data,
    will return sum of available values.

    **Examples**

    Generate price series and compute rolling sum over :math:`22` observations

    >>> prices = generate_series(100)
    >>> sum_(prices, 22)

    **See also**

    :func:`product`

    """
    if isinstance(x, list):
        x = pd.concat(x, axis=1).sum(axis=1)
    w = normalize_window(x, w)
    assert x.index.is_monotonic_increasing
    if isinstance(w.w, pd.DateOffset):
        values = [x.loc[(x.index > idx - w.w) & (x.index <= idx)].sum() for idx in x.index]
        return apply_ramp(pd.Series(values, index=x.index, dtype=np.dtype(float)), w)
    else:
        return apply_ramp(x.rolling(w.w, 0).sum(), w)


@plot_function
def product(x: pd.Series, w: Union[Window, int, str] = Window(None, 0)) -> pd.Series:
    """
    Rolling product of series over given window

    :param x: series: timeseries
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value.  If w is a string, it should be a relative date like '1m', '1d', etc.
              Window size defaults to length of series.
    :return: timeseries of rolling product

    **Usage**

    Calculate the product of observations over a given rolling window. For each time, :math:`t`, returns the value
    of all observations from :math:`t-w+1` to :math:`t` multiplied together:

    :math:`R_t = \prod_{i=t-w+1}^{t} X_i`

    where :math:`w` is the size of the rolling window. If window is not provided, computes product over the full series

    **Examples**

    Generate price series and compute rolling sum over :math:`22` observations

    >>> prices = generate_series(100)
    >>> product(1+returns(prices))

    **See also**

    :func:`sum_`
    """
    w = normalize_window(x, w)
    assert x.index.is_monotonic_increasing
    if isinstance(w.w, pd.DateOffset):
        values = [x.loc[(x.index > idx - w.w) & (x.index <= idx)].agg(pd.Series.prod) for idx in x.index]
        return apply_ramp(pd.Series(values, index=x.index, dtype=np.dtype(float)), w)
    else:
        return apply_ramp(x.rolling(w.w, 0).agg(pd.Series.prod), w)


@plot_function
def std(x: pd.Series, w: Union[Window, int, str] = Window(None, 0)) -> pd.Series:
    """
    Rolling standard deviation of series over given window

    :param x: series: timeseries
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value.  If w is a string, it should be a relative date like '1m', '1d', etc.
              Window size defaults to length of series.
    :return: timeseries of standard deviation

    **Usage**

    Provides `unbiased estimator <https://en.wikipedia.org/wiki/Unbiased_estimation_of_standard_deviation>`_ of sample
    `standard deviation <https://en.wikipedia.org/wiki/Standard_deviation>`_ over a rolling window:

    :math:`R_t = \sqrt{\\frac{1}{N-1} \sum_{i=t-w+1}^t (X_i - \overline{X_t})^2}`

    where :math:`N` is the number of observations in each rolling window, :math:`w`, and :math:`\overline{X_t}` is the
    mean value over the same window:

    :math:`\overline{X_t} = \\frac{\sum_{i=t-w+1}^{t} X_i}{N}`

    If window is not provided, computes standard deviation over the full series

    **Examples**

    Generate price series and compute standard deviation of returns over :math:`22` observations

    >>> prices = generate_series(100)
    >>> std(returns(prices), 22)

    **See also**

    :func:`sum` :func:`mean` :func:`var`

    """
    w = normalize_window(x, w)
    assert x.index.is_monotonic_increasing, "series index is monotonic increasing"
    if isinstance(w.w, pd.DateOffset):
        values = [x.loc[(x.index > idx - w.w) & (x.index <= idx)].std() for idx in x.index]
        return apply_ramp(pd.Series(values, index=x.index, dtype=np.dtype(float)), w)
    else:
        return apply_ramp(x.rolling(w.w, 0).std(), w)


@plot_function
def exponential_std(x: pd.Series, beta: float = 0.75) -> pd.Series:
    """
    Exponentially weighted standard deviation

    :param x: time series
    :param beta: how much to weigh the previous price in the time series, thus controlling how much importance we
                  place on the (more distant) past. Must be between 0 (inclusive) and 1 (exclusive)
    :return: time series of standard deviation of the input series

    **Usage**

    Provides an unbiased estimator of `exponentially weighted standard deviation
    <https://en.wikipedia.org/wiki/Moving_average#Exponentially_weighted_moving_variance_and_standard_deviation>`_ of
    a series [:math:`X_0`, :math:`X_1`, :math:`X_2`, ...]:

    :math:`S_t = \\sqrt{[EWMA(X_t^2) - EWMA(X_t)^2] * DF_t}`

    where :math:`EWMA(X_t)` is the `exponential moving average
    <https://en.wikipedia.org/wiki/Moving_average#Exponential_moving_average>`_ at :math:`t` (see function
    :func:`exponential_moving_average`), :math:`DF_t` is the debiasing factor (see
    `Weighted sample variance <https://en.wikipedia.org/wiki/Weighted_arithmetic_mean#Weighted_sample_variance>`_
    for further details):

    :math:`DF_t = \\frac{(\sum_{i=0}^t w_i)^2} {(\sum_{i=0}^t w_i)^2 - \sum_{i=0}^t w_i^2}`

    where :math:`w_i` is the weight assigned to :math:`i` th observation:

    :math:`w_i = (1-\\beta)\\beta^i` for i<t; :math:`\\beta^i` for i=t

    **Examples**

    Generate price series and compute exponentially weighted standard deviation of returns

    >>> prices = generate_series(100)
    >>> exponential_std(returns(prices), 0.9)

    **See also**

    :func:`std` :func:`var` :func:`exponential_moving_average`

    """
    return x.ewm(alpha=1 - beta, adjust=False).std()


@plot_function
def var(x: pd.Series, w: Union[Window, int, str] = Window(None, 0)) -> pd.Series:
    """
    Rolling variance of series over given window

    :param x: series: timeseries
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value.  If w is a string, it should be a relative date like '1m', '1d', etc.
              Window size defaults to length of series.
    :return: timeseries of variance

    **Usage**

    Provides `unbiased estimator <https://en.wikipedia.org/wiki/Unbiased_estimation_of_standard_deviation>`_ of sample
    `variance <https://en.wikipedia.org/wiki/Variance>`_ over a rolling window:

    :math:`R_t = \\frac{1}{N-1} \sum_{i=t-w+1}^t (X_i - \overline{X_t})^2`

    where :math:`N` is the number of observations in each rolling window, :math:`w`, and :math:`\overline{X_t}` is the
    mean value over the same window:

    :math:`\overline{X_t} = \\frac{\sum_{i=t-w+1}^{t} X_i}{N}`

    If window is not provided, computes variance over the full series

    **Examples**

    Generate price series and compute variance of returns over :math:`22` observations

    >>> prices = generate_series(100)
    >>> var(returns(prices), 22)

    **See also**

    :func:`var` :func:`mean` :func:`std`

    """
    w = normalize_window(x, w)
    assert x.index.is_monotonic_increasing, "series index is monotonic increasing"
    if isinstance(w.w, pd.DateOffset):
        values = [x.loc[(x.index > idx - w.w) & (x.index <= idx)].var() for idx in x.index]
        return apply_ramp(pd.Series(values, index=x.index, dtype=np.dtype(float)), w)
    else:
        return apply_ramp(x.rolling(w.w, 0).var(), w)


@plot_function
def cov(x: pd.Series, y: pd.Series, w: Union[Window, int, str] = Window(None, 0)) -> pd.Series:
    """
    Rolling co-variance of series over given window

    :param x: series: timeseries
    :param y: series: timeseries
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value.  If w is a string, it should be a relative date like '1m', '1d', etc.
              Window size defaults to length of series.
    :return: timeseries of covariance

    **Usage**

    Provides `unbiased estimator <https://en.wikipedia.org/wiki/Unbiased_estimation_of_standard_deviation>`_ of sample
    `co-variance <https://en.wikipedia.org/wiki/Covariance>`_ over a rolling window:

    :math:`R_t = \\frac{1}{N-1} \sum_{i=t-w+1}^t (X_i - \overline{X_t}) (Y_i - \overline{Y_t})`

    where :math:`N` is the number of observations in each rolling window, :math:`w`, and :math:`\overline{X_t}` and
    :math:`\overline{Y_t}` represent the sample mean of series :math:`X_t` and :math:`Y_t` over the same window:

    :math:`\overline{X_t} = \\frac{\sum_{i=t-w+1}^{t} X_i}{N}` and
    :math:`\overline{Y_t} = \\frac{\sum_{i=t-w+1}^{t} Y_i}{N}`

    If window is not provided, computes variance over the full series

    **Examples**

    Generate price series and compute variance of returns over :math:`22` observations

    >>> prices_x = generate_series(100)
    >>> prices_y = generate_series(100)
    >>> cov(returns(prices_x) returns(prices_y), 22)

    **See also**

    :func:`sum` :func:`mean` :func:`var`
    """
    w = normalize_window(x, w)
    assert x.index.is_monotonic_increasing, "series index is monotonic increasing"
    if isinstance(w.w, pd.DateOffset):
        values = [x.loc[(x.index > idx - w.w) & (x.index <= idx)].cov(y) for idx in x.index]
        return apply_ramp(pd.Series(values, index=x.index, dtype=np.dtype(float)), w)
    else:
        return apply_ramp(x.rolling(w.w, 0).cov(y), w)


def _zscore(x):
    if x.size == 1:
        return 0

    return stats.zscore(x, ddof=1)[-1]


@plot_function
def zscores(x: pd.Series, w: Union[Window, int, str] = Window(None, 0)) -> pd.Series:
    """
    Rolling z-scores over a given window

    :param x: time series of prices
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value.  If w is a string, it should be a relative date like '1m', '1d', etc.
              Window size defaults to length of series.
    :return: timeseries of z-scores

    **Usage**

    Calculate `standard score <https://en.wikipedia.org/wiki/Standard_score>`_ of each value in series over given
    window. Standard deviation and sample mean are computed over the specified rolling window, then element is
    normalized to provide a rolling z-score:

    :math:`R_t = \\frac { X_t - \mu }{ \sigma }`

    Where :math:`\mu` and :math:`\sigma` are sample mean and standard deviation over the given window

    If window is not provided, computes z-score relative to mean and standard deviation over the full series

    **Examples**

    Generate price series and compute z-score of returns over :math:`22` observations

    >>> prices = generate_series(100)
    >>> zscores(returns(prices), 22)

    **See also**

    :func:`mean` :func:`std`

    """
    if x.size < 1:
        return x

    if isinstance(w, int):
        w = normalize_window(x, w)
    elif isinstance(w, str):
        if not (isinstance(x.index, pd.DatetimeIndex) or isinstance(x.index[0], datetime.date)):
            raise MqValueError("When string is passed window index must be a DatetimeIndex or of type datetime.date")
        w = normalize_window(x, w)
    if not w.w:
        if x.size == 1:
            return pd.Series([0.0], index=x.index, dtype=np.dtype(float))

        clean_series = x.dropna()
        zscore_series = pd.Series(stats.zscore(clean_series, ddof=1), clean_series.index, dtype=np.dtype(float))
        return interpolate(zscore_series, x, Interpolate.NAN)
    if not isinstance(w.w, int):
        w = normalize_window(x, w)
        values = [_zscore(x.loc[(x.index > idx - w.w) & (x.index <= idx)]) for idx in x.index]
        return apply_ramp(pd.Series(values, index=x.index, dtype=np.dtype(float)), w)
    else:
        return apply_ramp(x.rolling(w.w, 0).apply(_zscore, raw=False), w)


@plot_function
def winsorize(x: pd.Series, limit: float = 2.5, w: Union[Window, int, str] = Window(None, 0)) -> pd.Series:
    """
    Limit extreme values in series

    :param x: time series of prices
    :param limit: max z-score of values
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value.  If w is a string, it should be a relative date like '1m', '1d', etc.
              Window size defaults to length of series.
    :return: timeseries of winsorized values

    **Usage**

    Cap and floor values in the series which have a z-score greater or less than provided value. This function will
    restrict the distribution of values. Calculates the sample standard deviation and adjusts values which
    fall outside the specified range to be equal to the upper or lower limits

    Lower and upper limits are defined as:

    :math:`upper = \mu + \sigma \\times limit`

    :math:`lower = \mu - \sigma \\times limit`

    Where :math:`\mu` and :math:`\sigma` are sample mean and standard deviation. The series is restricted by:

    :math:`R_t = max( min( X_t, upper), lower )`

    See `winsorising <https://en.wikipedia.org/wiki/Winsorizing>`_ for additional information

    **Examples**

    Generate price series and winsorize z-score of returns over :math:`22` observations

    >>> prices = generate_series(100)
    >>> winsorize(zscore(returns(prices), 22))

    **See also**

    :func:`zscore` :func:`mean` :func:`std`

    """
    w = normalize_window(x, w)

    if x.size < 1:
        return x

    assert w.w, "window is not 0"

    mu = x.mean()
    sigma = x.std()

    high = mu + sigma * limit
    low = mu - sigma * limit

    ret = ceil(x, high)
    ret = floor(ret, low)

    return apply_ramp(ret, w)


@plot_function
def generate_series(length: int) -> pd.Series:
    """
    Generate sample timeseries

    :param length: number of observations
    :return: date-based time series of randomly generated prices

    **Usage**

    Create timeseries from returns generated from a normally distributed random variables (IDD). Length determines the
    number of observations to be generated.

    Assume random variables :math:`R` which follow a normal distribution with mean :math:`0` and standard deviation
    of :math:`1`

    :math:`R \sim N(0, 1)`

    The timeseries is generated from these random numbers through:

    :math:`X_t = (1 + R)X_{t-1}`

    **Examples**

    Generate price series with 100 observations starting from today's date:

    >>> prices = generate_series(100)

    **See also**

    :func:`numpy.random.normal()`

    """
    levels = [100]
    dates = [datetime.date.today()]

    for i in range(length - 1):
        levels.append(levels[i] * 1 + numpy.random.normal())
        dates.append(datetime.date.fromordinal(dates[i].toordinal() + 1))

    return pd.Series(data=levels, index=dates, dtype=np.dtype(float))


@plot_function
def percentiles(x: pd.Series, y: pd.Series = None, w: Union[Window, int, str] = Window(None, 0)) -> pd.Series:
    """
    Rolling percentiles over given window

    :param x: value series
    :param y: distribution series
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value.  If w is a string, it should be a relative date like '1m', '1d', etc.
              Window size defaults to length of series.
    :return: timeseries of percentiles

    **Usage**

    Calculate `percentile rank <https://en.wikipedia.org/wiki/Percentile_rank>`_ of :math:`y` in the sample distribution
    of :math:`x` over a rolling window of length :math:`w`:

    :math:`R_t = \\frac{\sum_{i=t-N+1}^{t}{[X_i<{Y_t}]}+0.5\sum_{i=t-N+1}^{t}{[X_i={Y_t}]}}{N}\\times100\%`

    Where :math:`N` is the number of observations in a rolling window. If :math:`y` is not provided, calculates
    percentiles of :math:`x` over its historical values. If window length :math:`w` is not provided, uses an
    ever-growing history of values. If :math:`w` is greater than the available data size, returns empty.

    **Examples**

    Compute percentile ranks of a series in the sample distribution of a second series over :math:`22` observations

    >>> a = generate_series(100)
    >>> b = generate_series(100)
    >>> percentiles(a, b, 22)

    **See also**

    :func:`zscores`

    """
    w = normalize_window(x, w)
    if x.empty:
        return x

    if y is None:
        y = x.copy()

    if isinstance(w.r, int) and w.r > len(y):
        raise ValueError('Ramp value must be less than the length of the series y.')

    if isinstance(w.w, int) and w.w > len(x):
        return pd.Series()

    res = pd.Series(dtype=np.dtype(float))
    for idx, val in y.iteritems():
        sample = x.loc[(x.index > idx - w.w) & (x.index <= idx)] if isinstance(w.w, pd.DateOffset) else x[:idx][-w.w:]
        res.loc[idx] = percentileofscore(sample, val, kind='mean')

    if isinstance(w.r, pd.DateOffset):
        return res.loc[res.index[0] + w.r:]
    else:
        return res[w.r:]


@plot_function
def percentile(x: pd.Series, n: float, w: Union[Window, int, str] = None) -> Union[pd.Series, float]:
    """
    Returns the nth percentile of a series.

    :param x: series
    :param n: percentile
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value.  If w is a string, it should be a relative date like '1m', '1d', etc.
    :return: nth percentile

    **Usage**

    Calculates the `nth percentile rank <https://en.wikipedia.org/wiki/Percentile_rank>`_ of :math:`x`. Rolling nth
    percentile is returned if a window is specified, else a scalar for nth percentile over the entire series.

    **Example**

    Compute the 90th percentile of a series.

    >>> a = generate_series(100)
    >>> percentile(a, 90)

    """
    if not 0 <= n <= 100:
        raise MqValueError('percentile must be in range [0, 100]')
    x = x.dropna()
    if x.size < 1:
        return x
    if w is None:
        return numpy.percentile(x.values, n)

    n /= 100
    w = normalize_window(x, w)
    if isinstance(w.w, pd.DateOffset):
        try:
            values = [x.loc[(x.index > idx - w.w) & (x.index <= idx)].quantile(n) for idx in x.index]
        except TypeError:
            raise MqTypeError(f'cannot use relative dates with index {x.index}')
        res = pd.Series(values, index=x.index, dtype=np.dtype(float))
    else:
        res = x.rolling(w.w, 0).quantile(n)
    return apply_ramp(res, w)


class LinearRegression:

    """
    Fit an Ordinary least squares (OLS) linear regression model.

    :param X: observations of the explanatory variable(s)
    :param y: observations of the dependant variable
    :param fit_intercept: whether to calculate intercept in the model

    **Usage**

    Fit `OLS Model <https://en.wikipedia.org/wiki/Ordinary_least_squares>`_ based on observations of the explanatory
    variables(s) X and the dependant variable y. If X and y are not aligned, only use the intersection of dates/times

    **Examples**

    R Squared of an OLS model:

    >>> x = generate_series(100)
    >>> y = generate_series(100)
    >>> r = LinearRegression(x, y)
    >>> r.r_squared()

    """

    def __init__(self, X: Union[pd.Series, List[pd.Series]], y: pd.Series, fit_intercept: bool = True):
        df = pd.concat(X, axis=1) if isinstance(X, list) else X.to_frame()
        df = sm.add_constant(df) if fit_intercept else df
        df.columns = range(len(df.columns)) if fit_intercept else range(1, len(df.columns) + 1)

        df = df[~df.isin([np.nan, np.inf, -np.inf]).any(1)]  # filter out nan and inf
        y = y[~y.isin([np.nan, np.inf, -np.inf])]
        df_aligned, y_aligned = df.align(y, 'inner', axis=0)  # align series

        self._index_scope = range(0, len(df.columns)) if fit_intercept else range(1, len(df.columns) + 1)
        self._res = sm.OLS(y_aligned, df_aligned).fit()
        self._fit_intercept = fit_intercept

    @plot_method
    def coefficient(self, i: int) -> float:
        """
        Estimated coefficient

        :param i: coefficient of which predictor to get. If intercept is used, start from 0, else start from 1
        :return: estimated coefficient of the i-th predictor
        """
        return self._res.params[i]

    @plot_method
    def r_squared(self) -> float:
        """
        Coefficient of determination (R Squared)

        :return: R Squared
        """
        return self._res.rsquared

    @plot_method
    def fitted_values(self) -> pd.Series:
        """
        Fitted values

        :return: fitted values
        """
        return self._res.fittedvalues

    @plot_method
    def predict(self, X_predict: Union[pd.Series, List[pd.Series]]) -> pd.Series:
        """
        Use the model for prediction

        :param X_predict: the values for which to predict
        :return: predicted values
        """
        df = pd.concat(X_predict, axis=1) if isinstance(X_predict, list) else X_predict.to_frame()
        return self._res.predict(sm.add_constant(df) if self._fit_intercept else df)

    @plot_method
    def standard_deviation_of_errors(self) -> float:
        """
        Standard deviation of the error term

        :return: standard deviation of the error term
        """
        return np.sqrt(self._res.mse_resid)


class RollingLinearRegression:

    """
    Fit a rolling ordinary least squares (OLS) linear regression model.

    :param X: observations of the explanatory variable(s)
    :param y: observations of the dependant variable
    :param w: number of observations in each rolling window. Must be larger than the number of observations or
              explanatory variables
    :param fit_intercept: whether to calculate intercept in the model

    **Usage**

    Fit `OLS Model <https://en.wikipedia.org/wiki/Ordinary_least_squares>`_ based on observations of the explanatory
    variables(s) X and the dependant variable y across a rolling window with fixed number of observations.
    The parameters of each rolling window are stored at the end of each window.
    If X and y are not aligned, only use the intersection of dates/times

    **Examples**

    R Squared of a rolling OLS model:

    >>> x = generate_series(100)
    >>> y = generate_series(100)
    >>> r = RollingLinearRegression(x, y, 5)
    >>> r.r_squared()

    """

    def __init__(self, X: Union[pd.Series, List[pd.Series]], y: pd.Series, w: int, fit_intercept: bool = True):
        df = pd.concat(X, axis=1) if isinstance(X, list) else X.to_frame()
        df = sm.add_constant(df) if fit_intercept else df
        df.columns = range(len(df.columns)) if fit_intercept else range(1, len(df.columns) + 1)

        if w <= len(df.columns):
            raise MqValueError('Window length must be larger than the number of explanatory variables')

        df = df[~df.isin([np.nan, np.inf, -np.inf]).any(1)]  # filter out nan and inf
        y = y[~y.isin([np.nan, np.inf, -np.inf])]
        df_aligned, y_aligned = df.align(y, 'inner', axis=0)  # align series

        self._X = df_aligned.copy()
        self._res = RollingOLS(y_aligned, df_aligned, w).fit()

    @plot_method
    def coefficient(self, i: int) -> pd.Series:
        """
        Estimated coefficients

        :param i: coefficients of which predictor to get. If intercept is used, start from 0, else start from 1
        :return: estimated coefficients of the i-th predictor
        """
        return self._res.params[i]

    @plot_method
    def r_squared(self) -> pd.Series:
        """
        Coefficients of determination (R Squared) of rolling regressions

        :return: R Squared
        """
        return self._res.rsquared

    @plot_method
    def fitted_values(self) -> pd.Series:
        """
        Fitted values at the end of each rolling window

        :return: fitted values
        """
        comp = self._X.mul(self._res.params.values)
        return comp.sum(axis=1, min_count=len(comp.columns))

    @plot_method
    def standard_deviation_of_errors(self) -> pd.Series:
        """
        Standard deviations of the error terms

        :return: standard deviations of the error terms
        """
        return np.sqrt(self._res.mse_resid)


class SIRModel:

    """SIR Compartmental model for transmission of infectious disease

    :param beta: transmission rate of the infection
    :param gamma: recovery rate of the infection
    :param s: number of susceptible individuals in population
    :param i: number of infectious individuals in population
    :param r: number of recovered individuals in population
    :param n: total population size
    :param end_date: end date for the evolution of the model
    :param fit: whether to fit the model to the data
    :param fit_period: on how many days back to fit the model

    **Usage**

    Fit `SIR Model <https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology#The_SIR_model>`_ based on the
    population in each compartment over a given time period.

    The SIR models the movement of individuals between three compartments: susceptible (S), infected (I), and resistant
    (R). The model calibrates parameters :

    ===========   =======================================================
    Parameter     Description
    ===========   =======================================================
    S0            initial susceptible individuals
    I0            initial infected individuals
    R0            initial recovered individuals
    beta          Transmission rate from susceptible to infected
    gamma         Immunity rate from infected to resistant
    ===========   =======================================================

    The parameters beta and gamma model how fast people move from being susceptible to infected (beta), and
    subsequently from infected to resistant (gamma). This model can be used to forecast the populations of each
    compartment once calibrated

    """
    def __init__(self, beta: float = None, gamma: float = None, s: Union[pd.Series, float] = None,
                 i: Union[pd.Series, float] = None, r: Union[pd.Series, float] = None,
                 n: Union[pd.Series, float] = None, fit: bool = True,
                 fit_period: int = None):
        n = n.dropna()[0] if isinstance(n, pd.Series) else n
        n = 100 if n is None else n
        fit = False if s is None and i is None and r is None else fit
        s = n if s is None else s
        i = 1 if i is None else i
        r = 0 if r is None else r

        data_start = [ts.index.min().date() for ts in [s, i, r] if isinstance(ts, pd.Series)]
        data_start.append(DataContext.current.start_date)
        start_date = max(data_start)

        data_end = [ts.index.max().date() for ts in [s, i, r] if isinstance(ts, pd.Series)]
        data_end.append(DataContext.current.end_date)
        end_date = max(data_end)

        self.s = s if isinstance(s, pd.Series) else [s]
        self.i = i if isinstance(i, pd.Series) else [i]
        self.r = r if isinstance(r, pd.Series) else [r]
        self.n = n
        self.beta_init = beta
        self.gamma_init = gamma
        self.fit = fit
        self.fit_period = fit_period
        self.beta_fixed = not (self.fit or (self.beta_init is None))
        self.gamma_fixed = not (self.fit or (self.gamma_init is None))

        data = np.array([self.s, self.i, self.r]).T

        beta_init = self.beta_init if self.beta_init is not None else 0.9
        gamma_init = self.gamma_init if self.gamma_init is not None else 0.01

        parameters, initial_conditions = SIR.get_parameters(self.s[0], self.i[0], self.r[0], n, beta=beta_init,
                                                            gamma=gamma_init, beta_fixed=self.beta_fixed,
                                                            gamma_fixed=self.gamma_fixed, S0_fixed=True, I0_fixed=True,
                                                            R0_fixed=True)
        self.parameters = parameters

        self._model = EpidemicModel(SIR, parameters=parameters, data=data, initial_conditions=initial_conditions,
                                    fit_period=self.fit_period)
        if self.fit:
            self._model.fit(verbose=False)

        t = np.arange((end_date - start_date).days + 1)
        predict = self._model.solve(t, (self.s0(), self.i0(), self.r0()), (self.beta(), self.gamma(), n))

        predict_dates = pd.date_range(start_date, end_date)

        self._model.s_predict = pd.Series(predict[:, 0], predict_dates)
        self._model.i_predict = pd.Series(predict[:, 1], predict_dates)
        self._model.r_predict = pd.Series(predict[:, 2], predict_dates)

    @plot_method
    def s0(self) -> float:
        """
        Model calibration for initial susceptible individuals

        :return: initial susceptible individuals
        """
        if self.fit:
            return self._model.fitted_parameters['S0']
        return self.parameters['S0'].value

    @plot_method
    def i0(self) -> float:
        """
        Model calibration for initial infectious individuals

        :return: initial infectious individuals
        """
        if self.fit:
            return self._model.fitted_parameters['I0']
        return self.parameters['I0'].value

    @plot_method
    def r0(self) -> float:
        """
        Model calibration for initial recovered individuals

        :return: initial recovered individuals
        """
        if self.fit:
            return self._model.fitted_parameters['R0']
        return self.parameters['R0'].value

    @plot_method
    def beta(self) -> float:
        """
        Model calibration for transmission rate (susceptible to infected)

        :return: beta
        """
        if self.fit:
            return self._model.fitted_parameters['beta']
        return self.parameters['beta'].value

    @plot_method
    def gamma(self) -> float:
        """
        Model calibration for immunity (infected to resistant)

        :return: beta
        """
        if self.fit:
            return self._model.fitted_parameters['gamma']
        return self.parameters['gamma'].value

    @plot_method
    def predict_s(self) -> pd.Series:
        """
        Model calibration for susceptible individuals through time

        :return: susceptible predict
        """
        return self._model.s_predict

    @plot_method
    def predict_i(self) -> pd.Series:
        """
        Model calibration for infected individuals through time

        :return: infected predict
        """
        return self._model.i_predict

    @plot_method
    def predict_r(self) -> pd.Series:
        """
        Model calibration for recovered individuals through time

        :return: infected predict
        """
        return self._model.r_predict


class SEIRModel(SIRModel):

    """SEIR Compartmental model for transmission of infectious disease

    :param beta: transmission rate of the infection
    :param gamma: recovery rate of the infection
    :param sigma: immunity rate from exposed to infected
    :param s: number of susceptible individuals in population
    :param e: number of exposed individuals in population
    :param i: number of infectious individuals in population
    :param r: number of recovered individuals in population
    :param n: total population size
    :param end_date: end date for the evolution of the model
    :param fit: whether to fit the model to the data
    :param fit_period: on how many days back to fit the model

    **Usage**

    Fit `SEIR Model <https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology#The_SEIR_model>`_ based on the
    population in each compartment over a given time period.

    The SEIR models the movement of individuals between four compartments: susceptible (S), exposed (E), infected (I),
    and resistant (R). The model calibrates parameters :

    ===========   =======================================================
    Parameter     Description
    ===========   =======================================================
    S0            initial susceptible individuals
    E0            initial exposed individuals
    I0            initial infected individuals
    R0            initial recovered individuals
    beta          Transmission rate from susceptible to exposed
    gamma         Immunity rate from infected to resistant
    sigma         Immunity rate from exposed to infected
    ===========   =======================================================

    The parameters beta, gamma, and sigma, model how fast people move from being susceptible to exposed (beta),
    from exposed to infected (sigma), and subsequently from infected to resistant (gamma). This model can be used to
    predict the populations of each compartment once calibrated.

    """
    def __init__(self, beta: float = None, gamma: float = None, sigma: float = None, s: Union[pd.Series, float] = None,
                 e: Union[pd.Series, float] = None, i: Union[pd.Series, float] = None,
                 r: Union[pd.Series, float] = None, n: Union[pd.Series, float] = None,
                 fit: bool = True, fit_period: int = None):
        n = n.dropna()[0] if isinstance(n, pd.Series) else n
        n = 100 if n is None else n
        fit = False if all(state is None for state in (s, e, i, r)) else fit
        s = n if s is None else s
        e = 1 if e is None else e
        i = 1 if i is None else i
        r = 0 if r is None else r

        data_start = [ts.index.min().date() for ts in [s, i, r] if isinstance(ts, pd.Series)]
        data_start.append(DataContext.current.start_date)
        start_date = max(data_start)

        data_end = [ts.index.max().date() for ts in [s, i, r] if isinstance(ts, pd.Series)]
        data_end.append(DataContext.current.end_date)
        end_date = max(data_end)

        self.s = s if isinstance(s, pd.Series) else [s]
        self.e = e if isinstance(e, pd.Series) else [e]
        self.i = i if isinstance(i, pd.Series) else [i]
        self.r = r if isinstance(r, pd.Series) else [r]
        self.n = n
        self.beta_init = beta
        self.gamma_init = gamma
        self.sigma_init = sigma
        self.fit = fit
        self.fit_period = fit_period
        self.beta_fixed = not (self.fit or (self.beta is None))
        self.gamma_fixed = not (self.fit or (self.gamma is None))
        self.sigma_fixed = not (self.fit or (self.sigma is None))

        data = np.array([self.s, self.e, self.i, self.r]).T

        beta_init = self.beta_init if self.beta_init is not None else 0.9
        gamma_init = self.gamma_init if self.gamma_init is not None else 0.01
        sigma_init = self.sigma_init if self.sigma_init is not None else 0.2

        parameters, initial_conditions = SEIR.get_parameters(self.s[0], self.e[0], self.i[0], self.r[0], n,
                                                             beta=beta_init, gamma=gamma_init, sigma=sigma_init,
                                                             beta_fixed=self.beta_fixed,
                                                             gamma_fixed=self.gamma_fixed,
                                                             sigma_fixed=self.sigma_fixed,
                                                             S0_fixed=True, I0_fixed=True,
                                                             R0_fixed=True, E0_fixed=True, S0_max=5e6, I0_max=5e6,
                                                             E0_max=10e6, R0_max=10e6)
        self.parameters = parameters

        self._model = EpidemicModel(SEIR, parameters=parameters, data=data, initial_conditions=initial_conditions,
                                    fit_period=self.fit_period)
        if self.fit:
            self._model.fit(verbose=False)

        t = np.arange((end_date - start_date).days + 1)
        predict = self._model.solve(t, (self.s0(), self.e0(), self.i0(), self.r0()),
                                    (self.beta(), self.gamma(), self.sigma(), n))

        predict_dates = pd.date_range(start_date, end_date)

        self._model.s_predict = pd.Series(predict[:, 0], predict_dates)
        self._model.e_predict = pd.Series(predict[:, 1], predict_dates)
        self._model.i_predict = pd.Series(predict[:, 2], predict_dates)
        self._model.r_predict = pd.Series(predict[:, 3], predict_dates)

    @plot_method
    def e0(self) -> float:
        """
        Model calibration for initial exposed individuals

        :return: initial exposed individuals
        """
        if self.fit:
            return self._model.fitted_parameters['E0']
        return self.parameters['E0'].value

    @plot_method
    def beta(self) -> float:
        """
        Model calibration for transmission rate (susceptible to exposed)

        :return: beta
        """
        if self.fit:
            return self._model.fitted_parameters['beta']
        return self.parameters['beta'].value

    @plot_method
    def gamma(self) -> float:
        """
        Model calibration for immunity (infected to resistant)

        :return: gamma
        """
        if self.fit:
            return self._model.fitted_parameters['gamma']
        return self.parameters['gamma'].value

    @plot_method
    def sigma(self) -> float:
        """
        Model calibration for infection rate (exposed to infected)

        :return: sigma
        """
        if self.fit:
            return self._model.fitted_parameters['sigma']
        return self.parameters['sigma'].value

    @plot_method
    def predict_e(self) -> pd.Series:
        """
        Model calibration for exposed individuals through time

        :return: exposed predict
        """
        return self._model.e_predict


DateRange = namedtuple('DateRange', ['start', 'end'])


def recurrence_parallel_score(args):
    """
    Function to feed to the Multiprocessing Pool in calcualting the similarity
    score between two time series.
    """
    curr_period_ts, recurrence_ts, factor, recurr_daterange, metric = args
    score = metric(curr_period_ts, recurrence_ts)
    return '{}_{}'.format(factor, recurr_daterange), score


def cummulative_pct_change(ts) -> float:
    """
    Function that calculates cummulative pct_change of series

    :param ts: pd.Series or list
    """
    ts = list(ts)

    if ts[0] == 0:  # deal with first value is 0
        if ts[-1] > ts[0]:
            pct_change = 1.0
        elif ts[-1] < ts[0]:
            pct_change = -1.0
        else:
            pct_change = 0.0
    else:
        pct_change = (ts[-1] - ts[0])/ts[0]

    return pct_change * 100


def dtw_metric(a, b):
    """
    Function that calculates the DTW similarity between two time series

    :param a: time series a
    :param b: time series b
    """

    if np.unique(a).size == 1 or np.unique(b).size == 1:
        return np.nan

    a = np.array(a)
    b = np.array(b)

    a = (a - a.mean())/a.std()
    b = (b - b.mean())/b.std()

    score = dtw.distance_fast(a, b)

    return score if score != np.inf or score != -np.inf else np.nan


class GS_Recurrence():
    """
    Finds historically similar time periods given a handful of time series,
    a similarity metric, query start/end date (time period to compare all
    other periods against of the same length), and various other parameters.

    :param df: the original Pandas Dataframe to feed to the model. Requires
               index as dates and columns as time series. Only supports daily
               data.

    **Examples**

    >>> query_start = datetime.date(2020, 3, 20)
    >>> query_end = datetime.date(2020, 9, 4)

    >>> GS_Recurr = GS_Recurrence(clean_df)
    >>> GS_Recurr.find_recurrences(factors=['NASDAQ', 'VIXCLS],
                                   start=query_start,
                                   end=query_end)
    """

    def __init__(self, df):

        self.df_original = df.loc[:, ~df.columns.duplicated()]
        self.df_original.index = pd.to_datetime(self.df_original.index)
        self.df_normalized = self.df_original.copy(deep=True)

        self.recurrences = None
        self.all_recurrences = None

        self.factors = None
        self.factor_weights = None

        self.factor_unit = None

        self.query_start = None
        self.query_end = None

        df_original_nans = self.df_original.isnull().sum().sum()
        if df_original_nans != 0:
            print('''Found {} NaNs... Imputing Using Cubic Spline & \
            Forward/Backward Filling...'''.format(df_original_nans))

            print('Done.')
            self.df_original = self.df_original.apply(self._fillnan)

    def _fillnan(self, ts: pd.Series) -> pd.Series:
        """
        Function fill in missing data by interpolating (cubic) and then
        backward/forward filling

        :param ts: Pandas Series
        """
        ts = ts.interpolate(method='cubic')
        ts = ts.ffill().bfill()
        ts = ts.round(4)
        return ts

    def _fill_inf_nan(self, series: pd.Series) -> pd.Series:
        """
        Function fill in missing np.nan and np.inf with 0.0

        :param series: Pandas Series
        """
        series = series.copy(deep=True)
        series = series.replace(np.inf, 1.0).replace(np.nan, 0.0)
        return series

    def _str_to_daterange(self,
                          s: str,
                          days_before: int = 0,
                          days_after: int = 0) -> DateRange:
        """
        Function that converts str with the format 'm/d/Y - m/d/Y' to
        DateRange with field names 'start' and 'end'

        """
        start, end = s.split('-', 1)
        start, end = start.strip(), end.strip()

        start = datetime.datetime.strptime(start,
                                           '%Y/%m/%d') - BDay(days_before)
        end = datetime.datetime.strptime(end, '%Y/%m/%d') + BDay(days_after)

        return DateRange(start=start, end=end)

    def _overlap_daterange(self,
                           dates: list,
                           length: int,
                           every_n: int = 1) -> list:
        """
        Function to generate all the overlapping date range given a list of
        datetimeindex

        :param dates: Pandas DatetimeIndex list
        :param length: length of overlapping time periods
        """

        lst = ['{} - {}'.format(
               date.strftime('%Y/%m/%d'),
               dates[idx + length - 1].strftime('%Y/%m/%d'))
               for idx, date in enumerate(dates[:len(dates) - length + 1])
               if len(dates[idx: idx + length]) == length]

        lst = lst[0::every_n]
        return lst

    def _calculate_overlap(self, r1: DateRange, r2: DateRange) -> int:
        """
        Function to calculate number of overlapped days from two DateRanges

        :param r1: first DateRange
        :param r2: second DateRange
        """
        latest_start = max(r1.start, r2.start)
        earliest_end = min(r1.end, r2.end)
        delta = (earliest_end - latest_start).days + 1
        num_overlap_days = max(0, delta)
        return num_overlap_days

    def _remove_overlap(self,
                        df: pd.DataFrame,
                        sort_by: str,
                        overlap_pct: float = 0.5,
                        asc: bool = False) -> pd.DataFrame:
        """
        Function to remove overlap dates in similarity score df

        :param df: simialrity scores df
        :param sort_by: column to sort in descending order before
        :param overlap_pct: % to determine if two date periods overlap
        :param asc: sort final df by asc
        """
        query_str = self.query_start.strftime('%Y/%m/%d') + \
            ' - ' + self.query_end.strftime('%Y/%m/%d')

        df = df.sort_values(sort_by, ascending=asc)

        non_overlap_list = []

        fst_recurr = df.index[0]
        non_overlap_list.append((fst_recurr,
                                 self._str_to_daterange(fst_recurr)))

        query_length = len(pd.date_range(self.query_start,
                                         self.query_end,
                                         freq='B'))
        non_overlap_thresh = query_length * overlap_pct

        for idx, date_str in enumerate(df.index):
            query_date_range = self._str_to_daterange(date_str)
            overlap_count = 0
            for non_overlap in non_overlap_list:
                non_overlap_date_range = self._str_to_daterange(non_overlap[0])
                num_overlap = self._calculate_overlap(query_date_range,
                                                      non_overlap_date_range)

                if num_overlap > non_overlap_thresh:
                    overlap_count += 1
                    break

            if overlap_count == 0:
                non_overlap_list.append((date_str, query_date_range))

        non_overlap_dates = [i[0] for i in non_overlap_list
                             if i[0] != query_str]
        print('    Before removing overlapped dates: {}'.format(df.shape[0]))
        final = df.loc[non_overlap_dates]
        print('    After removing overlapped dates: {}'.format(final.shape[0]))
        return final

    def _calculate_weights(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Function to weight the factors and their similarity scores.
        Returns the recurrences using weighted factors.

        :param df: Pandas DataFrame of scores
        """

        for col in df.columns:
            min_ = self._fill_inf_nan(df[col].copy(deep=True)).dropna().min()
            max_ = self._fill_inf_nan(df[col].copy(deep=True)).dropna().max()
            df['{} 0-1'.format(col)] = ((df[col] - min_) / (max_ - min_))

        norm_columns = [col for col in df.columns if '0-1' in col]

        norm_df = df[norm_columns]
        norm_df.columns = [col.replace(' Score 0-1', '')
                           for col in norm_columns]

        assert(((1.0 - norm_df) <= 1.0).sum().sum() == (norm_df.shape[0] *
                                                        norm_df.shape[1]))
        assert(((1.0 - norm_df) >= 0.0).sum().sum() == (norm_df.shape[0] *
                                                        norm_df.shape[1]))

        w_score = (1.0 - norm_df).mul([self.factor_weights[col]
                                       for col in norm_df.columns]).sum(axis=1)
        df['Final Score'] = w_score

        df = df.sort_values('Final Score', ascending=False)

        return df

    def _parallel_recurr_dict_creation(self, args: list) -> dict:
        """
        Function to run in parallel that extracts overlapping time periods
        and stores them into a dict of dict.

        :param: args is of the format factor, time series, and a list of
        overlapping date ranges
        """
        factor, df, overlap_date_ranges = args

        temp_dict = {}
        for start_end in overlap_date_ranges:
            daterange = self._str_to_daterange(start_end)
            daterange = pd.date_range(daterange.start, daterange.end, freq='B')

            recurr_chunk = df.loc[daterange]
            temp_dict[start_end] = np.array(recurr_chunk)

        return {factor: temp_dict}

    def find_recurrences(self,
                         factors: list,
                         start: datetime.date,
                         end: datetime.date,
                         factor_unit: Optional[dict] = None,
                         factor_weights: Optional[dict] = None,
                         overlap_pct: float = 0.2,
                         sim_metric: Union[str, Callable]='dtw',
                         normalize: Union[str, Callable]='z-score',
                         asc: bool = False,
                         parallel: bool = False,
                         n_jobs: int = 1,
                         every_n: int = 1,
                         search_start: Optional[datetime.date] = None,
                         search_end: Optional[datetime.date] = None) -> None:
        """
        Function to find recurrences.

        :param factors: factors of interest
        :param start: query period start date
        :param end: query period end date
        :param factor_unit: dict with factors as key and resepctive unit as
                            values; 'r' (return) or 'd' (difference)
        :param factor_weights: factors weights to weigh the factors; should
                                sum to 1; higher value implies more important
        :param overlap_pct: % threshold to determine if two periods overlap
        :param sim_metric: default metric is 'dtw', but can pass in your own
                            metric that compares two time series
        :param normalize: normalization function that is applied to the entire
                          time series; defauly is z-score, but can pass in
                          own function or choose None
        :param asc: order final scores by asc; default is that most similar
                    scores are 1.0 and least similar 0.0, since score is first
                    nomalized between 0-1 and then subtracted from one before
                    applying weights
        :param parallel: run in parallel
        :param n_jobs: number of cores to use; -1 specifies all cores
        :param every_n: every n overlapping date ranges is selected (instead
                        of every overlapping period). Helps reduce
                        computational time.

        **Examples**

        >>> GS_Recurr = GS_Recurrence(clean_df)
        >>> GS_Recurr.find_recurrences(factors=['NASDAQ', 'VIXCLS],
                                    start=query_start,
                                    end=query_end)

        """
        def z_score_normalize(ts) -> np.array:
            if np.unique(ts).size == 1:  # if values same, return same array
                return np.array(ts)
            else:
                return np.array(((ts - ts.mean())/ts.std()).dropna())

        df = self.df_original.copy(deep=True)

        self.factors = list(set(factors))
        self.query_start = start
        self.query_end = end
        assert(start < end), 'Start date is not before end date!'

        if factor_unit and not set(self.factors).issubset(factor_unit.keys()):
            raise ValueError('Specified factor units do not match factors.')
        else:
            if factor_unit:
                assert(set(factor_unit.values()).issubset(['r', 'd'])), \
                      ('Specified factor type is not r (return) or d (diff).')
                self.factor_unit = factor_unit
            else:
                self.factor_unit = {factor: 'r'
                                    for factor in df.columns}

        if factor_weights:
            assert(sum(factor_weights.values()) == 1.0), \
                  ('Specified weights do not sum to 1.')
            self.factor_weights = factor_weights
        else:
            self.factor_weights = {factor: 1 for factor in self.factors}

        if normalize == 'z-score':
            self.df_normalized = self.df_normalized.apply(z_score_normalize)
        elif normalize is None:
            self.df_normalized = df.copy(deep=True)
        else:
            self.df_normalized = self.df_normalized.apply(normalize)

        if isinstance(sim_metric, dict):
            sim_metric = {factor: (dtw_metric if metric == 'dtw'
                                   else metric)
                          for factor, metric in sim_metric.items()}
            sim_metric = {factor: (dtw_metric if sim_metric.get(factor, 0) == 0
                                   else sim_metric[factor])
                          for factor in factors}
        else:
            sim_metric = {factor: dtw_metric
                          for factor in factors}

        search_start = search_start if search_start else df.index[0]
        search_start = pd.Timestamp(search_start)

        search_end = search_end if search_end else df.index[-1]
        search_end = pd.Timestamp(search_end)
        assert(search_start < search_end), \
            'Search start date is not before end date!'

        print('========================================================')
        print('''INPUT PARAMETERS:\n\
        QUERY PERIOD = {0} - {1}\n\
        SEARCHING BETWEEN: {2} - {3}\n\
        FACTORS =  {4}\n\
        OVERLAP PCT = {5}\n\
        FACTOR TYPES = {6}\n\
        SIMILARITY METRICS = {7}\n\
        EVERY N: {8}'''.format(start.strftime('%Y/%m/%d'),
                               end.strftime('%Y/%m/%d'),
                               search_start.strftime('%Y/%m/%d'),
                               search_end.strftime('%Y/%m/%d'),
                               self.factors,
                               overlap_pct,
                               {factor: self.factor_unit[factor]
                                for factor in factors},
                               {factor: sim_metric[factor].__name__
                                for factor, _ in sim_metric.items()},
                               every_n))
        print('========================================================')

        query_length = len(pd.date_range(start, end, freq='B'))

        search_period = self.df_normalized.index
        search_period = search_period[search_period >= search_start]
        search_period = search_period[search_period <= search_end]

        overlap_date_ranges = self._overlap_daterange(search_period,
                                                      query_length,
                                                      every_n=every_n)

        query_str = self.query_start.strftime('%Y/%m/%d') + \
            ' - ' + self.query_end.strftime('%Y/%m/%d')

        if query_str not in overlap_date_ranges:
            overlap_date_ranges.append(query_str)

        # Create Dict That Contains Normalized Time Series for Query Period
        print('Creating query dict...')
        query_dict = {}

        query_chunk = self.df_normalized[self.factors].loc[start:end]
        query_str = '{} - {}'.format(start.strftime('%Y/%m/%d'),
                                     end.strftime('%Y/%m/%d'))

        for factor in self.factors:
            query_dict[factor] = {}
            query_dict[factor][query_str] = np.array(query_chunk[factor])
        print('Done.')

        # Compare each recurrence period with query period.
        # If user specifies custom function, use custom function, o/w use DTW.
        if parallel:
            try:
                pool = Pool(mp.cpu_count() if n_jobs == -1 else n_jobs)

                # Create Dict That Contains Time Series for All Recurrences
                print('Creating recurrences dict...')

                recurr_dict = {factor: {} for factor in self.factors}
                inputs = [(factor,
                           self.df_normalized[factor].copy(deep=True),
                           overlap_date_ranges)
                          for factor in self.factors]

                recurr_list = pool.map(self._parallel_recurr_dict_creation,
                                       inputs)
                for temp_dict in recurr_list:
                    factor = list(temp_dict.keys())[0]
                    recurr_dict[factor] = temp_dict[factor]

                print('Done.')

                # Calcualte scores
                print('''Calculating scores b/w query period and \
recurrence periods...''')
                scores = {factor: {} for factor in self.factors}

                inputs = [(np.array(query_dict[factor][query_str]),
                           np.array(recurr_dict[factor][recurr_daterange]),
                           factor,
                           recurr_daterange,
                           sim_metric[factor])
                          for factor in factors
                          for recurr_daterange in recurr_dict[factor].keys()]

                scores_results = pool.map(recurrence_parallel_score, inputs)

                for result in scores_results:
                    factor, recurr_date_range = result[0].split('_')
                    scores[factor][recurr_date_range] = result[1]
                pool.close()
            except Exception as e:
                pool.close()
                raise ValueError(e)
        else:
            # Create Dict That Contains Time Series for All Recurrence Periods
            print('Creating recurrences dict...')
            recurr_dict = {}
            for factor in self.factors:
                recurr_dict[factor] = {}
                for start_end in overlap_date_ranges:
                    daterange = self._str_to_daterange(start_end)
                    daterange = pd.date_range(daterange.start,
                                              daterange.end,
                                              freq='B')
                    recurr_chunk = self.df_normalized.loc[daterange][factor]
                    recurr_dict[factor][start_end] = np.array(recurr_chunk)

            print('Done.')

            # Calcualte scores
            print('''Calculating scores b/w query period and recurrence
periods...''')
            scores = {factor: {} for factor in self.factors}

            for factor in self.factors:
                scores[factor] = {}
                for recurr_daterange in recurr_dict[factor].keys():
                    recurr_series = recurr_dict[factor][recurr_daterange]
                    query_series = query_dict[factor][query_str]

                    score = sim_metric[factor](recurr_series, query_series)
                    scores[factor][recurr_daterange] = score

        print('Done.')

        # Fill in missing scores with least similar score
        print('Filling NaNs w/ min score.')

        for factor in self.factors:
            all_scores = [v for _, v in scores[factor].items()
                          if not math.isnan(v)]
            least_similar_score = max(all_scores) if asc else min(all_scores)

            for recurr_daterange, dtw_score in scores[factor].items():
                if math.isnan(scores[factor][recurr_daterange]):
                    scores[factor][recurr_daterange] = least_similar_score

        print('Done.')

        print('Calculating weights...')
        scores_df = pd.DataFrame.from_dict(scores)
        scores_df.columns = ['{} Score'.format(col)
                             for col in scores_df.columns]

        scores_df_weighted = self._calculate_weights(scores_df)
        self.all_recurrences = scores_df_weighted

        print('Done.')
        print('Removing overlapped dates...')

        # Remove Overlap
        recurrences = self._remove_overlap(scores_df_weighted,
                                           sort_by='Final Score',
                                           overlap_pct=overlap_pct,
                                           asc=asc)
        self.recurrences = recurrences

        print('Done.')

        print('=============================')
        print('DONE WITH FINDING RECURRENCES.')
        print('=============================')

    def _calc_significance(self,
                           n: int,
                           factor: str,
                           days_after: int,
                           recurrences_chg: list):
        """
        Function to calculate the signifance of the moves of n recurrences.
        Signficance is calculated using a one-sided t-test, where the mean to
        compare the recurrence's move is calculated by sampling periods
        of the same length as the recurrences and averaging the returns.

        Returns the sampled mean, t-statistic, and p-value.

        :param n: number of recurrences
        :param factor: the factor / time series in question
        :param days_after: the number of days after the recurrences to
                           calculate the significance for
        :param recurrences_chg: list of cummulative returns / differences
                                of the n recurrences (length n)
        """

        df = self.df_original.copy(deep=True)
        series = df.copy(deep=True)[factor].sort_index()

        query_length = days_after

        overlap_date_ranges = self._overlap_daterange(series.index,
                                                      query_length,
                                                      every_n=5)

        overlap_date_ranges = [self._str_to_daterange(daterange)
                               for daterange in overlap_date_ranges]

        all_changes = []
        for date_range in overlap_date_ranges:
            sample_series = series.loc[date_range.start:date_range.end]

            if self.factor_unit[factor] == 'r':
                diff = cummulative_pct_change(sample_series)
            elif self.factor_unit[factor] == 'd':
                diff = sample_series[-1] - sample_series[0]

            all_changes.append(diff)

        sim_diff_mean = np.nanmean(all_changes)
        recurrences_chg = recurrences_chg[~np.isnan(recurrences_chg)]
        t, p_value_sim = stats.ttest_1samp(np.array(recurrences_chg),
                                           sim_diff_mean)

        return sim_diff_mean, t, p_value_sim

    def summary(self, factors: list, n: int = 10, days_before: int = 15,
                days_after: int = 252) -> None:
        """
        Function to plot the recurrences found on a global view, a comparison
        of all the recurrences on the same graph, and a statistic table.

        Returns: None

        :param factors: list of factors to calculate statistics for.
                        Should be a subset of all the factors.
        :param n: the number of most similar recurrences to consider
        :param days_before: the number of days before the recurrences to
                            graph
        :param days_after: the number of days after the recurrences to graph
                           and calculate the significance for

        **Examples**

        >>> GS_Recurr.summary(factors=['NASDAQ'])
        """

        df = self.df_original.copy(deep=True)

        # Plot all recurrences on the same map
        print('Looking at {} recurrences.'.format(n))
        print('''Displaying period -{0} days before and +{1} days after \
recurrences.'''.format(days_before, days_after))

        fig = make_subplots(rows=1, cols=1,
                            shared_xaxes=True,
                            subplot_titles=factors)

        for idx, factor in enumerate(self.factors[:1]):
            temp = pd.Series(df[factor])
            temp.index = pd.to_datetime(temp.index)

            fig.add_trace(go.Scatter(x=temp.index, y=np.array(temp),
                                     name=factor), row=idx+1, col=1)

            for recurrence_date in sorted(self.recurrences.index[:n]):
                start_str, end_str = recurrence_date.split(' - ', 1)
                start = datetime.datetime.strptime(start_str.strip(),
                                                   '%Y/%m/%d')
                end = datetime.datetime.strptime(end_str.strip(), '%Y/%m/%d')

                # Adding a trace with a fill, setting opacity to 0
                fig.add_trace(
                    go.Scatter(
                        x=[start, end, end, start, start],
                        y=[0, 0, max(temp), max(temp), 0],
                        fill='toself',
                        mode='lines',
                        opacity=0.5,
                        name=recurrence_date,
                        fillcolor='salmon',
                        line_color='salmon',
                    ),
                    row=idx+1, col=1
                )

            # Add Query Period
            fig.add_trace(
                go.Scatter(
                    x=[self.query_start, self.query_end, self.query_end,
                       self.query_start, self.query_start],
                    y=[0, 0, max(temp), max(temp), 0],
                    fill='toself',
                    mode='lines',
                    opacity=0.5,
                    name='{} - {} (Query)'.format(self.query_start,
                                                  self.query_end),
                    fillcolor='forestgreen',
                    line_color='forestgreen',
                ),
                row=idx+1, col=1
            )
        title = 'Recurrences Overview ({})'.format(factor)
        fig.update_layout(title_text=title,
                          title_x=0.5,
                          legend_title='Recurrence Dates',
                          showlegend=False,
                          margin=dict(
                                    l=20,
                                    r=20,
                                    b=40,
                                    t=40,
                                    pad=4
                                  )
                          )
        fig.show()

        # Plot normalized recurrences on one plot
        all_stats = {}
        for factor in factors:
            stats = {}

            fig = go.Figure()

            ext_date_range = pd.date_range(self.query_start -
                                           BDay(days_before),
                                           self.query_end +
                                           BDay(days_after), freq='B')

            t = np.arange(len(ext_date_range)) - days_before
            query_factor_series = df.loc[ext_date_range][factor]
            query_factor_series /= query_factor_series[days_before]

            for idx, recurr_date_str in enumerate(self.recurrences.index[:n]):
                stats[recurr_date_str] = {}
                ext_daterange = self._str_to_daterange(recurr_date_str,
                                                       days_before,
                                                       days_after)
                ext_daterange = pd.date_range(ext_daterange.start,
                                              ext_daterange.end,
                                              freq='B')

                ext_series = df.loc[ext_daterange][factor]
                ext_series /= ext_series[days_before]

                daterange = self._str_to_daterange(recurr_date_str)

                during_daterange = pd.date_range(daterange.start,
                                                 daterange.end,
                                                 freq='B')
                recurr_series = df.loc[during_daterange][factor]

                after_date_range = pd.date_range(daterange.end,
                                                 daterange.end +
                                                 BDay(days_after),
                                                 freq='B')
                after_series = df.loc[after_date_range][factor]

                # Calculate Stats
                if self.factor_unit[factor] == 'd':
                    change = recurr_series[-1] - recurr_series[0]
                    after_chg = after_series[-1] - after_series[0]
                elif self.factor_unit[factor] == 'r':
                    change = cummulative_pct_change(recurr_series)
                    after_chg = cummulative_pct_change(after_series)
                else:
                    raise ValueError('Not r or d.')

                ended_up_during = recurr_series[-1] > recurr_series[0]
                ended_up_after = after_series[-1] > after_series[0]

                stats[recurr_date_str]['Chg'] = change
                stats[recurr_date_str]['After Chg'] = after_chg
                stats[recurr_date_str]['Ended Up During'] = ended_up_during
                stats[recurr_date_str]['Ended Up After'] = ended_up_after

                fig.add_trace(
                    go.Scatter(
                        x=t,
                        y=ext_series,
                        name='{} (#{})'.format(recurr_date_str, idx)
                    )
                )

            all_stats[factor] = {}

            ended_up_during = len([1 for k, v in stats.items()
                                   if v['Ended Up During']])
            ended_down_during = n - ended_up_during

            ended_up_after = len([1 for k, v in stats.items()
                                 if v['Ended Up After']])
            ended_down_after = n - ended_up_after

            avg_change = np.nanmean([v['Chg'] for k, v in stats.items()])
            stdev_chg = np.nanstd([v['Chg'] for k, v in stats.items()])

            avg_change_after = np.nanmean([v['After Chg']
                                          for k, v in stats.items()])
            stdev_chg_after = np.nanstd([v['After Chg']
                                        for k, v in stats.items()])

            avg_change = round(avg_change, 2)
            stdev_chg = round(stdev_chg, 2)
            avg_change_after = round(avg_change_after, 2)
            stdev_change_after = round(stdev_chg_after, 2)

            # Calculate p-value (durig recurrence)
            recurrence_chg = np.array([v['Chg'] for k, v in stats.items()])
            query_length = np.busday_count(self.query_start,
                                           self.query_end) + 1
            results_during = self._calc_significance(n,
                                                     factor,
                                                     query_length,
                                                     recurrence_chg)
            sim_diff_mean_d, t_stat_d, p_value_sim_d = results_during
            sim_diff_mean_d = round(sim_diff_mean_d, 2)
            p_value_sim_d = round(p_value_sim_d, 2)

            # Calculate p-value (after recurrence)
            recurr_chg_after = np.array([v['After Chg']
                                         for k, v in stats.items()])
            results_after = self._calc_significance(n,
                                                    factor,
                                                    days_after,
                                                    recurr_chg_after)
            sim_diff_mean_a, t_stat_a, p_value_sim_a = results_after
            sim_diff_mean_a = round(sim_diff_mean_a, 2)
            p_value_sim_a = round(p_value_sim_a, 2)

            # Overall stats
            all_stats[factor]['Ended Up/Down (During)'] = (ended_up_during,
                                                           ended_down_during)
            all_stats[factor]['Average Change (During) (%)'] = avg_change
            all_stats[factor]['Stdev Change (During) (%)'] = stdev_chg
            all_stats[factor]['p-value (During)'] = p_value_sim_d
            all_stats[factor]['Sampled Mean Change (During) (%)'] = \
                sim_diff_mean_d

            all_stats[factor]['Units'] = self.factor_unit[factor]
            all_stats[factor]['Ended Up/Down (After)'] = (ended_up_after,
                                                          ended_down_after)

            all_stats[factor]['Average Change (After) (%)'] = avg_change_after
            all_stats[factor]['Stdev Change (After) (%)'] = stdev_change_after
            all_stats[factor]['p-value (After)'] = p_value_sim_a
            all_stats[factor]['Sampled Mean Change (After) (%)'] = \
                sim_diff_mean_a

            stats_df = pd.DataFrame.from_dict(all_stats).T
            cols = [
                    'Ended Up/Down (During)',
                    'Average Change (During) (%)',
                    'Stdev Change (During) (%)',
                    'p-value (During)',
                    'Sampled Mean Change (During) (%)',
                    'Units',
                    'Ended Up/Down (After)',
                    'Average Change (After) (%)',
                    'Stdev Change (After) (%)',
                    'p-value (After)',
                    'Sampled Mean Change (After) (%)'
                    ]
            stats_df = stats_df[cols]
            display(stats_df)

            # Add query time series
            fig.add_trace(go.Scatter(
                x=t,
                y=query_factor_series,
                name='{} - {} (Query)'.format(self.query_start,
                                              self.query_end),
                line=dict(color='black'))
            )

            # Add black line to denote start/end of recurrences
            fig.update_layout(
                shapes=[dict(
                            type='line',
                            yref='paper',
                            y0=0,
                            y1=1,
                            xref='x',
                            x0=len(pd.date_range(self.query_start,
                                                 self.query_end, freq='B')),
                            x1=len(pd.date_range(self.query_start,
                                                 self.query_end, freq='B'))
                        ),

                        dict(
                            type='line',
                            yref='paper', y0=0, y1=1,
                            xref='x', x0=0, x1=0
                        )
                        ],
                margin=dict(
                        l=20,
                        r=20,
                        b=40,
                        t=40,
                        pad=4
                    )
            )

            # Add Title, Y-Axis, X_Axis
            fig.update_layout(
                title='Recurrence Comparison Graph for {}'.format(factor),
                title_x=0.5,
                xaxis_title='Time (days)',
                yaxis_title='Normalized Time Series',
                font=dict(
                    family='Courier New, monospace',
                    size=12,
                    color='#7f7f7f'
                ),
                xaxis=dict(tickmode='linear',
                           tick0=-days_before,
                           dtick=10)
            )

            fig.show()
            print('==========================================================')


class GS_RecurrenceUI:
    """
    The GUI for GS_Recurrence. Uses Jupyter Widgets and is only useable
    in Jupyter Notebooks / Jupyter Lab.

    :param df: the original Pandas Dataframe to feed to the model. Requires
               index as dates and columns as time series. Only supports daily
               data.
    :param factor_unit: dict with factor name as keys and resepctive unit as
                        values; 'r' (return) or 'd' (difference)
    :param sim_metric: default metric is 'dtw', but can pass in your own
                       metric that compares two time series. Can specify
                       a dict with factor name as keys and callable as values.
    :param normalize: normalization function that is applied to the entire
                      time series; default is z-score, but can pass in
                      own function or choose None
    :param factor_weights: factors weights to weigh the factors; should
                            sum to 1; higher value implies more important
    :param parallel: run in parallel
    :param n_jobs: number of cores to use; -1 specifies all cores
    :param every_n: every n overlapping date ranges is selected (instead
                of every overlapping period). Helps reduce
                computational time.

    **Examples**
    >>> def custom_metric_pct_chg(a, b):
            pct_chg_a = (a[-1] - a[0])/a[0] * 100
            pct_chg_b = (b[-1] - b[0])/b[0] * 100

            feature_vector_a = np.array([pct_chg_a])
            feature_vector_b = np.array([pct_chg_b])

            score = np.linalg.norm(feature_vector_a - feature_vector_b)
            if score == np.inf or score == -np.inf:
                return np.nan
            return score

    >>> factor_units = {'NASDAQ': 'r', '10Y2Y': 'd'}
    >>> similarity_dict = {'NASDAQ': custom_metric_pct_chg,
                           '10Y2Y': 'DTW'}

    >>> GS_RecurrenceUI(df=df,
                        factor_unit=factor_units,
                        sim_metric=similarity_dict)
    """

    def __init__(self,
                 df: pd.DataFrame,
                 factor_unit: dict,
                 sim_metric: Union[str, Callable]='dtw',
                 normalize: Union[str, Callable]='z-score',
                 factor_weights: Optional[dict] = None,
                 parallel: bool = False,
                 n_jobs: int = 1,
                 every_n: int = 1) -> None:

        df.index = pd.to_datetime(df.index)
        self.GSRecurrence = None
        self.df = df.sort_index()
        self.sim_metric = sim_metric
        self.normalize = normalize
        self.factor_weights = factor_weights
        self.parallel = parallel
        self.n_jobs = n_jobs
        self.every_n = every_n

        self.factor_unit = factor_unit

        # INPUT PARAMTERS FOR GSRecurrence
        self.out = widgets.Output(layout={'border': '1px solid black'})

        self.start_date = \
            widgets.DatePicker(value=datetime.date(2020, 1, 1),
                               description='Query Start ',
                               style=dict(description_width='initial'))
        self.end_date = \
            widgets.DatePicker(value=df.index[-1],
                               description='Query End ',
                               style=dict(description_width='initial'))

        self.search_start = \
            widgets.DatePicker(value=df.index[0],
                               description='Search Start',
                               style=dict(description_width='initial'))
        self.search_end = \
            widgets.DatePicker(value=df.index[-1],
                               description='Search End',
                               style=dict(description_width='initial'))

        self.factors = widgets.SelectMultiple(
            options=list(df.columns),
            value=[df.columns[0]],
            description='Factors',
            disabled=False,
            rows=3
        )

        self.overlap_pct = widgets.FloatSlider(
            value=0.2,
            min=0,
            max=1,
            description='Overlap %:',
            continuous_update=False,
            style=dict(description_width='initial')
        )

        self.button = widgets.Button(description='Calculate Recurrences!',
                                     layout=widgets.Layout(width='auto'))
        self.param_box = widgets.HBox([widgets.VBox([self.start_date,
                                                     self.search_start]),
                                       widgets.VBox([self.end_date,
                                                     self.search_end]),
                                       self.factors,
                                       self.overlap_pct,
                                       self.button])

        self.button.on_click(self.calculate_recurrences)

        # INPUT PARAMTERS FOR Visualization
        self.days_before = widgets.IntSlider(
            value=-15,
            min=-100,
            max=-15,
            step=5,
            description='Days Before:',
            continuous_update=False
        )

        self.days_after = widgets.IntSlider(
            value=30,
            min=0,
            max=500,
            step=5,
            description='Days After:',
            continuous_update=False
        )

        self.normalize_slide = widgets.IntSlider(
            value=0,
            min=0,
            max=100,
            step=1,
            description='Normalize: ',
            continuous_update=False
        )

        self.normalize_check = widgets.Checkbox(
                                    value=True,
                                    description='',
                                    disabled=False,
                                    indent=False,
                                    layout=widgets.Layout(width='12px')
                                )

        self.num_recurrences = widgets.IntSlider(
            value=10,
            min=1,
            max=100,
            step=1,
            description='# Recurrences:',
            continuous_update=False
        )

        self.factor = widgets.Dropdown(
            description='Factor:   ',
            value=self.df.columns[0],
            options=self.df.columns
        )

        self.graphs = go.FigureWidget()
        self.graphs.update_layout(title_text='Recurrences Comparison (__)',
                                  title_x=0.5)

        self.recurr_graph = go.FigureWidget()
        self.recurr_graph.update_layout(
            title_text='Recurrences Overview (__)', title_x=0.5)

        self.update_stats = widgets.Button(description='Refresh Stats Table',
                                           layout=widgets.Layout(width='auto'))

        self.stats_table = go.FigureWidget(make_subplots(
                                rows=1, cols=1,
                                shared_xaxes=True,
                                vertical_spacing=0.03,
                                specs=[[{'type': 'table'}]]))
        self.stats_table.update_layout(title_text='Stats Table', title_x=0.5)

        self.panel = widgets.VBox([widgets.HBox([self.days_before,
                                                 self.days_after,
                                                 self.num_recurrences,
                                                 self.factor,
                                                 self.update_stats]),
                                   widgets.HBox([self.normalize_check,
                                                 self.normalize_slide]),
                                   self.graphs,
                                   self.recurr_graph,
                                   self.stats_table,
                                   self.out])

        self.days_before.observe(self.update_graphs, names='value')
        self.days_after.observe(self.update_graphs, names='value')
        self.normalize_slide.observe(self.update_graphs, names='value')
        self.normalize_check.observe(self.update_graphs, names='value')
        self.factor.observe(self.update_graphs, names='value')
        self.factor.observe(self.update_recurr_graph, names='value')

        self.num_recurrences.observe(self.update_graphs, names='value')
        self.num_recurrences.observe(self.update_recurr_graph, names='value')

        self.update_stats.on_click(self.update_stats_table)

    def update_recurr_graph(self, change):
        """
        Function that is called when a change is detected. Updates the graph
        with all the recurrences plotted against each other.
        """
        with self.out:
            GS_Recurr = self.GSRecurrence
            recurrences = GS_Recurr.recurrences

            n = self.num_recurrences.value
            factor = self.factor.value

            # PLot all recurrences on same graph
            new_traces = []

            series = GS_Recurr.df_normalized[factor]
            min_series, max_series = min(series), max(series)
            new_traces.append(go.Scatter(x=series.index,
                                         y=np.array(series),
                                         name=factor
                                         )
                              )

            for recurrence_date in sorted(GS_Recurr.recurrences.index[:n]):
                start_str, end_str = recurrence_date.split(' - ', 1)
                start_ = datetime.datetime.strptime(start_str.strip(),
                                                    '%Y/%m/%d')
                end_ = datetime.datetime.strptime(end_str.strip(), '%Y/%m/%d')

                new_traces.append(
                    go.Scatter(
                        x=[start_, end_, end_, start_, start_],
                        y=[min_series, min_series, max_series,
                           max_series, min_series],
                        fill='toself',
                        mode='lines',
                        opacity=0.5,
                        name=recurrence_date,
                        fillcolor='salmon',
                        line_color='salmon',
                    )
                )

            # Add Query Period
            query_start = pd.Timestamp(GS_Recurr.query_start)
            query_end = pd.Timestamp(GS_Recurr.query_end)
            new_traces.append(
                go.Scatter(
                    x=[query_start, query_end, query_end,
                       query_start, query_start],
                    y=[min_series, min_series, max_series,
                       max_series, min_series],
                    fill='toself',
                    mode='lines',
                    opacity=0.5,
                    name='{} - {} (Query)'.format(query_start, query_end),
                    fillcolor='forestgreen',
                    line_color='forestgreen',
                )
            )

            with self.recurr_graph.batch_update():
                self.recurr_graph.data = []
                self.recurr_graph.add_traces(new_traces)

                self.recurr_graph.update_layout(
                    title_text='Recurrences Overview ({})'.format(factor),
                    title_x=0.5,
                    legend_title='Recurrence Dates',
                    showlegend=False,
                    xaxis_title='Date (Days)',
                    yaxis_title='{}'.format(factor),

                    margin=dict(
                                l=20,
                                r=20,
                                b=40,
                                t=40,
                                pad=4
                            )
                )

    def calculate_recurrences(self, change):
        """
        Function that is called when the Calculate Recurrences button is
        clicked. Calls GS_Recurrence and calculates a new set of recurrences.
        """

        with self.out:
            factors = self.factors.value
            n = self.num_recurrences.value
            days_after = self.days_after.value
            days_before = np.abs(self.days_before.value)
            normalize_day = self.normalize_slide.value
            start = self.start_date.value
            end = self.end_date.value
            pct_overlap = self.overlap_pct.value
            factor_unit = self.factor_unit
            parallel = self.parallel
            n_jobs = self.n_jobs

            # Clear outputs and graphs
            self.out.clear_output()
            self.graphs.data = []
            self.recurr_graph.data = []
            self.stats_table.data = []

            title = 'Recurrences Overview (__)'
            self.recurr_graph.update_layout(title_text=title,
                                            title_x=0.5)
            self.graphs.update_layout(title_text='Recurrences Comparison (__)',
                                      title_x=0.5)

            GS_Recurr = GS_Recurrence(self.df)
            GS_Recurr.find_recurrences(factors=self.factors.value,
                                       start=start,
                                       end=end,
                                       factor_unit=factor_unit,
                                       factor_weights=self.factor_weights,
                                       overlap_pct=pct_overlap,
                                       parallel=parallel,
                                       n_jobs=n_jobs,
                                       sim_metric=self.sim_metric,
                                       normalize=self.normalize,
                                       every_n=self.every_n,
                                       search_start=self.search_start.value,
                                       search_end=self.search_end.value)
            recurrences = GS_Recurr.recurrences
            display(recurrences.head(n))

            self.GSRecurrence = GS_Recurr
            self.normalize_slide.max = len(pd.date_range(GS_Recurr.query_start,
                                                         GS_Recurr.query_end,
                                                         freq='B'))
            self.num_recurrences.max = GS_Recurr.recurrences.shape[0]

            self.factor.value = factors[0]

            # Plot recurrences and update stats table
            self.update_graphs(change)
            self.update_recurr_graph(change)
            self.update_stats_table(change)

    def update_graphs(self, change):
        """
        Function that is called when a change is detected. Updates the graphs.
        """

        GS_Recurr = self.GSRecurrence
        n = self.num_recurrences.value
        factor = self.factor.value
        days_after = self.days_after.value
        days_before = np.abs(self.days_before.value)
        normalize_day = self.normalize_slide.value
        recurrences = GS_Recurr.recurrences
        start = self.start_date.value
        end = self.end_date.value

        with self.out:
            temp_df = GS_Recurr.df_original[factor]
            date_range = pd.date_range(start - BDay(days_before),
                                       end + BDay(days_after),
                                       freq='B')
            query_series = temp_df.loc[date_range]
            if self.normalize_check.value:
                query_series /= query_series[normalize_day +
                                             days_before]

            t = np.arange(len(query_series)) - days_before

            new_traces = []
            for idx, recurr_date_str in enumerate(recurrences.index[:n]):
                daterange = GS_Recurr._str_to_daterange(recurr_date_str,
                                                        days_before,
                                                        days_after)
                daterange = pd.date_range(daterange.start,
                                          daterange.end,
                                          freq='B')
                recurr_series = temp_df.loc[daterange]

                assert(recurr_series[days_before] ==
                       recurr_series[daterange[days_before]])

                normalized_series = recurr_series
                if self.normalize_check.value:
                    normalized_series = recurr_series / \
                                        recurr_series[normalize_day +
                                                      days_before]

                # Add recurrence to graph
                new_traces.append(go.Scatter(
                    x=t,
                    y=normalized_series,
                    name='{} (#{})'.format(recurr_date_str, idx+1))
                 )

            new_traces.append(
                go.Scatter(
                    x=t,
                    y=query_series,
                    name='{} - {} (Query)'.format(GS_Recurr.query_start,
                                                  GS_Recurr.query_end),
                    line=dict(color='black'))
            )

            with self.graphs.batch_update():
                self.graphs.data = []
                self.graphs.add_traces(new_traces)

                # Add black line to denote start/end of recurrences
                self.graphs.update_layout(
                    title_text='Recurrences Comparison ({})'.format(factor),
                    title_x=0.5,

                    xaxis_title='Date (Days)',
                    yaxis_title='Normalized Time Series',
                    legend_title='Recurrence Dates',
                    showlegend=True,
                    shapes=[dict(
                                type='line',
                                xref='x',
                                x0=len(pd.date_range(GS_Recurr.query_start,
                                                     GS_Recurr.query_end,
                                                     freq='B'))-1,
                                x1=len(pd.date_range(GS_Recurr.query_start,
                                                     GS_Recurr.query_end,
                                                     freq='B'))-1,
                                yref='paper', y0=0, y1=1
                            ),

                            # Line that goes through origin
                            dict(
                                type='line',
                                yref='paper', y0=0, y1=1,
                                xref='x', x0=0, x1=0
                            ),

                            # Shaded line to denote normalized date
                            dict(
                                type='line',
                                xref='x',
                                x0=normalize_day,
                                x1=normalize_day,
                                yref='paper', y0=0, y1=1,
                                line=dict(
                                    dash='dash'
                                )
                            )
                            ],
                    margin=dict(
                        l=20,
                        r=20,
                        b=40,
                        t=40,
                        pad=4
                    )
                )

    def update_stats_table(self, change):
        """
        Function that is called when the Refresh Stats button is clicked.
        Refreshes the statistics table using the new paramters.
        """
        GS_Recurr = self.GSRecurrence
        start = self.start_date.value
        end = self.end_date.value
        days_before = np.abs(self.days_before.value)
        days_after = self.days_after.value
        n = self.num_recurrences.value
        recurrs = GS_Recurr.recurrences
        factor_unit = GS_Recurr.factor_unit

        query_start = pd.Timestamp(GS_Recurr.query_start)
        query_end = pd.Timestamp(GS_Recurr.query_end)

        with self.out:
            print('''Updating stats table... N={0}, days_before={1}, \
days_after={2}'''.format(n, days_before, days_after))

            all_stats = {}
            for factor in self.df.columns:
                stats = {}

                date_range = pd.date_range(start -
                                           BDay(days_before),
                                           end +
                                           BDay(days_after), freq='B')

                for idx, recurr_date_str in enumerate(recurrs.index[:n]):
                    stats[recurr_date_str] = {}
                    daterange = GS_Recurr._str_to_daterange(recurr_date_str)
                    during_daterange = pd.date_range(daterange.start,
                                                     daterange.end,
                                                     freq='B')

                    recurr_series = self.df.loc[during_daterange][factor]

                    after_date_range = pd.date_range(daterange.end,
                                                     daterange.end +
                                                     BDay(days_after),
                                                     freq='B')
                    after_series = self.df.loc[after_date_range][factor]

                    # Calculate Stats
                    if factor_unit[factor] == 'd':
                        change = recurr_series[-1] - recurr_series[0]
                        after_chg = after_series[-1] - after_series[0]
                    elif factor_unit[factor] == 'r':
                        change = cummulative_pct_change(recurr_series)
                        after_chg = cummulative_pct_change(after_series)
                    else:
                        raise ValueError('Not r or d.')

                    ended_up_during = recurr_series[-1] > recurr_series[0]
                    ended_up_after = after_series[-1] > after_series[0]

                    stats[recurr_date_str]['Chg'] = change
                    stats[recurr_date_str]['After Chg'] = after_chg
                    stats[recurr_date_str]['Ended Up During'] = ended_up_during
                    stats[recurr_date_str]['Ended Up After'] = ended_up_after

                all_stats[factor] = {}

                ended_up_during = len([1 for k, v in stats.items()
                                       if v['Ended Up During']])
                ended_down_during = n - ended_up_during

                ended_up_after = len([1 for k, v in stats.items()
                                      if v['Ended Up After']])
                ended_down_after = n - ended_up_after

                avg_change = np.nanmean([v['Chg'] for k, v in stats.items()])
                stdev_chg = np.nanstd([v['Chg'] for k, v in stats.items()])

                avg_change_after = np.nanmean([v['After Chg']
                                               for k, v in stats.items()])
                stdev_chg_after = np.nanstd([v['After Chg']
                                             for k, v in stats.items()])

                avg_change = round(avg_change, 2)
                stdev_chg = round(stdev_chg, 2)
                avg_change_after = round(avg_change_after, 2)
                stdev_change_after = round(stdev_chg_after, 2)

                # Calculate p-value (durig recurrence)
                recurrence_chg = np.array([v['Chg']
                                           for k, v in stats.items()])
                query_length = np.busday_count(query_start.date(),
                                               query_end.date()) + 1
                results_during = GS_Recurr._calc_significance(n,
                                                              factor,
                                                              query_length,
                                                              recurrence_chg)
                sim_diff_mean_d, t_stat_d, p_value_sim_d = results_during
                sim_diff_mean_d = round(sim_diff_mean_d, 2)
                p_value_sim_d = round(p_value_sim_d, 2)

                # Calculate p-value (after recurrence)
                recurr_chg_after = np.array([v['After Chg']
                                             for k, v in stats.items()])
                results_after = GS_Recurr._calc_significance(n,
                                                             factor,
                                                             days_after,
                                                             recurr_chg_after)
                sim_diff_mean_a, t_stat_a, p_value_sim_a = results_after
                sim_diff_mean_a = round(sim_diff_mean_a, 2)
                p_value_sim_a = round(p_value_sim_a, 2)

                all_stats[factor]['Ended Up/Down (During)'] = \
                    (ended_up_during, ended_down_during)
                all_stats[factor]['Average Change (During) (%)'] = avg_change
                all_stats[factor]['Stdev Change (During) (%)'] = stdev_chg
                all_stats[factor]['p-value (During)'] = p_value_sim_d
                all_stats[factor]['Sampled Mean Change (During) (%)'] = \
                    sim_diff_mean_d

                all_stats[factor]['Units'] = factor_unit[factor]
                all_stats[factor]['Ended Up/Down (After)'] = (ended_up_after,
                                                              ended_down_after)

                all_stats[factor]['Average Change (After) (%)'] = \
                    avg_change_after
                all_stats[factor]['Stdev Change (After) (%)'] = \
                    stdev_change_after
                all_stats[factor]['p-value (After)'] = p_value_sim_a
                all_stats[factor]['Sampled Mean Change (After) (%)'] = \
                    sim_diff_mean_a

            stats_df = pd.DataFrame.from_dict(all_stats).T
            display(stats_df)

            with self.stats_table.batch_update():
                self.stats_table.add_trace(
                    go.Table(
                        header=dict(
                            values=['Factor'] + list(stats_df.columns),
                            font=dict(size=10),
                            align='center'
                        ),
                        cells=dict(
                            values=[list(self.df.columns)] +
                                   [stats_df[k].tolist()
                                    for k in stats_df.columns],
                            align='center')
                    ),
                    row=1, col=1
                )
                title = 'Stats Table (N={}, {} Days After)'.format(n,
                                                                   days_after)
                self.stats_table.update_layout(title_text=title,
                                               title_x=0.5)
            print('Done.')

    def _ipython_display_(self):
        display(self.param_box)
        display(self.panel)
