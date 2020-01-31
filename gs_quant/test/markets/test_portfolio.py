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
from gs_quant.instrument import IRSwap
from gs_quant.markets import HistoricalPricingContext, PricingContext
from gs_quant.markets.portfolio import Portfolio
import gs_quant.risk as risk
from gs_quant.risk.results import PortfolioRiskResult
from gs_quant.session import Environment, GsSession


def set_session():
    from gs_quant.session import OAuth2Session
    OAuth2Session.init = mock.MagicMock(return_value=None)
    GsSession.use(Environment.PROD, 'client_id', 'secret')


@mock.patch.object(GsRiskApi, '_exec')
def test_portfolio(mocker):
    set_session()

    dollar_price_values = [
        [
            [
                {'date': '2019-10-07', 'value': 0.01}
            ],
            [
                {'date': '2019-10-07', 'value': 0.02}
            ],
            [
                {'date': '2019-10-07', 'value': 0.03}
            ]
        ]
    ]

    dollar_price_ir_delta_values = [
        [
            [
                {'date': '2019-10-07', 'value': 0.01}
            ],
            [
                {'date': '2019-10-07', 'value': 0.02}
            ],
            [
                {'date': '2019-10-07', 'value': 0.03}
            ]
        ],
        [
            [
                {'date': '2019-10-07', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
                 'point': '1y', 'value': 0.01},
                {'date': '2019-10-07', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
                 'point': '2y', 'value': 0.015}
            ],
            [
                {'date': '2019-10-07', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
                 'point': '1y', 'value': 0.02},
                {'date': '2019-10-07', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
                 'point': '2y', 'value': 0.025}
            ],
            [
                {'date': '2019-10-07', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
                 'point': '1y', 'value': 0.03},
                {'date': '2019-10-07', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
                 'point': '2y', 'value': 0.035}
            ]
        ]
    ]

    swap1 = IRSwap('Pay', '10y', 'USD', fixed_rate=0.01, name='swap1')
    swap2 = IRSwap('Pay', '10y', 'USD', fixed_rate=0.02, name='swap2')
    swap3 = IRSwap('Pay', '10y', 'USD', fixed_rate=0.03, name='swap3')

    portfolio = Portfolio((swap1, swap2, swap3))

    mocker.return_value = dollar_price_values
    prices: PortfolioRiskResult = portfolio.dollar_price()
    assert tuple(sorted(prices)) == (0.01, 0.02, 0.03)
    assert round(prices.aggregate(), 2) == 0.06
    assert prices[0] == 0.01
    assert prices[swap2] == 0.02
    assert prices['swap3'] == 0.03

    mocker.return_value = dollar_price_ir_delta_values
    result = portfolio.calc((risk.DollarPrice, risk.IRDelta))

    assert tuple(result[risk.DollarPrice]) == (0.01, 0.02, 0.03)
    assert result[risk.DollarPrice].aggregate() == 0.06
    assert result[risk.DollarPrice]['swap3'] == 0.03
    assert result[risk.DollarPrice]['swap3'] == result['swap3'][risk.DollarPrice]

    expected = risk.aggregate_risk([risk.DataFrameWithInfo(PricingContext.current.pricing_key, pd.DataFrame(v))
                                   for v in dollar_price_ir_delta_values[1]]).reset_index(drop=True)
    actual = result[risk.IRDelta].aggregate().raw_value
    assert actual.equals(expected)

    prices_only = result[risk.DollarPrice]
    assert tuple(prices) == tuple(prices_only)

    swap4 = IRSwap('Pay', '10y', 'USD', fixed_rate=0.01, name='swap4')
    portfolio.append(swap4)
    assert len(portfolio.instruments) == 4

    extracted_swap = portfolio.pop('swap2')
    assert extracted_swap == swap2
    assert len(portfolio.instruments) == 3

    swap_dict = {'swap_5': swap1,
                 'swap_6': swap2,
                 'swap_7': swap3}

    portfolio = Portfolio(swap_dict)
    assert len(portfolio) == 3


