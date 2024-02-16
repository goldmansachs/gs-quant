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
import copy
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import TypeVar, Callable

from gs_quant.backtests.backtest_utils import *
from gs_quant.backtests.backtest_objects import ConstantTransactionModel, TransactionModel
from gs_quant.base import Priceable
from gs_quant.common import RiskMeasure
from gs_quant.markets.portfolio import Portfolio
from gs_quant.markets.securities import *
from gs_quant.risk.transform import Transformer
from gs_quant.target.backtests import BacktestTradingQuantityType

action_count = 1


def default_transaction_cost(obj):
    return field(default_factory=lambda: copy.copy(obj))


@dataclass_json
@dataclass
class Action(object):
    _needs_scaling = False
    _calc_type = CalcType.simple
    _risk = None
    _transaction_cost = ConstantTransactionModel(0)
    name = None

    def __post_init__(self):
        self.set_name(self.name)

    @property
    def calc_type(self):
        return self._calc_type

    @property
    def risk(self):
        return self._risk

    def set_name(self, name: str):
        global action_count
        if self.name is None:
            self.name = 'Action{}'.format(action_count)
            action_count += 1

    @property
    def transaction_cost(self):
        return self._transaction_cost

    @transaction_cost.setter
    def transaction_cost(self, value):
        self._transaction_cost = value


TAction = TypeVar('TAction', bound='Action')


@dataclass_json
@dataclass
class AddTradeAction(Action):
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

    priceables: Union[Priceable, Iterable[Priceable]] = None
    trade_duration: Union[str, dt.date, dt.timedelta] = None
    name: str = None
    transaction_cost: TransactionModel = default_transaction_cost(ConstantTransactionModel())

    def __post_init__(self):
        self._dated_priceables = {}
        named_priceables = []
        for i, p in enumerate(make_list(self.priceables)):
            if p.name is None:
                named_priceables.append(p.clone(name=f'{self.name}_Priceable{i}'))
            else:
                named_priceables.append(p.clone(name=f'{self.name}_{p.name}'))
        self.priceables = named_priceables

    def set_dated_priceables(self, state, priceables):
        self._dated_priceables[state] = make_list(priceables)

    @property
    def dated_priceables(self):
        return self._dated_priceables


AddTradeActionInfo = namedtuple('AddTradeActionInfo', 'scaling')
EnterPositionQuantityScaledActionInfo = namedtuple('EnterPositionQuantityScaledActionInfo', 'not_applicable')
HedgeActionInfo = namedtuple('HedgeActionInfo', 'not_applicable')
ExitTradeActionInfo = namedtuple('ExitTradeActionInfo', 'not_applicable')
RebalanceActionInfo = namedtuple('RebalanceActionInfo', 'not_applicable')


@dataclass_json
@dataclass
class EnterPositionQuantityScaledAction(Action):
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
    priceables: Union[Priceable, Iterable[Priceable]] = None
    trade_duration: Union[str, dt.date, dt.timedelta] = None
    name: str = None
    trade_quantity: float = 1
    trade_quantity_type: Union[BacktestTradingQuantityType, str] = BacktestTradingQuantityType.quantity

    def __post_init__(self):
        named_priceables = []
        for i, p in enumerate(make_list(self.priceables)):
            if p.name is None:
                named_priceables.append(p.clone(name=f'{self.name}_Priceable{i}'))
            else:
                named_priceables.append(p.clone(name=f'{self.name}_{p.name}'))
        self.priceables = named_priceables


@dataclass_json
@dataclass
class ExitPositionAction(Action):
    name: str = None


@dataclass_json
@dataclass
class ExitTradeAction(Action):
    priceable_names: Union[str, Iterable[str]] = None
    name: str = None

    def __post_init__(self):
        self.priceables_names = make_list(self.priceable_names)


@dataclass_json
@dataclass
class ExitAllPositionsAction(ExitTradeAction):
    """
    Fully exit all held positions
    """

    def __post_init__(self):
        self._calc_type = CalcType.path_dependent


@dataclass_json
@dataclass
class HedgeAction(Action):
    risk: RiskMeasure = None
    priceables: Optional[Priceable] = None
    trade_duration: Union[str, dt.date, dt.timedelta] = None
    name: str = None
    csa_term: str = None
    scaling_parameter: str = 'notional_amount'
    transaction_cost: TransactionModel = default_transaction_cost(ConstantTransactionModel())
    risk_transformation: Transformer = None

    def __post_init__(self):
        self._calc_type = CalcType.semi_path_dependent
        if isinstance(self.priceables, Portfolio):
            named_priceables = []
            for i, priceable in enumerate(self.priceables):
                if priceable.name is None:
                    named_priceables.append(priceable.clone(name=f'{self.name}_Priceable{i}'))
                else:
                    named_priceables.append(priceable.clone(name=f'{self.name}_{priceable.name}'))
            named_priceable = Portfolio(named_priceables)
        elif isinstance(self.priceables, Priceable):
            if self.priceables.name is None:
                named_priceable = self.priceables.clone(name=f'{self.name}_Priceable0')
            else:
                named_priceable = self.priceables.clone(name=f'{self.name}_{self.priceables.name}')
        else:
            raise RuntimeError('hedge action only accepts one trade or one portfolio')
        self.priceables = named_priceable

    @property
    def priceable(self):
        return self.priceables


@dataclass_json
@dataclass
class RebalanceAction(Action):
    priceable: Priceable = None
    size_parameter: Union[str, float] = None
    method: Callable = None
    transaction_cost: TransactionModel = default_transaction_cost(ConstantTransactionModel())
    name: str = None

    def __post_init__(self):
        self._calc_type = CalcType.path_dependent
        if self.priceable.unresolved is None:
            raise ValueError("Please specify a resolved priceable to rebalance.")
        if self.priceable is not None:
            if self.priceable.name is None:
                self.priceable = self.priceable.clone(name=f'{self.name}_Priceable0')
            else:
                self.priceable = self.priceable.clone(name=f'{self.name}_{self.priceable.name}')
