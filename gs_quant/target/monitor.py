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
from gs_quant.base import Base, get_enum_value


class ColumnFormat(Base):
        
    """Object used to specify the column formatting"""
       
    def __init__(
        self,
        precision: float,
        unit=None,
        human_readable: bool = None
    ):        
        super().__init__()
        self.precision = precision
        self.unit = unit
        self.human_readable = human_readable

    @property
    def precision(self) -> float:
        """Number of decimals to show"""
        return self.__precision

    @precision.setter
    def precision(self, value: float):
        self.__precision = value
        self._property_changed('precision')        

    @property
    def unit(self):
        """Unit to show next to number"""
        return self.__unit

    @unit.setter
    def unit(self, value):
        self.__unit = value
        self._property_changed('unit')        

    @property
    def human_readable(self) -> bool:
        """Formats number to have commas"""
        return self.__human_readable

    @human_readable.setter
    def human_readable(self, value: bool):
        self.__human_readable = value
        self._property_changed('human_readable')        


class FunctionParameters(Base):
        
    """Function parameters to be passed into the relevant gs_quant function."""
       
    def __init__(
        self,
        initial: int = None,
        obs: int = None,
        returns_type=None,
        type_=None,
        w: int = None,
        entity_id: str = None
    ):        
        super().__init__()
        self.initial = initial
        self.obs = obs
        self.returns_type = returns_type
        self.__type = type_
        self.w = w
        self.entity_id = entity_id

    @property
    def initial(self) -> int:
        """Initial value"""
        return self.__initial

    @initial.setter
    def initial(self, value: int):
        self.__initial = value
        self._property_changed('initial')        

    @property
    def obs(self) -> int:
        """Number of Observations"""
        return self.__obs

    @obs.setter
    def obs(self, value: int):
        self.__obs = value
        self._property_changed('obs')        

    @property
    def returns_type(self):
        """returns type (simple, log)"""
        return self.__returns_type

    @returns_type.setter
    def returns_type(self, value):
        self.__returns_type = value
        self._property_changed('returns_type')        

    @property
    def type(self):
        """returns type (simple, log)"""
        return self.__type

    @type.setter
    def type(self, value):
        self.__type = value
        self._property_changed('type')        

    @property
    def w(self) -> int:
        """Window or int: number of observations and ramp up to use. e.g. Window(22, 10)
           where 22 is the window size"""
        return self.__w

    @w.setter
    def w(self, value: int):
        self.__w = value
        self._property_changed('w')        

    @property
    def entity_id(self) -> str:
        """Entity to use as additional series for functions. i.e. Beta or Correlation
           functions."""
        return self.__entity_id

    @entity_id.setter
    def entity_id(self, value: str):
        self.__entity_id = value
        self._property_changed('entity_id')        


class FunctionWhere(Base):
        
    """Parameters that will be passed into the data measure requests."""
       
    def __init__(
        self,
        participation_rate: float = None,
        percent_adv: float = None,
        strike_reference: str = None
    ):        
        super().__init__()
        self.participation_rate = participation_rate
        self.percent_adv = percent_adv
        self.strike_reference = strike_reference

    @property
    def participation_rate(self) -> float:
        """Executed quantity over market volume (e.g. 5, 10, 20)."""
        return self.__participation_rate

    @participation_rate.setter
    def participation_rate(self, value: float):
        self.__participation_rate = value
        self._property_changed('participation_rate')        

    @property
    def percent_adv(self) -> float:
        """Size of trade as percentage of average daily volume (e.g. .05, 1, 2, ..., 20)."""
        return self.__percent_adv

    @percent_adv.setter
    def percent_adv(self, value: float):
        self.__percent_adv = value
        self._property_changed('percent_adv')        

    @property
    def strike_reference(self) -> str:
        """Reference for strike level (enum: spot, forward)."""
        return self.__strike_reference

    @strike_reference.setter
    def strike_reference(self, value: str):
        self.__strike_reference = value
        self._property_changed('strike_reference')        


class Historical(Base):
        
    """value and date for historical data"""
       
    def __init__(
        self,
        value: Union[float, str] = None
    ):        
        super().__init__()
        self.value = value

    @property
    def value(self) -> Union[float, str]:
        return self.__value

    @value.setter
    def value(self, value: Union[float, str]):
        self.__value = value
        self._property_changed('value')        


class MonitorResponseData(Base):
        
    """Monitor calculated response data"""
       
    def __init__(
        self,
        id_: str,
        result: dict
    ):        
        super().__init__()
        self.__id = id_
        self.result = result

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value
        self._property_changed('id')        

    @property
    def result(self) -> dict:
        return self.__result

    @result.setter
    def result(self, value: dict):
        self.__result = value
        self._property_changed('result')        


