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

from gs_quant.api.gs.risk_models import GsRiskModelApi, GsFactorRiskModelApi
from gs_quant.session import *
from gs_quant.target.risk_models import RiskModel, Factor, RiskModelCalendar, \
    RiskModelDataAssetsRequest as DataAssetsRequest, RiskModelDataMeasure as Measure, \
    RiskModelUniverseIdentifierRequest as UniverseIdentifier


def test_get_risk_models(mocker):
    mock_response = {
        'results': [
            RiskModel.from_dict({
                "coverage": "Global",
                "id": "WW_TEST_MODEL",
                "name": "World Wide Medium Term Test Model",
                "term": "Medium",
                "vendor": "Goldman Sachs",
                "universeIdentifier": "gsid",
                "type": "Factor",
                "version": 4
            }),
            RiskModel.from_dict({
                "coverage": "Global",
                "id": "WW_TEST_MODEL_2",
                "name": "World Wide Medium Term Test Model 2",
                "term": "Medium",
                "vendor": "Goldman Sachs",
                "universeIdentifier": "gsid",
                "version": 2,
                "type": "Thematic"
            })
        ],
        'totalResults': 2
    }

    expected_response = [
        RiskModel(coverage='Global', id='WW_TEST_MODEL', name='World Wide Medium Term Test Model', term='Medium',
                  vendor='Goldman Sachs', universe_identifier='gsid', version=4, type='Factor'),
        RiskModel(coverage='Global', id='WW_TEST_MODEL_2', name='World Wide Medium Term Test Model 2', term='Medium',
                  vendor='Goldman Sachs', universe_identifier='gsid', version=2, type='Thematic')
    ]

    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_get', return_value=mock_response)

    # run test
    response = GsRiskModelApi.get_risk_models()
    GsSession.current._get.assert_called_with('/risk/models?', cls=RiskModel)
    assert response == expected_response


def test_get_risk_model(mocker):
    model_id = 'WW_TEST_MODEL'
    model = RiskModel.from_dict({
        "coverage": "Global",
        "id": "WW_TEST_MODEL",
        "name": "World Wide Medium Term Test Model",
        "term": "Medium",
        "vendor": "Goldman Sachs",
        "universeIdentifier": "gsid",
        "version": 4,
        "type": "Factor"
    })

    expected_response = RiskModel(coverage='Global', id='WW_TEST_MODEL', name='World Wide Medium Term Test Model',
                                  term='Medium', vendor='Goldman Sachs', version=4, universe_identifier='gsid',
                                  type='Factor')

    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_get', return_value=model)

    # run test
    response = GsRiskModelApi.get_risk_model(model_id)
    GsSession.current._get.assert_called_with('/risk/models/{id}'.format(id=model_id), cls=RiskModel)
    assert response == expected_response


def test_create_risk_model(mocker):
    model = RiskModel.from_dict({
        "coverage": "Global",
        "id": "WW_TEST_MODEL",
        "name": "World Wide Medium Term Test Model",
        "term": "Medium",
        "vendor": "Goldman Sachs",
        "universeIdentifier": "gsid",
        "version": 4,
        "type": "Macro"
    })

    expected_response = RiskModel(coverage='Global', id='WW_TEST_MODEL', name='World Wide Medium Term Test Model',
                                  term='Medium', vendor='Goldman Sachs', version=4, universe_identifier='gsid',
                                  type='Macro')

    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_post', return_value=model)

    # run test
    response = GsRiskModelApi.create_risk_model(model)
    GsSession.current._post.assert_called_with('/risk/models', model, cls=RiskModel)
    assert response == expected_response


def test_update_risk_model(mocker):
    model = RiskModel.from_dict({
        "coverage": "Global",
        "id": "WW_TEST_MODEL",
        "name": "World Wide Medium Term Test Model",
        "term": "Medium",
        "vendor": "Goldman Sachs",
        "RiskModelUniverseIdentifier": "gsid",
        "version": 4
    })

    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_put', return_value=model)

    # run test
    response = GsRiskModelApi.update_risk_model(model)
    GsSession.current._put.assert_called_with('/risk/models/{id}'.format(id='WW_TEST_MODEL'), model, cls=RiskModel)
    assert response == model


def test_delete_risk_model(mocker):
    mock_response = "Deleted Risk Model"

    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_delete', return_value=mock_response)

    # run test
    response = GsRiskModelApi.delete_risk_model('model id')
    GsSession.current._delete.assert_called_with('/risk/models/{id}'.format(id='model id'))
    assert response == mock_response


