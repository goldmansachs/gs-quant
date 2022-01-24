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

from gs_quant.common import *
import datetime
from typing import Mapping, Tuple, Union, Optional
from enum import Enum
from gs_quant.base import Base, EnumBase, InstrumentBase, camel_case_translate, get_enum_value


class SecMasterAssetType(EnumBase, Enum):    
    
    """Asset type differentiates the product categorization or contract type."""

    ETF = 'ETF'
    ETN = 'ETN'
    Future = 'Future'
    Index = 'Index'
    Option = 'Option'
    Preferred_Stock = 'Preferred Stock'
    Single_Stock = 'Single Stock'    


class SecMasterSourceNames(EnumBase, Enum):    
    
    """Data source."""

    Barra = 'Barra'
    Refinitiv = 'Refinitiv'
    Bloomberg = 'Bloomberg'
    Goldman_Sachs = 'Goldman Sachs'    


class SecMasterAuditFields(Base):
        
    """Audit fields for security."""

    @camel_case_translate
    def __init__(
        self,
        last_updated_time: datetime.datetime = None,
        last_updated_by_id: str = None,
        created_time: datetime.datetime = None,
        created_by_id: str = None,
        owner_id: str = None,
        name: str = None
    ):        
        super().__init__()
        self.last_updated_time = last_updated_time
        self.last_updated_by_id = last_updated_by_id
        self.created_time = created_time
        self.created_by_id = created_by_id
        self.owner_id = owner_id
        self.name = name

    @property
    def last_updated_time(self) -> datetime.datetime:
        """Timestamp of when the object was last updated."""
        return self.__last_updated_time

    @last_updated_time.setter
    def last_updated_time(self, value: datetime.datetime):
        self._property_changed('last_updated_time')
        self.__last_updated_time = value        

    @property
    def last_updated_by_id(self) -> str:
        """Unique identifier of user who last updated the object."""
        return self.__last_updated_by_id

    @last_updated_by_id.setter
    def last_updated_by_id(self, value: str):
        self._property_changed('last_updated_by_id')
        self.__last_updated_by_id = value        

    @property
    def created_time(self) -> datetime.datetime:
        """Time created. ISO 8601 formatted string."""
        return self.__created_time

    @created_time.setter
    def created_time(self, value: datetime.datetime):
        self._property_changed('created_time')
        self.__created_time = value        

    @property
    def created_by_id(self) -> str:
        """Unique identifier of user who created the object."""
        return self.__created_by_id

    @created_by_id.setter
    def created_by_id(self, value: str):
        self._property_changed('created_by_id')
        self.__created_by_id = value        

    @property
    def owner_id(self) -> str:
        """Marquee unique identifier for user who owns the object."""
        return self.__owner_id

    @owner_id.setter
    def owner_id(self, value: str):
        self._property_changed('owner_id')
        self.__owner_id = value        


class SecMasterIdentifiers(Base):
        
    """Map of identifiers."""

    @camel_case_translate
    def __init__(
        self,
        name: str = None
    ):        
        super().__init__()
        self.name = name


class SecMasterResourceCompany(Base):
        
    """Company properties."""

    @camel_case_translate
    def __init__(
        self,
        company_id: float = None,
        company_name: str = None,
        name: str = None
    ):        
        super().__init__()
        self.company_id = company_id
        self.company_name = company_name
        self.name = name

    @property
    def company_id(self) -> float:
        """Numeric id of company."""
        return self.__company_id

    @company_id.setter
    def company_id(self, value: float):
        self._property_changed('company_id')
        self.__company_id = value        

    @property
    def company_name(self) -> str:
        """Name of company."""
        return self.__company_name

    @company_name.setter
    def company_name(self, value: str):
        self._property_changed('company_name')
        self.__company_name = value        


class SecMasterTemporalCompany(Base):
        
    """Company properties"""

    @camel_case_translate
    def __init__(
        self,
        gs_company_id: str,
        id_: str = None,
        start_date: datetime.date = None,
        end_date: datetime.date = None,
        name: str = None
    ):        
        super().__init__()
        self.__id = id_
        self.gs_company_id = gs_company_id
        self.start_date = start_date
        self.end_date = end_date
        self.name = name

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def gs_company_id(self) -> str:
        """Marquee unique identifier"""
        return self.__gs_company_id

    @gs_company_id.setter
    def gs_company_id(self, value: str):
        self._property_changed('gs_company_id')
        self.__gs_company_id = value        

    @property
    def start_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__start_date

    @start_date.setter
    def start_date(self, value: datetime.date):
        self._property_changed('start_date')
        self.__start_date = value        

    @property
    def end_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__end_date

    @end_date.setter
    def end_date(self, value: datetime.date):
        self._property_changed('end_date')
        self.__end_date = value        

    @property
    def name(self) -> str:
        """Name of company."""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        


