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
from gs_quant.datetime import prev_business_date
from gs_quant.backtests.core import ValuationMethod
from gs_quant.backtests.order import OrderBase
from gs_quant.backtests.event import FillEvent
from gs_quant.backtests.data_handler import DataHandler
from gs_quant.data import DataFrequency
import numpy as np
import datetime as dt


class BackTest(object):
    def __init__(self, strategy, states, risks):
        self._portfolio_dict = defaultdict(Portfolio)  # portfolio by state
        self._scaling_portfolios = defaultdict(list)  # list of ScalingPortfolio
        self._strategy = deepcopy(strategy)  # the strategy definition
        self._states = states  # list of states
        self._results = defaultdict()
        self._risks = tuple(risks)  # list of risks to calculate
        self._calc_calls = 0
        self._calculations = 0

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
    def states(self):
        return self._states

    @property
    def results(self):
        return self._results

    @property
    def risks(self):
        return self._risks

    def add_results(self, date, results):
        if date in self._results:
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
        return pd.DataFrame({date: {risk: results[risk].aggregate() for risk in results.risk_measures}
                             for date, results in self._results.items()}).T


class ScalingPortfolio(object):
    def __init__(self, trade, dates, risk):
        self.trade = trade
        self.dates = dates
        self.risk = risk
        self.results = None


class PriceBacktest(object):
    def __init__(self, data_handler: DataHandler):
        self.data_handler = data_handler
        self.performance = pd.Series()
        self.cash_asset = Cash('USD')
        self.holdings = {}
        self.holdings_projected = {}
        self.orders = []

    def set_start_date(self, start: dt.date):
        self.performance[prev_business_date(start)] = 100
        self.holdings[self.cash_asset] = 100
        self.holdings_projected[self.cash_asset] = 100

    def record_orders(self, orders: Iterable[OrderBase]):
        for order in orders:
            # projected holdings (i.e. the order may not started yet)
            inst = order.instrument
            if inst not in self.holdings_projected:
                self.holdings_projected[inst] = 0
            self.holdings_projected[inst] += order.quantity

        self.orders.extend(orders)

    def update_fill(self, fill: FillEvent):
        inst = fill.order.instrument
        self.holdings[self.cash_asset] -= fill.filled_price * fill.filled_units
        if inst not in self.holdings:
            self.holdings[inst] = 0
        self.holdings[inst] += fill.filled_units

        # update projected holdings as well
        if inst not in self.holdings_projected:
            self.holdings_projected[inst] = 0
        self.holdings_projected[inst] -= fill.order.quantity
        self.holdings_projected[inst] += fill.filled_units

    def units_held(self, projected: bool = False):
        holdings = self.holdings_projected if projected else self.holdings
        return holdings

    def mark_to_market(self, state: dt.datetime, valuation_method: ValuationMethod):
        mtm = 0
        for instrument, units in self.holdings.items():
            if abs(units) > 1e-12:
                if isinstance(instrument, Cash):
                    fixing = 1
                else:
                    tag, window = valuation_method.data_tag, valuation_method.window
                    if window:
                        fixings = self.data_handler.get_data_range(window.start, window.end, instrument,
                                                                   DataFrequency.REAL_TIME, tag)
                        fixing = np.mean(fixings) if len(fixings) else np.nan
                    else:  # no time window specified, use daily fixing
                        fixing = self.data_handler.get_data(state.date(), instrument, DataFrequency.DAILY, tag)
                mtm += fixing * units
        self.performance[state.date()] = mtm
        print(state, mtm)

    def get_level(self, date: dt.date):
        return self.performance[date]
