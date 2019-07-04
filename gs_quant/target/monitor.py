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
       
    def __init__(self, precision: float, unit=None, humanReadable: bool = None):
        super().__init__()
        self.__precision = precision
        self.__unit = unit
        self.__humanReadable = humanReadable

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
    def humanReadable(self) -> bool:
        """Formats number to have commas"""
        return self.__humanReadable

    @humanReadable.setter
    def humanReadable(self, value: bool):
        self.__humanReadable = value
        self._property_changed('humanReadable')        


class Historical(Base):
        
    """value and date for historical data"""
       
    def __init__(self, value: Union[float, str] = None):
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
       
    def __init__(self, count: float = None):
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
       
    def __init__(self, maxDataPoints: float = None):
        super().__init__()
        self.__maxDataPoints = maxDataPoints

    @property
    def maxDataPoints(self) -> float:
        """Integer in the range from 0 to 10000"""
        return self.__maxDataPoints

    @maxDataPoints.setter
    def maxDataPoints(self, value: float):
        self.__maxDataPoints = value
        self._property_changed('maxDataPoints')        


class Metadata(Base):
        
    """Entity metadata"""
       
    def __init__(self, tooltip: str = None):
        super().__init__()
        self.__tooltip = tooltip

    @property
    def tooltip(self) -> str:
        """Required small string with a length from empty string to 50 characters"""
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self.__tooltip = value
        self._property_changed('tooltip')        


class Movers(Base):
        
    """Object that allows to specify the case in which we only want to return the n top or bottom entities"""
       
    def __init__(self, columnName: str, top: float = None, bottom: float = None):
        super().__init__()
        self.__top = top
        self.__bottom = bottom
        self.__columnName = columnName

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
    def columnName(self) -> str:
        """Required small string with a length from empty string to 50 characters"""
        return self.__columnName

    @columnName.setter
    def columnName(self, value: str):
        self.__columnName = value
        self._property_changed('columnName')        


class Sort(Base):
        
    """Object used to define sorting"""
       
    def __init__(self, columnName: str, type=None, direction=None):
        super().__init__()
        self.__type = type
        self.__columnName = columnName
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
    def columnName(self) -> str:
        """Required small string with a length from empty string to 50 characters"""
        return self.__columnName

    @columnName.setter
    def columnName(self, value: str):
        self.__columnName = value
        self._property_changed('columnName')        

    @property
    def direction(self):
        """Enum with available sort directions"""
        return self.__direction

    @direction.setter
    def direction(self, value):
        self.__direction = value
        self._property_changed('direction')        


class FunctionParameters(Base):
        
    """Function parameters to be passed"""
       
    def __init__(self, period=None, intervals: dict = None):
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
       
    def __init__(self, period, last: float, change: float, std: float, slope: float, historical: Historical = None, percentageChange: float = None):
        super().__init__()
        self.__period = period
        self.__last = last
        self.__historical = historical
        self.__change = change
        self.__percentageChange = percentageChange
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
    def percentageChange(self) -> float:
        """One day prince change in percentage"""
        return self.__percentageChange

    @percentageChange.setter
    def percentageChange(self, value: float):
        self.__percentageChange = value
        self._property_changed('percentageChange')        

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


class RowData(Base):
        
    """Calculated row data for a particular asset"""
       
    def __init__(self, GENERATED_INVALID: dict = None):
        super().__init__()
        self.__GENERATED_INVALID = GENERATED_INVALID

    @property
    def GENERATED_INVALID(self) -> dict:
        """timestamp and value for calculated field"""
        return self.__GENERATED_INVALID

    @GENERATED_INVALID.setter
    def GENERATED_INVALID(self, value: dict):
        self.__GENERATED_INVALID = value
        self._property_changed('GENERATED_INVALID')        


class RowGroup(Base):
        
    """Object specifying a group name and a list of assets to be calculated in a monitor"""
       
    def __init__(self, name: str, entityIds: Tuple[str, ...], movers: Movers = None, sort: Sort = None):
        super().__init__()
        self.__name = name
        self.__movers = movers
        self.__entityIds = entityIds
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
    def entityIds(self) -> Tuple[str, ...]:
        """Array of entities that belong to the group"""
        return self.__entityIds

    @entityIds.setter
    def entityIds(self, value: Tuple[str, ...]):
        self.__entityIds = value
        self._property_changed('entityIds')        

    @property
    def sort(self) -> Sort:
        """Object used to define sorting"""
        return self.__sort

    @sort.setter
    def sort(self, value: Sort):
        self.__sort = value
        self._property_changed('sort')        


class Function(Base):
        
    """Function to be applied"""
       
    def __init__(self, name, parameters: FunctionParameters = None):
        super().__init__()
        self.__name = name
        self.__parameters = parameters

    @property
    def name(self):
        """Enum listing supported functions for monitor calculations"""
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value
        self._property_changed('name')        

    @property
    def parameters(self) -> FunctionParameters:
        """Function parameters to be passed"""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: FunctionParameters):
        self.__parameters = value
        self._property_changed('parameters')        


class MonitorResponseData(Base):
        
    """Monitor calculated response data"""
       
    def __init__(self, id: str, result: dict):
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


