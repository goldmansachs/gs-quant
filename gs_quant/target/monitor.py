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
from gs_quant.base import Base, InstrumentBase, camel_case_translate, get_enum_value


class ColumnFormat(Base):
        
    """Object used to specify the column formatting"""

    @camel_case_translate
    def __init__(
        self,
        precision: float,
        unit=None,
        human_readable: bool = None,
        axis_key=None,
        name: str = None
    ):        
        super().__init__()
        self.precision = precision
        self.unit = unit
        self.human_readable = human_readable
        self.axis_key = axis_key
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
    def unit(self):
        """Unit to show next to number"""
        return self.__unit

    @unit.setter
    def unit(self, value):
        self._property_changed('unit')
        self.__unit = value        

    @property
    def human_readable(self) -> bool:
        """Formats number to have commas"""
        return self.__human_readable

    @human_readable.setter
    def human_readable(self, value: bool):
        self._property_changed('human_readable')
        self.__human_readable = value        

    @property
    def axis_key(self):
        """Applicable for render type chart, determines line to be on the left or right
           axis"""
        return self.__axis_key

    @axis_key.setter
    def axis_key(self, value):
        self._property_changed('axis_key')
        self.__axis_key = value        


class ColumnMappingParameters(Base):
        
    """Object used to apply parameters to a column."""

    @camel_case_translate
    def __init__(
        self,
        name: str = None
    ):        
        super().__init__()
        self.name = name


class ColumnOperation(Base):
        
    """Object used to describe function chaining and column operations."""

    @camel_case_translate
    def __init__(
        self,
        column_names: Tuple[str, ...] = None,
        function_name: str = None,
        type_=None,
        name: str = None
    ):        
        super().__init__()
        self.column_names = column_names
        self.function_name = function_name
        self.__type = type_
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
    def type(self):
        """Type of inputs into the function. Series means pass the whole series into the
           function, value means just gets the result of the column and pass it
           into the given function"""
        return self.__type

    @type.setter
    def type(self, value):
        self._property_changed('type')
        self.__type = value        


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


class FunctionParameters(Base):
        
    """Function parameters to be passed into the relevant gs_quant function."""

    @camel_case_translate
    def __init__(
        self,
        initial: int = None,
        obs: int = None,
        returns_type=None,
        type_=None,
        w: int = None,
        entity_id: str = None,
        returns: bool = None,
        name: str = None
    ):        
        super().__init__()
        self.initial = initial
        self.obs = obs
        self.returns_type = returns_type
        self.__type = type_
        self.w = w
        self.entity_id = entity_id
        self.returns = returns
        self.name = name

    @property
    def initial(self) -> int:
        """Initial value"""
        return self.__initial

    @initial.setter
    def initial(self, value: int):
        self._property_changed('initial')
        self.__initial = value        

    @property
    def obs(self) -> int:
        """Number of Observations"""
        return self.__obs

    @obs.setter
    def obs(self, value: int):
        self._property_changed('obs')
        self.__obs = value        

    @property
    def returns_type(self):
        """returns type (simple, log)"""
        return self.__returns_type

    @returns_type.setter
    def returns_type(self, value):
        self._property_changed('returns_type')
        self.__returns_type = value        

    @property
    def type(self):
        """returns type (simple, log)"""
        return self.__type

    @type.setter
    def type(self, value):
        self._property_changed('type')
        self.__type = value        

    @property
    def w(self) -> int:
        """Window or int: number of observations and ramp up to use. e.g. Window(22, 10)
           where 22 is the window size"""
        return self.__w

    @w.setter
    def w(self, value: int):
        self._property_changed('w')
        self.__w = value        

    @property
    def entity_id(self) -> str:
        """Entity to use as additional series for functions. i.e. Beta or Correlation
           functions."""
        return self.__entity_id

    @entity_id.setter
    def entity_id(self, value: str):
        self._property_changed('entity_id')
        self.__entity_id = value        

    @property
    def returns(self) -> bool:
        """Whether pb_total_return custom function returns the sum or typical returns."""
        return self.__returns

    @returns.setter
    def returns(self, value: bool):
        self._property_changed('returns')
        self.__returns = value        


