from enum import Enum


def _create_enum(name, members):
    return Enum(name, {n.upper(): n.lower() for n in members}, module=__name__)


Interpolate = _create_enum('Interpolate', ['intersect', 'step', 'nan', 'zero'])
Returns = _create_enum('Returns', ['simple', 'logarithmic'])
SeriesType = _create_enum('SeriesType', ['prices', 'returns'])
