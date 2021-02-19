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

import json
import logging
from collections import defaultdict
from dataclasses import asdict
from datetime import datetime
from numbers import Number
from typing import List, Dict, Optional

import numpy as np
from pandas import DataFrame

from gs_quant.analytics.common import DATAGRID_HELP_MSG
from gs_quant.analytics.common.helpers import resolve_entities, get_rdate_cache_key
from gs_quant.analytics.core.processor import DataQueryInfo
from gs_quant.analytics.core.processor_result import ProcessorResult
from gs_quant.analytics.core.query_helpers import aggregate_queries, fetch_query, build_query_string
from gs_quant.analytics.datagrid.data_cell import DataCell
from gs_quant.analytics.datagrid.data_column import DataColumn, ColumnFormat
from gs_quant.analytics.datagrid.data_row import DataRow, DimensionsOverride, ProcessorOverride, Override
from gs_quant.analytics.datagrid.utils import DataGridSort, SortOrder, SortType, DataGridFilter, FilterOperation, \
    FilterCondition
from gs_quant.analytics.processors import CoordinateProcessor, EntityProcessor
from gs_quant.datetime.relative_date import RelativeDate
from gs_quant.entities.entity import Entity
from gs_quant.errors import MqValueError
from gs_quant.session import GsSession

_logger = logging.getLogger(__name__)

API = '/data/grids'
DATAGRID_HEADERS: Dict[str, str] = {'Content-Type': 'application/json;charset=utf-8'}


