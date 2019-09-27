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

from enum import Enum
from gs_quant.base import Base, EnumBase, get_enum_value
from gs_quant.target.common import *
from gs_quant.target.instrument import *
from typing import Tuple, Union
import datetime


class BacktestRiskMeasureType(EnumBase, Enum):    
    
    """The type of measure to perform risk on. e.g. Greeks"""

    Price = 'Price'
    Delta = 'Delta'
    Gamma = 'Gamma'
    Vega = 'Vega'
    Forward = 'Forward'
    Volatility = 'Volatility'
    
    def __repr__(self):
        return self.value


class BacktestType(EnumBase, Enum):    
    
    """Backtest type differentiates the backtest type."""

    Basket = 'Basket'
    Volatility = 'Volatility'
    Volatility_Flow = 'Volatility Flow'
    Enhanced_Beta = 'Enhanced Beta'
    
    def __repr__(self):
        return self.value


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
    
    def __repr__(self):
        return self.value


class BacktestComparison(Base):
        
    """Comparison object for backtests"""
       
    def __init__(
        self,
        id: str = None,
        correlation: float = None        
    ):
        super().__init__()
        self.__id = id
        self.__correlation = correlation

    @property
    def id(self) -> str:
        """Marquee unique identifier for the comparison asset or backtest"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value
        self._property_changed('id')        

    @property
    def correlation(self) -> float:
        """Correlation between the comparison entity and the backtest"""
        return self.__correlation

    @correlation.setter
    def correlation(self, value: float):
        self.__correlation = value
        self._property_changed('correlation')        


class BacktestPerformanceDecomposition(Base):
        
    """Decomposition of backtest performance"""
       
    def __init__(
        self,
        name: str = None,
        stats: PerformanceStats = None        
    ):
        super().__init__()
        self.__name = name
        self.__stats = stats

    @property
    def name(self) -> str:
        """Name of this performance decomposition"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def stats(self) -> PerformanceStats:
        """Performance statistics."""
        return self.__stats

    @stats.setter
    def stats(self, value: PerformanceStats):
        self.__stats = value
        self._property_changed('stats')        


class BacktestRebalanceParameters(Base):
        
    """Parameters relating to the backtest's rebalance"""
       
    def __init__(
        self,
        frequency_period: str = None,
        frequency: int = None,
        day_of_week: str = None,
        day_of_month: float = None        
    ):
        super().__init__()
        self.__frequency_period = frequency_period
        self.__frequency = frequency
        self.__day_of_week = day_of_week
        self.__day_of_month = day_of_month

    @property
    def frequency_period(self) -> str:
        """What frequency period should be used for the rebalance"""
        return self.__frequency_period

    @frequency_period.setter
    def frequency_period(self, value: str):
        self.__frequency_period = value
        self._property_changed('frequency_period')        

    @property
    def frequency(self) -> int:
        """What the frequency should be, given the frequency period, i.e. every 2 weeks"""
        return self.__frequency

    @frequency.setter
    def frequency(self, value: int):
        self.__frequency = value
        self._property_changed('frequency')        

    @property
    def day_of_week(self) -> str:
        """For weekly frequencyPeriod, the day of the week the rebalance should occur"""
        return self.__day_of_week

    @day_of_week.setter
    def day_of_week(self, value: str):
        self.__day_of_week = value
        self._property_changed('day_of_week')        

    @property
    def day_of_month(self) -> float:
        """For monthly frequencyPeriod rebalances, the day of the month the rebalance should occur"""
        return self.__day_of_month

    @day_of_month.setter
    def day_of_month(self, value: float):
        self.__day_of_month = value
        self._property_changed('day_of_month')        


