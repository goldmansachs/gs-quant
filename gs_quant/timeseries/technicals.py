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
from enum import Enum
from typing import Union

import pandas as pd
import statsmodels.tsa.seasonal

from gs_quant.timeseries import diff, annualize, returns
from .algebra import subtract
from .helper import Window, plot_function, normalize_window, apply_ramp
from .statistics import mean, std, exponential_std
from ..errors import MqValueError

"""
Technicals library is for technical analysis functions on timeseries, including moving averages,
volatility indicators and and other numerical operations which are finance-oriented for analyzing
statistical properties of trading activity, such as price movement and volume changes
"""


class Seasonality(Enum):
    MONTH = 'month'
    QUARTER = 'quarter'


class SeasonalModel(Enum):
    ADDITIVE = 'additive'
    MULTIPLICATIVE = 'multiplicative'


class Frequency(Enum):
    WEEK = 'week'
    MONTH = 'month'
    QUARTER = 'quarter'
    YEAR = 'year'


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

    :math:`R_t = \\frac{\\sum_{i=t-w+1}^{t} X_t}{N}`

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
    if x.empty:
        return pd.Series(dtype=float)
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

    :math:`u_t = \\bar{X_t} + k\\sigma_t`

    :math:`l_t = \\bar{X_t} - k\\sigma_t`

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
        return pd.Series(dtype=float)
    initial_moving_average = means.iloc[0]
    if (isinstance(ramp, int) and ramp > 0) or isinstance(ramp, pd.DateOffset):
        x = apply_ramp(x, w)

    smoothed_moving_averages = x.copy()
    smoothed_moving_averages *= 0
    smoothed_moving_averages.iloc[0] = initial_moving_average
    for i in range(1, len(x)):
        if isinstance(window_size, int):
            window_num_elem = window_size
        else:
            window_num_elem = len(x[(x.index > (x.index[i] - window_size).date()) & (x.index <= x.index[i])])
        smoothed_moving_averages.iloc[i] = (
            (window_num_elem - 1) * smoothed_moving_averages.iloc[i - 1] + x.iloc[i]
        ) / window_num_elem
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
        if moving_avg_losses.iloc[index] == 0:
            rsi.iloc[index] = 100
        else:
            relative_strength = moving_avg_gains.iloc[index] / moving_avg_losses.iloc[index]
            rsi.iloc[index] = 100 - (100 / (1 + relative_strength))

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

    :math:`Y_t = \\beta \\cdot Y_{t-1} + (1 - \\beta) \\cdot X_t`

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
def macd(x: pd.Series, m: int = 12, n: int = 26, s: int = 1) -> pd.Series:
    """
    Moving average convergence divergence (MACD).

    Moving average convergence divergence (MACD) is a trend-following momentum indicator that shows the relationship
    between two moving averages of a timeseries. It is the result of subtracting the exponential moving average of `x`
    with a period of :math:`m` from the exponential moving average of :math:`x` with a period of :math:`n`.

    Optionally, specify :math:`s` to apply an exponential moving average to the resulting series with a period of
    :math:`s` (default 1, equivalent to no exponential moving average).

    :param x: time series
    :param m: period of first, short exponential moving average (default 12)
    :param n: period of second, long exponential moving average (default 26)
    :param s: optional smoothing parameter (default 1)
    :return: date-based time series of return

    **Usage**

    The exponential(ly weighted) moving average (EMA) of a series [:math:`X_0`, :math:`X_1`, :math:`X_2`, ...],
    is defined as:

    :math:`Y_0 = X_0`

    :math:`Y_t = \\beta \\cdot Y_{t-1} + (1 - \\beta) \\cdot X_t`

    where :math:`\\beta = \\frac{2}{\\text{period} + 1}` is the weight we place on the previous average.

    The MACD of a series is defined as :math:`\\text{EMA}(\\text{EMA}(X, M) - \\text{EMA}(X, N), S)`

    **Examples**

    Generate price series with 100 observations starting from today's date:

    >>> prices = generate_series(100)
    >>> macd(prices, 12, 26)

    **See also**

    :func:`exponential_moving_average` :func:`moving_average` :func:`smoothed_moving_average`

    """
    a = x.ewm(adjust=False, span=m).mean()
    b = x.ewm(adjust=False, span=n).mean()
    return subtract(a, b).ewm(adjust=False, span=s).mean()


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