class Movers(Base):
        
    """Object that allows to specify the case in which we only want to return the n top
       or bottom entities"""
       
    def __init__(
        self,
        column_name: str,
        top: float = None,
        bottom: float = None
    ):        
        super().__init__()
        self.top = top
        self.bottom = bottom
        self.column_name = column_name

    @property
    def top(self) -> float:
        """Integer in the range from 0 to 10000"""
        return self.__top

    @top.setter
    def top(self, value: float):
        self.__top = value
        self._property_changed('top')        

    @property
    def bottom(self) -> float:
        """Integer in the range from 0 to 10000"""
        return self.__bottom

    @bottom.setter
    def bottom(self, value: float):
        self.__bottom = value
        self._property_changed('bottom')        

    @property
    def column_name(self) -> str:
        """Required small string with a length from empty string to 50 characters"""
        return self.__column_name

    @column_name.setter
    def column_name(self, value: str):
        self.__column_name = value
        self._property_changed('column_name')        


class Sort(Base):
        
    """Object used to define sorting"""
       
    def __init__(
        self,
        column_name: str,
        type_=None,
        direction=None
    ):        
        super().__init__()
        self.__type = type_
        self.column_name = column_name
        self.direction = direction

    @property
    def type(self):
        """Enum listing supported sort types"""
        return self.__type

    @type.setter
    def type(self, value):
        self.__type = value
        self._property_changed('type')        

    @property
    def column_name(self) -> str:
        """Required small string with a length from empty string to 50 characters"""
        return self.__column_name

    @column_name.setter
    def column_name(self, value: str):
        self.__column_name = value
        self._property_changed('column_name')        

    @property
    def direction(self):
        """Enum with available sort directions"""
        return self.__direction

    @direction.setter
    def direction(self, value):
        self.__direction = value
        self._property_changed('direction')        


class WipiRequestFilter(Base):
        
    """A filter used for transforming data"""
       
    def __init__(
        self,
        column: str,
        operation,
        value: Union[float, str],
        type_=None
    ):        
        super().__init__()
        self.column = column
        self.operation = operation
        self.value = value
        self.__type = type_

    @property
    def column(self) -> str:
        """The column to perform the operation on."""
        return self.__column

    @column.setter
    def column(self, value: str):
        self.__column = value
        self._property_changed('column')        

    @property
    def operation(self):
        """Enum listing supported operations for wipi filters."""
        return self.__operation

    @operation.setter
    def operation(self, value):
        self.__operation = value
        self._property_changed('operation')        

    @property
    def value(self) -> Union[float, str]:
        """The value of the operation is used with. Relative dates are used against the
           last valuationDate."""
        return self.__value

    @value.setter
    def value(self, value: Union[float, str]):
        self.__value = value
        self._property_changed('value')        

    @property
    def type(self):
        """Enum listing supported wipi filter types."""
        return self.__type

    @type.setter
    def type(self, value):
        self.__type = value
        self._property_changed('type')        


class Function(Base):
        
    """Function or Measure to be applied to the column."""
       
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
        vendor: str = None
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

    @property
    def name(self) -> str:
        """The name of the function to be applied to the column."""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def measure(self) -> str:
        """The asset data measure to be applied to the column."""
        return self.__measure

    @measure.setter
    def measure(self, value: str):
        self.__measure = value
        self._property_changed('measure')        

    @property
    def frequency(self):
        """The frequency of the column data changes which dataset the values are retrieved
           from."""
        return self.__frequency

    @frequency.setter
    def frequency(self, value):
        self.__frequency = value
        self._property_changed('frequency')        

    @property
    def start_date(self) -> str:
        """The relative start date for columns requiring historical data. Eg: -1y."""
        return self.__start_date

    @start_date.setter
    def start_date(self, value: str):
        self.__start_date = value
        self._property_changed('start_date')        

    @property
    def end_date(self) -> str:
        """The relative end date for columns requiring historical data. Eg: -1y."""
        return self.__end_date

    @end_date.setter
    def end_date(self, value: str):
        self.__end_date = value
        self._property_changed('end_date')        

    @property
    def start_time(self) -> str:
        """The relative start time for columns requiring historical data. Eg: -1y."""
        return self.__start_time

    @start_time.setter
    def start_time(self, value: str):
        self.__start_time = value
        self._property_changed('start_time')        

    @property
    def end_time(self) -> str:
        """The relative end time for columns requiring historical data. Eg: -1y."""
        return self.__end_time

    @end_time.setter
    def end_time(self, value: str):
        self.__end_time = value
        self._property_changed('end_time')        

    @property
    def fields(self) -> Tuple[str, ...]:
        """Fields to be passed into Measure Service. i.e. sum(value)"""
        return self.__fields

    @fields.setter
    def fields(self, value: Tuple[str, ...]):
        self.__fields = value
        self._property_changed('fields')        

    @property
    def parameters(self) -> FunctionParameters:
        """Function parameters to be passed into the relevant gs_quant function."""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: FunctionParameters):
        self.__parameters = value
        self._property_changed('parameters')        

    @property
    def where(self) -> FunctionWhere:
        """Parameters that will be passed into the data measure requests."""
        return self.__where

    @where.setter
    def where(self, value: FunctionWhere):
        self.__where = value
        self._property_changed('where')        

    @property
    def vendor(self) -> str:
        """The vendor the dataset is owned by."""
        return self.__vendor

    @vendor.setter
    def vendor(self, value: str):
        self.__vendor = value
        self._property_changed('vendor')        


