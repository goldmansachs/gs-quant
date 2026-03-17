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

from abc import ABCMeta
import datetime as dt
from collections import defaultdict, namedtuple
from itertools import zip_longest
from typing import Union, Iterable, Optional, Dict, Collection

from gs_quant.backtests.actions import (
    Action,
    AddTradeAction,
    HedgeAction,
    AddTradeActionInfo,
    HedgeActionInfo,
    ExitTradeAction,
    ExitTradeActionInfo,
    RebalanceAction,
    RebalanceActionInfo,
    AddScaledTradeAction,
    ScalingActionType,
    AddScaledTradeActionInfo,
    AddWeightedTradeAction,
    AddWeightedTradeActionInfo,
)
from gs_quant.backtests.action_handler import ActionHandler
from gs_quant.backtests.backtest_objects import (
    BackTest,
    ScalingPortfolio,
    CashPayment,
    Hedge,
    TransactionCostEntry,
    WeightedScalingPortfolio,
    WeightedTrade,
)
from gs_quant.backtests.backtest_utils import make_list, get_final_date, interpolate_signal
from gs_quant.common import RiskMeasure
from gs_quant.instrument import Instrument
from gs_quant.markets import PricingContext, HistoricalPricingContext
from gs_quant.markets.portfolio import Portfolio
from gs_quant.risk.results import PortfolioRiskResult
from gs_quant.target.measures import ResolvedInstrumentValues


