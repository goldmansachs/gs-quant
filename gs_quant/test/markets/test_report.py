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

from gs_quant.api.gs.data import GsDataApi
from gs_quant.api.gs.thematics import GsThematicApi
from gs_quant.markets.report import FactorRiskReport, PerformanceReport, ThematicReport, flatten_results_into_df
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


def test_flatten_results_into_df():
    thematics_endpoint_results = [
        {
            "date": "2020-09-14",
            "topFiveThematicExposures": [
                {
                    "basketName": "GS TMT MegaCap Tech",
                    "basketTicker": "GSTMTMEG",
                    "basketRegion": "Americas",
                    "basketCurrency": "USD",
                    "basketId": "MA459FTE58S22HY4",
                    "thematicExposure": 11251933.154873407,
                    "thematicBeta": 1.438066493862124
                },
                {
                    "basketName": "Hedge Fund VIP",
                    "basketTicker": "GSTHHVIP",
                    "basketRegion": "Americas",
                    "basketCurrency": "USD",
                    "basketId": "MAMGDVSWVXWHEHFQ",
                    "thematicExposure": 5158237.284525287,
                    "thematicBeta": 0.6592545568983715
                },
                {
                    "basketName": "GS Asia Stay at Home",
                    "basketTicker": "GSXASTAY",
                    "basketRegion": "Asia",
                    "basketCurrency": "USD",
                    "basketId": "MA1C2Q2AAAT57AX7",
                    "thematicExposure": 3878730.3538401644,
                    "thematicBeta": 0.49572567520698857
                },
                {
                    "basketName": "GS Secular Growth",
                    "basketTicker": "GSXUSGRO",
                    "basketRegion": "Americas",
                    "basketCurrency": "USD",
                    "basketId": "MAHQEJG82N4DNBCH",
                    "thematicExposure": 3642083.749962656,
                    "thematicBeta": 0.46548077886443323
                },
                {
                    "basketName": "GS China 14th 5Year Plan",
                    "basketTicker": "GSXAC5YP",
                    "basketRegion": "Asia",
                    "basketCurrency": "USD",
                    "basketId": "MAGP7WNPCMN5MJWQ",
                    "thematicExposure": 3347766.929109541,
                    "thematicBeta": 0.42786527290441334
                }
            ]
        },
        {
            "date": "2020-09-15",
            "topFiveThematicExposures": [
                {
                    "basketName": "GS TMT MegaCap Tech",
                    "basketTicker": "GSTMTMEG",
                    "basketRegion": "Americas",
                    "basketCurrency": "USD",
                    "basketId": "MA459FTE58S22HY4",
                    "thematicExposure": 11304916.702270757,
                    "thematicBeta": 1.4050953516801092
                },
                {
                    "basketName": "Hedge Fund VIP",
                    "basketTicker": "GSTHHVIP",
                    "basketRegion": "Americas",
                    "basketCurrency": "USD",
                    "basketId": "MAMGDVSWVXWHEHFQ",
                    "thematicExposure": 5241527.529878033,
                    "thematicBeta": 0.651472820357501
                },
                {
                    "basketName": "GS Asia Stay at Home",
                    "basketTicker": "GSXASTAY",
                    "basketRegion": "Asia",
                    "basketCurrency": "USD",
                    "basketId": "MA1C2Q2AAAT57AX7",
                    "thematicExposure": 3868608.7685798025,
                    "thematicBeta": 0.4808318664664322
                },
                {
                    "basketName": "GS Secular Growth",
                    "basketTicker": "GSXUSGRO",
                    "basketRegion": "Americas",
                    "basketCurrency": "USD",
                    "basketId": "MAHQEJG82N4DNBCH",
                    "thematicExposure": 3661450.0674766554,
                    "thematicBeta": 0.4550839785654401
                },
                {
                    "basketName": "GS China 14th 5Year Plan",
                    "basketTicker": "GSXAC5YP",
                    "basketRegion": "Asia",
                    "basketCurrency": "USD",
                    "basketId": "MAGP7WNPCMN5MJWQ",
                    "thematicExposure": 3344638.716916008,
                    "thematicBeta": 0.41570729249548893
                }
            ]
        },
        {
            "date": "2020-09-16",
            "topFiveThematicExposures": [
                {
                    "basketName": "GS TMT MegaCap Tech",
                    "basketTicker": "GSTMTMEG",
                    "basketRegion": "Americas",
                    "basketCurrency": "USD",
                    "basketId": "MA459FTE58S22HY4",
                    "thematicExposure": 11173613.76263776,
                    "thematicBeta": 1.487220141961805
                },
                {
                    "basketName": "Hedge Fund VIP",
                    "basketTicker": "GSTHHVIP",
                    "basketRegion": "Americas",
                    "basketCurrency": "USD",
                    "basketId": "MAMGDVSWVXWHEHFQ",
                    "thematicExposure": 4800709.171521289,
                    "thematicBeta": 0.6389796110065071
                },
                {
                    "basketName": "GS Asia Stay at Home",
                    "basketTicker": "GSXASTAY",
                    "basketRegion": "Asia",
                    "basketCurrency": "USD",
                    "basketId": "MA1C2Q2AAAT57AX7",
                    "thematicExposure": 3767199.2638762216,
                    "thematicBeta": 0.501418318463317
                },
                {
                    "basketName": "GS Secular Growth",
                    "basketTicker": "GSXUSGRO",
                    "basketRegion": "Americas",
                    "basketCurrency": "USD",
                    "basketId": "MAHQEJG82N4DNBCH",
                    "thematicExposure": 3645814.9989552647,
                    "thematicBeta": 0.4852619408094451
                },
                {
                    "basketName": "GS US Stay at Home",
                    "basketTicker": "GSXUSTAY",
                    "basketRegion": "Americas",
                    "basketCurrency": "USD",
                    "basketId": "MA9B9TEMQ2RW16K9",
                    "thematicExposure": 3354419.7766576866,
                    "thematicBeta": 0.4464769198593304
                }
            ]
        }
    ]
    df = flatten_results_into_df(thematics_endpoint_results)
    assert (df.shape == (15, 8))
    thematics_endpoint_results = [
        {
            "date": "2020-09-14",
            "allThematicExposures": [
                {
                    "basketName": "GS TMT MegaCap Tech",
                    "basketTicker": "GSTMTMEG",
                    "basketRegion": "Americas",
                    "basketCurrency": "USD",
                    "basketId": "MA459FTE58S22HY4",
                    "thematicExposure": 11251933.154873407,
                    "thematicBeta": 1.438066493862124
                },
                {
                    "basketName": "Hedge Fund VIP",
                    "basketTicker": "GSTHHVIP",
                    "basketRegion": "Americas",
                    "basketCurrency": "USD",
                    "basketId": "MAMGDVSWVXWHEHFQ",
                    "thematicExposure": 5158237.284525287,
                    "thematicBeta": 0.6592545568983715
                },
                {
                    "basketName": "GS Asia Stay at Home",
                    "basketTicker": "GSXASTAY",
                    "basketRegion": "Asia",
                    "basketCurrency": "USD",
                    "basketId": "MA1C2Q2AAAT57AX7",
                    "thematicExposure": 3878730.3538401644,
                    "thematicBeta": 0.49572567520698857
                }
            ]
        }
    ]
    df = flatten_results_into_df(thematics_endpoint_results)
    assert (df.shape == (3, 8))


