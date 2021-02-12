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

import pytest
from testfixtures import Replacer
from testfixtures.mock import Mock

import gs_quant.timeseries.measures_risk_models as mrm
from gs_quant.data.core import DataContext
from gs_quant.errors import MqValueError
from gs_quant.markets.risk_model import RiskModel as Risk_Model
from gs_quant.markets.securities import Stock
from gs_quant.target.risk_models import RiskModel, CoverageType, Term, UniverseIdentifier


def mock_risk_model():
    risk_model = RiskModel(coverage=CoverageType.Country, id_='model_id', name='Fake Risk Model',
                           term=Term.Long, universe_identifier=UniverseIdentifier.gsid, vendor='GS',
                           version=1.0)

    replace = Replacer()

    # mock getting risk model entity()
    mock = replace('gs_quant.api.gs.risk_models.GsRiskModelApi.get_risk_model', Mock())
    mock.return_value = risk_model

    actual = Risk_Model(model_id='model_id')
    replace.restore()
    return actual


def test_factor_exposure():
    risk_model = RiskModel(coverage=CoverageType.Country, id_='model_id', name='Fake Risk Model',
                           term=Term.Long, universe_identifier=UniverseIdentifier.gsid, vendor='GS',
                           version=1.0)

    risk_model_data = {
        'results': [
            {
                'date': '2020-01-01',
                'assetData': {
                    'factorExposure': [
                        {
                            'factor_id': 1.01,
                            'factor_id_1': 1.23
                        }
                    ]
                }
            },
            {
                'date': '2020-01-02',
                'assetData': {
                    'factorExposure': [
                        {
                            'factor_id': 1.02,
                            'factor_id_1': 1.23
                        }
                    ]
                }
            },
            {
                'date': '2020-01-03',
                'assetData': {
                    'factorExposure': [
                        {
                            'factor_id': 1.03,
                            'factor_id_1': 1.23
                        }
                    ]
                }
            }
        ]
    }
    replace = Replacer()

    # mock getting risk model entity()
    mock = replace('gs_quant.api.gs.risk_models.GsRiskModelApi.get_risk_model', Mock())
    mock.return_value = risk_model

    # mock getting risk model factor entity
    mock = replace('gs_quant.api.gs.risk_models.GsRiskModelApi.get_risk_model_factor_data', Mock())
    mock.return_value = [{
        'identifier': 'factor_id',
        'type': 'Factor',
        'name': "Factor Name"
    }]

    # mock getting asset gsid
    mock = replace('gs_quant.markets.securities.Asset.get_identifiers', Mock())
    mock.return_value = {'GSID': '12345'}

    # mock getting risk model dates
    mock = replace('gs_quant.api.gs.risk_models.GsRiskModelApi.get_risk_model_dates', Mock())
    mock.return_value = ['2020-01-01', '2020-01-02', '2020-01-03']

    # mock getting risk model data
    mock = replace('gs_quant.markets.risk_model.RiskModel.get_data', Mock())
    mock.return_value = risk_model_data

    with DataContext(datetime.date(2020, 1, 1), datetime.date(2020, 1, 3)):
        actual = mrm.factor_zscore(Stock(id_='id', name='Fake Asset'), 'model_id', 'Factor Name')
        assert all(actual.values == [1.01, 1.02, 1.03])

    with pytest.raises(MqValueError):
        mrm.factor_zscore(Stock(id_='id', name='Fake Asset'), 'model_id', 'Wrong Factor Name')
    replace.restore()


def test_covariance():
    risk_model = RiskModel(coverage=CoverageType.Country, id_='model_id', name='Fake Risk Model',
                           term=Term.Long, universe_identifier=UniverseIdentifier.gsid, vendor='GS',
                           version=1.0)

    covariances = [
        {
            'date': '2020-01-01',
            'covariance': 1.01
        },
        {
            'date': '2020-01-02',
            'covariance': 1.02
        },
        {
            'date': '2020-01-03',
            'covariance': 1.03
        },
    ]
    replace = Replacer()

    # mock getting risk model factor entity
    mock = replace('gs_quant.api.gs.risk_models.GsRiskModelApi.get_risk_model_factor_data', Mock())
    mock.return_value = [{
        'identifier': 'factor_id',
        'type': 'Factor',
        'name': "Factor Name"
    }]

    # mock getting risk model entity()
    mock = replace('gs_quant.api.gs.risk_models.GsRiskModelApi.get_risk_model', Mock())
    mock.return_value = risk_model

    # mock getting risk model dates
    mock = replace('gs_quant.api.gs.risk_models.GsRiskModelApi.get_risk_model_dates', Mock())
    mock.return_value = ['2020-01-01', '2020-01-02', '2020-01-03']

    # mock getting covariances
    mock = replace('gs_quant.markets.factor.Factor.get_covariance', Mock())
    mock.return_value = covariances

    with DataContext(datetime.date(2020, 1, 1), datetime.date(2020, 1, 3)):
        actual = mrm.covariance(mock_risk_model(), 'Factor Name', 'Factor Name')
        assert all(actual.values == [1.01, 1.02, 1.03])

    with pytest.raises(MqValueError):
        mrm.covariance(mock_risk_model(), 'Wrong Factor Name', 'Factor Name')
    replace.restore()


if __name__ == '__main__':
    pytest.main(args=[__file__])
