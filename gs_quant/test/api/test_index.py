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

from unittest import mock

import datetime as dt

from gs_quant.api.gs.assets import AssetType
from gs_quant.api.gs.indices import GsIndexApi
from gs_quant.session import GsSession, Environment
from gs_quant.target.indices import *

# values used to build api payloads
basket_id = 'MQID_BASKET'
name = 'Test Basket'
position_set = [{'assetId': 'MQID_1', 'quantity': 100}, {'assetId': 'MQID_2', 'quantity': 200}]
publish_parameters = PublishParameters(False, False, False, False)
pricing_parameters = CustomBasketsPricingParameters(currency=IndicesCurrency.USD, initial_price=100)
return_type = 'Price Return'
ticker = 'BASKETTKR'
report_id = 'REPORT_ID'
date = dt.date(2021, 1, 1)


@mock.patch.object(GsSession.__class__, 'default_value')
def mock_session(mocker):
    mocker.return_value = GsSession.get(Environment.QA, 'client_id', 'secret')


@mock.patch.object(GsIndexApi, 'create')
def test_basket_create(mocker):
    # construct inputs and mock response
    inputs = CustomBasketsCreateInputs(name, position_set, pricing_parameters, return_type,
                                       ticker, publish_parameters=publish_parameters)
    mock_response = CustomBasketsResponse(report_id, basket_id, 'done')

    # setup mock session and api response
    mock_session()
    mocker.return_value = mock_response

    # run test
    response = GsIndexApi.create(inputs)
    assert response == mock_response


@mock.patch.object(GsIndexApi, 'edit')
def test_basket_edit(mocker):
    # construct inputs and mock response
    inputs = CustomBasketsEditInputs(name=name, flagship=True)
    mock_response = CustomBasketsResponse(report_id, basket_id, 'done')

    # setup mock session and api response
    mock_session()
    mocker.return_value = mock_response

    # run test
    response = GsIndexApi.edit(basket_id, inputs)
    assert response == mock_response


@mock.patch.object(GsIndexApi, 'rebalance')
def test_basket_rebalance(mocker):
    # construct inputs and mock response
    inputs = CustomBasketsRebalanceInputs(position_set, pricing_parameters)
    mock_response = CustomBasketsResponse(report_id, basket_id, 'done')

    # setup mock session and api response
    mock_session()
    mocker.return_value = mock_response

    # run test
    response = GsIndexApi.rebalance(basket_id, AssetType.Custom_Basket, inputs)
    assert response == mock_response


@mock.patch.object(GsIndexApi, 'cancel_rebalance')
def test_basket_cancel_rebalance(mocker):
    # construct inputs and mock response
    inputs = CustomBasketsRebalanceAction(comment='test cancel')
    mock_response = f'Rebalance submission for {basket_id} has been cancelled'

    # setup mock session and api response
    mock_session()
    mocker.return_value = mock_response

    # run test
    response = GsIndexApi.cancel_rebalance(basket_id, inputs)
    assert response == mock_response


@mock.patch.object(GsIndexApi, 'last_rebalance_data')
def test_basket_last_rebalance_data(mocker):
    # construct mock response
    mock_response = {'reportId': report_id, 'assetId': basket_id}

    # setup mock session and api response
    mock_session()
    mocker.return_value = mock_response

    # run test
    response = GsIndexApi.last_rebalance_data(basket_id)
    assert response == mock_response


@mock.patch.object(GsIndexApi, 'initial_price')
def test_basket_initial_price(mocker):
    # construct mock response
    mock_response = {'price': 100}

    # setup mock session and api response
    mock_session()
    mocker.return_value = mock_response

    # run test
    response = GsIndexApi.initial_price(basket_id, date)
    assert response == mock_response
