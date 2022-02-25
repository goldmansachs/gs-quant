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
class ScreenParameters(Base):
    face_value: Optional[float] = None
    direction: Optional[str] = None
    currency: Optional[Tuple[str, ...]] = None
    gs_liquidity_score: Optional[AssetScreenerRequestFilterLimits] = None
    gs_charge_bps: Optional[AssetScreenerRequestFilterLimits] = None
    gs_charge_dollars: Optional[AssetScreenerRequestFilterLimits] = None
    modified_duration: Optional[AssetScreenerRequestFilterLimits] = None
    issue_date: Optional[AssetScreenerRequestFilterDateLimits] = None
    yield_to_convention: Optional[AssetScreenerRequestFilterLimits] = None
    spread_to_benchmark: Optional[AssetScreenerRequestFilterLimits] = None
    z_spread: Optional[AssetScreenerRequestFilterLimits] = None
    g_spread: Optional[AssetScreenerRequestFilterLimits] = None
    bval_mid_price: Optional[AssetScreenerRequestFilterLimits] = None
    maturity: Optional[AssetScreenerRequestFilterLimits] = None
    amount_outstanding: Optional[AssetScreenerRequestFilterLimits] = None
    rating_standard_and_poors: Optional[AssetScreenerCreditStandardAndPoorsRatingOptions] = None
    seniority: Optional[Tuple[str, ...]] = None
    sector: Optional[Tuple[str, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Screen(Base):
    name: str = None
    parameters: ScreenParameters = None
    id_: Optional[str] = field(default=None, metadata=config(field_name='id'))
    active: Optional[bool] = None
    owner_id: Optional[str] = None
    created_by_id: Optional[str] = None
    created_time: Optional[datetime.datetime] = None
    last_updated_by_id: Optional[str] = None
    last_updated_time: Optional[datetime.datetime] = None
    entitlements: Optional[Entitlements] = None