class FunctionWhere(Base):
        
    """Parameters that will be passed into the data measure requests."""

    @camel_case_translate
    def __init__(
        self,
        participation_rate: float = None,
        percent_adv: float = None,
        strike_reference: str = None,
        group: str = None,
        name: str = None
    ):        
        super().__init__()
        self.participation_rate = participation_rate
        self.percent_adv = percent_adv
        self.strike_reference = strike_reference
        self.group = group
        self.name = name

    @property
    def participation_rate(self) -> float:
        """Executed quantity over market volume (e.g. 5, 10, 20)."""
        return self.__participation_rate

    @participation_rate.setter
    def participation_rate(self, value: float):
        self._property_changed('participation_rate')
        self.__participation_rate = value        

    @property
    def percent_adv(self) -> float:
        """Size of trade as percentage of average daily volume (e.g. .05, 1, 2, ..., 20)."""
        return self.__percent_adv

    @percent_adv.setter
    def percent_adv(self, value: float):
        self._property_changed('percent_adv')
        self.__percent_adv = value        

    @property
    def strike_reference(self) -> str:
        """Reference for strike level (enum: spot, forward)."""
        return self.__strike_reference

    @strike_reference.setter
    def strike_reference(self, value: str):
        self._property_changed('strike_reference')
        self.__strike_reference = value        

    @property
    def group(self) -> str:
        """Group for the request."""
        return self.__group

    @group.setter
    def group(self, value: str):
        self._property_changed('group')
        self.__group = value        


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


class Sort(Base):
        
    """Object used to define sorting"""

    @camel_case_translate
    def __init__(
        self,
        column_name: str,
        type_=None,
        direction=None,
        name: str = None
    ):        
        super().__init__()
        self.__type = type_
        self.column_name = column_name
        self.direction = direction
        self.name = name

    @property
    def type(self):
        """Enum listing supported sort types"""
        return self.__type

    @type.setter
    def type(self, value):
        self._property_changed('type')
        self.__type = value        

    @property
    def column_name(self) -> str:
        """Required small string with a length from empty string to 50 characters"""
        return self.__column_name

    @column_name.setter
    def column_name(self, value: str):
        self._property_changed('column_name')
        self.__column_name = value        

    @property
    def direction(self):
        """Enum with available sort directions"""
        return self.__direction

    @direction.setter
    def direction(self, value):
        self._property_changed('direction')
        self.__direction = value        


class WipiRequestFilter(Base):
        
    """A filter used for transforming data"""

    @camel_case_translate
    def __init__(
        self,
        column: str,
        operation,
        value: Union[float, str],
        type_=None,
        name: str = None
    ):        
        super().__init__()
        self.column = column
        self.operation = operation
        self.value = value
        self.__type = type_
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
    def operation(self):
        """Enum listing supported operations for wipi filters."""
        return self.__operation

    @operation.setter
    def operation(self, value):
        self._property_changed('operation')
        self.__operation = value        

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
    def type(self):
        """Enum listing supported wipi filter types."""
        return self.__type

    @type.setter
    def type(self, value):
        self._property_changed('type')
        self.__type = value        


class ColumnMappings(Base):
        
    """Object used to map parameters to a column"""

    @camel_case_translate
    def __init__(
        self,
        column_name: str = None,
        parameters: ColumnMappingParameters = None,
        name: str = None
    ):        
        super().__init__()
        self.column_name = column_name
        self.parameters = parameters
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
    def parameters(self) -> ColumnMappingParameters:
        """Object used to apply parameters to a column."""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: ColumnMappingParameters):
        self._property_changed('parameters')
        self.__parameters = value        


class Function(Base):
        
    """Function or Measure to be applied to the column."""

    @camel_case_translate
    def __init__(
        self,
        measure: str,
        frequency,
        name: str = None,
        start_date: str = None,
        end_date: str = None,
        start_time: str = None,
        end_time: str = None,
        fields: Tuple[str, ...] = None,
        parameters: FunctionParameters = None,
        where: FunctionWhere = None,
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
    def frequency(self):
        """The frequency of the column data changes which dataset the values are retrieved
           from."""
        return self.__frequency

    @frequency.setter
    def frequency(self, value):
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
    def parameters(self) -> FunctionParameters:
        """Function parameters to be passed into the relevant gs_quant function."""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: FunctionParameters):
        self._property_changed('parameters')
        self.__parameters = value        

    @property
    def where(self) -> FunctionWhere:
        """Parameters that will be passed into the data measure requests."""
        return self.__where

    @where.setter
    def where(self, value: FunctionWhere):
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
        period,
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
    def period(self):
        """Calculated period"""
        return self.__period

    @period.setter
    def period(self, value):
        self._property_changed('period')
        self.__period = value        

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


