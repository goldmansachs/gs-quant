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

from gs_quant.datetime import GsCalendar
from gs_quant.common import PricingLocation
from gs_quant.test.api.test_risk import set_session
from gs_quant.data import Dataset

from unittest import mock
import pandas as pd
import datetime


# Test GsCalendar initiated with single PricingLocation
@mock.patch.object(Dataset, 'get_data')
def test_gs_calendar_single(mocker):
    set_session()
    mocker.return_value = pd.DataFrame(index=[datetime.datetime(1999, 9, 12)],
                                       data={'holiday': 'Labor Day'})
    nyc = PricingLocation.NYC
    days = GsCalendar(nyc).holidays
    assert days


# Test GsCalendar initiated with tuple
@mock.patch.object(Dataset, 'get_data')
def test_gs_calendar_tuple(mocker):
    set_session()
    mocker.return_value = pd.DataFrame(index=[datetime.datetime(1999, 9, 12)],
                                       data={'holiday': 'Labor Day'})
    locs = (PricingLocation.NYC, PricingLocation.LDN)
    days = GsCalendar(locs).holidays
    assert days