def test_get_risk_model_calendar(mocker):
    calendar = RiskModelCalendar.from_dict({
        "businessDates": ["2020-01-01", "2020-11-01"]
    })

    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_get', return_value=calendar)

    # run test
    response = GsRiskModelApi.get_risk_model_calendar('id')
    GsSession.current._get.assert_called_with('/risk/models/{id}/calendar'.format(id='id'), cls=RiskModelCalendar)
    assert response == calendar


def test_upload_risk_model_calendar(mocker):
    calendar = RiskModelCalendar.from_dict({
        "businessDates": [
            "2020-01-01",
            "2020-11-01"
        ]
    })

    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_put', return_value=calendar)

    # run test
    response = GsRiskModelApi.upload_risk_model_calendar('WW_TEST_MODEL', calendar)
    GsSession.current._put.assert_called_with('/risk/models/{id}/calendar'.format(id='WW_TEST_MODEL'),
                                              calendar, cls=RiskModelCalendar)
    assert response == calendar


def test_get_risk_model_factors(mocker):
    factors = {'results': [
        Factor.from_dict({
            "type": "Factor",
            "identifier": "Factor1"
        }),
        Factor.from_dict({
            "type": "Category",
            "identifier": "Factor2"
        })
    ],
        'totalResults': 2
    }

    expected_response = [
        Factor(identifier='Factor1', type='Factor'),
        Factor(identifier='Factor2', type='Category')
    ]

    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_get', return_value=factors)

    # run test
    response = GsFactorRiskModelApi.get_risk_model_factors(model_id='id')
    GsSession.current._get.assert_called_with('/risk/models/id/factors', cls=Factor)
    assert response == expected_response


def test_create_risk_model_factor(mocker):
    factor = Factor.from_dict({
        "identifier": "Factor1",
        "type": "Factor"
    })

    expected_response = Factor(identifier='Factor1', type='Factor')

    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_post', return_value=factor)

    # run test
    response = GsFactorRiskModelApi.create_risk_model_factor(model_id='id', factor=factor)
    GsSession.current._post.assert_called_with('/risk/models/id/factors', factor, cls=Factor)
    assert response == expected_response


def test_update_risk_model_factor(mocker):
    factor = Factor.from_dict({
        "identifier": "factor",
        "type": "Factor"
    })

    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_put', return_value=factor)

    # run test
    response = GsFactorRiskModelApi.update_risk_model_factor(model_id='id', factor=factor)
    GsSession.current._put.assert_called_with('/risk/models/{id}/factors/{identifier}'
                                              .format(id='id', identifier='factor'), factor, cls=Factor)
    assert response == factor


def test_get_risk_model_coverage(mocker):
    results = {
        "results": [
            Factor.from_dict({
                "model": "AXUS4S",
                "businessDate": "2020-11-02"
            }),
            Factor.from_dict({
                "model": "AXAU4M",
                "businessDate": "2020-11-03"
            })
        ]
    }

    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_post', return_value=results)

    # run test
    response = GsFactorRiskModelApi.get_risk_model_coverage()
    GsSession.current._post.assert_called_with('/risk/models/coverage', {}, timeout=200)
    assert response == results['results']


def test_upload_risk_model_data(mocker):
    risk_model_data = {
        'date': '2020-02-05',
        'assetData': {
            'universe': ['2407966', '2046251', 'USD'],
            'specificRisk': [12.09, 45.12, 3.09],
            'factorExposure': [{'1': 0.23, '2': 0.023}],
            'historicalBeta': [0.12, 0.45, 1.2]
        },
        'factorData': [{
            'factorId': '1',
            'factorName': 'USD',
            'factorCategory': 'Currency',
            'factorCategoryId': 'CUR'
        }],
        'covarianceMatrix': [[0.089, 0.0123, 0.345]],
        'issuerSpecificCovariance': {
            'universeId1': ['2407966'],
            'universeId2': ['2046251'],
            'covariance': [0.03754]
        },
        'factorPortfolios': {
            'universe': ['2407966', '2046251'],
            'portfolio': [{'factorId': 2, 'weights': [0.25, 0.75]}]
        }
    }

    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_post', return_value='Successfully uploaded')

    # run test
    response = GsFactorRiskModelApi.upload_risk_model_data(model_id='id', model_data=risk_model_data)
    GsSession.current._post.assert_called_with('/risk/models/data/{id}'.format(id='id'), risk_model_data, timeout=200)
    assert response == 'Successfully uploaded'


