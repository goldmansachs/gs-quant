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


class Commodities(EnumBase, Enum):    
    
    """Commodity asset"""

    Aluminium = 'Aluminium'
    Aluminium_Alloy = 'Aluminium Alloy'
    Chicago_Ethanol = 'Chicago Ethanol'
    Coal = 'Coal'
    Coffee = 'Coffee'
    Copper = 'Copper'
    Corn = 'Corn'
    Cotton = 'Cotton'
    Crude_Palm_Oil = 'Crude Palm Oil'
    Diesel_Fuel = 'Diesel Fuel'
    Electricity = 'Electricity'
    Emissions = 'Emissions'
    Ethylene = 'Ethylene'
    Freight = 'Freight'
    Fuel_Oil = 'Fuel Oil'
    Gas_Oil = 'Gas Oil'
    Gasoline = 'Gasoline'
    Gold = 'Gold'
    Heating_Oil = 'Heating Oil'
    Iron_Ore = 'Iron Ore'
    Jet_Fuel = 'Jet Fuel'
    Lead = 'Lead'
    Lean_Hogs = 'Lean Hogs'
    NGL = 'NGL'
    Naphtha = 'Naphtha'
    Natural_Gas = 'Natural Gas'
    Nickel = 'Nickel'
    Oil = 'Oil'
    Palladium = 'Palladium'
    Platinum = 'Platinum'
    Polypropylene = 'Polypropylene'
    Primary_Aluminium = 'Primary Aluminium'
    Silver = 'Silver'
    Soybean_Meal = 'Soybean Meal'
    Soybean_Oil = 'Soybean Oil'
    Soybeans = 'Soybeans'
    Sugar = 'Sugar'
    Tin = 'Tin'
    Ultra_Low_Sulphur_Diesel = 'Ultra Low Sulphur Diesel'
    Wheat = 'Wheat'
    White_Sugar = 'White Sugar'
    Zinc = 'Zinc'
    
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
               
    def __init__(
        self,
        risk_country_name: str = None,
        risk_country_code: str = None,
        country_name: str = None,
        country_code: str = None,
        is_primary: bool = None,
        gics_sector: str = None,
        gics_industry_group: str = None,
        gics_industry: str = None,
        gics_sub_industry: str = None,
        commod_template: str = None        
    ):
        super().__init__()
        self.__risk_country_name = risk_country_name
        self.__risk_country_code = risk_country_code
        self.__country_name = country_name
        self.__country_code = country_code
        self.__is_primary = is_primary
        self.__gics_sector = gics_sector
        self.__gics_industry_group = gics_industry_group
        self.__gics_industry = gics_industry
        self.__gics_sub_industry = gics_sub_industry
        self.__commod_template = commod_template

    @property
    def risk_country_name(self) -> str:
        """Risk Country"""
        return self.__risk_country_name

    @risk_country_name.setter
    def risk_country_name(self, value: str):
        self.__risk_country_name = value
        self._property_changed('risk_country_name')        

    @property
    def risk_country_code(self) -> str:
        """Risk Country code (ISO 3166)."""
        return self.__risk_country_code

    @risk_country_code.setter
    def risk_country_code(self, value: str):
        self.__risk_country_code = value
        self._property_changed('risk_country_code')        

    @property
    def country_name(self) -> str:
        """Country name of asset"""
        return self.__country_name

    @country_name.setter
    def country_name(self, value: str):
        self.__country_name = value
        self._property_changed('country_name')        

    @property
    def country_code(self) -> str:
        """Country code (ISO 3166)"""
        return self.__country_code

    @country_code.setter
    def country_code(self, value: str):
        self.__country_code = value
        self._property_changed('country_code')        

    @property
    def is_primary(self) -> bool:
        """Is this the primary exchange listing for the asset"""
        return self.__is_primary

    @is_primary.setter
    def is_primary(self, value: bool):
        self.__is_primary = value
        self._property_changed('is_primary')        

    @property
    def gics_sector(self) -> str:
        """GICS Sector classification (level 1)"""
        return self.__gics_sector

    @gics_sector.setter
    def gics_sector(self, value: str):
        self.__gics_sector = value
        self._property_changed('gics_sector')        

    @property
    def gics_industry_group(self) -> str:
        """GICS Industry Group classification (level 2)"""
        return self.__gics_industry_group

    @gics_industry_group.setter
    def gics_industry_group(self, value: str):
        self.__gics_industry_group = value
        self._property_changed('gics_industry_group')        

    @property
    def gics_industry(self) -> str:
        """GICS Industry classification (level 3)"""
        return self.__gics_industry

    @gics_industry.setter
    def gics_industry(self, value: str):
        self.__gics_industry = value
        self._property_changed('gics_industry')        

    @property
    def gics_sub_industry(self) -> str:
        """GICS Sub Industry classification (level 4)"""
        return self.__gics_sub_industry

    @gics_sub_industry.setter
    def gics_sub_industry(self, value: str):
        self.__gics_sub_industry = value
        self._property_changed('gics_sub_industry')        

    @property
    def commod_template(self) -> str:
        """Commodities generic template, i.e. Heating Oil"""
        return self.__commod_template

    @commod_template.setter
    def commod_template(self, value: str):
        self.__commod_template = value
        self._property_changed('commod_template')        


class AssetToInstrumentResponse(Base):
        
    """Resolution of assetId to instrument"""
       
    def __init__(
        self,
        asset_id: str,
        name: str,
        instrument: Instrument,
        size_field: str        
    ):
        super().__init__()
        self.__asset_id = asset_id
        self.__name = name
        self.__instrument = instrument
        self.__size_field = size_field

    @property
    def asset_id(self) -> str:
        """Marquee unique asset identifier."""
        return self.__asset_id

    @asset_id.setter
    def asset_id(self, value: str):
        self.__asset_id = value
        self._property_changed('asset_id')        

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
    def size_field(self) -> str:
        """Size field."""
        return self.__size_field

    @size_field.setter
    def size_field(self, value: str):
        self.__size_field = value
        self._property_changed('size_field')        


