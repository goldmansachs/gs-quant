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
import logging
from typing import Dict, Union

from gs_quant.errors import MqValueError
from gs_quant.session import GsSession
from gs_quant.target.indices import *
from requests.exceptions import HTTPError

_logger = logging.getLogger(__name__)


# type aliases -- can add for edit/backcast/etc. if STS implements them in future
CreateRequest = Union[CustomBasketsCreateInputs, IndicesDynamicConstructInputs]
CreateRepsonse = Union[CustomBasketsResponse, DynamicConstructionResponse]
RebalanceRequest = Union[CustomBasketsRebalanceInputs, ISelectRebalance, ISelectRequest]
RebalanceResponse = Union[CustomBasketsResponse, ISelectResponse]
RebalanceCancelRequest = Union[CustomBasketsRebalanceAction, ISelectActionRequest]
RebalanceCancelResponse = Union[Dict, ISelectResponse]


class GsIndexApi:
    """GS Index API client implementation"""
    _response_cls = {
        CustomBasketsCreateInputs: CustomBasketsResponse,
        IndicesDynamicConstructInputs: DynamicConstructionResponse,
        CustomBasketsRebalanceInputs: CustomBasketsResponse,
        ISelectRebalance: ISelectResponse,
        ISelectRequest: ISelectResponse,
        CustomBasketsRebalanceAction: Dict,
        ISelectActionRequest: ISelectResponse
    }

    @classmethod
    def create(cls, inputs: CreateRequest) -> CreateRepsonse:
        """ Create new basket or iselect strategy """
        response_cls = cls._response_cls[type(inputs)]
        try:
            response = GsSession.current._post('/indices', payload=inputs, cls=response_cls)
        except HTTPError as err:
            raise MqValueError(f'Unable to create index with {err}')
        return response

    @classmethod
    def edit(cls, id_: str, inputs: CustomBasketsEditInputs) -> CustomBasketsResponse:
        """ Update basket metadata """
        url = f'/indices/{id_}/edit'
        inputs = IndicesEditInputs(parameters=inputs)
        try:
            response = GsSession.current._post(url, payload=inputs, cls=CustomBasketsResponse)
        except HTTPError as err:
            raise MqValueError(f'Unable to edit index with {err}')
        return response

    @classmethod
    def rebalance(cls, id_: str, inputs: RebalanceRequest) -> RebalanceResponse:
        """ Rebalance existing index with new composition """
        url = f'/indices/{id_}/rebalance'
        response_cls = cls._response_cls[type(inputs)]
        inputs = IndicesRebalanceInputs(parameters=inputs) if not isinstance(inputs, ISelectRequest) else inputs
        try:
            response = GsSession.current._post(url, payload=inputs, cls=response_cls)
        except HTTPError as err:
            raise MqValueError(f'Unable to rebalance index with {err}')
        return response

    @classmethod
    def cancel_rebalance(cls, id_: str, inputs: RebalanceCancelRequest) -> RebalanceCancelResponse:
        """ Cancel most recent rebalance submission if not yet approved """
        url = f'/indices/{id_}/rebalance/cancel'
        response_cls = cls._response_cls[type(inputs)]
        try:
            response = GsSession.current._post(url, payload=inputs, cls=response_cls)
        except HTTPError as err:
            raise MqValueError(f'Unable to cancel rebalance with {err}')
        return response

    @classmethod
    def last_rebalance_data(cls, id_: str) -> Dict:
        """ Get latest basket rebalance data """
        url = f'/indices/{id_}/rebalance/data/last'
        try:
            response = GsSession.current._get(url)
        except HTTPError as err:
            raise MqValueError(f'Unable to retrieve latest rebalance data with {err}')
        return response

    @classmethod
    def last_rebalance_approval(cls, id_: str) -> ApprovalCustomBasketResponse:
        """ Get latest basket rebalance approval info """
        url = f'/indices/{id_}/rebalance/approvals/last'
        try:
            response = GsSession.current._get(url, cls=ApprovalCustomBasketResponse)
        except HTTPError as err:
            raise MqValueError(f'Unable to retrieve latest rebalance approval with {err}')
        return response

    @classmethod
    def initial_price(cls, id_: str, date: dt.date) -> Dict:
        """ Get initial basket price """
        url = f'/indices/{id_}/rebalance/initialprice/{date.isoformat()}'
        try:
            response = GsSession.current._get(url)
        except HTTPError as err:
            raise MqValueError(f'Unable to retrieve initial price with {err}')
        return response

    @classmethod
    def validate_ticker(cls, ticker: str):
        """ Validate basket ticker """
        url = '/indices/validate'
        try:
            GsSession.current._post(url, payload=IndicesValidateInputs(ticker=ticker))
        except HTTPError as err:
            raise MqValueError(f'Unable to validate ticker with {err}')

    @classmethod
    def backcast(cls, _id: str, inputs: CustomBasketsBackcastInputs) -> CustomBasketsResponse:
        """ Backcast basket composition history before live date """
        url = f'/indices/{_id}/backcast'
        inputs = IndicesBackcastInputs(parameters=inputs)
        try:
            response = GsSession.current._post(url, payload=inputs, cls=CustomBasketsResponse)
        except HTTPError as err:
            raise MqValueError(f'Unable to backcast custom basket history with {err}')
        return response