class RatesResponseData(Base):
        
    """Rates calculated response data"""
       
    def __init__(self, name, id: str, rows: Tuple[RateRow, ...], libor_id: str = None):
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
       
    def __init__(self, render, name: str, enableCellFlashing: bool = None, entityProperty=None, function: Function = None, format: ColumnFormat = None, width: float = None):
        super().__init__()
        self.__enableCellFlashing = enableCellFlashing
        self.__name = name
        self.__render = render
        self.__entityProperty = entityProperty
        self.__function = function
        self.__format = format
        self.__width = width

    @property
    def enableCellFlashing(self) -> bool:
        """Enable cell flashing for the column"""
        return self.__enableCellFlashing

    @enableCellFlashing.setter
    def enableCellFlashing(self, value: bool):
        self.__enableCellFlashing = value
        self._property_changed('enableCellFlashing')        

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
    def entityProperty(self):
        """Property to fetch from an entity"""
        return self.__entityProperty

    @entityProperty.setter
    def entityProperty(self, value):
        self.__entityProperty = value
        self._property_changed('entityProperty')        

    @property
    def function(self) -> Function:
        """Function to be applied"""
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
       
    def __init__(self, columnDefinitions: Tuple[ColumnDefinition, ...], rowGroups: Tuple[RowGroup, ...]):
        super().__init__()
        self.__columnDefinitions = columnDefinitions
        self.__rowGroups = rowGroups

    @property
    def columnDefinitions(self) -> Tuple[ColumnDefinition, ...]:
        """Array of monitor column definitions"""
        return self.__columnDefinitions

    @columnDefinitions.setter
    def columnDefinitions(self, value: Tuple[ColumnDefinition, ...]):
        self.__columnDefinitions = value
        self._property_changed('columnDefinitions')        

    @property
    def rowGroups(self) -> Tuple[RowGroup, ...]:
        """Monitor row groups"""
        return self.__rowGroups

    @rowGroups.setter
    def rowGroups(self, value: Tuple[RowGroup, ...]):
        self.__rowGroups = value
        self._property_changed('rowGroups')        


class Monitor(Base):
        
    """A marquee monitor object"""
       
    def __init__(self, name: str, type, id: str = None, parameters: MonitorParameters = None, createdTime: datetime.datetime = None, lastUpdatedTime: datetime.datetime = None, createdById: str = None, lastUpdatedById: str = None, ownerId: str = None, entitlements: Entitlements = None, folderName: str = None, pollingTime: float = None, tags: Tuple[str, ...] = None):
        super().__init__()
        self.__id = id
        self.__name = name
        self.__type = type
        self.__parameters = parameters
        self.__createdTime = createdTime
        self.__lastUpdatedTime = lastUpdatedTime
        self.__createdById = createdById
        self.__lastUpdatedById = lastUpdatedById
        self.__ownerId = ownerId
        self.__entitlements = entitlements
        self.__folderName = folderName
        self.__pollingTime = pollingTime
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
    def createdTime(self) -> datetime.datetime:
        """Time created. ISO 8601 formatted string"""
        return self.__createdTime

    @createdTime.setter
    def createdTime(self, value: datetime.datetime):
        self.__createdTime = value
        self._property_changed('createdTime')        

    @property
    def lastUpdatedTime(self) -> datetime.datetime:
        """Timestamp of when the object was last updated"""
        return self.__lastUpdatedTime

    @lastUpdatedTime.setter
    def lastUpdatedTime(self, value: datetime.datetime):
        self.__lastUpdatedTime = value
        self._property_changed('lastUpdatedTime')        

    @property
    def createdById(self) -> str:
        """Unique identifier of user who created the object"""
        return self.__createdById

    @createdById.setter
    def createdById(self, value: str):
        self.__createdById = value
        self._property_changed('createdById')        

    @property
    def lastUpdatedById(self) -> str:
        """Unique identifier of user who last updated the object"""
        return self.__lastUpdatedById

    @lastUpdatedById.setter
    def lastUpdatedById(self, value: str):
        self.__lastUpdatedById = value
        self._property_changed('lastUpdatedById')        

    @property
    def ownerId(self) -> str:
        """Marquee unique identifier"""
        return self.__ownerId

    @ownerId.setter
    def ownerId(self, value: str):
        self.__ownerId = value
        self._property_changed('ownerId')        

    @property
    def entitlements(self) -> Entitlements:
        """Defines the entitlements of a given resource"""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self.__entitlements = value
        self._property_changed('entitlements')        

    @property
    def folderName(self) -> str:
        """Folder name of the monitor"""
        return self.__folderName

    @folderName.setter
    def folderName(self, value: str):
        self.__folderName = value
        self._property_changed('folderName')        

    @property
    def pollingTime(self) -> float:
        """Polling time to use in milliseconds."""
        return self.__pollingTime

    @pollingTime.setter
    def pollingTime(self, value: float):
        self.__pollingTime = value
        self._property_changed('pollingTime')        

    @property
    def tags(self) -> Tuple[str, ...]:
        """Array of tag strings"""
        return self.__tags

    @tags.setter
    def tags(self, value: Tuple[str, ...]):
        self.__tags = value
        self._property_changed('tags')        
