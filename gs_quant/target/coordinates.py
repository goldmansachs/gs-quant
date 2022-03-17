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
from enum import Enum


class MDAPIQueryField(EnumBase, Enum):    
    
    ask = 'ask'
    bid = 'bid'
    mid = 'mid'
    expectedDataQuality = 'expectedDataQuality'
    actualDataQuality = 'actualDataQuality'    


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MDAPIDataQuery(Base):
    market_data_coordinates: Tuple[MarketDataCoordinate, ...] = field(default=None, metadata=field_metadata)
    format_: Optional[Format] = field(default=None, metadata=config(field_name='format', exclude=exclude_none))
    pricing_location: Optional[PricingLocation] = field(default=None, metadata=field_metadata)
    selector_function: Optional[str] = field(default=None, metadata=field_metadata)
    samples: Optional[int] = field(default=None, metadata=field_metadata)
    interval: Optional[str] = field(default=None, metadata=field_metadata)
    vendor: Optional[MarketDataVendor] = field(default=None, metadata=field_metadata)
    start_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    end_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    start_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    end_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    real_time: Optional[bool] = field(default=True, metadata=field_metadata)
    fields: Optional[Tuple[MDAPIQueryField, ...]] = field(default=None, metadata=field_metadata)
    time_filter: Optional[TimeFilter] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MDAPIDataQueryResponse(Base):
    data: Optional[Tuple[FieldValueMap, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MDAPIDataBatchResponse(Base):
    request_id: Optional[str] = field(default=None, metadata=field_metadata)
    responses: Optional[Tuple[MDAPIDataQueryResponse, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)
