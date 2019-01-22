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

"""
Stats library is for basic arithmetic and statistical operations on timeseries.
These include basic algebraic operations, probability and distribution analysis.
Generally not finance-specific routines.
"""


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


def exp(series: pd.Series) -> pd.Series:
    """
    Exponential of series

    :param series: time series
    :return: exponential of each element

    **Usage**

    For each element in the series, :math:`X_t`, raise :math:`e` (Euler's number) to the power of :math:`X_t`.
    Euler's number is the base of the natural logarithm, :math:`ln`.

    :math:`Y_t = e^{X_t}`

    **Examples**

    Raise :math:`e` to the power :math:`1`. Returns Euler's number, approximately 2.71828

    >>> exp(1)

    **See also**

    :func:`log`

    """
    return numpy.exp(series)


def log(series: pd.Series) -> pd.Series:
    """
    Natural logarithm of series

    :param series: time series
    :return: series with exponential of each element

    **Usage**

    For each element in the series, :math:`X_t`, return the natural logarithm :math:`ln` of :math:`X_t`
    The natural logarithm is the logarithm in base :math:`e`.

    :math:`Y_t = log(X_t)`

    This function is the inverse of the exponential function.

    More information on `logarithms <https://en.wikipedia.org/wiki/Logarithm>`_

    **Examples**

    Take natural logarithm of 3

    >>> log(3)

    **See also**

    :func:`exp`

    """
    return numpy.log(series)


def absolute(series: pd.Series) -> pd.Series:
    """
    Absolute value of each element in series

    :param series: date-based time series of prices
    :return: date-based time series of minimum value

    **Usage**

    Return the absolute value of :math:`X`. For each value in time series :math:`X_t`, return :math:`X_t` if :math:`X_t`
    is greater than or equal to 0; otherwise return :math:`-X_t`:

    :math:`Y_t = |X_t|`

    Equivalent to :math:`Y_t = \sqrt{X_t^2}`

    **Examples**

    Generate price series and take absolute value of :math:`X_t-100`

    >>> prices = generate_series(100) - 100
    >>> abs(prices)

    **See also**

    :func:`exp` :func:`sqrt`

    """
    return abs(series)


def minimum(series: pd.Series, window: int=0) -> pd.Series:
    """
    Minimum value of series over given window

    :param series: date-based time series of prices
    :param window: number of days / observations to use (defaults to length of series)
    :return: date-based time series of minimum value

    **Usage**

    Returns the minimum value of the series over each window:

    :math:`Y_t = min(X_{t-w-1}:X_t)`

    where :math:`w` is the size of the rolling window. If window is not provided, returns the minimum value over the full series

    **Examples**

    Minimum value of price series over the last 22 observations:

    >>> prices = generate_series(100)
    >>> min(prices, 22)

    **See also**

    :func:`maximum`

    """
    window = window or series.size
    assert series.index.is_monotonic_increasing
    return series.rolling(window, 0).min()


def maximum(series: pd.Series, window: int=0) -> pd.Series:
    """
    Maximum value of series over given window

    :param series: date-based time series of prices
    :param window: number of days / observations to use (defaults to length of series)
    :return: date-based time series of maximum value

    **Usage**

    Returns the maximum value of the series over each window:

    :math:`Y_t = max(X_{t-w-1}:X_t)`

    where :math:`w` is the size of the rolling window. If window is not provided, returns the minimum value over the full series

    **Examples**

    Maximum value of price series over the last 22 observations:

    >>> prices = generate_series(100)
    >>> maximum(prices, 22)

    **See also**

    :func:`minimum`

    """
    window = window or series.size
    assert series.index.is_monotonic_increasing
    return series.rolling(window, 0).max()


def floor(series: pd.Series, value: float=0) -> pd.Series:
    """
    Floor series at minimum value

    :param series: date-based time series of prices
    :param value: minimum value
    :return: date-based time series of maximum value

    **Usage**

    Returns series where all values are greater than or equal to the minimum value.

    :math:`Y_t = max(X_t, value)`

    See `Floor and Ceil functions <https://en.wikipedia.org/wiki/Floor_and_ceiling_functions>`_ for more details

    **Examples**

    Generate price series and floor all values at 100

    >>> prices = generate_series(100)
    >>> floor(prices, 100)

    **See also**

    :func:`ceil`

    """
    assert series.index.is_monotonic_increasing
    return series.apply(lambda x: max(x, value))


def ceil(series: pd.Series, value: float=0) -> pd.Series:
    """
    Cap series at maximum value

    :param series: date-based time series of prices
    :param value: maximum value
    :return: date-based time series of maximum value

    **Usage**

    Returns series where all values are less than or equal to the maximum value.

    :math:`Y_t = min(X_t, value)`

    See `Floor and Ceil functions <https://en.wikipedia.org/wiki/Floor_and_ceiling_functions>`_ for more details

    **Examples**

    Generate price series and floor all values at 100

    >>> prices = generate_series(100)
    >>> floor(prices, 100)

    **See also**

    :func:`floor`

    """
    assert series.index.is_monotonic_increasing
    return series.apply(lambda x: min(x, value))


