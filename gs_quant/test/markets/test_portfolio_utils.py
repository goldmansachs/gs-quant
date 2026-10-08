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

import pytest

from gs_quant.markets import equal_weight, from_asset_ids, market_cap_weighted
from gs_quant.markets.position_set import PositionSet


def _weights(ps):
    return [p.weight for p in ps.positions]


def test_equal_weight():
    ps = equal_weight(['AAPL UW', 'MSFT UW', 'GOOG UW'])
    assert isinstance(ps, PositionSet)
    assert _weights(ps) == pytest.approx([1 / 3, 1 / 3, 1 / 3])
    assert sum(_weights(ps)) == pytest.approx(1.0)


def test_equal_weight_rejects_empty():
    with pytest.raises(ValueError):
        equal_weight([])


def test_market_cap_weighted():
    caps = {'AAPL UW': 3000.0, 'MSFT UW': 1000.0}
    ps = market_cap_weighted(list(caps.keys()), market_caps=caps)
    # 3:1 -> weights 0.75 / 0.25
    assert _weights(ps) == pytest.approx([0.75, 0.25])


def test_market_cap_weighted_falls_back_to_equal():
    ps = market_cap_weighted(['A', 'B', 'C'])  # no caps provided
    assert _weights(ps) == pytest.approx([1 / 3, 1 / 3, 1 / 3])


def test_market_cap_weighted_zero_total():
    with pytest.raises(ValueError):
        market_cap_weighted(['A', 'B'], {'A': 0.0, 'B': 0.0})


def test_from_asset_ids_equal_by_default():
    ps = from_asset_ids(['A', 'B', 'C'])
    assert _weights(ps) == pytest.approx([1 / 3, 1 / 3, 1 / 3])


def test_from_asset_ids_with_weights():
    ps = from_asset_ids(['A', 'B'], weights=[2, 1])
    assert _weights(ps) == pytest.approx([2 / 3, 1 / 3])


def test_from_asset_ids_length_mismatch():
    with pytest.raises(ValueError):
        from_asset_ids(['A', 'B'], weights=[0.5])