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

from abc import ABC
from enum import Enum
from typing import Dict, List, Optional, Union

from gs_quant.analytics.core import BaseProcessor
from gs_quant.data import DataCoordinate
from gs_quant.data.fields import DataDimension
from gs_quant.entities.entity import Entity

DataDimensions = Dict[Union[DataDimension, str], Union[str, float]]

# Override Types
DIMENSIONS_OVERRIDE = 'dimensionsOverride'
PROCESSOR_OVERRIDE = 'processorOverride'
VALUE_OVERRIDE = 'valueOverride'

# Row Types
DATA_ROW = 'dataRow'
ROW_SEPARATOR = 'rowSeparator'


class Override(ABC):
    """Base class for a DataGrid row override"""

    def __init__(self,
                 column_names: List[str]):
        """ Abstract Row Override

        :param column_names: column names to override with the specified dimensions
        """
        self.column_names = column_names
        super().__init__()

    def as_dict(self) -> Dict:
        return {
            'columnNames': self.column_names
        }

    @classmethod
    def from_dict(cls, obj, reference_list):
        pass


class ValueOverride(Override):
    def __init__(self, column_names: List[str], value: Union[float, str, bool]):
        """
        Allows the ability to set a cell to a specific value.

        :param column_names: Name of columns to apply the value override.
        :param value: Value to set to the row and column intersections.
        """
        super().__init__(column_names)
        self.value = value

    def as_dict(self):
        override = super().as_dict()
        override['type'] = VALUE_OVERRIDE
        override['value'] = self.value
        return override

    @classmethod
    def from_dict(cls, obj, ref):
        return ValueOverride(column_names=obj.get('columnNames', []), value=obj['value'])


class DimensionsOverride(Override):
    def __init__(self,
                 column_names: List[str],
                 dimensions: DataDimensions,
                 coordinate: DataCoordinate):
        """ Override dimensions for the given coordinate

        :param column_names: column names to override with the specified dimensions
        :param dimensions: dict of dimensions to override columns when fetching data
        """
        super().__init__(column_names)
        # Following coordinate model, convert override dimensions to match coordinate dimension
        self.dimensions = {k.value if isinstance(k, Enum) else k: v for k, v in dimensions.items()}
        self.coordinate = coordinate

    def as_dict(self):
        override = super().as_dict()
        override['type'] = DIMENSIONS_OVERRIDE
        override['dimensions'] = self.dimensions
        override['coordinate'] = self.coordinate.as_dict()
        return override

    @classmethod
    def from_dict(cls, obj, reference_list):
        parsed_dimensions = {}
        data_dimension_map = DataDimension._value2member_map_
        for key, value in obj.get('dimensions', {}).items():
            if key in data_dimension_map:
                parsed_dimensions[DataDimension(key)] = value
            else:
                parsed_dimensions[key] = value
        return DimensionsOverride(column_names=obj.get('columnNames', []),
                                  dimensions=parsed_dimensions,
                                  coordinate=DataCoordinate.from_dict(obj.get('coordinate', {})))


class ProcessorOverride(Override):
    def __init__(self,
                 column_names: List[str],
                 processor: BaseProcessor):
        """ Abstract Row Override

        :param column_names: column names to override with the specified dimensions
        :param processor: processor to override
        """
        super().__init__(column_names=column_names)
        self.processor = processor

    def as_dict(self):
        override = super().as_dict()
        override['type'] = PROCESSOR_OVERRIDE
        if self.processor:
            override['processor'] = self.processor.as_dict()
            override['processor']['processorName'] = self.processor.__class__.__name__
        else:
            override['processor'] = None
            override['processor']['processorName'] = None
        return override

    @classmethod
    def from_dict(cls, obj, reference_list):
        return ProcessorOverride(column_names=obj.get('columnNames', []),
                                 processor=BaseProcessor.from_dict(obj.get('processor', {}), reference_list))


class RowSeparator:
    def __init__(self, name: str):
        """ Row Separator

        :param name: name of the row separator
        """
        self.name = name

    def as_dict(self):
        return {
            'type': ROW_SEPARATOR,
            'name': self.name
        }

    @classmethod
    def from_dict(cls, obj):
        return RowSeparator(obj['name'])


class DataRow:
    """Row object for DataGrid"""

    def __init__(self,
                 entity: Entity,
                 overrides: Optional[List[Override]] = None):
        """ Data row

        :param entity: Specified entity for the DataRow
        :param overrides: Optional List of DataRowOverride's for retrieving data
        """
        self.entity = entity
        self.overrides: List[Override] = overrides or []

    def as_dict(self):
        data_row = {
            'type': DATA_ROW,
            'entityId': self.entity.get_marquee_id() if isinstance(self.entity, Entity) else self.entity,
            'entityType': self.entity.entity_type().value if isinstance(self.entity, Entity) else ''
        }
        if len(self.overrides):
            data_row['overrides'] = [override.as_dict() for override in self.overrides]
        return data_row

    @classmethod
    def from_dict(cls, obj, reference_list):
        overrides = []
        for override_dict in obj.get('overrides', []):
            override_type = override_dict.get('type')
            if override_type == PROCESSOR_OVERRIDE:
                override = ProcessorOverride.from_dict(override_dict, reference_list)
            elif override_type == DIMENSIONS_OVERRIDE:
                override = DimensionsOverride.from_dict(override_dict, reference_list)
            else:
                override = ValueOverride.from_dict(override_dict, reference_list)
            overrides.append(override)

        data_row = DataRow(entity=None, overrides=overrides)  # Entity gets resolved later

        reference_list.append({
            'type': DATA_ROW,
            'entityId': obj.get('entityId', ''),
            'entityType': obj.get('entityType', ''),
            'reference': data_row
        })

        return data_row
