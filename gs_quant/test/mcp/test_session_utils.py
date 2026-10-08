"""
Copyright 2026 Goldman Sachs.
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

import importlib.util
from http.cookies import SimpleCookie
from pathlib import Path

import pytest

# gs_quant.mcp's package __init__ imports fastmcp (optional); load the module
# directly so these auth-classification tests run without the optional dep.
pytest.importorskip("fastmcp")

_MODULE_PATH = Path(__file__).parent.parent.parent / "mcp" / "session_utils.py"
_spec = importlib.util.spec_from_file_location("gs_quant_mcp_session_utils", _MODULE_PATH)
session_utils = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(session_utils)


def _cookies(**values) -> SimpleCookie:
    cookie = SimpleCookie()
    for k, v in values.items():
        cookie[k] = v
    return cookie


def test_gssso_cookie_classified():
    token, auth_type = session_utils._get_auth_token_and_type(_cookies(GSSSO="abc123"), {})
    assert token == "abc123"
    assert auth_type == session_utils.AuthType.GSSSO


def test_marquee_login_cookie_classified():
    token, auth_type = session_utils._get_auth_token_and_type(_cookies(MarqueeLogin="ml1"), {})
    assert token == "ml1"
    assert auth_type == session_utils.AuthType.MARQUEE_LOGIN


def test_jwt_shaped_bearer_classified_as_jwt():
    token, auth_type = session_utils._get_auth_token_and_type(SimpleCookie(), {"Authorization": "Bearer aaa.bbb.ccc"})
    assert token == "aaa.bbb.ccc"
    assert auth_type == session_utils.AuthType.JWT


def test_bearer_without_dots_classified_as_oauth():
    token, auth_type = session_utils._get_auth_token_and_type(SimpleCookie(), {"Authorization": "Bearer abc"})
    assert token == "abc"
    assert auth_type == session_utils.AuthType.OAUTH


def test_unknown_auth():
    token, auth_type = session_utils._get_auth_token_and_type(SimpleCookie(), {})
    assert token is None
    assert auth_type == session_utils.AuthType.UNKNOWN