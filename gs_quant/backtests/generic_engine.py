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
from gs_quant.backtests.action_handler import ActionHandlerBaseFactory, ActionHandler
from gs_quant.backtests.backtest_engine import BacktestBaseEngine
from gs_quant.backtests.backtest_utils import make_list, CalcType, get_final_date
from gs_quant.backtests.backtest_objects import BackTest, ScalingPortfolio, CashPayment
from gs_quant.backtests.actions import Action, AddTradeAction, HedgeAction, AddTradeActionInfo, HedgeActionInfo
from gs_quant.datetime.relative_date import RelativeDateSchedule
from gs_quant.instrument import Instrument
from gs_quant.markets.portfolio import Portfolio
from gs_quant.markets import PricingContext, HistoricalPricingContext
from gs_quant.risk import Price
from gs_quant.risk.base_measures import ParameterisedRiskMeasure
from functools import reduce
from datetime import date
from collections import defaultdict
from itertools import zip_longest
import datetime as dt
import logging


def raiser(ex):
    raise RuntimeError(ex)


logger = logging.getLogger(__name__)


# Action Implementations
class AddTradeActionImpl(ActionHandler):
    def __init__(self, action: AddTradeAction):
        super().__init__(action)

    def _raise_order(self,
                     state: Union[date, Iterable[date]],
                     trigger_info: Optional[Union[AddTradeActionInfo, Iterable[AddTradeActionInfo]]] = None):
        with PricingContext(is_batch=True, show_progress=True):
            state_list = make_list(state)
            orders = {}
            if trigger_info is None or isinstance(trigger_info, AddTradeActionInfo):
                trigger_info = [trigger_info for _ in range(len(state_list))]
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

        # record entry and unwind cashflows
        for create_date, portfolio in orders.items():
            for inst in portfolio.all_instruments:
                inst.name = f'{inst.name}_{create_date}'
                backtest.cash_payments[create_date].append(CashPayment(inst, effective_date=create_date, direction=-1))
                final_date = get_final_date(inst, create_date, self.action.trade_duration)
                backtest.cash_payments[final_date].append(CashPayment(inst, effective_date=final_date))

        for s in backtest.states:
            pos = []
            for create_date, portfolio in orders.items():
                pos += [inst for inst in portfolio.instruments
                        if get_final_date(inst, create_date, self.action.trade_duration) > s >= create_date]
            if len(pos):
                backtest.portfolio_dict[s].append(pos)

        return backtest


