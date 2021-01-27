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
from gs_quant.timeseries import change


class ChangeProcessor(BaseProcessor):

    def __init__(self,
                 a: DataCoordinateOrProcessor,
                 start: Optional[DateOrDatetimeOrRDate] = None,
                 end: Optional[DateOrDatetimeOrRDate] = None):
        """ Change Processor

        :param a: WIP
        """
        super().__init__()
        # coordinate
        self.children['a'] = a

        # datetime
        self.start = start
        self.end = end

    def process(self) -> None:
        a_data = self.children_data.get('a')
        if isinstance(a_data, ProcessorResult):
            if a_data.success:
                value = change(a_data.data)
                self.value = ProcessorResult(True, value)

    def get_plot_expression(self):
        pass
