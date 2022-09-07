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

from gs_quant.target.common import *
from gs_quant.target.common import PayReceive as _PayReceive
from gs_quant.target.common import RiskMeasure as __RiskMeasure
from gs_quant.target.common import RiskMeasureType, AssetClass


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


class MarketBehaviour(EnumBase, Enum):

    """ContraintsBased or Calibrated"""

    ContraintsBased = 'ContraintsBased'
    Calibrated = 'Calibrated'


class RiskMeasure(__RiskMeasure):

    def __lt__(self, other):
        if self.name != other.name:
            return self.name < other.name
        elif self.parameters is not None:
            if other.parameters is None:
                return False
            if not isinstance(other.parameters, type(self.parameters)):
                return self.parameters.parameter_type < other.parameters.parameter_type
            else:
                return self.parameters < other.parameters
        elif other.parameters is not None:
            return True
        return False

    def __repr__(self):
        return self.name or self.measure_type.name

    @property
    def pricing_context(self):
        from gs_quant.markets import PricingContext
        return PricingContext.current


class ParameterisedRiskMeasure(RiskMeasure):
    def __init__(self, asset_class: Union[AssetClass, str] = None,
                 measure_type: Union[RiskMeasureType, str] = None, unit: Union[RiskMeasureUnit, str] = None,
                 value: Union[float, str] = None, parameters: RiskMeasureParameter = None, name: str = None):
        super().__init__(asset_class=asset_class, measure_type=measure_type, unit=unit, value=value, name=name)
        if parameters:
            if isinstance(parameters, RiskMeasureParameter):
                self.parameters = parameters
            else:
                raise TypeError(f"Unsupported parameter {parameters}")

    def __repr__(self):
        name = self.name or self.measure_type.name
        params = None
        if self.parameters:
            params = self.parameters.as_dict()
            params.pop('parameter_type', None)
            sorted_keys = sorted(params.keys(), key=lambda x: x.lower())
            params = ', '.join(
                [f'{k}:{params[k].value if isinstance(params[k], EnumBase) else params[k]}' for k in sorted_keys])
        return name + '(' + params + ')' if params else name

    def parameter_is_empty(self):
        return self.parameters is None

