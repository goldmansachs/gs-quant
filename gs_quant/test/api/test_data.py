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
import datetime as dt

import pandas as pd
import pytest
from pandas.util.testing import assert_frame_equal, assert_series_equal

from gs_quant.api.gs.data import GsDataApi
from gs_quant.context_base import ContextMeta
from gs_quant.errors import MqValueError
from gs_quant.markets import MarketDataCoordinate
from gs_quant.session import GsSession, Environment

test_coordinates = (
    MarketDataCoordinate(mkt_type='Prime', mkt_quoting_style='price', mkt_asset='335320934'),
    MarketDataCoordinate(mkt_type='IR', mkt_asset='USD', mkt_class='Swap', mkt_point=('2Y',)),
)

test_str_coordinates = (
    'Prime_335320934_.price',
    'IR_USD_Swap_2Y'
)

bond_data = [
    {
        'mktType': 'Prime',
        'mktAsset': '335320934',
        'mktQuotingStyle': 'price',
        'price': 1.0139,
        'time': pd.to_datetime('2019-01-20T01:03:00Z')
    },
    {
        'mktType': 'Prime',
        'mktAsset': '335320934',
        'mktQuotingStyle': 'price',
        'price': 1.0141,
        'time': pd.to_datetime('2019-01-20T01:08:00Z')
    }
]

swap_data = [
    {
        'mktType': 'IR',
        'mktAsset': 'USD',
        'mktClass': 'Swap',
        'mktPoint': ('2Y',),
        'mktQuotingStyle': 'ATMRate',
        'ATMRate': 0.02592,
        'time': pd.to_datetime('2019-01-20T01:09:45Z')
    }
]

bond_expected_frame = pd.DataFrame(
    data={
        'time': [pd.to_datetime('2019-01-20T01:03:00Z'), pd.to_datetime('2019-01-20T01:08:00Z')],
        'mktType': ['Prime', 'Prime'],
        'mktAsset': ['335320934', '335320934'],
        'mktQuotingStyle': ['price', 'price'],
        'value': [1.0139, 1.0141]
    },
    index=pd.DatetimeIndex(['2019-01-20T01:03:00', '2019-01-20T01:08:00']),
)

swap_expected_frame = pd.DataFrame(
    data={
        'time': [pd.to_datetime('2019-01-20T01:09:45Z')],
        'mktType': ['IR'],
        'mktAsset': ['USD'],
        'mktClass': ['Swap'],
        'mktPoint': [('2Y',)],
        'mktQuotingStyle': ['ATMRate'],
        'value': [0.02592]
    },
    index=pd.DatetimeIndex(['2019-01-20T01:09:45']),
)


def test_coordinates_data(mocker):
    # mock GsSession and data response
    mocker.patch.object(GsSession.__class__, 'current',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_post', side_effect=[{'responses': [{'data': bond_data}]},
                                                                 {'responses': [{'data': swap_data}]},
                                                                 {'responses': [{'data': bond_data},
                                                                                {'data': swap_data}]},
                                                                 {'responses': [{'data': bond_data},
                                                                                {'data': swap_data}]}
                                                                 ])

    coord_data_result = GsDataApi.coordinates_data(coordinates=test_coordinates[0], start=dt.datetime(2019, 1, 2, 1, 0),
                                                   end=dt.datetime(2019, 1, 2, 1, 10))
    assert_frame_equal(coord_data_result, bond_expected_frame)

    str_coord_data_result = GsDataApi.coordinates_data(coordinates=test_str_coordinates[1],
                                                       start=dt.datetime(2019, 1, 2, 1, 0),
                                                       end=dt.datetime(2019, 1, 2, 1, 10))
    assert_frame_equal(str_coord_data_result, swap_expected_frame)

    coords_data_result = GsDataApi.coordinates_data(coordinates=test_coordinates, start=dt.datetime(2019, 1, 2, 1, 0),
                                                    end=dt.datetime(2019, 1, 2, 1, 10), as_multiple_dataframes=True)
    assert len(coords_data_result) == 2
    assert_frame_equal(coords_data_result[0], bond_expected_frame)
    assert_frame_equal(coords_data_result[1], swap_expected_frame)

    str_coords_data_result = GsDataApi.coordinates_data(coordinates=test_str_coordinates,
                                                        start=dt.datetime(2019, 1, 2, 1, 0),
                                                        end=dt.datetime(2019, 1, 2, 1, 10), as_multiple_dataframes=True)
    assert len(str_coords_data_result) == 2
    assert_frame_equal(str_coords_data_result[0], bond_expected_frame)
    assert_frame_equal(str_coords_data_result[1], swap_expected_frame)

    GsSession.current._post.assert_called_with('/data/coordinates/query', payload=mocker.ANY)
    assert GsSession.current._post.call_count == 4