class ColumnDefinition(Base):
        
    """Object defining the columns to be calculated in the monitor"""

    @camel_case_translate
    def __init__(
        self,
        render,
        name: str,
        enable_cell_flashing: bool = None,
        entity_property=None,
        function: Function = None,
        format_: ColumnFormat = None,
        width: float = None,
        column_property: ColumnProperty = None,
        column_operation: ColumnOperation = None,
        expression: str = None,
        expressions: Tuple[str, ...] = None,
        start_date: str = None,
        end_date: str = None
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
    def render(self):
        """Enum listing supported column definition render types"""
        return self.__render

    @render.setter
    def render(self, value):
        self._property_changed('render')
        self.__render = value        

    @property
    def entity_property(self):
        """Property to fetch from an entity"""
        return self.__entity_property

    @entity_property.setter
    def entity_property(self, value):
        self._property_changed('entity_property')
        self.__entity_property = value        

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


class EntityId(Base):
        
    """Object used to define entities"""

    @camel_case_translate
    def __init__(
        self,
        id_: str = None,
        column_mappings: Tuple[ColumnMappings, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.__id = id_
        self.column_mappings = column_mappings
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


class RatesResponseData(Base):
        
    """Rates calculated response data."""

    @camel_case_translate
    def __init__(
        self,
        name,
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
    def name(self):
        """Enum listing supported rate ids"""
        return self.__name

    @name.setter
    def name(self, value):
        self._property_changed('name')
        self.__name = value        

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
        sort: Sort = None
    ):        
        super().__init__()
        self.name = name
        self.movers = movers
        self.entity_ids = entity_ids
        self.sort = sort

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


class MonitorParameters(Base):
        
    """Parameters provided for a monitor"""

    @camel_case_translate
    def __init__(
        self,
        column_definitions: Tuple[ColumnDefinition, ...],
        row_groups: Tuple[RowGroup, ...],
        data_set_id: str = None,
        rebase_to_spot: bool = None,
        rebase_historical_curve: bool = None,
        meeting_after_next: bool = None,
        next_meeting: bool = None,
        last_meeting: bool = None,
        rebase_to_end_of_year_spot: bool = None,
        filters: Tuple[WipiRequestFilter, ...] = None,
        exportable: Tuple[str, ...] = None,
        fill_column_index: float = None,
        knot: float = None,
        default_hidden: bool = None,
        line_chart_color: str = None,
        chart_curve_type=None,
        name: str = None
    ):        
        super().__init__()
        self.column_definitions = column_definitions
        self.row_groups = row_groups
        self.data_set_id = data_set_id
        self.rebase_to_spot = rebase_to_spot
        self.rebase_historical_curve = rebase_historical_curve
        self.meeting_after_next = meeting_after_next
        self.next_meeting = next_meeting
        self.last_meeting = last_meeting
        self.rebase_to_end_of_year_spot = rebase_to_end_of_year_spot
        self.filters = filters
        self.exportable = exportable
        self.fill_column_index = fill_column_index
        self.knot = knot
        self.default_hidden = default_hidden
        self.line_chart_color = line_chart_color
        self.chart_curve_type = chart_curve_type
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
    def data_set_id(self) -> str:
        """ID of the dataset in which the monitor fetches data."""
        return self.__data_set_id

    @data_set_id.setter
    def data_set_id(self, value: str):
        self._property_changed('data_set_id')
        self.__data_set_id = value        

    @property
    def rebase_to_spot(self) -> bool:
        """Whether to rebase the output to the first rows values"""
        return self.__rebase_to_spot

    @rebase_to_spot.setter
    def rebase_to_spot(self, value: bool):
        self._property_changed('rebase_to_spot')
        self.__rebase_to_spot = value        

    @property
    def rebase_historical_curve(self) -> bool:
        """Whether to rebase the historical curve."""
        return self.__rebase_historical_curve

    @rebase_historical_curve.setter
    def rebase_historical_curve(self, value: bool):
        self._property_changed('rebase_historical_curve')
        self.__rebase_historical_curve = value        

    @property
    def meeting_after_next(self) -> bool:
        """For a given valuation date, toggle to pull the hikes/cuts priced in for the 2nd
           meeting after the valuation date over the past 3 months."""
        return self.__meeting_after_next

    @meeting_after_next.setter
    def meeting_after_next(self, value: bool):
        self._property_changed('meeting_after_next')
        self.__meeting_after_next = value        

    @property
    def next_meeting(self) -> bool:
        """For a given valuation date, toggle to pull the hikes/cuts priced in for the next
           meeting after the valuation date over the past 3 months."""
        return self.__next_meeting

    @next_meeting.setter
    def next_meeting(self, value: bool):
        self._property_changed('next_meeting')
        self.__next_meeting = value        

    @property
    def last_meeting(self) -> bool:
        """For a given valuation date, toggle to pull the hikes/cuts priced in for the last
           meeting before the valuation date over the past 3 months."""
        return self.__last_meeting

    @last_meeting.setter
    def last_meeting(self, value: bool):
        self._property_changed('last_meeting')
        self.__last_meeting = value        

    @property
    def rebase_to_end_of_year_spot(self) -> bool:
        """Whether to rebase to the EOY Forward."""
        return self.__rebase_to_end_of_year_spot

    @rebase_to_end_of_year_spot.setter
    def rebase_to_end_of_year_spot(self, value: bool):
        self._property_changed('rebase_to_end_of_year_spot')
        self.__rebase_to_end_of_year_spot = value        

    @property
    def filters(self) -> Tuple[WipiRequestFilter, ...]:
        """Filters for the dataset before returning the data response."""
        return self.__filters

    @filters.setter
    def filters(self, value: Tuple[WipiRequestFilter, ...]):
        self._property_changed('filters')
        self.__filters = value        

    @property
    def exportable(self) -> Tuple[str, ...]:
        """Permission to export monitor data."""
        return self.__exportable

    @exportable.setter
    def exportable(self, value: Tuple[str, ...]):
        self._property_changed('exportable')
        self.__exportable = value        

    @property
    def fill_column_index(self) -> float:
        """The Index to place the fill column. The Fill column is remaining white space in
           the monitor. Defaults to the last column."""
        return self.__fill_column_index

    @fill_column_index.setter
    def fill_column_index(self, value: float):
        self._property_changed('fill_column_index')
        self.__fill_column_index = value        

    @property
    def knot(self) -> float:
        """Used when rendering a chart component from the output, whether to display a knot
           in the chart configuration as a prop. Number represents size of the
           knot."""
        return self.__knot

    @knot.setter
    def knot(self, value: float):
        self._property_changed('knot')
        self.__knot = value        

    @property
    def default_hidden(self) -> bool:
        """On workspaces, monitors may be hidden by default. True will by default hide this
           monitor. For example, used in workspaces with multi charts."""
        return self.__default_hidden

    @default_hidden.setter
    def default_hidden(self, value: bool):
        self._property_changed('default_hidden')
        self.__default_hidden = value        

    @property
    def line_chart_color(self) -> str:
        """On monitors that render line charts, for example Central Bank Watch curves, this
           will enforce the line color."""
        return self.__line_chart_color

    @line_chart_color.setter
    def line_chart_color(self, value: str):
        self._property_changed('line_chart_color')
        self.__line_chart_color = value        

    @property
    def chart_curve_type(self):
        """The curve type of the chart line."""
        return self.__chart_curve_type

    @chart_curve_type.setter
    def chart_curve_type(self, value):
        self._property_changed('chart_curve_type')
        self.__chart_curve_type = value        


class Monitor(Base):
        
    """A marquee monitor object"""

    @camel_case_translate
    def __init__(
        self,
        name: str,
        type_,
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
        self.__type = type_
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
    def type(self):
        """Enum listing supported entities"""
        return self.__type

    @type.setter
    def type(self, value):
        self._property_changed('type')
        self.__type = value        

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
