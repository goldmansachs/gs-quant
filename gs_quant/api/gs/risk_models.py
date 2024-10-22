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
import logging
from typing import Tuple, Dict, List, Union

import backoff

from gs_quant.errors import MqRateLimitedError, MqTimeoutError, MqInternalServerError
from gs_quant.session import GsSession
from gs_quant.target.risk_models import RiskModel, RiskModelCalendar, Factor, RiskModelData, \
    RiskModelDataAssetsRequest, RiskModelDataMeasure, RiskModelEventType, RiskModelTerm

_logger = logging.getLogger(__name__)


class GsRiskModelApi:
    """GS Risk Models API client implementation"""

    @classmethod
    def create_risk_model(cls, model: RiskModel) -> RiskModel:
        return GsSession.current._post('/risk/models', model, cls=RiskModel)

    @classmethod
    @backoff.on_exception(lambda: backoff.expo(base=2, factor=2),
                          (MqTimeoutError, MqInternalServerError),
                          max_tries=5)
    @backoff.on_exception(lambda: backoff.constant(90),
                          MqRateLimitedError,
                          max_tries=5)
    def get_risk_model(cls, model_id: str) -> RiskModel:
        return GsSession.current._get(f'/risk/models/{model_id}', cls=RiskModel)

    @classmethod
    def get_risk_models(cls,
                        ids: List[str] = None,
                        limit: int = None,
                        offset: int = None,
                        terms: List[str] = None,
                        versions: List[str] = None,
                        vendors: List[str] = None,
                        names: List[str] = None,
                        types: List[str] = None,
                        coverages: List[str] = None) -> Tuple[RiskModel, ...]:
        url = '/risk/models?'
        if limit:
            url += f'&limit={limit}'
        if ids:
            url += '&id={ids}'.format(ids='&id='.join(ids))
        if offset:
            url += f'&offset={offset}'
        if terms:
            url += f'&term={terms}'
        if versions:
            url += '&version={versions}'.format(versions='&version='.join(versions))
        if vendors:
            url += '&vendor={vendors}'.format(vendors='&vendor='.join(vendors))
        if names is not None:
            url += '&name={names}'.format(names='&name='.join(names))
        if coverages is not None:
            url += '&coverage={cov}'.format(cov='&coverage='.join(coverages))
        if types is not None:
            url += '&type={type}'.format(type='&type='.join(types))
        return GsSession.current._get(url, cls=RiskModel)['results']

    @classmethod
    def update_risk_model(cls, model: RiskModel) -> RiskModel:
        return GsSession.current._put(f'/risk/models/{model.id}', model, cls=RiskModel)

    @classmethod
    def delete_risk_model(cls, model_id: str) -> Dict:
        return GsSession.current._delete(f'/risk/models/{model_id}')

    @classmethod
    @backoff.on_exception(lambda: backoff.expo(base=2, factor=2),
                          (MqTimeoutError, MqInternalServerError),
                          max_tries=5)
    @backoff.on_exception(lambda: backoff.constant(90),
                          MqRateLimitedError,
                          max_tries=5)
    def get_risk_model_calendar(cls, model_id: str) -> RiskModelCalendar:
        return GsSession.current._get(f'/risk/models/{model_id}/calendar', cls=RiskModelCalendar)

    @classmethod
    def upload_risk_model_calendar(cls, model_id: str, model_calendar: RiskModelCalendar) -> RiskModelCalendar:
        return GsSession.current._put(f'/risk/models/{model_id}/calendar', model_calendar, cls=RiskModelCalendar)

    @classmethod
    @backoff.on_exception(lambda: backoff.expo(base=2, factor=2),
                          (MqTimeoutError, MqInternalServerError),
                          max_tries=5)
    @backoff.on_exception(lambda: backoff.constant(90),
                          MqRateLimitedError,
                          max_tries=5)
    def get_risk_model_dates(cls,
                             model_id: str,
                             start_date: dt.date = None,
                             end_date: dt.date = None,
                             event_type: RiskModelEventType = None) -> List:
        url = f'/risk/models/{model_id}/dates?'
        if start_date is not None:
            url += f'&startDate={start_date.strftime("%Y-%m-%d")}'
        if end_date is not None:
            url += f'&endDate={end_date.strftime("%Y-%m-%d")}'
        if event_type is not None:
            url += f'&eventType={event_type.value}'
        return GsSession.current._get(url)['results']


