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
from gs_quant.target.common import FieldFilterMap
from gs_quant.target.coordinates import MDAPIDataQuery
from gs_quant.target.data import MarketDataVendor, DataSetEntity, DataQuery

test_coordinates = (
    MarketDataCoordinate(mkt_type='Prime', mkt_quoting_style='price', mkt_asset='335320934'),
    MarketDataCoordinate(mkt_type='IR', mkt_asset='USD', mkt_class='Swap', mkt_point=('2Y',)),
)

test_str_coordinates = (
    'Prime_335320934_.price',
    'IR_USD_Swap_2Y'
)

test_defn_dict = {'id': 'EXAMPLE_FROM_SLANG',
                  'name': 'Example DataSet',
                  'description': 'This is a test.',
                  'shortDescription': '',
                  'vendor': 'Goldman Sachs',
                  'dataProduct': 'TEST',
                  'entitlements': {'query': ['internal'],
                                   'view': ['internal', 'role:DataServiceView', 'role:DataServiceAdmin'],
                                   'upload': ['internal'],
                                   'admin': ['internal', 'role:DataServiceAdmin'],
                                   'edit': ['internal', 'role:DataServiceAdmin']},
                  'parameters': {'methodology': '',
                                 'coverage': '',
                                 'notes': '',
                                 'history': '',
                                 'frequency': '',
                                 'applyMarketDataEntitlements': False,
                                 'uploadDataPolicy': 'DEFAULT_POLICY',
                                 'logicalDb': 'STUDIO_DAILY',
                                 'symbolStrategy': 'ARCTIC_LINK',
                                 'immutable': False,
                                 'includeInCatalog': False,
                                 'coverageEnabled': True},
                  'dimensions': {'timeField': 'date',
                                 'transactionTimeField': 'updateTime',
                                 'symbolDimensions': ['assetId'],
                                 'nonSymbolDimensions': [{'field': 'price', 'column': 'PRICE'}],
                                 'measures': [{'field': 'updateTime', 'column': 'UPDATE_TIME'}],
                                 'entityDimension': 'assetId'},
                  'defaults': {'startSeconds': 2592000.0},
                  'createdById': '9eb7226166a44236905cae2913cfbd3c',
                  'createdTime': '2018-07-24T00:32:25.77Z',
                  'lastUpdatedById': '4ad8ebb6480d49e6b2e9eea9210685cf',
                  'lastUpdatedTime': '2019-10-24T14:20:13.653Z'}

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
    start = dt.datetime(2019, 1, 2, 1, 0)
    end = dt.datetime(2019, 1, 2, 1, 10)
    # mock GsSession and data response
    mocker.patch.object(GsSession.__class__, 'default_value',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_post', side_effect=[{'responses': [{'data': bond_data}]},
                                                                 {'responses': [{'data': swap_data}]},
                                                                 {'responses': [{'data': bond_data},
                                                                                {'data': swap_data}]},
                                                                 {'responses': [{'data': bond_data},
                                                                                {'data': swap_data}]}
                                                                 ])

    coord_data_result = GsDataApi.coordinates_data(coordinates=test_coordinates[0], start=start, end=end)
    assert_frame_equal(coord_data_result, bond_expected_frame)

    str_coord_data_result = GsDataApi.coordinates_data(coordinates=test_str_coordinates[1], start=start, end=end)
    assert_frame_equal(str_coord_data_result, swap_expected_frame)

    coords_data_result = GsDataApi.coordinates_data(coordinates=test_coordinates, start=start, end=end,
                                                    as_multiple_dataframes=True)
    assert len(coords_data_result) == 2
    assert_frame_equal(coords_data_result[0], bond_expected_frame)
    assert_frame_equal(coords_data_result[1], swap_expected_frame)

    GsSession.current._post.reset_mock()
    str_coords_data_result = GsDataApi.coordinates_data(coordinates=test_str_coordinates, start=start, end=end,
                                                        as_multiple_dataframes=True)
    assert len(str_coords_data_result) == 2
    assert_frame_equal(str_coords_data_result[0], bond_expected_frame)
    assert_frame_equal(str_coords_data_result[1], swap_expected_frame)
    GsSession.current._post.assert_called_once_with('/data/coordinates/query',
                                                    payload=MDAPIDataQuery(market_data_coordinates=test_coordinates,
                                                                           start_time=start,
                                                                           end_time=end,
                                                                           vendor=MarketDataVendor.Goldman_Sachs,
                                                                           format="MessagePack")
                                                    )


