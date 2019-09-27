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

from gs_quant.base import Base, get_enum_value
from gs_quant.target.common import *
from typing import Tuple, Union
import datetime


class ColumnFormat(Base):
        
    """Object used to specify the column formatting"""
       
    def __init__(
        self,
        precision: float,
        unit=None,
        human_readable: bool = None        
    ):
        super().__init__()
        self.__precision = precision
        self.__unit = unit
        self.__human_readable = human_readable

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


class Historical(Base):
        
    """value and date for historical data"""
       
    def __init__(
        self,
        value: Union[float, str] = None        
    ):
        super().__init__()
        self.__value = value

    @property
    def value(self) -> Union[float, str]:
        return self.__value

    @value.setter
    def value(self, value: Union[float, str]):
        self.__value = value
        self._property_changed('value')        


class IntervalCount(Base):
        
    """Defines the interval in which data is returned"""
       
    def __init__(
        self,
        count: float = None        
    ):
        super().__init__()
        self.__count = count

    @property
    def count(self) -> float:
        """Integer in the range from 0 to 10000"""
        return self.__count

    @count.setter
    def count(self, value: float):
        self.__count = value
        self._property_changed('count')        


class MaxDataPoints(Base):
        
    """Defines the max number of data points to be returned in equal intervals"""
       
    def __init__(
        self,
        max_data_points: float = None        
    ):
        super().__init__()
        self.__max_data_points = max_data_points

    @property
    def max_data_points(self) -> float:
        """Integer in the range from 0 to 10000"""
        return self.__max_data_points

    @max_data_points.setter
    def max_data_points(self, value: float):
        self.__max_data_points = value
        self._property_changed('max_data_points')        


class MonitorResponseData(Base):
        
    """Monitor calculated response data"""
       
    def __init__(
        self,
        id: str,
        result: dict        
    ):
        super().__init__()
        self.__id = id
        self.__result = result

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
        
    """Object that allows to specify the case in which we only want to return the n top or bottom entities"""
       
    def __init__(
        self,
        column_name: str,
        top: float = None,
        bottom: float = None        
    ):
        super().__init__()
        self.__top = top
        self.__bottom = bottom
        self.__column_name = column_name

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
        type=None,
        direction=None        
    ):
        super().__init__()
        self.__type = type
        self.__column_name = column_name
        self.__direction = direction

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
        type=None        
    ):
        super().__init__()
        self.__column = column
        self.__operation = operation
        self.__value = value
        self.__type = type

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
        """The value of the operation is used with. Relative dates are used against the last valuationDate."""
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


class FunctionParameters(Base):
        
    """Function parameters to be passed"""
       
    def __init__(
        self,
        period=None,
        intervals: dict = None        
    ):
        super().__init__()
        self.__period = period
        self.__intervals = intervals

    @property
    def period(self):
        """Enum listing supported parameter periods"""
        return self.__period

    @period.setter
    def period(self, value):
        self.__period = value
        self._property_changed('period')        

    @property
    def intervals(self) -> dict:
        return self.__intervals

    @intervals.setter
    def intervals(self, value: dict):
        self.__intervals = value
        self._property_changed('intervals')        


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
        self.__period = period
        self.__last = last
        self.__historical = historical
        self.__change = change
        self.__percentage_change = percentage_change
        self.__std = std
        self.__slope = slope

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
        
    """Object specifying a group name and a list of assets to be calculated in a monitor"""
       
    def __init__(
        self,
        name: str,
        entity_ids: Tuple[str, ...],
        movers: Movers = None,
        sort: Sort = None        
    ):
        super().__init__()
        self.__name = name
        self.__movers = movers
        self.__entity_ids = entity_ids
        self.__sort = sort

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
        """Object that allows to specify the case in which we only want to return the n top or bottom entities"""
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


class Function(Base):
        
    """Function or Measure to be applied to the column."""
       
    def __init__(
        self,
        measure: str,
        frequency,
        name: str = None,
        start_date: str = None,
        parameters: FunctionParameters = None        
    ):
        super().__init__()
        self.__name = name
        self.__measure = measure
        self.__frequency = frequency
        self.__start_date = start_date
        self.__parameters = parameters

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
        """The frequency of the column data changes which dataset the values are retrieved from."""
        return self.__frequency

    @frequency.setter
    def frequency(self, value):
        self.__frequency = value
        self._property_changed('frequency')        

    @property
    def start_date(self) -> str:
        """The relative date for columns requiring historical data. Eg: -1y."""
        return self.__start_date

    @start_date.setter
    def start_date(self, value: str):
        self.__start_date = value
        self._property_changed('start_date')        

    @property
    def parameters(self) -> FunctionParameters:
        """Function parameters to be passed"""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: FunctionParameters):
        self.__parameters = value
        self._property_changed('parameters')        


class RatesResponseData(Base):
        
    """Rates calculated response data."""
       
    def __init__(
        self,
        name,
        id: str,
        rows: Tuple[RateRow, ...],
        libor_id: str = None        
    ):
        super().__init__()
        self.__name = name
        self.__id = id
        self.__libor_id = libor_id
        self.__rows = rows

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


class ColumnDefinition(Base):
        
    """Object defining the columns to be calculated in the monitor"""
       
    def __init__(
        self,
        render,
        name: str,
        enable_cell_flashing: bool = None,
        entity_property=None,
        function: Function = None,
        format: ColumnFormat = None,
        width: float = None        
    ):
        super().__init__()
        self.__enable_cell_flashing = enable_cell_flashing
        self.__name = name
        self.__render = render
        self.__entity_property = entity_property
        self.__function = function
        self.__format = format
        self.__width = width

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
        filters: Tuple[WipiRequestFilter, ...] = None        
    ):
        super().__init__()
        self.__column_definitions = column_definitions
        self.__row_groups = row_groups
        self.__data_set_id = data_set_id
        self.__rebase_to_spot = rebase_to_spot
        self.__rebase_historical_curve = rebase_historical_curve
        self.__meeting_after_next = meeting_after_next
        self.__next_meeting = next_meeting
        self.__last_meeting = last_meeting
        self.__rebase_to_end_of_year_spot = rebase_to_end_of_year_spot
        self.__filters = filters

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
        """For a given valuation date, toggle to pull the hikes/cuts priced in for the 2nd meeting after the valuation date over the past 3 months."""
        return self.__meeting_after_next

    @meeting_after_next.setter
    def meeting_after_next(self, value: bool):
        self.__meeting_after_next = value
        self._property_changed('meeting_after_next')        

    @property
    def next_meeting(self) -> bool:
        """For a given valuation date, toggle to pull the hikes/cuts priced in for the next meeting after the valuation date over the past 3 months."""
        return self.__next_meeting

    @next_meeting.setter
    def next_meeting(self, value: bool):
        self.__next_meeting = value
        self._property_changed('next_meeting')        

    @property
    def last_meeting(self) -> bool:
        """For a given valuation date, toggle to pull the hikes/cuts priced in for the last meeting before the valuation date over the past 3 months."""
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


class Monitor(Base):
        
    """A marquee monitor object"""
       
    def __init__(
        self,
        name: str,
        type,
        id: str = None,
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
        self.__id = id
        self.__name = name
        self.__type = type
        self.__parameters = parameters
        self.__created_time = created_time
        self.__last_updated_time = last_updated_time
        self.__created_by_id = created_by_id
        self.__last_updated_by_id = last_updated_by_id
        self.__owner_id = owner_id
        self.__entitlements = entitlements
        self.__folder_name = folder_name
        self.__polling_time = polling_time
        self.__tags = tags

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
