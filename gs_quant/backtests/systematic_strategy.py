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
import logging
from .core import Backtest, BacktestType, EquityMarketModel, QuantityType, TradeInMethod
from gs_quant.instrument import EqOption
import gs_quant.target.backtests as backtests
from gs_quant.target.backtests import *
from gs_quant.api.gs.backtests import GsBacktestApi

_logger = logging.getLogger(__name__)


class EqSystematicStrategy:
    """Equity back testing systematic strategy"""

    def __init__(self,
                 underliers: [(EqOption, float), ...],
                 quantity: float = 1,
                 quantity_type: Union[QuantityType, str] = QuantityType.Notional,
                 backtest_type: Union[BacktestType, str] = BacktestType.VolatilityFlow,
                 market_model: Union[EquityMarketModel, str] = EquityMarketModel.SFK,
                 trade_in_method: Union[TradeInMethod, str] = TradeInMethod.FixedRoll,
                 roll_frequency: str = None,
                 scaling_method: str = None,
                 index_initial_value: float = 0,
                 delta_hedge: DeltaHedgeParameters = None,
                 name: str = None,
                 cost_netting: bool = False,
                 currency: Union[Currency, str] = Currency.USD):
        self.__cost_netting = cost_netting
        self.__currency = get_enum_value(Currency, currency)
        self.__name = name
        self.__backtest_type = get_enum_value(BacktestType, backtest_type)

        trade_in_method = get_enum_value(TradeInMethod, trade_in_method).value

        self.__trading_parameters = BacktestTradingParameters(
            quantity=quantity,
            quantityType=get_enum_value(QuantityType, quantity_type).value,
            tradeInMethod=trade_in_method,
            rollFrequency=roll_frequency)

        self.__underliers = []

        for eq_option in underliers:
            # TODO: Only support option strike type "Absolute", need to support "Delta" and "Fwd Percentage" as well
            self.__underliers.append(BacktestStrategyUnderlier(
                instrument= eq_option[0],
                notionalPercentage = eq_option[1],
                hedge=BacktestStrategyUnderlierHedge(riskDetails=delta_hedge),
                marketModel=get_enum_value(EquityMarketModel, market_model).value))


        backtest_parameters_class: Base = getattr(backtests, self.__backtest_type.name + 'BacktestParameters')
        backtest_parameter_args = {
            'tradingParameters': self.__trading_parameters,
            'underliers': self.__underliers,
            'tradeInMethod': trade_in_method,
            'scalingMethod': scaling_method,
            'indexInitialValue': index_initial_value
        }

        self.__backtest_parameters = backtest_parameters_class.from_dict(backtest_parameter_args)

    def backtest(
            self,
            start: datetime.date,
            end: datetime.date,
            is_async: bool = False) -> Union[Backtest, BacktestResult]:

        backtest = Backtest(name=self.__name,
                            mqSymbol=self.__name,
                            parameters=self.__backtest_parameters.as_dict(),
                            startDate=start,
                            endDate=end,
                            type=self.__backtest_type.value,
                            assetClass=AssetClass.Equity,
                            currency=self.__currency,
                            costNetting=self.__cost_netting)

        if is_async:
            # Create back test ...
            response = GsBacktestApi.create_backtest(backtest)

            # ... and schedule it
            GsBacktestApi.schedule_backtest(backtest_id=response.id)
        else:
            # Run on-the-fly back test
            response = GsBacktestApi.run_backtest(backtest)

        return response