class GsFactorRiskModelApi(GsRiskModelApi):
    def __init__(
            self
    ):
        super().__init__()

    @classmethod
    def get_risk_model_factors(cls, model_id: str) -> Tuple[Factor, ...]:
        return GsSession.current._get(f'/risk/models/{model_id}/factors', cls=Factor)['results']

    @classmethod
    def create_risk_model_factor(cls, model_id: str, factor: Factor) -> Factor:
        return GsSession.current._post(f'/risk/models/{model_id}/factors', factor, cls=Factor)

    @classmethod
    def get_risk_model_factor(cls, model_id: str, factor_id: str) -> Factor:
        return GsSession.current._get(f'/risk/models/{model_id}/factors/{factor_id}')

    @classmethod
    def update_risk_model_factor(cls, model_id: str, factor: Factor) -> Factor:
        url = f'/risk/models/{model_id}/factors/{factor.identifier}'
        return GsSession.current._put(url, factor, cls=Factor)

    @classmethod
    def delete_risk_model_factor(cls, model_id: str, factor_id: str) -> Dict:
        return GsSession.current._delete(f'/risk/models/{model_id}/factors/{factor_id}')

    @classmethod
    @backoff.on_exception(lambda: backoff.expo(base=2, factor=2),
                          (MqTimeoutError, MqInternalServerError),
                          max_tries=5)
    @backoff.on_exception(lambda: backoff.constant(90),
                          MqRateLimitedError,
                          max_tries=5)
    def get_risk_model_factor_data(cls,
                                   model_id: str,
                                   start_date: dt.date = None,
                                   end_date: dt.date = None,
                                   identifiers: List[str] = None,
                                   include_performance_curve: bool = False,
                                   factor_categories: List[str] = None,
                                   names: List[str] = None) -> List[Dict]:
        url = f'/risk/models/{model_id}/factors/data?'
        if start_date is not None:
            url += f'&startDate={start_date.strftime("%Y-%m-%d")}'
        if end_date is not None:
            url += f'&endDate={end_date.strftime("%Y-%m-%d")}'
        if identifiers is not None:
            url += '&identifiers={ids}'.format(ids='&identifiers='.join(identifiers))
        if include_performance_curve:
            url += '&includePerformanceCurve=true'
        if names:
            url += '&name={names}'.format(names='&name='.join(names))
        if factor_categories:
            url += '&factorCategory={factor_categories}'\
                .format(factor_categories='&factorCategory='.join(factor_categories))
        return GsSession.current._get(url)['results']

    @classmethod
    def get_risk_model_coverage(cls,
                                asset_ids: List[str] = None,
                                as_of_date: dt.datetime = None,
                                sort_by_term: RiskModelTerm = None) -> List[Dict]:
        query = {}
        if asset_ids is not None:
            query['assetIds'] = asset_ids
        if as_of_date is not None:
            query['asOfDate'] = as_of_date.strftime('%Y-%m-%d')
        if sort_by_term is not None:
            query['sortByTerm'] = sort_by_term
        return GsSession.current._post('/risk/models/coverage', query, timeout=200)['results']

    @classmethod
    def upload_risk_model_data(cls,
                               model_id: str,
                               model_data: Union[Dict, RiskModelData],
                               partial_upload: bool = False,
                               target_universe_size: float = None,
                               final_upload: bool = None,
                               aws_upload: bool = False) -> str:
        url = f'/risk/models/data/{model_id}'
        if partial_upload:
            url += '?partialUpload=true'
            if target_universe_size:
                url += f'&targetUniverseSize={target_universe_size}'
            if final_upload is not None:
                final_upload_flag = 'true' if final_upload else 'false'
                url += f'&finalUpload={final_upload_flag}'
            if aws_upload:
                url += '&awsUpload=true'
        else:
            if aws_upload:
                url += '?awsUpload=true'
        return GsSession.current._post(url, model_data, timeout=200)

    @classmethod
    @backoff.on_exception(lambda: backoff.expo(base=2, factor=2),
                          (MqTimeoutError, MqInternalServerError),
                          max_tries=5)
    @backoff.on_exception(lambda: backoff.constant(90),
                          MqRateLimitedError,
                          max_tries=5)
    def get_risk_model_data(cls, model_id: str, start_date: dt.date, end_date: dt.date = None,
                            assets: RiskModelDataAssetsRequest = None, measures: List[RiskModelDataMeasure] = None,
                            factors: list = None, limit_factors: bool = None) -> Dict:
        end_date = cls.get_risk_model_dates(model_id)[-1] if not end_date else end_date.strftime('%Y-%m-%d')
        query = {
            'startDate': start_date.strftime('%Y-%m-%d'),
            'endDate': end_date
        }
        if assets is not None:
            query['assets'] = assets
        if measures is not None:
            query['measures'] = measures
        if factors is not None:
            query['factors'] = factors
        if limit_factors is not None:
            query['limitFactors'] = limit_factors
        return GsSession.current._post(f'/risk/models/data/{model_id}/query', query, timeout=200)
