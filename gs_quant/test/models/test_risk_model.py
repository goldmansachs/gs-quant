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

from pandas._testing import assert_frame_equal

from gs_quant.models.risk_model_utils import get_optional_data_as_dataframe, _map_measure_to_field_name
from gs_quant.target.common import Currency

from gs_quant.models.risk_model import FactorRiskModel, MacroRiskModel, ReturnFormat, Unit
from gs_quant.session import *
from gs_quant.target.risk_models import RiskModel as Risk_Model, RiskModelCoverage, RiskModelTerm, \
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


@pytest.mark.parametrize("statistical_measure, fieldKey", [
    (Measure.Factor_Mean, _map_measure_to_field_name(Measure.Factor_Mean)),
    (Measure.Factor_Cross_Sectional_Mean, _map_measure_to_field_name(Measure.Factor_Cross_Sectional_Mean)),
    (Measure.Factor_Standard_Deviation, _map_measure_to_field_name(Measure.Factor_Standard_Deviation)),
    (Measure.Factor_Cross_Sectional_Standard_Deviation,
     _map_measure_to_field_name(Measure.Factor_Cross_Sectional_Standard_Deviation))
])
def test_get_statistical_factor_data(mocker, statistical_measure, fieldKey):
    risk_model = mock_risk_model(mocker)
    universe = ["904026", "232128", "24985", "160444"]
    query = {
        'startDate': '2022-04-04',
        'endDate': '2022-04-06',
        'assets': DataAssetsRequest(UniverseIdentifier.gsid, universe),
        'measures': [statistical_measure, Measure.Factor_Name, Measure.Factor_Id,
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
                        f"{fieldKey}": 89.0,
                        "factorName": "Factor1"
                    },
                    {
                        "factorId": "2",
                        f"{fieldKey}": 0.67,
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

    expected_response = {
        'Factor1': {'2022-04-05': 89.0},
        'Factor2': {'2022-04-05': 0.67}
    }

    kwargs = {
        "start_date": dt.date(2022, 4, 4),
        "end_date": dt.date(2022, 4, 6),
        "assets": DataAssetsRequest(UniverseIdentifier.gsid, universe),
        "format": ReturnFormat.JSON
    }

    field_key_to_getter_ref = {
        _map_measure_to_field_name(Measure.Factor_Mean): risk_model.get_factor_mean,
        _map_measure_to_field_name(Measure.Factor_Cross_Sectional_Mean): risk_model.get_factor_cross_sectional_mean,
        _map_measure_to_field_name(Measure.Factor_Standard_Deviation): risk_model.get_factor_standard_deviation,
        _map_measure_to_field_name(
            Measure.Factor_Cross_Sectional_Standard_Deviation): risk_model.get_factor_cross_sectional_standard_deviation
    }

    mocker.patch.object(GsSession.current, '_post', return_value=results)

    actual_response = field_key_to_getter_ref[fieldKey](**kwargs)
    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='model_id'),
                                               query, timeout=200)

    assert actual_response == expected_response


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


