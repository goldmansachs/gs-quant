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
import asyncio
import datetime as dt
import json
import logging
import time
from copy import copy, deepcopy
from enum import Enum
from itertools import chain
from typing import Iterable, List, Optional, Tuple, Union, Dict

import cachetools
import pandas as pd
from cachetools import TTLCache
from dateutil import parser
from pydash import get

from gs_quant.api.data import DataApi
from gs_quant.base import Base
from gs_quant.data.core import DataContext, DataFrequency
from gs_quant.data.log import log_debug, log_warning
from gs_quant.errors import MqValueError
from gs_quant.json_encoder import JSONEncoder
from gs_quant.markets import MarketDataCoordinate
from gs_quant.target.common import MarketDataVendor, PricingLocation, Format
from gs_quant.target.coordinates import MDAPIDataBatchResponse, MDAPIDataQuery, MDAPIDataQueryResponse, MDAPIQueryField
from gs_quant.target.data import DataQuery, DataQueryResponse, DataSetCatalogEntry
from gs_quant.target.data import DataSetEntity, DataSetFieldEntity
from .assets import GsIdType
from ..api_cache import ApiRequestCache
from ...target.assets import EntityQuery, FieldFilterMap

_logger = logging.getLogger(__name__)
_REQUEST_HEADERS = "request_headers"


class QueryType(Enum):
    IMPLIED_VOLATILITY = "Implied Volatility"
    IMPLIED_VOLATILITY_BY_EXPIRATION = "Implied Volatility By Expiration"
    IMPLIED_CORRELATION = "Implied Correlation"
    REALIZED_CORRELATION = "Realized Correlation"
    AVERAGE_IMPLIED_VOLATILITY = "Average Implied Volatility"
    AVERAGE_IMPLIED_VARIANCE = "Average Implied Variance"
    AVERAGE_REALIZED_VOLATILITY = "Average Realized Volatility"
    SWAP_RATE = "Swap Rate"
    SWAP_ANNUITY = "Swap Annuity"
    SWAPTION_PREMIUM = "Swaption Premium"
    SWAPTION_ANNUITY = "Swaption Annuity"
    BASIS_SWAP_RATE = "Basis Swap Rate"
    XCCY_SWAP_SPREAD = "Xccy Swap Spread"
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
    MIDCURVE_PREMIUM = "Midcurve Premium"
    MIDCURVE_ANNUITY = "Midcurve Annuity"
    MIDCURVE_ATM_FWD_RATE = "Midcurve Atm Fwd Rate"
    CAP_FLOOR_ATM_FWD_RATE = "Cap Floor Atm Fwd Rate"
    SPREAD_OPTION_ATM_FWD_RATE = "Spread Option Atm Fwd Rate"
    FORECAST = "Forecast"
    IMPLIED_VOLATILITY_BY_DELTA_STRIKE = "Implied Volatility By Delta Strike"
    FUNDAMENTAL_METRIC = "Fundamental Metric"
    POLICY_RATE_EXPECTATION = "Policy Rate Expectation"
    CENTRAL_BANK_SWAP_RATE = "Central Bank Swap Rate"
    FORWARD_PRICE = "Forward Price"
    FAIR_PRICE = "Fair Price"
    PNL = "Pnl"
    SPOT = "Spot"
    AUM = "Aum"
    RATE = "Rate"
    ES_NUMERIC_SCORE = "Es Numeric Score"
    ES_NUMERIC_PERCENTILE = "Es Numeric Percentile"
    ES_POLICY_SCORE = "Es Policy Score"
    ES_POLICY_PERCENTILE = "Es Policy Percentile"
    ES_SCORE = "Es Score"
    ES_PERCENTILE = "Es Percentile"
    ES_PRODUCT_IMPACT_SCORE = "Es Product Impact Score"
    ES_PRODUCT_IMPACT_PERCENTILE = "Es Product Impact Percentile"
    G_SCORE = "G Score"
    G_PERCENTILE = "G Percentile"
    ES_MOMENTUM_SCORE = "Es Momentum Score"
    ES_MOMENTUM_PERCENTILE = "Es Momentum Percentile"
    G_REGIONAL_SCORE = "G Regional Score"
    G_REGIONAL_PERCENTILE = "G Regional Percentile"
    ES_DISCLOSURE_PERCENTAGE = "Es Disclosure Percentage"
    CONTROVERSY_SCORE = "Controversy Score"
    CONTROVERSY_PERCENTILE = "Controversy Percentile"
    RATING = "Rating"
    CONVICTION_LIST = "Conviction List"
    FAIR_VALUE = "Fair Value"
    FX_FORECAST = "Fx Forecast"
    GROWTH_SCORE = "Growth Score"
    FINANCIAL_RETURNS_SCORE = "Financial Returns Score"
    MULTIPLE_SCORE = "Multiple Score"
    INTEGRATED_SCORE = "Integrated Score"
    COMMODITY_FORECAST = "Commodity Forecast"
    FORECAST_VALUE = "Forecast Value"
    FORWARD_POINT = "Forward Point"
    FCI = "Fci"
    LONG_RATES_CONTRIBUTION = "Long Rates Contribution"
    SHORT_RATES_CONTRIBUTION = "Short Rates Contribution"
    CORPORATE_SPREAD_CONTRIBUTION = "Corporate Spread Contribution"
    SOVEREIGN_SPREAD_CONTRIBUTION = "Sovereign Spread Contribution"
    EQUITIES_CONTRIBUTION = "Equities Contribution"
    REAL_LONG_RATES_CONTRIBUTION = "Real Long Rates Contribution"
    REAL_SHORT_RATES_CONTRIBUTION = "Real Short Rates Contribution"
    REAL_FCI = "Real Fci"
    DWI_CONTRIBUTION = "Dwi Contribution"
    REAL_TWI_CONTRIBUTION = "Real Twi Contribution"
    TWI_CONTRIBUTION = "Twi Contribution"
    COVARIANCE = "Covariance"
    FACTOR_EXPOSURE = "Factor Exposure"
    FACTOR_RETURN = "Factor Return"
    HISTORICAL_BETA = "Historical Beta"
    FACTOR_PNL = "Factor Pnl"
    FACTOR_PROPORTION_OF_RISK = "Factor Proportion Of Risk"
    DAILY_RISK = "Daily Risk"
    ANNUAL_RISK = "Annual Risk"
    VOLATILITY = "Volatility"
    CORRELATION = "Correlation"
    OIS_XCCY = "Ois Xccy"
    OIS_XCCY_EX_SPIKE = "Ois Xccy Ex Spike"
    USD_OIS = "Usd Ois"
    NON_USD_OIS = "Non Usd Ois"
    SETTLEMENT_PRICE = "Settlement Price"
    THEMATIC_EXPOSURE = "Thematic Exposure"
    THEMATIC_BETA = "Thematic Beta"
    THEMATIC_MODEL_BETA = "Thematic Model Beta"
    CDS_SPREAD_100 = "Spread At100"
    CDS_SPREAD_250 = "Spread At250"
    CDS_SPREAD_500 = "Spread At500"
    STRIKE_VOL = "Strike Vol"
    OPTION_PREMIUM = "Option Premium"
    ABSOLUTE_STRIKE = "Absolute Strike"
    RETAIL_PCT_SHARES = 'impliedRetailPctShares'
    RETAIL_PCT_NOTIONAL = 'impliedRetailPctNotional'
    RETAIL_SHARES = 'impliedRetailShares'
    RETAIL_NOTIONAL = 'impliedRetailNotional'
    SHARES = 'shares'
    NOTIONAL = 'notional'
    RETAIL_BUY_NOTIONAL = 'impliedRetailBuyNotional'
    RETAIL_BUY_PCT_NOTIONAL = 'impliedRetailBuyPctNotional'
    RETAIL_BUY_PCT_SHARES = 'impliedRetailBuyPctShares'
    RETAIL_BUY_SHARES = 'impliedRetailBuyShares'
    RETAIL_SELL_NOTIONAL = 'impliedRetailSellNotional'
    RETAIL_SELL_PCT_NOTIONAL = 'impliedRetailSellPctNotional'
    RETAIL_SELL_PCT_SHARES = 'impliedRetailSellPctShares'
    RETAIL_SELL_SHARES = 'impliedRetailSellShares'
    FWD_POINTS = 'Fwd Points'
    S3_AGGREGATE_DATA = 'value'


