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

import backoff
import inspect
import itertools
import json
import os
import requests

from abc import abstractmethod
from configparser import ConfigParser
from enum import Enum, auto, unique
from typing import Optional, Tuple, Union


from gs_quant.api.base import Base
from gs_quant.context_base import ContextBase
from gs_quant.errors import MqError, MqRequestError, MqAuthenticationError
from gs_quant.json_encoder import JSONEncoder

API_VERSION = 'v1'
DEFAULT_APPLICATION = 'gs-quant'


@unique
class Environment(Enum):
    DEV = auto()
    QA = auto()
    PROD = auto()


class GsSession(ContextBase):

    __sessions = {}
    __config = None

    def __init__(self, domain: str, api_version: str=API_VERSION, application: str=DEFAULT_APPLICATION):
        super().__init__()
        self._session = None
        self.domain = domain
        self.api_version = api_version
        self.application = application

    @backoff.on_exception(lambda: backoff.expo(factor=2),
                          (requests.exceptions.HTTPError, requests.exceptions.Timeout),
                          max_tries=5)
    @backoff.on_predicate(lambda: backoff.expo(factor=2),
                          lambda x: x.status_code in (500, 502, 503, 504),
                          max_tries=5)
    @abstractmethod
    def _authenticate(self):
        raise NotImplementedError("Must implement __authenticate")

    @abstractmethod
    def endpoints_and_definitions(self, service):
        raise NotImplementedError("Must implement endpoints_and_definitions")

    @abstractmethod
    def request_response_gen(self, endpoint_definition):
        raise NotImplementedError("Must implement request_response_gen")

    def _on_enter(self):
        self.__close_on_exit = self._session is None
        if not self._session:
            self.init()

    def _on_exit(self, exc_type, exc_val, exc_tb):
        if self.__close_on_exit:
            self._session = None

    def init(self):
        if not self._session:
            self._session = requests.Session()
            self._session.verify = True
            self._session.headers.update({'X-Application': self.application})
            self._authenticate()

    def __request(self, method: str, path: str, payload: Optional[Union[dict, str, Base]]=None, cls: Optional[type]=None) -> Union[list, dict]:
        payload = payload or {}
        url = '{}{}{}'.format(self.domain, '/' + self.api_version, path)

        kwargs = {}
        if method in ['GET', 'DELETE']:
            kwargs['params'] = payload
        elif method in ['POST', 'PUT']:
            headers = self._session.headers.copy()
            headers.update({'Content-Type': 'application/json'})
            kwargs['headers'] = headers
            if payload:
                kwargs['data'] = payload if isinstance(payload, str) else json.dumps(payload, cls=JSONEncoder)
        else:
            raise MqError('not implemented')

        response = self._session.request(method, url, **kwargs)
        if not 199 < response.status_code < 300:
            raise MqRequestError(response.status_code, response.text, context='{} {}'.format(method, url))
        elif 'application/json' in response.headers['content-type']:
            dct = json.loads(response.text)
            return cls(**dct) if cls else dct
        else:
            return {'raw': response}

    def _get(self, path: str, payload: Optional[Union[dict, Base]]=None, cls: Optional[type]=None) -> Union[dict, str]:
        return self.__request('GET', path, payload=payload, cls=cls)

    def _post(self, path: str, payload: Optional[Union[dict, Base]]=None, cls: Optional[type]=None) -> Union[dict, str]:
        return self.__request('POST', path, payload=payload, cls=cls)

    def _delete(self, path: str, payload: Optional[Union[dict, Base]]=None, cls: Optional[type]=None) -> Union[dict, str]:
        return self.__request('DELETE', path, payload=payload, cls=cls)

    def _put(self, path: str, payload: Optional[Union[dict, Base]]=None, cls: Optional[type]=None) -> Union[dict, str]:
        return self.__request('PUT', path, payload=payload, cls=cls)

    @classmethod
    def _config_for_environment(cls, environment):
        if cls.__config is None:
            cls.__config = ConfigParser()
            cls.__config.read(os.path.join(os.path.dirname(inspect.getfile(cls)), 'config.ini'))

        return cls.__config[environment]

    @classmethod
    def use(
            cls,
            environment_or_domain: Union[Environment, str] = Environment.PROD,
            client_id: Optional[str] = None,
            client_secret: Optional[str] = None,
            scopes: Optional[Tuple[str]] = (),
            api_version: str = API_VERSION,
            application: str = DEFAULT_APPLICATION
    ) -> None:
        environment_or_domain = environment_or_domain.name if isinstance(environment_or_domain, Environment) else environment_or_domain
        key = (environment_or_domain, client_id, scopes)
        session = cls.__sessions.get(key)

        if session is None:
            session = cls.get(
                environment_or_domain,
                client_id=client_id,
                client_secret=client_secret,
                scopes=scopes,
                api_version=api_version,
                application=application
            )

            session.init()
            cls.__sessions[key] = session

        current = type(session).current or cls.current
        if current is not None and current._is_entered:
            raise RuntimeError('Cannot call GsSession.use while an existing session is entered')

        cls.current = session
        type(session).current = session

    @classmethod
    def get(
            cls,
            environment_or_domain: Union[Environment, str],
            client_id: Optional[str] = None,
            client_secret: Optional[str] = None,
            scopes: Optional[Tuple[str]] = (),
            api_version: str = API_VERSION,
            application: str = DEFAULT_APPLICATION
    ) -> 'GsSession':
        """ Return an instance of the appropriate session type for the given credentials"""

        environment_or_domain = environment_or_domain.name if isinstance(environment_or_domain, Environment) else environment_or_domain

        if client_id is not None:
            if environment_or_domain not in (Environment.PROD.name, Environment.QA.name):
                raise MqAuthenticationError('Only PROD and QA are valid environments')

            return OAuth2Session(environment_or_domain, client_id, client_secret, scopes, api_version=api_version, application=application)
        else:
            try:
                from gs_quant.kerberos.session_kerberos import KerberosSession
            except ImportError:
                raise MqAuthenticationError('Must specify client_id and client_secret')

            return KerberosSession(environment_or_domain, api_version=api_version, application=application)


class OAuth2Session(GsSession):

    def __init__(self, environment, client_id, client_secret, scopes, api_version=API_VERSION, application=DEFAULT_APPLICATION):
        env_config = self._config_for_environment(environment)

        super().__init__(env_config['AppDomain'], api_version=api_version, application=application)
        self.auth_url = env_config['AuthURL']
        self.client_id = client_id
        self.client_secret = client_secret
        self.scopes = scopes

    def _authenticate(self):
        auth_data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': ' '.join(self.scopes)
        }
        reply = requests.post(self.auth_url, data=auth_data, verify=True)
        if reply.status_code != 200:
            raise MqAuthenticationError(reply.status_code, reply.text, context=self.auth_url)

        response = json.loads(reply.text)
        self._session.headers.update({'Authorization': 'Bearer {}'.format(response['access_token'])})

    def endpoints_and_definitions(self, service):
        url = '{}/developer/{}/docs/service/{}-service'.format(self.domain, self.api_version, service)
        response = self._session.get(url)
        service_definition = json.loads(response.text)['definition']

        endpoints = []
        for endpoint in service_definition['endpoints']:
            endpoint['path'] = endpoint.get('path', '').replace('/{}/{}'.format(self.api_version, service), '')
            endpoints.append(endpoint)

        return endpoints, service_definition['definitions']

    def request_response_gen(self, endpoint_definition):
        return filter(None, itertools.chain(
            (endpoint_definition.get('requestBody', {}),),
            endpoint_definition.get('responseBody', ())))
