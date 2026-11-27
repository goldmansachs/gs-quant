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

Portions copyright Kwangbeom Choi. Licensed under Apache 2.0 license
"""

import datetime as dt

import pandas as pd

from gs_quant.backtests.data_sources import GenericDataSource, MissingDataStrategy


def date_indexed_series():
    # ten business days with a weekend gap between Jan 5 and Jan 8
    dates = [dt.date(2024, 1, d) for d in (2, 3, 4, 5, 8, 9, 10, 11, 12, 15)]
    values = [100.0, 101, 102, 103, 104, 105, 106, 107, 108, 109]
    return pd.Series(values, index=dates)


def test_missing_date_fill_forward_date_index():
    # a missing date must fill forward from the preceding date,
    # not from the last value of the whole series
    source = GenericDataSource(date_indexed_series(), MissingDataStrategy.fill_forward)
    assert source.get_data(dt.date(2024, 1, 6)) == 103.0


def test_missing_date_fill_forward_datetime_index():
    series = date_indexed_series()
    series.index = pd.DatetimeIndex([pd.Timestamp(d) for d in series.index])
    source = GenericDataSource(series, MissingDataStrategy.fill_forward)
    assert source.get_data(dt.date(2024, 1, 6)) == 103.0


def test_missing_date_interpolate_date_index():
    # interpolation must use the neighbouring dates around the gap
    source = GenericDataSource(date_indexed_series(), MissingDataStrategy.interpolate)
    assert source.get_data(dt.date(2024, 1, 6)) == 103.5


def test_present_date_lookup_unchanged():
    source = GenericDataSource(date_indexed_series(), MissingDataStrategy.fill_forward)
    assert source.get_data(dt.date(2024, 1, 15)) == 109.0
    assert source.get_data(dt.date(2024, 1, 2)) == 100.0
