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

import copy
import inspect
import pickle

from gs_quant.base import Base
from gs_quant.common import Currency
from gs_quant.test.dataclass_test_utils import generated_classes, generated_modules


def test_enum():
    ccy = copy.deepcopy(Currency.HUF)
    assert ccy == Currency.HUF

    gbp_pickled = pickle.dumps(Currency.GBP)
    assert pickle.loads(gbp_pickled) == Currency.GBP


def test_classes():
    # The contracts of these classes are tested in gs_quant/test/test_class_contracts.py
    modules = generated_modules()
    covered = set(generated_classes(modules))
    assert covered
    for module in modules:
        defined = {
            c
            for c in vars(module).values()
            if inspect.isclass(c) and c.__module__ == module.__name__ and issubclass(c, Base)
        }
        assert defined <= covered, module.__name__
