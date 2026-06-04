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

from enum import Enum
from http.cookies import SimpleCookie
from typing import Mapping

import cachetools
from starlette.requests import Request

from gs_quant.session import GsSession, Environment

__session_cache = cachetools.LRUCache(50)


async def extract_from_starlette_request(
    http_request: Request,
    environment: Environment = Environment.PROD,
) -> tuple[dict, GsSession] | tuple[None, None]:
    cookies = SimpleCookie(http_request.cookies)
    token, auth_type = _get_auth_token_and_type(SimpleCookie(http_request.cookies), http_request.headers)
    if auth_type == AuthType.UNKNOWN:
        return None, None
    cache_key = (token, auth_type, environment)
    session_and_profile = __session_cache.get(cache_key, None)
    if session_and_profile is None:
        session = construct_session(environment, token, auth_type, application_name_override=None, cookies=cookies)
        session.init(cookies)
        user_profile = await session.async_.get('/users/self')
        __session_cache[cache_key] = (user_profile, session)
        return user_profile, session
    else:
        return session_and_profile


_local_config = {}


def set_session_config(name: str):
    _local_config['name'] = name


def get_session_application_name():
    return _local_config.get('name', 'gs-quant')


GSSSO = "GSSSO"
MARQUEE_CSRF_TOKEN = "MARQUEE-CSRF-TOKEN"
MARQUEE_LOGIN = "MarqueeLogin"
AUTHORIZATION = 'Authorization'
BEARER_PREFIX = "BEARER "


class AuthType(Enum):
    GSSSO = "GSSSO"
    OAUTH = "OAUTH"
    MARQUEE_LOGIN = "MARQUEE_LOGIN"
    JWT = "JWT"
    UNKNOWN = "UNKNOWN"


def _get_auth_token_and_type(cookies: SimpleCookie, headers: Mapping[str, str]) -> tuple[str | None, AuthType]:
    if GSSSO in cookies:
        return cookies[GSSSO].value, AuthType.GSSSO
    elif MARQUEE_LOGIN in cookies:
        return cookies[MARQUEE_LOGIN].value, AuthType.MARQUEE_LOGIN
    elif AUTHORIZATION in headers:
        authorization = headers[AUTHORIZATION]
        if authorization.upper().startswith(BEARER_PREFIX):
            token = authorization[len(BEARER_PREFIX) :]
            return token, AuthType.OAUTH
    return None, AuthType.UNKNOWN


def construct_session(realm, token, auth_type: AuthType, application_name_override=None, cookies=None):
    application_name = application_name_override or get_session_application_name()

    if auth_type == AuthType.UNKNOWN:
        raise ValueError("Unknown auth type, cannot construct session")

    return GsSession.get(
        environment_or_domain=realm,
        application=application_name,
        token=token,
        is_gssso=auth_type == AuthType.GSSSO,
        is_marquee_login=auth_type == AuthType.MARQUEE_LOGIN,
        is_jwt_login=auth_type == AuthType.JWT,
        cookies=cookies,
    )
