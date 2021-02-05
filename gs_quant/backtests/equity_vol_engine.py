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

from gs_quant.backtests.strategy_systematic import StrategySystematic, DeltaHedgeParameters, TradeInMethod
from gs_quant.backtests import triggers as t
from gs_quant.backtests import actions as a
from gs_quant.instrument import EqOption, EqVarianceSwap
from gs_quant.risk import EqDelta
from gs_quant.target.backtests import FlowVolBacktestMeasure
import pandas as pd
from functools import reduce


class BacktestResult(object):
    def __init__(self, results):
        self._results = results

    def get_measure_series(self, measure: FlowVolBacktestMeasure):
        df = pd.DataFrame(self._results[measure.value])
        df['date'] = pd.to_datetime(df['date'])
        return df.set_index('date').value


class EquityVolEngine(object):

    @classmethod
    def supports_strategy(cls, strategy):
        if len(strategy.initial_portfolio) > 0:
            return False

        if len(strategy.triggers) > 2:
            return False

        if not all((isinstance(x, t.PeriodicTrigger)) for x in strategy.triggers):
            return False

        all_actions = reduce(lambda x, y: x + y, (map(lambda x: x.actions, strategy.triggers)))
        if not all((isinstance(x, a.AddTradesQuantityScaledAction) | isinstance(x, a.HedgeAction))
                   for x in all_actions):
            return False

        # no duplicate actions
        if not len(set(map(lambda x: type(x), all_actions))) == len(all_actions):
            return False

        for trigger in strategy.triggers:
            # could be the equity options or the hedge
            if len(trigger.actions) != 1:
                return False

            action = trigger.actions[0]
            if not trigger.trigger_requirements.frequency == action.trade_duration:
                return False

            if isinstance(action, a.AddTradesQuantityScaledAction):
                if not all((isinstance(p, EqOption) | isinstance(p, EqVarianceSwap))
                           for p in action.priceables):
                    return False
                if action.trade_quantity is None or action.trade_quantity_type is None:
                    return False
            elif isinstance(action, a.HedgeAction):
                if not action.risk == EqDelta:
                    return False
                if not trigger.trigger_requirements.frequency == 'B':
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
        trade_quantity = None
        trade_quantity_type = None
        hedge = None
        for trigger in strategy.triggers:
            action = trigger.actions[0]
            if isinstance(action, a.AddTradesQuantityScaledAction):
                underlier_list = action.priceables
                roll_frequency = action.trade_duration
                trade_quantity = action.trade_quantity
                trade_quantity_type = action.trade_quantity_type
            elif isinstance(action, a.HedgeAction):
                if trigger.trigger_requirements.frequency == 'B':
                    frequency = 'Daily'
                else:
                    raise RuntimeError('unrecognised hedge frequency')
                hedge = DeltaHedgeParameters(frequency=frequency)

        strategy = StrategySystematic(name="Flow Vol Backtest",
                                      underliers=underlier_list,
                                      delta_hedge=hedge,
                                      quantity=trade_quantity,
                                      quantity_type=trade_quantity_type,
                                      trade_in_method=TradeInMethod.FixedRoll,
                                      roll_frequency=roll_frequency,
                                      # entry_signal= Mapping of Date->0/1,
                                      # exit_signal= Mapping of Date->0/1
                                      )

        result = strategy.backtest(start, end)
        return BacktestResult(result.risks)
