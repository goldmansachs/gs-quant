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
import urllib.parse
from enum import Enum
from typing import Tuple, List

from gs_quant.base import EnumBase
from gs_quant.session import GsSession
from gs_quant.target.common import Currency
from gs_quant.target.reports import Report

_logger = logging.getLogger(__name__)


class OrderType(EnumBase, Enum):
    """Source object for position data"""

    Ascending = 'Ascending'
    Descending = 'Descending'


class FactorRiskTableMode(EnumBase, Enum):
    """Source object for position data"""

    Pnl = 'Pnl'
    Exposure = 'Exposure'
    ZScore = 'ZScore'
    Mctr = 'Mctr'


class GsReportApi:
    """GS Reports API client implementation"""

    @classmethod
    def create_report(cls, report: Report) -> Report:
        return GsSession.current._post('/reports', report, cls=Report)

    @classmethod
    def get_report(cls, report_id: str) -> Report:
        return GsSession.current._get('/reports/{id}'.format(id=report_id), cls=Report)

    @classmethod
    def get_reports(cls, limit: int = 100, offset: int = None, position_source_type: str = None,
                    position_source_id: str = None, status: str = None, report_type: str = None,
                    order_by: str = None) -> Tuple[Report, ...]:
        url = '/reports?limit={limit}'.format(limit=limit)
        if offset is not None:
            url += '&offset={offset}'.format(offset=offset)
        if position_source_type is not None:
            url += '&positionSourceType={pst}'.format(pst=position_source_type)
        if position_source_id is not None:
            url += '&positionSourceId={psi}'.format(psi=position_source_id)
        if status is not None:
            url += '&status={status}'.format(status=status)
        if report_type is not None:
            url += '&reportType={report_type}'.format(report_type=urllib.parse.quote(report_type))
        if order_by is not None:
            url += '&orderBy={order_by}'.format(order_by=order_by)
        return GsSession.current._get(url, cls=Report)['results']

    @classmethod
    def update_report(cls, report: Report) -> dict:
        return GsSession.current._put('/reports/{id}'.format(id=report.id), report, cls=Report)

    @classmethod
    def delete_report(cls, report_id: str) -> dict:
        return GsSession.current._delete('/reports/{id}'.format(id=report_id))

    @classmethod
    def schedule_report(cls, report_id: str, start_date: dt.date, end_date: dt.date, backcast: bool = False) -> dict:
        report_schedule_request = {
            'startDate': start_date.strftime('%Y-%m-%d'),
            'endDate': end_date.strftime('%Y-%m-%d')
        }
        if backcast:
            report_schedule_request['parameters'] = {'backcast': backcast}
        return GsSession.current._post('/reports/{id}/schedule'.format(id=report_id), report_schedule_request)

    @classmethod
    def get_report_status(cls, report_id: str) -> Tuple[dict, ...]:
        return GsSession.current._get('/reports/{id}/status'.format(id=report_id))

    @classmethod
    def get_report_jobs(cls, report_id: str) -> Tuple[dict]:
        return GsSession.current._get('/reports/{id}/jobs'.format(id=report_id))['results']

    @classmethod
    def get_report_job(cls, report_job_id: str) -> dict:
        return GsSession.current._get('/reports/jobs/{report_job_id}'.format(report_job_id=report_job_id))

    @classmethod
    def reschedule_report_job(cls, report_job_id: str):
        return GsSession.current._post(f'/reports/jobs/{report_job_id}/reschedule', {})

    @classmethod
    def cancel_report_job(cls, report_job_id: str) -> dict:
        return GsSession.current._post('/reports/jobs/{report_job_id}/cancel'.format(report_job_id=report_job_id))

    @classmethod
    def update_report_job(cls, report_job_id: str, status: str) -> dict:
        status_body = {
            "status": '{status}'.format(status=status)
        }
        return GsSession.current._post('/reports/jobs/{report_job_id}/update'.format(report_job_id=report_job_id),
                                       status_body)

    @classmethod
    def get_factor_risk_report_results(cls,
                                       risk_report_id: str,
                                       view: str = None,
                                       factors: List[str] = None,
                                       factor_categories: List[str] = None,
                                       currency: Currency = None,
                                       start_date: dt.date = None,
                                       end_date: dt.date = None,
                                       unit: str = None) -> dict:
        url = f'/risk/factors/reports/{risk_report_id}/results?'
        if view is not None:
            url += f'&view={view}'
        if factors is not None:
            factors = map(urllib.parse.quote, factors)  # to support factors like "Automobiles & Components"
            url += f'&factors={"&factors=".join(factors)}'
        if factor_categories is not None:
            url += f'&factorCategories={"&factorCategories=".join(factor_categories)}'
        if currency is not None:
            url += f'&currency={currency.value}'
        if start_date is not None:
            url += f'&startDate={start_date.strftime("%Y-%m-%d")}'
        if end_date is not None:
            url += f'&endDate={end_date.strftime("%Y-%m-%d")}'
        if unit is not None:
            url += f'&unit={unit}'

        return GsSession.current._get(url)

    @classmethod
    def get_factor_risk_report_view(cls,
                                    risk_report_id: str,
                                    view: str = None,
                                    factor: str = None,
                                    factor_category: str = None,
                                    currency: Currency = None,
                                    start_date: dt.date = None,
                                    end_date: dt.date = None,
                                    unit: str = None) -> dict:

        query_string = urllib.parse.urlencode(
            dict(filter(lambda item: item[1] is not None,
                        dict(view=view, factor=factor, factorCategory=factor_category,
                             currency=currency, startDate=start_date, endDate=end_date, unit=unit).items())))

        url = f'/risk/factors/reports/{risk_report_id}/views?{query_string}'
        return GsSession.current._get(url)

    @classmethod
    def get_factor_risk_report_table(cls,
                                     risk_report_id: str,
                                     mode: FactorRiskTableMode = None,
                                     factors: List[str] = None,
                                     factor_categories: List[str] = None,
                                     unit: str = None,
                                     currency: Currency = None,
                                     date: dt.date = None,
                                     start_date: dt.date = None,
                                     end_date: dt.date = None,
                                     order_by_column: str = None,
                                     order_type: OrderType = None) -> dict:
        url = f'/risk/factors/reports/{risk_report_id}/tables?'
        if mode is not None:
            url += f'&mode={mode.value}'
        if unit is not None:
            url += f'&unit={unit}'
        if currency is not None:
            url += f'&currency={currency.value}'
        if date is not None:
            url += f'&date={date.strftime("%Y-%m-%d")}'
        if start_date is not None:
            url += f'&startDate={start_date.strftime("%Y-%m-%d")}'
        if end_date is not None:
            url += f'&endDate={end_date.strftime("%Y-%m-%d")}'
        if factors is not None:
            factors = map(urllib.parse.quote, factors)
            url += f'&factor={"&factor=".join(factors)}'
        if factor_categories is not None:
            url += f'&factorCategory={"&factorCategory=".join(factor_categories)}'
        if order_by_column is not None:
            url += f'&orderByColumn={order_by_column}'
        if order_type is not None:
            url += f'&orderType={order_type}'

        return GsSession.current._get(url)

    @classmethod
    def get_brinson_attribution_results(cls,
                                        portfolio_id: str,
                                        benchmark: str = None,
                                        currency: Currency = None,
                                        include_interaction: bool = None,
                                        aggregation_type: str = None,
                                        start_date: dt.date = None,
                                        end_date: dt.date = None):
        url = f'/attribution/{portfolio_id}/brinson?'
        if benchmark is not None:
            url += f'&benchmark={benchmark}'
        if currency is not None:
            url += f'&currency={currency.value}'
        if include_interaction is not None:
            url += f'&includeInteraction={str(include_interaction).lower()}'
        if aggregation_type is not None:
            url += f'&aggregationType={aggregation_type}'
        if start_date is not None:
            url += f'&startDate={start_date.strftime("%Y-%m-%d")}'
        if end_date is not None:
            url += f'&endDate={end_date.strftime("%Y-%m-%d")}'

        return GsSession.current._get(url)