class SecMasterExchange(Base):
        
    """An exchange from Security Master"""

    @camel_case_translate
    def __init__(
        self,
        gs_exchange_id: str,
        id_: str = None,
        name: str = None,
        country: str = None,
        timezone: str = None,
        type_: str = None,
        identifiers: SecMasterIdentifiers = None
    ):        
        super().__init__()
        self.__id = id_
        self.gs_exchange_id = gs_exchange_id
        self.name = name
        self.country = country
        self.timezone = timezone
        self.__type = type_
        self.identifiers = identifiers

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def gs_exchange_id(self) -> str:
        """Marquee unique identifier"""
        return self.__gs_exchange_id

    @gs_exchange_id.setter
    def gs_exchange_id(self, value: str):
        self._property_changed('gs_exchange_id')
        self.__gs_exchange_id = value        

    @property
    def name(self) -> str:
        """Name of exchange."""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def country(self) -> str:
        """Country of exchange."""
        return self.__country

    @country.setter
    def country(self, value: str):
        self._property_changed('country')
        self.__country = value        

    @property
    def timezone(self) -> str:
        """Timezone of exchange."""
        return self.__timezone

    @timezone.setter
    def timezone(self, value: str):
        self._property_changed('timezone')
        self.__timezone = value        

    @property
    def type(self) -> str:
        """Type of exchange."""
        return self.__type

    @type.setter
    def type(self, value: str):
        self._property_changed('type')
        self.__type = value        

    @property
    def identifiers(self) -> SecMasterIdentifiers:
        """Map of identifiers."""
        return self.__identifiers

    @identifiers.setter
    def identifiers(self, value: SecMasterIdentifiers):
        self._property_changed('identifiers')
        self.__identifiers = value        


class SecMasterResourceExchange(Base):
        
    """Exchange properties."""

    @camel_case_translate
    def __init__(
        self,
        name: str = None,
        identifiers: SecMasterIdentifiers = None
    ):        
        super().__init__()
        self.name = name
        self.identifiers = identifiers

    @property
    def name(self) -> str:
        """Name for exchange."""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def identifiers(self) -> SecMasterIdentifiers:
        """Exchange identifiers."""
        return self.__identifiers

    @identifiers.setter
    def identifiers(self, value: SecMasterIdentifiers):
        self._property_changed('identifiers')
        self.__identifiers = value        


class SecMasterResourceProduct(Base):
        
    """Product properties."""

    @camel_case_translate
    def __init__(
        self,
        name: str = None,
        identifiers: SecMasterIdentifiers = None
    ):        
        super().__init__()
        self.name = name
        self.identifiers = identifiers

    @property
    def name(self) -> str:
        """Product name."""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def identifiers(self) -> SecMasterIdentifiers:
        """Product identifiers."""
        return self.__identifiers

    @identifiers.setter
    def identifiers(self, value: SecMasterIdentifiers):
        self._property_changed('identifiers')
        self.__identifiers = value        


class SecMasterSources(Base):
        
    """Map from fields to their sources."""

    @camel_case_translate
    def __init__(
        self,
        name: str = None
    ):        
        super().__init__()
        self.name = name


