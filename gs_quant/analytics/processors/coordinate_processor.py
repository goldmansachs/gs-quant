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

from enum import Enum
from typing import Union

from gs_quant.analytics.core.processor import BaseProcessor
from gs_quant.analytics.core.processor_result import ProcessorResult
from gs_quant.data import DataDimension, DataCoordinate


class CoordinateProcessor(BaseProcessor):
    def __init__(self,
                 a: DataCoordinate,
                 dimension: Union[DataDimension, str]):
        """ Returns a field from a coordinate

        :param a: WIP
        """
        super().__init__()
        # coordinate
        self.children['a'] = a
        # parameters
        self.dimension = dimension

    def update(self, attribute: str, result: ProcessorResult):
        pass

    def process(self):
        key: str = self.dimension.value if isinstance(self.dimension, Enum) else self.dimension
        coordinate = self.children.get('a')
        dimension_value = coordinate.dimensions.get(key) if coordinate else None
        if dimension_value:
            return ProcessorResult(True, dimension_value)
        else:
            return ProcessorResult(False, f'Dimension {key} not in given coordinate')

    def get_plot_expression(self):
        pass
