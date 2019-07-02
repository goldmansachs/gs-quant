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

from gs_quant.base import Base, get_enum_value
from gs_quant.target.common import *
from typing import Tuple, Union
import datetime


class BacktestComparison(Base):
        
    """Comparison object for backtests"""
       
    def __init__(self, id: str = None, correlation: float = None):
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
       
    def __init__(self, name: str = None, stats: PerformanceStats = None):
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
       
    def __init__(self, frequencyPeriod: str = None, frequency: int = None, dayOfWeek: str = None, dayOfMonth: float = None):
        super().__init__()
        self.__frequencyPeriod = frequencyPeriod
        self.__frequency = frequency
        self.__dayOfWeek = dayOfWeek
        self.__dayOfMonth = dayOfMonth

    @property
    def frequencyPeriod(self) -> str:
        """What frequency period should be used for the rebalance"""
        return self.__frequencyPeriod

    @frequencyPeriod.setter
    def frequencyPeriod(self, value: str):
        self.__frequencyPeriod = value
        self._property_changed('frequencyPeriod')        

    @property
    def frequency(self) -> int:
        """What the frequency should be, given the frequency period, i.e. every 2 weeks"""
        return self.__frequency

    @frequency.setter
    def frequency(self, value: int):
        self.__frequency = value
        self._property_changed('frequency')        

    @property
    def dayOfWeek(self) -> str:
        """For weekly frequencyPeriod, the day of the week the rebalance should occur"""
        return self.__dayOfWeek

    @dayOfWeek.setter
    def dayOfWeek(self, value: str):
        self.__dayOfWeek = value
        self._property_changed('dayOfWeek')        

    @property
    def dayOfMonth(self) -> float:
        """For monthly frequencyPeriod rebalances, the day of the month the rebalance should occur"""
        return self.__dayOfMonth

    @dayOfMonth.setter
    def dayOfMonth(self, value: float):
        self.__dayOfMonth = value
        self._property_changed('dayOfMonth')        


class BacktestRisk(Base):
        
    """Risks of the backtest portfolio"""
       
    def __init__(self, name: str = None):
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


class BacktestTradingParameters(Base):
        
    """Trading Information for the Backtesting Strategy"""
       
    def __init__(self, quantityType: str = None, quantity: float = None, tradeInMethod: str = None, rollFrequency: str = None, scalingMethod: str = None):
        super().__init__()
        self.__quantityType = quantityType
        self.__quantity = quantity
        self.__tradeInMethod = tradeInMethod
        self.__rollFrequency = rollFrequency
        self.__scalingMethod = scalingMethod

    @property
    def quantityType(self) -> str:
        """The unit of the quantity of backtest strategy"""
        return self.__quantityType

    @quantityType.setter
    def quantityType(self, value: str):
        self.__quantityType = value
        self._property_changed('quantityType')        

    @property
    def quantity(self) -> float:
        """The quantity of backtest strategy"""
        return self.__quantity

    @quantity.setter
    def quantity(self, value: float):
        self.__quantity = value
        self._property_changed('quantity')        

    @property
    def tradeInMethod(self) -> str:
        """Roll method for the backtest strategy"""
        return self.__tradeInMethod

    @tradeInMethod.setter
    def tradeInMethod(self, value: str):
        self.__tradeInMethod = value
        self._property_changed('tradeInMethod')        

    @property
    def rollFrequency(self) -> str:
        """Period the strategy rolls"""
        return self.__rollFrequency

    @rollFrequency.setter
    def rollFrequency(self, value: str):
        self.__rollFrequency = value
        self._property_changed('rollFrequency')        

    @property
    def scalingMethod(self) -> str:
        """The method for scaling underliers, i.e fixedQuantity"""
        return self.__scalingMethod

    @scalingMethod.setter
    def scalingMethod(self, value: str):
        self.__scalingMethod = value
        self._property_changed('scalingMethod')        


class BaseIndexRefData(Base):
        
    """Base index reference data object."""
       
    def __init__(self, default: str = None, enum: Tuple[str, ...] = None):
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
       
    def __init__(self, default: str = None, enum: Tuple[str, ...] = None):
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
       
    def __init__(self, stats: PerformanceStats = None, id: str = None):
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
       
    def __init__(self, default: Union[Currency, str] = None, enum: Tuple[Union[Currency, str], ...] = None):
        super().__init__()
        self.__default = default if isinstance(default, Currency) else get_enum_value(Currency, default)
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
       
    def __init__(self, frequency: str, fixingTime: str = None, notional: float = None):
        super().__init__()
        self.__fixingTime = fixingTime
        self.__frequency = frequency
        self.__notional = notional

    @property
    def deltaType(self) -> str:
        """Details of how to compute delta"""
        return 'BlackScholes'        

    @property
    def fixingTime(self) -> str:
        """When the leg is hedged, i.e End of Day (EOD)."""
        return self.__fixingTime

    @fixingTime.setter
    def fixingTime(self, value: str):
        self.__fixingTime = value
        self._property_changed('fixingTime')        

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
       
    def __init__(self, enabled: bool, frequency: str, fixingTime: str, notionalPercentage: float):
        super().__init__()
        self.__enabled = enabled
        self.__fixingTime = fixingTime
        self.__frequency = frequency
        self.__notionalPercentage = notionalPercentage

    @property
    def enabled(self) -> bool:
        """Whether the leg is being hedged."""
        return self.__enabled

    @enabled.setter
    def enabled(self, value: bool):
        self.__enabled = value
        self._property_changed('enabled')        

    @property
    def fixingTime(self) -> str:
        """When the leg is hedged, i.e End of Day (EOD)."""
        return self.__fixingTime

    @fixingTime.setter
    def fixingTime(self, value: str):
        self.__fixingTime = value
        self._property_changed('fixingTime')        

    @property
    def frequency(self) -> str:
        """What frequency the leg is hedged."""
        return self.__frequency

    @frequency.setter
    def frequency(self, value: str):
        self.__frequency = value
        self._property_changed('frequency')        

    @property
    def notionalPercentage(self) -> float:
        """Percentage of notional to hedge."""
        return self.__notionalPercentage

    @notionalPercentage.setter
    def notionalPercentage(self, value: float):
        self.__notionalPercentage = value
        self._property_changed('notionalPercentage')        


