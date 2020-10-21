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
from datetime import date, time, timedelta
from numbers import Real
import numpy as np
from .helper import *
from ..errors import MqValueError
from ..datetime.date import DayCountConvention, PaymentFrequency, day_count_fraction
from ..datetime.date import date_range as _date_range

"""
Date and time manipulation for timeseries, including date or time shifting, calendar operations, curve alignment and
interpolation operations. Includes sampling operations based on daif dates[0]te or time manipulation
"""


def __interpolate_step(x: pd.Series, dates: pd.Series = None) -> pd.Series:
    if x.empty:
        raise MqValueError('Cannot perform step interpolation on an empty series')

    first_date = pd.Timestamp(dates.index[0]) if isinstance(x.index[0], pd.Timestamp) else dates.index[0]

    # locate previous valid date or take first value from series
    prev = x.index[0] if first_date < x.index[0] else x.index[x.index.get_loc(first_date, 'pad')]

    current = x[prev]

    curve = x.align(dates, 'right', )[0]                  # only need values from dates

    for knot in curve.iteritems():
        if np.isnan(knot[1]):
            curve[knot[0]] = current
        else:
            current = knot[1]
    return curve


@plot_function
def align(x: Union[pd.Series, Real], y: Union[pd.Series, Real], method: Interpolate = Interpolate.INTERSECT) -> \
        Union[List[pd.Series], List[Real]]:
    """
    Align dates of two series or scalars

    :param x: first timeseries or scalar
    :param y: second timeseries or scalar
    :param method: interpolation method (default: intersect). Only used when both x and y are timeseries
    :return: timeseries with specified dates or two scalars from the input

    **Usage**

    Align the dates of two series using the specified interpolation method. Returns two series with dates based on the
    method of interpolation, for example, can be used to intersect the dates of two series, union dates with a defined
    manner to compute missing values.

    Interpolation methods:

    =========   ========================================================================
    Type        Behavior
    =========   ========================================================================
    intersect   Resultant series only have values on the intersection of dates /times.
    nan         Resultant series have values on the union of dates /times. Values will
                be NaN for dates or times only present in the other series
    zero        Resultant series have values on the union of  dates / times. Values will
                be zero for dates or times only present in the other series
    step        Resultant series have values on the union of  dates / times. Each series
                will use the value of the previous valid point if requested date does
                not exist. Values prior to the first date will be equivalent to the
                first available value
    time        Resultant series have values on the union of dates / times. Missing
                values surrounded by valid values will be interpolated given length of
                interval. Input series must use DateTimeIndex.
    =========   ========================================================================

    **Examples**

    Stepwize interpolation of series based on dates in second series:

    >>> a = generate_series(100)
    >>> b = generate_series(100)
    >>> align(a, b)

    **See also**

    :func:`sub`
    """
    if isinstance(x, Real) and isinstance(y, Real):
        return [x, y]
    if isinstance(x, Real):
        return [pd.Series(x, index=y.index), y]
    if isinstance(y, Real):
        return [x, pd.Series(y, index=x.index)]

    if method == Interpolate.INTERSECT:
        return x.align(y, 'inner')
    if method == Interpolate.NAN:
        return x.align(y, 'outer')
    if method == Interpolate.ZERO:
        return x.align(y, 'outer', fill_value=0)
    if method == Interpolate.TIME:
        new_x, new_y = x.align(y, 'outer')
        new_x.interpolate('time', limit_area='inside', inplace=True)
        new_y.interpolate('time', limit_area='inside', inplace=True)
        return [new_x, new_y]
    if method == Interpolate.STEP:
        new_x, new_y = x.align(y, 'outer')
        new_x.fillna(method='ffill', inplace=True)
        new_y.fillna(method='ffill', inplace=True)
        new_x.fillna(method='bfill', inplace=True)
        new_y.fillna(method='bfill', inplace=True)
        return [new_x, new_y]
    else:
        raise MqValueError('Unknown intersection type: ' + method)


