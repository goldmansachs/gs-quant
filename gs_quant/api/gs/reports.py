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
from typing import Tuple

from gs_quant.session import GsSession
from gs_quant.target.reports import Report, ReportScheduleRequest, ReportJob

_logger = logging.getLogger(__name__)


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
                    position_source_id: str = None, status: str = None, report_type: str = None) \
            -> Tuple[Report, ...]:
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
            url += '&type={report_type}'.format(report_type=report_type)
        return GsSession.current._get(url, cls=Report)['results']

    @classmethod
    def update_report(cls, report: Report) -> dict:
        return GsSession.current._put('/reports/{id}'.format(id=report.id), report, cls=Report)

    @classmethod
    def delete_report(cls, report_id: str) -> dict:
        return GsSession.current._delete('/reports/{id}'.format(id=report_id))

    @classmethod
    def schedule_report(cls, report_id: str, start_date: dt.date, end_date: dt.date) -> dict:
        report_schedule_request = ReportScheduleRequest(startDate=start_date, endDate=end_date)
        return GsSession.current._post('/reports/{id}/schedule'.format(id=report_id), report_schedule_request,
                                       cls=ReportScheduleRequest)

    @classmethod
    def get_report_status(cls, report_id: str) -> Tuple[dict, ...]:
        return GsSession.current._get('/reports/{id}/status'.format(id=report_id))

    @classmethod
    def get_report_jobs(cls, report_id: str) -> Tuple[ReportJob, ...]:
        return GsSession.current._get('/reports/{id}/jobs'.format(id=report_id))['results']

    @classmethod
    def get_report_job(cls, report_job_id: str) -> dict:
        return GsSession.current._get('/reports/jobs/{report_job_id}'.format(report_job_id=report_job_id))

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