# Action Implementations
class OrderBasedActionImpl(ActionHandler, metaclass=ABCMeta):
    def __init__(self, action: Action):
        self._order_valuations = [ResolvedInstrumentValues]
        super().__init__(action)

    def get_base_orders_for_states(self, states: Collection[dt.date], **kwargs):
        orders = {}
        dated_priceables = getattr(self.action, 'dated_priceables', {}) or {}
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

    def _raise_order(
        self,
        state: Union[dt.date, Iterable[dt.date]],
        trigger_info: Optional[Union[AddTradeActionInfo, Iterable[AddTradeActionInfo]]] = None,
    ):
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

    def apply_action(
        self,
        state: Union[dt.date, Iterable[dt.date]],
        backtest: BackTest,
        trigger_info: Optional[Union[AddTradeActionInfo, Iterable[AddTradeActionInfo]]] = None,
    ):
        orders = self._raise_order(state, trigger_info)

        current_tc_entries = []
        # record entry and unwind cashflows
        for create_date, (portfolio, info) in orders.items():
            for inst in portfolio.all_instruments:
                tc_enter = TransactionCostEntry(create_date, inst, self.action.transaction_cost)
                current_tc_entries.append(tc_enter)
                backtest.cash_payments[create_date].append(
                    CashPayment(inst, effective_date=create_date, direction=-1, transaction_cost_entry=tc_enter)
                )
                backtest.transaction_cost_entries[create_date].append(tc_enter)
                final_date = self.get_instrument_final_date(inst, create_date, info)
                tc_exit = TransactionCostEntry(final_date, inst, self.action.transaction_cost_exit)
                current_tc_entries.append(tc_exit)
                backtest.cash_payments[final_date].append(
                    CashPayment(inst, effective_date=final_date, transaction_cost_entry=tc_exit)
                )
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
        self._scaling_level_signal = (
            interpolate_signal(self.action.scaling_level) if isinstance(self.action.scaling_level, dict) else None
        )

    @staticmethod
    def __portfolio_scaling_for_available_cash(
        portfolio, available_cash, cur_day, unscaled_prices_by_day, unscaled_entry_tces_by_day
    ) -> float:
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
        first_scale_factor = (available_cash - fixed_tcs) / (
            unscaled_prices_by_day[cur_day].aggregate() + scaling_based_tcs
        )
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
        second_scale_factor = max(available_cash - fixed_tcs, 0) / (
            unscaled_prices_by_day[cur_day].aggregate() * first_scale_factor + scaling_based_tcs
        )
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
            scale_factor = self.__portfolio_scaling_for_available_cash(
                portfolio, available_cash, cur_day, unscaled_prices_by_day, unscaled_entry_tces_by_day
            )
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

    def _scaling_level_for_date(self, d: dt.date) -> float:
        if self._scaling_level_signal is not None:
            if d in self._scaling_level_signal:
                return self._scaling_level_signal[d]
            return 0
        else:
            return self.action.scaling_level

    def _scale_order(self, orders, daily_risk, price_measure, trigger_infos):
        if self.action.scaling_type == ScalingActionType.size:
            for day, portfolio in orders.items():
                portfolio.scale(self._scaling_level_for_date(day))
        elif self.action.scaling_type == ScalingActionType.NAV:
            self._nav_scale_orders(orders, price_measure, trigger_infos)
        elif self.action.scaling_type == ScalingActionType.risk_measure:
            for day, portfolio in orders.items():
                scaling_factor = self._scaling_level_for_date(day) / daily_risk[day]
                portfolio.scale(scaling_factor)
        else:
            raise RuntimeError(f'Scaling Type {self.action.scaling_type} not supported by engine')

    def _raise_order(
        self,
        state_list: Collection[dt.date],
        price_measure: RiskMeasure,
        trigger_infos: Dict[dt.date, Optional[Union[AddScaledTradeActionInfo, Iterable[AddScaledTradeActionInfo]]]],
    ):
        if self.action.scaling_type == ScalingActionType.risk_measure:
            self._order_valuations.append(self.action.scaling_risk)
        orders = self.get_base_orders_for_states(state_list, trigger_infos=trigger_infos)

        final_orders = {}
        for d, res in orders.items():
            new_port = []
            dated_priceables = getattr(self.action, 'dated_priceables', {}) or {}
            instruments = dated_priceables.get(d) or self.action.priceables
            for inst in instruments:
                new_inst = res[inst]
                if len(self._order_valuations) > 1:
                    new_inst = new_inst[ResolvedInstrumentValues]
                new_inst.name = f'{new_inst.name}_{d}'
                new_port.append(new_inst)
            final_orders[d] = Portfolio(new_port)
        daily_risk = (
            {d: res[self.action.scaling_risk].aggregate() for d, res in orders.items()}
            if self.action.scaling_type == ScalingActionType.risk_measure
            else None
        )

        self._scale_order(final_orders, daily_risk, price_measure, trigger_infos)

        return final_orders

    def apply_action(
        self,
        state: Union[dt.date, Iterable[dt.date]],
        backtest: BackTest,
        trigger_info: Optional[Union[AddScaledTradeActionInfo, Iterable[AddScaledTradeActionInfo]]] = None,
    ):
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
                backtest.cash_payments[create_date].append(
                    CashPayment(inst, effective_date=create_date, direction=-1, transaction_cost_entry=tc_enter)
                )
                backtest.transaction_cost_entries[create_date].append(tc_enter)
                final_date = self.get_instrument_final_date(inst, create_date, info)
                tc_exit = TransactionCostEntry(final_date, inst, self.action.transaction_cost_exit)
                current_tc_entries.append(tc_exit)
                backtest.cash_payments[final_date].append(
                    CashPayment(inst, effective_date=final_date, transaction_cost_entry=tc_exit)
                )
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

    def get_base_orders_for_states(self, states: Collection[dt.date], **kwargs):
        with HistoricalPricingContext(dates=states, csa_term=self.action.csa_term):
            f = Portfolio(self.action.priceable).resolve(in_place=False)
        return f.result()

    def apply_action(
        self,
        state: Union[dt.date, Iterable[dt.date]],
        backtest: BackTest,
        trigger_info: Optional[Union[HedgeActionInfo, Iterable[HedgeActionInfo]]] = None,
    ):
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
                scaling_portfolio = ScalingPortfolio(
                    trade=hedge_trade,
                    dates=active_dates,
                    risk=self.action.risk,
                    csa_term=self.action.csa_term,
                    risk_transformation=self.action.risk_transformation,
                    risk_percentage=self.action.risk_percentage,
                )
                tc_enter = TransactionCostEntry(create_date, hedge_trade, self.action.transaction_cost)
                current_tc_entries.append(tc_enter)
                entry_payment = CashPayment(
                    trade=hedge_trade, effective_date=create_date, direction=-1, transaction_cost_entry=tc_enter
                )
                backtest.transaction_cost_entries[create_date].append(tc_enter)
                tc_exit = TransactionCostEntry(final_date, hedge_trade, self.action.transaction_cost_exit)
                current_tc_entries.append(tc_exit)
                exit_payment = (
                    CashPayment(trade=hedge_trade, effective_date=final_date, transaction_cost_entry=tc_exit)
                    if final_date <= dt.date.today()
                    else None
                )
                backtest.transaction_cost_entries[final_date].append(tc_exit)
                hedge = Hedge(
                    scaling_portfolio=scaling_portfolio, entry_payment=entry_payment, exit_payment=exit_payment
                )
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

    def apply_action(
        self,
        state: Union[dt.date, Iterable[dt.date]],
        backtest: BackTest,
        trigger_info: Optional[Union[ExitTradeActionInfo, Iterable[ExitTradeActionInfo]]] = None,
    ):
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
                    port_indexes_to_remove = [
                        i
                        for i, x in enumerate(pos_fut)
                        if dt.datetime.strptime(x.name.split('_')[-1], '%Y-%m-%d').date() <= s
                        and x.name.split('_')[-2] in self.action.priceable_names
                    ]
                    result_indexes_to_remove = [
                        i
                        for i, x in enumerate(res_fut)
                        if dt.datetime.strptime(x.name.split('_')[-1], '%Y-%m-%d').date() <= s
                        and x.name.split('_')[-2] in self.action.priceable_names
                    ]
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
                    del res_fut[index]
                    del res_futures[index]
                backtest.portfolio_dict[port_date] = Portfolio(tuple(pos_fut))
                if result_indexes_to_remove:
                    backtest.results[port_date] = PortfolioRiskResult(
                        Portfolio(res_fut), backtest.results[port_date].risk_measures, res_futures
                    )

            for cp_date, cp_list in list(backtest.cash_payments.items()):
                if cp_date > s:
                    indexes_to_remove = [
                        i for i, cp in enumerate(cp_list) if cp.trade.name in [x.name for x in trades_to_remove]
                    ]
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
                    trade_instruments = (
                        set(t.to_dict() for t in trade.all_instruments)
                        if isinstance(trade, Portfolio)
                        else {trade.to_dict()}
                    )
                    # find TCE corresponding to trade
                    trade_tce = [
                        tce
                        for tce in backtest.transaction_cost_entries[s]
                        if set(i.to_dict() for i in tce.all_instruments) == trade_instruments
                    ]
                    tce = trade_tce[0] if trade_tce else None
                    backtest.cash_payments[s].append(CashPayment(trade, effective_date=s, transaction_cost_entry=tce))

        return backtest


