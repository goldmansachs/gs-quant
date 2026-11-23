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
import enum
import functools
import importlib
import inspect
import json
import pickle
import pkgutil
import re
import sys
import types
import typing

import pandas as pd
import pytest
from dataclasses_json import global_config
from inflection import underscore

from gs_quant.base import Base, HashableDict, Market

DATE = '2021-03-04'
DATETIME = '2021-03-04T05:06:07.123Z'
TIME = '05:06:07'
TENOR = '10y'
MAX_DEPTH = 2
GENERATED_PACKAGES = ('gs_quant.target',)

_SCALARS = {float: 1.5, int: 2, bool: True, str: 'abc'}
_FLOAT_OR_STR = frozenset({float, str})
_DATE_OR_STR = frozenset({dt.date, str})
_UNSET = object()


@functools.lru_cache(maxsize=None)
def generated_modules(package: str = GENERATED_PACKAGES[0]) -> tuple:
    root = importlib.import_module(package)
    return tuple(importlib.import_module(f'{package}.{m.name}') for m in pkgutil.iter_modules(root.__path__))


def is_class(tp) -> bool:
    # inspect.isclass() is True for tuple[int, ...] on Python 3.10, and for typing.Any from 3.11
    return inspect.isclass(tp) and typing.get_origin(tp) is None and tp is not typing.Any


def generated_classes(modules) -> tuple:
    return tuple(
        cls
        for module in modules
        for cls in vars(module).values()
        if is_class(cls) and cls.__module__ == module.__name__ and dataclasses.is_dataclass(cls)
    )


def fill_field_caches_subclasses_first(classes) -> None:
    # Base caches fields per class, and a subclass that hasn't filled its own cache reads its parent's
    for cls in sorted(classes, key=lambda c: len(c.__mro__), reverse=True):
        if issubclass(cls, Base) and dataclasses.fields(cls):
            cls._fields_by_name()
            cls.default_instance()


def init_fields(cls) -> tuple:
    return tuple(f for f in dataclasses.fields(cls) if f.init)


def never_serialised(fld: dataclasses.Field) -> bool:
    exclude = fld.metadata.get('dataclasses_json', {}).get('exclude')
    return fld.metadata.get('exclude') is True or (callable(exclude) and exclude(fld.name))


def static_fields(cls) -> tuple:
    return tuple(f for f in dataclasses.fields(cls) if not f.init)


def wire_name(cls, fld: dataclasses.Field) -> str:
    letter_case = fld.metadata.get('dataclasses_json', {}).get('letter_case')
    if letter_case is None:
        letter_case = getattr(cls, 'dataclass_json_config', {}).get('letter_case')
    return letter_case(fld.name) if letter_case else fld.name


@functools.lru_cache(maxsize=None)
def type_hints(cls) -> dict:
    hints = typing.get_type_hints(cls)
    return {name: _resolve_quoted_args(tp, _annotation_namespace(cls, name)) for name, tp in hints.items()}


def _annotation_namespace(cls, name: str) -> dict:
    owner = next(c for c in cls.__mro__ if name in inspect.get_annotations(c))
    return getattr(sys.modules.get(owner.__module__), '__dict__', {})


def _resolve_quoted_args(tp, namespace: dict):
    # Python 3.10's get_type_hints leaves the quoted name in tuple['X', ...] as a string; 3.11 resolves it
    args = typing.get_args(tp)
    resolved = tuple(
        namespace.get(a, a)
        if isinstance(a, str) and isinstance(tp, types.GenericAlias)
        else _resolve_quoted_args(a, namespace)
        for a in args
    )
    if resolved == args:
        return tp
    return typing.Union[resolved] if is_union(tp) else typing.get_origin(tp)[resolved]


def union_members(tp) -> tuple:
    return tuple(a for a in typing.get_args(tp) if a is not type(None)) if is_union(tp) else (tp,)


def is_union(tp) -> bool:
    return typing.get_origin(tp) in (typing.Union, types.UnionType)


def without_optional(tp):
    members = union_members(tp)
    return members[0] if is_union(tp) and len(members) == 1 else tp


