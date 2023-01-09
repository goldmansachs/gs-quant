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
import datetime
import hashlib
import inspect
from pathlib import Path

from gs_quant.api.gs.risk import GsRiskApi
from gs_quant.datetime import business_day_offset
from gs_quant.target.common import CompositeScenario
from gs_quant.test.utils.mock_request import MockRequest


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


class MockCalc(MockRequest):
    api = GsRiskApi
    method = '_exec'
    api_method = GsRiskApi._exec

    def __init__(self, mocker, save_files=False, paths=None, application='gs-quant'):
        super().__init__(mocker, save_files, paths, application)
        self.paths = paths if paths else \
            Path(next(filter(lambda x: x.code_context and self.__class__.__name__ in x.code_context[0],
                             inspect.stack())).filename).parents[1]

    def mock_calc_create_files(self, *args, **kwargs):
        import orjson

        # never leave a side_effect calling this function.  Call it once to create the files, check them in
        # and switch to mock_calc
        def get_json(*i_args, **i_kwargs):
            this_json = self.api_method(*i_args, **i_kwargs)
            # Post process the json a bit to remove timing info that makes spurious diffs
            for d in [d for a in this_json for b in a for c in b for d in c]:
                for key, val in list(d.items()):
                    if val is None or key in ['queueingTime', 'calculationTime']:
                        del d[key]
            return this_json

        result = get_json(*args, **kwargs)
        result_json = orjson.dumps(result,
                                   option=orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_NON_STR_KEYS | orjson.OPT_SORT_KEYS)
        request_id = self.get_request_id(args, kwargs)
        self.create_files(request_id, result_json)

        return result

    def get_request_id(self, args, kwargs):
        request = kwargs.get('request') or args[0]
        request_id = get_risk_request_id(request)
        return request_id
