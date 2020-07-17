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


def test_classes():
    for module_name in ('assets', 'backtests', 'charts', 'common', 'content', 'coordinates', 'countries', 'data',
                        'hedge', 'indices', 'instrument', 'monitor', 'portfolios', 'reports', 'risk', 'trades',
                        'workspaces_markets'):
        for typ in classes(module_name):
            properties = typ.properties()
            if not properties:
                continue

            obj = typ.default_instance()

            for prop_name in properties:
                _ = object.__getattribute__(obj, prop_name)
                if getattr(typ, prop_name).fset is not None:
                    setattr(obj, prop_name, None)
