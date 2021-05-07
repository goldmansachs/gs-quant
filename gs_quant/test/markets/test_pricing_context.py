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

import pytest
from gs_quant import risk
from gs_quant.datetime import business_day_offset
from gs_quant.instrument import IRSwap
from gs_quant.markets import PricingContext, CloseMarket, OverlayMarket
from gs_quant.risk import RollFwd
from gs_quant.test.utils.test_utils import MockCalc


def test_pricing_context(mocker):
    swap1 = IRSwap('Pay', '1y', 'EUR', name='EUR1y')
    future_date = business_day_offset(dt.date.today(), 10, roll='forward')
    with MockCalc(mocker):
        with RollFwd(date='10b', realise_fwd=True):
            market = swap1.market()

    with pytest.raises(ValueError):
        # cannot pass in future date into pricing context, use RollFwd instead
        with PricingContext(pricing_date=future_date):
            _ = swap1.calc(risk.Price)

        # cannot pass in market dated in the future into pricing context, use RollFwd instead
        with PricingContext(market=CloseMarket(date=future_date)):
            _ = swap1.calc(risk.Price)

        with PricingContext(market=OverlayMarket(base_market=CloseMarket(date=future_date, location='NYC'),
                                                 market_data=market.result())):
            _ = swap1.calc(risk.Price)