@pytest.mark.parametrize("aws_upload", [True, False])
def test_upload_risk_model_data(mocker, aws_upload):
    model = mock_risk_model(mocker)
    risk_model_data = {
        'date': '2023-04-14',
        'assetData': {
            'universe': ['2407966', '2046251', 'USD'],
            'specificRisk': [12.09, 45.12, 3.09],
            'factorExposure': [
                {'1': 0.23, '2': 0.023},
                {'1': 0.23},
                {'3': 0.23, '2': 0.023}
            ],
            'totalRisk': [0.12, 0.45, 1.2]
        },
        'factorData': [
            {
                'factorId': '1',
                'factorName': 'USD',
                'factorCategory': 'Currency',
                'factorCategoryId': 'CUR'
            },
            {
                'factorId': '2',
                'factorName': 'ST',
                'factorCategory': 'ST',
                'factorCategoryId': 'ST'
            },
            {
                'factorId': '3',
                'factorName': 'IND',
                'factorCategory': 'IND',
                'factorCategoryId': 'IND'
            }
        ],
        'covarianceMatrix': [[0.089, 0.0123, 0.345],
                             [0.0123, 3.45, 0.345],
                             [0.345, 0.345, 1.23]],
        'issuerSpecificCovariance': {
            'universeId1': ['2407966'],
            'universeId2': ['2046251'],
            'covariance': [0.03754]
        },
        'factorPortfolios': {
            'universe': ['2407966', '2046251'],
            'portfolio': [{'factorId': 1, 'weights': [0.25, 0.75]},
                          {'factorId': 2, 'weights': [0.25, 0.75]},
                          {'factorId': 3, 'weights': [0.25, 0.75]}]
        }
    }

    base_url = f"/risk/models/data/{model.id}?partialUpload=true"
    date = risk_model_data.get("date")
    max_asset_batch_size = 2

    batched_asset_data = [
        {"assetData": {key: value[i:i + max_asset_batch_size] for key, value in
                       risk_model_data.get("assetData").items()}, "date": date,
         } for i in range(0, len(risk_model_data.get("assetData").get("universe")), max_asset_batch_size)
    ]

    max_asset_batch_size //= 2
    batched_factor_portfolios = [
        {"factorPortfolios": {key: (value[i:i + max_asset_batch_size] if key in "universe" else
                                    [{"factorId": factor_weights.get("factorId"),
                                      "weights": factor_weights.get("weights")[i:i + max_asset_batch_size]} for
                                     factor_weights in
                                     value])
                              for key, value in risk_model_data.get("factorPortfolios").items()},
         "date": date
         } for i in range(0, len(risk_model_data.get("factorPortfolios").get("universe")), max_asset_batch_size)
    ]

    expected_factor_data_calls = [
        mock.call(f"{base_url}{'&awsUpload=true' if aws_upload else ''}",
                  {"date": date, "factorData": risk_model_data.get("factorData"),
                   "covarianceMatrix": risk_model_data.get("covarianceMatrix")}, timeout=200)
    ]

    expected_asset_data_calls = []
    for batch_num, batch_asset_payload in enumerate(batched_asset_data):
        final_upload_flag = 'true' if batch_num == len(batched_asset_data) - 1 else 'false'
        expected_asset_data_calls.append(
            mock.call(f"{base_url}&finalUpload={final_upload_flag}{'&awsUpload=true' if aws_upload else ''}",
                      batch_asset_payload, timeout=200)
        )

    expected_factor_portfolios_data_calls = []
    for batch_num, batched_fp_payload in enumerate(batched_factor_portfolios):
        final_upload_flag = 'true' if batch_num == len(batched_factor_portfolios) - 1 else 'false'
        expected_factor_portfolios_data_calls.append(
            mock.call(f"{base_url}&finalUpload={final_upload_flag}{'&awsUpload=true' if aws_upload else ''}",
                      batched_fp_payload, timeout=200)
        )

    expected_isc_data_calls = [
        mock.call(f"{base_url}&finalUpload=true{'&awsUpload=true' if aws_upload else ''}",
                  {"issuerSpecificCovariance": risk_model_data.get("issuerSpecificCovariance"), "date": date},
                  timeout=200)
    ]

    expected_calls = (expected_factor_data_calls + expected_asset_data_calls + expected_isc_data_calls +
                      expected_factor_portfolios_data_calls)

    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_post', return_value='Upload Successful')

    max_asset_batch_size = 2
    model.upload_data(risk_model_data, max_asset_batch_size=max_asset_batch_size, aws_upload=aws_upload)

    call_args_list = GsSession.current._post.call_args_list

    assert len(call_args_list) == len(expected_calls)
    assert call_args_list == expected_calls

    GsSession.current._post.assert_has_calls(expected_calls, any_order=False)


@pytest.mark.parametrize("days", [0, 30, 60, 90])
def test_get_bid_ask_spread(mocker, days):
    model = mock_risk_model(mocker)

    universe = ["2046251", "2588173"]
    assets = DataAssetsRequest(UniverseIdentifier.sedol, universe)
    measure_to_query = Measure.Bid_Ask_Spread if not days else Measure[f'Bid_Ask_Spread_{days}d']
    query = {
        'startDate': '2022-04-05',
        'endDate': '2022-04-05',
        'assets': assets,
        'measures': [measure_to_query, Measure.Asset_Universe],
        'limitFactors': False
    }

    results = {
        'results': [
            {
                "date": "2022-04-05",
                "assetData": {
                    "universe": ["2046251", "2588173"],
                    f"bidAskSpread{'' if days == 0 else f'{days}d'}": [0.5, 1.6]
                }
            }
        ],
        'totalResults': 1
    }

    bid_ask_spread_response = {
        '2588173': {'2022-04-05': 1.6},
        '2046251': {'2022-04-05': 0.5}
    }

    mocker.patch.object(GsSession.current, '_post', return_value=results)

    # run test
    response = model.get_bid_ask_spread(start_date=dt.date(2022, 4, 5),
                                        end_date=dt.date(2022, 4, 5),
                                        days=days,
                                        assets=assets,
                                        format=ReturnFormat.JSON)

    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='model_id'),
                                               query, timeout=200)
    assert response == bid_ask_spread_response


