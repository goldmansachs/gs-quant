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
from unittest.mock import patch

from gs_quant.target.measures import EqDelta, EqVega

from gs_quant.backtests.actions import AddTradeAction, HedgeAction, ExitTradeAction
from gs_quant.backtests.backtest_objects import (ScaledTransactionModel, AggregateTransactionModel, TransactionAggType,
                                                 ConstantTransactionModel)
from gs_quant.backtests.data_sources import GenericDataSource
from gs_quant.backtests.generic_engine import GenericEngine
from gs_quant.backtests.strategy import Strategy
from gs_quant.backtests.triggers import *
from gs_quant.common import Currency, PayReceive, OptionType, OptionStyle
from gs_quant.instrument import FXOption, FXForward, IRSwaption, IRSwap, EqOption
from gs_quant.markets import PricingContext
from gs_quant.markets.portfolio import Portfolio
from gs_quant.risk import Price, FXDelta, DollarPrice, IRDelta
from gs_quant.test.utils.mock_calc import MockCalc


def mock_pricing_context(self):
    context = PricingContext(set_parameters_only=True, is_batch=False, show_progress=True)
    return context


@patch.object(GenericEngine, 'new_pricing_context', mock_pricing_context)
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
        actions = AddTradeAction(call, freq, name='Action1')

        # starting with empty portfolio (first arg to Strategy), apply actions on trig_req
        triggers = DateTrigger(trig_req, actions)

        strategy = Strategy(None, triggers)

        # run backtest daily
        engine = GenericEngine()
        backtest = engine.run_backtest(strategy, states=[date(2021, 12, 1), date(2021, 12, 2), date(2021, 12, 3)],
                                       show_progress=True)
        summary = backtest.result_summary
        assert len(summary) == 3
        assert round(summary[Price].sum()) == 2424
        assert round(summary['Cumulative Cash'][-1]) == 0


@patch.object(GenericEngine, 'new_pricing_context', mock_pricing_context)
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
        action_hedge = HedgeAction(hedge_risk, fwd_hedge, '2b', name='HedgeAction1')

        triggers = StrategyRiskTrigger(trig_req, action_hedge)

        with PricingContext(pricing_date=start_date, use_historical_diddles_only=True):
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
        assert round(summary['Cumulative Cash'][-1]) == -7090
        assert Price in summary.columns


@patch.object(GenericEngine, 'new_pricing_context', mock_pricing_context)
def test_hedge_without_risk(mocker):
    with MockCalc(mocker):
        # Define trade
        call = FXOption(buy_sell='Buy', option_type='Call', pair='USDJPY', strike_price='ATMF',
                        notional_amount=1e5, expiration_date='2y', name='2y_call')

        trig_req = PeriodicTriggerRequirements(start_date=date(2021, 12, 1), end_date=date(2021, 12, 3),
                                               frequency='1b')

        action = AddTradeAction(call, '1b', name='AddAction1')

        hedge_risk = FXDelta(aggregation_level='Type')
        fwd_hedge = FXForward(pair='USDJPY', settlement_date='2y', notional_amount=1e5, name='2y_forward')

        hedge_trig_req = PeriodicTriggerRequirements(start_date=date(2021, 11, 1), end_date=date(2022, 1, 1),
                                                     frequency='1b')
        action_hedge = HedgeAction(hedge_risk, fwd_hedge, '2b', name='HedgeAction1')

        triggers = [PeriodicTrigger(trig_req, action), PeriodicTrigger(hedge_trig_req, action_hedge)]

        strategy = Strategy(None, triggers)

        # run backtest daily
        engine = GenericEngine()
        # backtest = engine.run_backtest(strategy, start=start_date, end=end_date, frequency='1b', show_progress=True)
        backtest = engine.run_backtest(strategy, states=[date(2021, 12, 1), date(2021, 12, 2), date(2021, 12, 3)],
                                       show_progress=True)
        summary = backtest.result_summary
        assert len(summary) == 3
        assert round(summary[hedge_risk].sum()) == 0
        assert round(summary['Cumulative Cash'][-1]) == -6579
        assert Price in summary.columns


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


