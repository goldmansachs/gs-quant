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

import gs_quant.backtests.predefined_asset_engine
import datetime as dt
from gs_quant.backtests.strategy import Strategy
from gs_quant.backtests.triggers import Trigger, TriggerInfo
from gs_quant.backtests.actions import Action
from gs_quant.backtests.action_handler import ActionHandler
from gs_quant.backtests.backtest_objects import PredefinedAssetBacktest
from gs_quant.backtests.data_sources import DataManager
import pandas as pd
from gs_quant.data.core import DataFrequency
from gs_quant.backtests.core import ValuationFixingType
from gs_quant.instrument import Security
from gs_quant.backtests.order import OrderMarketOnClose
from unittest import mock
import gs_quant.datetime


class TestTrigger(Trigger):
    def __init__(self, action: Action):
        super().__init__(None, action)

        self._trigger_time = dt.time(22, 59, 59)

    def generate_orders(self, time: dt.datetime, backtest: PredefinedAssetBacktest = None) -> list:
        date = time.date()
        if date == dt.date(2021, 1, 5):
            return [OrderMarketOnClose(instrument=Security(ric='TestRic'),
                                       quantity=1,
                                       generation_time=time,
                                       execution_date=date,
                                       source='Test')
                    ]
        else:
            return []

    def get_trigger_times(self) -> list:
        return [dt.time(10, 0, 0)]

    def has_triggered(self, state: dt.datetime, backtest: PredefinedAssetBacktest = None) -> TriggerInfo:
        if state.time() not in self.get_trigger_times():
            return TriggerInfo(False)
        else:
            orders = self.generate_orders(state, backtest)
            return TriggerInfo(True, {type(a): orders for a in self.actions}) if len(orders) else TriggerInfo(False)


class TestActionImpl(ActionHandler):
    def __init__(self, action: Action):
        super().__init__(action)

    def apply_action(self, state: dt.datetime, backtest: PredefinedAssetBacktest, info=None):
        return info


def f():
    yield dt.date(2021, 1, 5)
    yield dt.date(2021, 1, 6)


def test_backtest_predefined():
    trigger = TestTrigger(Action())
    strategy = Strategy(initial_portfolio=None, triggers=[trigger])

    data_mgr = DataManager()
    underlying = Security(ric='TestRic')
    close_prices = pd.Series()
    close_prices[dt.date(2021, 1, 4)] = 1
    close_prices[dt.date(2021, 1, 5)] = 1.5
    close_prices[dt.date(2021, 1, 6)] = 2
    data_mgr.add_data_source(close_prices, DataFrequency.DAILY, underlying, ValuationFixingType.PRICE)

    # all these mocks are needed as the date functions need a GSSession
    gs_quant.backtests.predefined_asset_engine.is_business_day = mock.Mock(return_value=True)
    gs_quant.backtests.predefined_asset_engine.business_day_offset = mock.Mock(return_value=dt.date(2021, 1, 5))
    gs_quant.backtests.predefined_asset_engine.date_range = mock.Mock(return_value=(d for d in f()))

    engine = gs_quant.backtests.predefined_asset_engine.PredefinedAssetEngine(data_mgr=data_mgr,
                                                                              action_impl_map={Action: TestActionImpl})

    backtest = engine.run_backtest(strategy, start=dt.date(2021, 1, 4), end=dt.date(2021, 1, 6))
    perf = backtest.performance
    holdings = backtest.historical_holdings
    cash_asset = backtest.cash_asset

    # 100 on the initial date
    assert perf[dt.date(2021, 1, 4)] == 100
    # 100 on the next day as we traded MOC
    assert perf[dt.date(2021, 1, 5)] == 100
    assert holdings[dt.date(2021, 1, 5)][cash_asset] == 100 - 1.5
    assert holdings[dt.date(2021, 1, 5)][underlying] == 1
    # 100.5 = 98.5 (cash) + 2 ( test asset)
    assert holdings[dt.date(2021, 1, 6)][cash_asset] == 100 - 1.5
    assert holdings[dt.date(2021, 1, 6)][underlying] == 1
    assert perf[dt.date(2021, 1, 6)] == 100.5
