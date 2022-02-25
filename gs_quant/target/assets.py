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


class AllocatorType(EnumBase, Enum):    
    
    """Allocator type defines the type of investor company managing an asset"""

    Advisor = 'Advisor'
    Consultant_Institutional = 'Consultant (Institutional)'
    Endowment = 'Endowment'
    Family_Office_Multi = 'Family Office (Multi)'
    Family_Office_Single = 'Family Office (Single)'
    Foundation = 'Foundation'
    Fund_of_Funds = 'Fund of Funds'
    Insurance_Company = 'Insurance Company'
    Outsourced_CIO = 'Outsourced CIO'
    Pension_Private = 'Pension (Private)'
    Pension_Public = 'Pension (Public)'
    Platform = 'Platform'
    Private_Bank = 'Private Bank'
    Prop_Capital_OVER_Commercial_Bank = 'Prop Capital/Commercial Bank'
    Registered_Investment_Advisor = 'Registered Investment Advisor'
    Sovereign_Wealth_Fund = 'Sovereign Wealth Fund'    


class Commodities(EnumBase, Enum):    
    
    """Commodity asset"""

    Aluminium = 'Aluminium'
    Aluminium_Alloy = 'Aluminium Alloy'
    Chicago_Ethanol = 'Chicago Ethanol'
    Coal = 'Coal'
    Coffee = 'Coffee'
    Copper = 'Copper'
    Corn = 'Corn'
    Cotton = 'Cotton'
    Crude_Palm_Oil = 'Crude Palm Oil'
    Diesel_Fuel = 'Diesel Fuel'
    Electricity = 'Electricity'
    Emissions = 'Emissions'
    Ethylene = 'Ethylene'
    Freight = 'Freight'
    Fuel_Oil = 'Fuel Oil'
    Gas_Oil = 'Gas Oil'
    Gasoline = 'Gasoline'
    Gold = 'Gold'
    Heating_Oil = 'Heating Oil'
    Iron_Ore = 'Iron Ore'
    Jet_Fuel = 'Jet Fuel'
    Lead = 'Lead'
    Lean_Hogs = 'Lean Hogs'
    NGL = 'NGL'
    Naphtha = 'Naphtha'
    Natural_Gas = 'Natural Gas'
    Nickel = 'Nickel'
    Oil = 'Oil'
    Palladium = 'Palladium'
    Platinum = 'Platinum'
    Polypropylene = 'Polypropylene'
    Primary_Aluminium = 'Primary Aluminium'
    Silver = 'Silver'
    Soybean_Meal = 'Soybean Meal'
    Soybean_Oil = 'Soybean Oil'
    Soybeans = 'Soybeans'
    Sugar = 'Sugar'
    Tin = 'Tin'
    Ultra_Low_Sulphur_Diesel = 'Ultra Low Sulphur Diesel'
    Wheat = 'Wheat'
    White_Sugar = 'White Sugar'
    Zinc = 'Zinc'    


class CommodityFamily(EnumBase, Enum):    
    
    """Commodity Family"""

    Base_Metal = 'Base Metal'
    Gas = 'Gas'
    Oil = 'Oil'
    Oil_Products = 'Oil Products'    


