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
import datetime as dt
from abc import ABC
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from queue import Queue as FifoQueue
from typing import Iterable, TypeVar, Optional

import numpy as np
import pandas as pd

from gs_quant.common import RiskMeasure
from gs_quant.instrument import Cash
from gs_quant.markets.portfolio import Portfolio
from gs_quant.backtests.backtest_utils import make_list
from gs_quant.backtests.core import ValuationMethod
from gs_quant.backtests.data_handler import DataHandler
from gs_quant.backtests.event import FillEvent
from gs_quant.backtests.order import OrderBase, OrderCost
from gs_quant.risk.transform import Transformer


class BaseBacktest(ABC):
    pass


TBaseBacktest = TypeVar('TBaseBacktest', bound='BaseBacktest')


@dataclass_json
@dataclass
class BackTest(BaseBacktest):
    strategy: object
    states: Iterable
    risks: Iterable[RiskMeasure]

    def __post_init__(self):
        self._portfolio_dict = defaultdict(Portfolio)  # portfolio by state
        self._cash_dict = {}  # cash by state
        self._hedges = defaultdict(list)  # list of Hedge by date
        self._cash_payments = defaultdict(list)  # list of cash payments (entry, unwind)
        self._transaction_costs = defaultdict(int)  # list of transaction costs by date
        self.strategy = deepcopy(self.strategy)  # the strategy definition
        self._results = defaultdict(list)
        self.risks = make_list(self.risks)  # list of risks to calculate
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
    def cash_payments(self):
        return self._cash_payments

    @cash_payments.setter
    def cash_payments(self, cash_payments):
        self._cash_payments = cash_payments

    @property
    def transaction_costs(self):
        return self._transaction_costs

    @property
    def hedges(self):
        return self._hedges

    @hedges.setter
    def hedges(self, hedges):
        self._hedges = hedges

    @property
    def results(self):
        return self._results

    def set_results(self, date, results):
        self._results[date] = results

    def add_results(self, date, results, replace=False):
        if date in self._results and len(self._results[date]) and not replace:
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
    def result_summary(self):
        """
        Get a dataframe showing the PV and other risks and cash on each day in the backtest
        :param show_units: choose to show the units in the column names
        :type show_units: bool default False
        :return: bool default False
        :rtype: pandas.dataframe
        """
        dates_with_results = list(filter(lambda x: len(x[1]), self._results.items()))
        summary = pd.DataFrame({date: {risk: results[risk].aggregate(True, True)
                                       for risk in results.risk_measures} for date, results in dates_with_results}).T
        cash_summary = defaultdict(dict)
        for date, results in self._cash_dict.items():
            for ccy, value in results.items():
                cash_summary[f'Cumulative Cash {ccy}'][date] = value
        if len(cash_summary) > 1:
            raise RuntimeError('Cannot aggregate cash in multiple currencies')
        cash = pd.concat([pd.Series(cash_dict, name='Cumulative Cash')
                          for name, cash_dict in cash_summary.items()], axis=1, sort=True)
        transaction_costs = pd.Series(self.transaction_costs, name='Transaction Costs')
        df = pd.concat([summary, cash, transaction_costs], axis=1, sort=True).fillna(0)
        df['Total'] = df.sum(numeric_only=True, axis=1)
        return df[:self.states[-1]]

    def trade_ledger(self):
        # this is a ledger of each instrument when it was entered and when it was closed out.  The cash associated
        # with the entry and exit are used in the open value and close value and PnL calc.  If the PnL is None it
        # means the instrument is still live and therefore will show up in the PV
        ledger = {}
        names = []
        for date in sorted(self.cash_payments.keys()):
            cash_list = self.cash_payments[date]
            for cash in cash_list:
                if cash.direction == 0:
                    ledger[cash.trade.name] = {'Open': date,
                                               'Close': date,
                                               'Open Value': 0,
                                               'Close Value': 0,
                                               'Long Short': cash.direction,
                                               'Status': 'closed',
                                               'Trade PnL': 0}
                elif cash.trade.name in names:
                    if len(cash.cash_paid) > 0:
                        ledger[cash.trade.name]['Close'] = date
                        ledger[cash.trade.name]['Close Value'] += sum(cash.cash_paid.values())
                        open_value = ledger[cash.trade.name]['Open Value']
                        ledger[cash.trade.name]['Trade PnL'] = ledger[cash.trade.name]['Close Value'] + open_value
                        ledger[cash.trade.name]['Status'] = 'closed'
                else:
                    names.append(cash.trade.name)
                    ledger[cash.trade.name] = {'Open': date,
                                               'Close': None,
                                               'Open Value': sum(cash.cash_paid.values()),
                                               'Close Value': 0,
                                               'Long Short': cash.direction,
                                               'Status': 'open',
                                               'Trade PnL': None}
        return pd.DataFrame(ledger).T.sort_index()

    def strategy_as_time_series(self):
        """
        Get a dataframe indexed by strategy dates and instruments present on the respective dates
        For each tradable, displays calculated risk measures, cash payment amount and ccy (if any) and static data.
        """
        # Construct a table of cash payments for each date and concat them in a single table of all cash payments
        cp_table = pd.concat(
            [pd.concat([cp.to_frame() for cp in date_payments])
             for _, date_payments in self.cash_payments.items()]
        )
        cp_table = cp_table.set_index(['Pricing Date', 'Instrument Name']).sort_index()
        cp_table.columns = pd.MultiIndex.from_product([['Cash Payments'], cp_table.columns])

        risk_measure_dict = {date: risk_res
                             .to_frame(values='value', index='instrument_name', columns='risk_measure')
                             .assign(pricing_date=[date] * len(risk_res))
                             for date, risk_res in self.results.items()}
        risk_measure_table = pd.concat(risk_measure_dict.values())
        risk_measure_table = risk_measure_table.reset_index()
        risk_measure_table = risk_measure_table.rename(columns={'pricing_date': 'Pricing Date',
                                                       'instrument_name': 'Instrument Name'})
        risk_measure_table = risk_measure_table.set_index(['Pricing Date', 'Instrument Name'])
        risk_measure_table.columns = pd.MultiIndex.from_product(
            [['Risk Measures'], [str(col) for col in risk_measure_table.columns]])

        risk_and_cp_joined = risk_measure_table.join(cp_table, how='outer')

        static_inst_info = pd.concat(
            [info.portfolio.to_frame()
             for info in self.results.values()]
        )
        static_inst_info = static_inst_info.rename(columns={'name': 'Instrument Name'})
        static_inst_info = static_inst_info.set_index(['Instrument Name'])
        static_inst_info = static_inst_info[~static_inst_info.index.duplicated(keep='first')]
        static_inst_info.columns = pd.MultiIndex.from_product([['Static Instrument Data'], static_inst_info.columns])

        result = static_inst_info.join(risk_and_cp_joined, how='outer')

        return result.sort_index()


