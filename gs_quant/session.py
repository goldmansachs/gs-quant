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

from abc import abstractmethod
import backoff
import certifi
from configparser import ConfigParser
from enum import Enum, auto, unique
import inspect
import itertools
import json
import msgpack
import os
import pandas as pd
import requests
import requests.adapters
import requests.cookies
import ssl
from typing import Optional, Union, Iterable

from gs_quant import version as APP_VERSION
from gs_quant.base import Base
from gs_quant.context_base import ContextBase
from gs_quant.errors import MqError, MqRequestError, MqAuthenticationError, MqUninitialisedError
from gs_quant.json_encoder import JSONEncoder, encode_default

API_VERSION = 'v1'
DEFAULT_APPLICATION = 'gs-quant'
DEFAULT_TIMEOUT = 65


@unique
class Environment(Enum):
    DEV = auto()
    QA = auto()
    PROD = auto()


class GsSession(ContextBase):
    __config = None
    __ssl_ctx = None

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
            return (
                cls.READ_CONTENT.value,
                cls.READ_PRODUCT_DATA.value,
                cls.READ_FINANCIAL_DATA.value,
                cls.READ_USER_PROFILE.value
            )

    def __init__(self, domain: str, api_version: str = API_VERSION, application: str = DEFAULT_APPLICATION, verify=True,
                 http_adapter: requests.adapters.HTTPAdapter = None, application_version=APP_VERSION, proxies=None):
        super().__init__()
        self._session = None
        self.domain = domain
        self.api_version = api_version
        self.application = application
        self.verify = verify
        self.http_adapter = requests.adapters.HTTPAdapter(pool_maxsize=100) if http_adapter is None else http_adapter
        self.application_version = application_version
        self.proxies = proxies

    @backoff.on_exception(lambda: backoff.expo(factor=2),
                          (requests.exceptions.HTTPError, requests.exceptions.Timeout),
                          max_tries=5)
    @backoff.on_predicate(lambda: backoff.expo(factor=2),
                          lambda x: x.status_code in (500, 502, 503, 504),
                          max_tries=5)
    @abstractmethod
    def _authenticate(self):
        raise NotImplementedError("Must implement _authenticate")

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
            if self.http_adapter is not None:
                self._session.mount('https://', self.http_adapter)
            if self.proxies is not None:
                self._session.proxies = self.proxies
            self._session.verify = self.verify
            self._session.headers.update({'X-Application': self.application})
            self._session.headers.update({'X-Version': self.application_version})
            self._authenticate()

    def close(self):
        self._session: requests.Session

        if self._session:
            # don't close a shared adapter
            if self.http_adapter is None:
                self._session.close()
            self._session = None

    def __del__(self):
        self.close()

    @staticmethod
    def __ssl_context() -> ssl.SSLContext:
        if GsSession.__ssl_ctx is None:
            GsSession.__ssl_ctx = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
            GsSession.__ssl_ctx.load_default_certs()
            GsSession.__ssl_ctx.load_verify_locations(certifi.where())

        return GsSession.__ssl_ctx

    @staticmethod
    def __unpack(results: Union[dict, list], cls: type) -> Union[Base, tuple, dict]:
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
            payload: Optional[Union[dict, str, bytes, Base, pd.DataFrame]] = None,
            request_headers: Optional[dict] = None,
            cls: Optional[type] = None,
            try_auth: Optional[bool] = True,
            include_version: Optional[bool] = True,
            timeout: Optional[int] = DEFAULT_TIMEOUT,
            return_request_id: Optional[bool] = False,
            use_body: bool = False
    ) -> Union[Base, tuple, dict]:
        is_dataframe = isinstance(payload, pd.DataFrame)
        if not is_dataframe:
            payload = payload or {}

        url = '{}{}{}'.format(self.domain, '/' + self.api_version if include_version else '', path)

        kwargs = {
            'timeout': timeout
        }

        if method in ['GET', 'DELETE'] and not use_body:
            kwargs['params'] = payload
        elif method in ['POST', 'PUT'] or (method in ['GET', 'DELETE'] and use_body):
            headers = self._session.headers.copy()

            if request_headers:
                headers.update(request_headers)

            if 'Content-Type' not in headers:
                headers.update({'Content-Type': 'application/json; charset=utf-8'})

            use_msgpack = headers.get('Content-Type') == 'application/x-msgpack'
            kwargs['headers'] = headers

            if is_dataframe or payload:
                kwargs['data'] = payload if isinstance(payload, (str, bytes)) else \
                    msgpack.dumps(payload, default=encode_default) if use_msgpack else \
                    json.dumps(payload, cls=JSONEncoder)
        else:
            raise MqError('not implemented')

        response = self._session.request(method, url, **kwargs)
        request_id = response.headers.get('x-dash-requestid')

        if response.status_code == 401:
            # Expired token or other authorization issue
            if not try_auth:
                raise MqRequestError(response.status_code, response.text, context='{} {}'.format(method, url))
            self._authenticate()
            return self.__request(method, path, payload=payload, cls=cls,
                                  include_version=include_version, return_request_id=return_request_id,
                                  use_body=use_body, try_auth=False)
        elif not 199 < response.status_code < 300:
            raise MqRequestError(response.status_code, response.text,
                                 context=f'{response.headers.get("")}: {method} {url}')
        elif 'Content-Type' in response.headers:
            if 'application/x-msgpack' in response.headers['Content-Type']:
                res = msgpack.unpackb(response.content, raw=False)

                if cls:
                    if isinstance(res, dict) and 'results' in res:
                        res['results'] = self.__unpack(res['results'], cls)
                    else:
                        res = self.__unpack(res, cls)

                return (res, request_id) if return_request_id else res
            elif 'application/json' in response.headers['Content-Type']:
                res = json.loads(response.text)

                if cls:
                    if isinstance(res, dict) and 'results' in res:
                        res['results'] = self.__unpack(res['results'], cls)
                    else:
                        res = self.__unpack(res, cls)

                return (res, request_id) if return_request_id else res
        else:
            ret = {'raw': response}
            if return_request_id:
                ret['request_id'] = request_id

            return ret

    def _get(self, path: str, payload: Optional[Union[dict, Base]] = None, request_headers: Optional[dict] = None,
             cls: Optional[type] = None, include_version: Optional[bool] = True,
             timeout: Optional[int] = DEFAULT_TIMEOUT, return_request_id: Optional[bool] = False) \
            -> Union[Base, tuple, dict]:
        return self.__request('GET', path, payload=payload, request_headers=request_headers,
                              cls=cls, include_version=include_version, timeout=timeout,
                              return_request_id=return_request_id)

    def _post(self, path: str, payload: Optional[Union[dict, bytes, Base, pd.DataFrame]] = None,
              request_headers: Optional[dict] = None, cls: Optional[type] = None,
              include_version: Optional[bool] = True, timeout: Optional[int] = DEFAULT_TIMEOUT,
              return_request_id: Optional[bool] = False) -> Union[Base, tuple, dict]:
        return self.__request('POST', path, payload=payload, request_headers=request_headers,
                              cls=cls, include_version=include_version, timeout=timeout,
                              return_request_id=return_request_id)

    def _delete(self, path: str, payload: Optional[Union[dict, Base]] = None,
                request_headers: Optional[dict] = None, cls: Optional[type] = None,
                include_version: Optional[bool] = True, timeout: Optional[int] = DEFAULT_TIMEOUT,
                return_request_id: Optional[bool] = False, use_body: Optional[bool] = False) -> \
            Union[Base, tuple, dict]:
        return self.__request('DELETE', path, payload=payload, request_headers=request_headers,
                              cls=cls, include_version=include_version, timeout=timeout,
                              return_request_id=return_request_id, use_body=use_body)

    def _put(self, path: str, payload: Optional[Union[dict, Base]] = None,
             request_headers: Optional[dict] = None, cls: Optional[type] = None, include_version: Optional[bool] = True,
             timeout: Optional[int] = DEFAULT_TIMEOUT, return_request_id: Optional[bool] = False) \
            -> Union[Base, tuple, dict]:
        return self.__request('PUT', path, payload=payload, request_headers=request_headers,
                              cls=cls, include_version=include_version, timeout=timeout,
                              return_request_id=return_request_id)

    def _connect_websocket(self, path: str, headers: Optional[dict] = None):
        import websockets
        url = 'ws{}{}{}'.format(self.domain[4:], '/' + self.api_version, path)
        extra_headers = self._headers() + list((headers or {}).items())
        return websockets.connect(url,
                                  extra_headers=extra_headers,
                                  max_size=2 ** 64,
                                  read_limit=2 ** 64,
                                  ssl=self.__ssl_context() if url.startswith('wss') else None)

    def _headers(self):
        return [('Cookie', 'GSSSO=' + self._session.cookies['GSSSO'])]

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
            scopes: Optional[Union[Iterable[Union[Scopes, str]], str]] = (),
            api_version: str = API_VERSION,
            application: str = DEFAULT_APPLICATION,
            http_adapter: requests.adapters.HTTPAdapter = None,
            use_mds: bool = False
    ) -> None:
        environment_or_domain = environment_or_domain.name if isinstance(environment_or_domain,
                                                                         Environment) else environment_or_domain
        session = cls.get(
            environment_or_domain,
            client_id=client_id,
            client_secret=client_secret,
            scopes=scopes,
            api_version=api_version,
            application=application,
            http_adapter=http_adapter,
            use_mds=use_mds
        )

        session.init()
        cls.current = session

    @classmethod
    def get(
            cls,
            environment_or_domain: Union[Environment, str] = Environment.PROD,
            client_id: Optional[str] = None,
            client_secret: Optional[str] = None,
            scopes: Optional[Union[Iterable[Union[Scopes, str]], str]] = (),
            token: str = '',
            is_gssso: bool = False,
            api_version: str = API_VERSION,
            application: str = DEFAULT_APPLICATION,
            http_adapter: requests.adapters.HTTPAdapter = None,
            application_version: str = APP_VERSION,
            use_mds: bool = False
    ) -> 'GsSession':
        """ Return an instance of the appropriate session type for the given credentials"""

        environment_or_domain = environment_or_domain.name if isinstance(environment_or_domain,
                                                                         Environment) else environment_or_domain

        if client_id is not None:
            if isinstance(scopes, str):
                scopes = (scopes,)

            scopes = (scope if isinstance(scope, str) else scope.value for scope in scopes)
            scopes = tuple(set(itertools.chain(scopes, cls.Scopes.get_default())))

            return OAuth2Session(environment_or_domain, client_id, client_secret, scopes, api_version=api_version,
                                 application=application, http_adapter=http_adapter, use_mds=use_mds)
        elif token:
            if is_gssso:
                try:
                    return PassThroughGSSSOSession(environment_or_domain, token, api_version=api_version,
                                                   application=application, http_adapter=http_adapter)
                except NameError:
                    raise MqUninitialisedError('This option requires gs_quant_auth to be installed')
            else:
                return PassThroughSession(environment_or_domain, token, api_version=api_version,
                                          application=application, http_adapter=http_adapter)
        else:
            try:
                return KerberosSession(environment_or_domain, api_version=api_version, http_adapter=http_adapter,
                                       application_version=application_version, application=application)
            except NameError:
                raise MqUninitialisedError('Must specify client_id and client_secret')

    def is_internal(self) -> bool:
        return False


