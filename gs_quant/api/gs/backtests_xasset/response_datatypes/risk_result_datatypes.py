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

from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json, LetterCase, config

from gs_quant.api.gs.backtests_xasset.json_encoders.response_datatypes.risk_result_datatype_encoders import \
    encode_series_result, decode_series_result, encode_dataframe_result, decode_dataframe_result


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class RiskResultWithData:
    unit: Optional[str] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class FloatWithData(RiskResultWithData):
    result: Optional[float] = None
    type: str = 'float'


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class StringWithData(RiskResultWithData):
    result: Optional[str] = None
    type: str = 'string'


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class VectorWithData(RiskResultWithData):
    result: Optional[pd.Series] = field(default=None, metadata=config(encoder=encode_series_result,
                                                                      decoder=decode_series_result))
    type: str = 'vector'


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class MatrixWithData(RiskResultWithData):
    result: pd.DataFrame = field(default=None, metadata=config(encoder=encode_dataframe_result,
                                                               decoder=decode_dataframe_result))
    type: str = 'matrix'
