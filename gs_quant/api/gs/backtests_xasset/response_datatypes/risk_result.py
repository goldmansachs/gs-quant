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

from dataclasses import dataclass
from enum import Enum
from typing import Dict

from dataclasses_json import dataclass_json, LetterCase

from gs_quant.api.gs.backtests_xasset.response_datatypes.risk_result_datatypes import RiskResultWithData


class RefType(Enum):
    LEG_ID = 'legId'
    RISK_MEASURE = 'riskMeasure'


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class RiskResultsByDate:
    refs: Dict[RefType, str]
    result: Dict[dt.date, RiskResultWithData]
