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

from gs_quant.backtests.backtest_utils import *
from gs_quant.base import Priceable
from gs_quant.datetime.date import *
from gs_quant.markets.securities import *
from gs_quant.target.backtests import BacktestTradingQuantityType
from collections import namedtuple

action_count = 1


class Action(object):
    def __init__(self, name: str = None):
        self._needs_scaling = False
        self._calc_type = CalcType.simple
        self._risk = None
        global action_count
        if name is None:
            self._name = 'Action{}'.format(action_count)
            action_count += 1
        else:
            self._name = name

    @property
    def calc_type(self):
        return self._calc_type

    @property
    def risk(self):
        return self._risk


class AddTradeAction(Action):
    def __init__(self,
                 priceables: Union[Priceable, Iterable[Priceable]],
                 trade_duration: Union[str, dt.date, dt.timedelta] = None,
                 name: str = None):
        """
        create an action which adds a trade when triggered.  The trades are resolved on the trigger date (state) and
        last until the trade_duration if specified or for all future dates if not.
        :param priceables: a priceable or a list of pricables.
        :param trade_duration: an instrument attribute eg. 'expiration_date' or a date or a tenor or timedelta
                               if left as None the
                               trade will be added for all future dates
        :param name: optional additional name to the priceable name
        """
        super().__init__(name)
        self._priceables = make_list(priceables)
        self._dated_priceables = {}
        self._trade_duration = trade_duration
        for i, p in enumerate(self._priceables):
            if p.name is None:
                p.name = '{}_Priceable{}'.format(self._name, i)
            else:
                p.name = '{}_{}'.format(self._name, p.name)

    @property
    def priceables(self):
        return self._priceables

    @property
    def trade_duration(self):
        return self._trade_duration

    def set_dated_priceables(self, state, priceables):
        self._dated_priceables[state] = make_list(priceables)

    @property
    def dated_priceables(self):
        return self._dated_priceables


AddTradeActionInfo = namedtuple('AddTradeActionInfo', 'scaling')
HedgeActionInfo = namedtuple('HedgeActionInfo', 'not_applicable')


class EnterPositionQuantityScaledAction(Action):
    def __init__(self, priceables: Union[Priceable, Iterable[Priceable]], trade_duration: str = None, name: str = None,
                 trade_quantity: float = 1,
                 trade_quantity_type: Union[BacktestTradingQuantityType, str] = BacktestTradingQuantityType.quantity):
        """
        create an action which enters trades when triggered.  The trades are executed with specified quantity and
        last until the trade_duration if specified, or for all future dates if not.
        :param priceables: a priceable or a list of pricables.
        :param trade_duration: an instrument attribute eg. 'expiration_date' or a date or a tenor if left as None the
                               trade will be added for all future dates
        :param name: optional additional name to the priceable name
        :param trade_quantity: the amount, in units of trade_quantity_type to be traded
        :param trade_quantity_type: the quantity type used to scale trade. eg. quantity for units, notional for
                                    underlier notional
        """
        super().__init__(name)
        self._priceables = make_list(priceables)
        self._trade_duration = trade_duration
        for i, p in enumerate(self._priceables):
            if p.name is None:
                p.name = '{}_Priceable{}'.format(self._name, i)
            else:
                p.name = '{}_{}'.format(self._name, p.name)
        self._trade_quantity = trade_quantity
        self._trade_quantity_type = trade_quantity_type

    @property
    def priceables(self):
        return self._priceables

    @property
    def trade_duration(self):
        return self._trade_duration

    @property
    def trade_quantity(self):
        return self._trade_quantity

    @property
    def trade_quantity_type(self):
        return self._trade_quantity_type


class ExitPositionAction(Action):
    def __init__(self, name: str = None):
        """
        Fully exit all held positions
        :param name: optional name of the action
        """
        super().__init__(name)


class HedgeAction(Action):
    def __init__(self, risk, priceables: Priceable = None, trade_duration: str = None, name: str = None,
                 csa_term: str = None, scaling_parameter: str = 'notional_amount'):
        super().__init__(name)
        self._calc_type = CalcType.semi_path_dependent
        self._priceable = priceables
        self._risk = risk
        self._trade_duration = trade_duration
        self._csa_term = csa_term
        self._scaling_parameter = scaling_parameter
        if priceables is not None:
            if self._priceable.name is None:
                self._priceable.name = '{}_Priceable{}'.format(self._name, 0)
            else:
                self._priceable.name = '{}_{}'.format(self._name, self._priceable.name)

    @property
    def trade_duration(self):
        return self._trade_duration

    @property
    def priceable(self):
        return self._priceable

    @property
    def risk(self):
        return self._risk

    @property
    def csa_term(self):
        return self._csa_term

    @property
    def scaling_parameter(self):
        return self._scaling_parameter
