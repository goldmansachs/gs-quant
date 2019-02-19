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
from gs_quant.base import Base


class DataSetEntity(Base):
               
    def __init__(self, id: Union[str, str], name: str, description: str, shortDescription: str, vendor: str, dataProduct: str, parameters: Union['DataSetParameters', str], dimensions: Union['DataSetDimensions', str], ownerId: Union[str, str] = None, startDate: Union[datetime.date, str] = None, mdapi: Union['MDAPI', str] = None, entitlements: Union['Entitlements', str] = None, queryProcessors: Union['ProcessorEntity', str] = None, defaults: Union['DataSetDefaults', str] = None, filters: Union['DataSetFilters', str] = None, createdById: Union[str, str] = None, createdTime: Union[datetime.datetime, str] = None, lastUpdatedById: Union[str, str] = None, lastUpdatedTime: Union[datetime.datetime, str] = None, tags: Iterable[str] = None):
        super().__init__()
        self.__ownerId = ownerId
        self.__id = id
        self.__name = name
        self.__description = description
        self.__shortDescription = shortDescription
        self.__vendor = vendor
        self.__startDate = startDate
        self.__mdapi = mdapi
        self.__dataProduct = dataProduct
        self.__entitlements = entitlements
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
    def ownerId(self) -> Union[str, str]:
        """Marquee unique identifier for user who owns the object."""
        return self.__ownerId

    @ownerId.setter
    def ownerId(self, value: Union[str, str]):
        self.__ownerId = value
        self._property_changed('ownerId')        

    @property
    def id(self) -> Union[str, str]:
        """Unique id of dataset."""
        return self.__id

    @id.setter
    def id(self, value: Union[str, str]):
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
    def vendor(self) -> str:
        return self.__vendor

    @vendor.setter
    def vendor(self, value: str):
        self.__vendor = value
        self._property_changed('vendor')        

    @property
    def startDate(self) -> Union[datetime.date, str]:
        """The start of this data set"""
        return self.__startDate

    @startDate.setter
    def startDate(self, value: Union[datetime.date, str]):
        self.__startDate = value
        self._property_changed('startDate')        

    @property
    def mdapi(self) -> Union['MDAPI', str]:
        """Defines MDAPI fields."""
        return self.__mdapi

    @mdapi.setter
    def mdapi(self, value: Union['MDAPI', str]):
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
    def entitlements(self) -> Union['Entitlements', str]:
        """Defines the entitlements of a given resource"""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Union['Entitlements', str]):
        self.__entitlements = value
        self._property_changed('entitlements')        

    @property
    def queryProcessors(self) -> Union['ProcessorEntity', str]:
        """Query processors for dataset."""
        return self.__queryProcessors

    @queryProcessors.setter
    def queryProcessors(self, value: Union['ProcessorEntity', str]):
        self.__queryProcessors = value
        self._property_changed('queryProcessors')        

    @property
    def parameters(self) -> Union['DataSetParameters', str]:
        """Dataset parameters."""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: Union['DataSetParameters', str]):
        self.__parameters = value
        self._property_changed('parameters')        

    @property
    def dimensions(self) -> Union['DataSetDimensions', str]:
        """Dataset dimensions."""
        return self.__dimensions

    @dimensions.setter
    def dimensions(self, value: Union['DataSetDimensions', str]):
        self.__dimensions = value
        self._property_changed('dimensions')        

    @property
    def defaults(self) -> Union['DataSetDefaults', str]:
        """Default settings."""
        return self.__defaults

    @defaults.setter
    def defaults(self, value: Union['DataSetDefaults', str]):
        self.__defaults = value
        self._property_changed('defaults')        

    @property
    def filters(self) -> Union['DataSetFilters', str]:
        """Filters to restrict the set of data returned."""
        return self.__filters

    @filters.setter
    def filters(self, value: Union['DataSetFilters', str]):
        self.__filters = value
        self._property_changed('filters')        

    @property
    def createdById(self) -> Union[str, str]:
        """Unique identifier of user who created the object"""
        return self.__createdById

    @createdById.setter
    def createdById(self, value: Union[str, str]):
        self.__createdById = value
        self._property_changed('createdById')        

    @property
    def createdTime(self) -> Union[datetime.datetime, str]:
        """Time created. ISO 8601 formatted string"""
        return self.__createdTime

    @createdTime.setter
    def createdTime(self, value: Union[datetime.datetime, str]):
        self.__createdTime = value
        self._property_changed('createdTime')        

    @property
    def lastUpdatedById(self) -> Union[str, str]:
        """Unique identifier of user who last updated the object"""
        return self.__lastUpdatedById

    @lastUpdatedById.setter
    def lastUpdatedById(self, value: Union[str, str]):
        self.__lastUpdatedById = value
        self._property_changed('lastUpdatedById')        

    @property
    def lastUpdatedTime(self) -> Union[datetime.datetime, str]:
        """Timestamp of when the object was last updated"""
        return self.__lastUpdatedTime

    @lastUpdatedTime.setter
    def lastUpdatedTime(self, value: Union[datetime.datetime, str]):
        self.__lastUpdatedTime = value
        self._property_changed('lastUpdatedTime')        

    @property
    def tags(self) -> Iterable[str]:
        """Tags associated with dataset."""
        return self.__tags

    @tags.setter
    def tags(self, value: Iterable[str]):
        self.__tags = value
        self._property_changed('tags')        


