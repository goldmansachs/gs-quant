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
from gs_quant.base import Priceable
from gs_quant.target.common import MarketDataCoordinate as __MarketDataCoordinate
from gs_quant.target.common import XRef as __XRef


class MarketDataCoordinate(__MarketDataCoordinate):

    def __str__(self):
        return "|".join(f or '' for f in (self.marketDataType, self.marketDataAsset or self.assetId, self.pointClass, '_'.join(self.marketDataPoint), self.field))


class XRef(__XRef, Priceable):

    def __str__(self):
        properties = [i for i in dir(self.__class__) if isinstance(getattr(self.__class__, i), property)]
        values = [getattr(self, p) for p in properties]
        return ', '.join(('{}={}'.format(p, v) for p, v in zip(properties, values) if v))
