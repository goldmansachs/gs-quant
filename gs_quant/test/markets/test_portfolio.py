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
import datetime as dt
from unittest import mock

import pandas as pd

import gs_quant.risk as risk
from gs_quant.api.gs.risk import GsRiskApi
from gs_quant.datetime import business_day_offset
from gs_quant.instrument import IRSwap, IRSwaption
from gs_quant.markets import HistoricalPricingContext, PricingContext, BackToTheFuturePricingContext
from gs_quant.markets.portfolio import Portfolio
from gs_quant.risk.results import PortfolioPath, PortfolioRiskResult
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
                {'$type': 'Risk', 'val': 0.01}
            ],
            [
                {'$type': 'Risk', 'val': 0.02}
            ],
            [
                {'$type': 'Risk', 'val': 0.03}
            ]
        ]
    ]

    dollar_price_ir_delta_values = [
        [
            [
                {'$type': 'Risk', 'val': 0.01}
            ],
            [
                {'$type': 'Risk', 'val': 0.02}
            ],
            [
                {'$type': 'Risk', 'val': 0.03}
            ]
        ],
        [
            [
                {
                    '$type': 'RiskVector',
                    'asset': [0.01, 0.015],
                    'points': [
                        {'type': 'IR', 'asset': 'USD', 'class_': 'Swap', 'point': '1y'},
                        {'type': 'IR', 'asset': 'USD', 'class_': 'Swap', 'point': '2y'}
                    ]
                }
            ],
            [
                {
                    '$type': 'RiskVector',
                    'asset': [0.02, 0.025],
                    'points': [
                        {'type': 'IR', 'asset': 'USD', 'class_': 'Swap', 'point': '1y'},
                        {'type': 'IR', 'asset': 'USD', 'class_': 'Swap', 'point': '2y'}
                    ]
                }
            ],
            [
                {
                    '$type': 'RiskVector',
                    'asset': [0.03, 0.035],
                    'points': [
                        {'type': 'IR', 'asset': 'USD', 'class_': 'Swap', 'point': '1y'},
                        {'type': 'IR', 'asset': 'USD', 'class_': 'Swap', 'point': '2y'}
                    ]
                }
            ]
        ]
    ]

    swap1 = IRSwap('Pay', '10y', 'USD', fixed_rate=0.01, name='swap1')
    swap2 = IRSwap('Pay', '10y', 'USD', fixed_rate=0.02, name='swap2')
    swap3 = IRSwap('Pay', '10y', 'USD', fixed_rate=0.03, name='swap3')

    portfolio = Portfolio((swap1, swap2, swap3))

    mocker.return_value = [dollar_price_values]
    prices: PortfolioRiskResult = portfolio.dollar_price()
    assert tuple(sorted(prices)) == (0.01, 0.02, 0.03)
    assert round(prices.aggregate(), 2) == 0.06
    assert prices[0] == 0.01
    assert prices[swap2] == 0.02
    assert prices['swap3'] == 0.03

    mocker.return_value = [dollar_price_ir_delta_values]
    result = portfolio.calc((risk.DollarPrice, risk.IRDelta))

    assert tuple(result[risk.DollarPrice]) == (0.01, 0.02, 0.03)
    assert result[risk.DollarPrice].aggregate() == 0.06
    assert result[risk.DollarPrice]['swap3'] == 0.03
    assert result[risk.DollarPrice]['swap3'] == result['swap3'][risk.DollarPrice]

    assert result[risk.IRDelta].aggregate().value.sum() == 0.135

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

    day1 = [
        [
            [{'$type': 'Risk', 'val': 0.01}],
            [{'$type': 'Risk', 'val': 0.02}],
            [{'$type': 'Risk', 'val': 0.03}],
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
            [{
                '$type': 'RiskVector',
                'asset': [0.02, 0.025],
                'points': [
                    {'type': 'IR', 'asset': 'USD', 'class_': 'Swap', 'point': '1y'},
                    {'type': 'IR', 'asset': 'USD', 'class_': 'Swap', 'point': '2y'}
                ]
            }],
            [{
                '$type': 'RiskVector',
                'asset': [0.03, 0.035],
                'points': [
                    {'type': 'IR', 'asset': 'USD', 'class_': 'Swap', 'point': '1y'},
                    {'type': 'IR', 'asset': 'USD', 'class_': 'Swap', 'point': '2y'}
                ]
            }]
        ]
    ]

    day2 = [
        [
            [{'$type': 'Risk', 'val': 0.011}],
            [{'$type': 'Risk', 'val': 0.021}],
            [{'$type': 'Risk', 'val': 0.031}],
        ],
        [
            [{
                '$type': 'RiskVector',
                'asset': [0.011, 0.0151],
                'points': [
                    {'type': 'IR', 'asset': 'USD', 'class_': 'Swap', 'point': '1y'},
                    {'type': 'IR', 'asset': 'USD', 'class_': 'Swap', 'point': '2y'}
                ]
            }],
            [{
                '$type': 'RiskVector',
                'asset': [0.021, 0.0251],
                'points': [
                    {'type': 'IR', 'asset': 'USD', 'class_': 'Swap', 'point': '1y'},
                    {'type': 'IR', 'asset': 'USD', 'class_': 'Swap', 'point': '2y'}
                ]
            }],
            [{
                '$type': 'RiskVector',
                'asset': [0.031, 0.0351],
                'points': [
                    {'type': 'IR', 'asset': 'USD', 'class_': 'Swap', 'point': '1y'},
                    {'type': 'IR', 'asset': 'USD', 'class_': 'Swap', 'point': '2y'}
                ]
            }]
        ]
    ]

    day3 = [
        [
            [{'$type': 'Risk', 'val': 0.012}],
            [{'$type': 'Risk', 'val': 0.022}],
            [{'$type': 'Risk', 'val': 0.032}],
        ],
        [
            [{
                '$type': 'RiskVector',
                'asset': [0.012, 0.0152],
                'points': [
                    {'type': 'IR', 'asset': 'USD', 'class_': 'Swap', 'point': '1y'},
                    {'type': 'IR', 'asset': 'USD', 'class_': 'Swap', 'point': '2y'}
                ]
            }],
            [{
                '$type': 'RiskVector',
                'asset': [0.022, 0.0252],
                'points': [
                    {'type': 'IR', 'asset': 'USD', 'class_': 'Swap', 'point': '1y'},
                    {'type': 'IR', 'asset': 'USD', 'class_': 'Swap', 'point': '2y'}
                ]
            }],
            [{
                '$type': 'RiskVector',
                'asset': [0.032, 0.0352],
                'points': [
                    {'type': 'IR', 'asset': 'USD', 'class_': 'Swap', 'point': '1y'},
                    {'type': 'IR', 'asset': 'USD', 'class_': 'Swap', 'point': '2y'}
                ]
            }]
        ]
    ]

    mocker.return_value = [day1, day2, day3]

    swap1 = IRSwap('Pay', '10y', 'USD', fixed_rate=0.01, name='swap1')
    swap2 = IRSwap('Pay', '10y', 'USD', fixed_rate=0.02, name='swap2')
    swap3 = IRSwap('Pay', '10y', 'USD', fixed_rate=0.03, name='swap3')

    portfolio = Portfolio((swap1, swap2, swap3))
    dates = (dt.date(2019, 10, 7), dt.date(2019, 10, 8), dt.date(2019, 10, 9))

    with HistoricalPricingContext(dates=dates) as hpc:
        risk_key = hpc._PricingContext__risk_key(risk.DollarPrice, swap1.provider)
        results = portfolio.calc((risk.DollarPrice, risk.IRDelta))

    expected = risk.SeriesWithInfo(
        pd.Series(
            data=[0.06, 0.063, 0.066],
            index=[dt.date(2019, 10, 7), dt.date(2019, 10, 8), dt.date(2019, 10, 9)]
        ),
        risk_key=risk_key.ex_date_and_market, )

    assert results.dates == dates
    actual = results[risk.DollarPrice].aggregate()
    assert actual.equals(expected)

    assert (results[dt.date(2019, 10, 9)][risk.DollarPrice]['swap1'] ==
            results[risk.DollarPrice][dt.date(2019, 10, 9)]['swap1'])
    assert (results[dt.date(2019, 10, 9)][risk.DollarPrice]['swap1'] ==
            results[risk.DollarPrice]['swap1'][dt.date(2019, 10, 9)])
    assert (results[dt.date(2019, 10, 9)][risk.DollarPrice]['swap1'] ==
            results['swap1'][risk.DollarPrice][dt.date(2019, 10, 9)])
    assert (results[dt.date(2019, 10, 9)][risk.DollarPrice]['swap1'] ==
            results['swap1'][dt.date(2019, 10, 9)][risk.DollarPrice])
    assert (results[dt.date(2019, 10, 9)][risk.DollarPrice]['swap1'] ==
            results[dt.date(2019, 10, 9)]['swap1'][risk.DollarPrice])


