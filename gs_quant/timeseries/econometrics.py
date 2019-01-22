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

import math
from .statistics import *
from ..errors import *

"""
Econometrics timeseries library is for standard economic and time series analytics operations, including returns,
diffs, lags, volatilities and other numerical operations which are generally finance-oriented
"""


# Return types
RETURN_TYPE_SIMPLE = "simple"
RETURN_TYPE_LOG = "log"

# Annualization factors
ANNUALIZATION_FACTOR_DAILY = 252
ANNUALIZATION_FACTOR_WEEKLY = 52
ANNUALIZATION_FACTOR_SEMI_MONTHLY = 26
ANNUALIZATION_FACTOR_MONTHLY = 12
ANNUALIZATION_FACTOR_QUARTERLY = 4
ANNUALIZATION_FACTOR_ANNUALLY = 1


def _get_annualization_factor(series):
    prev_idx = series.index[0]
    prev_value = series[0]
    distances = []
    r = []  # returns
    for idx, value in series.iloc[1:].iteritems():
        d = (idx - prev_idx).days
        if d == 0:
            raise MqValueError('multiple data points on same date')
        distances.append(d)
        r.append(value / prev_value - 1)
        prev_idx = idx
        prev_value = value

    average = numpy.average(distances)
    if average < 2.1:
        factor = ANNUALIZATION_FACTOR_DAILY
    elif average <= 6:
        factor = ANNUALIZATION_FACTOR_WEEKLY + ((6 - average) * (ANNUALIZATION_FACTOR_DAILY - ANNUALIZATION_FACTOR_WEEKLY) / 3.9)
    elif average < 8:
        factor = ANNUALIZATION_FACTOR_WEEKLY
    elif average <= 14:
        factor = ANNUALIZATION_FACTOR_SEMI_MONTHLY + ((14 - average) * (ANNUALIZATION_FACTOR_WEEKLY - ANNUALIZATION_FACTOR_SEMI_MONTHLY) / 6)
    elif average < 17:
        factor = ANNUALIZATION_FACTOR_SEMI_MONTHLY
    elif average <= 25:
        factor = ANNUALIZATION_FACTOR_MONTHLY + ((25 - average) * (ANNUALIZATION_FACTOR_SEMI_MONTHLY - ANNUALIZATION_FACTOR_MONTHLY) / 8)
    elif average < 35:
        factor = ANNUALIZATION_FACTOR_MONTHLY
    elif average <= 85:
        factor = ANNUALIZATION_FACTOR_QUARTERLY + ((85 - average) * (ANNUALIZATION_FACTOR_MONTHLY - ANNUALIZATION_FACTOR_QUARTERLY) / 50)
    elif average < 97:
        factor = ANNUALIZATION_FACTOR_QUARTERLY
    elif average <= 364:
        factor = ANNUALIZATION_FACTOR_ANNUALLY + ((364 - average) * (ANNUALIZATION_FACTOR_QUARTERLY - ANNUALIZATION_FACTOR_ANNUALLY) / 279)
    elif average < 386:
        factor = ANNUALIZATION_FACTOR_ANNUALLY
    else:
        raise MqValueError('data points are too far apart')
    return factor


def annualize(series: pd.Series) -> pd.Series:
    """
    Annualize timeseries based on sample observation frequency

    :param series: time series of prices
    :return: date-based time series of annualized values

    **Usage**

    Based on number of days between observations, will determine an annualization factor and then adjust values
    accordingly. Useful for annualizing daily or monthly returns

    :math:`Y_t = X_t * \sqrt{F}`

    Annualization factors as follows, based on period implied by observations:

    =========   =============================
    Period      Annualization Factor (F)
    =========   =============================
    Daily       :math:`252`
    Weekly      :math:`52`
    Bi-Weekly   :math:`26`
    Monthly     :math:`12`
    Quarterly   :math:`4`
    Annually    :math:`1`
    =========   =============================

    **Examples**

    Annualize daily returns series:

    >>> prices = generate_series(100)
    >>> ann = annualize(returns(prices))

    **See also**

    :func:`returns`
    """

    factor = _get_annualization_factor(series)
    return series * math.sqrt(factor)


def lag(series: pd.Series, obs: int=1) -> pd.Series:
    """
    Lag timeseries by a specified number of observations

    :param series: time series of prices
    :param obs: number of observations to lag series
    :return: date-based time series of return

    **Usage**

    Shift the series backwards by a specified number of observations:

    :math:`Y_t =  X_{t-obs}`

    **Examples**

    Lag series by 2 observations:

    >>> prices = generate_series(100)
    >>> lagged = lag(prices, 2)

    **See also**

    :func:`prices`
    """

    # Determine how we want to handle observations prior to start date

    return series.shift(obs)


