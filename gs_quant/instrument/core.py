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
from gs_quant.target.common import RiskPosition
from gs_quant.target.instrument import *
from gs_quant.common import XRef

from typing import Iterable, Mapping, Union

__asset_class_and_type_to_instrument = {}


class Security(XRef):

    """A security, specified by a well-known identifier"""

    def __init__(self, ticker: str=None, bbid: str=None, isin: str=None, cusip: str=None, primeId: str=None, quantity: float=1):
        """
        Create a security by passing one identifier only and, optionally, a quantity

        :param ticker: Exchange ticker
        :param bbid: Bloomberg identifier
        :param isin: International Security Number
        :param cusip: CUSIP
        :param primeId: Prime (GS internal) identifier
        :param quantity: Quantity (number of contracts for exchange-traded instruments, notional for bonds)
        """
        if len(tuple(filter(None, (f is not None for f in (ticker, bbid, isin, cusip, primeId))))) > 1:
            raise ValueError('Only specify one identifier')

        super().__init__(ticker=ticker, bbid=bbid, isin=isin, cusip=cusip, primeId=primeId)
        self.quantity = quantity

    def get_quantity(self) -> float:
        """
        Quantity of the security
        """
        return self.quantity
