from gs_quant.context_base import ContextBaseWithDefault
from gs_quant.markets.core import PricingContext
from gs_quant.target.risk import CurveScenario, MarketDataScenario, MarketDataPattern, MarketDataShock,\
    MarketDataPatternAndShock, MarketDataShockBasedScenario as __MarketDataShockBasedScenario

from typing import Mapping, Union


class MarketDataShockBasedScenario(__MarketDataShockBasedScenario):

    def __init__(self, shocks: Mapping[MarketDataPattern, MarketDataShock]):
        super().__init__(tuple(MarketDataPatternAndShock(p, s) for p, s in shocks.items()))


class ScenarioContext(MarketDataScenario, ContextBaseWithDefault):

    """A context containing scenario parameters, such as shocks"""

    def __init__(self, scenario: Union[CurveScenario, MarketDataShockBasedScenario]=None, subtract_base: bool = False):
        super().__init__(scenario, subtract_base)

    def _on_enter(self):
        PricingContext.current.__enter__()

    def _on_exit(self, exc_type, exc_val, exc_tb):
        PricingContext.current.__exit__(exc_type, exc_val, exc_tb)
