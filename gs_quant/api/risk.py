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
from concurrent.futures import TimeoutError
import itertools
import logging
import queue
import sys
from threading import Thread
from tqdm import tqdm
from typing import Iterable, Optional, Union, Tuple

from gs_quant.base import RiskKey, Sentinel
from gs_quant.risk import ErrorValue, RiskRequest
from gs_quant.risk.result_handlers import result_handlers
from gs_quant.session import GsSession

_logger = logging.getLogger(__name__)


class RiskApi(metaclass=ABCMeta):

    __SHUTDOWN_SENTINEL = Sentinel('QueueListenerShutdown')

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
                              first: object) -> Tuple[bool, list]:
        if first is cls.__SHUTDOWN_SENTINEL:
            return True, []

        ret = [first]
        shutdown = False

        while True:
            try:
                elem = q.get_nowait()
                if elem is cls.__SHUTDOWN_SENTINEL:
                    shutdown = True
                else:
                    ret.append(elem)
            except (asyncio.QueueEmpty, queue.Empty):
                break

        return shutdown, ret

    @classmethod
    def drain_queue(cls, q: queue.Queue, timeout: Optional[int] = None) -> Tuple[bool, list]:
        try:
            return cls.__handle_queue_update(q, q.get(timeout=timeout))
        except queue.Empty:
            return False, []

    @classmethod
    async def drain_queue_async(cls, q: asyncio.Queue, timeout: Optional[int] = None) -> Tuple[bool, list]:
        try:
            elem = await asyncio.wait_for(q.get(), timeout=timeout) if timeout else await q.get()
            return cls.__handle_queue_update(q, elem)
        except TimeoutError:
            return False, []

    @classmethod
    def enqueue(cls,
                q: Union[queue.Queue, asyncio.Queue],
                items: Iterable,
                loop: Optional[asyncio.AbstractEventLoop] = None,
                wait: Optional[bool] = False):
        try:
            iter(items)
        except TypeError:
            items = (items,)

        put = q.put if wait else q.put_nowait

        for item in items:
            if loop:
                loop.call_soon_threadsafe(put, item)
            else:
                put(item)

    @classmethod
    def shutdown_queue_listener(cls,
                                q: Union[queue.Queue, asyncio.Queue],
                                loop: Optional[asyncio.AbstractEventLoop] = None):
        if loop:
            loop.call_soon_threadsafe(q.put_nowait, cls.__SHUTDOWN_SENTINEL)
        else:
            q.put_nowait(cls.__SHUTDOWN_SENTINEL)

    @classmethod
    def run(cls,
            requests: list,
            results: queue.Queue,
            max_concurrent: int,
            progress_bar: Optional[tqdm] = None,
            timeout: Optional[int] = None):
        def _process_results(completed: list):
            chunk_results = tuple(itertools.chain.from_iterable(cls._handle_results(request, result).items()
                                                                for request, result in completed))
            cls.enqueue(results, chunk_results, wait=True)

        def process_results(unprocessed_results: queue.Queue):
            shutdown = False

            while not shutdown:
                shutdown, completed = cls.drain_queue(unprocessed_results)
                _process_results(completed)

        def execute_requests(outstanding_requests: queue.Queue,
                             responses: asyncio.Queue,
                             raw_results: asyncio.Queue,
                             session: GsSession,
                             loop: asyncio.AbstractEventLoop):
            with session:
                shutdown = False
                while not shutdown:
                    shutdown, requests_chunk = cls.drain_queue(outstanding_requests)
                    if requests_chunk:
                        try:
                            # Get the responses for our requests chunk
                            responses_chunk = cls.calc_multi(requests_chunk)

                            # Enqueue the replies for either the result subscriber (if async requests) or directly
                            cls.enqueue(responses, responses_chunk.items(), loop=loop)
                        except Exception as e:
                            # Enqueue the error as a reply
                            cls.enqueue(raw_results, ((r, e) for r in requests_chunk), loop=loop)

                if responses != raw_results:
                    # If we are in async mode, indicate to the result subscriber that there are no more requests
                    cls.shutdown_queue_listener(responses, loop=loop)

        async def run_async():
            def num_risk_keys(request: RiskRequest):
                return len(request.pricing_and_market_data_as_of) * len(request.positions) * len(request.measures)

            is_async = not requests[0].wait_for_results
            loop = asyncio.get_event_loop()
            raw_results = asyncio.Queue()
            responses = asyncio.Queue() if is_async else raw_results
            outstanding_requests = queue.Queue()
            unprocessed_results = None
            results_handler = None

            # The requests library (which we use for dispatching) is not async, so we need a thread for concurrency
            Thread(daemon=True,
                   target=execute_requests,
                   args=(outstanding_requests, responses, raw_results, GsSession.current, loop)).start()

            if is_async:
                # If async we need a task to handle result subscription
                results_handler = loop.create_task(cls.get_results(responses, raw_results, timeout=timeout))

            expected = sum(num_risk_keys(r) for r in requests)
            received = 0
            chunk_size = min(max_concurrent, expected)
            result_thread = None

            if expected > chunk_size:
                # Result handling can occur while we're blocked on I/O
                unprocessed_results = queue.Queue()
                result_thread = Thread(daemon=True, target=process_results, args=(unprocessed_results,))
                result_thread.start()

            while received < expected:
                if requests:
                    # Enqueue requests for dispatch
                    dispatch_risk_keys = 0
                    dispatch_requests = []
                    while requests and dispatch_risk_keys < chunk_size:
                        dispatch_request = requests.pop()
                        dispatch_requests.append(dispatch_request)
                        dispatch_risk_keys += num_risk_keys(dispatch_request)

                    cls.enqueue(outstanding_requests, dispatch_requests, loop=loop)

                # Wait for results
                shutdown, completed = await cls.drain_queue_async(raw_results)
                if shutdown:
                    # Only happens on error
                    break

                # Enable as many new requests as we've received results, to keep the outstanding number constant
                chunk_received = sum(num_risk_keys(request) for request, _ in completed)
                chunk_size = min(chunk_received, expected - received)

                if progress_bar:
                    progress_bar.update(chunk_received)
                    progress_bar.refresh()

                received += chunk_received

                # Handle the results
                if unprocessed_results is not None:
                    cls.enqueue(unprocessed_results, completed)
                else:
                    _process_results(completed)

            cls.shutdown_queue_listener(outstanding_requests)

            if results_handler:
                await results_handler

            if progress_bar:
                progress_bar.close()

            if result_thread is not None:
                cls.shutdown_queue_listener(unprocessed_results)
                result_thread.join()

            cls.shutdown_queue_listener(results)

            if result_thread is not None:
                cls.shutdown_queue_listener(unprocessed_results)
                result_thread.join()

            cls.shutdown_queue_listener(results)

        if sys.version_info >= (3, 7):
            asyncio.run(run_async())
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
                main_loop.run_until_complete(run_async())
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
                        result = handler(date_result, risk_key, position.instrument,
                                         request_id=getattr(request, '_id', None)) if handler else date_result
                    except Exception as e:
                        result = ErrorValue(risk_key, str(e))
                        _logger.error(result)

                    formatted_results[(risk_key, position.instrument)] = result

        return formatted_results