class DataSetFilters(Base):
        
    """Filters to restrict the set of data returned."""
       
    def __init__(self, entityFilter: Union['EntityFilter', str] = None, rowFilters: Iterable['DataFilter'] = None, advancedFilters: Iterable['AdvancedFilter'] = None, historyFilter: Union['HistoryFilter', str] = None):
        super().__init__()
        self.__entityFilter = entityFilter
        self.__rowFilters = rowFilters
        self.__advancedFilters = advancedFilters
        self.__historyFilter = historyFilter

    @property
    def entityFilter(self) -> Union['EntityFilter', str]:
        """Filter on entities."""
        return self.__entityFilter

    @entityFilter.setter
    def entityFilter(self, value: Union['EntityFilter', str]):
        self.__entityFilter = value
        self._property_changed('entityFilter')        

    @property
    def rowFilters(self) -> Iterable['DataFilter']:
        """Filters on database rows."""
        return self.__rowFilters

    @rowFilters.setter
    def rowFilters(self, value: Iterable['DataFilter']):
        self.__rowFilters = value
        self._property_changed('rowFilters')        

    @property
    def advancedFilters(self) -> Iterable['AdvancedFilter']:
        return self.__advancedFilters

    @advancedFilters.setter
    def advancedFilters(self, value: Iterable['AdvancedFilter']):
        self.__advancedFilters = value
        self._property_changed('advancedFilters')        

    @property
    def historyFilter(self) -> Union['HistoryFilter', str]:
        """Restricts queries against dataset to an absolute or relative range."""
        return self.__historyFilter

    @historyFilter.setter
    def historyFilter(self, value: Union['HistoryFilter', str]):
        self.__historyFilter = value
        self._property_changed('historyFilter')        


class HistoryFilter(Base):
        
    """Restricts queries against dataset to an absolute or relative range."""
       
    def __init__(self, absoluteStart: Union[datetime.datetime, str] = None, absoluteEnd: Union[datetime.datetime, str] = None, relativeStartSeconds: float = None, relativeEndSeconds: float = None):
        super().__init__()
        self.__absoluteStart = absoluteStart
        self.__absoluteEnd = absoluteEnd
        self.__relativeStartSeconds = relativeStartSeconds
        self.__relativeEndSeconds = relativeEndSeconds

    @property
    def absoluteStart(self) -> Union[datetime.datetime, str]:
        """ISO 8601-formatted timestamp"""
        return self.__absoluteStart

    @absoluteStart.setter
    def absoluteStart(self, value: Union[datetime.datetime, str]):
        self.__absoluteStart = value
        self._property_changed('absoluteStart')        

    @property
    def absoluteEnd(self) -> Union[datetime.datetime, str]:
        """ISO 8601-formatted timestamp"""
        return self.__absoluteEnd

    @absoluteEnd.setter
    def absoluteEnd(self, value: Union[datetime.datetime, str]):
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
       
    def __init__(self, field: str, values: Iterable[str], column: Union[str, str] = None):
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
    def column(self) -> Union[str, str]:
        """Database column name."""
        return self.__column

    @column.setter
    def column(self, value: Union[str, str]):
        self.__column = value
        self._property_changed('column')        

    @property
    def values(self) -> Iterable[str]:
        """Value(s) to match."""
        return self.__values

    @values.setter
    def values(self, value: Iterable[str]):
        self.__values = value
        self._property_changed('values')        


