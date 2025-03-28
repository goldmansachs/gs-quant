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
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json, config
from typing import TypeVar, Callable, ClassVar

from gs_quant.backtests.backtest_utils import *
from gs_quant.backtests.backtest_objects import ConstantTransactionModel, TransactionModel
from gs_quant.base import Priceable, static_field
from gs_quant.common import RiskMeasure
from gs_quant.json_convertors import decode_named_instrument, dc_decode, encode_named_instrument, decode_date_or_str
from gs_quant.json_convertors_common import decode_risk_measure, encode_risk_measure
from gs_quant.markets.portfolio import Portfolio
from gs_quant.markets.securities import *
from gs_quant.risk.transform import Transformer
from gs_quant.target.backtests import BacktestTradingQuantityType

action_count = 1


Duration = Union[str, dt.date, dt.timedelta, CustomDuration]


def default_transaction_cost():
    return ConstantTransactionModel(0)


class ScalingActionType(Enum):
    risk_measure = 'risk_measure'
    size = 'size'
    NAV = 'NAV'


@dataclass_json
@dataclass
class Action(object):
    _needs_scaling = False
    _calc_type = CalcType.simple
    _risk = None
    _transaction_cost = ConstantTransactionModel(0)
    _transaction_cost_exit = None
    name = None
    __sub_classes: ClassVar[List[type]] = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Action.__sub_classes.append(cls)

    @staticmethod
    def sub_classes():
        return tuple(Action.__sub_classes)

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

    @property
    def transaction_cost_exit(self):
        return self._transaction_cost_exit

    @transaction_cost_exit.setter
    def transaction_cost_exit(self, value):
        self._transaction_cost_exit = value


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
                           can also specify 'next schedule' in order to exit at the next periodic trigger date
    :param name: optional additional name to the priceable name
    :param transaction_cost: optional a cash amount paid for each transaction
    :param transaction_cost_exit: optionally specify a different model for exits; defaults to entry cost if None
    """

    priceables: Union[Instrument, Iterable[Instrument]] = field(default=None,
                                                                metadata=config(decoder=decode_named_instrument,
                                                                                encoder=encode_named_instrument))
    trade_duration: Duration = field(default=None,  # de/encoder doesn't handle timedelta
                                     metadata=config(decoder=decode_date_or_str))
    name: str = None
    transaction_cost: TransactionModel = field(default_factory=default_transaction_cost,
                                               metadata=config(decoder=dc_decode(ConstantTransactionModel)))
    transaction_cost_exit: Optional[TransactionModel] = field(default=None,
                                                              metadata=config(
                                                                  decoder=dc_decode(ConstantTransactionModel)))
    holiday_calendar: Iterable[dt.date] = None
    class_type: str = static_field('add_trade_action')

    def __post_init__(self):
        super().__post_init__()
        self._dated_priceables = {}
        named_priceables = []
        for i, p in enumerate(make_list(self.priceables)):
            if p.name is None:
                named_priceables.append(p.clone(name=f'{self.name}_Priceable{i}'))
            elif p.name.startswith(self.name):
                named_priceables.append(p)
            else:
                named_priceables.append(p.clone(name=f'{self.name}_{p.name}'))
        self.priceables = named_priceables
        if self.transaction_cost is None:
            self.transaction_cost = ConstantTransactionModel(0)
        if self.transaction_cost_exit is None:
            self.transaction_cost_exit = self.transaction_cost

    def set_dated_priceables(self, state, priceables):
        self._dated_priceables[state] = make_list(priceables)

    @property
    def dated_priceables(self):
        return self._dated_priceables


AddTradeActionInfo = namedtuple('AddTradeActionInfo', ['scaling', 'next_schedule'])
HedgeActionInfo = namedtuple('HedgeActionInfo', 'next_schedule')
ExitTradeActionInfo = namedtuple('ExitTradeActionInfo', 'not_applicable')
RebalanceActionInfo = namedtuple('RebalanceActionInfo', 'not_applicable')
AddScaledTradeActionInfo = namedtuple('AddScaledActionInfo', 'next_schedule')


@dataclass_json
@dataclass
class AddScaledTradeAction(Action):

    """
    create an action which adds a trade when triggered.  The trade is scaled by a measure or trade property.
    The trades are resolved on the trigger date (state) and last until the trade_duration if specified or for
    all future dates if not.
    :param priceables: a priceable or a list of pricables.
    :param trade_duration: an instrument attribute eg. 'expiration_date' or a date or a tenor or timedelta
                           if left as None the
                           trade will be added for all future dates
                           can also specify 'next schedule' in order to exit at the next periodic trigger date
    :param name: optional additional name to the priceable name
    :param scaling_type: the type of scaling we are doing
    :param scaling_risk: if the scaling type is a measure then this is the definition of the measure
    :param scaling_level: the level of scaling to be done
    :param transaction_cost: optional a cash amount paid for each transaction
    :param transaction_cost_exit: optionally specify a different model for exits; defaults to entry cost if None
    """
    priceables: Union[Priceable, Iterable[Priceable]] = field(default=None,
                                                              metadata=config(decoder=decode_named_instrument,
                                                                              encoder=encode_named_instrument))
    trade_duration: Duration = field(default=None,  # de/encoder doesn't handle timedelta
                                     metadata=config(decoder=decode_date_or_str))
    name: str = None
    scaling_type: ScalingActionType = ScalingActionType.size
    scaling_risk: RiskMeasure = None
    scaling_level: Union[float, int] = 1
    transaction_cost: TransactionModel = field(default_factory=default_transaction_cost,
                                               metadata=config(decoder=dc_decode(ConstantTransactionModel)))
    transaction_cost_exit: Optional[TransactionModel] = field(default=None,
                                                              metadata=config(
                                                                  decoder=dc_decode(ConstantTransactionModel)))
    holiday_calendar: Iterable[dt.date] = None
    class_type: str = static_field('add_scaled_trade_action')

    def __post_init__(self):
        super().__post_init__()
        named_priceables = []
        for i, p in enumerate(make_list(self.priceables)):
            if p.name is None:
                named_priceables.append(p.clone(name=f'{self.name}_Priceable{i}'))
            elif p.name.startswith(self.name):
                named_priceables.append(p)
            else:
                named_priceables.append(p.clone(name=f'{self.name}_{p.name}'))
        self.priceables = named_priceables
        if self.transaction_cost_exit is None:
            self.transaction_cost_exit = self.transaction_cost


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
    priceables: Union[Priceable, Iterable[Priceable]] = field(default=None,
                                                              metadata=config(decoder=decode_named_instrument,
                                                                              encoder=encode_named_instrument))
    trade_duration: Duration = field(default=None,  # de/encoder doesn't handle timedelta
                                     metadata=config(decoder=decode_date_or_str))
    name: str = None
    trade_quantity: float = 1
    trade_quantity_type: BacktestTradingQuantityType = BacktestTradingQuantityType.quantity
    class_type: str = static_field('enter_position_quantity_scaled_action')

    def __post_init__(self):
        super().__post_init__()
        named_priceables = []
        for i, p in enumerate(make_list(self.priceables)):
            if p.name is None:
                named_priceables.append(p.clone(name=f'{self.name}_Priceable{i}'))
            elif p.name.startswith(self.name):
                named_priceables.append(p)
            else:
                named_priceables.append(p.clone(name=f'{self.name}_{p.name}'))
        self.priceables = named_priceables


@dataclass_json
@dataclass
class ExitPositionAction(Action):
    name: str = None
    class_type: str = 'exit_position_action'


@dataclass_json
@dataclass
class ExitTradeAction(Action):
    priceable_names: Union[str, Iterable[str]] = None
    name: str = None
    transaction_cost: TransactionModel = field(default_factory=default_transaction_cost,
                                               metadata=config(decoder=dc_decode(ConstantTransactionModel)))
    class_type: str = static_field('exit_trade_action')

    def __post_init__(self):
        super().__post_init__()
        self.priceables_names = make_list(self.priceable_names)


@dataclass_json
@dataclass
class ExitAllPositionsAction(ExitTradeAction):
    """
    Fully exit all held positions
    """
    class_type: str = static_field('exit_all_positions_action')

    def __post_init__(self):
        super().__post_init__()
        self._calc_type = CalcType.path_dependent


@dataclass_json
@dataclass
class HedgeAction(Action):

    """
    create an action which adds a hedge trade when triggered.  This trade will be scaled to hedge the risk
    specified.  The trades are resolved on the trigger date (state) and
    last until the trade_duration if specified or for all future dates if not.
    :param risk: a risk measure which should be hedged
    :param priceables: a priceable or a list of pricables these should have sensitivity to the risk.
    :param trade_duration: an instrument attribute eg. 'expiration_date' or a date or a tenor or timedelta
                           if left as None the
                           trade will be added for all future dates
                           can also specify 'next schedule' in order to exit at the next periodic trigger date
    :param name: optional additional name to the priceable name
    :param transaction_cost: optional a cash amount paid for each transaction
    :param transaction_cost_exit: optionally specify a different model for exits; defaults to entry cost if None
    :param risk_transformation: optional a Transformer which will be applied to the raw risk numbers before hedging
    :param holiday_calendar: optional an iterable list of holiday dates
    """

    risk: RiskMeasure = field(default=None, metadata=config(decoder=decode_risk_measure,
                                                            encoder=encode_risk_measure))
    priceables: Optional[Priceable] = field(default=None, metadata=config(decoder=decode_named_instrument,
                                                                          encoder=encode_named_instrument))
    trade_duration: Duration = field(default=None,  # de/encoder doesn't handle timedelta
                                     metadata=config(decoder=decode_date_or_str))
    name: str = None
    csa_term: str = None
    scaling_parameter: str = 'notional_amount'
    transaction_cost: TransactionModel = field(default_factory=default_transaction_cost,
                                               metadata=config(decoder=dc_decode(ConstantTransactionModel)))
    transaction_cost_exit: Optional[TransactionModel] = field(default=None,
                                                              metadata=config(
                                                                  decoder=dc_decode(ConstantTransactionModel)))
    risk_transformation: Transformer = None
    holiday_calendar: Iterable[dt.date] = None
    class_type: str = static_field('hedge_action')

    def __post_init__(self):
        super().__post_init__()
        self._calc_type = CalcType.semi_path_dependent
        if isinstance(self.priceables, Portfolio):
            named_priceables = []
            for i, priceable in enumerate(self.priceables):
                if priceable.name is None:
                    named_priceables.append(priceable.clone(name=f'{self.name}_Priceable{i}'))
                elif priceable.name.startswith(self.name):
                    named_priceables.append(priceable)
                else:
                    named_priceables.append(priceable.clone(name=f'{self.name}_{priceable.name}'))
            named_priceable = Portfolio(named_priceables)
        elif isinstance(self.priceables, Priceable):
            if self.priceables.name is None:
                named_priceable = self.priceables.clone(name=f'{self.name}_Priceable0')
            elif self.priceable.name.startswith(self.name):
                named_priceable = self.priceable
            else:
                named_priceable = self.priceables.clone(name=f'{self.name}_{self.priceables.name}')
        else:
            raise RuntimeError('hedge action only accepts one trade or one portfolio')
        self.priceables = named_priceable
        if self.transaction_cost_exit is None:
            self.transaction_cost_exit = self.transaction_cost

    @property
    def priceable(self):
        return self.priceables


@dataclass_json
@dataclass
class RebalanceAction(Action):
    priceable: Priceable = field(default=None, metadata=config(decoder=decode_named_instrument,
                                                               encoder=encode_named_instrument))
    size_parameter: Union[str, float] = None
    method: Callable = None
    transaction_cost: TransactionModel = field(default_factory=default_transaction_cost,
                                               metadata=config(decoder=dc_decode(ConstantTransactionModel)))
    transaction_cost_exit: Optional[TransactionModel] = field(default=None,
                                                              metadata=config(
                                                                  decoder=dc_decode(ConstantTransactionModel)))
    name: str = None

    def __post_init__(self):
        super().__post_init__()
        self._calc_type = CalcType.path_dependent
        if self.priceable.unresolved is None:
            raise ValueError("Please specify a resolved priceable to rebalance.")
        if self.priceable is not None:
            if self.priceable.name is None:
                self.priceable = self.priceable.clone(name=f'{self.name}_Priceable0')
            else:
                self.priceable = self.priceable.clone(name=f'{self.name}_{self.priceable.name}')
        if self.transaction_cost_exit is None:
            self.transaction_cost_exit = self.transaction_cost
