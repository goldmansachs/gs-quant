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
import zoneinfo

import gs_quant.backtests.predefined_asset_engine
import datetime as dt
from gs_quant.backtests.actions import AddTradeAction
from gs_quant.backtests.strategy import Strategy
from gs_quant.backtests.triggers import OrdersGeneratorTrigger, DateTriggerRequirements, DateTrigger
from gs_quant.backtests.backtest_objects import PredefinedAssetBacktest
from gs_quant.backtests.predefined_asset_engine import PredefinedAssetEngine
from gs_quant.backtests.data_sources import DataManager
import pandas as pd
import numpy as np
from gs_quant.data.core import DataFrequency
from gs_quant.backtests.core import ValuationFixingType
from gs_quant.instrument import IRBondFuture
from gs_quant.backtests.order import OrderMarketOnClose, OrderTWAP, TimeWindow
from unittest import mock
import gs_quant.datetime


class ExampleTestTrigger(OrdersGeneratorTrigger):
    def __init__(self):
        super().__init__()

    def generate_orders(self, time: dt.datetime, backtest: PredefinedAssetBacktest = None) -> list:
        date = time.date()
        if date == dt.date(2021, 1, 5):
            return [OrderMarketOnClose(instrument=IRBondFuture(currency='EUR', name='TestRic'),
                                       quantity=1,
                                       generation_time=time,
                                       execution_date=date,
                                       source='Test')
                    ]
        else:
            return []

    def get_trigger_times(self) -> list:
        return [dt.time(10, 0, 0)]


class FuturesExample(OrdersGeneratorTrigger):
    def __init__(self):
        super().__init__()

    def get_trigger_times(self):
        """ generate orders at 9:30am every day """
        return [dt.time(9, 30)]

    def generate_orders(self, state: dt.datetime, backtest: PredefinedAssetBacktest = None) -> list:
        date = state.date()

        contract = IRBondFuture(currency='EUR', name='TestRic')
        orders = []
        units_to_trade = 1

        """ enter trade is a TWAP order between 10 and 10:30 """
        exec_start = dt.datetime.combine(date, dt.time(10))
        exec_end = dt.datetime.combine(date, dt.time(10, 30))
        orders.append(OrderTWAP(instrument=contract,
                                quantity=units_to_trade,
                                generation_time=state,
                                window=TimeWindow(start=exec_start, end=exec_end),
                                source=str(self.__class__)))

        """ exit the intraday quantity at TWAP between 14 and 14:30 """
        twap_start = dt.datetime.combine(date, dt.time(14))
        twap_end = dt.datetime.combine(date, dt.time(14, 30))
        orders.append(OrderTWAP(instrument=contract,
                                quantity=units_to_trade * -1,
                                generation_time=state,
                                window=TimeWindow(start=twap_start, end=twap_end),
                                source=str(self.__class__)))
        return orders


def test_backtest_predefined_timezone_aware():
    tz = 'Europe/London'
    start_dt = '2021-01-01T08:00'
    end_dt = '2021-12-31T17:00'

    states = pd.bdate_range(start_dt, end_dt, freq='1H', tz=tz).to_series().between_time('08:00',
                                                                                         '17:00').index.tolist()
    trigger_dates = pd.bdate_range(start_dt, end_dt, freq='1H', tz=tz).to_series().at_time('17:00').index.tolist()
    data = np.random.default_rng().standard_normal(len(states))
    s_rt = pd.Series(index=states, data=data)
    s_eod = s_rt.at_time('17:00')
    s_eod.index = s_eod.index.date

    generic_bond_future = IRBondFuture(currency='EUR', name='EURBond')

    add_trade_action = AddTradeAction(generic_bond_future)
    simple_date_trigger_requirement = DateTriggerRequirements(dates=trigger_dates)
    simple_date_trigger = DateTrigger(trigger_requirements=simple_date_trigger_requirement, actions=[add_trade_action])

    data_manager = DataManager()
    data_manager.add_data_source(pd.Series(index=states, data=data), DataFrequency.REAL_TIME, generic_bond_future,
                                 ValuationFixingType.PRICE)
    data_manager.add_data_source(s_eod, DataFrequency.DAILY, generic_bond_future,
                                 ValuationFixingType.PRICE)

    # instantiate a new strategy
    strategy = Strategy(None, triggers=simple_date_trigger)

    engine = PredefinedAssetEngine(data_mgr=data_manager, tz=zoneinfo.ZoneInfo(tz))
    backtest = engine.run_backtest(strategy=strategy, start=states[0], end=states[-1], states=states)
    assert len(backtest.trade_ledger()) == 364


