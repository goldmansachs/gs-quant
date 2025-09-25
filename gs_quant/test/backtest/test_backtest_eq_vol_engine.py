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

from unittest import mock

import datetime as dt
from gs_quant.api.gs.backtests_xasset.apis import GsBacktestXassetApi
from gs_quant.api.gs.backtests_xasset.request import BasicBacktestRequest
from gs_quant.api.gs.backtests_xasset.response import BasicBacktestResponse
from gs_quant.api.gs.backtests_xasset.response_datatypes.backtest_datatypes import DateConfig, Trade, \
    TransactionCostConfig, TradingCosts, FixedCostModel, Configuration, RollDateMode
from gs_quant.backtests.backtest_objects import ConstantTransactionModel
from gs_quant.backtests.strategy import Strategy
from gs_quant.backtests.triggers import PeriodicTrigger, PeriodicTriggerRequirements, DateTriggerRequirements, \
    AggregateTrigger, AggregateTriggerRequirements, PortfolioTriggerRequirements, TriggerDirection
from gs_quant.backtests.actions import EnterPositionQuantityScaledAction, HedgeAction, ExitPositionAction, \
    AddTradeAction, AddScaledTradeAction, ScalingActionType
from gs_quant.backtests.equity_vol_engine import EquityVolEngine
from gs_quant.common import BuySell
from gs_quant.instrument import EqOption
from gs_quant.markets.portfolio import Portfolio
from gs_quant.risk import EqDelta
from gs_quant.session import GsSession, Environment
from gs_quant.target.backtests import OptionStyle, OptionType, BacktestTradingQuantityType, \
    FlowVolBacktestMeasure, EquityMarketModel
import pandas as pd
from gs_quant.common import TradeAs


def set_session():
    from gs_quant.session import OAuth2Session
    OAuth2Session.init = mock.MagicMock(return_value=None)
    GsSession.use(Environment.QA, 'client_id', 'secret')


def api_mock_data() -> BasicBacktestResponse:
    pnl_response = {
        'measures': {
            'PNL': {
                '2019-02-18': {'result': 0, 'type': 'float'},
                '2019-02-19': {'result': -0.18, 'type': 'float'},
                '2019-02-20': {'result': -0.27, 'type': 'float'}
            }
        },
        'portfolio': {
            "2019-02-18": [
                {
                    "expirationDate": "2019-05-20", "optionType": "Call", "strikePrice": 3244.79,
                    "assetClass": "Equity", "underlier": ".STOXX50E", "currency": "EUR", "type": "Option",
                    "settlementType": "Cash", "optionStyle": "European", "buySell": "Buy", "numberOfOptions": 1
                },
                {
                    "assetClass": "Equity", "expirationDate": "2019-05-20", "strikePrice": 3244.79,
                    "underlier": ".STOXX50E", "type": "Synthetic Forward", "currency": "EUR", "buySell": "Sell",
                    "quantity": 0.38264157605861704
                }
            ]
        },
        'transactions': {
            "2019-02-18": [
                {
                    "portfolio": [
                        {
                            "expirationDate": "2019-05-20", "optionType": "Call", "strikePrice": 3244.79,
                            "assetClass": "Equity", "underlier": ".STOXX50E", "currency": "EUR", "type": "Option",
                            "settlementType": "Cash", "optionStyle": "European", "buySell": "Buy", "numberOfOptions": 1
                        }
                    ],
                    "portfolio_price": 51.49543980712991,
                    "cost": 0,
                    "currency": None,
                    "direction": "Entry",
                    "quantity": 1
                },
                {
                    "portfolio": [
                        {
                            "assetClass": "Equity", "expirationDate": "2019-05-20", "strikePrice": 3244.79,
                            "underlier": ".STOXX50E", "type": "Synthetic Forward", "currency": "EUR",
                            "buySell": "Sell", "quantity": 0.38264157605861704
                        }
                    ],
                    "portfolio_price": -67.01178502458444,
                    "cost": 0,
                    "currency": None,
                    "direction": "Entry",
                    "quantity": -0.38264157605861704
                }
            ]
        },
        'additional_results': None
    }

    return BasicBacktestResponse.from_dict_custom(pnl_response, decode_instruments=False)


def mock_api_response(mocker, mock_result: BasicBacktestResponse):
    mocker.return_value = mock_result


