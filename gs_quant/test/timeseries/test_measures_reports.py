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
import datetime
import pandas as pd
import pytest
from testfixtures import Replacer
from testfixtures.mock import Mock

import gs_quant.timeseries.measures_reports as mr
from gs_quant.api.gs.data import MarketDataResponseFrame
from gs_quant.data.core import DataContext
from gs_quant.errors import MqValueError, MqError
from gs_quant.models.risk_model import FactorRiskModel as Factor_Risk_Model
from gs_quant.target.common import ReportParameters
from gs_quant.target.reports import Report, PositionSourceType, ReportType
from gs_quant.target.risk_models import RiskModel, CoverageType, Term, UniverseIdentifier
from gs_quant.markets.report import PerformanceReport
from gs_quant.target.portfolios import RiskAumSource, Portfolio

risk_model = RiskModel(coverage=CoverageType.Country, id_='model_id', name='Fake Risk Model',
                       term=Term.Long, universe_identifier=UniverseIdentifier.gsid, vendor='GS',
                       version=1.0)

factor_risk_report = Report(position_source_id='position source id',
                            position_source_type=PositionSourceType.Portfolio,
                            type_=ReportType.Portfolio_Factor_Risk,
                            id_='report_id',
                            parameters=ReportParameters(risk_model='risk_model_id'),
                            status='new')

ppa_report = Report(position_source_id='position source id',
                    position_source_type=PositionSourceType.Portfolio,
                    type_=ReportType.Portfolio_Performance_Analytics,
                    id_='report_id',
                    parameters=ReportParameters(risk_model='risk_model_id'),
                    status='new')

