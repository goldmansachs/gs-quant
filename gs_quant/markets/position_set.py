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
from typing import Dict, List, Union, Optional

import pandas as pd
from pydash import get

from gs_quant.api.gs.assets import GsAssetApi
from gs_quant.api.gs.price import GsPriceApi
from gs_quant.errors import MqValueError
from gs_quant.target.common import Position as CommonPosition, PositionPriceInput, PositionSet as CommonPositionSet, \
    PositionTag, Currency, PositionSetWeightingStrategy
from gs_quant.target.price import PriceParameters, PositionSetPriceInput

_logger = logging.getLogger(__name__)


class Position:
    def __init__(self,
                 identifier: str,
                 weight: float = None,
                 quantity: float = None,
                 name: str = None,
                 asset_id: str = None,
                 tags: Dict = None):
        self.__identifier = identifier
        self.__weight = weight
        self.__quantity = quantity
        self.__name = name
        self.__asset_id = asset_id
        self.__tags = tags

    def __eq__(self, other) -> bool:
        if not isinstance(other, Position):
            return False
        for prop in ['asset_id', 'weight', 'quantity', 'tags']:
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

    @property
    def tags(self) -> Dict:
        return self.__tags

    @tags.setter
    def tags(self, value: Dict):
        self.__tags = value

    def as_dict(self) -> Dict:
        position_dict = dict(identifier=self.identifier, weight=self.weight,
                             quantity=self.quantity, name=self.name, asset_id=self.asset_id, tags=self.tags)
        return {k: v for k, v in position_dict.items() if v is not None}

    def to_target(self, common: bool = True) -> Union[CommonPosition, PositionPriceInput]:
        """ Returns Postion type defined in target file for API payloads """
        if common:
            tags_as_target = tuple(PositionTag(name=key, value=self.tags[key]) for key in self.tags) if self.tags \
                else None
            return CommonPosition(self.asset_id, quantity=self.quantity, tags=tags_as_target)
        return PositionPriceInput(self.asset_id, quantity=self.quantity, weight=self.weight)


