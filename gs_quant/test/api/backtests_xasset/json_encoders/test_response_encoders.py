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

import datetime as dt
import json

import pytest

from gs_quant.api.gs.backtests_xasset.json_encoders.response_encoders import (
    decode_basic_bt_transactions,
    encode_response_obj,
)
from gs_quant.api.gs.backtests_xasset.response_datatypes.backtest_datatypes import TransactionDirection
from gs_quant.backtests.backtest_utils import CustomDuration, encode_duration, decode_duration, make_list
from gs_quant.common import Currency
from gs_quant.instrument import EqOption
from gs_quant.json_convertors import encode_callable, decode_callable


def test_decode_basic_bt_transactions():
    server_response_minimum = {
        dt.date(2025, 5, 1).isoformat(): [
            {
                'portfolio': (EqOption(underlier='.SPX', expiration_date='2025-12-19', strike_price=5000).as_dict(),),
            }
        ]
    }
    assert len(decode_basic_bt_transactions(server_response_minimum)) == 1
    assert len(decode_basic_bt_transactions(server_response_minimum, decode_instruments=False)) == 1

    server_response = {
        dt.date(2025, 5, 1).isoformat(): [
            {
                'portfolio': (EqOption(underlier='.SPX', expiration_date='2025-12-19', strike_price=5000).as_dict(),),
                'currency': 'USD',
                'portfolio_price': 100,
                'cost': 0.5,
                'direction': 'Entry',
                'quantity': 25,
            }
        ]
    }

    decoded_response = decode_basic_bt_transactions(server_response)
    transaction = decoded_response[dt.date(2025, 5, 1)][0]
    assert transaction.portfolio_price == 100
    assert transaction.cost == 0.5
    assert transaction.currency == Currency.USD
    assert transaction.direction == TransactionDirection.Entry
    assert transaction.quantity == 25


def test_encode_callable_builtin():
    encoded = encode_callable(min)
    assert encoded == {'module': 'builtins', 'qualname': 'min'}
    decoded = decode_callable(encoded)
    assert decoded is min

    encoded_max = encode_callable(max)
    assert encoded_max == {'module': 'builtins', 'qualname': 'max'}
    assert decode_callable(encoded_max) is max


def test_encode_callable_none():
    assert encode_callable(None) is None
    assert decode_callable(None) is None


def test_decode_callable_passthrough():
    assert decode_callable(min) is min


def test_encode_callable_named_function():
    encoded = encode_callable(make_list)
    assert encoded['module'] == 'gs_quant.backtests.backtest_utils'
    assert encoded['qualname'] == 'make_list'


def test_decode_callable_rejects_non_allowlisted():
    with pytest.raises(ValueError, match='Callable not in allowlist'):
        decode_callable({'module': 'os', 'qualname': 'system'})


def test_custom_duration_round_trip():
    cd = CustomDuration(('3m', 'expiration_date'), min)
    serialized = cd.to_dict()
    assert serialized['function'] == {'module': 'builtins', 'qualname': 'min'}
    assert list(serialized['durations']) == ['3m', 'expiration_date']

    deserialized = CustomDuration.from_dict(serialized)
    assert deserialized.function is min
    assert deserialized.durations == ('3m', 'expiration_date')


def test_custom_duration_json_serializable():
    cd = CustomDuration(('3m', 'expiration_date'), min)
    serialized = cd.to_dict()
    json_str = json.dumps(serialized)
    roundtripped = json.loads(json_str)
    deserialized = CustomDuration.from_dict(roundtripped)
    assert deserialized.function is min
    assert list(deserialized.durations) == ['3m', 'expiration_date']


def test_encode_duration_str():
    assert encode_duration(None) is None
    assert encode_duration('3m') == '3m'
    assert encode_duration('expiration_date') == 'expiration_date'


def test_encode_duration_date():
    d = dt.date(2025, 6, 15)
    assert encode_duration(d) == '2025-06-15'
    assert decode_duration('2025-06-15') == d


def test_encode_duration_timedelta():
    td = dt.timedelta(days=30)
    encoded = encode_duration(td)
    assert encoded == '30d'


def test_encode_duration_custom_duration():
    cd = CustomDuration(('3m', 'expiration_date'), min)
    encoded = encode_duration(cd)
    assert isinstance(encoded, dict)
    assert encoded['function'] == {'module': 'builtins', 'qualname': 'min'}
    decoded = decode_duration(encoded)
    assert isinstance(decoded, CustomDuration)
    assert decoded.function is min


def test_encode_response_obj_callable():
    result = encode_response_obj(min)
    assert result == {'module': 'builtins', 'qualname': 'min'}


def test_encode_response_obj_unhandled_type():
    with pytest.raises(TypeError, match='Type is not JSON serializable: object'):
        encode_response_obj(object())
