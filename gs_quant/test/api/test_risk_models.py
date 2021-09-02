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
from gs_quant.target.risk_models import RiskModel, RiskModelFactor, RiskModelCalendar


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
                "version": 4
            }),
            RiskModel.from_dict({
                "coverage": "Global",
                "id": "WW_TEST_MODEL_2",
                "name": "World Wide Medium Term Test Model 2",
                "term": "Medium",
                "vendor": "Goldman Sachs",
                "universeIdentifier": "gsid",
                "version": 2
            })
        ],
        'totalResults': 2
    }

    expected_response = [
        RiskModel(coverage='Global', id='WW_TEST_MODEL', name='World Wide Medium Term Test Model', term='Medium',
                  vendor='Goldman Sachs', universe_identifier='gsid', version=4),
        RiskModel(coverage='Global', id='WW_TEST_MODEL_2', name='World Wide Medium Term Test Model 2', term='Medium',
                  vendor='Goldman Sachs', universe_identifier='gsid', version=2)
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
        "version": 4
    })

    expected_response = RiskModel(coverage='Global', id='WW_TEST_MODEL', name='World Wide Medium Term Test Model',
                                  term='Medium', vendor='Goldman Sachs', version=4, universe_identifier='gsid')

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
        "version": 4
    })

    expected_response = RiskModel(coverage='Global', id='WW_TEST_MODEL', name='World Wide Medium Term Test Model',
                                  term='Medium',
                                  vendor='Goldman Sachs', version=4, universe_identifier='gsid')

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
        "universeIdentifier": "gsid",
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
        RiskModelFactor.from_dict({
            "type": "Factor",
            "identifier": "Factor1"
        }),
        RiskModelFactor.from_dict({
            "type": "Category",
            "identifier": "Factor2"
        })
    ],
        'totalResults': 2
    }

    expected_response = [
        RiskModelFactor(identifier='Factor1', type='Factor'),
        RiskModelFactor(identifier='Factor2', type='Category')
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
    GsSession.current._get.assert_called_with('/risk/models/id/factors', cls=RiskModelFactor)
    assert response == expected_response


def test_create_risk_model_factor(mocker):
    factor = RiskModelFactor.from_dict({
        "identifier": "Factor1",
        "type": "Factor"
    })

    expected_response = RiskModelFactor(identifier='Factor1', type='Factor')

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
    GsSession.current._post.assert_called_with('/risk/models/id/factors', factor, cls=RiskModelFactor)
    assert response == expected_response


def test_update_risk_model_factor(mocker):
    factor = RiskModelFactor.from_dict({
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
                                              .format(id='id', identifier='factor'), factor, cls=RiskModelFactor)
    assert response == factor


def test_get_risk_model_coverage(mocker):
    results = {
        "results": [
            RiskModelFactor.from_dict({
                "model": "AXUS4S",
                "businessDate": "2020-11-02"
            }),
            RiskModelFactor.from_dict({
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
    GsSession.current._post.assert_called_with('/risk/models/coverage', {})
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
    GsSession.current._post.assert_called_with('/risk/models/data/{id}'.format(id='id'), risk_model_data)
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
    GsSession.current._post.assert_called_with('/risk/models/data/{id}/query'.format(id='id'), query)
    assert response == results
