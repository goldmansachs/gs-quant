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

from gs_quant.base import *
from gs_quant.common import *
import datetime
from typing import Dict, Optional, Tuple, Union
from dataclasses import dataclass, field
from dataclasses_json import LetterCase, config, dataclass_json
from enum import Enum


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


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ChartDisplaySettings(Base):
    scatter_fill: Optional[bool] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ChartLabelSettings(Base):
    hide_last_value_labels: Optional[bool] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ChartProperties(Base):
    x: Optional[str] = None
    x_label: Optional[str] = None
    y: Optional[str] = None
    y_label: Optional[str] = None
    color: Optional[str] = None
    shape: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ChartShare(Base):
    guids: Optional[Tuple[str, ...]] = None
    version: Optional[int] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ChartTime(Base):
    start: Optional[str] = None
    end: Optional[str] = None
    timezone: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class XAxisSettings(Base):
    auto_fit_range_to_data: Optional[bool] = None
    show_grid_lines: Optional[bool] = None
    x_axis_date_format: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class YAxisSettings(Base):
    decimal_precision: Optional[int] = None
    id_: Optional[str] = field(default=None, metadata=config(field_name='id'))
    label: Optional[str] = None
    label_format: Optional[str] = None
    max_: Optional[int] = field(default=None, metadata=config(field_name='max'))
    min_: Optional[int] = field(default=None, metadata=config(field_name='min'))
    show_grid_lines: Optional[bool] = None
    hide: Optional[bool] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ChartAnnotation(Base):
    id_: str = field(default=None, metadata=config(field_name='id'))
    type_: Optional[ChartAnnotationType] = field(default=None, metadata=config(field_name='type'))
    chart_type: Optional[ChartType] = None
    start_time: Optional[datetime.datetime] = None
    end_time: Optional[datetime.datetime] = None
    start_value: Optional[str] = None
    end_value: Optional[str] = None
    color: Optional[str] = None
    is_proportional: Optional[bool] = False
    fill_color: Optional[str] = None
    font_size: Optional[float] = None
    font_style: Optional[ChartAnnotationFontStyle] = None
    font_weight: Optional[ChartAnnotationFontWeight] = None
    label: Optional[str] = None
    line_height: Optional[float] = None
    line_type: Optional[ChartAnnotationLineType] = None
    line_width: Optional[float] = None
    radius: Optional[float] = None
    text_align: Optional[ChartAnnotationTextAlign] = None
    text_decoration: Optional[ChartAnnotationTextDecoration] = None
    text_width: Optional[float] = None
    text_height: Optional[float] = None
    y_axis_index: Optional[float] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ChartExpression(Base):
    axis: Optional[str] = None
    color: Optional[str] = None
    delete_gap: Optional[bool] = None
    delete_weekends: Optional[bool] = None
    digits: Optional[float] = None
    disable: Optional[bool] = None
    fill: Optional[ChartFill] = None
    has_x_grid: Optional[bool] = None
    has_y_grid: Optional[bool] = None
    show_statistics: Optional[bool] = None
    hide: Optional[bool] = None
    label: Optional[str] = None
    line_type: Optional[ChartLineType] = None
    line_draw_type: Optional[ChartLineDrawType] = None
    line_transparency: Optional[float] = None
    line_width: Optional[float] = None
    x_label: Optional[str] = None
    y_label: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ChartRegression(Base):
    type_: Optional[ChartRegressionType] = field(default=None, metadata=config(field_name='type'))
    line_data_index: Optional[int] = None
    is_visible: Optional[bool] = None
    stroke_color: Optional[str] = None
    stroke_type: Optional[ChartRegressionStrokeType] = None
    stroke_width: Optional[float] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Chart(Base):
    name: str = None
    id_: Optional[str] = field(default=None, metadata=config(field_name='id'))
    owner_id: Optional[str] = None
    created_by_id: Optional[str] = None
    created_time: Optional[datetime.datetime] = None
    last_updated_by_id: Optional[str] = None
    last_updated_time: Optional[datetime.datetime] = None
    entitlements: Optional[Entitlements] = None
    entitlement_exclusions: Optional[EntitlementExclusions] = None
    folder_name: Optional[str] = None
    description: Optional[str] = None
    description_history: Optional[Tuple[str, ...]] = None
    expressions: Optional[Tuple[ChartExpression, ...]] = None
    chart_type: Optional[ChartType] = None
    chart_properties: Optional[Tuple[ChartProperties, ...]] = None
    regression_properties: Optional[Tuple[ChartRegression, ...]] = None
    real_time: Optional[bool] = None
    interval: Optional[str] = None
    relative_start_date: Optional[str] = None
    relative_end_date: Optional[str] = None
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None
    start_time: Optional[datetime.datetime] = None
    end_time: Optional[datetime.datetime] = None
    tags: Optional[Tuple[str, ...]] = None
    auto_tags: Optional[Tuple[str, ...]] = None
    show_statistics: Optional[bool] = None
    copy_from_id: Optional[str] = None
    version: Optional[int] = None
    draft_view_id: Optional[str] = None
    label_settings: Optional[ChartLabelSettings] = None
    time_settings: Optional[ChartTime] = None
    x_axis_settings: Optional[XAxisSettings] = None
    display_settings: Optional[ChartDisplaySettings] = None
    y_axes_settings: Optional[Tuple[YAxisSettings, ...]] = None
    annotations: Optional[Tuple[ChartAnnotation, ...]] = None
