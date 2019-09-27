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
       
    def __init__(
        self,
        column: str,
        value: float,
        operator: str        
    ):
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
       
    def __init__(
        self,
        field: str,
        values: Tuple[str, ...],
        column: str = None        
    ):
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
       
    def __init__(
        self,
                
    ):
        super().__init__()
        


class DataQuery(Base):
               
    def __init__(
        self,
        id: str = None,
        data_set_id: str = None,
        format: Union[Format, str] = None,
        market_data_coordinates: Tuple[MarketDataCoordinate, ...] = None,
        where: FieldFilterMap = None,
        vendor: str = None,
        start_date: datetime.date = None,
        end_date: datetime.date = None,
        start_time: datetime.datetime = None,
        end_time: datetime.datetime = None,
        as_of_time: datetime.datetime = None,
        id_as_of_date: datetime.date = None,
        use_temporal_x_ref: bool = False,
        since: datetime.datetime = None,
        dates: Tuple[datetime.date, ...] = None,
        times: Tuple[datetime.datetime, ...] = None,
        delay: int = None,
        intervals: int = None,
        samples: int = None,
        limit: int = None,
        polling_interval: int = None,
        grouped: bool = None,
        fields: Tuple[Union[dict, str], ...] = None,
        restrict_fields: bool = False        
    ):
        super().__init__()
        self.__id = id
        self.__data_set_id = data_set_id
        self.__format = get_enum_value(Format, format)
        self.__market_data_coordinates = market_data_coordinates
        self.__where = where
        self.__vendor = vendor
        self.__start_date = start_date
        self.__end_date = end_date
        self.__start_time = start_time
        self.__end_time = end_time
        self.__as_of_time = as_of_time
        self.__id_as_of_date = id_as_of_date
        self.__use_temporal_x_ref = use_temporal_x_ref
        self.__since = since
        self.__dates = dates
        self.__times = times
        self.__delay = delay
        self.__intervals = intervals
        self.__samples = samples
        self.__limit = limit
        self.__polling_interval = polling_interval
        self.__grouped = grouped
        self.__fields = fields
        self.__restrict_fields = restrict_fields

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value
        self._property_changed('id')        

    @property
    def data_set_id(self) -> str:
        """Marquee unique identifier"""
        return self.__data_set_id

    @data_set_id.setter
    def data_set_id(self, value: str):
        self.__data_set_id = value
        self._property_changed('data_set_id')        

    @property
    def format(self) -> Union[Format, str]:
        """Alternative format for data to be returned in"""
        return self.__format

    @format.setter
    def format(self, value: Union[Format, str]):
        self.__format = value if isinstance(value, Format) else get_enum_value(Format, value)
        self._property_changed('format')        

    @property
    def market_data_coordinates(self) -> Tuple[MarketDataCoordinate, ...]:
        """Object representation of a market data coordinate"""
        return self.__market_data_coordinates

    @market_data_coordinates.setter
    def market_data_coordinates(self, value: Tuple[MarketDataCoordinate, ...]):
        self.__market_data_coordinates = value
        self._property_changed('market_data_coordinates')        

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
    def start_time(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__start_time

    @start_time.setter
    def start_time(self, value: datetime.datetime):
        self.__start_time = value
        self._property_changed('start_time')        

    @property
    def end_time(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__end_time

    @end_time.setter
    def end_time(self, value: datetime.datetime):
        self.__end_time = value
        self._property_changed('end_time')        

    @property
    def as_of_time(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__as_of_time

    @as_of_time.setter
    def as_of_time(self, value: datetime.datetime):
        self.__as_of_time = value
        self._property_changed('as_of_time')        

    @property
    def id_as_of_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__id_as_of_date

    @id_as_of_date.setter
    def id_as_of_date(self, value: datetime.date):
        self.__id_as_of_date = value
        self._property_changed('id_as_of_date')        

    @property
    def use_temporal_x_ref(self) -> bool:
        """Set to true when xrefs provided in the query should be treated in a temporal way (e.g. get data points which had a certain BCID at some point in time, not which currently have it)."""
        return self.__use_temporal_x_ref

    @use_temporal_x_ref.setter
    def use_temporal_x_ref(self, value: bool):
        self.__use_temporal_x_ref = value
        self._property_changed('use_temporal_x_ref')        

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
    def samples(self) -> int:
        """Number of points to down sample the data, for example if 10, it will return at most 10 sample data points evenly spaced over the time/date range"""
        return self.__samples

    @samples.setter
    def samples(self, value: int):
        self.__samples = value
        self._property_changed('samples')        

    @property
    def limit(self) -> int:
        """Maximum number of rows for each asset to return."""
        return self.__limit

    @limit.setter
    def limit(self, value: int):
        self.__limit = value
        self._property_changed('limit')        

    @property
    def polling_interval(self) -> int:
        """When streaming, wait for this number of seconds between poll attempts."""
        return self.__polling_interval

    @polling_interval.setter
    def polling_interval(self, value: int):
        self.__polling_interval = value
        self._property_changed('polling_interval')        

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

    @property
    def restrict_fields(self) -> bool:
        """Whether to return only the fields which are requested and suppress every other field"""
        return self.__restrict_fields

    @restrict_fields.setter
    def restrict_fields(self, value: bool):
        self.__restrict_fields = value
        self._property_changed('restrict_fields')        


class DataSetDefaults(Base):
        
    """Default settings."""
       
    def __init__(
        self,
        start_seconds: float = None,
        end_seconds: float = None,
        delay_seconds: float = None        
    ):
        super().__init__()
        self.__start_seconds = start_seconds
        self.__end_seconds = end_seconds
        self.__delay_seconds = delay_seconds

    @property
    def start_seconds(self) -> float:
        """Default start date/time, in seconds before current time."""
        return self.__start_seconds

    @start_seconds.setter
    def start_seconds(self, value: float):
        self.__start_seconds = value
        self._property_changed('start_seconds')        

    @property
    def end_seconds(self) -> float:
        """Default end date/time, in seconds before current time."""
        return self.__end_seconds

    @end_seconds.setter
    def end_seconds(self, value: float):
        self.__end_seconds = value
        self._property_changed('end_seconds')        

    @property
    def delay_seconds(self) -> float:
        """Default market delay to apply, in seconds."""
        return self.__delay_seconds

    @delay_seconds.setter
    def delay_seconds(self, value: float):
        self.__delay_seconds = value
        self._property_changed('delay_seconds')        


class DataSetDelay(Base):
        
    """Specifies the delayed data properties."""
       
    def __init__(
        self,
        until_seconds: float,
        at_time_zone: str,
        history_up_to_seconds: float = None,
        history_up_to_time: datetime.datetime = None        
    ):
        super().__init__()
        self.__until_seconds = until_seconds
        self.__at_time_zone = at_time_zone
        self.__history_up_to_seconds = history_up_to_seconds
        self.__history_up_to_time = history_up_to_time

    @property
    def until_seconds(self) -> float:
        """Seconds from midnight until which the delay will be applicable."""
        return self.__until_seconds

    @until_seconds.setter
    def until_seconds(self, value: float):
        self.__until_seconds = value
        self._property_changed('until_seconds')        

    @property
    def at_time_zone(self) -> str:
        """The time zone with respect to which the delay will be applied (must be a valid IANA TimeZone identifier)."""
        return self.__at_time_zone

    @at_time_zone.setter
    def at_time_zone(self, value: str):
        self.__at_time_zone = value
        self._property_changed('at_time_zone')        

    @property
    def history_up_to_seconds(self) -> float:
        """Relative seconds up to which the data history will be shown for the business day."""
        return self.__history_up_to_seconds

    @history_up_to_seconds.setter
    def history_up_to_seconds(self, value: float):
        self.__history_up_to_seconds = value
        self._property_changed('history_up_to_seconds')        

    @property
    def history_up_to_time(self) -> datetime.datetime:
        """Absolute time up to which the data history will be shown for the business day."""
        return self.__history_up_to_time

    @history_up_to_time.setter
    def history_up_to_time(self, value: datetime.datetime):
        self.__history_up_to_time = value
        self._property_changed('history_up_to_time')        


class DataSetParameters(Base):
        
    """Dataset parameters."""
       
    def __init__(
        self,
        upload_data_policy: str,
        logical_db: str,
        symbol_strategy: str,
        apply_market_data_entitlements: bool,
        coverage: str,
        frequency: str,
        methodology: str,
        history: str,
        category: str = None,
        sub_category: str = None,
        sample_start: datetime.datetime = None,
        sample_end: datetime.datetime = None,
        published_date: datetime.datetime = None,
        history_date: datetime.datetime = None,
        asset_class: Union[AssetClass, str] = None,
        owner_ids: Tuple[str, ...] = None,
        approver_ids: Tuple[str, ...] = None,
        support_ids: Tuple[str, ...] = None,
        support_distribution_list: Tuple[str, ...] = None,
        identifier_mapper_name: str = None,
        constant_symbols: Tuple[str, ...] = None,
        underlying_data_set_id: str = None,
        immutable: bool = None,
        include_in_catalog: bool = False,
        override_query_column_ids: Tuple[str, ...] = None,
        plot: bool = None,
        coverage_enabled: bool = True        
    ):
        super().__init__()
        self.__category = category
        self.__sub_category = sub_category
        self.__methodology = methodology
        self.__coverage = coverage
        self.__history = history
        self.__sample_start = sample_start
        self.__sample_end = sample_end
        self.__published_date = published_date
        self.__history_date = history_date
        self.__frequency = frequency
        self.__asset_class = get_enum_value(AssetClass, asset_class)
        self.__owner_ids = owner_ids
        self.__approver_ids = approver_ids
        self.__support_ids = support_ids
        self.__support_distribution_list = support_distribution_list
        self.__apply_market_data_entitlements = apply_market_data_entitlements
        self.__upload_data_policy = upload_data_policy
        self.__identifier_mapper_name = identifier_mapper_name
        self.__logical_db = logical_db
        self.__symbol_strategy = symbol_strategy
        self.__constant_symbols = constant_symbols
        self.__underlying_data_set_id = underlying_data_set_id
        self.__immutable = immutable
        self.__include_in_catalog = include_in_catalog
        self.__override_query_column_ids = override_query_column_ids
        self.__plot = plot
        self.__coverage_enabled = coverage_enabled

    @property
    def category(self) -> str:
        """Top level grouping."""
        return self.__category

    @category.setter
    def category(self, value: str):
        self.__category = value
        self._property_changed('category')        

    @property
    def sub_category(self) -> str:
        """Second level grouping."""
        return self.__sub_category

    @sub_category.setter
    def sub_category(self, value: str):
        self.__sub_category = value
        self._property_changed('sub_category')        

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
    def sample_start(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__sample_start

    @sample_start.setter
    def sample_start(self, value: datetime.datetime):
        self.__sample_start = value
        self._property_changed('sample_start')        

    @property
    def sample_end(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__sample_end

    @sample_end.setter
    def sample_end(self, value: datetime.datetime):
        self.__sample_end = value
        self._property_changed('sample_end')        

    @property
    def published_date(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__published_date

    @published_date.setter
    def published_date(self, value: datetime.datetime):
        self.__published_date = value
        self._property_changed('published_date')        

    @property
    def history_date(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__history_date

    @history_date.setter
    def history_date(self, value: datetime.datetime):
        self.__history_date = value
        self._property_changed('history_date')        

    @property
    def frequency(self) -> str:
        """Frequency of updates to dataset."""
        return self.__frequency

    @frequency.setter
    def frequency(self, value: str):
        self.__frequency = value
        self._property_changed('frequency')        

    @property
    def asset_class(self) -> Union[AssetClass, str]:
        """Asset classification of security. Assets are classified into broad groups which exhibit similar characteristics and behave in a consistent way under different market conditions"""
        return self.__asset_class

    @asset_class.setter
    def asset_class(self, value: Union[AssetClass, str]):
        self.__asset_class = value if isinstance(value, AssetClass) else get_enum_value(AssetClass, value)
        self._property_changed('asset_class')        

    @property
    def owner_ids(self) -> Tuple[str, ...]:
        """Users who own dataset."""
        return self.__owner_ids

    @owner_ids.setter
    def owner_ids(self, value: Tuple[str, ...]):
        self.__owner_ids = value
        self._property_changed('owner_ids')        

    @property
    def approver_ids(self) -> Tuple[str, ...]:
        """Users who can grant access to dataset."""
        return self.__approver_ids

    @approver_ids.setter
    def approver_ids(self, value: Tuple[str, ...]):
        self.__approver_ids = value
        self._property_changed('approver_ids')        

    @property
    def support_ids(self) -> Tuple[str, ...]:
        """Users who support dataset."""
        return self.__support_ids

    @support_ids.setter
    def support_ids(self, value: Tuple[str, ...]):
        self.__support_ids = value
        self._property_changed('support_ids')        

    @property
    def support_distribution_list(self) -> Tuple[str, ...]:
        """Distribution list who support dataset."""
        return self.__support_distribution_list

    @support_distribution_list.setter
    def support_distribution_list(self, value: Tuple[str, ...]):
        self.__support_distribution_list = value
        self._property_changed('support_distribution_list')        

    @property
    def apply_market_data_entitlements(self) -> bool:
        """Whether market data entitlements are checked."""
        return self.__apply_market_data_entitlements

    @apply_market_data_entitlements.setter
    def apply_market_data_entitlements(self, value: bool):
        self.__apply_market_data_entitlements = value
        self._property_changed('apply_market_data_entitlements')        

    @property
    def upload_data_policy(self) -> str:
        """Policy governing uploads."""
        return self.__upload_data_policy

    @upload_data_policy.setter
    def upload_data_policy(self, value: str):
        self.__upload_data_policy = value
        self._property_changed('upload_data_policy')        

    @property
    def identifier_mapper_name(self) -> str:
        """Identifier mapper associated with dataset."""
        return self.__identifier_mapper_name

    @identifier_mapper_name.setter
    def identifier_mapper_name(self, value: str):
        self.__identifier_mapper_name = value
        self._property_changed('identifier_mapper_name')        

    @property
    def identifier_updater_name(self) -> str:
        """Identifier updater associated with dataset."""
        return 'REPORT_IDENTIFIER_UPDATER'        

    @property
    def logical_db(self) -> str:
        """Database where contents are (to be) stored."""
        return self.__logical_db

    @logical_db.setter
    def logical_db(self, value: str):
        self.__logical_db = value
        self._property_changed('logical_db')        

    @property
    def symbol_strategy(self) -> str:
        """Method for looking up database table name."""
        return self.__symbol_strategy

    @symbol_strategy.setter
    def symbol_strategy(self, value: str):
        self.__symbol_strategy = value
        self._property_changed('symbol_strategy')        

    @property
    def constant_symbols(self) -> Tuple[str, ...]:
        return self.__constant_symbols

    @constant_symbols.setter
    def constant_symbols(self, value: Tuple[str, ...]):
        self.__constant_symbols = value
        self._property_changed('constant_symbols')        

    @property
    def underlying_data_set_id(self) -> str:
        """Dataset on which this (virtual) dataset is based."""
        return self.__underlying_data_set_id

    @underlying_data_set_id.setter
    def underlying_data_set_id(self, value: str):
        self.__underlying_data_set_id = value
        self._property_changed('underlying_data_set_id')        

    @property
    def immutable(self) -> bool:
        """Whether dataset is immutable (i.e. not writable through data service)."""
        return self.__immutable

    @immutable.setter
    def immutable(self, value: bool):
        self.__immutable = value
        self._property_changed('immutable')        

    @property
    def include_in_catalog(self) -> bool:
        """Whether dataset should be in the catalog."""
        return self.__include_in_catalog

    @include_in_catalog.setter
    def include_in_catalog(self, value: bool):
        self.__include_in_catalog = value
        self._property_changed('include_in_catalog')        

    @property
    def override_query_column_ids(self) -> Tuple[str, ...]:
        """Explicit set of database columns to query for, regardless of fields specified in request."""
        return self.__override_query_column_ids

    @override_query_column_ids.setter
    def override_query_column_ids(self, value: Tuple[str, ...]):
        self.__override_query_column_ids = value
        self._property_changed('override_query_column_ids')        

    @property
    def plot(self) -> bool:
        """Whether dataset is intended for use in Plottool."""
        return self.__plot

    @plot.setter
    def plot(self, value: bool):
        self.__plot = value
        self._property_changed('plot')        

    @property
    def coverage_enabled(self) -> bool:
        """Whether coverage requests are available for the DataSet"""
        return self.__coverage_enabled

    @coverage_enabled.setter
    def coverage_enabled(self, value: bool):
        self.__coverage_enabled = value
        self._property_changed('coverage_enabled')        


class FieldLink(Base):
        
    """Link the dataset field to an entity to also fetch its fields."""
       
    def __init__(
        self,
        entity_identifier: str = None,
        prefix: str = None        
    ):
        super().__init__()
        self.__entity_identifier = entity_identifier
        self.__prefix = prefix

    @property
    def entity_type(self) -> str:
        """The type of the entity to lookup to."""
        return 'Asset'        

    @property
    def entity_identifier(self) -> str:
        """The identifier of the entity to link the dataset field to."""
        return self.__entity_identifier

    @entity_identifier.setter
    def entity_identifier(self, value: str):
        self.__entity_identifier = value
        self._property_changed('entity_identifier')        

    @property
    def prefix(self) -> str:
        """Prefix to put before the fields fetched from the linked entity (must be unique for each dataset field)."""
        return self.__prefix

    @prefix.setter
    def prefix(self, value: str):
        self.__prefix = value
        self._property_changed('prefix')        


class MDAPI(Base):
        
    """Defines MDAPI fields."""
       
    def __init__(
        self,
        type: str,
        quoting_styles: Tuple[dict, ...],
        class_: str = None        
    ):
        super().__init__()
        self.__class = class_
        self.__type = type
        self.__quoting_styles = quoting_styles

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
    def quoting_styles(self) -> Tuple[dict, ...]:
        """Map from MDAPI QuotingStyles to database columns"""
        return self.__quoting_styles

    @quoting_styles.setter
    def quoting_styles(self, value: Tuple[dict, ...]):
        self.__quoting_styles = value
        self._property_changed('quoting_styles')        


class MDAPIDataQueryResponse(Base):
               
    def __init__(
        self,
        data: Tuple[FieldValueMap, ...] = None        
    ):
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
               
    def __init__(
        self,
        name: str = None,
        mapping: str = None        
    ):
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
               
    def __init__(
        self,
        field: str = None,
        default_value: str = None,
        default_numerical_value: float = None,
        numerical_values: Tuple[float, ...] = None,
        values: Tuple[str, ...] = None        
    ):
        super().__init__()
        self.__field = field
        self.__default_value = default_value
        self.__default_numerical_value = default_numerical_value
        self.__numerical_values = numerical_values
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
    def default_value(self) -> str:
        """Default filtered field"""
        return self.__default_value

    @default_value.setter
    def default_value(self, value: str):
        self.__default_value = value
        self._property_changed('default_value')        

    @property
    def default_numerical_value(self) -> float:
        """Default numerical filtered field"""
        return self.__default_numerical_value

    @default_numerical_value.setter
    def default_numerical_value(self, value: float):
        self.__default_numerical_value = value
        self._property_changed('default_numerical_value')        

    @property
    def numerical_values(self) -> Tuple[float, ...]:
        """Array of numerical filtered fields"""
        return self.__numerical_values

    @numerical_values.setter
    def numerical_values(self, value: Tuple[float, ...]):
        self.__numerical_values = value
        self._property_changed('numerical_values')        

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
       
    def __init__(
        self,
                
    ):
        super().__init__()
        


class MeasureKpi(Base):
        
    """Describes KPIs that should be associated with a measure."""
       
    def __init__(
        self,
                
    ):
        super().__init__()
        


class MidPrice(Base):
        
    """Specification for a mid price column derived from bid and ask columns."""
       
    def __init__(
        self,
        bid_column: str = None,
        ask_column: str = None,
        mid_column: str = None        
    ):
        super().__init__()
        self.__bid_column = bid_column
        self.__ask_column = ask_column
        self.__mid_column = mid_column

    @property
    def bid_column(self) -> str:
        """Database column name."""
        return self.__bid_column

    @bid_column.setter
    def bid_column(self, value: str):
        self.__bid_column = value
        self._property_changed('bid_column')        

    @property
    def ask_column(self) -> str:
        """Database column name."""
        return self.__ask_column

    @ask_column.setter
    def ask_column(self, value: str):
        self.__ask_column = value
        self._property_changed('ask_column')        

    @property
    def mid_column(self) -> str:
        """Database column name."""
        return self.__mid_column

    @mid_column.setter
    def mid_column(self, value: str):
        self.__mid_column = value
        self._property_changed('mid_column')        


class ParserEntity(Base):
        
    """Settings for a parser processor"""
       
    def __init__(
        self,
        only_normalized_fields: bool = None,
        quotes: bool = None,
        trades: bool = None        
    ):
        super().__init__()
        self.__only_normalized_fields = only_normalized_fields
        self.__quotes = quotes
        self.__trades = trades

    @property
    def only_normalized_fields(self) -> bool:
        """Setting for onlyNormalizedFields."""
        return self.__only_normalized_fields

    @only_normalized_fields.setter
    def only_normalized_fields(self, value: bool):
        self.__only_normalized_fields = value
        self._property_changed('only_normalized_fields')        

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
       
    def __init__(
        self,
        operator: str,
        simple_filters: Tuple[DataFilter, ...]        
    ):
        super().__init__()
        self.__operator = operator
        self.__simple_filters = simple_filters

    @property
    def operator(self) -> str:
        return self.__operator

    @operator.setter
    def operator(self, value: str):
        self.__operator = value
        self._property_changed('operator')        

    @property
    def simple_filters(self) -> Tuple[DataFilter, ...]:
        """Filter on specified field."""
        return self.__simple_filters

    @simple_filters.setter
    def simple_filters(self, value: Tuple[DataFilter, ...]):
        self.__simple_filters = value
        self._property_changed('simple_filters')        


class DataQueryResponse(Base):
               
    def __init__(
        self,
        type: str,
        request_id: str = None,
        error_message: str = None,
        id: str = None,
        data_set_id: str = None,
        entity_type: Union[MeasureEntityType, str] = None,
        delay: int = None,
        data: Tuple[FieldValueMap, ...] = None,
        groups: Tuple[DataGroup, ...] = None        
    ):
        super().__init__()
        self.__request_id = request_id
        self.__type = type
        self.__error_message = error_message
        self.__id = id
        self.__data_set_id = data_set_id
        self.__entity_type = get_enum_value(MeasureEntityType, entity_type)
        self.__delay = delay
        self.__data = data
        self.__groups = groups

    @property
    def request_id(self) -> str:
        """Marquee unique identifier"""
        return self.__request_id

    @request_id.setter
    def request_id(self, value: str):
        self.__request_id = value
        self._property_changed('request_id')        

    @property
    def type(self) -> str:
        return self.__type

    @type.setter
    def type(self, value: str):
        self.__type = value
        self._property_changed('type')        

    @property
    def error_message(self) -> str:
        return self.__error_message

    @error_message.setter
    def error_message(self, value: str):
        self.__error_message = value
        self._property_changed('error_message')        

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value
        self._property_changed('id')        

    @property
    def data_set_id(self) -> str:
        """Unique id of dataset."""
        return self.__data_set_id

    @data_set_id.setter
    def data_set_id(self, value: str):
        self.__data_set_id = value
        self._property_changed('data_set_id')        

    @property
    def entity_type(self) -> Union[MeasureEntityType, str]:
        """Entity type associated with a measure."""
        return self.__entity_type

    @entity_type.setter
    def entity_type(self, value: Union[MeasureEntityType, str]):
        self.__entity_type = value if isinstance(value, MeasureEntityType) else get_enum_value(MeasureEntityType, value)
        self._property_changed('entity_type')        

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


class FieldColumnPair(Base):
        
    """Map from fields to database columns."""
       
    def __init__(
        self,
        field: str = None,
        column: str = None,
        field_description: str = None,
        link: FieldLink = None        
    ):
        super().__init__()
        self.__field = field
        self.__column = column
        self.__field_description = field_description
        self.__link = link

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
    def field_description(self) -> str:
        """Custom description (overrides field default)."""
        return self.__field_description

    @field_description.setter
    def field_description(self, value: str):
        self.__field_description = value
        self._property_changed('field_description')        

    @property
    def link(self) -> FieldLink:
        """Link the field with other entity to also fetch its fields."""
        return self.__link

    @link.setter
    def link(self, value: FieldLink):
        self.__link = value
        self._property_changed('link')        


class HistoryFilter(Base):
        
    """Restricts queries against dataset to a time range."""
       
    def __init__(
        self,
        absolute_start: datetime.datetime = None,
        absolute_end: datetime.datetime = None,
        relative_start_seconds: float = None,
        relative_end_seconds: float = None,
        delay: DataSetDelay = None        
    ):
        super().__init__()
        self.__absolute_start = absolute_start
        self.__absolute_end = absolute_end
        self.__relative_start_seconds = relative_start_seconds
        self.__relative_end_seconds = relative_end_seconds
        self.__delay = delay

    @property
    def absolute_start(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__absolute_start

    @absolute_start.setter
    def absolute_start(self, value: datetime.datetime):
        self.__absolute_start = value
        self._property_changed('absolute_start')        

    @property
    def absolute_end(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__absolute_end

    @absolute_end.setter
    def absolute_end(self, value: datetime.datetime):
        self.__absolute_end = value
        self._property_changed('absolute_end')        

    @property
    def relative_start_seconds(self) -> float:
        """Earliest start time in seconds before current time."""
        return self.__relative_start_seconds

    @relative_start_seconds.setter
    def relative_start_seconds(self, value: float):
        self.__relative_start_seconds = value
        self._property_changed('relative_start_seconds')        

    @property
    def relative_end_seconds(self) -> float:
        """Latest end time in seconds before current time."""
        return self.__relative_end_seconds

    @relative_end_seconds.setter
    def relative_end_seconds(self, value: float):
        self.__relative_end_seconds = value
        self._property_changed('relative_end_seconds')        

    @property
    def delay(self) -> DataSetDelay:
        """Specifies the delayed data properties."""
        return self.__delay

    @delay.setter
    def delay(self, value: DataSetDelay):
        self.__delay = value
        self._property_changed('delay')        


class MDAPIDataBatchResponse(Base):
               
    def __init__(
        self,
        request_id: str = None,
        responses: Tuple[MDAPIDataQueryResponse, ...] = None        
    ):
        super().__init__()
        self.__request_id = request_id
        self.__responses = responses

    @property
    def request_id(self) -> str:
        """Marquee unique identifier"""
        return self.__request_id

    @request_id.setter
    def request_id(self, value: str):
        self.__request_id = value
        self._property_changed('request_id')        

    @property
    def responses(self) -> Tuple[MDAPIDataQueryResponse, ...]:
        """MDAPI Data query responses"""
        return self.__responses

    @responses.setter
    def responses(self, value: Tuple[MDAPIDataQueryResponse, ...]):
        self.__responses = value
        self._property_changed('responses')        


class MarketDataMapping(Base):
               
    def __init__(
        self,
        asset_class: Union[AssetClass, str] = None,
        query_type: str = None,
        description: str = None,
        scale: float = None,
        frequency: Union[MarketDataFrequency, str] = None,
        measures: Tuple[Union[MarketDataMeasure, str], ...] = None,
        data_set: str = None,
        vendor: Union[MarketDataVendor, str] = None,
        fields: Tuple[MarketDataField, ...] = None,
        rank: float = None,
        filtered_fields: Tuple[MarketDataFilteredField, ...] = None,
        asset_types: Tuple[Union[AssetType, str], ...] = None,
        entity_type: Union[MeasureEntityType, str] = None,
        backtest_entity: MeasureBacktest = None,
        kpi_entity: MeasureKpi = None        
    ):
        super().__init__()
        self.__asset_class = get_enum_value(AssetClass, asset_class)
        self.__query_type = query_type
        self.__description = description
        self.__scale = scale
        self.__frequency = get_enum_value(MarketDataFrequency, frequency)
        self.__measures = measures
        self.__data_set = data_set
        self.__vendor = get_enum_value(MarketDataVendor, vendor)
        self.__fields = fields
        self.__rank = rank
        self.__filtered_fields = filtered_fields
        self.__asset_types = asset_types
        self.__entity_type = get_enum_value(MeasureEntityType, entity_type)
        self.__backtest_entity = backtest_entity
        self.__kpi_entity = kpi_entity

    @property
    def asset_class(self) -> Union[AssetClass, str]:
        """Asset class that is applicable for mapping."""
        return self.__asset_class

    @asset_class.setter
    def asset_class(self, value: Union[AssetClass, str]):
        self.__asset_class = value if isinstance(value, AssetClass) else get_enum_value(AssetClass, value)
        self._property_changed('asset_class')        

    @property
    def query_type(self) -> str:
        """Market data query type."""
        return self.__query_type

    @query_type.setter
    def query_type(self, value: str):
        self.__query_type = value
        self._property_changed('query_type')        

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
    def data_set(self) -> str:
        """Marquee unique identifier"""
        return self.__data_set

    @data_set.setter
    def data_set(self, value: str):
        self.__data_set = value
        self._property_changed('data_set')        

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
    def filtered_fields(self) -> Tuple[MarketDataFilteredField, ...]:
        return self.__filtered_fields

    @filtered_fields.setter
    def filtered_fields(self, value: Tuple[MarketDataFilteredField, ...]):
        self.__filtered_fields = value
        self._property_changed('filtered_fields')        

    @property
    def asset_types(self) -> Tuple[Union[AssetType, str], ...]:
        """Asset type differentiates the product categorization or contract type"""
        return self.__asset_types

    @asset_types.setter
    def asset_types(self, value: Tuple[Union[AssetType, str], ...]):
        self.__asset_types = value
        self._property_changed('asset_types')        

    @property
    def entity_type(self) -> Union[MeasureEntityType, str]:
        """Entity type associated with a measure."""
        return self.__entity_type

    @entity_type.setter
    def entity_type(self, value: Union[MeasureEntityType, str]):
        self.__entity_type = value if isinstance(value, MeasureEntityType) else get_enum_value(MeasureEntityType, value)
        self._property_changed('entity_type')        

    @property
    def backtest_entity(self) -> MeasureBacktest:
        """Describes backtests that should be associated with a measure."""
        return self.__backtest_entity

    @backtest_entity.setter
    def backtest_entity(self, value: MeasureBacktest):
        self.__backtest_entity = value
        self._property_changed('backtest_entity')        

    @property
    def kpi_entity(self) -> MeasureKpi:
        """Describes KPIs that should be associated with a measure."""
        return self.__kpi_entity

    @kpi_entity.setter
    def kpi_entity(self, value: MeasureKpi):
        self.__kpi_entity = value
        self._property_changed('kpi_entity')        


class ProcessorEntity(Base):
        
    """Query processors for dataset."""
       
    def __init__(
        self,
        filters: Tuple[str, ...] = None,
        parsers: Tuple[ParserEntity, ...] = None,
        deduplicate: Tuple[str, ...] = None        
    ):
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


class DataSetDimensions(Base):
        
    """Dataset dimensions."""
       
    def __init__(
        self,
        time_field: str,
        transaction_time_field: str = None,
        symbol_dimensions: Tuple[str, ...] = None,
        non_symbol_dimensions: Tuple[FieldColumnPair, ...] = None,
        key_dimensions: Tuple[str, ...] = None,
        measures: Tuple[FieldColumnPair, ...] = None,
        entity_dimension: str = None        
    ):
        super().__init__()
        self.__time_field = time_field
        self.__transaction_time_field = transaction_time_field
        self.__symbol_dimensions = symbol_dimensions
        self.__non_symbol_dimensions = non_symbol_dimensions
        self.__key_dimensions = key_dimensions
        self.__measures = measures
        self.__entity_dimension = entity_dimension

    @property
    def time_field(self) -> str:
        return self.__time_field

    @time_field.setter
    def time_field(self, value: str):
        self.__time_field = value
        self._property_changed('time_field')        

    @property
    def transaction_time_field(self) -> str:
        """For bi-temporal datasets, field for capturing the time at which a data point was updated."""
        return self.__transaction_time_field

    @transaction_time_field.setter
    def transaction_time_field(self, value: str):
        self.__transaction_time_field = value
        self._property_changed('transaction_time_field')        

    @property
    def symbol_dimensions(self) -> Tuple[str, ...]:
        """Set of fields that determine database table name."""
        return self.__symbol_dimensions

    @symbol_dimensions.setter
    def symbol_dimensions(self, value: Tuple[str, ...]):
        self.__symbol_dimensions = value
        self._property_changed('symbol_dimensions')        

    @property
    def non_symbol_dimensions(self) -> Tuple[FieldColumnPair, ...]:
        """Fields that are not nullable."""
        return self.__non_symbol_dimensions

    @non_symbol_dimensions.setter
    def non_symbol_dimensions(self, value: Tuple[FieldColumnPair, ...]):
        self.__non_symbol_dimensions = value
        self._property_changed('non_symbol_dimensions')        

    @property
    def key_dimensions(self) -> Tuple[str, ...]:
        return self.__key_dimensions

    @key_dimensions.setter
    def key_dimensions(self, value: Tuple[str, ...]):
        self.__key_dimensions = value
        self._property_changed('key_dimensions')        

    @property
    def measures(self) -> Tuple[FieldColumnPair, ...]:
        """Fields that are nullable."""
        return self.__measures

    @measures.setter
    def measures(self, value: Tuple[FieldColumnPair, ...]):
        self.__measures = value
        self._property_changed('measures')        

    @property
    def entity_dimension(self) -> str:
        """Symbol dimension corresponding to an entity e.g. asset or report."""
        return self.__entity_dimension

    @entity_dimension.setter
    def entity_dimension(self, value: str):
        self.__entity_dimension = value
        self._property_changed('entity_dimension')        


class EntityFilter(Base):
        
    """Filter on entities."""
       
    def __init__(
        self,
        operator: str = None,
        simple_filters: Tuple[DataFilter, ...] = None,
        complex_filters: Tuple[ComplexFilter, ...] = None        
    ):
        super().__init__()
        self.__operator = operator
        self.__simple_filters = simple_filters
        self.__complex_filters = complex_filters

    @property
    def operator(self) -> str:
        return self.__operator

    @operator.setter
    def operator(self, value: str):
        self.__operator = value
        self._property_changed('operator')        

    @property
    def simple_filters(self) -> Tuple[DataFilter, ...]:
        """Filter on specified field."""
        return self.__simple_filters

    @simple_filters.setter
    def simple_filters(self, value: Tuple[DataFilter, ...]):
        self.__simple_filters = value
        self._property_changed('simple_filters')        

    @property
    def complex_filters(self) -> Tuple[ComplexFilter, ...]:
        """A compound filter for data requests."""
        return self.__complex_filters

    @complex_filters.setter
    def complex_filters(self, value: Tuple[ComplexFilter, ...]):
        self.__complex_filters = value
        self._property_changed('complex_filters')        


class DataSetFilters(Base):
        
    """Filters to restrict the set of data returned."""
       
    def __init__(
        self,
        entity_filter: EntityFilter = None,
        row_filters: Tuple[DataFilter, ...] = None,
        advanced_filters: Tuple[AdvancedFilter, ...] = None,
        history_filter: HistoryFilter = None        
    ):
        super().__init__()
        self.__entity_filter = entity_filter
        self.__row_filters = row_filters
        self.__advanced_filters = advanced_filters
        self.__history_filter = history_filter

    @property
    def entity_filter(self) -> EntityFilter:
        """Filter on entities."""
        return self.__entity_filter

    @entity_filter.setter
    def entity_filter(self, value: EntityFilter):
        self.__entity_filter = value
        self._property_changed('entity_filter')        

    @property
    def row_filters(self) -> Tuple[DataFilter, ...]:
        """Filters on database rows."""
        return self.__row_filters

    @row_filters.setter
    def row_filters(self, value: Tuple[DataFilter, ...]):
        self.__row_filters = value
        self._property_changed('row_filters')        

    @property
    def advanced_filters(self) -> Tuple[AdvancedFilter, ...]:
        """Advanced filter for numeric fields."""
        return self.__advanced_filters

    @advanced_filters.setter
    def advanced_filters(self, value: Tuple[AdvancedFilter, ...]):
        self.__advanced_filters = value
        self._property_changed('advanced_filters')        

    @property
    def history_filter(self) -> HistoryFilter:
        """Restricts queries against dataset to a time range."""
        return self.__history_filter

    @history_filter.setter
    def history_filter(self, value: HistoryFilter):
        self.__history_filter = value
        self._property_changed('history_filter')        


class DataSetEntity(Base):
               
    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        short_description: str,
        vendor: str,
        data_product: str,
        parameters: DataSetParameters,
        dimensions: DataSetDimensions,
        owner_id: str = None,
        mappings: Tuple[MarketDataMapping, ...] = None,
        start_date: datetime.date = None,
        mdapi: MDAPI = None,
        entitlements: Entitlements = None,
        entitlement_exclusions: EntitlementExclusions = None,
        query_processors: ProcessorEntity = None,
        defaults: DataSetDefaults = None,
        filters: DataSetFilters = None,
        created_by_id: str = None,
        created_time: datetime.datetime = None,
        last_updated_by_id: str = None,
        last_updated_time: datetime.datetime = None,
        tags: Tuple[str, ...] = None        
    ):
        super().__init__()
        self.__owner_id = owner_id
        self.__id = id
        self.__name = name
        self.__description = description
        self.__short_description = short_description
        self.__mappings = mappings
        self.__vendor = vendor
        self.__start_date = start_date
        self.__mdapi = mdapi
        self.__data_product = data_product
        self.__entitlements = entitlements
        self.__entitlement_exclusions = entitlement_exclusions
        self.__query_processors = query_processors
        self.__parameters = parameters
        self.__dimensions = dimensions
        self.__defaults = defaults
        self.__filters = filters
        self.__created_by_id = created_by_id
        self.__created_time = created_time
        self.__last_updated_by_id = last_updated_by_id
        self.__last_updated_time = last_updated_time
        self.__tags = tags

    @property
    def owner_id(self) -> str:
        """Marquee unique identifier for user who owns the object."""
        return self.__owner_id

    @owner_id.setter
    def owner_id(self, value: str):
        self.__owner_id = value
        self._property_changed('owner_id')        

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
    def short_description(self) -> str:
        """Short description of dataset."""
        return self.__short_description

    @short_description.setter
    def short_description(self, value: str):
        self.__short_description = value
        self._property_changed('short_description')        

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
    def start_date(self) -> datetime.date:
        """The start of this data set"""
        return self.__start_date

    @start_date.setter
    def start_date(self, value: datetime.date):
        self.__start_date = value
        self._property_changed('start_date')        

    @property
    def mdapi(self) -> MDAPI:
        """Defines MDAPI fields."""
        return self.__mdapi

    @mdapi.setter
    def mdapi(self, value: MDAPI):
        self.__mdapi = value
        self._property_changed('mdapi')        

    @property
    def data_product(self) -> str:
        """Product that dataset belongs to."""
        return self.__data_product

    @data_product.setter
    def data_product(self, value: str):
        self.__data_product = value
        self._property_changed('data_product')        

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
    def query_processors(self) -> ProcessorEntity:
        """Query processors for dataset."""
        return self.__query_processors

    @query_processors.setter
    def query_processors(self, value: ProcessorEntity):
        self.__query_processors = value
        self._property_changed('query_processors')        

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
    def tags(self) -> Tuple[str, ...]:
        """Tags associated with dataset."""
        return self.__tags

    @tags.setter
    def tags(self, value: Tuple[str, ...]):
        self.__tags = value
        self._property_changed('tags')        
