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


class SecMasterAssetType(EnumBase, Enum):    
    
    """Asset type differentiates the product categorization or contract type."""

    ETF = 'ETF'
    ETN = 'ETN'
    Future = 'Future'
    Index = 'Index'
    Option = 'Option'
    Preferred_Stock = 'Preferred Stock'
    Single_Stock = 'Single Stock'
    Common_Stock = 'Common Stock'
    ADR = 'ADR'
    GDR = 'GDR'
    Dutch_Cert = 'Dutch Cert'
    NY_Reg_Shrs = 'NY Reg Shrs'
    Receipt = 'Receipt'
    Unit = 'Unit'
    Mutual_Fund = 'Mutual Fund'
    Right = 'Right'
    Preferred = 'Preferred'
    Misc_ = 'Misc.'
    REIT = 'REIT'
    Private_Comp = 'Private Comp'
    Preference = 'Preference'
    Ltd_Part = 'Ltd Part'
    Tracking_Stk = 'Tracking Stk'
    Royalty_Trst = 'Royalty Trst'
    Closed_End_Fund = 'Closed-End Fund'
    Open_End_Fund = 'Open-End Fund'
    Fund_of_Funds = 'Fund of Funds'
    MLP = 'MLP'
    Stapled_Security = 'Stapled Security'
    Savings_Share = 'Savings Share'
    Equity_WRT = 'Equity WRT'
    Savings_Plan = 'Savings Plan'
    Equity_Index = 'Equity Index'
    Municipal_Bond = 'Municipal Bond'
    Corporate_Bond = 'Corporate Bond'
    Government_Bond = 'Government Bond'
    Agency_Bond = 'Agency Bond'
    Currency = 'Currency'
    Equity_Option = 'Equity Option'
    Financial_index_future_ = 'Financial index future.'
    Single_Stock_Future = 'Single Stock Future'
    Pool = 'Pool'
    Certificate_Of_Deposit = 'Certificate Of Deposit'
    Debt_Structured_Note = 'Debt Structured Note'
    Agency_CMO = 'Agency CMO'
    Future_Option = 'Future Option'
    Convertible_Bond = 'Convertible Bond'
    Austrian_Crt = 'Austrian Crt'
    BDR = 'BDR'
    Belgium_Cert = 'Belgium Cert'
    CDR = 'CDR'
    EDR = 'EDR'
    German_Cert = 'German Cert'
    IDR = 'IDR'
    RDC = 'RDC'
    Swiss_Cert = 'Swiss Cert'
    Canadian_DR = 'Canadian DR'
    Singapore_DR = 'Singapore DR'
    To_Be_Announced = 'To Be Announced'
    Basket = 'Basket'    


class SecMasterCorporateActionStatus(EnumBase, Enum):    
    
    """Status of corporate actions."""

    Normal = 'Normal'
    Completed = 'Completed'
    Pending = 'Pending'
    Deleted = 'Deleted'
    Incomplete = 'Incomplete'
    Missing_Adj_Factor = 'Missing Adj Factor'
    Not_Quoted_By_Exchange = 'Not Quoted By Exchange'
    Missing_Terms = 'Missing Terms'
    Cancelled = 'Cancelled'
    Lapsed = 'Lapsed'
    Proposed = 'Proposed'
    Withdrawn = 'Withdrawn'
    All = 'All'    


class SecMasterCorporateActionType(EnumBase, Enum):    
    
    """Types of corporate actions."""

    Cash_Dividend = 'Cash Dividend'
    Merger = 'Merger'
    Spinoff = 'Spinoff'
    Split = 'Split'
    Rights = 'Rights'
    Reorganization = 'Reorganization'
    Special_Adjustment = 'Special Adjustment'
    Quote_Lot_Adjustment = 'Quote Lot Adjustment'
    Currency_Adjustment = 'Currency Adjustment'
    All = 'All'    


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecMasterAuditFields(Base):
    last_updated_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    last_updated_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    created_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    created_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    owner_id: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