@mock.patch.object(GsBacktestXassetApi, 'calculate_basic_backtest')
def test_eq_vol_engine_result(mocker):
    # 1. setup strategy

    start_date = dt.date(2019, 2, 18)
    end_date = dt.date(2019, 2, 20)

    option = EqOption('.STOXX50E', expiration_date='3m', strike_price='ATM', option_type=OptionType.Call,
                      option_style=OptionStyle.European, name='option')

    long_call = EqOption('.STOXX50E', expiration_date='3m', strike_price='ATM', option_type=OptionType.Call,
                         option_style=OptionStyle.European, buy_sell=BuySell.Buy, number_of_options=1)
    short_put = EqOption('.STOXX50E', expiration_date='3m', strike_price='ATM', option_type=OptionType.Put,
                         option_style=OptionStyle.European, buy_sell=BuySell.Sell, number_of_options=1)

    hedge_portfolio = Portfolio(name='SynFwd', priceables=[long_call, short_put])

    action = EnterPositionQuantityScaledAction(priceables=option, trade_duration='1m', name='action')
    trigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1m'),
        actions=action)
    hedgetrigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1b'),
        actions=HedgeAction(EqDelta, priceables=hedge_portfolio, trade_duration='1b', name='hedge_action'))
    strategy = Strategy(initial_portfolio=None, triggers=[trigger, hedgetrigger])

    # 2. setup mock api response

    mock_api_response(mocker, api_mock_data())

    # 3. when run backtest

    set_session()
    backtest_result = EquityVolEngine.run_backtest(strategy, start_date, end_date)

    # 4. assert response

    data = [{'date': d, 'value': v.result} for d, v in api_mock_data().measures[FlowVolBacktestMeasure.PNL].items()]
    df = pd.DataFrame.from_records(data)
    df.date = pd.to_datetime(df.date)
    expected_pnl = df.set_index('date').value

    assert expected_pnl.equals(backtest_result.get_measure_series(FlowVolBacktestMeasure.PNL))


@mock.patch.object(GsBacktestXassetApi, 'calculate_basic_backtest')
def test_engine_mapping_basic(mocker):
    # 1. setup strategy

    start_date = dt.date(2019, 2, 18)
    end_date = dt.date(2019, 2, 20)

    option = EqOption('.STOXX50E', expiration_date='3m', strike_price='ATM', option_type=OptionType.Call,
                      option_style=OptionStyle.European, number_of_options=1, name='option')

    long_call = EqOption('.STOXX50E', expiration_date='3m', strike_price='ATM', option_type=OptionType.Call,
                         option_style=OptionStyle.European, buy_sell=BuySell.Buy, number_of_options=1)
    short_put = EqOption('.STOXX50E', expiration_date='3m', strike_price='ATM', option_type=OptionType.Put,
                         option_style=OptionStyle.European, buy_sell=BuySell.Sell, number_of_options=1)

    hedge_portfolio = Portfolio(name='SynFwd', priceables=[long_call, short_put])

    action = EnterPositionQuantityScaledAction(priceables=option, trade_duration='1m', name='action')
    trigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1m'),
        actions=action)
    hedgetrigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1b'),
        actions=HedgeAction(EqDelta, priceables=hedge_portfolio, trade_duration='1b', name='hedge_action'))
    strategy = Strategy(initial_portfolio=None, triggers=[trigger, hedgetrigger])

    # 2. setup mock api response

    response = BasicBacktestResponse.from_dict_custom({
        'measures': {
            'PNL': {
                '2019-02-18': {'result': 0, 'type': 'float'},
                '2019-02-19': {'result': -0.18, 'type': 'float'},
                '2019-02-20': {'result': -0.27, 'type': 'float'}
            }
        },
        'portfolio': {},
        'transactions': {}
    })

    mock_api_response(mocker, response)

    # 3. when run backtest

    set_session()
    EquityVolEngine.run_backtest(strategy, start_date, end_date)

    # 4. assert API call

    backtest = BasicBacktestRequest(
        dates=DateConfig(start_date=start_date, end_date=end_date),
        trades=(Trade(legs=tuple(action.priceables),
                      buy_frequency='1m',
                      holding_period='1m',
                      buy_dates=None,
                      exit_dates=None,
                      quantity=1,
                      quantity_type=BacktestTradingQuantityType.quantity
                      ),
                ),
        measures=(FlowVolBacktestMeasure.ALL_MEASURES,),
        delta_hedge_frequency='1b',
        transaction_costs=TransactionCostConfig(
            trade_cost_model=TradingCosts(entry=FixedCostModel(0), exit=FixedCostModel(0)),
            hedge_cost_model=TradingCosts(entry=FixedCostModel(0), exit=FixedCostModel(0))
        ),
        configuration=Configuration(
            market_model=EquityMarketModel.SFK,
            cash_accrual=True,
            combine_roll_signal_entries=False
        )
    )

    mocker.assert_called_with(backtest, decode_instruments=False)


