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

from typing import Optional, Union

from gs_quant.analytics.core.processor import BaseProcessor, DataCoordinateOrProcessor, DateOrDatetimeOrRDate
from gs_quant.analytics.core.processor_result import ProcessorResult
from gs_quant.timeseries.econometrics import volatility, Returns, Window


class VolatilityProcessor(BaseProcessor):

    def __init__(self,
                 a: DataCoordinateOrProcessor,
                 w: Union[Window, int] = Window(None, 0),
                 returns_type: Returns = Returns.SIMPLE,
                 start: Optional[DateOrDatetimeOrRDate] = None,
                 end: Optional[DateOrDatetimeOrRDate] = None):
        """ Change Processor

        :param a: DataCoordinateOrProcessor to apply volatility timeseries function
        """
        super().__init__()
        # coordinate
        self.children['a'] = a

        # datetime
        self.start = start
        self.end = end

        # parameters
        self.w = w
        self.returns_type = returns_type

    def process(self):
        a_data = self.children_data.get('a')
        if isinstance(a_data, ProcessorResult):
            if a_data.success:
                result = volatility(a_data.data, self.w, self.returns_type)
                self.value = ProcessorResult(True, result)
            else:
                self.value = ProcessorResult(False, 'Could not compute volatility')
        else:
            self.value = ProcessorResult(False, 'Processor does not have data')

    def get_plot_expression(self):
        pass
