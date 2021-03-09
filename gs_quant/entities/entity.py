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

import datetime as dt
import json
import pandas as pd

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from enum import auto, Enum
from typing import Dict, Optional, Union, Tuple, List

from pydash import get

from gs_quant.api.gs.assets import GsAssetApi, PositionSet
from gs_quant.api.gs.data import GsDataApi
from gs_quant.common import PositionType, DateLimit
from gs_quant.data import DataCoordinate, DataFrequency, DataMeasure
from gs_quant.data.coordinate import DataDimensions
from gs_quant.errors import MqTypeError
from gs_quant.json_encoder import JSONEncoder
from gs_quant.session import GsSession


class EntityType(Enum):
    ASSET = 'asset'
    BACKTEST = 'backtest'
    COUNTRY = 'country'
    HEDGE = 'hedge'
    KPI = 'kpi'
    PORTFOLIO = 'portfolio'
    REPORT = 'report'
    RISK_MODEL = 'risk_model'
    SUBDIVISION = 'subdivision'


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
            id_type: Union[EntityIdentifier, str],
            entity_type: Optional[Union[EntityType, str]] = None) -> Optional['Entity']:
        id_type = id_type.value if isinstance(id_type, Enum) else id_type

        if entity_type is None:
            entity_type = cls.entity_type()
            endpoint = cls._entity_to_endpoint[entity_type]
        else:
            entity_type = entity_type.value if isinstance(entity_type, Enum) else entity_type
            endpoint = cls._entity_to_endpoint[EntityType(entity_type)]

        if entity_type == 'asset':
            from gs_quant.markets.securities import SecurityMaster, AssetIdentifier
            return SecurityMaster.get_asset(id_value, AssetIdentifier.MARQUEE_ID)

        if id_type == 'MQID':
            result = GsSession.current._get(f'/{endpoint}/{id_value}')
        else:
            result = get(GsSession.current._get(f'/{endpoint}?{id_type.lower()}={id_value}'), 'results.0')
        if result:
            return cls._get_entity_from_type(result, EntityType(entity_type))

    @classmethod
    def _get_entity_from_type(cls,
                              entity: Dict,
                              entity_type: EntityType = None):
        id_ = entity.get('id')
        entity_type = entity_type or cls.entity_type()
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
                            measure: Union[DataMeasure, str],
                            dimensions: Optional[DataDimensions] = None,
                            frequency: DataFrequency = DataFrequency.DAILY,
                            availability=None) -> DataCoordinate:
        id_ = self.get_marquee_id()
        dimensions = dimensions or {}
        dimensions[self.data_dimension] = id_
        measure = measure if isinstance(measure, str) else measure.value
        available: Dict = GsDataApi.get_data_providers(id_, availability).get(measure, {})

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

    def get_name(self) -> Optional[str]:
        return get(self.get_entity(), 'name')

    def get_region(self) -> Optional[str]:
        return get(self.get_entity(), 'region')

    def get_sub_region(self):
        return get(self.get_entity(), 'subRegion')

    def get_region_code(self):
        return get(self.get_entity(), 'regionCode')

    def get_sub_region_code(self):
        return get(self.get_entity(), 'subRegionCode')

    def get_alpha3(self):
        return get(self.get_entity(), 'xref.alpha3')

    def get_bbid(self):
        return get(self.get_entity(), 'xref.bbid')

    def get_alpha2(self):
        return get(self.get_entity(), 'xref.alpha2')

    def get_country_code(self):
        return get(self.get_entity(), 'xref.countryCode')


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

    def get_name(self) -> Optional[str]:
        return get(self.get_entity(), 'name')


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

    def get_name(self) -> Optional[str]:
        return get(self.get_entity(), 'name')

    def get_category(self) -> Optional[str]:
        return get(self.get_entity(), 'category')

    def get_sub_category(self):
        return get(self.get_entity(), 'subCategory')


class ReturnFormat(Enum):
    DICT = auto()
    DATA_FRAME = auto()
    POSITION_SET = auto()


