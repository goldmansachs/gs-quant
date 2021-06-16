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

import pandas as pd

from gs_quant.analytics.core.processor import BaseProcessor, DataCoordinateOrProcessor, DateOrDatetimeOrRDate
from gs_quant.analytics.core.processor_result import ProcessorResult
from gs_quant.timeseries.statistics import percentiles, percentile, Window, mean, sum_, std, var, cov, zscores


class PercentilesProcessor(BaseProcessor):
    def __init__(self,
                 a: DataCoordinateOrProcessor,
                 *,
                 b: Optional[DataCoordinateOrProcessor] = None,
                 start: Optional[DateOrDatetimeOrRDate] = None,
                 end: Optional[DateOrDatetimeOrRDate] = None,
                 w: Union[Window, int] = Window(None, 0),
                 **kwargs):
        """ PercentilesProcessor

        :param a: DataCoordinate or BaseProcessor for the first series
        :param b: DataCoordinate or BaseProcessor for the second series
        :param start: start date or time used in the underlying data query
        :param end: end date or time used in the underlying data query
        :param w:  Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value.  If w is a string, it should be a relative date like '1m', '1d', etc.
              Window size defaults to length of series.
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
                        result = percentiles(a_data.data, b_data.data, w=self.w)
                        self.value = ProcessorResult(True, result)
                    else:
                        self.value = ProcessorResult(True, 'PercentilesProcessor: b is not a valid series.')
                result = percentiles(a_data.data, w=self.w)
                self.value = ProcessorResult(True, result)
            else:
                self.value = ProcessorResult(False, "PercentilesProcessor does not have 'a' series values yet")
        else:
            self.value = ProcessorResult(False, "PercentilesProcessor does not have 'a' series yet")

        return self.value

    def get_plot_expression(self):
        pass


class PercentileProcessor(BaseProcessor):
    def __init__(self,
                 a: DataCoordinateOrProcessor,
                 *,
                 n: float,
                 start: Optional[DateOrDatetimeOrRDate] = None,
                 end: Optional[DateOrDatetimeOrRDate] = None,
                 w: Union[Window, int] = None,
                 **kwargs):
        """ PercentileProcessor

        :param a: DataCoordinate or BaseProcessor for the series
        :param n: Percentile
        :param start: start date or time used in the underlying data query
        :param end: end date or time used in the underlying data query
        :param w:  Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value.  If w is a string, it should be a relative date like '1m', '1d', etc.
              Window size defaults to length of series.
        """
        super().__init__(**kwargs)
        self.children['a'] = a
        self.n = n
        self.start = start
        self.end = end
        self.w = w

    def process(self):
        a_data = self.children_data.get('a')
        if isinstance(a_data, ProcessorResult):
            if a_data.success:
                series_length = len(a_data.data)
                window = None
                if self.w:
                    window = self.w if self.w <= series_length else series_length
                result = percentile(a_data.data, self.n, w=window)
                if not isinstance(result, pd.Series):
                    result = pd.Series(result)
                self.value = ProcessorResult(True, result)
            else:
                self.value = ProcessorResult(False, "PercentileProcessor does not have 'a' series values yet")
        else:
            self.value = ProcessorResult(False, "PercentileProcessor does not have 'a' series yet")

        return self.value

    def get_plot_expression(self):
        pass


class MeanProcessor(BaseProcessor):
    def __init__(self,
                 a: DataCoordinateOrProcessor,
                 *,
                 start: Optional[DateOrDatetimeOrRDate] = None,
                 end: Optional[DateOrDatetimeOrRDate] = None,
                 w: Union[Window, int] = None,
                 **kwargs):
        """ MeanProcessor

        :param a: DataCoordinate or BaseProcessor for the series
        :param start: start date or time used in the underlying data query
        :param end: end date or time used in the underlying data query
        :param w:  Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value.  If w is a string, it should be a relative date like '1m', '1d', etc.
              Window size defaults to length of series.

         **Usage**

        Calculates `arithmetic mean <https://en.wikipedia.org/wiki/Arithmetic_mean>`_ of the series over a rolling
        window

        If window is not provided, computes rolling mean over the full series. If the window size is greater than the
        available data, will return mean of available values.

        """
        super().__init__(**kwargs)
        self.children['a'] = a
        self.start = start
        self.end = end
        self.w = w

    def process(self):
        a_data = self.children_data.get('a')
        if isinstance(a_data, ProcessorResult):
            if a_data.success:
                series_length = len(a_data.data)
                window = None
                if self.w:
                    window = self.w if self.w <= series_length else series_length
                result = mean(a_data.data, w=window)
                self.value = ProcessorResult(True, result)
            else:
                self.value = ProcessorResult(False, "MeanProcessor does not have 'a' series values yet")
        else:
            self.value = ProcessorResult(False, "MeanProcessor does not have 'a' series yet")

        return self.value

    def get_plot_expression(self):
        pass


class SumProcessor(BaseProcessor):
    def __init__(self,
                 a: DataCoordinateOrProcessor,
                 *,
                 start: Optional[DateOrDatetimeOrRDate] = None,
                 end: Optional[DateOrDatetimeOrRDate] = None,
                 w: Union[Window, int] = None,
                 **kwargs):
        """ SumProcessor

        :param a: DataCoordinate or BaseProcessor for the series
        :param start: start date or time used in the underlying data query
        :param end: end date or time used in the underlying data query
        :param w:  Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value.  If w is a string, it should be a relative date like '1m', '1d', etc.
              Window size defaults to length of series.

        **Usage**

        Calculate the sum of observations over a given rolling window.

        If window is not provided, computes sum over the full series. If the window size is greater than the available
        data, will return sum of available values.

        """

        super().__init__(**kwargs)
        self.children['a'] = a
        self.start = start
        self.end = end
        self.w = w

    def process(self):
        a_data = self.children_data.get('a')
        if isinstance(a_data, ProcessorResult):
            if a_data.success:
                series_length = len(a_data.data)
                window = None
                if self.w:
                    window = self.w if self.w <= series_length else series_length
                result = sum_(a_data.data, w=window)
                self.value = ProcessorResult(True, result)
            else:
                self.value = ProcessorResult(False, "SumProcessor does not have 'a' series values yet")
        else:
            self.value = ProcessorResult(False, "SumProcessor does not have 'a' series yet")

        return self.value

    def get_plot_expression(self):
        pass


class StdDevProcessor(BaseProcessor):
    def __init__(self,
                 a: DataCoordinateOrProcessor,
                 *,
                 start: Optional[DateOrDatetimeOrRDate] = None,
                 end: Optional[DateOrDatetimeOrRDate] = None,
                 w: Union[Window, int] = Window(None, 0),
                 **kwargs):
        """ StdDevProcessor

        :param a: DataCoordinate or BaseProcessor for the first series
        :param start: start date or time used in the underlying data query
        :param end: end date or time used in the underlying data query
        :param w:  Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value.  If w is a string, it should be a relative date like '1m', '1d', etc.
              Window size defaults to length of series.

          **Usage**

        Provides `unbiased estimator <https://en.wikipedia.org/wiki/Unbiased_estimation_of_standard_deviation>`_ of
        sample standard deviation <https://en.wikipedia.org/wiki/Standard_deviation>`_ over a rolling window

        If window is not provided, computes standard deviation over the full series
        """
        super().__init__(**kwargs)
        self.children['a'] = a

        self.start = start
        self.end = end
        self.w = w

    def process(self):
        a_data = self.children_data.get('a')
        if isinstance(a_data, ProcessorResult):
            if a_data.success:
                series_length = len(a_data.data)
                window = None
                if self.w:
                    window = self.w if self.w <= series_length else series_length
                result = std(a_data.data, w=window)
                self.value = ProcessorResult(True, result)
            else:
                self.value = ProcessorResult(False, "StdDevProcessor does not have 'a' series values yet")
        else:
            self.value = ProcessorResult(False, "StdDevProcessor does not have 'a' series yet")

        return self.value

    def get_plot_expression(self):
        pass


class VarianceProcessor(BaseProcessor):
    def __init__(self,
                 a: DataCoordinateOrProcessor,
                 *,
                 start: Optional[DateOrDatetimeOrRDate] = None,
                 end: Optional[DateOrDatetimeOrRDate] = None,
                 w: Union[Window, int] = Window(None, 0),
                 **kwargs):
        """ VarianceProcessor

        :param a: DataCoordinate or BaseProcessor for the first series
        :param start: start date or time used in the underlying data query
        :param end: end date or time used in the underlying data query
        :param w:  Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value.  If w is a string, it should be a relative date like '1m', '1d', etc.
              Window size defaults to length of series.

          **Usage**

        Provides `unbiased estimator <https://en.wikipedia.org/wiki/Unbiased_estimation_of_standard_deviation>`_ of
        sample variance <https://en.wikipedia.org/wiki/Variance>`_ over a rolling window
        If window is not provided, computes variance over the full series
        """
        super().__init__(**kwargs)
        self.children['a'] = a

        self.start = start
        self.end = end
        self.w = w

    def process(self):
        a_data = self.children_data.get('a')
        if isinstance(a_data, ProcessorResult):
            if a_data.success:
                series_length = len(a_data.data)
                window = None
                if self.w:
                    window = self.w if self.w <= series_length else series_length
                result = var(a_data.data, w=window)
                self.value = ProcessorResult(True, result)
            else:
                self.value = ProcessorResult(False, "VarianceProcessor does not have 'a' series values yet")
        else:
            self.value = ProcessorResult(False, "VarianceProcessor does not have 'a' series yet")

        return self.value

    def get_plot_expression(self):
        pass


class CovarianceProcessor(BaseProcessor):
    def __init__(self,
                 a: DataCoordinateOrProcessor,
                 b: DataCoordinateOrProcessor,
                 *,
                 start: Optional[DateOrDatetimeOrRDate] = None,
                 end: Optional[DateOrDatetimeOrRDate] = None,
                 w: Union[Window, int] = Window(None, 0),
                 **kwargs):
        """ CovarianceProcessor

        :param a: DataCoordinate or BaseProcessor for the first series
        :param b: DataCoordinate or BaseProcessor for the second series
        :param start: start date or time used in the underlying data query
        :param end: end date or time used in the underlying data query
        :param w:  Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value.  If w is a string, it should be a relative date like '1m', '1d', etc.
              Window size defaults to length of series.
        **Usage**

        Provides `unbiased estimator <https://en.wikipedia.org/wiki/Unbiased_estimation_of_standard_deviation>`_ of
        sample co-variance <https://en.wikipedia.org/wiki/Covariance>`_ over a rolling window:

        If window is not provided, computes variance over the full series
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
                        result = cov(a_data.data, b_data.data, w=self.w)
                        self.value = ProcessorResult(True, result)
                    else:
                        self.value = ProcessorResult(True, "CovarianceProcessor does not 'b' series values yet.")
                else:
                    self.value = ProcessorResult(True, 'CovarianceProcessor: b is not a valid series.')
            else:
                self.value = ProcessorResult(False, "CovarianceProcessor does not have 'a' series values yet")
        else:
            self.value = ProcessorResult(False, "CovarianceProcessor does not have 'a' series yet")

        return self.value

    def get_plot_expression(self):
        pass


