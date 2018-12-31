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

Marquee Plot Service will attempt to make public functions (not prefixed with _) from this module available.
Such functions should be fully documented: docstrings should describe parameters and the return value, and provide
a 1-line description. Type annotations should be provided for parameters.

Stats library is for basic arithmetic and statistical operations on timeseries.
These include basic algebraic operations, probability and distribution analysis.
Generally not finance-specific routines.
"""

import numpy
import pandas as pd
import datetime


def generate_series(length):
    """
    Generate sample timeseries.
    :param length: number of observations
    :return: date-based time series of randomly generated prices
    """
    levels = [100]
    dates = [datetime.date.today()]

    for i in range(length-1):
        levels.append(levels[i] * 1 + numpy.random.normal())
        dates.append(datetime.date.fromordinal(dates[i].toordinal()+1))

    return pd.Series(data=levels, index=dates)


generate_series.__annotations__ = {'length': int, 'return': pd.Series}


def absolute(series):
    """
    Absolute value of each element in series
    :param series: date-based time series of prices
    :return: date-based time series of minimum value
    """
    return abs(series)


absolute.__annotations__ = {'series': pd.Series, 'return': pd.Series}


def minimum(series, window=0):
    """
    Calculate minimum value of series over given window.
    :param series: date-based time series of prices
    :param window: number of days / observations to use (defaults to length of series)
    :return: date-based time series of minimum value
    """
    window = window or series.size
    assert series.index.is_monotonic_increasing
    return series.rolling(window, 0).min()


minimum.__annotations__ = {'series': pd.Series, 'window': int, 'return': pd.Series}


def maximum(series, window=0):
    """
    Calculate maximum value of series over given window.
    :param series: date-based time series of prices
    :param window: number of days / observations to use (defaults to length of series)
    :return: date-based time series of maximum value
    """
    window = window or series.size
    assert series.index.is_monotonic_increasing
    return series.rolling(window, 0).max()


maximum.__annotations__ = {'series': pd.Series, 'window': int, 'return': pd.Series}


def mean(series, window=0):
    """
    Calculate mean value of series over given window.
    :param series: date-based time series of prices
    :param window: number of days / observations to use (defaults to length of series)
    :return: date-based time series of mean value
    """
    window = window or series.size
    assert series.index.is_monotonic_increasing
    return series.rolling(window, 0).mean()


mean.__annotations__ = {'series': pd.Series, 'window': int, 'return': pd.Series}


def median(series, window=0):
    """
    Calculate median value of series over given window.
    :param series: date-based time series of prices
    :param window: number of days / observations to use (defaults to length of series)
    :return: date-based time series of median value
    """
    window = window or series.size
    assert series.index.is_monotonic_increasing
    return series.rolling(window, 0).median()


median.__annotations__ = {'series': pd.Series, 'window': int, 'return': pd.Series}


def summation(series, window=0):
    """
    Calculate rolling sum of series over given window.
    :param series: date-based time series of prices
    :param window: number of days / observations to use (defaults to length of series)
    :return: date-based time series of median value
    """
    window = window or series.size
    assert series.index.is_monotonic_increasing
    return series.rolling(window, 0).sum()


summation.__annotations__ = {'series': pd.Series, 'window': int, 'return': pd.Series}


def product(series, window=0):
    """
    Calculate rolling product of series over given window.
    :param series: date-based time series of prices
    :param window: number of days / observations to use (defaults to length of series)
    :return: date-based time series of median value
    """
    window = window or series.size
    assert series.index.is_monotonic_increasing
    return series.rolling(window, 0).agg(pd.Series.prod)


product.__annotations__ = {'series': pd.Series, 'window': int, 'return': pd.Series}


def standard_deviation(series, window=0):
    """
    Calculate rolling standard deviation of series over given window.
    :param series: date-based time series of prices
    :param window: number of days / observations to use (defaults to length of series)
    :return: date-based time series of median value
    """
    window = window or series.size
    assert series.index.is_monotonic_increasing
    return series.rolling(window, 0).std()


standard_deviation.__annotations__ = {'series': pd.Series, 'window': int, 'return': pd.Series}


def variance(series, window=0):
    """
    Calculate rolling variance of series over given window.
    :param series: date-based time series of prices
    :param window: number of days / observations to use (defaults to length of series)
    :return: date-based time series of median value
    """
    window = window or series.size
    assert series.index.is_monotonic_increasing
    return series.rolling(window, 0).var()


variance.__annotations__ = {'series': pd.Series, 'window': int, 'return': pd.Series}
