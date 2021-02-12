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
from dataclasses import dataclass, asdict, fields
from typing import Dict, List

from gs_quant.analytics.core.processor import BaseProcessor

DEFAULT_WIDTH = 100


class RenderType:
    DEFAULT = 'default'
    HEATMAP = 'heatmap'


@dataclass
class ColumnFormat:
    renderType: RenderType = RenderType.DEFAULT
    precision: int = 2
    humanReadable: bool = True
    tooltip: str = None

    @classmethod
    def from_dict(cls, dict_):
        class_fields = {f.name for f in fields(cls)}
        return ColumnFormat(**{k: v for k, v in dict_.items() if k in class_fields})


class DataColumn:
    """Base class for grid column"""

    def __init__(self,
                 name: str,
                 processor: BaseProcessor,
                 *,
                 format_: ColumnFormat = ColumnFormat(),
                 width: int = DEFAULT_WIDTH):
        """ DataColumn

        :param name: Name of the column
        :param processor: Processor to apply to the column for calculation
        :param format_: Formatting information for the column result
        :param width: Size of the column in pixels when presented on the UI
        """
        self.name = name
        self.processor = processor
        self.format_ = format_
        self.width = width

    def as_dict(self):
        format_ = asdict(self.format_)
        if format_['tooltip'] is None:
            del format_['tooltip']

        return {
            'name': self.name,
            'processorName': self.processor.__class__.__name__,
            **self.processor.as_dict(),
            'format': format_,
            'width': self.width
        }

    @classmethod
    def from_dict(cls, obj: Dict, reference_list: List):
        processor = BaseProcessor.from_dict(obj, reference_list)

        return DataColumn(name=obj['name'],
                          processor=processor,
                          format_=ColumnFormat.from_dict(obj.get('format', {})),
                          width=obj.get('width', DEFAULT_WIDTH))
