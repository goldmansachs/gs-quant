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
from gs_quant.base import Base, InstrumentBase, camel_case_translate, get_enum_value


class GroupWithMembersCount(Base):
        
    """Marquee Group with Members Count"""

    @camel_case_translate
    def __init__(
        self,
        members_count: int = None,
        name: str = None
    ):        
        super().__init__()
        self.members_count = members_count
        self.name = name

    @property
    def members_count(self) -> int:
        """Total number of members in the group"""
        return self.__members_count

    @members_count.setter
    def members_count(self, value: int):
        self._property_changed('members_count')
        self.__members_count = value        


class UpdateGroupMembershipRequest(Base):
        
    @camel_case_translate
    def __init__(
        self,
        user_ids: Tuple[str, ...],
        name: str = None
    ):        
        super().__init__()
        self.user_ids = user_ids
        self.name = name

    @property
    def user_ids(self) -> Tuple[str, ...]:
        """List of marquee user guids"""
        return self.__user_ids

    @user_ids.setter
    def user_ids(self, value: Tuple[str, ...]):
        self._property_changed('user_ids')
        self.__user_ids = value        


class UserTag(Base):
        
    """Marquee User Tag Attribute"""

    @camel_case_translate
    def __init__(
        self,
        name: str,
        added_on: datetime.datetime = None,
        added_by_id: str = None,
        removed: bool = None,
        removed_on: datetime.datetime = None,
        removed_by_id: str = None,
        removal_reason: str = None,
        category: str = None
    ):        
        super().__init__()
        self.added_on = added_on
        self.added_by_id = added_by_id
        self.removed = removed
        self.removed_on = removed_on
        self.removed_by_id = removed_by_id
        self.removal_reason = removal_reason
        self.category = category
        self.name = name

    @property
    def added_on(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__added_on

    @added_on.setter
    def added_on(self, value: datetime.datetime):
        self._property_changed('added_on')
        self.__added_on = value        

    @property
    def added_by_id(self) -> str:
        """Marquee unique identifier"""
        return self.__added_by_id

    @added_by_id.setter
    def added_by_id(self, value: str):
        self._property_changed('added_by_id')
        self.__added_by_id = value        

    @property
    def removed(self) -> bool:
        """Flag to indicate if tag has been removed"""
        return self.__removed

    @removed.setter
    def removed(self, value: bool):
        self._property_changed('removed')
        self.__removed = value        

    @property
    def removed_on(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__removed_on

    @removed_on.setter
    def removed_on(self, value: datetime.datetime):
        self._property_changed('removed_on')
        self.__removed_on = value        

    @property
    def removed_by_id(self) -> str:
        """Marquee unique identifier"""
        return self.__removed_by_id

    @removed_by_id.setter
    def removed_by_id(self, value: str):
        self._property_changed('removed_by_id')
        self.__removed_by_id = value        

    @property
    def removal_reason(self) -> str:
        """Reason tag was removed"""
        return self.__removal_reason

    @removal_reason.setter
    def removal_reason(self, value: str):
        self._property_changed('removal_reason')
        self.__removal_reason = value        

    @property
    def category(self) -> str:
        """Category of the tag"""
        return self.__category

    @category.setter
    def category(self, value: str):
        self._property_changed('category')
        self.__category = value        

    @property
    def name(self) -> str:
        """Name of the tag"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        


class GroupResponse(Base):
        
    @camel_case_translate
    def __init__(
        self,
        results: Tuple[GroupWithMembersCount, ...],
        total_results: int,
        scroll_id: Tuple[str, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.total_results = total_results
        self.results = results
        self.scroll_id = scroll_id
        self.name = name

    @property
    def total_results(self) -> int:
        """Total number of groups that match the query."""
        return self.__total_results

    @total_results.setter
    def total_results(self, value: int):
        self._property_changed('total_results')
        self.__total_results = value        

    @property
    def results(self) -> Tuple[GroupWithMembersCount, ...]:
        """Array of group objects"""
        return self.__results

    @results.setter
    def results(self, value: Tuple[GroupWithMembersCount, ...]):
        self._property_changed('results')
        self.__results = value        

    @property
    def scroll_id(self) -> Tuple[str, ...]:
        """Scroll identifier to be used to retrieve the next batch of results"""
        return self.__scroll_id

    @scroll_id.setter
    def scroll_id(self, value: Tuple[str, ...]):
        self._property_changed('scroll_id')
        self.__scroll_id = value        


class CreateGroupRequest(Base):
        
    """Marquee Group"""

    @camel_case_translate
    def __init__(
        self,
        id_: str,
        name: str,
        description: str = None,
        entitlements: Entitlements = None,
        oe_id: str = None,
        owner_id: str = None,
        tags: Tuple[str, ...] = None
    ):        
        super().__init__()
        self.__id = id_
        self.description = description
        self.name = name
        self.entitlements = entitlements
        self.oe_id = oe_id
        self.owner_id = owner_id
        self.tags = tags

    @property
    def id(self) -> str:
        """Marquee unique identifier for a group"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def description(self) -> str:
        """Group description"""
        return self.__description

    @description.setter
    def description(self, value: str):
        self._property_changed('description')
        self.__description = value        

    @property
    def name(self) -> str:
        """Name of the group"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def entitlements(self) -> Entitlements:
        """Entitlements for the given group"""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self._property_changed('entitlements')
        self.__entitlements = value        

    @property
    def oe_id(self) -> str:
        """Goldman Sachs unique identifier for client's organization"""
        return self.__oe_id

    @oe_id.setter
    def oe_id(self, value: str):
        self._property_changed('oe_id')
        self.__oe_id = value        

    @property
    def owner_id(self) -> str:
        """Marquee unique identifier of user who owns the group. If not specified, ownerId
           is same as createdById"""
        return self.__owner_id

    @owner_id.setter
    def owner_id(self, value: str):
        self._property_changed('owner_id')
        self.__owner_id = value        

    @property
    def tags(self) -> Tuple[str, ...]:
        """Tags associated with the groups"""
        return self.__tags

    @tags.setter
    def tags(self, value: Tuple[str, ...]):
        self._property_changed('tags')
        self.__tags = value        


class UpdateGroupRequest(Base):
        
    """Marquee Group"""

    @camel_case_translate
    def __init__(
        self,
        name: str = None,
        description: str = None,
        entitlements: Entitlements = None,
        oe_id: str = None,
        owner_id: str = None,
        tags: Tuple[str, ...] = None
    ):        
        super().__init__()
        self.name = name
        self.description = description
        self.entitlements = entitlements
        self.oe_id = oe_id
        self.owner_id = owner_id
        self.tags = tags

    @property
    def name(self) -> str:
        """Name of the group"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def description(self) -> str:
        """Group description"""
        return self.__description

    @description.setter
    def description(self, value: str):
        self._property_changed('description')
        self.__description = value        

    @property
    def entitlements(self) -> Entitlements:
        """Entitlements for the given group"""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self._property_changed('entitlements')
        self.__entitlements = value        

    @property
    def oe_id(self) -> str:
        """Goldman Sachs unique identifier for client's organization"""
        return self.__oe_id

    @oe_id.setter
    def oe_id(self, value: str):
        self._property_changed('oe_id')
        self.__oe_id = value        

    @property
    def owner_id(self) -> str:
        """Marquee unique identifier of user who owns the group. If not specified, ownerId
           is same as createdById"""
        return self.__owner_id

    @owner_id.setter
    def owner_id(self, value: str):
        self._property_changed('owner_id')
        self.__owner_id = value        

    @property
    def tags(self) -> Tuple[str, ...]:
        """Tags associated with the groups"""
        return self.__tags

    @tags.setter
    def tags(self, value: Tuple[str, ...]):
        self._property_changed('tags')
        self.__tags = value        


class Group(Base):
        
    """Marquee Group"""

    @camel_case_translate
    def __init__(
        self,
        id_: str,
        name: str,
        description: str = None,
        created_by_id: str = None,
        last_updated_by_id: str = None,
        entitlements: Entitlements = None,
        owner_id: str = None,
        oe_id: str = None,
        tags: Tuple[str, ...] = None
    ):        
        super().__init__()
        self.description = description
        self.name = name
        self.__id = id_
        self.created_by_id = created_by_id
        self.last_updated_by_id = last_updated_by_id
        self.entitlements = entitlements
        self.owner_id = owner_id
        self.oe_id = oe_id
        self.tags = tags

    @property
    def description(self) -> str:
        """Group description"""
        return self.__description

    @description.setter
    def description(self, value: str):
        self._property_changed('description')
        self.__description = value        

    @property
    def name(self) -> str:
        """Name of the group"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def id(self) -> str:
        """Marquee unique identifier of the group"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def created_by_id(self) -> str:
        """Marquee unique identifier of user who created the group"""
        return self.__created_by_id

    @created_by_id.setter
    def created_by_id(self, value: str):
        self._property_changed('created_by_id')
        self.__created_by_id = value        

    @property
    def last_updated_by_id(self) -> str:
        """Marquee unique identifier of user who last updated the group"""
        return self.__last_updated_by_id

    @last_updated_by_id.setter
    def last_updated_by_id(self, value: str):
        self._property_changed('last_updated_by_id')
        self.__last_updated_by_id = value        

    @property
    def entitlements(self) -> Entitlements:
        """Entitlements for the given group"""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self._property_changed('entitlements')
        self.__entitlements = value        

    @property
    def owner_id(self) -> str:
        """Marquee unique identifier of user who owns the group. If not specified, ownerId
           is same as createdById"""
        return self.__owner_id

    @owner_id.setter
    def owner_id(self, value: str):
        self._property_changed('owner_id')
        self.__owner_id = value        

    @property
    def oe_id(self) -> str:
        """Goldman Sachs unique identifier for client's organization"""
        return self.__oe_id

    @oe_id.setter
    def oe_id(self, value: str):
        self._property_changed('oe_id')
        self.__oe_id = value        

    @property
    def tags(self) -> Tuple[str, ...]:
        """Tags associated with the groups"""
        return self.__tags

    @tags.setter
    def tags(self, value: Tuple[str, ...]):
        self._property_changed('tags')
        self.__tags = value        
