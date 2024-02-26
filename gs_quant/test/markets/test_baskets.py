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
from typing import Dict
from unittest import mock

import datetime as dt
import pytest

from gs_quant.api.gs.assets import AssetClass, AssetType, GsAsset, GsAssetApi
from gs_quant.api.gs.indices import GsIndexApi
from gs_quant.api.gs.reports import GsReportApi
from gs_quant.api.gs.users import GsUsersApi
from gs_quant.entities.entitlements import User
from gs_quant.errors import MqError
from gs_quant.markets.baskets import Basket, ErrorMessage
from gs_quant.markets.indices_utils import ReturnType
from gs_quant.markets.position_set import Position, PositionSet
from gs_quant.session import GsSession, Environment
from gs_quant.target.common import Entitlements as TargetEntitlements, \
    PositionSet as TargetPositionSet, Position as TargetPosition, ReportParameters, XRef
from gs_quant.target.indices import CustomBasketsResponse, CustomBasketRiskParams
from gs_quant.target.reports import Report, User as TargetUser

# Helper mock value constants
asset_1 = {'name': 'asset 1', 'id': 'id1', 'bbid': 'bbid1'}
asset_2 = {'name': 'asset 2', 'id': 'id2', 'bbid': 'bbid2'}
assets_data = [asset_1, asset_2]
base_user = {'name': 'First Last',
             'email': 'ex@email.com',
             'city': 'City A',
             'company': 'Company A',
             'country': 'Country A',
             'region': 'Region A'}
cb_response = CustomBasketsResponse('done', 'R1234567890', 'MA1234567890')
gs_asset = GsAsset(asset_class=AssetClass.Equity,
                   type_=AssetType.Custom_Basket,
                   name='Test Basket',
                   id_='MA1234567890',
                   entitlements=TargetEntitlements(admin=['guid:user_abc']),
                   xref=XRef(ticker='GSMBXXXX'))
initial_price = {'price': 100}
mqid = 'MA1234567890'
name = 'Test Basket'
positions = [Position('bbid1', asset_id='id1', quantity=100), Position('bbid2', asset_id='id2', quantity=200)]
positions_weighted = positions = [Position('bbid1', asset_id='id1', weight=0.4),
                                  Position('bbid2', asset_id='id2', weight=0.6)]
position_set = PositionSet(positions, divisor=1000)
report = Report(mqid, 'asset', 'Basket Create', ReportParameters(), status='done')
resolved_asset = {'GSMBXXXX': [{'id': mqid}]}
target_positions = tuple([TargetPosition(asset_id='id1', quantity=100), TargetPosition(asset_id='id2', quantity=200)])
target_position_set = TargetPositionSet(target_positions, dt.date(2021, 1, 7), divisor=1000)
ticker = 'GSMBXXXX'
user_ea = {**base_user, 'id': 'user_abc', 'tokens': ['external', 'guid:user_abc']}  # external, admin
user_ena = {**base_user, 'id': 'user_xyz', 'tokens': ['external', 'guid:user_xyz']}  # external, non admin
user_ia = {**base_user, 'id': 'user_abc', 'tokens': ['internal', 'guid:user_abc']}  # internal, admin


@mock.patch.object(GsSession.__class__, 'default_value')
def mock_session(mocker):
    """ Mock GsSession helper """
    mocker.return_value = GsSession.get(Environment.QA, 'client_id', 'secret')


def mock_response(mocker, mock_object, mock_fn, mock_response):
    """ Mock patch helper """
    if mock_response is not None:
        mocker.patch.object(mock_object, mock_fn, return_value=mock_response)


def mock_basket_init(mocker, user: Dict, existing: bool = True):
    """ Mock basket initialization helper """
    if existing:
        mock_response(mocker, GsAssetApi, 'resolve_assets', resolved_asset)
        mock_response(mocker, GsAssetApi, 'get_asset', gs_asset)
        mock_response(mocker, GsAssetApi, 'get_latest_positions', target_position_set)
        mock_response(mocker, GsAssetApi, 'get_many_assets_data', assets_data)
        mock_response(mocker, GsIndexApi, 'initial_price', initial_price)
        mock_response(mocker, GsReportApi, 'get_reports', [report])
        mock_response(mocker, GsUsersApi, 'get_users', [TargetUser.from_dict(user)])
    mock_response(mocker, GsUsersApi, 'get_current_user_info', user)


