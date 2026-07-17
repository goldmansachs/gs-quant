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

import numpy as np
import pandas as pd

from gs_quant.backtests.actions import AddTradeAction, AddTradeActionInfo
from gs_quant.backtests.backtest_objects import BackTest
from gs_quant.backtests.data_sources import GenericDataSource, MissingDataStrategy
from gs_quant.backtests.order import OrderCost
from gs_quant.backtests.triggers import MeanReversionTrigger, MeanReversionTriggerRequirements
from gs_quant.instrument import IRSwap


def test_generic_data_source_no_lookahead():
    # fill_forward must return the last PAST observation, not a future one, and must not mutate the dataset
    series = pd.Series({dt.date(2021, 1, 1): 1.0, dt.date(2021, 1, 5): 3.0})
    ds = GenericDataSource(series, MissingDataStrategy.fill_forward)

    assert ds.get_data(dt.date(2021, 1, 3)) == 1.0

    # underlying dataset unchanged (no NaN row appended, no ffill applied in place)
    assert len(ds.data_set) == 2
    assert ds.data_set[dt.date(2021, 1, 1)] == 1.0
    assert ds.data_set[dt.date(2021, 1, 5)] == 3.0

    # exact dates still resolve directly
    assert ds.get_data(dt.date(2021, 1, 5)) == 3.0


def test_generic_data_source_no_lookahead_datetime_index():
    series = pd.Series(
        [1.0, 3.0], index=pd.DatetimeIndex([dt.datetime(2021, 1, 1, 12), dt.datetime(2021, 1, 5, 12)])
    )
    ds = GenericDataSource(series, MissingDataStrategy.fill_forward)

    assert ds.get_data(dt.datetime(2021, 1, 3, 12)) == 1.0
    assert len(ds.data_set) == 2


def test_generic_data_source_interpolate_does_not_mutate():
    series = pd.Series({dt.date(2021, 1, 1): 1.0, dt.date(2021, 1, 5): 3.0})
    ds = GenericDataSource(series, MissingDataStrategy.interpolate)

    assert ds.get_data(dt.date(2021, 1, 3)) == 2.0
    assert len(ds.data_set) == 2


def test_mean_reversion_trigger():
    # price series engineered to walk through long entry, long exit, short entry, short exit
    prices = pd.Series(
        {
            dt.date(2021, 1, 4): 100.0,
            dt.date(2021, 1, 5): 102.0,
            dt.date(2021, 1, 6): 100.5,
            dt.date(2021, 1, 7): 90.0,  # far below rolling mean -> long entry
            dt.date(2021, 1, 8): 101.0,  # back above rolling mean -> long exit
            dt.date(2021, 1, 9): 115.0,  # far above rolling mean -> short entry
            dt.date(2021, 1, 10): 95.0,  # back below rolling mean -> short exit
        }
    )
    requirements = MeanReversionTriggerRequirements(
        data_source=GenericDataSource(prices, MissingDataStrategy.fail),
        z_score_bound=2.0,
        rolling_mean_window=3,
        rolling_std_window=3,
    )
    trigger = MeanReversionTrigger(requirements, [AddTradeAction(IRSwap())])

    # warm-up dates: no position, no trigger
    assert not requirements.has_triggered(dt.date(2021, 1, 6))

    # long entry: price well below rolling mean
    info = requirements.has_triggered(dt.date(2021, 1, 7))
    assert info.triggered
    assert info.info_dict[AddTradeAction].scaling == 1
    assert requirements.current_position == 1

    # long exit: price crosses back above the rolling mean
    info = requirements.has_triggered(dt.date(2021, 1, 8))
    assert info.triggered
    assert info.info_dict[AddTradeAction].scaling == -1
    assert requirements.current_position == 0

    # short entry: price well above rolling mean
    info = requirements.has_triggered(dt.date(2021, 1, 9))
    assert info.triggered
    assert info.info_dict[AddTradeAction].scaling == -1
    assert requirements.current_position == -1

    # short exit: price reverts back DOWN below the rolling mean
    info = requirements.has_triggered(dt.date(2021, 1, 10))
    assert info.triggered
    assert info.info_dict[AddTradeAction].scaling == 1
    assert requirements.current_position == 0

    assert trigger.trigger_requirements is requirements


def test_add_trade_action_info_next_schedule():
    info = AddTradeActionInfo(scaling=1, next_schedule=None)
    assert info.scaling == 1
    assert info.next_schedule is None


def test_order_cost_execution_quantity():
    order = OrderCost('USD', 100.0, 'test', dt.datetime(2021, 1, 4, 12))
    # execution_quantity takes no arguments; get_costs accumulates it per execution date
    assert order.execution_quantity() == 100.0
    costs = {order.execution_end_time().date(): order.execution_quantity()}
    assert costs[dt.date(2021, 1, 4)] == 100.0


class _StubBackTest(BackTest):
    def __init__(self, summary, ledger_rows=2):
        self._summary = summary
        self._ledger_rows = ledger_rows

    @property
    def result_summary(self):
        return self._summary

    def trade_ledger(self):
        return pd.DataFrame({'Instrument': range(self._ledger_rows)})


def test_sortino_downside_std():
    dates = pd.date_range(dt.date(2021, 1, 4), periods=4)
    total = pd.Series([0.0, 1.0, -1.0, 2.0], index=dates)
    summary = pd.DataFrame({BackTest.TOTAL_COLUMN: total})

    stats = _StubBackTest(summary).summary_stats(annualisation_factor=252)

    daily_pnl = total.diff().dropna()  # [1, -2, 3]
    ann_return = daily_pnl.mean() * 252
    # downside deviation: squared below-zero deviations averaged over ALL periods, not just losing days
    downside_std = np.sqrt((np.minimum(daily_pnl, 0) ** 2).mean())
    expected_sortino = ann_return / (downside_std * np.sqrt(252))

    assert stats['Sortino Ratio'] == expected_sortino
    assert stats['Total Trades'] == 2
