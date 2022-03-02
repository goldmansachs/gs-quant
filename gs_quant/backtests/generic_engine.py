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
from gs_quant.backtests.actions import Action, AddTradeAction, HedgeAction, AddTradeActionInfo, HedgeActionInfo, \
    ExitTradeAction, ExitTradeActionInfo
from gs_quant.datetime.relative_date import RelativeDateSchedule
from gs_quant.instrument import Instrument
from gs_quant.markets.portfolio import Portfolio
from gs_quant.markets import PricingContext, HistoricalPricingContext
from gs_quant.risk import Price
from gs_quant.common import ParameterisedRiskMeasure
from functools import reduce
from datetime import date
from collections import defaultdict
from itertools import zip_longest
import copy
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
        final_orders = {}
        for d, p in orders.items():
            new_port = []
            for t in p[0].result():
                t.name = f'{t.name}_{d}'
                new_port.append(t)
            new_port = Portfolio(new_port)
            final_orders[d] = new_port.scale(None if p[1] is None else p[1].scaling, in_place=False)

        return final_orders

    def apply_action(self,
                     state: Union[date, Iterable[date]],
                     backtest: BackTest,
                     trigger_info: Optional[Union[AddTradeActionInfo, Iterable[AddTradeActionInfo]]] = None):

        orders = self._raise_order(state, trigger_info)

        # record entry and unwind cashflows
        for create_date, portfolio in orders.items():
            for inst in portfolio.all_instruments:
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
        with HistoricalPricingContext(is_batch=True, dates=make_list(state), csa_term=self.action.csa_term,
                                      show_progress=True):
            backtest.calc_calls += 1
            backtest.calculations += len(make_list(state))
            f = Portfolio(self.action.priceable).resolve(in_place=False)

        for create_date, portfolio in f.result().items():
            hedge = portfolio.priceables[0]
            hedge.name = f'{hedge.name}_{create_date.strftime("%Y-%m-%d")}'
            if isinstance(hedge, Portfolio):
                for instrument in hedge.all_instruments:
                    instrument.name = f'{hedge.name}_{instrument.name}'
            final_date = get_final_date(hedge, create_date, self.action.trade_duration)
            active_dates = [s for s in backtest.states if create_date <= s < final_date]

            if len(active_dates):
                backtest.scaling_portfolios[create_date].append(
                    ScalingPortfolio(trade=hedge, dates=active_dates, risk=self.action.risk,
                                     csa_term=self.action.csa_term, scaling_parameter=self.action.scaling_parameter))

                # add cashflows on trade entry and unwind
                backtest.cash_payments[create_date].append(
                    CashPayment(trade=hedge, effective_date=create_date, direction=-1))
                if final_date <= dt.date.today():
                    backtest.cash_payments[final_date].append(
                        CashPayment(trade=hedge, effective_date=final_date, scale_date=create_date))

        return backtest


class ExitTradeActionImpl(ActionHandler):
    def __init__(self, action: ExitTradeAction):
        super().__init__(action)

    def apply_action(self,
                     state: Union[date, Iterable[date]],
                     backtest: BackTest,
                     trigger_info: Optional[Union[ExitTradeActionInfo, Iterable[ExitTradeActionInfo]]] = None):

        for s in make_list(state):

            trades_to_remove = []

            fut_dates = list(filter(lambda d: d >= s and type(d) is dt.date, backtest.states))
            for port_date in fut_dates:
                pos_fut = list(backtest.portfolio_dict[port_date].all_instruments)

                # We expect tradable names to be defined as <ActionName>_<TradeName>_<TradeDate>
                if self.action.priceable_names:
                    # List of trade names provided -> TradeDate <= exit trigger date and TradeName is present in list
                    indexes_to_remove = [i for i, x in enumerate(pos_fut) if
                                         dt.datetime.strptime(x.name.split('_')[-1], '%Y-%m-%d').date() <= s and
                                         x.name.split('_')[-2] in self.action.priceable_names]
                else:
                    # List of trade names not provided -> TradeDate <= exit trigger date
                    indexes_to_remove = [i for i, x in enumerate(pos_fut) if
                                         dt.datetime.strptime(x.name.split('_')[-1], '%Y-%m-%d').date() <= s]

                for index in sorted(indexes_to_remove, reverse=True):
                    # Get list of trades' names that have been removed to check for their future cash flow date
                    if pos_fut[index].name not in trades_to_remove:
                        trades_to_remove.append(pos_fut[index].name)
                    del pos_fut[index]
                backtest.portfolio_dict[port_date] = Portfolio(tuple(pos_fut))

            for cp_date, cp_list in list(backtest.cash_payments.items()):
                if cp_date > s:
                    indexes_to_remove = [i for i, cp in enumerate(cp_list) if cp.trade.name in trades_to_remove]
                    for index in sorted(indexes_to_remove, reverse=True):
                        cp = cp_list[index]
                        prev_pos = [i for i, x in enumerate(backtest.cash_payments[s]) if cp.trade.name == x.trade.name]
                        # If trade already exists in exit trigger date cash payments, net out the position
                        if prev_pos:
                            backtest.cash_payments[s][prev_pos[0]].direction += cp.direction
                        else:
                            cp.effective_date = s
                            backtest.cash_payments[s].append(cp)
                        del backtest.cash_payments[cp_date][index]

                    if not backtest.cash_payments[cp_date]:
                        del backtest.cash_payments[cp_date]

        return backtest


