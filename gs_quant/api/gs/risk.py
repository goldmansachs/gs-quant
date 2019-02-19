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
from gs_quant.common import MarketDataCoordinate
from gs_quant.session import GsSession
from gs_quant.risk import CoordinatesRequest, Formatters, RiskRequest
import asyncio
import datetime as dt
from typing import List, Iterable


class GsRiskApi(RiskApi):

    @classmethod
    def calc(cls, request: RiskRequest, futures: RiskFutureMapping, is_async: bool, is_batch: bool):
        if is_batch:
            request.waitForResults = False
            response = cls.__exec(request)

            if is_async:
                asyncio.create_task(cls.__wait_for_results(response['reportId'], request, futures))
            else:
                asyncio.run(cls.__wait_for_results(response['reportId'], request, futures))
        elif is_async:
            request.waitForResults = True
            asyncio.create_task(cls.__run_async(request, futures))
        else:
            request.waitForResults = True
            results = cls.__exec(request)
            cls.__complete_futures(request, results, futures)

    @classmethod
    def coordinates(cls, priceables: Iterable[Priceable]) -> List[MarketDataCoordinate]:
        coordinates_request = CoordinatesRequest(dt.date.today(), instruments=priceables)
        response = GsSession.current._post(r'/risk/coordinates', coordinates_request)

        return [MarketDataCoordinate(
            marketDataType=r.get('marketDataType'),
            assetId=r.get('assetId'),
            pointClass=r.get('pointClass'),
            marketDataPoint=tuple(r.get('marketDataPoint', r.get('point', '')).split('_')),
            field=r.get('field'))
            for r in response
        ]

    @classmethod
    def __exec(cls, request: RiskRequest):
        return GsSession.current._post(r'/risk/calculate', request)

    @classmethod
    async def __run_async(cls, request: RiskRequest, futures: RiskFutureMapping):
        results = cls.__exec(request)
        cls.__complete_futures(request, results, futures)

    @classmethod
    def __complete_futures(cls, request: RiskRequest, results: Iterable, futures: RiskFutureMapping):
        for measure_idx, position_results in enumerate(results):
            formatter = Formatters.get(request.measures[measure_idx])
            for position_idx, result in enumerate(position_results):
                result = formatter(result) if formatter else result
                futures[request.measures[measure_idx]][request.positions[position_idx].instrument].set_result(result)

    @classmethod
    async def __wait_for_results(cls, results_id: str, request: RiskRequest, futures: RiskFutureMapping):
        session = GsSession.current
        results = session._get(r'/risk/calculate/{}'.format(results_id))

        while not isinstance(results, list):
            await asyncio.sleep(1)
            results = session._get(r'/risk/calculate/{}'.format(results_id))

        cls.__complete_futures(request, results, futures)
