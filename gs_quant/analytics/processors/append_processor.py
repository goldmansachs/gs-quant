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

from typing import Optional

from gs_quant.analytics.core.processor import BaseProcessor, DataCoordinateOrProcessor, DateOrDatetimeOrRDate
from gs_quant.analytics.core.processor_result import ProcessorResult


class AppendProcessor(BaseProcessor):
    def __init__(self,
                 a: DataCoordinateOrProcessor,
                 b: DataCoordinateOrProcessor,
                 start: Optional[DateOrDatetimeOrRDate] = None,
                 end: Optional[DateOrDatetimeOrRDate] = None):
        """ Append Processor appends both a and b data series into one list

        :param a: DataCoordinate or BaseProcessor for the first coordinate
        :param b: DataCoordinate or BaseProcessor for the second coordinate
        :param start: Start date or time used in the underlying data query
        :param end: Start date or time used in the underlying data query
        """
        super().__init__()
        # coordinates
        self.children['a'] = a
        self.children['b'] = b

        # datetime
        self.start = start
        self.end = end

    def process(self) -> None:
        a_data = self.children_data.get('a')
        b_data = self.children_data.get('b')
        if isinstance(a_data, ProcessorResult) and isinstance(b_data, ProcessorResult):
            if a_data.success and b_data.success:
                result = a_data.data.append(b_data.data)
                self.value = ProcessorResult(True, result)
            else:
                self.value = ProcessorResult(False, "Processor does not have A and B data yet")
        else:
            self.value = ProcessorResult(False, "Processor does not have A and B data yet")

    def get_plot_expression(self):
        pass
