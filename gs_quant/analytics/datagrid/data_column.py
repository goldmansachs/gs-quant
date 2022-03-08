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
from dataclasses import dataclass, asdict, fields, field
from typing import Dict, List, Union
from gs_quant.analytics.core.processor import BaseProcessor

DEFAULT_WIDTH = 100


class RenderType:
    DEFAULT = 'default'
    HEATMAP = 'heatmap'
    BOXPLOT = 'boxplot'
    SCALE = 'scale'
    DATE_MMM_YY = 'dateMmmYy'
    TIME_HH_MM = 'timeHhMm'


@dataclass
class HeatMapColorRange:
    """
    Dataclass for HeatMap color ranges. All values must be in hex format. Example: '#ffffff' for white.
    """
    low: str
    mid: str
    high: str

    @classmethod
    def from_dict(cls, dict_: dict):
        class_fields = {f.name for f in fields(cls)}
        return HeatMapColorRange(**{k: v for k, v in dict_.items() if k in class_fields})


@dataclass
class MultiColumnGroup:
    """
    MultiColumnGroup allows you to group DataGrid columns by index. Useful when working with
    heatmap renderers.

    :param id (Union[int, str]): Integer or string to identify the group. Defaults to 0.
    :param columnIndices (List[int]): Optional List of integers specifying the column indices to group
    :param groupAll (List[int]): Optional flag that allows you to easily group all columns so you don't have to
    pass every column index to the columnIndices list.
    :param heatMapColorRange (HeatMapColorRange): Optional HeatMapColorRange which allows you to specify a color theme
    for your grouped heatmap columns
    """
    id: Union[int, str] = 0
    columnIndices: List[int] = field(default_factory=list)
    groupAll: bool = False
    heatMapColorRange: HeatMapColorRange = None

    def asdict(self):
        obj = {
            'id': self.id,
            'columnIndices': self.columnIndices
        }
        if self.groupAll:
            obj['groupAll'] = True
        if self.heatMapColorRange:
            obj['heatMapColorRange'] = asdict(self.heatMapColorRange)

        return obj

    @classmethod
    def from_dict(cls, dict_: dict):
        heat_map_color_range = dict_.get('heatMapColorRange')
        return MultiColumnGroup(
            id=dict_.get('id'),
            groupAll=dict_.get('groupAll', False),
            columnIndices=dict_.get('columnIndices'),
            heatMapColorRange=HeatMapColorRange.from_dict(heat_map_color_range) if heat_map_color_range else None
        )


class ColumnFormat:
    def __init__(self,
                 *,
                 renderType: RenderType = RenderType.DEFAULT,
                 precision: int = 2,
                 humanReadable: bool = True,
                 tooltip: str = None,
                 displayValues: bool = True):
        """
        Use this class to specify the format options for your column.
        :param renderType: Type to use when rendering the column.
        :param precision: Number of precision points to use.
        :param humanReadable: Formats number to have commas.
        :param tooltip: Helper text to use as tooltip for the column.
        :param displayValues: For graphical render types only. True will show numerical values and title in the column.
         else only the graphics will be displayed.
         """
        self.renderType = renderType
        self.precision = precision
        self.humanReadable = humanReadable
        self.tooltip = tooltip
        self.displayValues = displayValues

    def as_dict(self):
        format_ = {
            'renderType': self.renderType,
            'precision': self.precision,
            'humanReadable': self.humanReadable,
        }

        if self.tooltip:
            format_['tooltip'] = self.tooltip

        if self.renderType != RenderType.DEFAULT:
            format_['displayValues'] = self.displayValues

        return format_

    @classmethod
    def from_dict(cls, obj: dict):
        return ColumnFormat(
            renderType=obj.get('renderType'),
            precision=obj.get('precision'),
            humanReadable=obj.get('humanReadable'),
            tooltip=obj.get('tooltip'),
            displayValues=obj.get('displayValues')
        )


class DataColumn:
    """Base class for grid column"""

    def __init__(self,
                 name: str,
                 processor: BaseProcessor = None,
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
        format_ = self.format_.as_dict()

        column = {
            'name': self.name,
            'format': format_,
            'width': self.width
        }

        processor = self.processor
        if processor:
            column['processorName'] = processor.__class__.__name__
            column.update(**processor.as_dict())

        return column

    @classmethod
    def from_dict(cls, obj: Dict, reference_list: List):
        processor = BaseProcessor.from_dict(obj, reference_list)

        return DataColumn(name=obj['name'],
                          processor=processor,
                          format_=ColumnFormat.from_dict(obj.get('format', {})),
                          width=obj.get('width', DEFAULT_WIDTH))
