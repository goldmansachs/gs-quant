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
from gs_quant.entities.entitlements import Entitlements
from gs_quant.errors import MqValueError
from enum import Enum
from typing import List, Union, Dict
from pydash import get
from copy import deepcopy

import datetime as dt
import pandas as pd


class ScenarioCalculationType(Enum):
    FACTOR_SCENARIO = "Factor Scenario"


class FactorShock:
    """ Marquee Factor Shock """

    def __init__(self,
                 factor: Union[str, Factor],
                 shock: float):
        self.__factor = factor
        self.__shock = shock

    def __eq__(self, other) -> bool:
        if not isinstance(other, FactorShock):
            return False

        factor_name = self.factor.name if isinstance(self.factor, Factor) else self.factor
        other_factor_name = other.factor.name if isinstance(other.factor, Factor) else other.factor

        return factor_name == other_factor_name and self.shock == other.shock

    def __repr__(self):
        return '%r(factor=%r, shock=%r)' % (self.__class__.__name__,
                                            self.factor,
                                            self.shock)

    @property
    def factor(self) -> Union[str, Factor]:
        """ Get factor being shocked"""
        return self.__factor

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

    def __eq__(self, other) -> bool:
        if not isinstance(other, FactorShockParameters):
            return False

        return \
            self.factor_shocks == other.factor_shocks \
            and self.propagate_shocks == other.propagate_shocks and self.risk_model == other.risk_model

    def __repr__(self):
        return '%r(risk_model=%r, propagate_shocks=%r, factor_shocks=%r)' % (self.__class__.__name__,
                                                                             self.risk_model,
                                                                             self.propagate_shocks,
                                                                             self.factor_shocks)

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

    def __eq__(self, other) -> bool:
        if not isinstance(other, HistoricalSimulationParameters):
            return False

        return self.start_date == other.start_date and self.end_date == other.end_date

    def __repr__(self):
        return '%r(start_date=%r, end_date=%r)' % (self.__class__.__name__, self.start_date, self.end_date)

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
                 type: Union[str, FactorScenarioType],
                 parameters: Union[Dict, HistoricalSimulationParameters, FactorShockParameters],
                 entitlements: Union[Dict, Entitlements] = None,
                 id_: str = None,
                 description: str = None,
                 tags: List[str] = None):
        self.__id = id_
        self.__name = name
        self.__type = type
        self.__description = description
        self.__parameters = parameters \
            if any([isinstance(parameters, FactorShockParameters),
                    isinstance(parameters, HistoricalSimulationParameters)]) \
            else FactorShockParameters.from_dict(parameters) if type == FactorScenarioType.Factor_Shock \
            else HistoricalSimulationParameters.from_dict(parameters)
        self.__entitlements = entitlements
        self.__tags = tags

    def __repr__(self):
        instance_repr = '%r(id=%r, name=%r, description=%r, type=%r, parameters=%r, entitlements=%r, tags=%r)' % (
            self.__class__.__name__,
            self.id,
            self.name,
            self.description,
            self.type,
            self.parameters.__repr__(),
            self.entitlements.__repr__(),
            self.tags)

        return instance_repr

    def __str__(self):
        s = "{}('id={}', 'name={}', 'description={}', 'type={}', 'parameters={}'".format(self.__class__.__name__,
                                                                                         self.id,
                                                                                         self.name,
                                                                                         self.description,
                                                                                         self.type.value,
                                                                                         self.parameters.__repr__())

        s += ")"
        return s

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
    def type(self) -> Union[str, FactorScenarioType]:
        return self.__type

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, description: str):
        self.__description = description

    @property
    def parameters(self) -> ScenarioParameters:
        return self.__parameters

    @parameters.setter
    def parameters(self, parameters: ScenarioParameters):
        self.__parameters = parameters

    @property
    def entitlements(self) -> Entitlements:
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, entitlements: Union[Dict, Entitlements]):
        self.__entitlements = entitlements

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
            "type": scenario_as_dict.get('type'),
            "parameters": get(scenario_as_dict, 'parameters', None),
            "entitlements": get(scenario_as_dict, 'entitlements', None),
            "tags": scenario_as_dict.get('tags')
        }
        return cls(**scenario_data)

    @classmethod
    def from_target(cls, target_scenario: TargetScenario):
        parameters = FactorShockParameters.from_dict(target_scenario.parameters) \
            if target_scenario.type == FactorScenarioType.Factor_Shock else \
            HistoricalSimulationParameters.from_dict(target_scenario.parameters)
        scenario = cls(id_=target_scenario.id,
                       name=target_scenario.name,
                       type=target_scenario.type,
                       parameters=parameters,
                       entitlements=Entitlements.from_target(target_scenario.entitlements),
                       description=target_scenario.description,
                       tags=target_scenario.tags)

        return scenario

    @classmethod
    def get(cls, scenario_id: str) -> 'FactorScenario':
        """
        Get a scenario by its name

        :param scenario_id: The ID of the scenario

        :return: Instance of factor scenario

        :func:`get_by_name` :func:`get_many`
        """
        scenario = GsFactorScenarioApi.get_scenario(scenario_id)
        return cls.from_target(scenario)

    @classmethod
    def get_by_name(cls, scenario_name: str) -> 'FactorScenario':
        """
        Get a scenario by its name

        :param scenario_name: The name of the scenario

        :return: Instance of factor scenario

        :func:`get_many` :func:`get`
        """
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
                 end_date: dt.date = None,
                 tags: List[str] = None,
                 limit: int = 100) -> List['FactorScenario']:
        """
        Get many factor scenarios from Marquee

        :param ids: List of unique Marquee Identifiers
        :param names: Names of requested scenarios
        :param type: The type of the scenario
        :param risk_model: Filter by the risk model
        :param shocked_factors: Return scenarios that shock requested factors.
        :param shocked_factor_categories: Filter scenarios that shock factors in the requested factor categories
        :param propagated_shocks: Return factor shock scenarios that propagate initial factor shocks to other
            non-shocked factors
        :param start_date: Return historical simulation scenarios with an start date that is greater or equal than this
            date. This is only applicable to historical simulation
        :param end_date: Return historical simulation scenarios with an end date that is lower or equal than this date.
            This is only applicable to historical simulation
        :param tags: Returns scenario with any of the requested tags
        :param limit: limit of number of models in response

        :return: list of Factor Shock scenario

        **Usage**

        >>> many_factor_shock_scenarios = FactorScenario.get_many(risk_model="MODEL_ID",
        ...                                                      propagated_shocks=True,
        ...                                                      type="Factor Shock")

        >>> value_shocks_scenarios = FactorScenario.get_many(risk_model="AXIOMA_AXWW4M",
        ...                                                  shocked_factors=["Value"],
        ...                                                  type="Factor Shock")

        >>> many_historical_simulation_scenarios = FactorScenario.get_many(type="Factor Historical Simulation",
        ...                                                                start_date=dt.date(2010, 1, 1),
        ...                                                                end_date=dt.date(2024, 1, 1))

        **See also**

        :func:`get_by_name` :func:`get`
        """
        many_scenarios_as_dict = GsFactorScenarioApi.get_many_scenarios(
            ids=ids,
            names=names,
            type=type.value if isinstance(type, FactorScenarioType) else type,
            risk_model=risk_model,
            shocked_factors=shocked_factors,
            shocked_factor_categories=shocked_factor_categories,
            start_date=start_date,
            end_date=end_date,
            tags=tags,
            limit=limit)

        all_scenarios = [cls.from_target(scenario_as_target) for scenario_as_target in many_scenarios_as_dict]

        if propagated_shocks is not None:
            return [scenario for scenario in all_scenarios if
                    (scenario.parameters.propagate_shocks == propagated_shocks) or
                    scenario.type != FactorScenarioType.Factor_Shock]

        return all_scenarios

    def save(self):
        """ Update factor scenario or Create it if it does not exist"""
        target_scenario = TargetScenario(name=self.name,
                                         type_=self.type,
                                         description=self.description if self.description else None,
                                         parameters=self.parameters.to_dict(),
                                         entitlements=self.entitlements.to_target() if self.entitlements else None,
                                         tags=tuple(self.tags) if self.tags else ())

        if self.id:
            target_scenario.id_ = self.id
            GsFactorScenarioApi.update_scenario(target_scenario)
        else:
            scenario = GsFactorScenarioApi.create_scenario(target_scenario)
            self.__id = scenario.id

    def delete(self):
        """Deletes factor scenario from Marquee"""
        if not self.id:
            raise MqValueError("Cannot delete scenario that has not been created in Marquee")

        GsFactorScenarioApi.delete_scenario(self.id)

    def clone(self):
        """
        Clones an existing scenario

        :return: New scenario instance with identical parameters

        **Usage**


        >>> from gs_quant.markets.scenario import FactorScenario
        >>>
        >>> initial_scenario = FactorScenario.get("SCENARIO_ID")
        >>> clone = initial_scenario.clone()
        >>> clone.save()

        **See also**

        :func:`save`
        """
        parameters = deepcopy(self.parameters)

        return FactorScenario(name=f"{self.name} copy", description=self.description,
                              type=self.type, parameters=parameters)


Scenario = Union[FactorScenario]