def test_upload_macro_risk_model_data(mocker):
    macro_risk_model_data = {
        'date': '2022-04-05',
        'assetData': {
            'universe': ["904026", "232128", "905739", "24985", "160444"],
            'specificRisk': [32.9, 61, 17.27, 30, 45.6],
            "factorExposure": [{"1": 0.2, "2": 0.3}, {"1": 0.02, "2": 0.03}, {"1": 0.82, "2": 0.63}, {"1": 6.2, "2": 3},
                               {"1": -6.2, "2": 0.3}],
            "rSquared": [89, 45, 34, 12, 5],
            "fairValueGapPercent": [90, 34, 6, 8, 34],
            "fairValueGapStandardDeviation": [4, 5, 9, 1, 7]
        },
        "factorData": [
            {
                "factorId": "1",
                "factorName": "Factor1",
                "factorCategory": "Category1",
                "factorCategoryId": "Category1",
                "factorReturn": 0.12,
                "factorStandardDeviation": 89,
                "factorZScore": 1.5

            },
            {
                "factorId": "2",
                "factorName": "Factor2",
                "factorCategory": "Category2",
                "factorCategoryId": "Category2",
                "factorReturn": 0.89,
                "factorStandardDeviation": 0.67,
                "factorZScore": -1
            }
        ]
    }
    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_post', return_value='Successfully uploaded')

    # run test
    response = GsFactorRiskModelApi.upload_risk_model_data(model_id='id', model_data=macro_risk_model_data)
    GsSession.current._post.assert_called_with(
        '/risk/models/data/{id}'.format(id='id'), macro_risk_model_data, timeout=200)
    assert response == 'Successfully uploaded'


def test_get_risk_model_data(mocker):
    query = {
        'startDate': '2020-01-01',
        'endDate': '2020-03-03'
    }

    results = {
        'results': [{
            'date': '2020-02-05',
            'assetData': {
                'universe': ['2407966', '2046251', 'USD'],
                'specificRisk': [12.09, 45.12, 3.09],
                'factorExposure': [{'1': 0.23, '2': 0.023}],
                'historicalBeta': [0.12, 0.45, 1.2]
            },
            'factorData': [{
                'factorId': '1',
                'factorName': 'USD',
                'factorCategory': 'Currency',
                'factorCategoryId': 'CUR'
            }],
            'covarianceMatrix': [[0.089, 0.0123, 0.345]],
            'issuerSpecificCovariance': {
                'universeId1': ['2407966'],
                'universeId2': ['2046251'],
                'covariance': [0.03754]
            },
            'factorPortfolios': {
                'universe': ['2407966', '2046251'],
                'portfolio': [{'factorId': 2, 'weights': [0.25, 0.75]}]
            }
        }],
        'totalResults': 1,
        'missingDates': []
    }

    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_post', return_value=results)

    # run test
    response = GsFactorRiskModelApi.get_risk_model_data(model_id='id', start_date=dt.date(2020, 1, 1),
                                                        end_date=dt.date(2020, 3, 3))
    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='id'), query, timeout=200)
    assert response == results


def test_get_r_squared(mocker):
    assets = ["904026", "232128", "24985", "160444"]
    query = {
        'startDate': '2022-04-04',
        'endDate': '2022-04-06',
        'assets': DataAssetsRequest(UniverseIdentifier.gsid, assets),
        'measures': [Measure.R_Squared, Measure.Asset_Universe],
        'limitFactors': False
    }

    r_squared_results = [
        {
            "date": "2022-04-05",
            "assetData": {
                "universe": ["904026", "232128", "24985", "160444"],
                "rSquared": [89.0, 45.0, 12.0, 5.0]
            }
        }
    ]

    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_post', return_value=r_squared_results)

    # run test
    response = GsFactorRiskModelApi.get_risk_model_data(model_id='id', start_date=dt.date(2022, 4, 4),
                                                        end_date=dt.date(2022, 4, 6),
                                                        assets=DataAssetsRequest(UniverseIdentifier.gsid, assets),
                                                        measures=[Measure.R_Squared, Measure.Asset_Universe],
                                                        limit_factors=False)
    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='id'), query, timeout=200)
    assert response == r_squared_results


