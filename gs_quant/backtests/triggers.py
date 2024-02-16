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


from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import Optional
from gs_quant.backtests.actions import Action, AddTradeAction, AddTradeActionInfo
from gs_quant.backtests.backtest_objects import BackTest, PredefinedAssetBacktest
from gs_quant.backtests.backtest_utils import make_list, CalcType
from gs_quant.backtests.data_sources import *
from gs_quant.base import field_metadata
from gs_quant.datetime.relative_date import RelativeDateSchedule
from gs_quant.risk.transform import Transformer
from gs_quant.risk import RiskMeasure


class TriggerDirection(Enum):
    ABOVE = 1
    BELOW = 2
    EQUAL = 3


class AggType(Enum):
    ALL_OF = 1
    ANY_OF = 2


@dataclass_json
@dataclass
class TriggerRequirements(object):
    pass


@dataclass_json
@dataclass
class PeriodicTriggerRequirements(TriggerRequirements):
    start_date: Optional[dt.date] = field(default=None, metadata=field_metadata)
    end_date: Optional[dt.date] = field(default=None, metadata=field_metadata)
    frequency: Optional[str] = field(default=None, metadata=field_metadata)
    calendar: Optional[str] = field(default=None, metadata=field_metadata)


@dataclass_json
@dataclass
class IntradayTriggerRequirements(TriggerRequirements):
    start_time: Optional[dt.datetime] = field(default=None, metadata=field_metadata)
    end_time: Optional[dt.datetime] = field(default=None, metadata=field_metadata)
    frequency: Optional[str] = field(default=None, metadata=field_metadata)


@dataclass_json
@dataclass
class MktTriggerRequirements(TriggerRequirements):
    data_source: DataSource = field(default=None, metadata=field_metadata)
    trigger_level: float = field(default=None, metadata=field_metadata)
    direction: TriggerDirection = field(default=None, metadata=field_metadata)


@dataclass_json
@dataclass
class RiskTriggerRequirements(TriggerRequirements):
    risk: RiskMeasure = field(default=None, metadata=field_metadata)
    trigger_level: float = field(default=None, metadata=field_metadata)
    direction: TriggerDirection = field(default=None, metadata=field_metadata)
    risk_transformation: Optional[Transformer] = field(default=None, metadata=field_metadata)


@dataclass_json
@dataclass
class AggregateTriggerRequirements(TriggerRequirements):
    triggers: Iterable = field(default=None, metadata=field_metadata)
    aggregate_type: AggType = field(default=AggType.ALL_OF, metadata=field_metadata)


@dataclass_json
@dataclass
class NotTriggerRequirements(TriggerRequirements):
    trigger: object = field(default=None, metadata=field_metadata)


@dataclass_json
@dataclass
class DateTriggerRequirements(TriggerRequirements):
    dates: Iterable[Union[dt.datetime, dt.date]] = field(default=None, metadata=field_metadata)
    entire_day: bool = field(default=False, metadata=field_metadata)


@dataclass_json
@dataclass
class PortfolioTriggerRequirements(TriggerRequirements):
    data_source: str = field(default=None, metadata=field_metadata)
    trigger_level: float = field(default=None, metadata=field_metadata)
    direction: TriggerDirection = field(default=None, metadata=field_metadata)


@dataclass_json
@dataclass
class MeanReversionTriggerRequirements(TriggerRequirements):
    data_source: DataSource = field(default=None, metadata=field_metadata)
    z_score_bound: float = field(default=None, metadata=field_metadata)
    rolling_mean_window: int = field(default=None, metadata=field_metadata)
    rolling_std_window: int = field(default=None, metadata=field_metadata)


@dataclass_json
@dataclass
class TriggerInfo(object):
    triggered: bool
    info_dict: Optional[dict] = None

    def __eq__(self, other):
        return self.triggered is other

    def __bool__(self):
        return self.triggered


