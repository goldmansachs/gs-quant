"""
Copyright 2018 Goldman Sachs.
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
from dataclasses import field, dataclass
from enum import Enum
from typing import Union, Tuple, Optional

import gs_quant.base as base
from gs_quant.base import handle_camel_case_args, Base, EnumBase


class TestEnum(EnumBase, Enum):
    Enum_1 = 'Enum_1'
    Enum_2 = 'Enum_2'


@handle_camel_case_args
@dataclass
class BaseSubclass(Base):
    instance_attr: str = field(default=None)
    attr_1: Optional[str] = field(default=None)
    attr_2: Tuple[Union[float, str], ...] = field(default=())
    attr_3: Union[Tuple[Optional[str], ...], str] = field(default=None)
    attr_4: Tuple[int] = field(default=None)
    attr_5: Tuple[int, str] = field(default=None)
    attr_6: TestEnum = field(default=None)


def test_handle_camel_case_args():
    # Handling camelcase args on init
    obj = BaseSubclass(instanceAttr="test")
    assert obj.instance_attr == "test"


def test_base_getter():
    obj = BaseSubclass(instance_attr="test")

    # Handling camelcase getter
    assert obj.instanceAttr == "test"


def test_base_setter():
    obj = BaseSubclass()

    # Handling camelcase setter
    obj.instanceAttr = "test"
    assert obj.instance_attr == "test"


def test_setter_coercion():
    base._is_supported_generic_cache = {}
    obj = BaseSubclass(instance_attr='test', attr_1=None, attr_2=('test', 1.0, 1), attr_3='test',
                       attr_4=(1,), attr_5=(3, 'test'), attr_6=TestEnum.Enum_1)
    obj.attr_1 = 'test'
    # str with type hint str is unchanged
    obj.attr_1 = 'Enum_1'
    assert isinstance(obj.attr_1, str)
    # Enum with type hint str is unchanged
    obj.attr_1 = TestEnum.Enum_1
    assert isinstance(obj.attr_1, TestEnum)
    obj.attr_2 = (1, 2, 3)
    obj.attr_3 = (None, 'test', None)
    obj.attr_4 = (1, 1, 1)
    obj.attr_5 = (0, 'test')
    # Enum with type hint Enum is unchanged
    obj.attr_6 = TestEnum.Enum_2
    assert isinstance(obj.attr_6, TestEnum)
    # all handled as type matches, we do not get to the generic coercion/default case
    assert not base._is_supported_generic_cache
    # str with type hint Enum gets cast to Enum
    obj.attr_6 = 'Enum_1'
    assert isinstance(obj.attr_6, TestEnum)
    assert TestEnum in base._is_supported_generic_cache
