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
import pathlib
from unittest import mock

from gs_quant.api.gs.risk import GsRiskApi
from gs_quant.json_encoder import JSONEncoder
from gs_quant.markets import PricingContext
from gs_quant.session import Environment, GsSession


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
        identifier += '_'
        identifier += '-'.join([pos.instrument.name for pos in request.positions])
        identifier += '-'.join([str(risk) for risk in request.measures])
        date = request.pricing_and_market_data_as_of[0].pricing_date.strftime('%Y%b%d')
        today = PricingContext().pricing_date.strftime('%Y%b%d')
        identifier += 'today' if date == today else date
        if request.scenario is not None:
            scenario_identifier = []
            for k, v in request.scenario.scenario.as_dict().items():
                if k != 'shocks':
                    scenario_identifier.append(str(k) + "=" + str(v))
                else:
                    shock_value = 'shock_value' + "=" + str(v[0].shock.value)
                    pattern = v[0].pattern
                    shock_pattern = 'shock_pattern' + "=" + '-'.join(
                        [str(m) for m in [pattern.mkt_type, pattern.mkt_asset, pattern.mkt_class]])
                    scenario_identifier.append(shock_value + "+" + shock_pattern)
            identifier += '+'.join(sorted(scenario_identifier))
    return hashlib.md5(identifier.encode('utf-8')).hexdigest()


class MockCalc:
    def __init__(self, mocker, save_files=False, paths=pathlib.Path(__file__).parents[1], application='gs-quant'):
        # do not save tests with save_files = True
        self.save_files = save_files
        self.mocker = mocker
        self.paths = paths
        self.application = application

    def __enter__(self):
        if self.save_files:
            GsSession.use(Environment.PROD, None, None, application=self.application)
            self.mocker.patch.object(GsRiskApi, '_exec', side_effect=self.mock_calc_create_files)
        else:
            from gs_quant.session import OAuth2Session
            OAuth2Session.init = mock.MagicMock(return_value=None)
            GsSession.use(Environment.PROD, 'fake_client_id', 'fake_secret', application=self.application)
            self.mocker.patch.object(GsRiskApi, '_exec', side_effect=self.mock_calc)

    def mock_calc(self, *args, **kwargs):
        request = kwargs.get('request') or args[0]
        with open(self.paths / f'calc_cache/request{get_risk_request_id(request)}.json') \
                as json_data:
            return json.load(json_data)

    def mock_calc_create_files(self, *args, **kwargs):
        # never leave a side_effect calling this function.  Call it once to create the files, check them in
        # and switch to mock_calc
        def get_json(*i_args, **i_kwargs):
            this_json = gs_risk_api_exec(*i_args, **i_kwargs)
            return this_json

        result_json = get_json(*args, **kwargs)
        request = kwargs.get('request') or args[0]

        with open(self.paths / f'calc_cache/request{get_risk_request_id(request)}.json',
                  'w') as json_data:
            json.dump(result_json, json_data)

        return result_json

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
