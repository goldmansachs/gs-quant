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
from typing import Tuple, Union, List, Dict

import pandas as pd

from gs_quant.api.gs.data import GsDataApi
from gs_quant.api.gs.reports import GsReportApi
from gs_quant.errors import MqValueError
from gs_quant.models.risk_model import ReturnFormat
from gs_quant.target.common import ReportParameters, Currency
from gs_quant.target.coordinates import MDAPIDataBatchResponse
from gs_quant.target.data import DataQuery, DataQueryResponse
from gs_quant.target.reports import Report as TargetReport
from gs_quant.target.reports import ReportType, PositionSourceType, ReportStatus


class ReportDataset(Enum):
    PPA_DATASET = "PPA"
    PFR_DATASET = "PFR"
    AFR_DATASET = "AFR"


class Report:
    """"Private variables"""

    def __init__(self,
                 report_id: str = None,
                 position_source_id: str = None,
                 position_source_type: Union[str, PositionSourceType] = None,
                 report_type: Union[str, ReportType] = None,
                 parameters: ReportParameters = None,
                 status: Union[str, ReportStatus] = ReportStatus.new):
        self.__id = report_id
        self.__position_source_id = position_source_id
        self.__position_source_type = position_source_type \
            if isinstance(position_source_type, PositionSourceType) or position_source_type is None \
            else PositionSourceType(position_source_type)
        self.__type = report_type if isinstance(report_type, ReportType) or report_type is None \
            else ReportType(report_type)
        self.__parameters = parameters
        self.__status = status if isinstance(status, ReportStatus) else ReportStatus(status)

    @property
    def id(self) -> str:
        return self.__id

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
    def status(self) -> ReportStatus:
        return self.__status

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
            return report_type_to_class_type[report.type](report_id=report.id,
                                                          position_source_id=report.position_source_id,
                                                          position_source_type=report.position_source_type,
                                                          report_type=report.type,
                                                          parameters=report.parameters,
                                                          status=report.status)
        return Report(report_id=report.id,
                      position_source_id=report.position_source_id,
                      position_source_type=report.position_source_type,
                      report_type=report.type,
                      parameters=report.parameters,
                      status=report.status)

    def save(self):
        """ Create a report using GsReportApi if it doesn't exist. Update the report if it does. """
        target_report = TargetReport(position_source_id=self.position_source_id,
                                     position_source_type=self.position_source_type,
                                     type_=self.type,
                                     parameters=self.parameters)
        if self.id:
            target_report.id = self.id
            GsReportApi.update_report(target_report)
        else:
            GsReportApi.create_report(target_report)

    def delete(self):
        """ Hits GsReportsApi to delete a report """
        GsReportApi.delete_report(self.id)


