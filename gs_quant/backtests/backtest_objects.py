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
from gs_quant.backtests.order import OrderBase
from gs_quant.backtests.event import FillEvent
from gs_quant.backtests.data_handler import DataHandler
import numpy as np
import datetime as dt


class BackTest(object):
    def __init__(self, strategy, states, risks):
        self._portfolio_dict = defaultdict(Portfolio)  # portfolio by state
        self._cash_dict = defaultdict(float)  # cash by state
        self._scaling_portfolios = defaultdict(list)  # list of ScalingPortfolio
        self._strategy = deepcopy(strategy)  # the strategy definition
        self._states = states  # list of states
        self._results = defaultdict()
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
    def result_summary(self, allow_mismatch_risk_keys=True):
        summary = pd.DataFrame({date: {risk: results[risk].aggregate(allow_mismatch_risk_keys)
                                       for risk in results.risk_measures} for date, results in self._results.items()}).T
        summary['Cash'] = pd.Series(self._cash_dict)
        return summary.fillna(0)


class ScalingPortfolio(object):
    def __init__(self, trade, dates, risk, csa_term=None, unwind=False):
        self.trade = trade
        self.dates = dates
        self.risk = risk
        self.csa_term = csa_term
        self.results = None
        self.unwind = unwind


class PredefinedAssetBacktest(object):
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
    def __init__(self, data_handler: DataHandler):
        self.data_handler = data_handler
        self.performance = pd.Series()
        self.cash_asset = Cash('USD')
        self.holdings = {}
        self.historical_holdings = pd.Series()
        self.orders = []
        self.initial_value = 100
        self.results = {}

    def set_start_date(self, start: dt.date):
        self.performance[start] = self.initial_value
        self.holdings[self.cash_asset] = self.initial_value

    def record_orders(self, orders: Iterable[OrderBase]):
        self.orders.extend(orders)

    def update_fill(self, fill: FillEvent):
        inst = fill.order.instrument
        self.holdings[self.cash_asset] -= fill.filled_price * fill.filled_units
        if inst not in self.holdings:
            self.holdings[inst] = 0
        self.holdings[inst] += fill.filled_units

    def mark_to_market(self, state: dt.datetime, valuation_method: ValuationMethod):
        mtm = 0
        for instrument, units in self.holdings.items():
            if abs(units) > 1e-12:
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
                mtm += fixing * units
        self.performance[state.date()] = mtm
        self.historical_holdings[state.date()] = self.holdings

    def get_level(self, date: dt.date):
        return self.performance[date]
