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


class BasketPricingEngine(EnumBase, Enum):    
    
    """Pricing engine or baskets"""

    Solactive = 'Solactive'
    Midas = 'Midas'    


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PositionPriceResponse(Base):
    asset_id: Optional[str] = field(default=None, metadata=field_metadata)
    quantity: Optional[float] = field(default=None, metadata=field_metadata)
    reference_weight: Optional[float] = field(default=None, metadata=field_metadata)
    weight: Optional[float] = field(default=None, metadata=field_metadata)
    fx_spot: Optional[float] = field(default=None, metadata=field_metadata)
    spot: Optional[float] = field(default=None, metadata=field_metadata)
    multiplier: Optional[float] = field(default=None, metadata=field_metadata)
    notional: Optional[float] = field(default=None, metadata=field_metadata)
    market_cap: Optional[float] = field(default=None, metadata=field_metadata)
    borrow_cost: Optional[float] = field(default=None, metadata=field_metadata)
    hard_to_borrow: Optional[bool] = field(default=None, metadata=field_metadata)
    composite5_day_adv: Optional[float] = field(default=None, metadata=field_metadata)
    composite10_day_adv: Optional[float] = field(default=None, metadata=field_metadata)
    composite22_day_adv: Optional[float] = field(default=None, metadata=field_metadata)
    adv5_day_pct: Optional[float] = field(default=None, metadata=field_metadata)
    adv10_day_pct: Optional[float] = field(default=None, metadata=field_metadata)
    adv22_day_pct: Optional[float] = field(default=None, metadata=field_metadata)
    median_daily_volume22_day: Optional[float] = field(default=None, metadata=field_metadata)
    tags: Optional[Tuple[PositionTag, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PriceParameters(Base):
    currency: Currency = field(default=None, metadata=field_metadata)
    asset_data_set_id: Optional[str] = field(default=None, metadata=field_metadata)
    divisor: Optional[float] = field(default=None, metadata=field_metadata)
    fractional_shares: Optional[bool] = field(default=False, metadata=field_metadata)
    price_regardless_of_assets_missing_prices: Optional[bool] = field(default=False, metadata=field_metadata)
    frequency: Optional[MarketDataFrequency] = field(default=None, metadata=field_metadata)
    fx_data_set_id: Optional[str] = field(default=None, metadata=field_metadata)
    initial_price: Optional[float] = field(default=None, metadata=field_metadata)
    target_notional: Optional[float] = field(default=None, metadata=field_metadata)
    pricing_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    fallback_date: Optional[str] = field(default=None, metadata=field_metadata)
    vendor: Optional[MarketDataVendor] = field(default=None, metadata=field_metadata)
    use_unadjusted_close_price: Optional[bool] = field(default=False, metadata=field_metadata)
    use_exchange_currency: Optional[bool] = field(default=False, metadata=field_metadata)
    weighting_strategy: Optional[PositionSetWeightingStrategy] = field(default=None, metadata=field_metadata)
    notional_type: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PositionSetPriceInput(Base):
    positions: Tuple[PositionPriceInput, ...] = field(default=None, metadata=field_metadata)
    parameters: PriceParameters = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PositionSetPriceResponse(Base):
    positions: Optional[Tuple[PositionPriceResponse, ...]] = field(default=None, metadata=field_metadata)
    divisor: Optional[float] = field(default=None, metadata=field_metadata)
    initial_price: Optional[float] = field(default=None, metadata=field_metadata)
    target_notional: Optional[float] = field(default=None, metadata=field_metadata)
    actual_notional: Optional[float] = field(default=None, metadata=field_metadata)
    long_notional: Optional[float] = field(default=None, metadata=field_metadata)
    short_notional: Optional[float] = field(default=None, metadata=field_metadata)
    gross_notional: Optional[float] = field(default=None, metadata=field_metadata)
    net_notional: Optional[float] = field(default=None, metadata=field_metadata)
    type_: Optional[str] = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    error_message: Optional[str] = field(default=None, metadata=field_metadata)
    asset_ids_missing_prices: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    asset_ids_missing_fx_fixings: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    asset_ids_missing_market_caps: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    unsupported_currencies: Optional[Tuple[Currency, ...]] = field(default=None, metadata=field_metadata)
    asset_ids_missing_multiplier: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    pricing_engine: Optional[BasketPricingEngine] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)
