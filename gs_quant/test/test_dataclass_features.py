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

import copy
import dataclasses
import datetime as dt
import inspect
import json
import pickle

import numpy as np
import pytest
from dateutil.tz import tzutc

from gs_quant.api.gs.backtests_xasset.response_datatypes.backtest_datatypes import AdditionalResults
from gs_quant.backtests.actions import AddScaledTradeAction, AddTradeAction, ExitTradeAction
from gs_quant.backtests.backtest_objects import (
    AggregateTransactionModel,
    BackTest,
    ConstantCashAccrualModel,
    OisFixingCashAccrualModel,
    ScaledTransactionModel,
)
from gs_quant.backtests.data_sources import GsDataSource
from gs_quant.backtests.generic_engine_action_impls import ExitTradeActionImpl
from gs_quant.backtests.strategy import Strategy
from gs_quant.backtests.triggers import IntradayTriggerRequirements, PeriodicTrigger, PeriodicTriggerRequirements
from gs_quant.base import Scenario
from gs_quant.common import (
    AssetClass,
    AssetType,
    Currency,
    CurveScenario,
    Identifier,
    MarketDataPattern,
    MarketDataScenario,
    MultiScenario,
    Op,
    PayReceive,
    PricingDateAndMarketDataAsOf,
    PricingLocation,
    RiskPosition,
    RiskRequestParameters,
)
from gs_quant.instrument import Forward, Instrument, IRSwap, Security
from gs_quant.markets import CloseMarket
from gs_quant.markets.portfolio import Portfolio
from gs_quant.risk import MarketDataShockBasedScenario, RollFwd
from gs_quant.target.assets import CommodityPowerNode, HedgeFundParameters
from gs_quant.target.backtests import BacktestStrategyTransactionCost, BacktestStrategyTransactionCostModelScaled
from gs_quant.target.data import DataQuery, DBConfig
from gs_quant.target.indices import IndicesEditInputs
from gs_quant.test import dataclass_test_utils as utils
from gs_quant.workflow import (
    BinaryImageComments,
    CustomDeltaHedge,
    DeltaHedge,
    HyperLinkImageComments,
    SaveQuoteRequest,
    VisualStructuringReport,
)

utils.fill_field_caches_subclasses_first(utils.generated_classes(utils.generated_modules()))

SWAP_DICT = {
    'payOrReceive': PayReceive.Pay,
    'terminationDate': '10y',
    'notionalCurrency': Currency.USD,
    'notionalAmount': 1e6,
    'effectiveDate': '2021-03-04',
    'fixedRate': 0.01,
    'fee': 0.0,
    'assetClass': AssetClass.Rates,
    'type': AssetType.Swap,
}


def _init_names(cls) -> list:
    return [f.name for f in dataclasses.fields(cls) if f.init]


def _round_trip(strategy: Strategy) -> Strategy:
    return Strategy.from_dict(strategy.to_dict())


def _one_action_strategy(action) -> Strategy:
    requirements = PeriodicTriggerRequirements(dt.date(2021, 3, 4), dt.date(2021, 6, 4), '1m')
    return Strategy(None, PeriodicTrigger(requirements, action))


def test_positional_construction():
    names = _init_names(IRSwap)
    assert names[:3] == ['pay_or_receive', 'termination_date', 'notional_currency']
    assert names[-1] == 'name'
    swap = IRSwap('Pay', '10y', 'USD')
    assert (swap.pay_or_receive, swap.termination_date, swap.notional_currency) == (
        PayReceive.Pay,
        '10y',
        Currency.USD,
    )
    values = [None] * len(names)
    values[-1] = 'myname'
    assert IRSwap(*values).name == 'myname'
    with pytest.raises(TypeError):
        IRSwap(*values, None)
    with pytest.raises(TypeError):
        IRSwap('Pay', pay_or_receive='Rec')


def test_signatures():
    for _ in range(2):
        assert list(inspect.signature(IRSwap).parameters) == _init_names(IRSwap)
        assert list(inspect.signature(Security).parameters) == [
            'ticker',
            'bbid',
            'ric',
            'isin',
            'cusip',
            'prime_id',
            'quantity',
        ]
        IRSwap('Pay', '10y', 'USD')
        Security(ticker='GS UN')