class EntityFilter(Base):
        
    """Filter on entities."""
       
    def __init__(self, operator: str = None, simpleFilters: Iterable['DataFilter'] = None, complexFilters: Iterable['ComplexFilter'] = None):
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
    def simpleFilters(self) -> Iterable['DataFilter']:
        return self.__simpleFilters

    @simpleFilters.setter
    def simpleFilters(self, value: Iterable['DataFilter']):
        self.__simpleFilters = value
        self._property_changed('simpleFilters')        

    @property
    def complexFilters(self) -> Iterable['ComplexFilter']:
        return self.__complexFilters

    @complexFilters.setter
    def complexFilters(self, value: Iterable['ComplexFilter']):
        self.__complexFilters = value
        self._property_changed('complexFilters')        


class ComplexFilter(Base):
        
    """A compound filter for data requests."""
       
    def __init__(self, operator: str, simpleFilters: Iterable['DataFilter']):
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
    def simpleFilters(self) -> Iterable['DataFilter']:
        return self.__simpleFilters

    @simpleFilters.setter
    def simpleFilters(self, value: Iterable['DataFilter']):
        self.__simpleFilters = value
        self._property_changed('simpleFilters')        


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


class DataSetDimensions(Base):
        
    """Dataset dimensions."""
       
    def __init__(self, timeField: str, transactionTimeField: str = None, symbolDimensions: Iterable[str] = None, nonSymbolDimensions: Iterable['FieldColumnPair'] = None, keyDimensions: Iterable[str] = None, measures: Iterable['FieldColumnPair'] = None, entityDimension: str = None):
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
    def symbolDimensions(self) -> Iterable[str]:
        """Set of fields that determine database table name."""
        return self.__symbolDimensions

    @symbolDimensions.setter
    def symbolDimensions(self, value: Iterable[str]):
        self.__symbolDimensions = value
        self._property_changed('symbolDimensions')        

    @property
    def nonSymbolDimensions(self) -> Iterable['FieldColumnPair']:
        """Fields that are not nullable."""
        return self.__nonSymbolDimensions

    @nonSymbolDimensions.setter
    def nonSymbolDimensions(self, value: Iterable['FieldColumnPair']):
        self.__nonSymbolDimensions = value
        self._property_changed('nonSymbolDimensions')        

    @property
    def keyDimensions(self) -> Iterable[str]:
        return self.__keyDimensions

    @keyDimensions.setter
    def keyDimensions(self, value: Iterable[str]):
        self.__keyDimensions = value
        self._property_changed('keyDimensions')        

    @property
    def measures(self) -> Iterable['FieldColumnPair']:
        """Fields that are nullable."""
        return self.__measures

    @measures.setter
    def measures(self, value: Iterable['FieldColumnPair']):
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


class Adjustments(Base):
        
    """Corporate action adjustments."""
       
    def __init__(self, priceColumns: Iterable[str], adjustedSuffix: str):
        super().__init__()
        self.__priceColumns = priceColumns
        self.__adjustedSuffix = adjustedSuffix

    @property
    def priceColumns(self) -> Iterable[str]:
        return self.__priceColumns

    @priceColumns.setter
    def priceColumns(self, value: Iterable[str]):
        self.__priceColumns = value
        self._property_changed('priceColumns')        

    @property
    def adjustedSuffix(self) -> str:
        return self.__adjustedSuffix

    @adjustedSuffix.setter
    def adjustedSuffix(self, value: str):
        self.__adjustedSuffix = value
        self._property_changed('adjustedSuffix')        


