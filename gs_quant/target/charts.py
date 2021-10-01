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


class ChartAnnotationFontStyle(EnumBase, Enum):    
    
    """Style of the font."""

    italic = 'italic'
    normal = 'normal'    


class ChartAnnotationFontWeight(EnumBase, Enum):    
    
    """Weight of the font."""

    bold = 'bold'
    normal = 'normal'    


class ChartAnnotationLineType(EnumBase, Enum):    
    
    """Type of the line."""

    dashed = 'dashed'
    solid = 'solid'    


class ChartAnnotationTextAlign(EnumBase, Enum):    
    
    """Alignment of the text."""

    center = 'center'
    left = 'left'
    right = 'right'    


class ChartAnnotationTextDecoration(EnumBase, Enum):    
    
    """Decoration of the text."""

    none = 'none'
    underline = 'underline'
    strike_through = 'strike-through'    


class ChartAnnotationType(EnumBase, Enum):    
    
    """Type of the annotation."""

    arrow = 'arrow'
    circle = 'circle'
    line = 'line'
    oval = 'oval'
    range = 'range'
    rect = 'rect'
    text = 'text'    


class ChartFill(EnumBase, Enum):    
    
    """Chart Fill Type"""

    _None = 'None'
    Solid = 'Solid'
    Gradient = 'Gradient'    


class ChartLineDrawType(EnumBase, Enum):    
    
    """Line Draw Type"""

    Area = 'Area'
    Bars = 'Bars'
    Candlesticks = 'Candlesticks'
    Lines = 'Lines'
    _None = 'None'
    StepAfter = 'StepAfter'
    StepBefore = 'StepBefore'
    StepLinear = 'StepLinear'
    Volumes = 'Volumes'    


class ChartLineType(EnumBase, Enum):    
    
    """Line Type"""

    Bubble = 'Bubble'
    Solid = 'Solid'
    Knotted = 'Knotted'
    Dashed = 'Dashed'    


class ChartRegressionStrokeType(EnumBase, Enum):    
    
    """Chart Regression Stroke Type"""

    Line = 'Line'
    Dash = 'Dash'    


class ChartRegressionType(EnumBase, Enum):    
    
    """Chart Regression Type"""

    Linear = 'Linear'
    Exponential = 'Exponential'
    PlotData = 'PlotData'    


class ChartType(EnumBase, Enum):    
    
    """Chart Type"""

    line = 'line'
    scatter = 'scatter'    


class ChartDisplaySettings(Base):
        
    """An object with the chart display settings."""

    @camel_case_translate
    def __init__(
        self,
        scatter_fill: bool = None,
        name: str = None
    ):        
        super().__init__()
        self.scatter_fill = scatter_fill
        self.name = name

    @property
    def scatter_fill(self) -> bool:
        """Scatter plot Fill Type."""
        return self.__scatter_fill

    @scatter_fill.setter
    def scatter_fill(self, value: bool):
        self._property_changed('scatter_fill')
        self.__scatter_fill = value        


class ChartLabelSettings(Base):
        
    """An object with the chart label settings."""

    @camel_case_translate
    def __init__(
        self,
        hide_last_value_labels: bool = None,
        name: str = None
    ):        
        super().__init__()
        self.hide_last_value_labels = hide_last_value_labels
        self.name = name

    @property
    def hide_last_value_labels(self) -> bool:
        """Whether to hide the last value label for all series on a chart."""
        return self.__hide_last_value_labels

    @hide_last_value_labels.setter
    def hide_last_value_labels(self, value: bool):
        self._property_changed('hide_last_value_labels')
        self.__hide_last_value_labels = value        


class ChartProperties(Base):
        
    """An object which chart properties"""

    @camel_case_translate
    def __init__(
        self,
        x: str = None,
        x_label: str = None,
        y: str = None,
        y_label: str = None,
        color: str = None,
        shape: str = None,
        name: str = None
    ):        
        super().__init__()
        self.x = x
        self.x_label = x_label
        self.y = y
        self.y_label = y_label
        self.color = color
        self.shape = shape
        self.name = name

    @property
    def x(self) -> str:
        return self.__x

    @x.setter
    def x(self, value: str):
        self._property_changed('x')
        self.__x = value        

    @property
    def x_label(self) -> str:
        return self.__x_label

    @x_label.setter
    def x_label(self, value: str):
        self._property_changed('x_label')
        self.__x_label = value        

    @property
    def y(self) -> str:
        return self.__y

    @y.setter
    def y(self, value: str):
        self._property_changed('y')
        self.__y = value        

    @property
    def y_label(self) -> str:
        return self.__y_label

    @y_label.setter
    def y_label(self, value: str):
        self._property_changed('y_label')
        self.__y_label = value        

    @property
    def color(self) -> str:
        return self.__color

    @color.setter
    def color(self, value: str):
        self._property_changed('color')
        self.__color = value        

    @property
    def shape(self) -> str:
        return self.__shape

    @shape.setter
    def shape(self, value: str):
        self._property_changed('shape')
        self.__shape = value        