def is_concrete(cls) -> bool:
    return dataclasses.is_dataclass(cls) and not inspect.isabstract(cls) and bool(dataclasses.fields(cls))


@functools.lru_cache(maxsize=None)
def concrete_subclasses(base: type, packages: tuple = GENERATED_PACKAGES) -> tuple:
    for package in packages:
        generated_modules(package)
    found, todo = set(), list(type.__subclasses__(base))
    while todo:
        sub = todo.pop()
        todo.extend(type.__subclasses__(sub))
        if sub.__module__.startswith(packages) and is_concrete(sub):
            found.add(sub)
    return tuple(sorted(found, key=lambda c: (c.__name__, c.__module__)))


def is_family_base(tp, packages: tuple = GENERATED_PACKAGES) -> bool:
    return is_class(tp) and tp is not object and bool(concrete_subclasses(tp, packages))


def statically_tagged_members(base: type, packages: tuple = GENERATED_PACKAGES) -> tuple:
    return tuple(
        member
        for member in concrete_subclasses(base, packages)
        if any(f.default not in (dataclasses.MISSING, None) for f in static_fields(member))
    )


def _wire_value(value):
    if isinstance(value, enum.Enum):
        return value.value
    if isinstance(value, (dt.date, dt.time)):
        return value.isoformat()
    return value


def payload(cls, packages: tuple = GENERATED_PACKAGES, omit=None, visit=None, with_statics=False, depth=0) -> dict:
    hints = type_hints(cls)
    out = {}
    if with_statics:
        for fld in static_fields(cls):
            if fld.default is not dataclasses.MISSING and fld.default is not None:
                out[wire_name(cls, fld)] = _wire_value(fld.default)
    for fld in init_fields(cls):
        if never_serialised(fld):
            continue
        tp = hints.get(fld.name, fld.type)
        if with_statics and fld.default is not dataclasses.MISSING and fld.default is not None:
            out[wire_name(cls, fld)] = _wire_value(fld.default)
            continue
        value = _sample(tp, depth, packages, omit, visit)
        if value is not _UNSET:
            out[wire_name(cls, fld)] = value
            if visit is not None:
                visit(cls, fld, tp, value)
    return out


def _sample(tp, depth, packages, omit, visit):
    if omit is not None and omit(tp):
        return _UNSET
    members = union_members(tp)
    if is_union(tp):
        if frozenset(members) == _FLOAT_OR_STR:
            return 1.5
        if frozenset(members) == _DATE_OR_STR:
            return TENOR
        for member in members:
            value = _sample(member, depth, packages, omit, visit)
            if value is not _UNSET:
                return value
        return _UNSET
    origin, args = typing.get_origin(tp), typing.get_args(tp)
    if origin is tuple or tp is tuple:
        item = _sample(args[0], depth, packages, omit, visit) if args else 'abc'
        return _UNSET if item is _UNSET else [item]
    if origin is dict or tp is dict:
        item = _sample(args[1], depth, packages, omit, visit) if len(args) == 2 else 1.5
        return _UNSET if item is _UNSET else {'k': item}
    if tp in _SCALARS:
        return _SCALARS[tp]
    if tp is dt.datetime:
        return DATETIME
    if tp is dt.date:
        return DATE
    if tp is dt.time:
        return TIME
    if not is_class(tp) or tp is object or issubclass(tp, Market):
        return _UNSET
    if issubclass(tp, enum.Enum):
        return next(iter(tp)).value
    if issubclass(tp, HashableDict):
        return {'k': 1.0}
    if depth >= MAX_DEPTH:
        return _UNSET
    if is_family_base(tp, packages):
        member = concrete_subclasses(tp, packages)[0]
        return payload(member, packages, omit, visit, with_statics=True, depth=depth + 1)
    if dataclasses.is_dataclass(tp):
        return payload(tp, packages, omit, visit, depth=depth + 1)
    return _UNSET


@functools.lru_cache(maxsize=None)
def reached_fields(cls, packages: tuple = GENERATED_PACKAGES, omit=None) -> tuple:
    reached = []
    payload(cls, packages, omit, visit=lambda owner, fld, tp, value: reached.append((owner, fld, tp, value)))
    return tuple(reached)