@pytest.mark.parametrize("days", [0, 30, 60, 90])
def test_get_trading_volume(mocker, days):
    model = mock_risk_model(mocker)

    universe = ["2046251", "2588173"]
    assets = DataAssetsRequest(UniverseIdentifier.sedol, universe)
    measure_to_query = Measure.Trading_Volume if not days else Measure[f'Trading_Volume_{days}d']
    query = {
        'startDate': '2022-04-05',
        'endDate': '2022-04-05',
        'assets': assets,
        'measures': [measure_to_query, Measure.Asset_Universe],
        'limitFactors': False
    }

    results = {
        'results': [
            {
                "date": "2022-04-05",
                "assetData": {
                    "universe": ["2046251", "2588173"],
                    f"tradingVolume{'' if days == 0 else f'{days}d'}": [0.5, 1.6]
                }
            }
        ],
        'totalResults': 1
    }

    trading_volume_response = {
        '2588173': {'2022-04-05': 1.6},
        '2046251': {'2022-04-05': 0.5}
    }

    mocker.patch.object(GsSession.current, '_post', return_value=results)

    # run test
    response = model.get_trading_volume(start_date=dt.date(2022, 4, 5),
                                        end_date=dt.date(2022, 4, 5),
                                        days=days,
                                        assets=assets,
                                        format=ReturnFormat.JSON)

    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='model_id'),
                                               query, timeout=200)
    assert response == trading_volume_response


@pytest.mark.parametrize("days", [0, 30])
def test_get_traded_value(mocker, days):
    model = mock_risk_model(mocker)

    universe = ["2046251", "2588173"]
    assets = DataAssetsRequest(UniverseIdentifier.sedol, universe)
    measure_to_query = Measure.Traded_Value_30d if not days else Measure[f'Traded_Value_{days}d']
    query = {
        'startDate': '2022-04-05',
        'endDate': '2022-04-05',
        'assets': assets,
        'measures': [measure_to_query, Measure.Asset_Universe],
        'limitFactors': False
    }

    results = {
        'results': [
            {
                "date": "2022-04-05",
                "assetData": {
                    "universe": ["2046251", "2588173"],
                    "tradedValue30d": [0.5, 1.6]
                }
            }
        ],
        'totalResults': 1
    }

    trading_value_30d_response = {
        '2588173': {'2022-04-05': 1.6},
        '2046251': {'2022-04-05': 0.5}
    }

    mocker.patch.object(GsSession.current, '_post', return_value=results)

    # run test
    response = model.get_traded_value(start_date=dt.date(2022, 4, 5),
                                      end_date=dt.date(2022, 4, 5),
                                      days=days,
                                      assets=assets,
                                      format=ReturnFormat.JSON)

    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='model_id'),
                                               query, timeout=200)
    assert response == trading_value_30d_response


@pytest.mark.parametrize("days", [0, 30, 60, 90])
def test_get_composite_volume(mocker, days):
    model = mock_risk_model(mocker)

    universe = ["2046251", "2588173"]
    assets = DataAssetsRequest(UniverseIdentifier.sedol, universe)
    measure_to_query = Measure.Composite_Volume if not days else Measure[f'Composite_Volume_{days}d']
    query = {
        'startDate': '2022-04-05',
        'endDate': '2022-04-05',
        'assets': assets,
        'measures': [measure_to_query, Measure.Asset_Universe],
        'limitFactors': False
    }

    results = {
        'results': [
            {
                "date": "2022-04-05",
                "assetData": {
                    "universe": ["2046251", "2588173"],
                    f"compositeVolume{'' if days == 0 else f'{days}d'}": [0.5, 1.6]
                }
            }
        ],
        'totalResults': 1
    }

    composite_volume_response = {
        '2588173': {'2022-04-05': 1.6},
        '2046251': {'2022-04-05': 0.5}
    }

    mocker.patch.object(GsSession.current, '_post', return_value=results)

    # run test
    response = model.get_composite_volume(start_date=dt.date(2022, 4, 5),
                                          end_date=dt.date(2022, 4, 5),
                                          days=days,
                                          assets=assets,
                                          format=ReturnFormat.JSON)

    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='model_id'),
                                               query, timeout=200)
    assert response == composite_volume_response