class EnhancedBetaUnderlier(Base):
        
    """Underlying asset and corresponding nearby adder and valid months"""
       
    def __init__(self, assetId: str, monthAdd: float = None, validMonths: Tuple[str, ...] = None, isIncluded: bool = None, weightScale: float = None):
        super().__init__()
        self.__assetId = assetId
        self.__monthAdd = monthAdd
        self.__validMonths = validMonths
        self.__isIncluded = isIncluded
        self.__weightScale = weightScale

    @property
    def assetId(self) -> str:
        """Marquee unique asset identifier."""
        return self.__assetId

    @assetId.setter
    def assetId(self, value: str):
        self.__assetId = value
        self._property_changed('assetId')        

    @property
    def monthAdd(self) -> float:
        """Allows users to roll to a contract farther in the future by the number of months specified."""
        return self.__monthAdd

    @monthAdd.setter
    def monthAdd(self, value: float):
        self.__monthAdd = value
        self._property_changed('monthAdd')        

    @property
    def validMonths(self) -> Tuple[str, ...]:
        """Valid months to which you can roll contracts."""
        return self.__validMonths

    @validMonths.setter
    def validMonths(self, value: Tuple[str, ...]):
        self.__validMonths = value
        self._property_changed('validMonths')        

    @property
    def isIncluded(self) -> bool:
        """True if underlier is included in user's strategy."""
        return self.__isIncluded

    @isIncluded.setter
    def isIncluded(self, value: bool):
        self.__isIncluded = value
        self._property_changed('isIncluded')        

    @property
    def weightScale(self) -> float:
        """The percentage the underlier's weight is scaled."""
        return self.__weightScale

    @weightScale.setter
    def weightScale(self, value: float):
        self.__weightScale = value
        self._property_changed('weightScale')        


class EnhancedBetaUnderlierRefData(Base):
        
    """Enhanced Beta Underlier reference data object."""
       
    def __init__(self, assetId: str = None, validMonths: Tuple[str, ...] = None, current: bool = None):
        super().__init__()
        self.__assetId = assetId
        self.__validMonths = validMonths
        self.__current = current

    @property
    def assetId(self) -> str:
        """Marquee unique asset identifier."""
        return self.__assetId

    @assetId.setter
    def assetId(self, value: str):
        self.__assetId = value
        self._property_changed('assetId')        

    @property
    def validMonths(self) -> Tuple[str, ...]:
        """Valid months with contracts you can roll to"""
        return self.__validMonths

    @validMonths.setter
    def validMonths(self, value: Tuple[str, ...]):
        self.__validMonths = value
        self._property_changed('validMonths')        

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
       
    def __init__(self, primaryId: str = None, secondaryId: str = None, correlation: float = None):
        super().__init__()
        self.__primaryId = primaryId
        self.__secondaryId = secondaryId
        self.__correlation = correlation

    @property
    def primaryId(self) -> str:
        """Marquee unique identifier for the primary underlying asset in the correlation"""
        return self.__primaryId

    @primaryId.setter
    def primaryId(self, value: str):
        self.__primaryId = value
        self._property_changed('primaryId')        

    @property
    def secondaryId(self) -> str:
        """Marquee unique identifier for the secondary underlying asset in the correlation"""
        return self.__secondaryId

    @secondaryId.setter
    def secondaryId(self, value: str):
        self.__secondaryId = value
        self._property_changed('secondaryId')        

    @property
    def correlation(self) -> float:
        """Correlation between the primary and secondary underliers"""
        return self.__correlation

    @correlation.setter
    def correlation(self, value: float):
        self.__correlation = value
        self._property_changed('correlation')        


class EqOptionBacktest(Base):
        
    """Eq Option Backtest Instrument"""
       
    def __init__(self, expiration: str, optionType: str, optionStrikeType: str, strike: float, underlyingAssetId: str, notionalPercentage: float = None):
        super().__init__()
        self.__expiration = expiration
        self.__notionalPercentage = notionalPercentage
        self.__optionType = optionType
        self.__optionStrikeType = optionStrikeType
        self.__strike = strike
        self.__underlyingAssetId = underlyingAssetId

    @property
    def expiration(self) -> str:
        """Time until expiration."""
        return self.__expiration

    @expiration.setter
    def expiration(self, value: str):
        self.__expiration = value
        self._property_changed('expiration')        

    @property
    def notionalPercentage(self) -> float:
        """The notional percentage applied to the instrument"""
        return self.__notionalPercentage

    @notionalPercentage.setter
    def notionalPercentage(self, value: float):
        self.__notionalPercentage = value
        self._property_changed('notionalPercentage')        

    @property
    def optionType(self) -> str:
        """Type of option, i.e call."""
        return self.__optionType

    @optionType.setter
    def optionType(self, value: str):
        self.__optionType = value
        self._property_changed('optionType')        

    @property
    def optionStrikeType(self) -> str:
        """Type of option strike, i.e relative."""
        return self.__optionStrikeType

    @optionStrikeType.setter
    def optionStrikeType(self, value: str):
        self.__optionStrikeType = value
        self._property_changed('optionStrikeType')        

    @property
    def strike(self) -> float:
        """Strike percentage, either relative % or delta % depending on strike type."""
        return self.__strike

    @strike.setter
    def strike(self, value: float):
        self.__strike = value
        self._property_changed('strike')        

    @property
    def underlyingAssetId(self) -> str:
        """Marquee unique asset identifier."""
        return self.__underlyingAssetId

    @underlyingAssetId.setter
    def underlyingAssetId(self, value: str):
        self.__underlyingAssetId = value
        self._property_changed('underlyingAssetId')        


