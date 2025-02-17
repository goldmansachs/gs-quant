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

from gs_quant.backtests.actions import *
from gs_quant.backtests.backtest_objects import BackTest, PredefinedAssetBacktest
from gs_quant.backtests.backtest_utils import make_list, CalcType
from gs_quant.backtests.data_sources import *
from gs_quant.base import field_metadata, exclude_none
from gs_quant.datetime.relative_date import RelativeDateSchedule
from gs_quant.json_convertors import decode_iso_date_or_datetime, decode_date_tuple
from gs_quant.json_convertors_common import encode_risk_measure, decode_risk_measure
from gs_quant.risk import RiskMeasure
from gs_quant.risk.transform import Transformer


class TriggerDirection(Enum):
    ABOVE = 1
    BELOW = 2
    EQUAL = 3


class AggType(Enum):
    ALL_OF = 1
    ANY_OF = 2


@dataclass_json
@dataclass
class TriggerRequirements:

    __sub_classes: ClassVar[List[type]] = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        TriggerRequirements.__sub_classes.append(cls)

    @staticmethod
    def sub_classes():
        return tuple(TriggerRequirements.__sub_classes)

    def get_trigger_times(self):
        return []

    @property
    def calc_type(self):
        return CalcType.simple


@dataclass_json
@dataclass
class TriggerInfo(object):
    triggered: bool
    info_dict: Optional[dict] = None

    def __eq__(self, other):
        return self.triggered is other

    def __bool__(self):
        return self.triggered


def check_barrier(direction, test_value, trigger_level) -> TriggerInfo:
    if direction == TriggerDirection.ABOVE:
        if test_value > trigger_level:
            return TriggerInfo(True)
    elif direction == TriggerDirection.BELOW:
        if test_value < trigger_level:
            return TriggerInfo(True)
    else:
        if test_value == trigger_level:
            return TriggerInfo(True)
    return TriggerInfo(False)


@dataclass_json
@dataclass
class PeriodicTriggerRequirements(TriggerRequirements):
    start_date: Optional[dt.date] = field(default=None, metadata=field_metadata)
    end_date: Optional[dt.date] = field(default=None, metadata=field_metadata)
    frequency: Optional[str] = field(default=None, metadata=field_metadata)
    calendar: Optional[Iterable[dt.date]] = field(default=None, metadata=config(exclude=exclude_none,
                                                                                decoder=decode_date_tuple))
    trigger_dates = []
    class_type: str = static_field('periodic_trigger_requirements')

    def get_trigger_times(self) -> [dt.date]:
        if not self.trigger_dates:
            self.trigger_dates = RelativeDateSchedule(self.frequency, self.start_date,
                                                      self.end_date).apply_rule(holiday_calendar=self.calendar)
        return self.trigger_dates

    def has_triggered(self, state: dt.date, backtest: BackTest = None) -> TriggerInfo:
        if not self.trigger_dates:
            self.get_trigger_times()
        if state in self.trigger_dates:
            next_state = None
            if self.trigger_dates.index(state) != len(self.trigger_dates) - 1:
                next_state = self.trigger_dates[self.trigger_dates.index(state) + 1]
            return TriggerInfo(True, {AddTradeAction: AddTradeActionInfo(scaling=None, next_schedule=next_state),
                                      AddScaledTradeAction: AddScaledTradeActionInfo(next_schedule=next_state),
                                      HedgeAction: HedgeActionInfo(next_schedule=next_state)})
        return TriggerInfo(False)


