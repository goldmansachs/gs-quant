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

from pandas.util.testing import assert_series_equal
import numpy as np
from gs_quant.timeseries import *
from datetime import date


def test_moving_average():

    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 5),
        date(2019, 1, 6),
    ]

    x = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)

    result = moving_average(x)
    expected = pd.Series([3.0, 2.5, 8/3, 2.25, 2.4, 3.0], index=dates)
    assert_series_equal(result, expected, obj="Moving average")

    result = moving_average(x, 1)
    expected = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)
    assert_series_equal(result, expected, obj="Moving average window 1")

    result = moving_average(x, 2)
    expected = pd.Series([3.0, 2.5, 2.5, 2.0, 2.0, 4.5], index=dates)
    assert_series_equal(result, expected, obj="Moving average window 2")


def test_bollinger_bands():

    dates = [
        date(2019, 1, 1),
        date(2019, 1, 2),
        date(2019, 1, 3),
        date(2019, 1, 4),
        date(2019, 1, 5),
        date(2019, 1, 6),
    ]

    x = pd.Series([3.0, 2.0, 3.0, 1.0, 3.0, 6.0], index=dates)

    expected_low = pd.Series([np.nan, 1.085786, 1.511966, 0.335146, 0.611146, -0.346640], index=dates)
    expected_high = pd.Series([np.nan, 3.914214, 3.821367, 4.164854, 4.188854, 6.346640], index=dates)

    result = bollinger_bands(x)

    low = result[0].squeeze()
    high = result[1].squeeze()

    assert_series_equal(low, expected_low, check_names=False, check_less_precise=True, obj="Bollinger bands low")
    assert_series_equal(high, expected_high, check_names=False, check_less_precise=True, obj="Bollinger bands high")