class ChartShare(Base):
        
    """Share With View Entitlement Object only for Chart"""

    @camel_case_translate
    def __init__(
        self,
        guids: Tuple[str, ...] = None,
        version: int = None,
        name: str = None
    ):        
        super().__init__()
        self.guids = guids
        self.version = version
        self.name = name

    @property
    def guids(self) -> Tuple[str, ...]:
        """Array of guid"""
        return self.__guids

    @guids.setter
    def guids(self, value: Tuple[str, ...]):
        self._property_changed('guids')
        self.__guids = value        

    @property
    def version(self) -> int:
        """Chart Object Version"""
        return self.__version

    @version.setter
    def version(self, value: int):
        self._property_changed('version')
        self.__version = value        


class ChartTime(Base):
        
    """An object which contains all the time settings."""

    @camel_case_translate
    def __init__(
        self,
        start: str = None,
        end: str = None,
        timezone: str = None,
        name: str = None
    ):        
        super().__init__()
        self.start = start
        self.end = end
        self.timezone = timezone
        self.name = name

    @property
    def start(self) -> str:
        """Start time in hh:mm:ss format"""
        return self.__start

    @start.setter
    def start(self, value: str):
        self._property_changed('start')
        self.__start = value        

    @property
    def end(self) -> str:
        """End time in hh:mm:ss format"""
        return self.__end

    @end.setter
    def end(self, value: str):
        self._property_changed('end')
        self.__end = value        

    @property
    def timezone(self) -> str:
        """The timezone to use"""
        return self.__timezone

    @timezone.setter
    def timezone(self, value: str):
        self._property_changed('timezone')
        self.__timezone = value        


class XAxisSettings(Base):
        
    """An object which contains all the settings for the X axis"""

    @camel_case_translate
    def __init__(
        self,
        auto_fit_range_to_data: bool = None,
        show_grid_lines: bool = None,
        x_axis_date_format: str = None,
        name: str = None
    ):        
        super().__init__()
        self.auto_fit_range_to_data = auto_fit_range_to_data
        self.show_grid_lines = show_grid_lines
        self.x_axis_date_format = x_axis_date_format
        self.name = name

    @property
    def auto_fit_range_to_data(self) -> bool:
        return self.__auto_fit_range_to_data

    @auto_fit_range_to_data.setter
    def auto_fit_range_to_data(self, value: bool):
        self._property_changed('auto_fit_range_to_data')
        self.__auto_fit_range_to_data = value        

    @property
    def show_grid_lines(self) -> bool:
        return self.__show_grid_lines

    @show_grid_lines.setter
    def show_grid_lines(self, value: bool):
        self._property_changed('show_grid_lines')
        self.__show_grid_lines = value        

    @property
    def x_axis_date_format(self) -> str:
        return self.__x_axis_date_format

    @x_axis_date_format.setter
    def x_axis_date_format(self, value: str):
        self._property_changed('x_axis_date_format')
        self.__x_axis_date_format = value        


