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
from gs_quant.datetime import business_day_offset
from gs_quant.instrument import IRSwap, IRSwaption
from gs_quant.markets import HistoricalPricingContext, PricingContext, BackToTheFuturePricingContext
from gs_quant.markets.portfolio import Portfolio
from gs_quant.risk.results import PortfolioPath, PortfolioRiskResult
from gs_quant.session import Environment, GsSession
from gs_quant.test.utils.test_utils import MockCalc


def set_session():
    from gs_quant.session import OAuth2Session
    OAuth2Session.init = mock.MagicMock(return_value=None)
    GsSession.use(Environment.PROD, 'client_id', 'secret')


def test_portfolio(mocker):

    with MockCalc(mocker):
        with PricingContext(pricing_date=dt.date(2020, 10, 15)):
            swap1 = IRSwap('Pay', '10y', 'USD', fixed_rate=0.001, name='swap_10y@10bp')
            swap2 = IRSwap('Pay', '10y', 'USD', fixed_rate=0.002, name='swap_10y@20bp')
            swap3 = IRSwap('Pay', '10y', 'USD', fixed_rate=0.003, name='swap_10y@30bp')

            portfolio = Portfolio((swap1, swap2, swap3))

            prices: PortfolioRiskResult = portfolio.dollar_price()
            result = portfolio.calc((risk.DollarPrice, risk.IRDelta))

        assert tuple(sorted(map(lambda x: round(x, 0), prices))) == (4439478.0, 5423405.0, 6407332.0)
        assert round(prices.aggregate(), 2) == 16270214.48
        assert round(prices[0], 0) == 6407332.0
        assert round(prices[swap2], 0) == 5423405.0
        assert round(prices['swap_10y@30bp'], 0) == 4439478.0

        assert tuple(map(lambda x: round(x, 0), result[risk.DollarPrice])) == (6407332.0, 5423405.0, 4439478.0)
        assert round(result[risk.DollarPrice].aggregate(), 0) == 16270214.0
        assert round(result[risk.DollarPrice]['swap_10y@30bp'], 0) == 4439478.0
        assert round(result[risk.DollarPrice]['swap_10y@30bp'], 0) == round(result['swap_10y@30bp'][risk.DollarPrice],
                                                                            0)

        assert round(result[risk.IRDelta].aggregate().value.sum(), 0) == 278977.0

        prices_only = result[risk.DollarPrice]
        assert tuple(map(lambda x: round(x, 0), prices)) == tuple(map(lambda x: round(x, 0), prices_only))

        swap4 = IRSwap('Pay', '10y', 'USD', fixed_rate=-0.001, name='swap_10y@-10bp')
        portfolio.append(swap4)
        assert len(portfolio.instruments) == 4

        extracted_swap = portfolio.pop('swap_10y@20bp')
        assert extracted_swap == swap2
        assert len(portfolio.instruments) == 3

        swap_dict = {'swap_5': swap1,
                     'swap_6': swap2,
                     'swap_7': swap3}

        portfolio = Portfolio(swap_dict)
        assert len(portfolio) == 3


def test_historical_pricing(mocker):
    with MockCalc(mocker):
        swap1 = IRSwap('Pay', '10y', 'USD', fixed_rate='ATM+1', name='10y@a+1')
        swap2 = IRSwap('Pay', '10y', 'USD', fixed_rate='ATM+2', name='10y@a+2')
        swap3 = IRSwap('Pay', '10y', 'USD', fixed_rate='ATM+3', name='10y@a+3')

        portfolio = Portfolio((swap1, swap2, swap3))
        dates = (dt.date(2019, 10, 7), dt.date(2019, 10, 8), dt.date(2019, 10, 9))

        with HistoricalPricingContext(dates=dates) as hpc:
            risk_key = hpc._PricingContext__risk_key(risk.DollarPrice, swap1.provider)
            results = portfolio.calc((risk.DollarPrice, risk.IRDelta))

        expected = risk.SeriesWithInfo(
            pd.Series(
                data=[-564854.3640043922, -565604.2636791412, -564751.5121349357],
                index=[dt.date(2019, 10, 7), dt.date(2019, 10, 8), dt.date(2019, 10, 9)]
            ),
            risk_key=risk_key.ex_date_and_market, )

        assert results.dates == dates
        actual = results[risk.DollarPrice].aggregate()
        assert actual.equals(expected)

        assert (results[dt.date(2019, 10, 9)][risk.DollarPrice]['10y@a+1'] ==
                results[risk.DollarPrice][dt.date(2019, 10, 9)]['10y@a+1'])
        assert (results[dt.date(2019, 10, 9)][risk.DollarPrice]['10y@a+1'] ==
                results[risk.DollarPrice]['10y@a+1'][dt.date(2019, 10, 9)])
        assert (results[dt.date(2019, 10, 9)][risk.DollarPrice]['10y@a+1'] ==
                results['10y@a+1'][risk.DollarPrice][dt.date(2019, 10, 9)])
        assert (results[dt.date(2019, 10, 9)][risk.DollarPrice]['10y@a+1'] ==
                results['10y@a+1'][dt.date(2019, 10, 9)][risk.DollarPrice])
        assert (results[dt.date(2019, 10, 9)][risk.DollarPrice]['10y@a+1'] ==
                results[dt.date(2019, 10, 9)]['10y@a+1'][risk.DollarPrice])