class Benchmark(Base):
        
    """Reference rate that can based on an absolute value or absolute value + index"""
       
    def __init__(
        self,
        asset_id: str = None,
        value: float = None,
        name: str = None        
    ):
        super().__init__()
        self.__asset_id = asset_id
        self.__value = value
        self.__name = name

    @property
    def asset_id(self) -> str:
        """Asset for rate index"""
        return self.__asset_id

    @asset_id.setter
    def asset_id(self, value: str):
        self.__asset_id = value
        self._property_changed('asset_id')        

    @property
    def value(self) -> float:
        """Absolute value for reference rate"""
        return self.__value

    @value.setter
    def value(self, value: float):
        self.__value = value
        self._property_changed('value')        

    @property
    def name(self) -> str:
        """Name of an asset if assetId cannot be provided"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        


class NumberRange(Base):
        
    """lower and upper bound to define a number range"""
       
    def __init__(
        self,
        lower_bound: float = None,
        upper_bound: float = None        
    ):
        super().__init__()
        self.__lower_bound = lower_bound
        self.__upper_bound = upper_bound

    @property
    def lower_bound(self) -> float:
        """value that defines the lower boundary of the range"""
        return self.__lower_bound

    @lower_bound.setter
    def lower_bound(self, value: float):
        self.__lower_bound = value
        self._property_changed('lower_bound')        

    @property
    def upper_bound(self) -> float:
        """value that defines the upper boundary of the range"""
        return self.__upper_bound

    @upper_bound.setter
    def upper_bound(self, value: float):
        self.__upper_bound = value
        self._property_changed('upper_bound')        


class People(Base):
        
    """People associated with an asset"""
       
    def __init__(
        self,
        portfolio_managers: Tuple[str, ...] = None        
    ):
        super().__init__()
        self.__portfolio_managers = portfolio_managers

    @property
    def portfolio_managers(self) -> Tuple[str, ...]:
        """Portfolio managers of asset"""
        return self.__portfolio_managers

    @portfolio_managers.setter
    def portfolio_managers(self, value: Tuple[str, ...]):
        self.__portfolio_managers = value
        self._property_changed('portfolio_managers')        


class PerformanceStatsRequest(Base):
        
    """Performance statistics."""
       
    def __init__(
        self,
        annualized_return: Op = None,
        annualized_volatility: Op = None,
        best_month: Op = None,
        max_draw_down: Op = None,
        max_draw_down_duration: Op = None,
        positive_months: Op = None,
        sharpe_ratio: Op = None,
        sortino_ratio: Op = None,
        worst_month: Op = None,
        average_return: Op = None        
    ):
        super().__init__()
        self.__annualized_return = annualized_return
        self.__annualized_volatility = annualized_volatility
        self.__best_month = best_month
        self.__max_draw_down = max_draw_down
        self.__max_draw_down_duration = max_draw_down_duration
        self.__positive_months = positive_months
        self.__sharpe_ratio = sharpe_ratio
        self.__sortino_ratio = sortino_ratio
        self.__worst_month = worst_month
        self.__average_return = average_return

    @property
    def annualized_return(self) -> Op:
        """Operations for searches."""
        return self.__annualized_return

    @annualized_return.setter
    def annualized_return(self, value: Op):
        self.__annualized_return = value
        self._property_changed('annualized_return')        

    @property
    def annualized_volatility(self) -> Op:
        """Operations for searches."""
        return self.__annualized_volatility

    @annualized_volatility.setter
    def annualized_volatility(self, value: Op):
        self.__annualized_volatility = value
        self._property_changed('annualized_volatility')        

    @property
    def best_month(self) -> Op:
        """Operations for searches."""
        return self.__best_month

    @best_month.setter
    def best_month(self, value: Op):
        self.__best_month = value
        self._property_changed('best_month')        

    @property
    def max_draw_down(self) -> Op:
        """Operations for searches."""
        return self.__max_draw_down

    @max_draw_down.setter
    def max_draw_down(self, value: Op):
        self.__max_draw_down = value
        self._property_changed('max_draw_down')        

    @property
    def max_draw_down_duration(self) -> Op:
        """Operations for searches."""
        return self.__max_draw_down_duration

    @max_draw_down_duration.setter
    def max_draw_down_duration(self, value: Op):
        self.__max_draw_down_duration = value
        self._property_changed('max_draw_down_duration')        

    @property
    def positive_months(self) -> Op:
        """Operations for searches."""
        return self.__positive_months

    @positive_months.setter
    def positive_months(self, value: Op):
        self.__positive_months = value
        self._property_changed('positive_months')        

    @property
    def sharpe_ratio(self) -> Op:
        """Operations for searches."""
        return self.__sharpe_ratio

    @sharpe_ratio.setter
    def sharpe_ratio(self, value: Op):
        self.__sharpe_ratio = value
        self._property_changed('sharpe_ratio')        

    @property
    def sortino_ratio(self) -> Op:
        """Operations for searches."""
        return self.__sortino_ratio

    @sortino_ratio.setter
    def sortino_ratio(self, value: Op):
        self.__sortino_ratio = value
        self._property_changed('sortino_ratio')        

    @property
    def worst_month(self) -> Op:
        """Operations for searches."""
        return self.__worst_month

    @worst_month.setter
    def worst_month(self, value: Op):
        self.__worst_month = value
        self._property_changed('worst_month')        

    @property
    def average_return(self) -> Op:
        """Operations for searches."""
        return self.__average_return

    @average_return.setter
    def average_return(self, value: Op):
        self.__average_return = value
        self._property_changed('average_return')        


class SecuritiesLendingLoan(Base):
        
    """Parameters specific to a securities lending loan"""
       
    def __init__(
        self,
        asset_id: str,
        fund_id: str,
        lender_id: str,
        borrower_id: str,
        loan_status: str = None,
        settlement_status: str = None,
        collateral_type: str = None,
        loan_currency: Union[Currency, str] = None,
        adjustment_ind: bool = None,
        country_of_issue: str = None,
        input_date: datetime.date = None,
        effective_date: datetime.date = None,
        security_settle_date: datetime.date = None,
        cash_settle_date: datetime.date = None,
        term_date: datetime.date = None,
        return_date: datetime.date = None        
    ):
        super().__init__()
        self.__asset_id = asset_id
        self.__fund_id = fund_id
        self.__lender_id = lender_id
        self.__borrower_id = borrower_id
        self.__loan_status = loan_status
        self.__settlement_status = settlement_status
        self.__collateral_type = collateral_type
        self.__loan_currency = get_enum_value(Currency, loan_currency)
        self.__adjustment_ind = adjustment_ind
        self.__country_of_issue = country_of_issue
        self.__input_date = input_date
        self.__effective_date = effective_date
        self.__security_settle_date = security_settle_date
        self.__cash_settle_date = cash_settle_date
        self.__term_date = term_date
        self.__return_date = return_date

    @property
    def asset_id(self) -> str:
        """Id of the security being lent as part of this loan.  This Id should tie to an Asset"""
        return self.__asset_id

    @asset_id.setter
    def asset_id(self, value: str):
        self.__asset_id = value
        self._property_changed('asset_id')        

    @property
    def fund_id(self) -> str:
        """Id of the fund from which the loan is booked.  This Id should tie to an Asset"""
        return self.__fund_id

    @fund_id.setter
    def fund_id(self, value: str):
        self.__fund_id = value
        self._property_changed('fund_id')        

    @property
    def lender_id(self) -> str:
        """Id of the counterpart lending the security.  This Id should tie to a Company"""
        return self.__lender_id

    @lender_id.setter
    def lender_id(self, value: str):
        self.__lender_id = value
        self._property_changed('lender_id')        

    @property
    def borrower_id(self) -> str:
        """Id of the counterpart borrowing the security.  This Id should tie to a Company"""
        return self.__borrower_id

    @borrower_id.setter
    def borrower_id(self, value: str):
        self.__borrower_id = value
        self._property_changed('borrower_id')        

    @property
    def loan_status(self) -> str:
        """The current state of the loan"""
        return self.__loan_status

    @loan_status.setter
    def loan_status(self, value: str):
        self.__loan_status = value
        self._property_changed('loan_status')        

    @property
    def settlement_status(self) -> str:
        """State of the underlying components of the loan."""
        return self.__settlement_status

    @settlement_status.setter
    def settlement_status(self, value: str):
        self.__settlement_status = value
        self._property_changed('settlement_status')        

    @property
    def collateral_type(self) -> str:
        """Type of collateral used to collateralize the loan"""
        return self.__collateral_type

    @collateral_type.setter
    def collateral_type(self, value: str):
        self.__collateral_type = value
        self._property_changed('collateral_type')        

    @property
    def loan_currency(self) -> Union[Currency, str]:
        """Currency in which the loan value is represented"""
        return self.__loan_currency

    @loan_currency.setter
    def loan_currency(self, value: Union[Currency, str]):
        self.__loan_currency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('loan_currency')        

    @property
    def adjustment_ind(self) -> bool:
        """Defines whether or not this contract is for the purpose of a month end loan adjustment."""
        return self.__adjustment_ind

    @adjustment_ind.setter
    def adjustment_ind(self, value: bool):
        self.__adjustment_ind = value
        self._property_changed('adjustment_ind')        

    @property
    def country_of_issue(self) -> str:
        """The country code (ISO 3166) of the underlying security"""
        return self.__country_of_issue

    @country_of_issue.setter
    def country_of_issue(self, value: str):
        self.__country_of_issue = value
        self._property_changed('country_of_issue')        

    @property
    def input_date(self) -> datetime.date:
        """Date that the loan is booked"""
        return self.__input_date

    @input_date.setter
    def input_date(self, value: datetime.date):
        self.__input_date = value
        self._property_changed('input_date')        

    @property
    def effective_date(self) -> datetime.date:
        """Date of the trade"""
        return self.__effective_date

    @effective_date.setter
    def effective_date(self, value: datetime.date):
        self.__effective_date = value
        self._property_changed('effective_date')        

    @property
    def security_settle_date(self) -> datetime.date:
        """Date that the loaned securities settled"""
        return self.__security_settle_date

    @security_settle_date.setter
    def security_settle_date(self, value: datetime.date):
        self.__security_settle_date = value
        self._property_changed('security_settle_date')        

    @property
    def cash_settle_date(self) -> datetime.date:
        """Date of the cash collateral settled"""
        return self.__cash_settle_date

    @cash_settle_date.setter
    def cash_settle_date(self, value: datetime.date):
        self.__cash_settle_date = value
        self._property_changed('cash_settle_date')        

    @property
    def term_date(self) -> datetime.date:
        """Date the dividend is paid for dividend based loans"""
        return self.__term_date

    @term_date.setter
    def term_date(self, value: datetime.date):
        self.__term_date = value
        self._property_changed('term_date')        

    @property
    def return_date(self) -> datetime.date:
        """Date the loan is returned"""
        return self.__return_date

    @return_date.setter
    def return_date(self, value: datetime.date):
        self.__return_date = value
        self._property_changed('return_date')        


class SocialDomain(Base):
               
    def __init__(
        self,
        onboarded: dict        
    ):
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
               
    def __init__(
        self,
        start_date: datetime.date = None,
        end_date: datetime.date = None,
        identifiers: XRef = None        
    ):
        super().__init__()
        self.__start_date = start_date
        self.__end_date = end_date
        self.__identifiers = identifiers

    @property
    def start_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__start_date

    @start_date.setter
    def start_date(self, value: datetime.date):
        self.__start_date = value
        self._property_changed('start_date')        

    @property
    def end_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__end_date

    @end_date.setter
    def end_date(self, value: datetime.date):
        self.__end_date = value
        self._property_changed('end_date')        

    @property
    def identifiers(self) -> XRef:
        return self.__identifiers

    @identifiers.setter
    def identifiers(self, value: XRef):
        self.__identifiers = value
        self._property_changed('identifiers')        


class AssetParameters(Base):
        
    """Parameters specific to the asset type"""
       
    def __init__(
        self,
        basket_type: str = None,
        style: str = None,
        index_calculation_type: str = None,
        index_return_type: str = None,
        index_divisor: float = None,
        currency: Union[Currency, str] = None,
        quote_currency: Union[Currency, str] = None,
        index_initial_price: float = None,
        initial_pricing_date: datetime.date = None,
        expiration_date: datetime.date = None,
        expiration_location: str = None,
        option_style: str = None,
        option_type: Union[OptionType, str] = None,
        settlement_date: datetime.date = None,
        settlement_type: str = None,
        strike_price: float = None,
        put_currency: Union[Currency, str] = None,
        put_amount: float = None,
        automatic_exercise: bool = None,
        call_amount: float = None,
        call_currency: Union[Currency, str] = None,
        exercise_time: str = None,
        multiplier: float = None,
        premium_payment_date: datetime.date = None,
        premium: float = None,
        premium_currency: Union[Currency, str] = None,
        callable: bool = None,
        puttable: bool = None,
        perpetual: bool = None,
        seniority: str = None,
        coupon_type: str = None,
        index: str = None,
        index_term: str = None,
        index_margin: float = None,
        coupon: float = None,
        issue_date: datetime.date = None,
        issuer: str = None,
        issuer_country_code: str = None,
        issuer_type: str = None,
        issue_size: float = None,
        commodity_sector: Union[CommoditySector, str] = None,
        pricing_location: Union[PricingLocation, str] = None,
        contract_months: Tuple[str, ...] = None,
        g10_currency: bool = None,
        hedge_id: str = None,
        ultimate_ticker: str = None,
        strategy: Union[Strategy, str] = None,
        supra_strategy: Union[SupraStrategy, str] = None,
        exchange_currency: Union[Currency, str] = None,
        region: str = None,
        delivery_point: str = None,
        pricing_index: str = None,
        contract_month: str = None,
        load_type: str = None,
        contract_unit: str = None,
        index_create_source: Union[IndexCreateSource, str] = None,
        index_approval_ids: Tuple[str, ...] = None,
        is_pair_basket: bool = None,
        fixed_rate_day_count_fraction: Union[DayCountFraction, str] = None,
        floating_rate_day_count_fraction: Union[DayCountFraction, str] = None,
        pay_day_count_fraction: Union[DayCountFraction, str] = None,
        receive_day_count_fraction: Union[DayCountFraction, str] = None,
        pay_frequency: str = None,
        receive_frequency: str = None,
        resettable_leg: Union[PayReceive, str] = None,
        inflation_lag: str = None,
        fx_index: str = None,
        trade_as: str = None,
        clone_parent_id: str = None,
        on_behalf_of: str = None,
        index_calculation_agent: str = None        
    ):
        super().__init__()
        self.__basket_type = basket_type
        self.__style = style
        self.__index_calculation_type = index_calculation_type
        self.__index_return_type = index_return_type
        self.__index_divisor = index_divisor
        self.__currency = get_enum_value(Currency, currency)
        self.__quote_currency = get_enum_value(Currency, quote_currency)
        self.__index_initial_price = index_initial_price
        self.__initial_pricing_date = initial_pricing_date
        self.__expiration_date = expiration_date
        self.__expiration_location = expiration_location
        self.__option_style = option_style
        self.__option_type = get_enum_value(OptionType, option_type)
        self.__settlement_date = settlement_date
        self.__settlement_type = settlement_type
        self.__strike_price = strike_price
        self.__put_currency = get_enum_value(Currency, put_currency)
        self.__put_amount = put_amount
        self.__automatic_exercise = automatic_exercise
        self.__call_amount = call_amount
        self.__call_currency = get_enum_value(Currency, call_currency)
        self.__exercise_time = exercise_time
        self.__multiplier = multiplier
        self.__premium_payment_date = premium_payment_date
        self.__premium = premium
        self.__premium_currency = get_enum_value(Currency, premium_currency)
        self.__callable = callable
        self.__puttable = puttable
        self.__perpetual = perpetual
        self.__seniority = seniority
        self.__coupon_type = coupon_type
        self.__index = index
        self.__index_term = index_term
        self.__index_margin = index_margin
        self.__coupon = coupon
        self.__issue_date = issue_date
        self.__issuer = issuer
        self.__issuer_country_code = issuer_country_code
        self.__issuer_type = issuer_type
        self.__issue_size = issue_size
        self.__commodity_sector = get_enum_value(CommoditySector, commodity_sector)
        self.__pricing_location = get_enum_value(PricingLocation, pricing_location)
        self.__contract_months = contract_months
        self.__g10_currency = g10_currency
        self.__hedge_id = hedge_id
        self.__ultimate_ticker = ultimate_ticker
        self.__strategy = get_enum_value(Strategy, strategy)
        self.__supra_strategy = get_enum_value(SupraStrategy, supra_strategy)
        self.__exchange_currency = get_enum_value(Currency, exchange_currency)
        self.__region = region
        self.__delivery_point = delivery_point
        self.__pricing_index = pricing_index
        self.__contract_month = contract_month
        self.__load_type = load_type
        self.__contract_unit = contract_unit
        self.__index_create_source = get_enum_value(IndexCreateSource, index_create_source)
        self.__index_approval_ids = index_approval_ids
        self.__is_pair_basket = is_pair_basket
        self.__fixed_rate_day_count_fraction = get_enum_value(DayCountFraction, fixed_rate_day_count_fraction)
        self.__floating_rate_day_count_fraction = get_enum_value(DayCountFraction, floating_rate_day_count_fraction)
        self.__pay_day_count_fraction = get_enum_value(DayCountFraction, pay_day_count_fraction)
        self.__receive_day_count_fraction = get_enum_value(DayCountFraction, receive_day_count_fraction)
        self.__pay_frequency = pay_frequency
        self.__receive_frequency = receive_frequency
        self.__resettable_leg = get_enum_value(PayReceive, resettable_leg)
        self.__inflation_lag = inflation_lag
        self.__fx_index = fx_index
        self.__trade_as = trade_as
        self.__clone_parent_id = clone_parent_id
        self.__on_behalf_of = on_behalf_of
        self.__index_calculation_agent = index_calculation_agent

    @property
    def basket_type(self) -> str:
        """Type of basket / implementation"""
        return self.__basket_type

    @basket_type.setter
    def basket_type(self, value: str):
        self.__basket_type = value
        self._property_changed('basket_type')        

    @property
    def style(self) -> str:
        """Asset style"""
        return self.__style

    @style.setter
    def style(self, value: str):
        self.__style = value
        self._property_changed('style')        

    @property
    def attribution_dataset_id(self) -> str:
        """Identifier of dataset which provides performance attribution data"""
        return 'STSATTR'        

    @property
    def index_calculation_type(self) -> str:
        """Determines the index calculation methodology with respect to dividend reinvestment"""
        return self.__index_calculation_type

    @index_calculation_type.setter
    def index_calculation_type(self, value: str):
        self.__index_calculation_type = value
        self._property_changed('index_calculation_type')        

    @property
    def index_return_type(self) -> str:
        """Determines the return calculation type method with respect to cash accrual / funding"""
        return self.__index_return_type

    @index_return_type.setter
    def index_return_type(self, value: str):
        self.__index_return_type = value
        self._property_changed('index_return_type')        

    @property
    def index_divisor(self) -> float:
        """Divisor to be applied to the overall position set of the index"""
        return self.__index_divisor

    @index_divisor.setter
    def index_divisor(self, value: float):
        self.__index_divisor = value
        self._property_changed('index_divisor')        

    @property
    def currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self.__currency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('currency')        

    @property
    def quote_currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__quote_currency

    @quote_currency.setter
    def quote_currency(self, value: Union[Currency, str]):
        self.__quote_currency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('quote_currency')        

    @property
    def index_initial_price(self) -> float:
        """Initial Price for the Index"""
        return self.__index_initial_price

    @index_initial_price.setter
    def index_initial_price(self, value: float):
        self.__index_initial_price = value
        self._property_changed('index_initial_price')        

    @property
    def initial_pricing_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__initial_pricing_date

    @initial_pricing_date.setter
    def initial_pricing_date(self, value: datetime.date):
        self.__initial_pricing_date = value
        self._property_changed('initial_pricing_date')        

    @property
    def expiration_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, value: datetime.date):
        self.__expiration_date = value
        self._property_changed('expiration_date')        

    @property
    def expiration_location(self) -> str:
        return self.__expiration_location

    @expiration_location.setter
    def expiration_location(self, value: str):
        self.__expiration_location = value
        self._property_changed('expiration_location')        

    @property
    def option_style(self) -> str:
        return self.__option_style

    @option_style.setter
    def option_style(self, value: str):
        self.__option_style = value
        self._property_changed('option_style')        

    @property
    def option_type(self) -> Union[OptionType, str]:
        """Option Type"""
        return self.__option_type

    @option_type.setter
    def option_type(self, value: Union[OptionType, str]):
        self.__option_type = value if isinstance(value, OptionType) else get_enum_value(OptionType, value)
        self._property_changed('option_type')        

    @property
    def settlement_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__settlement_date

    @settlement_date.setter
    def settlement_date(self, value: datetime.date):
        self.__settlement_date = value
        self._property_changed('settlement_date')        

    @property
    def settlement_type(self) -> str:
        return self.__settlement_type

    @settlement_type.setter
    def settlement_type(self, value: str):
        self.__settlement_type = value
        self._property_changed('settlement_type')        

    @property
    def strike_price(self) -> float:
        return self.__strike_price

    @strike_price.setter
    def strike_price(self, value: float):
        self.__strike_price = value
        self._property_changed('strike_price')        

    @property
    def put_currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__put_currency

    @put_currency.setter
    def put_currency(self, value: Union[Currency, str]):
        self.__put_currency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('put_currency')        

    @property
    def put_amount(self) -> float:
        return self.__put_amount

    @put_amount.setter
    def put_amount(self, value: float):
        self.__put_amount = value
        self._property_changed('put_amount')        

    @property
    def automatic_exercise(self) -> bool:
        return self.__automatic_exercise

    @automatic_exercise.setter
    def automatic_exercise(self, value: bool):
        self.__automatic_exercise = value
        self._property_changed('automatic_exercise')        

    @property
    def call_amount(self) -> float:
        return self.__call_amount

    @call_amount.setter
    def call_amount(self, value: float):
        self.__call_amount = value
        self._property_changed('call_amount')        

    @property
    def call_currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__call_currency

    @call_currency.setter
    def call_currency(self, value: Union[Currency, str]):
        self.__call_currency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('call_currency')        

    @property
    def exercise_time(self) -> str:
        """Time at which the asset can be exercised"""
        return self.__exercise_time

    @exercise_time.setter
    def exercise_time(self, value: str):
        self.__exercise_time = value
        self._property_changed('exercise_time')        

    @property
    def multiplier(self) -> float:
        """Underlying unit per asset multiplier"""
        return self.__multiplier

    @multiplier.setter
    def multiplier(self, value: float):
        self.__multiplier = value
        self._property_changed('multiplier')        

    @property
    def premium_payment_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__premium_payment_date

    @premium_payment_date.setter
    def premium_payment_date(self, value: datetime.date):
        self.__premium_payment_date = value
        self._property_changed('premium_payment_date')        

    @property
    def premium(self) -> float:
        return self.__premium

    @premium.setter
    def premium(self, value: float):
        self.__premium = value
        self._property_changed('premium')        

    @property
    def premium_currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__premium_currency

    @premium_currency.setter
    def premium_currency(self, value: Union[Currency, str]):
        self.__premium_currency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('premium_currency')        

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
    def coupon_type(self) -> str:
        """The coupon type of the bond"""
        return self.__coupon_type

    @coupon_type.setter
    def coupon_type(self, value: str):
        self.__coupon_type = value
        self._property_changed('coupon_type')        

    @property
    def index(self) -> str:
        """The rate index (e.g. USD-LIBOR-BBA) for the floating rate coupon of this bond"""
        return self.__index

    @index.setter
    def index(self, value: str):
        self.__index = value
        self._property_changed('index')        

    @property
    def index_term(self) -> str:
        """The term of rate index (e.g. USD-LIBOR-BBA) for the floating rate coupon of this bond"""
        return self.__index_term

    @index_term.setter
    def index_term(self, value: str):
        self.__index_term = value
        self._property_changed('index_term')        

    @property
    def index_margin(self) -> float:
        """The spread over the rate index (e.g. USD-LIBOR-BBA) for the floating rate coupon of this bond"""
        return self.__index_margin

    @index_margin.setter
    def index_margin(self, value: float):
        self.__index_margin = value
        self._property_changed('index_margin')        

    @property
    def coupon(self) -> float:
        """The fixed coupon for this bond"""
        return self.__coupon

    @coupon.setter
    def coupon(self, value: float):
        self.__coupon = value
        self._property_changed('coupon')        

    @property
    def issue_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__issue_date

    @issue_date.setter
    def issue_date(self, value: datetime.date):
        self.__issue_date = value
        self._property_changed('issue_date')        

    @property
    def issuer(self) -> str:
        """The issuer of this bond"""
        return self.__issuer

    @issuer.setter
    def issuer(self, value: str):
        self.__issuer = value
        self._property_changed('issuer')        

    @property
    def issuer_country_code(self) -> str:
        """The country code (ISO 3166) in which this bond was issued"""
        return self.__issuer_country_code

    @issuer_country_code.setter
    def issuer_country_code(self, value: str):
        self.__issuer_country_code = value
        self._property_changed('issuer_country_code')        

    @property
    def issuer_type(self) -> str:
        """The type of the bond issuer"""
        return self.__issuer_type

    @issuer_type.setter
    def issuer_type(self, value: str):
        self.__issuer_type = value
        self._property_changed('issuer_type')        

    @property
    def issue_size(self) -> float:
        """The notional issue size of the bond"""
        return self.__issue_size

    @issue_size.setter
    def issue_size(self, value: float):
        self.__issue_size = value
        self._property_changed('issue_size')        

    @property
    def commodity_sector(self) -> Union[CommoditySector, str]:
        """The sector of the commodity"""
        return self.__commodity_sector

    @commodity_sector.setter
    def commodity_sector(self, value: Union[CommoditySector, str]):
        self.__commodity_sector = value if isinstance(value, CommoditySector) else get_enum_value(CommoditySector, value)
        self._property_changed('commodity_sector')        

    @property
    def pricing_location(self) -> Union[PricingLocation, str]:
        """Based on the location of the exchange. Called 'Native Region' in SecDB"""
        return self.__pricing_location

    @pricing_location.setter
    def pricing_location(self, value: Union[PricingLocation, str]):
        self.__pricing_location = value if isinstance(value, PricingLocation) else get_enum_value(PricingLocation, value)
        self._property_changed('pricing_location')        

    @property
    def contract_months(self) -> Tuple[str, ...]:
        """Contract months"""
        return self.__contract_months

    @contract_months.setter
    def contract_months(self, value: Tuple[str, ...]):
        self.__contract_months = value
        self._property_changed('contract_months')        

    @property
    def g10_currency(self) -> bool:
        """Is a G10 asset."""
        return self.__g10_currency

    @g10_currency.setter
    def g10_currency(self, value: bool):
        self.__g10_currency = value
        self._property_changed('g10_currency')        

    @property
    def hedge_id(self) -> str:
        """Marquee unique identifier"""
        return self.__hedge_id

    @hedge_id.setter
    def hedge_id(self, value: str):
        self.__hedge_id = value
        self._property_changed('hedge_id')        

    @property
    def ultimate_ticker(self) -> str:
        """The ultimate ticker for this security (e.g. SPXW)"""
        return self.__ultimate_ticker

    @ultimate_ticker.setter
    def ultimate_ticker(self, value: str):
        self.__ultimate_ticker = value
        self._property_changed('ultimate_ticker')        

    @property
    def strategy(self) -> Union[Strategy, str]:
        """More specific descriptor of a fund's investment approach. Same view permissions as the asset"""
        return self.__strategy

    @strategy.setter
    def strategy(self, value: Union[Strategy, str]):
        self.__strategy = value if isinstance(value, Strategy) else get_enum_value(Strategy, value)
        self._property_changed('strategy')        

    @property
    def supra_strategy(self) -> Union[SupraStrategy, str]:
        """Broad descriptor of a fund's investment approach. Same view permissions as the asset"""
        return self.__supra_strategy

    @supra_strategy.setter
    def supra_strategy(self, value: Union[SupraStrategy, str]):
        self.__supra_strategy = value if isinstance(value, SupraStrategy) else get_enum_value(SupraStrategy, value)
        self._property_changed('supra_strategy')        

    @property
    def exchange_currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__exchange_currency

    @exchange_currency.setter
    def exchange_currency(self, value: Union[Currency, str]):
        self.__exchange_currency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('exchange_currency')        

    @property
    def region(self) -> str:
        return self.__region

    @region.setter
    def region(self, value: str):
        self.__region = value
        self._property_changed('region')        

    @property
    def delivery_point(self) -> str:
        return self.__delivery_point

    @delivery_point.setter
    def delivery_point(self, value: str):
        self.__delivery_point = value
        self._property_changed('delivery_point')        

    @property
    def pricing_index(self) -> str:
        return self.__pricing_index

    @pricing_index.setter
    def pricing_index(self, value: str):
        self.__pricing_index = value
        self._property_changed('pricing_index')        

    @property
    def contract_month(self) -> str:
        return self.__contract_month

    @contract_month.setter
    def contract_month(self, value: str):
        self.__contract_month = value
        self._property_changed('contract_month')        

    @property
    def load_type(self) -> str:
        return self.__load_type

    @load_type.setter
    def load_type(self, value: str):
        self.__load_type = value
        self._property_changed('load_type')        

    @property
    def contract_unit(self) -> str:
        return self.__contract_unit

    @contract_unit.setter
    def contract_unit(self, value: str):
        self.__contract_unit = value
        self._property_changed('contract_unit')        

    @property
    def index_create_source(self) -> Union[IndexCreateSource, str]:
        """Source of basket create"""
        return self.__index_create_source

    @index_create_source.setter
    def index_create_source(self, value: Union[IndexCreateSource, str]):
        self.__index_create_source = value if isinstance(value, IndexCreateSource) else get_enum_value(IndexCreateSource, value)
        self._property_changed('index_create_source')        

    @property
    def index_approval_ids(self) -> Tuple[str, ...]:
        """Array of approval identifiers related to the object"""
        return self.__index_approval_ids

    @index_approval_ids.setter
    def index_approval_ids(self, value: Tuple[str, ...]):
        self.__index_approval_ids = value
        self._property_changed('index_approval_ids')        

    @property
    def is_pair_basket(self) -> bool:
        return self.__is_pair_basket

    @is_pair_basket.setter
    def is_pair_basket(self, value: bool):
        self.__is_pair_basket = value
        self._property_changed('is_pair_basket')        

    @property
    def fixed_rate_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """Default day count fraction for fixed legs"""
        return self.__fixed_rate_day_count_fraction

    @fixed_rate_day_count_fraction.setter
    def fixed_rate_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self.__fixed_rate_day_count_fraction = value if isinstance(value, DayCountFraction) else get_enum_value(DayCountFraction, value)
        self._property_changed('fixed_rate_day_count_fraction')        

    @property
    def floating_rate_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """Default day count fraction for floating legs"""
        return self.__floating_rate_day_count_fraction

    @floating_rate_day_count_fraction.setter
    def floating_rate_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self.__floating_rate_day_count_fraction = value if isinstance(value, DayCountFraction) else get_enum_value(DayCountFraction, value)
        self._property_changed('floating_rate_day_count_fraction')        

    @property
    def pay_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """Default day count fraction for pay leg"""
        return self.__pay_day_count_fraction

    @pay_day_count_fraction.setter
    def pay_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self.__pay_day_count_fraction = value if isinstance(value, DayCountFraction) else get_enum_value(DayCountFraction, value)
        self._property_changed('pay_day_count_fraction')        

    @property
    def receive_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """Default day count fraction for the receive leg"""
        return self.__receive_day_count_fraction

    @receive_day_count_fraction.setter
    def receive_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self.__receive_day_count_fraction = value if isinstance(value, DayCountFraction) else get_enum_value(DayCountFraction, value)
        self._property_changed('receive_day_count_fraction')        

    @property
    def pay_frequency(self) -> str:
        """Default frequency of the pay leg"""
        return self.__pay_frequency

    @pay_frequency.setter
    def pay_frequency(self, value: str):
        self.__pay_frequency = value
        self._property_changed('pay_frequency')        

    @property
    def receive_frequency(self) -> str:
        """Default frequency of the receive leg"""
        return self.__receive_frequency

    @receive_frequency.setter
    def receive_frequency(self, value: str):
        self.__receive_frequency = value
        self._property_changed('receive_frequency')        

    @property
    def resettable_leg(self) -> Union[PayReceive, str]:
        """Resettable leg"""
        return self.__resettable_leg

    @resettable_leg.setter
    def resettable_leg(self, value: Union[PayReceive, str]):
        self.__resettable_leg = value if isinstance(value, PayReceive) else get_enum_value(PayReceive, value)
        self._property_changed('resettable_leg')        

    @property
    def inflation_lag(self) -> str:
        """Inflation lag"""
        return self.__inflation_lag

    @inflation_lag.setter
    def inflation_lag(self, value: str):
        self.__inflation_lag = value
        self._property_changed('inflation_lag')        

    @property
    def fx_index(self) -> str:
        """FX index"""
        return self.__fx_index

    @fx_index.setter
    def fx_index(self, value: str):
        self.__fx_index = value
        self._property_changed('fx_index')        

    @property
    def trade_as(self) -> str:
        """How to trade the Option."""
        return self.__trade_as

    @trade_as.setter
    def trade_as(self, value: str):
        self.__trade_as = value
        self._property_changed('trade_as')        

    @property
    def clone_parent_id(self) -> str:
        """Marquee unique identifier"""
        return self.__clone_parent_id

    @clone_parent_id.setter
    def clone_parent_id(self, value: str):
        self.__clone_parent_id = value
        self._property_changed('clone_parent_id')        

    @property
    def on_behalf_of(self) -> str:
        """Marquee unique identifier"""
        return self.__on_behalf_of

    @on_behalf_of.setter
    def on_behalf_of(self, value: str):
        self.__on_behalf_of = value
        self._property_changed('on_behalf_of')        

    @property
    def index_calculation_agent(self) -> str:
        """Calculation agent of the index."""
        return self.__index_calculation_agent

    @index_calculation_agent.setter
    def index_calculation_agent(self, value: str):
        self.__index_calculation_agent = value
        self._property_changed('index_calculation_agent')        


