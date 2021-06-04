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

from gs_quant.common import *
import datetime
from typing import Mapping, Tuple, Union, Optional
from enum import Enum
from gs_quant.base import Base, EnumBase, InstrumentBase, camel_case_translate, get_enum_value


class BacktestRiskMeasureType(EnumBase, Enum):    
    
    """The type of measure to perform risk on. e.g. Greeks"""

    Price = 'Price'
    Delta = 'Delta'
    Gamma = 'Gamma'
    Vega = 'Vega'
    Forward = 'Forward'
    Implied_Volatility = 'Implied Volatility'
    Fair_Variance = 'Fair Variance'
    Strike_Level = 'Strike Level'    


class BacktestTradingQuantityType(EnumBase, Enum):    
    
    """The trading quantity unit of a backtest strategy"""

    notional = 'notional'
    quantity = 'quantity'
    vega = 'vega'
    gamma = 'gamma'
    NAV = 'NAV'    


class BacktestType(EnumBase, Enum):    
    
    """Backtest type differentiates the backtest type."""

    Basket = 'Basket'
    Volatility = 'Volatility'
    Volatility_Flow = 'Volatility Flow'
    Enhanced_Beta = 'Enhanced Beta'
    ISelect = 'ISelect'    


class EquityMarketModel(EnumBase, Enum):    
    
    """Market model for pricing"""

    SFK = 'SFK'
    SD = 'SD'    


class FlowVolBacktestMeasure(EnumBase, Enum):    
    
    """Metric which can be calculated using Flow Vol. Backtester"""

    ALL_MEASURES = 'ALL MEASURES'
    PNL_spot = 'PNL_spot'
    PNL_vol = 'PNL_vol'
    PNL_carry = 'PNL_carry'
    PNL_delta = 'PNL_delta'
    PNL_gamma = 'PNL_gamma'
    PNL_higher_order_spot = 'PNL_higher_order_spot'
    PNL_higher_order_vol = 'PNL_higher_order_vol'
    PNL_theta = 'PNL_theta'
    Total = 'Total'
    transaction_costs = 'transaction_costs'
    PNL_unexplained = 'PNL_unexplained'
    PNL_vega = 'PNL_vega'
    PNL = 'PNL'
    delta = 'delta'
    gamma = 'gamma'
    vega = 'vega'
    portfolio = 'portfolio'
    NAV = 'NAV'    


class BacktestComparison(Base):
        
    """Comparison object for backtests"""

    @camel_case_translate
    def __init__(
        self,
        id_: str = None,
        correlation: float = None,
        name: str = None
    ):        
        super().__init__()
        self.__id = id_
        self.correlation = correlation
        self.name = name

    @property
    def id(self) -> str:
        """Marquee unique identifier for the comparison asset or backtest"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def correlation(self) -> float:
        """Correlation between the comparison entity and the backtest"""
        return self.__correlation

    @correlation.setter
    def correlation(self, value: float):
        self._property_changed('correlation')
        self.__correlation = value        


class BacktestRebalanceParameters(Base):
        
    """Parameters relating to the backtest's rebalance"""

    @camel_case_translate
    def __init__(
        self,
        frequency_period: str = None,
        frequency: int = None,
        day_of_week: str = None,
        day_of_month: float = None,
        name: str = None
    ):        
        super().__init__()
        self.frequency_period = frequency_period
        self.frequency = frequency
        self.day_of_week = day_of_week
        self.day_of_month = day_of_month
        self.name = name

    @property
    def frequency_period(self) -> str:
        """What frequency period should be used for the rebalance"""
        return self.__frequency_period

    @frequency_period.setter
    def frequency_period(self, value: str):
        self._property_changed('frequency_period')
        self.__frequency_period = value        

    @property
    def frequency(self) -> int:
        """What the frequency should be, given the frequency period, i.e. every 2 weeks"""
        return self.__frequency

    @frequency.setter
    def frequency(self, value: int):
        self._property_changed('frequency')
        self.__frequency = value        

    @property
    def day_of_week(self) -> str:
        """For weekly frequencyPeriod, the day of the week the rebalance should occur"""
        return self.__day_of_week

    @day_of_week.setter
    def day_of_week(self, value: str):
        self._property_changed('day_of_week')
        self.__day_of_week = value        

    @property
    def day_of_month(self) -> float:
        """For monthly frequencyPeriod rebalances, the day of the month the rebalance
           should occur"""
        return self.__day_of_month

    @day_of_month.setter
    def day_of_month(self, value: float):
        self._property_changed('day_of_month')
        self.__day_of_month = value        


class BacktestSignalSeriesItem(Base):
        
    """A backtest signal series item consisting of a date and boolean"""

    @camel_case_translate
    def __init__(
        self,
        date: datetime.date = None,
        value: bool = None,
        name: str = None
    ):        
        super().__init__()
        self.date = date
        self.value = value
        self.name = name

    @property
    def date(self) -> datetime.date:
        """Date on which the signal applies"""
        return self.__date

    @date.setter
    def date(self, value: datetime.date):
        self._property_changed('date')
        self.__date = value        

    @property
    def value(self) -> bool:
        """Whether the signal should be evaluated or not"""
        return self.__value

    @value.setter
    def value(self, value: bool):
        self._property_changed('value')
        self.__value = value        


