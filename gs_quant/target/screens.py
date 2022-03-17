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
class ScreenParameters(Base):
    face_value: Optional[float] = field(default=None, metadata=field_metadata)
    direction: Optional[str] = field(default=None, metadata=field_metadata)
    currency: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    gs_liquidity_score: Optional[AssetScreenerRequestFilterLimits] = field(default=None, metadata=field_metadata)
    gs_charge_bps: Optional[AssetScreenerRequestFilterLimits] = field(default=None, metadata=field_metadata)
    gs_charge_dollars: Optional[AssetScreenerRequestFilterLimits] = field(default=None, metadata=field_metadata)
    modified_duration: Optional[AssetScreenerRequestFilterLimits] = field(default=None, metadata=field_metadata)
    issue_date: Optional[AssetScreenerRequestFilterDateLimits] = field(default=None, metadata=field_metadata)
    yield_to_convention: Optional[AssetScreenerRequestFilterLimits] = field(default=None, metadata=field_metadata)
    spread_to_benchmark: Optional[AssetScreenerRequestFilterLimits] = field(default=None, metadata=field_metadata)
    z_spread: Optional[AssetScreenerRequestFilterLimits] = field(default=None, metadata=field_metadata)
    g_spread: Optional[AssetScreenerRequestFilterLimits] = field(default=None, metadata=field_metadata)
    bval_mid_price: Optional[AssetScreenerRequestFilterLimits] = field(default=None, metadata=field_metadata)
    maturity: Optional[AssetScreenerRequestFilterLimits] = field(default=None, metadata=field_metadata)
    amount_outstanding: Optional[AssetScreenerRequestFilterLimits] = field(default=None, metadata=field_metadata)
    rating_standard_and_poors: Optional[AssetScreenerCreditStandardAndPoorsRatingOptions] = field(default=None, metadata=field_metadata)
    seniority: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    sector: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Screen(Base):
    name: str = field(default=None, metadata=field_metadata)
    parameters: ScreenParameters = field(default=None, metadata=field_metadata)
    id_: Optional[str] = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    active: Optional[bool] = field(default=None, metadata=field_metadata)
    owner_id: Optional[str] = field(default=None, metadata=field_metadata)
    created_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    created_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    last_updated_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    last_updated_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    entitlements: Optional[Entitlements] = field(default=None, metadata=field_metadata)
