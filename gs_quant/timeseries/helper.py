import logging
from enum import Enum, IntEnum
from functools import wraps
from typing import Optional


def _create_enum(name, members):
    return Enum(name, {n.upper(): n.lower() for n in members}, module=__name__)


def _create_int_enum(name, mappings):
    return IntEnum(name, {k.upper(): v for k, v in mappings.items()})


Interpolate = _create_enum('Interpolate', ['intersect', 'step', 'nan', 'zero'])
Returns = _create_enum('Returns', ['simple', 'logarithmic'])
SeriesType = _create_enum('SeriesType', ['prices', 'returns'])


def plot_function(fn):
    # Indicates that fn should be exported to plottool as a pure function.
    fn.plot_function = True
    return fn


def plot_measure(asset_class: Optional[tuple] = None, asset_type: Optional[tuple] = None):
    # Indicates that fn should be exported to plottool as a member function / pseudo-measure.
    # Set category to None for no restrictions, else provide a tuple of allowed values.
    def decorator(fn):
        assert asset_class is None or isinstance(asset_class, tuple)
        assert asset_type is None or isinstance(asset_type, tuple)

        fn.plot_measure = True
        fn.asset_class = asset_class
        fn.asset_type = asset_type
        return fn

    return decorator


def log_return(logger: logging.Logger, message):
    def outer(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            response = fn(*args, **kwargs)
            logger.debug('%s: %s', message, response)
            return response

        return inner

    return outer
