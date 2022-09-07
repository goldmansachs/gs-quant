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

from collections import namedtuple
from typing import TypeVar

from gs_quant.backtests.backtest_utils import *
from gs_quant.backtests.backtest_objects import ConstantTransactionModel, TransactionModel
from gs_quant.risk.transform import Transformer
from gs_quant.base import Priceable
from gs_quant.markets.securities import *
from gs_quant.markets.portfolio import Portfolio
from gs_quant.target.backtests import BacktestTradingQuantityType

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
        self._transaction_cost = ConstantTransactionModel(0)

    @property
    def calc_type(self):
        return self._calc_type

    @property
    def risk(self):
        return self._risk

    @property
    def transaction_cost(self):
        return self._transaction_cost


TAction = TypeVar('TAction', bound='Action')


class AddTradeAction(Action):
    def __init__(self,
                 priceables: Union[Priceable, Iterable[Priceable]],
                 trade_duration: Union[str, dt.date, dt.timedelta] = None,
                 name: str = None,
                 transaction_cost: TransactionModel = ConstantTransactionModel(0)):
        """
        create an action which adds a trade when triggered.  The trades are resolved on the trigger date (state) and
        last until the trade_duration if specified or for all future dates if not.
        :param priceables: a priceable or a list of pricables.
        :param trade_duration: an instrument attribute eg. 'expiration_date' or a date or a tenor or timedelta
                               if left as None the
                               trade will be added for all future dates
        :param name: optional additional name to the priceable name
        :param transaction_cost: optional a cash amount paid for each transaction, paid on both enter and exit
        """
        super().__init__(name)

        self._priceables = []
        self._dated_priceables = {}
        self._trade_duration = trade_duration
        self._transaction_cost = transaction_cost
        for i, p in enumerate(make_list(priceables)):
            if p.name is None:
                self._priceables.append(p.clone(name=f'{self._name}_Priceable{i}'))
            else:
                self._priceables.append(p.clone(name=f'{self._name}_{p.name}'))

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

    @property
    def transaction_cost(self):
        return self._transaction_cost


AddTradeActionInfo = namedtuple('AddTradeActionInfo', 'scaling')
EnterPositionQuantityScaledActionInfo = namedtuple('EnterPositionQuantityScaledActionInfo', 'not_applicable')
HedgeActionInfo = namedtuple('HedgeActionInfo', 'not_applicable')
ExitTradeActionInfo = namedtuple('ExitTradeActionInfo', 'not_applicable')
RebalanceActionInfo = namedtuple('RebalanceActionInfo', 'not_applicable')


class EnterPositionQuantityScaledAction(Action):
    def __init__(self,
                 priceables: Union[Priceable, Iterable[Priceable]],
                 trade_duration: Union[str, dt.date, dt.timedelta] = None,
                 name: str = None,
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
        self._priceables = []
        self._trade_duration = trade_duration
        for i, p in enumerate(make_list(priceables)):
            if p.name is None:
                self._priceables.append(p.clone(name=f'{self._name}_Priceable{i}'))
            else:
                self._priceables.append(p.clone(name=f'{self._name}_{p.name}'))
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


class ExitTradeAction(Action):
    def __init__(self, priceable_names: Union[str, Iterable[str]] = None, name: str = None):
        """
        Fully exit all held positions
        :param priceable_names: optional string or list of strings of priceable names
        :param name: optional name of the action
        """
        super().__init__(name)
        self._priceables_names = make_list(priceable_names)

    @property
    def priceable_names(self):
        return self._priceables_names


class HedgeAction(Action):
    def __init__(self, risk, priceables: Priceable = None, trade_duration: str = None, name: str = None,
                 csa_term: str = None, scaling_parameter: str = 'notional_amount',
                 transaction_cost: TransactionModel = ConstantTransactionModel(0),
                 risk_transformation: Transformer = None):
        super().__init__(name)
        self._calc_type = CalcType.semi_path_dependent
        self._priceable = priceables
        self._risk = risk
        self._trade_duration = trade_duration
        self._csa_term = csa_term
        self._scaling_parameter = scaling_parameter
        self._transaction_cost = transaction_cost
        self._risk_transformation = risk_transformation
        if isinstance(priceables, Portfolio):
            trades = []
            for i, priceable in enumerate(priceables):
                if priceable.name is None:
                    trades.append(priceable.clone(name=f'{self._name}_Priceable{i}'))
                else:
                    trades.append(priceable.clone(name=f'{self._name}_{priceable.name}'))
            self._priceable = Portfolio(trades)
        else:
            if priceables is not None:
                if priceables.name is None:
                    self._priceable = priceables.clone(name=f'{self._name}_Priceable0')
                else:
                    self._priceable = priceables.clone(name=f'{self._name}_{priceables.name}')

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

    @property
    def transaction_cost(self):
        return self._transaction_cost

    @property
    def risk_transformation(self):
        return self._risk_transformation


class RebalanceAction(Action):
    def __init__(self, priceable: Priceable, size_parameter, method,
                 transaction_cost: TransactionModel = ConstantTransactionModel(0)):
        super().__init__()
        self._calc_type = CalcType.path_dependent
        self._size_parameter = size_parameter
        self._method = method
        self._transaction_cost = transaction_cost
        if priceable.unresolved is None:
            raise ValueError("Please specify a resolved priceable to rebalance.")
        if priceable is not None:
            if priceable.name is None:
                self._priceable = priceable.clone(name=f'{self._name}_Priceable0')
            else:
                self._priceable = priceable.clone(name=f'{self._name}_{priceable.name}')

    @property
    def priceable(self):
        return self._priceable

    @property
    def size_parameter(self):
        return self._size_parameter

    @property
    def method(self):
        return self._method

    @property
    def args(self):
        return self._args

    @property
    def transaction_cost(self):
        return self._transaction_cost