class ExpirationRefData(Base):
        
    """Expiration reference data object."""
       
    def __init__(self, default: str = None, enum: Tuple[str, ...] = None):
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
       
    def __init__(self, default: str = None, enum: Tuple[str, ...] = None):
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
       
    def __init__(self, default: str = None, enum: Tuple[str, ...] = None):
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
       
    def __init__(self, default: str = None, enum: Tuple[str, ...] = None):
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
       
    def __init__(self, default: float = None, min: float = None, max: float = None):
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
       
    def __init__(self, default: str = None, enum: Tuple[str, ...] = None):
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
       
    def __init__(self, default: str = None, enum: Tuple[str, ...] = None):
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
       
    def __init__(self, horizon: str = None, stats: PerformanceStats = None):
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
       
    def __init__(self, default: str = None, enum: Tuple[str, ...] = None):
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
       
    def __init__(self, default: float = None, min: float = None, max: float = None):
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
       
    def __init__(self, default: str = None, enum: Tuple[str, ...] = None):
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
       
    def __init__(self, default: str = None, enum: Tuple[str, ...] = None):
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
       
    def __init__(self, assetId: str = None, weight: float = None):
        super().__init__()
        self.__assetId = assetId
        self.__weight = weight

    @property
    def assetId(self) -> str:
        """Marquee unique asset identifier."""
        return self.__assetId

    @assetId.setter
    def assetId(self, value: str):
        self.__assetId = value
        self._property_changed('assetId')        

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
       
    def __init__(self, EMAalpha: float = None, lookBackPeriod: str = None, useLogReturn: bool = False):
        super().__init__()
        self.__EMAalpha = EMAalpha
        self.__lookBackPeriod = lookBackPeriod
        self.__useLogReturn = useLogReturn

    @property
    def name(self) -> str:
        """Name of the Modifier"""
        return 'Volatility Weighted'        

    @property
    def EMAalpha(self) -> float:
        """Alpha value for Exponentially Weighted Moving Average Volatility; set to 0 if standard volatility."""
        return self.__EMAalpha

    @EMAalpha.setter
    def EMAalpha(self, value: float):
        self.__EMAalpha = value
        self._property_changed('EMAalpha')        

    @property
    def lookBackPeriod(self) -> str:
        """Look back period to measure volatility for each underlier."""
        return self.__lookBackPeriod

    @lookBackPeriod.setter
    def lookBackPeriod(self, value: str):
        self.__lookBackPeriod = value
        self._property_changed('lookBackPeriod')        

    @property
    def useLogReturn(self) -> bool:
        """Whether to use Log Returns instead of Arithmetic Returns for volatility calculation."""
        return self.__useLogReturn

    @useLogReturn.setter
    def useLogReturn(self, value: bool):
        self.__useLogReturn = value
        self._property_changed('useLogReturn')        


class VolatilityWeightedWeightingModifierRefData(Base):
        
    """Volatility Weighted Weighting Modifier reference data object."""
       
    def __init__(self, EMAalpha: dict = None, lookBackPeriod: dict = None):
        super().__init__()
        self.__EMAalpha = EMAalpha
        self.__lookBackPeriod = lookBackPeriod

    @property
    def EMAalpha(self) -> dict:
        """Alpha value for Exponentially Weighted Moving Average Volatility reference data object."""
        return self.__EMAalpha

    @EMAalpha.setter
    def EMAalpha(self, value: dict):
        self.__EMAalpha = value
        self._property_changed('EMAalpha')        

    @property
    def lookBackPeriod(self) -> dict:
        """Lookback period to measure volatility for each underlier reference data object. """
        return self.__lookBackPeriod

    @lookBackPeriod.setter
    def lookBackPeriod(self, value: dict):
        self.__lookBackPeriod = value
        self._property_changed('lookBackPeriod')        


class BacktestResult(Base):
        
    """backtest result"""
       
    def __init__(self, backtestId: str = None, performance: Tuple[FieldValueMap, ...] = None, stats: PerformanceStats = None, performanceDecompositions: Tuple[BacktestPerformanceDecomposition, ...] = None, risks: Tuple[BacktestRisk, ...] = None, history: Tuple[PerformanceRange, ...] = None, underlierCorrelation: Tuple[EntityCorrelation, ...] = None, comparisons: Tuple[BacktestComparison, ...] = None, backtestVersion: float = None):
        super().__init__()
        self.__backtestId = backtestId
        self.__performance = performance
        self.__stats = stats
        self.__performanceDecompositions = performanceDecompositions
        self.__risks = risks
        self.__history = history
        self.__underlierCorrelation = underlierCorrelation
        self.__comparisons = comparisons
        self.__backtestVersion = backtestVersion

    @property
    def backtestId(self) -> str:
        """Marquee unique backtest identifier"""
        return self.__backtestId

    @backtestId.setter
    def backtestId(self, value: str):
        self.__backtestId = value
        self._property_changed('backtestId')        

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
    def performanceDecompositions(self) -> Tuple[BacktestPerformanceDecomposition, ...]:
        """Decompositions of the performance of the backtest"""
        return self.__performanceDecompositions

    @performanceDecompositions.setter
    def performanceDecompositions(self, value: Tuple[BacktestPerformanceDecomposition, ...]):
        self.__performanceDecompositions = value
        self._property_changed('performanceDecompositions')        

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
    def underlierCorrelation(self) -> Tuple[EntityCorrelation, ...]:
        """entity correlation"""
        return self.__underlierCorrelation

    @underlierCorrelation.setter
    def underlierCorrelation(self, value: Tuple[EntityCorrelation, ...]):
        self.__underlierCorrelation = value
        self._property_changed('underlierCorrelation')        

    @property
    def comparisons(self) -> Tuple[BacktestComparison, ...]:
        """Array of comparisons btw the backtest and comparison entity."""
        return self.__comparisons

    @comparisons.setter
    def comparisons(self, value: Tuple[BacktestComparison, ...]):
        self.__comparisons = value
        self._property_changed('comparisons')        

    @property
    def backtestVersion(self) -> float:
        """Backtest version number."""
        return self.__backtestVersion

    @backtestVersion.setter
    def backtestVersion(self, value: float):
        self.__backtestVersion = value
        self._property_changed('backtestVersion')        


