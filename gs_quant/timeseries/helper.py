from enum import Enum, IntEnum


def _create_enum(name, members):
    return Enum(name, {n.upper(): n.lower() for n in members}, module=__name__)


def _create_int_enum(name, mappings):
    return IntEnum(name, {k.upper(): v for k, v in mappings.items()})


Interpolate = _create_enum('Interpolate', ['intersect', 'step', 'nan', 'zero'])
Returns = _create_enum('Returns', ['simple', 'logarithmic'])
SeriesType = _create_enum('SeriesType', ['prices', 'returns'])
