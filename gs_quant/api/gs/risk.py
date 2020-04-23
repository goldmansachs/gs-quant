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
import asyncio
import datetime as dt
from itertools import chain
import logging
import json
import math
import time
from typing import Iterable, Mapping, Optional, Tuple, Union
from websockets import ConnectionClosedError

from gs_quant.api.risk import RiskApi
from gs_quant.risk import RiskRequest
from gs_quant.session import GsSession


_logger = logging.getLogger(__name__)


class GsRiskApi(RiskApi):

    @classmethod
    def calc_multi(cls, requests: Iterable[RiskRequest]) -> Tuple[Union[dict, str], ...]:
        requests = tuple(requests)
        results = cls._exec(requests)

        if len(results) < len(requests):
            raise RuntimeError('Missing results')

        return tuple(cls.__result(request, result) for request, result in zip(requests, results))

    @classmethod
    def calc(cls, request: RiskRequest) -> Union[Iterable, str]:
        return cls.__result(request, cls._exec(request))

    @classmethod
    def _exec(cls, request: Union[RiskRequest, Iterable[RiskRequest]]) -> Union[Iterable, dict]:
        return GsSession.current._post(cls.__url(request), request, timeout=180)

    @classmethod
    def __result(cls, request: RiskRequest, result: Union[Iterable, dict]) -> Union[dict, str]:
        return cls._handle_results(request, result) if request.waitForResults else result['reportId']

    @classmethod
    def __url(cls, request: Union[RiskRequest, Iterable[RiskRequest]]):
        is_bulk = not isinstance(request, RiskRequest)
        is_internal = any(hasattr(p.instrument, '_derived_type') for p in
                          chain.from_iterable(r.positions for r in (request if is_bulk else (request,))))
        return '/risk{}/calculate{}'.format('-internal' if is_internal else '', '/bulk' if is_bulk else '')

    @classmethod
    def __add_missing_results(cls,
                              ids_to_requests: Mapping[str, RiskRequest],
                              results: Mapping[RiskRequest, Union[Exception, dict]],
                              error: str):
        for request in ids_to_requests.values():
            if request not in results:
                results[request] = RuntimeError(error)

    @classmethod
    def get_results(cls, ids_to_requests: Mapping[str, RiskRequest], poll: bool, timeout: Optional[int] = None)\
            -> Mapping[RiskRequest, Union[Exception, dict]]:
        if not poll:
            return cls.subscribe_for_results(ids_to_requests, timeout=timeout)

        end_time = dt.datetime.now() + dt.timedelta(seconds=timeout) if timeout else None
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
                    results[ids_to_requests[result_id]] = cls._handle_results(ids_to_requests[result_id], result)

            if end_time and dt.datetime.now() > end_time:
                cls.__add_missing_results(ids_to_requests, results, "Timed out")
                return results

            time.sleep(2)

        return results

    @classmethod
    def subscribe_for_results(cls, ids_to_requests: Mapping[str, RiskRequest], timeout: Optional[int] = None)\
            -> Mapping[RiskRequest, Union[Exception, dict]]:

        max_attempts = 5
        send_timeout = 10
        results = {}

        async def get_results():
            error = 'Unknown'
            attempts = 0

            async def impl():
                async with GsSession.current._connect_websocket('/risk/calculate/results/subscribe') as ws:
                    request_ids = [k for k in ids_to_requests.keys() if k not in results]
                    await asyncio.wait_for(ws.send(json.dumps(request_ids)), timeout=send_timeout)

                    while len(results) < len(ids_to_requests):
                        response = await asyncio.wait_for(ws.recv(), timeout=timeout)

                        result_parts = response.split(';')
                        result_id = result_parts[0]
                        raw_result = ';'.join(result_parts[1:])
                        result_str = raw_result[1:]
                        is_error = not raw_result.startswith(r'R[')

                        try:
                            result = RuntimeError(result_str) if is_error else\
                                cls._handle_results(ids_to_requests[result_id], json.loads(result_str))
                        except json.decoder.JSONDecodeError:
                            result = RuntimeError(result_str)

                        results[ids_to_requests[result_id]] = result

            while len(results) < len(ids_to_requests) and attempts < max_attempts:
                if attempts > 0:
                    await asyncio.sleep(math.pow(2, attempts))
                    _logger.error('{} error, retrying (attempt {} of {})'.format(error, attempts + 1, max_attempts))

                try:
                    await impl()
                except ConnectionClosedError as cce:
                    error = 'Connection failed: ' + str(cce)
                    attempts += 1
                except asyncio.TimeoutError:
                    error = 'Timed out'
                    attempts = max_attempts
                except Exception as e:
                    error = str(e)
                    attempts = max_attempts

            if len(results) < len(ids_to_requests):
                cls.__add_missing_results(ids_to_requests, results, error)

        asyncio.run(get_results())

        return results
