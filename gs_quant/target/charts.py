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

from gs_quant.target.common import *
import datetime
from typing import Tuple, Union
from enum import Enum
from gs_quant.base import Base, EnumBase, InstrumentBase, camel_case_translate, get_enum_value


class ChartFill(EnumBase, Enum):    
    
    """Chart Fill Type"""

    _None = 'None'
    Solid = 'Solid'
    Gradient = 'Gradient'
    
    def __repr__(self):
        return self.value


class ChartLineDrawType(EnumBase, Enum):    
    
    """Line Draw Type"""

    Area = 'Area'
    Bars = 'Bars'
    Candlesticks = 'Candlesticks'
    Lines = 'Lines'
    StepAfter = 'StepAfter'
    StepBefore = 'StepBefore'
    StepLinear = 'StepLinear'
    Volumes = 'Volumes'
    
    def __repr__(self):
        return self.value


class ChartLineType(EnumBase, Enum):    
    
    """Line Type"""

    Solid = 'Solid'
    Knotted = 'Knotted'
    Dashed = 'Dashed'
    
    def __repr__(self):
        return self.value


class ChartShare(Base):
        
    """Share With View Entitlement Object only for Chart"""

    @camel_case_translate
    def __init__(
        self,
        guids: Tuple[str, ...] = None,
        version: int = None,
        name: str = None
    ):        
        super().__init__()
        self.guids = guids
        self.version = version
        self.name = name

    @property
    def guids(self) -> Tuple[str, ...]:
        """Array of guid"""
        return self.__guids

    @guids.setter
    def guids(self, value: Tuple[str, ...]):
        self._property_changed('guids')
        self.__guids = value        

    @property
    def version(self) -> int:
        """Chart Object Version"""
        return self.__version

    @version.setter
    def version(self, value: int):
        self._property_changed('version')
        self.__version = value        
