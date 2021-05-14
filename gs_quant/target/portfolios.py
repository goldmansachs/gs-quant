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


class SecDbBookDetail(Base):
        
    """Details about SecDb Book"""

    @camel_case_translate
    def __init__(
        self,
        book_id: str = None,
        book_type: str = None,
        name: str = None
    ):        
        super().__init__()
        self.book_id = book_id
        self.book_type = book_type
        self.name = name

    @property
    def book_id(self) -> str:
        """Book Id"""
        return self.__book_id

    @book_id.setter
    def book_id(self, value: str):
        self._property_changed('book_id')
        self.__book_id = value        

    @property
    def book_type(self) -> str:
        return self.__book_type

    @book_type.setter
    def book_type(self, value: str):
        self._property_changed('book_type')
        self.__book_type = value        


class GRDBPortfolioParameters(Base):
        
    """Parameters required for a GRDB portfolio."""

    _name_mappings = {'oasis_account_names': 'OasisAccountNames'}

    @camel_case_translate
    def __init__(
        self,
        oe_id: str,
        client_name: str,
        increment: str,
        risk_packages: Tuple[str, ...],
        enabled: str,
        is_live: str,
        client_account_names: Tuple[str, ...] = None,
        oasis_account_names: Tuple[str, ...] = None,
        client_position_filter: Union[ClientPositionFilter, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.oe_id = oe_id
        self.client_name = client_name
        self.client_account_names = client_account_names
        self.oasis_account_names = oasis_account_names
        self.client_position_filter = client_position_filter
        self.increment = increment
        self.risk_packages = risk_packages
        self.enabled = enabled
        self.is_live = is_live
        self.name = name

    @property
    def oe_id(self) -> str:
        """Marquee unique identifier"""
        return self.__oe_id

    @oe_id.setter
    def oe_id(self, value: str):
        self._property_changed('oe_id')
        self.__oe_id = value        

    @property
    def client_name(self) -> str:
        """Client's name or user-friendly identifier"""
        return self.__client_name

    @client_name.setter
    def client_name(self, value: str):
        self._property_changed('client_name')
        self.__client_name = value        

    @property
    def client_account_names(self) -> Tuple[str, ...]:
        """List of SecDB Customer Book Names"""
        return self.__client_account_names

    @client_account_names.setter
    def client_account_names(self, value: Tuple[str, ...]):
        self._property_changed('client_account_names')
        self.__client_account_names = value        

    @property
    def oasis_account_names(self) -> Tuple[str, ...]:
        """List of OASIS Accounts"""
        return self.__oasis_account_names

    @oasis_account_names.setter
    def oasis_account_names(self, value: Tuple[str, ...]):
        self._property_changed('oasis_account_names')
        self.__oasis_account_names = value        

    @property
    def client_position_filter(self) -> Union[ClientPositionFilter, str]:
        """Filter used to select client positions from GRDB. 'oeId' selects all positions
           associated with the provided oeId. 'oeIdOrClientAccounts' selects
           positions associated with their the provided oeId or ClientAccounts.
           'clientAccounts' selects positions only associated with those
           provided accounts."""
        return self.__client_position_filter

    @client_position_filter.setter
    def client_position_filter(self, value: Union[ClientPositionFilter, str]):
        self._property_changed('client_position_filter')
        self.__client_position_filter = get_enum_value(ClientPositionFilter, value)        

    @property
    def increment(self) -> str:
        """Generated Unique three character string"""
        return self.__increment

    @increment.setter
    def increment(self, value: str):
        self._property_changed('increment')
        self.__increment = value        

    @property
    def risk_packages(self) -> Tuple[str, ...]:
        """Metadata associated with the object. Provide an array of strings which will be
           indexed for search and locating related objects"""
        return self.__risk_packages

    @risk_packages.setter
    def risk_packages(self, value: Tuple[str, ...]):
        self._property_changed('risk_packages')
        self.__risk_packages = value        

    @property
    def enabled(self) -> str:
        """Gives information on whether risks are run for the portfolio"""
        return self.__enabled

    @enabled.setter
    def enabled(self, value: str):
        self._property_changed('enabled')
        self.__enabled = value        

    @property
    def is_live(self) -> str:
        """Gives information on whether alerts are enabled for the portfolio"""
        return self.__is_live

    @is_live.setter
    def is_live(self, value: str):
        self._property_changed('is_live')
        self.__is_live = value        


class Portfolio(Base):
        
    @camel_case_translate
    def __init__(
        self,
        currency: Union[Currency, str],
        name: str,
        created_by_id: str = None,
        created_time: datetime.datetime = None,
        description: str = None,
        entitlements: Entitlements = None,
        entitlement_exclusions: EntitlementExclusions = None,
        id_: str = None,
        identifiers: Tuple[Identifier, ...] = None,
        last_updated_by_id: str = None,
        last_updated_time: datetime.datetime = None,
        owner_id: str = None,
        report_ids: Tuple[str, ...] = None,
        short_name: str = None,
        underlying_portfolio_ids: Tuple[str, ...] = None,
        tags: Tuple[str, ...] = None,
        type_: Union[PortfolioType, str] = None,
        parameters: dict = None
    ):        
        super().__init__()
        self.created_by_id = created_by_id
        self.created_time = created_time
        self.currency = currency
        self.description = description
        self.entitlements = entitlements
        self.entitlement_exclusions = entitlement_exclusions
        self.__id = id_
        self.identifiers = identifiers
        self.last_updated_by_id = last_updated_by_id
        self.last_updated_time = last_updated_time
        self.name = name
        self.owner_id = owner_id
        self.report_ids = report_ids
        self.short_name = short_name
        self.underlying_portfolio_ids = underlying_portfolio_ids
        self.tags = tags
        self.__type = get_enum_value(PortfolioType, type_)
        self.parameters = parameters

    @property
    def created_by_id(self) -> str:
        """Unique identifier of user who created the object."""
        return self.__created_by_id

    @created_by_id.setter
    def created_by_id(self, value: str):
        self._property_changed('created_by_id')
        self.__created_by_id = value        

    @property
    def created_time(self) -> datetime.datetime:
        """Time created. ISO 8601 formatted string."""
        return self.__created_time

    @created_time.setter
    def created_time(self, value: datetime.datetime):
        self._property_changed('created_time')
        self.__created_time = value        

    @property
    def currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self._property_changed('currency')
        self.__currency = get_enum_value(Currency, value)        

    @property
    def description(self) -> str:
        """Free text description of portfolio. Description provided will be indexed in the
           search service for free text relevance match"""
        return self.__description

    @description.setter
    def description(self, value: str):
        self._property_changed('description')
        self.__description = value        

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
    def id(self) -> str:
        """Marquee unique portfolio identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def identifiers(self) -> Tuple[Identifier, ...]:
        """Array of identifier objects which can be used to locate this item in searches
           and other services"""
        return self.__identifiers

    @identifiers.setter
    def identifiers(self, value: Tuple[Identifier, ...]):
        self._property_changed('identifiers')
        self.__identifiers = value        

    @property
    def last_updated_by_id(self) -> str:
        """Unique identifier of user who last updated the object."""
        return self.__last_updated_by_id

    @last_updated_by_id.setter
    def last_updated_by_id(self, value: str):
        self._property_changed('last_updated_by_id')
        self.__last_updated_by_id = value        

    @property
    def last_updated_time(self) -> datetime.datetime:
        """Timestamp of when the object was last updated."""
        return self.__last_updated_time

    @last_updated_time.setter
    def last_updated_time(self, value: datetime.datetime):
        self._property_changed('last_updated_time')
        self.__last_updated_time = value        

    @property
    def name(self) -> str:
        """Display name of the portfolio"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def owner_id(self) -> str:
        """Marquee unique identifier for user who owns the object."""
        return self.__owner_id

    @owner_id.setter
    def owner_id(self, value: str):
        self._property_changed('owner_id')
        self.__owner_id = value        

    @property
    def report_ids(self) -> Tuple[str, ...]:
        """Array of report identifiers related to the object"""
        return self.__report_ids

    @report_ids.setter
    def report_ids(self, value: Tuple[str, ...]):
        self._property_changed('report_ids')
        self.__report_ids = value        

    @property
    def short_name(self) -> str:
        """Short name or alias for the portfolio"""
        return self.__short_name

    @short_name.setter
    def short_name(self, value: str):
        self._property_changed('short_name')
        self.__short_name = value        

    @property
    def underlying_portfolio_ids(self) -> Tuple[str, ...]:
        """Underlying portfolio Ids"""
        return self.__underlying_portfolio_ids

    @underlying_portfolio_ids.setter
    def underlying_portfolio_ids(self, value: Tuple[str, ...]):
        self._property_changed('underlying_portfolio_ids')
        self.__underlying_portfolio_ids = value        

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
    def type(self) -> Union[PortfolioType, str]:
        """Portfolio type differentiates the portfolio categorization"""
        return self.__type

    @type.setter
    def type(self, value: Union[PortfolioType, str]):
        self._property_changed('type')
        self.__type = get_enum_value(PortfolioType, value)        

    @property
    def parameters(self) -> dict:
        return self.__parameters

    @parameters.setter
    def parameters(self, value: dict):
        self._property_changed('parameters')
        self.__parameters = value        