class OAuth2Session(GsSession):

    def __init__(self, environment, client_id, client_secret, scopes, api_version=API_VERSION,
                 application=DEFAULT_APPLICATION, http_adapter=None, use_mds=False):

        if environment not in (Environment.PROD.name, Environment.QA.name, Environment.DEV.name):
            env_config = self._config_for_environment(Environment.DEV.name)
            url = environment
        else:
            env_config = self._config_for_environment(environment)
            url = env_config['MdsDomain'] if use_mds else env_config['AppDomain']

        super().__init__(url, api_version=api_version, application=application, http_adapter=http_adapter)
        self.auth_url = env_config['AuthURL']
        self.client_id = client_id
        self.client_secret = client_secret
        self.scopes = scopes

        if environment == Environment.DEV.name or (url != env_config['AppDomain'] and not use_mds):
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
        reply = self._session.post(self.auth_url, data=auth_data, verify=self.verify)
        if reply.status_code != 200:
            raise MqAuthenticationError(reply.status_code, reply.text, context=self.auth_url)

        response = json.loads(reply.text)
        self._session.headers.update({'Authorization': 'Bearer {}'.format(response['access_token'])})

    def _headers(self):
        return [('Authorization', self._session.headers['Authorization'])]


class PassThroughSession(GsSession):

    def __init__(self, environment: str, token, api_version=API_VERSION,
                 application=DEFAULT_APPLICATION, http_adapter=None):
        domain = self._config_for_environment(environment)['AppDomain']
        verify = True

        super().__init__(domain, api_version=api_version, application=application, verify=verify,
                         http_adapter=http_adapter)

        self.token = token

    def _authenticate(self):
        self._session.headers.update({'Authorization': 'Bearer {}'.format(self.token)})

    def _headers(self):
        return [('Authorization', self._session.headers['Authorization'])]


