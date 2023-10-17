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

import concurrent
import socket
from concurrent.futures.thread import ThreadPoolExecutor
from typing import List, Callable, Optional

import requests
from opentracing import Span

from gs_quant.data import DataContext
from gs_quant.errors import MqUninitialisedError
from gs_quant.session import GsSession
from gs_quant.tracing import Tracer


def handle_proxy(url, params):
    try:
        internal = GsSession.current.is_internal()
    except MqUninitialisedError:
        internal = False
    if internal or socket.getfqdn().split('.')[-2:] == ['gs', 'com']:
        try:
            import gs_quant_auth
            proxies = gs_quant_auth.__proxies__
            response = requests.get(url, params=params, proxies=proxies)
        except ModuleNotFoundError:
            raise RuntimeError('You must install gs_quant_auth to be able to use this endpoint')
    else:
        response = requests.get(url, params=params)
    return response


class ThreadPoolManager:
    __executor: ThreadPoolExecutor = None

    @classmethod
    def initialize(cls, max_workers: int):
        cls.__executor = ThreadPoolExecutor(max_workers=max_workers)

    @classmethod
    def run_async(cls, tasks: List[Callable]) -> List:
        if not cls.__executor:
            cls.__executor = ThreadPoolExecutor()

        tasks_to_idx = {}
        for i, task in enumerate(tasks):
            tasks_to_idx[cls.__executor.submit(cls.__run,
                                               GsSession.current,
                                               DataContext.current,
                                               Tracer.get_instance().active_span,
                                               task)] = i
        results = [None] * len(tasks_to_idx)
        for task in concurrent.futures.as_completed(tasks_to_idx):
            idx = tasks_to_idx[task]
            results[idx] = task.result()

        return results

    @staticmethod
    def __run(session, data_context, span: Optional[Span], func):
        if span:
            Tracer.get_instance().scope_manager.activate(span, finish_on_close=False)

        with session:
            with data_context:
                return func()