class BacktestRisk(Base):
        
    """Risks of the backtest portfolio"""
       
    def __init__(
        self,
        name: str = None        
    ):
        super().__init__()
        self.__name = name

    @property
    def name(self) -> str:
        """Name of this risk"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        


class BacktestRiskPosition(Base):
               
    def __init__(
        self,
        instrument: EqOption,
        quantity: float = None        
    ):
        super().__init__()
        self.__instrument = instrument
        self.__quantity = quantity

    @property
    def instrument(self) -> EqOption:
        return self.__instrument

    @instrument.setter
    def instrument(self, value: EqOption):
        self.__instrument = value
        self._property_changed('instrument')        

    @property
    def quantity(self) -> float:
        """Quantity of instrument"""
        return self.__quantity

    @quantity.setter
    def quantity(self, value: float):
        self.__quantity = value
        self._property_changed('quantity')        


class BacktestTradingParameters(Base):
        
    """Trading Information for the Backtesting Strategy"""
       
    def __init__(
        self,
        quantity_type: str = None,
        quantity: float = None,
        trade_in_method: str = None,
        roll_frequency: str = None,
        scaling_method: str = None        
    ):
        super().__init__()
        self.__quantity_type = quantity_type
        self.__quantity = quantity
        self.__trade_in_method = trade_in_method
        self.__roll_frequency = roll_frequency
        self.__scaling_method = scaling_method

    @property
    def quantity_type(self) -> str:
        """The unit of the quantity of backtest strategy"""
        return self.__quantity_type

    @quantity_type.setter
    def quantity_type(self, value: str):
        self.__quantity_type = value
        self._property_changed('quantity_type')        

    @property
    def quantity(self) -> float:
        """The quantity of backtest strategy"""
        return self.__quantity

    @quantity.setter
    def quantity(self, value: float):
        self.__quantity = value
        self._property_changed('quantity')        

    @property
    def trade_in_method(self) -> str:
        """Roll method for the backtest strategy"""
        return self.__trade_in_method

    @trade_in_method.setter
    def trade_in_method(self, value: str):
        self.__trade_in_method = value
        self._property_changed('trade_in_method')        

    @property
    def roll_frequency(self) -> str:
        """Period the strategy rolls"""
        return self.__roll_frequency

    @roll_frequency.setter
    def roll_frequency(self, value: str):
        self.__roll_frequency = value
        self._property_changed('roll_frequency')        

    @property
    def scaling_method(self) -> str:
        """The method for scaling underliers, i.e fixedQuantity"""
        return self.__scaling_method

    @scaling_method.setter
    def scaling_method(self, value: str):
        self.__scaling_method = value
        self._property_changed('scaling_method')        


class BaseIndexRefData(Base):
        
    """Base index reference data object."""
       
    def __init__(
        self,
        default: str = None,
        enum: Tuple[str, ...] = None        
    ):
        super().__init__()
        self.__default = default
        self.__enum = enum

    @property
    def default(self) -> str:
        """Default asset id of base index"""
        return self.__default

    @default.setter
    def default(self, value: str):
        self.__default = value
        self._property_changed('default')        

    @property
    def enum(self) -> Tuple[str, ...]:
        """Base Indices Allowed"""
        return self.__enum

    @enum.setter
    def enum(self, value: Tuple[str, ...]):
        self.__enum = value
        self._property_changed('enum')        


class BuySellRefData(Base):
        
    """Buy Sell reference data object."""
       
    def __init__(
        self,
        default: str = None,
        enum: Tuple[str, ...] = None        
    ):
        super().__init__()
        self.__default = default
        self.__enum = enum

    @property
    def default(self) -> str:
        """Default Buy/Sell parameter."""
        return self.__default

    @default.setter
    def default(self, value: str):
        self.__default = value
        self._property_changed('default')        

    @property
    def enum(self) -> Tuple[str, ...]:
        """Buy/Sell parameters allowed."""
        return self.__enum

    @enum.setter
    def enum(self, value: Tuple[str, ...]):
        self.__enum = value
        self._property_changed('enum')        


class ComparisonBacktestResult(Base):
        
    """Comparisons of backtest results"""
       
    def __init__(
        self,
        stats: PerformanceStats = None,
        id: str = None        
    ):
        super().__init__()
        self.__stats = stats
        self.__id = id

    @property
    def stats(self) -> PerformanceStats:
        """Performance statistics."""
        return self.__stats

    @stats.setter
    def stats(self, value: PerformanceStats):
        self.__stats = value
        self._property_changed('stats')        

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value
        self._property_changed('id')        


class CurrencyRefData(Base):
        
    """Currency Reference Data"""
       
    def __init__(
        self,
        default: Union[Currency, str] = None,
        enum: Tuple[Union[Currency, str], ...] = None        
    ):
        super().__init__()
        self.__default = get_enum_value(Currency, default)
        self.__enum = enum

    @property
    def default(self) -> Union[Currency, str]:
        """Default currency."""
        return self.__default

    @default.setter
    def default(self, value: Union[Currency, str]):
        self.__default = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('default')        

    @property
    def enum(self) -> Tuple[Union[Currency, str], ...]:
        """All currencies allowed."""
        return self.__enum

    @enum.setter
    def enum(self, value: Tuple[Union[Currency, str], ...]):
        self.__enum = value
        self._property_changed('enum')        


class DeltaHedgeParameters(Base):
        
    """Parameters for delta hedging a backtest strategy"""
       
    def __init__(
        self,
        frequency: str,
        fixing_time: str = None,
        notional: float = None        
    ):
        super().__init__()
        self.__fixing_time = fixing_time
        self.__frequency = frequency
        self.__notional = notional

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
        self.__fixing_time = value
        self._property_changed('fixing_time')        

    @property
    def frequency(self) -> str:
        """What frequency the leg is hedged."""
        return self.__frequency

    @frequency.setter
    def frequency(self, value: str):
        self.__frequency = value
        self._property_changed('frequency')        

    @property
    def notional(self) -> float:
        """Notional to delta hedge the underlier"""
        return self.__notional

    @notional.setter
    def notional(self, value: float):
        self.__notional = value
        self._property_changed('notional')        


class DeltaHedgingParameters(Base):
        
    """Parameters for delta hedging an option."""
       
    def __init__(
        self,
        enabled: bool,
        frequency: str,
        fixing_time: str,
        notional_percentage: float        
    ):
        super().__init__()
        self.__enabled = enabled
        self.__fixing_time = fixing_time
        self.__frequency = frequency
        self.__notional_percentage = notional_percentage

    @property
    def enabled(self) -> bool:
        """Whether the leg is being hedged."""
        return self.__enabled

    @enabled.setter
    def enabled(self, value: bool):
        self.__enabled = value
        self._property_changed('enabled')        

    @property
    def fixing_time(self) -> str:
        """When the leg is hedged, i.e End of Day (EOD)."""
        return self.__fixing_time

    @fixing_time.setter
    def fixing_time(self, value: str):
        self.__fixing_time = value
        self._property_changed('fixing_time')        

    @property
    def frequency(self) -> str:
        """What frequency the leg is hedged."""
        return self.__frequency

    @frequency.setter
    def frequency(self, value: str):
        self.__frequency = value
        self._property_changed('frequency')        

    @property
    def notional_percentage(self) -> float:
        """Percentage of notional to hedge."""
        return self.__notional_percentage

    @notional_percentage.setter
    def notional_percentage(self, value: float):
        self.__notional_percentage = value
        self._property_changed('notional_percentage')        


class EnhancedBetaUnderlier(Base):
        
    """Underlying asset and corresponding nearby adder and valid months"""
       
    def __init__(
        self,
        asset_id: str,
        month_add: float = None,
        valid_months: Tuple[str, ...] = None,
        is_included: bool = None,
        weight_scale: float = None        
    ):
        super().__init__()
        self.__asset_id = asset_id
        self.__month_add = month_add
        self.__valid_months = valid_months
        self.__is_included = is_included
        self.__weight_scale = weight_scale

    @property
    def asset_id(self) -> str:
        """Marquee unique asset identifier."""
        return self.__asset_id

    @asset_id.setter
    def asset_id(self, value: str):
        self.__asset_id = value
        self._property_changed('asset_id')        

    @property
    def month_add(self) -> float:
        """Allows users to roll to a contract farther in the future by the number of months specified."""
        return self.__month_add

    @month_add.setter
    def month_add(self, value: float):
        self.__month_add = value
        self._property_changed('month_add')        

    @property
    def valid_months(self) -> Tuple[str, ...]:
        """Valid months to which you can roll contracts."""
        return self.__valid_months

    @valid_months.setter
    def valid_months(self, value: Tuple[str, ...]):
        self.__valid_months = value
        self._property_changed('valid_months')        

    @property
    def is_included(self) -> bool:
        """True if underlier is included in user's strategy."""
        return self.__is_included

    @is_included.setter
    def is_included(self, value: bool):
        self.__is_included = value
        self._property_changed('is_included')        

    @property
    def weight_scale(self) -> float:
        """The percentage the underlier's weight is scaled."""
        return self.__weight_scale

    @weight_scale.setter
    def weight_scale(self, value: float):
        self.__weight_scale = value
        self._property_changed('weight_scale')        


class EnhancedBetaUnderlierRefData(Base):
        
    """Enhanced Beta Underlier reference data object."""
       
    def __init__(
        self,
        asset_id: str = None,
        valid_months: Tuple[str, ...] = None,
        current: bool = None        
    ):
        super().__init__()
        self.__asset_id = asset_id
        self.__valid_months = valid_months
        self.__current = current

    @property
    def asset_id(self) -> str:
        """Marquee unique asset identifier."""
        return self.__asset_id

    @asset_id.setter
    def asset_id(self, value: str):
        self.__asset_id = value
        self._property_changed('asset_id')        

    @property
    def valid_months(self) -> Tuple[str, ...]:
        """Valid months with contracts you can roll to"""
        return self.__valid_months

    @valid_months.setter
    def valid_months(self, value: Tuple[str, ...]):
        self.__valid_months = value
        self._property_changed('valid_months')        

    @property
    def current(self) -> bool:
        """True when underlier is currently in the base index, else false."""
        return self.__current

    @current.setter
    def current(self, value: bool):
        self.__current = value
        self._property_changed('current')        


class EntityCorrelation(Base):
        
    """entity correlation"""
       
    def __init__(
        self,
        primary_id: str = None,
        secondary_id: str = None,
        correlation: float = None        
    ):
        super().__init__()
        self.__primary_id = primary_id
        self.__secondary_id = secondary_id
        self.__correlation = correlation

    @property
    def primary_id(self) -> str:
        """Marquee unique identifier for the primary underlying asset in the correlation"""
        return self.__primary_id

    @primary_id.setter
    def primary_id(self, value: str):
        self.__primary_id = value
        self._property_changed('primary_id')        

    @property
    def secondary_id(self) -> str:
        """Marquee unique identifier for the secondary underlying asset in the correlation"""
        return self.__secondary_id

    @secondary_id.setter
    def secondary_id(self, value: str):
        self.__secondary_id = value
        self._property_changed('secondary_id')        

    @property
    def correlation(self) -> float:
        """Correlation between the primary and secondary underliers"""
        return self.__correlation

    @correlation.setter
    def correlation(self, value: float):
        self.__correlation = value
        self._property_changed('correlation')        


class ExpirationRefData(Base):
        
    """Expiration reference data object."""
       
    def __init__(
        self,
        default: str = None,
        enum: Tuple[str, ...] = None        
    ):
        super().__init__()
        self.__default = default
        self.__enum = enum

    @property
    def default(self) -> str:
        """Default option expiration."""
        return self.__default

    @default.setter
    def default(self, value: str):
        self.__default = value
        self._property_changed('default')        

    @property
    def enum(self) -> Tuple[str, ...]:
        """Option expirations allowed."""
        return self.__enum

    @enum.setter
    def enum(self, value: Tuple[str, ...]):
        self.__enum = value
        self._property_changed('enum')        


class FixingTimeRefData(Base):
        
    """Fixing Time reference data object."""
       
    def __init__(
        self,
        default: str = None,
        enum: Tuple[str, ...] = None        
    ):
        super().__init__()
        self.__default = default
        self.__enum = enum

    @property
    def default(self) -> str:
        """Default hedge fixing time."""
        return self.__default

    @default.setter
    def default(self, value: str):
        self.__default = value
        self._property_changed('default')        

    @property
    def enum(self) -> Tuple[str, ...]:
        """Fixing times allowed."""
        return self.__enum

    @enum.setter
    def enum(self, value: Tuple[str, ...]):
        self.__enum = value
        self._property_changed('enum')        


