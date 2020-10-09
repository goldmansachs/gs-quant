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


class AssetProperties(EnumBase, Enum):    
    
    """Enum listing supported asset properties"""

    assetClass = 'assetClass'
    currency = 'currency'
    createdTime = 'createdTime'
    description = 'description'
    exchange = 'exchange'
    id = 'id'
    liveDate = 'liveDate'
    name = 'name'
    underliers = 'underliers'
    region = 'region'
    shortName = 'shortName'
    type = 'type'
    xref_bbid = 'xref.bbid'
    xref_bcid = 'xref.bcid'
    xref_ticker = 'xref.ticker'
    xref_ric = 'xref.ric'
    date = 'date'
    value = 'value'
    slope = 'slope'
    OIS_value = 'OIS value'
    
    def __repr__(self):
        return self.value


class AvailableUnitTypes(EnumBase, Enum):    
    
    """Enum listing supported unit types"""

    percentage = 'percentage'
    percentageWithSymbol = 'percentageWithSymbol'
    bps = 'bps'
    bp = 'bp'
    x = 'x'
    
    def __repr__(self):
        return self.value


class EntitiesSupported(EnumBase, Enum):    
    
    """Enum listing supported entities"""

    assets = 'assets'
    tds = 'tds'
    
    def __repr__(self):
        return self.value


class ParameterPeriod(EnumBase, Enum):    
    
    """Enum listing supported parameter periods"""

    _1d = '1d'
    _1w = '1w'
    _1m = '1m'
    _3m = '3m'
    _6m = '6m'
    _1y = '1y'
    _2y = '2y'
    _5y = '5y'
    _10y = '10y'
    _30y = '30y'
    mtd = 'mtd'
    ytd = 'ytd'
    
    def __repr__(self):
        return self.value


class ParameterRender(EnumBase, Enum):    
    
    """Enum listing supported column definition render types"""

    bar = 'bar'
    boxplot = 'boxplot'
    chart = 'chart'
    color = 'color'
    default = 'default'
    direction = 'direction'
    heatmap = 'heatmap'
    hidden = 'hidden'
    multiColumnHeatmap = 'multiColumnHeatmap'
    progress = 'progress'
    range = 'range'
    scale = 'scale'
    simpleCandlestick = 'simpleCandlestick'
    sparkline = 'sparkline'
    stackedBarChart = 'stackedBarChart'
    text = 'text'
    triColor = 'triColor'
    
    def __repr__(self):
        return self.value


class RateIds(EnumBase, Enum):    
    
    """Enum listing supported rate ids"""

    USD = 'USD'
    EUR = 'EUR'
    JPY = 'JPY'
    GBP = 'GBP'
    CAD = 'CAD'
    AUD = 'AUD'
    
    def __repr__(self):
        return self.value


class SortDirection(EnumBase, Enum):    
    
    """Enum with available sort directions"""

    asc = 'asc'
    desc = 'desc'
    default = 'default'
    
    def __repr__(self):
        return self.value


class SortType(EnumBase, Enum):    
    
    """Enum listing supported sort types"""

    value = 'value'
    abs = 'abs'
    
    def __repr__(self):
        return self.value


class WipiFilterOperation(EnumBase, Enum):    
    
    """Enum listing supported operations for wipi filters."""

    eq = 'eq'
    ne = 'ne'
    gt = 'gt'
    lt = 'lt'
    gte = 'gte'
    lte = 'lte'
    last = 'last'
    
    def __repr__(self):
        return self.value


class WipiFilterType(EnumBase, Enum):    
    
    """Enum listing supported wipi filter types."""

    AND = 'AND'
    OR = 'OR'
    
    def __repr__(self):
        return self.value


class ColumnProperty(Base):
        
    """Object used to reference a column mapping"""

    @camel_case_translate
    def __init__(
        self,
        column_name: str = None,
        property_: str = None,
        name: str = None
    ):        
        super().__init__()
        self.column_name = column_name
        self.__property = property_
        self.name = name

    @property
    def column_name(self) -> str:
        """Name of the column to get property"""
        return self.__column_name

    @column_name.setter
    def column_name(self, value: str):
        self._property_changed('column_name')
        self.__column_name = value        

    @property
    def property(self) -> str:
        """Name of the property to get from column mapping"""
        return self.__property

    @property.setter
    def property(self, value: str):
        self._property_changed('property')
        self.__property = value        


