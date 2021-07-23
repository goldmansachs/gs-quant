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


from typing import Optional
from gs_quant.backtests.actions import Action, AddTradeAction, AddTradeActionInfo
from gs_quant.backtests.backtest_objects import BackTest, PredefinedAssetBacktest
from gs_quant.backtests.backtest_utils import make_list, CalcType
from gs_quant.backtests.data_sources import *


class TriggerDirection(Enum):
    ABOVE = 1
    BELOW = 2
    EQUAL = 3


class TriggerRequirements(object):
    def __init__(self):
        pass


class PeriodicTriggerRequirements(TriggerRequirements):
    def __init__(self, start_date=None, end_date=None, frequency=None, calendar=None):
        super().__init__()
        self.start_date = start_date
        self.end_date = end_date
        self.frequency = frequency
        self.calendar = calendar


class IntradayTriggerRequirements(TriggerRequirements):
    def __init__(self, start_time, end_time, frequency):
        super().__init__()
        self.start_time = start_time
        self.end_time = end_time
        self.frequency = frequency


class MktTriggerRequirements(TriggerRequirements):
    def __init__(self, data_source, trigger_level, direction):
        super().__init__()
        self.data_source = data_source
        self.trigger_level = trigger_level
        self.direction = direction


class RiskTriggerRequirements(TriggerRequirements):
    def __init__(self, strategy_results, risk, trigger_level, direction):
        super().__init__()
        self.strategy_results = strategy_results
        self.risk = risk
        self.trigger_level = trigger_level
        self.direction = direction


class AggregateTriggerRequirements(TriggerRequirements):
    def __init__(self, triggers: Iterable[object]):
        super().__init__()
        self.triggers = triggers


class DateTriggerRequirements(TriggerRequirements):
    def __init__(self, dates: Iterable[dt.date]):
        """
        :param dates: the list of dates on which to trigger
        """
        self.dates = dates


class PortfolioTriggerRequirements(TriggerRequirements):
    def __init__(self, data_source: str, trigger_level: float, direction: TriggerDirection):
        """
        :param data_source: the portfolio property to check
        :param trigger_level: the threshold level on which to trigger
        :param direction: a direction for the trigger_level comparison
        """
        super().__init__()
        self.data_source = data_source
        self.trigger_level = trigger_level
        self.direction = direction


class MeanReversionTriggerRequirements(TriggerRequirements):
    def __init__(self, data_source: DataSource,
                 z_score_bound: float,
                 rolling_mean_window: int,
                 rolling_std_window: int):
        """
        This trigger will sell when the value hits the z score threshold on the up side, will close out a position
        when the value crosses the rolling_mean and buy when the value hits the z score threshold on the down side.

        :param data_source: the asset values
        :param z_score_bound: the threshold level on which to trigger
        :param rolling_mean_window: the number of values to consider when calculating the rolling mean
        :param rolling_std_window: the number of values to consider when calculating the standard deviation
        """
        super().__init__()
        self.data_source = data_source
        self.z_score_bound = z_score_bound
        self.rolling_mean_window = rolling_mean_window
        self.rolling_std_window = rolling_std_window


class TriggerInfo(object):
    def __init__(self, triggered: bool, info_dict: Optional[dict] = None):
        self.triggered = triggered
        self.info_dict = info_dict

    def __eq__(self, other):
        return self.triggered is other

    def __bool__(self):
        return self.triggered


class Trigger(object):

    def __init__(self, trigger_requirements: Optional[TriggerRequirements], actions: Union[Action, Iterable[Action]]):
        self._trigger_requirements = trigger_requirements
        self._actions = make_list(actions)
        self._risks = [x.risk for x in self.actions if x.risk is not None]
        self._calc_type = CalcType.simple

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

    @property
    def calc_type(self):
        return self._calc_type

    @property
    def actions(self):
        return self._actions

    @property
    def trigger_requirements(self):
        return self._trigger_requirements

    @property
    def risks(self):
        return self._risks


class PeriodicTrigger(Trigger):
    def __init__(self,
                 trigger_requirements: PeriodicTriggerRequirements,
                 actions: Union[Action, Iterable[Action]]):
        super().__init__(trigger_requirements, actions)
        self._trigger_dates = None

    def get_trigger_dates(self) -> [dt.date]:
        if not self._trigger_dates:
            self._trigger_dates = self._trigger_requirements.dates if \
                hasattr(self._trigger_requirements, 'dates') else \
                pd.date_range(start=self._trigger_requirements.start_date,
                              end=self._trigger_requirements.end_date,
                              freq=self._trigger_requirements.frequency).date.tolist()
        return self._trigger_dates

    def has_triggered(self, state: dt.date, backtest: BackTest = None) -> TriggerInfo:
        if not self._trigger_dates:
            self.get_trigger_dates()
        return TriggerInfo(state in self._trigger_dates)


