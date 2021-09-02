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
import datetime
import logging
from typing import Dict, List, Union

import pandas as pd
from pydash import get

from gs_quant.api.gs.assets import GsAssetApi
from gs_quant.errors import MqValueError
from gs_quant.target.common import Position as CommonPosition
from gs_quant.target.common import PositionSet as CommonPositionSet
from gs_quant.target.indices import PositionPriceInput

_logger = logging.getLogger(__name__)


class Position:
    def __init__(self,
                 identifier: str,
                 weight: float = None,
                 quantity: float = None,
                 name: str = None,
                 asset_id: str = None):
        self.__identifier = identifier
        self.__weight = weight
        self.__quantity = quantity
        self.__name = name
        self.__asset_id = asset_id
        if asset_id is None:
            self.__resolve_identifier(identifier)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Position):
            return False
        for prop in ['asset_id', 'weight', 'quantity']:
            slf = get(self, prop)
            oth = get(other, prop)
            if not (slf is None and oth is None) and not slf == oth:
                return False
        return True

    def __hash__(self):
        return hash(self.asset_id) ^ hash(self.identifier)

    @property
    def identifier(self) -> str:
        return self.__identifier

    @identifier.setter
    def identifier(self, value: str):
        self.__identifier = value

    @property
    def weight(self) -> float:
        return self.__weight

    @weight.setter
    def weight(self, value: float):
        self.__weight = value

    @property
    def quantity(self) -> float:
        return self.__quantity

    @quantity.setter
    def quantity(self, value: float):
        self.__quantity = value

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def asset_id(self) -> str:
        return self.__asset_id

    @asset_id.setter
    def asset_id(self, value: str):
        self.__asset_id = value

    def as_dict(self) -> Dict:
        position_dict = dict(identifier=self.identifier, weight=self.weight,
                             quantity=self.quantity, name=self.name, asset_id=self.asset_id)
        return {k: v for k, v in position_dict.items() if v is not None}

    def to_target(self, common: bool = True) -> Union[CommonPosition, PositionPriceInput]:
        """ Returns Postion type defined in target file for API payloads """
        if common:
            return CommonPosition(self.asset_id, quantity=self.quantity)
        return PositionPriceInput(self.asset_id, quantity=self.quantity, weight=self.weight)

    def __resolve_identifier(self, identifier: str) -> Dict:
        response = GsAssetApi.resolve_assets(identifier=[identifier], fields=['id', 'name'], limit=1)[identifier]
        if len(response) == 0:
            raise MqValueError(f'Asset could not be found using identifier {identifier}')
        self.__name = get(response, '0.name')
        self.__asset_id = get(response, '0.id')