class DataGrid:
    """
    DataGrid is a object for fetching Marquee data and applying processors (functions). DataGrids can be
    persisted via the DataGrid API and utilized on the Marquee Markets platform.

    :param name: Name of the DataGrid
    :param rows: List of DataGrid rows for the grid
    :param columns: List of DataGrid columns for the grid
    :param id_: Unique identifier of the grid
    :param entitlements: Marquee entitlements of the grid for the Marquee Market's platform

    **Usage**

    To create a DataGrid, we define two components, rows and columns:

    >>> from gs_quant.markets.securities import Asset, AssetIdentifier
    >>> from gs_quant.data.coordinate import DataMeasure, DataFrequency
    >>> from gs_quant.analytics.processors import LastProcessor
    >>>
    >>> GS = Asset.get("GS UN", AssetIdentifier.BLOOMBERG_ID)
    >>> AAPL = Asset.get("AAPL UW", AssetIdentifier.BLOOMBERG_ID)
    >>> rows = [
    >>>     DataRow(GS),
    >>>     DataRow(AAPL)
    >>> ]
    >>> trade_price = DataCoordinate(
    >>>    measure=DataMeasure.TRADE_PRICE,
    >>>    frequency=DataFrequency.REAL_TIME,
    >>> )
    >>>
    >>> col_0 = DataColumn(name="Name", processor=EntityProcessor(field="short_name"))
    >>> col_1 = DataColumn(name="Last", processor=LastProcessor(trade_price))
    >>> columns = [ col_0, col_1 ]
    >>>
    >>> datagrid = DataGrid(name="Example DataGrid", rows=rows, columns=columns)
    >>> datagrid.initialize()
    >>> datagrid.poll()
    >>> print(datagrid.to_frame())

    **Documentation**

    Full Documentation and examples can be found here:
    https://developer.gs.com/docs/gsquant/tutorials/Data/DataGrid/
    """

    def __init__(self,
                 name: str,
                 rows: List[DataRow],
                 columns: List[DataColumn],
                 *,
                 id_: str = None,
                 entitlements: Optional[Dict[str, List[str]]] = None,
                 sorts: Optional[List[DataGridSort]] = None,
                 filters: Optional[List[DataGridFilter]] = None,
                 **kwargs):
        self.id_ = id_
        self.entitlements = entitlements
        self.name = name
        self.rows = rows
        self.columns = columns
        self.sorts = sorts or []
        self.filters = filters or []

        # store the graph, data queries to leaf processors and results
        self._primary_column_index: int = kwargs.get('primary_column_index', 0)
        self._cells: List[DataCell] = []
        self._data_queries: List[DataQueryInfo] = []
        self._entity_cells: List[DataCell] = []
        self._coord_processor_cells: List[DataCell] = []

        self.results: List[List[DataCell]] = []
        self.is_initialized: bool = False
        print(DATAGRID_HELP_MSG)

    def get_id(self) -> Optional[str]:
        """Get the unique DataGrid identifier. Will only exists if the DataGrid has been persisted. """
        return self.id_

    def initialize(self) -> None:
        """
        Initializes the DataGrid.

        Iterates over all rows and columns, preparing cell structures.
        Cells then contain a graph and data queries to leaf processors.

        Upon providing data to a leaf, the leaf processor is calculated and propagated up the graph to the cell level.
        """
        all_queries: List[DataQueryInfo] = []
        entity_cells: List[DataCell] = []

        # Loop over rows, columns
        for row_index, row in enumerate(self.rows):
            entity: Entity = row.entity
            cells: List[DataCell] = []
            row_overrides = row.overrides

            for column_index, column in enumerate(self.columns):
                column_name = column.name
                column_processor = column.processor

                # Get all the data coordinate overrides and apply the processor override if it exists
                data_overrides = _get_overrides(row_overrides, column_name, column)

                # Create the cell
                cell: DataCell = DataCell(column_name,
                                          column_processor,
                                          entity,
                                          data_overrides,
                                          column_index,
                                          row_index)

                # treat data cells different to entity
                if isinstance(column_processor, EntityProcessor):
                    # store these cells to fetch entity data during poll
                    entity_cells.append(cell)
                if isinstance(column_processor, CoordinateProcessor):
                    # store these cells to fetch entity data during poll
                    if len(data_overrides):
                        # Get the last in the list if more than 1 override is given
                        cell.processor.children['a'].set_dimensions(data_overrides[-1].dimensions)

                    self._coord_processor_cells.append(cell)
                else:
                    # append the required queries to the map
                    cell.build_cell_graph(all_queries)

                cells.append(cell)

            self._cells.extend(cells)
            self.results.append(cells)

        self._data_queries = all_queries
        self._entity_cells = entity_cells
        self.is_initialized = True

    def poll(self) -> None:
        """ Poll the data queries required to process this grid.
            Set the results at the leaf processors
        """
        self._resolve_queries()
        self._process_special_cells()
        self.__send_activity()
        self._fetch_queries()

    def save(self) -> str:
        """
        Saves the DataGrid. If the DataGrid has already been created, the DataGrid will be updated.
        If the DataGrid has not been created it will be added to the DataGrid service.
        :return: Unique identifier of the DataGrid
        """
        datagrid_json = self.__as_json()
        if self.id_:
            response = GsSession.current._put(f'{API}/{self.id_}', datagrid_json, request_headers=DATAGRID_HEADERS)
        else:
            response = GsSession.current._post(f'{API}', datagrid_json, request_headers=DATAGRID_HEADERS)
            self.id_ = response['id']
        return DataGrid.from_dict(response).id_

    def create(self):
        """
        Creates a new DataGrid even if the DataGrid already exists.
        If the DataGrid has already been persisted, the DataGrid id will be replaced with the newly persisted DataGrid.
        :return: New DataGrid unique identifier
        """
        datagrid_json = self.__as_json()
        response = GsSession.current._post(f'{API}', datagrid_json, request_headers=DATAGRID_HEADERS)
        self.id_ = response['id']
        return response['id']

    def delete(self):
        """
        Deletes the DataGrid if it has been persisted.
        :return: None
        """
        if self.id_:
            GsSession.current._delete(f'{API}/{self.id_}', request_headers=DATAGRID_HEADERS)
        else:
            raise MqValueError('DataGrid has not been persisted.')

    def _process_special_cells(self) -> None:
        """
        Processes Coordinate and Entity cells

        :return: None
        """
        # fetch entity cells
        for cell in self._entity_cells:
            try:
                cell.value = cell.processor.process(cell.entity)
            except Exception as e:
                cell.value = f'Error Calculating processor {cell.processor.__class__.__name__} ' \
                             f'for entity: {cell.entity.get_marquee_id()} due to {e}'

            cell.updated_time = f'{datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]}Z'

        for cell in self._coord_processor_cells:
            try:
                cell.value = cell.processor.process()
            except Exception as e:
                cell.value = f'Error Calculating processor {cell.processor.__class__.__name__} ' \
                             f'for entity: {cell.entity.get_marquee_id()} due to {e}'

            cell.updated_time = f'{datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]}Z'

    def _resolve_queries(self) -> None:
        """ Resolves the dataset_id for each data query
            This is used to query data thereafter
        """
        local_rule_cache = {}
        local_availablility_cache = {}

        for query in self._data_queries:
            entity = query.entity
            query = query.query
            coord = query.coordinate
            entity_dimension = entity.data_dimension
            query_start = query.start
            query_end = query.end
            entity_dict = entity.get_entity()
            if entity_dict is None:
                currencies = None
                exchanges = None
            else:
                currency = entity_dict.get("currency")
                exchange = entity_dict.get("exchange")
                currencies = [currency] if currency else None
                exchanges = [exchange] if exchange else None

            if isinstance(query_start, RelativeDate):
                cache_key = get_rdate_cache_key(query_start.rule, currencies, exchanges)
                if cache_key in local_rule_cache:
                    query.start = local_rule_cache[cache_key]
                else:
                    query.start = query_start.apply_rule(currencies=currencies, exchanges=exchanges)
                    local_rule_cache[cache_key] = query.start

            if isinstance(query_end, RelativeDate):
                cache_key = get_rdate_cache_key(query_start.rule, currencies, exchanges)
                if cache_key in local_rule_cache:
                    query.end = local_rule_cache[cache_key]
                else:
                    query.end = query_end.apply_rule(currencies=currencies, exchanges=exchanges)
                    local_rule_cache[cache_key] = query.end

            if entity_dimension not in coord.dimensions:
                if coord.dataset_id:
                    # don't need to fetch the data set if user supplied it
                    coord.set_dimensions({entity_dimension: entity.get_marquee_id()})
                    query.coordinate = coord
                else:
                    # Need to resolve the dataset from availability
                    entity_id = entity.get_marquee_id()
                    try:
                        raw_availability = local_availablility_cache.get(entity_id)
                        if raw_availability is None:
                            raw_availability: Dict = GsSession.current._get(f'/data/measures/{entity_id}/availability')
                            local_availablility_cache[entity.get_marquee_id()] = raw_availability
                        query.coordinate = entity.get_data_coordinate(measure=coord.measure,
                                                                      dimensions=coord.dimensions,
                                                                      frequency=coord.frequency,
                                                                      availability=raw_availability)
                    except Exception as e:
                        _logger.info(
                            f'Could not get DataCoordinate with {coord} for entity {entity_id} due to {e}')

    def _fetch_queries(self):
        query_aggregations = aggregate_queries(self._data_queries)

        for dataset_id, query_map in query_aggregations.items():
            for query in query_map.values():
                df = fetch_query(query)
                for query_dimensions, query_infos in query['queries'].items():
                    query_string = build_query_string(query_dimensions)
                    queried_df = df.query(query_string)
                    for query_info in query_infos:
                        series = queried_df[query_info.query.coordinate.measure]
                        query_info.data = series

        for query_info in self._data_queries:
            if query_info.data is None or len(query_info.data) == 0:
                query_info.processor.calculate(query_info.attr,
                                               ProcessorResult(False,
                                                               f'No data found for '
                                                               f'Coordinate {query_info.query.coordinate}'))
            else:
                query_info.processor.calculate(query_info.attr, ProcessorResult(True, query_info.data))

    @staticmethod
    def aggregate_queries(query_infos):
        mappings = defaultdict(dict)
        for query_info in query_infos:
            query = query_info.query
            coordinate = query.coordinate
            dataset_mappings = mappings[coordinate.dataset_id]
            query_key = query.get_range_string()
            dataset_mappings.setdefault(query_key, {
                'parameters': {},
                'queries': {}
            })
            queries = dataset_mappings[query_key]['queries']
            queries[coordinate.get_dimensions()] = query_info
            parameters = dataset_mappings[query_key]['parameters']
            for dimension, value in coordinate.dimensions.items():
                parameters.setdefault(dimension, set())
                parameters[dimension].add(value)

    def _post_process(self) -> DataFrame:
        columns = self.columns
        results = defaultdict(list)
        for row in self.results:
            for column in row:
                column_value = column.value
                if column_value.success is True:
                    column_data = column_value.data
                    if isinstance(column_data, Number):
                        format_: ColumnFormat = columns[column.column_index].format_
                        results[column.name].append(round(column_data, format_.precision))
                    else:
                        results[column.name].append(column_data)
                else:
                    results[column.name].append(np.NaN)

        df = DataFrame.from_dict(results)
        df = self.__handle_filters(df)
        df = self.__handle_sorts(df)
        return df

    def __handle_sorts(self, df):
        """
        Handles sorting of the dataframe
        :param df: incoming dataframe to be sorted
        :return: dataframe with sorting applied if any
        """
        for sort in self.sorts:
            ascending = True if sort.order == SortOrder.ASCENDING else False
            if sort.sortType == SortType.ABSOLUTE_VALUE:
                df = df.reindex(df[sort.columnName].abs().sort_values(ascending=ascending, na_position='last').index)
            else:
                df = df.sort_values(by=sort.columnName, ascending=ascending, na_position='last')
        return df

    def __handle_filters(self, df) -> DataFrame:
        """
        Handles filtering the dataframe
        :param df: incoming dataframe to be filtered
        :return: dataframe with filters applied if any
        """
        if not len(df):
            return df
        starting_df = df.copy()
        running_df = df
        for filter_ in self.filters:
            filter_value = filter_.value
            if filter_value is None:
                continue
            filter_condition = filter_.condition
            if filter_condition == FilterCondition.OR:
                df = starting_df
            else:
                df = running_df

            column_name = filter_.columnName
            operation = filter_.operation
            if operation == FilterOperation.TOP:
                df = df.sort_values(by=column_name, ascending=False, na_position='last').head(filter_value)
            elif operation == FilterOperation.BOTTOM:
                df = df.sort_values(by=column_name, ascending=True, na_position='last').head(filter_value)
            elif operation == FilterOperation.ABSOLUTE_TOP:
                df = df.reindex(df[column_name].abs().sort_values(ascending=False, na_position='last').index).head(
                    filter_value)
            elif operation == FilterOperation.ABSOLUTE_BOTTOM:
                df = df.reindex(df[column_name].abs().sort_values(ascending=True, na_position='last').index).head(
                    filter_value)
            elif operation == FilterOperation.EQUALS:
                if not isinstance(filter_value, list):
                    filter_value = [filter_value]
                # Special case to handle different types of floats
                if isinstance(filter_value[0], str):
                    df = df.loc[df[column_name].isin(filter_value)]
                else:
                    # Add a tolerance for the special case to handle different types of floats
                    df = df[np.isclose(df[column_name].values[:, None], filter_value, atol=1e-10).any(axis=1)]
            elif operation == FilterOperation.NOT_EQUALS:
                if not isinstance(filter_value, list):
                    filter_value = [filter_value]
                if isinstance(filter_value[0], str):
                    df = df.loc[~df[column_name].isin(filter_value)]
                else:
                    # Add a tolerance for the special case to handle different types of float
                    df = df[~np.isclose(df[column_name].values[:, None], filter_value, atol=1e-10).any(axis=1)]
            elif operation == FilterOperation.GREATER_THAN:
                df = df[df[column_name] > filter_value]
            elif operation == FilterOperation.LESS_THAN:
                df = df[df[column_name] < filter_value]
            elif operation == FilterOperation.LESS_THAN_EQUALS:
                df = df[df[column_name] <= filter_value]
            elif operation == FilterOperation.GREATER_THAN_EQUALS:
                df = df[df[column_name] >= filter_value]
            else:
                raise MqValueError(f'Invalid Filter operation Type: {operation}')

            if filter_.condition == FilterCondition.OR:
                # Need to merge the results
                running_df = running_df.merge(df, how='outer')
            else:
                running_df = df

        return running_df

    def to_frame(self) -> DataFrame:
        """
        Returns the results of the DataGrid data fetching and applied processors.
        :return: DataFrame of results
        """
        if not self.is_initialized:
            _logger.info("Grid has not been initialized. Ensure to run DataGrid.initialize()")
            return DataFrame()

        return self._post_process()

    @classmethod
    def from_dict(cls, obj, reference_list: Optional[List] = None):
        id_ = obj.get('id', None)
        name = obj.get('name', '')
        parameters = obj.get('parameters', {})
        entitlements = obj.get('entitlements', {})

        # If a reference list is given, then the entities will be resolved by the caller
        if reference_list is not None:
            should_resolve_entities = False
        else:
            should_resolve_entities = True
            reference_list = []

        rows = [DataRow.from_dict(row, reference_list) for row in parameters.get('rows', [])]
        columns = [DataColumn.from_dict(column, reference_list) for column in parameters.get('columns', [])]
        sorts = [DataGridSort.from_dict(sort) for sort in parameters.get('sorts', [])]
        filters = [DataGridFilter.from_dict(filter_) for filter_ in parameters.get('filters', [])]

        if should_resolve_entities:
            resolve_entities(reference_list)

        return DataGrid(name=name,
                        rows=rows,
                        columns=columns,
                        id_=id_,
                        entitlements=entitlements,
                        primary_column_index=parameters.get('primaryColumnIndex', 0),
                        sorts=sorts,
                        filters=filters)

    def as_dict(self):
        datagrid = {
            'name': self.name,
            'parameters': {
                'rows': [row.as_dict() for row in self.rows],
                'columns': [column.as_dict() for column in self.columns],
                'primaryColumnIndex': self._primary_column_index
            }
        }
        if self.entitlements:
            datagrid['entitlements'] = self.entitlements
        if len(self.sorts):
            datagrid['parameters']['sorts'] = [asdict(sort) for sort in self.sorts]
        if len(self.filters):
            datagrid['parameters']['filters'] = [asdict(filter_) for filter_ in self.filters]
        return datagrid

    def set_primary_column_index(self, index: int):
        """
        Sets the primary column index which affects which row will expand to fill any additional horizontal space.
        :param index: index of the column to make primary
        :return: None
        """
        self._primary_column_index = index

    def set_sorts(self, sorts: List[DataGridSort]):
        """
        Set the sorts parameter of the grid response
        :param sorts: value of grid sorts
        :return: None
        """
        self.sorts = sorts

    def add_sort(self, sort: DataGridSort, index: int = None):
        """
        Add a sort to the grid response
        :param sort: DataGridSort
        :param index: index of the sort object to be added, defaults to end of sorts list
        :return: None
        """
        if index:
            self.sorts.insert(index, sort)
        else:
            self.sorts.append(sort)

    def set_filters(self, filters: List[DataGridFilter]):
        """
        Set the filters parameter of the grid response
        :param filters: value of grid sorts
        :return: None
        """
        self.filters = filters

    def add_filter(self, filter_: DataGridFilter, index: int = None):
        """
        Add a filter to the grid response
        :param filter_: DataGridFilter
        :param index: index of the sort object to be added, defaults to end of filters list
        :return: None
        """
        if index:
            self.filters.insert(index, filter_)
        else:
            self.filters.append(filter_)

    def __as_json(self) -> str:
        return json.dumps(self.as_dict())

    def __send_activity(self):
        try:
            body = {
                'resource': 'DataGrid',
                'action': 'Calculated',
                'parameters': {
                    'dataGridId': self.id_ or "NotPersisted"
                },
                'kpis': [{'id': 'DataGrid_Calculated', 'value': 1}],
                'context': {
                    'apiDomain': True,
                    'userAgent': "gs_quant"
                }
            }
            GsSession.current._post('/activities', payload=body)
        except Exception as e:
            _logger.warning(f"Unable to track DataGrid_Calculated activity. Details: {e}")


def _get_overrides(row_overrides: List[Override],
                   column_name: str,
                   column: DataColumn) -> List[DimensionsOverride]:
    if not row_overrides:
        return []

    data_overrides: List[DimensionsOverride] = [row_override for row_override in row_overrides if
                                                isinstance(row_override, DimensionsOverride) and
                                                column_name in row_override.column_names]

    # Get the first processor override if it exists and set on the column
    processor_overrides: List[ProcessorOverride] = [row_override for row_override in row_overrides if
                                                    isinstance(row_override, ProcessorOverride) and
                                                    column_name in row_override.column_names]
    if len(processor_overrides):
        # Apply the processor override if it exists
        column.processor = processor_overrides[0].processor

    return data_overrides