@pytest.mark.parametrize("days", [0, 30])
def test_get_composite_value(mocker, days):
    model = mock_risk_model(mocker)

    universe = ["2046251", "2588173"]
    assets = DataAssetsRequest(UniverseIdentifier.sedol, universe)
    measure_to_query = Measure.Composite_Value_30d if not days else Measure[f'Composite_Value_{days}d']
    query = {
        'startDate': '2022-04-05',
        'endDate': '2022-04-05',
        'assets': assets,
        'measures': [measure_to_query, Measure.Asset_Universe],
        'limitFactors': False
    }

    results = {
        'results': [
            {
                "date": "2022-04-05",
                "assetData": {
                    "universe": ["2046251", "2588173"],
                    "compositeValue30d": [0.5, 1.6]
                }
            }
        ],
        'totalResults': 1
    }

    composite_value_response = {
        '2588173': {'2022-04-05': 1.6},
        '2046251': {'2022-04-05': 0.5}
    }

    mocker.patch.object(GsSession.current, '_post', return_value=results)

    # run test
    response = model.get_composite_value(start_date=dt.date(2022, 4, 5),
                                         end_date=dt.date(2022, 4, 5),
                                         days=days,
                                         assets=assets,
                                         format=ReturnFormat.JSON)

    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='model_id'),
                                               query, timeout=200)
    assert response == composite_value_response


def test_get_issuer_market_cap(mocker):
    model = mock_risk_model(mocker)

    universe = ["2046251", "2588173"]
    assets = DataAssetsRequest(UniverseIdentifier.sedol, universe)
    query = {
        'startDate': '2022-04-05',
        'endDate': '2022-04-05',
        'assets': assets,
        'measures': [Measure.Issuer_Market_Cap, Measure.Asset_Universe],
        'limitFactors': False
    }

    results = {
        'results': [
            {
                "date": "2022-04-05",
                "assetData": {
                    "universe": ["2046251", "2588173"],
                    "issuerMarketCap": [1000000000, 2000000000]
                }
            }
        ],
        'totalResults': 1
    }

    issuer_market_cap_response = {
        '2588173': {'2022-04-05': 2000000000},
        '2046251': {'2022-04-05': 1000000000}
    }

    mocker.patch.object(GsSession.current, '_post', return_value=results)

    # run test
    response = model.get_issuer_market_cap(start_date=dt.date(2022, 4, 5),
                                           end_date=dt.date(2022, 4, 5),
                                           assets=assets,
                                           format=ReturnFormat.JSON)

    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='model_id'),
                                               query, timeout=200)
    assert response == issuer_market_cap_response


def test_get_asset_price(mocker):
    model = mock_risk_model(mocker)

    universe = ["2046251", "2588173"]
    assets = DataAssetsRequest(UniverseIdentifier.sedol, universe)
    query = {
        'startDate': '2022-04-05',
        'endDate': '2022-04-05',
        'assets': assets,
        'measures': [Measure.Price, Measure.Asset_Universe],
        'limitFactors': False
    }

    results = {
        'results': [
            {
                "date": "2022-04-05",
                "assetData": {
                    "universe": ["2046251", "2588173"],
                    "price": [100, 200]
                }
            }
        ],
        'totalResults': 1
    }

    price_response = {
        '2588173': {'2022-04-05': 200},
        '2046251': {'2022-04-05': 100}
    }

    mocker.patch.object(GsSession.current, '_post', return_value=results)

    # run test
    response = model.get_asset_price(start_date=dt.date(2022, 4, 5),
                                     end_date=dt.date(2022, 4, 5),
                                     assets=assets,
                                     format=ReturnFormat.JSON)

    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='model_id'),
                                               query, timeout=200)
    assert response == price_response