class AssetStats(Base):
        
    """Performance statistics."""
       
    def __init__(
        self,
        last_updated_time: datetime.datetime = None,
        period: Union[AssetStatsPeriod, str] = None,
        type: Union[AssetStatsType, str] = None,
        stats: PerformanceStats = None        
    ):
        super().__init__()
        self.__last_updated_time = last_updated_time
        self.__period = get_enum_value(AssetStatsPeriod, period)
        self.__type = get_enum_value(AssetStatsType, type)
        self.__stats = stats

    @property
    def last_updated_time(self) -> datetime.datetime:
        return self.__last_updated_time

    @last_updated_time.setter
    def last_updated_time(self, value: datetime.datetime):
        self.__last_updated_time = value
        self._property_changed('last_updated_time')        

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
       
    def __init__(
        self,
        last_updated_time: DateRange = None,
        period: Union[AssetStatsPeriod, str] = None,
        type: Union[AssetStatsType, str] = None,
        stats: PerformanceStatsRequest = None        
    ):
        super().__init__()
        self.__last_updated_time = last_updated_time
        self.__period = get_enum_value(AssetStatsPeriod, period)
        self.__type = get_enum_value(AssetStatsType, type)
        self.__stats = stats

    @property
    def last_updated_time(self) -> DateRange:
        return self.__last_updated_time

    @last_updated_time.setter
    def last_updated_time(self, value: DateRange):
        self.__last_updated_time = value
        self._property_changed('last_updated_time')        

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
       
    def __init__(
        self,
        infra: str,
        field_history: Tuple[dict, ...]        
    ):
        super().__init__()
        self.__infra = infra
        self.__field_history = field_history

    @property
    def infra(self) -> str:
        return self.__infra

    @infra.setter
    def infra(self, value: str):
        self.__infra = value
        self._property_changed('infra')        

    @property
    def field_history(self) -> Tuple[dict, ...]:
        return self.__field_history

    @field_history.setter
    def field_history(self, value: Tuple[dict, ...]):
        self.__field_history = value
        self._property_changed('field_history')        


