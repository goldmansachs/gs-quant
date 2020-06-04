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


class BasketAction(EnumBase, Enum):    
    
    """Indicates what was the action taken on basket - create/edit/rebalance"""

    Create = 'Create'
    Edit = 'Edit'
    Rebalance = 'Rebalance'
    
    def __repr__(self):
        return self.value


class PositionSourceType(EnumBase, Enum):    
    
    """Source object for position data"""

    Portfolio = 'Portfolio'
    Asset = 'Asset'
    Backtest = 'Backtest'
    RiskRequest = 'RiskRequest'
    Hedge = 'Hedge'
    
    def __repr__(self):
        return self.value


class ReportMeasures(EnumBase, Enum):    
    
    """Enums for measures to be outputted for the report"""

    _ = ''
    pnl = 'pnl'
    longExposure = 'longExposure'
    shortExposure = 'shortExposure'
    assetCount = 'assetCount'
    turnover = 'turnover'
    assetCountLong = 'assetCountLong'
    assetCountShort = 'assetCountShort'
    netExposure = 'netExposure'
    grossExposure = 'grossExposure'
    tradingPnl = 'tradingPnl'
    tradingCostPnl = 'tradingCostPnl'
    servicingCostLongPnl = 'servicingCostLongPnl'
    servicingCostShortPnl = 'servicingCostShortPnl'
    exposure = 'exposure'
    sensitivity = 'sensitivity'
    mctr = 'mctr'
    price = 'price'
    basePrice = 'basePrice'
    
    def __repr__(self):
        return self.value


class ReportStatus(EnumBase, Enum):    
    
    """Status of report run"""

    new = 'new'
    ready = 'ready'
    executing = 'executing'
    calculating = 'calculating'
    done = 'done'
    error = 'error'
    cancelled = 'cancelled'
    waiting = 'waiting'
    
    def __repr__(self):
        return self.value


class ReportType(EnumBase, Enum):    
    
    """Type of report to execute"""

    Portfolio_Performance_Analytics = 'Portfolio Performance Analytics'
    Portfolio_Factor_Risk = 'Portfolio Factor Risk'
    Portfolio_Aging = 'Portfolio Aging'
    Asset_Factor_Risk = 'Asset Factor Risk'
    Basket_Create = 'Basket Create'
    Basket_Backcast = 'Basket Backcast'
    Scenario = 'Scenario'
    Iselect_Backtest = 'Iselect Backtest'
    Backtest_Run = 'Backtest Run'
    Analytics = 'Analytics'
    Risk_Calculation = 'Risk Calculation'
    
    def __repr__(self):
        return self.value


class ScenarioType(EnumBase, Enum):    
    
    """Type of Scenario"""

    Spot_Vol = 'Spot Vol'
    Greeks = 'Greeks'
    
    def __repr__(self):
        return self.value