class YAxisSettings(Base):
        
    """An object which contains all the settings for a Y axis."""

    @camel_case_translate
    def __init__(
        self,
        decimal_precision: int = None,
        id_: str = None,
        label: str = None,
        label_format: str = None,
        max_: int = None,
        min_: int = None,
        show_grid_lines: bool = None,
        hide: bool = None,
        name: str = None
    ):        
        super().__init__()
        self.decimal_precision = decimal_precision
        self.__id = id_
        self.label = label
        self.label_format = label_format
        self.__max = max_
        self.__min = min_
        self.show_grid_lines = show_grid_lines
        self.hide = hide
        self.name = name

    @property
    def decimal_precision(self) -> int:
        """Number of decimals displayed for value labels on all the series on this Y axis."""
        return self.__decimal_precision

    @decimal_precision.setter
    def decimal_precision(self, value: int):
        self._property_changed('decimal_precision')
        self.__decimal_precision = value        

    @property
    def id(self) -> str:
        """The unique ID of the axis."""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def label(self) -> str:
        """The label to display on the axis"""
        return self.__label

    @label.setter
    def label(self, value: str):
        self._property_changed('label')
        self.__label = value        

    @property
    def label_format(self) -> str:
        """The format to apply to the Y axis ticks."""
        return self.__label_format

    @label_format.setter
    def label_format(self, value: str):
        self._property_changed('label_format')
        self.__label_format = value        

    @property
    def max(self) -> int:
        """Maximum Y axis tick value."""
        return self.__max

    @max.setter
    def max(self, value: int):
        self._property_changed('max')
        self.__max = value        

    @property
    def min(self) -> int:
        """Minimum Y axis tick value."""
        return self.__min

    @min.setter
    def min(self, value: int):
        self._property_changed('min')
        self.__min = value        

    @property
    def show_grid_lines(self) -> bool:
        """Whether or not the grid lines for this axis will be rendered on the chart."""
        return self.__show_grid_lines

    @show_grid_lines.setter
    def show_grid_lines(self, value: bool):
        self._property_changed('show_grid_lines')
        self.__show_grid_lines = value        

    @property
    def hide(self) -> bool:
        """Whether or not the axis lines will be rendered on the chart."""
        return self.__hide

    @hide.setter
    def hide(self, value: bool):
        self._property_changed('hide')
        self.__hide = value        


