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
from gs_quant.backtests import FlowVolBacktestMeasure
from gs_quant.backtests import triggers as t
from gs_quant.backtests import actions as a
from gs_quant.backtests.strategy_systematic import StrategySystematic, DeltaHedgeParameters, TradeInMethod
from gs_quant.instrument import EqOption, EqVarianceSwap
from gs_quant.markets.portfolio import Portfolio
from gs_quant.risk import EqDelta
from gs_quant.target.backtests import BacktestSignalSeriesItem, BacktestTradingQuantityType, EquityMarketModel
import pandas as pd
import re
import copy
from functools import reduce
import warnings

from gs_quant.target.common import OptionType, BuySell


def is_synthetic_forward(priceable):
    is_portfolio = isinstance(priceable, Portfolio)
    is_syn_fwd = is_portfolio
    if is_portfolio:
        is_size_two = len(priceable) == 2
        is_syn_fwd = is_size_two
        if is_size_two:
            has_two_eq_options = isinstance(priceable[0], EqOption) and isinstance(priceable[1], EqOption)
            is_syn_fwd &= has_two_eq_options
            if has_two_eq_options:
                is_syn_fwd &= (priceable[0].underlier == priceable[1].underlier) and \
                              (priceable[0].expiration_date == priceable[1].expiration_date) and \
                              (priceable[0].strike_price == priceable[1].strike_price)
                is_syn_fwd &= (OptionType.Call, BuySell.Buy) and (OptionType.Put, BuySell.Sell) in {
                              (priceable[0].option_type, priceable[0].buy_sell),
                              (priceable[1].option_type, priceable[1].buy_sell)}

    return is_syn_fwd


class BacktestResult:
    def __init__(self, results):
        self._results = results

    def get_measure_series(self, measure: FlowVolBacktestMeasure):
        data = next(iter(r.timeseries for r in self._results.risks if r.name == measure.value), ())
        df = pd.DataFrame.from_records(data)
        if len(df) == 0:
            return df

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
                    {'date': item['date'], 'quantity': x['quantity'], 'transactionType': transaction['type'],
                     'price': x['price']},
                    **x['instrument']), transaction['trades']))
                data = data + trades

        return pd.DataFrame(data)


