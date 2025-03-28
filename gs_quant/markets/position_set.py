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
import datetime as dt
import logging
import math
from time import time
from typing import Dict, List, Union, Optional

import numpy as np
import pandas as pd
from pydash import get

from gs_quant.api.gs.assets import GsAssetApi
from gs_quant.api.gs.price import GsPriceApi
from gs_quant.errors import MqValueError, MqRequestError
from gs_quant.markets.position_set_utils import _get_asset_temporal_xrefs, \
    _group_temporal_xrefs_into_discrete_time_ranges, _resolve_many_assets
from gs_quant.models.risk_model_utils import _repeat_try_catch_request
from gs_quant.target.common import Position as CommonPosition, PositionPriceInput, PositionSet as CommonPositionSet, \
    PositionTag as PositionTagTarget, Currency, PositionSetWeightingStrategy, MarketDataFrequency
from gs_quant.target.positions_v2_pricing import PositionsPricingParameters, PositionsRequest, PositionSetRequest, \
    PositionsPricingRequest
from gs_quant.target.price import PriceParameters, PositionSetPriceInput, PositionPriceResponse

_logger = logging.getLogger(__name__)


class PositionTag(PositionTagTarget):
    @classmethod
    def from_dict(cls, tag_dict: Dict):
        if len(tag_dict) > 1:
            raise MqValueError('PositionTag.from_dict only accepts a single key-value pair')
        return cls(name=list(tag_dict.keys())[0], value=list(tag_dict.values())[0])


