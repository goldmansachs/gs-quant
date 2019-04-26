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
import pytest

from gs_quant.timeseries.operator import *


def test_add():
    result = add(3, 2)
    assert result == 5
    with pytest.raises(TypeError):
        add(None, None)


def test_subtract():
    result = subtract(3, 2)
    assert result == 1
    with pytest.raises(TypeError):
        subtract(None, None)


def test_multiply():
    result = multiply(3, 2)
    assert result == 6
    with pytest.raises(TypeError):
        multiply(None, None)


def test_truediv():
    result = truediv(3, 2)
    assert result == 1.5
    with pytest.raises(TypeError):
        truediv(None, None)


def test_floordiv():
    result = floordiv(3, 2)
    assert result == 1
    with pytest.raises(TypeError):
        floordiv(None, None)
