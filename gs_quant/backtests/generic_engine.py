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

from collections import defaultdict
from functools import reduce
from typing import Union, Iterable, Optional

from gs_quant.backtests.action_handler import ActionHandlerBaseFactory, ActionHandler
from gs_quant.backtests.actions import (
    Action,
    AddTradeAction,
    HedgeAction,
    ExitTradeAction,
    RebalanceAction,
    ExitAllPositionsAction,
    AddScaledTradeAction,
    AddWeightedTradeAction,
    EarlyExitPositionLimitScaledAction,
)
from gs_quant.backtests.backtest_engine import BacktestBaseEngine
from gs_quant.backtests.backtest_objects import BackTest, CashPayment, PnlDefinition
from gs_quant.backtests.backtest_utils import make_list, CalcType, get_final_date, map_ccy_name_to_ccy
from gs_quant.backtests.generic_engine_action_impls import (
    AddTradeActionImpl,
    AddScaledTradeActionImpl,
    HedgeActionImpl,
    ExitTradeActionImpl,
    RebalanceActionImpl,
    AddWeightedTradeActionImpl,
    EarlyExitPositionLimitScaledActionImpl,
)
from gs_quant.backtests.strategy import Strategy
from gs_quant.common import Currency, ParameterisedRiskMeasure, RiskMeasure
from gs_quant.context_base import nullcontext
from gs_quant.datetime.relative_date import RelativeDateSchedule
from gs_quant.markets import PricingContext, HistoricalPricingContext
from gs_quant.markets.portfolio import Portfolio
from gs_quant.risk import Price
from gs_quant.risk.results import PortfolioRiskResult
from gs_quant.tracing import Tracer

# priority set to contexts making requests to the pricing API (min. 1 - max. 10)
DEFAULT_REQUEST_PRIORITY = 5


def raiser(ex):
    raise RuntimeError(ex)


logger = logging.getLogger(__name__)