class RateRow(Base):
        
    """Rate row with calculated data"""
       
    def __init__(
        self,
        period,
        last: float,
        change: float,
        std: float,
        slope: float,
        historical: Historical = None,
        percentage_change: float = None
    ):        
        super().__init__()
        self.period = period
        self.last = last
        self.historical = historical
        self.change = change
        self.percentage_change = percentage_change
        self.std = std
        self.slope = slope

    @property
    def period(self):
        """Calculated period"""
        return self.__period

    @period.setter
    def period(self, value):
        self.__period = value
        self._property_changed('period')        

    @property
    def last(self) -> float:
        """Last available price"""
        return self.__last

    @last.setter
    def last(self, value: float):
        self.__last = value
        self._property_changed('last')        

    @property
    def historical(self) -> Historical:
        """EOD price and date"""
        return self.__historical

    @historical.setter
    def historical(self, value: Historical):
        self.__historical = value
        self._property_changed('historical')        

    @property
    def change(self) -> float:
        """One day prince change"""
        return self.__change

    @change.setter
    def change(self, value: float):
        self.__change = value
        self._property_changed('change')        

    @property
    def percentage_change(self) -> float:
        """One day prince change in percentage"""
        return self.__percentage_change

    @percentage_change.setter
    def percentage_change(self, value: float):
        self.__percentage_change = value
        self._property_changed('percentage_change')        

    @property
    def std(self) -> float:
        """2 year standard deviation of daily changes for given tenor swaps"""
        return self.__std

    @std.setter
    def std(self, value: float):
        self.__std = value
        self._property_changed('std')        

    @property
    def slope(self) -> float:
        """Number in the range from -1000000000000 to 1000000000000"""
        return self.__slope

    @slope.setter
    def slope(self, value: float):
        self.__slope = value
        self._property_changed('slope')        


