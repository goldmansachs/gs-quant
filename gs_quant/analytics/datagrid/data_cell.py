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

import copy
from datetime import datetime
from typing import List, Optional

from pandas import Series

from gs_quant.analytics.common import DATA_CELL_NOT_CALCULATED
from gs_quant.analytics.core import BaseProcessor
from gs_quant.analytics.core.processor import DataQueryInfo
from gs_quant.analytics.core.processor_result import ProcessorResult
from gs_quant.analytics.datagrid import Override
from gs_quant.entities.entity import Entity


class DataCell:
    """ Entity data cell

        Computes value and manages formatting of a data cell
    """

    def __init__(self,
                 name: str,
                 processor: BaseProcessor,
                 entity: Entity,
                 dimension_overrides: List[Override],
                 column_index: int,
                 row_index: int):
        # Cell starts with root processor
        # Deep copies so the processor and children are unique objects
        self.processor: BaseProcessor = copy.deepcopy(processor)
        self.entity: Entity = entity
        self.name: str = name
        self.dimension_overrides = dimension_overrides
        self.column_index = column_index
        self.row_index = row_index

        self.updated_time: Optional[str] = None

        # Default the value for a cell processor
        self.value: ProcessorResult = ProcessorResult(False, DATA_CELL_NOT_CALCULATED)

        # Store the cell data queries
        self.data_queries: List[DataQueryInfo] = []

    def build_cell_graph(self, all_queries: List[DataQueryInfo]) -> None:
        """ Generate and store the cell graph and data queries

            This can be modified to return the data queries rather than store on the cell
        """
        # Set the root processor node parent to data cell
        self.processor.parent = self
        cell_queries: List[DataQueryInfo] = []
        self.processor.build_graph(self.entity,
                                   self,
                                   cell_queries,
                                   self.dimension_overrides)

        self.data_queries = cell_queries
        all_queries.extend(cell_queries)  # Add this cell's queries to the entire datagrid's list of queries

    def update(self, result: ProcessorResult) -> None:
        """ Sets the value of the cell"""
        value = result.data.iloc[-1] if isinstance(result.data, Series) else result.data
        self.value = ProcessorResult(True, value)
        self.updated_time = f'{datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]}Z'