class GenericEngineActionFactory(ActionHandlerBaseFactory):
    def __init__(self, action_impl_map={}):
        self.action_impl_map = {
            AddTradeAction: AddTradeActionImpl,
            HedgeAction: HedgeActionImpl,
            ExitTradeAction: ExitTradeActionImpl
        }
        self.action_impl_map.update(action_impl_map)

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
                     show_progress=True, csa_term=None, visible_to_gs=False, initial_value=0, result_ccy=None,
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

        strategy_pricing_dates = RelativeDateSchedule(frequency,
                                                      start,
                                                      end).apply_rule(holiday_calendar=holiday_calendar) \
            if states is None else states

        strategy_start_date = strategy_pricing_dates[0]
        strategy_end_date = strategy_pricing_dates[-1]

        risks = list(set(make_list(risks) + strategy.risks))
        if result_ccy is not None:
            risks = [(r(currency=result_ccy) if isinstance(r, ParameterisedRiskMeasure)
                      else raiser(f'Unparameterised risk: {r}')) for r in risks]
        price_risk = Price(currency=result_ccy) if result_ccy is not None else Price

        backtest = BackTest(strategy, strategy_pricing_dates, risks)

        logging.info('Resolving initial portfolio')
        if len(strategy.initial_portfolio):
            for index in range(len(strategy.initial_portfolio)):
                old_name = strategy.initial_portfolio[index].name
                strategy.initial_portfolio[index].name = f'{old_name}_{strategy_start_date.strftime("%Y-%m-%d")}'
                entry_payment = CashPayment(strategy.initial_portfolio[index],
                                            effective_date=strategy_start_date, direction=-1)
                backtest.cash_payments[strategy_start_date].append(entry_payment)
                final_date = get_final_date(strategy.initial_portfolio[index], strategy_start_date, None)
                exit_payment = CashPayment(strategy.initial_portfolio[index],
                                           effective_date=final_date)
                backtest.cash_payments[final_date].append(exit_payment)
            init_port = Portfolio(strategy.initial_portfolio)
            with PricingContext(pricing_date=strategy_start_date, csa_term=csa_term, show_progress=show_progress,
                                visible_to_gs=visible_to_gs):
                init_port.resolve()
            for d in strategy_pricing_dates:
                backtest.portfolio_dict[d].append(init_port.instruments)

        logging.info('Building simple and semi-deterministic triggers and actions')
        for trigger in strategy.triggers:
            if trigger.calc_type != CalcType.path_dependent:
                triggered_dates = []
                trigger_infos = defaultdict(list)
                for d in strategy_pricing_dates:
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

        logging.info(f'Filtering strategy calculations to run from {strategy_start_date} to {strategy_end_date}')
        backtest.portfolio_dict = defaultdict(Portfolio, {k: backtest.portfolio_dict[k]
                                                          for k in backtest.portfolio_dict
                                                          if strategy_start_date <= k <= strategy_end_date})
        backtest.scaling_portfolios = defaultdict(list, {k: backtest.scaling_portfolios[k]
                                                         for k in backtest.scaling_portfolios
                                                         if strategy_start_date <= k <= strategy_end_date})

        logging.info('Pricing simple and semi-deterministic triggers and actions')
        with PricingContext(is_batch=True, show_progress=show_progress, csa_term=csa_term, visible_to_gs=visible_to_gs):
            backtest.calc_calls += 1
            for day, portfolio in backtest.portfolio_dict.items():
                if isinstance(day, dt.date):
                    with PricingContext(day):
                        backtest.calculations += len(portfolio) * len(risks)
                        backtest.add_results(day, portfolio.calc(tuple(risks)))

            # semi path dependent initial calc
            for _, scaling_list in backtest.scaling_portfolios.items():
                for p in scaling_list:
                    with HistoricalPricingContext(dates=p.dates):
                        backtest.calculations += len(risks) * len(p.dates)
                        port = p.trade if isinstance(p.trade, Portfolio) else Portfolio([p.trade])
                        p.results = port.calc(tuple(risks))

        logging.info('Scaling semi-deterministic triggers and actions and calculating path dependent triggers '
                     'and actions')
        for d in strategy_pricing_dates:
            logging.info(f'{d}: Processing triggers and actions')
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
            # test to see if new trades have been added and calc
            port = []
            for t in backtest.portfolio_dict[d]:
                if t.name not in list(backtest.results[d].to_frame().index):
                    port.append(t)

            with PricingContext(is_batch=True, csa_term=csa_term, show_progress=show_progress,
                                visible_to_gs=visible_to_gs):
                if len(port):
                    with PricingContext(pricing_date=d):
                        results = Portfolio(port).calc(tuple(risks))

                for sp in backtest.scaling_portfolios[d]:
                    if sp.results is None:
                        with HistoricalPricingContext(dates=sp.dates):
                            backtest.calculations += len(risks) * len(sp.dates)
                            port_sp = sp.trade if isinstance(sp.trade, Portfolio) else Portfolio([sp.trade])
                            sp.results = port_sp.calc(tuple(risks))

            # results should be added outside of pricing context and not in the same call as valuating them
            if len(port):
                backtest.add_results(d, results)

            # semi path dependent scaling
            if d in backtest.scaling_portfolios:
                for p in backtest.scaling_portfolios[d]:
                    current_risk = backtest.results[d][p.risk].aggregate(allow_mismatch_risk_keys=True)
                    hedge_risk = p.results[d][p.risk].aggregate()
                    if current_risk.unit != hedge_risk.unit:
                        raise RuntimeError('cannot hedge in a different currency')
                    scaling_factor = current_risk / hedge_risk
                    if isinstance(p.trade, Portfolio):
                        # Scale the portfolio by risk target
                        scaled_portfolio_position = copy.deepcopy(p.trade)
                        scaled_portfolio_position.name = f'Scaled_{scaled_portfolio_position.name}'
                        for instrument in scaled_portfolio_position.all_instruments:
                            instrument.name = f'Scaled_{instrument.name}'

                        # trade hedge in opposite direction
                        scale_direction = -1
                        scaled_portfolio_position.scale(scaling_factor * scale_direction)

                        for day in p.dates:
                            # add scaled hedge position to portfolio for day. NOTE this adds leaves, not the portfolio
                            backtest.portfolio_dict[day] += copy.deepcopy(scaled_portfolio_position)

                        # now apply scaled portfolio to cash payments
                        for d, payments in backtest.cash_payments.items():
                            for payment in payments:
                                if payment.trade == p.trade:
                                    payment.trade = copy.deepcopy(scaled_portfolio_position)
                                    payment.scale_date = None

                    else:
                        new_notional = getattr(p.trade, p.scaling_parameter) * -scaling_factor
                        scaled_trade = p.trade.as_dict()
                        scaled_trade[p.scaling_parameter] = new_notional
                        scaled_trade = Instrument.from_dict(scaled_trade)
                        scaled_trade.name = p.trade.name
                        for day in p.dates:
                            backtest.add_results(day, p.results[day] * -scaling_factor)
                            backtest.portfolio_dict[day] += Portfolio(scaled_trade)

        logging.info('Calculating and scaling newly added portfolio positions')
        # test to see if new trades have been added and calc
        with PricingContext(is_batch=True, show_progress=show_progress, csa_term=csa_term, visible_to_gs=visible_to_gs):
            backtest.calc_calls += 1
            leaves_by_date = {}
            for day, portfolio in backtest.portfolio_dict.items():
                results_for_date = backtest.results[day]
                if len(results_for_date) == 0:
                    continue

                trades_for_date = list(results_for_date.to_frame().index)
                leaves = []
                for leaf in portfolio:
                    if leaf.name not in trades_for_date:
                        logging.info(f'{day}: new portfolio position {leaf} scheduled for calculation')
                        leaves.append(leaf)

                if len(leaves):
                    with PricingContext(pricing_date=day):
                        leaves_by_date[day] = Portfolio(leaves).calc(tuple(risks))
                        backtest.calculations += len(leaves) * len(risks)

        logging.info('Processing results for newly added portfolio positions')
        for day, leaves in leaves_by_date.items():
            backtest.add_results(day, leaves)

        logging.info('Calculating prices for cash payments')
        # run any additional calcs to handle cash scaling (e.g. unwinds)
        cash_results = {}
        with PricingContext(is_batch=True, show_progress=show_progress, csa_term=csa_term, visible_to_gs=visible_to_gs):
            backtest.calc_calls += 1
            cash_trades_by_date = defaultdict(list)
            for _, cash_payments in backtest.cash_payments.items():
                for cp in cash_payments:
                    # only calc if additional point is required
                    trades = cp.trade.all_instruments if isinstance(cp.trade, Portfolio) else [cp.trade]
                    for trade in trades:
                        if cp.effective_date and cp.effective_date <= end:
                            if cp.effective_date not in backtest.results or \
                                    trade not in backtest.results[cp.effective_date]:
                                cash_trades_by_date[cp.effective_date].append(trade)
                            else:
                                cp.scale_date = None

            for cash_date, trades in cash_trades_by_date.items():
                with PricingContext(cash_date):
                    backtest.calculations += len(risks)
                    cash_results[cash_date] = Portfolio(trades).calc(price_risk)

        # handle cash
        current_value = None
        for d in sorted(set(strategy_pricing_dates + list(backtest.cash_payments.keys()))):
            if d <= end:
                if current_value is not None:
                    backtest.cash_dict[d] = current_value
                if d in backtest.cash_payments:
                    for cp in backtest.cash_payments[d]:
                        trades = cp.trade.all_instruments if isinstance(cp.trade, Portfolio) else [cp.trade]
                        for trade in trades:
                            value = cash_results.get(cp.effective_date, {}).get(price_risk, {}).get(trade.name, {})
                            try:
                                value = backtest.results[cp.effective_date][price_risk][trade.name] \
                                    if value == {} else value
                            except (KeyError, ValueError):
                                raise RuntimeError(f'failed to get cash value for {trade.name} on '
                                                   f'{cp.effective_date} received value of {value}')
                            if not isinstance(value, float):
                                raise RuntimeError(f'failed to get cash value for {trade.name} on '
                                                   f'{cp.effective_date} received value of {value}')
                            ccy = next(iter(value.unit))
                            if d not in backtest.cash_dict:
                                backtest.cash_dict[d] = {ccy: initial_value}
                            if ccy not in backtest.cash_dict[d]:
                                backtest.cash_dict[d][ccy] = 0
                            if cp.scale_date:
                                scale_notional = backtest.portfolio_dict[cp.scale_date][cp.trade.name].notional_amount
                                scale_date_adj = scale_notional / cp.trade.notional_amount
                                cp.cash_paid = value * scale_date_adj * cp.direction
                                backtest.cash_dict[d][ccy] += cp.cash_paid
                            else:
                                cp.cash_paid = (0 if cp.cash_paid is None else cp.cash_paid) + value * cp.direction
                                backtest.cash_dict[d][ccy] += cp.cash_paid

                current_value = copy.deepcopy(backtest.cash_dict[d])

        logging.info(f'Finished Backtest:- {dt.datetime.now()}')
        return backtest