def test_get_fair_value_gap(mocker):
    assets = ["904026", "232128", "24985", "160444"]
    query = {
        'startDate': '2022-04-04',
        'endDate': '2022-04-06',
        'assets': DataAssetsRequest(UniverseIdentifier.gsid, assets),
        'measures': [Measure.Fair_Value_Gap_Percent, Measure.Fair_Value_Gap_Standard_Deviation,
                     Measure.Asset_Universe],
        'limitFactors': False
    }

    fvg_results = [
        {
            "date": "2022-04-05",
            "assetData": {
                "fairValueGapPercent": [90.0, 34.0, 8.0, 34.0],
                "universe": ["904026", "232128", "24985", "160444"],
                "fairValueGapStandardDeviation": [4.0, 5.0, 1.0, 7.0]
            }
        }
    ]

    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_post', return_value=fvg_results)

    # run test
    response = GsFactorRiskModelApi.get_risk_model_data(model_id='id', start_date=dt.date(2022, 4, 4),
                                                        end_date=dt.date(2022, 4, 6),
                                                        assets=DataAssetsRequest(UniverseIdentifier.gsid, assets),
                                                        measures=[Measure.Fair_Value_Gap_Percent,
                                                                  Measure.Fair_Value_Gap_Standard_Deviation,
                                                                  Measure.Asset_Universe],
                                                        limit_factors=False)
    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='id'), query, timeout=200)
    assert response == fvg_results


def test_get_factor_standard_deviation(mocker):
    assets = ["904026", "232128", "24985", "160444"]
    query = {
        'startDate': '2022-04-04',
        'endDate': '2022-04-06',
        'assets': DataAssetsRequest(UniverseIdentifier.gsid, assets),
        'measures': [Measure.Factor_Standard_Deviation, Measure.Factor_Name, Measure.Factor_Id],
        'limitFactors': False
    }

    factor_standard_deviation_results = [
        {
            "date": "2022-04-05",
            "factorData": [
                {
                    "factorId": "1",
                    "factorStandardDeviation": 89.0,
                    "factorName": "Factor1"
                },
                {
                    "factorId": "2",
                    "factorStandardDeviation": 0.67,
                    "factorName": "Factor2"
                }
            ]
        }
    ]

    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_post', return_value=factor_standard_deviation_results)

    # run test
    response = GsFactorRiskModelApi.get_risk_model_data(model_id='id', start_date=dt.date(2022, 4, 4),
                                                        end_date=dt.date(2022, 4, 6),
                                                        assets=DataAssetsRequest(UniverseIdentifier.gsid, assets),
                                                        measures=[Measure.Factor_Standard_Deviation,
                                                                  Measure.Factor_Name,
                                                                  Measure.Factor_Id],
                                                        limit_factors=False)
    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='id'), query, timeout=200)
    assert response == factor_standard_deviation_results


def test_get_factor_z_score(mocker):
    assets = ["904026", "232128", "24985", "160444"]
    query = {
        'startDate': '2022-04-04',
        'endDate': '2022-04-06',
        'assets': DataAssetsRequest(UniverseIdentifier.gsid, assets),
        'measures': [Measure.Factor_Z_Score, Measure.Factor_Name, Measure.Factor_Id],
        'limitFactors': False
    }

    factor_z_score_results = [
        {
            "date": "2022-04-05",
            "factorData": [
                {
                    "factorId": "1",
                    "factorZScore": 1.5,
                    "factorName": "Factor1"
                },
                {
                    "factorId": "2",
                    "factorZScore": -1.0,
                    "factorName": "Factor2"
                }
            ]
        }
    ]

    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_post', return_value=factor_z_score_results)

    # run test
    response = GsFactorRiskModelApi.get_risk_model_data(model_id='id', start_date=dt.date(2022, 4, 4),
                                                        end_date=dt.date(2022, 4, 6),
                                                        assets=DataAssetsRequest(UniverseIdentifier.gsid, assets),
                                                        measures=[Measure.Factor_Z_Score,
                                                                  Measure.Factor_Name,
                                                                  Measure.Factor_Id],
                                                        limit_factors=False)
    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='id'), query, timeout=200)
    assert response == factor_z_score_results


