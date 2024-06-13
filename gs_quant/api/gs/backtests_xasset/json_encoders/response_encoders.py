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

import pandas as pd

from typing import Dict, Any

from gs_quant.api.gs.backtests_xasset.json_encoders.response_datatypes.risk_result_datatype_encoders import \
    encode_series_result, encode_dataframe_result
from gs_quant.api.gs.backtests_xasset.json_encoders.response_datatypes.risk_result_encoders import decode_risk_result
from gs_quant.common import RiskMeasure
from gs_quant.instrument import Instrument
from gs_quant.json_convertors_common import encode_risk_measure, decode_risk_measure
from gs_quant.priceable import PriceableImpl


def encode_response_obj(data: Any) -> Dict:
    if isinstance(data, RiskMeasure):
        return encode_risk_measure(data)
    if isinstance(data, pd.Series):
        return encode_series_result(data)
    if isinstance(data, pd.DataFrame):
        return encode_dataframe_result(data)
    return data.to_dict()


def decode_leg_refs(d: dict) -> Dict[str, PriceableImpl]:
    return {k: Instrument.from_dict(v) for k, v in d.items()}


def decode_risk_measure_refs(d: dict) -> Dict[str, RiskMeasure]:
    return {k: decode_risk_measure(v) for k, v in d.items()}


def decode_result_tuple(results: tuple):
    return tuple(decode_risk_result(r) for r in results)