class HedgeFundParameters(Base):
        
    """Asset parameters specific to hedge funds"""
       
    def __init__(
        self,
        aum: float = None,
        strategy_aum: float = None,
        aum_range: NumberRange = None,
        strategy_aum_range: NumberRange = None,
        disclaimers: str = None,
        market_cap_category: Tuple[str, ...] = None,
        marketing_status: str = None,
        preferences: dict = None,
        regional_focus: Tuple[str, ...] = None,
        risk_taking_model: str = None,
        strategy: Union[Strategy, str] = None,
        supra_strategy: Union[SupraStrategy, str] = None,
        strategy_description: str = None,
        targeted_gross_exposure: NumberRange = None,
        targeted_net_exposure: NumberRange = None,
        targeted_num_of_positions_short: NumberRange = None,
        targeted_num_of_positions_long: NumberRange = None,
        turnover: str = None,
        vehicle_type: str = None,
        net_exposure_classification: Union[NetExposureClassification, str] = None        
    ):
        super().__init__()
        self.__aum = aum
        self.__strategy_aum = strategy_aum
        self.__aum_range = aum_range
        self.__strategy_aum_range = strategy_aum_range
        self.__disclaimers = disclaimers
        self.__market_cap_category = market_cap_category
        self.__marketing_status = marketing_status
        self.__preferences = preferences
        self.__regional_focus = regional_focus
        self.__risk_taking_model = risk_taking_model
        self.__strategy = get_enum_value(Strategy, strategy)
        self.__supra_strategy = get_enum_value(SupraStrategy, supra_strategy)
        self.__strategy_description = strategy_description
        self.__targeted_gross_exposure = targeted_gross_exposure
        self.__targeted_net_exposure = targeted_net_exposure
        self.__targeted_num_of_positions_short = targeted_num_of_positions_short
        self.__targeted_num_of_positions_long = targeted_num_of_positions_long
        self.__turnover = turnover
        self.__vehicle_type = vehicle_type
        self.__net_exposure_classification = get_enum_value(NetExposureClassification, net_exposure_classification)

    @property
    def aum(self) -> float:
        """Current assets under management. Only viewable after having been granted additional access to asset information."""
        return self.__aum

    @aum.setter
    def aum(self, value: float):
        self.__aum = value
        self._property_changed('aum')        

    @property
    def strategy_aum(self) -> float:
        """Total assets under management for this strategy (including comingled fund, managed accounts, and funds of one). Only viewable after having been granted additional access to asset information."""
        return self.__strategy_aum

    @strategy_aum.setter
    def strategy_aum(self, value: float):
        self.__strategy_aum = value
        self._property_changed('strategy_aum')        

    @property
    def aum_range(self) -> NumberRange:
        """Range in which assets under management fall. Same view permissions as the asset."""
        return self.__aum_range

    @aum_range.setter
    def aum_range(self, value: NumberRange):
        self.__aum_range = value
        self._property_changed('aum_range')        

    @property
    def strategy_aum_range(self) -> NumberRange:
        """Range in which assets under management for this strategy fall. Same view permissions as the asset."""
        return self.__strategy_aum_range

    @strategy_aum_range.setter
    def strategy_aum_range(self, value: NumberRange):
        self.__strategy_aum_range = value
        self._property_changed('strategy_aum_range')        

    @property
    def disclaimers(self) -> str:
        """Legal disclaimers for performance data. Same view permissions as the asset."""
        return self.__disclaimers

    @disclaimers.setter
    def disclaimers(self, value: str):
        self.__disclaimers = value
        self._property_changed('disclaimers')        

    @property
    def market_cap_category(self) -> Tuple[str, ...]:
        """Category of market capitalizations a fund is focused on from an investment perspective. Same view permissions as the asset."""
        return self.__market_cap_category

    @market_cap_category.setter
    def market_cap_category(self, value: Tuple[str, ...]):
        self.__market_cap_category = value
        self._property_changed('market_cap_category')        

    @property
    def marketing_status(self) -> str:
        """A fund's posture as to whether it is currently accepting new subscriptions. Same view permissions as the asset."""
        return self.__marketing_status

    @marketing_status.setter
    def marketing_status(self, value: str):
        self.__marketing_status = value
        self._property_changed('marketing_status')        

    @property
    def preferences(self) -> dict:
        """Lists of blacklisted company attributes."""
        return self.__preferences

    @preferences.setter
    def preferences(self, value: dict):
        self.__preferences = value
        self._property_changed('preferences')        

    @property
    def regional_focus(self) -> Tuple[str, ...]:
        """Section of the world a fund is focused on from an investment perspective. Same view permissions as the asset"""
        return self.__regional_focus

    @regional_focus.setter
    def regional_focus(self, value: Tuple[str, ...]):
        self.__regional_focus = value
        self._property_changed('regional_focus')        

    @property
    def risk_taking_model(self) -> str:
        """Number of risk takers a fund has. Same view permissions as the asset"""
        return self.__risk_taking_model

    @risk_taking_model.setter
    def risk_taking_model(self, value: str):
        self.__risk_taking_model = value
        self._property_changed('risk_taking_model')        

    @property
    def strategy(self) -> Union[Strategy, str]:
        """More specific descriptor of a fund's investment approach. Same view permissions as the asset"""
        return self.__strategy

    @strategy.setter
    def strategy(self, value: Union[Strategy, str]):
        self.__strategy = value if isinstance(value, Strategy) else get_enum_value(Strategy, value)
        self._property_changed('strategy')        

    @property
    def supra_strategy(self) -> Union[SupraStrategy, str]:
        """Broad descriptor of a fund's investment approach. Same view permissions as the asset"""
        return self.__supra_strategy

    @supra_strategy.setter
    def supra_strategy(self, value: Union[SupraStrategy, str]):
        self.__supra_strategy = value if isinstance(value, SupraStrategy) else get_enum_value(SupraStrategy, value)
        self._property_changed('supra_strategy')        

    @property
    def strategy_description(self) -> str:
        """Statement explaining a fund's investment approach. Only viewable after having been granted additional access to asset information."""
        return self.__strategy_description

    @strategy_description.setter
    def strategy_description(self, value: str):
        self.__strategy_description = value
        self._property_changed('strategy_description')        

    @property
    def targeted_gross_exposure(self) -> NumberRange:
        """Value of a fund's long positions plus short positions, expressed in percentage terms. Only viewable after having been granted additional access to asset information."""
        return self.__targeted_gross_exposure

    @targeted_gross_exposure.setter
    def targeted_gross_exposure(self, value: NumberRange):
        self.__targeted_gross_exposure = value
        self._property_changed('targeted_gross_exposure')        

    @property
    def targeted_net_exposure(self) -> NumberRange:
        """Value of a fund's long positions minus short positions, expressed in percentage terms. Only viewable after having been granted additional access to asset information."""
        return self.__targeted_net_exposure

    @targeted_net_exposure.setter
    def targeted_net_exposure(self, value: NumberRange):
        self.__targeted_net_exposure = value
        self._property_changed('targeted_net_exposure')        

    @property
    def targeted_num_of_positions_short(self) -> NumberRange:
        """Range of positions the fund typically holds on the short side of its portfolio. Only viewable after having been granted additional access to asset information."""
        return self.__targeted_num_of_positions_short

    @targeted_num_of_positions_short.setter
    def targeted_num_of_positions_short(self, value: NumberRange):
        self.__targeted_num_of_positions_short = value
        self._property_changed('targeted_num_of_positions_short')        

    @property
    def targeted_num_of_positions_long(self) -> NumberRange:
        """Range of positions the fund typically holds on the long side of its portfolio. Only viewable after having been granted additional access to asset information."""
        return self.__targeted_num_of_positions_long

    @targeted_num_of_positions_long.setter
    def targeted_num_of_positions_long(self, value: NumberRange):
        self.__targeted_num_of_positions_long = value
        self._property_changed('targeted_num_of_positions_long')        

    @property
    def turnover(self) -> str:
        """Rate at which a fund replaces its investment holdings. Only viewable after having been granted additional access to asset information."""
        return self.__turnover

    @turnover.setter
    def turnover(self, value: str):
        self.__turnover = value
        self._property_changed('turnover')        

    @property
    def vehicle_type(self) -> str:
        """Type of investment vehicle. Only viewable after having been granted additional access to asset information."""
        return self.__vehicle_type

    @vehicle_type.setter
    def vehicle_type(self, value: str):
        self.__vehicle_type = value
        self._property_changed('vehicle_type')        

    @property
    def net_exposure_classification(self) -> Union[NetExposureClassification, str]:
        """Classification for net exposure of fund."""
        return self.__net_exposure_classification

    @net_exposure_classification.setter
    def net_exposure_classification(self, value: Union[NetExposureClassification, str]):
        self.__net_exposure_classification = value if isinstance(value, NetExposureClassification) else get_enum_value(NetExposureClassification, value)
        self._property_changed('net_exposure_classification')        


