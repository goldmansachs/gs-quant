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

import pandas as pd
from copy import deepcopy
from collections import defaultdict
from gs_quant.markets.portfolio import Portfolio
from typing import Iterable
from gs_quant.target.instrument import Cash
from gs_quant.backtests.core import ValuationMethod
from gs_quant.backtests.order import OrderBase, OrderCost
from gs_quant.backtests.event import FillEvent
from gs_quant.backtests.data_handler import DataHandler
import numpy as np
import datetime as dt
from queue import Queue as FifoQueue


class BackTest:
    def __init__(self, strategy, states, risks):
        self._portfolio_dict = defaultdict(Portfolio)  # portfolio by state
        self._cash_dict = defaultdict(float)  # cash by state
        self._scaling_portfolios = defaultdict(list)  # list of ScalingPortfolio
        self._cash_payments = defaultdict(list)  # list of cash payments (entry, unwind)
        self._strategy = deepcopy(strategy)  # the strategy definition
        self._states = states  # list of states
        self._results = defaultdict(list)
        self._risks = tuple(risks)  # list of risks to calculate
        self._calc_calls = 0
        self._calculations = 0

    @property
    def cash_dict(self):
        return self._cash_dict

    @property
    def portfolio_dict(self):
        return self._portfolio_dict

    @portfolio_dict.setter
    def portfolio_dict(self, portfolio_dict):
        self._portfolio_dict = portfolio_dict

    @property
    def scaling_portfolios(self):
        return self._scaling_portfolios

    @scaling_portfolios.setter
    def scaling_portfolios(self, scaling_portfolios):
        self._scaling_portfolios = scaling_portfolios

    @property
    def cash_payments(self):
        return self._cash_payments

    @cash_payments.setter
    def cash_payments(self, cash_payments):
        self._cash_payments = cash_payments

    @property
    def states(self):
        return self._states

    @property
    def results(self):
        return self._results

    def set_results(self, date, results):
        self._results[date] = results

    @property
    def risks(self):
        return self._risks

    def add_results(self, date, results):
        if date in self._results and len(self._results[date]):
            self._results[date] += results
        else:
            self._results[date] = results

    @property
    def calc_calls(self):
        return self._calc_calls

    @calc_calls.setter
    def calc_calls(self, calc_calls):
        self._calc_calls = calc_calls

    @property
    def calculations(self):
        return self._calculations

    @calculations.setter
    def calculations(self, calculations):
        self._calculations = calculations

    @property
    def result_summary(self, allow_mismatch_risk_keys=True):
        summary = pd.DataFrame({date: {risk: results[risk].aggregate(allow_mismatch_risk_keys)
                                       for risk in results.risk_measures} for date, results in self._results.items()}).T
        cash = pd.Series(self._cash_dict, name='Cash')
        return pd.concat([summary, cash], axis=1, sort=True).fillna(0)


class ScalingPortfolio:
    def __init__(self, trade, dates, risk, csa_term=None, scaling_parameter='notional_amount'):
        self.trade = trade
        self.dates = dates
        self.risk = risk
        self.csa_term = csa_term
        self.scaling_parameter = scaling_parameter
        self.results = None


class CashPayment:
    def __init__(self, trade, effective_date=None, scale_date=None, direction=1):
        self.trade = trade
        self.effective_date = effective_date
        self.scale_date = scale_date
        self.direction = direction