class GenericEngineActionFactory(ActionHandlerBaseFactory):
    def __init__(self, action_impl_map=None):
        self.action_impl_map = {
            AddTradeAction: AddTradeActionImpl,
            HedgeAction: HedgeActionImpl,
            ExitTradeAction: ExitTradeActionImpl,
            ExitAllPositionsAction: ExitTradeActionImpl,
            RebalanceAction: RebalanceActionImpl,
            AddScaledTradeAction: AddScaledTradeActionImpl,
            AddWeightedTradeAction: AddWeightedTradeActionImpl,
            EarlyExitPositionLimitScaledAction: EarlyExitPositionLimitScaledActionImpl,
        } | (action_impl_map or {})

    def get_action_handler(self, action: Action) -> ActionHandler:
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

        context = PricingContext(
            set_parameters_only=True,
            show_progress=show_progress,
            csa_term=csa_term,
            market_data_location=market_data_location,
            request_priority=request_priority,
            is_batch=is_batch,
            use_historical_diddles_only=True,
        )

        context._max_concurrent = 1500
        context._dates_per_batch = 200

        return context

    def run_backtest(
        self,
        strategy: Strategy,
        start: Optional[dt.date] = None,
        end: Optional[dt.date] = None,
        frequency: Optional[str] = '1m',
        states: Optional[Iterable[dt.date]] = None,
        risks: Optional[Iterable[RiskMeasure]] = None,
        show_progress: bool = True,
        csa_term: Optional[str] = None,
        visible_to_gs: bool = False,
        initial_value: float = 0,
        result_ccy: Optional[Union[str, Currency]] = None,
        holiday_calendar: Optional[str] = None,
        market_data_location: Optional[str] = None,
        is_batch: bool = True,
        calc_risk_at_trade_exits: bool = False,
        pnl_explain: Optional[PnlDefinition] = None,
    ):
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
        self._tracing_enabled = Tracer.active_span() is not None and Tracer.active_span().is_recording()
        self._pricing_context_params = {
            'show_progress': show_progress,
            'csa_term': csa_term,
            'visible_to_gs': visible_to_gs,
            'market_data_location': market_data_location,
            'is_batch': is_batch,
        }

        with self.new_pricing_context():
            return self.__run(
                strategy,
                start,
                end,
                frequency,
                states,
                risks,
                initial_value,
                result_ccy,
                holiday_calendar,
                calc_risk_at_trade_exits,
                pnl_explain,
            )

    def _trace(self, label: str):
        if self._tracing_enabled:
            return Tracer(label)
        else:
            return nullcontext()

    def __run(
        self,
        strategy,
        start,
        end,
        frequency,
        states,
        risks,
        initial_value,
        result_ccy,
        holiday_calendar,
        calc_risk_at_trade_exits,
        pnl_explain,
    ):
        """
        Run the backtest strategy using the ambient pricing context
        """
        with self._trace('Relative Schedule'):
            strategy_pricing_dates = (
                RelativeDateSchedule(frequency, start, end).apply_rule(holiday_calendar=holiday_calendar)
                if states is None
                else states
            )

        strategy_pricing_dates.sort()

        strategy_start_date = strategy_pricing_dates[0]
        strategy_end_date = strategy_pricing_dates[-1]

        for trigger in strategy.triggers:
            strategy_pricing_dates += [
                t for t in trigger.get_trigger_times() if strategy_start_date <= t <= strategy_end_date
            ]

        strategy_pricing_dates = list(set(strategy_pricing_dates))
        strategy_pricing_dates.sort()
        if pnl_explain is not None:
            calc_risk_at_trade_exits = True
            pnl_risks = pnl_explain.get_risks()
        else:
            pnl_risks = []
        risks = list(set(make_list(risks) + strategy.risks + pnl_risks + [self.price_measure]))
        if result_ccy is not None:
            risks = [
                (
                    r(currency=result_ccy)
                    if isinstance(r, ParameterisedRiskMeasure)
                    else raiser(f'Unparameterised risk: {r}')
                )
                for r in risks
            ]

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
            self._resolve_initial_portfolio(
                strategy.initial_portfolio, backtest, strategy_start_date, strategy_pricing_dates, holiday_calendar
            )

        logger.info('Building simple and semi-deterministic triggers and actions')
        self._build_simple_and_semi_triggers_and_actions(strategy, backtest, strategy_pricing_dates)

        logger.info(f'Filtering strategy calculations to run from {strategy_start_date} to {strategy_end_date}')
        backtest.portfolio_dict = defaultdict(
            Portfolio,
            {
                k: backtest.portfolio_dict[k]
                for k in backtest.portfolio_dict
                if strategy_start_date <= k <= strategy_end_date
            },
        )
        backtest.hedges = defaultdict(
            list, {k: backtest.hedges[k] for k in backtest.hedges if strategy_start_date <= k <= strategy_end_date}
        )
        backtest.weighted_trades = defaultdict(
            list,
            {
                k: backtest.weighted_trades[k]
                for k in backtest.weighted_trades
                if strategy_start_date <= k <= strategy_end_date
            },
        )

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
            self._handle_cash(
                backtest,
                risks,
                price_risk,
                strategy_pricing_dates,
                strategy_end_date,
                initial_value,
                calc_risk_at_trade_exits,
                strategy.cash_accrual,
            )

        with self._trace('Populate Transaction Costs'):
            backtest.transaction_costs = {
                d: -sum(tce.get_final_cost() for tce in tce_list)
                for d, tce_list in backtest.transaction_cost_entries.items()
            }

        logger.info(f'Finished Backtest:- {dt.datetime.now()}')
        return backtest

    def _resolve_initial_portfolio(
        self, initial_portfolio, backtest, strategy_start_date, strategy_pricing_dates, holiday_calendar, duration=None
    ):
        if isinstance(initial_portfolio, dict):
            sorted_dates = sorted(list(initial_portfolio.keys()))
            for i, d in enumerate(sorted_dates):
                portfolio = make_list(initial_portfolio[d])
                end_date = sorted_dates[i + 1] if i + 1 < len(sorted_dates) else strategy_pricing_dates[-1]
                self._resolve_initial_portfolio(
                    portfolio, backtest, d, strategy_pricing_dates, holiday_calendar, end_date
                )
        else:
            if len(initial_portfolio):
                renamed_port = []
                for index in range(len(initial_portfolio)):
                    old_name = initial_portfolio[index].name
                    renamed_inst = initial_portfolio[index].clone(
                        name=f'{old_name}_{strategy_start_date.strftime("%Y-%m-%d")}'
                    )
                    renamed_port.append(renamed_inst)
                    entry_payment = CashPayment(renamed_inst, effective_date=strategy_start_date, direction=-1)
                    backtest.cash_payments[strategy_start_date].append(entry_payment)
                    final_date = get_final_date(renamed_inst, strategy_start_date, duration, holiday_calendar)
                    exit_payment = CashPayment(initial_portfolio[index], effective_date=final_date)
                    backtest.cash_payments[final_date].append(exit_payment)
                init_port = Portfolio(renamed_port)
                with PricingContext(strategy_start_date):
                    init_port.resolve()
                for d in strategy_pricing_dates:
                    if duration is None or (
                        d >= strategy_start_date and (d < duration or duration == strategy_pricing_dates[-1])
                    ):
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
                                self.get_action_handler(action).apply_action(triggered_dates, backtest, trigger_info)

    @staticmethod
    def _price_semi_det_triggers(backtest, risks):
        with PricingContext():
            backtest.calc_calls += 1
            for day, portfolio in backtest.portfolio_dict.items():
                if isinstance(day, dt.date):
                    with PricingContext(day):
                        backtest.calculations += len(portfolio) * len(risks)
                        backtest.add_results(day, portfolio.calc(tuple(risks)))

            # semi path dependent initial calc for hedges
            for _, hedge_list in backtest.hedges.items():
                scaling_list = [h.scaling_portfolio for h in hedge_list]
                for p in scaling_list:
                    with HistoricalPricingContext(dates=p.dates):
                        backtest.calculations += len(risks) * len(p.dates)
                        port = p.trade if isinstance(p.trade, Portfolio) else Portfolio([p.trade])
                        p.results = port.calc(tuple(risks))

            # semi path dependent initial calc for weighted trades
            for _, weighted_trade_list in backtest.weighted_trades.items():
                for wt in weighted_trade_list:
                    sp = wt.scaling_portfolio
                    with HistoricalPricingContext(dates=sp.dates):
                        backtest.calculations += len(risks) * len(sp.dates) * len(sp.trades)
                        sp.results = sp.trades.calc(tuple(risks))

    @staticmethod
    def __ensure_risk_results(dates, backtest: BackTest, risks):
        port_by_date = {}
        for d in dates:
            port = []
            for t in backtest.portfolio_dict[d]:
                if not backtest.results[d] or t.name not in backtest.results[d].portfolio:
                    port.append(t)
            if len(port):
                port_by_date[d] = port

        if len(port_by_date):
            results_by_date = {}
            with PricingContext():
                for d, port in port_by_date.items():
                    with PricingContext(pricing_date=d):
                        results_by_date[d] = Portfolio(port).calc(tuple(risks))

            for d, results in results_by_date.items():
                backtest.add_results(d, results)

    def _process_triggers_and_actions_for_date(self, d, strategy, backtest: BackTest, risks):
        logger.debug(f'{d}: Processing triggers and actions')

        # need to ensure risk results for the day are available prior to the path-dependent action/trigger being applied
        # note that __ensure_risk_results sends a risk calculation for the day, so it should only happen when required
        trigger_infos = defaultdict(list)
        for trigger in strategy.triggers:
            if trigger.calc_type == CalcType.path_dependent:
                t_info = trigger.has_triggered(d, backtest)
                if t_info:
                    if t_info.info_dict:
                        for k, v in t_info.info_dict.items():
                            trigger_infos[k].append(v)
                    for action in trigger.actions:
                        self.__ensure_risk_results([d], backtest, risks)
                        trigger_info = trigger_infos.get(type(action), None)
                        self.get_action_handler(action).apply_action(d, backtest, trigger_info)
            else:
                for action in trigger.actions:
                    if action.calc_type == CalcType.path_dependent:
                        t_info = trigger.has_triggered(d, backtest)
                        if t_info:
                            trigger_info = t_info.info_dict.get(type(action), None) if t_info.info_dict else None
                            self.__ensure_risk_results([d], backtest, risks)
                            self.get_action_handler(action).apply_action(d, backtest, trigger_info)
        # explicit check needed because backtest.hedges is a defaultdict that gets populated on access below
        if d not in backtest.hedges and d not in backtest.weighted_trades:
            return
        for hedge in backtest.hedges[d]:
            sp = hedge.scaling_portfolio
            if sp.results is None:
                with HistoricalPricingContext(dates=sp.dates):
                    backtest.calculations += len(risks) * len(sp.dates)
                    port_sp = sp.trade if isinstance(sp.trade, Portfolio) else Portfolio([sp.trade])
                    sp.results = port_sp.calc(tuple(risks))

        # semi path dependent scaling for hedges; only apply if there are any hedges to scale
        if backtest.hedges[d]:
            # ensure all risk results are available (including the hedge risk required to scale below)
            # this is useful when there is overlap between hedges (e.g. an instrument hedging risk from another hedge)
            # note it does not get applied when there is no overlap between hedges, as the ensure fn will skip the calc
            self.__ensure_risk_results([d], backtest, risks)
            # this needs to be applied after the "ensure" line above, which may add results
            # if there is no risk to hedge, skip to the next day; hedges for this day can be ignored
            if d not in backtest.results:
                return
            for hedge in backtest.hedges[d]:
                p = hedge.scaling_portfolio
                current_risk = (
                    backtest.results[d][p.risk]
                    .transform(risk_transformation=p.risk_transformation)
                    .aggregate(allow_mismatch_risk_keys=True)
                )
                hedge_risk = p.results[d][p.risk].transform(risk_transformation=p.risk_transformation).aggregate()
                if hedge_risk == 0:
                    continue
                if current_risk.unit != hedge_risk.unit:
                    raise RuntimeError('cannot hedge in a different currency')
                scaling_factor = current_risk / hedge_risk * hedge.scaling_portfolio.risk_percentage / 100
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
                else:
                    raise RuntimeError('Hedge trade instrument must be a Portfolio')

                # Add cash payments for hedge entry and exit
                backtest.cash_payments[hedge.entry_payment.effective_date].append(hedge.entry_payment)
                if hedge.exit_payment is not None:
                    backtest.cash_payments[hedge.exit_payment.effective_date].append(hedge.exit_payment)

        # semi path dependent scaling for weighted trades
        if d in backtest.weighted_trades and backtest.weighted_trades[d]:
            for weighted_trade in backtest.weighted_trades[d]:
                sp = weighted_trade.scaling_portfolio
                if sp.results is None:
                    with HistoricalPricingContext(dates=sp.dates):
                        backtest.calculations += len(risks) * len(sp.dates) * len(sp.trades)
                        sp.results = sp.trades.calc(tuple(risks))

                # Get risk for each instrument on the entry date
                instrument_risks = {}
                for inst in sp.trades.all_instruments:
                    try:
                        inst_risk = sp.results[d][sp.risk][inst.name]
                        if hasattr(inst_risk, 'aggregate'):
                            inst_risk = inst_risk.aggregate()
                        instrument_risks[inst.name] = abs(inst_risk) if inst_risk != 0 else 0
                    except (KeyError, ValueError):
                        instrument_risks[inst.name] = 0

                # Calculate scaling factors so each instrument is scaled by its proportion of total portfolio risk
                # and the sum of all notionals equals total_size
                num_instruments = len(sp.trades.all_instruments)
                if num_instruments == 0:
                    continue

                total_portfolio_risk = sum(instrument_risks.values())
                if total_portfolio_risk == 0:
                    continue

                scaling_factors = {}
                for inst_name, inst_risk in instrument_risks.items():
                    if inst_risk != 0:
                        # Weight is the proportion of this instrument's risk to total portfolio risk
                        weight = inst_risk / total_portfolio_risk
                        # Notional for this instrument = weight * total_size
                        # Scaling factor = notional (since unit notional instruments)
                        scaling_factors[inst_name] = weight * sp.total_size
                    else:
                        scaling_factors[inst_name] = 0

                # Scale each instrument and add to portfolio
                for idx, inst in enumerate(sp.trades.all_instruments):
                    scaling_factor = scaling_factors.get(inst.name, 0)
                    if scaling_factor == 0:
                        continue

                    scaled_inst = copy.deepcopy(inst)
                    scaled_inst.name = f'Weighted_{inst.name}'
                    scaled_inst.scale(scaling_factor)

                    # Update transaction cost entries with scaling
                    entry_payment = weighted_trade.entry_payments[idx]
                    entry_payment.transaction_cost_entry.additional_scaling = scaling_factor
                    if weighted_trade.exit_payments[idx] is not None:
                        weighted_trade.exit_payments[idx].transaction_cost_entry.additional_scaling = scaling_factor

                    # Add scaled instrument to portfolio for each active date
                    for day in sp.dates:
                        backtest.portfolio_dict[day].append(copy.deepcopy(scaled_inst))

                    # Update cash payment trades with scaled version
                    entry_payment.trade = copy.deepcopy(scaled_inst)
                    if weighted_trade.exit_payments[idx] is not None:
                        weighted_trade.exit_payments[idx].trade = copy.deepcopy(scaled_inst)

                    # Add cash payments
                    backtest.cash_payments[entry_payment.effective_date].append(entry_payment)
                    if weighted_trade.exit_payments[idx] is not None:
                        backtest.cash_payments[weighted_trade.exit_payments[idx].effective_date].append(
                            weighted_trade.exit_payments[idx]
                        )

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

                trades_for_date = (
                    results_for_date.portfolio if isinstance(results_for_date, PortfolioRiskResult) else []
                )
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

    @staticmethod
    def _handle_cash(
        backtest,
        risks,
        price_risk,
        strategy_pricing_dates,
        strategy_end_date,
        initial_value,
        calc_risk_at_trade_exits,
        cash_accrual,
    ):
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
                        if (
                            cp.effective_date not in backtest.results
                            or trade not in backtest.results[cp.effective_date]
                        ):
                            cash_trades_by_date[cp.effective_date].append(trade)
                            if calc_risk_at_trade_exits and cp.direction == 1:
                                exited_cash_trades_by_date[cp.effective_date].append(trade)

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
                    backtest.cash_dict[d] = (
                        current_value[0] if cash_accrual is None else cash_accrual.get_accrued_value(current_value, d)
                    )
                if d in backtest.cash_payments:
                    for cp in backtest.cash_payments[d]:
                        trades = cp.trade.all_instruments if isinstance(cp.trade, Portfolio) else [cp.trade]
                        for trade in trades:
                            value = cash_results.get(cp.effective_date, {}).get(price_risk, {}).get(trade.name, {})
                            try:
                                value = (
                                    backtest.results[cp.effective_date][price_risk][trade.name]
                                    if value == {}
                                    else value
                                )
                            except (KeyError, ValueError):
                                raise RuntimeError(
                                    f'failed to get cash value for {trade.name} on '
                                    f'{cp.effective_date} received value of {value}'
                                )
                            if not isinstance(value, float):
                                raise RuntimeError(
                                    f'failed to get cash value for {trade.name} on '
                                    f'{cp.effective_date} received value of {value}'
                                )
                            ccy = map_ccy_name_to_ccy(next(iter(value.unit)))
                            if d not in backtest.cash_dict:
                                backtest.cash_dict[d] = {ccy: initial_value}
                            if ccy not in backtest.cash_dict[d]:
                                backtest.cash_dict[d][ccy] = 0

                            cp.cash_paid[ccy] += value * cp.direction

                        for ccy, cash_paid in cp.cash_paid.items():
                            backtest.cash_dict[d][ccy] += cash_paid

                    current_value = backtest.cash_dict[d], d

                current_value = copy.deepcopy(current_value)
