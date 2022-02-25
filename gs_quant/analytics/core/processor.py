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
import asyncio
import functools
import logging
import uuid
from abc import ABCMeta, abstractmethod
from concurrent.futures.process import ProcessPoolExecutor
from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum, EnumMeta
from typing import List, Optional, Union, Dict, get_type_hints, Set, Tuple

import numpy as np
from pandas import Series
from pydash import decapitalize, get

from gs_quant.analytics.common import TYPE, PROCESSOR, PARAMETERS, DATA_COORDINATE, \
    ENTITY, VALUE, DATE, DATETIME, PROCESSOR_NAME, ENTITY_ID, ENTITY_TYPE, PARAMETER, REFERENCE, RELATIVE_DATE, LIST
from gs_quant.analytics.common.enumerators import ScaleShape
from gs_quant.analytics.common.helpers import is_of_builtin_type, get_entity_rdate_key_from_rdate
from gs_quant.analytics.core.processor_result import ProcessorResult
from gs_quant.data import DataCoordinate, DataFrequency
from gs_quant.data.query import DataQuery, DataQueryType
from gs_quant.entities.entity import Entity
from gs_quant.target.common import Currency
from gs_quant.timeseries import Window, Returns, RelativeDate, DateOrDatetime

PARSABLE_OBJECT_MAP = {
    'window': Window,
    'returns': Returns,
    'currency': Currency,
    'scaleShape': ScaleShape
}

_logger = logging.getLogger(__name__)


@dataclass
class DataQueryInfo:
    attr: str
    processor: 'BaseProcessor'
    query: DataQuery
    entity: Entity
    data: Series = None


@dataclass
class MeasureQueryInfo:
    attr: str
    processor: 'BaseProcessor'
    entity: Entity


DateOrDatetimeOrRDate = Union[DateOrDatetime, RelativeDate]