def _leaf_types(tp) -> list:
    origin, args = typing.get_origin(tp), [a for a in typing.get_args(tp) if a is not Ellipsis]
    if not args:
        return [tp]
    if origin is dict:
        args = args[1:]
    elif origin is tuple:
        args = args[:1]
    return [leaf for arg in args for leaf in _leaf_types(arg)]


def _left_at_default(tp) -> bool:
    return tp in (object, typing.Any, type(None)) or (is_class(tp) and issubclass(tp, Market))


def expected_payload_keys(cls) -> set:
    hints = type_hints(cls)
    return {
        wire_name(cls, f)
        for f in init_fields(cls)
        if not never_serialised(f) and not all(_left_at_default(leaf) for leaf in _leaf_types(hints[f.name]))
    }


def distinct_value(value, index: int):
    if value is None:
        return None
    if isinstance(value, bool):
        return value if index % 2 == 0 else not value
    if isinstance(value, enum.Enum):
        members = list(type(value))
        return members[(members.index(value) + index) % len(members)]
    if isinstance(value, (int, float)):
        return value + index
    if isinstance(value, str):
        return f'{value}{index}'
    if isinstance(value, dt.datetime):
        return value + dt.timedelta(seconds=index)
    if isinstance(value, dt.date):
        return value + dt.timedelta(days=index)
    if isinstance(value, dt.time):
        return (dt.datetime.combine(dt.date(2000, 1, 1), value) + dt.timedelta(minutes=index)).time()
    if isinstance(value, (tuple, list)):
        return type(value)(distinct_value(v, index) for v in value)
    if isinstance(value, dict):
        return type(value)({k: distinct_value(v, index) for k, v in value.items()})
    if dataclasses.is_dataclass(value):
        fld = next((f for f in init_fields(type(value)) if getattr(value, f.name) is not None), None)
        if fld is not None:
            value = copy.copy(value)
            setattr(value, fld.name, distinct_value(getattr(value, fld.name), index))
    return value


def element_type(tp):
    tp = without_optional(tp)
    if typing.get_origin(tp) is tuple:
        args = typing.get_args(tp)
        return without_optional(args[0]) if args else object
    return tp


def family_base_of(tp, packages: tuple = GENERATED_PACKAGES):
    base = element_type(tp)
    return base if is_family_base(base, packages) and not issubclass(base, Market) else None


def has_handwritten_init(cls) -> bool:
    owner = next(c for c in cls.__mro__ if '__init__' in c.__dict__)
    params = owner.__dict__.get('__dataclass_params__')
    return params is None or not params.init


def camelcase(name: str) -> str:
    name = re.sub(r'^[\-_.]', '', name)
    if not name:
        return name
    return name[0].lower() + re.sub(r'[\-_.\s]([a-z0-9])', lambda m: m.group(1).upper(), name[1:])


POPULATED = frozenset({'positional', 'kwargs', 'attributes', 'round_trip', 'wire_names', 'hash', 'pickle', 'replace'})


@dataclasses.dataclass(frozen=True)
class KnownFailure:
    invariants: frozenset
    reason: str
    applies: typing.Callable[..., bool]


def known_failure(invariant: str, case: tuple, rules) -> KnownFailure | None:
    return next((rule for rule in rules if invariant in rule.invariants and rule.applies(*case)), None)


def _param(invariant: str, case: tuple, case_id: str, rules):
    failure = known_failure(invariant, case, rules)
    marks = [pytest.mark.xfail(strict=True, reason=failure.reason)] if failure else []
    return pytest.param(*case, id=case_id, marks=marks)


def class_params(invariant: str, classes, rules) -> list:
    return [_param(invariant, (cls,), cls.__name__, rules) for cls in classes]


def family_cases(classes, packages: tuple = GENERATED_PACKAGES) -> list:
    holders = {}
    for cls in sorted(classes, key=lambda c: c.__name__):
        hints = type_hints(cls)
        for fld in init_fields(cls):
            base = family_base_of(hints[fld.name], packages)
            if base is not None and base not in holders and statically_tagged_members(base, packages):
                holders[base] = (cls, fld)
    return [
        (holder, fld, member)
        for base, (holder, fld) in holders.items()
        for member in statically_tagged_members(base, packages)
    ]