def test_get_asset_capitalization(mocker):
    model = mock_risk_model(mocker)

    universe = ["2046251", "2588173"]
    assets = DataAssetsRequest(UniverseIdentifier.sedol, universe)
    query = {
        'startDate': '2022-04-05',
        'endDate': '2022-04-05',
        'assets': assets,
        'measures': [Measure.Capitalization, Measure.Asset_Universe],
        'limitFactors': False
    }

    results = {
        'results': [
            {
                "date": "2022-04-05",
                "assetData": {
                    "universe": ["2046251", "2588173"],
                    "capitalization": [1000000000, 2000000000]
                }
            }
        ],
        'totalResults': 1
    }

    capitalization_response = {
        '2588173': {'2022-04-05': 2000000000},
        '2046251': {'2022-04-05': 1000000000}
    }

    mocker.patch.object(GsSession.current, '_post', return_value=results)

    # run test
    response = model.get_asset_capitalization(start_date=dt.date(2022, 4, 5),
                                              end_date=dt.date(2022, 4, 5),
                                              assets=assets,
                                              format=ReturnFormat.JSON)

    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='model_id'),
                                               query, timeout=200)
    assert response == capitalization_response


def test_get_currency(mocker):
    model = mock_risk_model(mocker)

    universe = ["2046251", "2588173"]
    assets = DataAssetsRequest(UniverseIdentifier.sedol, universe)
    query = {
        'startDate': '2022-04-05',
        'endDate': '2022-04-05',
        'assets': assets,
        'measures': [Measure.Currency, Measure.Asset_Universe],
        'limitFactors': False
    }

    results = {
        'results': [
            {
                "date": "2022-04-05",
                "assetData": {
                    "universe": ["2046251", "2588173"],
                    "currency": ["USD", "GBP"]
                }
            }
        ],
        'totalResults': 1
    }

    currency_response = {
        '2588173': {'2022-04-05': "GBP"},
        '2046251': {'2022-04-05': "USD"}
    }

    mocker.patch.object(GsSession.current, '_post', return_value=results)

    # run test
    response = model.get_currency(start_date=dt.date(2022, 4, 5),
                                  end_date=dt.date(2022, 4, 5),
                                  assets=assets,
                                  format=ReturnFormat.JSON)

    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='model_id'),
                                               query, timeout=200)
    assert response == currency_response


def test_get_unadjusted_specific_risk(mocker):
    model = mock_risk_model(mocker)

    universe = ["2046251", "2588173"]
    assets = DataAssetsRequest(UniverseIdentifier.sedol, universe)
    query = {
        'startDate': '2022-04-05',
        'endDate': '2022-04-05',
        'assets': assets,
        'measures': [Measure.Unadjusted_Specific_Risk, Measure.Asset_Universe],
        'limitFactors': False
    }

    results = {
        'results': [
            {
                "date": "2022-04-05",
                "assetData": {
                    "universe": ["2046251", "2588173"],
                    "unadjustedSpecificRisk": [0.5, 1.6]
                }
            }
        ],
        'totalResults': 1
    }

    unadjusted_specific_risk_response = {
        '2588173': {'2022-04-05': 1.6},
        '2046251': {'2022-04-05': 0.5}
    }

    mocker.patch.object(GsSession.current, '_post', return_value=results)

    # run test
    response = model.get_unadjusted_specific_risk(start_date=dt.date(2022, 4, 5),
                                                  end_date=dt.date(2022, 4, 5),
                                                  assets=assets,
                                                  format=ReturnFormat.JSON)

    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='model_id'),
                                               query, timeout=200)
    assert response == unadjusted_specific_risk_response


def test_get_dividend_yield(mocker):
    model = mock_risk_model(mocker)

    universe = ["2046251", "2588173"]
    assets = DataAssetsRequest(UniverseIdentifier.sedol, universe)
    query = {
        'startDate': '2022-04-05',
        'endDate': '2022-04-05',
        'assets': assets,
        'measures': [Measure.Dividend_Yield, Measure.Asset_Universe],
        'limitFactors': False
    }

    results = {
        'results': [
            {
                "date": "2022-04-05",
                "assetData": {
                    "universe": ["2046251", "2588173"],
                    "dividendYield": [0.5, 1.6]
                }
            }
        ],
        'totalResults': 1
    }

    dividend_yield_response = {
        '2588173': {'2022-04-05': 1.6},
        '2046251': {'2022-04-05': 0.5}
    }

    mocker.patch.object(GsSession.current, '_post', return_value=results)

    # run test
    response = model.get_dividend_yield(start_date=dt.date(2022, 4, 5),
                                        end_date=dt.date(2022, 4, 5),
                                        assets=assets,
                                        format=ReturnFormat.JSON)

    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='model_id'),
                                               query, timeout=200)
    assert response == dividend_yield_response


