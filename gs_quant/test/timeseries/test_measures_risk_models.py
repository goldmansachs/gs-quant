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
from math import sqrt

import pytest
from testfixtures import Replacer
from testfixtures.mock import Mock

import gs_quant.timeseries.measures_risk_models as mrm
from gs_quant.data.core import DataContext
from gs_quant.errors import MqValueError
from gs_quant.models.risk_model import FactorRiskModel as Factor_Risk_Model
from gs_quant.markets.securities import Stock
from gs_quant.target.risk_models import RiskModel, CoverageType, Term, UniverseIdentifier

mock_risk_model_obj = RiskModel(
    id_='model_id',
    name='Fake Risk Model',
    coverage=CoverageType.Country,
    term=Term.Long,
    universe_identifier=UniverseIdentifier.gsid,
    vendor='GS',
    version=1.0
)

mock_risk_model_data = {
    'totalResults': 2,
    'missingDates': [],
    'results': [
        {
            'date': '2020-01-01',
            'factorData': [
                {'factorId': '1', 'factorCategory': 'Style'},
                {'factorId': '2', 'factorCategory': 'Style'},
                {'factorId': '3', 'factorCategory': 'Style'},
            ]
        },
        {
            'date': '2020-01-02',
            'factorData': [
                {'factorId': '1', 'factorCategory': 'Style'},
                {'factorId': '2', 'factorCategory': 'Style'},
                {'factorId': '3', 'factorCategory': 'Style'},
            ]
        },
        {
            'date': '2020-01-03',
            'factorData': [
                {'factorId': '1', 'factorCategory': 'Style'},
                {'factorId': '2', 'factorCategory': 'Style'},
                {'factorId': '3', 'factorCategory': 'Style'},
            ]
        }
    ]
}

mock_risk_model_factor_data = [{
    'identifier': 'factor_id',
    'type': 'Factor',
    'name': "Factor Name",
}]

mock_covariance_curve = {
    '2020-01-01': 1.01,
    '2020-01-02': 1.02,
    '2020-01-03': 1.03
}


def mock_risk_model():
    replace = Replacer()

    # mock getting risk model entity()
    mock = replace('gs_quant.api.gs.risk_models.GsRiskModelApi.get_risk_model', Mock())
    mock.return_value = mock_risk_model_obj

    actual = Factor_Risk_Model.get(model_id='model_id')
    replace.restore()
    return actual