class FrequencyRefData(Base):
        
    """Frequency reference data object."""
       
    def __init__(
        self,
        default: str = None,
        enum: Tuple[str, ...] = None        
    ):
        super().__init__()
        self.__default = default
        self.__enum = enum

    @property
    def default(self) -> str:
        """Default hedge fixing time."""
        return self.__default

    @default.setter
    def default(self, value: str):
        self.__default = value
        self._property_changed('default')        

    @property
    def enum(self) -> Tuple[str, ...]:
        """Fixing times allowed."""
        return self.__enum

    @enum.setter
    def enum(self, value: Tuple[str, ...]):
        self.__enum = value
        self._property_changed('enum')        


class LookBackPeriodRefData(Base):
        
    """Look back period reference data object."""
       
    def __init__(
        self,
        default: str = None,
        enum: Tuple[str, ...] = None        
    ):
        super().__init__()
        self.__default = default
        self.__enum = enum

    @property
    def default(self) -> str:
        """Default look back period."""
        return self.__default

    @default.setter
    def default(self, value: str):
        self.__default = value
        self._property_changed('default')        

    @property
    def enum(self) -> Tuple[str, ...]:
        """Look back periods allowed."""
        return self.__enum

    @enum.setter
    def enum(self, value: Tuple[str, ...]):
        self.__enum = value
        self._property_changed('enum')        


class NotionalPercentageRefData(Base):
        
    """Notional Percentage Reference Data"""
       
    def __init__(
        self,
        default: float = None,
        min: float = None,
        max: float = None        
    ):
        super().__init__()
        self.__default = default
        self.__min = min
        self.__max = max

    @property
    def default(self) -> float:
        """Default notional percentage."""
        return self.__default

    @default.setter
    def default(self, value: float):
        self.__default = value
        self._property_changed('default')        

    @property
    def min(self) -> float:
        """Minimum notional percentage allowed."""
        return self.__min

    @min.setter
    def min(self, value: float):
        self.__min = value
        self._property_changed('min')        

    @property
    def max(self) -> float:
        """Maximum notional percentage allowed."""
        return self.__max

    @max.setter
    def max(self, value: float):
        self.__max = value
        self._property_changed('max')        


class OptionStrikeTypeRefData(Base):
        
    """Option strike type reference data object."""
       
    def __init__(
        self,
        default: str = None,
        enum: Tuple[str, ...] = None        
    ):
        super().__init__()
        self.__default = default
        self.__enum = enum

    @property
    def default(self) -> str:
        """Default option strike type."""
        return self.__default

    @default.setter
    def default(self, value: str):
        self.__default = value
        self._property_changed('default')        

    @property
    def enum(self) -> Tuple[str, ...]:
        """Option strike types allowed."""
        return self.__enum

    @enum.setter
    def enum(self, value: Tuple[str, ...]):
        self.__enum = value
        self._property_changed('enum')        


class OptionTypeRefData(Base):
        
    """Option Type reference data object."""
       
    def __init__(
        self,
        default: str = None,
        enum: Tuple[str, ...] = None        
    ):
        super().__init__()
        self.__default = default
        self.__enum = enum

    @property
    def default(self) -> str:
        """Default option type."""
        return self.__default

    @default.setter
    def default(self, value: str):
        self.__default = value
        self._property_changed('default')        

    @property
    def enum(self) -> Tuple[str, ...]:
        """Option types allowed."""
        return self.__enum

    @enum.setter
    def enum(self, value: Tuple[str, ...]):
        self.__enum = value
        self._property_changed('enum')        


class PerformanceRange(Base):
        
    """a unit of performance"""
       
    def __init__(
        self,
        horizon: str = None,
        stats: PerformanceStats = None        
    ):
        super().__init__()
        self.__horizon = horizon
        self.__stats = stats

    @property
    def horizon(self) -> str:
        """description of the time range"""
        return self.__horizon

    @horizon.setter
    def horizon(self, value: str):
        self.__horizon = value
        self._property_changed('horizon')        

    @property
    def stats(self) -> PerformanceStats:
        """Performance statistics."""
        return self.__stats

    @stats.setter
    def stats(self, value: PerformanceStats):
        self.__stats = value
        self._property_changed('stats')        


class ScalingMethodRefData(Base):
        
    """Scaling Method Reference Data"""
       
    def __init__(
        self,
        default: str = None,
        enum: Tuple[str, ...] = None        
    ):
        super().__init__()
        self.__default = default
        self.__enum = enum

    @property
    def default(self) -> str:
        """Default scaling method."""
        return self.__default

    @default.setter
    def default(self, value: str):
        self.__default = value
        self._property_changed('default')        

    @property
    def enum(self) -> Tuple[str, ...]:
        """Scaling methods allowed."""
        return self.__enum

    @enum.setter
    def enum(self, value: Tuple[str, ...]):
        self.__enum = value
        self._property_changed('enum')        


class StrikeRefData(Base):
        
    """Strike reference data object."""
       
    def __init__(
        self,
        default: float = None,
        min: float = None,
        max: float = None        
    ):
        super().__init__()
        self.__default = default
        self.__min = min
        self.__max = max

    @property
    def default(self) -> float:
        """Default strike."""
        return self.__default

    @default.setter
    def default(self, value: float):
        self.__default = value
        self._property_changed('default')        

    @property
    def min(self) -> float:
        """Minimum strike allowed."""
        return self.__min

    @min.setter
    def min(self, value: float):
        self.__min = value
        self._property_changed('min')        

    @property
    def max(self) -> float:
        """Maximum strike allowed."""
        return self.__max

    @max.setter
    def max(self, value: float):
        self.__max = value
        self._property_changed('max')        


class TradeInMethodRefData(Base):
        
    """Trade In Method Reference Data"""
       
    def __init__(
        self,
        default: str = None,
        enum: Tuple[str, ...] = None        
    ):
        super().__init__()
        self.__default = default
        self.__enum = enum

    @property
    def default(self) -> str:
        """Default trade in method."""
        return self.__default

    @default.setter
    def default(self, value: str):
        self.__default = value
        self._property_changed('default')        

    @property
    def enum(self) -> Tuple[str, ...]:
        """Trade in methods allowed."""
        return self.__enum

    @enum.setter
    def enum(self, value: Tuple[str, ...]):
        self.__enum = value
        self._property_changed('enum')        


class TradeInTimeRefData(Base):
        
    """Trade In Time Reference Data"""
       
    def __init__(
        self,
        default: str = None,
        enum: Tuple[str, ...] = None        
    ):
        super().__init__()
        self.__default = default
        self.__enum = enum

    @property
    def default(self) -> str:
        """Default trade in time."""
        return self.__default

    @default.setter
    def default(self, value: str):
        self.__default = value
        self._property_changed('default')        

    @property
    def enum(self) -> Tuple[str, ...]:
        """Trade in times allowed."""
        return self.__enum

    @enum.setter
    def enum(self, value: Tuple[str, ...]):
        self.__enum = value
        self._property_changed('enum')        


class Underlier(Base):
        
    """Underlying asset and corresponding weight"""
       
    def __init__(
        self,
        asset_id: str = None,
        weight: float = None        
    ):
        super().__init__()
        self.__asset_id = asset_id
        self.__weight = weight

    @property
    def asset_id(self) -> str:
        """Marquee unique asset identifier."""
        return self.__asset_id

    @asset_id.setter
    def asset_id(self, value: str):
        self.__asset_id = value
        self._property_changed('asset_id')        

    @property
    def weight(self) -> float:
        """Percentage of notional."""
        return self.__weight

    @weight.setter
    def weight(self, value: float):
        self.__weight = value
        self._property_changed('weight')        


