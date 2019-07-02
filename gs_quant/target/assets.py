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
from gs_quant.base import Base, EnumBase, Instrument, get_enum_value
from gs_quant.target.common import *
from typing import Tuple, Union
import datetime


class AllocatorType(EnumBase, Enum):    
    
    """Allocator type defines the type of investor company managing an asset"""

    Advisor = 'Advisor'
    Consultant_Institutional = 'Consultant (Institutional)'
    Endowment = 'Endowment'
    Family_Office_Multi = 'Family Office (Multi)'
    Family_Office_Single = 'Family Office (Single)'
    Foundation = 'Foundation'
    Fund_of_Funds = 'Fund of Funds'
    Insurance_Company = 'Insurance Company'
    Outsourced_CIO = 'Outsourced CIO'
    Pension_Private = 'Pension (Private)'
    Pension_Public = 'Pension (Public)'
    Private_Bank = 'Private Bank'
    Prop_Capital_OVER_Commercial_Bank = 'Prop Capital/Commercial Bank'
    Sovereign_Wealth_Fund = 'Sovereign Wealth Fund'
    
    def __repr__(self):
        return self.value


class AssetStatsPeriod(EnumBase, Enum):    
    
    """The period used to produce date range."""

    _1y = '1y'
    _3y = '3y'
    _5y = '5y'
    _10y = '10y'
    
    def __repr__(self):
        return self.value


class AssetStatsType(EnumBase, Enum):    
    
    """Is it rolling, none etc."""

    Rolling = 'Rolling'
    Calendar = 'Calendar'
    
    def __repr__(self):
        return self.value


class CommodityFamily(EnumBase, Enum):    
    
    """Commodity Family"""

    Base_Metal = 'Base Metal'
    Gas = 'Gas'
    Oil = 'Oil'
    Oil_Products = 'Oil Products'
    
    def __repr__(self):
        return self.value


class CommoditySector(EnumBase, Enum):    
    
    """The sector of the commodity"""

    Base_metals = 'Base metals'
    Precious_metals = 'Precious metals'
    Energy = 'Energy'
    Agriculturals = 'Agriculturals'
    Power = 'Power'
    
    def __repr__(self):
        return self.value


class CommoditySubFamily(EnumBase, Enum):    
    
    """Commodity SubFamily"""

    Crude = 'Crude'
    Fuel = 'Fuel'
    Heat = 'Heat'
    NG = 'NG'
    
    def __repr__(self):
        return self.value


class NetExposureClassification(EnumBase, Enum):    
    
    """Classification for net exposure of fund."""

    Short_Only__OVER__Short_Bias = 'Short Only / Short Bias'
    Market_Neutral = 'Market Neutral'
    Low_Net = 'Low Net'
    Variable_Net = 'Variable Net'
    Long_Biased = 'Long Biased'
    Long_Only = 'Long Only'
    
    def __repr__(self):
        return self.value


class Strategy(EnumBase, Enum):    
    
    """More specific descriptor of a fund's investment approach. Same view permissions as the asset"""

    Active_Trading = 'Active Trading'
    Activist = 'Activist'
    Co_Invest__OVER__SPV = 'Co-Invest / SPV'
    Commodity = 'Commodity'
    Commodities = 'Commodities'
    Composite = 'Composite'
    Conservative = 'Conservative'
    Convert_Arb = 'Convert Arb'
    Convertible_Arbitrage = 'Convertible Arbitrage'
    Credit_Arbitrage = 'Credit Arbitrage'
    Cross_Capital_Structure = 'Cross-Capital-Structure'
    CTA__OVER__Managed_Futures = 'CTA / Managed Futures'
    Currency = 'Currency'
    Discretionary = 'Discretionary'
    Discretionary_Thematic = 'Discretionary Thematic'
    Distressed = 'Distressed'
    Distressed_Securities = 'Distressed Securities'
    Distressed_OVER_Restructuring = 'Distressed/Restructuring'
    Diversified = 'Diversified'
    Equity_Hedge = 'Equity Hedge'
    Equity_Market_Neutral = 'Equity Market Neutral'
    Equity_Only = 'Equity Only'
    Event_Driven = 'Event-Driven'
    Fixed_Income_Arb = 'Fixed Income Arb'
    Fixed_Income_Asset_Backed = 'Fixed Income-Asset Backed'
    Fixed_Income_Corporate = 'Fixed Income-Corporate'
    Fixed_Income_Sovereign = 'Fixed Income-Sovereign'
    Fundamental_Growth = 'Fundamental Growth'
    Fundamental_Value = 'Fundamental Value'
    General = 'General'
    General_Multi_Strategy = 'General Multi-Strategy'
    Generalist = 'Generalist'
    Hybrid__OVER__Illiquid = 'Hybrid / Illiquid'
    Long__OVER__Short = 'Long / Short'
    Macro = 'Macro'
    Market_Defensive = 'Market Defensive'
    Merger_Arb = 'Merger Arb'
    Merger_Arbitrage = 'Merger Arbitrage'
    Multi_Strategy = 'Multi-Strategy'
    Quantitative_Directional = 'Quantitative Directional'
    Relative_Value_Arbitrage = 'Relative Value Arbitrage'
    Risk_Premia = 'Risk Premia'
    Sector___Energy_OVER_Basic_Materials = 'Sector - Energy/Basic Materials'
    Sector___Healthcare = 'Sector - Healthcare'
    Sector___Technology = 'Sector - Technology'
    Sector___Technology_OVER_Healthcare = 'Sector - Technology/Healthcare'
    Sector_Specific = 'Sector-Specific'
    Short_Bias = 'Short Bias'
    Special_Situations = 'Special Situations'
    Stat_Arb = 'Stat Arb'
    Statistical_Arbitrage = 'Statistical Arbitrage'
    Strategic = 'Strategic'
    Structured = 'Structured'
    Systematic = 'Systematic'
    Systematic_Diversified = 'Systematic Diversified'
    Vol_Arb__OVER__Options = 'Vol Arb / Options'
    Volatility = 'Volatility'
    Volatility_Target_10 = 'Volatility Target 10'
    Volatility_Target_12 = 'Volatility Target 12'
    Volatility_Target_15 = 'Volatility Target 15'
    Yield_Alternative = 'Yield Alternative'
    
    def __repr__(self):
        return self.value


class SupraStrategy(EnumBase, Enum):    
    
    """Broad descriptor of a fund's investment approach. Same view permissions as the asset"""

    Composite = 'Composite'
    Credit = 'Credit'
    Equity = 'Equity'
    Equity_Hedge = 'Equity Hedge'
    Event_Driven = 'Event Driven'
    Fund_of_Funds = 'Fund of Funds'
    Macro = 'Macro'
    Multi_Strategy = 'Multi-Strategy'
    Other = 'Other'
    Quant = 'Quant'
    Relative_Value = 'Relative Value'
    Risk_Parity = 'Risk Parity'
    
    def __repr__(self):
        return self.value


class AssetClassifications(Base):
               
    def __init__(self, riskCountryName: str = None, riskCountryCode: str = None, countryName: str = None, countryCode: str = None, isPrimary: bool = None, gicsSector: str = None, gicsIndustryGroup: str = None, gicsIndustry: str = None, gicsSubIndustry: str = None, commodTemplate: str = None):
        super().__init__()
        self.__riskCountryName = riskCountryName
        self.__riskCountryCode = riskCountryCode
        self.__countryName = countryName
        self.__countryCode = countryCode
        self.__isPrimary = isPrimary
        self.__gicsSector = gicsSector
        self.__gicsIndustryGroup = gicsIndustryGroup
        self.__gicsIndustry = gicsIndustry
        self.__gicsSubIndustry = gicsSubIndustry
        self.__commodTemplate = commodTemplate

    @property
    def riskCountryName(self) -> str:
        """Risk Country"""
        return self.__riskCountryName

    @riskCountryName.setter
    def riskCountryName(self, value: str):
        self.__riskCountryName = value
        self._property_changed('riskCountryName')        

    @property
    def riskCountryCode(self) -> str:
        """Risk Country code (ISO 3166)."""
        return self.__riskCountryCode

    @riskCountryCode.setter
    def riskCountryCode(self, value: str):
        self.__riskCountryCode = value
        self._property_changed('riskCountryCode')        

    @property
    def countryName(self) -> str:
        """Country name of asset"""
        return self.__countryName

    @countryName.setter
    def countryName(self, value: str):
        self.__countryName = value
        self._property_changed('countryName')        

    @property
    def countryCode(self) -> str:
        """Country code (ISO 3166)"""
        return self.__countryCode

    @countryCode.setter
    def countryCode(self, value: str):
        self.__countryCode = value
        self._property_changed('countryCode')        

    @property
    def isPrimary(self) -> bool:
        """Is this the primary exchange listing for the asset"""
        return self.__isPrimary

    @isPrimary.setter
    def isPrimary(self, value: bool):
        self.__isPrimary = value
        self._property_changed('isPrimary')        

    @property
    def gicsSector(self) -> str:
        """GICS Sector classification (level 1)"""
        return self.__gicsSector

    @gicsSector.setter
    def gicsSector(self, value: str):
        self.__gicsSector = value
        self._property_changed('gicsSector')        

    @property
    def gicsIndustryGroup(self) -> str:
        """GICS Industry Group classification (level 2)"""
        return self.__gicsIndustryGroup

    @gicsIndustryGroup.setter
    def gicsIndustryGroup(self, value: str):
        self.__gicsIndustryGroup = value
        self._property_changed('gicsIndustryGroup')        

    @property
    def gicsIndustry(self) -> str:
        """GICS Industry classification (level 3)"""
        return self.__gicsIndustry

    @gicsIndustry.setter
    def gicsIndustry(self, value: str):
        self.__gicsIndustry = value
        self._property_changed('gicsIndustry')        

    @property
    def gicsSubIndustry(self) -> str:
        """GICS Sub Industry classification (level 4)"""
        return self.__gicsSubIndustry

    @gicsSubIndustry.setter
    def gicsSubIndustry(self, value: str):
        self.__gicsSubIndustry = value
        self._property_changed('gicsSubIndustry')        

    @property
    def commodTemplate(self) -> str:
        """Commodities generic template, i.e. Heating Oil"""
        return self.__commodTemplate

    @commodTemplate.setter
    def commodTemplate(self, value: str):
        self.__commodTemplate = value
        self._property_changed('commodTemplate')        


