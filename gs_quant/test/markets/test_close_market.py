"""
Copyright 2024 Goldman Sachs.
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
import datetime as dt
import json

from freezegun import freeze_time

from gs_quant.common import PricingLocation
from gs_quant.json_encoder import JSONEncoder
from gs_quant.markets import CloseMarket, PricingContext


def test_close_market_dict():
    mkt = CloseMarket(date=dt.date(2024, 4, 11))
    assert json.dumps(mkt.to_dict(), cls=JSONEncoder) == json.dumps(mkt.market.to_dict(), cls=JSONEncoder)
    mkt = CloseMarket(date=dt.date(2024, 4, 11), location='LDN')
    assert json.dumps(mkt.to_dict(), cls=JSONEncoder) == json.dumps(mkt.market.to_dict(), cls=JSONEncoder)


@freeze_time("2025-03-20 16:00:00", tz_offset=4)
def test_close_market_roll():
    # 8PM in LDN, 4PM in NYC
    CloseMarket.roll_hr_and_min = (17, 30)
    test_date = dt.date(2025, 3, 20)
    with PricingContext(test_date, market_data_location="NYC"):
        assert PricingContext.current.market == CloseMarket(test_date - dt.timedelta(days=1), PricingLocation.NYC)
    CloseMarket.roll_hr_and_min = (12, 00)
    with PricingContext(test_date, market_data_location="NYC"):
        assert PricingContext.current.market == CloseMarket(test_date, PricingLocation.NYC)


@freeze_time("2025-03-20 22:00:00", tz_offset=4)
def test_close_market_roll_diff_days():
    # 2AM in LDN, 10PM yesterday in NYC
    CloseMarket.roll_hr_and_min = (23, 30)
    test_date = dt.date(2025, 3, 21)
    with PricingContext(test_date, market_data_location="NYC"):
        # requested a date in the future for NYC - roll back to yesterday and do not apply the roll logic
        assert PricingContext.current.market == CloseMarket(test_date - dt.timedelta(days=1), PricingLocation.NYC)
    test_date = dt.date(2025, 3, 20)
    with PricingContext(test_date, market_data_location="NYC"):
        # requested today NYC, we are not past the roll time so roll back to 2025-03-19
        assert PricingContext.current.market == CloseMarket(test_date - dt.timedelta(days=1), PricingLocation.NYC)
