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
from time import sleep
from typing import Tuple, Union, List, Dict
import pandas as pd

from gs_quant.api.gs.data import GsDataApi
from gs_quant.api.gs.portfolios import GsPortfolioApi
from gs_quant.api.gs.reports import GsReportApi
from gs_quant.errors import MqValueError
from gs_quant.models.risk_model import ReturnFormat
from gs_quant.markets.report_utils import _get_ppaa_batches

from gs_quant.target.common import ReportParameters, Currency
from gs_quant.target.coordinates import MDAPIDataBatchResponse
from gs_quant.target.data import DataQuery, DataQueryResponse
from gs_quant.target.reports import Report as TargetReport
from gs_quant.target.reports import ReportType, PositionSourceType, ReportStatus


class ReportDataset(Enum):
    PPA_DATASET = "PPA"
    PFR_DATASET = "PFR"
    AFR_DATASET = "AFR"
    PORTFOLIO_CONSTITUENTS = "PORTFOLIO_CONSTITUENTS"


class ReportJobFuture:
    def __init__(self,
                 report_id: str,
                 job_id: str,
                 report_type: ReportType,
                 start_date: dt.date,
                 end_date: dt.date):
        self.__report_id = report_id
        self.__job_id = job_id
        self.__report_type = report_type
        self.__start_date = start_date
        self.__end_date = end_date

    def status(self) -> ReportStatus:
        job = GsReportApi.get_report_job(self.__job_id)
        return ReportStatus(job.get('status'))

    def done(self) -> bool:
        return self.status() in [ReportStatus.done, ReportStatus.error, ReportStatus.cancelled]

    def result(self):
        status = self.status()
        if status == ReportStatus.cancelled:
            raise MqValueError('This report job in status "cancelled". Cannot retrieve results.')
        if status == ReportStatus.error:
            raise MqValueError('This report job is in status "error". Cannot retrieve results.')
        if status != ReportStatus.done:
            raise MqValueError('This report job is not done. Cannot retrieve results.')
        if self.__report_type in [ReportType.Portfolio_Factor_Risk, ReportType.Asset_Factor_Risk]:
            results = GsReportApi.get_risk_factor_data_results(risk_report_id=self.__report_id,
                                                               start_date=self.__start_date,
                                                               end_date=self.__end_date)
            return pd.DataFrame(results)
        if self.__report_type == ReportType.Portfolio_Performance_Analytics:
            query = DataQuery(where={'reportId': self.__report_id},
                              start_date=self.__start_date,
                              end_date=self.__end_date)
            results = GsDataApi.query_data(query=query, dataset_id=ReportDataset.PPA_DATASET.value)
            return pd.DataFrame(results)
        return None