def returns(series: pd.Series, type: str=RETURN_TYPE_SIMPLE, naiszero: bool=True) -> pd.Series:
    """
    Calculate returns from price series

    :param series: time series of prices
    :param type: returns type
    :param naiszero: returns zero rather than NaN for lagged dates
    :return: date-based time series of return

    **Usage**

    Compute returns series from price levels, based on the value of *type*:

    ======   =============================
    Type     Description
    ======   =============================
    simple   Simple arithmetic returns
    log      Logarithmic returns
    ======   =============================

    *Simple*

    Simple geometric change in asset prices, which can be aggregated across assets

    :math:`Y_t = \\frac{X_t}{X_{t-1}} - 1`

    where :math:`X_t` is the asset price at time :math:`t`

    *Logarithmic*

    Natural logarithm of asset price changes, which can be aggregated through time

    :math:`Y_t = log(X_t) - log(X_{t-1})`

    where :math:`X_t` is the asset price at time :math:`t`

    **Examples**

    Generate price series and take compute returns

    >>> prices = generate_series(100)
    >>> returns = returns(prices)

    **See also**

    :func:`prices`
    """

    if series.size < 1:
        return series

    if type == RETURN_TYPE_SIMPLE:
        ret_series = series / series.shift(1) - 1
    elif type == RETURN_TYPE_LOG:
        log_s = series.apply(math.log)
        ret_series = log_s - log_s.shift(1)
    else:
        raise MqValueError('Unknown returns type (use simple / log)')

    # Ensures prod(1+returns(series)) == index(series)
    if naiszero:
        ret_series[0] = math.nan

    return ret_series


def prices(series: pd.Series, initial: int=1, type: str=RETURN_TYPE_SIMPLE) ->pd.Series:
    """
    Calculate price levels from returns series

    :param series: time series of prices
    :param initial: initial price level
    :param type: returns type (simple, log)
    :return: date-based time series of return

    **Usage**

    Compute price levels from returns series, based on the value of *type*:

    ======   =============================
    Type     Description
    ======   =============================
    simple   Simple arithmetic returns
    log      Logarithmic returns
    ======   =============================

    *Simple*

    Compute asset price series from simple returns:

    :math:`Y_t = (1 + X_{t-1}) Y_{t-1}`

    where :math:`X_t` is the asset price at time :math:`t`

    *Logarithmic*

    Compute asset price series from logarithmic returns:

    :math:`Y_t = e^{X_{t-1}} Y_{t-1}`

    where :math:`X_t` is the asset price at time :math:`t`

    **Examples**

    Generate price series and take compute returns

    >>> series = generate_series(100)
    >>> returns = prices(returns(series))

    **See also**

    :func:`returns` :func:`product` :func:`exp`
    """

    if series.size < 1:
        return series

    if type == RETURN_TYPE_SIMPLE:
        return product(1 + series) * initial
    elif type == RETURN_TYPE_LOG:
        return product(series.apply(math.exp)) * initial
    else:
        raise MqValueError('Unknown returns type (use simple / log)')


def diff(series: pd.Series, lag: int=1, naiszero: bool=True) -> pd.Series:
    """
    Diff observations with given lag

    :param series: time series of prices
    :param lag: number of observations to lag
    :param naiszero: returns zero rather than NaN for lagged dates
    :return: date-based time series of return

    **Usage**

    Compute the difference in series values over a given lag:

    :math:`Y_t = X_t - X_{t-l}`

    where :math:`l` is the number of observations to lag series in diff function

    **Examples**

    Diff prices levels:

    >>> series = generate_series(100)
    >>> returns = diff(series)

    **See also**

    :func:`lag`

    """

    if series.size < 1:
        return series

    ret_series = series - series.shift(lag)

    # Ensures 1+sum(diff(s)) == s
    if naiszero:
        ret_series[0:lag] = 0

    return ret_series


def first(x: pd.Series) -> pd.Series:
    """
    First value of series

    :param x: time series
    :return: time series of first value

    **Usage**

    Return series with first value of X for all dates:

    :math:`Y_t = X_0`

    where :math:`X_0` is the first value in the series

    **Examples**

    Last value of series:

    >>> series = generate_series(100)
    >>> returns = first(series)

    **See also**

    :func:`last`

    """
    return pd.Series(x[0], x.index)


