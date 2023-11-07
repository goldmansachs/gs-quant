"""
Copyright 2023 Goldman Sachs.
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
import datetime as dt
from unittest.mock import patch

from pandas.testing import assert_frame_equal

from gs_quant.api.api_cache import InMemoryApiRequestCache, CacheEvent
from gs_quant.api.gs.data import GsDataApi, QueryType
from gs_quant.data import Dataset, DataContext


class NotExpectedToBeCalledSession():
    @classmethod
    def _get(cls, url, **kwargs):
        raise Exception("Not expecting to be called at this point")

    @classmethod
    def _post(cls, url, **kwargs):
        raise Exception("Not expecting to be called at this point")


class FakeSession():

    @classmethod
    def _get(cls, url, **kwargs):
        if url == '/data/catalog/FXSPOT_STANDARD':
            return {
                'id': 'FXSPOT_STANDARD',
                'fields': {
                    'date': {'type': 'string', 'format': 'date'},
                    'assetId': {'type': 'string'},
                    'spot': {'type': 'number', },
                    'updateTime': {'type': 'string', 'format': 'date-time'}
                }
            }
        else:
            raise Exception("Need to mock _get request here")

    @classmethod
    def _post(cls, url, **kwargs):
        if url == '/data/FXSPOT_STANDARD/last/query':
            return {
                'requestId': '1234',
                'data': [
                    {
                        'date': '2023-10-25',
                        'assetId': 'MATGYV0J9MPX534Z',
                        'bbid': 'USDJPY',
                        'spot': 150.123,
                        'updateTime': '2023-10-25T21:53:56Z'
                    }
                ]}
        elif url == '/data/FXSPOT_STANDARD/query':
            return {
                'requestId': '5678',
                'data': [
                    {
                        'date': '2023-10-26',
                        'assetId': 'MATGYV0J9MPX534Z',
                        'bbid': 'USDJPY',
                        'spot': 152.234,
                        'updateTime': '2023-10-26T21:53:56Z'
                    }
                ]
            }
        elif url == '/data/measures':
            return {
                'requestId': '890', 'responses': [
                    {
                        'queryResponse': [
                            {'measure': 'Curve', 'dataSetIds': ['DATASET_FOO'], 'entityTypes': ['ASSET'],
                             'response': {
                                 'data': [
                                     {'date': '2023-04-11', 'assetId': 'MATGYV0J9MPX534Z', 'pricingLocation': 'HKG',
                                      'name': 'USDJPY', 'spot': 133.},
                                     {'date': '2023-04-11', 'assetId': 'MATGYV0J9MPX534Z', 'pricingLocation': 'LDN',
                                      'name': 'USDJPY', 'spot': 134.0},
                                     {'date': '2023-04-11', 'assetId': 'MATGYV0J9MPX534Z', 'pricingLocation': 'NYC',
                                      'name': 'USDJPY', 'spot': 136.0}]}}]
                    }
                ]
            }


class TestDataApiCache:

    def setup_method(self, test_method):
        self.cache = InMemoryApiRequestCache()
        GsDataApi.set_api_request_cache(self.cache)

    def teardown_method(self, test_method):
        GsDataApi.set_api_request_cache(None)

    def test_last_data(self):
        ds = Dataset("FXSPOT_STANDARD")
        with patch.object(GsDataApi, 'get_session', return_value=FakeSession()):
            df = ds.get_data_last(as_of=dt.date(2023, 10, 25), bbid='USDJPY')
        with patch.object(GsDataApi, 'get_session', return_value=NotExpectedToBeCalledSession()):
            df2 = ds.get_data_last(dt.date(2023, 10, 25), bbid='USDJPY')
        assert not df.empty
        assert_frame_equal(df, df2)
        cache_events = self.cache.get_events()
        assert len(cache_events) == 2
        assert cache_events[0][0] == CacheEvent.PUT
        assert cache_events[1][0] == CacheEvent.GET

    def test_query_data(self):
        ds = Dataset("FXSPOT_STANDARD")
        with patch.object(GsDataApi, 'get_session', return_value=FakeSession()):
            df = ds.get_data(dt.date(2023, 10, 26), dt.date(2023, 10, 26), bbid='USDJPY')
        with patch.object(GsDataApi, 'get_session', return_value=NotExpectedToBeCalledSession()):
            df2 = ds.get_data(dt.date(2023, 10, 26), dt.date(2023, 10, 26), bbid='USDJPY')

        assert_frame_equal(df, df2)
        cache_events = self.cache.get_events()
        assert len(cache_events) == 2
        assert cache_events[0][0] == CacheEvent.PUT
        assert cache_events[1][0] == CacheEvent.GET

    def test_market_data(self):
        asset_id = "MATGYV0J9MPX534Z"
        with DataContext(dt.date(2023, 4, 11), dt.date(2023, 4, 11)):
            q = GsDataApi.build_market_data_query([asset_id], QueryType.SPOT)

        with patch.object(GsDataApi, 'get_session', return_value=FakeSession()):
            df = GsDataApi.get_market_data(q)
        with patch.object(GsDataApi, 'get_session', return_value=NotExpectedToBeCalledSession()):
            df2 = GsDataApi.get_market_data(q)

        assert_frame_equal(df, df2)
        cache_events = self.cache.get_events()
        assert len(cache_events) == 2
        assert cache_events[0][0] == CacheEvent.PUT
        assert cache_events[1][0] == CacheEvent.GET
