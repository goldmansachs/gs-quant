"""
Copyright 2026 Russlan Ramdowar.
Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied. See the License for the
specific language governing permissions and limitations
under the License.
"""

from unittest.mock import PropertyMock, patch

import numpy as np
import pandas as pd
import pytest

from gs_quant.backtests.backtest_objects import BackTest


def _stats(summary: pd.DataFrame) -> pd.Series:
    with (
        patch.object(BackTest, 'result_summary', new_callable=PropertyMock, return_value=summary),
        patch.object(BackTest, 'trade_ledger', return_value=pd.DataFrame()),
    ):
        return BackTest.__new__(BackTest).summary_stats()


@pytest.mark.parametrize('initial_value', [0.0, 1000.0])
@pytest.mark.parametrize('opening_cost', [0.0, 1.0, 5.0])
def test_summary_stats_accounts_for_initial_capital_and_opening_cost(initial_value, opening_cost):
    index = pd.bdate_range('2024-01-02', periods=5)
    summary = pd.DataFrame(
        {
            'Total': initial_value + np.array([0.0, -1.0, -2.0, 1.0, 3.0]) - opening_cost,
            'Transaction Costs': -opening_cost,
        },
        index=index,
    )
    original = summary.copy(deep=True)
    stats = _stats(summary)
    daily = pd.Series([-1.0 - opening_cost, -1.0, 3.0, 2.0])

    assert stats['Total PnL'] == pytest.approx(3.0 - opening_cost)
    assert stats['Total Transaction Costs'] == -opening_cost
    assert stats['Average Daily PnL'] == pytest.approx(daily.mean())
    assert stats['Daily PnL Std Dev'] == pytest.approx(daily.std())
    assert stats['Annualised Return'] == pytest.approx(daily.mean() * 252)
    assert stats['Annualised Volatility'] == pytest.approx(daily.std() * np.sqrt(252))
    assert stats['Sharpe Ratio'] == pytest.approx(daily.mean() / daily.std() * np.sqrt(252))
    assert stats['Skewness'] == pytest.approx(daily.skew())
    assert stats['Kurtosis'] == pytest.approx(daily.kurt())
    assert stats['% Positive Days'] == 50.0
    assert stats['Best Day'] == 3.0
    assert stats['Worst Day'] == -1.0 - opening_cost
    assert stats['Max Drawdown'] == -2.0 - opening_cost
    assert stats['Peak PnL'] == max(0.0, 3.0 - opening_cost)
    assert stats['Current Drawdown'] == min(0.0, 3.0 - opening_cost)
    pd.testing.assert_frame_equal(summary, original)


@pytest.mark.parametrize('opening_cost', [0.0, 5.0])
def test_single_row_reports_opening_loss_without_daily_observations(opening_cost):
    summary = pd.DataFrame(
        {'Total': [1000.0 - opening_cost], 'Transaction Costs': [-opening_cost]},
        index=pd.bdate_range('2024-01-02', periods=1),
    )
    stats = _stats(summary)
    assert stats['Total PnL'] == -opening_cost
    assert stats['Max Drawdown'] == -opening_cost
    assert stats['Peak PnL'] == 0.0
    for name in [
        'Average Daily PnL',
        'Daily PnL Std Dev',
        'Best Day',
        'Worst Day',
        '% Positive Days',
        'Sharpe Ratio',
        'Sortino Ratio',
    ]:
        assert pd.isna(stats[name])


def test_summary_without_transaction_cost_column_preserves_cost_free_daily_stats():
    summary = pd.DataFrame({'Total': [0.0, 1.0, -1.0, 2.0, 3.0]}, index=pd.bdate_range('2024-01-02', periods=5))
    stats = _stats(summary)
    daily = summary['Total'].diff().dropna()
    assert stats['Total PnL'] == 3.0
    assert stats['Average Daily PnL'] == daily.mean()
    assert stats['Daily PnL Std Dev'] == daily.std()
    assert stats['% Positive Days'] == 75.0


def test_empty_summary_has_no_statistics():
    assert _stats(pd.DataFrame()).empty
