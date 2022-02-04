"""
Copyright 2018 Goldman Sachs.
Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""

from datetime import date
import pandas as pd
import pytest
from gs_quant.instrument import FXOption, FXForward, IRSwaption, IRSwap
from gs_quant.backtests.triggers import *
from gs_quant.backtests.actions import AddTradeAction, HedgeAction, ExitTradeAction
from gs_quant.backtests.data_sources import GenericDataSource
from gs_quant.backtests.strategy import Strategy
from gs_quant.backtests.generic_engine import GenericEngine
from gs_quant.test.utils.test_utils import MockCalc
from gs_quant.risk import Price, FXDelta
from gs_quant.markets import PricingContext
from gs_quant.common import Currency, PayReceive


@pytest.mark.skip(reason="requires mocking of data extraction for calendar information")
def test_generic_engine_simple(mocker):
    with MockCalc(mocker):

        start_date = date(2021, 12, 1)
        # end_date = date(2021, 12, 3)

        # Define trade
        call = FXOption(buy_sell='Buy', option_type='Call', pair='USDJPY', strike_price='ATMF',
                        notional_amount=1e5, expiration_date='2y', name='2y_call')

        # Periodic trigger: based on frequency
        freq = '1m'

        # trig_req = PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency=freq)
        trig_req = DateTriggerRequirements(dates=[start_date])
        actions = AddTradeAction(call, freq)

        # starting with empty portfolio (first arg to Strategy), apply actions on trig_req
        triggers = DateTrigger(trig_req, actions)

        strategy = Strategy(None, triggers)

        # run backtest daily
        engine = GenericEngine()
        # backtest = engine.run_backtest(strategy, start=start_date, end=end_date, frequency='1b', show_progress=True)
        backtest = engine.run_backtest(strategy, states=[date(2021, 12, 1), date(2021, 12, 2), date(2021, 12, 3)],
                                       show_progress=True)
        summary = backtest.result_summary
        assert len(summary) == 3
        assert round(summary[Price].sum()) == 2424
        assert round(summary['Cumulative Cash'].sum()) == 0


@pytest.mark.skip(reason="requires mocking of data extraction for calendar information")
def test_hedge_action_risk_trigger(mocker):
    with MockCalc(mocker):
        start_date = date(2021, 12, 1)
        # end_date = date(2021, 12, 3)

        # Define trade
        call = FXOption(buy_sell='Buy', option_type='Call', pair='USDJPY', strike_price='ATMF',
                        notional_amount=1e5, expiration_date='2y', name='2y_call')

        hedge_risk = FXDelta(aggregation_level='Type')
        fwd_hedge = FXForward(pair='USDJPY', settlement_date='2y', notional_amount=1e5, name='2y_forward')

        trig_req = RiskTriggerRequirements(risk=hedge_risk, trigger_level=0, direction=TriggerDirection.ABOVE)
        action_hedge = HedgeAction(hedge_risk, fwd_hedge, '2b')

        triggers = StrategyRiskTrigger(trig_req, action_hedge)

        with PricingContext(pricing_date=start_date):
            fut = call.resolve(in_place=False)

        call = fut.result()

        strategy = Strategy(call, triggers)

        # run backtest daily
        engine = GenericEngine()
        # backtest = engine.run_backtest(strategy, start=start_date, end=end_date, frequency='1b', show_progress=True)
        backtest = engine.run_backtest(strategy, states=[date(2021, 12, 1), date(2021, 12, 2), date(2021, 12, 3)],
                                       show_progress=True)
        summary = backtest.result_summary
        assert len(summary) == 3
        assert round(summary[hedge_risk].sum()) == 0
        assert round(summary['Cumulative Cash'].sum()) == -7090
        assert Price in summary.columns


@pytest.mark.skip(reason="requires mocking of data extraction for calendar information")
def test_mkt_trigger_data_sources(mocker):
    with MockCalc(mocker):
        s = pd.Series({date(2021, 10, 1): 0.984274,
                       date(2021, 10, 4): 1.000706,
                       date(2021, 10, 5): 1.044055,
                       date(2021, 10, 6): 1.095361,
                       date(2021, 10, 7): 1.129336,
                       date(2021, 10, 8): 1.182954,
                       date(2021, 10, 12): 1.200108,
                       date(2021, 10, 13): 1.220607,
                       date(2021, 10, 14): 1.172837,
                       date(2021, 10, 15): 1.163660,
                       date(2021, 10, 18): 1.061084,
                       date(2021, 10, 19): 1.025012,
                       date(2021, 10, 20): 1.018035,
                       date(2021, 10, 21): 1.080751,
                       date(2021, 10, 22): 1.069340,
                       date(2021, 10, 25): 1.033413})

        action = AddTradeAction(IRSwaption(notional_currency='USD', expiration_date='1y', termination_date='1y'),
                                'expiration_date')
        data_source = GenericDataSource(s, MissingDataStrategy.fill_forward)
        mkt_trigger = MktTrigger(MktTriggerRequirements(data_source, 1.1, TriggerDirection.ABOVE), action)
        strategy = Strategy(None, mkt_trigger)

        engine = GenericEngine()

        # backtest = engine.run_backtest(strategy, start=date(2021, 10, 1), end=date(2021, 10, 25), frequency='1b',
        #                                show_progress=True)
        backtest = engine.run_backtest(strategy, states=s.index, show_progress=True)

        summary = backtest.result_summary
        ledger = backtest.trade_ledger()
        assert len(summary) == 12
        assert len(ledger) == 6
        assert round(summary[Price].sum()) == 25163614
        assert round(summary['Cumulative Cash'].sum()) == -2153015


@pytest.mark.skip(reason="requires mocking of data extraction for calendar information")
def test_exit_action_noarg(mocker):
    with MockCalc(mocker):

        start_date = date(2021, 12, 6)
        end_date = date(2021, 12, 10)

        # Define trade
        irswap = IRSwap(PayReceive.Receive, '10y', Currency.USD, notional_amount=1e5, name='swap')

        trig_req_add = PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1b')
        trig_req_exit = PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='2b')
        actions_add = AddTradeAction(irswap)
        actions_exit = ExitTradeAction()

        triggers = [PeriodicTrigger(trig_req_add, actions_add), PeriodicTrigger(trig_req_exit, actions_exit)]
        strategy = Strategy(None, triggers)

        # run backtest daily
        engine = GenericEngine()
        # backtest = engine.run_backtest(strategy, start=start_date, end=end_date, frequency='1b', show_progress=True)
        backtest = engine.run_backtest(strategy, states=[date(2021, 12, 6), date(2021, 12, 7), date(2021, 12, 8),
                                                         date(2021, 12, 9), date(2021, 12, 10)], end=end_date,
                                       show_progress=True)

        trade_ledger = backtest.trade_ledger().to_dict('index')

        assert trade_ledger['Action1_swap_2021-12-06']['Open'] == date(2021, 12, 6)
        assert trade_ledger['Action1_swap_2021-12-06']['Close'] == date(2021, 12, 6)
        assert trade_ledger['Action1_swap_2021-12-07']['Open'] == date(2021, 12, 7)
        assert trade_ledger['Action1_swap_2021-12-07']['Close'] == date(2021, 12, 8)


@pytest.mark.skip(reason="requires mocking of data extraction for calendar information")
def test_exit_action_emptyresults(mocker):
    with MockCalc(mocker):

        start_date = date(2021, 12, 6)
        end_date = date(2021, 12, 10)

        # Define trade
        irswap = IRSwap(PayReceive.Receive, '10y', Currency.USD, notional_amount=1e5, name='swap')

        trig_req_add = PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='2b')
        trig_req_exit = PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1b')
        actions_add = AddTradeAction(irswap)
        actions_exit = ExitTradeAction()

        triggers = [PeriodicTrigger(trig_req_add, actions_add), PeriodicTrigger(trig_req_exit, actions_exit)]
        strategy = Strategy(None, triggers)

        # run backtest daily
        engine = GenericEngine()
        # backtest = engine.run_backtest(strategy, start=start_date, end=end_date, frequency='1b', show_progress=True)
        backtest = engine.run_backtest(strategy, states=[date(2021, 12, 6), date(2021, 12, 7), date(2021, 12, 8),
                                                         date(2021, 12, 9), date(2021, 12, 10)], end=end_date,
                                       show_progress=True)

        trade_ledger = backtest.trade_ledger().to_dict('index')

        assert trade_ledger['Action1_swap_2021-12-06']['Open'] == date(2021, 12, 6)
        assert trade_ledger['Action1_swap_2021-12-06']['Close'] == date(2021, 12, 6)
        assert trade_ledger['Action1_swap_2021-12-08']['Open'] == date(2021, 12, 8)
        assert trade_ledger['Action1_swap_2021-12-08']['Close'] == date(2021, 12, 8)
        assert trade_ledger['Action1_swap_2021-12-10']['Open'] == date(2021, 12, 10)
        assert trade_ledger['Action1_swap_2021-12-10']['Close'] == date(2021, 12, 10)


@pytest.mark.skip(reason="requires mocking of data extraction for calendar information")
def test_exit_action_bytradename(mocker):
    with MockCalc(mocker):

        start_date = date(2021, 12, 6)
        end_date = date(2021, 12, 10)

        # Define trade
        irswap1 = IRSwap(PayReceive.Receive, '10y', Currency.USD, notional_amount=1e5, name='swap1')
        irswap2 = IRSwap(PayReceive.Pay, '5y', Currency.USD, notional_amount=1e5, name='swap2')

        trig_req_add = PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1b')
        trig_req_exit = PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='2b')
        actions_add = AddTradeAction([irswap1, irswap2])
        actions_exit = ExitTradeAction('swap1')

        triggers = [PeriodicTrigger(trig_req_add, actions_add), PeriodicTrigger(trig_req_exit, actions_exit)]
        strategy = Strategy(None, triggers)

        # run backtest daily
        engine = GenericEngine()
        # backtest = engine.run_backtest(strategy, start=start_date, end=end_date, frequency='1b', show_progress=True)
        backtest = engine.run_backtest(strategy, states=[date(2021, 12, 6), date(2021, 12, 7), date(2021, 12, 8),
                                                         date(2021, 12, 9), date(2021, 12, 10)], end=end_date,
                                       show_progress=True)

        trade_ledger = backtest.trade_ledger().to_dict('index')

        assert trade_ledger['Action1_swap1_2021-12-06']['Open'] == date(2021, 12, 6)
        assert trade_ledger['Action1_swap1_2021-12-06']['Close'] == date(2021, 12, 6)
        assert trade_ledger['Action1_swap1_2021-12-07']['Open'] == date(2021, 12, 7)
        assert trade_ledger['Action1_swap1_2021-12-07']['Close'] == date(2021, 12, 8)
        assert trade_ledger['Action1_swap2_2021-12-06']['Status'] == 'open'
        assert trade_ledger['Action1_swap2_2021-12-07']['Status'] == 'open'
        assert trade_ledger['Action1_swap2_2021-12-10']['Status'] == 'open'
