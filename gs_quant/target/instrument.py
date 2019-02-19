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

import datetime
from typing import Any, Iterable, Union
from gs_quant.base import Instrument


class IRSwaption(Instrument):
        
    """Object representation of a swaption"""
       
    def __init__(self, payOrReceive: str, terminationDate: Union['DateOrTenor', str], notionalCurrency: Union['Currency', str], effectiveDate: Union[datetime.date, str] = None, notionalAmount: float = 1000000.0, expirationDate: Union['DateOrTenor', str] = None, floatingRateOption: str = None, floatingRateDesignatedMaturity: Union[str, str] = None, floatingRateSpread: float = None, floatingRateFrequency: Union[str, str] = None, floatingRateDayCountFraction: Union['DayCountFraction', str] = None, floatingRateBusinessDayConvention: Union['BusinessDayConvention', str] = None, fixedRateFrequency: Union[str, str] = None, fixedRateDayCountFraction: Union['DayCountFraction', str] = None, fixedRateBusinessDayConvention: Union['BusinessDayConvention', str] = None, strike: Union['Strike', str] = None):
        super().__init__()
        self.__payOrReceive = payOrReceive
        self.__effectiveDate = effectiveDate
        self.__terminationDate = terminationDate
        self.__notionalCurrency = notionalCurrency
        self.__notionalAmount = notionalAmount
        self.__expirationDate = expirationDate
        self.__floatingRateOption = floatingRateOption
        self.__floatingRateDesignatedMaturity = floatingRateDesignatedMaturity
        self.__floatingRateSpread = floatingRateSpread
        self.__floatingRateFrequency = floatingRateFrequency
        self.__floatingRateDayCountFraction = floatingRateDayCountFraction
        self.__floatingRateBusinessDayConvention = floatingRateBusinessDayConvention
        self.__fixedRateFrequency = fixedRateFrequency
        self.__fixedRateDayCountFraction = fixedRateDayCountFraction
        self.__fixedRateBusinessDayConvention = fixedRateBusinessDayConvention
        self.__strike = strike

    @property
    def assetClass(self) -> str:
        """Rates"""
        return 'Rates'        

    @property
    def type(self) -> str:
        """Swaption"""
        return 'Swaption'        

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
        """ISO 8601-formatted date"""
        return self.__effectiveDate

    @effectiveDate.setter
    def effectiveDate(self, value: Union[datetime.date, str]):
        self.__effectiveDate = value
        self._property_changed('effectiveDate')        

    @property
    def terminationDate(self) -> Union['DateOrTenor', str]:
        """Swap termination date"""
        return self.__terminationDate

    @terminationDate.setter
    def terminationDate(self, value: Union['DateOrTenor', str]):
        self.__terminationDate = value
        self._property_changed('terminationDate')        

    @property
    def notionalCurrency(self) -> Union['Currency', str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__notionalCurrency

    @notionalCurrency.setter
    def notionalCurrency(self, value: Union['Currency', str]):
        self.__notionalCurrency = value
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
    def expirationDate(self) -> Union['DateOrTenor', str]:
        """Swaption expiration date"""
        return self.__expirationDate

    @expirationDate.setter
    def expirationDate(self, value: Union['DateOrTenor', str]):
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
    def floatingRateDesignatedMaturity(self) -> Union[str, str]:
        """Tenor"""
        return self.__floatingRateDesignatedMaturity

    @floatingRateDesignatedMaturity.setter
    def floatingRateDesignatedMaturity(self, value: Union[str, str]):
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
    def floatingRateFrequency(self) -> Union[str, str]:
        """Tenor"""
        return self.__floatingRateFrequency

    @floatingRateFrequency.setter
    def floatingRateFrequency(self, value: Union[str, str]):
        self.__floatingRateFrequency = value
        self._property_changed('floatingRateFrequency')        

    @property
    def floatingRateDayCountFraction(self) -> Union['DayCountFraction', str]:
        """Day Count Fraction."""
        return self.__floatingRateDayCountFraction

    @floatingRateDayCountFraction.setter
    def floatingRateDayCountFraction(self, value: Union['DayCountFraction', str]):
        self.__floatingRateDayCountFraction = value
        self._property_changed('floatingRateDayCountFraction')        

    @property
    def floatingRateBusinessDayConvention(self) -> Union['BusinessDayConvention', str]:
        """Business Day Convention."""
        return self.__floatingRateBusinessDayConvention

    @floatingRateBusinessDayConvention.setter
    def floatingRateBusinessDayConvention(self, value: Union['BusinessDayConvention', str]):
        self.__floatingRateBusinessDayConvention = value
        self._property_changed('floatingRateBusinessDayConvention')        

    @property
    def fixedRateFrequency(self) -> Union[str, str]:
        """Tenor"""
        return self.__fixedRateFrequency

    @fixedRateFrequency.setter
    def fixedRateFrequency(self, value: Union[str, str]):
        self.__fixedRateFrequency = value
        self._property_changed('fixedRateFrequency')        

    @property
    def fixedRateDayCountFraction(self) -> Union['DayCountFraction', str]:
        """Day Count Fraction."""
        return self.__fixedRateDayCountFraction

    @fixedRateDayCountFraction.setter
    def fixedRateDayCountFraction(self, value: Union['DayCountFraction', str]):
        self.__fixedRateDayCountFraction = value
        self._property_changed('fixedRateDayCountFraction')        

    @property
    def fixedRateBusinessDayConvention(self) -> Union['BusinessDayConvention', str]:
        """Business Day Convention."""
        return self.__fixedRateBusinessDayConvention

    @fixedRateBusinessDayConvention.setter
    def fixedRateBusinessDayConvention(self, value: Union['BusinessDayConvention', str]):
        self.__fixedRateBusinessDayConvention = value
        self._property_changed('fixedRateBusinessDayConvention')        

    @property
    def strike(self) -> Union['Strike', str]:
        """Strike as value, percent or at-the-money e.g. 62.5, 95%, ATM, ATMF"""
        return self.__strike

    @strike.setter
    def strike(self, value: Union['Strike', str]):
        self.__strike = value
        self._property_changed('strike')        


class IRBasisSwap(Instrument):
        
    """Object representation of an interest rate basis swap"""
       
    def __init__(self, terminationDate: Union['DateOrTenor', str], payerCurrency: Union['Currency', str], receiverCurrency: Union['Currency', str], notionalAmount: float = 1000000.0, effectiveDate: Union[datetime.date, str] = None, payerSpread: float = None, payerRateOption: str = None, payerDesignatedMaturity: Union[str, str] = None, payerFrequency: Union[str, str] = None, payerDayCountFraction: Union['DayCountFraction', str] = None, payerBusinessDayConvention: Union['BusinessDayConvention', str] = None, receiverSpread: float = None, receiverRateOption: str = None, receiverDesignatedMaturity: Union[str, str] = None, receiverFrequency: Union[str, str] = None, receiverDayCountFraction: Union['DayCountFraction', str] = None, receiverBusinessDayConvention: Union['BusinessDayConvention', str] = None):
        super().__init__()
        self.__notionalAmount = notionalAmount
        self.__effectiveDate = effectiveDate
        self.__terminationDate = terminationDate
        self.__payerSpread = payerSpread
        self.__payerCurrency = payerCurrency
        self.__payerRateOption = payerRateOption
        self.__payerDesignatedMaturity = payerDesignatedMaturity
        self.__payerFrequency = payerFrequency
        self.__payerDayCountFraction = payerDayCountFraction
        self.__payerBusinessDayConvention = payerBusinessDayConvention
        self.__receiverSpread = receiverSpread
        self.__receiverCurrency = receiverCurrency
        self.__receiverRateOption = receiverRateOption
        self.__receiverDesignatedMaturity = receiverDesignatedMaturity
        self.__receiverFrequency = receiverFrequency
        self.__receiverDayCountFraction = receiverDayCountFraction
        self.__receiverBusinessDayConvention = receiverBusinessDayConvention

    @property
    def assetClass(self) -> str:
        """Rates"""
        return 'Rates'        

    @property
    def type(self) -> str:
        """BasisSwap"""
        return 'BasisSwap'        

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
        """ISO 8601-formatted date"""
        return self.__effectiveDate

    @effectiveDate.setter
    def effectiveDate(self, value: Union[datetime.date, str]):
        self.__effectiveDate = value
        self._property_changed('effectiveDate')        

    @property
    def terminationDate(self) -> Union['DateOrTenor', str]:
        """Date or tenor, e.g. 2018-09-03, 3m"""
        return self.__terminationDate

    @terminationDate.setter
    def terminationDate(self, value: Union['DateOrTenor', str]):
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
    def payerCurrency(self) -> Union['Currency', str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__payerCurrency

    @payerCurrency.setter
    def payerCurrency(self, value: Union['Currency', str]):
        self.__payerCurrency = value
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
    def payerDesignatedMaturity(self) -> Union[str, str]:
        """Tenor"""
        return self.__payerDesignatedMaturity

    @payerDesignatedMaturity.setter
    def payerDesignatedMaturity(self, value: Union[str, str]):
        self.__payerDesignatedMaturity = value
        self._property_changed('payerDesignatedMaturity')        

    @property
    def payerFrequency(self) -> Union[str, str]:
        """Tenor"""
        return self.__payerFrequency

    @payerFrequency.setter
    def payerFrequency(self, value: Union[str, str]):
        self.__payerFrequency = value
        self._property_changed('payerFrequency')        

    @property
    def payerDayCountFraction(self) -> Union['DayCountFraction', str]:
        """Day Count Fraction."""
        return self.__payerDayCountFraction

    @payerDayCountFraction.setter
    def payerDayCountFraction(self, value: Union['DayCountFraction', str]):
        self.__payerDayCountFraction = value
        self._property_changed('payerDayCountFraction')        

    @property
    def payerBusinessDayConvention(self) -> Union['BusinessDayConvention', str]:
        """Business Day Convention."""
        return self.__payerBusinessDayConvention

    @payerBusinessDayConvention.setter
    def payerBusinessDayConvention(self, value: Union['BusinessDayConvention', str]):
        self.__payerBusinessDayConvention = value
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
    def receiverCurrency(self) -> Union['Currency', str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__receiverCurrency

    @receiverCurrency.setter
    def receiverCurrency(self, value: Union['Currency', str]):
        self.__receiverCurrency = value
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
    def receiverDesignatedMaturity(self) -> Union[str, str]:
        """Tenor"""
        return self.__receiverDesignatedMaturity

    @receiverDesignatedMaturity.setter
    def receiverDesignatedMaturity(self, value: Union[str, str]):
        self.__receiverDesignatedMaturity = value
        self._property_changed('receiverDesignatedMaturity')        

    @property
    def receiverFrequency(self) -> Union[str, str]:
        """Tenor"""
        return self.__receiverFrequency

    @receiverFrequency.setter
    def receiverFrequency(self, value: Union[str, str]):
        self.__receiverFrequency = value
        self._property_changed('receiverFrequency')        

    @property
    def receiverDayCountFraction(self) -> Union['DayCountFraction', str]:
        """Day Count Fraction."""
        return self.__receiverDayCountFraction

    @receiverDayCountFraction.setter
    def receiverDayCountFraction(self, value: Union['DayCountFraction', str]):
        self.__receiverDayCountFraction = value
        self._property_changed('receiverDayCountFraction')        

    @property
    def receiverBusinessDayConvention(self) -> Union['BusinessDayConvention', str]:
        """Business Day Convention."""
        return self.__receiverBusinessDayConvention

    @receiverBusinessDayConvention.setter
    def receiverBusinessDayConvention(self, value: Union['BusinessDayConvention', str]):
        self.__receiverBusinessDayConvention = value
        self._property_changed('receiverBusinessDayConvention')        


class IRSwap(Instrument):
        
    """Object representation of a vanilla interest rate swap"""
       
    def __init__(self, payOrReceive: Union['PayReceive', str], terminationDate: Union['DateOrTenor', str], notionalCurrency: Union['Currency', str], notionalAmount: float = 1000000.0, effectiveDate: Union[datetime.date, str] = None, floatingRateForTheInitialCalculationPeriod: float = None, floatingRateOption: str = None, floatingRateDesignatedMaturity: Union[str, str] = None, floatingRateSpread: float = None, floatingRateFrequency: Union[str, str] = None, floatingRateDayCountFraction: Union['DayCountFraction', str] = None, floatingRateBusinessDayConvention: Union['BusinessDayConvention', str] = None, fixedRate: float = None, fixedRateFrequency: Union[str, str] = None, fixedRateDayCountFraction: Union['DayCountFraction', str] = None, fixedRateBusinessDayConvention: Union['BusinessDayConvention', str] = None):
        super().__init__()
        self.__payOrReceive = payOrReceive
        self.__terminationDate = terminationDate
        self.__notionalCurrency = notionalCurrency
        self.__notionalAmount = notionalAmount
        self.__effectiveDate = effectiveDate
        self.__floatingRateForTheInitialCalculationPeriod = floatingRateForTheInitialCalculationPeriod
        self.__floatingRateOption = floatingRateOption
        self.__floatingRateDesignatedMaturity = floatingRateDesignatedMaturity
        self.__floatingRateSpread = floatingRateSpread
        self.__floatingRateFrequency = floatingRateFrequency
        self.__floatingRateDayCountFraction = floatingRateDayCountFraction
        self.__floatingRateBusinessDayConvention = floatingRateBusinessDayConvention
        self.__fixedRate = fixedRate
        self.__fixedRateFrequency = fixedRateFrequency
        self.__fixedRateDayCountFraction = fixedRateDayCountFraction
        self.__fixedRateBusinessDayConvention = fixedRateBusinessDayConvention

    @property
    def assetClass(self) -> str:
        """Rates"""
        return 'Rates'        

    @property
    def type(self) -> str:
        """Swap"""
        return 'Swap'        

    @property
    def payOrReceive(self) -> Union['PayReceive', str]:
        """Pay or receive fixed"""
        return self.__payOrReceive

    @payOrReceive.setter
    def payOrReceive(self, value: Union['PayReceive', str]):
        self.__payOrReceive = value
        self._property_changed('payOrReceive')        

    @property
    def terminationDate(self) -> Union['DateOrTenor', str]:
        """Date or tenor, e.g. 2018-09-03, 3m"""
        return self.__terminationDate

    @terminationDate.setter
    def terminationDate(self, value: Union['DateOrTenor', str]):
        self.__terminationDate = value
        self._property_changed('terminationDate')        

    @property
    def notionalCurrency(self) -> Union['Currency', str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__notionalCurrency

    @notionalCurrency.setter
    def notionalCurrency(self, value: Union['Currency', str]):
        self.__notionalCurrency = value
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
        """ISO 8601-formatted date"""
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
    def floatingRateDesignatedMaturity(self) -> Union[str, str]:
        """Tenor"""
        return self.__floatingRateDesignatedMaturity

    @floatingRateDesignatedMaturity.setter
    def floatingRateDesignatedMaturity(self, value: Union[str, str]):
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
    def floatingRateFrequency(self) -> Union[str, str]:
        """Tenor"""
        return self.__floatingRateFrequency

    @floatingRateFrequency.setter
    def floatingRateFrequency(self, value: Union[str, str]):
        self.__floatingRateFrequency = value
        self._property_changed('floatingRateFrequency')        

    @property
    def floatingRateDayCountFraction(self) -> Union['DayCountFraction', str]:
        """Day Count Fraction."""
        return self.__floatingRateDayCountFraction

    @floatingRateDayCountFraction.setter
    def floatingRateDayCountFraction(self, value: Union['DayCountFraction', str]):
        self.__floatingRateDayCountFraction = value
        self._property_changed('floatingRateDayCountFraction')        

    @property
    def floatingRateBusinessDayConvention(self) -> Union['BusinessDayConvention', str]:
        """Business Day Convention."""
        return self.__floatingRateBusinessDayConvention

    @floatingRateBusinessDayConvention.setter
    def floatingRateBusinessDayConvention(self, value: Union['BusinessDayConvention', str]):
        self.__floatingRateBusinessDayConvention = value
        self._property_changed('floatingRateBusinessDayConvention')        

    @property
    def fixedRate(self) -> float:
        """The coupon of the fixed leg"""
        return self.__fixedRate

    @fixedRate.setter
    def fixedRate(self, value: float):
        self.__fixedRate = value
        self._property_changed('fixedRate')        

    @property
    def fixedRateFrequency(self) -> Union[str, str]:
        """Tenor"""
        return self.__fixedRateFrequency

    @fixedRateFrequency.setter
    def fixedRateFrequency(self, value: Union[str, str]):
        self.__fixedRateFrequency = value
        self._property_changed('fixedRateFrequency')        

    @property
    def fixedRateDayCountFraction(self) -> Union['DayCountFraction', str]:
        """Day Count Fraction."""
        return self.__fixedRateDayCountFraction

    @fixedRateDayCountFraction.setter
    def fixedRateDayCountFraction(self, value: Union['DayCountFraction', str]):
        self.__fixedRateDayCountFraction = value
        self._property_changed('fixedRateDayCountFraction')        

    @property
    def fixedRateBusinessDayConvention(self) -> Union['BusinessDayConvention', str]:
        """Business Day Convention."""
        return self.__fixedRateBusinessDayConvention

    @fixedRateBusinessDayConvention.setter
    def fixedRateBusinessDayConvention(self, value: Union['BusinessDayConvention', str]):
        self.__fixedRateBusinessDayConvention = value
        self._property_changed('fixedRateBusinessDayConvention')        


class IRFloor(Instrument):
        
    """Object representation of an interest rate floor"""
       
    def __init__(self, terminationDate: Union['DateOrTenor', str], notionalCurrency: Union['Currency', str], notionalAmount: float = 1000000.0, effectiveDate: Union[datetime.date, str] = None, floatingRateOption: str = None, floatingRateDesignatedMaturity: Union[str, str] = None, floatingRateFrequency: Union[str, str] = None, floatingRateDayCountFraction: Union['DayCountFraction', str] = None, floatingRateBusinessDayConvention: Union['BusinessDayConvention', str] = None, floorRate: Union['Strike', str] = None):
        super().__init__()
        self.__terminationDate = terminationDate
        self.__notionalCurrency = notionalCurrency
        self.__notionalAmount = notionalAmount
        self.__effectiveDate = effectiveDate
        self.__floatingRateOption = floatingRateOption
        self.__floatingRateDesignatedMaturity = floatingRateDesignatedMaturity
        self.__floatingRateFrequency = floatingRateFrequency
        self.__floatingRateDayCountFraction = floatingRateDayCountFraction
        self.__floatingRateBusinessDayConvention = floatingRateBusinessDayConvention
        self.__floorRate = floorRate

    @property
    def assetClass(self) -> str:
        """Rates"""
        return 'Rates'        

    @property
    def type(self) -> str:
        """Floor"""
        return 'Floor'        

    @property
    def terminationDate(self) -> Union['DateOrTenor', str]:
        """Date or tenor, e.g. 2018-09-03, 3m"""
        return self.__terminationDate

    @terminationDate.setter
    def terminationDate(self, value: Union['DateOrTenor', str]):
        self.__terminationDate = value
        self._property_changed('terminationDate')        

    @property
    def notionalCurrency(self) -> Union['Currency', str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__notionalCurrency

    @notionalCurrency.setter
    def notionalCurrency(self, value: Union['Currency', str]):
        self.__notionalCurrency = value
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
        """ISO 8601-formatted date"""
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
    def floatingRateDesignatedMaturity(self) -> Union[str, str]:
        """Tenor"""
        return self.__floatingRateDesignatedMaturity

    @floatingRateDesignatedMaturity.setter
    def floatingRateDesignatedMaturity(self, value: Union[str, str]):
        self.__floatingRateDesignatedMaturity = value
        self._property_changed('floatingRateDesignatedMaturity')        

    @property
    def floatingRateFrequency(self) -> Union[str, str]:
        """Tenor"""
        return self.__floatingRateFrequency

    @floatingRateFrequency.setter
    def floatingRateFrequency(self, value: Union[str, str]):
        self.__floatingRateFrequency = value
        self._property_changed('floatingRateFrequency')        

    @property
    def floatingRateDayCountFraction(self) -> Union['DayCountFraction', str]:
        """Day Count Fraction."""
        return self.__floatingRateDayCountFraction

    @floatingRateDayCountFraction.setter
    def floatingRateDayCountFraction(self, value: Union['DayCountFraction', str]):
        self.__floatingRateDayCountFraction = value
        self._property_changed('floatingRateDayCountFraction')        

    @property
    def floatingRateBusinessDayConvention(self) -> Union['BusinessDayConvention', str]:
        """Business Day Convention."""
        return self.__floatingRateBusinessDayConvention

    @floatingRateBusinessDayConvention.setter
    def floatingRateBusinessDayConvention(self, value: Union['BusinessDayConvention', str]):
        self.__floatingRateBusinessDayConvention = value
        self._property_changed('floatingRateBusinessDayConvention')        

    @property
    def floorRate(self) -> Union['Strike', str]:
        """Strike as value, percent or at-the-money e.g. 62.5, 95%, ATM, ATMF"""
        return self.__floorRate

    @floorRate.setter
    def floorRate(self, value: Union['Strike', str]):
        self.__floorRate = value
        self._property_changed('floorRate')        


class IRCap(Instrument):
        
    """Object representation of an interest rate cap"""
       
    def __init__(self, terminationDate: Union['DateOrTenor', str], notionalCurrency: Union['Currency', str], notionalAmount: float = 1000000.0, effectiveDate: Union[datetime.date, str] = None, floatingRateOption: str = None, floatingRateDesignatedMaturity: Union[str, str] = None, floatingRateFrequency: Union[str, str] = None, floatingRateDayCountFraction: Union['DayCountFraction', str] = None, floatingRateBusinessDayConvention: Union['BusinessDayConvention', str] = None, capRate: Union['Strike', str] = None):
        super().__init__()
        self.__terminationDate = terminationDate
        self.__notionalCurrency = notionalCurrency
        self.__notionalAmount = notionalAmount
        self.__effectiveDate = effectiveDate
        self.__floatingRateOption = floatingRateOption
        self.__floatingRateDesignatedMaturity = floatingRateDesignatedMaturity
        self.__floatingRateFrequency = floatingRateFrequency
        self.__floatingRateDayCountFraction = floatingRateDayCountFraction
        self.__floatingRateBusinessDayConvention = floatingRateBusinessDayConvention
        self.__capRate = capRate

    @property
    def assetClass(self) -> str:
        """Rates"""
        return 'Rates'        

    @property
    def type(self) -> str:
        """Cap"""
        return 'Cap'        

    @property
    def terminationDate(self) -> Union['DateOrTenor', str]:
        """Date or tenor, e.g. 2018-09-03, 3m"""
        return self.__terminationDate

    @terminationDate.setter
    def terminationDate(self, value: Union['DateOrTenor', str]):
        self.__terminationDate = value
        self._property_changed('terminationDate')        

    @property
    def notionalCurrency(self) -> Union['Currency', str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__notionalCurrency

    @notionalCurrency.setter
    def notionalCurrency(self, value: Union['Currency', str]):
        self.__notionalCurrency = value
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
        """ISO 8601-formatted date"""
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
    def floatingRateDesignatedMaturity(self) -> Union[str, str]:
        """Tenor"""
        return self.__floatingRateDesignatedMaturity

    @floatingRateDesignatedMaturity.setter
    def floatingRateDesignatedMaturity(self, value: Union[str, str]):
        self.__floatingRateDesignatedMaturity = value
        self._property_changed('floatingRateDesignatedMaturity')        

    @property
    def floatingRateFrequency(self) -> Union[str, str]:
        """Tenor"""
        return self.__floatingRateFrequency

    @floatingRateFrequency.setter
    def floatingRateFrequency(self, value: Union[str, str]):
        self.__floatingRateFrequency = value
        self._property_changed('floatingRateFrequency')        

    @property
    def floatingRateDayCountFraction(self) -> Union['DayCountFraction', str]:
        """Day Count Fraction."""
        return self.__floatingRateDayCountFraction

    @floatingRateDayCountFraction.setter
    def floatingRateDayCountFraction(self, value: Union['DayCountFraction', str]):
        self.__floatingRateDayCountFraction = value
        self._property_changed('floatingRateDayCountFraction')        

    @property
    def floatingRateBusinessDayConvention(self) -> Union['BusinessDayConvention', str]:
        """Business Day Convention."""
        return self.__floatingRateBusinessDayConvention

    @floatingRateBusinessDayConvention.setter
    def floatingRateBusinessDayConvention(self, value: Union['BusinessDayConvention', str]):
        self.__floatingRateBusinessDayConvention = value
        self._property_changed('floatingRateBusinessDayConvention')        

    @property
    def capRate(self) -> Union['Strike', str]:
        """Strike as value, percent or at-the-money e.g. 62.5, 95%, ATM, ATMF"""
        return self.__capRate

    @capRate.setter
    def capRate(self, value: Union['Strike', str]):
        self.__capRate = value
        self._property_changed('capRate')        


class FXOption(Instrument):
        
    """Object representation of a FX option"""
       
    def __init__(self, callCurrency: Union['Currency', str], putCurrency: Union['Currency', str], strikePrice: Union['Strike', str], expirationDate: Union['DateOrTenor', str], optionType: Union['OptionType', str], callAmount: float = 1000000.0, putAmount: float = 1000000.0, premium: float = 0):
        super().__init__()
        self.__callCurrency = callCurrency
        self.__putCurrency = putCurrency
        self.__callAmount = callAmount
        self.__putAmount = putAmount
        self.__strikePrice = strikePrice
        self.__expirationDate = expirationDate
        self.__optionType = optionType
        self.__premium = premium

    @property
    def assetClass(self) -> str:
        """FX"""
        return 'FX'        

    @property
    def type(self) -> str:
        """Option"""
        return 'Option'        

    @property
    def callCurrency(self) -> Union['Currency', str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__callCurrency

    @callCurrency.setter
    def callCurrency(self, value: Union['Currency', str]):
        self.__callCurrency = value
        self._property_changed('callCurrency')        

    @property
    def putCurrency(self) -> Union['Currency', str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__putCurrency

    @putCurrency.setter
    def putCurrency(self, value: Union['Currency', str]):
        self.__putCurrency = value
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
    def strikePrice(self) -> Union['Strike', str]:
        """Strike as value, percent or at-the-money e.g. 62.5, 95%, ATM, ATMF"""
        return self.__strikePrice

    @strikePrice.setter
    def strikePrice(self, value: Union['Strike', str]):
        self.__strikePrice = value
        self._property_changed('strikePrice')        

    @property
    def expirationDate(self) -> Union['DateOrTenor', str]:
        """Date or tenor, e.g. 2018-09-03, 3m"""
        return self.__expirationDate

    @expirationDate.setter
    def expirationDate(self, value: Union['DateOrTenor', str]):
        self.__expirationDate = value
        self._property_changed('expirationDate')        

    @property
    def optionType(self) -> Union['OptionType', str]:
        return self.__optionType

    @optionType.setter
    def optionType(self, value: Union['OptionType', str]):
        self.__optionType = value
        self._property_changed('optionType')        

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
       
    def __init__(self, pair: str = None, settlementDate: Union['DateOrTenor', str] = None, forwardRate: float = None, notional: float = None):
        super().__init__()
        self.__pair = pair
        self.__settlementDate = settlementDate
        self.__forwardRate = forwardRate
        self.__notional = notional

    @property
    def assetClass(self) -> str:
        """FX"""
        return 'FX'        

    @property
    def type(self) -> str:
        """Forward"""
        return 'Forward'        

    @property
    def pair(self) -> str:
        """Currency pair"""
        return self.__pair

    @pair.setter
    def pair(self, value: str):
        self.__pair = value
        self._property_changed('pair')        

    @property
    def settlementDate(self) -> Union['DateOrTenor', str]:
        """Date or tenor, e.g. 2018-09-03, 3m"""
        return self.__settlementDate

    @settlementDate.setter
    def settlementDate(self, value: Union['DateOrTenor', str]):
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
    def notional(self) -> float:
        """Notional amount"""
        return self.__notional

    @notional.setter
    def notional(self, value: float):
        self.__notional = value
        self._property_changed('notional')        


class EqOption(Instrument):
        
    """Object representation of an equity option"""
       
    def __init__(self, asset: str, expirationDate: Union['DateOrTenor', str], strikePrice: Union['Strike', str], optionType: Union['OptionType', str], optionStyle: Union['OptionStyle', str], numberOfOptions: int = 1, exchange: Union[str, str] = None, multiplier: float = None, settlementDate: Union['DateOrTenor', str] = None, currency: Union['Currency', str] = None, premium: float = 0):
        super().__init__()
        self.__numberOfOptions = numberOfOptions
        self.__asset = asset
        self.__exchange = exchange
        self.__expirationDate = expirationDate
        self.__strikePrice = strikePrice
        self.__optionType = optionType
        self.__optionStyle = optionStyle
        self.__multiplier = multiplier
        self.__settlementDate = settlementDate
        self.__currency = currency
        self.__premium = premium

    @property
    def assetClass(self) -> str:
        """Equity"""
        return 'Equity'        

    @property
    def type(self) -> str:
        """Option"""
        return 'Option'        

    @property
    def numberOfOptions(self) -> int:
        """Number of options"""
        return self.__numberOfOptions

    @numberOfOptions.setter
    def numberOfOptions(self, value: int):
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
    def exchange(self) -> Union[str, str]:
        """Name of marketplace where security, derivative or other instrument is traded"""
        return self.__exchange

    @exchange.setter
    def exchange(self, value: Union[str, str]):
        self.__exchange = value
        self._property_changed('exchange')        

    @property
    def expirationDate(self) -> Union['DateOrTenor', str]:
        """Date or tenor, e.g. 2018-09-03, 3m"""
        return self.__expirationDate

    @expirationDate.setter
    def expirationDate(self, value: Union['DateOrTenor', str]):
        self.__expirationDate = value
        self._property_changed('expirationDate')        

    @property
    def strikePrice(self) -> Union['Strike', str]:
        """Strike as value, percent or at-the-money e.g. 62.5, 95%, ATM, ATMF"""
        return self.__strikePrice

    @strikePrice.setter
    def strikePrice(self, value: Union['Strike', str]):
        self.__strikePrice = value
        self._property_changed('strikePrice')        

    @property
    def optionType(self) -> Union['OptionType', str]:
        return self.__optionType

    @optionType.setter
    def optionType(self, value: Union['OptionType', str]):
        self.__optionType = value
        self._property_changed('optionType')        

    @property
    def optionStyle(self) -> Union['OptionStyle', str]:
        """Option Style"""
        return self.__optionStyle

    @optionStyle.setter
    def optionStyle(self, value: Union['OptionStyle', str]):
        self.__optionStyle = value
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
    def settlementDate(self) -> Union['DateOrTenor', str]:
        """Date or tenor, e.g. 2018-09-03, 3m"""
        return self.__settlementDate

    @settlementDate.setter
    def settlementDate(self, value: Union['DateOrTenor', str]):
        self.__settlementDate = value
        self._property_changed('settlementDate')        

    @property
    def currency(self) -> Union['Currency', str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union['Currency', str]):
        self.__currency = value
        self._property_changed('currency')        

    @property
    def premium(self) -> float:
        """Option premium"""
        return self.__premium

    @premium.setter
    def premium(self, value: float):
        self.__premium = value
        self._property_changed('premium')        


class EqForward(Instrument):
        
    """Object representation of an equity forward"""
       
    def __init__(self, asset: str, expirationDate: Union['DateOrTenor', str], forwardPrice: float, numberOfShares: int = 1):
        super().__init__()
        self.__asset = asset
        self.__numberOfShares = numberOfShares
        self.__expirationDate = expirationDate
        self.__forwardPrice = forwardPrice

    @property
    def assetClass(self) -> str:
        """Equity"""
        return 'Equity'        

    @property
    def type(self) -> str:
        """Forward"""
        return 'Forward'        

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
    def expirationDate(self) -> Union['DateOrTenor', str]:
        """Date or tenor, e.g. 2018-09-03, 3m"""
        return self.__expirationDate

    @expirationDate.setter
    def expirationDate(self, value: Union['DateOrTenor', str]):
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


class CommodSwap(Instrument):
        
    """Object representation of a commodities swap"""
       
    def __init__(self, commodity: Union['Commodities', str], start, commodityReferencePrice: str = None, notionalAmount: float = 1000000.0, currency: Union['Currency', str] = None, calculationPeriods: int = None, calculationPeriodFrequency: Union['Frequency', str] = None):
        super().__init__()
        self.__commodity = commodity
        self.__commodityReferencePrice = commodityReferencePrice
        self.__start = start
        self.__notionalAmount = notionalAmount
        self.__currency = currency
        self.__calculationPeriods = calculationPeriods
        self.__calculationPeriodFrequency = calculationPeriodFrequency

    @property
    def assetClass(self) -> str:
        """Commod"""
        return 'Commod'        

    @property
    def type(self) -> str:
        """Swap"""
        return 'Swap'        

    @property
    def commodity(self) -> Union['Commodities', str]:
        """Commodity asset"""
        return self.__commodity

    @commodity.setter
    def commodity(self, value: Union['Commodities', str]):
        self.__commodity = value
        self._property_changed('commodity')        

    @property
    def commodityReferencePrice(self) -> str:
        return self.__commodityReferencePrice

    @commodityReferencePrice.setter
    def commodityReferencePrice(self, value: str):
        self.__commodityReferencePrice = value
        self._property_changed('commodityReferencePrice')        

    @property
    def start(self):
        return self.__start

    @start.setter
    def start(self, value):
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
    def currency(self) -> Union['Currency', str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union['Currency', str]):
        self.__currency = value
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
    def calculationPeriodFrequency(self) -> Union['Frequency', str]:
        """The frequency of the calculation periods"""
        return self.__calculationPeriodFrequency

    @calculationPeriodFrequency.setter
    def calculationPeriodFrequency(self, value: Union['Frequency', str]):
        self.__calculationPeriodFrequency = value
        self._property_changed('calculationPeriodFrequency')        


class Forward(Instrument):
        
    """Object representation of a forward"""
       
    def __init__(self, currency: Union['Currency', str], expirationDate: Union['DateOrTenor', str]):
        super().__init__()
        self.__currency = currency
        self.__expirationDate = expirationDate

    @property
    def assetClass(self) -> str:
        """Cash"""
        return 'Cash'        

    @property
    def type(self) -> str:
        """Forward"""
        return 'Forward'        

    @property
    def currency(self) -> Union['Currency', str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union['Currency', str]):
        self.__currency = value
        self._property_changed('currency')        

    @property
    def expirationDate(self) -> Union['DateOrTenor', str]:
        """Date or tenor, e.g. 2018-09-03, 3m"""
        return self.__expirationDate

    @expirationDate.setter
    def expirationDate(self, value: Union['DateOrTenor', str]):
        self.__expirationDate = value
        self._property_changed('expirationDate')        
