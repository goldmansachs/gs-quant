"""
Copyright 2019 Goldman Sachs.
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

from typing import Union, Iterable, Optional
import datetime
from enum import Enum
import pandas as pd

from gs_quant.backtests.actions import Action
from gs_quant.backtests.backtest_utils import make_list
from gs_quant.backtests.generic_engine import BackTest


class TriggerDirection(Enum):
    ABOVE = 1
    BELOW = 2
    EQUAL = 3


class TriggerRequirements(object):
    def __init__(self):
        pass


class PeriodicTriggerRequirements(TriggerRequirements):
    def __init__(self, start_date=None, end_date=None, frequency=None, calendar=None):
        super().__init__()
        self.start_date = start_date
        self.end_date = end_date
        self.frequency = frequency
        self.calendar = calendar


class MktTriggerRequirements(TriggerRequirements):
    def __init__(self, data_source, trigger_level, direction):
        super().__init__()
        self.data_source = data_source
        self.trigger_level = trigger_level
        self.direction = direction


class RiskTriggerRequirements(TriggerRequirements):
    def __init__(self, strategy_results, risk, trigger_level, direction):
        super().__init__()
        self.strategy_results = strategy_results
        self.risk = risk
        self.trigger_level = trigger_level
        self.direction = direction


class AggregateTriggerRequirements(TriggerRequirements):
    def __init__(self, triggers: Iterable[object]):
        super().__init__()
        self.triggers = triggers


class Trigger(object):

    def __init__(self, trigger_requirements: Optional[TriggerRequirements], actions: Union[Action, Iterable[Action]]):
        self._trigger_requirements = trigger_requirements
        self._actions = make_list(actions)
        self._risks = [x.risk for x in self.actions if x.risk is not None]
        self._deterministic = True

    def has_triggered(self, state: datetime.date, backtest: BackTest = None) -> bool:
        """
        implemented by sub classes
        :param state:
        :param backtest:
        :return:
        """
        raise RuntimeError('has_triggered to be implemented by subclass')

    @property
    def deterministic(self):
        return self._deterministic

    @property
    def actions(self):
        return self._actions

    @property
    def trigger_requirements(self):
        return self._trigger_requirements

    @property
    def risks(self):
        return self._risks


class PeriodicTrigger(Trigger):
    def __init__(self,
                 trigger_requirements: PeriodicTriggerRequirements,
                 actions: Union[Action, Iterable[Action]]):
        super().__init__(trigger_requirements, actions)
        self._trigger_dates = None

    def get_trigger_dates(self) -> [datetime.date]:
        if not self._trigger_dates:
            self._trigger_dates = pd.date_range(start=self._trigger_requirements.start_date,
                                                end=self._trigger_requirements.end_date,
                                                freq=self._trigger_requirements.frequency).to_pydatetime().tolist()
            self._trigger_dates = [my_date.date() for my_date in self._trigger_dates]
        return self._trigger_dates

    def has_triggered(self, state: datetime.date, backtest: BackTest = None) -> bool:
        if not self._trigger_dates:
            self.get_trigger_dates()
        return state in self._trigger_dates


class MktTrigger(Trigger):
    def __init__(self,
                 trigger_requirements: MktTriggerRequirements,
                 actions: Union[Action, Iterable[Action]]):
        super().__init__(trigger_requirements, actions)

    def has_triggered(self, state: datetime.date, backtest: BackTest = None) -> bool:
        data_value = self._trigger_requirements.data_source.get_data(state)
        if self._trigger_requirements.direction == TriggerDirection.ABOVE:
            if data_value > self._trigger_requirements.trigger_level:
                return True
        elif self._trigger_requirements.direction == TriggerDirection.BELOW:
            if data_value < self._trigger_requirements.trigger_level:
                return True
        else:
            if data_value == self._trigger_requirements.trigger_level:
                return True
        return False


class StrategyRiskTrigger(Trigger):
    def __init__(self,
                 trigger_requirements: RiskTriggerRequirements,
                 actions: Union[Action, Iterable[Action]]):
        super().__init__(trigger_requirements, actions)
        self._deterministic = False
        self._risks += [trigger_requirements.risk]

    def has_triggered(self, state: datetime.date, backtest: BackTest = None) -> bool:
        risk_value = backtest[state][self._trigger_requirements.risk]
        if self._trigger_requirements.direction == TriggerDirection.ABOVE:
            if risk_value > self._trigger_requirements.trigger_level:
                return True
        elif self._trigger_requirements.direction == TriggerDirection.BELOW:
            if risk_value < self._trigger_requirements.trigger_level:
                return True
        else:
            if risk_value == self._trigger_requirements.trigger_level:
                return True
        return False


class AggregateTrigger(Trigger):
    def __init__(self, triggers: Iterable[Trigger]):
        actions = []
        for t in triggers:
            actions += [action for action in t.actions]
        super().__init__(AggregateTriggerRequirements(triggers), actions)

    def has_triggered(self, state: datetime.date, backtest: BackTest = None) -> bool:
        for trigger in self._trigger_requirements.triggers:
            if not trigger.has_triggered(state, backtest):
                return False
        return True
