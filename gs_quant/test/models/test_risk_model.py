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

from gs_quant.models.risk_model import FactorRiskModel
from gs_quant.session import *
from gs_quant.target.risk_models import RiskModel as Risk_Model, CoverageType, Term, UniverseIdentifier, Entitlements

empty_entitlements = {
    "execute": [],
    "edit": [],
    "view": [],
    "admin": [],
    "query": [],
    "upload": []
}

mock_risk_model_obj = Risk_Model(
    id_='model_id',
    name='Fake Risk Model',
    coverage=CoverageType.Country,
    term=Term.Long,
    universe_identifier=UniverseIdentifier.gsid,
    vendor='GS',
    version=1.0,
    entitlements=empty_entitlements
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
    return FactorRiskModel('model_id')


def test_create_risk_model(mocker):
    mock_risk_model(mocker)
    risk_model_id = 'model_id'
    mocker.patch.object(GsSession.current, '_get', return_value=mock_risk_model_obj)
    new_model = FactorRiskModel.create(
        coverage=CoverageType.Country,
        id_=risk_model_id,
        name='Fake Risk Model',
        term=Term.Long,
        universe_identifier=UniverseIdentifier.gsid,
        vendor='GS',
        version=1.0
    )
    assert new_model.id == risk_model_id


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

    new_model.add_entitlements(new_entitlements)
    new_model.update()
    assert 'guid:X' in new_model.entitlements.execute
    mocker.patch.object(GsSession.current, '_get', return_value=new_model)
    new_model.remove_entitlements(new_entitlements)
    new_model.update()
    assert 'guid:X' not in new_model.entitlements.execute
    mocker.patch.object(GsSession.current, '_get', return_value=new_model)
    new_model.add_entitlements(Entitlements.from_dict(new_entitlements))
    new_model.update()
    assert 'guid:X' in new_model.entitlements.execute
    mocker.patch.object(GsSession.current, '_get', return_value=new_model)
    new_model.remove_entitlements(Entitlements.from_dict(new_entitlements))
    new_model.update()
    assert 'guid:X' not in new_model.entitlements.execute

    new_entitlements = {
        "execute": ['guid:X'],
        "edit": [],
        "view": [],
        "admin": ['guid:XX'],
        "query": [],
        "upload": ['guid:XXX']
    }
    new_model.entitlements = Entitlements.from_dict(new_entitlements)
    new_model.update()
    mocker.patch.object(GsSession.current, '_get', return_value=new_model)
    assert 'guid:X' in new_model.entitlements.execute
    assert 'guid:XX' in new_model.entitlements.admin
    assert 'guid:XXX' in new_model.entitlements.upload


def test_update_risk_model(mocker):
    new_model = mock_risk_model(mocker)

    new_model.term = Term.Short
    new_model.update()
    mocker.patch.object(GsSession.current, '_get', return_value=new_model)
    assert new_model.term == Term.Short

    new_model.description = 'Test risk model'
    new_model.update()
    mocker.patch.object(GsSession.current, '_get', return_value=new_model)
    assert new_model.description == 'Test risk model'

    new_model.vendor = 'GS'
    new_model.update()
    mocker.patch.object(GsSession.current, '_get', return_value=new_model)
    assert new_model.vendor == 'GS'

    new_model.term = Term.Medium
    new_model.update()
    mocker.patch.object(GsSession.current, '_get', return_value=new_model)
    assert new_model.term == Term.Medium

    new_model.version = 0.1
    new_model.update()
    mocker.patch.object(GsSession.current, '_get', return_value=new_model)
    assert new_model.version == 0.1

    new_model.coverage = CoverageType.Global
    new_model.update()
    mocker.patch.object(GsSession.current, '_get', return_value=new_model)
    assert new_model.coverage == CoverageType.Global

    new_model.name = 'TEST RISK MODEL'
    new_model.update()
    mocker.patch.object(GsSession.current, '_get', return_value=new_model)
    assert new_model.name == 'TEST RISK MODEL'


if __name__ == "__main__":
    pytest.main([__file__])
