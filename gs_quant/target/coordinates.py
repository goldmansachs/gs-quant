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


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MDAPIDataQuery(Base):
    market_data_coordinates: Tuple[MarketDataCoordinate, ...] = None
    format_: Optional[Format] = field(default=None, metadata=config(field_name='format'))
    pricing_location: Optional[PricingLocation] = None
    selector_function: Optional[str] = None
    samples: Optional[int] = None
    interval: Optional[str] = None
    vendor: Optional[MarketDataVendor] = None
    start_time: Optional[datetime.datetime] = None
    end_time: Optional[datetime.datetime] = None
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None
    real_time: Optional[bool] = True
    fields: Optional[Tuple[MDAPIQueryField, ...]] = None
    time_filter: Optional[TimeFilter] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MDAPIDataQueryResponse(Base):
    data: Optional[Tuple[FieldValueMap, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MDAPIDataBatchResponse(Base):
    request_id: Optional[str] = None
    responses: Optional[Tuple[MDAPIDataQueryResponse, ...]] = None