def test_get_model_price(mocker):
    model = mock_macro_risk_model(mocker)

    universe = ["2046251", "2588173"]
    assets = DataAssetsRequest(UniverseIdentifier.sedol, universe)
    query = {
        'startDate': '2022-04-05',
        'endDate': '2022-04-05',
        'assets': assets,
        'measures': [Measure.Model_Price, Measure.Asset_Universe],
        'limitFactors': False
    }

    results = {
        'results': [
            {
                "date": "2022-04-05",
                "assetData": {
                    "universe": ["2046251", "2588173"],
                    "modelPrice": [100, 200]
                }
            }
        ],
        'totalResults': 1
    }

    model_price_response = {
        '2588173': {'2022-04-05': 200},
        '2046251': {'2022-04-05': 100}
    }

    mocker.patch.object(GsSession.current, '_post', return_value=results)

    # run test
    response = model.get_model_price(start_date=dt.date(2022, 4, 5),
                                     end_date=dt.date(2022, 4, 5),
                                     assets=assets,
                                     format=ReturnFormat.JSON)

    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='macro_model_id'),
                                               query, timeout=200)
    assert response == model_price_response


def test_get_covariance_matrix(mocker):
    model = mock_risk_model(mocker)

    universe = ["2046251", "2588173"]
    assets = DataAssetsRequest(UniverseIdentifier.sedol, universe)
    query = {
        'startDate': '2022-04-05',
        'endDate': '2022-04-05',
        'assets': assets,
        'measures': [Measure.Covariance_Matrix, Measure.Factor_Name, Measure.Factor_Id,
                     Measure.Universe_Factor_Exposure,
                     Measure.Asset_Universe],
        'limitFactors': True
    }

    results = {
        'results': [
            {
                "date": "2022-04-05",
                "factorData": [
                    {
                        "factorId": "1",
                        "factorName": "factor1",
                    },
                    {
                        "factorId": "2",
                        "factorName": "factor2",
                    },
                    {
                        "factorId": "3",
                        "factorName": "factor3",
                    },
                    {
                        "factorId": "4",
                        "factorName": "factor4",
                    }
                ],
                "covarianceMatrix": [[0.5, 0.6, 0.7, 0.8], [0.3, 0.7, 0.8, 0.9], [0.5, 0.6, 0.7, 0.8],
                                     [0.3, 0.7, 0.8, 0.9]]
            }
        ],
        'totalResults': 1
    }

    covariance_matrix_response = [{
        "date": "2022-04-05",
        "factorData": [
            {
                "factorId": "1",
                "factorName": "factor1",
            },
            {
                "factorId": "2",
                "factorName": "factor2",
            },
            {
                "factorId": "3",
                "factorName": "factor3",
            },
            {
                "factorId": "4",
                "factorName": "factor4",
            }
        ],
        "covarianceMatrix": [[0.5, 0.6, 0.7, 0.8], [0.3, 0.7, 0.8, 0.9], [0.5, 0.6, 0.7, 0.8],
                             [0.3, 0.7, 0.8, 0.9]]
    }]

    mocker.patch.object(GsSession.current, '_post', return_value=results)

    # run test
    response = model.get_covariance_matrix(start_date=dt.date(2022, 4, 5),
                                           end_date=dt.date(2022, 4, 5),
                                           assets=assets,
                                           format=ReturnFormat.JSON)

    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='model_id'),
                                               query, timeout=200)
    assert response == covariance_matrix_response


