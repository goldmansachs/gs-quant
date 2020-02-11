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
from enum import Enum
from itertools import chain
from typing import Iterable, List, Optional, Tuple, Union

import logging
from urllib.parse import urlencode

import cachetools
import numpy
import pandas as pd
from cachetools import TTLCache

from gs_quant.base import Base
from gs_quant.api.data import DataApi
from gs_quant.data.core import DataContext
from gs_quant.errors import MqValueError
from gs_quant.markets import MarketDataCoordinate
from gs_quant.session import GsSession
from gs_quant.target.common import FieldFilterMap, XRef, MarketDataVendor
from gs_quant.target.data import DataQuery, DataQueryResponse, MDAPIDataBatchResponse, MDAPIDataQueryResponse
from gs_quant.target.data import DataSetEntity
from .assets import GsAssetApi, GsIdType

_logger = logging.getLogger(__name__)


class QueryType(Enum):
    IMPLIED_VOLATILITY = "Implied Volatility"
    IMPLIED_CORRELATION = "Implied Correlation"
    AVERAGE_IMPLIED_VOLATILITY = "Average Implied Volatility"
    AVERAGE_IMPLIED_VARIANCE = "Average Implied Variance"
    SWAP_RATE = "Swap Rate"
    SWAPTION_VOL = "Swaption Vol"
    MIDCURVE_VOL = "Midcurve Vol"
    CAP_FLOOR_VOL = "Cap Floor Vol"
    SPREAD_OPTION_VOL = "Spread Option Vol"
    INFLATION_SWAP_RATE = "Inflation Swap Rate"
    FORWARD = "Forward"
    PRICE = "Price"
    ATM_FWD_RATE = "Atm Fwd Rate"
    BASIS = "Basis"
    VAR_SWAP = "Var Swap"
    MIDCURVE_ATM_FWD_RATE = "Midcurve Atm Fwd Rate"
    CAP_FLOOR_ATM_FWD_RATE = "Cap Floor Atm Fwd Rate"
    SPREAD_OPTION_ATM_FWD_RATE = "Spread Option Atm Fwd Rate"
    FORECAST = "Forecast"
    IMPLIED_VOLATILITY_BY_DELTA_STRIKE = "Implied Volatility By Delta Strike"
    FUNDAMENTAL_METRIC = "Fundamental Metric"
    POLICY_RATE_EXPECTATION = "Policy Rate Expectation"
    CENTRAL_BANK_SWAP_RATE = "Central Bank Swap Rate"
    FORWARD_PRICE = "Forward Price"
    SPOT = "Spot"


