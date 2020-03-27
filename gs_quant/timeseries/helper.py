"""
Copyright 2019 Goldman Sachs.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""
import inspect
import logging
from collections import namedtuple
from enum import Enum, IntEnum
from functools import wraps
from typing import Optional, Union, List

import pandas as pd

from gs_quant.api.gs.data import QueryType


def _create_enum(name, members):
    return Enum(name, {n.upper(): n.lower() for n in members}, module=__name__)


def _create_int_enum(name, mappings):
    return IntEnum(name, {k.upper(): v for k, v in mappings.items()})


def _to_offset(tenor: str) -> pd.DateOffset:
    import re
    matcher = re.fullmatch('(\\d+)([dwmy])', tenor)
    if not matcher:
        raise ValueError('invalid tenor ' + tenor)

    ab = matcher.group(2)
    if ab == 'd':
        name = 'days'
    elif ab == 'w':
        name = 'weeks'
    elif ab == 'm':
        name = 'months'
    else:
        assert ab == 'y'
        name = 'years'

    kwarg = {name: int(matcher.group(1))}
    return pd.DateOffset(**kwarg)


Interpolate = _create_enum('Interpolate', ['intersect', 'step', 'nan', 'zero', 'time'])
Returns = _create_enum('Returns', ['simple', 'logarithmic'])
SeriesType = _create_enum('SeriesType', ['prices', 'returns'])

Window = namedtuple('Window', ['w', 'r'])


def _check_window(x: pd.Series, window: Window):
    if len(x) > 0 and isinstance(window.w, int) and isinstance(window.r, int):
        if window.w <= 0:
            raise ValueError('Window value must be greater than zero.')
        if window.r > len(x) or window.r < 0:
            raise ValueError('Ramp value must be less than the length of the series and greater than zero.')


def apply_ramp(x: pd.Series, window: Window) -> pd.Series:
    _check_window(x, window)
    if isinstance(window.w, int) and window.w > len(x):  # does not restrict window size when it is a DataOffset
        return pd.Series([])
    if isinstance(window.r, pd.DateOffset):
        return x.loc[x.index[0] + window.r:]
    else:
        return x[window.r:]


def normalize_window(x: pd.Series, window: Union[Window, int, None], default_window: int = None) -> Window:
    if default_window is None:
        default_window = x.size

    if isinstance(window, int):
        window = Window(w=window, r=window)
    else:
        if window is None:
            window = Window(w=default_window, r=0)
        else:
            if isinstance(window.w, str):
                window = Window(_to_offset(window.w), window.r)
            if isinstance(window.r, str):
                window = Window(window.w, _to_offset(window.r))
            if window.w and window.r is None:
                window_size = window.w
                window = Window(w=window_size, r=window_size)
            elif window.w is None:
                window = Window(w=default_window, r=window.r)

    _check_window(x, window)
    return window


def plot_function(fn):
    # Indicates that fn should be exported to plottool as a pure function.
    fn.plot_function = True
    return fn


def plot_session_function(fn):
    fn.plot_function = True
    fn.requires_session = True
    return fn


def plot_measure(asset_class: Optional[tuple] = None, asset_type: Optional[tuple] = None,
                 dependencies: Optional[List[QueryType]] = []):
    # Indicates that fn should be exported to plottool as a member function / pseudo-measure.
    # Set category to None for no restrictions, else provide a tuple of allowed values.
    def decorator(fn):
        assert asset_class is None or isinstance(asset_class, tuple)
        assert asset_type is None or isinstance(asset_type, tuple)

        fn.plot_measure = True
        fn.asset_class = asset_class
        fn.asset_type = asset_type
        fn.dependencies = dependencies

        return fn

    return decorator


def plot_method(fn):
    # Indicates that fn should be exported to plottool as a method.
    fn.plot_method = True

    # Allows fn to accept and ignore real_time argument even if it is not defined in the signature
    @wraps(fn)
    def ignore_extra_argument(*args, **kwargs):
        if 'real_time' not in inspect.signature(fn).parameters:
            kwargs.pop('real_time', None)
        return fn(*args, **kwargs)

    return ignore_extra_argument


def log_return(logger: logging.Logger, message):
    def outer(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            response = fn(*args, **kwargs)
            logger.debug('%s: %s', message, response)
            return response

        return inner

    return outer
