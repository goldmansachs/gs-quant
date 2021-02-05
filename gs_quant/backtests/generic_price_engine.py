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


from gs_quant.backtests.event import *
from gs_quant.datetime import date_range, prev_business_date
from typing import Iterable
from collections import deque
import pytz
import time
import pandas as pd
import datetime as dt


class ExecutionEngine(object):
    pass


class PriceBacktest(object):
    def __init__(self, data_sources):
        self.data_sources = data_sources
        self.performance = pd.Series()
        self.holdings = {}
        self.holdings_projected = {}
        self.cash = 100
        self.trades = []

    def set_start_date(self, start: dt.date):
        self.performance[prev_business_date(start)] = 100

    def record_orders(self, orders: Iterable[OrderEvent]):
        for order in orders:
            # projected holdings (i.e. the order may not started yet)
            inst = order.instrument
            if inst not in self.holdings_projected:
                self.holdings_projected[inst] = 0
            self.holdings_projected[inst] += order.units

    def update_fill(self, fill: FillEvent):
        inst = fill.instrument
        self.cash -= fill.filled_price * fill.filled_units
        if inst not in self.holdings:
            self.holdings[inst] = 0
        self.holdings[inst] += fill.filled_units

        # update projected holdings as well
        if inst not in self.holdings_projected:
            self.holdings_projected[inst] = 0
        self.holdings_projected[inst] -= fill.requested_units
        self.holdings_projected[inst] += fill.filled_units

    def units_held(self, projected: bool = False):
        holdings = self.holdings_projected if projected else self.holdings
        return holdings

    def mark_to_market(self, date: dt.date):
        mtm = self.cash
        for instrument, units in self.holdings.items():
            if abs(units) > 1e-12:
                fixing = self.data_sources[instrument + ' Daily'].gs_data(date)
                mtm += fixing * units
        self.performance[date] = mtm

    def get_level(self, date: dt.date):
        return self.performance[date]


class GenericPriceEngine(object):

    @classmethod
    def supports_strategy(cls, strategy):
        return False

    def __init__(self, data_sources, eod_valuation_time: dt.datetime = dt.time(23, 0, 0)):
        self.eod_valuation_time = eod_valuation_time
        self.data_sources = data_sources
        self.execution_engine = None

    def _timer(self, strategy, start, end):
        dates = date_range(start, end)
        times = strategy.triggers[0].get_trigger_times()
        times.append(self.eod_valuation_time)

        for d in dates:
            for t in times:
                yield dt.datetime.combine(d, t)

    def _timer_live(self, strategy):
        date = dt.date.today()
        timer = self._timer(strategy, date, date)
        for t in timer:
            while t >= dt.datetime.now(pytz.timezone('US/Eastern')):
                time.sleep(60)
            yield t

    def run_live(self, strategy):
        # initialize backtest object
        backtest = PriceBacktest(self.data_sources)
        backtest.set_start_date(dt.date.today())

        # initialize execution engine
        self.execution_engine = ExecutionEngine()

        # create timer
        timer = self._timer_live(strategy)
        self._run(strategy, timer, backtest)

    def run_backtest(self, strategy, start, end):
        # initialize backtest object
        backtest = PriceBacktest(self.data_sources)
        backtest.set_start_date(start)

        # initialize execution engine
        self.execution_engine = SimulatedExecutionEngine(self.data_sources)

        # create timer
        timer = self._timer(strategy, start, end)
        self._run(strategy, timer, backtest)
        return backtest

    def _run(self, strategy, timer, backtest: PriceBacktest):
        events = deque()

        while True:
            try:
                state = next(timer)
            except StopIteration:
                break

            # update to latest data
            for ds in backtest.data_sources.values():
                ds.update(state)

            # see if any submitted orders have been executed
            fills = self.execution_engine.ping(state)
            events.extend(fills)

            # generate a market event
            events.append(MarketEvent())

            # create valuation event when it's due for daily valuation
            if state.time() == self.eod_valuation_time:
                events.append(ValuationEvent())

            while events:
                event = events.popleft()

                if event.type == 'Market':  # market event (new mkt data coming in)
                    for trigger in strategy.triggers:
                        if trigger.has_triggered(state, backtest):
                            for action in trigger.actions:
                                orders = action.apply_action(state, backtest)
                                backtest.record_orders(orders)
                                events.extend(orders)
                elif event.type == 'Order':  # order event (submit the order to execution engine)
                    self.execution_engine.submit_order(event)
                elif event.type == 'Fill':  # fill event (update backtest with the fill results)
                    backtest.update_fill(event)
                elif event.type == 'Valuation':  # valuation event (calculate daily level)
                    backtest.mark_to_market(state.date())

        return backtest


class SimulatedExecutionEngine(ExecutionEngine):
    def __init__(self, data_sources, slippage=0, absolute_slippage=True):
        self.data_sources = data_sources
        self.slippage = slippage
        self.absolute_slippage = absolute_slippage
        self.orders = []

    def submit_order(self, order: OrderEvent):
        self.orders.append(order)

    def _calculate_fill(self, order: OrderEvent):
        times = order.execution_time if order.execution_window is None else [
            order.execution_time + dt.timedelta(minutes=i * 5) for i in range(1, int(order.execution_window / 5) + 1)]
        price = self.data_sources[order.instrument + ' Intraday'].get_data(times)
        slip = self.slippage if self.absolute_slippage else price * self.slippage
        fill = price + slip if order.units > 0 else price - slip
        fill = FillEvent(order.instrument, order.units, order.units, fill)
        return fill

    def ping(self, state: dt.datetime):
        fill_events = []
        while self.orders:
            order: OrderEvent = self.orders[0]
            end_time = order.execution_time + dt.timedelta(minutes=order.execution_window)
            if end_time > state:
                break
            else:
                fill = self._calculate_fill(order)
                fill_events.append(fill)
                self.orders.pop(0)
        return fill_events


class ExecutionEngine(object):
    pass
