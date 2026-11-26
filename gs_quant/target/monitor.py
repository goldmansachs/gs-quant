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


class ParameterPeriod(EnumBase, Enum):    
    
    """Enum listing supported parameter periods"""

    _1d = '1d'
    _1w = '1w'
    _1m = '1m'
    _3m = '3m'
    _6m = '6m'
    _1y = '1y'
    _2y = '2y'
    _5y = '5y'
    _10y = '10y'
    _30y = '30y'
    mtd = 'mtd'
    ytd = 'ytd'    


class RateIds(EnumBase, Enum):    
    
    """Enum listing supported rate ids"""

    USD = 'USD'
    EUR = 'EUR'
    JPY = 'JPY'
    GBP = 'GBP'
    CAD = 'CAD'
    AUD = 'AUD'    


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Historical(Base):
    value: Optional[Union[float, str]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MonitorResponseData(Base):
    id_: str = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    result: DictBase = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RateRow(Base):
    period: ParameterPeriod = field(default=None, metadata=field_metadata)
    last: float = field(default=None, metadata=field_metadata)
    change: float = field(default=None, metadata=field_metadata)
    std: float = field(default=None, metadata=field_metadata)
    slope: float = field(default=None, metadata=field_metadata)
    historical: Optional[Historical] = field(default=None, metadata=field_metadata)
    percentage_change: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RatesResponseData(Base):
    name: RateIds = field(default=None, metadata=field_metadata)
    id_: str = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    rows: tuple[RateRow, ...] = field(default=None, metadata=field_metadata)
    libor_id: Optional[str] = field(default=None, metadata=config(field_name='libor_id', exclude=exclude_none))


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Monitor(Base):
    name: str = field(default=None, metadata=field_metadata)
    type_: EntitiesSupported = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    id_: Optional[str] = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    parameters: Optional[MonitorParameters] = field(default=None, metadata=field_metadata)
    created_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    last_updated_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    created_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    last_updated_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    owner_id: Optional[str] = field(default=None, metadata=field_metadata)
    entitlements: Optional[Entitlements] = field(default=None, metadata=field_metadata)
    folder_name: Optional[str] = field(default=None, metadata=field_metadata)
    polling_time: Optional[float] = field(default=None, metadata=field_metadata)
    tags: Optional[tuple[str, ...]] = field(default=None, metadata=field_metadata)
    show_staleness_indicator: Optional[bool] = field(default=None, metadata=field_metadata)
    staleness_threshold: Optional[float] = field(default=None, metadata=field_metadata)
