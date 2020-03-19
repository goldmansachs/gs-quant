"""
Copyright 2018 Goldman Sachs.
Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""
from gs_quant.api.gs.monitors import GsMonitorsApi
from gs_quant.session import *
from gs_quant.target.monitor import Monitor, MonitorResponseData


def test_get_many_monitors(mocker):
    mock_response = {'results': (
        Monitor(id='abc', name='test', type='assets'),
        Monitor(id='bde', name='test2', type='assets')
    ), 'totalResults': 2}

    expected_response = (
        Monitor(id='abc', name='test', type='assets'),
        Monitor(id='bde', name='test2', type='assets')
    )

    # mock GsSession
    mocker.patch.object(GsSession.__class__, 'default_value',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_get', return_value=mock_response)

    # run test
    GsMonitorsApi.get_monitors()
    GsSession.current._get.assert_called_with('/monitors?limit=100', cls=Monitor)
    GsMonitorsApi.get_monitors(monitor_id='abc')
    GsSession.current._get.assert_called_with('/monitors?id=abc&limit=100', cls=Monitor)
    GsMonitorsApi.get_monitors(owner_id='aedf')
    GsSession.current._get.assert_called_with('/monitors?ownerId=aedf&limit=100', cls=Monitor)
    GsMonitorsApi.get_monitors(name='name')
    GsSession.current._get.assert_called_with('/monitors?name=name&limit=100', cls=Monitor)
    GsMonitorsApi.get_monitors(folder_name='folderName')
    GsSession.current._get.assert_called_with('/monitors?folderName=folderName&limit=100', cls=Monitor)
    GsMonitorsApi.get_monitors(monitor_type='type')
    GsSession.current._get.assert_called_with('/monitors?type=type&limit=100', cls=Monitor)
    response = GsMonitorsApi.get_monitors(name='name', owner_id='ia', limit=10)
    GsSession.current._get.assert_called_with('/monitors?ownerId=ia&name=name&limit=10', cls=Monitor)
    assert response == expected_response


def test_get_monitor(mocker):
    monitor_id = 'abc'
    mock_response = Monitor(id=monitor_id, name='test', type='assets')

    # mock GsSession
    mocker.patch.object(GsSession.__class__, 'default_value',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_get', return_value=mock_response)

    # run test
    response = GsMonitorsApi.get_monitor(monitor_id)
    GsSession.current._get.assert_called_with('/monitors/{id}'.format(id=monitor_id), cls=Monitor)
    assert response == mock_response


def test_create_monitor(mocker):
    monitor_id = 'abc'

    monitor = Monitor(id=monitor_id, name='test', type='assets')

    # mock GsSession
    mocker.patch.object(GsSession.__class__, 'default_value',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_post', return_value=monitor)

    # run test
    response = GsMonitorsApi.create_monitor(monitor)
    GsSession.current._post.assert_called_with('/monitors', monitor,
                                               request_headers={'Content-Type': 'application/json;charset=utf-8'},
                                               cls=Monitor)
    assert response == monitor


def test_update_monitor(mocker):
    monitor_id = 'abc'

    monitor = Monitor(id=monitor_id, name='test', type='assets')

    # mock GsSession
    mocker.patch.object(GsSession.__class__, 'default_value',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_put', return_value=monitor)

    # run test
    response = GsMonitorsApi.update_monitor(monitor)
    GsSession.current._put.assert_called_with('/monitors/{id}'.format(id=monitor_id), monitor,
                                              request_headers={'Content-Type': 'application/json;charset=utf-8'},
                                              cls=Monitor)
    assert response == monitor


def test_delete_monitor(mocker):
    monitor_id = 'abc'

    mock_response = True

    # mock GsSession
    mocker.patch.object(GsSession.__class__, 'default_value',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_delete', return_value=mock_response)

    # run test
    response = GsMonitorsApi.delete_monitor(monitor_id)
    GsSession.current._delete.assert_called_with('/monitors/{id}'.format(id=monitor_id))
    assert response == mock_response


def test_calculate_monitor(mocker):
    monitor_id = 'abc'

    calc_data = {
        'Name': {
            'value': "Multiline Retail 4",
            'metadata': {
                'tooltip': "GSS4MRET"
            }
        },
        'Last': {
            'timestamp': "2019-06-03T20:57:31.407999992Z",
            'value': 119.21,
            'formattedValue': "119.21"
        }
    }

    mock_response = MonitorResponseData(
        id=monitor_id,
        result={
            'groupName': 'some name',
            'rows': [
                {
                    'entityId': 'id',
                    'data': calc_data
                }
            ]
        }
    )

    # mock GsSession
    mocker.patch.object(GsSession.__class__, 'default_value',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_get', return_value=mock_response)

    # run test
    response = GsMonitorsApi.calculate_monitor(monitor_id)
    GsSession.current._get.assert_called_with('/monitors/{id}/data'.format(id=monitor_id), cls=MonitorResponseData)
    assert response == mock_response