def test_coordinate_data_series(mocker):
    start = dt.datetime(2019, 1, 2, 1, 0)
    end = dt.datetime(2019, 1, 2, 1, 10)
    # mock GsSession and data response
    mocker.patch.object(GsSession.__class__, 'default_value',
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

    coord_data_result = GsDataApi.coordinates_data_series(coordinates=test_coordinates[0], start=start, end=end)
    assert_series_equal(coord_data_result, bond_expected_series)

    str_coord_data_result = GsDataApi.coordinates_data_series(coordinates=test_str_coordinates[1], start=start, end=end)
    assert_series_equal(str_coord_data_result, swap_expected_series)

    coords_data_result = GsDataApi.coordinates_data_series(coordinates=test_coordinates, start=start, end=end)
    assert len(coords_data_result) == 2
    assert_series_equal(coords_data_result[0], bond_expected_series)
    assert_series_equal(coords_data_result[1], swap_expected_series)

    GsSession.current._post.reset_mock()
    str_coords_data_result = GsDataApi.coordinates_data_series(coordinates=test_str_coordinates, start=start, end=end)
    assert len(str_coords_data_result) == 2
    assert_series_equal(str_coords_data_result[0], bond_expected_series)
    assert_series_equal(str_coords_data_result[1], swap_expected_series)
    GsSession.current._post.assert_called_with('/data/coordinates/query',
                                               payload=MDAPIDataQuery(market_data_coordinates=test_coordinates,
                                                                      start_time=start,
                                                                      end_time=end,
                                                                      vendor=MarketDataVendor.Goldman_Sachs,
                                                                      format="MessagePack")
                                               )


def test_coordinate_last(mocker):
    as_of = dt.datetime(2019, 1, 2, 1, 10)
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
            'time': ['2019-01-20T01:08:00Z', '2019-01-20T01:09:45Z'],
            'mktType': ['Prime', 'IR'],
            'mktAsset': ['335320934', 'USD'],
            'mktClass': [None, 'Swap'],
            'mktPoint': [None, ('2Y',)],
            'mktQuotingStyle': ['price', None],
            'value': [1.0141, 0.02592]
        }
    )

    # mock GsSession and data response
    mocker.patch.object(GsSession.__class__, 'default_value',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    GsSession.current._post = mocker.Mock(return_value=data)

    result = GsDataApi.coordinates_last(coordinates=test_coordinates, as_of=as_of, as_dataframe=True)
    assert result.equals(expected_result)

    GsSession.current._post.reset_mock()
    result_from_str = GsDataApi.coordinates_last(coordinates=test_str_coordinates, as_of=as_of, as_dataframe=True)
    assert result_from_str.equals(expected_result)
    GsSession.current._post.assert_called_once_with('/data/coordinates/query/last',
                                                    payload=MDAPIDataQuery(market_data_coordinates=test_coordinates,
                                                                           end_time=as_of,
                                                                           vendor=MarketDataVendor.Goldman_Sachs,
                                                                           format="MessagePack")
                                                    )


def test_get_coverage_api(mocker):
    test_coverage_data = {'results': [{'gsid': 'gsid1'}]}

    mocker.patch.object(ContextMeta, 'current', return_value=GsSession(Environment.QA))
    mocker.patch.object(ContextMeta.current, '_get', return_value=test_coverage_data)
    data = GsDataApi.get_coverage('MA_RANK')

    assert [{'gsid': 'gsid1'}] == data


def test_get_many_defns_api(mocker):
    test_defn = DataSetEntity.from_dict(test_defn_dict)
    mock_response = {'results': (test_defn,), 'totalResults': 1}

    expected_response = (test_defn,)

    # mock GsSession
    mocker.patch.object(GsSession.__class__, 'default_value',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_get', return_value=mock_response)

    # run test
    response = GsDataApi.get_many_definitions()
    GsSession.current._get.assert_called_with('/data/datasets?limit=100', cls=DataSetEntity)
    assert response == expected_response


def test_coordinates_converter():
    coord = GsDataApi._coordinate_from_str("A_B_C_D")
    assert str(coord) == 'A_B_C_D'

    coord = GsDataApi._coordinate_from_str("A_B_C.E")
    assert str(coord) == 'A_B_C.E'

    coord = GsDataApi._coordinate_from_str("A_B_.E")
    assert str(coord) == 'A_B_.E'

    coord = GsDataApi._coordinate_from_str("A_B_C_D;E.F")
    assert str(coord) == 'A_B_C_D;E.F'

    with pytest.raises(MqValueError, match='invalid coordinate A'):
        GsDataApi._coordinate_from_str("A")


def test_get_many_coordinates(mocker):
    coordinates = [
        {
            'id': 'MC123',
            'name': 'A_B_C_D_E.F1'
        },
        {
            'id': 'MC123',
            'name': 'A_B_C_D_E.F2'
        }
    ]
    mocker.patch.object(GsSession.__class__, 'default_value',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    GsSession.current._post = mocker.Mock(return_value={'results': coordinates})
    response = GsDataApi.get_many_coordinates(mkt_type='A', mkt_asset='B')
    assert response == ('A_B_C_D_E.F1', 'A_B_C_D_E.F2')


def test_auto_scroll_on_pages(mocker):
    response = {
        "requestId": "049de678-1480000",
        "totalPages": 5,
        "data": [
            {
                "date": "2012-01-25",
                "assetId": "MADXKSGX6921CFNF",
                "value": 1
            }
        ]
    }
    mocker.patch.object(ContextMeta, 'current', return_value=GsSession(Environment.QA))
    mocker.patch.object(ContextMeta.current, '_post', return_value=response)

    query = DataQuery(
        start_date=dt.date(2017, 1, 15),
        end_date=dt.date(2017, 1, 18),
        where=FieldFilterMap(
            currency="GBP"
        )
    )
    response = GsDataApi.get_results("test", response, query)
    assert len(response) == 5


if __name__ == "__main__":
    pytest.main(args=["test_data.py"])