def test_get_thematic_breakdown(mocker):
    thematics_endpoint_results = [
        {
            "date": "2020-09-14",
            "thematicBreakdownByAsset": [
                {
                    "basketName": "GS Asia Stay at Home",
                    "basketTicker": "GSXASTAY",
                    "basketRegion": "Asia",
                    "basketCurrency": "USD",
                    "basketId": "MA1C2Q2AAAT57AX7",
                    "thematicBeta": 0.49572567520698857,
                    "thematicBreakdownByAsset": [
                        {
                            "name": "Allstate Corp",
                            "bbid": "ALL UN",
                            "sector": "Financials",
                            "industry": "Insurance",
                            "region": "Americas",
                            "country": "United States",
                            "assetId": "MA4B66MW5E27U9YGM27",
                            "beta": -0.19208866590832985,
                            "thematicExposure": 38530.05709547743
                        },
                        {
                            "name": "Allergan PLC",
                            "bbid": "AGN UN",
                            "sector": "None",
                            "industry": "None",
                            "region": "Europe",
                            "country": "United States",
                            "assetId": "MA4B66MW5E27U9XPVMG",
                            "beta": 0.10085184726854478,
                            "thematicExposure": -41210.418676042646
                        },
                        {
                            "name": "Bristol-Myers Squibb Co",
                            "bbid": "BMY UN",
                            "sector": "Health Care",
                            "industry": "Pharmaceuticals",
                            "region": "Americas",
                            "country": "United States",
                            "assetId": "MA4B66MW5E27UA4479J",
                            "beta": 0.02101418329131077,
                            "thematicExposure": 19108.02476936883
                        },
                        {
                            "name": "Bank of New York Mellon Corp",
                            "bbid": "BK UN",
                            "sector": "Financials",
                            "industry": "Capital Markets",
                            "region": "Americas",
                            "country": "United States",
                            "assetId": "MA4B66MW5E27UA39JL8",
                            "beta": -0.060160353375185896,
                            "thematicExposure": 11806.1366204509
                        }
                    ]
                }
            ]
        }
    ]
    mocker.patch.object(GsThematicApi, 'get_thematics', return_value=thematics_endpoint_results)
    df = fake_pta.get_thematic_breakdown(date=dt.date(2020, 9, 14), basket_id='MA1C2Q2AAAT57AX7')
    assert (df.shape == (4, 9))


if __name__ == '__main__':
    pytest.main(args=[__file__])
