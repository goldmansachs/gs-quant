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


class DataRow(DictBase):
    pass


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OrderByBody(Base):
    column_name: Optional[str] = field(default=None, metadata=field_metadata)
    type_: Optional[str] = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FilterRequest(Base):
    scroll: Optional[str] = field(default=None, metadata=field_metadata)
    scroll_id: Optional[str] = field(default=None, metadata=field_metadata)
    include_columns: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    filters: Optional[Tuple[DictBase, ...]] = field(default=None, metadata=field_metadata)
    order_by: Optional[OrderByBody] = field(default=None, metadata=field_metadata)
    limit: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FilteredData(Base):
    total_results: Optional[float] = field(default=None, metadata=field_metadata)
    results: Optional[Tuple[DataRow, ...]] = field(default=None, metadata=field_metadata)
    scroll: Optional[str] = field(default=None, metadata=field_metadata)
    scroll_id: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class AnalyticsScreen(Base):
    name: str = field(default=None, metadata=field_metadata)
    filter_parameters: FilterRequest = field(default=None, metadata=field_metadata)
    base_screener: str = field(default=None, metadata=field_metadata)
    id_: Optional[str] = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    created_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    last_updated_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    created_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    last_updated_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    owner_id: Optional[str] = field(default=None, metadata=field_metadata)
    description: Optional[str] = field(default=None, metadata=field_metadata)
    entitlements: Optional[Entitlements] = field(default=None, metadata=field_metadata)
    hidden_columns: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
