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

import copy
import datetime as dt
import logging
from abc import ABCMeta
from collections import defaultdict, namedtuple
from datetime import date
from functools import reduce
from itertools import zip_longest
from typing import Union, Iterable, Optional, Dict, Collection

from gs_quant.backtests.action_handler import ActionHandlerBaseFactory, ActionHandler
from gs_quant.backtests.actions import (Action, AddTradeAction, HedgeAction, AddTradeActionInfo, HedgeActionInfo,
                                        ExitTradeAction, ExitTradeActionInfo, RebalanceAction, RebalanceActionInfo,
                                        ExitAllPositionsAction, AddScaledTradeAction, ScalingActionType,
                                        AddScaledTradeActionInfo)
from gs_quant.backtests.backtest_engine import BacktestBaseEngine
from gs_quant.backtests.backtest_objects import BackTest, ScalingPortfolio, CashPayment, Hedge, PnlDefinition, \
    TransactionCostEntry
from gs_quant.backtests.backtest_utils import make_list, CalcType, get_final_date, map_ccy_name_to_ccy
from gs_quant.backtests.strategy import Strategy
from gs_quant.common import AssetClass, Currency, ParameterisedRiskMeasure, RiskMeasure
from gs_quant.context_base import nullcontext
from gs_quant.datetime.relative_date import RelativeDateSchedule
from gs_quant.instrument import Instrument
from gs_quant.markets import PricingContext, HistoricalPricingContext
from gs_quant.markets.portfolio import Portfolio
from gs_quant.risk import Price
from gs_quant.risk.results import PortfolioRiskResult
from gs_quant.target.measures import ResolvedInstrumentValues
from gs_quant.tracing import Tracer

# priority set to contexts making requests to the pricing API (min. 1 - max. 10)
DEFAULT_REQUEST_PRIORITY = 5


def raiser(ex):
    raise RuntimeError(ex)


logger = logging.getLogger(__name__)


# Action Implementations
class OrderBasedActionImpl(ActionHandler, metaclass=ABCMeta):
    def __init__(self, action: Action):
        self._order_valuations = [ResolvedInstrumentValues]
        super().__init__(action)

    def get_base_orders_for_states(self, states: Collection[date], **kwargs):
        orders = {}
        dated_priceables = getattr(self.action, 'dated_priceables', {})
        with PricingContext():
            for s in states:
                active_portfolio = dated_priceables.get(s) or self.action.priceables
                with PricingContext(pricing_date=s):
                    orders[s] = Portfolio(active_portfolio).calc(tuple(self._order_valuations))
        return orders

    def get_instrument_final_date(self, inst: Instrument, order_date: dt.date, info: namedtuple):
        return get_final_date(inst, order_date, self.action.trade_duration, self.action.holiday_calendar, info)


class AddTradeActionImpl(OrderBasedActionImpl):
    def __init__(self, action: AddTradeAction):
        super().__init__(action)

    def _raise_order(self,
                     state: Union[date, Iterable[date]],
                     trigger_info: Optional[Union[AddTradeActionInfo, Iterable[AddTradeActionInfo]]] = None):
        state_list = make_list(state)
        if trigger_info is None or isinstance(trigger_info, AddTradeActionInfo):
            trigger_info = [trigger_info for _ in range(len(state_list))]
        ti_by_state = {}
        for s, ti in zip_longest(state_list, trigger_info):
            ti_by_state[s] = ti
        orders = self.get_base_orders_for_states(state_list, trigger_infos=ti_by_state)
        final_orders = {}
        for d, p in orders.items():
            new_port = Portfolio([t.clone(name=f'{t.name}_{d}') for t in p.result()])
            ti = ti_by_state[d]
            final_orders[d] = (new_port.scale(None if ti is None else ti.scaling, in_place=False), ti)

        return final_orders

    def apply_action(self,
                     state: Union[date, Iterable[date]],
                     backtest: BackTest,
                     trigger_info: Optional[Union[AddTradeActionInfo, Iterable[AddTradeActionInfo]]] = None):

        orders = self._raise_order(state, trigger_info)

        current_tc_entries = []
        # record entry and unwind cashflows
        for create_date, (portfolio, info) in orders.items():
            for inst in portfolio.all_instruments:
                tc_enter = TransactionCostEntry(create_date, inst, self.action.transaction_cost)
                current_tc_entries.append(tc_enter)
                backtest.cash_payments[create_date].append(CashPayment(inst, effective_date=create_date, direction=-1,
                                                                       transaction_cost_entry=tc_enter))
                backtest.transaction_cost_entries[create_date].append(tc_enter)
                final_date = self.get_instrument_final_date(inst, create_date, info)
                tc_exit = TransactionCostEntry(final_date, inst, self.action.transaction_cost_exit)
                current_tc_entries.append(tc_exit)
                backtest.cash_payments[final_date].append(CashPayment(inst, effective_date=final_date,
                                                                      transaction_cost_entry=tc_exit))
                backtest.transaction_cost_entries[final_date].append(tc_exit)
                backtest_states = (s for s in backtest.states if final_date > s >= create_date)
                for s in backtest_states:
                    backtest.portfolio_dict[s].append(inst)

        with PricingContext(is_async=True):
            if any(tce.no_of_risk_calcs > 0 for tce in current_tc_entries):
                backtest.calc_calls += 1
            for tce in current_tc_entries:
                backtest.calculations += tce.no_of_risk_calcs
                tce.calculate_unit_cost()

        return backtest