class RowGroup(Base):
        
    """Object specifying a group name and a list of assets to be calculated in a
       monitor"""
       
    def __init__(
        self,
        name: str,
        entity_ids: Tuple[str, ...],
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
        self.__name = value
        self._property_changed('name')        

    @property
    def movers(self) -> Movers:
        """Object that allows to specify the case in which we only want to return the n top
           or bottom entities"""
        return self.__movers

    @movers.setter
    def movers(self, value: Movers):
        self.__movers = value
        self._property_changed('movers')        

    @property
    def entity_ids(self) -> Tuple[str, ...]:
        """Array of entities that belong to the group"""
        return self.__entity_ids

    @entity_ids.setter
    def entity_ids(self, value: Tuple[str, ...]):
        self.__entity_ids = value
        self._property_changed('entity_ids')        

    @property
    def sort(self) -> Sort:
        """Object used to define sorting"""
        return self.__sort

    @sort.setter
    def sort(self, value: Sort):
        self.__sort = value
        self._property_changed('sort')        


class ColumnDefinition(Base):
        
    """Object defining the columns to be calculated in the monitor"""
       
    def __init__(
        self,
        render,
        name: str,
        enable_cell_flashing: bool = None,
        entity_property=None,
        function: Function = None,
        format_: ColumnFormat = None,
        width: float = None
    ):        
        super().__init__()
        self.enable_cell_flashing = enable_cell_flashing
        self.name = name
        self.render = render
        self.entity_property = entity_property
        self.function = function
        self.__format = format_
        self.width = width

    @property
    def enable_cell_flashing(self) -> bool:
        """Enable cell flashing for the column"""
        return self.__enable_cell_flashing

    @enable_cell_flashing.setter
    def enable_cell_flashing(self, value: bool):
        self.__enable_cell_flashing = value
        self._property_changed('enable_cell_flashing')        

    @property
    def name(self) -> str:
        """Column name"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def render(self):
        """Enum listing supported column definition render types"""
        return self.__render

    @render.setter
    def render(self, value):
        self.__render = value
        self._property_changed('render')        

    @property
    def entity_property(self):
        """Property to fetch from an entity"""
        return self.__entity_property

    @entity_property.setter
    def entity_property(self, value):
        self.__entity_property = value
        self._property_changed('entity_property')        

    @property
    def function(self) -> Function:
        """Function or Measure to be applied to the column."""
        return self.__function

    @function.setter
    def function(self, value: Function):
        self.__function = value
        self._property_changed('function')        

    @property
    def format(self) -> ColumnFormat:
        """Object used to specify the column formatting"""
        return self.__format

    @format.setter
    def format(self, value: ColumnFormat):
        self.__format = value
        self._property_changed('format')        

    @property
    def width(self) -> float:
        """Width of the column"""
        return self.__width

    @width.setter
    def width(self, value: float):
        self.__width = value
        self._property_changed('width')        


class RatesResponseData(Base):
        
    """Rates calculated response data."""
       
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
        self.__name = value
        self._property_changed('name')        

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value
        self._property_changed('id')        

    @property
    def libor_id(self) -> str:
        """Marquee unique identifier"""
        return self.__libor_id

    @libor_id.setter
    def libor_id(self, value: str):
        self.__libor_id = value
        self._property_changed('libor_id')        

    @property
    def rows(self) -> Tuple[RateRow, ...]:
        """Calculated rows for given rate ID"""
        return self.__rows

    @rows.setter
    def rows(self, value: Tuple[RateRow, ...]):
        self.__rows = value
        self._property_changed('rows')        


class MonitorParameters(Base):
        
    """Parameters provided for a monitor"""
       
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
        knot: float = None
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

    @property
    def column_definitions(self) -> Tuple[ColumnDefinition, ...]:
        """Array of monitor column definitions"""
        return self.__column_definitions

    @column_definitions.setter
    def column_definitions(self, value: Tuple[ColumnDefinition, ...]):
        self.__column_definitions = value
        self._property_changed('column_definitions')        

    @property
    def row_groups(self) -> Tuple[RowGroup, ...]:
        """Monitor row groups"""
        return self.__row_groups

    @row_groups.setter
    def row_groups(self, value: Tuple[RowGroup, ...]):
        self.__row_groups = value
        self._property_changed('row_groups')        

    @property
    def data_set_id(self) -> str:
        """ID of the dataset in which the monitor fetches data."""
        return self.__data_set_id

    @data_set_id.setter
    def data_set_id(self, value: str):
        self.__data_set_id = value
        self._property_changed('data_set_id')        

    @property
    def rebase_to_spot(self) -> bool:
        """Whether to rebase the output to the first rows values"""
        return self.__rebase_to_spot

    @rebase_to_spot.setter
    def rebase_to_spot(self, value: bool):
        self.__rebase_to_spot = value
        self._property_changed('rebase_to_spot')        

    @property
    def rebase_historical_curve(self) -> bool:
        """Whether to rebase the historical curve."""
        return self.__rebase_historical_curve

    @rebase_historical_curve.setter
    def rebase_historical_curve(self, value: bool):
        self.__rebase_historical_curve = value
        self._property_changed('rebase_historical_curve')        

    @property
    def meeting_after_next(self) -> bool:
        """For a given valuation date, toggle to pull the hikes/cuts priced in for the 2nd
           meeting after the valuation date over the past 3 months."""
        return self.__meeting_after_next

    @meeting_after_next.setter
    def meeting_after_next(self, value: bool):
        self.__meeting_after_next = value
        self._property_changed('meeting_after_next')        

    @property
    def next_meeting(self) -> bool:
        """For a given valuation date, toggle to pull the hikes/cuts priced in for the next
           meeting after the valuation date over the past 3 months."""
        return self.__next_meeting

    @next_meeting.setter
    def next_meeting(self, value: bool):
        self.__next_meeting = value
        self._property_changed('next_meeting')        

    @property
    def last_meeting(self) -> bool:
        """For a given valuation date, toggle to pull the hikes/cuts priced in for the last
           meeting before the valuation date over the past 3 months."""
        return self.__last_meeting

    @last_meeting.setter
    def last_meeting(self, value: bool):
        self.__last_meeting = value
        self._property_changed('last_meeting')        

    @property
    def rebase_to_end_of_year_spot(self) -> bool:
        """Whether to rebase to the EOY Forward."""
        return self.__rebase_to_end_of_year_spot

    @rebase_to_end_of_year_spot.setter
    def rebase_to_end_of_year_spot(self, value: bool):
        self.__rebase_to_end_of_year_spot = value
        self._property_changed('rebase_to_end_of_year_spot')        

    @property
    def filters(self) -> Tuple[WipiRequestFilter, ...]:
        """Filters for the dataset before returning the data response."""
        return self.__filters

    @filters.setter
    def filters(self, value: Tuple[WipiRequestFilter, ...]):
        self.__filters = value
        self._property_changed('filters')        

    @property
    def exportable(self) -> Tuple[str, ...]:
        """Permission to export monitor data."""
        return self.__exportable

    @exportable.setter
    def exportable(self, value: Tuple[str, ...]):
        self.__exportable = value
        self._property_changed('exportable')        

    @property
    def fill_column_index(self) -> float:
        """The Index to place the fill column. The Fill column is remaining white space in
           the monitor. Defaults to the last column."""
        return self.__fill_column_index

    @fill_column_index.setter
    def fill_column_index(self, value: float):
        self.__fill_column_index = value
        self._property_changed('fill_column_index')        

    @property
    def knot(self) -> float:
        """Used when rendering a chart component from the output, whether to display a knot
           in the chart configuration as a prop. Number represents size of the
           knot."""
        return self.__knot

    @knot.setter
    def knot(self, value: float):
        self.__knot = value
        self._property_changed('knot')        


class Monitor(Base):
        
    """A marquee monitor object"""
       
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
        self.__id = value
        self._property_changed('id')        

    @property
    def name(self) -> str:
        """Display name of monitor"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def type(self):
        """Enum listing supported entities"""
        return self.__type

    @type.setter
    def type(self, value):
        self.__type = value
        self._property_changed('type')        

    @property
    def parameters(self) -> MonitorParameters:
        """Parameters provided for a monitor"""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: MonitorParameters):
        self.__parameters = value
        self._property_changed('parameters')        

    @property
    def created_time(self) -> datetime.datetime:
        """Time created. ISO 8601 formatted string"""
        return self.__created_time

    @created_time.setter
    def created_time(self, value: datetime.datetime):
        self.__created_time = value
        self._property_changed('created_time')        

    @property
    def last_updated_time(self) -> datetime.datetime:
        """Timestamp of when the object was last updated"""
        return self.__last_updated_time

    @last_updated_time.setter
    def last_updated_time(self, value: datetime.datetime):
        self.__last_updated_time = value
        self._property_changed('last_updated_time')        

    @property
    def created_by_id(self) -> str:
        """Unique identifier of user who created the object"""
        return self.__created_by_id

    @created_by_id.setter
    def created_by_id(self, value: str):
        self.__created_by_id = value
        self._property_changed('created_by_id')        

    @property
    def last_updated_by_id(self) -> str:
        """Unique identifier of user who last updated the object"""
        return self.__last_updated_by_id

    @last_updated_by_id.setter
    def last_updated_by_id(self, value: str):
        self.__last_updated_by_id = value
        self._property_changed('last_updated_by_id')        

    @property
    def owner_id(self) -> str:
        """Marquee unique identifier"""
        return self.__owner_id

    @owner_id.setter
    def owner_id(self, value: str):
        self.__owner_id = value
        self._property_changed('owner_id')        

    @property
    def entitlements(self) -> Entitlements:
        """Defines the entitlements of a given resource"""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self.__entitlements = value
        self._property_changed('entitlements')        

    @property
    def folder_name(self) -> str:
        """Folder name of the monitor"""
        return self.__folder_name

    @folder_name.setter
    def folder_name(self, value: str):
        self.__folder_name = value
        self._property_changed('folder_name')        

    @property
    def polling_time(self) -> float:
        """Polling time to use in milliseconds."""
        return self.__polling_time

    @polling_time.setter
    def polling_time(self, value: float):
        self.__polling_time = value
        self._property_changed('polling_time')        

    @property
    def tags(self) -> Tuple[str, ...]:
        """Array of tag strings"""
        return self.__tags

    @tags.setter
    def tags(self, value: Tuple[str, ...]):
        self.__tags = value
        self._property_changed('tags')        
