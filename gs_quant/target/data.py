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


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class AdvancedFilter(Base):
    column: str = None
    operator: str = None
    value: Optional[float] = None
    values: Optional[Tuple[str, ...]] = None
    format_: Optional[str] = field(default=None, metadata=config(field_name='format'))


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataSetCondition(Base):
    column: str = None
    operator: str = None
    value: Optional[float] = None
    values: Optional[Tuple[str, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataSetDefaults(Base):
    start_seconds: Optional[float] = None
    end_seconds: Optional[float] = None
    delay_seconds: Optional[float] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataSetFieldEntityAttributes(Base):
    in_code: Optional[bool] = None
    is_entity: Optional[bool] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataSetFieldEntityClassifications(Base):
    groups: Optional[Tuple[str, ...]] = None
    data_set_id: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataSetFieldEntityNumberParameters(Base):
    maximum: Optional[int] = None
    minimum: Optional[int] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class EntityMetadata(Base):
    created_by_id: Optional[str] = None
    created_time: Optional[datetime.datetime] = None
    last_updated_by_id: Optional[str] = None
    last_updated_time: Optional[datetime.datetime] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ErrorInfo(Base):
    status_code: int = None
    reason_phrase: str = None
    title: Optional[str] = None
    messages: Optional[Tuple[str, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FieldLinkSelector(Base):
    field_selector: Optional[str] = None
    description: Optional[str] = None
    display_name: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MDAPI(Base):
    type_: str = field(default=None, metadata=config(field_name='type'))
    quoting_styles: Tuple[DictBase, ...] = None
    class_: Optional[str] = field(default=None, metadata=config(field_name='class'))


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MarketDataField(Base):
    name: Optional[str] = None
    mapping: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MarketDataFilteredField(Base):
    field_: Optional[str] = field(default=None, metadata=config(field_name='field'))
    default_value: Optional[str] = None
    default_numerical_value: Optional[float] = None
    default_boolean_value: Optional[bool] = None
    numerical_values: Optional[Tuple[float, ...]] = None
    values: Optional[Tuple[str, ...]] = None
    multi_measure: Optional[bool] = None


class MeasureBacktest(DictBase):
    pass


class MeasureKpi(DictBase):
    pass


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MidPrice(Base):
    bid_column: Optional[str] = None
    ask_column: Optional[str] = None
    mid_column: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ParserEntity(Base):
    only_normalized_fields: Optional[bool] = None
    quotes: Optional[bool] = None
    trades: Optional[bool] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RemapFieldPair(Base):
    field_: Optional[str] = field(default=None, metadata=config(field_name='field'))
    remap_to: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ResponseInfo(Base):
    request_id: Optional[str] = None
    messages: Optional[Tuple[str, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SymbolFilterLink(Base):
    entity_type: Optional[str] = 'MktCoordinate'
    entity_field: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataFilter(Base):
    field_: str = field(default=None, metadata=config(field_name='field'))
    values: Tuple[str, ...] = None
    column: Optional[str] = None
    where: Optional[DataSetCondition] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataSetCoverageProperties(Base):
    prefixes: Optional[Tuple[str, ...]] = None
    prefix_type: Optional[str] = None
    asset_classes: Optional[Tuple[AssetClass, ...]] = None
    asset_types: Optional[Tuple[AssetType, ...]] = None
    entity_types: Optional[Tuple[MeasureEntityType, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataSetDelay(Base):
    until_seconds: float = None
    at_time_zone: str = None
    when: Optional[Tuple[DelayExclusionType, ...]] = None
    history_up_to_seconds: Optional[float] = None
    history_up_to_time: Optional[datetime.datetime] = None
    history_up_to_months: Optional[float] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataSetFieldEntityStringParameters(Base):
    enum: Optional[Tuple[str, ...]] = None
    format_: Optional[FieldFormat] = field(default=None, metadata=config(field_name='format'))
    pattern: Optional[str] = '^[\w ]{1,256}$'
    max_length: Optional[int] = None
    min_length: Optional[int] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataSetParameters(Base):
    frequency: str = None
    category: Optional[str] = None
    sub_category: Optional[str] = None
    methodology: Optional[str] = None
    coverage: Optional[str] = None
    coverages: Optional[Tuple[AssetType, ...]] = None
    notes: Optional[str] = None
    history: Optional[str] = None
    sample_start: Optional[datetime.datetime] = None
    sample_end: Optional[datetime.datetime] = None
    published_date: Optional[datetime.datetime] = None
    history_date: Optional[datetime.datetime] = None
    asset_class: Optional[AssetClass] = None
    owner_ids: Optional[Tuple[str, ...]] = None
    support_ids: Optional[Tuple[str, ...]] = None
    support_distribution_list: Optional[Tuple[str, ...]] = None
    apply_market_data_entitlements: Optional[bool] = None
    upload_data_policy: Optional[str] = None
    logical_db: Optional[str] = None
    symbol_strategy: Optional[str] = None
    underlying_data_set_id: Optional[str] = None
    immutable: Optional[bool] = None
    include_in_catalog: Optional[bool] = False
    coverage_enabled: Optional[bool] = True
    use_created_time_for_upload: Optional[bool] = None
    apply_entity_entitlements: Optional[bool] = None
    development_status: Optional[DevelopmentStatus] = None
    internal_owned: Optional[bool] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataSetTransforms(Base):
    redact_columns: Optional[Tuple[str, ...]] = None
    round_columns: Optional[Tuple[str, ...]] = None
    remap_fields: Optional[Tuple[RemapFieldPair, ...]] = None


class FieldFilterMapDataQuery(DictBase):
    pass


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FieldLink(Base):
    entity_type: Optional[str] = 'Asset'
    entity_identifier: Optional[str] = None
    prefix: Optional[str] = None
    additional_entity_fields: Optional[Tuple[FieldLinkSelector, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MarketDataMapping(Base):
    asset_class: Optional[AssetClass] = None
    query_type: Optional[str] = None
    description: Optional[str] = None
    scale: Optional[float] = None
    frequency: Optional[MarketDataFrequency] = None
    measures: Optional[Tuple[MarketDataMeasure, ...]] = None
    data_set: Optional[str] = None
    vendor: Optional[MarketDataVendor] = None
    fields: Optional[Tuple[MarketDataField, ...]] = None
    rank: Optional[float] = None
    filtered_fields: Optional[Tuple[MarketDataFilteredField, ...]] = None
    asset_types: Optional[Tuple[AssetType, ...]] = None
    entity_type: Optional[MeasureEntityType] = None
    backtest_entity: Optional[MeasureBacktest] = None
    kpi_entity: Optional[MeasureKpi] = None
    multi_measure: Optional[bool] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ProcessorEntity(Base):
    filters: Optional[Tuple[str, ...]] = None
    parsers: Optional[Tuple[ParserEntity, ...]] = None
    deduplicate: Optional[Tuple[str, ...]] = None
    enum_type: Optional[Tuple[str, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SymbolFilterDimension(Base):
    field_: Optional[str] = field(default=None, metadata=config(field_name='field'))
    field_description: Optional[str] = None
    symbol_filter_link: Optional[SymbolFilterLink] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ComplexFilter(Base):
    operator: str = None
    simple_filters: Tuple[DataFilter, ...] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataGroup(Base):
    context: Optional[FieldValueMap] = None
    data: Optional[Tuple[FieldValueMap, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataQuery(Base):
    id_: Optional[str] = field(default=None, metadata=config(field_name='id'))
    data_set_id: Optional[str] = None
    format_: Optional[Format] = field(default=None, metadata=config(field_name='format'))
    where: Optional[FieldFilterMapDataQuery] = None
    vendor: Optional[MarketDataVendor] = None
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None
    start_time: Optional[datetime.datetime] = None
    page: Optional[int] = None
    page_size: Optional[int] = None
    end_time: Optional[datetime.datetime] = None
    relative_start_date: Optional[str] = None
    relative_end_date: Optional[str] = None
    as_of_time: Optional[datetime.datetime] = None
    id_as_of_date: Optional[datetime.date] = None
    use_temporal_x_ref: Optional[bool] = False
    restrict_secondary_identifier: Optional[bool] = False
    since: Optional[datetime.datetime] = None
    dates: Optional[Tuple[datetime.date, ...]] = None
    times: Optional[Tuple[datetime.datetime, ...]] = None
    delay: Optional[int] = None
    intervals: Optional[int] = None
    samples: Optional[int] = None
    limit: Optional[int] = None
    polling_interval: Optional[int] = None
    grouped: Optional[bool] = None
    fields: Optional[Tuple[Union[DictBase, str], ...]] = None
    restrict_fields: Optional[bool] = False
    entity_filter: Optional[FieldFilterMapDataQuery] = None
    interval: Optional[str] = None
    distinct_consecutive: Optional[bool] = False
    time_filter: Optional[TimeFilter] = None
    use_field_alias: Optional[bool] = False
    remap_schema_to_alias: Optional[bool] = False
    show_linked_dimensions: Optional[bool] = True
    use_project_processor: Optional[bool] = False
    snapshot: Optional[bool] = False


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataSetCatalogEntry(Base):
    id_: str = field(default=None, metadata=config(field_name='id'))
    name: str = None
    vendor: str = None
    fields: DictBase = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    data_product: Optional[str] = None
    terms: Optional[str] = None
    internal_only: Optional[bool] = None
    actions: Optional[Tuple[str, ...]] = None
    default_start_seconds: Optional[float] = None
    identifier_mapper_name: Optional[str] = None
    identifier_updater_name: Optional[str] = None
    default_delay_minutes: Optional[float] = None
    apply_market_data_entitlements: Optional[bool] = None
    sample: Optional[Tuple[FieldValueMap, ...]] = None
    parameters: Optional[DataSetParameters] = None
    tags: Optional[Tuple[str, ...]] = None
    created_time: Optional[str] = None
    last_updated_time: Optional[str] = None
    start_date: Optional[datetime.date] = None
    mdapi: Optional[MDAPI] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataSetFieldEntity(Base):
    name: str = None
    description: str = None
    type_: str = field(default=None, metadata=config(field_name='type'))
    id_: Optional[str] = field(default=None, metadata=config(field_name='id'))
    classifications: Optional[DataSetFieldEntityClassifications] = None
    unique: Optional[bool] = False
    field_java_type: Optional[str] = None
    parameters: Optional[DictBase] = None
    entitlements: Optional[Entitlements] = None
    metadata: Optional[EntityMetadata] = None
    attributes: Optional[DataSetFieldEntityAttributes] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataSetTransformation(Base):
    transforms: DataSetTransforms = None
    condition: Optional[DataSetCondition] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DeleteCoverageQuery(Base):
    where: Optional[FieldFilterMapDataQuery] = None
    delete_all: Optional[bool] = False


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FieldColumnPair(Base):
    field_: Optional[str] = field(default=None, metadata=config(field_name='field'))
    column: Optional[str] = None
    field_description: Optional[str] = None
    link: Optional[FieldLink] = None
    aliases: Optional[Tuple[str, ...]] = None
    resolvable: Optional[bool] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class HistoryFilter(Base):
    absolute_start: Optional[datetime.datetime] = None
    absolute_end: Optional[datetime.datetime] = None
    relative_start_seconds: Optional[float] = None
    relative_end_seconds: Optional[float] = None
    delay: Optional[DictBase] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataQueryResponse(Base):
    type_: str = field(default=None, metadata=config(field_name='type'))
    request_id: Optional[str] = None
    error_message: Optional[str] = None
    id_: Optional[str] = field(default=None, metadata=config(field_name='id'))
    total_pages: Optional[int] = None
    data_set_id: Optional[str] = None
    entity_type: Optional[MeasureEntityType] = None
    delay: Optional[int] = None
    data: Optional[Tuple[FieldValueMap, ...]] = None
    groups: Optional[Tuple[DataGroup, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataSetDimensions(Base):
    symbol_dimensions: Tuple[str, ...] = None
    time_field: Optional[str] = None
    transaction_time_field: Optional[str] = None
    symbol_dimension_properties: Optional[Tuple[FieldColumnPair, ...]] = None
    non_symbol_dimensions: Optional[Tuple[FieldColumnPair, ...]] = None
    symbol_dimension_link: Optional[FieldLink] = None
    linked_dimensions: Optional[Tuple[FieldLinkSelector, ...]] = None
    symbol_filter_dimensions: Optional[Tuple[SymbolFilterDimension, ...]] = None
    key_dimensions: Optional[Tuple[str, ...]] = None
    measures: Optional[Tuple[FieldColumnPair, ...]] = None
    entity_dimension: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataSetFieldEntityBulkRequest(Base):
    fields: Tuple[DataSetFieldEntity, ...] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class EntityFilter(Base):
    operator: Optional[str] = None
    simple_filters: Optional[Tuple[DataFilter, ...]] = None
    complex_filters: Optional[Tuple[ComplexFilter, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataSetFilters(Base):
    entity_filter: Optional[EntityFilter] = None
    row_filters: Optional[Tuple[DataFilter, ...]] = None
    advanced_filters: Optional[Tuple[AdvancedFilter, ...]] = None
    history_filter: Optional[HistoryFilter] = None
    time_filter: Optional[TimeFilter] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataSetEntity(Base):
    id_: str = field(default=None, metadata=config(field_name='id'))
    name: str = None
    organization_id: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    mappings: Optional[Tuple[MarketDataMapping, ...]] = None
    vendor: Optional[MarketDataVendor] = None
    mdapi: Optional[MDAPI] = None
    data_product: Optional[str] = None
    entitlements: Optional[Entitlements] = None
    query_processors: Optional[ProcessorEntity] = None
    parameters: Optional[DataSetParameters] = None
    dimensions: Optional[DataSetDimensions] = None
    coverage_properties: Optional[DataSetCoverageProperties] = None
    defaults: Optional[DataSetDefaults] = None
    filters: Optional[DataSetFilters] = None
    transformations: Optional[Tuple[DataSetTransformation, ...]] = None
    created_by_id: Optional[str] = None
    created_time: Optional[datetime.datetime] = None
    last_updated_by_id: Optional[str] = None
    last_updated_time: Optional[datetime.datetime] = None
    tags: Optional[Tuple[str, ...]] = None
