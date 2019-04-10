from enum import Enum, IntEnum
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
        fn.plot_measure = True
        fn.asset_class = asset_class
        fn.asset_type = asset_type
        return fn

    return decorator