def test_factor_zscore():

    replace = Replacer()

    # mock getting risk model entity()
    mock = replace('gs_quant.api.gs.risk_models.GsRiskModelApi.get_risk_model', Mock())
    mock.return_value = mock_risk_model_obj

    # mock getting risk model factor entity
    mock = replace('gs_quant.api.gs.risk_models.GsFactorRiskModelApi.get_risk_model_data', Mock())
    mock.return_value = mock_risk_model_data

    # mock getting risk model factor entity
    mock = replace('gs_quant.api.gs.risk_models.GsFactorRiskModelApi.get_risk_model_factor_data', Mock())
    mock.return_value = mock_risk_model_factor_data

    # mock getting asset gsid
    mock = replace('gs_quant.markets.securities.Asset.get_identifier', Mock())
    mock.return_value = '12345'

    # mock getting risk model dates
    mock = replace('gs_quant.api.gs.risk_models.GsRiskModelApi.get_risk_model_dates', Mock())
    mock.return_value = ['2020-01-01', '2020-01-02', '2020-01-03']

    # mock getting risk model data
    mock = replace('gs_quant.models.risk_model.FactorRiskModel.get_data', Mock())
    mock.return_value = {
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

    with DataContext(datetime.date(2020, 1, 1), datetime.date(2020, 1, 3)):
        actual = mrm.factor_zscore(Stock(id_='id', name='Fake Asset'), 'model_id', 'Factor Name')
        assert all(actual.values == [1.01, 1.02, 1.03])

    with pytest.raises(MqValueError):
        mrm.factor_zscore(Stock(id_='id', name='Fake Asset'), 'model_id', 'Wrong Factor Name')
    replace.restore()


def test_factor_covariance():

    replace = Replacer()

    # mock getting risk model entity()
    mock = replace('gs_quant.api.gs.risk_models.GsRiskModelApi.get_risk_model', Mock())
    mock.return_value = mock_risk_model_obj

    # mock getting risk model dates
    mock = replace('gs_quant.api.gs.risk_models.GsRiskModelApi.get_risk_model_dates', Mock())
    mock.return_value = ['2020-01-01', '2020-01-02', '2020-01-03']

    # mock getting risk model factor entity
    mock = replace('gs_quant.api.gs.risk_models.GsFactorRiskModelApi.get_risk_model_data', Mock())
    mock.return_value = mock_risk_model_data

    # mock getting risk model factor entity
    mock = replace('gs_quant.api.gs.risk_models.GsFactorRiskModelApi.get_risk_model_factor_data', Mock())
    mock.return_value = mock_risk_model_factor_data

    # mock getting covariances
    mock = replace('gs_quant.markets.factor.Factor.covariance', Mock())
    mock.return_value = mock_covariance_curve

    with DataContext(datetime.date(2020, 1, 1), datetime.date(2020, 1, 3)):
        actual = mrm.factor_covariance(mock_risk_model(), 'Factor Name', 'Factor Name')
        assert all(actual.values == [1.01, 1.02, 1.03])

    with pytest.raises(MqValueError):
        mrm.factor_covariance(mock_risk_model(), 'Wrong Factor Name', 'Factor Name')
    replace.restore()


def test_factor_volatility():

    replace = Replacer()

    # mock getting risk model factor entity
    mock = replace('gs_quant.api.gs.risk_models.GsFactorRiskModelApi.get_risk_model_data', Mock())
    mock.return_value = mock_risk_model_data

    # mock getting risk model factor entity
    mock = replace('gs_quant.api.gs.risk_models.GsFactorRiskModelApi.get_risk_model_factor_data', Mock())
    mock.return_value = mock_risk_model_factor_data

    # mock getting risk model entity()
    mock = replace('gs_quant.api.gs.risk_models.GsRiskModelApi.get_risk_model', Mock())
    mock.return_value = mock_risk_model_obj

    # mock getting risk model dates
    mock = replace('gs_quant.api.gs.risk_models.GsRiskModelApi.get_risk_model_dates', Mock())
    mock.return_value = ['2020-01-01', '2020-01-02', '2020-01-03']

    # mock getting covariances
    mock = replace('gs_quant.markets.factor.Factor.variance', Mock())
    mock.return_value = mock_covariance_curve

    with DataContext(datetime.date(2020, 1, 1), datetime.date(2020, 1, 3)):
        actual = mrm.factor_volatility(mock_risk_model(), 'Factor Name')
        assert all(actual.values == [sqrt(1.01) * 100, sqrt(1.02) * 100, sqrt(1.03) * 100])

    with pytest.raises(MqValueError):
        mrm.factor_covariance(mock_risk_model(), 'Wrong Factor Name', 'Factor Name')
    replace.restore()


def test_factor_correlation():

    replace = Replacer()

    # mock getting risk model factor entity
    mock = replace('gs_quant.api.gs.risk_models.GsFactorRiskModelApi.get_risk_model_data', Mock())
    mock.return_value = mock_risk_model_data

    # mock getting risk model factor entity
    mock = replace('gs_quant.api.gs.risk_models.GsFactorRiskModelApi.get_risk_model_factor_data', Mock())
    mock.return_value = mock_risk_model_factor_data

    # mock getting risk model entity()
    mock = replace('gs_quant.api.gs.risk_models.GsRiskModelApi.get_risk_model', Mock())
    mock.return_value = mock_risk_model_obj

    # mock getting risk model dates
    mock = replace('gs_quant.api.gs.risk_models.GsRiskModelApi.get_risk_model_dates', Mock())
    mock.return_value = ['2020-01-01', '2020-01-02', '2020-01-03']

    # mock getting covariances
    mock = replace('gs_quant.markets.factor.Factor.covariance', Mock())
    mock.return_value = mock_covariance_curve

    with DataContext(datetime.date(2020, 1, 1), datetime.date(2020, 1, 3)):
        actual = mrm.factor_correlation(mock_risk_model(), 'Factor Name', 'Factor Name')
        assert all(actual.values == [1.0000000000000002, 1, 1])
    replace.restore()


def test_factor_performance():

    replace = Replacer()

    # mock getting risk model factor entity
    mock = replace('gs_quant.api.gs.risk_models.GsFactorRiskModelApi.get_risk_model_data', Mock())
    mock.return_value = mock_risk_model_data

    # mock getting risk model factor entity
    mock = replace('gs_quant.api.gs.risk_models.GsFactorRiskModelApi.get_risk_model_factor_data', Mock())
    mock.return_value = mock_risk_model_factor_data

    # mock getting risk model entity()
    mock = replace('gs_quant.api.gs.risk_models.GsRiskModelApi.get_risk_model', Mock())
    mock.return_value = mock_risk_model_obj

    # mock getting risk model dates
    mock = replace('gs_quant.api.gs.risk_models.GsRiskModelApi.get_risk_model_dates', Mock())
    mock.return_value = ['2020-01-01', '2020-01-02', '2020-01-03']

    # mock getting factor returns
    mock = replace('gs_quant.markets.factor.Factor.returns', Mock())
    mock.return_value = mock_covariance_curve

    with DataContext(datetime.date(2020, 1, 1), datetime.date(2020, 1, 3)):
        actual = mrm.factor_performance(mock_risk_model(), 'Factor Name')
        assert len(actual.values) == 3
    replace.restore()


if __name__ == '__main__':
    pytest.main(args=[__file__])
