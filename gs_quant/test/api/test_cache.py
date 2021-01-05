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
        mocker.return_value = [[[[{'$type': 'Risk', 'val': 0.07}]]]]

        with PricingContext(use_cache=True) as pc:
            p1.price()
            price_key = pc._PricingContext__risk_key(risk.Price, p1.provider)
            delta_key = pc._PricingContext__risk_key(risk.IRDelta, p1.provider)

        assert PricingCache.get(price_key, p1)

    assert not PricingCache.get(delta_key, p1)

    # Assert that deleting the cached instrument removes it from the PricingCache
    # N.B, this may not work when debugging tests
    del p1
    del mocker

    import gc
    gc.collect()

    p2 = IRSwap('Pay', '10y', 'DKK')
    p2_price_key = PricingContext.current._PricingContext__risk_key(risk.Price, p2.provider)
    # assert not PricingCache.get(p2_price_key)

    with mock.patch('gs_quant.api.gs.risk.GsRiskApi._exec') as mocker:
        mocker.return_value = [[[[{'$type': 'Risk', 'val': 0.07}]]]]

        with PricingContext(use_cache=True):
            p2_price = p2.price()

    assert PricingCache.get(p2_price_key, p2) == p2_price.result()

    # Assert that running under a scenario does not retrieve the base result
    with mock.patch('gs_quant.api.gs.risk.GsRiskApi._exec') as mocker:
        mocker.return_value = [[[[{'$type': 'Risk', 'val': 0.08}]]]]

        with risk.RollFwd(date='1m'), PricingContext(use_cache=True) as spc:
            # Don't want the price without the scenario
            scenario_risk_key = spc._PricingContext__risk_key(risk.Price, p2.provider)
            assert not PricingCache.get(scenario_risk_key, p2)
            scenario_price = p2.price()

        assert PricingCache.get(scenario_risk_key, p2) == scenario_price.result()

        with PricingContext(use_cache=True) as pc, risk.RollFwd(date='1m'):
            cached_scenario_price = PricingCache.get(pc._PricingContext__risk_key(risk.Price, p2.provider), p2)

    # Check that we get the cached scenario price
    assert cached_scenario_price == scenario_price.result()

    # Check the base result is still correct
    assert PricingCache.get(p2_price_key, p2) == p2_price.result()

    # Assert that caching respects parameters, such as csa
    with mock.patch('gs_quant.api.gs.risk.GsRiskApi._exec') as mocker:
        mocker.return_value = [[[[{'$type': 'Risk', 'val': 0.08}]]]]

        with PricingContext(use_cache=True, csa_term='INVALID') as pc:
            # Don't want the price with default csa
            assert not PricingCache.get(pc._PricingContext__risk_key(risk.Price, p2.provider), p2)
            csa_price = p2.price()

        with PricingContext(use_cache=True, csa_term='INVALID') as pc:
            cached_csa_price = PricingCache.get(pc._PricingContext__risk_key(risk.Price, p2.provider), p2)

    # Check that we get the cached csa price
    assert cached_csa_price == csa_price.result()

    # Check the base result is still correct
    assert PricingCache.get(p2_price_key, p2) == p2_price.result()

    # Change a property and assert that p2 is no longer cached
    p2.notional_currency = 'EUR'
    assert not PricingCache.get(p2_price_key, p2)


@mock.patch.object(GsRiskApi, '_exec')
def test_cache_subset(mocker):
    set_session()

    ir_swap = IRSwap('Pay', '10y', 'DKK')

    values = [
        {'$type': 'Risk', 'val': 0.01}
    ]
    mocker.return_value = [[[values]], [[values]]]

    dates = (dt.date(2019, 10, 7), dt.date(2019, 10, 8))
    with HistoricalPricingContext(dates=dates, use_cache=True):
        price_f = ir_swap.price()
    price_f.result()

    for date in dates:
        risk_key = PricingContext(pricing_date=date)._PricingContext__risk_key(risk.Price, ir_swap.provider)
        cached_scalar = PricingCache.get(risk_key, ir_swap)
        assert cached_scalar
        assert isinstance(cached_scalar, float)

    risk_key = PricingContext(pricing_date=dt.date(2019, 10, 9))._PricingContext__risk_key(risk.Price,
                                                                                           ir_swap.provider)
    cached2 = PricingCache.get(risk_key, ir_swap)
    assert cached2 is None

    values = [
        {
            '$type': 'RiskVector',
            'asset': [0.01, 0.015],
            'points': [
                {'type': 'IR', 'asset': 'USD', 'class_': 'Swap', 'point': '1y'},
                {'type': 'IR', 'asset': 'USD', 'class_': 'Swap', 'point': '2y'}
            ]
        }
    ]

    # Check that we can return the same values from the cache, after calculating once (with return values set to None)

    for return_values in ([[[values]], [[values]], [[values]]], None):
        mocker.return_value = return_values

        with HistoricalPricingContext(dates=dates, use_cache=True):
            risk_f = ir_swap.calc(risk.IRDelta)

        risk_frame = risk_f.result()

        assert isinstance(risk_frame, pd.DataFrame)
        assert len(risk_frame.index.unique()) == len(dates)


@mock.patch.object(GsRiskApi, '_exec')
def test_multiple_measures(mocker):
    day = [
        [
            [{
                '$type': 'RiskVector',
                'asset': [0.01, 0.015],
                'points': [
                    {'type': 'IR Vol', 'asset': 'USD-LIBOR-BBA', 'class_': 'Swap', 'point': '1y'},
                    {'type': 'IR Vol', 'asset': 'USD-LIBOR-BBA', 'class_': 'Swap', 'point': '2y'}
                ]
            }]
        ],
        [
            [{
                '$type': 'RiskVector',
                'asset': [0.01, 0.015],
                'points': [
                    {'type': 'IR', 'asset': 'USD', 'class_': 'Swap', 'point': '1y'},
                    {'type': 'IR', 'asset': 'USD', 'class_': 'Swap', 'point': '2y'}
                ]
            }],
        ],
        [
            [{'$type': 'Risk', 'val': 0.01}]
        ]
    ]

    mocker.return_value = [day, day, day]

    set_session()

    ir_swaption = IRSwaption('Pay', '10y', 'USD')

    dates = (dt.date(2019, 10, 7), dt.date(2019, 10, 8), dt.date(2019, 10, 9))
    with HistoricalPricingContext(dates=dates, use_cache=True):
        ir_swaption.price()
        ir_swaption.calc(risk.IRDelta)
        ir_swaption.calc(risk.IRVega)

    # make sure all the risk measures got cached correctly
    for date in dates:
        with PricingContext(pricing_date=date) as pc:
            for risk_measure in (risk.Price, risk.IRDelta, risk.IRVega):
                val = PricingCache.get(pc._PricingContext__risk_key(risk_measure, ir_swaption.provider), ir_swaption)
                assert val is not None

    with PricingContext(pricing_date=dt.date(2019, 10, 11)) as pc:
        for risk_measure in (risk.Price, risk.IRDelta, risk.IRVega):
            val = PricingCache.get(pc._PricingContext__risk_key(risk_measure, ir_swaption.provider), ir_swaption)
            assert val is None
