"""
Copyright 2018 Goldman Sachs.
Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""

import datetime as dt

import pytest

from gs_quant.api.gs.esg import GsEsgApi, ESGMeasure
from gs_quant.api.gs.portfolios import GsPortfolioApi
from gs_quant.api.gs.reports import GsReportApi
from gs_quant.entities.entitlements import Entitlements, User, EntitlementBlock
from gs_quant.markets.portfolio_manager import PortfolioManager
from gs_quant.markets.report import FactorRiskReport, PerformanceReport
from gs_quant.session import GsSession, Environment
from gs_quant.target.portfolios import Portfolio as TargetPortfolio
from gs_quant.target.reports import Report

esg_data = {
    'pricingDate': '2021-08-25',
    'quintiles': [{
        'measure': 'gPercentile',
        'results': [{
            'name': 'Q1',
            'description': '<=80-100%',
            'gross': 91.03557560284325,
            'long': 91.03557560284325,
            'short': 0
        }, {
            'name': 'Q2',
            'description': '<=60-80%',
            'gross': 0,
            'long': 0,
            'short': 0
        }, {
            'name': 'Q3',
            'description': '<=40-60%',
            'gross': 0,
            'long': 0,
            'short': 0
        }, {
            'name': 'Q4',
            'description': '<=20-40%',
            'gross': 8.955474904385047,
            'long': 0,
            'short': 8.955474904385047
        }, {
            'name': 'Q5',
            'description': '<=0-20%',
            'gross': 0,
            'long': 0,
            'short': 0
        }, {
            'name': 'Not Included',
            'description': 'Not Included',
            'gross': 0.008949492771697426,
            'long': 0.008949492771697426,
            'short': 0
        }]
    }],
    'summary': {
        'gross': {
            'gPercentile': 91.71440761636107,
            'gRegionalPercentile': 84.58263751763046,
            'esPercentile': 90.07443582510577,
            'esDisclosurePercentage': 78.50077574047954,
            'esMomentumPercentile': 74.20073342736248
        },
        'long': {
            'gPercentile': 97.39,
            'gRegionalPercentile': 92.62,
            'esPercentile': 94.24,
            'esDisclosurePercentage': 83.33,
            'esMomentumPercentile': 76.85
        },
        'short': {
            'gPercentile': 34.02,
            'gRegionalPercentile': 2.88,
            'esPercentile': 47.73,
            'esDisclosurePercentage': 29.41,
            'esMomentumPercentile': 47.27
        }
    },
    'weightsBySector': [{
        'name': 'Diversified Financials',
        'gross': 91.03557560284325,
        'long': 91.03557560284325,
        'short': 0
    }, {
        'name': 'Automobile Manufacturers',
        'gross': 8.955474904385047,
        'long': 0,
        'short': 8.955474904385047
    }, {
        'name': 'Total',
        'gross': 99.99105050722832,
        'long': 91.03557560284325,
        'short': 8.955474904385047
    }, {
        'name': 'Not Included',
        'gross': 0.008949492771697426,
        'long': 0.008949492771697426,
        'short': 0
    }],
    'measuresBySector': [{
        'measure': 'gPercentile',
        'results': [{
            'name': 'Diversified Financials',
            'gross': 97.39,
            'long': 97.39,
            'short': 0
        }, {
            'name': 'Automobile Manufacturers',
            'gross': 34.02,
            'long': 0,
            'short': 34.02
        }, {
            'name': 'Total',
            'gross': 91.71440761636107,
            'long': 97.39,
            'short': 34.02
        }]
    }],
    'weightsByRegion': [{
        'name': 'N. America',
        'gross': 99.99105050722832,
        'long': 91.03557560284325,
        'short': 8.955474904385047
    }, {
        'name': 'Total',
        'gross': 99.99105050722832,
        'long': 91.03557560284325,
        'short': 8.955474904385047
    }, {
        'name': 'Not Included',
        'gross': 0.008949492771697426,
        'long': 0.008949492771697426,
        'short': 0
    }],
    'measuresByRegion': [{
        'measure': 'gPercentile',
        'results': [{
            'name': 'N. America',
            'gross': 91.71440761636107,
            'long': 97.39,
            'short': 34.02
        }, {
            'name': 'Total',
            'gross': 91.71440761636107,
            'long': 97.39,
            'short': 34.02
        }]
    }],
    'topTenRanked': [{
        'measure': 'gPercentile',
        'results': [{
            'assetId': 'MA4B66MW5E27UAHKG34',
            'name': 'The Goldman Sachs Group, Inc.',
            'value': 97.39
        }, {
            'assetId': 'MA4B66MW5E27UANEQ6R',
            'name': 'Tesla Inc',
            'value': 34.02
        }]
    }],
    'bottomTenRanked': [{
        'measure': 'gPercentile',
        'results': [{
            'assetId': 'MA4B66MW5E27UANEQ6R',
            'name': 'Tesla Inc',
            'value': 34.02
        }, {
            'assetId': 'MA4B66MW5E27UAHKG34',
            'name': 'The Goldman Sachs Group, Inc.',
            'value': 97.39
        }]
    }],
    'noESGData': {
        'gross': {
            'weight': 0.008949492771697426,
            'assets': [{
                'assetId': 'MA4B66MW5E27UAL9SX6',
                'name': 'Mustek LTD',
                'weight': 0.008949492771697426
            }]
        },
        'long': {
            'weight': 0.008949492771697426,
            'assets': [{
                'assetId': 'MA4B66MW5E27UAL9SX6',
                'name': 'Mustek LTD',
                'weight': 0.008949492771697426
            }]
        },
        'short': {
            'weight': 0.0,
            'assets': []
        }
    }
}


def test_get_reports(mocker):
    mock_portfolio = TargetPortfolio(id='MP', currency='USD', name='Example Port')
    mock_reports = (Report.from_dict({'id': 'PPAID', 'positionSourceType': 'Portfolio', 'positionSourceId': 'MP',
                                      'type': 'Portfolio Performance Analytics',
                                      'parameters': {'transactionCostModel': 'FIXED'},
                                      'percentageComplete': 0, 'status': 'new'}),
                    Report.from_dict({'id': 'PFRID', 'positionSourceType': 'Portfolio', 'positionSourceId': 'MP',
                                      'type': 'Portfolio Factor Risk', 'parameters': {'riskModel': 'AXUS4M',
                                                                                      'transactionCostModel': 'FIXED'},
                                      'percentageComplete': 0, 'status': 'new'}))

    mocker.patch.object(GsPortfolioApi, 'get_portfolio',
                        return_value=mock_portfolio)
    mocker.patch.object(GsPortfolioApi, 'get_position_dates',
                        return_value=[dt.date(2020, 1, 1)])
    mocker.patch.object(GsPortfolioApi, 'get_positions_for_date',
                        return_value=None)
    mocker.patch.object(GsPortfolioApi, 'get_reports',
                        return_value=mock_reports)

    # run test
    pm = PortfolioManager('MP')
    reports = pm.get_reports()
    assert len(reports) == 2
    assert isinstance(reports[0], PerformanceReport)
    assert isinstance(reports[1], FactorRiskReport)


def test_get_schedule_dates(mocker):
    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_get', return_value={'startDate': '2019-01-01', 'endDate': '2020-01-02'})

    # run test
    pm = PortfolioManager('MP')
    dates = pm.get_schedule_dates()
    assert dates[1] == dt.date(2020, 1, 2)


def test_set_entitlements(mocker):
    mock_portfolio = TargetPortfolio(id='MP', currency='USD', name='Example Port')
    entitlements = Entitlements(view=EntitlementBlock(users=[User(user_id='fakeId',
                                                                  name='Fake User',
                                                                  email='fake@gs.com',
                                                                  company='Goldman Sachs')]))

    mocker.patch.object(GsSession, '_get',
                        return_value=mock_portfolio)
    mocker.patch.object(GsPortfolioApi, 'get_position_dates',
                        return_value=[dt.date(2020, 1, 2), dt.date(2020, 2, 1), dt.date(2020, 3, 1)])
    mocker.patch.object(GsPortfolioApi, 'get_positions_for_date',
                        return_value=None)
    mocker.patch.object(GsPortfolioApi, 'update_portfolio',
                        return_value='')

    # run test
    pm = PortfolioManager('MP')
    pm.set_entitlements(entitlements)


def test_run_reports(mocker):
    mock_portfolio = TargetPortfolio(id='MP', currency='USD', name='Example Port')
    mock_reports = (Report.from_dict({'id': 'PPAID', 'positionSourceType': 'Portfolio', 'positionSourceId': 'MP',
                                      'type': 'Portfolio Performance Analytics',
                                      'parameters': {'transactionCostModel': 'FIXED'},
                                      'percentageComplete': 0, 'status': 'new'}),)
    mock_report_jobs = ({'startDate': '2020-01-01',
                         'endDate': '2020-03-02',
                         'id': 'jobId1',
                         'createdTime': '2021-05-18T17:08:18.72Z',
                         'reportType': 'Portfolio Factor Risk'
                         },
                        {'startDate': '2020-05-01',
                         'endDate': '2020-07-02',
                         'id': 'jobId1',
                         'createdTime': '2020-05-18T17:08:18.72Z',
                         'reportType': 'Portfolio Factor Risk'
                         })
    mock_report_job = {
        'startDate': '2020-01-01',
        'endDate': '2020-03-02',
        'id': 'jobId1',
        'createdTime': '2021-05-18T17:08:18.72Z',
        'reportType': 'Portfolio Factor Risk',
        'status': 'done'
    }
    mock_results = [{
        'date': "2019-08-27",
        'factor': "United States",
        'factorCategory': "Country",
        'pnl': -162.93571064768423,
        'exposure': 19878.043518298073,
        'sensitivity': 52.7507947211687,
        'proportionOfRisk': 0.050898995661382604
    }]

    mocker.patch.object(GsPortfolioApi, 'get_portfolio',
                        return_value=mock_portfolio)
    mocker.patch.object(GsPortfolioApi, 'schedule_reports',
                        return_value='')
    mocker.patch.object(GsPortfolioApi, 'get_position_dates',
                        return_value=[dt.date(2020, 1, 1)])
    mocker.patch.object(GsPortfolioApi, 'get_positions_for_date',
                        return_value=None)
    mocker.patch.object(GsPortfolioApi, 'get_reports',
                        return_value=mock_reports)
    mocker.patch.object(GsReportApi, 'get_report_jobs',
                        return_value=mock_report_jobs)
    mocker.patch.object(GsReportApi, 'get_report_job',
                        return_value=mock_report_job)
    mocker.patch.object(GsReportApi, 'get_factor_risk_report_results',
                        return_value=mock_results)

    # run test
    pm = PortfolioManager('MP')
    pm.run_reports(is_async=False)


def test_esg_summary(mocker):
    mocker.patch.object(GsEsgApi, 'get_esg',
                        return_value=esg_data)

    # run test
    pm = PortfolioManager('MP')
    summary = pm.get_esg_summary()
    assert all(summary.columns.values == ['gross', 'long', 'short'])


def test_esg_quintiles(mocker):
    mocker.patch.object(GsEsgApi, 'get_esg',
                        return_value=esg_data)

    # run test
    pm = PortfolioManager('MP')
    quintiles = pm.get_esg_quintiles(measure=ESGMeasure.G_PERCENTILE)
    assert all(quintiles.columns.values == ['gross', 'long', 'short'])


def test_esg_by_sector(mocker):
    mocker.patch.object(GsEsgApi, 'get_esg',
                        return_value=esg_data)

    # run test
    pm = PortfolioManager('MP')
    breakdown = pm.get_esg_by_region(measure=ESGMeasure.G_PERCENTILE)
    assert all(breakdown.columns.values == ['gross', 'long', 'short'])


def test_esg_by_region(mocker):
    mocker.patch.object(GsEsgApi, 'get_esg',
                        return_value=esg_data)

    # run test
    pm = PortfolioManager('MP')
    breakdown = pm.get_esg_by_region(measure=ESGMeasure.G_PERCENTILE)
    assert all(breakdown.columns.values == ['gross', 'long', 'short'])


def test_esg_top_ten(mocker):
    mocker.patch.object(GsEsgApi, 'get_esg',
                        return_value=esg_data)

    # run test
    pm = PortfolioManager('MP')
    ranked = pm.get_esg_top_ten(measure=ESGMeasure.G_PERCENTILE)
    assert ranked.size == 4


def test_esg_bottom_ten(mocker):
    mocker.patch.object(GsEsgApi, 'get_esg',
                        return_value=esg_data)

    # run test
    pm = PortfolioManager('MP')
    ranked = pm.get_esg_bottom_ten(measure=ESGMeasure.G_PERCENTILE)
    assert ranked.size == 4


if __name__ == '__main__':
    pytest.main(args=[__file__])
