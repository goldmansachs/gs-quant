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
    Registered_Investment_Advisor = 'Registered Investment Advisor'
    Sovereign_Wealth_Fund = 'Sovereign Wealth Fund'    


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


class CommodityFamily(EnumBase, Enum):    
    
    """Commodity Family"""

    Base_Metal = 'Base Metal'
    Gas = 'Gas'
    Oil = 'Oil'
    Oil_Products = 'Oil Products'    


class CommoditySubFamily(EnumBase, Enum):    
    
    """Commodity SubFamily"""

    Crude = 'Crude'
    Fuel = 'Fuel'
    Heat = 'Heat'
    NG = 'NG'    


class AssetMetadata(Base):
        
    """Asset Meta Data that holds information related to the source of the asset rather
       than economics"""

    @camel_case_translate
    def __init__(
        self,
        version_timestamp: datetime.datetime = None,
        name: str = None
    ):        
        super().__init__()
        self.version_timestamp = version_timestamp
        self.name = name

    @property
    def version_timestamp(self) -> datetime.datetime:
        """Timestamp when object was milestoned in source database."""
        return self.__version_timestamp

    @version_timestamp.setter
    def version_timestamp(self, value: datetime.datetime):
        self._property_changed('version_timestamp')
        self.__version_timestamp = value        


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
        naics_classification_code: str = None,
        naics_industry_description: str = None,
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
        self.naics_classification_code = naics_classification_code
        self.naics_industry_description = naics_industry_description
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
    def naics_classification_code(self) -> str:
        """NAICS industry classification code."""
        return self.__naics_classification_code

    @naics_classification_code.setter
    def naics_classification_code(self, value: str):
        self._property_changed('naics_classification_code')
        self.__naics_classification_code = value        

    @property
    def naics_industry_description(self) -> str:
        """NAICS industry description."""
        return self.__naics_industry_description

    @naics_industry_description.setter
    def naics_industry_description(self, value: str):
        self._property_changed('naics_industry_description')
        self.__naics_industry_description = value        

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
        strategy_description: str = None,
        targeted_gross_exposure: NumberRange = None,
        targeted_net_exposure: NumberRange = None,
        targeted_num_of_positions_short: NumberRange = None,
        targeted_num_of_positions_long: NumberRange = None,
        turnover: str = None,
        vehicle_type: str = None,
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
        self.strategy_description = strategy_description
        self.targeted_gross_exposure = targeted_gross_exposure
        self.targeted_net_exposure = targeted_net_exposure
        self.targeted_num_of_positions_short = targeted_num_of_positions_short
        self.targeted_num_of_positions_long = targeted_num_of_positions_long
        self.turnover = turnover
        self.vehicle_type = vehicle_type
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
    def last_returns_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__last_returns_date

    @last_returns_date.setter
    def last_returns_date(self, value: datetime.date):
        self._property_changed('last_returns_date')
        self.__last_returns_date = value        


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
        active: bool = None,
        classifications: AssetClassifications = None,
        created_by_id: str = None,
        created_time: datetime.datetime = None,
        currency: Union[Currency, str] = None,
        default_quantity: float = None,
        description: str = None,
        economic_terms_hash: str = None,
        entitlements: Entitlements = None,
        entitlement_exclusions: EntitlementExclusions = None,
        exchange: str = None,
        id_: str = None,
        identifiers: Tuple[Identifier, ...] = None,
        last_updated_by_id: str = None,
        last_updated_time: datetime.datetime = None,
        listed: bool = None,
        live_date: datetime.date = None,
        key: str = None,
        key_map: dict = None,
        owner_id: str = None,
        parameters: dict = None,
        asset_stats: Tuple[AssetStats, ...] = None,
        people: People = None,
        people_history: Tuple[TemporalPeople, ...] = None,
        rank: float = None,
        region: Union[Region, str] = None,
        report_ids: Tuple[str, ...] = None,
        sectors: Tuple[str, ...] = None,
        short_name: str = None,
        styles: Tuple[str, ...] = None,
        tags: Tuple[str, ...] = None,
        underliers: Tuple[str, ...] = None,
        underlying_asset_ids: Tuple[str, ...] = None,
        xrefs: Tuple[TemporalXRef, ...] = None,
        xref: XRef = None,
        metadata: AssetMetadata = None
    ):        
        super().__init__()
        self.active = active
        self.asset_class = asset_class
        self.classifications = classifications
        self.created_by_id = created_by_id
        self.created_time = created_time
        self.currency = currency
        self.default_quantity = default_quantity
        self.description = description
        self.economic_terms_hash = economic_terms_hash
        self.entitlements = entitlements
        self.entitlement_exclusions = entitlement_exclusions
        self.exchange = exchange
        self.__id = id_
        self.identifiers = identifiers
        self.last_updated_by_id = last_updated_by_id
        self.last_updated_time = last_updated_time
        self.listed = listed
        self.live_date = live_date
        self.key = key
        self.key_map = key_map
        self.name = name
        self.owner_id = owner_id
        self.parameters = parameters
        self.asset_stats = asset_stats
        self.people = people
        self.people_history = people_history
        self.rank = rank
        self.region = region
        self.report_ids = report_ids
        self.sectors = sectors
        self.short_name = short_name
        self.styles = styles
        self.tags = tags
        self.__type = get_enum_value(AssetType, type_)
        self.underliers = underliers
        self.underlying_asset_ids = underlying_asset_ids
        self.xrefs = xrefs
        self.xref = xref
        self.metadata = metadata

    @property
    def active(self) -> bool:
        return self.__active

    @active.setter
    def active(self, value: bool):
        self._property_changed('active')
        self.__active = value        

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
    def classifications(self) -> AssetClassifications:
        return self.__classifications

    @classifications.setter
    def classifications(self, value: AssetClassifications):
        self._property_changed('classifications')
        self.__classifications = value        

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
    def default_quantity(self) -> float:
        return self.__default_quantity

    @default_quantity.setter
    def default_quantity(self, value: float):
        self._property_changed('default_quantity')
        self.__default_quantity = value        

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
    def economic_terms_hash(self) -> str:
        return self.__economic_terms_hash

    @economic_terms_hash.setter
    def economic_terms_hash(self, value: str):
        self._property_changed('economic_terms_hash')
        self.__economic_terms_hash = value        

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
    def key(self) -> str:
        return self.__key

    @key.setter
    def key(self, value: str):
        self._property_changed('key')
        self.__key = value        

    @property
    def key_map(self) -> dict:
        return self.__key_map

    @key_map.setter
    def key_map(self, value: dict):
        self._property_changed('key_map')
        self.__key_map = value        

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
    def people_history(self) -> Tuple[TemporalPeople, ...]:
        """Historical list of people"""
        return self.__people_history

    @people_history.setter
    def people_history(self, value: Tuple[TemporalPeople, ...]):
        self._property_changed('people_history')
        self.__people_history = value        

    @property
    def rank(self) -> float:
        return self.__rank

    @rank.setter
    def rank(self, value: float):
        self._property_changed('rank')
        self.__rank = value        

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
    def sectors(self) -> Tuple[str, ...]:
        """Sectors associated with the asset"""
        return self.__sectors

    @sectors.setter
    def sectors(self, value: Tuple[str, ...]):
        self._property_changed('sectors')
        self.__sectors = value        

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
    def underliers(self) -> Tuple[str, ...]:
        """Underlying asset ids (deprecated, use underlyingAssetIds)"""
        return self.__underliers

    @underliers.setter
    def underliers(self, value: Tuple[str, ...]):
        self._property_changed('underliers')
        self.__underliers = value        

    @property
    def underlying_asset_ids(self) -> Tuple[str, ...]:
        """Underlying asset ids"""
        return self.__underlying_asset_ids

    @underlying_asset_ids.setter
    def underlying_asset_ids(self, value: Tuple[str, ...]):
        self._property_changed('underlying_asset_ids')
        self.__underlying_asset_ids = value        

    @property
    def xrefs(self) -> Tuple[TemporalXRef, ...]:
        """xref history"""
        return self.__xrefs

    @xrefs.setter
    def xrefs(self, value: Tuple[TemporalXRef, ...]):
        self._property_changed('xrefs')
        self.__xrefs = value        

    @property
    def xref(self) -> XRef:
        return self.__xref

    @xref.setter
    def xref(self, value: XRef):
        self._property_changed('xref')
        self.__xref = value        

    @property
    def metadata(self) -> AssetMetadata:
        """Asset Meta Data that holds information related to the source of the asset rather
           than economics"""
        return self.__metadata

    @metadata.setter
    def metadata(self, value: AssetMetadata):
        self._property_changed('metadata')
        self.__metadata = value        


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