@mock.patch.object(GsBacktestXassetApi, 'calculate_basic_backtest')
def test_engine_mapping_trade_quantity(mocker):
    # 1. setup strategy

    start_date = dt.date(2019, 2, 18)
    end_date = dt.date(2019, 2, 20)

    option = EqOption('.STOXX50E', expiration_date='3m', strike_price='ATM', option_type=OptionType.Call,
                      option_style=OptionStyle.European, number_of_options=1, name='option')

    long_call = EqOption('.STOXX50E', expiration_date='3m', strike_price='ATM', option_type=OptionType.Call,
                         option_style=OptionStyle.European, buy_sell=BuySell.Buy, number_of_options=1)
    short_put = EqOption('.STOXX50E', expiration_date='3m', strike_price='ATM', option_type=OptionType.Put,
                         option_style=OptionStyle.European, buy_sell=BuySell.Sell, number_of_options=1)

    hedge_portfolio = Portfolio(name='SynFwd', priceables=[long_call, short_put])

    action = EnterPositionQuantityScaledAction(priceables=option, trade_duration='1m', trade_quantity=12345,
                                               trade_quantity_type=BacktestTradingQuantityType.notional, name='action')
    trigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1m'),
        actions=action)
    hedgetrigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1b'),
        actions=HedgeAction(EqDelta, priceables=hedge_portfolio, trade_duration='1b', name='hedge_action'))
    strategy = Strategy(initial_portfolio=None, triggers=[trigger, hedgetrigger])

    # 2. setup mock api response

    mock_api_response(mocker, api_mock_data())

    # 3. when run backtest

    set_session()
    EquityVolEngine.run_backtest(strategy, start_date, end_date)

    # 4. assert API call

    backtest = BasicBacktestRequest(
        dates=DateConfig(start_date=start_date, end_date=end_date),
        trades=(Trade(legs=tuple(action.priceables),
                      buy_frequency='1m',
                      holding_period='1m',
                      buy_dates=None,
                      exit_dates=None,
                      quantity=12345,
                      quantity_type=BacktestTradingQuantityType.notional
                      ),
                ),
        measures=(FlowVolBacktestMeasure.ALL_MEASURES,),
        delta_hedge_frequency='1b',
        transaction_costs=TransactionCostConfig(
            trade_cost_model=TradingCosts(entry=FixedCostModel(0), exit=FixedCostModel(0)),
            hedge_cost_model=TradingCosts(entry=FixedCostModel(0), exit=FixedCostModel(0))
        ),
        configuration=Configuration(
            market_model=EquityMarketModel.SFK,
            cash_accrual=True,
            combine_roll_signal_entries=False
        )
    )

    mocker.assert_called_with(backtest, decode_instruments=False)


@mock.patch.object(GsBacktestXassetApi, 'calculate_basic_backtest')
def test_engine_mapping_with_signals(mocker):
    # 1. setup strategy

    start_date = dt.date(2019, 2, 18)
    end_date = dt.date(2019, 2, 27)

    option = EqOption('.STOXX50E', expirationDate='3m', strikePrice='ATM', optionType=OptionType.Call,
                      optionStyle=OptionStyle.European, name='option', number_of_options=1)

    entry_action = EnterPositionQuantityScaledAction(priceables=option, trade_duration='1m', trade_quantity=12345,
                                                     trade_quantity_type=BacktestTradingQuantityType.notional,
                                                     name='action')

    entry_signal_series = pd.Series(data={dt.date(2019, 2, 19): 1})
    entry_dates = entry_signal_series[entry_signal_series > 0].keys()

    entry_trigger = AggregateTrigger(AggregateTriggerRequirements(triggers=[
        DateTriggerRequirements(dates=entry_dates), PortfolioTriggerRequirements('len', 0, TriggerDirection.EQUAL)]),
        actions=entry_action)

    exit_signal_series = pd.Series(data={dt.date(2019, 2, 20): 1})
    exit_dates = exit_signal_series[exit_signal_series > 0].keys()

    exit_trigger = AggregateTrigger(AggregateTriggerRequirements(triggers=[
        DateTriggerRequirements(dates=exit_dates), PortfolioTriggerRequirements('len', 0, TriggerDirection.ABOVE)]),
        actions=ExitPositionAction(name='exit_action'))

    strategy = Strategy(initial_portfolio=None, triggers=[entry_trigger, exit_trigger])

    # 2. setup mock api response

    mock_api_response(mocker, api_mock_data())

    # 3. when run backtest

    set_session()
    EquityVolEngine.run_backtest(strategy, start_date, end_date)

    # 4. assert API call

    backtest = BasicBacktestRequest(
        dates=DateConfig(start_date=start_date, end_date=end_date),
        trades=(Trade(legs=tuple(entry_action.priceables),
                      buy_frequency='1m',
                      holding_period='1m',
                      buy_dates=tuple(entry_dates),
                      exit_dates=tuple(exit_dates),
                      quantity=12345,
                      quantity_type=BacktestTradingQuantityType.notional
                      ),
                ),
        measures=(FlowVolBacktestMeasure.ALL_MEASURES,),
        delta_hedge_frequency=None,
        transaction_costs=TransactionCostConfig(
            trade_cost_model=TradingCosts(entry=FixedCostModel(0), exit=FixedCostModel(0))
        ),
        configuration=Configuration(
            market_model=EquityMarketModel.SFK,
            cash_accrual=True,
            combine_roll_signal_entries=False
        )
    )

    mocker.assert_called_with(backtest, decode_instruments=False)