class ChartAnnotation(Base):
        
    """An object that represents an annotation on a chart."""

    @camel_case_translate
    def __init__(
        self,
        id_: str,
        type_: Union[ChartAnnotationType, str] = None,
        chart_type: Union[ChartType, str] = None,
        start_time: datetime.datetime = None,
        end_time: datetime.datetime = None,
        start_value: str = None,
        end_value: str = None,
        color: str = None,
        is_proportional: bool = False,
        fill_color: str = None,
        font_size: float = None,
        font_style: Union[ChartAnnotationFontStyle, str] = None,
        font_weight: Union[ChartAnnotationFontWeight, str] = None,
        label: str = None,
        line_height: float = None,
        line_type: Union[ChartAnnotationLineType, str] = None,
        line_width: float = None,
        radius: float = None,
        text_align: Union[ChartAnnotationTextAlign, str] = None,
        text_decoration: Union[ChartAnnotationTextDecoration, str] = None,
        text_width: float = None,
        y_axis_index: float = None,
        name: str = None
    ):        
        super().__init__()
        self.__id = id_
        self.__type = get_enum_value(ChartAnnotationType, type_)
        self.chart_type = chart_type
        self.start_time = start_time
        self.end_time = end_time
        self.start_value = start_value
        self.end_value = end_value
        self.color = color
        self.is_proportional = is_proportional
        self.fill_color = fill_color
        self.font_size = font_size
        self.font_style = font_style
        self.font_weight = font_weight
        self.label = label
        self.line_height = line_height
        self.line_type = line_type
        self.line_width = line_width
        self.radius = radius
        self.text_align = text_align
        self.text_decoration = text_decoration
        self.text_width = text_width
        self.y_axis_index = y_axis_index
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
    def type(self) -> Union[ChartAnnotationType, str]:
        """Type of the annotation."""
        return self.__type

    @type.setter
    def type(self, value: Union[ChartAnnotationType, str]):
        self._property_changed('type')
        self.__type = get_enum_value(ChartAnnotationType, value)        

    @property
    def chart_type(self) -> Union[ChartType, str]:
        """Chart Type"""
        return self.__chart_type

    @chart_type.setter
    def chart_type(self, value: Union[ChartType, str]):
        self._property_changed('chart_type')
        self.__chart_type = get_enum_value(ChartType, value)        

    @property
    def start_time(self) -> datetime.datetime:
        """Start time of the annotation."""
        return self.__start_time

    @start_time.setter
    def start_time(self, value: datetime.datetime):
        self._property_changed('start_time')
        self.__start_time = value        

    @property
    def end_time(self) -> datetime.datetime:
        """End time of the annotation."""
        return self.__end_time

    @end_time.setter
    def end_time(self, value: datetime.datetime):
        self._property_changed('end_time')
        self.__end_time = value        

    @property
    def start_value(self) -> str:
        """Starting value of the annotation."""
        return self.__start_value

    @start_value.setter
    def start_value(self, value: str):
        self._property_changed('start_value')
        self.__start_value = value        

    @property
    def end_value(self) -> str:
        """Ending value of the annotation."""
        return self.__end_value

    @end_value.setter
    def end_value(self, value: str):
        self._property_changed('end_value')
        self.__end_value = value        

    @property
    def color(self) -> str:
        """Color of the shape."""
        return self.__color

    @color.setter
    def color(self, value: str):
        self._property_changed('color')
        self.__color = value        

    @property
    def is_proportional(self) -> bool:
        """The proportional relationship of the width and height"""
        return self.__is_proportional

    @is_proportional.setter
    def is_proportional(self, value: bool):
        self._property_changed('is_proportional')
        self.__is_proportional = value        

    @property
    def fill_color(self) -> str:
        """Fill color of the shape."""
        return self.__fill_color

    @fill_color.setter
    def fill_color(self, value: str):
        self._property_changed('fill_color')
        self.__fill_color = value        

    @property
    def font_size(self) -> float:
        """Size of the font."""
        return self.__font_size

    @font_size.setter
    def font_size(self, value: float):
        self._property_changed('font_size')
        self.__font_size = value        

    @property
    def font_style(self) -> Union[ChartAnnotationFontStyle, str]:
        """Style of the font."""
        return self.__font_style

    @font_style.setter
    def font_style(self, value: Union[ChartAnnotationFontStyle, str]):
        self._property_changed('font_style')
        self.__font_style = get_enum_value(ChartAnnotationFontStyle, value)        

    @property
    def font_weight(self) -> Union[ChartAnnotationFontWeight, str]:
        """Weight of the font."""
        return self.__font_weight

    @font_weight.setter
    def font_weight(self, value: Union[ChartAnnotationFontWeight, str]):
        self._property_changed('font_weight')
        self.__font_weight = get_enum_value(ChartAnnotationFontWeight, value)        

    @property
    def label(self) -> str:
        """Label of the text annotation."""
        return self.__label

    @label.setter
    def label(self, value: str):
        self._property_changed('label')
        self.__label = value        

    @property
    def line_height(self) -> float:
        """Height of the line."""
        return self.__line_height

    @line_height.setter
    def line_height(self, value: float):
        self._property_changed('line_height')
        self.__line_height = value        

    @property
    def line_type(self) -> Union[ChartAnnotationLineType, str]:
        """Type of the line."""
        return self.__line_type

    @line_type.setter
    def line_type(self, value: Union[ChartAnnotationLineType, str]):
        self._property_changed('line_type')
        self.__line_type = get_enum_value(ChartAnnotationLineType, value)        

    @property
    def line_width(self) -> float:
        """Width of the line."""
        return self.__line_width

    @line_width.setter
    def line_width(self, value: float):
        self._property_changed('line_width')
        self.__line_width = value        

    @property
    def radius(self) -> float:
        """Radius of the circle annotation."""
        return self.__radius

    @radius.setter
    def radius(self, value: float):
        self._property_changed('radius')
        self.__radius = value        

    @property
    def text_align(self) -> Union[ChartAnnotationTextAlign, str]:
        """Alignment of the text."""
        return self.__text_align

    @text_align.setter
    def text_align(self, value: Union[ChartAnnotationTextAlign, str]):
        self._property_changed('text_align')
        self.__text_align = get_enum_value(ChartAnnotationTextAlign, value)        

    @property
    def text_decoration(self) -> Union[ChartAnnotationTextDecoration, str]:
        """Decoration of the text."""
        return self.__text_decoration

    @text_decoration.setter
    def text_decoration(self, value: Union[ChartAnnotationTextDecoration, str]):
        self._property_changed('text_decoration')
        self.__text_decoration = get_enum_value(ChartAnnotationTextDecoration, value)        

    @property
    def text_width(self) -> float:
        """Width of the text annotation container."""
        return self.__text_width

    @text_width.setter
    def text_width(self, value: float):
        self._property_changed('text_width')
        self.__text_width = value        

    @property
    def y_axis_index(self) -> float:
        """Y axis index annotation is tied to."""
        return self.__y_axis_index

    @y_axis_index.setter
    def y_axis_index(self, value: float):
        self._property_changed('y_axis_index')
        self.__y_axis_index = value        


