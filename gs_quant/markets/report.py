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
from dateutil.relativedelta import relativedelta

from gs_quant.api.gs.data import GsDataApi
from gs_quant.api.gs.portfolios import GsPortfolioApi
from gs_quant.api.gs.reports import GsReportApi, OrderType, FactorRiskTableMode
from gs_quant.datetime import business_day_offset
from gs_quant.errors import MqValueError
from gs_quant.markets.report_utils import _get_ppaa_batches
from gs_quant.models.risk_model import ReturnFormat
from gs_quant.target.common import ReportParameters, Currency
from gs_quant.target.coordinates import MDAPIDataBatchResponse
from gs_quant.target.data import DataQuery, DataQueryResponse
from gs_quant.target.reports import Report as TargetReport, ReportType, PositionSourceType, ReportStatus


class ReportDataset(Enum):
    PPA_DATASET = "PPA"
    PFR_DATASET = "PFR"
    AFR_DATASET = "AFR"
    ATA_DATASET = "ATA"
    ATAA_DATASET = "ATAA"
    PTA_DATASET = "PTA"
    PTAA_DATASET = "PTAA"
    PORTFOLIO_CONSTITUENTS = "PORTFOLIO_CONSTITUENTS"


class FactorRiskViewsMode(Enum):
    Risk = 'Risk'
    Attribution = 'Attribution'


class FactorRiskResultsMode(Enum):
    Portfolio = 'Portfolio'
    Positions = 'Positions'


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
        """
        :return: the status of the report job
        """
        job = GsReportApi.get_report_job(self.__job_id)
        return ReportStatus(job.get('status'))

    def done(self) -> bool:
        """
        :return: true if the report job is in the following states: "done", "error", or "cancelled". Returns
        false otherwise
        """
        return self.status() in [ReportStatus.done, ReportStatus.error, ReportStatus.cancelled]

    def result(self):
        """
        :return: a Pandas DataFrame containing the results of the report job
        """
        status = self.status()
        if status == ReportStatus.cancelled:
            raise MqValueError('This report job in status "cancelled". Cannot retrieve results.')
        if status == ReportStatus.error:
            raise MqValueError('This report job is in status "error". Cannot retrieve results.')
        if status != ReportStatus.done:
            raise MqValueError('This report job is not done. Cannot retrieve results.')
        if self.__report_type in [ReportType.Portfolio_Factor_Risk, ReportType.Asset_Factor_Risk]:
            results = GsReportApi.get_factor_risk_report_results(risk_report_id=self.__report_id,
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
                 earliest_start_date: dt.date = None,
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
        self.__earliest_start_date = earliest_start_date
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
    def earliest_start_date(self) -> dt.date:
        return self.__earliest_start_date

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
        return cls.from_target(GsReportApi.get_report(report_id))

    @classmethod
    def from_target(cls,
                    report: TargetReport):
        return Report(report_id=report.id,
                      name=report.name,
                      position_source_id=report.position_source_id,
                      position_source_type=report.position_source_type,
                      report_type=report.type,
                      parameters=report.parameters,
                      earliest_start_date=report.earliest_start_date,
                      latest_end_date=report.latest_end_date,
                      latest_execution_time=report.latest_execution_time,
                      status=report.status,
                      percentage_complete=report.percentage_complete)

    def save(self):
        """ Create a report in Marquee if it doesn't exist. Update the report if it does. """
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
        """ Delete a report from Marquee"""
        GsReportApi.delete_report(self.id)

    def set_position_source(self, entity_id: str):
        is_portfolio = entity_id.startswith('MP')
        self.position_source_type = 'Portfolio' if is_portfolio else 'Asset'
        self.position_source_id = entity_id
        if isinstance(self, FactorRiskReport):
            self.type = ReportType.Portfolio_Factor_Risk if is_portfolio else ReportType.Asset_Factor_Risk
        if isinstance(self, ThematicReport):
            self.type = ReportType.Portfolio_Thematic_Analytics if is_portfolio else ReportType.Asset_Thematic_Analytics

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
                 end_date: dt.date = None,
                 backcast: bool = None):
        if None in [self.id, self.__position_source_id]:
            raise MqValueError('Can only schedule reports with valid IDs and Position Source IDs.')
        if self.position_source_type != PositionSourceType.Portfolio and None in [start_date, end_date]:
            raise MqValueError('Must specify schedule start and end dates for report.')
        if None in [start_date, end_date]:
            position_dates = GsPortfolioApi.get_position_dates(self.position_source_id)
            if len(position_dates) == 0:
                raise MqValueError('Cannot schedule reports for a portfolio with no positions.')
            if start_date is None:
                start_date = business_day_offset(min(position_dates) - relativedelta(years=1), -1, roll='forward') \
                    if backcast else min(position_dates)
            if end_date is None:
                end_date = min(position_dates) if backcast else max(position_dates)
        GsReportApi.schedule_report(report_id=self.id,
                                    start_date=start_date,
                                    end_date=end_date,
                                    backcast=backcast)

    def run(self,
            start_date: dt.date = None,
            end_date: dt.date = None,
            backcast: bool = None,
            is_async: bool = True):
        self.schedule(start_date, end_date, backcast)
        counter = 5
        while counter > 0:
            try:
                job_future = self.get_most_recent_job()
                if is_async:
                    return job_future
                counter = 100
                while counter > 0:
                    if job_future.done():
                        return job_future.result()
                    sleep(6)
                raise MqValueError(
                    f'Your report {self.id} is taking longer than expected to finish. Please contact the '
                    'Marquee Analytics team at gs-marquee-analytics-support@gs.com')
            except IndexError:
                counter -= 1
        status = Report.get(self.id).status
        if status == ReportStatus.waiting:
            raise MqValueError(f'Your report {self.id} is stuck in "waiting" status and therefore cannot be run at '
                               'this time.')
        raise MqValueError(f'Your report {self.id} is taking longer to run than expected. '
                           'Please reach out to the Marquee Analytics team at gs-marquee-analytics-support@gs.com '
                           'for assistance.')


