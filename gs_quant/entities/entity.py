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

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional

from pydash import get

from gs_quant.api.gs.data import GsDataApi
from gs_quant.data import DataCoordinate, DataFrequency, DataMeasure
from gs_quant.data.coordinate import DataDimensions
from gs_quant.session import GsSession


class EntityType(Enum):
    ASSET = 'asset'
    COUNTRY = 'country'
    SUBDIVISION = 'subdivision'
    KPI = 'kpi'


@dataclass
class EntityKey:
    id_: str
    entity_type: EntityType


class EntityIdentifier(Enum):
    pass


class Entity(metaclass=ABCMeta):
    """Base class for any first-class entity"""
    _entity_to_endpoint = {
        EntityType.ASSET: 'assets',
        EntityType.COUNTRY: 'countries',
        EntityType.SUBDIVISION: 'countries/subdivisions',
        EntityType.KPI: 'kpis'
    }

    def __init__(self,
                 id_: str,
                 entity_type: EntityType,
                 entity: Optional[Dict] = None):
        self.__id: str = id_
        self.__entity_type: EntityType = entity_type
        self.__entity: Dict = entity

    @property
    @abstractmethod
    def data_dimension(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def entity_type(cls) -> EntityType:
        pass

    @classmethod
    def get(cls,
            id_value: str,
            id_type: EntityIdentifier) -> Optional['Entity']:
        if id_type.value == 'MQID':
            result = GsSession.current._get(f'/{cls._entity_to_endpoint[cls.entity_type()]}/{id_value}')
        else:
            result = get(GsSession.current._get(
                f'/{cls._entity_to_endpoint[cls.entity_type()]}?{id_type.value.lower()}={id_value}'), 'results.0')
        if result:
            return cls._get_entity_from_type(result)

    @classmethod
    def _get_entity_from_type(cls,
                              entity: Dict):
        id_ = entity.get('id')
        entity_type = cls.entity_type()
        if entity_type == EntityType.COUNTRY:
            return Country(id_, entity=entity)
        if entity_type == EntityType.KPI:
            return KPI(id_, entity=entity)
        if entity_type == EntityType.SUBDIVISION:
            return Subdivision(id_, entity=entity)

    def get_marquee_id(self) -> str:
        return self.__id

    def get_entity(self) -> Optional[Dict]:
        return self.__entity

    def get_unique_entity_key(self) -> EntityKey:
        return EntityKey(self.__id, self.__entity_type)

    def get_data_coordinate(self,
                            measure: DataMeasure,
                            dimensions: Optional[DataDimensions] = None,
                            frequency: Optional[DataFrequency] = None) -> DataCoordinate:
        id_ = self.get_marquee_id()
        dimensions = dimensions or {}
        dimensions[self.data_dimension] = id_
        available: Dict = GsDataApi.get_data_providers(id_).get(measure.value, {})

        if frequency == DataFrequency.DAILY:
            daily_dataset_id = available.get(DataFrequency.DAILY)
            return DataCoordinate(dataset_id=daily_dataset_id, measure=measure, dimensions=dimensions,
                                  frequency=frequency)
        if frequency == DataFrequency.REAL_TIME:
            rt_dataset_id = available.get(DataFrequency.REAL_TIME)
            return DataCoordinate(dataset_id=rt_dataset_id, measure=measure, dimensions=dimensions, frequency=frequency)


class Country(Entity):
    class Identifier(EntityIdentifier):
        MARQUEE_ID = 'MQID'
        NAME = 'name'

    def __init__(self,
                 id_: str,
                 entity: Optional[Dict] = None):
        super().__init__(id_, EntityType.COUNTRY, entity)

    @property
    def data_dimension(self) -> str:
        return 'countryId'

    @classmethod
    def entity_type(cls) -> EntityType:
        return EntityType.COUNTRY

    @classmethod
    def get_by_identifier(cls,
                          id_value: str,
                          id_type: Identifier) -> Optional['Entity']:
        super().get(id_value, id_type)


class Subdivision(Entity):
    class Identifier(EntityIdentifier):
        MARQUEE_ID = 'MQID'
        name = 'name'

    def __init__(self,
                 id_: str,
                 entity: Optional[Dict] = None):
        super().__init__(id_, EntityType.SUBDIVISION, entity)

    @property
    def data_dimension(self) -> str:
        return 'subdivisionId'

    @classmethod
    def entity_type(cls) -> EntityType:
        return EntityType.SUBDIVISION

    @classmethod
    def get_by_identifier(cls,
                          id_value: str,
                          id_type: Identifier) -> Optional['Entity']:
        super().get(id_value, id_type)


class KPI(Entity):
    class Identifier(EntityIdentifier):
        MARQUEE_ID = "MQID"
        name = 'name'

    def __init__(self,
                 id_: str,
                 entity: Optional[Dict] = None):
        super().__init__(id_, EntityType.KPI, entity)

    @property
    def data_dimension(self) -> str:
        return 'kpiId'

    @classmethod
    def entity_type(cls) -> EntityType:
        return EntityType.KPI

    @classmethod
    def get_by_identifier(cls,
                          id_value: str,
                          id_type: Identifier) -> Optional['Entity']:
        super().get(id_value, id_type)
