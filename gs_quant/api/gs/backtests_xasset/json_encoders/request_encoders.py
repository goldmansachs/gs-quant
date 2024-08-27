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

from typing import Any, Iterable

from gs_quant.common import RiskMeasure
from gs_quant.instrument import Instrument
from gs_quant.json_convertors_common import encode_risk_measure


def encode_request_object(data: Any):
    if isinstance(data, RiskMeasure):
        return encode_risk_measure(data)
    if isinstance(data, Instrument):
        return data.to_dict()
    if isinstance(data, tuple):
        return tuple(encode_request_object(d) for d in data)


def legs_decoder(data: Any):
    if data is None:
        return None
    result = [Instrument.from_dict(d) for d in data]
    names = set(getattr(i, 'name', None) for i in result)
    name_idx = 0
    for i in result:
        if i.name is not None:
            continue
        cur_name = 'leg_' + str(name_idx)
        while cur_name in names:
            name_idx += 1
            cur_name = 'leg_' + str(name_idx)
        i.name = cur_name
        name_idx += 1
    return result


def legs_encoder(data: Iterable[Instrument]):
    return [i.to_dict() for i in data]
