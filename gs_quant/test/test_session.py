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

Portions copyright Dipesh Pandit. Licensed under Apache 2.0 license
"""

import json
import pickle
from unittest import mock

import pytest

from gs_quant.errors import MqAuthenticationError
from gs_quant.session import GsSession, Environment


def test_session_pickle():
    session = GsSession.get(Environment.PROD, 'fake_client_id', 'fake_secret')
    pk = pickle.dumps(session)
    unpk = pickle.loads(pk)
    assert unpk is not None


def _session_with_reply(status_code, text):
    session = GsSession.get(Environment.PROD, 'fake_client_id', 'fake_secret', scopes=('read_product_data',))
    reply = mock.Mock(status_code=status_code, text=text)
    session._session = mock.Mock()
    session._session.post.return_value = reply
    return session


def test_authenticate_invalid_scope_message():
    body = json.dumps({
        'error': 'invalid_scope',
        'error_description': 'The requested scope(s) must be blank or a subset of the provided scopes.',
    })
    session = _session_with_reply(400, body)

    with pytest.raises(MqAuthenticationError) as exc_info:
        session._authenticate()

    message = exc_info.value.message
    assert 'not authorized' in message
    assert 'read_product_data' in message
    # The raw OAuth error body should not leak into the friendly message
    assert 'error_description' not in message


def test_authenticate_non_scope_error_preserves_raw_text():
    body = json.dumps({'error': 'invalid_client'})
    session = _session_with_reply(401, body)

    with pytest.raises(MqAuthenticationError) as exc_info:
        session._authenticate()

    assert exc_info.value.message == body
