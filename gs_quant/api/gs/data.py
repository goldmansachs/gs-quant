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
from itertools import chain
import pandas as pd
from typing import List, Optional, Tuple, Union
from gs_quant.api.data import DataApi
from gs_quant.data import DataQuery, DataSet
from gs_quant.errors import MqValueError
from gs_quant.session import GsSession
from gs_quant.target.data import DataSetEntity


class GsDataApi(DataApi):

    __definitions = {}

    # DataApi interface

    @classmethod
    def query_data(cls, query: DataQuery, dataset: DataSet=None) -> Union[list, tuple]:
        if query.marketDataCoordinates:
            result = GsSession.current._post('/data/coordinates/query', payload=query)
        else:
            result = GsSession.current._post('/data/{}/query'.format(dataset.dataset_id), payload=query)

        return result.get('data', ())

    @classmethod
    def last_data(cls, query: DataQuery, dataset: DataSet=None) -> Union[list, tuple]:
        if query.marketDataCoordinates:
            result = GsSession.current._post('/data/coordinates/query/last', payload=query)
        else:
            result = GsSession.current._post('/data/{}/last/query'.format(dataset.dataset_id), payload=query)

        return result.get('data', ())

    @classmethod
    def symbol_dimensions(cls, dataset: DataSet) -> tuple:
        definition = cls.get_definition(dataset)
        # TODO Sort out proper JSON decoding
        return tuple(definition.dimensions['symbolDimensions'])

    @classmethod
    def time_field(cls, dataset: DataSet) -> str:
        definition = cls.get_definition(dataset)
        # TODO Sort out proper JSON decoding
        return definition.dimensions['timeField']

    # GS-specific functionality

    @classmethod
    def get_coverage(cls, dataset: DataSet, scroll_id: Optional[str] = None) -> List[dict]:
        params = {'scroll': '1m', 'limit': 1000}
        if scroll_id:
            params['scrollId'] = scroll_id

        body = GsSession.current._get('/data/{}/coverage'.format(dataset.dataset_id), payload=params)
        results = body['results']
        if len(results) > 0:
            return results + cls.get_coverage(dataset, body['scrollId'])
        else:
            return results

    @classmethod
    def create(cls, definition: Union[DataSetEntity, dict]) -> DataSetEntity:
        result = GsSession.current._post('/data/datasets', payload=definition)
        return result

    @classmethod
    def update_definition(cls, dataset: DataSet, definition: Union[DataSetEntity, dict]) -> DataSetEntity:
        result = GsSession.current._put('/data/datasets/{}'.format(dataset.dataset_id), payload=definition, cls=DataSetEntity)
        return result

    @classmethod
    def upload_data(cls, dataset: DataSet, data: Union[pd.DataFrame, list, tuple]) -> dict:
        result = GsSession.current._post('/data/{}'.format(dataset.dataset_id), payload=data)
        return result

    @classmethod
    def get_definition(cls, dataset: DataSet) -> DataSetEntity:
        definition = cls.__definitions.get(dataset.dataset_id)
        if not definition:
            definition = GsSession.current._get('/data/datasets/{}'.format(dataset.dataset_id), cls=DataSetEntity)
            if not definition:
                raise MqValueError('Unknown dataset {}'.format(dataset.dataset_id))

            cls.__definitions[dataset.dataset_id] = definition

        return definition

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

        for idx, row in enumerate(data):
            if not row:
                continue

            value = row[row['field']]
            ret[coordinates[idx]] = value

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

        return pd.DataFrame(cls.query_data(query))