class VolatilityWeightedWeightingModifier(Base):
        
    """Volatility Weighted backtest weighting modifier."""
       
    def __init__(
        self,
        em_aalpha: float = None,
        look_back_period: str = None,
        use_log_return: bool = False        
    ):
        super().__init__()
        self.__em_aalpha = em_aalpha
        self.__look_back_period = look_back_period
        self.__use_log_return = use_log_return

    @property
    def name(self) -> str:
        """Name of the Modifier"""
        return 'Volatility Weighted'        

    @property
    def em_aalpha(self) -> float:
        """Alpha value for Exponentially Weighted Moving Average Volatility; set to 0 if standard volatility."""
        return self.__em_aalpha

    @em_aalpha.setter
    def em_aalpha(self, value: float):
        self.__em_aalpha = value
        self._property_changed('em_aalpha')        

    @property
    def look_back_period(self) -> str:
        """Look back period to measure volatility for each underlier."""
        return self.__look_back_period

    @look_back_period.setter
    def look_back_period(self, value: str):
        self.__look_back_period = value
        self._property_changed('look_back_period')        

    @property
    def use_log_return(self) -> bool:
        """Whether to use Log Returns instead of Arithmetic Returns for volatility calculation."""
        return self.__use_log_return

    @use_log_return.setter
    def use_log_return(self, value: bool):
        self.__use_log_return = value
        self._property_changed('use_log_return')        


class VolatilityWeightedWeightingModifierRefData(Base):
        
    """Volatility Weighted Weighting Modifier reference data object."""
       
    def __init__(
        self,
        em_aalpha: dict = None,
        look_back_period: dict = None        
    ):
        super().__init__()
        self.__em_aalpha = em_aalpha
        self.__look_back_period = look_back_period

    @property
    def em_aalpha(self) -> dict:
        """Alpha value for Exponentially Weighted Moving Average Volatility reference data object."""
        return self.__em_aalpha

    @em_aalpha.setter
    def em_aalpha(self, value: dict):
        self.__em_aalpha = value
        self._property_changed('em_aalpha')        

    @property
    def look_back_period(self) -> dict:
        """Lookback period to measure volatility for each underlier reference data object. """
        return self.__look_back_period

    @look_back_period.setter
    def look_back_period(self, value: dict):
        self.__look_back_period = value
        self._property_changed('look_back_period')        


class BacktestResult(Base):
        
    """backtest result"""
       
    def __init__(
        self,
        backtest_id: str = None,
        performance: Tuple[FieldValueMap, ...] = None,
        stats: PerformanceStats = None,
        performance_decompositions: Tuple[BacktestPerformanceDecomposition, ...] = None,
        risks: Tuple[BacktestRisk, ...] = None,
        history: Tuple[PerformanceRange, ...] = None,
        underlier_correlation: Tuple[EntityCorrelation, ...] = None,
        comparisons: Tuple[BacktestComparison, ...] = None,
        backtest_version: float = None        
    ):
        super().__init__()
        self.__backtest_id = backtest_id
        self.__performance = performance
        self.__stats = stats
        self.__performance_decompositions = performance_decompositions
        self.__risks = risks
        self.__history = history
        self.__underlier_correlation = underlier_correlation
        self.__comparisons = comparisons
        self.__backtest_version = backtest_version

    @property
    def backtest_id(self) -> str:
        """Marquee unique backtest identifier"""
        return self.__backtest_id

    @backtest_id.setter
    def backtest_id(self, value: str):
        self.__backtest_id = value
        self._property_changed('backtest_id')        

    @property
    def performance(self) -> Tuple[FieldValueMap, ...]:
        """Backtest performance curve."""
        return self.__performance

    @performance.setter
    def performance(self, value: Tuple[FieldValueMap, ...]):
        self.__performance = value
        self._property_changed('performance')        

    @property
    def stats(self) -> PerformanceStats:
        """Performance statistics."""
        return self.__stats

    @stats.setter
    def stats(self, value: PerformanceStats):
        self.__stats = value
        self._property_changed('stats')        

    @property
    def performance_decompositions(self) -> Tuple[BacktestPerformanceDecomposition, ...]:
        """Decompositions of the performance of the backtest"""
        return self.__performance_decompositions

    @performance_decompositions.setter
    def performance_decompositions(self, value: Tuple[BacktestPerformanceDecomposition, ...]):
        self.__performance_decompositions = value
        self._property_changed('performance_decompositions')        

    @property
    def risks(self) -> Tuple[BacktestRisk, ...]:
        """Risks of the backtest portfolio"""
        return self.__risks

    @risks.setter
    def risks(self, value: Tuple[BacktestRisk, ...]):
        self.__risks = value
        self._property_changed('risks')        

    @property
    def history(self) -> Tuple[PerformanceRange, ...]:
        """Backtest historical calculations."""
        return self.__history

    @history.setter
    def history(self, value: Tuple[PerformanceRange, ...]):
        self.__history = value
        self._property_changed('history')        

    @property
    def underlier_correlation(self) -> Tuple[EntityCorrelation, ...]:
        """entity correlation"""
        return self.__underlier_correlation

    @underlier_correlation.setter
    def underlier_correlation(self, value: Tuple[EntityCorrelation, ...]):
        self.__underlier_correlation = value
        self._property_changed('underlier_correlation')        

    @property
    def comparisons(self) -> Tuple[BacktestComparison, ...]:
        """Array of comparisons btw the backtest and comparison entity."""
        return self.__comparisons

    @comparisons.setter
    def comparisons(self, value: Tuple[BacktestComparison, ...]):
        self.__comparisons = value
        self._property_changed('comparisons')        

    @property
    def backtest_version(self) -> float:
        """Backtest version number."""
        return self.__backtest_version

    @backtest_version.setter
    def backtest_version(self, value: float):
        self.__backtest_version = value
        self._property_changed('backtest_version')        


class BacktestRiskRequest(Base):
        
    """Request to compute Backtest Price and Risk"""
       
    def __init__(
        self,
        positions: Tuple[BacktestRiskPosition, ...],
        measures: Tuple[Union[BacktestRiskMeasureType, str], ...],
        start_date: datetime.date = None,
        end_date: datetime.date = None        
    ):
        super().__init__()
        self.__positions = positions
        self.__measures = measures
        self.__start_date = start_date
        self.__end_date = end_date

    @property
    def positions(self) -> Tuple[BacktestRiskPosition, ...]:
        """The positions on which to run the risk calculation"""
        return self.__positions

    @positions.setter
    def positions(self, value: Tuple[BacktestRiskPosition, ...]):
        self.__positions = value
        self._property_changed('positions')        

    @property
    def measures(self) -> Tuple[Union[BacktestRiskMeasureType, str], ...]:
        """A collection of risk measures to compute. E.g. { 'measureType': 'Delta', 'assetClass': 'Equity'"""
        return self.__measures

    @measures.setter
    def measures(self, value: Tuple[Union[BacktestRiskMeasureType, str], ...]):
        self.__measures = value
        self._property_changed('measures')        

    @property
    def start_date(self) -> datetime.date:
        """Start date of backtest risk computation selected by user."""
        return self.__start_date

    @start_date.setter
    def start_date(self, value: datetime.date):
        self.__start_date = value
        self._property_changed('start_date')        

    @property
    def end_date(self) -> datetime.date:
        """End date of backtest risk computation selected by user. If not selected, defaults to the last date for which we can compute price"""
        return self.__end_date

    @end_date.setter
    def end_date(self, value: datetime.date):
        self.__end_date = value
        self._property_changed('end_date')        


class BacktestStrategyUnderlierHedge(Base):
        
    """Hedge information for the backtest underlier"""
       
    def __init__(
        self,
        risk_details: DeltaHedgeParameters = None,
        quantity_percentage: float = None        
    ):
        super().__init__()
        self.__risk_details = risk_details
        self.__quantity_percentage = quantity_percentage

    @property
    def risk_details(self) -> DeltaHedgeParameters:
        """details of the risk being hedged"""
        return self.__risk_details

    @risk_details.setter
    def risk_details(self, value: DeltaHedgeParameters):
        self.__risk_details = value
        self._property_changed('risk_details')        

    @property
    def quantity_percentage(self) -> float:
        """Percentage of quantity to hedge"""
        return self.__quantity_percentage

    @quantity_percentage.setter
    def quantity_percentage(self, value: float):
        self.__quantity_percentage = value
        self._property_changed('quantity_percentage')        


