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
from enum import Enum
from typing import Union

from pydash import get

from gs_quant.analytics.core.processor import BaseProcessor
from gs_quant.analytics.core.processor_result import ProcessorResult
from gs_quant.data import DataDimension, DataCoordinate
from gs_quant.entities.entity import Entity


class EntityProcessor(BaseProcessor):
    def __init__(self, field: str):
        """ EntityProcessor gets a value off an entity object

        :param field: The entity property to be returned. If a nested field, separate each level with ".",
            i.e. 'xref.bbid'
        """
        super().__init__()
        self.field = field

    def process(self, entity: Entity) -> ProcessorResult:
        """ Fetch the entity and resolve the field """
        if isinstance(entity, str):  # If we were unable to fetch entity (404/403)
            return ProcessorResult(False, f"Unable to resolve Entity {entity}")
        try:
            # First try to get the value off the entity
            entity_dict = entity.get_entity()
            data = get(entity_dict, self.field)
            if data:
                return ProcessorResult(True, data)

            # If not found, try to get the value from the asset identifiers
            identifier = next(iter(filter(lambda x: x['type'] == self.field, entity_dict.get('identifiers', []))), None)
            if identifier:
                return ProcessorResult(True, identifier['value'])

            # Return a failed processor result if no field was found on the object or it's identifiers
            return ProcessorResult(False,
                                   f'Unable to find {self.field} in identifiers for entity {entity.get_marquee_id()}')

        except ValueError:
            return ProcessorResult(False, "Could not get field on entity")

    def update(self, attribute: str, result: ProcessorResult) -> None:
        """ This method does not apply for entity processor """
        pass

    def get_plot_expression(self):
        """ This method does not apply for entity processor """
        pass


class CoordinateProcessor(BaseProcessor):
    def __init__(self,
                 a: DataCoordinate,
                 dimension: Union[DataDimension, str]):
        """ Returns a field from a coordinate

        :param a: coordinate to get the field
        :param dimension: dimension to get from the coordinate
        """
        super().__init__()
        # coordinate
        self.children['a'] = a
        # parameters
        self.dimension = dimension

    def process(self):
        key: str = self.dimension.value if isinstance(self.dimension, Enum) else self.dimension
        coordinate = self.children.get('a')
        dimension_value = coordinate.dimensions.get(key) if coordinate else None
        if dimension_value:
            return ProcessorResult(True, dimension_value)
        else:
            return ProcessorResult(False, f'Dimension {key} not in given coordinate')

    def update(self, attribute: str, result: ProcessorResult):
        pass

    def get_plot_expression(self):
        pass
