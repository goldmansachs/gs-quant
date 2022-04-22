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


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class GroupWithMembersCount(Base):
    members_count: Optional[int] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class UpdateGroupMembershipRequest(Base):
    user_ids: Tuple[str, ...] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class UserCoverage(Base):
    name: str = field(default=None, metadata=field_metadata)
    email: str = field(default=None, metadata=field_metadata)
    app: Optional[str] = field(default=None, metadata=field_metadata)
    phone: Optional[str] = field(default=None, metadata=field_metadata)
    guid: Optional[str] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class UserTag(Base):
    name: str = field(default=None, metadata=field_metadata)
    added_on: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    added_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    removed: Optional[bool] = field(default=None, metadata=field_metadata)
    removed_on: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    removed_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    removal_reason: Optional[str] = field(default=None, metadata=field_metadata)
    category: Optional[str] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class GroupResponse(Base):
    results: Tuple[GroupWithMembersCount, ...] = field(default=None, metadata=field_metadata)
    total_results: int = field(default=None, metadata=field_metadata)
    scroll_id: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CreateGroupRequest(Base):
    id_: str = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    name: str = field(default=None, metadata=field_metadata)
    description: Optional[str] = field(default=None, metadata=field_metadata)
    entitlements: Optional[Entitlements] = field(default=None, metadata=field_metadata)
    oe_id: Optional[str] = field(default=None, metadata=field_metadata)
    owner_id: Optional[str] = field(default=None, metadata=field_metadata)
    tags: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class UpdateGroupRequest(Base):
    name: Optional[str] = field(default=None, metadata=field_metadata)
    description: Optional[str] = field(default=None, metadata=field_metadata)
    entitlements: Optional[Entitlements] = field(default=None, metadata=field_metadata)
    oe_id: Optional[str] = field(default=None, metadata=field_metadata)
    owner_id: Optional[str] = field(default=None, metadata=field_metadata)
    tags: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Group(Base):
    id_: str = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    name: str = field(default=None, metadata=field_metadata)
    description: Optional[str] = field(default=None, metadata=field_metadata)
    created_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    last_updated_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    entitlements: Optional[Entitlements] = field(default=None, metadata=field_metadata)
    owner_id: Optional[str] = field(default=None, metadata=field_metadata)
    oe_id: Optional[str] = field(default=None, metadata=field_metadata)
    tags: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