class GsDataApi(DataApi):
    __definitions = {}
    __asset_coordinates_cache = TTLCache(10000, 86400)
    _api_request_cache: ApiRequestCache = None
    DEFAULT_SCROLL = '30s'

    # DataApi interface

    @classmethod
    def set_api_request_cache(cls, cache: ApiRequestCache):
        cls._api_request_cache = cache

    @classmethod
    def _construct_cache_key(cls, url, **kwargs) -> tuple:
        def fallback_encoder(v) -> str:
            if isinstance(v, dt.date):
                return v.isoformat()

        def serialize_value(v):
            if any(isinstance(v, class_) for class_ in {MDAPIDataQuery, DataQuery}):
                return v.to_json(sort_keys=True, default=fallback_encoder)
            encoded_v = fallback_encoder(v)
            return encoded_v or v

        json_kwargs = {
            k: serialize_value(v)
            for k, v in kwargs.items()
            if k not in {_REQUEST_HEADERS}
        }
        cache_key = (url, 'POST', json_kwargs)
        return cache_key

    @classmethod
    def _check_cache(cls, url, **kwargs):
        session = cls.get_session()
        cached_val, cache_key = None, None
        if cls._api_request_cache:
            cache_key = cls._construct_cache_key(url, **kwargs)
            cached_val = cls._api_request_cache.get(session, cache_key)
        return cached_val, cache_key, session

    @classmethod
    def _post_with_cache_check(cls, url, validator=lambda x: x, domain=None, **kwargs):
        result, cache_key, session = cls._check_cache(url=url, **kwargs)
        if result is None:
            result = validator(session._post(url, domain=domain, **kwargs))
            if cls._api_request_cache:
                cls._api_request_cache.put(session, cache_key, result)
        return result

    @classmethod
    def _get_with_cache_check(cls, url, validator=lambda x: x, domain=None, **kwargs):
        result, cache_key, session = cls._check_cache(url, **kwargs)
        if result is None:
            result = validator(session._get(url, domain=domain, **kwargs))
            if cls._api_request_cache:
                cls._api_request_cache.put(session, cache_key, result)
        return result

    @classmethod
    async def _get_with_cache_check_async(cls, url, validator=lambda x: x, domain=None, **kwargs):
        result, cache_key, session = cls._check_cache(url, **kwargs)
        if result is None:
            result = await session._get_async(url, domain=domain, **kwargs)
            result = validator(result)
            if cls._api_request_cache:
                cls._api_request_cache.put(session, cache_key, result)
        return result

    @classmethod
    async def _post_with_cache_check_async(cls, url, validator=lambda x: x, domain=None, **kwargs):
        result, cache_key, session = cls._check_cache(url, **kwargs)
        if result is None:
            result = await session._post_async(url, domain=domain, **kwargs)
            result = validator(result)
            if cls._api_request_cache:
                cls._api_request_cache.put(session, cache_key, result)
        return result

    @classmethod
    def query_data(cls, query: Union[DataQuery, MDAPIDataQuery], dataset_id: str = None,
                   asset_id_type: Union[GsIdType, str] = None) \
            -> Union[MDAPIDataBatchResponse, DataQueryResponse, tuple, list]:
        if isinstance(query, MDAPIDataQuery) and query.market_data_coordinates:
            # Don't use MDAPIDataBatchResponse for now - it doesn't handle quoting style correctly
            results: Union[MDAPIDataBatchResponse, dict] = cls.execute_query('coordinates', query)
            if isinstance(results, dict):
                return results.get('responses', ())
            else:
                return results.responses if results.responses is not None else ()
        response: Union[DataQueryResponse, dict] = cls.execute_query(dataset_id, query)
        return cls.get_results(dataset_id, response, query)

    @classmethod
    async def query_data_async(cls, query: Union[DataQuery, MDAPIDataQuery], dataset_id: str = None) \
            -> Union[MDAPIDataBatchResponse, DataQueryResponse, tuple, list]:
        if isinstance(query, MDAPIDataQuery) and query.market_data_coordinates:
            # Don't use MDAPIDataBatchResponse for now - it doesn't handle quoting style correctly
            results: Union[MDAPIDataBatchResponse, dict] = await cls.execute_query_async('coordinates', query)
            if isinstance(results, dict):
                return results.get('responses', ())
            else:
                return results.responses if results.responses is not None else ()
        response: Union[DataQueryResponse, dict] = await cls.execute_query_async(dataset_id, query)
        results = await cls.get_results_async(dataset_id, response, query)
        return results

    @classmethod
    def execute_query(cls, dataset_id: str, query: Union[DataQuery, MDAPIDataQuery]):
        kwargs = {'payload': query}
        if getattr(query, 'format', None) in (Format.MessagePack, 'MessagePack'):
            kwargs[_REQUEST_HEADERS] = {'Accept': 'application/msgpack'}

        domain = cls._check_data_on_cloud(dataset_id)
        return cls._post_with_cache_check('/data/{}/query'.format(dataset_id), domain=domain, **kwargs)

    @classmethod
    async def execute_query_async(cls, dataset_id: str, query: Union[DataQuery, MDAPIDataQuery]):
        kwargs = {'payload': query}
        if getattr(query, 'format', None) in (Format.MessagePack, 'MessagePack'):
            kwargs[_REQUEST_HEADERS] = {'Accept': 'application/msgpack'}

        domain = await cls._check_data_on_cloud_async(dataset_id)
        result = await cls._post_with_cache_check_async('/data/{}/query'.format(dataset_id), domain=domain, **kwargs)
        return result

    @classmethod
    def _check_data_on_cloud(cls, dataset_id: str):
        session = cls.get_session()
        if session.redirect_to_mds and dataset_id != 'coordinates':
            dataset_data = cls._get_with_cache_check('/data/datasets/{}'.format(dataset_id))
            database_id_exists = get(dataset_data, 'parameters.databaseId')

            if database_id_exists:
                return cls.get_session()._get_mds_domain()
        return None

    @classmethod
    async def _check_data_on_cloud_async(cls, dataset_id: str):
        session = cls.get_session()
        if session.redirect_to_mds and dataset_id != 'coordinates':
            dataset_data = await cls._get_with_cache_check(f'/data/datasets/{dataset_id}')
            database_id_exists = get(dataset_data, 'parameters.databaseId')

            if database_id_exists:
                return cls.get_session()._get_mds_domain()
        return None

    @staticmethod
    def _get_results(response: Union[DataQueryResponse, dict]):
        if isinstance(response, dict):
            total_pages = response.get('totalPages')
            results = response.get('data', [])
            if 'groups' in response:
                group_by = set()
                for group in response['groups']:
                    group_by.update(group['context'].keys())
                    for row in group['data']:
                        row.update(group['context'])
                    results += group['data']
                results = (results, list(group_by))
        else:
            total_pages = response.total_pages if response.total_pages is not None else 0
            results = response.data if response.data is not None else ()
        return results, total_pages

    @staticmethod
    def get_results(dataset_id: str, response: Union[DataQueryResponse, dict], query: DataQuery) -> \
            Union[list, Tuple[list, list]]:
        results, total_pages = GsDataApi._get_results(response)
        if total_pages:
            if query.page is None:
                query.page = total_pages - 1
                results = results + GsDataApi.get_results(dataset_id, GsDataApi.execute_query(dataset_id, query), query)
            elif query.page - 1 > 0:
                query.page -= 1
                results = results + GsDataApi.get_results(dataset_id, GsDataApi.execute_query(dataset_id, query), query)
            else:
                return results
        return results

    @staticmethod
    async def get_results_async(dataset_id: str, response: Union[DataQueryResponse, dict], query: DataQuery) -> \
            Union[list, Tuple[list, list]]:
        results, total_pages = GsDataApi._get_results(response)
        if total_pages and total_pages > 1:
            futures = []
            for page in range(1, total_pages):
                query = deepcopy(query)
                query.page = page
                futures.append(GsDataApi.execute_query_async(dataset_id, query))
            all_responses = await asyncio.gather(*futures, return_exceptions=True)
            for response_crt in all_responses:
                results += GsDataApi._get_results(response_crt)[0]
        return results

    @classmethod
    def last_data(cls, query: Union[DataQuery, MDAPIDataQuery], dataset_id: str = None, timeout: int = None) \
            -> Union[list, tuple]:
        kwargs = {}
        if timeout is not None:
            kwargs['timeout'] = timeout
        if getattr(query, 'marketDataCoordinates', None):
            result = cls._post_with_cache_check('/data/coordinates/query/last', payload=query, **kwargs)
            return result.get('responses', ())
        else:
            domain = cls._check_data_on_cloud(dataset_id)
            result = cls._post_with_cache_check(
                '/data/{}/last/query'.format(dataset_id),
                payload=query,
                domain=domain,
                **kwargs
            )
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
    def _build_params(cls, scroll: str, scroll_id: Optional[str], limit: int, offset: int, fields: List[str],
                      include_history: bool, **kwargs) -> dict:
        params = {'limit': limit or 4000, 'scroll': scroll}
        if scroll_id:
            params['scrollId'] = scroll_id
        if offset:
            params['offset'] = offset
        if fields:
            params['fields'] = fields
        if include_history:
            params['includeHistory'] = 'true'
        params = {**params, **kwargs}
        return params

    @classmethod
    def get_coverage(
            cls,
            dataset_id: str,
            scroll: str = DEFAULT_SCROLL,
            scroll_id: Optional[str] = None,
            limit: int = None,
            offset: int = None,
            fields: List[str] = None,
            include_history: bool = False,
            **kwargs
    ) -> List[dict]:
        session = cls.get_session()
        params = cls._build_params(scroll, scroll_id, limit, offset, fields, include_history, **kwargs)
        body = session._get(f'/data/{dataset_id}/coverage', payload=params)
        results = scroll_results = body['results']
        total_results = body['totalResults']
        while len(scroll_results) and len(results) < total_results:
            scroll_id = body.get('scrollId')
            if scroll_id is None:
                break
            params['scrollId'] = scroll_id
            body = session._get(f'/data/{dataset_id}/coverage', payload=params)
            scroll_results = body['results']
            results += scroll_results

        return results

    @classmethod
    async def get_coverage_async(
            cls,
            dataset_id: str,
            scroll: str = DEFAULT_SCROLL,
            scroll_id: Optional[str] = None,
            limit: int = None,
            offset: int = None,
            fields: List[str] = None,
            include_history: bool = False,
            **kwargs
    ) -> List[dict]:
        session = cls.get_session()
        params = cls._build_params(scroll, scroll_id, limit, offset, fields, include_history, **kwargs)
        body = await session._get_async(f'/data/{dataset_id}/coverage', payload=params)
        results = scroll_results = body['results']
        total_results = body['totalResults']
        while len(scroll_results) and len(results) < total_results:
            params['scrollId'] = body['scrollId']
            body = await session._get_async(f'/data/{dataset_id}/coverage', payload=params)
            scroll_results = body['results']
            if scroll_results:
                results += scroll_results
        return results

    @classmethod
    def create(cls, definition: Union[DataSetEntity, dict]) -> DataSetEntity:
        result = cls.get_session()._post('/data/datasets', payload=definition)
        return result

    @classmethod
    def delete_dataset(cls, dataset_id: str) -> dict:
        result = cls.get_session()._delete(f'/data/datasets/{dataset_id}')
        return result

    @classmethod
    def undelete_dataset(cls, dataset_id: str) -> dict:
        result = cls.get_session()._put(f'/data/datasets/{dataset_id}/undelete')
        return result

    @classmethod
    def update_definition(cls, dataset_id: str, definition: Union[DataSetEntity, dict]) -> DataSetEntity:
        result = cls.get_session()._put('/data/datasets/{}'.format(dataset_id), payload=definition, cls=DataSetEntity)
        return result

    @classmethod
    def upload_data(cls, dataset_id: str, data: Union[pd.DataFrame, list, tuple]) -> dict:
        if isinstance(data, pd.DataFrame):
            # We require the Dataframe to return a list in the 'records' format:
            #  https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_json.html
            data = data.to_json(orient='records')
        # Don't use msgpack for MDS
        session = cls.get_session()
        headers = None if 'us-east' in session.domain else {'Content-Type': 'application/x-msgpack'}
        result = session._post('/data/{}'.format(dataset_id), payload=data, request_headers=headers)
        return result

    @classmethod
    def delete_data(cls, dataset_id: str, delete_query: Dict) -> Dict:
        """
        Delete data from dataset. You must have admin access to the dataset to delete data.
        All data deleted is not recoverable.
        """
        return cls.get_session()._delete(f'/data/{dataset_id}', payload=delete_query, use_body=True)

    @classmethod
    def get_definition(cls, dataset_id: str) -> DataSetEntity:
        definition = cls.__definitions.get(dataset_id)
        if not definition:
            definition = cls.get_session()._get('/data/datasets/{}'.format(dataset_id), cls=DataSetEntity)
            if not definition:
                raise MqValueError('Unknown dataset {}'.format(dataset_id))

            cls.__definitions[dataset_id] = definition

        return definition

    @classmethod
    def get_many_definitions(cls,
                             limit: int = 100,
                             offset: int = None,
                             scroll: str = DEFAULT_SCROLL,
                             scroll_id: Optional[str] = None,
                             ) -> Tuple[DataSetEntity, ...]:

        params = dict(filter(lambda item: item[1] is not None,
                             dict(limit=limit, offset=offset, scroll=scroll, scrollId=scroll_id,
                                  enablePagination='true').items()))

        body = cls.get_session()._get('/data/datasets', payload=params, cls=DataSetEntity)
        results = scroll_results = body['results']
        total_results = body['totalResults']

        while len(scroll_results) and len(results) < total_results:
            params['scrollId'] = body['scrollId']
            body = cls.get_session()._get('/data/datasets', payload=params, cls=DataSetEntity)
            scroll_results = body['results']
            results = results + scroll_results

        return results

    @classmethod
    def get_catalog(cls,
                    dataset_ids: List[str] = None,
                    limit: int = 100,
                    offset: int = None,
                    scroll: str = DEFAULT_SCROLL,
                    scroll_id: Optional[str] = None,
                    ) -> Tuple[DataSetCatalogEntry, ...]:

        query = f'dataSetId={"&dataSetId=".join(dataset_ids)}' if dataset_ids else ''
        gs_session = cls.get_session()
        if len(query):
            return gs_session._get(f'/data/catalog?{query}', cls=DataSetCatalogEntry)['results']
        else:
            params = dict(filter(lambda item: item[1] is not None,
                                 dict(limit=limit, offset=offset, scroll=scroll, scrollId=scroll_id,
                                      enablePagination='true').items()))

            body = gs_session._get('/data/catalog', payload=params, cls=DataSetEntity)
            results = scroll_results = body['results']
            total_results = body['totalResults']

            while len(scroll_results) and len(results) < total_results:
                params['scrollId'] = body['scrollId']
                body = gs_session._get('/data/catalog', payload=params, cls=DataSetEntity)
                scroll_results = body['results']
                results = results + scroll_results

            return results

    @classmethod
    @cachetools.cached(__asset_coordinates_cache)
    def get_many_coordinates(
            cls,
            mkt_type: str = None,
            mkt_asset: str = None,
            mkt_class: str = None,
            mkt_point: Tuple[str, ...] = (),
            *,
            limit: int = 100,
            return_type: type = str,
    ) -> Union[Tuple[str, ...], Tuple[MarketDataCoordinate, ...]]:
        where = FieldFilterMap(
            mkt_type=mkt_type.upper() if mkt_type is not None else None,
            mkt_asset=mkt_asset.upper() if mkt_asset is not None else None,
            mkt_class=mkt_class.upper() if mkt_class is not None else None,
        )
        for index, point in enumerate(mkt_point):
            setattr(where, 'mkt_point' + str(index + 1), point.upper())

        query = EntityQuery(
            where=where,
            limit=limit
        )
        results = cls._post_with_cache_check('/data/mdapi/query', payload=query)['results']

        if return_type is str:
            return tuple(coordinate['name'] for coordinate in results)
        elif return_type is MarketDataCoordinate:
            return tuple(
                MarketDataCoordinate(
                    mkt_type=coordinate['dimensions']['mktType'],
                    mkt_asset=coordinate['dimensions']['mktAsset'],
                    mkt_class=coordinate['dimensions']['mktClass'],
                    mkt_point=tuple(coordinate['dimensions']['mktPoint'].values()),
                    mkt_quoting_style=coordinate['dimensions']['mktQuotingStyle']
                ) for coordinate in results)
        else:
            raise NotImplementedError('Unsupported return type')

    @classmethod
    def _to_zulu(cls, d):
        return d.strftime('%Y-%m-%dT%H:%M:%SZ')

    @classmethod
    def get_mxapi_curve_measure(cls, curve_type=None, curve_asset=None, curve_point=None, curve_tags=None,
                                measure=None, start_time=None, end_time=None, request_id=None,
                                close_location=None, real_time=None) -> pd.DataFrame:
        real_time = real_time or isinstance(start_time, dt.datetime)

        if not start_time:
            if real_time:
                start_time = DataContext.current.start_time
            else:
                start_time = DataContext.current.start_date

        if not end_time:
            if real_time:
                end_time = DataContext.current.end_time
            else:
                end_time = DataContext.current.end_date

        if not real_time and not close_location:
            close_location = 'NYC'

        if real_time and not isinstance(end_time, dt.date):
            raise ValueError("Start and end need to be either both date or both time")

        if real_time:
            request_dict = {
                'type': 'MxAPI Measure Request',
                'modelType': curve_type,
                'modelAsset': curve_asset,
                'point': curve_point,
                'tags': curve_tags,
                'startTime': cls._to_zulu(start_time),
                'endTime': cls._to_zulu(end_time),
                'measureName': measure
            }
        else:
            request_dict = {
                'type': 'MxAPI Measure Request EOD',
                'modelType': curve_type,
                'modelAsset': curve_asset,
                'point': curve_point,
                'tags': curve_tags,
                'startDate': start_time.isoformat(),
                'endDate': end_time.isoformat(),
                'close': close_location,
                'measureName': measure
            }

        url = '/mxapi/mq/measure' if real_time else '/mxapi/mq/measure/eod'

        start = time.perf_counter()
        try:
            body = cls._post_with_cache_check(url, payload=request_dict)
        except Exception as e:
            log_warning(request_id, _logger, f'Mxapi measure query {request_dict} failed due to {e}')
            raise e
        log_debug(request_id, _logger, 'MxAPI measure query (%s) with payload (%s) ran in %.3f ms',
                  body.get('requestId'), request_dict, (time.perf_counter() - start) * 1000)

        if real_time:
            values = body['measures']
            valuation_times = body['measureTimes']
            timestamps = [parser.parse(s) for s in valuation_times]
            column_name = body['measureName']

            d = {column_name: values, 'timeStamp': timestamps}
            df = MarketDataResponseFrame(pd.DataFrame(data=d))
            df = df.set_index('timeStamp')
            return df
        else:
            values = body['measures']
            valuation_date_strings = body['measureDates']
            valuation_dates = [dt.date.fromisoformat(s) for s in valuation_date_strings]
            column_name = body['measureName']

            d = {column_name: values, 'date': valuation_dates}
            df = MarketDataResponseFrame(pd.DataFrame(data=d))
            df = df.set_index('date')
            return df

    @classmethod
    def get_mxapi_vector_measure(cls, curve_type=None, curve_asset=None, curve_point=None, curve_tags=None,
                                 vector_measure=None, as_of_time=None, request_id=None,
                                 close_location=None) -> pd.DataFrame:
        if not vector_measure:
            raise ValueError("Vector measure must be specified.")

        if not as_of_time:
            raise ValueError("As-of date or time must be specified.")

        real_time = isinstance(as_of_time, dt.datetime)

        if not real_time and not isinstance(as_of_time, dt.date):
            raise ValueError("As-of date or time must be specified.")

        if not real_time and not close_location:
            close_location = 'NYC'

        if real_time:
            request_dict = {
                'type': 'MxAPI Curve Request',
                'modelType': curve_type,
                'modelAsset': curve_asset,
                'point': curve_point,
                'tags': curve_tags,
                'asOfTime': cls._to_zulu(as_of_time),
                'curveName': vector_measure
            }
        else:
            request_dict = {
                'type': 'MxAPI Curve Request EOD',
                'modelType': curve_type,
                'modelAsset': curve_asset,
                'point': curve_point,
                'tags': curve_tags,
                'asOfDate': as_of_time.isoformat(),
                'close': close_location,
                'curveName': vector_measure
            }

        url = '/mxapi/mq/curve' if real_time else '/mxapi/mq/curve/eod'

        start = time.perf_counter()
        try:
            body = cls._post_with_cache_check(url, payload=request_dict)
        except Exception as e:
            log_warning(request_id, _logger, f'Mxapi curve query {request_dict} failed due to {e}')
            raise e
        log_debug(request_id, _logger, 'MxAPI curve query (%s) with payload (%s) ran in %.3f ms',
                  body.get('requestId'), request_dict, (time.perf_counter() - start) * 1000)

        values = body['curve']
        value_col_name = body['curveName']
        knots = body['knots']
        column_name = body['knotType']

        if len(values) == 0 and len(body['errMsg']) > 0:
            raise RuntimeError(body['errMsg'])

        d = {value_col_name: values, column_name: knots}
        df = MarketDataResponseFrame(pd.DataFrame(data=d))
        df = df.set_index(column_name)
        return df

    @classmethod
    def get_mxapi_backtest_data(cls, builder, start_time=None, end_time=None, num_samples=120,
                                csa=None, request_id=None, close_location=None, real_time=None) -> pd.DataFrame:
        real_time = real_time or isinstance(start_time, dt.datetime)

        if not start_time:
            if real_time:
                start_time = DataContext.current.start_time
            else:
                start_time = DataContext.current.start_date

        if not end_time:
            if real_time:
                end_time = DataContext.current.end_time
            else:
                end_time = DataContext.current.end_date

        if not csa:
            csa = 'Default'

        if not real_time and not close_location:
            close_location = 'NYC'

        if real_time and not isinstance(end_time, dt.date):
            raise ValueError("Start and end need to be either both date or both time")

        leg = builder.resolve(in_place=False)
        leg_dict_string = json.dumps(leg, cls=JSONEncoder)
        leg_dict = json.loads(leg_dict_string)

        if real_time:
            request_dict = {
                'type': 'MxAPI Backtest Request MQ',
                'builder': leg_dict,
                'startTime': cls._to_zulu(start_time),
                'endTime': cls._to_zulu(end_time),
                'sampleSize': num_samples,
                'csa': csa
            }
        else:
            request_dict = {
                'type': 'MxAPI Backtest Request MQEOD',
                'builder': leg_dict,
                'startDate': start_time.isoformat(),
                'endDate': end_time.isoformat(),
                'sampleSize': num_samples,
                'csa': csa,
                'close': close_location
            }

        url = '/mxapi/mq/backtest' if real_time else '/mxapi/mq/backtest/eod'

        start = time.perf_counter()
        try:
            body = cls._post_with_cache_check(url, payload=request_dict)
        except Exception as e:
            log_warning(request_id, _logger, f'Mxapi backtest query {request_dict} failed due to {e}')
            raise e
        log_debug(request_id, _logger, 'MxAPI backtest query (%s) with payload (%s) ran in %.3f ms',
                  body.get('requestId'), request_dict, (time.perf_counter() - start) * 1000)

        if real_time:
            values = body['valuations']
            valuation_times = body['valuationTimes']
            timestamps = [parser.parse(s) for s in valuation_times]
            column_name = body['valuationName']

            d = {column_name: values, 'timeStamp': timestamps}
            df = MarketDataResponseFrame(pd.DataFrame(data=d))
            df = df.set_index('timeStamp')
            return df
        else:
            values = body['valuations']
            valuation_date_strings = body['valuationDates']
            valuation_dates = [dt.date.fromisoformat(s) for s in valuation_date_strings]
            column_name = body['valuationName']

            d = {column_name: values, 'date': valuation_dates}
            df = MarketDataResponseFrame(pd.DataFrame(data=d))
            df = df.set_index('date')
            return df

    @staticmethod
    def _get_market_data_filters(asset_ids: List[str],
                                 query_type: Union[QueryType, str],
                                 where: Union[FieldFilterMap, Dict] = None,
                                 source: Union[str] = None,
                                 real_time: bool = False,
                                 measure='Curve',
                                 vendor: str = ''):
        inner = {
            'entityIds': asset_ids,
            'queryType': query_type.value if isinstance(query_type, QueryType) else query_type,
            'where': where or {},
            'source': source or 'any',
            'frequency': 'Real Time' if real_time else 'End Of Day',
            'measures': [
                measure
            ]
        }
        if vendor != '':
            inner['vendor'] = vendor
        return inner

    @staticmethod
    def build_interval_chunked_market_data_queries(asset_ids: List[str],
                                                   query_type: Union[QueryType, str],
                                                   where: Union[FieldFilterMap, Dict] = None,
                                                   source: Union[str] = None,
                                                   real_time: bool = False,
                                                   measure='Curve',
                                                   vendor: str = '') -> List[dict]:
        parallel_interval = 365  # chunk over a year

        def chunk_time(start, end) -> tuple:
            # chunk the time interval into 1 year chunks
            s = start
            while s < end:
                e = min(s + dt.timedelta(days=parallel_interval), end)
                yield s, e
                s = e

        queries = []
        if real_time:
            start, end = DataContext.current.start_time, DataContext.current.end_time
            start_key, end_key = 'startTime', 'endTime'
        else:
            start, end = DataContext.current.start_date, DataContext.current.end_date
            start_key, end_key = 'startDate', 'endDate'

        for s, e in chunk_time(start, end):
            inner = copy(GsDataApi._get_market_data_filters(asset_ids, query_type, where, source, real_time, measure,
                                                            vendor))
            inner[start_key], inner[end_key] = s, e
            queries.append({
                'queries': [inner]
            })

        log_debug("", _logger, f"Created {len(queries)} market data queries")

        return queries

    @staticmethod
    def build_market_data_query(asset_ids: List[str],
                                query_type: Union[QueryType, str],
                                where: Union[FieldFilterMap, Dict] = None,
                                source: Union[str] = None,
                                real_time: bool = False,
                                measure='Curve',
                                parallelize_queries: bool = False,
                                vendor: str = '') -> Union[dict, List[dict]]:
        if parallelize_queries:
            return GsDataApi.build_interval_chunked_market_data_queries(asset_ids, query_type, where, source, real_time,
                                                                        measure, vendor)

        inner = GsDataApi._get_market_data_filters(asset_ids, query_type, where, source, real_time, measure, vendor)
        if DataContext.current.interval is not None:
            inner['interval'] = DataContext.current.interval
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
    def get_data_providers(cls,
                           entity_id: str,
                           availability: Optional[Dict] = None) -> Dict:
        """Return daily and real-time data providers

        :param entity_id: identifier of entity i.e. asset, country, subdivision
        :param availability: Optional Measures Availability response for the entity
        :return: dictionary of available data providers

        ** Usage **

        Return a dictionary containing a set of dataset providers for each available data field.
        For each field will return a dict of daily and real-time dataset providers where available.
        """
        response = availability if availability else cls.get_session()._get(f'/data/measures/{entity_id}/availability')
        if 'errorMessages' in response:
            raise MqValueError(f"Data availability request {response['requestId']} "
                               f"failed: {response.get('errorMessages', '')}")

        if 'data' not in response:
            return {}

        providers = {}
        all_data_mappings = sorted(response['data'], key=lambda x: x['rank'], reverse=True)

        for source in all_data_mappings:
            freq = source.get('frequency', 'End Of Day')
            dataset_field = source.get('datasetField', '')
            rank = source.get('rank')

            providers.setdefault(dataset_field, {})

            if rank:
                if freq == 'End Of Day':
                    providers[dataset_field][DataFrequency.DAILY] = source['datasetId']
                elif freq == 'Real Time':
                    providers[dataset_field][DataFrequency.REAL_TIME] = source['datasetId']

        return providers

    @classmethod
    def get_market_data(cls, query, request_id=None, ignore_errors: bool = False) -> pd.DataFrame:
        def validate(body):
            for e in body['responses']:
                container = e['queryResponse'][0]
                if 'errorMessages' in container:
                    msg = f'measure service request {body["requestId"]} failed: {container["errorMessages"]}'
                    raise MqValueError(msg)
            return body

        start = time.perf_counter()
        try:
            body = cls._post_with_cache_check(url='/data/measures', validator=validate, payload=query)
        except Exception as e:
            log_warning(request_id, _logger, f'Market data query {query} failed due to {e}')
            raise e
        log_debug(request_id, _logger, 'market data query (%s) with payload (%s) ran in %.3f ms', body.get('requestId'),
                  query, (time.perf_counter() - start) * 1000)

        ids = []
        parts = []
        for e in body['responses']:
            container = e['queryResponse'][0]
            ids.extend(container.get('dataSetIds', ()))
            if 'errorMessages' in container:
                msg = f'measure service request {body["requestId"]} failed: {container["errorMessages"]}'
                if ignore_errors:
                    log_warning(request_id, _logger, msg)
                else:
                    raise MqValueError(msg)
            if 'response' in container:
                df = MarketDataResponseFrame(container['response']['data'])
                df.set_index('date' if 'date' in df.columns else 'time', inplace=True)
                df.index = pd.to_datetime(df.index)
                parts.append(df)

        log_debug(request_id, _logger, f'fetched data from {ids}')
        df = pd.concat(parts) if len(parts) > 0 else MarketDataResponseFrame()
        df.dataset_ids = tuple(ids)
        return df

    @classmethod
    def __normalise_coordinate_data(
            cls,
            data: Iterable[Union[MDAPIDataQueryResponse, Dict]],
            fields: Optional[Tuple[MDAPIQueryField, ...]] = None
    ) -> Iterable[Iterable[Dict]]:
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

                if not fields and 'value' not in pt:
                    value_field = pt['mktQuotingStyle']
                    pt['value'] = pt.pop(value_field)

                coord_data.append(pt)
            ret.append(coord_data)

        return ret

    @classmethod
    def __df_from_coordinate_data(
            cls,
            data: Iterable[Dict],
            *,
            use_datetime_index: Optional[bool] = True
    ) -> pd.DataFrame:
        df = cls._sort_coordinate_data(pd.DataFrame.from_records(data))
        index_field = next((f for f in ('time', 'date') if f in df.columns), None)
        if index_field and use_datetime_index:
            df = df.set_index(pd.DatetimeIndex(df.loc[:, index_field].values))

        return df

    @classmethod
    def _sort_coordinate_data(
            cls,
            df: pd.DataFrame,
            by: Tuple[str, ...] = ('date', 'time', 'mktType', 'mktAsset', 'mktClass',
                                   'mktPoint', 'mktQuotingStyle', 'value')
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
            pricing_location: Optional[PricingLocation] = None,
            timeout: int = None
    ) -> Union[Dict, pd.DataFrame]:
        """
        Get last value of coordinates data

        :param coordinates: market data coordinate(s)
        :param as_of: snapshot date or time
        :param vendor: data vendor
        :param as_dataframe: whether to return the result as Dataframe
        :param pricing_location: the location where close data has been recorded (not used for real-time query)
        :param timeout: data query timeout; if timeout is not set then the default timeout is used
        :return: Dataframe or dictionary of the returned data

        **Examples**

        >>> coordinate = ("FX Fwd_USD/EUR_Fwd Pt_2y",)
        >>> data = GsDataApi.coordinates_last(coordinate, dt.datetime(2019, 11, 19))
        """
        market_data_coordinates = tuple(cls._coordinate_from_str(coord) if isinstance(coord, str) else coord
                                        for coord in coordinates)
        query = cls.build_query(
            end=as_of,
            market_data_coordinates=market_data_coordinates,
            vendor=vendor,
            pricing_location=pricing_location
        )

        kwargs = {}
        if timeout is not None:
            kwargs['timeout'] = timeout

        data = cls.last_data(query, **kwargs)

        if not as_dataframe:
            ret = {coordinate: None for coordinate in market_data_coordinates}
            for idx, row in enumerate(cls.__normalise_coordinate_data(data)):
                try:
                    ret[market_data_coordinates[idx]] = row[0]['value']
                except IndexError:
                    ret[market_data_coordinates[idx]] = None
            return ret

        ret = []
        datetime_field = 'time' if isinstance(as_of, dt.datetime) else 'date'
        for idx, row in enumerate(cls.__normalise_coordinate_data(data)):
            coordinate_as_dict = market_data_coordinates[idx].as_dict(as_camel_case=True)
            try:
                ret.append(dict(chain(coordinate_as_dict.items(),
                                      (('value', row[0]['value']), (datetime_field, row[0][datetime_field])))))
            except IndexError:
                ret.append(dict(chain(coordinate_as_dict.items(), (('value', None), (datetime_field, None)))))
        return cls.__df_from_coordinate_data(ret, use_datetime_index=False)

    @classmethod
    def coordinates_data(
            cls,
            coordinates: Union[str, MarketDataCoordinate, Iterable[str], Iterable[MarketDataCoordinate]],
            start: Union[dt.datetime, dt.date] = None,
            end: Union[dt.datetime, dt.date] = None,
            vendor: MarketDataVendor = MarketDataVendor.Goldman_Sachs,
            as_multiple_dataframes: bool = False,
            pricing_location: Optional[PricingLocation] = None,
            fields: Optional[Tuple[MDAPIQueryField, ...]] = None,
            **kwargs
    ) -> Union[pd.DataFrame, Tuple[pd.DataFrame]]:
        """
        Get coordinates data

        :param coordinates: market data coordinate(s)
        :param start: start date or time
        :param end: end date or time
        :param vendor: data vendor
        :param as_multiple_dataframes: whether to return the result as one or multiple Dataframe(s)
        :param pricing_location: the location where close data has been recorded (not used for real-time query)
        :param fields: value fields to return
        :param kwargs: Extra query arguments
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
            pricing_location=pricing_location,
            fields=fields,
            **kwargs
        )

        results = cls.__normalise_coordinate_data(cls.query_data(query), fields=fields)

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
            pricing_location: Optional[PricingLocation] = None,
            **kwargs
    ) -> Union[pd.Series, Tuple[pd.Series]]:
        """
        Get coordinates data series

        :param coordinates: market data coordinate(s)
        :param start: start date or time
        :param end: end date or time
        :param vendor: data vendor
        :param pricing_location: the location where close data has been recorded (not used for real-time query)
        :param kwargs: Extra query arguments
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
            as_multiple_dataframes=True,
            **kwargs
        )

        ret = tuple(pd.Series(dtype=float) if df.empty else pd.Series(index=df.index, data=df.value.values)
                    for df in dfs)
        if isinstance(coordinates, (MarketDataCoordinate, str)):
            return ret[0]
        else:
            return ret

    @classmethod
    @cachetools.cached(TTLCache(ttl=3600, maxsize=128))
    def get_types(cls, dataset_id: str):
        results = cls.get_session()._get(f'/data/catalog/{dataset_id}')
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
    def get_field_types(cls, field_names: Union[str, List[str]]):
        try:
            fields = cls.get_dataset_fields(names=field_names, limit=len(field_names))
        except Exception:
            return {}
        if fields:
            field_types = {}
            field: DataSetFieldEntity
            for field in fields:
                field_name = field.name
                field_type = field.type_
                field_format = field.parameters.get('format') if field.parameters else None
                field_types[field_name] = field_format or field_type
            return field_types
        return {}

    @classmethod
    def construct_dataframe_with_types(cls, dataset_id: str, data: Union[Base, List, Tuple],
                                       schema_varies=False, standard_fields=False) -> pd.DataFrame:
        """
        Constructs a dataframe with correct date types.
        :param dataset_id: id of the dataset
        :param data: data to convert with correct types
        :param schema_varies: if set, method will not assume that all rows have the same columns
        :param standard_fields: if set, will use fields api instead of catalog api to get fieldTypes
        :return: dataframe with correct types
        """
        if len(data):
            # Use first row to infer fields from data
            sample = data if schema_varies else [data[0]]
            incoming_data_data_types = pd.DataFrame(sample).dtypes.to_dict()
            dataset_types = cls.get_types(dataset_id) if not standard_fields \
                else cls.get_field_types(field_names=list(incoming_data_data_types.keys()))

            # fallback approach in case fields api doesn't return results
            if dataset_types is {} and standard_fields:
                dataset_types = cls.get_types(dataset_id)

            df = pd.DataFrame(data, columns={**dataset_types, **incoming_data_data_types})

            for field_name, type_name in dataset_types.items():
                if df.get(field_name) is not None and type_name in ('date', 'date-time') and \
                        len(df.get(field_name).value_counts()) > 0:
                    df[field_name] = pd.to_datetime(df[field_name],
                                                    format='ISO8601' if int(
                                                        pd.__version__.split('.')[0]) == 2 else None)

            field_names = dataset_types.keys()

            if 'date' in field_names:
                df = df.set_index('date')
            elif 'time' in field_names:
                df = df.set_index('time')

            return df
        else:
            return pd.DataFrame({})

    @classmethod
    def get_dataset_fields(
            cls,
            ids: Union[str, List[str]] = None,
            names: Union[str, List[str]] = None,
            limit: int = 10,
    ) -> Union[Tuple[DataSetFieldEntity, ...], Tuple[dict, ...]]:
        """
        Get many dataset fields

        :param ids: ID(s) of the field(s)
        :param names: Name(s) of the field(s)
        :param limit: Limit on the number of results returned. Default: 10
        :return: Tuple of DataSetFieldEntity

        **Examples**

        >>> from gs_quant.api.gs.data import GsDataApi
        >>> fields = GsDataApi.get_dataset_fields(names = ['adjustedClosePrice', 'adjustedOpenPrice'])
        """

        where = dict(filter(lambda item: item[1] is not None, dict(id=ids, name=names).items()))
        response = cls.get_session()._post('/data/fields/query',
                                           payload={'where': where, 'limit': limit},
                                           cls=DataSetFieldEntity)
        return response['results']

    @classmethod
    def create_dataset_fields(
            cls,
            fields: List[DataSetFieldEntity]
    ) -> Union[Tuple[DataSetFieldEntity, ...], Tuple[dict, ...]]:
        """
        Create many dataset fields

        :param fields: Fields to be created
        :return: Tuple of DataSetFieldEntity

        **Examples**

        >>> from gs_quant.api.gs.data import GsDataApi
        >>> from gs_quant.target.data import DataSetFieldEntity
        >>> fields = [
        >>>     DataSetFieldEntity(name='price', type_='number', description='Price of the instrument.'),
        >>>     DataSetFieldEntity(name='strikeReference', type_='string', description='Reference for strike level.',
        >>>                        parameters={'enum': ['delta', 'spot', 'forward', 'normalized']})
        >>> ]
        >>> GsDataApi.create_dataset_fields(fields)
        """
        params = {'fields': fields}
        response = cls.get_session()._post('/data/fields/bulk', payload=params, cls=DataSetFieldEntity)
        return response['results']

    @classmethod
    def update_dataset_fields(
            cls,
            fields: List[DataSetFieldEntity]
    ) -> Union[Tuple[DataSetFieldEntity, ...], Tuple[dict, ...]]:
        """
        Update many dataset fields

        :param fields: Fields to be created
        :return: Tuple of DataSetFieldEntity

        **Examples**

        >>> from gs_quant.api.gs.data import GsDataApi
        >>> from gs_quant.target.data import DataSetFieldEntity
        >>> fields = [
        >>>     DataSetFieldEntity(id='FIMFMQ0P19AZ2XK9', name='price', type_='number',
        >>>                        description='Price of the instrument.'),
        >>>     DataSetFieldEntity(id='FI7EFDC3SQQBMDX8', name='strikeReference', type_='string',
        >>>                        description='Reference for strike level.',
        >>>                        parameters={'enum': ['delta', 'spot', 'forward', 'normalized']})
        >>> ]
        >>> GsDataApi.update_dataset_fields(fields)
        """
        params = {'fields': fields}
        response = cls.get_session()._put('/data/fields/bulk', payload=params, cls=DataSetFieldEntity)
        return response['results']


class MarketDataResponseFrame(pd.DataFrame):
    _internal_names = pd.DataFrame._internal_names + ['dataset_ids']
    _internal_names_set = set(_internal_names)

    @property
    def _constructor(self):
        return MarketDataResponseFrame