class HedgeActionImpl(ActionHandler):
    def __init__(self, action: HedgeAction):
        super().__init__(action)

    def apply_action(self,
                     state: Union[date, Iterable[date]],
                     backtest: BackTest,
                     trigger_info: Optional[Union[HedgeActionInfo, Iterable[HedgeActionInfo]]] = None):
        with HistoricalPricingContext(dates=make_list(state), csa_term=self.action.csa_term, show_progress=True):
            backtest.calc_calls += 1
            backtest.calculations += len(make_list(state))
            f = Portfolio(make_list(self.action.priceable)).resolve(in_place=False)

        for create_date, portfolio in f.result().items():
            hedge = portfolio.instruments[0]
            final_date = get_final_date(hedge, create_date, self.action.trade_duration)
            active_dates = [s for s in backtest.states if create_date <= s < final_date]

            if len(active_dates):
                for t in portfolio:
                    t.name = f'{t.name}_{create_date.strftime("%Y-%m-%d")}'
                backtest.scaling_portfolios[create_date].append(
                    ScalingPortfolio(trade=hedge, dates=active_dates, risk=self.action.risk,
                                     csa_term=self.action.csa_term, scaling_parameter=self.action.scaling_parameter))

                # add cashflows on trade entry and unwind
                backtest.cash_payments[create_date].append(
                    CashPayment(trade=hedge, effective_date=create_date, direction=-1))
                if final_date <= dt.date.today():
                    backtest.cash_payments[final_date].append(
                        CashPayment(trade=hedge, effective_date=final_date, scale_date=active_dates[-1]))

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

    def run_backtest(self, strategy, start=None, end=None, frequency='1m', states=None, risks=Price,
                     show_progress=True, csa_term=None, visible_to_gs=False, initial_value=0, result_ccy='USD',
                     holiday_calendar=None):
        """
        run the backtest following the triggers and actions defined in the strategy.  If states are entered run on
        those dates otherwise build a schedule from the start, end, frequency
        using gs_quant.datetime.relative_date.RelativeDateSchedule
        :param strategy: the strategy object
        :param start: a datetime
        :param end: a datetime
        :param frequency: str, default '1m'
        :param states: a list of dates will override the start, end, freq if provided
        :param risks: risks to run
        :param show_progress: boolean default true
        :param csa_term: the csa term to use
        :param visible_to_gs: are the contents of risk requests visible to GS (defaults to False)
        :param initial_value: initial cash value of strategy defaults to 0
        :param result_ccy: ccy of all risks, pvs and cash
        :param holiday_calendar for date maths - list of dates
        :return: a backtest object containing the portfolios on each day and results which show all risks on all days

        """

        logging.info(f'Starting Backtest: Building Date Schedule - {dt.datetime.now()}')

        dates = RelativeDateSchedule(frequency,
                                     start,
                                     end).apply_rule(holiday_calendar=holiday_calendar) if states is None else states

        risks = list(set(make_list(risks) + strategy.risks))
        risks = [r(currency=result_ccy) if isinstance(r, ParameterisedRiskMeasure)
                 else raiser(f'Unparameterised risk: {r}') for r in risks]
        price_risk = Price(currency=result_ccy)

        backtest = BackTest(strategy, dates, risks)

        logging.info('Resolving Initial Portfolio')
        if len(strategy.initial_portfolio):
            init_port = Portfolio(strategy.initial_portfolio)
            with PricingContext(pricing_date=dates[0], csa_term=csa_term, show_progress=show_progress,
                                visible_to_gs=visible_to_gs):
                init_port.resolve()
            for d in dates:
                backtest.portfolio_dict[d].append(init_port.instruments)

        logging.info('Building Simple and Semi-deterministic triggers and actions')
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

        logging.info('Pricing Simple and Semi-deterministic triggers and actions')
        with PricingContext(is_batch=True, show_progress=show_progress, csa_term=csa_term, visible_to_gs=visible_to_gs):
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

        logging.info('Scaling Semi-deterministic Triggers and Actions and Calculating Path Dependent Triggers '
                     'and Actions')
        for d in dates:
            # semi path dependent scaling
            if d in backtest.scaling_portfolios:
                for p in backtest.scaling_portfolios[d]:
                    current_risk = backtest.results[d][p.risk].aggregate(allow_mismatch_risk_keys=True)
                    hedge_risk = p.results[d][p.risk].aggregate()
                    scaling_factor = current_risk / hedge_risk
                    new_notional = getattr(p.trade, p.scaling_parameter) * -scaling_factor
                    scaled_trade = p.trade.as_dict()
                    scaled_trade[p.scaling_parameter] = new_notional
                    scaled_trade = Instrument.from_dict(scaled_trade)
                    scaled_trade.name = p.trade.name
                    for day in p.dates:
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

        logging.info('Calculate Cash')
        # run any additional calcs to handle cash scaling (e.g. unwinds)
        cash_calcs = defaultdict(list)
        with PricingContext(is_batch=True, show_progress=show_progress, csa_term=csa_term, visible_to_gs=visible_to_gs):
            backtest.calc_calls += 1
            for _, cash_payments in backtest.cash_payments.items():
                for cp in cash_payments:
                    # only calc if additional point is required
                    if cp.effective_date and cp.effective_date <= end:
                        if cp.effective_date not in backtest.results or \
                                cp.trade not in backtest.results[cp.effective_date]:
                            with PricingContext(cp.effective_date):
                                backtest.calculations += len(risks)
                                cash_calcs[cp.effective_date].append(Portfolio([cp.trade]).calc(price_risk))

        cash_results = {}
        for day, risk_results in cash_calcs.items():
            cash_results[day] = risk_results[0]
            if len(risk_results) > 1:
                for i in range(1, len(risk_results)):
                    cash_results[day] += risk_results[i]

        # handle cash
        current_value = initial_value
        for d in sorted(set(dates + list(backtest.cash_payments.keys()))):
            backtest.cash_dict[d] = current_value
            if d in backtest.cash_payments and d <= end:
                for cp in backtest.cash_payments[d]:
                    value = cash_results.get(cp.effective_date, {}).get(price_risk, {}).get(cp.trade.name, {})
                    try:
                        value = backtest.results[cp.effective_date][price_risk][cp.trade.name] if value == {} else value
                    except ValueError:
                        raise RuntimeError(f'failed to get cash value for {cp.trade.name} on '
                                           f'{cp.effective_date} received value of {value}')
                    if not isinstance(value, float):
                        raise RuntimeError(f'failed to get cash value for {cp.trade.name} on '
                                           f'{cp.effective_date} received value of {value}')
                    if cp.scale_date:
                        scale_notional = backtest.portfolio_dict[cp.scale_date][cp.trade.name].notional_amount
                        scale_date_adj = scale_notional / cp.trade.notional_amount
                        cp.cash_paid = value * scale_date_adj * cp.direction
                        backtest.cash_dict[d] += cp.cash_paid
                    else:
                        cp.cash_paid = value * cp.direction
                        backtest.cash_dict[d] += cp.cash_paid
                current_value = backtest.cash_dict[d]

        logging.info(f'Finished Backtest:- {dt.datetime.now()}')
        return backtest