class ChartExpression(Base):
        
    """An object which represent the single chart expression row"""

    @camel_case_translate
    def __init__(
        self,
        axis: str = None,
        color: str = None,
        delete_gap: bool = None,
        delete_weekends: bool = None,
        digits: float = None,
        disable: bool = None,
        fill: Union[ChartFill, str] = None,
        has_x_grid: bool = None,
        has_y_grid: bool = None,
        show_statistics: bool = None,
        hide: bool = None,
        label: str = None,
        line_type: Union[ChartLineType, str] = None,
        line_draw_type: Union[ChartLineDrawType, str] = None,
        line_transparency: float = None,
        line_width: float = None,
        x_label: str = None,
        y_label: str = None,
        name: str = None
    ):        
        super().__init__()
        self.axis = axis
        self.color = color
        self.delete_gap = delete_gap
        self.delete_weekends = delete_weekends
        self.digits = digits
        self.disable = disable
        self.fill = fill
        self.has_x_grid = has_x_grid
        self.has_y_grid = has_y_grid
        self.show_statistics = show_statistics
        self.hide = hide
        self.label = label
        self.line_type = line_type
        self.line_draw_type = line_draw_type
        self.line_transparency = line_transparency
        self.line_width = line_width
        self.x_label = x_label
        self.y_label = y_label
        self.name = name

    @property
    def axis(self) -> str:
        return self.__axis

    @axis.setter
    def axis(self, value: str):
        self._property_changed('axis')
        self.__axis = value        

    @property
    def color(self) -> str:
        return self.__color

    @color.setter
    def color(self, value: str):
        self._property_changed('color')
        self.__color = value        

    @property
    def delete_gap(self) -> bool:
        return self.__delete_gap

    @delete_gap.setter
    def delete_gap(self, value: bool):
        self._property_changed('delete_gap')
        self.__delete_gap = value        

    @property
    def delete_weekends(self) -> bool:
        return self.__delete_weekends

    @delete_weekends.setter
    def delete_weekends(self, value: bool):
        self._property_changed('delete_weekends')
        self.__delete_weekends = value        

    @property
    def digits(self) -> float:
        """The number of digits to appear after the decimal point"""
        return self.__digits

    @digits.setter
    def digits(self, value: float):
        self._property_changed('digits')
        self.__digits = value        

    @property
    def disable(self) -> bool:
        return self.__disable

    @disable.setter
    def disable(self, value: bool):
        self._property_changed('disable')
        self.__disable = value        

    @property
    def fill(self) -> Union[ChartFill, str]:
        """Chart Fill Type"""
        return self.__fill

    @fill.setter
    def fill(self, value: Union[ChartFill, str]):
        self._property_changed('fill')
        self.__fill = get_enum_value(ChartFill, value)        

    @property
    def has_x_grid(self) -> bool:
        return self.__has_x_grid

    @has_x_grid.setter
    def has_x_grid(self, value: bool):
        self._property_changed('has_x_grid')
        self.__has_x_grid = value        

    @property
    def has_y_grid(self) -> bool:
        return self.__has_y_grid

    @has_y_grid.setter
    def has_y_grid(self, value: bool):
        self._property_changed('has_y_grid')
        self.__has_y_grid = value        

    @property
    def show_statistics(self) -> bool:
        return self.__show_statistics

    @show_statistics.setter
    def show_statistics(self, value: bool):
        self._property_changed('show_statistics')
        self.__show_statistics = value        

    @property
    def hide(self) -> bool:
        return self.__hide

    @hide.setter
    def hide(self, value: bool):
        self._property_changed('hide')
        self.__hide = value        

    @property
    def label(self) -> str:
        return self.__label

    @label.setter
    def label(self, value: str):
        self._property_changed('label')
        self.__label = value        

    @property
    def line_type(self) -> Union[ChartLineType, str]:
        """Line Type"""
        return self.__line_type

    @line_type.setter
    def line_type(self, value: Union[ChartLineType, str]):
        self._property_changed('line_type')
        self.__line_type = get_enum_value(ChartLineType, value)        

    @property
    def line_draw_type(self) -> Union[ChartLineDrawType, str]:
        """Line Draw Type"""
        return self.__line_draw_type

    @line_draw_type.setter
    def line_draw_type(self, value: Union[ChartLineDrawType, str]):
        self._property_changed('line_draw_type')
        self.__line_draw_type = get_enum_value(ChartLineDrawType, value)        

    @property
    def line_transparency(self) -> float:
        """Stroke transparency"""
        return self.__line_transparency

    @line_transparency.setter
    def line_transparency(self, value: float):
        self._property_changed('line_transparency')
        self.__line_transparency = value        

    @property
    def line_width(self) -> float:
        """Stroke width"""
        return self.__line_width

    @line_width.setter
    def line_width(self, value: float):
        self._property_changed('line_width')
        self.__line_width = value        

    @property
    def x_label(self) -> str:
        return self.__x_label

    @x_label.setter
    def x_label(self, value: str):
        self._property_changed('x_label')
        self.__x_label = value        

    @property
    def y_label(self) -> str:
        return self.__y_label

    @y_label.setter
    def y_label(self, value: str):
        self._property_changed('y_label')
        self.__y_label = value        