@plot_function
def interpolate(x: pd.Series, dates: Union[List[date], List[time], pd.Series] = None,
                method: Interpolate = Interpolate.INTERSECT) -> pd.Series:
    """
    Interpolate over specified dates or times

    :param x: timeseries to interpolate
    :param dates: array of dates/times or another series to interpolate
    :param method: interpolation method (default: intersect)
    :return: timeseries with specified dates

    **Usage**

    Interpolate the series X over the dates specified by the dates parameter. This can be an array of dates or another
    series, in which case the index of the series will be used to specify dates

    Interpolation methods:

    =========   ========================================================================
    Type        Behavior
    =========   ========================================================================
    intersect   Resultant series only has values on the intersection of dates /times.
                Will only contain intersection of valid dates / times in the series
    nan         Resultant series only has values on the intersection of dates /times.
                Value will be NaN for dates not present in the series
    zero        Resultant series has values on all requested dates / times. The series
                will have a value of zero where the requested date or time was not
                present in the series
    step        Resultant series has values on all requested dates / times. The series
                will use the value of the previous valid point if requested date does
                not exist. Values prior to the first date will be equivalent to the
                first available value
    =========   ========================================================================

    **Examples**

    Stepwize interpolation of series based on dates in second series:

    >>> a = generate_series(100)
    >>> b = generate_series(100)
    >>> interpolate(a, b, Interpolate.INTERSECT)

    **See also**

    :func:`sub`
    """
    if dates is None:
        dates = x

    if isinstance(dates, pd.Series):
        align_series = dates
    else:
        align_series = pd.Series(np.nan, dates)

    if method == Interpolate.INTERSECT:
        return x.align(align_series, 'inner')[0]
    if method == Interpolate.NAN:
        return x.align(align_series, 'right')[0]
    if method == Interpolate.ZERO:
        align_series = pd.Series(0.0, dates)
        return x.align(align_series, 'right', fill_value=0)[0]
    if method == Interpolate.STEP:
        return __interpolate_step(x, align_series)
    else:
        raise MqValueError('Unknown intersection type: ' + method)


@plot_function
def value(x: pd.Series, date: Union[date, time], method: Interpolate = Interpolate.STEP) -> pd.Series:
    """
    Value at specified date or time

    :param x: timeseries
    :param date: requested date or time
    :param method: interpolation method (default: step)
    :return: value at specified date or time

    **Usage**

    Returns the value of series X at the specified date:

    :math:`Y_t = X_{date}`

    If the requested date or time is not present in the series, the value function will return the value from the
    previous available date or time by default. Caller can specify other interpolation styles via the method param:

    Interpolation methods:

    =========   ========================================================================
    Type        Behavior
    =========   ========================================================================
    intersect   Only returns a value for valid dates
    nan         Value will be NaN for dates not present in the series
    zero        Value will be zero for dates not present in the series
    step        Value of the previous valid point if requested date does not exist.
                Values prior to the first date will be equivalent to the first available
                value
    =========   ========================================================================

    **Examples**

    Value of series on 5Mar18:

    >>> a = generate_series(100)
    >>> value(a, date(2019, 1, 3)

    **See also**

    :func:`interpolate`
    """

    values = interpolate(x, [date], method)
    return values.get(0)


@plot_function
def day(x: pd.Series) -> pd.Series:
    """
    Day of each value in series

    :param x: time series
    :return: day of observations

    **Usage**

    Returns the day as a numeric value for each observation in the series:

    :math:`Y_t = day(t)`

    Day of the time or date is the integer day number within the month, e.g. 1-31

    **Examples**

    Day for observations in series:

    >>> series = generate_series(100)
    >>> days = day(series)

    **See also**

    :func:`month` :func:`year`

    """
    return pd.to_datetime(x.index.to_series()).dt.day


@plot_function
def month(x: pd.Series) -> pd.Series:
    """
    Month of each value in series

    :param x: time series
    :return: month of observations

    **Usage**

    Returns the month as a numeric value for each observation in the series:

    :math:`Y_t = month(t)`

    Month of the time or date is the integer month number, e.g. 1-12

    **Examples**

    Day for observations in series:

    >>> series = generate_series(100)
    >>> days = month(series)

    **See also**

    :func:`day` :func:`year`

    """
    return pd.to_datetime(x.index.to_series()).dt.month


@plot_function
def year(x: pd.Series) -> pd.Series:
    """
    Year of each value in series

    :param x: time series
    :return: year of observations

    **Usage**

    Returns the year as a numeric value for each observation in the series:

    :math:`Y_t = year(t)`

    Year of the time or date is the integer year number, e.g. 2019, 2020

    **Examples**

    Year for observations in series:

    >>> series = generate_series(100)
    >>> days = year(series)

    **See also**

    :func:`day` :func:`month`

    """
    return pd.to_datetime(x.index.to_series()).dt.year


@plot_function
def quarter(x: pd.Series) -> pd.Series:
    """
    Quarter of each value in series

    :param x: time series
    :return: quarter of observations

    **Usage**

    Returns the quarter as a numeric value for each observation in the series:

    :math:`Y_t = quarter(t)`

    Quarter of the time or date is the integer quarter number, e.g. 1, 2, 3, 4

    **Examples**

    Quarter for observations in series:

    >>> series = generate_series(100)
    >>> days = quarter(series)

    **See also**

    :func:`day` :func:`month`

    """
    return pd.to_datetime(x.index.to_series()).dt.quarter


@plot_function
def weekday(x: pd.Series) -> pd.Series:
    """
    Weekday of each value in series

    :param x: time series
    :return: weekday of observations

    **Usage**

    Returns the weekday as a numeric value for each observation in the series:

    :math:`Y_t = weekday(t)`

    Weekday of the time or date is the integer day of the week, e.g. 0-6, where 0 represents Monday

    **Examples**

    Weekday for observations in series:

    >>> series = generate_series(100)
    >>> days = weekday(series)

    **See also**

    :func:`day` :func:`month`

    """
    return pd.to_datetime(x.index.to_series()).dt.weekday