@patch.object(GenericEngine, 'new_pricing_context', mock_pricing_context)
def test_mkt_trigger_data_sources(mocker):
    with MockCalc(mocker):
        action = AddTradeAction(IRSwaption(notional_currency='USD', expiration_date='1y', termination_date='1y'),
                                'expiration_date', name='Action1')
        data_source = GenericDataSource(s, MissingDataStrategy.fill_forward)
        mkt_trigger = MktTrigger(MktTriggerRequirements(data_source, 1.1, TriggerDirection.ABOVE), action)
        strategy = Strategy(None, mkt_trigger)

        engine = GenericEngine()

        # backtest = engine.run_backtest(strategy, start=date(2021, 10, 1), end=date(2021, 10, 25), frequency='1b',
        #                                show_progress=True)
        backtest = engine.run_backtest(strategy, states=list(s.index), show_progress=True)

        summary = backtest.result_summary
        ledger = backtest.trade_ledger()
        assert len(summary) == 12
        assert len(ledger) == 6
        assert round(summary[Price].sum()) == 25163614
        assert round(summary['Cumulative Cash'][-1]) == -2153015


@patch.object(GenericEngine, 'new_pricing_context', mock_pricing_context)
def test_exit_action_noarg(mocker):
    with MockCalc(mocker):
        start_date = date(2021, 12, 6)
        end_date = date(2021, 12, 10)

        # Define trade
        irswap = IRSwap(PayReceive.Receive, '10y', Currency.USD, notional_amount=1e5, name='swap')

        trig_req_add = PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1b')
        trig_req_exit = PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='2b')
        actions_add = AddTradeAction(irswap, name='Action1')
        actions_exit = ExitTradeAction(name='ExitAction1')

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


@patch.object(GenericEngine, 'new_pricing_context', mock_pricing_context)
def test_exit_action_emptyresults(mocker):
    with MockCalc(mocker):
        start_date = date(2021, 12, 6)
        end_date = date(2021, 12, 10)

        # Define trade
        irswap = IRSwap(PayReceive.Receive, '10y', Currency.USD, notional_amount=1e5, name='swap')

        trig_req_add = PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='2b')
        trig_req_exit = PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1b')
        actions_add = AddTradeAction(irswap, name='Action1')
        actions_exit = ExitTradeAction(name='ExitAction1')

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


@patch.object(GenericEngine, 'new_pricing_context', mock_pricing_context)
def test_exit_action_bytradename(mocker):
    with MockCalc(mocker):
        start_date = date(2021, 12, 6)
        end_date = date(2021, 12, 10)

        # Define trade
        irswap1 = IRSwap(PayReceive.Receive, '10y', Currency.USD, notional_amount=1e5, name='swap1')
        irswap2 = IRSwap(PayReceive.Pay, '5y', Currency.USD, notional_amount=1e5, name='swap2')

        trig_req_add = PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1b')
        trig_req_exit = PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='2b')
        actions_add = AddTradeAction([irswap1, irswap2], name='Action1')
        actions_exit = ExitTradeAction('swap1', name='ExitAction1')

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


