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
from functools import reduce
import warnings

from gs_quant.errors import MqTypeError
from .datetime import *
from .helper import plot_function

"""
Algebra library contains basic numerical and algebraic operations, including addition, division, multiplication,
division and other functions on timeseries
"""


class FilterOperator(Enum):
    LESS = 'less_than'
    GREATER = 'greater_than'
    L_EQUALS = 'l_equals'
    G_EQUALS = 'g_equals'
    EQUALS = 'equals'
    N_EQUALS = 'not_equals'


@plot_function
def add(x: Union[pd.Series, Real], y: Union[pd.Series, Real], method: Interpolate = Interpolate.STEP) \
        -> Union[pd.Series, Real]:
    """
    Add two series or scalars

    :param x: timeseries or scalar
    :param y: timeseries or scalar
    :param method: interpolation method (default: step). Only used when both x and y are timeseries
    :return: timeseries of x + y or sum of the given real numbers

    **Usage**

    Add two series or scalar variables with the given interpolation method

    :math:`R_t =  X_t + Y_t`

    Alignment operators:

    =========   ========================================================================
    Method      Behavior
    =========   ========================================================================
    intersect   Resultant series only has values on the intersection of dates. Values
                for dates present in only one series will be ignored
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

    **Examples**

    Add two series:

    >>> a = generate_series(100)
    >>> b = generate_series(100)
    >>> add(a, b, Interpolate.STEP)

    **See also**

    :func:`subtract`
    """

    if isinstance(x, Real) and isinstance(y, Real):
        return x + y

    [x_align, y_align] = align(x, y, method)
    return x_align.add(y_align)


@plot_function
def subtract(x: Union[pd.Series, Real], y: Union[pd.Series, Real], method: Interpolate = Interpolate.STEP) \
        -> Union[pd.Series, Real]:
    """
    Add two series or scalars

    :param x: timeseries or scalar
    :param y: timeseries or scalar
    :param method: index alignment operator (default: intersect). Only used when both x and y are timeseries
    :return: timeseries of x - y or difference between the given real numbers

    **Usage**

    Subtracts one series or scalar from another applying the given interpolation method

    :math:`R_t =  X_t - Y_t`

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

    **Examples**

    Subtract one series from another:

    >>> a = generate_series(100)
    >>> b = generate_series(100)
    >>> subtract(a, b, Interpolate.STEP)

    **See also**

    :func:`add`
    """

    # Determine how we want to handle observations prior to start date

    if isinstance(x, Real) and isinstance(y, Real):
        return x - y

    [x_align, y_align] = align(x, y, method)
    return x_align.subtract(y_align)


@plot_function
def multiply(x: Union[pd.Series, Real], y: Union[pd.Series, Real], method: Interpolate = Interpolate.STEP) \
        -> Union[pd.Series, Real]:
    """
    Multiply two series or scalars

    :param x: timeseries or scalar
    :param y: timeseries or scalar
    :param method: interpolation method (default: step). Only used when both x and y are timeseries
    :return: timeseries of x * y or product of the given real numbers

    **Usage**

    Multiply two series or scalar variables applying the given interpolation method

    :math:`R_t =  X_t \\times Y_t`

    Alignment operators:

    =========   ========================================================================
    Method      Behavior
    =========   ========================================================================
    intersect   Resultant series only has values on the intersection of dates. Values
                for dates present in only one series will be ignored
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

    **Examples**

    Multiply two series:

    >>> a = generate_series(100)
    >>> b = generate_series(100)
    >>> multiply(a, b, Interpolate.STEP)

    **See also**

    :func:`divide`
    """

    if isinstance(x, Real) and isinstance(y, Real):
        return x * y

    [x_align, y_align] = align(x, y, method)
    return x_align.multiply(y_align)


@plot_function
def divide(x: Union[pd.Series, Real], y: Union[pd.Series, Real], method: Interpolate = Interpolate.STEP) \
        -> Union[pd.Series, Real]:
    """
    Divide two series or scalars

    :param x: timeseries or scalar
    :param y: timeseries or scalar
    :param method: interpolation method (default: step). Only used when both x and y are timeseries
    :return: timeseries of x / y or quotient of the given real numbers

    **Usage**

    Divide two series or scalar variables applying the given interpolation method

    :math:`R_t =  X_t / Y_t`

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

    **Examples**

    Divide two series:

    >>> a = generate_series(100)
    >>> b = generate_series(100)
    >>> divide(a, b, Interpolate.STEP)

    **See also**

    :func:`multiply`
    """

    if isinstance(x, Real) and isinstance(y, Real):
        return x / y

    [x_align, y_align] = align(x, y, method)
    return x_align.divide(y_align)


