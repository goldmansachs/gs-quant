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

from gs_quant.base import Instrument, get_enum_value
from gs_quant.target.common import *
from typing import Tuple, Union
import datetime


class CSLPython(Instrument):
        
    """Object representation of an arbitrary payoff defined in Python"""
       
    def __init__(self, className: str = None, denominated: Union[Currency, str] = None, doubleParams: Tuple[CSLDouble, ...] = None, dateParams: Tuple[CSLDate, ...] = None, stringParams: Tuple[CSLString, ...] = None, simpleScheduleParams: Tuple[CSLSimpleSchedule, ...] = None, scheduleParams: Tuple[CSLSchedule, ...] = None, currencyParams: Tuple[CSLCurrency, ...] = None, stockParams: Tuple[CSLStock, ...] = None, indexParams: Tuple[CSLIndex, ...] = None, fXCrossParams: Tuple[CSLFXCross, ...] = None, doubleArrayParams: Tuple[CSLDoubleArray, ...] = None, dateArrayParams: Tuple[CSLDateArray, ...] = None, stringArrayParams: Tuple[CSLStringArray, ...] = None, simpleScheduleArrayParams: Tuple[CSLSimpleScheduleArray, ...] = None, scheduleArrayParams: Tuple[CSLScheduleArray, ...] = None, currencyArrayParams: Tuple[CSLCurrencyArray, ...] = None, stockArrayParams: Tuple[CSLStockArray, ...] = None, indexArrayParams: Tuple[CSLIndexArray, ...] = None, fXCrossArrayParams: Tuple[CSLFXCrossArray, ...] = None):
        super().__init__()
        self.__className = className
        self.__denominated = denominated if isinstance(denominated, Currency) else get_enum_value(Currency, denominated)
        self.__doubleParams = doubleParams
        self.__dateParams = dateParams
        self.__stringParams = stringParams
        self.__simpleScheduleParams = simpleScheduleParams
        self.__scheduleParams = scheduleParams
        self.__currencyParams = currencyParams
        self.__stockParams = stockParams
        self.__indexParams = indexParams
        self.__fXCrossParams = fXCrossParams
        self.__doubleArrayParams = doubleArrayParams
        self.__dateArrayParams = dateArrayParams
        self.__stringArrayParams = stringArrayParams
        self.__simpleScheduleArrayParams = simpleScheduleArrayParams
        self.__scheduleArrayParams = scheduleArrayParams
        self.__currencyArrayParams = currencyArrayParams
        self.__stockArrayParams = stockArrayParams
        self.__indexArrayParams = indexArrayParams
        self.__fXCrossArrayParams = fXCrossArrayParams

    @property
    def assetClass(self) -> AssetClass:
        """Cross Asset"""
        return AssetClass.Cross_Asset        

    @property
    def type(self) -> AssetType:
        """CSL"""
        return AssetType.CSL        

    @property
    def className(self) -> str:
        """A reference to the Python script defining this payoff class"""
        return self.__className

    @className.setter
    def className(self, value: str):
        self.__className = value
        self._property_changed('className')        

    @property
    def denominated(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__denominated

    @denominated.setter
    def denominated(self, value: Union[Currency, str]):
        self.__denominated = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('denominated')        

    @property
    def doubleParams(self) -> Tuple[CSLDouble, ...]:
        """A double"""
        return self.__doubleParams

    @doubleParams.setter
    def doubleParams(self, value: Tuple[CSLDouble, ...]):
        self.__doubleParams = value
        self._property_changed('doubleParams')        

    @property
    def dateParams(self) -> Tuple[CSLDate, ...]:
        """A date"""
        return self.__dateParams

    @dateParams.setter
    def dateParams(self, value: Tuple[CSLDate, ...]):
        self.__dateParams = value
        self._property_changed('dateParams')        

    @property
    def stringParams(self) -> Tuple[CSLString, ...]:
        """A string"""
        return self.__stringParams

    @stringParams.setter
    def stringParams(self, value: Tuple[CSLString, ...]):
        self.__stringParams = value
        self._property_changed('stringParams')        

    @property
    def simpleScheduleParams(self) -> Tuple[CSLSimpleSchedule, ...]:
        """A fixing date, settlement date pair"""
        return self.__simpleScheduleParams

    @simpleScheduleParams.setter
    def simpleScheduleParams(self, value: Tuple[CSLSimpleSchedule, ...]):
        self.__simpleScheduleParams = value
        self._property_changed('simpleScheduleParams')        

    @property
    def scheduleParams(self) -> Tuple[CSLSchedule, ...]:
        """A schedule"""
        return self.__scheduleParams

    @scheduleParams.setter
    def scheduleParams(self, value: Tuple[CSLSchedule, ...]):
        self.__scheduleParams = value
        self._property_changed('scheduleParams')        

    @property
    def currencyParams(self) -> Tuple[CSLCurrency, ...]:
        """A currency"""
        return self.__currencyParams

    @currencyParams.setter
    def currencyParams(self, value: Tuple[CSLCurrency, ...]):
        self.__currencyParams = value
        self._property_changed('currencyParams')        

    @property
    def stockParams(self) -> Tuple[CSLStock, ...]:
        """A stock"""
        return self.__stockParams

    @stockParams.setter
    def stockParams(self, value: Tuple[CSLStock, ...]):
        self.__stockParams = value
        self._property_changed('stockParams')        

    @property
    def indexParams(self) -> Tuple[CSLIndex, ...]:
        """An index"""
        return self.__indexParams

    @indexParams.setter
    def indexParams(self, value: Tuple[CSLIndex, ...]):
        self.__indexParams = value
        self._property_changed('indexParams')        

    @property
    def fXCrossParams(self) -> Tuple[CSLFXCross, ...]:
        """An FX cross"""
        return self.__fXCrossParams

    @fXCrossParams.setter
    def fXCrossParams(self, value: Tuple[CSLFXCross, ...]):
        self.__fXCrossParams = value
        self._property_changed('fXCrossParams')        

    @property
    def doubleArrayParams(self) -> Tuple[CSLDoubleArray, ...]:
        """An array of doubles"""
        return self.__doubleArrayParams

    @doubleArrayParams.setter
    def doubleArrayParams(self, value: Tuple[CSLDoubleArray, ...]):
        self.__doubleArrayParams = value
        self._property_changed('doubleArrayParams')        

    @property
    def dateArrayParams(self) -> Tuple[CSLDateArray, ...]:
        """An array of dates"""
        return self.__dateArrayParams

    @dateArrayParams.setter
    def dateArrayParams(self, value: Tuple[CSLDateArray, ...]):
        self.__dateArrayParams = value
        self._property_changed('dateArrayParams')        

    @property
    def stringArrayParams(self) -> Tuple[CSLStringArray, ...]:
        """An array of strings"""
        return self.__stringArrayParams

    @stringArrayParams.setter
    def stringArrayParams(self, value: Tuple[CSLStringArray, ...]):
        self.__stringArrayParams = value
        self._property_changed('stringArrayParams')        

    @property
    def simpleScheduleArrayParams(self) -> Tuple[CSLSimpleScheduleArray, ...]:
        """An array of simple schedules"""
        return self.__simpleScheduleArrayParams

    @simpleScheduleArrayParams.setter
    def simpleScheduleArrayParams(self, value: Tuple[CSLSimpleScheduleArray, ...]):
        self.__simpleScheduleArrayParams = value
        self._property_changed('simpleScheduleArrayParams')        

    @property
    def scheduleArrayParams(self) -> Tuple[CSLScheduleArray, ...]:
        """An array of schedules"""
        return self.__scheduleArrayParams

    @scheduleArrayParams.setter
    def scheduleArrayParams(self, value: Tuple[CSLScheduleArray, ...]):
        self.__scheduleArrayParams = value
        self._property_changed('scheduleArrayParams')        

    @property
    def currencyArrayParams(self) -> Tuple[CSLCurrencyArray, ...]:
        """An array of currencies"""
        return self.__currencyArrayParams

    @currencyArrayParams.setter
    def currencyArrayParams(self, value: Tuple[CSLCurrencyArray, ...]):
        self.__currencyArrayParams = value
        self._property_changed('currencyArrayParams')        

    @property
    def stockArrayParams(self) -> Tuple[CSLStockArray, ...]:
        """An array of stocks"""
        return self.__stockArrayParams

    @stockArrayParams.setter
    def stockArrayParams(self, value: Tuple[CSLStockArray, ...]):
        self.__stockArrayParams = value
        self._property_changed('stockArrayParams')        

    @property
    def indexArrayParams(self) -> Tuple[CSLIndexArray, ...]:
        """An array of indices"""
        return self.__indexArrayParams

    @indexArrayParams.setter
    def indexArrayParams(self, value: Tuple[CSLIndexArray, ...]):
        self.__indexArrayParams = value
        self._property_changed('indexArrayParams')        

    @property
    def fXCrossArrayParams(self) -> Tuple[CSLFXCrossArray, ...]:
        """An array of FX crosses"""
        return self.__fXCrossArrayParams

    @fXCrossArrayParams.setter
    def fXCrossArrayParams(self, value: Tuple[CSLFXCrossArray, ...]):
        self.__fXCrossArrayParams = value
        self._property_changed('fXCrossArrayParams')        


class CommodSwap(Instrument):
        
    """Object representation of a commodities swap"""
       
    def __init__(self, commodity: Union[Commodities, str], start: Union[datetime.date, str], commodityReferencePrice: str = None, notionalAmount: float = 1000000.0, currency: Union[Currency, str] = None, calculationPeriods: int = None, calculationPeriodFrequency: Union[Frequency, str] = None):
        super().__init__()
        self.__commodity = commodity if isinstance(commodity, Commodities) else get_enum_value(Commodities, commodity)
        self.__commodityReferencePrice = commodityReferencePrice
        self.__start = start
        self.__notionalAmount = notionalAmount
        self.__currency = currency if isinstance(currency, Currency) else get_enum_value(Currency, currency)
        self.__calculationPeriods = calculationPeriods
        self.__calculationPeriodFrequency = calculationPeriodFrequency if isinstance(calculationPeriodFrequency, Frequency) else get_enum_value(Frequency, calculationPeriodFrequency)

    @property
    def assetClass(self) -> AssetClass:
        """Commod"""
        return AssetClass.Commod        

    @property
    def type(self) -> AssetType:
        """Swap"""
        return AssetType.Swap        

    @property
    def commodity(self) -> Union[Commodities, str]:
        """Commodity asset"""
        return self.__commodity

    @commodity.setter
    def commodity(self, value: Union[Commodities, str]):
        self.__commodity = value if isinstance(value, Commodities) else get_enum_value(Commodities, value)
        self._property_changed('commodity')        

    @property
    def commodityReferencePrice(self) -> str:
        return self.__commodityReferencePrice

    @commodityReferencePrice.setter
    def commodityReferencePrice(self, value: str):
        self.__commodityReferencePrice = value
        self._property_changed('commodityReferencePrice')        

    @property
    def start(self) -> Union[datetime.date, str]:
        return self.__start

    @start.setter
    def start(self, value: Union[datetime.date, str]):
        self.__start = value
        self._property_changed('start')        

    @property
    def notionalAmount(self) -> float:
        """Notional amount"""
        return self.__notionalAmount

    @notionalAmount.setter
    def notionalAmount(self, value: float):
        self.__notionalAmount = value
        self._property_changed('notionalAmount')        

    @property
    def currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self.__currency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('currency')        

    @property
    def calculationPeriods(self) -> int:
        """The number of calculation periods"""
        return self.__calculationPeriods

    @calculationPeriods.setter
    def calculationPeriods(self, value: int):
        self.__calculationPeriods = value
        self._property_changed('calculationPeriods')        

    @property
    def calculationPeriodFrequency(self) -> Union[Frequency, str]:
        """The frequency of the calculation periods"""
        return self.__calculationPeriodFrequency

    @calculationPeriodFrequency.setter
    def calculationPeriodFrequency(self, value: Union[Frequency, str]):
        self.__calculationPeriodFrequency = value if isinstance(value, Frequency) else get_enum_value(Frequency, value)
        self._property_changed('calculationPeriodFrequency')        


class EqCliquet(Instrument):
        
    """Object representation of an Equity Cliquet"""
       
    def __init__(self, asset: str, expirationDate: Union[datetime.date, str], strikePrice: float, currency: Union[Currency, str] = None, firstValuationDate: datetime.date = None, globalFloor: float = -1000000, globalCap: float = 1000000, lastValuationDate: datetime.date = None, notionalAmount: float = 1000000, paymentFrequency: str = 'Maturity', returnStyle: str = 'Rate of Return', returnType: str = 'Sum', valuationPeriod: str = None):
        super().__init__()
        self.__asset = asset
        self.__currency = currency if isinstance(currency, Currency) else get_enum_value(Currency, currency)
        self.__expirationDate = expirationDate
        self.__firstValuationDate = firstValuationDate
        self.__globalFloor = globalFloor
        self.__globalCap = globalCap
        self.__lastValuationDate = lastValuationDate
        self.__notionalAmount = notionalAmount
        self.__paymentFrequency = paymentFrequency
        self.__returnStyle = returnStyle
        self.__returnType = returnType
        self.__strikePrice = strikePrice
        self.__valuationPeriod = valuationPeriod

    @property
    def assetClass(self) -> AssetClass:
        """Equity"""
        return AssetClass.Equity        

    @property
    def type(self) -> AssetType:
        """Cliquet"""
        return AssetType.Cliquet        

    @property
    def asset(self) -> str:
        """Ticker of the underlying stock or index"""
        return self.__asset

    @asset.setter
    def asset(self, value: str):
        self.__asset = value
        self._property_changed('asset')        

    @property
    def currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self.__currency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('currency')        

    @property
    def expirationDate(self) -> Union[datetime.date, str]:
        """Date or tenor, e.g. 2018-09-03, 3m"""
        return self.__expirationDate

    @expirationDate.setter
    def expirationDate(self, value: Union[datetime.date, str]):
        self.__expirationDate = value
        self._property_changed('expirationDate')        

    @property
    def firstValuationDate(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__firstValuationDate

    @firstValuationDate.setter
    def firstValuationDate(self, value: datetime.date):
        self.__firstValuationDate = value
        self._property_changed('firstValuationDate')        

    @property
    def globalFloor(self) -> float:
        """Global Floor of return, relevant only if paying at maturity"""
        return self.__globalFloor

    @globalFloor.setter
    def globalFloor(self, value: float):
        self.__globalFloor = value
        self._property_changed('globalFloor')        

    @property
    def globalCap(self) -> float:
        """Global Cap of return, relevant only if paying at maturity"""
        return self.__globalCap

    @globalCap.setter
    def globalCap(self, value: float):
        self.__globalCap = value
        self._property_changed('globalCap')        

    @property
    def lastValuationDate(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__lastValuationDate

    @lastValuationDate.setter
    def lastValuationDate(self, value: datetime.date):
        self.__lastValuationDate = value
        self._property_changed('lastValuationDate')        

    @property
    def notionalAmount(self) -> float:
        """Notional of this position"""
        return self.__notionalAmount

    @notionalAmount.setter
    def notionalAmount(self, value: float):
        self.__notionalAmount = value
        self._property_changed('notionalAmount')        

    @property
    def paymentFrequency(self) -> str:
        return self.__paymentFrequency

    @paymentFrequency.setter
    def paymentFrequency(self, value: str):
        self.__paymentFrequency = value
        self._property_changed('paymentFrequency')        

    @property
    def returnStyle(self) -> str:
        """Return calculation style"""
        return self.__returnStyle

    @returnStyle.setter
    def returnStyle(self, value: str):
        self.__returnStyle = value
        self._property_changed('returnStyle')        

    @property
    def returnType(self) -> str:
        """Sum or Product of periodic return, relevant only if paying at maturity"""
        return self.__returnType

    @returnType.setter
    def returnType(self, value: str):
        self.__returnType = value
        self._property_changed('returnType')        

    @property
    def strikePrice(self) -> float:
        """Strike price as value"""
        return self.__strikePrice

    @strikePrice.setter
    def strikePrice(self, value: float):
        self.__strikePrice = value
        self._property_changed('strikePrice')        

    @property
    def valuationPeriod(self) -> str:
        """Tenor"""
        return self.__valuationPeriod

    @valuationPeriod.setter
    def valuationPeriod(self, value: str):
        self.__valuationPeriod = value
        self._property_changed('valuationPeriod')        


class EqForward(Instrument):
        
    """Object representation of an equity forward"""
       
    def __init__(self, asset: str, expirationDate: Union[datetime.date, str], forwardPrice: float, numberOfShares: int = 1):
        super().__init__()
        self.__asset = asset
        self.__numberOfShares = numberOfShares
        self.__expirationDate = expirationDate
        self.__forwardPrice = forwardPrice

    @property
    def assetClass(self) -> AssetClass:
        """Equity"""
        return AssetClass.Equity        

    @property
    def type(self) -> AssetType:
        """Forward"""
        return AssetType.Forward        

    @property
    def asset(self) -> str:
        """Ticker of the underlying stock or index"""
        return self.__asset

    @asset.setter
    def asset(self, value: str):
        self.__asset = value
        self._property_changed('asset')        

    @property
    def numberOfShares(self) -> int:
        """Number of shares"""
        return self.__numberOfShares

    @numberOfShares.setter
    def numberOfShares(self, value: int):
        self.__numberOfShares = value
        self._property_changed('numberOfShares')        

    @property
    def expirationDate(self) -> Union[datetime.date, str]:
        """Date or tenor, e.g. 2018-09-03, 3m"""
        return self.__expirationDate

    @expirationDate.setter
    def expirationDate(self, value: Union[datetime.date, str]):
        self.__expirationDate = value
        self._property_changed('expirationDate')        

    @property
    def forwardPrice(self) -> float:
        """Forward price"""
        return self.__forwardPrice

    @forwardPrice.setter
    def forwardPrice(self, value: float):
        self.__forwardPrice = value
        self._property_changed('forwardPrice')        


class EqOption(Instrument):
        
    """Object representation of an equity option"""
       
    def __init__(self, asset: str, expirationDate: Union[datetime.date, str], strikePrice: Union[float, str], optionType: Union[OptionType, str], optionStyle: Union[OptionStyle, str], numberOfOptions: float = 1, exchange: str = None, multiplier: float = None, settlementDate: Union[datetime.date, str] = None, currency: Union[Currency, str] = None, premium: float = 0):
        super().__init__()
        self.__numberOfOptions = numberOfOptions
        self.__asset = asset
        self.__exchange = exchange
        self.__expirationDate = expirationDate
        self.__strikePrice = strikePrice
        self.__optionType = optionType if isinstance(optionType, OptionType) else get_enum_value(OptionType, optionType)
        self.__optionStyle = optionStyle if isinstance(optionStyle, OptionStyle) else get_enum_value(OptionStyle, optionStyle)
        self.__multiplier = multiplier
        self.__settlementDate = settlementDate
        self.__currency = currency if isinstance(currency, Currency) else get_enum_value(Currency, currency)
        self.__premium = premium

    @property
    def assetClass(self) -> AssetClass:
        """Equity"""
        return AssetClass.Equity        

    @property
    def type(self) -> AssetType:
        """Option"""
        return AssetType.Option        

    @property
    def numberOfOptions(self) -> float:
        """Number of options"""
        return self.__numberOfOptions

    @numberOfOptions.setter
    def numberOfOptions(self, value: float):
        self.__numberOfOptions = value
        self._property_changed('numberOfOptions')        

    @property
    def asset(self) -> str:
        """Ticker of the underlying stock or index"""
        return self.__asset

    @asset.setter
    def asset(self, value: str):
        self.__asset = value
        self._property_changed('asset')        

    @property
    def exchange(self) -> str:
        """Name of marketplace where security, derivative or other instrument is traded"""
        return self.__exchange

    @exchange.setter
    def exchange(self, value: str):
        self.__exchange = value
        self._property_changed('exchange')        

    @property
    def expirationDate(self) -> Union[datetime.date, str]:
        """Date or tenor, e.g. 2018-09-03, 3m"""
        return self.__expirationDate

    @expirationDate.setter
    def expirationDate(self, value: Union[datetime.date, str]):
        self.__expirationDate = value
        self._property_changed('expirationDate')        

    @property
    def strikePrice(self) -> Union[float, str]:
        """Strike as value, percent or at-the-money e.g. 62.5, 95%, ATM-25, ATMF"""
        return self.__strikePrice

    @strikePrice.setter
    def strikePrice(self, value: Union[float, str]):
        self.__strikePrice = value
        self._property_changed('strikePrice')        

    @property
    def optionType(self) -> Union[OptionType, str]:
        return self.__optionType

    @optionType.setter
    def optionType(self, value: Union[OptionType, str]):
        self.__optionType = value if isinstance(value, OptionType) else get_enum_value(OptionType, value)
        self._property_changed('optionType')        

    @property
    def optionStyle(self) -> Union[OptionStyle, str]:
        """Option Style"""
        return self.__optionStyle

    @optionStyle.setter
    def optionStyle(self, value: Union[OptionStyle, str]):
        self.__optionStyle = value if isinstance(value, OptionStyle) else get_enum_value(OptionStyle, value)
        self._property_changed('optionStyle')        

    @property
    def multiplier(self) -> float:
        """Number of stock units per option contract"""
        return self.__multiplier

    @multiplier.setter
    def multiplier(self, value: float):
        self.__multiplier = value
        self._property_changed('multiplier')        

    @property
    def settlementDate(self) -> Union[datetime.date, str]:
        """Date or tenor, e.g. 2018-09-03, 3m"""
        return self.__settlementDate

    @settlementDate.setter
    def settlementDate(self, value: Union[datetime.date, str]):
        self.__settlementDate = value
        self._property_changed('settlementDate')        

    @property
    def currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self.__currency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('currency')        

    @property
    def premium(self) -> float:
        """Option premium"""
        return self.__premium

    @premium.setter
    def premium(self, value: float):
        self.__premium = value
        self._property_changed('premium')        


class FXForward(Instrument):
        
    """Object representation of an FX forward"""
       
    def __init__(self, pair: str = None, settlementDate: Union[datetime.date, str] = None, forwardRate: float = None, notionalAmount: float = None):
        super().__init__()
        self.__pair = pair
        self.__settlementDate = settlementDate
        self.__forwardRate = forwardRate
        self.__notionalAmount = notionalAmount

    @property
    def assetClass(self) -> AssetClass:
        """FX"""
        return AssetClass.FX        

    @property
    def type(self) -> AssetType:
        """Forward"""
        return AssetType.Forward        

    @property
    def pair(self) -> str:
        """Currency pair"""
        return self.__pair

    @pair.setter
    def pair(self, value: str):
        self.__pair = value
        self._property_changed('pair')        

    @property
    def settlementDate(self) -> Union[datetime.date, str]:
        """Date or tenor, e.g. 2018-09-03, 3m"""
        return self.__settlementDate

    @settlementDate.setter
    def settlementDate(self, value: Union[datetime.date, str]):
        self.__settlementDate = value
        self._property_changed('settlementDate')        

    @property
    def forwardRate(self) -> float:
        """Forward FX rate"""
        return self.__forwardRate

    @forwardRate.setter
    def forwardRate(self, value: float):
        self.__forwardRate = value
        self._property_changed('forwardRate')        

    @property
    def notionalAmount(self) -> float:
        """Notional amount"""
        return self.__notionalAmount

    @notionalAmount.setter
    def notionalAmount(self, value: float):
        self.__notionalAmount = value
        self._property_changed('notionalAmount')        


class FXOption(Instrument):
        
    """Object representation of a FX option"""
       
    def __init__(self, callCurrency: Union[Currency, str], putCurrency: Union[Currency, str], expirationDate: Union[datetime.date, str], optionType: Union[OptionType, str], callAmount: float = 1000000.0, putAmount: float = 1000000.0, strike: Union[float, str] = None, premium: float = 0, pair: str = None):
        super().__init__()
        self.__callCurrency = callCurrency if isinstance(callCurrency, Currency) else get_enum_value(Currency, callCurrency)
        self.__putCurrency = putCurrency if isinstance(putCurrency, Currency) else get_enum_value(Currency, putCurrency)
        self.__callAmount = callAmount
        self.__putAmount = putAmount
        self.__strike = strike
        self.__expirationDate = expirationDate
        self.__optionType = optionType if isinstance(optionType, OptionType) else get_enum_value(OptionType, optionType)
        self.__premium = premium
        self.__pair = pair

    @property
    def assetClass(self) -> AssetClass:
        """FX"""
        return AssetClass.FX        

    @property
    def type(self) -> AssetType:
        """Option"""
        return AssetType.Option        

    @property
    def callCurrency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__callCurrency

    @callCurrency.setter
    def callCurrency(self, value: Union[Currency, str]):
        self.__callCurrency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('callCurrency')        

    @property
    def putCurrency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__putCurrency

    @putCurrency.setter
    def putCurrency(self, value: Union[Currency, str]):
        self.__putCurrency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('putCurrency')        

    @property
    def callAmount(self) -> float:
        """Amount of the call currency"""
        return self.__callAmount

    @callAmount.setter
    def callAmount(self, value: float):
        self.__callAmount = value
        self._property_changed('callAmount')        

    @property
    def putAmount(self) -> float:
        """Amount of the put currency"""
        return self.__putAmount

    @putAmount.setter
    def putAmount(self, value: float):
        self.__putAmount = value
        self._property_changed('putAmount')        

    @property
    def strike(self) -> Union[float, str]:
        """Strike as value, percent or at-the-money e.g. 62.5, 95%, ATM-25, ATMF"""
        return self.__strike

    @strike.setter
    def strike(self, value: Union[float, str]):
        self.__strike = value
        self._property_changed('strike')        

    @property
    def expirationDate(self) -> Union[datetime.date, str]:
        """Date or tenor, e.g. 2018-09-03, 3m"""
        return self.__expirationDate

    @expirationDate.setter
    def expirationDate(self, value: Union[datetime.date, str]):
        self.__expirationDate = value
        self._property_changed('expirationDate')        

    @property
    def optionType(self) -> Union[OptionType, str]:
        return self.__optionType

    @optionType.setter
    def optionType(self, value: Union[OptionType, str]):
        self.__optionType = value if isinstance(value, OptionType) else get_enum_value(OptionType, value)
        self._property_changed('optionType')        

    @property
    def premium(self) -> float:
        """Option premium"""
        return self.__premium

    @premium.setter
    def premium(self, value: float):
        self.__premium = value
        self._property_changed('premium')        

    @property
    def pair(self) -> str:
        """Currency pair"""
        return self.__pair

    @pair.setter
    def pair(self, value: str):
        self.__pair = value
        self._property_changed('pair')        


class Forward(Instrument):
        
    """Object representation of a forward"""
       
    def __init__(self, currency: Union[Currency, str], expirationDate: Union[datetime.date, str], notionalAmount: float = None):
        super().__init__()
        self.__currency = currency if isinstance(currency, Currency) else get_enum_value(Currency, currency)
        self.__expirationDate = expirationDate
        self.__notionalAmount = notionalAmount

    @property
    def assetClass(self) -> AssetClass:
        """Cash"""
        return AssetClass.Cash        

    @property
    def type(self) -> AssetType:
        """Forward"""
        return AssetType.Forward        

    @property
    def currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self.__currency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('currency')        

    @property
    def expirationDate(self) -> Union[datetime.date, str]:
        """Date or tenor, e.g. 2018-09-03, 3m"""
        return self.__expirationDate

    @expirationDate.setter
    def expirationDate(self, value: Union[datetime.date, str]):
        self.__expirationDate = value
        self._property_changed('expirationDate')        

    @property
    def notionalAmount(self) -> float:
        """Notional amount"""
        return self.__notionalAmount

    @notionalAmount.setter
    def notionalAmount(self, value: float):
        self.__notionalAmount = value
        self._property_changed('notionalAmount')        


class IRBasisSwap(Instrument):
        
    """An exchange of cashflows from different interest rate indices"""
       
    def __init__(self, terminationDate: Union[datetime.date, str], payerCurrency: Union[Currency, str], receiverCurrency: Union[Currency, str], notionalAmount: float = 1000000.0, effectiveDate: Union[datetime.date, str] = None, payerSpread: float = None, payerRateOption: str = None, payerDesignatedMaturity: str = None, payerFrequency: str = None, payerDayCountFraction: Union[DayCountFraction, str] = None, payerBusinessDayConvention: Union[BusinessDayConvention, str] = None, receiverSpread: float = None, receiverRateOption: str = None, receiverDesignatedMaturity: str = None, receiverFrequency: str = None, receiverDayCountFraction: Union[DayCountFraction, str] = None, receiverBusinessDayConvention: Union[BusinessDayConvention, str] = None, fee: float = 0, clearingHouse: Union[SwapClearingHouse, str] = None):
        super().__init__()
        self.__notionalAmount = notionalAmount
        self.__effectiveDate = effectiveDate
        self.__terminationDate = terminationDate
        self.__payerSpread = payerSpread
        self.__payerCurrency = payerCurrency if isinstance(payerCurrency, Currency) else get_enum_value(Currency, payerCurrency)
        self.__payerRateOption = payerRateOption
        self.__payerDesignatedMaturity = payerDesignatedMaturity
        self.__payerFrequency = payerFrequency
        self.__payerDayCountFraction = payerDayCountFraction if isinstance(payerDayCountFraction, DayCountFraction) else get_enum_value(DayCountFraction, payerDayCountFraction)
        self.__payerBusinessDayConvention = payerBusinessDayConvention if isinstance(payerBusinessDayConvention, BusinessDayConvention) else get_enum_value(BusinessDayConvention, payerBusinessDayConvention)
        self.__receiverSpread = receiverSpread
        self.__receiverCurrency = receiverCurrency if isinstance(receiverCurrency, Currency) else get_enum_value(Currency, receiverCurrency)
        self.__receiverRateOption = receiverRateOption
        self.__receiverDesignatedMaturity = receiverDesignatedMaturity
        self.__receiverFrequency = receiverFrequency
        self.__receiverDayCountFraction = receiverDayCountFraction if isinstance(receiverDayCountFraction, DayCountFraction) else get_enum_value(DayCountFraction, receiverDayCountFraction)
        self.__receiverBusinessDayConvention = receiverBusinessDayConvention if isinstance(receiverBusinessDayConvention, BusinessDayConvention) else get_enum_value(BusinessDayConvention, receiverBusinessDayConvention)
        self.__fee = fee
        self.__clearingHouse = clearingHouse if isinstance(clearingHouse, SwapClearingHouse) else get_enum_value(SwapClearingHouse, clearingHouse)

    @property
    def assetClass(self) -> AssetClass:
        """Rates"""
        return AssetClass.Rates        

    @property
    def type(self) -> AssetType:
        """BasisSwap"""
        return AssetType.BasisSwap        

    @property
    def notionalAmount(self) -> float:
        """Notional amount"""
        return self.__notionalAmount

    @notionalAmount.setter
    def notionalAmount(self, value: float):
        self.__notionalAmount = value
        self._property_changed('notionalAmount')        

    @property
    def effectiveDate(self) -> Union[datetime.date, str]:
        """The date on which the swap becomes effective"""
        return self.__effectiveDate

    @effectiveDate.setter
    def effectiveDate(self, value: Union[datetime.date, str]):
        self.__effectiveDate = value
        self._property_changed('effectiveDate')        

    @property
    def terminationDate(self) -> Union[datetime.date, str]:
        """The termination of the swap, e.g. 2050-04-01, 10y"""
        return self.__terminationDate

    @terminationDate.setter
    def terminationDate(self, value: Union[datetime.date, str]):
        self.__terminationDate = value
        self._property_changed('terminationDate')        

    @property
    def payerSpread(self) -> float:
        """Spread over the payer rate"""
        return self.__payerSpread

    @payerSpread.setter
    def payerSpread(self, value: float):
        self.__payerSpread = value
        self._property_changed('payerSpread')        

    @property
    def payerCurrency(self) -> Union[Currency, str]:
        """The currency of the payer payments"""
        return self.__payerCurrency

    @payerCurrency.setter
    def payerCurrency(self, value: Union[Currency, str]):
        self.__payerCurrency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('payerCurrency')        

    @property
    def payerRateOption(self) -> str:
        """The underlying benchmark for the payer, e.g. USD-LIBOR-BBA, EUR-EURIBOR-TELERATE"""
        return self.__payerRateOption

    @payerRateOption.setter
    def payerRateOption(self, value: str):
        self.__payerRateOption = value
        self._property_changed('payerRateOption')        

    @property
    def payerDesignatedMaturity(self) -> str:
        """Tenor of the payerRateOption, e.g. 3m, 6m"""
        return self.__payerDesignatedMaturity

    @payerDesignatedMaturity.setter
    def payerDesignatedMaturity(self, value: str):
        self.__payerDesignatedMaturity = value
        self._property_changed('payerDesignatedMaturity')        

    @property
    def payerFrequency(self) -> str:
        """The frequency of payer payments, e.g. 6m"""
        return self.__payerFrequency

    @payerFrequency.setter
    def payerFrequency(self, value: str):
        self.__payerFrequency = value
        self._property_changed('payerFrequency')        

    @property
    def payerDayCountFraction(self) -> Union[DayCountFraction, str]:
        """The day count fraction for the payer"""
        return self.__payerDayCountFraction

    @payerDayCountFraction.setter
    def payerDayCountFraction(self, value: Union[DayCountFraction, str]):
        self.__payerDayCountFraction = value if isinstance(value, DayCountFraction) else get_enum_value(DayCountFraction, value)
        self._property_changed('payerDayCountFraction')        

    @property
    def payerBusinessDayConvention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention for the payer"""
        return self.__payerBusinessDayConvention

    @payerBusinessDayConvention.setter
    def payerBusinessDayConvention(self, value: Union[BusinessDayConvention, str]):
        self.__payerBusinessDayConvention = value if isinstance(value, BusinessDayConvention) else get_enum_value(BusinessDayConvention, value)
        self._property_changed('payerBusinessDayConvention')        

    @property
    def receiverSpread(self) -> float:
        """Spread over the receiver rate"""
        return self.__receiverSpread

    @receiverSpread.setter
    def receiverSpread(self, value: float):
        self.__receiverSpread = value
        self._property_changed('receiverSpread')        

    @property
    def receiverCurrency(self) -> Union[Currency, str]:
        """The currency of the receiver payments"""
        return self.__receiverCurrency

    @receiverCurrency.setter
    def receiverCurrency(self, value: Union[Currency, str]):
        self.__receiverCurrency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('receiverCurrency')        

    @property
    def receiverRateOption(self) -> str:
        """The underlying benchmark for the receiver, e.g. USD-LIBOR-BBA, EUR-EURIBOR-TELERATE"""
        return self.__receiverRateOption

    @receiverRateOption.setter
    def receiverRateOption(self, value: str):
        self.__receiverRateOption = value
        self._property_changed('receiverRateOption')        

    @property
    def receiverDesignatedMaturity(self) -> str:
        """Tenor of the receiverRateOption, e.g. 3m, 6m"""
        return self.__receiverDesignatedMaturity

    @receiverDesignatedMaturity.setter
    def receiverDesignatedMaturity(self, value: str):
        self.__receiverDesignatedMaturity = value
        self._property_changed('receiverDesignatedMaturity')        

    @property
    def receiverFrequency(self) -> str:
        """The frequency of receiver payments, e.g. 6m"""
        return self.__receiverFrequency

    @receiverFrequency.setter
    def receiverFrequency(self, value: str):
        self.__receiverFrequency = value
        self._property_changed('receiverFrequency')        

    @property
    def receiverDayCountFraction(self) -> Union[DayCountFraction, str]:
        """The day count fraction for the receiver"""
        return self.__receiverDayCountFraction

    @receiverDayCountFraction.setter
    def receiverDayCountFraction(self, value: Union[DayCountFraction, str]):
        self.__receiverDayCountFraction = value if isinstance(value, DayCountFraction) else get_enum_value(DayCountFraction, value)
        self._property_changed('receiverDayCountFraction')        

    @property
    def receiverBusinessDayConvention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention for the receiver"""
        return self.__receiverBusinessDayConvention

    @receiverBusinessDayConvention.setter
    def receiverBusinessDayConvention(self, value: Union[BusinessDayConvention, str]):
        self.__receiverBusinessDayConvention = value if isinstance(value, BusinessDayConvention) else get_enum_value(BusinessDayConvention, value)
        self._property_changed('receiverBusinessDayConvention')        

    @property
    def fee(self) -> float:
        """The fee"""
        return self.__fee

    @fee.setter
    def fee(self, value: float):
        self.__fee = value
        self._property_changed('fee')        

    @property
    def clearingHouse(self) -> Union[SwapClearingHouse, str]:
        """Swap Clearing House"""
        return self.__clearingHouse

    @clearingHouse.setter
    def clearingHouse(self, value: Union[SwapClearingHouse, str]):
        self.__clearingHouse = value if isinstance(value, SwapClearingHouse) else get_enum_value(SwapClearingHouse, value)
        self._property_changed('clearingHouse')        


class IRCap(Instrument):
        
    """Object representation of an interest rate cap"""
       
    def __init__(self, terminationDate: Union[datetime.date, str], notionalCurrency: Union[Currency, str], notionalAmount: float = 1000000.0, effectiveDate: Union[datetime.date, str] = None, floatingRateOption: str = None, floatingRateDesignatedMaturity: str = None, floatingRateFrequency: str = None, floatingRateDayCountFraction: Union[DayCountFraction, str] = None, floatingRateBusinessDayConvention: Union[BusinessDayConvention, str] = None, capRate: Union[float, str] = None, premium: float = 0, fee: float = 0):
        super().__init__()
        self.__terminationDate = terminationDate
        self.__notionalCurrency = notionalCurrency if isinstance(notionalCurrency, Currency) else get_enum_value(Currency, notionalCurrency)
        self.__notionalAmount = notionalAmount
        self.__effectiveDate = effectiveDate
        self.__floatingRateOption = floatingRateOption
        self.__floatingRateDesignatedMaturity = floatingRateDesignatedMaturity
        self.__floatingRateFrequency = floatingRateFrequency
        self.__floatingRateDayCountFraction = floatingRateDayCountFraction if isinstance(floatingRateDayCountFraction, DayCountFraction) else get_enum_value(DayCountFraction, floatingRateDayCountFraction)
        self.__floatingRateBusinessDayConvention = floatingRateBusinessDayConvention if isinstance(floatingRateBusinessDayConvention, BusinessDayConvention) else get_enum_value(BusinessDayConvention, floatingRateBusinessDayConvention)
        self.__capRate = capRate
        self.__premium = premium
        self.__fee = fee

    @property
    def assetClass(self) -> AssetClass:
        """Rates"""
        return AssetClass.Rates        

    @property
    def type(self) -> AssetType:
        """Cap"""
        return AssetType.Cap        

    @property
    def terminationDate(self) -> Union[datetime.date, str]:
        """The termination of the cap, e.g. 2025-04-01, 2y"""
        return self.__terminationDate

    @terminationDate.setter
    def terminationDate(self, value: Union[datetime.date, str]):
        self.__terminationDate = value
        self._property_changed('terminationDate')        

    @property
    def notionalCurrency(self) -> Union[Currency, str]:
        """Notional currency"""
        return self.__notionalCurrency

    @notionalCurrency.setter
    def notionalCurrency(self, value: Union[Currency, str]):
        self.__notionalCurrency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('notionalCurrency')        

    @property
    def notionalAmount(self) -> float:
        """Notional amount"""
        return self.__notionalAmount

    @notionalAmount.setter
    def notionalAmount(self, value: float):
        self.__notionalAmount = value
        self._property_changed('notionalAmount')        

    @property
    def effectiveDate(self) -> Union[datetime.date, str]:
        """The date on which the cap becomes effective"""
        return self.__effectiveDate

    @effectiveDate.setter
    def effectiveDate(self, value: Union[datetime.date, str]):
        self.__effectiveDate = value
        self._property_changed('effectiveDate')        

    @property
    def floatingRateOption(self) -> str:
        """The underlying benchmark for the floating rate, e.g. USD-LIBOR-BBA, EUR-EURIBOR-TELERATE"""
        return self.__floatingRateOption

    @floatingRateOption.setter
    def floatingRateOption(self, value: str):
        self.__floatingRateOption = value
        self._property_changed('floatingRateOption')        

    @property
    def floatingRateDesignatedMaturity(self) -> str:
        """Tenor of the floatingRateOption, e.g. 3m, 6m"""
        return self.__floatingRateDesignatedMaturity

    @floatingRateDesignatedMaturity.setter
    def floatingRateDesignatedMaturity(self, value: str):
        self.__floatingRateDesignatedMaturity = value
        self._property_changed('floatingRateDesignatedMaturity')        

    @property
    def floatingRateFrequency(self) -> str:
        """The frequency of floating payments, e.g. 3m"""
        return self.__floatingRateFrequency

    @floatingRateFrequency.setter
    def floatingRateFrequency(self, value: str):
        self.__floatingRateFrequency = value
        self._property_changed('floatingRateFrequency')        

    @property
    def floatingRateDayCountFraction(self) -> Union[DayCountFraction, str]:
        """The day count fraction of the floating rate"""
        return self.__floatingRateDayCountFraction

    @floatingRateDayCountFraction.setter
    def floatingRateDayCountFraction(self, value: Union[DayCountFraction, str]):
        self.__floatingRateDayCountFraction = value if isinstance(value, DayCountFraction) else get_enum_value(DayCountFraction, value)
        self._property_changed('floatingRateDayCountFraction')        

    @property
    def floatingRateBusinessDayConvention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention of the floating rate"""
        return self.__floatingRateBusinessDayConvention

    @floatingRateBusinessDayConvention.setter
    def floatingRateBusinessDayConvention(self, value: Union[BusinessDayConvention, str]):
        self.__floatingRateBusinessDayConvention = value if isinstance(value, BusinessDayConvention) else get_enum_value(BusinessDayConvention, value)
        self._property_changed('floatingRateBusinessDayConvention')        

    @property
    def capRate(self) -> Union[float, str]:
        """The rate of this cap, as value, percent or at-the-money e.g. 62.5, 95%, ATM-25, ATMF"""
        return self.__capRate

    @capRate.setter
    def capRate(self, value: Union[float, str]):
        self.__capRate = value
        self._property_changed('capRate')        

    @property
    def premium(self) -> float:
        """The premium"""
        return self.__premium

    @premium.setter
    def premium(self, value: float):
        self.__premium = value
        self._property_changed('premium')        

    @property
    def fee(self) -> float:
        """The fee"""
        return self.__fee

    @fee.setter
    def fee(self, value: float):
        self.__fee = value
        self._property_changed('fee')        


class IRFloor(Instrument):
        
    """Object representation of an interest rate floor"""
       
    def __init__(self, terminationDate: Union[datetime.date, str], notionalCurrency: Union[Currency, str], notionalAmount: float = 1000000.0, effectiveDate: Union[datetime.date, str] = None, floatingRateOption: str = None, floatingRateDesignatedMaturity: str = None, floatingRateFrequency: str = None, floatingRateDayCountFraction: Union[DayCountFraction, str] = None, floatingRateBusinessDayConvention: Union[BusinessDayConvention, str] = None, floorRate: Union[float, str] = None, fee: float = 0):
        super().__init__()
        self.__terminationDate = terminationDate
        self.__notionalCurrency = notionalCurrency if isinstance(notionalCurrency, Currency) else get_enum_value(Currency, notionalCurrency)
        self.__notionalAmount = notionalAmount
        self.__effectiveDate = effectiveDate
        self.__floatingRateOption = floatingRateOption
        self.__floatingRateDesignatedMaturity = floatingRateDesignatedMaturity
        self.__floatingRateFrequency = floatingRateFrequency
        self.__floatingRateDayCountFraction = floatingRateDayCountFraction if isinstance(floatingRateDayCountFraction, DayCountFraction) else get_enum_value(DayCountFraction, floatingRateDayCountFraction)
        self.__floatingRateBusinessDayConvention = floatingRateBusinessDayConvention if isinstance(floatingRateBusinessDayConvention, BusinessDayConvention) else get_enum_value(BusinessDayConvention, floatingRateBusinessDayConvention)
        self.__floorRate = floorRate
        self.__fee = fee

    @property
    def assetClass(self) -> AssetClass:
        """Rates"""
        return AssetClass.Rates        

    @property
    def type(self) -> AssetType:
        """Floor"""
        return AssetType.Floor        

    @property
    def terminationDate(self) -> Union[datetime.date, str]:
        """The termination of the floor, e.g. 2025-04-01, 2y"""
        return self.__terminationDate

    @terminationDate.setter
    def terminationDate(self, value: Union[datetime.date, str]):
        self.__terminationDate = value
        self._property_changed('terminationDate')        

    @property
    def notionalCurrency(self) -> Union[Currency, str]:
        """Notional currency"""
        return self.__notionalCurrency

    @notionalCurrency.setter
    def notionalCurrency(self, value: Union[Currency, str]):
        self.__notionalCurrency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('notionalCurrency')        

    @property
    def notionalAmount(self) -> float:
        """Notional amount"""
        return self.__notionalAmount

    @notionalAmount.setter
    def notionalAmount(self, value: float):
        self.__notionalAmount = value
        self._property_changed('notionalAmount')        

    @property
    def effectiveDate(self) -> Union[datetime.date, str]:
        """The date on which the floor becomes effective"""
        return self.__effectiveDate

    @effectiveDate.setter
    def effectiveDate(self, value: Union[datetime.date, str]):
        self.__effectiveDate = value
        self._property_changed('effectiveDate')        

    @property
    def floatingRateOption(self) -> str:
        """The underlying benchmark for the floating rate, e.g. USD-LIBOR-BBA, EUR-EURIBOR-TELERATE"""
        return self.__floatingRateOption

    @floatingRateOption.setter
    def floatingRateOption(self, value: str):
        self.__floatingRateOption = value
        self._property_changed('floatingRateOption')        

    @property
    def floatingRateDesignatedMaturity(self) -> str:
        """Tenor of the floatingRateOption, e.g. 3m, 6m"""
        return self.__floatingRateDesignatedMaturity

    @floatingRateDesignatedMaturity.setter
    def floatingRateDesignatedMaturity(self, value: str):
        self.__floatingRateDesignatedMaturity = value
        self._property_changed('floatingRateDesignatedMaturity')        

    @property
    def floatingRateFrequency(self) -> str:
        """The frequency of floating payments, e.g. 3m"""
        return self.__floatingRateFrequency

    @floatingRateFrequency.setter
    def floatingRateFrequency(self, value: str):
        self.__floatingRateFrequency = value
        self._property_changed('floatingRateFrequency')        

    @property
    def floatingRateDayCountFraction(self) -> Union[DayCountFraction, str]:
        """The day count fraction of the floating rate"""
        return self.__floatingRateDayCountFraction

    @floatingRateDayCountFraction.setter
    def floatingRateDayCountFraction(self, value: Union[DayCountFraction, str]):
        self.__floatingRateDayCountFraction = value if isinstance(value, DayCountFraction) else get_enum_value(DayCountFraction, value)
        self._property_changed('floatingRateDayCountFraction')        

    @property
    def floatingRateBusinessDayConvention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention of the floating rate"""
        return self.__floatingRateBusinessDayConvention

    @floatingRateBusinessDayConvention.setter
    def floatingRateBusinessDayConvention(self, value: Union[BusinessDayConvention, str]):
        self.__floatingRateBusinessDayConvention = value if isinstance(value, BusinessDayConvention) else get_enum_value(BusinessDayConvention, value)
        self._property_changed('floatingRateBusinessDayConvention')        

    @property
    def floorRate(self) -> Union[float, str]:
        """The rate of this floor, as value, percent or at-the-money e.g. 62.5, 95%, ATM-25, ATMF"""
        return self.__floorRate

    @floorRate.setter
    def floorRate(self, value: Union[float, str]):
        self.__floorRate = value
        self._property_changed('floorRate')        

    @property
    def fee(self) -> float:
        """The fee"""
        return self.__fee

    @fee.setter
    def fee(self, value: float):
        self.__fee = value
        self._property_changed('fee')        


class IRSwap(Instrument):
        
    """A vanilla interest rate swap of fixed vs floating cashflows"""
       
    def __init__(self, payOrReceive: Union[PayReceive, str], terminationDate: Union[datetime.date, str], notionalCurrency: Union[Currency, str], notionalAmount: float = 1000000.0, effectiveDate: Union[datetime.date, str] = None, floatingRateForTheInitialCalculationPeriod: float = None, floatingRateOption: str = None, floatingRateDesignatedMaturity: str = None, floatingRateSpread: float = None, floatingRateFrequency: str = None, floatingRateDayCountFraction: Union[DayCountFraction, str] = None, floatingRateBusinessDayConvention: Union[BusinessDayConvention, str] = None, fixedRate: Union[float, str] = None, fixedRateFrequency: str = None, fixedRateDayCountFraction: Union[DayCountFraction, str] = None, fixedRateBusinessDayConvention: Union[BusinessDayConvention, str] = None, fee: float = 0, clearingHouse: Union[SwapClearingHouse, str] = None):
        super().__init__()
        self.__payOrReceive = payOrReceive if isinstance(payOrReceive, PayReceive) else get_enum_value(PayReceive, payOrReceive)
        self.__terminationDate = terminationDate
        self.__notionalCurrency = notionalCurrency if isinstance(notionalCurrency, Currency) else get_enum_value(Currency, notionalCurrency)
        self.__notionalAmount = notionalAmount
        self.__effectiveDate = effectiveDate
        self.__floatingRateForTheInitialCalculationPeriod = floatingRateForTheInitialCalculationPeriod
        self.__floatingRateOption = floatingRateOption
        self.__floatingRateDesignatedMaturity = floatingRateDesignatedMaturity
        self.__floatingRateSpread = floatingRateSpread
        self.__floatingRateFrequency = floatingRateFrequency
        self.__floatingRateDayCountFraction = floatingRateDayCountFraction if isinstance(floatingRateDayCountFraction, DayCountFraction) else get_enum_value(DayCountFraction, floatingRateDayCountFraction)
        self.__floatingRateBusinessDayConvention = floatingRateBusinessDayConvention if isinstance(floatingRateBusinessDayConvention, BusinessDayConvention) else get_enum_value(BusinessDayConvention, floatingRateBusinessDayConvention)
        self.__fixedRate = fixedRate
        self.__fixedRateFrequency = fixedRateFrequency
        self.__fixedRateDayCountFraction = fixedRateDayCountFraction if isinstance(fixedRateDayCountFraction, DayCountFraction) else get_enum_value(DayCountFraction, fixedRateDayCountFraction)
        self.__fixedRateBusinessDayConvention = fixedRateBusinessDayConvention if isinstance(fixedRateBusinessDayConvention, BusinessDayConvention) else get_enum_value(BusinessDayConvention, fixedRateBusinessDayConvention)
        self.__fee = fee
        self.__clearingHouse = clearingHouse if isinstance(clearingHouse, SwapClearingHouse) else get_enum_value(SwapClearingHouse, clearingHouse)

    @property
    def assetClass(self) -> AssetClass:
        """Rates"""
        return AssetClass.Rates        

    @property
    def type(self) -> AssetType:
        """Swap"""
        return AssetType.Swap        

    @property
    def payOrReceive(self) -> Union[PayReceive, str]:
        """Pay or receive fixed"""
        return self.__payOrReceive

    @payOrReceive.setter
    def payOrReceive(self, value: Union[PayReceive, str]):
        self.__payOrReceive = value if isinstance(value, PayReceive) else get_enum_value(PayReceive, value)
        self._property_changed('payOrReceive')        

    @property
    def terminationDate(self) -> Union[datetime.date, str]:
        """The termination of the swap, e.g. 2050-04-01, 10y"""
        return self.__terminationDate

    @terminationDate.setter
    def terminationDate(self, value: Union[datetime.date, str]):
        self.__terminationDate = value
        self._property_changed('terminationDate')        

    @property
    def notionalCurrency(self) -> Union[Currency, str]:
        """Notional currency"""
        return self.__notionalCurrency

    @notionalCurrency.setter
    def notionalCurrency(self, value: Union[Currency, str]):
        self.__notionalCurrency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('notionalCurrency')        

    @property
    def notionalAmount(self) -> float:
        """Notional amount"""
        return self.__notionalAmount

    @notionalAmount.setter
    def notionalAmount(self, value: float):
        self.__notionalAmount = value
        self._property_changed('notionalAmount')        

    @property
    def effectiveDate(self) -> Union[datetime.date, str]:
        """The date on which the swap becomes effective"""
        return self.__effectiveDate

    @effectiveDate.setter
    def effectiveDate(self, value: Union[datetime.date, str]):
        self.__effectiveDate = value
        self._property_changed('effectiveDate')        

    @property
    def floatingRateForTheInitialCalculationPeriod(self) -> float:
        """First fixing"""
        return self.__floatingRateForTheInitialCalculationPeriod

    @floatingRateForTheInitialCalculationPeriod.setter
    def floatingRateForTheInitialCalculationPeriod(self, value: float):
        self.__floatingRateForTheInitialCalculationPeriod = value
        self._property_changed('floatingRateForTheInitialCalculationPeriod')        

    @property
    def floatingRateOption(self) -> str:
        """The underlying benchmark for the floating rate, e.g. USD-LIBOR-BBA, EUR-EURIBOR-TELERATE"""
        return self.__floatingRateOption

    @floatingRateOption.setter
    def floatingRateOption(self, value: str):
        self.__floatingRateOption = value
        self._property_changed('floatingRateOption')        

    @property
    def floatingRateDesignatedMaturity(self) -> str:
        """Tenor of the floatingRateOption, e.g. 3m, 6m"""
        return self.__floatingRateDesignatedMaturity

    @floatingRateDesignatedMaturity.setter
    def floatingRateDesignatedMaturity(self, value: str):
        self.__floatingRateDesignatedMaturity = value
        self._property_changed('floatingRateDesignatedMaturity')        

    @property
    def floatingRateSpread(self) -> float:
        """The spread over the floating rate"""
        return self.__floatingRateSpread

    @floatingRateSpread.setter
    def floatingRateSpread(self, value: float):
        self.__floatingRateSpread = value
        self._property_changed('floatingRateSpread')        

    @property
    def floatingRateFrequency(self) -> str:
        """The frequency of floating payments, e.g. 3m"""
        return self.__floatingRateFrequency

    @floatingRateFrequency.setter
    def floatingRateFrequency(self, value: str):
        self.__floatingRateFrequency = value
        self._property_changed('floatingRateFrequency')        

    @property
    def floatingRateDayCountFraction(self) -> Union[DayCountFraction, str]:
        """The day count fraction of the floating rate"""
        return self.__floatingRateDayCountFraction

    @floatingRateDayCountFraction.setter
    def floatingRateDayCountFraction(self, value: Union[DayCountFraction, str]):
        self.__floatingRateDayCountFraction = value if isinstance(value, DayCountFraction) else get_enum_value(DayCountFraction, value)
        self._property_changed('floatingRateDayCountFraction')        

    @property
    def floatingRateBusinessDayConvention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention of the floating rate"""
        return self.__floatingRateBusinessDayConvention

    @floatingRateBusinessDayConvention.setter
    def floatingRateBusinessDayConvention(self, value: Union[BusinessDayConvention, str]):
        self.__floatingRateBusinessDayConvention = value if isinstance(value, BusinessDayConvention) else get_enum_value(BusinessDayConvention, value)
        self._property_changed('floatingRateBusinessDayConvention')        

    @property
    def fixedRate(self) -> Union[float, str]:
        """The coupon of the fixed leg"""
        return self.__fixedRate

    @fixedRate.setter
    def fixedRate(self, value: Union[float, str]):
        self.__fixedRate = value
        self._property_changed('fixedRate')        

    @property
    def fixedRateFrequency(self) -> str:
        """The frequency of fixed payments, e.g. 6m"""
        return self.__fixedRateFrequency

    @fixedRateFrequency.setter
    def fixedRateFrequency(self, value: str):
        self.__fixedRateFrequency = value
        self._property_changed('fixedRateFrequency')        

    @property
    def fixedRateDayCountFraction(self) -> Union[DayCountFraction, str]:
        """The day count fraction for the fixed rate"""
        return self.__fixedRateDayCountFraction

    @fixedRateDayCountFraction.setter
    def fixedRateDayCountFraction(self, value: Union[DayCountFraction, str]):
        self.__fixedRateDayCountFraction = value if isinstance(value, DayCountFraction) else get_enum_value(DayCountFraction, value)
        self._property_changed('fixedRateDayCountFraction')        

    @property
    def fixedRateBusinessDayConvention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention for the fixed rate"""
        return self.__fixedRateBusinessDayConvention

    @fixedRateBusinessDayConvention.setter
    def fixedRateBusinessDayConvention(self, value: Union[BusinessDayConvention, str]):
        self.__fixedRateBusinessDayConvention = value if isinstance(value, BusinessDayConvention) else get_enum_value(BusinessDayConvention, value)
        self._property_changed('fixedRateBusinessDayConvention')        

    @property
    def fee(self) -> float:
        """The fee"""
        return self.__fee

    @fee.setter
    def fee(self, value: float):
        self.__fee = value
        self._property_changed('fee')        

    @property
    def clearingHouse(self) -> Union[SwapClearingHouse, str]:
        """Swap Clearing House"""
        return self.__clearingHouse

    @clearingHouse.setter
    def clearingHouse(self, value: Union[SwapClearingHouse, str]):
        self.__clearingHouse = value if isinstance(value, SwapClearingHouse) else get_enum_value(SwapClearingHouse, value)
        self._property_changed('clearingHouse')        


class IRSwaption(Instrument):
        
    """Object representation of a swaption"""
       
    def __init__(self, payOrReceive: str, terminationDate: Union[datetime.date, str], notionalCurrency: Union[Currency, str], effectiveDate: Union[datetime.date, str] = None, notionalAmount: float = 1000000.0, expirationDate: Union[datetime.date, str] = None, floatingRateOption: str = None, floatingRateDesignatedMaturity: str = None, floatingRateSpread: float = None, floatingRateFrequency: str = None, floatingRateDayCountFraction: Union[DayCountFraction, str] = None, floatingRateBusinessDayConvention: Union[BusinessDayConvention, str] = None, fixedRateFrequency: str = None, fixedRateDayCountFraction: Union[DayCountFraction, str] = None, fixedRateBusinessDayConvention: Union[BusinessDayConvention, str] = None, strike: Union[float, str] = None, premium: float = 0, fee: float = 0, clearingHouse: Union[SwapClearingHouse, str] = None, settlement: Union[SwapSettlement, str] = None, premiumPaymentDate: Union[datetime.date, str] = None):
        super().__init__()
        self.__payOrReceive = payOrReceive
        self.__effectiveDate = effectiveDate
        self.__terminationDate = terminationDate
        self.__notionalCurrency = notionalCurrency if isinstance(notionalCurrency, Currency) else get_enum_value(Currency, notionalCurrency)
        self.__notionalAmount = notionalAmount
        self.__expirationDate = expirationDate
        self.__floatingRateOption = floatingRateOption
        self.__floatingRateDesignatedMaturity = floatingRateDesignatedMaturity
        self.__floatingRateSpread = floatingRateSpread
        self.__floatingRateFrequency = floatingRateFrequency
        self.__floatingRateDayCountFraction = floatingRateDayCountFraction if isinstance(floatingRateDayCountFraction, DayCountFraction) else get_enum_value(DayCountFraction, floatingRateDayCountFraction)
        self.__floatingRateBusinessDayConvention = floatingRateBusinessDayConvention if isinstance(floatingRateBusinessDayConvention, BusinessDayConvention) else get_enum_value(BusinessDayConvention, floatingRateBusinessDayConvention)
        self.__fixedRateFrequency = fixedRateFrequency
        self.__fixedRateDayCountFraction = fixedRateDayCountFraction if isinstance(fixedRateDayCountFraction, DayCountFraction) else get_enum_value(DayCountFraction, fixedRateDayCountFraction)
        self.__fixedRateBusinessDayConvention = fixedRateBusinessDayConvention if isinstance(fixedRateBusinessDayConvention, BusinessDayConvention) else get_enum_value(BusinessDayConvention, fixedRateBusinessDayConvention)
        self.__strike = strike
        self.__premium = premium
        self.__fee = fee
        self.__clearingHouse = clearingHouse if isinstance(clearingHouse, SwapClearingHouse) else get_enum_value(SwapClearingHouse, clearingHouse)
        self.__settlement = settlement if isinstance(settlement, SwapSettlement) else get_enum_value(SwapSettlement, settlement)
        self.__premiumPaymentDate = premiumPaymentDate

    @property
    def assetClass(self) -> AssetClass:
        """Rates"""
        return AssetClass.Rates        

    @property
    def type(self) -> AssetType:
        """Swaption"""
        return AssetType.Swaption        

    @property
    def payOrReceive(self) -> str:
        """Pay or receive fixed"""
        return self.__payOrReceive

    @payOrReceive.setter
    def payOrReceive(self, value: str):
        self.__payOrReceive = value
        self._property_changed('payOrReceive')        

    @property
    def effectiveDate(self) -> Union[datetime.date, str]:
        """Swaption effective date, e.g. 2019-01-01, 10y"""
        return self.__effectiveDate

    @effectiveDate.setter
    def effectiveDate(self, value: Union[datetime.date, str]):
        self.__effectiveDate = value
        self._property_changed('effectiveDate')        

    @property
    def terminationDate(self) -> Union[datetime.date, str]:
        """Swaption termination date, e.g. 2030-05-01, 10y"""
        return self.__terminationDate

    @terminationDate.setter
    def terminationDate(self, value: Union[datetime.date, str]):
        self.__terminationDate = value
        self._property_changed('terminationDate')        

    @property
    def notionalCurrency(self) -> Union[Currency, str]:
        """Notional currency"""
        return self.__notionalCurrency

    @notionalCurrency.setter
    def notionalCurrency(self, value: Union[Currency, str]):
        self.__notionalCurrency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('notionalCurrency')        

    @property
    def notionalAmount(self) -> float:
        """Notional amount"""
        return self.__notionalAmount

    @notionalAmount.setter
    def notionalAmount(self, value: float):
        self.__notionalAmount = value
        self._property_changed('notionalAmount')        

    @property
    def expirationDate(self) -> Union[datetime.date, str]:
        """Swaption expiration date, 2020-05-01, 3m"""
        return self.__expirationDate

    @expirationDate.setter
    def expirationDate(self, value: Union[datetime.date, str]):
        self.__expirationDate = value
        self._property_changed('expirationDate')        

    @property
    def floatingRateOption(self) -> str:
        """The underlying benchmark for the floating rate, e.g. USD-LIBOR-BBA, EUR-EURIBOR-TELERATE"""
        return self.__floatingRateOption

    @floatingRateOption.setter
    def floatingRateOption(self, value: str):
        self.__floatingRateOption = value
        self._property_changed('floatingRateOption')        

    @property
    def floatingRateDesignatedMaturity(self) -> str:
        """Tenor"""
        return self.__floatingRateDesignatedMaturity

    @floatingRateDesignatedMaturity.setter
    def floatingRateDesignatedMaturity(self, value: str):
        self.__floatingRateDesignatedMaturity = value
        self._property_changed('floatingRateDesignatedMaturity')        

    @property
    def floatingRateSpread(self) -> float:
        """The spread over the floating rate"""
        return self.__floatingRateSpread

    @floatingRateSpread.setter
    def floatingRateSpread(self, value: float):
        self.__floatingRateSpread = value
        self._property_changed('floatingRateSpread')        

    @property
    def floatingRateFrequency(self) -> str:
        """The frequency of floating payments, e.g. 3m"""
        return self.__floatingRateFrequency

    @floatingRateFrequency.setter
    def floatingRateFrequency(self, value: str):
        self.__floatingRateFrequency = value
        self._property_changed('floatingRateFrequency')        

    @property
    def floatingRateDayCountFraction(self) -> Union[DayCountFraction, str]:
        """The day count fraction of the floating rate"""
        return self.__floatingRateDayCountFraction

    @floatingRateDayCountFraction.setter
    def floatingRateDayCountFraction(self, value: Union[DayCountFraction, str]):
        self.__floatingRateDayCountFraction = value if isinstance(value, DayCountFraction) else get_enum_value(DayCountFraction, value)
        self._property_changed('floatingRateDayCountFraction')        

    @property
    def floatingRateBusinessDayConvention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention of the floating rate"""
        return self.__floatingRateBusinessDayConvention

    @floatingRateBusinessDayConvention.setter
    def floatingRateBusinessDayConvention(self, value: Union[BusinessDayConvention, str]):
        self.__floatingRateBusinessDayConvention = value if isinstance(value, BusinessDayConvention) else get_enum_value(BusinessDayConvention, value)
        self._property_changed('floatingRateBusinessDayConvention')        

    @property
    def fixedRateFrequency(self) -> str:
        """The frequency of fixed payments, e.g. 6m"""
        return self.__fixedRateFrequency

    @fixedRateFrequency.setter
    def fixedRateFrequency(self, value: str):
        self.__fixedRateFrequency = value
        self._property_changed('fixedRateFrequency')        

    @property
    def fixedRateDayCountFraction(self) -> Union[DayCountFraction, str]:
        """The day count fraction for the fixed rate"""
        return self.__fixedRateDayCountFraction

    @fixedRateDayCountFraction.setter
    def fixedRateDayCountFraction(self, value: Union[DayCountFraction, str]):
        self.__fixedRateDayCountFraction = value if isinstance(value, DayCountFraction) else get_enum_value(DayCountFraction, value)
        self._property_changed('fixedRateDayCountFraction')        

    @property
    def fixedRateBusinessDayConvention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention for the fixed rate"""
        return self.__fixedRateBusinessDayConvention

    @fixedRateBusinessDayConvention.setter
    def fixedRateBusinessDayConvention(self, value: Union[BusinessDayConvention, str]):
        self.__fixedRateBusinessDayConvention = value if isinstance(value, BusinessDayConvention) else get_enum_value(BusinessDayConvention, value)
        self._property_changed('fixedRateBusinessDayConvention')        

    @property
    def strike(self) -> Union[float, str]:
        """Strike as value, percent or at-the-money e.g. 62.5, 95%, ATM-25, ATMF"""
        return self.__strike

    @strike.setter
    def strike(self, value: Union[float, str]):
        self.__strike = value
        self._property_changed('strike')        

    @property
    def premium(self) -> float:
        """The premium"""
        return self.__premium

    @premium.setter
    def premium(self, value: float):
        self.__premium = value
        self._property_changed('premium')        

    @property
    def fee(self) -> float:
        """The fee"""
        return self.__fee

    @fee.setter
    def fee(self, value: float):
        self.__fee = value
        self._property_changed('fee')        

    @property
    def clearingHouse(self) -> Union[SwapClearingHouse, str]:
        """Swap Clearing House"""
        return self.__clearingHouse

    @clearingHouse.setter
    def clearingHouse(self, value: Union[SwapClearingHouse, str]):
        self.__clearingHouse = value if isinstance(value, SwapClearingHouse) else get_enum_value(SwapClearingHouse, value)
        self._property_changed('clearingHouse')        

    @property
    def settlement(self) -> Union[SwapSettlement, str]:
        """Swap Settlement Type"""
        return self.__settlement

    @settlement.setter
    def settlement(self, value: Union[SwapSettlement, str]):
        self.__settlement = value if isinstance(value, SwapSettlement) else get_enum_value(SwapSettlement, value)
        self._property_changed('settlement')        

    @property
    def premiumPaymentDate(self) -> Union[datetime.date, str]:
        """Date or tenor, e.g. 2018-09-03, 3m"""
        return self.__premiumPaymentDate

    @premiumPaymentDate.setter
    def premiumPaymentDate(self, value: Union[datetime.date, str]):
        self.__premiumPaymentDate = value
        self._property_changed('premiumPaymentDate')        