class PositionSet:
    """

    Position Sets hold a collection of positions associated with a particular date

    """

    def __init__(self,
                 positions: List[Position],
                 date: datetime.date = datetime.date.today(),
                 divisor: float = None):
        self.__positions = positions
        self.__date = date
        self.__divisor = divisor

    @property
    def positions(self) -> List[Position]:
        return self.__positions

    @positions.setter
    def positions(self, value: List[Position]):
        self.__positions = value

    @property
    def date(self) -> datetime.date:
        return self.__date

    @date.setter
    def date(self, value: datetime.date):
        self.__date = value

    @property
    def divisor(self) -> float:
        return self.__divisor

    def get_positions(self) -> pd.DataFrame:
        """ Retrieve formatted positions """
        positions = [p.as_dict() for p in self.positions]
        return pd.DataFrame(positions)

    def equalize_position_weights(self):
        """ Assigns equal weight to each position in position set """
        weight = 1 / len(self.positions)
        equally_weighted_positions = []
        for p in self.positions:
            p.weight = weight
            p.quantity = None
            equally_weighted_positions.append(p)
        self.positions = equally_weighted_positions

    def to_frame(self) -> pd.DataFrame:
        """ Retrieve formatted position set """
        positions = []
        for p in self.positions:
            position = dict(date=self.date.isoformat())
            if self.divisor is not None:
                position.update(dict(divisor=self.divisor))
            position.update(p.as_dict())
            positions.append(position)
        return pd.DataFrame(positions)

    def to_target(self, common: bool = True) -> Union[CommonPositionSet, List[PositionPriceInput]]:
        """ Returns PostionSet type defined in target file for API payloads """
        positions = tuple(p.to_target(common) for p in self.positions)
        return CommonPositionSet(positions, self.date) if common else list(positions)

    @classmethod
    def from_target(cls, position_set: CommonPositionSet):
        """ Create PostionSet instance from PostionSet type defined in target file """
        positions = position_set.positions
        mqids = [position.asset_id for position in positions]
        position_data = cls.__get_positions_data(mqids)
        converted_positions = []
        for p in positions:
            asset = get(position_data, p.asset_id)
            position = Position(identifier=get(asset, 'bbid'), name=get(asset, 'name'),
                                asset_id=p.asset_id, quantity=p.quantity)
            converted_positions.append(position)
        return cls(converted_positions, position_set.position_date, position_set.divisor)

    @classmethod
    def from_list(cls, positions: List[str], date: datetime.date = datetime.date.today()):
        """ Create equally-weighted PostionSet instance from a list of identifiers """
        id_map = cls.__resolve_identifiers(positions)
        converted_positions = []
        weight = 1 / len(positions)

        for p in positions:
            identifier = get(p, 'identifier')
            asset = get(id_map, identifier)
            position = Position(identifier=identifier, asset_id=get(asset, 'id'),
                                name=get(asset, 'name'), weight=weight)
            converted_positions.append(position)
        return cls(converted_positions, date)

    @classmethod
    def from_dicts(cls, positions: List[Dict], date: datetime.date = datetime.date.today()):
        """ Create PostionSet instance from a list of position-object-like dictionaries """
        positions_df = pd.DataFrame(positions)
        return cls.from_frame(positions_df, date)

    @classmethod
    def from_frame(cls, positions: pd.DataFrame, date: datetime.date = datetime.date.today()):
        """ Create PostionSet instance from a list of position-object-like dataframes """
        positions.columns = positions.columns.str.lower()
        positions = positions[~positions['identifier'].isnull()]
        id_map = cls.__resolve_identifiers(identifiers=positions['identifier'].to_list(), date=date)
        equalize = not ('quantity' in positions.columns or 'weight' in positions.columns)
        equal_weight = 1 / len(positions)
        converted_positions = []

        for i, row in positions.iterrows():
            identifier = get(row, 'identifier')
            asset = get(id_map, identifier)
            weight = get(row, 'weight') if not equalize else equal_weight
            quantity = get(row, 'quantity') if not equalize else None
            position = Position(identifier=identifier, asset_id=get(asset, 'id'), name=get(asset, 'name'),
                                weight=weight, quantity=quantity)
            converted_positions.append(position)
        return cls(converted_positions, date)

    @staticmethod
    def __resolve_identifiers(identifiers: List[str], date: datetime.date) -> Dict:
        response = GsAssetApi.resolve_assets(
            identifier=identifiers,
            fields=['name', 'id'],
            limit=1,
            as_of=date
        )
        try:
            id_map = dict(zip(response.keys(),
                          [dict(id=asset[0]['id'], name=asset[0]['name']) for asset in response.values()]))
        except IndexError:
            unmapped_assets = {_id for _id, asset in response.items() if not asset}
            raise MqValueError(f'Error in resolving the following identifiers: {unmapped_assets}')
        return id_map

    @staticmethod
    def __get_positions_data(mqids: List[str]) -> Dict:
        response = GsAssetApi.get_many_assets_data(id=mqids, fields=['id', 'name', 'bbid'])
        data = {}
        for asset in response:
            data[get(asset, 'id')] = dict(name=get(asset, 'name'), bbid=get(asset, 'bbid'))
        return data
