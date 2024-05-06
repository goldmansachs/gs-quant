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

import datetime

import numpy
import scipy.stats.mstats as stats
import statsmodels.api as sm
from scipy.stats import percentileofscore
from statsmodels.regression.rolling import RollingOLS

from .algebra import *
from ..data import DataContext
from ..models.epidemiology import SIR, SEIR, EpidemicModel

"""
Stats library is for basic arithmetic and statistical operations on timeseries.
These include basic algebraic operations, probability and distribution analysis.
Generally not finance-specific routines.
"""

try:
    from quant_extensions.timeseries.statistics import rolling_std
except ImportError:
    def rolling_std(x: pd.Series, offset: pd.DateOffset) -> pd.Series:
        size = len(x)
        index = x.index
        results = np.empty(size, dtype=np.double)
        results[0] = np.nan
        values = np.array(x.values, dtype=np.double)  # put data into np arrays to save time on slicing later

        start = 0
        for i in range(1, size):
            for j in range(start, i + 1):
                if pd.Timestamp(index[j]) > index[i] - offset:
                    start = j
                    break
            section = values[start:i + 1]
            results[i] = np.std(section[section == section], ddof=1)
        return pd.Series(results, index=index, dtype=np.double)


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

    :param w: window: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value. If w is a string, it should be a relative time duration like '1m', '1d', etc.
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

    If :math:`w` is a string, it should be a relative time duration such as '1m', '5d', etc. The available frequency
    strings can be found below:

    ==============    ================
    Frequency         Description
    ==============    ================
    y                 one year
    m                 one month
    w                 one week
    d                 one day
    h                 one hour
    ==============    ================

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
        values = rolling_offset(x, w.w, np.nanmin, 'min') if isinstance(x, pd.Series) else [
            x.loc[(x.index > (idx - w.w).datetime()) & (x.index <= idx)].min() for idx in x.index]
        return apply_ramp(pd.Series(values, index=x.index, dtype=np.dtype(float)), w)
    else:
        return apply_ramp(x.rolling(w.w, 0).min(), w)