class CommoditySubFamily(EnumBase, Enum):    
    
    """Commodity SubFamily"""

    Crude = 'Crude'
    Fuel = 'Fuel'
    Heat = 'Heat'
    NG = 'NG'    


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class AssetMetadata(Base):
    version_timestamp: Optional[datetime.datetime] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Benchmark(Base):
    asset_id: Optional[str] = None
    value: Optional[float] = None
    name: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CommodityEUNaturalGasHub(Base):
    region: Optional[str] = None
    hub_type: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CommodityNaturalGasHub(Base):
    region: Optional[str] = None
    pipelines: Optional[Tuple[str, ...]] = None
    platts_codes: Optional[Tuple[str, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CommodityPowerAggregatedNodes(Base):
    ISO: Optional[str] = None
    aggregate_type: Optional[str] = None
    location_name: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CommodityPowerNode(Base):
    ISO: Optional[str] = None
    location_name: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CommodityReferencePriceParameters(Base):
    commodity_base: Optional[str] = None
    commodity_details: Optional[str] = None
    currency: Optional[str] = None
    unit: Optional[str] = None
    exchange_id: Optional[str] = None
    publication: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FutureContract(Base):
    future_market_marquee_id: Optional[str] = None
    contract: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FutureMarket(Base):
    exchange: Optional[str] = None
    period_frequency: Optional[str] = None
    product_group: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class NumberRange(Base):
    lower_bound: Optional[float] = None
    upper_bound: Optional[float] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class People(Base):
    portfolio_managers: Optional[Tuple[str, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class WeatherIndexParameters(Base):
    data_provider: Optional[str] = None
    weather_station: Optional[str] = None
    reference_level_amount: Optional[float] = None
    reference_level_unit: Optional[str] = None
    weather_station_fallback: Optional[str] = None
    weather_station_second_fallback: Optional[str] = None
    alternative_data_provider: Optional[str] = None
    synoptic_data_fallback: Optional[str] = None
    adjustment_to_fallback_weather_station: Optional[str] = None
    primary_disruption_fallbacks: Optional[str] = None
    secondary_disruption_fallbacks: Optional[str] = None
    final_edited_data: Optional[bool] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class AssetStats(Base):
    last_updated_time: Optional[datetime.datetime] = None
    period: Optional[AssetStatsPeriod] = None
    type_: Optional[AssetStatsType] = field(default=None, metadata=config(field_name='type'))
    stats: Optional[PerformanceStats] = None
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CommodConfigParameters(Base):
    infra: str = None
    field_history: Tuple[DictBase, ...] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CreditBasketParameters(Base):
    index_calculation_type: Optional[IndexCalculationType] = None
    currency: Optional[Currency] = None
    initial_pricing_date: Optional[datetime.date] = None
    index_notes: Optional[str] = None
    on_behalf_of: Optional[str] = None
    valuation_source: Optional[BasketValuationSource] = None
    quote_time: Optional[str] = None
    official_side: Optional[Side] = None
    quoting_type: Optional[QuoteType] = None
    weighting_type: Optional[WeightingType] = None
    close_time: Optional[datetime.datetime] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class HedgeFundParameters(Base):
    aum: Optional[float] = None
    strategy_aum: Optional[float] = None
    aum_range: Optional[NumberRange] = None
    strategy_aum_range: Optional[NumberRange] = None
    disclaimers: Optional[str] = None
    market_cap_category: Optional[Tuple[str, ...]] = None
    marketing_status: Optional[str] = None
    preferences: Optional[DictBase] = None
    regional_focus: Optional[Tuple[str, ...]] = None
    risk_taking_model: Optional[str] = None
    strategy: Optional[Strategy] = None
    strategy_description: Optional[str] = None
    targeted_gross_exposure: Optional[NumberRange] = None
    targeted_net_exposure: Optional[NumberRange] = None
    targeted_num_of_positions_short: Optional[NumberRange] = None
    targeted_num_of_positions_long: Optional[NumberRange] = None
    turnover: Optional[str] = None
    vehicle_type: Optional[str] = None
    last_returns_date: Optional[datetime.date] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecuritiesLendingLoan(Base):
    asset_id: str = None
    fund_id: str = None
    lender_id: str = None
    borrower_id: str = None
    loan_status: Optional[str] = None
    settlement_status: Optional[str] = None
    collateral_type: Optional[str] = None
    loan_currency: Optional[Currency] = None
    adjustment_ind: Optional[bool] = None
    country_of_issue: Optional[str] = None
    input_date: Optional[datetime.date] = None
    effective_date: Optional[datetime.date] = None
    security_settle_date: Optional[datetime.date] = None
    cash_settle_date: Optional[datetime.date] = None
    term_date: Optional[datetime.date] = None
    return_date: Optional[datetime.date] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ShareClassParameters(Base):
    active_liquidity_fee: Optional[float] = None
    additional_provisions: Optional[str] = None
    benchmark: Optional[Benchmark] = None
    class_fees: Optional[float] = None
    class_type: Optional[str] = None
    early_redemption_fee: Optional[float] = None
    expense_ratio_gross: Optional[float] = None
    expense_ratio_net: Optional[float] = None
    share_class_type: Optional[str] = None
    gate: Optional[float] = None
    gate_type: Optional[str] = None
    hurdle: Optional[float] = None
    hurdle_type: Optional[str] = None
    investment_manager: Optional[str] = None
    investment_type: Optional[str] = None
    institutional_share_class: Optional[bool] = None
    lockup: Optional[float] = None
    lockup_type: Optional[str] = None
    management_fee: Optional[float] = None
    minimum_subscription: Optional[float] = None
    name: Optional[str] = None
    number_of_shares: Optional[float] = None
    performance_fee: Optional[float] = None
    redemption_notice_period: Optional[float] = None
    redemption_period: Optional[str] = None
    share_class_currency: Optional[str] = None
    side_pocket: Optional[str] = None
    status: Optional[str] = None
    sub_category: Optional[str] = None
    term_type: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class TemporalPeople(Base):
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None
    people: Optional[People] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class TemporalXRef(Base):
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None
    identifiers: Optional[XRef] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class AssetGetRequestPathSchema(Base):
    limit: Optional[Tuple[str, ...]] = None
    offset: Optional[Tuple[str, ...]] = None
    scroll: Optional[Tuple[str, ...]] = None
    scroll_id: Optional[Tuple[str, ...]] = None
    as_of_time: Optional[Tuple[datetime.datetime, ...]] = None
    field_: Optional[Tuple[str, ...]] = field(default=None, metadata=config(field_name='field'))
    fields: Optional[Tuple[str, ...]] = None
    order_by: Optional[Tuple[Union[DictBase, str], ...]] = None
    sectors: Optional[Tuple[str, ...]] = None
    ticker: Optional[Tuple[str, ...]] = None
    valoren: Optional[Tuple[str, ...]] = None
    asset_parameters_payer_currency: Optional[Tuple[str, ...]] = None
    styles: Optional[Tuple[Tuple[str, ...], ...]] = None
    short_name: Optional[Tuple[str, ...]] = None
    currency: Optional[Tuple[str, ...]] = None
    rating_moodys: Optional[Tuple[str, ...]] = None
    identifier: Optional[Tuple[str, ...]] = None
    rcic: Optional[Tuple[str, ...]] = None
    name_raw: Optional[Tuple[str, ...]] = None
    asset_parameters_receiver_currency: Optional[Tuple[str, ...]] = None
    primary_country_ric: Optional[Tuple[str, ...]] = None
    strike_price: Optional[Tuple[str, ...]] = None
    listed: Optional[Tuple[str, ...]] = None
    tags: Optional[Tuple[str, ...]] = None
    delisted: Optional[Tuple[str, ...]] = None
    asset_parameters_floating_rate_option: Optional[Tuple[str, ...]] = None
    pair_calculation: Optional[Tuple[str, ...]] = None
    mic: Optional[Tuple[str, ...]] = None
    rating_fitch: Optional[Tuple[str, ...]] = None
    cusip: Optional[Tuple[str, ...]] = None
    is_legacy_pair_basket: Optional[Tuple[str, ...]] = None
    last_updated_by_id: Optional[Tuple[str, ...]] = None
    expiration_date: Optional[Tuple[datetime.date, ...]] = None
    asset_parameters_index: Optional[Tuple[str, ...]] = None
    display_id: Optional[Tuple[str, ...]] = None
    isin: Optional[Tuple[str, ...]] = None
    asset_parameters_strike_type: Optional[Tuple[str, ...]] = None
    created_by_id: Optional[Tuple[str, ...]] = None
    asset_parameters_cap_floor: Optional[Tuple[str, ...]] = None
    last_updated_since: Optional[Tuple[datetime.datetime, ...]] = None
    option_type: Optional[Tuple[str, ...]] = None
    exchange: Optional[Tuple[str, ...]] = None
    asset_class: Optional[Tuple[str, ...]] = None
    ric: Optional[Tuple[str, ...]] = None
    trading_restriction: Optional[Tuple[str, ...]] = None
    bbid: Optional[Tuple[str, ...]] = None
    underlying_asset_ids: Optional[Tuple[str, ...]] = None
    bbid_equivalent: Optional[Tuple[str, ...]] = None
    asset_parameters_index1_tenor: Optional[Tuple[str, ...]] = None
    owner_id: Optional[Tuple[str, ...]] = None
    asset_classifications_is_primary: Optional[Tuple[str, ...]] = None
    tsdb_shortname: Optional[Tuple[str, ...]] = None
    name: Optional[Tuple[str, ...]] = None
    live_date: Optional[Tuple[DictBase, ...]] = None
    prime_id: Optional[Tuple[str, ...]] = None
    description: Optional[Tuple[str, ...]] = None
    asset_classifications_is_country_primary: Optional[Tuple[str, ...]] = None
    sedol: Optional[Tuple[str, ...]] = None
    default_backcast: Optional[Tuple[str, ...]] = None
    wpk: Optional[Tuple[str, ...]] = None
    id_: Optional[Tuple[str, ...]] = field(default=None, metadata=config(field_name='id'))
    bcid: Optional[Tuple[str, ...]] = None
    settlement_date: Optional[Tuple[datetime.date, ...]] = None
    rating_second_highest: Optional[Tuple[str, ...]] = None
    region: Optional[Tuple[str, ...]] = None
    asset_parameters_payer_spread: Optional[Tuple[str, ...]] = None
    rating_linear: Optional[Tuple[str, ...]] = None
    type_: Optional[Tuple[DictBase, ...]] = field(default=None, metadata=config(field_name='type'))
    asset_parameters_index2_tenor: Optional[Tuple[str, ...]] = None
    rating_standard_and_poors: Optional[Tuple[str, ...]] = None
    asset_parameters_fee_currency: Optional[Tuple[str, ...]] = None
    asset_parameters_receiver_spread: Optional[Tuple[str, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Asset(Base):
    asset_class: AssetClass = None
    type_: AssetType = field(default=None, metadata=config(field_name='type'))
    name: str = None
    active: Optional[bool] = None
    classifications: Optional[AssetClassifications] = None
    created_by_id: Optional[str] = None
    created_time: Optional[datetime.datetime] = None
    currency: Optional[Currency] = None
    default_quantity: Optional[float] = None
    description: Optional[str] = None
    economic_terms_hash: Optional[str] = None
    entitlements: Optional[Entitlements] = None
    entitlement_exclusions: Optional[EntitlementExclusions] = None
    exchange: Optional[str] = None
    id_: Optional[str] = field(default=None, metadata=config(field_name='id'))
    identifiers: Optional[Tuple[Identifier, ...]] = None
    last_updated_by_id: Optional[str] = None
    last_updated_time: Optional[datetime.datetime] = None
    listed: Optional[bool] = None
    live_date: Optional[datetime.date] = None
    key: Optional[str] = None
    key_map: Optional[DictBase] = None
    owner_id: Optional[str] = None
    parameters: Optional[DictBase] = None
    asset_stats: Optional[Tuple[AssetStats, ...]] = None
    people: Optional[People] = None
    people_history: Optional[Tuple[TemporalPeople, ...]] = None
    rank: Optional[float] = None
    region: Optional[Region] = None
    report_ids: Optional[Tuple[str, ...]] = None
    sectors: Optional[Tuple[str, ...]] = None
    short_name: Optional[str] = None
    styles: Optional[Tuple[str, ...]] = None
    tags: Optional[Tuple[str, ...]] = None
    underliers: Optional[Tuple[str, ...]] = None
    underlying_asset_ids: Optional[Tuple[str, ...]] = None
    xrefs: Optional[Tuple[TemporalXRef, ...]] = None
    xref: Optional[XRef] = None
    metadata: Optional[AssetMetadata] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class AssetToInstrumentResponse(Base):
    asset_id: str = None
    name: str = None
    instrument: InstrumentBase = None
    size_field: Optional[str] = None
