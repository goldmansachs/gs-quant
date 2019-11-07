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
from abc import ABCMeta
from typing import Mapping, Union

from gs_quant.context_base import ContextBaseWithDefault, ContextMeta
from gs_quant.markets.core import PricingContext
from gs_quant.target.risk import CarryScenario, CurveScenario, MarketDataScenario, MarketDataPattern, MarketDataShock,\
    MarketDataPatternAndShock, MarketDataShockBasedScenario as __MarketDataShockBasedScenario


class __ScenarioMeta(ABCMeta, ContextMeta):
    pass


class MarketDataShockBasedScenario(__MarketDataShockBasedScenario):

    def __init__(self, shocks: Mapping[MarketDataPattern, MarketDataShock]):
        super().__init__(tuple(MarketDataPatternAndShock(p, s) for p, s in shocks.items()))


class ScenarioContext(MarketDataScenario, ContextBaseWithDefault, metaclass=__ScenarioMeta):

    """A context containing scenario parameters, such as shocks"""

    def __init__(self, scenario: Union[CarryScenario, CurveScenario, MarketDataShockBasedScenario]
                 = None, subtract_base: bool = False):
        super().__init__(scenario, subtract_base)

    def _on_enter(self):
        PricingContext.current.__enter__()

    def _on_exit(self, exc_type, exc_val, exc_tb):
        PricingContext.current.__exit__(exc_type, exc_val, exc_tb)
