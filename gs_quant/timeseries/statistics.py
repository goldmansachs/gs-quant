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


def generate_series(length):
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

    :math:`Y_t = (1 + R)X_{t-1}`

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


generate_series.__annotations__ = {'length': int, 'return': pd.Series}


def absolute(series):
    """
    Absolute value of each element in series

    :param series: date-based time series of prices
    :return: date-based time series of minimum value

    **Usage**

    Return the absolute value of :math:`X`. For each value in time series :math:`X_t`, return :math:`X_t` if :math:`X_t`
    is greater than or equal to 0; otherwise return :math:`-X_t`:

    :math:`Y_t = |X_t|`

    **Examples**

    Generate price series and take absolute value of :math:`X_t-100`

    >>> prices = generate_series(100) - 100
    >>> abs(prices)

    """
    return abs(series)


absolute.__annotations__ = {'series': pd.Series, 'return': pd.Series}


def minimum(series, window=0):
    """
    Minimum value of series over given window

    :param series: date-based time series of prices
    :param window: number of days / observations to use (defaults to length of series)
    :return: date-based time series of minimum value

    **Usage**

    Returns the minimum value of the series over each window:

    :math:`Y_t = min(X_{t-window}:X_t)`

    If window is not provided, returns the minimum value over the full series

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


minimum.__annotations__ = {'series': pd.Series, 'window': int, 'return': pd.Series}


def maximum(series, window=0):
    """
    Maximum value of series over given window

    :param series: date-based time series of prices
    :param window: number of days / observations to use (defaults to length of series)
    :return: date-based time series of maximum value

    **Usage**

    Returns the maximum value of the series over each window:

    :math:`Y_t = max(X_{t-window}:X_t)`

    If window is not provided, returns the minimum value over the full series

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


maximum.__annotations__ = {'series': pd.Series, 'window': int, 'return': pd.Series}


def floor(series, value=0):
    """
    Floor series at minimum value

    :param series: date-based time series of prices
    :param value: minimum value
    :return: date-based time series of maximum value

    **Usage**

    Returns series where all values are greater than or equal to the minimum value.

    :math:`Y_t = max(X_t, value)`

    If window is not provided, operates over the full series

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


floor.__annotations__ = {'series': pd.Series, 'value': int, 'return': pd.Series}


def ceil(series, value=0):
    """
    Cap series at maximum value

    :param series: date-based time series of prices
    :param value: maximum value
    :return: date-based time series of maximum value

    **Usage**

    Returns series where all values are less than or equal to the maximum value.

    :math:`Y_t = min(X_t, value)`

    If window is not provided, operates over the full series

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


ceil.__annotations__ = {'series': pd.Series, 'value': int, 'return': pd.Series}


def mean(series, window=0):
    """
    Arithmetic mean of series over given window

    :param series: date-based time series of prices
    :param window: number of days / observations to use (defaults to length of series)
    :return: date-based time series of mean value

    **Usage**

    :math:`Y_t = \\frac{\sum_{i=t-window}^{t} X_t}{N}`

    where N is the number of observations in each rolling window

    If window is not provided, computes mean over the full series

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


mean.__annotations__ = {'series': pd.Series, 'window': int, 'return': pd.Series}


def median(series, window=0):
    """
    Median value of series over given window

    :param series: date-based time series of prices
    :param window: number of days / observations to use (defaults to length of series)
    :return: date-based time series of median value

    **Usage**

    Computes the median value over a given window. For each window, this function will return the middle value when
    all elements in the window are sorted. If the number of observations in the window is even, will return the average
    of the middle two values.

    If window is not provided, computes median over the full series

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


median.__annotations__ = {'series': pd.Series, 'window': int, 'return': pd.Series}


def mode(series, window=0):
    """
    Most common value in series over given window

    :param series: date-based time series of prices
    :param window: number of days / observations to use (defaults to length of series)
    :return: date-based time series of median value

    **Usage**

    Computes the mode value over a given window. For each window, this function will return the most common value of
    all elements in the window.

    If window is not provided, computes median over the full series

    **Examples**

    Generate price series and compute mode over 22 observations

    >>> prices = generate_series(100)
    >>> mode(prices, 22)

    **See also**

    :func:`mean` :func:`median`
    """
    window = window or series.size
    assert series.index.is_monotonic_increasing
    return series.rolling(window, 0).mode()


mode.__annotations__ = {'series': pd.Series, 'window': int, 'return': pd.Series}