class PositionSet:
    """

    Position Sets hold a collection of positions associated with a particular date

    """

    def __init__(self,
                 positions: List[Position],
                 date: datetime.date = datetime.date.today(),
                 divisor: float = None,
                 reference_notional: float = None,
                 unresolved_positions: List[Position] = None,
                 unpriced_positions: List[Position] = None):
        if reference_notional is not None:
            for p in positions:
                if p.weight is None:
                    raise MqValueError('Position set with reference notionals must have weights for every position.')
                if p.quantity is not None:
                    raise MqValueError('Position sets with reference notionals cannot have positions with quantities.')
        self.__positions = positions
        self.__date = date
        self.__divisor = divisor
        self.__reference_notional = reference_notional
        self.__unresolved_positions = unresolved_positions if unresolved_positions is not None else []
        self.__unpriced_positions = unpriced_positions if unpriced_positions is not None else []

    def __eq__(self, other) -> bool:
        if len(self.positions) != len(other.positions):
            return False
        if self.date != other.date:
            return False
        if self.reference_notional != other.reference_notional:
            return False
        positions = self.positions
        positions.sort(key=lambda position: position.asset_id)
        other_positions = other.positions
        other_positions.sort(key=lambda position: position.asset_id)
        for i in range(0, len(positions)):
            if positions[i] != other_positions[i]:
                return False
        return True

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

    @property
    def reference_notional(self) -> float:
        return self.__reference_notional

    @reference_notional.setter
    def reference_notional(self, value: float):
        self.__reference_notional = value

    @property
    def unresolved_positions(self) -> List[Position]:
        return self.__unresolved_positions

    @property
    def unpriced_positions(self) -> List[Position]:
        return self.__unpriced_positions

    def get_positions(self) -> pd.DataFrame:
        """
        Retrieve formatted positions

        :return: DataFrame of positions for position set

        **Usage**

        View position set position info

        **Examples**

        Get position set positions:

        >>> from gs_quant.markets.position_set import Position, PositionSet
        >>>
        >>> my_positions = [Position(identifier='AAPL UW'), Position(identifier='MSFT UW')]
        >>> position_set = PositionSet(positions=my_positions)
        >>> position_set.get_positions()

        **See also**

        :func:`get_unresolved_positions` :func:`get_unpriced_positions` :func:`resolve` :func:`price`
        """
        positions = [p.as_dict() for p in self.positions]
        return pd.DataFrame(positions)

    def get_unresolved_positions(self) -> pd.DataFrame:
        """
        Retrieve formatted unresolved positions

        :return: DataFrame of unresolved positions for position set

        **Usage**

        View position set unresolved position info

        **Examples**

        Get position set unresolved positions:

        >>> from gs_quant.markets.position_set import Position, PositionSet
        >>>
        >>> my_positions = [Position(identifier='AAPL UW'), Position(identifier='MSFT UW')]
        >>> position_set = PositionSet(positions=my_positions)
        >>> position_set.resolve()
        >>> position_set.get_unresolved_positions()

        **See also**

        :func:`get_positions` :func:`get_unpriced_positions` :func:`resolve` :func:`price`
        """
        positions = [p.as_dict() for p in self.unresolved_positions]
        return pd.DataFrame(positions)

    def remove_unresolved_positions(self):
        """
        Remove unresolved positions from your position set

        **Usage**

        Remove unresolved positions from your position set

        **Examples**

        Remove unresolved positions from your position set:

        >>> from gs_quant.markets.position_set import Position, PositionSet
        >>>
        >>> my_positions = [Position(identifier='AAPL UW'), Position(identifier='MSFT UW')]
        >>> position_set = PositionSet(positions=my_positions)
        >>> position_set.resolve()
        >>> position_set.remove_unresolved_positions()

        **See also**

        :func:`get_positions` :func:`get_unpriced_positions` :func:`resolve` :func:`price`
        :func:`remove_unpriced_positions` :func:`get_unresolved_positions`
        """
        self.positions = [p for p in self.positions if p.asset_id is not None]
        self.__unresolved_positions = None

    def get_unpriced_positions(self) -> pd.DataFrame:
        """
        Retrieve formatted unpriced positions

        :return: DataFrame of unpriced positions for position set

        **Usage**

        View position set unpriced position info

        **Examples**

        Get position set unpriced positions:

        >>> import datetime as dt
        >>> from gs_quant.markets.position_set import Position, PositionSet
        >>>
        >>> my_positions = [Position(identifier='AAPL UW', quantity=100), Position(identifier='MSFT UW', quantity=100)]
        >>> position_set = PositionSet(positions=my_positions)
        >>> position_set.resolve()
        >>> position_set.price()
        >>> position_set.get_unpriced_positions()

        **See also**

        :func:`get_positions` :func:`get_unresolved_positions` :func:`resolve` :func:`price`
        """
        positions = [p.as_dict() for p in self.unpriced_positions]
        return pd.DataFrame(positions)

    def remove_unpriced_positions(self):
        """
        Remove unpriced positions from your position set

        **Usage**

        Remove unpriced positions from your position set

        **Examples**

        Remove unpriced positions from your position set:

        >>> from gs_quant.markets.position_set import Position, PositionSet
        >>>
        >>> my_positions = [Position(identifier='AAPL UW'), Position(identifier='MSFT UW')]
        >>> position_set = PositionSet(positions=my_positions)
        >>> position_set.resolve()
        >>> position_set.remove_unpriced_positions()

        **See also**

        :func:`get_positions` :func:`get_unpriced_positions` :func:`resolve` :func:`price`
        :func:`get_unresolved_positions` :func:`remove_unresolved_positions`
        """
        self.__unpriced_positions = None

    def equalize_position_weights(self):
        """
        Assigns equal weight to each position in position set

        **Usage**

        Assigns equal weight to each position in position set

        **Examples**

        Assign equal weight to each position in position set:

        >>> from gs_quant.markets.position_set import Position, PositionSet
        >>>
        >>> my_positions = [Position(identifier='AAPL UW'), Position(identifier='MSFT UW')]
        >>> position_set = PositionSet(positions=my_positions)
        >>> position_set.equalize_position_weights()

        **See also**

        :func:`get_positions` :func:`redistribute_weights`
        """
        weight = 1 / len(self.positions)
        equally_weighted_positions = []
        for p in self.positions:
            p.weight = weight
            p.quantity = None
            equally_weighted_positions.append(p)
        self.positions = equally_weighted_positions

    def to_frame(self) -> pd.DataFrame:
        """
        Retrieve formatted position set

        :return: DataFrame of position set info

        **Usage**

        View position set info

        **Examples**

        Retrieve formatted position set:

        >>> from gs_quant.markets.position_set import Position, PositionSet
        >>>
        >>> my_positions = [Position(identifier='AAPL UW', quantity=100), Position(identifier='MSFT UW', quantity=100)]
        >>> position_set = PositionSet(positions=my_positions)
        >>> position_set.get_unpriced_positions()

        **See also**

        :func:`from_frame` :func:`from_dicts` :func:`from_list`
        """
        positions = []
        for p in self.positions:
            position = dict(date=self.date.isoformat())
            if self.divisor is not None:
                position.update(dict(divisor=self.divisor))
            position.update(p.as_dict())
            positions.append(position)
        return pd.DataFrame(positions)

    def resolve(self, **kwargs):
        """
        Resolve any unmapped positions

        **Usage**

        Resolve any unmapped positions

        **Examples**

        Resolve any unmapped positions:

        >>> from gs_quant.markets.position_set import Position, PositionSet
        >>>
        >>> my_positions = [Position(identifier='AAPL UW'), Position(identifier='MSFT UW')]
        >>> position_set = PositionSet(positions=my_positions)
        >>> position_set.resolve()

        **See also**

        :func:`get_positions` :func:`get_unresolved_positions` :func:`get_unpriced_positions` :func:`price`
        """
        unresolved_positions = [p.identifier for p in self.positions if p.asset_id is None]
        if len(unresolved_positions):
            [id_map, unresolved_positions] = self.__resolve_identifiers(unresolved_positions, self.date, **kwargs)
            self.__unresolved_positions = [p for p in self.positions if p.identifier in unresolved_positions]
            resolved_positions = []
            for p in self.positions:
                if p.identifier in id_map:
                    asset = get(id_map, p.identifier.replace('.', '\.'))
                    p.asset_id = get(asset, 'id')
                    p.name = get(asset, 'name')
                if p.asset_id is not None:
                    resolved_positions.append(p)
            self.positions = resolved_positions

    def redistribute_weights(self):
        """
        Redistribute position weights proportionally for a one-sided position set

        **Usage**

        Redistribute position weights proportionally for a one-sided position set

        **Examples**

        Redistribute position weights proportionally for a one-sided position set:

        >>> from gs_quant.markets.position_set import Position, PositionSet
        >>>
        >>> my_positions = [Position(identifier='AAPL UW', weight=0.3), Position(identifier='MSFT UW', weight=0.3)]
        >>> position_set = PositionSet(positions=my_positions)
        >>> position_set.redistribute_weights()

        **See also**

        :func:`get_positions` :func:`equalize_position_weights` :func:`get_unpriced_positions` :func:`price`
        """
        total_weight = 0
        new_weights, unweighted = [], []
        for p in self.positions:
            if p.weight is None:
                unweighted.append(p.identifier)
            else:
                total_weight += p.weight
        if len(unweighted):
            raise MqValueError(f'Cannot reweight as some positions are missing weights: {unweighted}')

        weight_to_distribute = 1 - total_weight if total_weight < 0 else total_weight - 1
        for p in self.positions:
            p.weight = p.weight - (p.weight / total_weight) * weight_to_distribute
            p.quantity = None
            new_weights.append(p)
        self.positions = new_weights

    def price(self, currency: Optional[Currency] = Currency.USD,
              weighting_strategy: Optional[PositionSetWeightingStrategy] = None, **kwargs):
        """
        Fetch positions weights from quantities, or vice versa

        :param currency: Reference notional currency (defaults to USD if not passed in)
        :param weighting_strategy: Quantity or Weighted weighting strategy (defaults based on positions info)

        **Usage**

        Fetch positions weights from quantities, or vice versa

        **Examples**

        Fetch position weights from quantities:

        >>> from gs_quant.markets.position_set import Position, PositionSet, PositionSetWeightingStrategy
        >>>
        >>> my_positions = [Position(identifier='AAPL UW', quantity=100), Position(identifier='MSFT UW', quantity=100)]
        >>> position_set = PositionSet(positions=my_positions)
        >>> position_set.resolve()
        >>> position_set.price(weighting_strategy=PositionSetWeightingStrategy.Quantity)

        Fetch position quantities from weights:

        >>> import datetime as dt
        >>> from gs_quant.markets.position_set import Position, PositionSet
        >>>
        >>> my_positions = [Position(identifier='AAPL UW', weight=0.5), Position(identifier='MSFT UW', weight=0.5)]
        >>> position_set = PositionSet(positions=my_positions, date= dt.date(2023, 3, 16), reference_notional=10000000)
        >>> position_set.resolve()
        >>> position_set.price(weighting_strategy=PositionSetWeightingStrategy.Weight)

        **See also**

        :func:`get_unpriced_positions` :func:`get_unresolved_positions` :func:`resolve`
        """
        weighting_strategy = self.__get_default_weighting_strategy(self.positions,
                                                                   self.reference_notional,
                                                                   weighting_strategy)
        positions = self.__convert_positions_for_pricing(self.positions, weighting_strategy)
        price_parameters = PriceParameters(currency=currency,
                                           divisor=self.divisor,
                                           asset_data_set_id='GSEOD',
                                           target_notional=self.reference_notional,
                                           notional_type='Gross',
                                           pricing_date=self.date,
                                           price_regardless_of_assets_missing_prices=True,
                                           weighting_strategy=weighting_strategy)
        for k, v in kwargs.items():
            price_parameters[k] = v
        results = GsPriceApi.price_positions(PositionSetPriceInput(positions=positions, parameters=price_parameters))
        position_result_map = {p.asset_id: p for p in results.positions}
        priced_positions, unpriced_positions = [], []
        for p in self.positions:
            if p.asset_id in position_result_map:
                p.weight = position_result_map.get(p.asset_id).weight
                p.quantity = position_result_map.get(p.asset_id).quantity
                priced_positions.append(p)
            else:
                unpriced_positions.append(p)
        self.positions = priced_positions
        self.__unpriced_positions = unpriced_positions

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
            tags = {t.name: t.value for t in p.tags} if p.tags else None
            position = Position(identifier=get(asset, 'bbid'), name=get(asset, 'name'),
                                asset_id=p.asset_id, quantity=p.quantity, tags=tags)
            converted_positions.append(position)
        return cls(converted_positions, position_set.position_date, position_set.divisor)

    @classmethod
    def from_list(cls, positions: List[str], date: datetime.date = datetime.date.today()):
        """
        Create equally-weighted PostionSet instance from a list of identifiers

        **Usage**

        Create equally-weighted PostionSet instance from a list of identifiers

        **Examples**

        Create equally-weighted PostionSet instance from a list of identifiers:

        >>> from gs_quant.markets.position_set import PositionSet
        >>>
        >>> identifiers = ['AAPL UW', 'MSFT UW']
        >>> position_set = PositionSet.from_list(positions=identifiers)

        **See also**

        :func:`get_positions` :func:`resolve` :func:`from_dicts` :func:`from_frame` :func:`to_frame`
        """
        weight = 1 / len(positions)
        converted_positions = [Position(identifier=p, weight=weight) for p in positions]
        return cls(converted_positions, date)

    @classmethod
    def from_dicts(cls, positions: List[Dict],
                   date: datetime.date = datetime.date.today(),
                   reference_notional: float = None):
        """
        Create PostionSet instance from a list of position-object-like dictionaries

        **Usage**

        Create PostionSet instance from a list of position-object-like dictionaries

        **Examples**

        Create PostionSet instance from a list of position-object-like dictionaries:

        >>> from gs_quant.markets.position_set import PositionSet
        >>>
        >>> my_positions = [{'identifier': 'AAPL UW', 'weight': 0.5}, {'identifier': 'AAPL UW', 'weight': 0.5}]
        >>> position_set = PositionSet.from_dicts(positions=my_positions)

        **See also**

        :func:`get_positions` :func:`resolve` :func:`from_list` :func:`from_frame` :func:`to_frame`
        """
        positions_df = pd.DataFrame(positions)
        return cls.from_frame(positions_df, date, reference_notional)

    @classmethod
    def from_frame(cls,
                   positions: pd.DataFrame,
                   date: datetime.date = datetime.date.today(),
                   reference_notional: float = None,
                   add_tags: bool = False):
        """
        Create PostionSet instance from a dataframe of positions

        **Usage**

        Create PostionSet instance from a dataframe of positions

        **Examples**

        Create PostionSet instance from a dataframe of positions:

        >>> import pandas as pd
        >>> from gs_quant.markets.position_set import PositionSet
        >>>
        >>> my_positions = [{'identifier': 'AAPL UW', 'weight': 0.5}, {'identifier': 'AAPL UW', 'weight': 0.5}]
        >>> positions_df = pd.DataFrame(my_positions)
        >>> position_set = PositionSet.from_frame(positions=positions_df)

        **See also**

        :func:`get_positions` :func:`resolve` :func:`from_list` :func:`from_dicts` :func:`to_frame`
        """
        positions.columns = cls.__normalize_position_columns(positions)
        tag_columns = cls.__get_tag_columns(positions) if add_tags else []
        positions = positions[~positions['identifier'].isnull()]
        equalize = not ('quantity' in positions.columns.str.lower() or 'weight' in positions.columns.str.lower())
        equal_weight = 1 / len(positions)

        positions_list = []
        for i, row in positions.iterrows():
            positions_list.append(
                Position(
                    identifier=row.get('identifier'),
                    asset_id=row.get('id'),
                    name=row.get('name'),
                    weight=equal_weight if equalize else row.get('weight'),
                    quantity=None if equalize else row.get('quantity'),
                    tags={tag: get(row, tag) for tag in tag_columns} if len(tag_columns) else None
                )
            )

        return cls(positions_list, date, reference_notional=reference_notional)

    @staticmethod
    def __get_tag_columns(positions: pd.DataFrame) -> List[str]:
        return [c for c in positions.columns if c.lower() not in ['identifier', 'quantity', 'weight', 'date']]

    @staticmethod
    def __normalize_position_columns(positions: pd.DataFrame) -> List[str]:
        columns = []
        for c in positions.columns:
            columns.append(c.lower() if c.lower() in ['identifier', 'quantity', 'weight', 'date'] else c)
        return columns

    @staticmethod
    def __resolve_identifiers(identifiers: List[str], date: datetime.date, **kwargs) -> List:
        response = GsAssetApi.resolve_assets(
            identifier=identifiers,
            fields=['name', 'id'],
            limit=1,
            as_of=date,
            **kwargs
        )
        unmapped_assets = []
        id_map = {}

        for identifier in response:
            if len(response[identifier]) > 0:
                id_map[identifier] = {'id': response[identifier][0]['id'], 'name': response[identifier][0]['name']}
            else:
                unmapped_assets.append(identifier)

        if len(unmapped_assets) > 0:
            logging.info(f'Error in resolving the following identifiers: {unmapped_assets}. Sifting them out and '
                         f'resolving the rest...')

        return [id_map, unmapped_assets]

    @staticmethod
    def __get_positions_data(mqids: List[str]) -> Dict:
        response = GsAssetApi.get_many_assets_data(id=mqids, fields=['id', 'name', 'bbid'])
        data = {}
        for asset in response:
            data[get(asset, 'id')] = dict(name=get(asset, 'name'), bbid=get(asset, 'bbid'))
        return data

    @staticmethod
    def __get_default_weighting_strategy(positions: List[Position],
                                         reference_notional: float = None,
                                         weighting_strategy: Optional[PositionSetWeightingStrategy] = None
                                         ) -> PositionSetWeightingStrategy:
        missing_weights = [p.identifier for p in positions if p.weight is None]
        missing_quantities = [p.identifier for p in positions if p.quantity is None]
        if weighting_strategy is None:
            if len(missing_weights) and len(missing_quantities):
                raise MqValueError(f'Unable to determine weighting strategy due to missing weights for \
                {missing_weights} and missing quantities for {missing_quantities}')
            if not len(missing_weights) and (reference_notional is not None or len(missing_quantities)):
                weighting_strategy = PositionSetWeightingStrategy.Weight
            else:
                weighting_strategy = PositionSetWeightingStrategy.Quantity
        use_weight = weighting_strategy == PositionSetWeightingStrategy.Weight
        if (use_weight and len(missing_weights)) or (not use_weight and len(missing_quantities)):
            raise MqValueError(f'You must input a {weighting_strategy.value} for the following positions: \
            {missing_weights if use_weight else missing_quantities}')
        if use_weight and reference_notional is None:
            raise MqValueError('You must specify a reference notional in order to price by weight.')
        return weighting_strategy

    @staticmethod
    def __convert_positions_for_pricing(positions: List[Position],
                                        weighting_strategy: PositionSetWeightingStrategy) -> List[PositionPriceInput]:
        position_inputs, missing_ids = [], []
        use_weight = weighting_strategy == PositionSetWeightingStrategy.Weight
        for p in positions:
            if p.asset_id is None:
                missing_ids.append(p.identifier)
            else:
                position_inputs.append(PositionPriceInput(asset_id=p.asset_id,
                                                          weight=p.weight if use_weight else None,
                                                          quantity=None if use_weight else p.quantity))
        if len(missing_ids):
            raise MqValueError(f'Positions: {missing_ids} are missing asset ids. Resolve your position \
            set or remove unmapped identifiers.')
        return position_inputs
