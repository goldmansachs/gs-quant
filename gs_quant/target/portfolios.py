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


class ActiveWeightType(EnumBase, Enum):    
    
    """Weight type used to calculate active holdings."""

    Net = 'Net'
    Gross = 'Gross'    


class ClientPositionFilter(EnumBase, Enum):    
    
    """Filter used to select client positions from GRDB. 'oeId' selects all positions
       associated with the provided oeId. 'oeIdOrClientAccounts' selects
       positions associated with their the provided oeId or ClientAccounts.
       'clientAccounts' selects positions only associated with those provided
       accounts."""

    oeId = 'oeId'
    clientAccounts = 'clientAccounts'
    oeIdOrClientAccounts = 'oeIdOrClientAccounts'    


class PortfolioType(EnumBase, Enum):    
    
    """Portfolio type differentiates the portfolio categorization"""

    Securities_Lending = 'Securities Lending'
    Draft_Portfolio = 'Draft Portfolio'
    Draft_Bond = 'Draft Bond'
    PCO_Portfolio = 'PCO Portfolio'
    PCO_Share_Class = 'PCO Share Class'    


class RefreshInterval(EnumBase, Enum):    
    
    """These intervals determine how often a portfolio is refreshed"""

    Daily = 'Daily'
    Start_Of_Week = 'Start Of Week'
    End_Of_Week = 'End Of Week'
    Start_Of_Month = 'Start Of Month'
    End_Of_Month = 'End Of Month'    


class RiskAumSource(EnumBase, Enum):    
    
    """Source of AUM for portfolio risk calculations."""

    Gross = 'Gross'
    Long = 'Long'
    Short = 'Short'
    Custom_AUM = 'Custom AUM'
    Net = 'Net'    


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecDbBookDetail(Base):
    book_id: Optional[str] = field(default=None, metadata=field_metadata)
    book_type: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CreditPreTradePortfolioParameters(Base):
    date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    currency: Optional[Currency] = field(default=None, metadata=field_metadata)
    reference_id: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class GRDBPortfolioParameters(Base):
    oe_id: str = field(default=None, metadata=field_metadata)
    client_name: str = field(default=None, metadata=field_metadata)
    increment: str = field(default=None, metadata=field_metadata)
    risk_packages: Tuple[str, ...] = field(default=None, metadata=field_metadata)
    enabled: str = field(default=None, metadata=field_metadata)
    is_live: str = field(default=None, metadata=field_metadata)
    client_account_names: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    oasis_account_names: Optional[Tuple[str, ...]] = field(default=None, metadata=config(field_name='OasisAccountNames', exclude=exclude_none))
    client_position_filter: Optional[ClientPositionFilter] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PCOTrade(Base):
    fill_rate: Optional[str] = field(default=None, metadata=field_metadata)
    include_in_hedge: Optional[bool] = field(default=None, metadata=field_metadata)
    settlement_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    spot_ref: Optional[str] = field(default=None, metadata=field_metadata)
    notes: Optional[str] = field(default=None, metadata=field_metadata)
    creation_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    base_currency: Optional[Currency] = field(default=None, metadata=field_metadata)
    quote_currency: Optional[Currency] = field(default=None, metadata=field_metadata)
    base_currency_notional: Optional[str] = field(default=None, metadata=field_metadata)
    quote_currency_notional: Optional[str] = field(default=None, metadata=field_metadata)
    trade_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    fixing_ref: Optional[str] = field(default=None, metadata=field_metadata)
    side: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class TemporalPortfolioParameters(Base):
    return_type: Optional[ReturnType] = field(default=None, metadata=field_metadata)
    refresh_interval: Optional[RefreshInterval] = field(default=None, metadata=field_metadata)
    active_weight_type: Optional[ActiveWeightType] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PCOPortfolioParameters(Base):
    base_currency: Optional[Currency] = field(default=None, metadata=field_metadata)
    local_currency: Optional[Currency] = field(default=None, metadata=field_metadata)
    fund_calendar: Optional[str] = field(default=None, metadata=field_metadata)
    calculation_currency: Optional[PCOCurrencyType] = field(default=None, metadata=field_metadata)
    hedge_settlement_interval: Optional[Tuple[PCOParameterValues, ...]] = field(default=None, metadata=field_metadata)
    hedge_settlement_day: Optional[Tuple[PCOParameterValues, ...]] = field(default=None, metadata=field_metadata)
    roll_horizon: Optional[Tuple[PCOParameterValues, ...]] = field(default=None, metadata=field_metadata)
    pnl_currency: Optional[Tuple[PCOParameterValues, ...]] = field(default=None, metadata=field_metadata)
    nav_publication_period: Optional[Tuple[PCOParameterValues, ...]] = field(default=None, metadata=field_metadata)
    roll_date_zero_threshold: Optional[bool] = field(default=None, metadata=field_metadata)
    unrealised_mark_to_market: Optional[PCOUnrealisedMarkToMarket] = field(default=None, metadata=field_metadata)
    target_deviation: Optional[Tuple[PCOTargetDeviation, ...]] = field(default=None, metadata=field_metadata)
    cash_balances: Optional[Tuple[PCOCashBalance, ...]] = field(default=None, metadata=field_metadata)
    exposure: Optional[PCOExposure] = field(default=None, metadata=field_metadata)
    pco_share_class: Optional[PCOShareClass] = field(default=None, metadata=field_metadata)
    settlements: Optional[Tuple[PCOSettlements, ...]] = field(default=None, metadata=field_metadata)
    show_cash: Optional[bool] = field(default=None, metadata=field_metadata)
    show_exposure: Optional[bool] = field(default=None, metadata=field_metadata)
    enable_rfq: Optional[bool] = field(default=None, metadata=config(field_name='enableRFQ', exclude=exclude_none))
    fixing_descriptions: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    pco_origin: Optional[PCOOrigin] = field(default=None, metadata=field_metadata)
    version: Optional[str] = field(default=None, metadata=field_metadata)
    trades: Optional[Tuple[PCOTrade, ...]] = field(default=None, metadata=field_metadata)
    investment_ratio: Optional[str] = field(default=None, metadata=field_metadata)
    roll_currency: Optional[Tuple[PCOParameterValues, ...]] = field(default=None, metadata=field_metadata)
    param_version: Optional[str] = field(default=None, metadata=field_metadata)
    security_breakdown: Optional[PCOSecurityBreakdown] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Portfolio(Base):
    currency: Currency = field(default=None, metadata=field_metadata)
    name: str = field(default=None, metadata=field_metadata)
    id_: Optional[str] = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    created_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    created_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    description: Optional[str] = field(default=None, metadata=field_metadata)
    entitlements: Optional[Entitlements] = field(default=None, metadata=field_metadata)
    entitlement_exclusions: Optional[EntitlementExclusions] = field(default=None, metadata=field_metadata)
    identifiers: Optional[Tuple[Identifier, ...]] = field(default=None, metadata=field_metadata)
    last_updated_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    last_updated_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    owner_id: Optional[str] = field(default=None, metadata=field_metadata)
    report_ids: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    scenario_ids: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    short_name: Optional[str] = field(default=None, metadata=field_metadata)
    underlying_portfolio_ids: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    tags: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    type_: Optional[PortfolioType] = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    parameters: Optional[DictBase] = field(default=None, metadata=field_metadata)
    aum_source: Optional[RiskAumSource] = field(default=None, metadata=field_metadata)
    tag_name_hierarchy: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