class GsDataApi(DataApi):
    __definitions = {}
    DEFAULT_SCROLL = '30s'

    # DataApi interface

    @classmethod
    def query_data(cls, query: DataQuery, dataset_id: str = None, asset_id_type: Union[GsIdType, str] = None) \
            -> Union[MDAPIDataBatchResponse, DataQueryResponse, tuple]:
        if query.marketDataCoordinates:
            # Don't use MDAPIDataBatchResponse for now - it doesn't handle quoting style correctly
            results: Union[MDAPIDataBatchResponse, dict] = GsSession.current._post(
                '/data/coordinates/query', payload=query)
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

                sd = definition.dimensions.symbolDimensions
                if definition.parameters.symbolStrategy == 'MDAPI' or ('assetId' not in sd and 'gsid' not in sd):
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
                                                                          payload=query)
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

    @classmethod
    def get_many_definitions(cls,
                             limit: int = 100,
                             dataset_id: str = None,
                             owner_id: str = None,
                             name: str = None,
                             mq_symbol: str = None) -> Tuple[DataSetEntity, ...]:

        query_string = urlencode(dict(filter(lambda item: item[1] is not None,
                                             dict(id=dataset_id, ownerId=owner_id, name=name,
                                                  mqSymbol=mq_symbol, limit=limit).items())))

        res = GsSession.current._get('/data/datasets?{query}'.format(query=query_string), cls=DataSetEntity)['results']
        return res

    @staticmethod
    def build_market_data_query(asset_ids: List[str], query_type: QueryType, where: Union[FieldFilterMap] = None,
                                source: Union[str] = None, real_time: bool = False):
        inner = {
            'assetIds': asset_ids,
            'queryType': query_type.value,
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
            raise MqValueError(f"market data request {body['requestId']} failed: {container['errorMessages']}")
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
            rows = (
                r.as_dict() for r in response.data) if isinstance(
                response,
                MDAPIDataQueryResponse) else response.get(
                'data',
                ())

            for pt in rows:
                if not pt:
                    continue

                if 'value' not in pt:
                    value_field = pt['mktQuotingStyle']
                    pt['value'] = pt.pop(value_field)

                coord_data.append(pt)
            ret.append(coord_data)

        return ret

    @classmethod
    def __df_from_coordinate_data(
            cls,
            data: Iterable[dict]
    ) -> pd.DataFrame:
        df = cls._sort_coordinate_data(pd.DataFrame.from_records(data))
        index_field = next((f for f in ('time', 'date') if f in df.columns), None)
        if index_field:
            df = df.set_index(pd.DatetimeIndex(df.loc[:, index_field].values))

        return df

    @classmethod
    def _sort_coordinate_data(
            cls,
            df: pd.DataFrame,
            by: Tuple[str] = ('date', 'time', 'mktType', 'mktAsset', 'mktClass', 'mktPoint', 'mktQuotingStyle', 'value')
    ) -> pd.DataFrame:
        columns = df.columns
        field_order = [f for f in by if f in columns]
        field_order.extend(f for f in columns if f not in field_order)
        return df[field_order]

    @classmethod
    def _coordinate_from_str(cls, coordinate_str: str) -> MarketDataCoordinate:
        tmp = coordinate_str.rsplit(".", 1)
        dimensions = tmp[0].split("_")
        if len(dimensions) < 2:
            raise MqValueError('invalid coordinate ' + coordinate_str)

        kwargs = {
            'mkt_type': dimensions[0],
            'mkt_asset': dimensions[1] or None,
            'mkt_quoting_style': tmp[-1] if len(tmp) > 1 else None}

        if len(dimensions) > 2:
            kwargs['mkt_class'] = dimensions[2] or None

        if len(dimensions) > 3:
            kwargs['mkt_point'] = tuple(dimensions[3:]) or None

        return MarketDataCoordinate(**kwargs)

    @classmethod
    def coordinates_last(
            cls,
            coordinates: Union[Iterable[str], Iterable[MarketDataCoordinate]],
            as_of: Union[dt.datetime, dt.date] = None,
            vendor: MarketDataVendor = MarketDataVendor.Goldman_Sachs,
            as_dataframe: bool = False,
            pricing_location: Optional[str] = None
    ) -> Union[dict, pd.DataFrame]:
        """
        Get last value of coordinates data

        :param coordinates: market data coordinate(s)
        :param as_of: snapshot date or time
        :param vendor: data vendor
        :param as_dataframe: whether to return the result as Dataframe
        :param pricing_location: the location where close data has been recorded (not used for real-time query)
        :return: Dataframe or dictionary of the returned data

        **Examples**

        >>> coordinate = ("FX Fwd_USD/EUR_Fwd Pt_2y",)
        >>> data = GsDataApi.coordinates_last(coordinate, dt.datetime(2019, 11, 19))
        """
        market_data_coordinates = tuple(cls._coordinate_from_str(coord) if isinstance(coord, str) else coord
                                        for coord in coordinates)
        ret = {coordinate: None for coordinate in market_data_coordinates}
        query = cls.build_query(
            end=as_of,
            market_data_coordinates=market_data_coordinates,
            vendor=vendor,
            pricing_location=pricing_location
        )

        data = cls.last_data(query)

        for idx, row in enumerate(cls.__normalise_coordinate_data(data)):
            try:
                ret[market_data_coordinates[idx]] = row[0]['value']
            except IndexError:
                ret[market_data_coordinates[idx]] = None

        if as_dataframe:
            data = [dict(chain(c.as_dict(as_camel_case=True).items(), (('value', v),))) for c, v in ret.items()]
            return cls.__df_from_coordinate_data(data)

        return ret

    @classmethod
    def coordinates_data(
            cls,
            coordinates: Union[str, MarketDataCoordinate, Iterable[str], Iterable[MarketDataCoordinate]],
            start: Union[dt.datetime, dt.date] = None,
            end: Union[dt.datetime, dt.date] = None,
            vendor: MarketDataVendor = MarketDataVendor.Goldman_Sachs,
            as_multiple_dataframes: bool = False,
            pricing_location: Optional[str] = None
    ) -> Union[pd.DataFrame, Tuple[pd.DataFrame]]:
        """
        Get coordinates data

        :param coordinates: market data coordinate(s)
        :param start: start date or time
        :param end: end date or time
        :param vendor: data vendor
        :param as_multiple_dataframes: whether to return the result as one or multiple Dataframe(s)
        :param pricing_location: the location where close data has been recorded (not used for real-time query)
        :return: Dataframe(s) of the returned data

        **Examples**

        >>> coordinate = ("FX Fwd_USD/EUR_Fwd Pt_2y",)
        >>> data = GsDataApi.coordinates_data(coordinate, dt.datetime(2019, 11, 18), dt.datetime(2019, 11, 19))
        """
        coordinates_iterable = (coordinates,) if isinstance(coordinates, (MarketDataCoordinate, str)) else coordinates
        query = cls.build_query(
            market_data_coordinates=tuple(cls._coordinate_from_str(coord) if isinstance(coord, str) else coord
                                          for coord in coordinates_iterable),
            vendor=vendor,
            start=start,
            end=end,
            pricing_location=pricing_location
        )

        results = cls.__normalise_coordinate_data(cls.query_data(query))

        if as_multiple_dataframes:
            return tuple(GsDataApi.__df_from_coordinate_data(r) for r in results)
        else:
            return cls.__df_from_coordinate_data(chain.from_iterable(results))

    @classmethod
    def coordinates_data_series(
            cls,
            coordinates: Union[str, MarketDataCoordinate, Iterable[str], Iterable[MarketDataCoordinate]],
            start: Union[dt.datetime, dt.date] = None,
            end: Union[dt.datetime, dt.date] = None,
            vendor: MarketDataVendor = MarketDataVendor.Goldman_Sachs,
            pricing_location: Optional[str] = None
    ) -> Union[pd.Series, Tuple[pd.Series]]:
        """
        Get coordinates data series

        :param coordinates: market data coordinate(s)
        :param start: start date or time
        :param end: end date or time
        :param vendor: data vendor
        :param pricing_location: the location where close data has been recorded (not used for real-time query)
        :return: Series of the returned data

        **Examples**

        >>> coordinate = ("FX Fwd_USD/EUR_Fwd Pt_2y",)
        >>> data = GsDataApi.coordinates_data_series(coordinate, dt.datetime(2019, 11, 18), dt.datetime(2019, 11, 19))
        """
        dfs = cls.coordinates_data(
            coordinates,
            start=start,
            end=end,
            pricing_location=pricing_location,
            vendor=vendor,
            as_multiple_dataframes=True)

        ret = tuple(pd.Series() if df.empty else pd.Series(index=df.index, data=df.value.values) for df in dfs)
        if isinstance(coordinates, (MarketDataCoordinate, str)):
            return ret[0]
        else:
            return ret

    @staticmethod
    @cachetools.cached(TTLCache(ttl=3600, maxsize=128))
    def get_types(dataset_id: str):
        results = GsSession.current._get(f'/data/catalog/{dataset_id}')
        fields = results.get("fields")
        if fields:
            field_types = {}
            for key, value in fields.items():
                field_type = value.get('type')
                field_format = value.get('format')
                field_types[key] = field_format or field_type
            return field_types
        raise RuntimeError(f"Unable to get Dataset schema for {dataset_id}")

    @classmethod
    def construct_dataframe_with_types(cls, dataset_id: str, data: Union[Base, list, tuple]) -> pd.DataFrame:
        """
        Constructs a dataframe with correct date types.
        :param data: data to convert with correct types
        :return: dataframe with correct types
        """
        if len(data):
            dataset_types = cls.get_types(dataset_id)
            df = pd.DataFrame(data)

            for field_name, type_name in dataset_types.items():
                if df.get(type_name) is not None and type_name in ('date', 'date-time'):
                    df = df.astype({field_name: numpy.datetime64})

            field_names = dataset_types.keys()

            if 'date' in field_names:
                df = df.set_index('date')
            elif 'time' in field_names:
                df = df.set_index('time')

            return df
        else:
            return pd.DataFrame({})
