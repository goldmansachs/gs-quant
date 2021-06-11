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
from gs_quant.timeseries import diff


class DiffProcessor(BaseProcessor):
    def __init__(self,
                 a: DataCoordinateOrProcessor,
                 *,
                 obs: int = 1,
                 start: Optional[DateOrDatetimeOrRDate] = None,
                 end: Optional[DateOrDatetimeOrRDate] = None,
                 **kwargs):
        """ DiffProcessor

        :param a: DataCoordinate or BaseProcessor for the series
        :param obs: number of observations to lag
        :param start: start date or time used in the underlying data query
        :param end: end date or time used in the underlying data query
       **Usage**

        Compute the difference in series values over a given lag:

        :math:`R_t = X_t - X_{t-obs}`

        where :math:`obs` is the number of observations to lag series in diff function

        """
        super().__init__(**kwargs)
        self.children['a'] = a
        self.obs = obs
        self.start = start
        self.end = end

    def process(self):
        a_data = self.children_data.get('a')
        if isinstance(a_data, ProcessorResult):
            if a_data.success:
                result = diff(a_data.data, self.obs)
                self.value = ProcessorResult(True, result)
            else:
                self.value = ProcessorResult(False, "DiffProcessor does not have 'a' series values yet")
        else:
            self.value = ProcessorResult(False, "DiffProcessor does not have 'a' series yet")

        return self.value

    def get_plot_expression(self):
        pass
