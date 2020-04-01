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
import logging
import json
import math
import time
from typing import Iterable, Mapping, Optional, Union
from websockets import ConnectionClosedError

from gs_quant.api.risk import RiskApi
from gs_quant.risk import RiskRequest
from gs_quant.session import GsSession


_logger = logging.getLogger(__name__)


class GsRiskApi(RiskApi):

    @classmethod
    def calc(cls, request: RiskRequest) -> Union[Iterable, str]:
        result = cls._exec(request)
        return cls._handle_results(request, result) if request.waitForResults else result['reportId']

    @classmethod
    def _exec(cls, request: RiskRequest) -> Union[Iterable, dict]:
        is_internal = any(hasattr(p.instrument, '_derived_type') for p in request.positions)
        url_root = '/risk-internal' if is_internal else '/risk'
        return GsSession.current._post(url_root + r'/calculate', request, timeout=180)

    @classmethod
    def __add_missing_results(cls, ids_to_requests: Mapping[str, RiskRequest], results: Mapping[str, dict], error: str):
        for result_id in ids_to_requests.keys():
            if result_id not in results:
                results[result_id] = RuntimeError(error)

    @classmethod
    def get_results(cls, ids_to_requests: Mapping[str, RiskRequest], poll: bool, timeout: Optional[int] = None)\
            -> Mapping[str, dict]:
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
                    results[result_id] = cls._handle_results(ids_to_requests[result_id], result)

            if end_time and dt.datetime.now() > end_time:
                cls.__add_missing_results(ids_to_requests, results, "Timed out")
                return results

            time.sleep(2)

        return results

    @classmethod
    def subscribe_for_results(cls, ids_to_requests: Mapping[str, RiskRequest], timeout: Optional[int] = None)\
            -> Mapping[str, dict]:

        max_attempts = 5
        send_timeout = 10
        rec_timeout = max(timeout or 0, 30)
        results = {}

        async def get_results():
            error = 'Unknown'
            attempts = 0

            async def impl():
                async with GsSession.current._connect_websocket('/risk/calculate/results/subscribe') as ws:
                    elapsed = 0
                    request_ids = [k for k in ids_to_requests.keys() if k not in results]
                    await asyncio.wait_for(ws.send(json.dumps(request_ids)), timeout=send_timeout)

                    while len(results) < len(ids_to_requests) and (timeout is None or elapsed < timeout):
                        if elapsed > 0:
                            # Send a ping
                            await asyncio.wait_for(ws.send(json.dumps([])), send_timeout)

                        try:
                            response = await asyncio.wait_for(ws.recv(), timeout=rec_timeout)
                            if response == 'true':
                                continue

                            result_parts = response.split(';')
                            result_id = result_parts[0]
                            raw_result = ';'.join(result_parts[1:])
                            result_str = raw_result[1:]
                            is_error = not raw_result.startswith(r'R[')

                            try:
                                result = RuntimeError(result_str) if is_error else\
                                    cls._handle_results(ids_to_requests[result_id], json.loads(result_str))
                            except Exception:
                                result = RuntimeError(result_str)

                            results[result_id] = result
                        except asyncio.TimeoutError:
                            elapsed += rec_timeout

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
                    attempts += 1
                except Exception as e:
                    error = str(e)
                    attempts = max_attempts

            if len(results) < len(ids_to_requests):
                cls.__add_missing_results(ids_to_requests, results, error)

        asyncio.run(get_results())

        return results
