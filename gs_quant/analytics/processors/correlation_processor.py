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

from gs_quant.analytics.core.processor import BaseProcessor, DataCoordinateOrProcessor, DataQueryInfo, \
    DateOrDatetimeOrRDate
from gs_quant.analytics.core.processor_result import ProcessorResult
from gs_quant.data.coordinate import DataCoordinate
from gs_quant.data.query import DataQuery
from gs_quant.entities.entity import Entity
from gs_quant.timeseries import correlation, Window, SeriesType, DataMeasure, DataFrequency


class CorrelationProcessor(BaseProcessor):

    def __init__(self,
                 a: DataCoordinateOrProcessor,
                 benchmark: Entity,
                 start: Optional[DateOrDatetimeOrRDate] = None,
                 end: Optional[DateOrDatetimeOrRDate] = None,
                 w: Union[Window, int] = Window(None, 0),
                 type_: SeriesType = SeriesType.PRICES):
        """ Correlation Processor

        :param a: Coordinate
        :param benchmark: Benchmark Entity to correlate coordinate data to
        """
        super().__init__()
        # coordinate
        self.children['a'] = a

        # Used for additional query
        self.benchmark: Entity = benchmark

        # datetime
        self.start = start
        self.end = end

        self.children['benchmark'] = self.get_benchmark_coordinate()

        # parameters
        self.w = w
        self.type_ = type_

    def get_benchmark_coordinate(self) -> DataQueryInfo:
        coordinate = DataCoordinate(measure=DataMeasure.CLOSE_PRICE, frequency=DataFrequency.DAILY)
        data_query = DataQuery(coordinate=coordinate, start=self.start, end=self.end)
        return DataQueryInfo('benchmark', None, data_query, self.benchmark)

    def process(self,
                w: Union[Window, int] = Window(None, 0),
                type_: SeriesType = SeriesType.PRICES):
        a_data = self.children_data.get('a')
        benchmark_data = self.children_data.get('benchmark')
        if isinstance(a_data, ProcessorResult) and isinstance(benchmark_data, ProcessorResult):
            if a_data.success and benchmark_data.success:
                result = correlation(a_data.data, benchmark_data.data, w=self.w, type_=SeriesType.PRICES)
                self.value = ProcessorResult(True, result)
            else:
                self.value = ProcessorResult(False, "Processor does not have A and Benchmark data yet")
        else:
            self.value = ProcessorResult(False, "Processor does not have A and Benchmark data yet")

    def get_plot_expression(self):
        pass
