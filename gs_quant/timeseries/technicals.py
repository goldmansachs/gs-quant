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
from gs_quant.timeseries import diff, annualize, returns
from .statistics import *

"""
Technicals library is for technical analysis functions on timeseries, including moving averages,
volatility indicators and and other numerical operations which are finance-oriented for analyzing
statistical properties of trading activity, such as price movement and volume changes
"""


@plot_function
def moving_average(x: pd.Series, w: Union[Window, int, str] = Window(None, 0)) -> pd.Series:
    """
    Moving average over specified window

    :param x: time series of prices
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value.  If w is a string, it should be a relative date like '1m', '1d', etc.
              Window size defaults to length of series.
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
def bollinger_bands(x: pd.Series, w: Union[Window, int, str] = Window(None, 0), k: float = 2) -> pd.DataFrame:
    """
    Bollinger bands with given window and width

    :param x: time series of prices
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value.  If w is a string, it should be a relative date like '1m', '1d', etc.
              Window size defaults to length of series.
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
def smoothed_moving_average(x: pd.Series, w: Union[Window, int, str] = Window(None, 0)) -> pd.Series:
    """
    Smoothed moving average over specified window

    :param x: time series of prices
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value.  If w is a string, it should be a relative date like '1m', '1d', etc.
              Window size defaults to length of series.
    :return: date-based time series of return

    **Usage**

    A modified moving average (MMA), running moving average (RMA), or smoothed moving average (SMMA) is defined as:

    :math:`P_{MM,today} = \\frac{(N-1)P_{MM,yesterday} + P_today}{N}`

    where N is the number of observations in each rolling window, :math:`w`. If window is not provided, computes
    rolling mean over the full series

    See `Modified moving average <https://en.wikipedia.org/wiki/Moving_average#Modified_moving_average>`_ for more
    information


    **Examples**

    Generate price series with 100 observations starting from today's date:

    >>> prices = generate_series(100)
    >>> smoothed_moving_average(prices, 22)

    **See also**

    :func:`mean` :func:'moving_average'

    """
    w = normalize_window(x, w)
    window_size = w.w
    ramp = w.r
    means = apply_ramp(mean(x, Window(window_size, 0)), w)
    if means.size < 1:
        return pd.Series()
    initial_moving_average = means[0]
    if (isinstance(ramp, int) and ramp > 0) or isinstance(ramp, pd.DateOffset):
        x = apply_ramp(x, w)

    smoothed_moving_averages = x.copy()
    smoothed_moving_averages *= 0
    smoothed_moving_averages[0] = initial_moving_average
    for i in range(1, len(x)):
        if isinstance(window_size, int):
            window_num_elem = window_size
        else:
            window_num_elem = len(x[(x.index > (x.index[i] - window_size)) & (x.index <= x.index[i])])
        smoothed_moving_averages[i] = ((window_num_elem - 1) * smoothed_moving_averages[i - 1] + x[i]) / window_num_elem
    return smoothed_moving_averages


@plot_function
def relative_strength_index(x: pd.Series, w: Union[Window, int, str] = 14) -> pd.DataFrame:
    """
    Relative Strength Index

    :param x: time series of prices
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value.  If w is a string, it should be a relative date like '1m', '1d', etc.
              Window size defaults to length of series.
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


@plot_function
def exponential_moving_average(x: pd.Series, beta: float = 0.75) -> pd.Series:
    """
    Exponentially weighted moving average

    :param x: time series of prices
    :param beta: how much to weigh the previous observations in the time series, thus controlling how much importance we
        place on the (more distant) past. Must be between 0 (inclusive) and 1 (exclusive)
    :return: date-based time series of return

    **Usage**

    The exponential(ly weighted) moving average (EMA) of a series [:math:`X_0`, :math:`X_1`, :math:`X_2`, ...],
    is defined as:

    :math:`Y_0 = X_0`

    :math:`Y_t = \\beta \cdot Y_{t-1} + (1 - \\beta) \cdot X_t`

    where :math:`\\beta` is the weight we place on the previous average.

    See `Exponential moving average <https://en.wikipedia.org/wiki/Moving_average#Exponential_moving_average>`_ for
    more information

    **Examples**

    Generate price series with 100 observations starting from today's date:

    >>> prices = generate_series(100)
    >>> exponential_moving_average(prices, 0.9)

    **See also**

    :func:`mean` :func:`moving_average` :func:`smoothed_moving_average`

    """
    return x.ewm(alpha=1 - beta, adjust=False).mean()


@plot_function
def exponential_volatility(x: pd.Series, beta: float = 0.75) -> pd.Series:
    """
    Exponentially weighted volatility

    :param x: time series of prices
    :param beta: how much to weigh the previous price in the time series, thus controlling how much importance we
                  place on the (more distant) past. Must be between 0 (inclusive) and 1 (exclusive)
    :return: date-based time series of exponential volatility of the input series

    **Usage**

    Calculates the exponentially weighted standard deviation of the return of the input series, and annualizes the
    standard deviation

    **Examples**

    Generate price series and compute exponentially weighted standard deviation of returns

    >>> prices = generate_series(100)
    >>> exponential_volatility(prices, 0.9)

    The above is equivalent to

    >>> annualize(exponential_std(returns(prices), 0.9)) * 100

    **See also**

    :func:`volatility` :func:`exponential_std` :func:`exponential_spread_volatility`

    """
    return annualize(exponential_std(returns(x), beta)).mul(100)


@plot_function
def exponential_spread_volatility(x: pd.Series, beta: float = 0.75) -> pd.Series:
    """
    Exponentially weighted spread volatility

    :param x: time series of prices
    :param beta: how much to weigh the previous price in the time series, thus controlling how much importance we
                  place on the (more distant) past. Must be between 0 (inclusive) and 1 (exclusive)
    :return: date-based time series of exponential spread volatility of the input series

    **Usage**

    Exponentially weights the daily differences of the input series, calculates the annualized standard deviation

    **Examples**

    Generate price series and compute exponentially weighted standard deviation of returns

    >>> prices = generate_series(100)
    >>> exponential_volatility(prices, 0.9)

    The above is equivalent to

    >>> annualize(exponential_std(diff(prices, 1), 0.9))

    **See also**

    :func:`volatility` :func:`exponential_std` :func:`exponential_volatility`

    """
    return annualize(exponential_std(diff(x, 1), beta))
