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
