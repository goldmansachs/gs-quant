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
import pandas as pd

from gs_quant.datetime.time import to_zulu_string
import gs_quant.risk as risk
from gs_quant.api.gs.risk import GsRiskApi
from gs_quant.base import Priceable
from gs_quant.common import AssetClass
from gs_quant.instrument import CommodSwap, EqForward, EqOption, FXOption, IRBasisSwap, IRSwap, IRSwaption, IRCap, \
    IRFloor
from gs_quant.markets import PricingContext
from gs_quant.session import Environment, GsSession
from gs_quant.target.risk import PricingDateAndMarketDataAsOf, RiskPosition, RiskRequestParameters, \
    OptimizationRequest

priceables = (
    CommodSwap('Electricity', '1y'),
    EqForward('GS.N', expiration_date='1y'),
    EqOption('GS.N', '3m', 'ATMF', 'Call', 'European'),
    FXOption(pair='EURUSD', expiration_date='1y', option_type='Call', strike_price='ATMF'),
    IRSwap('Pay', '10y', 'USD'),
    IRBasisSwap('10y', 'USD'),
    IRSwaption('Pay', '10y', 'USD'),
    IRCap('10y', 'EUR'),
    IRFloor('10y', 'EUR')
)


def set_session():
    from gs_quant.session import OAuth2Session
    OAuth2Session.init = mock.MagicMock(return_value=None)
    GsSession.use(Environment.QA, 'client_id', 'secret')


def structured_calc(mocker, priceable: Priceable, measure: risk.RiskMeasure):
    set_session()

    values = {
        '$type': 'RiskVector',
        'asset': [0.01, 0.015],
        'points': [
            {'type': 'IR', 'asset': 'USD', 'class_': 'Swap', 'point': '1y'},
            {'type': 'IR', 'asset': 'USD', 'class_': 'Swap', 'point': '2y'}
        ]
    }
    mocker.return_value = [[[[values]]]]

    expected = risk.sort_risk(pd.DataFrame([
        {'mkt_type': 'IR', 'mkt_asset': 'USD', 'mkt_class': 'Swap', 'mkt_point': '1y', 'value': 0.01},
        {'mkt_type': 'IR', 'mkt_asset': 'USD', 'mkt_class': 'Swap', 'mkt_point': '2y', 'value': 0.015}
    ]))

    result = priceable.calc(measure)
    assert result.raw_value.equals(expected)
    default_date = PricingContext.current.pricing_date
    default_mkt = PricingContext.current.market
    risk_requests = (risk.RiskRequest(
        positions=(RiskPosition(instrument=priceable, quantity=1),),
        measures=(measure,),
        use_cache=PricingContext.current.use_server_cache,
        pricing_and_market_data_as_of=(PricingDateAndMarketDataAsOf(pricing_date=default_date,
                                                                    market=default_mkt),),
        parameters=RiskRequestParameters(raw_results=True),
        wait_for_results=True),)
    mocker.assert_called_with(risk_requests)


def scalar_calc(mocker, priceable: Priceable, measure: risk.RiskMeasure):
    set_session()
    mocker.return_value = [[[[{'$type': 'Risk', 'val': 0.01}]]]]

    result = priceable.calc(measure)
    assert result == 0.01
    default_date = PricingContext.current.pricing_date
    default_mkt = PricingContext.current .market
    risk_requests = (risk.RiskRequest(
        positions=(RiskPosition(instrument=priceable, quantity=1),),
        measures=(measure,),
        use_cache=PricingContext.current.use_server_cache,
        pricing_and_market_data_as_of=(PricingDateAndMarketDataAsOf(pricing_date=default_date,
                                                                    market=default_mkt),),
        parameters=RiskRequestParameters(raw_results=True),
        wait_for_results=True),)
    mocker.assert_called_with(risk_requests)


def price(mocker, priceable: Priceable):
    set_session()
    mocker.return_value = [[[[{'$type': 'Risk', 'val': 0.01}]]]]

    result = priceable.dollar_price()
    assert result == 0.01
    default_date = PricingContext.current.pricing_date
    default_mkt = PricingContext.current.market
    risk_requests = (risk.RiskRequest(
        positions=(RiskPosition(instrument=priceable, quantity=1),),
        measures=(risk.DollarPrice,),
        use_cache=PricingContext.current.use_server_cache,
        pricing_and_market_data_as_of=(PricingDateAndMarketDataAsOf(pricing_date=default_date,
                                                                    market=default_mkt),),
        parameters=RiskRequestParameters(raw_results=True),
        wait_for_results=True),)
    mocker.assert_called_with(risk_requests)


