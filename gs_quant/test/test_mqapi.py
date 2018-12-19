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

from ..errors import *
from ..mqapi import API_VERSION, AppSession, _get_env_config
from requests.structures import CaseInsensitiveDict
import datetime
import json
import pytest
import requests


def test_get_env_config(env):
    config = _get_env_config(env)
    for prop in ['AppDomain', 'UserDomain', 'AuthURL']:
        assert prop in config


def test_session_start(own_session):
    own_session.start()
    profile = own_session._get_profile()
    if hasattr(own_session, 'client_id'):
        assert profile['id'] == own_session.client_id


def test_requests(shared_session):
    url = '/{}/data/WEATHER'.format(API_VERSION)
    out = shared_session.request('GET', url, {'city': 'Boston'})
    assert 'requestId' in out
    assert 'data' in out

    with pytest.raises(MqRequestError):
        shared_session.request('GET', url, {'city': 'Boston', 'foo': 'bar'})

    url += '/query'
    body = {'where': {'city': ['Boston']}}
    out = shared_session.request('POST', url, body)
    assert 'requestId' in out
    assert 'data' in out

    body['foo'] = 'bar'
    with pytest.raises(MqRequestError):
        shared_session.request('POST', url, body)


def test_requests_with_mock(mocker, env):
    expected = {'id': 'WEATHER'}

    # noinspection PyUnusedLocal
    class MockRequests:
        @staticmethod
        def auth_request(url, data, verify, **kwargs):
            return mocker.MagicMock(spec=requests.Response, status_code=200, text='{"access_token": ""}')

        @staticmethod
        def catalog_request(method, url, **kwargs):
            return mocker.MagicMock(spec=requests.Response, status_code=200, text=json.dumps(expected),
                                    headers=CaseInsensitiveDict({'content-type': 'application/json'}))

    mocker.spy(MockRequests, 'auth_request')
    mocker.patch('requests.post', side_effect=MockRequests.auth_request)
    session = AppSession('user', 'pass', env)
    session.start()
    assert MockRequests.auth_request.call_count == 1

    mocker.spy(MockRequests, 'catalog_request')
    mocker.patch('requests.Session.request', side_effect=MockRequests.catalog_request)
    catalog = session.get_data_catalog("WEATHER")
    assert MockRequests.catalog_request.call_count == 1
    assert catalog == expected


def check_catalog_entry(entry):
    props = ['id',
             'name',
             # 'description',
             # 'shortDescription',
             'vendor',
             'dataProduct',
             'fields',
             'timeField',
             # 'transactionTimeField',
             'symbolDimensions',
             'nonSymbolDimensions',
             'measures',
             'internalOnly',
             'actions',
             'immutable',
             # 'underlyingDataSet',
             'defaultStartSeconds',
             'defaultDelayMinutes',
             # 'sample',
             'parameters',
             'tags',
             'lastUpdatedTime']
    for prop in props:
        assert prop in entry


def test_get_data_catalog(shared_session):
    catalog = shared_session.get_data_catalog()
    assert len(catalog) > 30
    for x in catalog:
        check_catalog_entry(x)

    entry = shared_session.get_data_catalog('WEATHER')
    for x in catalog:
        if x['id'] == 'WEATHER':
            assert x.keys() == entry.keys()
            for k, v in x.items():
                if not isinstance(v, dict):
                    assert v == entry[k]
            break
    else:
        assert False, 'expected to find a catalog entry for WEATHER'


def test_get_coverage(shared_session):
    coverage = shared_session.get_coverage('WEATHER')
    assert coverage
    matches = [x for x in coverage if x['city'] == 'NewYorkCity']
    assert len(matches) == 1


# FIXME: mocks!
def test_build_payload(shared_session):
    raw = {
        'start': '2018-01-02',
        'end': datetime.datetime(2018, 1, 5, 9),
        'as_of_time': datetime.datetime(2018, 1, 5, 12),
        'since': datetime.datetime(2018, 1, 1, 3),
        'foo': 'hello world',
        'bar': 5
    }
    expected = {
        'where': {},
        'startDate': '2018-01-02',
        'endTime': '2018-01-05T09:00:00Z',
        'asOfTime': '2018-01-05T12:00:00Z',
        'since': '2018-01-01T03:00:00Z',
        'foo': 'hello world',
        'bar': 5
    }
    payload = shared_session._build_payload(None, **raw)
    assert payload == expected

    payload = shared_session._build_payload('query string', **raw)
    expected['where'] = 'query string'
    assert payload == expected