@mock.patch.object(GsRiskApi, '_exec')
def test_backtothefuture_pricing(mocker):
    set_session()

    day1 = [
        [
            [{'$type': 'Risk', 'val': 0.01}],
            [{'$type': 'Risk', 'val': 0.02}],
            [{'$type': 'Risk', 'val': 0.03}],
        ]
    ]

    day2 = [
        [
            [{'$type': 'Risk', 'val': 0.011}],
            [{'$type': 'Risk', 'val': 0.021}],
            [{'$type': 'Risk', 'val': 0.031}],
        ]
    ]

    day3 = [
        [
            [{'$type': 'Risk', 'val': 0.012}],
            [{'$type': 'Risk', 'val': 0.022}],
            [{'$type': 'Risk', 'val': 0.032}],
        ]
    ]

    mocker.return_value = [day1, day2, day3]

    swap1 = IRSwap('Pay', '10y', 'USD', fixed_rate=0.01, name='swap1')
    swap2 = IRSwap('Pay', '10y', 'USD', fixed_rate=0.02, name='swap2')
    swap3 = IRSwap('Pay', '10y', 'USD', fixed_rate=0.03, name='swap3')

    portfolio = Portfolio((swap1, swap2, swap3))

    with BackToTheFuturePricingContext(dates=business_day_offset(dt.datetime.today().date(), [-1, 0, 1],
                                                                 roll='forward')) as hpc:
        risk_key = hpc._PricingContext__risk_key(risk.DollarPrice, swap1.provider)
        results = portfolio.calc(risk.DollarPrice)

    expected = risk.SeriesWithInfo(
        pd.Series(
            data=[0.06, 0.063, 0.066],
            index=business_day_offset(dt.datetime.today().date(), [-1, 0, 1], roll='forward')
        ),
        risk_key=risk_key.ex_date_and_market, )

    actual = results[risk.DollarPrice].aggregate()

    assert actual.equals(expected)


