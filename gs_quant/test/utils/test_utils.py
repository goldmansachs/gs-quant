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

import hashlib
import json
import os
import pathlib
from os.path import exists
from typing import List
from unittest import mock

import pytest

from gs_quant import datetime
from gs_quant.api.gs.risk import GsRiskApi
from gs_quant.datetime import business_day_offset
from gs_quant.json_encoder import JSONEncoder
from gs_quant.session import Environment, GsSession
from gs_quant.target.common import CompositeScenario


def _remove_unwanted(json_text):
    json_dict = json.loads(json_text)
    if "asOfTime" in json_dict:
        del json_dict["asOfTime"]
    return json_dict


def load_json_from_resource(test_file_name, json_file_name):
    with open(pathlib.Path(__file__).parents[1] / f'resources/{test_file_name}/{json_file_name}') as json_data:
        return json.load(json_data)


def mock_request(method, path, payload, test_file_name):
    queries = {
        'assetsDataGSNWithRic':
            '{"asOfTime": "2019-05-16T21:18:18.294Z", "limit": 4, "where": {"ric": ["GS.N"]}, "fields": ["ric", "id"]}',
        'assetsDataGSNWithId':
            '{"limit": 4, "fields": ["id", "ric"], "where": {"id": ["123456MW5E27U123456"]}}',
        'assetsDataSPXWithRic':
            '{"where": {"ric": [".SPX"]}, "limit": 4, "fields": ["ric", "id"]}',
        'assetsDataSPXWithId':
            '{"limit": 4, "fields": ["id", "ric"], "where": {"id": ["456123MW5E27U123456"]}}',
        'dataQueryRic':
            '{"fields": ["adjustedTradePrice"],'
            ' "format": "MessagePack", "where": {"assetId": ["123456MW5E27U123456"]}}',
        'dataQuerySPX':
            '{"fields": ["adjustedTradePrice"], "format": "MessagePack", "where": {"assetId": ["456123MW5E27U123456"]}}'
    }
    payload = _remove_unwanted(json.dumps(payload, cls=JSONEncoder) if payload else '{}')
    if method == 'GET':
        if path == '/data/datasets/TREOD':
            return load_json_from_resource(test_file_name, 'datasets_treod_response.json')
    elif method == 'POST':
        if path == '/assets/data/query':
            if payload == _remove_unwanted(queries['assetsDataGSNWithRic']) or \
                    payload == _remove_unwanted(queries['assetsDataGSNWithId']):
                return load_json_from_resource(test_file_name, 'assets_data_query_response_gsn.json')
            elif payload == _remove_unwanted(queries['assetsDataSPXWithRic']) or \
                    payload == _remove_unwanted(queries['assetsDataSPXWithId']):
                return load_json_from_resource(test_file_name, 'assets_data_query_response_spx.json')
        elif path == '/data/TREOD/query':
            if payload == _remove_unwanted(queries['dataQueryRic']):
                return load_json_from_resource(test_file_name, 'treod_query_response_gsn.json')
            elif payload == _remove_unwanted(queries['dataQuerySPX']):
                return load_json_from_resource(test_file_name, 'treod_query_response_spx.json')
    raise Exception(f'Unhandled request. Method: {method}, Path: {path}, payload: {payload} not recognized.')


gs_risk_api_exec = GsRiskApi._exec


def get_risk_request_id(requests):
    """
    This is not a formal equality of the risk request as it covers only the names of core components.  When a formal
    eq function is provided on risk_request then this should be replaced with something derived from that.
    :param requests: a collection of RiskRequests
    :type requests: tuple of RiskRequest
    :return: hash
    :rtype: str
    """
    identifier = str(len(requests))
    for request in requests:
        for pos in request.positions:
            if pos.instrument.name is None:
                raise ValueError('Positions must have names to be mocked')
        identifier += '_'
        identifier += '-'.join([pos.instrument.name for pos in request.positions])
        identifier += '-'.join([r.__repr__() for r in request.measures])
        date = request.pricing_and_market_data_as_of[0].pricing_date.strftime('%Y%b%d')
        today = business_day_offset(datetime.date.today(), 0, roll='preceding').strftime('%Y%b%d')
        identifier += 'today' if date == today else date
        if request.scenario is not None:
            if isinstance(request.scenario.scenario, CompositeScenario):
                underlying_scenarios = request.scenario.scenario.scenarios
                if any([scen.name is None for scen in underlying_scenarios]):
                    raise RuntimeError('Please provide unique names for your scenarios for testing')
                identifier += '+'.join(sorted([r.name for r in underlying_scenarios]))
            else:
                if request.scenario.scenario.name is None:
                    raise RuntimeError('Please provide unique names for your scenarios for testing')
                identifier += request.scenario.scenario.name
    return hashlib.md5(identifier.encode('utf-8')).hexdigest()


