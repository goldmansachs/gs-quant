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


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ColumnProperty(Base):
    column_name: Optional[str] = field(default=None, metadata=field_metadata)
    property_: Optional[str] = field(default=None, metadata=config(field_name='property', exclude=exclude_none))
    name: Optional[str] = field(default=None, metadata=name_metadata)


class FieldMap(DictBase):
    pass


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Historical(Base):
    value: Optional[Union[float, str]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MonitorResponseData(Base):
    id_: str = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    result: DictBase = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Movers(Base):
    column_name: str = field(default=None, metadata=field_metadata)
    top: Optional[float] = field(default=None, metadata=field_metadata)
    bottom: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ColumnFormat(Base):
    precision: float = field(default=None, metadata=field_metadata)
    unit: Optional[AvailableUnitTypes] = field(default=None, metadata=field_metadata)
    human_readable: Optional[bool] = field(default=None, metadata=field_metadata)
    multiplier: Optional[float] = field(default=None, metadata=field_metadata)
    axis_key: Optional[str] = field(default=None, metadata=field_metadata)
    show_tooltip: Optional[bool] = field(default=None, metadata=field_metadata)
    low_color: Optional[str] = field(default=None, metadata=field_metadata)
    high_color: Optional[str] = field(default=None, metadata=field_metadata)
    mid_color: Optional[str] = field(default=None, metadata=field_metadata)
    low_value: Optional[float] = field(default=None, metadata=field_metadata)
    high_value: Optional[float] = field(default=None, metadata=field_metadata)
    mid_value: Optional[float] = field(default=None, metadata=field_metadata)
    hide_value: Optional[bool] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ColumnMappings(Base):
    column_name: Optional[str] = field(default=None, metadata=field_metadata)
    parameters: Optional[FieldMap] = field(default=None, metadata=field_metadata)
    color: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ColumnOperation(Base):
    column_names: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    function_name: Optional[str] = field(default=None, metadata=field_metadata)
    type_: Optional[str] = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    parameters: Optional[FieldMap] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ExportParameters(Base):
    tokens: Tuple[str, ...] = field(default=None, metadata=field_metadata)
    data_set_id: Optional[str] = field(default=None, metadata=field_metadata)
    fields: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    label: Optional[str] = field(default=None, metadata=field_metadata)
    start_date: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Function(Base):
    measure: str = field(default=None, metadata=field_metadata)
    frequency: str = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=field_metadata)
    start_date: Optional[str] = field(default=None, metadata=field_metadata)
    end_date: Optional[str] = field(default=None, metadata=field_metadata)
    start_time: Optional[str] = field(default=None, metadata=field_metadata)
    end_time: Optional[str] = field(default=None, metadata=field_metadata)
    should_use_search_until: Optional[bool] = field(default=None, metadata=field_metadata)
    fields: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    parameters: Optional[FieldMap] = field(default=None, metadata=field_metadata)
    where: Optional[FieldMap] = field(default=None, metadata=field_metadata)
    vendor: Optional[str] = field(default=None, metadata=field_metadata)
    data_set_id: Optional[str] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RateRow(Base):
    period: ParameterPeriod = field(default=None, metadata=field_metadata)
    last: float = field(default=None, metadata=field_metadata)
    change: float = field(default=None, metadata=field_metadata)
    std: float = field(default=None, metadata=field_metadata)
    slope: float = field(default=None, metadata=field_metadata)
    historical: Optional[Historical] = field(default=None, metadata=field_metadata)
    percentage_change: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Sort(Base):
    column_name: str = field(default=None, metadata=field_metadata)
    type_: Optional[SortType] = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    direction: Optional[SortDirection] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class WipiRequestFilter(Base):
    column: str = field(default=None, metadata=field_metadata)
    operation: WipiFilterOperation = field(default=None, metadata=field_metadata)
    value: Union[float, str] = field(default=None, metadata=field_metadata)
    type_: Optional[WipiFilterType] = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ColumnDefinition(Base):
    render: ParameterRender = field(default=None, metadata=field_metadata)
    name: str = field(default=None, metadata=field_metadata)
    enable_cell_flashing: Optional[bool] = field(default=None, metadata=field_metadata)
    entity_property: Optional[str] = field(default=None, metadata=field_metadata)
    function: Optional[Function] = field(default=None, metadata=field_metadata)
    format_: Optional[ColumnFormat] = field(default=None, metadata=config(field_name='format', exclude=exclude_none))
    width: Optional[float] = field(default=None, metadata=field_metadata)
    column_property: Optional[ColumnProperty] = field(default=None, metadata=field_metadata)
    column_operation: Optional[ColumnOperation] = field(default=None, metadata=field_metadata)
    expression: Optional[str] = field(default=None, metadata=field_metadata)
    expressions: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    start_date: Optional[str] = field(default=None, metadata=field_metadata)
    end_date: Optional[str] = field(default=None, metadata=field_metadata)
    tooltip: Optional[str] = field(default=None, metadata=field_metadata)
    parent_column_name: Optional[str] = field(default=None, metadata=field_metadata)
    primary: Optional[bool] = field(default=None, metadata=field_metadata)
    pivots: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    disable_cell_tooltips: Optional[bool] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class EntityId(Base):
    id_: Optional[str] = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    column_mappings: Optional[Tuple[ColumnMappings, ...]] = field(default=None, metadata=field_metadata)
    color: Optional[str] = field(default=None, metadata=field_metadata)
    route_url: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RatesResponseData(Base):
    name: RateIds = field(default=None, metadata=field_metadata)
    id_: str = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    rows: Tuple[RateRow, ...] = field(default=None, metadata=field_metadata)
    libor_id: Optional[str] = field(default=None, metadata=config(field_name='libor_id', exclude=exclude_none))


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RowGroup(Base):
    name: str = field(default=None, metadata=field_metadata)
    entity_ids: Tuple[EntityId, ...] = field(default=None, metadata=field_metadata)
    movers: Optional[Movers] = field(default=None, metadata=field_metadata)
    sort: Optional[Sort] = field(default=None, metadata=field_metadata)
    export: Optional[ExportParameters] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MonitorParameters(Base):
    column_definitions: Tuple[ColumnDefinition, ...] = field(default=None, metadata=field_metadata)
    row_groups: Tuple[RowGroup, ...] = field(default=None, metadata=field_metadata)
    export: Optional[ExportParameters] = field(default=None, metadata=field_metadata)
    ignore_business_day_logic: Optional[bool] = field(default=None, metadata=field_metadata)
    horizontal_scroll: Optional[bool] = field(default=None, metadata=field_metadata)
    mid_value_average: Optional[bool] = field(default=None, metadata=field_metadata)
    aggregate_queries: Optional[bool] = field(default=None, metadata=field_metadata)
    row_heatmap: Optional[bool] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Monitor(Base):
    name: str = field(default=None, metadata=field_metadata)
    type_: EntitiesSupported = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    id_: Optional[str] = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    parameters: Optional[MonitorParameters] = field(default=None, metadata=field_metadata)
    created_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    last_updated_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    created_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    last_updated_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    owner_id: Optional[str] = field(default=None, metadata=field_metadata)
    entitlements: Optional[Entitlements] = field(default=None, metadata=field_metadata)
    folder_name: Optional[str] = field(default=None, metadata=field_metadata)
    polling_time: Optional[float] = field(default=None, metadata=field_metadata)
    tags: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