@mock.patch.object(GsRiskApi, '_exec')
def test_duplicate_instrument(mocker):
    set_session()

    dollar_price_values = [
        [
            [
                {'$type': 'Risk', 'val': 0.01}
            ],
            [
                {'$type': 'Risk', 'val': 0.02}
            ],
            [
                {'$type': 'Risk', 'val': 0.03}
            ]
        ]
    ]
    mocker.return_value = [dollar_price_values]

    swap1 = IRSwap('Pay', '10y', 'USD', fixed_rate=0.01, name='swap1')
    swap2 = IRSwap('Pay', '10y', 'USD', fixed_rate=0.02, name='swap2')
    swap3 = IRSwap('Pay', '10y', 'USD', fixed_rate=0.03, name='swap3')

    portfolio = Portfolio((swap1, swap2, swap3, swap1))
    assert portfolio.paths('swap1') == (PortfolioPath(0), PortfolioPath(3))
    assert portfolio.paths('swap2') == (PortfolioPath(1),)

    prices: PortfolioRiskResult = portfolio.dollar_price()
    assert tuple(prices) == (0.01, 0.02, 0.03, 0.01)
    assert round(prices.aggregate(), 2) == 0.07
    assert prices[swap1] == 0.01


@mock.patch.object(GsRiskApi, '_exec')
def test_nested_portfolios(mocker):
    swap1 = IRSwap('Pay', '10y', 'USD', name='USD-swap')
    swap2 = IRSwap('Pay', '10y', 'EUR', name='EUR-swap')
    swap3 = IRSwap('Pay', '10y', 'GBP', name='GBP-swap')

    swap4 = IRSwap('Pay', '10y', 'JPY', name='JPY-swap')
    swap5 = IRSwap('Pay', '10y', 'HUF', name='HUF-swap')
    swap6 = IRSwap('Pay', '10y', 'CHF', name='CHF-swap')

    portfolio2_1 = Portfolio((swap1, swap2, swap3), name='portfolio2_1')
    portfolio2_2 = Portfolio((swap1, swap2, swap3), name='portfolio2_2')
    portfolio1_1 = Portfolio((swap4, portfolio2_1), name='portfolio1_1')
    portfolio1_2 = Portfolio((swap5, portfolio2_2), name='USD-swap')
    portfolio = Portfolio((swap6, portfolio1_1, portfolio1_2), name='portfolio')

    assert portfolio.paths('USD-swap') == (PortfolioPath(2), PortfolioPath((1, 1, 0)), PortfolioPath((2, 1, 0)))