@dataclass_json
@dataclass
class IntradayTriggerRequirements(TriggerRequirements):
    start_time: Optional[dt.time] = field(default=None, metadata=field_metadata)
    end_time: Optional[dt.time] = field(default=None, metadata=field_metadata)
    frequency: Optional[float] = field(default=None, metadata=field_metadata)
    class_type: str = static_field('intraday_trigger_requirements')

    def __post_init__(self):
        # generate all the trigger times
        self._trigger_times = []
        time = self.start_time
        while time <= self.end_time:
            self._trigger_times.append(time)
            time = (dt.datetime.combine(dt.date.today(), time) + dt.timedelta(minutes=self.frequency)).time()

    def get_trigger_times(self):
        return self._trigger_times

    def has_triggered(self, state: Union[dt.date, dt.datetime], backtest: BackTest = None) -> TriggerInfo:
        return TriggerInfo(state.time() in self._trigger_times)


@dataclass_json
@dataclass
class MktTriggerRequirements(TriggerRequirements):
    data_source: DataSource = field(default=None, metadata=config(decoder=dc_decode(*DataSource.sub_classes(),
                                                                                    allow_missing=True)))
    trigger_level: float = field(default=None, metadata=field_metadata)
    direction: TriggerDirection = field(default=None, metadata=field_metadata)
    class_type: str = static_field('mkt_trigger_requirements')

    def has_triggered(self, state: dt.date, backtest: BackTest = None) -> TriggerInfo:
        data_value = self.data_source.get_data(state)
        try:
            triggered = check_barrier(self.direction, data_value, self.trigger_level)
        except TypeError:
            raise RuntimeError(f'unable to determine trigger state on {str(state)}, data value was {data_value}')
        return triggered


@dataclass_json
@dataclass
class RiskTriggerRequirements(TriggerRequirements):
    risk: RiskMeasure = field(default=None, metadata=config(decoder=decode_risk_measure, encoder=encode_risk_measure))
    trigger_level: float = field(default=None, metadata=field_metadata)
    direction: TriggerDirection = field(default=None, metadata=field_metadata)
    risk_transformation: Optional[Transformer] = field(default=None, metadata=field_metadata)
    class_type: str = static_field('risk_trigger_requirements')

    def has_triggered(self, state: dt.date, backtest: BackTest = None) -> TriggerInfo:
        if state not in backtest.results:
            return TriggerInfo(False)
        if self.risk_transformation is None:
            risk_value = backtest.results[state][self.risk].aggregate()
        else:
            risk_value = backtest.results[state][self.risk].transform(
                risk_transformation=self.risk_transformation).aggregate(
                allow_mismatch_risk_keys=True)
        return check_barrier(self.direction, risk_value, self.trigger_level)

    @property
    def calc_type(self):
        return CalcType.path_dependent


@dataclass_json
@dataclass
class AggregateTriggerRequirements(TriggerRequirements):
    triggers: Iterable[TriggerRequirements] = field(default=None, metadata=field_metadata)
    aggregate_type: AggType = field(default=AggType.ALL_OF, metadata=field_metadata)
    class_type: str = static_field('aggregate_trigger_requirements')

    def __setattr__(self, key, value):
        if key == 'triggers':
            if all([isinstance(v, Trigger) for v in value]):
                value = tuple(v.trigger_requirements for v in value)
        super().__setattr__(key, value)

    def has_triggered(self, state: dt.date, backtest: BackTest = None) -> TriggerInfo:
        info_dict = {}
        if self.aggregate_type == AggType.ALL_OF:
            for trigger in self.triggers:
                t_info = trigger.has_triggered(state, backtest)
                if not t_info:
                    return TriggerInfo(False)
                else:
                    if t_info.info_dict:
                        info_dict.update(t_info.info_dict)
            return TriggerInfo(True, info_dict)
        elif self.aggregate_type == AggType.ANY_OF:
            triggered = False
            for trigger in self.triggers:
                t_info = trigger.has_triggered(state, backtest)
                if t_info:
                    triggered = True
                    if t_info.info_dict:
                        info_dict.update(t_info.info_dict)
            return TriggerInfo(True, info_dict) if triggered else TriggerInfo(False)
        else:
            raise RuntimeError(f'Unrecognised aggregation type: {self.aggregate_type}')

    @property
    def calc_type(self):
        seen_types = set()
        for trigger in self.triggers:
            seen_types.add(trigger.calc_type)

        if CalcType.path_dependent in seen_types:
            return CalcType.path_dependent
        elif CalcType.semi_path_dependent in seen_types:
            return CalcType.semi_path_dependent
        else:
            return CalcType.simple


