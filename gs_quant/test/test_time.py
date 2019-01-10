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

from gs_quant.datetime import *


def test_time_difference_as_string():
    check_map = {
        '4 Seconds': np.timedelta64(4, 's'),
        '1 Minute 5 Seconds': np.timedelta64(65, 's'),
        '1 Year': np.timedelta64(int(SECS_IN_YEAR), 's'),
        '1 Day 1 Minute 5 Seconds': np.timedelta64(86465, 's')
    }

    for expected, input in check_map.items():
        actual = time_difference_as_string(input)
        assert expected == actual
