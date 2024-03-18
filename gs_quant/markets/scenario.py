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

from gs_quant.api.gs.scenarios import GsFactorScenarioApi
from gs_quant.markets.factor import Factor
from gs_quant.target.risk import Scenario as TargetScenario, FactorScenarioType
from enum import Enum
from typing import List, Union, Dict
from pydash import get

import datetime as dt
import pandas as pd


class ScenarioCalculationType(Enum):
    FACTOR_SCENARIO = "Factor Scenario"


class ScenarioResultsMode(Enum):
    POSITIONED_ENTITY = "Positioned Entity"
    POSITIONS = "Positions"


class FactorShock:
    """ Marquee Factor Shock """

    def __init__(self,
                 factor: Union[str, Factor],
                 shock: float):
        self.__factor = factor
        self.__shock = shock

    @property
    def factor(self) -> Union[str, Factor]:
        """ Get factor being shocked"""
        return self.__factor

    @factor.setter
    def factor(self, factor: Union[str, Factor]):
        self.__factor = factor

    @property
    def shock(self) -> float:
        """ Get factor being shocked"""
        return self.__shock

    @shock.setter
    def shock(self, shock: float):
        self.__shock = shock

    def to_dict(self):
        return {
            "factor": self.factor.name if isinstance(self.factor, Factor) else self.factor,
            "shock": self.shock
        }

    @classmethod
    def from_dict(cls, obj):
        return FactorShock(factor=obj.get("factor"), shock=obj.get("shock"))


class FactorShockParameters:
    def __init__(self,
                 factor_shocks: List[FactorShock] = None,
                 propagate_shocks: bool = None,
                 risk_model: str = None):
        self.__factor_shocks = factor_shocks
        self.__propagate_shocks = propagate_shocks
        self.__risk_model = risk_model

    @property
    def factor_shocks(self) -> List[FactorShock]:
        return self.__factor_shocks

    @factor_shocks.setter
    def factor_shocks(self, factor_shocks: Union[List[FactorShock], Dict, pd.DataFrame]):
        if isinstance(factor_shocks, pd.DataFrame):
            factor_shocks_as_dict = factor_shocks.to_dict(orient='split')
            self.__factor_shocks = [FactorShock(factor=f, shock=s) for f, s in
                                    zip(factor_shocks_as_dict.get('columns'), factor_shocks_as_dict.get('data'))]
        elif isinstance(factor_shocks, Dict):
            self.__factor_shocks = [FactorShock(factor=k, shock=v) for k, v in factor_shocks.items()]
        else:
            self.__factor_shocks = factor_shocks

    @property
    def propagate_shocks(self) -> bool:
        return self.__propagate_shocks

    @propagate_shocks.setter
    def propagate_shocks(self, propagate_shocks: bool):
        self.__propagate_shocks = propagate_shocks

    @property
    def risk_model(self) -> str:
        return self.__risk_model

    @classmethod
    def from_dict(cls, obj: Dict) -> 'FactorShockParameters':
        return cls(factor_shocks=[FactorShock.from_dict(f_shock) for f_shock in obj.get('factorShocks')],
                   risk_model=obj.get("riskModel"),
                   propagate_shocks=obj.get("propagateShocks"))

    def to_dict(self) -> Dict:
        return {
            "riskModel": self.risk_model,
            "propagateShocks": self.propagate_shocks,
            "factorShocks": [f_shock.to_dict() for f_shock in self.factor_shocks]
        }


class HistoricalSimulationParameters:
    def __init__(self,
                 start_date: dt.date = None,
                 end_date: dt.date = None):
        self.__start_date = start_date
        self.__end_date = end_date

    @property
    def start_date(self) -> dt.date:
        return self.__start_date

    @start_date.setter
    def start_date(self, start_date: dt.date):
        self.__start_date = start_date

    @property
    def end_date(self) -> dt.date:
        return self.__end_date

    @end_date.setter
    def end_date(self, end_date: dt.date):
        self.__end_date = end_date

    @classmethod
    def from_dict(cls, obj: Dict) -> 'HistoricalSimulationParameters':
        return cls(start_date=dt.datetime.strptime(obj.get('startDate'), "%Y-%m-%d").date(),
                   end_date=dt.datetime.strptime(obj.get('endDate'), "%Y-%m-%d").date())

    def to_dict(self) -> Dict:
        return {"startDate": self.start_date, "endDate": self.end_date}


