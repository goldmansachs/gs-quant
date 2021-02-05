"""
Copyright 2019 Goldman Sachs.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicablNe law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""
import datetime as dt
from typing import Tuple

from gs_quant.api.gs.data import GsDataApi
from gs_quant.api.gs.reports import GsReportApi
from gs_quant.target.common import FieldValueMap
from gs_quant.target.data import DataQuery
from gs_quant.target.reports import Report

PPA_DATASET = "PPA"
PFR_DATASET = "PFR"
AFR_DATASET = "AFR"


class BaseReport:
    """"Private variables"""
    def __init__(self, report_id: str):
        self.report = GsReportApi.get_report(report_id=report_id)

    def get_id(self):
        return self.report.id

    def get_position_source_type(self):
        return self.report.position_source_type

    def get_parameters(self):
        return self.report.parameters

    def get_type(self):
        return self.report.type

    @staticmethod
    def get_report_by_id(report_id: str) -> Report:
        """ Hits GsReportsApi to retrieve a report from id """
        return GsReportApi.get_report(report_id)

    @staticmethod
    def create_report(report: Report):
        """ Creates a report using GsReportApi """
        GsReportApi.create_report(report)

    @staticmethod
    def update_report(report: Report):
        """ Update report using GsReportApi """
        GsReportApi.update_report(report)

    @staticmethod
    def delete_report_by_id(report_id: str):
        """ Hits GsReportsApi to delete a report """
        GsReportApi.delete_report(report_id)


class PerformanceReport(BaseReport):
    @classmethod
    def get_pnl(cls, report_id: str, start_date: dt.date = None, end_date: dt.date = None):
        return cls.get_measure(report_id, "pnl", start_date, end_date)

    @classmethod
    def get_long_exposure(cls, report_id: str, start_date: dt.date = None, end_date: dt.date = None):
        return cls.get_measure(report_id, "longExposure", start_date, end_date)

    @classmethod
    def get_short_exposure(cls, report_id: str, start_date: dt.date = None, end_date: dt.date = None):
        return cls.get_measure(report_id, "shortExposure", start_date, end_date)

    @classmethod
    def get_asset_count(cls, report_id: str, start_date: dt.date = None, end_date: dt.date = None):
        return cls.get_measure(report_id, "assetCount", start_date, end_date)

    @classmethod
    def get_turnover(cls, report_id: str, start_date: dt.date = None, end_date: dt.date = None):
        return cls.get_measure(report_id, "turnover", start_date, end_date)

    @classmethod
    def get_asset_count_long(cls, report_id: str, start_date: dt.date = None, end_date: dt.date = None):
        return cls.get_measure(report_id, "assetCountLong", start_date, end_date)

    @classmethod
    def get_asset_count_short(cls, report_id: str, start_date: dt.date = None, end_date: dt.date = None):
        return cls.get_measure(report_id, "assetCountShort", start_date, end_date)

    @classmethod
    def get_net_exposure(cls, report_id: str, start_date: dt.date = None, end_date: dt.date = None):
        return cls.get_measure(report_id, "netExposure", start_date, end_date)

    @classmethod
    def get_gross_exposure(cls, report_id: str, start_date: dt.date = None, end_date: dt.date = None):
        return cls.get_measure(report_id, "grossExposure", start_date, end_date)

    @classmethod
    def get_trading_pnl(cls, report_id: str, start_date: dt.date = None, end_date: dt.date = None):
        return cls.get_measure(report_id, "tradingPnl", start_date, end_date)

    @classmethod
    def get_trading_cost_pnl(cls, report_id: str, start_date: dt.date = None, end_date: dt.date = None):
        return cls.get_measure(report_id, "tradingCostPnl", start_date, end_date)

    @classmethod
    def get_servicing_cost_long_pnl(cls, report_id: str, start_date: dt.date = None, end_date: dt.date = None):
        return cls.get_measure(report_id, "servicingCostLongPnl", start_date, end_date)

    @classmethod
    def get_servicing_cost_short_pnl(cls, report_id: str, start_date: dt.date = None, end_date: dt.date = None):
        return cls.get_measure(report_id, "servicingCostShortPnl", start_date, end_date)

    @classmethod
    def get_asset_count_priced(cls, report_id: str, start_date: dt.date = None, end_date: dt.date = None):
        return cls.get_measure(report_id, "assetCountPriced", start_date, end_date)

    @classmethod
    def get_measure(cls, report_id: str, field: str, start_date: dt.date = None, end_date: dt.date = None):
        fields = [field]
        where = FieldValueMap(report_id=report_id)
        query = DataQuery(where=where, fields=fields, start_date=start_date, end_date=end_date)
        return GsDataApi.query_data(query=query, dataset_id=PPA_DATASET)

    @classmethod
    def get_many_measures(cls, report_id: str, measures: Tuple[str, ...], start_date: dt.date = None,
                          end_date: dt.date = None):
        fields = []
        for measure in measures:
            fields.append(measure)
        where = FieldValueMap(report_id=report_id)
        query = DataQuery(where=where, fields=fields, start_date=start_date, end_date=end_date)
        return GsDataApi.query_data(query=query, dataset_id=PPA_DATASET)


class RiskReport(BaseReport):

    def get_factor_data(self, factor: str, start_date: dt.date = None, end_date: dt.date = None):
        return GsReportApi.get_risk_factor_data_results(self.get_id(), [factor], start_date, end_date)

    def get_risk_model_id(self):
        return self.get_parameters().risk_model