class ExportParameters(Base):
        
    """Object with properties specifying how to export individual row or complete
       monitor data."""

    @camel_case_translate
    def __init__(
        self,
        tokens: Tuple[str, ...],
        data_set_id: str = None,
        fields: Tuple[str, ...] = None,
        label: str = None,
        start_date: str = None,
        name: str = None
    ):        
        super().__init__()
        self.data_set_id = data_set_id
        self.fields = fields
        self.label = label
        self.start_date = start_date
        self.tokens = tokens
        self.name = name

    @property
    def data_set_id(self) -> str:
        """Id of the DataSet in which the export will retrieve data from."""
        return self.__data_set_id

    @data_set_id.setter
    def data_set_id(self, value: str):
        self._property_changed('data_set_id')
        self.__data_set_id = value        

    @property
    def fields(self) -> Tuple[str, ...]:
        """The fields to be exported from the DataSet."""
        return self.__fields

    @fields.setter
    def fields(self, value: Tuple[str, ...]):
        self._property_changed('fields')
        self.__fields = value        

    @property
    def label(self) -> str:
        """The label for the export button. For example: Export Historical Data."""
        return self.__label

    @label.setter
    def label(self, value: str):
        self._property_changed('label')
        self.__label = value        

    @property
    def start_date(self) -> str:
        """The relative start date for the history of data to retrieve. Eg: -1y."""
        return self.__start_date

    @start_date.setter
    def start_date(self, value: str):
        self._property_changed('start_date')
        self.__start_date = value        

    @property
    def tokens(self) -> Tuple[str, ...]:
        return self.__tokens

    @tokens.setter
    def tokens(self, value: Tuple[str, ...]):
        self._property_changed('tokens')
        self.__tokens = value        


class FieldMap(Base):
        
    @camel_case_translate
    def __init__(
        self,
        name: str = None
    ):        
        super().__init__()
        self.name = name