@plot_function
def day_count_fractions(
    dates: Union[List[date], pd.Series],
    convention: DayCountConvention = DayCountConvention.ACTUAL_360,
    frequency: PaymentFrequency = PaymentFrequency.MONTHLY
) -> pd.Series:
    """
    Day count fractions between dates in series

    :param dates: time series or array of dates
    :param convention: day count convention (default: Actual/360 ISDA)
    :param frequency: payment frequency of instrument (optional)
    :return: series of day count fractions

    **Usage**

    Returns the day count fraction between dates in the series

    :math:`Y_t = DCF(t_{-1}, t)`

    Default is Actual/360 per ISDA specification:

    :math:`Y_t = \frac{Days(t_{-1}, t)}{360}`

    For a full list of available conventions, see
    `Day Count Conventions <https://developer.gs.com/docs/gsquant/guides/Dates/1-day-count-conventions>`_.
    For more information on day count conventions, see the
    `day count conventions <https://en.wikipedia.org/wiki/Day_count_convention>`_ page on Wikipedia

    **Examples**

    Weekday for observations in series:

    >>> series = generate_series(100)
    >>> days = day_count_fractions(series)

    **See also**

    :func:`day` :func:`month` :func:`year`

    """
    if isinstance(dates, pd.Series):
        date_list = list(dates.index)
    else:
        date_list = dates

    if len(date_list) < 2:
        return pd.Series([])

    start_dates = date_list[0:-1]
    end_dates = date_list[1:len(date_list)]

    dcfs = map(lambda a, b: day_count_fraction(a, b, convention, frequency), start_dates, end_dates)
    return pd.Series(data=[np.NaN] + list(dcfs), index=date_list[0:len(date_list)])


@plot_function
def date_range(x: pd.Series, start_date: Union[date, int], end_date: Union[date, int],
               weekdays_only: bool = False) -> pd.Series:
    """
    Create a time series from a (sub-)range of dates in an existing time series.

    :param x: time series
    :param start_date: start date for the sliced time series. If integer, number of observations after the first
    :param end_date: end date for the sliced time series. If integer, number of observations before the last
    :param weekdays_only: whether to include only weekdays in the sliced ranges
    :return: sliced time series

    **Usage**

    Returns a restricted ("sliced") time series based on start and end dates:

    :math:`Y_t = R_t |_{start < t < end}`

    **Examples**

    Slice the first and last week of a time series:

    >>> series = generate_series(100)
    >>> sliced_series = date_range(series,7,7)

    **See also**

    :func:`day` :func: `lag`

    """
    if not (x.index.is_all_dates or all(map(lambda a: isinstance(a, date), x.index.values))):
        raise MqValueError('input is not a time series')

    if isinstance(start_date, int):
        start_date = x.index[start_date]
    if isinstance(end_date, int):
        end_date = x.index[- (1 + end_date)]

    try:
        start_date = start_date.date()
        end_date = end_date.date()
    except AttributeError:
        pass

    if weekdays_only:
        week_mask = None
        wd = start_date.weekday()
        if wd > 4:
            start_date += timedelta(days=7 - wd)
    else:
        week_mask = tuple([True] * 7)

    return x.loc[x.index.intersection(list(_date_range(start_date, end_date, week_mask=week_mask)))]


@plot_function
def prepend(x: List[pd.Series]) -> pd.Series:
    """
    Prepend data series

    :param x: an array of timeseries
    :return: concatenated timeseries

    **Usage**

    For input series [:math:`x_1`, :math:`x_2`, ... , :math:`X_n`], takes data from series :math:`X_i` until
    the first date for which :math:`X_{i+1}` has data, useful when a higher quality series has a shorter history
    than a lower quality series.

    **Examples**

    Prepend two series:

    >>> x = generate_series(100)
    >>> y = generate_series(100)
    >>> prepend([x, y])

    **See also**

    :func:`union`

    """
    res = pd.Series(dtype='float64')
    for i in range(len(x)):
        this = x[i]
        if i == len(x) - 1:
            return res.append(this)
        end = x[i + 1].index[0]
        res = res.append(this.loc[this.index < end])
    return res


@plot_function
def union(x: List[pd.Series]) -> pd.Series:
    """
    Fill in missing dates or times of one series with another

    :param x: an array of timeseries
    :return: combined series

    **Usage**

    Starting from :math:`i=1`, takes points from series :math:`x_i`. Where points are missing from :math:`x_i`,
    returns points from :math:`x_{i+1}`.

    **Examples**

    Union of two series:

    >>> x = generate_series(100)
    >>> y = generate_series(100)
    >>> union([x, y])

    **See also**

    :func:`prepend`

    """
    res = pd.Series(dtype='float64')
    for series in x:
        res = res.combine_first(series)
    return res