class BasketBacktestParameters(Base):
        
    """Parameters of a Basket backtest."""
       
    def __init__(
        self,
        underliers: Tuple[Underlier, ...],
        rebalance_parameters: BacktestRebalanceParameters = None,
        weighting_modifiers: Tuple[VolatilityWeightedWeightingModifier, ...] = None,
        weighting_strategy: str = None        
    ):
        super().__init__()
        self.__rebalance_parameters = rebalance_parameters
        self.__underliers = underliers
        self.__weighting_modifiers = weighting_modifiers
        self.__weighting_strategy = weighting_strategy

    @property
    def rebalance_parameters(self) -> BacktestRebalanceParameters:
        """Parameters relating to the backtest's rebalance"""
        return self.__rebalance_parameters

    @rebalance_parameters.setter
    def rebalance_parameters(self, value: BacktestRebalanceParameters):
        self.__rebalance_parameters = value
        self._property_changed('rebalance_parameters')        

    @property
    def underliers(self) -> Tuple[Underlier, ...]:
        """Underlying assets for the backtest"""
        return self.__underliers

    @underliers.setter
    def underliers(self, value: Tuple[Underlier, ...]):
        self.__underliers = value
        self._property_changed('underliers')        

    @property
    def weighting_modifiers(self) -> Tuple[VolatilityWeightedWeightingModifier, ...]:
        """Weighting modifiers for the backtest."""
        return self.__weighting_modifiers

    @weighting_modifiers.setter
    def weighting_modifiers(self, value: Tuple[VolatilityWeightedWeightingModifier, ...]):
        self.__weighting_modifiers = value
        self._property_changed('weighting_modifiers')        

    @property
    def weighting_strategy(self) -> str:
        """Strategy for determining the weight of the backtest underliers."""
        return self.__weighting_strategy

    @weighting_strategy.setter
    def weighting_strategy(self, value: str):
        self.__weighting_strategy = value
        self._property_changed('weighting_strategy')        


class BasketBacktestRefData(Base):
        
    """Basket backtest reference data"""
       
    def __init__(
        self,
        currency: CurrencyRefData = None,
        look_back_period: LookBackPeriodRefData = None,
        weighting_strategy: dict = None,
        weighting_modifiers: dict = None        
    ):
        super().__init__()
        self.__currency = currency
        self.__look_back_period = look_back_period
        self.__weighting_strategy = weighting_strategy
        self.__weighting_modifiers = weighting_modifiers

    @property
    def currency(self) -> CurrencyRefData:
        """Currency Reference Data"""
        return self.__currency

    @currency.setter
    def currency(self, value: CurrencyRefData):
        self.__currency = value
        self._property_changed('currency')        

    @property
    def look_back_period(self) -> LookBackPeriodRefData:
        """Look back period reference data object."""
        return self.__look_back_period

    @look_back_period.setter
    def look_back_period(self, value: LookBackPeriodRefData):
        self.__look_back_period = value
        self._property_changed('look_back_period')        

    @property
    def weighting_strategy(self) -> dict:
        """Weighting strategy reference data object."""
        return self.__weighting_strategy

    @weighting_strategy.setter
    def weighting_strategy(self, value: dict):
        self.__weighting_strategy = value
        self._property_changed('weighting_strategy')        

    @property
    def weighting_modifiers(self) -> dict:
        """Weighting Modifiers reference data object."""
        return self.__weighting_modifiers

    @weighting_modifiers.setter
    def weighting_modifiers(self, value: dict):
        self.__weighting_modifiers = value
        self._property_changed('weighting_modifiers')        


class DeltaHedgingRefData(Base):
        
    """Delta Hedging Reference Data"""
       
    def __init__(
        self,
        fixing_time: FixingTimeRefData = None,
        frequency: FrequencyRefData = None,
        notional_percentage: NotionalPercentageRefData = None        
    ):
        super().__init__()
        self.__fixing_time = fixing_time
        self.__frequency = frequency
        self.__notional_percentage = notional_percentage

    @property
    def fixing_time(self) -> FixingTimeRefData:
        """Fixing Time reference data object."""
        return self.__fixing_time

    @fixing_time.setter
    def fixing_time(self, value: FixingTimeRefData):
        self.__fixing_time = value
        self._property_changed('fixing_time')        

    @property
    def frequency(self) -> FrequencyRefData:
        """Frequency reference data object."""
        return self.__frequency

    @frequency.setter
    def frequency(self, value: FrequencyRefData):
        self.__frequency = value
        self._property_changed('frequency')        

    @property
    def notional_percentage(self) -> NotionalPercentageRefData:
        """Notional Percentage Reference Data"""
        return self.__notional_percentage

    @notional_percentage.setter
    def notional_percentage(self, value: NotionalPercentageRefData):
        self.__notional_percentage = value
        self._property_changed('notional_percentage')        


class EnhancedBetaBacktestParameters(Base):
        
    """Parameters of an Enhanced Beta backtest."""
       
    def __init__(
        self,
        underliers: Tuple[EnhancedBetaUnderlier, ...],
        roll_start: float,
        roll_end: float,
        base_index: str        
    ):
        super().__init__()
        self.__roll_start = roll_start
        self.__roll_end = roll_end
        self.__base_index = base_index
        self.__underliers = underliers

    @property
    def roll_start(self) -> float:
        """Business day on which to begin rolling."""
        return self.__roll_start

    @roll_start.setter
    def roll_start(self, value: float):
        self.__roll_start = value
        self._property_changed('roll_start')        

    @property
    def roll_end(self) -> float:
        """Business day on which to finish rolling."""
        return self.__roll_end

    @roll_end.setter
    def roll_end(self, value: float):
        self.__roll_end = value
        self._property_changed('roll_end')        

    @property
    def base_index(self) -> str:
        """Base index which strategy is attempting to beat."""
        return self.__base_index

    @base_index.setter
    def base_index(self, value: str):
        self.__base_index = value
        self._property_changed('base_index')        

    @property
    def underliers(self) -> Tuple[EnhancedBetaUnderlier, ...]:
        """Assets included in the user's strategy."""
        return self.__underliers

    @underliers.setter
    def underliers(self, value: Tuple[EnhancedBetaUnderlier, ...]):
        self.__underliers = value
        self._property_changed('underliers')        


class EnhancedBetaRefData(Base):
        
    """Enhanced Beta backtest reference data"""
       
    def __init__(
        self,
        look_back_period: LookBackPeriodRefData = None,
        currency: CurrencyRefData = None,
        base_index: BaseIndexRefData = None,
        MASJ8W49Y02X9CGS: dict = None,
        MAAHST8JED9B607H: dict = None        
    ):
        super().__init__()
        self.__look_back_period = look_back_period
        self.__currency = currency
        self.__base_index = base_index
        self.__MASJ8W49Y02X9CGS = MASJ8W49Y02X9CGS
        self.__MAAHST8JED9B607H = MAAHST8JED9B607H

    @property
    def look_back_period(self) -> LookBackPeriodRefData:
        """Look back period reference data object."""
        return self.__look_back_period

    @look_back_period.setter
    def look_back_period(self, value: LookBackPeriodRefData):
        self.__look_back_period = value
        self._property_changed('look_back_period')        

    @property
    def currency(self) -> CurrencyRefData:
        """Currency Reference Data"""
        return self.__currency

    @currency.setter
    def currency(self, value: CurrencyRefData):
        self.__currency = value
        self._property_changed('currency')        

    @property
    def base_index(self) -> BaseIndexRefData:
        """Base index reference data object."""
        return self.__base_index

    @base_index.setter
    def base_index(self, value: BaseIndexRefData):
        self.__base_index = value
        self._property_changed('base_index')        

    @property
    def MASJ8W49Y02X9CGS(self) -> dict:
        return self.__MASJ8W49Y02X9CGS

    @MASJ8W49Y02X9CGS.setter
    def MASJ8W49Y02X9CGS(self, value: dict):
        self.__MASJ8W49Y02X9CGS = value
        self._property_changed('MASJ8W49Y02X9CGS')        

    @property
    def MAAHST8JED9B607H(self) -> dict:
        return self.__MAAHST8JED9B607H

    @MAAHST8JED9B607H.setter
    def MAAHST8JED9B607H(self, value: dict):
        self.__MAAHST8JED9B607H = value
        self._property_changed('MAAHST8JED9B607H')        


