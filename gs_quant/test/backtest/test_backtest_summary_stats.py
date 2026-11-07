"""
Copyright 2026 John Kingola.
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

import math
from unittest import mock

import numpy as np
import pandas as pd

from gs_quant.backtests.backtest_objects import BackTest


def _summary_stats_for(pnl: np.ndarray) -> pd.Series:
    total = pd.Series(np.concatenate([[0.0], np.cumsum(pnl)]), index=pd.bdate_range("2024-01-01", periods=len(pnl) + 1))
    backtest = BackTest.__new__(BackTest)
    with (
        mock.patch.object(BackTest, "result_summary", new_callable=mock.PropertyMock, return_value=pd.DataFrame({"Total": total})),
        mock.patch.object(BackTest, "trade_ledger", return_value=pd.DataFrame()),
    ):
        return backtest.summary_stats()


def test_sortino_uses_downside_deviation_over_all_periods():
    pnl = np.array([1.0, 2.0, -1.0, 3.0, -2.0, 1.0, 0.5, -1.0, 2.0, 1.5])
    stats = _summary_stats_for(pnl)

    ann_return = pnl.mean() * 252
    downside_deviation = math.sqrt((np.minimum(pnl, 0) ** 2).mean()) * math.sqrt(252)
    assert stats["Sortino Ratio"] == pytest_approx(ann_return / downside_deviation)
    # the Sharpe row is unaffected
    assert stats["Sharpe Ratio"] == pytest_approx(pnl.mean() / pnl.std(ddof=1) * math.sqrt(252))


def test_sortino_depends_on_the_size_of_losses_not_their_count():
    # same losses, different number of flat days: dividing by the losing days only would give both
    # vectors the same downside deviation; over all periods they differ by sqrt(2)
    a = np.array([2.0, -1.0, 2.0, -1.0])
    b = np.array([2.0, -1.0, 0.0, 0.0, 2.0, -1.0, 0.0, 0.0])
    for pnl in (a, b):
        expected = (pnl.mean() * 252) / (math.sqrt((np.minimum(pnl, 0) ** 2).mean()) * math.sqrt(252))
        assert _summary_stats_for(pnl)["Sortino Ratio"] == pytest_approx(expected)
    downside_a = math.sqrt((np.minimum(a, 0) ** 2).mean())
    downside_b = math.sqrt((np.minimum(b, 0) ** 2).mean())
    assert downside_a == pytest_approx(downside_b * math.sqrt(2))


def test_sortino_is_nan_without_losses():
    stats = _summary_stats_for(np.array([1.0, 2.0, 0.5]))
    assert np.isnan(stats["Sortino Ratio"])


def pytest_approx(value):
    import pytest

    return pytest.approx(value, rel=1e-9)