def family_params(classes, rules, packages: tuple = GENERATED_PACKAGES) -> list:
    return [
        _param('family', (holder, fld, member), f'{holder.__name__}.{fld.name}-{member.__name__}', rules)
        for holder, fld, member in family_cases(classes, packages)
    ]


def is_plain_dict(tp) -> bool:
    return tp is dict or typing.get_origin(tp) is dict


HASH_OMITS = is_plain_dict


def reaches(cls, predicate, omit=None, packages: tuple = GENERATED_PACKAGES) -> bool:
    return any(
        predicate(owner, fld, tp, value, packages=packages)
        for owner, fld, tp, value in reached_fields(cls, packages, omit)
    )


def undispatched_family(owner, fld, tp, value, packages: tuple = GENERATED_PACKAGES) -> bool:
    return family_base_of(tp, packages) is not None and tp not in global_config.decoders


def is_zero_field_base(tp) -> bool:
    base = element_type(tp)
    return is_class(base) and dataclasses.is_dataclass(base) and not dataclasses.fields(base)


def undispatched_zero_field_family(owner, fld, tp, value, packages: tuple = GENERATED_PACKAGES) -> bool:
    return is_zero_field_base(tp) and undispatched_family(owner, fld, tp, value, packages)


def memberless_zero_field_base(owner, fld, tp, value, packages: tuple = GENERATED_PACKAGES) -> bool:
    return is_zero_field_base(tp) and family_base_of(tp, packages) is None


def is_forward_reference(tp) -> bool:
    return isinstance(tp, (str, typing.ForwardRef)) or any(is_forward_reference(a) for a in typing.get_args(tp))


def forward_reference(owner, fld, tp, value, packages: tuple = GENERATED_PACKAGES) -> bool:
    return is_forward_reference(fld.type)


def raw_union_value(tp, value) -> bool:
    members = union_members(tp)
    if is_union(tp) and len(members) > 1:
        if frozenset(members) in (_FLOAT_OR_STR, _DATE_OR_STR):
            return False
        has_dataclass = any(dataclasses.is_dataclass(m) for m in members)
        return isinstance(value, list) or (isinstance(value, dict) and not has_dataclass)
    tp = without_optional(tp)
    args = typing.get_args(tp)
    if typing.get_origin(tp) is tuple and args and isinstance(value, list):
        return raw_union_value(args[0], value[0])
    if typing.get_origin(tp) is dict and len(args) == 2 and isinstance(value, dict):
        return raw_union_value(args[1], value['k'])
    return False


def collection_valued_union(owner, fld, tp, value, packages: tuple = GENERATED_PACKAGES) -> bool:
    return raw_union_value(tp, value)


def all_caps_fields(cls) -> list:
    return [f for f in dataclasses.fields(cls) if f.name.isupper()]


def colliding_all_caps(cls) -> bool:
    fields = dataclasses.fields(cls)
    return any(
        underscore(f.name) in {n for g in fields if g is not f for n in (g.name, wire_name(cls, g))}
        for f in all_caps_fields(cls)
    )


def reaches_colliding_all_caps(owner, fld, tp, value, packages: tuple = GENERATED_PACKAGES) -> bool:
    return colliding_all_caps(owner)


def populated_instance(cls, omit=None, packages: tuple = GENERATED_PACKAGES):
    sent = payload(cls, packages, omit=omit)
    if omit is None:
        assert set(sent) == expected_payload_keys(cls)
    return cls.from_dict(json.loads(json.dumps(sent)))


def _distinct_init_values(cls, instance) -> dict:
    return {f.name: distinct_value(getattr(instance, f.name), i) for i, f in enumerate(init_fields(cls))}


def _clear_name(obj):
    fld = type(obj).__dataclass_fields__.get('name')
    if fld is not None and fld.init and never_serialised(fld):
        obj.name = None
    return obj