@mock.patch.object(GsRiskApi, '_exec')
def test_historical_pricing(mocker):
    set_session()

    dollar_price_ir_delta_values = [
        [
            [
                {'date': '2019-10-07', 'value': 0.01},
                {'date': '2019-10-08', 'value': 0.011},
                {'date': '2019-10-09', 'value': 0.012}
            ],
            [
                {'date': '2019-10-07', 'value': 0.02},
                {'date': '2019-10-08', 'value': 0.021},
                {'date': '2019-10-09', 'value': 0.022}
            ],
            [
                {'date': '2019-10-07', 'value': 0.03},
                {'date': '2019-10-08', 'value': 0.031},
                {'date': '2019-10-09', 'value': 0.032}
            ]
        ],
        [
            [
                {'date': '2019-10-07', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
                 'point': '1y', 'value': 0.01},
                {'date': '2019-10-07', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
                 'point': '2y', 'value': 0.015},
                {'date': '2019-10-08', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
                 'point': '1y', 'value': 0.011},
                {'date': '2019-10-08', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
                 'point': '2y', 'value': 0.0151},
                {'date': '2019-10-09', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
                 'point': '1y', 'value': 0.012},
                {'date': '2019-10-09', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
                 'point': '2y', 'value': 0.0152}
            ],
            [
                {'date': '2019-10-07', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
                 'point': '1y', 'value': 0.02},
                {'date': '2019-10-07', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
                 'point': '2y', 'value': 0.025},
                {'date': '2019-10-08', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
                 'point': '1y', 'value': 0.021},
                {'date': '2019-10-08', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
                 'point': '2y', 'value': 0.0251},
                {'date': '2019-10-09', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
                 'point': '1y', 'value': 0.022},
                {'date': '2019-10-09', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
                 'point': '2y', 'value': 0.0252}
            ],
            [
                {'date': '2019-10-07', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
                 'point': '1y', 'value': 0.03},
                {'date': '2019-10-07', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
                 'point': '2y', 'value': 0.035},
                {'date': '2019-10-08', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
                 'point': '1y', 'value': 0.031},
                {'date': '2019-10-08', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
                 'point': '2y', 'value': 0.0351},
                {'date': '2019-10-09', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
                 'point': '1y', 'value': 0.032},
                {'date': '2019-10-09', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
                 'point': '2y', 'value': 0.0352}
            ]
        ]
    ]

    mocker.return_value = dollar_price_ir_delta_values

    swap1 = IRSwap('Pay', '10y', 'USD', fixed_rate=0.01, name='swap1')
    swap2 = IRSwap('Pay', '10y', 'USD', fixed_rate=0.02, name='swap2')
    swap3 = IRSwap('Pay', '10y', 'USD', fixed_rate=0.03, name='swap3')

    portfolio = Portfolio((swap1, swap2, swap3))

    with HistoricalPricingContext(dates=(dt.date(2019, 10, 7), dt.date(2019, 10, 8), dt.date(2019, 10, 9))) as hpc:
        pricing_key = hpc.pricing_key
        results = portfolio.calc((risk.DollarPrice, risk.IRDelta))

    expected = risk.SeriesWithInfo(
        pricing_key,
        pd.Series(
            data=[0.06, 0.063, 0.066],
            index=[dt.date(2019, 10, 7), dt.date(2019, 10, 8), dt.date(2019, 10, 9)]
        ))

    actual = results[risk.DollarPrice].aggregate()

    assert actual.equals(expected)


@mock.patch.object(GsRiskApi, '_exec')
def test_duplicate_instrument(mocker):
    set_session()

    dollar_price_values = [
        [
            [
                {'date': '2019-10-07', 'value': 0.01}
            ],
            [
                {'date': '2019-10-07', 'value': 0.02}
            ],
            [
                {'date': '2019-10-07', 'value': 0.03}
            ]
        ]
    ]
    mocker.return_value = dollar_price_values

    swap1 = IRSwap('Pay', '10y', 'USD', fixed_rate=0.01, name='swap1')
    swap2 = IRSwap('Pay', '10y', 'USD', fixed_rate=0.02, name='swap2')
    swap3 = IRSwap('Pay', '10y', 'USD', fixed_rate=0.03, name='swap3')

    portfolio = Portfolio((swap1, swap2, swap3, swap1))
    assert portfolio.index('swap1') == (0, 3)
    assert portfolio.index('swap2') == 1

    prices: PortfolioRiskResult = portfolio.dollar_price()
    assert tuple(prices) == (0.01, 0.02, 0.03, 0.01)
    assert round(prices.aggregate(), 2) == 0.07
    assert prices[swap1] == (0.01, 0.01)