def mean(series: pd.Series, window: int=0) -> pd.Series:
    """
    Arithmetic mean of series over given window

    :param series: date-based time series of prices
    :param window: number of days / observations to use (defaults to length of series)
    :return: date-based time series of mean value

    **Usage**

    :math:`Y_t = \\frac{\sum_{i=t-w-1}^{t} X_t}{N}`

    where N is the number of observations in each rolling window, :math:`w`. If window is not provided, computes
    rolling mean over the full series

    **Examples**

    Generate price series and compute mean over 22 observations

    >>> prices = generate_series(100)
    >>> mean(prices, 22)

    **See also**

    :func:`median` :func:`mode`

    """
    window = window or series.size
    assert series.index.is_monotonic_increasing
    return series.rolling(window, 0).mean()


def median(series: pd.Series, window: int=0) -> pd.Series:
    """
    Median value of series over given window

    :param series: date-based time series of prices
    :param window: number of days / observations to use (defaults to length of series)
    :return: date-based time series of median value

    **Usage**

    Computes the median value over a given window. For each window, this function will return the middle value when
    all elements in the window are sorted. If the number of observations in the window is even, will return the average
    of the middle two values.

    :math:`d = \\frac{w-1}{2}`

    :math:`Y_t = \\frac{X_{\lfloor t-d \\rfloor} + X_{\lceil t-d \\rceil}}{2}`

    where :math:`w` is the size of the rolling window. If window is not provided, computes median over the full series

    **Examples**

    Generate price series and compute median over 22 observations

    >>> prices = generate_series(100)
    >>> median(prices, 22)

    **See also**

    :func:`mean` :func:`mode`
    """
    window = window or series.size
    assert series.index.is_monotonic_increasing
    return series.rolling(window, 0).median()


def mode(series: pd.Series, window: int=0) -> pd.Series:
    """
    Most common value in series over given window

    :param series: date-based time series of prices
    :param window: number of days / observations to use (defaults to length of series)
    :return: date-based time series of modal value

    **Usage**

    Computes the mode value over a given window. For each window, this function will return the most common value of
    all elements in the window.

    If window is not provided, computes mode over the full series

    **Examples**

    Generate price series and compute mode over 22 observations

    >>> prices = generate_series(100)
    >>> mode(prices, 22)

    **See also**

    :func:`mean` :func:`median`
    """
    window = window or series.size
    assert series.index.is_monotonic_increasing
    return series.rolling(window, 0).apply(lambda x: stats.mode(x).mode)


def summation(series: pd.Series, window: int=0) -> pd.Series:
    """
    Rolling sum of series over given window

    :param series: date-based time series of prices
    :param window: number of days / observations to use (defaults to length of series)
    :return: date-based time series of median value

    **Usage**

    Calculate the sum of observations over a given rolling window. For each time, :math:`t`, returns the value
    of all observations from :math:`t-w-1` to :math:`t` summed together:

    :math:`Y_t = \sum_{i=t-w-1}^{t} X_t`

    where :math:`w` is the size of the rolling window. If window is not provided, computes sum over the full series

    **Examples**

    Generate price series and compute rolling sum over 22 observations

    >>> prices = generate_series(100)
    >>> summation(prices, 22)

    **See also**

    :func:`product`

    """
    window = window or series.size
    assert series.index.is_monotonic_increasing
    return series.rolling(window, 0).sum()


def product(series: pd.Series, window: int=0) -> pd.Series:
    """
    Rolling product of series over given window

    :param series: date-based time series of prices
    :param window: number of days / observations to use (defaults to length of series)
    :return: date-based time series of median value

    **Usage**

    Calculate the product of observations over a given rolling window. For each time, :math:`t`, returns the value
    of all observations from :math:`t-w-1` to :math:`t` multiplied together:

    :math:`Y_t = \prod_{i=t-w-1}^{t} X_t`

    where :math:`w` is the size of the rolling window. If window is not provided, computes product over the full series

    **Examples**

    Generate price series and compute rolling sum over 22 observations

    >>> prices = generate_series(100)
    >>> product(1+returns(prices))

    **See also**

    :func:`summation`
    """
    window = window or series.size
    assert series.index.is_monotonic_increasing
    return series.rolling(window, 0).agg(pd.Series.prod)


