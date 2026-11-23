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

import dataclasses
import json
from typing import Optional

import pytest
from dataclasses_json import dataclass_json

from gs_quant.base import Base
from gs_quant.common import Currency, PayReceive
from gs_quant.instrument import Instrument, IRSwap
from gs_quant.test import dataclass_test_utils as utils
from gs_quant.workflow import CustomDeltaHedge, DeltaHedge, HedgeModel, HedgeTypes, WorkflowEntitlements


@dataclass_json
@dataclasses.dataclass
class _ConsumerResponse:
    entitlements: Optional[WorkflowEntitlements] = None
    leg: Optional[IRSwap] = None
    legs: Optional[dict[str, Instrument]] = None


def test_dataclasses_replace_and_fields():
    swap = utils.irswap()
    replaced = dataclasses.replace(swap, fixed_rate=0.02)
    assert (type(replaced), replaced.fixed_rate, replaced.name) == (IRSwap, 0.02, 'swap')
    names = [f.name for f in dataclasses.fields(swap)]
    assert names[:3] == ['pay_or_receive', 'termination_date', 'notional_currency']
    assert set(IRSwap.__dataclass_fields__) == set(names) | {'quantity_'}


def test_orjson_dumps_instrument():
    orjson = pytest.importorskip('orjson')
    swap = utils.irswap()
    native = json.loads(orjson.dumps(swap))
    assert native['pay_or_receive'] == 'Pay'
    assert native['effective_date'] == '2021-03-04'
    assert native['fixed_rate'] == 0.01
    assert 'principal_exchange' in native and native['principal_exchange'] is None
    assert json.loads(orjson.dumps(swap.to_dict(encode_json=True))) == swap.to_dict(encode_json=True)


def test_stdlib_dataclass_subclass_of_base():
    @dataclasses.dataclass(unsafe_hash=True)
    class CacheKey(Base):
        ccy: str = None
        tenor: Optional[str] = None

    key = CacheKey('USD', '1y')
    assert (key.ccy, key.tenor) == ('USD', '1y')
    assert hash(key) == hash(CacheKey('USD', '1y'))
    assert [f.name for f in dataclasses.fields(key)] == ['ccy', 'tenor']
    assert key.as_dict() == {'ccy': 'USD', 'tenor': '1y'}
    key.tenor = 2
    assert key.tenor == '2'


def test_dataclass_json_subclass_of_base():
    @dataclass_json
    @dataclasses.dataclass
    class State(Base):
        ccy: str = None
        notional: Optional[float] = None

    assert State('USD', 1e6).to_dict() == {'ccy': 'USD', 'notional': 1e6}
    assert State.from_dict({'ccy': 'EUR'}) == State('EUR')


def test_consumer_dataclass_json_class_nesting_gs_quant_types():
    decoded = _ConsumerResponse.from_dict(
        {
            'entitlements': {'version': 1, 'readers': [{'type': 'user', 'value': 'abc'}]},
            'leg': {
                'payOrReceive': 'Pay',
                'terminationDate': '10y',
                'fixedRate': 0.01,
                'assetClass': 'Rates',
                'type': 'Swap',
            },
            'legs': {'a': {'payOrReceive': 'Rec', 'terminationDate': '5y', 'assetClass': 'Rates', 'type': 'Swap'}},
        }
    )
    assert decoded.entitlements.readers[0].type_ == 'user'
    assert type(decoded.leg) is IRSwap
    assert (decoded.leg.pay_or_receive, decoded.leg.fixed_rate) == (PayReceive.Pay, 0.01)
    assert type(decoded.legs['a']) is IRSwap
    assert decoded.legs['a'].pay_or_receive is PayReceive.Receive

    swap = utils.irswap()
    response = _ConsumerResponse(WorkflowEntitlements(version=1), swap, {'a': swap})
    encoded = response.to_dict()
    assert encoded['entitlements'] == {'version': 1}
    assert encoded['leg'] == swap.to_dict()
    assert encoded['legs'] == {'a': swap.to_dict()}
    assert encoded['leg']['notionalCurrency'] is Currency.USD
    unnamed = swap.clone(name=None)
    expected = _ConsumerResponse(WorkflowEntitlements(version=1), unnamed, {'a': unnamed})
    assert _ConsumerResponse.from_json(response.to_json()) == expected


def test_consumer_decoder_keyed_by_static_type_defaults():
    by_type = {
        next(f.default for f in dataclasses.fields(cls) if f.name in ('type', 'type_')): cls
        for cls in HedgeTypes.__subclasses__()
    }

    def decode(value: dict) -> HedgeTypes:
        return by_type[value['type']].from_dict(value)

    assert by_type == {'CustomDeltaHedge': CustomDeltaHedge, 'DeltaHedge': DeltaHedge}
    assert decode({'type': 'CustomDeltaHedge', 'amount': 1.5}) == CustomDeltaHedge(amount=1.5)
    assert decode({'type': 'DeltaHedge', 'model': 'Smile'}) == DeltaHedge(model=HedgeModel.Smile)