class BacktestStrategyUnderlierHedge(Base):
        
    """Hedge information for the backtest underlier"""
       
    def __init__(self, riskDetails: DeltaHedgeParameters = None, quantityPercentage: float = None):
        super().__init__()
        self.__riskDetails = riskDetails
        self.__quantityPercentage = quantityPercentage

    @property
    def riskDetails(self) -> DeltaHedgeParameters:
        """details of the risk being hedged"""
        return self.__riskDetails

    @riskDetails.setter
    def riskDetails(self, value: DeltaHedgeParameters):
        self.__riskDetails = value
        self._property_changed('riskDetails')        

    @property
    def quantityPercentage(self) -> float:
        """Percentage of quantity to hedge"""
        return self.__quantityPercentage

    @quantityPercentage.setter
    def quantityPercentage(self, value: float):
        self.__quantityPercentage = value
        self._property_changed('quantityPercentage')        


class BasketBacktestParameters(Base):
        
    """Parameters of a Basket backtest."""
       
    def __init__(self, underliers: Tuple[Underlier, ...], rebalanceParameters: BacktestRebalanceParameters = None, weightingModifiers: Tuple[VolatilityWeightedWeightingModifier, ...] = None, weightingStrategy: str = None):
        super().__init__()
        self.__rebalanceParameters = rebalanceParameters
        self.__underliers = underliers
        self.__weightingModifiers = weightingModifiers
        self.__weightingStrategy = weightingStrategy

    @property
    def rebalanceParameters(self) -> BacktestRebalanceParameters:
        """Parameters relating to the backtest's rebalance"""
        return self.__rebalanceParameters

    @rebalanceParameters.setter
    def rebalanceParameters(self, value: BacktestRebalanceParameters):
        self.__rebalanceParameters = value
        self._property_changed('rebalanceParameters')        

    @property
    def underliers(self) -> Tuple[Underlier, ...]:
        """Underlying assets for the backtest"""
        return self.__underliers

    @underliers.setter
    def underliers(self, value: Tuple[Underlier, ...]):
        self.__underliers = value
        self._property_changed('underliers')        

    @property
    def weightingModifiers(self) -> Tuple[VolatilityWeightedWeightingModifier, ...]:
        """Weighting modifiers for the backtest."""
        return self.__weightingModifiers

    @weightingModifiers.setter
    def weightingModifiers(self, value: Tuple[VolatilityWeightedWeightingModifier, ...]):
        self.__weightingModifiers = value
        self._property_changed('weightingModifiers')        

    @property
    def weightingStrategy(self) -> str:
        """Strategy for determining the weight of the backtest underliers."""
        return self.__weightingStrategy

    @weightingStrategy.setter
    def weightingStrategy(self, value: str):
        self.__weightingStrategy = value
        self._property_changed('weightingStrategy')        


class BasketBacktestRefData(Base):
        
    """Basket backtest reference data"""
       
    def __init__(self, currency: CurrencyRefData = None, lookBackPeriod: LookBackPeriodRefData = None, weightingStrategy: dict = None, weightingModifiers: dict = None):
        super().__init__()
        self.__currency = currency
        self.__lookBackPeriod = lookBackPeriod
        self.__weightingStrategy = weightingStrategy
        self.__weightingModifiers = weightingModifiers

    @property
    def currency(self) -> CurrencyRefData:
        """Currency Reference Data"""
        return self.__currency

    @currency.setter
    def currency(self, value: CurrencyRefData):
        self.__currency = value
        self._property_changed('currency')        

    @property
    def lookBackPeriod(self) -> LookBackPeriodRefData:
        """Look back period reference data object."""
        return self.__lookBackPeriod

    @lookBackPeriod.setter
    def lookBackPeriod(self, value: LookBackPeriodRefData):
        self.__lookBackPeriod = value
        self._property_changed('lookBackPeriod')        

    @property
    def weightingStrategy(self) -> dict:
        """Weighting strategy reference data object."""
        return self.__weightingStrategy

    @weightingStrategy.setter
    def weightingStrategy(self, value: dict):
        self.__weightingStrategy = value
        self._property_changed('weightingStrategy')        

    @property
    def weightingModifiers(self) -> dict:
        """Weighting Modifiers reference data object."""
        return self.__weightingModifiers

    @weightingModifiers.setter
    def weightingModifiers(self, value: dict):
        self.__weightingModifiers = value
        self._property_changed('weightingModifiers')        


class DeltaHedgingRefData(Base):
        
    """Delta Hedging Reference Data"""
       
    def __init__(self, fixingTime: FixingTimeRefData = None, frequency: FrequencyRefData = None, notionalPercentage: NotionalPercentageRefData = None):
        super().__init__()
        self.__fixingTime = fixingTime
        self.__frequency = frequency
        self.__notionalPercentage = notionalPercentage

    @property
    def fixingTime(self) -> FixingTimeRefData:
        """Fixing Time reference data object."""
        return self.__fixingTime

    @fixingTime.setter
    def fixingTime(self, value: FixingTimeRefData):
        self.__fixingTime = value
        self._property_changed('fixingTime')        

    @property
    def frequency(self) -> FrequencyRefData:
        """Frequency reference data object."""
        return self.__frequency

    @frequency.setter
    def frequency(self, value: FrequencyRefData):
        self.__frequency = value
        self._property_changed('frequency')        

    @property
    def notionalPercentage(self) -> NotionalPercentageRefData:
        """Notional Percentage Reference Data"""
        return self.__notionalPercentage

    @notionalPercentage.setter
    def notionalPercentage(self, value: NotionalPercentageRefData):
        self.__notionalPercentage = value
        self._property_changed('notionalPercentage')        


