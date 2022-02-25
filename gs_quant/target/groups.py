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


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class GroupWithMembersCount(Base):
    members_count: Optional[int] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class UpdateGroupMembershipRequest(Base):
    user_ids: Tuple[str, ...] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class UserCoverage(Base):
    name: str = None
    email: str = None
    app: Optional[str] = None
    phone: Optional[str] = None
    guid: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class GroupResponse(Base):
    results: Tuple[GroupWithMembersCount, ...] = None
    total_results: int = None
    scroll_id: Optional[Tuple[str, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CreateGroupRequest(Base):
    id_: str = field(default=None, metadata=config(field_name='id'))
    name: str = None
    description: Optional[str] = None
    entitlements: Optional[Entitlements] = None
    oe_id: Optional[str] = None
    owner_id: Optional[str] = None
    tags: Optional[Tuple[str, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class UpdateGroupRequest(Base):
    name: Optional[str] = None
    description: Optional[str] = None
    entitlements: Optional[Entitlements] = None
    oe_id: Optional[str] = None
    owner_id: Optional[str] = None
    tags: Optional[Tuple[str, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Group(Base):
    id_: str = field(default=None, metadata=config(field_name='id'))
    name: str = None
    description: Optional[str] = None
    created_by_id: Optional[str] = None
    last_updated_by_id: Optional[str] = None
    entitlements: Optional[Entitlements] = None
    owner_id: Optional[str] = None
    oe_id: Optional[str] = None
    tags: Optional[Tuple[str, ...]] = None
