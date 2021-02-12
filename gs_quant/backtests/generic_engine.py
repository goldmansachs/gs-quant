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

from typing import Union, Iterable
import pandas as pd
from gs_quant.backtests.action_handler import ActionHandlerBaseFactory, ActionHandler
from gs_quant.backtests.backtest_engine import BacktestBaseEngine
from gs_quant.backtests.backtest_utils import make_list, CalcType, get_final_date
from gs_quant.backtests.backtest_objects import BackTest, ScalingPortfolio
from gs_quant.backtests.actions import Action, AddTradeAction, HedgeAction
from gs_quant.instrument import Instrument
from gs_quant.markets.portfolio import Portfolio
from gs_quant.markets import PricingContext, HistoricalPricingContext
from gs_quant.risk import Price
from functools import reduce
from datetime import date


# Action Implementations

class AddTradeActionImpl(ActionHandler):
    def __init__(self, action: AddTradeAction):
        super().__init__(action)

    def _raise_order(self, state: Union[date, Iterable[date]]):
        with PricingContext(is_batch=True):
            orders = {}
            for s in state:
                active_portfolio = self.action.dated_priceables.get(s) or self.action.priceables
                with PricingContext(pricing_date=s):
                    orders[s] = Portfolio(active_portfolio).resolve(in_place=False)
        return orders

    def apply_action(self, state: Union[date, Iterable[date]], backtest: BackTest):

        orders = self._raise_order(state)

        for s in backtest.states:
            pos = []
            for create_date, portfolio in orders.items():
                pos += [inst for inst in portfolio.result().instruments
                        if get_final_date(inst, create_date, self.action.trade_duration) >= s >= create_date]
            if len(pos) > 0:
                backtest.portfolio_dict[s].append(pos)

        return backtest


class HedgeActionImpl(ActionHandler):
    def __init__(self, action: HedgeAction):
        super().__init__(action)

    def apply_action(self, state: Union[date, Iterable[date]], backtest: BackTest):
        with HistoricalPricingContext(dates=make_list(state)):
            backtest.calc_calls += 1
            backtest.calculations += len(make_list(state))
            f = Portfolio(make_list(self.action.priceable)).resolve(in_place=False)

        for create_date, portfolio in f.result().items():
            active_dates = [s for s in backtest.states
                            if get_final_date(portfolio.instruments[0], create_date,
                                              self.action.trade_duration) >= s >= create_date]
            if len(active_dates):
                backtest.scaling_portfolios[create_date].append(
                    ScalingPortfolio(trade=portfolio.instruments[0], dates=active_dates, risk=self.action.risk))

        return backtest


class GenericEngineActionFactory(ActionHandlerBaseFactory):
    def get_action_handler(self, action: Action) -> Action:
        if isinstance(action, AddTradeAction):
            return AddTradeActionImpl(action)
        elif isinstance(action, HedgeAction):
            return HedgeActionImpl(action)

        raise RuntimeError(f'Action {type(action)} not supported by engine')


class GenericEngine(BacktestBaseEngine):

    @classmethod
    def get_action_handler(self, action: Action) -> Action:
        handler_factory = GenericEngineActionFactory()
        return handler_factory.get_action_handler(action)

    @classmethod
    def supports_strategy(cls, strategy):
        all_actions = reduce(lambda x, y: x + y, (map(lambda x: x.actions, strategy.triggers)))
        try:
            for x in all_actions:
                cls.get_action_handler(x)
        except RuntimeError:
            return False
        return True

    @classmethod
    def run_backtest(cls, strategy, start=None, end=None, frequency='BM', window=None, states=None, risks=Price,
                     show_progress=True):
        dates = pd.date_range(start=start, end=end, freq=frequency).date.tolist()
        risks = make_list(risks) + strategy.risks

        backtest = BackTest(strategy, dates, risks)

        if strategy.initial_portfolio is not None:
            for d in dates:
                backtest.portfolio_dict[d].append(strategy.initial_portfolio)

        for trigger in strategy.triggers:
            if trigger.calc_type != CalcType.path_dependent:
                triggered_dates = [date for date in dates if trigger.has_triggered(date, backtest)]
                for action in trigger.actions:
                    if action.calc_type != CalcType.path_dependent:
                        cls.get_action_handler(action).apply_action(triggered_dates, backtest)

        with PricingContext(is_batch=True, show_progress=show_progress):
            for day, portfolio in backtest.portfolio_dict.items():
                with PricingContext(day):
                    backtest.calc_calls += 1
                    backtest.calculations += len(portfolio) * len(risks)
                    backtest.add_results(day, portfolio.calc(tuple(risks)))

            # semi path dependent initial calc
            for _, scaling_list in backtest.scaling_portfolios.items():
                for p in scaling_list:
                    with HistoricalPricingContext(dates=p.dates):
                        backtest.calc_calls += 1
                        backtest.calculations += len(p.dates) * len(risks)
                        p.results = Portfolio([p.trade]).calc(tuple(risks))

        for d in dates:
            # semi path dependent scaling
            if d in backtest.scaling_portfolios:
                for p in backtest.scaling_portfolios[d]:
                    scale_date = p.dates[0]
                    scaling_factor = backtest.results[scale_date][p.risk][0] / p.results[scale_date][p.risk][0]
                    scaled_trade = p.trade.as_dict()
                    scaled_trade['notional_amount'] *= -scaling_factor
                    scaled_trade = Instrument.from_dict(scaled_trade)
                    for day in p.dates:
                        backtest.add_results(day, p.results[day] * -scaling_factor)
                        backtest.portfolio_dict[day] += Portfolio(scaled_trade)

            # path dependent
            for trigger in strategy.triggers:
                if trigger.calc_type == CalcType.path_dependent:
                    if trigger.has_triggered(d, backtest):
                        for action in trigger.actions:
                            cls.get_action_handler(action).apply_action(d, backtest)
                else:
                    for action in trigger.actions:
                        if action.calc_type == CalcType.path_dependent:
                            if trigger.has_triggered(d, backtest):
                                cls.get_action_handler(action).apply_action(d, backtest)
        return backtest