@mock.patch.object(GsRiskApi, '_exec')
def test_price(mocker):
    for priceable in priceables:
        price(mocker, priceable)


@mock.patch.object(GsRiskApi, '_exec')
def test_structured_calc(mocker):
    set_session()

    for priceable in priceables:
        if priceable.assetClass == AssetClass.Rates:
            for measure in (risk.IRDelta, risk.IRVega):
                structured_calc(mocker, priceable, measure)
        elif priceable.assetClass == AssetClass.FX:
            for measure in (risk.FXDelta, risk.FXGamma, risk.FXVega):
                structured_calc(mocker, priceable, measure)

    values = {
        '$type': 'RiskVector',
        'asset': [0.01, 0.015],
        'points': [
            {'type': 'IR', 'asset': 'USD', 'class_': 'Swap', 'point': '1y'},
            {'type': 'IR', 'asset': 'USD', 'class_': 'Swap', 'point': '2y'}
        ]
    }

    mocker.return_value = [[[[values]] * len(priceables)]]

    with PricingContext():
        delta_f = [p.calc(risk.IRDelta) for p in priceables if not isinstance(p, EqOption)]

    delta = risk.aggregate_risk(delta_f, threshold=0)

    assert len(delta) == 2


@mock.patch.object(GsRiskApi, '_exec')
def test_scalar_calc(mocker):
    for priceable in priceables:
        if priceable.assetClass == AssetClass.Equity:
            for measure in (risk.EqDelta, risk.EqGamma, risk.EqVega, risk.Theta):
                scalar_calc(mocker, priceable, measure)
        elif priceable.assetClass == AssetClass.Commod:
            for measure in (risk.CommodDelta, risk.CommodVega, risk.CommodTheta):
                scalar_calc(mocker, priceable, measure)


@mock.patch.object(GsRiskApi, '_exec')
def test_async_calc(mocker):
    set_session()

    mocker.return_value = [[[[{'$type': 'Risk', 'val': 0.01 * idx}] for idx in range(len(priceables))]]]

    with PricingContext():
        dollar_price_f = [p.dollar_price() for p in priceables]

    prices = tuple(f.result() for f in dollar_price_f)
    assert prices == tuple(0.01 * i for i in range(len(priceables)))


@mock.patch.object(GsRiskApi, '_exec')
def test_disjoint_priceables_measures(mocker):
    set_session()

    swap = priceables[4]
    swaption = priceables[6]

    mocker.return_value = [[[[{'$type': 'Risk', 'val': 0.01}]]]] * 2

    with PricingContext():
        swap_price_f = swap.price()
        swaption_dollar_price_f = swaption.dollar_price()

    assert swap_price_f.result() == 0.01
    assert swaption_dollar_price_f.result() == 0.01


def test_create_pretrade_execution_optimization():
    start_time = dt.datetime.utcnow()
    duration = dt.timedelta(hours=8)
    end_time = start_time + duration

    positions = [{"assetId": "MA4B66MW5E27UANLXW6", "quantity": 350},
                 {"assetId": "MA4B66MW5E27UAMFDDC", "quantity": 675}]

    request = OptimizationRequest(positions,
                                  type="APEX",
                                  executionStartTime=to_zulu_string(start_time),
                                  executionEndTime=to_zulu_string(end_time),
                                  waitForResults=False,
                                  parameters={"urgency": "MEDIUM", "participationRate": 0.1})

    set_session()
    with mock.patch.object(GsSession.current, '_post') as mocker:
        mock_response = {'optimizationId': 'LI0D2ND2JCFANFAN'}
        mocker.return_value = mock_response
        response = GsRiskApi.create_pretrade_execution_optimization(request)
        GsSession.current._post.assert_called_with('/risk/execution/pretrade', request)
        assert response == mock_response


def test_get_pretrade_execution_optimization():
    optimization_id = 'LI0D2ND2JCFANFAN'
    mock_response = {'id': optimization_id, 'analytics': {}, 'status': 'Completed'}

    set_session()
    with mock.patch.object(GsSession.current, '_get') as mocker:
        mocker.return_value = mock_response
        response = GsRiskApi.get_pretrade_execution_optimization(optimization_id)
        GsSession.current._get.assert_called_with('/risk/execution/pretrade/{}/results'.format(optimization_id))
        assert response == mock_response
