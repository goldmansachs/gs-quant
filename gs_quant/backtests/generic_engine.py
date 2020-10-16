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
from typing import Optional

from gs_quant.backtests.backtest_utils import make_list, CalcType
from gs_quant.instrument import Instrument
from gs_quant.markets.portfolio import Portfolio
from gs_quant.markets import PricingContext, HistoricalPricingContext
from gs_quant.risk import RiskMeasure, Price
from gs_quant.errors import MqValueError


class BackTest(object):
    def __init__(self, strategy, states, risks):
        self._portfolio_dict = defaultdict(Portfolio)
        self._scaling_portfolios = defaultdict(list)  # list of ScalingPortfolio
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

    def get_aggregated_result(self, risk: Optional[RiskMeasure] = Price):
        if risk not in self.risks:
            raise MqValueError('{} not in calculated risks for this backtest'.format(risk))
        return pd.Series({d: i[risk].aggregate() for d, i in self._results.items()})


class ScalingPortfolio(object):
    def __init__(self, trade, dates, risk):
        self.trade = trade
        self.dates = dates
        self.risk = risk
        self.results = None


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
            if trigger.calc_type != CalcType.path_dependent:
                triggered_dates = [date for date in dates if trigger.has_triggered(date, backtest)]
                for action in trigger.actions:
                    if action.calc_type != CalcType.path_dependent:
                        action.apply_action(triggered_dates, backtest)

        with PricingContext(is_batch=True, show_progress=show_progress):
            for day, portfolio in backtest.portfolio_dict.items():
                with PricingContext(day):
                    backtest.calc_calls += 1
                    backtest.calculations += len(portfolio) * len(risks)
                    backtest.add_results(day, portfolio.calc(tuple(risks)))

            # semi path dependent initial calc
            for _, scaling_list in backtest.scaling_portfolios.items():
                for p in scaling_list:
                    with HistoricalPricingContext(dates=p.dates):
                        backtest.calc_calls += 1
                        backtest.calculations += len(p.dates) * len(risks)
                        p.results = Portfolio([p.trade]).calc(tuple(risks))

        for date in dates:
            # semi path dependent scaling
            if date in backtest.scaling_portfolios:
                for p in backtest.scaling_portfolios[date]:
                    scale_date = p.dates[0]
                    scaling_factor = backtest.results[scale_date][p.risk][0] / p.results[scale_date][p.risk][0]
                    scaled_trade = p.trade.as_dict()
                    scaled_trade['notional_amount'] *= scaling_factor
                    scaled_trade = Instrument.from_dict(scaled_trade)
                    for day in p.dates:
                        backtest.add_results(day, p.results[day] * scaling_factor)
                        backtest.portfolio_dict[day] += Portfolio(scaled_trade)

            # path dependent
            for trigger in strategy.triggers:
                if trigger.calc_type == CalcType.path_dependent:
                    if trigger.has_triggered(date, backtest):
                        for action in trigger.actions:
                            action.apply_action(date, backtest)
                else:
                    for action in trigger.actions:
                        if action.calc_type == CalcType.path_dependent:
                            if trigger.has_triggered(date, backtest):
                                action.apply_action(date, backtest)
            return backtest
