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


class AdditionProcessor(BaseProcessor):
    """ Add scalar or series together """

    def __init__(self,
                 a: DataCoordinateOrProcessor,
                 b: Optional[DataCoordinateOrProcessor] = None,
                 start: Optional[DateOrDatetimeOrRDate] = None,
                 end: Optional[DateOrDatetimeOrRDate] = None,
                 addend: Optional[float] = None):
        super().__init__()
        # coordinates
        self.children['a'] = a
        self.children['b'] = b
        # datetime
        self.start = start
        self.end = end

        self.addend = addend

    def process(self):
        a_data = self.children_data.get('a')
        if isinstance(a_data, ProcessorResult):
            if not a_data.success:
                self.value = a_data
                return
            if self.addend:
                value = a_data.data.add(self.addend)
                self.value = ProcessorResult(True, value)
                return
            b_data = self.children_data.get('b')
            if isinstance(b_data, ProcessorResult):
                if b_data.success:
                    value = a_data.data.add(b_data.data)
                    self.value = ProcessorResult(True, value)
                else:
                    self.value = ProcessorResult(True, b_data.data)

    def get_plot_expression(self):
        pass


class SubtractionProcessor(BaseProcessor):
    """ Subtract scalar or series together """

    def __init__(self,
                 a: DataCoordinateOrProcessor,
                 b: Optional[DataCoordinateOrProcessor] = None,
                 start: Optional[DateOrDatetimeOrRDate] = None,
                 end: Optional[DateOrDatetimeOrRDate] = None,
                 subtrahend: Optional[float] = None):
        super().__init__()
        # coordinates
        self.children['a'] = a
        self.children['b'] = b
        # datetime
        self.start = start
        self.end = end

        self.subtrahend = subtrahend

    def process(self):
        a_data = self.children_data.get('a')
        if isinstance(a_data, ProcessorResult):
            if not a_data.success:
                self.value = a_data
                return
            if self.subtrahend:
                value = a_data.data.sub(self.subtrahend)
                self.value = ProcessorResult(True, value)
                return
            b_data = self.children_data.get('b')
            if isinstance(b_data, ProcessorResult):
                if b_data.success:
                    value = a_data.data.sub(b_data.data)
                    self.value = ProcessorResult(True, value)
                else:
                    self.value = b_data

    def get_plot_expression(self):
        pass


class MultiplicationProcessor(BaseProcessor):
    """ Multiply scalar or series together """

    def __init__(self,
                 a: DataCoordinateOrProcessor,
                 b: Optional[DataCoordinateOrProcessor] = None,
                 start: Optional[DateOrDatetimeOrRDate] = None,
                 end: Optional[DateOrDatetimeOrRDate] = None,
                 factor: Optional[float] = None):
        super().__init__()
        # coordinates
        self.children['a'] = a
        self.children['b'] = b
        # datetime
        self.start = start
        self.end = end

        self.factor = factor

    def process(self):
        a_data = self.children_data.get('a')
        if isinstance(a_data, ProcessorResult):
            if not a_data.success:
                self.value = a_data
                return
            if self.factor:
                value = a_data.data.mul(self.factor)
                self.value = ProcessorResult(True, value)
                return
            b_data = self.children_data.get('b')
            if isinstance(b_data, ProcessorResult):
                if b_data.success:
                    value = a_data.data.mul(b_data.data)
                    self.value = ProcessorResult(True, value)
                else:
                    self.value = b_data

    def get_plot_expression(self):
        pass


class DivisionProcessor(BaseProcessor):
    """ Divide scalar or series together """

    def __init__(self,
                 a: DataCoordinateOrProcessor,
                 b: Optional[DataCoordinateOrProcessor] = None,
                 start: Optional[DateOrDatetimeOrRDate] = None,
                 end: Optional[DateOrDatetimeOrRDate] = None,
                 dividend: Optional[float] = None):
        super().__init__()
        # coordinates
        self.children['a'] = a
        self.children['b'] = b
        # datetime
        self.start = start
        self.end = end

        self.dividend = dividend

    def process(self):
        a_data = self.children_data.get('a')
        if isinstance(a_data, ProcessorResult):
            if not a_data.success:
                self.value = a_data
                return
            if self.dividend:
                value = a_data.data.div(self.dividend)
                self.value = ProcessorResult(True, value)
                return
            b_data = self.children_data.get('b')
            if isinstance(b_data, ProcessorResult):
                if b_data.success:
                    value = a_data.data.div(b_data.data)
                    self.value = ProcessorResult(True, value)
                else:
                    self.value = b_data

    def get_plot_expression(self):
        pass
