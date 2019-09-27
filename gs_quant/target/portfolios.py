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

from enum import Enum
from gs_quant.base import Base, EnumBase, get_enum_value
from gs_quant.target.common import *
from typing import Tuple, Union
import datetime


class PortfolioType(EnumBase, Enum):    
    
    """Portfolio type differentiates the portfolio categorization"""

    Securities_Lending = 'Securities Lending'
    Draft_Portfolio = 'Draft Portfolio'
    
    def __repr__(self):
        return self.value


class Portfolio(Base):
               
    def __init__(
        self,
        currency: Union[Currency, str],
        name: str,
        created_by_id: str = None,
        created_time: datetime.datetime = None,
        description: str = None,
        entitlements: Entitlements = None,
        entitlement_exclusions: EntitlementExclusions = None,
        id: str = None,
        identifiers: Tuple[Identifier, ...] = None,
        last_updated_by_id: str = None,
        last_updated_time: datetime.datetime = None,
        owner_id: str = None,
        report_ids: Tuple[str, ...] = None,
        short_name: str = None,
        underlying_portfolio_ids: Tuple[str, ...] = None,
        tags: Tuple[str, ...] = None,
        type: Union[PortfolioType, str] = None,
        parameters: LiquidityRequest = None        
    ):
        super().__init__()
        self.__created_by_id = created_by_id
        self.__created_time = created_time
        self.__currency = get_enum_value(Currency, currency)
        self.__description = description
        self.__entitlements = entitlements
        self.__entitlement_exclusions = entitlement_exclusions
        self.__id = id
        self.__identifiers = identifiers
        self.__last_updated_by_id = last_updated_by_id
        self.__last_updated_time = last_updated_time
        self.__name = name
        self.__owner_id = owner_id
        self.__report_ids = report_ids
        self.__short_name = short_name
        self.__underlying_portfolio_ids = underlying_portfolio_ids
        self.__tags = tags
        self.__type = get_enum_value(PortfolioType, type)
        self.__parameters = parameters

    @property
    def created_by_id(self) -> str:
        """Unique identifier of user who created the object"""
        return self.__created_by_id

    @created_by_id.setter
    def created_by_id(self, value: str):
        self.__created_by_id = value
        self._property_changed('created_by_id')        

    @property
    def created_time(self) -> datetime.datetime:
        """Time created. ISO 8601 formatted string"""
        return self.__created_time

    @created_time.setter
    def created_time(self, value: datetime.datetime):
        self.__created_time = value
        self._property_changed('created_time')        

    @property
    def currency(self) -> Union[Currency, str]:
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self.__currency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('currency')        

    @property
    def description(self) -> str:
        """Free text description of portfolio. Description provided will be indexed in the search service for free text relevance match"""
        return self.__description

    @description.setter
    def description(self, value: str):
        self.__description = value
        self._property_changed('description')        

    @property
    def entitlements(self) -> Entitlements:
        """Defines the entitlements of a given resource"""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self.__entitlements = value
        self._property_changed('entitlements')        

    @property
    def entitlement_exclusions(self) -> EntitlementExclusions:
        """Defines the exclusion entitlements of a given resource"""
        return self.__entitlement_exclusions

    @entitlement_exclusions.setter
    def entitlement_exclusions(self, value: EntitlementExclusions):
        self.__entitlement_exclusions = value
        self._property_changed('entitlement_exclusions')        

    @property
    def id(self) -> str:
        """Marquee unique portfolio identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value
        self._property_changed('id')        

    @property
    def identifiers(self) -> Tuple[Identifier, ...]:
        """Array of identifier objects which can be used to locate this item in searches and other services"""
        return self.__identifiers

    @identifiers.setter
    def identifiers(self, value: Tuple[Identifier, ...]):
        self.__identifiers = value
        self._property_changed('identifiers')        

    @property
    def last_updated_by_id(self) -> str:
        """Unique identifier of user who last updated the object"""
        return self.__last_updated_by_id

    @last_updated_by_id.setter
    def last_updated_by_id(self, value: str):
        self.__last_updated_by_id = value
        self._property_changed('last_updated_by_id')        

    @property
    def last_updated_time(self) -> datetime.datetime:
        """Timestamp of when the object was last updated"""
        return self.__last_updated_time

    @last_updated_time.setter
    def last_updated_time(self, value: datetime.datetime):
        self.__last_updated_time = value
        self._property_changed('last_updated_time')        

    @property
    def name(self) -> str:
        """Display name of the portfolio"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def owner_id(self) -> str:
        """Marquee unique identifier for user who owns the object."""
        return self.__owner_id

    @owner_id.setter
    def owner_id(self, value: str):
        self.__owner_id = value
        self._property_changed('owner_id')        

    @property
    def report_ids(self) -> Tuple[str, ...]:
        """Array of report identifiers related to the object"""
        return self.__report_ids

    @report_ids.setter
    def report_ids(self, value: Tuple[str, ...]):
        self.__report_ids = value
        self._property_changed('report_ids')        

    @property
    def short_name(self) -> str:
        """Short name or alias for the portfolio"""
        return self.__short_name

    @short_name.setter
    def short_name(self, value: str):
        self.__short_name = value
        self._property_changed('short_name')        

    @property
    def underlying_portfolio_ids(self) -> Tuple[str, ...]:
        """Underlying portfolio Ids"""
        return self.__underlying_portfolio_ids

    @underlying_portfolio_ids.setter
    def underlying_portfolio_ids(self, value: Tuple[str, ...]):
        self.__underlying_portfolio_ids = value
        self._property_changed('underlying_portfolio_ids')        

    @property
    def tags(self) -> Tuple[str, ...]:
        """Metadata associated with the object. Provide an array of strings which will be indexed for search and locating related objects"""
        return self.__tags

    @tags.setter
    def tags(self, value: Tuple[str, ...]):
        self.__tags = value
        self._property_changed('tags')        

    @property
    def type(self) -> Union[PortfolioType, str]:
        """Portfolio type differentiates the portfolio categorization"""
        return self.__type

    @type.setter
    def type(self, value: Union[PortfolioType, str]):
        self.__type = value if isinstance(value, PortfolioType) else get_enum_value(PortfolioType, value)
        self._property_changed('type')        

    @property
    def parameters(self) -> LiquidityRequest:
        return self.__parameters

    @parameters.setter
    def parameters(self, value: LiquidityRequest):
        self.__parameters = value
        self._property_changed('parameters')        