@patch.object(GenericEngine, 'new_pricing_context', mock_pricing_context)
def test_add_scaled_action(mocker):
    with MockCalc(mocker):
        start_date = date(2021, 12, 6)
        end_date = date(2021, 12, 10)

        scale_factor = 7

        # Define instruments for strategy
        # Portfolio of two eq options
        call = EqOption('.STOXX50E', expiration_date='1m', strike_price='ATM', option_type=OptionType.Call,
                        option_style=OptionStyle.European, name='call')
        put = EqOption('.STOXX50E', expiration_date='1m', strike_price='ATM', option_type=OptionType.Put,
                       option_style=OptionStyle.European, name='put')
        portfolio = Portfolio(name='portfolio', priceables=[call, put])

        # Trade the position monthly without any scaling
        trade_action = AddScaledTradeAction(priceables=portfolio, trade_duration='1m',
                                            name='QuantityScaledAction1')
        trade_trigger = PeriodicTrigger(
            trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1b'),
            actions=trade_action)

        strategy = Strategy(None, trade_trigger)

        GE = GenericEngine()
        backtest = GE.run_backtest(strategy, start=start_date, end=end_date, frequency='1b', show_progress=True)

        summary = backtest.result_summary
        ledger = backtest.trade_ledger()

        assert len(summary) == 5
        assert len(ledger) == 10
        assert round(summary[Price].sum()) == 2715
        assert round(summary['Cumulative Cash'][-1]) == -922

        # Trade the position monthly and scale the quantity of the trade
        trade_action_scaled = AddScaledTradeAction(priceables=portfolio, trade_duration='1m',
                                                   scaling_level=scale_factor, name='QuantityScaledAction2')
        trade_trigger_scaled = PeriodicTrigger(
            trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1b'),
            actions=trade_action_scaled)

        strategy_scaled = Strategy(None, trade_trigger_scaled)

        backtest_scaled = GE.run_backtest(strategy_scaled, start=start_date, end=end_date, frequency='1b',
                                          show_progress=True)

        summary_scaled = backtest_scaled.result_summary
        ledger_scaled = backtest_scaled.trade_ledger()

        # Price and cash should scale linearly
        assert len(summary_scaled) == len(summary)
        assert len(ledger_scaled) == len(ledger)
        assert round(summary_scaled[Price].sum()) == round(summary[Price].sum() * scale_factor)
        assert round(summary_scaled['Cumulative Cash'][-1]) == round(summary['Cumulative Cash'][-1] * scale_factor)


@patch.object(GenericEngine, 'new_pricing_context', mock_pricing_context)
def test_scaled_transaction_cost(mocker):
    with MockCalc(mocker):
        start_date = date(2024, 5, 6)
        end_date = date(2024, 5, 10)

        # notional based transaction cost.  charge 1/10000th of the notional
        transaction_cost = ScaledTransactionModel('notional_amount', 0.0001)

        swap = IRSwap(notional_currency=Currency.GBP, notional_amount='50k', termination_date='1y', name='GBP1y')
        trade_action = AddTradeAction(priceables=swap, trade_duration='1m', name='Action1',
                                      transaction_cost=transaction_cost)
        trade_trigger = PeriodicTrigger(trigger_requirements=PeriodicTriggerRequirements(start_date=start_date,
                                                                                         end_date=end_date,
                                                                                         frequency='1b'),
                                        actions=trade_action)

        strategy = Strategy(None, trade_trigger)

        GE = GenericEngine()
        backtest = GE.run_backtest(strategy, start=start_date, end=end_date, frequency='1b', show_progress=True)

        summary = backtest.result_summary
        ledger = backtest.trade_ledger()

        assert len(summary) == 5
        assert len(ledger) == 5
        assert round(summary[Price].sum()) == 90
        assert round(summary['Transaction Costs'][-1]) == 50000 * 0.0001 * 5 * -1