class SecMasterTemporalProduct(Base):
        
    """Product properties"""

    @camel_case_translate
    def __init__(
        self,
        gsid: str,
        id_: str = None,
        start_date: datetime.date = None,
        end_date: datetime.date = None,
        name: str = None,
        country: str = None,
        primary_exchange_id: str = None,
        type_: Union[SecMasterAssetType, str] = None,
        subtype: str = None,
        source: Union[SecMasterSourceNames, str] = None,
        flag: bool = None,
        update_time: datetime.datetime = None
    ):        
        super().__init__()
        self.__id = id_
        self.gsid = gsid
        self.start_date = start_date
        self.end_date = end_date
        self.name = name
        self.country = country
        self.primary_exchange_id = primary_exchange_id
        self.__type = get_enum_value(SecMasterAssetType, type_)
        self.subtype = subtype
        self.source = source
        self.flag = flag
        self.update_time = update_time

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def gsid(self) -> str:
        """Marquee unique identifier"""
        return self.__gsid

    @gsid.setter
    def gsid(self, value: str):
        self._property_changed('gsid')
        self.__gsid = value        

    @property
    def start_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__start_date

    @start_date.setter
    def start_date(self, value: datetime.date):
        self._property_changed('start_date')
        self.__start_date = value        

    @property
    def end_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__end_date

    @end_date.setter
    def end_date(self, value: datetime.date):
        self._property_changed('end_date')
        self.__end_date = value        

    @property
    def name(self) -> str:
        """Name of company."""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def country(self) -> str:
        """Country name of asset."""
        return self.__country

    @country.setter
    def country(self, value: str):
        self._property_changed('country')
        self.__country = value        

    @property
    def primary_exchange_id(self) -> str:
        """Marquee unique identifier"""
        return self.__primary_exchange_id

    @primary_exchange_id.setter
    def primary_exchange_id(self, value: str):
        self._property_changed('primary_exchange_id')
        self.__primary_exchange_id = value        

    @property
    def type(self) -> Union[SecMasterAssetType, str]:
        """Asset type differentiates the product categorization or contract type."""
        return self.__type

    @type.setter
    def type(self, value: Union[SecMasterAssetType, str]):
        self._property_changed('type')
        self.__type = get_enum_value(SecMasterAssetType, value)        

    @property
    def subtype(self) -> str:
        """Subtype of product."""
        return self.__subtype

    @subtype.setter
    def subtype(self, value: str):
        self._property_changed('subtype')
        self.__subtype = value        

    @property
    def source(self) -> Union[SecMasterSourceNames, str]:
        """Data source."""
        return self.__source

    @source.setter
    def source(self, value: Union[SecMasterSourceNames, str]):
        self._property_changed('source')
        self.__source = get_enum_value(SecMasterSourceNames, value)        

    @property
    def flag(self) -> bool:
        """Whether this product is flagged."""
        return self.__flag

    @flag.setter
    def flag(self, value: bool):
        self._property_changed('flag')
        self.__flag = value        

    @property
    def update_time(self) -> datetime.datetime:
        """Timestamp of when the object was last updated."""
        return self.__update_time

    @update_time.setter
    def update_time(self, value: datetime.datetime):
        self._property_changed('update_time')
        self.__update_time = value        


class SecMasterAssetSources(Base):
        
    """Source for each field (when known)."""

    @camel_case_translate
    def __init__(
        self,
        id_: Union[SecMasterSourceNames, str] = None,
        asset_class: Union[SecMasterSourceNames, str] = None,
        product: SecMasterSources = None,
        exchange: SecMasterSources = None,
        company: SecMasterSources = None,
        classifications: SecMasterSources = None,
        identifiers: SecMasterSources = None,
        name: str = None
    ):        
        super().__init__()
        self.__id = get_enum_value(SecMasterSourceNames, id_)
        self.asset_class = asset_class
        self.product = product
        self.exchange = exchange
        self.company = company
        self.classifications = classifications
        self.identifiers = identifiers
        self.name = name

    @property
    def id(self) -> Union[SecMasterSourceNames, str]:
        """Data source."""
        return self.__id

    @id.setter
    def id(self, value: Union[SecMasterSourceNames, str]):
        self._property_changed('id')
        self.__id = get_enum_value(SecMasterSourceNames, value)        

    @property
    def asset_class(self) -> Union[SecMasterSourceNames, str]:
        """Data source."""
        return self.__asset_class

    @asset_class.setter
    def asset_class(self, value: Union[SecMasterSourceNames, str]):
        self._property_changed('asset_class')
        self.__asset_class = get_enum_value(SecMasterSourceNames, value)        

    @property
    def product(self) -> SecMasterSources:
        """Map from fields to their sources."""
        return self.__product

    @product.setter
    def product(self, value: SecMasterSources):
        self._property_changed('product')
        self.__product = value        

    @property
    def exchange(self) -> SecMasterSources:
        """Map from fields to their sources."""
        return self.__exchange

    @exchange.setter
    def exchange(self, value: SecMasterSources):
        self._property_changed('exchange')
        self.__exchange = value        

    @property
    def company(self) -> SecMasterSources:
        """Map from fields to their sources."""
        return self.__company

    @company.setter
    def company(self, value: SecMasterSources):
        self._property_changed('company')
        self.__company = value        

    @property
    def classifications(self) -> SecMasterSources:
        """Map from fields to their sources."""
        return self.__classifications

    @classifications.setter
    def classifications(self, value: SecMasterSources):
        self._property_changed('classifications')
        self.__classifications = value        

    @property
    def identifiers(self) -> SecMasterSources:
        """Map from fields to their sources."""
        return self.__identifiers

    @identifiers.setter
    def identifiers(self, value: SecMasterSources):
        self._property_changed('identifiers')
        self.__identifiers = value        