@dataclass_json
@dataclass
class NotTriggerRequirements(TriggerRequirements):
    trigger: TriggerRequirements = field(default=None, metadata=field_metadata)
    class_type: str = static_field('not_trigger_requirements')

    def __setattr__(self, key, value):
        if key == 'trigger':
            if isinstance(value, Trigger):
                value = value.trigger_requirements
            super().__setattr__(key, value)

    def has_triggered(self, state: dt.date, backtest: BackTest = None) -> TriggerInfo:
        t_info = self.trigger.has_triggered(state, backtest)
        if t_info:
            return TriggerInfo(False)
        else:
            return TriggerInfo(True)


@dataclass_json
@dataclass
class DateTriggerRequirements(TriggerRequirements):
    dates: Iterable[Union[dt.datetime, dt.date]] = field(default=None, metadata=config(
        exclude=exclude_none, decoder=decode_iso_date_or_datetime))
    entire_day: bool = field(default=False, metadata=field_metadata)
    class_type: str = static_field('date_trigger_requirements')
    dates_from_datetimes = []

    def __post_init__(self):
        self.dates_from_datetimes = [d.date() if isinstance(d, dt.datetime)
                                     else d for d in self.dates] if self.entire_day else None

    def has_triggered(self, state: Union[dt.date, dt.datetime], backtest: BackTest = None) -> TriggerInfo:
        if self.entire_day:
            dates = sorted(self.dates_from_datetimes)
            if isinstance(state, dt.datetime):
                state = state.date()
        else:
            dates = sorted(self.dates)
        if state in dates:
            next_state = None
            if dates.index(state) < len(dates) - 1:
                next_state = dates[dates.index(state) + 1]
            return TriggerInfo(True, {AddTradeAction: AddTradeActionInfo(scaling=None, next_schedule=next_state),
                                      AddScaledTradeAction: AddScaledTradeActionInfo(next_schedule=next_state),
                                      HedgeAction: HedgeActionInfo(next_schedule=next_state)})
        return TriggerInfo(False)

    def get_trigger_times(self):
        return self.dates_from_datetimes or self.dates


@dataclass_json
@dataclass
class PortfolioTriggerRequirements(TriggerRequirements):
    data_source: str = field(default=None, metadata=field_metadata)
    trigger_level: float = field(default=None, metadata=field_metadata)
    direction: TriggerDirection = field(default=None, metadata=field_metadata)
    class_type: str = static_field('portfolio_trigger_requirements')

    def has_triggered(self, state: dt.date, backtest: BackTest = None) -> TriggerInfo:
        if self.data_source == 'len':
            value = len(backtest.portfolio_dict)
            if self.direction == TriggerDirection.ABOVE:
                if value > self.trigger_level:
                    return TriggerInfo(True)
            elif self.direction == TriggerDirection.BELOW:
                if value < self.trigger_level:
                    return TriggerInfo(True)
            else:
                if value == self.trigger_level:
                    return TriggerInfo(True)
        return TriggerInfo(False)


