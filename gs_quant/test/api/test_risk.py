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

from gs_quant.api.gs.risk import GsRiskApi, RiskModelRequest
from gs_quant.base import Priceable
from gs_quant.common import AssetClass
from gs_quant.instrument import CommodSwap, EqForward, EqOption, FXOption, IRBasisSwap, IRSwap, IRSwaption, IRCap, IRFloor
from gs_quant.markets import PricingContext
import gs_quant.risk as risk
from gs_quant.session import Environment, GsSession

import pandas as pd
from unittest import mock

priceables = (
    CommodSwap('Electricity', '1y'),
    EqForward('GS.N', '1y', 100.0),
    EqOption('GS.N', '3m', 'ATMF', 'Call', 'European'),
    FXOption('EUR', 'USD', '1y', 'Call', strike='ATMF'),
    IRSwap('Pay', '10y', 'USD'),
    IRBasisSwap('10y', 'USD', 'EUR'),
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

    values = [
        {'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap', 'point': '1y', 'value': 0.01},
        {'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap', 'point': '2y', 'value': 0.015}
    ]
    mocker.return_value = [[values]]

    result = priceable.calc(measure)
    expected = risk.sort_risk(pd.DataFrame(values))
    assert result.equals(expected)
    risk_request = risk.RiskRequest(
        positions=(risk.RiskPosition(priceable, 1),),
        measures=(measure,),
        pricingLocation=PricingContext.current.market_data_location,
        pricingAndMarketDataAsOf=PricingContext.current._pricing_market_data_as_of,
        waitForResults=True)
    mocker.assert_called_with(risk_request)


def scalar_calc(mocker, priceable: Priceable, measure: risk.RiskMeasure):
    set_session()
    mocker.return_value = [[[{'value': 0.01}]]]

    result = priceable.calc(measure)
    assert result == 0.01
    risk_request = risk.RiskRequest(
        positions=(risk.RiskPosition(priceable, 1),),
        measures=(measure,),
        pricingLocation=PricingContext.current.market_data_location,
        pricingAndMarketDataAsOf=PricingContext.current._pricing_market_data_as_of,
        waitForResults=True)
    mocker.assert_called_with(risk_request)


def price(mocker, priceable: Priceable):
    set_session()
    mocker.return_value = [[[{'value': 0.01}]]]

    result = priceable.dollar_price()
    assert result == 0.01
    risk_request = risk.RiskRequest(
        positions=(risk.RiskPosition(priceable, 1),),
        measures=(risk.DollarPrice,),
        pricingLocation=PricingContext.current.market_data_location,
        pricingAndMarketDataAsOf=PricingContext.current._pricing_market_data_as_of,
        waitForResults=True)
    mocker.assert_called_with(risk_request)


def test_suggest_risk_model(mocker):
    set_session()

    marquee_id_1 = 'MQA1234567890'
    marquee_id_2 = 'MQA4567890123'

    inputs = RiskModelRequest((marquee_id_1, marquee_id_2))

    mock_response = {'results':[
        {'model': 'AXUS4S', 'businessDate': '2019-03-04'},
        {'model': 'AXWW21M', 'businessDate': '2019-03-04'}
    ]}

    expected_response = 'AXUS4S'

    # mock GsSession
    mocker.patch.object(GsSession.current, '_post', return_value=mock_response)
    GsSession.current._post.risk_models('/risk/models', payload=inputs)

    # run test
    response = GsRiskApi._suggest_risk_model(inputs)

    assert response == expected_response


@mock.patch.object(GsRiskApi, '_exec')
def test_price(mocker):
    for priceable in priceables:
        price(mocker, priceable)


@mock.patch.object(GsRiskApi, '_exec')
def test_structured_calc(mocker):
    set_session()

    for priceable in priceables:
        if priceable.assetClass == AssetClass.Rates:
            for measure in (risk.IRDelta, risk.IRGamma, risk.IRVega):
                structured_calc(mocker, priceable, measure)
        elif priceable.assetClass == AssetClass.Commod:
            for measure in (risk.CommodDelta, risk.CommodVega, risk.CommodTheta):
                structured_calc(mocker, priceable, measure)
        elif priceable.assetClass == AssetClass.FX:
            for measure in (risk.FXDelta, risk.FXGamma, risk.FXVega):
                structured_calc(mocker, priceable, measure)

    values = [
        {'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap', 'point': '1y', 'value': 0.01},
        {'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap', 'point': '2y', 'value': 0.015}
    ]

    mocker.return_value = [[values] * len(priceables)]

    with risk.PricingContext():
        delta_f = [p.calc(risk.IRDelta) for p in priceables]

    delta = risk.aggregate_risk(delta_f, threshold=0)

    assert len(delta) == 2


@mock.patch.object(GsRiskApi, '_exec')
def test_scalar_calc(mocker):
    for priceable in priceables:
        if priceable.assetClass == AssetClass.Equity:
            for measure in (risk.EqDelta, risk.EqGamma, risk.EqVega, risk.Theta):
                scalar_calc(mocker, priceable, measure)


@mock.patch.object(GsRiskApi, '_exec')
def test_async_calc(mocker):
    set_session()

    results = [[{'value': 0.01 * idx}] for idx in range(len(priceables))]
    mocker.return_value = [results]

    with risk.PricingContext():
        dollar_price_f = [p.dollar_price() for p in priceables]

    prices = tuple(f.result() for f in dollar_price_f)
    assert prices == tuple(0.01 * i for i in range(len(priceables)))