class AssetToInstrumentResponse(Base):
        
    """Resolution of assetId to instrument"""
       
    def __init__(self, assetId: str, name: str, instrument: Instrument, sizeField: str):
        super().__init__()
        self.__assetId = assetId
        self.__name = name
        self.__instrument = instrument
        self.__sizeField = sizeField

    @property
    def assetId(self) -> str:
        """Marquee unique asset identifier."""
        return self.__assetId

    @assetId.setter
    def assetId(self, value: str):
        self.__assetId = value
        self._property_changed('assetId')        

    @property
    def name(self) -> str:
        """Display name of the asset"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def instrument(self) -> Instrument:
        """Derivative instruments"""
        return self.__instrument

    @instrument.setter
    def instrument(self, value: Instrument):
        self.__instrument = value
        self._property_changed('instrument')        

    @property
    def sizeField(self) -> str:
        """Size field."""
        return self.__sizeField

    @sizeField.setter
    def sizeField(self, value: str):
        self.__sizeField = value
        self._property_changed('sizeField')        


class Benchmark(Base):
        
    """Reference rate that can based on an absolute value or absolute value + index"""
       
    def __init__(self, assetId: str = None, value: float = None):
        super().__init__()
        self.__assetId = assetId
        self.__value = value

    @property
    def assetId(self) -> str:
        """Asset for rate index"""
        return self.__assetId

    @assetId.setter
    def assetId(self, value: str):
        self.__assetId = value
        self._property_changed('assetId')        

    @property
    def value(self) -> float:
        """Absolute value for reference rate"""
        return self.__value

    @value.setter
    def value(self, value: float):
        self.__value = value
        self._property_changed('value')        


class NumberRange(Base):
        
    """lower and upper bound to define a number range"""
       
    def __init__(self, lowerBound: float = None, upperBound: float = None):
        super().__init__()
        self.__lowerBound = lowerBound
        self.__upperBound = upperBound

    @property
    def lowerBound(self) -> float:
        """value that defines the lower boundary of the range"""
        return self.__lowerBound

    @lowerBound.setter
    def lowerBound(self, value: float):
        self.__lowerBound = value
        self._property_changed('lowerBound')        

    @property
    def upperBound(self) -> float:
        """value that defines the upper boundary of the range"""
        return self.__upperBound

    @upperBound.setter
    def upperBound(self, value: float):
        self.__upperBound = value
        self._property_changed('upperBound')        


class People(Base):
        
    """People associated with an asset"""
       
    def __init__(self, portfolioManagers: Tuple[str, ...] = None):
        super().__init__()
        self.__portfolioManagers = portfolioManagers

    @property
    def portfolioManagers(self) -> Tuple[str, ...]:
        """Portfolio managers of asset"""
        return self.__portfolioManagers

    @portfolioManagers.setter
    def portfolioManagers(self, value: Tuple[str, ...]):
        self.__portfolioManagers = value
        self._property_changed('portfolioManagers')        


class PerformanceStatsRequest(Base):
        
    """Performance statistics."""
       
    def __init__(self, annualizedReturn: Op = None, annualizedVolatility: Op = None, bestMonth: Op = None, maxDrawDown: Op = None, maxDrawDownDuration: Op = None, positiveMonths: Op = None, sharpeRatio: Op = None, sortinoRatio: Op = None, worstMonth: Op = None, averageReturn: Op = None):
        super().__init__()
        self.__annualizedReturn = annualizedReturn
        self.__annualizedVolatility = annualizedVolatility
        self.__bestMonth = bestMonth
        self.__maxDrawDown = maxDrawDown
        self.__maxDrawDownDuration = maxDrawDownDuration
        self.__positiveMonths = positiveMonths
        self.__sharpeRatio = sharpeRatio
        self.__sortinoRatio = sortinoRatio
        self.__worstMonth = worstMonth
        self.__averageReturn = averageReturn

    @property
    def annualizedReturn(self) -> Op:
        """Operations for searches."""
        return self.__annualizedReturn

    @annualizedReturn.setter
    def annualizedReturn(self, value: Op):
        self.__annualizedReturn = value
        self._property_changed('annualizedReturn')        

    @property
    def annualizedVolatility(self) -> Op:
        """Operations for searches."""
        return self.__annualizedVolatility

    @annualizedVolatility.setter
    def annualizedVolatility(self, value: Op):
        self.__annualizedVolatility = value
        self._property_changed('annualizedVolatility')        

    @property
    def bestMonth(self) -> Op:
        """Operations for searches."""
        return self.__bestMonth

    @bestMonth.setter
    def bestMonth(self, value: Op):
        self.__bestMonth = value
        self._property_changed('bestMonth')        

    @property
    def maxDrawDown(self) -> Op:
        """Operations for searches."""
        return self.__maxDrawDown

    @maxDrawDown.setter
    def maxDrawDown(self, value: Op):
        self.__maxDrawDown = value
        self._property_changed('maxDrawDown')        

    @property
    def maxDrawDownDuration(self) -> Op:
        """Operations for searches."""
        return self.__maxDrawDownDuration

    @maxDrawDownDuration.setter
    def maxDrawDownDuration(self, value: Op):
        self.__maxDrawDownDuration = value
        self._property_changed('maxDrawDownDuration')        

    @property
    def positiveMonths(self) -> Op:
        """Operations for searches."""
        return self.__positiveMonths

    @positiveMonths.setter
    def positiveMonths(self, value: Op):
        self.__positiveMonths = value
        self._property_changed('positiveMonths')        

    @property
    def sharpeRatio(self) -> Op:
        """Operations for searches."""
        return self.__sharpeRatio

    @sharpeRatio.setter
    def sharpeRatio(self, value: Op):
        self.__sharpeRatio = value
        self._property_changed('sharpeRatio')        

    @property
    def sortinoRatio(self) -> Op:
        """Operations for searches."""
        return self.__sortinoRatio

    @sortinoRatio.setter
    def sortinoRatio(self, value: Op):
        self.__sortinoRatio = value
        self._property_changed('sortinoRatio')        

    @property
    def worstMonth(self) -> Op:
        """Operations for searches."""
        return self.__worstMonth

    @worstMonth.setter
    def worstMonth(self, value: Op):
        self.__worstMonth = value
        self._property_changed('worstMonth')        

    @property
    def averageReturn(self) -> Op:
        """Operations for searches."""
        return self.__averageReturn

    @averageReturn.setter
    def averageReturn(self, value: Op):
        self.__averageReturn = value
        self._property_changed('averageReturn')        


class SecuritiesLendingLoan(Base):
        
    """Parameters specific to a securities lending loan"""
       
    def __init__(self, assetId: str, fundId: str, lenderId: str, borrowerId: str, loanStatus: str = None, settlementStatus: str = None, collateralType: str = None, loanCurrency: Union[Currency, str] = None, adjustmentInd: bool = None, countryOfIssue: str = None, inputDate: datetime.date = None, effectiveDate: datetime.date = None, securitySettleDate: datetime.date = None, cashSettleDate: datetime.date = None, termDate: datetime.date = None, returnDate: datetime.date = None):
        super().__init__()
        self.__assetId = assetId
        self.__fundId = fundId
        self.__lenderId = lenderId
        self.__borrowerId = borrowerId
        self.__loanStatus = loanStatus
        self.__settlementStatus = settlementStatus
        self.__collateralType = collateralType
        self.__loanCurrency = loanCurrency if isinstance(loanCurrency, Currency) else get_enum_value(Currency, loanCurrency)
        self.__adjustmentInd = adjustmentInd
        self.__countryOfIssue = countryOfIssue
        self.__inputDate = inputDate
        self.__effectiveDate = effectiveDate
        self.__securitySettleDate = securitySettleDate
        self.__cashSettleDate = cashSettleDate
        self.__termDate = termDate
        self.__returnDate = returnDate

    @property
    def assetId(self) -> str:
        """Id of the security being lent as part of this loan.  This Id should tie to an Asset"""
        return self.__assetId

    @assetId.setter
    def assetId(self, value: str):
        self.__assetId = value
        self._property_changed('assetId')        

    @property
    def fundId(self) -> str:
        """Id of the fund from which the loan is booked.  This Id should tie to an Asset"""
        return self.__fundId

    @fundId.setter
    def fundId(self, value: str):
        self.__fundId = value
        self._property_changed('fundId')        

    @property
    def lenderId(self) -> str:
        """Id of the counterpart lending the security.  This Id should tie to a Company"""
        return self.__lenderId

    @lenderId.setter
    def lenderId(self, value: str):
        self.__lenderId = value
        self._property_changed('lenderId')        

    @property
    def borrowerId(self) -> str:
        """Id of the counterpart borrowing the security.  This Id should tie to a Company"""
        return self.__borrowerId

    @borrowerId.setter
    def borrowerId(self, value: str):
        self.__borrowerId = value
        self._property_changed('borrowerId')        

    @property
    def loanStatus(self) -> str:
        """The current state of the loan"""
        return self.__loanStatus

    @loanStatus.setter
    def loanStatus(self, value: str):
        self.__loanStatus = value
        self._property_changed('loanStatus')        

    @property
    def settlementStatus(self) -> str:
        """State of the underlying components of the loan."""
        return self.__settlementStatus

    @settlementStatus.setter
    def settlementStatus(self, value: str):
        self.__settlementStatus = value
        self._property_changed('settlementStatus')        

    @property
    def collateralType(self) -> str:
        """Type of collateral used to collateralize the loan"""
        return self.__collateralType

    @collateralType.setter
    def collateralType(self, value: str):
        self.__collateralType = value
        self._property_changed('collateralType')        

    @property
    def loanCurrency(self) -> Union[Currency, str]:
        """Currency in which the loan value is represented"""
        return self.__loanCurrency

    @loanCurrency.setter
    def loanCurrency(self, value: Union[Currency, str]):
        self.__loanCurrency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('loanCurrency')        

    @property
    def adjustmentInd(self) -> bool:
        """Defines whether or not this contract is for the purpose of a month end loan adjustment."""
        return self.__adjustmentInd

    @adjustmentInd.setter
    def adjustmentInd(self, value: bool):
        self.__adjustmentInd = value
        self._property_changed('adjustmentInd')        

    @property
    def countryOfIssue(self) -> str:
        """The country code (ISO 3166) of the underlying security"""
        return self.__countryOfIssue

    @countryOfIssue.setter
    def countryOfIssue(self, value: str):
        self.__countryOfIssue = value
        self._property_changed('countryOfIssue')        

    @property
    def inputDate(self) -> datetime.date:
        """Date that the loan is booked"""
        return self.__inputDate

    @inputDate.setter
    def inputDate(self, value: datetime.date):
        self.__inputDate = value
        self._property_changed('inputDate')        

    @property
    def effectiveDate(self) -> datetime.date:
        """Date of the trade"""
        return self.__effectiveDate

    @effectiveDate.setter
    def effectiveDate(self, value: datetime.date):
        self.__effectiveDate = value
        self._property_changed('effectiveDate')        

    @property
    def securitySettleDate(self) -> datetime.date:
        """Date that the loaned securities settled"""
        return self.__securitySettleDate

    @securitySettleDate.setter
    def securitySettleDate(self, value: datetime.date):
        self.__securitySettleDate = value
        self._property_changed('securitySettleDate')        

    @property
    def cashSettleDate(self) -> datetime.date:
        """Date of the cash collateral settled"""
        return self.__cashSettleDate

    @cashSettleDate.setter
    def cashSettleDate(self, value: datetime.date):
        self.__cashSettleDate = value
        self._property_changed('cashSettleDate')        

    @property
    def termDate(self) -> datetime.date:
        """Date the dividend is paid for dividend based loans"""
        return self.__termDate

    @termDate.setter
    def termDate(self, value: datetime.date):
        self.__termDate = value
        self._property_changed('termDate')        

    @property
    def returnDate(self) -> datetime.date:
        """Date the loan is returned"""
        return self.__returnDate

    @returnDate.setter
    def returnDate(self, value: datetime.date):
        self.__returnDate = value
        self._property_changed('returnDate')        


class SocialDomain(Base):
               
    def __init__(self, onboarded: dict):
        super().__init__()
        self.__onboarded = onboarded

    @property
    def onboarded(self) -> dict:
        return self.__onboarded

    @onboarded.setter
    def onboarded(self, value: dict):
        self.__onboarded = value
        self._property_changed('onboarded')        


class TemporalXRef(Base):
               
    def __init__(self, startDate: datetime.date = None, endDate: datetime.date = None, identifiers: XRef = None):
        super().__init__()
        self.__startDate = startDate
        self.__endDate = endDate
        self.__identifiers = identifiers

    @property
    def startDate(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__startDate

    @startDate.setter
    def startDate(self, value: datetime.date):
        self.__startDate = value
        self._property_changed('startDate')        

    @property
    def endDate(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__endDate

    @endDate.setter
    def endDate(self, value: datetime.date):
        self.__endDate = value
        self._property_changed('endDate')        

    @property
    def identifiers(self) -> XRef:
        return self.__identifiers

    @identifiers.setter
    def identifiers(self, value: XRef):
        self.__identifiers = value
        self._property_changed('identifiers')        


class AssetParameters(Base):
        
    """Parameters specific to the asset type"""
       
    def __init__(self, basketType: str = None, style: str = None, indexCalculationType: str = None, indexReturnType: str = None, indexDivisor: float = None, currency: Union[Currency, str] = None, quoteCurrency: Union[Currency, str] = None, indexInitialPrice: float = None, initialPricingDate: datetime.date = None, expirationDate: datetime.date = None, expirationLocation: str = None, optionStyle: str = None, optionType: Union[OptionType, str] = None, settlementDate: datetime.date = None, settlementType: str = None, strikePrice: float = None, putCurrency: Union[Currency, str] = None, putAmount: float = None, automaticExercise: bool = None, callAmount: float = None, callCurrency: Union[Currency, str] = None, exerciseTime: str = None, multiplier: float = None, premiumPaymentDate: datetime.date = None, premium: float = None, premiumCurrency: Union[Currency, str] = None, callable: bool = None, puttable: bool = None, perpetual: bool = None, seniority: str = None, couponType: str = None, index: str = None, indexTerm: str = None, indexMargin: float = None, coupon: float = None, issueDate: datetime.date = None, issuer: str = None, issuerCountryCode: str = None, issuerType: str = None, issueSize: float = None, commoditySector: Union[CommoditySector, str] = None, pricingLocation: Union[PricingLocation, str] = None, contractMonths: Tuple[str, ...] = None, g10Currency: bool = None, hedgeId: str = None, ultimateTicker: str = None, strategy: Union[Strategy, str] = None, supraStrategy: Union[SupraStrategy, str] = None, exchangeCurrency: Union[Currency, str] = None, region: str = None, deliveryPoint: str = None, pricingIndex: str = None, contractMonth: str = None, loadType: str = None, contractUnit: str = None, indexCreateSource: Union[IndexCreateSource, str] = None, indexApprovalIds: Tuple[str, ...] = None, isPairBasket: bool = None, fixedRateDayCountFraction: Union[DayCountFraction, str] = None, floatingRateDayCountFraction: Union[DayCountFraction, str] = None, payDayCountFraction: Union[DayCountFraction, str] = None, receiveDayCountFraction: Union[DayCountFraction, str] = None, payFrequency: str = None, receiveFrequency: str = None, resettableLeg: Union[PayReceive, str] = None, inflationLag: str = None, fxIndex: str = None, tradeAs: str = None, cloneParentId: str = None, onBehalfOf: str = None, indexCalculationAgent: str = None):
        super().__init__()
        self.__basketType = basketType
        self.__style = style
        self.__indexCalculationType = indexCalculationType
        self.__indexReturnType = indexReturnType
        self.__indexDivisor = indexDivisor
        self.__currency = currency if isinstance(currency, Currency) else get_enum_value(Currency, currency)
        self.__quoteCurrency = quoteCurrency if isinstance(quoteCurrency, Currency) else get_enum_value(Currency, quoteCurrency)
        self.__indexInitialPrice = indexInitialPrice
        self.__initialPricingDate = initialPricingDate
        self.__expirationDate = expirationDate
        self.__expirationLocation = expirationLocation
        self.__optionStyle = optionStyle
        self.__optionType = optionType if isinstance(optionType, OptionType) else get_enum_value(OptionType, optionType)
        self.__settlementDate = settlementDate
        self.__settlementType = settlementType
        self.__strikePrice = strikePrice
        self.__putCurrency = putCurrency if isinstance(putCurrency, Currency) else get_enum_value(Currency, putCurrency)
        self.__putAmount = putAmount
        self.__automaticExercise = automaticExercise
        self.__callAmount = callAmount
        self.__callCurrency = callCurrency if isinstance(callCurrency, Currency) else get_enum_value(Currency, callCurrency)
        self.__exerciseTime = exerciseTime
        self.__multiplier = multiplier
        self.__premiumPaymentDate = premiumPaymentDate
        self.__premium = premium
        self.__premiumCurrency = premiumCurrency if isinstance(premiumCurrency, Currency) else get_enum_value(Currency, premiumCurrency)
        self.__callable = callable
        self.__puttable = puttable
        self.__perpetual = perpetual
        self.__seniority = seniority
        self.__couponType = couponType
        self.__index = index
        self.__indexTerm = indexTerm
        self.__indexMargin = indexMargin
        self.__coupon = coupon
        self.__issueDate = issueDate
        self.__issuer = issuer
        self.__issuerCountryCode = issuerCountryCode
        self.__issuerType = issuerType
        self.__issueSize = issueSize
        self.__commoditySector = commoditySector if isinstance(commoditySector, CommoditySector) else get_enum_value(CommoditySector, commoditySector)
        self.__pricingLocation = pricingLocation if isinstance(pricingLocation, PricingLocation) else get_enum_value(PricingLocation, pricingLocation)
        self.__contractMonths = contractMonths
        self.__g10Currency = g10Currency
        self.__hedgeId = hedgeId
        self.__ultimateTicker = ultimateTicker
        self.__strategy = strategy if isinstance(strategy, Strategy) else get_enum_value(Strategy, strategy)
        self.__supraStrategy = supraStrategy if isinstance(supraStrategy, SupraStrategy) else get_enum_value(SupraStrategy, supraStrategy)
        self.__exchangeCurrency = exchangeCurrency if isinstance(exchangeCurrency, Currency) else get_enum_value(Currency, exchangeCurrency)
        self.__region = region
        self.__deliveryPoint = deliveryPoint
        self.__pricingIndex = pricingIndex
        self.__contractMonth = contractMonth
        self.__loadType = loadType
        self.__contractUnit = contractUnit
        self.__indexCreateSource = indexCreateSource if isinstance(indexCreateSource, IndexCreateSource) else get_enum_value(IndexCreateSource, indexCreateSource)
        self.__indexApprovalIds = indexApprovalIds
        self.__isPairBasket = isPairBasket
        self.__fixedRateDayCountFraction = fixedRateDayCountFraction if isinstance(fixedRateDayCountFraction, DayCountFraction) else get_enum_value(DayCountFraction, fixedRateDayCountFraction)
        self.__floatingRateDayCountFraction = floatingRateDayCountFraction if isinstance(floatingRateDayCountFraction, DayCountFraction) else get_enum_value(DayCountFraction, floatingRateDayCountFraction)
        self.__payDayCountFraction = payDayCountFraction if isinstance(payDayCountFraction, DayCountFraction) else get_enum_value(DayCountFraction, payDayCountFraction)
        self.__receiveDayCountFraction = receiveDayCountFraction if isinstance(receiveDayCountFraction, DayCountFraction) else get_enum_value(DayCountFraction, receiveDayCountFraction)
        self.__payFrequency = payFrequency
        self.__receiveFrequency = receiveFrequency
        self.__resettableLeg = resettableLeg if isinstance(resettableLeg, PayReceive) else get_enum_value(PayReceive, resettableLeg)
        self.__inflationLag = inflationLag
        self.__fxIndex = fxIndex
        self.__tradeAs = tradeAs
        self.__cloneParentId = cloneParentId
        self.__onBehalfOf = onBehalfOf
        self.__indexCalculationAgent = indexCalculationAgent

    @property
    def basketType(self) -> str:
        """Type of basket / implementation"""
        return self.__basketType

    @basketType.setter
    def basketType(self, value: str):
        self.__basketType = value
        self._property_changed('basketType')        

    @property
    def style(self) -> str:
        """Asset style"""
        return self.__style

    @style.setter
    def style(self, value: str):
        self.__style = value
        self._property_changed('style')        

    @property
    def attributionDatasetId(self) -> str:
        """Identifier of dataset which provides performance attribution data"""
        return 'STSATTR'        

    @property
    def indexCalculationType(self) -> str:
        """Determines the index calculation methodology with respect to dividend reinvestment"""
        return self.__indexCalculationType

    @indexCalculationType.setter
    def indexCalculationType(self, value: str):
        self.__indexCalculationType = value
        self._property_changed('indexCalculationType')        

    @property
    def indexReturnType(self) -> str:
        """Determines the return calculation type method with respect to cash accrual / funding"""
        return self.__indexReturnType

    @indexReturnType.setter
    def indexReturnType(self, value: str):
        self.__indexReturnType = value
        self._property_changed('indexReturnType')        

    @property
    def indexDivisor(self) -> float:
        """Divisor to be applied to the overall position set of the index"""
        return self.__indexDivisor

    @indexDivisor.setter
    def indexDivisor(self, value: float):
        self.__indexDivisor = value
        self._property_changed('indexDivisor')        

    @property
    def currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self.__currency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('currency')        

    @property
    def quoteCurrency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__quoteCurrency

    @quoteCurrency.setter
    def quoteCurrency(self, value: Union[Currency, str]):
        self.__quoteCurrency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('quoteCurrency')        

    @property
    def indexInitialPrice(self) -> float:
        """Initial Price for the Index"""
        return self.__indexInitialPrice

    @indexInitialPrice.setter
    def indexInitialPrice(self, value: float):
        self.__indexInitialPrice = value
        self._property_changed('indexInitialPrice')        

    @property
    def initialPricingDate(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__initialPricingDate

    @initialPricingDate.setter
    def initialPricingDate(self, value: datetime.date):
        self.__initialPricingDate = value
        self._property_changed('initialPricingDate')        

    @property
    def expirationDate(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__expirationDate

    @expirationDate.setter
    def expirationDate(self, value: datetime.date):
        self.__expirationDate = value
        self._property_changed('expirationDate')        

    @property
    def expirationLocation(self) -> str:
        return self.__expirationLocation

    @expirationLocation.setter
    def expirationLocation(self, value: str):
        self.__expirationLocation = value
        self._property_changed('expirationLocation')        

    @property
    def optionStyle(self) -> str:
        return self.__optionStyle

    @optionStyle.setter
    def optionStyle(self, value: str):
        self.__optionStyle = value
        self._property_changed('optionStyle')        

    @property
    def optionType(self) -> Union[OptionType, str]:
        return self.__optionType

    @optionType.setter
    def optionType(self, value: Union[OptionType, str]):
        self.__optionType = value if isinstance(value, OptionType) else get_enum_value(OptionType, value)
        self._property_changed('optionType')        

    @property
    def settlementDate(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__settlementDate

    @settlementDate.setter
    def settlementDate(self, value: datetime.date):
        self.__settlementDate = value
        self._property_changed('settlementDate')        

    @property
    def settlementType(self) -> str:
        return self.__settlementType

    @settlementType.setter
    def settlementType(self, value: str):
        self.__settlementType = value
        self._property_changed('settlementType')        

    @property
    def strikePrice(self) -> float:
        return self.__strikePrice

    @strikePrice.setter
    def strikePrice(self, value: float):
        self.__strikePrice = value
        self._property_changed('strikePrice')        

    @property
    def putCurrency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__putCurrency

    @putCurrency.setter
    def putCurrency(self, value: Union[Currency, str]):
        self.__putCurrency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('putCurrency')        

    @property
    def putAmount(self) -> float:
        return self.__putAmount

    @putAmount.setter
    def putAmount(self, value: float):
        self.__putAmount = value
        self._property_changed('putAmount')        

    @property
    def automaticExercise(self) -> bool:
        return self.__automaticExercise

    @automaticExercise.setter
    def automaticExercise(self, value: bool):
        self.__automaticExercise = value
        self._property_changed('automaticExercise')        

    @property
    def callAmount(self) -> float:
        return self.__callAmount

    @callAmount.setter
    def callAmount(self, value: float):
        self.__callAmount = value
        self._property_changed('callAmount')        

    @property
    def callCurrency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__callCurrency

    @callCurrency.setter
    def callCurrency(self, value: Union[Currency, str]):
        self.__callCurrency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('callCurrency')        

    @property
    def exerciseTime(self) -> str:
        """Time at which the asset can be exercised"""
        return self.__exerciseTime

    @exerciseTime.setter
    def exerciseTime(self, value: str):
        self.__exerciseTime = value
        self._property_changed('exerciseTime')        

    @property
    def multiplier(self) -> float:
        """Underlying unit per asset multiplier"""
        return self.__multiplier

    @multiplier.setter
    def multiplier(self, value: float):
        self.__multiplier = value
        self._property_changed('multiplier')        

    @property
    def premiumPaymentDate(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__premiumPaymentDate

    @premiumPaymentDate.setter
    def premiumPaymentDate(self, value: datetime.date):
        self.__premiumPaymentDate = value
        self._property_changed('premiumPaymentDate')        

    @property
    def premium(self) -> float:
        return self.__premium

    @premium.setter
    def premium(self, value: float):
        self.__premium = value
        self._property_changed('premium')        

    @property
    def premiumCurrency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__premiumCurrency

    @premiumCurrency.setter
    def premiumCurrency(self, value: Union[Currency, str]):
        self.__premiumCurrency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('premiumCurrency')        

    @property
    def callable(self) -> bool:
        """Bond is callable"""
        return self.__callable

    @callable.setter
    def callable(self, value: bool):
        self.__callable = value
        self._property_changed('callable')        

    @property
    def puttable(self) -> bool:
        """Bond is puttable"""
        return self.__puttable

    @puttable.setter
    def puttable(self, value: bool):
        self.__puttable = value
        self._property_changed('puttable')        

    @property
    def perpetual(self) -> bool:
        """Bond is a perpetual"""
        return self.__perpetual

    @perpetual.setter
    def perpetual(self, value: bool):
        self.__perpetual = value
        self._property_changed('perpetual')        

    @property
    def seniority(self) -> str:
        """The seniority of the bond"""
        return self.__seniority

    @seniority.setter
    def seniority(self, value: str):
        self.__seniority = value
        self._property_changed('seniority')        

    @property
    def couponType(self) -> str:
        """The coupon type of the bond"""
        return self.__couponType

    @couponType.setter
    def couponType(self, value: str):
        self.__couponType = value
        self._property_changed('couponType')        

    @property
    def index(self) -> str:
        """The rate index (e.g. USD-LIBOR-BBA) for the floating rate coupon of this bond"""
        return self.__index

    @index.setter
    def index(self, value: str):
        self.__index = value
        self._property_changed('index')        

    @property
    def indexTerm(self) -> str:
        """The term of rate index (e.g. USD-LIBOR-BBA) for the floating rate coupon of this bond"""
        return self.__indexTerm

    @indexTerm.setter
    def indexTerm(self, value: str):
        self.__indexTerm = value
        self._property_changed('indexTerm')        

    @property
    def indexMargin(self) -> float:
        """The spread over the rate index (e.g. USD-LIBOR-BBA) for the floating rate coupon of this bond"""
        return self.__indexMargin

    @indexMargin.setter
    def indexMargin(self, value: float):
        self.__indexMargin = value
        self._property_changed('indexMargin')        

    @property
    def coupon(self) -> float:
        """The fixed coupon for this bond"""
        return self.__coupon

    @coupon.setter
    def coupon(self, value: float):
        self.__coupon = value
        self._property_changed('coupon')        

    @property
    def issueDate(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__issueDate

    @issueDate.setter
    def issueDate(self, value: datetime.date):
        self.__issueDate = value
        self._property_changed('issueDate')        

    @property
    def issuer(self) -> str:
        """The issuer of this bond"""
        return self.__issuer

    @issuer.setter
    def issuer(self, value: str):
        self.__issuer = value
        self._property_changed('issuer')        

    @property
    def issuerCountryCode(self) -> str:
        """The country code (ISO 3166) in which this bond was issued"""
        return self.__issuerCountryCode

    @issuerCountryCode.setter
    def issuerCountryCode(self, value: str):
        self.__issuerCountryCode = value
        self._property_changed('issuerCountryCode')        

    @property
    def issuerType(self) -> str:
        """The type of the bond issuer"""
        return self.__issuerType

    @issuerType.setter
    def issuerType(self, value: str):
        self.__issuerType = value
        self._property_changed('issuerType')        

    @property
    def issueSize(self) -> float:
        """The notional issue size of the bond"""
        return self.__issueSize

    @issueSize.setter
    def issueSize(self, value: float):
        self.__issueSize = value
        self._property_changed('issueSize')        

    @property
    def commoditySector(self) -> Union[CommoditySector, str]:
        """The sector of the commodity"""
        return self.__commoditySector

    @commoditySector.setter
    def commoditySector(self, value: Union[CommoditySector, str]):
        self.__commoditySector = value if isinstance(value, CommoditySector) else get_enum_value(CommoditySector, value)
        self._property_changed('commoditySector')        

    @property
    def pricingLocation(self) -> Union[PricingLocation, str]:
        """Based on the location of the exchange. Called 'Native Region' in SecDB"""
        return self.__pricingLocation

    @pricingLocation.setter
    def pricingLocation(self, value: Union[PricingLocation, str]):
        self.__pricingLocation = value if isinstance(value, PricingLocation) else get_enum_value(PricingLocation, value)
        self._property_changed('pricingLocation')        

    @property
    def contractMonths(self) -> Tuple[str, ...]:
        """Contract months"""
        return self.__contractMonths

    @contractMonths.setter
    def contractMonths(self, value: Tuple[str, ...]):
        self.__contractMonths = value
        self._property_changed('contractMonths')        

    @property
    def g10Currency(self) -> bool:
        """Is a G10 asset."""
        return self.__g10Currency

    @g10Currency.setter
    def g10Currency(self, value: bool):
        self.__g10Currency = value
        self._property_changed('g10Currency')        

    @property
    def hedgeId(self) -> str:
        """Marquee unique identifier"""
        return self.__hedgeId

    @hedgeId.setter
    def hedgeId(self, value: str):
        self.__hedgeId = value
        self._property_changed('hedgeId')        

    @property
    def ultimateTicker(self) -> str:
        """The ultimate ticker for this security (e.g. SPXW)"""
        return self.__ultimateTicker

    @ultimateTicker.setter
    def ultimateTicker(self, value: str):
        self.__ultimateTicker = value
        self._property_changed('ultimateTicker')        

    @property
    def strategy(self) -> Union[Strategy, str]:
        """More specific descriptor of a fund's investment approach. Same view permissions as the asset"""
        return self.__strategy

    @strategy.setter
    def strategy(self, value: Union[Strategy, str]):
        self.__strategy = value if isinstance(value, Strategy) else get_enum_value(Strategy, value)
        self._property_changed('strategy')        

    @property
    def supraStrategy(self) -> Union[SupraStrategy, str]:
        """Broad descriptor of a fund's investment approach. Same view permissions as the asset"""
        return self.__supraStrategy

    @supraStrategy.setter
    def supraStrategy(self, value: Union[SupraStrategy, str]):
        self.__supraStrategy = value if isinstance(value, SupraStrategy) else get_enum_value(SupraStrategy, value)
        self._property_changed('supraStrategy')        

    @property
    def exchangeCurrency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__exchangeCurrency

    @exchangeCurrency.setter
    def exchangeCurrency(self, value: Union[Currency, str]):
        self.__exchangeCurrency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('exchangeCurrency')        

    @property
    def region(self) -> str:
        return self.__region

    @region.setter
    def region(self, value: str):
        self.__region = value
        self._property_changed('region')        

    @property
    def deliveryPoint(self) -> str:
        return self.__deliveryPoint

    @deliveryPoint.setter
    def deliveryPoint(self, value: str):
        self.__deliveryPoint = value
        self._property_changed('deliveryPoint')        

    @property
    def pricingIndex(self) -> str:
        return self.__pricingIndex

    @pricingIndex.setter
    def pricingIndex(self, value: str):
        self.__pricingIndex = value
        self._property_changed('pricingIndex')        

    @property
    def contractMonth(self) -> str:
        return self.__contractMonth

    @contractMonth.setter
    def contractMonth(self, value: str):
        self.__contractMonth = value
        self._property_changed('contractMonth')        

    @property
    def loadType(self) -> str:
        return self.__loadType

    @loadType.setter
    def loadType(self, value: str):
        self.__loadType = value
        self._property_changed('loadType')        

    @property
    def contractUnit(self) -> str:
        return self.__contractUnit

    @contractUnit.setter
    def contractUnit(self, value: str):
        self.__contractUnit = value
        self._property_changed('contractUnit')        

    @property
    def indexCreateSource(self) -> Union[IndexCreateSource, str]:
        """Source of basket create"""
        return self.__indexCreateSource

    @indexCreateSource.setter
    def indexCreateSource(self, value: Union[IndexCreateSource, str]):
        self.__indexCreateSource = value if isinstance(value, IndexCreateSource) else get_enum_value(IndexCreateSource, value)
        self._property_changed('indexCreateSource')        

    @property
    def indexApprovalIds(self) -> Tuple[str, ...]:
        """Array of approval identifiers related to the object"""
        return self.__indexApprovalIds

    @indexApprovalIds.setter
    def indexApprovalIds(self, value: Tuple[str, ...]):
        self.__indexApprovalIds = value
        self._property_changed('indexApprovalIds')        

    @property
    def isPairBasket(self) -> bool:
        return self.__isPairBasket

    @isPairBasket.setter
    def isPairBasket(self, value: bool):
        self.__isPairBasket = value
        self._property_changed('isPairBasket')        

    @property
    def fixedRateDayCountFraction(self) -> Union[DayCountFraction, str]:
        """Default day count fraction for fixed legs"""
        return self.__fixedRateDayCountFraction

    @fixedRateDayCountFraction.setter
    def fixedRateDayCountFraction(self, value: Union[DayCountFraction, str]):
        self.__fixedRateDayCountFraction = value if isinstance(value, DayCountFraction) else get_enum_value(DayCountFraction, value)
        self._property_changed('fixedRateDayCountFraction')        

    @property
    def floatingRateDayCountFraction(self) -> Union[DayCountFraction, str]:
        """Default day count fraction for floating legs"""
        return self.__floatingRateDayCountFraction

    @floatingRateDayCountFraction.setter
    def floatingRateDayCountFraction(self, value: Union[DayCountFraction, str]):
        self.__floatingRateDayCountFraction = value if isinstance(value, DayCountFraction) else get_enum_value(DayCountFraction, value)
        self._property_changed('floatingRateDayCountFraction')        

    @property
    def payDayCountFraction(self) -> Union[DayCountFraction, str]:
        """Default day count fraction for pay leg"""
        return self.__payDayCountFraction

    @payDayCountFraction.setter
    def payDayCountFraction(self, value: Union[DayCountFraction, str]):
        self.__payDayCountFraction = value if isinstance(value, DayCountFraction) else get_enum_value(DayCountFraction, value)
        self._property_changed('payDayCountFraction')        

    @property
    def receiveDayCountFraction(self) -> Union[DayCountFraction, str]:
        """Default day count fraction for the receive leg"""
        return self.__receiveDayCountFraction

    @receiveDayCountFraction.setter
    def receiveDayCountFraction(self, value: Union[DayCountFraction, str]):
        self.__receiveDayCountFraction = value if isinstance(value, DayCountFraction) else get_enum_value(DayCountFraction, value)
        self._property_changed('receiveDayCountFraction')        

    @property
    def payFrequency(self) -> str:
        """Default frequency of the pay leg"""
        return self.__payFrequency

    @payFrequency.setter
    def payFrequency(self, value: str):
        self.__payFrequency = value
        self._property_changed('payFrequency')        

    @property
    def receiveFrequency(self) -> str:
        """Default frequency of the receive leg"""
        return self.__receiveFrequency

    @receiveFrequency.setter
    def receiveFrequency(self, value: str):
        self.__receiveFrequency = value
        self._property_changed('receiveFrequency')        

    @property
    def resettableLeg(self) -> Union[PayReceive, str]:
        """Resettable leg"""
        return self.__resettableLeg

    @resettableLeg.setter
    def resettableLeg(self, value: Union[PayReceive, str]):
        self.__resettableLeg = value if isinstance(value, PayReceive) else get_enum_value(PayReceive, value)
        self._property_changed('resettableLeg')        

    @property
    def inflationLag(self) -> str:
        """Inflation lag"""
        return self.__inflationLag

    @inflationLag.setter
    def inflationLag(self, value: str):
        self.__inflationLag = value
        self._property_changed('inflationLag')        

    @property
    def fxIndex(self) -> str:
        """FX index"""
        return self.__fxIndex

    @fxIndex.setter
    def fxIndex(self, value: str):
        self.__fxIndex = value
        self._property_changed('fxIndex')        

    @property
    def tradeAs(self) -> str:
        """How to trade the Option."""
        return self.__tradeAs

    @tradeAs.setter
    def tradeAs(self, value: str):
        self.__tradeAs = value
        self._property_changed('tradeAs')        

    @property
    def cloneParentId(self) -> str:
        """Marquee unique identifier"""
        return self.__cloneParentId

    @cloneParentId.setter
    def cloneParentId(self, value: str):
        self.__cloneParentId = value
        self._property_changed('cloneParentId')        

    @property
    def onBehalfOf(self) -> str:
        """Marquee unique identifier"""
        return self.__onBehalfOf

    @onBehalfOf.setter
    def onBehalfOf(self, value: str):
        self.__onBehalfOf = value
        self._property_changed('onBehalfOf')        

    @property
    def indexCalculationAgent(self) -> str:
        """Calculation agent of the index."""
        return self.__indexCalculationAgent

    @indexCalculationAgent.setter
    def indexCalculationAgent(self, value: str):
        self.__indexCalculationAgent = value
        self._property_changed('indexCalculationAgent')        


