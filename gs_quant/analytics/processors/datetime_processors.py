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

from datetime import date, timedelta
from typing import Union

from gs_quant.analytics.core.processor import BaseProcessor, DataCoordinateOrProcessor, DateOrDatetimeOrRDate
from gs_quant.analytics.core.processor_result import ProcessorResult
from gs_quant.markets import PricingContext
from gs_quant.timeseries.datetime import date_range, RelativeDate


class DateRangeProcessor(BaseProcessor):
    def __init__(self,
                 a: DataCoordinateOrProcessor,
                 start: Union[DateOrDatetimeOrRDate, int] = None,
                 end: Union[DateOrDatetimeOrRDate, int] = None,
                 weekdays_only: bool = False):
        """ DateRangeProcessor

        :param a: DataCoordinate or BaseProcessor for the first series
        :param start: start date for the sliced time series. If integer, number of observations after the first
        :param end: end date for the sliced time series. If integer, number of observations before the last
        :param weekdays_only: whether to include only weekdays in the sliced ranges
        :return: sliced time series
        """
        super().__init__()
        self.children['a'] = a
        self.start = start
        self.end = end
        self.weekdays_only = weekdays_only

    def process(self):
        a_data = self.children_data.get('a')
        if isinstance(a_data, ProcessorResult):
            if a_data.success:
                date_array = a_data.data.reset_index()['date']
                if self.end is None:
                    self.end = max(date_array)
                if self.start is None:
                    self.start = min(date_array)
                if not isinstance(self.weekdays_only, bool):
                    self.value = ProcessorResult(False,
                                                 "DateRangeProcessor requires weekdays_only argument to be a boolean.")
                yesterday = date.today() - timedelta(days=1)
                with PricingContext(pricing_date=yesterday):
                    # for EOD datasets latest datapoint is T-1,
                    # relative dates will be evaluated using yesterday as base_date
                    if isinstance(self.end, RelativeDate):
                        self.end = self.end.apply_rule()
                    if isinstance(self.start, RelativeDate):
                        self.start = self.start.apply_rule()

                result = date_range(a_data.data, start_date=self.start, end_date=self.end,
                                    weekdays_only=self.weekdays_only)
                self.value = ProcessorResult(True, result)
            else:
                self.value = ProcessorResult(False, "DateRangeProcessor does not have 'a' series values yet")
        else:
            self.value = ProcessorResult(False, "DateRangeProcessor does not have 'a' series yet")

    def get_plot_expression(self):
        pass