class AddScaledTradeActionImpl(OrderBasedActionImpl):
    def __init__(self, action: AddScaledTradeAction):
        super().__init__(action)

    @staticmethod
    def __portfolio_scaling_for_available_cash(portfolio, available_cash, cur_day, unscaled_prices_by_day,
                                               unscaled_entry_tces_by_day) -> float:
        fixed_tcs = 0
        scaling_based_tcs = 0
        for inst in portfolio:
            insed_fixed_tc, inst_scaling_tc = unscaled_entry_tces_by_day[cur_day][inst].get_cost_by_component()
            fixed_tcs += insed_fixed_tc
            scaling_based_tcs += inst_scaling_tc
        # solve such that fixed TCs, instrument prices and scaled transaction costs (under the same scaling factor)
        # add up to available_cash
        # do not floor to zero on the first iteration - first scale factor can be negative,
        # e.g. if the aggregation operator is "min" and the fixed cost is the minimum but it exceeds the available cash,
        # it would be too early to floor to zero, must solve again in case there still is an acceptable scaling level
        first_scale_factor = (available_cash - fixed_tcs) / (unscaled_prices_by_day[cur_day].aggregate() +
                                                             scaling_based_tcs)
        if first_scale_factor == 0:
            return 0
        # set additional scaling on TCE and solve again in case aggregation (min/max) has been affected by scaling
        fixed_tcs = 0
        scaling_based_tcs = 0
        for inst in portfolio:
            unscaled_entry_tces_by_day[cur_day][inst].additional_scaling = first_scale_factor
            insed_fixed_tc, inst_scaling_tc = unscaled_entry_tces_by_day[cur_day][inst].get_cost_by_component()
            fixed_tcs += insed_fixed_tc
            scaling_based_tcs += inst_scaling_tc
        # this is 1 if aggregation is unaffected (e.g. switch from Scaled to Fixed), otherwise additional scaling needed
        second_scale_factor = max(available_cash - fixed_tcs, 0) / (unscaled_prices_by_day[cur_day].aggregate() *
                                                                    first_scale_factor + scaling_based_tcs)
        return first_scale_factor * second_scale_factor

    def _nav_scale_orders(self, orders, price_measure, trigger_infos):
        sorted_order_days = sorted(make_list(orders.keys()))
        final_days_orders = {}
        unscaled_entry_tces_by_day = defaultdict(dict)
        unscaled_unwind_tces_by_day = defaultdict(dict)
        # Populate dict of dates and instruments sold on those dates
        for create_date, portfolio in orders.items():
            info = trigger_infos[create_date]
            for inst in portfolio.all_instruments:
                tc_enter = TransactionCostEntry(create_date, inst, self.action.transaction_cost)
                unscaled_entry_tces_by_day[create_date][inst] = tc_enter
                d = self.get_instrument_final_date(inst, create_date, info)
                tc_exit = TransactionCostEntry(d, inst, self.action.transaction_cost_exit)
                unscaled_unwind_tces_by_day[d][inst] = tc_exit
                if d not in final_days_orders.keys():
                    final_days_orders[d] = []
                final_days_orders[d].append(inst)

        unscaled_prices_by_day = {}
        unscaled_unwind_prices_by_day = {}
        # Send all unscaled prices and transaction costs to calculate together
        with PricingContext(is_async=True):
            for day, portfolio in orders.items():
                with PricingContext(pricing_date=day):
                    unscaled_prices_by_day[day] = portfolio.calc(price_measure)
            for unwind_day, unwind_instruments in final_days_orders.items():
                if unwind_day <= dt.date.today():
                    with PricingContext(pricing_date=unwind_day):
                        unscaled_unwind_prices_by_day[unwind_day] = Portfolio(unwind_instruments).calc(price_measure)
            for day, inst_tce_map in unscaled_entry_tces_by_day.items():
                for inst, tce in inst_tce_map.items():
                    tce.calculate_unit_cost()
            for day, inst_tce_map in unscaled_unwind_tces_by_day.items():
                for inst, tce in inst_tce_map.items():
                    tce.calculate_unit_cost()

        # Start with scaling_level, then only use proceeds from selling instruments
        available_cash = self.action.scaling_level
        scaling_factors_by_inst = {}
        scaling_factors_by_day = {}
        # Go through each order day of the strategy in sorted order
        for idx, cur_day in enumerate(sorted_order_days):
            portfolio = orders[cur_day]
            scale_factor = self.__portfolio_scaling_for_available_cash(portfolio, available_cash, cur_day,
                                                                       unscaled_prices_by_day,
                                                                       unscaled_entry_tces_by_day)
            scaling_factors_by_day[cur_day] = scale_factor
            for inst in portfolio:
                scaling_factors_by_inst[inst] = scale_factor

            available_cash = 0

            if idx + 1 < len(sorted_order_days):
                next_day = sorted_order_days[idx + 1]
            else:
                break

            # Cash received from unwinds is the cash available for the next order
            for d, p in final_days_orders.items():
                # Only consider final days between current order date and the next in an iteration
                if cur_day < d <= next_day:
                    for inst in p:
                        available_cash += unscaled_unwind_prices_by_day[d][inst] * scaling_factors_by_inst[inst]
                        tce = unscaled_unwind_tces_by_day[d][inst]
                        # additional_scaling only scales the scaling part of the TC
                        tce.additional_scaling = scaling_factors_by_inst[inst]
                        available_cash -= unscaled_unwind_tces_by_day[d][inst].get_final_cost()
            available_cash = max(available_cash, 0)

        # portfolio.scale() applies a deepcopy so interferes with inst dict lookup; apply at the end
        for day in sorted_order_days:
            if scaling_factors_by_day[day] == 0:
                del orders[day]
            else:
                orders[day].scale(scaling_factors_by_day[day])

    def _scale_order(self, orders, daily_risk, price_measure, trigger_infos):
        if self.action.scaling_type == ScalingActionType.size:
            for _, portfolio in orders.items():
                portfolio.scale(self.action.scaling_level)
        elif self.action.scaling_type == ScalingActionType.NAV:
            self._nav_scale_orders(orders, price_measure, trigger_infos)
        elif self.action.scaling_type == ScalingActionType.risk_measure:
            for day, portfolio in orders.items():
                scaling_factor = self.action.scaling_level / daily_risk[day]
                portfolio.scale(scaling_factor)
        else:
            raise RuntimeError(f'Scaling Type {self.action.scaling_type} not supported by engine')

    def _raise_order(self,
                     state_list: Collection[date],
                     price_measure: RiskMeasure,
                     trigger_infos: Dict[dt.date, Optional[Union[AddScaledTradeActionInfo,
                                                                 Iterable[AddScaledTradeActionInfo]]]]):
        if self.action.scaling_type == ScalingActionType.risk_measure:
            self._order_valuations.append(self.action.scaling_risk)
        orders = self.get_base_orders_for_states(state_list, trigger_infos=trigger_infos)

        final_orders = {}
        for d, res in orders.items():
            new_port = []
            for inst in self.action.priceables:
                new_inst = res[inst]
                if len(self._order_valuations) > 1:
                    new_inst = new_inst[ResolvedInstrumentValues]
                new_inst.name = f'{new_inst.name}_{d}'
                new_port.append(new_inst)
            final_orders[d] = Portfolio(new_port)
        daily_risk = {d: res[self.action.scaling_risk].aggregate() for d, res in orders.items()} if \
            self.action.scaling_type == ScalingActionType.risk_measure else None

        self._scale_order(final_orders, daily_risk, price_measure, trigger_infos)

        return final_orders

    def apply_action(self,
                     state: Union[date, Iterable[date]],
                     backtest: BackTest,
                     trigger_info: Optional[Union[AddScaledTradeActionInfo,
                                                  Iterable[AddScaledTradeActionInfo]]] = None):

        state_list = make_list(state)
        if trigger_info is None or isinstance(trigger_info, AddScaledTradeActionInfo):
            trigger_info = [trigger_info for _ in range(len(state_list))]
        trigger_infos = dict(zip_longest(state_list, trigger_info))
        orders = self._raise_order(state_list, backtest.price_measure, trigger_infos)

        current_tc_entries = []
        # record entry and unwind cashflows
        for create_date, portfolio in orders.items():
            info = trigger_infos[create_date]
            for inst in portfolio.all_instruments:
                tc_enter = TransactionCostEntry(create_date, inst, self.action.transaction_cost)
                current_tc_entries.append(tc_enter)
                backtest.cash_payments[create_date].append(CashPayment(inst, effective_date=create_date, direction=-1,
                                                                       transaction_cost_entry=tc_enter))
                backtest.transaction_cost_entries[create_date].append(tc_enter)
                final_date = self.get_instrument_final_date(inst, create_date, info)
                tc_exit = TransactionCostEntry(final_date, inst, self.action.transaction_cost_exit)
                current_tc_entries.append(tc_exit)
                backtest.cash_payments[final_date].append(CashPayment(inst, effective_date=final_date,
                                                                      transaction_cost_entry=tc_exit))
                backtest.transaction_cost_entries[final_date].append(tc_exit)
                backtest_states = (s for s in backtest.states if final_date > s >= create_date)
                for s in backtest_states:
                    backtest.portfolio_dict[s].append(inst)

        with PricingContext(is_async=True):
            if any(tce.no_of_risk_calcs > 0 for tce in current_tc_entries):
                backtest.calc_calls += 1
            for tce in current_tc_entries:
                backtest.calculations += tce.no_of_risk_calcs
                tce.calculate_unit_cost()

        return backtest


