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
from datetime import date, time

import numpy as np
import pandas as pd
from ..errors import *
from enum import Enum
from typing import Iterable, List, Union

"""
Date and time manipulation for timeseries, including date or time shifting, calendar operations, curve alignment and
interpolation operations. Includes sampling operations based on date or time manipulation
"""


class Interpolate(Enum):

    INTERSECT = "intersect"
    STEP = "step"
    NAN = "nan"
    ZERO = "zero"


def __interpolate_step(x: pd.Series, dates: Iterable[float]=None) -> pd.Series:

    curve = x.align(dates, 'right')[0]
    current = x[0]
    for knot in curve.iteritems():
        if np.isnan(knot[1]):
            curve[knot[0]] = current
        else:
            current = knot[1]
    return curve


def align(x: pd.Series, y: pd.Series, method: Interpolate=Interpolate.INTERSECT) -> List[pd.Series]:
    """
    Align dates of two series

    :param x: first timeseries
    :param y: second timeseries
    :param method: interpolation method (default: intersect)
    :return: timeseries with specified dates

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
    =========   ========================================================================

    **Examples**

    Stepwize interpolation of series based on dates in second series:

    >>> a = generate_series(100)
    >>> b = generate_series(100)
    >>> align(a,b, "step")

    **See also**

    :func:`sub`
    """

    if method == Interpolate.INTERSECT:
        return x.align(y, 'inner')
    if method == Interpolate.NAN:
        return x.align(y, 'outer')
    if method == Interpolate.ZERO:
        return x.align(y, 'outer', fill_value=0)
    if method == Interpolate.STEP:

        all_dates = x.align(y, 'outer')[0]

        new_x = all_dates.copy()
        new_y = all_dates.copy()

        curr_x = x.get(0, np.nan)
        curr_y = y.get(0, np.nan)

        for knot in all_dates.iteritems():
            date = knot[0]

            xd = x.get(date, curr_x)
            yd = y.get(date, curr_y)

            curr_x = curr_x if xd is np.nan else xd
            curr_y = curr_y if yd is np.nan else yd

            new_x[date] = curr_x
            new_y[date] = curr_y

        return [new_x, new_y]
    else:
        raise MqValueError('Unknown intersection type: ' + method)


def interpolate(x: pd.Series, dates: Union[List[date], List[time], pd.Series]=None, method: Interpolate=Interpolate.INTERSECT) -> pd.Series:
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
    >>> interpolate(a,b, "step")

    **See also**

    :func:`sub`
    """
    if dates is None:
        dates = x

    if type(dates) is pd.Series:
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
