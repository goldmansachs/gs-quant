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

from gs_quant.backtests.strategy_systematic import StrategySystematic, DeltaHedgeParameters, QuantityType, TradeInMethod
from gs_quant.backtests import triggers as t
from gs_quant.backtests import actions as a
from gs_quant.instrument import EqOption, EqVarianceSwap
from gs_quant.risk import EqDelta


class EquityVolEngine(object):

    @classmethod
    def supports_strategy(cls, strategy):
        for trigger in strategy.triggers:
            if isinstance(trigger, t.PeriodicTrigger):
                # could be the equity options or the hedge
                if len(trigger.actions) != 1:
                    return False
                elif isinstance(trigger.actions[0], a.AddTradeAction):
                    if not all((isinstance(p, EqOption) | isinstance(p, EqVarianceSwap))
                               for p in trigger.actions[0].priceables):
                        return False
                elif isinstance(trigger.actions[0], a.HedgeAction):
                    if not isinstance(trigger.actions[0].risk, EqDelta):
                        return False
            else:
                return False
        return True

    @classmethod
    def run_backtest(cls, strategy, start, end):
        if not EquityVolEngine.supports_strategy(strategy):
            raise RuntimeError('unsupported strategy')
        underlier_list = None
        roll_frequency = None
        hedge = None
        for trigger in strategy.triggers:
            if isinstance(trigger, t.PeriodicTrigger):
                if isinstance(trigger.actions[0], a.AddTradeAction):
                    underlier_list = trigger.actions[0].priceables
                    roll_frequency = trigger.actions[0].trade_duration
                elif isinstance(trigger.actions[0], a.HedgeAction):
                    if trigger.trigger_requirements.frequency == '1B':
                        frequency = 'Daily'
                    elif trigger.trigger_requirements.frequency == '1M':
                        frequency = 'Monthly'
                    else:
                        raise RuntimeError('unrecognised hedge frequency')
                    hedge = DeltaHedgeParameters(frequency=frequency)

        strategy = StrategySystematic(name="Mock Test",
                                      underliers=underlier_list,
                                      delta_hedge=hedge,
                                      quantity=-1,
                                      quantity_type=QuantityType.Quantity,
                                      trade_in_method=TradeInMethod.FixedRoll,
                                      roll_frequency=roll_frequency,
                                      # entry_signal= Mapping of Date->0/1,
                                      # exit_signal= Mapping of Date->0/1
                                      )
        result = strategy.backtest(start, end)
        perf = result.performance
        return perf
