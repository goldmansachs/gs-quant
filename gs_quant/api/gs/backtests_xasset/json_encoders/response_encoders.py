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
import pandas as pd

from typing import Dict, Any, Tuple, Union

from gs_quant.api.gs.backtests_xasset.json_encoders.response_datatypes.generic_datatype_encoders import \
    decode_inst_tuple, decode_inst
from gs_quant.api.gs.backtests_xasset.json_encoders.response_datatypes.risk_result_datatype_encoders import \
    encode_series_result, encode_dataframe_result
from gs_quant.api.gs.backtests_xasset.json_encoders.response_datatypes.risk_result_encoders import decode_risk_result, \
    decode_risk_result_with_data
from gs_quant.api.gs.backtests_xasset.response_datatypes.backtest_datatypes import Transaction, TransactionDirection
from gs_quant.api.gs.backtests_xasset.response_datatypes.risk_result_datatypes import RiskResultWithData
from gs_quant.common import Currency, CurrencyName, RiskMeasure
from gs_quant.json_convertors_common import encode_risk_measure, decode_risk_measure
from gs_quant.priceable import PriceableImpl
from gs_quant.target.backtests import FlowVolBacktestMeasure


def encode_response_obj(data: Any) -> Dict:
    if isinstance(data, RiskMeasure):
        return encode_risk_measure(data)
    if isinstance(data, pd.Series):
        return encode_series_result(data)
    if isinstance(data, pd.DataFrame):
        return encode_dataframe_result(data)
    return data.to_dict()


def decode_leg_refs(d: dict) -> Dict[str, PriceableImpl]:
    return {k: decode_inst(v) for k, v in d.items()}


def decode_risk_measure_refs(d: dict) -> Dict[str, RiskMeasure]:
    return {k: decode_risk_measure(v) for k, v in d.items()}


def decode_result_tuple(results: tuple):
    return tuple(decode_risk_result(r) for r in results)


def decode_basic_bt_measure_dict(results: dict) -> Dict[FlowVolBacktestMeasure, Dict[dt.date, RiskResultWithData]]:
    return {FlowVolBacktestMeasure(k): {dt.date.fromisoformat(d): decode_risk_result_with_data(r) for d, r in v.items()}
            for k, v in results.items()}


def decode_basic_bt_transactions(results: dict, decode_instruments: bool = True) -> \
        Dict[dt.date, Tuple[Transaction, ...]]:
    def to_ccy(s: str) -> Union[Currency, CurrencyName, str]:
        if s in [x.value for x in Currency]:
            return Currency(s)
        elif s in [x.value for x in CurrencyName]:
            return CurrencyName(s)
        else:
            return s

    return {dt.date.fromisoformat(k): tuple(
            Transaction(decode_inst_tuple(t['portfolio']) if decode_instruments else t['portfolio'],
                        t.get('portfolio_price'), t.get('cost'), to_ccy(t['currency']) if t.get('currency') else None,
                        TransactionDirection(t['direction']) if t.get('direction') else None, t.get('quantity'))
            for t in v) for k, v in results.items()}
