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
import base64
from itertools import chain
import json
import logging
import math
import msgpack
import time
from typing import Iterable, Optional, Union
from websockets import ConnectionClosedError, client

from gs_quant.api.risk import RiskApi
from gs_quant.risk import RiskRequest
from gs_quant.session import GsSession
from gs_quant.target.risk import APEXOptimizationRequest

_logger = logging.getLogger(__name__)


class GsRiskApi(RiskApi):

    USE_MSGPACK = False

    @classmethod
    def calc_multi(cls, requests: Iterable[RiskRequest]) -> dict:
        requests = tuple(requests)
        results = cls._exec(requests)

        if len(results) < len(requests):
            results = [RuntimeError('Missing results')] * len(requests)

        return dict(zip(requests, results))

    @classmethod
    def calc(cls, request: RiskRequest) -> Iterable:
        return cls._exec(request)

    @classmethod
    def _exec(cls, request: Union[RiskRequest, Iterable[RiskRequest]]) -> Union[Iterable, dict]:
        use_msgpack = cls.USE_MSGPACK and not isinstance(request, RiskRequest)
        return GsSession.current._post(cls.__url(request),
                                       request,
                                       timeout=181,
                                       request_headers={'Content-Type': 'application/x-msgpack'} if use_msgpack else {})

    @classmethod
    def __url(cls, request: Union[RiskRequest, Iterable[RiskRequest]]):
        is_bulk = not isinstance(request, RiskRequest)
        is_internal = any(hasattr(p.instrument, '_type') for p in
                          chain.from_iterable(r.positions for r in (request if is_bulk else (request,))))
        return '/risk{}/calculate{}'.format('-internal' if is_internal else '', '/bulk' if is_bulk else '')

    @classmethod
    async def get_results(cls, responses: asyncio.Queue, results: asyncio.Queue, timeout: Optional[int] = None):
        async def send_to_websocket(ws: client):
            while True:
                items = await cls.drain_queue_async(responses)
                if not items:
                    break

                report_ids = [i[1]['reportId'] for i in items]
                requests_by_id.update(zip(report_ids, (i[0] for i in items)))
                await asyncio.wait_for(ws.send(json.dumps(report_ids)), timeout=send_timeout)
                dispatched.update(report_ids)

            done.set_result(None)

        async def read_from_websocket(ws: client):
            run = True
            outstanding_report_ids = [i for i in requests_by_id.keys() if i not in dispatched]
            if outstanding_report_ids:
                _logger.info(f'Re-sending {len(outstanding_report_ids)} requests')
                await asyncio.wait_for(ws.send(json.dumps(outstanding_report_ids)), timeout=send_timeout)

            pending = set()
            while requests_by_id or run:
                complete, pending = await asyncio.wait((ws.recv(), done),
                                                       timeout=timeout,
                                                       return_when=asyncio.FIRST_COMPLETED)
                if done in complete:
                    complete.remove(done)
                    run = False

                if not complete:
                    continue

                result_id, status_result_str = complete.pop().result().split(';', 1)
                status, result_str = status_result_str[0], status_result_str[1:]

                if status == 'E':
                    result = RuntimeError(result_str)
                else:
                    try:
                        result = msgpack.unpackb(base64.b64decode(result_str), raw=False) if cls.USE_MSGPACK else\
                            json.loads(result_str)
                    except Exception as ee:
                        result = ee

                request = requests_by_id.pop(result_id)
                results.put_nowait((request, result))

            while pending:
                pending.pop().cancel()

        requests_by_id = {}
        dispatched = set()
        error = ''
        attempts = 0
        max_attempts = 5
        send_timeout = 30
        done = asyncio.Future()

        while attempts < max_attempts:
            if attempts > 0:
                await asyncio.sleep(math.pow(2, attempts))
                _logger.error(f'{error} error, retrying (attempt {attempts + 1} of {max_attempts})')

            try:
                async with GsSession.current._connect_websocket('/risk/calculate/results/subscribe') as ws:
                    await asyncio.wait((send_to_websocket(ws), read_from_websocket(ws)))
                    attempts = max_attempts
                    error = ''
            except ConnectionClosedError as cce:
                error = 'Connection failed: ' + str(cce)
                attempts += 1
            except asyncio.TimeoutError:
                error = 'Timed out'
                attempts = max_attempts
            except Exception as e:
                error = str(e)
                attempts = max_attempts

        if error != '':
            _logger.error(f'Fatal error: {error}')
            results.put_nowait([])

    @classmethod
    def create_pretrade_execution_optimization(cls, request: APEXOptimizationRequest) -> str:
        try:
            response = GsSession.current._post(r'/risk/execution/pretrade', request)
            _logger.info('New optimization is created with id: {}'.format(response.get("optimizationId")))
            return response
        except Exception as e:
            error = str(e)
            _logger.error(error)
            return error

    @classmethod
    def get_pretrade_execution_optimization(cls, optimization_id: str, max_attempts: int = 15):
        url = '/risk/execution/pretrade/{}/results'.format(optimization_id)
        attempts = 0
        start = time.perf_counter()
        results = {}

        while attempts < max_attempts:
            if attempts > 0:
                time.sleep(math.pow(2, attempts))
                _logger.error('Retrying (attempt {} of {})'.format(attempts, max_attempts))
            try:
                results = GsSession.current._get(url)
                if results.get('status') == 'Running':
                    attempts += 1
                else:
                    break
            except Exception as e:
                error = str(e)
                _logger.error(error)
                return error

        if results.get('status') == 'Running':
            _logger.info('Optimization is still running. Please retry fetching the results.')
            return results
        else:
            _logger.info('Optimization is fetched in {:.3f}s.'.format(time.perf_counter() - start))
            return results
