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

import copy

from enum import Enum
from typing import Tuple, Dict, Optional, Union

from gs_quant.base import RiskMeasureParameter
from gs_quant.common import RiskMeasure, ParameterisedRiskMeasure

from gs_quant import common
from gs_quant import risk


def gsq_rm_for_name(name: str) -> Optional[RiskMeasure]:
    if name is None or name not in dir(risk):
        return None
    return getattr(risk, name)


def encode_risk_measure(rm: RiskMeasure) -> Dict:
    result = rm.as_dict(as_camel_case=True)
    if rm.parameters is not None:
        result['parameters'] = rm.parameters.as_dict(as_camel_case=True)
    return result


def encode_risk_measure_tuple(blob: Tuple[RiskMeasure, ...]) -> Tuple[Dict, ...]:
    return tuple(encode_risk_measure(rm) for rm in blob)


def _decode_param(data: dict) -> Optional[RiskMeasureParameter]:
    params = data.get('parameters', None)
    if params is not None and isinstance(params, dict) and 'parameterType' in params:
        cls_name = params['parameterType'] + 'Parameter'
        parameter_cls = getattr(common, cls_name)
        parameter = parameter_cls(**{k: v for k, v in params.items() if k != 'parameterType'})
        return parameter
    return None


def _decode_gsq_risk_measure(data: dict) -> Optional[RiskMeasure]:
    def _enum_or_str_equal(a: Optional[Union[Enum, str]], b: Optional[Union[Enum, str]]):
        return (a is None and b is None) or (str(a).lower() == str(b).lower())

    name = data.get('name', None)
    gsq_rm = gsq_rm_for_name(name)
    if gsq_rm is None:
        return None
    asset_class = data.get('assetClass', None)
    measure_type = data.get('measureType', None)
    if _enum_or_str_equal(asset_class, gsq_rm.asset_class) and _enum_or_str_equal(measure_type, gsq_rm.measure_type):
        result = copy.copy(gsq_rm)
        param = _decode_param(data)
        if param:
            result.parameters = param
        return result
    return None


def decode_risk_measure(data: Dict) -> RiskMeasure:
    result = _decode_gsq_risk_measure(data)
    if result is not None:
        return result
    if 'parameters' in data:
        result = ParameterisedRiskMeasure.from_dict(data)
        result.parameters = _decode_param(data)
    else:
        result = RiskMeasure.from_dict(data)
    return result


def decode_risk_measure_tuple(blob: Tuple[Dict, ...]) -> Tuple[RiskMeasure, ...]:
    return tuple(decode_risk_measure(s) for s in blob) if isinstance(blob, (tuple, list)) else None