class Historical(Base):
        
    """value and date for historical data"""

    @camel_case_translate
    def __init__(
        self,
        value: Union[float, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.value = value
        self.name = name

    @property
    def value(self) -> Union[float, str]:
        return self.__value

    @value.setter
    def value(self, value: Union[float, str]):
        self._property_changed('value')
        self.__value = value        


class MonitorResponseData(Base):
        
    """Monitor calculated response data"""

    @camel_case_translate
    def __init__(
        self,
        id_: str,
        result: dict,
        name: str = None
    ):        
        super().__init__()
        self.__id = id_
        self.result = result
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
    def result(self) -> dict:
        return self.__result

    @result.setter
    def result(self, value: dict):
        self._property_changed('result')
        self.__result = value        


class Movers(Base):
        
    """Object that allows to specify the case in which we only want to return the n top
       or bottom entities"""

    @camel_case_translate
    def __init__(
        self,
        column_name: str,
        top: float = None,
        bottom: float = None,
        name: str = None
    ):        
        super().__init__()
        self.top = top
        self.bottom = bottom
        self.column_name = column_name
        self.name = name

    @property
    def top(self) -> float:
        """Integer in the range from 0 to 10000"""
        return self.__top

    @top.setter
    def top(self, value: float):
        self._property_changed('top')
        self.__top = value        

    @property
    def bottom(self) -> float:
        """Integer in the range from 0 to 10000"""
        return self.__bottom

    @bottom.setter
    def bottom(self, value: float):
        self._property_changed('bottom')
        self.__bottom = value        

    @property
    def column_name(self) -> str:
        """Required small string with a length from empty string to 50 characters"""
        return self.__column_name

    @column_name.setter
    def column_name(self, value: str):
        self._property_changed('column_name')
        self.__column_name = value        


class ColumnFormat(Base):
        
    """Object used to specify the column formatting"""

    @camel_case_translate
    def __init__(
        self,
        precision: float,
        unit: Union[AvailableUnitTypes, str] = None,
        human_readable: bool = None,
        multiplier: float = None,
        axis_key: str = None,
        show_tooltip: bool = None,
        low_color: str = None,
        high_color: str = None,
        mid_color: str = None,
        low_value: float = None,
        high_value: float = None,
        name: str = None
    ):        
        super().__init__()
        self.precision = precision
        self.unit = unit
        self.human_readable = human_readable
        self.multiplier = multiplier
        self.axis_key = axis_key
        self.show_tooltip = show_tooltip
        self.low_color = low_color
        self.high_color = high_color
        self.mid_color = mid_color
        self.low_value = low_value
        self.high_value = high_value
        self.name = name

    @property
    def precision(self) -> float:
        """Number of decimals to show"""
        return self.__precision

    @precision.setter
    def precision(self, value: float):
        self._property_changed('precision')
        self.__precision = value        

    @property
    def unit(self) -> Union[AvailableUnitTypes, str]:
        """Unit to show next to number"""
        return self.__unit

    @unit.setter
    def unit(self, value: Union[AvailableUnitTypes, str]):
        self._property_changed('unit')
        self.__unit = get_enum_value(AvailableUnitTypes, value)        

    @property
    def human_readable(self) -> bool:
        """Formats number to have commas"""
        return self.__human_readable

    @human_readable.setter
    def human_readable(self, value: bool):
        self._property_changed('human_readable')
        self.__human_readable = value        

    @property
    def multiplier(self) -> float:
        """Formatted value is the product of the original value and multiplier"""
        return self.__multiplier

    @multiplier.setter
    def multiplier(self, value: float):
        self._property_changed('multiplier')
        self.__multiplier = value        

    @property
    def axis_key(self) -> str:
        """Applicable for render type chart, determines line to be on the left or right
           axis"""
        return self.__axis_key

    @axis_key.setter
    def axis_key(self, value: str):
        self._property_changed('axis_key')
        self.__axis_key = value        

    @property
    def show_tooltip(self) -> bool:
        """Whether to show the cell timestamp in a tooltip"""
        return self.__show_tooltip

    @show_tooltip.setter
    def show_tooltip(self, value: bool):
        self._property_changed('show_tooltip')
        self.__show_tooltip = value        

    @property
    def low_color(self) -> str:
        """Hex color of cell if the resulting value is less than lowValue. i.e. #FF0000"""
        return self.__low_color

    @low_color.setter
    def low_color(self, value: str):
        self._property_changed('low_color')
        self.__low_color = value        

    @property
    def high_color(self) -> str:
        """Hex color of cell if the resulting value is less than highValue. i.e. #FF0000"""
        return self.__high_color

    @high_color.setter
    def high_color(self, value: str):
        self._property_changed('high_color')
        self.__high_color = value        

    @property
    def mid_color(self) -> str:
        """Hex color of cell if the resulting value is equal to or between lowValue and
           highValue. i.e. #FF0000"""
        return self.__mid_color

    @mid_color.setter
    def mid_color(self, value: str):
        self._property_changed('mid_color')
        self.__mid_color = value        

    @property
    def low_value(self) -> float:
        """Value to compare for lowColor."""
        return self.__low_value

    @low_value.setter
    def low_value(self, value: float):
        self._property_changed('low_value')
        self.__low_value = value        

    @property
    def high_value(self) -> float:
        """Value to compare for HighColor."""
        return self.__high_value

    @high_value.setter
    def high_value(self, value: float):
        self._property_changed('high_value')
        self.__high_value = value        


class ColumnMappings(Base):
        
    """Object used to map parameters to a column"""

    @camel_case_translate
    def __init__(
        self,
        column_name: str = None,
        parameters: FieldMap = None,
        color: str = None,
        name: str = None
    ):        
        super().__init__()
        self.column_name = column_name
        self.parameters = parameters
        self.color = color
        self.name = name

    @property
    def column_name(self) -> str:
        """Required small string with a length from empty string to 50 characters"""
        return self.__column_name

    @column_name.setter
    def column_name(self, value: str):
        self._property_changed('column_name')
        self.__column_name = value        

    @property
    def parameters(self) -> FieldMap:
        return self.__parameters

    @parameters.setter
    def parameters(self, value: FieldMap):
        self._property_changed('parameters')
        self.__parameters = value        

    @property
    def color(self) -> str:
        """Hex color of the bar chart. i.e. #FF0000"""
        return self.__color

    @color.setter
    def color(self, value: str):
        self._property_changed('color')
        self.__color = value        


class ColumnOperation(Base):
        
    """Object used to describe function chaining and column operations."""

    @camel_case_translate
    def __init__(
        self,
        column_names: Tuple[str, ...] = None,
        function_name: str = None,
        type_: str = None,
        parameters: FieldMap = None,
        name: str = None
    ):        
        super().__init__()
        self.column_names = column_names
        self.function_name = function_name
        self.__type = type_
        self.parameters = parameters
        self.name = name

    @property
    def column_names(self) -> Tuple[str, ...]:
        """Name of the columns to get results from in order and put into the given
           function."""
        return self.__column_names

    @column_names.setter
    def column_names(self, value: Tuple[str, ...]):
        self._property_changed('column_names')
        self.__column_names = value        

    @property
    def function_name(self) -> str:
        """Name of the function to pass column results into."""
        return self.__function_name

    @function_name.setter
    def function_name(self, value: str):
        self._property_changed('function_name')
        self.__function_name = value        

    @property
    def type(self) -> str:
        """Type of inputs into the function. Series means pass the whole series into the
           function, value means just gets the result of the column and pass it
           into the given function"""
        return self.__type

    @type.setter
    def type(self, value: str):
        self._property_changed('type')
        self.__type = value        

    @property
    def parameters(self) -> FieldMap:
        """Parameters to be passed into GS Quant functions. For example, window (w)."""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: FieldMap):
        self._property_changed('parameters')
        self.__parameters = value        


class Function(Base):
        
    """Function or Measure to be applied to the column."""

    @camel_case_translate
    def __init__(
        self,
        measure: str,
        frequency: str,
        name: str = None,
        start_date: str = None,
        end_date: str = None,
        start_time: str = None,
        end_time: str = None,
        fields: Tuple[str, ...] = None,
        parameters: FieldMap = None,
        where: FieldMap = None,
        vendor: str = None,
        data_set_id: str = None
    ):        
        super().__init__()
        self.name = name
        self.measure = measure
        self.frequency = frequency
        self.start_date = start_date
        self.end_date = end_date
        self.start_time = start_time
        self.end_time = end_time
        self.fields = fields
        self.parameters = parameters
        self.where = where
        self.vendor = vendor
        self.data_set_id = data_set_id

    @property
    def name(self) -> str:
        """The name of the function to be applied to the column."""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def measure(self) -> str:
        """The asset data measure to be applied to the column."""
        return self.__measure

    @measure.setter
    def measure(self, value: str):
        self._property_changed('measure')
        self.__measure = value        

    @property
    def frequency(self) -> str:
        """The frequency of the column data changes which dataset the values are retrieved
           from."""
        return self.__frequency

    @frequency.setter
    def frequency(self, value: str):
        self._property_changed('frequency')
        self.__frequency = value        

    @property
    def start_date(self) -> str:
        """The relative start date for columns requiring historical data. Eg: -1y."""
        return self.__start_date

    @start_date.setter
    def start_date(self, value: str):
        self._property_changed('start_date')
        self.__start_date = value        

    @property
    def end_date(self) -> str:
        """The relative end date for columns requiring historical data. Eg: -1y."""
        return self.__end_date

    @end_date.setter
    def end_date(self, value: str):
        self._property_changed('end_date')
        self.__end_date = value        

    @property
    def start_time(self) -> str:
        """The relative start time for columns requiring historical data. Eg: -1y."""
        return self.__start_time

    @start_time.setter
    def start_time(self, value: str):
        self._property_changed('start_time')
        self.__start_time = value        

    @property
    def end_time(self) -> str:
        """The relative end time for columns requiring historical data. Eg: -1y."""
        return self.__end_time

    @end_time.setter
    def end_time(self, value: str):
        self._property_changed('end_time')
        self.__end_time = value        

    @property
    def fields(self) -> Tuple[str, ...]:
        """Fields to be passed into Measure Service. i.e. sum(value)"""
        return self.__fields

    @fields.setter
    def fields(self, value: Tuple[str, ...]):
        self._property_changed('fields')
        self.__fields = value        

    @property
    def parameters(self) -> FieldMap:
        """Parameters to be passed into GS Quant functions. For example, window (w)."""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: FieldMap):
        self._property_changed('parameters')
        self.__parameters = value        

    @property
    def where(self) -> FieldMap:
        return self.__where

    @where.setter
    def where(self, value: FieldMap):
        self._property_changed('where')
        self.__where = value        

    @property
    def vendor(self) -> str:
        """The vendor the dataset is owned by."""
        return self.__vendor

    @vendor.setter
    def vendor(self, value: str):
        self._property_changed('vendor')
        self.__vendor = value        

    @property
    def data_set_id(self) -> str:
        """The name of a DataSet to directly query."""
        return self.__data_set_id

    @data_set_id.setter
    def data_set_id(self, value: str):
        self._property_changed('data_set_id')
        self.__data_set_id = value        