@plot_function
def max_(x: Union[pd.Series, List[pd.Series]], w: Union[Window, int, str] = Window(None, 0)) -> pd.Series:
    """
    Maximum value of series over given window

    :param x: series: a timeseries or an array of timeseries
    :param w: window: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value. If w is a string, it should be a relative time duration like '1m', '5d', etc.
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

    If :math:`w` is a string, it should be a relative time duration such as '1m', '5d', etc. The available frequency
    strings can be found below:

    ==============    ================
    Frequency         Description
    ==============    ================
    y                 one year
    m                 one month
    w                 one week
    d                 one day
    h                 one hour
    ==============    ================

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
        values = rolling_offset(x, w.w, np.nanmax, 'max') if isinstance(x, pd.Series) else [
            x.loc[(x.index > idx - w.w) & (x.index <= idx)].max() for idx in x.index]
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

    max_v = max_(x, Window(w.w, 0))
    min_v = min_(x, Window(w.w, 0))

    return apply_ramp(max_v - min_v, w)


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

    :math:`R_t = \\frac{\\sum_{i=t-w+1}^{t} X_i}{N}`

    where :math:`N` is the number of observations in each rolling window, :math:`w`.

    If an array of timeseries is provided:

    :math:`R_t = \\frac{\\sum_{i=t-w+1}^{t} {\\sum_{j=1}^{n}} X_{ij}}{N}`

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
        if isinstance(x, pd.Series):
            values = rolling_offset(x, w.w, np.nanmean, 'mean')
        else:
            values = [np.nanmean(x.loc[(x.index > (idx - w.w).date()) & (x.index <= idx)]) for idx in x.index]
    else:
        if isinstance(x, pd.Series):
            values = x.rolling(w.w, 0).mean()  # faster than slicing in Python
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

    :math:`R_t = \\frac{X_{\\lfloor t-d \\rfloor} + X_{\\lceil t-d \\rceil}}{2}`

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
        values = rolling_offset(x, w.w, np.nanmedian, 'median') if isinstance(x, pd.Series) else [
            x.loc[(x.index > (idx - w.w).date()) & (x.index <= idx)].median() for idx in x.index]
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
        values = rolling_apply(x, w.w, lambda a: stats.mode(a).mode[0]) if isinstance(x, pd.Series) else [
            stats.mode(x.loc[(x.index > (idx - w.w).date()) & (x.index <= idx)]).mode[0] for idx in x.index]
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

    :math:`R_t = \\sum_{i=t-w+1}^{t} X_i`

    where :math:`w` is the size of the rolling window.

    If :math:`x` is an array of series:

    :math:`R_t = \\sum_{i=t-w+1}^{t} \\sum_{j=1}^{n} X_{ij}`

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
        assert isinstance(x, pd.Series), 'expected a series'
        values = rolling_offset(x, w.w, np.nansum, 'sum')
        return apply_ramp(values, w)
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

    :math:`R_t = \\prod_{i=t-w+1}^{t} X_i`

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
        values = rolling_offset(x, w.w, np.nanprod, 'prod') if isinstance(x, pd.Series) else [
            x.loc[(x.index > (idx - w.w).date()) & (x.index <= idx)].prod() for idx in x.index]
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

    :math:`R_t = \\sqrt{\\frac{1}{N-1} \\sum_{i=t-w+1}^t (X_i - \\overline{X_t})^2}`

    where :math:`N` is the number of observations in each rolling window, :math:`w`, and :math:`\\overline{X_t}` is the
    mean value over the same window:

    :math:`\\overline{X_t} = \\frac{\\sum_{i=t-w+1}^{t} X_i}{N}`

    If window is not provided, computes standard deviation over the full series

    **Examples**

    Generate price series and compute standard deviation of returns over :math:`22` observations

    >>> prices = generate_series(100)
    >>> std(returns(prices), 22)

    **See also**

    :func:`sum` :func:`mean` :func:`var`

    """
    if x.empty:
        return x

    w = normalize_window(x, w)
    assert x.index.is_monotonic_increasing, "series index is monotonic increasing"
    if isinstance(w.w, pd.DateOffset):
        return apply_ramp(rolling_std(x, w.w), w)
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

    :math:`DF_t = \\frac{(\\sum_{i=0}^t w_i)^2} {(\\sum_{i=0}^t w_i)^2 - \\sum_{i=0}^t w_i^2}`

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

    :math:`R_t = \\frac{1}{N-1} \\sum_{i=t-w+1}^t (X_i - \\overline{X_t})^2`

    where :math:`N` is the number of observations in each rolling window, :math:`w`, and :math:`\\overline{X_t}` is the
    mean value over the same window:

    :math:`\\overline{X_t} = \\frac{\\sum_{i=t-w+1}^{t} X_i}{N}`

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
        values = rolling_offset(x, w.w, lambda a: np.nanvar(a, ddof=1), 'var') if isinstance(x, pd.Series) else [
            x.loc[(x.index > (idx - w.w).date()) & (x.index <= idx)].var() for idx in x.index]
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

    :math:`R_t = \\frac{1}{N-1} \\sum_{i=t-w+1}^t (X_i - \\overline{X_t}) (Y_i - \\overline{Y_t})`

    where :math:`N` is the number of observations in each rolling window, :math:`w`, and :math:`\\overline{X_t}` and
    :math:`\\overline{Y_t}` represent the sample mean of series :math:`X_t` and :math:`Y_t` over the same window:

    :math:`\\overline{X_t} = \\frac{\\sum_{i=t-w+1}^{t} X_i}{N}` and
    :math:`\\overline{Y_t} = \\frac{\\sum_{i=t-w+1}^{t} Y_i}{N}`

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
        values = [x.loc[(x.index > (idx - w.w).date()) & (x.index <= idx)].cov(y) for idx in x.index]
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

    :math:`R_t = \\frac { X_t - \\mu }{ \\sigma }`

    Where :math:`\\mu` and :math:`\\sigma` are sample mean and standard deviation over the given window

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
        dt_idx = pd.DatetimeIndex(x.index).date
        values = [_zscore(x.loc[(dt_idx > (idx - w.w).date()) & (dt_idx <= idx)]) for idx in dt_idx]
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

    :math:`upper = \\mu + \\sigma \\times limit`

    :math:`lower = \\mu - \\sigma \\times limit`

    Where :math:`\\mu` and :math:`\\sigma` are sample mean and standard deviation. The series is restricted by:

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