def last(x: pd.Series) -> pd.Series:
    """
    Last value of series

    :param x: time series
    :return: time series of last value

    **Usage**

    Return series with last value of X for all dates:

    :math:`Y_t = X_T`

    where :math:`X_T` is the last value in the series

    **Examples**

    Last value of series:

    >>> series = generate_series(100)
    >>> returns = last(series)

    **See also**

    :func:`first`

    """
    return pd.Series(x[-1], x.index)


def index(x: pd.Series) -> pd.Series:
    """
    Geometric series normalization

    :param x: time series
    :return: normalized time series

    **Usage**

    Divides every value in x by the initial value of x:

    :math:`Y_t = X_t / X_0`

    where :math:`X_0` is the first value in the series

    **Examples**

    Normalize series to 1:

    >>> series = generate_series(100)
    >>> returns = index(series)

    **See also**

    :func:`returns`

    """
    return x / x[0]


def change(x: pd.Series) -> pd.Series:
    """
    Arithmetic series normalization

    :param x: time series
    :return: normalized time series

    **Usage**

    Compute difference of every value from the initial value of x:

    :math:`Y_t = X_t - X_0`

    where :math:`X_0` is the first value in the series

    **Examples**

    Change in level from initial value:

    >>> series = generate_series(100)
    >>> returns = change(series)

    **See also**

    :func:`index`

    """
    return x - x[0]


def max_drawdown(series: pd.Series, window: int=0) -> pd.Series:
    """
    Compute the maximum peak to trough drawdown over a rolling window.

    :param series: time series
    :param window: number of days / observations to use (defaults to length of series)
    :return: time series of rolling maximum drawdown

    **Examples**

    Compute the maximum peak to trough `drawdown <https://en.wikipedia.org/wiki/Drawdown_(economics)>`_

    >>> series = generate_series(100)
    >>> max_drawdown(series)

    **See also**

    :func:`returns`

    """
    window = window or series.size

    rolling_max = series.rolling(window, 0).max()
    result = (series / rolling_max - 1).rolling(window, 0).min()
    return result


def volatility(series: pd.Series, window: int=0) -> pd.Series:
    """
    Realized volatility of price series

    :param series: time series of prices
    :param window: number of observations
    :return: date-based time series of return

    **Usage**

    Calculate rolling annualized realized volatility of a price series over a given window:

    :math:`Y_t = \sqrt{\\frac{1}{N-1} \sum_{i=t-w-1}^t (R_t - \overline{R_t})^2} * \sqrt{252}`

    where N is the number of observations in each rolling window, :math:`w`, :math:`R_t` is the simple return on time
    :math:`t`:

    :math:`R_t = \\frac{X_t}{X_{t-1}} - 1`

    and :math:`\overline{R_t}` is the mean value over the same window:

    :math:`\overline{R_t} = \\frac{\sum_{i=t-w-1}^{t} R_t}{N}`

    If window is not provided, computes realized volatility over the full series

    **Examples**

    Compute rolling :math:`1` month (:math:`22` business day) annualized volatility of price series

    >>> series = generate_series(100)
    >>> returns = volatility(series)

    **See also**

    :func:`std` :func:`annualize` :func:`returns`

    """
    window = window or series.size

    if series.size < 1:
        return series

    return annualize(std(returns(series), window)) * 100


def correlation(series1: pd.Series, series2: pd.Series, window: int=0) -> pd.Series:
    """
    Rolling correlation of two price series

    :param series1: time series of prices
    :param series2: time series of prices
    :param window: number of observations
    :return: date-based time series of return
    """
    window = window or series1.size

    if series1.size < 1:
        return series1

    ret_1 = returns(series1)
    ret_2 = returns(series2)

    return ret_1.rolling(window, 0).corr(ret_2)


def beta(series: pd.Series, benchmark: pd.Series, window: int=0) -> pd.Series:
    """
    Rolling beta of a price series and a corresponding benchmark price series.

    :param series: time series of prices
    :param benchmark: time series of benchmark prices
    :param window: number of observations
    :return: date-based time series of beta

    **Examples**

    Compute rolling :math:`1` month (:math:`22` business day) beta of two price series

    >>> series = generate_series(100)
    >>> benchmark = generate_series(100)
    >>> b = beta(series, benchmark, 22)

    **See also**

    :func:`correlation` :func:`returns`
    """
    window = window or series.size

    ret_series = returns(series)
    ret_benchmark = returns(benchmark)

    cov = ret_series.rolling(window, 0).cov(ret_benchmark.rolling(window, 0))
    result = cov / ret_benchmark.rolling(window, 0).var()

    return result.iloc[1:]  # remove first na val
