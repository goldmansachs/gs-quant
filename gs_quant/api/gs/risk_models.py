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
from typing import Tuple, Dict, List

from gs_quant.session import GsSession
from gs_quant.target.risk_models import RiskModel, RiskModelCalendar, RiskModelFactor, Term, RiskModelData, Format, \
    DataAssetsRequest, Measures

_logger = logging.getLogger(__name__)


class GsRiskModelApi:
    """GS Risk Models API client implementation"""

    @classmethod
    def create_risk_model(cls, model: RiskModel) -> RiskModel:
        return GsSession.current._post('/risk/models', model, cls=RiskModel)

    @classmethod
    def get_risk_model(cls, model_id: str) -> RiskModel:
        return GsSession.current._get('/risk/models/{id}'.format(id=model_id), cls=RiskModel)

    @classmethod
    def get_risk_models(cls,
                        ids: List[str] = None,
                        limit: int = 100,
                        offset: int = None,
                        terms: List[str] = None,
                        last_updated_by_ids: List[str] = None,
                        created_by_ids: List[str] = None,
                        versions: List[str] = None,
                        owner_ids: List[str] = None,
                        vendors: List[str] = None,
                        names: List[str] = None,
                        descriptions: List[str] = None,
                        coverages: List[str] = None) -> Tuple[RiskModel, ...]:
        url = '/risk/models?limit={limit}'.format(limit=limit)
        if ids is not None:
            url += '&id={ids}'.format(ids='&id='.join(ids))
        if offset is not None:
            url += '&offset={offset}'.format(offset=offset)
        if terms is not None:
            url += '&term={terms}'.format(terms='&term='.join(terms))
        if last_updated_by_ids is not None:
            url += '&lastUpdatedById={ids}'.format(ids='&lastUpdatedById='.join(last_updated_by_ids))
        if created_by_ids is not None:
            url += '&createdById={ids}'.format(ids='&createdById='.join(created_by_ids))
        if versions is not None:
            url += '&version={versions}'.format(versions='&version='.join(versions))
        if owner_ids is not None:
            url += '&ownerId={ids}'.format(ids='&ownerId='.join(owner_ids))
        if vendors is not None:
            url += '&vendor={vendors}'.format(vendors='&vendor='.join(vendors))
        if names is not None:
            url += '&name={names}'.format(names='&name='.join(names))
        if descriptions is not None:
            url += '&description={des}'.format(des='&description='.join(descriptions))
        if coverages is not None:
            url += '&coverage={cov}'.format(cov='&coverage='.join(coverages))

        return GsSession.current._get(url, cls=RiskModel)['results']

    @classmethod
    def update_risk_model(cls, model: RiskModel) -> RiskModel:
        return GsSession.current._put('/risk/models/{id}'.format(id=model.id), model, cls=RiskModel)

    @classmethod
    def delete_risk_model(cls, model_id: str) -> Dict:
        return GsSession.current._delete('/risk/models/{id}'.format(id=model_id))

    @classmethod
    def get_risk_model_calendar(cls, model_id: str) -> RiskModelCalendar:
        return GsSession.current._get('/risk/models/{id}/calendar'.format(id=model_id), cls=RiskModelCalendar)

    @classmethod
    def upload_risk_model_calendar(cls, model_id: str, model_calendar: RiskModelCalendar) -> RiskModelCalendar:
        return GsSession.current._put('/risk/models/{id}/calendar'.format(id=model_id), model_calendar,
                                      cls=RiskModelCalendar)

    @classmethod
    def get_risk_model_dates(cls,
                             model_id: str,
                             start_date: dt.datetime = None,
                             end_date: dt.datetime = None) -> List:
        url = '/risk/models/{id}/dates'
        if start_date is not None:
            url += '&startDate={date}'.format(date=start_date.strftime('%Y-%m-%d'))
        if end_date is not None:
            url += '&endDate={date}'.format(date=end_date.strftime('%Y-%m-%d'))
        return GsSession.current._get(url.format(id=model_id))['results']

    @classmethod
    def get_risk_model_factors(cls, model_id: str) -> Tuple[RiskModelFactor, ...]:
        return GsSession.current._get('/risk/models/{id}/factors'.format(id=model_id), cls=RiskModelFactor)['results']

    @classmethod
    def create_risk_model_factor(cls, model_id: str, factor: RiskModelFactor) -> RiskModelFactor:
        return GsSession.current._post('/risk/models/{id}/factors'.format(id=model_id), factor, cls=RiskModelFactor)

    @classmethod
    def get_risk_model_factor(cls, model_id: str, factor_id: str) -> RiskModelFactor:
        return GsSession.current._get(
            '/risk/models/{id}/factors/{identifier}'.format(id=model_id, identifier=factor_id), cls=RiskModelFactor)

    @classmethod
    def update_risk_model_factor(cls, model_id: str, factor_id: str, factor: RiskModelFactor) -> RiskModelFactor:
        return GsSession.current._put(
            '/risk/models/{id}/factors/{identifier}'.format(id=model_id, identifier=factor_id), factor,
            cls=RiskModelFactor)

    @classmethod
    def delete_risk_model_factor(cls, model_id: str, factor_id: str) -> Dict:
        return GsSession.current._delete(
            '/risk/models/{id}/factors/{identifier}'.format(id=model_id, identifier=factor_id))

    @classmethod
    def get_risk_model_factor_data(cls,
                                   model_id: str,
                                   start_date: dt.datetime = None,
                                   end_date: dt.datetime = None,
                                   identifiers: List[str] = None,
                                   include_performance_curve: bool = None) -> List[Dict]:
        url = '/risk/models/{id}/factors/data'.format(id=model_id)

        if start_date is not None:
            url += '&startDate={date}'.format(date=start_date.strftime('%Y-%m-%d'))
        if end_date is not None:
            url += '&endDate={date}'.format(date=end_date.strftime('%Y-%m-%d'))
        if identifiers is not None:
            url += '&identifier={ids}'.format(ids='&identifier='.join(identifiers))
        if include_performance_curve is not None:
            url += '&includePerformanceCurve={curve}'.format(curve=include_performance_curve)

        return GsSession.current._get(url)['results']

    @classmethod
    def get_risk_model_coverage(cls,
                                asset_ids: List[str] = None,
                                as_of_date: dt.datetime = None,
                                sort_by_term: Term = None) -> List[Dict]:
        query = {}
        if asset_ids is not None:
            query['assetIds'] = asset_ids
        if as_of_date is not None:
            query['asOfDate'] = as_of_date.strftime('%Y-%m-%d')
        if sort_by_term is not None:
            query['sortByTerm'] = sort_by_term
        return GsSession.current._post('/risk/models/coverage', query)['results']

    @classmethod
    def upload_risk_model_data(cls, model_id: str, model_data: RiskModelData) -> RiskModelData:
        return GsSession.current._post('/risk/models/data/{id}'.format(id=model_id), model_data, cls=RiskModelData)

    @classmethod
    def get_risk_model_data(cls, model_id: str, start_date: dt.date, end_date: dt.date,
                            assets: DataAssetsRequest = None, measures: List[Measures] = None,
                            limit_factors: bool = None, format: Format = None) -> Dict:
        query = {
            'startDate': start_date.strftime('%Y-%m-%d'),
            'endDate': end_date.strftime('%Y-%m-%d')
        }
        if assets is not None:
            query['assets'] = assets
        if measures is not None:
            query['measures'] = measures
        if limit_factors is not None:
            query['limitFactors'] = limit_factors
        if format is not None:
            query['format'] = format
        return GsSession.current._post('/risk/models/data/{id}/query'.format(id=model_id), query)