class EnhancedBetaBacktestParameters(Base):
        
    """Parameters of an Enhanced Beta backtest."""
       
    def __init__(self, underliers: Tuple[EnhancedBetaUnderlier, ...], rollStart: float, rollEnd: float, baseIndex: str):
        super().__init__()
        self.__rollStart = rollStart
        self.__rollEnd = rollEnd
        self.__baseIndex = baseIndex
        self.__underliers = underliers

    @property
    def rollStart(self) -> float:
        """Business day on which to begin rolling."""
        return self.__rollStart

    @rollStart.setter
    def rollStart(self, value: float):
        self.__rollStart = value
        self._property_changed('rollStart')        

    @property
    def rollEnd(self) -> float:
        """Business day on which to finish rolling."""
        return self.__rollEnd

    @rollEnd.setter
    def rollEnd(self, value: float):
        self.__rollEnd = value
        self._property_changed('rollEnd')        

    @property
    def baseIndex(self) -> str:
        """Base index which strategy is attempting to beat."""
        return self.__baseIndex

    @baseIndex.setter
    def baseIndex(self, value: str):
        self.__baseIndex = value
        self._property_changed('baseIndex')        

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
       
    def __init__(self, lookBackPeriod: LookBackPeriodRefData = None, currency: CurrencyRefData = None, baseIndex: BaseIndexRefData = None, MASJ8W49Y02X9CGS: dict = None, MAAHST8JED9B607H: dict = None):
        super().__init__()
        self.__lookBackPeriod = lookBackPeriod
        self.__currency = currency
        self.__baseIndex = baseIndex
        self.__MASJ8W49Y02X9CGS = MASJ8W49Y02X9CGS
        self.__MAAHST8JED9B607H = MAAHST8JED9B607H

    @property
    def lookBackPeriod(self) -> LookBackPeriodRefData:
        """Look back period reference data object."""
        return self.__lookBackPeriod

    @lookBackPeriod.setter
    def lookBackPeriod(self, value: LookBackPeriodRefData):
        self.__lookBackPeriod = value
        self._property_changed('lookBackPeriod')        

    @property
    def currency(self) -> CurrencyRefData:
        """Currency Reference Data"""
        return self.__currency

    @currency.setter
    def currency(self, value: CurrencyRefData):
        self.__currency = value
        self._property_changed('currency')        

    @property
    def baseIndex(self) -> BaseIndexRefData:
        """Base index reference data object."""
        return self.__baseIndex

    @baseIndex.setter
    def baseIndex(self, value: BaseIndexRefData):
        self.__baseIndex = value
        self._property_changed('baseIndex')        

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
       
    def __init__(self, buySell: str, expiration: str, optionType: str, optionStrikeType: str, strike: float, underlyingAssetId: str, notionalPercentage: float = None, deltaHedging: DeltaHedgingParameters = None, tradeInTime: str = None):
        super().__init__()
        self.__buySell = buySell
        self.__expiration = expiration
        self.__optionType = optionType
        self.__optionStrikeType = optionStrikeType
        self.__notionalPercentage = notionalPercentage
        self.__strike = strike
        self.__underlyingAssetId = underlyingAssetId
        self.__deltaHedging = deltaHedging
        self.__tradeInTime = tradeInTime

    @property
    def buySell(self) -> str:
        """Option position, i.e buy"""
        return self.__buySell

    @buySell.setter
    def buySell(self, value: str):
        self.__buySell = value
        self._property_changed('buySell')        

    @property
    def expiration(self) -> str:
        """Time until expiration."""
        return self.__expiration

    @expiration.setter
    def expiration(self, value: str):
        self.__expiration = value
        self._property_changed('expiration')        

    @property
    def optionType(self) -> str:
        """Type of option, i.e call."""
        return self.__optionType

    @optionType.setter
    def optionType(self, value: str):
        self.__optionType = value
        self._property_changed('optionType')        

    @property
    def optionStrikeType(self) -> str:
        """Type of option strike, i.e relative."""
        return self.__optionStrikeType

    @optionStrikeType.setter
    def optionStrikeType(self, value: str):
        self.__optionStrikeType = value
        self._property_changed('optionStrikeType')        

    @property
    def notionalPercentage(self) -> float:
        """The percentage to increase/decrease your position on the leg."""
        return self.__notionalPercentage

    @notionalPercentage.setter
    def notionalPercentage(self, value: float):
        self.__notionalPercentage = value
        self._property_changed('notionalPercentage')        

    @property
    def strike(self) -> float:
        """Strike percentage, either relative % or delta % depending on strike type."""
        return self.__strike

    @strike.setter
    def strike(self, value: float):
        self.__strike = value
        self._property_changed('strike')        

    @property
    def underlyingAssetId(self) -> str:
        """Marquee unique asset identifier."""
        return self.__underlyingAssetId

    @underlyingAssetId.setter
    def underlyingAssetId(self, value: str):
        self.__underlyingAssetId = value
        self._property_changed('underlyingAssetId')        

    @property
    def deltaHedging(self) -> DeltaHedgingParameters:
        """Parameters for delta hedging an option."""
        return self.__deltaHedging

    @deltaHedging.setter
    def deltaHedging(self, value: DeltaHedgingParameters):
        self.__deltaHedging = value
        self._property_changed('deltaHedging')        

    @property
    def tradeInTime(self) -> str:
        """When from now to trade out the leg (must be less than expiration)."""
        return self.__tradeInTime

    @tradeInTime.setter
    def tradeInTime(self, value: str):
        self.__tradeInTime = value
        self._property_changed('tradeInTime')        