def _expected_wire_name(fld) -> str:
    overridden = fld.metadata.get('dataclasses_json', {}).get('letter_case')
    alias = fld.metadata.get('alias') or (overridden(fld.name) if overridden else None)
    return alias or (fld.name if fld.name.isupper() else camelcase(fld.name))


def _plain_camel_case_field(cls):
    return next(
        (f for f in init_fields(cls) if wire_name(cls, f) != f.name and underscore(wire_name(cls, f)) == f.name),
        None,
    )


def check_payload_populates_every_field(cls, packages: tuple = GENERATED_PACKAGES):
    assert set(payload(cls, packages)) == expected_payload_keys(cls)


def check_default_instance_and_repr(cls):
    repr(cls.default_instance())


def check_positional_construction(cls, packages: tuple = GENERATED_PACKAGES):
    instance = populated_instance(cls, packages=packages)
    names = list(inspect.signature(cls).parameters)
    if not has_handwritten_init(cls):
        assert names == [f.name for f in init_fields(cls)]
    values = [distinct_value(getattr(instance, n), i) for i, n in enumerate(names)]
    positional = cls(*values)
    assert positional == cls(**dict(zip(names, values)))
    assert [getattr(positional, n) for n in names] == values


def check_camel_case_kwargs(cls, packages: tuple = GENERATED_PACKAGES):
    snake = _distinct_init_values(cls, populated_instance(cls, packages=packages))
    camel = {wire_name(cls, f): snake[f.name] for f in init_fields(cls)}
    with pytest.raises(TypeError):
        cls(not_a_field=1)
    if has_handwritten_init(cls):
        assert [getattr(cls(**snake), n) for n in snake] == list(snake.values())
        if camel != snake:
            with pytest.raises(TypeError):
                cls(**camel)
        return
    by_camel = cls(**camel)
    assert [getattr(by_camel, n) for n in snake] == list(snake.values())
    assert by_camel == cls(**snake)
    fld = _plain_camel_case_field(cls)
    if fld is not None:
        with pytest.raises(ValueError):
            cls(**{fld.name: snake[fld.name], wire_name(cls, fld): snake[fld.name]})


def check_attributes_by_both_names(cls, packages: tuple = GENERATED_PACKAGES):
    values = _distinct_init_values(cls, populated_instance(cls, packages=packages))
    source = cls(**values)
    copied = cls.default_instance()
    for fld in dataclasses.fields(cls):
        camel = wire_name(cls, fld)
        value = getattr(source, fld.name)
        assert getattr(source, camel) == value
        if fld.init:
            assert value == values[fld.name]
            setattr(copied, camel, value)
            assert getattr(copied, fld.name) == value
        else:
            for name in {fld.name, camel}:
                with pytest.raises(ValueError):
                    setattr(copied, name, value)
    assert copied == source


def check_round_trip(cls, packages: tuple = GENERATED_PACKAGES):
    instance = _clear_name(populated_instance(cls, packages=packages))
    assert cls.from_dict(instance.to_dict()) == instance
    assert cls.from_json(instance.to_json()) == instance


def check_wire_names(cls, packages: tuple = GENERATED_PACKAGES):
    sent = payload(cls, packages)
    assert set(sent) == expected_payload_keys(cls)
    instance = cls.from_dict(json.loads(json.dumps(sent)))
    written = instance.to_dict()
    expected = {
        _expected_wire_name(f)
        for f in dataclasses.fields(cls)
        if getattr(instance, f.name) is not None and not never_serialised(f)
    }
    assert set(written) == expected
    assert set(sent) <= set(written)


def check_hash_survives_deepcopy(cls, packages: tuple = GENERATED_PACKAGES):
    # Fields holding a plain dict make an instance unhashable by design, so they stay unset here.
    instance = populated_instance(cls, HASH_OMITS, packages)
    assert hash(instance) == hash(copy.deepcopy(instance))


def check_pickle_round_trip(cls, packages: tuple = GENERATED_PACKAGES):
    instance = populated_instance(cls, packages=packages)
    assert pickle.loads(pickle.dumps(instance)) == instance


