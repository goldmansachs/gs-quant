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

from typing import Union, Iterable, Tuple

from gs_quant.backtests import TradeInMethod, StrategySystematic
from gs_quant.common import Currency
from gs_quant.instrument import EqOption, EqVarianceSwap, Instrument
from gs_quant.target.backtests import BacktestTradingQuantityType, DeltaHedgeParameters, BacktestSignalSeriesItem, \
    EquityMarketModel


class StrategySystematicFactory:
    @staticmethod
    def get(underliers: Union[Instrument, Iterable[Instrument]],
            quantity: float = 1,
            quantity_type: Union[BacktestTradingQuantityType, str] = BacktestTradingQuantityType.notional,
            trade_in_method: Union[TradeInMethod, str] = TradeInMethod.FixedRoll,
            roll_frequency: str = None,
            scaling_method: str = None,
            index_initial_value: float = 0.0,
            delta_hedge: DeltaHedgeParameters = None,
            name: str = None,
            cost_netting: bool = False,
            currency: Union[Currency, str] = Currency.USD,
            trade_in_signals: Tuple[BacktestSignalSeriesItem, ...] = None,
            trade_out_signals: Tuple[BacktestSignalSeriesItem, ...] = None,
            market_model: Union[EquityMarketModel, str] = EquityMarketModel.SFK,
            roll_date_mode: str = None,
            expiry_date_mode: str = None,
            cash_accrual: bool = True):
        supported_eq_inst = (EqOption, EqVarianceSwap)
        if (isinstance(underliers, Instrument) and isinstance(underliers, supported_eq_inst)) or \
                isinstance(underliers, Iterable) and all(isinstance(u, supported_eq_inst) for u in underliers):
            return StrategySystematic(underliers, quantity, quantity_type, trade_in_method, roll_frequency,
                                      scaling_method, index_initial_value, delta_hedge, name, cost_netting,
                                      currency, trade_in_signals, trade_out_signals, market_model, roll_date_mode,
                                      expiry_date_mode, cash_accrual)
        else:
            raise NotImplementedError('StrategySystematic only implemented for equity underliers')
