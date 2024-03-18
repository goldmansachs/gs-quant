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
import datetime
import math

import pandas
import pandas as pd
import pytest
from testfixtures import Replacer
from testfixtures.mock import Mock

import gs_quant.timeseries.measures_reports as mr
from gs_quant.api.gs.assets import GsTemporalXRef
from gs_quant.api.gs.data import MarketDataResponseFrame
from gs_quant.data.core import DataContext
from gs_quant.errors import MqValueError
from gs_quant.markets.report import PerformanceReport, ThematicReport, CustomAUMDataPoint
from gs_quant.markets.securities import Stock
from gs_quant.models.risk_model import FactorRiskModel as Factor_Risk_Model
from gs_quant.target.common import ReportParameters, XRef
from gs_quant.target.portfolios import RiskAumSource
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


factor_exposure_data = [
    {
        'date': '2024-03-14',
        'reportId': 'report_id',
        'factor': 'Factor_1',
        'factorCategory': 'Style',
        'pnl': 19.23,
        'exposure': 100,
        'proportionOfRisk': 1
    },
    {
        'date': '2024-03-14',
        'reportId': 'report_id',
        'factor': 'Factor_2',
        'factorCategory': 'Style',
        'pnl': 14.24,
        'exposure': 100,
        'proportionOfRisk': 2
    },
    {
        'date': '2024-03-14',
        'reportId': 'report_id',
        'factor': 'Factor_3',
        'factorCategory': 'Style',
        'pnl': 21.25,
        'exposure': 100,
        'proportionOfRisk': 3
    }
]


