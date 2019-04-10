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
import datetime as dt
import pandas as pd
from itertools import chain
from typing import Iterable, List, Optional, Tuple, Union
from gs_quant.api.data import DataApi
from gs_quant.data.core import DataContext
from gs_quant.target.common import FieldFilterMap
from gs_quant.target.data import DataQuery
from gs_quant.errors import MqValueError
from gs_quant.session import GsSession
from gs_quant.target.data import DataSetEntity


class GsDataApi(DataApi):
    __definitions = {}
    DEFAULT_SCROLL = '30s'

    # DataApi interface

    @classmethod
    def query_data(cls, query: DataQuery, dataset_id: str = None) -> Union[list, tuple]:
        if query.marketDataCoordinates:
            result = GsSession.current._post('/data/coordinates/query', payload=query)
        else:
            result = GsSession.current._post('/data/{}/query'.format(dataset_id), payload=query)

        return result.get('data', ())

    @classmethod
    def last_data(cls, query: DataQuery, dataset_id: str = None) -> Union[list, tuple]:
        if query.marketDataCoordinates:
            result = GsSession.current._post('/data/coordinates/query/last', payload=query)
        else:
            result = GsSession.current._post('/data/{}/last/query'.format(dataset_id), payload=query)

        return result.get('data', ())

    @classmethod
    def symbol_dimensions(cls, dataset_id: str) -> tuple:
        definition = cls.get_definition(dataset_id)
        # TODO Sort out proper JSON decoding
        return tuple(definition.dimensions.get('symbolDimensions'))

    @classmethod
    def time_field(cls, dataset_id: str) -> str:
        definition = cls.get_definition(dataset_id)
        # TODO Sort out proper JSON decoding
        return definition.dimensions.get('timeField')

    # GS-specific functionality

    @classmethod
    def get_coverage(
            cls,
            dataset_id: str,
            scroll: str = DEFAULT_SCROLL,
            scroll_id: Optional[str] = None,
            limit: int = None,
            offset: int = None,
            fields: List[str] = None
    ) -> List[dict]:
        params = {}
        if scroll:
            params['scroll'] = scroll

        if scroll_id:
            params['scrollId'] = scroll_id

        if not limit:
            limit = 4000
        params['limit'] = limit

        if offset:
            params['offset'] = offset

        if fields:
            params['fields'] = fields

        body = GsSession.current._get('/data/{}/coverage'.format(dataset_id), payload=params)
        results = body['results']
        if len(results) > 0 and 'scrollId' in body:
            return results + cls.get_coverage(dataset_id, scroll_id=body['scrollId'], scroll=GsDataApi.DEFAULT_SCROLL,
                                              limit=limit)
        else:
            return results

    @classmethod
    def create(cls, definition: Union[DataSetEntity, dict]) -> DataSetEntity:
        result = GsSession.current._post('/data/datasets', payload=definition)
        return result

    @classmethod
    def update_definition(cls, dataset_id: str, definition: Union[DataSetEntity, dict]) -> DataSetEntity:
        result = GsSession.current._put('/data/datasets/{}'.format(dataset_id), payload=definition, cls=DataSetEntity)
        return result

    @classmethod
    def upload_data(cls, dataset_id: str, data: Union[pd.DataFrame, list, tuple]) -> dict:
        result = GsSession.current._post('/data/{}'.format(dataset_id), payload=data)
        return result

    @classmethod
    def get_definition(cls, dataset_id: str) -> DataSetEntity:
        definition = cls.__definitions.get(dataset_id)
        if not definition:
            definition = GsSession.current._get('/data/datasets/{}'.format(dataset_id), cls=DataSetEntity)
            if not definition:
                raise MqValueError('Unknown dataset {}'.format(dataset_id))

            cls.__definitions[dataset_id] = definition

        return definition

    @staticmethod
    def build_market_data_query(asset_ids: List[str], query_type: str, where: Union[FieldFilterMap] = None,
                                source: Union[str] = None):
        return {
            'queries': [
                {
                    'assetIds': asset_ids,
                    'queryType': query_type,
                    'where': where or {},
                    'source': source or 'any',
                    'frequency': 'End Of Day',
                    'measures': [
                        'Curve'
                    ],
                    'startDate': DataContext.current.start_date,
                    'endDate': DataContext.current.end_date
                }
            ]
        }

    @classmethod
    def get_market_data(cls, query) -> pd.DataFrame:
        GsSession.current: GsSession
        body = GsSession.current._post('/data/markets', payload=query)
        container = body['responses'][0]['queryResponse'][0]
        if 'errorMessages' in container:
            raise MqValueError(container['errorMessages'])
        if 'response' not in container:
            return pd.DataFrame()
        df = pd.DataFrame(container['response']['data'])
        df.set_index('date', inplace=True)
        df.index = pd.to_datetime(df.index)
        return df

    @classmethod
    def __normalise_coordinate_data(cls, data: Iterable[dict]) -> list:
        ret = []

        for row in data:
            if not row:
                continue

            value_field = row['quotingStyle'] if 'field' not in row.keys() else row['field']
            row['value'] = row.pop(value_field)
            ret.append(row)

        return ret

    @classmethod
    def coordinates_last(
            cls,
            coordinates: Union[List, Tuple],
            as_of: Union[dt.date, dt.datetime],
            vendor: str = 'Goldman Sachs',
            as_dataframe: bool = False,
    ) -> Union[dict, pd.DataFrame]:
        ret = {coordinate: None for coordinate in coordinates}
        query = cls.build_query(
            end=as_of,
            marketDataCoordinates=coordinates,
            vendor=vendor
        )

        data = cls.last_data(query)

        for idx, row in enumerate(cls.__normalise_coordinate_data(data)):
            ret[coordinates[idx]] = row['value']

        if as_dataframe:
            data = [dict(chain(c.as_dict().items(), (('value', v),))) for c, v in ret.items()]
            return pd.DataFrame(data)

        return ret

    @classmethod
    def coordinates_data(
            cls,
            coordinates: Union[List, Tuple],
            start: Optional[Union[dt.date, dt.datetime]] = None,
            end: Optional[Union[dt.date, dt.datetime]] = None,
            vendor: str = 'Goldman Sachs',
            as_of: Optional[dt.datetime] = None,
            since: Optional[dt.datetime] = None
    ) -> pd.DataFrame:
        query = cls.build_query(
            marketDataCoordinates=coordinates,
            vendor=vendor,
            start=start,
            end=end,
            asOfTime=as_of,
            since=since
        )

        return pd.DataFrame(cls.__normalise_coordinate_data(cls.query_data(query)))

    @classmethod
    def coordinates_data_series(
            cls,
            coordinates: Union[List, Tuple],
            start: Optional[Union[dt.date, dt.datetime]] = None,
            end: Optional[Union[dt.date, dt.datetime]] = None,
            vendor: str = 'Goldman Sachs',
            as_of: Optional[dt.datetime] = None,
            since: Optional[dt.datetime] = None
    ) -> pd.Series:
        df = cls.coordinates_data(
            coordinates,
            start=start,
            end=end,
            vendor=vendor,
            as_of=as_of,
            since=since)

        index_field = 'time' if 'time' in df.columns else 'date'
        return pd.Series(index=pd.to_datetime(df.loc[:, index_field].values), data=df.value.values)
