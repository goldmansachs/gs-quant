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
from pandas.util.testing import assert_frame_equal

from gs_quant.api.gs.data import GsDataApi
from gs_quant.markets import MarketDataCoordinate
from gs_quant.risk import sort_risk

import datetime as dt
import pandas as pd

from gs_quant.session import GsSession, Environment
from gs_quant.context_base import ContextMeta

test_coordinates = (
   MarketDataCoordinate('Prime', field='price', marketDataAsset='335320934'),
   MarketDataCoordinate('IR', marketDataAsset='USD', pointClass='Swap', marketDataPoint=('2Y',),
                        quotingStyle='ATMRate'),
)


def test_coordinates_data(mocker):
    bond_data = [
        {
            'marketDataType': 'Prime',
            'marketDataAsset': '335320934',
            'field': 'price',
            'price': 1.0139,
            'time': pd.to_datetime('2019-01-20T01:03:00Z')
        },
        {
            'marketDataType': 'Prime',
            'marketDataAsset': '335320934',
            'field': 'price',
            'price': 1.0141,
            'time': pd.to_datetime('2019-01-20T01:08:00Z')
        }
    ]
    swap_data = [
        {
            'marketDataType': 'IR',
            'marketDataAsset': 'USD',
            'pointClass': 'Swap',
            'marketDataPoint': ('2Y',),
            'quotingStyle': 'ATMRate',
            'ATMRate': 0.02592,
            'time': pd.to_datetime('2019-01-20T01:09:45Z')
        }
    ]
    bond_expected_result = [
        {
            'marketDataType': 'Prime',
            'marketDataAsset': '335320934',
            'field': 'price',
            'value': 1.0139,
            'time': pd.to_datetime('2019-01-20T01:03:00Z')
        },
        {
            'marketDataType': 'Prime',
            'marketDataAsset': '335320934',
            'field': 'price',
            'value': 1.0141,
            'time': pd.to_datetime('2019-01-20T01:08:00Z')
        }
    ]
    swap_expected_result = [
        {
            'marketDataType': 'IR',
            'marketDataAsset': 'USD',
            'pointClass': 'Swap',
            'marketDataPoint': ('2Y',),
            'quotingStyle': 'ATMRate',
            'value': 0.02592,
            'time': pd.to_datetime('2019-01-20T01:09:45Z')
        }
    ]

    bond_expected_df = sort_risk(pd.DataFrame(bond_expected_result))
    bond_expected_df = bond_expected_df.set_index(pd.DatetimeIndex(bond_expected_df.time.values))

    swap_expected_df = sort_risk(pd.DataFrame(swap_expected_result))
    swap_expected_df = swap_expected_df.set_index(pd.DatetimeIndex(swap_expected_df.time.values))

    # mock GsSession
    mocker.patch.object(GsSession.__class__, 'current',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_post', side_effect=[{'responses': [{'data': bond_data}]},
                                                                 {'responses': [{'data': bond_data},
                                                                                {'data': swap_data}]}
                                                                 ])

    coord_data_result = GsDataApi.coordinates_data(coordinates=test_coordinates[0], start=dt.datetime(2019, 1, 2, 1, 0),
                                                   end=dt.datetime(2019, 1, 2, 1, 10))
    assert_frame_equal(coord_data_result, bond_expected_df)

    coords_data_result = GsDataApi.coordinates_data(coordinates=test_coordinates, start=dt.datetime(2019, 1, 2, 1, 0),
                                                    end=dt.datetime(2019, 1, 2, 1, 10), as_multiple_dataframes=True)
    assert len(coords_data_result) == 2
    assert_frame_equal(coords_data_result[0], bond_expected_df)
    assert_frame_equal(coords_data_result[1], swap_expected_df)


def test_coordinate_last(mocker):
    data = {'responses': [
        {'data': [
            {
                'marketDataType': 'Prime',
                'marketDataAsset': '335320934',
                'field': 'price',
                'price': 1.0141,
                'time': '2019-01-20T01:08:00Z'
            }
        ]},
        {'data': [
            {
                'marketDataType': 'IR',
                'marketDataAsset': 'USD',
                'pointClass': 'Swap',
                'marketDataPoint': ('2Y',),
                'quotingStyle': 'ATMRate',
                'ATMRate': 0.02592,
                'time': '2019-01-20T01:09:45Z'
            }
        ]}
    ]}

    expected_result = sort_risk(pd.DataFrame([
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
    ]))

    # mock GsSession
    mocker.patch.object(GsSession.__class__, 'current',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_post', return_value=data)

    result = GsDataApi.coordinates_last(coordinates=test_coordinates, as_of=dt.datetime(2019, 1, 2, 1, 10),
                                        as_dataframe=True)
    assert result.equals(expected_result)


def test_get_coverage_api(mocker):
    test_coverage_data = {'results': [{'gsid': 'gsid1'}]}

    mocker.patch.object(ContextMeta, 'current', return_value=GsSession(Environment.QA))
    mocker.patch.object(ContextMeta.current, '_get', return_value=test_coverage_data)
    data = GsDataApi.get_coverage('MA_RANK')

    assert [{'gsid': 'gsid1'}] == data


if __name__ == "__main__":
    pytest.main(args=["test_data.py"])
