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
import re

from gs_quant.datetime import relative_date_add
from gs_quant.timeseries.datetime import *
from .helper import plot_function

"""
Timeseries analysis library contains functions used to analyze properties of timeseries, including laging, differencing,
autocorrelation, co-integration and other operations
"""


@plot_function
def smooth_spikes(x: pd.Series, threshold: float) -> pd.Series:
    """
    Smooth out the spikes of a series. If a point is larger/smaller than (1 +/- threshold) times both neighbors, replace
    it with the average of those neighbours. Note: the first and last points in the input series are dropped.

    :param x: timeseries
    :param threshold: minimum increment to trigger filter
    :return: smoothed timeseries

    **Usage**

    Returns series where values that exceed the threshold relative to both neighbors are replaced.

    **Examples**

    Generate price series and smooth spikes over a threshold of 0.5.

    >>> prices = generate_series(100)
    >>> smooth_spikes(prices, 0.5)

    **See also**

    :func:`exponential_moving_average`
    """
    if len(x) < 3:
        return pd.Series()

    result = x.copy()
    multiplier = (1 + threshold)
    current, next_ = x.iloc[0:2]
    for i in range(1, len(x) - 1):
        previous = current
        current = next_
        next_ = x.iloc[i + 1]

        scaled = current * multiplier
        if (current > previous * multiplier and current > next_ * multiplier) or (previous > scaled and next_ > scaled):
            result.iloc[i] = (previous + next_) / 2

    return result[1:-1]


@plot_function
def repeat(x: pd.Series, n: int = 1) -> pd.Series:
    """
    Repeats values for days where data is missing. For any date with missing data, the last recorded value is used.
    Optionally downsamples the result such that there are data points every n days.

    :param x: date-based timeseries
    :param n: desired frequency of output
    :return: a timeseries that has been forward-filled, and optionally downsampled

    **Usage**

    Fill missing values with last seen value e.g. to combine daily with weekly or monthly data.
    """
    if not 0 < n < 367:
        raise MqValueError('n must be between 0 and 367')
    index = pd.date_range(freq=f'{n}D', start=x.index[0], end=x.index[-1])
    return x.reindex(index, method='ffill')


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
    Last value of series (as a series)

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
    return pd.Series(x.dropna()[-1], x.index)


@plot_function
def last_value(x: pd.Series) -> Union[int, float]:
    """
    Last value of series (as a scalar)

    :param x: time series
    :return: last value

    **Usage**

    Return a scalar value :math:`X_T` where T is the last index value in the series.

    **Examples**

    Last value of series:

    >>> series = generate_series(100)
    >>> lv = last_value(series)

    **See also**

    :func:`last`

    """
    if x.empty:
        raise MqValueError("cannot get last value of an empty series")
    return x.dropna().iloc[-1]


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
def diff(x: pd.Series, obs: int = 1) -> pd.Series:
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
def compare(x: Union[pd.Series, Real], y: Union[pd.Series, Real], method: Interpolate = Interpolate.STEP) \
        -> Union[pd.Series, Real]:
    """
    Compare two series or scalars against each other

    :param x: timeseries or scalar
    :param y: timeseries or scalar
    :param method: interpolation method (default: step). Only used when both x and y are timeseries
    :return: binary timeseries with the result of x relation y or the comparison of the given real numbers

    **Usage**

    Compare two series or scalar variables applying the given interpolation method in case indices of :math:`x`
    and :math:`y` differ. Returns a signal with values of 1, 0, or -1.

    If :math:`X_t > Y_t`, then :math:`R_t = 1`.
    If :math:`X_t = Y_t`, then :math:`R_t = 0`.
    If :math:`X_t < Y_t`, then :math:`R_t = -1`.

    Alignment operators:

    =========   ========================================================================
    Method      Behavior
    =========   ========================================================================
    intersect   Resultant series only has values on the intersection of dates.
                Values for dates present in only one series will be ignored
    nan         Resultant series has values on the union of dates in both series. Values
                for dates only available in one series will be treated as nan in the
                other series, and therefore in the resultant series
    zero        Resultant series has values on the union of dates in both series. Values
                for dates only available in one series will be treated as zero in the
                other series
    step        Resultant series has values on the union of dates in both series. Values
                for dates only available in one series will be interpolated via step
                function in the other series
    time        Resultant series have values on the union of dates / times. Missing
                values surrounded by valid values will be interpolated given length of
                interval. Input series must use DateTimeIndex.
    =========   ========================================================================
    """
    x, y = align(x, y, method)

    return (x > y) * 1.0 + (x < y) * -1.0


class LagMode(Enum):
    TRUNCATE = "truncate"
    EXTEND = "extend"


@plot_function
def lag(x: pd.Series, obs: Union[Window, int, str] = 1, mode: LagMode = LagMode.EXTEND) -> pd.Series:
    """
    Lag timeseries by a number of observations or a relative date.

    :param x: timeseries of prices
    :param obs: non-zero integer (number of observations) or relative date e.g. "-90d", "1d", "1m", "1y"
    :param mode: whether to extend series index (into the future)
    :return: date-based time series of return

    **Usage**

    Shift the series backwards by a specified number of observations:

    :math:`R_t =  X_{t-obs}`

    where :math:`obs` is the number of observations to lag series

    **Examples**

    Lag series by 2 observations:

    >>> prices = generate_series(100)
    >>> lagged = lag(prices, 2)

    Lag series by 1 year:

    >>> prices = generate_series(100)
    >>> lagged = lag(prices, '1y')

    **See also**

    :func:`diff`
    """
    if isinstance(obs, str):
        end = x.index[-1]
        y = x.copy()  # avoid mutating the provided series

        match = re.fullmatch('(\\d+)y', obs)
        if match:
            y.index += pd.DateOffset(years=int(match.group(1)))
            y = y.groupby(y.index).first()
        else:
            y.index += pd.DateOffset(relative_date_add(obs))

        if mode == LagMode.EXTEND:
            return y
        return y[:end]

    obs = getattr(obs, 'w', obs)
    # Determine how we want to handle observations prior to start date
    if mode == LagMode.EXTEND:
        if x.index.resolution != 'day':
            raise MqValueError(f'unable to extend index with resolution {x.index.resolution}')
        kwargs = {'periods': abs(obs) + 1, 'freq': 'D'}
        if obs > 0:
            kwargs['start'] = x.index[-1]
        else:
            kwargs['end'] = x.index[0]
        x = x.reindex(x.index.union(pd.date_range(**kwargs)))
    return x.shift(obs)
