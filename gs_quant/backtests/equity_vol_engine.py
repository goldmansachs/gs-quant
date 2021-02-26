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
from gs_quant.target.backtests import FlowVolBacktestMeasure, BacktestSignalSeriesItem, BacktestTradingQuantityType
import pandas as pd
from functools import reduce


class BacktestResult(object):
    def __init__(self, results):
        self._results = results

    def get_measure_series(self, measure: FlowVolBacktestMeasure):
        df = pd.DataFrame(self._results.risks[measure.value])
        df['date'] = pd.to_datetime(df['date'])
        return df.set_index('date').value

    def get_portfolio_history(self):
        data = []
        for item in self._results.portfolio:
            positions = list(map(lambda x: dict({'date': item['date'], 'quantity': x['quantity']}, **x['instrument']),
                                 item['positions']))
            data = data + positions

        return pd.DataFrame(data)

    def get_trade_history(self):
        data = []
        for item in self._results.portfolio:
            for transaction in item['transactions']:
                trades = list(map(lambda x: dict(
                    {'date': item['date'], 'quantity': x['quantity'], 'transactionType': transaction['type']},
                    **x['instrument']), transaction['trades']))
                data = data + trades

        return pd.DataFrame(data)


class EquityVolEngine(object):

    @classmethod
    def supports_strategy(cls, strategy):
        if len(strategy.initial_portfolio) > 0:
            return False

        # Validate Triggers

        if len(strategy.triggers) > 3:
            return False

        if not all(isinstance(x, (t.AggregateTrigger, t.PeriodicTrigger)) for x in strategy.triggers):
            return False

        # aggregate triggers composed of a dated and portfolio trigger define a signal
        aggregate_triggers = [x for x in strategy.triggers if isinstance(x, t.AggregateTrigger)]
        for at in aggregate_triggers:
            if not len(at.triggers) == 2:
                return False
            if not len([x for x in at.triggers if isinstance(x, t.DateTrigger)]) == 1:
                return False
            portfolio_triggers = [x for x in at.triggers if isinstance(x, t.PortfolioTrigger)]
            if not len(portfolio_triggers) == 1:
                return False
            if not (portfolio_triggers[0].trigger_requirements.data_source == 'len' and
                    portfolio_triggers[0].trigger_requirements.trigger_level == 0):
                return False

        # Validate Actions

        all_actions = reduce(lambda acc, x: acc + x, (map(lambda x: x.actions, strategy.triggers)), [])
        if not all(isinstance(x, (a.EnterPositionQuantityScaledAction, a.HedgeAction, a.ExitPositionAction))
                   for x in all_actions):
            return False

        # no duplicate actions
        if not len(set(map(lambda x: type(x), all_actions))) == len(all_actions):
            return False

        all_child_triggers = reduce(lambda acc, x: acc + x,
                                    map(lambda x: x.triggers if isinstance(x, t.AggregateTrigger) else [x],
                                        strategy.triggers), [])

        for trigger in all_child_triggers:
            if isinstance(trigger, t.PortfolioTrigger):
                continue

            # action one of enter position, exit position, hedge
            if len(trigger.actions) != 1:
                return False

            action = trigger.actions[0]
            if isinstance(action, a.EnterPositionQuantityScaledAction):
                if isinstance(trigger, t.PeriodicTrigger) and \
                        not trigger.trigger_requirements.frequency == action.trade_duration:
                    return False
                if not all((isinstance(p, EqOption) | isinstance(p, EqVarianceSwap))
                           for p in action.priceables):
                    return False
                if action.trade_quantity is None or action.trade_quantity_type is None:
                    return False
            elif isinstance(action, a.HedgeAction):
                if not trigger.trigger_requirements.frequency == action.trade_duration:
                    return False
                if not action.risk == EqDelta:
                    return False
                if not trigger.trigger_requirements.frequency == 'B':
                    return False
            elif isinstance(action, a.ExitPositionAction):
                continue
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
        trade_in_signals = None
        trade_out_signals = None
        hedge = None
        index_initial_value = 0
        for trigger in strategy.triggers:
            if isinstance(trigger, t.AggregateTrigger):
                child_triggers = trigger.triggers

                date_trigger = [x for x in child_triggers if isinstance(x, t.DateTrigger)][0]
                date_signal = list(map(lambda x: BacktestSignalSeriesItem(x, True),
                                       date_trigger.trigger_requirements.dates))

                portfolio_trigger = [x for x in child_triggers if isinstance(x, t.PortfolioTrigger)][0]
                trigger_requirements = portfolio_trigger.trigger_requirements
                if trigger_requirements.direction == t.TriggerDirection.EQUAL and \
                        trigger_requirements.trigger_level == 0:
                    is_trade_in = True
                else:
                    is_trade_in = False

                if is_trade_in:
                    trade_in_signals = date_signal
                else:
                    trade_out_signals = date_signal

            action = trigger.actions[0]
            if isinstance(action, a.EnterPositionQuantityScaledAction):
                underlier_list = action.priceables
                roll_frequency = action.trade_duration
                trade_quantity = action.trade_quantity
                trade_quantity_type = action.trade_quantity_type
                if trade_quantity_type is BacktestTradingQuantityType.NAV:
                    index_initial_value = trade_quantity
            elif isinstance(action, a.HedgeAction):
                if trigger.trigger_requirements.frequency == 'B':
                    frequency = 'Daily'
                else:
                    raise RuntimeError('unrecognised hedge frequency')
                hedge = DeltaHedgeParameters(frequency=frequency)

        strategy = StrategySystematic(name="Flow Vol Backtest",
                                      underliers=underlier_list,
                                      index_initial_value=index_initial_value,
                                      delta_hedge=hedge,
                                      quantity=trade_quantity,
                                      quantity_type=trade_quantity_type,
                                      trade_in_method=TradeInMethod.FixedRoll,
                                      roll_frequency=roll_frequency,
                                      trade_in_signals=trade_in_signals,
                                      trade_out_signals=trade_out_signals
                                      )

        result = strategy.backtest(start, end)
        return BacktestResult(result)
