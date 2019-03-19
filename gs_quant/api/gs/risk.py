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
from gs_quant.api.risk import RiskFutureMapping, RiskApi
from gs_quant.base import Priceable
from gs_quant.markets.core import MarketDataCoordinate
from gs_quant.session import GsSession
from gs_quant.risk import CoordinatesRequest, Formatters, RiskRequest, PricingContext, LiquidityRequest, \
    LiquidityResponse, RiskModelRequest
from threading import Thread
import time
from typing import Iterable, Tuple


class GsRiskApi(RiskApi):

    @classmethod
    def liquidity(cls, request: LiquidityRequest) -> LiquidityResponse:
        # Pick a risk model based on positions if not provided
        if request.riskModel is None:
            position_ids = [p['assetId'] for p in request.positions]
            request.riskModel = cls._suggest_risk_model(RiskModelRequest(position_ids))

        return GsSession.current._post(r'/risk/liquidity', request)

    @classmethod
    def risk_models(cls, request: RiskModelRequest):
        return GsSession.current._post(r'/risk/models', request)

    @classmethod
    def calc(cls, request: RiskRequest, futures: RiskFutureMapping, is_async: bool, is_batch: bool):
        if is_batch:
            request.waitForResults = False
            response = cls._exec(request)
            func = cls.__wait_for_results
            args = (response['reportId'], request, tuple(futures.items()))
        else:
            request.waitForResults = True
            func = cls.__exec
            args = (request, tuple(futures.items()))

        if is_async:
            thread = Thread(target=func, args=args, daemon=True)
            thread.start()
        else:
            func(*args)

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
    def _exec(cls, request: RiskRequest):
        return GsSession.current._post(r'/risk/calculate', request)

    @classmethod
    def __exec(cls, request: RiskRequest, futures: tuple):
        results = cls._exec(request)
        cls.__complete_futures(request, results, dict(futures))

    @classmethod
    def __complete_futures(cls, request: RiskRequest, results: Iterable, futures: RiskFutureMapping):
        for measure_idx, position_results in enumerate(results):
            formatter = Formatters.get(request.measures[measure_idx])
            for position_idx, result in enumerate(position_results):
                result = formatter(result) if formatter else result
                futures[request.measures[measure_idx]][request.positions[position_idx].instrument].set_result(result)

    @classmethod
    def __wait_for_results(cls, results_id: str, request: RiskRequest, futures: tuple):
        session = GsSession.current
        url = '/risk/calculate/{}/results'.format(results_id)
        results = session._get(url)

        while not isinstance(results, list):
            time.sleep(1)
            results = session._get(url)

        cls.__complete_futures(request, results, dict(futures))

    @classmethod
    def _suggest_risk_model(cls, request: RiskModelRequest):
        models = GsRiskApi.risk_models(request)['results']
        if len(models) > 0:
            return models[0]['model']
        else:
            raise ValueError('There are no valid risk models for the set of assets provided.')
