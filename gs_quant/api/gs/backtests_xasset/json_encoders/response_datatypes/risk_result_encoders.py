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
from typing import Any, Type

import pandas as pd

from gs_quant.api.gs.backtests_xasset.response_datatypes.risk_result import (
    RiskResultsByDate,
    RefType,
    RiskResultsError,
    RiskResults,
)
from gs_quant.api.gs.backtests_xasset.response_datatypes.risk_result_datatypes import (
    FloatWithData,
    StringWithData,
    VectorWithData,
    MatrixWithData,
    RiskResultWithData,
    DefnValuesWithData,
    DictsWithData,
)
from gs_quant.priceable import PriceableImpl

_type_to_datatype_map = {
    'float': FloatWithData,
    'string': StringWithData,
    'vector': VectorWithData,
    'matrix': MatrixWithData,
    'defn': DefnValuesWithData,
    'dict': DictsWithData
}


def map_result_to_datatype(data: Any) -> Type[RiskResultWithData]:
    if isinstance(data, (float, int)):
        return FloatWithData
    if isinstance(data, str):
        return StringWithData
    if isinstance(data, pd.Series):
        return VectorWithData
    if isinstance(data, pd.DataFrame):
        return MatrixWithData
    if isinstance(data, PriceableImpl):
        return DefnValuesWithData
    if isinstance(data, dict):
        return DictsWithData
    raise ValueError('Cannot assign result type to data')


def decode_risk_result_with_data(r: dict) -> RiskResultWithData:
    return _type_to_datatype_map[r['type']].from_dict(r)


def decode_risk_result(d: dict) -> RiskResults:
    refs = {RefType(k): v for k, v in d['refs'].items()}
    if 'result' in d:
        result = {dt.date.fromisoformat(k): decode_risk_result_with_data(v) for k, v in d['result'].items()}
        return RiskResultsByDate(refs, result)
    else:
        return RiskResultsError(refs, d['error'], d['trace_id'])