class ChartRegression(Base):
        
    """An object which chart regression"""

    @camel_case_translate
    def __init__(
        self,
        type_: Union[ChartRegressionType, str] = None,
        line_data_index: int = None,
        is_visible: bool = None,
        stroke_color: str = None,
        stroke_type: Union[ChartRegressionStrokeType, str] = None,
        stroke_width: float = None,
        name: str = None
    ):        
        super().__init__()
        self.__type = get_enum_value(ChartRegressionType, type_)
        self.line_data_index = line_data_index
        self.is_visible = is_visible
        self.stroke_color = stroke_color
        self.stroke_type = stroke_type
        self.stroke_width = stroke_width
        self.name = name

    @property
    def type(self) -> Union[ChartRegressionType, str]:
        """Chart Regression Type"""
        return self.__type

    @type.setter
    def type(self, value: Union[ChartRegressionType, str]):
        self._property_changed('type')
        self.__type = get_enum_value(ChartRegressionType, value)        

    @property
    def line_data_index(self) -> int:
        """If Regression type is PlotData Type, line data index is required and it is the
           index of the data that return from the plot runner"""
        return self.__line_data_index

    @line_data_index.setter
    def line_data_index(self, value: int):
        self._property_changed('line_data_index')
        self.__line_data_index = value        

    @property
    def is_visible(self) -> bool:
        """Visible Flag"""
        return self.__is_visible

    @is_visible.setter
    def is_visible(self, value: bool):
        self._property_changed('is_visible')
        self.__is_visible = value        

    @property
    def stroke_color(self) -> str:
        return self.__stroke_color

    @stroke_color.setter
    def stroke_color(self, value: str):
        self._property_changed('stroke_color')
        self.__stroke_color = value        

    @property
    def stroke_type(self) -> Union[ChartRegressionStrokeType, str]:
        """Regression Stroke Type"""
        return self.__stroke_type

    @stroke_type.setter
    def stroke_type(self, value: Union[ChartRegressionStrokeType, str]):
        self._property_changed('stroke_type')
        self.__stroke_type = get_enum_value(ChartRegressionStrokeType, value)        

    @property
    def stroke_width(self) -> float:
        """Stroke Width"""
        return self.__stroke_width

    @stroke_width.setter
    def stroke_width(self, value: float):
        self._property_changed('stroke_width')
        self.__stroke_width = value        


