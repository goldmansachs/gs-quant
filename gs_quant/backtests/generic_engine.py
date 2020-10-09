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

from copy import deepcopy
from collections import defaultdict
import pandas as pd

from gs_quant.backtests.backtest_utils import make_list
from gs_quant.markets.portfolio import Portfolio
from gs_quant.markets import PricingContext
from gs_quant.risk import RiskMeasure, Price
from gs_quant.errors import MqValueError
from typing import Optional


class BackTest(object):
    def __init__(self, strategy, states, risks):
        self._portfolio_dict = defaultdict(Portfolio)
        self._strategy = deepcopy(strategy)
        self._states = states
        self._results = defaultdict()
        self._risks = tuple(risks)
        self._calc_calls = 0
        self._calculations = 0

    @property
    def portfolio_dict(self):
        return self._portfolio_dict

    @portfolio_dict.setter
    def portfolio_dict(self, portfolio_dict):
        self._portfolio_dict = portfolio_dict

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
        # TODO this may not work with portfolio risk results
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

    def get_aggregated_result(self, risk: Optional[RiskMeasure] = Price):
        if risk not in self.risks:
            raise MqValueError('{} not in calculated risks for this backtest'.format(risk))
        return pd.Series({d: i[risk].aggregate() for d, i in self._results.items()})


class GenericEngine(object):

    @classmethod
    def supports_strategy(cls, strategy):
        return True

    @classmethod
    def run_backtest(cls, strategy, start=None, end=None, frequency='BM', window=None, states=None, risks=Price,
                     show_progress=True):
        dates = pd.date_range(start=start, end=end, freq=frequency).date.tolist()
        risks = make_list(risks) + strategy.risks

        backtest = BackTest(strategy, dates, risks)

        for trigger in strategy.triggers:
            if trigger.deterministic:
                triggered_dates = [date for date in dates if trigger.has_triggered(date, backtest)]
                for action in trigger.actions:
                    if action.deterministic:
                        action.apply_action(triggered_dates, backtest)

        with PricingContext(is_batch=True, show_progress=show_progress):
            for day, portfolio in backtest.portfolio_dict.items():
                with PricingContext(day):
                    backtest.calc_calls += 1
                    backtest.calculations += len(portfolio) * len(risks)
                    backtest.add_results(day, portfolio.calc(risks[0] if len(risks) == 1 else tuple(risks)))

        for trigger in strategy.triggers:
            if not trigger.deterministic:
                for date in dates:
                    if trigger.has_triggered(date, backtest):
                        for action in trigger.actions:
                            action.apply_action(date, backtest)
            else:
                for action in trigger.actions:
                    if not action.deterministic:
                        for date in dates:
                            if trigger.has_triggered(date, backtest):
                                action.apply_action(date, backtest)
        return backtest