class UnderlyingAssetIdDataRefData(Base):
        
    """Underlying asset id data reference data object."""
       
    def __init__(self, assetId: str = None, fixingTime: FixingTimeRefData = None, frequency: FrequencyRefData = None):
        super().__init__()
        self.__assetId = assetId
        self.__fixingTime = fixingTime
        self.__frequency = frequency

    @property
    def assetId(self) -> str:
        """Marquee unique asset identifier."""
        return self.__assetId

    @assetId.setter
    def assetId(self, value: str):
        self.__assetId = value
        self._property_changed('assetId')        

    @property
    def fixingTime(self) -> FixingTimeRefData:
        """Fixing Time reference data object."""
        return self.__fixingTime

    @fixingTime.setter
    def fixingTime(self, value: FixingTimeRefData):
        self.__fixingTime = value
        self._property_changed('fixingTime')        

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
       
    def __init__(self, instrument: EqOptionBacktest, marketModel: str, name: str = None, hedge: BacktestStrategyUnderlierHedge = None):
        super().__init__()
        self.__instrument = instrument
        self.__marketModel = marketModel
        self.__name = name
        self.__hedge = hedge

    @property
    def instrument(self) -> EqOptionBacktest:
        """instrument that you are getting into"""
        return self.__instrument

    @instrument.setter
    def instrument(self, value: EqOptionBacktest):
        self.__instrument = value
        self._property_changed('instrument')        

    @property
    def marketModel(self) -> str:
        """Market model used for the underlier."""
        return self.__marketModel

    @marketModel.setter
    def marketModel(self, value: str):
        self.__marketModel = value
        self._property_changed('marketModel')        

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
       
    def __init__(self, default: str = None, enum: Tuple[str, ...] = None, data: Tuple[UnderlyingAssetIdDataRefData, ...] = None):
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
       
    def __init__(self, underliers: Tuple[OptionBacktestUnderlier, ...], tradeInMethod: str = None, scalingMethod: str = None):
        super().__init__()
        self.__underliers = underliers
        self.__tradeInMethod = tradeInMethod
        self.__scalingMethod = scalingMethod

    @property
    def underliers(self) -> Tuple[OptionBacktestUnderlier, ...]:
        """Underlying assets of the backtest"""
        return self.__underliers

    @underliers.setter
    def underliers(self, value: Tuple[OptionBacktestUnderlier, ...]):
        self.__underliers = value
        self._property_changed('underliers')        

    @property
    def tradeInMethod(self) -> str:
        """Method used to trade in legs before expiry."""
        return self.__tradeInMethod

    @tradeInMethod.setter
    def tradeInMethod(self, value: str):
        self.__tradeInMethod = value
        self._property_changed('tradeInMethod')        

    @property
    def scalingMethod(self) -> str:
        """The method for scaling legs, i.e percentage of NAV"""
        return self.__scalingMethod

    @scalingMethod.setter
    def scalingMethod(self, value: str):
        self.__scalingMethod = value
        self._property_changed('scalingMethod')        


class VolBacktestRefData(Base):
        
    """Volatility backtest reference data"""
       
    def __init__(self, buySell: BuySellRefData = None, currency: CurrencyRefData = None, deltaHedging: DeltaHedgingRefData = None, deltaStrike: StrikeRefData = None, notionalPercentage: NotionalPercentageRefData = None, expiration: ExpirationRefData = None, lookBackPeriod: LookBackPeriodRefData = None, optionType: OptionTypeRefData = None, optionStrikeType: OptionStrikeTypeRefData = None, relativeStrike: StrikeRefData = None, strike: StrikeRefData = None, scalingMethod: ScalingMethodRefData = None, underlyingAssetId: UnderlyingAssetIdRefData = None, tradeInMethod: TradeInMethodRefData = None, tradeInTime: TradeInTimeRefData = None):
        super().__init__()
        self.__buySell = buySell
        self.__currency = currency
        self.__deltaHedging = deltaHedging
        self.__deltaStrike = deltaStrike
        self.__notionalPercentage = notionalPercentage
        self.__expiration = expiration
        self.__lookBackPeriod = lookBackPeriod
        self.__optionType = optionType
        self.__optionStrikeType = optionStrikeType
        self.__relativeStrike = relativeStrike
        self.__strike = strike
        self.__scalingMethod = scalingMethod
        self.__underlyingAssetId = underlyingAssetId
        self.__tradeInMethod = tradeInMethod
        self.__tradeInTime = tradeInTime

    @property
    def buySell(self) -> BuySellRefData:
        """Buy Sell reference data object."""
        return self.__buySell

    @buySell.setter
    def buySell(self, value: BuySellRefData):
        self.__buySell = value
        self._property_changed('buySell')        

    @property
    def currency(self) -> CurrencyRefData:
        """Currency Reference Data"""
        return self.__currency

    @currency.setter
    def currency(self, value: CurrencyRefData):
        self.__currency = value
        self._property_changed('currency')        

    @property
    def deltaHedging(self) -> DeltaHedgingRefData:
        """Delta Hedging Reference Data"""
        return self.__deltaHedging

    @deltaHedging.setter
    def deltaHedging(self, value: DeltaHedgingRefData):
        self.__deltaHedging = value
        self._property_changed('deltaHedging')        

    @property
    def deltaStrike(self) -> StrikeRefData:
        """Strike reference data object."""
        return self.__deltaStrike

    @deltaStrike.setter
    def deltaStrike(self, value: StrikeRefData):
        self.__deltaStrike = value
        self._property_changed('deltaStrike')        

    @property
    def notionalPercentage(self) -> NotionalPercentageRefData:
        """Notional Percentage Reference Data"""
        return self.__notionalPercentage

    @notionalPercentage.setter
    def notionalPercentage(self, value: NotionalPercentageRefData):
        self.__notionalPercentage = value
        self._property_changed('notionalPercentage')        

    @property
    def expiration(self) -> ExpirationRefData:
        """Expiration reference data object."""
        return self.__expiration

    @expiration.setter
    def expiration(self, value: ExpirationRefData):
        self.__expiration = value
        self._property_changed('expiration')        

    @property
    def lookBackPeriod(self) -> LookBackPeriodRefData:
        """Look back period reference data object."""
        return self.__lookBackPeriod

    @lookBackPeriod.setter
    def lookBackPeriod(self, value: LookBackPeriodRefData):
        self.__lookBackPeriod = value
        self._property_changed('lookBackPeriod')        

    @property
    def optionType(self) -> OptionTypeRefData:
        """Option Type reference data object."""
        return self.__optionType

    @optionType.setter
    def optionType(self, value: OptionTypeRefData):
        self.__optionType = value
        self._property_changed('optionType')        

    @property
    def optionStrikeType(self) -> OptionStrikeTypeRefData:
        """Option strike type reference data object."""
        return self.__optionStrikeType

    @optionStrikeType.setter
    def optionStrikeType(self, value: OptionStrikeTypeRefData):
        self.__optionStrikeType = value
        self._property_changed('optionStrikeType')        

    @property
    def relativeStrike(self) -> StrikeRefData:
        """Strike reference data object."""
        return self.__relativeStrike

    @relativeStrike.setter
    def relativeStrike(self, value: StrikeRefData):
        self.__relativeStrike = value
        self._property_changed('relativeStrike')        

    @property
    def strike(self) -> StrikeRefData:
        """Strike reference data object."""
        return self.__strike

    @strike.setter
    def strike(self, value: StrikeRefData):
        self.__strike = value
        self._property_changed('strike')        

    @property
    def scalingMethod(self) -> ScalingMethodRefData:
        """Scaling Method Reference Data"""
        return self.__scalingMethod

    @scalingMethod.setter
    def scalingMethod(self, value: ScalingMethodRefData):
        self.__scalingMethod = value
        self._property_changed('scalingMethod')        

    @property
    def underlyingAssetId(self) -> UnderlyingAssetIdRefData:
        """Underlying asset id reference data object."""
        return self.__underlyingAssetId

    @underlyingAssetId.setter
    def underlyingAssetId(self, value: UnderlyingAssetIdRefData):
        self.__underlyingAssetId = value
        self._property_changed('underlyingAssetId')        

    @property
    def tradeInMethod(self) -> TradeInMethodRefData:
        """Trade In Method Reference Data"""
        return self.__tradeInMethod

    @tradeInMethod.setter
    def tradeInMethod(self, value: TradeInMethodRefData):
        self.__tradeInMethod = value
        self._property_changed('tradeInMethod')        

    @property
    def tradeInTime(self) -> TradeInTimeRefData:
        """Trade In Time Reference Data"""
        return self.__tradeInTime

    @tradeInTime.setter
    def tradeInTime(self, value: TradeInTimeRefData):
        self.__tradeInTime = value
        self._property_changed('tradeInTime')        


