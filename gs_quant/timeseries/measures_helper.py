"""
Copyright 2021 Goldman Sachs.
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
from numbers import Real

from gs_quant.errors import MqValueError


class EdrDataReference(Enum):
    DELTA_CALL = 'delta_call'
    DELTA_PUT = 'delta_put'
    SPOT = 'spot'


class VolReference(Enum):
    DELTA_CALL = 'delta_call'
    DELTA_PUT = 'delta_put'
    DELTA_NEUTRAL = 'delta_neutral'
    NORMALIZED = 'normalized'
    SPOT = 'spot'
    FORWARD = 'forward'


def preprocess_implied_vol_strikes_eq(strike_reference: VolReference = None, relative_strike: Real = None):
    if relative_strike is None and strike_reference != VolReference.DELTA_NEUTRAL:
        raise MqValueError('Relative strike must be provided if your strike reference is not delta_neutral')

    if strike_reference == VolReference.DELTA_NEUTRAL:
        raise MqValueError('delta_neutral strike reference is not supported for equities.')

    if strike_reference == VolReference.DELTA_PUT:
        relative_strike = abs(100 - relative_strike)
    relative_strike = relative_strike if strike_reference == VolReference.NORMALIZED else relative_strike / 100

    ref_string = "delta" if strike_reference in (VolReference.DELTA_CALL, VolReference.DELTA_PUT,
                                                 VolReference.DELTA_NEUTRAL) else strike_reference.value

    return ref_string, relative_strike