@patch.object(GenericEngine, 'new_pricing_context', mock_pricing_context)
def test_agg_transaction_cost(mocker):
    with MockCalc(mocker):
        start_date = date(2024, 5, 6)
        end_date = date(2024, 5, 10)

        # aggregation based transaction cost.  charge 1/10000th of the notional + 1 for evey transaction
        models = tuple([ScaledTransactionModel('notional_amount', 0.0001), ConstantTransactionModel(1)])
        transaction_cost = AggregateTransactionModel(models, TransactionAggType.SUM)

        swap = IRSwap(notional_currency=Currency.GBP, notional_amount='50k', termination_date='1y', name='GBP1y')
        trade_action = AddTradeAction(priceables=swap, trade_duration='1m', name='Action1',
                                      transaction_cost=transaction_cost)
        trade_trigger = PeriodicTrigger(trigger_requirements=PeriodicTriggerRequirements(start_date=start_date,
                                                                                         end_date=end_date,
                                                                                         frequency='1b'),
                                        actions=trade_action)

        strategy = Strategy(None, trade_trigger)

        GE = GenericEngine()
        backtest = GE.run_backtest(strategy, start=start_date, end=end_date, frequency='1b', show_progress=True)

        summary = backtest.result_summary
        ledger = backtest.trade_ledger()

        assert len(summary) == 5
        assert len(ledger) == 5
        assert round(summary[Price].sum()) == 90
        assert round(summary['Transaction Costs'][-1]) == (50000 * 0.0001 * 5 * -1) - 5


@patch.object(GenericEngine, 'new_pricing_context', mock_pricing_context)
def test_risk_scaled_transaction_cost(mocker):
    with MockCalc(mocker):
        start_date = dt.date(2023, 6, 5)
        end_date = dt.date(2023, 6, 9)

        # risk based transaction cost.  Charge a 2 times the delta.
        transaction_cost = ScaledTransactionModel(IRDelta(aggregation_level='Type'), 2)

        swap = IRSwap(notional_currency=Currency.GBP, notional_amount='50k', termination_date='1y', name='GBP1y')
        trade_action = AddTradeAction(priceables=swap, trade_duration='1m', name='Action1',
                                      transaction_cost=transaction_cost)
        trade_trigger = PeriodicTrigger(trigger_requirements=PeriodicTriggerRequirements(start_date=start_date,
                                                                                         end_date=end_date,
                                                                                         frequency='1b'),
                                        actions=trade_action)

        strategy = Strategy(None, trade_trigger)

        GE = GenericEngine()
        backtest = GE.run_backtest(strategy, start=start_date, end=end_date, frequency='1b', show_progress=True)

        summary = backtest.result_summary
        ledger = backtest.trade_ledger()

        assert len(summary) == 5
        assert len(ledger) == 5
        assert round(summary[Price].sum()) == -64
        assert round(summary['Transaction Costs'][-1]) == -62


@patch.object(GenericEngine, 'new_pricing_context', mock_pricing_context)
def test_hedge_transaction_costs(mocker):
    with MockCalc(mocker):
        start_date = dt.date(2023, 6, 5)
        end_date = dt.date(2023, 6, 9)

        scaled_transaction_cost = ScaledTransactionModel('number_of_options', 1)
        fixed_transaction_cost = ConstantTransactionModel(0)

        opt = EqOption(underlier='.SPX', option_type=OptionType.Call, number_of_options=1, expiration_date='3m',
                       name='SPX_opt')
        trade_action = AddTradeAction(priceables=opt, trade_duration='1m', name='Action1',
                                      transaction_cost=fixed_transaction_cost)
        trade_trigger = PeriodicTrigger(trigger_requirements=PeriodicTriggerRequirements(start_date=start_date,
                                                                                         end_date=end_date,
                                                                                         frequency='1m'),
                                        actions=trade_action)
        hedge_port = Portfolio([EqOption(underlier='.SPX', option_type=OptionType.Call, number_of_options=1,
                                         expiration_date='3m', name='syn_fwd_call'),
                                EqOption(underlier='.SPX', option_type=OptionType.Put, number_of_options=1,
                                         expiration_date='3m', name='syn_fwd_put')])
        hedge_action = HedgeAction(risk=EqDelta, priceables=hedge_port, trade_duration='1b',
                                   transaction_cost=scaled_transaction_cost, name='HedgeAction1')
        hedge_trigger = PeriodicTrigger(trigger_requirements=PeriodicTriggerRequirements(start_date=start_date,
                                                                                         end_date=end_date,
                                                                                         frequency='1b'),
                                        actions=hedge_action)

        strategy = Strategy(None, [trade_trigger, hedge_trigger])
        GE = GenericEngine()
        backtest = GE.run_backtest(strategy, start=start_date, end=end_date, frequency='1b', show_progress=True)

        summary = backtest.result_summary

        assert len(summary) == 5

        total_expected_transaction_costs = 0
        cur_bought_hedges = 0
        for d, port in backtest.portfolio_dict.items():
            # sale of prior hedges
            total_expected_transaction_costs += cur_bought_hedges
            cur_bought_hedges = sum(i.number_of_options for i in port.priceables if i.name.startswith('Scaled'))
            # buy next hedge
            total_expected_transaction_costs += cur_bought_hedges
            np.testing.assert_almost_equal(-summary['Transaction Costs'][d], total_expected_transaction_costs)


