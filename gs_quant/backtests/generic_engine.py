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
import pandas as pd
from gs_quant.backtests.action_handler import ActionHandlerBaseFactory, ActionHandler
from gs_quant.backtests.backtest_engine import BacktestBaseEngine
from gs_quant.backtests.backtest_utils import make_list, CalcType, get_final_date
from gs_quant.backtests.backtest_objects import BackTest, ScalingPortfolio
from gs_quant.backtests.actions import Action, AddTradeAction, HedgeAction, AddTradeActionInfo, HedgeActionInfo
from gs_quant.instrument import Instrument
from gs_quant.markets.portfolio import Portfolio
from gs_quant.markets import PricingContext, HistoricalPricingContext
from gs_quant.risk import Price
from functools import reduce
from datetime import date
from collections import defaultdict
from itertools import zip_longest
import datetime as dt


# Action Implementations

class AddTradeActionImpl(ActionHandler):
    def __init__(self, action: AddTradeAction):
        super().__init__(action)

    def _raise_order(self,
                     state: Union[date, Iterable[date]],
                     trigger_info: Optional[Union[AddTradeActionInfo, Iterable[AddTradeActionInfo]]] = None):
        with PricingContext(is_batch=True):
            state_list = make_list(state)
            orders = {}
            if trigger_info is None or isinstance(trigger_info, AddTradeActionInfo):
                trigger_info = [trigger_info for i in range(len(state_list))]
            for s, ti in zip_longest(state_list, trigger_info):
                active_portfolio = self.action.dated_priceables.get(s) or self.action.priceables
                with PricingContext(pricing_date=s):
                    orders[s] = (Portfolio(active_portfolio).resolve(in_place=False), ti)
        orders = {k: v[0].result().scale(None if v[1] is None else v[1].scaling, in_place=False) for k, v in
                  orders.items()}
        return orders

    def apply_action(self,
                     state: Union[date, Iterable[date]],
                     backtest: BackTest,
                     trigger_info: Optional[Union[AddTradeActionInfo, Iterable[AddTradeActionInfo]]] = None):

        orders = self._raise_order(state, trigger_info)

        for s in backtest.states:
            pos = []
            for create_date, portfolio in orders.items():
                pos += [inst for inst in portfolio.instruments
                        if get_final_date(inst, create_date, self.action.trade_duration) >= s >= create_date]
            if len(pos) > 0:
                backtest.portfolio_dict[s].append(pos)

        return backtest


class HedgeActionImpl(ActionHandler):
    def __init__(self, action: HedgeAction):
        super().__init__(action)

    def apply_action(self,
                     state: Union[date, Iterable[date]],
                     backtest: BackTest,
                     trigger_info: Optional[Union[HedgeActionInfo, Iterable[HedgeActionInfo]]] = None):
        with HistoricalPricingContext(dates=make_list(state), csa_term=self.action.csa_term):
            backtest.calc_calls += 1
            backtest.calculations += len(make_list(state))
            f = Portfolio(make_list(self.action.priceable)).resolve(in_place=False)

        for create_date, portfolio in f.result().items():
            final_date = get_final_date(portfolio.instruments[0], create_date, self.action.trade_duration)
            if self.action.risks_on_final_day:
                next_state = list(filter(lambda x: x > create_date, backtest.states))
                final_date = min(final_date, next_state[0]) if len(next_state) else final_date
            active_dates = [s for s in backtest.states if create_date <= s < final_date]

            if len(active_dates):
                for t in portfolio:
                    t.name = f'{t.name}_{create_date.strftime("%Y-%m-%d")}'
                backtest.scaling_portfolios[create_date].append(
                    ScalingPortfolio(trade=portfolio.instruments[0], dates=active_dates, risk=self.action.risk,
                                     csa_term=self.action.csa_term))
                if self.action.risks_on_final_day and final_date <= dt.date.today():
                    backtest.scaling_portfolios[final_date].append(
                        ScalingPortfolio(trade=portfolio.instruments[0], dates=[final_date], risk=self.action.risk,
                                         csa_term=self.action.csa_term, unwind=True))

        return backtest


class GenericEngineActionFactory(ActionHandlerBaseFactory):
    def __init__(self, action_impl_map={}):
        self.action_impl_map = action_impl_map
        self.action_impl_map[AddTradeAction] = AddTradeActionImpl
        self.action_impl_map[HedgeAction] = HedgeActionImpl

    def get_action_handler(self, action: Action) -> Action:
        if type(action) in self.action_impl_map:
            return self.action_impl_map[type(action)](action)
        raise RuntimeError(f'Action {type(action)} not supported by engine')