class OptionBacktestUnderlier(Base):
        
    """Option Backtest Undelier."""
       
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
        trade_in_time: str = None        
    ):
        super().__init__()
        self.__buy_sell = buy_sell
        self.__expiration = expiration
        self.__option_type = option_type
        self.__option_strike_type = option_strike_type
        self.__notional_percentage = notional_percentage
        self.__strike = strike
        self.__underlying_asset_id = underlying_asset_id
        self.__delta_hedging = delta_hedging
        self.__trade_in_time = trade_in_time

    @property
    def buy_sell(self) -> str:
        """Option position, i.e buy"""
        return self.__buy_sell

    @buy_sell.setter
    def buy_sell(self, value: str):
        self.__buy_sell = value
        self._property_changed('buy_sell')        

    @property
    def expiration(self) -> str:
        """Time until expiration."""
        return self.__expiration

    @expiration.setter
    def expiration(self, value: str):
        self.__expiration = value
        self._property_changed('expiration')        

    @property
    def option_type(self) -> str:
        """Type of option, i.e call."""
        return self.__option_type

    @option_type.setter
    def option_type(self, value: str):
        self.__option_type = value
        self._property_changed('option_type')        

    @property
    def option_strike_type(self) -> str:
        """Type of option strike, i.e relative."""
        return self.__option_strike_type

    @option_strike_type.setter
    def option_strike_type(self, value: str):
        self.__option_strike_type = value
        self._property_changed('option_strike_type')        

    @property
    def notional_percentage(self) -> float:
        """The percentage to increase/decrease your position on the leg."""
        return self.__notional_percentage

    @notional_percentage.setter
    def notional_percentage(self, value: float):
        self.__notional_percentage = value
        self._property_changed('notional_percentage')        

    @property
    def strike(self) -> float:
        """Strike percentage, either relative % or delta % depending on strike type."""
        return self.__strike

    @strike.setter
    def strike(self, value: float):
        self.__strike = value
        self._property_changed('strike')        

    @property
    def underlying_asset_id(self) -> str:
        """Marquee unique asset identifier."""
        return self.__underlying_asset_id

    @underlying_asset_id.setter
    def underlying_asset_id(self, value: str):
        self.__underlying_asset_id = value
        self._property_changed('underlying_asset_id')        

    @property
    def delta_hedging(self) -> DeltaHedgingParameters:
        """Parameters for delta hedging an option."""
        return self.__delta_hedging

    @delta_hedging.setter
    def delta_hedging(self, value: DeltaHedgingParameters):
        self.__delta_hedging = value
        self._property_changed('delta_hedging')        

    @property
    def trade_in_time(self) -> str:
        """When from now to trade out the leg (must be less than expiration)."""
        return self.__trade_in_time

    @trade_in_time.setter
    def trade_in_time(self, value: str):
        self.__trade_in_time = value
        self._property_changed('trade_in_time')        


class UnderlyingAssetIdDataRefData(Base):
        
    """Underlying asset id data reference data object."""
       
    def __init__(
        self,
        asset_id: str = None,
        fixing_time: FixingTimeRefData = None,
        frequency: FrequencyRefData = None        
    ):
        super().__init__()
        self.__asset_id = asset_id
        self.__fixing_time = fixing_time
        self.__frequency = frequency

    @property
    def asset_id(self) -> str:
        """Marquee unique asset identifier."""
        return self.__asset_id

    @asset_id.setter
    def asset_id(self, value: str):
        self.__asset_id = value
        self._property_changed('asset_id')        

    @property
    def fixing_time(self) -> FixingTimeRefData:
        """Fixing Time reference data object."""
        return self.__fixing_time

    @fixing_time.setter
    def fixing_time(self, value: FixingTimeRefData):
        self.__fixing_time = value
        self._property_changed('fixing_time')        

    @property
    def frequency(self) -> FrequencyRefData:
        """Frequency reference data object."""
        return self.__frequency

    @frequency.setter
    def frequency(self, value: FrequencyRefData):
        self.__frequency = value
        self._property_changed('frequency')        