class RebalanceActionImpl(ActionHandler):
    def __init__(self, action: RebalanceAction):
        super().__init__(action)

    def apply_action(
        self,
        state: Union[dt.date, Iterable[dt.date]],
        backtest: BackTest,
        trigger_info: Optional[Union[RebalanceActionInfo, Iterable[RebalanceActionInfo]]] = None,
    ):
        new_size = self.action.method(state, backtest, trigger_info)
        current_size = 0
        for trade in backtest.portfolio_dict[state]:
            if self.action.priceable.name.split('_')[-1] in trade.name:
                current_size += getattr(trade, self.action.size_parameter)
        # if we are already at the required size then do nothing.
        if new_size - current_size == 0:
            return backtest
        pos = self.action.priceable.clone(
            **{self.action.size_parameter: new_size - current_size, 'name': f'{self.action.priceable.name}_{state}'}
        )

        current_tc_entries = []
        tc_enter = TransactionCostEntry(state, pos, self.action.transaction_cost)
        current_tc_entries.append(tc_enter)
        backtest.cash_payments[state].append(
            CashPayment(pos, effective_date=state, direction=-1, transaction_cost_entry=tc_enter)
        )
        backtest.transaction_cost_entries[state].append(tc_enter)
        unwind_payment = None
        cash_payment_dates = backtest.cash_payments.keys()
        for d in reversed(sorted(cash_payment_dates)):
            for cp in backtest.cash_payments[d]:
                if self.action.priceable.name.split('_')[-1] in cp.trade.name and cp.direction == 1:
                    tc_exit = TransactionCostEntry(d, pos, self.action.transaction_cost_exit)
                    current_tc_entries.append(tc_exit)
                    unwind_payment = CashPayment(pos, effective_date=d, transaction_cost_entry=tc_exit)
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


