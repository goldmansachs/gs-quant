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


class DataSetType(EnumBase, Enum):    
    
    """Type of the dataset"""

    PlotTool_Pro = 'PlotTool Pro'
    Alloy = 'Alloy'
    Snowflake = 'Snowflake'    


class DelayExclusionType(EnumBase, Enum):    
    
    """Type of the delay exclusion"""

    LAST_DAY_OF_THE_MONTH = 'LAST_DAY_OF_THE_MONTH'    


class DevelopmentStatus(EnumBase, Enum):    
    
    """The status of development of this dataset. Controls rate limit on query/upload."""

    Development = 'Development'
    Production = 'Production'    


class FieldFormat(EnumBase, Enum):    
    
    """Format to apply on field validation. Currently supports a subset of built-in
       formats (from JSON schema specification)."""

    date = 'date'
    date_time = 'date-time'    


class MarketDataMeasure(EnumBase, Enum):    
    
    Last = 'Last'
    Curve = 'Curve'
    Close_Change = 'Close Change'
    Previous_Close = 'Previous Close'    


class MeasureEntityType(EnumBase, Enum):    
    
    """Entity type associated with a measure."""

    ASSET = 'ASSET'
    BACKTEST = 'BACKTEST'
    KPI = 'KPI'
    COUNTRY = 'COUNTRY'
    SUBDIVISION = 'SUBDIVISION'
    REPORT = 'REPORT'
    HEDGE = 'HEDGE'
    PORTFOLIO = 'PORTFOLIO'
    RISK_MODEL = 'RISK_MODEL'    


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class AdvancedFilter(Base):
    column: str = field(default=None, metadata=field_metadata)
    operator: str = field(default=None, metadata=field_metadata)
    value: Optional[float] = field(default=None, metadata=field_metadata)
    values: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    format_: Optional[str] = field(default=None, metadata=config(field_name='format', exclude=exclude_none))
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class AlloyService(Base):
    base_url: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ColumnEnumPair(Base):
    column: Optional[str] = field(default=None, metadata=field_metadata)
    enum_key: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataSetCondition(Base):
    column: str = field(default=None, metadata=field_metadata)
    operator: str = field(default=None, metadata=field_metadata)
    value: Optional[float] = field(default=None, metadata=field_metadata)
    values: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataSetDefaults(Base):
    start_seconds: Optional[float] = field(default=None, metadata=field_metadata)
    end_seconds: Optional[float] = field(default=None, metadata=field_metadata)
    delay_seconds: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataSetFieldEntityAttributes(Base):
    in_code: Optional[bool] = field(default=None, metadata=field_metadata)
    is_entity: Optional[bool] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataSetFieldEntityClassifications(Base):
    groups: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    data_set_id: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataSetFieldEntityNumberParameters(Base):
    maximum: Optional[int] = field(default=None, metadata=field_metadata)
    minimum: Optional[int] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class EntityMetadata(Base):
    created_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    created_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    last_updated_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    last_updated_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ErrorInfo(Base):
    status_code: int = field(default=None, metadata=field_metadata)
    reason_phrase: str = field(default=None, metadata=field_metadata)
    title: Optional[str] = field(default=None, metadata=field_metadata)
    messages: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FieldLinkSelector(Base):
    field_selector: Optional[str] = field(default=None, metadata=field_metadata)
    description: Optional[str] = field(default=None, metadata=field_metadata)
    display_name: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MDAPI(Base):
    type_: str = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    quoting_styles: Tuple[DictBase, ...] = field(default=None, metadata=field_metadata)
    class_: Optional[str] = field(default=None, metadata=config(field_name='class', exclude=exclude_none))
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MarketDataField(Base):
    name: Optional[str] = field(default=None, metadata=field_metadata)
    mapping: Optional[str] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MarketDataFilteredField(Base):
    field_: Optional[str] = field(default=None, metadata=config(field_name='field', exclude=exclude_none))
    default_value: Optional[str] = field(default=None, metadata=field_metadata)
    default_numerical_value: Optional[float] = field(default=None, metadata=field_metadata)
    default_boolean_value: Optional[bool] = field(default=None, metadata=field_metadata)
    numerical_values: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    values: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    multi_measure: Optional[bool] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@dataclass