class BacktestStrategyUnderlier(Base):
        
    """Backtest Strategy Undelier."""
       
    def __init__(
        self,
        instrument: dict,
        market_model: str,
        notional_percentage: float = None,
        name: str = None,
        hedge: BacktestStrategyUnderlierHedge = None        
    ):
        super().__init__()
        self.__instrument = instrument
        self.__notional_percentage = notional_percentage
        self.__market_model = market_model
        self.__name = name
        self.__hedge = hedge

    @property
    def instrument(self) -> dict:
        """instrument that you are getting into"""
        return self.__instrument

    @instrument.setter
    def instrument(self, value: dict):
        self.__instrument = value
        self._property_changed('instrument')        

    @property
    def notional_percentage(self) -> float:
        """The quantity of the underlier"""
        return self.__notional_percentage

    @notional_percentage.setter
    def notional_percentage(self, value: float):
        self.__notional_percentage = value
        self._property_changed('notional_percentage')        

    @property
    def market_model(self) -> str:
        """Market model used for the underlier."""
        return self.__market_model

    @market_model.setter
    def market_model(self, value: str):
        self.__market_model = value
        self._property_changed('market_model')        

    @property
    def name(self) -> str:
        """identifying name for the backtest leg"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def hedge(self) -> BacktestStrategyUnderlierHedge:
        """Hedge information for the backtest underlier"""
        return self.__hedge

    @hedge.setter
    def hedge(self, value: BacktestStrategyUnderlierHedge):
        self.__hedge = value
        self._property_changed('hedge')        


class UnderlyingAssetIdRefData(Base):
        
    """Underlying asset id reference data object."""
       
    def __init__(
        self,
        default: str = None,
        enum: Tuple[str, ...] = None,
        data: Tuple[UnderlyingAssetIdDataRefData, ...] = None        
    ):
        super().__init__()
        self.__default = default
        self.__enum = enum
        self.__data = data

    @property
    def default(self) -> str:
        """Default asset id underlying the option."""
        return self.__default

    @default.setter
    def default(self, value: str):
        self.__default = value
        self._property_changed('default')        

    @property
    def enum(self) -> Tuple[str, ...]:
        """Asset ids allowed to underly the option."""
        return self.__enum

    @enum.setter
    def enum(self, value: Tuple[str, ...]):
        self.__enum = value
        self._property_changed('enum')        

    @property
    def data(self) -> Tuple[UnderlyingAssetIdDataRefData, ...]:
        """Underlying asset id data reference data object."""
        return self.__data

    @data.setter
    def data(self, value: Tuple[UnderlyingAssetIdDataRefData, ...]):
        self.__data = value
        self._property_changed('data')        


class VolatilityBacktestParameters(Base):
        
    """Parameters of a Volatility backtest."""
       
    def __init__(
        self,
        underliers: Tuple[OptionBacktestUnderlier, ...],
        trade_in_method: str = None,
        scaling_method: str = None        
    ):
        super().__init__()
        self.__underliers = underliers
        self.__trade_in_method = trade_in_method
        self.__scaling_method = scaling_method

    @property
    def underliers(self) -> Tuple[OptionBacktestUnderlier, ...]:
        """Underlying assets of the backtest"""
        return self.__underliers

    @underliers.setter
    def underliers(self, value: Tuple[OptionBacktestUnderlier, ...]):
        self.__underliers = value
        self._property_changed('underliers')        

    @property
    def trade_in_method(self) -> str:
        """Method used to trade in legs before expiry."""
        return self.__trade_in_method

    @trade_in_method.setter
    def trade_in_method(self, value: str):
        self.__trade_in_method = value
        self._property_changed('trade_in_method')        

    @property
    def scaling_method(self) -> str:
        """The method for scaling legs, i.e percentage of NAV"""
        return self.__scaling_method

    @scaling_method.setter
    def scaling_method(self, value: str):
        self.__scaling_method = value
        self._property_changed('scaling_method')        


class VolBacktestRefData(Base):
        
    """Volatility backtest reference data"""
       
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
        trade_in_time: TradeInTimeRefData = None        
    ):
        super().__init__()
        self.__buy_sell = buy_sell
        self.__currency = currency
        self.__delta_hedging = delta_hedging
        self.__delta_strike = delta_strike
        self.__notional_percentage = notional_percentage
        self.__expiration = expiration
        self.__look_back_period = look_back_period
        self.__option_type = option_type
        self.__option_strike_type = option_strike_type
        self.__relative_strike = relative_strike
        self.__strike = strike
        self.__scaling_method = scaling_method
        self.__underlying_asset_id = underlying_asset_id
        self.__trade_in_method = trade_in_method
        self.__trade_in_time = trade_in_time

    @property
    def buy_sell(self) -> BuySellRefData:
        """Buy Sell reference data object."""
        return self.__buy_sell

    @buy_sell.setter
    def buy_sell(self, value: BuySellRefData):
        self.__buy_sell = value
        self._property_changed('buy_sell')        

    @property
    def currency(self) -> CurrencyRefData:
        """Currency Reference Data"""
        return self.__currency

    @currency.setter
    def currency(self, value: CurrencyRefData):
        self.__currency = value
        self._property_changed('currency')        

    @property
    def delta_hedging(self) -> DeltaHedgingRefData:
        """Delta Hedging Reference Data"""
        return self.__delta_hedging

    @delta_hedging.setter
    def delta_hedging(self, value: DeltaHedgingRefData):
        self.__delta_hedging = value
        self._property_changed('delta_hedging')        

    @property
    def delta_strike(self) -> StrikeRefData:
        """Strike reference data object."""
        return self.__delta_strike

    @delta_strike.setter
    def delta_strike(self, value: StrikeRefData):
        self.__delta_strike = value
        self._property_changed('delta_strike')        

    @property
    def notional_percentage(self) -> NotionalPercentageRefData:
        """Notional Percentage Reference Data"""
        return self.__notional_percentage

    @notional_percentage.setter
    def notional_percentage(self, value: NotionalPercentageRefData):
        self.__notional_percentage = value
        self._property_changed('notional_percentage')        

    @property
    def expiration(self) -> ExpirationRefData:
        """Expiration reference data object."""
        return self.__expiration

    @expiration.setter
    def expiration(self, value: ExpirationRefData):
        self.__expiration = value
        self._property_changed('expiration')        

    @property
    def look_back_period(self) -> LookBackPeriodRefData:
        """Look back period reference data object."""
        return self.__look_back_period

    @look_back_period.setter
    def look_back_period(self, value: LookBackPeriodRefData):
        self.__look_back_period = value
        self._property_changed('look_back_period')        

    @property
    def option_type(self) -> OptionTypeRefData:
        """Option Type reference data object."""
        return self.__option_type

    @option_type.setter
    def option_type(self, value: OptionTypeRefData):
        self.__option_type = value
        self._property_changed('option_type')        

    @property
    def option_strike_type(self) -> OptionStrikeTypeRefData:
        """Option strike type reference data object."""
        return self.__option_strike_type

    @option_strike_type.setter
    def option_strike_type(self, value: OptionStrikeTypeRefData):
        self.__option_strike_type = value
        self._property_changed('option_strike_type')        

    @property
    def relative_strike(self) -> StrikeRefData:
        """Strike reference data object."""
        return self.__relative_strike

    @relative_strike.setter
    def relative_strike(self, value: StrikeRefData):
        self.__relative_strike = value
        self._property_changed('relative_strike')        

    @property
    def strike(self) -> StrikeRefData:
        """Strike reference data object."""
        return self.__strike

    @strike.setter
    def strike(self, value: StrikeRefData):
        self.__strike = value
        self._property_changed('strike')        

    @property
    def scaling_method(self) -> ScalingMethodRefData:
        """Scaling Method Reference Data"""
        return self.__scaling_method

    @scaling_method.setter
    def scaling_method(self, value: ScalingMethodRefData):
        self.__scaling_method = value
        self._property_changed('scaling_method')        

    @property
    def underlying_asset_id(self) -> UnderlyingAssetIdRefData:
        """Underlying asset id reference data object."""
        return self.__underlying_asset_id

    @underlying_asset_id.setter
    def underlying_asset_id(self, value: UnderlyingAssetIdRefData):
        self.__underlying_asset_id = value
        self._property_changed('underlying_asset_id')        

    @property
    def trade_in_method(self) -> TradeInMethodRefData:
        """Trade In Method Reference Data"""
        return self.__trade_in_method

    @trade_in_method.setter
    def trade_in_method(self, value: TradeInMethodRefData):
        self.__trade_in_method = value
        self._property_changed('trade_in_method')        

    @property
    def trade_in_time(self) -> TradeInTimeRefData:
        """Trade In Time Reference Data"""
        return self.__trade_in_time

    @trade_in_time.setter
    def trade_in_time(self, value: TradeInTimeRefData):
        self.__trade_in_time = value
        self._property_changed('trade_in_time')        


class VolatilityFlowBacktestParameters(Base):
        
    """Parameters of a Volatility Flow Backtest."""
       
    def __init__(
        self,
        trading_parameters: BacktestTradingParameters,
        index_initial_value: float,
        underliers: Tuple[BacktestStrategyUnderlier, ...] = None,
        measures: Tuple[Union[FlowVolBacktestMeasure, str], ...] = ['ALL MEASURES']        
    ):
        super().__init__()
        self.__index_initial_value = index_initial_value
        self.__underliers = underliers
        self.__trading_parameters = trading_parameters
        self.__measures = measures

    @property
    def index_initial_value(self) -> float:
        """The initial index value of the strategy"""
        return self.__index_initial_value

    @index_initial_value.setter
    def index_initial_value(self, value: float):
        self.__index_initial_value = value
        self._property_changed('index_initial_value')        

    @property
    def underliers(self) -> Tuple[BacktestStrategyUnderlier, ...]:
        """Underlying units of the backtest strategy"""
        return self.__underliers

    @underliers.setter
    def underliers(self, value: Tuple[BacktestStrategyUnderlier, ...]):
        self.__underliers = value
        self._property_changed('underliers')        

    @property
    def trading_parameters(self) -> BacktestTradingParameters:
        """details about how to transact in the instrument"""
        return self.__trading_parameters

    @trading_parameters.setter
    def trading_parameters(self, value: BacktestTradingParameters):
        self.__trading_parameters = value
        self._property_changed('trading_parameters')        

    @property
    def measures(self) -> Tuple[Union[FlowVolBacktestMeasure, str], ...]:
        """Array of measures which should be calculated. By default all measures will be calculated"""
        return self.__measures

    @measures.setter
    def measures(self, value: Tuple[Union[FlowVolBacktestMeasure, str], ...]):
        self.__measures = value
        self._property_changed('measures')        


class Backtest(Base):
        
    """A backtest"""
       
    def __init__(
        self,
        name: str,
        type: Union[BacktestType, str],
        asset_class: Union[AssetClass, str],
        cost_netting: bool = False,
        created_by_id: str = None,
        created_time: datetime.datetime = None,
        currency: Union[Currency, str] = None,
        entitlements: Entitlements = None,
        entitlement_exclusions: EntitlementExclusions = None,
        id: str = None,
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
        self.__cost_netting = cost_netting
        self.__created_by_id = created_by_id
        self.__created_time = created_time
        self.__currency = get_enum_value(Currency, currency)
        self.__entitlements = entitlements
        self.__entitlement_exclusions = entitlement_exclusions
        self.__id = id
        self.__last_updated_by_id = last_updated_by_id
        self.__last_updated_time = last_updated_time
        self.__mq_symbol = mq_symbol
        self.__name = name
        self.__owner_id = owner_id
        self.__report_ids = report_ids
        self.__parameters = parameters
        self.__start_date = start_date
        self.__end_date = end_date
        self.__type = get_enum_value(BacktestType, type)
        self.__asset_class = get_enum_value(AssetClass, asset_class)
        self.__version = version

    @property
    def cost_netting(self) -> bool:
        """Nets trading costs across the leaf nodes of the strategy."""
        return self.__cost_netting

    @cost_netting.setter
    def cost_netting(self, value: bool):
        self.__cost_netting = value
        self._property_changed('cost_netting')        

    @property
    def created_by_id(self) -> str:
        """Unique identifier of user who created the object"""
        return self.__created_by_id

    @created_by_id.setter
    def created_by_id(self, value: str):
        self.__created_by_id = value
        self._property_changed('created_by_id')        

    @property
    def created_time(self) -> datetime.datetime:
        """Time created. ISO 8601 formatted string"""
        return self.__created_time

    @created_time.setter
    def created_time(self, value: datetime.datetime):
        self.__created_time = value
        self._property_changed('created_time')        

    @property
    def currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self.__currency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('currency')        

    @property
    def entitlements(self) -> Entitlements:
        """Defines the entitlements of a given resource"""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self.__entitlements = value
        self._property_changed('entitlements')        

    @property
    def entitlement_exclusions(self) -> EntitlementExclusions:
        """Defines the exclusion entitlements of a given resource"""
        return self.__entitlement_exclusions

    @entitlement_exclusions.setter
    def entitlement_exclusions(self, value: EntitlementExclusions):
        self.__entitlement_exclusions = value
        self._property_changed('entitlement_exclusions')        

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value
        self._property_changed('id')        

    @property
    def last_updated_by_id(self) -> str:
        """Unique identifier of user who last updated the object"""
        return self.__last_updated_by_id

    @last_updated_by_id.setter
    def last_updated_by_id(self, value: str):
        self.__last_updated_by_id = value
        self._property_changed('last_updated_by_id')        

    @property
    def last_updated_time(self) -> datetime.datetime:
        """Timestamp of when the object was last updated"""
        return self.__last_updated_time

    @last_updated_time.setter
    def last_updated_time(self, value: datetime.datetime):
        self.__last_updated_time = value
        self._property_changed('last_updated_time')        

    @property
    def mq_symbol(self) -> str:
        """Marquee unique symbol identifier for the backtest."""
        return self.__mq_symbol

    @mq_symbol.setter
    def mq_symbol(self, value: str):
        self.__mq_symbol = value
        self._property_changed('mq_symbol')        

    @property
    def name(self) -> str:
        """Display name of the basket"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def owner_id(self) -> str:
        """Marquee unique identifier"""
        return self.__owner_id

    @owner_id.setter
    def owner_id(self, value: str):
        self.__owner_id = value
        self._property_changed('owner_id')        

    @property
    def report_ids(self) -> Tuple[str, ...]:
        """Array of report identifiers related to the object"""
        return self.__report_ids

    @report_ids.setter
    def report_ids(self, value: Tuple[str, ...]):
        self.__report_ids = value
        self._property_changed('report_ids')        

    @property
    def parameters(self) -> dict:
        return self.__parameters

    @parameters.setter
    def parameters(self, value: dict):
        self.__parameters = value
        self._property_changed('parameters')        

    @property
    def start_date(self) -> datetime.date:
        """Start date of backtest selected by user. If not selected, defaults to start of backtest timeseries."""
        return self.__start_date

    @start_date.setter
    def start_date(self, value: datetime.date):
        self.__start_date = value
        self._property_changed('start_date')        

    @property
    def end_date(self) -> datetime.date:
        """End date of backtest selected by user. If not selected, defaults to end of backtest timeseries."""
        return self.__end_date

    @end_date.setter
    def end_date(self, value: datetime.date):
        self.__end_date = value
        self._property_changed('end_date')        

    @property
    def type(self) -> Union[BacktestType, str]:
        """Backtest type differentiates the backtest type."""
        return self.__type

    @type.setter
    def type(self, value: Union[BacktestType, str]):
        self.__type = value if isinstance(value, BacktestType) else get_enum_value(BacktestType, value)
        self._property_changed('type')        

    @property
    def asset_class(self) -> Union[AssetClass, str]:
        """Asset class of the backtest underliers."""
        return self.__asset_class

    @asset_class.setter
    def asset_class(self, value: Union[AssetClass, str]):
        self.__asset_class = value if isinstance(value, AssetClass) else get_enum_value(AssetClass, value)
        self._property_changed('asset_class')        

    @property
    def version(self) -> float:
        """Backtest version number."""
        return self.__version

    @version.setter
    def version(self, value: float):
        self.__version = value
        self._property_changed('version')        