def test_basket_error_messages(mocker):
    mock_session()

    # test non admin errors
    mock_basket_init(mocker, user_ena)
    basket = Basket.get(ticker)
    with pytest.raises(MqError, match=ErrorMessage.NON_ADMIN.value):
        basket.cancel_rebalance()
    with pytest.raises(MqError, match=ErrorMessage.NON_ADMIN.value):
        basket.allow_ca_restricted_assets = False

    # test non internal errors
    with pytest.raises(MqError, match=ErrorMessage.NON_INTERNAL.value):
        basket.flagship = False

    # test unmodifiable errors
    with pytest.raises(MqError, match=ErrorMessage.UNMODIFIABLE.value):
        basket.ticker = 'GSMBZZZZ'

    # test uninitialized errors
    mock_basket_init(mocker, user_ena, False)
    basket = Basket()
    with pytest.raises(MqError, match=ErrorMessage.UNINITIALIZED.value):
        basket.clone()
    with pytest.raises(MqError, match=ErrorMessage.UNINITIALIZED.value):
        basket.get_latest_rebalance_data()


def test_basket_create(mocker):
    mock_session()
    mock_basket_init(mocker, user_ea, False)
    mock_response(mocker, GsIndexApi, 'validate_ticker', True)

    basket = Basket()
    basket.name = name
    basket.ticker = ticker
    basket.position_set = position_set
    basket.return_type = ReturnType.PRICE_RETURN

    mock_response(mocker, GsIndexApi, 'create', cb_response)
    mock_response(mocker, GsAssetApi, 'get_asset', gs_asset)
    mock_response(mocker, GsReportApi, 'get_report', report)
    mock_basket_init(mocker, user_ea)

    response = basket.create()
    GsIndexApi.create.assert_called()
    assert response == cb_response.as_dict()


def test_basket_clone(mocker):
    mock_session()

    # test uninitialized errors
    mock_basket_init(mocker, user_ea, False)
    basket = Basket()
    with pytest.raises(MqError, match=ErrorMessage.UNINITIALIZED.value):
        basket.clone()

    # test clone
    mock_basket_init(mocker, user_ena)
    parent_basket = Basket.get(ticker)
    clone = parent_basket.clone()
    mock_basket_init(mocker, user_ea, False)

    parent_positions = [p.as_dict() for p in parent_basket.position_set.positions]
    clone_positions = [p.as_dict() for p in clone.position_set.positions]

    assert clone_positions == parent_positions
    assert clone.clone_parent_id == mqid
    assert clone.parent_basket == ticker


def test_basket_edit(mocker):
    mock_session()

    # test errors
    mock_basket_init(mocker, user_ea, False)
    basket = Basket()
    with pytest.raises(MqError, match=ErrorMessage.UNINITIALIZED.value):
        basket.update()

    mock_basket_init(mocker, user_ena)
    basket = Basket.get(ticker)
    with pytest.raises(MqError, match=ErrorMessage.NON_ADMIN.value):
        basket.update()

    # test update
    mock_basket_init(mocker, user_ia)
    basket = Basket.get(ticker)
    basket.description = 'New Basket Description'
    gs_asset.description = 'New Basket Description'

    mock_response(mocker, GsIndexApi, 'edit', cb_response)
    mock_response(mocker, GsAssetApi, 'get_asset', gs_asset)
    mock_response(mocker, GsReportApi, 'get_report', report)
    mock_basket_init(mocker, user_ia)

    response = basket.update()
    GsIndexApi.edit.assert_called()
    assert response == cb_response.as_dict()
    assert basket.description == 'New Basket Description'

    gs_asset.description = None


def test_basket_rebalance(mocker):
    mock_session()
    mock_basket_init(mocker, user_ia)

    basket = Basket.get(ticker)
    basket.allow_ca_restricted_assets = True

    mock_response(mocker, GsIndexApi, 'rebalance', cb_response)
    mock_response(mocker, GsAssetApi, 'get_asset', gs_asset)
    mock_response(mocker, GsReportApi, 'get_report', report)
    mock_basket_init(mocker, user_ia)

    response = basket.update()
    GsIndexApi.rebalance.assert_called()
    assert response == cb_response.as_dict()


