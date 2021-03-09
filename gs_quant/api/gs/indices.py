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

import logging
import datetime as dt
from typing import Union, Dict

from gs_quant.api.gs.assets import AssetType
from gs_quant.errors import MqValueError
from gs_quant.session import GsSession
from gs_quant.target.indices import CustomBasketsCreateInputs, CustomBasketsResponse, \
    CustomBasketsRebalanceAction, IndicesDynamicConstructInputs, IndicesEditInputs, \
    IndicesRebalanceInputs, ISelectActionRequest, ISelectResponse
from requests.exceptions import HTTPError

_logger = logging.getLogger(__name__)


class GsIndexApi:
    """GS Index API client implementation"""

    @classmethod
    def create(cls,
               inputs: Union[CustomBasketsCreateInputs, IndicesDynamicConstructInputs]
               ) -> CustomBasketsResponse:
        try:
            response = GsSession.current._post('/indices', payload=inputs, cls=CustomBasketsResponse)
        except HTTPError as err:
            raise MqValueError(f'Unable to create index with {err}')
        return response

    @classmethod
    def edit(cls, id_: str, inputs: IndicesEditInputs) -> CustomBasketsResponse:
        url = f'/indices/{id_}/edit'
        try:
            response = GsSession.current._post(url, payload=inputs, cls=CustomBasketsResponse)
        except HTTPError as err:
            raise MqValueError(f'Unable to edit index with {err}')
        return response

    @classmethod
    def rebalance(cls,
                  id_: str,
                  asset_type: AssetType,
                  inputs: IndicesRebalanceInputs) -> Union[CustomBasketsResponse, ISelectResponse]:
        cls = CustomBasketsResponse if asset_type == AssetType.Custom_Basket or \
            asset_type == AssetType.Research_Basket else ISelectResponse
        url = f'/indices/{id_}/rebalance'
        try:
            response = GsSession.current._post(url, payload=inputs, cls=cls)
        except HTTPError as err:
            raise MqValueError(f'Unable to rebalance index with {err}')
        return response

    @classmethod
    def cancel_rebalance(cls, id_: str, inputs: Union[CustomBasketsRebalanceAction, ISelectActionRequest]):
        url = f'/indices/{id_}/rebalance/cancel'
        try:
            GsSession.current._post(url, payload=inputs)
        except HTTPError as err:
            raise MqValueError(f'Unable to cancel rebalance with {err}')
        return f'Rebalance submission for {id_} has been cancelled'

    @classmethod
    def last_rebalance_data(cls, id_: str) -> Dict:
        url = f'/indices/{id_}/rebalance/data/last'
        try:
            response = GsSession.current._get(url)
        except HTTPError as err:
            raise MqValueError(f'Unable to retrieve latest rebalance data with {err}')
        return response

    @classmethod
    def initial_price(cls, id_: str, date: dt.date) -> Dict:
        url = f'/indices/{id_}/rebalance/initialprice/{date.isoformat()}'
        try:
            response = GsSession.current._get(url)
        except HTTPError as err:
            raise MqValueError(f'Unable to retrieve initial price with {err}')
        return response
