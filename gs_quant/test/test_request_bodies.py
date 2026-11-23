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

import asyncio
import contextlib
import datetime as dt
import json
import pathlib
from unittest import mock

import httpx
import msgpack
import pytest
import requests

from gs_quant.api.gs.backtests import GsBacktestApiAsync
from gs_quant.api.gs.backtests_xasset.apis import GsBacktestXassetApiAsync
from gs_quant.api.gs.backtests_xasset.request import BasicBacktestRequest, DateConfig, GenericBacktestRequest
from gs_quant.api.gs.backtests_xasset.response_datatypes.backtest_datatypes import Configuration, Trade
from gs_quant.api.gs.data import GsDataApi
from gs_quant.api.gs.portfolios import GsPortfolioApi
from gs_quant.api.gs.risk import GsRiskApi
from gs_quant.backtests.actions import AddTradeAction
from gs_quant.backtests.strategy import Strategy
from gs_quant.backtests.triggers import PeriodicTrigger, PeriodicTriggerRequirements
from gs_quant.common import (
    MarketDataScenario,
    Position,
    PositionSet,
    PricingDateAndMarketDataAsOf,
    PricingLocation,
    RiskPosition,
    RiskRequestParameters,
)
from gs_quant.markets import CloseMarket
from gs_quant.risk import Price, RiskRequest
from gs_quant.session import Environment, GsSession
from gs_quant.target.backtests import (
    Backtest,
    BacktestStrategyUnderlier,
    BacktestTradingParameters,
    BacktestType,
    FlowVolBacktestMeasure,
    VolatilityFlowBacktestParameters,
)
from gs_quant.target.data import DataQuery
from gs_quant.test import dataclass_test_utils as utils
from gs_quant.workflow import (
    BinaryImageComments,
    DeltaHedge,
    SaveQuoteRequest,
    VisualStructuringReport,
    WorkflowEntitlement,
    WorkflowEntitlements,
)

RESOURCES = pathlib.Path(__file__).parent / 'resources' / 'request_bodies'
DOMAIN = 'https://marquee.test'
BACKTEST_RESPONSE = {'measures': {}, 'portfolio': {}, 'transactions': {}}


class _OfflineSession(GsSession):
    def __init__(self):
        super().__init__(DOMAIN, Environment.DEV)

    def _authenticate(self):
        pass


class _Transport:
    def __init__(self):
        self.sent = []
        self.response = {}

    def _record(self, method, url, kwargs, body):
        content_type = kwargs['headers']['Content-Type']
        if content_type == 'application/x-msgpack':
            encoding, decoded = 'msgpack', utils.type_tagged(msgpack.unpackb(body, raw=False, strict_map_key=False))
        else:
            encoding, decoded = 'json', json.loads(body)
        self.sent.append(
            {
                'method': method,
                'path': url.removeprefix(DOMAIN),
                'contentType': content_type,
                'encoding': encoding,
                'body': decoded,
            }
        )
        return httpx.Response(200, json=self.response)

    def sync_request(self, method, url, **kwargs):
        return self._record(method, url, kwargs, kwargs.get('data'))

    async def async_request(self, method, url, **kwargs):
        return self._record(method, url, kwargs, kwargs.get('content'))


@contextlib.contextmanager
def patched_transport():
    transport = _Transport()
    with mock.patch.object(requests.Session, 'request', side_effect=transport.sync_request):
        with mock.patch.object(httpx.AsyncClient, 'request', side_effect=transport.async_request):
            with _OfflineSession():
                yield transport


@pytest.fixture
def transport():
    with patched_transport() as recorder:
        yield recorder


def _risk_request(pricing_date: dt.date) -> RiskRequest:
    swap, option = utils.irswap(), utils.eq_option()
    return RiskRequest(
        tuple(
            RiskPosition(instrument=i, quantity=i.instrument_quantity, instrument_name=i.name) for i in (swap, option)
        ),
        (Price, utils.parameterised_risk_measure()),
        pricing_and_market_data_as_of=(
            PricingDateAndMarketDataAsOf(
                pricing_date=pricing_date, market=CloseMarket(pricing_date, PricingLocation.NYC, check=False)
            ),
        ),
        parameters=RiskRequestParameters(csa_term='USD-1', raw_results=True),
        wait_for_results=True,
        scenario=MarketDataScenario(scenario=utils.market_data_shock_scenario()),
    )


def _risk_calculate_json():
    with mock.patch.object(GsRiskApi, 'USE_MSGPACK', False):
        GsRiskApi._exec((_risk_request(dt.date(2021, 3, 4)),))


def _risk_calculate_bulk_msgpack():
    GsRiskApi._exec((_risk_request(dt.date(2021, 3, 4)), _risk_request(dt.date(2021, 3, 5))))


