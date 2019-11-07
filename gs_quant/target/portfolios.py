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
from gs_quant.base import Base, EnumBase, camel_case_translate, get_enum_value


class LiquidityMeasure(EnumBase, Enum):    
    
    """A list of the different liquidity measures to choose from."""

    Summary = 'Summary'
    Constituent_Transaction_Costs = 'Constituent Transaction Costs'
    Constituents = 'Constituents'
    Largest_Holdings_By_Weight = 'Largest Holdings By Weight'
    Least_Liquid_Holdings = 'Least Liquid Holdings'
    ADV_Percent_Buckets = 'ADV Percent Buckets'
    Market_Cap_Buckets = 'Market Cap Buckets'
    Region_Buckets = 'Region Buckets'
    Country_Buckets = 'Country Buckets'
    Sector_Buckets = 'Sector Buckets'
    Industry_Buckets = 'Industry Buckets'
    Risk_Buckets = 'Risk Buckets'
    Factor_Risk_Buckets = 'Factor Risk Buckets'
    Exposure_Buckets = 'Exposure Buckets'
    Factor_Exposure_Buckets = 'Factor Exposure Buckets'
    Percent_Of_Trade_Complete_Over_Time = 'Percent Of Trade Complete Over Time'
    Execution_Cost_With_Different_Time_Horizons = 'Execution Cost With Different Time Horizons'
    Participation_Rate_With_Different_Time_Horizons = 'Participation Rate With Different Time Horizons'
    Risk_With_Different_Time_Horizons = 'Risk With Different Time Horizons'
    Historical_ADV_Percent_Curve = 'Historical ADV Percent Curve'
    Time_Series_Data = 'Time Series Data'
    
    def __repr__(self):
        return self.value


class PortfolioType(EnumBase, Enum):    
    
    """Portfolio type differentiates the portfolio categorization"""

    Securities_Lending = 'Securities Lending'
    Draft_Portfolio = 'Draft Portfolio'
    
    def __repr__(self):
        return self.value


class LiquidityReportParameters(Base):
        
    """Parameters to be used on liquidity reports"""
       
    @camel_case_translate
    def __init__(
        self,
        title: str = None,
        email: str = None,
        trading_desk: str = None,
        name: str = None
    ):        
        super().__init__()
        self.title = title
        self.email = email
        self.trading_desk = trading_desk
        self.name = name

    @property
    def title(self) -> str:
        """Report title"""
        return self.__title

    @title.setter
    def title(self, value: str):
        self._property_changed('title')
        self.__title = value        

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, value: str):
        self._property_changed('email')
        self.__email = value        

    @property
    def trading_desk(self) -> str:
        return self.__trading_desk

    @trading_desk.setter
    def trading_desk(self, value: str):
        self._property_changed('trading_desk')
        self.__trading_desk = value        


class WeightedPosition(Base):
               
    @camel_case_translate
    def __init__(
        self,
        asset_id: str,
        weight: float,
        name: str = None
    ):        
        super().__init__()
        self.asset_id = asset_id
        self.weight = weight
        self.name = name

    @property
    def asset_id(self) -> str:
        """Marquee unique identifier"""
        return self.__asset_id

    @asset_id.setter
    def asset_id(self, value: str):
        self._property_changed('asset_id')
        self.__asset_id = value        

    @property
    def weight(self) -> float:
        """Relative net weight of the given position"""
        return self.__weight

    @weight.setter
    def weight(self, value: float):
        self._property_changed('weight')
        self.__weight = value        


