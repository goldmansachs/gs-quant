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

from gs_quant.api.gs.portfolios import GsPortfolioApi
from gs_quant.api.gs.reports import GsReportApi
from gs_quant.entities.entitlements import Entitlements, User, EntitlementBlock
from gs_quant.markets.portfolio_manager import PortfolioManager
from gs_quant.markets.report import FactorRiskReport, PerformanceReport
from gs_quant.target.portfolios import Portfolio as TargetPortfolio
from gs_quant.target.reports import Report


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
    mock_portfolio = TargetPortfolio(id='MP', currency='USD', name='Example Port')

    mocker.patch.object(GsPortfolioApi, 'get_portfolio',
                        return_value=mock_portfolio)
    mocker.patch.object(GsPortfolioApi, 'get_position_dates',
                        return_value=[dt.date(2020, 1, 2), dt.date(2020, 2, 1), dt.date(2020, 3, 1)])
    mocker.patch.object(GsPortfolioApi, 'get_positions_for_date',
                        return_value=None)

    # run test
    pm = PortfolioManager('MP')
    dates = pm.get_schedule_dates(backcast=True)
    assert dates == [dt.date(2019, 1, 1), dt.date(2020, 1, 2)]
    dates = pm.get_schedule_dates(backcast=False)
    assert dates == [dt.date(2020, 1, 2), dt.date(2020, 3, 1)]


def test_set_entitlements(mocker):
    mock_portfolio = TargetPortfolio(id='MP', currency='USD', name='Example Port')
    entitlements = Entitlements(view=EntitlementBlock(users=[User(user_id='fakeId',
                                                                  name='Fake User',
                                                                  email='fake@gs.com',
                                                                  company='Goldman Sachs')]))

    mocker.patch.object(GsPortfolioApi, 'get_portfolio',
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
    mocker.patch.object(GsReportApi, 'get_risk_factor_data_results',
                        return_value=mock_results)

    # run test
    pm = PortfolioManager('MP')
    pm.run_reports(is_async=False)


if __name__ == '__main__':
    pytest.main(args=[__file__])
