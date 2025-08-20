"""
Copyright 2020 Goldman Sachs.
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

import copy
import datetime as dt

import numpy as np
import pandas as pd
import pytest
from testfixtures import Replacer
from testfixtures.mock import Mock

import gs_quant.timeseries.measures_portfolios as mp
from gs_quant.api.gs.assets import GsTemporalXRef
from gs_quant.api.gs.data import MarketDataResponseFrame
from gs_quant.data import DataCoordinate
from gs_quant.data.core import DataContext
from gs_quant.errors import MqValueError
from gs_quant.markets.index import Index
from gs_quant.markets.report import PerformanceReport, ThematicReport
from gs_quant.markets.securities import Stock, Bond
from gs_quant.models.risk_model import FactorRiskModel as Factor_Risk_Model
from gs_quant.common import ReportParameters, XRef
from gs_quant.target.reports import Report, PositionSourceType, ReportType
from gs_quant.target.risk_models import RiskModel, RiskModelCoverage, RiskModelTerm, RiskModelUniverseIdentifier

risk_model = RiskModel(coverage=RiskModelCoverage.Country, id_='model_id', name='Fake Risk Model',
                       term=RiskModelTerm.Long, universe_identifier=RiskModelUniverseIdentifier.gsid, vendor='GS',
                       version=1.0)

factor_risk_report = Report(position_source_id='position source id',
                            position_source_type=PositionSourceType.Portfolio,
                            type_=ReportType.Portfolio_Factor_Risk,
                            id_='report_id',
                            parameters=ReportParameters(risk_model='risk_model_id'),
                            status='new')

asset_factor_risk_report = Report(position_source_id='position source id',
                                  position_source_type=PositionSourceType.Asset,
                                  type_=ReportType.Portfolio_Factor_Risk,
                                  id_='report_id',
                                  parameters=ReportParameters(risk_model='risk_model_id'),
                                  status='new')

ppa_report = PerformanceReport(position_source_id='position source id',
                               position_source_type=PositionSourceType.Portfolio,
                               type_=ReportType.Portfolio_Performance_Analytics,
                               id_='report_id',
                               parameters=ReportParameters(risk_model='risk_model_id'),
                               status='new')

factor_data = [
    {
        'date': '2020-11-23',
        'reportId': 'report_id',
        'factor': 'Factor Name',
        'factorCategory': 'CNT',
        'pnl': 11.23,
        'exposure': -11.23,
        'proportionOfRisk': 1
    },
    {
        'date': '2020-11-24',
        'reportId': 'report_id',
        'factor': 'Factor Name',
        'factorCategory': 'CNT',
        'pnl': 11.24,
        'exposure': -11.24,
        'proportionOfRisk': 2
    },
    {
        'date': '2020-11-25',
        'reportId': 'report_id',
        'factor': 'Factor Name',
        'factorCategory': 'CNT',
        'pnl': 11.25,
        'exposure': -11.25,
        'proportionOfRisk': 3
    },
    {
        'date': '2020-11-23',
        'reportId': 'report_id',
        'factor': 'Total',
        'factorCategory': 'CNT',
        'pnl': 19.23,
        'exposure': -11.23,
        'proportionOfRisk': 1
    },
    {
        'date': '2020-11-24',
        'reportId': 'report_id',
        'factor': 'Total',
        'factorCategory': 'CNT',
        'pnl': 14.24,
        'exposure': -11.24,
        'proportionOfRisk': 2
    },
    {
        'date': '2020-11-25',
        'reportId': 'report_id',
        'factor': 'Total',
        'factorCategory': 'CNT',
        'pnl': 21.25,
        'exposure': -11.25,
        'proportionOfRisk': 3
    }
]

aum_data = {
    '2020-01-01': 1,
    '2020-01-02': 2,
    '2020-01-03': 1,
    '2020-01-04': 1,
    '2020-01-05': 1,
    '2020-01-06': 3
}

yield_data = {
    pd.Timestamp('2020-01-01'): .01,
    pd.Timestamp('2020-01-02'): .02,
    pd.Timestamp('2020-01-03'): .025,
    pd.Timestamp('2020-01-04'): .03,
    pd.Timestamp('2020-01-05'): .04,
}

thematic_data = [
    {
        "date": "2021-07-12",
        "reportId": "PTAID",
        "basketId": "MA01GPR89HZF1FZ5",
        "region": "Asia",
        "grossExposure": 3.448370345015856E8,
        "thematicExposure": 2,
        "thematicBeta": 1,
        "updateTime": "2021-07-20T23:43:38Z"
    },
    {
        "date": "2021-07-13",
        "reportId": "PTAID",
        "basketId": "MA01GPR89HZF1FZ5",
        "region": "Asia",
        "grossExposure": 3.375772519907556E8,
        "thematicExposure": 2,
        "thematicBeta": 1,
        "updateTime": "2021-07-20T23:43:38Z"
    },
    {
        "date": "2021-07-14",
        "reportId": "PTAID",
        "basketId": "MA01GPR89HZF1FZ5",
        "region": "Asia",
        "grossExposure": 3.321189950666118E8,
        "thematicExposure": 2,
        "thematicBeta": 1,
        "updateTime": "2021-07-20T23:43:38Z"
    },
    {
        "date": "2021-07-15",
        "reportId": "PTAID",
        "basketId": "MA01GPR89HZF1FZ5",
        "region": "Asia",
        "grossExposure": 3.274071805135091E8,
        "thematicExposure": 2,
        "thematicBeta": 1,
        "updateTime": "2021-07-20T23:43:38Z"
    }
]

aggregate_factor_data = [
    {
        'date': '2020-11-23',
        'reportId': 'report_id',
        'factor': 'Factor',
        'factorCategory': 'CNT',
        'pnl': 11.23,
        'exposure': -11.23,
        'proportionOfRisk': 1,
        'dailyRisk': 1,
        'annualRisk': 1
    },
    {
        'date': '2020-11-24',
        'reportId': 'report_id',
        'factor': 'Factor',
        'factorCategory': 'CNT',
        'pnl': 11.24,
        'exposure': -11.24,
        'proportionOfRisk': 2,
        'dailyRisk': 2,
        'annualRisk': 2
    },
    {
        'date': '2020-11-25',
        'reportId': 'report_id',
        'factor': 'Factor',
        'factorCategory': 'CNT',
        'pnl': 11.25,
        'exposure': -11.25,
        'proportionOfRisk': 3,
        'dailyRisk': 3,
        'annualRisk': 3
    }
]


def mock_risk_model():
    risk_model = RiskModel(coverage=RiskModelCoverage.Country, id_='model_id', name='Fake Risk Model',
                           term=RiskModelTerm.Long, universe_identifier=RiskModelUniverseIdentifier.gsid, vendor='GS',
                           version=1.0)

    replace = Replacer()

    # mock getting risk model entity()
    mock = replace('gs_quant.api.gs.risk_models.GsRiskModelApi.get_risk_model', Mock())
    mock.return_value = risk_model

    actual = Factor_Risk_Model.get(model_id='model_id')
    replace.restore()
    return actual


def test_portfolio_factor_exposure():
    replace = Replacer()

    # mock getting risk model entity()
    mock = replace('gs_quant.api.gs.risk_models.GsRiskModelApi.get_risk_model', Mock())
    mock.return_value = risk_model

    mock = replace('gs_quant.api.gs.reports.GsReportApi.get_report', Mock())
    mock.return_value = factor_risk_report

    mock = replace('gs_quant.api.gs.reports.GsReportApi.get_reports', Mock())
    mock.return_value = [factor_risk_report]

    # mock getting report factor data
    mock = replace('gs_quant.api.gs.reports.GsReportApi.get_factor_risk_report_results', Mock())
    mock.return_value = factor_data

    # mock getting risk model dates
    mock = replace('gs_quant.api.gs.risk_models.GsRiskModelApi.get_risk_model_dates', Mock())
    mock.return_value = ['2010-01-01']

    # mock getting risk model factor category
    mock = replace('gs_quant.api.gs.risk_models.GsFactorRiskModelApi.get_risk_model_data', Mock())
    mock.return_value = {
        'results': [{
            'factorData': [{
                'factorId': 'factor_id',
                'factorCategory': 'Factor Name'
            }]}
        ]}

    # mock getting risk model factor entity
    mock = replace('gs_quant.api.gs.risk_models.GsFactorRiskModelApi.get_risk_model_factor_data', Mock())
    mock.return_value = [{
        'identifier': 'factor_id',
        'type': 'Factor',
        'name': 'Factor Name',
        'factorCategory': 'Factor Name'
    }]

    with DataContext(dt.date(2020, 11, 23), dt.date(2020, 11, 25)):
        actual = mp.portfolio_factor_exposure('report_id', 'risk_model_id', 'Factor Name')
        assert all(actual.values == [-11.23, -11.24, -11.25])

    with pytest.raises(MqValueError):
        mp.portfolio_factor_exposure('report_id', 'risk_model_id', 'Wrong Factor Name')
    replace.restore()


def test_portfolio_factor_pnl():
    replace = Replacer()

    # mock getting risk model entity()
    mock = replace('gs_quant.api.gs.risk_models.GsRiskModelApi.get_risk_model', Mock())
    mock.return_value = risk_model

    mock = replace('gs_quant.api.gs.reports.GsReportApi.get_report', Mock())
    mock.return_value = factor_risk_report

    mock = replace('gs_quant.api.gs.reports.GsReportApi.get_reports', Mock())
    mock.return_value = [factor_risk_report]

    # mock getting risk model dates
    mock = replace('gs_quant.api.gs.risk_models.GsRiskModelApi.get_risk_model_dates', Mock())
    mock.return_value = ['2010-01-01']

    # mock getting risk model factor category
    mock = replace('gs_quant.api.gs.risk_models.GsFactorRiskModelApi.get_risk_model_data', Mock())
    mock.return_value = {
        'results': [{
            'factorData': [{
                'factorId': 'factor_id',
                'factorCategory': 'Factor Name'
            }]}
        ]}

    # mock getting risk model factor entity
    mock = replace('gs_quant.api.gs.risk_models.GsFactorRiskModelApi.get_risk_model_factor_data', Mock())
    mock.return_value = [{
        'identifier': 'factor_id',
        'type': 'Factor',
        'name': 'Factor Name',
        'factorCategory': 'Factor Name'
    }]

    with DataContext(dt.date(2020, 11, 23), dt.date(2020, 11, 25)):
        # mock getting report factor data
        mock = replace('gs_quant.api.gs.reports.GsReportApi.get_factor_risk_report_results', Mock())
        mock.return_value = factor_data

        actual = mp.portfolio_factor_pnl('report_id', 'risk_model_id', 'Factor Name')
        assert all(actual.values == [11.23, 11.24, 11.25])

    with DataContext(dt.date(2020, 11, 22), dt.date(2020, 11, 25)):
        # mock getting report factor data with first day set to 0
        factor_data_copy = copy.copy(factor_data)
        factor_data_copy.insert(0, {
            'date': '2020-11-22',
            'reportId': 'report_id',
            'factor': 'Factor Name',
            'factorCategory': 'CNT',
            'pnl': 0,
            'exposure': -11.23,
            'proportionOfRisk': 1
        })
        mock = replace('gs_quant.api.gs.reports.GsReportApi.get_factor_risk_report_results', Mock())
        mock.return_value = factor_data_copy

        actual = mp.portfolio_factor_pnl('report_id', 'risk_model_id', 'Factor Name')
        assert all(actual.values == [0.0, 11.23, 11.24, 11.25])

    with pytest.raises(MqValueError):
        mp.portfolio_factor_pnl('report_id', 'risk_model_id', 'Wrong Factor Name')
    replace.restore()


def test_portfolio_factor_proportion_of_risk():
    replace = Replacer()

    # mock getting risk model entity()
    mock = replace('gs_quant.api.gs.risk_models.GsRiskModelApi.get_risk_model', Mock())
    mock.return_value = risk_model

    mock = replace('gs_quant.api.gs.reports.GsReportApi.get_report', Mock())
    mock.return_value = factor_risk_report

    mock = replace('gs_quant.api.gs.reports.GsReportApi.get_reports', Mock())
    mock.return_value = [factor_risk_report]

    # mock getting report factor data
    mock = replace('gs_quant.api.gs.reports.GsReportApi.get_factor_risk_report_results', Mock())
    mock.return_value = factor_data

    # mock getting risk model dates
    mock = replace('gs_quant.api.gs.risk_models.GsRiskModelApi.get_risk_model_dates', Mock())
    mock.return_value = ['2010-01-01']

    # mock getting risk model factor category
    mock = replace('gs_quant.api.gs.risk_models.GsFactorRiskModelApi.get_risk_model_data', Mock())
    mock.return_value = {
        'results': [{
            'factorData': [{
                'factorId': 'factor_id',
                'factorCategory': 'Factor Name'
            }]}
        ]}

    # mock getting risk model factor entity
    mock = replace('gs_quant.api.gs.risk_models.GsFactorRiskModelApi.get_risk_model_factor_data', Mock())
    mock.return_value = [{
        'identifier': 'factor_id',
        'type': 'Factor',
        'name': 'Factor Name',
        'factorCategory': 'Factor Name'
    }]

    with DataContext(dt.date(2020, 11, 23), dt.date(2020, 11, 25)):
        actual = mp.portfolio_factor_proportion_of_risk('report_id', 'risk_model_id', 'Factor Name')
        assert all(actual.values == [1, 2, 3])

    with pytest.raises(MqValueError):
        mp.portfolio_factor_proportion_of_risk('report_id', 'risk_model_id', 'Wrong Factor Name')
    replace.restore()


def test_portfolio_thematic_exposure():
    replace = Replacer()

    # mock getting PTA report
    mock = replace('gs_quant.markets.report.ThematicReport.get', Mock())
    mock.return_value = ThematicReport(id='report_id')

    mock = replace('gs_quant.entities.entity.PositionedEntity.get_thematic_report', Mock())
    mock.return_value = ThematicReport(id='report_id')

    # mock getting thematic exposure
    mock = replace('gs_quant.markets.report.ThematicReport.get_thematic_exposure', Mock())
    mock.return_value = pd.DataFrame(thematic_data)

    # mock getting asset
    mock = Stock('MAA0NE9QX2ABETG6', 'Test Asset')
    xrefs = replace('gs_quant.timeseries.measures.GsAssetApi.get_asset_xrefs', Mock())
    xrefs.return_value = [
        GsTemporalXRef(dt.date(2019, 1, 1),
                       dt.date(2952, 12, 31),
                       XRef(ticker='basket_ticker', ))
    ]
    replace('gs_quant.markets.securities.SecurityMaster.get_asset', Mock()).return_value = mock

    with DataContext(dt.date(2020, 7, 12), dt.date(2020, 7, 15)):
        actual = mp.portfolio_thematic_exposure('report_id', 'basket_ticker')
        assert all(actual.values == [2, 2, 2, 2])

    replace.restore()


def test_portfolio_pnl():
    replace = Replacer()

    performance_report = PerformanceReport(report_id='RP1',
                                           position_source_type='Portfolio',
                                           position_source_id='MP1',
                                           report_type='Portfolio Performance Analytics',
                                           parameters=ReportParameters(transaction_cost_model='FIXED'))

    # mock PerformanceReport.get()
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = performance_report

    mock = replace('gs_quant.markets.portfolio_manager.PortfolioManager.get_performance_report', Mock())
    mock.return_value = performance_report

    # mock PerformanceReport.get_pnl()
    mock = replace('gs_quant.markets.report.PerformanceReport.get_pnl', Mock())
    mock.return_value = pd.DataFrame.from_dict(
        {'date': ['2022-07-01', '2022-07-02', '2022-07-03'], 'pnl': [200, 400, 600]})

    with DataContext(dt.date(2022, 7, 1), dt.date(2022, 7, 3)):
        actual = mp.portfolio_pnl('RP1')
        assert all(actual.values == [200, 400, 600])

    replace.restore()


def test_aggregate_factor_support():
    replace = Replacer()

    # mock getting risk model entity()
    mock = replace('gs_quant.entities.entity.PositionedEntity.get_factor_risk_report', Mock())
    mock.return_value = risk_model

    mock = replace('gs_quant.api.gs.reports.GsReportApi.get_report', Mock())
    mock.return_value = factor_risk_report

    mock = replace('gs_quant.api.gs.reports.GsReportApi.get_report', Mock())
    mock.return_value = factor_risk_report

    # mock getting report factor data
    mock = replace('gs_quant.api.gs.reports.GsReportApi.get_factor_risk_report_results', Mock())
    mock.return_value = aggregate_factor_data

    # mock getting risk model dates
    mock = replace('gs_quant.api.gs.risk_models.GsRiskModelApi.get_risk_model_dates', Mock())
    mock.return_value = ['2010-01-01']

    # mock getting risk model factor category
    mock = replace('gs_quant.api.gs.risk_models.GsFactorRiskModelApi.get_risk_model_data', Mock())
    mock.return_value = {
        'results': [{
            'factorData': [{
                'factorId': 'factor_id',
                'factorCategory': 'Factor Name'
            }]}
        ]}

    # mock getting risk model factor entity
    mock = replace('gs_quant.api.gs.risk_models.GsFactorRiskModelApi.get_risk_model_factor_data', Mock())
    mock.return_value = [{
        'identifier': 'factor_id',
        'type': 'Factor',
        'name': 'Factor Name',
        'factorCategory': 'Factor Name'
    }]

    with DataContext(dt.date(2020, 11, 23), dt.date(2020, 11, 25)):
        actual = mp.portfolio_factor_proportion_of_risk('portfolio_id', 'report_id', 'Factor')
        assert all(actual.values == [1, 2, 3])

    with DataContext(dt.date(2020, 11, 23), dt.date(2020, 11, 25)):
        actual = mp.portfolio_daily_risk('portfolio_id', 'report_id', 'Factor')
        assert all(actual.values == [1, 2, 3])

    with DataContext(dt.date(2020, 11, 23), dt.date(2020, 11, 25)):
        actual = mp.portfolio_annual_risk('portfolio_id', 'report_id', 'Factor')
        assert all(actual.values == [1, 2, 3])

    with pytest.raises(MqValueError):
        mp.portfolio_daily_risk('portfolio_id', 'report_id', 'Factor Name')

    with pytest.raises(MqValueError):
        mp.portfolio_annual_risk('portfolio_id', 'report_id', 'Factor Name')
    replace.restore()


def test_hit_rate():
    replace = Replacer()
    data = {
        'pnl': [
            .2,
            0,
            1,
            -.97
        ],
        'date': [
            '2020-01-01',
            '2020-01-01',
            '2020-01-02',
            '2020-01-02'
        ],
        'entryType': [
            'Holding',
            'Holding',
            'Holding',
            'Holding'
        ],
        'assetId': [
            'asset1',
            'asset2',
            'asset1',
            'asset2'
        ]
    }

    timeseries = {
        '2020-01-02': .5
    }

    mock = replace('gs_quant.markets.report.PerformanceReport.get_portfolio_constituents', Mock())
    mock.return_value = pd.DataFrame(data)
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport()
    mock = replace('gs_quant.markets.portfolio_manager.PortfolioManager.get_performance_report', Mock())
    mock.return_value = PerformanceReport()

    expected = pd.Series(timeseries)
    with DataContext(dt.date(2020, 1, 1), dt.date(2019, 1, 2)):
        returned = mp.portfolio_hit_rate("test", 2)
        assert np.allclose(expected.dropna(), returned.dropna(), atol=1e-6)
    replace.restore()


def test_max_drawdown():
    replace = Replacer()
    data = {
        '2020-01-01': 1,
        '2020-01-02': 2,
        '2020-01-03': 1,
        '2020-01-04': 0
    }

    timeseries = {
        pd.Timestamp('2020-01-01 00:00:00'): np.nan,
        pd.Timestamp('2020-01-02 00:00:00'): np.nan,
        pd.Timestamp('2020-01-03 00:00:00'): np.nan,
        pd.Timestamp('2020-01-04 00:00:00'): -1
    }

    mock = replace('gs_quant.markets.report.PerformanceReport.get_aum', Mock())
    mock.return_value = data
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport()
    mock = replace('gs_quant.markets.portfolio_manager.PortfolioManager.get_performance_report', Mock())
    mock.return_value = PerformanceReport()

    max_drawdown_series = pd.Series(timeseries)
    with DataContext(dt.date(2020, 1, 1), dt.date(2019, 1, 4)):
        returned = mp.portfolio_max_drawdown("test", 4)
        assert max_drawdown_series.equals(returned)
    replace.restore()


def test_max_recovery_period():
    replace = Replacer()

    timeseries = {
        pd.Timestamp('2020-01-01 00:00:00'): np.nan,
        pd.Timestamp('2020-01-02 00:00:00'): np.nan,
        pd.Timestamp('2020-01-03 00:00:00'): np.nan,
        pd.Timestamp('2020-01-04 00:00:00'): np.nan,
        pd.Timestamp('2020-01-05 00:00:00'): np.nan,
        pd.Timestamp('2020-01-06 00:00:00'): 3
    }

    mock = replace('gs_quant.markets.report.PerformanceReport.get_aum', Mock())
    mock.return_value = aum_data
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport()
    mock = replace('gs_quant.markets.portfolio_manager.PortfolioManager.get_performance_report', Mock())
    mock.return_value = PerformanceReport()

    max_drawdown_series = pd.Series(timeseries)
    with DataContext(dt.date(2020, 1, 1), dt.date(2019, 1, 6)):
        returned = mp.portfolio_max_recovery_period("test", 6)
        assert max_drawdown_series.equals(returned)
    replace.restore()


def test_drawdown_length():
    replace = Replacer()

    timeseries = {
        pd.Timestamp('2020-01-01 00:00:00'): np.nan,
        pd.Timestamp('2020-01-02 00:00:00'): np.nan,
        pd.Timestamp('2020-01-03 00:00:00'): np.nan,
        pd.Timestamp('2020-01-04 00:00:00'): np.nan,
        pd.Timestamp('2020-01-05 00:00:00'): np.nan,
        pd.Timestamp('2020-01-06 00:00:00'): 3
    }

    mock = replace('gs_quant.markets.report.PerformanceReport.get_aum', Mock())
    mock.return_value = aum_data
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport()
    mock = replace('gs_quant.markets.portfolio_manager.PortfolioManager.get_performance_report', Mock())
    mock.return_value = PerformanceReport()

    max_drawdown_series = pd.Series(timeseries)
    with DataContext(dt.date(2020, 1, 1), dt.date(2019, 1, 6)):
        returned = mp.portfolio_drawdown_length("test", 6)
        assert max_drawdown_series.equals(returned)
    replace.restore()


def test_standard_deviation():
    replace = Replacer()
    data = {
        'pnl': [
            4,
            5,
            6
        ],
        'date': [
            '2020-01-01',
            '2020-01-02',
            '2020-01-03'
        ]
    }

    timeseries = {
        '2020-01-01': np.nan,
        '2020-01-02': np.nan,
        '2020-01-03': 1.41421
    }
    mock = replace('gs_quant.markets.report.PerformanceReport.get_aum', Mock())
    mock.return_value = aum_data
    mock = replace('gs_quant.markets.report.PerformanceReport.get_pnl', Mock())
    mock.return_value = pd.DataFrame(data)
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport()
    mock = replace('gs_quant.markets.portfolio_manager.PortfolioManager.get_performance_report', Mock())
    mock.return_value = PerformanceReport()

    expected = pd.Series(timeseries)
    with DataContext(dt.date(2020, 1, 1), dt.date(2019, 1, 2)):
        returned = mp.portfolio_standard_deviation("test", '2d')
        assert np.allclose(expected.dropna(), returned.dropna(), atol=1e-6)
    replace.restore()


def test_downside_risk():
    replace = Replacer()
    data = {
        'pnl': [
            4,
            -7,
            6
        ],
        'date': [
            '2020-01-01',
            '2020-01-02',
            '2020-01-03'
        ]
    }

    timeseries = {
        '2020-01-01': np.nan,
        '2020-01-02': np.nan,
        '2020-01-03': 5
    }
    mock = replace('gs_quant.markets.report.PerformanceReport.get_aum', Mock())
    mock.return_value = aum_data
    mock = replace('gs_quant.markets.report.PerformanceReport.get_pnl', Mock())
    mock.return_value = pd.DataFrame(data)
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport()
    mock = replace('gs_quant.markets.portfolio_manager.PortfolioManager.get_performance_report', Mock())
    mock.return_value = PerformanceReport()

    expected = pd.Series(timeseries)
    with DataContext(dt.date(2020, 1, 1), dt.date(2019, 1, 2)):
        returned = mp.portfolio_downside_risk("test", 2)
        assert np.allclose(expected.dropna(), returned.dropna(), atol=1e-6)
    replace.restore()


def test_semi_variance():
    replace = Replacer()
    data = {
        'pnl': [
            4,
            -7,
            6,
            7
        ],
        'date': [
            '2020-01-01',
            '2020-01-02',
            '2020-01-03',
            '2020-01-04'
        ]
    }

    timeseries = {
        '2020-01-01': np.nan,
        '2020-01-02': np.nan,
        '2020-01-04': 8
    }
    mock = replace('gs_quant.markets.report.PerformanceReport.get_aum', Mock())
    mock.return_value = aum_data
    mock = replace('gs_quant.markets.report.PerformanceReport.get_pnl', Mock())
    mock.return_value = pd.DataFrame(data)
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport()
    mock = replace('gs_quant.markets.portfolio_manager.PortfolioManager.get_performance_report', Mock())
    mock.return_value = PerformanceReport()

    expected = pd.Series(timeseries)
    with DataContext(dt.date(2020, 1, 1), dt.date(2019, 1, 2)):
        returned = mp.portfolio_semi_variance("test", 3)
        assert np.allclose(expected.dropna(), returned.dropna(), atol=1e-6)
    replace.restore()


def test_kurtosis():
    replace = Replacer()
    data = {
        'pnl': [
            -1,
            0,
            1,

        ],
        'date': [
            '2020-01-01',
            '2020-01-02',
            '2020-01-03'
        ]
    }

    timeseries = {
        '2020-01-01': np.nan,
        '2020-01-02': np.nan,
        '2020-01-03': -2
    }
    mock = replace('gs_quant.markets.report.PerformanceReport.get_aum', Mock())
    mock.return_value = aum_data
    mock = replace('gs_quant.markets.report.PerformanceReport.get_pnl', Mock())
    mock.return_value = pd.DataFrame(data)
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport()
    mock = replace('gs_quant.markets.portfolio_manager.PortfolioManager.get_performance_report', Mock())
    mock.return_value = PerformanceReport()

    expected = pd.Series(timeseries)
    with DataContext(dt.date(2020, 1, 1), dt.date(2019, 1, 2)):
        returned = mp.portfolio_kurtosis("test", 2)
        assert np.allclose(expected.dropna(), returned.dropna(), atol=1e-6)
    replace.restore()


def test_skewness():
    replace = Replacer()
    data = {
        'pnl': [
            -1,
            0,
            2,

        ],
        'date': [
            '2020-01-01',
            '2020-01-02',
            '2020-01-03'
        ]
    }

    timeseries = {
        '2020-01-01': np.nan,
        '2020-01-02': np.nan,
        '2020-01-03': 0
    }
    mock = replace('gs_quant.markets.report.PerformanceReport.get_aum', Mock())
    mock.return_value = aum_data
    mock = replace('gs_quant.markets.report.PerformanceReport.get_pnl', Mock())
    mock.return_value = pd.DataFrame(data)
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport()
    mock = replace('gs_quant.markets.portfolio_manager.PortfolioManager.get_performance_report', Mock())
    mock.return_value = PerformanceReport()

    expected = pd.Series(timeseries)
    with DataContext(dt.date(2020, 1, 1), dt.date(2019, 1, 2)):
        returned = mp.portfolio_skewness("test", 2)
        assert np.allclose(expected.dropna(), returned.dropna(), atol=1e-6)
    replace.restore()


def test_realized_var():
    replace = Replacer()
    data = {
        'pnl': [
            1,
            1,
            1,

        ],
        'date': [
            '2020-01-01',
            '2020-01-02',
            '2020-01-03'
        ]
    }

    timeseries = {
        '2020-01-01': np.nan,
        '2020-01-02': np.nan,
        '2020-01-03': -0.52500
    }
    mock = replace('gs_quant.markets.report.PerformanceReport.get_aum', Mock())
    mock.return_value = aum_data
    mock = replace('gs_quant.markets.report.PerformanceReport.get_pnl', Mock())
    mock.return_value = pd.DataFrame(data)
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport()
    mock = replace('gs_quant.markets.portfolio_manager.PortfolioManager.get_performance_report', Mock())
    mock.return_value = PerformanceReport()

    expected = pd.Series(timeseries)
    with DataContext(dt.date(2020, 1, 1), dt.date(2019, 1, 2)):
        returned = mp.portfolio_realized_var("test", 2)
        assert np.allclose(expected.dropna(), returned.dropna(), atol=1e-6)
    replace.restore()


def test_bad_date():
    replace = Replacer()
    data = {
        'pnl': [
            1,
            1,
            1,

        ],
        'date': [
            '2020-01-01',
            '2020-01-02',
            '2020-01-03'
        ]
    }
    mock = replace('gs_quant.markets.report.PerformanceReport.get_aum', Mock())
    mock.return_value = aum_data
    mock = replace('gs_quant.markets.report.PerformanceReport.get_pnl', Mock())
    mock.return_value = pd.DataFrame(data)
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport()
    mock = replace('gs_quant.markets.portfolio_manager.PortfolioManager.get_performance_report', Mock())
    mock.return_value = PerformanceReport()

    with DataContext(dt.date(2020, 1, 1), dt.date(2019, 1, 2)):
        try:
            mp.portfolio_realized_var("test", "12p")
        except MqValueError:
            pass
        else:
            assert False

    replace.restore()


def test_tracking_error():
    replace = Replacer()

    data = {
        'pnl': [
            0,
            .02,
            .01,
            .01,
            .02

        ],
        'date': [
            '2020-01-01',
            '2020-01-02',
            '2020-01-03',
            '2020-01-04',
            '2020-01-05'
        ]
    }

    benchmark_data = {
        pd.Timestamp('2020-01-01'): 1,
        pd.Timestamp('2020-01-02'): 1.02,
        pd.Timestamp('2020-01-03'): 1.03,
        pd.Timestamp('2020-01-04'): 1.04,
        pd.Timestamp('2020-01-05'): 1.045
    }

    timeseries = {
        pd.Timestamp('2020-01-01'): np.nan,
        pd.Timestamp('2020-01-02'): np.nan,
        pd.Timestamp('2020-01-03'): 0.00340,
        pd.Timestamp('2020-01-04'): 0.003603,
        pd.Timestamp('2020-01-05'): 0.010537
    }

    mock = replace('gs_quant.markets.report.PerformanceReport.get_aum', Mock())
    mock.return_value = aum_data
    mock = replace('gs_quant.markets.report.PerformanceReport.get_pnl', Mock())
    mock.return_value = pd.DataFrame(data)
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport()

    mock = replace('gs_quant.markets.securities.SecurityMaster.get_asset', Mock())
    mock.return_value = Index("test", 'test', "test")
    mock = replace('gs_quant.entities.entity.Entity.get_data_coordinate', Mock())
    mock.return_value = DataCoordinate("test")
    mock = replace('gs_quant.data.coordinate.DataCoordinate.get_series', Mock())
    mock.return_value = pd.Series(benchmark_data)

    mock = replace('gs_quant.markets.portfolio_manager.PortfolioManager.get_performance_report', Mock())
    mock.return_value = PerformanceReport()

    expected = pd.Series(timeseries)
    with DataContext(dt.date(2020, 1, 1), dt.date(2019, 1, 2)):
        returned = mp.portfolio_tracking_error("test", 'test', 2)
        assert np.allclose(expected.dropna(), returned.dropna(), atol=1e-5)
    replace.restore()


def test_tracking_error_bull():
    replace = Replacer()
    data = {
        'pnl': [
            0,
            .02,
            .01,
            .01,
            .02

        ],
        'date': [
            '2020-01-01',
            '2020-01-02',
            '2020-01-03',
            '2020-01-04',
            '2020-01-05'
        ]
    }

    benchmark_data = {
        pd.Timestamp('2020-01-01'): 1,
        pd.Timestamp('2020-01-02'): 1.02,
        pd.Timestamp('2020-01-03'): 1.03,
        pd.Timestamp('2020-01-04'): 1.04,
        pd.Timestamp('2020-01-05'): 1.045
    }

    timeseries = {
        pd.Timestamp('2020-01-01'): np.nan,
        pd.Timestamp('2020-01-02'): np.nan,
        pd.Timestamp('2020-01-03'): 0.71771,
        pd.Timestamp('2020-01-04'): 0.70357,
        pd.Timestamp('2020-01-05'): 0.34648
    }

    mock = replace('gs_quant.markets.report.PerformanceReport.get_aum', Mock())
    mock.return_value = aum_data
    mock = replace('gs_quant.markets.report.PerformanceReport.get_pnl', Mock())
    mock.return_value = pd.DataFrame(data)
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport()

    mock = replace('gs_quant.markets.securities.SecurityMaster.get_asset', Mock())
    mock.return_value = Index("test", 'test', "test")
    mock = replace('gs_quant.entities.entity.Entity.get_data_coordinate', Mock())
    mock.return_value = DataCoordinate("test")
    mock = replace('gs_quant.data.coordinate.DataCoordinate.get_series', Mock())
    mock.return_value = pd.Series(benchmark_data)

    mock = replace('gs_quant.markets.portfolio_manager.PortfolioManager.get_performance_report', Mock())
    mock.return_value = PerformanceReport()

    expected = pd.Series(timeseries)
    with DataContext(dt.date(2020, 1, 1), dt.date(2019, 1, 2)):
        returned = mp.portfolio_tracking_error_bull("test", 'test', 2)
        assert np.allclose(expected.dropna(), returned.dropna(), atol=1e-6)
    replace.restore()


def test_tracking_error_bear():
    replace = Replacer()
    data = {
        'pnl': [
            0,
            .02,
            .01,
            .01,
            .02

        ],
        'date': [
            '2020-01-01',
            '2020-01-02',
            '2020-01-03',
            '2020-01-04',
            '2020-01-05'
        ]
    }

    benchmark_data = {
        pd.Timestamp('2020-01-01'): 1,
        pd.Timestamp('2020-01-02'): 1.02,
        pd.Timestamp('2020-01-03'): 1.03,
        pd.Timestamp('2020-01-04'): 1.04,
        pd.Timestamp('2020-01-05'): 1.045
    }

    timeseries = {
        pd.Timestamp('2020-01-01'): np.nan,
        pd.Timestamp('2020-01-02'): np.nan,
        pd.Timestamp('2020-01-03'): np.nan,
    }

    mock = replace('gs_quant.markets.report.PerformanceReport.get_aum', Mock())
    mock.return_value = aum_data
    mock = replace('gs_quant.markets.report.PerformanceReport.get_pnl', Mock())
    mock.return_value = pd.DataFrame(data)
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport()

    mock = replace('gs_quant.markets.securities.SecurityMaster.get_asset', Mock())
    mock.return_value = Index("test", 'test', "test")
    mock = replace('gs_quant.entities.entity.Entity.get_data_coordinate', Mock())
    mock.return_value = DataCoordinate("test")
    mock = replace('gs_quant.data.coordinate.DataCoordinate.get_series', Mock())
    mock.return_value = pd.Series(benchmark_data)

    mock = replace('gs_quant.markets.portfolio_manager.PortfolioManager.get_performance_report', Mock())
    mock.return_value = PerformanceReport()

    expected = pd.Series(timeseries)
    with DataContext(dt.date(2020, 1, 1), dt.date(2019, 1, 2)):
        returned = mp.portfolio_tracking_error_bear("test", 'test', 2)
        assert np.allclose(expected.dropna(), returned.dropna(), atol=1e-5)
    replace.restore()


def test_sharpe_ratio():
    replace = Replacer()
    data = {
        'pnl': [
            0,
            .02,
            .02,
            .01,
            .02

        ],
        'date': [
            '2020-01-01',
            '2020-01-02',
            '2020-01-03',
            '2020-01-04',
            '2020-01-05'
        ]
    }

    benchmark_data = {
        pd.Timestamp('2020-01-01'): .02,
        pd.Timestamp('2020-01-02'): .02,
        pd.Timestamp('2020-01-03'): .03,
        pd.Timestamp('2020-01-04'): .04,
        pd.Timestamp('2020-01-05'): .045
    }

    timeseries = {
        pd.Timestamp('2020-01-01'): np.nan,
        pd.Timestamp('2020-01-02'): np.nan,
        pd.Timestamp('2020-01-03'): np.nan,
        pd.Timestamp('2020-01-04'): 32.60231,
        pd.Timestamp('2020-01-05'): 33.77863,
    }
    aum_data = {
        '2020-01-01': 1.00,
        '2020-01-02': 1.035,
        '2020-01-03': 1.05,
        '2020-01-04': 1.06,
        '2020-01-05': 1.065
    }

    mock = replace('gs_quant.markets.report.PerformanceReport.get_aum', Mock())
    mock.return_value = aum_data
    mock = replace('gs_quant.markets.report.PerformanceReport.get_pnl', Mock())
    mock.return_value = pd.DataFrame(data)
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport()

    mock = replace('gs_quant.markets.securities.SecurityMaster.get_asset', Mock())
    mock.return_value = Index("test", 'test', "test")
    mock = replace('gs_quant.entities.entity.Entity.get_data_coordinate', Mock())
    mock.return_value = DataCoordinate("test")
    mock = replace('gs_quant.data.coordinate.DataCoordinate.get_series', Mock())
    mock.return_value = pd.Series(benchmark_data)

    mock = replace('gs_quant.markets.portfolio_manager.PortfolioManager.get_performance_report', Mock())
    mock.return_value = PerformanceReport()

    expected = pd.Series(timeseries)
    with DataContext(dt.date(2020, 1, 1), dt.date(2019, 1, 2)):
        returned = mp.portfolio_sharpe_ratio("test", 'test', 2)
        assert np.allclose(expected.dropna(), returned.dropna(), atol=1e-5)
    replace.restore()


def test_calmar_ratio():
    replace = Replacer()
    data = {
        'pnl': [
            0,
            .02,
            .01,
            .04,
            .03

        ],
        'date': [
            '2020-01-01',
            '2020-01-02',
            '2020-01-03',
            '2020-01-04',
            '2020-01-05'
        ]
    }

    yield_data = {
        pd.Timestamp('2020-01-01'): .01,
        pd.Timestamp('2020-01-02'): .02,
        pd.Timestamp('2020-01-03'): .03,
        pd.Timestamp('2020-01-04'): .03,
        pd.Timestamp('2020-01-05'): .03
    }

    timeseries = {
        pd.Timestamp('2020-01-04 00:00:00'): 16.20658,
        pd.Timestamp('2020-01-05 00:00:00'): 30.31192
    }

    aum_data = {
        '2020-01-01': 1.00,
        '2020-01-02': .95,
        '2020-01-03': 1.05,
        '2020-01-04': 1.03,
        '2020-01-05': 1.065
    }

    mock = replace('gs_quant.markets.report.PerformanceReport.get_aum', Mock())
    mock.return_value = aum_data
    mock = replace('gs_quant.markets.report.PerformanceReport.get_pnl', Mock())
    mock.return_value = pd.DataFrame(data)
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport()

    mock = replace('gs_quant.markets.securities.SecurityMaster.get_asset', Mock())
    mock.return_value = Bond("test", 'test', )
    mock = replace('gs_quant.entities.entity.Entity.get_data_coordinate', Mock())
    mock.return_value = DataCoordinate("test")
    mock = replace('gs_quant.data.coordinate.DataCoordinate.get_series', Mock())
    mock.return_value = pd.Series(yield_data)

    mock = replace('gs_quant.markets.portfolio_manager.PortfolioManager.get_performance_report', Mock())
    mock.return_value = PerformanceReport()

    expected = pd.Series(timeseries)
    with DataContext(dt.date(2020, 1, 1), dt.date(2019, 1, 2)):
        returned = mp.portfolio_calmar_ratio("test", 3)
        assert np.allclose(expected.dropna(), returned.dropna(), atol=1e-5)
    replace.restore()


def test_sortino_ratio():
    replace = Replacer()
    data = {
        'pnl': [
            .02,
            .02,
            -.01,
            .02,
            .01

        ],
        'date': [
            '2020-01-01',
            '2020-01-02',
            '2020-01-03',
            '2020-01-04',
            '2020-01-05'
        ]
    }

    yield_data = {
        pd.Timestamp('2020-01-01'): .001,
        pd.Timestamp('2020-01-02'): .07,
        pd.Timestamp('2020-01-03'): .08,
        pd.Timestamp('2020-01-04'): .075,
        pd.Timestamp('2020-01-05'): .02
    }

    timeseries = {
        pd.Timestamp('2020-01-04 00:00:00'): 15.063383,
        pd.Timestamp('2020-01-05 00:00:00'): 10.128712,
    }

    aum_data = {
        '2020-01-01': 1.00,
        '2020-01-02': .95,
        '2020-01-03': .9,
        '2020-01-04': 1.03,
        '2020-01-05': 1.065
    }

    mock = replace('gs_quant.markets.report.PerformanceReport.get_aum', Mock())
    mock.return_value = aum_data
    mock = replace('gs_quant.markets.report.PerformanceReport.get_pnl', Mock())
    mock.return_value = pd.DataFrame(data)
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport()

    mock = replace('gs_quant.markets.securities.SecurityMaster.get_asset', Mock())
    mock.return_value = Bond("test", 'test', )
    mock = replace('gs_quant.entities.entity.Entity.get_data_coordinate', Mock())
    mock.return_value = DataCoordinate("test")
    mock = replace('gs_quant.data.coordinate.DataCoordinate.get_series', Mock())
    mock.return_value = pd.Series(yield_data)

    mock = replace('gs_quant.markets.portfolio_manager.PortfolioManager.get_performance_report', Mock())
    mock.return_value = PerformanceReport()

    expected = pd.Series(timeseries)
    with DataContext(dt.date(2020, 1, 1), dt.date(2019, 1, 2)):
        returned = mp.portfolio_sortino_ratio("test", "test", 3)
        assert np.allclose(expected.dropna(), returned.dropna(), atol=1e-6)
    replace.restore()


def test_sortino_ratio_index():
    replace = Replacer()
    data = {
        'pnl': [
            .02,
            .02,
            -.01,
            .02,
            .01

        ],
        'date': [
            '2020-01-01',
            '2020-01-02',
            '2020-01-03',
            '2020-01-04',
            '2020-01-05'
        ]
    }

    pricing_data = {
        pd.Timestamp('2020-01-01'): .001,
        pd.Timestamp('2020-01-02'): .07,
        pd.Timestamp('2020-01-03'): .07,
        pd.Timestamp('2020-01-04'): .001,
        pd.Timestamp('2020-01-05'): .02
    }

    timeseries = {
        pd.Timestamp('2020-01-05 00:00:00'): -8.355985
    }

    aum_data = {
        '2020-01-01': 1.00,
        '2020-01-02': .95,
        '2020-01-03': .9,
        '2020-01-04': 1.03,
        '2020-01-05': 1.065
    }

    mock = replace('gs_quant.markets.report.PerformanceReport.get_aum', Mock())
    mock.return_value = aum_data
    mock = replace('gs_quant.markets.report.PerformanceReport.get_pnl', Mock())
    mock.return_value = pd.DataFrame(data)
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport()

    mock = replace('gs_quant.markets.securities.SecurityMaster.get_asset', Mock())
    mock.return_value = Index("test", 'test', "test")
    mock = replace('gs_quant.entities.entity.Entity.get_data_coordinate', Mock())
    mock.return_value = DataCoordinate("test")
    mock = replace('gs_quant.data.coordinate.DataCoordinate.get_series', Mock())
    mock.return_value = pd.Series(pricing_data)

    mock = replace('gs_quant.markets.portfolio_manager.PortfolioManager.get_performance_report', Mock())
    mock.return_value = PerformanceReport()

    expected = pd.Series(timeseries)
    with DataContext(dt.date(2020, 1, 1), dt.date(2020, 1, 2)):
        returned = mp.portfolio_sortino_ratio("test", "test", 4)
        assert np.allclose(expected.dropna(), returned.dropna(), atol=1e-5)
    replace.restore()


def test_jensen_alpha():
    replace = Replacer()
    data = {
        'pnl': [
            .02,
            .02,
            .01,
            .02,
            .01

        ],
        'date': [
            '2020-01-01',
            '2020-01-02',
            '2020-01-03',
            '2020-01-04',
            '2020-01-05'
        ]
    }

    yield_data = {
        pd.Timestamp('2020-01-01'): .01,
        pd.Timestamp('2020-01-02'): .02,
        pd.Timestamp('2020-01-03'): .025,
        pd.Timestamp('2020-01-04'): .03,
        pd.Timestamp('2020-01-05'): .04,
    }

    timeseries = {
        pd.Timestamp('2020-01-04 00:00:00'): 0.01814,
        pd.Timestamp('2020-01-05 00:00:00'): 0.00661
    }

    mock = replace('gs_quant.markets.report.PerformanceReport.get_aum', Mock())
    mock.return_value = aum_data
    mock = replace('gs_quant.markets.report.PerformanceReport.get_pnl', Mock())
    mock.return_value = pd.DataFrame(data)
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport()

    mock = replace('gs_quant.markets.securities.SecurityMaster.get_asset', Mock())
    mock.return_value = Bond("test", 'test', )
    mock = replace('gs_quant.entities.entity.Entity.get_data_coordinate', Mock())
    mock.return_value = DataCoordinate("test")
    mock = replace('gs_quant.data.coordinate.DataCoordinate.get_series', Mock())
    mock.return_value = pd.Series(yield_data)

    mock = replace('gs_quant.markets.portfolio_manager.PortfolioManager.get_performance_report', Mock())
    mock.return_value = PerformanceReport()

    expected = pd.Series(timeseries)
    with DataContext(dt.date(2020, 1, 1), dt.date(2019, 1, 2)):
        returned = mp.portfolio_jensen_alpha("test", "test", 4)
        assert np.allclose(expected.dropna(), returned.dropna(), atol=1e-5)
    replace.restore()


def test_jensen_bull():
    replace = Replacer()

    benchmark_data = {
        pd.Timestamp('2020-01-01'): 6,
        pd.Timestamp('2020-01-02'): 5,
        pd.Timestamp('2020-01-03'): 7,
        pd.Timestamp('2020-01-04'): 9,
        pd.Timestamp('2020-01-08'): 10
    }

    data = {
        'pnl': [
            .02,
            .02,
            .01,
            .02,
            .01

        ],
        'date': [
            '2020-01-01',
            '2020-01-02',
            '2020-01-03',
            '2020-01-04',
            '2020-01-05'
        ]
    }

    yield_data = {
        pd.Timestamp('2020-01-01'): .01,
        pd.Timestamp('2020-01-02'): .02,
        pd.Timestamp('2020-01-03'): .025,
        pd.Timestamp('2020-01-04'): .03,
        pd.Timestamp('2020-01-05'): .04,
    }

    timeseries = {
        pd.Timestamp('2020-01-04 00:00:00'): 0.02530
    }

    mock = replace('gs_quant.markets.report.PerformanceReport.get_aum', Mock())
    mock.return_value = aum_data
    mock = replace('gs_quant.markets.report.PerformanceReport.get_pnl', Mock())
    mock.return_value = pd.DataFrame(data)
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport()

    mock = replace('gs_quant.markets.securities.SecurityMaster.get_asset', Mock())
    mock.return_value = Bond("test", 'test', )
    mock = replace('gs_quant.entities.entity.Entity.get_data_coordinate', Mock())
    mock.return_value = DataCoordinate("test")
    replace('gs_quant.data.coordinate.DataCoordinate.get_series',
            Mock(side_effect=[pd.Series(benchmark_data), pd.Series(yield_data)]))

    mock = replace('gs_quant.markets.portfolio_manager.PortfolioManager.get_performance_report', Mock())
    mock.return_value = PerformanceReport()

    expected = pd.Series(timeseries)
    with DataContext(dt.date(2020, 1, 1), dt.date(2019, 1, 2)):
        returned = mp.portfolio_jensen_alpha_bull("test", "test", 4)
        assert np.allclose(expected.dropna(), returned.dropna(), atol=1e-5)
    replace.restore()


def test_jensen_alpha_bear():
    replace = Replacer()

    benchmark_data = {
        pd.Timestamp('2020-01-01'): 6,
        pd.Timestamp('2020-01-02'): 5,
        pd.Timestamp('2020-01-03'): 7,
        pd.Timestamp('2020-01-04'): 9,
        pd.Timestamp('2020-01-08'): 10
    }

    data = {
        'pnl': [
            .02,
            -.02,
            -.01,
            -.02,
            -.01

        ],
        'date': [
            '2020-01-01',
            '2020-01-02',
            '2020-01-03',
            '2020-01-04',
            '2020-01-05'
        ]
    }

    yield_data = {
        pd.Timestamp('2020-01-01'): .01,
        pd.Timestamp('2020-01-02'): .02,
        pd.Timestamp('2020-01-03'): .025,
        pd.Timestamp('2020-01-04'): .03,
        pd.Timestamp('2020-01-05'): .04,
    }

    timeseries = {
        pd.Timestamp('2020-01-04 00:00:00'): -0.88850
    }

    mock = replace('gs_quant.markets.report.PerformanceReport.get_aum', Mock())
    mock.return_value = aum_data

    mock = replace('gs_quant.markets.report.PerformanceReport.get_pnl', Mock())
    mock.return_value = pd.DataFrame(data)
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport()

    mock = replace('gs_quant.markets.securities.SecurityMaster.get_asset', Mock())
    mock.return_value = Bond("test", 'test', )
    mock = replace('gs_quant.entities.entity.Entity.get_data_coordinate', Mock())
    mock.return_value = DataCoordinate("test")
    replace('gs_quant.data.coordinate.DataCoordinate.get_series',
            Mock(side_effect=[pd.Series(benchmark_data), pd.Series(yield_data)]))

    mock = replace('gs_quant.markets.portfolio_manager.PortfolioManager.get_performance_report', Mock())
    mock.return_value = PerformanceReport()

    expected = pd.Series(timeseries)
    with DataContext(dt.date(2020, 1, 1), dt.date(2019, 1, 2)):
        returned = mp.portfolio_jensen_alpha_bear("test", "test", 4)
        assert np.allclose(expected.dropna(), returned.dropna(), atol=1e-5)
    replace.restore()


def test_information_ratio():
    replace = Replacer()
    benchmark_data = {
        pd.Timestamp('2020-01-01'): 6,
        pd.Timestamp('2020-01-02'): 5,
        pd.Timestamp('2020-01-03'): 7,
        pd.Timestamp('2020-01-04'): 9
    }

    data = {
        'pnl': [
            .02,
            .02,
            .01,
            .02

        ],
        'date': [
            '2020-01-01',
            '2020-01-02',
            '2020-01-03',
            '2020-01-04'
        ]
    }

    yield_data = {
        pd.Timestamp('2020-01-01'): .01,
        pd.Timestamp('2020-01-02'): .02,
        pd.Timestamp('2020-01-03'): .025,
        pd.Timestamp('2020-01-04'): .03
    }

    timeseries = {
        pd.Timestamp('2020-01-02 00:00:00'): 0.748532,
        pd.Timestamp('2020-01-03 00:00:00'): -1.583948,
        pd.Timestamp('2020-01-04 00:00:00'): -1.065513
    }

    mock = replace('gs_quant.markets.report.PerformanceReport.get_aum', Mock())
    mock.return_value = aum_data
    mock = replace('gs_quant.markets.report.PerformanceReport.get_pnl', Mock())
    mock.return_value = pd.DataFrame(data)
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport()

    mock = replace('gs_quant.markets.securities.SecurityMaster.get_asset', Mock())
    mock.return_value = Bond("test", 'test', )
    mock = replace('gs_quant.entities.entity.Entity.get_data_coordinate', Mock())
    mock.return_value = DataCoordinate("test")
    replace('gs_quant.data.coordinate.DataCoordinate.get_series',
            Mock(side_effect=[pd.Series(benchmark_data), pd.Series(yield_data)]))

    mock = replace('gs_quant.markets.portfolio_manager.PortfolioManager.get_performance_report', Mock())
    mock.return_value = PerformanceReport()

    expected = pd.Series(timeseries)
    with DataContext(dt.date(2020, 1, 1), dt.date(2019, 1, 2)):
        returned = mp.portfolio_information_ratio("test", "test")
        assert np.allclose(expected.dropna(), returned.dropna(), atol=1e-5)
    replace.restore()


def test_information_ratio_bull():
    replace = Replacer()
    benchmark_data = {
        pd.Timestamp('2020-01-01'): 6,
        pd.Timestamp('2020-01-02'): 5,
        pd.Timestamp('2020-01-03'): 7,
        pd.Timestamp('2020-01-04'): 9
    }

    data = {
        'pnl': [
            .02,
            .02,
            .01,
            .02

        ],
        'date': [
            '2020-01-01',
            '2020-01-02',
            '2020-01-03',
            '2020-01-04'
        ]
    }

    yield_data = {
        pd.Timestamp('2020-01-01'): .01,
        pd.Timestamp('2020-01-02'): .02,
        pd.Timestamp('2020-01-03'): .025,
        pd.Timestamp('2020-01-04'): .03
    }

    timeseries = {
        pd.Timestamp('2020-01-03 00:00:00'): -6.11050,
        pd.Timestamp('2020-01-04 00:00:00'): -4.11050
    }

    mock = replace('gs_quant.markets.report.PerformanceReport.get_aum', Mock())
    mock.return_value = aum_data
    mock = replace('gs_quant.markets.report.PerformanceReport.get_pnl', Mock())
    mock.return_value = pd.DataFrame(data)
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport()

    mock = replace('gs_quant.markets.securities.SecurityMaster.get_asset', Mock())
    mock.return_value = Bond("test", 'test', )
    mock = replace('gs_quant.entities.entity.Entity.get_data_coordinate', Mock())
    mock.return_value = DataCoordinate("test")
    replace('gs_quant.data.coordinate.DataCoordinate.get_series',
            Mock(side_effect=[pd.Series(benchmark_data), pd.Series(yield_data)]))

    mock = replace('gs_quant.markets.portfolio_manager.PortfolioManager.get_performance_report', Mock())
    mock.return_value = PerformanceReport()

    expected = pd.Series(timeseries)
    with DataContext(dt.date(2020, 1, 1), dt.date(2019, 1, 2)):
        returned = mp.portfolio_information_ratio_bull("test", "test")
        assert np.allclose(expected.dropna(), returned.dropna(), atol=1e-5)
    replace.restore()


def test_information_ratio_bear():
    replace = Replacer()
    benchmark_data = {
        pd.Timestamp('2020-01-01'): 6,
        pd.Timestamp('2020-01-02'): 5,
        pd.Timestamp('2020-01-03'): 4,
        pd.Timestamp('2020-01-04'): 9
    }

    data = {
        'pnl': [
            .02,
            .02,
            .01,
            .02

        ],
        'date': [
            '2020-01-01',
            '2020-01-02',
            '2020-01-03',
            '2020-01-04'
        ]
    }

    yield_data = {
        pd.Timestamp('2020-01-01'): .01,
        pd.Timestamp('2020-01-02'): .02,
        pd.Timestamp('2020-01-03'): .025,
        pd.Timestamp('2020-01-04'): .03
    }

    timeseries = {
        pd.Timestamp('2020-01-02 00:00:00'): 20.36364,
        pd.Timestamp('2020-01-03 00:00:00'): 22.36364
    }

    mock = replace('gs_quant.markets.report.PerformanceReport.get_aum', Mock())
    mock.return_value = aum_data
    mock = replace('gs_quant.markets.report.PerformanceReport.get_pnl', Mock())
    mock.return_value = pd.DataFrame(data)
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport()

    mock = replace('gs_quant.markets.securities.SecurityMaster.get_asset', Mock())
    mock.return_value = Bond("test", 'test', )
    mock = replace('gs_quant.entities.entity.Entity.get_data_coordinate', Mock())
    mock.return_value = DataCoordinate("test")
    replace('gs_quant.data.coordinate.DataCoordinate.get_series',
            Mock(side_effect=[pd.Series(benchmark_data), pd.Series(yield_data)]))

    mock = replace('gs_quant.markets.portfolio_manager.PortfolioManager.get_performance_report', Mock())
    mock.return_value = PerformanceReport()

    expected = pd.Series(timeseries)
    with DataContext(dt.date(2020, 1, 1), dt.date(2019, 1, 2)):
        returned = mp.portfolio_information_ratio_bear("test", "test")
        assert np.allclose(expected.dropna(), returned.dropna(), atol=1e-5)
    replace.restore()


def test_modigliani_ratio():
    replace = Replacer()
    benchmark_data = {
        pd.Timestamp('2020-01-01'): 1,
        pd.Timestamp('2020-01-02'): 1.03,
        pd.Timestamp('2020-01-03'): 1.04,
        pd.Timestamp('2020-01-04'): .96,
        pd.Timestamp('2020-01-05'): 1.01,
        pd.Timestamp('2020-01-06'): 1.06,
        pd.Timestamp('2020-01-07'): 1.04
    }

    data = {
        'pnl': [
            .02,
            .02,
            -.01,
            -.002,
            .003,
            .01,
            .002,

        ],
        'date': [
            '2020-01-01',
            '2020-01-02',
            '2020-01-03',
            '2020-01-04',
            '2020-01-05',
            '2020-01-06',
            '2020-01-07'
        ]
    }

    yield_data = {
        pd.Timestamp('2020-01-01'): .01,
        pd.Timestamp('2020-01-02'): .02,
        pd.Timestamp('2020-01-03'): .025,
        pd.Timestamp('2020-01-04'): .03,
        pd.Timestamp('2020-01-05'): .028,
        pd.Timestamp('2020-01-06'): .031,
        pd.Timestamp('2020-01-07'): .032
    }

    timeseries = {
        pd.Timestamp('2020-01-05 00:00:00'): 0.31288,
        pd.Timestamp('2020-01-06 00:00:00'): 0.20278
    }

    mock = replace('gs_quant.markets.report.PerformanceReport.get_aum', Mock())
    mock.return_value = aum_data
    mock = replace('gs_quant.markets.report.PerformanceReport.get_pnl', Mock())
    mock.return_value = pd.DataFrame(data)
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport()

    mock = replace('gs_quant.markets.securities.SecurityMaster.get_asset', Mock())
    mock.return_value = Bond("test", 'test', )
    mock = replace('gs_quant.entities.entity.Entity.get_data_coordinate', Mock())
    mock.return_value = DataCoordinate("test")
    mock = replace('gs_quant.data.coordinate.DataCoordinate.get_series', Mock(side_effect=[pd.Series(benchmark_data),
                                                                                           pd.Series(yield_data),
                                                                                           pd.Series(yield_data),
                                                                                           pd.Series(yield_data),
                                                                                           pd.Series(yield_data)]))
    mock.return_value = pd.Series(benchmark_data)

    mock = replace('gs_quant.markets.portfolio_manager.PortfolioManager.get_performance_report', Mock())
    mock.return_value = PerformanceReport()

    expected = pd.Series(timeseries)
    with DataContext(dt.date(2020, 1, 1), dt.date(2019, 1, 2)):
        returned = mp.portfolio_modigliani_ratio("test", "test", "test", 4)
        assert np.allclose(expected.dropna(), returned.dropna(), atol=1e-5)
    replace.restore()


def test_treynor_measure():
    replace = Replacer()
    data = {
        'pnl': [
            .02,
            .02,
            .01,
            .002,
            .003,
            .01,
            .002,

        ],
        'date': [
            '2020-01-01',
            '2020-01-02',
            '2020-01-03',
            '2020-01-04',
            '2020-01-05',
            '2020-01-06',
            '2020-01-07'
        ]
    }

    yield_data = {
        pd.Timestamp('2020-01-01'): .01,
        pd.Timestamp('2020-01-02'): .02,
        pd.Timestamp('2020-01-03'): .025,
        pd.Timestamp('2020-01-04'): .03,
        pd.Timestamp('2020-01-05'): .028,
        pd.Timestamp('2020-01-06'): .031,
        pd.Timestamp('2020-01-07'): .032
    }

    timeseries = {
        pd.Timestamp('2020-01-04 00:00:00'): -0.01426,
    }

    benchmark_data = {
        pd.Timestamp('2020-01-01'): 6,
        pd.Timestamp('2020-01-02'): 5,
        pd.Timestamp('2020-01-03'): 4,
        pd.Timestamp('2020-01-04'): 9
    }

    mock = replace('gs_quant.markets.report.PerformanceReport.get_aum', Mock())
    mock.return_value = aum_data

    mock = replace('gs_quant.markets.report.PerformanceReport.get_pnl', Mock())
    mock.return_value = pd.DataFrame(data)
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport()

    mock = replace('gs_quant.markets.securities.SecurityMaster.get_asset', Mock())
    mock.return_value = Bond("test", 'test', )
    mock = replace('gs_quant.entities.entity.Entity.get_data_coordinate', Mock())
    mock.return_value = DataCoordinate("test")
    replace('gs_quant.data.coordinate.DataCoordinate.get_series',
            Mock(side_effect=[pd.Series(benchmark_data), pd.Series(yield_data)]))

    mock = replace('gs_quant.markets.portfolio_manager.PortfolioManager.get_performance_report', Mock())
    mock.return_value = PerformanceReport()

    expected = pd.Series(timeseries)
    with DataContext(dt.date(2020, 1, 1), dt.date(2019, 1, 2)):
        returned = mp.portfolio_treynor_measure("test", 'test', 'test')
        assert np.allclose(expected.dropna(), returned.dropna(), atol=1e-5)
    replace.restore()


def test_alpha():
    replace = Replacer()
    benchmark_data = {
        pd.Timestamp('2020-01-01'): 1,
        pd.Timestamp('2020-01-02'): 1.03,
        pd.Timestamp('2020-01-03'): 1.04,
        pd.Timestamp('2020-01-04'): .96,
        pd.Timestamp('2020-01-05'): 1.01,
        pd.Timestamp('2020-01-06'): 1.06,
        pd.Timestamp('2020-01-07'): 1.04
    }

    data = {
        'pnl': [
            .02,
            .02,
            .01,
            .002,
            .003,
            .01,
            .002,

        ],
        'date': [
            '2020-01-01',
            '2020-01-02',
            '2020-01-03',
            '2020-01-04',
            '2020-01-05',
            '2020-01-06',
            '2020-01-07'
        ]
    }

    yield_data = {
        pd.Timestamp('2020-01-01'): .01,
        pd.Timestamp('2020-01-02'): .02,
        pd.Timestamp('2020-01-03'): .025,
        pd.Timestamp('2020-01-04'): .03,
        pd.Timestamp('2020-01-05'): .028,
        pd.Timestamp('2020-01-06'): .031,
        pd.Timestamp('2020-01-07'): .032
    }

    timeseries = {
        pd.Timestamp('2020-01-05 00:00:00'): -1.61319,
        pd.Timestamp('2020-01-06 00:00:00'): -3.73679,
        pd.Timestamp('2020-01-07 00:00:00'): -1.38878
    }

    aum_data = {
        '2020-01-01': 1.00,
        '2020-01-02': .95,
        '2020-01-03': .9,
        '2020-01-04': 1.03,
        '2020-01-05': 1.065,
        '2020-01-06': 1.08,
        '2020-01-07': 1.072
    }

    mock = replace('gs_quant.markets.report.PerformanceReport.get_aum', Mock())
    mock.return_value = aum_data
    mock = replace('gs_quant.markets.report.PerformanceReport.get_pnl', Mock())
    mock.return_value = pd.DataFrame(data)
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport()

    mock = replace('gs_quant.markets.securities.SecurityMaster.get_asset', Mock())
    mock.return_value = Bond("test", 'test', )
    mock = replace('gs_quant.entities.entity.Entity.get_data_coordinate', Mock())
    mock.return_value = DataCoordinate("test")
    replace('gs_quant.data.coordinate.DataCoordinate.get_series', Mock(side_effect=[pd.Series(benchmark_data),
                                                                                    pd.Series(yield_data)]))

    mock = replace('gs_quant.markets.portfolio_manager.PortfolioManager.get_performance_report', Mock())
    mock.return_value = PerformanceReport()

    expected = pd.Series(timeseries)
    with DataContext(dt.date(2020, 1, 1), dt.date(2019, 1, 2)):
        returned = mp.portfolio_alpha("test", "test", 4)
        assert np.allclose(expected.dropna(), returned.dropna(), atol=1e-6)
    replace.restore()


def test_beta():
    replace = Replacer()
    benchmark_data = {
        pd.Timestamp('2020-01-01'): 1,
        pd.Timestamp('2020-01-02'): 1.03,
        pd.Timestamp('2020-01-03'): 1.04,
        pd.Timestamp('2020-01-04'): .96,
        pd.Timestamp('2020-01-05'): 1.01,
        pd.Timestamp('2020-01-06'): 1.06,
        pd.Timestamp('2020-01-07'): 1.04
    }

    data = {
        'pnl': [
            .02,
            .02,
            .01,
            .002,
            .003,
            .01,
            .002,

        ],
        'date': [
            '2020-01-01',
            '2020-01-02',
            '2020-01-03',
            '2020-01-04',
            '2020-01-05',
            '2020-01-06',
            '2020-01-07'
        ]
    }

    yield_data = {
        pd.Timestamp('2020-01-01'): .01,
        pd.Timestamp('2020-01-02'): .02,
        pd.Timestamp('2020-01-03'): .025,
        pd.Timestamp('2020-01-04'): .03,
        pd.Timestamp('2020-01-05'): .028,
        pd.Timestamp('2020-01-06'): .031,
        pd.Timestamp('2020-01-07'): .032
    }

    timeseries = {
        pd.Timestamp('2020-01-05 00:00:00'): 0.00118,
        pd.Timestamp('2020-01-06 00:00:00'): 0.00070,
        pd.Timestamp('2020-01-07 00:00:00'): 0.00106
    }

    mock = replace('gs_quant.markets.report.PerformanceReport.get_aum', Mock())
    mock.return_value = aum_data
    mock = replace('gs_quant.markets.report.PerformanceReport.get_pnl', Mock())
    mock.return_value = pd.DataFrame(data)
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport()

    mock = replace('gs_quant.markets.securities.SecurityMaster.get_asset', Mock())
    mock.return_value = Bond("test", 'test', )
    mock = replace('gs_quant.entities.entity.Entity.get_data_coordinate', Mock())
    mock.return_value = DataCoordinate("test")
    replace('gs_quant.data.coordinate.DataCoordinate.get_series', Mock(side_effect=[pd.Series(benchmark_data),
                                                                                    pd.Series(yield_data)]))

    mock = replace('gs_quant.markets.portfolio_manager.PortfolioManager.get_performance_report', Mock())
    mock.return_value = PerformanceReport()

    expected = pd.Series(timeseries)
    with DataContext(dt.date(2020, 1, 1), dt.date(2019, 1, 2)):
        returned = mp.portfolio_beta("test", "test", 4)
        assert np.allclose(expected.dropna(), returned.dropna(), atol=1e-5)
    replace.restore()


def test_correlation():
    replace = Replacer()
    benchmark_data = {
        pd.Timestamp('2020-01-01'): 1,
        pd.Timestamp('2020-01-02'): 1.03,
        pd.Timestamp('2020-01-03'): 1.04,
        pd.Timestamp('2020-01-04'): .96,
        pd.Timestamp('2020-01-05'): 1.01,
        pd.Timestamp('2020-01-06'): 1.06,
        pd.Timestamp('2020-01-07'): 1.04
    }

    data = {
        'pnl': [
            .02,
            .02,
            .01,
            .002,
            .003,
            .01,
            .002,

        ],
        'date': [
            '2020-01-01',
            '2020-01-02',
            '2020-01-03',
            '2020-01-04',
            '2020-01-05',
            '2020-01-06',
            '2020-01-07'
        ]
    }

    yield_data = {
        pd.Timestamp('2020-01-01'): .01,
        pd.Timestamp('2020-01-02'): .02,
        pd.Timestamp('2020-01-03'): .025,
        pd.Timestamp('2020-01-04'): .03,
        pd.Timestamp('2020-01-05'): .028,
        pd.Timestamp('2020-01-06'): .031,
        pd.Timestamp('2020-01-07'): .032
    }

    timeseries = {
        pd.Timestamp('2020-01-06 00:00:00'): 0.21846,
        pd.Timestamp('2020-01-07 00:00:00'): 0.40573
    }

    mock = replace('gs_quant.markets.report.PerformanceReport.get_aum', Mock())
    mock.return_value = aum_data
    mock = replace('gs_quant.markets.report.PerformanceReport.get_pnl', Mock())
    mock.return_value = pd.DataFrame(data)
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport()

    mock = replace('gs_quant.markets.securities.SecurityMaster.get_asset', Mock())
    mock.return_value = Bond("test", 'test', )
    mock = replace('gs_quant.entities.entity.Entity.get_data_coordinate', Mock())
    mock.return_value = DataCoordinate("test")
    replace('gs_quant.data.coordinate.DataCoordinate.get_series', Mock(side_effect=[pd.Series(benchmark_data),
                                                                                    pd.Series(yield_data)]))

    mock = replace('gs_quant.markets.portfolio_manager.PortfolioManager.get_performance_report', Mock())
    mock.return_value = PerformanceReport()

    expected = pd.Series(timeseries)
    with DataContext(dt.date(2020, 1, 1), dt.date(2019, 1, 2)):
        returned = mp.portfolio_correlation("test", "test", 4)
        assert np.allclose(expected.dropna(), returned.dropna(), atol=1e-5)
    replace.restore()


def test_r_squared():
    replace = Replacer()
    benchmark_data = {
        pd.Timestamp('2020-01-01'): 1,
        pd.Timestamp('2020-01-02'): 1.03,
        pd.Timestamp('2020-01-03'): 1.04,
        pd.Timestamp('2020-01-04'): .96,
        pd.Timestamp('2020-01-05'): 1.01,
        pd.Timestamp('2020-01-06'): 1.06,
        pd.Timestamp('2020-01-07'): 1.04
    }

    data = {
        'pnl': [
            .02,
            .02,
            .01,
            .002,
            .003,
            .01,
            .002,

        ],
        'date': [
            '2020-01-01',
            '2020-01-02',
            '2020-01-03',
            '2020-01-04',
            '2020-01-05',
            '2020-01-06',
            '2020-01-07'
        ]
    }

    yield_data = {
        pd.Timestamp('2020-01-01'): .01,
        pd.Timestamp('2020-01-02'): .02,
        pd.Timestamp('2020-01-03'): .025,
        pd.Timestamp('2020-01-04'): .03,
        pd.Timestamp('2020-01-05'): .028,
        pd.Timestamp('2020-01-06'): .031,
        pd.Timestamp('2020-01-07'): .032
    }

    timeseries = {
        pd.Timestamp('2020-01-05 00:00:00'): 0.04772,
        pd.Timestamp('2020-01-06 00:00:00'): 0.16462
    }

    mock = replace('gs_quant.markets.report.PerformanceReport.get_aum', Mock())
    mock.return_value = aum_data
    mock = replace('gs_quant.markets.report.PerformanceReport.get_pnl', Mock())
    mock.return_value = pd.DataFrame(data)
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport()

    mock = replace('gs_quant.markets.securities.SecurityMaster.get_asset', Mock())
    mock.return_value = Bond("test", 'test', )
    mock = replace('gs_quant.entities.entity.Entity.get_data_coordinate', Mock())
    mock.return_value = DataCoordinate("test")
    replace('gs_quant.data.coordinate.DataCoordinate.get_series', Mock(side_effect=[pd.Series(benchmark_data),
                                                                                    pd.Series(yield_data)]))

    mock = replace('gs_quant.markets.portfolio_manager.PortfolioManager.get_performance_report', Mock())
    mock.return_value = PerformanceReport()

    expected = pd.Series(timeseries)
    with DataContext(dt.date(2020, 1, 1), dt.date(2019, 1, 2)):
        returned = mp.portfolio_r_squared("test", "test", 4)
        assert np.allclose(expected.dropna(), returned.dropna(), atol=1e-5)
    replace.restore()


def test_capture_ratio():
    replace = Replacer()
    benchmark_data = {
        pd.Timestamp('2020-01-01'): 1,
        pd.Timestamp('2020-01-02'): 1.03,
        pd.Timestamp('2020-01-03'): 1.04,
        pd.Timestamp('2020-01-04'): 1.06,
        pd.Timestamp('2020-01-05'): 1.06,
        pd.Timestamp('2020-01-06'): 1.06,
        pd.Timestamp('2020-01-07'): 1.04
    }

    data = {
        'pnl': [
            .02,
            .02,
            .01,
            .002,
            .003,
            .01,
            .002,

        ],
        'date': [
            '2020-01-01',
            '2020-01-02',
            '2020-01-03',
            '2020-01-04',
            '2020-01-05',
            '2020-01-06',
            '2020-01-07'
        ]
    }

    yield_data = {
        pd.Timestamp('2020-01-01'): .01,
        pd.Timestamp('2020-01-02'): .02,
        pd.Timestamp('2020-01-03'): .025,
        pd.Timestamp('2020-01-04'): .03,
        pd.Timestamp('2020-01-05'): .028,
        pd.Timestamp('2020-01-06'): .031,
        pd.Timestamp('2020-01-07'): .032
    }

    timeseries = {
        pd.Timestamp('2020-01-05 00:00:00'): 0.50900,
        pd.Timestamp('2020-01-06 00:00:00'): 0.69110
    }

    mock = replace('gs_quant.markets.report.PerformanceReport.get_aum', Mock())
    mock.return_value = aum_data
    mock = replace('gs_quant.markets.report.PerformanceReport.get_pnl', Mock())
    mock.return_value = pd.DataFrame(data)
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport()

    mock = replace('gs_quant.markets.securities.SecurityMaster.get_asset', Mock())
    mock.return_value = Bond("test", 'test', )
    mock = replace('gs_quant.entities.entity.Entity.get_data_coordinate', Mock())
    mock.return_value = DataCoordinate("test")
    replace('gs_quant.data.coordinate.DataCoordinate.get_series', Mock(side_effect=[pd.Series(benchmark_data),
                                                                                    pd.Series(yield_data)]))

    mock = replace('gs_quant.markets.portfolio_manager.PortfolioManager.get_performance_report', Mock())
    mock.return_value = PerformanceReport()

    expected = pd.Series(timeseries)
    with DataContext(dt.date(2020, 1, 1), dt.date(2019, 1, 2)):
        returned = mp.portfolio_capture_ratio("test", "test", 4)
        assert np.allclose(expected.dropna(), returned.dropna(), atol=1e-5)
    replace.restore()


def test_custom_aum():
    data = {
        'aum': [
            101,
            102,
            103
        ],
        'date': [
            '2020-01-01',
            '2020-01-02',
            '2020-01-03'
        ]
    }
    idx = pd.date_range('2020-01-01', freq='D', periods=3)
    df = MarketDataResponseFrame(data=data, index=idx)
    df.dataset_ids = ('AUM',)
    replace = Replacer()

    # mock GsPortfolioApi.get_reports()
    mock = replace('gs_quant.api.gs.portfolios.GsPortfolioApi.get_custom_aum', Mock())
    mock.return_value = df
    with DataContext(dt.date(2020, 1, 1), dt.date(2019, 1, 3)):
        actual = mp.aum('MP1')
        assert actual.index.equals(idx)
        assert all(actual.values == data['aum'])
    replace.restore()


if __name__ == '__main__':
    pytest.main(args=[__file__])