class ShareClassParameters(Base):
        
    """Attributes specific to share class assets"""
       
    def __init__(
        self,
        active_liquidity_fee: float = None,
        additional_provisions: str = None,
        benchmark: Benchmark = None,
        class_fees: float = None,
        class_type: str = None,
        early_redemption_fee: float = None,
        expense_ratio_gross: float = None,
        expense_ratio_net: float = None,
        share_class_type: str = None,
        gate: float = None,
        gate_type: str = None,
        hurdle: float = None,
        hurdle_type: str = None,
        investment_manager: str = None,
        investment_type: str = None,
        institutional_share_class: bool = None,
        lockup: float = None,
        lockup_type: str = None,
        management_fee: float = None,
        minimum_subscription: float = None,
        name: str = None,
        number_of_shares: float = None,
        performance_fee: float = None,
        redemption_notice_period: float = None,
        redemption_period: str = None,
        share_class_currency: str = None,
        side_pocket: str = None,
        status: str = None,
        sub_category: str = None,
        term_type: str = None        
    ):
        super().__init__()
        self.__active_liquidity_fee = active_liquidity_fee
        self.__additional_provisions = additional_provisions
        self.__benchmark = benchmark
        self.__class_fees = class_fees
        self.__class_type = class_type
        self.__early_redemption_fee = early_redemption_fee
        self.__expense_ratio_gross = expense_ratio_gross
        self.__expense_ratio_net = expense_ratio_net
        self.__share_class_type = share_class_type
        self.__gate = gate
        self.__gate_type = gate_type
        self.__hurdle = hurdle
        self.__hurdle_type = hurdle_type
        self.__investment_manager = investment_manager
        self.__investment_type = investment_type
        self.__institutional_share_class = institutional_share_class
        self.__lockup = lockup
        self.__lockup_type = lockup_type
        self.__management_fee = management_fee
        self.__minimum_subscription = minimum_subscription
        self.__name = name
        self.__number_of_shares = number_of_shares
        self.__performance_fee = performance_fee
        self.__redemption_notice_period = redemption_notice_period
        self.__redemption_period = redemption_period
        self.__share_class_currency = share_class_currency
        self.__side_pocket = side_pocket
        self.__status = status
        self.__sub_category = sub_category
        self.__term_type = term_type

    @property
    def active_liquidity_fee(self) -> float:
        """Denotes percent active liquidity fee associated with this fund"""
        return self.__active_liquidity_fee

    @active_liquidity_fee.setter
    def active_liquidity_fee(self, value: float):
        self.__active_liquidity_fee = value
        self._property_changed('active_liquidity_fee')        

    @property
    def additional_provisions(self) -> str:
        """Additional details that are relevant to the share class that not captured by the other fields"""
        return self.__additional_provisions

    @additional_provisions.setter
    def additional_provisions(self, value: str):
        self.__additional_provisions = value
        self._property_changed('additional_provisions')        

    @property
    def benchmark(self) -> Benchmark:
        """Reference rate that can based on an absolute value or absolute value + index"""
        return self.__benchmark

    @benchmark.setter
    def benchmark(self, value: Benchmark):
        self.__benchmark = value
        self._property_changed('benchmark')        

    @property
    def class_fees(self) -> float:
        """Annual cost of investing in specific shareclass, expressed in basis points"""
        return self.__class_fees

    @class_fees.setter
    def class_fees(self, value: float):
        self.__class_fees = value
        self._property_changed('class_fees')        

    @property
    def class_type(self) -> str:
        """For example: B, C, Offshore, Offshore - A, etc"""
        return self.__class_type

    @class_type.setter
    def class_type(self, value: str):
        self.__class_type = value
        self._property_changed('class_type')        

    @property
    def early_redemption_fee(self) -> float:
        """Fee an investor pays to redeem before the expiry of a soft lock-up"""
        return self.__early_redemption_fee

    @early_redemption_fee.setter
    def early_redemption_fee(self, value: float):
        self.__early_redemption_fee = value
        self._property_changed('early_redemption_fee')        

    @property
    def expense_ratio_gross(self) -> float:
        """Gross expense ratio of the shareclass"""
        return self.__expense_ratio_gross

    @expense_ratio_gross.setter
    def expense_ratio_gross(self, value: float):
        self.__expense_ratio_gross = value
        self._property_changed('expense_ratio_gross')        

    @property
    def expense_ratio_net(self) -> float:
        """Net expense ratio of the shareclass"""
        return self.__expense_ratio_net

    @expense_ratio_net.setter
    def expense_ratio_net(self, value: float):
        self.__expense_ratio_net = value
        self._property_changed('expense_ratio_net')        

    @property
    def share_class_type(self) -> str:
        """Must be Money Market, Equity, or Fixed Income"""
        return self.__share_class_type

    @share_class_type.setter
    def share_class_type(self, value: str):
        self.__share_class_type = value
        self._property_changed('share_class_type')        

    @property
    def gate(self) -> float:
        """Limit to the amount of capital that can be redeemed from a fund"""
        return self.__gate

    @gate.setter
    def gate(self, value: float):
        self.__gate = value
        self._property_changed('gate')        

    @property
    def gate_type(self) -> str:
        """Category that gate relates to"""
        return self.__gate_type

    @gate_type.setter
    def gate_type(self, value: str):
        self.__gate_type = value
        self._property_changed('gate_type')        

    @property
    def hurdle(self) -> float:
        """Minimum rate of return a fund must generate before it collects a performance fee"""
        return self.__hurdle

    @hurdle.setter
    def hurdle(self, value: float):
        self.__hurdle = value
        self._property_changed('hurdle')        

    @property
    def hurdle_type(self) -> str:
        """Determines if the hurdle is calculated on all profits above hurdle rate"""
        return self.__hurdle_type

    @hurdle_type.setter
    def hurdle_type(self, value: str):
        self.__hurdle_type = value
        self._property_changed('hurdle_type')        

    @property
    def investment_manager(self) -> str:
        """Goldman Sachs, Blackrock Liquidity"""
        return self.__investment_manager

    @investment_manager.setter
    def investment_manager(self, value: str):
        self.__investment_manager = value
        self._property_changed('investment_manager')        

    @property
    def investment_type(self) -> str:
        """Government, Prime Institutional"""
        return self.__investment_type

    @investment_type.setter
    def investment_type(self, value: str):
        self.__investment_type = value
        self._property_changed('investment_type')        

    @property
    def institutional_share_class(self) -> bool:
        """User to identify if this is the largest and cheapest share class"""
        return self.__institutional_share_class

    @institutional_share_class.setter
    def institutional_share_class(self, value: bool):
        self.__institutional_share_class = value
        self._property_changed('institutional_share_class')        

    @property
    def lockup(self) -> float:
        """Number of months an investor is not allowed to redeem investment"""
        return self.__lockup

    @lockup.setter
    def lockup(self, value: float):
        self.__lockup = value
        self._property_changed('lockup')        

    @property
    def lockup_type(self) -> str:
        """Classification of lockup"""
        return self.__lockup_type

    @lockup_type.setter
    def lockup_type(self, value: str):
        self.__lockup_type = value
        self._property_changed('lockup_type')        

    @property
    def management_fee(self) -> float:
        """Percent fee paid by investor to compensate manager for the cost of managing their assets"""
        return self.__management_fee

    @management_fee.setter
    def management_fee(self, value: float):
        self.__management_fee = value
        self._property_changed('management_fee')        

    @property
    def minimum_subscription(self) -> float:
        """Lowest level of investment a fund will accept"""
        return self.__minimum_subscription

    @minimum_subscription.setter
    def minimum_subscription(self, value: float):
        self.__minimum_subscription = value
        self._property_changed('minimum_subscription')        

    @property
    def name(self) -> str:
        """Identifier for particular share class"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def number_of_shares(self) -> float:
        """Number of shares in the share class"""
        return self.__number_of_shares

    @number_of_shares.setter
    def number_of_shares(self, value: float):
        self.__number_of_shares = value
        self._property_changed('number_of_shares')        

    @property
    def performance_fee(self) -> float:
        """Fee paid by investor to compensate manager for generating positive returns or alpha"""
        return self.__performance_fee

    @performance_fee.setter
    def performance_fee(self, value: float):
        self.__performance_fee = value
        self._property_changed('performance_fee')        

    @property
    def redemption_notice_period(self) -> float:
        """Number of days prior to a redemption that an investor must notify a manager of their intent"""
        return self.__redemption_notice_period

    @redemption_notice_period.setter
    def redemption_notice_period(self, value: float):
        self.__redemption_notice_period = value
        self._property_changed('redemption_notice_period')        

    @property
    def redemption_period(self) -> str:
        """Frequency on which an investor can redeem from a fund"""
        return self.__redemption_period

    @redemption_period.setter
    def redemption_period(self, value: str):
        self.__redemption_period = value
        self._property_changed('redemption_period')        

    @property
    def share_class_currency(self) -> str:
        """Currency of the share class"""
        return self.__share_class_currency

    @share_class_currency.setter
    def share_class_currency(self, value: str):
        self.__share_class_currency = value
        self._property_changed('share_class_currency')        

    @property
    def side_pocket(self) -> str:
        """Account utilized to separate illiquid assets from more liquid investments"""
        return self.__side_pocket

    @side_pocket.setter
    def side_pocket(self, value: str):
        self.__side_pocket = value
        self._property_changed('side_pocket')        

    @property
    def status(self) -> str:
        """Denotes whether the share class is currently accepting new subscriptions"""
        return self.__status

    @status.setter
    def status(self, value: str):
        self.__status = value
        self._property_changed('status')        

    @property
    def sub_category(self) -> str:
        """Subtype of what funds invest in within each SEC category """
        return self.__sub_category

    @sub_category.setter
    def sub_category(self, value: str):
        self.__sub_category = value
        self._property_changed('sub_category')        

    @property
    def term_type(self) -> str:
        """category that describes share class offering"""
        return self.__term_type

    @term_type.setter
    def term_type(self, value: str):
        self.__term_type = value
        self._property_changed('term_type')        


class TemporalPeople(Base):
        
    """People associated with an asset during a certain date range"""
       
    def __init__(
        self,
        start_date: datetime.date = None,
        end_date: datetime.date = None,
        people: People = None        
    ):
        super().__init__()
        self.__start_date = start_date
        self.__end_date = end_date
        self.__people = people

    @property
    def start_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__start_date

    @start_date.setter
    def start_date(self, value: datetime.date):
        self.__start_date = value
        self._property_changed('start_date')        

    @property
    def end_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__end_date

    @end_date.setter
    def end_date(self, value: datetime.date):
        self.__end_date = value
        self._property_changed('end_date')        

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
       
    def __init__(
        self,
        asset_class: Union[AssetClass, str],
        type: Union[AssetType, str],
        name: str,
        created_by_id: str = None,
        created_time: datetime.datetime = None,
        currency: Union[Currency, str] = None,
        description: str = None,
        entitlements: Entitlements = None,
        entitlement_exclusions: EntitlementExclusions = None,
        exchange: str = None,
        id: str = None,
        identifiers: Tuple[Identifier, ...] = None,
        last_updated_by_id: str = None,
        last_updated_time: datetime.datetime = None,
        listed: bool = None,
        live_date: datetime.date = None,
        owner_id: str = None,
        parameters: dict = None,
        asset_stats: Tuple[AssetStats, ...] = None,
        people: People = None,
        region: Union[Region, str] = None,
        report_ids: Tuple[str, ...] = None,
        short_name: str = None,
        styles: Tuple[str, ...] = None,
        tags: Tuple[str, ...] = None,
        underlying_asset_ids: Tuple[str, ...] = None        
    ):
        super().__init__()
        self.__asset_class = get_enum_value(AssetClass, asset_class)
        self.__created_by_id = created_by_id
        self.__created_time = created_time
        self.__currency = get_enum_value(Currency, currency)
        self.__description = description
        self.__entitlements = entitlements
        self.__entitlement_exclusions = entitlement_exclusions
        self.__exchange = exchange
        self.__id = id
        self.__identifiers = identifiers
        self.__last_updated_by_id = last_updated_by_id
        self.__last_updated_time = last_updated_time
        self.__listed = listed
        self.__live_date = live_date
        self.__name = name
        self.__owner_id = owner_id
        self.__parameters = parameters
        self.__asset_stats = asset_stats
        self.__people = people
        self.__region = get_enum_value(Region, region)
        self.__report_ids = report_ids
        self.__short_name = short_name
        self.__styles = styles
        self.__tags = tags
        self.__type = get_enum_value(AssetType, type)
        self.__underlying_asset_ids = underlying_asset_ids

    @property
    def asset_class(self) -> Union[AssetClass, str]:
        """Asset classification of security. Assets are classified into broad groups which exhibit similar characteristics and behave in a consistent way under different market conditions"""
        return self.__asset_class

    @asset_class.setter
    def asset_class(self, value: Union[AssetClass, str]):
        self.__asset_class = value if isinstance(value, AssetClass) else get_enum_value(AssetClass, value)
        self._property_changed('asset_class')        

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
    def entitlement_exclusions(self) -> EntitlementExclusions:
        """Defines the exclusion entitlements of a given resource"""
        return self.__entitlement_exclusions

    @entitlement_exclusions.setter
    def entitlement_exclusions(self, value: EntitlementExclusions):
        self.__entitlement_exclusions = value
        self._property_changed('entitlement_exclusions')        

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
    def listed(self) -> bool:
        """Whether the asset is currently listed or not"""
        return self.__listed

    @listed.setter
    def listed(self, value: bool):
        self.__listed = value
        self._property_changed('listed')        

    @property
    def live_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__live_date

    @live_date.setter
    def live_date(self, value: datetime.date):
        self.__live_date = value
        self._property_changed('live_date')        

    @property
    def name(self) -> str:
        """Display name of the asset"""
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
    def parameters(self) -> dict:
        return self.__parameters

    @parameters.setter
    def parameters(self, value: dict):
        self.__parameters = value
        self._property_changed('parameters')        

    @property
    def asset_stats(self) -> Tuple[AssetStats, ...]:
        """Performance statistics."""
        return self.__asset_stats

    @asset_stats.setter
    def asset_stats(self, value: Tuple[AssetStats, ...]):
        self.__asset_stats = value
        self._property_changed('asset_stats')        

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
    def report_ids(self) -> Tuple[str, ...]:
        """Array of report identifiers related to the object"""
        return self.__report_ids

    @report_ids.setter
    def report_ids(self, value: Tuple[str, ...]):
        self.__report_ids = value
        self._property_changed('report_ids')        

    @property
    def short_name(self) -> str:
        """Short name or alias for the asset"""
        return self.__short_name

    @short_name.setter
    def short_name(self, value: str):
        self.__short_name = value
        self._property_changed('short_name')        

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
    def underlying_asset_ids(self) -> Tuple[str, ...]:
        """Underlying asset ids"""
        return self.__underlying_asset_ids

    @underlying_asset_ids.setter
    def underlying_asset_ids(self, value: Tuple[str, ...]):
        self.__underlying_asset_ids = value
        self._property_changed('underlying_asset_ids')        


class EntityQuery(Base):
               
    def __init__(
        self,
        format: Union[Format, str] = None,
        where: FieldFilterMap = None,
        as_of_time: datetime.datetime = None,
        last_updated_since: datetime.datetime = None,
        date: datetime.date = None,
        time: datetime.datetime = None,
        delay: int = None,
        order_by: Tuple[Union[dict, str], ...] = None,
        scroll: str = None,
        scroll_id: str = None,
        fields: Tuple[Union[dict, str], ...] = None,
        limit: int = None,
        offset: int = None        
    ):
        super().__init__()
        self.__format = get_enum_value(Format, format)
        self.__where = where
        self.__as_of_time = as_of_time
        self.__last_updated_since = last_updated_since
        self.__date = date
        self.__time = time
        self.__delay = delay
        self.__order_by = order_by
        self.__scroll = scroll
        self.__scroll_id = scroll_id
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
    def as_of_time(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__as_of_time

    @as_of_time.setter
    def as_of_time(self, value: datetime.datetime):
        self.__as_of_time = value
        self._property_changed('as_of_time')        

    @property
    def last_updated_since(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__last_updated_since

    @last_updated_since.setter
    def last_updated_since(self, value: datetime.datetime):
        self.__last_updated_since = value
        self._property_changed('last_updated_since')        

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
    def order_by(self) -> Tuple[Union[dict, str], ...]:
        return self.__order_by

    @order_by.setter
    def order_by(self, value: Tuple[Union[dict, str], ...]):
        self.__order_by = value
        self._property_changed('order_by')        

    @property
    def scroll(self) -> str:
        """Time for which to keep the scroll search context alive, i.e. 1m (1 minute) or 10s (10 seconds)"""
        return self.__scroll

    @scroll.setter
    def scroll(self, value: str):
        self.__scroll = value
        self._property_changed('scroll')        

    @property
    def scroll_id(self) -> str:
        """Scroll identifier to be used to retrieve the next batch of results"""
        return self.__scroll_id

    @scroll_id.setter
    def scroll_id(self, value: str):
        self.__scroll_id = value
        self._property_changed('scroll_id')        

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
