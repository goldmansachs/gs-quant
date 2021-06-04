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


class DelayExclusionType(EnumBase, Enum):    
    
    """Type of the delay exclusion"""

    LAST_DAY_OF_THE_MONTH = 'LAST_DAY_OF_THE_MONTH'    


class DevelopmentStatus(EnumBase, Enum):    
    
    """The status of development of this dataset. Controls rate limit on query/upload."""

    Development = 'Development'
    Production = 'Production'    


class FieldFormat(EnumBase, Enum):    
    
    """Format to apply on field validation. Currently supports a subset of built-in
       formats (from JSON schema specification)."""

    date = 'date'
    date_time = 'date-time'    


class MarketDataFrequency(EnumBase, Enum):    
    
    Real_Time = 'Real Time'
    End_Of_Day = 'End Of Day'    


class MarketDataMeasure(EnumBase, Enum):    
    
    Last = 'Last'
    Curve = 'Curve'
    Close_Change = 'Close Change'
    Previous_Close = 'Previous Close'    


class MeasureEntityType(EnumBase, Enum):    
    
    """Entity type associated with a measure."""

    ASSET = 'ASSET'
    BACKTEST = 'BACKTEST'
    KPI = 'KPI'
    COUNTRY = 'COUNTRY'
    SUBDIVISION = 'SUBDIVISION'
    REPORT = 'REPORT'
    HEDGE = 'HEDGE'
    PORTFOLIO = 'PORTFOLIO'
    RISK_MODEL = 'RISK_MODEL'    


class AdvancedFilter(Base):
        
    """Advanced filters for the Dataset."""

    @camel_case_translate
    def __init__(
        self,
        column: str,
        operator: str,
        value: float = None,
        values: Tuple[str, ...] = None,
        format_: str = None,
        name: str = None
    ):        
        super().__init__()
        self.column = column
        self.value = value
        self.values = values
        self.operator = operator
        self.__format = format_
        self.name = name

    @property
    def column(self) -> str:
        """Database column to match against."""
        return self.__column

    @column.setter
    def column(self, value: str):
        self._property_changed('column')
        self.__column = value        

    @property
    def value(self) -> float:
        """Numeric value to compare against. Cannot be used with 'in' and 'notIn'
           operators."""
        return self.__value

    @value.setter
    def value(self, value: float):
        self._property_changed('value')
        self.__value = value        

    @property
    def values(self) -> Tuple[str, ...]:
        """Values to compare against. Can only be used with 'in' and 'notIn' operators."""
        return self.__values

    @values.setter
    def values(self, value: Tuple[str, ...]):
        self._property_changed('values')
        self.__values = value        

    @property
    def operator(self) -> str:
        """Comparison operator."""
        return self.__operator

    @operator.setter
    def operator(self, value: str):
        self._property_changed('operator')
        self.__operator = value        

    @property
    def format(self) -> str:
        """Format like relativeToDate"""
        return self.__format

    @format.setter
    def format(self, value: str):
        self._property_changed('format')
        self.__format = value        