class Report:
    """"Private variables"""

    def __init__(self,
                 report_id: str = None,
                 name: str = None,
                 position_source_id: str = None,
                 position_source_type: Union[str, PositionSourceType] = None,
                 report_type: Union[str, ReportType] = None,
                 parameters: ReportParameters = None,
                 latest_end_date: dt.date = None,
                 latest_execution_time: dt.datetime = None,
                 status: Union[str, ReportStatus] = ReportStatus.new,
                 percentage_complete: float = None):
        self.__id = report_id
        self.__name = name
        self.__position_source_id = position_source_id
        self.__position_source_type = position_source_type \
            if isinstance(position_source_type, PositionSourceType) or position_source_type is None \
            else PositionSourceType(position_source_type)
        self.__type = report_type if isinstance(report_type, ReportType) or report_type is None \
            else ReportType(report_type)
        self.__parameters = parameters
        self.__latest_end_date = latest_end_date
        self.__latest_execution_time = latest_execution_time
        self.__status = status if isinstance(status, ReportStatus) else ReportStatus(status)
        self.__percentage_complete = percentage_complete

    @property
    def id(self) -> str:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def position_source_id(self) -> str:
        return self.__position_source_id

    @position_source_id.setter
    def position_source_id(self, value: str):
        self.__position_source_id = value

    @property
    def position_source_type(self) -> PositionSourceType:
        return self.__position_source_type

    @position_source_type.setter
    def position_source_type(self, value: Union[str, PositionSourceType]):
        self.__position_source_type = value if isinstance(value, PositionSourceType) else PositionSourceType(value)

    @property
    def type(self) -> ReportType:
        return self.__type

    @type.setter
    def type(self, value: Union[str, ReportType]):
        self.__type = value if isinstance(value, ReportType) else ReportType(value)

    @property
    def parameters(self) -> ReportParameters:
        return self.__parameters

    @parameters.setter
    def parameters(self, value: ReportParameters):
        self.__parameters = value

    @property
    def latest_end_date(self) -> dt.date:
        return self.__latest_end_date

    @property
    def latest_execution_time(self) -> dt.datetime:
        return self.__latest_execution_time

    @property
    def status(self) -> ReportStatus:
        return self.__status

    @property
    def percentage_complete(self) -> float:
        return self.__percentage_complete

    @classmethod
    def get(cls,
            report_id: str,
            acceptable_types: List[ReportType] = None):
        # This map cant be instantiated / stored at the top of this file, bc the Factor/RiskReport classes aren't
        # defined there. Don't know the best place to put this
        report_type_to_class_type = {
            ReportType.Portfolio_Factor_Risk: type(FactorRiskReport()),
            ReportType.Asset_Factor_Risk: type(FactorRiskReport()),
            ReportType.Portfolio_Performance_Analytics: type(PerformanceReport())
        }

        report = GsReportApi.get_report(report_id=report_id)
        if acceptable_types is not None and report.type not in acceptable_types:
            raise MqValueError('Unexpected report type found.')
        if report.type in report_type_to_class_type:
            return report_type_to_class_type[report.type].from_target(report)
        return Report.from_target(report)

    @classmethod
    def from_target(cls,
                    report: TargetReport):
        return Report(report_id=report.id,
                      name=report.name,
                      position_source_id=report.position_source_id,
                      position_source_type=report.position_source_type,
                      report_type=report.type,
                      parameters=report.parameters,
                      latest_end_date=report.latest_end_date,
                      latest_execution_time=report.latest_execution_time,
                      status=report.status,
                      percentage_complete=report.percentage_complete)

    def save(self):
        """ Create a report using GsReportApi if it doesn't exist. Update the report if it does. """
        target_report = TargetReport(name=self.name,
                                     position_source_id=self.position_source_id,
                                     position_source_type=self.position_source_type,
                                     type_=self.type,
                                     parameters=self.parameters if self.parameters else ReportParameters())
        if self.id:
            target_report.id = self.id
            GsReportApi.update_report(target_report)
        else:
            report = GsReportApi.create_report(target_report)
            self.__id = report.id

    def delete(self):
        """ Hits GsReportsApi to delete a report """
        GsReportApi.delete_report(self.id)

    def set_position_source(self, entity_id: str):
        is_portfolio = entity_id.startswith('MP')
        self.position_source_type = 'Portfolio' if is_portfolio else 'Asset'
        self.position_source_id = entity_id
        if isinstance(self, FactorRiskReport):
            self.type = ReportType.Portfolio_Factor_Risk if is_portfolio else ReportType.Asset_Factor_Risk

    def get_most_recent_job(self):
        jobs = GsReportApi.get_report_jobs(self.id)
        most_current_job = sorted(jobs, key=lambda i: i['createdTime'], reverse=True)[0]
        return ReportJobFuture(report_id=self.id,
                               job_id=most_current_job.get('id'),
                               report_type=ReportType(most_current_job.get('reportType')),
                               start_date=dt.datetime.strptime(most_current_job.get('startDate'),
                                                               "%Y-%m-%d").date(),
                               end_date=dt.datetime.strptime(most_current_job.get('endDate'),
                                                             "%Y-%m-%d").date())

    def schedule(self,
                 start_date: dt.date = None,
                 end_date: dt.date = None):
        if None in [self.id, self.__position_source_id]:
            raise MqValueError('Can only schedule reports with valid IDs and Position Source IDs.')
        if self.position_source_type != PositionSourceType.Portfolio and None in [start_date, end_date]:
            raise MqValueError('Must specify schedule start and end dates for report.')
        if None in [start_date, end_date]:
            position_dates = GsPortfolioApi.get_position_dates(self.position_source_id)
            if len(position_dates) == 0:
                raise MqValueError('Cannot schedule reports for a portfolio with no positions.')
            if start_date is None:
                start_date = min(position_dates)
            if end_date is None:
                end_date = max(position_dates)
        GsReportApi.schedule_report(report_id=self.id,
                                    start_date=start_date,
                                    end_date=end_date)

    def run(self,
            start_date: dt.date,
            end_date: dt.date,
            is_async: bool = True):
        self.schedule(start_date, end_date)
        job_future = self.get_most_recent_job()
        if is_async:
            return job_future
        counter = 100
        while counter > 0:
            if job_future.done():
                return job_future.result()
            sleep(6)
        raise MqValueError(f'Your report {self.id} is taking longer than expected to finish. Please contact the '
                           'Marquee Analytics team at gs-marquee-analytics-support@gs.com')


