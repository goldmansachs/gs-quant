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


class MarketDataFrequency(EnumBase, Enum):    
    
    Real_Time = 'Real Time'
    End_Of_Day = 'End Of Day'
    
    def __repr__(self):
        return self.value


class MarketDataMeasure(EnumBase, Enum):    
    
    Last = 'Last'
    Curve = 'Curve'
    Close_Change = 'Close Change'
    Previous_Close = 'Previous Close'
    
    def __repr__(self):
        return self.value


class MeasureEntityType(EnumBase, Enum):    
    
    """Entity type associated with a measure."""

    ASSET = 'ASSET'
    BACKTEST = 'BACKTEST'
    KPI = 'KPI'
    
    def __repr__(self):
        return self.value


class AdvancedFilter(Base):
        
    """Advanced filter for numeric fields."""
       
    def __init__(self, column: str, value: float, operator: str):
        super().__init__()
        self.__column = column
        self.__value = value
        self.__operator = operator

    @property
    def column(self) -> str:
        """Database column to filter on."""
        return self.__column

    @column.setter
    def column(self, value: str):
        self.__column = value
        self._property_changed('column')        

    @property
    def value(self) -> float:
        """Value to compare against."""
        return self.__value

    @value.setter
    def value(self, value: float):
        self.__value = value
        self._property_changed('value')        

    @property
    def operator(self) -> str:
        """Comparison operator."""
        return self.__operator

    @operator.setter
    def operator(self, value: str):
        self.__operator = value
        self._property_changed('operator')        


class DataFilter(Base):
        
    """Filter on specified field."""
       
    def __init__(self, field: str, values: Tuple[str, ...], column: str = None):
        super().__init__()
        self.__field = field
        self.__column = column
        self.__values = values

    @property
    def field(self) -> str:
        """Field to filter on."""
        return self.__field

    @field.setter
    def field(self, value: str):
        self.__field = value
        self._property_changed('field')        

    @property
    def column(self) -> str:
        """Database column name."""
        return self.__column

    @column.setter
    def column(self, value: str):
        self.__column = value
        self._property_changed('column')        

    @property
    def values(self) -> Tuple[str, ...]:
        """Value(s) to match."""
        return self.__values

    @values.setter
    def values(self, value: Tuple[str, ...]):
        self.__values = value
        self._property_changed('values')        


class DataGroup(Base):
        
    """Dataset grouped by context (key dimensions)"""
       
    def __init__(self, ):
        super().__init__()
        