@plot_function
def floordiv(x: Union[pd.Series, Real], y: Union[pd.Series, Real], method: Interpolate = Interpolate.STEP) \
        -> Union[pd.Series, Real]:
    """
    Floor divide two series or scalars

    :param x: timeseries or scalar
    :param y: timeseries or scalar
    :param method: interpolation method (default: step). Only used for operating two series
    :return: timeseries of x // y or quotient of the floor division of the given real numbers

    **Usage**

    Divide two series or scalar variables applying the given interpolation method

    :math:`R_t =  X_t / Y_t`

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
    =========   ========================================================================

    **Examples**

    Floor divide two series:

    >>> a = generate_series(100)
    >>> b = generate_series(100)
    >>> floordiv(a, b, Interpolate.STEP)

    **See also**

    :func:`divide`
    """

    if isinstance(x, Real) and isinstance(y, Real):
        return x // y

    [x_align, y_align] = align(x, y, method)
    return x_align.floordiv(y_align)


@plot_function
def exp(x: pd.Series) -> pd.Series:
    """
    Exponential of series

    :param x: timeseries
    :return: exponential of each element

    **Usage**

    For each element in the series, :math:`X_t`, raise :math:`e` (Euler's number) to the power of :math:`X_t`.
    Euler's number is the base of the natural logarithm, :math:`ln`.

    :math:`R_t = e^{X_t}`

    **Examples**

    Raise :math:`e` to the power :math:`1`. Returns Euler's number, approximately 2.71828

    >>> exp(1)

    **See also**

    :func:`log`

    """
    return np.exp(x)


@plot_function
def log(x: pd.Series) -> pd.Series:
    """
    Natural logarithm of series

    :param x: timeseries
    :return: series with exponential of each element

    **Usage**

    For each element in the series, :math:`X_t`, return the natural logarithm :math:`ln` of :math:`X_t`
    The natural logarithm is the logarithm in base :math:`e`.

    :math:`R_t = log(X_t)`

    This function is the inverse of the exponential function.

    More information on `logarithms <https://en.wikipedia.org/wiki/Logarithm>`_

    **Examples**

    Take natural logarithm of 3

    >>> log(3)

    **See also**

    :func:`exp`

    """
    return np.log(x)


@plot_function
def power(x: pd.Series, y: float = 1) -> pd.Series:
    """
    Raise each element in series to power

    :param x: timeseries
    :param y: value
    :return: date-based time series of square roots

    **Usage**

    Raise each value in time series :math:`X_t` to the power :math:`y`:

    :math:`R_t = X_t^{y}`

    **Examples**

    Generate price series and raise each value to the power 2:

    >>> prices = generate_series(100)
    >>> power(prices, 2)

    **See also**

    :func:`sqrt`

    """
    return np.power(x, y)


@plot_function
def sqrt(x: Union[Real, pd.Series]) -> Union[Real, pd.Series]:
    """
    Square root of (a) each element in a series or (b) a real number

    :param x: date-based time series of prices or real number
    :return: date-based time series of square roots or square root of given number

    **Usage**

    Return the square root of each value in time series :math:`X_t`:

    :math:`R_t = \\sqrt{X_t}`

    **Examples**

    Generate price series and take square root of each value:

    >>> prices = generate_series(100)
    >>> sqrt(prices)

    **See also**

    :func:`pow`

    """
    if isinstance(x, pd.Series):
        return np.sqrt(x)

    result = math.sqrt(x)
    # return int if result is integral (should work for values up to 2**53)
    return round(result) if round(result) == result else result


