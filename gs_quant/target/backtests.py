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


class BacktestTradingParameters(Base):
        
    """Trading Information for the Backtesting Strategy"""
       
    def __init__(self, quantityType: str = None, quantityAmount: float = None, tradeInMethod: str = None):
        super().__init__()
        self.__quantityType = quantityType
        self.__quantityAmount = quantityAmount
        self.__tradeInMethod = tradeInMethod

    @property
    def quantityType(self) -> str:
        """The unit of the quantity of backtest strategy"""
        return self.__quantityType

    @quantityType.setter
    def quantityType(self, value: str):
        self.__quantityType = value
        self._property_changed('quantityType')        

    @property
    def quantityAmount(self) -> float:
        """The quantity of backtest strategy"""
        return self.__quantityAmount

    @quantityAmount.setter
    def quantityAmount(self, value: float):
        self.__quantityAmount = value
        self._property_changed('quantityAmount')        

    @property
    def tradeInMethod(self) -> str:
        """Roll method for the backtest strategy"""
        return self.__tradeInMethod

    @tradeInMethod.setter
    def tradeInMethod(self, value: str):
        self.__tradeInMethod = value
        self._property_changed('tradeInMethod')        


class DeltaHedgeParameters(Base):
        
    """Parameters for delta hedging a backtest strategy"""
       
    def __init__(self, frequency: str, fixingTime: str):
        super().__init__()
        self.__fixingTime = fixingTime
        self.__frequency = frequency

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


class EqOptionBacktest(Base):
        
    """Eq Option Backtest Instrument"""
       
    def __init__(self, expiration: str, optionType: str, optionStrikeType: str, strike: float, underlyingAssetId: str):
        super().__init__()
        self.__expiration = expiration
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


class BacktestHedgingParameters(Base):
        
    """Parameters for hedging a backtest strategy"""
       
    def __init__(self, riskDetails: DeltaHedgeParameters, quantityPercentage: float, legs: Tuple[str, ...] = None, name: str = None):
        super().__init__()
        self.__riskDetails = riskDetails
        self.__quantityPercentage = quantityPercentage
        self.__legs = legs
        self.__name = name

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

    @property
    def legs(self) -> Tuple[str, ...]:
        """name of the legs this hedge is relevant for"""
        return self.__legs

    @legs.setter
    def legs(self, value: Tuple[str, ...]):
        self.__legs = value
        self._property_changed('legs')        

    @property
    def name(self) -> str:
        """identifying name for the hedge leg"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        


class BacktestStrategyUnderlier(Base):
        
    """Backtest Strategy Undelier."""
       
    def __init__(self, buySell: str, instrument: EqOptionBacktest, legQuantity: float = None, name: str = None):
        super().__init__()
        self.__buySell = buySell
        self.__instrument = instrument
        self.__legQuantity = legQuantity
        self.__name = name

    @property
    def buySell(self) -> str:
        """transaction direction, i.e. buy or sell"""
        return self.__buySell

    @buySell.setter
    def buySell(self, value: str):
        self.__buySell = value
        self._property_changed('buySell')        

    @property
    def instrument(self) -> EqOptionBacktest:
        """instrument that you are getting into"""
        return self.__instrument

    @instrument.setter
    def instrument(self, value: EqOptionBacktest):
        self.__instrument = value
        self._property_changed('instrument')        

    @property
    def legQuantity(self) -> float:
        """quantity of this leg in a unit strategy. Base unit defined in trading Params"""
        return self.__legQuantity

    @legQuantity.setter
    def legQuantity(self, value: float):
        self.__legQuantity = value
        self._property_changed('legQuantity')        

    @property
    def name(self) -> str:
        """identifying name for the backtest leg"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        


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


class VolatilityBacktestParametersGeneric(Base):
        
    """Parameters of a Generic Volatility Backtest."""
       
    def __init__(self, strategyParameters: Tuple[BacktestStrategyUnderlier, ...], hedgingParameters: Tuple[BacktestHedgingParameters, ...] = None, tradingParameters: BacktestTradingParameters = None):
        super().__init__()
        self.__strategyParameters = strategyParameters
        self.__hedgingParameters = hedgingParameters
        self.__tradingParameters = tradingParameters

    @property
    def strategyParameters(self) -> Tuple[BacktestStrategyUnderlier, ...]:
        """Underlying units of the backtest strategy"""
        return self.__strategyParameters

    @strategyParameters.setter
    def strategyParameters(self, value: Tuple[BacktestStrategyUnderlier, ...]):
        self.__strategyParameters = value
        self._property_changed('strategyParameters')        

    @property
    def hedgingParameters(self) -> Tuple[BacktestHedgingParameters, ...]:
        """hedging instructions for the backtest strategy"""
        return self.__hedgingParameters

    @hedgingParameters.setter
    def hedgingParameters(self, value: Tuple[BacktestHedgingParameters, ...]):
        self.__hedgingParameters = value
        self._property_changed('hedgingParameters')        

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
       
    def __init__(self, name: str, type: str, assetClass: Union[AssetClass, str], costNetting: bool = False, createdById: str = None, createdTime: datetime.datetime = None, currency: Union[Currency, str] = None, entitlements: Entitlements = None, id: str = None, identifiers: Tuple[Identifier, ...] = None, lastUpdatedById: str = None, lastUpdatedTime: datetime.datetime = None, ownerId: str = None, reportIds: Tuple[str, ...] = None, parameters: dict = None, startDate: datetime.date = None, endDate: datetime.date = None, version: float = None):
        super().__init__()
        self.__costNetting = costNetting
        self.__createdById = createdById
        self.__createdTime = createdTime
        self.__currency = currency if isinstance(currency, Currency) else get_enum_value(Currency, currency)
        self.__entitlements = entitlements
        self.__id = id
        self.__identifiers = identifiers
        self.__lastUpdatedById = lastUpdatedById
        self.__lastUpdatedTime = lastUpdatedTime
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
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value
        self._property_changed('id')        

    @property
    def identifiers(self) -> Tuple[Identifier, ...]:
        """Array of identifier objects which can be used to locate this item in searches and other services"""
        return self.__identifiers

    @identifiers.setter
    def identifiers(self, value: Tuple[Identifier, ...]):
        self.__identifiers = value
        self._property_changed('identifiers')        

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