def test_camel_case_kwargs():
    assert IRSwap(notionalAmount=1e6, fixedRate=0.01) == IRSwap(notional_amount=1e6, fixed_rate=0.01)
    assert HedgeFundParameters(openToSMA=True).open_to_sma is True
    with pytest.raises(ValueError, match='notionalAmount and notional_amount both specified'):
        IRSwap(notionalAmount=1e6, notional_amount=2e6)
    with pytest.raises(TypeError):
        IRSwap(notAField=1)


def test_camel_case_attributes():
    swap = IRSwap('Pay', '10y', 'USD')
    assert swap.notionalCurrency is Currency.USD
    swap.fixedRate = 0.02
    assert swap.fixed_rate == 0.02
    assert swap.fixedRate == 0.02
    assert 'fixedRate' not in vars(swap)
    swap.notionalCurrency = 'EUR'
    assert swap.notional_currency is Currency.EUR


def test_renamed_fields():
    swap = utils.irswap()
    assert swap.type is swap.type_ is AssetType.Swap
    assert swap.to_dict()['type'] is AssetType.Swap
    assert swap.as_dict()['type'] is AssetType.Swap
    assert swap.as_dict(as_camel_case=True)['type'] is AssetType.Swap
    params = HedgeFundParameters(open_to_sma=True)
    assert params.openToSMA is True
    assert params.to_dict() == {'openToSMA': True}
    assert params.as_dict() == {'openToSMA': True}
    assert HedgeFundParameters.from_dict({'openToSMA': False}).open_to_sma is False


@pytest.mark.xfail(
    strict=True, reason='D-29: given both a renamed field name and its wire name (type_ and type), the last one wins'
)
@pytest.mark.parametrize(
    'kwargs', ({'type_': 'a', 'type': 'b'}, {'type': 'a', 'type_': 'b'}), ids=('name_first', 'wire_name_first')
)
def test_renamed_field_given_both_names(kwargs):
    with pytest.raises(ValueError):
        Identifier(**kwargs)


def test_assignment_coercion():
    swap = IRSwap()
    swap.notional_currency = 'gbp'
    assert swap.notional_currency is Currency.GBP
    swap.pay_or_receive = 'Receive'
    assert swap.pay_or_receive is PayReceive.Receive
    pattern = MarketDataPattern(mkt_point=['a', 'b'])
    assert pattern.mkt_point == ('a', 'b')
    scenario = CurveScenario(market_data_pattern={'mktType': 'IR', 'mktAsset': 'USD'})
    assert scenario.market_data_pattern == MarketDataPattern('IR', 'USD')


def test_numeric_assignment():
    swap = IRSwap()
    swap.fixed_rate = 1
    assert type(swap.fixed_rate) is int
    swap.fixed_rate = np.float64(0.5)
    assert type(swap.fixed_rate) is np.float64
    swap.notional_amount = np.int64(5)
    assert swap.notional_amount == 5
    assert type(swap.notional_amount) is int


def test_construction_parsing():
    swap = IRSwap(termination_date='2030-01-02', notional_amount='1e6')
    assert swap.termination_date == '2030-01-02'
    assert swap.notional_amount == '1e6'
    request = SaveQuoteRequest(pricing_and_market_data_as_of=[{'pricingDate': '2021-03-04'}])
    assert request.pricing_and_market_data_as_of[0].pricing_date == dt.date(2021, 3, 4)


def test_static_fields():
    swap = IRSwap('Pay', '10y', 'USD')
    assert 'asset_class' not in _init_names(IRSwap)
    with pytest.raises(TypeError):
        IRSwap(asset_class='FX')
    for name in ('asset_class', 'assetClass', 'type', 'type_'):
        with pytest.raises(ValueError, match='cannot be set'):
            setattr(swap, name, 'FX')
    assert swap.to_dict()['assetClass'] is AssetClass.Rates
    assert swap.to_dict()['type'] is AssetType.Swap
    assert IRSwap.from_dict({'assetClass': 'FX', 'type': 'Option'}).asset_class is AssetClass.Rates


