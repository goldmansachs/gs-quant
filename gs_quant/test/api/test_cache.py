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

from gs_quant.api.gs.risk import GsRiskApi
from gs_quant.instrument import IRSwap, IRSwaption
from gs_quant.markets import HistoricalPricingContext, PricingCache, PricingContext
import gs_quant.risk as risk
from gs_quant.session import Environment, GsSession


def set_session():
    from gs_quant.session import OAuth2Session
    OAuth2Session.init = mock.MagicMock(return_value=None)
    GsSession.use(Environment.PROD, 'client_id', 'secret')
    PricingCache.clear()


def test_cache_addition_removal():
    set_session()

    p1 = IRSwap('Pay', '10y', 'DKK')

    with mock.patch('gs_quant.api.gs.risk.GsRiskApi._exec') as mocker:
        mocker.return_value = [[[{'date': '2019-10-07', 'value': 0.07}]]]

        with PricingContext(use_cache=True):
            p1.price()

        assert PricingCache.get(p1, risk.Price)

    assert not PricingCache.get(p1, risk.IRDelta)

    # Assert that deleting the cached instrument removes it from the PricingCache
    # N.B, this may not work when debugging tests
    del p1
    del mocker

    import gc
    gc.collect()

    p2 = IRSwap('Pay', '10y', 'DKK')
    assert not PricingCache.get(p2, risk.Price)

    with mock.patch('gs_quant.api.gs.risk.GsRiskApi._exec') as mocker:
        mocker.return_value = [[[{'date': '2019-10-07', 'value': 0.07}]]]

        with PricingContext(use_cache=True):
            p2_price = p2.price()

    assert PricingCache.get(p2, risk.Price) == p2_price.result()

    # Assert that running under a scenario does not retrieve the base result
    with mock.patch('gs_quant.api.gs.risk.GsRiskApi._exec') as mocker:
        mocker.return_value = [[[{'date': '2019-10-07', 'value': 0.08}]]]

        with risk.CarryScenario(time_shift=30), PricingContext(use_cache=True) as spc:
            # Don't want the price without the scenario
            assert not PricingCache.get(p2, risk.Price)
            scenario_price = p2.price()
            scenario_pricing_key = spc.pricing_key

        assert PricingCache.get(p2, risk.Price, scenario_pricing_key) == scenario_price.result()

        with PricingContext(use_cache=True), risk.CarryScenario(time_shift=30):
            cached_scenario_price = PricingCache.get(p2, risk.Price)

    # Check that we get the cached scenario price
    assert cached_scenario_price == scenario_price.result()

    # Check the base result is still correct
    assert PricingCache.get(p2, risk.Price) == p2_price.result()

    # Assert that caching respects parameters, such as csa
    with mock.patch('gs_quant.api.gs.risk.GsRiskApi._exec') as mocker:
        mocker.return_value = [[[{'date': '2019-10-07', 'value': 0.08}]]]

        with PricingContext(use_cache=True, csa_term='INVALID'):
            # Don't want the price with default csa
            assert not PricingCache.get(p2, risk.Price)
            csa_price = p2.price()

        with PricingContext(use_cache=True, csa_term='INVALID'):
            cached_csa_price = PricingCache.get(p2, risk.Price)

    # Check that we get the cached csa price
    assert cached_csa_price == csa_price.result()

    # Check the base result is still correct
    assert PricingCache.get(p2, risk.Price) == p2_price.result()

    # Change a property and assert that p2 is no longer cached
    p2.notional_currency = 'EUR'
    assert not PricingCache.get(p2, risk.Price)


@mock.patch.object(GsRiskApi, '_exec')
def test_cache_subset(mocker):
    set_session()

    ir_swap = IRSwap('Pay', '10y', 'DKK')

    values = [
        {'date': '2019-10-07', 'value': 0.01},
        {'date': '2019-10-08', 'value': 0.01}
    ]
    mocker.return_value = [[values]]

    dates = (dt.date(2019, 10, 7), dt.date(2019, 10, 8))
    with HistoricalPricingContext(dates=dates, use_cache=True) as hpc:
        pricing_key = hpc.pricing_key
        price_f = ir_swap.price()
    price_f.result()

    cached = PricingCache.get(ir_swap, risk.Price, pricing_key)
    assert len(cached) == len(dates)

    cached_scalar = PricingCache.get(ir_swap, risk.Price, PricingContext(pricing_date=dates[0]).pricing_key)
    assert isinstance(cached_scalar, float)

    dates = dates + (dt.date(2019, 10, 9),)
    pricing_key = HistoricalPricingContext(dates=dates).pricing_key
    cached2 = PricingCache.get(ir_swap, risk.Price, pricing_key)
    assert cached2 is None

    cached3 = PricingCache.get(ir_swap, risk.Price, pricing_key, return_partial=True)
    assert len(cached3) < len(dates)

    values = [
        {'date': '2019-10-07', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
         'point': '1y', 'value': 0.01},
        {'date': '2019-10-07', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
         'point': '2y', 'value': 0.015},
        {'date': '2019-10-08', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
         'point': '1y', 'value': 0.01},
        {'date': '2019-10-08', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
         'point': '2y', 'value': 0.015},
        {'date': '2019-10-09', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
         'point': '1y', 'value': 0.01},
        {'date': '2019-10-09', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
         'point': '2y', 'value': 0.015}
    ]
    mocker.return_value = [[values]]

    with HistoricalPricingContext(dates=dates, use_cache=True) as hpc:
        pricing_key = hpc.pricing_key
        risk_f = ir_swap.calc(risk.IRDelta)

    risk_frame = risk_f.result()

    assert isinstance(risk_frame, pd.DataFrame)
    assert len(risk_frame.index.unique()) == len(dates)
    cached4 = PricingCache.get(ir_swap, risk.IRDelta, pricing_key)
    assert len(cached4.index.unique()) == len(dates)

    cached5 = PricingCache.get(ir_swap, risk.IRDelta, PricingContext(pricing_date=dates[0]).pricing_key)
    assert len(cached5.index.unique()) == len(cached5)