def test_get_unadjusted_covariance_matrix(mocker):
    model = mock_risk_model(mocker)

    universe = ["2046251", "2588173"]
    assets = DataAssetsRequest(UniverseIdentifier.sedol, universe)
    query = {
        'startDate': '2022-04-05',
        'endDate': '2022-04-05',
        'assets': assets,
        'measures': [Measure.Unadjusted_Covariance_Matrix, Measure.Factor_Name, Measure.Factor_Id,
                     Measure.Universe_Factor_Exposure, Measure.Asset_Universe],
        'limitFactors': True
    }

    results = {
        'results': [
            {
                "date": "2022-04-05",
                "factorData": [
                    {
                        "factorId": "1",
                        "factorName": "factor1",
                    },
                    {
                        "factorId": "2",
                        "factorName": "factor2",
                    },
                    {
                        "factorId": "3",
                        "factorName": "factor3",
                    },
                    {
                        "factorId": "4",
                        "factorName": "factor4",
                    }
                ],
                "unadjustedCovarianceMatrix": [[0.5, 0.6, 0.7, 0.8], [0.3, 0.7, 0.8, 0.9], [0.5, 0.6, 0.7, 0.8],
                                               [0.3, 0.7, 0.8, 0.9]]
            }
        ],
        'totalResults': 1
    }

    unadjusted_covariance_matrix_response = [{
        "date": "2022-04-05",
        "factorData": [
            {
                "factorId": "1",
                "factorName": "factor1",
            },
            {
                "factorId": "2",
                "factorName": "factor2",
            },
            {
                "factorId": "3",
                "factorName": "factor3",
            },
            {
                "factorId": "4",
                "factorName": "factor4",
            }
        ],
        "unadjustedCovarianceMatrix": [[0.5, 0.6, 0.7, 0.8], [0.3, 0.7, 0.8, 0.9], [0.5, 0.6, 0.7, 0.8],
                                       [0.3, 0.7, 0.8, 0.9]]
    }]

    mocker.patch.object(GsSession.current, '_post', return_value=results)

    # run test
    response = model.get_unadjusted_covariance_matrix(start_date=dt.date(2022, 4, 5),
                                                      end_date=dt.date(2022, 4, 5),
                                                      assets=assets,
                                                      format=ReturnFormat.JSON)

    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='model_id'),
                                               query, timeout=200)
    assert response == unadjusted_covariance_matrix_response


def test_get_pre_vra_covariance_matrix(mocker):
    model = mock_risk_model(mocker)

    universe = ["2046251", "2588173"]
    assets = DataAssetsRequest(UniverseIdentifier.sedol, universe)
    query = {
        'startDate': '2022-04-05',
        'endDate': '2022-04-05',
        'assets': assets,
        'measures': [Measure.Pre_VRA_Covariance_Matrix, Measure.Factor_Name, Measure.Factor_Id,
                     Measure.Universe_Factor_Exposure, Measure.Asset_Universe],
        'limitFactors': True
    }

    results = {
        'results': [
            {
                "date": "2022-04-05",
                "factorData": [
                    {
                        "factorId": "1",
                        "factorName": "factor1",
                    },
                    {
                        "factorId": "2",
                        "factorName": "factor2",
                    },
                    {
                        "factorId": "3",
                        "factorName": "factor3",
                    },
                    {
                        "factorId": "4",
                        "factorName": "factor4",
                    }
                ],
                "preVRACovarianceMatrix": [[0.5, 0.6, 0.7, 0.8], [0.3, 0.7, 0.8, 0.9], [0.5, 0.6, 0.7, 0.8],
                                           [0.3, 0.7, 0.8, 0.9]]
            }
        ],
        'totalResults': 1
    }

    pre_vra_covariance_matrix_response = [{
        "date": "2022-04-05",
        "factorData": [
            {
                "factorId": "1",
                "factorName": "factor1",
            },
            {
                "factorId": "2",
                "factorName": "factor2",
            },
            {
                "factorId": "3",
                "factorName": "factor3",
            },
            {
                "factorId": "4",
                "factorName": "factor4",
            }
        ],
        "preVRACovarianceMatrix": [[0.5, 0.6, 0.7, 0.8], [0.3, 0.7, 0.8, 0.9], [0.5, 0.6, 0.7, 0.8],
                                   [0.3, 0.7, 0.8, 0.9]]
    }]

    mocker.patch.object(GsSession.current, '_post', return_value=results)

    # run test
    response = model.get_pre_vra_covariance_matrix(start_date=dt.date(2022, 4, 5),
                                                   end_date=dt.date(2022, 4, 5),
                                                   assets=assets,
                                                   format=ReturnFormat.JSON)

    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='model_id'),
                                               query, timeout=200)
    assert response == pre_vra_covariance_matrix_response