def test_to_dict_shape():
    assert utils.irswap().to_dict() == SWAP_DICT
    assert MarketDataPattern(mkt_point=('a', 'b')).to_dict() == {'mktPoint': ['a', 'b']}


def test_to_dict_encode_json():
    expected = {k: v.value if hasattr(v, 'value') else v for k, v in SWAP_DICT.items()}
    assert utils.irswap().to_dict(encode_json=True) == expected


def test_json_round_trip():
    swap = utils.irswap()
    assert json.loads(swap.to_json()) == swap.to_dict(encode_json=True)
    assert IRSwap.from_json(swap.to_json()) == swap.clone(name=None)


def test_from_dict_leniency():
    expected = IRSwap('Pay', '10y', 'EUR', fixed_rate=0.01)
    assert (
        IRSwap.from_dict(
            {'pay_or_receive': 'Pay', 'termination_date': '10y', 'notional_currency': 'EUR', 'fixed_rate': 0.01}
        )
        == expected
    )
    assert (
        IRSwap.from_dict(
            {'payOrReceive': 'Pay', 'terminationDate': '10y', 'notionalCurrency': 'EUR', 'fixedRate': 0.01}
        )
        == expected
    )
    assert (
        IRSwap.from_dict(
            {
                'pay_or_receive': 'Pay',
                'terminationDate': '10y',
                'notionalCurrency': 'EUR',
                'fixed_rate': 0.01,
                'notAField': 1,
            }
        )
        == expected
    )
    typed = IRSwap.from_dict(
        {'payOrReceive': PayReceive.Pay, 'effectiveDate': dt.date(2021, 3, 4), 'notionalCurrency': Currency.EUR}
    )
    assert (typed.pay_or_receive, typed.effective_date, typed.notional_currency) == (
        PayReceive.Pay,
        dt.date(2021, 3, 4),
        Currency.EUR,
    )
    assert RiskRequestParameters.from_dict({'rawResults': 'false'}).raw_results is True


def test_schema():
    schema = IRSwap.schema()
    dumped = schema.dump(utils.irswap())
    assert dumped['payOrReceive'] == 'Pay'
    assert dumped['fixedRate'] == 0.01
    loaded = schema.load({'payOrReceive': 'Pay', 'fixedRate': 0.01})
    assert loaded == IRSwap('Pay', fixed_rate=0.01)


def test_helpers():
    swap = utils.irswap()
    as_dict = swap.as_dict()
    assert as_dict['effective_date'] == dt.date(2021, 3, 4)
    assert as_dict['name'] == 'swap'
    assert 'notional_amount' in as_dict and 'principal_exchange' not in as_dict
    assert swap.as_dict(as_camel_case=True)['fixedRate'] == 0.01
    clone = swap.clone(fixed_rate=0.02)
    assert (clone.fixed_rate, clone.name, swap.fixed_rate) == (0.02, 'swap', 0.01)
    assert {'pay_or_receive', 'asset_class', 'type', 'name'} <= IRSwap.properties()
    assert 'asset_class' not in IRSwap.properties_init()
    assert IRSwap.properties() - IRSwap.properties_init() == {'asset_class', 'type'}
    assert IRSwap.default_instance() == IRSwap()
    target = MarketDataPattern()
    target.from_instance(MarketDataPattern('IR', 'USD', name='usd'))
    assert target == MarketDataPattern('IR', 'USD', name='usd')
    with pytest.raises(ValueError):
        target.from_instance(CurveScenario())


@pytest.mark.xfail(strict=True, reason='D-29: clone() rejects camelCase names as "both specified"')
def test_clone_camel_case():
    assert utils.irswap().clone(fixedRate=0.02).fixed_rate == 0.02


def test_name_semantics():
    swap = utils.irswap()
    assert 'name' not in swap.to_dict()
    assert swap != swap.clone(name='other')
    assert hash(swap) != hash(swap.clone(name='other'))
    assert IRSwap.from_dict(swap.to_dict()).name is None