factor_data = [
    {
        'date': '2020-11-23',
        'reportId': 'report_id',
        'factor': 'factor_id',
        'factorCategory': 'CNT',
        'pnl': 11.23,
        'exposure': -11.23,
        'proportionOfRisk': 1
    },
    {
        'date': '2020-11-24',
        'reportId': 'report_id',
        'factor': 'factor_id',
        'factorCategory': 'CNT',
        'pnl': 11.24,
        'exposure': -11.24,
        'proportionOfRisk': 2
    },
    {
        'date': '2020-11-25',
        'reportId': 'report_id',
        'factor': 'factor_id',
        'factorCategory': 'CNT',
        'pnl': 11.25,
        'exposure': -11.25,
        'proportionOfRisk': 3
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

ppa_data = {
    'netExposure': [
        -1,
        -0.8,
        -0.6
    ],
    'grossExposure': [
        1,
        1.2,
        1.4
    ],
    'longExposure': [
        1,
        1.2,
        1.4
    ],
    'shortExposure': [
        1,
        0.8,
        0.6
    ],
    'pnl': [
        0.1,
        0.2,
        0.2
    ],
    'date': [
        '2020-01-02',
        '2020-01-03',
        '2020-01-04'
    ]
}

aum = [{'date': '2020-01-02', 'aum': 2}, {'date': '2020-01-03', 'aum': 2.2}, {'date': '2020-01-04', 'aum': 2.4}]


def mock_risk_model():
    risk_model = RiskModel(coverage=CoverageType.Country, id_='model_id', name='Fake Risk Model',
                           term=Term.Long, universe_identifier=UniverseIdentifier.gsid, vendor='GS',
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
    mock = replace('gs_quant.api.gs.reports.GsReportApi.get_risk_factor_data_results', Mock())
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


def test_factor_pnl():
    replace = Replacer()

    # mock getting risk model entity()
    mock = replace('gs_quant.api.gs.risk_models.GsRiskModelApi.get_risk_model', Mock())
    mock.return_value = risk_model

    mock = replace('gs_quant.api.gs.reports.GsReportApi.get_report', Mock())
    mock.return_value = factor_risk_report

    # mock getting report factor data
    mock = replace('gs_quant.api.gs.reports.GsReportApi.get_risk_factor_data_results', Mock())
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
        actual = mr.factor_pnl('report_id', 'Factor Name')
        assert all(actual.values == [11.23, 11.24, 11.25])

    with pytest.raises(MqValueError):
        mr.factor_pnl('report_id', 'Wrong Factor Name')
    replace.restore()


def test_factor_proportion_of_risk():
    replace = Replacer()

    # mock getting risk model entity()
    mock = replace('gs_quant.api.gs.risk_models.GsRiskModelApi.get_risk_model', Mock())
    mock.return_value = risk_model

    mock = replace('gs_quant.api.gs.reports.GsReportApi.get_report', Mock())
    mock.return_value = factor_risk_report

    # mock getting report factor data
    mock = replace('gs_quant.api.gs.reports.GsReportApi.get_risk_factor_data_results', Mock())
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
    mock = replace('gs_quant.api.gs.reports.GsReportApi.get_risk_factor_data_results', Mock())
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
    expected = {RiskAumSource.Net: pd.Series(data=[1, 1 / 0.8, 1 / 0.6], index=idx,
                                             name='normalizedPerformance', dtype='float64'),
                RiskAumSource.Gross: pd.Series(data=[1, 1.2, 1.4], index=idx,
                                               name='normalizedPerformance', dtype='float64'),
                RiskAumSource.Long: pd.Series(data=[1, 1.2, 1.4], index=idx,
                                              name='normalizedPerformance', dtype='float64'),
                RiskAumSource.Short: pd.Series(data=[1, 1 / 0.8, 1 / 0.6], index=idx,
                                               name='normalizedPerformance', dtype='float64'),
                RiskAumSource.Custom_AUM: pd.Series(data=[1, 1.1, 1.2], index=idx,
                                                    name='normalizedPerformance', dtype='float64')}

    with DataContext(datetime.date(2020, 1, 1), datetime.date(2019, 1, 3)):
        for k, v in expected.items():
            df = MarketDataResponseFrame(data=ppa_data, dtype="float64")
            replace = Replacer()

            # mock GsPortfolioApi.get_reports()
            mock = replace('gs_quant.api.gs.portfolios.GsPortfolioApi.get_reports', Mock())
            mock.return_value = [
                Report.from_dict({'id': 'RP1', 'positionSourceType': 'Portfolio', 'positionSourceId': 'MP1',
                                  'type': 'Portfolio Performance Analytics',
                                  'parameters': {'transactionCostModel': 'FIXED'}})]

            # mock PerformanceReport.get_many_measures()
            mock = replace('gs_quant.markets.report.PerformanceReport.get_many_measures', Mock())
            mock.return_value = df

            # mock PerformanceReport.get_custom_aum()
            mock = replace('gs_quant.api.gs.portfolios.GsPortfolioApi.get_custom_aum', Mock())
            mock.return_value = aum

            # mock PerformanceReport.get()
            mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
            mock.return_value = PerformanceReport(report_id='RP1',
                                                  position_source_type='Portfolio',
                                                  position_source_id='MP1',
                                                  report_type='Portfolio Performance Analytics',
                                                  parameters=ReportParameters(transaction_cost_model='FIXED'))

            actual = mr.normalized_performance('MP1', k.value)
            assert all(actual.values == v.values)
            replace.restore()


def test_normalized_performance_default_aum():
    idx = pd.date_range('2020-01-02', freq='D', periods=3)
    expected = pd.Series(data=[1, 1 / 0.8, 1 / 0.6], index=idx, name='normalizedPerformance', dtype='float64')

    with DataContext(datetime.date(2020, 1, 1), datetime.date(2019, 1, 3)):

        df = MarketDataResponseFrame(data=ppa_data, dtype="float64")
        replace = Replacer()

        # mock GsPortfolioApi.get_reports()
        mock = replace('gs_quant.api.gs.portfolios.GsPortfolioApi.get_reports', Mock())
        mock.return_value = [
            Report.from_dict({'id': 'RP1', 'positionSourceType': 'Portfolio', 'positionSourceId': 'MP1',
                              'type': 'Portfolio Performance Analytics',
                              'parameters': {'transactionCostModel': 'FIXED'}})]

        # mock PerformanceReport.get_many_measures()
        mock = replace('gs_quant.markets.report.PerformanceReport.get_many_measures', Mock())
        mock.return_value = df

        # mock PerformanceReport.get_custom_aum()
        mock = replace('gs_quant.api.gs.portfolios.GsPortfolioApi.get_custom_aum', Mock())
        mock.return_value = aum

        # mock PerformanceReport.get()
        mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
        mock.return_value = PerformanceReport(report_id='RP1',
                                              position_source_type='Portfolio',
                                              position_source_id='MP1',
                                              report_type='Portfolio Performance Analytics',
                                              parameters=ReportParameters(transaction_cost_model='FIXED'))

        mock = replace('gs_quant.api.gs.portfolios.GsPortfolioApi.get_portfolio', Mock())
        mock.return_value = Portfolio('USD', 'P1', id_='MP1')

        actual = mr.normalized_performance('MP1', None)
        assert all(actual.values == expected.values)
        replace.restore()


def test_normalized_performance_no_custom_aum():
    with DataContext(datetime.date(2020, 1, 1), datetime.date(2019, 1, 3)):
        df = MarketDataResponseFrame(data=ppa_data, dtype="float64")
        replace = Replacer()

        # mock GsPortfolioApi.get_reports()
        mock = replace('gs_quant.api.gs.portfolios.GsPortfolioApi.get_reports', Mock())
        mock.return_value = [
            Report.from_dict({'id': 'RP1', 'positionSourceType': 'Portfolio', 'positionSourceId': 'MP1',
                              'type': 'Portfolio Performance Analytics',
                              'parameters': {'transactionCostModel': 'FIXED'}})]

        # mock PerformanceReport.get_many_measures()
        mock = replace('gs_quant.markets.report.PerformanceReport.get_many_measures', Mock())
        mock.return_value = df

        # mock PerformanceReport.get_custom_aum()
        mock = replace('gs_quant.api.gs.portfolios.GsPortfolioApi.get_custom_aum', Mock())
        mock.return_value = pd.DataFrame({})

        # mock PerformanceReport.get()
        mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
        mock.return_value = PerformanceReport(report_id='RP1',
                                              position_source_type='Portfolio',
                                              position_source_id='MP1',
                                              report_type='Portfolio Performance Analytics',
                                              parameters=ReportParameters(transaction_cost_model='FIXED'))

        with pytest.raises(MqError):
            mr.normalized_performance('MP1', 'Custom AUM')
        replace.restore()


if __name__ == '__main__':
    pytest.main(args=[__file__])