try:
    from gs_quant_auth.kerberos.session_kerberos import KerberosSessionMixin

    class KerberosSession(KerberosSessionMixin, GsSession):

        def __init__(self, environment_or_domain: str, api_version: str = API_VERSION,
                     application: str = DEFAULT_APPLICATION, http_adapter: requests.adapters.HTTPAdapter = None,
                     application_version: str = APP_VERSION):
            domain, verify = self.domain_and_verify(environment_or_domain)
            GsSession.__init__(self, domain, api_version=api_version, application=application, verify=verify,
                               http_adapter=http_adapter, application_version=application_version)

    class PassThroughGSSSOSession(KerberosSessionMixin, GsSession):

        def __init__(self, environment: str, token, api_version=API_VERSION,
                     application=DEFAULT_APPLICATION, http_adapter=None, csrf_token=None):
            domain, verify = self.domain_and_verify(environment)
            GsSession.__init__(self, domain, api_version=api_version, application=application, verify=verify,
                               http_adapter=http_adapter)

            self.token = token
            self.csrf_token = csrf_token

        def _authenticate(self):
            if not (self.token and self.csrf_token):
                self._handle_cookies(self.token)
                return

            cookie = requests.cookies.create_cookie(domain='.gs.com', name='GSSSO', value=self.token)
            self._session.cookies.set_cookie(cookie)
            if self.csrf_token:
                cookie = requests.cookies.create_cookie(domain='.gs.com', name='MARQUEE-CSRF-TOKEN',
                                                        value=self.csrf_token)
                self._session.cookies.set_cookie(cookie)
                self._session.headers.update({'X-MARQUEE-CSRF-TOKEN': self.csrf_token})

except ModuleNotFoundError:
    pass
