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

from gs_quant.base import *
from gs_quant.common import *
import datetime
from typing import Dict, Optional, Tuple, Union
from dataclasses import dataclass, field
from dataclasses_json import LetterCase, config, dataclass_json


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PositionsPricingParameters(Base):
    currency: str = field(default=None, metadata=field_metadata)
    weighting_strategy: str = field(default=None, metadata=field_metadata)
    carryover_positions_for_missing_dates: Optional[bool] = field(default=False, metadata=field_metadata)
    should_reweight: Optional[bool] = field(default=False, metadata=field_metadata)
    allow_fractional_shares: Optional[bool] = field(default=True, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PositionsPricingRequest(Base):
    parameters: PositionsPricingParameters = field(default=None, metadata=field_metadata)
    position_sets: Tuple[PositionSetRequest, ...] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)
