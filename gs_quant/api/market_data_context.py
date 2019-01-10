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
from gs_quant.datetime.date import adjust_to_business_date
from gs_quant.api.risk import MarketDataCoordinate

from datetime import date, datetime, timedelta
from typing import Mapping, Union


class MarketDataContext(ContextBaseWithDefault):

    """A context containing market data parameters, such as as_of date/time and overrides"""

    def __init__(self, as_of: Union[date, datetime]=None, overrides: Mapping[MarketDataCoordinate, float]=None):
        super().__init__()
        self.__as_of = as_of or adjust_to_business_date(date.today() + timedelta(days=-1), prev=True)
        self.__overrides = overrides or {}

    @property
    def as_of(self):
        return self.__as_of

    @property
    def overrides(self):
        return self.__overrides