def check_replace_matches_clone(cls, packages: tuple = GENERATED_PACKAGES):
    instance = populated_instance(cls, packages=packages)
    fld = next((f for f in init_fields(cls) if getattr(instance, f.name) is not None), None)
    if fld is None:
        assert not expected_payload_keys(cls)
        return
    current = getattr(instance, fld.name)
    changed = distinct_value(current, 1)
    change = {fld.name: None if changed == current else changed}
    replaced = dataclasses.replace(instance, **change)
    assert replaced != instance
    assert replaced == instance.clone(**change)


def check_dataclass_fields_match_properties(cls):
    assert dataclasses.is_dataclass(cls)
    names = {f.name[:-1] if f.name.endswith('_') else f.name for f in dataclasses.fields(cls)}
    assert names == cls.properties()


def check_family_member_round_trips_through_base_field(holder, fld, member, packages: tuple = GENERATED_PACKAGES):
    value = member.from_dict(json.loads(json.dumps(payload(member, packages, with_statics=True))))
    is_tuple = typing.get_origin(without_optional(type_hints(holder)[fld.name])) is tuple
    instance = holder.default_instance()
    setattr(instance, fld.name, (value,) if is_tuple else value)
    decoded = getattr(holder.from_dict(instance.to_dict()), fld.name)
    decoded_type = type(decoded[0] if is_tuple else decoded)
    assert decoded_type is member


def type_tagged(value):
    if isinstance(value, Base) or (hasattr(value, 'as_dict') and hasattr(value, 'to_dict')):
        try:
            return ['obj', type(value).__name__, {k: type_tagged(v) for k, v in value.as_dict().items()}]
        except Exception as e:
            return ['broken-obj', type(value).__name__, type(e).__name__]
    if dataclasses.is_dataclass(value) and not isinstance(value, type):
        values = {f.name: type_tagged(getattr(value, f.name, None)) for f in dataclasses.fields(value)}
        return ['obj', type(value).__name__, values]
    if isinstance(value, enum.Enum):
        return ['enum', type(value).__name__, value.value]
    if isinstance(value, dt.datetime):
        return ['datetime', value.isoformat()]
    if isinstance(value, dt.date):
        return ['date', value.isoformat()]
    if isinstance(value, dt.time):
        return ['time', value.isoformat()]
    if isinstance(value, dt.timedelta):
        return ['timedelta', value.total_seconds()]
    if isinstance(value, dict):
        if all(isinstance(k, str) for k in value):
            return {k: type_tagged(v) for k, v in value.items()}
        return ['map', [[type_tagged(k), type_tagged(v)] for k, v in value.items()]]
    if isinstance(value, (list, tuple)):
        return [type(value).__name__] + [type_tagged(v) for v in value]
    if isinstance(value, bytes):
        return ['bytes', value.hex()]
    if value is None or isinstance(value, (str, int, float, bool)):
        return [type(value).__name__, value]
    return ['opaque', type(value).__name__]


def irswap():
    from gs_quant.common import Currency, PayReceive
    from gs_quant.instrument import IRSwap

    return IRSwap(
        PayReceive.Pay,
        '10y',
        Currency.USD,
        fixed_rate=0.01,
        notional_amount=1e6,
        effective_date=dt.date(2021, 3, 4),
        name='swap',
    )


def eq_option():
    from gs_quant.instrument import EqOption

    return EqOption('.SPX', '3m', 'ATMF', 'Call', 'European', number_of_options=10, name='spx_call')


def fx_option():
    from gs_quant.instrument import FXOption

    return FXOption(
        buy_sell='Buy',
        option_type='Call',
        pair='USDJPY',
        strike_price='ATMF',
        notional_amount=1e5,
        expiration_date='2y',
        name='2y_call',
    )


def market_data_shock_scenario():
    from gs_quant.common import MarketDataShockType
    from gs_quant.risk import MarketDataPattern, MarketDataShock, MarketDataShockBasedScenario

    return MarketDataShockBasedScenario(
        shocks={MarketDataPattern('IR', 'USD'): MarketDataShock(MarketDataShockType.Absolute, 1e-4)}
    )


