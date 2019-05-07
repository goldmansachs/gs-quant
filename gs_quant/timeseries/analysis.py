# Copyright 2018 Goldman Sachs.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
#
# Chart Service will attempt to make public functions (not prefixed with _) from this module available. Such functions
# should be fully documented: docstrings should describe parameters and the return value, and provide a 1-line
# description. Type annotations should be provided for parameters.


import numpy as np
import pandas as pd
from gs_quant.timeseries.datetime import *
from ..errors import *
from .helper import plot_function

"""
Timeseries analysis library contains functions used to analyze properties of timeseries, including laging, differencing,
autocorrelation, co-integration and other operations
"""


@plot_function
def first(x: pd.Series) -> pd.Series:
    """
    First value of series

    :param x: time series
    :return: time series of first value

    **Usage**

    Return series with first value of `X` for all dates:

    :math:`R_t = X_0`

    where :math:`X_0` is the first value in the series

    **Examples**

    Last value of series:

    >>> series = generate_series(100)
    >>> returns = first(series)

    **See also**

    :func:`last`

    """
    return pd.Series(x[0], x.index)


@plot_function
def last(x: pd.Series) -> pd.Series:
    """
    Last value of series

    :param x: time series
    :return: time series of last value

    **Usage**

    Return series with last value of `X` for all dates:

    :math:`R_t = X_T`

    where :math:`X_T` is the last value in the series

    **Examples**

    Last value of series:

    >>> series = generate_series(100)
    >>> returns = last(series)

    **See also**

    :func:`first`

    """
    return pd.Series(x[-1], x.index)


@plot_function
def count(x: pd.Series) -> pd.Series:
    """
    Count observations in series

    :param x: time series
    :return: number of observations

    **Usage**

    Count the number of valid observations in a series:

    :math:`R_t = R_{t-1} + 1`

    if :math:`X_t` is not NaN, and

    :math:`R_t = R_{t-1} + 0`

    if :math:`X_t` is NaN

    **Examples**

    Count observations in series:

    >>> series = generate_series(100)
    >>> count = count(series)

    **See also**

    :func:`sum`

    """
    return x.rolling(x.size, 0).count()


@plot_function
def diff(x: pd.Series, obs: int=1) -> pd.Series:
    """
    Diff observations with given lag

    :param x: time series of prices
    :param obs: number of observations to lag
    :return: date-based time series of return

    **Usage**

    Compute the difference in series values over a given lag:

    :math:`R_t = X_t - X_{t-obs}`

    where :math:`obs` is the number of observations to lag series in diff function

    **Examples**

    Diff prices levels:

    >>> series = generate_series(100)
    >>> returns = diff(series)

    **See also**

    :func:`lag`

    """

    if x.size < 1:
        return x

    ret_series = x - x.shift(obs)

    return ret_series


@plot_function
def lag(x: pd.Series, obs: int=1) -> pd.Series:
    """
    Lag timeseries by a specified number of observations

    :param x: timeseries of prices
    :param obs: number of observations to lag series
    :return: date-based time series of return

    **Usage**

    Shift the series backwards by a specified number of observations:

    :math:`R_t =  X_{t-obs}`

    where :math:`obs` is the number of observations to lag series

    **Examples**

    Lag series by 2 observations:

    >>> prices = generate_series(100)
    >>> lagged = lag(prices, 2)

    **See also**

    :func:`diff`
    """

    # Determine how we want to handle observations prior to start date

    return x.shift(obs)
