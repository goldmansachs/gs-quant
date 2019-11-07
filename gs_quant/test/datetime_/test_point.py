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


def test_point_sort_order():
    check_map = {
        'o/n': 0,  # O/N
        'Jan20': 379,  # EuroOrFraReg
        'JAN20': 379,  # EuroOrFraReg
        '1y': 365,  # RDatePartReg
        '1Y': 365,  # RDatePartReg
        '3m': 90,  # RDatePartReg
        '-1f XC': -30,  # CashFXReg
        '3x3': 90,  # FRAxReg
        'QE1-2020': 425,  # SpikeQEReg
        'JAN2021': 731,  # MMMYYYYReg
        '9JAN2021': 739,  # DDMMMYYYYReg
        '1.1y': 1.1 * 365,  # FloatingYear
        'K19': 120,  # LYYReg
        'JAN 20': 365,  # MMMYYReg
        'FFK9': 120,  # FFFutReg
        'ON GC': 0,  # RepoGCReg
        '1 Week GC': 7,  # RepoGCReg
        '1 week': 7,  # RelativeReg
        '01Jan20': 365,  # DDMMMYYReg
        '20Y;3M': 7300.0012328767125
    }

    for input, expected in check_map.items():
        day = dt.date(2019, 1, 1)
        actual = point_sort_order(input, day)
        assert expected == actual