class VolatilityFlowBacktestParameters(Base):
        
    """Parameters of a Volatility Flow Backtest."""
       
    def __init__(self, tradingParameters: BacktestTradingParameters, indexInitialValue: float, underliers: Tuple[BacktestStrategyUnderlier, ...] = None):
        super().__init__()
        self.__indexInitialValue = indexInitialValue
        self.__underliers = underliers
        self.__tradingParameters = tradingParameters

    @property
    def indexInitialValue(self) -> float:
        """The initial index value of the strategy"""
        return self.__indexInitialValue

    @indexInitialValue.setter
    def indexInitialValue(self, value: float):
        self.__indexInitialValue = value
        self._property_changed('indexInitialValue')        

    @property
    def underliers(self) -> Tuple[BacktestStrategyUnderlier, ...]:
        """Underlying units of the backtest strategy"""
        return self.__underliers

    @underliers.setter
    def underliers(self, value: Tuple[BacktestStrategyUnderlier, ...]):
        self.__underliers = value
        self._property_changed('underliers')        

    @property
    def tradingParameters(self) -> BacktestTradingParameters:
        """details about how to transact in the instrument"""
        return self.__tradingParameters

    @tradingParameters.setter
    def tradingParameters(self, value: BacktestTradingParameters):
        self.__tradingParameters = value
        self._property_changed('tradingParameters')        