class BaseIndexRefData(Base):
        
    """Base index reference data object."""

    @camel_case_translate
    def __init__(
        self,
        default: str = None,
        enum: Tuple[str, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.default = default
        self.enum = enum
        self.name = name

    @property
    def default(self) -> str:
        """Default asset id of base index"""
        return self.__default

    @default.setter
    def default(self, value: str):
        self._property_changed('default')
        self.__default = value        

    @property
    def enum(self) -> Tuple[str, ...]:
        """Base Indices Allowed"""
        return self.__enum

    @enum.setter
    def enum(self, value: Tuple[str, ...]):
        self._property_changed('enum')
        self.__enum = value        


class BuySellRefData(Base):
        
    """Buy Sell reference data object."""

    @camel_case_translate
    def __init__(
        self,
        default: str = None,
        enum: Tuple[str, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.default = default
        self.enum = enum
        self.name = name

    @property
    def default(self) -> str:
        """Default Buy/Sell parameter."""
        return self.__default

    @default.setter
    def default(self, value: str):
        self._property_changed('default')
        self.__default = value        

    @property
    def enum(self) -> Tuple[str, ...]:
        """Buy/Sell parameters allowed."""
        return self.__enum

    @enum.setter
    def enum(self, value: Tuple[str, ...]):
        self._property_changed('enum')
        self.__enum = value        


class DeltaHedgeParameters(Base):
        
    """Parameters for delta hedging a backtest strategy"""

    @camel_case_translate
    def __init__(
        self,
        frequency: str,
        fixing_time: str = None,
        notional: float = None,
        name: str = None
    ):        
        super().__init__()
        self.fixing_time = fixing_time
        self.frequency = frequency
        self.notional = notional
        self.name = name

    @property
    def delta_type(self) -> str:
        """Details of how to compute delta"""
        return 'BlackScholes'        

    @property
    def fixing_time(self) -> str:
        """When the leg is hedged, i.e End of Day (EOD)."""
        return self.__fixing_time

    @fixing_time.setter
    def fixing_time(self, value: str):
        self._property_changed('fixing_time')
        self.__fixing_time = value        

    @property
    def frequency(self) -> str:
        """What frequency the leg is hedged."""
        return self.__frequency

    @frequency.setter
    def frequency(self, value: str):
        self._property_changed('frequency')
        self.__frequency = value        

    @property
    def notional(self) -> float:
        """Notional to delta hedge the underlier"""
        return self.__notional

    @notional.setter
    def notional(self, value: float):
        self._property_changed('notional')
        self.__notional = value        


class DeltaHedgingParameters(Base):
        
    """Parameters for delta hedging an option."""

    @camel_case_translate
    def __init__(
        self,
        enabled: bool,
        frequency: str,
        fixing_time: str,
        notional_percentage: float,
        name: str = None
    ):        
        super().__init__()
        self.enabled = enabled
        self.fixing_time = fixing_time
        self.frequency = frequency
        self.notional_percentage = notional_percentage
        self.name = name

    @property
    def enabled(self) -> bool:
        """Whether the leg is being hedged."""
        return self.__enabled

    @enabled.setter
    def enabled(self, value: bool):
        self._property_changed('enabled')
        self.__enabled = value        

    @property
    def fixing_time(self) -> str:
        """When the leg is hedged, i.e End of Day (EOD)."""
        return self.__fixing_time

    @fixing_time.setter
    def fixing_time(self, value: str):
        self._property_changed('fixing_time')
        self.__fixing_time = value        

    @property
    def frequency(self) -> str:
        """What frequency the leg is hedged."""
        return self.__frequency

    @frequency.setter
    def frequency(self, value: str):
        self._property_changed('frequency')
        self.__frequency = value        

    @property
    def notional_percentage(self) -> float:
        """Percentage of notional to hedge."""
        return self.__notional_percentage

    @notional_percentage.setter
    def notional_percentage(self, value: float):
        self._property_changed('notional_percentage')
        self.__notional_percentage = value        


class EnhancedBetaUnderlier(Base):
        
    """Underlying asset and corresponding nearby adder and valid months"""

    @camel_case_translate
    def __init__(
        self,
        asset_id: str,
        month_add: float = None,
        valid_months: Tuple[str, ...] = None,
        is_included: bool = None,
        weight_scale: float = None,
        name: str = None
    ):        
        super().__init__()
        self.asset_id = asset_id
        self.month_add = month_add
        self.valid_months = valid_months
        self.is_included = is_included
        self.weight_scale = weight_scale
        self.name = name

    @property
    def asset_id(self) -> str:
        """Marquee unique asset identifier."""
        return self.__asset_id

    @asset_id.setter
    def asset_id(self, value: str):
        self._property_changed('asset_id')
        self.__asset_id = value        

    @property
    def month_add(self) -> float:
        """Allows users to roll to a contract farther in the future by the number of months
           specified."""
        return self.__month_add

    @month_add.setter
    def month_add(self, value: float):
        self._property_changed('month_add')
        self.__month_add = value        

    @property
    def valid_months(self) -> Tuple[str, ...]:
        """Valid months to which you can roll contracts."""
        return self.__valid_months

    @valid_months.setter
    def valid_months(self, value: Tuple[str, ...]):
        self._property_changed('valid_months')
        self.__valid_months = value        

    @property
    def is_included(self) -> bool:
        """True if underlier is included in user's strategy."""
        return self.__is_included

    @is_included.setter
    def is_included(self, value: bool):
        self._property_changed('is_included')
        self.__is_included = value        

    @property
    def weight_scale(self) -> float:
        """The percentage the underlier's weight is scaled."""
        return self.__weight_scale

    @weight_scale.setter
    def weight_scale(self, value: float):
        self._property_changed('weight_scale')
        self.__weight_scale = value        


class EnhancedBetaUnderlierRefData(Base):
        
    """Enhanced Beta Underlier reference data object."""

    @camel_case_translate
    def __init__(
        self,
        asset_id: str = None,
        valid_months: Tuple[str, ...] = None,
        current: bool = None,
        name: str = None
    ):        
        super().__init__()
        self.asset_id = asset_id
        self.valid_months = valid_months
        self.current = current
        self.name = name

    @property
    def asset_id(self) -> str:
        """Marquee unique asset identifier."""
        return self.__asset_id

    @asset_id.setter
    def asset_id(self, value: str):
        self._property_changed('asset_id')
        self.__asset_id = value        

    @property
    def valid_months(self) -> Tuple[str, ...]:
        """Valid months with contracts you can roll to"""
        return self.__valid_months

    @valid_months.setter
    def valid_months(self, value: Tuple[str, ...]):
        self._property_changed('valid_months')
        self.__valid_months = value        

    @property
    def current(self) -> bool:
        """True when underlier is currently in the base index, else false."""
        return self.__current

    @current.setter
    def current(self, value: bool):
        self._property_changed('current')
        self.__current = value        


class EntityCorrelation(Base):
        
    """entity correlation"""

    @camel_case_translate
    def __init__(
        self,
        primary_id: str = None,
        secondary_id: str = None,
        correlation: float = None,
        name: str = None
    ):        
        super().__init__()
        self.primary_id = primary_id
        self.secondary_id = secondary_id
        self.correlation = correlation
        self.name = name

    @property
    def primary_id(self) -> str:
        """Marquee unique identifier for the primary underlying asset in the correlation"""
        return self.__primary_id

    @primary_id.setter
    def primary_id(self, value: str):
        self._property_changed('primary_id')
        self.__primary_id = value        

    @property
    def secondary_id(self) -> str:
        """Marquee unique identifier for the secondary underlying asset in the correlation"""
        return self.__secondary_id

    @secondary_id.setter
    def secondary_id(self, value: str):
        self._property_changed('secondary_id')
        self.__secondary_id = value        

    @property
    def correlation(self) -> float:
        """Correlation between the primary and secondary underliers"""
        return self.__correlation

    @correlation.setter
    def correlation(self, value: float):
        self._property_changed('correlation')
        self.__correlation = value        


class ExpirationRefData(Base):
        
    """Expiration reference data object."""

    @camel_case_translate
    def __init__(
        self,
        default: str = None,
        enum: Tuple[str, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.default = default
        self.enum = enum
        self.name = name

    @property
    def default(self) -> str:
        """Default option expiration."""
        return self.__default

    @default.setter
    def default(self, value: str):
        self._property_changed('default')
        self.__default = value        

    @property
    def enum(self) -> Tuple[str, ...]:
        """Option expirations allowed."""
        return self.__enum

    @enum.setter
    def enum(self, value: Tuple[str, ...]):
        self._property_changed('enum')
        self.__enum = value        


class FixingTimeRefData(Base):
        
    """Fixing Time reference data object."""

    @camel_case_translate
    def __init__(
        self,
        default: str = None,
        enum: Tuple[str, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.default = default
        self.enum = enum
        self.name = name

    @property
    def default(self) -> str:
        """Default hedge fixing time."""
        return self.__default

    @default.setter
    def default(self, value: str):
        self._property_changed('default')
        self.__default = value        

    @property
    def enum(self) -> Tuple[str, ...]:
        """Fixing times allowed."""
        return self.__enum

    @enum.setter
    def enum(self, value: Tuple[str, ...]):
        self._property_changed('enum')
        self.__enum = value        


class FrequencyRefData(Base):
        
    """Frequency reference data object."""

    @camel_case_translate
    def __init__(
        self,
        default: str = None,
        enum: Tuple[str, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.default = default
        self.enum = enum
        self.name = name

    @property
    def default(self) -> str:
        """Default hedge fixing time."""
        return self.__default

    @default.setter
    def default(self, value: str):
        self._property_changed('default')
        self.__default = value        

    @property
    def enum(self) -> Tuple[str, ...]:
        """Fixing times allowed."""
        return self.__enum

    @enum.setter
    def enum(self, value: Tuple[str, ...]):
        self._property_changed('enum')
        self.__enum = value        


class HistoricalUnderlier(Base):
        
    """Underlying asset only without any other info"""

    @camel_case_translate
    def __init__(
        self,
        asset_id: str,
        weight: float = None,
        date: str = None,
        name: str = None
    ):        
        super().__init__()
        self.asset_id = asset_id
        self.weight = weight
        self.date = date
        self.name = name

    @property
    def asset_id(self) -> str:
        """Marquee unique asset identifier."""
        return self.__asset_id

    @asset_id.setter
    def asset_id(self, value: str):
        self._property_changed('asset_id')
        self.__asset_id = value        

    @property
    def weight(self) -> float:
        """Weight as a percentage of notional assigned to the underlier for a particular
           date"""
        return self.__weight

    @weight.setter
    def weight(self, value: float):
        self._property_changed('weight')
        self.__weight = value        

    @property
    def date(self) -> str:
        """Date to apply the weight for a particular underlier"""
        return self.__date

    @date.setter
    def date(self, value: str):
        self._property_changed('date')
        self.__date = value        


class LookBackPeriodRefData(Base):
        
    """Look back period reference data object."""

    @camel_case_translate
    def __init__(
        self,
        default: str = None,
        enum: Tuple[str, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.default = default
        self.enum = enum
        self.name = name

    @property
    def default(self) -> str:
        """Default look back period."""
        return self.__default

    @default.setter
    def default(self, value: str):
        self._property_changed('default')
        self.__default = value        

    @property
    def enum(self) -> Tuple[str, ...]:
        """Look back periods allowed."""
        return self.__enum

    @enum.setter
    def enum(self, value: Tuple[str, ...]):
        self._property_changed('enum')
        self.__enum = value        


class NotionalPercentageRefData(Base):
        
    """Notional Percentage Reference Data"""

    @camel_case_translate
    def __init__(
        self,
        default: float = None,
        min_: float = None,
        max_: float = None,
        name: str = None
    ):        
        super().__init__()
        self.default = default
        self.__min = min_
        self.__max = max_
        self.name = name

    @property
    def default(self) -> float:
        """Default notional percentage."""
        return self.__default

    @default.setter
    def default(self, value: float):
        self._property_changed('default')
        self.__default = value        

    @property
    def min(self) -> float:
        """Minimum notional percentage allowed."""
        return self.__min

    @min.setter
    def min(self, value: float):
        self._property_changed('min')
        self.__min = value        

    @property
    def max(self) -> float:
        """Maximum notional percentage allowed."""
        return self.__max

    @max.setter
    def max(self, value: float):
        self._property_changed('max')
        self.__max = value        


class OptionStrikeTypeRefData(Base):
        
    """Option strike type reference data object."""

    @camel_case_translate
    def __init__(
        self,
        default: str = None,
        enum: Tuple[str, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.default = default
        self.enum = enum
        self.name = name

    @property
    def default(self) -> str:
        """Default option strike type."""
        return self.__default

    @default.setter
    def default(self, value: str):
        self._property_changed('default')
        self.__default = value        

    @property
    def enum(self) -> Tuple[str, ...]:
        """Option strike types allowed."""
        return self.__enum

    @enum.setter
    def enum(self, value: Tuple[str, ...]):
        self._property_changed('enum')
        self.__enum = value        


class OptionTypeRefData(Base):
        
    """Option Type reference data object."""

    @camel_case_translate
    def __init__(
        self,
        default: str = None,
        enum: Tuple[str, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.default = default
        self.enum = enum
        self.name = name

    @property
    def default(self) -> str:
        """Default option type."""
        return self.__default

    @default.setter
    def default(self, value: str):
        self._property_changed('default')
        self.__default = value        

    @property
    def enum(self) -> Tuple[str, ...]:
        """Option types allowed."""
        return self.__enum

    @enum.setter
    def enum(self, value: Tuple[str, ...]):
        self._property_changed('enum')
        self.__enum = value        


class ScalingMethodRefData(Base):
        
    """Scaling Method Reference Data"""

    @camel_case_translate
    def __init__(
        self,
        default: str = None,
        enum: Tuple[str, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.default = default
        self.enum = enum
        self.name = name

    @property
    def default(self) -> str:
        """Default scaling method."""
        return self.__default

    @default.setter
    def default(self, value: str):
        self._property_changed('default')
        self.__default = value        

    @property
    def enum(self) -> Tuple[str, ...]:
        """Scaling methods allowed."""
        return self.__enum

    @enum.setter
    def enum(self, value: Tuple[str, ...]):
        self._property_changed('enum')
        self.__enum = value        


class StrikeRefData(Base):
        
    """Strike reference data object."""

    @camel_case_translate
    def __init__(
        self,
        default: float = None,
        min_: float = None,
        max_: float = None,
        name: str = None
    ):        
        super().__init__()
        self.default = default
        self.__min = min_
        self.__max = max_
        self.name = name

    @property
    def default(self) -> float:
        """Default strike."""
        return self.__default

    @default.setter
    def default(self, value: float):
        self._property_changed('default')
        self.__default = value        

    @property
    def min(self) -> float:
        """Minimum strike allowed."""
        return self.__min

    @min.setter
    def min(self, value: float):
        self._property_changed('min')
        self.__min = value        

    @property
    def max(self) -> float:
        """Maximum strike allowed."""
        return self.__max

    @max.setter
    def max(self, value: float):
        self._property_changed('max')
        self.__max = value        


class TradeInMethodRefData(Base):
        
    """Trade In Method Reference Data"""

    @camel_case_translate
    def __init__(
        self,
        default: str = None,
        enum: Tuple[str, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.default = default
        self.enum = enum
        self.name = name

    @property
    def default(self) -> str:
        """Default trade in method."""
        return self.__default

    @default.setter
    def default(self, value: str):
        self._property_changed('default')
        self.__default = value        

    @property
    def enum(self) -> Tuple[str, ...]:
        """Trade in methods allowed."""
        return self.__enum

    @enum.setter
    def enum(self, value: Tuple[str, ...]):
        self._property_changed('enum')
        self.__enum = value        


class TradeInTimeRefData(Base):
        
    """Trade In Time Reference Data"""

    @camel_case_translate
    def __init__(
        self,
        default: str = None,
        enum: Tuple[str, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.default = default
        self.enum = enum
        self.name = name

    @property
    def default(self) -> str:
        """Default trade in time."""
        return self.__default

    @default.setter
    def default(self, value: str):
        self._property_changed('default')
        self.__default = value        

    @property
    def enum(self) -> Tuple[str, ...]:
        """Trade in times allowed."""
        return self.__enum

    @enum.setter
    def enum(self, value: Tuple[str, ...]):
        self._property_changed('enum')
        self.__enum = value        


class VolatilityWeightedWeightingModifier(Base):
        
    """Volatility Weighted backtest weighting modifier."""

    _name_mappings = {'em_aalpha': 'EMAalpha'}

    @camel_case_translate
    def __init__(
        self,
        em_aalpha: float = None,
        look_back_period: str = None,
        use_log_return: bool = False
    ):        
        super().__init__()
        self.em_aalpha = em_aalpha
        self.look_back_period = look_back_period
        self.use_log_return = use_log_return

    @property
    def name(self) -> str:
        """Name of the Modifier"""
        return 'Volatility Weighted'        

    @property
    def em_aalpha(self) -> float:
        """Alpha value for Exponentially Weighted Moving Average Volatility; set to 0 if
           standard volatility."""
        return self.__em_aalpha

    @em_aalpha.setter
    def em_aalpha(self, value: float):
        self._property_changed('em_aalpha')
        self.__em_aalpha = value        

    @property
    def look_back_period(self) -> str:
        """Look back period to measure volatility for each underlier."""
        return self.__look_back_period

    @look_back_period.setter
    def look_back_period(self, value: str):
        self._property_changed('look_back_period')
        self.__look_back_period = value        

    @property
    def use_log_return(self) -> bool:
        """Whether to use Log Returns instead of Arithmetic Returns for volatility
           calculation."""
        return self.__use_log_return

    @use_log_return.setter
    def use_log_return(self, value: bool):
        self._property_changed('use_log_return')
        self.__use_log_return = value        


class VolatilityWeightedWeightingModifierRefData(Base):
        
    """Volatility Weighted Weighting Modifier reference data object."""

    _name_mappings = {'em_aalpha': 'EMAalpha'}

    @camel_case_translate
    def __init__(
        self,
        em_aalpha: dict = None,
        look_back_period: dict = None,
        name: str = None
    ):        
        super().__init__()
        self.em_aalpha = em_aalpha
        self.look_back_period = look_back_period
        self.name = name

    @property
    def em_aalpha(self) -> dict:
        """Alpha value for Exponentially Weighted Moving Average Volatility reference data
           object."""
        return self.__em_aalpha

    @em_aalpha.setter
    def em_aalpha(self, value: dict):
        self._property_changed('em_aalpha')
        self.__em_aalpha = value        

    @property
    def look_back_period(self) -> dict:
        """Lookback period to measure volatility for each underlier reference data object."""
        return self.__look_back_period

    @look_back_period.setter
    def look_back_period(self, value: dict):
        self._property_changed('look_back_period')
        self.__look_back_period = value        


class BacktestStrategyUnderlierHedge(Base):
        
    """Hedge information for the backtest underlier"""

    @camel_case_translate
    def __init__(
        self,
        risk_details: DeltaHedgeParameters = None,
        quantity_percentage: float = None,
        name: str = None
    ):        
        super().__init__()
        self.risk_details = risk_details
        self.quantity_percentage = quantity_percentage
        self.name = name

    @property
    def risk_details(self) -> DeltaHedgeParameters:
        """details of the risk being hedged"""
        return self.__risk_details

    @risk_details.setter
    def risk_details(self, value: DeltaHedgeParameters):
        self._property_changed('risk_details')
        self.__risk_details = value        

    @property
    def quantity_percentage(self) -> float:
        """Percentage of quantity to hedge"""
        return self.__quantity_percentage

    @quantity_percentage.setter
    def quantity_percentage(self, value: float):
        self._property_changed('quantity_percentage')
        self.__quantity_percentage = value        


class BacktestTradingParameters(Base):
        
    """Trading Information for the Backtesting Strategy"""

    @camel_case_translate
    def __init__(
        self,
        quantity_type: Union[BacktestTradingQuantityType, str] = None,
        quantity: float = None,
        trade_in_method: str = None,
        roll_frequency: str = None,
        roll_date_mode: str = None,
        scaling_method: str = None,
        trade_in_signals: Tuple[BacktestSignalSeriesItem, ...] = None,
        trade_out_signals: Tuple[BacktestSignalSeriesItem, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.quantity_type = quantity_type
        self.quantity = quantity
        self.trade_in_method = trade_in_method
        self.roll_frequency = roll_frequency
        self.roll_date_mode = roll_date_mode
        self.scaling_method = scaling_method
        self.trade_in_signals = trade_in_signals
        self.trade_out_signals = trade_out_signals
        self.name = name

    @property
    def quantity_type(self) -> Union[BacktestTradingQuantityType, str]:
        """The trading quantity unit of a backtest strategy"""
        return self.__quantity_type

    @quantity_type.setter
    def quantity_type(self, value: Union[BacktestTradingQuantityType, str]):
        self._property_changed('quantity_type')
        self.__quantity_type = get_enum_value(BacktestTradingQuantityType, value)        

    @property
    def quantity(self) -> float:
        """The quantity of backtest strategy"""
        return self.__quantity

    @quantity.setter
    def quantity(self, value: float):
        self._property_changed('quantity')
        self.__quantity = value        

    @property
    def trade_in_method(self) -> str:
        """Roll method for the backtest strategy"""
        return self.__trade_in_method

    @trade_in_method.setter
    def trade_in_method(self, value: str):
        self._property_changed('trade_in_method')
        self.__trade_in_method = value        

    @property
    def roll_frequency(self) -> str:
        """Period the strategy rolls"""
        return self.__roll_frequency

    @roll_frequency.setter
    def roll_frequency(self, value: str):
        self._property_changed('roll_frequency')
        self.__roll_frequency = value        

    @property
    def roll_date_mode(self) -> str:
        """Roll date mode to be used in the backtest strategy e.g. listed."""
        return self.__roll_date_mode

    @roll_date_mode.setter
    def roll_date_mode(self, value: str):
        self._property_changed('roll_date_mode')
        self.__roll_date_mode = value        

    @property
    def scaling_method(self) -> str:
        """The method for scaling underliers, i.e fixedQuantity"""
        return self.__scaling_method

    @scaling_method.setter
    def scaling_method(self, value: str):
        self._property_changed('scaling_method')
        self.__scaling_method = value        

    @property
    def trade_in_signals(self) -> Tuple[BacktestSignalSeriesItem, ...]:
        """Set of dates to define if trade in signal is enabled/disabled"""
        return self.__trade_in_signals

    @trade_in_signals.setter
    def trade_in_signals(self, value: Tuple[BacktestSignalSeriesItem, ...]):
        self._property_changed('trade_in_signals')
        self.__trade_in_signals = value        

    @property
    def trade_out_signals(self) -> Tuple[BacktestSignalSeriesItem, ...]:
        """Set of dates to define if trade out signal is enabled/disabled"""
        return self.__trade_out_signals

    @trade_out_signals.setter
    def trade_out_signals(self, value: Tuple[BacktestSignalSeriesItem, ...]):
        self._property_changed('trade_out_signals')
        self.__trade_out_signals = value        


class BasketBacktestParameters(Base):
        
    """Parameters of a Basket backtest."""

    @camel_case_translate
    def __init__(
        self,
        underliers: Tuple[Union[float, str], ...],
        rebalance_parameters: BacktestRebalanceParameters = None,
        weighting_modifiers: Tuple[VolatilityWeightedWeightingModifier, ...] = None,
        weighting_strategy: str = None,
        name: str = None
    ):        
        super().__init__()
        self.rebalance_parameters = rebalance_parameters
        self.underliers = underliers
        self.weighting_modifiers = weighting_modifiers
        self.weighting_strategy = weighting_strategy
        self.name = name

    @property
    def rebalance_parameters(self) -> BacktestRebalanceParameters:
        """Parameters relating to the backtest's rebalance"""
        return self.__rebalance_parameters

    @rebalance_parameters.setter
    def rebalance_parameters(self, value: BacktestRebalanceParameters):
        self._property_changed('rebalance_parameters')
        self.__rebalance_parameters = value        

    @property
    def underliers(self) -> Tuple[Union[float, str], ...]:
        """Underlying assets for the backtest"""
        return self.__underliers

    @underliers.setter
    def underliers(self, value: Tuple[Union[float, str], ...]):
        self._property_changed('underliers')
        self.__underliers = value        

    @property
    def weighting_modifiers(self) -> Tuple[VolatilityWeightedWeightingModifier, ...]:
        """Weighting modifiers for the backtest."""
        return self.__weighting_modifiers

    @weighting_modifiers.setter
    def weighting_modifiers(self, value: Tuple[VolatilityWeightedWeightingModifier, ...]):
        self._property_changed('weighting_modifiers')
        self.__weighting_modifiers = value        

    @property
    def weighting_strategy(self) -> str:
        """Strategy for determining the weight of the backtest underliers."""
        return self.__weighting_strategy

    @weighting_strategy.setter
    def weighting_strategy(self, value: str):
        self._property_changed('weighting_strategy')
        self.__weighting_strategy = value        


class CurrencyRefData(Base):
        
    """Currency Reference Data"""

    @camel_case_translate
    def __init__(
        self,
        default: Union[Currency, str] = None,
        enum: Tuple[Union[Currency, str], ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.default = default
        self.enum = enum
        self.name = name

    @property
    def default(self) -> Union[Currency, str]:
        """Default currency."""
        return self.__default

    @default.setter
    def default(self, value: Union[Currency, str]):
        self._property_changed('default')
        self.__default = get_enum_value(Currency, value)        

    @property
    def enum(self) -> Tuple[Union[Currency, str], ...]:
        """All currencies allowed."""
        return self.__enum

    @enum.setter
    def enum(self, value: Tuple[Union[Currency, str], ...]):
        self._property_changed('enum')
        self.__enum = value        


class DeltaHedgingRefData(Base):
        
    """Delta Hedging Reference Data"""

    @camel_case_translate
    def __init__(
        self,
        fixing_time: FixingTimeRefData = None,
        frequency: FrequencyRefData = None,
        notional_percentage: NotionalPercentageRefData = None,
        name: str = None
    ):        
        super().__init__()
        self.fixing_time = fixing_time
        self.frequency = frequency
        self.notional_percentage = notional_percentage
        self.name = name

    @property
    def fixing_time(self) -> FixingTimeRefData:
        """Fixing Time reference data object."""
        return self.__fixing_time

    @fixing_time.setter
    def fixing_time(self, value: FixingTimeRefData):
        self._property_changed('fixing_time')
        self.__fixing_time = value        

    @property
    def frequency(self) -> FrequencyRefData:
        """Frequency reference data object."""
        return self.__frequency

    @frequency.setter
    def frequency(self, value: FrequencyRefData):
        self._property_changed('frequency')
        self.__frequency = value        

    @property
    def notional_percentage(self) -> NotionalPercentageRefData:
        """Notional Percentage Reference Data"""
        return self.__notional_percentage

    @notional_percentage.setter
    def notional_percentage(self, value: NotionalPercentageRefData):
        self._property_changed('notional_percentage')
        self.__notional_percentage = value        


class EnhancedBetaBacktestParameters(Base):
        
    """Parameters of an Enhanced Beta backtest."""

    @camel_case_translate
    def __init__(
        self,
        underliers: Tuple[EnhancedBetaUnderlier, ...],
        roll_start: float,
        roll_end: float,
        base_index: str,
        name: str = None
    ):        
        super().__init__()
        self.roll_start = roll_start
        self.roll_end = roll_end
        self.base_index = base_index
        self.underliers = underliers
        self.name = name

    @property
    def roll_start(self) -> float:
        """Business day on which to begin rolling."""
        return self.__roll_start

    @roll_start.setter
    def roll_start(self, value: float):
        self._property_changed('roll_start')
        self.__roll_start = value        

    @property
    def roll_end(self) -> float:
        """Business day on which to finish rolling."""
        return self.__roll_end

    @roll_end.setter
    def roll_end(self, value: float):
        self._property_changed('roll_end')
        self.__roll_end = value        

    @property
    def base_index(self) -> str:
        """Base index which strategy is attempting to beat."""
        return self.__base_index

    @base_index.setter
    def base_index(self, value: str):
        self._property_changed('base_index')
        self.__base_index = value        

    @property
    def underliers(self) -> Tuple[EnhancedBetaUnderlier, ...]:
        """Assets included in the user's strategy."""
        return self.__underliers

    @underliers.setter
    def underliers(self, value: Tuple[EnhancedBetaUnderlier, ...]):
        self._property_changed('underliers')
        self.__underliers = value        


class ISelectBacktestParameters(Base):
        
    """Parameters of an ISelect backtest."""

    @camel_case_translate
    def __init__(
        self,
        max_leverage: float,
        underliers: Tuple[HistoricalUnderlier, ...],
        name: str = None
    ):        
        super().__init__()
        self.max_leverage = max_leverage
        self.underliers = underliers
        self.name = name

    @property
    def max_leverage(self) -> float:
        """Maximum leverage that can be used for the ISelect backtest"""
        return self.__max_leverage

    @max_leverage.setter
    def max_leverage(self, value: float):
        self._property_changed('max_leverage')
        self.__max_leverage = value        

    @property
    def underliers(self) -> Tuple[HistoricalUnderlier, ...]:
        """The underliers, the historical weights and dates that the client has chosen for
           their backtest"""
        return self.__underliers

    @underliers.setter
    def underliers(self, value: Tuple[HistoricalUnderlier, ...]):
        self._property_changed('underliers')
        self.__underliers = value        


class OptionBacktestUnderlier(Base):
        
    """Option Backtest Undelier."""

    @camel_case_translate
    def __init__(
        self,
        buy_sell: str,
        expiration: str,
        option_type: str,
        option_strike_type: str,
        strike: float,
        underlying_asset_id: str,
        notional_percentage: float = None,
        delta_hedging: DeltaHedgingParameters = None,
        trade_in_time: str = None,
        name: str = None
    ):        
        super().__init__()
        self.buy_sell = buy_sell
        self.expiration = expiration
        self.option_type = option_type
        self.option_strike_type = option_strike_type
        self.notional_percentage = notional_percentage
        self.strike = strike
        self.underlying_asset_id = underlying_asset_id
        self.delta_hedging = delta_hedging
        self.trade_in_time = trade_in_time
        self.name = name

    @property
    def buy_sell(self) -> str:
        """Option position, i.e buy"""
        return self.__buy_sell

    @buy_sell.setter
    def buy_sell(self, value: str):
        self._property_changed('buy_sell')
        self.__buy_sell = value        

    @property
    def expiration(self) -> str:
        """Time until expiration."""
        return self.__expiration

    @expiration.setter
    def expiration(self, value: str):
        self._property_changed('expiration')
        self.__expiration = value        

    @property
    def option_type(self) -> str:
        """Type of option, i.e call."""
        return self.__option_type

    @option_type.setter
    def option_type(self, value: str):
        self._property_changed('option_type')
        self.__option_type = value        

    @property
    def option_strike_type(self) -> str:
        """Type of option strike, i.e relative."""
        return self.__option_strike_type

    @option_strike_type.setter
    def option_strike_type(self, value: str):
        self._property_changed('option_strike_type')
        self.__option_strike_type = value        

    @property
    def notional_percentage(self) -> float:
        """The percentage to increase/decrease your position on the leg."""
        return self.__notional_percentage

    @notional_percentage.setter
    def notional_percentage(self, value: float):
        self._property_changed('notional_percentage')
        self.__notional_percentage = value        

    @property
    def strike(self) -> float:
        """Strike percentage, either relative % or delta % depending on strike type."""
        return self.__strike

    @strike.setter
    def strike(self, value: float):
        self._property_changed('strike')
        self.__strike = value        

    @property
    def underlying_asset_id(self) -> str:
        """Marquee unique asset identifier."""
        return self.__underlying_asset_id

    @underlying_asset_id.setter
    def underlying_asset_id(self, value: str):
        self._property_changed('underlying_asset_id')
        self.__underlying_asset_id = value        

    @property
    def delta_hedging(self) -> DeltaHedgingParameters:
        """Parameters for delta hedging an option."""
        return self.__delta_hedging

    @delta_hedging.setter
    def delta_hedging(self, value: DeltaHedgingParameters):
        self._property_changed('delta_hedging')
        self.__delta_hedging = value        

    @property
    def trade_in_time(self) -> str:
        """When from now to trade out the leg (must be less than expiration)."""
        return self.__trade_in_time

    @trade_in_time.setter
    def trade_in_time(self, value: str):
        self._property_changed('trade_in_time')
        self.__trade_in_time = value        


class PerformanceRange(Base):
        
    """a unit of performance"""

    @camel_case_translate
    def __init__(
        self,
        horizon: str = None,
        stats: PerformanceStats = None,
        name: str = None
    ):        
        super().__init__()
        self.horizon = horizon
        self.stats = stats
        self.name = name

    @property
    def horizon(self) -> str:
        """description of the time range"""
        return self.__horizon

    @horizon.setter
    def horizon(self, value: str):
        self._property_changed('horizon')
        self.__horizon = value        

    @property
    def stats(self) -> PerformanceStats:
        """Performance statistics."""
        return self.__stats

    @stats.setter
    def stats(self, value: PerformanceStats):
        self._property_changed('stats')
        self.__stats = value        


class UnderlyingAssetIdDataRefData(Base):
        
    """Underlying asset id data reference data object."""

    @camel_case_translate
    def __init__(
        self,
        asset_id: str = None,
        fixing_time: FixingTimeRefData = None,
        frequency: FrequencyRefData = None,
        name: str = None
    ):        
        super().__init__()
        self.asset_id = asset_id
        self.fixing_time = fixing_time
        self.frequency = frequency
        self.name = name

    @property
    def asset_id(self) -> str:
        """Marquee unique asset identifier."""
        return self.__asset_id

    @asset_id.setter
    def asset_id(self, value: str):
        self._property_changed('asset_id')
        self.__asset_id = value        

    @property
    def fixing_time(self) -> FixingTimeRefData:
        """Fixing Time reference data object."""
        return self.__fixing_time

    @fixing_time.setter
    def fixing_time(self, value: FixingTimeRefData):
        self._property_changed('fixing_time')
        self.__fixing_time = value        

    @property
    def frequency(self) -> FrequencyRefData:
        """Frequency reference data object."""
        return self.__frequency

    @frequency.setter
    def frequency(self, value: FrequencyRefData):
        self._property_changed('frequency')
        self.__frequency = value        


class BacktestPerformanceDecomposition(Base):
        
    """Decomposition of backtest performance"""

    @camel_case_translate
    def __init__(
        self,
        name: str = None,
        performance: Tuple[FieldValueMap, ...] = None,
        stats: PerformanceStats = None
    ):        
        super().__init__()
        self.name = name
        self.performance = performance
        self.stats = stats

    @property
    def name(self) -> str:
        """Name of this performance decomposition"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def performance(self) -> Tuple[FieldValueMap, ...]:
        """Backtest performance curve."""
        return self.__performance

    @performance.setter
    def performance(self, value: Tuple[FieldValueMap, ...]):
        self._property_changed('performance')
        self.__performance = value        

    @property
    def stats(self) -> PerformanceStats:
        """Performance statistics."""
        return self.__stats

    @stats.setter
    def stats(self, value: PerformanceStats):
        self._property_changed('stats')
        self.__stats = value        


class BacktestRisk(Base):
        
    """Risks of the backtest portfolio"""

    @camel_case_translate
    def __init__(
        self,
        name: str = None,
        timeseries: Tuple[FieldValueMap, ...] = None
    ):        
        super().__init__()
        self.name = name
        self.timeseries = timeseries

    @property
    def name(self) -> str:
        """Name of this risk"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def timeseries(self) -> Tuple[FieldValueMap, ...]:
        """Backtest portfolio risk curve."""
        return self.__timeseries

    @timeseries.setter
    def timeseries(self, value: Tuple[FieldValueMap, ...]):
        self._property_changed('timeseries')
        self.__timeseries = value        


class BacktestRiskPosition(Base):
        
    @camel_case_translate
    def __init__(
        self,
        instrument: dict,
        quantity: float = None,
        market_model: Union[EquityMarketModel, str] = None,
        expiry_date_mode: str = None,
        name: str = None
    ):        
        super().__init__()
        self.instrument = instrument
        self.quantity = quantity
        self.market_model = market_model
        self.expiry_date_mode = expiry_date_mode
        self.name = name

    @property
    def instrument(self) -> dict:
        return self.__instrument

    @instrument.setter
    def instrument(self, value: dict):
        self._property_changed('instrument')
        self.__instrument = value        

    @property
    def quantity(self) -> float:
        """Quantity of instrument"""
        return self.__quantity

    @quantity.setter
    def quantity(self, value: float):
        self._property_changed('quantity')
        self.__quantity = value        

    @property
    def market_model(self) -> Union[EquityMarketModel, str]:
        """Market model for pricing"""
        return self.__market_model

    @market_model.setter
    def market_model(self, value: Union[EquityMarketModel, str]):
        self._property_changed('market_model')
        self.__market_model = get_enum_value(EquityMarketModel, value)        

    @property
    def expiry_date_mode(self) -> str:
        """Expiry date mode to be used in the instrument e.g. listed."""
        return self.__expiry_date_mode

    @expiry_date_mode.setter
    def expiry_date_mode(self, value: str):
        self._property_changed('expiry_date_mode')
        self.__expiry_date_mode = value        


class BacktestStrategyUnderlier(Base):
        
    """Backtest Strategy Undelier."""

    @camel_case_translate
    def __init__(
        self,
        instrument: dict,
        market_model: str,
        notional_percentage: float = None,
        expiry_date_mode: str = None,
        name: str = None,
        hedge: BacktestStrategyUnderlierHedge = None
    ):        
        super().__init__()
        self.instrument = instrument
        self.notional_percentage = notional_percentage
        self.market_model = market_model
        self.expiry_date_mode = expiry_date_mode
        self.name = name
        self.hedge = hedge

    @property
    def instrument(self) -> dict:
        """instrument that you are getting into"""
        return self.__instrument

    @instrument.setter
    def instrument(self, value: dict):
        self._property_changed('instrument')
        self.__instrument = value        

    @property
    def notional_percentage(self) -> float:
        """The quantity of the underlier"""
        return self.__notional_percentage

    @notional_percentage.setter
    def notional_percentage(self, value: float):
        self._property_changed('notional_percentage')
        self.__notional_percentage = value        

    @property
    def market_model(self) -> str:
        """Market model used for the underlier."""
        return self.__market_model

    @market_model.setter
    def market_model(self, value: str):
        self._property_changed('market_model')
        self.__market_model = value        

    @property
    def expiry_date_mode(self) -> str:
        """Expiry date mode to be used in the instrument e.g. listed."""
        return self.__expiry_date_mode

    @expiry_date_mode.setter
    def expiry_date_mode(self, value: str):
        self._property_changed('expiry_date_mode')
        self.__expiry_date_mode = value        

    @property
    def name(self) -> str:
        """identifying name for the backtest leg"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def hedge(self) -> BacktestStrategyUnderlierHedge:
        """Hedge information for the backtest underlier"""
        return self.__hedge

    @hedge.setter
    def hedge(self, value: BacktestStrategyUnderlierHedge):
        self._property_changed('hedge')
        self.__hedge = value        


class BasketBacktestRefData(Base):
        
    """Basket backtest reference data"""

    @camel_case_translate
    def __init__(
        self,
        currency: CurrencyRefData = None,
        look_back_period: LookBackPeriodRefData = None,
        weighting_strategy: dict = None,
        weighting_modifiers: dict = None,
        name: str = None
    ):        
        super().__init__()
        self.currency = currency
        self.look_back_period = look_back_period
        self.weighting_strategy = weighting_strategy
        self.weighting_modifiers = weighting_modifiers
        self.name = name

    @property
    def currency(self) -> CurrencyRefData:
        """Currency Reference Data"""
        return self.__currency

    @currency.setter
    def currency(self, value: CurrencyRefData):
        self._property_changed('currency')
        self.__currency = value        

    @property
    def look_back_period(self) -> LookBackPeriodRefData:
        """Look back period reference data object."""
        return self.__look_back_period

    @look_back_period.setter
    def look_back_period(self, value: LookBackPeriodRefData):
        self._property_changed('look_back_period')
        self.__look_back_period = value        

    @property
    def weighting_strategy(self) -> dict:
        """Weighting strategy reference data object."""
        return self.__weighting_strategy

    @weighting_strategy.setter
    def weighting_strategy(self, value: dict):
        self._property_changed('weighting_strategy')
        self.__weighting_strategy = value        

    @property
    def weighting_modifiers(self) -> dict:
        """Weighting Modifiers reference data object."""
        return self.__weighting_modifiers

    @weighting_modifiers.setter
    def weighting_modifiers(self, value: dict):
        self._property_changed('weighting_modifiers')
        self.__weighting_modifiers = value        


class ComparisonBacktestResult(Base):
        
    """Comparisons of backtest results"""

    @camel_case_translate
    def __init__(
        self,
        stats: PerformanceStats = None,
        performance: Tuple[FieldValueMap, ...] = None,
        id_: str = None,
        name: str = None
    ):        
        super().__init__()
        self.stats = stats
        self.performance = performance
        self.__id = id_
        self.name = name

    @property
    def stats(self) -> PerformanceStats:
        """Performance statistics."""
        return self.__stats

    @stats.setter
    def stats(self, value: PerformanceStats):
        self._property_changed('stats')
        self.__stats = value        

    @property
    def performance(self) -> Tuple[FieldValueMap, ...]:
        """Performance for the comparison asset or backtest curve"""
        return self.__performance

    @performance.setter
    def performance(self, value: Tuple[FieldValueMap, ...]):
        self._property_changed('performance')
        self.__performance = value        

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        


class EnhancedBetaRefData(Base):
        
    """Enhanced Beta backtest reference data"""

    @camel_case_translate
    def __init__(
        self,
        look_back_period: LookBackPeriodRefData = None,
        currency: CurrencyRefData = None,
        base_index: BaseIndexRefData = None,
        MASJ8W49Y02X9CGS: dict = None,
        MAAHST8JED9B607H: dict = None,
        name: str = None
    ):        
        super().__init__()
        self.look_back_period = look_back_period
        self.currency = currency
        self.base_index = base_index
        self.MASJ8W49Y02X9CGS = MASJ8W49Y02X9CGS
        self.MAAHST8JED9B607H = MAAHST8JED9B607H
        self.name = name

    @property
    def look_back_period(self) -> LookBackPeriodRefData:
        """Look back period reference data object."""
        return self.__look_back_period

    @look_back_period.setter
    def look_back_period(self, value: LookBackPeriodRefData):
        self._property_changed('look_back_period')
        self.__look_back_period = value        

    @property
    def currency(self) -> CurrencyRefData:
        """Currency Reference Data"""
        return self.__currency

    @currency.setter
    def currency(self, value: CurrencyRefData):
        self._property_changed('currency')
        self.__currency = value        

    @property
    def base_index(self) -> BaseIndexRefData:
        """Base index reference data object."""
        return self.__base_index

    @base_index.setter
    def base_index(self, value: BaseIndexRefData):
        self._property_changed('base_index')
        self.__base_index = value        

    @property
    def MASJ8W49Y02X9CGS(self) -> dict:
        return self.__MASJ8W49Y02X9CGS

    @MASJ8W49Y02X9CGS.setter
    def MASJ8W49Y02X9CGS(self, value: dict):
        self._property_changed('MASJ8W49Y02X9CGS')
        self.__MASJ8W49Y02X9CGS = value        

    @property
    def MAAHST8JED9B607H(self) -> dict:
        return self.__MAAHST8JED9B607H

    @MAAHST8JED9B607H.setter
    def MAAHST8JED9B607H(self, value: dict):
        self._property_changed('MAAHST8JED9B607H')
        self.__MAAHST8JED9B607H = value        


class UnderlyingAssetIdRefData(Base):
        
    """Underlying asset id reference data object."""

    @camel_case_translate
    def __init__(
        self,
        default: str = None,
        enum: Tuple[str, ...] = None,
        data: Tuple[UnderlyingAssetIdDataRefData, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.default = default
        self.enum = enum
        self.data = data
        self.name = name

    @property
    def default(self) -> str:
        """Default asset id underlying the option."""
        return self.__default

    @default.setter
    def default(self, value: str):
        self._property_changed('default')
        self.__default = value        

    @property
    def enum(self) -> Tuple[str, ...]:
        """Asset ids allowed to underly the option."""
        return self.__enum

    @enum.setter
    def enum(self, value: Tuple[str, ...]):
        self._property_changed('enum')
        self.__enum = value        

    @property
    def data(self) -> Tuple[UnderlyingAssetIdDataRefData, ...]:
        """Underlying asset id data reference data object."""
        return self.__data

    @data.setter
    def data(self, value: Tuple[UnderlyingAssetIdDataRefData, ...]):
        self._property_changed('data')
        self.__data = value        


class VolatilityBacktestParameters(Base):
        
    """Parameters of a Volatility backtest."""

    @camel_case_translate
    def __init__(
        self,
        underliers: Tuple[OptionBacktestUnderlier, ...],
        trade_in_method: str = None,
        scaling_method: str = None,
        name: str = None
    ):        
        super().__init__()
        self.underliers = underliers
        self.trade_in_method = trade_in_method
        self.scaling_method = scaling_method
        self.name = name

    @property
    def underliers(self) -> Tuple[OptionBacktestUnderlier, ...]:
        """Underlying assets of the backtest"""
        return self.__underliers

    @underliers.setter
    def underliers(self, value: Tuple[OptionBacktestUnderlier, ...]):
        self._property_changed('underliers')
        self.__underliers = value        

    @property
    def trade_in_method(self) -> str:
        """Method used to trade in legs before expiry."""
        return self.__trade_in_method

    @trade_in_method.setter
    def trade_in_method(self, value: str):
        self._property_changed('trade_in_method')
        self.__trade_in_method = value        

    @property
    def scaling_method(self) -> str:
        """The method for scaling legs, i.e percentage of NAV"""
        return self.__scaling_method

    @scaling_method.setter
    def scaling_method(self, value: str):
        self._property_changed('scaling_method')
        self.__scaling_method = value        


class BacktestResult(Base):
        
    """backtest result"""

    @camel_case_translate
    def __init__(
        self,
        backtest_id: str = None,
        performance: Tuple[FieldValueMap, ...] = None,
        portfolio: Tuple[FieldValueMap, ...] = None,
        stats: PerformanceStats = None,
        performance_decompositions: Tuple[BacktestPerformanceDecomposition, ...] = None,
        risks: Tuple[BacktestRisk, ...] = None,
        history: Tuple[PerformanceRange, ...] = None,
        underlier_correlation: Tuple[EntityCorrelation, ...] = None,
        comparisons: Tuple[BacktestComparison, ...] = None,
        backtest_version: float = None,
        name: str = None
    ):        
        super().__init__()
        self.backtest_id = backtest_id
        self.performance = performance
        self.portfolio = portfolio
        self.stats = stats
        self.performance_decompositions = performance_decompositions
        self.risks = risks
        self.history = history
        self.underlier_correlation = underlier_correlation
        self.comparisons = comparisons
        self.backtest_version = backtest_version
        self.name = name

    @property
    def backtest_id(self) -> str:
        """Marquee unique backtest identifier"""
        return self.__backtest_id

    @backtest_id.setter
    def backtest_id(self, value: str):
        self._property_changed('backtest_id')
        self.__backtest_id = value        

    @property
    def performance(self) -> Tuple[FieldValueMap, ...]:
        """Backtest performance curve."""
        return self.__performance

    @performance.setter
    def performance(self, value: Tuple[FieldValueMap, ...]):
        self._property_changed('performance')
        self.__performance = value        

    @property
    def portfolio(self) -> Tuple[FieldValueMap, ...]:
        """Backtest entry/exit transactions and portfolio composition."""
        return self.__portfolio

    @portfolio.setter
    def portfolio(self, value: Tuple[FieldValueMap, ...]):
        self._property_changed('portfolio')
        self.__portfolio = value        

    @property
    def stats(self) -> PerformanceStats:
        """Performance statistics."""
        return self.__stats

    @stats.setter
    def stats(self, value: PerformanceStats):
        self._property_changed('stats')
        self.__stats = value        

    @property
    def performance_decompositions(self) -> Tuple[BacktestPerformanceDecomposition, ...]:
        """Decompositions of the performance of the backtest"""
        return self.__performance_decompositions

    @performance_decompositions.setter
    def performance_decompositions(self, value: Tuple[BacktestPerformanceDecomposition, ...]):
        self._property_changed('performance_decompositions')
        self.__performance_decompositions = value        

    @property
    def risks(self) -> Tuple[BacktestRisk, ...]:
        """Risks of the backtest portfolio"""
        return self.__risks

    @risks.setter
    def risks(self, value: Tuple[BacktestRisk, ...]):
        self._property_changed('risks')
        self.__risks = value        

    @property
    def history(self) -> Tuple[PerformanceRange, ...]:
        """Backtest historical calculations."""
        return self.__history

    @history.setter
    def history(self, value: Tuple[PerformanceRange, ...]):
        self._property_changed('history')
        self.__history = value        

    @property
    def underlier_correlation(self) -> Tuple[EntityCorrelation, ...]:
        """entity correlation"""
        return self.__underlier_correlation

    @underlier_correlation.setter
    def underlier_correlation(self, value: Tuple[EntityCorrelation, ...]):
        self._property_changed('underlier_correlation')
        self.__underlier_correlation = value        

    @property
    def comparisons(self) -> Tuple[BacktestComparison, ...]:
        """Array of comparisons btw the backtest and comparison entity."""
        return self.__comparisons

    @comparisons.setter
    def comparisons(self, value: Tuple[BacktestComparison, ...]):
        self._property_changed('comparisons')
        self.__comparisons = value        

    @property
    def backtest_version(self) -> float:
        """Backtest version number."""
        return self.__backtest_version

    @backtest_version.setter
    def backtest_version(self, value: float):
        self._property_changed('backtest_version')
        self.__backtest_version = value        


class BacktestRiskRequest(Base):
        
    """Request to compute Backtest Price and Risk"""

    @camel_case_translate
    def __init__(
        self,
        positions: Tuple[BacktestRiskPosition, ...],
        measures: Tuple[Union[BacktestRiskMeasureType, str], ...],
        start_date: datetime.date = None,
        end_date: datetime.date = None,
        name: str = None
    ):        
        super().__init__()
        self.positions = positions
        self.measures = measures
        self.start_date = start_date
        self.end_date = end_date
        self.name = name

    @property
    def positions(self) -> Tuple[BacktestRiskPosition, ...]:
        """The positions on which to run the risk calculation"""
        return self.__positions

    @positions.setter
    def positions(self, value: Tuple[BacktestRiskPosition, ...]):
        self._property_changed('positions')
        self.__positions = value        

    @property
    def measures(self) -> Tuple[Union[BacktestRiskMeasureType, str], ...]:
        """A collection of risk measures to compute. E.g. { 'measureType': 'Delta',
           'assetClass': 'Equity'"""
        return self.__measures

    @measures.setter
    def measures(self, value: Tuple[Union[BacktestRiskMeasureType, str], ...]):
        self._property_changed('measures')
        self.__measures = value        

    @property
    def start_date(self) -> datetime.date:
        """Start date of backtest risk computation selected by user."""
        return self.__start_date

    @start_date.setter
    def start_date(self, value: datetime.date):
        self._property_changed('start_date')
        self.__start_date = value        

    @property
    def end_date(self) -> datetime.date:
        """End date of backtest risk computation selected by user. If not selected,
           defaults to the last date for which we can compute price"""
        return self.__end_date

    @end_date.setter
    def end_date(self, value: datetime.date):
        self._property_changed('end_date')
        self.__end_date = value        


class VolBacktestRefData(Base):
        
    """Volatility backtest reference data"""

    @camel_case_translate
    def __init__(
        self,
        buy_sell: BuySellRefData = None,
        currency: CurrencyRefData = None,
        delta_hedging: DeltaHedgingRefData = None,
        delta_strike: StrikeRefData = None,
        notional_percentage: NotionalPercentageRefData = None,
        expiration: ExpirationRefData = None,
        look_back_period: LookBackPeriodRefData = None,
        option_type: OptionTypeRefData = None,
        option_strike_type: OptionStrikeTypeRefData = None,
        relative_strike: StrikeRefData = None,
        strike: StrikeRefData = None,
        scaling_method: ScalingMethodRefData = None,
        underlying_asset_id: UnderlyingAssetIdRefData = None,
        trade_in_method: TradeInMethodRefData = None,
        trade_in_time: TradeInTimeRefData = None,
        name: str = None
    ):        
        super().__init__()
        self.buy_sell = buy_sell
        self.currency = currency
        self.delta_hedging = delta_hedging
        self.delta_strike = delta_strike
        self.notional_percentage = notional_percentage
        self.expiration = expiration
        self.look_back_period = look_back_period
        self.option_type = option_type
        self.option_strike_type = option_strike_type
        self.relative_strike = relative_strike
        self.strike = strike
        self.scaling_method = scaling_method
        self.underlying_asset_id = underlying_asset_id
        self.trade_in_method = trade_in_method
        self.trade_in_time = trade_in_time
        self.name = name

    @property
    def buy_sell(self) -> BuySellRefData:
        """Buy Sell reference data object."""
        return self.__buy_sell

    @buy_sell.setter
    def buy_sell(self, value: BuySellRefData):
        self._property_changed('buy_sell')
        self.__buy_sell = value        

    @property
    def currency(self) -> CurrencyRefData:
        """Currency Reference Data"""
        return self.__currency

    @currency.setter
    def currency(self, value: CurrencyRefData):
        self._property_changed('currency')
        self.__currency = value        

    @property
    def delta_hedging(self) -> DeltaHedgingRefData:
        """Delta Hedging Reference Data"""
        return self.__delta_hedging

    @delta_hedging.setter
    def delta_hedging(self, value: DeltaHedgingRefData):
        self._property_changed('delta_hedging')
        self.__delta_hedging = value        

    @property
    def delta_strike(self) -> StrikeRefData:
        """Strike reference data object."""
        return self.__delta_strike

    @delta_strike.setter
    def delta_strike(self, value: StrikeRefData):
        self._property_changed('delta_strike')
        self.__delta_strike = value        

    @property
    def notional_percentage(self) -> NotionalPercentageRefData:
        """Notional Percentage Reference Data"""
        return self.__notional_percentage

    @notional_percentage.setter
    def notional_percentage(self, value: NotionalPercentageRefData):
        self._property_changed('notional_percentage')
        self.__notional_percentage = value        

    @property
    def expiration(self) -> ExpirationRefData:
        """Expiration reference data object."""
        return self.__expiration

    @expiration.setter
    def expiration(self, value: ExpirationRefData):
        self._property_changed('expiration')
        self.__expiration = value        

    @property
    def look_back_period(self) -> LookBackPeriodRefData:
        """Look back period reference data object."""
        return self.__look_back_period

    @look_back_period.setter
    def look_back_period(self, value: LookBackPeriodRefData):
        self._property_changed('look_back_period')
        self.__look_back_period = value        

    @property
    def option_type(self) -> OptionTypeRefData:
        """Option Type reference data object."""
        return self.__option_type

    @option_type.setter
    def option_type(self, value: OptionTypeRefData):
        self._property_changed('option_type')
        self.__option_type = value        

    @property
    def option_strike_type(self) -> OptionStrikeTypeRefData:
        """Option strike type reference data object."""
        return self.__option_strike_type

    @option_strike_type.setter
    def option_strike_type(self, value: OptionStrikeTypeRefData):
        self._property_changed('option_strike_type')
        self.__option_strike_type = value        

    @property
    def relative_strike(self) -> StrikeRefData:
        """Strike reference data object."""
        return self.__relative_strike

    @relative_strike.setter
    def relative_strike(self, value: StrikeRefData):
        self._property_changed('relative_strike')
        self.__relative_strike = value        

    @property
    def strike(self) -> StrikeRefData:
        """Strike reference data object."""
        return self.__strike

    @strike.setter
    def strike(self, value: StrikeRefData):
        self._property_changed('strike')
        self.__strike = value        

    @property
    def scaling_method(self) -> ScalingMethodRefData:
        """Scaling Method Reference Data"""
        return self.__scaling_method

    @scaling_method.setter
    def scaling_method(self, value: ScalingMethodRefData):
        self._property_changed('scaling_method')
        self.__scaling_method = value        

    @property
    def underlying_asset_id(self) -> UnderlyingAssetIdRefData:
        """Underlying asset id reference data object."""
        return self.__underlying_asset_id

    @underlying_asset_id.setter
    def underlying_asset_id(self, value: UnderlyingAssetIdRefData):
        self._property_changed('underlying_asset_id')
        self.__underlying_asset_id = value        

    @property
    def trade_in_method(self) -> TradeInMethodRefData:
        """Trade In Method Reference Data"""
        return self.__trade_in_method

    @trade_in_method.setter
    def trade_in_method(self, value: TradeInMethodRefData):
        self._property_changed('trade_in_method')
        self.__trade_in_method = value        

    @property
    def trade_in_time(self) -> TradeInTimeRefData:
        """Trade In Time Reference Data"""
        return self.__trade_in_time

    @trade_in_time.setter
    def trade_in_time(self, value: TradeInTimeRefData):
        self._property_changed('trade_in_time')
        self.__trade_in_time = value        


class VolatilityFlowBacktestParameters(Base):
        
    """Parameters of a Volatility Flow Backtest."""

    @camel_case_translate
    def __init__(
        self,
        trading_parameters: BacktestTradingParameters,
        index_initial_value: float,
        underliers: Tuple[BacktestStrategyUnderlier, ...] = None,
        measures: Tuple[Union[FlowVolBacktestMeasure, str], ...] = ['ALL MEASURES'],
        name: str = None
    ):        
        super().__init__()
        self.index_initial_value = index_initial_value
        self.underliers = underliers
        self.trading_parameters = trading_parameters
        self.measures = measures
        self.name = name

    @property
    def index_initial_value(self) -> float:
        """The initial index value of the strategy"""
        return self.__index_initial_value

    @index_initial_value.setter
    def index_initial_value(self, value: float):
        self._property_changed('index_initial_value')
        self.__index_initial_value = value        

    @property
    def underliers(self) -> Tuple[BacktestStrategyUnderlier, ...]:
        """Underlying units of the backtest strategy"""
        return self.__underliers

    @underliers.setter
    def underliers(self, value: Tuple[BacktestStrategyUnderlier, ...]):
        self._property_changed('underliers')
        self.__underliers = value        

    @property
    def trading_parameters(self) -> BacktestTradingParameters:
        """details about how to transact in the instrument"""
        return self.__trading_parameters

    @trading_parameters.setter
    def trading_parameters(self, value: BacktestTradingParameters):
        self._property_changed('trading_parameters')
        self.__trading_parameters = value        

    @property
    def measures(self) -> Tuple[Union[FlowVolBacktestMeasure, str], ...]:
        """Array of measures which should be calculated. By default all measures will be
           calculated"""
        return self.__measures

    @measures.setter
    def measures(self, value: Tuple[Union[FlowVolBacktestMeasure, str], ...]):
        self._property_changed('measures')
        self.__measures = value        


class Backtest(Base):
        
    """A backtest"""

    @camel_case_translate
    def __init__(
        self,
        name: str,
        type_: Union[BacktestType, str],
        asset_class: Union[AssetClass, str],
        cost_netting: bool = False,
        created_by_id: str = None,
        created_time: datetime.datetime = None,
        currency: Union[Currency, str] = None,
        entitlements: Entitlements = None,
        entitlement_exclusions: EntitlementExclusions = None,
        id_: str = None,
        last_updated_by_id: str = None,
        last_updated_time: datetime.datetime = None,
        mq_symbol: str = None,
        owner_id: str = None,
        report_ids: Tuple[str, ...] = None,
        parameters: dict = None,
        start_date: datetime.date = None,
        end_date: datetime.date = None,
        version: float = None
    ):        
        super().__init__()
        self.cost_netting = cost_netting
        self.created_by_id = created_by_id
        self.created_time = created_time
        self.currency = currency
        self.entitlements = entitlements
        self.entitlement_exclusions = entitlement_exclusions
        self.__id = id_
        self.last_updated_by_id = last_updated_by_id
        self.last_updated_time = last_updated_time
        self.mq_symbol = mq_symbol
        self.name = name
        self.owner_id = owner_id
        self.report_ids = report_ids
        self.parameters = parameters
        self.start_date = start_date
        self.end_date = end_date
        self.__type = get_enum_value(BacktestType, type_)
        self.asset_class = asset_class
        self.version = version

    @property
    def cost_netting(self) -> bool:
        """Nets trading costs across the leaf nodes of the strategy."""
        return self.__cost_netting

    @cost_netting.setter
    def cost_netting(self, value: bool):
        self._property_changed('cost_netting')
        self.__cost_netting = value        

    @property
    def created_by_id(self) -> str:
        """Unique identifier of user who created the object."""
        return self.__created_by_id

    @created_by_id.setter
    def created_by_id(self, value: str):
        self._property_changed('created_by_id')
        self.__created_by_id = value        

    @property
    def created_time(self) -> datetime.datetime:
        """Time created. ISO 8601 formatted string."""
        return self.__created_time

    @created_time.setter
    def created_time(self, value: datetime.datetime):
        self._property_changed('created_time')
        self.__created_time = value        

    @property
    def currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self._property_changed('currency')
        self.__currency = get_enum_value(Currency, value)        

    @property
    def entitlements(self) -> Entitlements:
        """Defines the entitlements of a given resource."""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self._property_changed('entitlements')
        self.__entitlements = value        

    @property
    def entitlement_exclusions(self) -> EntitlementExclusions:
        """Defines the exclusion entitlements of a given resource."""
        return self.__entitlement_exclusions

    @entitlement_exclusions.setter
    def entitlement_exclusions(self, value: EntitlementExclusions):
        self._property_changed('entitlement_exclusions')
        self.__entitlement_exclusions = value        

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def last_updated_by_id(self) -> str:
        """Unique identifier of user who last updated the object."""
        return self.__last_updated_by_id

    @last_updated_by_id.setter
    def last_updated_by_id(self, value: str):
        self._property_changed('last_updated_by_id')
        self.__last_updated_by_id = value        

    @property
    def last_updated_time(self) -> datetime.datetime:
        """Timestamp of when the object was last updated."""
        return self.__last_updated_time

    @last_updated_time.setter
    def last_updated_time(self, value: datetime.datetime):
        self._property_changed('last_updated_time')
        self.__last_updated_time = value        

    @property
    def mq_symbol(self) -> str:
        """Marquee unique symbol identifier for the backtest."""
        return self.__mq_symbol

    @mq_symbol.setter
    def mq_symbol(self, value: str):
        self._property_changed('mq_symbol')
        self.__mq_symbol = value        

    @property
    def name(self) -> str:
        """Display name of the basket"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def owner_id(self) -> str:
        """Marquee unique identifier"""
        return self.__owner_id

    @owner_id.setter
    def owner_id(self, value: str):
        self._property_changed('owner_id')
        self.__owner_id = value        

    @property
    def report_ids(self) -> Tuple[str, ...]:
        """Array of report identifiers related to the object"""
        return self.__report_ids

    @report_ids.setter
    def report_ids(self, value: Tuple[str, ...]):
        self._property_changed('report_ids')
        self.__report_ids = value        

    @property
    def parameters(self) -> dict:
        return self.__parameters

    @parameters.setter
    def parameters(self, value: dict):
        self._property_changed('parameters')
        self.__parameters = value        

    @property
    def start_date(self) -> datetime.date:
        """Start date of backtest selected by user. If not selected, defaults to start of
           backtest timeseries."""
        return self.__start_date

    @start_date.setter
    def start_date(self, value: datetime.date):
        self._property_changed('start_date')
        self.__start_date = value        

    @property
    def end_date(self) -> datetime.date:
        """End date of backtest selected by user. If not selected, defaults to end of
           backtest timeseries."""
        return self.__end_date

    @end_date.setter
    def end_date(self, value: datetime.date):
        self._property_changed('end_date')
        self.__end_date = value        

    @property
    def type(self) -> Union[BacktestType, str]:
        """Backtest type differentiates the backtest type."""
        return self.__type

    @type.setter
    def type(self, value: Union[BacktestType, str]):
        self._property_changed('type')
        self.__type = get_enum_value(BacktestType, value)        

    @property
    def asset_class(self) -> Union[AssetClass, str]:
        """Asset class of the backtest underliers."""
        return self.__asset_class

    @asset_class.setter
    def asset_class(self, value: Union[AssetClass, str]):
        self._property_changed('asset_class')
        self.__asset_class = get_enum_value(AssetClass, value)        

    @property
    def version(self) -> float:
        """Backtest version number."""
        return self.__version

    @version.setter
    def version(self, value: float):
        self._property_changed('version')
        self.__version = value        


class BacktestRefData(Base):
        
    """Backtest reference data"""

    _name_mappings = {'enhanced_beta': 'enhanced_beta'}

    @camel_case_translate
    def __init__(
        self,
        id_: str = None,
        volatility: dict = None,
        enhanced_beta: EnhancedBetaRefData = None,
        basket: BasketBacktestRefData = None,
        owner_id: str = None,
        entitlements: Entitlements = None,
        entitlement_exclusions: EntitlementExclusions = None,
        last_updated_by_id: str = None,
        last_updated_time: datetime.datetime = None,
        name: str = None
    ):        
        super().__init__()
        self.__id = id_
        self.volatility = volatility
        self.enhanced_beta = enhanced_beta
        self.basket = basket
        self.owner_id = owner_id
        self.entitlements = entitlements
        self.entitlement_exclusions = entitlement_exclusions
        self.last_updated_by_id = last_updated_by_id
        self.last_updated_time = last_updated_time
        self.name = name

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def volatility(self) -> dict:
        """Volatility backtest reference data."""
        return self.__volatility

    @volatility.setter
    def volatility(self, value: dict):
        self._property_changed('volatility')
        self.__volatility = value        

    @property
    def enhanced_beta(self) -> EnhancedBetaRefData:
        """Enhanced Beta backtest reference data"""
        return self.__enhanced_beta

    @enhanced_beta.setter
    def enhanced_beta(self, value: EnhancedBetaRefData):
        self._property_changed('enhanced_beta')
        self.__enhanced_beta = value        

    @property
    def basket(self) -> BasketBacktestRefData:
        """Basket backtest reference data"""
        return self.__basket

    @basket.setter
    def basket(self, value: BasketBacktestRefData):
        self._property_changed('basket')
        self.__basket = value        

    @property
    def owner_id(self) -> str:
        """Marquee unique identifier for user who owns the object."""
        return self.__owner_id

    @owner_id.setter
    def owner_id(self, value: str):
        self._property_changed('owner_id')
        self.__owner_id = value        

    @property
    def entitlements(self) -> Entitlements:
        """Defines the entitlements of a given resource."""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self._property_changed('entitlements')
        self.__entitlements = value        

    @property
    def entitlement_exclusions(self) -> EntitlementExclusions:
        """Defines the exclusion entitlements of a given resource."""
        return self.__entitlement_exclusions

    @entitlement_exclusions.setter
    def entitlement_exclusions(self, value: EntitlementExclusions):
        self._property_changed('entitlement_exclusions')
        self.__entitlement_exclusions = value        

    @property
    def last_updated_by_id(self) -> str:
        """Unique identifier of user who last updated the object."""
        return self.__last_updated_by_id

    @last_updated_by_id.setter
    def last_updated_by_id(self, value: str):
        self._property_changed('last_updated_by_id')
        self.__last_updated_by_id = value        

    @property
    def last_updated_time(self) -> datetime.datetime:
        """Timestamp of when the object was last updated."""
        return self.__last_updated_time

    @last_updated_time.setter
    def last_updated_time(self, value: datetime.datetime):
        self._property_changed('last_updated_time')
        self.__last_updated_time = value        
