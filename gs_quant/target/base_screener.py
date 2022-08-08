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
class ScreenerColumn(Base):
    column_name: str = field(default=None, metadata=field_metadata)
    entity_parameter: Optional[str] = field(default=None, metadata=field_metadata)
    expression: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ScreenerRow(Base):
    entity_id: str = field(default=None, metadata=field_metadata)
    entity_type: str = field(default=None, metadata=field_metadata)
    universe: Optional[bool] = field(default=None, metadata=field_metadata)
    expand: Optional[bool] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ScreenerData(Base):
    rows: Optional[Tuple[DataRow, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ScreenerParameters(Base):
    rows: Tuple[ScreenerRow, ...] = field(default=None, metadata=field_metadata)
    columns: Tuple[ScreenerColumn, ...] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Screener(Base):
    name: str = field(default=None, metadata=field_metadata)
    parameters: ScreenerParameters = field(default=None, metadata=field_metadata)
    id_: Optional[str] = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    created_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    last_updated_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    created_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    last_updated_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    owner_id: Optional[str] = field(default=None, metadata=field_metadata)
    description: Optional[str] = field(default=None, metadata=field_metadata)
    cron_schedule: Optional[str] = field(default=None, metadata=field_metadata)
    entitlements: Optional[Entitlements] = field(default=None, metadata=field_metadata)
