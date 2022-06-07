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


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class AssetMetadata(Base):
    version_timestamp: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Benchmark(Base):
    asset_id: Optional[str] = field(default=None, metadata=field_metadata)
    value: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CommodityEUNaturalGasHub(Base):
    region: Optional[str] = field(default=None, metadata=field_metadata)
    hub_type: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CommodityNaturalGasHub(Base):
    region: Optional[str] = field(default=None, metadata=field_metadata)
    pipelines: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    platts_codes: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CommodityPowerAggregatedNodes(Base):
    ISO: Optional[str] = field(default=None, metadata=field_metadata)
    aggregate_type: Optional[str] = field(default=None, metadata=field_metadata)
    location_name: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CommodityPowerNode(Base):
    ISO: Optional[str] = field(default=None, metadata=field_metadata)
    location_name: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CommodityReferencePriceParameters(Base):
    commodity_base: Optional[str] = field(default=None, metadata=field_metadata)
    commodity_details: Optional[str] = field(default=None, metadata=field_metadata)
    currency: Optional[str] = field(default=None, metadata=field_metadata)
    unit: Optional[str] = field(default=None, metadata=field_metadata)
    exchange_id: Optional[str] = field(default=None, metadata=field_metadata)
    publication: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FutureContract(Base):
    future_market_marquee_id: Optional[str] = field(default=None, metadata=field_metadata)
    contract: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FutureMarket(Base):
    exchange: Optional[str] = field(default=None, metadata=field_metadata)
    period_frequency: Optional[str] = field(default=None, metadata=field_metadata)
    product_group: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class NumberRange(Base):
    lower_bound: Optional[float] = field(default=None, metadata=field_metadata)
    upper_bound: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class People(Base):
    portfolio_managers: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class WeatherIndexParameters(Base):
    data_provider: Optional[str] = field(default=None, metadata=field_metadata)
    weather_station: Optional[str] = field(default=None, metadata=field_metadata)
    reference_level_amount: Optional[float] = field(default=None, metadata=field_metadata)
    reference_level_unit: Optional[str] = field(default=None, metadata=field_metadata)
    weather_station_fallback: Optional[str] = field(default=None, metadata=field_metadata)
    weather_station_second_fallback: Optional[str] = field(default=None, metadata=field_metadata)
    alternative_data_provider: Optional[str] = field(default=None, metadata=field_metadata)
    synoptic_data_fallback: Optional[str] = field(default=None, metadata=field_metadata)
    adjustment_to_fallback_weather_station: Optional[str] = field(default=None, metadata=field_metadata)
    primary_disruption_fallbacks: Optional[str] = field(default=None, metadata=field_metadata)
    secondary_disruption_fallbacks: Optional[str] = field(default=None, metadata=field_metadata)
    final_edited_data: Optional[bool] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class AssetStats(Base):
    last_updated_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    period: Optional[AssetStatsPeriod] = field(default=None, metadata=field_metadata)
    type_: Optional[AssetStatsType] = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    stats: Optional[PerformanceStats] = field(default=None, metadata=field_metadata)
    start_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    end_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CommodConfigParameters(Base):
    infra: str = field(default=None, metadata=field_metadata)
    field_history: Tuple[DictBase, ...] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CreditBasketParameters(Base):
    index_calculation_type: Optional[IndexCalculationType] = field(default=None, metadata=field_metadata)
    currency: Optional[Currency] = field(default=None, metadata=field_metadata)
    initial_pricing_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    index_notes: Optional[str] = field(default=None, metadata=field_metadata)
    on_behalf_of: Optional[str] = field(default=None, metadata=field_metadata)
    valuation_source: Optional[BasketValuationSource] = field(default=None, metadata=field_metadata)
    quote_time: Optional[str] = field(default=None, metadata=field_metadata)
    official_side: Optional[Side] = field(default=None, metadata=field_metadata)
    quoting_type: Optional[QuoteType] = field(default=None, metadata=field_metadata)
    weighting_type: Optional[WeightingType] = field(default=None, metadata=field_metadata)
    close_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    clone_parent_id: Optional[str] = field(default=None, metadata=field_metadata)
    hedge_id: Optional[str] = field(default=None, metadata=field_metadata)
    portfolio_id: Optional[str] = field(default=None, metadata=field_metadata)
    index_approval_ids: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class HedgeFundParameters(Base):
    aum: Optional[float] = field(default=None, metadata=field_metadata)
    strategy_aum: Optional[float] = field(default=None, metadata=field_metadata)
    aum_range: Optional[NumberRange] = field(default=None, metadata=field_metadata)
    strategy_aum_range: Optional[NumberRange] = field(default=None, metadata=field_metadata)
    disclaimers: Optional[str] = field(default=None, metadata=field_metadata)
    market_cap_category: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    marketing_status: Optional[str] = field(default=None, metadata=field_metadata)
    preferences: Optional[DictBase] = field(default=None, metadata=field_metadata)
    regional_focus: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    risk_taking_model: Optional[str] = field(default=None, metadata=field_metadata)
    strategy: Optional[Strategy] = field(default=None, metadata=field_metadata)
    strategy_description: Optional[str] = field(default=None, metadata=field_metadata)
    targeted_gross_exposure: Optional[NumberRange] = field(default=None, metadata=field_metadata)
    targeted_net_exposure: Optional[NumberRange] = field(default=None, metadata=field_metadata)
    targeted_num_of_positions_short: Optional[NumberRange] = field(default=None, metadata=field_metadata)
    targeted_num_of_positions_long: Optional[NumberRange] = field(default=None, metadata=field_metadata)
    turnover: Optional[str] = field(default=None, metadata=field_metadata)
    vehicle_type: Optional[str] = field(default=None, metadata=field_metadata)
    last_returns_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecuritiesLendingLoan(Base):
    asset_id: str = field(default=None, metadata=field_metadata)
    fund_id: str = field(default=None, metadata=field_metadata)
    lender_id: str = field(default=None, metadata=field_metadata)
    borrower_id: str = field(default=None, metadata=field_metadata)
    loan_status: Optional[str] = field(default=None, metadata=field_metadata)
    settlement_status: Optional[str] = field(default=None, metadata=field_metadata)
    collateral_type: Optional[str] = field(default=None, metadata=field_metadata)
    loan_currency: Optional[Currency] = field(default=None, metadata=field_metadata)
    adjustment_ind: Optional[bool] = field(default=None, metadata=field_metadata)
    country_of_issue: Optional[str] = field(default=None, metadata=field_metadata)
    input_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    effective_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    security_settle_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    cash_settle_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    term_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    return_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ShareClassParameters(Base):
    active_liquidity_fee: Optional[float] = field(default=None, metadata=field_metadata)
    additional_provisions: Optional[str] = field(default=None, metadata=field_metadata)
    benchmark: Optional[Benchmark] = field(default=None, metadata=field_metadata)
    class_fees: Optional[float] = field(default=None, metadata=field_metadata)
    class_type: Optional[str] = field(default=None, metadata=field_metadata)
    early_redemption_fee: Optional[float] = field(default=None, metadata=field_metadata)
    expense_ratio_gross: Optional[float] = field(default=None, metadata=field_metadata)
    expense_ratio_net: Optional[float] = field(default=None, metadata=field_metadata)
    share_class_type: Optional[str] = field(default=None, metadata=field_metadata)
    gate: Optional[float] = field(default=None, metadata=field_metadata)
    gate_type: Optional[str] = field(default=None, metadata=field_metadata)
    hurdle: Optional[float] = field(default=None, metadata=field_metadata)
    hurdle_type: Optional[str] = field(default=None, metadata=field_metadata)
    investment_manager: Optional[str] = field(default=None, metadata=field_metadata)
    investment_type: Optional[str] = field(default=None, metadata=field_metadata)
    institutional_share_class: Optional[bool] = field(default=None, metadata=field_metadata)
    lockup: Optional[float] = field(default=None, metadata=field_metadata)
    lockup_type: Optional[str] = field(default=None, metadata=field_metadata)
    management_fee: Optional[float] = field(default=None, metadata=field_metadata)
    minimum_subscription: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=field_metadata)
    number_of_shares: Optional[float] = field(default=None, metadata=field_metadata)
    performance_fee: Optional[float] = field(default=None, metadata=field_metadata)
    redemption_notice_period: Optional[float] = field(default=None, metadata=field_metadata)
    redemption_period: Optional[str] = field(default=None, metadata=field_metadata)
    share_class_currency: Optional[str] = field(default=None, metadata=field_metadata)
    side_pocket: Optional[str] = field(default=None, metadata=field_metadata)
    status: Optional[str] = field(default=None, metadata=field_metadata)
    sub_category: Optional[str] = field(default=None, metadata=field_metadata)
    term_type: Optional[str] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class TemporalPeople(Base):
    start_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    end_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    people: Optional[People] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class TemporalXRef(Base):
    start_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    end_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    identifiers: Optional[XRef] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class AssetGetRequestPathSchema(Base):
    limit: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    offset: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    scroll: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    scroll_id: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    as_of_time: Optional[Tuple[datetime.datetime, ...]] = field(default=None, metadata=field_metadata)
    field_: Optional[Tuple[str, ...]] = field(default=None, metadata=config(field_name='field', exclude=exclude_none))
    fields: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    order_by: Optional[Tuple[Union[DictBase, str], ...]] = field(default=None, metadata=field_metadata)
    next_rebalance_date: Optional[Tuple[datetime.date, ...]] = field(default=None, metadata=field_metadata)
    sectors: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    ticker: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    valoren: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    asset_parameters_payer_currency: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    styles: Optional[Tuple[Tuple[str, ...], ...]] = field(default=None, metadata=field_metadata)
    short_name: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    currency: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    rating_moodys: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    identifier: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    rcic: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    name_raw: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    asset_parameters_receiver_currency: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    primary_country_ric: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    strike_price: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    listed: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    tags: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    delisted: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    asset_parameters_floating_rate_option: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    pair_calculation: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    mic: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    rating_fitch: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    cusip: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    is_legacy_pair_basket: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    last_updated_by_id: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    expiration_date: Optional[Tuple[datetime.date, ...]] = field(default=None, metadata=field_metadata)
    asset_parameters_index: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    display_id: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    isin: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    asset_parameters_strike_type: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    created_by_id: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    asset_parameters_cap_floor: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    last_updated_since: Optional[Tuple[datetime.datetime, ...]] = field(default=None, metadata=field_metadata)
    option_type: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    exchange: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    coin_metrics_id: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    asset_class: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    ric: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    trading_restriction: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    bbid: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    underlying_asset_ids: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    bbid_equivalent: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    asset_parameters_index1_tenor: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    owner_id: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    asset_classifications_is_primary: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    tsdb_shortname: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    live_date: Optional[Tuple[DictBase, ...]] = field(default=None, metadata=field_metadata)
    prime_id: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    description: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    asset_classifications_is_country_primary: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    sedol: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    default_backcast: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    wpk: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    id_: Optional[Tuple[str, ...]] = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    bcid: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    settlement_date: Optional[Tuple[datetime.date, ...]] = field(default=None, metadata=field_metadata)
    last_rebalance_date: Optional[Tuple[datetime.date, ...]] = field(default=None, metadata=field_metadata)
    rating_second_highest: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    region: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    asset_parameters_payer_spread: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    rating_linear: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    type_: Optional[Tuple[DictBase, ...]] = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    asset_parameters_index2_tenor: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    rating_standard_and_poors: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    asset_parameters_fee_currency: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    asset_parameters_receiver_spread: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Asset(Base):
    asset_class: AssetClass = field(default=None, metadata=field_metadata)
    type_: AssetType = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    name: str = field(default=None, metadata=field_metadata)
    active: Optional[bool] = field(default=None, metadata=field_metadata)
    classifications: Optional[AssetClassifications] = field(default=None, metadata=field_metadata)
    created_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    created_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    currency: Optional[Currency] = field(default=None, metadata=field_metadata)
    default_quantity: Optional[float] = field(default=None, metadata=field_metadata)
    description: Optional[str] = field(default=None, metadata=field_metadata)
    economic_terms_hash: Optional[str] = field(default=None, metadata=field_metadata)
    entitlements: Optional[Entitlements] = field(default=None, metadata=field_metadata)
    entitlement_exclusions: Optional[EntitlementExclusions] = field(default=None, metadata=field_metadata)
    exchange: Optional[str] = field(default=None, metadata=field_metadata)
    id_: Optional[str] = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    identifiers: Optional[Tuple[Identifier, ...]] = field(default=None, metadata=field_metadata)
    last_updated_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    last_updated_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    listed: Optional[bool] = field(default=None, metadata=field_metadata)
    live_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    key: Optional[str] = field(default=None, metadata=field_metadata)
    key_map: Optional[DictBase] = field(default=None, metadata=field_metadata)
    owner_id: Optional[str] = field(default=None, metadata=field_metadata)
    parameters: Optional[DictBase] = field(default=None, metadata=field_metadata)
    asset_stats: Optional[Tuple[AssetStats, ...]] = field(default=None, metadata=field_metadata)
    people: Optional[People] = field(default=None, metadata=field_metadata)
    people_history: Optional[Tuple[TemporalPeople, ...]] = field(default=None, metadata=field_metadata)
    rank: Optional[float] = field(default=None, metadata=field_metadata)
    region: Optional[Region] = field(default=None, metadata=field_metadata)
    report_ids: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    sectors: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    short_name: Optional[str] = field(default=None, metadata=field_metadata)
    styles: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    tags: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    underliers: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    underlying_asset_ids: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    xrefs: Optional[Tuple[TemporalXRef, ...]] = field(default=None, metadata=field_metadata)
    xref: Optional[XRef] = field(default=None, metadata=field_metadata)
    metadata: Optional[AssetMetadata] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class AssetToInstrumentResponse(Base):
    asset_id: str = field(default=None, metadata=field_metadata)
    name: str = field(default=None, metadata=field_metadata)
    instrument: InstrumentBase = field(default=None, metadata=field_metadata)
    size_field: Optional[str] = field(default=None, metadata=field_metadata)