def test_hash_repr():
    swap = utils.irswap()
    assert {swap: 1}[utils.irswap()] == 1
    before = hash(swap)
    swap.fixed_rate = 0.03
    assert hash(swap) != before
    assert hash(swap) == hash(utils.irswap().clone(fixed_rate=0.03))
    assert repr(swap) == 'IRSwap(swap)'
    assert repr(IRSwap()) == 'IRSwap'
    assert repr(MarketDataPattern('IR', name='usd')) == 'usd (MarketDataPattern)'
    assert repr(MarketDataPattern('IR')).startswith('<gs_quant.target.common.MarketDataPattern object at ')
    assert repr(RollFwd(date='1m', realise_fwd=True)) == 'RollFwd(date:1m, realise_fwd:True, scenario_type:RollFwd)'
    assert repr(RollFwd(date='1m', name='fwd')) == 'fwd'
    assert repr(utils.parameterised_risk_measure()) == 'IRDelta(aggregation_level:Type, currency:local)'


@pytest.mark.xfail(strict=True, reason='D-29: repr() raises for a generated class without a name field')
@pytest.mark.parametrize('cls', (DBConfig, IndicesEditInputs))
def test_repr_without_name_field(cls):
    assert repr(cls()).startswith(f'<{cls.__module__}.{cls.__name__} object at ')


@pytest.mark.parametrize(
    'value',
    (utils.irswap(), utils.eq_option(), utils.market_data_shock_scenario(), utils.eleven_trigger_strategy()),
    ids=lambda v: type(v).__name__,
)
def test_pickle_and_copy(value):
    for copied in (pickle.loads(pickle.dumps(value)), copy.copy(value), copy.deepcopy(value)):
        assert copied == value
        assert type(copied) is type(value)
        assert getattr(copied, 'name', None) == getattr(value, 'name', None)


def test_dataclass_protocol():
    swap = utils.irswap()
    assert dataclasses.is_dataclass(IRSwap) and dataclasses.is_dataclass(swap)
    assert [f.name for f in dataclasses.fields(swap)][:3] == ['pay_or_receive', 'termination_date', 'notional_currency']
    replaced = dataclasses.replace(swap, fixed_rate=0.02)
    assert type(replaced) is IRSwap
    assert (replaced.fixed_rate, replaced.name) == (0.02, 'swap')
    assert dataclasses.asdict(swap)['notional_currency'] is Currency.USD


def test_float_or_str_codec():
    assert IRSwap.from_dict({'notionalAmount': '5'}).notional_amount == 5.0
    assert type(IRSwap.from_dict({'notionalAmount': 5}).notional_amount) is float
    assert IRSwap.from_dict({'fixedRate': 'ATMF'}).fixed_rate == 'ATMF'
    assert IRSwap(notional_amount='ATMF').to_dict()['notionalAmount'] == 'ATMF'


@pytest.mark.parametrize(
    'value, expected',
    (
        ('2020-07-28', dt.date(2020, 7, 28)),
        ('28Jul20', dt.date(2020, 7, 28)),
        ('28Jul2020', dt.date(2020, 7, 28)),
        ('28-Jul-20', dt.date(2020, 7, 28)),
        ('28/07/2020', dt.date(2020, 7, 28)),
        (44040.0, dt.date(2020, 7, 28)),
        (59.0, dt.date(1900, 2, 28)),
        (61.0, dt.date(1900, 3, 1)),
        ('10y', '10y'),
    ),
)
def test_date_or_tenor_codec(value, expected):
    swap = IRSwap.from_dict({'terminationDate': value})
    assert swap.termination_date == expected
    assert swap.to_dict()['terminationDate'] == (expected.isoformat() if isinstance(expected, dt.date) else expected)


def test_date_codec():
    assert DataQuery.from_dict({'startDate': '28/07/2020'}).start_date == dt.date(2020, 7, 28)
    assert DataQuery(start_date=dt.date(2020, 7, 28)).to_dict()['startDate'] == '2020-07-28'
    with pytest.raises(ValueError):
        DataQuery.from_dict({'startDate': '10y'})


