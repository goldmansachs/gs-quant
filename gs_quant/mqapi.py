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

from abc import ABCMeta, abstractmethod
from configparser import ConfigParser  # requires configparser
from enum import Enum, unique  # requires enum34
from urllib3 import disable_warnings, exceptions
from .errors import *

import backoff
import cachetools.func
import datetime
import inflection
import json
import logging
import os
import pandas as pd
import re
import requests
import requests.exceptions
import six  # requires six
import typing as ty  # requires typing

API_VERSION = 'v1'
DEFAULT_APPLICATION = 'python-sdk'
Date = ty.Union[datetime.date, ty.AnyStr]
Time = ty.Union[datetime.datetime, ty.AnyStr]
DateOrTime = ty.Union[Date, Time]
_logger = logging.getLogger(__name__)
_config_file = os.path.dirname(__file__) + '/config.ini'
_time_pattern = re.compile('^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}Z)?$')
__all__ = ['Environment', 'MqSession', 'AppSession', '_get_env_config', 'API_VERSION', 'DEFAULT_APPLICATION']

logging.getLogger('backoff').addHandler(logging.StreamHandler())  # log backoff to stderr


@unique
class Environment(Enum):
    PROD = 0


def _get_env_config(env):
    # type: (Environment) -> ty.AnyStr
    config = ConfigParser()
    config.read(_config_file)
    if env.name not in config.sections():
        raise MqError('environment {} does not exist in config {}'.format(env, _config_file))
    return config[env.name]


def _convert_bound(value):
    # type: (DateOrTime) -> ty.Tuple(ty.AnyStr, ty.AnyStr)
    """
    >>> _convert_bound('2018-01-01')
    ('Date', '2018-01-01')
    >>> _convert_bound('2018-01-01T12:10:05Z')
    ('Time', '2018-01-01T12:10:05Z')
    >>> _convert_bound(datetime.datetime(2018, 1, 1, 12, 10, 5))
    ('Time', '2018-01-01T12:10:05Z')
    >>> _convert_bound(datetime.date(2018, 1, 1))
    ('Date', '2018-01-01')
    """
    if isinstance(value, datetime.datetime):
        if value.utcoffset() is not None and value.utcoffset() != datetime.timedelta(0):
            raise MqValueError('only UTC time is supported')
        return 'Time', value.strftime('%Y-%m-%dT%H:%M:%SZ')
    elif isinstance(value, datetime.date):
        return 'Date', value.strftime('%Y-%m-%d')
    elif isinstance(value, six.string_types):
        matcher = _time_pattern.match(value)
        if matcher is None:
            raise MqValueError('invalid time or date string ' + value)
        elif matcher.group(1) is None:
            return 'Date', value
        else:
            return 'Time', value
    else:
        raise MqTypeError('parameter must be a date, time, or parsable string')