@dataclass_json
@dataclass
class MeanReversionTriggerRequirements(TriggerRequirements):
    data_source: DataSource = field(default=None, metadata=config(decoder=dc_decode(*DataSource.sub_classes(),
                                                                                    allow_missing=True)))
    z_score_bound: float = field(default=None, metadata=field_metadata)
    rolling_mean_window: int = field(default=None, metadata=field_metadata)
    rolling_std_window: int = field(default=None, metadata=field_metadata)
    current_position = 0
    class_type: str = static_field('mean_reversion_trigger_requirements')

    def has_triggered(self, state: dt.date, backtest: BackTest = None) -> TriggerInfo:
        rolling_mean = self.data_source.get_data_range(state, self.rolling_mean_window).mean()
        rolling_std = self.data_source.get_data_range(state, self.rolling_std_window).std()
        current_price = self.data_source.get_data(state)
        if self.current_position == 0:
            if abs((current_price - rolling_mean) / rolling_std) > self.z_score_bound:
                if current_price > rolling_mean:
                    self.current_position = -1
                    return TriggerInfo(True, {AddTradeAction: AddTradeActionInfo(scaling=-1)})
                else:
                    self.current_position = 1
                    return TriggerInfo(True, {AddTradeAction: AddTradeActionInfo(scaling=1)})
        elif self.current_position == 1:
            if current_price > rolling_mean:
                self._current_position = 0
                return TriggerInfo(True, {AddTradeAction: AddTradeActionInfo(scaling=-1)})
        elif self.current_position == -1:
            if current_price > rolling_mean:
                self.current_position = 0
                return TriggerInfo(True, {AddTradeAction: AddTradeActionInfo(scaling=1)})
        else:
            raise RuntimeWarning(f'unexpected current position: {self.current_position}')
        return TriggerInfo(False)


@dataclass_json
@dataclass
class TradeCountTriggerRequirements(TriggerRequirements):
    trade_count: float = field(default=None, metadata=field_metadata)
    direction: TriggerDirection = field(default=None, metadata=field_metadata)
    class_type: str = static_field('trade_count_requirements')

    def has_triggered(self, state: dt.date, backtest: BackTest = None) -> TriggerInfo:
        value = len(backtest.portfolio_dict.get(state, []))
        if self.direction == TriggerDirection.ABOVE:
            if value > self.trade_count:
                return TriggerInfo(True)
        elif self.direction == TriggerDirection.BELOW:
            if value < self.trade_count:
                return TriggerInfo(True)
        else:
            if value == self.trade_count:
                return TriggerInfo(True)
        return TriggerInfo(False)

    @property
    def calc_type(self):
        return CalcType.path_dependent


@dataclass_json
@dataclass
class EventTriggerRequirements(TriggerRequirements):
    event_name: str = field(default=None, metadata=field_metadata)
    offset_days: int = 0
    data_source: DataSource = field(default=None, metadata=config(decoder=dc_decode(*DataSource.sub_classes(),
                                                                                    allow_missing=True)))
    class_type: str = static_field('event_requirements')
    trigger_dates = []

    def __post_init__(self):
        if self.data_source is None:
            self.data_source = GsDataSource(data_set='MACRO_EVENTS_CALENDAR', asset_id=None, value_header='eventName')

    def get_trigger_times(self) -> [dt.date]:
        if not self.trigger_dates:
            kwargs = {'eventName': self.event_name}
            self.trigger_dates = [d.date() + dt.timedelta(days=self.offset_days) for d in
                                  self.data_source.get_data(None, **kwargs).index]
        return self.trigger_dates

    def has_triggered(self, state: dt.date, backtest: BackTest = None) -> TriggerInfo:
        dates = sorted(self.trigger_dates)
        if state in dates:
            next_state = None
            if dates.index(state) < len(dates) - 1:
                next_state = dates[dates.index(state) + 1]
            return TriggerInfo(True, {AddTradeAction: AddTradeActionInfo(scaling=None, next_schedule=next_state),
                                      AddScaledTradeAction: AddScaledTradeActionInfo(next_schedule=next_state),
                                      HedgeAction: HedgeActionInfo(next_schedule=next_state)})
        return TriggerInfo(False)

    @staticmethod
    def list_events(currency: str,
                    start=Optional[dt.datetime],
                    end=Optional[dt.datetime], **kwargs):
        kwargs['currency'] = currency
        dataset = Dataset('MACRO_EVENTS_CALENDAR')
        return dataset.get_data(start, end, **kwargs)['eventName'].unique()


