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

from gs_quant.base import handle_camel_case_args, Base


@handle_camel_case_args
@dataclass
class BaseSubclass(Base):
    instance_attr: str = field(default=None)


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
