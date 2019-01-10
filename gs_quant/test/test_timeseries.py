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

from ..timeseries import *
import inspect
import pytest
import re
import types


@pytest.fixture(scope='module')
def ts_map():
    return {k: v for k, v in globals().items() if isinstance(v, types.FunctionType)
            and v.__module__.startswith('gs_quant.timeseries') and not k.startswith('_')}


def test_have_docstrings(ts_map):
    for k, v in ts_map.items():
        assert v.__doc__


def test_docstrings(ts_map):
    for k, v in ts_map.items():
        print('testing function', k)
        params = set()
        has_return = False
        others = 0

        lines = [x.strip() for x in v.__doc__.splitlines()]
        for line in lines:
            if not line:
                continue
            print(line)
            if line.startswith(':param'):
                params.add(re.split('[:\\s]+', line)[2])
            elif line.startswith(':return:'):
                has_return = True
            else:
                others += 1

        assert params == set(inspect.signature(v).parameters.keys()), 'all parameters documented'
        assert has_return, 'return value is documented'
        assert others >= 1, 'at least one line description'


def test_annotations(ts_map):
    for k, v in ts_map.items():
        print('testing function', k)
        annotations = v.__annotations__
        assert annotations, 'has annotations'
        assert 'return' in annotations, 'specifies return type'
        assert set(inspect.signature(v).parameters.keys()) | {'return'} == set(annotations.keys()), \
            'specifies parameter types'
