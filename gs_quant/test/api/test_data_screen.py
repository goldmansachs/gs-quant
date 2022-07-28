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
"""

from gs_quant.api.gs.data_screen import GsDataScreenApi
from gs_quant.session import *
from gs_quant.target.data_screen import AnalyticsScreen, FilterRequest, DataRow


def test_get_all_screens(mocker):
    mock_response = {'totalResults': 2,
                     'results': (
                         AnalyticsScreen(name='foo', id_='abc', filter_parameters=FilterRequest(),
                                         base_screener='base1'),
                         AnalyticsScreen(name='bar', filter_parameters=FilterRequest(name='filter1'),
                                         base_screener='base2'))}  # possibly add filters to this to test?

    expected_response = (
        AnalyticsScreen(name='foo', id_='abc', filter_parameters=FilterRequest(), base_screener='base1'),
        AnalyticsScreen(name='bar', filter_parameters=FilterRequest(name='filter1'), base_screener='base2'))

    # mock GsSession
    mocker.patch.object(GsSession.__class__, 'default_value',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_get', return_value=mock_response)

    # run test
    response = GsDataScreenApi.get_screens()
    GsSession.current._get.assert_called_with('/data/screens', cls=AnalyticsScreen)
    assert response == expected_response


def test_get_screen(mocker):
    mock_filter = FilterRequest(filters=({'type': 'Substring', 'columnName': 'Column1', 'q': 'A'},))
    screen_id = 'bar'
    mock_response = AnalyticsScreen(name='foo', id_=screen_id, base_screener="base1", filter_parameters=mock_filter)

    # mock GsSession
    mocker.patch.object(GsSession.__class__, 'default_value',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_get', return_value=mock_response)

    # run test
    response = GsDataScreenApi.get_screen(screen_id)
    GsSession.current._get.assert_called_with('/data/screens/{id}'.format(id=screen_id), cls=AnalyticsScreen)
    assert response == mock_response


def test_get_column_info(mocker):
    screen_id = 'id'
    mock_response = {'totalResults': 20,
                     'aggregations': {
                         'column_a': {'type': 'Number', 'parameters': {'min': 0.0, 'max': 1.0}},
                         'column_b': {'type': 'String', 'parameters': {}}
                     }}

    expected_response = {'column_a': {'type': 'Number', 'parameters': {'min': 0.0, 'max': 1.0}},
                         'column_b': {'type': 'String', 'parameters': {}}}

    # mock GsSession
    mocker.patch.object(GsSession.__class__, 'default_value',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_get', return_value=mock_response)

    # run test
    response = GsDataScreenApi.get_column_info(screen_id)
    GsSession.current._get.assert_called_with('/data/screens/{id}/filters'.format(id=screen_id))

    assert response == expected_response


def test_delete_screen(mocker):
    screen_id = 'id1'
    mock_response = None

    # mock GsSession
    mocker.patch.object(GsSession.__class__, 'default_value',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_delete', return_value=mock_response)

    # run test
    response = GsDataScreenApi.delete_screen(screen_id)
    GsSession.current._delete.assert_called_with('/data/screens/{id}'.format(id=screen_id))

    assert response == mock_response


def test_create_screen(mocker):
    mock_input = AnalyticsScreen(name='screen1', id_='1', filter_parameters=FilterRequest(), base_screener='base1')
    mock_response = AnalyticsScreen(name='screen1', id_='2', filter_parameters=FilterRequest(), base_screener='base1')

    # mock GsSession
    mocker.patch.object(GsSession.__class__, 'default_value',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_post', return_value=mock_response)

    # run test
    response = GsDataScreenApi.create_screen(mock_input)
    GsSession.current._post.assert_called_with('/data/screens', mock_input,
                                               request_headers={'Content-Type': 'application/json;charset=utf-8'},
                                               cls=AnalyticsScreen)

    assert response == mock_response


def test_filter_screen(mocker):
    screen_id = 'id1'
    mock_filter = FilterRequest(name='filtername', include_columns=('Name',))
    mock_response = {
        'scroll': '30s',
        'scrollId': "scrollid",
        'totalResults': 2,
        'scrollResults': 2,
        'results': (DataRow(), DataRow())
    }

    expected_response = (DataRow(), DataRow())

    # mock GsSession
    mocker.patch.object(GsSession.__class__, 'default_value',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_post', return_value=mock_response)

    # run test
    response = GsDataScreenApi.filter_screen(screen_id, mock_filter)
    GsSession.current._post.assert_called_with('/data/screens/{id}/filter'.format(id=screen_id), mock_filter,
                                               request_headers={'Content-Type': 'application/json;charset=utf-8'},
                                               cls=DataRow)

    assert response == expected_response


def test_update_screen(mocker):
    screen_id = 'id1'
    screen_input = AnalyticsScreen(name='screenname', base_screener='base1', filter_parameters=FilterRequest(),
                                   id_='id1')

    # mock GsSession
    mocker.patch.object(GsSession.__class__, 'default_value',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_put', return_value=screen_input)

    # run test
    response = GsDataScreenApi.update_screen(screen_id, screen_input)
    GsSession.current._put.assert_called_with('/data/screens/{id}'.format(id=screen_id), screen_input,
                                              request_headers={'Content-Type': 'application/json;charset=utf-8'},
                                              cls=AnalyticsScreen)
    assert response == screen_input
