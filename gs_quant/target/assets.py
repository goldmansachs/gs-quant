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

from gs_quant.target.common import *
import datetime
from typing import Tuple, Union
from enum import Enum
from gs_quant.base import Base, EnumBase, InstrumentBase, camel_case_translate, get_enum_value


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
    Platform = 'Platform'
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
    YTD = 'YTD'
    
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


class ProductType(EnumBase, Enum):    
    
    """Product type of basket"""

    Flow = 'Flow'
    MPS = 'MPS'
    
    def __repr__(self):
        return self.value


class Strategy(EnumBase, Enum):    
    
    """More specific descriptor of a fund's investment approach. Same view permissions
       as the asset"""

    Active_Extension = 'Active Extension'
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
    
    """Broad descriptor of a fund's investment approach. Same view permissions as the
       asset"""

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
        
    @camel_case_translate
    def __init__(
        self,
        risk_country_name: str = None,
        risk_country_code: str = None,
        country_name: str = None,
        country_code: str = None,
        is_primary: bool = None,
        is_country_primary: bool = None,
        gics_sector: str = None,
        gics_industry_group: str = None,
        gics_industry: str = None,
        gics_sub_industry: str = None,
        bbg_industry_sector: str = None,
        bbg_industry_group: str = None,
        bbg_industry_sub_group: str = None,
        rating_moodys: str = None,
        rating_fitch: str = None,
        rating_standard_and_poors: str = None,
        rating_second_highest: str = None,
        rating_linear: float = None,
        commod_template: str = None,
        region: Union[Region, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.risk_country_name = risk_country_name
        self.risk_country_code = risk_country_code
        self.country_name = country_name
        self.country_code = country_code
        self.is_primary = is_primary
        self.is_country_primary = is_country_primary
        self.gics_sector = gics_sector
        self.gics_industry_group = gics_industry_group
        self.gics_industry = gics_industry
        self.gics_sub_industry = gics_sub_industry
        self.bbg_industry_sector = bbg_industry_sector
        self.bbg_industry_group = bbg_industry_group
        self.bbg_industry_sub_group = bbg_industry_sub_group
        self.rating_moodys = rating_moodys
        self.rating_fitch = rating_fitch
        self.rating_standard_and_poors = rating_standard_and_poors
        self.rating_second_highest = rating_second_highest
        self.rating_linear = rating_linear
        self.commod_template = commod_template
        self.region = region
        self.name = name

    @property
    def risk_country_name(self) -> str:
        """Risk Country"""
        return self.__risk_country_name

    @risk_country_name.setter
    def risk_country_name(self, value: str):
        self._property_changed('risk_country_name')
        self.__risk_country_name = value        

    @property
    def risk_country_code(self) -> str:
        """Risk Country code (ISO 3166)."""
        return self.__risk_country_code

    @risk_country_code.setter
    def risk_country_code(self, value: str):
        self._property_changed('risk_country_code')
        self.__risk_country_code = value        

    @property
    def country_name(self) -> str:
        """Country name of asset"""
        return self.__country_name

    @country_name.setter
    def country_name(self, value: str):
        self._property_changed('country_name')
        self.__country_name = value        

    @property
    def country_code(self) -> str:
        """Country code (ISO 3166)"""
        return self.__country_code

    @country_code.setter
    def country_code(self, value: str):
        self._property_changed('country_code')
        self.__country_code = value        

    @property
    def is_primary(self) -> bool:
        """Is this the primary exchange listing for the asset"""
        return self.__is_primary

    @is_primary.setter
    def is_primary(self, value: bool):
        self._property_changed('is_primary')
        self.__is_primary = value        

    @property
    def is_country_primary(self) -> bool:
        """Is this the primary exchange listing for the asset given the exchange country"""
        return self.__is_country_primary

    @is_country_primary.setter
    def is_country_primary(self, value: bool):
        self._property_changed('is_country_primary')
        self.__is_country_primary = value        

    @property
    def gics_sector(self) -> str:
        """GICS Sector classification (level 1)"""
        return self.__gics_sector

    @gics_sector.setter
    def gics_sector(self, value: str):
        self._property_changed('gics_sector')
        self.__gics_sector = value        

    @property
    def gics_industry_group(self) -> str:
        """GICS Industry Group classification (level 2)"""
        return self.__gics_industry_group

    @gics_industry_group.setter
    def gics_industry_group(self, value: str):
        self._property_changed('gics_industry_group')
        self.__gics_industry_group = value        

    @property
    def gics_industry(self) -> str:
        """GICS Industry classification (level 3)"""
        return self.__gics_industry

    @gics_industry.setter
    def gics_industry(self, value: str):
        self._property_changed('gics_industry')
        self.__gics_industry = value        

    @property
    def gics_sub_industry(self) -> str:
        """GICS Sub Industry classification (level 4)"""
        return self.__gics_sub_industry

    @gics_sub_industry.setter
    def gics_sub_industry(self, value: str):
        self._property_changed('gics_sub_industry')
        self.__gics_sub_industry = value        

    @property
    def bbg_industry_sector(self) -> str:
        """BBG Industry Sector"""
        return self.__bbg_industry_sector

    @bbg_industry_sector.setter
    def bbg_industry_sector(self, value: str):
        self._property_changed('bbg_industry_sector')
        self.__bbg_industry_sector = value        

    @property
    def bbg_industry_group(self) -> str:
        """BBG Industry Group"""
        return self.__bbg_industry_group

    @bbg_industry_group.setter
    def bbg_industry_group(self, value: str):
        self._property_changed('bbg_industry_group')
        self.__bbg_industry_group = value        

    @property
    def bbg_industry_sub_group(self) -> str:
        """BBG Industry Sub Group"""
        return self.__bbg_industry_sub_group

    @bbg_industry_sub_group.setter
    def bbg_industry_sub_group(self, value: str):
        self._property_changed('bbg_industry_sub_group')
        self.__bbg_industry_sub_group = value        

    @property
    def rating_moodys(self) -> str:
        """Bond rating from Moody's"""
        return self.__rating_moodys

    @rating_moodys.setter
    def rating_moodys(self, value: str):
        self._property_changed('rating_moodys')
        self.__rating_moodys = value        

    @property
    def rating_fitch(self) -> str:
        """Bond rating from Fitch"""
        return self.__rating_fitch

    @rating_fitch.setter
    def rating_fitch(self, value: str):
        self._property_changed('rating_fitch')
        self.__rating_fitch = value        

    @property
    def rating_standard_and_poors(self) -> str:
        """Bond rating from Standard And Poor's"""
        return self.__rating_standard_and_poors

    @rating_standard_and_poors.setter
    def rating_standard_and_poors(self, value: str):
        self._property_changed('rating_standard_and_poors')
        self.__rating_standard_and_poors = value        

    @property
    def rating_second_highest(self) -> str:
        """Second highest bond rating between Moody's, Fitch, and Standard and Poor's"""
        return self.__rating_second_highest

    @rating_second_highest.setter
    def rating_second_highest(self, value: str):
        self._property_changed('rating_second_highest')
        self.__rating_second_highest = value        

    @property
    def rating_linear(self) -> float:
        """Rating of the bond in linear form"""
        return self.__rating_linear

    @rating_linear.setter
    def rating_linear(self, value: float):
        self._property_changed('rating_linear')
        self.__rating_linear = value        

    @property
    def commod_template(self) -> str:
        """Commodities generic template, i.e. Heating Oil"""
        return self.__commod_template

    @commod_template.setter
    def commod_template(self, value: str):
        self._property_changed('commod_template')
        self.__commod_template = value        

    @property
    def region(self) -> Union[Region, str]:
        """Regional classification for the asset"""
        return self.__region

    @region.setter
    def region(self, value: Union[Region, str]):
        self._property_changed('region')
        self.__region = get_enum_value(Region, value)        


class AssetToInstrumentResponse(Base):
        
    """Resolution of assetId to instrument"""

    @camel_case_translate
    def __init__(
        self,
        asset_id: str,
        name: str,
        instrument: InstrumentBase,
        size_field: str
    ):        
        super().__init__()
        self.asset_id = asset_id
        self.name = name
        self.instrument = instrument
        self.size_field = size_field

    @property
    def asset_id(self) -> str:
        """Marquee unique asset identifier."""
        return self.__asset_id

    @asset_id.setter
    def asset_id(self, value: str):
        self._property_changed('asset_id')
        self.__asset_id = value        

    @property
    def name(self) -> str:
        """Display name of the asset"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def instrument(self) -> InstrumentBase:
        """Derivative instruments"""
        return self.__instrument

    @instrument.setter
    def instrument(self, value: InstrumentBase):
        self._property_changed('instrument')
        self.__instrument = value        

    @property
    def size_field(self) -> str:
        """Size field."""
        return self.__size_field

    @size_field.setter
    def size_field(self, value: str):
        self._property_changed('size_field')
        self.__size_field = value        


class Benchmark(Base):
        
    """Reference rate that can based on an absolute value or absolute value + index"""

    @camel_case_translate
    def __init__(
        self,
        asset_id: str = None,
        value: float = None,
        name: str = None
    ):        
        super().__init__()
        self.asset_id = asset_id
        self.value = value
        self.name = name

    @property
    def asset_id(self) -> str:
        """Asset for rate index"""
        return self.__asset_id

    @asset_id.setter
    def asset_id(self, value: str):
        self._property_changed('asset_id')
        self.__asset_id = value        

    @property
    def value(self) -> float:
        """Absolute value for reference rate"""
        return self.__value

    @value.setter
    def value(self, value: float):
        self._property_changed('value')
        self.__value = value        

    @property
    def name(self) -> str:
        """Name of an asset if assetId cannot be provided"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        


class CommodityEUNaturalGasHub(Base):
        
    """Commodity Natural Gas hub asset in EU NG market for which the prices are
       published"""

    @camel_case_translate
    def __init__(
        self,
        region: str = None,
        hub_type: str = None,
        name: str = None
    ):        
        super().__init__()
        self.region = region
        self.hub_type = hub_type
        self.name = name

    @property
    def region(self) -> str:
        """Geographical Region"""
        return self.__region

    @region.setter
    def region(self, value: str):
        self._property_changed('region')
        self.__region = value        

    @property
    def hub_type(self) -> str:
        """Type of hub - virtual or physical"""
        return self.__hub_type

    @hub_type.setter
    def hub_type(self, value: str):
        self._property_changed('hub_type')
        self.__hub_type = value        


class CommodityNaturalGasHub(Base):
        
    """Commodity Natural Gas hub represents a distinct location in natural gas markets"""

    @camel_case_translate
    def __init__(
        self,
        region: str = None,
        pipelines: Tuple[str, ...] = None,
        platts_codes: Tuple[str, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.region = region
        self.pipelines = pipelines
        self.platts_codes = platts_codes
        self.name = name

    @property
    def region(self) -> str:
        """Natural Gas Region"""
        return self.__region

    @region.setter
    def region(self, value: str):
        self._property_changed('region')
        self.__region = value        

    @property
    def pipelines(self) -> Tuple[str, ...]:
        """All natural gas pipelines this hub exists on"""
        return self.__pipelines

    @pipelines.setter
    def pipelines(self, value: Tuple[str, ...]):
        self._property_changed('pipelines')
        self.__pipelines = value        

    @property
    def platts_codes(self) -> Tuple[str, ...]:
        """All platts codes associated with this hub"""
        return self.__platts_codes

    @platts_codes.setter
    def platts_codes(self, value: Tuple[str, ...]):
        self._property_changed('platts_codes')
        self.__platts_codes = value        


class CommodityPowerAggregatedNodes(Base):
        
    """Commodity power aggregated node represents a group of locations in power markets
       e.g. zone or hub."""

    @camel_case_translate
    def __init__(
        self,
        ISO: str = None,
        aggregate_type: str = None,
        location_name: str = None,
        name: str = None
    ):        
        super().__init__()
        self.ISO = ISO
        self.aggregate_type = aggregate_type
        self.location_name = location_name
        self.name = name

    @property
    def ISO(self) -> str:
        """Independent system operator"""
        return self.__ISO

    @ISO.setter
    def ISO(self, value: str):
        self._property_changed('ISO')
        self.__ISO = value        

    @property
    def aggregate_type(self) -> str:
        """Aggregate type of nodes within the ISO."""
        return self.__aggregate_type

    @aggregate_type.setter
    def aggregate_type(self, value: str):
        self._property_changed('aggregate_type')
        self.__aggregate_type = value        

    @property
    def location_name(self) -> str:
        """Location within the ISO"""
        return self.__location_name

    @location_name.setter
    def location_name(self, value: str):
        self._property_changed('location_name')
        self.__location_name = value        


class CommodityPowerNode(Base):
        
    """Commodity power node represents a distinct location in power markets"""

    @camel_case_translate
    def __init__(
        self,
        ISO: str = None,
        location_name: str = None,
        name: str = None
    ):        
        super().__init__()
        self.ISO = ISO
        self.location_name = location_name
        self.name = name

    @property
    def ISO(self) -> str:
        """Independent system operator"""
        return self.__ISO

    @ISO.setter
    def ISO(self, value: str):
        self._property_changed('ISO')
        self.__ISO = value        

    @property
    def location_name(self) -> str:
        """Location within the ISO"""
        return self.__location_name

    @location_name.setter
    def location_name(self, value: str):
        self._property_changed('location_name')
        self.__location_name = value        


class CommodityReferencePriceParameters(Base):
        
    """Deprecated - Parameters specific to the group used to specify the commodity
       underlier."""

    @camel_case_translate
    def __init__(
        self,
        commodity_base: str = None,
        commodity_details: str = None,
        currency: str = None,
        unit: str = None,
        exchange_id: str = None,
        publication: str = None,
        name: str = None
    ):        
        super().__init__()
        self.commodity_base = commodity_base
        self.commodity_details = commodity_details
        self.currency = currency
        self.unit = unit
        self.exchange_id = exchange_id
        self.publication = publication
        self.name = name

    @property
    def commodity_base(self) -> str:
        """Value to identify the base type of the commodity being traded."""
        return self.__commodity_base

    @commodity_base.setter
    def commodity_base(self, value: str):
        self._property_changed('commodity_base')
        self.__commodity_base = value        

    @property
    def commodity_details(self) -> str:
        """Value to identify the commodity being traded more specifically."""
        return self.__commodity_details

    @commodity_details.setter
    def commodity_details(self, value: str):
        self._property_changed('commodity_details')
        self.__commodity_details = value        

    @property
    def currency(self) -> str:
        """Currency of price."""
        return self.__currency

    @currency.setter
    def currency(self, value: str):
        self._property_changed('currency')
        self.__currency = value        

    @property
    def unit(self) -> str:
        """Unit of measurement of the commodity."""
        return self.__unit

    @unit.setter
    def unit(self, value: str):
        self._property_changed('unit')
        self.__unit = value        

    @property
    def exchange_id(self) -> str:
        """Exchange where that future is listed, if traded by a listed price."""
        return self.__exchange_id

    @exchange_id.setter
    def exchange_id(self, value: str):
        self._property_changed('exchange_id')
        self.__exchange_id = value        

    @property
    def publication(self) -> str:
        """Publication with reference to whose prices commodity is traded."""
        return self.__publication

    @publication.setter
    def publication(self, value: str):
        self._property_changed('publication')
        self.__publication = value        


class DateRange(Base):
        
    @camel_case_translate
    def __init__(
        self,
        end_date: datetime.date = None,
        start_date: datetime.date = None,
        name: str = None
    ):        
        super().__init__()
        self.end_date = end_date
        self.start_date = start_date
        self.name = name

    @property
    def end_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__end_date

    @end_date.setter
    def end_date(self, value: datetime.date):
        self._property_changed('end_date')
        self.__end_date = value        

    @property
    def start_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__start_date

    @start_date.setter
    def start_date(self, value: datetime.date):
        self._property_changed('start_date')
        self.__start_date = value        


class FieldFilterMap(Base):
        
    @camel_case_translate
    def __init__(
        self,
        internal_index_calc_region: dict = None,
        issue_status_date: dict = None,
        pl_id: dict = None,
        last_returns_start_date: dict = None,
        amount_outstanding: dict = None,
        asset_classifications_gics_sub_industry: dict = None,
        mdapi_class: dict = None,
        data_set_ids: dict = None,
        call_first_date: dict = None,
        pb_client_id: dict = None,
        owner_id: dict = None,
        economic_terms_hash: dict = None,
        sec_db: dict = None,
        objective: dict = None,
        simon_intl_asset_tags: dict = None,
        private_placement_type: dict = None,
        hedge_notional: dict = None,
        rank: dict = None,
        data_set_category: dict = None,
        created_by_id: dict = None,
        vehicle_type: dict = None,
        market_data_type: dict = None,
        asset_parameters_payer_day_count_fraction: dict = None,
        point_class: dict = None,
        minimum_increment: dict = None,
        hedge_volatility: dict = None,
        version: dict = None,
        tags: dict = None,
        asset_classifications_gics_industry_group: dict = None,
        market_data_asset: dict = None,
        asset_classifications_is_primary: dict = None,
        styles: dict = None,
        short_name: dict = None,
        eid: dict = None,
        jsn: dict = None,
        mkt_quoting_style: dict = None,
        mic: dict = None,
        ps_id: dict = None,
        issue_status: dict = None,
        region_code: dict = None,
        dollar_cross: dict = None,
        portfolio_type: dict = None,
        vendor: dict = None,
        popularity: dict = None,
        currency: dict = None,
        term: dict = None,
        real_time_restriction_status: dict = None,
        asset_parameters_clearing_house: dict = None,
        rating_fitch: dict = None,
        non_symbol_dimensions: dict = None,
        asset_parameters_floating_rate_designated_maturity: dict = None,
        target_notional: dict = None,
        mkt_class: dict = None,
        delisted: dict = None,
        last_updated_since: dict = None,
        regional_focus: dict = None,
        asset_parameters_payer_designated_maturity: dict = None,
        seasonal_adjustment_short: dict = None,
        asset_parameters_exchange_currency: dict = None,
        asset_classifications_country_name: dict = None,
        management_fee: dict = None,
        rating_moodys: dict = None,
        simon_id: dict = None,
        cusip: dict = None,
        notes: dict = None,
        asset_parameters_floating_rate_option: dict = None,
        internal_index_calc_agent: dict = None,
        rating_second_highest: dict = None,
        asset_classifications_country_code: dict = None,
        frequency: dict = None,
        option_type: dict = None,
        data_set_sub_category: dict = None,
        is_legacy_pair_basket: dict = None,
        issuer_type: dict = None,
        asset_parameters_pricing_location: dict = None,
        plot_id: dict = None,
        asset_parameters_coupon: dict = None,
        data_product: dict = None,
        mq_symbol: dict = None,
        sectors: dict = None,
        multiplier: dict = None,
        asset_parameters_payer_rate_option: dict = None,
        market_data_point: dict = None,
        external: dict = None,
        wpk: dict = None,
        sts_fx_currency: dict = None,
        hedge_annualized_volatility: dict = None,
        name: dict = None,
        asset_parameters_expiration_date: dict = None,
        aum: dict = None,
        exchange: dict = None,
        folder_name: dict = None,
        region: dict = None,
        cid: dict = None,
        onboarded: dict = None,
        live_date: dict = None,
        issue_price: dict = None,
        sink_factor: dict = None,
        underlying_data_set_id: dict = None,
        asset_parameters_payer_frequency: dict = None,
        prime_id: dict = None,
        asset_classifications_gics_sector: dict = None,
        sts_asset_name: dict = None,
        description: dict = None,
        asset_classifications_is_country_primary: dict = None,
        title: dict = None,
        net_exposure_classification: dict = None,
        coupon_type: dict = None,
        last_updated_by_id: dict = None,
        clone_parent_id: dict = None,
        company: dict = None,
        issue_date: dict = None,
        expiration_date: dict = None,
        coverage: dict = None,
        ticker: dict = None,
        asset_parameters_receiver_rate_option: dict = None,
        call_last_date: dict = None,
        sts_rates_country: dict = None,
        latest_execution_time: dict = None,
        asset_parameters_receiver_designated_maturity: dict = None,
        gsn: dict = None,
        gss: dict = None,
        rating_linear: dict = None,
        asset_class: dict = None,
        cm_id: dict = None,
        gsideid: dict = None,
        type_: dict = None,
        mdapi: dict = None,
        ric: dict = None,
        issuer: dict = None,
        position_source_id: dict = None,
        measures: dict = None,
        asset_parameters_floating_rate_day_count_fraction: dict = None,
        action: dict = None,
        id_: dict = None,
        asset_parameters_seniority: dict = None,
        redemption_date: dict = None,
        identifier: dict = None,
        index_create_source: dict = None,
        sec_name: dict = None,
        sub_region: dict = None,
        asset_parameters_receiver_day_count_fraction: dict = None,
        asset_parameters_notional_currency: dict = None,
        sedol: dict = None,
        mkt_asset: dict = None,
        rating_standard_and_poors: dict = None,
        asset_types: dict = None,
        bcid: dict = None,
        gsid: dict = None,
        tdapi: dict = None,
        last_updated_message: dict = None,
        rcic: dict = None,
        trading_restriction: dict = None,
        status: dict = None,
        asset_parameters_pay_or_receive: dict = None,
        name_raw: dict = None,
        asset_classifications_gics_industry: dict = None,
        on_behalf_of: dict = None,
        accrued_interest_standard: dict = None,
        sts_commodity: dict = None,
        sectors_raw: dict = None,
        sts_commodity_sector: dict = None,
        asset_parameters_receiver_frequency: dict = None,
        position_source_name: dict = None,
        gsid_equivalent: dict = None,
        categories: dict = None,
        symbol_dimensions: dict = None,
        ext_mkt_asset: dict = None,
        asset_parameters_fixed_rate_frequency: dict = None,
        coupon: dict = None,
        compliance_restricted_status: dict = None,
        quoting_style: dict = None,
        scenario_group_id: dict = None,
        asset_parameters_issuer_type: dict = None,
        sts_credit_market: dict = None,
        bbid: dict = None,
        asset_classifications_risk_country_code: dict = None,
        sts_em_dm: dict = None,
        issue_size: dict = None,
        returns_enabled: dict = None,
        seniority: dict = None,
        asset_parameters_settlement: dict = None,
        primary_country_ric: dict = None,
        is_pair_basket: dict = None,
        default_backcast: dict = None,
        use_machine_learning: dict = None,
        performance_fee: dict = None,
        report_type: dict = None,
        underlying_asset_ids: dict = None,
        encoded_stats: dict = None,
        pnode_id: dict = None,
        backtest_type: dict = None,
        asset_parameters_issuer: dict = None,
        exchange_code: dict = None,
        asset_parameters_strike: dict = None,
        asset_parameters_termination_date: dict = None,
        resource: dict = None,
        bbid_equivalent: dict = None,
        asset_parameters_effective_date: dict = None,
        valoren: dict = None,
        asset_parameters_fixed_rate_day_count_fraction: dict = None,
        auto_tags: dict = None,
        short_description: dict = None,
        ext_mkt_class: dict = None,
        mkt_point1: dict = None,
        portfolio_managers: dict = None,
        asset_parameters_commodity_sector: dict = None,
        hedge_tracking_error: dict = None,
        asset_parameters_coupon_type: dict = None,
        supra_strategy: dict = None,
        wi_id: dict = None,
        market_cap_category: dict = None,
        mkt_point3: dict = None,
        mkt_point2: dict = None,
        strike_price: dict = None,
        mkt_point4: dict = None,
        units: dict = None,
        em_id: dict = None,
        sts_credit_region: dict = None,
        ext_mkt_point3: dict = None,
        asset_classifications_risk_country_name: dict = None,
        asset_parameters_vendor: dict = None,
        mkt_type: dict = None,
        ext_mkt_point1: dict = None,
        product_type: dict = None,
        sub_region_code: dict = None,
        ext_mkt_point2: dict = None,
        asset_parameters_fixed_rate: dict = None,
        last_returns_end_date: dict = None,
        position_source_type: dict = None,
        minimum_denomination: dict = None,
        flagship: dict = None,
        lms_id: dict = None,
        cross: dict = None,
        sts_rates_maturity: dict = None,
        position_source: dict = None,
        listed: dict = None,
        shock_style: dict = None,
        g10_currency: dict = None,
        strategy: dict = None,
        methodology: dict = None,
        isin: dict = None
    ):        
        super().__init__()
        self.internal_index_calc_region = internal_index_calc_region
        self.issue_status_date = issue_status_date
        self.pl_id = pl_id
        self.last_returns_start_date = last_returns_start_date
        self.amount_outstanding = amount_outstanding
        self.asset_classifications_gics_sub_industry = asset_classifications_gics_sub_industry
        self.mdapi_class = mdapi_class
        self.data_set_ids = data_set_ids
        self.call_first_date = call_first_date
        self.pb_client_id = pb_client_id
        self.owner_id = owner_id
        self.economic_terms_hash = economic_terms_hash
        self.sec_db = sec_db
        self.objective = objective
        self.simon_intl_asset_tags = simon_intl_asset_tags
        self.private_placement_type = private_placement_type
        self.hedge_notional = hedge_notional
        self.rank = rank
        self.data_set_category = data_set_category
        self.created_by_id = created_by_id
        self.vehicle_type = vehicle_type
        self.market_data_type = market_data_type
        self.asset_parameters_payer_day_count_fraction = asset_parameters_payer_day_count_fraction
        self.point_class = point_class
        self.minimum_increment = minimum_increment
        self.hedge_volatility = hedge_volatility
        self.version = version
        self.tags = tags
        self.asset_classifications_gics_industry_group = asset_classifications_gics_industry_group
        self.market_data_asset = market_data_asset
        self.asset_classifications_is_primary = asset_classifications_is_primary
        self.styles = styles
        self.short_name = short_name
        self.eid = eid
        self.jsn = jsn
        self.mkt_quoting_style = mkt_quoting_style
        self.mic = mic
        self.ps_id = ps_id
        self.issue_status = issue_status
        self.region_code = region_code
        self.dollar_cross = dollar_cross
        self.portfolio_type = portfolio_type
        self.vendor = vendor
        self.popularity = popularity
        self.currency = currency
        self.term = term
        self.real_time_restriction_status = real_time_restriction_status
        self.asset_parameters_clearing_house = asset_parameters_clearing_house
        self.rating_fitch = rating_fitch
        self.non_symbol_dimensions = non_symbol_dimensions
        self.asset_parameters_floating_rate_designated_maturity = asset_parameters_floating_rate_designated_maturity
        self.target_notional = target_notional
        self.mkt_class = mkt_class
        self.delisted = delisted
        self.last_updated_since = last_updated_since
        self.regional_focus = regional_focus
        self.asset_parameters_payer_designated_maturity = asset_parameters_payer_designated_maturity
        self.seasonal_adjustment_short = seasonal_adjustment_short
        self.asset_parameters_exchange_currency = asset_parameters_exchange_currency
        self.asset_classifications_country_name = asset_classifications_country_name
        self.management_fee = management_fee
        self.rating_moodys = rating_moodys
        self.simon_id = simon_id
        self.cusip = cusip
        self.notes = notes
        self.asset_parameters_floating_rate_option = asset_parameters_floating_rate_option
        self.internal_index_calc_agent = internal_index_calc_agent
        self.rating_second_highest = rating_second_highest
        self.asset_classifications_country_code = asset_classifications_country_code
        self.frequency = frequency
        self.option_type = option_type
        self.data_set_sub_category = data_set_sub_category
        self.is_legacy_pair_basket = is_legacy_pair_basket
        self.issuer_type = issuer_type
        self.asset_parameters_pricing_location = asset_parameters_pricing_location
        self.plot_id = plot_id
        self.asset_parameters_coupon = asset_parameters_coupon
        self.data_product = data_product
        self.mq_symbol = mq_symbol
        self.sectors = sectors
        self.multiplier = multiplier
        self.asset_parameters_payer_rate_option = asset_parameters_payer_rate_option
        self.market_data_point = market_data_point
        self.external = external
        self.wpk = wpk
        self.sts_fx_currency = sts_fx_currency
        self.hedge_annualized_volatility = hedge_annualized_volatility
        self.name = name
        self.asset_parameters_expiration_date = asset_parameters_expiration_date
        self.aum = aum
        self.exchange = exchange
        self.folder_name = folder_name
        self.region = region
        self.cid = cid
        self.onboarded = onboarded
        self.live_date = live_date
        self.issue_price = issue_price
        self.sink_factor = sink_factor
        self.underlying_data_set_id = underlying_data_set_id
        self.asset_parameters_payer_frequency = asset_parameters_payer_frequency
        self.prime_id = prime_id
        self.asset_classifications_gics_sector = asset_classifications_gics_sector
        self.sts_asset_name = sts_asset_name
        self.description = description
        self.asset_classifications_is_country_primary = asset_classifications_is_country_primary
        self.title = title
        self.net_exposure_classification = net_exposure_classification
        self.coupon_type = coupon_type
        self.last_updated_by_id = last_updated_by_id
        self.clone_parent_id = clone_parent_id
        self.company = company
        self.issue_date = issue_date
        self.expiration_date = expiration_date
        self.coverage = coverage
        self.ticker = ticker
        self.asset_parameters_receiver_rate_option = asset_parameters_receiver_rate_option
        self.call_last_date = call_last_date
        self.sts_rates_country = sts_rates_country
        self.latest_execution_time = latest_execution_time
        self.asset_parameters_receiver_designated_maturity = asset_parameters_receiver_designated_maturity
        self.gsn = gsn
        self.gss = gss
        self.rating_linear = rating_linear
        self.asset_class = asset_class
        self.cm_id = cm_id
        self.gsideid = gsideid
        self.__type = type_
        self.mdapi = mdapi
        self.ric = ric
        self.issuer = issuer
        self.position_source_id = position_source_id
        self.measures = measures
        self.asset_parameters_floating_rate_day_count_fraction = asset_parameters_floating_rate_day_count_fraction
        self.action = action
        self.__id = id_
        self.asset_parameters_seniority = asset_parameters_seniority
        self.redemption_date = redemption_date
        self.identifier = identifier
        self.index_create_source = index_create_source
        self.sec_name = sec_name
        self.sub_region = sub_region
        self.asset_parameters_receiver_day_count_fraction = asset_parameters_receiver_day_count_fraction
        self.asset_parameters_notional_currency = asset_parameters_notional_currency
        self.sedol = sedol
        self.mkt_asset = mkt_asset
        self.rating_standard_and_poors = rating_standard_and_poors
        self.asset_types = asset_types
        self.bcid = bcid
        self.gsid = gsid
        self.tdapi = tdapi
        self.last_updated_message = last_updated_message
        self.rcic = rcic
        self.trading_restriction = trading_restriction
        self.status = status
        self.asset_parameters_pay_or_receive = asset_parameters_pay_or_receive
        self.name_raw = name_raw
        self.asset_classifications_gics_industry = asset_classifications_gics_industry
        self.on_behalf_of = on_behalf_of
        self.accrued_interest_standard = accrued_interest_standard
        self.sts_commodity = sts_commodity
        self.sectors_raw = sectors_raw
        self.sts_commodity_sector = sts_commodity_sector
        self.asset_parameters_receiver_frequency = asset_parameters_receiver_frequency
        self.position_source_name = position_source_name
        self.gsid_equivalent = gsid_equivalent
        self.categories = categories
        self.symbol_dimensions = symbol_dimensions
        self.ext_mkt_asset = ext_mkt_asset
        self.asset_parameters_fixed_rate_frequency = asset_parameters_fixed_rate_frequency
        self.coupon = coupon
        self.compliance_restricted_status = compliance_restricted_status
        self.quoting_style = quoting_style
        self.scenario_group_id = scenario_group_id
        self.asset_parameters_issuer_type = asset_parameters_issuer_type
        self.sts_credit_market = sts_credit_market
        self.bbid = bbid
        self.asset_classifications_risk_country_code = asset_classifications_risk_country_code
        self.sts_em_dm = sts_em_dm
        self.issue_size = issue_size
        self.returns_enabled = returns_enabled
        self.seniority = seniority
        self.asset_parameters_settlement = asset_parameters_settlement
        self.primary_country_ric = primary_country_ric
        self.is_pair_basket = is_pair_basket
        self.default_backcast = default_backcast
        self.use_machine_learning = use_machine_learning
        self.performance_fee = performance_fee
        self.report_type = report_type
        self.underlying_asset_ids = underlying_asset_ids
        self.encoded_stats = encoded_stats
        self.pnode_id = pnode_id
        self.backtest_type = backtest_type
        self.asset_parameters_issuer = asset_parameters_issuer
        self.exchange_code = exchange_code
        self.asset_parameters_strike = asset_parameters_strike
        self.asset_parameters_termination_date = asset_parameters_termination_date
        self.resource = resource
        self.bbid_equivalent = bbid_equivalent
        self.asset_parameters_effective_date = asset_parameters_effective_date
        self.valoren = valoren
        self.asset_parameters_fixed_rate_day_count_fraction = asset_parameters_fixed_rate_day_count_fraction
        self.auto_tags = auto_tags
        self.short_description = short_description
        self.ext_mkt_class = ext_mkt_class
        self.mkt_point1 = mkt_point1
        self.portfolio_managers = portfolio_managers
        self.asset_parameters_commodity_sector = asset_parameters_commodity_sector
        self.hedge_tracking_error = hedge_tracking_error
        self.asset_parameters_coupon_type = asset_parameters_coupon_type
        self.supra_strategy = supra_strategy
        self.wi_id = wi_id
        self.market_cap_category = market_cap_category
        self.mkt_point3 = mkt_point3
        self.mkt_point2 = mkt_point2
        self.strike_price = strike_price
        self.mkt_point4 = mkt_point4
        self.units = units
        self.em_id = em_id
        self.sts_credit_region = sts_credit_region
        self.ext_mkt_point3 = ext_mkt_point3
        self.asset_classifications_risk_country_name = asset_classifications_risk_country_name
        self.asset_parameters_vendor = asset_parameters_vendor
        self.mkt_type = mkt_type
        self.ext_mkt_point1 = ext_mkt_point1
        self.product_type = product_type
        self.sub_region_code = sub_region_code
        self.ext_mkt_point2 = ext_mkt_point2
        self.asset_parameters_fixed_rate = asset_parameters_fixed_rate
        self.last_returns_end_date = last_returns_end_date
        self.position_source_type = position_source_type
        self.minimum_denomination = minimum_denomination
        self.flagship = flagship
        self.lms_id = lms_id
        self.cross = cross
        self.sts_rates_maturity = sts_rates_maturity
        self.position_source = position_source
        self.listed = listed
        self.shock_style = shock_style
        self.g10_currency = g10_currency
        self.strategy = strategy
        self.methodology = methodology
        self.isin = isin

    @property
    def internal_index_calc_region(self) -> dict:
        return self.__internal_index_calc_region

    @internal_index_calc_region.setter
    def internal_index_calc_region(self, value: dict):
        self._property_changed('internal_index_calc_region')
        self.__internal_index_calc_region = value        

    @property
    def issue_status_date(self) -> dict:
        return self.__issue_status_date

    @issue_status_date.setter
    def issue_status_date(self, value: dict):
        self._property_changed('issue_status_date')
        self.__issue_status_date = value        

    @property
    def pl_id(self) -> dict:
        return self.__pl_id

    @pl_id.setter
    def pl_id(self, value: dict):
        self._property_changed('pl_id')
        self.__pl_id = value        

    @property
    def last_returns_start_date(self) -> dict:
        return self.__last_returns_start_date

    @last_returns_start_date.setter
    def last_returns_start_date(self, value: dict):
        self._property_changed('last_returns_start_date')
        self.__last_returns_start_date = value        

    @property
    def amount_outstanding(self) -> dict:
        return self.__amount_outstanding

    @amount_outstanding.setter
    def amount_outstanding(self, value: dict):
        self._property_changed('amount_outstanding')
        self.__amount_outstanding = value        

    @property
    def asset_classifications_gics_sub_industry(self) -> dict:
        return self.__asset_classifications_gics_sub_industry

    @asset_classifications_gics_sub_industry.setter
    def asset_classifications_gics_sub_industry(self, value: dict):
        self._property_changed('asset_classifications_gics_sub_industry')
        self.__asset_classifications_gics_sub_industry = value        

    @property
    def mdapi_class(self) -> dict:
        return self.__mdapi_class

    @mdapi_class.setter
    def mdapi_class(self, value: dict):
        self._property_changed('mdapi_class')
        self.__mdapi_class = value        

    @property
    def data_set_ids(self) -> dict:
        return self.__data_set_ids

    @data_set_ids.setter
    def data_set_ids(self, value: dict):
        self._property_changed('data_set_ids')
        self.__data_set_ids = value        

    @property
    def call_first_date(self) -> dict:
        return self.__call_first_date

    @call_first_date.setter
    def call_first_date(self, value: dict):
        self._property_changed('call_first_date')
        self.__call_first_date = value        

    @property
    def pb_client_id(self) -> dict:
        return self.__pb_client_id

    @pb_client_id.setter
    def pb_client_id(self, value: dict):
        self._property_changed('pb_client_id')
        self.__pb_client_id = value        

    @property
    def owner_id(self) -> dict:
        return self.__owner_id

    @owner_id.setter
    def owner_id(self, value: dict):
        self._property_changed('owner_id')
        self.__owner_id = value        

    @property
    def economic_terms_hash(self) -> dict:
        return self.__economic_terms_hash

    @economic_terms_hash.setter
    def economic_terms_hash(self, value: dict):
        self._property_changed('economic_terms_hash')
        self.__economic_terms_hash = value        

    @property
    def sec_db(self) -> dict:
        return self.__sec_db

    @sec_db.setter
    def sec_db(self, value: dict):
        self._property_changed('sec_db')
        self.__sec_db = value        

    @property
    def objective(self) -> dict:
        return self.__objective

    @objective.setter
    def objective(self, value: dict):
        self._property_changed('objective')
        self.__objective = value        

    @property
    def simon_intl_asset_tags(self) -> dict:
        return self.__simon_intl_asset_tags

    @simon_intl_asset_tags.setter
    def simon_intl_asset_tags(self, value: dict):
        self._property_changed('simon_intl_asset_tags')
        self.__simon_intl_asset_tags = value        

    @property
    def private_placement_type(self) -> dict:
        return self.__private_placement_type

    @private_placement_type.setter
    def private_placement_type(self, value: dict):
        self._property_changed('private_placement_type')
        self.__private_placement_type = value        

    @property
    def hedge_notional(self) -> dict:
        return self.__hedge_notional

    @hedge_notional.setter
    def hedge_notional(self, value: dict):
        self._property_changed('hedge_notional')
        self.__hedge_notional = value        

    @property
    def rank(self) -> dict:
        return self.__rank

    @rank.setter
    def rank(self, value: dict):
        self._property_changed('rank')
        self.__rank = value        

    @property
    def data_set_category(self) -> dict:
        return self.__data_set_category

    @data_set_category.setter
    def data_set_category(self, value: dict):
        self._property_changed('data_set_category')
        self.__data_set_category = value        

    @property
    def created_by_id(self) -> dict:
        return self.__created_by_id

    @created_by_id.setter
    def created_by_id(self, value: dict):
        self._property_changed('created_by_id')
        self.__created_by_id = value        

    @property
    def vehicle_type(self) -> dict:
        return self.__vehicle_type

    @vehicle_type.setter
    def vehicle_type(self, value: dict):
        self._property_changed('vehicle_type')
        self.__vehicle_type = value        

    @property
    def market_data_type(self) -> dict:
        return self.__market_data_type

    @market_data_type.setter
    def market_data_type(self, value: dict):
        self._property_changed('market_data_type')
        self.__market_data_type = value        

    @property
    def asset_parameters_payer_day_count_fraction(self) -> dict:
        return self.__asset_parameters_payer_day_count_fraction

    @asset_parameters_payer_day_count_fraction.setter
    def asset_parameters_payer_day_count_fraction(self, value: dict):
        self._property_changed('asset_parameters_payer_day_count_fraction')
        self.__asset_parameters_payer_day_count_fraction = value        

    @property
    def point_class(self) -> dict:
        return self.__point_class

    @point_class.setter
    def point_class(self, value: dict):
        self._property_changed('point_class')
        self.__point_class = value        

    @property
    def minimum_increment(self) -> dict:
        return self.__minimum_increment

    @minimum_increment.setter
    def minimum_increment(self, value: dict):
        self._property_changed('minimum_increment')
        self.__minimum_increment = value        

    @property
    def hedge_volatility(self) -> dict:
        return self.__hedge_volatility

    @hedge_volatility.setter
    def hedge_volatility(self, value: dict):
        self._property_changed('hedge_volatility')
        self.__hedge_volatility = value        

    @property
    def version(self) -> dict:
        return self.__version

    @version.setter
    def version(self, value: dict):
        self._property_changed('version')
        self.__version = value        

    @property
    def tags(self) -> dict:
        return self.__tags

    @tags.setter
    def tags(self, value: dict):
        self._property_changed('tags')
        self.__tags = value        

    @property
    def asset_classifications_gics_industry_group(self) -> dict:
        return self.__asset_classifications_gics_industry_group

    @asset_classifications_gics_industry_group.setter
    def asset_classifications_gics_industry_group(self, value: dict):
        self._property_changed('asset_classifications_gics_industry_group')
        self.__asset_classifications_gics_industry_group = value        

    @property
    def market_data_asset(self) -> dict:
        return self.__market_data_asset

    @market_data_asset.setter
    def market_data_asset(self, value: dict):
        self._property_changed('market_data_asset')
        self.__market_data_asset = value        

    @property
    def asset_classifications_is_primary(self) -> dict:
        return self.__asset_classifications_is_primary

    @asset_classifications_is_primary.setter
    def asset_classifications_is_primary(self, value: dict):
        self._property_changed('asset_classifications_is_primary')
        self.__asset_classifications_is_primary = value        

    @property
    def styles(self) -> dict:
        return self.__styles

    @styles.setter
    def styles(self, value: dict):
        self._property_changed('styles')
        self.__styles = value        

    @property
    def short_name(self) -> dict:
        return self.__short_name

    @short_name.setter
    def short_name(self, value: dict):
        self._property_changed('short_name')
        self.__short_name = value        

    @property
    def eid(self) -> dict:
        return self.__eid

    @eid.setter
    def eid(self, value: dict):
        self._property_changed('eid')
        self.__eid = value        

    @property
    def jsn(self) -> dict:
        return self.__jsn

    @jsn.setter
    def jsn(self, value: dict):
        self._property_changed('jsn')
        self.__jsn = value        

    @property
    def mkt_quoting_style(self) -> dict:
        return self.__mkt_quoting_style

    @mkt_quoting_style.setter
    def mkt_quoting_style(self, value: dict):
        self._property_changed('mkt_quoting_style')
        self.__mkt_quoting_style = value        

    @property
    def mic(self) -> dict:
        return self.__mic

    @mic.setter
    def mic(self, value: dict):
        self._property_changed('mic')
        self.__mic = value        

    @property
    def ps_id(self) -> dict:
        return self.__ps_id

    @ps_id.setter
    def ps_id(self, value: dict):
        self._property_changed('ps_id')
        self.__ps_id = value        

    @property
    def issue_status(self) -> dict:
        return self.__issue_status

    @issue_status.setter
    def issue_status(self, value: dict):
        self._property_changed('issue_status')
        self.__issue_status = value        

    @property
    def region_code(self) -> dict:
        return self.__region_code

    @region_code.setter
    def region_code(self, value: dict):
        self._property_changed('region_code')
        self.__region_code = value        

    @property
    def dollar_cross(self) -> dict:
        return self.__dollar_cross

    @dollar_cross.setter
    def dollar_cross(self, value: dict):
        self._property_changed('dollar_cross')
        self.__dollar_cross = value        

    @property
    def portfolio_type(self) -> dict:
        return self.__portfolio_type

    @portfolio_type.setter
    def portfolio_type(self, value: dict):
        self._property_changed('portfolio_type')
        self.__portfolio_type = value        

    @property
    def vendor(self) -> dict:
        return self.__vendor

    @vendor.setter
    def vendor(self, value: dict):
        self._property_changed('vendor')
        self.__vendor = value        

    @property
    def popularity(self) -> dict:
        return self.__popularity

    @popularity.setter
    def popularity(self, value: dict):
        self._property_changed('popularity')
        self.__popularity = value        

    @property
    def currency(self) -> dict:
        return self.__currency

    @currency.setter
    def currency(self, value: dict):
        self._property_changed('currency')
        self.__currency = value        

    @property
    def term(self) -> dict:
        return self.__term

    @term.setter
    def term(self, value: dict):
        self._property_changed('term')
        self.__term = value        

    @property
    def real_time_restriction_status(self) -> dict:
        return self.__real_time_restriction_status

    @real_time_restriction_status.setter
    def real_time_restriction_status(self, value: dict):
        self._property_changed('real_time_restriction_status')
        self.__real_time_restriction_status = value        

    @property
    def asset_parameters_clearing_house(self) -> dict:
        return self.__asset_parameters_clearing_house

    @asset_parameters_clearing_house.setter
    def asset_parameters_clearing_house(self, value: dict):
        self._property_changed('asset_parameters_clearing_house')
        self.__asset_parameters_clearing_house = value        

    @property
    def rating_fitch(self) -> dict:
        return self.__rating_fitch

    @rating_fitch.setter
    def rating_fitch(self, value: dict):
        self._property_changed('rating_fitch')
        self.__rating_fitch = value        

    @property
    def non_symbol_dimensions(self) -> dict:
        return self.__non_symbol_dimensions

    @non_symbol_dimensions.setter
    def non_symbol_dimensions(self, value: dict):
        self._property_changed('non_symbol_dimensions')
        self.__non_symbol_dimensions = value        

    @property
    def asset_parameters_floating_rate_designated_maturity(self) -> dict:
        return self.__asset_parameters_floating_rate_designated_maturity

    @asset_parameters_floating_rate_designated_maturity.setter
    def asset_parameters_floating_rate_designated_maturity(self, value: dict):
        self._property_changed('asset_parameters_floating_rate_designated_maturity')
        self.__asset_parameters_floating_rate_designated_maturity = value        

    @property
    def target_notional(self) -> dict:
        return self.__target_notional

    @target_notional.setter
    def target_notional(self, value: dict):
        self._property_changed('target_notional')
        self.__target_notional = value        

    @property
    def mkt_class(self) -> dict:
        return self.__mkt_class

    @mkt_class.setter
    def mkt_class(self, value: dict):
        self._property_changed('mkt_class')
        self.__mkt_class = value        

    @property
    def delisted(self) -> dict:
        return self.__delisted

    @delisted.setter
    def delisted(self, value: dict):
        self._property_changed('delisted')
        self.__delisted = value        

    @property
    def last_updated_since(self) -> dict:
        return self.__last_updated_since

    @last_updated_since.setter
    def last_updated_since(self, value: dict):
        self._property_changed('last_updated_since')
        self.__last_updated_since = value        

    @property
    def regional_focus(self) -> dict:
        return self.__regional_focus

    @regional_focus.setter
    def regional_focus(self, value: dict):
        self._property_changed('regional_focus')
        self.__regional_focus = value        

    @property
    def asset_parameters_payer_designated_maturity(self) -> dict:
        return self.__asset_parameters_payer_designated_maturity

    @asset_parameters_payer_designated_maturity.setter
    def asset_parameters_payer_designated_maturity(self, value: dict):
        self._property_changed('asset_parameters_payer_designated_maturity')
        self.__asset_parameters_payer_designated_maturity = value        

    @property
    def seasonal_adjustment_short(self) -> dict:
        return self.__seasonal_adjustment_short

    @seasonal_adjustment_short.setter
    def seasonal_adjustment_short(self, value: dict):
        self._property_changed('seasonal_adjustment_short')
        self.__seasonal_adjustment_short = value        

    @property
    def asset_parameters_exchange_currency(self) -> dict:
        return self.__asset_parameters_exchange_currency

    @asset_parameters_exchange_currency.setter
    def asset_parameters_exchange_currency(self, value: dict):
        self._property_changed('asset_parameters_exchange_currency')
        self.__asset_parameters_exchange_currency = value        

    @property
    def asset_classifications_country_name(self) -> dict:
        return self.__asset_classifications_country_name

    @asset_classifications_country_name.setter
    def asset_classifications_country_name(self, value: dict):
        self._property_changed('asset_classifications_country_name')
        self.__asset_classifications_country_name = value        

    @property
    def management_fee(self) -> dict:
        return self.__management_fee

    @management_fee.setter
    def management_fee(self, value: dict):
        self._property_changed('management_fee')
        self.__management_fee = value        

    @property
    def rating_moodys(self) -> dict:
        return self.__rating_moodys

    @rating_moodys.setter
    def rating_moodys(self, value: dict):
        self._property_changed('rating_moodys')
        self.__rating_moodys = value        

    @property
    def simon_id(self) -> dict:
        return self.__simon_id

    @simon_id.setter
    def simon_id(self, value: dict):
        self._property_changed('simon_id')
        self.__simon_id = value        

    @property
    def cusip(self) -> dict:
        return self.__cusip

    @cusip.setter
    def cusip(self, value: dict):
        self._property_changed('cusip')
        self.__cusip = value        

    @property
    def notes(self) -> dict:
        return self.__notes

    @notes.setter
    def notes(self, value: dict):
        self._property_changed('notes')
        self.__notes = value        

    @property
    def asset_parameters_floating_rate_option(self) -> dict:
        return self.__asset_parameters_floating_rate_option

    @asset_parameters_floating_rate_option.setter
    def asset_parameters_floating_rate_option(self, value: dict):
        self._property_changed('asset_parameters_floating_rate_option')
        self.__asset_parameters_floating_rate_option = value        

    @property
    def internal_index_calc_agent(self) -> dict:
        return self.__internal_index_calc_agent

    @internal_index_calc_agent.setter
    def internal_index_calc_agent(self, value: dict):
        self._property_changed('internal_index_calc_agent')
        self.__internal_index_calc_agent = value        

    @property
    def rating_second_highest(self) -> dict:
        return self.__rating_second_highest

    @rating_second_highest.setter
    def rating_second_highest(self, value: dict):
        self._property_changed('rating_second_highest')
        self.__rating_second_highest = value        

    @property
    def asset_classifications_country_code(self) -> dict:
        return self.__asset_classifications_country_code

    @asset_classifications_country_code.setter
    def asset_classifications_country_code(self, value: dict):
        self._property_changed('asset_classifications_country_code')
        self.__asset_classifications_country_code = value        

    @property
    def frequency(self) -> dict:
        return self.__frequency

    @frequency.setter
    def frequency(self, value: dict):
        self._property_changed('frequency')
        self.__frequency = value        

    @property
    def option_type(self) -> dict:
        return self.__option_type

    @option_type.setter
    def option_type(self, value: dict):
        self._property_changed('option_type')
        self.__option_type = value        

    @property
    def data_set_sub_category(self) -> dict:
        return self.__data_set_sub_category

    @data_set_sub_category.setter
    def data_set_sub_category(self, value: dict):
        self._property_changed('data_set_sub_category')
        self.__data_set_sub_category = value        

    @property
    def is_legacy_pair_basket(self) -> dict:
        return self.__is_legacy_pair_basket

    @is_legacy_pair_basket.setter
    def is_legacy_pair_basket(self, value: dict):
        self._property_changed('is_legacy_pair_basket')
        self.__is_legacy_pair_basket = value        

    @property
    def issuer_type(self) -> dict:
        return self.__issuer_type

    @issuer_type.setter
    def issuer_type(self, value: dict):
        self._property_changed('issuer_type')
        self.__issuer_type = value        

    @property
    def asset_parameters_pricing_location(self) -> dict:
        return self.__asset_parameters_pricing_location

    @asset_parameters_pricing_location.setter
    def asset_parameters_pricing_location(self, value: dict):
        self._property_changed('asset_parameters_pricing_location')
        self.__asset_parameters_pricing_location = value        

    @property
    def plot_id(self) -> dict:
        return self.__plot_id

    @plot_id.setter
    def plot_id(self, value: dict):
        self._property_changed('plot_id')
        self.__plot_id = value        

    @property
    def asset_parameters_coupon(self) -> dict:
        return self.__asset_parameters_coupon

    @asset_parameters_coupon.setter
    def asset_parameters_coupon(self, value: dict):
        self._property_changed('asset_parameters_coupon')
        self.__asset_parameters_coupon = value        

    @property
    def data_product(self) -> dict:
        return self.__data_product

    @data_product.setter
    def data_product(self, value: dict):
        self._property_changed('data_product')
        self.__data_product = value        

    @property
    def mq_symbol(self) -> dict:
        return self.__mq_symbol

    @mq_symbol.setter
    def mq_symbol(self, value: dict):
        self._property_changed('mq_symbol')
        self.__mq_symbol = value        

    @property
    def sectors(self) -> dict:
        return self.__sectors

    @sectors.setter
    def sectors(self, value: dict):
        self._property_changed('sectors')
        self.__sectors = value        

    @property
    def multiplier(self) -> dict:
        return self.__multiplier

    @multiplier.setter
    def multiplier(self, value: dict):
        self._property_changed('multiplier')
        self.__multiplier = value        

    @property
    def asset_parameters_payer_rate_option(self) -> dict:
        return self.__asset_parameters_payer_rate_option

    @asset_parameters_payer_rate_option.setter
    def asset_parameters_payer_rate_option(self, value: dict):
        self._property_changed('asset_parameters_payer_rate_option')
        self.__asset_parameters_payer_rate_option = value        

    @property
    def market_data_point(self) -> dict:
        return self.__market_data_point

    @market_data_point.setter
    def market_data_point(self, value: dict):
        self._property_changed('market_data_point')
        self.__market_data_point = value        

    @property
    def external(self) -> dict:
        return self.__external

    @external.setter
    def external(self, value: dict):
        self._property_changed('external')
        self.__external = value        

    @property
    def wpk(self) -> dict:
        return self.__wpk

    @wpk.setter
    def wpk(self, value: dict):
        self._property_changed('wpk')
        self.__wpk = value        

    @property
    def sts_fx_currency(self) -> dict:
        return self.__sts_fx_currency

    @sts_fx_currency.setter
    def sts_fx_currency(self, value: dict):
        self._property_changed('sts_fx_currency')
        self.__sts_fx_currency = value        

    @property
    def hedge_annualized_volatility(self) -> dict:
        return self.__hedge_annualized_volatility

    @hedge_annualized_volatility.setter
    def hedge_annualized_volatility(self, value: dict):
        self._property_changed('hedge_annualized_volatility')
        self.__hedge_annualized_volatility = value        

    @property
    def name(self) -> dict:
        return self.__name

    @name.setter
    def name(self, value: dict):
        self._property_changed('name')
        self.__name = value        

    @property
    def asset_parameters_expiration_date(self) -> dict:
        return self.__asset_parameters_expiration_date

    @asset_parameters_expiration_date.setter
    def asset_parameters_expiration_date(self, value: dict):
        self._property_changed('asset_parameters_expiration_date')
        self.__asset_parameters_expiration_date = value        

    @property
    def aum(self) -> dict:
        return self.__aum

    @aum.setter
    def aum(self, value: dict):
        self._property_changed('aum')
        self.__aum = value        

    @property
    def exchange(self) -> dict:
        return self.__exchange

    @exchange.setter
    def exchange(self, value: dict):
        self._property_changed('exchange')
        self.__exchange = value        

    @property
    def folder_name(self) -> dict:
        return self.__folder_name

    @folder_name.setter
    def folder_name(self, value: dict):
        self._property_changed('folder_name')
        self.__folder_name = value        

    @property
    def region(self) -> dict:
        return self.__region

    @region.setter
    def region(self, value: dict):
        self._property_changed('region')
        self.__region = value        

    @property
    def cid(self) -> dict:
        return self.__cid

    @cid.setter
    def cid(self, value: dict):
        self._property_changed('cid')
        self.__cid = value        

    @property
    def onboarded(self) -> dict:
        return self.__onboarded

    @onboarded.setter
    def onboarded(self, value: dict):
        self._property_changed('onboarded')
        self.__onboarded = value        

    @property
    def live_date(self) -> dict:
        return self.__live_date

    @live_date.setter
    def live_date(self, value: dict):
        self._property_changed('live_date')
        self.__live_date = value        

    @property
    def issue_price(self) -> dict:
        return self.__issue_price

    @issue_price.setter
    def issue_price(self, value: dict):
        self._property_changed('issue_price')
        self.__issue_price = value        

    @property
    def sink_factor(self) -> dict:
        return self.__sink_factor

    @sink_factor.setter
    def sink_factor(self, value: dict):
        self._property_changed('sink_factor')
        self.__sink_factor = value        

    @property
    def underlying_data_set_id(self) -> dict:
        return self.__underlying_data_set_id

    @underlying_data_set_id.setter
    def underlying_data_set_id(self, value: dict):
        self._property_changed('underlying_data_set_id')
        self.__underlying_data_set_id = value        

    @property
    def asset_parameters_payer_frequency(self) -> dict:
        return self.__asset_parameters_payer_frequency

    @asset_parameters_payer_frequency.setter
    def asset_parameters_payer_frequency(self, value: dict):
        self._property_changed('asset_parameters_payer_frequency')
        self.__asset_parameters_payer_frequency = value        

    @property
    def prime_id(self) -> dict:
        return self.__prime_id

    @prime_id.setter
    def prime_id(self, value: dict):
        self._property_changed('prime_id')
        self.__prime_id = value        

    @property
    def asset_classifications_gics_sector(self) -> dict:
        return self.__asset_classifications_gics_sector

    @asset_classifications_gics_sector.setter
    def asset_classifications_gics_sector(self, value: dict):
        self._property_changed('asset_classifications_gics_sector')
        self.__asset_classifications_gics_sector = value        

    @property
    def sts_asset_name(self) -> dict:
        return self.__sts_asset_name

    @sts_asset_name.setter
    def sts_asset_name(self, value: dict):
        self._property_changed('sts_asset_name')
        self.__sts_asset_name = value        

    @property
    def description(self) -> dict:
        return self.__description

    @description.setter
    def description(self, value: dict):
        self._property_changed('description')
        self.__description = value        

    @property
    def asset_classifications_is_country_primary(self) -> dict:
        return self.__asset_classifications_is_country_primary

    @asset_classifications_is_country_primary.setter
    def asset_classifications_is_country_primary(self, value: dict):
        self._property_changed('asset_classifications_is_country_primary')
        self.__asset_classifications_is_country_primary = value        

    @property
    def title(self) -> dict:
        return self.__title

    @title.setter
    def title(self, value: dict):
        self._property_changed('title')
        self.__title = value        

    @property
    def net_exposure_classification(self) -> dict:
        return self.__net_exposure_classification

    @net_exposure_classification.setter
    def net_exposure_classification(self, value: dict):
        self._property_changed('net_exposure_classification')
        self.__net_exposure_classification = value        

    @property
    def coupon_type(self) -> dict:
        return self.__coupon_type

    @coupon_type.setter
    def coupon_type(self, value: dict):
        self._property_changed('coupon_type')
        self.__coupon_type = value        

    @property
    def last_updated_by_id(self) -> dict:
        return self.__last_updated_by_id

    @last_updated_by_id.setter
    def last_updated_by_id(self, value: dict):
        self._property_changed('last_updated_by_id')
        self.__last_updated_by_id = value        

    @property
    def clone_parent_id(self) -> dict:
        return self.__clone_parent_id

    @clone_parent_id.setter
    def clone_parent_id(self, value: dict):
        self._property_changed('clone_parent_id')
        self.__clone_parent_id = value        

    @property
    def company(self) -> dict:
        return self.__company

    @company.setter
    def company(self, value: dict):
        self._property_changed('company')
        self.__company = value        

    @property
    def issue_date(self) -> dict:
        return self.__issue_date

    @issue_date.setter
    def issue_date(self, value: dict):
        self._property_changed('issue_date')
        self.__issue_date = value        

    @property
    def expiration_date(self) -> dict:
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, value: dict):
        self._property_changed('expiration_date')
        self.__expiration_date = value        

    @property
    def coverage(self) -> dict:
        return self.__coverage

    @coverage.setter
    def coverage(self, value: dict):
        self._property_changed('coverage')
        self.__coverage = value        

    @property
    def ticker(self) -> dict:
        return self.__ticker

    @ticker.setter
    def ticker(self, value: dict):
        self._property_changed('ticker')
        self.__ticker = value        

    @property
    def asset_parameters_receiver_rate_option(self) -> dict:
        return self.__asset_parameters_receiver_rate_option

    @asset_parameters_receiver_rate_option.setter
    def asset_parameters_receiver_rate_option(self, value: dict):
        self._property_changed('asset_parameters_receiver_rate_option')
        self.__asset_parameters_receiver_rate_option = value        

    @property
    def call_last_date(self) -> dict:
        return self.__call_last_date

    @call_last_date.setter
    def call_last_date(self, value: dict):
        self._property_changed('call_last_date')
        self.__call_last_date = value        

    @property
    def sts_rates_country(self) -> dict:
        return self.__sts_rates_country

    @sts_rates_country.setter
    def sts_rates_country(self, value: dict):
        self._property_changed('sts_rates_country')
        self.__sts_rates_country = value        

    @property
    def latest_execution_time(self) -> dict:
        return self.__latest_execution_time

    @latest_execution_time.setter
    def latest_execution_time(self, value: dict):
        self._property_changed('latest_execution_time')
        self.__latest_execution_time = value        

    @property
    def asset_parameters_receiver_designated_maturity(self) -> dict:
        return self.__asset_parameters_receiver_designated_maturity

    @asset_parameters_receiver_designated_maturity.setter
    def asset_parameters_receiver_designated_maturity(self, value: dict):
        self._property_changed('asset_parameters_receiver_designated_maturity')
        self.__asset_parameters_receiver_designated_maturity = value        

    @property
    def gsn(self) -> dict:
        return self.__gsn

    @gsn.setter
    def gsn(self, value: dict):
        self._property_changed('gsn')
        self.__gsn = value        

    @property
    def gss(self) -> dict:
        return self.__gss

    @gss.setter
    def gss(self, value: dict):
        self._property_changed('gss')
        self.__gss = value        

    @property
    def rating_linear(self) -> dict:
        return self.__rating_linear

    @rating_linear.setter
    def rating_linear(self, value: dict):
        self._property_changed('rating_linear')
        self.__rating_linear = value        

    @property
    def asset_class(self) -> dict:
        return self.__asset_class

    @asset_class.setter
    def asset_class(self, value: dict):
        self._property_changed('asset_class')
        self.__asset_class = value        

    @property
    def cm_id(self) -> dict:
        return self.__cm_id

    @cm_id.setter
    def cm_id(self, value: dict):
        self._property_changed('cm_id')
        self.__cm_id = value        

    @property
    def gsideid(self) -> dict:
        return self.__gsideid

    @gsideid.setter
    def gsideid(self, value: dict):
        self._property_changed('gsideid')
        self.__gsideid = value        

    @property
    def type(self) -> dict:
        return self.__type

    @type.setter
    def type(self, value: dict):
        self._property_changed('type')
        self.__type = value        

    @property
    def mdapi(self) -> dict:
        return self.__mdapi

    @mdapi.setter
    def mdapi(self, value: dict):
        self._property_changed('mdapi')
        self.__mdapi = value        

    @property
    def ric(self) -> dict:
        return self.__ric

    @ric.setter
    def ric(self, value: dict):
        self._property_changed('ric')
        self.__ric = value        

    @property
    def issuer(self) -> dict:
        return self.__issuer

    @issuer.setter
    def issuer(self, value: dict):
        self._property_changed('issuer')
        self.__issuer = value        

    @property
    def position_source_id(self) -> dict:
        return self.__position_source_id

    @position_source_id.setter
    def position_source_id(self, value: dict):
        self._property_changed('position_source_id')
        self.__position_source_id = value        

    @property
    def measures(self) -> dict:
        return self.__measures

    @measures.setter
    def measures(self, value: dict):
        self._property_changed('measures')
        self.__measures = value        

    @property
    def asset_parameters_floating_rate_day_count_fraction(self) -> dict:
        return self.__asset_parameters_floating_rate_day_count_fraction

    @asset_parameters_floating_rate_day_count_fraction.setter
    def asset_parameters_floating_rate_day_count_fraction(self, value: dict):
        self._property_changed('asset_parameters_floating_rate_day_count_fraction')
        self.__asset_parameters_floating_rate_day_count_fraction = value        

    @property
    def action(self) -> dict:
        return self.__action

    @action.setter
    def action(self, value: dict):
        self._property_changed('action')
        self.__action = value        

    @property
    def id(self) -> dict:
        return self.__id

    @id.setter
    def id(self, value: dict):
        self._property_changed('id')
        self.__id = value        

    @property
    def asset_parameters_seniority(self) -> dict:
        return self.__asset_parameters_seniority

    @asset_parameters_seniority.setter
    def asset_parameters_seniority(self, value: dict):
        self._property_changed('asset_parameters_seniority')
        self.__asset_parameters_seniority = value        

    @property
    def redemption_date(self) -> dict:
        return self.__redemption_date

    @redemption_date.setter
    def redemption_date(self, value: dict):
        self._property_changed('redemption_date')
        self.__redemption_date = value        

    @property
    def identifier(self) -> dict:
        return self.__identifier

    @identifier.setter
    def identifier(self, value: dict):
        self._property_changed('identifier')
        self.__identifier = value        

    @property
    def index_create_source(self) -> dict:
        return self.__index_create_source

    @index_create_source.setter
    def index_create_source(self, value: dict):
        self._property_changed('index_create_source')
        self.__index_create_source = value        

    @property
    def sec_name(self) -> dict:
        return self.__sec_name

    @sec_name.setter
    def sec_name(self, value: dict):
        self._property_changed('sec_name')
        self.__sec_name = value        

    @property
    def sub_region(self) -> dict:
        return self.__sub_region

    @sub_region.setter
    def sub_region(self, value: dict):
        self._property_changed('sub_region')
        self.__sub_region = value        

    @property
    def asset_parameters_receiver_day_count_fraction(self) -> dict:
        return self.__asset_parameters_receiver_day_count_fraction

    @asset_parameters_receiver_day_count_fraction.setter
    def asset_parameters_receiver_day_count_fraction(self, value: dict):
        self._property_changed('asset_parameters_receiver_day_count_fraction')
        self.__asset_parameters_receiver_day_count_fraction = value        

    @property
    def asset_parameters_notional_currency(self) -> dict:
        return self.__asset_parameters_notional_currency

    @asset_parameters_notional_currency.setter
    def asset_parameters_notional_currency(self, value: dict):
        self._property_changed('asset_parameters_notional_currency')
        self.__asset_parameters_notional_currency = value        

    @property
    def sedol(self) -> dict:
        return self.__sedol

    @sedol.setter
    def sedol(self, value: dict):
        self._property_changed('sedol')
        self.__sedol = value        

    @property
    def mkt_asset(self) -> dict:
        return self.__mkt_asset

    @mkt_asset.setter
    def mkt_asset(self, value: dict):
        self._property_changed('mkt_asset')
        self.__mkt_asset = value        

    @property
    def rating_standard_and_poors(self) -> dict:
        return self.__rating_standard_and_poors

    @rating_standard_and_poors.setter
    def rating_standard_and_poors(self, value: dict):
        self._property_changed('rating_standard_and_poors')
        self.__rating_standard_and_poors = value        

    @property
    def asset_types(self) -> dict:
        return self.__asset_types

    @asset_types.setter
    def asset_types(self, value: dict):
        self._property_changed('asset_types')
        self.__asset_types = value        

    @property
    def bcid(self) -> dict:
        return self.__bcid

    @bcid.setter
    def bcid(self, value: dict):
        self._property_changed('bcid')
        self.__bcid = value        

    @property
    def gsid(self) -> dict:
        return self.__gsid

    @gsid.setter
    def gsid(self, value: dict):
        self._property_changed('gsid')
        self.__gsid = value        

    @property
    def tdapi(self) -> dict:
        return self.__tdapi

    @tdapi.setter
    def tdapi(self, value: dict):
        self._property_changed('tdapi')
        self.__tdapi = value        

    @property
    def last_updated_message(self) -> dict:
        return self.__last_updated_message

    @last_updated_message.setter
    def last_updated_message(self, value: dict):
        self._property_changed('last_updated_message')
        self.__last_updated_message = value        

    @property
    def rcic(self) -> dict:
        return self.__rcic

    @rcic.setter
    def rcic(self, value: dict):
        self._property_changed('rcic')
        self.__rcic = value        

    @property
    def trading_restriction(self) -> dict:
        return self.__trading_restriction

    @trading_restriction.setter
    def trading_restriction(self, value: dict):
        self._property_changed('trading_restriction')
        self.__trading_restriction = value        

    @property
    def status(self) -> dict:
        return self.__status

    @status.setter
    def status(self, value: dict):
        self._property_changed('status')
        self.__status = value        

    @property
    def asset_parameters_pay_or_receive(self) -> dict:
        return self.__asset_parameters_pay_or_receive

    @asset_parameters_pay_or_receive.setter
    def asset_parameters_pay_or_receive(self, value: dict):
        self._property_changed('asset_parameters_pay_or_receive')
        self.__asset_parameters_pay_or_receive = value        

    @property
    def name_raw(self) -> dict:
        return self.__name_raw

    @name_raw.setter
    def name_raw(self, value: dict):
        self._property_changed('name_raw')
        self.__name_raw = value        

    @property
    def asset_classifications_gics_industry(self) -> dict:
        return self.__asset_classifications_gics_industry

    @asset_classifications_gics_industry.setter
    def asset_classifications_gics_industry(self, value: dict):
        self._property_changed('asset_classifications_gics_industry')
        self.__asset_classifications_gics_industry = value        

    @property
    def on_behalf_of(self) -> dict:
        return self.__on_behalf_of

    @on_behalf_of.setter
    def on_behalf_of(self, value: dict):
        self._property_changed('on_behalf_of')
        self.__on_behalf_of = value        

    @property
    def accrued_interest_standard(self) -> dict:
        return self.__accrued_interest_standard

    @accrued_interest_standard.setter
    def accrued_interest_standard(self, value: dict):
        self._property_changed('accrued_interest_standard')
        self.__accrued_interest_standard = value        

    @property
    def sts_commodity(self) -> dict:
        return self.__sts_commodity

    @sts_commodity.setter
    def sts_commodity(self, value: dict):
        self._property_changed('sts_commodity')
        self.__sts_commodity = value        

    @property
    def sectors_raw(self) -> dict:
        return self.__sectors_raw

    @sectors_raw.setter
    def sectors_raw(self, value: dict):
        self._property_changed('sectors_raw')
        self.__sectors_raw = value        

    @property
    def sts_commodity_sector(self) -> dict:
        return self.__sts_commodity_sector

    @sts_commodity_sector.setter
    def sts_commodity_sector(self, value: dict):
        self._property_changed('sts_commodity_sector')
        self.__sts_commodity_sector = value        

    @property
    def asset_parameters_receiver_frequency(self) -> dict:
        return self.__asset_parameters_receiver_frequency

    @asset_parameters_receiver_frequency.setter
    def asset_parameters_receiver_frequency(self, value: dict):
        self._property_changed('asset_parameters_receiver_frequency')
        self.__asset_parameters_receiver_frequency = value        

    @property
    def position_source_name(self) -> dict:
        return self.__position_source_name

    @position_source_name.setter
    def position_source_name(self, value: dict):
        self._property_changed('position_source_name')
        self.__position_source_name = value        

    @property
    def gsid_equivalent(self) -> dict:
        return self.__gsid_equivalent

    @gsid_equivalent.setter
    def gsid_equivalent(self, value: dict):
        self._property_changed('gsid_equivalent')
        self.__gsid_equivalent = value        

    @property
    def categories(self) -> dict:
        return self.__categories

    @categories.setter
    def categories(self, value: dict):
        self._property_changed('categories')
        self.__categories = value        

    @property
    def symbol_dimensions(self) -> dict:
        return self.__symbol_dimensions

    @symbol_dimensions.setter
    def symbol_dimensions(self, value: dict):
        self._property_changed('symbol_dimensions')
        self.__symbol_dimensions = value        

    @property
    def ext_mkt_asset(self) -> dict:
        return self.__ext_mkt_asset

    @ext_mkt_asset.setter
    def ext_mkt_asset(self, value: dict):
        self._property_changed('ext_mkt_asset')
        self.__ext_mkt_asset = value        

    @property
    def asset_parameters_fixed_rate_frequency(self) -> dict:
        return self.__asset_parameters_fixed_rate_frequency

    @asset_parameters_fixed_rate_frequency.setter
    def asset_parameters_fixed_rate_frequency(self, value: dict):
        self._property_changed('asset_parameters_fixed_rate_frequency')
        self.__asset_parameters_fixed_rate_frequency = value        

    @property
    def coupon(self) -> dict:
        return self.__coupon

    @coupon.setter
    def coupon(self, value: dict):
        self._property_changed('coupon')
        self.__coupon = value        

    @property
    def compliance_restricted_status(self) -> dict:
        return self.__compliance_restricted_status

    @compliance_restricted_status.setter
    def compliance_restricted_status(self, value: dict):
        self._property_changed('compliance_restricted_status')
        self.__compliance_restricted_status = value        

    @property
    def quoting_style(self) -> dict:
        return self.__quoting_style

    @quoting_style.setter
    def quoting_style(self, value: dict):
        self._property_changed('quoting_style')
        self.__quoting_style = value        

    @property
    def scenario_group_id(self) -> dict:
        return self.__scenario_group_id

    @scenario_group_id.setter
    def scenario_group_id(self, value: dict):
        self._property_changed('scenario_group_id')
        self.__scenario_group_id = value        

    @property
    def asset_parameters_issuer_type(self) -> dict:
        return self.__asset_parameters_issuer_type

    @asset_parameters_issuer_type.setter
    def asset_parameters_issuer_type(self, value: dict):
        self._property_changed('asset_parameters_issuer_type')
        self.__asset_parameters_issuer_type = value        

    @property
    def sts_credit_market(self) -> dict:
        return self.__sts_credit_market

    @sts_credit_market.setter
    def sts_credit_market(self, value: dict):
        self._property_changed('sts_credit_market')
        self.__sts_credit_market = value        

    @property
    def bbid(self) -> dict:
        return self.__bbid

    @bbid.setter
    def bbid(self, value: dict):
        self._property_changed('bbid')
        self.__bbid = value        

    @property
    def asset_classifications_risk_country_code(self) -> dict:
        return self.__asset_classifications_risk_country_code

    @asset_classifications_risk_country_code.setter
    def asset_classifications_risk_country_code(self, value: dict):
        self._property_changed('asset_classifications_risk_country_code')
        self.__asset_classifications_risk_country_code = value        

    @property
    def sts_em_dm(self) -> dict:
        return self.__sts_em_dm

    @sts_em_dm.setter
    def sts_em_dm(self, value: dict):
        self._property_changed('sts_em_dm')
        self.__sts_em_dm = value        

    @property
    def issue_size(self) -> dict:
        return self.__issue_size

    @issue_size.setter
    def issue_size(self, value: dict):
        self._property_changed('issue_size')
        self.__issue_size = value        

    @property
    def returns_enabled(self) -> dict:
        return self.__returns_enabled

    @returns_enabled.setter
    def returns_enabled(self, value: dict):
        self._property_changed('returns_enabled')
        self.__returns_enabled = value        

    @property
    def seniority(self) -> dict:
        return self.__seniority

    @seniority.setter
    def seniority(self, value: dict):
        self._property_changed('seniority')
        self.__seniority = value        

    @property
    def asset_parameters_settlement(self) -> dict:
        return self.__asset_parameters_settlement

    @asset_parameters_settlement.setter
    def asset_parameters_settlement(self, value: dict):
        self._property_changed('asset_parameters_settlement')
        self.__asset_parameters_settlement = value        

    @property
    def primary_country_ric(self) -> dict:
        return self.__primary_country_ric

    @primary_country_ric.setter
    def primary_country_ric(self, value: dict):
        self._property_changed('primary_country_ric')
        self.__primary_country_ric = value        

    @property
    def is_pair_basket(self) -> dict:
        return self.__is_pair_basket

    @is_pair_basket.setter
    def is_pair_basket(self, value: dict):
        self._property_changed('is_pair_basket')
        self.__is_pair_basket = value        

    @property
    def default_backcast(self) -> dict:
        return self.__default_backcast

    @default_backcast.setter
    def default_backcast(self, value: dict):
        self._property_changed('default_backcast')
        self.__default_backcast = value        

    @property
    def use_machine_learning(self) -> dict:
        return self.__use_machine_learning

    @use_machine_learning.setter
    def use_machine_learning(self, value: dict):
        self._property_changed('use_machine_learning')
        self.__use_machine_learning = value        

    @property
    def performance_fee(self) -> dict:
        return self.__performance_fee

    @performance_fee.setter
    def performance_fee(self, value: dict):
        self._property_changed('performance_fee')
        self.__performance_fee = value        

    @property
    def report_type(self) -> dict:
        return self.__report_type

    @report_type.setter
    def report_type(self, value: dict):
        self._property_changed('report_type')
        self.__report_type = value        

    @property
    def underlying_asset_ids(self) -> dict:
        return self.__underlying_asset_ids

    @underlying_asset_ids.setter
    def underlying_asset_ids(self, value: dict):
        self._property_changed('underlying_asset_ids')
        self.__underlying_asset_ids = value        

    @property
    def encoded_stats(self) -> dict:
        return self.__encoded_stats

    @encoded_stats.setter
    def encoded_stats(self, value: dict):
        self._property_changed('encoded_stats')
        self.__encoded_stats = value        

    @property
    def pnode_id(self) -> dict:
        return self.__pnode_id

    @pnode_id.setter
    def pnode_id(self, value: dict):
        self._property_changed('pnode_id')
        self.__pnode_id = value        

    @property
    def backtest_type(self) -> dict:
        return self.__backtest_type

    @backtest_type.setter
    def backtest_type(self, value: dict):
        self._property_changed('backtest_type')
        self.__backtest_type = value        

    @property
    def asset_parameters_issuer(self) -> dict:
        return self.__asset_parameters_issuer

    @asset_parameters_issuer.setter
    def asset_parameters_issuer(self, value: dict):
        self._property_changed('asset_parameters_issuer')
        self.__asset_parameters_issuer = value        

    @property
    def exchange_code(self) -> dict:
        return self.__exchange_code

    @exchange_code.setter
    def exchange_code(self, value: dict):
        self._property_changed('exchange_code')
        self.__exchange_code = value        

    @property
    def asset_parameters_strike(self) -> dict:
        return self.__asset_parameters_strike

    @asset_parameters_strike.setter
    def asset_parameters_strike(self, value: dict):
        self._property_changed('asset_parameters_strike')
        self.__asset_parameters_strike = value        

    @property
    def asset_parameters_termination_date(self) -> dict:
        return self.__asset_parameters_termination_date

    @asset_parameters_termination_date.setter
    def asset_parameters_termination_date(self, value: dict):
        self._property_changed('asset_parameters_termination_date')
        self.__asset_parameters_termination_date = value        

    @property
    def resource(self) -> dict:
        return self.__resource

    @resource.setter
    def resource(self, value: dict):
        self._property_changed('resource')
        self.__resource = value        

    @property
    def bbid_equivalent(self) -> dict:
        return self.__bbid_equivalent

    @bbid_equivalent.setter
    def bbid_equivalent(self, value: dict):
        self._property_changed('bbid_equivalent')
        self.__bbid_equivalent = value        

    @property
    def asset_parameters_effective_date(self) -> dict:
        return self.__asset_parameters_effective_date

    @asset_parameters_effective_date.setter
    def asset_parameters_effective_date(self, value: dict):
        self._property_changed('asset_parameters_effective_date')
        self.__asset_parameters_effective_date = value        

    @property
    def valoren(self) -> dict:
        return self.__valoren

    @valoren.setter
    def valoren(self, value: dict):
        self._property_changed('valoren')
        self.__valoren = value        

    @property
    def asset_parameters_fixed_rate_day_count_fraction(self) -> dict:
        return self.__asset_parameters_fixed_rate_day_count_fraction

    @asset_parameters_fixed_rate_day_count_fraction.setter
    def asset_parameters_fixed_rate_day_count_fraction(self, value: dict):
        self._property_changed('asset_parameters_fixed_rate_day_count_fraction')
        self.__asset_parameters_fixed_rate_day_count_fraction = value        

    @property
    def auto_tags(self) -> dict:
        return self.__auto_tags

    @auto_tags.setter
    def auto_tags(self, value: dict):
        self._property_changed('auto_tags')
        self.__auto_tags = value        

    @property
    def short_description(self) -> dict:
        return self.__short_description

    @short_description.setter
    def short_description(self, value: dict):
        self._property_changed('short_description')
        self.__short_description = value        

    @property
    def ext_mkt_class(self) -> dict:
        return self.__ext_mkt_class

    @ext_mkt_class.setter
    def ext_mkt_class(self, value: dict):
        self._property_changed('ext_mkt_class')
        self.__ext_mkt_class = value        

    @property
    def mkt_point1(self) -> dict:
        return self.__mkt_point1

    @mkt_point1.setter
    def mkt_point1(self, value: dict):
        self._property_changed('mkt_point1')
        self.__mkt_point1 = value        

    @property
    def portfolio_managers(self) -> dict:
        return self.__portfolio_managers

    @portfolio_managers.setter
    def portfolio_managers(self, value: dict):
        self._property_changed('portfolio_managers')
        self.__portfolio_managers = value        

    @property
    def asset_parameters_commodity_sector(self) -> dict:
        return self.__asset_parameters_commodity_sector

    @asset_parameters_commodity_sector.setter
    def asset_parameters_commodity_sector(self, value: dict):
        self._property_changed('asset_parameters_commodity_sector')
        self.__asset_parameters_commodity_sector = value        

    @property
    def hedge_tracking_error(self) -> dict:
        return self.__hedge_tracking_error

    @hedge_tracking_error.setter
    def hedge_tracking_error(self, value: dict):
        self._property_changed('hedge_tracking_error')
        self.__hedge_tracking_error = value        

    @property
    def asset_parameters_coupon_type(self) -> dict:
        return self.__asset_parameters_coupon_type

    @asset_parameters_coupon_type.setter
    def asset_parameters_coupon_type(self, value: dict):
        self._property_changed('asset_parameters_coupon_type')
        self.__asset_parameters_coupon_type = value        

    @property
    def supra_strategy(self) -> dict:
        return self.__supra_strategy

    @supra_strategy.setter
    def supra_strategy(self, value: dict):
        self._property_changed('supra_strategy')
        self.__supra_strategy = value        

    @property
    def wi_id(self) -> dict:
        return self.__wi_id

    @wi_id.setter
    def wi_id(self, value: dict):
        self._property_changed('wi_id')
        self.__wi_id = value        

    @property
    def market_cap_category(self) -> dict:
        return self.__market_cap_category

    @market_cap_category.setter
    def market_cap_category(self, value: dict):
        self._property_changed('market_cap_category')
        self.__market_cap_category = value        

    @property
    def mkt_point3(self) -> dict:
        return self.__mkt_point3

    @mkt_point3.setter
    def mkt_point3(self, value: dict):
        self._property_changed('mkt_point3')
        self.__mkt_point3 = value        

    @property
    def mkt_point2(self) -> dict:
        return self.__mkt_point2

    @mkt_point2.setter
    def mkt_point2(self, value: dict):
        self._property_changed('mkt_point2')
        self.__mkt_point2 = value        

    @property
    def strike_price(self) -> dict:
        return self.__strike_price

    @strike_price.setter
    def strike_price(self, value: dict):
        self._property_changed('strike_price')
        self.__strike_price = value        

    @property
    def mkt_point4(self) -> dict:
        return self.__mkt_point4

    @mkt_point4.setter
    def mkt_point4(self, value: dict):
        self._property_changed('mkt_point4')
        self.__mkt_point4 = value        

    @property
    def units(self) -> dict:
        return self.__units

    @units.setter
    def units(self, value: dict):
        self._property_changed('units')
        self.__units = value        

    @property
    def em_id(self) -> dict:
        return self.__em_id

    @em_id.setter
    def em_id(self, value: dict):
        self._property_changed('em_id')
        self.__em_id = value        

    @property
    def sts_credit_region(self) -> dict:
        return self.__sts_credit_region

    @sts_credit_region.setter
    def sts_credit_region(self, value: dict):
        self._property_changed('sts_credit_region')
        self.__sts_credit_region = value        

    @property
    def ext_mkt_point3(self) -> dict:
        return self.__ext_mkt_point3

    @ext_mkt_point3.setter
    def ext_mkt_point3(self, value: dict):
        self._property_changed('ext_mkt_point3')
        self.__ext_mkt_point3 = value        

    @property
    def asset_classifications_risk_country_name(self) -> dict:
        return self.__asset_classifications_risk_country_name

    @asset_classifications_risk_country_name.setter
    def asset_classifications_risk_country_name(self, value: dict):
        self._property_changed('asset_classifications_risk_country_name')
        self.__asset_classifications_risk_country_name = value        

    @property
    def asset_parameters_vendor(self) -> dict:
        return self.__asset_parameters_vendor

    @asset_parameters_vendor.setter
    def asset_parameters_vendor(self, value: dict):
        self._property_changed('asset_parameters_vendor')
        self.__asset_parameters_vendor = value        

    @property
    def mkt_type(self) -> dict:
        return self.__mkt_type

    @mkt_type.setter
    def mkt_type(self, value: dict):
        self._property_changed('mkt_type')
        self.__mkt_type = value        

    @property
    def ext_mkt_point1(self) -> dict:
        return self.__ext_mkt_point1

    @ext_mkt_point1.setter
    def ext_mkt_point1(self, value: dict):
        self._property_changed('ext_mkt_point1')
        self.__ext_mkt_point1 = value        

    @property
    def product_type(self) -> dict:
        return self.__product_type

    @product_type.setter
    def product_type(self, value: dict):
        self._property_changed('product_type')
        self.__product_type = value        

    @property
    def sub_region_code(self) -> dict:
        return self.__sub_region_code

    @sub_region_code.setter
    def sub_region_code(self, value: dict):
        self._property_changed('sub_region_code')
        self.__sub_region_code = value        

    @property
    def ext_mkt_point2(self) -> dict:
        return self.__ext_mkt_point2

    @ext_mkt_point2.setter
    def ext_mkt_point2(self, value: dict):
        self._property_changed('ext_mkt_point2')
        self.__ext_mkt_point2 = value        

    @property
    def asset_parameters_fixed_rate(self) -> dict:
        return self.__asset_parameters_fixed_rate

    @asset_parameters_fixed_rate.setter
    def asset_parameters_fixed_rate(self, value: dict):
        self._property_changed('asset_parameters_fixed_rate')
        self.__asset_parameters_fixed_rate = value        

    @property
    def last_returns_end_date(self) -> dict:
        return self.__last_returns_end_date

    @last_returns_end_date.setter
    def last_returns_end_date(self, value: dict):
        self._property_changed('last_returns_end_date')
        self.__last_returns_end_date = value        

    @property
    def position_source_type(self) -> dict:
        return self.__position_source_type

    @position_source_type.setter
    def position_source_type(self, value: dict):
        self._property_changed('position_source_type')
        self.__position_source_type = value        

    @property
    def minimum_denomination(self) -> dict:
        return self.__minimum_denomination

    @minimum_denomination.setter
    def minimum_denomination(self, value: dict):
        self._property_changed('minimum_denomination')
        self.__minimum_denomination = value        

    @property
    def flagship(self) -> dict:
        return self.__flagship

    @flagship.setter
    def flagship(self, value: dict):
        self._property_changed('flagship')
        self.__flagship = value        

    @property
    def lms_id(self) -> dict:
        return self.__lms_id

    @lms_id.setter
    def lms_id(self, value: dict):
        self._property_changed('lms_id')
        self.__lms_id = value        

    @property
    def cross(self) -> dict:
        return self.__cross

    @cross.setter
    def cross(self, value: dict):
        self._property_changed('cross')
        self.__cross = value        

    @property
    def sts_rates_maturity(self) -> dict:
        return self.__sts_rates_maturity

    @sts_rates_maturity.setter
    def sts_rates_maturity(self, value: dict):
        self._property_changed('sts_rates_maturity')
        self.__sts_rates_maturity = value        

    @property
    def position_source(self) -> dict:
        return self.__position_source

    @position_source.setter
    def position_source(self, value: dict):
        self._property_changed('position_source')
        self.__position_source = value        

    @property
    def listed(self) -> dict:
        return self.__listed

    @listed.setter
    def listed(self, value: dict):
        self._property_changed('listed')
        self.__listed = value        

    @property
    def shock_style(self) -> dict:
        return self.__shock_style

    @shock_style.setter
    def shock_style(self, value: dict):
        self._property_changed('shock_style')
        self.__shock_style = value        

    @property
    def g10_currency(self) -> dict:
        return self.__g10_currency

    @g10_currency.setter
    def g10_currency(self, value: dict):
        self._property_changed('g10_currency')
        self.__g10_currency = value        

    @property
    def strategy(self) -> dict:
        return self.__strategy

    @strategy.setter
    def strategy(self, value: dict):
        self._property_changed('strategy')
        self.__strategy = value        

    @property
    def methodology(self) -> dict:
        return self.__methodology

    @methodology.setter
    def methodology(self, value: dict):
        self._property_changed('methodology')
        self.__methodology = value        

    @property
    def isin(self) -> dict:
        return self.__isin

    @isin.setter
    def isin(self, value: dict):
        self._property_changed('isin')
        self.__isin = value        


class FutureContract(Base):
        
    """A Future Contract"""

    @camel_case_translate
    def __init__(
        self,
        future_market_marquee_id: str = None,
        contract: str = None,
        name: str = None
    ):        
        super().__init__()
        self.future_market_marquee_id = future_market_marquee_id
        self.contract = contract
        self.name = name

    @property
    def future_market_marquee_id(self) -> str:
        """A unique identifier which associates the current asset with the Future Market
           asset in Marquee"""
        return self.__future_market_marquee_id

    @future_market_marquee_id.setter
    def future_market_marquee_id(self, value: str):
        self._property_changed('future_market_marquee_id')
        self.__future_market_marquee_id = value        

    @property
    def contract(self) -> str:
        """Strip which describes the contract - day/month"""
        return self.__contract

    @contract.setter
    def contract(self, value: str):
        self._property_changed('contract')
        self.__contract = value        


class FutureMarket(Base):
        
    """A Future Market"""

    @camel_case_translate
    def __init__(
        self,
        exchange: str = None,
        period_frequency: str = None,
        product_group: str = None,
        name: str = None
    ):        
        super().__init__()
        self.exchange = exchange
        self.period_frequency = period_frequency
        self.product_group = product_group
        self.name = name

    @property
    def exchange(self) -> str:
        """An exchange where future is listed"""
        return self.__exchange

    @exchange.setter
    def exchange(self, value: str):
        self._property_changed('exchange')
        self.__exchange = value        

    @property
    def period_frequency(self) -> str:
        """Frequency of contracts - daily/monthly/quarterly"""
        return self.__period_frequency

    @period_frequency.setter
    def period_frequency(self, value: str):
        self._property_changed('period_frequency')
        self.__period_frequency = value        

    @property
    def product_group(self) -> str:
        """The future group this represents"""
        return self.__product_group

    @product_group.setter
    def product_group(self, value: str):
        self._property_changed('product_group')
        self.__product_group = value        


class NumberRange(Base):
        
    """lower and upper bound to define a number range"""

    @camel_case_translate
    def __init__(
        self,
        lower_bound: float = None,
        upper_bound: float = None,
        name: str = None
    ):        
        super().__init__()
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.name = name

    @property
    def lower_bound(self) -> float:
        """value that defines the lower boundary of the range"""
        return self.__lower_bound

    @lower_bound.setter
    def lower_bound(self, value: float):
        self._property_changed('lower_bound')
        self.__lower_bound = value        

    @property
    def upper_bound(self) -> float:
        """value that defines the upper boundary of the range"""
        return self.__upper_bound

    @upper_bound.setter
    def upper_bound(self, value: float):
        self._property_changed('upper_bound')
        self.__upper_bound = value        


class People(Base):
        
    """People associated with an asset"""

    @camel_case_translate
    def __init__(
        self,
        portfolio_managers: Tuple[str, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.portfolio_managers = portfolio_managers
        self.name = name

    @property
    def portfolio_managers(self) -> Tuple[str, ...]:
        """Portfolio managers of asset"""
        return self.__portfolio_managers

    @portfolio_managers.setter
    def portfolio_managers(self, value: Tuple[str, ...]):
        self._property_changed('portfolio_managers')
        self.__portfolio_managers = value        


class PerformanceStatsRequest(Base):
        
    """Performance statistics."""

    @camel_case_translate
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
        average_return: Op = None,
        name: str = None
    ):        
        super().__init__()
        self.annualized_return = annualized_return
        self.annualized_volatility = annualized_volatility
        self.best_month = best_month
        self.max_draw_down = max_draw_down
        self.max_draw_down_duration = max_draw_down_duration
        self.positive_months = positive_months
        self.sharpe_ratio = sharpe_ratio
        self.sortino_ratio = sortino_ratio
        self.worst_month = worst_month
        self.average_return = average_return
        self.name = name

    @property
    def annualized_return(self) -> Op:
        """Operations for searches."""
        return self.__annualized_return

    @annualized_return.setter
    def annualized_return(self, value: Op):
        self._property_changed('annualized_return')
        self.__annualized_return = value        

    @property
    def annualized_volatility(self) -> Op:
        """Operations for searches."""
        return self.__annualized_volatility

    @annualized_volatility.setter
    def annualized_volatility(self, value: Op):
        self._property_changed('annualized_volatility')
        self.__annualized_volatility = value        

    @property
    def best_month(self) -> Op:
        """Operations for searches."""
        return self.__best_month

    @best_month.setter
    def best_month(self, value: Op):
        self._property_changed('best_month')
        self.__best_month = value        

    @property
    def max_draw_down(self) -> Op:
        """Operations for searches."""
        return self.__max_draw_down

    @max_draw_down.setter
    def max_draw_down(self, value: Op):
        self._property_changed('max_draw_down')
        self.__max_draw_down = value        

    @property
    def max_draw_down_duration(self) -> Op:
        """Operations for searches."""
        return self.__max_draw_down_duration

    @max_draw_down_duration.setter
    def max_draw_down_duration(self, value: Op):
        self._property_changed('max_draw_down_duration')
        self.__max_draw_down_duration = value        

    @property
    def positive_months(self) -> Op:
        """Operations for searches."""
        return self.__positive_months

    @positive_months.setter
    def positive_months(self, value: Op):
        self._property_changed('positive_months')
        self.__positive_months = value        

    @property
    def sharpe_ratio(self) -> Op:
        """Operations for searches."""
        return self.__sharpe_ratio

    @sharpe_ratio.setter
    def sharpe_ratio(self, value: Op):
        self._property_changed('sharpe_ratio')
        self.__sharpe_ratio = value        

    @property
    def sortino_ratio(self) -> Op:
        """Operations for searches."""
        return self.__sortino_ratio

    @sortino_ratio.setter
    def sortino_ratio(self, value: Op):
        self._property_changed('sortino_ratio')
        self.__sortino_ratio = value        

    @property
    def worst_month(self) -> Op:
        """Operations for searches."""
        return self.__worst_month

    @worst_month.setter
    def worst_month(self, value: Op):
        self._property_changed('worst_month')
        self.__worst_month = value        

    @property
    def average_return(self) -> Op:
        """Operations for searches."""
        return self.__average_return

    @average_return.setter
    def average_return(self, value: Op):
        self._property_changed('average_return')
        self.__average_return = value        


class SecuritiesLendingLoan(Base):
        
    """Parameters specific to a securities lending loan"""

    @camel_case_translate
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
        return_date: datetime.date = None,
        name: str = None
    ):        
        super().__init__()
        self.asset_id = asset_id
        self.fund_id = fund_id
        self.lender_id = lender_id
        self.borrower_id = borrower_id
        self.loan_status = loan_status
        self.settlement_status = settlement_status
        self.collateral_type = collateral_type
        self.loan_currency = loan_currency
        self.adjustment_ind = adjustment_ind
        self.country_of_issue = country_of_issue
        self.input_date = input_date
        self.effective_date = effective_date
        self.security_settle_date = security_settle_date
        self.cash_settle_date = cash_settle_date
        self.term_date = term_date
        self.return_date = return_date
        self.name = name

    @property
    def asset_id(self) -> str:
        """Id of the security being lent as part of this loan.  This Id should tie to an
           Asset"""
        return self.__asset_id

    @asset_id.setter
    def asset_id(self, value: str):
        self._property_changed('asset_id')
        self.__asset_id = value        

    @property
    def fund_id(self) -> str:
        """Id of the fund from which the loan is booked.  This Id should tie to an Asset"""
        return self.__fund_id

    @fund_id.setter
    def fund_id(self, value: str):
        self._property_changed('fund_id')
        self.__fund_id = value        

    @property
    def lender_id(self) -> str:
        """Id of the counterpart lending the security.  This Id should tie to a Company"""
        return self.__lender_id

    @lender_id.setter
    def lender_id(self, value: str):
        self._property_changed('lender_id')
        self.__lender_id = value        

    @property
    def borrower_id(self) -> str:
        """Id of the counterpart borrowing the security.  This Id should tie to a Company"""
        return self.__borrower_id

    @borrower_id.setter
    def borrower_id(self, value: str):
        self._property_changed('borrower_id')
        self.__borrower_id = value        

    @property
    def loan_status(self) -> str:
        """The current state of the loan"""
        return self.__loan_status

    @loan_status.setter
    def loan_status(self, value: str):
        self._property_changed('loan_status')
        self.__loan_status = value        

    @property
    def settlement_status(self) -> str:
        """State of the underlying components of the loan."""
        return self.__settlement_status

    @settlement_status.setter
    def settlement_status(self, value: str):
        self._property_changed('settlement_status')
        self.__settlement_status = value        

    @property
    def collateral_type(self) -> str:
        """Type of collateral used to collateralize the loan"""
        return self.__collateral_type

    @collateral_type.setter
    def collateral_type(self, value: str):
        self._property_changed('collateral_type')
        self.__collateral_type = value        

    @property
    def loan_currency(self) -> Union[Currency, str]:
        """Currency in which the loan value is represented"""
        return self.__loan_currency

    @loan_currency.setter
    def loan_currency(self, value: Union[Currency, str]):
        self._property_changed('loan_currency')
        self.__loan_currency = get_enum_value(Currency, value)        

    @property
    def adjustment_ind(self) -> bool:
        """Defines whether or not this contract is for the purpose of a month end loan
           adjustment."""
        return self.__adjustment_ind

    @adjustment_ind.setter
    def adjustment_ind(self, value: bool):
        self._property_changed('adjustment_ind')
        self.__adjustment_ind = value        

    @property
    def country_of_issue(self) -> str:
        """The country code (ISO 3166) of the underlying security"""
        return self.__country_of_issue

    @country_of_issue.setter
    def country_of_issue(self, value: str):
        self._property_changed('country_of_issue')
        self.__country_of_issue = value        

    @property
    def input_date(self) -> datetime.date:
        """Date that the loan is booked"""
        return self.__input_date

    @input_date.setter
    def input_date(self, value: datetime.date):
        self._property_changed('input_date')
        self.__input_date = value        

    @property
    def effective_date(self) -> datetime.date:
        """Date of the trade"""
        return self.__effective_date

    @effective_date.setter
    def effective_date(self, value: datetime.date):
        self._property_changed('effective_date')
        self.__effective_date = value        

    @property
    def security_settle_date(self) -> datetime.date:
        """Date that the loaned securities settled"""
        return self.__security_settle_date

    @security_settle_date.setter
    def security_settle_date(self, value: datetime.date):
        self._property_changed('security_settle_date')
        self.__security_settle_date = value        

    @property
    def cash_settle_date(self) -> datetime.date:
        """Date of the cash collateral settled"""
        return self.__cash_settle_date

    @cash_settle_date.setter
    def cash_settle_date(self, value: datetime.date):
        self._property_changed('cash_settle_date')
        self.__cash_settle_date = value        

    @property
    def term_date(self) -> datetime.date:
        """Date the dividend is paid for dividend based loans"""
        return self.__term_date

    @term_date.setter
    def term_date(self, value: datetime.date):
        self._property_changed('term_date')
        self.__term_date = value        

    @property
    def return_date(self) -> datetime.date:
        """Date the loan is returned"""
        return self.__return_date

    @return_date.setter
    def return_date(self, value: datetime.date):
        self._property_changed('return_date')
        self.__return_date = value        


class TemporalXRef(Base):
        
    @camel_case_translate
    def __init__(
        self,
        start_date: datetime.date = None,
        end_date: datetime.date = None,
        identifiers: XRef = None,
        name: str = None
    ):        
        super().__init__()
        self.start_date = start_date
        self.end_date = end_date
        self.identifiers = identifiers
        self.name = name

    @property
    def start_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__start_date

    @start_date.setter
    def start_date(self, value: datetime.date):
        self._property_changed('start_date')
        self.__start_date = value        

    @property
    def end_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__end_date

    @end_date.setter
    def end_date(self, value: datetime.date):
        self._property_changed('end_date')
        self.__end_date = value        

    @property
    def identifiers(self) -> XRef:
        return self.__identifiers

    @identifiers.setter
    def identifiers(self, value: XRef):
        self._property_changed('identifiers')
        self.__identifiers = value        


class WeatherIndexParameters(Base):
        
    """parameters specific to weather index data underlier"""

    @camel_case_translate
    def __init__(
        self,
        data_provider: str = None,
        weather_station: str = None,
        reference_level_amount: float = None,
        reference_level_unit: str = None,
        weather_station_fallback: str = None,
        weather_station_second_fallback: str = None,
        alternative_data_provider: str = None,
        synoptic_data_fallback: str = None,
        adjustment_to_fallback_weather_station: str = None,
        primary_disruption_fallbacks: str = None,
        secondary_disruption_fallbacks: str = None,
        final_edited_data: bool = None,
        name: str = None
    ):        
        super().__init__()
        self.data_provider = data_provider
        self.weather_station = weather_station
        self.reference_level_amount = reference_level_amount
        self.reference_level_unit = reference_level_unit
        self.weather_station_fallback = weather_station_fallback
        self.weather_station_second_fallback = weather_station_second_fallback
        self.alternative_data_provider = alternative_data_provider
        self.synoptic_data_fallback = synoptic_data_fallback
        self.adjustment_to_fallback_weather_station = adjustment_to_fallback_weather_station
        self.primary_disruption_fallbacks = primary_disruption_fallbacks
        self.secondary_disruption_fallbacks = secondary_disruption_fallbacks
        self.final_edited_data = final_edited_data
        self.name = name

    @property
    def data_provider(self) -> str:
        """Weather index data provider"""
        return self.__data_provider

    @data_provider.setter
    def data_provider(self, value: str):
        self._property_changed('data_provider')
        self.__data_provider = value        

    @property
    def weather_station(self) -> str:
        """Weather index data source"""
        return self.__weather_station

    @weather_station.setter
    def weather_station(self, value: str):
        self._property_changed('weather_station')
        self.__weather_station = value        

    @property
    def reference_level_amount(self) -> float:
        """Number on which degree days or CPD differential is calculated"""
        return self.__reference_level_amount

    @reference_level_amount.setter
    def reference_level_amount(self, value: float):
        self._property_changed('reference_level_amount')
        self.__reference_level_amount = value        

    @property
    def reference_level_unit(self) -> str:
        """Unit of reference level"""
        return self.__reference_level_unit

    @reference_level_unit.setter
    def reference_level_unit(self, value: str):
        self._property_changed('reference_level_unit')
        self.__reference_level_unit = value        

    @property
    def weather_station_fallback(self) -> str:
        """First alternative Weather Index Station"""
        return self.__weather_station_fallback

    @weather_station_fallback.setter
    def weather_station_fallback(self, value: str):
        self._property_changed('weather_station_fallback')
        self.__weather_station_fallback = value        

    @property
    def weather_station_second_fallback(self) -> str:
        """Second alternative Weather Index Station"""
        return self.__weather_station_second_fallback

    @weather_station_second_fallback.setter
    def weather_station_second_fallback(self, value: str):
        self._property_changed('weather_station_second_fallback')
        self.__weather_station_second_fallback = value        

    @property
    def alternative_data_provider(self) -> str:
        """Alternative weather Data Provider"""
        return self.__alternative_data_provider

    @alternative_data_provider.setter
    def alternative_data_provider(self, value: str):
        self._property_changed('alternative_data_provider')
        self.__alternative_data_provider = value        

    @property
    def synoptic_data_fallback(self) -> str:
        """Alternative weather synoptic data location"""
        return self.__synoptic_data_fallback

    @synoptic_data_fallback.setter
    def synoptic_data_fallback(self, value: str):
        self._property_changed('synoptic_data_fallback')
        self.__synoptic_data_fallback = value        

    @property
    def adjustment_to_fallback_weather_station(self) -> str:
        """Weather station applicable to Adjustment Fallback Station Data terms"""
        return self.__adjustment_to_fallback_weather_station

    @adjustment_to_fallback_weather_station.setter
    def adjustment_to_fallback_weather_station(self, value: str):
        self._property_changed('adjustment_to_fallback_weather_station')
        self.__adjustment_to_fallback_weather_station = value        

    @property
    def primary_disruption_fallbacks(self) -> str:
        """Actions available following a weather Primary Disruption Event"""
        return self.__primary_disruption_fallbacks

    @primary_disruption_fallbacks.setter
    def primary_disruption_fallbacks(self, value: str):
        self._property_changed('primary_disruption_fallbacks')
        self.__primary_disruption_fallbacks = value        

    @property
    def secondary_disruption_fallbacks(self) -> str:
        """Actions available following a weather Secondary Disruption Event"""
        return self.__secondary_disruption_fallbacks

    @secondary_disruption_fallbacks.setter
    def secondary_disruption_fallbacks(self, value: str):
        self._property_changed('secondary_disruption_fallbacks')
        self.__secondary_disruption_fallbacks = value        

    @property
    def final_edited_data(self) -> bool:
        """Invoke Primary Disruption Fallbacks if weather data is not in final edited form"""
        return self.__final_edited_data

    @final_edited_data.setter
    def final_edited_data(self, value: bool):
        self._property_changed('final_edited_data')
        self.__final_edited_data = value        


class AssetParameters(Base):
        
    """Parameters specific to the asset type"""

    @camel_case_translate
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
        strike_price: Union[float, str] = None,
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
        callable_: bool = None,
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
        index_approval_ids: Tuple[str, ...] = None,
        is_pair_basket: bool = None,
        is_legacy_pair_basket: bool = None,
        fixed_rate_day_count_fraction: Union[DayCountFraction, str] = None,
        floating_rate_day_count_fraction: Union[DayCountFraction, str] = None,
        pay_day_count_fraction: Union[DayCountFraction, str] = None,
        receive_day_count_fraction: Union[DayCountFraction, str] = None,
        pay_frequency: str = None,
        receive_frequency: str = None,
        resettable_leg: Union[PayReceive, str] = None,
        inflation_lag: str = None,
        fx_index: str = None,
        index_notes: str = None,
        index_not_trading_reasons: Union[IndexNotTradingReasons, str] = None,
        trade_as: str = None,
        clone_parent_id: str = None,
        on_behalf_of: str = None,
        index_calculation_agent: str = None,
        product_type: Union[ProductType, str] = None,
        vendor: str = None,
        call_first_date: datetime.date = None,
        call_last_date: datetime.date = None,
        amount_outstanding: float = None,
        covered_bond: bool = None,
        issue_status: str = None,
        issue_status_date: datetime.date = None,
        issue_price: float = None,
        sinkable: bool = None,
        sink_factor: float = None,
        accrued_interest_standard: float = None,
        redemption_date: datetime.date = None,
        redemption_price: float = None,
        private_placement_type: str = None,
        minimum_piece: float = None,
        minimum_increment: float = None,
        minimum_denomination: float = None,
        default_backcast: bool = None,
        name: str = None
    ):        
        super().__init__()
        self.basket_type = basket_type
        self.style = style
        self.index_calculation_type = index_calculation_type
        self.index_return_type = index_return_type
        self.index_divisor = index_divisor
        self.currency = currency
        self.quote_currency = quote_currency
        self.index_initial_price = index_initial_price
        self.initial_pricing_date = initial_pricing_date
        self.expiration_date = expiration_date
        self.expiration_location = expiration_location
        self.option_style = option_style
        self.option_type = option_type
        self.settlement_date = settlement_date
        self.settlement_type = settlement_type
        self.strike_price = strike_price
        self.put_currency = put_currency
        self.put_amount = put_amount
        self.automatic_exercise = automatic_exercise
        self.call_amount = call_amount
        self.call_currency = call_currency
        self.exercise_time = exercise_time
        self.multiplier = multiplier
        self.premium_payment_date = premium_payment_date
        self.premium = premium
        self.premium_currency = premium_currency
        self.__callable = callable_
        self.puttable = puttable
        self.perpetual = perpetual
        self.seniority = seniority
        self.coupon_type = coupon_type
        self.index = index
        self.index_term = index_term
        self.index_margin = index_margin
        self.coupon = coupon
        self.issue_date = issue_date
        self.issuer = issuer
        self.issuer_country_code = issuer_country_code
        self.issuer_type = issuer_type
        self.issue_size = issue_size
        self.commodity_sector = commodity_sector
        self.pricing_location = pricing_location
        self.contract_months = contract_months
        self.g10_currency = g10_currency
        self.hedge_id = hedge_id
        self.ultimate_ticker = ultimate_ticker
        self.strategy = strategy
        self.supra_strategy = supra_strategy
        self.exchange_currency = exchange_currency
        self.region = region
        self.delivery_point = delivery_point
        self.pricing_index = pricing_index
        self.contract_month = contract_month
        self.load_type = load_type
        self.contract_unit = contract_unit
        self.index_approval_ids = index_approval_ids
        self.is_pair_basket = is_pair_basket
        self.is_legacy_pair_basket = is_legacy_pair_basket
        self.fixed_rate_day_count_fraction = fixed_rate_day_count_fraction
        self.floating_rate_day_count_fraction = floating_rate_day_count_fraction
        self.pay_day_count_fraction = pay_day_count_fraction
        self.receive_day_count_fraction = receive_day_count_fraction
        self.pay_frequency = pay_frequency
        self.receive_frequency = receive_frequency
        self.resettable_leg = resettable_leg
        self.inflation_lag = inflation_lag
        self.fx_index = fx_index
        self.index_notes = index_notes
        self.index_not_trading_reasons = index_not_trading_reasons
        self.trade_as = trade_as
        self.clone_parent_id = clone_parent_id
        self.on_behalf_of = on_behalf_of
        self.index_calculation_agent = index_calculation_agent
        self.product_type = product_type
        self.vendor = vendor
        self.call_first_date = call_first_date
        self.call_last_date = call_last_date
        self.amount_outstanding = amount_outstanding
        self.covered_bond = covered_bond
        self.issue_status = issue_status
        self.issue_status_date = issue_status_date
        self.issue_price = issue_price
        self.sinkable = sinkable
        self.sink_factor = sink_factor
        self.accrued_interest_standard = accrued_interest_standard
        self.redemption_date = redemption_date
        self.redemption_price = redemption_price
        self.private_placement_type = private_placement_type
        self.minimum_piece = minimum_piece
        self.minimum_increment = minimum_increment
        self.minimum_denomination = minimum_denomination
        self.default_backcast = default_backcast
        self.name = name

    @property
    def basket_type(self) -> str:
        """Type of basket / implementation"""
        return self.__basket_type

    @basket_type.setter
    def basket_type(self, value: str):
        self._property_changed('basket_type')
        self.__basket_type = value        

    @property
    def style(self) -> str:
        """Asset style"""
        return self.__style

    @style.setter
    def style(self, value: str):
        self._property_changed('style')
        self.__style = value        

    @property
    def attribution_dataset_id(self) -> str:
        """Identifier of dataset which provides performance attribution data"""
        return 'STSATTR'        

    @property
    def index_calculation_type(self) -> str:
        """Determines the index calculation methodology with respect to dividend
           reinvestment"""
        return self.__index_calculation_type

    @index_calculation_type.setter
    def index_calculation_type(self, value: str):
        self._property_changed('index_calculation_type')
        self.__index_calculation_type = value        

    @property
    def index_return_type(self) -> str:
        """Determines the return calculation type method with respect to cash accrual /
           funding"""
        return self.__index_return_type

    @index_return_type.setter
    def index_return_type(self, value: str):
        self._property_changed('index_return_type')
        self.__index_return_type = value        

    @property
    def index_divisor(self) -> float:
        """Divisor to be applied to the overall position set of the index"""
        return self.__index_divisor

    @index_divisor.setter
    def index_divisor(self, value: float):
        self._property_changed('index_divisor')
        self.__index_divisor = value        

    @property
    def currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self._property_changed('currency')
        self.__currency = get_enum_value(Currency, value)        

    @property
    def quote_currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__quote_currency

    @quote_currency.setter
    def quote_currency(self, value: Union[Currency, str]):
        self._property_changed('quote_currency')
        self.__quote_currency = get_enum_value(Currency, value)        

    @property
    def index_initial_price(self) -> float:
        """Initial Price for the Index"""
        return self.__index_initial_price

    @index_initial_price.setter
    def index_initial_price(self, value: float):
        self._property_changed('index_initial_price')
        self.__index_initial_price = value        

    @property
    def initial_pricing_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__initial_pricing_date

    @initial_pricing_date.setter
    def initial_pricing_date(self, value: datetime.date):
        self._property_changed('initial_pricing_date')
        self.__initial_pricing_date = value        

    @property
    def expiration_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, value: datetime.date):
        self._property_changed('expiration_date')
        self.__expiration_date = value        

    @property
    def expiration_location(self) -> str:
        return self.__expiration_location

    @expiration_location.setter
    def expiration_location(self, value: str):
        self._property_changed('expiration_location')
        self.__expiration_location = value        

    @property
    def option_style(self) -> str:
        return self.__option_style

    @option_style.setter
    def option_style(self, value: str):
        self._property_changed('option_style')
        self.__option_style = value        

    @property
    def option_type(self) -> Union[OptionType, str]:
        """Option Type"""
        return self.__option_type

    @option_type.setter
    def option_type(self, value: Union[OptionType, str]):
        self._property_changed('option_type')
        self.__option_type = get_enum_value(OptionType, value)        

    @property
    def settlement_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__settlement_date

    @settlement_date.setter
    def settlement_date(self, value: datetime.date):
        self._property_changed('settlement_date')
        self.__settlement_date = value        

    @property
    def settlement_type(self) -> str:
        return self.__settlement_type

    @settlement_type.setter
    def settlement_type(self, value: str):
        self._property_changed('settlement_type')
        self.__settlement_type = value        

    @property
    def strike_price(self) -> Union[float, str]:
        return self.__strike_price

    @strike_price.setter
    def strike_price(self, value: Union[float, str]):
        self._property_changed('strike_price')
        self.__strike_price = value        

    @property
    def put_currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__put_currency

    @put_currency.setter
    def put_currency(self, value: Union[Currency, str]):
        self._property_changed('put_currency')
        self.__put_currency = get_enum_value(Currency, value)        

    @property
    def put_amount(self) -> float:
        return self.__put_amount

    @put_amount.setter
    def put_amount(self, value: float):
        self._property_changed('put_amount')
        self.__put_amount = value        

    @property
    def automatic_exercise(self) -> bool:
        return self.__automatic_exercise

    @automatic_exercise.setter
    def automatic_exercise(self, value: bool):
        self._property_changed('automatic_exercise')
        self.__automatic_exercise = value        

    @property
    def call_amount(self) -> float:
        return self.__call_amount

    @call_amount.setter
    def call_amount(self, value: float):
        self._property_changed('call_amount')
        self.__call_amount = value        

    @property
    def call_currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__call_currency

    @call_currency.setter
    def call_currency(self, value: Union[Currency, str]):
        self._property_changed('call_currency')
        self.__call_currency = get_enum_value(Currency, value)        

    @property
    def exercise_time(self) -> str:
        """Time at which the asset can be exercised"""
        return self.__exercise_time

    @exercise_time.setter
    def exercise_time(self, value: str):
        self._property_changed('exercise_time')
        self.__exercise_time = value        

    @property
    def multiplier(self) -> float:
        """Underlying unit per asset multiplier"""
        return self.__multiplier

    @multiplier.setter
    def multiplier(self, value: float):
        self._property_changed('multiplier')
        self.__multiplier = value        

    @property
    def premium_payment_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__premium_payment_date

    @premium_payment_date.setter
    def premium_payment_date(self, value: datetime.date):
        self._property_changed('premium_payment_date')
        self.__premium_payment_date = value        

    @property
    def premium(self) -> float:
        return self.__premium

    @premium.setter
    def premium(self, value: float):
        self._property_changed('premium')
        self.__premium = value        

    @property
    def premium_currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__premium_currency

    @premium_currency.setter
    def premium_currency(self, value: Union[Currency, str]):
        self._property_changed('premium_currency')
        self.__premium_currency = get_enum_value(Currency, value)        

    @property
    def callable(self) -> bool:
        """Bond is callable"""
        return self.__callable

    @callable.setter
    def callable(self, value: bool):
        self._property_changed('callable')
        self.__callable = value        

    @property
    def puttable(self) -> bool:
        """Bond is puttable"""
        return self.__puttable

    @puttable.setter
    def puttable(self, value: bool):
        self._property_changed('puttable')
        self.__puttable = value        

    @property
    def perpetual(self) -> bool:
        """Bond is a perpetual"""
        return self.__perpetual

    @perpetual.setter
    def perpetual(self, value: bool):
        self._property_changed('perpetual')
        self.__perpetual = value        

    @property
    def seniority(self) -> str:
        """The seniority of the bond"""
        return self.__seniority

    @seniority.setter
    def seniority(self, value: str):
        self._property_changed('seniority')
        self.__seniority = value        

    @property
    def coupon_type(self) -> str:
        """The coupon type of the bond"""
        return self.__coupon_type

    @coupon_type.setter
    def coupon_type(self, value: str):
        self._property_changed('coupon_type')
        self.__coupon_type = value        

    @property
    def index(self) -> str:
        """The rate index (e.g. USD-LIBOR-BBA) for the floating rate coupon of this bond"""
        return self.__index

    @index.setter
    def index(self, value: str):
        self._property_changed('index')
        self.__index = value        

    @property
    def index_term(self) -> str:
        """The term of rate index (e.g. USD-LIBOR-BBA) for the floating rate coupon of this
           bond"""
        return self.__index_term

    @index_term.setter
    def index_term(self, value: str):
        self._property_changed('index_term')
        self.__index_term = value        

    @property
    def index_margin(self) -> float:
        """The spread over the rate index (e.g. USD-LIBOR-BBA) for the floating rate coupon
           of this bond"""
        return self.__index_margin

    @index_margin.setter
    def index_margin(self, value: float):
        self._property_changed('index_margin')
        self.__index_margin = value        

    @property
    def coupon(self) -> float:
        """The fixed coupon for this bond"""
        return self.__coupon

    @coupon.setter
    def coupon(self, value: float):
        self._property_changed('coupon')
        self.__coupon = value        

    @property
    def issue_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__issue_date

    @issue_date.setter
    def issue_date(self, value: datetime.date):
        self._property_changed('issue_date')
        self.__issue_date = value        

    @property
    def issuer(self) -> str:
        """The issuer of this bond"""
        return self.__issuer

    @issuer.setter
    def issuer(self, value: str):
        self._property_changed('issuer')
        self.__issuer = value        

    @property
    def issuer_country_code(self) -> str:
        """The country code (ISO 3166) in which this bond was issued"""
        return self.__issuer_country_code

    @issuer_country_code.setter
    def issuer_country_code(self, value: str):
        self._property_changed('issuer_country_code')
        self.__issuer_country_code = value        

    @property
    def issuer_type(self) -> str:
        """The type of the bond issuer"""
        return self.__issuer_type

    @issuer_type.setter
    def issuer_type(self, value: str):
        self._property_changed('issuer_type')
        self.__issuer_type = value        

    @property
    def issue_size(self) -> float:
        """The notional issue size of the bond"""
        return self.__issue_size

    @issue_size.setter
    def issue_size(self, value: float):
        self._property_changed('issue_size')
        self.__issue_size = value        

    @property
    def commodity_sector(self) -> Union[CommoditySector, str]:
        """The sector of the commodity"""
        return self.__commodity_sector

    @commodity_sector.setter
    def commodity_sector(self, value: Union[CommoditySector, str]):
        self._property_changed('commodity_sector')
        self.__commodity_sector = get_enum_value(CommoditySector, value)        

    @property
    def pricing_location(self) -> Union[PricingLocation, str]:
        """Based on the location of the exchange. Called 'Native Region' in SecDB"""
        return self.__pricing_location

    @pricing_location.setter
    def pricing_location(self, value: Union[PricingLocation, str]):
        self._property_changed('pricing_location')
        self.__pricing_location = get_enum_value(PricingLocation, value)        

    @property
    def contract_months(self) -> Tuple[str, ...]:
        """Contract months"""
        return self.__contract_months

    @contract_months.setter
    def contract_months(self, value: Tuple[str, ...]):
        self._property_changed('contract_months')
        self.__contract_months = value        

    @property
    def g10_currency(self) -> bool:
        """Is a G10 asset."""
        return self.__g10_currency

    @g10_currency.setter
    def g10_currency(self, value: bool):
        self._property_changed('g10_currency')
        self.__g10_currency = value        

    @property
    def hedge_id(self) -> str:
        """Marquee unique identifier"""
        return self.__hedge_id

    @hedge_id.setter
    def hedge_id(self, value: str):
        self._property_changed('hedge_id')
        self.__hedge_id = value        

    @property
    def ultimate_ticker(self) -> str:
        """The ultimate ticker for this security (e.g. SPXW)"""
        return self.__ultimate_ticker

    @ultimate_ticker.setter
    def ultimate_ticker(self, value: str):
        self._property_changed('ultimate_ticker')
        self.__ultimate_ticker = value        

    @property
    def strategy(self) -> Union[Strategy, str]:
        """More specific descriptor of a fund's investment approach. Same view permissions
           as the asset"""
        return self.__strategy

    @strategy.setter
    def strategy(self, value: Union[Strategy, str]):
        self._property_changed('strategy')
        self.__strategy = get_enum_value(Strategy, value)        

    @property
    def supra_strategy(self) -> Union[SupraStrategy, str]:
        """Broad descriptor of a fund's investment approach. Same view permissions as the
           asset"""
        return self.__supra_strategy

    @supra_strategy.setter
    def supra_strategy(self, value: Union[SupraStrategy, str]):
        self._property_changed('supra_strategy')
        self.__supra_strategy = get_enum_value(SupraStrategy, value)        

    @property
    def exchange_currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__exchange_currency

    @exchange_currency.setter
    def exchange_currency(self, value: Union[Currency, str]):
        self._property_changed('exchange_currency')
        self.__exchange_currency = get_enum_value(Currency, value)        

    @property
    def region(self) -> str:
        return self.__region

    @region.setter
    def region(self, value: str):
        self._property_changed('region')
        self.__region = value        

    @property
    def delivery_point(self) -> str:
        return self.__delivery_point

    @delivery_point.setter
    def delivery_point(self, value: str):
        self._property_changed('delivery_point')
        self.__delivery_point = value        

    @property
    def pricing_index(self) -> str:
        return self.__pricing_index

    @pricing_index.setter
    def pricing_index(self, value: str):
        self._property_changed('pricing_index')
        self.__pricing_index = value        

    @property
    def contract_month(self) -> str:
        return self.__contract_month

    @contract_month.setter
    def contract_month(self, value: str):
        self._property_changed('contract_month')
        self.__contract_month = value        

    @property
    def load_type(self) -> str:
        return self.__load_type

    @load_type.setter
    def load_type(self, value: str):
        self._property_changed('load_type')
        self.__load_type = value        

    @property
    def contract_unit(self) -> str:
        return self.__contract_unit

    @contract_unit.setter
    def contract_unit(self, value: str):
        self._property_changed('contract_unit')
        self.__contract_unit = value        

    @property
    def index_approval_ids(self) -> Tuple[str, ...]:
        """Array of approval identifiers related to the object"""
        return self.__index_approval_ids

    @index_approval_ids.setter
    def index_approval_ids(self, value: Tuple[str, ...]):
        self._property_changed('index_approval_ids')
        self.__index_approval_ids = value        

    @property
    def is_pair_basket(self) -> bool:
        return self.__is_pair_basket

    @is_pair_basket.setter
    def is_pair_basket(self, value: bool):
        self._property_changed('is_pair_basket')
        self.__is_pair_basket = value        

    @property
    def is_legacy_pair_basket(self) -> bool:
        return self.__is_legacy_pair_basket

    @is_legacy_pair_basket.setter
    def is_legacy_pair_basket(self, value: bool):
        self._property_changed('is_legacy_pair_basket')
        self.__is_legacy_pair_basket = value        

    @property
    def fixed_rate_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """Default day count fraction for fixed legs"""
        return self.__fixed_rate_day_count_fraction

    @fixed_rate_day_count_fraction.setter
    def fixed_rate_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self._property_changed('fixed_rate_day_count_fraction')
        self.__fixed_rate_day_count_fraction = get_enum_value(DayCountFraction, value)        

    @property
    def floating_rate_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """Default day count fraction for floating legs"""
        return self.__floating_rate_day_count_fraction

    @floating_rate_day_count_fraction.setter
    def floating_rate_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self._property_changed('floating_rate_day_count_fraction')
        self.__floating_rate_day_count_fraction = get_enum_value(DayCountFraction, value)        

    @property
    def pay_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """Default day count fraction for pay leg"""
        return self.__pay_day_count_fraction

    @pay_day_count_fraction.setter
    def pay_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self._property_changed('pay_day_count_fraction')
        self.__pay_day_count_fraction = get_enum_value(DayCountFraction, value)        

    @property
    def receive_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """Default day count fraction for the receive leg"""
        return self.__receive_day_count_fraction

    @receive_day_count_fraction.setter
    def receive_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self._property_changed('receive_day_count_fraction')
        self.__receive_day_count_fraction = get_enum_value(DayCountFraction, value)        

    @property
    def pay_frequency(self) -> str:
        """Default frequency of the pay leg"""
        return self.__pay_frequency

    @pay_frequency.setter
    def pay_frequency(self, value: str):
        self._property_changed('pay_frequency')
        self.__pay_frequency = value        

    @property
    def receive_frequency(self) -> str:
        """Default frequency of the receive leg"""
        return self.__receive_frequency

    @receive_frequency.setter
    def receive_frequency(self, value: str):
        self._property_changed('receive_frequency')
        self.__receive_frequency = value        

    @property
    def resettable_leg(self) -> Union[PayReceive, str]:
        """Resettable leg"""
        return self.__resettable_leg

    @resettable_leg.setter
    def resettable_leg(self, value: Union[PayReceive, str]):
        self._property_changed('resettable_leg')
        self.__resettable_leg = get_enum_value(PayReceive, value)        

    @property
    def inflation_lag(self) -> str:
        """Inflation lag"""
        return self.__inflation_lag

    @inflation_lag.setter
    def inflation_lag(self, value: str):
        self._property_changed('inflation_lag')
        self.__inflation_lag = value        

    @property
    def fx_index(self) -> str:
        """FX index"""
        return self.__fx_index

    @fx_index.setter
    def fx_index(self, value: str):
        self._property_changed('fx_index')
        self.__fx_index = value        

    @property
    def index_notes(self) -> str:
        """Notes for the index"""
        return self.__index_notes

    @index_notes.setter
    def index_notes(self, value: str):
        self._property_changed('index_notes')
        self.__index_notes = value        

    @property
    def index_not_trading_reasons(self) -> Union[IndexNotTradingReasons, str]:
        """Reasons the index was not traded"""
        return self.__index_not_trading_reasons

    @index_not_trading_reasons.setter
    def index_not_trading_reasons(self, value: Union[IndexNotTradingReasons, str]):
        self._property_changed('index_not_trading_reasons')
        self.__index_not_trading_reasons = get_enum_value(IndexNotTradingReasons, value)        

    @property
    def trade_as(self) -> str:
        """How to trade the Option."""
        return self.__trade_as

    @trade_as.setter
    def trade_as(self, value: str):
        self._property_changed('trade_as')
        self.__trade_as = value        

    @property
    def clone_parent_id(self) -> str:
        """Marquee unique identifier"""
        return self.__clone_parent_id

    @clone_parent_id.setter
    def clone_parent_id(self, value: str):
        self._property_changed('clone_parent_id')
        self.__clone_parent_id = value        

    @property
    def on_behalf_of(self) -> str:
        """Marquee unique identifier"""
        return self.__on_behalf_of

    @on_behalf_of.setter
    def on_behalf_of(self, value: str):
        self._property_changed('on_behalf_of')
        self.__on_behalf_of = value        

    @property
    def index_calculation_agent(self) -> str:
        """Calculation agent of the index."""
        return self.__index_calculation_agent

    @index_calculation_agent.setter
    def index_calculation_agent(self, value: str):
        self._property_changed('index_calculation_agent')
        self.__index_calculation_agent = value        

    @property
    def product_type(self) -> Union[ProductType, str]:
        """Basket Product Type."""
        return self.__product_type

    @product_type.setter
    def product_type(self, value: Union[ProductType, str]):
        self._property_changed('product_type')
        self.__product_type = get_enum_value(ProductType, value)        

    @property
    def vendor(self) -> str:
        """Basket Vendor OEID."""
        return self.__vendor

    @vendor.setter
    def vendor(self, value: str):
        self._property_changed('vendor')
        self.__vendor = value        

    @property
    def call_first_date(self) -> datetime.date:
        """The first date which you call the bond."""
        return self.__call_first_date

    @call_first_date.setter
    def call_first_date(self, value: datetime.date):
        self._property_changed('call_first_date')
        self.__call_first_date = value        

    @property
    def call_last_date(self) -> datetime.date:
        """The first date which you call the bond."""
        return self.__call_last_date

    @call_last_date.setter
    def call_last_date(self, value: datetime.date):
        self._property_changed('call_last_date')
        self.__call_last_date = value        

    @property
    def amount_outstanding(self) -> float:
        """The aggregate principal amount of the total number of bonds not redeemed or
           otherwise discharged."""
        return self.__amount_outstanding

    @amount_outstanding.setter
    def amount_outstanding(self, value: float):
        self._property_changed('amount_outstanding')
        self.__amount_outstanding = value        

    @property
    def covered_bond(self) -> bool:
        """Whether the debt security is collateralized against a pool of assets that, in
           case of failure of the issuer, can cover claims at any point of time."""
        return self.__covered_bond

    @covered_bond.setter
    def covered_bond(self, value: bool):
        self._property_changed('covered_bond')
        self.__covered_bond = value        

    @property
    def issue_status(self) -> str:
        """Status of the issue."""
        return self.__issue_status

    @issue_status.setter
    def issue_status(self, value: str):
        self._property_changed('issue_status')
        self.__issue_status = value        

    @property
    def issue_status_date(self) -> datetime.date:
        """Date at which the status was given to the issue."""
        return self.__issue_status_date

    @issue_status_date.setter
    def issue_status_date(self, value: datetime.date):
        self._property_changed('issue_status_date')
        self.__issue_status_date = value        

    @property
    def issue_price(self) -> float:
        """The price for which the instrument is issued"""
        return self.__issue_price

    @issue_price.setter
    def issue_price(self, value: float):
        self._property_changed('issue_price')
        self.__issue_price = value        

    @property
    def sinkable(self) -> bool:
        """A bond that is protected by a fund (called a sinking fund) that sets aside money
           to ensure principal and interest payments are made by the issuer as
           promised."""
        return self.__sinkable

    @sinkable.setter
    def sinkable(self, value: bool):
        self._property_changed('sinkable')
        self.__sinkable = value        

    @property
    def sink_factor(self) -> float:
        """The level to which a sinkable bond has currently sunk."""
        return self.__sink_factor

    @sink_factor.setter
    def sink_factor(self, value: float):
        self._property_changed('sink_factor')
        self.__sink_factor = value        

    @property
    def accrued_interest_standard(self) -> float:
        """The accrued interest paid on the bond if it is settled two business days after
           the trade date."""
        return self.__accrued_interest_standard

    @accrued_interest_standard.setter
    def accrued_interest_standard(self, value: float):
        self._property_changed('accrued_interest_standard')
        self.__accrued_interest_standard = value        

    @property
    def redemption_date(self) -> datetime.date:
        """The date on which a bond's face value is repaid to bondholders."""
        return self.__redemption_date

    @redemption_date.setter
    def redemption_date(self, value: datetime.date):
        self._property_changed('redemption_date')
        self.__redemption_date = value        

    @property
    def redemption_price(self) -> float:
        """The price for which the issuer will repurchase the security for at the
           redemption date."""
        return self.__redemption_price

    @redemption_price.setter
    def redemption_price(self, value: float):
        self._property_changed('redemption_price')
        self.__redemption_price = value        

    @property
    def private_placement_type(self) -> str:
        """Regulation that applies to a bond."""
        return self.__private_placement_type

    @private_placement_type.setter
    def private_placement_type(self, value: str):
        self._property_changed('private_placement_type')
        self.__private_placement_type = value        

    @property
    def minimum_piece(self) -> float:
        """The lowest denomination of an issue that can be purchased as authorized by the
           bond documents"""
        return self.__minimum_piece

    @minimum_piece.setter
    def minimum_piece(self, value: float):
        self._property_changed('minimum_piece')
        self.__minimum_piece = value        

    @property
    def minimum_increment(self) -> float:
        """The minimum increment size of the bond purchase allowed above the minimum
           denomination as authorized by the bond documents"""
        return self.__minimum_increment

    @minimum_increment.setter
    def minimum_increment(self, value: float):
        self._property_changed('minimum_increment')
        self.__minimum_increment = value        

    @property
    def minimum_denomination(self) -> float:
        """The lowest denomination of an issue that can be purchased as authorized by the
           bond documents"""
        return self.__minimum_denomination

    @minimum_denomination.setter
    def minimum_denomination(self, value: float):
        self._property_changed('minimum_denomination')
        self.__minimum_denomination = value        

    @property
    def default_backcast(self) -> bool:
        """Is basket backcasted using initial positions."""
        return self.__default_backcast

    @default_backcast.setter
    def default_backcast(self, value: bool):
        self._property_changed('default_backcast')
        self.__default_backcast = value        


class AssetStats(Base):
        
    """Performance statistics."""

    @camel_case_translate
    def __init__(
        self,
        last_updated_time: datetime.datetime = None,
        period: Union[AssetStatsPeriod, str] = None,
        type_: Union[AssetStatsType, str] = None,
        stats: PerformanceStats = None,
        start_date: datetime.date = None,
        end_date: datetime.date = None,
        name: str = None
    ):        
        super().__init__()
        self.last_updated_time = last_updated_time
        self.period = period
        self.__type = get_enum_value(AssetStatsType, type_)
        self.stats = stats
        self.start_date = start_date
        self.end_date = end_date
        self.name = name

    @property
    def last_updated_time(self) -> datetime.datetime:
        return self.__last_updated_time

    @last_updated_time.setter
    def last_updated_time(self, value: datetime.datetime):
        self._property_changed('last_updated_time')
        self.__last_updated_time = value        

    @property
    def period(self) -> Union[AssetStatsPeriod, str]:
        """The period used to produce date range."""
        return self.__period

    @period.setter
    def period(self, value: Union[AssetStatsPeriod, str]):
        self._property_changed('period')
        self.__period = get_enum_value(AssetStatsPeriod, value)        

    @property
    def type(self) -> Union[AssetStatsType, str]:
        """Is it rolling, none etc."""
        return self.__type

    @type.setter
    def type(self, value: Union[AssetStatsType, str]):
        self._property_changed('type')
        self.__type = get_enum_value(AssetStatsType, value)        

    @property
    def stats(self) -> PerformanceStats:
        """Performance statistics."""
        return self.__stats

    @stats.setter
    def stats(self, value: PerformanceStats):
        self._property_changed('stats')
        self.__stats = value        

    @property
    def start_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__start_date

    @start_date.setter
    def start_date(self, value: datetime.date):
        self._property_changed('start_date')
        self.__start_date = value        

    @property
    def end_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__end_date

    @end_date.setter
    def end_date(self, value: datetime.date):
        self._property_changed('end_date')
        self.__end_date = value        


class AssetStatsRequest(Base):
        
    """Performance statistics."""

    @camel_case_translate
    def __init__(
        self,
        last_updated_time: DateRange = None,
        period: Union[AssetStatsPeriod, str] = None,
        type_: Union[AssetStatsType, str] = None,
        stats: PerformanceStatsRequest = None,
        name: str = None
    ):        
        super().__init__()
        self.last_updated_time = last_updated_time
        self.period = period
        self.__type = get_enum_value(AssetStatsType, type_)
        self.stats = stats
        self.name = name

    @property
    def last_updated_time(self) -> DateRange:
        return self.__last_updated_time

    @last_updated_time.setter
    def last_updated_time(self, value: DateRange):
        self._property_changed('last_updated_time')
        self.__last_updated_time = value        

    @property
    def period(self) -> Union[AssetStatsPeriod, str]:
        """The period used to produce date range."""
        return self.__period

    @period.setter
    def period(self, value: Union[AssetStatsPeriod, str]):
        self._property_changed('period')
        self.__period = get_enum_value(AssetStatsPeriod, value)        

    @property
    def type(self) -> Union[AssetStatsType, str]:
        """Is it rolling, none etc."""
        return self.__type

    @type.setter
    def type(self, value: Union[AssetStatsType, str]):
        self._property_changed('type')
        self.__type = get_enum_value(AssetStatsType, value)        

    @property
    def stats(self) -> PerformanceStatsRequest:
        """Performance statistics."""
        return self.__stats

    @stats.setter
    def stats(self, value: PerformanceStatsRequest):
        self._property_changed('stats')
        self.__stats = value        


class CommodConfigParameters(Base):
        
    """Commodity configuration parameters"""

    @camel_case_translate
    def __init__(
        self,
        infra: str,
        field_history: Tuple[dict, ...],
        name: str = None
    ):        
        super().__init__()
        self.infra = infra
        self.field_history = field_history
        self.name = name

    @property
    def infra(self) -> str:
        return self.__infra

    @infra.setter
    def infra(self, value: str):
        self._property_changed('infra')
        self.__infra = value        

    @property
    def field_history(self) -> Tuple[dict, ...]:
        return self.__field_history

    @field_history.setter
    def field_history(self, value: Tuple[dict, ...]):
        self._property_changed('field_history')
        self.__field_history = value        


class HedgeFundParameters(Base):
        
    """Asset parameters specific to hedge funds"""

    @camel_case_translate
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
        net_exposure_classification: Union[NetExposureClassification, str] = None,
        last_returns_date: datetime.date = None,
        name: str = None
    ):        
        super().__init__()
        self.aum = aum
        self.strategy_aum = strategy_aum
        self.aum_range = aum_range
        self.strategy_aum_range = strategy_aum_range
        self.disclaimers = disclaimers
        self.market_cap_category = market_cap_category
        self.marketing_status = marketing_status
        self.preferences = preferences
        self.regional_focus = regional_focus
        self.risk_taking_model = risk_taking_model
        self.strategy = strategy
        self.supra_strategy = supra_strategy
        self.strategy_description = strategy_description
        self.targeted_gross_exposure = targeted_gross_exposure
        self.targeted_net_exposure = targeted_net_exposure
        self.targeted_num_of_positions_short = targeted_num_of_positions_short
        self.targeted_num_of_positions_long = targeted_num_of_positions_long
        self.turnover = turnover
        self.vehicle_type = vehicle_type
        self.net_exposure_classification = net_exposure_classification
        self.last_returns_date = last_returns_date
        self.name = name

    @property
    def aum(self) -> float:
        """Current assets under management. Only viewable after having been granted
           additional access to asset information."""
        return self.__aum

    @aum.setter
    def aum(self, value: float):
        self._property_changed('aum')
        self.__aum = value        

    @property
    def strategy_aum(self) -> float:
        """Total assets under management for this strategy (including comingled fund,
           managed accounts, and funds of one). Only viewable after having been
           granted additional access to asset information."""
        return self.__strategy_aum

    @strategy_aum.setter
    def strategy_aum(self, value: float):
        self._property_changed('strategy_aum')
        self.__strategy_aum = value        

    @property
    def aum_range(self) -> NumberRange:
        """Range in which assets under management fall. Same view permissions as the asset."""
        return self.__aum_range

    @aum_range.setter
    def aum_range(self, value: NumberRange):
        self._property_changed('aum_range')
        self.__aum_range = value        

    @property
    def strategy_aum_range(self) -> NumberRange:
        """Range in which assets under management for this strategy fall. Same view
           permissions as the asset."""
        return self.__strategy_aum_range

    @strategy_aum_range.setter
    def strategy_aum_range(self, value: NumberRange):
        self._property_changed('strategy_aum_range')
        self.__strategy_aum_range = value        

    @property
    def disclaimers(self) -> str:
        """Legal disclaimers for performance data. Same view permissions as the asset."""
        return self.__disclaimers

    @disclaimers.setter
    def disclaimers(self, value: str):
        self._property_changed('disclaimers')
        self.__disclaimers = value        

    @property
    def market_cap_category(self) -> Tuple[str, ...]:
        """Category of market capitalizations a fund is focused on from an investment
           perspective. Same view permissions as the asset."""
        return self.__market_cap_category

    @market_cap_category.setter
    def market_cap_category(self, value: Tuple[str, ...]):
        self._property_changed('market_cap_category')
        self.__market_cap_category = value        

    @property
    def marketing_status(self) -> str:
        """A fund's posture as to whether it is currently accepting new subscriptions. Same
           view permissions as the asset."""
        return self.__marketing_status

    @marketing_status.setter
    def marketing_status(self, value: str):
        self._property_changed('marketing_status')
        self.__marketing_status = value        

    @property
    def preferences(self) -> dict:
        """Lists of blacklisted company attributes."""
        return self.__preferences

    @preferences.setter
    def preferences(self, value: dict):
        self._property_changed('preferences')
        self.__preferences = value        

    @property
    def regional_focus(self) -> Tuple[str, ...]:
        """Section of the world a fund is focused on from an investment perspective. Same
           view permissions as the asset"""
        return self.__regional_focus

    @regional_focus.setter
    def regional_focus(self, value: Tuple[str, ...]):
        self._property_changed('regional_focus')
        self.__regional_focus = value        

    @property
    def risk_taking_model(self) -> str:
        """Number of risk takers a fund has. Same view permissions as the asset"""
        return self.__risk_taking_model

    @risk_taking_model.setter
    def risk_taking_model(self, value: str):
        self._property_changed('risk_taking_model')
        self.__risk_taking_model = value        

    @property
    def strategy(self) -> Union[Strategy, str]:
        """More specific descriptor of a fund's investment approach. Same view permissions
           as the asset"""
        return self.__strategy

    @strategy.setter
    def strategy(self, value: Union[Strategy, str]):
        self._property_changed('strategy')
        self.__strategy = get_enum_value(Strategy, value)        

    @property
    def supra_strategy(self) -> Union[SupraStrategy, str]:
        """Broad descriptor of a fund's investment approach. Same view permissions as the
           asset"""
        return self.__supra_strategy

    @supra_strategy.setter
    def supra_strategy(self, value: Union[SupraStrategy, str]):
        self._property_changed('supra_strategy')
        self.__supra_strategy = get_enum_value(SupraStrategy, value)        

    @property
    def strategy_description(self) -> str:
        """Statement explaining a fund's investment approach. Only viewable after having
           been granted additional access to asset information."""
        return self.__strategy_description

    @strategy_description.setter
    def strategy_description(self, value: str):
        self._property_changed('strategy_description')
        self.__strategy_description = value        

    @property
    def targeted_gross_exposure(self) -> NumberRange:
        """Value of a fund's long positions plus short positions, expressed in percentage
           terms. Only viewable after having been granted additional access to
           asset information."""
        return self.__targeted_gross_exposure

    @targeted_gross_exposure.setter
    def targeted_gross_exposure(self, value: NumberRange):
        self._property_changed('targeted_gross_exposure')
        self.__targeted_gross_exposure = value        

    @property
    def targeted_net_exposure(self) -> NumberRange:
        """Value of a fund's long positions minus short positions, expressed in percentage
           terms. Only viewable after having been granted additional access to
           asset information."""
        return self.__targeted_net_exposure

    @targeted_net_exposure.setter
    def targeted_net_exposure(self, value: NumberRange):
        self._property_changed('targeted_net_exposure')
        self.__targeted_net_exposure = value        

    @property
    def targeted_num_of_positions_short(self) -> NumberRange:
        """Range of positions the fund typically holds on the short side of its portfolio.
           Only viewable after having been granted additional access to asset
           information."""
        return self.__targeted_num_of_positions_short

    @targeted_num_of_positions_short.setter
    def targeted_num_of_positions_short(self, value: NumberRange):
        self._property_changed('targeted_num_of_positions_short')
        self.__targeted_num_of_positions_short = value        

    @property
    def targeted_num_of_positions_long(self) -> NumberRange:
        """Range of positions the fund typically holds on the long side of its portfolio.
           Only viewable after having been granted additional access to asset
           information."""
        return self.__targeted_num_of_positions_long

    @targeted_num_of_positions_long.setter
    def targeted_num_of_positions_long(self, value: NumberRange):
        self._property_changed('targeted_num_of_positions_long')
        self.__targeted_num_of_positions_long = value        

    @property
    def turnover(self) -> str:
        """Rate at which a fund replaces its investment holdings. Only viewable after
           having been granted additional access to asset information."""
        return self.__turnover

    @turnover.setter
    def turnover(self, value: str):
        self._property_changed('turnover')
        self.__turnover = value        

    @property
    def vehicle_type(self) -> str:
        """Type of investment vehicle. Only viewable after having been granted additional
           access to asset information."""
        return self.__vehicle_type

    @vehicle_type.setter
    def vehicle_type(self, value: str):
        self._property_changed('vehicle_type')
        self.__vehicle_type = value        

    @property
    def net_exposure_classification(self) -> Union[NetExposureClassification, str]:
        """Classification for net exposure of fund."""
        return self.__net_exposure_classification

    @net_exposure_classification.setter
    def net_exposure_classification(self, value: Union[NetExposureClassification, str]):
        self._property_changed('net_exposure_classification')
        self.__net_exposure_classification = get_enum_value(NetExposureClassification, value)        

    @property
    def last_returns_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__last_returns_date

    @last_returns_date.setter
    def last_returns_date(self, value: datetime.date):
        self._property_changed('last_returns_date')
        self.__last_returns_date = value        