class Position:
    def __init__(self,
                 identifier: str,
                 weight: float = None,
                 quantity: float = None,
                 name: str = None,
                 asset_id: str = None,
                 tags: Optional[List[Union[PositionTag, Dict]]] = None):
        self.__identifier = identifier
        self.__weight = weight
        self.__quantity = quantity
        self.__name = name
        self.__asset_id = asset_id
        if tags is not None:
            self.__tags = [PositionTag.from_dict(tag) if isinstance(tag, dict) else tag for tag in tags]
        else:
            self.__tags = tags
        self.__restricted, self.__hard_to_borrow = None, None

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
    def tags(self) -> List[PositionTag]:
        return self.__tags

    @tags.setter
    def tags(self, value: List[PositionTag]):
        self.__tags = value

    @property
    def hard_to_borrow(self) -> bool:
        return self.__hard_to_borrow

    @hard_to_borrow.setter
    def _hard_to_borrow(self, value: bool):
        self.__hard_to_borrow = value

    @property
    def restricted(self) -> bool:
        return self.__restricted

    @restricted.setter
    def _restricted(self, value: bool):
        self.__restricted = value

    def add_tag(self, name: str, value: str):
        if self.tags is None:
            self.tags = []
        if not any(tag.name == name for tag in self.tags):
            self.tags.append(PositionTag(name=name, value=value))
        else:
            raise MqValueError(f'Position already has tag with name {name}')

    def tags_as_dict(self):
        return {tag.name: tag.value for tag in self.tags}

    def as_dict(self, tags_as_keys: bool = False) -> Dict:
        position_dict = dict(identifier=self.identifier, weight=self.weight,
                             quantity=self.quantity, name=self.name, asset_id=self.asset_id, restricted=self.restricted)
        if self.tags and tags_as_keys:
            position_dict.update(self.tags_as_dict())
        else:
            position_dict['tags'] = self.tags
        return {k: v for k, v in position_dict.items() if v is not None}

    @classmethod
    def from_dict(cls, position_dict: Dict, add_tags: bool = True):
        fields = [k.lower() for k in position_dict.keys()]
        if 'id' in fields and 'asset_id' in fields:
            raise MqValueError('Position cannot have both id and asset_id')
        if 'id' in fields:
            position_dict['asset_id'] = position_dict.pop('id')
        position_fields = ['identifier', 'weight', 'quantity', 'name', 'asset_id']
        tag_dict = {k: v for k, v in position_dict.items() if k not in position_fields}
        return cls(
            identifier=position_dict['identifier'],
            weight=position_dict.get('weight'),
            quantity=position_dict.get('quantity'),
            name=position_dict.get('name'),
            asset_id=position_dict.get('asset_id'),
            tags=[PositionTag(name=k, value=v) for k, v in tag_dict.items()] if add_tags else position_dict.get('tags')
        )

    def clone(self):
        return Position.from_dict(self.as_dict(tags_as_keys=True), add_tags=True)

    def to_target(self, common: bool = True) -> Union[CommonPosition, PositionPriceInput]:
        """ Returns Position type defined in target file for API payloads """
        if common:
            tags_as_target = self.tags if self.tags else None
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

    def clone(self, keep_reference_notional: bool = False):
        """Create a clone of the current position set

        :param keep_reference_notional: Whether to keep the reference notional of the original position set in case it
        has both quantity and reference notional
        """
        frame = self.to_frame(add_tags=True)
        ref_notional = self.reference_notional
        if 'quantity' in frame.columns and ref_notional is not None:
            if keep_reference_notional:
                frame = frame.drop(columns=['quantity'])
            else:
                ref_notional = None
        return PositionSet.from_frame(
            frame,
            date=self.date,
            reference_notional=ref_notional,
            divisor=self.divisor,
            add_tags=True
        )

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

    def get_restricted_positions(self) -> pd.DataFrame:
        """
        Retrieve formatted RTL positions

        :return: DataFrame of RTL positions for position set

        **Usage**

        View position set RTL position info

        **Examples**

        Get position set RTL positions:

        >>> import datetime as dt
        >>> from gs_quant.markets.position_set import Position, PositionSet
        >>>
        >>> my_positions = [Position(identifier='AAPL UW', quantity=100), Position(identifier='MSFT UW', quantity=100)]
        >>> position_set = PositionSet(positions=my_positions)
        >>> position_set.resolve()
        >>> position_set.get_restricted_positions()

        **See also**

        :func:`get_positions` :func:`resolve` :func:`price` :func:`remove_restricted_positions`
        :func:`get_hard_to_borrow_positions` :func:`remove_hard_to_borrow_positions`
        """
        positions = [p.as_dict() for p in self.positions if p.restricted]
        return pd.DataFrame(positions)

    def remove_restricted_positions(self):
        """
        Remove RTL positions from your position set

        **Usage**

        Remove RTL positions from your position set

        **Examples**

        Remove RTL positions from your position set:

        >>> from gs_quant.markets.position_set import Position, PositionSet
        >>>
        >>> my_positions = [Position(identifier='AAPL UW'), Position(identifier='MSFT UW')]
        >>> position_set = PositionSet(positions=my_positions)
        >>> position_set.resolve()
        >>> position_set.remove_restricted_positions()

        **See also**

        :func:`get_positions` :func:`resolve` :func:`price` :func:`get_restricted_positions`
        :func:`get_hard_to_borrow_positions` :func:`remove_hard_to_borrow_positions`
        """
        self.positions = [p for p in self.positions if p.restricted is not True]

    def get_hard_to_borrow_positions(self) -> pd.DataFrame:
        """
        Retrieve formatted htb positions

        :return: DataFrame of htb positions for position set

        **Usage**

        View position set htb position info

        **Examples**

        Get position set htb positions:

        >>> import datetime as dt
        >>> from gs_quant.markets.position_set import Position, PositionSet
        >>>
        >>> my_positions = [Position(identifier='AAPL UW', quantity=100), Position(identifier='MSFT UW', quantity=100)]
        >>> position_set = PositionSet(positions=my_positions)
        >>> position_set.resolve()
        >>> position_set.price()
        >>> position_set.get_hard_to_borrow_positions()

        **See also**

        :func:`get_positions` :func:`resolve` :func:`price` :func:`get_restricted_positions`
        :func:`remove_restricted_positions` :func:`remove_hard_to_borrow_positions`
        """
        positions = [p.as_dict() for p in self.positions if p.hard_to_borrow]
        return pd.DataFrame(positions)

    def remove_hard_to_borrow_positions(self):
        """
        Remove hard to borrow positions from your position set

        **Usage**

        Remove hard to borrow positions from your position set

        **Examples**

        Remove hard to borrow positions from your position set:

        >>> from gs_quant.markets.position_set import Position, PositionSet
        >>>
        >>> my_positions = [Position(identifier='AAPL UW'), Position(identifier='MSFT UW')]
        >>> position_set = PositionSet(positions=my_positions)
        >>> position_set.resolve()
        >>> position_set.price()
        >>> position_set.remove_hard_to_borrow_positions()

        **See also**

        :func:`get_positions` :func:`resolve` :func:`price` :func:`get_restricted_positions`
        :func:`remove_restricted_positions` :func:`get_hard_to_borrow_positions`
        """
        self.positions = [p for p in self.positions if p.hard_to_borrow is not True]

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

    def to_frame(self, add_tags: bool = False) -> pd.DataFrame:
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
        >>> position_set.to_frame()

        Retrieve tags in the pd DataFrame:

        >>> from gs_quant.markets.position_set import PositionSet
        >>> pset = PositionSet.from_dicts([
        >>>     {'identifier': 'AAPL UW', 'quantity': 100, 'MyTag': 'Name 1'},
        >>>     {'identifier': 'AAPL UW', 'quantity': 100, 'MyTag': 'Name 2'},
        >>>     {'identifier': 'META UW', 'quantity': 100, 'MyTag': 'Name 1'}
        >>> ], add_tags=True)
        >>> pset.to_frame(add_tags=True)

        **See also**

        :func:`from_frame` :func:`from_dicts` :func:`from_list`
        """
        positions = []
        for p in self.positions:
            position = dict(date=self.date.isoformat())
            if self.divisor is not None:
                position.update(dict(divisor=self.divisor))
            position.update(p.as_dict(tags_as_keys=add_tags))
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
                    asset = get(id_map, p.identifier.replace('.', '\\.'))
                    p.asset_id = get(asset, 'id')
                    p.name = get(asset, 'name')
                    p._restricted = get(asset, 'restricted')
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
              use_unadjusted_close_price: bool = True,
              weighting_strategy: Optional[PositionSetWeightingStrategy] = None,
              handle_long_short: bool = False,
              fail_on_unpriced_positions: bool = False,
              **kwargs):
        """
        Fetch positions weights from quantities, or vice versa

        :param currency: Reference notional currency (defaults to USD if not passed in)
        :param use_unadjusted_close_price: Use adjusted or unadjusted close prices (defaults to unadjusted)
        :param weighting_strategy: Quantity or Weighted weighting strategy (defaults based on positions info)
        :param handle_long_short: Whether to handle the loss of directionality in weights that comes from pricing using
        gross notional. Useful when input position iset is a long/short. Note, this also sets the reference notional to
        Gross Notional if not already so
        :param fail_on_unpriced_positions: Whether to raise an exception if any positions are unpriced
        :param kwargs: Additional parameters to pass to the pricing API

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
                                           frequency=MarketDataFrequency.End_Of_Day,
                                           target_notional=self.reference_notional,
                                           notional_type='Gross',
                                           pricing_date=self.date,
                                           price_regardless_of_assets_missing_prices=True,
                                           weighting_strategy=weighting_strategy,
                                           use_unadjusted_close_price=use_unadjusted_close_price)

        if 'dataset' in kwargs:
            price_parameters.asset_data_set_id = kwargs['dataset']
            price_parameters.frequency = None

        for k, v in kwargs.items():
            price_parameters.__setattr__(k, v)
        results = GsPriceApi.price_positions(PositionSetPriceInput(positions=positions, parameters=price_parameters))
        position_result_map = {f'{p.asset_id}{self.__hash_position_tag_list(p.tags)}': p for p in results.positions}
        priced_positions, unpriced_positions = [], []
        for p in self.positions:
            asset_key = f'{p.asset_id}{self.__hash_position_tag_list(p.tags)}'
            if asset_key in position_result_map:
                pos: PositionPriceResponse = position_result_map.get(asset_key)
                p.quantity = pos.quantity
                w = pos.weight
                if handle_long_short:
                    # In case of long/short positions, we need to convert the returned gross weight to reference weight
                    w = math.copysign(w, pos.notional)
                p.weight = w
                p._hard_to_borrow = pos.hard_to_borrow
                priced_positions.append(p)
            else:
                unpriced_positions.append(p)

        if fail_on_unpriced_positions and unpriced_positions:
            raise MqValueError(f'Failed to price positions: '
                               f'{", ".join([p.identifier for p in unpriced_positions])} on {self.date}. Please'
                               f'contat Marquee Support for assistance.')
        self.positions = priced_positions
        self.__unpriced_positions = unpriced_positions
        if handle_long_short:
            # Set notional to gross notional because in case of L/S pricing the API normalizes all weights wrt gross
            self.reference_notional = results.gross_notional

    def get_subset(self, copy: bool = True, **kwargs):
        """Extract a subset of the position set based on values of tags.

        Not that weights are returned with respect to original position set. Use redistribute_weights function.
        For more advanced filtering, use .to_frame() to get the frame as a pandas DataFrame.

        **Usage**
        Given a position set that has tags, extract a subset of the positions based on the values of one or more of the
        tags.

        **Examples**
        Extract a subset of the position set based on the value of a single tag:

        >>> from gs_quant.markets.position_set import Position, PositionSet
        >>> from gs_quant.target.common import PositionTag
        >>> pset = PositionSet.from_dicts([
        >>>     {'identifier': 'AAPL UW', 'quantity': 1000, 'MyTag': 'Name 1', 'MyOtherTag': 'Class 1'},
        >>>     {'identifier': 'MSFT UW', 'quantity': 2000, 'MyTag': 'Name 2', 'MyOtherTag': 'Class 1'},
        >>>     {'identifier': 'GOOGL UW', 'quantity': 3000, 'MyTag': 'Name 1', 'MyOtherTag': 'Class 2'}
        >>> ])
        >>>
        >>> subset = pset.get_subset(MyTag='Name 1')

        Extract a subset of the position set based on the values of multiple tags:

        >>> subset = pset.get_subset(MyTag='Name 1', MyOtherTag='Class 2')

        """
        subset = []
        for p in self.positions:
            if not p.tags:
                raise MqValueError(f'PositionSet has position {p.identifier} that does not have tags')
            tags_dict = p.tags_as_dict()
            if all(tags_dict.get(k) == v for k, v in kwargs.items()):
                subset.append(p if not copy else p.clone())
        return PositionSet(positions=subset, date=self.date, reference_notional=self.reference_notional)

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
            tags = p.tags if p.tags else None
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
                   reference_notional: float = None,
                   add_tags: bool = False):
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
        return cls.from_frame(positions_df, date, reference_notional, add_tags=add_tags)

    @classmethod
    def from_frame(cls,
                   positions: pd.DataFrame,
                   date: datetime.date = datetime.date.today(),
                   reference_notional: float = None,
                   divisor: float = None,
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
        for row in positions.to_dict(orient='records'):
            positions_list.append(
                Position(
                    identifier=row.get('identifier'),
                    asset_id=row.get('id'),
                    name=row.get('name'),
                    weight=equal_weight if equalize else row.get('weight'),
                    quantity=None if equalize else row.get('quantity'),
                    tags=list(PositionTag(tag, get(row, tag)) for tag in tag_columns) if len(tag_columns) else None
                )
            )

        return cls(positions_list, date, reference_notional=reference_notional, divisor=divisor)

    @staticmethod
    def __get_tag_columns(positions: pd.DataFrame) -> List[str]:
        return [c for c in positions.columns if c.lower() not in
                ['identifier', 'id', 'quantity', 'weight', 'date', 'restricted']]

    @staticmethod
    def __normalize_position_columns(positions: pd.DataFrame) -> List[str]:
        columns = []
        if 'asset_id' in positions.columns and 'id' not in positions.columns:
            positions = positions.rename(columns={'asset_id': 'id'})
        for c in positions.columns:
            columns.append(
                c.lower() if c.lower() in ['identifier', 'id', 'quantity', 'weight', 'date', 'restricted'] else c
            )
        return columns

    @staticmethod
    def __resolve_identifiers(identifiers: List[str], date: datetime.date, **kwargs) -> List:
        unmapped_assets = []
        id_map = {}
        batch_size = 500
        logging.debug(f'Resolving positions in {len(identifiers) / batch_size} batches')
        for i in range(0, len(identifiers), batch_size):
            identifier_batch = identifiers[i: i + batch_size]
            response = GsAssetApi.resolve_assets(
                identifier=identifier_batch,
                fields=['name', 'id', 'tradingRestriction'],
                limit=1,
                as_of=date,
                **kwargs
            )

            for identifier in response:
                if response[identifier] is not None and len(response[identifier]) > 0:
                    id_map[identifier] = {'id': response[identifier][0]['id'],
                                          'name': response[identifier][0]['name'],
                                          'restricted': response[identifier][0].get('tradingRestriction')}
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
                                                          quantity=None if use_weight else p.quantity,
                                                          tags=p.tags))
        if len(missing_ids):
            raise MqValueError(f'Positions: {missing_ids} are missing asset ids. Resolve your position \
            set or remove unmapped identifiers.')
        return position_inputs

    @staticmethod
    def __hash_position_tag_list(position_tags: List[PositionTag]) -> str:
        hashed_results = ''
        if position_tags is not None:
            for tag in position_tags:
                hashed_results = hashed_results + tag.name + '-' + tag.value
        return hashed_results

    @staticmethod
    def to_frame_many(position_sets: List['PositionSet']) -> pd.DataFrame:
        """Returns dataframe of position sets"""
        position_sets = pd.DataFrame(position_sets, columns=["position_sets"])

        for field in ['date', 'divisor', 'reference_notional']:
            position_sets[field] = [getattr(pos, field, None) for pos in position_sets['position_sets']]

        position_sets['positions'] = [pos.positions for pos in position_sets['position_sets']]

        position_sets = position_sets[position_sets['positions'].apply(lambda x: len(x) > 0)]

        position_sets = position_sets.explode('positions')
        position_sets['positions'] = [pos.as_dict() for pos in position_sets['positions']]

        for field in ['name', 'asset_id', 'identifier', 'weight', 'restricted', 'quantity', 'tags']:
            position_sets[field] = [pos.get(field) for pos in position_sets['positions']]

        columns_to_drop = ["position_sets", "positions"]
        position_sets.drop(columns=columns_to_drop, inplace=True)
        return position_sets

    @staticmethod
    @np.vectorize
    def __build_positions_from_frame(names: pd.Series = None,
                                     identifiers: pd.Series = None,
                                     asset_ids: pd.Series = None,
                                     weights: pd.Series = None,
                                     quantities: pd.Series = None,
                                     restricted: pd.Series = None,
                                     hard_to_borrow: pd.Series = None,
                                     tags: pd.Series = None):
        position = Position(asset_id=asset_ids,
                            name=names,
                            identifier=identifiers,
                            weight=weights if weights else None,
                            quantity=quantities if quantities else None,
                            tags=tags)

        position._restricted = restricted
        position._hard_to_borrow = hard_to_borrow

        return position

    @classmethod
    def resolve_many(cls, position_sets: List['PositionSet'], **kwargs):
        """
        Resolve positions on each holding date into Marquee assets. Positions sets will be updated inplace.
        Each resolved position will have a unique Marquee ID.

            :param position_sets: Positions sets in a list.
            :param kwargs: Additional parameters to send to the GS Resolver API.

            **Usage**

            >>> from gs_quant.markets.position_set import PositionSet, Position, PositionTag
            >>> import datetime as dt
            >>> import pandas as pd

            The input to the function can be a list of `PositionSet` object.

            >>> position_set_list = [
            ...          PositionSet(date=dt.date(2024, 5, 1),
            ...                      reference_notional=1000,
            ...                      positions=[Position(identifier='GS UN',
            ...                                          weight=0.5,
            ...                                          tags=[PositionTag(name="tag1", value="tagvalue1")]),
            ...                                 Position(identifier='AAPL UW',
            ...                                          weight=0.5,
            ...                                          ags=[PositionTag(name="tag2", value="tagvalue2")])]),
            ...          PositionSet(date=dt.date(2024, 5, 1),
            ...                      reference_notional=1000,
            ...                      positions=[Position(identifier='GS UN',
            ...                                          weight=0.5,
            ...                                          tags=[PositionTag(name="tag1", value="tagvalue1")]),
            ...                                 Position(identifier='AAPL UW',
            ...                                           weight=0.5,
            ...                                           tags=[PositionTag(name="tag2", value="tagvalue2")])])
            ...                        ]

            >>> PositionSet.resolve_many(position_set_list)

            **See also**

            :func:`price_many`

            """

        position_sets_df = cls.to_frame_many(position_sets)
        if "name" in position_sets_df.columns.tolist():
            position_sets_df = position_sets_df.drop(columns="name")
        if "asset_id" in position_sets_df.columns.tolist():
            position_sets_df = position_sets_df.drop(columns="asset_id")
        position_sets_df = position_sets_df.dropna(how='all', axis=1)

        position_sets_attributes = position_sets_df.columns.tolist()
        if "quantity" in position_sets_attributes and "weight" in position_sets_attributes:
            raise MqValueError("Cannot have both weight and quantity in position sets")

        asset_temporal_xrefs_df, asset_identifier_type = \
            _get_asset_temporal_xrefs(position_sets_df)
        _group_temporal_xrefs_into_discrete_time_ranges(asset_temporal_xrefs_df)
        resolved_assets_results_df = _resolve_many_assets(asset_temporal_xrefs_df, asset_identifier_type, **kwargs)

        position_sets_df = pd.merge(position_sets_df,
                                    resolved_assets_results_df[["assetId", asset_identifier_type, "name", "asOfDate",
                                                                "tradingRestriction", "startDate", "endDate"]],
                                    how="left",
                                    left_on="identifier",
                                    right_on=asset_identifier_type)
        position_sets_df["date"] = pd.to_datetime(position_sets_df["date"])

        # Fill N/A for startDate and endDate so they are not filtered out (for instance if some positions
        # did not have xrefs or were not resolved. These should be included in the unresolved positions group"
        position_sets_df['startDate'] = position_sets_df['startDate'].fillna(position_sets_df['date'])
        position_sets_df['endDate'] = position_sets_df['endDate'].fillna(position_sets_df['date'])

        position_sets_df = position_sets_df[(position_sets_df["startDate"] <= position_sets_df["date"]) &
                                            (position_sets_df["date"] <= position_sets_df["endDate"])]
        position_sets_df = (
            position_sets_df.drop(columns=[asset_identifier_type, "asOfDate", "startDate", "endDate"])
                            .rename(columns={"tradingRestriction": "restricted"})
                            .fillna(np.nan)
                            .replace([np.nan], [None])
        )

        # Build position sets
        if 'reference_notional' in position_sets_df.columns.tolist():
            if "quantity" in position_sets_df.columns.tolist():
                position_sets_df = position_sets_df.drop(columns='quantity')

        weights_df = position_sets_df['weight'] \
            if 'weight' in position_sets_df.columns.tolist() else None
        quantities_df = position_sets_df['quantity'] \
            if 'quantity' in position_sets_df.columns.tolist() else None
        tags_df = position_sets_df['tags'] if 'tags' in position_sets_df.columns.tolist() else None

        all_positions = cls.__build_positions_from_frame(names=position_sets_df['name'],
                                                         identifiers=position_sets_df['identifier'],
                                                         asset_ids=position_sets_df['assetId'],
                                                         weights=weights_df,
                                                         quantities=quantities_df,
                                                         restricted=position_sets_df['restricted'],
                                                         tags=tags_df)

        position_sets_df['positions'] = all_positions
        position_sets_grouped_by_date = position_sets_df.groupby('date')
        for position_set in position_sets:
            if not isinstance(position_set.date, dt.date):
                position_set.date = pd.Timestamp(position_set.date).to_pydatetime().date()
            positions_on_holding_date_df = position_sets_grouped_by_date.get_group(position_set.date)
            position_set.positions = positions_on_holding_date_df.loc[~positions_on_holding_date_df['assetId'].isnull(),
                                                                      'positions'].tolist()
            unresolved_positions = positions_on_holding_date_df.loc[positions_on_holding_date_df['assetId'].isnull(),
                                                                    'positions'].tolist()
            if unresolved_positions:
                position_set.__unresolved_positions = unresolved_positions

    @classmethod
    def price_many(cls,
                   position_sets: List['PositionSet'],
                   currency: Optional[Currency] = Currency.USD,
                   weighting_strategy: PositionSetWeightingStrategy = None,
                   carryover_positions_for_missing_dates: bool = False,
                   should_reweight: bool = False,
                   allow_fractional_shares: bool = False,
                   allow_partial_pricing: bool = False,
                   batch_size: int = 20,
                   **kwargs):
        """Fetch position weights from quantities or vice versa for a list of position sets. This function modifies the
         input position sets inplace

            :param position_sets: Positions sets in a list.
            :param currency: Currency to use to price. Defaults to USD.
            :param weighting_strategy: The weighting strategy to use. Should be weight or quantity. If None, infers
            weighting strategy from positions metadata
            :param carryover_positions_for_missing_dates: Broadcast previous positions onto dates with missing
            positions. Defaults to False
            :param should_reweight: Ensures total weight across positions on a holding date equals 1. Defaults to False
            :param allow_fractional_shares: Whether to allow fractional shares. Defaults to False
            :param allow_partial_pricing: whether to price a subset of positions in case of errors
            :param batch_size: Size of position sets to send to the pricing API per request. Defaults to 30
            :param kwargs: Additional parameters to pass to the GS pricing API

            **Usage**

            The function expects a required input of positions sets, which can be a dataframe of the format below or
            a list of `PositionSet` object

            >>> from gs_quant.markets.position_set import PositionSet, Position, PositionTag
            >>> import datetime as dt
            >>> import pandas as pd

            The input to the function is a list of `PositoinSet`

            >>> position_set_list = [
            ...     PositionSet(date=dt.date(2024, 5, 1),
            ...                 reference_notional=1000,
            ...                 positions=[Position(identifier='GS UN',
            ...                                      weight=0.5,
            ...                                      tags=[PositionTag(name="tag1", value="tagvalue1")]),
            ...                            Position(identifier='AAPL UW',
            ...                                     weight=0.5,
            ...                                     tags=[PositionTag(name="tag2", value="tagvalue2")])]),
            ...     PositionSet(date=dt.date(2024, 5, 1),
            ...                 reference_notional=1000,
            ...                 positions=[Position(identifier='GS UN',
            ...                                     weight=0.5,
            ...                                     tags=[PositionTag(name="tag1", value="tagvalue1")]),
            ...                            Position(identifier='AAPL UW',
            ...                                     weight=0.5,
            ...                                     tags=[PositionTag(name="tag2", value="tagvalue2")])])
            ...                        ]

            >>> PositionSet.price_many(position_set_list)

            :func:`resolve_many`

            """
        position_sets_to_price_df = cls.to_frame_many(position_sets)
        position_sets_to_price_df = position_sets_to_price_df.dropna(how='all', axis=1)
        position_sets_column_attributes = position_sets_to_price_df.columns.tolist()

        if "quantity" in position_sets_column_attributes and "weight" in position_sets_column_attributes:
            raise MqValueError("Cannot have both weight and quantity in position sets")

        if not weighting_strategy:
            weighting_strategy = PositionSetWeightingStrategy.Weight \
                if "weight" in position_sets_column_attributes \
                   and "reference_notional" in position_sets_column_attributes \
                else PositionSetWeightingStrategy.Quantity

        if weighting_strategy not in [PositionSetWeightingStrategy.Quantity, PositionSetWeightingStrategy.Weight]:
            raise MqValueError("Can only specify a weighting strategy of weight or quantity")

        if weighting_strategy == PositionSetWeightingStrategy.Quantity and \
                "quantity" not in position_sets_column_attributes:
            raise MqValueError("Unable to price positions without position weights and daily reference notional "
                               "or position quantities")

        position_pricing_parameters = PositionsPricingParameters(
            currency=currency.value,
            weighting_strategy=weighting_strategy.value,
            carryover_positions_for_missing_dates=carryover_positions_for_missing_dates,
            should_reweight=should_reweight,
            allow_fractional_shares=allow_fractional_shares
        )

        if kwargs:
            [setattr(position_pricing_parameters, arg, value) for arg, value in kwargs.items()]

        if weighting_strategy == PositionSetWeightingStrategy.Weight:
            positions_with_missing_weights = position_sets_to_price_df[position_sets_to_price_df['weight'].isna()]
            if not positions_with_missing_weights.empty:
                _logger.warning("Some positions do not have weights. These will be filtered out")
        else:
            positions_with_missing_quantities = position_sets_to_price_df[position_sets_to_price_df['quantity'].isna()]
            if not positions_with_missing_quantities.empty:
                _logger.warning("Some positions do not have quantities. These will be filtered out")

        if "weight" not in position_sets_column_attributes:
            position_sets_to_price_df['weight'] = None
        elif "quantity" not in position_sets_column_attributes:
            position_sets_to_price_df["quantity"] = None

        position_sets_to_price_df['positions'] = \
            np.vectorize(
                lambda asset_id, weight, quantity:
                PositionsRequest(asset_id=asset_id, weight=weight, quantity=quantity))(
                position_sets_to_price_df['asset_id'],
                position_sets_to_price_df['weight'],
                position_sets_to_price_df['quantity'])

        # build positionSets requests
        position_sets_grouped_by_date = position_sets_to_price_df.groupby("date")

        all_pos_sets = []
        for date, pos_df in position_sets_grouped_by_date:
            all_pos_sets.append(
                PositionSetRequest(date=date,
                                   positions=pos_df['positions'].tolist(),
                                   target_notional=pos_df['reference_notional'].iat[
                                       0] if weighting_strategy == PositionSetWeightingStrategy.Weight else None))

        batches = np.array_split(all_pos_sets, math.ceil(len(all_pos_sets) / batch_size))
        all_pricing_results = []

        start = time()
        for batch_idx, batch in enumerate(batches):
            _logger.info(f"Pricing batch {batch_idx} of {len(batches)}")
            try:
                payload = PositionsPricingRequest(parameters=position_pricing_parameters,
                                                  position_sets=tuple(batch))
                pricing_results = _repeat_try_catch_request(GsPriceApi.price_many_positions, number_retries=3,
                                                            return_result=True,
                                                            verbose=False,
                                                            pricing_request=payload)
                all_pricing_results += pricing_results
            except MqRequestError as request_exception:
                earliest_pos_set_in_batch = batch[0]
                latest_pos_set_in_batch = batch[-1]
                _logger.error(f"An error occurred while pricing positions on holding dates "
                              f"{earliest_pos_set_in_batch.date} to {latest_pos_set_in_batch.date}: "
                              f"{request_exception}.Consider batching position sets or reducing the batch"
                              f"size")
                if not allow_partial_pricing:
                    raise request_exception
        _logger.info(f"Total time to price positions is {time() - start} seconds")

        next_start = time()
        date_to_priced_position_sets = {
            dt.datetime.strptime(pos_set.get('date'), '%Y-%m-%d').date(): pos_set for pos_set in all_pricing_results}

        for input_position_set in position_sets:
            if not isinstance(input_position_set.date, dt.date):
                # use pandas to infer format of date
                input_position_set.date = pd.to_datetime(input_position_set.date).date()
            if not date_to_priced_position_sets.get(input_position_set.date):
                input_position_set.__unpriced_positions = list(input_position_set.positions)
                input_position_set.positions = None
                continue

            priced_position_set = date_to_priced_position_sets.get(input_position_set.date)
            position_date = dt.datetime.strptime(priced_position_set.get('date'), '%Y-%m-%d').date()
            priced_positions_df = pd.DataFrame(priced_position_set.get('positions'))
            column_from_initial_position_sets_to_merge_by = "weight" \
                if weighting_strategy == PositionSetWeightingStrategy.Weight else "quantity"
            column_from_priced_positions_results_to_merge_by = "referenceWeight" \
                if column_from_initial_position_sets_to_merge_by == "weight" else "quantity"
            priced_positions_df = priced_positions_df\
                .drop_duplicates(subset=['assetId', column_from_priced_positions_results_to_merge_by])

            priced_positions_df = pd.merge(
                position_sets_to_price_df.loc[position_sets_to_price_df['date'] == position_date, :],
                priced_positions_df,
                how="left",
                left_on=['asset_id', column_from_initial_position_sets_to_merge_by],
                right_on=['assetId', column_from_priced_positions_results_to_merge_by],
                suffixes=("original", None)
            )

            unpriced_positions_df = priced_positions_df[priced_positions_df['weight'].isna()] \
                if weighting_strategy == PositionSetWeightingStrategy.Weight else \
                priced_positions_df[priced_positions_df['quantity'].isna()]
            priced_positions_df = priced_positions_df[~priced_positions_df['weight'].isna()] \
                if weighting_strategy == PositionSetWeightingStrategy.Weight else \
                priced_positions_df[~priced_positions_df["quantity"].isna()]
            positions = []
            for record in priced_positions_df.to_dict('records'):
                curr_position = Position(asset_id=record.get('assetId'),
                                         identifier=record.get('identifier'),
                                         name=record.get('name'),
                                         weight=record.get('weight'),
                                         quantity=record.get('quantity'),
                                         tags=record.get('tags'))
                curr_position._restricted = record.get('restricted')
                positions.append(curr_position)

            unpriced_positions = [Position(asset_id=unpriced_record.get('assetId'),
                                           identifier=unpriced_record.get('identifier'),
                                           name=unpriced_record.get('name')) for unpriced_record in
                                  unpriced_positions_df.to_dict('records')]

            input_position_set.positions = positions
            input_position_set._unpriced_positions = unpriced_positions

        _logger.info(f"Total time to process pricing results is {time() - next_start} seconds")