@plot_function
def abs_(x: pd.Series) -> pd.Series:
    """
    Absolute value of each element in series

    :param x: date-based time series of prices
    :return: date-based time series of absolute value

    **Usage**

    Return the absolute value of :math:`X`. For each value in time series :math:`X_t`, return :math:`X_t` if :math:`X_t`
    is greater than or equal to 0; otherwise return :math:`-X_t`:

    :math:`R_t = |X_t|`

    Equivalent to :math:`R_t = \sqrt{X_t^2}`

    **Examples**

    Generate price series and take absolute value of :math:`X_t-100`

    >>> prices = generate_series(100) - 100
    >>> abs_(prices)

    **See also**

    :func:`exp` :func:`sqrt`

    """
    return abs(x)


@plot_function
def floor(x: pd.Series, value: float = 0) -> pd.Series:
    """
    Floor series at minimum value

    :param x: date-based time series of prices
    :param value: minimum value
    :return: date-based time series of maximum value

    **Usage**

    Returns series where all values are greater than or equal to the minimum value.

    :math:`R_t = max(X_t, value)`

    See `Floor and Ceil functions <https://en.wikipedia.org/wiki/Floor_and_ceiling_functions>`_ for more details

    **Examples**

    Generate price series and floor all values at 100

    >>> prices = generate_series(100)
    >>> floor(prices, 100)

    **See also**

    :func:`ceil`

    """
    assert x.index.is_monotonic_increasing
    return x.apply(lambda y: max(y, value))


@plot_function
def ceil(x: pd.Series, value: float = 0) -> pd.Series:
    """
    Cap series at maximum value

    :param x: date-based time series of prices
    :param value: maximum value
    :return: date-based time series of maximum value

    **Usage**

    Returns series where all values are less than or equal to the maximum value.

    :math:`R_t = min(X_t, value)`

    See `Floor and Ceil functions <https://en.wikipedia.org/wiki/Floor_and_ceiling_functions>`_ for more details

    **Examples**

    Generate price series and floor all values at 100

    >>> prices = generate_series(100)
    >>> floor(prices, 100)

    **See also**

    :func:`floor`

    """
    assert x.index.is_monotonic_increasing
    return x.apply(lambda y: min(y, value))


@plot_function
def filter_(x: pd.Series, operator: Optional[FilterOperator] = None, value: Optional[Real] = None) -> pd.Series:
    """
    Removes values where comparison with the operator and value combination results in true, defaults to removing
    missing values from the series

    :param x: timeseries
    :param operator: FilterOperator describing logic for value removal, e.g 'less_than'
    :param value: number indicating value(s) to remove from the series
    :return: timeseries with specified values removed


    **Usage**

    Remove each value determined by operator and value from timeseries where that expression yields true

    **Examples**

    Remove 0 from time series

    >>> prices = generate_series(100)
    >>> filter_(prices, FilterOperator.EQUALS, 0)

    Remove positive numbers from time series

    >>> prices = generate_series(100)
    >>> filter_(prices, FilterOperator.GREATER, 0)

    Remove missing values from time series

    >>> prices = generate_series(100)
    >>> filter_(prices)

    """

    if value is None and operator is None:
        x = x.dropna(axis=0, how='any')
    elif value is None:
        raise MqValueError('No value is specified for the operator')
    else:
        if operator == FilterOperator.EQUALS:
            remove = x == value
        elif operator == FilterOperator.GREATER:
            remove = x > value
        elif operator == FilterOperator.LESS:
            remove = x < value
        elif operator == FilterOperator.L_EQUALS:
            remove = x <= value
        elif operator == FilterOperator.G_EQUALS:
            remove = x >= value
        elif operator == FilterOperator.N_EQUALS:
            remove = x != value
        else:
            if not isinstance(operator, str):
                operator = str(operator)
            raise MqValueError('Unexpected operator: ' + operator)
        x = x.drop(x[remove].index)
    return x


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
    # Deprecation warning
    warnings.simplefilter('once')
    message = "This function will be moved to timeseries.analysis.smooth_spikes on October 1, 2021."
    warnings.warn(message, DeprecationWarning)
    warnings.simplefilter('ignore')

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
    # Deprecation warning
    message = "This function will be moved to timeseries.analysis.smooth_spikes on October 1, 2021."
    warnings.simplefilter('once')
    warnings.warn(message, DeprecationWarning)
    warnings.simplefilter('ignore')

    if not 0 < n < 367:
        raise MqValueError('n must be between 0 and 367')
    index = pd.date_range(freq=f'{n}D', start=x.index[0], end=x.index[-1])
    return x.reindex(index, method='ffill')


