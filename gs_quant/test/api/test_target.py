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

import inspect
import sys

from gs_quant.base import Base


def classes(module_name) -> list:
    module_path = 'gs_quant.target.' + module_name
    __import__(module_path)
    module = sys.modules[module_path]
    return [m for n, m in inspect.getmembers(module) if inspect.isclass(m) and issubclass(m, Base)]


def new_instance(typ: type) -> Base:
    args = [k for k, v in inspect.signature(typ.__init__).parameters.items() if v.default == inspect.Parameter.empty][1:]
    return typ(**{a: None for a in args})


def test_classes():
    for module_name in ('assets', 'backtests', 'common', 'content', 'data', 'indices', 'instrument', 'monitor', 'portfolios', 'reports', 'risk', 'trades'):
        for typ in classes(module_name):
            obj = new_instance(typ)

            for prop_name in obj.properties():
                _ = getattr(obj, prop_name)
                if getattr(typ, prop_name).fset is not None:
                    setattr(obj, prop_name, None)
