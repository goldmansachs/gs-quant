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

import datetime as dt
from dataclasses import dataclass, field
from typing import Any, Optional

from dataclasses_json import LetterCase, config, dataclass_json

from gs_quant.api.gs.backtests_xasset.json_encoders.response_datatypes.generic_datatype_encoders import (
    decode_daily_portfolio,
)
from gs_quant.api.gs.backtests_xasset.json_encoders.response_encoders import (
    decode_basic_bt_measure_dict,
    decode_basic_bt_transactions,
    decode_leg_refs,
    decode_result_tuple,
    decode_risk_measure_refs,
)
from gs_quant.api.gs.backtests_xasset.response_datatypes.backtest_datatypes import AdditionalResults, Transaction
from gs_quant.api.gs.backtests_xasset.response_datatypes.generic_backtest_datatypes import decode_strategy
from gs_quant.api.gs.backtests_xasset.response_datatypes.risk_result import RiskResults
from gs_quant.api.gs.backtests_xasset.response_datatypes.risk_result_datatypes import RiskResultWithData
from gs_quant.common import RiskMeasure
from gs_quant.instrument import Instrument
from gs_quant.priceable import PriceableImpl
from gs_quant.target.backtests import FlowVolBacktestMeasure


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class RiskResponse:
    legRefs: dict[str, PriceableImpl] = field(default=None, metadata=config(decoder=decode_leg_refs))
    riskMeasureRefs: dict[str, RiskMeasure] = field(default=None, metadata=config(decoder=decode_risk_measure_refs))
    results: tuple[RiskResults, ...] = field(default=None, metadata=config(decoder=decode_result_tuple))

    def serializable(self):
        self.legRefs = {
            k: {**v.to_dict(), 'properties': {**v.to_dict().get('properties', {}), 'name': v.name}}
            for k, v in self.legRefs.items()
        }
        return self


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class BacktestResponse:
    measures: dict[FlowVolBacktestMeasure, dict[dt.date, RiskResultWithData]] = field(
        default=None, metadata=config(decoder=decode_basic_bt_measure_dict)
    )
    portfolio: dict[dt.date, tuple[Instrument, ...]] = field(
        default=None, metadata=config(decoder=decode_daily_portfolio)
    )
    transactions: dict[dt.date, tuple[Transaction, ...]] = field(
        default=None, metadata=config(decoder=decode_basic_bt_transactions)
    )
    strategy: Optional[object] = field(default=None, metadata=config(decoder=decode_strategy))
    additional_results: Optional[AdditionalResults] = field(default=None)

    @classmethod
    def from_dict_custom(cls, data: Any, decode_instruments: bool = True):
        if decode_instruments:
            return cls.from_dict(data)
        return BacktestResponse(
            measures=decode_basic_bt_measure_dict(data['measures']),
            portfolio=decode_daily_portfolio(data['portfolio'], decode_instruments),
            transactions=decode_basic_bt_transactions(data['transactions'], decode_instruments),
            strategy=decode_strategy(data['strategy']) if data.get('strategy') is not None else None,
            additional_results=AdditionalResults.from_dict_custom(data['additional_results'], decode_instruments)
            if data['additional_results'] is not None
            else None,
        )


# Backward compatibility aliases
BasicBacktestResponse = BacktestResponse
GenericBacktestResponse = BacktestResponse
