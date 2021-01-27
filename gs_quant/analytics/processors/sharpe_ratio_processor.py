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

from gs_quant.analytics.core.processor import BaseProcessor, DataCoordinateOrProcessor, DataQueryInfo,\
    DateOrDatetimeOrRDate
from gs_quant.analytics.core.processor_result import ProcessorResult
from gs_quant.data import DataMeasure, DataFrequency
from gs_quant.data.coordinate import DataCoordinate
from gs_quant.data.query import DataQuery
from gs_quant.markets.securities import Stock
from gs_quant.target.common import Currency
from gs_quant.timeseries import Window, SeriesType, excess_returns_pure
from gs_quant.timeseries.econometrics import get_ratio_pure, SharpeAssets
from gs_quant.timeseries.helper import CurveType


class SharpeRatioProcessor(BaseProcessor):

    def __init__(self,
                 a: DataCoordinateOrProcessor,
                 currency: Currency,
                 w: Union[Window, int] = None,
                 curve_type: CurveType = CurveType.PRICES,
                 start: Optional[DateOrDatetimeOrRDate] = None,
                 end: Optional[DateOrDatetimeOrRDate] = None,
                 type_: SeriesType = SeriesType.PRICES):
        """ Change Processor

        :param a: WIP
        """
        super().__init__()
        # coordinates
        self.children['a'] = a
        # datetime
        self.start = start
        self.end = end
        # parameters
        self.currency = currency
        self.w = w
        self.curve_type = curve_type
        self.type_ = type_
        # additional queries
        self.children['excess_returns'] = self.get_excess_returns_query()

    def get_excess_returns_query(self) -> DataQueryInfo:
        marquee_id = SharpeAssets[self.currency.value].value
        entity = Stock(marquee_id, "", "")

        coordinate: DataCoordinate = DataCoordinate(
            measure=DataMeasure.CLOSE_PRICE,
            frequency=DataFrequency.DAILY
        )

        data_query: DataQuery = DataQuery(coordinate=coordinate, start=self.start, end=self.end)

        return DataQueryInfo('excess_returns', None, data_query, entity)

    def process(self,
                w: Union[Window, int] = Window(None, 0),
                type_: SeriesType = SeriesType.PRICES):
        a_data = self.children_data.get('a')
        excess_returns_data = self.children_data.get('excess_returns')
        if isinstance(a_data, ProcessorResult) and isinstance(excess_returns_data, ProcessorResult):
            if a_data.success and excess_returns_data.success:
                excess_returns = excess_returns_pure(a_data.data, excess_returns_data.data)
                ratio = get_ratio_pure(excess_returns, self.w)
                self.value = ProcessorResult(True, ratio)

    def get_plot_expression(self):
        pass