class PositionedEntity(metaclass=ABCMeta):
    __invalid_entity_message = 'Unable to fetch positions, as function does not currently support entity type'

    def __init__(self, id_: str, entity_type: EntityType):
        self.__id: str = id_
        self.__entity_type: EntityType = entity_type

    @property
    def id(self) -> str:
        return self.__id

    @property
    def positioned_entity_type(self) -> EntityType:
        return self.__entity_type

    def get_latest_positions(self,
                             position_type: PositionType = PositionType.CLOSE,
                             format: ReturnFormat = ReturnFormat.DICT) -> Union[PositionSet, Dict, pd.DataFrame]:
        if self.positioned_entity_type == EntityType.ASSET:
            response = GsAssetApi.get_latest_positions(self.id, position_type)
            position_set = response if type(response) == PositionSet else PositionSet.from_dict(response)
            return self.__convert_position_set(position_set, format)

        raise MqTypeError(f'{self.__invalid_entity_message} {self.positioned_entity_type}')

    def get_positions_for_date(self,
                               position_date: dt.date,
                               position_type: PositionType = PositionType.CLOSE,
                               format: ReturnFormat = ReturnFormat.DICT) -> Union[PositionSet, Dict, pd.DataFrame]:
        if self.positioned_entity_type == EntityType.ASSET:
            position_set = GsAssetApi.get_asset_positions_for_date(self.id, position_date, position_type)[0]
            return self.__convert_position_set(position_set, format)

        raise MqTypeError(f'{self.__invalid_entity_message} {self.positioned_entity_type}')

    def get_positions(self,
                      start_date: dt.date = DateLimit.LOW_LIMIT.value,
                      end_date: dt.date = DateLimit.TODAY.value,
                      position_type: PositionType = PositionType.CLOSE,
                      format: ReturnFormat = ReturnFormat.DICT) -> Union[Tuple[PositionSet], Dict, pd.DataFrame]:
        if self.positioned_entity_type == EntityType.ASSET:
            position_sets = GsAssetApi.get_asset_positions_for_dates(self.id, start_date, end_date, position_type)
            return self.__convert_position_sets(position_sets, format)

        raise MqTypeError(f'{self.__invalid_entity_message} {self.positioned_entity_type}')

    def get_positions_data(self,
                           start_date: dt.date = DateLimit.LOW_LIMIT.value,
                           end_date: dt.date = DateLimit.TODAY.value,
                           fields: [str] = None,
                           position_type: PositionType = PositionType.CLOSE) -> List[Dict]:
        if self.positioned_entity_type == EntityType.ASSET:
            return GsAssetApi.get_asset_positions_data(self.id, start_date, end_date, fields, position_type)

        raise MqTypeError(f'{self.__invalid_entity_message} {self.positioned_entity_type}')

    def __convert_position_set(self,
                               position_set: PositionSet,
                               format: ReturnFormat) -> Union[PositionSet, Dict, pd.DataFrame]:
        format = ReturnFormat[format.upper()] if isinstance(format, str) else format
        if format == ReturnFormat.POSITION_SET:
            return position_set
        elif format == ReturnFormat.DICT:
            pset_dict: Dict = json.loads(json.dumps(position_set.as_dict(), cls=JSONEncoder))
            return {'positionDate': position_set.position_date.isoformat(),
                    'divisor': position_set.divisor,
                    'positions': pset_dict['positions']}
        else:
            position_dict = [{'positionDate': position_set.position_date.isoformat(),
                              'divisor': position_set.divisor,
                              'assetId': position.asset_id,
                              'quantity': position.quantity} for position in position_set.positions]
            return pd.DataFrame(position_dict)

    def __convert_position_sets(self,
                                position_sets: Tuple[PositionSet],
                                format: ReturnFormat) -> Union[Tuple[PositionSet], Dict, pd.DataFrame]:
        format = ReturnFormat[format.upper()] if isinstance(format, str) else format
        if format == ReturnFormat.POSITION_SET:
            return position_sets
        elif format == ReturnFormat.DICT:
            position_set_dict = {}
            for position_set in position_sets:
                position_set_dict[position_set.position_date.isoformat()] = \
                    self.__convert_position_set(position_set, format)
            return position_set_dict
        else:
            position_set_df = []
            for position_set in position_sets:
                position_set_df.append(self.__convert_position_set(position_set, format))
            return pd.concat(position_set_df)