class SecMasterIdentifiers(DictBase):
    pass


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecMasterRecord(Base):
    recordid: Optional[float] = field(default=None, metadata=field_metadata)
    action_type: Optional[str] = field(default=None, metadata=field_metadata)
    instrument_value: Optional[float] = field(default=None, metadata=field_metadata)
    data_value: Optional[float] = field(default=None, metadata=field_metadata)
    term_type: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecMasterResourceCompany(Base):
    company_id: Optional[float] = field(default=None, metadata=field_metadata)
    company_name: Optional[str] = field(default=None, metadata=field_metadata)
    identifiers: Optional[DictBase] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=field_metadata)
    issuer_id: Optional[str] = field(default=None, metadata=field_metadata)


SecMasterSources = Dict[str, str]


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecMasterTemporalCompany(Base):
    gs_company_id: str = field(default=None, metadata=field_metadata)
    id_: Optional[str] = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    start_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    end_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ExchangeGetRequestPathSchema(Base):
    gs_exchange_id: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    mic: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    operating_mic: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    ric_suffix_code: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    ric_exchange_code: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    bbg_exchange_code: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    country: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    fields: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    as_of_date: Optional[Tuple[datetime.date, ...]] = field(default=None, metadata=field_metadata)
    limit: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    offset: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    offset_key: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecMasterAssetSources(Base):
    id_: Optional[str] = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    asset_class: Optional[str] = field(default=None, metadata=field_metadata)
    product: Optional[SecMasterSources] = field(default=None, metadata=field_metadata)
    exchange: Optional[SecMasterSources] = field(default=None, metadata=field_metadata)
    company: Optional[SecMasterSources] = field(default=None, metadata=field_metadata)
    classifications: Optional[SecMasterSources] = field(default=None, metadata=field_metadata)
    identifiers: Optional[SecMasterSources] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecMasterCorporateAction(Base):
    actionid: Optional[str] = field(default=None, metadata=field_metadata)
    eventid: Optional[str] = field(default=None, metadata=field_metadata)
    gsid: Optional[str] = field(default=None, metadata=field_metadata)
    event_type: Optional[SecMasterCorporateActionType] = field(default=None, metadata=field_metadata)
    announce_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    effective_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    multiplicative_adjust: Optional[float] = field(default=None, metadata=field_metadata)
    additive_adjust: Optional[float] = field(default=None, metadata=field_metadata)
    event_status: Optional[SecMasterCorporateActionStatus] = field(default=None, metadata=field_metadata)
    records: Optional[Tuple[SecMasterRecord, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecMasterExchange(Base):
    gs_exchange_id: str = field(default=None, metadata=field_metadata)
    id_: Optional[str] = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    name: Optional[str] = field(default=None, metadata=field_metadata)
    country: Optional[str] = field(default=None, metadata=field_metadata)
    timezone: Optional[str] = field(default=None, metadata=field_metadata)
    type_: Optional[str] = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    identifiers: Optional[SecMasterIdentifiers] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecMasterGetActionsRequestPathSchema(Base):
    event_type: Optional[Tuple[SecMasterCorporateActionType, ...]] = field(default=None, metadata=field_metadata)
    event_status: Optional[Tuple[SecMasterCorporateActionStatus, ...]] = field(default=None, metadata=field_metadata)
    gsid: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    event_id: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    corp_action_id: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    effective_date: Optional[Tuple[datetime.date, ...]] = field(default=None, metadata=field_metadata)
    as_of_time: Optional[Tuple[datetime.datetime, ...]] = field(default=None, metadata=field_metadata)
    effective_date_from: Optional[Tuple[datetime.date, ...]] = field(default=None, metadata=field_metadata)
    effective_date_to: Optional[Tuple[datetime.date, ...]] = field(default=None, metadata=field_metadata)
    offset_key: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    limit: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecMasterGetCapitalStructureRequestPathSchema(Base):
    gsid: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    ticker: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    bbid: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    ric: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    rcic: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    cusip: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    sedol: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    isin: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    gss: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    prime_id: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    issuer_id: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    type_: Optional[Tuple[str, ...]] = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    as_of_time: Optional[Tuple[datetime.datetime, ...]] = field(default=None, metadata=field_metadata)
    is_primary: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    effective_date: Optional[Tuple[datetime.date, ...]] = field(default=None, metadata=field_metadata)
    limit: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    offset_key: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecMasterGetRequestPathSchema(Base):
    identifier: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    gsid: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    ticker: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    bbg: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    bbid: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    ric: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    rcic: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    cusip: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    cins: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    sedol: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    isin: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    gss: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    prime_id: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    type_: Optional[Tuple[SecMasterAssetType, ...]] = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    country_code: Optional[Tuple[CountryCode, ...]] = field(default=None, metadata=field_metadata)
    is_primary: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    all_listings: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    effective_date: Optional[Tuple[datetime.date, ...]] = field(default=None, metadata=field_metadata)
    as_of_time: Optional[Tuple[datetime.datetime, ...]] = field(default=None, metadata=field_metadata)
    limit: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    offset_key: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecMasterResourceExchange(Base):
    name: Optional[str] = field(default=None, metadata=field_metadata)
    identifiers: Optional[SecMasterIdentifiers] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecMasterResourceProduct(Base):
    name: Optional[str] = field(default=None, metadata=field_metadata)
    identifiers: Optional[SecMasterIdentifiers] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecMasterTemporalProduct(Base):
    gsid: str = field(default=None, metadata=field_metadata)
    id_: Optional[str] = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    start_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    end_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=field_metadata)
    country: Optional[str] = field(default=None, metadata=field_metadata)
    primary_exchange_id: Optional[str] = field(default=None, metadata=field_metadata)
    type_: Optional[SecMasterAssetType] = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    subtype: Optional[str] = field(default=None, metadata=field_metadata)
    source: Optional[str] = field(default=None, metadata=field_metadata)
    flag: Optional[bool] = field(default=None, metadata=field_metadata)
    update_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecMasterAsset(Base):
    id_: str = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    effective_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    start_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=field_metadata)
    asset_class: Optional[AssetClass] = field(default=None, metadata=field_metadata)
    type_: Optional[SecMasterAssetType] = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    product: Optional[SecMasterResourceProduct] = field(default=None, metadata=field_metadata)
    exchange: Optional[SecMasterResourceExchange] = field(default=None, metadata=field_metadata)
    currency: Optional[str] = field(default=None, metadata=field_metadata)
    company: Optional[SecMasterResourceCompany] = field(default=None, metadata=field_metadata)
    issuer: Optional[SecMasterResourceCompany] = field(default=None, metadata=field_metadata)
    classifications: Optional[AssetClassifications] = field(default=None, metadata=field_metadata)
    identifiers: Optional[SecMasterIdentifiers] = field(default=None, metadata=field_metadata)
    tags: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    active_listing: Optional[bool] = field(default=None, metadata=field_metadata)
    last_active_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    entitlements: Optional[Entitlements] = field(default=None, metadata=field_metadata)
    entitlement_exclusions: Optional[EntitlementExclusions] = field(default=None, metadata=field_metadata)
    audit_fields: Optional[SecMasterAuditFields] = field(default=None, metadata=field_metadata)
    field_sources: Optional[SecMasterAssetSources] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecMasterResponseActions(Base):
    results: Optional[Tuple[SecMasterCorporateAction, ...]] = field(default=None, metadata=field_metadata)
    total_results: Optional[float] = field(default=None, metadata=field_metadata)
    offset_key: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecMasterResponseMulti(Base):
    request_id: Optional[str] = field(default=None, metadata=field_metadata)
    results: Optional[Tuple[Union[SecMasterExchange, SecMasterTemporalCompany, SecMasterTemporalProduct], ...]] = field(default=None, metadata=field_metadata)
    total_results: Optional[float] = field(default=None, metadata=field_metadata)
    offset_key: Optional[str] = field(default=None, metadata=field_metadata)
    limit: Optional[int] = field(default=None, metadata=field_metadata)
    offset: Optional[int] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecMasterResponseAssets(Base):
    results: Optional[Tuple[SecMasterAsset, ...]] = field(default=None, metadata=field_metadata)
    total_results: Optional[float] = field(default=None, metadata=field_metadata)
    offset_key: Optional[str] = field(default=None, metadata=field_metadata)
    limit: Optional[int] = field(default=None, metadata=field_metadata)
    offset: Optional[int] = field(default=None, metadata=field_metadata)
    update_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)
