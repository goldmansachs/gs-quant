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
from typing import Any, Type

from gs_quant.api.gs.backtests_xasset.response_datatypes.risk_result import RiskResultsByDate, RefType
from gs_quant.api.gs.backtests_xasset.response_datatypes.risk_result_datatypes import FloatWithData, StringWithData, \
    VectorWithData, MatrixWithData, RiskResultWithData

_type_to_datatype_map = {'float': FloatWithData, 'string': StringWithData,
                         'vector': VectorWithData, 'matrix': MatrixWithData}


def map_result_to_datatype(data: Any) -> Type[RiskResultWithData]:
    if isinstance(data, (float, int)):
        return FloatWithData
    if isinstance(data, str):
        return StringWithData
    if isinstance(data, pd.Series):
        return VectorWithData
    if isinstance(data, pd.DataFrame):
        return MatrixWithData
    raise ValueError('Cannot assign result type to data')


def decode_risk_result_with_data(r: dict) -> RiskResultWithData:
    return _type_to_datatype_map[r['type']].from_dict(r)


def decode_risk_result(d: dict) -> RiskResultsByDate:
    refs = {RefType(k): v for k, v in d['refs'].items()}
    result = {dt.date.fromisoformat(k): decode_risk_result_with_data(v) for k, v in d['result'].items()}
    return RiskResultsByDate(refs, result)