class AssetStats(Base):
        
    """Performance statistics."""
       
    def __init__(self, lastUpdatedTime: datetime.datetime = None, period: Union[AssetStatsPeriod, str] = None, type: Union[AssetStatsType, str] = None, stats: PerformanceStats = None):
        super().__init__()
        self.__lastUpdatedTime = lastUpdatedTime
        self.__period = period if isinstance(period, AssetStatsPeriod) else get_enum_value(AssetStatsPeriod, period)
        self.__type = type if isinstance(type, AssetStatsType) else get_enum_value(AssetStatsType, type)
        self.__stats = stats

    @property
    def lastUpdatedTime(self) -> datetime.datetime:
        return self.__lastUpdatedTime

    @lastUpdatedTime.setter
    def lastUpdatedTime(self, value: datetime.datetime):
        self.__lastUpdatedTime = value
        self._property_changed('lastUpdatedTime')        

    @property
    def period(self) -> Union[AssetStatsPeriod, str]:
        """The period used to produce date range."""
        return self.__period

    @period.setter
    def period(self, value: Union[AssetStatsPeriod, str]):
        self.__period = value if isinstance(value, AssetStatsPeriod) else get_enum_value(AssetStatsPeriod, value)
        self._property_changed('period')        

    @property
    def type(self) -> Union[AssetStatsType, str]:
        """Is it rolling, none etc."""
        return self.__type

    @type.setter
    def type(self, value: Union[AssetStatsType, str]):
        self.__type = value if isinstance(value, AssetStatsType) else get_enum_value(AssetStatsType, value)
        self._property_changed('type')        

    @property
    def stats(self) -> PerformanceStats:
        """Performance statistics."""
        return self.__stats

    @stats.setter
    def stats(self, value: PerformanceStats):
        self.__stats = value
        self._property_changed('stats')        