class DataSetCondition(Base):
        
    """Condition for Dataset Transformations and Filters."""

    @camel_case_translate
    def __init__(
        self,
        column: str,
        operator: str,
        value: float = None,
        values: Tuple[str, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.column = column
        self.value = value
        self.values = values
        self.operator = operator
        self.name = name

    @property
    def column(self) -> str:
        """Database column to match against."""
        return self.__column

    @column.setter
    def column(self, value: str):
        self._property_changed('column')
        self.__column = value        

    @property
    def value(self) -> float:
        """Numeric value to compare against. Cannot be used with 'in' and 'notIn'
           operators."""
        return self.__value

    @value.setter
    def value(self, value: float):
        self._property_changed('value')
        self.__value = value        

    @property
    def values(self) -> Tuple[str, ...]:
        """Values to compare against. Can only be used with 'in' and 'notIn' operators."""
        return self.__values

    @values.setter
    def values(self, value: Tuple[str, ...]):
        self._property_changed('values')
        self.__values = value        

    @property
    def operator(self) -> str:
        """Comparison operator."""
        return self.__operator

    @operator.setter
    def operator(self, value: str):
        self._property_changed('operator')
        self.__operator = value        


class DataSetDefaults(Base):
        
    """Default start/end dates/times applied when data is queried, if not specified by
       user."""

    @camel_case_translate
    def __init__(
        self,
        start_seconds: float = None,
        end_seconds: float = None,
        delay_seconds: float = None,
        name: str = None
    ):        
        super().__init__()
        self.start_seconds = start_seconds
        self.end_seconds = end_seconds
        self.delay_seconds = delay_seconds
        self.name = name

    @property
    def start_seconds(self) -> float:
        """Default start date/time, in seconds before current time. Recommend 86400 (1 day)
           for time-based datasets and 2592000 (30 days) for date-base datasets."""
        return self.__start_seconds

    @start_seconds.setter
    def start_seconds(self, value: float):
        self._property_changed('start_seconds')
        self.__start_seconds = value        

    @property
    def end_seconds(self) -> float:
        """Default end date/time, in seconds before current time. Typically 0."""
        return self.__end_seconds

    @end_seconds.setter
    def end_seconds(self, value: float):
        self._property_changed('end_seconds')
        self.__end_seconds = value        

    @property
    def delay_seconds(self) -> float:
        """Default market delay to apply, in seconds. Typically 0."""
        return self.__delay_seconds

    @delay_seconds.setter
    def delay_seconds(self, value: float):
        self._property_changed('delay_seconds')
        self.__delay_seconds = value        


class DataSetFieldEntityAttributes(Base):
        
    """Read-only attributes of the field. Useful for searching."""

    @camel_case_translate
    def __init__(
        self,
        in_code: bool = None,
        is_entity: bool = None,
        name: str = None
    ):        
        super().__init__()
        self.in_code = in_code
        self.is_entity = is_entity
        self.name = name

    @property
    def in_code(self) -> bool:
        """If 'TRUE', this field is defined in code."""
        return self.__in_code

    @in_code.setter
    def in_code(self, value: bool):
        self._property_changed('in_code')
        self.__in_code = value        

    @property
    def is_entity(self) -> bool:
        """If 'TRUE', this field is an entity field."""
        return self.__is_entity

    @is_entity.setter
    def is_entity(self, value: bool):
        self._property_changed('is_entity')
        self.__is_entity = value        


class DataSetFieldEntityClassifications(Base):
        
    """Classifications for a Field Entity."""

    @camel_case_translate
    def __init__(
        self,
        groups: Tuple[str, ...] = None,
        data_set_id: str = None,
        name: str = None
    ):        
        super().__init__()
        self.groups = groups
        self.data_set_id = data_set_id
        self.name = name

    @property
    def groups(self) -> Tuple[str, ...]:
        """Logical group(s) for the field."""
        return self.__groups

    @groups.setter
    def groups(self, value: Tuple[str, ...]):
        self._property_changed('groups')
        self.__groups = value        

    @property
    def data_set_id(self) -> str:
        """Unique id of dataset."""
        return self.__data_set_id

    @data_set_id.setter
    def data_set_id(self, value: str):
        self._property_changed('data_set_id')
        self.__data_set_id = value        


class DataSetFieldEntityNumberParameters(Base):
        
    """Parameters for field 'type' of 'number'."""

    @camel_case_translate
    def __init__(
        self,
        maximum: int = None,
        minimum: int = None,
        name: str = None
    ):        
        super().__init__()
        self.maximum = maximum
        self.minimum = minimum
        self.name = name

    @property
    def maximum(self) -> int:
        """Maximum value of the field. Default on create: 1,000,000,000"""
        return self.__maximum

    @maximum.setter
    def maximum(self, value: int):
        self._property_changed('maximum')
        self.__maximum = value        

    @property
    def minimum(self) -> int:
        """Minimum value of the field. Default on create: -1,000,000,000"""
        return self.__minimum

    @minimum.setter
    def minimum(self, value: int):
        self._property_changed('minimum')
        self.__minimum = value        


class EntityMetadata(Base):
        
    """Contains read-only metadata for internal users to view."""

    @camel_case_translate
    def __init__(
        self,
        created_by_id: str = None,
        created_time: datetime.datetime = None,
        last_updated_by_id: str = None,
        last_updated_time: datetime.datetime = None,
        name: str = None
    ):        
        super().__init__()
        self.created_by_id = created_by_id
        self.created_time = created_time
        self.last_updated_by_id = last_updated_by_id
        self.last_updated_time = last_updated_time
        self.name = name

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


class ErrorInfo(Base):
        
    """A standard JSON-formatted error response."""

    @camel_case_translate
    def __init__(
        self,
        status_code: int,
        reason_phrase: str,
        title: str = None,
        messages: Tuple[str, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.status_code = status_code
        self.reason_phrase = reason_phrase
        self.title = title
        self.messages = messages
        self.name = name

    @property
    def status_code(self) -> int:
        """HTTP response status code."""
        return self.__status_code

    @status_code.setter
    def status_code(self, value: int):
        self._property_changed('status_code')
        self.__status_code = value        

    @property
    def reason_phrase(self) -> str:
        """Reason for the error."""
        return self.__reason_phrase

    @reason_phrase.setter
    def reason_phrase(self, value: str):
        self._property_changed('reason_phrase')
        self.__reason_phrase = value        

    @property
    def title(self) -> str:
        """Title of the error response."""
        return self.__title

    @title.setter
    def title(self, value: str):
        self._property_changed('title')
        self.__title = value        

    @property
    def messages(self) -> Tuple[str, ...]:
        """Accompanying array of messages."""
        return self.__messages

    @messages.setter
    def messages(self, value: Tuple[str, ...]):
        self._property_changed('messages')
        self.__messages = value        


class FieldLinkSelector(Base):
        
    """Stores selector and name how field is presented in dataset."""

    @camel_case_translate
    def __init__(
        self,
        field_selector: str = None,
        description: str = None,
        display_name: str = None,
        name: str = None
    ):        
        super().__init__()
        self.field_selector = field_selector
        self.description = description
        self.display_name = display_name
        self.name = name

    @property
    def field_selector(self) -> str:
        """Selector which captures the field from the Entity."""
        return self.__field_selector

    @field_selector.setter
    def field_selector(self, value: str):
        self._property_changed('field_selector')
        self.__field_selector = value        

    @property
    def description(self) -> str:
        """Custom description (overrides field default)."""
        return self.__description

    @description.setter
    def description(self, value: str):
        self._property_changed('description')
        self.__description = value        

    @property
    def display_name(self) -> str:
        """Name under which the captured field will be displayed. The name must be
           registered in fields."""
        return self.__display_name

    @display_name.setter
    def display_name(self, value: str):
        self._property_changed('display_name')
        self.__display_name = value        


class MDAPI(Base):
        
    """Defines MDAPI fields."""

    @camel_case_translate
    def __init__(
        self,
        type_: str,
        quoting_styles: Tuple[dict, ...],
        class_: str = None,
        name: str = None
    ):        
        super().__init__()
        self.__class = class_
        self.__type = type_
        self.quoting_styles = quoting_styles
        self.name = name

    @property
    def class_(self) -> str:
        """MDAPI Class."""
        return self.__class

    @class_.setter
    def class_(self, value: str):
        self._property_changed('class_')
        self.__class = value        

    @property
    def type(self) -> str:
        """The MDAPI Type field (private)"""
        return self.__type

    @type.setter
    def type(self, value: str):
        self._property_changed('type')
        self.__type = value        

    @property
    def quoting_styles(self) -> Tuple[dict, ...]:
        """Map from MDAPI QuotingStyles to database columns"""
        return self.__quoting_styles

    @quoting_styles.setter
    def quoting_styles(self, value: Tuple[dict, ...]):
        self._property_changed('quoting_styles')
        self.__quoting_styles = value        


class MarketDataField(Base):
        
    @camel_case_translate
    def __init__(
        self,
        name: str = None,
        mapping: str = None
    ):        
        super().__init__()
        self.name = name
        self.mapping = mapping

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def mapping(self) -> str:
        return self.__mapping

    @mapping.setter
    def mapping(self, value: str):
        self._property_changed('mapping')
        self.__mapping = value        


class MarketDataFilteredField(Base):
        
    @camel_case_translate
    def __init__(
        self,
        field: str = None,
        default_value: str = None,
        default_numerical_value: float = None,
        default_boolean_value: bool = None,
        numerical_values: Tuple[float, ...] = None,
        values: Tuple[str, ...] = None,
        multi_measure: bool = None,
        name: str = None
    ):        
        super().__init__()
        self.field = field
        self.default_value = default_value
        self.default_numerical_value = default_numerical_value
        self.default_boolean_value = default_boolean_value
        self.numerical_values = numerical_values
        self.values = values
        self.multi_measure = multi_measure
        self.name = name

    @property
    def field(self) -> str:
        """Filtered field name"""
        return self.__field

    @field.setter
    def field(self, value: str):
        self._property_changed('field')
        self.__field = value        

    @property
    def default_value(self) -> str:
        """Default filtered field"""
        return self.__default_value

    @default_value.setter
    def default_value(self, value: str):
        self._property_changed('default_value')
        self.__default_value = value        

    @property
    def default_numerical_value(self) -> float:
        """Default numerical filtered field"""
        return self.__default_numerical_value

    @default_numerical_value.setter
    def default_numerical_value(self, value: float):
        self._property_changed('default_numerical_value')
        self.__default_numerical_value = value        

    @property
    def default_boolean_value(self) -> bool:
        """Default for boolean field"""
        return self.__default_boolean_value

    @default_boolean_value.setter
    def default_boolean_value(self, value: bool):
        self._property_changed('default_boolean_value')
        self.__default_boolean_value = value        

    @property
    def numerical_values(self) -> Tuple[float, ...]:
        """Array of numerical filtered fields"""
        return self.__numerical_values

    @numerical_values.setter
    def numerical_values(self, value: Tuple[float, ...]):
        self._property_changed('numerical_values')
        self.__numerical_values = value        

    @property
    def values(self) -> Tuple[str, ...]:
        """Array of filtered fields"""
        return self.__values

    @values.setter
    def values(self, value: Tuple[str, ...]):
        self._property_changed('values')
        self.__values = value        

    @property
    def multi_measure(self) -> bool:
        """Allow you to pivot the mapping selection based on the available measures being
           used as parameters."""
        return self.__multi_measure

    @multi_measure.setter
    def multi_measure(self, value: bool):
        self._property_changed('multi_measure')
        self.__multi_measure = value        


class MeasureBacktest(Base):
        
    """Describes backtests that should be associated with a measure."""

    @camel_case_translate
    def __init__(
        self,
        name: str = None
    ):        
        super().__init__()
        self.name = name


class MeasureKpi(Base):
        
    """Describes KPIs that should be associated with a measure."""

    @camel_case_translate
    def __init__(
        self,
        name: str = None
    ):        
        super().__init__()
        self.name = name


class MidPrice(Base):
        
    """Specification for a mid price column derived from bid and ask columns."""

    @camel_case_translate
    def __init__(
        self,
        bid_column: str = None,
        ask_column: str = None,
        mid_column: str = None,
        name: str = None
    ):        
        super().__init__()
        self.bid_column = bid_column
        self.ask_column = ask_column
        self.mid_column = mid_column
        self.name = name

    @property
    def bid_column(self) -> str:
        """Database column name."""
        return self.__bid_column

    @bid_column.setter
    def bid_column(self, value: str):
        self._property_changed('bid_column')
        self.__bid_column = value        

    @property
    def ask_column(self) -> str:
        """Database column name."""
        return self.__ask_column

    @ask_column.setter
    def ask_column(self, value: str):
        self._property_changed('ask_column')
        self.__ask_column = value        

    @property
    def mid_column(self) -> str:
        """Database column name."""
        return self.__mid_column

    @mid_column.setter
    def mid_column(self, value: str):
        self._property_changed('mid_column')
        self.__mid_column = value        


class ParserEntity(Base):
        
    """Settings for a parser processor"""

    @camel_case_translate
    def __init__(
        self,
        only_normalized_fields: bool = None,
        quotes: bool = None,
        trades: bool = None,
        name: str = None
    ):        
        super().__init__()
        self.only_normalized_fields = only_normalized_fields
        self.quotes = quotes
        self.trades = trades
        self.name = name

    @property
    def only_normalized_fields(self) -> bool:
        """Setting for onlyNormalizedFields."""
        return self.__only_normalized_fields

    @only_normalized_fields.setter
    def only_normalized_fields(self, value: bool):
        self._property_changed('only_normalized_fields')
        self.__only_normalized_fields = value        

    @property
    def quotes(self) -> bool:
        """Setting for quotes."""
        return self.__quotes

    @quotes.setter
    def quotes(self, value: bool):
        self._property_changed('quotes')
        self.__quotes = value        

    @property
    def trades(self) -> bool:
        """Setting for trades."""
        return self.__trades

    @trades.setter
    def trades(self, value: bool):
        self._property_changed('trades')
        self.__trades = value        


class RemapFieldPair(Base):
        
    """Field and remapTo field pair."""

    @camel_case_translate
    def __init__(
        self,
        field: str = None,
        remap_to: str = None,
        name: str = None
    ):        
        super().__init__()
        self.field = field
        self.remap_to = remap_to
        self.name = name

    @property
    def field(self) -> str:
        """Field to remap."""
        return self.__field

    @field.setter
    def field(self, value: str):
        self._property_changed('field')
        self.__field = value        

    @property
    def remap_to(self) -> str:
        """Field to remap to."""
        return self.__remap_to

    @remap_to.setter
    def remap_to(self, value: str):
        self._property_changed('remap_to')
        self.__remap_to = value        


class ResponseInfo(Base):
        
    """A standard JSON-formatted response."""

    @camel_case_translate
    def __init__(
        self,
        request_id: str = None,
        messages: Tuple[str, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.request_id = request_id
        self.messages = messages
        self.name = name

    @property
    def request_id(self) -> str:
        """Marquee unique identifier"""
        return self.__request_id

    @request_id.setter
    def request_id(self, value: str):
        self._property_changed('request_id')
        self.__request_id = value        

    @property
    def messages(self) -> Tuple[str, ...]:
        """Accompanying array of messages."""
        return self.__messages

    @messages.setter
    def messages(self, value: Tuple[str, ...]):
        self._property_changed('messages')
        self.__messages = value        


class SymbolFilterLink(Base):
        
    """The entity type and field used to filter symbols."""

    @camel_case_translate
    def __init__(
        self,
        entity_field: str = None,
        name: str = None
    ):        
        super().__init__()
        self.entity_field = entity_field
        self.name = name

    @property
    def entity_type(self) -> str:
        """The type of the entity to lookup to."""
        return 'MktCoordinate'        

    @property
    def entity_field(self) -> str:
        """The field of the entity to lookup to."""
        return self.__entity_field

    @entity_field.setter
    def entity_field(self, value: str):
        self._property_changed('entity_field')
        self.__entity_field = value        


class DataFilter(Base):
        
    """Filter on specified field."""

    @camel_case_translate
    def __init__(
        self,
        field: str,
        values: Tuple[str, ...],
        column: str = None,
        where: DataSetCondition = None,
        name: str = None
    ):        
        super().__init__()
        self.field = field
        self.column = column
        self.values = values
        self.where = where
        self.name = name

    @property
    def field(self) -> str:
        """Field to filter on."""
        return self.__field

    @field.setter
    def field(self, value: str):
        self._property_changed('field')
        self.__field = value        

    @property
    def column(self) -> str:
        """Database column name."""
        return self.__column

    @column.setter
    def column(self, value: str):
        self._property_changed('column')
        self.__column = value        

    @property
    def values(self) -> Tuple[str, ...]:
        """Value(s) to match."""
        return self.__values

    @values.setter
    def values(self, value: Tuple[str, ...]):
        self._property_changed('values')
        self.__values = value        

    @property
    def where(self) -> DataSetCondition:
        """Only apply the filter where this condition matches."""
        return self.__where

    @where.setter
    def where(self, value: DataSetCondition):
        self._property_changed('where')
        self.__where = value        


class DataSetCoverageProperties(Base):
        
    """Dataset coverage properties."""

    @camel_case_translate
    def __init__(
        self,
        prefixes: Tuple[str, ...] = None,
        prefix_type: str = 'SYMBOL',
        asset_classes: Tuple[Union[AssetClass, str], ...] = None,
        asset_types: Tuple[Union[AssetType, str], ...] = None,
        entity_types: Tuple[Union[MeasureEntityType, str], ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.prefixes = prefixes
        self.prefix_type = prefix_type
        self.asset_classes = asset_classes
        self.asset_types = asset_types
        self.entity_types = entity_types
        self.name = name

    @property
    def prefixes(self) -> Tuple[str, ...]:
        """Prefixes of the dataset coverage"""
        return self.__prefixes

    @prefixes.setter
    def prefixes(self, value: Tuple[str, ...]):
        self._property_changed('prefixes')
        self.__prefixes = value        

    @property
    def prefix_type(self) -> str:
        """The type of the coverage prefixes."""
        return self.__prefix_type

    @prefix_type.setter
    def prefix_type(self, value: str):
        self._property_changed('prefix_type')
        self.__prefix_type = value        

    @property
    def asset_classes(self) -> Tuple[Union[AssetClass, str], ...]:
        """Asset classification of security. Assets are classified into broad groups which
           exhibit similar characteristics and behave in a consistent way under
           different market conditions"""
        return self.__asset_classes

    @asset_classes.setter
    def asset_classes(self, value: Tuple[Union[AssetClass, str], ...]):
        self._property_changed('asset_classes')
        self.__asset_classes = value        

    @property
    def asset_types(self) -> Tuple[Union[AssetType, str], ...]:
        """Asset type differentiates the product categorization or contract type"""
        return self.__asset_types

    @asset_types.setter
    def asset_types(self, value: Tuple[Union[AssetType, str], ...]):
        self._property_changed('asset_types')
        self.__asset_types = value        

    @property
    def entity_types(self) -> Tuple[Union[MeasureEntityType, str], ...]:
        """Entity type associated with a measure."""
        return self.__entity_types

    @entity_types.setter
    def entity_types(self, value: Tuple[Union[MeasureEntityType, str], ...]):
        self._property_changed('entity_types')
        self.__entity_types = value        


class DataSetDelay(Base):
        
    """Specifies the delayed data properties."""

    @camel_case_translate
    def __init__(
        self,
        until_seconds: float,
        at_time_zone: str,
        when: Tuple[Union[DelayExclusionType, str], ...] = None,
        history_up_to_seconds: float = None,
        history_up_to_time: datetime.datetime = None,
        history_up_to_months: float = None,
        name: str = None
    ):        
        super().__init__()
        self.until_seconds = until_seconds
        self.at_time_zone = at_time_zone
        self.when = when
        self.history_up_to_seconds = history_up_to_seconds
        self.history_up_to_time = history_up_to_time
        self.history_up_to_months = history_up_to_months
        self.name = name

    @property
    def until_seconds(self) -> float:
        """Seconds from midnight until which the delay will be applicable."""
        return self.__until_seconds

    @until_seconds.setter
    def until_seconds(self, value: float):
        self._property_changed('until_seconds')
        self.__until_seconds = value        

    @property
    def at_time_zone(self) -> str:
        """The time zone with respect to which the delay will be applied (must be a valid
           IANA TimeZone identifier)."""
        return self.__at_time_zone

    @at_time_zone.setter
    def at_time_zone(self, value: str):
        self._property_changed('at_time_zone')
        self.__at_time_zone = value        

    @property
    def when(self) -> Tuple[Union[DelayExclusionType, str], ...]:
        """Apply this delay filter only when the day belongs to this exclusion list."""
        return self.__when

    @when.setter
    def when(self, value: Tuple[Union[DelayExclusionType, str], ...]):
        self._property_changed('when')
        self.__when = value        

    @property
    def history_up_to_seconds(self) -> float:
        """Relative seconds up to which the data history will be shown for the business
           day."""
        return self.__history_up_to_seconds

    @history_up_to_seconds.setter
    def history_up_to_seconds(self, value: float):
        self._property_changed('history_up_to_seconds')
        self.__history_up_to_seconds = value        

    @property
    def history_up_to_time(self) -> datetime.datetime:
        """Absolute time up to which the data history will be shown for the business day."""
        return self.__history_up_to_time

    @history_up_to_time.setter
    def history_up_to_time(self, value: datetime.datetime):
        self._property_changed('history_up_to_time')
        self.__history_up_to_time = value        

    @property
    def history_up_to_months(self) -> float:
        """Months time up to which the data history will be shown for the business day."""
        return self.__history_up_to_months

    @history_up_to_months.setter
    def history_up_to_months(self, value: float):
        self._property_changed('history_up_to_months')
        self.__history_up_to_months = value        


class DataSetFieldEntityStringParameters(Base):
        
    """Parameters for field 'type' of 'string'."""

    @camel_case_translate
    def __init__(
        self,
        enum: Tuple[str, ...] = None,
        format_: Union[FieldFormat, str] = None,
        pattern: str = '^[\w ]{1,256}$',
        max_length: int = None,
        min_length: int = None,
        name: str = None
    ):        
        super().__init__()
        self.enum = enum
        self.__format = get_enum_value(FieldFormat, format_)
        self.pattern = pattern
        self.max_length = max_length
        self.min_length = min_length
        self.name = name

    @property
    def enum(self) -> Tuple[str, ...]:
        """List of possible values the field can take on."""
        return self.__enum

    @enum.setter
    def enum(self, value: Tuple[str, ...]):
        self._property_changed('enum')
        self.__enum = value        

    @property
    def format(self) -> Union[FieldFormat, str]:
        """Format to apply on field validation. Currently supports a subset of built-in
           formats (from JSON schema specification)."""
        return self.__format

    @format.setter
    def format(self, value: Union[FieldFormat, str]):
        self._property_changed('format')
        self.__format = get_enum_value(FieldFormat, value)        

    @property
    def pattern(self) -> str:
        """Regular Expression pattern to validate the field value."""
        return self.__pattern

    @pattern.setter
    def pattern(self, value: str):
        self._property_changed('pattern')
        self.__pattern = value        

    @property
    def max_length(self) -> int:
        """Max length of the string. To be used with 'pattern'."""
        return self.__max_length

    @max_length.setter
    def max_length(self, value: int):
        self._property_changed('max_length')
        self.__max_length = value        

    @property
    def min_length(self) -> int:
        """Min length of the string. To be used with 'pattern'."""
        return self.__min_length

    @min_length.setter
    def min_length(self, value: int):
        self._property_changed('min_length')
        self.__min_length = value        


class DataSetParameters(Base):
        
    """Dataset parameters."""

    @camel_case_translate
    def __init__(
        self,
        frequency: str,
        category: str = None,
        sub_category: str = None,
        methodology: str = None,
        coverage: str = None,
        coverages: Tuple[Union[AssetType, str], ...] = None,
        notes: str = None,
        history: str = None,
        sample_start: datetime.datetime = None,
        sample_end: datetime.datetime = None,
        published_date: datetime.datetime = None,
        history_date: datetime.datetime = None,
        asset_class: Union[AssetClass, str] = None,
        owner_ids: Tuple[str, ...] = None,
        support_ids: Tuple[str, ...] = None,
        support_distribution_list: Tuple[str, ...] = None,
        apply_market_data_entitlements: bool = None,
        upload_data_policy: str = None,
        logical_db: str = None,
        symbol_strategy: str = None,
        underlying_data_set_id: str = None,
        immutable: bool = None,
        include_in_catalog: bool = False,
        coverage_enabled: bool = True,
        use_created_time_for_upload: bool = None,
        apply_entity_entitlements: bool = None,
        development_status: Union[DevelopmentStatus, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.category = category
        self.sub_category = sub_category
        self.methodology = methodology
        self.coverage = coverage
        self.coverages = coverages
        self.notes = notes
        self.history = history
        self.sample_start = sample_start
        self.sample_end = sample_end
        self.published_date = published_date
        self.history_date = history_date
        self.frequency = frequency
        self.asset_class = asset_class
        self.owner_ids = owner_ids
        self.support_ids = support_ids
        self.support_distribution_list = support_distribution_list
        self.apply_market_data_entitlements = apply_market_data_entitlements
        self.upload_data_policy = upload_data_policy
        self.logical_db = logical_db
        self.symbol_strategy = symbol_strategy
        self.underlying_data_set_id = underlying_data_set_id
        self.immutable = immutable
        self.include_in_catalog = include_in_catalog
        self.coverage_enabled = coverage_enabled
        self.use_created_time_for_upload = use_created_time_for_upload
        self.apply_entity_entitlements = apply_entity_entitlements
        self.development_status = development_status
        self.name = name

    @property
    def category(self) -> str:
        """Top level grouping."""
        return self.__category

    @category.setter
    def category(self, value: str):
        self._property_changed('category')
        self.__category = value        

    @property
    def sub_category(self) -> str:
        """Second level grouping."""
        return self.__sub_category

    @sub_category.setter
    def sub_category(self, value: str):
        self._property_changed('sub_category')
        self.__sub_category = value        

    @property
    def methodology(self) -> str:
        """Methodology of dataset."""
        return self.__methodology

    @methodology.setter
    def methodology(self, value: str):
        self._property_changed('methodology')
        self.__methodology = value        

    @property
    def coverage(self) -> str:
        """Coverage of dataset."""
        return self.__coverage

    @coverage.setter
    def coverage(self, value: str):
        self._property_changed('coverage')
        self.__coverage = value        

    @property
    def coverages(self) -> Tuple[Union[AssetType, str], ...]:
        """asset types coverage of dataset."""
        return self.__coverages

    @coverages.setter
    def coverages(self, value: Tuple[Union[AssetType, str], ...]):
        self._property_changed('coverages')
        self.__coverages = value        

    @property
    def notes(self) -> str:
        """Notes of dataset. Corresponds to the 'Frequently Asked Questions' card on the
           Dataset Documentation Page."""
        return self.__notes

    @notes.setter
    def notes(self, value: str):
        self._property_changed('notes')
        self.__notes = value        

    @property
    def history(self) -> str:
        """Deprecated: Used 'historyDate' instead. Period of time covered by dataset."""
        return self.__history

    @history.setter
    def history(self, value: str):
        self._property_changed('history')
        self.__history = value        

    @property
    def sample_start(self) -> datetime.datetime:
        """Used to determine the query start date when loading a sample of the data."""
        return self.__sample_start

    @sample_start.setter
    def sample_start(self, value: datetime.datetime):
        self._property_changed('sample_start')
        self.__sample_start = value        

    @property
    def sample_end(self) -> datetime.datetime:
        """Used to determine the query end date when loading a sample of the data."""
        return self.__sample_end

    @sample_end.setter
    def sample_end(self, value: datetime.datetime):
        self._property_changed('sample_end')
        self.__sample_end = value        

    @property
    def published_date(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__published_date

    @published_date.setter
    def published_date(self, value: datetime.datetime):
        self._property_changed('published_date')
        self.__published_date = value        

    @property
    def history_date(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__history_date

    @history_date.setter
    def history_date(self, value: datetime.datetime):
        self._property_changed('history_date')
        self.__history_date = value        

    @property
    def frequency(self) -> str:
        """Frequency of updates to dataset."""
        return self.__frequency

    @frequency.setter
    def frequency(self, value: str):
        self._property_changed('frequency')
        self.__frequency = value        

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
    def owner_ids(self) -> Tuple[str, ...]:
        """Users who own dataset."""
        return self.__owner_ids

    @owner_ids.setter
    def owner_ids(self, value: Tuple[str, ...]):
        self._property_changed('owner_ids')
        self.__owner_ids = value        

    @property
    def support_ids(self) -> Tuple[str, ...]:
        """Users who support dataset."""
        return self.__support_ids

    @support_ids.setter
    def support_ids(self, value: Tuple[str, ...]):
        self._property_changed('support_ids')
        self.__support_ids = value        

    @property
    def support_distribution_list(self) -> Tuple[str, ...]:
        """Distribution list who support dataset."""
        return self.__support_distribution_list

    @support_distribution_list.setter
    def support_distribution_list(self, value: Tuple[str, ...]):
        self._property_changed('support_distribution_list')
        self.__support_distribution_list = value        

    @property
    def apply_market_data_entitlements(self) -> bool:
        """Whether market data entitlements are checked."""
        return self.__apply_market_data_entitlements

    @apply_market_data_entitlements.setter
    def apply_market_data_entitlements(self, value: bool):
        self._property_changed('apply_market_data_entitlements')
        self.__apply_market_data_entitlements = value        

    @property
    def upload_data_policy(self) -> str:
        """Policy governing uploads."""
        return self.__upload_data_policy

    @upload_data_policy.setter
    def upload_data_policy(self, value: str):
        self._property_changed('upload_data_policy')
        self.__upload_data_policy = value        

    @property
    def logical_db(self) -> str:
        """Database where contents are (to be) stored."""
        return self.__logical_db

    @logical_db.setter
    def logical_db(self, value: str):
        self._property_changed('logical_db')
        self.__logical_db = value        

    @property
    def symbol_strategy(self) -> str:
        """Method for looking up database table name."""
        return self.__symbol_strategy

    @symbol_strategy.setter
    def symbol_strategy(self, value: str):
        self._property_changed('symbol_strategy')
        self.__symbol_strategy = value        

    @property
    def underlying_data_set_id(self) -> str:
        """Dataset on which this (virtual) dataset is based."""
        return self.__underlying_data_set_id

    @underlying_data_set_id.setter
    def underlying_data_set_id(self, value: str):
        self._property_changed('underlying_data_set_id')
        self.__underlying_data_set_id = value        

    @property
    def immutable(self) -> bool:
        """Whether dataset is immutable (i.e. not writable through data service)."""
        return self.__immutable

    @immutable.setter
    def immutable(self, value: bool):
        self._property_changed('immutable')
        self.__immutable = value        

    @property
    def include_in_catalog(self) -> bool:
        """Whether dataset should be in the catalog."""
        return self.__include_in_catalog

    @include_in_catalog.setter
    def include_in_catalog(self, value: bool):
        self._property_changed('include_in_catalog')
        self.__include_in_catalog = value        

    @property
    def coverage_enabled(self) -> bool:
        """Whether coverage requests are available for the DataSet"""
        return self.__coverage_enabled

    @coverage_enabled.setter
    def coverage_enabled(self, value: bool):
        self._property_changed('coverage_enabled')
        self.__coverage_enabled = value        

    @property
    def use_created_time_for_upload(self) -> bool:
        """Whether the dataset uses createdTime to record the time at which the data got
           uploaded."""
        return self.__use_created_time_for_upload

    @use_created_time_for_upload.setter
    def use_created_time_for_upload(self, value: bool):
        self._property_changed('use_created_time_for_upload')
        self.__use_created_time_for_upload = value        

    @property
    def apply_entity_entitlements(self) -> bool:
        """Whether entity level entitlements are applied while querying the dataset and its
           coverage."""
        return self.__apply_entity_entitlements

    @apply_entity_entitlements.setter
    def apply_entity_entitlements(self, value: bool):
        self._property_changed('apply_entity_entitlements')
        self.__apply_entity_entitlements = value        

    @property
    def development_status(self) -> Union[DevelopmentStatus, str]:
        """The status of development of this dataset. Controls rate limit on query/upload."""
        return self.__development_status

    @development_status.setter
    def development_status(self, value: Union[DevelopmentStatus, str]):
        self._property_changed('development_status')
        self.__development_status = get_enum_value(DevelopmentStatus, value)        


class DataSetTransforms(Base):
        
    """Dataset transformation specifiers."""

    @camel_case_translate
    def __init__(
        self,
        redact_columns: Tuple[str, ...] = None,
        round_columns: Tuple[str, ...] = None,
        remap_fields: Tuple[RemapFieldPair, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.redact_columns = redact_columns
        self.round_columns = round_columns
        self.remap_fields = remap_fields
        self.name = name

    @property
    def redact_columns(self) -> Tuple[str, ...]:
        """Redact (exclude) a list of database columns."""
        return self.__redact_columns

    @redact_columns.setter
    def redact_columns(self, value: Tuple[str, ...]):
        self._property_changed('redact_columns')
        self.__redact_columns = value        

    @property
    def round_columns(self) -> Tuple[str, ...]:
        """Rounds list of database columns."""
        return self.__round_columns

    @round_columns.setter
    def round_columns(self, value: Tuple[str, ...]):
        self._property_changed('round_columns')
        self.__round_columns = value        

    @property
    def remap_fields(self) -> Tuple[RemapFieldPair, ...]:
        """Remaps a list of output fields to a different list of fields."""
        return self.__remap_fields

    @remap_fields.setter
    def remap_fields(self, value: Tuple[RemapFieldPair, ...]):
        self._property_changed('remap_fields')
        self.__remap_fields = value        


class FieldFilterMapDataQuery(Base):
        
    """Filters on data fields."""

    @camel_case_translate
    def __init__(
        self,
        name: str = None
    ):        
        super().__init__()
        self.name = name


class FieldLink(Base):
        
    """Link the dataset field to an entity to also fetch its fields. It has two
       mutually exclusive modes of operation: prefixing or explicit inclusion
       entity fields."""

    @camel_case_translate
    def __init__(
        self,
        entity_identifier: str = None,
        prefix: str = None,
        additional_entity_fields: Tuple[FieldLinkSelector, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.entity_identifier = entity_identifier
        self.prefix = prefix
        self.additional_entity_fields = additional_entity_fields
        self.name = name

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
        self._property_changed('entity_identifier')
        self.__entity_identifier = value        

    @property
    def prefix(self) -> str:
        """Prefix to put before the fields fetched from the linked entity (must be unique
           for each dataset field). Prefix cannot be applied with
           additionalEntityFields."""
        return self.__prefix

    @prefix.setter
    def prefix(self, value: str):
        self._property_changed('prefix')
        self.__prefix = value        

    @property
    def additional_entity_fields(self) -> Tuple[FieldLinkSelector, ...]:
        """List of fields from the linked entity to include. It cannot be applied with
           prefix"""
        return self.__additional_entity_fields

    @additional_entity_fields.setter
    def additional_entity_fields(self, value: Tuple[FieldLinkSelector, ...]):
        self._property_changed('additional_entity_fields')
        self.__additional_entity_fields = value        


class MarketDataMapping(Base):
        
    @camel_case_translate
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
        kpi_entity: MeasureKpi = None,
        multi_measure: bool = None,
        name: str = None
    ):        
        super().__init__()
        self.asset_class = asset_class
        self.query_type = query_type
        self.description = description
        self.scale = scale
        self.frequency = frequency
        self.measures = measures
        self.data_set = data_set
        self.vendor = vendor
        self.fields = fields
        self.rank = rank
        self.filtered_fields = filtered_fields
        self.asset_types = asset_types
        self.entity_type = entity_type
        self.backtest_entity = backtest_entity
        self.kpi_entity = kpi_entity
        self.multi_measure = multi_measure
        self.name = name

    @property
    def asset_class(self) -> Union[AssetClass, str]:
        """Asset class that is applicable for mapping."""
        return self.__asset_class

    @asset_class.setter
    def asset_class(self, value: Union[AssetClass, str]):
        self._property_changed('asset_class')
        self.__asset_class = get_enum_value(AssetClass, value)        

    @property
    def query_type(self) -> str:
        """Market data query type."""
        return self.__query_type

    @query_type.setter
    def query_type(self, value: str):
        self._property_changed('query_type')
        self.__query_type = value        

    @property
    def description(self) -> str:
        """Query type description"""
        return self.__description

    @description.setter
    def description(self, value: str):
        self._property_changed('description')
        self.__description = value        

    @property
    def scale(self) -> float:
        """Scale multiplier for time series"""
        return self.__scale

    @scale.setter
    def scale(self, value: float):
        self._property_changed('scale')
        self.__scale = value        

    @property
    def frequency(self) -> Union[MarketDataFrequency, str]:
        return self.__frequency

    @frequency.setter
    def frequency(self, value: Union[MarketDataFrequency, str]):
        self._property_changed('frequency')
        self.__frequency = get_enum_value(MarketDataFrequency, value)        

    @property
    def measures(self) -> Tuple[Union[MarketDataMeasure, str], ...]:
        return self.__measures

    @measures.setter
    def measures(self, value: Tuple[Union[MarketDataMeasure, str], ...]):
        self._property_changed('measures')
        self.__measures = value        

    @property
    def data_set(self) -> str:
        """Marquee unique identifier"""
        return self.__data_set

    @data_set.setter
    def data_set(self, value: str):
        self._property_changed('data_set')
        self.__data_set = value        

    @property
    def vendor(self) -> Union[MarketDataVendor, str]:
        return self.__vendor

    @vendor.setter
    def vendor(self, value: Union[MarketDataVendor, str]):
        self._property_changed('vendor')
        self.__vendor = get_enum_value(MarketDataVendor, value)        

    @property
    def fields(self) -> Tuple[MarketDataField, ...]:
        return self.__fields

    @fields.setter
    def fields(self, value: Tuple[MarketDataField, ...]):
        self._property_changed('fields')
        self.__fields = value        

    @property
    def rank(self) -> float:
        return self.__rank

    @rank.setter
    def rank(self, value: float):
        self._property_changed('rank')
        self.__rank = value        

    @property
    def filtered_fields(self) -> Tuple[MarketDataFilteredField, ...]:
        return self.__filtered_fields

    @filtered_fields.setter
    def filtered_fields(self, value: Tuple[MarketDataFilteredField, ...]):
        self._property_changed('filtered_fields')
        self.__filtered_fields = value        

    @property
    def asset_types(self) -> Tuple[Union[AssetType, str], ...]:
        """Asset type differentiates the product categorization or contract type"""
        return self.__asset_types

    @asset_types.setter
    def asset_types(self, value: Tuple[Union[AssetType, str], ...]):
        self._property_changed('asset_types')
        self.__asset_types = value        

    @property
    def entity_type(self) -> Union[MeasureEntityType, str]:
        """Entity type associated with a measure."""
        return self.__entity_type

    @entity_type.setter
    def entity_type(self, value: Union[MeasureEntityType, str]):
        self._property_changed('entity_type')
        self.__entity_type = get_enum_value(MeasureEntityType, value)        

    @property
    def backtest_entity(self) -> MeasureBacktest:
        """Describes backtests that should be associated with a measure."""
        return self.__backtest_entity

    @backtest_entity.setter
    def backtest_entity(self, value: MeasureBacktest):
        self._property_changed('backtest_entity')
        self.__backtest_entity = value        

    @property
    def kpi_entity(self) -> MeasureKpi:
        """Describes KPIs that should be associated with a measure."""
        return self.__kpi_entity

    @kpi_entity.setter
    def kpi_entity(self, value: MeasureKpi):
        self._property_changed('kpi_entity')
        self.__kpi_entity = value        

    @property
    def multi_measure(self) -> bool:
        return self.__multi_measure

    @multi_measure.setter
    def multi_measure(self, value: bool):
        self._property_changed('multi_measure')
        self.__multi_measure = value        


class ProcessorEntity(Base):
        
    """Query processors for dataset."""

    @camel_case_translate
    def __init__(
        self,
        filters: Tuple[str, ...] = None,
        parsers: Tuple[ParserEntity, ...] = None,
        deduplicate: Tuple[str, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.filters = filters
        self.parsers = parsers
        self.deduplicate = deduplicate
        self.name = name

    @property
    def filters(self) -> Tuple[str, ...]:
        """List of filter processors."""
        return self.__filters

    @filters.setter
    def filters(self, value: Tuple[str, ...]):
        self._property_changed('filters')
        self.__filters = value        

    @property
    def parsers(self) -> Tuple[ParserEntity, ...]:
        """List of parser processors."""
        return self.__parsers

    @parsers.setter
    def parsers(self, value: Tuple[ParserEntity, ...]):
        self._property_changed('parsers')
        self.__parsers = value        

    @property
    def deduplicate(self) -> Tuple[str, ...]:
        """Columns on which a deduplication processor should be run."""
        return self.__deduplicate

    @deduplicate.setter
    def deduplicate(self, value: Tuple[str, ...]):
        self._property_changed('deduplicate')
        self.__deduplicate = value        


class SymbolFilterDimension(Base):
        
    """Map the dataset field with an entity for filtering arctic symbols."""

    @camel_case_translate
    def __init__(
        self,
        field: str = None,
        field_description: str = None,
        symbol_filter_link: SymbolFilterLink = None,
        name: str = None
    ):        
        super().__init__()
        self.field = field
        self.field_description = field_description
        self.symbol_filter_link = symbol_filter_link
        self.name = name

    @property
    def field(self) -> str:
        """Field name."""
        return self.__field

    @field.setter
    def field(self, value: str):
        self._property_changed('field')
        self.__field = value        

    @property
    def field_description(self) -> str:
        """Custom description (overrides field default)."""
        return self.__field_description

    @field_description.setter
    def field_description(self, value: str):
        self._property_changed('field_description')
        self.__field_description = value        

    @property
    def symbol_filter_link(self) -> SymbolFilterLink:
        """The entity type and field used to filter symbols."""
        return self.__symbol_filter_link

    @symbol_filter_link.setter
    def symbol_filter_link(self, value: SymbolFilterLink):
        self._property_changed('symbol_filter_link')
        self.__symbol_filter_link = value        


class ComplexFilter(Base):
        
    """A compound filter for data requests."""

    @camel_case_translate
    def __init__(
        self,
        operator: str,
        simple_filters: Tuple[DataFilter, ...],
        name: str = None
    ):        
        super().__init__()
        self.operator = operator
        self.simple_filters = simple_filters
        self.name = name

    @property
    def operator(self) -> str:
        return self.__operator

    @operator.setter
    def operator(self, value: str):
        self._property_changed('operator')
        self.__operator = value        

    @property
    def simple_filters(self) -> Tuple[DataFilter, ...]:
        """Filter on specified field."""
        return self.__simple_filters

    @simple_filters.setter
    def simple_filters(self, value: Tuple[DataFilter, ...]):
        self._property_changed('simple_filters')
        self.__simple_filters = value        


class DataGroup(Base):
        
    """Dataset grouped by context (key dimensions)"""

    @camel_case_translate
    def __init__(
        self,
        context: FieldValueMap = None,
        data: Tuple[FieldValueMap, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.context = context
        self.data = data
        self.name = name

    @property
    def context(self) -> FieldValueMap:
        """Context map for the grouped data (key dimensions)"""
        return self.__context

    @context.setter
    def context(self, value: FieldValueMap):
        self._property_changed('context')
        self.__context = value        

    @property
    def data(self) -> Tuple[FieldValueMap, ...]:
        """Array of grouped data objects"""
        return self.__data

    @data.setter
    def data(self, value: Tuple[FieldValueMap, ...]):
        self._property_changed('data')
        self.__data = value        


class DataQuery(Base):
        
    @camel_case_translate
    def __init__(
        self,
        id_: str = None,
        data_set_id: str = None,
        format_: Union[Format, str] = None,
        where: FieldFilterMapDataQuery = None,
        vendor: Union[MarketDataVendor, str] = None,
        start_date: datetime.date = None,
        end_date: datetime.date = None,
        start_time: datetime.datetime = None,
        page: int = None,
        page_size: int = None,
        end_time: datetime.datetime = None,
        relative_start_date: str = None,
        relative_end_date: str = None,
        as_of_time: datetime.datetime = None,
        id_as_of_date: datetime.date = None,
        use_temporal_x_ref: bool = False,
        restrict_secondary_identifier: bool = False,
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
        restrict_fields: bool = False,
        entity_filter: FieldFilterMapDataQuery = None,
        interval: str = None,
        distinct_consecutive: bool = False,
        time_filter: TimeFilter = None,
        use_field_alias: bool = False,
        remap_schema_to_alias: bool = False,
        show_linked_dimensions: bool = True,
        use_project_processor: bool = False,
        name: str = None
    ):        
        super().__init__()
        self.__id = id_
        self.data_set_id = data_set_id
        self.__format = get_enum_value(Format, format_)
        self.where = where
        self.vendor = vendor
        self.start_date = start_date
        self.end_date = end_date
        self.start_time = start_time
        self.page = page
        self.page_size = page_size
        self.end_time = end_time
        self.relative_start_date = relative_start_date
        self.relative_end_date = relative_end_date
        self.as_of_time = as_of_time
        self.id_as_of_date = id_as_of_date
        self.use_temporal_x_ref = use_temporal_x_ref
        self.restrict_secondary_identifier = restrict_secondary_identifier
        self.since = since
        self.dates = dates
        self.times = times
        self.delay = delay
        self.intervals = intervals
        self.samples = samples
        self.limit = limit
        self.polling_interval = polling_interval
        self.grouped = grouped
        self.fields = fields
        self.restrict_fields = restrict_fields
        self.entity_filter = entity_filter
        self.interval = interval
        self.distinct_consecutive = distinct_consecutive
        self.time_filter = time_filter
        self.use_field_alias = use_field_alias
        self.remap_schema_to_alias = remap_schema_to_alias
        self.show_linked_dimensions = show_linked_dimensions
        self.use_project_processor = use_project_processor
        self.name = name

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def data_set_id(self) -> str:
        """Marquee unique identifier"""
        return self.__data_set_id

    @data_set_id.setter
    def data_set_id(self, value: str):
        self._property_changed('data_set_id')
        self.__data_set_id = value        

    @property
    def format(self) -> Union[Format, str]:
        """Alternative format for data to be returned in"""
        return self.__format

    @format.setter
    def format(self, value: Union[Format, str]):
        self._property_changed('format')
        self.__format = get_enum_value(Format, value)        

    @property
    def where(self) -> FieldFilterMapDataQuery:
        """Filters on data fields."""
        return self.__where

    @where.setter
    def where(self, value: FieldFilterMapDataQuery):
        self._property_changed('where')
        self.__where = value        

    @property
    def vendor(self) -> Union[MarketDataVendor, str]:
        return self.__vendor

    @vendor.setter
    def vendor(self, value: Union[MarketDataVendor, str]):
        self._property_changed('vendor')
        self.__vendor = get_enum_value(MarketDataVendor, value)        

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
    def start_time(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__start_time

    @start_time.setter
    def start_time(self, value: datetime.datetime):
        self._property_changed('start_time')
        self.__start_time = value        

    @property
    def page(self) -> int:
        """Number of symbols page to fetch."""
        return self.__page

    @page.setter
    def page(self, value: int):
        self._property_changed('page')
        self.__page = value        

    @property
    def page_size(self) -> int:
        """Number of how many symbols can be single page contain"""
        return self.__page_size

    @page_size.setter
    def page_size(self, value: int):
        self._property_changed('page_size')
        self.__page_size = value        

    @property
    def end_time(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__end_time

    @end_time.setter
    def end_time(self, value: datetime.datetime):
        self._property_changed('end_time')
        self.__end_time = value        

    @property
    def relative_start_date(self) -> str:
        """Number of days, weeks, months or years relative from today.  Max input number is
           99."""
        return self.__relative_start_date

    @relative_start_date.setter
    def relative_start_date(self, value: str):
        self._property_changed('relative_start_date')
        self.__relative_start_date = value        

    @property
    def relative_end_date(self) -> str:
        """Number of days, weeks, months or years relative from today.  Max input number is
           99."""
        return self.__relative_end_date

    @relative_end_date.setter
    def relative_end_date(self, value: str):
        self._property_changed('relative_end_date')
        self.__relative_end_date = value        

    @property
    def as_of_time(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__as_of_time

    @as_of_time.setter
    def as_of_time(self, value: datetime.datetime):
        self._property_changed('as_of_time')
        self.__as_of_time = value        

    @property
    def id_as_of_date(self) -> datetime.date:
        """If secondary identifiers are specified, find corresponding assets as of this
           date"""
        return self.__id_as_of_date

    @id_as_of_date.setter
    def id_as_of_date(self, value: datetime.date):
        self._property_changed('id_as_of_date')
        self.__id_as_of_date = value        

    @property
    def use_temporal_x_ref(self) -> bool:
        """Set to true when xrefs provided in the query should be treated in a temporal way
           (e.g. get data points which had a certain BCID at some point in time,
           not which currently have it)."""
        return self.__use_temporal_x_ref

    @use_temporal_x_ref.setter
    def use_temporal_x_ref(self, value: bool):
        self._property_changed('use_temporal_x_ref')
        self.__use_temporal_x_ref = value        

    @property
    def restrict_secondary_identifier(self) -> bool:
        """A secondary identifier is an identifier that maps to the primary symbol on the
           dataset. When 'TRUE', a data query filters the time series to the
           queried symbol's secondary identifier continuous history till now.
           Otherwise it returns full time series."""
        return self.__restrict_secondary_identifier

    @restrict_secondary_identifier.setter
    def restrict_secondary_identifier(self, value: bool):
        self._property_changed('restrict_secondary_identifier')
        self.__restrict_secondary_identifier = value        

    @property
    def since(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__since

    @since.setter
    def since(self, value: datetime.datetime):
        self._property_changed('since')
        self.__since = value        

    @property
    def dates(self) -> Tuple[datetime.date, ...]:
        """Select and return specific dates from dataset query results."""
        return self.__dates

    @dates.setter
    def dates(self, value: Tuple[datetime.date, ...]):
        self._property_changed('dates')
        self.__dates = value        

    @property
    def times(self) -> Tuple[datetime.datetime, ...]:
        """Select and return specific times from dataset query results."""
        return self.__times

    @times.setter
    def times(self, value: Tuple[datetime.datetime, ...]):
        self._property_changed('times')
        self.__times = value        

    @property
    def delay(self) -> int:
        """Number of minutes to delay returning data."""
        return self.__delay

    @delay.setter
    def delay(self, value: int):
        self._property_changed('delay')
        self.__delay = value        

    @property
    def intervals(self) -> int:
        """Number of intervals for which to return output times, for example if 10, it will
           return 10 data points evenly spaced over the time/date range."""
        return self.__intervals

    @intervals.setter
    def intervals(self, value: int):
        self._property_changed('intervals')
        self.__intervals = value        

    @property
    def samples(self) -> int:
        """Number of points to down sample the data, for example if 10, it will return at
           most 10 sample data points evenly spaced over the time/date range"""
        return self.__samples

    @samples.setter
    def samples(self, value: int):
        self._property_changed('samples')
        self.__samples = value        

    @property
    def limit(self) -> int:
        """Maximum number of rows for each asset to return."""
        return self.__limit

    @limit.setter
    def limit(self, value: int):
        self._property_changed('limit')
        self.__limit = value        

    @property
    def polling_interval(self) -> int:
        """When streaming, wait for this number of seconds between poll attempts."""
        return self.__polling_interval

    @polling_interval.setter
    def polling_interval(self, value: int):
        self._property_changed('polling_interval')
        self.__polling_interval = value        

    @property
    def grouped(self) -> bool:
        """Set to true to return results grouped by a given context (set of dimensions)."""
        return self.__grouped

    @grouped.setter
    def grouped(self, value: bool):
        self._property_changed('grouped')
        self.__grouped = value        

    @property
    def fields(self) -> Tuple[Union[dict, str], ...]:
        """Fields to be returned."""
        return self.__fields

    @fields.setter
    def fields(self, value: Tuple[Union[dict, str], ...]):
        self._property_changed('fields')
        self.__fields = value        

    @property
    def restrict_fields(self) -> bool:
        """Whether to return only the fields which are requested and suppress every other
           field"""
        return self.__restrict_fields

    @restrict_fields.setter
    def restrict_fields(self, value: bool):
        self._property_changed('restrict_fields')
        self.__restrict_fields = value        

    @property
    def entity_filter(self) -> FieldFilterMapDataQuery:
        """Filters that are applied only to entities i.e Asset. It is used for querying by
           asset parameters to return data for assets matching a certain
           criteria i.e floatingRateOption = LIBOR."""
        return self.__entity_filter

    @entity_filter.setter
    def entity_filter(self, value: FieldFilterMapDataQuery):
        self._property_changed('entity_filter')
        self.__entity_filter = value        

    @property
    def interval(self) -> str:
        """Interval to use when returning data. E.g. 1s, 1m, 1h, 1d. Only seconds(s),
           minutes(m), hours(h) and days(d) are supported."""
        return self.__interval

    @interval.setter
    def interval(self, value: str):
        self._property_changed('interval')
        self.__interval = value        

    @property
    def distinct_consecutive(self) -> bool:
        """enable removing consecutive duplicates"""
        return self.__distinct_consecutive

    @distinct_consecutive.setter
    def distinct_consecutive(self, value: bool):
        self._property_changed('distinct_consecutive')
        self.__distinct_consecutive = value        

    @property
    def time_filter(self) -> TimeFilter:
        """Filter to restrict data to a range of hours per day."""
        return self.__time_filter

    @time_filter.setter
    def time_filter(self, value: TimeFilter):
        self._property_changed('time_filter')
        self.__time_filter = value        

    @property
    def use_field_alias(self) -> bool:
        """Whether to use field alias in the query."""
        return self.__use_field_alias

    @use_field_alias.setter
    def use_field_alias(self, value: bool):
        self._property_changed('use_field_alias')
        self.__use_field_alias = value        

    @property
    def remap_schema_to_alias(self) -> bool:
        """Whether to remap the schema of the output data to field aliases, if aliases have
           been used to query the data"""
        return self.__remap_schema_to_alias

    @remap_schema_to_alias.setter
    def remap_schema_to_alias(self, value: bool):
        self._property_changed('remap_schema_to_alias')
        self.__remap_schema_to_alias = value        

    @property
    def show_linked_dimensions(self) -> bool:
        """Whether to show linked dimensions in query response"""
        return self.__show_linked_dimensions

    @show_linked_dimensions.setter
    def show_linked_dimensions(self, value: bool):
        self._property_changed('show_linked_dimensions')
        self.__show_linked_dimensions = value        

    @property
    def use_project_processor(self) -> bool:
        """Whether to use project processor for projecting the fields in the query."""
        return self.__use_project_processor

    @use_project_processor.setter
    def use_project_processor(self, value: bool):
        self._property_changed('use_project_processor')
        self.__use_project_processor = value        


class DataSetFieldEntity(Base):
        
    """Decorator object on com.gs.marquee.api.the field to allow fields to be written
       to Elastic."""

    @camel_case_translate
    def __init__(
        self,
        name: str,
        description: str,
        type_: str,
        id_: str = None,
        classifications: DataSetFieldEntityClassifications = None,
        unique: bool = False,
        field_java_type: str = None,
        parameters: dict = None,
        entitlements: Entitlements = None,
        metadata: EntityMetadata = None,
        attributes: DataSetFieldEntityAttributes = None
    ):        
        super().__init__()
        self.__id = id_
        self.name = name
        self.description = description
        self.__type = type_
        self.classifications = classifications
        self.unique = unique
        self.field_java_type = field_java_type
        self.parameters = parameters
        self.entitlements = entitlements
        self.metadata = metadata
        self.attributes = attributes

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def name(self) -> str:
        """Name of the field in camelCase."""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def description(self) -> str:
        """Description of the field."""
        return self.__description

    @description.setter
    def description(self, value: str):
        self._property_changed('description')
        self.__description = value        

    @property
    def type(self) -> str:
        """Type of the field."""
        return self.__type

    @type.setter
    def type(self, value: str):
        self._property_changed('type')
        self.__type = value        

    @property
    def classifications(self) -> DataSetFieldEntityClassifications:
        """Classifications for a Field Entity."""
        return self.__classifications

    @classifications.setter
    def classifications(self, value: DataSetFieldEntityClassifications):
        self._property_changed('classifications')
        self.__classifications = value        

    @property
    def unique(self) -> bool:
        """If 'TRUE', only one field with this name exists."""
        return self.__unique

    @unique.setter
    def unique(self, value: bool):
        self._property_changed('unique')
        self.__unique = value        

    @property
    def field_java_type(self) -> str:
        """For advanced users to specify the Java Class of the field as the service reads
           it. Otherwise, the service assumes some default based on the field
           'type'."""
        return self.__field_java_type

    @field_java_type.setter
    def field_java_type(self, value: str):
        self._property_changed('field_java_type')
        self.__field_java_type = value        

    @property
    def parameters(self) -> dict:
        """Parameters for the field."""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: dict):
        self._property_changed('parameters')
        self.__parameters = value        

    @property
    def entitlements(self) -> Entitlements:
        """Defines the entitlements of a given resource."""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self._property_changed('entitlements')
        self.__entitlements = value        

    @property
    def metadata(self) -> EntityMetadata:
        """Contains read-only metadata for internal users to view."""
        return self.__metadata

    @metadata.setter
    def metadata(self, value: EntityMetadata):
        self._property_changed('metadata')
        self.__metadata = value        

    @property
    def attributes(self) -> DataSetFieldEntityAttributes:
        """Read-only attributes of the field. Useful for searching."""
        return self.__attributes

    @attributes.setter
    def attributes(self, value: DataSetFieldEntityAttributes):
        self._property_changed('attributes')
        self.__attributes = value        


class DataSetTransformation(Base):
        
    """Transform the Dataset output. Can be used with or without certain conditions."""

    @camel_case_translate
    def __init__(
        self,
        transforms: DataSetTransforms,
        condition: DataSetCondition = None,
        name: str = None
    ):        
        super().__init__()
        self.condition = condition
        self.transforms = transforms
        self.name = name

    @property
    def condition(self) -> DataSetCondition:
        """Condition to match before applying the transformations."""
        return self.__condition

    @condition.setter
    def condition(self, value: DataSetCondition):
        self._property_changed('condition')
        self.__condition = value        

    @property
    def transforms(self) -> DataSetTransforms:
        """Series of transformation actions to perform."""
        return self.__transforms

    @transforms.setter
    def transforms(self, value: DataSetTransforms):
        self._property_changed('transforms')
        self.__transforms = value        


class DeleteCoverageQuery(Base):
        
    @camel_case_translate
    def __init__(
        self,
        where: FieldFilterMapDataQuery = None,
        delete_all: bool = False,
        name: str = None
    ):        
        super().__init__()
        self.where = where
        self.delete_all = delete_all
        self.name = name

    @property
    def where(self) -> FieldFilterMapDataQuery:
        """Filters on data fields."""
        return self.__where

    @where.setter
    def where(self, value: FieldFilterMapDataQuery):
        self._property_changed('where')
        self.__where = value        

    @property
    def delete_all(self) -> bool:
        return self.__delete_all

    @delete_all.setter
    def delete_all(self, value: bool):
        self._property_changed('delete_all')
        self.__delete_all = value        


class FieldColumnPair(Base):
        
    """Map from fields to database columns."""

    @camel_case_translate
    def __init__(
        self,
        field: str = None,
        column: str = None,
        field_description: str = None,
        link: FieldLink = None,
        aliases: Tuple[str, ...] = None,
        resolvable: bool = None,
        name: str = None
    ):        
        super().__init__()
        self.field = field
        self.column = column
        self.field_description = field_description
        self.link = link
        self.aliases = aliases
        self.resolvable = resolvable
        self.name = name

    @property
    def field(self) -> str:
        """Field name."""
        return self.__field

    @field.setter
    def field(self, value: str):
        self._property_changed('field')
        self.__field = value        

    @property
    def column(self) -> str:
        """Database column name."""
        return self.__column

    @column.setter
    def column(self, value: str):
        self._property_changed('column')
        self.__column = value        

    @property
    def field_description(self) -> str:
        """Custom description (overrides field default)."""
        return self.__field_description

    @field_description.setter
    def field_description(self, value: str):
        self._property_changed('field_description')
        self.__field_description = value        

    @property
    def link(self) -> FieldLink:
        """Link the field with other entity to also fetch its fields."""
        return self.__link

    @link.setter
    def link(self, value: FieldLink):
        self._property_changed('link')
        self.__link = value        

    @property
    def aliases(self) -> Tuple[str, ...]:
        """Set of alias fields that can be used to refer to the current field when
           querying."""
        return self.__aliases

    @aliases.setter
    def aliases(self, value: Tuple[str, ...]):
        self._property_changed('aliases')
        self.__aliases = value        

    @property
    def resolvable(self) -> bool:
        """Whether this field is resolvable in the measure service."""
        return self.__resolvable

    @resolvable.setter
    def resolvable(self, value: bool):
        self._property_changed('resolvable')
        self.__resolvable = value        


class HistoryFilter(Base):
        
    """Restricts queries against dataset to a time range."""

    @camel_case_translate
    def __init__(
        self,
        absolute_start: datetime.datetime = None,
        absolute_end: datetime.datetime = None,
        relative_start_seconds: float = None,
        relative_end_seconds: float = None,
        delay: dict = None,
        name: str = None
    ):        
        super().__init__()
        self.absolute_start = absolute_start
        self.absolute_end = absolute_end
        self.relative_start_seconds = relative_start_seconds
        self.relative_end_seconds = relative_end_seconds
        self.delay = delay
        self.name = name

    @property
    def absolute_start(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__absolute_start

    @absolute_start.setter
    def absolute_start(self, value: datetime.datetime):
        self._property_changed('absolute_start')
        self.__absolute_start = value        

    @property
    def absolute_end(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__absolute_end

    @absolute_end.setter
    def absolute_end(self, value: datetime.datetime):
        self._property_changed('absolute_end')
        self.__absolute_end = value        

    @property
    def relative_start_seconds(self) -> float:
        """Earliest start time in seconds before current time."""
        return self.__relative_start_seconds

    @relative_start_seconds.setter
    def relative_start_seconds(self, value: float):
        self._property_changed('relative_start_seconds')
        self.__relative_start_seconds = value        

    @property
    def relative_end_seconds(self) -> float:
        """Latest end time in seconds before current time."""
        return self.__relative_end_seconds

    @relative_end_seconds.setter
    def relative_end_seconds(self, value: float):
        self._property_changed('relative_end_seconds')
        self.__relative_end_seconds = value        

    @property
    def delay(self) -> dict:
        return self.__delay

    @delay.setter
    def delay(self, value: dict):
        self._property_changed('delay')
        self.__delay = value        


class DataQueryResponse(Base):
        
    @camel_case_translate
    def __init__(
        self,
        type_: str,
        request_id: str = None,
        error_message: str = None,
        id_: str = None,
        total_pages: int = None,
        data_set_id: str = None,
        entity_type: Union[MeasureEntityType, str] = None,
        delay: int = None,
        data: Tuple[FieldValueMap, ...] = None,
        groups: Tuple[DataGroup, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.request_id = request_id
        self.__type = type_
        self.error_message = error_message
        self.__id = id_
        self.total_pages = total_pages
        self.data_set_id = data_set_id
        self.entity_type = entity_type
        self.delay = delay
        self.data = data
        self.groups = groups
        self.name = name

    @property
    def request_id(self) -> str:
        """Marquee unique identifier"""
        return self.__request_id

    @request_id.setter
    def request_id(self, value: str):
        self._property_changed('request_id')
        self.__request_id = value        

    @property
    def type(self) -> str:
        return self.__type

    @type.setter
    def type(self, value: str):
        self._property_changed('type')
        self.__type = value        

    @property
    def error_message(self) -> str:
        return self.__error_message

    @error_message.setter
    def error_message(self, value: str):
        self._property_changed('error_message')
        self.__error_message = value        

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def total_pages(self) -> int:
        """Number of total symbol pages"""
        return self.__total_pages

    @total_pages.setter
    def total_pages(self, value: int):
        self._property_changed('total_pages')
        self.__total_pages = value        

    @property
    def data_set_id(self) -> str:
        """Unique id of dataset."""
        return self.__data_set_id

    @data_set_id.setter
    def data_set_id(self, value: str):
        self._property_changed('data_set_id')
        self.__data_set_id = value        

    @property
    def entity_type(self) -> Union[MeasureEntityType, str]:
        """Entity type associated with a measure."""
        return self.__entity_type

    @entity_type.setter
    def entity_type(self, value: Union[MeasureEntityType, str]):
        self._property_changed('entity_type')
        self.__entity_type = get_enum_value(MeasureEntityType, value)        

    @property
    def delay(self) -> int:
        return self.__delay

    @delay.setter
    def delay(self, value: int):
        self._property_changed('delay')
        self.__delay = value        

    @property
    def data(self) -> Tuple[FieldValueMap, ...]:
        """Array of data elements from dataset"""
        return self.__data

    @data.setter
    def data(self, value: Tuple[FieldValueMap, ...]):
        self._property_changed('data')
        self.__data = value        

    @property
    def groups(self) -> Tuple[DataGroup, ...]:
        """If the data is requested in grouped mode, will return data group object"""
        return self.__groups

    @groups.setter
    def groups(self, value: Tuple[DataGroup, ...]):
        self._property_changed('groups')
        self.__groups = value        


class DataSetDimensions(Base):
        
    """Dataset dimensions."""

    @camel_case_translate
    def __init__(
        self,
        symbol_dimensions: Tuple[str, ...],
        time_field: str = None,
        transaction_time_field: str = None,
        symbol_dimension_properties: Tuple[FieldColumnPair, ...] = None,
        non_symbol_dimensions: Tuple[FieldColumnPair, ...] = None,
        symbol_dimension_link: FieldLink = None,
        linked_dimensions: Tuple[FieldLinkSelector, ...] = None,
        symbol_filter_dimensions: Tuple[SymbolFilterDimension, ...] = None,
        key_dimensions: Tuple[str, ...] = None,
        measures: Tuple[FieldColumnPair, ...] = None,
        entity_dimension: str = None,
        name: str = None
    ):        
        super().__init__()
        self.time_field = time_field
        self.transaction_time_field = transaction_time_field
        self.symbol_dimensions = symbol_dimensions
        self.symbol_dimension_properties = symbol_dimension_properties
        self.non_symbol_dimensions = non_symbol_dimensions
        self.symbol_dimension_link = symbol_dimension_link
        self.linked_dimensions = linked_dimensions
        self.symbol_filter_dimensions = symbol_filter_dimensions
        self.key_dimensions = key_dimensions
        self.measures = measures
        self.entity_dimension = entity_dimension
        self.name = name

    @property
    def time_field(self) -> str:
        return self.__time_field

    @time_field.setter
    def time_field(self, value: str):
        self._property_changed('time_field')
        self.__time_field = value        

    @property
    def transaction_time_field(self) -> str:
        """For bi-temporal datasets, field for capturing the time at which a data point was
           updated."""
        return self.__transaction_time_field

    @transaction_time_field.setter
    def transaction_time_field(self, value: str):
        self._property_changed('transaction_time_field')
        self.__transaction_time_field = value        

    @property
    def symbol_dimensions(self) -> Tuple[str, ...]:
        """Set of fields that determine database table name."""
        return self.__symbol_dimensions

    @symbol_dimensions.setter
    def symbol_dimensions(self, value: Tuple[str, ...]):
        self._property_changed('symbol_dimensions')
        self.__symbol_dimensions = value        

    @property
    def symbol_dimension_properties(self) -> Tuple[FieldColumnPair, ...]:
        """Additional properties for symbol dimensions."""
        return self.__symbol_dimension_properties

    @symbol_dimension_properties.setter
    def symbol_dimension_properties(self, value: Tuple[FieldColumnPair, ...]):
        self._property_changed('symbol_dimension_properties')
        self.__symbol_dimension_properties = value        

    @property
    def non_symbol_dimensions(self) -> Tuple[FieldColumnPair, ...]:
        """Fields that are not nullable."""
        return self.__non_symbol_dimensions

    @non_symbol_dimensions.setter
    def non_symbol_dimensions(self, value: Tuple[FieldColumnPair, ...]):
        self._property_changed('non_symbol_dimensions')
        self.__non_symbol_dimensions = value        

    @property
    def symbol_dimension_link(self) -> FieldLink:
        """Deprecated - use linkedDimensions."""
        return self.__symbol_dimension_link

    @symbol_dimension_link.setter
    def symbol_dimension_link(self, value: FieldLink):
        self._property_changed('symbol_dimension_link')
        self.__symbol_dimension_link = value        

    @property
    def linked_dimensions(self) -> Tuple[FieldLinkSelector, ...]:
        """Fields that are injected from entity into dataset."""
        return self.__linked_dimensions

    @linked_dimensions.setter
    def linked_dimensions(self, value: Tuple[FieldLinkSelector, ...]):
        self._property_changed('linked_dimensions')
        self.__linked_dimensions = value        

    @property
    def symbol_filter_dimensions(self) -> Tuple[SymbolFilterDimension, ...]:
        """Map the dataset field with an entity for filtering arctic symbols."""
        return self.__symbol_filter_dimensions

    @symbol_filter_dimensions.setter
    def symbol_filter_dimensions(self, value: Tuple[SymbolFilterDimension, ...]):
        self._property_changed('symbol_filter_dimensions')
        self.__symbol_filter_dimensions = value        

    @property
    def key_dimensions(self) -> Tuple[str, ...]:
        """Fields to slice dataset by. Used for query results where same symbolDimension
           has multiple updateTimes."""
        return self.__key_dimensions

    @key_dimensions.setter
    def key_dimensions(self, value: Tuple[str, ...]):
        self._property_changed('key_dimensions')
        self.__key_dimensions = value        

    @property
    def measures(self) -> Tuple[FieldColumnPair, ...]:
        """Fields that are nullable."""
        return self.__measures

    @measures.setter
    def measures(self, value: Tuple[FieldColumnPair, ...]):
        self._property_changed('measures')
        self.__measures = value        

    @property
    def entity_dimension(self) -> str:
        """Symbol dimension that corresponds to a known Marquee Entity. Examples: assetId,
           countryId, portfolioId, reportId."""
        return self.__entity_dimension

    @entity_dimension.setter
    def entity_dimension(self, value: str):
        self._property_changed('entity_dimension')
        self.__entity_dimension = value        


class DataSetFieldEntityBulkRequest(Base):
        
    """Bulk Request object for DataSetFieldEntity"""

    @camel_case_translate
    def __init__(
        self,
        fields: Tuple[DataSetFieldEntity, ...],
        name: str = None
    ):        
        super().__init__()
        self.fields = fields
        self.name = name

    @property
    def fields(self) -> Tuple[DataSetFieldEntity, ...]:
        """Decorator object on com.gs.marquee.api.the field to allow fields to be written
           to Elastic."""
        return self.__fields

    @fields.setter
    def fields(self, value: Tuple[DataSetFieldEntity, ...]):
        self._property_changed('fields')
        self.__fields = value        


class EntityFilter(Base):
        
    """Filter on known Marquee Entities. Examples: assetId, countryId, portfolioId,
       reportId."""

    @camel_case_translate
    def __init__(
        self,
        operator: str = None,
        simple_filters: Tuple[DataFilter, ...] = None,
        complex_filters: Tuple[ComplexFilter, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.operator = operator
        self.simple_filters = simple_filters
        self.complex_filters = complex_filters
        self.name = name

    @property
    def operator(self) -> str:
        return self.__operator

    @operator.setter
    def operator(self, value: str):
        self._property_changed('operator')
        self.__operator = value        

    @property
    def simple_filters(self) -> Tuple[DataFilter, ...]:
        """Filter on specified field."""
        return self.__simple_filters

    @simple_filters.setter
    def simple_filters(self, value: Tuple[DataFilter, ...]):
        self._property_changed('simple_filters')
        self.__simple_filters = value        

    @property
    def complex_filters(self) -> Tuple[ComplexFilter, ...]:
        """A compound filter for data requests."""
        return self.__complex_filters

    @complex_filters.setter
    def complex_filters(self, value: Tuple[ComplexFilter, ...]):
        self._property_changed('complex_filters')
        self.__complex_filters = value        


class DataSetFilters(Base):
        
    """Filters can be applied to restrict data that is returned."""

    @camel_case_translate
    def __init__(
        self,
        entity_filter: EntityFilter = None,
        row_filters: Tuple[DataFilter, ...] = None,
        advanced_filters: Tuple[AdvancedFilter, ...] = None,
        history_filter: HistoryFilter = None,
        time_filter: TimeFilter = None,
        name: str = None
    ):        
        super().__init__()
        self.entity_filter = entity_filter
        self.row_filters = row_filters
        self.advanced_filters = advanced_filters
        self.history_filter = history_filter
        self.time_filter = time_filter
        self.name = name

    @property
    def entity_filter(self) -> EntityFilter:
        """Filter on known Marquee Entities. Examples: assetId, countryId, portfolioId,
           reportId."""
        return self.__entity_filter

    @entity_filter.setter
    def entity_filter(self, value: EntityFilter):
        self._property_changed('entity_filter')
        self.__entity_filter = value        

    @property
    def row_filters(self) -> Tuple[DataFilter, ...]:
        """Filters on database rows."""
        return self.__row_filters

    @row_filters.setter
    def row_filters(self, value: Tuple[DataFilter, ...]):
        self._property_changed('row_filters')
        self.__row_filters = value        

    @property
    def advanced_filters(self) -> Tuple[AdvancedFilter, ...]:
        """Advanced filters for the Dataset."""
        return self.__advanced_filters

    @advanced_filters.setter
    def advanced_filters(self, value: Tuple[AdvancedFilter, ...]):
        self._property_changed('advanced_filters')
        self.__advanced_filters = value        

    @property
    def history_filter(self) -> HistoryFilter:
        """Restricts queries against dataset to a time range."""
        return self.__history_filter

    @history_filter.setter
    def history_filter(self, value: HistoryFilter):
        self._property_changed('history_filter')
        self.__history_filter = value        

    @property
    def time_filter(self) -> TimeFilter:
        """Filter to restrict data to a range of hours per day."""
        return self.__time_filter

    @time_filter.setter
    def time_filter(self, value: TimeFilter):
        self._property_changed('time_filter')
        self.__time_filter = value        


class DataSetEntity(Base):
        
    @camel_case_translate
    def __init__(
        self,
        id_: str,
        name: str,
        description: str = None,
        short_description: str = None,
        mappings: Tuple[MarketDataMapping, ...] = None,
        vendor: Union[MarketDataVendor, str] = None,
        mdapi: MDAPI = None,
        data_product: str = None,
        entitlements: Entitlements = None,
        query_processors: ProcessorEntity = None,
        parameters: DataSetParameters = None,
        dimensions: DataSetDimensions = None,
        coverage_properties: DataSetCoverageProperties = None,
        defaults: DataSetDefaults = None,
        filters: DataSetFilters = None,
        transformations: Tuple[DataSetTransformation, ...] = None,
        created_by_id: str = None,
        created_time: datetime.datetime = None,
        last_updated_by_id: str = None,
        last_updated_time: datetime.datetime = None,
        tags: Tuple[str, ...] = None
    ):        
        super().__init__()
        self.__id = id_
        self.name = name
        self.description = description
        self.short_description = short_description
        self.mappings = mappings
        self.vendor = vendor
        self.mdapi = mdapi
        self.data_product = data_product
        self.entitlements = entitlements
        self.query_processors = query_processors
        self.parameters = parameters
        self.dimensions = dimensions
        self.coverage_properties = coverage_properties
        self.defaults = defaults
        self.filters = filters
        self.transformations = transformations
        self.created_by_id = created_by_id
        self.created_time = created_time
        self.last_updated_by_id = last_updated_by_id
        self.last_updated_time = last_updated_time
        self.tags = tags

    @property
    def id(self) -> str:
        """Unique id of dataset."""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def name(self) -> str:
        """Name of dataset."""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def description(self) -> str:
        """Description of dataset."""
        return self.__description

    @description.setter
    def description(self, value: str):
        self._property_changed('description')
        self.__description = value        

    @property
    def short_description(self) -> str:
        """Short description of dataset."""
        return self.__short_description

    @short_description.setter
    def short_description(self, value: str):
        self._property_changed('short_description')
        self.__short_description = value        

    @property
    def mappings(self) -> Tuple[MarketDataMapping, ...]:
        """Market data mappings."""
        return self.__mappings

    @mappings.setter
    def mappings(self, value: Tuple[MarketDataMapping, ...]):
        self._property_changed('mappings')
        self.__mappings = value        

    @property
    def vendor(self) -> Union[MarketDataVendor, str]:
        return self.__vendor

    @vendor.setter
    def vendor(self, value: Union[MarketDataVendor, str]):
        self._property_changed('vendor')
        self.__vendor = get_enum_value(MarketDataVendor, value)        

    @property
    def mdapi(self) -> MDAPI:
        """Defines MDAPI fields."""
        return self.__mdapi

    @mdapi.setter
    def mdapi(self, value: MDAPI):
        self._property_changed('mdapi')
        self.__mdapi = value        

    @property
    def data_product(self) -> str:
        """Product that dataset belongs to."""
        return self.__data_product

    @data_product.setter
    def data_product(self, value: str):
        self._property_changed('data_product')
        self.__data_product = value        

    @property
    def entitlements(self) -> Entitlements:
        """Defines the entitlements of a given resource."""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self._property_changed('entitlements')
        self.__entitlements = value        

    @property
    def query_processors(self) -> ProcessorEntity:
        """Query processors for dataset."""
        return self.__query_processors

    @query_processors.setter
    def query_processors(self, value: ProcessorEntity):
        self._property_changed('query_processors')
        self.__query_processors = value        

    @property
    def parameters(self) -> DataSetParameters:
        """Dataset parameters."""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: DataSetParameters):
        self._property_changed('parameters')
        self.__parameters = value        

    @property
    def dimensions(self) -> DataSetDimensions:
        """Dataset dimensions."""
        return self.__dimensions

    @dimensions.setter
    def dimensions(self, value: DataSetDimensions):
        self._property_changed('dimensions')
        self.__dimensions = value        

    @property
    def coverage_properties(self) -> DataSetCoverageProperties:
        """Dataset coverage properties."""
        return self.__coverage_properties

    @coverage_properties.setter
    def coverage_properties(self, value: DataSetCoverageProperties):
        self._property_changed('coverage_properties')
        self.__coverage_properties = value        

    @property
    def defaults(self) -> DataSetDefaults:
        """Default start/end dates/times applied when data is queried, if not specified by
           user."""
        return self.__defaults

    @defaults.setter
    def defaults(self, value: DataSetDefaults):
        self._property_changed('defaults')
        self.__defaults = value        

    @property
    def filters(self) -> DataSetFilters:
        """Filters can be applied to restrict data that is returned."""
        return self.__filters

    @filters.setter
    def filters(self, value: DataSetFilters):
        self._property_changed('filters')
        self.__filters = value        

    @property
    def transformations(self) -> Tuple[DataSetTransformation, ...]:
        """Transformations that can be applied on the output data."""
        return self.__transformations

    @transformations.setter
    def transformations(self, value: Tuple[DataSetTransformation, ...]):
        self._property_changed('transformations')
        self.__transformations = value        

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
    def tags(self) -> Tuple[str, ...]:
        """Tags associated with dataset."""
        return self.__tags

    @tags.setter
    def tags(self, value: Tuple[str, ...]):
        self._property_changed('tags')
        self.__tags = value        