def parameterised_risk_measure():
    from gs_quant.common import AggregationLevel
    from gs_quant.risk import IRDelta

    return IRDelta(aggregation_level=AggregationLevel.Type, currency='local')


def eleven_trigger_strategy():
    from gs_quant.backtests.actions import (
        AddScaledTradeAction,
        AddTradeAction,
        ExitAllPositionsAction,
        ExitTradeAction,
        HedgeAction,
        ScalingActionType,
    )
    from gs_quant.backtests.data_sources import GenericDataSource, GsDataSource, MissingDataStrategy
    from gs_quant.backtests.strategy import Strategy
    from gs_quant.backtests.triggers import (
        AggregateTrigger,
        AggregateTriggerRequirements,
        DateTrigger,
        DateTriggerRequirements,
        IntradayPeriodicTrigger,
        IntradayTriggerRequirements,
        MeanReversionTrigger,
        MeanReversionTriggerRequirements,
        MktTrigger,
        MktTriggerRequirements,
        NotTrigger,
        NotTriggerRequirements,
        PeriodicTrigger,
        PeriodicTriggerRequirements,
        PortfolioTrigger,
        PortfolioTriggerRequirements,
        RiskTriggerRequirements,
        StrategyRiskTrigger,
        TriggerDirection,
    )
    from gs_quant.instrument import FXForward
    from gs_quant.risk import DollarPrice, FXDelta

    call = fx_option()
    hedge = FXForward(pair='USDJPY', settlement_date='2y', name='2y_hedge')
    d1, d2, d3 = dt.date(2023, 4, 11), dt.date(2023, 12, 25), dt.date(2024, 2, 29)
    series = pd.Series({dt.date(2021, 10, 1): 0.98, dt.date(2021, 10, 4): 1.0, dt.date(2021, 10, 5): 1.04})
    gs_data_source = GsDataSource('DATASET_ABC', 'ASSET123', d1, d2)
    generic_data_source = GenericDataSource(series, MissingDataStrategy.fill_forward)
    add_1m = AddTradeAction(call, '1m', name='Action1')
    add_to_d1 = AddTradeAction(call, d1, name='Action2')
    add_to_d2 = AddTradeAction(call, d2, name='Action3')
    hedge_action = HedgeAction(FXDelta(aggregation_level='type'), hedge, name='HedgeAction')
    exit_call = ExitTradeAction('2y_call', name='ExitAction1')
    exit_all = ExitAllPositionsAction(name='ExitEverything')
    add_scaled = AddScaledTradeAction(
        priceables=call, trade_duration='1b', scaling_level=100, scaling_type=ScalingActionType.NAV, name='Scaled1'
    )
    date_trigger = DateTrigger(DateTriggerRequirements(dates=(dt.date(2021, 12, 1),)), add_1m)
    periodic_trigger = PeriodicTrigger(PeriodicTriggerRequirements(d1, d2, '3m', (d3,)), add_to_d1)
    triggers = (
        date_trigger,
        periodic_trigger,
        DateTrigger(DateTriggerRequirements(dates=(dt.date(2021, 12, 1),)), [add_to_d2, hedge_action]),
        PeriodicTrigger(PeriodicTriggerRequirements(d1, d2, '3m', (d3,))),
        IntradayPeriodicTrigger(IntradayTriggerRequirements(dt.time(9, 17, 34), dt.time(10, 7, 57), 5.0)),
        MktTrigger(MktTriggerRequirements(generic_data_source, 1.1, TriggerDirection.BELOW), exit_call),
        StrategyRiskTrigger(RiskTriggerRequirements(DollarPrice, -1.4, TriggerDirection.BELOW), exit_all),
        AggregateTrigger(AggregateTriggerRequirements((date_trigger, periodic_trigger)), add_scaled),
        NotTrigger(NotTriggerRequirements(date_trigger)),
        PortfolioTrigger(PortfolioTriggerRequirements('len', 2)),
        MeanReversionTrigger(MeanReversionTriggerRequirements(gs_data_source, 1.5, 0, 5)),
    )
    return Strategy(None, triggers)
