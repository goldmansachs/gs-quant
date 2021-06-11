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

from pandas import Series

from gs_quant.analytics.core.processor import BaseProcessor, DataCoordinateOrProcessor, DataQueryInfo, \
    DateOrDatetimeOrRDate
from gs_quant.analytics.core.processor_result import ProcessorResult
from gs_quant.data.coordinate import DataCoordinate
from gs_quant.data.query import DataQuery
from gs_quant.entities.entity import Entity
from gs_quant.markets.securities import Stock
from gs_quant.target.common import Currency
from gs_quant.timeseries import correlation, Window, SeriesType, DataMeasure, DataFrequency
from gs_quant.timeseries import excess_returns_pure
from gs_quant.timeseries.econometrics import get_ratio_pure, SharpeAssets, change, returns
from gs_quant.timeseries.econometrics import volatility, Returns, beta
from gs_quant.timeseries.helper import CurveType


class VolatilityProcessor(BaseProcessor):

    def __init__(self,
                 a: DataCoordinateOrProcessor,
                 *,
                 start: Optional[DateOrDatetimeOrRDate] = None,
                 end: Optional[DateOrDatetimeOrRDate] = None,
                 w: Union[Window, int] = Window(None, 0),
                 returns_type: Returns = Returns.SIMPLE,
                 **kwargs):
        """ VolatilityProcessor

        :param a: DataCoordinate or BaseProcessor for the series to apply the volatility timeseries function
        :param start: start date or time used in the underlying data query
        :param end: end date or time used in the underlying data query
        :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value.  If w is a string, it should be a relative date like '1m', '1d', etc.
              Window size defaults to length of series.
        :param returns_type: returns type: simple, logarithmic or absolute
        """
        super().__init__(**kwargs)
        # coordinate
        self.children['a'] = a

        self.start = start
        self.end = end

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

        return self.value

    def get_plot_expression(self):
        pass


class SharpeRatioProcessor(BaseProcessor):

    def __init__(self,
                 a: DataCoordinateOrProcessor,
                 *,
                 start: Optional[DateOrDatetimeOrRDate] = None,
                 end: Optional[DateOrDatetimeOrRDate] = None,
                 currency: Currency,
                 w: Union[Window, int] = None,
                 curve_type: CurveType = CurveType.PRICES,
                 **kwargs):
        """ SharpeRatioProcessor

        :param a: DataCoordinate or BaseProcessor for the series of prices or excess returns
        :param currency: currency for risk-free rate, defaults to USD
        :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
                and 10 the ramp up value.
        :param curve_type: whether input series is of prices or excess returns, defaults to prices
        :param start: start date or time used in the underlying data query
        :param end: end date or time used in the underlying data query
        """
        super().__init__(**kwargs)
        # coordinates
        self.children['a'] = a
        # datetime
        self.start = start
        self.end = end
        # parameters
        self.currency = currency
        self.w = w
        self.curve_type = curve_type
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

    def process(self):
        a_data = self.children_data.get('a')
        excess_returns_data = self.children_data.get('excess_returns')
        if isinstance(a_data, ProcessorResult) and isinstance(excess_returns_data, ProcessorResult):
            if a_data.success and excess_returns_data.success:
                if self.curve_type == CurveType.PRICES:
                    excess_returns = excess_returns_pure(a_data.data, excess_returns_data.data)
                else:
                    excess_returns = a_data.data
                ratio = get_ratio_pure(excess_returns, self.w)
                self.value = ProcessorResult(True, ratio)

        return self.value

    def get_plot_expression(self):
        pass


class CorrelationProcessor(BaseProcessor):

    def __init__(self,
                 a: DataCoordinateOrProcessor,
                 *,
                 benchmark: Entity,
                 start: Optional[DateOrDatetimeOrRDate] = None,
                 end: Optional[DateOrDatetimeOrRDate] = None,
                 w: Union[Window, int] = Window(None, 0),
                 type_: SeriesType = SeriesType.PRICES,
                 **kwargs):
        """ CorrelationProcessor

        :param a: DataCoordinate or BaseProcessor for the series
        :param benchmark: benchmark to compare price series
        :param start: start date or time used in the underlying data query
        :param end: end date or time used in the underlying data query
        :param w: Window, int, or str: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window
                size and 10 the ramp up value. If w is a string, it should be a relative date like '1m', '1d', etc.
                Window size defaults to length of series.
        :param type_: type of both input series: prices or returns
        """
        super().__init__(**kwargs)
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

    def process(self):
        a_data = self.children_data.get('a')
        benchmark_data = self.children_data.get('benchmark')
        if isinstance(a_data, ProcessorResult) and isinstance(benchmark_data, ProcessorResult):
            if a_data.success and benchmark_data.success:
                result = correlation(a_data.data, benchmark_data.data, w=self.w, type_=self.type_)
                self.value = ProcessorResult(True, result)
            else:
                self.value = ProcessorResult(False, "Processor does not have A and Benchmark data yet")
        else:
            self.value = ProcessorResult(False, "Processor does not have A and Benchmark data yet")

        return self.value

    def get_plot_expression(self):
        pass


