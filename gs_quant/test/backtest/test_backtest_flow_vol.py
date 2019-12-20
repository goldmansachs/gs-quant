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

import datetime as dt
from unittest import mock

import gs_quant.target.backtests as backtests
from gs_quant.api.gs.backtests import GsBacktestApi
from gs_quant.backtests.core import Backtest, QuantityType, TradeInMethod
from gs_quant.backtests.strategy_systematic import StrategySystematic
from gs_quant.instrument import EqOption
from gs_quant.session import *
from gs_quant.target.backtests import *

underlierList = [EqOption("MA4B66MW5E27U8P32SB", "3m", 3000, 'Call', 'European'),
                 EqOption("MA4B66MW5E27U8P32SB", "3m", 3000, 'Put', 'European')]

hedge = DeltaHedgeParameters(frequency='Daily')

strategy = StrategySystematic(name="Mock Test",
                              underliers=underlierList,
                              delta_hedge=hedge,
                              quantity=1,
                              quantity_type=QuantityType.Notional,
                              trade_in_method=TradeInMethod.FixedRoll,
                              roll_frequency='1m')


def set_session():
    from gs_quant.session import OAuth2Session
    OAuth2Session.init = mock.MagicMock(return_value=None)
    GsSession.use(Environment.QA, 'client_id', 'secret')


@mock.patch.object(GsBacktestApi, 'run_backtest')
def test_eqstrategies_backtest(mocker):
    start_date = dt.date(2019, 6, 3)
    end_date = dt.date(2019, 6, 5)

    data = (
        FieldValueMap(date='2019-02-18', price=0),
        FieldValueMap(date='2019-02-19', price=0),
        FieldValueMap(date='2019-02-20', price=-14256.398),
    )

    delta = BacktestRisk.from_dict({'name': 'Delta', 'timeseries': [
        {'date': '2019-02-18', 'price': 0},
        {'date': '2019-02-19', 'price': -0.000000000058},
        {'date': '2019-02-20', 'price': 0.000000000262}
    ]})
    vega = BacktestRisk.from_dict({'name': 'Vega', 'timeseries': [
        {'date': '2019-02-18', 'price': -22225.061886411593},
        {'date': '2019-02-19', 'price': -50889.171772423098},
        {'date': '2019-02-20', 'price': 44266.899784030174}
    ]})
    gamma = BacktestRisk.from_dict({'name': 'Gamma', 'timeseries': [
        {'date': '2019-02-18', 'price': 24834.106837453899},
        {'date': '2019-02-19', 'price': 41164.597344927679},
        {'date': '2019-02-20', 'price': 94404.04327008425}
    ]})
    theta = BacktestRisk.from_dict({'name': 'Theta', 'timeseries': [
        {'date': '2019-02-18', 'price': -57618.719522251748},
        {'date': '2019-02-19', 'price': -113749.56356887663},
        {'date': '2019-02-20', 'price': -169875.93826522797}
    ]})

    risk_data = (delta, vega, gamma, theta)

    mock_response = BacktestResult('BT1', performance=data, risks=risk_data, stats=None, backtest_version=1)

    expected_response = BacktestResult('BT1', performance=data, risks=risk_data, stats=None, backtest_version=1)

    set_session()

    mocker.return_value = mock_response

    result = strategy.backtest(start_date, end_date)

    assert result == expected_response

    trading_parameters = BacktestTradingParameters(
        quantity=1,
        quantity_type=QuantityType.Notional.value,
        trade_in_method=TradeInMethod.FixedRoll.value,
        roll_frequency='1m')

    l1 = BacktestStrategyUnderlier(
        instrument=underlierList[0],
        notional_percentage=100,
        hedge=BacktestStrategyUnderlierHedge(risk_details=hedge),
        market_model='SFK')

    l2 = BacktestStrategyUnderlier(
        instrument=underlierList[1],
        notional_percentage=100,
        hedge=BacktestStrategyUnderlierHedge(risk_details=hedge),
        market_model='SFK')

    underliers = [l1, l2]

    backtest_parameters_class: Base = getattr(backtests, 'VolatilityFlowBacktestParameters')

    backtest_parameter_args = {
        'trading_parameters': trading_parameters,
        'underliers': underliers,
        'trade_in_method': TradeInMethod.FixedRoll,
        'scaling_method': None,
        'index_initial_value': 0.0,
    }
    backtest_parameters = backtest_parameters_class.from_dict(backtest_parameter_args)

    params_dict = backtest_parameters.as_dict()
    params_dict["measures"] = [FlowVolBacktestMeasure.ALL_MEASURES]
    params = backtest_parameters_class.from_dict(params_dict)

    backtest = Backtest(name="Mock Test",
                        mq_symbol="Mock Test",
                        parameters=params,
                        start_date=start_date,
                        end_date=end_date,
                        type='Volatility Flow',
                        asset_class=AssetClass.Equity,
                        currency=Currency.USD,
                        cost_netting=False)

    mocker.assert_called_with(backtest, None)
