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
from gs_quant.api.risk import RiskApi
from gs_quant.base import Priceable
from gs_quant.markets.core import MarketDataCoordinate
from gs_quant.session import GsSession
from gs_quant.risk import CoordinatesRequest, RiskRequest, PricingContext, LiquidityRequest, LiquidityResponse, RiskModelRequest
import time
from typing import Iterable, Tuple, Union


class GsRiskApi(RiskApi):

    @classmethod
    def calc(cls, request: RiskRequest) -> Union[Iterable, str]:
        result = cls._exec(request)
        return cls._handle_results(request, result) if request.waitForResults else result['reportId']

    @classmethod
    def _exec(cls, request: RiskRequest) -> Union[Iterable, dict]:
        return GsSession.current._post(r'/risk/calculate', request)

    @classmethod
    def get_results(cls, risk_request: RiskRequest, result_id: str) -> dict:
        session = GsSession.current
        url = '/risk/calculate/{}/results'.format(result_id)
        results = {}

        while not results:
            result = session._get(url)

            if isinstance(result, list):
                results = cls._handle_results(risk_request, result)
            else:
                time.sleep(1)

        return results

    @classmethod
    def coordinates(cls, priceables: Iterable[Priceable]) -> Tuple[MarketDataCoordinate, ...]:
        coordinates_request = CoordinatesRequest(PricingContext.current.pricing_date, instruments=tuple(priceables))
        response = GsSession.current._post(r'/risk/coordinates', coordinates_request)

        return tuple(MarketDataCoordinate(
            marketDataType=r.get('marketDataType'),
            assetId=r.get('assetId'),
            pointClass=r.get('pointClass'),
            marketDataPoint=tuple(r.get('marketDataPoint', r.get('point', '')).split('_')),
            quotingStyle=r.get('field', r.get('quotingStyle')))  # TODO use 'quotingStyle' after changing risk definition in slang
            for r in response
        )

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
