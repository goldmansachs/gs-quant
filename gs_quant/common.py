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
from gs_quant.target.common import PayReceive as _PayReceive
from gs_quant.target.common import *
from gs_quant.target.risk import CountryCode
from enum import Enum


class PositionType(Enum):
    """Position type enumeration

    Enumeration of different position types for a portfolio or index

    """

    OPEN = "open"  #: Open positions (corporate action adjusted)
    CLOSE = "close"  #: Close positions (reflect trading activity on the close)
    ANY = 'any'


class DateLimit(Enum):
    
    """ Datetime date constants """

    LOW_LIMIT = dt.date(1952, 1, 1)


class PayReceive(EnumBase, Enum):

    """Pay or receive fixed"""

    Pay = 'Pay'
    Receive = 'Rec'
    Straddle = 'Straddle'

    @classmethod
    def _missing_(cls, key):
        if isinstance(key, _PayReceive):
            key = key.value

        return cls.Receive if key.lower() in ('receive', 'receiver') else super()._missing_(key)
