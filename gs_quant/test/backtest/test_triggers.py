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

import datetime as dt
from unittest.mock import MagicMock

import pandas as pd

from gs_quant.backtests.actions import AddTradeAction
from gs_quant.backtests.triggers import (
    AggregateTrigger,
    AggregateTriggerRequirements,
    AggType,
    DateTrigger,
    DateTriggerRequirements,
    MeanReversionTriggerRequirements,
    NotTrigger,
    NotTriggerRequirements,
)
from gs_quant.instrument import IRSwap, IRSwaption


def test_date_trigger():
    # Test DateTrigger
    action = AddTradeAction(IRSwap())
    trigger = DateTrigger(
        DateTriggerRequirements([dt.date(2021, 11, 9), dt.date(2021, 11, 10), dt.date(2021, 11, 11)]), [action]
    )

    assert not trigger.has_triggered(dt.datetime(2021, 11, 10, 14, 0))
    assert trigger.has_triggered(dt.date(2021, 11, 10))

    trigger = DateTrigger(
        DateTriggerRequirements(
            [dt.datetime(2021, 11, 9, 14, 0), dt.datetime(2021, 11, 10, 14, 0), dt.datetime(2021, 11, 11, 14, 0)]
        ),
        [action],
    )

    assert trigger.has_triggered(dt.datetime(2021, 11, 10, 14, 0))
    assert not trigger.has_triggered(dt.date(2021, 11, 10))

    trigger = DateTrigger(
        DateTriggerRequirements(
            [dt.datetime(2021, 11, 9, 14, 0), dt.datetime(2021, 11, 10, 14, 0), dt.datetime(2021, 11, 11, 14, 0)],
            entire_day=True,
        ),
        [action],
    )

    assert trigger.has_triggered(dt.datetime(2021, 11, 10, 14, 0))
    assert trigger.has_triggered(dt.date(2021, 11, 10))


def test_aggregate_triggger():
    # Test Aggregate Trigger
    action_1 = AddTradeAction(IRSwap())
    action_2 = AddTradeAction(IRSwaption())
    trigger_1 = DateTrigger(
        DateTriggerRequirements([dt.date(2021, 11, 9), dt.date(2021, 11, 10), dt.date(2021, 11, 11)]), [action_1]
    )

    trigger_2 = DateTrigger(
        DateTriggerRequirements([dt.date(2021, 11, 8), dt.date(2021, 11, 10), dt.date(2021, 11, 12)]), [action_2]
    )

    agg_trigger = AggregateTrigger(AggregateTriggerRequirements([trigger_1, trigger_2], aggregate_type=AggType.ALL_OF))

    assert not agg_trigger.has_triggered(dt.date(2021, 11, 9))
    assert agg_trigger.has_triggered(dt.date(2021, 11, 10))
    assert len(agg_trigger.actions) == 0

    agg_trigger = AggregateTrigger(
        AggregateTriggerRequirements([trigger_1, trigger_2], aggregate_type=AggType.ANY_OF), [action_1, action_2]
    )

    assert agg_trigger.has_triggered(dt.date(2021, 11, 8))
    assert isinstance(agg_trigger.actions[1].priceables[0], IRSwaption)
    assert agg_trigger.has_triggered(dt.date(2021, 11, 10))
    assert len(agg_trigger.actions) == 2


def test_not_triggger():
    # Test Not Trigger
    action = AddTradeAction(IRSwap())
    not_action = AddTradeAction(IRSwaption())
    trigger = DateTrigger(
        DateTriggerRequirements([dt.date(2021, 11, 9), dt.date(2021, 11, 10), dt.date(2021, 11, 11)]), [action]
    )

    not_trigger = NotTrigger(NotTriggerRequirements(trigger), [not_action])

    assert not_trigger.has_triggered(dt.date(2021, 11, 8))
    assert isinstance(not_trigger.actions[0].priceables[0], IRSwaption)
    assert not not_trigger.has_triggered(dt.date(2021, 11, 10))