class RateRow(Base):
        
    """Rate row with calculated data"""

    @camel_case_translate
    def __init__(
        self,
        period: Union[ParameterPeriod, str],
        last: float,
        change: float,
        std: float,
        slope: float,
        historical: Historical = None,
        percentage_change: float = None,
        name: str = None
    ):        
        super().__init__()
        self.period = period
        self.last = last
        self.historical = historical
        self.change = change
        self.percentage_change = percentage_change
        self.std = std
        self.slope = slope
        self.name = name

    @property
    def period(self) -> Union[ParameterPeriod, str]:
        """Calculated period"""
        return self.__period

    @period.setter
    def period(self, value: Union[ParameterPeriod, str]):
        self._property_changed('period')
        self.__period = get_enum_value(ParameterPeriod, value)        

    @property
    def last(self) -> float:
        """Last available price"""
        return self.__last

    @last.setter
    def last(self, value: float):
        self._property_changed('last')
        self.__last = value        

    @property
    def historical(self) -> Historical:
        """EOD price and date"""
        return self.__historical

    @historical.setter
    def historical(self, value: Historical):
        self._property_changed('historical')
        self.__historical = value        

    @property
    def change(self) -> float:
        """One day prince change"""
        return self.__change

    @change.setter
    def change(self, value: float):
        self._property_changed('change')
        self.__change = value        

    @property
    def percentage_change(self) -> float:
        """One day prince change in percentage"""
        return self.__percentage_change

    @percentage_change.setter
    def percentage_change(self, value: float):
        self._property_changed('percentage_change')
        self.__percentage_change = value        

    @property
    def std(self) -> float:
        """2 year standard deviation of daily changes for given tenor swaps"""
        return self.__std

    @std.setter
    def std(self, value: float):
        self._property_changed('std')
        self.__std = value        

    @property
    def slope(self) -> float:
        """Number in the range from -1000000000000 to 1000000000000"""
        return self.__slope

    @slope.setter
    def slope(self, value: float):
        self._property_changed('slope')
        self.__slope = value        


