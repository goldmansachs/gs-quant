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
import time
from typing import Iterable, Mapping, Union

from gs_quant.api.risk import RiskApi
from gs_quant.risk import RiskRequest, LiquidityRequest, LiquidityResponse, RiskModelRequest
from gs_quant.session import GsSession


class GsRiskApi(RiskApi):

    @classmethod
    def calc(cls, request: RiskRequest) -> Union[Iterable, str]:
        result = cls._exec(request)
        return cls._handle_results(request, result) if request.waitForResults else result['reportId']

    @classmethod
    def _exec(cls, request: RiskRequest) -> Union[Iterable, dict]:
        return GsSession.current._post(r'/risk/calculate', request)

    @classmethod
    def get_results(cls, ids_to_requests: Mapping[str, RiskRequest]) -> Mapping[str, dict]:
        session = GsSession.current
        result_ids = tuple(ids_to_requests.keys())
        num_results = len(result_ids)
        urls = {i: '/risk/calculate/{}/results'.format(i) for i in result_ids}
        results = {}

        while len(results) < num_results:
            for result_id, url in urls.items():
                if result_id in results:
                    continue

                result = session._get(url)
                if isinstance(result, list):
                    results[result_id] = cls._handle_results(ids_to_requests[result_id], result)

            time.sleep(1)

        return results

    @classmethod
    def liquidity(cls, request: LiquidityRequest) -> LiquidityResponse:
        # Pick a risk model based on positions if not provided
        if request.riskModel is None:
            position_ids = tuple(p['assetId'] for p in request.positions)
            request.riskModel = cls._suggest_risk_model(RiskModelRequest(position_ids))

        return GsSession.current._post(r'/risk/liquidity', request)

    @classmethod
    def risk_models(cls, request: RiskModelRequest):
        return GsSession.current._post(r'/risk/models', request)

    @classmethod
    def _suggest_risk_model(cls, request: RiskModelRequest):
        models = GsRiskApi.risk_models(request)['results']
        if len(models) > 0:
            return models[0]['model']
        else:
            raise ValueError('There are no valid risk models for the set of assets provided.')