class Chart(Base):
        
    """Object representation of a Chart"""

    @camel_case_translate
    def __init__(
        self,
        name: str,
        id_: str = None,
        owner_id: str = None,
        created_by_id: str = None,
        created_time: datetime.datetime = None,
        last_updated_by_id: str = None,
        last_updated_time: datetime.datetime = None,
        entitlements: Entitlements = None,
        entitlement_exclusions: EntitlementExclusions = None,
        folder_name: str = None,
        description: str = None,
        description_history: Tuple[str, ...] = None,
        expressions: Tuple[ChartExpression, ...] = None,
        chart_type: Union[ChartType, str] = None,
        chart_properties: Tuple[ChartProperties, ...] = None,
        regression_properties: Tuple[ChartRegression, ...] = None,
        real_time: bool = None,
        interval: str = None,
        relative_start_date: str = None,
        relative_end_date: str = None,
        start_date: datetime.date = None,
        end_date: datetime.date = None,
        start_time: datetime.datetime = None,
        end_time: datetime.datetime = None,
        tags: Tuple[str, ...] = None,
        auto_tags: Tuple[str, ...] = None,
        show_statistics: bool = None,
        copy_from_id: str = None,
        version: int = None,
        draft_view_id: str = None,
        label_settings: ChartLabelSettings = None,
        time_settings: ChartTime = None,
        x_axis_settings: XAxisSettings = None,
        display_settings: ChartDisplaySettings = None,
        y_axes_settings: Tuple[YAxisSettings, ...] = None,
        annotations: Tuple[ChartAnnotation, ...] = None
    ):        
        super().__init__()
        self.__id = id_
        self.owner_id = owner_id
        self.created_by_id = created_by_id
        self.created_time = created_time
        self.last_updated_by_id = last_updated_by_id
        self.last_updated_time = last_updated_time
        self.entitlements = entitlements
        self.entitlement_exclusions = entitlement_exclusions
        self.name = name
        self.folder_name = folder_name
        self.description = description
        self.description_history = description_history
        self.expressions = expressions
        self.chart_type = chart_type
        self.chart_properties = chart_properties
        self.regression_properties = regression_properties
        self.real_time = real_time
        self.interval = interval
        self.relative_start_date = relative_start_date
        self.relative_end_date = relative_end_date
        self.start_date = start_date
        self.end_date = end_date
        self.start_time = start_time
        self.end_time = end_time
        self.tags = tags
        self.auto_tags = auto_tags
        self.show_statistics = show_statistics
        self.copy_from_id = copy_from_id
        self.version = version
        self.draft_view_id = draft_view_id
        self.label_settings = label_settings
        self.time_settings = time_settings
        self.x_axis_settings = x_axis_settings
        self.display_settings = display_settings
        self.y_axes_settings = y_axes_settings
        self.annotations = annotations

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def owner_id(self) -> str:
        """Marquee unique identifier for user who owns the object."""
        return self.__owner_id

    @owner_id.setter
    def owner_id(self, value: str):
        self._property_changed('owner_id')
        self.__owner_id = value        

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
    def entitlements(self) -> Entitlements:
        """Defines the entitlements of a given resource."""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self._property_changed('entitlements')
        self.__entitlements = value        

    @property
    def entitlement_exclusions(self) -> EntitlementExclusions:
        """Defines the exclusion entitlements of a given resource."""
        return self.__entitlement_exclusions

    @entitlement_exclusions.setter
    def entitlement_exclusions(self, value: EntitlementExclusions):
        self._property_changed('entitlement_exclusions')
        self.__entitlement_exclusions = value        

    @property
    def name(self) -> str:
        """Display name of the chart"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def folder_name(self) -> str:
        """Folder name of the chart"""
        return self.__folder_name

    @folder_name.setter
    def folder_name(self, value: str):
        self._property_changed('folder_name')
        self.__folder_name = value        

    @property
    def description(self) -> str:
        """Chart description"""
        return self.__description

    @description.setter
    def description(self, value: str):
        self._property_changed('description')
        self.__description = value        

    @property
    def description_history(self) -> Tuple[str, ...]:
        """Recent description history."""
        return self.__description_history

    @description_history.setter
    def description_history(self, value: Tuple[str, ...]):
        self._property_changed('description_history')
        self.__description_history = value        

    @property
    def expressions(self) -> Tuple[ChartExpression, ...]:
        """Chart expressions"""
        return self.__expressions

    @expressions.setter
    def expressions(self, value: Tuple[ChartExpression, ...]):
        self._property_changed('expressions')
        self.__expressions = value        

    @property
    def chart_type(self) -> Union[ChartType, str]:
        return self.__chart_type

    @chart_type.setter
    def chart_type(self, value: Union[ChartType, str]):
        self._property_changed('chart_type')
        self.__chart_type = get_enum_value(ChartType, value)        

    @property
    def chart_properties(self) -> Tuple[ChartProperties, ...]:
        """Chart Properties"""
        return self.__chart_properties

    @chart_properties.setter
    def chart_properties(self, value: Tuple[ChartProperties, ...]):
        self._property_changed('chart_properties')
        self.__chart_properties = value        

    @property
    def regression_properties(self) -> Tuple[ChartRegression, ...]:
        """Chart Regression Properties"""
        return self.__regression_properties

    @regression_properties.setter
    def regression_properties(self, value: Tuple[ChartRegression, ...]):
        self._property_changed('regression_properties')
        self.__regression_properties = value        

    @property
    def real_time(self) -> bool:
        """Intraday or end-of-day chart"""
        return self.__real_time

    @real_time.setter
    def real_time(self, value: bool):
        self._property_changed('real_time')
        self.__real_time = value        

    @property
    def interval(self) -> str:
        """The interval value to be used e.g. Daily, 1M or 20Y"""
        return self.__interval

    @interval.setter
    def interval(self, value: str):
        self._property_changed('interval')
        self.__interval = value        

    @property
    def relative_start_date(self) -> str:
        return self.__relative_start_date

    @relative_start_date.setter
    def relative_start_date(self, value: str):
        self._property_changed('relative_start_date')
        self.__relative_start_date = value        

    @property
    def relative_end_date(self) -> str:
        return self.__relative_end_date

    @relative_end_date.setter
    def relative_end_date(self, value: str):
        self._property_changed('relative_end_date')
        self.__relative_end_date = value        

    @property
    def start_date(self) -> datetime.date:
        return self.__start_date

    @start_date.setter
    def start_date(self, value: datetime.date):
        self._property_changed('start_date')
        self.__start_date = value        

    @property
    def end_date(self) -> datetime.date:
        return self.__end_date

    @end_date.setter
    def end_date(self, value: datetime.date):
        self._property_changed('end_date')
        self.__end_date = value        

    @property
    def start_time(self) -> datetime.datetime:
        return self.__start_time

    @start_time.setter
    def start_time(self, value: datetime.datetime):
        self._property_changed('start_time')
        self.__start_time = value        

    @property
    def end_time(self) -> datetime.datetime:
        return self.__end_time

    @end_time.setter
    def end_time(self, value: datetime.datetime):
        self._property_changed('end_time')
        self.__end_time = value        

    @property
    def tags(self) -> Tuple[str, ...]:
        """Metadata associated with the object. Provide an array of strings which will be
           indexed for search and locating related objects"""
        return self.__tags

    @tags.setter
    def tags(self, value: Tuple[str, ...]):
        self._property_changed('tags')
        self.__tags = value        

    @property
    def auto_tags(self) -> Tuple[str, ...]:
        """Metadata associated with the object. Provide an array of strings which will be
           indexed for search and locating related objects"""
        return self.__auto_tags

    @auto_tags.setter
    def auto_tags(self, value: Tuple[str, ...]):
        self._property_changed('auto_tags')
        self.__auto_tags = value        

    @property
    def show_statistics(self) -> bool:
        """Flag to show the statistic in the chart area"""
        return self.__show_statistics

    @show_statistics.setter
    def show_statistics(self, value: bool):
        self._property_changed('show_statistics')
        self.__show_statistics = value        

    @property
    def copy_from_id(self) -> str:
        """Marquee unique identifier"""
        return self.__copy_from_id

    @copy_from_id.setter
    def copy_from_id(self, value: str):
        self._property_changed('copy_from_id')
        self.__copy_from_id = value        

    @property
    def version(self) -> int:
        """Chart Object Version"""
        return self.__version

    @version.setter
    def version(self, value: int):
        self._property_changed('version')
        self.__version = value        

    @property
    def draft_view_id(self) -> str:
        """Marquee unique identifier"""
        return self.__draft_view_id

    @draft_view_id.setter
    def draft_view_id(self, value: str):
        self._property_changed('draft_view_id')
        self.__draft_view_id = value        

    @property
    def label_settings(self) -> ChartLabelSettings:
        """Common label settings for a chart."""
        return self.__label_settings

    @label_settings.setter
    def label_settings(self, value: ChartLabelSettings):
        self._property_changed('label_settings')
        self.__label_settings = value        

    @property
    def time_settings(self) -> ChartTime:
        """Start / end time settings with timezone"""
        return self.__time_settings

    @time_settings.setter
    def time_settings(self, value: ChartTime):
        self._property_changed('time_settings')
        self.__time_settings = value        

    @property
    def x_axis_settings(self) -> XAxisSettings:
        """Settings for the X axis"""
        return self.__x_axis_settings

    @x_axis_settings.setter
    def x_axis_settings(self, value: XAxisSettings):
        self._property_changed('x_axis_settings')
        self.__x_axis_settings = value        

    @property
    def display_settings(self) -> ChartDisplaySettings:
        """Display settings associated with the chart"""
        return self.__display_settings

    @display_settings.setter
    def display_settings(self, value: ChartDisplaySettings):
        self._property_changed('display_settings')
        self.__display_settings = value        

    @property
    def y_axes_settings(self) -> Tuple[YAxisSettings, ...]:
        """Settings for the Y axes"""
        return self.__y_axes_settings

    @y_axes_settings.setter
    def y_axes_settings(self, value: Tuple[YAxisSettings, ...]):
        self._property_changed('y_axes_settings')
        self.__y_axes_settings = value        

    @property
    def annotations(self) -> Tuple[ChartAnnotation, ...]:
        """List of annotation objects for the chart."""
        return self.__annotations

    @annotations.setter
    def annotations(self, value: Tuple[ChartAnnotation, ...]):
        self._property_changed('annotations')
        self.__annotations = value        