class PerformanceReport(Report):

    def __init__(self,
                 report_id: str = None,
                 position_source_id: str = None,
                 position_source_type: Union[str, PositionSourceType] = None,
                 report_type: Union[str, ReportType] = None,
                 parameters: ReportParameters = None,
                 status: Union[str, ReportStatus] = ReportStatus.new,
                 **kwargs):
        super().__init__(report_id, position_source_id, position_source_type, report_type, parameters, status)

    @classmethod
    def get(cls,
            report_id: str,
            **kwargs):
        return super(PerformanceReport, cls).get(report_id=report_id,
                                                 acceptable_types=[ReportType.Portfolio_Performance_Analytics])

    def get_pnl(self,
                start_date: dt.date = None,
                end_date: dt.date = None) -> Union[MDAPIDataBatchResponse, DataQueryResponse, tuple, list]:
        return self.get_measure("pnl", start_date, end_date)

    def get_long_exposure(self,
                          start_date: dt.date = None,
                          end_date: dt.date = None) -> Union[MDAPIDataBatchResponse, DataQueryResponse, tuple, list]:
        return self.get_measure("longExposure", start_date, end_date)

    def get_short_exposure(self,
                           start_date: dt.date = None,
                           end_date: dt.date = None) -> Union[MDAPIDataBatchResponse, DataQueryResponse, tuple, list]:
        return self.get_measure("shortExposure", start_date, end_date)

    def get_asset_count(self,
                        start_date: dt.date = None,
                        end_date: dt.date = None) -> Union[MDAPIDataBatchResponse, DataQueryResponse, tuple, list]:
        return self.get_measure("assetCount", start_date, end_date)

    def get_turnover(self,
                     start_date: dt.date = None,
                     end_date: dt.date = None) -> Union[MDAPIDataBatchResponse, DataQueryResponse, tuple, list]:
        return self.get_measure("turnover", start_date, end_date)

    def get_asset_count_long(self,
                             start_date: dt.date = None,
                             end_date: dt.date = None) -> Union[MDAPIDataBatchResponse, DataQueryResponse, tuple, list]:
        return self.get_measure("assetCountLong", start_date, end_date)

    def get_asset_count_short(self,
                              start_date: dt.date = None,
                              end_date: dt.date = None) \
            -> Union[MDAPIDataBatchResponse, DataQueryResponse, tuple, list]:
        return self.get_measure("assetCountShort", start_date, end_date)

    def get_net_exposure(self,
                         start_date: dt.date = None,
                         end_date: dt.date = None) -> Union[MDAPIDataBatchResponse, DataQueryResponse, tuple, list]:
        return self.get_measure("netExposure", start_date, end_date)

    def get_gross_exposure(self,
                           start_date: dt.date = None,
                           end_date: dt.date = None) -> Union[MDAPIDataBatchResponse, DataQueryResponse, tuple, list]:
        return self.get_measure("grossExposure", start_date, end_date)

    def get_trading_pnl(self,
                        start_date: dt.date = None,
                        end_date: dt.date = None) -> Union[MDAPIDataBatchResponse, DataQueryResponse, tuple, list]:
        return self.get_measure("tradingPnl", start_date, end_date)

    def get_trading_cost_pnl(self,
                             start_date: dt.date = None,
                             end_date: dt.date = None) -> Union[MDAPIDataBatchResponse, DataQueryResponse, tuple, list]:
        return self.get_measure("tradingCostPnl", start_date, end_date)

    def get_servicing_cost_long_pnl(self,
                                    start_date: dt.date = None,
                                    end_date: dt.date = None) \
            -> Union[MDAPIDataBatchResponse, DataQueryResponse, tuple, list]:
        return self.get_measure("servicingCostLongPnl", start_date, end_date)

    def get_servicing_cost_short_pnl(self,
                                     start_date: dt.date = None,
                                     end_date: dt.date = None) \
            -> Union[MDAPIDataBatchResponse, DataQueryResponse, tuple, list]:
        return self.get_measure("servicingCostShortPnl", start_date, end_date)

    def get_asset_count_priced(self,
                               start_date: dt.date = None,
                               end_date: dt.date = None) \
            -> Union[MDAPIDataBatchResponse, DataQueryResponse, tuple, list]:
        return self.get_measure("assetCountPriced", start_date, end_date)

    def get_measure(self,
                    field: str,
                    start_date: dt.date = None,
                    end_date: dt.date = None) -> Union[MDAPIDataBatchResponse, DataQueryResponse, tuple, list]:
        fields = (field,)
        where = {'reportId': self.id}
        query = DataQuery(where=where, fields=fields, start_date=start_date, end_date=end_date)
        return GsDataApi.query_data(query=query, dataset_id=ReportDataset.PPA_DATASET.value)

    def get_many_measures(self,
                          measures: Tuple[str, ...],
                          start_date: dt.date = None,
                          end_date: dt.date = None) -> Union[MDAPIDataBatchResponse, DataQueryResponse, tuple, list]:
        fields = tuple(measure for measure in measures)
        where = {'reportId': self.id}
        query = DataQuery(where=where, fields=fields, start_date=start_date, end_date=end_date)
        return GsDataApi.query_data(query=query, dataset_id=ReportDataset.PPA_DATASET.value)


class FactorRiskReport(Report):

    def __init__(self,
                 report_id: str = None,
                 position_source_id: str = None,
                 position_source_type: Union[str, PositionSourceType] = None,
                 report_type: Union[str, ReportType] = None,
                 parameters: ReportParameters = None,
                 status: Union[str, ReportStatus] = ReportStatus.new,
                 **kwargs):
        super().__init__(report_id, position_source_id, position_source_type, report_type, parameters, status)

    @classmethod
    def get(cls,
            report_id: str,
            **kwargs):
        return super().get(report_id=report_id,
                           acceptable_types=[ReportType.Portfolio_Factor_Risk, ReportType.Asset_Factor_Risk])

    def get_risk_model_id(self) -> str:
        return self.parameters.risk_model

    def set_position_target(self, entity_id: str):
        is_portfolio = entity_id.startswith('MP')
        self.position_source_type = 'Portfolio' if is_portfolio else 'Asset'
        self.position_source_id = entity_id
        self.type = ReportType.Portfolio_Factor_Risk if is_portfolio else ReportType.Asset_Factor_Risk

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
