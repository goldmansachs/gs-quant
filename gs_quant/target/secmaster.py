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
    Municipal_Bonds = 'Municipal Bonds'
    Municipal_Bond = 'Municipal Bond'
    Corporate_Bond = 'Corporate Bond'
    Government_Bond = 'Government Bond'
    Agency_Bond = 'Agency Bond'
    Currency = 'Currency'    


class SecMasterSourceNames(EnumBase, Enum):    
    
    """Data source."""

    Barra = 'Barra'
    Refinitiv = 'Refinitiv'
    Bloomberg = 'Bloomberg'
    Goldman_Sachs = 'Goldman Sachs'    


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


SecMasterIdentifiers = Dict[str, str]


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecMasterResourceCompany(Base):
    company_id: Optional[float] = field(default=None, metadata=field_metadata)
    company_name: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecMasterTemporalCompany(SecMasterResponseMulti):
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
class SecMasterExchange(SecMasterResponseMulti):
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
class SecMasterGetRequestPathSchema(Base):
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
    type_: Optional[Tuple[str, ...]] = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    exchange: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    fields: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    as_of_date: Optional[Tuple[datetime.date, ...]] = field(default=None, metadata=field_metadata)
    limit: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    offset: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
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


SecMasterSources = Dict[str, SecMasterSourceNames]


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecMasterTemporalProduct(SecMasterResponseMulti):
    gsid: str = field(default=None, metadata=field_metadata)
    id_: Optional[str] = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    start_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    end_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=field_metadata)
    country: Optional[str] = field(default=None, metadata=field_metadata)
    primary_exchange_id: Optional[str] = field(default=None, metadata=field_metadata)
    type_: Optional[SecMasterAssetType] = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    subtype: Optional[str] = field(default=None, metadata=field_metadata)
    source: Optional[SecMasterSourceNames] = field(default=None, metadata=field_metadata)
    flag: Optional[bool] = field(default=None, metadata=field_metadata)
    update_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecMasterAssetSources(Base):
    id_: Optional[SecMasterSourceNames] = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    asset_class: Optional[SecMasterSourceNames] = field(default=None, metadata=field_metadata)
    product: Optional[SecMasterSources] = field(default=None, metadata=field_metadata)
    exchange: Optional[SecMasterSources] = field(default=None, metadata=field_metadata)
    company: Optional[SecMasterSources] = field(default=None, metadata=field_metadata)
    classifications: Optional[SecMasterSources] = field(default=None, metadata=field_metadata)
    identifiers: Optional[SecMasterSources] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecMasterResponseMulti(Base):
    request_id: Optional[str] = field(default=None, metadata=field_metadata)
    results: Optional[Tuple[SecMasterResponseMulti, ...]] = field(default=None, metadata=field_metadata)
    total_results: Optional[float] = field(default=None, metadata=field_metadata)
    offset_key: Optional[str] = field(default=None, metadata=field_metadata)
    limit: Optional[int] = field(default=None, metadata=field_metadata)
    offset: Optional[int] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecMasterAsset(Base):
    id_: str = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    asset_class: Optional[AssetClass] = field(default=None, metadata=field_metadata)
    type_: Optional[SecMasterAssetType] = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    product: Optional[SecMasterResourceProduct] = field(default=None, metadata=field_metadata)
    exchange: Optional[SecMasterResourceExchange] = field(default=None, metadata=field_metadata)
    company: Optional[SecMasterResourceCompany] = field(default=None, metadata=field_metadata)
    classifications: Optional[AssetClassifications] = field(default=None, metadata=field_metadata)
    identifiers: Optional[SecMasterIdentifiers] = field(default=None, metadata=field_metadata)
    tags: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    entitlements: Optional[Entitlements] = field(default=None, metadata=field_metadata)
    entitlement_exclusions: Optional[EntitlementExclusions] = field(default=None, metadata=field_metadata)
    audit_fields: Optional[SecMasterAuditFields] = field(default=None, metadata=field_metadata)
    field_sources: Optional[SecMasterAssetSources] = field(default=None, metadata=field_metadata)
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
    name: Optional[str] = field(default=None, metadata=name_metadata)
