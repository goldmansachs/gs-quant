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


class AvailableUnitTypes(EnumBase, Enum):    
    
    """Enum listing supported unit types"""

    percentage = 'percentage'
    percentageWithSymbol = 'percentageWithSymbol'
    bps = 'bps'
    bp = 'bp'
    x = 'x'    


class EntitiesSupported(EnumBase, Enum):    
    
    """Enum listing supported entities"""

    assets = 'assets'
    tds = 'tds'    


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
    treemap = 'treemap'
    triColor = 'triColor'    


class RateIds(EnumBase, Enum):    
    
    """Enum listing supported rate ids"""

    USD = 'USD'
    EUR = 'EUR'
    JPY = 'JPY'
    GBP = 'GBP'
    CAD = 'CAD'
    AUD = 'AUD'    


class SortDirection(EnumBase, Enum):    
    
    """Enum with available sort directions"""

    asc = 'asc'
    desc = 'desc'
    default = 'default'    


class SortType(EnumBase, Enum):    
    
    """Enum listing supported sort types"""

    value = 'value'
    abs = 'abs'    


class WipiFilterOperation(EnumBase, Enum):    
    
    """Enum listing supported operations for wipi filters."""

    eq = 'eq'
    ne = 'ne'
    gt = 'gt'
    lt = 'lt'
    gte = 'gte'
    lte = 'lte'
    last = 'last'    


class WipiFilterType(EnumBase, Enum):    
    
    """Enum listing supported wipi filter types."""

    AND = 'AND'
    OR = 'OR'    


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ColumnProperty(Base):
    column_name: Optional[str] = None
    property_: Optional[str] = field(default=None, metadata=config(field_name='property'))


class FieldMap(DictBase):
    pass


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Historical(Base):
    value: Optional[Union[float, str]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MonitorResponseData(Base):
    id_: str = field(default=None, metadata=config(field_name='id'))
    result: DictBase = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Movers(Base):
    column_name: str = None
    top: Optional[float] = None
    bottom: Optional[float] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ColumnFormat(Base):
    precision: float = None
    unit: Optional[AvailableUnitTypes] = None
    human_readable: Optional[bool] = None
    multiplier: Optional[float] = None
    axis_key: Optional[str] = None
    show_tooltip: Optional[bool] = None
    low_color: Optional[str] = None
    high_color: Optional[str] = None
    mid_color: Optional[str] = None
    low_value: Optional[float] = None
    high_value: Optional[float] = None
    mid_value: Optional[float] = None
    hide_value: Optional[bool] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ColumnMappings(Base):
    column_name: Optional[str] = None
    parameters: Optional[FieldMap] = None
    color: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ColumnOperation(Base):
    column_names: Optional[Tuple[str, ...]] = None
    function_name: Optional[str] = None
    type_: Optional[str] = field(default=None, metadata=config(field_name='type'))
    parameters: Optional[FieldMap] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ExportParameters(Base):
    tokens: Tuple[str, ...] = None
    data_set_id: Optional[str] = None
    fields: Optional[Tuple[str, ...]] = None
    label: Optional[str] = None
    start_date: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Function(Base):
    measure: str = None
    frequency: str = None
    name: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    fields: Optional[Tuple[str, ...]] = None
    parameters: Optional[FieldMap] = None
    where: Optional[FieldMap] = None
    vendor: Optional[str] = None
    data_set_id: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RateRow(Base):
    period: ParameterPeriod = None
    last: float = None
    change: float = None
    std: float = None
    slope: float = None
    historical: Optional[Historical] = None
    percentage_change: Optional[float] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Sort(Base):
    column_name: str = None
    type_: Optional[SortType] = field(default=None, metadata=config(field_name='type'))
    direction: Optional[SortDirection] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class WipiRequestFilter(Base):
    column: str = None
    operation: WipiFilterOperation = None
    value: Union[float, str] = None
    type_: Optional[WipiFilterType] = field(default=None, metadata=config(field_name='type'))


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ColumnDefinition(Base):
    render: ParameterRender = None
    name: str = None
    enable_cell_flashing: Optional[bool] = None
    entity_property: Optional[str] = None
    function: Optional[Function] = None
    format_: Optional[ColumnFormat] = field(default=None, metadata=config(field_name='format'))
    width: Optional[float] = None
    column_property: Optional[ColumnProperty] = None
    column_operation: Optional[ColumnOperation] = None
    expression: Optional[str] = None
    expressions: Optional[Tuple[str, ...]] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    tooltip: Optional[str] = None
    parent_column_name: Optional[str] = None
    primary: Optional[bool] = None
    pivots: Optional[Tuple[str, ...]] = None
    disable_cell_tooltips: Optional[bool] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class EntityId(Base):
    id_: Optional[str] = field(default=None, metadata=config(field_name='id'))
    column_mappings: Optional[Tuple[ColumnMappings, ...]] = None
    color: Optional[str] = None
    route_url: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RatesResponseData(Base):
    name: RateIds = None
    id_: str = field(default=None, metadata=config(field_name='id'))
    rows: Tuple[RateRow, ...] = None
    libor_id: Optional[str] = field(default=None, metadata=config(field_name='libor_id'))


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RowGroup(Base):
    name: str = None
    entity_ids: Tuple[EntityId, ...] = None
    movers: Optional[Movers] = None
    sort: Optional[Sort] = None
    export: Optional[ExportParameters] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MonitorParameters(Base):
    column_definitions: Tuple[ColumnDefinition, ...] = None
    row_groups: Tuple[RowGroup, ...] = None
    export: Optional[ExportParameters] = None
    ignore_business_day_logic: Optional[bool] = None
    horizontal_scroll: Optional[bool] = None
    mid_value_average: Optional[bool] = None
    aggregate_queries: Optional[bool] = None
    row_heatmap: Optional[bool] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Monitor(Base):
    name: str = None
    type_: EntitiesSupported = field(default=None, metadata=config(field_name='type'))
    id_: Optional[str] = field(default=None, metadata=config(field_name='id'))
    parameters: Optional[MonitorParameters] = None
    created_time: Optional[datetime.datetime] = None
    last_updated_time: Optional[datetime.datetime] = None
    created_by_id: Optional[str] = None
    last_updated_by_id: Optional[str] = None
    owner_id: Optional[str] = None
    entitlements: Optional[Entitlements] = None
    folder_name: Optional[str] = None
    polling_time: Optional[float] = None
    tags: Optional[Tuple[str, ...]] = None