class Backtest(Base):
        
    """A backtest"""
       
    def __init__(self, name: str, type: str, assetClass: Union[AssetClass, str], costNetting: bool = False, createdById: str = None, createdTime: datetime.datetime = None, currency: Union[Currency, str] = None, entitlements: Entitlements = None, entitlementExclusions: EntitlementExclusions = None, id: str = None, lastUpdatedById: str = None, lastUpdatedTime: datetime.datetime = None, mqSymbol: str = None, ownerId: str = None, reportIds: Tuple[str, ...] = None, parameters: dict = None, startDate: datetime.date = None, endDate: datetime.date = None, version: float = None):
        super().__init__()
        self.__costNetting = costNetting
        self.__createdById = createdById
        self.__createdTime = createdTime
        self.__currency = currency if isinstance(currency, Currency) else get_enum_value(Currency, currency)
        self.__entitlements = entitlements
        self.__entitlementExclusions = entitlementExclusions
        self.__id = id
        self.__lastUpdatedById = lastUpdatedById
        self.__lastUpdatedTime = lastUpdatedTime
        self.__mqSymbol = mqSymbol
        self.__name = name
        self.__ownerId = ownerId
        self.__reportIds = reportIds
        self.__parameters = parameters
        self.__startDate = startDate
        self.__endDate = endDate
        self.__type = type
        self.__assetClass = assetClass if isinstance(assetClass, AssetClass) else get_enum_value(AssetClass, assetClass)
        self.__version = version

    @property
    def costNetting(self) -> bool:
        """Nets trading costs across the leaf nodes of the strategy."""
        return self.__costNetting

    @costNetting.setter
    def costNetting(self, value: bool):
        self.__costNetting = value
        self._property_changed('costNetting')        

    @property
    def createdById(self) -> str:
        """Unique identifier of user who created the object"""
        return self.__createdById

    @createdById.setter
    def createdById(self, value: str):
        self.__createdById = value
        self._property_changed('createdById')        

    @property
    def createdTime(self) -> datetime.datetime:
        """Time created. ISO 8601 formatted string"""
        return self.__createdTime

    @createdTime.setter
    def createdTime(self, value: datetime.datetime):
        self.__createdTime = value
        self._property_changed('createdTime')        

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
    def entitlementExclusions(self) -> EntitlementExclusions:
        """Defines the exclusion entitlements of a given resource"""
        return self.__entitlementExclusions

    @entitlementExclusions.setter
    def entitlementExclusions(self, value: EntitlementExclusions):
        self.__entitlementExclusions = value
        self._property_changed('entitlementExclusions')        

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value
        self._property_changed('id')        

    @property
    def lastUpdatedById(self) -> str:
        """Unique identifier of user who last updated the object"""
        return self.__lastUpdatedById

    @lastUpdatedById.setter
    def lastUpdatedById(self, value: str):
        self.__lastUpdatedById = value
        self._property_changed('lastUpdatedById')        

    @property
    def lastUpdatedTime(self) -> datetime.datetime:
        """Timestamp of when the object was last updated"""
        return self.__lastUpdatedTime

    @lastUpdatedTime.setter
    def lastUpdatedTime(self, value: datetime.datetime):
        self.__lastUpdatedTime = value
        self._property_changed('lastUpdatedTime')        

    @property
    def mqSymbol(self) -> str:
        """Marquee unique symbol identifier for the backtest."""
        return self.__mqSymbol

    @mqSymbol.setter
    def mqSymbol(self, value: str):
        self.__mqSymbol = value
        self._property_changed('mqSymbol')        

    @property
    def name(self) -> str:
        """Display name of the basket"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def ownerId(self) -> str:
        """Marquee unique identifier"""
        return self.__ownerId

    @ownerId.setter
    def ownerId(self, value: str):
        self.__ownerId = value
        self._property_changed('ownerId')        

    @property
    def reportIds(self) -> Tuple[str, ...]:
        """Array of report identifiers related to the object"""
        return self.__reportIds

    @reportIds.setter
    def reportIds(self, value: Tuple[str, ...]):
        self.__reportIds = value
        self._property_changed('reportIds')        

    @property
    def parameters(self) -> dict:
        return self.__parameters

    @parameters.setter
    def parameters(self, value: dict):
        self.__parameters = value
        self._property_changed('parameters')        

    @property
    def startDate(self) -> datetime.date:
        """Start date of backtest selected by user. If not selected, defaults to start of backtest timeseries."""
        return self.__startDate

    @startDate.setter
    def startDate(self, value: datetime.date):
        self.__startDate = value
        self._property_changed('startDate')        

    @property
    def endDate(self) -> datetime.date:
        """End date of backtest selected by user. If not selected, defaults to end of backtest timeseries."""
        return self.__endDate

    @endDate.setter
    def endDate(self, value: datetime.date):
        self.__endDate = value
        self._property_changed('endDate')        

    @property
    def type(self) -> str:
        """Type of Backtest."""
        return self.__type

    @type.setter
    def type(self, value: str):
        self.__type = value
        self._property_changed('type')        

    @property
    def assetClass(self) -> Union[AssetClass, str]:
        """Asset class of the backtest underliers."""
        return self.__assetClass

    @assetClass.setter
    def assetClass(self, value: Union[AssetClass, str]):
        self.__assetClass = value if isinstance(value, AssetClass) else get_enum_value(AssetClass, value)
        self._property_changed('assetClass')        

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
       
    def __init__(self, id: str = None, volatility: dict = None, enhanced_beta: EnhancedBetaRefData = None, basket: BasketBacktestRefData = None, ownerId: str = None, entitlements: Entitlements = None, entitlementExclusions: EntitlementExclusions = None, lastUpdatedById: str = None, lastUpdatedTime: datetime.datetime = None):
        super().__init__()
        self.__id = id
        self.__volatility = volatility
        self.__enhanced_beta = enhanced_beta
        self.__basket = basket
        self.__ownerId = ownerId
        self.__entitlements = entitlements
        self.__entitlementExclusions = entitlementExclusions
        self.__lastUpdatedById = lastUpdatedById
        self.__lastUpdatedTime = lastUpdatedTime

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
    def ownerId(self) -> str:
        """Marquee unique identifier for user who owns the object."""
        return self.__ownerId

    @ownerId.setter
    def ownerId(self, value: str):
        self.__ownerId = value
        self._property_changed('ownerId')        

    @property
    def entitlements(self) -> Entitlements:
        """Defines the entitlements of a given resource"""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self.__entitlements = value
        self._property_changed('entitlements')        

    @property
    def entitlementExclusions(self) -> EntitlementExclusions:
        """Defines the exclusion entitlements of a given resource"""
        return self.__entitlementExclusions

    @entitlementExclusions.setter
    def entitlementExclusions(self, value: EntitlementExclusions):
        self.__entitlementExclusions = value
        self._property_changed('entitlementExclusions')        

    @property
    def lastUpdatedById(self) -> str:
        """Unique identifier of user who last updated the object"""
        return self.__lastUpdatedById

    @lastUpdatedById.setter
    def lastUpdatedById(self, value: str):
        self.__lastUpdatedById = value
        self._property_changed('lastUpdatedById')        

    @property
    def lastUpdatedTime(self) -> datetime.datetime:
        """Timestamp of when the object was last updated"""
        return self.__lastUpdatedTime

    @lastUpdatedTime.setter
    def lastUpdatedTime(self, value: datetime.datetime):
        self.__lastUpdatedTime = value
        self._property_changed('lastUpdatedTime')        
