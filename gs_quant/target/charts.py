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


class ChartAnnotationRangeLabelType(EnumBase, Enum):    
    
    """Type of the range label."""

    withPct = 'withPct'
    withoutPct = 'withoutPct'    


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
    OHLC = 'OHLC'    


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

    bar = 'bar'
    line = 'line'
    scatter = 'scatter'    


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ChartDisplaySettings(Base):
    scatter_fill: Optional[bool] = field(default=None, metadata=field_metadata)
    bar_chart_type: Optional[str] = field(default=None, metadata=field_metadata)
    bar_padding: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ChartLabelSettings(Base):
    hide_last_value_labels: Optional[bool] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ChartProperties(Base):
    x: Optional[str] = field(default=None, metadata=field_metadata)
    x_label: Optional[str] = field(default=None, metadata=field_metadata)
    y: Optional[str] = field(default=None, metadata=field_metadata)
    y_label: Optional[str] = field(default=None, metadata=field_metadata)
    color: Optional[str] = field(default=None, metadata=field_metadata)
    shape: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ChartShare(Base):
    guids: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    version: Optional[int] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ChartTime(Base):
    start: Optional[str] = field(default=None, metadata=field_metadata)
    end: Optional[str] = field(default=None, metadata=field_metadata)
    timezone: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ParameterField(Base):
    field_: str = field(default=None, metadata=config(field_name='field', exclude=exclude_none))
    values: Tuple[str, ...] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class XAxisSettings(Base):
    auto_fit_range_to_data: Optional[bool] = field(default=None, metadata=field_metadata)
    label: Optional[str] = field(default=None, metadata=field_metadata)
    show_grid_lines: Optional[bool] = field(default=None, metadata=field_metadata)
    ignore_nil_date: Optional[bool] = field(default=None, metadata=field_metadata)
    x_axis_date_format: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class YAxisSettings(Base):
    decimal_precision: Optional[int] = field(default=None, metadata=field_metadata)
    id_: Optional[str] = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    label: Optional[str] = field(default=None, metadata=field_metadata)
    label_format: Optional[str] = field(default=None, metadata=field_metadata)
    max_: Optional[int] = field(default=None, metadata=config(field_name='max', exclude=exclude_none))
    min_: Optional[int] = field(default=None, metadata=config(field_name='min', exclude=exclude_none))
    show_grid_lines: Optional[bool] = field(default=None, metadata=field_metadata)
    hide: Optional[bool] = field(default=None, metadata=field_metadata)
    invert_axis: Optional[bool] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ChartAnnotation(Base):
    id_: str = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    type_: Optional[ChartAnnotationType] = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    chart_type: Optional[ChartType] = field(default=None, metadata=field_metadata)
    start_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    end_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    start_value: Optional[str] = field(default=None, metadata=field_metadata)
    end_value: Optional[str] = field(default=None, metadata=field_metadata)
    color: Optional[str] = field(default=None, metadata=field_metadata)
    is_proportional: Optional[bool] = field(default=False, metadata=field_metadata)
    fill_color: Optional[str] = field(default=None, metadata=field_metadata)
    font_size: Optional[float] = field(default=None, metadata=field_metadata)
    font_style: Optional[ChartAnnotationFontStyle] = field(default=None, metadata=field_metadata)
    font_weight: Optional[ChartAnnotationFontWeight] = field(default=None, metadata=field_metadata)
    label: Optional[str] = field(default=None, metadata=field_metadata)
    line_height: Optional[float] = field(default=None, metadata=field_metadata)
    line_type: Optional[ChartAnnotationLineType] = field(default=None, metadata=field_metadata)
    line_width: Optional[float] = field(default=None, metadata=field_metadata)
    radius: Optional[float] = field(default=None, metadata=field_metadata)
    range_label_type: Optional[ChartAnnotationRangeLabelType] = field(default=None, metadata=field_metadata)
    text_align: Optional[ChartAnnotationTextAlign] = field(default=None, metadata=field_metadata)
    text_decoration: Optional[ChartAnnotationTextDecoration] = field(default=None, metadata=field_metadata)
    text_width: Optional[float] = field(default=None, metadata=field_metadata)
    text_height: Optional[float] = field(default=None, metadata=field_metadata)
    y_axis_index: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


