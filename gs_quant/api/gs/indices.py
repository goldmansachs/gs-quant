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
from gs_quant.api.gs.assets import GsAssetApi
from gs_quant.session import *
from gs_quant.target.indices import *
from typing import Union


class GsIndexApi:

    marquee_id = None

    def __init__(self, marquee_id: str = None):
        self.marquee_id = marquee_id

    def create(
            self,
            inputs: IndicesCreateInputs,
    ) -> CustomBasketsResponse:
        """
        Create a custom basket of equity stocks or ETFs

        :param inputs: parameters used to create the index
        :return: a response object containing status of create process, reportId and assetId
        """

        response = GsSession.current._post('/indices', payload=inputs, cls=CustomBasketsResponse)
        self.marquee_id = response.assetId
        return response

    def rebalance(
            self,
            inputs: IndicesRebalanceInputs,
    ) -> Union[CustomBasketsResponse, ISelectResponse]:
        """
        Rebalance of indices: including iSelect and Custom Baskets

        :param inputs: parameters used to rebalance the index
        :return: a response object containing status of rebalance, reportId, approvalId and assetId
        """

        if self.marquee_id is None:
            raise ValueError('Missing Asset Id of target index at initialization')

        asset = GsAssetApi.get_asset(self.marquee_id)
        if asset.type == AssetType.Custom_Basket or asset.type == AssetType.Research_Basket:
            cls = CustomBasketsResponse
        else:
            cls = ISelectResponse

        url = "/indices/{id}/rebalance".format(id=self.marquee_id)
        response = GsSession.current._post(url, payload=inputs, cls=cls)
        return response

    def cancel_rebalance(
            self,
            inputs: ApprovalAction,
    ):
        """
        Cancel current pending rebalance of an index

        :param inputs: Comments for the approval action
        """

        if self.marquee_id is None:
            raise ValueError('Missing Asset Id of target index at initialization')

        url = "/indices/{id}/rebalance/cancel".format(id=self.marquee_id)
        GsSession.current._post(url, payload=inputs)

    def edit(
            self,
            inputs: IndicesEditInputs,
    ) -> CustomBasketsResponse:
        """
        Edit indices

        :param inputs: parameters used to edit the index
        :return: a response object containing status of edit, reportId and assetId
        """

        if self.marquee_id is None:
            raise ValueError('Missing Asset Id of target index at initialization')

        url = "/indices/{id}/edit".format(id=self.marquee_id)
        response = GsSession.current._post(url, payload=inputs, cls=CustomBasketsResponse)
        return response