class HedgeActionImpl(OrderBasedActionImpl):
    def __init__(self, action: HedgeAction):
        super().__init__(action)

    def get_base_orders_for_states(self, states: Collection[date], **kwargs):
        with HistoricalPricingContext(dates=states, csa_term=self.action.csa_term):
            f = Portfolio(self.action.priceable).resolve(in_place=False)
        return f.result()

    def apply_action(self,
                     state: Union[date, Iterable[date]],
                     backtest: BackTest,
                     trigger_info: Optional[Union[HedgeActionInfo, Iterable[HedgeActionInfo]]] = None):
        state_list = make_list(state)
        if trigger_info is None or isinstance(trigger_info, HedgeActionInfo):
            trigger_info = [trigger_info for _ in range(len(state_list))]
        trigger_infos = dict(zip_longest(state_list, trigger_info))
        backtest.calc_calls += 1
        backtest.calculations += len(state_list)
        orders = self.get_base_orders_for_states(state_list, trigger_infos=trigger_infos)

        current_tc_entries = []
        for create_date, portfolio in orders.items():
            info = trigger_infos[create_date]
            hedge_trade = portfolio.priceables[0]
            hedge_trade.name = f'{hedge_trade.name}_{create_date.strftime("%Y-%m-%d")}'
            if isinstance(hedge_trade, Portfolio):
                for instrument in hedge_trade.all_instruments:
                    instrument.name = f'{hedge_trade.name}_{instrument.name}'
            final_date = self.get_instrument_final_date(hedge_trade, create_date, info)
            active_dates = [s for s in backtest.states if create_date <= s < final_date]

            if len(active_dates):
                scaling_portfolio = ScalingPortfolio(trade=hedge_trade, dates=active_dates, risk=self.action.risk,
                                                     csa_term=self.action.csa_term,
                                                     scaling_parameter=self.action.scaling_parameter,
                                                     risk_transformation=self.action.risk_transformation)
                tc_enter = TransactionCostEntry(create_date, hedge_trade, self.action.transaction_cost)
                current_tc_entries.append(tc_enter)
                entry_payment = CashPayment(trade=hedge_trade, effective_date=create_date, direction=-1,
                                            scaling_parameter=self.action.scaling_parameter,
                                            transaction_cost_entry=tc_enter)
                backtest.transaction_cost_entries[create_date].append(tc_enter)
                tc_exit = TransactionCostEntry(final_date, hedge_trade, self.action.transaction_cost_exit)
                current_tc_entries.append(tc_exit)
                exit_payment = CashPayment(trade=hedge_trade, effective_date=final_date, scale_date=create_date,
                                           scaling_parameter=self.action.scaling_parameter,
                                           transaction_cost_entry=tc_exit) \
                    if final_date <= dt.date.today() else None
                backtest.transaction_cost_entries[final_date].append(tc_exit)
                hedge = Hedge(scaling_portfolio=scaling_portfolio,
                              entry_payment=entry_payment,
                              exit_payment=exit_payment)
                backtest.hedges[create_date].append(hedge)

        with PricingContext(is_async=True):
            if any(tce.no_of_risk_calcs > 0 for tce in current_tc_entries):
                backtest.calc_calls += 1
            for tce in current_tc_entries:
                backtest.calculations += tce.no_of_risk_calcs
                tce.calculate_unit_cost()

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
            if self.action.priceable_names is None:
                current_trade_names = [i.name for i in list(backtest.portfolio_dict[s].all_instruments)]

            fut_dates = list(filter(lambda d: d >= s and type(d) is dt.date, backtest.states))
            for port_date in fut_dates:
                res_fut = []
                res_futures = []
                pos_fut = list(backtest.portfolio_dict[port_date].all_instruments)
                if backtest.results[port_date]:  # there are results in future dates which need removing
                    res_fut = list(backtest.results[port_date].portfolio.all_instruments)
                    res_futures = list(backtest.results[port_date].futures)

                # We expect tradable names to be defined as <ActionName>_<TradeName>_<TradeDate>
                if self.action.priceable_names:
                    # List of trade names provided -> TradeDate <= exit trigger date and TradeName is present in list
                    port_indexes_to_remove = [i for i, x in enumerate(pos_fut) if
                                              dt.datetime.strptime(x.name.split('_')[-1], '%Y-%m-%d').date() <= s and
                                              x.name.split('_')[-2] in self.action.priceable_names]
                    result_indexes_to_remove = [i for i, x in enumerate(res_fut) if
                                                dt.datetime.strptime(x.name.split('_')[-1], '%Y-%m-%d').date() <= s and
                                                x.name.split('_')[-2] in self.action.priceable_names]
                else:
                    # List of trade names not provided -> TradeDate <= exit trigger date and trade present on trigger
                    # date
                    port_indexes_to_remove = [i for i, x in enumerate(pos_fut) if x.name in current_trade_names]
                    result_indexes_to_remove = [i for i, x in enumerate(res_fut) if x.name in current_trade_names]

                for index in sorted(port_indexes_to_remove, reverse=True):
                    # Get list of trades that have been removed to check for their future cash flow date
                    if pos_fut[index].name not in trades_to_remove:
                        trades_to_remove.append(pos_fut[index])
                    del pos_fut[index]
                for index in sorted(result_indexes_to_remove, reverse=True):
                    del res_futures[index]
                backtest.portfolio_dict[port_date] = Portfolio(tuple(pos_fut))
                if result_indexes_to_remove:
                    backtest.results[port_date] = PortfolioRiskResult(backtest.portfolio_dict[port_date],
                                                                      backtest.results[port_date].risk_measures,
                                                                      res_futures)

            for cp_date, cp_list in list(backtest.cash_payments.items()):
                if cp_date > s:
                    indexes_to_remove = [i for i, cp in enumerate(cp_list)
                                         if cp.trade.name in [x.name for x in trades_to_remove]]
                    for index in sorted(indexes_to_remove, reverse=True):
                        cp = cp_list[index]
                        prev_pos = [i for i, x in enumerate(backtest.cash_payments[s]) if cp.trade.name == x.trade.name]
                        # If trade already exists in exit trigger date cash payments, net out the position
                        if prev_pos:
                            backtest.cash_payments[s][prev_pos[0]].direction += cp.direction
                        else:
                            cp.effective_date = s
                            backtest.cash_payments[s].append(cp)
                        backtest.transaction_cost_entries[s].append(cp.transaction_cost_entry)
                        backtest.transaction_cost_entries[cp_date].remove(cp.transaction_cost_entry)
                        cp.transaction_cost_entry.date = s
                        del backtest.cash_payments[cp_date][index]

                    if not backtest.cash_payments[cp_date]:
                        del backtest.cash_payments[cp_date]

            for trade in trades_to_remove:
                if trade.name not in [x.trade.name for x in backtest.cash_payments[s]]:
                    # to_dict omits name
                    trade_instruments = set(t.to_dict() for t in trade.all_instruments) if \
                        isinstance(trade, Portfolio) else {trade.to_dict()}
                    # find TCE corresponding to trade
                    trade_tce = [tce for tce in backtest.transaction_cost_entries[s] if
                                 set(i.to_dict() for i in tce.all_instruments) == trade_instruments]
                    tce = trade_tce[0] if trade_tce else None
                    backtest.cash_payments[s].append(CashPayment(trade, effective_date=s, transaction_cost_entry=tce))

        return backtest


