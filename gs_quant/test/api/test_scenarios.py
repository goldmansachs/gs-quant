"""
Copyright 2024 Goldman Sachs.
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
from gs_quant.api.gs.scenarios import GsFactorScenarioApi
from gs_quant.session import *
from gs_quant.target.risk import Scenario, FactorScenarioType
from gs_quant.base import DictBase


def test_get_many_scenarios(mocker):
    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_get', return_value={})

    # run test
    GsFactorScenarioApi.get_many_scenarios(ids=["scenario_1"],
                                           names=["scenario_name"],
                                           type="Factor Shock",
                                           risk_model="MODEL_ID",
                                           shocked_factors=["factor 1"],
                                           shocked_factor_categories=["factor 2"],
                                           start_date=dt.date(2024, 1, 1),
                                           end_date=dt.date(2024, 1, 1))

    GsSession.current._get.assert_called_with('/risk/scenarios?limit=100&'
                                              'id=scenario_1&name=scenario_name&riskModel=MODEL_ID'
                                              '&factorScenarioType=Factor Shock'
                                              '&shockedFactor=factor 1&shockedFactorCategory=factor 2'
                                              '&historicalSimulationStartDate=2024-01-01'
                                              '&historicalSimulationEndDate=2024-01-01',
                                              cls=Scenario)


def test_get_scenario(mocker):
    scenario_id = 'SCENARIO_ID'

    expected_response = Scenario(name="scenario name",
                                 id_=scenario_id,
                                 description="scenario_description",
                                 type_=FactorScenarioType.Factor_Shock,
                                 parameters=DictBase())

    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_get', return_value=expected_response)

    # run test
    response = GsFactorScenarioApi.get_scenario(scenario_id)
    GsSession.current._get.assert_called_with(f'/risk/scenarios/{scenario_id}', cls=Scenario)
    assert response == expected_response


def test_create_scenario(mocker):
    scenario_id = 'SCENARIO_ID'

    scenario_without_id = Scenario(name="scenario name",
                                   description="scenario_description",
                                   type_=FactorScenarioType.Factor_Shock,
                                   parameters=DictBase())
    expected_response = Scenario(name="scenario name",
                                 id_=scenario_id,
                                 description="scenario_description",
                                 type_=FactorScenarioType.Factor_Shock,
                                 parameters=DictBase())

    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))

    mocker.patch.object(GsSession.current, '_post', return_value=expected_response)

    # run test
    response = GsFactorScenarioApi.create_scenario(scenario_without_id)
    GsSession.current._post.assert_called_with('/risk/scenarios', scenario_without_id, cls=Scenario)
    assert response == expected_response


def test_update_scenario(mocker):
    scenario_id = 'SCENARIO_ID'

    scenario = Scenario(name="scenario name",
                        id_=scenario_id,
                        description="scenario_description",
                        type_=FactorScenarioType.Factor_Shock,
                        parameters=DictBase())

    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))

    mocker.patch.object(GsSession.current, '_put', return_value=scenario)

    # run test
    GsFactorScenarioApi.update_scenario(scenario)
    GsSession.current._put.assert_called_with(f'/risk/scenarios/{scenario_id}', scenario, cls=Scenario)


def test_delete_scenario(mocker):
    mock_response = "Deleted Scenario"

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
    response = GsFactorScenarioApi.delete_scenario('SCENARIO_ID')
    GsSession.current._delete.assert_called_with('/risk/scenarios/SCENARIO_ID')
    assert response == mock_response


def test_scenario_calculate(mocker):
    calculation_request = {
        'date': '2020-02-05',
        "riskModel": "MODEL_ID",
        "measures": ["Summary", "Factor Pnl", "By Sector Pnl Aggregations", "By Asset"],
        "scenarios": ["scenario_1"],
        "reportId": "REPORT_ID"
    }

    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_post', return_value=dict())

    # run test
    GsFactorScenarioApi.calculate_scenario(calculation_request)
    GsSession.current._post.assert_called_with('/scenarios/calculate', calculation_request)