class MeasureBacktest(Base):
    pass


@dataclass
class MeasureKpi(Base):
    pass


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MidPrice(Base):
    bid_column: Optional[str] = field(default=None, metadata=field_metadata)
    ask_column: Optional[str] = field(default=None, metadata=field_metadata)
    mid_column: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ParserEntity(Base):
    only_normalized_fields: Optional[bool] = field(default=None, metadata=field_metadata)
    quotes: Optional[bool] = field(default=None, metadata=field_metadata)
    trades: Optional[bool] = field(default=None, metadata=field_metadata)
    only_mqtick_fields: Optional[bool] = field(default=None, metadata=field_metadata)
    include_trd_flg_proc: Optional[bool] = field(default=None, metadata=field_metadata)
    keep_raw_fields: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    include_mmt: Optional[bool] = field(default=None, metadata=field_metadata)
    include_currency: Optional[bool] = field(default=None, metadata=field_metadata)
    separate_quote_exchange_codes: Optional[bool] = field(default=None, metadata=field_metadata)
    trade_ids: Optional[bool] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class QueryProcessor(Base):
    processor_name: Optional[str] = field(default=None, metadata=field_metadata)
    manual_processor_name: Optional[str] = field(default=None, metadata=field_metadata)
    params: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RemapFieldPair(Base):
    field_: Optional[str] = field(default=None, metadata=config(field_name='field', exclude=exclude_none))
    remap_to: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ResponseInfo(Base):
    request_id: Optional[str] = field(default=None, metadata=field_metadata)
    messages: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class StoredEntity(Base):
    stored_processor_name: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SymbolFilterLink(Base):
    entity_field: Optional[str] = field(default=None, metadata=field_metadata)
    entity_type: Optional[str] = field(init=False, default='MktCoordinate', metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class AlloyConfig(Base):
    data_service: Optional[AlloyService] = field(default=None, metadata=field_metadata)
    coverage_service: Optional[AlloyService] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataFilter(Base):
    field_: str = field(default=None, metadata=config(field_name='field', exclude=exclude_none))
    values: Tuple[str, ...] = field(default=None, metadata=field_metadata)
    column: Optional[str] = field(default=None, metadata=field_metadata)
    where: Optional[DataSetCondition] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataSetCoverageProperties(Base):
    prefixes: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    prefix_type: Optional[str] = field(default=None, metadata=field_metadata)
    asset_classes: Optional[Tuple[AssetClass, ...]] = field(default=None, metadata=field_metadata)
    asset_types: Optional[Tuple[AssetType, ...]] = field(default=None, metadata=field_metadata)
    entity_types: Optional[Tuple[MeasureEntityType, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataSetDelay(Base):
    until_seconds: float = field(default=None, metadata=field_metadata)
    at_time_zone: str = field(default=None, metadata=field_metadata)
    when: Optional[Tuple[DelayExclusionType, ...]] = field(default=None, metadata=field_metadata)
    history_up_to_seconds: Optional[float] = field(default=None, metadata=field_metadata)
    history_up_to_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    history_up_to_months: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataSetFieldEntityStringParameters(Base):
    enum: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    format_: Optional[FieldFormat] = field(default=None, metadata=config(field_name='format', exclude=exclude_none))
    pattern: Optional[str] = field(default=r'^[\w ]{1,256}$', metadata=field_metadata)
    max_length: Optional[int] = field(default=None, metadata=field_metadata)
    min_length: Optional[int] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataSetTransforms(Base):
    redact_columns: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    round_columns: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    remap_fields: Optional[Tuple[RemapFieldPair, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


class FieldFilterMapDataQuery(DictBase):
    pass


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FieldLink(Base):
    entity_identifier: Optional[str] = field(default=None, metadata=field_metadata)
    prefix: Optional[str] = field(default=None, metadata=field_metadata)
    additional_entity_fields: Optional[Tuple[FieldLinkSelector, ...]] = field(default=None, metadata=field_metadata)
    entity_type: Optional[str] = field(init=False, default='Asset', metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MarketDataMapping(Base):
    asset_class: Optional[AssetClass] = field(default=None, metadata=field_metadata)
    query_type: Optional[str] = field(default=None, metadata=field_metadata)
    description: Optional[str] = field(default=None, metadata=field_metadata)
    scale: Optional[float] = field(default=None, metadata=field_metadata)
    frequency: Optional[MarketDataFrequency] = field(default=None, metadata=field_metadata)
    measures: Optional[Tuple[MarketDataMeasure, ...]] = field(default=None, metadata=field_metadata)
    data_set: Optional[str] = field(default=None, metadata=field_metadata)
    vendor: Optional[MarketDataVendor] = field(default=None, metadata=field_metadata)
    fields: Optional[Tuple[MarketDataField, ...]] = field(default=None, metadata=field_metadata)
    rank: Optional[float] = field(default=None, metadata=field_metadata)
    filtered_fields: Optional[Tuple[MarketDataFilteredField, ...]] = field(default=None, metadata=field_metadata)
    asset_types: Optional[Tuple[AssetType, ...]] = field(default=None, metadata=field_metadata)
    entity_type: Optional[MeasureEntityType] = field(default=None, metadata=field_metadata)
    backtest_entity: Optional[MeasureBacktest] = field(default=None, metadata=field_metadata)
    kpi_entity: Optional[MeasureKpi] = field(default=None, metadata=field_metadata)
    multi_measure: Optional[bool] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ProcessorEntity(Base):
    filters: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    parsers: Optional[Tuple[ParserEntity, ...]] = field(default=None, metadata=field_metadata)
    deduplicate: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    enum_type: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    enums: Optional[Tuple[ColumnEnumPair, ...]] = field(default=None, metadata=field_metadata)
    fill_fwd: Optional[str] = field(default=None, metadata=field_metadata)
    stored: Optional[Tuple[StoredEntity, ...]] = field(default=None, metadata=field_metadata)
    additional_processors: Optional[Tuple[QueryProcessor, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SymbolFilterDimension(Base):
    field_: Optional[str] = field(default=None, metadata=config(field_name='field', exclude=exclude_none))
    field_description: Optional[str] = field(default=None, metadata=field_metadata)
    symbol_filter_link: Optional[SymbolFilterLink] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ComplexFilter(Base):
    operator: str = field(default=None, metadata=field_metadata)
    simple_filters: Tuple[DataFilter, ...] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataGroup(Base):
    context: Optional[FieldValueMap] = field(default=None, metadata=field_metadata)
    data: Optional[Tuple[FieldValueMap, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataQuery(Base):
    id_: Optional[str] = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    data_set_id: Optional[str] = field(default=None, metadata=field_metadata)
    format_: Optional[Format] = field(default=None, metadata=config(field_name='format', exclude=exclude_none))
    where: Optional[FieldFilterMapDataQuery] = field(default=None, metadata=field_metadata)
    vendor: Optional[MarketDataVendor] = field(default=None, metadata=field_metadata)
    start_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    end_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    start_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    page: Optional[int] = field(default=None, metadata=field_metadata)
    page_size: Optional[int] = field(default=None, metadata=field_metadata)
    end_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    relative_start_date: Optional[str] = field(default=None, metadata=field_metadata)
    relative_end_date: Optional[str] = field(default=None, metadata=field_metadata)
    adjust_as_of: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    as_of_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    id_as_of_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    use_temporal_x_ref: Optional[bool] = field(default=False, metadata=field_metadata)
    restrict_secondary_identifier: Optional[bool] = field(default=False, metadata=field_metadata)
    since: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    dates: Optional[Tuple[datetime.date, ...]] = field(default=None, metadata=field_metadata)
    times: Optional[Tuple[datetime.datetime, ...]] = field(default=None, metadata=field_metadata)
    delay: Optional[int] = field(default=None, metadata=field_metadata)
    intervals: Optional[int] = field(default=None, metadata=field_metadata)
    samples: Optional[int] = field(default=None, metadata=field_metadata)
    limit: Optional[int] = field(default=None, metadata=field_metadata)
    polling_interval: Optional[int] = field(default=None, metadata=field_metadata)
    group_by: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    grouped: Optional[bool] = field(default=None, metadata=field_metadata)
    fields: Optional[Tuple[Union[DictBase, str], ...]] = field(default=None, metadata=field_metadata)
    restrict_fields: Optional[bool] = field(default=False, metadata=field_metadata)
    entity_filter: Optional[FieldFilterMapDataQuery] = field(default=None, metadata=field_metadata)
    interval: Optional[str] = field(default=None, metadata=field_metadata)
    distinct_consecutive: Optional[bool] = field(default=False, metadata=field_metadata)
    time_filter: Optional[TimeFilter] = field(default=None, metadata=field_metadata)
    use_field_alias: Optional[bool] = field(default=False, metadata=field_metadata)
    remap_schema_to_alias: Optional[bool] = field(default=False, metadata=field_metadata)
    show_linked_dimensions: Optional[bool] = field(default=True, metadata=field_metadata)
    use_project_processor: Optional[bool] = field(default=False, metadata=field_metadata)
    snapshot: Optional[bool] = field(default=False, metadata=field_metadata)
    search_until: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    markout: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    offset_to_exchange_open: Optional[str] = field(default=None, metadata=field_metadata)
    offset_to_exchange_close: Optional[str] = field(default=None, metadata=field_metadata)
    multi_trading_session: Optional[bool] = field(default=None, metadata=field_metadata)
    multi_session: Optional[bool] = field(default=None, metadata=field_metadata)
    quote_consolidation: Optional[bool] = field(default=None, metadata=field_metadata)
    consolidation: Optional[bool] = field(default=None, metadata=field_metadata)
    primary: Optional[bool] = field(default=None, metadata=field_metadata)
    time_index: Optional[str] = field(default=None, metadata=field_metadata)
    empty_intervals: Optional[bool] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataSetFieldEntity(Base):
    name: str = field(default=None, metadata=field_metadata)
    description: str = field(default=None, metadata=field_metadata)
    type_: str = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    id_: Optional[str] = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    classifications: Optional[DataSetFieldEntityClassifications] = field(default=None, metadata=field_metadata)
    unique: Optional[bool] = field(default=False, metadata=field_metadata)
    field_java_type: Optional[str] = field(default=None, metadata=field_metadata)
    parameters: Optional[Union[DataSetFieldEntityNumberParameters, DataSetFieldEntityStringParameters]] = field(default=None, metadata=field_metadata)
    entitlements: Optional[Entitlements] = field(default=None, metadata=field_metadata)
    metadata: Optional[EntityMetadata] = field(default=None, metadata=field_metadata)
    attributes: Optional[DataSetFieldEntityAttributes] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataSetParameters(Base):
    frequency: str = field(default=None, metadata=field_metadata)
    category: Optional[str] = field(default=None, metadata=field_metadata)
    sub_category: Optional[str] = field(default=None, metadata=field_metadata)
    methodology: Optional[str] = field(default=None, metadata=field_metadata)
    coverage: Optional[str] = field(default=None, metadata=field_metadata)
    coverages: Optional[Tuple[AssetType, ...]] = field(default=None, metadata=field_metadata)
    notes: Optional[str] = field(default=None, metadata=field_metadata)
    history: Optional[str] = field(default=None, metadata=field_metadata)
    sample_start: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    sample_end: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    published_date: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    history_date: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    asset_class: Optional[AssetClass] = field(default=None, metadata=field_metadata)
    owner_ids: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    support_ids: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    support_distribution_list: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    apply_market_data_entitlements: Optional[bool] = field(default=None, metadata=field_metadata)
    upload_data_policy: Optional[str] = field(default=None, metadata=field_metadata)
    logical_db: Optional[str] = field(default=None, metadata=field_metadata)
    symbol_strategy: Optional[str] = field(default=None, metadata=field_metadata)
    underlying_data_set_id: Optional[str] = field(default=None, metadata=field_metadata)
    immutable: Optional[bool] = field(default=None, metadata=field_metadata)
    include_in_catalog: Optional[bool] = field(default=False, metadata=field_metadata)
    coverage_enabled: Optional[bool] = field(default=True, metadata=field_metadata)
    use_created_time_for_upload: Optional[bool] = field(default=None, metadata=field_metadata)
    apply_entity_entitlements: Optional[bool] = field(default=None, metadata=field_metadata)
    development_status: Optional[DevelopmentStatus] = field(default=None, metadata=field_metadata)
    internal_owned: Optional[bool] = field(default=None, metadata=field_metadata)
    cr_limit_read: Optional[int] = field(default=None, metadata=field_metadata)
    cr_limit_write: Optional[int] = field(default=None, metadata=field_metadata)
    alloy_config: Optional[AlloyConfig] = field(default=None, metadata=field_metadata)
    external_distribution: Optional[bool] = field(default=None, metadata=field_metadata)
    snowflake_db: Optional[str] = field(init=False, default='TIMESERIES', metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataSetTransformation(Base):
    transforms: DataSetTransforms = field(default=None, metadata=field_metadata)
    condition: Optional[DataSetCondition] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DeleteCoverageQuery(Base):
    where: Optional[FieldFilterMapDataQuery] = field(default=None, metadata=field_metadata)
    delete_all: Optional[bool] = field(default=False, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FieldColumnPair(Base):
    field_: Optional[str] = field(default=None, metadata=config(field_name='field', exclude=exclude_none))
    column: Optional[str] = field(default=None, metadata=field_metadata)
    field_description: Optional[str] = field(default=None, metadata=field_metadata)
    link: Optional[FieldLink] = field(default=None, metadata=field_metadata)
    aliases: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    display_alias: Optional[str] = field(default=None, metadata=field_metadata)
    resolvable: Optional[bool] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class HistoryFilter(Base):
    absolute_start: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    absolute_end: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    relative_start_seconds: Optional[float] = field(default=None, metadata=field_metadata)
    relative_end_seconds: Optional[float] = field(default=None, metadata=field_metadata)
    delay: Optional[Union[DataSetDelay, Tuple[DataSetDelay, ...]]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataQueryResponse(Base):
    type_: str = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    request_id: Optional[str] = field(default=None, metadata=field_metadata)
    error_message: Optional[str] = field(default=None, metadata=field_metadata)
    id_: Optional[str] = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    total_pages: Optional[int] = field(default=None, metadata=field_metadata)
    data_set_id: Optional[str] = field(default=None, metadata=field_metadata)
    entity_type: Optional[MeasureEntityType] = field(default=None, metadata=field_metadata)
    delay: Optional[int] = field(default=None, metadata=field_metadata)
    data: Optional[Tuple[FieldValueMap, ...]] = field(default=None, metadata=field_metadata)
    groups: Optional[Tuple[DataGroup, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataSetCatalogEntry(Base):
    id_: str = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    name: str = field(default=None, metadata=field_metadata)
    vendor: str = field(default=None, metadata=field_metadata)
    fields: DictBase = field(default=None, metadata=field_metadata)
    description: Optional[str] = field(default=None, metadata=field_metadata)
    short_description: Optional[str] = field(default=None, metadata=field_metadata)
    data_product: Optional[str] = field(default=None, metadata=field_metadata)
    terms: Optional[str] = field(default=None, metadata=field_metadata)
    internal_only: Optional[bool] = field(default=None, metadata=field_metadata)
    actions: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    default_start_seconds: Optional[float] = field(default=None, metadata=field_metadata)
    identifier_mapper_name: Optional[str] = field(default=None, metadata=field_metadata)
    identifier_updater_name: Optional[str] = field(default=None, metadata=field_metadata)
    default_delay_minutes: Optional[float] = field(default=None, metadata=field_metadata)
    apply_market_data_entitlements: Optional[bool] = field(default=None, metadata=field_metadata)
    sample: Optional[Tuple[FieldValueMap, ...]] = field(default=None, metadata=field_metadata)
    parameters: Optional[DataSetParameters] = field(default=None, metadata=field_metadata)
    tags: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    created_time: Optional[str] = field(default=None, metadata=field_metadata)
    last_updated_time: Optional[str] = field(default=None, metadata=field_metadata)
    start_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    mdapi: Optional[MDAPI] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataSetDimensions(Base):
    time_field: str = field(default=None, metadata=field_metadata)
    symbol_dimensions: Tuple[str, ...] = field(default=None, metadata=field_metadata)
    transaction_time_field: Optional[str] = field(default=None, metadata=field_metadata)
    symbol_dimension_properties: Optional[Tuple[FieldColumnPair, ...]] = field(default=None, metadata=field_metadata)
    non_symbol_dimensions: Optional[Tuple[FieldColumnPair, ...]] = field(default=None, metadata=field_metadata)
    symbol_dimension_link: Optional[FieldLink] = field(default=None, metadata=field_metadata)
    linked_dimensions: Optional[Tuple[FieldLinkSelector, ...]] = field(default=None, metadata=field_metadata)
    symbol_filter_dimensions: Optional[Tuple[SymbolFilterDimension, ...]] = field(default=None, metadata=field_metadata)
    key_dimensions: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    measures: Optional[Tuple[FieldColumnPair, ...]] = field(default=None, metadata=field_metadata)
    entity_dimension: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataSetFieldEntityBulkRequest(Base):
    fields: Tuple[DataSetFieldEntity, ...] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class EntityFilter(Base):
    operator: Optional[str] = field(default=None, metadata=field_metadata)
    simple_filters: Optional[Tuple[DataFilter, ...]] = field(default=None, metadata=field_metadata)
    complex_filters: Optional[Tuple[ComplexFilter, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataSetFilters(Base):
    entity_filter: Optional[EntityFilter] = field(default=None, metadata=field_metadata)
    row_filters: Optional[Tuple[DataFilter, ...]] = field(default=None, metadata=field_metadata)
    advanced_filters: Optional[Tuple[AdvancedFilter, ...]] = field(default=None, metadata=field_metadata)
    history_filter: Optional[HistoryFilter] = field(default=None, metadata=field_metadata)
    time_filter: Optional[TimeFilter] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataSetEntity(Base):
    id_: str = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    name: str = field(default=None, metadata=field_metadata)
    organization_id: Optional[str] = field(default=None, metadata=field_metadata)
    description: Optional[str] = field(default=None, metadata=field_metadata)
    short_description: Optional[str] = field(default=None, metadata=field_metadata)
    mappings: Optional[Tuple[MarketDataMapping, ...]] = field(default=None, metadata=field_metadata)
    vendor: Optional[MarketDataVendor] = field(default=None, metadata=field_metadata)
    mdapi: Optional[MDAPI] = field(default=None, metadata=field_metadata)
    data_product: Optional[str] = field(default=None, metadata=field_metadata)
    entitlements: Optional[Entitlements] = field(default=None, metadata=field_metadata)
    query_processors: Optional[ProcessorEntity] = field(default=None, metadata=field_metadata)
    parameters: Optional[DataSetParameters] = field(default=None, metadata=field_metadata)
    dimensions: Optional[DataSetDimensions] = field(default=None, metadata=field_metadata)
    coverage_properties: Optional[DataSetCoverageProperties] = field(default=None, metadata=field_metadata)
    defaults: Optional[DataSetDefaults] = field(default=None, metadata=field_metadata)
    filters: Optional[DataSetFilters] = field(default=None, metadata=field_metadata)
    transformations: Optional[Tuple[DataSetTransformation, ...]] = field(default=None, metadata=field_metadata)
    created_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    created_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    last_updated_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    last_updated_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    tags: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    type_: Optional[DataSetType] = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