def _make_mean_reversion_trigger(prices: dict[dt.date, float], z_score_bound=1.0, window=5):
    """Helper: build a MeanReversionTriggerRequirements backed by a mock DataSource."""
    data_source = MagicMock()

    def get_data(state, **kwargs):
        return prices[state]

    def get_data_range(state, n, **kwargs):
        dates = sorted(d for d in prices if d <= state)
        values = [prices[d] for d in dates[-n:]]
        return pd.Series(values)

    data_source.get_data.side_effect = get_data
    data_source.get_data_range.side_effect = get_data_range

    return MeanReversionTriggerRequirements(
        data_source=data_source,
        z_score_bound=z_score_bound,
        rolling_mean_window=window,
        rolling_std_window=window,
    )


def test_mean_reversion_trigger_no_signal():
    """Price stays close to its mean — trigger never fires."""
    # Prices all equal: std=0 would blow up, so use a small wobble well inside z_score_bound=2
    prices = {dt.date(2021, 1, i): 100.0 + 0.01 * (i % 3) for i in range(1, 11)}
    req = _make_mean_reversion_trigger(prices, z_score_bound=2.0)

    for date in sorted(prices):
        result = req.has_triggered(date)
        assert not result, f"Unexpected trigger on {date}"
    assert req.current_position == 0


def test_mean_reversion_trigger_go_short_then_exit():
    """Price spikes well above mean → go short; reverts below mean → exit short (Bug 2 fix)."""
    # Establish a baseline mean of ~100 over 5 days, then spike up
    prices = {
        dt.date(2021, 1, 1): 100.0,
        dt.date(2021, 1, 2): 100.0,
        dt.date(2021, 1, 3): 100.0,
        dt.date(2021, 1, 4): 100.0,
        dt.date(2021, 1, 5): 100.0,
        dt.date(2021, 1, 6): 130.0,  # spike — z-score >> 1, should go short (scaling=-1)
        dt.date(2021, 1, 7): 99.0,  # reverts below mean — should exit short (scaling=+1)
    }
    req = _make_mean_reversion_trigger(prices, z_score_bound=1.0)

    # Flat days — no trigger
    for date in [dt.date(2021, 1, d) for d in range(1, 6)]:
        assert not req.has_triggered(date)
    assert req.current_position == 0

    # Spike — enter short
    result = req.has_triggered(dt.date(2021, 1, 6))
    assert result.info_dict[AddTradeAction].scaling == -1
    assert req.current_position == -1

    # Revert below mean — exit short (scaling=+1 to close)
    result = req.has_triggered(dt.date(2021, 1, 7))
    assert result.info_dict[AddTradeAction].scaling == 1
    assert req.current_position == 0


def test_mean_reversion_trigger_go_long_then_exit():
    """Price drops well below mean → go long; reverts above mean → exit long (Bug 1 fix)."""
    prices = {
        dt.date(2021, 1, 1): 100.0,
        dt.date(2021, 1, 2): 100.0,
        dt.date(2021, 1, 3): 100.0,
        dt.date(2021, 1, 4): 100.0,
        dt.date(2021, 1, 5): 100.0,
        dt.date(2021, 1, 6): 70.0,  # drop — z-score << -1, should go long (scaling=+1)
        dt.date(2021, 1, 7): 101.0,  # reverts above mean — should exit long (scaling=-1)
    }
    req = _make_mean_reversion_trigger(prices, z_score_bound=1.0)

    for date in [dt.date(2021, 1, d) for d in range(1, 6)]:
        assert not req.has_triggered(date)
    assert req.current_position == 0

    # Drop — enter long
    result = req.has_triggered(dt.date(2021, 1, 6))
    assert result.info_dict[AddTradeAction].scaling == 1
    assert req.current_position == 1

    # Revert above mean — exit long (scaling=-1 to close)
    result = req.has_triggered(dt.date(2021, 1, 7))
    assert result.info_dict[AddTradeAction].scaling == -1
    assert req.current_position == 0
