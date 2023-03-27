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

from gs_quant.session import GsSession
from gs_quant.target.price import *


class GsPriceApi:
    """GS Price API client implementation"""

    @classmethod
    def price_positions(cls, inputs: PositionSetPriceInput) -> PositionSetPriceResponse:
        url = '/price/positions'
        return GsSession.current._post(url, payload=inputs, cls=PositionSetPriceResponse)