@patch.object(GenericEngine, 'new_pricing_context', mock_pricing_context)
def test_exit_transaction_costs(mocker):
    with MockCalc(mocker):
        start_date = dt.date(2024, 6, 3)
        end_date = dt.date(2024, 6, 7)

        scaled_cost = 2
        scaled_transaction_cost = ScaledTransactionModel('number_of_options', scaled_cost)
        fixed_cost = 5
        fixed_transaction_cost = ConstantTransactionModel(fixed_cost)

        opt = EqOption(underlier='.SPX', option_type=OptionType.Call, number_of_options=1, expiration_date='3m',
                       name='SPX_opt')
        trade_action = AddTradeAction(priceables=opt, trade_duration='1b', transaction_cost=scaled_transaction_cost,
                                      transaction_cost_exit=fixed_transaction_cost, name='Action1')
        trade_trigger = PeriodicTrigger(trigger_requirements=PeriodicTriggerRequirements(start_date=start_date,
                                                                                         end_date=end_date,
                                                                                         frequency='1b'),
                                        actions=trade_action)

        strategy = Strategy(None, trade_trigger)
        GE = GenericEngine()
        backtest = GE.run_backtest(strategy, start=start_date, end=end_date, frequency='1b', show_progress=True)

        summary = backtest.result_summary

        assert len(summary) == 5

        total_expected_transaction_costs = 0
        for d, port in backtest.portfolio_dict.items():
            # sale of prior trades
            total_expected_transaction_costs += 0 if d == start_date else fixed_cost
            cur_bought = sum(i.number_of_options for i in port.priceables)
            # buy next trade
            total_expected_transaction_costs += scaled_cost * cur_bought
            np.testing.assert_almost_equal(-summary['Transaction Costs'][d], total_expected_transaction_costs)


@patch.object(GenericEngine, 'new_pricing_context', mock_pricing_context)
def test_add_scaled_action_nav(mocker):
    with MockCalc(mocker):
        start_date = date(2021, 12, 6)
        end_date = date(2021, 12, 10)

        initial_cash = 100

        # Define instruments for strategy
        call = EqOption('.STOXX50E', expiration_date='1m', strike_price='ATM', option_type=OptionType.Call,
                        option_style=OptionStyle.European, name='call')

        # NAV trading strategy with specified initial cash
        trade_action_scaled = AddScaledTradeAction(priceables=call, trade_duration='1b',
                                                   scaling_level=initial_cash,
                                                   scaling_type=ScalingActionType.NAV,
                                                   name='QuantityScaledAction1')

        trade_trigger_scaled = PeriodicTrigger(
            trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1b'),
            actions=trade_action_scaled)

        strategy = Strategy(None, trade_trigger_scaled)

        GE = GenericEngine()
        backtest = GE.run_backtest(strategy, start=start_date, end=end_date, frequency='1b', show_progress=True)

        summary = backtest.result_summary
        ledger = backtest.trade_ledger().to_dict('index')

        # Start with initial cash and only use sale proceeds to buy new options
        np.testing.assert_almost_equal(ledger['QuantityScaledAction1_call_2021-12-06']['Open Value'], -initial_cash)
        np.testing.assert_almost_equal(ledger['QuantityScaledAction1_call_2021-12-07']['Open Value'],
                                       -ledger['QuantityScaledAction1_call_2021-12-06']['Close Value'])
        np.testing.assert_almost_equal(ledger['QuantityScaledAction1_call_2021-12-08']['Open Value'],
                                       -ledger['QuantityScaledAction1_call_2021-12-07']['Close Value'])
        np.testing.assert_almost_equal(ledger['QuantityScaledAction1_call_2021-12-09']['Open Value'],
                                       -ledger['QuantityScaledAction1_call_2021-12-08']['Close Value'])
        np.testing.assert_almost_equal(ledger['QuantityScaledAction1_call_2021-12-10']['Open Value'],
                                       -ledger['QuantityScaledAction1_call_2021-12-09']['Close Value'])

        # Total cash spent is the initial cash throughout the entire strategy
        np.testing.assert_almost_equal(summary['Cumulative Cash'][0], -initial_cash)
        for c in summary['Cumulative Cash']:
            np.testing.assert_almost_equal(c, summary['Cumulative Cash'][0])


