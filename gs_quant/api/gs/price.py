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
import backoff

from gs_quant.errors import MqRateLimitedError, MqTimeoutError, MqInternalServerError
from gs_quant.session import GsSession
from gs_quant.target.price import *
from gs_quant.target.positions_v2_pricing import *


class GsPriceApi:
    """GS Price API client implementation"""

    @classmethod
    @backoff.on_exception(lambda: backoff.expo(base=2, factor=2),
                          (MqTimeoutError, MqInternalServerError),
                          max_tries=5)
    @backoff.on_exception(lambda: backoff.constant(60),
                          MqRateLimitedError,
                          max_tries=5)
    def price_positions(cls, inputs: PositionSetPriceInput) -> PositionSetPriceResponse:
        url = '/price/positions'
        return GsSession.current._post(url, payload=inputs, cls=PositionSetPriceResponse)

    @classmethod
    def price_many_positions(cls, pricing_request: PositionsPricingRequest) -> dict:
        url = '/positions/price/bulk'
        GsSession.current.api_version = "v2"
        pricing_response = GsSession.current._post(url, payload=pricing_request)
        GsSession.current.api_version = "v1"

        positions = pricing_response.get("positions")

        return positions