@dataclass_json
@dataclass
class Trigger(object):
    trigger_requirements: Optional[TriggerRequirements] = field(default=None, metadata=field_metadata)
    actions: Union[Action, Iterable[Action]] = field(default=None, metadata=field_metadata)

    def __post_init__(self):
        self.actions = make_list(self.actions)

    def has_triggered(self, state: dt.date, backtest: BackTest = None) -> TriggerInfo:
        """
        implemented by sub classes
        :param state:
        :param backtest:
        :return:
            TriggerInfo containing a bool indication of whether the trigger has triggered and optionally info
            in the form of a dictionary of action type to object info understood by that action.
        """
        raise RuntimeError('has_triggered to be implemented by subclass')

    def get_trigger_times(self):
        return []

    @property
    def calc_type(self):
        return CalcType.simple

    @property
    def risks(self):
        return [x.risk for x in make_list(self.actions) if x.risk is not None]


@dataclass_json
@dataclass
class PeriodicTrigger(Trigger):
    trigger_requirements: PeriodicTriggerRequirements = field(default=None, metadata=field_metadata)
    actions: Union[Action, Iterable[Action]] = field(default=None, metadata=field_metadata)
    _trigger_dates = None

    def get_trigger_times(self) -> [dt.date]:
        if not self._trigger_dates:
            self._trigger_dates = self.trigger_requirements.dates if \
                hasattr(self.trigger_requirements, 'dates') else \
                RelativeDateSchedule(self.trigger_requirements.frequency,
                                     self.trigger_requirements.start_date,
                                     self.trigger_requirements.end_date).apply_rule(
                    holiday_calendar=self.trigger_requirements.calendar)
        return self._trigger_dates

    def has_triggered(self, state: dt.date, backtest: BackTest = None) -> TriggerInfo:
        if not self._trigger_dates:
            self.get_trigger_times()
        return TriggerInfo(state in self._trigger_dates)


@dataclass_json
@dataclass
class IntradayPeriodicTrigger(Trigger):
    trigger_requirements: IntradayTriggerRequirements = field(default=None, metadata=field_metadata)
    actions: Union[Action, Iterable[Action]] = field(default=None, metadata=field_metadata)

    def __post_init__(self):
        super().__post_init__()
        # generate all the trigger times
        start = self.trigger_requirements.start_time
        end = self.trigger_requirements.end_time
        freq = self.trigger_requirements.frequency

        self._trigger_times = []
        time = start
        while time <= end:
            self._trigger_times.append(time)
            time = (dt.datetime.combine(dt.date.today(), time) + dt.timedelta(minutes=freq)).time()

    def get_trigger_times(self):
        return self._trigger_times

    def has_triggered(self, state: Union[dt.date, dt.datetime], backtest: BackTest = None) -> TriggerInfo:
        return TriggerInfo(state.time() in self._trigger_times)


@dataclass_json
@dataclass
class MktTrigger(Trigger):
    trigger_requirements: MktTriggerRequirements = field(default=None, metadata=field_metadata)
    actions: Union[Action, Iterable[Action]] = field(default=None, metadata=field_metadata)

    def has_triggered(self, state: dt.date, backtest: BackTest = None) -> TriggerInfo:
        data_value = self.trigger_requirements.data_source.get_data(state)
        if self.trigger_requirements.direction == TriggerDirection.ABOVE:
            if data_value > self.trigger_requirements.trigger_level:
                return TriggerInfo(True)
        elif self.trigger_requirements.direction == TriggerDirection.BELOW:
            if data_value < self.trigger_requirements.trigger_level:
                return TriggerInfo(True)
        else:
            if data_value == self.trigger_requirements.trigger_level:
                return TriggerInfo(True)
        return TriggerInfo(False)


