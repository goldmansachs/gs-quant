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

import os
import pytest
from ..mqapi import AppSession, Environment
from configparser import ConfigParser

try:
    import requests_kerberos
except ImportError:
    requests_kerberos = None


@pytest.fixture(scope='session')
def run_user_tests(request):
    return request.config.getoption("--run-user-tests")


@pytest.fixture(scope='session')
def env():
    return Environment.PROD


@pytest.fixture(scope='session')
def credentials(env):
    _config_file = os.path.dirname(__file__) + '/credentials.ini'
    try:
        open(_config_file)
    except IOError:
        pytest.skip('no credentials found for app session tests')
    config = ConfigParser()
    config.read(_config_file)
    section = env.name
    return config.get(section, 'id'), config.get(section, 'secret')


@pytest.fixture(scope='module')
def shared_session(env, credentials):
    with AppSession(credentials[0], credentials[1], env) as session:
            yield session


@pytest.fixture()
def own_session(env, credentials):
    session = AppSession(credentials[0], credentials[1], env)
    yield session
    session.finish()
