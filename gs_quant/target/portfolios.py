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


class DateRange(Base):
               
    def __init__(self, endDate: datetime.date = None, startDate: datetime.date = None):
        super().__init__()
        self.__endDate = endDate
        self.__startDate = startDate

    @property
    def endDate(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__endDate

    @endDate.setter
    def endDate(self, value: datetime.date):
        self.__endDate = value
        self._property_changed('endDate')        

    @property
    def startDate(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__startDate

    @startDate.setter
    def startDate(self, value: datetime.date):
        self.__startDate = value
        self._property_changed('startDate')        


class Portfolio(Base):
               
    def __init__(self, currency: Union[Currency, str], name: str, createdById: str = None, createdTime: datetime.datetime = None, description: str = None, entitlements: Entitlements = None, entitlementExclusions: EntitlementExclusions = None, id: str = None, identifiers: Tuple[Identifier, ...] = None, lastUpdatedById: str = None, lastUpdatedTime: datetime.datetime = None, ownerId: str = None, reportIds: Tuple[str, ...] = None, shortName: str = None, underlyingPortfolioIds: Tuple[str, ...] = None, tags: Tuple[str, ...] = None, type: Union[PortfolioType, str] = None, parameters: LiquidityRequest = None):
        super().__init__()
        self.__createdById = createdById
        self.__createdTime = createdTime
        self.__currency = currency if isinstance(currency, Currency) else get_enum_value(Currency, currency)
        self.__description = description
        self.__entitlements = entitlements
        self.__entitlementExclusions = entitlementExclusions
        self.__id = id
        self.__identifiers = identifiers
        self.__lastUpdatedById = lastUpdatedById
        self.__lastUpdatedTime = lastUpdatedTime
        self.__name = name
        self.__ownerId = ownerId
        self.__reportIds = reportIds
        self.__shortName = shortName
        self.__underlyingPortfolioIds = underlyingPortfolioIds
        self.__tags = tags
        self.__type = type if isinstance(type, PortfolioType) else get_enum_value(PortfolioType, type)
        self.__parameters = parameters

    @property
    def createdById(self) -> str:
        """Unique identifier of user who created the object"""
        return self.__createdById

    @createdById.setter
    def createdById(self, value: str):
        self.__createdById = value
        self._property_changed('createdById')        

    @property
    def createdTime(self) -> datetime.datetime:
        """Time created. ISO 8601 formatted string"""
        return self.__createdTime

    @createdTime.setter
    def createdTime(self, value: datetime.datetime):
        self.__createdTime = value
        self._property_changed('createdTime')        

    @property
    def currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
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
    def entitlementExclusions(self) -> EntitlementExclusions:
        """Defines the exclusion entitlements of a given resource"""
        return self.__entitlementExclusions

    @entitlementExclusions.setter
    def entitlementExclusions(self, value: EntitlementExclusions):
        self.__entitlementExclusions = value
        self._property_changed('entitlementExclusions')        

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
    def lastUpdatedById(self) -> str:
        """Unique identifier of user who last updated the object"""
        return self.__lastUpdatedById

    @lastUpdatedById.setter
    def lastUpdatedById(self, value: str):
        self.__lastUpdatedById = value
        self._property_changed('lastUpdatedById')        

    @property
    def lastUpdatedTime(self) -> datetime.datetime:
        """Timestamp of when the object was last updated"""
        return self.__lastUpdatedTime

    @lastUpdatedTime.setter
    def lastUpdatedTime(self, value: datetime.datetime):
        self.__lastUpdatedTime = value
        self._property_changed('lastUpdatedTime')        

    @property
    def name(self) -> str:
        """Display name of the portfolio"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def ownerId(self) -> str:
        """Marquee unique identifier for user who owns the object."""
        return self.__ownerId

    @ownerId.setter
    def ownerId(self, value: str):
        self.__ownerId = value
        self._property_changed('ownerId')        

    @property
    def reportIds(self) -> Tuple[str, ...]:
        """Array of report identifiers related to the object"""
        return self.__reportIds

    @reportIds.setter
    def reportIds(self, value: Tuple[str, ...]):
        self.__reportIds = value
        self._property_changed('reportIds')        

    @property
    def shortName(self) -> str:
        """Short name or alias for the portfolio"""
        return self.__shortName

    @shortName.setter
    def shortName(self, value: str):
        self.__shortName = value
        self._property_changed('shortName')        

    @property
    def underlyingPortfolioIds(self) -> Tuple[str, ...]:
        """Underlying portfolio Ids"""
        return self.__underlyingPortfolioIds

    @underlyingPortfolioIds.setter
    def underlyingPortfolioIds(self, value: Tuple[str, ...]):
        self.__underlyingPortfolioIds = value
        self._property_changed('underlyingPortfolioIds')        

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