def test_coordinate_data_series(mocker):
    # mock GsSession and data response
    mocker.patch.object(GsSession.__class__, 'current',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_post', side_effect=[{'responses': [{'data': bond_data}]},
                                                                 {'responses': [{'data': swap_data}]},
                                                                 {'responses': [{'data': bond_data},
                                                                                {'data': swap_data}]},
                                                                 {'responses': [{'data': bond_data},
                                                                                {'data': swap_data}]}
                                                                 ])

    bond_expected_series = pd.Series(index=bond_expected_frame.index, data=bond_expected_frame.value.values)
    swap_expected_series = pd.Series(index=swap_expected_frame.index, data=swap_expected_frame.value.values)

    coord_data_result = GsDataApi.coordinates_data_series(coordinates=test_coordinates[0],
                                                          start=dt.datetime(2019, 1, 2, 1, 0),
                                                          end=dt.datetime(2019, 1, 2, 1, 10))
    assert_series_equal(coord_data_result, bond_expected_series)

    str_coord_data_result = GsDataApi.coordinates_data_series(coordinates=test_str_coordinates[1],
                                                              start=dt.datetime(2019, 1, 2, 1, 0),
                                                              end=dt.datetime(2019, 1, 2, 1, 10))
    assert_series_equal(str_coord_data_result, swap_expected_series)

    coords_data_result = GsDataApi.coordinates_data_series(coordinates=test_coordinates,
                                                           start=dt.datetime(2019, 1, 2, 1, 0),
                                                           end=dt.datetime(2019, 1, 2, 1, 10))
    assert len(coords_data_result) == 2
    assert_series_equal(coords_data_result[0], bond_expected_series)
    assert_series_equal(coords_data_result[1], swap_expected_series)

    str_coords_data_result = GsDataApi.coordinates_data_series(coordinates=test_str_coordinates,
                                                               start=dt.datetime(2019, 1, 2, 1, 0),
                                                               end=dt.datetime(2019, 1, 2, 1, 10))
    assert len(str_coords_data_result) == 2
    assert_series_equal(str_coords_data_result[0], bond_expected_series)
    assert_series_equal(str_coords_data_result[1], swap_expected_series)

    GsSession.current._post.assert_called_with('/data/coordinates/query', payload=mocker.ANY)
    assert GsSession.current._post.call_count == 4


def test_coordinate_last(mocker):
    data = {'responses': [
        {'data': [
            {
                'mktType': 'Prime',
                'mktAsset': '335320934',
                'mktQuotingStyle': 'price',
                'price': 1.0141,
                'time': '2019-01-20T01:08:00Z'
            }
        ]},
        {'data': [
            {
                'mktType': 'IR',
                'mktAsset': 'USD',
                'mktClass': 'Swap',
                'mktPoint': ('2Y',),
                'mktQuotingStyle': 'ATMRate',
                'ATMRate': 0.02592,
                'time': '2019-01-20T01:09:45Z'
            }
        ]}
    ]}

    expected_result = pd.DataFrame(
        data={
            'mktType': ['Prime', 'IR'],
            'mktAsset': ['335320934', 'USD'],
            'mktClass': [None, 'Swap'],
            'mktPoint': [None, ('2Y',)],
            'mktQuotingStyle': ['price', None],
            'value': [1.0141, 0.02592]
        }
    )

    # mock GsSession and data response
    mocker.patch.object(GsSession.__class__, 'current',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    GsSession.current._post = mocker.Mock(return_value=data)

    result = GsDataApi.coordinates_last(coordinates=test_coordinates, as_of=dt.datetime(2019, 1, 2, 1, 10),
                                        as_dataframe=True)
    assert result.equals(expected_result)

    result_from_str = GsDataApi.coordinates_last(coordinates=test_str_coordinates, as_of=dt.datetime(2019, 1, 2, 1, 10),
                                                 as_dataframe=True)
    assert result_from_str.equals(expected_result)

    GsSession.current._post.assert_called_with('/data/coordinates/query/last', payload=mocker.ANY)
    assert GsSession.current._post.call_count == 2


def test_get_coverage_api(mocker):
    test_coverage_data = {'results': [{'gsid': 'gsid1'}]}

    mocker.patch.object(ContextMeta, 'current', return_value=GsSession(Environment.QA))
    mocker.patch.object(ContextMeta.current, '_get', return_value=test_coverage_data)
    data = GsDataApi.get_coverage('MA_RANK')

    assert [{'gsid': 'gsid1'}] == data


def test_coordinates_converter():
    coord = GsDataApi._coordinate_from_str("A_B_C_D")
    assert str(coord) == 'A|B|C|D|'

    coord = GsDataApi._coordinate_from_str("A_B_C.E")
    assert str(coord) == 'A|B|C||E'

    coord = GsDataApi._coordinate_from_str("A_B_.E")
    assert str(coord) == 'A|B|||E'

    coord = GsDataApi._coordinate_from_str("A_B_C_D_E.F")
    assert str(coord) == 'A|B|C|D_E|F'

    with pytest.raises(MqValueError, match='invalid coordinate A'):
        GsDataApi._coordinate_from_str("A")


if __name__ == "__main__":
    pytest.main(args=["test_data.py"])
