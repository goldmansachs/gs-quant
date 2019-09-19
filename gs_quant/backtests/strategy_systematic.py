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
import re
from typing import Iterable

import gs_quant.target.backtests as backtests
from gs_quant.api.gs.backtests import GsBacktestApi
from gs_quant.backtests.core import Backtest, QuantityType, TradeInMethod
from gs_quant.backtests.flow_vol_backtest_measure import FlowVolBacktestMeasure
from gs_quant.errors import MqValueError
from gs_quant.instrument import EqOption
from gs_quant.target.backtests import *

_logger = logging.getLogger(__name__)

BACKTEST_TYPE_NAME = 'VolatilityFlow'
BACKTEST_TYPE_VALUE = 'Volatility Flow'
EQ_MARKET_MODEL = 'SFK'
ISO_FORMAT = r"^([0-9]{4})-([0-9]{2})-([0-9]{2})$"


class StrategySystematic:
    """Equity back testing systematic strategy"""

    def __init__(self,
                 underliers: Union[EqOption, Iterable[EqOption]],
                 quantity: float = 1,
                 quantity_type: Union[QuantityType, str] = QuantityType.Notional,
                 trade_in_method: Union[TradeInMethod, str] = TradeInMethod.FixedRoll,
                 roll_frequency: str = None,
                 scaling_method: str = None,
                 index_initial_value: float = 0.0,
                 delta_hedge: DeltaHedgeParameters = None,
                 name: str = None,
                 cost_netting: bool = False,
                 currency: Union[Currency, str] = Currency.USD,
                 measures: Iterable[FlowVolBacktestMeasure] = (FlowVolBacktestMeasure.ALL_MEASURES,)):
        self.__cost_netting = cost_netting
        self.__currency = get_enum_value(Currency, currency)
        self.__name = name
        self.__backtest_type = BACKTEST_TYPE_NAME

        trade_in_method = get_enum_value(TradeInMethod, trade_in_method).value

        self.__trading_parameters = BacktestTradingParameters(
            quantity=quantity,
            quantityType=get_enum_value(QuantityType, quantity_type).value,
            tradeInMethod=trade_in_method,
            rollFrequency=roll_frequency)

        self.__underliers = []

        if isinstance(underliers, EqOption):
            instrument = underliers
            notional_percentage = 100
            self.check_underlier_fields(instrument)
            self.__underliers.append(BacktestStrategyUnderlier(
                instrument=instrument,
                notionalPercentage=notional_percentage,
                hedge=BacktestStrategyUnderlierHedge(riskDetails=delta_hedge),
                marketModel=EQ_MARKET_MODEL))
        else:
            for eq_option in underliers:
                if isinstance(eq_option, tuple):
                    instrument = eq_option[0]
                    notional_percentage = eq_option[1]
                elif isinstance(eq_option, EqOption):
                    instrument = eq_option
                    notional_percentage = 100
                else:
                    raise MqValueError('The format of the backtest asset is incorrect.')
                self.check_underlier_fields(instrument)
                self.__underliers.append(BacktestStrategyUnderlier(
                    instrument=instrument,
                    notionalPercentage=notional_percentage,
                    hedge=BacktestStrategyUnderlierHedge(riskDetails=delta_hedge),
                    marketModel=EQ_MARKET_MODEL))

        backtest_parameters_class: Base = getattr(backtests, self.__backtest_type + 'BacktestParameters')
        backtest_parameter_args = {
            'tradingParameters': self.__trading_parameters,
            'underliers': self.__underliers,
            'tradeInMethod': trade_in_method,
            'scalingMethod': scaling_method,
            'indexInitialValue': index_initial_value,
            'measures': [measure.str_value for measure in measures]
        }
        self.__backtest_parameters = backtest_parameters_class.from_dict(backtest_parameter_args)

    def check_underlier_fields(
            self,
            underlier: EqOption) -> bool:

        # validation for different fields
        if isinstance(underlier.expirationDate, datetime.date):
            raise MqValueError('Datetime.date format for expiration date field is not supported for backtest service')
        elif re.search(ISO_FORMAT, underlier.expirationDate) is not None:
            if datetime.datetime.strptime(underlier.expirationDate, "%Y-%m-%d"):
                raise MqValueError('Date format for expiration date field is not supported for backtest service')

        return True

    def backtest(
            self,
            start: datetime.date = None,
            end: datetime.date = datetime.date.today() - datetime.timedelta(days=1),
            is_async: bool = False) -> Union[Backtest, BacktestResult]:

        backtest = Backtest(name=self.__name,
                            mqSymbol=self.__name,
                            parameters=self.__backtest_parameters.as_dict(),
                            startDate=start,
                            endDate=end,
                            type=BACKTEST_TYPE_VALUE,
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