class PerformanceReport(Report):

    def __init__(self,
                 report_id: str = None,
                 name: str = None,
                 position_source_id: str = None,
                 position_source_type: Union[str, PositionSourceType] = None,
                 parameters: ReportParameters = None,
                 latest_end_date: dt.date = None,
                 latest_execution_time: dt.datetime = None,
                 status: Union[str, ReportStatus] = ReportStatus.new,
                 percentage_complete: float = None,
                 **kwargs):
        super().__init__(report_id, name, position_source_id, position_source_type,
                         ReportType.Portfolio_Performance_Analytics, parameters, latest_end_date, latest_execution_time,
                         status, percentage_complete)

    @classmethod
    def get(cls,
            report_id: str,
            **kwargs):
        return super(PerformanceReport, cls).get(report_id=report_id,
                                                 acceptable_types=[ReportType.Portfolio_Performance_Analytics])

    @classmethod
    def from_target(cls,
                    report: TargetReport):
        if report.type != ReportType.Portfolio_Performance_Analytics:
            raise MqValueError('This report is not a performance report.')
        return PerformanceReport(report_id=report.id,
                                 name=report.name,
                                 position_source_id=report.position_source_id,
                                 position_source_type=report.position_source_type,
                                 report_type=report.type,
                                 parameters=report.parameters,
                                 latest_end_date=report.latest_end_date,
                                 latest_execution_time=report.latest_execution_time,
                                 status=report.status,
                                 percentage_complete=report.percentage_complete)

    def get_pnl(self,
                start_date: dt.date = None,
                end_date: dt.date = None) -> pd.DataFrame:
        return self.get_measure("pnl", start_date, end_date)

    def get_long_exposure(self,
                          start_date: dt.date = None,
                          end_date: dt.date = None) -> pd.DataFrame:
        return self.get_measure("longExposure", start_date, end_date)

    def get_short_exposure(self,
                           start_date: dt.date = None,
                           end_date: dt.date = None) -> pd.DataFrame:
        return self.get_measure("shortExposure", start_date, end_date)

    def get_asset_count(self,
                        start_date: dt.date = None,
                        end_date: dt.date = None) -> pd.DataFrame:
        return self.get_measure("assetCount", start_date, end_date)

    def get_turnover(self,
                     start_date: dt.date = None,
                     end_date: dt.date = None) -> pd.DataFrame:
        return self.get_measure("turnover", start_date, end_date)

    def get_asset_count_long(self,
                             start_date: dt.date = None,
                             end_date: dt.date = None) -> pd.DataFrame:
        return self.get_measure("assetCountLong", start_date, end_date)

    def get_asset_count_short(self,
                              start_date: dt.date = None,
                              end_date: dt.date = None) \
            -> Union[MDAPIDataBatchResponse, DataQueryResponse, tuple, list]:
        return self.get_measure("assetCountShort", start_date, end_date)

    def get_net_exposure(self,
                         start_date: dt.date = None,
                         end_date: dt.date = None) -> pd.DataFrame:
        return self.get_measure("netExposure", start_date, end_date)

    def get_gross_exposure(self,
                           start_date: dt.date = None,
                           end_date: dt.date = None) -> pd.DataFrame:
        return self.get_measure("grossExposure", start_date, end_date)

    def get_trading_pnl(self,
                        start_date: dt.date = None,
                        end_date: dt.date = None) -> pd.DataFrame:
        return self.get_measure("tradingPnl", start_date, end_date)

    def get_trading_cost_pnl(self,
                             start_date: dt.date = None,
                             end_date: dt.date = None) -> pd.DataFrame:
        return self.get_measure("tradingCostPnl", start_date, end_date)

    def get_servicing_cost_long_pnl(self,
                                    start_date: dt.date = None,
                                    end_date: dt.date = None) -> pd.DataFrame:
        return self.get_measure("servicingCostLongPnl", start_date, end_date)

    def get_servicing_cost_short_pnl(self,
                                     start_date: dt.date = None,
                                     end_date: dt.date = None) -> pd.DataFrame:
        return self.get_measure("servicingCostShortPnl", start_date, end_date)

    def get_asset_count_priced(self,
                               start_date: dt.date = None,
                               end_date: dt.date = None) -> pd.DataFrame:
        return self.get_measure("assetCountPriced", start_date, end_date)

    def get_measure(self,
                    field: str,
                    start_date: dt.date = None,
                    end_date: dt.date = None,
                    return_format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[Dict, pd.DataFrame]:
        fields = (field,)
        where = {'reportId': self.id}
        query = DataQuery(where=where, fields=fields, start_date=start_date, end_date=end_date)
        results = GsDataApi.query_data(query=query, dataset_id=ReportDataset.PPA_DATASET.value)
        return pd.DataFrame(results) if return_format == ReturnFormat.DATA_FRAME else results

    def get_many_measures(self,
                          measures: Tuple[str, ...],
                          start_date: dt.date = None,
                          end_date: dt.date = None,
                          return_format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[Dict, pd.DataFrame]:
        fields = tuple(measure for measure in measures)
        where = {'reportId': self.id}
        query = DataQuery(where=where, fields=fields, start_date=start_date, end_date=end_date)
        results = GsDataApi.query_data(query=query, dataset_id=ReportDataset.PPA_DATASET.value)
        return pd.DataFrame(results) if return_format == ReturnFormat.DATA_FRAME else results

    def get_portfolio_constituents(self,
                                   fields: List[str] = None,
                                   start_date: dt.date = None,
                                   end_date: dt.date = None,
                                   return_format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[Dict, pd.DataFrame]:
        where = {'reportId': self.id}
        date_batches = _get_ppaa_batches(self.get_asset_count(start_date, end_date), 3000000)
        queries = [DataQuery(where=where, fields=fields, start_date=dates_batch[0], end_date=dates_batch[1]) for
                   dates_batch in date_batches]
        results = [GsDataApi.query_data(query=query, dataset_id=ReportDataset.PORTFOLIO_CONSTITUENTS.value)
                   for query in queries]
        results = sum(results, [])
        return pd.DataFrame(results) if return_format == ReturnFormat.DATA_FRAME else results


class FactorRiskReport(Report):

    def __init__(self,
                 risk_model_id: str = None,
                 fx_hedged: bool = True,
                 report_id: str = None,
                 name: str = None,
                 position_source_id: str = None,
                 position_source_type: Union[str, PositionSourceType] = None,
                 report_type: Union[str, ReportType] = None,
                 latest_end_date: dt.date = None,
                 latest_execution_time: dt.datetime = None,
                 status: Union[str, ReportStatus] = ReportStatus.new,
                 percentage_complete: float = None,
                 **kwargs):
        super().__init__(report_id, name, position_source_id, position_source_type,
                         report_type, ReportParameters(risk_model=risk_model_id,
                                                       fx_hedged=fx_hedged),
                         latest_end_date, latest_execution_time, status, percentage_complete)

    @classmethod
    def get(cls,
            report_id: str,
            **kwargs):
        return super().get(report_id=report_id,
                           acceptable_types=[ReportType.Portfolio_Factor_Risk, ReportType.Asset_Factor_Risk])

    @classmethod
    def from_target(cls,
                    report: TargetReport):
        if report.type not in [ReportType.Portfolio_Factor_Risk, ReportType.Asset_Factor_Risk]:
            raise MqValueError('This report is not a factor risk report.')
        return FactorRiskReport(risk_model_id=report.parameters.risk_model,
                                fx_hedged=report.parameters.fx_hedged,
                                report_id=report.id,
                                position_source_id=report.position_source_id,
                                position_source_type=report.position_source_type,
                                report_type=report.type,
                                latest_end_date=report.latest_end_date,
                                status=report.status,
                                percentage_complete=report.percentage_complete)

    def get_risk_model_id(self) -> str:
        return self.parameters.risk_model

    def get_results(self,
                    factors: List[str] = None,
                    factor_categories: List[str] = None,
                    start_date: dt.date = None,
                    end_date: dt.date = None,
                    currency: Currency = None,
                    return_format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[Dict, pd.DataFrame]:
        results = GsReportApi.get_risk_factor_data_results(risk_report_id=self.id,
                                                           factors=factors,
                                                           factor_categories=factor_categories,
                                                           currency=currency,
                                                           start_date=start_date,
                                                           end_date=end_date)
        return pd.DataFrame(results) if return_format == ReturnFormat.DATA_FRAME else results

    def get_factor_pnl(self,
                       factor_name: str,
                       start_date: dt.date = None,
                       end_date: dt.date = None,
                       currency: Currency = None) -> pd.DataFrame:
        factor_data = self.get_results(factors=[factor_name],
                                       start_date=start_date,
                                       end_date=end_date,
                                       currency=currency)
        return factor_data.filter(items=['date', 'pnl'])

    def get_factor_exposure(self,
                            factor_name: str,
                            start_date: dt.date = None,
                            end_date: dt.date = None,
                            currency: Currency = None) -> pd.DataFrame:
        factor_data = self.get_results(factors=[factor_name],
                                       start_date=start_date,
                                       end_date=end_date,
                                       currency=currency)
        return factor_data.filter(items=['date', 'exposure'])

    def get_factor_proportion_of_risk(self,
                                      factor_name: str,
                                      start_date: dt.date = None,
                                      end_date: dt.date = None,
                                      currency: Currency = None) -> pd.DataFrame:
        factor_data = self.get_results(factors=[factor_name],
                                       start_date=start_date,
                                       end_date=end_date,
                                       currency=currency)
        return factor_data.filter(items=['date', 'proportionOfRisk'])

    def get_annual_risk(self,
                        factor_name: str,
                        start_date: dt.date = None,
                        end_date: dt.date = None,
                        currency: Currency = None) -> pd.DataFrame:
        factor_data = self.get_results(factors=[factor_name],
                                       start_date=start_date,
                                       end_date=end_date,
                                       currency=currency)
        return factor_data.filter(items=['date', 'annualRisk'])

    def get_daily_risk(self,
                       factor_name: str,
                       start_date: dt.date = None,
                       end_date: dt.date = None,
                       currency: Currency = None) -> pd.DataFrame:
        factor_data = self.get_results(factors=[factor_name],
                                       start_date=start_date,
                                       end_date=end_date,
                                       currency=currency)
        return factor_data.filter(items=['date', 'dailyRisk'])