class FieldColumnPair(Base):
        
    """Map from fields to database columns."""
       
    def __init__(self, field: str = None, column: Union[str, str] = None, fieldDescription: str = None):
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
    def column(self) -> Union[str, str]:
        """Database column name."""
        return self.__column

    @column.setter
    def column(self, value: Union[str, str]):
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


class DataSetParameters(Base):
        
    """Dataset parameters."""
       
    def __init__(self, uploadDataPolicy: str, logicalDb: str, symbolStrategy: str, applyMarketDataEntitlements: bool, coverage: str, frequency: str, methodology: str, history: str, category: str = None, subCategory: str = None, assetClass: Union['AssetClass', str] = None, ownerIds: Iterable[str] = None, approverIds: Iterable[str] = None, supportIds: Iterable[str] = None, identifierMapperName: str = None, constantSymbols: Iterable[str] = None, underlyingDataSetId: str = None, immutable: bool = None, includeInCatalog: bool = None, overrideQueryColumnIds: Iterable[str] = None):
        super().__init__()
        self.__category = category
        self.__subCategory = subCategory
        self.__methodology = methodology
        self.__coverage = coverage
        self.__history = history
        self.__frequency = frequency
        self.__assetClass = assetClass
        self.__ownerIds = ownerIds
        self.__approverIds = approverIds
        self.__supportIds = supportIds
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
    def assetClass(self) -> Union['AssetClass', str]:
        """Asset classification of security. Assets are classified into broad groups which exhibit similar characteristics and behave in a consistent way under different market conditions"""
        return self.__assetClass

    @assetClass.setter
    def assetClass(self, value: Union['AssetClass', str]):
        self.__assetClass = value
        self._property_changed('assetClass')        

    @property
    def ownerIds(self) -> Iterable[str]:
        """Users who own dataset."""
        return self.__ownerIds

    @ownerIds.setter
    def ownerIds(self, value: Iterable[str]):
        self.__ownerIds = value
        self._property_changed('ownerIds')        

    @property
    def approverIds(self) -> Iterable[str]:
        """Users who can grant access to dataset."""
        return self.__approverIds

    @approverIds.setter
    def approverIds(self, value: Iterable[str]):
        self.__approverIds = value
        self._property_changed('approverIds')        

    @property
    def supportIds(self) -> Iterable[str]:
        """Users who support dataset."""
        return self.__supportIds

    @supportIds.setter
    def supportIds(self, value: Iterable[str]):
        self.__supportIds = value
        self._property_changed('supportIds')        

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
    def constantSymbols(self) -> Iterable[str]:
        return self.__constantSymbols

    @constantSymbols.setter
    def constantSymbols(self, value: Iterable[str]):
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
    def overrideQueryColumnIds(self) -> Iterable[str]:
        """Explicit set of database columns to query for, regardless of fields specified in request."""
        return self.__overrideQueryColumnIds

    @overrideQueryColumnIds.setter
    def overrideQueryColumnIds(self, value: Iterable[str]):
        self.__overrideQueryColumnIds = value
        self._property_changed('overrideQueryColumnIds')        


class ProcessorEntity(Base):
        
    """Query processors for dataset."""
       
    def __init__(self, filters: Iterable[str] = None, parsers: Iterable['ParserEntity'] = None, deduplicate: Iterable[str] = None):
        super().__init__()
        self.__filters = filters
        self.__parsers = parsers
        self.__deduplicate = deduplicate

    @property
    def filters(self) -> Iterable[str]:
        """List of filter processors."""
        return self.__filters

    @filters.setter
    def filters(self, value: Iterable[str]):
        self.__filters = value
        self._property_changed('filters')        

    @property
    def parsers(self) -> Iterable['ParserEntity']:
        """List of parser processors."""
        return self.__parsers

    @parsers.setter
    def parsers(self, value: Iterable['ParserEntity']):
        self.__parsers = value
        self._property_changed('parsers')        

    @property
    def deduplicate(self) -> Iterable[str]:
        """Columns on which a deduplication processor should be run."""
        return self.__deduplicate

    @deduplicate.setter
    def deduplicate(self, value: Iterable[str]):
        self.__deduplicate = value
        self._property_changed('deduplicate')        


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


