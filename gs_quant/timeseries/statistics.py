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

import numpy
import pandas as pd
import datetime
import scipy.stats.mstats as stats
from scipy.stats import percentileofscore

from .algebra import *

"""
Stats library is for basic arithmetic and statistical operations on timeseries.
These include basic algebraic operations, probability and distribution analysis.
Generally not finance-specific routines.
"""


@plot_function
def min_(x: pd.Series, w: int = 0) -> pd.Series:
    """
    Minimum value of series over given window

    :param x: series: timeseries
    :param w: window: number of observations to use (defaults to length of series)
    :return: timeseries of minimum value

    **Usage**

    Returns the minimum value of the series over each window:

    :math:`R_t = min(X_{t-w+1}:X_t)`

    where :math:`w` is the size of the rolling window. If window is not provided, returns the minimum value over the
    full series. If the window size is greater than the available data, will return minimum of available values.

    **Examples**

    Minimum value of price series over the last :math:`22` observations:

    >>> prices = generate_series(100)
    >>> min_(prices, 22)

    **See also**

    :func:`max_`

    """
    w = w or x.size
    assert x.index.is_monotonic_increasing, "series index is monotonic increasing"
    return x.rolling(w, 0).min()


@plot_function
def max_(x: pd.Series, w: int = 0) -> pd.Series:
    """
    Maximum value of series over given window

    :param x: series: timeseries
    :param w: window: number of observations to use (defaults to length of series)
    :return: timeseries of maximum value

    **Usage**

    Returns the maximum value of the series over each window:

    :math:`R_t = max(X_{t-w+1}:X_t)`

    where :math:`w` is the size of the rolling window. If window is not provided, returns the minimum value over the
    full series. If the window size is greater than the available data, will return minimum of available values.

    **Examples**

    Maximum value of price series over the last :math:`22` observations:

    >>> prices = generate_series(100)
    >>> max_(prices, 22)

    **See also**

    :func:`min_`

    """
    w = w or x.size
    assert x.index.is_monotonic_increasing, "series index is monotonic increasing"
    return x.rolling(w, 0).max()


@plot_function
def range_(x: pd.Series, w: int = 0) -> pd.Series:
    """
    Range of series over given window

    :param x: series: timeseries
    :param w: window: number of observations to use (defaults to length of series)
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
    w = w or x.size
    assert x.index.is_monotonic_increasing, "series index is monotonic increasing"

    max = max_(x, w)
    min = min_(x, w)

    return max - min


@plot_function
def mean(x: pd.Series, w: int = 0) -> pd.Series:
    """
    Arithmetic mean of series over given window

    :param x: series: timeseries
    :param w: window: number of observations to use (defaults to length of series)
    :return: timeseries of mean value

    **Usage**

    Calculates `arithmetic mean <https://en.wikipedia.org/wiki/Arithmetic_mean>`_ of the series over a rolling window

    :math:`R_t = \\frac{\sum_{i=t-w+1}^{t} X_i}{N}`

    where :math:`N` is the number of observations in each rolling window, :math:`w`. If window is not provided, computes
    rolling mean over the full series. If the window size is greater than the available data, will return mean of
    available values.

    **Examples**

    Generate price series and compute mean over :math:`22` observations

    >>> prices = generate_series(100)
    >>> mean(prices, 22)

    **See also**

    :func:`median` :func:`mode`

    """
    w = w or x.size
    assert x.index.is_monotonic_increasing, "series index is monotonic increasing"
    return x.rolling(w, 0).mean()


@plot_function
def median(x: pd.Series, w: int = 0) -> pd.Series:
    """
    Median value of series over given window

    :param x: series: timeseries
    :param w: window: number of observations to use (defaults to length of series)
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
    w = w or x.size
    assert x.index.is_monotonic_increasing, "series index is monotonic increasing"
    return x.rolling(w, 0).median()


@plot_function
def mode(x: pd.Series, w: int = 0) -> pd.Series:
    """
    Most common value in series over given window

    :param x: series: timeseries
    :param w: window: number of observations to use (defaults to length of series)
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
    w = w or x.size
    assert x.index.is_monotonic_increasing, "series index is monotonic increasing"
    return x.rolling(w, 0).apply(lambda y: stats.mode(y).mode, raw=True)


@plot_function
def sum_(x: pd.Series, w: int = 0) -> pd.Series:
    """
    Rolling sum of series over given window

    :param x: series: timeseries
    :param w: window: number of observations to use (defaults to length of series)
    :return: timeseries of rolling sum

    **Usage**

    Calculate the sum of observations over a given rolling window. For each time, :math:`t`, returns the value
    of all observations from :math:`t-w+1` to :math:`t` summed together:

    :math:`R_t = \sum_{i=t-w+1}^{t} X_i`

    where :math:`w` is the size of the rolling window. If window is not provided, computes sum over the full series

    **Examples**

    Generate price series and compute rolling sum over :math:`22` observations

    >>> prices = generate_series(100)
    >>> sum_(prices, 22)

    **See also**

    :func:`product`

    """
    w = w or x.size
    assert x.index.is_monotonic_increasing
    return x.rolling(w, 0).sum()


@plot_function
def product(x: pd.Series, w: int = 0) -> pd.Series:
    """
    Rolling product of series over given window

    :param x: series: timeseries
    :param w: window: number of observations to use (defaults to length of series)
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
    w = w or x.size
    assert x.index.is_monotonic_increasing
    return x.rolling(w, 0).agg(pd.Series.prod)


