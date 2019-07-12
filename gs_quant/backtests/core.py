
from gs_quant.target.backtests import Backtest as __Backtest, BacktestResult
from gs_quant.base import EnumBase
from enum import Enum
from typing import Tuple


# TODO add these in Studio as a standalone JSON, so they will be generated

class BacktestType(EnumBase, Enum):
    Volatility = 'Volatility'
    VolatilityFlow = 'Volatility Flow'


class EquityMarketModel(EnumBase, Enum):
    SFK = 'SFK'
    SVR = 'SVR'


class QuantityType(EnumBase, Enum):
    Notional = 'notional'
    Quantity = 'quantity'
    Vega = 'vega'


class TradeInMethod(EnumBase, Enum)  :
    BackToBack = 'backToBack'
    FixedRoll = 'fixedRoll'


class Backtest(__Backtest):

    def get_results(self) -> Tuple[BacktestResult, ...]:
        from gs_quant.api.gs.backtests import GsBacktestApi
        return GsBacktestApi.get_results(backtest_id=self.id)
