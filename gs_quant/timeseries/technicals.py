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
from gs_quant.timeseries import diff
from .statistics import *

"""
Technicals library is for technical analysis functions on timeseries, including moving averages,
volatility indicators and and other numerical operations which are finance-oriented for analyzing
statistical properties of trading activity, such as price movement and volume changes
"""


@plot_function
def moving_average(x: pd.Series, w: Union[Window, int] = Window(None, 0)) -> pd.Series:
    """
    Moving average over specified window

    :param x: time series of prices
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value. Window size defaults to length of series.
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
    w = normalize_window(x, w)
    return apply_ramp(mean(x, Window(w.w, 0)), w)


@plot_function
def bollinger_bands(x: pd.Series, w: Union[Window, int] = Window(None, 0), k: float = 2) -> pd.DataFrame:
    """
    Bollinger bands with given window and width

    :param x: time series of prices
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value. Window size defaults to length of series.
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
    w = normalize_window(x, w)
    avg = moving_average(x, w)
    sigma_t = std(x, w)

    upper = avg + k * sigma_t
    lower = avg - k * sigma_t

    return pd.concat([lower, upper], axis=1)


@plot_function
def smoothed_moving_average(x: pd.Series, w: Union[Window, int] = Window(None, 0)) -> pd.Series:
    """
    Smoothed moving average over specified window

    :param x: time series of prices
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value. Window size defaults to length of series.
    :return: date-based time series of return

    **Usage**

    A modified moving average (MMA), running moving average (RMA), or smoothed moving average (SMMA) is defined as:

    :math:`P_MM,today = \\frac{(N_1)P_MM,yesterday + P_today}{N}`

    where N is the number of observations in each rolling window, :math:`w`. If window is not provided, computes
    rolling mean over the full series

    See `Modified moving average <https://en.wikipedia.org/wiki/Moving_average#Modified_moving_average>`
    _ for more information


    **Examples**

    Generate price series with 100 observations starting from today's date:

    >>> prices = generate_series(100)
    >>> smoothed_moving_average(prices, 22)

    **See also**

    :func:`mean` :func:'moving_average'

    """
    w = normalize_window(x, w)
    window = w.w
    ramp = w.r
    initial_moving_average = apply_ramp(mean(x, Window(window, 0)), w)[0]
    if ramp > 0:
        x = apply_ramp(x, w)

    smoothed_moving_averages = x.copy()
    smoothed_moving_averages *= 0
    smoothed_moving_averages[0] = initial_moving_average
    for i in range(1, len(x)):
        smoothed_moving_averages[i] = ((window - 1) * smoothed_moving_averages[i - 1] + x[i]) / window
    return smoothed_moving_averages


@plot_function
def relative_strength_index(x: pd.Series, w: Union[Window, int] = 14) -> pd.DataFrame:
    """
    Relative Strength Index

    :param x: time series of prices
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value. Window size defaults to length of series.
    :return: date-based time series of RSI

    **Usage**

    The RSI computes momentum as the ratio of higher closes to lower closes: stocks which have had more or stronger
    positive changes have a higher RSI than stocks which have had more or stronger negative changes.

    See `RSI <https://en.wikipedia.org/wiki/Relative_strength_index>`_ for more information

    **Examples**

    Compute relative strength index over a :math:`14` day window:

    >>> prices = generate_series(100)
    >>> relative_strength_index(prices, 14)

    **See also**

    :func:`moving_average` :func:`std` :func:`smoothed_moving_average`
    """
    w = normalize_window(x, w)
    one_period_change = diff(x, 1)[1:]
    gains = one_period_change.copy()
    losses = one_period_change.copy()
    gains[gains < 0] = 0
    losses[losses > 0] = 0
    losses[losses < 0] *= -1

    moving_avg_gains = smoothed_moving_average(gains, w)
    moving_avg_losses = smoothed_moving_average(losses, w)

    rsi_len = len(moving_avg_gains)
    rsi = moving_avg_gains.copy()
    rsi *= 0

    for index in range(0, rsi_len):
        if moving_avg_losses[index] == 0:
            rsi[index] = 100
        else:
            relative_strength = moving_avg_gains[index] / moving_avg_losses[index]
            rsi[index] = 100 - (100 / (1 + relative_strength))

    return rsi