class PerformanceReport(Report):

    def __init__(self,
                 report_id: str = None,
                 name: str = None,
                 position_source_id: str = None,
                 position_source_type: Union[str, PositionSourceType] = None,
                 parameters: ReportParameters = None,
                 earliest_start_date: dt.date = None,
                 latest_end_date: dt.date = None,
                 latest_execution_time: dt.datetime = None,
                 status: Union[str, ReportStatus] = ReportStatus.new,
                 percentage_complete: float = None,
                 **kwargs):
        super().__init__(report_id, name, position_source_id, position_source_type,
                         ReportType.Portfolio_Performance_Analytics, parameters, earliest_start_date, latest_end_date,
                         latest_execution_time, status, percentage_complete)

    @classmethod
    def get(cls,
            report_id: str,
            **kwargs):
        """
        Get a performance report from the unique report identifier
        :param report_id: Marquee report ID
        :return: returns a PerfomanceReport object that correlates to the Marquee report
        """
        return cls.from_target(GsReportApi.get_report(report_id))

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
                                 earliest_start_date=report.earliest_start_date,
                                 latest_end_date=report.latest_end_date,
                                 latest_execution_time=report.latest_execution_time,
                                 status=report.status,
                                 percentage_complete=report.percentage_complete)

    def get_pnl(self,
                start_date: dt.date = None,
                end_date: dt.date = None) -> pd.DataFrame:
        """
        Get historical portfolio PnL
        :param start_date: start date
        :param end_date: end date
        :return: returns a Pandas DataFrame with the results
        """
        return self.get_measure("pnl", start_date, end_date)

    def get_long_exposure(self,
                          start_date: dt.date = None,
                          end_date: dt.date = None) -> pd.DataFrame:
        """
        Get historical portfolio long exposure
        :param start_date: start date
        :param end_date: end date
        :return: returns a Pandas DataFrame with the results
        """
        return self.get_measure("longExposure", start_date, end_date)

    def get_short_exposure(self,
                           start_date: dt.date = None,
                           end_date: dt.date = None) -> pd.DataFrame:
        """
        Get historical portfolio short exposure
        :param start_date: start date
        :param end_date: end date
        :return: returns a Pandas DataFrame with the results
        """
        return self.get_measure("shortExposure", start_date, end_date)

    def get_asset_count(self,
                        start_date: dt.date = None,
                        end_date: dt.date = None) -> pd.DataFrame:
        """
        Get historical portfolio asset count
        :param start_date: start date
        :param end_date: end date
        :return: returns a Pandas DataFrame with the results
        """
        return self.get_measure("assetCount", start_date, end_date)

    def get_turnover(self,
                     start_date: dt.date = None,
                     end_date: dt.date = None) -> pd.DataFrame:
        """
        Get historical portfolio turnover
        :param start_date: start date
        :param end_date: end date
        :return: returns a Pandas DataFrame with the results
        """
        return self.get_measure("turnover", start_date, end_date)

    def get_asset_count_long(self,
                             start_date: dt.date = None,
                             end_date: dt.date = None) -> pd.DataFrame:
        """
        Get historical portfolio long asset count
        :param start_date: start date
        :param end_date: end date
        :return: returns a Pandas DataFrame with the results
        """
        return self.get_measure("assetCountLong", start_date, end_date)

    def get_asset_count_short(self,
                              start_date: dt.date = None,
                              end_date: dt.date = None) \
            -> Union[MDAPIDataBatchResponse, DataQueryResponse, tuple, list]:
        """
        Get historical portfolio short asset count
        :param start_date: start date
        :param end_date: end date
        :return: returns a Pandas DataFrame with the results
        """
        return self.get_measure("assetCountShort", start_date, end_date)

    def get_net_exposure(self,
                         start_date: dt.date = None,
                         end_date: dt.date = None) -> pd.DataFrame:
        """
        Get historical portfolio net exposure
        :param start_date: start date
        :param end_date: end date
        :return: returns a Pandas DataFrame with the results
        """
        return self.get_measure("netExposure", start_date, end_date)

    def get_gross_exposure(self,
                           start_date: dt.date = None,
                           end_date: dt.date = None) -> pd.DataFrame:
        """
        Get historical portfolio gross exposure
        :param start_date: start date
        :param end_date: end date
        :return: returns a Pandas DataFrame with the results
        """
        return self.get_measure("grossExposure", start_date, end_date)

    def get_trading_pnl(self,
                        start_date: dt.date = None,
                        end_date: dt.date = None) -> pd.DataFrame:
        """
        Get historical portfolio trading PnL
        :param start_date: start date
        :param end_date: end date
        :return: returns a Pandas DataFrame with the results
        """
        return self.get_measure("tradingPnl", start_date, end_date)

    def get_trading_cost_pnl(self,
                             start_date: dt.date = None,
                             end_date: dt.date = None) -> pd.DataFrame:
        """
        Get historical portfolio trading cost PnL
        :param start_date: start date
        :param end_date: end date
        :return: returns a Pandas DataFrame with the results
        """
        return self.get_measure("tradingCostPnl", start_date, end_date)

    def get_servicing_cost_long_pnl(self,
                                    start_date: dt.date = None,
                                    end_date: dt.date = None) -> pd.DataFrame:
        """
        Get historical portfolio servicing cost long PnL
        :param start_date: start date
        :param end_date: end date
        :return: returns a Pandas DataFrame with the results
        """
        return self.get_measure("servicingCostLongPnl", start_date, end_date)

    def get_servicing_cost_short_pnl(self,
                                     start_date: dt.date = None,
                                     end_date: dt.date = None) -> pd.DataFrame:
        """
        Get historical portfolio servicing cost short PnL
        :param start_date: start date
        :param end_date: end date
        :return: returns a Pandas DataFrame with the results
        """
        return self.get_measure("servicingCostShortPnl", start_date, end_date)

    def get_asset_count_priced(self,
                               start_date: dt.date = None,
                               end_date: dt.date = None) -> pd.DataFrame:
        """
        Get historical portfolio asset count priced
        :param start_date: start date
        :param end_date: end date
        :return: returns a Pandas DataFrame with the results
        """
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
                          measures: Tuple[str, ...] = None,
                          start_date: dt.date = None,
                          end_date: dt.date = None,
                          return_format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[Dict, pd.DataFrame]:
        """
        Get many historical portfolio metrics
        :param measures: a list of metrics
        :param start_date: start date
        :param end_date: end date
        :return: returns a Pandas DataFrame with the results
        """
        if measures is None:
            measures = []
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
        """
        Get historical portfolio constituents
        :param fields: list of fields to include in the results
        :param start_date: start date
        :param end_date: end date
        :param return_format: return format; defaults to a Pandas DataFrame, but can be manually
        set to ReturnFormat.JSON
        :return: Portfolio constituent data for each day in the requested date range
        """
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
                 earliest_start_date: dt.date = None,
                 latest_end_date: dt.date = None,
                 latest_execution_time: dt.datetime = None,
                 status: Union[str, ReportStatus] = ReportStatus.new,
                 percentage_complete: float = None,
                 **kwargs):
        super().__init__(report_id, name, position_source_id, position_source_type,
                         report_type, ReportParameters(risk_model=risk_model_id,
                                                       fx_hedged=fx_hedged), earliest_start_date,
                         latest_end_date, latest_execution_time, status, percentage_complete)

    @classmethod
    def get(cls,
            report_id: str,
            **kwargs):
        """
        Get a performance report from the unique report identifier
        :param report_id: Marquee report ID
        :return: returns a PerfomanceReport object that correlates to the Marquee report
        """
        return cls.from_target(GsReportApi.get_report(report_id))

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
                                earliest_start_date=report.earliest_start_date,
                                latest_end_date=report.latest_end_date,
                                status=report.status,
                                percentage_complete=report.percentage_complete)

    def get_risk_model_id(self) -> str:
        """
        :return: the ID of the risk model associated with the factor risk report
        """
        return self.parameters.risk_model

    def get_results(self,
                    mode: FactorRiskResultsMode = FactorRiskResultsMode.Portfolio,
                    factors: List[str] = None,
                    factor_categories: List[str] = None,
                    start_date: dt.date = None,
                    end_date: dt.date = None,
                    currency: Currency = None,
                    return_format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[Dict, pd.DataFrame]:
        """
        Get the raw results associated with the factor risk report
        :param mode: results mode; defaults to the portfolio level
        :param factors: optional list of factors; defaults to all of them
        :param factor_categories: optional list of factor categories; defaults to all of them
        :param start_date: start date
        :param end_date: end date
        :param currency: currency
        :param return_format: return format; defaults to a Pandas DataFrame, but can be manually
        set to ReturnFormat.JSON
        :return: risk report results
        """
        results = GsReportApi.get_factor_risk_report_results(risk_report_id=self.id,
                                                             view=mode.value,
                                                             factors=factors,
                                                             factor_categories=factor_categories,
                                                             currency=currency,
                                                             start_date=start_date,
                                                             end_date=end_date)
        return pd.DataFrame(results) if return_format == ReturnFormat.DATA_FRAME else results

    def get_view(self,
                 mode: FactorRiskViewsMode,
                 factor: str = None,
                 factor_category: str = None,
                 start_date: dt.date = None,
                 end_date: dt.date = None,
                 currency: Currency = None) -> Dict:
        """
        Get the results associated with the factor risk report as seen on the Marquee user interface
        :param mode: views mode
        :param factor: optional factor name
        :param factor_category: optional factor category
        :param start_date: start date
        :param end_date: end date
        :param currency: currency
        :return: risk report results
        """
        return GsReportApi.get_factor_risk_report_view(
            risk_report_id=self.id,
            view=mode.value,
            factor=factor,
            factor_category=factor_category,
            currency=currency,
            start_date=start_date,
            end_date=end_date
        )

    def get_table(self,
                  mode: FactorRiskTableMode = None,
                  factors: List[str] = None,
                  factor_categories: List[str] = None,
                  date: dt.date = None,
                  currency: Currency = None,
                  order_by_column: str = None,
                  order_type: OrderType = None,
                  return_format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[Dict, pd.DataFrame]:
        table = GsReportApi.get_factor_risk_report_table(risk_report_id=self.id,
                                                         mode=mode,
                                                         factors=factors,
                                                         factor_categories=factor_categories,
                                                         currency=currency,
                                                         date=date,
                                                         order_by_column=order_by_column,
                                                         order_type=order_type)
        if return_format == ReturnFormat.DATA_FRAME:
            column_info = table.get('table').get('metadata').get('columnInfo')
            column_info[0].update({'columns': ['name', 'symbol', 'sector']})
            rows = table.get('table').get('rows')
            sorted_columns = []
            for column_group in column_info:
                sorted_columns = sorted_columns + column_group.get('columns')
            rows_data_frame = pd.DataFrame(rows)
            rows_data_frame = rows_data_frame[sorted_columns]
            rows_data_frame = rows_data_frame.set_index('name')
            return rows_data_frame
        return table

    def get_factor_pnl(self,
                       factor_names: List[str] = None,
                       factor_categories: List[str] = None,
                       start_date: dt.date = None,
                       end_date: dt.date = None,
                       currency: Currency = None) -> pd.DataFrame:
        """
        Get historical factor PnL
        :param factor_names: optional list of factor names; defaults to all of them
        :param factor_categories: optional list of factor categories; defaults to all of them
        :param start_date: start date
        :param end_date: end date
        :param currency: currency
        :return: a Pandas DataFrame with the results
        """
        factor_data = self.get_results(factors=factor_names,
                                       factor_categories=factor_categories,
                                       start_date=start_date,
                                       end_date=end_date,
                                       currency=currency,
                                       return_format=ReturnFormat.JSON)

        return _format_multiple_factor_table(factor_data, 'pnl')

    def get_factor_exposure(self,
                            factor_names: List[str] = None,
                            factor_categories: List[str] = None,
                            start_date: dt.date = None,
                            end_date: dt.date = None,
                            currency: Currency = None) -> pd.DataFrame:
        """
        Get historical factor exposure
        :param factor_names: optional list of factor names; defaults to all of them
        :param factor_categories: optional list of factor categories; defaults to all of them
        :param start_date: start date
        :param end_date: end date
        :param currency: currency
        :return: a Pandas DataFrame with the results
        """
        factor_data = self.get_results(factors=factor_names,
                                       factor_categories=factor_categories,
                                       start_date=start_date,
                                       end_date=end_date,
                                       currency=currency,
                                       return_format=ReturnFormat.JSON)
        return _format_multiple_factor_table(factor_data, 'exposure')

    def get_factor_proportion_of_risk(self,
                                      factor_names: List[str] = None,
                                      factor_categories: List[str] = None,
                                      start_date: dt.date = None,
                                      end_date: dt.date = None,
                                      currency: Currency = None) -> pd.DataFrame:
        """
        Get historical factor proportion of risk
        :param factor_names: optional list of factor names; defaults to all of them
        :param factor_categories: optional list of factor categories; defaults to all of them
        :param start_date: start date
        :param end_date: end date
        :param currency: currency
        :return: a Pandas DataFrame with the results
        """
        factor_data = self.get_results(factors=factor_names,
                                       factor_categories=factor_categories,
                                       start_date=start_date,
                                       end_date=end_date,
                                       currency=currency,
                                       return_format=ReturnFormat.JSON)
        return _format_multiple_factor_table(factor_data, 'proportionOfRisk')

    def get_annual_risk(self,
                        factor_names: List[str] = None,
                        start_date: dt.date = None,
                        end_date: dt.date = None,
                        currency: Currency = None) -> pd.DataFrame:
        """
        Get historical annual risk
        :param factor_names: optional list of factor names; must be from the following: "Factor", "Specific", "Total
        :param start_date: start date
        :param end_date: end date
        :param currency: currency
        :return: a Pandas DataFrame with the results
        """
        factor_data = self.get_results(factors=factor_names,
                                       start_date=start_date,
                                       end_date=end_date,
                                       currency=currency,
                                       return_format=ReturnFormat.JSON)
        return _format_multiple_factor_table(factor_data, 'annualRisk')

    def get_daily_risk(self,
                       factor_names: List[str] = None,
                       start_date: dt.date = None,
                       end_date: dt.date = None,
                       currency: Currency = None) -> pd.DataFrame:
        """
        Get historical daily risk
        :param factor_names: optional list of factor names; must be from the following: "Factor", "Specific", "Total
        :param start_date: start date
        :param end_date: end date
        :param currency: currency
        :return: a Pandas DataFrame with the results
        """
        factor_data = self.get_results(factors=factor_names,
                                       start_date=start_date,
                                       end_date=end_date,
                                       currency=currency,
                                       return_format=ReturnFormat.JSON)
        return _format_multiple_factor_table(factor_data, 'dailyRisk')


def _format_multiple_factor_table(factor_data: List[Dict],
                                  key: str) -> pd.DataFrame:
    formatted_data = {}
    for data in factor_data:
        date = data['date']
        if date in formatted_data:
            formatted_data[date][data['factor']] = data[key]
        else:
            formatted_data[date] = {
                'date': date,
                data['factor']: data[key]
            }

    return pd.DataFrame(formatted_data.values())


class ThematicReport(Report):

    def __init__(self,
                 report_id: str = None,
                 name: str = None,
                 position_source_id: str = None,
                 parameters: ReportParameters = None,
                 position_source_type: Union[str, PositionSourceType] = None,
                 report_type: Union[str, ReportType] = None,
                 earliest_start_date: dt.date = None,
                 latest_end_date: dt.date = None,
                 latest_execution_time: dt.datetime = None,
                 status: Union[str, ReportStatus] = ReportStatus.new,
                 percentage_complete: float = None,
                 **kwargs):
        super().__init__(report_id, name, position_source_id, position_source_type,
                         report_type, parameters, earliest_start_date, latest_end_date,
                         latest_execution_time, status, percentage_complete)

    @classmethod
    def get(cls,
            report_id: str,
            **kwargs):
        """
        Get a thematic report from the unique report identifier
        :param report_id: Marquee report ID
        :return: returns a ThematicReport object that correlates to the Marquee report
        """
        return cls.from_target(GsReportApi.get_report(report_id))

    @classmethod
    def from_target(cls,
                    report: TargetReport):
        if report.type not in [ReportType.Portfolio_Thematic_Analytics, ReportType.Asset_Thematic_Analytics]:
            raise MqValueError('This report is not a thematic report.')
        return ThematicReport(report_id=report.id,
                              name=report.name,
                              position_source_id=report.position_source_id,
                              parameters=report.parameters,
                              position_source_type=report.position_source_type,
                              report_type=report.type,
                              earliest_start_date=report.earliest_start_date,
                              latest_end_date=report.latest_end_date,
                              latest_execution_time=report.latest_execution_time,
                              status=report.status,
                              percentage_complete=report.percentage_complete)

    def get_thematic_data(self,
                          start_date: dt.date = None,
                          end_date: dt.date = None,
                          basket_ids: List[str] = None) -> pd.DataFrame:
        """
        Get all results from the thematic report for a date range
        :param start_date: start date
        :param end_date: end date
        :param basket_ids: optional list of thematic basket IDs to include; defaults to all of them
        :return: a Pandas DataFrame with results
        """

        results = self._get_measures(["thematicExposure", "grossExposure"], start_date, end_date, basket_ids,
                                     ReturnFormat.JSON)
        for result in results:
            result['thematicBeta'] = result['thematicExposure'] / result['grossExposure']
        return pd.DataFrame(results).filter(items=['date', 'thematicExposure', 'thematicBeta'])

    def get_thematic_exposure(self,
                              start_date: dt.date = None,
                              end_date: dt.date = None,
                              basket_ids: List[str] = None) -> pd.DataFrame:
        """
        Get portfolio historical exposure to GS Flagship Thematic baskets
        :param start_date: start date
        :param end_date: end date
        :param basket_ids: optional list of thematic basket IDs to include; defaults to all of them
        :return: a Pandas DataFrame with results
        """
        return self._get_measures(["thematicExposure"], start_date, end_date, basket_ids)

    def get_thematic_betas(self,
                           start_date: dt.date = None,
                           end_date: dt.date = None,
                           basket_ids: List[str] = None) -> pd.DataFrame:
        """
        Get portfolio historical beta to GS Flagship Thematic baskets
        :param start_date: start date
        :param end_date: end date
        :param basket_ids: optional list of thematic basket IDs to include; defaults to all of them
        :return: a Pandas DataFrame with results
        """
        results = self._get_measures(["thematicExposure", "grossExposure"], start_date, end_date, basket_ids,
                                     ReturnFormat.JSON)
        for result in results:
            result['thematicBeta'] = result['thematicExposure'] / result['grossExposure']
            result.pop('thematicExposure')
            result.pop('grossExposure')
        return pd.DataFrame(results)

    def _get_measures(self,
                      fields: List,
                      start_date: dt.date = None,
                      end_date: dt.date = None,
                      basket_ids: List[str] = None,
                      return_format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[Dict, pd.DataFrame]:
        where = {'reportId': self.id}
        if basket_ids:
            where['basketId'] = basket_ids
        dataset = ReportDataset.PTA_DATASET.value if self.position_source_type == PositionSourceType.Portfolio \
            else ReportDataset.ATA_DATASET.value
        query = DataQuery(where=where, fields=fields, start_date=start_date, end_date=end_date)
        results = GsDataApi.query_data(query=query, dataset_id=dataset)
        return pd.DataFrame(results) if return_format == ReturnFormat.DATA_FRAME else results