def nav_scaled_action_transaction_cost_test_for_agg_type(mocker, agg_type):
    with MockCalc(mocker):
        start_date = date(2021, 12, 6)
        end_date = date(2021, 12, 10)

        initial_cash = 100

        # Define instruments for strategy
        call = EqOption('.STOXX50E', expiration_date='3m', strike_price='ATM', option_type=OptionType.Call,
                        option_style=OptionStyle.European, name='call')

        scaled_transaction_cost = ScaledTransactionModel(EqVega, 1.2)
        fixed_transaction_cost = ConstantTransactionModel(1)
        agg_tc = AggregateTransactionModel((scaled_transaction_cost, fixed_transaction_cost), agg_type)

        # NAV trading strategy with specified initial cash
        trade_action_scaled = AddScaledTradeAction(priceables=call, trade_duration='1b',
                                                   scaling_level=initial_cash,
                                                   scaling_type=ScalingActionType.NAV,
                                                   transaction_cost=agg_tc,
                                                   name=f'QuantityScaledAction2_{agg_type}')

        trade_trigger_scaled = PeriodicTrigger(
            trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1b'),
            actions=trade_action_scaled)

        strategy = Strategy(None, trade_trigger_scaled)

        GE = GenericEngine()
        backtest = GE.run_backtest(strategy, start=start_date, end=end_date, frequency='1b', show_progress=True)

        summary = backtest.result_summary

        ledger = backtest.trade_ledger().to_dict('index')
        tc = backtest.transaction_costs

        # Prior close value minus today's transaction costs equal today's value of options bought
        np.testing.assert_almost_equal(ledger[f'QuantityScaledAction2_{agg_type}_call_2021-12-06']['Open Value'],
                                       -initial_cash - tc[dt.date(2021, 12, 6)])
        np.testing.assert_almost_equal(ledger[f'QuantityScaledAction2_{agg_type}_call_2021-12-07']['Open Value'],
                                       -ledger[f'QuantityScaledAction2_{agg_type}_call_2021-12-06']['Close Value'] -
                                       tc[dt.date(2021, 12, 7)])
        np.testing.assert_almost_equal(ledger[f'QuantityScaledAction2_{agg_type}_call_2021-12-08']['Open Value'],
                                       -ledger[f'QuantityScaledAction2_{agg_type}_call_2021-12-07']['Close Value'] -
                                       tc[dt.date(2021, 12, 8)])
        np.testing.assert_almost_equal(ledger[f'QuantityScaledAction2_{agg_type}_call_2021-12-09']['Open Value'],
                                       -ledger[f'QuantityScaledAction2_{agg_type}_call_2021-12-08']['Close Value'] -
                                       tc[dt.date(2021, 12, 9)])
        np.testing.assert_almost_equal(ledger[f'QuantityScaledAction2_{agg_type}_call_2021-12-10']['Open Value'],
                                       -ledger[f'QuantityScaledAction2_{agg_type}_call_2021-12-09']['Close Value'] -
                                       tc[dt.date(2021, 12, 10)])

        # Cash spent on trades + Transaction costs are equal to the initial cash throughout the entire strategy
        total_cash_spent = summary['Cumulative Cash'] + summary['Transaction Costs']
        np.testing.assert_almost_equal(total_cash_spent[0], -initial_cash)
        for c in total_cash_spent:
            np.testing.assert_almost_equal(c, total_cash_spent[0])