factor_return_data = [
    {
        "date": "2024-03-13",
        "factor": "Factor_1",
        "return": 2
    },
    {
        "date": "2024-03-13",
        "factor": "Factor_2",
        "return": 3
    },
    {
        "date": "2024-03-13",
        "factor": "Factor_3",
        "return": 2
    },
    {
        "date": "2024-03-14",
        "factor": "Factor_1",
        "return": 2
    },
    {
        "date": "2024-03-14",
        "factor": "Factor_2",
        "return": 3
    },
    {
        "date": "2024-03-14",
        "factor": "Factor_3",
        "return": 2
    },
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

constituents_data_l_s = {
    'assetId': [
        "MA1",
        "MA1",
        "MA1",
        "MA2",
        "MA2",
        "MA2"
    ],
    'quantity': [
        -1.,
        -2.,
        -3.,
        1.,
        2.,
        3.
    ],
    'netExposure': [
        -1.,
        -2.,
        -3.,
        1.,
        2.,
        3.
    ],
    'pnl': [
        0.,
        -1.,
        -1.,
        0.,
        1.,
        1.
    ],
    'date': [
        '2020-01-02',
        '2020-01-03',
        '2020-01-04',
        '2020-01-02',
        '2020-01-03',
        '2020-01-04'
    ]
}

pnl_data_l_s = {
    'quantity': [
        -1.,
        -2.,
        -3.,
        -1.,
        -2.,
        -3.,
        1.,
        2.,
        3.,
        1.,
        2.,
        3.
    ],
    'pnl': [
        0.,
        -1.,
        -1.,
        0.,
        -1.,
        -1.,
        0.,
        1.,
        1.,
        0.,
        1.,
        1.
    ],
    'date': [
        '2020-01-02',
        '2020-01-03',
        '2020-01-04',
        '2020-01-02',
        '2020-01-03',
        '2020-01-04',
        '2020-01-02',
        '2020-01-03',
        '2020-01-04',
        '2020-01-02',
        '2020-01-03',
        '2020-01-04'
    ]
}

constituents_data = {
    'netExposure': [
        1.,
        2.,
        3.
    ],
    'assetId': [
        "MA",
        "MA",
        "MA"
    ],
    'quantity': [
        1.,
        1.,
        1.
    ],
    'pnl': [
        0.,
        1.,
        1.
    ],
    'date': [
        '2020-01-02',
        '2020-01-03',
        '2020-01-04'
    ]
}

constituents_data_s = {
    'netExposure': [
        -1.,
        -2.,
        -3.
    ],
    'assetId': [
        "MA",
        "MA",
        "MA"
    ],
    'quantity': [
        -1.,
        -1.,
        -1.
    ],
    'pnl': [
        0.,
        1.,
        1.
    ],
    'date': [
        '2020-01-02',
        '2020-01-03',
        '2020-01-04'
    ]
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


def compute_geometric_aggregation_calculations(aum: dict, pnl: dict, dates: list):
    daily_returns = [0]
    for i in range(2, len(dates)):
        daily_returns.append(pnl[dates[i]] / aum[dates[i - 1]])

    expected_values = [daily_returns[0]]
    for i in range(1, len(daily_returns)):
        expected_values.append((1 + expected_values[i - 1]) * (1 + daily_returns[i]) - 1)

    return [v * 100 for v in expected_values]


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


def test_factor_exposure():
    replace = Replacer()

    # mock getting risk model entity()
    mock = replace('gs_quant.api.gs.risk_models.GsRiskModelApi.get_risk_model', Mock())
    mock.return_value = risk_model

    mock = replace('gs_quant.api.gs.reports.GsReportApi.get_report', Mock())
    mock.return_value = factor_risk_report

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

    with DataContext(datetime.date(2020, 11, 23), datetime.date(2020, 11, 25)):
        actual = mr.factor_exposure('report_id', 'Factor Name')
        assert all(actual.values == [-11.23, -11.24, -11.25])

    with pytest.raises(MqValueError):
        mr.factor_exposure('report_id', 'Wrong Factor Name')
    replace.restore()


def test_factor_exposure_percent():
    replace = Replacer()

    # mock getting risk model entity()
    mock = replace('gs_quant.api.gs.risk_models.GsRiskModelApi.get_risk_model', Mock())
    mock.return_value = risk_model

    mock = replace('gs_quant.api.gs.reports.GsReportApi.get_report', Mock())
    mock.return_value = factor_risk_report

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

    # mock getting performance report
    mock = replace('gs_quant.markets.portfolio_manager.PortfolioManager.get_performance_report', Mock())
    mock.return_value = ppa_report

    # mock getting aum source
    mock = replace('gs_quant.markets.report.PerformanceReport.get_aum_source', Mock())
    mock.return_value = RiskAumSource.Custom_AUM

    with DataContext(datetime.date(2020, 11, 23), datetime.date(2020, 11, 25)):
        # mock getting aum
        mock = replace('gs_quant.markets.report.PerformanceReport.get_custom_aum', Mock())
        mock.return_value = [CustomAUMDataPoint(date=datetime.date(2020, 11, 23), aum=2),
                             CustomAUMDataPoint(date=datetime.date(2020, 11, 24), aum=2),
                             CustomAUMDataPoint(date=datetime.date(2020, 11, 25), aum=2)]
        actual = mr.factor_exposure('report_id', 'Factor Name', 'Percent')
        assert all(actual.values == [-11.23 * 50, -11.24 * 50, -11.25 * 50])

    with pytest.raises(MqValueError):
        # mock getting aum with missing data
        mock = replace('gs_quant.markets.report.PerformanceReport.get_custom_aum', Mock())
        mock.return_value = [CustomAUMDataPoint(date=datetime.date(2020, 11, 23), aum=2),
                             CustomAUMDataPoint(date=datetime.date(2020, 11, 25), aum=2)]
        mr.factor_exposure('report_id', 'Factor Name', 'Percent')

    replace.restore()


def test_factor_pnl():
    replace = Replacer()

    # mock getting risk model entity()
    mock = replace('gs_quant.api.gs.risk_models.GsRiskModelApi.get_risk_model', Mock())
    mock.return_value = risk_model

    mock = replace('gs_quant.api.gs.reports.GsReportApi.get_report', Mock())
    mock.return_value = factor_risk_report

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

    with DataContext(datetime.date(2020, 11, 23), datetime.date(2020, 11, 25)):
        # mock getting report factor data
        mock = replace('gs_quant.api.gs.reports.GsReportApi.get_factor_risk_report_results', Mock())
        mock.return_value = factor_data

        actual = mr.factor_pnl('report_id', 'Factor Name')
        assert all(actual.values == [11.23, 11.24, 11.25])

    with DataContext(datetime.date(2020, 11, 22), datetime.date(2020, 11, 25)):
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

        actual = mr.factor_pnl('report_id', 'Factor Name')
        assert all(actual.values == [0.0, 11.23, 11.24, 11.25])

    with pytest.raises(MqValueError):
        mr.factor_pnl('report_id', 'Wrong Factor Name')
    replace.restore()


def test_factor_pnl_percent():
    replace = Replacer()

    aum = {'2020-11-22': 200, '2020-11-23': 400, '2020-11-24': 400, '2020-11-25': 400}

    # mock getting risk model entity()
    mock = replace('gs_quant.api.gs.risk_models.GsRiskModelApi.get_risk_model', Mock())
    mock.return_value = risk_model

    mock = replace('gs_quant.api.gs.reports.GsReportApi.get_report', Mock())
    mock.return_value = factor_risk_report

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

    mock = replace('gs_quant.markets.report.PerformanceReport.get_aum', Mock())
    mock.return_value = aum

    # Each team uses pnl today/aum yesterday
    expected_values = [0, 0, 2.8844318, 5.7471343]

    with DataContext(datetime.date(2020, 11, 23), datetime.date(2020, 11, 25)):
        # mock getting aum source
        mock = replace('gs_quant.markets.report.PerformanceReport.get_aum_source', Mock())
        mock.return_value = RiskAumSource.Long

        # mock getting performance report
        mock = replace('gs_quant.markets.portfolio_manager.PortfolioManager.get_performance_report', Mock())
        mock.return_value = PerformanceReport(id='ID')

        # mock getting aum
        mock = replace('gs_quant.markets.report.PerformanceReport.get_long_exposure', Mock())
        mock.return_value = pandas.DataFrame.from_dict({'date': aum.keys(), 'longExposure': aum.values()})
        actual = mr.factor_pnl('report_id', 'Factor Name', 'Percent')
        assert all([a == pytest.approx(e) for a, e in zip(actual.values, expected_values)])

    with DataContext(datetime.date(2020, 11, 23), datetime.date(2020, 11, 25)):
        # mock getting aum source
        mock = replace('gs_quant.markets.report.PerformanceReport.get_aum_source', Mock())
        mock.return_value = RiskAumSource.Short

        # mock getting performance report
        mock = replace('gs_quant.markets.portfolio_manager.PortfolioManager.get_performance_report', Mock())
        mock.return_value = PerformanceReport(id='ID')

        # mock getting aum
        mock = replace('gs_quant.markets.report.PerformanceReport.get_short_exposure', Mock())
        mock.return_value = pandas.DataFrame.from_dict({'date': aum.keys(), 'shortExposure': aum.values()})
        actual = mr.factor_pnl('report_id', 'Factor Name', 'Percent')
        assert all([a == pytest.approx(e) for a, e in zip(actual.values, expected_values)])

    with DataContext(datetime.date(2020, 11, 23), datetime.date(2020, 11, 25)):
        # mock getting aum source
        mock = replace('gs_quant.markets.report.PerformanceReport.get_aum_source', Mock())
        mock.return_value = RiskAumSource.Gross

        # mock getting performance report
        mock = replace('gs_quant.markets.portfolio_manager.PortfolioManager.get_performance_report', Mock())
        mock.return_value = PerformanceReport(id='ID')

        # mock getting aum
        mock = replace('gs_quant.markets.report.PerformanceReport.get_gross_exposure', Mock())
        mock.return_value = pandas.DataFrame.from_dict({'date': aum.keys(), 'grossExposure': aum.values()})
        actual = mr.factor_pnl('report_id', 'Factor Name', 'Percent')
        assert all([a == pytest.approx(e) for a, e in zip(actual.values, expected_values)])

    with DataContext(datetime.date(2020, 11, 23), datetime.date(2020, 11, 25)):
        # mock getting aum source
        mock = replace('gs_quant.markets.report.PerformanceReport.get_aum_source', Mock())
        mock.return_value = RiskAumSource.Net

        # mock getting performance report
        mock = replace('gs_quant.markets.portfolio_manager.PortfolioManager.get_performance_report', Mock())
        mock.return_value = PerformanceReport(id='ID')

        # mock getting aum
        mock = replace('gs_quant.markets.report.PerformanceReport.get_net_exposure', Mock())
        mock.return_value = pandas.DataFrame.from_dict({'date': aum.keys(), 'netExposure': aum.values()})
        actual = mr.factor_pnl('report_id', 'Factor Name', 'Percent')
        assert all([a == pytest.approx(e) for a, e in zip(actual.values, expected_values)])

    replace.restore()


def test_asset_factor_pnl_percent():
    replace = Replacer()

    # mock getting risk model entity()
    mock = replace('gs_quant.api.gs.risk_models.GsRiskModelApi.get_risk_model', Mock())
    mock.return_value = risk_model

    mock = replace('gs_quant.api.gs.reports.GsReportApi.get_report', Mock())
    mock.return_value = asset_factor_risk_report

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

    with pytest.raises(MqValueError):
        mr.factor_pnl('report_id', 'Factor Name', 'Percent')

    replace.restore()


def test_factor_proportion_of_risk():
    replace = Replacer()

    # mock getting risk model entity()
    mock = replace('gs_quant.api.gs.risk_models.GsRiskModelApi.get_risk_model', Mock())
    mock.return_value = risk_model

    mock = replace('gs_quant.api.gs.reports.GsReportApi.get_report', Mock())
    mock.return_value = factor_risk_report

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

    with DataContext(datetime.date(2020, 11, 23), datetime.date(2020, 11, 25)):
        actual = mr.factor_proportion_of_risk('report_id', 'Factor Name')
        assert all(actual.values == [1, 2, 3])

    with pytest.raises(MqValueError):
        mr.factor_proportion_of_risk('report_id', 'Wrong Factor Name')
    replace.restore()


def test_get_factor_data():
    replace = Replacer()

    mock = replace('gs_quant.api.gs.reports.GsReportApi.get_report', Mock())
    mock.return_value = ppa_report

    with pytest.raises(MqValueError):
        mr.factor_proportion_of_risk('report_id', 'Factor Name')
    replace.restore()


def test_aggregate_factor_support():
    replace = Replacer()

    # mock getting risk model entity()
    mock = replace('gs_quant.api.gs.risk_models.GsRiskModelApi.get_risk_model', Mock())
    mock.return_value = risk_model

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

    with DataContext(datetime.date(2020, 11, 23), datetime.date(2020, 11, 25)):
        actual = mr.factor_proportion_of_risk('report_id', 'Factor')
        assert all(actual.values == [1, 2, 3])

    with DataContext(datetime.date(2020, 11, 23), datetime.date(2020, 11, 25)):
        actual = mr.daily_risk('report_id', 'Factor')
        assert all(actual.values == [1, 2, 3])

    with DataContext(datetime.date(2020, 11, 23), datetime.date(2020, 11, 25)):
        actual = mr.annual_risk('report_id', 'Factor')
        assert all(actual.values == [1, 2, 3])

    with pytest.raises(MqValueError):
        mr.daily_risk('report_id', 'Factor Name')

    with pytest.raises(MqValueError):
        mr.annual_risk('report_id', 'Factor Name')
    replace.restore()


def test_normalized_performance():
    idx = pd.date_range('2020-01-02', freq='D', periods=3)
    replace = Replacer()
    expected = {None: pd.Series(data=[1, 2, 3], index=idx,
                                name='normalizedPerformance', dtype='float64'),
                "Long": pd.Series(data=[1, 2, 3], index=idx,
                                  name='normalizedPerformance', dtype='float64')}

    mock = replace('gs_quant.api.gs.portfolios.GsPortfolioApi.get_reports', Mock())
    mock.return_value = [
        Report.from_dict({'id': 'RP1', 'positionSourceType': 'Portfolio', 'positionSourceId': 'MP1',
                          'type': 'Portfolio Performance Analytics',
                          'parameters': {'transactionCostModel': 'FIXED'}})]
    # mock PerformanceReport.get_portfolio_constituents()
    mock = replace('gs_quant.markets.report.PerformanceReport.get_portfolio_constituents', Mock())
    mock.return_value = MarketDataResponseFrame(data=constituents_data)

    # mock PerformanceReport.get()
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport(report_id='RP1',
                                          position_source_type='Portfolio',
                                          position_source_id='MP1',
                                          report_type='Portfolio Performance Analytics',
                                          parameters=ReportParameters(transaction_cost_model='FIXED'))

    for k, v in expected.items():
        with DataContext(datetime.date(2020, 1, 1), datetime.date(2019, 1, 3)):
            actual = mr.normalized_performance('MP1', k)
            assert all(actual.values == v.values)
    replace.restore()


def test_normalized_performance_short():
    idx = pd.date_range('2020-01-02', freq='D', periods=3)
    replace = Replacer()
    expected = {"Short": pd.Series(data=[1, 1 / 2, 1 / 3], index=idx,
                                   name='normalizedPerformance', dtype='float64'),
                "Long": pd.Series(data=[1, 2, 3], index=idx,
                                  name='normalizedPerformance', dtype='float64'),
                None: pd.Series(data=[1, (2 + 1 / 2) / 2, (3 + 1 / 3) / 2], index=idx,
                                name='normalizedPerformance', dtype='float64')}

    mock = replace('gs_quant.api.gs.portfolios.GsPortfolioApi.get_reports', Mock())
    mock.return_value = [
        Report.from_dict({'id': 'RP1', 'positionSourceType': 'Portfolio', 'positionSourceId': 'MP1',
                          'type': 'Portfolio Performance Analytics',
                          'parameters': {'transactionCostModel': 'FIXED'}})]
    # mock PerformanceReport.get_portfolio_constituents()
    mock = replace('gs_quant.markets.report.PerformanceReport.get_portfolio_constituents', Mock())
    mock.return_value = MarketDataResponseFrame(data=constituents_data_l_s)

    # mock PerformanceReport.get()
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport(report_id='RP1',
                                          position_source_type='Portfolio',
                                          position_source_id='MP1',
                                          report_type='Portfolio Performance Analytics',
                                          parameters=ReportParameters(transaction_cost_model='FIXED'))

    for k, v in expected.items():
        with DataContext(datetime.date(2020, 1, 1), datetime.date(2019, 1, 3)):
            actual = mr.normalized_performance('MP1', k)
            assert all((actual.values - v.values) < 0.01)
    replace.restore()


def test_get_long_pnl():
    idx = pd.date_range('2020-01-02', freq='D', periods=3)
    replace = Replacer()
    expected = pd.Series(data=[0, 2, 2], index=idx, name='longPnl', dtype='float64')

    mock = replace('gs_quant.api.gs.portfolios.GsPortfolioApi.get_reports', Mock())
    mock.return_value = [
        Report.from_dict({'id': 'RP1', 'positionSourceType': 'Portfolio', 'positionSourceId': 'MP1',
                          'type': 'Portfolio Performance Analytics',
                          'parameters': {'transactionCostModel': 'FIXED'}})]
    # mock PerformanceReport.get_portfolio_constituents()
    mock = replace('gs_quant.markets.report.PerformanceReport.get_portfolio_constituents', Mock())
    mock.return_value = MarketDataResponseFrame(data=pnl_data_l_s)

    # mock PerformanceReport.get()
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport(report_id='RP1',
                                          position_source_type='Portfolio',
                                          position_source_id='MP1',
                                          report_type='Portfolio Performance Analytics',
                                          parameters=ReportParameters(transaction_cost_model='FIXED'))

    with DataContext(datetime.date(2020, 1, 1), datetime.date(2019, 1, 3)):
        actual = mr.long_pnl('MP1')
        assert all(actual.values == expected.values)
    replace.restore()


def test_get_short_pnl():
    idx = pd.date_range('2020-01-02', freq='D', periods=3)
    replace = Replacer()
    expected = pd.Series(data=[0, -2, -2], index=idx, name='shortPnl', dtype='float64')

    mock = replace('gs_quant.api.gs.portfolios.GsPortfolioApi.get_reports', Mock())
    mock.return_value = [
        Report.from_dict({'id': 'RP1', 'positionSourceType': 'Portfolio', 'positionSourceId': 'MP1',
                          'type': 'Portfolio Performance Analytics',
                          'parameters': {'transactionCostModel': 'FIXED'}})]
    # mock PerformanceReport.get_portfolio_constituents()
    mock = replace('gs_quant.markets.report.PerformanceReport.get_portfolio_constituents', Mock())
    mock.return_value = MarketDataResponseFrame(data=pnl_data_l_s)

    # mock PerformanceReport.get()
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport(report_id='RP1',
                                          position_source_type='Portfolio',
                                          position_source_id='MP1',
                                          report_type='Portfolio Performance Analytics',
                                          parameters=ReportParameters(transaction_cost_model='FIXED'))

    with DataContext(datetime.date(2020, 1, 1), datetime.date(2019, 1, 3)):
        actual = mr.short_pnl('MP1')
        assert all(actual.values == expected.values)
    replace.restore()


def test_get_short_pnl_empty():
    replace = Replacer()
    expected = pd.Series(dtype=float)

    mock = replace('gs_quant.api.gs.portfolios.GsPortfolioApi.get_reports', Mock())
    mock.return_value = [
        Report.from_dict({'id': 'RP1', 'positionSourceType': 'Portfolio', 'positionSourceId': 'MP1',
                          'type': 'Portfolio Performance Analytics',
                          'parameters': {'transactionCostModel': 'FIXED'}})]
    # mock PerformanceReport.get_portfolio_constituents()
    mock = replace('gs_quant.markets.report.PerformanceReport.get_portfolio_constituents', Mock())
    mock.return_value = MarketDataResponseFrame(data=constituents_data)

    # mock PerformanceReport.get()
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport(report_id='RP1',
                                          position_source_type='Portfolio',
                                          position_source_id='MP1',
                                          report_type='Portfolio Performance Analytics',
                                          parameters=ReportParameters(transaction_cost_model='FIXED'))

    with DataContext(datetime.date(2020, 1, 1), datetime.date(2019, 1, 3)):
        actual = mr.short_pnl('MP1')
        assert all(actual.values == expected.values)
    replace.restore()


def test_get_long_pnl_empty():
    replace = Replacer()
    expected = pd.Series(dtype=float)

    mock = replace('gs_quant.api.gs.portfolios.GsPortfolioApi.get_reports', Mock())
    mock.return_value = [
        Report.from_dict({'id': 'RP1', 'positionSourceType': 'Portfolio', 'positionSourceId': 'MP1',
                          'type': 'Portfolio Performance Analytics',
                          'parameters': {'transactionCostModel': 'FIXED'}})]
    # mock PerformanceReport.get_portfolio_constituents()
    mock = replace('gs_quant.markets.report.PerformanceReport.get_portfolio_constituents', Mock())
    mock.return_value = MarketDataResponseFrame(data=constituents_data_s)

    # mock PerformanceReport.get()
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport(report_id='RP1',
                                          position_source_type='Portfolio',
                                          position_source_id='MP1',
                                          report_type='Portfolio Performance Analytics',
                                          parameters=ReportParameters(transaction_cost_model='FIXED'))

    with DataContext(datetime.date(2020, 1, 1), datetime.date(2019, 1, 3)):
        actual = mr.long_pnl('MP1')
        assert all(actual.values == expected.values)
    replace.restore()


def test_thematic_exposure():
    replace = Replacer()

    # mock getting PTA report
    mock = replace('gs_quant.markets.report.ThematicReport.get', Mock())
    mock.return_value = ThematicReport(id='report_id')

    # mock getting thematic exposure
    mock = replace('gs_quant.markets.report.ThematicReport.get_thematic_exposure', Mock())
    mock.return_value = pd.DataFrame(thematic_data)

    # mock getting asset
    mock = Stock('MAA0NE9QX2ABETG6', 'Test Asset')
    xrefs = replace('gs_quant.timeseries.measures.GsAssetApi.get_asset_xrefs', Mock())
    xrefs.return_value = [
        GsTemporalXRef(datetime.date(2019, 1, 1),
                       datetime.date(2952, 12, 31),
                       XRef(ticker='basket_ticker', ))
    ]
    replace('gs_quant.markets.securities.SecurityMaster.get_asset', Mock()).return_value = mock

    with DataContext(datetime.date(2020, 7, 12), datetime.date(2020, 7, 15)):
        actual = mr.thematic_exposure('report_id', 'basket_ticker')
        assert all(actual.values == [2, 2, 2, 2])

    replace.restore()


def test_thematic_beta():
    replace = Replacer()

    # mock getting PTA report
    mock = replace('gs_quant.markets.report.ThematicReport.get', Mock())
    mock.return_value = ThematicReport(id='report_id')

    # mock getting thematic exposure
    mock = replace('gs_quant.markets.report.ThematicReport.get_thematic_betas', Mock())
    mock.return_value = pd.DataFrame(thematic_data)

    # mock getting asset
    mock = Stock('MAA0NE9QX2ABETG6', 'Test Asset')
    xrefs = replace('gs_quant.timeseries.measures.GsAssetApi.get_asset_xrefs', Mock())
    xrefs.return_value = [
        GsTemporalXRef(datetime.date(2019, 1, 1),
                       datetime.date(2952, 12, 31),
                       XRef(ticker='basket_ticker', ))
    ]
    replace('gs_quant.markets.securities.SecurityMaster.get_asset', Mock()).return_value = mock

    with DataContext(datetime.date(2020, 7, 12), datetime.date(2020, 7, 15)):
        actual = mr.thematic_beta('report_id', 'basket_ticker')
        assert all(actual.values == [1, 1, 1, 1])

    replace.restore()


def test_aum():
    replace = Replacer()

    # mock PerformanceReport.get()
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport(report_id='RP1',
                                          position_source_type='Portfolio',
                                          position_source_id='MP1',
                                          report_type='Portfolio Performance Analytics',
                                          parameters=ReportParameters(transaction_cost_model='FIXED'))

    # mock PerformanceReport.get()
    mock = replace('gs_quant.markets.report.PerformanceReport.get_aum', Mock())
    mock.return_value = {
        '2022-07-01': 100,
        '2022-07-02': 200
    }

    with DataContext(datetime.date(2022, 7, 1), datetime.date(2022, 7, 3)):
        actual = mr.aum('RP1')
        assert all(actual.values == [100, 200])

    replace.restore()


def test_pnl():
    replace = Replacer()

    # mock PerformanceReport.get()
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport(report_id='RP1',
                                          position_source_type='Portfolio',
                                          position_source_id='MP1',
                                          report_type='Portfolio Performance Analytics',
                                          parameters=ReportParameters(transaction_cost_model='FIXED'))

    # mock PerformanceReport.get_pnl()
    mock = replace('gs_quant.markets.report.PerformanceReport.get_pnl', Mock())
    mock.return_value = pandas.DataFrame.from_dict(
        {'date': ['2022-07-01', '2022-07-02', '2022-07-03'], 'pnl': [200, 400, 600]})

    with DataContext(datetime.date(2022, 7, 1), datetime.date(2022, 7, 3)):
        actual = mr.pnl('RP1')
        assert all(actual.values == [200, 400, 600])

    replace.restore()


def test_pnl_percent():
    replace = Replacer()

    # mock PerformanceReport.get()
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport(report_id='RP1',
                                          position_source_type='Portfolio',
                                          position_source_id='MP1',
                                          report_type='Portfolio Performance Analytics',
                                          parameters=ReportParameters(transaction_cost_model='FIXED'))

    pnl = {'2022-07-01': 200, '2022-07-02': 400, '2022-07-03': 600}
    aum = {'2022-06-30': 2000, '2022-07-01': 3000, '2022-07-02': 3000, '2022-07-03': 4000}

    # mock PerformanceReport.get_pnl()
    mock = replace('gs_quant.markets.report.PerformanceReport.get_pnl', Mock())
    mock.return_value = pandas.DataFrame.from_dict({'date': list(pnl.keys()), 'pnl': list(pnl.values())})

    mock = replace('gs_quant.markets.report.PerformanceReport.get_aum_source', Mock())
    mock.return_value = RiskAumSource.Long

    # mock getting performance report
    mock = replace('gs_quant.markets.portfolio_manager.PortfolioManager.get_performance_report', Mock())
    mock.return_value = PerformanceReport(id='ID')

    mock = replace('gs_quant.markets.report.PerformanceReport.get_aum', Mock())
    mock.return_value = aum

    # Each team uses pnl today/aum yesterday
    expected_values = compute_geometric_aggregation_calculations(aum, pnl, list(aum.keys()))

    with DataContext(datetime.date(2022, 7, 1), datetime.date(2022, 7, 3)):
        # mock getting aum
        mock = replace('gs_quant.markets.report.PerformanceReport.get_long_exposure', Mock())
        mock.return_value = pandas.DataFrame.from_dict({'date': aum.keys(), 'longExposure': aum.values()})

        actual = mr.pnl('report_id', 'Percent')
        assert all([a == pytest.approx(e) for a, e in zip(actual.values, expected_values)])

    # with one day's aum missed to test forward filling logic
    with DataContext(datetime.date(2022, 7, 1), datetime.date(2022, 7, 3)):
        # mock getting aum with one day missed to test forward filling logic
        aum = {'2022-06-30': 2000, '2022-07-01': 3000, '2022-07-03': 4000}
        mock = replace('gs_quant.markets.report.PerformanceReport.get_long_exposure', Mock())
        mock.return_value = pandas.DataFrame.from_dict({'date': aum.keys(), 'longExposure': aum.values()})

        actual = mr.pnl('report_id', 'Percent')
        assert all([a == pytest.approx(e) for a, e in zip(actual.values, expected_values)])

    replace.restore()


def test_historical_simulation_estimated_pnl():
    replace = Replacer()

    # mock getting report
    mock = replace('gs_quant.api.gs.reports.GsReportApi.get_report', Mock())
    mock.return_value = factor_risk_report

    # mock getting report factor data
    mock = replace('gs_quant.api.gs.reports.GsReportApi.get_factor_risk_report_results', Mock())
    mock.return_value = factor_exposure_data

    # mock sending data request
    mock = replace('gs_quant.api.gs.data.GsDataApi.execute_query', Mock())
    mock.return_value = {"data": factor_return_data}

    with DataContext(datetime.date(2024, 3, 13), datetime.date(2024, 3, 14)):
        actual = mr.historical_simulation_estimated_pnl('report_id')
        actual_values = list(actual.values)
        assert all([math.isclose(x, actual_values[i]) for i, x in enumerate([7.0, 14.17])])

    replace.restore()


def test_historical_simulation_estimated_factor_attribution():
    replace = Replacer()

    # mock getting report
    mock = replace('gs_quant.api.gs.reports.GsReportApi.get_report', Mock())
    mock.return_value = factor_risk_report

    # mock getting report factor data
    mock = replace('gs_quant.api.gs.reports.GsReportApi.get_factor_risk_report_results', Mock())
    mock.return_value = factor_exposure_data

    # mock sending data request
    mock = replace('gs_quant.api.gs.data.GsDataApi.execute_query', Mock())
    mock.return_value = {"data": [data for data in factor_return_data if data['factor'] == 'Factor_1']}

    with DataContext(datetime.date(2024, 3, 13), datetime.date(2024, 3, 14)):
        actual = mr.historical_simulation_estimated_factor_attribution('report_id', "Factor_1")
        actual_values = list(actual.values)
        assert all([math.isclose(x, actual_values[i]) for i, x in enumerate([2.0, 4.04])])

    replace.restore()


if __name__ == '__main__':
    pytest.main(args=[__file__])
