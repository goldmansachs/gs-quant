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
import asyncio
import logging
from collections import defaultdict
from datetime import date, datetime
from typing import Dict, Tuple, Union

from pandas import DataFrame, to_datetime

from gs_quant.analytics.core.processor import MeasureQueryInfo
from gs_quant.analytics.core.processor_result import ProcessorResult
from gs_quant.data import DataFrequency
from gs_quant.session import GsSession

_logger = logging.getLogger(__name__)


def aggregate_queries(query_infos):
    mappings = defaultdict(dict)  # DataSet -> start/end
    for query_info in query_infos:
        if isinstance(query_info, MeasureQueryInfo):
            continue
        query = query_info.query
        coordinate = query.coordinate
        dataset_id = coordinate.dataset_id
        dataset_mappings = mappings[dataset_id]
        query_key = query.get_range_string()
        if dataset_id is None:
            series: ProcessorResult = ProcessorResult(False,
                                                      f'No dataset resolved for '
                                                      f'measure={coordinate.measure} with '
                                                      f'dimensions={coordinate.dimensions}')
            asyncio.get_event_loop().run_until_complete(query_info.processor.calculate(query_info.attr, series, None))
            continue
        dataset_mappings.setdefault(query_key, {
            'datasetId': dataset_id,
            'parameters': {},
            'queries': defaultdict(list),
            'range': {},
            'realTime': True if coordinate.frequency == DataFrequency.REAL_TIME else False,
            'measures': set()
        })
        query_map = dataset_mappings[query_key]
        if not query_map['range']:
            if isinstance(query.start, date):
                query_map['range']['startDate'] = query.start
            elif isinstance(query.start, datetime):
                query_map['range']['startTime'] = query.start

            if isinstance(query.end, date):
                query_map['range']['endDate'] = query.end
            elif isinstance(query.end, datetime):
                query_map['range']['endTime'] = query.end

        queries = query_map['queries']
        queries[coordinate.get_dimensions()].append(query_info)
        parameters = query_map['parameters']
        query_map['measures'].add(coordinate.measure)
        for dimension, value in coordinate.dimensions.items():
            parameters.setdefault(dimension, set())
            parameters[dimension].add(value)

    return mappings


def fetch_query(query_info: Dict):
    where = {}
    for key, value in query_info['parameters'].items():
        value_list = list(value)
        if isinstance(value_list[0], bool):
            if len(value_list) == 1:
                # If only 1 bool value is given (True/False) set the where to the value. Else skip.
                where[key] = value_list[0]
            continue  # Skip adding as both True/False must be there
        where[key] = list(value)
    query = {
        'where': where,
        **query_info['range'],
        'useFieldAlias': True,
        'remapSchemaToAlias': True
    }
    try:
        if query_info['realTime'] and not query_info['range']:
            response = GsSession.current._post(f'/data/{query_info["datasetId"]}/last/query', payload=query)
        else:
            response = GsSession.current._post(f'/data/{query_info["datasetId"]}/query', payload=query)
    except Exception as e:
        _logger.error(f'Error fetching query due to {e}')
        return DataFrame()

    df = DataFrame(response.get('data', {}))
    if df.empty:
        return df
    df.set_index('date' if 'date' in df.columns else 'time', inplace=True)
    df.index = to_datetime(df.index).tz_localize(None)
    return df


def build_query_string(dimensions):
    output = ''
    for count, dimension in enumerate(dimensions):
        value = dimension[1]
        if isinstance(value, str):
            value = f'"{value}"'
        if count == 0:
            output += f'{dimension[0]} == {value}'
        else:
            output += f' & {dimension[0]} == {value}'
    return output


def valid_dimensions(query_dimensions: Tuple[str, Union[str, float, bool]], df: DataFrame) -> bool:
    columns = df.columns
    for query_dimension in query_dimensions:
        dimension = query_dimension[0]
        if dimension not in columns:
            return False
    return True