class LiquidityRequest(Base):
        
    """Required parameters in order to get liquidity information on a set of positions"""
       
    @camel_case_translate
    def __init__(
        self,
        notional: float = None,
        positions: dict = None,
        risk_model: str = None,
        date: datetime.date = None,
        currency: Union[Currency, str] = None,
        participation_rate: float = None,
        execution_horizon: float = None,
        execution_start_time: datetime.datetime = None,
        execution_end_time: datetime.datetime = None,
        benchmark_id: str = None,
        measures: Tuple[Union[LiquidityMeasure, str], ...] = None,
        time_series_benchmark_ids: Tuple[str, ...] = None,
        time_series_start_date: datetime.date = None,
        time_series_end_date: datetime.date = None,
        format_: Union[Format, str] = None,
        report_parameters: LiquidityReportParameters = None,
        name: str = None
    ):        
        super().__init__()
        self.notional = notional
        self.positions = positions
        self.risk_model = risk_model
        self.date = date
        self.currency = currency
        self.participation_rate = participation_rate
        self.execution_horizon = execution_horizon
        self.execution_start_time = execution_start_time
        self.execution_end_time = execution_end_time
        self.benchmark_id = benchmark_id
        self.measures = measures
        self.time_series_benchmark_ids = time_series_benchmark_ids
        self.time_series_start_date = time_series_start_date
        self.time_series_end_date = time_series_end_date
        self.__format = get_enum_value(Format, format_)
        self.report_parameters = report_parameters
        self.name = name

    @property
    def notional(self) -> float:
        """Notional value of the positions."""
        return self.__notional

    @notional.setter
    def notional(self, value: float):
        self._property_changed('notional')
        self.__notional = value        

    @property
    def positions(self) -> dict:
        """A set of quantity or weighted positions."""
        return self.__positions

    @positions.setter
    def positions(self, value: dict):
        self._property_changed('positions')
        self.__positions = value        

    @property
    def risk_model(self) -> str:
        """Marquee unique risk model identifier"""
        return self.__risk_model

    @risk_model.setter
    def risk_model(self, value: str):
        self._property_changed('risk_model')
        self.__risk_model = value        

    @property
    def date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__date

    @date.setter
    def date(self, value: datetime.date):
        self._property_changed('date')
        self.__date = value        

    @property
    def currency(self) -> Union[Currency, str]:
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self._property_changed('currency')
        self.__currency = get_enum_value(Currency, value)        

    @property
    def participation_rate(self) -> float:
        return self.__participation_rate

    @participation_rate.setter
    def participation_rate(self, value: float):
        self._property_changed('participation_rate')
        self.__participation_rate = value        

    @property
    def execution_horizon(self) -> float:
        return self.__execution_horizon

    @execution_horizon.setter
    def execution_horizon(self, value: float):
        self._property_changed('execution_horizon')
        self.__execution_horizon = value        

    @property
    def execution_start_time(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__execution_start_time

    @execution_start_time.setter
    def execution_start_time(self, value: datetime.datetime):
        self._property_changed('execution_start_time')
        self.__execution_start_time = value        

    @property
    def execution_end_time(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__execution_end_time

    @execution_end_time.setter
    def execution_end_time(self, value: datetime.datetime):
        self._property_changed('execution_end_time')
        self.__execution_end_time = value        

    @property
    def benchmark_id(self) -> str:
        """Marquee unique asset identifier of the benchmark."""
        return self.__benchmark_id

    @benchmark_id.setter
    def benchmark_id(self, value: str):
        self._property_changed('benchmark_id')
        self.__benchmark_id = value        

    @property
    def measures(self) -> Tuple[Union[LiquidityMeasure, str], ...]:
        return self.__measures

    @measures.setter
    def measures(self, value: Tuple[Union[LiquidityMeasure, str], ...]):
        self._property_changed('measures')
        self.__measures = value        

    @property
    def time_series_benchmark_ids(self) -> Tuple[str, ...]:
        """Marquee unique identifiers of assets to be used as benchmarks."""
        return self.__time_series_benchmark_ids

    @time_series_benchmark_ids.setter
    def time_series_benchmark_ids(self, value: Tuple[str, ...]):
        self._property_changed('time_series_benchmark_ids')
        self.__time_series_benchmark_ids = value        

    @property
    def time_series_start_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__time_series_start_date

    @time_series_start_date.setter
    def time_series_start_date(self, value: datetime.date):
        self._property_changed('time_series_start_date')
        self.__time_series_start_date = value        

    @property
    def time_series_end_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__time_series_end_date

    @time_series_end_date.setter
    def time_series_end_date(self, value: datetime.date):
        self._property_changed('time_series_end_date')
        self.__time_series_end_date = value        

    @property
    def format(self) -> Union[Format, str]:
        """Alternative format for data to be returned in"""
        return self.__format

    @format.setter
    def format(self, value: Union[Format, str]):
        self._property_changed('format')
        self.__format = get_enum_value(Format, value)        

    @property
    def report_parameters(self) -> LiquidityReportParameters:
        """Parameters to be used on liquidity reports"""
        return self.__report_parameters

    @report_parameters.setter
    def report_parameters(self, value: LiquidityReportParameters):
        self._property_changed('report_parameters')
        self.__report_parameters = value        


class Portfolio(Base):
               
    @camel_case_translate
    def __init__(
        self,
        currency: Union[Currency, str],
        name: str,
        created_by_id: str = None,
        created_time: datetime.datetime = None,
        description: str = None,
        entitlements: Entitlements = None,
        entitlement_exclusions: EntitlementExclusions = None,
        id_: str = None,
        identifiers: Tuple[Identifier, ...] = None,
        last_updated_by_id: str = None,
        last_updated_time: datetime.datetime = None,
        owner_id: str = None,
        report_ids: Tuple[str, ...] = None,
        short_name: str = None,
        underlying_portfolio_ids: Tuple[str, ...] = None,
        tags: Tuple[str, ...] = None,
        type_: Union[PortfolioType, str] = None,
        parameters: LiquidityRequest = None
    ):        
        super().__init__()
        self.created_by_id = created_by_id
        self.created_time = created_time
        self.currency = currency
        self.description = description
        self.entitlements = entitlements
        self.entitlement_exclusions = entitlement_exclusions
        self.__id = id_
        self.identifiers = identifiers
        self.last_updated_by_id = last_updated_by_id
        self.last_updated_time = last_updated_time
        self.name = name
        self.owner_id = owner_id
        self.report_ids = report_ids
        self.short_name = short_name
        self.underlying_portfolio_ids = underlying_portfolio_ids
        self.tags = tags
        self.__type = get_enum_value(PortfolioType, type_)
        self.parameters = parameters

    @property
    def created_by_id(self) -> str:
        """Unique identifier of user who created the object"""
        return self.__created_by_id

    @created_by_id.setter
    def created_by_id(self, value: str):
        self._property_changed('created_by_id')
        self.__created_by_id = value        

    @property
    def created_time(self) -> datetime.datetime:
        """Time created. ISO 8601 formatted string"""
        return self.__created_time

    @created_time.setter
    def created_time(self, value: datetime.datetime):
        self._property_changed('created_time')
        self.__created_time = value        

    @property
    def currency(self) -> Union[Currency, str]:
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self._property_changed('currency')
        self.__currency = get_enum_value(Currency, value)        

    @property
    def description(self) -> str:
        """Free text description of portfolio. Description provided will be indexed in the
           search service for free text relevance match"""
        return self.__description

    @description.setter
    def description(self, value: str):
        self._property_changed('description')
        self.__description = value        

    @property
    def entitlements(self) -> Entitlements:
        """Defines the entitlements of a given resource"""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self._property_changed('entitlements')
        self.__entitlements = value        

    @property
    def entitlement_exclusions(self) -> EntitlementExclusions:
        """Defines the exclusion entitlements of a given resource"""
        return self.__entitlement_exclusions

    @entitlement_exclusions.setter
    def entitlement_exclusions(self, value: EntitlementExclusions):
        self._property_changed('entitlement_exclusions')
        self.__entitlement_exclusions = value        

    @property
    def id(self) -> str:
        """Marquee unique portfolio identifier"""
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
        """Unique identifier of user who last updated the object"""
        return self.__last_updated_by_id

    @last_updated_by_id.setter
    def last_updated_by_id(self, value: str):
        self._property_changed('last_updated_by_id')
        self.__last_updated_by_id = value        

    @property
    def last_updated_time(self) -> datetime.datetime:
        """Timestamp of when the object was last updated"""
        return self.__last_updated_time

    @last_updated_time.setter
    def last_updated_time(self, value: datetime.datetime):
        self._property_changed('last_updated_time')
        self.__last_updated_time = value        

    @property
    def name(self) -> str:
        """Display name of the portfolio"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def owner_id(self) -> str:
        """Marquee unique identifier for user who owns the object."""
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
    def short_name(self) -> str:
        """Short name or alias for the portfolio"""
        return self.__short_name

    @short_name.setter
    def short_name(self, value: str):
        self._property_changed('short_name')
        self.__short_name = value        

    @property
    def underlying_portfolio_ids(self) -> Tuple[str, ...]:
        """Underlying portfolio Ids"""
        return self.__underlying_portfolio_ids

    @underlying_portfolio_ids.setter
    def underlying_portfolio_ids(self, value: Tuple[str, ...]):
        self._property_changed('underlying_portfolio_ids')
        self.__underlying_portfolio_ids = value        

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
    def type(self) -> Union[PortfolioType, str]:
        """Portfolio type differentiates the portfolio categorization"""
        return self.__type

    @type.setter
    def type(self, value: Union[PortfolioType, str]):
        self._property_changed('type')
        self.__type = get_enum_value(PortfolioType, value)        

    @property
    def parameters(self) -> LiquidityRequest:
        return self.__parameters

    @parameters.setter
    def parameters(self, value: LiquidityRequest):
        self._property_changed('parameters')
        self.__parameters = value        
