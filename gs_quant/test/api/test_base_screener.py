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

from gs_quant.api.gs.base_screener import GsBaseScreenerApi
from gs_quant.session import *
from gs_quant.target.base_screener import Screener, ScreenerRow, ScreenerColumn, ScreenerParameters


def test_get_all_screeners(mocker):
    rows = (ScreenerRow(entity_id='MA33ZVRPT84HRK5A', entity_type='index',
                        universe=True, expand=True),)

    cols1 = (ScreenerColumn(column_name='Name', entity_parameter='name'),)
    cols2 = (ScreenerColumn(column_name='BBID', entity_parameter='bbid'),)

    screener1_params = ScreenerParameters(rows=rows, columns=cols1)
    screener2_params = ScreenerParameters(rows=rows, columns=cols2)

    screener1 = Screener(name='Screener1', parameters=screener1_params)
    screener2 = Screener(name='Screener2', parameters=screener2_params)
    mock_response = {'totalResults': 2,
                     'results': (screener1, screener2)}

    expected_response = (screener1, screener2)

    # mock GsSession
    mocker.patch.object(GsSession.__class__, 'default_value',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_get', return_value=mock_response)

    # run test
    response = GsBaseScreenerApi.get_screeners()
    GsSession.current._get.assert_called_with('/data/screeners', cls=Screener)
    assert response == expected_response


def test_get_screen(mocker):
    rows = (ScreenerRow(entity_id='MA33ZVRPT84HRK5A', entity_type='index',
                        universe=True, expand=True),)
    cols = (ScreenerColumn(column_name='Name', entity_parameter='name'),)
    screener_params = ScreenerParameters(rows=rows, columns=cols)
    screener_id = 'id'

    mock_response = Screener(name='Screener', parameters=screener_params, id_=screener_id)

    # mock GsSession
    mocker.patch.object(GsSession.__class__, 'default_value',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_get', return_value=mock_response)

    # run test
    response = GsBaseScreenerApi.get_screener(screener_id)
    GsSession.current._get.assert_called_with('/data/screeners/{id}'.format(id=screener_id),
                                              cls=Screener)
    assert response == mock_response


def test_create_screener(mocker):
    rows = (ScreenerRow(entity_id='MA33ZVRPT84HRK5A', entity_type='index',
                        universe=True, expand=True),)
    cols = (ScreenerColumn(column_name='Name', entity_parameter='name'),)
    screener_params = ScreenerParameters(rows=rows, columns=cols)

    mock_input = Screener(name='Screener', parameters=screener_params, id_=None)
    mock_response = Screener(name='Screener', parameters=screener_params, id_='1')

    # mock GsSession
    mocker.patch.object(GsSession.__class__, 'default_value',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_post', return_value=mock_response)

    # run test
    response = GsBaseScreenerApi.create_screener(mock_input)
    request_headers = {'Content-Type': 'application/json;charset=utf-8'}
    GsSession.current._post.assert_called_with('/data/screeners', mock_input,
                                               request_headers=request_headers,
                                               cls=Screener)
    assert response == mock_response


def test_edit_screener(mocker):
    rows = (ScreenerRow(entity_id='MA33ZVRPT84HRK5A', entity_type='index',
                        universe=True, expand=True),)
    new_cols = (ScreenerColumn(column_name='BBID', entity_parameter='bbid'),)
    screener_params = ScreenerParameters(rows=rows, columns=new_cols)
    screener_id = 'id'

    mock_screen = Screener(name='Screener', parameters=screener_params, id_=screener_id)

    # mock GsSession
    mocker.patch.object(GsSession.__class__, 'default_value',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_put', return_value=mock_screen)

    # run test
    response = GsBaseScreenerApi.edit_screener(screener_id, mock_screen)
    request_headers = {'Content-Type': 'application/json;charset=utf-8'}
    GsSession.current._put.assert_called_with('/data/screeners/{id}'.format(id=screener_id),
                                              mock_screen,
                                              request_headers=request_headers,
                                              cls=Screener)
    assert response == mock_screen


def test_publish_to_screener(mocker):
    screener_id = 'id'
    publish_data = {'rows': [{"Name": "Obalon Therapeutics Inc",
                              "Entity ID": "ABDFDSCD"}]}

    mock_response = {
        "requestId": "",
        "timestamp": "2022-06-10T19:46:54.945Z",
        "data": [
            {
                "name": "Obalon Therapeutics Inc",
                "entityId": "ABDFDSCD",
                "active": True,
                "lastUpdatedTime": "2022-06-10T19:46:54.862Z"
            }
        ]
    }

    expected_result = [{
        "name": "Obalon Therapeutics Inc",
        "entityId": "ABDFDSCD",
        "active": True,
        "lastUpdatedTime": "2022-06-10T19:46:54.862Z"
    }]

    # mock GsSession
    mocker.patch.object(GsSession.__class__, 'default_value',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_post', return_value=mock_response)

    # run test
    response = GsBaseScreenerApi.publish_to_screener(screener_id, publish_data)
    request_headers = {'Content-Type': 'application/json;charset=utf-8'}
    GsSession.current._post.assert_called_with('/data/screeners/{id}/publish'.format(id=screener_id),
                                               publish_data,
                                               request_headers=request_headers)
    assert response == expected_result


def test_clear_screener(mocker):
    screener_id = 'id'

    mock_response = {'requestId': '1', 'timestamp': '2022-08-01T16:56:11.241Z', 'success': True}

    # mock GsSession
    mocker.patch.object(GsSession.__class__, 'default_value',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_post', return_value=mock_response)

    # run test
    response = GsBaseScreenerApi.clear_screener(screener_id)
    request_headers = {'Content-Type': 'application/json;charset=utf-8'}
    GsSession.current._post.assert_called_with('/data/screeners/{id}/clear'.format(id=screener_id),
                                               {},
                                               request_headers=request_headers)

    assert response == mock_response


def test_delete_screener(mocker):
    screener_id = 'id'
    mock_response = None

    # mock GsSession
    mocker.patch.object(GsSession.__class__, 'default_value',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_delete', return_value=mock_response)

    # run test
    response = GsBaseScreenerApi.delete_screener(screener_id)
    GsSession.current._delete.assert_called_with('/data/screeners/{id}'.format(id=screener_id))

    assert response == mock_response