class BacktestRefData(Base):
        
    """Backtest reference data"""
       
    def __init__(
        self,
        id: str = None,
        volatility: dict = None,
        enhanced_beta: EnhancedBetaRefData = None,
        basket: BasketBacktestRefData = None,
        owner_id: str = None,
        entitlements: Entitlements = None,
        entitlement_exclusions: EntitlementExclusions = None,
        last_updated_by_id: str = None,
        last_updated_time: datetime.datetime = None        
    ):
        super().__init__()
        self.__id = id
        self.__volatility = volatility
        self.__enhanced_beta = enhanced_beta
        self.__basket = basket
        self.__owner_id = owner_id
        self.__entitlements = entitlements
        self.__entitlement_exclusions = entitlement_exclusions
        self.__last_updated_by_id = last_updated_by_id
        self.__last_updated_time = last_updated_time

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value
        self._property_changed('id')        

    @property
    def volatility(self) -> dict:
        """Volatility backtest reference data."""
        return self.__volatility

    @volatility.setter
    def volatility(self, value: dict):
        self.__volatility = value
        self._property_changed('volatility')        

    @property
    def enhanced_beta(self) -> EnhancedBetaRefData:
        """Enhanced Beta backtest reference data"""
        return self.__enhanced_beta

    @enhanced_beta.setter
    def enhanced_beta(self, value: EnhancedBetaRefData):
        self.__enhanced_beta = value
        self._property_changed('enhanced_beta')        

    @property
    def basket(self) -> BasketBacktestRefData:
        """Basket backtest reference data"""
        return self.__basket

    @basket.setter
    def basket(self, value: BasketBacktestRefData):
        self.__basket = value
        self._property_changed('basket')        

    @property
    def owner_id(self) -> str:
        """Marquee unique identifier for user who owns the object."""
        return self.__owner_id

    @owner_id.setter
    def owner_id(self, value: str):
        self.__owner_id = value
        self._property_changed('owner_id')        

    @property
    def entitlements(self) -> Entitlements:
        """Defines the entitlements of a given resource"""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self.__entitlements = value
        self._property_changed('entitlements')        

    @property
    def entitlement_exclusions(self) -> EntitlementExclusions:
        """Defines the exclusion entitlements of a given resource"""
        return self.__entitlement_exclusions

    @entitlement_exclusions.setter
    def entitlement_exclusions(self, value: EntitlementExclusions):
        self.__entitlement_exclusions = value
        self._property_changed('entitlement_exclusions')        

    @property
    def last_updated_by_id(self) -> str:
        """Unique identifier of user who last updated the object"""
        return self.__last_updated_by_id

    @last_updated_by_id.setter
    def last_updated_by_id(self, value: str):
        self.__last_updated_by_id = value
        self._property_changed('last_updated_by_id')        

    @property
    def last_updated_time(self) -> datetime.datetime:
        """Timestamp of when the object was last updated"""
        return self.__last_updated_time

    @last_updated_time.setter
    def last_updated_time(self, value: datetime.datetime):
        self.__last_updated_time = value
        self._property_changed('last_updated_time')        