class Direction(Enum):
    START_TODAY = 'start_today'
    END_TODAY = 'end_today'


@plot_function
def generate_series(length: int, direction: Direction = Direction.START_TODAY) -> pd.Series:
    """
    Generate sample timeseries

    :param length: number of observations
    :param direction: whether generated series should start from today or end on today
    :return: date-based time series of randomly generated prices

    **Usage**

    Create timeseries from returns generated from a normally distributed random variables (IDD). Length determines the
    number of observations to be generated.

    Assume random variables :math:`R` which follow a normal distribution with mean :math:`0` and standard deviation
    of :math:`1`

    :math:`R \\sim N(0, 1)`

    The timeseries is generated from these random numbers through:

    :math:`X_t = (1 + R)X_{t-1}`

    **Examples**

    Generate price series with 100 observations starting from today's date:

    >>> prices = generate_series(100)

    **See also**

    :func:`numpy.random.normal()`

    """
    levels = [100]
    first = datetime.date.today()
    if direction == Direction.END_TODAY:
        first -= datetime.timedelta(days=length - 1)
    dates = [first]

    for i in range(length - 1):
        levels.append(levels[i] * 1 + numpy.random.normal())
        dates.append(datetime.date.fromordinal(dates[i].toordinal() + 1))

    return pd.Series(data=levels, index=dates, dtype=np.dtype(float))