def _save_workflow_quote_msgpack():
    swap = utils.irswap()
    report = VisualStructuringReport(
        position_set_id='ps1',
        as_of_date=dt.date(2021, 3, 4),
        hedge_instruction=DeltaHedge(),
        comments=(BinaryImageComments(data='abc', img_type='png'),),
    )
    GsPortfolioApi.save_workflow_quote(
        SaveQuoteRequest(
            positions=(
                PositionSet(positions=(Position(instrument=swap, quantity=1.0),), position_date=dt.date(2021, 3, 4)),
            ),
            measures=(Price,),
            pricing_and_market_data_as_of=(PricingDateAndMarketDataAsOf(pricing_date=dt.date(2021, 3, 4)),),
            reports=(report,),
            entitlements=WorkflowEntitlements(readers=(WorkflowEntitlement(type_='user', value='abc'),)),
        )
    )


def _backtest_calculate():
    backtest = Backtest(
        name='Flow Vol Backtest',
        mq_symbol='SPX',
        parameters=VolatilityFlowBacktestParameters(
            trading_parameters=BacktestTradingParameters(
                quantity=1, roll_frequency='1m', scaling_method='fixedQuantity'
            ),
            index_initial_value=100.0,
            underliers=(BacktestStrategyUnderlier(instrument=utils.eq_option(), market_model='SFK'),),
        ),
        start_date=dt.date(2021, 1, 4),
        end_date=dt.date(2021, 3, 4),
        type_=BacktestType.Volatility_Flow,
        asset_class='Equity',
        currency='USD',
        cost_netting=False,
    )
    asyncio.run(GsBacktestApiAsync.run_backtest(backtest, correlation_id='abc'))


def _xasset_generic_backtest():
    request = GenericBacktestRequest(
        strategy=utils.eleven_trigger_strategy(),
        dates=(dt.date(2023, 4, 11), dt.date(2023, 4, 12)),
        measures=(Price,),
    )
    asyncio.run(GsBacktestXassetApiAsync.calculate_generic_backtest(request))


def _xasset_basic_backtest():
    option = utils.eq_option().clone(expiration_date=dt.date(2021, 6, 18))
    request = BasicBacktestRequest(
        DateConfig(dt.date(2021, 1, 4), dt.date(2021, 3, 4)),
        (Trade((option,), '1m', (dt.date(2021, 1, 4),), '1m', None, 1.0, None),),
        (FlowVolBacktestMeasure.PNL,),
        configuration=Configuration(),
    )
    asyncio.run(GsBacktestXassetApiAsync.calculate_basic_backtest(request))


CASES = {
    'risk_calculate_json': (_risk_calculate_json, []),
    'risk_calculate_bulk_msgpack': (_risk_calculate_bulk_msgpack, []),
    'save_workflow_quote_msgpack': (_save_workflow_quote_msgpack, {'results': 'abc'}),
    'backtest_calculate': (_backtest_calculate, {'RiskData': {}}),
    'xasset_generic_backtest': (_xasset_generic_backtest, BACKTEST_RESPONSE),
    'xasset_basic_backtest': (_xasset_basic_backtest, BACKTEST_RESPONSE),
}


def data_query_cache_key() -> dict:
    query = DataQuery(
        where={'assetId': ['MA123']},
        start_date=dt.date(2021, 3, 4),
        end_date=dt.date(2021, 3, 5),
        fields=('price', 'volume'),
    )
    url, method, json_kwargs = GsDataApi._construct_cache_key('/data/DATASET/query', payload=query)
    return {'path': url, 'method': method, 'payload': json.loads(json_kwargs['payload'])}


def _expected(name: str) -> dict:
    return json.loads((RESOURCES / f'{name}.json').read_text())


@pytest.mark.parametrize('case', CASES)
def test_request_body(transport, case):
    call, transport.response = CASES[case]
    call()
    assert len(transport.sent) == 1
    assert utils.type_tagged(transport.sent[0]) == utils.type_tagged(_expected(case))


def test_data_query_cache_key():
    assert utils.type_tagged(data_query_cache_key()) == utils.type_tagged(_expected('data_query_cache_key'))


@pytest.mark.xfail(strict=True, reason='D-13: Strategy.to_json() raises for an instrument with a date field')
def test_generic_backtest_with_dated_instrument(transport):
    swap = utils.irswap()
    trigger = PeriodicTrigger(
        PeriodicTriggerRequirements(dt.date(2021, 3, 4), dt.date(2021, 6, 4), '1m'), AddTradeAction(swap, name='Add')
    )
    request = GenericBacktestRequest(
        strategy=Strategy(swap, trigger), dates=DateConfig(dt.date(2021, 3, 4), dt.date(2021, 6, 4)), measures=(Price,)
    )
    transport.response = BACKTEST_RESPONSE
    asyncio.run(GsBacktestXassetApiAsync.calculate_generic_backtest(request))
    assert transport.sent[0]['body']['strategy']['initial_portfolio'][0]['effective_date'] == '2021-03-04'