class SecMasterResponseMulti(Base):
        
    @camel_case_translate
    def __init__(
        self,
        request_id: str = None,
        results: Tuple[dict, ...] = None,
        total_results: float = None,
        offset_key: str = None,
        limit: int = None,
        offset: int = None,
        name: str = None
    ):        
        super().__init__()
        self.request_id = request_id
        self.results = results
        self.total_results = total_results
        self.offset_key = offset_key
        self.limit = limit
        self.offset = offset
        self.name = name

    @property
    def request_id(self) -> str:
        """Marquee unique identifier"""
        return self.__request_id

    @request_id.setter
    def request_id(self, value: str):
        self._property_changed('request_id')
        self.__request_id = value        

    @property
    def results(self) -> Tuple[dict, ...]:
        """Array of results."""
        return self.__results

    @results.setter
    def results(self, value: Tuple[dict, ...]):
        self._property_changed('results')
        self.__results = value        

    @property
    def total_results(self) -> float:
        """Total number of results."""
        return self.__total_results

    @total_results.setter
    def total_results(self, value: float):
        self._property_changed('total_results')
        self.__total_results = value        

    @property
    def offset_key(self) -> str:
        """Offset key to get next page of results."""
        return self.__offset_key

    @offset_key.setter
    def offset_key(self, value: str):
        self._property_changed('offset_key')
        self.__offset_key = value        

    @property
    def limit(self) -> int:
        """Limit on number of results returned in this batch."""
        return self.__limit

    @limit.setter
    def limit(self, value: int):
        self._property_changed('limit')
        self.__limit = value        

    @property
    def offset(self) -> int:
        """Offset of the first result returned in this batch."""
        return self.__offset

    @offset.setter
    def offset(self, value: int):
        self._property_changed('offset')
        self.__offset = value        