class BaseProcessor(metaclass=ABCMeta):
    def __init__(self, **kwargs):
        self.id = f'{self.__class__.__name__}-{str(uuid.uuid4())}'
        self.value: ProcessorResult = ProcessorResult(False, 'Value not set')
        self.parent: Optional[Union[BaseProcessor]] = None
        self.parent_attr: Optional[str] = None
        self.children: Dict[str, Union[DataCoordinateOrProcessor, DataQueryInfo]] = {}
        self.children_data: Dict[str, ProcessorResult] = {}
        self.data_cell = None
        self.last_value = kwargs.get('last_value', False)
        self.measure_processor = kwargs.get('measure_processor', False)

    @abstractmethod
    def process(self, *args):
        """ Handle the calculation of the data with given coordinate data series """
        pass

    def post_process(self):
        if self.last_value:
            if isinstance(self.value, ProcessorResult) and self.value.success \
                    and isinstance(self.value.data, Series) and not self.value.data.empty:
                self.value.data = self.value.data.iloc[-1:]

    def __handle_date_range(self,
                            result,
                            rdate_entity_map: Dict[str, date]):
        """
        Applies a date/datetime mask on the result using the start/end parameters on a processor
        :param result:
        :param rdate_entity_map: map of entity, rule, base_date to date value
        :return: None
        """
        if not isinstance(result, ProcessorResult) or not result.success:
            return
        start, end = get(self, 'start'), get(self, 'end')
        if not (start or end):
            return

        entity = self.data_cell.entity
        # If the entity wasn't found default to base rule (no entity)
        entity_id = '' if isinstance(entity, str) else entity.get_marquee_id()
        if start and end:
            if isinstance(start, RelativeDate):
                key = get_entity_rdate_key_from_rdate(entity_id, start)
                start = rdate_entity_map[key]
            if isinstance(end, RelativeDate):
                key = get_entity_rdate_key_from_rdate(entity_id, end)
                end = rdate_entity_map[key]
            mask = (result.data.index >= np.datetime64(start)) & (result.data.index <= np.datetime64(end))
        elif start:
            if isinstance(start, RelativeDate):
                key = get_entity_rdate_key_from_rdate(entity_id, start)
                start = rdate_entity_map[key]
            mask = (result.data.index >= np.datetime64(start))
        else:
            if isinstance(end, RelativeDate):
                key = get_entity_rdate_key_from_rdate(entity_id, end)
                end = rdate_entity_map[key]
            mask = (result.data.index >= np.datetime64(end))

        result.data = result.data[mask]

    async def update(self,
                     attribute: str,
                     result: ProcessorResult,
                     rdate_entity_map: Dict[str, date],
                     pool: ProcessPoolExecutor = None,
                     query_info: Union[DataQueryInfo, MeasureQueryInfo] = None):
        """ Handle the update of a single coordinate and recalculate the value

        :param attribute: Attribute alinging to data coordinate in the processor
        :param result: Processor result including success and series from data query
        """
        if not self.measure_processor:
            self.__handle_date_range(result, rdate_entity_map)
        self.children_data[attribute] = result

        if isinstance(result, ProcessorResult):
            if result.success:
                try:
                    if pool:
                        if self.measure_processor:
                            value = await asyncio.get_running_loop()\
                                .run_in_executor(pool, functools.partial(self.process, query_info.entity))
                        else:
                            value = await asyncio.get_running_loop().run_in_executor(pool, self.process)
                        self.value = value
                    else:
                        if self.measure_processor:
                            self.process(query_info.entity)
                        else:
                            self.process()
                    self.post_process()
                except Exception as e:
                    self.value = ProcessorResult(False,
                                                 f'Error Calculating processor {self.__class__.__name__}  due to {e}')
            else:
                self.value = result

    @abstractmethod
    def get_plot_expression(self):
        """ Returns a plot expression used to go from grid to plottool """
        pass

    def __add_required_rdates(self, entity: Entity, rdate_entity_map: Dict[str, Set[Tuple]]):
        start, end = get(self, 'start'), get(self, 'end')
        entity_id = entity.get_marquee_id() if isinstance(entity, Entity) else ''

        if isinstance(start, RelativeDate):
            base_date = str(start.base_date) if start.base_date_passed_in else None
            rdate_entity_map[entity_id].add((start.rule, base_date))
        if isinstance(end, RelativeDate):
            base_date = str(end.base_date) if end.base_date_passed_in else None
            rdate_entity_map[entity_id].add((end.rule, base_date))

    def build_graph(self,
                    entity: Entity,
                    cell,
                    queries: List[Union[DataQueryInfo, MeasureQueryInfo]],
                    rdate_entity_map: Dict[str, Set[Tuple]],
                    overrides: Optional[List]):
        """ Generates the nested cell graph and keeps a map of leaf data queries to processors"""
        self.data_cell = cell
        self.__add_required_rdates(entity, rdate_entity_map)

        attributes = self.__dict__

        if self.measure_processor:
            queries.append(MeasureQueryInfo(attr='a', processor=self, entity=entity))

        for attr_name, child in self.children.items():
            if isinstance(child, DataCoordinate):
                # Override coordinate dimensions
                if overrides:
                    override_dimensions = list(filter(lambda x: x.coordinate == child, overrides))
                    if len(override_dimensions):
                        use_default = True
                        for override in overrides:
                            if override.coordinate_id == child.id:
                                child.set_dimensions(override.dimensions)
                                use_default = False
                                break
                        if use_default and overrides[0].coordinate_id is None:
                            child.set_dimensions(overrides[0].dimensions)

                if child.frequency == DataFrequency.DAILY:
                    query = DataQuery(coordinate=child, start=attributes.get('start'), end=attributes.get('end'))
                else:
                    query = DataQuery(coordinate=child, query_type=DataQueryType.LAST)

                # track the leaf data query
                queries.append(DataQueryInfo(attr=attr_name,
                                             processor=self,
                                             query=query,
                                             entity=entity))

            elif isinstance(child, BaseProcessor):
                # Set the children's parent fields
                child.parent = self
                child.parent_attr = attr_name
                child.build_graph(entity, cell, queries, rdate_entity_map, overrides)

            elif isinstance(child, DataQueryInfo):
                child.parent = self
                child.parent_attr = attr_name
                child.processor = self
                queries.append(child)

    async def calculate(self,
                        attribute: str,
                        result: ProcessorResult,
                        rdate_entity_map: Dict[str, date],
                        pool: ProcessPoolExecutor = None,
                        query_info: Union[DataQueryInfo, MeasureQueryInfo] = None):
        """ Sets the result on the processor and recursively calls parent to set and calculate value

            :param attribute: Attribute alinging to data coordinate in the processor
            :param result: Processor result including success and series from data query
        """
        # update the result
        await self.update(attribute, result, rdate_entity_map, pool, query_info)

        # if there is a parent, traverse up and recompute
        if self.parent:
            value: ProcessorResult = self.value
            if isinstance(value, ProcessorResult):
                # only traverse if processor successful calculates
                if value.success:
                    if isinstance(self.parent, BaseProcessor):
                        await self.parent.calculate(self.parent_attr, value, rdate_entity_map, pool)
                    else:
                        # Must be the data cell
                        self.parent.update(value)
                else:
                    self.data_cell.value = value  # Put the error on the data cell
                    self.data_cell.updated_time = f'{datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]}Z'

    def as_dict(self) -> Dict:
        """
        Create a dictionary representation of the processor. Used for eventually turning the processor into json for
        API usage. Allows for nested processors.
        :return: Dictionary representation of the processor
        """
        processor = {
            TYPE: PROCESSOR,
            PARAMETERS: self.get_default_params()
        }

        if isinstance(self, BaseProcessor):
            processor[PROCESSOR_NAME] = self.__class__.__name__

        parameters = processor[PARAMETERS]

        for parameter, alias in get_type_hints(self.__init__).items():
            if alias in (DataCoordinateOrProcessor, DataCoordinate,
                         Union[DataCoordinateOrProcessor, None],
                         BaseProcessor):
                # If the parameter is a DataCoordinate or processor, recursively call as_dict()
                attribute = self.children[parameter]
                if attribute is None:
                    continue
                parameters[parameter] = {}
                this_parameter = parameters[parameter]

                if isinstance(attribute, BaseProcessor):
                    this_parameter[TYPE] = PROCESSOR
                    this_parameter[PROCESSOR_NAME] = attribute.__class__.__name__
                elif isinstance(attribute, DataCoordinate):
                    this_parameter[TYPE] = DATA_COORDINATE
                else:
                    # Continue if not an expected type or None
                    continue

                this_parameter.update(**attribute.as_dict())
            else:
                # Handle the less complex types such as python built in types, enums, entities, datetimes
                attribute = getattr(self, parameter)
                if attribute is not None:
                    parameters[parameter] = {}
                    if isinstance(attribute, list):
                        value = [item.as_dict() for item in attribute]
                    elif is_of_builtin_type(attribute):
                        value = attribute
                    elif isinstance(attribute, Enum):
                        value = attribute.value
                    elif isinstance(attribute, Entity):
                        parameters[parameter].update({
                            TYPE: ENTITY,
                            ENTITY_ID: attribute.get_marquee_id(),
                            ENTITY_TYPE: attribute.entity_type().value
                        })
                        continue
                    elif isinstance(attribute, (date, datetime)):
                        if isinstance(attribute, date):
                            value = str(attribute)
                        else:
                            value = f"{attribute.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]}Z"
                    else:
                        value = attribute.as_dict()
                    parameters[parameter].update({
                        TYPE: decapitalize(type(attribute).__name__),
                        VALUE: value
                    })

        return processor

    def get_default_params(self):
        # Handle all the kwarg based parameters that all processors take
        default_params = {}
        if self.last_value:
            default_params['last_value'] = dict(type='bool', value=True)
        return default_params

    @classmethod
    def from_dict(cls, obj: Dict, reference_list: List):
        processor_name: str = obj.get(PROCESSOR_NAME, 'None')
        # Dynamically import the processor to for instantiation.
        processor = getattr(__import__('gs_quant.analytics.processors', fromlist=['']), processor_name, None)

        parameters = obj.get(PARAMETERS, {})

        local_reference_list = []
        arguments = {}

        for parameter, parameters_dict in parameters.items():
            # Loop through all the parameters and turned them into objects based off their dictionary values.
            # Will recursively handle the more complex objects such as DataCoordinate and Processors.
            parameter_type: str = parameters_dict.get(TYPE)

            if parameter_type == DATA_COORDINATE:
                # Handle the DataCoordinate parameters
                arguments[parameter] = DataCoordinate.from_dict(parameters_dict)
            elif parameter_type == PROCESSOR:
                # Handle the BaseProcessor parameters
                arguments[parameter] = BaseProcessor.from_dict(parameters_dict, reference_list)
            elif parameter_type == ENTITY:
                # Handle the entity parameter list and put into the reference mapped to be resolved later
                local_reference_list.append({TYPE: PROCESSOR,
                                             ENTITY_ID: parameters_dict.get(ENTITY_ID),
                                             ENTITY_TYPE: parameters_dict.get(ENTITY_TYPE),
                                             PARAMETER: parameter})

                arguments[parameter] = None
            elif parameter_type in (DATE, DATETIME, RELATIVE_DATE):
                # Handle date/datetime parameters
                if parameter_type == DATE:
                    arguments[parameter] = datetime.strptime(parameters_dict.get(VALUE), '%Y-%m-%d').date()
                elif parameter_type == RELATIVE_DATE:
                    val = parameters_dict.get(VALUE)
                    base_date = val.get('baseDate')
                    base_date = datetime.strptime(base_date, '%Y-%m-%d').date() if base_date else None
                    arguments[parameter] = RelativeDate(rule=val['rule'], base_date=base_date)
                else:
                    arguments[parameter] = datetime.strptime(parameters_dict.get(VALUE)[0:-1], '%Y-%m-%dT%H:%M:%S.%f')
            else:
                # Handle all other object which should be mapped in the PARSABLE_OBJECT_MAP
                if parameter_type in PARSABLE_OBJECT_MAP:
                    parameter_obj = PARSABLE_OBJECT_MAP[parameter_type]
                    if isinstance(parameter_obj, (Enum, EnumMeta)):
                        arguments[parameter] = parameter_obj(parameters_dict.get(VALUE, {}))
                    else:
                        arguments[parameter] = parameter_obj.from_dict(parameters_dict.get(VALUE, {}))
                elif parameter_type == LIST:
                    arguments[parameter] = [BaseProcessor.from_dict(item, reference_list)
                                            if isinstance(item, dict) else item
                                            for item in parameters_dict['value']]
                else:
                    # Handles built in types that are stored natively
                    arguments[parameter] = parameters_dict.get(VALUE)

        processor = processor(**arguments) if processor else None  # Instantiate the processor with all arguments

        # Add all the references to entities to the list which will be resolved later
        for reference in local_reference_list:
            reference[REFERENCE] = processor

        reference_list.extend(local_reference_list)
        return processor


DataCoordinateOrProcessor = Union[DataCoordinate, BaseProcessor]