def test_backtest_predefined():
    # Test simple MOC order
    trigger = ExampleTestTrigger()
    strategy = Strategy(initial_portfolio=None, triggers=[trigger])
    start = dt.date(2021, 1, 4)
    mid = dt.date(2021, 1, 5)
    end = dt.date(2021, 1, 6)

    # these mocks are needed as the date functions need a GSSession
    gs_quant.backtests.predefined_asset_engine.is_business_day = mock.Mock(return_value=True)
    gs_quant.backtests.predefined_asset_engine.business_day_offset = mock.Mock(return_value=mid)

    data_mgr = DataManager()
    underlying = IRBondFuture(currency='EUR', name='TestRic')
    close_prices = pd.Series(dtype=float)
    close_prices[start] = 1
    close_prices[mid] = 1.5
    close_prices[end] = 2
    data_mgr.add_data_source(close_prices, DataFrequency.DAILY, underlying, ValuationFixingType.PRICE)

    engine = PredefinedAssetEngine(data_mgr=data_mgr)

    backtest = engine.run_backtest(strategy, start=start, end=end)
    perf = backtest.performance
    holdings = backtest.historical_holdings
    cash_asset = backtest.cash_asset

    # 100 on the initial date
    assert perf[start] == 100
    # 100 on the next day as we traded MOC
    assert perf[mid] == 100
    assert holdings[mid][cash_asset] == 100 - 1.5
    assert holdings[mid][underlying] == 1
    # 100.5 = 98.5 (cash) + 2 ( test asset)
    assert holdings[end][cash_asset] == 100 - 1.5
    assert holdings[end][underlying] == 1
    assert perf[end] == 100.5

    # Test TWAP orders with no ON positions
    twap_entry_mid = 16
    twap_exit_mid = 25

    twap_entry_end = 30
    twap_exit_end = 40

    data_twap = {dt.datetime.combine(mid, dt.time(10, 30)): twap_entry_mid,
                 dt.datetime.combine(mid, dt.time(14, 30)): twap_exit_mid,
                 dt.datetime.combine(end, dt.time(10, 30)): twap_entry_end,
                 dt.datetime.combine(end, dt.time(14, 30)): twap_exit_end}

    data_mgr.add_data_source(pd.Series(data_twap), DataFrequency.REAL_TIME, underlying, ValuationFixingType.PRICE)
    trigger = FuturesExample()
    strategy = Strategy(initial_portfolio=None, triggers=[trigger])
    engine = PredefinedAssetEngine(data_mgr=data_mgr, tz=zoneinfo.ZoneInfo('Europe/London'))
    backtest = engine.run_backtest(strategy, start=start, end=end)
    perf = backtest.performance
    holdings = backtest.historical_holdings
    weights = backtest.historical_weights
    cash_asset = backtest.cash_asset

    # start: 100
    assert perf[start] == 100
    # mid: 100 + (twap_exit - twap_entry)
    assert perf[mid] == 100 - twap_entry_mid + twap_exit_mid
    assert holdings[mid][cash_asset] == perf[mid]
    assert underlying not in holdings[mid]
    assert weights[mid][cash_asset] == 1
    assert underlying not in weights[mid]
    # 100.5 = 98.5 (cash) + 2 ( test asset)
    assert perf[end] == 100 - twap_entry_mid + twap_exit_mid - twap_entry_end + twap_exit_end
    assert holdings[end][cash_asset] == perf[end]
    assert underlying not in holdings[end]
    assert weights[end][cash_asset] == 1
    assert underlying not in weights[end]
