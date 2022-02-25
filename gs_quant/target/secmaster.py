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


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecMasterAuditFields(Base):
    last_updated_time: Optional[datetime.datetime] = None
    last_updated_by_id: Optional[str] = None
    created_time: Optional[datetime.datetime] = None
    created_by_id: Optional[str] = None
    owner_id: Optional[str] = None


SecMasterIdentifiers = Dict[str, str]


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecMasterResourceCompany(Base):
    company_id: Optional[float] = None
    company_name: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecMasterTemporalCompany(SecMasterResponseMulti):
    gs_company_id: str = None
    id_: Optional[str] = field(default=None, metadata=config(field_name='id'))
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None
    name: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ExchangeGetRequestPathSchema(Base):
    gs_exchange_id: Optional[Tuple[str, ...]] = None
    mic: Optional[Tuple[str, ...]] = None
    operating_mic: Optional[Tuple[str, ...]] = None
    ric_suffix_code: Optional[Tuple[str, ...]] = None
    ric_exchange_code: Optional[Tuple[str, ...]] = None
    bbg_exchange_code: Optional[Tuple[str, ...]] = None
    name: Optional[Tuple[str, ...]] = None
    country: Optional[Tuple[str, ...]] = None
    fields: Optional[Tuple[str, ...]] = None
    as_of_date: Optional[Tuple[datetime.date, ...]] = None
    limit: Optional[Tuple[str, ...]] = None
    offset: Optional[Tuple[str, ...]] = None
    offset_key: Optional[Tuple[str, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecMasterExchange(SecMasterResponseMulti):
    gs_exchange_id: str = None
    id_: Optional[str] = field(default=None, metadata=config(field_name='id'))
    name: Optional[str] = None
    country: Optional[str] = None
    timezone: Optional[str] = None
    type_: Optional[str] = field(default=None, metadata=config(field_name='type'))
    identifiers: Optional[SecMasterIdentifiers] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecMasterGetRequestPathSchema(Base):
    gsid: Optional[Tuple[str, ...]] = None
    ticker: Optional[Tuple[str, ...]] = None
    bbid: Optional[Tuple[str, ...]] = None
    ric: Optional[Tuple[str, ...]] = None
    rcic: Optional[Tuple[str, ...]] = None
    cusip: Optional[Tuple[str, ...]] = None
    sedol: Optional[Tuple[str, ...]] = None
    isin: Optional[Tuple[str, ...]] = None
    gss: Optional[Tuple[str, ...]] = None
    prime_id: Optional[Tuple[str, ...]] = None
    type_: Optional[Tuple[str, ...]] = field(default=None, metadata=config(field_name='type'))
    exchange: Optional[Tuple[str, ...]] = None
    fields: Optional[Tuple[str, ...]] = None
    as_of_date: Optional[Tuple[datetime.date, ...]] = None
    limit: Optional[Tuple[str, ...]] = None
    offset: Optional[Tuple[str, ...]] = None
    offset_key: Optional[Tuple[str, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecMasterResourceExchange(Base):
    name: Optional[str] = None
    identifiers: Optional[SecMasterIdentifiers] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecMasterResourceProduct(Base):
    name: Optional[str] = None
    identifiers: Optional[SecMasterIdentifiers] = None


SecMasterSources = Dict[str, SecMasterSourceNames]


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecMasterTemporalProduct(SecMasterResponseMulti):
    gsid: str = None
    id_: Optional[str] = field(default=None, metadata=config(field_name='id'))
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None
    name: Optional[str] = None
    country: Optional[str] = None
    primary_exchange_id: Optional[str] = None
    type_: Optional[SecMasterAssetType] = field(default=None, metadata=config(field_name='type'))
    subtype: Optional[str] = None
    source: Optional[SecMasterSourceNames] = None
    flag: Optional[bool] = None
    update_time: Optional[datetime.datetime] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecMasterAssetSources(Base):
    id_: Optional[SecMasterSourceNames] = field(default=None, metadata=config(field_name='id'))
    asset_class: Optional[SecMasterSourceNames] = None
    product: Optional[SecMasterSources] = None
    exchange: Optional[SecMasterSources] = None
    company: Optional[SecMasterSources] = None
    classifications: Optional[SecMasterSources] = None
    identifiers: Optional[SecMasterSources] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecMasterResponseMulti(Base):
    request_id: Optional[str] = None
    results: Optional[Tuple[SecMasterResponseMulti, ...]] = None
    total_results: Optional[float] = None
    offset_key: Optional[str] = None
    limit: Optional[int] = None
    offset: Optional[int] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecMasterAsset(Base):
    id_: str = field(default=None, metadata=config(field_name='id'))
    asset_class: Optional[AssetClass] = None
    type_: Optional[SecMasterAssetType] = field(default=None, metadata=config(field_name='type'))
    product: Optional[SecMasterResourceProduct] = None
    exchange: Optional[SecMasterResourceExchange] = None
    company: Optional[SecMasterResourceCompany] = None
    classifications: Optional[AssetClassifications] = None
    identifiers: Optional[SecMasterIdentifiers] = None
    tags: Optional[Tuple[str, ...]] = None
    entitlements: Optional[Entitlements] = None
    entitlement_exclusions: Optional[EntitlementExclusions] = None
    audit_fields: Optional[SecMasterAuditFields] = None
    field_sources: Optional[SecMasterAssetSources] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SecMasterResponseAssets(Base):
    results: Optional[Tuple[SecMasterAsset, ...]] = None
    total_results: Optional[float] = None
    offset_key: Optional[str] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