@mock.patch.object(GsBacktestXassetApi, 'calculate_basic_backtest')
def test_engine_mapping_trade_quantity_nav(mocker):
    # 1. setup strategy

    start_date = dt.date(2019, 2, 18)
    end_date = dt.date(2019, 2, 20)

    option = EqOption('.STOXX50E', expiration_date='3m', strike_price='ATM', option_type=OptionType.Call,
                      option_style=OptionStyle.European, number_of_options=1, name='option')

    long_call = EqOption('.STOXX50E', expiration_date='3m', strike_price='ATM', option_type=OptionType.Call,
                         option_style=OptionStyle.European, buy_sell=BuySell.Buy, number_of_options=1)
    short_put = EqOption('.STOXX50E', expiration_date='3m', strike_price='ATM', option_type=OptionType.Put,
                         option_style=OptionStyle.European, buy_sell=BuySell.Sell, number_of_options=1)

    hedge_portfolio = Portfolio(name='SynFwd', priceables=[long_call, short_put])

    action = EnterPositionQuantityScaledAction(priceables=option, trade_duration='1m', trade_quantity=12345,
                                               trade_quantity_type=BacktestTradingQuantityType.NAV,
                                               name='action')
    trigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1m'),
        actions=action)
    hedgetrigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1b'),
        actions=HedgeAction(EqDelta, priceables=hedge_portfolio, trade_duration='1b', name='hedge_action'))
    strategy = Strategy(initial_portfolio=None, triggers=[trigger, hedgetrigger])

    # 2. setup mock api response

    mock_api_response(mocker, api_mock_data())

    # 3. when run backtest

    set_session()
    EquityVolEngine.run_backtest(strategy, start_date, end_date)

    # 4. assert API call

    backtest = BasicBacktestRequest(
        dates=DateConfig(start_date=start_date, end_date=end_date),
        trades=(Trade(legs=tuple(action.priceables),
                      buy_frequency='1m',
                      holding_period='1m',
                      buy_dates=None,
                      exit_dates=None,
                      quantity=12345,
                      quantity_type=BacktestTradingQuantityType.NAV
                      ),
                ),
        measures=(FlowVolBacktestMeasure.ALL_MEASURES,),
        delta_hedge_frequency='1b',
        transaction_costs=TransactionCostConfig(
            trade_cost_model=TradingCosts(entry=FixedCostModel(0), exit=FixedCostModel(0)),
            hedge_cost_model=TradingCosts(entry=FixedCostModel(0), exit=FixedCostModel(0))
        ),
        configuration=Configuration(
            market_model=EquityMarketModel.SFK,
            cash_accrual=True,
            combine_roll_signal_entries=False
        )
    )

    mocker.assert_called_with(backtest, decode_instruments=False)


@mock.patch.object(GsBacktestXassetApi, 'calculate_basic_backtest')
def test_engine_mapping_listed_expiry_date(mocker):
    # 1. setup strategy

    start_date = dt.date(2019, 2, 18)
    end_date = dt.date(2019, 2, 20)

    option = EqOption('.STOXX50E', expiration_date='3m@listed', strike_price='ATM', option_type=OptionType.Call,
                      option_style=OptionStyle.European, number_of_options=1, name='option')

    long_call = EqOption('.STOXX50E', expiration_date='3m@listed', strike_price='ATM', option_type=OptionType.Call,
                         option_style=OptionStyle.European, buy_sell=BuySell.Buy, number_of_options=1)
    short_put = EqOption('.STOXX50E', expiration_date='3m@listed', strike_price='ATM', option_type=OptionType.Put,
                         option_style=OptionStyle.European, buy_sell=BuySell.Sell, number_of_options=1)

    hedge_portfolio = Portfolio(name='SynFwd', priceables=[long_call, short_put])

    action = EnterPositionQuantityScaledAction(priceables=option, trade_duration='1m', name='action')
    trigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1m'),
        actions=action)
    hedgetrigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1b'),
        actions=HedgeAction(EqDelta, priceables=hedge_portfolio, trade_duration='1b', name='hedge_action'))
    strategy = Strategy(initial_portfolio=None, triggers=[trigger, hedgetrigger])

    # 2. setup mock api response

    mock_api_response(mocker, api_mock_data())

    # 3. when run backtest

    set_session()
    EquityVolEngine.run_backtest(strategy, start_date, end_date)

    # 4. assert API call

    action.priceables[0].expiration_date = action.priceables[0].expiration_date.replace('@listed', '')
    action.priceables[0].trade_as = TradeAs.Listed
    backtest = BasicBacktestRequest(
        dates=DateConfig(start_date=start_date, end_date=end_date),
        trades=(Trade(legs=tuple(action.priceables),
                      buy_frequency='1m',
                      holding_period='1m',
                      buy_dates=None,
                      exit_dates=None,
                      quantity=1,
                      quantity_type=BacktestTradingQuantityType.quantity
                      ),
                ),
        measures=(FlowVolBacktestMeasure.ALL_MEASURES,),
        delta_hedge_frequency='1b',
        transaction_costs=TransactionCostConfig(
            trade_cost_model=TradingCosts(entry=FixedCostModel(0), exit=FixedCostModel(0)),
            hedge_cost_model=TradingCosts(entry=FixedCostModel(0), exit=FixedCostModel(0))
        ),
        configuration=Configuration(
            market_model=EquityMarketModel.SFK,
            cash_accrual=True,
            combine_roll_signal_entries=False
        )
    )

    mocker.assert_called_with(backtest, decode_instruments=False)


