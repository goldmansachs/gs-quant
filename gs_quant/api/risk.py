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
from abc import ABCMeta, abstractmethod
import asyncio
import logging
import queue
import sys
from threading import Thread
from tqdm import tqdm
from typing import Iterable, Optional, Union

from gs_quant.base import RiskKey
from gs_quant.risk import ErrorValue, RiskRequest
from gs_quant.risk.result_handlers import result_handlers
from gs_quant.session import GsSession

_logger = logging.getLogger(__name__)


class RiskApi(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    async def get_results(cls, responses: asyncio.Queue, results: asyncio.Queue, timeout: Optional[int] = None):
        ...

    @classmethod
    @abstractmethod
    def calc(cls, request: RiskRequest) -> Iterable:
        ...

    @classmethod
    def calc_multi(cls, requests: Iterable[RiskRequest]) -> dict:
        return {request: cls.calc(request) for request in requests}

    @classmethod
    def __handle_queue_update(cls,
                              q: Union[queue.Queue, asyncio.Queue],
                              first: object) -> list:
        ret = first if isinstance(first, list) else [first]

        while True:
            try:
                elem = q.get_nowait()
                if isinstance(elem, list):
                    ret.extend(elem)
                else:
                    ret.append(elem)
            except (asyncio.QueueEmpty, queue.Empty):
                break

        return ret

    @classmethod
    def drain_queue(cls, q: queue.Queue) -> list:
        return cls.__handle_queue_update(q, q.get())

    @classmethod
    async def drain_queue_async(cls, q: asyncio.Queue) -> list:
        elem = await q.get()
        return cls.__handle_queue_update(q, elem)

    @classmethod
    def run(cls,
            requests: list,
            max_concurrent: int,
            progress_bar: Optional[tqdm] = None,
            timeout: Optional[int] = None) -> dict:
        def execute_requests(outstanding_requests: asyncio.Queue,
                             responses: asyncio.Queue,
                             raw_results: asyncio.Queue,
                             session: GsSession,
                             loop: asyncio.AbstractEventLoop):
            with session:
                while True:
                    requests_chunk = cls.drain_queue(outstanding_requests)
                    if requests_chunk == [None]:
                        break

                    try:
                        responses_chunk = cls.calc_multi(requests_chunk)
                        loop.call_soon_threadsafe(responses.put_nowait, list(responses_chunk.items()))
                    except Exception as e:
                        loop.call_soon_threadsafe(raw_results.put_nowait, [(r, e) for r in requests_chunk])

        async def run_async():
            is_async = not requests[0].wait_for_results
            loop = asyncio.get_event_loop()
            raw_results = asyncio.Queue()
            responses = asyncio.Queue() if is_async else raw_results
            outstanding_requests = queue.Queue()
            listener = None

            Thread(daemon=True,
                   target=execute_requests,
                   args=(outstanding_requests, responses, raw_results, GsSession.current, loop)).start()

            if is_async:
                listener = loop.create_task(cls.get_results(responses, raw_results, timeout=timeout))

            results = {}
            expected = len(requests)
            received = 0
            chunk_size = max_concurrent

            while received < expected:
                chunk_size = min(chunk_size, len(requests))
                if requests:
                    outstanding_requests.put([requests.pop(0) for _ in range(chunk_size)])

                completed = await cls.drain_queue_async(raw_results)
                if not completed:
                    break

                chunk_size = len(completed)

                for request, result in completed:
                    received += 1
                    results_by_key = cls._handle_results(request, result)
                    if progress_bar:
                        progress_bar.update(len(results_by_key))

                    results.update(results_by_key)

            outstanding_requests.put(None)
            await responses.put(None)

            if is_async:
                await listener

            return results

        if sys.version_info >= (3, 7):
            return asyncio.run(run_async())
        else:
            try:
                existing_event_loop = asyncio.get_event_loop()
            except RuntimeError:
                existing_event_loop = None

            use_existing = existing_event_loop and existing_event_loop.is_running()
            main_loop = existing_event_loop if use_existing else asyncio.new_event_loop()

            if not use_existing:
                asyncio.set_event_loop(main_loop)

            try:
                return main_loop.run_until_complete(run_async())
            except Exception:
                if not use_existing:
                    main_loop.stop()
                raise
            finally:
                if not use_existing:
                    main_loop.close()
                    asyncio.set_event_loop(None)

    @classmethod
    def _handle_results(cls, request: RiskRequest, results: Union[Iterable, Exception]) -> dict:
        formatted_results = {}

        if isinstance(results, Exception):
            date_results = [
                {'$type': 'Error', 'errorString': str(results)}] * len(request.pricing_and_market_data_as_of)
            position_results = [date_results] * len(request.positions)
            results = [position_results] * len(request.measures)

        for risk_measure, position_results in zip(request.measures, results):
            for position, date_results in zip(request.positions, position_results):
                for as_of, date_result in zip(request.pricing_and_market_data_as_of, date_results):
                    handler = result_handlers.get(date_result.get('$type'))
                    risk_key = RiskKey(
                        cls,
                        as_of.pricing_date,
                        as_of.market,
                        request.parameters,
                        request.scenario,
                        risk_measure
                    )

                    try:
                        result = handler(date_result, risk_key, position.instrument) if handler else date_result
                    except Exception as e:
                        result = ErrorValue(risk_key, str(e))
                        _logger.error(result)

                    formatted_results[(risk_key, position.instrument)] = result

        return formatted_results
