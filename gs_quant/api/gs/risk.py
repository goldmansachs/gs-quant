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
import datetime as dt
import json
import logging
import math
import os
import sys
import time
from socket import gaierror
from typing import Iterable, Optional, Union
import re

import msgpack
from websockets import ConnectionClosed

from gs_quant.api.risk import RiskApi
from gs_quant.errors import MqValueError
from gs_quant.risk import RiskRequest
from gs_quant.target.risk import OptimizationRequest
from gs_quant.tracing import Tracer, TracingSpan

_logger = logging.getLogger(__name__)


class WebsocketUnavailable(Exception):
    pass


class GsRiskApi(RiskApi):
    USE_MSGPACK = True
    POLL_FOR_BATCH_RESULTS = False
    WEBSOCKET_RETRY_ON_CLOSE_CODES = (1000, 1001, 1006)
    PRICING_API_VERSION = None

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
        headers = {'Content-Type': 'application/x-msgpack'} if use_msgpack else {}
        risk_session = cls.get_session()
        version = GsRiskApi.PRICING_API_VERSION or risk_session.api_version
        result, request_id = risk_session._post(f'/{version}' + cls.__url(request),
                                                request,
                                                include_version=False,
                                                request_headers=headers,
                                                timeout=181,
                                                return_request_id=True)

        for sub_request in request:
            sub_request._id = request_id

        return result

    @classmethod
    def __url(cls, request: Union[RiskRequest, Iterable[RiskRequest]]):
        is_bulk = not isinstance(request, RiskRequest)
        return '/risk/calculate{}'.format('/bulk' if is_bulk else '')

    @classmethod
    async def get_results(cls, responses: asyncio.Queue, results: asyncio.Queue,
                          timeout: Optional[int] = None, span: Optional[TracingSpan] = None) -> Optional[str]:
        if cls.POLL_FOR_BATCH_RESULTS:
            return await cls.__get_results_poll(responses, results, timeout=timeout)
        else:
            try:
                return await cls.__get_results_ws(responses, results, timeout=timeout)
            except WebsocketUnavailable:
                return await cls.__get_results_poll(responses, results, timeout=timeout)

    @classmethod
    async def __get_results_poll(cls, responses: asyncio.Queue, results: asyncio.Queue, timeout: Optional[int] = None):
        run = True
        pending_requests = {}
        end_time = dt.datetime.now() + dt.timedelta(seconds=timeout) if timeout else None

        while pending_requests or run:
            # Check for timeout
            if end_time is not None and dt.datetime.now() > end_time:
                _logger.error('Fatal error: timeout while waiting for results')
                cls.shutdown_queue_listener(results)
                return

            shutdown, items = await cls.drain_queue_async(responses, timeout=2)

            if shutdown:
                run = False

            if items:
                # ... update the pending requests ...
                pending_requests.update(((i[1]['reportId'], i[0]) for i in items))

            if not pending_requests:
                continue

            # ... poll for completed requests ...

            try:
                risk_session = cls.get_session()
                version = GsRiskApi.PRICING_API_VERSION or risk_session.api_version
                calc_results = risk_session._post(f'/{version}/risk/calculate/results/bulk',
                                                  list(pending_requests.keys()), include_version=False)

                # ... enqueue the request and result for the listener to handle ...
                for result in calc_results:
                    if 'error' in result:
                        results.put_nowait((pending_requests.pop(result['requestId']), RuntimeError(result['error'])))
                    elif 'result' in result:
                        results.put_nowait((pending_requests.pop(result['requestId']), result['result']))
            except Exception as e:
                error_str = f'Fatal error polling for results: {e}'
                _logger.error(error_str)
                cls.shutdown_queue_listener(results)
                return error_str

    @classmethod
    async def __get_results_ws(cls, responses: asyncio.Queue, results: asyncio.Queue, timeout: Optional[int] = None):
        async def handle_websocket():
            nonlocal all_requests_dispatched
            ret = ''

            try:
                # If we're re-connecting then re-send any in-flight request ids
                if pending_requests:
                    _logger.info(f'Re-subscribing {len(pending_requests)} requests')
                    await asyncio.wait_for(ws.send(json.dumps(list(pending_requests.keys()))), timeout=send_timeout)

                while pending_requests or not all_requests_dispatched:
                    # Continue while we have pending or un-dispatched requests
                    _logger.debug(f'waiting for {", ".join(pending_requests.keys())}')
                    request_listener = asyncio.ensure_future(cls.drain_queue_async(responses)) \
                        if not all_requests_dispatched else None
                    result_listener = asyncio.ensure_future(ws.recv())
                    listeners = tuple(filter(None, (request_listener, result_listener)))

                    # Wait for either a request or result
                    complete, pending = await asyncio.wait(listeners, return_when=asyncio.FIRST_COMPLETED)

                    # Check results before sending more requests. Results can be lost otherwise
                    if result_listener in complete:
                        # New results have been received
                        request_id = None
                        try:
                            raw_res = result_listener.result()
                            # Message of the form <REQUEST_ID>;<STATUS_CHAR><DATA>
                            # The status char tells us the format of the data:
                            # 'E' - an error string - encoded as utf-8 bytes
                            # 'R' - json data encoded as utf-8 string
                            # 'M' - msgpack data encoded as base64 string
                            # 'B' - msgpack data (raw binary)
                            is_bytes_response = isinstance(raw_res, bytes)
                            separator = b';' if is_bytes_response else ';'
                            # Use partition to split the byte or char sequence at the first semicolon
                            request_id_raw, _, result_data_raw = raw_res.partition(separator)
                            if is_bytes_response:
                                request_id = request_id_raw.decode()
                                status, risk_data = chr(result_data_raw[0]), result_data_raw[1:]
                            else:
                                request_id = request_id_raw
                                status, risk_data = result_data_raw[0], result_data_raw[1:]
                        except ConnectionClosed as conn_closed:
                            if conn_closed.rcvd and conn_closed.rcvd.code in cls.WEBSOCKET_RETRY_ON_CLOSE_CODES:
                                # websocket closed, but we can retry
                                if request_listener:
                                    if request_listener in complete:
                                        # WebSocket Closed on us, but had we had results just dispatched
                                        # They need subscribing so re-queue them to pick up later
                                        _, res = request_listener.result()
                                        cls.enqueue(responses, res, wait=False)
                                    else:
                                        # Conn Closed, cancelling request listener as no-one will hear the response
                                        # And we don't want to take anything from the queue
                                        request_listener.cancel()
                                # Now re-raise connection closed to be handled and potentially we'll try again
                                raise
                            status = 'E'
                            risk_data = str(conn_closed)
                        except Exception as ee:
                            status = 'E'
                            risk_data = str(ee)

                        if status == 'E':
                            # An error
                            result = RuntimeError(risk_data.decode() if isinstance(risk_data, bytes) else risk_data)
                        else:
                            # Unpack the result
                            try:
                                result = msgpack.unpackb(risk_data) if status == 'B' else msgpack.unpackb(
                                    base64.b64decode(risk_data), raw=False) if status == 'M' else json.loads(
                                    risk_data)
                            except Exception as ee:
                                result = ee
                        if request_id is None:
                            # Certain fatal websocket errors (e.g. ConnectionClosed) that are caught above will mean
                            # we have no request_id - In this case we abort and set the error on all results
                            result_listener.cancel()
                            for req in pending_requests.values():
                                results.put_nowait((req, result))
                            # Give up
                            pending_requests.clear()
                            all_requests_dispatched = True
                        else:
                            # Enqueue the request and result for the listener to handle
                            results.put_nowait((pending_requests.pop(request_id), result))
                    else:
                        result_listener.cancel()

                    if request_listener:
                        if request_listener in complete:
                            # New requests have been posted ...

                            all_requests_dispatched, items = request_listener.result()
                            if items:
                                if not all([isinstance(i[1], dict) for i in items]):
                                    error_item = next(i[1] for i in items if not isinstance(i[1], dict))
                                    raise RuntimeError(error_item[0][0][0]['errorString'])

                                # ... extract the request IDs ...
                                request_ids = [i[1]['reportId'] for i in items]

                                # ... update the pending requests ...
                                pending_requests.update(zip(request_ids, (i[0] for i in items)))

                                # ... add to our result subscription ...
                                await asyncio.wait_for(ws.send(json.dumps(request_ids)), timeout=send_timeout)

                                # ... note dispatched
                                dispatched.update(request_ids)
                        else:
                            request_listener.cancel()
            except ConnectionClosed:
                raise
            except Exception as ee:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                ret = f'{exc_type} {fname} ln:{exc_tb.tb_lineno}' + str(ee)

            return ret

        all_requests_dispatched = False
        pending_requests = {}
        dispatched = set()
        error = ''
        exc_info = None
        attempts = 0
        max_attempts = 5
        send_timeout = 30

        while attempts < max_attempts:
            if attempts > 0:
                await asyncio.sleep(math.pow(2, attempts - 1))
                _logger.error(f'{error} error, retrying (attempt {attempts + 1} of {max_attempts})')

            try:
                risk_session = cls.get_session()
                api_version = GsRiskApi.PRICING_API_VERSION or risk_session.api_version
                ws_url = f'/{api_version}/risk/calculate/results/subscribe'
                subprotocols = ["msgpack-binary"] if cls.USE_MSGPACK else None
                # we set a 50ms timeout for the websocket close to avoid manually waiting for marquee
                # to acknowledge the close and close the underlying TCP stream. We have seen delays of up to 1000ms here
                ws_close_timeout = 0.05
                async with risk_session._connect_websocket(
                        ws_url,
                        include_version=False,
                        subprotocols=subprotocols,
                        close_timeout=ws_close_timeout) as ws:
                    error = await handle_websocket()

                attempts = max_attempts
            except ConnectionClosed as cce:
                error = (f'Unexpected Connection Closed ({len(pending_requests)}/{len(dispatched)} '
                         f'request(s) still pending): {cce}')
                attempts += 1
            except asyncio.TimeoutError:
                error = 'Timed out'
                attempts = max_attempts
            except gaierror:
                raise WebsocketUnavailable()
            except Exception as e:
                error = str(e)
                exc_info = e
                attempts = max_attempts

        if error != '':
            _logger.error(f'Fatal error with websocket: {error}', exc_info=exc_info)
            span = Tracer.active_span()
            if span and span.is_recording():
                span.set_tag('error', True)
                span.log_kv({'event': 'error', 'message': error})
            cls.shutdown_queue_listener(results)
            return error

    @classmethod
    def create_pretrade_execution_optimization(cls, request: OptimizationRequest) -> str:
        try:
            response = cls.get_session()._post(r'/risk/execution/pretrade', request)
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
                results = cls.get_session()._get(url)
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

    @classmethod
    def get_liquidity_and_factor_analysis(cls,
                                          positions: list,
                                          risk_model: str,
                                          date: dt.date,
                                          currency: str = 'USD',
                                          participation_rate: float = 0.1,
                                          measures: Optional[list] = None,
                                          notional: Optional[float] = None,
                                          time_series_benchmark_ids: Optional[list] = None):
        """
        Get liquidity and factor analysis for a portfolio using the /risk/liquidity endpoint.

        :param positions: List of positions with assetId and quantity/weight
        :param risk_model: Risk model identifier (e.g., 'BARRA_EFM_USALTL', 'AXIOMA_AXUS4S')
        :param date: Analysis date
        :param currency: Currency for analysis (default: USD)
        :param participation_rate: Market participation rate (default: 0.1 = 10%)
        :param measures: List of measures to include (default: all available measures)
        :param notional: Optional reference notional
        :param time_series_benchmark_ids: Optional benchmark IDs for time series comparison
        :return: Dictionary with liquidity and factor analysis results
        """
        if measures is None:
            measures = [
                "Time Series Data",
                "Risk Buckets",
                "Factor Risk Buckets",
                "Factor Exposure Buckets",
                "Exposure Buckets"
            ]

        payload = {
            "currency": currency,
            "date": date.isoformat() if isinstance(date, dt.date) else date,
            "positions": positions,
            "participationRate": participation_rate,
            "riskModel": risk_model,
            "timeSeriesBenchmarkIds": time_series_benchmark_ids or [],
            "measures": measures
        }

        if notional is not None:
            payload["notional"] = notional

        try:
            response = cls.get_session()._post('/risk/liquidity', payload)

            if isinstance(response, dict) and 'errorMessage' in response:
                error_msg = response['errorMessage']

                asset_ids_pattern = (r'Assets with the following ids are missing in marquee:'
                                     r'\s*\[\s*([^\]]+)\s*\]')
                asset_ids_match = re.search(asset_ids_pattern, error_msg, re.IGNORECASE)
                if asset_ids_match:
                    clean_error_pattern = (r'(Assets with the following ids are missing in '
                                           r'marquee:\s*\[[^\]]+\])')
                    clean_error_line = re.search(clean_error_pattern, error_msg, re.IGNORECASE)
                    if clean_error_line:
                        clean_message = (f"ERROR: liquidity analysis failed\n"
                                         f"{clean_error_line.group(1)}")
                        _logger.error(clean_message)
                        raise MqValueError(clean_message)
                    else:
                        missing_assets = asset_ids_match.group(1).strip()
                        clean_message = (f"ERROR: liquidity analysis failed\n"
                                         f"Assets with the following ids are missing in marquee: "
                                         f"[ {missing_assets} ]")
                        _logger.error(clean_message)
                        raise MqValueError(clean_message)
                else:
                    _logger.error(f'Liquidity analysis failed: {error_msg}')
                    raise MqValueError("ERROR: liquidity analysis failed")

            _logger.info('Liquidity analysis completed successfully')
            return response
        except Exception:
            raise