def test_datetime_codec():
    assert DataQuery.from_dict({'startTime': 1614834367123}).start_time == dt.datetime.fromtimestamp(1614834367.123)
    parsed = DataQuery.from_dict({'startTime': '2021-03-04T05:06:07.123456789Z'}).start_time
    assert parsed == dt.datetime(2021, 3, 4, 5, 6, 7, 123456, tzinfo=tzutc())
    naive = DataQuery(start_time=dt.datetime(2021, 3, 4, 5, 6, 7, 123456))
    assert naive.to_dict()['startTime'] == '2021-03-04T05:06:07.123Z'
    aware = DataQuery(start_time=dt.datetime(2021, 3, 4, 5, 6, 7, tzinfo=dt.timezone.utc))
    assert aware.to_dict()['startTime'] == '2021-03-04T05:06:07.000+00:00'


def test_time_codec():
    requirements = IntradayTriggerRequirements(dt.time(9, 17, 34), dt.time(10, 7, 57), 5.0)
    encoded = requirements.to_dict()
    assert (encoded['start_time'], encoded['end_time']) == ('09:17:34', '10:07:57')
    assert IntradayTriggerRequirements.from_dict(encoded).start_time == dt.time(9, 17, 34)


def _priced_with_market() -> PricingDateAndMarketDataAsOf:
    return PricingDateAndMarketDataAsOf(
        pricing_date=dt.date(2021, 3, 4), market=CloseMarket(dt.date(2021, 3, 3), PricingLocation.NYC, check=False)
    )


def test_market_field():
    assert _priced_with_market().to_dict() == {
        'pricingDate': '2021-03-04',
        'market': {'date': dt.date(2021, 3, 3), 'location': PricingLocation.NYC, 'marketType': 'CloseMarket'},
    }


@pytest.mark.xfail(strict=True, reason='D-29: to_json() raises for a Market field holding a CloseMarket')
def test_market_field_to_json():
    assert json.loads(_priced_with_market().to_json()) == {
        'pricingDate': '2021-03-04',
        'market': {'date': '2021-03-03', 'location': 'NYC', 'marketType': 'CloseMarket'},
    }


def test_instrument_dispatch():
    assert type(Instrument.from_dict({'assetClass': 'rates', 'type': 'swap', 'payOrReceive': 'Pay'})) is IRSwap
    assert type(Instrument.from_dict({'asset_class': 'Rates', 'type': 'Swap'})) is IRSwap
    for tag in (None, '', 'Security'):
        security = Instrument.from_dict({'assetClass': tag, 'type': tag, 'ticker': 'GS UN'})
        assert type(security) is Security
        assert security.ticker == 'GS UN'
    assert type(Instrument.from_dict({'assetClass': 'Cash', 'type': 'Currency'})) is Forward
    assert type(IRSwap.from_dict({'assetClass': 'FX', 'type': 'Option'})) is IRSwap
    assert Instrument.from_dict({}) is None
    with pytest.raises(ValueError, match='unable to build instrument'):
        Instrument.from_dict({'assetClass': 'Rates', 'type': 'NotAType'})
    with pytest.raises(ValueError, match='assetClass/asset_class not specified'):
        Instrument.from_dict({'type': 'Swap'})
    with pytest.raises(ValueError, match='type not specified'):
        Instrument.from_dict({'assetClass': 'Rates'})


@pytest.mark.xfail(strict=True, reason='D-29: Instrument.from_dict pops assetClass and type from its input')
def test_instrument_dispatch_keeps_input():
    values = {'assetClass': 'Rates', 'type': 'Swap', 'payOrReceive': 'Pay'}
    Instrument.from_dict(values)
    assert values == {'assetClass': 'Rates', 'type': 'Swap', 'payOrReceive': 'Pay'}


def test_report_comment_hedge_dispatch():
    request = SaveQuoteRequest.from_dict(
        {'reports': [{'reportType': 'VisualStructuringReport', 'positionSetId': 'ps1'}, {'reportType': 'Unknown'}]}
    )
    assert type(request.reports[0]) is VisualStructuringReport
    assert request.reports[0].position_set_id == 'ps1'
    assert request.reports[1] is None
    report = VisualStructuringReport.from_dict(
        {
            'comments': [
                {'commentType': 'binaryImageComments', 'data': 'abc'},
                {'commentType': 'hyperLinkImageComments'},
            ],
            'hedgeInstruction': {'type': 'CustomDeltaHedge', 'amount': 1.5},
        }
    )
    assert [type(c) for c in report.comments] == [BinaryImageComments, HyperLinkImageComments]
    assert report.comments[0].data == 'abc'
    assert report.hedge_instruction == CustomDeltaHedge(amount=1.5)
    assert type(VisualStructuringReport.from_dict({'hedgeInstruction': {'type': 'DeltaHedge'}}).hedge_instruction) is (
        DeltaHedge
    )