class Sort(Base):
        
    """Object used to define sorting"""

    @camel_case_translate
    def __init__(
        self,
        column_name: str,
        type_: Union[SortType, str] = None,
        direction: Union[SortDirection, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.__type = get_enum_value(SortType, type_)
        self.column_name = column_name
        self.direction = direction
        self.name = name

    @property
    def type(self) -> Union[SortType, str]:
        """Enum listing supported sort types"""
        return self.__type

    @type.setter
    def type(self, value: Union[SortType, str]):
        self._property_changed('type')
        self.__type = get_enum_value(SortType, value)        

    @property
    def column_name(self) -> str:
        """Required small string with a length from empty string to 50 characters"""
        return self.__column_name

    @column_name.setter
    def column_name(self, value: str):
        self._property_changed('column_name')
        self.__column_name = value        

    @property
    def direction(self) -> Union[SortDirection, str]:
        """Enum with available sort directions"""
        return self.__direction

    @direction.setter
    def direction(self, value: Union[SortDirection, str]):
        self._property_changed('direction')
        self.__direction = get_enum_value(SortDirection, value)        


class WipiRequestFilter(Base):
        
    """A filter used for transforming data"""

    @camel_case_translate
    def __init__(
        self,
        column: str,
        operation: Union[WipiFilterOperation, str],
        value: Union[float, str],
        type_: Union[WipiFilterType, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.column = column
        self.operation = operation
        self.value = value
        self.__type = get_enum_value(WipiFilterType, type_)
        self.name = name

    @property
    def column(self) -> str:
        """The column to perform the operation on."""
        return self.__column

    @column.setter
    def column(self, value: str):
        self._property_changed('column')
        self.__column = value        

    @property
    def operation(self) -> Union[WipiFilterOperation, str]:
        """Enum listing supported operations for wipi filters."""
        return self.__operation

    @operation.setter
    def operation(self, value: Union[WipiFilterOperation, str]):
        self._property_changed('operation')
        self.__operation = get_enum_value(WipiFilterOperation, value)        

    @property
    def value(self) -> Union[float, str]:
        """The value of the operation is used with. Relative dates are used against the
           last valuationDate."""
        return self.__value

    @value.setter
    def value(self, value: Union[float, str]):
        self._property_changed('value')
        self.__value = value        

    @property
    def type(self) -> Union[WipiFilterType, str]:
        """Enum listing supported wipi filter types."""
        return self.__type

    @type.setter
    def type(self, value: Union[WipiFilterType, str]):
        self._property_changed('type')
        self.__type = get_enum_value(WipiFilterType, value)        


class ColumnDefinition(Base):
        
    """Object defining the columns to be calculated in the monitor"""

    @camel_case_translate
    def __init__(
        self,
        render: Union[ParameterRender, str],
        name: str,
        enable_cell_flashing: bool = None,
        entity_property: Union[AssetProperties, str] = None,
        function: Function = None,
        format_: ColumnFormat = None,
        width: float = None,
        column_property: ColumnProperty = None,
        column_operation: ColumnOperation = None,
        expression: str = None,
        expressions: Tuple[str, ...] = None,
        start_date: str = None,
        end_date: str = None,
        tooltip: str = None,
        parent_column_name: str = None,
        primary: bool = None
    ):        
        super().__init__()
        self.enable_cell_flashing = enable_cell_flashing
        self.name = name
        self.render = render
        self.entity_property = entity_property
        self.function = function
        self.__format = format_
        self.width = width
        self.column_property = column_property
        self.column_operation = column_operation
        self.expression = expression
        self.expressions = expressions
        self.start_date = start_date
        self.end_date = end_date
        self.tooltip = tooltip
        self.parent_column_name = parent_column_name
        self.primary = primary

    @property
    def enable_cell_flashing(self) -> bool:
        """Enable cell flashing for the column"""
        return self.__enable_cell_flashing

    @enable_cell_flashing.setter
    def enable_cell_flashing(self, value: bool):
        self._property_changed('enable_cell_flashing')
        self.__enable_cell_flashing = value        

    @property
    def name(self) -> str:
        """Column name"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def render(self) -> Union[ParameterRender, str]:
        """Enum listing supported column definition render types"""
        return self.__render

    @render.setter
    def render(self, value: Union[ParameterRender, str]):
        self._property_changed('render')
        self.__render = get_enum_value(ParameterRender, value)        

    @property
    def entity_property(self) -> Union[AssetProperties, str]:
        """Property to fetch from an entity"""
        return self.__entity_property

    @entity_property.setter
    def entity_property(self, value: Union[AssetProperties, str]):
        self._property_changed('entity_property')
        self.__entity_property = get_enum_value(AssetProperties, value)        

    @property
    def function(self) -> Function:
        """Function or Measure to be applied to the column."""
        return self.__function

    @function.setter
    def function(self, value: Function):
        self._property_changed('function')
        self.__function = value        

    @property
    def format(self) -> ColumnFormat:
        """Object used to specify the column formatting"""
        return self.__format

    @format.setter
    def format(self, value: ColumnFormat):
        self._property_changed('format')
        self.__format = value        

    @property
    def width(self) -> float:
        """Width of the column"""
        return self.__width

    @width.setter
    def width(self, value: float):
        self._property_changed('width')
        self.__width = value        

    @property
    def column_property(self) -> ColumnProperty:
        """Column name"""
        return self.__column_property

    @column_property.setter
    def column_property(self, value: ColumnProperty):
        self._property_changed('column_property')
        self.__column_property = value        

    @property
    def column_operation(self) -> ColumnOperation:
        """Object that describes function chaining and operations."""
        return self.__column_operation

    @column_operation.setter
    def column_operation(self, value: ColumnOperation):
        self._property_changed('column_operation')
        self.__column_operation = value        

    @property
    def expression(self) -> str:
        """String that represents the column in the form of a PlotTool expression."""
        return self.__expression

    @expression.setter
    def expression(self, value: str):
        self._property_changed('expression')
        self.__expression = value        

    @property
    def expressions(self) -> Tuple[str, ...]:
        """Array of PlotTool Expressions for /v1/plots/expansionRunner"""
        return self.__expressions

    @expressions.setter
    def expressions(self, value: Tuple[str, ...]):
        self._property_changed('expressions')
        self.__expressions = value        

    @property
    def start_date(self) -> str:
        """String that represents the start date for expressions."""
        return self.__start_date

    @start_date.setter
    def start_date(self, value: str):
        self._property_changed('start_date')
        self.__start_date = value        

    @property
    def end_date(self) -> str:
        """String that represents the end date for expressions"""
        return self.__end_date

    @end_date.setter
    def end_date(self, value: str):
        self._property_changed('end_date')
        self.__end_date = value        

    @property
    def tooltip(self) -> str:
        """Tooltip that is displayed on the column header"""
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self._property_changed('tooltip')
        self.__tooltip = value        

    @property
    def parent_column_name(self) -> str:
        """Name of the top level column name."""
        return self.__parent_column_name

    @parent_column_name.setter
    def parent_column_name(self, value: str):
        self._property_changed('parent_column_name')
        self.__parent_column_name = value        

    @property
    def primary(self) -> bool:
        """Applies variable column width to primary column when displayed as a monitor"""
        return self.__primary

    @primary.setter
    def primary(self, value: bool):
        self._property_changed('primary')
        self.__primary = value        


class EntityId(Base):
        
    """Object used to define entities"""

    @camel_case_translate
    def __init__(
        self,
        id_: str = None,
        column_mappings: Tuple[ColumnMappings, ...] = None,
        color: str = None,
        name: str = None
    ):        
        super().__init__()
        self.__id = id_
        self.column_mappings = column_mappings
        self.color = color
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
    def column_mappings(self) -> Tuple[ColumnMappings, ...]:
        """Array of column mappings for the entity"""
        return self.__column_mappings

    @column_mappings.setter
    def column_mappings(self, value: Tuple[ColumnMappings, ...]):
        self._property_changed('column_mappings')
        self.__column_mappings = value        

    @property
    def color(self) -> str:
        """Hex color of the cell. i.e. #FF0000"""
        return self.__color

    @color.setter
    def color(self, value: str):
        self._property_changed('color')
        self.__color = value        


class RatesResponseData(Base):
        
    """Rates calculated response data."""

    @camel_case_translate
    def __init__(
        self,
        name: Union[RateIds, str],
        id_: str,
        rows: Tuple[RateRow, ...],
        libor_id: str = None
    ):        
        super().__init__()
        self.name = name
        self.__id = id_
        self.libor_id = libor_id
        self.rows = rows

    @property
    def name(self) -> Union[RateIds, str]:
        """Enum listing supported rate ids"""
        return self.__name

    @name.setter
    def name(self, value: Union[RateIds, str]):
        self._property_changed('name')
        self.__name = get_enum_value(RateIds, value)        

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def libor_id(self) -> str:
        """Marquee unique identifier"""
        return self.__libor_id

    @libor_id.setter
    def libor_id(self, value: str):
        self._property_changed('libor_id')
        self.__libor_id = value        

    @property
    def rows(self) -> Tuple[RateRow, ...]:
        """Calculated rows for given rate ID"""
        return self.__rows

    @rows.setter
    def rows(self, value: Tuple[RateRow, ...]):
        self._property_changed('rows')
        self.__rows = value        


class RowGroup(Base):
        
    """Object specifying a group name and a list of assets to be calculated in a
       monitor"""

    @camel_case_translate
    def __init__(
        self,
        name: str,
        entity_ids: Tuple[EntityId, ...],
        movers: Movers = None,
        sort: Sort = None,
        export: ExportParameters = None
    ):        
        super().__init__()
        self.name = name
        self.movers = movers
        self.entity_ids = entity_ids
        self.sort = sort
        self.export = export

    @property
    def name(self) -> str:
        """Group name"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def movers(self) -> Movers:
        """Object that allows to specify the case in which we only want to return the n top
           or bottom entities"""
        return self.__movers

    @movers.setter
    def movers(self, value: Movers):
        self._property_changed('movers')
        self.__movers = value        

    @property
    def entity_ids(self) -> Tuple[EntityId, ...]:
        """Array of entity objects that belong to the group"""
        return self.__entity_ids

    @entity_ids.setter
    def entity_ids(self, value: Tuple[EntityId, ...]):
        self._property_changed('entity_ids')
        self.__entity_ids = value        

    @property
    def sort(self) -> Sort:
        """Object used to define sorting"""
        return self.__sort

    @sort.setter
    def sort(self, value: Sort):
        self._property_changed('sort')
        self.__sort = value        

    @property
    def export(self) -> ExportParameters:
        """Object with properties specifying how to export individual row or complete
           monitor data."""
        return self.__export

    @export.setter
    def export(self, value: ExportParameters):
        self._property_changed('export')
        self.__export = value        


class MonitorParameters(Base):
        
    """Parameters provided for a monitor"""

    @camel_case_translate
    def __init__(
        self,
        column_definitions: Tuple[ColumnDefinition, ...],
        row_groups: Tuple[RowGroup, ...],
        export: ExportParameters = None,
        ignore_business_day_logic: bool = None,
        name: str = None
    ):        
        super().__init__()
        self.column_definitions = column_definitions
        self.row_groups = row_groups
        self.export = export
        self.ignore_business_day_logic = ignore_business_day_logic
        self.name = name

    @property
    def column_definitions(self) -> Tuple[ColumnDefinition, ...]:
        """Array of monitor column definitions"""
        return self.__column_definitions

    @column_definitions.setter
    def column_definitions(self, value: Tuple[ColumnDefinition, ...]):
        self._property_changed('column_definitions')
        self.__column_definitions = value        

    @property
    def row_groups(self) -> Tuple[RowGroup, ...]:
        """Monitor row groups"""
        return self.__row_groups

    @row_groups.setter
    def row_groups(self, value: Tuple[RowGroup, ...]):
        self._property_changed('row_groups')
        self.__row_groups = value        

    @property
    def export(self) -> ExportParameters:
        """Object with properties specifying how to export individual row or complete
           monitor data."""
        return self.__export

    @export.setter
    def export(self, value: ExportParameters):
        self._property_changed('export')
        self.__export = value        

    @property
    def ignore_business_day_logic(self) -> bool:
        """Whether or not to apply business day logic for relative dates."""
        return self.__ignore_business_day_logic

    @ignore_business_day_logic.setter
    def ignore_business_day_logic(self, value: bool):
        self._property_changed('ignore_business_day_logic')
        self.__ignore_business_day_logic = value        


class Monitor(Base):
        
    """A marquee monitor object"""

    @camel_case_translate
    def __init__(
        self,
        name: str,
        type_: Union[EntitiesSupported, str],
        id_: str = None,
        parameters: MonitorParameters = None,
        created_time: datetime.datetime = None,
        last_updated_time: datetime.datetime = None,
        created_by_id: str = None,
        last_updated_by_id: str = None,
        owner_id: str = None,
        entitlements: Entitlements = None,
        folder_name: str = None,
        polling_time: float = None,
        tags: Tuple[str, ...] = None
    ):        
        super().__init__()
        self.__id = id_
        self.name = name
        self.__type = get_enum_value(EntitiesSupported, type_)
        self.parameters = parameters
        self.created_time = created_time
        self.last_updated_time = last_updated_time
        self.created_by_id = created_by_id
        self.last_updated_by_id = last_updated_by_id
        self.owner_id = owner_id
        self.entitlements = entitlements
        self.folder_name = folder_name
        self.polling_time = polling_time
        self.tags = tags

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
        """Display name of monitor"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def type(self) -> Union[EntitiesSupported, str]:
        """Enum listing supported entities"""
        return self.__type

    @type.setter
    def type(self, value: Union[EntitiesSupported, str]):
        self._property_changed('type')
        self.__type = get_enum_value(EntitiesSupported, value)        

    @property
    def parameters(self) -> MonitorParameters:
        """Parameters provided for a monitor"""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: MonitorParameters):
        self._property_changed('parameters')
        self.__parameters = value        

    @property
    def created_time(self) -> datetime.datetime:
        """Time created. ISO 8601 formatted string"""
        return self.__created_time

    @created_time.setter
    def created_time(self, value: datetime.datetime):
        self._property_changed('created_time')
        self.__created_time = value        

    @property
    def last_updated_time(self) -> datetime.datetime:
        """Timestamp of when the object was last updated"""
        return self.__last_updated_time

    @last_updated_time.setter
    def last_updated_time(self, value: datetime.datetime):
        self._property_changed('last_updated_time')
        self.__last_updated_time = value        

    @property
    def created_by_id(self) -> str:
        """Unique identifier of user who created the object"""
        return self.__created_by_id

    @created_by_id.setter
    def created_by_id(self, value: str):
        self._property_changed('created_by_id')
        self.__created_by_id = value        

    @property
    def last_updated_by_id(self) -> str:
        """Unique identifier of user who last updated the object"""
        return self.__last_updated_by_id

    @last_updated_by_id.setter
    def last_updated_by_id(self, value: str):
        self._property_changed('last_updated_by_id')
        self.__last_updated_by_id = value        

    @property
    def owner_id(self) -> str:
        """Marquee unique identifier"""
        return self.__owner_id

    @owner_id.setter
    def owner_id(self, value: str):
        self._property_changed('owner_id')
        self.__owner_id = value        

    @property
    def entitlements(self) -> Entitlements:
        """Defines the entitlements of a given resource"""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self._property_changed('entitlements')
        self.__entitlements = value        

    @property
    def folder_name(self) -> str:
        """Folder name of the monitor"""
        return self.__folder_name

    @folder_name.setter
    def folder_name(self, value: str):
        self._property_changed('folder_name')
        self.__folder_name = value        

    @property
    def polling_time(self) -> float:
        """Polling time to use in milliseconds. A polling time of zero denotes no
           streaming."""
        return self.__polling_time

    @polling_time.setter
    def polling_time(self, value: float):
        self._property_changed('polling_time')
        self.__polling_time = value        

    @property
    def tags(self) -> Tuple[str, ...]:
        """Array of tag strings"""
        return self.__tags

    @tags.setter
    def tags(self, value: Tuple[str, ...]):
        self._property_changed('tags')
        self.__tags = value        
