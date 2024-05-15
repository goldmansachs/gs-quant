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

import datetime as dt
import logging
from typing import Dict, List, Tuple

from gs_quant.session import GsSession
from gs_quant.target.risk import Scenario

_logger = logging.getLogger(__name__)


class GsScenarioApi:
    """GS Scenarios API client implementation"""

    @classmethod
    def create_scenario(cls, scenario: Scenario) -> Scenario:
        return GsSession.current._post('/risk/scenarios', scenario, cls=Scenario)

    @classmethod
    def get_scenario(cls, scenario_id: str) -> Scenario:
        return GsSession.current._get(f'/risk/scenarios/{scenario_id}', cls=Scenario)

    @classmethod
    def get_many_scenarios(cls,
                           ids: List[str] = None,
                           names: List[str] = None,
                           limit: int = 100,
                           **kwargs) -> Tuple[Scenario, ...]:
        url = f'/risk/scenarios?limit={limit}'
        if ids:
            url += f'&id={"&id=".join(ids)}'
        if names:
            url += f'&name={"&name=".join(names)}'
        if kwargs:
            for k, v in kwargs.items():
                url += f'&{k}={f"&{k}=".join(v)}' if isinstance(v, list) else f'&{k}={v}'

        return GsSession.current._get(url, cls=Scenario).get('results', [])

    @classmethod
    def get_scenario_by_name(cls, name: str) -> Scenario:
        url = f"/risk/scenarios?name={name}"
        ret = GsSession.current._get(url, cls=Scenario)
        num_found = ret.get('totalResults', 0)

        if num_found == 0:
            raise ValueError(f'Scenario {name}not found')
        elif num_found > 1:
            raise ValueError(f'More than one scemario named {name}')
        else:
            return ret['results'][0]

    @classmethod
    def update_scenario(cls, scenario: Scenario) -> Dict:
        return GsSession.current._put(f'/risk/scenarios/{scenario.id_}', scenario, cls=Scenario)

    @classmethod
    def delete_scenario(cls, scenario_id: str) -> Dict:
        return GsSession.current._delete(f'/risk/scenarios/{scenario_id}')

    @classmethod
    def calculate_scenario(cls, request: Dict) -> Dict:
        return GsSession.current._post('/scenarios/calculate', request)


class GsFactorScenarioApi(GsScenarioApi):
    def __init__(self):
        super().__init__()

    @classmethod
    def get_many_scenarios(cls,
                           ids: List[str] = None,
                           names: List[str] = None,
                           limit: int = 100,
                           type: str = None,
                           risk_model: str = None,
                           shocked_factors: List[str] = None,
                           shocked_factor_categories: List[str] = None,
                           start_date: dt.date = None,
                           end_date: dt.date = None,
                           tags: List[str] = None) -> Tuple[Scenario, ...]:
        factor_scenario_args = {}
        if risk_model:
            factor_scenario_args['riskModel'] = risk_model
        if type:
            factor_scenario_args['factorScenarioType'] = type
        if shocked_factors:
            factor_scenario_args['shockedFactor'] = shocked_factors
        if shocked_factor_categories:
            factor_scenario_args['shockedFactorCategory'] = shocked_factor_categories
        if start_date:
            factor_scenario_args['historicalSimulationStartDate'] = start_date
        if end_date:
            factor_scenario_args['historicalSimulationEndDate'] = end_date
        if tags:
            factor_scenario_args['tags'] = tags

        many_scenarios = super().get_many_scenarios(ids=ids, names=names, limit=limit, **factor_scenario_args)
        many_scenarios = tuple([scenario for scenario in many_scenarios if scenario.type_])

        return many_scenarios

    @classmethod
    def calculate_scenario(cls, calculation_request: Dict) -> Dict:
        return super().calculate_scenario(request=calculation_request)