@pytest.mark.xfail(strict=True, reason='D-13: a field typed with an abstract or oneOf base decodes as the bare base')
@pytest.mark.parametrize(
    'holder, attribute, value',
    (
        (RiskPosition, 'instrument', utils.irswap()),
        (MultiScenario, 'scenarios', (RollFwd(date='1m', realise_fwd=True),)),
    ),
    ids=('RiskPosition.instrument', 'MultiScenario.scenarios'),
)
def test_family_field_decodes_subclass(holder, attribute, value):
    decoded = getattr(holder.from_dict(holder(**{attribute: value}).to_dict()), attribute)
    decoded_type = type(decoded[0] if isinstance(value, tuple) else decoded)
    assert decoded_type is type(value[0] if isinstance(value, tuple) else value)


@pytest.mark.xfail(
    strict=True, reason='D-24: a scenario overlay inside MarketDataScenario decodes as the bare Scenario'
)
def test_overlay_round_trip():
    scenario = MarketDataScenario(scenario=utils.market_data_shock_scenario())
    decoded = MarketDataScenario.from_dict(scenario.to_dict()).scenario
    decoded_type = type(decoded)
    assert decoded_type is MarketDataShockBasedScenario
    assert decoded == scenario.scenario


@pytest.mark.xfail(strict=True, reason='D-13: a union of dataclasses always decodes as its first member')
def test_union_of_dataclasses():
    cost = BacktestStrategyTransactionCost(entry=BacktestStrategyTransactionCostModelScaled(scaling_level=0.1))
    decoded = BacktestStrategyTransactionCost.from_dict(cost.to_dict()).entry
    assert type(decoded) is BacktestStrategyTransactionCostModelScaled


@pytest.mark.xfail(strict=True, reason='D-13: a composite union such as Union[date, float] is left undecoded')
def test_composite_union_decoded():
    assert Op.from_dict({'gte': '2021-03-04', 'lte': 1.5}).gte == dt.date(2021, 3, 4)


@pytest.mark.xfail(strict=True, reason='D-13: an all-caps field such as ISO serialises as iSO')
def test_all_caps_wire_name():
    assert CommodityPowerNode(ISO='PJM').to_dict() == {'ISO': 'PJM'}


def test_scenario_context():
    roll = RollFwd(date='1m', realise_fwd=True)
    shock = utils.market_data_shock_scenario()
    with roll:
        assert Scenario.current is roll
        with shock:
            assert Scenario.current is shock
            assert roll in Scenario.path and shock in Scenario.path
        assert Scenario.current is roll
    assert roll not in Scenario.path


def _requirement(trigger):
    return trigger.trigger_requirements


def _actions(trigger):
    return trigger.actions


def _data_sources(trigger):
    source = getattr(trigger.trigger_requirements, 'data_source', None)
    return [] if source is None or isinstance(source, str) else [source]


def _transaction_models(trigger):
    return [action.transaction_cost for action in trigger.actions]


@pytest.mark.parametrize(
    'members',
    (
        lambda trigger: [trigger],
        lambda trigger: [_requirement(trigger)],
        _actions,
        _data_sources,
        _transaction_models,
    ),
    ids=('triggers', 'trigger_requirements', 'actions', 'data_sources', 'transaction_models'),
)
def test_backtest_families(members):
    strategy = utils.eleven_trigger_strategy()
    decoded = _round_trip(strategy)
    sent = [m for t in strategy.triggers for m in members(t)]
    received = [m for t in decoded.triggers for m in members(t)]
    assert sent
    assert [type(m) for m in received] == [type(m) for m in sent]
    assert received == sent


