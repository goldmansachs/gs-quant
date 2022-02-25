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
class AssetScreenerRequestStringOptions(Base):
    options: tuple = None
    type_: str = field(default=None, metadata=config(field_name='type'))


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class AssetScreenerCarbonRequestFilter(Base):
    science_based_target: Optional[AssetScreenerRequestStringOptions] = None
    net_zero_emissions_target: Optional[AssetScreenerRequestStringOptions] = None
    emissions_intensity_enterprise_value: Optional[AssetScreenerRequestFilterLimits] = None
    emissions_intensity_revenue: Optional[AssetScreenerRequestFilterLimits] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class AssetScreenerCreditRequestFilters(Base):
    face_value: Optional[float] = None
    direction: Optional[str] = None
    liquidity_score: Optional[AssetScreenerRequestFilterLimits] = None
    gs_charge_bps: Optional[AssetScreenerRequestFilterLimits] = None
    gs_charge_dollars: Optional[AssetScreenerRequestFilterLimits] = None
    duration: Optional[AssetScreenerRequestFilterLimits] = None
    carbon_data: Optional[AssetScreenerCarbonRequestFilter] = None
    issue_date: Optional[AssetScreenerRequestFilterDateLimits] = None
    yield_: Optional[AssetScreenerRequestFilterLimits] = field(default=None, metadata=config(field_name='yield'))
    spread: Optional[AssetScreenerRequestFilterLimits] = None
    z_spread: Optional[AssetScreenerRequestFilterLimits] = None
    g_spread: Optional[AssetScreenerRequestFilterLimits] = None
    mid_price: Optional[AssetScreenerRequestFilterLimits] = None
    maturity: Optional[AssetScreenerRequestFilterLimits] = None
    amount_outstanding: Optional[AssetScreenerRequestFilterLimits] = None
    rating: Optional[AssetScreenerCreditStandardAndPoorsRatingOptions] = None
    seniority: Optional[AssetScreenerRequestStringOptions] = None
    ticker: Optional[AssetScreenerRequestStringOptions] = None
    cusip: Optional[AssetScreenerRequestStringOptions] = None
    isin: Optional[AssetScreenerRequestStringOptions] = None
    currency: Optional[AssetScreenerRequestStringOptions] = None
    region: Optional[AssetScreenerRequestStringOptions] = None
    sector: Optional[AssetScreenerRequestStringOptions] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class AssetScreenerCreditResponseItem(Base):
    asset_id: Optional[str] = None
    name: Optional[str] = None
    entitlements: Optional[Entitlements] = None
    entitlement_exclusions: Optional[EntitlementExclusions] = None
    cusip: Optional[str] = None
    isin: Optional[str] = None
    bbid: Optional[str] = None
    currency: Optional[Currency] = None
    region: Optional[Region] = None
    seniority: Optional[str] = None
    ticker: Optional[str] = None
    rating_standard_and_poors: Optional[str] = None
    gs_liquidity_score: Optional[float] = None
    amount_outstanding: Optional[float] = None
    maturity: Optional[float] = None
    bval_mid_price: Optional[float] = None
    yield_to_convention: Optional[float] = None
    modified_duration: Optional[float] = None
    spread_to_benchmark: Optional[float] = None
    g_spread: Optional[float] = None
    z_spread: Optional[float] = None
    charge_in_dollars: Optional[str] = None
    charge_in_bps: Optional[str] = None
    science_based_target: Optional[str] = None
    net_zero_emissions_target: Optional[str] = None
    emissions_intensity_enterprise_value: Optional[float] = None
    emissions_intensity_revenue: Optional[float] = None
    direction: Optional[str] = None
    face_value: Optional[float] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class AssetScreenerCreditResponse(Base):
    total_results: int = None
    results: Optional[Tuple[AssetScreenerCreditResponseItem, ...]] = None
    scroll_id: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class AssetScreenerRequest(Base):
    asset_class: Optional[AssetClass] = None
    type_: Optional[AssetType] = field(default=None, metadata=config(field_name='type'))
    scroll: Optional[str] = None
    scroll_id: Optional[str] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    filters: Optional[AssetScreenerCreditRequestFilters] = None
