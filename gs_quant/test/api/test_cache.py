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
    # Don't use a mocker here as it will hold refs to things and break the cache removal test
    set_session()

    p1 = IRSwap('Pay', '10y', 'DKK')

    with PricingContext(use_cache=True):
        market_data_location = PricingContext.current.market_data_location
        pricing_date = PricingContext.current.pricing_date
        p1.price()

    assert PricingCache.get(p1, market_data_location, risk.Price, pricing_date)

    assert not PricingCache.get(p1, market_data_location, risk.IRDelta, pricing_date)

    # Assert that deleting the cached instrument removes it from the PricingCache
    # N.B, this may not work when debugging tests
    del p1
    p2 = IRSwap('Pay', '10y', 'DKK')
    assert not PricingCache.get(p2, market_data_location, risk.Price, pricing_date)

    with PricingContext(use_cache=True):
        p2.price()

    assert PricingCache.get(p2, market_data_location, risk.Price, pricing_date)

    # Change a property and assert that p2 is no longer cached
    p2.notional_currency = 'EUR'
    assert not PricingCache.get(p2, market_data_location, risk.Price, pricing_date)


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
    with HistoricalPricingContext(dates=dates, use_cache=True):
        market_data_location = PricingContext.current.market_data_location
        price_f = ir_swap.price()
    price_f.result()

    cached = PricingCache.get(ir_swap, market_data_location, risk.Price, dates)
    assert len(cached) == len(dates)

    cached_scalar = PricingCache.get(ir_swap, market_data_location, risk.Price, dates[0])
    assert isinstance(cached_scalar, float)

    dates = dates + (dt.date(2019, 10, 9),)
    cached2 = PricingCache.get(ir_swap, market_data_location, risk.Price, dates)
    assert len(cached2)
    assert len(cached2) < len(dates)

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

    with HistoricalPricingContext(dates=dates, use_cache=True):
        market_data_location = PricingContext.current.market_data_location
        risk_f = ir_swap.calc(risk.IRDelta)
    risk_frame = risk_f.result()

    assert isinstance(risk_frame, pd.DataFrame)
    assert len(risk_frame.index.unique()) == len(dates)
    cached3 = PricingCache.get(ir_swap, market_data_location, risk.IRDelta, dates)
    assert len(cached3.index.unique()) == len(dates)

    cached4 = PricingCache.get(ir_swap, market_data_location, risk.IRDelta, dates[0])
    assert len(cached4.index.unique()) == len(cached4)


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
    with HistoricalPricingContext(dates=dates, use_cache=True):
        market_data_location = PricingContext.current.market_data_location
        ir_swaption.price()
        ir_swaption.calc(risk.IRDelta)
        ir_swaption.calc(risk.IRVega)

    # make sure all the risk measures got cached correctly
    cached = PricingCache.get(ir_swaption, market_data_location, risk.Price, dates)
    assert len(cached) == len(dates)

    cached1 = PricingCache.get(ir_swaption, market_data_location, risk.IRDelta, dates)
    assert len(cached1.index.unique()) == len(dates)

    cached2 = PricingCache.get(ir_swaption, market_data_location, risk.IRVega, dates)
    assert len(cached2.index.unique()) == len(dates)

    # date not in cache
    cached3 = PricingCache.get(ir_swaption, market_data_location, risk.IRVega, dt.date(2019, 10, 11))
    assert cached3 is None

    # subset from cache
    subset = dates[0:2]
    cached4 = PricingCache.get(ir_swaption, market_data_location, risk.Price, subset)
    assert len(cached4) == len(subset)

    # intersection
    subset += (dt.date(2019, 10, 2),)
    cached5 = PricingCache.get(ir_swaption, market_data_location, risk.Price, subset)
    assert len(cached5) == len(subset) - 1