@mock.patch.object(GsBacktestXassetApi, 'calculate_basic_backtest')
def test_engine_mapping_listed_roll_date(mocker):
    # 1. setup strategy

    start_date = dt.date(2019, 2, 18)
    end_date = dt.date(2019, 2, 20)

    option = EqOption('.STOXX50E', expiration_date='3m', strike_price='ATM', option_type=OptionType.Call,
                      option_style=OptionStyle.European, number_of_options=1, name='option')

    action = EnterPositionQuantityScaledAction(priceables=option, trade_duration='1m@listed', name='action')
    trigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date,
                                                         frequency='1m@listed'),
        actions=action)
    strategy = Strategy(initial_portfolio=None, triggers=[trigger,])

    # 2. setup mock api response

    mock_api_response(mocker, api_mock_data())

    # 3. when run backtest

    set_session()
    EquityVolEngine.run_backtest(strategy, start_date, end_date)

    # 4. assert API call

    backtest = BasicBacktestRequest(
        dates=DateConfig(start_date=start_date, end_date=end_date),
        trades=(Trade(legs=tuple(action.priceables),
                      buy_frequency='1m',
                      holding_period='1m',
                      buy_dates=None,
                      exit_dates=None,
                      quantity=1,
                      quantity_type=BacktestTradingQuantityType.quantity
                      ),
                ),
        measures=(FlowVolBacktestMeasure.ALL_MEASURES,),
        transaction_costs=TransactionCostConfig(
            trade_cost_model=TradingCosts(entry=FixedCostModel(0), exit=FixedCostModel(0))
        ),
        configuration=Configuration(
            market_model=EquityMarketModel.SFK,
            cash_accrual=True,
            combine_roll_signal_entries=False,
            roll_date_mode=RollDateMode.Listed
        )
    )

    mocker.assert_called_with(backtest, decode_instruments=False)


@mock.patch.object(GsBacktestXassetApi, 'calculate_basic_backtest')
def test_engine_mapping_market_model(mocker):
    # 1. setup strategy

    start_date = dt.date(2019, 2, 18)
    end_date = dt.date(2019, 2, 20)

    option = EqOption('.STOXX50E', expiration_date='3m', strike_price='ATM', option_type=OptionType.Call,
                      option_style=OptionStyle.European, number_of_options=1, name='option')

    long_call = EqOption('.STOXX50E', expiration_date='3m', strike_price='ATM', option_type=OptionType.Call,
                         option_style=OptionStyle.European, buy_sell=BuySell.Buy, number_of_options=1)
    short_put = EqOption('.STOXX50E', expiration_date='3m', strike_price='ATM', option_type=OptionType.Put,
                         option_style=OptionStyle.European, buy_sell=BuySell.Sell, number_of_options=1)

    hedge_portfolio = Portfolio(name='SynFwd', priceables=[long_call, short_put])

    action = EnterPositionQuantityScaledAction(priceables=option, trade_duration='1m', name='action')
    trigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1m'),
        actions=action)
    hedgetrigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1b'),
        actions=HedgeAction(EqDelta, priceables=hedge_portfolio, trade_duration='1b', name='hedge_action'))
    strategy = Strategy(initial_portfolio=None, triggers=[trigger, hedgetrigger])

    # 2. setup mock api response

    mock_api_response(mocker, api_mock_data())

    # 3. when run backtest

    set_session()
    EquityVolEngine.run_backtest(strategy, start_date, end_date, market_model=EquityMarketModel.SVR)

    # 4. assert response

    backtest = BasicBacktestRequest(
        dates=DateConfig(start_date=start_date, end_date=end_date),
        trades=(Trade(legs=tuple(action.priceables),
                      buy_frequency='1m',
                      holding_period='1m',
                      buy_dates=None,
                      exit_dates=None,
                      quantity=1,
                      quantity_type=BacktestTradingQuantityType.quantity
                      ),
                ),
        measures=(FlowVolBacktestMeasure.ALL_MEASURES,),
        delta_hedge_frequency='1b',
        transaction_costs=TransactionCostConfig(
            trade_cost_model=TradingCosts(entry=FixedCostModel(0), exit=FixedCostModel(0)),
            hedge_cost_model=TradingCosts(entry=FixedCostModel(0), exit=FixedCostModel(0))
        ),
        configuration=Configuration(
            market_model=EquityMarketModel.SVR,
            cash_accrual=True,
            combine_roll_signal_entries=False
        )
    )

    mocker.assert_called_with(backtest, decode_instruments=False)


