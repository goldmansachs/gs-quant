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

from gs_quant.backtests.actions import Action
from gs_quant.backtests.backtest_objects import BackTest
from typing import Union, Iterable
from datetime import date


class ActionHandler(object):
    def __init__(self, action: Action):
        self._action = action

    @property
    def action(self) -> Action:
        return self._action

    def apply_action(self, state: Union[date, Iterable[date]], backtest: BackTest):
        """
        Used by the Generic Engine
        :param backtest:
        :param state:
        :return:
        """
        raise RuntimeError('apply_action must be implemented by subclass')


class ActionHandlerBaseFactory(object):
    def get_action_handler(self, action: str) -> ActionHandler:
        """
        :param action: the source action object
        :return: handler for action
        """
        raise RuntimeError('get_action_handler must be implemented by subclass')