class AddWeightedTradeActionImpl(OrderBasedActionImpl):
    def __init__(self, action: AddWeightedTradeAction):
        super().__init__(action)

    def get_base_orders_for_states(self, states: Collection[dt.date], **kwargs):
        with HistoricalPricingContext(dates=states):
            f = Portfolio(self.action.priceables).resolve(in_place=False)
        return f.result()

    def apply_action(
        self,
        state: Union[dt.date, Iterable[dt.date]],
        backtest: BackTest,
        trigger_info: Optional[Union[AddWeightedTradeActionInfo, Iterable[AddWeightedTradeActionInfo]]] = None,
    ):
        state_list = make_list(state)
        if trigger_info is None or isinstance(trigger_info, AddWeightedTradeActionInfo):
            trigger_info = [trigger_info for _ in range(len(state_list))]
        trigger_infos = dict(zip_longest(state_list, trigger_info))
        backtest.calc_calls += 1
        backtest.calculations += len(state_list)
        orders = self.get_base_orders_for_states(state_list, trigger_infos=trigger_infos)

        current_tc_entries = []
        for create_date, portfolio in orders.items():
            info = trigger_infos[create_date]
            # Get all instruments from the resolved portfolio
            instruments = portfolio.priceables
            if not instruments:
                continue

            # Rename instruments with the create date
            renamed_instruments = []
            for inst in instruments:
                renamed_inst = inst.clone(name=f'{inst.name}_{create_date.strftime("%Y-%m-%d")}')
                renamed_instruments.append(renamed_inst)

            weighted_portfolio = Portfolio(renamed_instruments)
            final_date = self.get_instrument_final_date(renamed_instruments[0], create_date, info)
            active_dates = [s for s in backtest.states if create_date <= s < final_date]

            if len(active_dates):
                scaling_portfolio = WeightedScalingPortfolio(
                    trades=weighted_portfolio,
                    dates=active_dates,
                    risk=self.action.scaling_risk,
                    total_size=self.action.total_size,
                )

                # Create entry and exit payments for each instrument
                entry_payments = []
                exit_payments = []
                for inst in renamed_instruments:
                    tc_enter = TransactionCostEntry(create_date, inst, self.action.transaction_cost)
                    current_tc_entries.append(tc_enter)
                    entry_payment = CashPayment(
                        trade=inst, effective_date=create_date, direction=-1, transaction_cost_entry=tc_enter
                    )
                    entry_payments.append(entry_payment)
                    backtest.transaction_cost_entries[create_date].append(tc_enter)

                    tc_exit = TransactionCostEntry(final_date, inst, self.action.transaction_cost_exit)
                    current_tc_entries.append(tc_exit)
                    exit_payment = (
                        CashPayment(trade=inst, effective_date=final_date, transaction_cost_entry=tc_exit)
                        if final_date <= dt.date.today()
                        else None
                    )
                    exit_payments.append(exit_payment)
                    backtest.transaction_cost_entries[final_date].append(tc_exit)

                weighted_trade = WeightedTrade(
                    scaling_portfolio=scaling_portfolio,
                    entry_payments=entry_payments,
                    exit_payments=exit_payments,
                )
                backtest.weighted_trades[create_date].append(weighted_trade)

        with PricingContext(is_async=True):
            if any(tce.no_of_risk_calcs > 0 for tce in current_tc_entries):
                backtest.calc_calls += 1
            for tce in current_tc_entries:
                backtest.calculations += tce.no_of_risk_calcs
                tce.calculate_unit_cost()

        return backtest