def summation(series, window=0):
    """
    Rolling sum of series over given window

    :param series: date-based time series of prices
    :param window: number of days / observations to use (defaults to length of series)
    :return: date-based time series of median value

    **Usage**

    Returns cumulative sum of the series over a rolling window of size ``window``

    :math:`Y_t = \sum_{i=t-window}^{t} X_t`

    If window is not provided, computes sum over the full series

  **Examples**

    Generate price series and compute rolling sum over 22 observations

    >>> prices = generate_series(100)
    >>> mean(prices, 22)

    **See also**

    :func:`product`

    """
    window = window or series.size
    assert series.index.is_monotonic_increasing
    return series.rolling(window, 0).sum()


summation.__annotations__ = {'series': pd.Series, 'window': int, 'return': pd.Series}


def product(series, window=0):
    """
    Rolling product of series over given window

    :math:`Y_t = \prod_{i=t-window}^{t} X_t`

    If window is not provided, computes product over the full series

    :param series: date-based time series of prices
    :param window: number of days / observations to use (defaults to length of series)
    :return: date-based time series of median value
    """
    window = window or series.size
    assert series.index.is_monotonic_increasing
    return series.rolling(window, 0).agg(pd.Series.prod)


product.__annotations__ = {'series': pd.Series, 'window': int, 'return': pd.Series}


def std(series, window=0):
    """
    Rolling standard deviation of series over given window

    :math:`Y_t = \sqrt{\\frac{1}{N-1} \sum_{i=t-window}^t (X_t - \overline{X_t})^2}`

    where N is the number of observations in each rolling window and :math:`\overline{X_t}` is the mean value over
    the same window:

    :math:`\overline{X_t} = \\frac{\sum_{i=t-window}^{t} X_t}{N}`

    If window is not provided, computes standard deviation over the full series

    Provides `unbiased estimator <https://en.wikipedia.org/wiki/Unbiased_estimation_of_standard_deviation>`_ of
    sample standard deviation

    :param series: date-based time series of prices
    :param window: number of days / observations to use (defaults to length of series)
    :return: date-based time series of median value
    """
    window = window or series.size
    assert series.index.is_monotonic_increasing
    return series.rolling(window, 0).std()

std.__annotations__ = {'series': pd.Series, 'window': int, 'return': pd.Series}


def var(series, window=0):
    """
    Rolling variance of series over given window

    :math:`Y_t = \\frac{1}{N-1} \sum_{i=t-window}^t (X_t - \overline{X_t})^2`

    where N is the number of observations in each rolling window and :math:`\overline{X_t}` is the mean value over
    the same window:

    :math:`\overline{X_t} = \\frac{\sum_{i=t-window}^{t} X_t}{N}`

    If window is not provided, computes variance over the full series

    Provides `unbiased estimator <https://en.wikipedia.org/wiki/Unbiased_estimation_of_standard_deviation>`_ of
    sample variance

    :param series: date-based time series of prices
    :param window: number of days / observations to use (defaults to length of series)
    :return: date-based time series of median value
    """
    window = window or series.size
    assert series.index.is_monotonic_increasing
    return series.rolling(window, 0).var()


var.__annotations__ = {'series': pd.Series, 'window': int, 'return': pd.Series}


def _zscore(series):
    if series.size < 1:
        return series

    if series.size == 1:
        return 0

    return stats.zscore(series)[-1]


def zscore(series, window=0):
    """
    Rolling z-score over a given window

    :math:`Y_t = \\frac { X_t - \mu }{ \sigma }`

    Where :math:`\mu` and :math:`\sigma` are sample mean and standard deviation over the given window

    z-score represents the `standard score <https://en.wikipedia.org/wiki/Standard_score>`_ of each value :math:`X_t`

    :param series: time series of prices
    :param window: number of observations
    :return: date-based time series of return

    **See also**

    :func:`mean` :func:`std`

    """
    if series.size < 1:
        return series

    if not window:
        return pd.Series(stats.zscore(series), series.index)

    return series.rolling(window, 0).apply(_zscore)


zscore.__annotations__ = {'series': pd.Series, 'window': int, 'return': pd.Series}


def winsorize(series, limit=2.5, window=0):
    """
    Limit extreme values in series

    Cap and floor values in the series which have a z-score greater or less than provided value. This function will
    restrict the distribution of values. Calculates the sample standard deviation and adjusts values which
    fall outside the specified range to be equal to the upper or lower limits

    Lower and upper limits are defined as:

    :math:`upper = \mu + \sigma \\times limit`

    :math:`lower = \mu - \sigma \\times limit`

    Where :math:`\mu` and :math:`\sigma` are sample mean and standard deviation. The series is restricted by:

    :math:`Y_t = max( min( X_t, upper), lower )`

    See `winsorising <https://en.wikipedia.org/wiki/Winsorizing>`_ for additional information

    :param series: time series of prices
    :param limit: max z-score of values
    :param window: number of observations
    :return: date-based time series of return
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


winsorize.__annotations__ = {'series': pd.Series, 'limit': float, 'window': int, 'return': pd.Series}
