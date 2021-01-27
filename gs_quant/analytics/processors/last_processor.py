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

import pandas as pd
from pandas import Series

from gs_quant.analytics.core.processor import BaseProcessor, DataCoordinateOrProcessor, DateOrDatetimeOrRDate
from gs_quant.analytics.core.processor_result import ProcessorResult


class LastProcessor(BaseProcessor):

    def __init__(self,
                 a: DataCoordinateOrProcessor,
                 start: Optional[DateOrDatetimeOrRDate] = None,
                 end: Optional[DateOrDatetimeOrRDate] = None):
        """ Last Processor returns the last value of the series a

        :param a: DataCoordinate or BaseProcessor for the first coordinate
        :param start: Start date or time used in the underlying data query
        :param end: Start date or time used in the underlying data query
        """
        super().__init__()
        # coordinates
        self.children['a'] = a

        # datetime
        self.start = start
        self.end = end

    def process(self) -> None:
        """ Calculate the result and store it as the processor value """
        a_data = self.children_data.get('a')
        if isinstance(a_data, ProcessorResult):
            if a_data.success and isinstance(a_data.data, Series):
                self.value = ProcessorResult(True, pd.Series(a_data.data[-1:]))

    def get_plot_expression(self):
        pass
