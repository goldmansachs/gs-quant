"""
Copyright 2018 Goldman Sachs.
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
import json
import pickle
import threading
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import httpx
import pytest

from gs_quant.session import Environment, GsSession


def test_session_pickle():
    session = GsSession.get(Environment.PROD, 'fake_client_id', 'fake_secret')
    pk = pickle.dumps(session)
    unpk = pickle.loads(pk)
    assert unpk is not None


class _LocalSession(GsSession):
    def __init__(self, url, proxies=None):
        super().__init__(url, Environment.DEV, proxies=proxies)

    def _authenticate(self):
        self._session.headers.update({'Authorization': 'Bearer test'})

    def post_to_activity_service(self):
        pass


class _Handler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    disable_nagle_algorithm = True

    def do_GET(self):
        body = json.dumps({'auth': self.headers.get('Authorization')}).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


@pytest.fixture
def local_session():
    server = ThreadingHTTPServer(('127.0.0.1', 0), _Handler)
    server.handle_error = lambda *args: None
    threading.Thread(target=server.serve_forever, kwargs={'poll_interval': 0.05}, daemon=True).start()
    session = _LocalSession(f'http://127.0.0.1:{server.server_address[1]}')
    session.init()
    yield session
    session.close()
    server.shutdown()
    server.server_close()


def test_async_requests_across_asyncio_run_calls(local_session):
    clients = []

    async def call():
        result = await local_session.async_.get('/ping')
        clients.append(local_session._session_async)
        return result

    for _ in range(4):
        assert asyncio.run(call()) == {'auth': 'Bearer test'}

    assert len(set(map(id, clients))) == 4
    assert len(local_session._async_clients) <= 1


def test_async_with_keeps_client_of_initialised_session(local_session):
    async def run():
        clients = []
        for _ in range(3):
            async with local_session:
                await local_session.async_.get('/ping')
                clients.append(local_session._session_async)
        return clients

    clients = asyncio.run(run())
    assert clients[0] is clients[1] is clients[2]


def test_async_with_closes_client_it_created(local_session):
    session = _LocalSession(local_session.domain)

    async def run():
        async with session:
            await session.async_.get('/ping')
            client = session._session_async
        return client

    client = asyncio.run(run())
    assert client.is_closed
    assert session._session is None
    assert len(session._async_clients) == 0


def test_async_requests_from_concurrent_event_loops(local_session):
    barrier = threading.Barrier(4)

    async def call():
        await local_session.async_.get('/ping')
        barrier.wait(timeout=5)
        return local_session._session_async

    with ThreadPoolExecutor(4) as pool:
        clients = list(pool.map(lambda _: asyncio.run(call()), range(4)))

    assert len(set(map(id, clients))) == 4


def test_close_closes_async_clients_of_idle_loops(local_session):
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(local_session.async_.get('/ping'))
        client = local_session._async_clients[loop]
        local_session.close()
        assert client.is_closed
        assert len(local_session._async_clients) == 0
    finally:
        loop.close()


def test_reauthentication_updates_async_clients(local_session):
    async def run():
        await local_session.async_.get('/ping')
        local_session._session.headers['Authorization'] = 'Bearer refreshed'
        local_session._authenticate_async()
        return await local_session.async_.get('/ping')

    assert asyncio.run(run()) == {'auth': 'Bearer refreshed'}


def test_session_pickle_after_async_use(local_session):
    async def call():
        await local_session.async_.get('/ping')
        unpickled = pickle.loads(pickle.dumps(local_session))
        assert len(unpickled._async_clients) == 0
        assert len(local_session._async_clients) == 1

    asyncio.run(call())


def test_async_proxy_mounts():
    session = _LocalSession('http://127.0.0.1', proxies={'https': 'http://proxy:8080', 'http://host': 'http://p:1'})
    mounts = session._async_mounts()
    assert set(mounts) == {'https://', 'http://host'}
    assert all(isinstance(t, httpx.AsyncHTTPTransport) for t in mounts.values())
    assert _LocalSession('http://127.0.0.1')._async_mounts() is None