@mock.patch.object(GsRiskApi, '_exec')
def test_single_instrument(mocker):
    set_session()

    mocker.return_value = [[[[{'$type': 'Risk', 'val': 0.01}]]]]

    swap1 = IRSwap('Pay', '10y', 'USD', fixed_rate=0.01, name='swap1')

    portfolio = Portfolio(swap1)
    assert portfolio.paths('swap1') == (PortfolioPath(0),)

    prices: PortfolioRiskResult = portfolio.dollar_price()
    assert tuple(prices) == (0.01,)
    assert round(prices.aggregate(), 2) == 0.01
    assert prices[swap1] == 0.01


def test_results_with_resolution():
    set_session()

    dollar_price_ir_delta_values = [
        [
            [
                {'$type': 'Risk', 'val': 0.01}
            ],
            [
                {'$type': 'Risk', 'val': 0.02}
            ],
            [
                {'$type': 'Risk', 'val': 0.03}
            ]
        ],
        [
            [
                {
                    '$type': 'RiskVector',
                    'asset': [0.01, 0.015],
                    'points': [
                        {'type': 'IR', 'asset': 'USD', 'class_': 'Swap', 'point': '1y'},
                        {'type': 'IR', 'asset': 'USD', 'class_': 'Swap', 'point': '2y'}
                    ]
                }
            ],
            [
                {
                    '$type': 'RiskVector',
                    'asset': [0.02, 0.025],
                    'points': [
                        {'type': 'IR', 'asset': 'USD', 'class_': 'Swap', 'point': '1y'},
                        {'type': 'IR', 'asset': 'USD', 'class_': 'Swap', 'point': '2y'}
                    ]
                }
            ],
            [
                {
                    '$type': 'RiskVector',
                    'asset': [0.03, 0.035],
                    'points': [
                        {'type': 'IR', 'asset': 'USD', 'class_': 'Swap', 'point': '1y'},
                        {'type': 'IR', 'asset': 'USD', 'class_': 'Swap', 'point': '2y'}
                    ]
                }
            ]
        ]
    ]

    swap1 = IRSwap('Pay', '10y', 'USD', name='swap1')
    swap2 = IRSwap('Pay', '10y', 'GBP', name='swap2')
    swap3 = IRSwap('Pay', '10y', 'EUR', name='swap3')

    portfolio = Portfolio((swap1, swap2, swap3))

    with mock.patch('gs_quant.api.gs.risk.GsRiskApi._exec') as mocker:
        mocker.return_value = [dollar_price_ir_delta_values]
        result = portfolio.calc((risk.DollarPrice, risk.IRDelta))

    # Check that we've got results
    assert result[swap1][risk.DollarPrice] is not None

    # Now resolve portfolio and assert that we can still get the result

    resolution_values = [
        [
            [{'$type': 'LegDefinition', 'fixedRate': 0.01, 'terminationDate': '1076-11-14'}],
            [{'$type': 'LegDefinition', 'fixedRate': 0.007, 'terminationDate': '1076-11-14'}],
            [{'$type': 'LegDefinition', 'fixedRate': 0.05, 'terminationDate': '1076-11-14'}]
        ]
    ]

    orig_swap1 = swap1.clone()

    with mock.patch('gs_quant.api.gs.risk.GsRiskApi._exec') as mocker:
        mocker.return_value = [resolution_values]
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
            mocker.return_value = [resolution_values]
            portfolio.resolve()

    assert all(i.termination_date == dt.date(1076, 11, 14) for i in portfolio.instruments)
    assert swap1.fixed_rate == 0.01
    assert swap2.fixed_rate == 0.007
    assert swap3.fixed_rate == 0.05

    # Assert that after resolution under a different context, we cannot retrieve the result

    try:
        _ = result[swap1][risk.DollarPrice]
        assert False
    except KeyError:
        assert True

    # Resolve again and check we get the same values

    with mock.patch('gs_quant.api.gs.risk.GsRiskApi._exec') as mocker:
        with PricingContext(dt.date(1066, 11, 14)):
            # Resolve under a different pricing date
            mocker.return_value = [resolution_values]
            portfolio.resolve()

    assert all(i.termination_date == dt.date(1076, 11, 14) for i in portfolio.instruments)
    assert swap1.fixed_rate == 0.01
    assert swap2.fixed_rate == 0.007
    assert swap3.fixed_rate == 0.05


def test_from_frame():
    swap = IRSwap('Receive', '3m', 'USD', fixed_rate=0, notional_amount=1)
    swaption = IRSwaption(notional_currency='GBP', expiration_date='10y', effective_date='0b')
    portfolio = Portfolio((swap, swaption))
    port_df = portfolio.to_frame()
    new_port_df = Portfolio.from_frame(port_df)

    assert new_port_df[swap] == swap
    assert new_port_df[swaption] == swaption
