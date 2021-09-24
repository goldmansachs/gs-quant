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

import pytest

from gs_quant.api.gs.data import GsDataApi
from gs_quant.markets.report import FactorRiskReport, PerformanceReport, ThematicReport
from gs_quant.session import *
from gs_quant.target.reports import ReportStatus, PositionSourceType, ReportType, ReportParameters, Report

fake_pfr = FactorRiskReport(risk_model_id='AXUS4M',
                            fx_hedged=True,
                            report_id='PFRID',
                            position_source_type=PositionSourceType.Portfolio,
                            position_source_id='PORTFOLIOID',
                            report_type=ReportType.Portfolio_Factor_Risk,
                            status=ReportStatus.done
                            )

fake_ppa = PerformanceReport(report_id='PPAID',
                             position_source_type=PositionSourceType.Portfolio,
                             position_source_id='PORTFOLIOID',
                             report_type=ReportType.Portfolio_Performance_Analytics,
                             parameters=None,
                             status=ReportStatus.done
                             )
fake_pta = ThematicReport(report_id='PTAID',
                          position_source_type=PositionSourceType.Portfolio,
                          position_source_id='PORTFOLIOID',
                          report_type=ReportType.Portfolio_Thematic_Analytics,
                          parameters=None,
                          status=ReportStatus.done
                          )

factor_risk_results = [
    {
        'date': '2021-01-02',
        'factor': 'factor1',
        'pnl': 123,
        'proportionOfRisk': 100,
        'exposure': 200,
        'annualRisk': 3928,
        'dailyRisk': 202
    },
    {
        'date': '2021-01-03',
        'factor': 'factor1',
        'pnl': 124,
        'proportionOfRisk': 200,
        'exposure': 100,
        'annualRisk': 392,
        'dailyRisk': 21
    },
    {
        'date': '2021-01-04',
        'factor': 'factor1',
        'pnl': 125,
        'proportionOfRisk': 300,
        'exposure': 150,
        'annualRisk': 39,
        'dailyRisk': 22
    }
]

thematic_results = [
    {
        "date": "2021-07-12",
        "reportId": "PTAID",
        "basketId": "MA01GPR89HZF1FZ5",
        "region": "Asia",
        "grossExposure": 3.448370345015856E8,
        "thematicExposure": 1.1057087573594835E8,
        "updateTime": "2021-07-20T23:43:38Z"
    },
    {
        "date": "2021-07-13",
        "reportId": "PTAID",
        "basketId": "MA01GPR89HZF1FZ5",
        "region": "Asia",
        "grossExposure": 3.375772519907556E8,
        "thematicExposure": 1.0511196135243121E8,
        "updateTime": "2021-07-20T23:43:38Z"
    },
    {
        "date": "2021-07-14",
        "reportId": "PTAID",
        "basketId": "MA01GPR89HZF1FZ5",
        "region": "Asia",
        "grossExposure": 3.321189950666118E8,
        "thematicExposure": 1.0089556961211234E8,
        "updateTime": "2021-07-20T23:43:38Z"
    },
    {
        "date": "2021-07-15",
        "reportId": "PTAID",
        "basketId": "MA01GPR89HZF1FZ5",
        "region": "Asia",
        "grossExposure": 3.274071805135091E8,
        "thematicExposure": 9.706991264825605E7,
        "updateTime": "2021-07-20T23:43:38Z"
    }
]


def test_get_performance_report(mocker):
    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_get',
                        return_value=Report(id='PPAID',
                                            position_source_type=PositionSourceType.Portfolio,
                                            position_source_id='PORTFOLIOID',
                                            parameters=None,
                                            type=ReportType.Portfolio_Performance_Analytics,
                                            status=ReportStatus.done))
    # run test
    response = PerformanceReport.get('PPAID')
    assert response.type == ReportType.Portfolio_Performance_Analytics


def test_get_risk_model_id():
    assert fake_pfr.get_risk_model_id() == 'AXUS4M'


def test_set_position_target():
    factor_report = FactorRiskReport(report_id='PFRID',
                                     position_source_type=PositionSourceType.Portfolio,
                                     position_source_id='PORTFOLIOID',
                                     report_type=ReportType.Portfolio_Factor_Risk,
                                     parameters=ReportParameters(fx_hedged=True,
                                                                 risk_model='AXUS4M'),
                                     status=ReportStatus.done
                                     )
    factor_report.set_position_source('MA3FMSN9VNMD')
    assert factor_report.position_source_type == PositionSourceType.Asset
    assert factor_report.type == ReportType.Asset_Factor_Risk


def test_get_factor_risk_report(mocker):
    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_get',
                        return_value=Report(id='PFRID',
                                            position_source_type=PositionSourceType.Portfolio,
                                            position_source_id='PORTFOLIOID',
                                            parameters=ReportParameters(risk_model='AXUS4M',
                                                                        fx_hedged=True),
                                            type=ReportType.Portfolio_Factor_Risk,
                                            status=ReportStatus.done))
    # run test
    response = FactorRiskReport.get('PFRID')
    assert response.type == ReportType.Portfolio_Factor_Risk


def test_get_factor_pnl(mocker):
    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_get', return_value=factor_risk_results)

    # run test
    response = fake_pfr.get_factor_pnl(factor_names=['factor1'])
    assert len(response) == 3


def test_get_factor_proportion_of_risk(mocker):
    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_get', return_value=factor_risk_results)

    # run test
    response = fake_pfr.get_factor_proportion_of_risk(factor_names=['factor1'])
    assert len(response) == 3


def test_get_factor_exposure(mocker):
    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_get', return_value=factor_risk_results)

    # run test
    response = fake_pfr.get_factor_exposure(factor_names=['factor1'])
    assert len(response) == 3


def test_get_annual_risk(mocker):
    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_get', return_value=factor_risk_results)

    # run test
    response = fake_pfr.get_annual_risk('factor1')
    assert len(response) == 3


def test_get_daily_risk(mocker):
    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_get', return_value=factor_risk_results)

    # run test
    response = fake_pfr.get_daily_risk('factor1')
    assert len(response) == 3


def test_get_measures(mocker):
    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsDataApi, 'query_data', return_value=thematic_results)

    # run test
    response = fake_pta._get_measures(["grossExposure", "thematicExposure"])
    assert len(response) == 4


if __name__ == '__main__':
    pytest.main(args=[__file__])
