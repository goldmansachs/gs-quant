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

from gs_quant.target.common import *
import datetime
from typing import Tuple, Union
from gs_quant.base import Base, InstrumentBase, camel_case_translate, get_enum_value


class CountryXref(Base):
        
    """Historical references used for a country."""

    @camel_case_translate
    def __init__(
        self,
        alpha2: str,
        alpha3: str,
        country_code: str,
        bbid: str = None,
        name: str = None
    ):        
        super().__init__()
        self.alpha2 = alpha2
        self.alpha3 = alpha3
        self.bbid = bbid
        self.country_code = country_code
        self.name = name

    @property
    def alpha2(self) -> str:
        """ISO 3166 Country Alpha 2 Code. 2 character code to identify a country."""
        return self.__alpha2

    @alpha2.setter
    def alpha2(self, value: str):
        self._property_changed('alpha2')
        self.__alpha2 = value        

    @property
    def alpha3(self) -> str:
        """ISO 3166 Country Alpha 3 Code. 3 character code to identify a country."""
        return self.__alpha3

    @alpha3.setter
    def alpha3(self, value: str):
        self._property_changed('alpha3')
        self.__alpha3 = value        

    @property
    def bbid(self) -> str:
        """The bloomberg identifier for a country."""
        return self.__bbid

    @bbid.setter
    def bbid(self, value: str):
        self._property_changed('bbid')
        self.__bbid = value        

    @property
    def country_code(self) -> str:
        """ISO 3166 Country Code. Generally a three digit country code."""
        return self.__country_code

    @country_code.setter
    def country_code(self, value: str):
        self._property_changed('country_code')
        self.__country_code = value        


