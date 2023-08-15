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
from abc import abstractmethod
from datetime import date
from typing import Union, Iterable, Any, TypeVar

from gs_quant.backtests.actions import TAction
from gs_quant.backtests.backtest_objects import TBaseBacktest


class ActionHandler:

    def __init__(
            self,
            action: TAction
    ) -> None:
        self._action = action

    @property
    def action(self) -> TAction:
        return self._action

    @abstractmethod
    def apply_action(
            self,
            state: Union[date, Iterable[date]],
            backtest: TBaseBacktest,
            trigger_info: Any,
    ) -> Any:
        pass


TActionHandler = TypeVar('TActionHandler', bound='ActionHandler')


class ActionHandlerBaseFactory:

    @abstractmethod
    def get_action_handler(
            self,
            action: TAction
    ) -> TActionHandler:
        pass