class ReportParameters(Base):
        
    """Parameters specific to the report type"""

    @camel_case_translate
    def __init__(
        self,
        asset_class: Union[AssetClass, str] = None,
        transaction_cost_model: str = None,
        trading_cost: float = None,
        servicing_cost_long: float = None,
        servicing_cost_short: float = None,
        region: str = None,
        risk_model: str = None,
        fx_hedged: bool = None,
        publish_to_bloomberg: bool = None,
        publish_to_reuters: bool = None,
        include_price_history: bool = None,
        index_update: bool = None,
        index_rebalance: bool = None,
        basket_action: Union[BasketAction, str] = None,
        api_domain: bool = None,
        initial_price: float = None,
        stock_level_exposures: bool = None,
        explode_positions: bool = None,
        scenario_id: str = None,
        scenario_ids: Tuple[str, ...] = None,
        scenario_group_id: str = None,
        scenario_type: Union[ScenarioType, str] = None,
        market_model_id: str = None,
        risk_measures: Tuple[RiskMeasure, ...] = None,
        initial_pricing_date: datetime.date = None,
        backcast: bool = None,
        risk_request: RiskRequest = None,
        participation_rate: float = None,
        approve_rebalance: bool = None,
        use_risk_request_batch_mode: bool = False,
        limited_access_assets: Tuple[str, ...] = None,
        corporate_action_restricted_assets: Tuple[str, ...] = None,
        backcast_dates: Tuple[datetime.date, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.asset_class = asset_class
        self.transaction_cost_model = transaction_cost_model
        self.trading_cost = trading_cost
        self.servicing_cost_long = servicing_cost_long
        self.servicing_cost_short = servicing_cost_short
        self.region = region
        self.risk_model = risk_model
        self.fx_hedged = fx_hedged
        self.publish_to_bloomberg = publish_to_bloomberg
        self.publish_to_reuters = publish_to_reuters
        self.include_price_history = include_price_history
        self.index_update = index_update
        self.index_rebalance = index_rebalance
        self.basket_action = basket_action
        self.api_domain = api_domain
        self.initial_price = initial_price
        self.stock_level_exposures = stock_level_exposures
        self.explode_positions = explode_positions
        self.scenario_id = scenario_id
        self.scenario_ids = scenario_ids
        self.scenario_group_id = scenario_group_id
        self.scenario_type = scenario_type
        self.market_model_id = market_model_id
        self.risk_measures = risk_measures
        self.initial_pricing_date = initial_pricing_date
        self.backcast = backcast
        self.risk_request = risk_request
        self.participation_rate = participation_rate
        self.approve_rebalance = approve_rebalance
        self.use_risk_request_batch_mode = use_risk_request_batch_mode
        self.limited_access_assets = limited_access_assets
        self.corporate_action_restricted_assets = corporate_action_restricted_assets
        self.backcast_dates = backcast_dates
        self.name = name

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
    def transaction_cost_model(self) -> str:
        """Determines which model to use"""
        return self.__transaction_cost_model

    @transaction_cost_model.setter
    def transaction_cost_model(self, value: str):
        self._property_changed('transaction_cost_model')
        self.__transaction_cost_model = value        

    @property
    def trading_cost(self) -> float:
        """bps cost to execute delta"""
        return self.__trading_cost

    @trading_cost.setter
    def trading_cost(self, value: float):
        self._property_changed('trading_cost')
        self.__trading_cost = value        

    @property
    def servicing_cost_long(self) -> float:
        """bps cost to fund long positions"""
        return self.__servicing_cost_long

    @servicing_cost_long.setter
    def servicing_cost_long(self, value: float):
        self._property_changed('servicing_cost_long')
        self.__servicing_cost_long = value        

    @property
    def servicing_cost_short(self) -> float:
        """bps cost to fund short positions"""
        return self.__servicing_cost_short

    @servicing_cost_short.setter
    def servicing_cost_short(self, value: float):
        self._property_changed('servicing_cost_short')
        self.__servicing_cost_short = value        

    @property
    def region(self) -> str:
        """The region of the report"""
        return self.__region

    @region.setter
    def region(self, value: str):
        self._property_changed('region')
        self.__region = value        

    @property
    def risk_model(self) -> str:
        """Marquee unique risk model identifier"""
        return self.__risk_model

    @risk_model.setter
    def risk_model(self, value: str):
        self._property_changed('risk_model')
        self.__risk_model = value        

    @property
    def fx_hedged(self) -> bool:
        """Assume portfolio is FX Hedged"""
        return self.__fx_hedged

    @fx_hedged.setter
    def fx_hedged(self, value: bool):
        self._property_changed('fx_hedged')
        self.__fx_hedged = value        

    @property
    def publish_to_bloomberg(self) -> bool:
        """Publish Basket to Bloomberg"""
        return self.__publish_to_bloomberg

    @publish_to_bloomberg.setter
    def publish_to_bloomberg(self, value: bool):
        self._property_changed('publish_to_bloomberg')
        self.__publish_to_bloomberg = value        

    @property
    def publish_to_reuters(self) -> bool:
        """Publish Basket to Reuters"""
        return self.__publish_to_reuters

    @publish_to_reuters.setter
    def publish_to_reuters(self, value: bool):
        self._property_changed('publish_to_reuters')
        self.__publish_to_reuters = value        

    @property
    def include_price_history(self) -> bool:
        """Include full price history"""
        return self.__include_price_history

    @include_price_history.setter
    def include_price_history(self, value: bool):
        self._property_changed('include_price_history')
        self.__include_price_history = value        

    @property
    def index_update(self) -> bool:
        """Update the basket"""
        return self.__index_update

    @index_update.setter
    def index_update(self, value: bool):
        self._property_changed('index_update')
        self.__index_update = value        

    @property
    def index_rebalance(self) -> bool:
        """Rebalance the basket"""
        return self.__index_rebalance

    @index_rebalance.setter
    def index_rebalance(self, value: bool):
        self._property_changed('index_rebalance')
        self.__index_rebalance = value        

    @property
    def basket_action(self) -> Union[BasketAction, str]:
        """Indicates which basket action triggered the report"""
        return self.__basket_action

    @basket_action.setter
    def basket_action(self, value: Union[BasketAction, str]):
        self._property_changed('basket_action')
        self.__basket_action = get_enum_value(BasketAction, value)        

    @property
    def api_domain(self) -> bool:
        """Indicates if report is triggered from ui/api call"""
        return self.__api_domain

    @api_domain.setter
    def api_domain(self, value: bool):
        self._property_changed('api_domain')
        self.__api_domain = value        

    @property
    def initial_price(self) -> float:
        """Initial price for the position set"""
        return self.__initial_price

    @initial_price.setter
    def initial_price(self, value: float):
        self._property_changed('initial_price')
        self.__initial_price = value        

    @property
    def stock_level_exposures(self) -> bool:
        """Publish stock level exposures"""
        return self.__stock_level_exposures

    @stock_level_exposures.setter
    def stock_level_exposures(self, value: bool):
        self._property_changed('stock_level_exposures')
        self.__stock_level_exposures = value        

    @property
    def explode_positions(self) -> bool:
        """Whether to explode positions during risk run"""
        return self.__explode_positions

    @explode_positions.setter
    def explode_positions(self, value: bool):
        self._property_changed('explode_positions')
        self.__explode_positions = value        

    @property
    def scenario_id(self) -> str:
        """Marquee unique scenario identifier"""
        return self.__scenario_id

    @scenario_id.setter
    def scenario_id(self, value: str):
        self._property_changed('scenario_id')
        self.__scenario_id = value        

    @property
    def scenario_ids(self) -> Tuple[str, ...]:
        """Array of scenario identifiers related to the object"""
        return self.__scenario_ids

    @scenario_ids.setter
    def scenario_ids(self, value: Tuple[str, ...]):
        self._property_changed('scenario_ids')
        self.__scenario_ids = value        

    @property
    def scenario_group_id(self) -> str:
        """Marquee unique scenario group identifier"""
        return self.__scenario_group_id

    @scenario_group_id.setter
    def scenario_group_id(self, value: str):
        self._property_changed('scenario_group_id')
        self.__scenario_group_id = value        

    @property
    def scenario_type(self) -> Union[ScenarioType, str]:
        """Type of Scenario"""
        return self.__scenario_type

    @scenario_type.setter
    def scenario_type(self, value: Union[ScenarioType, str]):
        self._property_changed('scenario_type')
        self.__scenario_type = get_enum_value(ScenarioType, value)        

    @property
    def market_model_id(self) -> str:
        """Marquee unique market model identifier"""
        return self.__market_model_id

    @market_model_id.setter
    def market_model_id(self, value: str):
        self._property_changed('market_model_id')
        self.__market_model_id = value        

    @property
    def risk_measures(self) -> Tuple[RiskMeasure, ...]:
        """An array of risk measures to get from the risk calculation."""
        return self.__risk_measures

    @risk_measures.setter
    def risk_measures(self, value: Tuple[RiskMeasure, ...]):
        self._property_changed('risk_measures')
        self.__risk_measures = value        

    @property
    def initial_pricing_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__initial_pricing_date

    @initial_pricing_date.setter
    def initial_pricing_date(self, value: datetime.date):
        self._property_changed('initial_pricing_date')
        self.__initial_pricing_date = value        

    @property
    def backcast(self) -> bool:
        """Use backcasted portfolio derived from positions on the end date."""
        return self.__backcast

    @backcast.setter
    def backcast(self, value: bool):
        self._property_changed('backcast')
        self.__backcast = value        

    @property
    def risk_request(self) -> RiskRequest:
        """A request for a risk calculation"""
        return self.__risk_request

    @risk_request.setter
    def risk_request(self, value: RiskRequest):
        self._property_changed('risk_request')
        self.__risk_request = value        

    @property
    def participation_rate(self) -> float:
        """Liquidity analytics participation rate."""
        return self.__participation_rate

    @participation_rate.setter
    def participation_rate(self, value: float):
        self._property_changed('participation_rate')
        self.__participation_rate = value        

    @property
    def approve_rebalance(self) -> bool:
        """An approved basket"""
        return self.__approve_rebalance

    @approve_rebalance.setter
    def approve_rebalance(self, value: bool):
        self._property_changed('approve_rebalance')
        self.__approve_rebalance = value        

    @property
    def use_risk_request_batch_mode(self) -> bool:
        """Switch to enable RiskRequest batching"""
        return self.__use_risk_request_batch_mode

    @use_risk_request_batch_mode.setter
    def use_risk_request_batch_mode(self, value: bool):
        self._property_changed('use_risk_request_batch_mode')
        self.__use_risk_request_batch_mode = value        

    @property
    def limited_access_assets(self) -> Tuple[str, ...]:
        """List of constituents in the basket that GS has limited access to"""
        return self.__limited_access_assets

    @limited_access_assets.setter
    def limited_access_assets(self, value: Tuple[str, ...]):
        self._property_changed('limited_access_assets')
        self.__limited_access_assets = value        

    @property
    def corporate_action_restricted_assets(self) -> Tuple[str, ...]:
        """List of constituents in the basket that will not be adjusted for corporate
           actions in the future"""
        return self.__corporate_action_restricted_assets

    @corporate_action_restricted_assets.setter
    def corporate_action_restricted_assets(self, value: Tuple[str, ...]):
        self._property_changed('corporate_action_restricted_assets')
        self.__corporate_action_restricted_assets = value        

    @property
    def backcast_dates(self) -> Tuple[datetime.date, ...]:
        """List of dates user upload to backcast basket"""
        return self.__backcast_dates

    @backcast_dates.setter
    def backcast_dates(self, value: Tuple[datetime.date, ...]):
        self._property_changed('backcast_dates')
        self.__backcast_dates = value        


class Report(Base):
        
    @camel_case_translate
    def __init__(
        self,
        position_source_id: str,
        position_source_type: Union[PositionSourceType, str],
        type_: Union[ReportType, str],
        parameters: ReportParameters,
        calculation_time: float = None,
        data_set_id: str = None,
        asset_id: str = None,
        created_by_id: str = None,
        created_time: datetime.datetime = None,
        entitlements: Entitlements = None,
        entitlement_exclusions: EntitlementExclusions = None,
        id_: str = None,
        last_updated_by_id: str = None,
        last_updated_time: datetime.datetime = None,
        measures: Tuple[Union[ReportMeasures, str], ...] = None,
        name: str = None,
        owner_id: str = None,
        status: Union[ReportStatus, str] = None,
        latest_execution_time: datetime.datetime = None,
        latest_end_date: datetime.date = None,
        percentage_complete: float = None
    ):        
        super().__init__()
        self.calculation_time = calculation_time
        self.data_set_id = data_set_id
        self.asset_id = asset_id
        self.created_by_id = created_by_id
        self.created_time = created_time
        self.entitlements = entitlements
        self.entitlement_exclusions = entitlement_exclusions
        self.__id = id_
        self.last_updated_by_id = last_updated_by_id
        self.last_updated_time = last_updated_time
        self.measures = measures
        self.name = name
        self.owner_id = owner_id
        self.parameters = parameters
        self.position_source_id = position_source_id
        self.position_source_type = position_source_type
        self.__type = get_enum_value(ReportType, type_)
        self.status = status
        self.latest_execution_time = latest_execution_time
        self.latest_end_date = latest_end_date
        self.percentage_complete = percentage_complete

    @property
    def calculation_time(self) -> float:
        """The calculation time between request to and response from Boltweb"""
        return self.__calculation_time

    @calculation_time.setter
    def calculation_time(self, value: float):
        self._property_changed('calculation_time')
        self.__calculation_time = value        

    @property
    def data_set_id(self) -> str:
        """Unique id of dataset."""
        return self.__data_set_id

    @data_set_id.setter
    def data_set_id(self, value: str):
        self._property_changed('data_set_id')
        self.__data_set_id = value        

    @property
    def asset_id(self) -> str:
        """Marquee unique asset identifier."""
        return self.__asset_id

    @asset_id.setter
    def asset_id(self, value: str):
        self._property_changed('asset_id')
        self.__asset_id = value        

    @property
    def created_by_id(self) -> str:
        """Marquee unique identifier"""
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
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def last_updated_by_id(self) -> str:
        """Marquee unique identifier"""
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
    def measures(self) -> Tuple[Union[ReportMeasures, str], ...]:
        """measures to be outputted for the report"""
        return self.__measures

    @measures.setter
    def measures(self, value: Tuple[Union[ReportMeasures, str], ...]):
        self._property_changed('measures')
        self.__measures = value        

    @property
    def name(self) -> str:
        """Report name"""
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
    def parameters(self) -> ReportParameters:
        """Parameters specific to the report type"""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: ReportParameters):
        self._property_changed('parameters')
        self.__parameters = value        

    @property
    def position_source_id(self) -> str:
        """Marquee unique identifier"""
        return self.__position_source_id

    @position_source_id.setter
    def position_source_id(self, value: str):
        self._property_changed('position_source_id')
        self.__position_source_id = value        

    @property
    def position_source_type(self) -> Union[PositionSourceType, str]:
        """Source object for position data"""
        return self.__position_source_type

    @position_source_type.setter
    def position_source_type(self, value: Union[PositionSourceType, str]):
        self._property_changed('position_source_type')
        self.__position_source_type = get_enum_value(PositionSourceType, value)        

    @property
    def type(self) -> Union[ReportType, str]:
        """Type of report to execute"""
        return self.__type

    @type.setter
    def type(self, value: Union[ReportType, str]):
        self._property_changed('type')
        self.__type = get_enum_value(ReportType, value)        

    @property
    def status(self) -> Union[ReportStatus, str]:
        """Status of report run"""
        return self.__status

    @status.setter
    def status(self, value: Union[ReportStatus, str]):
        self._property_changed('status')
        self.__status = get_enum_value(ReportStatus, value)        

    @property
    def latest_execution_time(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__latest_execution_time

    @latest_execution_time.setter
    def latest_execution_time(self, value: datetime.datetime):
        self._property_changed('latest_execution_time')
        self.__latest_execution_time = value        

    @property
    def latest_end_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__latest_end_date

    @latest_end_date.setter
    def latest_end_date(self, value: datetime.date):
        self._property_changed('latest_end_date')
        self.__latest_end_date = value        

    @property
    def percentage_complete(self) -> float:
        """Percentage that the report has been completed so far"""
        return self.__percentage_complete

    @percentage_complete.setter
    def percentage_complete(self, value: float):
        self._property_changed('percentage_complete')
        self.__percentage_complete = value        
