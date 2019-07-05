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
from typing import Iterable, List, Optional, Tuple, Union

import pandas as pd

from gs_quant.api.data import DataApi
from gs_quant.data.core import DataContext
from gs_quant.errors import MqValueError
from gs_quant.session import GsSession
from gs_quant.target.common import FieldFilterMap, XRef, MarketDataCoordinate
from gs_quant.target.data import DataQuery, DataQueryResponse, MDAPIDataBatchResponse, MDAPIDataQueryResponse
from gs_quant.target.data import DataSetEntity
from .assets import GsAssetApi, GsIdType


class GsDataApi(DataApi):
    __definitions = {}
    DEFAULT_SCROLL = '30s'

    # DataApi interface

    @classmethod
    def query_data(cls, query: DataQuery, dataset_id: str = None, asset_id_type: Union[GsIdType, str] = None) \
            -> Union[MDAPIDataBatchResponse, DataQueryResponse, tuple]:
        if query.marketDataCoordinates:
            # Don't use MDAPIDataBatchResponse for now - it doesn't handle quoting style correctly
            results: Union[MDAPIDataBatchResponse, dict] = GsSession.current._post('/data/coordinates/query', payload=query)
            if isinstance(results, dict):
                return results.get('responses', ())
            else:
                return results.responses if results.responses is not None else ()
        if query.where:
            where = query.where.as_dict()
            xref_keys = set(where.keys()).intersection(XRef.properties())
            if xref_keys:
                # Check that assetId is a symbol dimension of this data set. If not, we need to do a separate query
                # to resolve xref --> assetId
                if len(xref_keys) > 1:
                    raise MqValueError('Cannot not specify more than one type of asset identifier')

                definition = cls.get_definition(dataset_id)

                if definition.parameters.symbolStrategy == 'MDAPI' or 'assetId' not in definition.dimensions.symbolDimensions:
                    xref_type = min(xref_keys)
                    if asset_id_type is None:
                        asset_id_type = xref_type

                    xref_values = where[asset_id_type]
                    xref_values = (xref_values,) if isinstance(xref_values, str) else xref_values
                    asset_id_map = GsAssetApi.map_identifiers(xref_type, GsIdType.id, xref_values)

                    if len(asset_id_map) != len(xref_values):
                        raise MqValueError('Not all {} were resolved to asset Ids'.format(asset_id_type))

                    setattr(query.where, xref_type, None)
                    query.where.assetId = [asset_id_map[x] for x in xref_values]

        results: Union[DataQueryResponse, dict] = GsSession.current._post('/data/{}/query'.format(dataset_id),
                                                                          payload=query,
                                                                          cls=DataQueryResponse)
        if isinstance(results, dict):
            results = results.get('data', ())
        else:
            results = results.data if results.data is not None else ()

        if asset_id_type not in {GsIdType.id, None}:
            asset_ids = tuple(set(filter(None, (r.get('assetId') for r in results))))
            if asset_ids:
                xref_map = GsAssetApi.map_identifiers(GsIdType.id, asset_id_type, asset_ids)

                if len(xref_map) != len(asset_ids):
                    raise MqValueError('Not all asset Ids were resolved to {}'.format(asset_id_type))

                for result in results:
                    result[asset_id_type] = xref_map[result['assetId']]

        return results

    @classmethod
    def last_data(cls, query: DataQuery, dataset_id: str = None) -> Union[list, tuple]:
        if query.marketDataCoordinates:
            result = GsSession.current._post('/data/coordinates/query/last', payload=query)
            return result.get('responses', ())
        else:
            result = GsSession.current._post('/data/{}/last/query'.format(dataset_id), payload=query)
            return result.get('data', ())

    @classmethod
    def symbol_dimensions(cls, dataset_id: str) -> tuple:
        definition = cls.get_definition(dataset_id)
        return definition.dimensions.symbolDimensions

    @classmethod
    def time_field(cls, dataset_id: str) -> str:
        definition = cls.get_definition(dataset_id)
        return definition.dimensions.timeField

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
                                source: Union[str] = None, real_time: bool = False):
        inner = {
            'assetIds': asset_ids,
            'queryType': query_type,
            'where': where or {},
            'source': source or 'any',
            'frequency': 'Real Time' if real_time else 'End Of Day',
            'measures': [
                'Curve'
            ]
        }
        if real_time:
            inner['startTime'] = DataContext.current.start_time
            inner['endTime'] = DataContext.current.end_time
        else:
            inner['startDate'] = DataContext.current.start_date
            inner['endDate'] = DataContext.current.end_date
        return {
            'queries': [inner]
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
        df.set_index('date' if 'date' in df.columns else 'time', inplace=True)
        df.index = pd.to_datetime(df.index)
        return df

    @classmethod
    def __normalise_coordinate_data(
            cls,
            data: Iterable[Union[MDAPIDataQueryResponse, dict]]
    ) -> Iterable[Iterable[dict]]:
        ret = []
        for response in data:
            coord_data = []
            rows = (r.as_dict() for r in response.data) if isinstance(response, MDAPIDataQueryResponse) else response.get('data', ())

            for pt in rows:
                if not pt:
                    continue

                if 'value' not in pt:
                    value_field = pt['quotingStyle'] if 'field' not in pt else pt['field']
                    pt['value'] = pt.pop(value_field)

                coord_data.append(pt)
            ret.append(coord_data)

        return ret

    @classmethod
    def __df_from_coordinate_data(
            cls,
            data: Iterable[dict]
    ) -> pd.DataFrame:
        from gs_quant.risk import sort_risk

        df = sort_risk(pd.DataFrame.from_records(data))
        index_field = next((f for f in ('time', 'date') if f in df.columns), None)
        if index_field:
            df = df.set_index(pd.DatetimeIndex(df.loc[:, index_field].values))

        return df

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
            try:
                ret[coordinates[idx]] = row[0]['value']
            except IndexError:
                ret[coordinates[idx]] = None

        if as_dataframe:
            data = [dict(chain(c.as_dict().items(), (('value', v),))) for c, v in ret.items()]
            return cls.__df_from_coordinate_data(data)

        return ret

    @classmethod
    def coordinates_data(
            cls,
            coordinates: Union[MarketDataCoordinate, Iterable[MarketDataCoordinate]],
            start: Optional[Union[dt.date, dt.datetime]] = None,
            end: Optional[Union[dt.date, dt.datetime]] = None,
            vendor: str = 'Goldman Sachs',
            as_multiple_dataframes: bool = False
    ) -> Union[pd.DataFrame, Tuple[pd.DataFrame]]:
        multiple_coordinates = not isinstance(coordinates, MarketDataCoordinate)
        query = cls.build_query(
            marketDataCoordinates=coordinates if multiple_coordinates else (coordinates,),
            vendor=vendor,
            start=start,
            end=end
        )

        results = cls.__normalise_coordinate_data(cls.query_data(query))

        if as_multiple_dataframes:
            return tuple(GsDataApi.__df_from_coordinate_data(r) for r in results)
        else:
            return cls.__df_from_coordinate_data(chain.from_iterable(results))

    @classmethod
    def coordinates_data_series(
            cls,
            coordinates: Union[MarketDataCoordinate, Iterable[MarketDataCoordinate]],
            start: Optional[Union[dt.date, dt.datetime]] = None,
            end: Optional[Union[dt.date, dt.datetime]] = None,
            vendor: str = 'Goldman Sachs',
    ) -> Union[pd.Series, Tuple[pd.Series]]:
        dfs = cls.coordinates_data(
            coordinates,
            start=start,
            end=end,
            vendor=vendor,
            as_multiple_dataframes=True)

        ret = tuple(pd.Series() if df.empty else pd.Series(index=df.index, data=df.value.values) for df in dfs)
        if isinstance(coordinates, MarketDataCoordinate):
            return ret[0]
        else:
            return ret
