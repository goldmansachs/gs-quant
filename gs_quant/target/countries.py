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


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CountryXref(Base):
    alpha2: str = None
    alpha3: str = None
    country_code: str = None
    bbid: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Country(Base):
    name: str = None
    id_: str = field(default=None, metadata=config(field_name='id'))
    xref: CountryXref = None
    region: str = None
    sub_region: str = None
    region_code: str = None
    sub_region_code: str = None
    created_time: Optional[datetime.datetime] = None
    last_updated_time: Optional[datetime.datetime] = None
    created_by_id: Optional[str] = None
    last_updated_by_id: Optional[str] = None
    owner_id: Optional[str] = None
    entitlements: Optional[Entitlements] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Subdivision(Base):
    name: str = None
    id_: str = field(default=None, metadata=config(field_name='id'))
    country_id: str = None
    created_time: Optional[datetime.datetime] = None
    last_updated_time: Optional[datetime.datetime] = None
    created_by_id: Optional[str] = None
    last_updated_by_id: Optional[str] = None
    owner_id: Optional[str] = None
    entitlements: Optional[Entitlements] = None