class ChangeProcessor(BaseProcessor):

    def __init__(self,
                 a: DataCoordinateOrProcessor,
                 *,
                 start: Optional[DateOrDatetimeOrRDate] = None,
                 end: Optional[DateOrDatetimeOrRDate] = None,
                 **kwargs):

        """ ChangeProcessor computes the change of a series

        :param a: DataCoordinate or BaseProcessor for the series
        :param start: start date or time used in the underlying data query
        :param end: end date or time used in the underlying data query
        """
        super().__init__(**kwargs)
        # coordinate
        self.children['a'] = a

        # datetime
        self.start = start
        self.end = end

    def process(self):
        a_data = self.children_data.get('a')
        if isinstance(a_data, ProcessorResult):
            if a_data.success:
                value = change(a_data.data)
                self.value = ProcessorResult(True, value)

        return self.value

    def get_plot_expression(self):
        pass


class ReturnsProcessor(BaseProcessor):

    def __init__(self,
                 a: DataCoordinateOrProcessor,
                 *,
                 start: Optional[DateOrDatetimeOrRDate] = None,
                 end: Optional[DateOrDatetimeOrRDate] = None,
                 observations: Optional[int] = None,
                 type_: Returns = Returns.SIMPLE,
                 **kwargs):

        """ ReturnsProcessor computes the returns of a series

        :param a: DataCoordinate or BaseProcessor for the series
        :param start: start date or time used in the underlying data query
        :param end: end date or time used in the underlying data query
        :param observations: number of observations, defaults to the return of the entire series as a single value
        :param type_: simple, logarithmic or absolute
        """
        super().__init__(**kwargs)
        # coordinate
        self.children['a'] = a

        # datetime
        self.start = start
        self.end = end

        self.observations = observations
        self.type_ = type_

    def process(self):
        a_data = self.children_data.get('a')
        if isinstance(a_data, ProcessorResult):
            if a_data.success:
                data = a_data.data
                if self.observations is None:
                    if len(data) > 1:
                        self.value = ProcessorResult(True, Series([(data.iloc[-1] - data.iloc[0]) / data.iloc[-1]]))
                    else:
                        self.value = ProcessorResult(True, 'Series has is less than 2.')
                else:
                    value = returns(a_data.data, self.observations, self.type_)
                    self.value = ProcessorResult(True, value)

        return self.value

    def get_plot_expression(self):
        pass


class BetaProcessor(BaseProcessor):
    def __init__(self,
                 a: DataCoordinateOrProcessor,
                 b: DataCoordinateOrProcessor,
                 *,
                 start: Optional[DateOrDatetimeOrRDate] = None,
                 end: Optional[DateOrDatetimeOrRDate] = None,
                 w: Union[Window, int] = Window(None, 0),
                 **kwargs):
        """ BetaProcessor

        :param a: DataCoordinate or BaseProcessor for the first series
        :param b: DataCoordinate or BaseProcessor for the second series
        :param start: start date or time used in the underlying data query
        :param end: end date or time used in the underlying data query
        :param w:  Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value.  If w is a string, it should be a relative date like '1m', '1d', etc.
              Window size defaults to length of series.

         **Usage**

        Calculate rolling `beta <https://en.wikipedia.org/wiki/Beta_(finance)>`_
        If window is not provided, computes beta over the full series

        """
        super().__init__(**kwargs)
        self.children['a'] = a
        self.children['b'] = b

        self.start = start
        self.end = end
        self.w = w

    def process(self):
        a_data = self.children_data.get('a')
        if isinstance(a_data, ProcessorResult):
            if a_data.success:
                b_data = self.children_data.get('b')
                # Need to check if the child node b was set in the first place.
                if self.children.get('b') and isinstance(b_data, ProcessorResult):
                    if b_data.success:
                        result = beta(a_data.data, b_data.data, w=self.w)
                        self.value = ProcessorResult(True, result)
                    else:
                        self.value = ProcessorResult(True, "BetaProcessor does not have 'b' series values yet.")
                else:
                    self.value = ProcessorResult(True, 'BetaProcessor: b is not a valid series.')
            else:
                self.value = ProcessorResult(False, "BetaProcessor does not have 'a' series values yet")
        else:
            self.value = ProcessorResult(False, "BetaProcessor does not have 'a' series yet")

        return self.value

    def get_plot_expression(self):
        pass
