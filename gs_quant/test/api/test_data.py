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

from gs_quant.api.gs.data import GsDataApi
from gs_quant.markets import MarketDataCoordinate

import datetime as dt
import pandas as pd
from unittest import mock

from gs_quant.session import GsSession, Environment
from gs_quant.context_base import ContextMeta

test_coordinates = (
   MarketDataCoordinate('Prime', field='price', marketDataAsset='335320934'),
   MarketDataCoordinate('IR', marketDataAsset='USD', pointClass='Swap', marketDataPoint=('2Y',)),
)

test_prime_data =[
    {
        'marketDataType': 'Prime',
        'marketDataAsset': '335320934',
        'field': 'price',
        'price': 1.0139,
        'time': '2019-01-2T01:03:00Z'
    },
    {
        'marketDataType': 'Prime',
        'marketDataAsset': '335320934',
        'field': 'price',
        'price': 1.0140,
        'time': '2019-01-2T01:04:30Z'
    },
    {
        'marketDataType': 'Prime',
        'marketDataAsset': '335320934',
        'field': 'price',
        'price': 1.0141,
        'time': '2019-01-2T01:08:00Z'
    }
]

test_coordinate_last_data = [
    {
        'marketDataType': 'Prime',
        'marketDataAsset': '335320934',
        'field': 'price',
        'price': 1.0141,
        'time': '2019-01-2T01:08:00Z'
    },
    {
        'marketDataType': 'IR',
        'marketDataAsset': 'USD',
        'pointClass': 'Swap',
        'marketDataPoint': ('2Y',),
        'quotingStyle': 'ATMRate',
        'ATMRate': 0.02592,
        'time': '2019-01-2T01:09:45Z'
    }
]

test_coordinate_last_df = pd.DataFrame([
    {
        'field': 'price',
        'marketDataAsset': '335320934',
        'marketDataType': 'Prime',
        'value': 1.0141
    },
    {
        'quotingStyle': 'ATMRate',
        'marketDataAsset': 'USD',
        'marketDataType': 'IR',
        'marketDataPoint': ('2Y',),
        'pointClass': 'Swap',
        'value': 0.02592
    }
])

test_coverage_data = {'results': [{'gsid': 'gsid1'}]}


@mock.patch.object(GsDataApi, 'query_data')
def test_coordinate_data(mocker):
    mocker.return_value = test_prime_data
    data = GsDataApi.coordinates_data(coordinates=(test_coordinates[0],), start=dt.datetime(2019, 1, 2, 1, 0), end=dt.datetime(2019, 1, 2, 1, 10))

    assert data.equals(pd.DataFrame(test_prime_data))


@mock.patch.object(GsDataApi, 'last_data')
def test_coordinate_last(mocker):
    mocker.return_value = test_coordinate_last_data
    data = GsDataApi.coordinates_last(coordinates=test_coordinates, as_of=dt.datetime(2019, 1, 2, 1, 10), as_dataframe=True)

    expected = test_coordinate_last_df.copy()
    del expected['quotingStyle']

    assert data.equals(expected)


def test_get_coverage_api(mocker):
    mocker.patch.object(ContextMeta, 'current', return_value=GsSession(Environment.QA))
    mocker.patch.object(ContextMeta.current, '_get', return_value=test_coverage_data)
    data = GsDataApi.get_coverage('MA_RANK')

    assert [{'gsid': 'gsid1'}] == data

