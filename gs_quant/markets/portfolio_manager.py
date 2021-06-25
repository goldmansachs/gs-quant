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
from time import sleep
from typing import List, Union

import pandas as pd
from dateutil.relativedelta import relativedelta

from gs_quant.api.gs.portfolios import GsPortfolioApi
from gs_quant.datetime import business_day_offset
from gs_quant.entities.entitlements import Entitlements
from gs_quant.errors import MqValueError
from gs_quant.markets.report import FactorRiskReport, PerformanceReport, ReportJobFuture, Report
from gs_quant.target.reports import ReportType

_logger = logging.getLogger(__name__)


class PortfolioManager:
    """

    Portfolio Manager is used to manage Marquee portfolios (setting entitlements, running and retrieving reports, etc)

    """

    def __init__(self,
                 portfolio_id: str):
        """
        Initialize a Portfolio Manager
        :param portfolio_id: Portfolio ID
        """
        self.__portfolio_id = portfolio_id

    @property
    def portfolio_id(self) -> str:
        return self.__portfolio_id

    @portfolio_id.setter
    def portfolio_id(self, value: str):
        self.__portfolio_id = value

    def get_reports(self) -> List[Report]:
        """
        Get a list of all reports associated with the portfolio
        :return: list of Report objects
        """
        reports = []
        reports_as_targets = GsPortfolioApi.get_reports(self.__portfolio_id)
        for report_target in reports_as_targets:
            if report_target.type in [ReportType.Portfolio_Factor_Risk, ReportType.Asset_Factor_Risk]:
                reports.append(FactorRiskReport.from_target(report_target))
            if report_target.type == ReportType.Portfolio_Performance_Analytics:
                reports.append(PerformanceReport.from_target(report_target))
        return reports

    def schedule_reports(self,
                         start_date: dt.date = None,
                         end_date: dt.date = None,
                         backcast: bool = False):
        if None in [start_date, end_date]:
            suggested_schedule_dates = self.get_schedule_dates(backcast)
            start_date = start_date if start_date else suggested_schedule_dates[0]
            end_date = end_date if end_date else suggested_schedule_dates[1]
        GsPortfolioApi.schedule_reports(self.__portfolio_id, start_date, end_date, backcast=backcast)

    def run_reports(self,
                    start_date: dt.date = None,
                    end_date: dt.date = None,
                    backcast: bool = False,
                    is_async: bool = True) -> List[Union[pd.DataFrame, ReportJobFuture]]:
        """
        Run all reports associated with a portfolio
        :param start_date: start date of report job
        :param end_date: end date of report job
        :param backcast: true if reports should be backcasted; defaults to false
        :param is_async: true if reports should run asynchronously; defaults to true
        :return: if is_async is true, returns a list of ReportJobFuture objects; if is_async is false, returns a list
        of dataframe objects containing report results for all portfolio results
        """
        self.schedule_reports(start_date, end_date, backcast)
        reports = self.get_reports()
        report_futures = [report.get_most_recent_job() for report in reports]
        if is_async:
            return report_futures
        counter = 100
        while counter > 0:
            is_done = [future.done() for future in report_futures]
            if False not in is_done:
                return [job_future.result() for job_future in report_futures]
            sleep(6)
        raise MqValueError(f'Your reports for Portfolio {self.__portfolio_id} are taking longer than expected '
                           f'to finish. Please contact the Marquee Analytics team at '
                           f'gs-marquee-analytics-support@gs.com')

    def set_entitlements(self,
                         entitlements: Entitlements):
        """
        Set the entitlements of a portfolio
        :param entitlements: Entitlements object
        """
        entitlements_as_target = entitlements.to_target()
        portfolio_as_target = GsPortfolioApi.get_portfolio(self.__portfolio_id)
        portfolio_as_target.entitlements = entitlements_as_target
        GsPortfolioApi.update_portfolio(portfolio_as_target)

    def get_schedule_dates(self,
                           backcast: bool) -> List[dt.date]:
        """
        Get recommended start and end dates for a portfolio report scheduling job
        :param backcast: true if reports should be backcasted
        :return: a list of two dates, the first is the suggested start date and the second is the suggested end date
        """
        position_dates = GsPortfolioApi.get_position_dates(self.__portfolio_id)
        if len(position_dates) == 0:
            raise MqValueError('Cannot schedule reports for a portfolio with no positions.')
        if backcast:
            start_date = business_day_offset(min(position_dates) - relativedelta(years=1), -1, roll='forward')
            end_date = min(position_dates)
        else:
            start_date = min(position_dates)
            end_date = max(position_dates)
        return [start_date, end_date]