class MqSession:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, domain, application=DEFAULT_APPLICATION, verify=True, timeout=(6.1, 60)):
        # type: (ty.AnyStr, ty.AnyStr, bool) -> None
        self.domain = domain
        self.application = application
        self.verify = verify
        self.timeout = timeout
        self.session = None

    @abstractmethod
    def _authenticate(self, session):
        raise NotImplementedError

    def start(self):
        """
        Begin session.
        """
        self.session = requests.Session()
        self.session.verify = self.verify
        self.session.headers.update({'X-Application': self.application})
        self._authenticate(self.session)

    def finish(self):
        """
        End (teardown) session.
        """
        self.session.close()
        self.session = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.finish()
        return False

    @backoff.on_exception(lambda: backoff.expo(factor=2),
                          (requests.exceptions.HTTPError, requests.exceptions.Timeout),
                          max_tries=5)
    @backoff.on_predicate(lambda: backoff.expo(factor=2),
                          lambda x: x.status_code in (500, 502, 503, 504),
                          max_tries=5)
    def perform_request(self, method, url, **kwargs):
        return self.session.request(method, url, **kwargs)

    def request(self, method, path, payload=None, domain=None):
        # type: (ty.AnyStr, ty.AnyStr, dict, ty.AnyStr) -> dict
        """
        Send an HTTP request and get the response body.

        :param method: HTTP method
        :param path: relative path (appended to domain)
        :param payload: query parameters or JSON body
        :param domain: domain including protocol e.g. https://marquee.gs.com
        :return: dict representing a JSON request body, or a string
        """
        # TODO: extend session if it has expired
        if self.session is None:
            raise MqError('Session has been closed. You can restart with start() or create a new session.')

        payload = payload or {}
        url = (domain or self.domain) + path

        kwargs = {}
        if method in ['GET', 'DELETE']:
            kwargs['params'] = payload
        elif method in ['POST', 'PUT']:
            kwargs['json'] = payload
        else:
            raise MqError('not implemented')

        kwargs['timeout'] = self.timeout
        r = self.perform_request(method, url, **kwargs)
        if not 199 < r.status_code < 300:
            raise MqRequestError(r.status_code, r.text, context='{} {}'.format(method, url))
        elif r.headers['content-type'] == 'application/json':
            return json.loads(r.text)
        else:
            return {'raw': r.text}

    def _execute_get(self, path, payload=None, domain=None):
        # type: (ty.AnyStr, dict, ty.AnyStr) -> dict
        return self.request('GET', path, payload, domain)

    def _execute_delete(self, path, payload=None, domain=None):
        # type: (ty.AnyStr, dict, ty.AnyStr) -> dict
        return self.request('DELETE', path, payload, domain)

    def _execute_post(self, path, payload=None, domain=None):
        # type: (ty.AnyStr, dict, ty.AnyStr) -> dict
        return self.request('POST', path, payload, domain)

    def _execute_put(self, path, payload=None, domain=None):
        # type: (ty.AnyStr, dict, ty.AnyStr) -> dict
        return self.request('PUT', path, payload, domain)

    def _get_profile(self):
        return self._execute_get('/{}/users/self'.format(API_VERSION))

    @cachetools.func.ttl_cache(ttl=60)
    def get_data_catalog(self, dataset_id=None):
        # type: (ty.AnyStr) -> dict
        """
        Get data catalog entry or entries.

        :param dataset_id: retrieves entry for dataset if id specified, else all visible entries 
        :return: catalog entry or entries
        """
        if dataset_id is None:
            return self._execute_get('/{}/data/catalog'.format(API_VERSION))['results']
        else:
            return self._execute_get('/{}/data/catalog/{}'.format(API_VERSION, dataset_id))

    def get_coverage(self, dataset_id, scroll_id=None):
        # type: (ty.AnyStr, ty.AnyStr) -> ty.List[dict]
        """
        Get coverage (items for which one or more entries exist) of a dataset.

        :param dataset_id: dataset of interest
        :param scroll_id: scroll_id returned from last page, used to get the next page
                          (if omitted, all pages will be retrieved)
        :return: coverage
        """
        params = {'scroll': '1m', 'limit': 1000}
        if scroll_id:
            params['scrollId'] = scroll_id
        body = self._execute_get('/{}/data/{}/coverage'.format(API_VERSION, dataset_id), payload=params)
        results = body['results']
        if len(results) > 0:
            return results + self.get_coverage(dataset_id, body['scrollId'])
        else:
            return results

    @staticmethod
    def _build_payload(query, **kwargs):
        payload = {'where': query or {}}

        start = kwargs.pop('start', None)
        if start:
            suffix, result = _convert_bound(start)
            payload['start' + suffix] = result

        end = kwargs.pop('end', None)
        if end:
            suffix, result = _convert_bound(end)
            payload['end' + suffix] = result

        as_of_time = kwargs.pop('as_of_time', None)
        if as_of_time:
            _ignore, payload['asOfTime'] = _convert_bound(as_of_time)

        since = kwargs.pop('since', None)
        if since:
            _ignore, payload['since'] = _convert_bound(since)

        for k, v in kwargs.items():
            if v is not None:
                payload[k] = v

        return payload

    def get_data(self,
                 dataset_id,  # type: ty.AnyStr
                 query,  # type: ty.Optional[dict]
                 start=None,  # type: DateOrTime
                 end=None,  # type: DateOrTime
                 as_of_time=None,  # type: ty.Union[datetime.datetime, ty.AnyStr]
                 since=None,  # type: ty.Union[datetime.datetime, ty.AnyStr]
                 fields=None  # type: ty.Iterable[ty.AnyStr]
                 ):
        # type: (...) -> pd.DataFrame
        """
        Query the Marquee Data Service.

        :param dataset_id: id of dataset to query
        :param query: dictionary of query parameters
        :param start: start date or start time
        :param end: end date or end time
        :param as_of_time: finds entries inserted on or before this time (defaults to now)
        :param since: finds entries inserted after this time
        :param fields: fields to be retrieved (all others will be projected away)
        :return: a DataFrame of results
        """
        payload = self._build_payload(query, start=start, end=end, as_of_time=as_of_time, since=since, fields=fields)
        result = self._execute_post('/{}/data/{}/query'.format(API_VERSION, dataset_id), payload)
        _logger.info('get_data request id was {}'.format(result.get('requestId', 'missing')))
        return pd.DataFrame(result['data'])

    def get_data_last(self,
                      dataset_id,  # type: ty.AnyStr
                      query,  # type: ty.Optional[dict]
                      start=None,  # type: DateOrTime
                      end=None,  # type: DateOrTime
                      fields=None  # type: ty.Iterable[ty.AnyStr]
                      ):
        # type: (...) -> pd.DataFrame
        """
        Query the Marquee Data Service for the last entry of a unitemporal dataset.

        :param dataset_id: id of dataset to query
        :param query: dictionary of query parameters
        :param start: start date or start time
        :param end: end date or end time
        :param fields: fields to be retrieved (all others will be projected away)
        :return: a DataFrame containing the result
        """
        payload = self._build_payload(query, start=start, end=end, fields=fields)
        result = self._execute_post('/{}/data/{}/last/query'.format(API_VERSION, dataset_id), payload)
        _logger.info('get_data_last request id was {}'.format(result.get('requestId', 'missing')))
        return pd.DataFrame(result['data'])

    @staticmethod
    def _df_to_ts(df, time_column, value_column):
        index = pd.to_datetime(df.loc[:, time_column].values)
        return pd.Series(index=index, data=df.loc[:, value_column].values)

    def get_data_series(self,
                        dataset_id,  # type: ty.AnyStr
                        query,  # type: ty.Optional[dict]
                        field,  # type: ty.AnyStr
                        start=None,  # type: DateOrTime
                        end=None,  # type: DateOrTime
                        as_of_time=None,  # type: ty.Union[datetime.datetime, ty.AnyStr]
                        since=None,  # type: ty.Union[datetime.datetime, ty.AnyStr]
                        ):
        # type: (...) -> ty.Union[ty.Dict[ty.AnyStr, pd.Series], pd.Series]
        """
        Query the Marquee Data Service for a time series.

        :param dataset_id: id of dataset to query
        :param query: dictionary of query parameters
        :param field: field in dataset to retain (all others will be ignored) 
        :param start: start date or start time
        :param end: end date or end time
        :param as_of_time: finds entries inserted on or before this time (defaults to now)
        :param since: finds entries inserted after this time
        :return: a Series of results
        """
        catalog = self.get_data_catalog(dataset_id)
        dimensions = catalog.get('symbolDimensions', [])
        if len(dimensions) != 1:
            raise MqValueError('{} is not compatible with get_data_curve'.format(dataset_id))

        df = self.get_data(dataset_id, query, start=start, end=end, as_of_time=as_of_time, since=since, fields=[field])
        if df.shape[0] == 0:
            return pd.Series()
        symbol_dimension = dimensions[0]
        gb = df.groupby(symbol_dimension)
        if len(gb.groups) > 1:
            raise MqValueError('not a series for a single {}'.format(symbol_dimension))

        return self._df_to_ts(df, catalog['timeField'], field)

    def write_data(self, dataset_id, df):
        # type: (ty.AnyStr, pd.DataFrame) -> None
        """
        Upload data to a dataset.

        :param dataset_id: id of dataset to be updated
        :param df: DataFrame of rows to be inserted
        """
        payload = df.to_dict(orient='records')
        result = self._execute_post('/{}/data/{}'.format(API_VERSION, dataset_id), payload=payload)
        _logger.info('write_data request id was {}'.format(result.get('requestId', 'missing')))

    def _get_identifiers(self, input_type, ids, output_type=None, as_of_date=None):
        # type: (ty.AnyStr, ty.List[ty.AnyStr], ty.Optional(ty.AnyStr), Date) -> dict
        identifiers = ['ric', 'bbid', 'bcid', 'cusip', 'sedol', 'mdapi', 'id', 'gsid']
        if input_type not in identifiers or (output_type is not None and output_type not in identifiers):
            raise MqValueError('supported identifier types are: ' + ", ".join(identifiers))
        found, date_string = _convert_bound(as_of_date or datetime.date.today())
        if found != 'Date':
            raise MqTypeError('expected parameter as_of_date to be compatible with date')

        payload = {
            'where': {input_type: ids},
            'asOfTime': date_string + 'T00:00:00Z',
            'fields': identifiers if output_type is None else [input_type, output_type]
        }
        response = self._execute_post('/{}/assets/data/query'.format(API_VERSION), payload=payload)
        return {entry.pop(input_type): entry for entry in response['results']}

    def map_identifiers(self, input_type, ids, output_type, as_of_date=None):
        # type: (ty.AnyStr, ty.List[ty.AnyStr], ty.AnyStr, Date) -> ty.Dict[ty.AnyStr, ty.AnyStr]
        """
        Map from one identifier type to another.

        :param input_type: identifier type of input ids
        :param ids: input ids
        :param output_type: target identifier type
        :param as_of_date: will find assets that matched input ids on this date (defaults to today)
        :return: map of {input_id: output_id} entries
        """
        tables = self._get_identifiers(input_type, ids, output_type=output_type, as_of_date=as_of_date)
        return {query_id: table.get(output_type, None) for query_id, table in tables.items()}


class AppSession(MqSession):
    READ_SCOPES = frozenset(('read_product_data', 'read_user_profile'))
    WRITE_SCOPES = READ_SCOPES | frozenset(('modify_product_data'))

    def __init__(self, client_id, client_secret, env, read_only=True, **kwargs):
        # type: (ty.AnyStr, ty.AnyStr, Environment, bool, ty.AnyStr) -> None
        env_config = _get_env_config(env)
        super(AppSession, self).__init__(env_config.get('AppDomain'), **kwargs)

        self.oauth_url = env_config.get('AuthURL')
        self.client_id = client_id
        self.client_secret = client_secret
        self.read_only = read_only

    def _authenticate(self, session):
        # type: (requests.Session) -> None
        scopes = self.READ_SCOPES if self.read_only else self.WRITE_SCOPES
        auth_data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': ' '.join(scopes)
        }
        r = requests.post(self.oauth_url, data=auth_data, verify=self.verify, timeout=(3.05, 10))
        if r.status_code != 200:
            raise MqRequestError(r.status_code, r.text, context=self.oauth_url)
        response = json.loads(r.text)
        session.headers.update({'Authorization': 'Bearer {}'.format(response['access_token'])})
