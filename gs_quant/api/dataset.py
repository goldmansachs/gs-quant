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

import datetime
from typing import Optional, Iterable, Union, Tuple, List

import pandas as pd

from gs_quant.api.data import DataSetEntity
from gs_quant.api.risk import MarketDataCoordinate
from gs_quant.errors import MqTypeError, MqValueError
from gs_quant.session import GsSession


class Dataset:

    __catalogs_by_dataset_id = {}
    __catalogs_by_mdapi_vendor_is_time = {}

    def __init__(self, dataset_id: str):
        self.__dataset_id = dataset_id

    @property
    def definition(self) -> DataSetEntity:
        return GsSession.current._get('/data/datasets/%s' % self.dataset_id, cls=DataSetEntity)

    def update_definition(self, dataset: Union[DataSetEntity, dict]) -> DataSetEntity:
        result = GsSession.current._put('/data/datasets/%s' % self.dataset_id, payload=dataset, cls=DataSetEntity)
        return result

    @staticmethod
    def create(dataset: Union[DataSetEntity, dict]) -> DataSetEntity:
        result = GsSession.current._post('/data/datasets', payload=dataset)
        return result

    @staticmethod
    def reset():
        Dataset.__catalogs_by_dataset_id.clear()
        Dataset.__catalogs_by_mdapi_vendor_is_time.clear()

    @staticmethod
    def __add_by_mdapi_info(catalog):
        mdapi = catalog.get('mdapi', {})
        _market_data_type = mdapi.get('type')
        if _market_data_type:
            for quoting_style in mdapi['quotingStyles']:
                key = (mdapi['type'], quoting_style['quotingStyle'], catalog['vendor'], catalog['timeField'] == 'time')
                Dataset.__catalogs_by_mdapi_vendor_is_time[key] = catalog

    @staticmethod
    def dataset_for_coordinate_vendor_is_time(coordinate: MarketDataCoordinate, vendor: str, is_time: bool ):
        # TODO: Search by market_data_type rather than loading all catalogs
        if not Dataset.__catalogs_by_mdapi_vendor_is_time:
            all_catalogs = GsSession.current._get('/data/catalog')['results']
            for catalog in all_catalogs:
                Dataset.__catalogs_by_dataset_id[catalog['id']] = catalog
                Dataset.__add_by_mdapi_info(catalog)

        catalog = Dataset.__catalogs_by_mdapi_vendor_is_time.get((coordinate.marketDataType, coordinate.field, vendor, is_time))

        if not catalog or catalog['mdapi'].get('class', coordinate.pointClass) != coordinate.pointClass:
            raise MqValueError('Could not find dataset for {}, {}, {}'.format(coordinate, vendor, is_time))

        return Dataset(catalog['id'])

    @staticmethod
    def __build_get_data_query_payload(start=None, end=None, as_of=None, since=None, fields=(), **kwargs):
        payload = {'where': kwargs}

        if start:
            suffix, result = Dataset.convert_date_or_datetime(start)
            payload['start' + suffix] = result

        if end:
            suffix, result = Dataset.convert_date_or_datetime(end)
            payload['end' + suffix] = result

        if as_of:
            _ignore, payload['asOfTime'] = Dataset.convert_date_or_datetime(as_of)

        if since:
            _ignore, payload['since'] = Dataset.convert_date_or_datetime(since)

        if fields:
            payload["fields"] = fields

        return payload

    @staticmethod
    def convert_date_or_datetime(value: Union[datetime.date, datetime.datetime]) -> Tuple[str, str]:
        """
        >>> convert_date_or_datetime(datetime.datetime(2018, 1, 1, 12, 10, 5))
        ('Time', '2018-01-01T12:10:05Z')
        >>> convert_date_or_datetime(datetime.date(2018, 1, 1))
        ('Date', '2018-01-01')
        """
        if isinstance(value, datetime.datetime):
            if value.utcoffset() is not None and value.utcoffset() != datetime.timedelta(0):
                raise MqValueError('only UTC time is supported')
            return 'Time', value.strftime('%Y-%m-%dT%H:%M:%SZ')
        elif isinstance(value, datetime.date):
            return 'Date', value.strftime('%Y-%m-%d')
        else:
            raise MqTypeError('parameter must be a date or datetime')

    @property
    def dataset_id(self):
        return self.__dataset_id

    @property
    def catalog(self):
        catalog = self.__catalogs_by_dataset_id.get(self.dataset_id)
        if not catalog:
            catalog = GsSession.current._get('/data/catalog/{}'.format(self.dataset_id))
            if not catalog:
                raise MqValueError('Unknown dataset {}'.format(self.dataset_id))

            self.__catalogs_by_dataset_id[self.dataset_id] = catalog
            Dataset.__add_by_mdapi_info(catalog)

        return catalog

    @property
    def marketDataType(self):
        return self.catalog.get('mdapi', {}).get('type')

    def get_coverage(self, scroll_id: Optional[str] = None) -> List[dict]:
        params = {'scroll': '1m', 'limit': 1000}
        if scroll_id:
            params['scrollId'] = scroll_id

        body = GsSession.current._get('/data/{}/coverage'.format(self.dataset_id), payload=params)
        results = body['results']
        if len(results) > 0:
            return results + self.get_coverage(body['scrollId'])
        else:
            return results

    def get_data(
        self,
        start: Optional[Union[datetime.date, datetime.datetime]] = None,
        end: Optional[Union[datetime.date, datetime.datetime]] = None,
        as_of: Optional[datetime.datetime] = None,
        since: Optional[datetime.datetime] = None,
        fields: Optional[Iterable[str]] = None,
        **kwargs
    ) -> pd.DataFrame:
        """Run a query against the Marquee Data Service. Returns a DataFrame."""
        payload = self.__build_get_data_query_payload(start=start, end=end, as_of=as_of, since=since, fields=fields,
                                                      **kwargs)
        result = GsSession.current._post('/data/{}/query'.format(self.dataset_id), payload=payload)
        return pd.DataFrame(result['data'])

    def upload_data(
            self,
            data: Union[pd.DataFrame, list]
                    ) -> dict:

        result = GsSession.current._post('/data/{}'.format(self.dataset_id), payload=data)
        return result


    def get_data_series(
            self,
            field: str,
            start: Optional[Union[datetime.date, datetime.datetime]] = None,
            end: Optional[Union[datetime.date, datetime.datetime]] = None,
            as_of: Optional[datetime.datetime] = None,
            since: Optional[datetime.datetime] = None,
            **kwargs
    ) -> pd.Series:
        catalog = self.catalog
        dimensions = catalog.get('symbolDimensions', ())

        if len(dimensions) != 1:
            raise MqValueError('{} is not compatible with get_data_curve'.format(self.dataset_id))

        df = self.get_data(start=start, end=end, as_of=as_of, since=since, fields=[field], **kwargs)
        symbol_dimension = dimensions[0]

        gb = df.groupby(dimensions)
        if len(gb.groups) > 1:
            raise MqValueError('not a series for a single {}'.format(symbol_dimension))

        index = pd.to_datetime(df.loc[:, catalog['timeField']].values)
        return pd.Series(index=index, data=df.loc[:, field].values)