class ZscoresProcessor(BaseProcessor):
    def __init__(self,
                 a: DataCoordinateOrProcessor,
                 *,
                 start: Optional[DateOrDatetimeOrRDate] = None,
                 end: Optional[DateOrDatetimeOrRDate] = None,
                 w: Union[Window, int] = None,
                 **kwargs):
        """ ZscoresProcessor

        :param a: DataCoordinate or BaseProcessor for the series
        :param start: start date or time used in the underlying data query
        :param end: end date or time used in the underlying data query
        :param w:  Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value.  If w is a string, it should be a relative date like '1m', '1d', etc.
              Window size defaults to length of series.

        **Usage**

        Calculate `standard score <https://en.wikipedia.org/wiki/Standard_score>`_ of each value in series over given
        window. Standard deviation and sample mean are computed over the specified rolling window, then element is
        normalized to provide a rolling z-score

        If window is not provided, computes z-score relative to mean and standard deviation over the full series


        """

        super().__init__(**kwargs)
        self.children['a'] = a
        self.start = start
        self.end = end
        self.w = w

    def process(self):
        a_data = self.children_data.get('a')
        if isinstance(a_data, ProcessorResult):
            if a_data.success:
                result = zscores(a_data.data, w=Window(None, 0) if self.w is None else self.w)
                self.value = ProcessorResult(True, result)
            else:
                self.value = ProcessorResult(False, "ZscoresProcessor does not have 'a' series values yet")
        else:
            self.value = ProcessorResult(False, "ZscoresProcessor does not have 'a' series yet")

        return self.value

    def get_plot_expression(self):
        pass