class EquityVolEngine(object):

    @classmethod
    def check_strategy(cls, strategy):
        check_results = []
        if len(strategy.initial_portfolio) > 0:
            check_results.append('Error: initial_portfolio must be empty or None')

        # Validate Triggers

        if len(strategy.triggers) > 3:
            check_results.append('Error: Maximum of 3 triggers')

        if not all(isinstance(x, (t.AggregateTrigger, t.PeriodicTrigger)) for x in strategy.triggers):
            check_results.append('Error: Only AggregateTrigger and PeriodTrigger supported')

        # aggregate triggers composed of a dated and portfolio trigger define a signal
        aggregate_triggers = [x for x in strategy.triggers if isinstance(x, t.AggregateTrigger)]
        for at in aggregate_triggers:
            if not len(at.triggers) == 2:
                check_results.append('Error: AggregateTrigger must be composed of 2 triggers')
            if not len([x for x in at.triggers if isinstance(x, t.DateTrigger)]) == 1:
                check_results.append('Error: AggregateTrigger must be contain 1 DateTrigger')
            portfolio_triggers = [x for x in at.triggers if isinstance(x, t.PortfolioTrigger)]
            if not len(portfolio_triggers) == 1:
                check_results.append('Error: AggregateTrigger must be contain 1 PortfolioTrigger')
            if not (portfolio_triggers[0].trigger_requirements.data_source == 'len' and
                    portfolio_triggers[0].trigger_requirements.trigger_level == 0):
                check_results.append(
                    'Error: PortfolioTrigger.trigger_requirements must have data_source = \'len\' '
                    'and trigger_level = 0')

        # Validate Actions

        all_actions = reduce(lambda acc, x: acc + x, (map(lambda x: x.actions, strategy.triggers)), [])

        if any(isinstance(x, a.ExitPositionAction) for x in all_actions):
            warnings.warn('ExitPositionAction will be deprecated soon, use ExitTradeAction.', DeprecationWarning, 2)

        if not all(isinstance(x, (a.EnterPositionQuantityScaledAction, a.HedgeAction, a.ExitPositionAction,
                                  a.ExitTradeAction)) for x in all_actions):
            check_results.append(
                'Error: actions must be one of EnterPositionQuantityScaledAction, HedgeAction, ExitPositionAction, '
                'ExitTradeAction')

        # no duplicate actions
        if not len(set(map(lambda x: type(x), all_actions))) == len(all_actions):
            check_results.append('Error: There are multiple actions of the same type')

        all_child_triggers = reduce(lambda acc, x: acc + x,
                                    map(lambda x: x.triggers if isinstance(x, t.AggregateTrigger) else [x],
                                        strategy.triggers), [])

        for trigger in all_child_triggers:
            if isinstance(trigger, t.PortfolioTrigger):
                continue

            # action one of enter position, exit position, hedge
            if len(trigger.actions) != 1:
                check_results.append('Error: All triggers must contain only 1 action')

            for action in trigger.actions:
                if isinstance(action, a.EnterPositionQuantityScaledAction):
                    if isinstance(trigger, t.PeriodicTrigger) and \
                            not trigger.trigger_requirements.frequency == action.trade_duration:
                        check_results.append(
                            'Error: EnterPositionQuantityScaledAction: PeriodicTrigger frequency must be the same '
                            'as trade_duration')
                    if not all((isinstance(p, EqOption) | isinstance(p, EqVarianceSwap))
                               for p in action.priceables):
                        check_results.append(
                            'Error: EnterPositionQuantityScaledAction: Only EqOption or EqVarianceSwap supported')
                    if action.trade_quantity is None or action.trade_quantity_type is None:
                        check_results.append(
                            'Error: EnterPositionQuantityScaledAction trade_quantity or trade_quantity_type is None')
                    expiry_date_modes = map(lambda x: ExpirationDateParser(x.expirationDate).get_mode(),
                                            action.priceables)
                    expiry_date_modes = list(set(expiry_date_modes))
                    if len(expiry_date_modes) > 1:
                        check_results.append(
                            'Error: EnterPositionQuantityScaledAction all priceable expiration_date modifiers must '
                            'be the same. Found [' + ', '.join(expiry_date_modes) + ']')
                    if expiry_date_modes[0] not in ['otc', 'listed']:
                        check_results.append(
                            'Error: EnterPositionQuantityScaledAction invalid expiration_date '
                            'modifier ' + expiry_date_modes[0])
                elif isinstance(action, a.HedgeAction):
                    if not is_synthetic_forward(action.priceable):
                        check_results.append(
                            'Error: HedgeAction: Hedge instrument must be a synthetic forward - a portfolio of two '
                            'equity options (long call and short put) with the same underlier, strike price and '
                            'expiration date')
                    if not trigger.trigger_requirements.frequency == action.trade_duration:
                        check_results.append(
                            'Error: HedgeAction: PeriodicTrigger frequency must be the same as trade_duration')
                    if not action.risk == EqDelta:
                        check_results.append('Error: HedgeAction: risk type must be EqDelta')
                    if not trigger.trigger_requirements.frequency == '1b':
                        check_results.append('Error: HedgeAction: frequency must be \'1b\'')
                elif isinstance(action, (a.ExitPositionAction, a.ExitTradeAction)):
                    continue
                else:
                    check_results.append('Error: Unsupported action type \'{}\''.format(type(action)))

        return check_results

    @classmethod
    def supports_strategy(cls, strategy):
        check_result = cls.check_strategy(strategy)
        if len(check_result):
            return False

        return True

    @classmethod
    def run_backtest(cls, strategy, start, end, market_model=EquityMarketModel.SFK):
        check_result = cls.check_strategy(strategy)
        if len(check_result):
            raise RuntimeError(check_result)

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
                underlier_list = cls.__get_underlier_list(action.priceables)
                roll_frequency = action.trade_duration
                trade_quantity = action.trade_quantity
                trade_quantity_type = action.trade_quantity_type
                if trade_quantity_type is BacktestTradingQuantityType.NAV:
                    index_initial_value = trade_quantity
                expiry_date_mode = ExpirationDateParser(action.priceables[0].expiration_date).get_mode()
            elif isinstance(action, a.HedgeAction):
                if trigger.trigger_requirements.frequency == '1b':
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
                                      trade_out_signals=trade_out_signals,
                                      market_model=market_model,
                                      expiry_date_mode=expiry_date_mode
                                      )

        result = strategy.backtest(start, end)
        return BacktestResult(result)

    @classmethod
    def __get_underlier_list(cls, pricables):
        pricables_copy = copy.deepcopy(pricables)
        for pricable in pricables_copy:
            edp = ExpirationDateParser(pricable.expiration_date)
            pricable.expiration_date = edp.get_date()
        return pricables_copy


class ExpirationDateParser(object):

    # match expiration dates expressed as 3m@listed
    expiry_regex = '(.*)@(.*)'

    def __init__(self, expiry: str):
        self.expiry = expiry

    def get_date(self):
        parts = re.search(self.expiry_regex, self.expiry)
        if parts:
            return parts.group(1)
        else:
            return self.expiry

    def get_mode(self):
        parts = re.search(self.expiry_regex, self.expiry)
        if parts:
            return parts.group(2)
        else:
            return 'otc'