@plot_function
def stochastic_oscillator(x: pd.Series, w: Union[Window, int, str] = 14, s: int = 3) -> pd.DataFrame:
    """
    Stochastic Oscillator (%K and %D)

    :param x: time series of prices
    :param w: Window or int: lookback period for %K calculation. e.g. Window(14, 10) where 14 is the window size
              and 10 the ramp up value.  If w is a string, it should be a relative date like '1m', '1d', etc.
              Defaults to 14 observations.
    :param s: smoothing period for %D (simple moving average of %K). Defaults to 3.
    :return: DataFrame with two columns: 'pctK' and 'pctD'

    **Usage**

    The `Stochastic Oscillator <https://en.wikipedia.org/wiki/Stochastic_oscillator>`_ is a momentum indicator that
    compares a security's closing price to its price range over a given lookback period. It generates values between
    0 and 100.

    %K (fast stochastic) is calculated as:

    :math:`\\%K_t = \\frac{X_t - L_w}{H_w - L_w} \\times 100`

    where :math:`X_t` is the current price, :math:`L_w` is the lowest price over window :math:`w`, and :math:`H_w`
    is the highest price over window :math:`w`.

    %D (slow stochastic) is the simple moving average of %K over :math:`s` periods:

    :math:`\\%D_t = \\frac{1}{s} \\sum_{i=0}^{s-1} \\%K_{t-i}`

    Readings above 80 are generally considered overbought, while readings below 20 are considered oversold.
    A common trading signal is when %K crosses above or below %D.

    **Examples**

    Generate price series and compute stochastic oscillator with default 14-day lookback:

    >>> prices = generate_series(100)
    >>> stochastic_oscillator(prices, 14, 3)

    **See also**

    :func:`relative_strength_index` :func:`moving_average`

    """
    w = normalize_window(x, w)
    if x.empty:
        return pd.DataFrame(columns=['pctK', 'pctD'], dtype=float)

    if isinstance(w.w, pd.DateOffset):
        rolling_low = x.rolling(w.w).min()
        rolling_high = x.rolling(w.w).max()
    else:
        rolling_low = x.rolling(w.w, min_periods=1).min()
        rolling_high = x.rolling(w.w, min_periods=1).max()

    high_low_range = rolling_high - rolling_low
    # Avoid division by zero when high == low (flat price)
    high_low_range = high_low_range.replace(0, float('nan'))

    pct_k = ((x - rolling_low) / high_low_range) * 100
    pct_d = pct_k.rolling(s, min_periods=1).mean()

    pct_k = apply_ramp(pct_k, w)
    pct_d = apply_ramp(pct_d, w)

    result = pd.concat([pct_k, pct_d], axis=1)
    result.columns = ['pctK', 'pctD']
    return result


@plot_function
def average_true_range(x: pd.Series, w: Union[Window, int, str] = 14) -> pd.Series:
    """
    Average True Range (ATR)

    :param x: time series of prices
    :param w: Window or int: size of window and ramp up to use. e.g. Window(14, 10) where 14 is the window size
              and 10 the ramp up value.  If w is a string, it should be a relative date like '1m', '1d', etc.
              Defaults to 14 observations.
    :return: date-based time series of ATR

    **Usage**

    The `Average True Range <https://en.wikipedia.org/wiki/Average_true_range>`_ is a volatility indicator that
    measures the degree of price movement for a given period. When only closing prices are available (as opposed
    to OHLC data), the True Range simplifies to the absolute change between consecutive prices:

    :math:`TR_t = |X_t - X_{t-1}|`

    The ATR is then the moving average of the True Range over the specified window:

    :math:`ATR_t = \\frac{1}{w} \\sum_{i=t-w+1}^{t} TR_i`

    Higher ATR values indicate higher volatility. Unlike percentage-based volatility measures, ATR is expressed
    in the same units as the price series, making it useful for setting stop-loss levels or position sizing.

    **Examples**

    Generate price series and compute ATR over a 14-day window:

    >>> prices = generate_series(100)
    >>> average_true_range(prices, 14)

    **See also**

    :func:`bollinger_bands` :func:`exponential_volatility` :func:`moving_average`

    """
    w = normalize_window(x, w)
    if x.empty:
        return pd.Series(dtype=float)

    # True Range: when only close prices are available, TR = |close_t - close_{t-1}|
    true_range = x.diff().abs()

    return apply_ramp(mean(true_range, Window(w.w, 0)), w)


