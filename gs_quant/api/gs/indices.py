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
from typing import Dict, List

from gs_quant.api.gs.assets import IdList
from gs_quant.common import PositionType
from gs_quant.session import GsSession
from gs_quant.target.indices import *

# type aliases -- can add for edit/backcast/etc. if STS implements them in future
CreateRequest = Union[CustomBasketsCreateInputs, IndicesDynamicConstructInputs]
CreateRepsonse = Union[CustomBasketsResponse, DynamicConstructionResponse]
RebalanceRequest = Union[CustomBasketsRebalanceInputs, ISelectRebalance, ISelectRequest]
RebalanceResponse = Union[CustomBasketsResponse, ISelectResponse]
RebalanceCancelRequest = Union[CustomBasketsRebalanceAction, ISelectActionRequest]
RebalanceCancelResponse = Union[Dict, ISelectResponse]
ValidatedRequest = Union[CreateRequest, RebalanceRequest]


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
        return GsSession.current._post('/indices', payload=inputs, cls=response_cls)

    @classmethod
    def edit(cls, id_: str, inputs: CustomBasketsEditInputs) -> CustomBasketsResponse:
        """ Update basket metadata """
        url = f'/indices/{id_}/edit'
        inputs = IndicesEditInputs(parameters=inputs)
        return GsSession.current._post(url, payload=inputs, cls=CustomBasketsResponse)

    @classmethod
    def rebalance(cls, id_: str, inputs: RebalanceRequest) -> RebalanceResponse:
        """ Rebalance existing index with new composition """
        url = f'/indices/{id_}/rebalance'
        response_cls = cls._response_cls[type(inputs)]
        inputs = IndicesRebalanceInputs(parameters=inputs) if not isinstance(inputs, ISelectRequest) else inputs
        return GsSession.current._post(url, payload=inputs, cls=response_cls)

    @classmethod
    def cancel_rebalance(cls, id_: str, inputs: RebalanceCancelRequest) -> RebalanceCancelResponse:
        """ Cancel most recent rebalance submission if not yet approved """
        url = f'/indices/{id_}/rebalance/cancel'
        response_cls = cls._response_cls[type(inputs)]
        return GsSession.current._post(url, payload=inputs, cls=response_cls)

    @classmethod
    def last_rebalance_data(cls, id_: str) -> Dict:
        """ Get latest basket rebalance data """
        url = f'/indices/{id_}/rebalance/data/last'
        return GsSession.current._get(url)

    @classmethod
    def last_rebalance_approval(cls, id_: str) -> ApprovalCustomBasketResponse:
        """ Get latest basket rebalance approval info """
        url = f'/indices/{id_}/rebalance/approvals/last'
        return GsSession.current._get(url, cls=ApprovalCustomBasketResponse)

    @classmethod
    def initial_price(cls, id_: str, date: dt.date) -> Dict:
        """ Get initial basket price """
        url = f'/indices/{id_}/rebalance/initialprice/{date.isoformat()}'
        return GsSession.current._get(url)

    @classmethod
    def validate_ticker(cls, ticker: str):
        """ Validate basket ticker """
        url = '/indices/validate'
        GsSession.current._post(url, payload={'ticker': ticker})

    @classmethod
    def backcast(cls, _id: str, inputs: CustomBasketsBackcastInputs) -> CustomBasketsResponse:
        """ Backcast basket composition history before live date """
        url = f'/indices/{_id}/backcast'
        inputs = IndicesBackcastInputs(parameters=inputs)
        return GsSession.current._post(url, payload=inputs, cls=CustomBasketsResponse, timeout=240)

    @classmethod
    def update_risk_reports(cls, _id: str, inputs: CustomBasketRiskParams):
        """ Create, modify, or delete a custom basket factor risk report """
        url = f'/indices/{_id}/risk/reports'
        inputs = CustomBasketsRiskScheduleInputs(risk_models=inputs)
        return GsSession.current._post(url, payload=inputs)

    @staticmethod
    def get_positions_data(
            asset_id: str,
            start_date: dt.date,
            end_date: dt.date,
            fields: IdList = None,
            position_type: PositionType = None,
    ) -> List[dict]:
        start_date_str = start_date.isoformat()
        end_date_str = end_date.isoformat()
        url = '/indices/{id}/positions/data?startDate={start_date}&endDate={end_date}'.format(id=asset_id,
                                                                                              start_date=start_date_str,
                                                                                              end_date=end_date_str)
        if fields is not None:
            url += '&fields='.join([''] + fields)

        if position_type is not None:
            url += '&type=' + position_type.value

        results = GsSession.current._get(url)['results']
        return results

    @staticmethod
    def get_last_positions_data(
            asset_id: str,
            fields: IdList = None,
            position_type: PositionType = None,
    ) -> List[dict]:
        url = f'/indices/{asset_id}/positions/last/data'
        params = ''
        if fields is not None:
            params += '&fields='.join([''] + fields)

        if position_type is not None:
            params += '&type=' + position_type.value

        if len(params):
            url = f'{url}?{params}'

        results = GsSession.current._get(url)['results']
        return results
