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

import pandas
import pandas as pd
import pytest
from testfixtures import Replacer
from testfixtures.mock import Mock

import gs_quant.timeseries.measures_portfolios as mp
from gs_quant.api.gs.assets import GsTemporalXRef
from gs_quant.api.gs.data import MarketDataResponseFrame
from gs_quant.data.core import DataContext
from gs_quant.errors import MqValueError
from gs_quant.markets.report import PerformanceReport, ThematicReport
from gs_quant.markets.securities import Stock
from gs_quant.models.risk_model import FactorRiskModel as Factor_Risk_Model
from gs_quant.target.common import ReportParameters, XRef
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

    with DataContext(datetime.date(2020, 11, 23), datetime.date(2020, 11, 25)):
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

    with DataContext(datetime.date(2020, 11, 23), datetime.date(2020, 11, 25)):
        # mock getting report factor data
        mock = replace('gs_quant.api.gs.reports.GsReportApi.get_factor_risk_report_results', Mock())
        mock.return_value = factor_data

        actual = mp.portfolio_factor_pnl('report_id', 'risk_model_id', 'Factor Name')
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

    with DataContext(datetime.date(2020, 11, 23), datetime.date(2020, 11, 25)):
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
        GsTemporalXRef(datetime.date(2019, 1, 1),
                       datetime.date(2952, 12, 31),
                       XRef(ticker='basket_ticker', ))
    ]
    replace('gs_quant.markets.securities.SecurityMaster.get_asset', Mock()).return_value = mock

    with DataContext(datetime.date(2020, 7, 12), datetime.date(2020, 7, 15)):
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
    mock.return_value = pandas.DataFrame.from_dict(
        {'date': ['2022-07-01', '2022-07-02', '2022-07-03'], 'pnl': [200, 400, 600]})

    with DataContext(datetime.date(2022, 7, 1), datetime.date(2022, 7, 3)):
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

    with DataContext(datetime.date(2020, 11, 23), datetime.date(2020, 11, 25)):
        actual = mp.portfolio_factor_proportion_of_risk('portfolio_id', 'report_id', 'Factor')
        assert all(actual.values == [1, 2, 3])

    with DataContext(datetime.date(2020, 11, 23), datetime.date(2020, 11, 25)):
        actual = mp.portfolio_daily_risk('portfolio_id', 'report_id', 'Factor')
        assert all(actual.values == [1, 2, 3])

    with DataContext(datetime.date(2020, 11, 23), datetime.date(2020, 11, 25)):
        actual = mp.portfolio_annual_risk('portfolio_id', 'report_id', 'Factor')
        assert all(actual.values == [1, 2, 3])

    with pytest.raises(MqValueError):
        mp.portfolio_daily_risk('portfolio_id', 'report_id', 'Factor Name')

    with pytest.raises(MqValueError):
        mp.portfolio_annual_risk('portfolio_id', 'report_id', 'Factor Name')
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
    with DataContext(datetime.date(2020, 1, 1), datetime.date(2019, 1, 3)):
        actual = mp.aum('MP1')
        assert actual.index.equals(idx)
        assert all(actual.values == data['aum'])
    replace.restore()


if __name__ == '__main__':
    pytest.main(args=[__file__])