class AssetStatsRequest(Base):
        
    """Performance statistics."""
       
    def __init__(self, lastUpdatedTime: datetime.datetime = None, period: Union[AssetStatsPeriod, str] = None, type: Union[AssetStatsType, str] = None, stats: PerformanceStatsRequest = None):
        super().__init__()
        self.__lastUpdatedTime = lastUpdatedTime
        self.__period = period if isinstance(period, AssetStatsPeriod) else get_enum_value(AssetStatsPeriod, period)
        self.__type = type if isinstance(type, AssetStatsType) else get_enum_value(AssetStatsType, type)
        self.__stats = stats

    @property
    def lastUpdatedTime(self) -> datetime.datetime:
        return self.__lastUpdatedTime

    @lastUpdatedTime.setter
    def lastUpdatedTime(self, value: datetime.datetime):
        self.__lastUpdatedTime = value
        self._property_changed('lastUpdatedTime')        

    @property
    def period(self) -> Union[AssetStatsPeriod, str]:
        """The period used to produce date range."""
        return self.__period

    @period.setter
    def period(self, value: Union[AssetStatsPeriod, str]):
        self.__period = value if isinstance(value, AssetStatsPeriod) else get_enum_value(AssetStatsPeriod, value)
        self._property_changed('period')        

    @property
    def type(self) -> Union[AssetStatsType, str]:
        """Is it rolling, none etc."""
        return self.__type

    @type.setter
    def type(self, value: Union[AssetStatsType, str]):
        self.__type = value if isinstance(value, AssetStatsType) else get_enum_value(AssetStatsType, value)
        self._property_changed('type')        

    @property
    def stats(self) -> PerformanceStatsRequest:
        """Performance statistics."""
        return self.__stats

    @stats.setter
    def stats(self, value: PerformanceStatsRequest):
        self.__stats = value
        self._property_changed('stats')        