def test_basket_edit_and_rebalance(mocker):
    mock_session()
    mock_basket_init(mocker, user_ia)

    basket = Basket.get(ticker)
    basket.description = 'New Basket Description'
    gs_asset.description = 'New Basket Description'
    basket.initial_price = 2000000

    mock_response(mocker, GsIndexApi, 'edit', cb_response)
    mock_response(mocker, GsReportApi, 'get_report', report)
    mock_response(mocker, GsIndexApi, 'rebalance', cb_response)
    mock_response(mocker, GsAssetApi, 'get_asset', gs_asset)
    mock_response(mocker, GsReportApi, 'get_report', report)
    mock_basket_init(mocker, user_ia)

    response = basket.update()
    GsIndexApi.edit.assert_called()
    GsIndexApi.rebalance.assert_called()
    assert response == cb_response.as_dict()
    assert basket.description == 'New Basket Description'
    gs_asset.description = None


def test_basket_update_entitlements(mocker):
    mock_session()

    mock_basket_init(mocker, user_ia)
    basket = Basket.get(ticker)

    mock_response(mocker, GsUsersApi, 'get_users', [TargetUser.from_dict(user_ena)])
    new_admin = User.get(user_id='user_xyz')
    basket.entitlements.admin.users += [new_admin]

    entitlements_response = TargetEntitlements(admin=['guid:user_abc', 'guid:user_xyz'])
    mock_response(mocker, GsAssetApi, 'update_asset_entitlements', entitlements_response)
    response = basket.update()
    GsAssetApi.update_asset_entitlements.assert_called()
    assert response == entitlements_response


def test_upload_position_history(mocker):
    mock_session()

    # test errors
    mock_basket_init(mocker, user_ea, False)
    basket = Basket()
    with pytest.raises(MqError, match=ErrorMessage.UNINITIALIZED.value):
        basket.upload_position_history()

    mock_basket_init(mocker, user_ena)
    basket = Basket.get(ticker)
    with pytest.raises(MqError, match=ErrorMessage.NON_ADMIN.value):
        basket.upload_position_history()

    # test backcast
    mock_basket_init(mocker, user_ia)
    basket = Basket.get(ticker)
    pos_set_1 = PositionSet(positions_weighted, dt.date(2021, 1, 1))
    pos_set_2 = PositionSet(positions_weighted, dt.date(2021, 3, 1))
    pos_set_3 = PositionSet(positions_weighted, dt.date(2021, 5, 1))

    mock_response(mocker, GsIndexApi, 'backcast', cb_response)
    response = basket.upload_position_history([pos_set_1, pos_set_2, pos_set_3])
    GsIndexApi.backcast.assert_called()
    assert response == cb_response.as_dict()


def test_update_risk_reports(mocker):
    mock_session()

    # test errors
    mock_basket_init(mocker, user_ea, False)
    basket = Basket()
    with pytest.raises(MqError, match=ErrorMessage.UNINITIALIZED.value):
        basket.add_factor_risk_report('AXUS4M', False)
    with pytest.raises(MqError, match=ErrorMessage.UNINITIALIZED.value):
        basket.delete_factor_risk_report('AXUS4M')

    mock_basket_init(mocker, user_ena)
    basket = Basket.get(ticker)
    with pytest.raises(MqError, match=ErrorMessage.NON_ADMIN.value):
        basket.add_factor_risk_report('AXUS4M', False)
    with pytest.raises(MqError, match=ErrorMessage.NON_ADMIN.value):
        basket.delete_factor_risk_report('AXUS4M')

    # test add/delete factor risk reports
    mock_basket_init(mocker, user_ea)
    basket = Basket.get(ticker)

    mock_response(mocker, GsIndexApi, 'update_risk_reports', {})
    basket.add_factor_risk_report('AXUS4M', False)
    payload = CustomBasketRiskParams(risk_model='AXUS4M', fx_hedged=False)
    GsIndexApi.update_risk_reports.assert_called_with(payload)

    mock_response(mocker, GsIndexApi, 'update_risk_reports', {})
    basket.delete_factor_risk_report('AXUS4M')
    payload = CustomBasketRiskParams(risk_model='AXUS4M', delete=True)
    GsIndexApi.update_risk_reports.assert_called_with(payload)