@mock.patch.object(GsBacktestXassetApi, 'calculate_basic_backtest')
def test_engine_mapping_portfolio(mocker):
    # 1. setup strategy

    start_date = dt.date(2019, 2, 18)
    end_date = dt.date(2019, 2, 20)

    call = EqOption('.STOXX50E', expiration_date='3m', strike_price='ATM', option_type=OptionType.Call,
                    option_style=OptionStyle.European, number_of_options=1, name='option_call')

    put = EqOption('.STOXX50E', expiration_date='3m', strike_price='ATM', option_type=OptionType.Put,
                   option_style=OptionStyle.European, number_of_options=1, name='option_put')

    portfolio = Portfolio(name='portfolio', priceables=[call, put])

    long_call = EqOption('.STOXX50E', expiration_date='3m', strike_price='ATM', option_type=OptionType.Call,
                         option_style=OptionStyle.European, buy_sell=BuySell.Buy)
    short_put = EqOption('.STOXX50E', expiration_date='3m', strike_price='ATM', option_type=OptionType.Put,
                         option_style=OptionStyle.European, buy_sell=BuySell.Sell)

    hedge_portfolio = Portfolio(name='SynFwd', priceables=[long_call, short_put])

    action = EnterPositionQuantityScaledAction(priceables=portfolio, trade_duration='1m', name='action')
    trigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1m'),
        actions=action)
    hedgetrigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1b'),
        actions=HedgeAction(EqDelta, priceables=hedge_portfolio, trade_duration='1b', name='hedge_action'))
    strategy = Strategy(initial_portfolio=None, triggers=[trigger, hedgetrigger])

    # 2. setup mock api response

    mock_api_response(mocker, api_mock_data())

    # 3. when run backtest

    set_session()
    EquityVolEngine.run_backtest(strategy, start_date, end_date)

    # 4. assert response

    backtest = BasicBacktestRequest(
        dates=DateConfig(start_date=start_date, end_date=end_date),
        trades=(Trade(legs=tuple(action.priceables),
                      buy_frequency='1m',
                      holding_period='1m',
                      buy_dates=None,
                      exit_dates=None,
                      quantity=1,
                      quantity_type=BacktestTradingQuantityType.quantity
                      ),
                ),
        measures=(FlowVolBacktestMeasure.ALL_MEASURES,),
        delta_hedge_frequency='1b',
        transaction_costs=TransactionCostConfig(
            trade_cost_model=TradingCosts(entry=FixedCostModel(0), exit=FixedCostModel(0)),
            hedge_cost_model=TradingCosts(entry=FixedCostModel(0), exit=FixedCostModel(0))
        ),
        configuration=Configuration(
            market_model=EquityMarketModel.SFK,
            cash_accrual=True,
            combine_roll_signal_entries=False
        )
    )

    mocker.assert_called_with(backtest, decode_instruments=False)


