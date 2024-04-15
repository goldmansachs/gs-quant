"""
Copyright 2024 Goldman Sachs.
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

from gs_quant.markets.scenario import FactorScenario, FactorScenarioType, FactorShockParameters, FactorShock
from gs_quant.session import *
from gs_quant.target.risk import Scenario
from gs_quant.target.common import Entitlements as TargetEntitlements
from gs_quant.entities.entitlements import Entitlements, EntitlementBlock


default_entitlements = TargetEntitlements(
    edit=(),
    view=(),
    admin=()
)

default_scenario_parameters = {
    "riskModel": "MODEL_ID",
    "propagateShocks": True,
    "factorShocks": [
        {"factor": "Factor 1", "shock": 5},
        {"factor": "Factor 2", "shock": -5}
    ]
}

mock_scenario_obj = Scenario(name="Scenario 1",
                             description="Scenario 1",
                             entitlements=default_entitlements,
                             id_="MSCENARIO",
                             parameters=default_scenario_parameters,
                             type_=FactorScenarioType.Factor_Shock)


def mock_factor_scenario(mocker):
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
    mocker.patch.object(GsSession.current, '_post', return_value=mock_scenario_obj)
    mocker.patch.object(GsSession.current, '_get', return_value=mock_scenario_obj)
    mocker.patch.object(GsSession.current, '_put', return_value=mock_scenario_obj)
    return FactorScenario.get('MSCENARIO')


def test_create_factor_scenario(mocker):
    mock_factor_scenario(mocker)
    mocker.patch.object(GsSession.current, '_post', return_value=mock_scenario_obj)
    new_scenario = FactorScenario(name="Scenario 1",
                                  type=FactorScenarioType.Factor_Shock,
                                  parameters=FactorShockParameters(
                                      factor_shocks=[
                                          FactorShock(factor="Factor 1", shock=5),
                                          FactorShock(factor="Factor 2", shock=-5)],
                                      propagate_shocks=True,
                                      risk_model="MODEL_ID"),
                                  entitlements=Entitlements(view=EntitlementBlock(),
                                                            edit=EntitlementBlock(),
                                                            admin=EntitlementBlock()),
                                  id_="MSCENARIO",
                                  description="Scenario 1")

    new_scenario.save()
    assert new_scenario.id == mock_scenario_obj.id
    assert new_scenario.name == mock_scenario_obj.name
    assert new_scenario.description == mock_scenario_obj.description
    assert new_scenario.entitlements == Entitlements.from_target(mock_scenario_obj.entitlements)
    assert new_scenario.parameters == FactorShockParameters.from_dict(mock_scenario_obj.parameters)
    assert new_scenario.type == mock_scenario_obj.type


def test_update_scenario_entitlements(mocker):
    scenario = mock_factor_scenario(mocker)

    new_entitlements = Entitlements(view=EntitlementBlock(roles=["role:A"]),
                                    edit=EntitlementBlock(roles=["role:B"]),
                                    admin=EntitlementBlock())

    scenario.entitlements = new_entitlements
    scenario.save()

    mocker.patch.object(GsSession.current, '_get', return_value=scenario)

    assert 'role:A' in scenario.entitlements.view.roles
    assert 'role:B' in scenario.entitlements.edit.roles


if __name__ == "__main__":
    pytest.main([__file__])