@plot_function
def percentiles(x: pd.Series, y: Optional[pd.Series] = None, w: Union[Window, int, str] = Window(None, 0)) -> pd.Series:
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

    :math:`R_t = \\frac{\\sum_{i=t-N+1}^{t}{[X_i<{Y_t}]}+0.5\\sum_{i=t-N+1}^{t}{[X_i={Y_t}]}}{N}\\times100\\%`

    Where :math:`N` is the number of observations in a rolling window. If :math:`y` is not provided (or is NULL),
    calculates percentiles of :math:`x` over its historical values. If window length :math:`w` is not provided, uses an
    ever-growing history of values. If :math:`w` is greater than the available data size, returns empty.

    **Examples**

    Compute percentile ranks of a series in the sample distribution of a second series over :math:`22` observations

    >>> a = generate_series(100)
    >>> b = generate_series(100)
    >>> percentiles(a, b, 22)

    **See also**

    :func:`zscores`

    """
    if x.empty:
        return x

    if y is None:
        y = x.copy()
    w = normalize_window(y, w)

    if isinstance(w.r, int) and w.r > len(y):
        raise ValueError('Ramp value must be less than the length of the series y.')

    if isinstance(w.w, int) and w.w > len(x):
        return pd.Series(dtype=float)

    res = pd.Series(dtype=np.dtype(float))
    convert_to_date = not isinstance(x.index, pd.DatetimeIndex)

    if isinstance(w.w, pd.DateOffset):
        for idx, val in y.items():
            sample = x.loc[(x.index > ((idx - w.w).date() if convert_to_date else idx - w.w)) & (x.index <= idx)]
            res.loc[idx] = percentileofscore(sample, val, kind='mean')
    elif not y.empty:
        min_periods = 0 if isinstance(w.r, pd.DateOffset) else w.r
        rolling_window = x[:y.index[-1]].rolling(w.w, min_periods)
        percentile_on_x_index = rolling_window.apply(lambda a: percentileofscore(a, y[a.index[-1]:][0], kind="mean"))
        joined_index = pd.concat([x, y], axis=1).index
        res = percentile_on_x_index.reindex(joined_index, method="ffill")[y.index]
    return apply_ramp(res, w)


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
            if isinstance(x.index, pd.DatetimeIndex):
                values = [x.loc[(x.index > (idx - w.w)) & (x.index <= idx)].quantile(n) for idx in x.index]
            else:
                values = [x.loc[(x.index > (idx - w.w).date()) & (x.index <= idx)].quantile(n) for idx in x.index]
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
    :param y: observations of the dependent variable
    :param fit_intercept: whether to calculate intercept in the model

    **Usage**

    Fit `OLS Model <https://en.wikipedia.org/wiki/Ordinary_least_squares>`_ based on observations of the explanatory
    variables(s) X and the dependent variable y. If X and y are not aligned, only use the intersection of dates/times.

    **Examples**

    Run a linear regression on y vs. x1 and x2 and compute the R squared:

    >>> x1 = generate_series(100)
    >>> x2 = generate_series(100)
    >>> y = generate_series(100)
    >>> r = LinearRegression([x1, x2], y, True)
    >>> r.r_squared()

    """

    def __init__(self, X: Union[pd.Series, List[pd.Series]], y: pd.Series, fit_intercept: bool = True):
        if not isinstance(fit_intercept, bool):
            raise MqTypeError('expected a boolean value for "fit_intercept"')

        df = pd.concat(X, axis=1) if isinstance(X, list) else X.to_frame()
        df = sm.add_constant(df) if fit_intercept else df
        df.columns = range(len(df.columns)) if fit_intercept else range(1, len(df.columns) + 1)

        df = df[~df.isin([np.nan, np.inf, -np.inf]).any(axis=1)]  # filter out nan and inf
        y = y[~y.isin([np.nan, np.inf, -np.inf])]
        df_aligned, y_aligned = df.align(y, 'inner', axis=0)  # align series

        self._index_scope = range(0, len(df.columns)) if fit_intercept else range(1, len(df.columns) + 1)
        self._res = sm.OLS(y_aligned, df_aligned).fit()
        self._fit_intercept = fit_intercept

    @plot_method
    def coefficient(self, i: int) -> float:
        """
        Estimated coefficient.

        :param i: 0 for intercept (available if intercept is used), 1 for regression slope
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
        Fitted values computed by evaluating the regression model on the original input X.

        :return: fitted values
        """
        return self._res.fittedvalues

    @plot_method
    def predict(self, X_predict: Union[pd.Series, List[pd.Series]]) -> pd.Series:
        """
        Use the model for prediction.

        :param X_predict: the values for which to predict
        :return: predicted values
        """
        df = pd.concat(X_predict, axis=1) if isinstance(X_predict, list) else X_predict.to_frame()
        return self._res.predict(sm.add_constant(df) if self._fit_intercept else df)

    @plot_method
    def standard_deviation_of_errors(self) -> float:
        """
        Standard deviation of the error term.

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
    If X and y are not aligned, only use the intersection of dates/times.

    **Examples**

    Run linear regressions on y vs. x1 and x2 in a rolling window of 22 observations and compute the R Squared:

    >>> x1 = generate_series(100)
    >>> x2 = generate_series(100)
    >>> y = generate_series(100)
    >>> r = RollingLinearRegression([x1, x2], y, 22)
    >>> r.r_squared()

    """

    def __init__(self, X: Union[pd.Series, List[pd.Series]], y: pd.Series, w: int, fit_intercept: bool = True):
        if not isinstance(fit_intercept, bool):
            raise MqTypeError('expected a boolean value for "fit_intercept"')

        df = pd.concat(X, axis=1) if isinstance(X, list) else X.to_frame()
        df = sm.add_constant(df) if fit_intercept else df
        df.columns = range(len(df.columns)) if fit_intercept else range(1, len(df.columns) + 1)

        if w <= len(df.columns):
            raise MqValueError('Window length must be larger than the number of explanatory variables')

        df = df[~df.isin([np.nan, np.inf, -np.inf]).any(axis=1)]  # filter out nan and inf
        y = y[~y.isin([np.nan, np.inf, -np.inf])]
        df_aligned, y_aligned = df.align(y, 'inner', axis=0)  # align series

        self._X = df_aligned.copy()
        self._res = RollingOLS(y_aligned, df_aligned, w).fit()

    @plot_method
    def coefficient(self, i: int) -> pd.Series:
        """
        Estimated coefficients.

        :param i: 0 for intercept (available if intercept is used), 1 for regression slope.
        :return: estimated coefficients of the i-th predictor
        """
        return self._res.params[i]

    @plot_method
    def r_squared(self) -> pd.Series:
        """
        Coefficients of determination (R Squared) of rolling regressions.

        :return: R Squared
        """
        return self._res.rsquared

    @plot_method
    def fitted_values(self) -> pd.Series:
        """
        Fitted values at the end of each rolling window.

        :return: fitted values
        """
        comp = self._X.mul(self._res.params.values)
        return comp.sum(axis=1, min_count=len(comp.columns))

    @plot_method
    def standard_deviation_of_errors(self) -> pd.Series:
        """
        Standard deviations of the error terms.

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
        if not isinstance(fit, bool):
            raise MqTypeError('expected a boolean value for "fit"')

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

        self.s = s if isinstance(s, pd.Series) else pd.Series([s])
        self.i = i if isinstance(i, pd.Series) else pd.Series([i])
        self.r = r if isinstance(r, pd.Series) else pd.Series([r])
        self.n = n
        self.beta_init = beta
        self.gamma_init = gamma
        self.fit = fit
        self.fit_period = fit_period
        self.beta_fixed = not (self.fit or (self.beta_init is None))
        self.gamma_fixed = not (self.fit or (self.gamma_init is None))

        lens = [len(x) for x in (self.s, self.i, self.r)]
        dtype = float if max(lens) == min(lens) else object
        data = np.array([self.s, self.i, self.r], dtype=dtype).T

        beta_init = self.beta_init if self.beta_init is not None else 0.9
        gamma_init = self.gamma_init if self.gamma_init is not None else 0.01

        parameters, initial_conditions = SIR.get_parameters(self.s.iloc[0], self.i.iloc[0], self.r.iloc[0], n,
                                                            beta=beta_init, gamma=gamma_init,
                                                            beta_fixed=self.beta_fixed, gamma_fixed=self.gamma_fixed,
                                                            S0_fixed=True, I0_fixed=True, R0_fixed=True)
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
        if not isinstance(fit, bool):
            raise MqTypeError('expected a boolean value for "fit"')

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

        self.s = s if isinstance(s, pd.Series) else pd.Series([s])
        self.e = e if isinstance(e, pd.Series) else pd.Series([e])
        self.i = i if isinstance(i, pd.Series) else pd.Series([i])
        self.r = r if isinstance(r, pd.Series) else pd.Series([r])
        self.n = n
        self.beta_init = beta
        self.gamma_init = gamma
        self.sigma_init = sigma
        self.fit = fit
        self.fit_period = fit_period
        self.beta_fixed = not (self.fit or (self.beta is None))
        self.gamma_fixed = not (self.fit or (self.gamma is None))
        self.sigma_fixed = not (self.fit or (self.sigma is None))

        lens = [len(x) for x in (self.s, self.e, self.i, self.r)]
        dtype = float if max(lens) == min(lens) else object
        data = np.array([self.s, self.e, self.i, self.r], dtype=dtype).T

        beta_init = self.beta_init if self.beta_init is not None else 0.9
        gamma_init = self.gamma_init if self.gamma_init is not None else 0.01
        sigma_init = self.sigma_init if self.sigma_init is not None else 0.2

        parameters, initial_conditions = SEIR.get_parameters(self.s.iloc[0], self.e.iloc[0],
                                                             self.i.iloc[0], self.r.iloc[0], n,
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