class RebalanceActionImpl(ActionHandler):
    def __init__(self, action: RebalanceAction):
        super().__init__(action)

    def apply_action(self,
                     state: Union[date, Iterable[date]],
                     backtest: BackTest,
                     trigger_info: Optional[Union[RebalanceActionInfo, Iterable[RebalanceActionInfo]]] = None):

        new_size = self.action.method(state, backtest, trigger_info)
        current_size = 0
        for trade in backtest.portfolio_dict[state]:
            if self.action.priceable.name.split('_')[-1] in trade.name:
                current_size += getattr(trade, self.action.size_parameter)
        # if we are already at the required size then do nothing.
        if new_size - current_size == 0:
            return backtest
        pos = self.action.priceable.clone(**{self.action.size_parameter: new_size - current_size,
                                             'name': f'{self.action.priceable.name}_{state}'})

        current_tc_entries = []
        tc_enter = TransactionCostEntry(state, pos, self.action.transaction_cost)
        current_tc_entries.append(tc_enter)
        backtest.cash_payments[state].append(CashPayment(pos, effective_date=state, direction=-1,
                                                         scaling_parameter=self.action.size_parameter,
                                                         transaction_cost_entry=tc_enter))
        backtest.transaction_cost_entries[state].append(tc_enter)
        unwind_payment = None
        cash_payment_dates = backtest.cash_payments.keys()
        for d in reversed(sorted(cash_payment_dates)):
            for cp in backtest.cash_payments[d]:
                if self.action.priceable.name.split('_')[-1] in cp.trade.name and cp.direction == 1:
                    tc_exit = TransactionCostEntry(d, pos, self.action.transaction_cost_exit)
                    current_tc_entries.append(tc_exit)
                    unwind_payment = CashPayment(pos, effective_date=d, scaling_parameter=self.action.size_parameter,
                                                 transaction_cost_entry=tc_exit)
                    backtest.cash_payments[d].append(unwind_payment)
                    backtest.transaction_cost_entries[d].append(exit)
                    break
            if unwind_payment:
                break

        if unwind_payment is None:
            raise ValueError("Found no final cash payment to rebalance for trade.")

        for s in backtest.states:
            if unwind_payment.effective_date > s >= state:
                backtest.portfolio_dict[s].append(pos)

        with PricingContext(is_async=True):
            if any(tce.no_of_risk_calcs > 0 for tce in current_tc_entries):
                backtest.calc_calls += 1
            for tce in current_tc_entries:
                backtest.calculations += tce.no_of_risk_calcs
                tce.calculate_unit_cost()

        return backtest


