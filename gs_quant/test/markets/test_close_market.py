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

from gs_quant.json_encoder import JSONEncoder
from gs_quant.markets import CloseMarket


def test_close_market_dict():
    mkt = CloseMarket(date=dt.date(2024, 4, 11))
    assert json.dumps(mkt.to_dict(), cls=JSONEncoder) == json.dumps(mkt.market.to_dict(), cls=JSONEncoder)
    mkt = CloseMarket(date=dt.date(2024, 4, 11), location='LDN')
    assert json.dumps(mkt.to_dict(), cls=JSONEncoder) == json.dumps(mkt.market.to_dict(), cls=JSONEncoder)
