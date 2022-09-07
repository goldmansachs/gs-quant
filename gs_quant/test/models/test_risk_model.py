"""
Copyright 2021 Goldman Sachs.
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
import pytest
from unittest import mock

from gs_quant.models.risk_model import FactorRiskModel, MacroRiskModel, ReturnFormat, Unit
from gs_quant.session import *
from gs_quant.target.risk_models import RiskModel as Risk_Model, RiskModelCoverage, RiskModelTerm,\
    RiskModelUniverseIdentifier, RiskModelType, RiskModelDataAssetsRequest as DataAssetsRequest, \
    RiskModelDataMeasure as Measure, RiskModelUniverseIdentifierRequest as UniverseIdentifier
import datetime as dt


empty_entitlements = {
    "execute": [],
    "edit": [],
    "view": [],
    "admin": [],
    "query": [],
    "upload": []
}

mock_risk_model_obj = Risk_Model(RiskModelCoverage.Country,
                                 'model_id',
                                 'Fake Risk Model',
                                 RiskModelTerm.Long,
                                 RiskModelUniverseIdentifier.gsid,
                                 'GS',
                                 1.0,
                                 universe_size=10000,
                                 entitlements=empty_entitlements,
                                 description='Test',
                                 expected_update_time='00:00:00',
                                 type=RiskModelType.Factor
                                 )

mock_macro_risk_model_obj = Risk_Model(coverage=RiskModelCoverage.Country,
                                       id='macro_model_id',
                                       name='Fake Risk Model',
                                       term=RiskModelTerm.Long,
                                       universe_identifier=RiskModelUniverseIdentifier.gsid,
                                       vendor='GS',
                                       version=1.0,
                                       entitlements=empty_entitlements,
                                       description='Test',
                                       expected_update_time='00:00:00',
                                       type=RiskModelType.Macro
                                       )


def mock_risk_model(mocker):
    from gs_quant.session import OAuth2Session
    OAuth2Session.init = mock.MagicMock(return_value=None)
    GsSession.use(Environment.QA, 'client_id', 'secret')
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_post', return_value=mock_risk_model_obj)
    mocker.patch.object(GsSession.current, '_get', return_value=mock_risk_model_obj)
    mocker.patch.object(GsSession.current, '_put', return_value=mock_risk_model_obj)
    return FactorRiskModel.get('model_id')


def mock_macro_risk_model(mocker):
    from gs_quant.session import OAuth2Session
    OAuth2Session.init = mock.MagicMock(return_value=None)
    GsSession.use(Environment.QA, 'client_id', 'secret')
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_post', return_value=mock_macro_risk_model_obj)
    mocker.patch.object(GsSession.current, '_get', return_value=mock_macro_risk_model_obj)
    mocker.patch.object(GsSession.current, '_put', return_value=mock_macro_risk_model_obj)
    return MacroRiskModel.get('macro_model_id')


def test_create_risk_model(mocker):
    mock_risk_model(mocker)
    risk_model_id = 'model_id'
    mocker.patch.object(GsSession.current, '_post', return_value=mock_risk_model_obj)
    new_model = FactorRiskModel(risk_model_id,
                                'Fake Risk Model',
                                RiskModelCoverage.Country,
                                RiskModelTerm.Long,
                                RiskModelUniverseIdentifier.gsid,
                                'GS',
                                0.1,
                                universe_size=10000,
                                entitlements={},
                                description='Test',
                                expected_update_time=dt.datetime.strptime('00:00:00', '%H:%M:%S').time())
    new_model.save()
    assert new_model.id == mock_risk_model_obj.id
    assert new_model.name == mock_risk_model_obj.name
    assert new_model.description == mock_risk_model_obj.description
    assert new_model.term == mock_risk_model_obj.term
    assert new_model.universe_size == mock_risk_model_obj.universe_size
    assert new_model.coverage == mock_risk_model_obj.coverage
    assert new_model.universe_identifier == mock_risk_model_obj.universe_identifier
    assert new_model.expected_update_time == dt.datetime.strptime(
        mock_risk_model_obj.expected_update_time, '%H:%M:%S').time()


def test_update_risk_model_entitlements(mocker):
    new_model = mock_risk_model(mocker)
    new_entitlements = {
        "execute": ['guid:X'],
        "edit": [],
        "view": [],
        "admin": [],
        "query": [],
        "upload": []
    }

    new_model.entitlements = new_entitlements
    new_model.save()
    assert 'guid:X' in new_model.entitlements.get('execute')
    mocker.patch.object(GsSession.current, '_get', return_value=new_model)
    new_model.entitlements = empty_entitlements
    new_model.save()
    new_entitlements = {
        "execute": ['guid:X'],
        "edit": [],
        "view": [],
        "admin": ['guid:XX'],
        "query": [],
        "upload": ['guid:XXX']
    }
    new_model.entitlements = new_entitlements
    new_model.save()
    mocker.patch.object(GsSession.current, '_get', return_value=new_model)
    assert 'guid:X' in new_model.entitlements.get('execute')
    assert 'guid:XX' in new_model.entitlements.get('admin')
    assert 'guid:XXX' in new_model.entitlements.get('upload')


def test_update_risk_model(mocker):
    new_model = mock_risk_model(mocker)

    new_model.term = RiskModelTerm.Short
    new_model.save()
    mocker.patch.object(GsSession.current, '_get', return_value=new_model)
    assert new_model.term == RiskModelTerm.Short

    new_model.description = 'Test risk model'
    new_model.save()
    mocker.patch.object(GsSession.current, '_get', return_value=new_model)
    assert new_model.description == 'Test risk model'

    new_model.vendor = 'GS'
    new_model.save()
    mocker.patch.object(GsSession.current, '_get', return_value=new_model)
    assert new_model.vendor == 'GS'

    new_model.term = RiskModelTerm.Medium
    new_model.save()
    mocker.patch.object(GsSession.current, '_get', return_value=new_model)
    assert new_model.term == RiskModelTerm.Medium

    new_model.version = 0.1
    new_model.save()
    mocker.patch.object(GsSession.current, '_get', return_value=new_model)
    assert new_model.version == 0.1

    new_model.universe_size = 10000
    new_model.save()
    mocker.patch.object(GsSession.current, '_get', return_value=new_model)
    assert new_model.universe_size == 10000

    new_model.coverage = RiskModelCoverage.Global
    new_model.save()
    mocker.patch.object(GsSession.current, '_get', return_value=new_model)
    assert new_model.coverage == RiskModelCoverage.Global

    new_model.name = 'TEST RISK MODEL'
    new_model.save()
    mocker.patch.object(GsSession.current, '_get', return_value=new_model)
    assert new_model.name == 'TEST RISK MODEL'

    new_model.expected_update_time = dt.time(1, 0, 0)
    new_model.save()
    mocker.patch.object(GsSession.current, '_get', return_value=new_model)
    assert new_model.expected_update_time == dt.time(1, 0, 0)

    new_model.type = RiskModelType.Thematic
    new_model.save()
    mocker.patch.object(GsSession.current, '_get', return_value=new_model)
    assert new_model.type == RiskModelType.Thematic


def test_get_r_squared(mocker):
    macro_model = mock_macro_risk_model(mocker)
    universe = ["904026", "232128", "24985", "160444"]
    query = {
        'startDate': '2022-04-04',
        'endDate': '2022-04-06',
        'assets': DataAssetsRequest(UniverseIdentifier.gsid, universe),
        'measures': [Measure.R_Squared, Measure.Asset_Universe],
        'limitFactors': False
    }

    results = {
        'missingDates': ['2022-04-04', '2022-04-06'],
        'results': [
            {
                "date": "2022-04-05",
                "assetData": {
                    "universe": ["904026", "232128", "24985", "160444"],
                    "rSquared": [89.0, 45.0, 12.0, 5.0]
                }
            }
        ],
        'totalResults': 1
    }

    r_squared_response = {
        '160444': {'2022-04-05': 5.0},
        '232128': {'2022-04-05': 45.0},
        '24985': {'2022-04-05': 12.0},
        '904026': {'2022-04-05': 89.0}
    }

    mocker.patch.object(GsSession.current, '_post', return_value=results)

    # run test
    response = macro_model.get_r_squared(start_date=dt.date(2022, 4, 4),
                                         end_date=dt.date(2022, 4, 6),
                                         assets=DataAssetsRequest(UniverseIdentifier.gsid, universe),
                                         format=ReturnFormat.JSON)

    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='macro_model_id'),
                                               query, timeout=200)
    assert response == r_squared_response


def test_get_fair_value_gap_standard_deviation(mocker):
    macro_model = mock_macro_risk_model(mocker)
    universe = ["904026", "232128", "24985", "160444"]
    query = {
        'startDate': '2022-04-04',
        'endDate': '2022-04-06',
        'assets': DataAssetsRequest(UniverseIdentifier.gsid, universe),
        'measures': [Measure.Fair_Value_Gap_Standard_Deviation, Measure.Asset_Universe],
        'limitFactors': False
    }

    results = {
        'missingDates': ['2022-04-04', '2022-04-06'],
        'results': [
            {
                "date": "2022-04-05",
                "assetData": {
                    "universe": ["904026", "232128", "24985", "160444"],
                    "fairValueGapStandardDeviation": [4.0, 5.0, 1.0, 7.0]
                }
            }
        ],
        'totalResults': 1
    }

    fvg_response = {
        '160444': {'2022-04-05': 7.0},
        '232128': {'2022-04-05': 5.0},
        '24985': {'2022-04-05': 1.0},
        '904026': {'2022-04-05': 4.0}
    }

    mocker.patch.object(GsSession.current, '_post', return_value=results)
    response = macro_model.get_fair_value_gap(start_date=dt.date(2022, 4, 4),
                                              end_date=dt.date(2022, 4, 6),
                                              assets=DataAssetsRequest(UniverseIdentifier.gsid, universe),
                                              format=ReturnFormat.JSON)
    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='macro_model_id'),
                                               query, timeout=200)
    assert response == fvg_response


def test_get_fair_value_gap_percent(mocker):
    macro_model = mock_macro_risk_model(mocker)
    universe = ["904026", "232128", "24985", "160444"]
    query = {
        'startDate': '2022-04-04',
        'endDate': '2022-04-06',
        'assets': DataAssetsRequest(UniverseIdentifier.gsid, universe),
        'measures': [Measure.Fair_Value_Gap_Percent, Measure.Asset_Universe],
        'limitFactors': False
    }

    results = {
        'missingDates': ['2022-04-04', '2022-04-06'],
        'results': [
            {
                "date": "2022-04-05",
                "assetData": {
                    "universe": ["904026", "232128", "24985", "160444"],
                    "fairValueGapPercent": [90.0, 34.0, 8.0, 34.0]
                }
            }
        ],
        'totalResults': 1
    }

    fvg_response = {
        '160444': {'2022-04-05': 34.0},
        '232128': {'2022-04-05': 34.0},
        '24985': {'2022-04-05': 8.0},
        '904026': {'2022-04-05': 90.0}
    }

    mocker.patch.object(GsSession.current, '_post', return_value=results)
    response = macro_model.get_fair_value_gap(start_date=dt.date(2022, 4, 4),
                                              end_date=dt.date(2022, 4, 6),
                                              assets=DataAssetsRequest(UniverseIdentifier.gsid, universe),
                                              fair_value_gap_unit=Unit.PERCENT,
                                              format=ReturnFormat.JSON)
    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='macro_model_id'),
                                               query, timeout=200)
    assert response == fvg_response


def test_get_factor_standard_deviation(mocker):
    macro_model = mock_macro_risk_model(mocker)
    universe = ["904026", "232128", "24985", "160444"]
    query = {
        'startDate': '2022-04-04',
        'endDate': '2022-04-06',
        'assets': DataAssetsRequest(UniverseIdentifier.gsid, universe),
        'measures': [Measure.Factor_Standard_Deviation, Measure.Factor_Name, Measure.Factor_Id,
                     Measure.Universe_Factor_Exposure, Measure.Asset_Universe],
        'limitFactors': True
    }

    results = {
        'missingDates': ['2022-04-04', '2022-04-06'],
        'results': [
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
                ],
                'assetData': {
                    'factorExposure': [{'1': 0.2, '2': 0.3}, {'1': 0.02, '2': 0.03},
                                       {'1': 6.2, '2': 3.0}, {'1': -6.2, '2': 0.3}],
                    'universe': ['904026', '232128', '24985', '160444']
                }
            }
        ],
        'totalResults': 1
    }

    factor_standard_deviation_response = {
        'Factor1': {'2022-04-05': 89.0},
        'Factor2': {'2022-04-05': 0.67}
    }

    mocker.patch.object(GsSession.current, '_post', return_value=results)

    # run test
    response = macro_model.get_factor_standard_deviation(start_date=dt.date(2022, 4, 4),
                                                         end_date=dt.date(2022, 4, 6),
                                                         assets=DataAssetsRequest(UniverseIdentifier.gsid, universe),
                                                         format=ReturnFormat.JSON)

    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='macro_model_id'),
                                               query, timeout=200)
    assert response == factor_standard_deviation_response


def test_get_factor_z_score(mocker):
    macro_model = mock_macro_risk_model(mocker)
    universe = ["904026", "232128", "24985", "160444"]
    query = {
        'startDate': '2022-04-04',
        'endDate': '2022-04-06',
        'assets': DataAssetsRequest(UniverseIdentifier.gsid, universe),
        'measures': [Measure.Factor_Z_Score, Measure.Factor_Name, Measure.Factor_Id,
                     Measure.Universe_Factor_Exposure, Measure.Asset_Universe],
        'limitFactors': True
    }

    results = {
        'missingDates': ['2022-04-04', '2022-04-06'],
        'results': [
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
                ],
                'assetData': {
                    'factorExposure': [{'1': 0.2, '2': 0.3}, {'1': 0.02, '2': 0.03},
                                       {'1': 6.2, '2': 3.0}, {'1': -6.2, '2': 0.3}],
                    'universe': ['904026', '232128', '24985', '160444']
                }
            }
        ],
        'totalResults': 1
    }

    factor_z_score_response = {
        'Factor1': {'2022-04-05': 1.5},
        'Factor2': {'2022-04-05': -1.0}
    }

    mocker.patch.object(GsSession.current, '_post', return_value=results)

    # run test
    response = macro_model.get_factor_z_score(start_date=dt.date(2022, 4, 4),
                                              end_date=dt.date(2022, 4, 6),
                                              assets=DataAssetsRequest(UniverseIdentifier.gsid, universe),
                                              format=ReturnFormat.JSON)
    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='macro_model_id'),
                                               query, timeout=200)
    assert response == factor_z_score_response


def test_get_predicted_beta(mocker):
    model = mock_risk_model(mocker)
    universe = ["904026", "232128", "24985", "160444"]
    query = {
        'startDate': '2022-04-04',
        'endDate': '2022-04-06',
        'assets': DataAssetsRequest(UniverseIdentifier.gsid, universe),
        'measures': [Measure.Predicted_Beta, Measure.Asset_Universe],
        'limitFactors': False
    }

    results = {
        'missingDates': ['2022-04-04', '2022-04-06'],
        'results': [
            {
                "date": "2022-04-05",
                "assetData": {
                    "universe": ["904026", "232128", "24985", "160444"],
                    "predictedBeta": [0.4, 1.5, 1.2, 0.5]
                }
            }
        ],
        'totalResults': 1
    }

    predicted_beta_response = {
        '160444': {'2022-04-05': 0.5},
        '232128': {'2022-04-05': 1.5},
        '24985': {'2022-04-05': 1.2},
        '904026': {'2022-04-05': 0.4}
    }

    mocker.patch.object(GsSession.current, '_post', return_value=results)

    # run test
    response = model.get_predicted_beta(start_date=dt.date(2022, 4, 4),
                                        end_date=dt.date(2022, 4, 6),
                                        assets=DataAssetsRequest(UniverseIdentifier.gsid, universe),
                                        format=ReturnFormat.JSON)

    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='model_id'),
                                               query, timeout=200)
    assert response == predicted_beta_response


def test_get_global_predicted_beta(mocker):
    model = mock_risk_model(mocker)
    universe = ["904026", "232128", "24985", "160444"]
    query = {
        'startDate': '2022-04-04',
        'endDate': '2022-04-06',
        'assets': DataAssetsRequest(UniverseIdentifier.gsid, universe),
        'measures': [Measure.Global_Predicted_Beta, Measure.Asset_Universe],
        'limitFactors': False
    }

    results = {
        'missingDates': ['2022-04-04', '2022-04-06'],
        'results': [
            {
                "date": "2022-04-05",
                "assetData": {
                    "universe": ["904026", "232128", "24985", "160444"],
                    "globalPredictedBeta": [0.4, 1.5, 1.2, 0.5]
                }
            }
        ],
        'totalResults': 1
    }

    global_predicted_beta_response = {
        '160444': {'2022-04-05': 0.5},
        '232128': {'2022-04-05': 1.5},
        '24985': {'2022-04-05': 1.2},
        '904026': {'2022-04-05': 0.4}
    }

    mocker.patch.object(GsSession.current, '_post', return_value=results)

    # run test
    response = model.get_global_predicted_beta(start_date=dt.date(2022, 4, 4),
                                               end_date=dt.date(2022, 4, 6),
                                               assets=DataAssetsRequest(UniverseIdentifier.gsid, universe),
                                               format=ReturnFormat.JSON)

    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='model_id'),
                                               query, timeout=200)
    assert response == global_predicted_beta_response


def test_get_estimation_universe_weights(mocker):
    model = mock_risk_model(mocker)
    universe = ["904026", "232128", "24985", "160444"]
    query = {
        'startDate': '2022-04-04',
        'endDate': '2022-04-06',
        'assets': DataAssetsRequest(UniverseIdentifier.gsid, universe),
        'measures': [Measure.Estimation_Universe_Weight, Measure.Asset_Universe],
        'limitFactors': False
    }

    results = {
        'missingDates': ['2022-04-04', '2022-04-06'],
        'results': [
            {
                "date": "2022-04-05",
                "assetData": {
                    "universe": ["904026", "232128", "24985", "160444"],
                    "estimationUniverseWeight": [0.4, None, None, 0.6]
                }
            }
        ],
        'totalResults': 1
    }

    estu_response = {
        '160444': {'2022-04-05': 0.6},
        '232128': {'2022-04-05': None},
        '24985': {'2022-04-05': None},
        '904026': {'2022-04-05': 0.4}
    }

    mocker.patch.object(GsSession.current, '_post', return_value=results)

    # run test
    response = model.get_estimation_universe_weights(start_date=dt.date(2022, 4, 4),
                                                     end_date=dt.date(2022, 4, 6),
                                                     assets=DataAssetsRequest(UniverseIdentifier.gsid, universe),
                                                     format=ReturnFormat.JSON)

    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='model_id'),
                                               query, timeout=200)
    assert response == estu_response


def test_get_daily_return(mocker):
    model = mock_risk_model(mocker)
    universe = ["904026", "232128", "24985", "160444"]
    query = {
        'startDate': '2022-04-04',
        'endDate': '2022-04-06',
        'assets': DataAssetsRequest(UniverseIdentifier.gsid, universe),
        'measures': [Measure.Daily_Return, Measure.Asset_Universe],
        'limitFactors': False
    }

    results = {
        'missingDates': ['2022-04-04', '2022-04-06'],
        'results': [
            {
                "date": "2022-04-05",
                "assetData": {
                    "universe": ["904026", "232128", "24985", "160444"],
                    "dailyReturn": [-0.4, -1.5, 1.2, 0.5]
                }
            }
        ],
        'totalResults': 1
    }

    daily_return_response = {
        '160444': {'2022-04-05': 0.5},
        '232128': {'2022-04-05': -1.5},
        '24985': {'2022-04-05': 1.2},
        '904026': {'2022-04-05': -0.4}
    }

    mocker.patch.object(GsSession.current, '_post', return_value=results)

    # run test
    response = model.get_daily_return(start_date=dt.date(2022, 4, 4),
                                      end_date=dt.date(2022, 4, 6),
                                      assets=DataAssetsRequest(UniverseIdentifier.gsid, universe),
                                      format=ReturnFormat.JSON)

    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='model_id'),
                                               query, timeout=200)
    assert response == daily_return_response


def test_get_specific_return(mocker):
    model = mock_risk_model(mocker)
    universe = ["904026", "232128", "24985", "160444"]
    query = {
        'startDate': '2022-04-04',
        'endDate': '2022-04-06',
        'assets': DataAssetsRequest(UniverseIdentifier.gsid, universe),
        'measures': [Measure.Specific_Return, Measure.Asset_Universe],
        'limitFactors': False
    }

    results = {
        'missingDates': ['2022-04-04', '2022-04-06'],
        'results': [
            {
                "date": "2022-04-05",
                "assetData": {
                    "universe": ["904026", "232128", "24985", "160444"],
                    "specificReturn": [0.5, 1.6, 1.4, 0.7]
                }
            }
        ],
        'totalResults': 1
    }

    specific_return_response = {
        '160444': {'2022-04-05': 0.7},
        '232128': {'2022-04-05': 1.6},
        '24985': {'2022-04-05': 1.4},
        '904026': {'2022-04-05': 0.5}
    }

    mocker.patch.object(GsSession.current, '_post', return_value=results)

    # run test
    response = model.get_specific_return(start_date=dt.date(2022, 4, 4),
                                         end_date=dt.date(2022, 4, 6),
                                         assets=DataAssetsRequest(UniverseIdentifier.gsid, universe),
                                         format=ReturnFormat.JSON)

    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='model_id'),
                                               query, timeout=200)
    assert response == specific_return_response


if __name__ == "__main__":
    pytest.main([__file__])