class SecMasterAsset(Base):
        
    """A Security Master asset"""

    @camel_case_translate
    def __init__(
        self,
        id_: str,
        asset_class: Union[AssetClass, str] = None,
        type_: Union[SecMasterAssetType, str] = None,
        product: SecMasterResourceProduct = None,
        exchange: SecMasterResourceExchange = None,
        company: SecMasterResourceCompany = None,
        classifications: AssetClassifications = None,
        identifiers: SecMasterIdentifiers = None,
        tags: Tuple[str, ...] = None,
        entitlements: Entitlements = None,
        entitlement_exclusions: EntitlementExclusions = None,
        audit_fields: SecMasterAuditFields = None,
        field_sources: SecMasterAssetSources = None,
        name: str = None
    ):        
        super().__init__()
        self.__id = id_
        self.asset_class = asset_class
        self.__type = get_enum_value(SecMasterAssetType, type_)
        self.product = product
        self.exchange = exchange
        self.company = company
        self.classifications = classifications
        self.identifiers = identifiers
        self.tags = tags
        self.entitlements = entitlements
        self.entitlement_exclusions = entitlement_exclusions
        self.audit_fields = audit_fields
        self.field_sources = field_sources
        self.name = name

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def asset_class(self) -> Union[AssetClass, str]:
        """Asset classification of security. Assets are classified into broad groups which
           exhibit similar characteristics and behave in a consistent way under
           different market conditions"""
        return self.__asset_class

    @asset_class.setter
    def asset_class(self, value: Union[AssetClass, str]):
        self._property_changed('asset_class')
        self.__asset_class = get_enum_value(AssetClass, value)        

    @property
    def type(self) -> Union[SecMasterAssetType, str]:
        """Asset type differentiates the product categorization or contract type."""
        return self.__type

    @type.setter
    def type(self, value: Union[SecMasterAssetType, str]):
        self._property_changed('type')
        self.__type = get_enum_value(SecMasterAssetType, value)        

    @property
    def product(self) -> SecMasterResourceProduct:
        """Product properties."""
        return self.__product

    @product.setter
    def product(self, value: SecMasterResourceProduct):
        self._property_changed('product')
        self.__product = value        

    @property
    def exchange(self) -> SecMasterResourceExchange:
        """Exchange properties."""
        return self.__exchange

    @exchange.setter
    def exchange(self, value: SecMasterResourceExchange):
        self._property_changed('exchange')
        self.__exchange = value        

    @property
    def company(self) -> SecMasterResourceCompany:
        """Company properties."""
        return self.__company

    @company.setter
    def company(self, value: SecMasterResourceCompany):
        self._property_changed('company')
        self.__company = value        

    @property
    def classifications(self) -> AssetClassifications:
        """Classification for security."""
        return self.__classifications

    @classifications.setter
    def classifications(self, value: AssetClassifications):
        self._property_changed('classifications')
        self.__classifications = value        

    @property
    def identifiers(self) -> SecMasterIdentifiers:
        """Map of identifiers."""
        return self.__identifiers

    @identifiers.setter
    def identifiers(self, value: SecMasterIdentifiers):
        self._property_changed('identifiers')
        self.__identifiers = value        

    @property
    def tags(self) -> Tuple[str, ...]:
        """Metadata associated with the object. Provide an array of strings which will be
           indexed for search and locating related objects"""
        return self.__tags

    @tags.setter
    def tags(self, value: Tuple[str, ...]):
        self._property_changed('tags')
        self.__tags = value        

    @property
    def entitlements(self) -> Entitlements:
        """Defines the entitlements of a given resource."""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self._property_changed('entitlements')
        self.__entitlements = value        

    @property
    def entitlement_exclusions(self) -> EntitlementExclusions:
        """Defines the exclusion entitlements of a given resource."""
        return self.__entitlement_exclusions

    @entitlement_exclusions.setter
    def entitlement_exclusions(self, value: EntitlementExclusions):
        self._property_changed('entitlement_exclusions')
        self.__entitlement_exclusions = value        

    @property
    def audit_fields(self) -> SecMasterAuditFields:
        """Audit fields for security."""
        return self.__audit_fields

    @audit_fields.setter
    def audit_fields(self, value: SecMasterAuditFields):
        self._property_changed('audit_fields')
        self.__audit_fields = value        

    @property
    def field_sources(self) -> SecMasterAssetSources:
        """Source for each field (when known)."""
        return self.__field_sources

    @field_sources.setter
    def field_sources(self, value: SecMasterAssetSources):
        self._property_changed('field_sources')
        self.__field_sources = value        


class SecMasterResponseAssets(Base):
        
    @camel_case_translate
    def __init__(
        self,
        results: Tuple[SecMasterAsset, ...] = None,
        total_results: float = None,
        offset_key: str = None,
        limit: int = None,
        offset: int = None,
        name: str = None
    ):        
        super().__init__()
        self.results = results
        self.total_results = total_results
        self.offset_key = offset_key
        self.limit = limit
        self.offset = offset
        self.name = name

    @property
    def results(self) -> Tuple[SecMasterAsset, ...]:
        """Array of assets."""
        return self.__results

    @results.setter
    def results(self, value: Tuple[SecMasterAsset, ...]):
        self._property_changed('results')
        self.__results = value        

    @property
    def total_results(self) -> float:
        """Total number of results."""
        return self.__total_results

    @total_results.setter
    def total_results(self, value: float):
        self._property_changed('total_results')
        self.__total_results = value        

    @property
    def offset_key(self) -> str:
        """Offset key to get next page of results."""
        return self.__offset_key

    @offset_key.setter
    def offset_key(self, value: str):
        self._property_changed('offset_key')
        self.__offset_key = value        

    @property
    def limit(self) -> int:
        """Limit on number of results returned in this batch."""
        return self.__limit

    @limit.setter
    def limit(self, value: int):
        self._property_changed('limit')
        self.__limit = value        

    @property
    def offset(self) -> int:
        """Offset of the first result returned in this batch."""
        return self.__offset

    @offset.setter
    def offset(self, value: int):
        self._property_changed('offset')
        self.__offset = value        
