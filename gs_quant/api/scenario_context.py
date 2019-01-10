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

from gs_quant.context_base import ContextBaseWithDefault
from gs_quant.api.risk import MarketDataCoordinate

from typing import Mapping


class ScenarioContext(ContextBaseWithDefault):

    """A context containing scenario parameters, such as shocks"""

    def __init__(self, subtract_base: bool=True, shocks: Mapping[MarketDataCoordinate, float]=None):
        super().__init__()
        self.__subtract_base = subtract_base
        self.__shocks = shocks or {}

    @property
    def subtract_base(self):
        return self.__subtract_base

    @property
    def shocks(self):
        return self.__shocks