class ScalingPortfolio:
    def __init__(self, trade, dates, risk, csa_term=None, scaling_parameter='notional_amount',
                 risk_transformation: Transformer = None):
        self.trade = trade
        self.dates = dates
        self.risk = risk
        self.csa_term = csa_term
        self.scaling_parameter = scaling_parameter
        self.risk_transformation = risk_transformation
        self.results = None


class CashPayment:
    def __init__(self, trade, effective_date=None, scale_date=None, direction=1, scaling_parameter='notional_amount'):
        self.trade = trade
        self.effective_date = effective_date
        self.scale_date = scale_date
        self.direction = direction
        self.cash_paid = defaultdict(float)
        self.scaling_parameter = scaling_parameter

    def to_frame(self):
        df = pd.DataFrame(self.cash_paid.items(), columns=['Cash Ccy', 'Cash Amount'])
        df['Instrument Name'] = self.trade.name
        df['Pricing Date'] = self.effective_date
        return df


class Hedge:
    def __init__(self,
                 scaling_portfolio: ScalingPortfolio,
                 entry_payment: CashPayment,
                 exit_payment: Optional[CashPayment]):
        self.scaling_portfolio = scaling_portfolio
        self.entry_payment = entry_payment
        self.exit_payment = exit_payment


@dataclass_json()
@dataclass
class TransactionModel:
    def get_cost(self, state, backtest, info) -> float:
        pass


@dataclass_json()
@dataclass
class ConstantTransactionModel(TransactionModel):
    cost: float = 0

    def get_cost(self, state, backtest, info) -> float:
        return self.cost


@dataclass_json
@dataclass
class PredefinedAssetBacktest(BaseBacktest):
    data_handler: DataHandler
    initial_value: float

    def __post_init__(self):
        self.performance = pd.Series(dtype=float)
        self.cash_asset = Cash('USD')
        self.holdings = defaultdict(float)
        self.historical_holdings = pd.Series(dtype=float)
        self.historical_weights = pd.Series(dtype=float)
        self.orders = []
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
                open_order, close_order = (long, short) if long.execution_end_time() < short.execution_end_time() \
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
                trade_df.append((inst, start_dt, end_dt, open_value, end_value, status,
                                 (end_value - open_value) * long_or_short if status == 'closed' else None))
        return pd.DataFrame(trade_df, columns=['Instrument', 'Open', 'Close', 'Open Value', 'Close Value',
                                               'Status', 'Trade PnL'])

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

    def get_costs(self) -> pd.Series(dtype=float):
        costs = defaultdict(float)
        for order in self.orders:
            if isinstance(order, OrderCost):
                costs[order.execution_end_time().date()] += order.execution_quantity(self.data_handler)

        return pd.Series(costs)

    def get_orders_for_date(self, date: dt.date) -> pd.DataFrame():
        return pd.DataFrame([order.to_dict(self.data_handler) for order in self.orders
                             if order.execution_end_time().date() == date])