def test_supports_strategy():
    # 1. Valid strategy

    start_date = dt.date(2019, 2, 18)
    end_date = dt.date(2019, 2, 20)

    option = EqOption('.STOXX50E', expiration_date='3m', strike_price='ATM', option_type=OptionType.Call,
                      option_style=OptionStyle.European, name='option')

    long_call = EqOption('.STOXX50E', expiration_date='3m', strike_price='ATM', option_type=OptionType.Call,
                         option_style=OptionStyle.European, buy_sell=BuySell.Buy)
    short_put = EqOption('.STOXX50E', expiration_date='3m', strike_price='ATM', option_type=OptionType.Put,
                         option_style=OptionStyle.European, buy_sell=BuySell.Sell)

    hedge_portfolio = Portfolio(name='SynFwd', priceables=[long_call, short_put])

    action = EnterPositionQuantityScaledAction(priceables=option, trade_duration='1m', name='action')
    trigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1m'),
        actions=action)
    hedge_trigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1b'),
        actions=HedgeAction(EqDelta, priceables=hedge_portfolio, trade_duration='1b', name='hedge_action'))
    strategy = Strategy(initial_portfolio=None, triggers=[trigger, hedge_trigger])

    assert EquityVolEngine.supports_strategy(strategy)

    # 2. Invalid - no trade action

    trigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1m'),
        actions=None
    )
    strategy = Strategy(initial_portfolio=None, triggers=[trigger])
    assert not EquityVolEngine.supports_strategy(strategy)

    # 3. Invalid - no trade quantity

    action = EnterPositionQuantityScaledAction(priceables=option, trade_duration='1m', trade_quantity=None,
                                               name='action')
    trigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1m'),
        actions=action)
    strategy = Strategy(initial_portfolio=None, triggers=[trigger])
    assert not EquityVolEngine.supports_strategy(strategy)

    # 4. Invalid - no trade quantity type

    action = EnterPositionQuantityScaledAction(priceables=option, trade_duration='1m', trade_quantity_type=None,
                                               name='action')
    trigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1m'),
        actions=action)
    strategy = Strategy(initial_portfolio=None, triggers=[trigger])
    assert not EquityVolEngine.supports_strategy(strategy)

    # 5. Invalid - mismatch trade duration and trigger period

    action = EnterPositionQuantityScaledAction(priceables=option, trade_duration='2m', name='action')
    trigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1m'),
        actions=action)
    strategy = Strategy(initial_portfolio=None, triggers=[trigger])
    assert not EquityVolEngine.supports_strategy(strategy)

    # 6. Invalid - mismatch hedge trade duration and trigger period

    action = EnterPositionQuantityScaledAction(priceables=option, trade_duration='1m', name='action')
    trigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1m'),
        actions=action)
    hedge_trigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='B'),
        actions=HedgeAction(EqDelta, priceables=option, trade_duration='M', name='hedge_action'))
    strategy = Strategy(initial_portfolio=None, triggers=[trigger, hedge_trigger])
    assert not EquityVolEngine.supports_strategy(strategy)

    # 7. Invalid - non-daily hedge trade

    action = EnterPositionQuantityScaledAction(priceables=option, trade_duration='1m', name='action')
    trigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1m'),
        actions=action)
    hedge_trigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='M'),
        actions=HedgeAction(EqDelta, priceables=option, trade_duration='M', name='hedge_action'))
    strategy = Strategy(initial_portfolio=None, triggers=[trigger, hedge_trigger])
    assert not EquityVolEngine.supports_strategy(strategy)

    # 8. Invalid - expiration date modifiers must be the same

    option_listed = EqOption('.STOXX50E', expirationDate='3m@listed', strikePrice='ATM', optionType=OptionType.Call,
                             optionStyle=OptionStyle.European, name='option')

    action = EnterPositionQuantityScaledAction(priceables=[option, option_listed], trade_duration='1m', name='action')
    trigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1m'),
        actions=action)
    strategy = Strategy(initial_portfolio=None, triggers=[trigger])
    assert not EquityVolEngine.supports_strategy(strategy)

    # 9. Invalid - expiration date modifier not in [otc, listed]

    option_invalid = EqOption('.STOXX50E', expirationDate='3m@invalid', strikePrice='ATM', optionType=OptionType.Call,
                              name='option')
    action = EnterPositionQuantityScaledAction(priceables=[option_invalid], trade_duration='1m', name='action')
    trigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1m'),
        actions=action)
    strategy = Strategy(initial_portfolio=None, triggers=[trigger])
    assert not EquityVolEngine.supports_strategy(strategy)

    # 10. Invalid - hedging without synthetic forward (not a portfolio)
    hedge_portfolio = Portfolio(name='SynFwd', priceables=[long_call])

    hedge_trigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1b'),
        actions=HedgeAction(EqDelta, priceables=hedge_portfolio, trade_duration='1b', name='hedge_action'))
    strategy = Strategy(initial_portfolio=None, triggers=[trigger, hedge_trigger])

    assert not EquityVolEngine.supports_strategy(strategy)

    # 11. Invalid - hedging without synthetic forward (two calls)

    long_call_2 = EqOption('.STOXX50E', expiration_date='3m', strike_price='ATM', option_type=OptionType.Call,
                           option_style=OptionStyle.European, buy_sell=BuySell.Buy, name='option')

    hedge_portfolio = Portfolio(name='SynFwd', priceables=[long_call, long_call_2])

    hedge_trigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1b'),
        actions=HedgeAction(EqDelta, priceables=hedge_portfolio, trade_duration='1b', name='hedge_action'))
    strategy = Strategy(initial_portfolio=None, triggers=[trigger, hedge_trigger])

    assert not EquityVolEngine.supports_strategy(strategy)

    # 12. Invalid - hedging without synthetic forward (more than two options)

    hedge_portfolio = Portfolio(name='SynFwd', priceables=[long_call, short_put, long_call_2])

    hedge_trigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1b'),
        actions=HedgeAction(EqDelta, priceables=hedge_portfolio, trade_duration='1b', name='hedge_action'))
    strategy = Strategy(initial_portfolio=None, triggers=[trigger, hedge_trigger])

    assert not EquityVolEngine.supports_strategy(strategy)

    # 13. Invalid - hedging without synthetic forward (properties mismatch)

    long_call_2m = EqOption('.STOXX50E', expiration_date='2m', strike_price='ATM', option_type=OptionType.Call,
                            option_style=OptionStyle.European, buy_sell=BuySell.Buy, name='option_1')
    short_put_4m = EqOption('.STOXX50E', expiration_date='4m', strike_price='ATM', option_type=OptionType.Put,
                            option_style=OptionStyle.European, buy_sell=BuySell.Sell, name='option_2')

    hedge_portfolio = Portfolio(name='SynFwd', priceables=[long_call_2m, short_put_4m])

    hedge_trigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1b'),
        actions=HedgeAction(EqDelta, priceables=hedge_portfolio, trade_duration='1b', name='hedge_action'))
    strategy = Strategy(initial_portfolio=None, triggers=[trigger, hedge_trigger])

    assert not EquityVolEngine.supports_strategy(strategy)

    # 14. Valid - AddTradeAction

    add_trade_action = AddTradeAction(priceables=option, trade_duration='1m', name='action')
    trigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1m'),
        actions=add_trade_action)
    strategy = Strategy(initial_portfolio=None, triggers=[trigger])
    assert EquityVolEngine.supports_strategy(strategy)

    # 15. Valid - AddScaledTradeAction

    add_scaled_trade_action = AddScaledTradeAction(priceables=option, trade_duration='1m',
                                                   scaling_type=ScalingActionType.size, scaling_level=2, name='action')
    trigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1m'),
        actions=add_scaled_trade_action)
    strategy = Strategy(initial_portfolio=None, triggers=[trigger])
    assert EquityVolEngine.supports_strategy(strategy)

    # 16. Invalid - transaction_costs not supported

    add_trade_action_tc = AddTradeAction(priceables=option, trade_duration='1m',
                                         transaction_cost=ConstantTransactionModel(100), name='action')
    trigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1m'),
        actions=add_trade_action_tc)
    strategy = Strategy(initial_portfolio=None, triggers=[trigger])
    assert EquityVolEngine.supports_strategy(strategy)

    # 17. Valid - transaction_costs supported if 0

    add_trade_action_tc0 = AddTradeAction(priceables=option, trade_duration='1m',
                                          transaction_cost=ConstantTransactionModel(0), name='action')
    trigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1m'),
        actions=add_trade_action_tc0)
    strategy = Strategy(initial_portfolio=None, triggers=[trigger])
    assert EquityVolEngine.supports_strategy(strategy)

    # 18. Invalid - instrument non unit contract size

    option_with_mult = EqOption('.STOXX50E', expiration_date='3m', strike_price='ATM', option_type=OptionType.Call,
                                option_style=OptionStyle.European, multiplier=100, name='option')

    action = AddTradeAction(priceables=option_with_mult, trade_duration='1m', name='action')
    trigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1m'),
        actions=action)
    strategy = Strategy(initial_portfolio=None, triggers=[trigger])
    assert not EquityVolEngine.supports_strategy(strategy)

    # 19. Invalid - instrument non unit contract count

    option_with_contracts = EqOption('.STOXX50E', expiration_date='3m', strike_price='ATM', option_type=OptionType.Call,
                                     option_style=OptionStyle.European, number_of_options=100, name='option')

    action = AddTradeAction(priceables=option_with_contracts, trade_duration='1m', name='action')
    trigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1m'),
        actions=action)
    strategy = Strategy(initial_portfolio=None, triggers=[trigger])
    assert not EquityVolEngine.supports_strategy(strategy)