class PredefinedAssetBacktest:
    """
    :param data_handler: holds all the data required to run the backtest
    :param performance: backtest values
    :param cash_asset: currently restricted to USD non-accrual
    :param holdings: a dictionary keyed by instruments with quantity values
    :param historical_holdings: holdings for each backtest date
    :param orders: a list of all the orders generated
    :param initial_value: the initial value of the index
    :param results: a dictionary which can be used to store intermediate results
    """
    def __init__(self, data_handler: DataHandler, initial_value: float):
        self.data_handler = data_handler
        self.performance = pd.Series()
        self.cash_asset = Cash('USD')
        self.holdings = defaultdict(float)
        self.historical_holdings = pd.Series()
        self.historical_weights = pd.Series()
        self.orders = []
        self.initial_value = initial_value
        self.results = {}

    def set_start_date(self, start: dt.date):
        self.performance[start] = self.initial_value
        self.holdings[self.cash_asset] = self.initial_value

    def record_orders(self, orders: Iterable[OrderBase]):
        self.orders.extend(orders)

    def update_fill(self, fill: FillEvent):
        inst = fill.order.instrument
        self.holdings[self.cash_asset] -= fill.filled_price * fill.filled_units
        self.holdings[inst] += fill.filled_units

    def trade_ledger(self):
        instrument_queues = {}
        order_pairs = {}
        for o in self.orders:
            if o.instrument not in instrument_queues:
                instrument_queues[o.instrument] = (FifoQueue(), FifoQueue())  # (longs, shorts)
            longs, shorts = instrument_queues[o.instrument]
            if o.quantity < 0:
                shorts.put(o)
            else:
                longs.put(o)

        # match up the longs and shorts
        for inst in instrument_queues.keys():
            longs, shorts = instrument_queues[inst]
            open_close_order_pairs = []
            while not longs.empty() and not shorts.empty():
                long, short = longs.get(), shorts.get()
                open_order, close_order = (long, short) if long.execution_end_time() < short.execution_end_time()\
                    else (short, long)
                open_close_order_pairs.append((open_order, close_order))

            # handle unmatched longs or shorts i.e. positions currently open
            while not longs.empty() or not shorts.empty():
                unclosed_open_order = longs.get() if not longs.empty() else shorts.get()
                open_close_order_pairs.append((unclosed_open_order, None))
            order_pairs[inst] = open_close_order_pairs

        trade_df = []
        for inst in order_pairs.keys():
            for open_order, close_order in [(o, c) for o, c in order_pairs[inst]]:
                if close_order:
                    end_dt = close_order.execution_end_time()
                    end_value = close_order.executed_price
                    status = 'closed'
                else:
                    end_dt = None
                    end_value = None
                    status = 'open'
                start_dt, open_value = open_order.execution_end_time(), open_order.executed_price
                long_or_short = np.sign(open_order.quantity)
                trade_df.append((inst, start_dt, end_dt, open_value, end_value, long_or_short, status,
                                 (end_value - open_value) * long_or_short if status == 'closed' else None))
        return pd.DataFrame(trade_df, columns=['Instrument', 'Open', 'Close', 'Open Value', 'Close Value',
                                               'Long Short', 'Status', 'Trade PnL'])

    def mark_to_market(self, state: dt.datetime, valuation_method: ValuationMethod):
        epsilon = 1e-12
        date = state.date()
        mtm = 0
        self.historical_holdings[date] = {}
        self.historical_weights[date] = {}
        for instrument, units in self.holdings.items():
            if abs(units) > epsilon:
                self.historical_holdings[date][instrument] = units

                if isinstance(instrument, Cash):
                    fixing = 1
                else:
                    tag, window = valuation_method.data_tag, valuation_method.window
                    if window:
                        start = dt.datetime.combine(state.date(), window.start)
                        end = dt.datetime.combine(state.date(), window.end)
                        fixings = self.data_handler.get_data_range(start, end, instrument, tag)
                        fixing = np.mean(fixings) if len(fixings) else np.nan
                    else:  # no time window specified, use daily fixing
                        fixing = self.data_handler.get_data(state.date(), instrument, tag)

                notional = fixing * units
                self.historical_weights[date][instrument] = notional
                mtm += notional

        self.performance[date] = mtm

        for instrument, notional in self.historical_weights[date].items():
            self.historical_weights[date][instrument] = notional / mtm

    def get_level(self, date: dt.date) -> float:
        return self.performance[date]

    def get_costs(self) -> pd.Series():
        costs = defaultdict(float)
        for order in self.orders:
            if isinstance(order, OrderCost):
                costs[order.execution_end_time().date()] += order.execution_quantity(self.data_handler)

        return pd.Series(costs)

    def get_orders_for_date(self, date: dt.date) -> pd.DataFrame():
        return pd.DataFrame([order.to_dict(self.data_handler) for order in self.orders
                             if order.execution_end_time().date() == date])