class Subdivision(Base):
        
    """A marquee subdivision (or state) object"""

    @camel_case_translate
    def __init__(
        self,
        name: str,
        id_: str,
        country_id: str,
        created_time: datetime.datetime = None,
        last_updated_time: datetime.datetime = None,
        created_by_id: str = None,
        last_updated_by_id: str = None,
        owner_id: str = None,
        entitlements: Entitlements = None
    ):        
        super().__init__()
        self.__id = id_
        self.country_id = country_id
        self.name = name
        self.created_time = created_time
        self.last_updated_time = last_updated_time
        self.created_by_id = created_by_id
        self.last_updated_by_id = last_updated_by_id
        self.owner_id = owner_id
        self.entitlements = entitlements

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def country_id(self) -> str:
        """Marquee unique identifier"""
        return self.__country_id

    @country_id.setter
    def country_id(self, value: str):
        self._property_changed('country_id')
        self.__country_id = value        

    @property
    def name(self) -> str:
        """Name of the subdivision (or state)"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def created_time(self) -> datetime.datetime:
        """Time created. ISO 8601 formatted string"""
        return self.__created_time

    @created_time.setter
    def created_time(self, value: datetime.datetime):
        self._property_changed('created_time')
        self.__created_time = value        

    @property
    def last_updated_time(self) -> datetime.datetime:
        """Timestamp of when the object was last updated"""
        return self.__last_updated_time

    @last_updated_time.setter
    def last_updated_time(self, value: datetime.datetime):
        self._property_changed('last_updated_time')
        self.__last_updated_time = value        

    @property
    def created_by_id(self) -> str:
        """Unique identifier of user who created the object"""
        return self.__created_by_id

    @created_by_id.setter
    def created_by_id(self, value: str):
        self._property_changed('created_by_id')
        self.__created_by_id = value        

    @property
    def last_updated_by_id(self) -> str:
        """Unique identifier of user who last updated the object"""
        return self.__last_updated_by_id

    @last_updated_by_id.setter
    def last_updated_by_id(self, value: str):
        self._property_changed('last_updated_by_id')
        self.__last_updated_by_id = value        

    @property
    def owner_id(self) -> str:
        """Marquee unique identifier"""
        return self.__owner_id

    @owner_id.setter
    def owner_id(self, value: str):
        self._property_changed('owner_id')
        self.__owner_id = value        

    @property
    def entitlements(self) -> Entitlements:
        """Defines the entitlements of a given resource"""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self._property_changed('entitlements')
        self.__entitlements = value        


class Country(Base):
        
    """A marquee country object"""

    @camel_case_translate
    def __init__(
        self,
        name: str,
        id_: str,
        xref: CountryXref,
        region: str,
        sub_region: str,
        region_code: str,
        sub_region_code: str,
        created_time: datetime.datetime = None,
        last_updated_time: datetime.datetime = None,
        created_by_id: str = None,
        last_updated_by_id: str = None,
        owner_id: str = None,
        entitlements: Entitlements = None
    ):        
        super().__init__()
        self.__id = id_
        self.name = name
        self.created_time = created_time
        self.last_updated_time = last_updated_time
        self.created_by_id = created_by_id
        self.last_updated_by_id = last_updated_by_id
        self.owner_id = owner_id
        self.entitlements = entitlements
        self.region = region
        self.sub_region = sub_region
        self.region_code = region_code
        self.sub_region_code = sub_region_code
        self.xref = xref

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def name(self) -> str:
        """Name of the country"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def created_time(self) -> datetime.datetime:
        """Time created. ISO 8601 formatted string"""
        return self.__created_time

    @created_time.setter
    def created_time(self, value: datetime.datetime):
        self._property_changed('created_time')
        self.__created_time = value        

    @property
    def last_updated_time(self) -> datetime.datetime:
        """Timestamp of when the object was last updated"""
        return self.__last_updated_time

    @last_updated_time.setter
    def last_updated_time(self, value: datetime.datetime):
        self._property_changed('last_updated_time')
        self.__last_updated_time = value        

    @property
    def created_by_id(self) -> str:
        """Unique identifier of user who created the object"""
        return self.__created_by_id

    @created_by_id.setter
    def created_by_id(self, value: str):
        self._property_changed('created_by_id')
        self.__created_by_id = value        

    @property
    def last_updated_by_id(self) -> str:
        """Unique identifier of user who last updated the object"""
        return self.__last_updated_by_id

    @last_updated_by_id.setter
    def last_updated_by_id(self, value: str):
        self._property_changed('last_updated_by_id')
        self.__last_updated_by_id = value        

    @property
    def owner_id(self) -> str:
        """Marquee unique identifier"""
        return self.__owner_id

    @owner_id.setter
    def owner_id(self, value: str):
        self._property_changed('owner_id')
        self.__owner_id = value        

    @property
    def entitlements(self) -> Entitlements:
        """Defines the entitlements of a given resource"""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self._property_changed('entitlements')
        self.__entitlements = value        

    @property
    def region(self) -> str:
        """ISO 3166 Country Region."""
        return self.__region

    @region.setter
    def region(self, value: str):
        self._property_changed('region')
        self.__region = value        

    @property
    def sub_region(self) -> str:
        """ISO 3166 Country Sub Region."""
        return self.__sub_region

    @sub_region.setter
    def sub_region(self, value: str):
        self._property_changed('sub_region')
        self.__sub_region = value        

    @property
    def region_code(self) -> str:
        """ISO 3166 Region Code. Generally a three digit code."""
        return self.__region_code

    @region_code.setter
    def region_code(self, value: str):
        self._property_changed('region_code')
        self.__region_code = value        

    @property
    def sub_region_code(self) -> str:
        """ISO 3166 Sub Region Code."""
        return self.__sub_region_code

    @sub_region_code.setter
    def sub_region_code(self, value: str):
        self._property_changed('sub_region_code')
        self.__sub_region_code = value        

    @property
    def xref(self) -> CountryXref:
        """Historical references used for a country."""
        return self.__xref

    @xref.setter
    def xref(self, value: CountryXref):
        self._property_changed('xref')
        self.__xref = value        