class ShareClassParameters(Base):
        
    """Attributes specific to share class assets"""

    @camel_case_translate
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
        self.active_liquidity_fee = active_liquidity_fee
        self.additional_provisions = additional_provisions
        self.benchmark = benchmark
        self.class_fees = class_fees
        self.class_type = class_type
        self.early_redemption_fee = early_redemption_fee
        self.expense_ratio_gross = expense_ratio_gross
        self.expense_ratio_net = expense_ratio_net
        self.share_class_type = share_class_type
        self.gate = gate
        self.gate_type = gate_type
        self.hurdle = hurdle
        self.hurdle_type = hurdle_type
        self.investment_manager = investment_manager
        self.investment_type = investment_type
        self.institutional_share_class = institutional_share_class
        self.lockup = lockup
        self.lockup_type = lockup_type
        self.management_fee = management_fee
        self.minimum_subscription = minimum_subscription
        self.name = name
        self.number_of_shares = number_of_shares
        self.performance_fee = performance_fee
        self.redemption_notice_period = redemption_notice_period
        self.redemption_period = redemption_period
        self.share_class_currency = share_class_currency
        self.side_pocket = side_pocket
        self.status = status
        self.sub_category = sub_category
        self.term_type = term_type

    @property
    def active_liquidity_fee(self) -> float:
        """Denotes percent active liquidity fee associated with this fund"""
        return self.__active_liquidity_fee

    @active_liquidity_fee.setter
    def active_liquidity_fee(self, value: float):
        self._property_changed('active_liquidity_fee')
        self.__active_liquidity_fee = value        

    @property
    def additional_provisions(self) -> str:
        """Additional details that are relevant to the share class that not captured by the
           other fields"""
        return self.__additional_provisions

    @additional_provisions.setter
    def additional_provisions(self, value: str):
        self._property_changed('additional_provisions')
        self.__additional_provisions = value        

    @property
    def benchmark(self) -> Benchmark:
        """Reference rate that can based on an absolute value or absolute value + index"""
        return self.__benchmark

    @benchmark.setter
    def benchmark(self, value: Benchmark):
        self._property_changed('benchmark')
        self.__benchmark = value        

    @property
    def class_fees(self) -> float:
        """Annual cost of investing in specific shareclass, expressed in basis points"""
        return self.__class_fees

    @class_fees.setter
    def class_fees(self, value: float):
        self._property_changed('class_fees')
        self.__class_fees = value        

    @property
    def class_type(self) -> str:
        """For example: B, C, Offshore, Offshore - A, etc"""
        return self.__class_type

    @class_type.setter
    def class_type(self, value: str):
        self._property_changed('class_type')
        self.__class_type = value        

    @property
    def early_redemption_fee(self) -> float:
        """Fee an investor pays to redeem before the expiry of a soft lock-up"""
        return self.__early_redemption_fee

    @early_redemption_fee.setter
    def early_redemption_fee(self, value: float):
        self._property_changed('early_redemption_fee')
        self.__early_redemption_fee = value        

    @property
    def expense_ratio_gross(self) -> float:
        """Gross expense ratio of the shareclass"""
        return self.__expense_ratio_gross

    @expense_ratio_gross.setter
    def expense_ratio_gross(self, value: float):
        self._property_changed('expense_ratio_gross')
        self.__expense_ratio_gross = value        

    @property
    def expense_ratio_net(self) -> float:
        """Net expense ratio of the shareclass"""
        return self.__expense_ratio_net

    @expense_ratio_net.setter
    def expense_ratio_net(self, value: float):
        self._property_changed('expense_ratio_net')
        self.__expense_ratio_net = value        

    @property
    def share_class_type(self) -> str:
        """Must be Money Market, Equity, or Fixed Income"""
        return self.__share_class_type

    @share_class_type.setter
    def share_class_type(self, value: str):
        self._property_changed('share_class_type')
        self.__share_class_type = value        

    @property
    def gate(self) -> float:
        """Limit to the amount of capital that can be redeemed from a fund"""
        return self.__gate

    @gate.setter
    def gate(self, value: float):
        self._property_changed('gate')
        self.__gate = value        

    @property
    def gate_type(self) -> str:
        """Category that gate relates to"""
        return self.__gate_type

    @gate_type.setter
    def gate_type(self, value: str):
        self._property_changed('gate_type')
        self.__gate_type = value        

    @property
    def hurdle(self) -> float:
        """Minimum rate of return a fund must generate before it collects a performance fee"""
        return self.__hurdle

    @hurdle.setter
    def hurdle(self, value: float):
        self._property_changed('hurdle')
        self.__hurdle = value        

    @property
    def hurdle_type(self) -> str:
        """Determines if the hurdle is calculated on all profits above hurdle rate"""
        return self.__hurdle_type

    @hurdle_type.setter
    def hurdle_type(self, value: str):
        self._property_changed('hurdle_type')
        self.__hurdle_type = value        

    @property
    def investment_manager(self) -> str:
        """Goldman Sachs, Blackrock Liquidity"""
        return self.__investment_manager

    @investment_manager.setter
    def investment_manager(self, value: str):
        self._property_changed('investment_manager')
        self.__investment_manager = value        

    @property
    def investment_type(self) -> str:
        """Government, Prime Institutional"""
        return self.__investment_type

    @investment_type.setter
    def investment_type(self, value: str):
        self._property_changed('investment_type')
        self.__investment_type = value        

    @property
    def institutional_share_class(self) -> bool:
        """User to identify if this is the largest and cheapest share class"""
        return self.__institutional_share_class

    @institutional_share_class.setter
    def institutional_share_class(self, value: bool):
        self._property_changed('institutional_share_class')
        self.__institutional_share_class = value        

    @property
    def lockup(self) -> float:
        """Number of months an investor is not allowed to redeem investment"""
        return self.__lockup

    @lockup.setter
    def lockup(self, value: float):
        self._property_changed('lockup')
        self.__lockup = value        

    @property
    def lockup_type(self) -> str:
        """Classification of lockup"""
        return self.__lockup_type

    @lockup_type.setter
    def lockup_type(self, value: str):
        self._property_changed('lockup_type')
        self.__lockup_type = value        

    @property
    def management_fee(self) -> float:
        """Percent fee paid by investor to compensate manager for the cost of managing
           their assets"""
        return self.__management_fee

    @management_fee.setter
    def management_fee(self, value: float):
        self._property_changed('management_fee')
        self.__management_fee = value        

    @property
    def minimum_subscription(self) -> float:
        """Lowest level of investment a fund will accept"""
        return self.__minimum_subscription

    @minimum_subscription.setter
    def minimum_subscription(self, value: float):
        self._property_changed('minimum_subscription')
        self.__minimum_subscription = value        

    @property
    def name(self) -> str:
        """Identifier for particular share class"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def number_of_shares(self) -> float:
        """Number of shares in the share class"""
        return self.__number_of_shares

    @number_of_shares.setter
    def number_of_shares(self, value: float):
        self._property_changed('number_of_shares')
        self.__number_of_shares = value        

    @property
    def performance_fee(self) -> float:
        """Fee paid by investor to compensate manager for generating positive returns or
           alpha"""
        return self.__performance_fee

    @performance_fee.setter
    def performance_fee(self, value: float):
        self._property_changed('performance_fee')
        self.__performance_fee = value        

    @property
    def redemption_notice_period(self) -> float:
        """Number of days prior to a redemption that an investor must notify a manager of
           their intent"""
        return self.__redemption_notice_period

    @redemption_notice_period.setter
    def redemption_notice_period(self, value: float):
        self._property_changed('redemption_notice_period')
        self.__redemption_notice_period = value        

    @property
    def redemption_period(self) -> str:
        """Frequency on which an investor can redeem from a fund"""
        return self.__redemption_period

    @redemption_period.setter
    def redemption_period(self, value: str):
        self._property_changed('redemption_period')
        self.__redemption_period = value        

    @property
    def share_class_currency(self) -> str:
        """Currency of the share class"""
        return self.__share_class_currency

    @share_class_currency.setter
    def share_class_currency(self, value: str):
        self._property_changed('share_class_currency')
        self.__share_class_currency = value        

    @property
    def side_pocket(self) -> str:
        """Account utilized to separate illiquid assets from more liquid investments"""
        return self.__side_pocket

    @side_pocket.setter
    def side_pocket(self, value: str):
        self._property_changed('side_pocket')
        self.__side_pocket = value        

    @property
    def status(self) -> str:
        """Denotes whether the share class is currently accepting new subscriptions"""
        return self.__status

    @status.setter
    def status(self, value: str):
        self._property_changed('status')
        self.__status = value        

    @property
    def sub_category(self) -> str:
        """Subtype of what funds invest in within each SEC category"""
        return self.__sub_category

    @sub_category.setter
    def sub_category(self, value: str):
        self._property_changed('sub_category')
        self.__sub_category = value        

    @property
    def term_type(self) -> str:
        """category that describes share class offering"""
        return self.__term_type

    @term_type.setter
    def term_type(self, value: str):
        self._property_changed('term_type')
        self.__term_type = value        


class TemporalPeople(Base):
        
    """People associated with an asset during a certain date range"""

    @camel_case_translate
    def __init__(
        self,
        start_date: datetime.date = None,
        end_date: datetime.date = None,
        people: People = None,
        name: str = None
    ):        
        super().__init__()
        self.start_date = start_date
        self.end_date = end_date
        self.people = people
        self.name = name

    @property
    def start_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__start_date

    @start_date.setter
    def start_date(self, value: datetime.date):
        self._property_changed('start_date')
        self.__start_date = value        

    @property
    def end_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__end_date

    @end_date.setter
    def end_date(self, value: datetime.date):
        self._property_changed('end_date')
        self.__end_date = value        

    @property
    def people(self) -> People:
        """People associated with an asset"""
        return self.__people

    @people.setter
    def people(self, value: People):
        self._property_changed('people')
        self.__people = value        


class Asset(Base):
        
    """A security or instrument which can be held in a trading book (for example a
       stock or a bond) or a publically identifiable object with observable
       market data fixings which can be referenced in derivative transations
       (for example the SPX Index)"""

    @camel_case_translate
    def __init__(
        self,
        asset_class: Union[AssetClass, str],
        type_: Union[AssetType, str],
        name: str,
        created_by_id: str = None,
        created_time: datetime.datetime = None,
        currency: Union[Currency, str] = None,
        description: str = None,
        entitlements: Entitlements = None,
        entitlement_exclusions: EntitlementExclusions = None,
        exchange: str = None,
        id_: str = None,
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
        self.asset_class = asset_class
        self.created_by_id = created_by_id
        self.created_time = created_time
        self.currency = currency
        self.description = description
        self.entitlements = entitlements
        self.entitlement_exclusions = entitlement_exclusions
        self.exchange = exchange
        self.__id = id_
        self.identifiers = identifiers
        self.last_updated_by_id = last_updated_by_id
        self.last_updated_time = last_updated_time
        self.listed = listed
        self.live_date = live_date
        self.name = name
        self.owner_id = owner_id
        self.parameters = parameters
        self.asset_stats = asset_stats
        self.people = people
        self.region = region
        self.report_ids = report_ids
        self.short_name = short_name
        self.styles = styles
        self.tags = tags
        self.__type = get_enum_value(AssetType, type_)
        self.underlying_asset_ids = underlying_asset_ids

    @property
    def asset_class(self) -> Union[AssetClass, str]:
        """Asset classification of security. Assets are classified into broad groups which
           exhibit similar characteristics and behave in a consistent way under
           different market conditions"""
        return self.__asset_class

    @asset_class.setter
    def asset_class(self, value: Union[AssetClass, str]):
        self._property_changed('asset_class')
        self.__asset_class = get_enum_value(AssetClass, value)        

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
    def description(self) -> str:
        """Free text description of asset. Description provided will be indexed in the
           search service for free text relevance match"""
        return self.__description

    @description.setter
    def description(self, value: str):
        self._property_changed('description')
        self.__description = value        

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
    def exchange(self) -> str:
        """Name of marketplace where security, derivative or other instrument is traded"""
        return self.__exchange

    @exchange.setter
    def exchange(self, value: str):
        self._property_changed('exchange')
        self.__exchange = value        

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def identifiers(self) -> Tuple[Identifier, ...]:
        """Array of identifier objects which can be used to locate this item in searches
           and other services"""
        return self.__identifiers

    @identifiers.setter
    def identifiers(self, value: Tuple[Identifier, ...]):
        self._property_changed('identifiers')
        self.__identifiers = value        

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
    def listed(self) -> bool:
        """Whether the asset is currently listed or not"""
        return self.__listed

    @listed.setter
    def listed(self, value: bool):
        self._property_changed('listed')
        self.__listed = value        

    @property
    def live_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__live_date

    @live_date.setter
    def live_date(self, value: datetime.date):
        self._property_changed('live_date')
        self.__live_date = value        

    @property
    def name(self) -> str:
        """Display name of the asset"""
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
    def parameters(self) -> dict:
        return self.__parameters

    @parameters.setter
    def parameters(self, value: dict):
        self._property_changed('parameters')
        self.__parameters = value        

    @property
    def asset_stats(self) -> Tuple[AssetStats, ...]:
        """Performance statistics."""
        return self.__asset_stats

    @asset_stats.setter
    def asset_stats(self, value: Tuple[AssetStats, ...]):
        self._property_changed('asset_stats')
        self.__asset_stats = value        

    @property
    def people(self) -> People:
        """Key people associated with asset"""
        return self.__people

    @people.setter
    def people(self, value: People):
        self._property_changed('people')
        self.__people = value        

    @property
    def region(self) -> Union[Region, str]:
        """Regional classification for the asset"""
        return self.__region

    @region.setter
    def region(self, value: Union[Region, str]):
        self._property_changed('region')
        self.__region = get_enum_value(Region, value)        

    @property
    def report_ids(self) -> Tuple[str, ...]:
        """Array of report identifiers related to the object"""
        return self.__report_ids

    @report_ids.setter
    def report_ids(self, value: Tuple[str, ...]):
        self._property_changed('report_ids')
        self.__report_ids = value        

    @property
    def short_name(self) -> str:
        """Short name or alias for the asset"""
        return self.__short_name

    @short_name.setter
    def short_name(self, value: str):
        self._property_changed('short_name')
        self.__short_name = value        

    @property
    def styles(self) -> Tuple[str, ...]:
        """Styles or themes associated with the asset (max 50)"""
        return self.__styles

    @styles.setter
    def styles(self, value: Tuple[str, ...]):
        self._property_changed('styles')
        self.__styles = value        

    @property
    def tags(self) -> Tuple[str, ...]:
        """Metadata associated with the object. Provide an array of strings which will be
           indexed for search and locating related objects"""
        return self.__tags

    @tags.setter
    def tags(self, value: Tuple[str, ...]):
        self._property_changed('tags')
        self.__tags = value        

    @property
    def type(self) -> Union[AssetType, str]:
        """Asset type differentiates the product categorization or contract type"""
        return self.__type

    @type.setter
    def type(self, value: Union[AssetType, str]):
        self._property_changed('type')
        self.__type = get_enum_value(AssetType, value)        

    @property
    def underlying_asset_ids(self) -> Tuple[str, ...]:
        """Underlying asset ids"""
        return self.__underlying_asset_ids

    @underlying_asset_ids.setter
    def underlying_asset_ids(self, value: Tuple[str, ...]):
        self._property_changed('underlying_asset_ids')
        self.__underlying_asset_ids = value        


class EntityQuery(Base):
        
    @camel_case_translate
    def __init__(
        self,
        format_: Union[Format, str] = None,
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
        offset: int = None,
        name: str = None
    ):        
        super().__init__()
        self.__format = get_enum_value(Format, format_)
        self.where = where
        self.as_of_time = as_of_time
        self.last_updated_since = last_updated_since
        self.date = date
        self.time = time
        self.delay = delay
        self.order_by = order_by
        self.scroll = scroll
        self.scroll_id = scroll_id
        self.fields = fields
        self.limit = limit
        self.offset = offset
        self.name = name

    @property
    def format(self) -> Union[Format, str]:
        """Alternative format for data to be returned in"""
        return self.__format

    @format.setter
    def format(self, value: Union[Format, str]):
        self._property_changed('format')
        self.__format = get_enum_value(Format, value)        

    @property
    def where(self) -> FieldFilterMap:
        return self.__where

    @where.setter
    def where(self, value: FieldFilterMap):
        self._property_changed('where')
        self.__where = value        

    @property
    def as_of_time(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__as_of_time

    @as_of_time.setter
    def as_of_time(self, value: datetime.datetime):
        self._property_changed('as_of_time')
        self.__as_of_time = value        

    @property
    def last_updated_since(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__last_updated_since

    @last_updated_since.setter
    def last_updated_since(self, value: datetime.datetime):
        self._property_changed('last_updated_since')
        self.__last_updated_since = value        

    @property
    def date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__date

    @date.setter
    def date(self, value: datetime.date):
        self._property_changed('date')
        self.__date = value        

    @property
    def time(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__time

    @time.setter
    def time(self, value: datetime.datetime):
        self._property_changed('time')
        self.__time = value        

    @property
    def delay(self) -> int:
        """Number of minutes to delay returning data"""
        return self.__delay

    @delay.setter
    def delay(self, value: int):
        self._property_changed('delay')
        self.__delay = value        

    @property
    def order_by(self) -> Tuple[Union[dict, str], ...]:
        return self.__order_by

    @order_by.setter
    def order_by(self, value: Tuple[Union[dict, str], ...]):
        self._property_changed('order_by')
        self.__order_by = value        

    @property
    def scroll(self) -> str:
        """Time for which to keep the scroll search context alive, i.e. 1m (1 minute) or
           10s (10 seconds)"""
        return self.__scroll

    @scroll.setter
    def scroll(self, value: str):
        self._property_changed('scroll')
        self.__scroll = value        

    @property
    def scroll_id(self) -> str:
        """Scroll identifier to be used to retrieve the next batch of results"""
        return self.__scroll_id

    @scroll_id.setter
    def scroll_id(self, value: str):
        self._property_changed('scroll_id')
        self.__scroll_id = value        

    @property
    def fields(self) -> Tuple[Union[dict, str], ...]:
        return self.__fields

    @fields.setter
    def fields(self, value: Tuple[Union[dict, str], ...]):
        self._property_changed('fields')
        self.__fields = value        

    @property
    def limit(self) -> int:
        """Limit on the number of objects to be returned in the response. Can range between
           1 and 10000"""
        return self.__limit

    @limit.setter
    def limit(self, value: int):
        self._property_changed('limit')
        self.__limit = value        

    @property
    def offset(self) -> int:
        """The offset of the first result returned (default 0). Can be used in pagination
           to defined the first item in the list to be returned, for example if
           you request 100 objects, to query the next page you would specify
           offset = 100."""
        return self.__offset

    @offset.setter
    def offset(self, value: int):
        self._property_changed('offset')
        self.__offset = value        
