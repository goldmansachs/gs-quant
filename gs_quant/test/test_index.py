"""
Copyright 2018 Goldman Sachs.
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

import pytest
from gs_quant.api.gs.indices import *
from gs_quant.session import *
from gs_quant.api.gs.assets import GsAssetApi, GsAsset
from gs_quant.context_base import ContextMeta

def test_create(mocker):
    # construct inputs
    asset1_marquee_id = 'MQIDAsset1'
    asset2_marquee_id = 'MQIDAsset2'
    position_set = [{'assetId': asset1_marquee_id, 'quantity': 100}, {'assetId': asset2_marquee_id, 'quantity': 200}]
    publish_parameters = PublishParameters(False, False, False)
    pricing_parameters = IndicesPriceParameters()
    pricing_parameters.initialPrice = 100
    inputs = IndicesCreateInputs("ticker", 'Test Basket', pricing_parameters, position_set)
    inputs.publishParameters = publish_parameters
    # mock GsSession
    mock_response = CustomBasketsResponse('done', 'approvalId', 'reportId', 'MQIDIndex')
    mocker.patch.object(ContextMeta, 'current', return_value=GsSession(Environment.QA))
    mocker.patch.object(ContextMeta.current, '_post', return_value=mock_response)
    # run test
    index = GsIndexApi()
    response = index.create(inputs)
    ContextMeta.current._post.assert_called_with('/indices', payload=inputs, cls=CustomBasketsResponse)
    assert response == mock_response
    assert index.marquee_id == 'MQIDIndex'


def test_rebalance(mocker):
    # construct inputs
    index_marquee_id = 'MQIDIndex'
    asset1_marquee_id = 'MQIDAsset1'
    asset2_marquee_id = 'MQIDAsset2'
    position_set = [{'assetId': asset1_marquee_id, 'quantity': 100}, {'assetId': asset2_marquee_id, 'quantity': 200}]
    publish_parameters = PublishParameters(False, False, False)
    pricing_parameters = IndicesPriceParameters()
    pricing_parameters.initialPrice = 100
    parameters = {'publishParameters': publish_parameters, 'pricingParameters': pricing_parameters, 'positionSet': position_set}
    inputs = IndicesRebalanceInputs(parameters)
    # mock GsSession
    mock_asset = GsAsset('Equity', AssetType.Custom_Basket, 'Test Basket')
    mock_response = CustomBasketsResponse('done', 'approvalId', 'reportId', index_marquee_id)
    mocker.patch.object(ContextMeta, 'current', return_value=GsSession(Environment.QA))
    mocker.patch.object(ContextMeta.current, '_post', return_value=mock_response)
    mocker.patch.object(GsAssetApi, 'get_asset', return_value=mock_asset)
    # run test
    index = GsIndexApi(index_marquee_id)
    response = index.rebalance(inputs)
    ContextMeta.current._post.assert_called_with("/indices/{id}/rebalance".format(id=index_marquee_id),
                                                 payload=inputs, cls=CustomBasketsResponse)
    assert response == mock_response


def test_rebalance_raises_exception(mocker):
    # construct inputs
    index_marquee_id = 'MQIDIndex'
    asset1_marquee_id = 'MQIDAsset1'
    asset2_marquee_id = 'MQIDAsset2'
    position_set = [{'assetId': asset1_marquee_id, 'quantity': 100}, {'assetId': asset2_marquee_id, 'quantity': 200}]
    publish_parameters = PublishParameters(False, False, False)
    pricing_parameters = IndicesPriceParameters()
    pricing_parameters.initialPrice = 100
    parameters = {'publishParameters': publish_parameters, 'pricingParameters': pricing_parameters, 'positionSet': position_set}
    inputs = IndicesRebalanceInputs(parameters)
    # mock GsSession
    mock_asset = GsAsset('Equity', AssetType.Custom_Basket, 'Test Basket')
    mock_response = CustomBasketsResponse('done', 'approvalId', 'reportId', index_marquee_id)
    mocker.patch.object(ContextMeta, 'current', return_value=GsSession(Environment.QA))
    mocker.patch.object(ContextMeta.current, '_get', return_value=mock_asset)
    mocker.patch.object(ContextMeta.current, '_post', return_value=mock_response)
    # run test
    index = GsIndexApi()
    with pytest.raises(Exception):
        response = index.rebalance(inputs)


def test_rebalance_cancel(mocker):
    # construct inputs
    index_marquee_id = 'MQIDIndex'
    cancel_inputs = ApprovalAction('Test Cancel.')
    # mock GsSession
    mocker.patch.object(ContextMeta, 'current', return_value=GsSession(Environment.QA))
    mocker.patch.object(ContextMeta.current, '_post', return_value='')
    # run test
    index = GsIndexApi(index_marquee_id)
    index.cancel_rebalance(cancel_inputs)
    ContextMeta.current._post.assert_called()


def test_rebalance_cancel_raises_exception(mocker):
    # construct inputs
    cancel_inputs = ApprovalAction('Test Cancel.')
    # mock GsSession
    mocker.patch.object(ContextMeta, 'current', return_value=GsSession(Environment.QA))
    mocker.patch.object(ContextMeta.current, '_post', return_value='')
    # run test
    index = GsIndexApi()
    with pytest.raises(Exception):
        index.cancel_rebalance(cancel_inputs)

