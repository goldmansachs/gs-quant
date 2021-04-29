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
from typing import List

from gs_quant.target.common import *


class Group(Base):

    @camel_case_translate
    def __init__(
            self,
            id_: str,
            name: str,
            oe_id: str = None,
            description: str = None,
            entitlements: Entitlements = None,
            owner_id: str = None,
            tags: List[str] = None
    ):
        super().__init__()
        self.__id = id_
        self.name = name
        self.oe_id = oe_id
        self.description = description
        self.entitlements = entitlements
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
    def name(self) -> str:
        """Name of the group"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value

    @property
    def oe_id(self) -> str:
        """Goldman Sachs unique identifier for client's organization"""
        return self.__oe_id

    @oe_id.setter
    def oe_id(self, value: str):
        self._property_changed('oe_id')
        self.__oe_id = value

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
    def owner_id(self) -> str:
        """Marquee unique identifier of who owns the group"""
        return self.__owner_id

    @owner_id.setter
    def owner_id(self, value: str):
        self._property_changed('owner_id')
        self.__owner_id = value

    @property
    def tags(self) -> List[str]:
        """Tags associated with the groups"""
        return self.__tags

    @tags.setter
    def tags(self, value: List[str]):
        self._property_changed('tags')
        self.__tags = value