def _sum_boolean_series(*series):
    if not 2 <= len(series) <= 100:
        raise MqValueError('expected between 2 and 100 arguments')

    for s in series:
        if not isinstance(s, pd.Series):
            raise MqTypeError('all arguments must be series')
        if not all(map(lambda a: a in (0, 1), s.values)):
            raise MqValueError(f'cannot perform operation on series with value(s) other than 1 and 0: {s.values}')

    current = series[0].add(series[1], fill_value=0)
    for s in series[2:]:
        current = current.add(s, fill_value=0)
    return current


@plot_function
def and_(*series: pd.Series) -> pd.Series:
    """
    Logical "and" of two or more boolean series.

    :param series: input series
    :return: result series (of numeric type, with booleans represented as 1s and 0s)
    """
    s = _sum_boolean_series(*series)
    return (s == len(series)).astype(int)


@plot_function
def or_(*series: pd.Series) -> pd.Series:
    """
    Logical "or" of two or more boolean series.

    :param series: input series
    :return: result series (of numeric type, with booleans represented as 1s and 0s)
    """
    s = _sum_boolean_series(*series)
    return (s > 0).astype(int)


@plot_function
def not_(series: pd.Series) -> pd.Series:
    """
    Logical negation of a single boolean series.

    :param series: single input series
    :return: result series (of numeric type, with booleans represented as 1s and 0s)
    """
    if not all(map(lambda a: a in (0, 1), series.values)):
        raise MqValueError(f'cannot negate series with value(s) other than 1 and 0: {series.values}')
    return series.replace([0, 1], [1, 0])


@plot_function
def if_(flags: pd.Series, x: Union[pd.Series, float], y: Union[pd.Series, float]) -> pd.Series:
    """
    Returns a series s. For i in the index of flags, s[i] = x[i] if flags[i] == 1 else y[i].

    :param flags: series of 1s and 0s
    :param x: values to use when flag is 1
    :param y: values to use when flag is 0
    :return: result series

    **Usage**

    Returns a series based off the given conditional series. If the condition is true it shows the first series's value
    else it shows the second series's value.

    **PlotTool Example**

    if(SPX.spot() > 4000, SPX.spot(), GSTHHVIP.spot())

    The above expression would show SPX.spot() if the spot price is above 4000 else it shows GSTHHVIP.spot().

    """
    if not all(map(lambda a: a in (0, 1), flags.values)):
        raise MqValueError(f'cannot perform "if" on series with value(s) other than 1 and 0: {flags.values}')

    def ensure_series(s):
        if isinstance(s, (float, int)):
            return flags, pd.Series([s] * flags.shape[0], index=flags.index)
        elif isinstance(s, pd.Series):
            return flags.align(s)
        else:
            raise MqTypeError('expected a number or series')

    x_flags, x = ensure_series(x)
    y_flags, y = ensure_series(y)
    return pd.concat([x[x_flags == 1], y[y_flags == 0]]).sort_index()


@plot_function
def weighted_sum(series: List[pd.Series], weights: list) -> pd.Series:
    """
    Calculate a weighted sum.

    :param series: list of time series
    :param weights: list of weights
    :return: time series of weighted average

    **Usage**

    Calculate a weighted sum e.g. for a basket.

    **Examples**

    Generate price series and get a sum (weights 70%/30%).

    >>> prices1 = generate_series(100)
    >>> prices2 = generate_series(100)
    >>> mybasket = weighted_sum([prices1, prices2], [0.7, 0.3])

    **See also**

    :func:`basket`
    """
    if not all(isinstance(x, pd.Series) for x in series):
        raise MqTypeError("expected a list of time series")
    if not all(isinstance(y, (float, int)) for y in weights):
        raise MqTypeError("expected a list of number for weights")
    if len(weights) != len(series):
        raise MqValueError("must have one weight for each time series")

    # for input series, get the intersection of their calendars
    cal = pd.DatetimeIndex(
        reduce(
            np.intersect1d,
            (
                curve.index
                for curve in series
            ),
        )
    )

    # reindex inputs and calculate
    series = [s.reindex(cal) for s in series]
    weights = [pd.Series(w, index=cal) for w in weights]
    return sum(series[i] * weights[i] for i in range(len(series))) / sum(weights)
