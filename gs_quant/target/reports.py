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
from gs_quant.base import Base, EnumBase, get_enum_value
from gs_quant.target.common import *
from typing import Tuple, Union
import datetime


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
       
    def __init__(self, assetClass: Union[AssetClass, str] = None, transactionCostModel: str = None, tradingCost: float = None, servicingCostLong: float = None, servicingCostShort: float = None, region: str = None, riskModel: Union[RiskModel, str] = None, fxHedged: bool = None, publishToBloomberg: bool = None, publishToReuters: bool = None, includePriceHistory: bool = None, indexUpdate: bool = None, indexRebalance: bool = None, basketAction: Union[BasketAction, str] = None, apiDomain: bool = None, initialPrice: float = None, stockLevelExposures: bool = None, explodePositions: bool = None, scenarioId: str = None, scenarioIds: Tuple[str, ...] = None, scenarioGroupId: str = None, scenarioType: Union[ScenarioType, str] = None, marketModelId: str = None, riskMeasures: Tuple[RiskMeasure, ...] = None, initialPricingDate: datetime.date = None, backcast: bool = None, riskRequest: RiskRequest = None, participationRate: float = None, approveRebalance: bool = None):
        super().__init__()
        self.__assetClass = assetClass if isinstance(assetClass, AssetClass) else get_enum_value(AssetClass, assetClass)
        self.__transactionCostModel = transactionCostModel
        self.__tradingCost = tradingCost
        self.__servicingCostLong = servicingCostLong
        self.__servicingCostShort = servicingCostShort
        self.__region = region
        self.__riskModel = riskModel if isinstance(riskModel, RiskModel) else get_enum_value(RiskModel, riskModel)
        self.__fxHedged = fxHedged
        self.__publishToBloomberg = publishToBloomberg
        self.__publishToReuters = publishToReuters
        self.__includePriceHistory = includePriceHistory
        self.__indexUpdate = indexUpdate
        self.__indexRebalance = indexRebalance
        self.__basketAction = basketAction if isinstance(basketAction, BasketAction) else get_enum_value(BasketAction, basketAction)
        self.__apiDomain = apiDomain
        self.__initialPrice = initialPrice
        self.__stockLevelExposures = stockLevelExposures
        self.__explodePositions = explodePositions
        self.__scenarioId = scenarioId
        self.__scenarioIds = scenarioIds
        self.__scenarioGroupId = scenarioGroupId
        self.__scenarioType = scenarioType if isinstance(scenarioType, ScenarioType) else get_enum_value(ScenarioType, scenarioType)
        self.__marketModelId = marketModelId
        self.__riskMeasures = riskMeasures
        self.__initialPricingDate = initialPricingDate
        self.__backcast = backcast
        self.__riskRequest = riskRequest
        self.__participationRate = participationRate
        self.__approveRebalance = approveRebalance

    @property
    def assetClass(self) -> Union[AssetClass, str]:
        """Asset classification of security. Assets are classified into broad groups which exhibit similar characteristics and behave in a consistent way under different market conditions"""
        return self.__assetClass

    @assetClass.setter
    def assetClass(self, value: Union[AssetClass, str]):
        self.__assetClass = value if isinstance(value, AssetClass) else get_enum_value(AssetClass, value)
        self._property_changed('assetClass')        

    @property
    def transactionCostModel(self) -> str:
        """Determines which model to use"""
        return self.__transactionCostModel

    @transactionCostModel.setter
    def transactionCostModel(self, value: str):
        self.__transactionCostModel = value
        self._property_changed('transactionCostModel')        

    @property
    def tradingCost(self) -> float:
        """bps cost to execute delta"""
        return self.__tradingCost

    @tradingCost.setter
    def tradingCost(self, value: float):
        self.__tradingCost = value
        self._property_changed('tradingCost')        

    @property
    def servicingCostLong(self) -> float:
        """bps cost to fund long positions"""
        return self.__servicingCostLong

    @servicingCostLong.setter
    def servicingCostLong(self, value: float):
        self.__servicingCostLong = value
        self._property_changed('servicingCostLong')        

    @property
    def servicingCostShort(self) -> float:
        """bps cost to fund short positions"""
        return self.__servicingCostShort

    @servicingCostShort.setter
    def servicingCostShort(self, value: float):
        self.__servicingCostShort = value
        self._property_changed('servicingCostShort')        

    @property
    def region(self) -> str:
        """The region of the report"""
        return self.__region

    @region.setter
    def region(self, value: str):
        self.__region = value
        self._property_changed('region')        

    @property
    def riskModel(self) -> Union[RiskModel, str]:
        """Axioma risk model identifier."""
        return self.__riskModel

    @riskModel.setter
    def riskModel(self, value: Union[RiskModel, str]):
        self.__riskModel = value if isinstance(value, RiskModel) else get_enum_value(RiskModel, value)
        self._property_changed('riskModel')        

    @property
    def fxHedged(self) -> bool:
        """Assume portfolio is FX Hedged"""
        return self.__fxHedged

    @fxHedged.setter
    def fxHedged(self, value: bool):
        self.__fxHedged = value
        self._property_changed('fxHedged')        

    @property
    def publishToBloomberg(self) -> bool:
        """Publish Basket to Bloomberg"""
        return self.__publishToBloomberg

    @publishToBloomberg.setter
    def publishToBloomberg(self, value: bool):
        self.__publishToBloomberg = value
        self._property_changed('publishToBloomberg')        

    @property
    def publishToReuters(self) -> bool:
        """Publish Basket to Reuters"""
        return self.__publishToReuters

    @publishToReuters.setter
    def publishToReuters(self, value: bool):
        self.__publishToReuters = value
        self._property_changed('publishToReuters')        

    @property
    def includePriceHistory(self) -> bool:
        """Include full price history"""
        return self.__includePriceHistory

    @includePriceHistory.setter
    def includePriceHistory(self, value: bool):
        self.__includePriceHistory = value
        self._property_changed('includePriceHistory')        

    @property
    def indexUpdate(self) -> bool:
        """Update the basket"""
        return self.__indexUpdate

    @indexUpdate.setter
    def indexUpdate(self, value: bool):
        self.__indexUpdate = value
        self._property_changed('indexUpdate')        

    @property
    def indexRebalance(self) -> bool:
        """Rebalance the basket"""
        return self.__indexRebalance

    @indexRebalance.setter
    def indexRebalance(self, value: bool):
        self.__indexRebalance = value
        self._property_changed('indexRebalance')        

    @property
    def basketAction(self) -> Union[BasketAction, str]:
        """Indicates which basket action triggered the report"""
        return self.__basketAction

    @basketAction.setter
    def basketAction(self, value: Union[BasketAction, str]):
        self.__basketAction = value if isinstance(value, BasketAction) else get_enum_value(BasketAction, value)
        self._property_changed('basketAction')        

    @property
    def apiDomain(self) -> bool:
        """Indicates if report is triggered from ui/api call"""
        return self.__apiDomain

    @apiDomain.setter
    def apiDomain(self, value: bool):
        self.__apiDomain = value
        self._property_changed('apiDomain')        

    @property
    def initialPrice(self) -> float:
        """Initial price for the position set"""
        return self.__initialPrice

    @initialPrice.setter
    def initialPrice(self, value: float):
        self.__initialPrice = value
        self._property_changed('initialPrice')        

    @property
    def stockLevelExposures(self) -> bool:
        """Publish stock level exposures"""
        return self.__stockLevelExposures

    @stockLevelExposures.setter
    def stockLevelExposures(self, value: bool):
        self.__stockLevelExposures = value
        self._property_changed('stockLevelExposures')        

    @property
    def explodePositions(self) -> bool:
        """Whether to explode positions during risk run"""
        return self.__explodePositions

    @explodePositions.setter
    def explodePositions(self, value: bool):
        self.__explodePositions = value
        self._property_changed('explodePositions')        

    @property
    def scenarioId(self) -> str:
        """Marquee unique scenario identifier"""
        return self.__scenarioId

    @scenarioId.setter
    def scenarioId(self, value: str):
        self.__scenarioId = value
        self._property_changed('scenarioId')        

    @property
    def scenarioIds(self) -> Tuple[str, ...]:
        """Array of scenario identifiers related to the object"""
        return self.__scenarioIds

    @scenarioIds.setter
    def scenarioIds(self, value: Tuple[str, ...]):
        self.__scenarioIds = value
        self._property_changed('scenarioIds')        

    @property
    def scenarioGroupId(self) -> str:
        """Marquee unique scenario group identifier"""
        return self.__scenarioGroupId

    @scenarioGroupId.setter
    def scenarioGroupId(self, value: str):
        self.__scenarioGroupId = value
        self._property_changed('scenarioGroupId')        

    @property
    def scenarioType(self) -> Union[ScenarioType, str]:
        """Type of Scenario"""
        return self.__scenarioType

    @scenarioType.setter
    def scenarioType(self, value: Union[ScenarioType, str]):
        self.__scenarioType = value if isinstance(value, ScenarioType) else get_enum_value(ScenarioType, value)
        self._property_changed('scenarioType')        

    @property
    def marketModelId(self) -> str:
        """Marquee unique market model identifier"""
        return self.__marketModelId

    @marketModelId.setter
    def marketModelId(self, value: str):
        self.__marketModelId = value
        self._property_changed('marketModelId')        

    @property
    def riskMeasures(self) -> Tuple[RiskMeasure, ...]:
        """An array of risk measures to get from the risk calculation."""
        return self.__riskMeasures

    @riskMeasures.setter
    def riskMeasures(self, value: Tuple[RiskMeasure, ...]):
        self.__riskMeasures = value
        self._property_changed('riskMeasures')        

    @property
    def initialPricingDate(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__initialPricingDate

    @initialPricingDate.setter
    def initialPricingDate(self, value: datetime.date):
        self.__initialPricingDate = value
        self._property_changed('initialPricingDate')        

    @property
    def backcast(self) -> bool:
        """Use backcasted portfolio derived from positions on the end date."""
        return self.__backcast

    @backcast.setter
    def backcast(self, value: bool):
        self.__backcast = value
        self._property_changed('backcast')        

    @property
    def riskRequest(self) -> RiskRequest:
        """A request for a risk calculation"""
        return self.__riskRequest

    @riskRequest.setter
    def riskRequest(self, value: RiskRequest):
        self.__riskRequest = value
        self._property_changed('riskRequest')        

    @property
    def participationRate(self) -> float:
        """Liquidity analytics participation rate."""
        return self.__participationRate

    @participationRate.setter
    def participationRate(self, value: float):
        self.__participationRate = value
        self._property_changed('participationRate')        

    @property
    def approveRebalance(self) -> bool:
        """An approved basket"""
        return self.__approveRebalance

    @approveRebalance.setter
    def approveRebalance(self, value: bool):
        self.__approveRebalance = value
        self._property_changed('approveRebalance')        


class Report(Base):
               
    def __init__(self, positionSourceId: str, positionSourceType: Union[PositionSourceType, str], type: Union[ReportType, str], parameters: ReportParameters, calculationTime: float = None, dataSetId: str = None, assetId: str = None, createdById: str = None, createdTime: datetime.datetime = None, entitlements: Entitlements = None, entitlementExclusions: EntitlementExclusions = None, id: str = None, lastUpdatedById: str = None, lastUpdatedTime: datetime.datetime = None, measures: Tuple[Union[ReportMeasures, str], ...] = None, name: str = None, ownerId: str = None, status: Union[ReportStatus, str] = None, latestExecutionTime: datetime.datetime = None, latestEndDate: datetime.date = None, percentageComplete: float = None):
        super().__init__()
        self.__calculationTime = calculationTime
        self.__dataSetId = dataSetId
        self.__assetId = assetId
        self.__createdById = createdById
        self.__createdTime = createdTime
        self.__entitlements = entitlements
        self.__entitlementExclusions = entitlementExclusions
        self.__id = id
        self.__lastUpdatedById = lastUpdatedById
        self.__lastUpdatedTime = lastUpdatedTime
        self.__measures = measures
        self.__name = name
        self.__ownerId = ownerId
        self.__parameters = parameters
        self.__positionSourceId = positionSourceId
        self.__positionSourceType = positionSourceType if isinstance(positionSourceType, PositionSourceType) else get_enum_value(PositionSourceType, positionSourceType)
        self.__type = type if isinstance(type, ReportType) else get_enum_value(ReportType, type)
        self.__status = status if isinstance(status, ReportStatus) else get_enum_value(ReportStatus, status)
        self.__latestExecutionTime = latestExecutionTime
        self.__latestEndDate = latestEndDate
        self.__percentageComplete = percentageComplete

    @property
    def calculationTime(self) -> float:
        """The calculation time between request to and response from Boltweb"""
        return self.__calculationTime

    @calculationTime.setter
    def calculationTime(self, value: float):
        self.__calculationTime = value
        self._property_changed('calculationTime')        

    @property
    def dataSetId(self) -> str:
        """Unique id of dataset."""
        return self.__dataSetId

    @dataSetId.setter
    def dataSetId(self, value: str):
        self.__dataSetId = value
        self._property_changed('dataSetId')        

    @property
    def assetId(self) -> str:
        """Marquee unique asset identifier."""
        return self.__assetId

    @assetId.setter
    def assetId(self, value: str):
        self.__assetId = value
        self._property_changed('assetId')        

    @property
    def createdById(self) -> str:
        """Marquee unique identifier"""
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
        """Marquee unique identifier"""
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
    def measures(self) -> Tuple[Union[ReportMeasures, str], ...]:
        """measures to be outputted for the report"""
        return self.__measures

    @measures.setter
    def measures(self, value: Tuple[Union[ReportMeasures, str], ...]):
        self.__measures = value
        self._property_changed('measures')        

    @property
    def name(self) -> str:
        """Report name"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def ownerId(self) -> str:
        """Marquee unique identifier for user who owns the object."""
        return self.__ownerId

    @ownerId.setter
    def ownerId(self, value: str):
        self.__ownerId = value
        self._property_changed('ownerId')        

    @property
    def parameters(self) -> ReportParameters:
        """Parameters specific to the report type"""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: ReportParameters):
        self.__parameters = value
        self._property_changed('parameters')        

    @property
    def positionSourceId(self) -> str:
        """Marquee unique identifier"""
        return self.__positionSourceId

    @positionSourceId.setter
    def positionSourceId(self, value: str):
        self.__positionSourceId = value
        self._property_changed('positionSourceId')        

    @property
    def positionSourceType(self) -> Union[PositionSourceType, str]:
        """Source object for position data"""
        return self.__positionSourceType

    @positionSourceType.setter
    def positionSourceType(self, value: Union[PositionSourceType, str]):
        self.__positionSourceType = value if isinstance(value, PositionSourceType) else get_enum_value(PositionSourceType, value)
        self._property_changed('positionSourceType')        

    @property
    def type(self) -> Union[ReportType, str]:
        """Type of report to execute"""
        return self.__type

    @type.setter
    def type(self, value: Union[ReportType, str]):
        self.__type = value if isinstance(value, ReportType) else get_enum_value(ReportType, value)
        self._property_changed('type')        

    @property
    def status(self) -> Union[ReportStatus, str]:
        """Status of report run"""
        return self.__status

    @status.setter
    def status(self, value: Union[ReportStatus, str]):
        self.__status = value if isinstance(value, ReportStatus) else get_enum_value(ReportStatus, value)
        self._property_changed('status')        

    @property
    def latestExecutionTime(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__latestExecutionTime

    @latestExecutionTime.setter
    def latestExecutionTime(self, value: datetime.datetime):
        self.__latestExecutionTime = value
        self._property_changed('latestExecutionTime')        

    @property
    def latestEndDate(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__latestEndDate

    @latestEndDate.setter
    def latestEndDate(self, value: datetime.date):
        self.__latestEndDate = value
        self._property_changed('latestEndDate')        

    @property
    def percentageComplete(self) -> float:
        """Percentage that the report has been completed so far"""
        return self.__percentageComplete

    @percentageComplete.setter
    def percentageComplete(self, value: float):
        self.__percentageComplete = value
        self._property_changed('percentageComplete')        
