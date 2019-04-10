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

from .statistics import *

"""
Technicals library is for technical analysis functions on timeseries, including moving averages,
volatility indicators and and other numerical operations which are finance-oriented for analyzing 
statistical properties of trading activity, such as price movement and volume changes
"""


@plot_function
def moving_average(x: pd.Series, w: int = 22) -> pd.Series:
    """
    Moving average over specified window

    :param x: time series of prices
    :param w: window: number of observations to use (defaults to length of series)
    :return: date-based time series of return

    **Usage**

    Simple arithmetic moving average over the specified window (number of observations). Shorter windows will be more
    reactive to changes in the asset price, but more volatile. Larger windows will be smoother but less reactive to
    near term changes in asset prices.

    :math:`R_t = \\frac{\sum_{i=t-w+1}^{t} X_t}{N}`

    where N is the number of observations in each rolling window, :math:`w`. If window is not provided, computes
    rolling mean over the full series

    Equivalent to ``mean``

    **Examples**

    Generate price series with 100 observations starting from today's date:

    >>> prices = generate_series(100)
    >>> moving_average(prices, 22)

    **See also**

    :func:`mean`

    """

    return mean(x, w)


@plot_function
def bollinger_bands(x: pd.Series, w: int = 20, k: float = 2) -> pd.DataFrame:
    """
    Bollinger bands with given window and width

    :param x: time series of prices
    :param w: window: number of observations to use (defaults to length of series)
    :param k: band width in standard deviations (default: 2)
    :return: date-based time series of return

    **Usage**

    Standard deviation bands around the moving average of asset price level. Bollinger bands can be used to determine
    a range around the price level which responds to local volatility changes. Returns two series,
    upper, :math:`u_t` and lower, :math:`l_t`

    :math:`u_t = \\bar{X_t} + k\sigma_t`

    :math:`l_t = \\bar{X_t} - k\sigma_t`

    where :math:`\\bar{X_t}` is the moving average over specified window, and :math:`\\sigma_t` is the rolling
    standard deviation over the specified window

    See `Bollinger Bands <https://en.wikipedia.org/wiki/Bollinger_Bands>`_ for more information

    **Examples**

    Compute bollinger bands around :math:`20` day moving average at :math:`2` standard deviations:

    >>> prices = generate_series(100)
    >>> bollinger_bands(prices, 20, 2)

    **See also**

    :func:`moving_average` :func:`std`
    """

    avg = moving_average(x, w)
    sigma_t = std(x, w)

    upper = avg + k * sigma_t
    lower = avg - k * sigma_t

    return pd.concat([lower, upper], axis=1)