@pytest.mark.xfail(strict=True, reason='D-13: Strategy.cash_accrual decodes every model as the base CashAccrualModel')
def test_backtest_cash_accrual_family():
    model = OisFixingCashAccrualModel(start_date='-6m', end_date=dt.date(2021, 3, 4))
    assert type(_round_trip(Strategy(None, None, model)).cash_accrual) is OisFixingCashAccrualModel


@pytest.mark.xfail(strict=True, reason='D-13: Strategy.to_json() raises for an instrument with a date field')
def test_strategy_to_json_with_dates():
    strategy = Strategy(utils.irswap(), None)
    assert json.loads(strategy.to_json())['initial_portfolio'][0]['effective_date'] == '2021-03-04'


@pytest.mark.xfail(strict=True, reason='D-13: cash_accrual decodes as the base CashAccrualModel, losing its rate')
@pytest.mark.parametrize(
    'encoded',
    ({'class_type': 'cash_accrual_model', 'rate': 0.05, 'annual': True}, None),
    ids=('legacy_tag', 'round_trip'),
)
def test_cash_accrual_round_trip(encoded):
    model = ConstantCashAccrualModel(rate=0.05)
    encoded = encoded or Strategy(None, None, model).to_dict()['cash_accrual']
    decoded = Strategy.from_dict({'initial_portfolio': None, 'triggers': None, 'cash_accrual': encoded}).cash_accrual
    assert type(decoded) is ConstantCashAccrualModel
    assert decoded.rate == 0.05


@pytest.mark.xfail(strict=True, reason='D-13: actions decode only ConstantTransactionModel transaction costs')
@pytest.mark.parametrize(
    'model',
    (
        ScaledTransactionModel('notional_amount', 0.1),
        AggregateTransactionModel((ScaledTransactionModel('notional_amount', 0.1),)),
    ),
    ids=lambda m: type(m).__name__,
)
def test_action_cost_models(model):
    strategy = _one_action_strategy(AddTradeAction(utils.fx_option(), name='Costed', transaction_cost=model))
    assert _round_trip(strategy).triggers[0].actions[0].transaction_cost == model


@pytest.mark.xfail(strict=True, reason='D-13: a timedelta trade duration comes back as a string such as "5d"')
def test_timedelta_duration():
    strategy = _one_action_strategy(AddTradeAction(utils.fx_option(), dt.timedelta(days=5), name='Timed'))
    assert _round_trip(strategy).triggers[0].actions[0].trade_duration == dt.timedelta(days=5)


@pytest.mark.xfail(strict=True, reason='D-13: a dict keyed by date cannot be decoded')
@pytest.mark.parametrize(
    'value, attribute',
    (
        (AdditionalResults(hedge_pnl={dt.date(2021, 3, 4): 1.5}), 'hedge_pnl'),
        (
            AddScaledTradeAction(name='Scaled', dated_priceables={dt.date(2021, 3, 4): utils.irswap()}),
            'dated_priceables',
        ),
    ),
    ids=('AdditionalResults.hedge_pnl', 'AddScaledTradeAction.dated_priceables'),
)
def test_date_keyed_dicts(value, attribute):
    decoded = type(value).from_dict(value.to_dict())
    assert list(getattr(decoded, attribute)) == [dt.date(2021, 3, 4)]


@pytest.mark.xfail(strict=True, reason='D-13: GsDataSource.to_dict() raises when min_date or max_date is None')
def test_data_source_without_min_date():
    source = GsDataSource('DATASET', 'ASSET')
    assert GsDataSource.from_dict(source.to_dict()) == source


@pytest.mark.xfail(
    strict=True, reason="D-13: the generic engine builds a set of to_dict() results, which aren't hashable"
)
def test_action_deduplication():
    state = dt.date(2021, 3, 4)
    swap = utils.irswap().clone(name='Add_swap_2021-03-04')
    backtest = BackTest(None, [state], [], None)
    backtest.portfolio_dict[state] = Portfolio((swap,))
    ExitTradeActionImpl(ExitTradeAction(name='Exit')).apply_action(state, backtest)
    assert [payment.trade.name for payment in backtest.cash_payments[state]] == [swap.name]