class ChartControls(DictBase):
    pass


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ChartExpression(Base):
    axis: Optional[str] = field(default=None, metadata=field_metadata)
    color: Optional[str] = field(default=None, metadata=field_metadata)
    delete_gap: Optional[bool] = field(default=None, metadata=field_metadata)
    delete_weekends: Optional[bool] = field(default=None, metadata=field_metadata)
    digits: Optional[float] = field(default=None, metadata=field_metadata)
    disable: Optional[bool] = field(default=None, metadata=field_metadata)
    fill: Optional[ChartFill] = field(default=None, metadata=field_metadata)
    has_x_grid: Optional[bool] = field(default=None, metadata=field_metadata)
    has_y_grid: Optional[bool] = field(default=None, metadata=field_metadata)
    show_statistics: Optional[bool] = field(default=None, metadata=field_metadata)
    hide: Optional[bool] = field(default=None, metadata=field_metadata)
    label: Optional[str] = field(default=None, metadata=field_metadata)
    line_type: Optional[ChartLineType] = field(default=None, metadata=field_metadata)
    line_draw_type: Optional[ChartLineDrawType] = field(default=None, metadata=field_metadata)
    line_transparency: Optional[float] = field(default=None, metadata=field_metadata)
    line_width: Optional[float] = field(default=None, metadata=field_metadata)
    x_label: Optional[str] = field(default=None, metadata=field_metadata)
    y_label: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ChartRegression(Base):
    type_: Optional[ChartRegressionType] = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    line_data_index: Optional[int] = field(default=None, metadata=field_metadata)
    is_visible: Optional[bool] = field(default=None, metadata=field_metadata)
    show_statistical_info: Optional[bool] = field(default=None, metadata=field_metadata)
    stroke_color: Optional[str] = field(default=None, metadata=field_metadata)
    stroke_type: Optional[ChartRegressionStrokeType] = field(default=None, metadata=field_metadata)
    stroke_width: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ConstructorParameter(Base):
    type_: str = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    values: Optional[Tuple[ParameterField, ...]] = field(default=None, metadata=field_metadata)
    options: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class TemplateVariable(Base):
    name: str = field(default=None, metadata=field_metadata)
    display_name: str = field(default=None, metadata=field_metadata)
    constructor_type: str = field(default=None, metadata=field_metadata)
    parameters: ConstructorParameter = field(default=None, metadata=field_metadata)
    default_value: Optional[Union[float, str]] = field(default=None, metadata=field_metadata)
    hide: Optional[bool] = field(default=False, metadata=field_metadata)
    tooltip: Optional[str] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Chart(Base):
    name: str = field(default=None, metadata=field_metadata)
    id_: Optional[str] = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    owner_id: Optional[str] = field(default=None, metadata=field_metadata)
    created_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    created_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    last_updated_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    last_updated_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    entitlements: Optional[Entitlements] = field(default=None, metadata=field_metadata)
    entitlement_exclusions: Optional[EntitlementExclusions] = field(default=None, metadata=field_metadata)
    title: Optional[str] = field(default=None, metadata=field_metadata)
    subtitle: Optional[str] = field(default=None, metadata=field_metadata)
    rank: Optional[int] = field(default=None, metadata=field_metadata)
    folder_name: Optional[str] = field(default=None, metadata=field_metadata)
    description: Optional[str] = field(default=None, metadata=field_metadata)
    description_history: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    expressions: Optional[Tuple[ChartExpression, ...]] = field(default=None, metadata=field_metadata)
    chart_type: Optional[ChartType] = field(default=None, metadata=field_metadata)
    chart_properties: Optional[Tuple[ChartProperties, ...]] = field(default=None, metadata=field_metadata)
    regression_properties: Optional[Tuple[ChartRegression, ...]] = field(default=None, metadata=field_metadata)
    real_time: Optional[bool] = field(default=None, metadata=field_metadata)
    show_controls_toolbar: Optional[bool] = field(default=None, metadata=field_metadata)
    interval: Optional[str] = field(default=None, metadata=field_metadata)
    relative_start_date: Optional[str] = field(default=None, metadata=field_metadata)
    relative_end_date: Optional[str] = field(default=None, metadata=field_metadata)
    start_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    end_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    start_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    end_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    tags: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    auto_tags: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    show_statistics: Optional[bool] = field(default=None, metadata=field_metadata)
    copy_from_id: Optional[str] = field(default=None, metadata=field_metadata)
    version: Optional[int] = field(default=None, metadata=field_metadata)
    draft_view_id: Optional[str] = field(default=None, metadata=field_metadata)
    label_settings: Optional[ChartLabelSettings] = field(default=None, metadata=field_metadata)
    time_settings: Optional[ChartTime] = field(default=None, metadata=field_metadata)
    x_axis_settings: Optional[XAxisSettings] = field(default=None, metadata=field_metadata)
    display_settings: Optional[ChartDisplaySettings] = field(default=None, metadata=field_metadata)
    y_axes_settings: Optional[Tuple[YAxisSettings, ...]] = field(default=None, metadata=field_metadata)
    annotations: Optional[Tuple[ChartAnnotation, ...]] = field(default=None, metadata=field_metadata)
    template_variables: Optional[DictBase] = field(default=None, metadata=field_metadata)
    parameters: Optional[ChartControls] = field(default=None, metadata=field_metadata)
    controls: Optional[Tuple[DictBase, ...]] = field(default=None, metadata=field_metadata)
