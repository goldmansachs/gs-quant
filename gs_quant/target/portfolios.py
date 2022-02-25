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


class RiskAumSource(EnumBase, Enum):    
    
    """Source of AUM for portfolio risk calculations."""

    Gross = 'Gross'
    Long = 'Long'
    Short = 'Short'
    Custom_AUM = 'Custom AUM'
    Net = 'Net'    


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecDbBookDetail(Base):
    book_id: Optional[str] = None
    book_type: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class GRDBPortfolioParameters(Base):
    oe_id: str = None
    client_name: str = None
    increment: str = None
    risk_packages: Tuple[str, ...] = None
    enabled: str = None
    is_live: str = None
    client_account_names: Optional[Tuple[str, ...]] = None
    oasis_account_names: Optional[Tuple[str, ...]] = field(default=None, metadata=config(field_name='OasisAccountNames'))
    client_position_filter: Optional[ClientPositionFilter] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PCOTrade(Base):
    fill_rate: Optional[str] = None
    include_in_hedge: Optional[bool] = None
    settlement_date: Optional[datetime.date] = None
    spot_ref: Optional[str] = None
    notes: Optional[str] = None
    creation_date: Optional[datetime.date] = None
    base_currency: Optional[Currency] = None
    quote_currency: Optional[Currency] = None
    base_currency_notional: Optional[str] = None
    quote_currency_notional: Optional[str] = None
    trade_date: Optional[datetime.date] = None
    fixing_ref: Optional[str] = None
    side: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PCOPortfolioParameters(Base):
    base_currency: Optional[Currency] = None
    local_currency: Optional[Currency] = None
    fund_calendar: Optional[str] = None
    calculation_currency: Optional[PCOCurrencyType] = None
    hedge_settlement_interval: Optional[Tuple[PCOParameterValues, ...]] = None
    hedge_settlement_day: Optional[Tuple[PCOParameterValues, ...]] = None
    roll_horizon: Optional[Tuple[PCOParameterValues, ...]] = None
    pnl_currency: Optional[Tuple[PCOParameterValues, ...]] = None
    nav_publication_period: Optional[Tuple[PCOParameterValues, ...]] = None
    roll_date_zero_threshold: Optional[bool] = None
    unrealised_mark_to_market: Optional[PCOUnrealisedMarkToMarket] = None
    target_deviation: Optional[Tuple[PCOTargetDeviation, ...]] = None
    cash_balances: Optional[Tuple[PCOCashBalance, ...]] = None
    exposure: Optional[PCOExposure] = None
    pco_share_class: Optional[PCOShareClass] = None
    settlements: Optional[Tuple[PCOSettlements, ...]] = None
    show_cash: Optional[bool] = None
    show_exposure: Optional[bool] = None
    enable_rfq: Optional[bool] = field(default=None, metadata=config(field_name='enableRFQ'))
    fixing_descriptions: Optional[Tuple[str, ...]] = None
    pco_origin: Optional[PCOOrigin] = None
    version: Optional[str] = None
    trades: Optional[Tuple[PCOTrade, ...]] = None
    investment_ratio: Optional[str] = None
    roll_currency: Optional[Tuple[PCOParameterValues, ...]] = None
    param_version: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Portfolio(Base):
    currency: Currency = None
    name: str = None
    id_: Optional[str] = field(default=None, metadata=config(field_name='id'))
    created_by_id: Optional[str] = None
    created_time: Optional[datetime.datetime] = None
    description: Optional[str] = None
    entitlements: Optional[Entitlements] = None
    entitlement_exclusions: Optional[EntitlementExclusions] = None
    identifiers: Optional[Tuple[Identifier, ...]] = None
    last_updated_by_id: Optional[str] = None
    last_updated_time: Optional[datetime.datetime] = None
    owner_id: Optional[str] = None
    report_ids: Optional[Tuple[str, ...]] = None
    short_name: Optional[str] = None
    underlying_portfolio_ids: Optional[Tuple[str, ...]] = None
    tags: Optional[Tuple[str, ...]] = None
    type_: Optional[PortfolioType] = field(default=None, metadata=config(field_name='type'))
    parameters: Optional[DictBase] = None
    aum_source: Optional[RiskAumSource] = None
