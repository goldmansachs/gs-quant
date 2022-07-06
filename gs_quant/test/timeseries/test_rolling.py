"""
Copyright 2022 Goldman Sachs.
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

import datetime
import pytest
import time
import numpy as np
import pandas as pd

from gs_quant.timeseries.helper import rolling_offset


class Timer:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.start = time.perf_counter()

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f'{self.name} ran in {(time.perf_counter() - self.start) * 1000:.2f}ms')


@pytest.mark.parametrize(
    "frequency,count,unit",
    [('D', 22, 'days'), ('D', 4, 'weeks'), ('D', 3, 'months'), ('D', 1, 'years'), ('S', 12, 'hours')]
)
def test_rolling_date_offset(frequency, count, unit):
    length = 1000
    values = [np.random.random() if np.random.random() > 0.1 else np.nan for _ in range(length)]
    s = pd.Series(values, index=pd.date_range(end=datetime.datetime.now(), freq=frequency, periods=length))
    offset = pd.DateOffset(**{unit: count})

    print(f'\nseries frequency: {frequency}, offset: {count}{unit}')
    with Timer('simple rolling'):
        expected = pd.Series([np.nanmean(s.loc[(s.index > idx - offset) & (s.index <= idx)]) for idx in s.index],
                             index=s.index)

    with Timer('rolling with method name'):
        a1 = rolling_offset(s, offset, np.nanmean, 'mean')
    pd.testing.assert_series_equal(expected, a1, obj="Pandas mean")

    with Timer('rolling without method name'):
        a2 = rolling_offset(s, offset, np.nanmean)
    pd.testing.assert_series_equal(expected, a2, obj="generic mean")


if __name__ == "__main__":
    pytest.main(args=["test_rolling.py", "-s"])