class MDAPI(Base):
        
    """Defines MDAPI fields."""
       
    def __init__(self, type: str, quotingStyles: Iterable[Any], class_: str = None):
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
    def quotingStyles(self) -> Iterable[Any]:
        """Map from MDAPI QuotingStyles to database columns"""
        return self.__quotingStyles

    @quotingStyles.setter
    def quotingStyles(self, value: Iterable[Any]):
        self.__quotingStyles = value
        self._property_changed('quotingStyles')        


class DataQueryResponse(Base):
               
    def __init__(self, requestId: Union[str, str] = None, data: Iterable['FieldValueMap'] = None, groups: Iterable['DataGroup'] = None):
        super().__init__()
        self.__requestId = requestId
        self.__data = data
        self.__groups = groups

    @property
    def requestId(self) -> Union[str, str]:
        """Marquee unique identifier"""
        return self.__requestId

    @requestId.setter
    def requestId(self, value: Union[str, str]):
        self.__requestId = value
        self._property_changed('requestId')        

    @property
    def data(self) -> Iterable['FieldValueMap']:
        """Array of data elements from dataset"""
        return self.__data

    @data.setter
    def data(self, value: Iterable['FieldValueMap']):
        self.__data = value
        self._property_changed('data')        

    @property
    def groups(self) -> Iterable['DataGroup']:
        """If the data is requested in grouped mode, will return data group object"""
        return self.__groups

    @groups.setter
    def groups(self, value: Iterable['DataGroup']):
        self.__groups = value
        self._property_changed('groups')        


class DataGroup(Base):
        
    """Dataset grouped by context (key dimensions)"""
       
    def __init__(self, context: Union['FieldValueMap', str] = None, data: Iterable['FieldValueMap'] = None):
        super().__init__()
        self.__context = context
        self.__data = data

    @property
    def context(self) -> Union['FieldValueMap', str]:
        """Context map for the grouped data (key dimensions)"""
        return self.__context

    @context.setter
    def context(self, value: Union['FieldValueMap', str]):
        self.__context = value
        self._property_changed('context')        

    @property
    def data(self) -> Iterable['FieldValueMap']:
        """Array of grouped data objects"""
        return self.__data

    @data.setter
    def data(self, value: Iterable['FieldValueMap']):
        self.__data = value
        self._property_changed('data')        