@pytest.mark.last
def test_all_cache_files_used():
    # Important that this test runs last, it asserts all the test files are used so we can cleanup unused ones
    saved_files = MockCalc.get_saved_files()
    assert [] == saved_files, 'Did you accidentally commit with save_files=True?!'

    unused_files = MockCalc.get_unused_files()
    print(unused_files)
    assert unused_files == [], 'Cleanup your unused test files!'


class MockCalc:
    __looked_at_files = {}
    __saved_files = set()

    def __init__(self, mocker, save_files=False, paths=pathlib.Path(__file__).parents[1], application='gs-quant'):
        # do not save tests with save_files = True
        self.save_files = save_files
        self.mocker = mocker
        self.paths = paths
        self.application = application

    def __enter__(self):
        if self.save_files:
            GsSession.use(Environment.PROD, None, None, application=self.application)
            self.mocker.patch.object(GsRiskApi, '_exec', side_effect=self.mock_calc_create_new_files if str(
                self.save_files).casefold() == 'new' else self.mock_calc_create_files)
        else:
            from gs_quant.session import OAuth2Session
            OAuth2Session.init = mock.MagicMock(return_value=None)
            GsSession.use(Environment.PROD, 'fake_client_id', 'fake_secret', application=self.application)
            self.mocker.patch.object(GsRiskApi, '_exec', side_effect=self.mock_calc)

    def mock_calc(self, *args, **kwargs):
        request = kwargs.get('request') or args[0]
        request_id = get_risk_request_id(request)
        file_name = f'request{request_id}.json'
        with open(self.paths / f'calc_cache/{file_name}') as json_data:
            MockCalc.__looked_at_files.setdefault(self.paths, set()).add(file_name)
            return json.load(json_data)

    def mock_calc_create_files(self, *args, **kwargs):
        # never leave a side_effect calling this function.  Call it once to create the files, check them in
        # and switch to mock_calc
        def get_json(*i_args, **i_kwargs):
            this_json = gs_risk_api_exec(*i_args, **i_kwargs)
            # Post process the json a bit to remove timing info that makes spurious diffs
            for d in [d for a in this_json for b in a for c in b for d in c]:
                for key, val in list(d.items()):
                    if val is None or key in ['queueingTime', 'calculationTime']:
                        del d[key]
            return this_json

        result_json = get_json(*args, **kwargs)
        request = kwargs.get('request') or args[0]
        request_id = get_risk_request_id(request)
        with open(self.paths / f'calc_cache/request{request_id}.json',
                  'w') as json_data:
            MockCalc.__saved_files.add(request_id)
            json.dump(result_json, json_data)

        return result_json

    def mock_calc_create_new_files(self, *args, **kwargs):
        request = kwargs.get('request') or args[0]
        request_id = get_risk_request_id(request)
        file_exists = exists(self.paths / f'calc_cache/request{request_id}.json')
        if file_exists:
            return self.mock_calc(*args, *kwargs)
        else:
            return self.mock_calc_create_files(*args, *kwargs)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @staticmethod
    def get_unused_files() -> List[str]:
        unused_files = []
        for test_path, files_used in MockCalc.__looked_at_files.items():
            for test_file in os.listdir(test_path / 'calc_cache'):
                if test_file.endswith('.json') and test_file not in files_used:
                    unused_files.append(test_file)
        return unused_files

    @staticmethod
    def get_saved_files() -> List[str]:
        return list(MockCalc.__saved_files)