def std(series: pd.Series, window: int=0) -> pd.Series:
    """
    Rolling standard deviation of series over given window

    :param series: date-based time series of prices
    :param window: number of days / observations to use (defaults to length of series)
    :return: date-based time series of median value

    **Usage**

    Provides `unbiased estimator <https://en.wikipedia.org/wiki/Unbiased_estimation_of_standard_deviation>`_ of sample
    standard deviation over a rolling window:

    :math:`Y_t = \sqrt{\\frac{1}{N-1} \sum_{i=t-w-1}^t (X_t - \overline{X_t})^2}`

    where N is the number of observations in each rolling window, :math:`w`, and :math:`\overline{X_t}` is the mean
    value over the same window:

    :math:`\overline{X_t} = \\frac{\sum_{i=t-w-1}^{t} X_t}{N}`

    If window is not provided, computes standard deviation over the full series

    **Examples**

    Generate price series and compute standard deviation of returns over 22 observations

    >>> prices = generate_series(100)
    >>> std(returns(prices), 22)

    **See also**

    :func:`sum` :func:`mean` :func:`var`

    """
    window = window or series.size
    assert series.index.is_monotonic_increasing
    return series.rolling(window, 0).std()


def var(series: pd.Series, window: int=0) -> pd.Series:
    """
    Rolling variance of series over given window

    :param series: date-based time series of prices
    :param window: number of days / observations to use (defaults to length of series)
    :return: date-based time series of median value

    **Usage**

    Provides `unbiased estimator <https://en.wikipedia.org/wiki/Unbiased_estimation_of_standard_deviation>`_ of sample
    variance over a rolling window:

    :math:`Y_t = \\frac{1}{N-1} \sum_{i=t-w-1}^t (X_t - \overline{X_t})^2`

    where N is the number of observations in each rolling window, :math:`w`, and :math:`\overline{X_t}` is the mean
    value over the same window:

    :math:`\overline{X_t} = \\frac{\sum_{i=t-w-1}^{t} X_t}{N}`

    If window is not provided, computes variance over the full series

    **Examples**

    Generate price series and compute variance of returns over 22 observations

    >>> prices = generate_series(100)
    >>> var(returns(prices), 22)

    **See also**

    :func:`sum` :func:`mean` :func:`std`

    """
    window = window or series.size
    assert series.index.is_monotonic_increasing
    return series.rolling(window, 0).var()


def _zscore(series):
    if series.size < 1:
        return series

    if series.size == 1:
        return 0

    return stats.zscore(series)[-1]


def zscore(series: pd.Series, window: int=0) -> pd.Series:
    """
    Rolling z-score over a given window

    :param series: time series of prices
    :param window: number of observations
    :return: date-based time series of return

    **Usage**

    Calculate `standard score <https://en.wikipedia.org/wiki/Standard_score>`_ of each value in series over given
    window. Standard deviation and sample mean are computed over the specified rolling window, then element is
    normalized to provide a rolling z-score:

    :math:`Y_t = \\frac { X_t - \mu }{ \sigma }`

    Where :math:`\mu` and :math:`\sigma` are sample mean and standard deviation over the given window

    If window is not provided, computes z-score relative to mean and standard deviation over the full series

    **Examples**

    Generate price series and compute variance of returns over 22 observations

    >>> prices = generate_series(100)
    >>> zscore(returns(prices), 22)

    **See also**

    :func:`mean` :func:`std`

    """
    if series.size < 1:
        return series

    if not window:
        return pd.Series(stats.zscore(series), series.index)

    return series.rolling(window, 0).apply(_zscore)


def winsorize(series: pd.Series, limit: float=2.5, window: int=0) -> pd.Series:
    """
    Limit extreme values in series

    :param series: time series of prices
    :param limit: max z-score of values
    :param window: number of observations
    :return: date-based time series of return

    **Usage**

    Cap and floor values in the series which have a z-score greater or less than provided value. This function will
    restrict the distribution of values. Calculates the sample standard deviation and adjusts values which
    fall outside the specified range to be equal to the upper or lower limits

    Lower and upper limits are defined as:

    :math:`upper = \mu + \sigma \\times limit`

    :math:`lower = \mu - \sigma \\times limit`

    Where :math:`\mu` and :math:`\sigma` are sample mean and standard deviation. The series is restricted by:

    :math:`Y_t = max( min( X_t, upper), lower )`

    See `winsorising <https://en.wikipedia.org/wiki/Winsorizing>`_ for additional information

    **Examples**

    Generate price series and winsorize z-score of returns over 22 observations

    >>> prices = generate_series(100)
    >>> winsorize(zscore(returns(prices), 22))

    **See also**

    :func:`zscore` :func:`mean` :func:`std`

    """
    window = window or series.size

    if series.size < 1:
        return series

    assert window

    mu = series.mean()
    sigma = series.std()

    high = mu + sigma * limit
    low = mu - sigma * limit

    ret = ceil(series, high)
    ret = floor(ret, low)

    return ret
