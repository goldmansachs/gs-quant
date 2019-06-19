"""
Copyright 2019 Goldman Sachs.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on ans
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

import msgpack
import requests
import requests.cookies

from abc import abstractmethod
from configparser import ConfigParser
from enum import Enum, auto, unique
import pandas as pd
from typing import List, Optional, Tuple, Union

from gs_quant.base import Base
from gs_quant.context_base import ContextBase
from gs_quant.errors import MqError, MqRequestError, MqAuthenticationError, MqUninitialisedError
from gs_quant.json_encoder import JSONEncoder

API_VERSION = 'v1'
DEFAULT_APPLICATION = 'gs-quant'


@unique
class Environment(Enum):
    DEV = auto()
    QA = auto()
    PROD = auto()


class GsSession(ContextBase):
    __config = None

    class Scopes(Enum):
        READ_CONTENT = 'read_content'
        READ_FINANCIAL_DATA = 'read_financial_data'
        READ_PRODUCT_DATA = 'read_product_data'
        READ_USER_PROFILE = 'read_user_profile'
        MODIFY_CONTENT = 'modify_content'
        MODIFY_FINANCIAL_DATA = 'modify_financial_data'
        MODIFY_PRODUCT_DATA = 'modify_product_data'
        MODIFY_USER_PROFILE = 'modify_user_profile'
        RUN_ANALYTICS = 'run_analytics'
        EXECUTE_TRADES = 'execute_trades'

        @classmethod
        def get_default(cls):
            return [
                cls.READ_CONTENT.value,
                cls.READ_PRODUCT_DATA.value,
                cls.READ_FINANCIAL_DATA.value
            ]

    def __init__(self, domain: str, api_version: str=API_VERSION, application: str=DEFAULT_APPLICATION, verify=True):
        super().__init__()
        self._session = None
        self.domain = domain
        self.api_version = api_version
        self.application = application
        self.verify = verify

    @backoff.on_exception(lambda: backoff.expo(factor=2),
                          (requests.exceptions.HTTPError, requests.exceptions.Timeout),
                          max_tries=5)
    @backoff.on_predicate(lambda: backoff.expo(factor=2),
                          lambda x: x.status_code in (500, 502, 503, 504),
                          max_tries=5)
    @abstractmethod
    def _authenticate(self):
        raise NotImplementedError("Must implement _authenticate")

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
            self._session.verify = self.verify
            self._session.headers.update({'X-Application': self.application})
            self._authenticate()

    def close(self):
        self._session: requests.Session
        self._session.close()
        self._session = None

    def __unpack(self, results: Union[dict, list], cls: type) -> Union[Base, tuple, dict]:
        if issubclass(cls, Base):
            if isinstance(results, list):
                return tuple(None if r is None else cls.from_dict(r) for r in results)
            else:
                return None if results is None else cls.from_dict(results)
        else:
            if isinstance(results, list):
                return tuple(cls(**r) for r in results)
            else:
                return cls(**results)

    def __request(
            self,
            method: str,
            path: str,
            payload: Optional[Union[dict, str, Base, pd.DataFrame]]=None,
            request_headers: Optional[dict]=None,
            cls: Optional[type]=None,
            try_auth=True,
            include_version: bool = True) -> Union[Base, tuple, dict]:
        is_dataframe = isinstance(payload, pd.DataFrame)
        if not is_dataframe:
            payload = payload or {}

        url = '{}{}{}'.format(self.domain, '/' + self.api_version if include_version else '', path)

        kwargs = {}
        if method in ['GET', 'DELETE']:
            kwargs['params'] = payload
        elif method in ['POST', 'PUT']:
            headers = self._session.headers.copy()
            if request_headers:
                headers.update({**{'Content-Type': 'application/json'}, **request_headers})
            else:
                headers.update({'Content-Type': 'application/json'})
            kwargs['headers'] = headers
            if is_dataframe or payload:
                kwargs['data'] = payload if isinstance(payload, str) else json.dumps(payload, cls=JSONEncoder)
        else:
            raise MqError('not implemented')

        response = self._session.request(method, url, **kwargs)
        if response.status_code == 401:
            # Expired token or other authorization issue
            if not try_auth:
                raise MqRequestError(response.status_code, response.text, context='{} {}'.format(method, url))
            self._authenticate()
            return self.__request(method, path, payload=payload, cls=cls, try_auth=False)
        elif not 199 < response.status_code < 300:
            raise MqRequestError(response.status_code, response.text, context='{} {}'.format(method, url))
        elif 'application/x-msgpack' in response.headers['content-type']:
            res = msgpack.unpackb(response.content, raw=False)

            if cls:
                if isinstance(res, dict) and 'results' in res:
                    res['results'] = self.__unpack(res['results'], cls)
                else:
                    res = self.__unpack(res, cls)

            return res
        elif 'application/json' in response.headers['content-type']:
            res = json.loads(response.text)

            if cls:
                if isinstance(res, dict) and 'results' in res:
                    res['results'] = self.__unpack(res['results'], cls)
                else:
                    res = self.__unpack(res, cls)

            return res
        else:
            return {'raw': response}

    def _get(self, path: str, payload: Optional[Union[dict, Base]]=None, request_headers: Optional[dict]=None, cls: Optional[type]=None, include_version: bool=True) -> Union[Base, tuple, dict]:
        return self.__request('GET', path, payload=payload, request_headers=request_headers, cls=cls, include_version=include_version)

    def _post(self, path: str, payload: Optional[Union[dict, Base, pd.DataFrame]]=None, request_headers: Optional[dict]=None, cls: Optional[type]=None, include_version: bool=True) -> Union[Base, tuple, dict]:
        return self.__request('POST', path, payload=payload, request_headers=request_headers, cls=cls, include_version=include_version)

    def _delete(self, path: str, payload: Optional[Union[dict, Base]]=None, request_headers: Optional[dict]=None, cls: Optional[type]=None, include_version: bool=True) -> Union[Base, tuple, dict]:
        return self.__request('DELETE', path, payload=payload, request_headers=request_headers, cls=cls, include_version=include_version)

    def _put(self, path: str, payload: Optional[Union[dict, Base]]=None, request_headers: Optional[dict]=None, cls: Optional[type]=None, include_version: bool=True) -> Union[Base, tuple, dict]:
        return self.__request('PUT', path, payload=payload, request_headers=request_headers, cls=cls, include_version=include_version)

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
            scopes: Optional[Union[Tuple, List]] = (),
            api_version: str = API_VERSION,
            application: str = DEFAULT_APPLICATION
    ) -> None:
        environment_or_domain = environment_or_domain.name if isinstance(environment_or_domain,
                                                                         Environment) else environment_or_domain
        session = cls.get(
            environment_or_domain,
            client_id=client_id,
            client_secret=client_secret,
            scopes=scopes,
            api_version=api_version,
            application=application
        )

        session.init()

        if cls.current_is_set:
            cls.current = session
        else:
            cls.default = session

    @classmethod
    def get(
            cls,
            environment_or_domain: Union[Environment, str] = Environment.PROD,
            client_id: Optional[str] = None,
            client_secret: Optional[str] = None,
            scopes: Optional[Union[Tuple, List]] = (),
            token: str = '',
            is_gssso: bool = False,
            api_version: str = API_VERSION,
            application: str = DEFAULT_APPLICATION
    ) -> 'GsSession':
        """ Return an instance of the appropriate session type for the given credentials"""

        environment_or_domain = environment_or_domain.name if isinstance(environment_or_domain,
                                                                         Environment) else environment_or_domain

        if client_id is not None:
            if environment_or_domain not in (Environment.PROD.name, Environment.QA.name, Environment.DEV.name):
                raise MqUninitialisedError('Only PROD, QA and DEV are valid environments')

            return OAuth2Session(environment_or_domain, client_id, client_secret, scopes, api_version=api_version,
                                 application=application)
        elif token:
            return PassThroughSession(environment_or_domain, token, is_gssso, api_version=api_version,
                                      application=application)
        else:
            try:
                return KerberosSession(environment_or_domain, api_version=api_version)
            except NameError:
                raise MqUninitialisedError('Must specify client_id and client_secret')


class OAuth2Session(GsSession):
    def __init__(self, environment, client_id, client_secret, scopes, api_version=API_VERSION,
                 application=DEFAULT_APPLICATION):
        env_config = self._config_for_environment(environment)

        super().__init__(env_config['AppDomain'], api_version=api_version, application=application)
        self.auth_url = env_config['AuthURL']
        self.client_id = client_id
        self.client_secret = client_secret
        self.scopes = scopes

        if environment == Environment.DEV.name:
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            self.verify = False

    def _authenticate(self):
        auth_data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': ' '.join(self.scopes)
        }
        reply = requests.post(self.auth_url, data=auth_data, verify=self.verify)
        if reply.status_code != 200:
            raise MqAuthenticationError(reply.status_code, reply.text, context=self.auth_url)

        response = json.loads(reply.text)
        self._session.headers.update({'Authorization': 'Bearer {}'.format(response['access_token'])})

    def request_response_gen(self, endpoint_definition):
        return filter(None, itertools.chain(
            (endpoint_definition.get('requestBody', {}),),
            endpoint_definition.get('responseBody', ())))


class PassThroughSession(GsSession):
    def __init__(self, environment: str, token, is_gssso=True, api_version=API_VERSION,
                 application=DEFAULT_APPLICATION):
        if is_gssso:
            domain, verify = KerberosSessionMixin.domain_and_verify(environment)
        else:
            domain = self._config_for_environment(environment)['AppDomain']
            verify = True

        super().__init__(domain, api_version=api_version, application=application, verify=verify)
        self.token = token
        self.is_gssso = is_gssso

        if environment == Environment.DEV.name:
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            self.verify = False

    def _authenticate(self):
        self._session: requests.Session
        if self.is_gssso:
            co = requests.cookies.create_cookie(domain='.gs.com', name='GSSSO', value=self.token)
            self._session.cookies.set_cookie(co)
        else:
            self._session.headers.update({'Authorization': 'Bearer {}'.format(self.token)})

    def endpoints_and_definitions(self, service):
        raise NotImplementedError('Not supported for this type of session')

    def request_response_gen(self, endpoint_definition):
        raise NotImplementedError('Not supported for this type of session')


try:
    import importlib
    from collections import namedtuple

    mod = importlib.import_module('gs_quant_internal.kerberos.session_kerberos')
    KerberosSessionMixin = getattr(mod, 'KerberosSessionMixin')

    class KerberosSession(KerberosSessionMixin, GsSession):

        def __init__(self, environment_or_domain: str, api_version: str=API_VERSION, application: str=DEFAULT_APPLICATION):
            domain, verify = KerberosSessionMixin.domain_and_verify(environment_or_domain)
            GsSession.__init__(self, domain, api_version=api_version, application=application, verify=verify)

except ModuleNotFoundError:
    pass