class CommodConfigParameters(Base):
        
    """Commodity configuration parameters"""
       
    def __init__(self, infra: str, fieldHistory: Tuple[dict, ...]):
        super().__init__()
        self.__infra = infra
        self.__fieldHistory = fieldHistory

    @property
    def infra(self) -> str:
        return self.__infra

    @infra.setter
    def infra(self, value: str):
        self.__infra = value
        self._property_changed('infra')        

    @property
    def fieldHistory(self) -> Tuple[dict, ...]:
        return self.__fieldHistory

    @fieldHistory.setter
    def fieldHistory(self, value: Tuple[dict, ...]):
        self.__fieldHistory = value
        self._property_changed('fieldHistory')        


class HedgeFundParameters(Base):
        
    """Asset parameters specific to hedge funds"""
       
    def __init__(self, aum: float = None, strategyAum: float = None, aumRange: NumberRange = None, strategyAumRange: NumberRange = None, disclaimers: str = None, marketCapCategory: Tuple[str, ...] = None, marketingStatus: str = None, preferences: dict = None, regionalFocus: Tuple[str, ...] = None, riskTakingModel: str = None, strategy: Union[Strategy, str] = None, supraStrategy: Union[SupraStrategy, str] = None, strategyDescription: str = None, targetedGrossExposure: NumberRange = None, targetedNetExposure: NumberRange = None, targetedNumOfPositionsShort: NumberRange = None, targetedNumOfPositionsLong: NumberRange = None, turnover: str = None, vehicleType: str = None, netExposureClassification: Union[NetExposureClassification, str] = None):
        super().__init__()
        self.__aum = aum
        self.__strategyAum = strategyAum
        self.__aumRange = aumRange
        self.__strategyAumRange = strategyAumRange
        self.__disclaimers = disclaimers
        self.__marketCapCategory = marketCapCategory
        self.__marketingStatus = marketingStatus
        self.__preferences = preferences
        self.__regionalFocus = regionalFocus
        self.__riskTakingModel = riskTakingModel
        self.__strategy = strategy if isinstance(strategy, Strategy) else get_enum_value(Strategy, strategy)
        self.__supraStrategy = supraStrategy if isinstance(supraStrategy, SupraStrategy) else get_enum_value(SupraStrategy, supraStrategy)
        self.__strategyDescription = strategyDescription
        self.__targetedGrossExposure = targetedGrossExposure
        self.__targetedNetExposure = targetedNetExposure
        self.__targetedNumOfPositionsShort = targetedNumOfPositionsShort
        self.__targetedNumOfPositionsLong = targetedNumOfPositionsLong
        self.__turnover = turnover
        self.__vehicleType = vehicleType
        self.__netExposureClassification = netExposureClassification if isinstance(netExposureClassification, NetExposureClassification) else get_enum_value(NetExposureClassification, netExposureClassification)

    @property
    def aum(self) -> float:
        """Current assets under management. Only viewable after having been granted additional access to asset information."""
        return self.__aum

    @aum.setter
    def aum(self, value: float):
        self.__aum = value
        self._property_changed('aum')        

    @property
    def strategyAum(self) -> float:
        """Total assets under management for this strategy (including comingled fund, managed accounts, and funds of one). Only viewable after having been granted additional access to asset information."""
        return self.__strategyAum

    @strategyAum.setter
    def strategyAum(self, value: float):
        self.__strategyAum = value
        self._property_changed('strategyAum')        

    @property
    def aumRange(self) -> NumberRange:
        """Range in which assets under management fall. Same view permissions as the asset."""
        return self.__aumRange

    @aumRange.setter
    def aumRange(self, value: NumberRange):
        self.__aumRange = value
        self._property_changed('aumRange')        

    @property
    def strategyAumRange(self) -> NumberRange:
        """Range in which assets under management for this strategy fall. Same view permissions as the asset."""
        return self.__strategyAumRange

    @strategyAumRange.setter
    def strategyAumRange(self, value: NumberRange):
        self.__strategyAumRange = value
        self._property_changed('strategyAumRange')        

    @property
    def disclaimers(self) -> str:
        """Legal disclaimers for performance data. Same view permissions as the asset."""
        return self.__disclaimers

    @disclaimers.setter
    def disclaimers(self, value: str):
        self.__disclaimers = value
        self._property_changed('disclaimers')        

    @property
    def marketCapCategory(self) -> Tuple[str, ...]:
        """Category of market capitalizations a fund is focused on from an investment perspective. Same view permissions as the asset."""
        return self.__marketCapCategory

    @marketCapCategory.setter
    def marketCapCategory(self, value: Tuple[str, ...]):
        self.__marketCapCategory = value
        self._property_changed('marketCapCategory')        

    @property
    def marketingStatus(self) -> str:
        """A fund's posture as to whether it is currently accepting new subscriptions. Same view permissions as the asset."""
        return self.__marketingStatus

    @marketingStatus.setter
    def marketingStatus(self, value: str):
        self.__marketingStatus = value
        self._property_changed('marketingStatus')        

    @property
    def preferences(self) -> dict:
        """Lists of blacklisted company attributes."""
        return self.__preferences

    @preferences.setter
    def preferences(self, value: dict):
        self.__preferences = value
        self._property_changed('preferences')        

    @property
    def regionalFocus(self) -> Tuple[str, ...]:
        """Section of the world a fund is focused on from an investment perspective. Same view permissions as the asset"""
        return self.__regionalFocus

    @regionalFocus.setter
    def regionalFocus(self, value: Tuple[str, ...]):
        self.__regionalFocus = value
        self._property_changed('regionalFocus')        

    @property
    def riskTakingModel(self) -> str:
        """Number of risk takers a fund has. Same view permissions as the asset"""
        return self.__riskTakingModel

    @riskTakingModel.setter
    def riskTakingModel(self, value: str):
        self.__riskTakingModel = value
        self._property_changed('riskTakingModel')        

    @property
    def strategy(self) -> Union[Strategy, str]:
        """More specific descriptor of a fund's investment approach. Same view permissions as the asset"""
        return self.__strategy

    @strategy.setter
    def strategy(self, value: Union[Strategy, str]):
        self.__strategy = value if isinstance(value, Strategy) else get_enum_value(Strategy, value)
        self._property_changed('strategy')        

    @property
    def supraStrategy(self) -> Union[SupraStrategy, str]:
        """Broad descriptor of a fund's investment approach. Same view permissions as the asset"""
        return self.__supraStrategy

    @supraStrategy.setter
    def supraStrategy(self, value: Union[SupraStrategy, str]):
        self.__supraStrategy = value if isinstance(value, SupraStrategy) else get_enum_value(SupraStrategy, value)
        self._property_changed('supraStrategy')        

    @property
    def strategyDescription(self) -> str:
        """Statement explaining a fund's investment approach. Only viewable after having been granted additional access to asset information."""
        return self.__strategyDescription

    @strategyDescription.setter
    def strategyDescription(self, value: str):
        self.__strategyDescription = value
        self._property_changed('strategyDescription')        

    @property
    def targetedGrossExposure(self) -> NumberRange:
        """Value of a fund's long positions plus short positions, expressed in percentage terms. Only viewable after having been granted additional access to asset information."""
        return self.__targetedGrossExposure

    @targetedGrossExposure.setter
    def targetedGrossExposure(self, value: NumberRange):
        self.__targetedGrossExposure = value
        self._property_changed('targetedGrossExposure')        

    @property
    def targetedNetExposure(self) -> NumberRange:
        """Value of a fund's long positions minus short positions, expressed in percentage terms. Only viewable after having been granted additional access to asset information."""
        return self.__targetedNetExposure

    @targetedNetExposure.setter
    def targetedNetExposure(self, value: NumberRange):
        self.__targetedNetExposure = value
        self._property_changed('targetedNetExposure')        

    @property
    def targetedNumOfPositionsShort(self) -> NumberRange:
        """Range of positions the fund typically holds on the short side of its portfolio. Only viewable after having been granted additional access to asset information."""
        return self.__targetedNumOfPositionsShort

    @targetedNumOfPositionsShort.setter
    def targetedNumOfPositionsShort(self, value: NumberRange):
        self.__targetedNumOfPositionsShort = value
        self._property_changed('targetedNumOfPositionsShort')        

    @property
    def targetedNumOfPositionsLong(self) -> NumberRange:
        """Range of positions the fund typically holds on the long side of its portfolio. Only viewable after having been granted additional access to asset information."""
        return self.__targetedNumOfPositionsLong

    @targetedNumOfPositionsLong.setter
    def targetedNumOfPositionsLong(self, value: NumberRange):
        self.__targetedNumOfPositionsLong = value
        self._property_changed('targetedNumOfPositionsLong')        

    @property
    def turnover(self) -> str:
        """Rate at which a fund replaces its investment holdings. Only viewable after having been granted additional access to asset information."""
        return self.__turnover

    @turnover.setter
    def turnover(self, value: str):
        self.__turnover = value
        self._property_changed('turnover')        

    @property
    def vehicleType(self) -> str:
        """Type of investment vehicle. Only viewable after having been granted additional access to asset information."""
        return self.__vehicleType

    @vehicleType.setter
    def vehicleType(self, value: str):
        self.__vehicleType = value
        self._property_changed('vehicleType')        

    @property
    def netExposureClassification(self) -> Union[NetExposureClassification, str]:
        """Classification for net exposure of fund."""
        return self.__netExposureClassification

    @netExposureClassification.setter
    def netExposureClassification(self, value: Union[NetExposureClassification, str]):
        self.__netExposureClassification = value if isinstance(value, NetExposureClassification) else get_enum_value(NetExposureClassification, value)
        self._property_changed('netExposureClassification')        