class DataQuery(Base):
               
    def __init__(self, id: str = None, dataSetId: str = None, format: Union[Format, str] = None, marketDataCoordinates: Tuple[MarketDataCoordinate, ...] = None, where: FieldFilterMap = None, vendor: str = None, startDate: datetime.date = None, endDate: datetime.date = None, startTime: datetime.datetime = None, endTime: datetime.datetime = None, asOfTime: datetime.datetime = None, idAsOfDate: datetime.date = None, useTemporalXRef: bool = False, since: datetime.datetime = None, dates: Tuple[datetime.date, ...] = None, times: Tuple[datetime.datetime, ...] = None, delay: int = None, intervals: int = None, pollingInterval: int = None, grouped: bool = None, fields: Tuple[Union[dict, str], ...] = None):
        super().__init__()
        self.__id = id
        self.__dataSetId = dataSetId
        self.__format = format if isinstance(format, Format) else get_enum_value(Format, format)
        self.__marketDataCoordinates = marketDataCoordinates
        self.__where = where
        self.__vendor = vendor
        self.__startDate = startDate
        self.__endDate = endDate
        self.__startTime = startTime
        self.__endTime = endTime
        self.__asOfTime = asOfTime
        self.__idAsOfDate = idAsOfDate
        self.__useTemporalXRef = useTemporalXRef
        self.__since = since
        self.__dates = dates
        self.__times = times
        self.__delay = delay
        self.__intervals = intervals
        self.__pollingInterval = pollingInterval
        self.__grouped = grouped
        self.__fields = fields

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value
        self._property_changed('id')        

    @property
    def dataSetId(self) -> str:
        """Marquee unique identifier"""
        return self.__dataSetId

    @dataSetId.setter
    def dataSetId(self, value: str):
        self.__dataSetId = value
        self._property_changed('dataSetId')        

    @property
    def format(self) -> Union[Format, str]:
        """Alternative format for data to be returned in"""
        return self.__format

    @format.setter
    def format(self, value: Union[Format, str]):
        self.__format = value if isinstance(value, Format) else get_enum_value(Format, value)
        self._property_changed('format')        

    @property
    def marketDataCoordinates(self) -> Tuple[MarketDataCoordinate, ...]:
        """Object representation of a market data coordinate"""
        return self.__marketDataCoordinates

    @marketDataCoordinates.setter
    def marketDataCoordinates(self, value: Tuple[MarketDataCoordinate, ...]):
        self.__marketDataCoordinates = value
        self._property_changed('marketDataCoordinates')        

    @property
    def where(self) -> FieldFilterMap:
        """Filters on data fields."""
        return self.__where

    @where.setter
    def where(self, value: FieldFilterMap):
        self.__where = value
        self._property_changed('where')        

    @property
    def vendor(self) -> str:
        return self.__vendor

    @vendor.setter
    def vendor(self, value: str):
        self.__vendor = value
        self._property_changed('vendor')        

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
    def startTime(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__startTime

    @startTime.setter
    def startTime(self, value: datetime.datetime):
        self.__startTime = value
        self._property_changed('startTime')        

    @property
    def endTime(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__endTime

    @endTime.setter
    def endTime(self, value: datetime.datetime):
        self.__endTime = value
        self._property_changed('endTime')        

    @property
    def asOfTime(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__asOfTime

    @asOfTime.setter
    def asOfTime(self, value: datetime.datetime):
        self.__asOfTime = value
        self._property_changed('asOfTime')        

    @property
    def idAsOfDate(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__idAsOfDate

    @idAsOfDate.setter
    def idAsOfDate(self, value: datetime.date):
        self.__idAsOfDate = value
        self._property_changed('idAsOfDate')        

    @property
    def useTemporalXRef(self) -> bool:
        """Set to true when xrefs provided in the query should be treated in a temporal way (e.g. get data points which had a certain BCID at some point in time, not which currently have it)."""
        return self.__useTemporalXRef

    @useTemporalXRef.setter
    def useTemporalXRef(self, value: bool):
        self.__useTemporalXRef = value
        self._property_changed('useTemporalXRef')        

    @property
    def since(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__since

    @since.setter
    def since(self, value: datetime.datetime):
        self.__since = value
        self._property_changed('since')        

    @property
    def dates(self) -> Tuple[datetime.date, ...]:
        """Select and return specific dates from dataset query results."""
        return self.__dates

    @dates.setter
    def dates(self, value: Tuple[datetime.date, ...]):
        self.__dates = value
        self._property_changed('dates')        

    @property
    def times(self) -> Tuple[datetime.datetime, ...]:
        """Select and return specific times from dataset query results."""
        return self.__times

    @times.setter
    def times(self, value: Tuple[datetime.datetime, ...]):
        self.__times = value
        self._property_changed('times')        

    @property
    def delay(self) -> int:
        """Number of minutes to delay returning data."""
        return self.__delay

    @delay.setter
    def delay(self, value: int):
        self.__delay = value
        self._property_changed('delay')        

    @property
    def intervals(self) -> int:
        """Number of intervals for which to return output times, for example if 10, it will return 10 data points evenly spaced over the time/date range."""
        return self.__intervals

    @intervals.setter
    def intervals(self, value: int):
        self.__intervals = value
        self._property_changed('intervals')        

    @property
    def pollingInterval(self) -> int:
        """When streaming, wait for this number of seconds between poll attempts."""
        return self.__pollingInterval

    @pollingInterval.setter
    def pollingInterval(self, value: int):
        self.__pollingInterval = value
        self._property_changed('pollingInterval')        

    @property
    def grouped(self) -> bool:
        """Set to true to return results grouped by a given context (set of dimensions)."""
        return self.__grouped

    @grouped.setter
    def grouped(self, value: bool):
        self.__grouped = value
        self._property_changed('grouped')        

    @property
    def fields(self) -> Tuple[Union[dict, str], ...]:
        """Fields to be returned."""
        return self.__fields

    @fields.setter
    def fields(self, value: Tuple[Union[dict, str], ...]):
        self.__fields = value
        self._property_changed('fields')        


class DataSetDefaults(Base):
        
    """Default settings."""
       
    def __init__(self, startSeconds: float = None, endSeconds: float = None, delaySeconds: float = None):
        super().__init__()
        self.__startSeconds = startSeconds
        self.__endSeconds = endSeconds
        self.__delaySeconds = delaySeconds

    @property
    def startSeconds(self) -> float:
        """Default start date/time, in seconds before current time."""
        return self.__startSeconds

    @startSeconds.setter
    def startSeconds(self, value: float):
        self.__startSeconds = value
        self._property_changed('startSeconds')        

    @property
    def endSeconds(self) -> float:
        """Default end date/time, in seconds before current time."""
        return self.__endSeconds

    @endSeconds.setter
    def endSeconds(self, value: float):
        self.__endSeconds = value
        self._property_changed('endSeconds')        

    @property
    def delaySeconds(self) -> float:
        """Default market delay to apply, in seconds."""
        return self.__delaySeconds

    @delaySeconds.setter
    def delaySeconds(self, value: float):
        self.__delaySeconds = value
        self._property_changed('delaySeconds')        


class DataSetParameters(Base):
        
    """Dataset parameters."""
       
    def __init__(self, uploadDataPolicy: str, logicalDb: str, symbolStrategy: str, applyMarketDataEntitlements: bool, coverage: str, frequency: str, methodology: str, history: str, category: str = None, subCategory: str = None, assetClass: Union[AssetClass, str] = None, ownerIds: Tuple[str, ...] = None, approverIds: Tuple[str, ...] = None, supportIds: Tuple[str, ...] = None, supportDistributionList: Tuple[str, ...] = None, identifierMapperName: str = None, constantSymbols: Tuple[str, ...] = None, underlyingDataSetId: str = None, immutable: bool = None, includeInCatalog: bool = None, overrideQueryColumnIds: Tuple[str, ...] = None, plot: bool = None, coverageEnabled: bool = True):
        super().__init__()
        self.__category = category
        self.__subCategory = subCategory
        self.__methodology = methodology
        self.__coverage = coverage
        self.__history = history
        self.__frequency = frequency
        self.__assetClass = assetClass if isinstance(assetClass, AssetClass) else get_enum_value(AssetClass, assetClass)
        self.__ownerIds = ownerIds
        self.__approverIds = approverIds
        self.__supportIds = supportIds
        self.__supportDistributionList = supportDistributionList
        self.__applyMarketDataEntitlements = applyMarketDataEntitlements
        self.__uploadDataPolicy = uploadDataPolicy
        self.__identifierMapperName = identifierMapperName
        self.__logicalDb = logicalDb
        self.__symbolStrategy = symbolStrategy
        self.__constantSymbols = constantSymbols
        self.__underlyingDataSetId = underlyingDataSetId
        self.__immutable = immutable
        self.__includeInCatalog = includeInCatalog
        self.__overrideQueryColumnIds = overrideQueryColumnIds
        self.__plot = plot
        self.__coverageEnabled = coverageEnabled

    @property
    def category(self) -> str:
        """Top level grouping."""
        return self.__category

    @category.setter
    def category(self, value: str):
        self.__category = value
        self._property_changed('category')        

    @property
    def subCategory(self) -> str:
        """Second level grouping."""
        return self.__subCategory

    @subCategory.setter
    def subCategory(self, value: str):
        self.__subCategory = value
        self._property_changed('subCategory')        

    @property
    def methodology(self) -> str:
        """Methodology of dataset."""
        return self.__methodology

    @methodology.setter
    def methodology(self, value: str):
        self.__methodology = value
        self._property_changed('methodology')        

    @property
    def coverage(self) -> str:
        """Coverage of dataset."""
        return self.__coverage

    @coverage.setter
    def coverage(self, value: str):
        self.__coverage = value
        self._property_changed('coverage')        

    @property
    def history(self) -> str:
        """Period of time covered by dataset."""
        return self.__history

    @history.setter
    def history(self, value: str):
        self.__history = value
        self._property_changed('history')        

    @property
    def frequency(self) -> str:
        """Frequency of updates to dataset."""
        return self.__frequency

    @frequency.setter
    def frequency(self, value: str):
        self.__frequency = value
        self._property_changed('frequency')        

    @property
    def assetClass(self) -> Union[AssetClass, str]:
        """Asset classification of security. Assets are classified into broad groups which exhibit similar characteristics and behave in a consistent way under different market conditions"""
        return self.__assetClass

    @assetClass.setter
    def assetClass(self, value: Union[AssetClass, str]):
        self.__assetClass = value if isinstance(value, AssetClass) else get_enum_value(AssetClass, value)
        self._property_changed('assetClass')        

    @property
    def ownerIds(self) -> Tuple[str, ...]:
        """Users who own dataset."""
        return self.__ownerIds

    @ownerIds.setter
    def ownerIds(self, value: Tuple[str, ...]):
        self.__ownerIds = value
        self._property_changed('ownerIds')        

    @property
    def approverIds(self) -> Tuple[str, ...]:
        """Users who can grant access to dataset."""
        return self.__approverIds

    @approverIds.setter
    def approverIds(self, value: Tuple[str, ...]):
        self.__approverIds = value
        self._property_changed('approverIds')        

    @property
    def supportIds(self) -> Tuple[str, ...]:
        """Users who support dataset."""
        return self.__supportIds

    @supportIds.setter
    def supportIds(self, value: Tuple[str, ...]):
        self.__supportIds = value
        self._property_changed('supportIds')        

    @property
    def supportDistributionList(self) -> Tuple[str, ...]:
        """Distribution list who support dataset."""
        return self.__supportDistributionList

    @supportDistributionList.setter
    def supportDistributionList(self, value: Tuple[str, ...]):
        self.__supportDistributionList = value
        self._property_changed('supportDistributionList')        

    @property
    def applyMarketDataEntitlements(self) -> bool:
        """Whether market data entitlements are checked."""
        return self.__applyMarketDataEntitlements

    @applyMarketDataEntitlements.setter
    def applyMarketDataEntitlements(self, value: bool):
        self.__applyMarketDataEntitlements = value
        self._property_changed('applyMarketDataEntitlements')        

    @property
    def uploadDataPolicy(self) -> str:
        """Policy governing uploads."""
        return self.__uploadDataPolicy

    @uploadDataPolicy.setter
    def uploadDataPolicy(self, value: str):
        self.__uploadDataPolicy = value
        self._property_changed('uploadDataPolicy')        

    @property
    def identifierMapperName(self) -> str:
        """Identifier mapper associated with dataset."""
        return self.__identifierMapperName

    @identifierMapperName.setter
    def identifierMapperName(self, value: str):
        self.__identifierMapperName = value
        self._property_changed('identifierMapperName')        

    @property
    def identifierUpdaterName(self) -> str:
        """Identifier updater associated with dataset."""
        return 'REPORT_IDENTIFIER_UPDATER'        

    @property
    def logicalDb(self) -> str:
        """Database where contents are (to be) stored."""
        return self.__logicalDb

    @logicalDb.setter
    def logicalDb(self, value: str):
        self.__logicalDb = value
        self._property_changed('logicalDb')        

    @property
    def symbolStrategy(self) -> str:
        """Method for looking up database table name."""
        return self.__symbolStrategy

    @symbolStrategy.setter
    def symbolStrategy(self, value: str):
        self.__symbolStrategy = value
        self._property_changed('symbolStrategy')        

    @property
    def constantSymbols(self) -> Tuple[str, ...]:
        return self.__constantSymbols

    @constantSymbols.setter
    def constantSymbols(self, value: Tuple[str, ...]):
        self.__constantSymbols = value
        self._property_changed('constantSymbols')        

    @property
    def underlyingDataSetId(self) -> str:
        """Dataset on which this (virtual) dataset is based."""
        return self.__underlyingDataSetId

    @underlyingDataSetId.setter
    def underlyingDataSetId(self, value: str):
        self.__underlyingDataSetId = value
        self._property_changed('underlyingDataSetId')        

    @property
    def immutable(self) -> bool:
        """Whether dataset is immutable (i.e. not writable through data service)."""
        return self.__immutable

    @immutable.setter
    def immutable(self, value: bool):
        self.__immutable = value
        self._property_changed('immutable')        

    @property
    def includeInCatalog(self) -> bool:
        """Whether dataset should be in the catalog."""
        return self.__includeInCatalog

    @includeInCatalog.setter
    def includeInCatalog(self, value: bool):
        self.__includeInCatalog = value
        self._property_changed('includeInCatalog')        

    @property
    def overrideQueryColumnIds(self) -> Tuple[str, ...]:
        """Explicit set of database columns to query for, regardless of fields specified in request."""
        return self.__overrideQueryColumnIds

    @overrideQueryColumnIds.setter
    def overrideQueryColumnIds(self, value: Tuple[str, ...]):
        self.__overrideQueryColumnIds = value
        self._property_changed('overrideQueryColumnIds')        

    @property
    def plot(self) -> bool:
        """Whether dataset is intended for use in Plottool."""
        return self.__plot

    @plot.setter
    def plot(self, value: bool):
        self.__plot = value
        self._property_changed('plot')        

    @property
    def coverageEnabled(self) -> bool:
        """Whether coverage requests are available for the DataSet"""
        return self.__coverageEnabled

    @coverageEnabled.setter
    def coverageEnabled(self, value: bool):
        self.__coverageEnabled = value
        self._property_changed('coverageEnabled')        


class FieldColumnPair(Base):
        
    """Map from fields to database columns."""
       
    def __init__(self, field: str = None, column: str = None, fieldDescription: str = None):
        super().__init__()
        self.__field = field
        self.__column = column
        self.__fieldDescription = fieldDescription

    @property
    def field(self) -> str:
        """Field name."""
        return self.__field

    @field.setter
    def field(self, value: str):
        self.__field = value
        self._property_changed('field')        

    @property
    def column(self) -> str:
        """Database column name."""
        return self.__column

    @column.setter
    def column(self, value: str):
        self.__column = value
        self._property_changed('column')        

    @property
    def fieldDescription(self) -> str:
        """Custom description (overrides field default)."""
        return self.__fieldDescription

    @fieldDescription.setter
    def fieldDescription(self, value: str):
        self.__fieldDescription = value
        self._property_changed('fieldDescription')        


class HistoryFilter(Base):
        
    """Restricts queries against dataset to an absolute or relative range."""
       
    def __init__(self, absoluteStart: datetime.datetime = None, absoluteEnd: datetime.datetime = None, relativeStartSeconds: float = None, relativeEndSeconds: float = None):
        super().__init__()
        self.__absoluteStart = absoluteStart
        self.__absoluteEnd = absoluteEnd
        self.__relativeStartSeconds = relativeStartSeconds
        self.__relativeEndSeconds = relativeEndSeconds

    @property
    def absoluteStart(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__absoluteStart

    @absoluteStart.setter
    def absoluteStart(self, value: datetime.datetime):
        self.__absoluteStart = value
        self._property_changed('absoluteStart')        

    @property
    def absoluteEnd(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__absoluteEnd

    @absoluteEnd.setter
    def absoluteEnd(self, value: datetime.datetime):
        self.__absoluteEnd = value
        self._property_changed('absoluteEnd')        

    @property
    def relativeStartSeconds(self) -> float:
        """Earliest start time in seconds before current time."""
        return self.__relativeStartSeconds

    @relativeStartSeconds.setter
    def relativeStartSeconds(self, value: float):
        self.__relativeStartSeconds = value
        self._property_changed('relativeStartSeconds')        

    @property
    def relativeEndSeconds(self) -> float:
        """Latest end time in seconds before current time."""
        return self.__relativeEndSeconds

    @relativeEndSeconds.setter
    def relativeEndSeconds(self, value: float):
        self.__relativeEndSeconds = value
        self._property_changed('relativeEndSeconds')        


class MDAPI(Base):
        
    """Defines MDAPI fields."""
       
    def __init__(self, type: str, quotingStyles: Tuple[dict, ...], class_: str = None):
        super().__init__()
        self.__class = class_
        self.__type = type
        self.__quotingStyles = quotingStyles

    @property
    def class_(self) -> str:
        """MDAPI Class."""
        return self.__class

    @class_.setter
    def class_(self, value: str):
        self.__class = value
        self._property_changed('class')        

    @property
    def type(self) -> str:
        """The MDAPI Type field (private)"""
        return self.__type

    @type.setter
    def type(self, value: str):
        self.__type = value
        self._property_changed('type')        

    @property
    def quotingStyles(self) -> Tuple[dict, ...]:
        """Map from MDAPI QuotingStyles to database columns"""
        return self.__quotingStyles

    @quotingStyles.setter
    def quotingStyles(self, value: Tuple[dict, ...]):
        self.__quotingStyles = value
        self._property_changed('quotingStyles')        


class MDAPIDataQueryResponse(Base):
               
    def __init__(self, data: Tuple[FieldValueMap, ...] = None):
        super().__init__()
        self.__data = data

    @property
    def data(self) -> Tuple[FieldValueMap, ...]:
        """Array of data elements from dataset"""
        return self.__data

    @data.setter
    def data(self, value: Tuple[FieldValueMap, ...]):
        self.__data = value
        self._property_changed('data')        


class MarketDataField(Base):
               
    def __init__(self, name: str = None, mapping: str = None):
        super().__init__()
        self.__name = name
        self.__mapping = mapping

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def mapping(self) -> str:
        return self.__mapping

    @mapping.setter
    def mapping(self, value: str):
        self.__mapping = value
        self._property_changed('mapping')        


class MarketDataFilteredField(Base):
               
    def __init__(self, field: str = None, defaultValue: str = None, defaultNumericalValue: float = None, numericalValues: Tuple[float, ...] = None, values: Tuple[str, ...] = None):
        super().__init__()
        self.__field = field
        self.__defaultValue = defaultValue
        self.__defaultNumericalValue = defaultNumericalValue
        self.__numericalValues = numericalValues
        self.__values = values

    @property
    def field(self) -> str:
        """Filtered field name"""
        return self.__field

    @field.setter
    def field(self, value: str):
        self.__field = value
        self._property_changed('field')        

    @property
    def defaultValue(self) -> str:
        """Default filtered field"""
        return self.__defaultValue

    @defaultValue.setter
    def defaultValue(self, value: str):
        self.__defaultValue = value
        self._property_changed('defaultValue')        

    @property
    def defaultNumericalValue(self) -> float:
        """Default numerical filtered field"""
        return self.__defaultNumericalValue

    @defaultNumericalValue.setter
    def defaultNumericalValue(self, value: float):
        self.__defaultNumericalValue = value
        self._property_changed('defaultNumericalValue')        

    @property
    def numericalValues(self) -> Tuple[float, ...]:
        """Array of numerical filtered fields"""
        return self.__numericalValues

    @numericalValues.setter
    def numericalValues(self, value: Tuple[float, ...]):
        self.__numericalValues = value
        self._property_changed('numericalValues')        

    @property
    def values(self) -> Tuple[str, ...]:
        """Array of filtered fields"""
        return self.__values

    @values.setter
    def values(self, value: Tuple[str, ...]):
        self.__values = value
        self._property_changed('values')        


class MeasureBacktest(Base):
        
    """Describes backtests that should be associated with a measure."""
       
    def __init__(self, ):
        super().__init__()
        


class MeasureKpi(Base):
        
    """Describes KPIs that should be associated with a measure."""
       
    def __init__(self, ):
        super().__init__()
        


class MidPrice(Base):
        
    """Specification for a mid price column derived from bid and ask columns."""
       
    def __init__(self, bidColumn: str = None, askColumn: str = None, midColumn: str = None):
        super().__init__()
        self.__bidColumn = bidColumn
        self.__askColumn = askColumn
        self.__midColumn = midColumn

    @property
    def bidColumn(self) -> str:
        """Database column name."""
        return self.__bidColumn

    @bidColumn.setter
    def bidColumn(self, value: str):
        self.__bidColumn = value
        self._property_changed('bidColumn')        

    @property
    def askColumn(self) -> str:
        """Database column name."""
        return self.__askColumn

    @askColumn.setter
    def askColumn(self, value: str):
        self.__askColumn = value
        self._property_changed('askColumn')        

    @property
    def midColumn(self) -> str:
        """Database column name."""
        return self.__midColumn

    @midColumn.setter
    def midColumn(self, value: str):
        self.__midColumn = value
        self._property_changed('midColumn')        


class ParserEntity(Base):
        
    """Settings for a parser processor"""
       
    def __init__(self, onlyNormalizedFields: bool = None, quotes: bool = None, trades: bool = None):
        super().__init__()
        self.__onlyNormalizedFields = onlyNormalizedFields
        self.__quotes = quotes
        self.__trades = trades

    @property
    def onlyNormalizedFields(self) -> bool:
        """Setting for onlyNormalizedFields."""
        return self.__onlyNormalizedFields

    @onlyNormalizedFields.setter
    def onlyNormalizedFields(self, value: bool):
        self.__onlyNormalizedFields = value
        self._property_changed('onlyNormalizedFields')        

    @property
    def quotes(self) -> bool:
        """Setting for quotes."""
        return self.__quotes

    @quotes.setter
    def quotes(self, value: bool):
        self.__quotes = value
        self._property_changed('quotes')        

    @property
    def trades(self) -> bool:
        """Setting for trades."""
        return self.__trades

    @trades.setter
    def trades(self, value: bool):
        self.__trades = value
        self._property_changed('trades')        


class ComplexFilter(Base):
        
    """A compound filter for data requests."""
       
    def __init__(self, operator: str, simpleFilters: Tuple[DataFilter, ...]):
        super().__init__()
        self.__operator = operator
        self.__simpleFilters = simpleFilters

    @property
    def operator(self) -> str:
        return self.__operator

    @operator.setter
    def operator(self, value: str):
        self.__operator = value
        self._property_changed('operator')        

    @property
    def simpleFilters(self) -> Tuple[DataFilter, ...]:
        """Filter on specified field."""
        return self.__simpleFilters

    @simpleFilters.setter
    def simpleFilters(self, value: Tuple[DataFilter, ...]):
        self.__simpleFilters = value
        self._property_changed('simpleFilters')        


class DataQueryResponse(Base):
               
    def __init__(self, type: str, requestId: str = None, errorMessage: str = None, id: str = None, dataSetId: str = None, entityType: Union[MeasureEntityType, str] = None, delay: int = None, data: Tuple[FieldValueMap, ...] = None, groups: Tuple[DataGroup, ...] = None):
        super().__init__()
        self.__requestId = requestId
        self.__type = type
        self.__errorMessage = errorMessage
        self.__id = id
        self.__dataSetId = dataSetId
        self.__entityType = entityType if isinstance(entityType, MeasureEntityType) else get_enum_value(MeasureEntityType, entityType)
        self.__delay = delay
        self.__data = data
        self.__groups = groups

    @property
    def requestId(self) -> str:
        """Marquee unique identifier"""
        return self.__requestId

    @requestId.setter
    def requestId(self, value: str):
        self.__requestId = value
        self._property_changed('requestId')        

    @property
    def type(self) -> str:
        return self.__type

    @type.setter
    def type(self, value: str):
        self.__type = value
        self._property_changed('type')        

    @property
    def errorMessage(self) -> str:
        return self.__errorMessage

    @errorMessage.setter
    def errorMessage(self, value: str):
        self.__errorMessage = value
        self._property_changed('errorMessage')        

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value
        self._property_changed('id')        

    @property
    def dataSetId(self) -> str:
        """Unique id of dataset."""
        return self.__dataSetId

    @dataSetId.setter
    def dataSetId(self, value: str):
        self.__dataSetId = value
        self._property_changed('dataSetId')        

    @property
    def entityType(self) -> Union[MeasureEntityType, str]:
        """Entity type associated with a measure."""
        return self.__entityType

    @entityType.setter
    def entityType(self, value: Union[MeasureEntityType, str]):
        self.__entityType = value if isinstance(value, MeasureEntityType) else get_enum_value(MeasureEntityType, value)
        self._property_changed('entityType')        

    @property
    def delay(self) -> int:
        return self.__delay

    @delay.setter
    def delay(self, value: int):
        self.__delay = value
        self._property_changed('delay')        

    @property
    def data(self) -> Tuple[FieldValueMap, ...]:
        """Array of data elements from dataset"""
        return self.__data

    @data.setter
    def data(self, value: Tuple[FieldValueMap, ...]):
        self.__data = value
        self._property_changed('data')        

    @property
    def groups(self) -> Tuple[DataGroup, ...]:
        """If the data is requested in grouped mode, will return data group object"""
        return self.__groups

    @groups.setter
    def groups(self, value: Tuple[DataGroup, ...]):
        self.__groups = value
        self._property_changed('groups')        


class DataSetDimensions(Base):
        
    """Dataset dimensions."""
       
    def __init__(self, timeField: str, transactionTimeField: str = None, symbolDimensions: Tuple[str, ...] = None, nonSymbolDimensions: Tuple[FieldColumnPair, ...] = None, keyDimensions: Tuple[str, ...] = None, measures: Tuple[FieldColumnPair, ...] = None, entityDimension: str = None):
        super().__init__()
        self.__timeField = timeField
        self.__transactionTimeField = transactionTimeField
        self.__symbolDimensions = symbolDimensions
        self.__nonSymbolDimensions = nonSymbolDimensions
        self.__keyDimensions = keyDimensions
        self.__measures = measures
        self.__entityDimension = entityDimension

    @property
    def timeField(self) -> str:
        return self.__timeField

    @timeField.setter
    def timeField(self, value: str):
        self.__timeField = value
        self._property_changed('timeField')        

    @property
    def transactionTimeField(self) -> str:
        """For bi-temporal datasets, field for capturing the time at which a data point was updated."""
        return self.__transactionTimeField

    @transactionTimeField.setter
    def transactionTimeField(self, value: str):
        self.__transactionTimeField = value
        self._property_changed('transactionTimeField')        

    @property
    def symbolDimensions(self) -> Tuple[str, ...]:
        """Set of fields that determine database table name."""
        return self.__symbolDimensions

    @symbolDimensions.setter
    def symbolDimensions(self, value: Tuple[str, ...]):
        self.__symbolDimensions = value
        self._property_changed('symbolDimensions')        

    @property
    def nonSymbolDimensions(self) -> Tuple[FieldColumnPair, ...]:
        """Fields that are not nullable."""
        return self.__nonSymbolDimensions

    @nonSymbolDimensions.setter
    def nonSymbolDimensions(self, value: Tuple[FieldColumnPair, ...]):
        self.__nonSymbolDimensions = value
        self._property_changed('nonSymbolDimensions')        

    @property
    def keyDimensions(self) -> Tuple[str, ...]:
        return self.__keyDimensions

    @keyDimensions.setter
    def keyDimensions(self, value: Tuple[str, ...]):
        self.__keyDimensions = value
        self._property_changed('keyDimensions')        

    @property
    def measures(self) -> Tuple[FieldColumnPair, ...]:
        """Fields that are nullable."""
        return self.__measures

    @measures.setter
    def measures(self, value: Tuple[FieldColumnPair, ...]):
        self.__measures = value
        self._property_changed('measures')        

    @property
    def entityDimension(self) -> str:
        """Symbol dimension corresponding to an entity e.g. asset or report."""
        return self.__entityDimension

    @entityDimension.setter
    def entityDimension(self, value: str):
        self.__entityDimension = value
        self._property_changed('entityDimension')        


class MDAPIDataBatchResponse(Base):
               
    def __init__(self, requestId: str = None, responses: Tuple[MDAPIDataQueryResponse, ...] = None):
        super().__init__()
        self.__requestId = requestId
        self.__responses = responses

    @property
    def requestId(self) -> str:
        """Marquee unique identifier"""
        return self.__requestId

    @requestId.setter
    def requestId(self, value: str):
        self.__requestId = value
        self._property_changed('requestId')        

    @property
    def responses(self) -> Tuple[MDAPIDataQueryResponse, ...]:
        """MDAPI Data query responses"""
        return self.__responses

    @responses.setter
    def responses(self, value: Tuple[MDAPIDataQueryResponse, ...]):
        self.__responses = value
        self._property_changed('responses')        


class MarketDataMapping(Base):
               
    def __init__(self, assetClass: Union[AssetClass, str] = None, queryType: str = None, description: str = None, scale: float = None, frequency: Union[MarketDataFrequency, str] = None, measures: Tuple[Union[MarketDataMeasure, str], ...] = None, dataSet: str = None, vendor: Union[MarketDataVendor, str] = None, fields: Tuple[MarketDataField, ...] = None, rank: float = None, filteredFields: Tuple[MarketDataFilteredField, ...] = None, assetTypes: Tuple[Union[AssetType, str], ...] = None, entityType: Union[MeasureEntityType, str] = None, backtestEntity: MeasureBacktest = None, kpiEntity: MeasureKpi = None):
        super().__init__()
        self.__assetClass = assetClass if isinstance(assetClass, AssetClass) else get_enum_value(AssetClass, assetClass)
        self.__queryType = queryType
        self.__description = description
        self.__scale = scale
        self.__frequency = frequency if isinstance(frequency, MarketDataFrequency) else get_enum_value(MarketDataFrequency, frequency)
        self.__measures = measures
        self.__dataSet = dataSet
        self.__vendor = vendor if isinstance(vendor, MarketDataVendor) else get_enum_value(MarketDataVendor, vendor)
        self.__fields = fields
        self.__rank = rank
        self.__filteredFields = filteredFields
        self.__assetTypes = assetTypes
        self.__entityType = entityType if isinstance(entityType, MeasureEntityType) else get_enum_value(MeasureEntityType, entityType)
        self.__backtestEntity = backtestEntity
        self.__kpiEntity = kpiEntity

    @property
    def assetClass(self) -> Union[AssetClass, str]:
        """Asset class that is applicable for mapping."""
        return self.__assetClass

    @assetClass.setter
    def assetClass(self, value: Union[AssetClass, str]):
        self.__assetClass = value if isinstance(value, AssetClass) else get_enum_value(AssetClass, value)
        self._property_changed('assetClass')        

    @property
    def queryType(self) -> str:
        """Market data query type."""
        return self.__queryType

    @queryType.setter
    def queryType(self, value: str):
        self.__queryType = value
        self._property_changed('queryType')        

    @property
    def description(self) -> str:
        """Query type description"""
        return self.__description

    @description.setter
    def description(self, value: str):
        self.__description = value
        self._property_changed('description')        

    @property
    def scale(self) -> float:
        """Scale multiplier for time series"""
        return self.__scale

    @scale.setter
    def scale(self, value: float):
        self.__scale = value
        self._property_changed('scale')        

    @property
    def frequency(self) -> Union[MarketDataFrequency, str]:
        return self.__frequency

    @frequency.setter
    def frequency(self, value: Union[MarketDataFrequency, str]):
        self.__frequency = value if isinstance(value, MarketDataFrequency) else get_enum_value(MarketDataFrequency, value)
        self._property_changed('frequency')        

    @property
    def measures(self) -> Tuple[Union[MarketDataMeasure, str], ...]:
        return self.__measures

    @measures.setter
    def measures(self, value: Tuple[Union[MarketDataMeasure, str], ...]):
        self.__measures = value
        self._property_changed('measures')        

    @property
    def dataSet(self) -> str:
        """Marquee unique identifier"""
        return self.__dataSet

    @dataSet.setter
    def dataSet(self, value: str):
        self.__dataSet = value
        self._property_changed('dataSet')        

    @property
    def vendor(self) -> Union[MarketDataVendor, str]:
        return self.__vendor

    @vendor.setter
    def vendor(self, value: Union[MarketDataVendor, str]):
        self.__vendor = value if isinstance(value, MarketDataVendor) else get_enum_value(MarketDataVendor, value)
        self._property_changed('vendor')        

    @property
    def fields(self) -> Tuple[MarketDataField, ...]:
        return self.__fields

    @fields.setter
    def fields(self, value: Tuple[MarketDataField, ...]):
        self.__fields = value
        self._property_changed('fields')        

    @property
    def rank(self) -> float:
        return self.__rank

    @rank.setter
    def rank(self, value: float):
        self.__rank = value
        self._property_changed('rank')        

    @property
    def filteredFields(self) -> Tuple[MarketDataFilteredField, ...]:
        return self.__filteredFields

    @filteredFields.setter
    def filteredFields(self, value: Tuple[MarketDataFilteredField, ...]):
        self.__filteredFields = value
        self._property_changed('filteredFields')        

    @property
    def assetTypes(self) -> Tuple[Union[AssetType, str], ...]:
        """Asset type differentiates the product categorization or contract type"""
        return self.__assetTypes

    @assetTypes.setter
    def assetTypes(self, value: Tuple[Union[AssetType, str], ...]):
        self.__assetTypes = value
        self._property_changed('assetTypes')        

    @property
    def entityType(self) -> Union[MeasureEntityType, str]:
        """Entity type associated with a measure."""
        return self.__entityType

    @entityType.setter
    def entityType(self, value: Union[MeasureEntityType, str]):
        self.__entityType = value if isinstance(value, MeasureEntityType) else get_enum_value(MeasureEntityType, value)
        self._property_changed('entityType')        

    @property
    def backtestEntity(self) -> MeasureBacktest:
        """Describes backtests that should be associated with a measure."""
        return self.__backtestEntity

    @backtestEntity.setter
    def backtestEntity(self, value: MeasureBacktest):
        self.__backtestEntity = value
        self._property_changed('backtestEntity')        

    @property
    def kpiEntity(self) -> MeasureKpi:
        """Describes KPIs that should be associated with a measure."""
        return self.__kpiEntity

    @kpiEntity.setter
    def kpiEntity(self, value: MeasureKpi):
        self.__kpiEntity = value
        self._property_changed('kpiEntity')        


class ProcessorEntity(Base):
        
    """Query processors for dataset."""
       
    def __init__(self, filters: Tuple[str, ...] = None, parsers: Tuple[ParserEntity, ...] = None, deduplicate: Tuple[str, ...] = None):
        super().__init__()
        self.__filters = filters
        self.__parsers = parsers
        self.__deduplicate = deduplicate

    @property
    def filters(self) -> Tuple[str, ...]:
        """List of filter processors."""
        return self.__filters

    @filters.setter
    def filters(self, value: Tuple[str, ...]):
        self.__filters = value
        self._property_changed('filters')        

    @property
    def parsers(self) -> Tuple[ParserEntity, ...]:
        """List of parser processors."""
        return self.__parsers

    @parsers.setter
    def parsers(self, value: Tuple[ParserEntity, ...]):
        self.__parsers = value
        self._property_changed('parsers')        

    @property
    def deduplicate(self) -> Tuple[str, ...]:
        """Columns on which a deduplication processor should be run."""
        return self.__deduplicate

    @deduplicate.setter
    def deduplicate(self, value: Tuple[str, ...]):
        self.__deduplicate = value
        self._property_changed('deduplicate')        


class EntityFilter(Base):
        
    """Filter on entities."""
       
    def __init__(self, operator: str = None, simpleFilters: Tuple[DataFilter, ...] = None, complexFilters: Tuple[ComplexFilter, ...] = None):
        super().__init__()
        self.__operator = operator
        self.__simpleFilters = simpleFilters
        self.__complexFilters = complexFilters

    @property
    def operator(self) -> str:
        return self.__operator

    @operator.setter
    def operator(self, value: str):
        self.__operator = value
        self._property_changed('operator')        

    @property
    def simpleFilters(self) -> Tuple[DataFilter, ...]:
        """Filter on specified field."""
        return self.__simpleFilters

    @simpleFilters.setter
    def simpleFilters(self, value: Tuple[DataFilter, ...]):
        self.__simpleFilters = value
        self._property_changed('simpleFilters')        

    @property
    def complexFilters(self) -> Tuple[ComplexFilter, ...]:
        """A compound filter for data requests."""
        return self.__complexFilters

    @complexFilters.setter
    def complexFilters(self, value: Tuple[ComplexFilter, ...]):
        self.__complexFilters = value
        self._property_changed('complexFilters')        


class DataSetFilters(Base):
        
    """Filters to restrict the set of data returned."""
       
    def __init__(self, entityFilter: EntityFilter = None, rowFilters: Tuple[DataFilter, ...] = None, advancedFilters: Tuple[AdvancedFilter, ...] = None, historyFilter: HistoryFilter = None):
        super().__init__()
        self.__entityFilter = entityFilter
        self.__rowFilters = rowFilters
        self.__advancedFilters = advancedFilters
        self.__historyFilter = historyFilter

    @property
    def entityFilter(self) -> EntityFilter:
        """Filter on entities."""
        return self.__entityFilter

    @entityFilter.setter
    def entityFilter(self, value: EntityFilter):
        self.__entityFilter = value
        self._property_changed('entityFilter')        

    @property
    def rowFilters(self) -> Tuple[DataFilter, ...]:
        """Filters on database rows."""
        return self.__rowFilters

    @rowFilters.setter
    def rowFilters(self, value: Tuple[DataFilter, ...]):
        self.__rowFilters = value
        self._property_changed('rowFilters')        

    @property
    def advancedFilters(self) -> Tuple[AdvancedFilter, ...]:
        """Advanced filter for numeric fields."""
        return self.__advancedFilters

    @advancedFilters.setter
    def advancedFilters(self, value: Tuple[AdvancedFilter, ...]):
        self.__advancedFilters = value
        self._property_changed('advancedFilters')        

    @property
    def historyFilter(self) -> HistoryFilter:
        """Restricts queries against dataset to an absolute or relative range."""
        return self.__historyFilter

    @historyFilter.setter
    def historyFilter(self, value: HistoryFilter):
        self.__historyFilter = value
        self._property_changed('historyFilter')        


class DataSetEntity(Base):
               
    def __init__(self, id: str, name: str, description: str, shortDescription: str, vendor: str, dataProduct: str, parameters: DataSetParameters, dimensions: DataSetDimensions, ownerId: str = None, mappings: Tuple[MarketDataMapping, ...] = None, startDate: datetime.date = None, mdapi: MDAPI = None, entitlements: Entitlements = None, entitlementExclusions: EntitlementExclusions = None, queryProcessors: ProcessorEntity = None, defaults: DataSetDefaults = None, filters: DataSetFilters = None, createdById: str = None, createdTime: datetime.datetime = None, lastUpdatedById: str = None, lastUpdatedTime: datetime.datetime = None, tags: Tuple[str, ...] = None):
        super().__init__()
        self.__ownerId = ownerId
        self.__id = id
        self.__name = name
        self.__description = description
        self.__shortDescription = shortDescription
        self.__mappings = mappings
        self.__vendor = vendor
        self.__startDate = startDate
        self.__mdapi = mdapi
        self.__dataProduct = dataProduct
        self.__entitlements = entitlements
        self.__entitlementExclusions = entitlementExclusions
        self.__queryProcessors = queryProcessors
        self.__parameters = parameters
        self.__dimensions = dimensions
        self.__defaults = defaults
        self.__filters = filters
        self.__createdById = createdById
        self.__createdTime = createdTime
        self.__lastUpdatedById = lastUpdatedById
        self.__lastUpdatedTime = lastUpdatedTime
        self.__tags = tags

    @property
    def ownerId(self) -> str:
        """Marquee unique identifier for user who owns the object."""
        return self.__ownerId

    @ownerId.setter
    def ownerId(self, value: str):
        self.__ownerId = value
        self._property_changed('ownerId')        

    @property
    def id(self) -> str:
        """Unique id of dataset."""
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value
        self._property_changed('id')        

    @property
    def name(self) -> str:
        """Name of dataset."""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def description(self) -> str:
        """Description of dataset."""
        return self.__description

    @description.setter
    def description(self, value: str):
        self.__description = value
        self._property_changed('description')        

    @property
    def shortDescription(self) -> str:
        """Short description of dataset."""
        return self.__shortDescription

    @shortDescription.setter
    def shortDescription(self, value: str):
        self.__shortDescription = value
        self._property_changed('shortDescription')        

    @property
    def mappings(self) -> Tuple[MarketDataMapping, ...]:
        """Market data mappings."""
        return self.__mappings

    @mappings.setter
    def mappings(self, value: Tuple[MarketDataMapping, ...]):
        self.__mappings = value
        self._property_changed('mappings')        

    @property
    def vendor(self) -> str:
        return self.__vendor

    @vendor.setter
    def vendor(self, value: str):
        self.__vendor = value
        self._property_changed('vendor')        

    @property
    def startDate(self) -> datetime.date:
        """The start of this data set"""
        return self.__startDate

    @startDate.setter
    def startDate(self, value: datetime.date):
        self.__startDate = value
        self._property_changed('startDate')        

    @property
    def mdapi(self) -> MDAPI:
        """Defines MDAPI fields."""
        return self.__mdapi

    @mdapi.setter
    def mdapi(self, value: MDAPI):
        self.__mdapi = value
        self._property_changed('mdapi')        

    @property
    def dataProduct(self) -> str:
        """Product that dataset belongs to."""
        return self.__dataProduct

    @dataProduct.setter
    def dataProduct(self, value: str):
        self.__dataProduct = value
        self._property_changed('dataProduct')        

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
    def queryProcessors(self) -> ProcessorEntity:
        """Query processors for dataset."""
        return self.__queryProcessors

    @queryProcessors.setter
    def queryProcessors(self, value: ProcessorEntity):
        self.__queryProcessors = value
        self._property_changed('queryProcessors')        

    @property
    def parameters(self) -> DataSetParameters:
        """Dataset parameters."""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: DataSetParameters):
        self.__parameters = value
        self._property_changed('parameters')        

    @property
    def dimensions(self) -> DataSetDimensions:
        """Dataset dimensions."""
        return self.__dimensions

    @dimensions.setter
    def dimensions(self, value: DataSetDimensions):
        self.__dimensions = value
        self._property_changed('dimensions')        

    @property
    def defaults(self) -> DataSetDefaults:
        """Default settings."""
        return self.__defaults

    @defaults.setter
    def defaults(self, value: DataSetDefaults):
        self.__defaults = value
        self._property_changed('defaults')        

    @property
    def filters(self) -> DataSetFilters:
        """Filters to restrict the set of data returned."""
        return self.__filters

    @filters.setter
    def filters(self, value: DataSetFilters):
        self.__filters = value
        self._property_changed('filters')        

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
    def tags(self) -> Tuple[str, ...]:
        """Tags associated with dataset."""
        return self.__tags

    @tags.setter
    def tags(self, value: Tuple[str, ...]):
        self.__tags = value
        self._property_changed('tags')        
