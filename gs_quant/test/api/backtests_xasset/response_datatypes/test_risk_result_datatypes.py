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

import dataclasses

import pytest

from gs_quant.api.gs.backtests_xasset.response_datatypes.risk_result_datatypes import RiskResultWithData, \
    FloatWithData, StringWithData, VectorWithData, MatrixWithData


def test_request_types():
    cls = (RiskResultWithData, FloatWithData, StringWithData, VectorWithData, MatrixWithData)
    for c in cls:
        assert dataclasses.is_dataclass(c)
        assert issubclass(c, RiskResultWithData)


def test_arithmetics():
    assert FloatWithData(result=2) + FloatWithData(result=3) == FloatWithData(result=5)
    assert FloatWithData(result=2) - FloatWithData(result=3) == FloatWithData(result=-1)
    assert FloatWithData(result=2) * FloatWithData(result=3) == FloatWithData(result=6)
    assert FloatWithData(result=2, unit='EUR') / FloatWithData(result=3, unit='EUR') == FloatWithData(result=2 / 3,
                                                                                                      unit='EUR')
    assert 3 + FloatWithData(result=2, unit='EUR') == FloatWithData(result=5, unit='EUR')
    with pytest.raises(TypeError):
        FloatWithData(result=2) + 'a'
    with pytest.raises(ValueError):
        FloatWithData(result=2, unit='EUR') + FloatWithData(result=3, unit='USD')

    assert StringWithData(result='ab') + StringWithData(result='cd') == StringWithData(result='abcd')
    assert StringWithData(result='ab') + 'cd' == StringWithData(result='abcd')