@patch.object(GenericEngine, 'new_pricing_context', mock_pricing_context)
def test_add_scaled_action_nav_with_transaction_costs(mocker):
    for agg_type in (TransactionAggType.SUM, TransactionAggType.MAX, TransactionAggType.MIN):
        nav_scaled_action_transaction_cost_test_for_agg_type(mocker, agg_type)


@patch.object(GenericEngine, 'new_pricing_context', mock_pricing_context)
def test_generic_engine_custom_price_measure(mocker):
    with MockCalc(mocker):
        trig_date = date(2021, 12, 1)
        call = EqOption('.STOXX50E', expiration_date='1y', strike_price='ATM', option_type=OptionType.Call,
                        option_style=OptionStyle.European, name='call')
        freq = '1m'
        trig_req = DateTriggerRequirements(dates=[trig_date])
        actions = AddTradeAction(call, freq, name='Action1')

        triggers = DateTrigger(trig_req, actions)
        strategy = Strategy(None, triggers)

        engine = GenericEngine(price_measure=DollarPrice)
        backtest = engine.run_backtest(strategy, states=[date(2021, 12, 1), date(2021, 12, 2), date(2021, 12, 3)],
                                       show_progress=True)
        summary = backtest.result_summary
        assert len(summary) == 3
        assert round(summary[DollarPrice].sum()) == 804
        assert round(summary['Cumulative Cash'][-1]) == -291


def test_serialisation(mocker):
    call = FXOption(buy_sell='Buy', option_type='Call', pair='USDJPY', strike_price='ATMF',
                    notional_amount=1e5, expiration_date='2y', name='2y_call')
    hedge = FXForward(pair='USDJPY', settlement_date='2y', name='2y_hedge')
    d1 = dt.date(2023, 4, 11)
    d2 = dt.date(2023, 12, 25)
    d3 = dt.date(2024, 2, 29)
    dt1 = dt.datetime(2024, 4, 11, 9, 17, 34)
    dt2 = dt.datetime(2024, 4, 12, 10, 7, 57)
    sample_data_source = GsDataSource('DATASET_ABC', 'ASSET123', d1, d2)
    generic_data_source = GenericDataSource(s, MissingDataStrategy.fill_forward)
    # Actions to check
    add_trade_action_1 = AddTradeAction(call, '1m', name='Action1')
    add_trade_action_2 = AddTradeAction(call, d1, name='Action2')
    add_trade_action_3 = AddTradeAction(call, d2, name='Action3')
    hedge_action = HedgeAction(FXDelta(aggregation_level='type'), hedge, name='HedgeAction')
    exit_trade_action = ExitTradeAction('2y_call', name='ExitAction1')
    exit_all_trades_action = ExitAllPositionsAction(name='ExitEverything')
    add_scaled_trade = AddScaledTradeAction(priceables=call, trade_duration='1b',
                                            scaling_level=100,
                                            scaling_type=ScalingActionType.NAV,
                                            name='QuantityScaledAction1')

    # Triggers to check (randomly assign actions to triggers to cover all above actions)
    date_trigger = DateTrigger(DateTriggerRequirements(dates=(date(2021, 12, 1),)), add_trade_action_1)
    periodic_trigger = PeriodicTrigger(PeriodicTriggerRequirements(d1, d2, "3m", (d3,)), add_trade_action_2)
    triggers = (
        date_trigger,
        periodic_trigger,
        DateTrigger(DateTriggerRequirements(dates=(date(2021, 12, 1),)), [add_trade_action_3, hedge_action]),
        PeriodicTrigger(PeriodicTriggerRequirements(d1, d2, "3m", (d3,))),
        IntradayPeriodicTrigger(IntradayTriggerRequirements(dt1.time(), dt2.time(), 5.0)),
        MktTrigger(MktTriggerRequirements(generic_data_source, 1.1, TriggerDirection.BELOW), exit_trade_action),
        StrategyRiskTrigger(RiskTriggerRequirements(DollarPrice, -1.4, TriggerDirection.BELOW), exit_all_trades_action),
        AggregateTrigger(AggregateTriggerRequirements((date_trigger, periodic_trigger)), add_scaled_trade),
        NotTrigger(NotTriggerRequirements(date_trigger)),
        PortfolioTrigger(PortfolioTriggerRequirements('len', 2)),
        MeanReversionTrigger(MeanReversionTriggerRequirements(sample_data_source, 1.5, 0, 5)),
    )
    strategy = Strategy(None, triggers)

    # Test to_dict()
    strategy_dict = strategy.to_dict()
    reconstituted_strategy = Strategy.from_dict(strategy_dict)
    assert reconstituted_strategy == strategy

    # Test to_json()
    strategy_json = json.dumps(strategy.to_dict(), cls=JSONEncoder)
    reconstituted_strategy = Strategy.from_json(strategy_json)
    assert reconstituted_strategy == strategy