@dataclass_json
@dataclass
class Trigger:
    trigger_requirements: Optional[TriggerRequirements] = field(default=None, metadata=field_metadata)
    actions: Union[Action, Iterable[Action]] = field(default=None,
                                                     metadata=config(
                                                         decoder=dc_decode(*Action.sub_classes(), allow_missing=True)))
    __sub_classes: ClassVar[List[type]] = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Trigger.__sub_classes.append(cls)

    @staticmethod
    def sub_classes():
        return tuple(Trigger.__sub_classes)

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
        return self.trigger_requirements.has_triggered(state, backtest)

    def get_trigger_times(self):
        return self.trigger_requirements.get_trigger_times()

    @property
    def calc_type(self):
        return self.trigger_requirements.calc_type

    @property
    def risks(self):
        return [x.risk for x in make_list(self.actions) if x.risk is not None]


@dataclass_json
@dataclass
class PeriodicTrigger(Trigger):
    trigger_requirements: PeriodicTriggerRequirements = field(default=None, metadata=field_metadata)
    _trigger_dates = None
    class_type: str = static_field('periodic_trigger')


@dataclass_json
@dataclass
class IntradayPeriodicTrigger(Trigger):
    trigger_requirements: IntradayTriggerRequirements = field(default=None, metadata=field_metadata)
    class_type: str = static_field('intraday_periodic_trigger')


@dataclass_json
@dataclass
class MktTrigger(Trigger):
    trigger_requirements: MktTriggerRequirements = field(default=None, metadata=field_metadata)
    class_type: str = static_field('mkt_trigger')


@dataclass_json
@dataclass
class StrategyRiskTrigger(Trigger):
    trigger_requirements: RiskTriggerRequirements = field(default=None, metadata=field_metadata)
    class_type: str = static_field('strategy_risk_trigger')

    @property
    def risks(self):
        return [x.risk for x in make_list(self.actions) if x.risk is not None] + [self.trigger_requirements.risk]


@dataclass_json
@dataclass
class AggregateTrigger(Trigger):
    trigger_requirements: AggregateTriggerRequirements = field(default=None, metadata=field_metadata)
    class_type: str = static_field('aggregate_trigger')


@dataclass_json
@dataclass
class NotTrigger(Trigger):
    trigger_requirements: NotTriggerRequirements = field(default=None, metadata=field_metadata)
    class_type: str = static_field('not_trigger')


@dataclass_json
@dataclass
class DateTrigger(Trigger):
    trigger_requirements: DateTriggerRequirements = field(default=None, metadata=field_metadata)
    class_type: str = static_field('date_trigger')


@dataclass_json
@dataclass
class PortfolioTrigger(Trigger):
    trigger_requirements: PortfolioTriggerRequirements = field(default=None, metadata=field_metadata)
    class_type: str = static_field('portfolio_trigger')


@dataclass_json
@dataclass
class MeanReversionTrigger(Trigger):
    trigger_requirements: MeanReversionTriggerRequirements = field(default=None, metadata=field_metadata)
    class_type: str = static_field('mean_reversion_trigger')


@dataclass_json
@dataclass
class TradeCountTrigger(Trigger):
    trigger_requirements: TradeCountTriggerRequirements = field(default=None, metadata=field_metadata)
    class_type: str = static_field('trade_count_trigger')


@dataclass_json
@dataclass
class EventTrigger(Trigger):
    trigger_requirements: EventTriggerRequirements = field(default=None, metadata=field_metadata)
    class_type: str = static_field('event_trigger')


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


# These special trigger requirements have a special dependency on other trigger types
triggers_field = AggregateTriggerRequirements.__dataclass_fields__['triggers']
triggers_field.metadata = config(decoder=dc_decode(*TriggerRequirements.sub_classes(), allow_missing=True))

trigger_field = NotTriggerRequirements.__dataclass_fields__['trigger']
trigger_field.metadata = config(decoder=dc_decode(*TriggerRequirements.sub_classes(), allow_missing=True))
