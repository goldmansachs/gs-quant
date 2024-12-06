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
from abc import ABC
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from queue import Queue as FifoQueue
from typing import Iterable, TypeVar, Optional, Union

import datetime as dt
import numpy as np
import pandas as pd

from gs_quant.backtests.backtest_utils import make_list
from gs_quant.backtests.core import ValuationMethod
from gs_quant.backtests.data_handler import DataHandler
from gs_quant.backtests.data_sources import DataSource, GenericDataSource, MissingDataStrategy
from gs_quant.backtests.event import FillEvent
from gs_quant.backtests.order import OrderBase, OrderCost
from gs_quant.base import static_field
from gs_quant.common import RiskMeasure
from gs_quant.datetime.relative_date import RelativeDate
from gs_quant.instrument import Cash, IRSwap
from gs_quant.json_convertors import dc_decode
from gs_quant.markets import PricingContext
from gs_quant.markets.portfolio import Portfolio
from gs_quant.risk import ErrorValue, Cashflows
from gs_quant.risk.transform import Transformer


class BaseBacktest(ABC):
    pass


TBaseBacktest = TypeVar('TBaseBacktest', bound='BaseBacktest')


@dataclass_json()
@dataclass
class PnlAttribute:
    attribute_name: str
    attribute_metric: RiskMeasure
    market_data_metric: RiskMeasure
    scaling_factor: float
    second_order: bool = False

    def get_risks(self):
        return [self.attribute_metric, self.market_data_metric]


@dataclass_json()
@dataclass
class PnlDefinition:
    attributes: Iterable[PnlAttribute]

    def get_risks(self):
        return [risk for attribute in self.attributes for risk in attribute.get_risks()]


@dataclass_json
@dataclass
class BackTest(BaseBacktest):
    strategy: object
    states: Iterable
    risks: Iterable[RiskMeasure]
    price_measure: RiskMeasure
    holiday_calendar: Iterable[dt.date] = None
    pnl_explain_def: Optional[PnlDefinition] = None

    def __post_init__(self):
        self._portfolio_dict = defaultdict(Portfolio)  # portfolio by state
        self._cash_dict = {}  # cash by state
        self._hedges = defaultdict(list)  # list of Hedge by date
        self._cash_payments = defaultdict(list)  # list of cash payments (entry, unwind)
        self._transaction_costs = defaultdict(int)  # list of transaction costs by date
        self.strategy = deepcopy(self.strategy)  # the strategy definition
        self._results = defaultdict(list)
        self._trade_exit_risk_results = defaultdict(list)
        self.risks = make_list(self.risks)  # list of risks to calculate
        self._risk_summary_dict = None  # Summary dict shared between output views, only initialized once
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
    def trade_exit_risk_results(self):
        return self._trade_exit_risk_results

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

    def get_risk_summary_dict(self, zero_on_empty_dates=False):
        if self._risk_summary_dict is not None:
            summary_dict = self._risk_summary_dict
        else:
            if not self._results:
                raise ValueError('Must run generic engine and populate results before results summary dict')
            dates_with_results = list(filter(lambda x: len(x[1]), self._results.items()))
            summary_dict = defaultdict(dict)
            for date, results in dates_with_results:
                for risk in results.risk_measures:
                    try:
                        value = results[risk].aggregate(True, True)
                    except TypeError:
                        value = ErrorValue(None, error='Could not aggregate risk results')
                    summary_dict[date][risk] = value
            self._risk_summary_dict = summary_dict
        zero_risk_sd_copy = summary_dict.copy()
        if zero_on_empty_dates:
            for cash_only_date in set(self._cash_dict.keys()).difference(zero_risk_sd_copy.keys()):
                for risk in self.risks:
                    zero_risk_sd_copy[cash_only_date][risk] = 0
        return zero_risk_sd_copy

    @property
    def result_summary(self):
        """
        Get a dataframe showing the PV and other risks and cash on each day in the backtest
        """
        summary_dict = self.get_risk_summary_dict()
        summary = pd.DataFrame(summary_dict).T
        cash_summary = defaultdict(dict)
        for date, results in self._cash_dict.items():
            for ccy, value in results.items():
                cash_summary[f'Cumulative Cash {ccy}'][date] = value
        if len(cash_summary) > 1:
            raise RuntimeError('Cannot aggregate cash in multiple currencies')
        cash = pd.concat([pd.Series(cash_dict, name='Cumulative Cash')
                          for name, cash_dict in cash_summary.items()], axis=1, sort=True)
        transaction_costs = pd.Series(self.transaction_costs, name='Transaction Costs')
        df = pd.concat([summary, cash, transaction_costs], axis=1, sort=True).ffill().fillna(0)
        # cum sum the transaction_costs
        df['Transaction Costs'] = df['Transaction Costs'].cumsum()
        df['Total'] = df[self.price_measure] + df['Cumulative Cash'] + df['Transaction Costs']
        return df[:self.states[-1]]

    @property
    def risk_summary(self):
        """
        Get a dataframe showing the risks in the backtest with zero values for days with no instruments held
        """
        summary_dict = self.get_risk_summary_dict(zero_on_empty_dates=True)
        return pd.DataFrame(summary_dict).T.sort_index()

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

    def pnl_explain(self):
        """
        Get a dictionary of risk attributions which explain the pnl
        """
        if self.pnl_explain_def is None:
            return None

        risk_results = self.results
        exit_risk_results = self.trade_exit_risk_results
        dates = sorted(set(risk_results.keys()).union(exit_risk_results.keys()))

        pnl_explain_results = {}

        for attribute in self.pnl_explain_def.attributes:
            result = {}
            cum_total = 0.0
            for idx in range(1, len(dates)):
                metric_pnl = 0.0
                cur_date = dates[idx]
                prev_date = dates[idx - 1]
                if prev_date not in risk_results:
                    result[cur_date] = cum_total
                    continue
                for prev_date_inst in risk_results[prev_date].portfolio.all_instruments:
                    prev_date_risk = risk_results[prev_date][prev_date_inst][attribute.attribute_metric]
                    if prev_date_risk == 0:
                        continue
                    prev_date_mkt_data = risk_results[prev_date][prev_date_inst][attribute.market_data_metric]
                    if cur_date in risk_results and prev_date_inst in risk_results[cur_date].portfolio:
                        cur_date_mkt_data = risk_results[cur_date][prev_date_inst][attribute.market_data_metric]
                    else:
                        cur_date_mkt_data = exit_risk_results[cur_date][prev_date_inst][attribute.market_data_metric]
                    if attribute.second_order:
                        metric_pnl += (0.5 * attribute.scaling_factor * prev_date_risk *
                                       (cur_date_mkt_data - prev_date_mkt_data) *
                                       (cur_date_mkt_data - prev_date_mkt_data))
                    else:
                        metric_pnl += (attribute.scaling_factor * prev_date_risk *
                                       (cur_date_mkt_data - prev_date_mkt_data))
                cum_total += metric_pnl
                result[cur_date] = cum_total
            pnl_explain_results[attribute.attribute_name] = result
        return pnl_explain_results


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
    def get_cost(self, state, backtest, info, instrument) -> float:
        pass