@mock.patch.object(GsRiskApi, '_exec')
def test_single_instrument(mocker):
    set_session()

    mocker.return_value = [[[{'date': '2019-10-07', 'value': 0.01}]]]

    swap1 = IRSwap('Pay', '10y', 'USD', fixed_rate=0.01, name='swap1')

    portfolio = Portfolio(swap1)
    assert portfolio.index('swap1') == 0

    prices: PortfolioRiskResult = portfolio.dollar_price()
    assert tuple(prices) == (0.01,)
    assert round(prices.aggregate(), 2) == 0.01
    assert prices[swap1] == 0.01


def test_results_with_resolution():
    set_session()

    dollar_price_ir_delta_values = [
        [
            [
                {'date': '2019-10-07', 'value': 0.01}
            ],
            [
                {'date': '2019-10-07', 'value': 0.02}
            ],
            [
                {'date': '2019-10-07', 'value': 0.03}
            ]
        ],
        [
            [
                {'date': '2019-10-07', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
                 'point': '1y', 'value': 0.01},
                {'date': '2019-10-07', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
                 'point': '2y', 'value': 0.015}
            ],
            [
                {'date': '2019-10-07', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
                 'point': '1y', 'value': 0.02},
                {'date': '2019-10-07', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
                 'point': '2y', 'value': 0.025}
            ],
            [
                {'date': '2019-10-07', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
                 'point': '1y', 'value': 0.03},
                {'date': '2019-10-07', 'marketDataType': 'IR', 'assetId': 'USD', 'pointClass': 'Swap',
                 'point': '2y', 'value': 0.035}
            ]
        ]
    ]

    swap1 = IRSwap('Pay', '10y', 'USD', name='swap1')
    swap2 = IRSwap('Pay', '10y', 'GBP', name='swap2')
    swap3 = IRSwap('Pay', '10y', 'EUR', name='swap3')

    portfolio = Portfolio((swap1, swap2, swap3))

    with mock.patch('gs_quant.api.gs.risk.GsRiskApi._exec') as mocker:
        mocker.return_value = dollar_price_ir_delta_values
        result = portfolio.calc((risk.DollarPrice, risk.IRDelta))

    # Check that we've got results
    assert result[swap1][risk.DollarPrice] is not None

    # Now resolve portfolio and assert that we can still get the result

    resolution_values = [
        [
            [{'fixedRate': 0.01}],
            [{'fixedRate': 0.007}],
            [{'fixedRate': 0.05}]
        ]
    ]

    orig_swap1 = swap1.clone()

    with mock.patch('gs_quant.api.gs.risk.GsRiskApi._exec') as mocker:
        mocker.return_value = resolution_values
        portfolio.resolve()

    # Assert that the resolved swap is indeed different and that we can retrieve results by both

    assert swap1 != orig_swap1
    assert result[swap1][risk.DollarPrice] is not None
    assert result[orig_swap1][risk.DollarPrice] is not None

    # Now reset the instruments and portfolio

    swap1 = IRSwap('Pay', '10y', 'USD', name='swap1')
    swap2 = IRSwap('Pay', '10y', 'GBP', name='swap2')
    swap3 = IRSwap('Pay', '10y', 'EUR', name='swap3')

    portfolio = Portfolio((swap1, swap2, swap3, swap1))

    with mock.patch('gs_quant.api.gs.risk.GsRiskApi._exec') as mocker:
        with PricingContext(dt.date(1066, 11, 14)):
            # Resolve under a different pricing date
            mocker.return_value = resolution_values
            portfolio.resolve()

    # Assert that after resolution under a different context, we cannot retrieve the result

    try:
        _ = result[swap1][risk.DollarPrice]
        assert False
    except KeyError:
        assert True
