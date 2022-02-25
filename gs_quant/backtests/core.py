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

from enum import Enum
from typing import Tuple, NamedTuple, Union
import datetime
from gs_quant.base import EnumBase
from gs_quant.target.backtests import Backtest as __Backtest, BacktestResult, FlowVolBacktestMeasure
from typing import Optional


# TODO add these in Studio as a standalone JSON, so they will be generated


class TradeInMethod(EnumBase, Enum):
    FixedRoll = 'fixedRoll'


class Backtest(__Backtest):

    def get_results(self) -> Tuple[BacktestResult, ...]:
        from gs_quant.api.gs.backtests import GsBacktestApi
        return GsBacktestApi.get_results(backtest_id=self.id)


class MarketModel(EnumBase, Enum):
    STICKY_FIXED_STRIKE = "SFK"
    STICKY_DELTA = "SD"


class TimeWindow(NamedTuple):
    start: Union[datetime.time, datetime.datetime] = None
    end: Union[datetime.time, datetime.datetime] = None


class ValuationFixingType(EnumBase, Enum):
    PRICE = 'price'


class ValuationMethod(NamedTuple):
    data_tag: ValuationFixingType = ValuationFixingType.PRICE
    window: Optional[TimeWindow] = None