class IntradayPeriodicTrigger(Trigger):
    def __init__(self,
                 trigger_requirements: IntradayTriggerRequirements,
                 actions: Union[Action, Iterable[Action]]):
        super().__init__(trigger_requirements, actions)

        # generate all the trigger times
        start = trigger_requirements.start_time
        end = trigger_requirements.end_time
        freq = trigger_requirements.frequency

        self._trigger_times = []
        time = start
        while time <= end:
            self._trigger_times.append(time)
            time = (dt.datetime.combine(dt.date.today(), time) + dt.timedelta(minutes=freq)).time()

    def get_trigger_times(self):
        return self._trigger_times

    def has_triggered(self, state: Union[dt.date, dt.datetime], backtest: BackTest = None) -> TriggerInfo:
        return TriggerInfo(state.time() in self._trigger_times)


class MktTrigger(Trigger):
    def __init__(self,
                 trigger_requirements: MktTriggerRequirements,
                 actions: Union[Action, Iterable[Action]]):
        super().__init__(trigger_requirements, actions)

    def has_triggered(self, state: dt.date, backtest: BackTest = None) -> TriggerInfo:
        data_value = self._trigger_requirements.data_source.get_data(state)
        if self._trigger_requirements.direction == TriggerDirection.ABOVE:
            if data_value > self._trigger_requirements.trigger_level:
                return TriggerInfo(True)
        elif self._trigger_requirements.direction == TriggerDirection.BELOW:
            if data_value < self._trigger_requirements.trigger_level:
                return TriggerInfo(True)
        else:
            if data_value == self._trigger_requirements.trigger_level:
                return TriggerInfo(True)
        return TriggerInfo(False)


class StrategyRiskTrigger(Trigger):
    def __init__(self,
                 trigger_requirements: RiskTriggerRequirements,
                 actions: Union[Action, Iterable[Action]]):
        super().__init__(trigger_requirements, actions)
        self._calc_type = CalcType.path_dependent
        self._risks += [trigger_requirements.risk]

    def has_triggered(self, state: dt.date, backtest: BackTest = None) -> TriggerInfo:
        risk_value = backtest[state][self._trigger_requirements.risk]
        if self._trigger_requirements.direction == TriggerDirection.ABOVE:
            if risk_value > self._trigger_requirements.trigger_level:
                return TriggerInfo(True)
        elif self._trigger_requirements.direction == TriggerDirection.BELOW:
            if risk_value < self._trigger_requirements.trigger_level:
                return TriggerInfo(True)
        else:
            if risk_value == self._trigger_requirements.trigger_level:
                return TriggerInfo(True)
        return TriggerInfo(False)


class AggregateTrigger(Trigger):
    def __init__(self, triggers: Iterable[Trigger]):
        actions = []
        for t in triggers:
            actions += [action for action in t.actions]
        super().__init__(AggregateTriggerRequirements(triggers), actions)
        self._triggers = triggers

    def has_triggered(self, state: dt.date, backtest: BackTest = None) -> TriggerInfo:
        for trigger in self._trigger_requirements.triggers:
            if not trigger.has_triggered(state, backtest):
                return TriggerInfo(False)
        return TriggerInfo(True)

    @property
    def triggers(self) -> Iterable[Trigger]:
        return self._triggers


class DateTrigger(Trigger):
    def __init__(self, trigger_requirements: DateTriggerRequirements, actions: Iterable[Action]):
        super().__init__(trigger_requirements, actions)

    def has_triggered(self, state: dt.date, backtest: BackTest = None) -> TriggerInfo:
        return TriggerInfo(state in self._trigger_requirements.dates)


class PortfolioTrigger(Trigger):
    def __init__(self, trigger_requirements: PortfolioTriggerRequirements, actions: Iterable[Action] = None):
        super().__init__(trigger_requirements, actions)

    def has_triggered(self, state: dt.date, backtest: BackTest = None) -> TriggerInfo:
        if self._trigger_requirements.data_source == 'len':
            value = len(backtest.portfolio_dict)
            if self._trigger_requirements.direction == TriggerDirection.ABOVE:
                if value > self._trigger_requirements.trigger_level:
                    return TriggerInfo(True)
            elif self._trigger_requirements.direction == TriggerDirection.BELOW:
                if value < self._trigger_requirements.trigger_level:
                    return TriggerInfo(True)
            else:
                if value == self._trigger_requirements.trigger_level:
                    return TriggerInfo(True)

        return TriggerInfo(False)


class MeanReversionTrigger(Trigger):
    def __init__(self,
                 trigger_requirements: MeanReversionTriggerRequirements,
                 actions: Union[Action, Iterable[Action]]):
        super().__init__(trigger_requirements, actions)
        self._current_position = 0

    def has_triggered(self, state: dt.date, backtest: BackTest = None) -> TriggerInfo:
        trigger_req = self._trigger_requirements
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


class OrdersGeneratorTrigger(Trigger):
    """Base class for triggers used with the PredefinedAssetEngine."""
    def __init__(self):
        super().__init__(None, Action())

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