@plot_function
def std(x: pd.Series, w: int = 0) -> pd.Series:
    """
    Rolling standard deviation of series over given window

    :param x: series: timeseries
    :param w: window: number of observations to use (defaults to length of series)
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
    w = w or x.size
    assert x.index.is_monotonic_increasing, "series index is monotonic increasing"
    return x.rolling(w, 0).std()


@plot_function
def var(x: pd.Series, w: int = 0) -> pd.Series:
    """
    Rolling variance of series over given window

    :param x: series: timeseries
    :param w: window: number of observations to use (defaults to length of series)
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
    w = w or x.size
    assert x.index.is_monotonic_increasing, "series index is monotonic increasing"
    return x.rolling(w, 0).var()


@plot_function
def cov(x: pd.Series, y: pd.Series, w: int = 0) -> pd.Series:
    """
    Rolling co-variance of series over given window

    :param x: series: timeseries
    :param y: series: timeseries
    :param w: window: number of observations to use (defaults to length of series)
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
    w = w or x.size
    assert x.index.is_monotonic_increasing, "series index is monotonic increasing"
    return x.rolling(w, 0).cov(y)


def _zscore(x):
    if x.size == 1:
        return 0

    return stats.zscore(x, ddof=1)[-1]


@plot_function
def zscores(x: pd.Series, w: int = 0) -> pd.Series:
    """
    Rolling z-scores over a given window

    :param x: time series of prices
    :param w: window: number of observations to use (defaults to length of series)
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

    if not w:

        if x.size == 1:
            return pd.Series([0.0], index=x.index)

        clean_series = x.dropna()
        zscore_series = pd.Series(stats.zscore(clean_series, ddof=1), clean_series.index)
        return interpolate(zscore_series, x, Interpolate.NAN)

    return x.rolling(w, 0).apply(_zscore, raw=False)


@plot_function
def winsorize(x: pd.Series, limit: float = 2.5, w: int = 0) -> pd.Series:
    """
    Limit extreme values in series

    :param x: time series of prices
    :param limit: max z-score of values
    :param w: window: number of observations to use (defaults to length of series)
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
    w = w or x.size

    if x.size < 1:
        return x

    assert w, "window is not 0"

    mu = x.mean()
    sigma = x.std()

    high = mu + sigma * limit
    low = mu - sigma * limit

    ret = ceil(x, high)
    ret = floor(ret, low)

    return ret


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

    return pd.Series(data=levels, index=dates)


@plot_function
def percentile(x: pd.Series, y: pd.Series, w: int = 0) -> pd.Series:
    """
    Rolling percentile over given window

    :param x: value series
    :param y: distribution series
    :param w: window: number of observations
    :return: timeseries of percentile

    **Usage**

    Calculate `percentile rank <https://en.wikipedia.org/wiki/Percentile_rank>`_of :math:`y` in the sample distribution
    of :math:`x` over a rolling window of length :math:`w`:

    :math:`R_t = \\frac{\sum_{i=t-N+1}^{t}{[X_i<{Y_t}]}+0.5\sum_{i=t-N+1}^{t}{[X_i={Y_t}]}}{N}\\times100\%`

    Where :math:`N` is the number of observations in a rolling window. If window length :math:'w' is not provided, uses
    an ever-growing history of values. If :math:'w' is greater than the available data size, returns empty.

    **Examples**

    Compute percentile ranks of a series in the sample distribution of a second series over :math:`22` observations

    >>> a = generate_series(100)
    >>> b = generate_series(100)
    >>> percentile(a, b, 22)

    **See also**

    :func:`zscores`

    """
    if x.empty:
        return x

    res = pd.Series()
    for idx, val in y.iteritems():
        sample = x[x.index <= idx]
        if w:
            if len(sample) < w:
                continue
            sample = sample[-w:]

        res.loc[idx] = percentileofscore(sample, val, kind='mean')

    return res
