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
from typing import Tuple

from gs_quant.target.portfolios import Position
from gs_quant.target.portfolios import PositionSet as PosSet

_logger = logging.getLogger(__name__)


class PositionSet:
    """

    Position Sets hold a collection of positions associated with a particular date

    """

    def __init__(self,
                 date: datetime.date,
                 positions: Tuple[Position, ...]):
        self.position_set = PosSet(positions=positions, position_date=date)

    def get_positions(self) -> Tuple[Position, ...]:
        """ Retrieve position set's positions """
        return self.position_set.positions

    def set_positions(self, positions: Tuple[Position, ...]):
        """ Set position set's positions """
        self.position_set.positions = positions

    def get_date(self) -> datetime.date:
        """ Retrieve position set's date """
        return self.position_set.position_date

    def set_date(self, date: datetime.date):
        """ Set position set's date """
        self.position_set.position_date = date

    def add_positions(self, positions: Tuple[Position, ...]):
        """ Add new positions to an existing position set """
        self.position_set.positions = self.position_set.positions + positions

    def remove_positions(self, positions: Tuple[Position, ...]):
        """ Remove positions from an existing position set """
        self.position_set.positions = [p for p in self.position_set.positions if p not in positions]
