"""
Copyright 2018 Goldman Sachs.
Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""

from gs_quant import risk
from gs_quant.instrument import IRSwap
from gs_quant.risk import FloatWithInfo, DataFrameWithInfo, AggregationLevel
from gs_quant.test.utils.mock_calc import MockCalc

swap_1 = IRSwap("Pay", "5y", "EUR", fixed_rate=-0.005, name="5y")


def test_currency_params(mocker):
    price = risk.Price
    myr_price = risk.Price(currency="MYR")

    with MockCalc(mocker):
        res1 = swap_1.calc(myr_price)
        res2 = swap_1.calc(price)
        res3 = swap_1.calc((price, myr_price))

    assert res1 != res2
    assert res3[price] == res2
    assert res3[myr_price] == res1


def test_finite_difference_params(mocker):
    nok_delta = risk.IRDelta(currency="NOK")
    local_ccy_delta = risk.IRDelta(currency="local")
    local_aggregated_delta = risk.IRDelta(
        currency="local", aggregation_level=AggregationLevel.Type
    )

    with MockCalc(mocker):
        res3 = swap_1.calc(risk.IRDelta)
        res5 = swap_1.calc((risk.Price, nok_delta))
        res6 = swap_1.calc((local_ccy_delta, nok_delta))
        res7 = swap_1.calc(risk.IRDelta(aggregation_level=AggregationLevel.Asset))
        res8 = swap_1.calc((local_ccy_delta, local_aggregated_delta))

    assert isinstance(res5[risk.Price], FloatWithInfo)
    assert isinstance(res5[nok_delta], DataFrameWithInfo)
    assert res6[local_ccy_delta]["value"].size != res6[nok_delta]["value"].size
    assert res6[local_ccy_delta]["value"].size != res3["value"].size
    assert res6[nok_delta]["value"].size != res3["value"].size
    assert res7["mkt_asset"].size == 2
    assert not isinstance(res8[local_ccy_delta], type(res8[local_aggregated_delta]))


def test_risk_measure_setters():
    base_delta = risk.IRDelta

    usd_delta = risk.IRDelta(currency="USD")

    assert usd_delta.parameters is not None
    assert usd_delta.parameters.currency == "USD"

    local_usd_delta = usd_delta(local_curve=True)

    assert local_usd_delta.parameters.local_curve
    assert usd_delta != local_usd_delta

    assert risk.IRDelta.parameters is None
    assert base_delta.parameters is None
