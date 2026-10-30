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
Portions copyright Senanur Çetin. Licensed under Apache 2.0 license
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



def test_nested_sync_contexts_close_only_after_outer_exit(local_session):
    session = _LocalSession(local_session.domain)
    with session:
        with session:
            assert session._session is not None
        assert session._session is not None
    assert session._session is None
    assert session._context_depth == 0


def test_nested_async_contexts_close_client_only_after_outer_exit(local_session):
    session = _LocalSession(local_session.domain)

    async def run():
        async with session:
            async with session:
                assert await session.async_.get('/ping') == {'auth': 'Bearer test'}
                client = session._session_async
            assert session._session is not None
            assert session._session_async is client
            assert not client.is_closed
        assert session._session is None
        assert client.is_closed
        assert session._context_depth == 0

    asyncio.run(run())


def test_overlapping_async_contexts_close_after_last_exit(local_session):
    session = _LocalSession(local_session.domain)

    async def run():
        first_entered = asyncio.Event()
        second_entered = asyncio.Event()
        first_left = asyncio.Event()

        async def first():
            async with session:
                first_entered.set()
                await second_entered.wait()
                assert await session.async_.get('/ping') == {'auth': 'Bearer test'}
            first_left.set()

        async def second():
            await first_entered.wait()
            async with session:
                second_entered.set()
                await first_left.wait()
                assert session._session is not None
                assert await session.async_.get('/ping') == {'auth': 'Bearer test'}

        await asyncio.gather(first(), second())
        assert session._session is None
        assert session._context_depth == 0

    asyncio.run(run())


def test_nested_contexts_do_not_close_preinitialised_session(local_session):
    async def run():
        async with local_session:
            async with local_session:
                assert await local_session.async_.get('/ping') == {'auth': 'Bearer test'}
            assert local_session._session is not None
        assert local_session._session is not None
        assert local_session._context_depth == 0

    asyncio.run(run())


def test_failed_async_context_entry_restores_cleanup_ownership(local_session, monkeypatch):
    session = _LocalSession(local_session.domain)

    def fail():
        raise RuntimeError('invalid proxy configuration')

    monkeypatch.setattr(session, '_init_async', fail)
    with pytest.raises(RuntimeError, match='invalid proxy configuration'):
        asyncio.run(session._on_aenter())

    assert session._context_depth == 0
    assert session._session is None
    assert not session._close_on_outer_exit


def test_failed_nested_context_entry_preserves_outer_owner(local_session, monkeypatch):
    session = _LocalSession(local_session.domain)

    async def run():
        async with session:
            def fail():
                raise RuntimeError('could not create async client')

            monkeypatch.setattr(session, '_init_async', fail)
            with pytest.raises(RuntimeError, match='could not create async client'):
                await session._on_aenter()
            assert session._context_depth == 1
            assert session._session is not None

    asyncio.run(run())
    assert session._context_depth == 0
    assert session._session is None

def test_async_proxy_mounts():
    session = _LocalSession('http://127.0.0.1', proxies={'https': 'http://proxy:8080', 'http://host': 'http://p:1'})
    mounts = session._async_mounts()
    assert set(mounts) == {'https://', 'http://host'}
    assert all(isinstance(t, httpx.AsyncHTTPTransport) for t in mounts.values())
    assert _LocalSession('http://127.0.0.1')._async_mounts() is None


def test_async_exit_does_not_clear_new_context_during_client_close(local_session, monkeypatch):
    session = _LocalSession(local_session.domain)

    async def run():
        await session._on_aenter()
        old_client = session._session_async
        close_started = asyncio.Event()
        allow_close = asyncio.Event()
        original_close = old_client.aclose

        async def delayed_close():
            close_started.set()
            await allow_close.wait()
            await original_close()

        monkeypatch.setattr(old_client, 'aclose', delayed_close)
        old_exit = asyncio.create_task(session._on_aexit(None, None, None))
        await close_started.wait()
        try:
            await session._on_aenter()
            new_client = session._session_async
            assert new_client is not old_client
            assert session._context_depth == 1
            assert session._session is not None
            allow_close.set()
            await old_exit
            assert old_client.is_closed
            assert session._session is not None
            assert session._session_async is new_client
            assert await session.async_.get('/ping') == {'auth': 'Bearer test'}
            await session._on_aexit(None, None, None)
            assert session._session is None
        finally:
            allow_close.set()
            if not old_exit.done():
                await old_exit

    asyncio.run(run())


def test_cancelled_async_exit_still_finishes_client_close(local_session, monkeypatch):
    session = _LocalSession(local_session.domain)

    async def run():
        await session._on_aenter()
        client = session._session_async
        close_started = asyncio.Event()
        allow_close = asyncio.Event()
        original_close = client.aclose

        async def delayed_close():
            close_started.set()
            await allow_close.wait()
            await original_close()

        monkeypatch.setattr(client, 'aclose', delayed_close)
        exiting = asyncio.create_task(session._on_aexit(None, None, None))
        try:
            await asyncio.wait_for(close_started.wait(), timeout=2)
            exiting.cancel()
            with pytest.raises(asyncio.CancelledError):
                await exiting

            assert not client.is_closed
            assert session._session is None
            assert session._context_depth == 0
        finally:
            allow_close.set()

        if session._async_close_tasks:
            await asyncio.wait_for(
                asyncio.gather(*list(session._async_close_tasks)), timeout=2
            )
        assert client.is_closed
        assert not session._async_close_tasks

    asyncio.run(run())