def _freq_to_period(x: pd.Series, freq: Frequency = Frequency.YEAR):
    """
    Given input series x with a DateTimeIndex and a desired temporal frequency (period), returns x with all NaNs
    forward-filled (according to x's index's DateTime frequency) and the number of data points in a period.

    freq should be the length of time in which x's cycles repeat. For example: yearly retail sales cycle, yearly
    temperature fluctuation cycle.

    For example: 1) If x is a daily series and freq = YEARLY, then there are 365 data points in a period; 2) If x is
    a monthly series and freq = QUARTERLY, then there are 3 data points in a period.

    Freq parameter only applies when data frequency is:
    'B' and frequency == Weekly --> period = 5
    'B' and frequency == Monthly --> convert to 'D' and period = 30
    'D' and frequency == Weekly --> period = 7
    'D' and frequency == Monthly --> period = 30
    'M' and frequency == Quarterly --> Period = 3
    'W' and frequency == Quarterly --> period = 13
    """
    if not isinstance(x.index, pd.DatetimeIndex):
        raise MqValueError("Series must have a pandas.DateTimeIndex.")
    pfreq = getattr(getattr(x, 'index', None), 'inferred_freq', None)
    # Some older versions of statsmodels don't handle some of the newer pandas frequencies, so we manually adjust them
    pfreq = 'MS' if pfreq in ('ME', 'M') else pfreq  # Convert Month[End] into MonthlyStart
    pfreq = 'QS' if pfreq in ('QE-DEC', 'QE') else pfreq  # Convert Quarter[End] into QuarterlyStart
    period = None if pfreq is None else statsmodels.tsa.seasonal.freq_to_period(pfreq)
    if period in [7, None]:  # daily
        x = x.asfreq('D', method='ffill')
        if freq == Frequency.YEAR:
            return x, 365
        elif freq == Frequency.QUARTER:
            return x, 91
        elif freq == Frequency.MONTH:
            return x, 30
        else:
            return x, 7
    elif period == 5:  # business day
        if freq == Frequency.YEAR:
            return x.asfreq('D', method='ffill'), 365
        if freq == Frequency.QUARTER:
            return x.asfreq('D', method='ffill'), 91
        elif freq == Frequency.MONTH:
            return x.asfreq('D', method='ffill'), 30
        else:  # freq == Frequency.WEEKLY:
            return x.asfreq('B', method='ffill'), 5
    elif period == 52:  # weekly frequency
        x = x.asfreq('W', method='ffill')
        if freq == Frequency.YEAR:
            return x, period
        elif freq == Frequency.QUARTER:
            return x, 13
        elif freq == Frequency.MONTH:
            return x, 4
        else:
            raise MqValueError(f'Frequency {freq.value} not compatible with series with frequency {pfreq}.')
    elif period == 12:  # monthly frequency
        x = x.asfreq('ME', method='ffill')
        if freq == Frequency.YEAR:
            return x, period
        elif freq == Frequency.QUARTER:
            return x, 3
        else:
            raise MqValueError(f'Frequency {freq.value} not compatible with series with frequency {pfreq}.')
    return x, period


def _seasonal_decompose(x: pd.Series, method: SeasonalModel = SeasonalModel.ADDITIVE, freq: Frequency = Frequency.YEAR):
    x, period = _freq_to_period(x, freq)
    if x.shape[0] < 2 * period:
        # Replace ValueError in seasonal_decompose with more descriptive error
        raise MqValueError(f"Series must have two complete cycles to be analyzed. Series has only {x.shape[0]} dpts.")
    decompose_obj = statsmodels.tsa.seasonal.seasonal_decompose(x, period=period, model=method.value)
    return decompose_obj


@plot_function
def seasonally_adjusted(
    x: pd.Series, method: SeasonalModel = SeasonalModel.ADDITIVE, freq: Frequency = Frequency.YEAR
) -> pd.Series:
    """
    Seasonally adjusted series

    :param x: time series with at least two years worth of data.
    :param method: 'additive' or 'multiplicative'. Type of seasonal model to use. 'multiplicative' is appropriate when
        the magnitude of the series's values affect the magnitude of seasonal swings; 'additive' is appropriate
        when seasonal swings' sizes are independent of the series's values.
    :param freq: 'year', 'quarter', 'month', or 'week'. Period in which full cycle occurs (i.e. the "period" of
        a wave).
    :return: date-based time series of seasonally-adjusted input series.

    **Usage**

    Uses a centered moving average and convolution to decompose the input series into seasonal, trend, and
    residual components. This function returns the series with the seasonal component removed.

    If using the default additive model:

    :math:`Y_t = X_t - S_t`

    If using the multiplicative model:

    :math:`Y_t = X_t / S_t`

    **Examples**

    Generate price series and compute seasonally-adjusted series.

    >>> prices = generate_series(1000)
    >>> seasonally_adjusted(prices)

    **See also**

    :func:`trend`

    """
    decompose_obj = _seasonal_decompose(x, method, freq)
    if method == SeasonalModel.ADDITIVE:
        return decompose_obj.trend + decompose_obj.resid
    else:
        return decompose_obj.trend * decompose_obj.resid


@plot_function
def trend(x: pd.Series, method: SeasonalModel = SeasonalModel.ADDITIVE, freq: Frequency = Frequency.YEAR) -> pd.Series:
    """
    Trend of series with seasonality and residuals removed.

    :param x: time series with at least two years worth of data.
    :param method: 'additive' or 'multiplicative'. Type of seasonal model to use. 'multiplicative' is appropriate when
        the magnitude of the series's values affect the magnitude of seasonal swings; 'additive' is appropriate
        when seasonal swings' sizes are independent of the series's values.
    :param freq: 'year', 'quarter', 'month', or 'week'. Period in which full cycle occurs (i.e. the "period" of
        a wave).
    :return: date-based time series with trend of input series.

    **Usage**

    Uses a centered moving average and convolution to decompose the input series into seasonal, trend, and
    residual components. This function returns the trend component.

    If using the default additive model:

    :math:`Y_t = X_t - S_t - R_t`

    If using the multiplicative model:

    :math:`Y_t = X_t / (S_t * R_t)`

    **Examples**

    Generate price series and compute its trend.

    >>> prices = generate_series(1000)
    >>> trend(prices)

    **See also**

    :func:`seasonally_adjusted`

    """
    decompose_obj = _seasonal_decompose(x, method, freq)
    return decompose_obj.trend
