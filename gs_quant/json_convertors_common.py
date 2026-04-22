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
from gs_quant.target import measures as target_measures


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


def _lookup_risk_measure_by_fields(data: dict) -> Optional[RiskMeasure]:
    """Look up a well-known RiskMeasure when 'name' is absent, using value or assetClass+measureType."""
    # Boltweb measures: extract name from 'boltweb:' value prefix
    value = data.get('value', '')
    if isinstance(value, str) and value.startswith('boltweb:'):
        name = value.split('boltweb:', 1)[1]
        enriched = {**data, 'name': name}
        # Try gs_quant.risk lookup first
        result = _decode_gsq_risk_measure(enriched)
        if result is not None:
            return result
        # Fall through to standard from_dict path with name populated
        if 'parameters' in data:
            result = ParameterisedRiskMeasure.from_dict(enriched)
            result.parameters = _decode_param(data)
            return result
        return RiskMeasure(value=value, name=name)

    # Standard measures: match by assetClass + measureType against gs_quant.target.measures
    asset_class = data.get('assetClass')
    measure_type = data.get('measureType')
    if asset_class and measure_type:

        def _str_equal(a, b):
            return a is not None and b is not None and str(a).lower() == str(b).lower()

        unit = data.get('unit')
        for attr_name in dir(target_measures):
            candidate = getattr(target_measures, attr_name)
            if (
                isinstance(candidate, RiskMeasure)
                and _str_equal(asset_class, candidate.asset_class)
                and _str_equal(measure_type, candidate.measure_type)
            ):
                if unit is None or _str_equal(unit, candidate.unit):
                    return copy.copy(candidate)

    return None


def decode_risk_measure(data: Dict) -> RiskMeasure:
    result = _decode_gsq_risk_measure(data)
    if result is not None:
        return result
    # Fallback: try to match by value prefix or assetClass+measureType when name is absent
    result = _lookup_risk_measure_by_fields(data)
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