class DataQuery(Base):
               
    def __init__(self, id: Union[str, str] = None, dataSetId: Union[str, str] = None, format: Union['Format', str] = None, marketDataCoordinates: Iterable['MarketDataCoordinate'] = None, where: Union['FieldFilterMap', str] = None, vendor: str = None, startDate: Union[datetime.date, str] = None, endDate: Union[datetime.date, str] = None, startTime: Union[datetime.datetime, str] = None, endTime: Union[datetime.datetime, str] = None, asOfTime: Union[datetime.datetime, str] = None, idAsOfDate: Union[datetime.date, str] = None, since: Union[datetime.datetime, str] = None, dates=None, times=None, delay: int = None, intervals: int = None, pollingInterval: int = None, groupBy: Iterable['Field'] = None, grouped: bool = None, fields: Iterable['Selector'] = None):
        super().__init__()
        self.__id = id
        self.__dataSetId = dataSetId
        self.__format = format
        self.__marketDataCoordinates = marketDataCoordinates
        self.__where = where
        self.__vendor = vendor
        self.__startDate = startDate
        self.__endDate = endDate
        self.__startTime = startTime
        self.__endTime = endTime
        self.__asOfTime = asOfTime
        self.__idAsOfDate = idAsOfDate
        self.__since = since
        self.__dates = dates
        self.__times = times
        self.__delay = delay
        self.__intervals = intervals
        self.__pollingInterval = pollingInterval
        self.__groupBy = groupBy
        self.__grouped = grouped
        self.__fields = fields

    @property
    def id(self) -> Union[str, str]:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: Union[str, str]):
        self.__id = value
        self._property_changed('id')        

    @property
    def dataSetId(self) -> Union[str, str]:
        """Marquee unique identifier"""
        return self.__dataSetId

    @dataSetId.setter
    def dataSetId(self, value: Union[str, str]):
        self.__dataSetId = value
        self._property_changed('dataSetId')        

    @property
    def format(self) -> Union['Format', str]:
        """Alternative format for data to be returned in"""
        return self.__format

    @format.setter
    def format(self, value: Union['Format', str]):
        self.__format = value
        self._property_changed('format')        

    @property
    def marketDataCoordinates(self) -> Iterable['MarketDataCoordinate']:
        return self.__marketDataCoordinates

    @marketDataCoordinates.setter
    def marketDataCoordinates(self, value: Iterable['MarketDataCoordinate']):
        self.__marketDataCoordinates = value
        self._property_changed('marketDataCoordinates')        

    @property
    def where(self) -> Union['FieldFilterMap', str]:
        """Filters on data fields."""
        return self.__where

    @where.setter
    def where(self, value: Union['FieldFilterMap', str]):
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
    def startDate(self) -> Union[datetime.date, str]:
        """ISO 8601-formatted date"""
        return self.__startDate

    @startDate.setter
    def startDate(self, value: Union[datetime.date, str]):
        self.__startDate = value
        self._property_changed('startDate')        

    @property
    def endDate(self) -> Union[datetime.date, str]:
        """ISO 8601-formatted date"""
        return self.__endDate

    @endDate.setter
    def endDate(self, value: Union[datetime.date, str]):
        self.__endDate = value
        self._property_changed('endDate')        

    @property
    def startTime(self) -> Union[datetime.datetime, str]:
        """ISO 8601-formatted timestamp"""
        return self.__startTime

    @startTime.setter
    def startTime(self, value: Union[datetime.datetime, str]):
        self.__startTime = value
        self._property_changed('startTime')        

    @property
    def endTime(self) -> Union[datetime.datetime, str]:
        """ISO 8601-formatted timestamp"""
        return self.__endTime

    @endTime.setter
    def endTime(self, value: Union[datetime.datetime, str]):
        self.__endTime = value
        self._property_changed('endTime')        

    @property
    def asOfTime(self) -> Union[datetime.datetime, str]:
        """ISO 8601-formatted timestamp"""
        return self.__asOfTime

    @asOfTime.setter
    def asOfTime(self, value: Union[datetime.datetime, str]):
        self.__asOfTime = value
        self._property_changed('asOfTime')        

    @property
    def idAsOfDate(self) -> Union[datetime.date, str]:
        """ISO 8601-formatted date"""
        return self.__idAsOfDate

    @idAsOfDate.setter
    def idAsOfDate(self, value: Union[datetime.date, str]):
        self.__idAsOfDate = value
        self._property_changed('idAsOfDate')        

    @property
    def since(self) -> Union[datetime.datetime, str]:
        """ISO 8601-formatted timestamp"""
        return self.__since

    @since.setter
    def since(self, value: Union[datetime.datetime, str]):
        self.__since = value
        self._property_changed('since')        

    @property
    def dates(self):
        """Select and return specific dates from dataset query results."""
        return self.__dates

    @dates.setter
    def dates(self, value):
        self.__dates = value
        self._property_changed('dates')        

    @property
    def times(self):
        """Select and return specific times from dataset query results."""
        return self.__times

    @times.setter
    def times(self, value):
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
    def groupBy(self) -> Iterable['Field']:
        """Fields that determine grouping of results. Defaults to the dimensions of the dataset."""
        return self.__groupBy

    @groupBy.setter
    def groupBy(self, value: Iterable['Field']):
        self.__groupBy = value
        self._property_changed('groupBy')        

    @property
    def grouped(self) -> bool:
        """Set to true to return results grouped by a given context (set of dimensions)."""
        return self.__grouped

    @grouped.setter
    def grouped(self, value: bool):
        self.__grouped = value
        self._property_changed('grouped')        

    @property
    def fields(self) -> Iterable['Selector']:
        """Fields to be returned."""
        return self.__fields

    @fields.setter
    def fields(self, value: Iterable['Selector']):
        self.__fields = value
        self._property_changed('fields')        