class GenericEngineActionFactory(ActionHandlerBaseFactory):
    def __init__(self, action_impl_map=None):
        self.action_impl_map = {
            AddTradeAction: AddTradeActionImpl,
            HedgeAction: HedgeActionImpl,
            ExitTradeAction: ExitTradeActionImpl,
            ExitAllPositionsAction: ExitTradeActionImpl,
            RebalanceAction: RebalanceActionImpl,
            AddScaledTradeAction: AddScaledTradeActionImpl,
            **(action_impl_map or {})
        }

    def get_action_handler(self, action: Action) -> ActionHandler:
        def is_eq_underlier(leg):
            if hasattr(leg, 'asset_class'):
                return isinstance(leg.asset_class, AssetClass) and leg.asset_class == AssetClass.Equity
            return leg.__class__.__name__.lower().startswith('eq')

        if type(action) in self.action_impl_map:
            return self.action_impl_map[type(action)](action)
        raise RuntimeError(f'Action {type(action)} not supported by engine')


class GenericEngine(BacktestBaseEngine):

    def __init__(self, action_impl_map=None, price_measure=Price):
        self.action_impl_map = {} if action_impl_map is None else action_impl_map
        self.price_measure = price_measure
        self._pricing_context_params = None
        self._initial_pricing_context = None
        self._tracing_enabled = False

    def get_action_handler(self, action: Action) -> ActionHandler:
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

    def new_pricing_context(self):
        """
        generate context with the same params to avoid duplication
        """
        context_params = self._pricing_context_params

        show_progress = context_params.get('show_progress', False)
        csa_term = context_params.get('csa_term')
        market_data_location = context_params.get('market_data_location')
        request_priority = context_params.get('request_priority', DEFAULT_REQUEST_PRIORITY)
        is_batch = context_params.get('is_batch', True)

        context = PricingContext(set_parameters_only=True, show_progress=show_progress, csa_term=csa_term,
                                 market_data_location=market_data_location, request_priority=request_priority,
                                 is_batch=is_batch, use_historical_diddles_only=True)

        context._max_concurrent = 1500
        context._dates_per_batch = 200

        return context

    def run_backtest(self, strategy: Strategy, start: Optional[dt.date] = None, end: Optional[dt.date] = None,
                     frequency: Optional[str] = '1m', states: Optional[Iterable[dt.date]] = None,
                     risks: Optional[Iterable[RiskMeasure]] = None, show_progress: bool = True,
                     csa_term: Optional[str] = None, visible_to_gs: bool = False, initial_value: float = 0,
                     result_ccy: Optional[Union[str, Currency]] = None, holiday_calendar: Optional[str] = None,
                     market_data_location: Optional[str] = None, is_batch: bool = True,
                     calc_risk_at_trade_exits: bool = False, pnl_explain: Optional[PnlDefinition] = None):
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
        :param market_data_location: location for the market data
        :param is_batch: use websockets to reduce timeout issues
        :param calc_risk_at_trade_exits: separate results for requested risk measures on tradable exit dates;
                                         not to be included in main results but useful for PnL decomposition
        :param pnl_explain: a Pnl Definition object which defines the risk attribution and mkt data for a pnl explain
        :return: a backtest object containing the portfolios on each day and results which show all risks on all days

        """

        logger.info(f'Starting Backtest: Building Date Schedule - {dt.datetime.now()}')
        self._tracing_enabled = Tracer.get_instance().active_span is not None
        self._pricing_context_params = {'show_progress': show_progress,
                                        'csa_term': csa_term,
                                        'visible_to_gs': visible_to_gs,
                                        'market_data_location': market_data_location,
                                        'is_batch': is_batch}

        with self.new_pricing_context():
            return self.__run(strategy, start, end, frequency, states, risks, initial_value,
                              result_ccy, holiday_calendar, calc_risk_at_trade_exits, pnl_explain)

    def _trace(self, label: str):
        if self._tracing_enabled:
            return Tracer(label)
        else:
            return nullcontext()

    def __run(self, strategy, start, end, frequency, states, risks, initial_value, result_ccy, holiday_calendar,
              calc_risk_at_trade_exits, pnl_explain):
        """
        Run the backtest strategy using the ambient pricing context
        """
        with self._trace('Relative Schedule'):
            strategy_pricing_dates = RelativeDateSchedule(frequency, start, end).apply_rule(
                holiday_calendar=holiday_calendar) if states is None else states

        strategy_pricing_dates.sort()

        strategy_start_date = strategy_pricing_dates[0]
        strategy_end_date = strategy_pricing_dates[-1]

        for trigger in strategy.triggers:
            strategy_pricing_dates += [t for t in trigger.get_trigger_times()
                                       if strategy_start_date <= t <= strategy_end_date]

        strategy_pricing_dates = list(set(strategy_pricing_dates))
        strategy_pricing_dates.sort()
        if pnl_explain is not None:
            calc_risk_at_trade_exits = True
            pnl_risks = pnl_explain.get_risks()
        else:
            pnl_risks = []
        risks = list(set(make_list(risks) + strategy.risks + pnl_risks + [self.price_measure]))
        if result_ccy is not None:
            risks = [(r(currency=result_ccy) if isinstance(r, ParameterisedRiskMeasure)
                      else raiser(f'Unparameterised risk: {r}')) for r in risks]

        if result_ccy is not None:
            if isinstance(self.price_measure, ParameterisedRiskMeasure):
                price_risk = self.price_measure(currency=result_ccy)
            else:
                raiser(f'Unparameterised price measure: {self.price_measure}')
        else:
            price_risk = self.price_measure

        backtest = BackTest(strategy, strategy_pricing_dates, risks, price_risk, holiday_calendar, pnl_explain)

        logger.info('Resolving initial portfolio')
        with self._trace('Resolve initial portfolio'):
            self._resolve_initial_portfolio(strategy.initial_portfolio, backtest, strategy_start_date,
                                            strategy_pricing_dates, holiday_calendar)

        logger.info('Building simple and semi-deterministic triggers and actions')
        self._build_simple_and_semi_triggers_and_actions(strategy, backtest, strategy_pricing_dates)

        logger.info(f'Filtering strategy calculations to run from {strategy_start_date} to {strategy_end_date}')
        backtest.portfolio_dict = defaultdict(Portfolio, {k: backtest.portfolio_dict[k]
                                                          for k in backtest.portfolio_dict
                                                          if strategy_start_date <= k <= strategy_end_date})
        backtest.hedges = defaultdict(list, {k: backtest.hedges[k]
                                             for k in backtest.hedges
                                             if strategy_start_date <= k <= strategy_end_date})

        logger.info('Pricing simple and semi-deterministic triggers and actions')
        with self._trace('Pricing semi-det Triggers'):
            self._price_semi_det_triggers(backtest, risks)

        logger.info('Scaling semi-determ triggers and actions and calculating path dependent triggers and actions')
        with self._trace('Process dates') as scope:
            if scope:
                scope.span.set_tag('dates.length', len(strategy_pricing_dates))
            for d in strategy_pricing_dates:
                if scope:
                    scope.span.log_kv({'date': str(d)})
                self._process_triggers_and_actions_for_date(d, strategy, backtest, risks)

        with self._trace('Calc New Trades'):
            self._calc_new_trades(backtest, risks)

        with self._trace('Handle Cash'):
            self._handle_cash(backtest, risks, price_risk, strategy_pricing_dates, strategy_end_date, initial_value,
                              calc_risk_at_trade_exits, strategy.cash_accrual)

        with self._trace('Populate Transaction Costs'):
            backtest.transaction_costs = {d: -sum(tce.get_final_cost() for tce in tce_list)
                                          for d, tce_list in backtest.transaction_cost_entries.items()}

        logger.info(f'Finished Backtest:- {dt.datetime.now()}')
        return backtest

    def _resolve_initial_portfolio(self, initial_portfolio, backtest, strategy_start_date, strategy_pricing_dates,
                                   holiday_calendar, duration=None):
        if isinstance(initial_portfolio, dict):
            sorted_dates = sorted(list(initial_portfolio.keys()))
            for i, d in enumerate(sorted_dates):
                portfolio = make_list(initial_portfolio[d])
                end_date = sorted_dates[i + 1] if i + 1 < len(sorted_dates) else strategy_pricing_dates[-1]
                self._resolve_initial_portfolio(portfolio, backtest, d, strategy_pricing_dates, holiday_calendar,
                                                end_date)
        else:
            if len(initial_portfolio):
                renamed_port = []
                for index in range(len(initial_portfolio)):
                    old_name = initial_portfolio[index].name
                    renamed_inst = initial_portfolio[index].clone(
                        name=f'{old_name}_{strategy_start_date.strftime("%Y-%m-%d")}')
                    renamed_port.append(renamed_inst)
                    entry_payment = CashPayment(renamed_inst,
                                                effective_date=strategy_start_date, direction=-1)
                    backtest.cash_payments[strategy_start_date].append(entry_payment)
                    final_date = get_final_date(renamed_inst, strategy_start_date, duration,
                                                holiday_calendar)
                    exit_payment = CashPayment(initial_portfolio[index],
                                               effective_date=final_date)
                    backtest.cash_payments[final_date].append(exit_payment)
                init_port = Portfolio(renamed_port)
                with PricingContext(strategy_start_date):
                    init_port.resolve()
                for d in strategy_pricing_dates:
                    if duration is None or (d >= strategy_start_date and
                                            (d < duration or duration == strategy_pricing_dates[-1])):
                        backtest.portfolio_dict[d].append(init_port.instruments)

    def _build_simple_and_semi_triggers_and_actions(self, strategy, backtest, strategy_pricing_dates):
        for trigger in strategy.triggers:
            if trigger.calc_type != CalcType.path_dependent:
                triggered_dates = []
                trigger_infos = defaultdict(list)
                with self._trace('Build semi-det trigger') as scope:
                    for d in strategy_pricing_dates:
                        t_info = trigger.has_triggered(d, backtest)
                        if t_info:
                            triggered_dates.append(d)
                            if t_info.info_dict:
                                for k, v in t_info.info_dict.items():
                                    trigger_infos[k].append(v)
                    if scope:
                        scope.span.set_tag('trigger.type', type(trigger).__name__)
                        scope.span.set_tag('dates.triggered', len(triggered_dates))
                        scope.span.set_tag('action.count', len(trigger.actions))

                    for action in trigger.actions:
                        if action.calc_type != CalcType.path_dependent:
                            with self._trace('Build semi-det action') as scope:
                                if scope:
                                    scope.span.set_tag('action.type', type(action).__name__)
                                trigger_info = None
                                if type(action) in trigger_infos:
                                    trigger_info = trigger_infos[type(action)]
                                else:
                                    for mapped_action_type, action_trigger_info in trigger_infos.items():
                                        if isinstance(action, mapped_action_type):
                                            trigger_info = action_trigger_info
                                            break
                                self.get_action_handler(action).apply_action(
                                    triggered_dates,
                                    backtest,
                                    trigger_info
                                )

    @staticmethod
    def _price_semi_det_triggers(backtest, risks):
        with PricingContext():
            backtest.calc_calls += 1
            for day, portfolio in backtest.portfolio_dict.items():
                if isinstance(day, dt.date):
                    with PricingContext(day):
                        backtest.calculations += len(portfolio) * len(risks)
                        backtest.add_results(day, portfolio.calc(tuple(risks)))

            # semi path dependent initial calc
            for _, hedge_list in backtest.hedges.items():
                scaling_list = [h.scaling_portfolio for h in hedge_list]
                for p in scaling_list:
                    with HistoricalPricingContext(dates=p.dates):
                        backtest.calculations += len(risks) * len(p.dates)
                        port = p.trade if isinstance(p.trade, Portfolio) else Portfolio([p.trade])
                        p.results = port.calc(tuple(risks))

    def _process_triggers_and_actions_for_date(self, d, strategy, backtest: BackTest, risks):
        logger.debug(f'{d}: Processing triggers and actions')
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
            if not backtest.results[d] or t.name not in backtest.results[d].portfolio:
                port.append(t)

        if len(port):
            with PricingContext(pricing_date=d):
                results = Portfolio(port).calc(tuple(risks))

            backtest.add_results(d, results)

        for hedge in backtest.hedges[d]:
            sp = hedge.scaling_portfolio
            if sp.results is None:
                with HistoricalPricingContext(dates=sp.dates):
                    backtest.calculations += len(risks) * len(sp.dates)
                    port_sp = sp.trade if isinstance(sp.trade, Portfolio) else Portfolio([sp.trade])
                    sp.results = port_sp.calc(tuple(risks))

        # semi path dependent scaling
        if d in backtest.hedges:
            if len(backtest.hedges[d]) and d not in backtest.results:
                # No risk found to hedge, proceed to the next date
                return
            for hedge in backtest.hedges[d]:
                p = hedge.scaling_portfolio
                current_risk = backtest.results[d][p.risk] \
                    .transform(risk_transformation=p.risk_transformation).aggregate(allow_mismatch_risk_keys=True)
                hedge_risk = p.results[d][p.risk].transform(risk_transformation=p.risk_transformation).aggregate()
                if hedge_risk == 0:
                    continue
                if current_risk.unit != hedge_risk.unit:
                    raise RuntimeError('cannot hedge in a different currency')
                scaling_factor = current_risk / hedge_risk
                hedge.entry_payment.transaction_cost_entry.additional_scaling = scaling_factor
                if hedge.exit_payment is not None:
                    hedge.exit_payment.transaction_cost_entry.additional_scaling = scaling_factor
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
                        # add scaled hedge position to portfolio for day.
                        # NOTE this adds leaves, not the portfolio
                        backtest.portfolio_dict[day] += copy.deepcopy(scaled_portfolio_position)

                    # scale trade in hedge cash payments
                    hedge.entry_payment.trade = copy.deepcopy(scaled_portfolio_position)
                    if hedge.exit_payment is not None:
                        hedge.exit_payment.trade = copy.deepcopy(scaled_portfolio_position)
                        hedge.exit_payment.scale_date = None
                else:
                    new_notional = getattr(p.trade, p.scaling_parameter) * -scaling_factor
                    scaled_trade = p.trade.clone(**{p.scaling_parameter: new_notional, 'name': p.trade.name})
                    for day in p.dates:
                        backtest.add_results(day, p.results[day] * -scaling_factor)
                        backtest.portfolio_dict[day] += Portfolio(scaled_trade)
                # Add payments to backtest cash payments
                # Scaled if portfolio, otherwise picked up from scaled results or scaled via scale_date
                backtest.cash_payments[hedge.entry_payment.effective_date].append(hedge.entry_payment)
                if hedge.exit_payment is not None:
                    backtest.cash_payments[hedge.exit_payment.effective_date].append(hedge.exit_payment)

    def _calc_new_trades(self, backtest, risks):
        logger.info('Calculating and scaling newly added portfolio positions')
        # test to see if new trades have been added and calc
        with PricingContext():
            backtest.calc_calls += 1
            leaves_by_date = {}
            for day, portfolio in backtest.portfolio_dict.items():
                # Nothing to schedule for calculation, continue
                if not portfolio:
                    continue
                results_for_date = backtest.results[day]

                trades_for_date = results_for_date.portfolio if isinstance(results_for_date, PortfolioRiskResult) \
                    else []
                leaves = []
                for leaf in portfolio:
                    if leaf.name not in trades_for_date:
                        logger.debug(f'{day}: new portfolio position {leaf.name} scheduled for calculation')
                        leaves.append(leaf)

                if len(leaves):
                    with PricingContext(pricing_date=day):
                        leaves_by_date[day] = Portfolio(leaves).calc(tuple(risks))
                        backtest.calculations += len(leaves) * len(risks)

        logger.info('Processing results for newly added portfolio positions')
        for day, leaves in leaves_by_date.items():
            backtest.add_results(day, leaves)

    def _handle_cash(self, backtest, risks, price_risk, strategy_pricing_dates, strategy_end_date, initial_value,
                     calc_risk_at_trade_exits, cash_accrual):
        logger.info('Calculating prices for cash payments')
        # run any additional calcs to handle cash scaling (e.g. unwinds)
        cash_results = {}
        cash_trades_by_date = defaultdict(list)
        exited_cash_trades_by_date = defaultdict(list)
        for _, cash_payments in backtest.cash_payments.items():
            for cp in cash_payments:
                # only calc if additional point is required
                trades = cp.trade.all_instruments if isinstance(cp.trade, Portfolio) else [cp.trade]
                for trade in trades:
                    if cp.effective_date and cp.effective_date <= strategy_end_date:
                        if cp.effective_date not in backtest.results or \
                                trade not in backtest.results[cp.effective_date]:
                            cash_trades_by_date[cp.effective_date].append(trade)
                            if calc_risk_at_trade_exits and cp.direction == 1:
                                exited_cash_trades_by_date[cp.effective_date].append(trade)
                        else:
                            cp.scale_date = None

        with PricingContext():
            backtest.calc_calls += 1
            for cash_date, trades in cash_trades_by_date.items():
                with PricingContext(cash_date):
                    backtest.calculations += len(risks)
                    cash_results[cash_date] = Portfolio(trades).calc(price_risk)
                    if calc_risk_at_trade_exits and cash_date in exited_cash_trades_by_date:
                        expiring_trades = exited_cash_trades_by_date[cash_date]
                        backtest.trade_exit_risk_results[cash_date] = Portfolio(expiring_trades).calc(risks)

        # handle cash
        current_value = None
        for d in sorted(set(strategy_pricing_dates + list(backtest.cash_payments.keys()))):
            if d <= strategy_end_date:
                if current_value is not None:
                    backtest.cash_dict[d] = current_value[
                        0] if cash_accrual is None else cash_accrual.get_accrued_value(current_value, d)
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
                            ccy = map_ccy_name_to_ccy(next(iter(value.unit)))
                            if d not in backtest.cash_dict:
                                backtest.cash_dict[d] = {ccy: initial_value}
                            if ccy not in backtest.cash_dict[d]:
                                backtest.cash_dict[d][ccy] = 0
                            if cp.scale_date:
                                scale_notional = getattr(backtest.portfolio_dict[cp.scale_date][cp.trade.name],
                                                         cp.scaling_parameter)
                                scale_date_adj = scale_notional / getattr(cp.trade, cp.scaling_parameter)
                                cp.cash_paid[ccy] += value * scale_date_adj * cp.direction
                            else:
                                cp.cash_paid[ccy] += value * cp.direction

                        for ccy, cash_paid in cp.cash_paid.items():
                            backtest.cash_dict[d][ccy] += cash_paid

                    current_value = backtest.cash_dict[d], d

                current_value = copy.deepcopy(current_value)