@dataclass_json
@dataclass
class StrategyRiskTrigger(Trigger):
    trigger_requirements: RiskTriggerRequirements = field(default=None, metadata=field_metadata)
    actions: Union[Action, Iterable[Action]] = field(default=None, metadata=field_metadata)

    @property
    def calc_type(self):
        return CalcType.path_dependent

    @property
    def risks(self):
        return [x.risk for x in make_list(self.actions) if x.risk is not None] + [self.trigger_requirements.risk]

    def has_triggered(self, state: dt.date, backtest: BackTest = None) -> TriggerInfo:
        if self.trigger_requirements.risk_transformation is None:
            risk_value = backtest.results[state][self.trigger_requirements.risk].aggregate()
        else:
            risk_value = backtest.results[state][self.trigger_requirements.risk].transform(
                risk_transformation=self.trigger_requirements.risk_transformation).aggregate(
                allow_mismatch_risk_keys=True)
        if self.trigger_requirements.direction == TriggerDirection.ABOVE:
            if risk_value > self.trigger_requirements.trigger_level:
                return TriggerInfo(True)
        elif self.trigger_requirements.direction == TriggerDirection.BELOW:
            if risk_value < self.trigger_requirements.trigger_level:
                return TriggerInfo(True)
        else:
            if risk_value == self.trigger_requirements.trigger_level:
                return TriggerInfo(True)
        return TriggerInfo(False)


@dataclass_json
@dataclass
class AggregateTrigger(Trigger):
    trigger_requirements: AggregateTriggerRequirements = field(default=None, metadata=field_metadata)
    actions: Union[Action, Iterable[Action]] = field(default=None, metadata=field_metadata)

    def __post_init__(self):
        super().__post_init__()
        actions = [] if not self.actions else make_list(self.actions)
        for t in self.trigger_requirements.triggers:
            actions += [action for action in t.actions]
        self.actions = actions

    def has_triggered(self, state: dt.date, backtest: BackTest = None) -> TriggerInfo:
        info_dict = {}
        if self.trigger_requirements.aggregate_type == AggType.ALL_OF:
            for trigger in self.trigger_requirements.triggers:
                t_info = trigger.has_triggered(state, backtest)
                if not t_info:
                    return TriggerInfo(False)
                else:
                    if t_info.info_dict:
                        info_dict.update(t_info.info_dict)
            return TriggerInfo(True, info_dict)
        elif self.trigger_requirements.aggregate_type == AggType.ANY_OF:
            triggered = False
            for trigger in self.trigger_requirements.triggers:
                t_info = trigger.has_triggered(state, backtest)
                if t_info:
                    triggered = True
                    if t_info.info_dict:
                        info_dict.update(t_info.info_dict)
            return TriggerInfo(True, info_dict) if triggered else TriggerInfo(False)
        else:
            raise RuntimeError(f'Unrecognised aggregation type: {self.trigger_requirements.aggregate_type}')

    @property
    def triggers(self) -> Iterable[Trigger]:
        return self.trigger_requirements.triggers


@dataclass_json
@dataclass
class NotTrigger(Trigger):
    trigger_requirements: NotTriggerRequirements = field(default=None, metadata=field_metadata)
    actions: Union[Action, Iterable[Action]] = field(default=None, metadata=field_metadata)

    def __post_init__(self):
        super().__post_init__()
        actions = [] if not self.actions else self.actions
        actions += [action for action in self.trigger_requirements.trigger.actions]

    def has_triggered(self, state: dt.date, backtest: BackTest = None) -> TriggerInfo:
        t_info = self.trigger_requirements.trigger.has_triggered(state, backtest)
        if t_info:
            return TriggerInfo(False)
        else:
            return TriggerInfo(True)


@dataclass_json
@dataclass
class DateTrigger(Trigger):
    trigger_requirements: DateTriggerRequirements = field(default=None, metadata=field_metadata)
    actions: Union[Action, Iterable[Action]] = field(default=None, metadata=field_metadata)

    def __post_init__(self):
        super().__post_init__()
        self._dates_from_datetimes = [d.date() if isinstance(d, dt.datetime) else d
                                      for d in self.trigger_requirements.dates] \
            if self.trigger_requirements.entire_day else None

    def has_triggered(self, state: Union[dt.date, dt.datetime], backtest: BackTest = None) -> TriggerInfo:
        assert isinstance(state, dt.datetime) or isinstance(state, dt.date)

        if self.trigger_requirements.entire_day:
            if isinstance(state, dt.datetime):
                return TriggerInfo(state.date() in self._dates_from_datetimes)
            elif isinstance(state, dt.date):
                return TriggerInfo(state in self._dates_from_datetimes)

        return TriggerInfo(state in self.trigger_requirements.dates)

    def get_trigger_times(self):
        return self._dates_from_datetimes or self.trigger_requirements.dates