@dataclass_json()
@dataclass
class ConstantTransactionModel(TransactionModel):
    cost: Union[float, int] = 0
    class_type: str = static_field('constant_transaction_model')

    def get_cost(self, state, backtest, info, instrument) -> float:
        return self.cost


@dataclass_json
@dataclass
class ScaledTransactionModel:
    scaling_type: Union[str, RiskMeasure] = 'notional_amount'
    scaling_level: Union[float, int] = 0.0001
    class_type: str = static_field('scaled_transaction_model')

    def get_cost(self, state, backtest, info, instrument) -> float:
        if isinstance(self.scaling_type, str):
            try:
                return getattr(instrument, self.scaling_type) * self.scaling_level
            except AttributeError:
                raise RuntimeError(f'{self.scaling_type} not recognised for instrument {instrument.type}')

        with PricingContext(state):
            risk = instrument.calc(self.scaling_type)
            backtest.calc_calls += 1
            backtest.calculations += 1
        return risk.result() * self.scaling_level


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


@dataclass_json
@dataclass
class CashAccrualModel:
    class_type: str = static_field('cash_accrual_model')

    def get_accrued_value(self, current_value, to_state) -> dict:
        pass


@dataclass_json
@dataclass
class ConstantCashAccrualModel(CashAccrualModel):
    rate: float = 0
    annual: bool = True
    class_type: str = static_field('cash_accrual_model')

    def get_accrued_value(self, current_value, to_state) -> dict:
        new_value = {}
        from_state = current_value[1]
        days = (to_state - from_state).days
        for currency, value in current_value[0].items():
            new_value[currency] = value * (1 + (self.rate / (365 if self.annual else 1))) ** days

        return new_value


@dataclass_json
@dataclass
class DataCashAccrualModel(CashAccrualModel):
    data_source: DataSource = field(default=None, metadata=config(decoder=dc_decode(*DataSource.sub_classes(),
                                                                                    allow_missing=True)))
    annual: bool = True
    class_type: str = static_field('cash_accrual_model')

    def get_accrued_value(self, current_value, to_state) -> dict:
        new_value = {}
        from_state = current_value[1]
        days = (to_state - from_state).days
        rate = self.data_source.get_data(from_state)
        for currency, value in current_value[0].items():
            new_value[currency] = value * (1 + (rate / (365 if self.annual else 1))) ** days
        return new_value


ois_fixings = {}


@dataclass_json
@dataclass
class OisFixingCashAccrualModel(CashAccrualModel):
    start_date: Union[dt.date, str] = '-1y'
    end_date: Union[dt.date, str] = dt.date.today()
    class_type: str = static_field('ois_fixing_cash_accrual_model')

    def get_accrued_value(self, current_value, to_state) -> dict:
        for currency in current_value[0].keys():
            if currency not in ois_fixings:
                start_date = self.start_date if isinstance(self.start_date, dt.date) else RelativeDate(
                    self.start_date).apply_rule()
                start_date = (start_date - dt.timedelta(days=7))
                swap = IRSwap(notional_currency=currency,
                              floating_rate_frequency='1b',
                              effective_date=start_date,
                              termination_date=self.end_date if isinstance(self.end_date, dt.date) else RelativeDate(
                                  self.end_date).apply_rule(),
                              floating_rate_option='OIS')
                with PricingContext():
                    result = swap.calc(Cashflows)

                ois_fixings[currency] = GenericDataSource(
                    result.result()[result.result()['payment_type'] == 'Flt'].set_index(['accrual_start_date'])['rate'],
                    MissingDataStrategy.fill_forward)
            ds_accrual_model = DataCashAccrualModel(ois_fixings[currency], True)
            return ds_accrual_model.get_accrued_value(current_value, to_state)