ScenarioParameters = Union[FactorShockParameters, HistoricalSimulationParameters]


class FactorScenario:
    """ Marquee Factor-based Scenario """

    def __init__(self,
                 name: str,
                 scenario_type: Union[str, FactorScenarioType],
                 parameters: Union[Dict, HistoricalSimulationParameters, FactorShockParameters],
                 id_: str = None,
                 description: str = None,
                 tags: List[str] = None):
        self.__id = id_
        self.__name = name
        self.__scenario_type = scenario_type
        self.__description = description
        self.__parameters = parameters \
            if any([isinstance(parameters, FactorShockParameters),
                    isinstance(parameters, HistoricalSimulationParameters)]) \
            else FactorShockParameters.from_dict(parameters) if scenario_type == FactorScenarioType.Factor_Shock \
            else HistoricalSimulationParameters.from_dict(parameters)
        self.__tags = tags

    @property
    def id(self) -> str:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = name

    @property
    def scenario_type(self) -> Union[str, FactorScenarioType]:
        return self.__scenario_type

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, description: str):
        self.description = description

    @property
    def parameters(self) -> ScenarioParameters:
        return self.__parameters

    @parameters.setter
    def parameters(self, parameters: ScenarioParameters):
        self.__parameters = parameters

    @property
    def tags(self) -> List[str]:
        return self.__tags

    @tags.setter
    def tags(self, tags: List[str]):
        self.__tags = tags

    @classmethod
    def from_dict(cls, scenario_as_dict: Dict) -> 'FactorScenario':
        scenario_data = {
            "name": scenario_as_dict.get('name'),
            "description": scenario_as_dict.get('description'),
            "id_": scenario_as_dict.get('id'),
            "scenario_type": scenario_as_dict.get('type'),
            "parameters": get(scenario_as_dict, 'parameters', None),
            "tags": scenario_as_dict.get('tags')
        }
        return cls(**scenario_data)

    @classmethod
    def from_target(cls, target_scenario: TargetScenario):
        scenario = cls(id_=target_scenario.id,
                       name=target_scenario.name,
                       scenario_type=target_scenario.type,
                       parameters=target_scenario.parameters,
                       description=target_scenario.description,
                       tags=target_scenario.tags)

        return scenario

    @classmethod
    def get(cls, scenario_id: str):
        scenario = GsFactorScenarioApi.get_scenario(scenario_id)
        return cls.from_target(scenario)

    @classmethod
    def get_by_name(cls, scenario_name: str):
        scenario = GsFactorScenarioApi.get_scenario_by_name(scenario_name)
        return cls.from_target(scenario)

    @classmethod
    def get_many(cls,
                 ids: List[str] = None,
                 names: List[str] = None,
                 type: Union[str, FactorScenarioType] = None,
                 risk_model: str = None,
                 shocked_factors: List[str] = None,
                 shocked_factor_categories: List[str] = None,
                 propagated_shocks: bool = None,
                 start_date: dt.date = None,
                 end_date: dt.date = None) -> List['FactorScenario']:
        many_scenarios_as_dict = GsFactorScenarioApi.get_many_scenarios(
            ids,
            names=names,
            type=type,
            risk_model=risk_model,
            shocked_factors=shocked_factors,
            shocked_factor_categories=shocked_factor_categories,
            propagated_shocks=propagated_shocks,
            start_date=start_date,
            end_date=end_date)

        return [cls.from_target(scenario_as_target) for scenario_as_target in many_scenarios_as_dict]

    def save(self):
        """ Update factor scenario or Create it if it does not exist"""
        target_scenario = TargetScenario(name=self.name,
                                         type_=self.scenario_type,
                                         description=self.description,
                                         parameters=self.parameters.to_dict(),
                                         tags=tuple(self.tags))

        if self.id:
            target_scenario.id_ = self.id
            GsFactorScenarioApi.update_scenario(target_scenario)
        else:
            GsFactorScenarioApi.create_scenario(target_scenario)


Scenario = Union[FactorScenario]