@dataclass_json
@dataclass
class PortfolioTrigger(Trigger):
    trigger_requirements: PortfolioTriggerRequirements = field(default=None, metadata=field_metadata)
    actions: Union[Action, Iterable[Action]] = field(default=None, metadata=field_metadata)

    def __post_init__(self):
        super().__post_init__()
        self._current_position = 0

    def has_triggered(self, state: dt.date, backtest: BackTest = None) -> TriggerInfo:
        if self.trigger_requirements.data_source == 'len':
            value = len(backtest.portfolio_dict)
            if self.trigger_requirements.direction == TriggerDirection.ABOVE:
                if value > self.trigger_requirements.trigger_level:
                    return TriggerInfo(True)
            elif self.trigger_requirements.direction == TriggerDirection.BELOW:
                if value < self.trigger_requirements.trigger_level:
                    return TriggerInfo(True)
            else:
                if value == self.trigger_requirements.trigger_level:
                    return TriggerInfo(True)
        return TriggerInfo(False)


@dataclass_json
@dataclass
class MeanReversionTrigger(Trigger):
    trigger_requirements: MeanReversionTriggerRequirements = field(default=None, metadata=field_metadata)
    actions: Union[Action, Iterable[Action]] = field(default=None, metadata=field_metadata)

    def __post_init__(self):
        super().__post_init__()
        self._current_position = 0

    def has_triggered(self, state: dt.date, backtest: BackTest = None) -> TriggerInfo:
        trigger_req = self.trigger_requirements
        rolling_mean = trigger_req.data_source.get_data_range(state, trigger_req.rolling_mean_window).mean()
        rolling_std = trigger_req.data_source.get_data_range(state, trigger_req.rolling_std_window).std()
        current_price = trigger_req.data_source.get_data(state)
        if self._current_position == 0:
            if abs((current_price - rolling_mean) / rolling_std) > self.trigger_requirements.z_score_bound:
                if current_price > rolling_mean:
                    self._current_position = -1
                    return TriggerInfo(True, {AddTradeAction: AddTradeActionInfo(scaling=-1)})
                else:
                    self._current_position = 1
                    return TriggerInfo(True, {AddTradeAction: AddTradeActionInfo(scaling=1)})
        elif self._current_position == 1:
            if current_price > rolling_mean:
                self._current_position = 0
                return TriggerInfo(True, {AddTradeAction: AddTradeActionInfo(scaling=-1)})
        elif self._current_position == -1:
            if current_price > rolling_mean:
                self._current_position = 0
                return TriggerInfo(True, {AddTradeAction: AddTradeActionInfo(scaling=1)})
        else:
            raise RuntimeWarning(f'unexpected current position: {self._current_position}')
        return TriggerInfo(False)


@dataclass_json
@dataclass
class OrdersGeneratorTrigger(Trigger):
    """Base class for triggers used with the PredefinedAssetEngine."""

    def __post_init__(self):
        if not self.actions:
            self.actions = [Action()]
        super().__post_init__()

    def get_trigger_times(self) -> list:
        """
        Returns the set of times when orders can be generated e.g. every 30 min
        :return: list
        """
        raise RuntimeError('get_trigger_times must be implemented by subclass')

    def generate_orders(self, state: dt.datetime, backtest: PredefinedAssetBacktest = None) -> list:
        """
        Returns the orders generated at state
        :param state: the time when orders are generated
        :param backtest: the backtest, used to access the holdings and orders generated so far
        :return: list
        """
        raise RuntimeError('generate_orders must be implemented by subclass')

    def has_triggered(self, state: dt.datetime, backtest: PredefinedAssetBacktest = None) -> TriggerInfo:
        """
        Calls generate_orders if state is among the trigger times
        :param state: the time of the trigger
        :param backtest: the backtest, used to access the holdings and orders generated so far
        :return: list
        """
        if state.time() not in self.get_trigger_times():
            return TriggerInfo(False)
        else:
            orders = self.generate_orders(state, backtest)
            return TriggerInfo(True, {type(a): orders for a in self.actions}) if len(orders) else TriggerInfo(False)