class GenericEngine(BacktestBaseEngine):

    def __init__(self, action_impl_map={}):
        self.action_impl_map = action_impl_map

    def get_action_handler(self, action: Action) -> Action:
        handler_factory = GenericEngineActionFactory(self.action_impl_map)
        return handler_factory.get_action_handler(action)

    def supports_strategy(self, strategy):
        all_actions = reduce(lambda x, y: x + y, (map(lambda x: x.actions, strategy.triggers)))
        try:
            for x in all_actions:
                self.get_action_handler(x)
        except RuntimeError:
            return False
        return True

    def run_backtest(self, strategy, start=None, end=None, frequency='BM', window=None, states=None, risks=Price,
                     show_progress=True, csa_term=None):
        """
        run the backtest following the triggers and actions defined in the strategy.  If states are entered run on
        those dates otherwise build a schedule from the start, end, frequency using pd.date_range
        :param strategy: the strategy object
        :param start: a datetime
        :param end: a datetime
        :param frequency: str or DateOffset, default 'D'. Frequency strings can have multiples, e.g. '5H'.
        :param window: not used yet - intended for running a strategy over a series of potentially overlapping dates
        :param states: a list of dates will override the start, end, freq if provided
        :param risks: risks to run
        :param show_progress: boolean default true
        :param csa_term: the csa term to use
        :return: a backtest object containing the portfolios on each day and results which show all risks on all days

        """

        if states is None:
            dates = pd.date_range(start=start, end=end, freq=frequency).date.tolist()
        else:
            dates = states

        risks = make_list(risks) + strategy.risks

        backtest = BackTest(strategy, dates, risks)

        if len(strategy.initial_portfolio):
            init_port = Portfolio(strategy.initial_portfolio)
            with PricingContext(pricing_date=dates[0], csa_term=csa_term):
                init_port.resolve()
            for d in dates:
                backtest.portfolio_dict[d].append(init_port.instruments)

        for trigger in strategy.triggers:
            if trigger.calc_type != CalcType.path_dependent:
                triggered_dates = []
                trigger_infos = defaultdict(list)
                for d in dates:
                    t_info = trigger.has_triggered(d, backtest)
                    if t_info:
                        triggered_dates.append(d)
                        if t_info.info_dict:
                            for k, v in t_info.info_dict.items():
                                trigger_infos[k].append(v)

                for action in trigger.actions:
                    if action.calc_type != CalcType.path_dependent:
                        self.get_action_handler(action).apply_action(triggered_dates,
                                                                     backtest,
                                                                     trigger_infos[type(action)]
                                                                     if type(action) in trigger_infos else None)

        with PricingContext(is_batch=True, show_progress=show_progress):
            for day, portfolio in backtest.portfolio_dict.items():
                with PricingContext(day, csa_term=csa_term):
                    backtest.calc_calls += 1
                    backtest.calculations += len(portfolio) * len(risks)
                    backtest.add_results(day, portfolio.calc(tuple(risks)))

            # semi path dependent initial calc
            for _, scaling_list in backtest.scaling_portfolios.items():
                for p in scaling_list:
                    with HistoricalPricingContext(dates=p.dates, csa_term=p.csa_term or csa_term):
                        backtest.calc_calls += 1
                        backtest.calculations += len(p.dates) * len(risks)
                        p.results = Portfolio([p.trade]).calc(tuple(risks))

        for d in dates:
            # semi path dependent scaling
            if d in backtest.scaling_portfolios:
                for p in backtest.scaling_portfolios[d]:
                    current_risk = backtest.results[d][p.risk].aggregate(allow_mismatch_risk_keys=True)
                    hedge_risk = p.results[d][p.risk].aggregate()
                    scaling_factor = current_risk / hedge_risk
                    new_notional = p.trade.notional_amount * -scaling_factor
                    scaled_trade = p.trade.as_dict()
                    scaled_trade['notional_amount'] = new_notional
                    scaled_trade = Instrument.from_dict(scaled_trade)
                    for day in p.dates:
                        if p.unwind:
                            backtest.cash_dict[day] += p.results[day][Price].aggregate() * -scaling_factor
                        else:
                            backtest.add_results(day, p.results[day] * -scaling_factor)
                            backtest.portfolio_dict[day] += Portfolio(scaled_trade)

            # path dependent
            for trigger in strategy.triggers:
                if trigger.calc_type == CalcType.path_dependent:
                    if trigger.has_triggered(d, backtest):
                        for action in trigger.actions:
                            self.get_action_handler(action).apply_action(d, backtest)
                else:
                    for action in trigger.actions:
                        if action.calc_type == CalcType.path_dependent:
                            if trigger.has_triggered(d, backtest):
                                self.get_action_handler(action).apply_action(d, backtest)
        return backtest