def test_get_predicted_beta(mocker):
    assets = ["904026", "232128", "24985", "160444"]
    query = {
        'startDate': '2022-04-04',
        'endDate': '2022-04-06',
        'assets': DataAssetsRequest(UniverseIdentifier.gsid, assets),
        'measures': [Measure.Predicted_Beta, Measure.Asset_Universe],
        'limitFactors': False
    }

    predicted_beta_results = [
        {
            "date": "2022-04-05",
            "assetData": {
                "universe": ["904026", "232128", "24985", "160444"],
                "predictedBeta": [0.4, 1.5, 1.2, 0.5]
            }
        }
    ]

    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_post', return_value=predicted_beta_results)

    # run test
    response = GsFactorRiskModelApi.get_risk_model_data(model_id='id', start_date=dt.date(2022, 4, 4),
                                                        end_date=dt.date(2022, 4, 6),
                                                        assets=DataAssetsRequest(UniverseIdentifier.gsid, assets),
                                                        measures=[Measure.Predicted_Beta, Measure.Asset_Universe],
                                                        limit_factors=False)
    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='id'), query, timeout=200)
    assert response == predicted_beta_results


def test_get_global_predicted_beta(mocker):
    assets = ["904026", "232128", "24985", "160444"]
    query = {
        'startDate': '2022-04-04',
        'endDate': '2022-04-06',
        'assets': DataAssetsRequest(UniverseIdentifier.gsid, assets),
        'measures': [Measure.Global_Predicted_Beta, Measure.Asset_Universe],
        'limitFactors': False
    }

    global_predicted_beta_results = [
        {
            "date": "2022-04-05",
            "assetData": {
                "universe": ["904026", "232128", "24985", "160444"],
                "globalPredictedBeta": [0.4, 1.5, 1.2, 0.5]
            }
        }
    ]

    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_post', return_value=global_predicted_beta_results)

    # run test
    response = GsFactorRiskModelApi.get_risk_model_data(model_id='id', start_date=dt.date(2022, 4, 4),
                                                        end_date=dt.date(2022, 4, 6),
                                                        assets=DataAssetsRequest(UniverseIdentifier.gsid, assets),
                                                        measures=[Measure.Global_Predicted_Beta,
                                                                  Measure.Asset_Universe],
                                                        limit_factors=False)
    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='id'), query, timeout=200)
    assert response == global_predicted_beta_results


def test_get_daily_return(mocker):
    assets = ["904026", "232128", "24985", "160444"]
    query = {
        'startDate': '2022-04-04',
        'endDate': '2022-04-06',
        'assets': DataAssetsRequest(UniverseIdentifier.gsid, assets),
        'measures': [Measure.Daily_Return, Measure.Asset_Universe],
        'limitFactors': False
    }

    daily_return_results = [
        {
            "date": "2022-04-05",
            "assetData": {
                "universe": ["904026", "232128", "24985", "160444"],
                "dailyReturn": [0.4, 1.5, 1.2, 0.5]
            }
        }
    ]

    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_post', return_value=daily_return_results)

    # run test
    response = GsFactorRiskModelApi.get_risk_model_data(model_id='id', start_date=dt.date(2022, 4, 4),
                                                        end_date=dt.date(2022, 4, 6),
                                                        assets=DataAssetsRequest(UniverseIdentifier.gsid, assets),
                                                        measures=[Measure.Daily_Return,
                                                                  Measure.Asset_Universe],
                                                        limit_factors=False)
    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='id'), query, timeout=200)
    assert response == daily_return_results


def test_get_specific_return(mocker):
    assets = ["904026", "232128", "24985", "160444"]
    query = {
        'startDate': '2022-04-04',
        'endDate': '2022-04-06',
        'assets': DataAssetsRequest(UniverseIdentifier.gsid, assets),
        'measures': [Measure.Specific_Return, Measure.Asset_Universe],
        'limitFactors': False
    }

    specific_return_resutls = [
        {
            "date": "2022-04-05",
            "assetData": {
                "universe": ["904026", "232128", "24985", "160444"],
                "specificReturn": [0.4, 1.5, 1.2, 0.5]
            }
        }
    ]

    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_post', return_value=specific_return_resutls)

    # run test
    response = GsFactorRiskModelApi.get_risk_model_data(model_id='id', start_date=dt.date(2022, 4, 4),
                                                        end_date=dt.date(2022, 4, 6),
                                                        assets=DataAssetsRequest(UniverseIdentifier.gsid, assets),
                                                        measures=[Measure.Specific_Return,
                                                                  Measure.Asset_Universe],
                                                        limit_factors=False)
    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='id'), query, timeout=200)
    assert response == specific_return_resutls
