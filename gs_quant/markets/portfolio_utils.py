"""
Copyright 2026 Goldman Sachs.
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

import datetime as dt
from typing import TYPE_CHECKING, Mapping, Optional, Sequence

if TYPE_CHECKING:
    from gs_quant.markets.position_set import PositionSet

__all__ = ['equal_weight', 'market_cap_weighted', 'from_asset_ids']


def _position_set_module():
    # Imported lazily: position_set pulls in instrument/api modules that create a
    # circular-import cycle if loaded eagerly during gs_quant.markets init.
    from gs_quant.markets.position_set import Position, PositionSet

    return Position, PositionSet


def equal_weight(asset_ids: Sequence[str], date: dt.date = None) -> PositionSet:
    """
    Build an equally-weighted :class:`PositionSet` from asset identifiers.

    :param asset_ids: sequence of asset identifiers (Bloomberg tickers or Marquee ids)
    :param date: position date; defaults to today
    :return: equally-weighted PositionSet
    """
    if not asset_ids:
        raise ValueError('asset_ids must not be empty')

    Position, PositionSet = _position_set_module()
    weight = 1.0 / len(asset_ids)
    positions = [Position(identifier=identifier, weight=round(weight, 10)) for identifier in asset_ids]
    return PositionSet(positions, date=date)


def market_cap_weighted(
    asset_ids: Sequence[str],
    market_caps: Optional[Mapping[str, float]] = None,
    date: dt.date = None,
) -> PositionSet:
    """
    Build a market-capitalization-weighted :class:`PositionSet`.

    :param asset_ids: sequence of asset identifiers
    :param market_caps: mapping of identifier -> market capitalisation. When omitted,
        weights are equally distributed (falling back to equal-weight).
    :param date: position date; defaults to today
    :return: cap-weighted PositionSet
    """
    if not asset_ids:
        raise ValueError('asset_ids must not be empty')

    Position, PositionSet = _position_set_module()
    caps = [market_caps.get(i) if market_caps else None for i in asset_ids]
    if any(c is None for c in caps):
        return equal_weight(asset_ids, date=date)

    total = sum(caps)
    if total <= 0:
        raise ValueError('market capitalisations must sum to a positive value')

    positions = [Position(identifier=i, weight=round(c / total, 10)) for i, c in zip(asset_ids, caps)]
    return PositionSet(positions, date=date)


def from_asset_ids(
    asset_ids: Sequence[str], weights: Optional[Sequence[float]] = None, date: dt.date = None
) -> PositionSet:
    """
    Build a :class:`PositionSet` from asset identifiers with optional weights.

    :param asset_ids: sequence of asset identifiers
    :param weights: optional weights (same length as ``asset_ids``). If omitted, weights are equal.
    :param date: position date; defaults to today
    :return: PositionSet with the supplied weights (normalised to sum to 1).
    """
    if not asset_ids:
        raise ValueError('asset_ids must not be empty')

    if weights is None:
        return equal_weight(asset_ids, date=date)

    Position, PositionSet = _position_set_module()
    if len(weights) != len(asset_ids):
        raise ValueError('weights must be the same length as asset_ids')

    total = sum(weights)
    if total <= 0:
        raise ValueError('weights must sum to a positive value')

    positions = [Position(identifier=i, weight=round(w / total, 10)) for i, w in zip(asset_ids, weights)]
    return PositionSet(positions, date=date)