def test_get_risk_free_rate(mocker):
    model = mock_risk_model(mocker)

    query = {
        'startDate': '2022-04-05',
        'endDate': '2022-04-05',
        'measures': [Measure.Risk_Free_Rate],
        'assets': DataAssetsRequest(UniverseIdentifier.gsid, []),
        'limitFactors': False
    }
    currencies = ["EUR", "INR"]
    risk_free_rate = [1.08, 0.012]
    results = {
        'results': [
            {
                "date": "2022-04-05",
                "currencyRatesData": {
                    "riskFreeRate": risk_free_rate,
                    "currency": currencies,
                },
            }
        ],
        'totalResults': 1
    }

    risk_free_rate_response = {
        "currency": {('2022-04-05', 0): 'EUR', ('2022-04-05', 1): 'INR'},
        "riskFreeRate": {('2022-04-05', 0): 1.08, ('2022-04-05', 1): 0.012}
    }

    mocker.patch.object(GsSession.current, '_post', return_value=results)

    response = model.get_risk_free_rate(start_date=dt.date(2022, 4, 5),
                                        end_date=dt.date(2022, 4, 5),
                                        format=ReturnFormat.JSON)

    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='model_id'),
                                               query, timeout=200)
    assert response == risk_free_rate_response

    # fitler risk free rates by currency
    expected_filtered_rates = {
        "currency": {('2022-04-05', 1): 'INR'},
        "riskFreeRate": {('2022-04-05', 1): 0.012}
    }
    actual_filtered_rates = model.get_risk_free_rate(start_date=dt.date(2022, 4, 5),
                                                     end_date=dt.date(2022, 4, 5),
                                                     currencies=[Currency.INR],
                                                     format=ReturnFormat.JSON)

    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='model_id'),
                                               query, timeout=200)

    assert actual_filtered_rates == expected_filtered_rates

    # test DataFrame return format
    expected_data_frame = get_optional_data_as_dataframe([
        {
            "date": "2022-04-05",
            "currencyRatesData": {
                "riskFreeRate": risk_free_rate,
                "currency": currencies,
            },
        }
    ], "currencyRatesData")

    expected_data_frame = expected_data_frame.loc[expected_data_frame['currency'].isin(['INR'])]
    actual_data_frame = model.get_risk_free_rate(start_date=dt.date(2022, 4, 5),
                                                 end_date=dt.date(2022, 4, 5),
                                                 currencies=[Currency.INR])

    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='model_id'),
                                               query, timeout=200)

    assert_frame_equal(expected_data_frame, actual_data_frame, check_like=True)


def test_get_currency_exchange_rate(mocker):
    model = mock_risk_model(mocker)

    query = {
        'startDate': '2022-04-05',
        'endDate': '2022-04-05',
        'measures': [Measure.Currency_Exchange_Rate],
        'assets': DataAssetsRequest(UniverseIdentifier.gsid, []),
        'limitFactors': False
    }
    currencies = ["EUR", "INR"]
    currency_exchange_rate = [1.08, 0.012]
    results = {
        'results': [
            {
                "date": "2022-04-05",
                "currencyRatesData": {
                    "exchangeRate": currency_exchange_rate,
                    "currency": currencies,
                },
            }
        ],
        'totalResults': 1
    }

    currency_exchange_rate_response = {
        "currency": {('2022-04-05', 0): 'EUR', ('2022-04-05', 1): 'INR'},
        "exchangeRate": {('2022-04-05', 0): 1.08, ('2022-04-05', 1): 0.012}
    }

    mocker.patch.object(GsSession.current, '_post', return_value=results)

    response = model.get_currency_exchange_rate(start_date=dt.date(2022, 4, 5),
                                                end_date=dt.date(2022, 4, 5),
                                                format=ReturnFormat.JSON)

    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='model_id'),
                                               query, timeout=200)
    assert response == currency_exchange_rate_response

    # fitler risk free rates by currency
    expected_filtered_rates = {
        "currency": {('2022-04-05', 1): 'INR'},
        "exchangeRate": {('2022-04-05', 1): 0.012}
    }
    actual_filtered_rates = model.get_currency_exchange_rate(start_date=dt.date(2022, 4, 5),
                                                             end_date=dt.date(2022, 4, 5),
                                                             currencies=[Currency.INR],
                                                             format=ReturnFormat.JSON)

    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='model_id'),
                                               query, timeout=200)

    assert actual_filtered_rates == expected_filtered_rates

    # test DataFrame return format

    expected_data_frame = get_optional_data_as_dataframe([
        {
            "date": "2022-04-05",
            "currencyRatesData": {
                "exchangeRate": currency_exchange_rate,
                "currency": currencies,
            },
        }
    ], "currencyRatesData")

    expected_data_frame = expected_data_frame.loc[expected_data_frame['currency'].isin(['INR'])]

    actual_data_frame = model.get_currency_exchange_rate(start_date=dt.date(2022, 4, 5),
                                                         end_date=dt.date(2022, 4, 5),
                                                         currencies=[Currency.INR])
    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='model_id'),
                                               query, timeout=200)

    assert_frame_equal(expected_data_frame, actual_data_frame, check_like=True)


if __name__ == "__main__":
    pytest.main([__file__])
