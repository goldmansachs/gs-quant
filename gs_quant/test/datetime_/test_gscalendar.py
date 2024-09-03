"""
Copyright 2021 Goldman Sachs.
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

import datetime as dt
from unittest import mock

import pandas as pd

from gs_quant.common import PricingLocation
from gs_quant.data import Dataset
from gs_quant.datetime import GsCalendar
from gs_quant.test.api.test_risk import set_session

MOCK_HOLIDAY = pd.DataFrame(index=[dt.datetime(1999, 9, 12)], data={'holiday': 'Labor Day'})


# Test GsCalendar initiated with single PricingLocation
@mock.patch.object(Dataset, 'get_coverage', return_value=pd.DataFrame())
@mock.patch.object(Dataset, 'get_data', return_value=MOCK_HOLIDAY)
def test_gs_calendar_single(mocker, _mocker_cov):
    set_session()
    nyc = PricingLocation.NYC
    GsCalendar.reset()
    days = GsCalendar(nyc).holidays
    assert days


# Test GsCalendar initiated with tuple
@mock.patch.object(Dataset, 'get_coverage', return_value=pd.DataFrame())
@mock.patch.object(Dataset, 'get_data', return_value=MOCK_HOLIDAY)
def test_gs_calendar_tuple(mocker, _mocker_cov):
    set_session()
    locs = (PricingLocation.NYC, PricingLocation.LDN)
    days = GsCalendar(locs).holidays
    assert days
