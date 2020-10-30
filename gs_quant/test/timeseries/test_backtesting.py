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
from pandas.util.testing import assert_series_equal
from gs_quant.timeseries import *


def test_basket():
    dates = [
        datetime.datetime(2019, 1, 1),
        datetime.datetime(2019, 1, 2),
        datetime.datetime(2019, 1, 3),
        datetime.datetime(2019, 1, 4),
        datetime.datetime(2019, 1, 5),
        datetime.datetime(2019, 1, 6),
    ]

    x = pd.Series([100.0, 101, 103.02, 100.9596, 100.9596, 102.978792], index=dates)
    y = pd.Series([100.0, 100, 100, 100, 100, 100], index=dates)

    assert_series_equal(x, basket([x], [1]))
    assert_series_equal(x, basket([x, x], [0.5, 0.5]))
    assert_series_equal(x, basket([x, x, x], [1 / 3, 1 / 3, 1 / 3]))
    assert_series_equal(x, basket([x, y], [1, 0]))
    assert_series_equal(y, basket([x, y], [0, 1]))
    with pytest.raises(MqValueError):
        basket([x, y], [1])
    with pytest.raises(MqTypeError):
        basket([1, 2, 3], [1])

    dates = [
        datetime.datetime(2019, 1, 1),
        datetime.datetime(2019, 1, 2),
        datetime.datetime(2019, 1, 3),
        datetime.datetime(2019, 1, 4),
        datetime.datetime(2019, 1, 5),
        datetime.datetime(2019, 1, 6),
        datetime.datetime(2019, 2, 1),
        datetime.datetime(2019, 2, 2),
        datetime.datetime(2019, 2, 3),
        datetime.datetime(2019, 2, 4),
        datetime.datetime(2019, 2, 5),
        datetime.datetime(2019, 2, 6),
    ]
    mreb = pd.Series(
        [100.0, 101, 103.02, 100.9596, 100.9596, 102.978792,
         100.0, 101, 103.02, 100.9596, 100.9596, 102.978792],
        index=dates)
    assert_series_equal(mreb, basket([mreb], [1], rebal_freq=RebalFreq.MONTHLY))
