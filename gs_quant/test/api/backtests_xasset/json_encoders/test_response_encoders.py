"""
Copyright 2019 Goldman Sachs.
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

from gs_quant.api.gs.backtests_xasset.json_encoders.response_encoders import decode_basic_bt_transactions
from gs_quant.api.gs.backtests_xasset.response_datatypes.backtest_datatypes import TransactionDirection
from gs_quant.instrument import EqOption
from gs_quant.target.common import Currency
import datetime as dt


def test_decode_basic_bt_transactions():
    server_response_minimum = {
        dt.date(2025, 5, 1).isoformat(): [{
            'portfolio': (EqOption(underlier='.SPX', expiration_date='2025-12-19', strike_price=5000).as_dict(),),
        }]
    }
    assert len(decode_basic_bt_transactions(server_response_minimum)) == 1
    assert len(decode_basic_bt_transactions(server_response_minimum, decode_instruments=False)) == 1

    server_response = {
        dt.date(2025, 5, 1).isoformat(): [{
            'portfolio': (EqOption(underlier='.SPX', expiration_date='2025-12-19', strike_price=5000).as_dict(),),
            'currency': 'USD',
            'portfolio_price': 100,
            'cost': 0.5,
            'direction': 'Entry',
            'quantity': 25
        }]
    }

    decoded_response = decode_basic_bt_transactions(server_response)
    transaction = decoded_response[dt.date(2025, 5, 1)][0]
    assert transaction.portfolio_price == 100
    assert transaction.cost == 0.5
    assert transaction.currency == Currency.USD
    assert transaction.direction == TransactionDirection.Entry
    assert transaction.quantity == 25