@mock.patch.object(GsBacktestXassetApi, 'calculate_basic_backtest')
def test_engine_mapping_basic_leg_size(mocker):
    # 1. setup strategy

    start_date = dt.date(2019, 2, 18)
    end_date = dt.date(2019, 2, 20)

    option = EqOption('.STOXX50E', expiration_date='3m', strike_price='ATM', option_type=OptionType.Call,
                      option_style=OptionStyle.European, name='option', number_of_options=0)

    long_call = EqOption('.STOXX50E', expiration_date='3m', strike_price='ATM', option_type=OptionType.Call,
                         option_style=OptionStyle.European, buy_sell=BuySell.Buy)
    short_put = EqOption('.STOXX50E', expiration_date='3m', strike_price='ATM', option_type=OptionType.Put,
                         option_style=OptionStyle.European, buy_sell=BuySell.Sell)

    hedge_portfolio = Portfolio(name='SynFwd', priceables=[long_call, short_put])

    action = EnterPositionQuantityScaledAction(priceables=option, trade_duration='1m', name='action')
    trigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1m'),
        actions=action)
    hedgetrigger = PeriodicTrigger(
        trigger_requirements=PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1b'),
        actions=HedgeAction(EqDelta, priceables=hedge_portfolio, trade_duration='1b', name='hedge_action'))
    strategy = Strategy(initial_portfolio=None, triggers=[trigger, hedgetrigger])

    # 2. setup mock api response

    mock_api_response(mocker, api_mock_data())

    # 3. when run backtest

    set_session()
    EquityVolEngine.run_backtest(strategy, start_date, end_date)

    # 4. assert API call

    backtest = BasicBacktestRequest(
        dates=DateConfig(start_date=start_date, end_date=end_date),
        trades=(Trade(legs=tuple(action.priceables),
                      buy_frequency='1m',
                      holding_period='1m',
                      buy_dates=None,
                      exit_dates=None,
                      quantity=1,
                      quantity_type=BacktestTradingQuantityType.quantity
                      ),
                ),
        measures=(FlowVolBacktestMeasure.ALL_MEASURES,),
        delta_hedge_frequency='1b',
        transaction_costs=TransactionCostConfig(
            trade_cost_model=TradingCosts(entry=FixedCostModel(0), exit=FixedCostModel(0)),
            hedge_cost_model=TradingCosts(entry=FixedCostModel(0), exit=FixedCostModel(0))
        ),
        configuration=Configuration(
            market_model=EquityMarketModel.SFK,
            cash_accrual=True,
            combine_roll_signal_entries=False
        )
    )

    mocker.assert_called_with(backtest, decode_instruments=False)