def test_backtothefuture_pricing(mocker):
    with MockCalc(mocker):
        swap1 = IRSwap('Pay', '10y', 'USD', fixed_rate=0.01, name='swap1')
        swap2 = IRSwap('Pay', '10y', 'USD', fixed_rate=0.02, name='swap2')
        swap3 = IRSwap('Pay', '10y', 'USD', fixed_rate=0.03, name='swap3')

        portfolio = Portfolio((swap1, swap2, swap3))
        pricing_date = dt.date(2020, 10, 7)
        with PricingContext(pricing_date=pricing_date):
            with BackToTheFuturePricingContext(dates=business_day_offset(pricing_date, [-1, 0, 1],
                                                                         roll='forward')) as hpc:
                risk_key = hpc._PricingContext__risk_key(risk.DollarPrice, swap1.provider)
                results = portfolio.calc(risk.DollarPrice)

    expected = risk.SeriesWithInfo(
        pd.Series(
            data=[-35301348.93982054, -35366234.71769963, -35281392.58523489],
            index=business_day_offset(pricing_date, [-1, 0, 1], roll='forward')
        ),
        risk_key=risk_key.ex_date_and_market, )

    actual = results[risk.DollarPrice].aggregate()

    assert actual.equals(expected)


def test_duplicate_instrument(mocker):
    with MockCalc(mocker):

        swap1 = IRSwap('Pay', '1y', 'EUR', name='EUR1y')
        swap2 = IRSwap('Pay', '2y', 'EUR', name='EUR2y')
        swap3 = IRSwap('Pay', '3y', 'EUR', name='EUR3y')

        portfolio = Portfolio((swap1, swap2, swap3, swap1))
        assert portfolio.paths('EUR1y') == (PortfolioPath(0), PortfolioPath(3))
        assert portfolio.paths('EUR2y') == (PortfolioPath(1),)
        with PricingContext(pricing_date=dt.date(2020, 10, 15)):
            fwds: PortfolioRiskResult = portfolio.calc(risk.IRFwdRate)

        assert tuple(map(lambda x: round(x, 6), fwds)) == (-0.005378, -0.005224, -0.00519, -0.005378)
        assert round(fwds.aggregate(), 6) == -0.02117
        assert round(fwds[swap1], 6) == -0.005378


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


def test_single_instrument(mocker):
    with MockCalc(mocker):

        swap1 = IRSwap('Pay', '10y', 'USD', fixed_rate=0.0, name='10y@0')

        portfolio = Portfolio(swap1)
        assert portfolio.paths('10y@0') == (PortfolioPath(0),)

        with PricingContext(pricing_date=dt.date(2020, 10, 15)):
            prices: PortfolioRiskResult = portfolio.dollar_price()
        assert tuple(map(lambda x: round(x, 0), prices)) == (7391258.0,)
        assert round(prices.aggregate(), 0) == 7391258.0
        assert round(prices[swap1], 0) == 7391258.0


def test_results_with_resolution(mocker):
    with MockCalc(mocker):

        swap1 = IRSwap('Pay', '10y', 'USD', name='swap1')
        swap2 = IRSwap('Pay', '10y', 'GBP', name='swap2')
        swap3 = IRSwap('Pay', '10y', 'EUR', name='swap3')

        portfolio = Portfolio((swap1, swap2, swap3))

        with PricingContext(pricing_date=dt.date(2020, 10, 15)):
            result = portfolio.calc((risk.DollarPrice, risk.IRDelta))

        # Check that we've got results
        assert result[swap1][risk.DollarPrice] is not None

        # Now resolve portfolio and assert that we can still get the result

        orig_swap1 = swap1.clone()

        with PricingContext(pricing_date=dt.date(2020, 10, 15)):
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

        with PricingContext(dt.date(2020, 10, 14)):
            # Resolve under a different pricing date
            portfolio.resolve()

        assert portfolio.instruments[0].termination_date == dt.date(2030, 10, 16)
        assert portfolio.instruments[1].termination_date == dt.date(2030, 10, 14)
        assert round(swap1.fixed_rate, 4) == 0.0075
        assert round(swap2.fixed_rate, 4) == 0.004
        assert round(swap3.fixed_rate, 4) == -0.0027

        # Assert that after resolution under a different context, we cannot retrieve the result

        try:
            _ = result[swap1][risk.DollarPrice]
            assert False
        except KeyError:
            assert True

        # Resolve again and check we get the same values

        with PricingContext(dt.date(2020, 10, 14)):
            # Resolve under a different pricing date
            portfolio.resolve()

        assert portfolio.instruments[0].termination_date == dt.date(2030, 10, 16)
        assert portfolio.instruments[1].termination_date == dt.date(2030, 10, 14)
        assert round(swap1.fixed_rate, 4) == 0.0075
        assert round(swap2.fixed_rate, 4) == 0.004
        assert round(swap3.fixed_rate, 4) == -0.0027


def test_from_frame():
    swap = IRSwap('Receive', '3m', 'USD', fixed_rate=0, notional_amount=1)
    swaption = IRSwaption(notional_currency='GBP', expiration_date='10y', effective_date='0b')
    portfolio = Portfolio((swap, swaption))
    port_df = portfolio.to_frame()
    new_port_df = Portfolio.from_frame(port_df)

    assert new_port_df[swap] == swap
    assert new_port_df[swaption] == swaption


def test_single_instrument_new_mock(mocker):

    with MockCalc(mocker):
        with PricingContext(pricing_date=dt.date(2020, 10, 15)):
            swap1 = IRSwap('Pay', '10y', 'USD', name='swap1')

            portfolio = Portfolio(swap1)
            fwd: PortfolioRiskResult = portfolio.calc(risk.IRFwdRate)

        assert portfolio.paths('swap1') == (PortfolioPath(0),)
        assert tuple(map(lambda x: round(x, 6), fwd)) == (0.007512,)
        assert round(fwd.aggregate(), 2) == 0.01
        assert round(fwd[swap1], 6) == 0.007512