class ShareClassParameters(Base):
        
    """Attributes specific to share class assets"""
       
    def __init__(self, additionalProvisions: str = None, benchmark: Benchmark = None, earlyRedemptionFee: float = None, gate: float = None, gateType: str = None, hurdle: float = None, hurdleType: str = None, lockup: float = None, lockupType: str = None, managementFee: float = None, minimumSubscription: float = None, name: str = None, performanceFee: float = None, redemptionNoticePeriod: float = None, redemptionPeriod: str = None, sidePocket: str = None, status: str = None, termType: str = None):
        super().__init__()
        self.__additionalProvisions = additionalProvisions
        self.__benchmark = benchmark
        self.__earlyRedemptionFee = earlyRedemptionFee
        self.__gate = gate
        self.__gateType = gateType
        self.__hurdle = hurdle
        self.__hurdleType = hurdleType
        self.__lockup = lockup
        self.__lockupType = lockupType
        self.__managementFee = managementFee
        self.__minimumSubscription = minimumSubscription
        self.__name = name
        self.__performanceFee = performanceFee
        self.__redemptionNoticePeriod = redemptionNoticePeriod
        self.__redemptionPeriod = redemptionPeriod
        self.__sidePocket = sidePocket
        self.__status = status
        self.__termType = termType

    @property
    def additionalProvisions(self) -> str:
        """Additional details that are relevant to the share class that not captured by the other fields"""
        return self.__additionalProvisions

    @additionalProvisions.setter
    def additionalProvisions(self, value: str):
        self.__additionalProvisions = value
        self._property_changed('additionalProvisions')        

    @property
    def benchmark(self) -> Benchmark:
        """Reference rate that can based on an absolute value or absolute value + index"""
        return self.__benchmark

    @benchmark.setter
    def benchmark(self, value: Benchmark):
        self.__benchmark = value
        self._property_changed('benchmark')        

    @property
    def earlyRedemptionFee(self) -> float:
        """Fee an investor pays to redeem before the expiry of a soft lock-up"""
        return self.__earlyRedemptionFee

    @earlyRedemptionFee.setter
    def earlyRedemptionFee(self, value: float):
        self.__earlyRedemptionFee = value
        self._property_changed('earlyRedemptionFee')        

    @property
    def gate(self) -> float:
        """Limit to the amount of capital that can be redeemed from a fund"""
        return self.__gate

    @gate.setter
    def gate(self, value: float):
        self.__gate = value
        self._property_changed('gate')        

    @property
    def gateType(self) -> str:
        """Category that gate relates to"""
        return self.__gateType

    @gateType.setter
    def gateType(self, value: str):
        self.__gateType = value
        self._property_changed('gateType')        

    @property
    def hurdle(self) -> float:
        """Minimum rate of return a fund must generate before it collects a performance fee"""
        return self.__hurdle

    @hurdle.setter
    def hurdle(self, value: float):
        self.__hurdle = value
        self._property_changed('hurdle')        

    @property
    def hurdleType(self) -> str:
        """Determines if the hurdle is calculated on all profits above hurdle rate"""
        return self.__hurdleType

    @hurdleType.setter
    def hurdleType(self, value: str):
        self.__hurdleType = value
        self._property_changed('hurdleType')        

    @property
    def lockup(self) -> float:
        """Number of months an investor is not allowed to redeem investment"""
        return self.__lockup

    @lockup.setter
    def lockup(self, value: float):
        self.__lockup = value
        self._property_changed('lockup')        

    @property
    def lockupType(self) -> str:
        """Classification of lockup"""
        return self.__lockupType

    @lockupType.setter
    def lockupType(self, value: str):
        self.__lockupType = value
        self._property_changed('lockupType')        

    @property
    def managementFee(self) -> float:
        """Percent fee paid by investor to compensate manager for the cost of managing their assets"""
        return self.__managementFee

    @managementFee.setter
    def managementFee(self, value: float):
        self.__managementFee = value
        self._property_changed('managementFee')        

    @property
    def minimumSubscription(self) -> float:
        """Lowest level of investment a fund will accept"""
        return self.__minimumSubscription

    @minimumSubscription.setter
    def minimumSubscription(self, value: float):
        self.__minimumSubscription = value
        self._property_changed('minimumSubscription')        

    @property
    def name(self) -> str:
        """Identifier for particular share class"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def performanceFee(self) -> float:
        """Fee paid by investor to compensate manager for generating positive returns or alpha"""
        return self.__performanceFee

    @performanceFee.setter
    def performanceFee(self, value: float):
        self.__performanceFee = value
        self._property_changed('performanceFee')        

    @property
    def redemptionNoticePeriod(self) -> float:
        """Number of days prior to a redemption that an investor must notify a manager of their intent"""
        return self.__redemptionNoticePeriod

    @redemptionNoticePeriod.setter
    def redemptionNoticePeriod(self, value: float):
        self.__redemptionNoticePeriod = value
        self._property_changed('redemptionNoticePeriod')        

    @property
    def redemptionPeriod(self) -> str:
        """Frequency on which an investor can redeem from a fund"""
        return self.__redemptionPeriod

    @redemptionPeriod.setter
    def redemptionPeriod(self, value: str):
        self.__redemptionPeriod = value
        self._property_changed('redemptionPeriod')        

    @property
    def sidePocket(self) -> str:
        """Account utilized to separate illiquid assets from more liquid investments"""
        return self.__sidePocket

    @sidePocket.setter
    def sidePocket(self, value: str):
        self.__sidePocket = value
        self._property_changed('sidePocket')        

    @property
    def status(self) -> str:
        """Denotes whether the share class is currently accepting new subscriptions"""
        return self.__status

    @status.setter
    def status(self, value: str):
        self.__status = value
        self._property_changed('status')        

    @property
    def termType(self) -> str:
        """category that describes share class offering"""
        return self.__termType

    @termType.setter
    def termType(self, value: str):
        self.__termType = value
        self._property_changed('termType')        


class TemporalPeople(Base):
        
    """People associated with an asset during a certain date range"""
       
    def __init__(self, startDate: datetime.date = None, endDate: datetime.date = None, people: People = None):
        super().__init__()
        self.__startDate = startDate
        self.__endDate = endDate
        self.__people = people

    @property
    def startDate(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__startDate

    @startDate.setter
    def startDate(self, value: datetime.date):
        self.__startDate = value
        self._property_changed('startDate')        

    @property
    def endDate(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__endDate

    @endDate.setter
    def endDate(self, value: datetime.date):
        self.__endDate = value
        self._property_changed('endDate')        

    @property
    def people(self) -> People:
        """People associated with an asset"""
        return self.__people

    @people.setter
    def people(self, value: People):
        self.__people = value
        self._property_changed('people')        


class Asset(Base):
        
    """A security or instrument which can be held in a trading book (for example a stock or a bond) or a publically identifiable object with observable market data fixings which can be referenced in derivative transations (for example the SPX Index)"""
       
    def __init__(self, assetClass: Union[AssetClass, str], type: Union[AssetType, str], name: str, createdById: str = None, createdTime: datetime.datetime = None, currency: Union[Currency, str] = None, description: str = None, entitlements: Entitlements = None, entitlementExclusions: EntitlementExclusions = None, exchange: str = None, id: str = None, identifiers: Tuple[Identifier, ...] = None, lastUpdatedById: str = None, lastUpdatedTime: datetime.datetime = None, listed: bool = None, liveDate: datetime.date = None, ownerId: str = None, parameters: dict = None, assetStats: Tuple[AssetStats, ...] = None, people: People = None, region: Union[Region, str] = None, reportIds: Tuple[str, ...] = None, shortName: str = None, styles: Tuple[str, ...] = None, tags: Tuple[str, ...] = None, underlyingAssetIds: Tuple[str, ...] = None):
        super().__init__()
        self.__assetClass = assetClass if isinstance(assetClass, AssetClass) else get_enum_value(AssetClass, assetClass)
        self.__createdById = createdById
        self.__createdTime = createdTime
        self.__currency = currency if isinstance(currency, Currency) else get_enum_value(Currency, currency)
        self.__description = description
        self.__entitlements = entitlements
        self.__entitlementExclusions = entitlementExclusions
        self.__exchange = exchange
        self.__id = id
        self.__identifiers = identifiers
        self.__lastUpdatedById = lastUpdatedById
        self.__lastUpdatedTime = lastUpdatedTime
        self.__listed = listed
        self.__liveDate = liveDate
        self.__name = name
        self.__ownerId = ownerId
        self.__parameters = parameters
        self.__assetStats = assetStats
        self.__people = people
        self.__region = region if isinstance(region, Region) else get_enum_value(Region, region)
        self.__reportIds = reportIds
        self.__shortName = shortName
        self.__styles = styles
        self.__tags = tags
        self.__type = type if isinstance(type, AssetType) else get_enum_value(AssetType, type)
        self.__underlyingAssetIds = underlyingAssetIds

    @property
    def assetClass(self) -> Union[AssetClass, str]:
        """Asset classification of security. Assets are classified into broad groups which exhibit similar characteristics and behave in a consistent way under different market conditions"""
        return self.__assetClass

    @assetClass.setter
    def assetClass(self, value: Union[AssetClass, str]):
        self.__assetClass = value if isinstance(value, AssetClass) else get_enum_value(AssetClass, value)
        self._property_changed('assetClass')        

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
    def description(self) -> str:
        """Free text description of asset. Description provided will be indexed in the search service for free text relevance match"""
        return self.__description

    @description.setter
    def description(self, value: str):
        self.__description = value
        self._property_changed('description')        

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
    def exchange(self) -> str:
        """Name of marketplace where security, derivative or other instrument is traded"""
        return self.__exchange

    @exchange.setter
    def exchange(self, value: str):
        self.__exchange = value
        self._property_changed('exchange')        

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
    def listed(self) -> bool:
        """Whether the asset is currently listed or not"""
        return self.__listed

    @listed.setter
    def listed(self, value: bool):
        self.__listed = value
        self._property_changed('listed')        

    @property
    def liveDate(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__liveDate

    @liveDate.setter
    def liveDate(self, value: datetime.date):
        self.__liveDate = value
        self._property_changed('liveDate')        

    @property
    def name(self) -> str:
        """Display name of the asset"""
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
    def parameters(self) -> dict:
        return self.__parameters

    @parameters.setter
    def parameters(self, value: dict):
        self.__parameters = value
        self._property_changed('parameters')        

    @property
    def assetStats(self) -> Tuple[AssetStats, ...]:
        """Performance statistics."""
        return self.__assetStats

    @assetStats.setter
    def assetStats(self, value: Tuple[AssetStats, ...]):
        self.__assetStats = value
        self._property_changed('assetStats')        

    @property
    def people(self) -> People:
        """Key people associated with asset"""
        return self.__people

    @people.setter
    def people(self, value: People):
        self.__people = value
        self._property_changed('people')        

    @property
    def region(self) -> Union[Region, str]:
        """Regional classification for the asset"""
        return self.__region

    @region.setter
    def region(self, value: Union[Region, str]):
        self.__region = value if isinstance(value, Region) else get_enum_value(Region, value)
        self._property_changed('region')        

    @property
    def reportIds(self) -> Tuple[str, ...]:
        """Array of report identifiers related to the object"""
        return self.__reportIds

    @reportIds.setter
    def reportIds(self, value: Tuple[str, ...]):
        self.__reportIds = value
        self._property_changed('reportIds')        

    @property
    def shortName(self) -> str:
        """Short name or alias for the asset"""
        return self.__shortName

    @shortName.setter
    def shortName(self, value: str):
        self.__shortName = value
        self._property_changed('shortName')        

    @property
    def styles(self) -> Tuple[str, ...]:
        """Styles or themes associated with the asset (max 50)"""
        return self.__styles

    @styles.setter
    def styles(self, value: Tuple[str, ...]):
        self.__styles = value
        self._property_changed('styles')        

    @property
    def tags(self) -> Tuple[str, ...]:
        """Metadata associated with the object. Provide an array of strings which will be indexed for search and locating related objects"""
        return self.__tags

    @tags.setter
    def tags(self, value: Tuple[str, ...]):
        self.__tags = value
        self._property_changed('tags')        

    @property
    def type(self) -> Union[AssetType, str]:
        """Asset type differentiates the product categorization or contract type"""
        return self.__type

    @type.setter
    def type(self, value: Union[AssetType, str]):
        self.__type = value if isinstance(value, AssetType) else get_enum_value(AssetType, value)
        self._property_changed('type')        

    @property
    def underlyingAssetIds(self) -> Tuple[str, ...]:
        """Underlying asset ids"""
        return self.__underlyingAssetIds

    @underlyingAssetIds.setter
    def underlyingAssetIds(self, value: Tuple[str, ...]):
        self.__underlyingAssetIds = value
        self._property_changed('underlyingAssetIds')        


class EntityQuery(Base):
               
    def __init__(self, format: Union[Format, str] = None, where: FieldFilterMap = None, asOfTime: datetime.datetime = None, date: datetime.date = None, time: datetime.datetime = None, delay: int = None, orderBy: Tuple[Union[dict, str], ...] = None, scroll: str = None, scrollId: str = None, fields: Tuple[Union[dict, str], ...] = None, limit: int = None, offset: int = None):
        super().__init__()
        self.__format = format if isinstance(format, Format) else get_enum_value(Format, format)
        self.__where = where
        self.__asOfTime = asOfTime
        self.__date = date
        self.__time = time
        self.__delay = delay
        self.__orderBy = orderBy
        self.__scroll = scroll
        self.__scrollId = scrollId
        self.__fields = fields
        self.__limit = limit
        self.__offset = offset

    @property
    def format(self) -> Union[Format, str]:
        """Alternative format for data to be returned in"""
        return self.__format

    @format.setter
    def format(self, value: Union[Format, str]):
        self.__format = value if isinstance(value, Format) else get_enum_value(Format, value)
        self._property_changed('format')        

    @property
    def where(self) -> FieldFilterMap:
        return self.__where

    @where.setter
    def where(self, value: FieldFilterMap):
        self.__where = value
        self._property_changed('where')        

    @property
    def asOfTime(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__asOfTime

    @asOfTime.setter
    def asOfTime(self, value: datetime.datetime):
        self.__asOfTime = value
        self._property_changed('asOfTime')        

    @property
    def date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__date

    @date.setter
    def date(self, value: datetime.date):
        self.__date = value
        self._property_changed('date')        

    @property
    def time(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__time

    @time.setter
    def time(self, value: datetime.datetime):
        self.__time = value
        self._property_changed('time')        

    @property
    def delay(self) -> int:
        """Number of minutes to delay returning data"""
        return self.__delay

    @delay.setter
    def delay(self, value: int):
        self.__delay = value
        self._property_changed('delay')        

    @property
    def orderBy(self) -> Tuple[Union[dict, str], ...]:
        return self.__orderBy

    @orderBy.setter
    def orderBy(self, value: Tuple[Union[dict, str], ...]):
        self.__orderBy = value
        self._property_changed('orderBy')        

    @property
    def scroll(self) -> str:
        """Time for which to keep the scroll search context alive, i.e. 1m (1 minute) or 10s (10 seconds)"""
        return self.__scroll

    @scroll.setter
    def scroll(self, value: str):
        self.__scroll = value
        self._property_changed('scroll')        

    @property
    def scrollId(self) -> str:
        """Scroll identifier to be used to retrieve the next batch of results"""
        return self.__scrollId

    @scrollId.setter
    def scrollId(self, value: str):
        self.__scrollId = value
        self._property_changed('scrollId')        

    @property
    def fields(self) -> Tuple[Union[dict, str], ...]:
        return self.__fields

    @fields.setter
    def fields(self, value: Tuple[Union[dict, str], ...]):
        self.__fields = value
        self._property_changed('fields')        

    @property
    def limit(self) -> int:
        """Limit on the number of objects to be returned in the response. Can range between 1 and 10000"""
        return self.__limit

    @limit.setter
    def limit(self, value: int):
        self.__limit = value
        self._property_changed('limit')        

    @property
    def offset(self) -> int:
        """The offset of the first result returned (default 0). Can be used in pagination to defined the first item in the list to be returned, for example if you request 100 objects, to query the next page you would specify offset = 100."""
        return self.__offset

    @offset.setter
    def offset(self, value: int):
        self.__offset = value
        self._property_changed('offset')        
