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
class AssetScreenerCreditResponseItem(Base):
    asset_id: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=field_metadata)
    entitlements: Optional[Entitlements] = field(default=None, metadata=field_metadata)
    entitlement_exclusions: Optional[EntitlementExclusions] = field(default=None, metadata=field_metadata)
    cusip: Optional[str] = field(default=None, metadata=field_metadata)
    isin: Optional[str] = field(default=None, metadata=field_metadata)
    bbid: Optional[str] = field(default=None, metadata=field_metadata)
    currency: Optional[Currency] = field(default=None, metadata=field_metadata)
    region: Optional[Region] = field(default=None, metadata=field_metadata)
    industry: Optional[str] = field(default=None, metadata=field_metadata)
    seniority: Optional[str] = field(default=None, metadata=field_metadata)
    ticker: Optional[str] = field(default=None, metadata=field_metadata)
    rating_standard_and_poors: Optional[str] = field(default=None, metadata=field_metadata)
    gs_liquidity_score: Optional[float] = field(default=None, metadata=field_metadata)
    amount_outstanding: Optional[float] = field(default=None, metadata=field_metadata)
    maturity: Optional[float] = field(default=None, metadata=field_metadata)
    bval_mid_price: Optional[float] = field(default=None, metadata=field_metadata)
    yield_to_convention: Optional[float] = field(default=None, metadata=field_metadata)
    modified_duration: Optional[float] = field(default=None, metadata=field_metadata)
    spread_to_benchmark: Optional[float] = field(default=None, metadata=field_metadata)
    g_spread: Optional[float] = field(default=None, metadata=field_metadata)
    z_spread: Optional[float] = field(default=None, metadata=field_metadata)
    charge_in_dollars: Optional[str] = field(default=None, metadata=field_metadata)
    charge_in_bps: Optional[str] = field(default=None, metadata=field_metadata)
    gs_indicative_benchmark_isin: Optional[str] = field(default=None, metadata=field_metadata)
    gs_indicative_buy_price: Optional[float] = field(default=None, metadata=field_metadata)
    gs_indicative_buy_quantity: Optional[float] = field(default=None, metadata=field_metadata)
    gs_indicative_buy_spread: Optional[float] = field(default=None, metadata=field_metadata)
    gs_indicative_buy_yield: Optional[float] = field(default=None, metadata=field_metadata)
    gs_indicative_pricing_convention: Optional[str] = field(default=None, metadata=field_metadata)
    gs_indicative_sell_price: Optional[float] = field(default=None, metadata=field_metadata)
    gs_indicative_sell_quantity: Optional[float] = field(default=None, metadata=field_metadata)
    gs_indicative_sell_spread: Optional[float] = field(default=None, metadata=field_metadata)
    gs_indicative_sell_yield: Optional[float] = field(default=None, metadata=field_metadata)
    science_based_target: Optional[str] = field(default=None, metadata=field_metadata)
    net_zero_emissions_target: Optional[str] = field(default=None, metadata=field_metadata)
    emissions_intensity_enterprise_value: Optional[float] = field(default=None, metadata=field_metadata)
    emissions_intensity_revenue: Optional[float] = field(default=None, metadata=field_metadata)
    g_percentile: Optional[float] = field(default=None, metadata=field_metadata)
    g_regional_percentile: Optional[float] = field(default=None, metadata=field_metadata)
    es_percentile: Optional[float] = field(default=None, metadata=field_metadata)
    es_disclosure_percentage: Optional[float] = field(default=None, metadata=field_metadata)
    es_momentum_percentile: Optional[float] = field(default=None, metadata=field_metadata)
    direction: Optional[str] = field(default=None, metadata=field_metadata)
    face_value: Optional[float] = field(default=None, metadata=field_metadata)
    indicative_short_financing_label: Optional[str] = field(default=None, metadata=field_metadata)
    indicative_long_financing_label: Optional[str] = field(default=None, metadata=field_metadata)
    country_of_risk: Optional[str] = field(default=None, metadata=field_metadata)
    payment_rank: Optional[str] = field(default=None, metadata=field_metadata)
    industry_sector: Optional[str] = field(default=None, metadata=field_metadata)
    industry_group: Optional[str] = field(default=None, metadata=field_metadata)
    industry_sub_group: Optional[str] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class AssetScreenerCreditResponse(Base):
    total_results: int = field(default=None, metadata=field_metadata)
    results: Optional[Tuple[AssetScreenerCreditResponseItem, ...]] = field(default=None, metadata=field_metadata)
    scroll_id: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class AssetScreenerRequest(Base):
    asset_class: Optional[AssetClass] = field(default=None, metadata=field_metadata)
    type_: Optional[AssetType] = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    scroll: Optional[str] = field(default=None, metadata=field_metadata)
    scroll_id: Optional[str] = field(default=None, metadata=field_metadata)
    limit: Optional[int] = field(default=None, metadata=field_metadata)
    offset: Optional[int] = field(default=None, metadata=field_metadata)
    filters: Optional[AssetScreenerCreditRequestFilters] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)
