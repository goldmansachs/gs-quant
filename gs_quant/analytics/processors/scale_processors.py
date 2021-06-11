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

import math
from typing import Union, List, Tuple, Dict

from gs_quant.analytics.common.enumerators import ScaleShape
from gs_quant.analytics.core import BaseProcessor
from gs_quant.analytics.core.processor_result import ProcessorResult


class SpotMarkerProcessor(BaseProcessor):
    def __init__(self,
                 a: BaseProcessor,
                 *,
                 name: str,
                 shape: ScaleShape):
        """ SpotMarkerProcessor
        Spot Marker Processors are used to accommodate a single value in your scale and this value
        can take either a PIPE shape or a DIAMOND shape.

        :param a: BaseProcessor that should resolve in a single value
        :param name: Name of the Scale Marker
        :param shape: ScaleShape.PIPE or ScaleShape.DIAMOND
        """
        if shape not in [ScaleShape.PIPE, ScaleShape.DIAMOND]:
            raise TypeError("SpotMarkerProcessor only allows PIPE or DIAMOND ScaleShapes.")
        super().__init__()
        self.children['a'] = a
        self.name = name
        self.shape = shape

    def process(self):
        a_data = self.children_data.get('a')
        if isinstance(a_data, ProcessorResult):
            if a_data.success:
                self.value = ProcessorResult(True, {
                    'name': self.name,
                    'value': a_data.data.get(0),
                    'shape': self.shape.value
                })
            else:
                self.value = ProcessorResult(False, 'Could not compute pipe marker')
        else:
            self.value = ProcessorResult(False, 'Processor does not have data')

        return self.value

    def get_plot_expression(self):
        pass


class BarMarkerProcessor(BaseProcessor):
    def __init__(self,
                 start: BaseProcessor,
                 end: BaseProcessor,
                 *,
                 name: str):
        """ BarMarkerProcessor
        Bar Marker Processors require 2 values to render correctly in the scale. Both start and end
        processors should resolve in single values.

        :param start: BaseProcessor to obtain a starting value
        :param end: BaseProcessor to obtain an ending value
        :param name: Name of the Scale Marker
        """
        super().__init__()
        self.children['start'] = start
        self.children['end'] = end
        self.name = name
        self.shape = ScaleShape.BAR

    def process(self):
        start = self.children_data.get('start')
        end = self.children_data.get('end')
        if isinstance(start, ProcessorResult) and isinstance(end, ProcessorResult):
            if start.success and end.success:
                self.value = ProcessorResult(True, {
                    'name': self.name,
                    'start': start.data.get(0),
                    'end': end.data.get(0),
                    'shape': self.shape.value
                })
            else:
                self.value = ProcessorResult(False, "Processor does not have start and end values yet")
        else:
            self.value = ProcessorResult(False, "Processor does not have start and end data yet")

        return self.value

    def get_plot_expression(self):
        pass


SpotOrBarMarker = Union[SpotMarkerProcessor, BarMarkerProcessor]


def validate_markers_data(result: Dict, marker_data: Dict) -> Tuple[bool, str]:
    min_val = result['min']
    max_val = result['max']
    if not min_val or math.isnan(min_val):
        result['min'] = None
        return False, 'Min Value needs to exist for Scale to render'
    if not max_val or math.isnan(max_val):
        result['max'] = None
        return False, 'Max Value needs to exist for Scale to render'

    marker_name = marker_data["name"]
    if ScaleShape(marker_data['shape']) == ScaleShape.BAR:
        starting_val = marker_data['start']
        ending_val = marker_data['end']
        if starting_val > ending_val or starting_val < min_val or starting_val > max_val:
            return False, f'Invalid marker={marker_name} with starting value={starting_val}.' \
                          f'Has to be within range (min={min_val}, max={max_val}) and less ' \
                          f'than or equal to ending value=({ending_val})'
        if ending_val < starting_val or ending_val < min_val or ending_val > max_val:
            return False, f'Invalid marker={marker_name} with ending value={ending_val}.' \
                          f'Has to be within range (min={min_val}, max={max_val}) and greater ' \
                          f'than or equal to starting value=({starting_val})'
    else:
        if marker_data['value'] < min_val or marker_data['value'] > max_val:
            return False, f'Invalid marker={marker_data["name"]} with value={marker_data["value"]}. Has to be ' \
                          f'within range (min={min_val}, max={max_val})'
    return True, ''


class ScaleProcessor(BaseProcessor):
    def __init__(self,
                 minimum: BaseProcessor,
                 maximum: BaseProcessor,
                 *,
                 markers: List[SpotOrBarMarker]):
        """ ScaleProcessor
        A Scale processor can be used to render a scale in a DataGrid Column. It takes in the min value and max value
        processors which should resolve to single values. Additionally it take a list of markers to render within the
        scale. At the moment you can use wither a Spot Marker or a Bar Marker Processor.

        :param minimum: BaseProcessor to obtain min value for the scale
        :param maximum: BaseProcessor to obtain max value for the scale
        :param markers: List of either Spot or Bar Markers to display in the scale
        """
        super().__init__()
        self.children['minimum'] = minimum
        self.children['maximum'] = maximum
        self.markers = markers
        for marker in markers:
            self.children[marker.name] = marker

    def process(self):
        min_data = self.children_data.get('minimum')
        max_data = self.children_data.get('maximum')
        markers_data = [self.children_data.get(marker.name) for marker in self.markers]
        if isinstance(min_data, ProcessorResult) and isinstance(max_data, ProcessorResult):
            if min_data.success and max_data.success:
                result = {
                    'min': min_data.data.get(0),
                    'max': max_data.data.get(0),
                    'markers': []
                }
                for marker_data in markers_data:
                    if marker_data and marker_data.success and marker_data.data:
                        valid, reason = validate_markers_data(result, marker_data.data)
                        if valid:
                            result['markers'].append(marker_data.data)
                        else:
                            result['markers'].append({**marker_data.data, **{'invalidReason': reason}})
                self.value = ProcessorResult(True, result)
            else:
                self.value = ProcessorResult(False, "Processor does not have min, max values yet")
        else:
            self.value = ProcessorResult(False, "Processor does not have min, max data yet")

        return self.value

    def get_plot_expression(self):
        pass