@mock.patch.object(GsRiskApi, '_exec')
def test_multiple_measures(mocker):
    values = [
        [
            [
                {'date': '2019-10-07', 'marketDataType': 'IR Vol', 'assetId': 'USD-LIBOR-BBA', 'pointClass': 'Swap',
                 'point': '1y', 'value': 0.01},
                {'date': '2019-10-07', 'marketDataType': 'IR Vol', 'assetId': 'USD-LIBOR-BBA', 'pointClass': 'Swap',
                 'point': '2y', 'value': 0.015},
                {'date': '2019-10-08', 'marketDataType': 'IR Vol', 'assetId': 'USD-LIBOR-BBA', 'pointClass': 'Swap',
                 'point': '1y', 'value': 0.01},
                {'date': '2019-10-08', 'marketDataType': 'IR Vol', 'assetId': 'USD-LIBOR-BBA', 'pointClass': 'Swap',
                 'point': '2y', 'value': 0.015},
                {'date': '2019-10-09', 'marketDataType': 'IR Vol', 'assetId': 'USD-LIBOR-BBA', 'pointClass': 'Swap',
                 'point': '1y', 'value': 0.01},
                {'date': '2019-10-09', 'marketDataType': 'IR Vol', 'assetId': 'USD-LIBOR-BBA', 'pointClass': 'Swap',
                 'point': '2y', 'value': 0.015}
            ]
        ],
        [
            [
                {'date': '2019-10-07', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
                 'point': '1y', 'value': 0.01},
                {'date': '2019-10-07', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
                 'point': '2y', 'value': 0.015},
                {'date': '2019-10-08', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
                 'point': '1y', 'value': 0.01},
                {'date': '2019-10-08', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
                 'point': '2y', 'value': 0.015},
                {'date': '2019-10-09', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
                 'point': '1y', 'value': 0.01},
                {'date': '2019-10-09', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
                 'point': '2y', 'value': 0.015}
            ]
        ],
        [
            [
                {'date': '2019-10-07', 'value': 0.01},
                {'date': '2019-10-08', 'value': 0.01},
                {'date': '2019-10-09', 'value': 0.01}
            ]
        ]
    ]
    mocker.return_value = values

    set_session()

    ir_swaption = IRSwaption('Pay', '10y', 'USD')

    dates = (dt.date(2019, 10, 7), dt.date(2019, 10, 8), dt.date(2019, 10, 9))
    with HistoricalPricingContext(dates=dates, use_cache=True) as hpc:
        pricing_key = hpc.pricing_key
        ir_swaption.price()
        ir_swaption.calc(risk.IRDelta)
        ir_swaption.calc(risk.IRVega)

    # make sure all the risk measures got cached correctly
    cached = PricingCache.get(ir_swaption, risk.Price, pricing_key)
    assert len(cached) == len(dates)

    cached1 = PricingCache.get(ir_swaption, risk.IRDelta, pricing_key)
    assert len(cached1.index.unique()) == len(dates)

    cached2 = PricingCache.get(ir_swaption, risk.IRVega, pricing_key)
    assert len(cached2.index.unique()) == len(dates)

    # date not in cache
    cached3 = PricingCache.get(ir_swaption, risk.IRVega, PricingContext(pricing_date=dt.date(2019, 10, 11)).pricing_key)
    assert cached3 is None

    # subset from cache
    subset_key = HistoricalPricingContext(dates=dates[0:2]).pricing_key
    cached4 = PricingCache.get(ir_swaption, risk.Price, subset_key)
    assert len(cached4) == 2

    # intersection
    subset_key = HistoricalPricingContext(dates=dates[0:2] + (dt.date(2019, 10, 2),)).pricing_key
    cached5 = PricingCache.get(ir_swaption, risk.Price, subset_key, return_partial=True)
    assert len(cached5) == 2