@patch.object(GenericEngine, 'new_pricing_context', mock_pricing_context)
def test_initial_portfolio(mocker):
    with MockCalc(mocker):
        irswap = IRSwap(PayReceive.Pay, '10y', Currency.USD, notional_amount=10000, name='10y')
        actions = AddTradeAction(irswap, '1b')

        new_ir_swap = IRSwap(PayReceive.Pay, '2y', Currency.USD, notional_amount=10000, name='2y')
        newer_ir_swap = IRSwap(PayReceive.Pay, '5y', Currency.USD, notional_amount=10000, name='5y')

        initial_port = {date(2024, 5, 3): irswap,
                        date(2024, 5, 24): [irswap, new_ir_swap],
                        date(2024, 6, 14): [new_ir_swap, newer_ir_swap]}

        trig_req = PeriodicTriggerRequirements(start_date=date(2024, 5, 3), end_date=date(2024, 7, 5), frequency='1b')
        triggers = PeriodicTrigger(trig_req, actions)

        strategy = Strategy(initial_port, triggers)

        engine = GenericEngine()

        pricing_dates = [date(2024, 5, 3),
                         date(2024, 5, 10),
                         date(2024, 5, 17),
                         date(2024, 5, 24),
                         date(2024, 5, 31),
                         date(2024, 6, 7),
                         date(2024, 6, 14),
                         date(2024, 6, 21),
                         date(2024, 6, 28),
                         date(2024, 7, 5)]

        backtest = BackTest(strategy, pricing_dates, [Price], Price)
        engine._resolve_initial_portfolio(initial_port, backtest, date(2024, 5, 3), pricing_dates, None)

        port_dict = backtest.portfolio_dict
        assert len(port_dict[date(2024, 5, 3)]) == 1
        assert len(port_dict[date(2024, 5, 24)]) == 2
        assert len(port_dict[date(2024, 6, 14)]) == 2
        assert len(port_dict[date(2024, 7, 5)]) == 2
        assert port_dict[date(2024, 5, 24)][0].name == '10y_2024-05-24'
        assert port_dict[date(2024, 5, 24)][1].name == '2y_2024-05-24'
        assert port_dict[date(2024, 6, 14)][0].name == '2y_2024-06-14'
        assert port_dict[date(2024, 6, 14)][1].name == '5y_2024-06-14'
