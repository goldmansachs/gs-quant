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

from collections import defaultdict
from datetime import date, datetime
from typing import Dict

from pandas import DataFrame, to_datetime

from gs_quant.analytics.core.processor_result import ProcessorResult
from gs_quant.data import DataFrequency
from gs_quant.session import GsSession


def aggregate_queries(query_infos):
    mappings = defaultdict(dict)  # DataSet -> start/end
    for query_info in query_infos:
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
            query_info.processor.calculate(query_info.attr, series)
            continue
        dataset_mappings.setdefault(query_key, {
            'datasetId': dataset_id,
            'parameters': {},
            'queries': defaultdict(list),
            'range': {},
            'realTime': True if coordinate.frequency == DataFrequency.REAL_TIME else False
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
        for dimension, value in coordinate.dimensions.items():
            parameters.setdefault(dimension, set())
            parameters[dimension].add(value)

    return mappings


def fetch_query(query_info: Dict):
    where = {}
    for key, value in query_info['parameters'].items():
        where[key] = list(value)
    query = {
        'where': where,
        **query_info['range']
    }

    if query_info['realTime'] and not query_info['range']:
        response = GsSession.current._post(f'/data/{query_info["datasetId"]}/last/query', payload=query)
    else:
        response = GsSession.current._post(f'/data/{query_info["datasetId"]}/query', payload=query)

    df = DataFrame(response.get('data', {}))
    df.set_index('date' if 'date' in df.columns else 'time', inplace=True)
    df.index = to_datetime(df.index)

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
