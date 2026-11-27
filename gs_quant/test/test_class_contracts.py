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
import datetime as dt
import json
import pathlib
import subprocess
import sys
import typing

import pytest

import gs_quant
import gs_quant.instrument  # noqa: F401
import gs_quant.workflow  # noqa: F401
from gs_quant.base import DictBase, HashableDict, Scenario
from gs_quant.common import Currency, MarketDataPattern, ParameterisedRiskMeasure
from gs_quant.test import dataclass_test_utils as utils
from gs_quant.test.dataclass_test_utils import KnownFailure

CLASSES = utils.generated_classes(utils.generated_modules())
utils.fill_field_caches_subclasses_first(CLASSES)

pytestmark = pytest.mark.filterwarnings('ignore:.*value of non-optional type:RuntimeWarning')


def _undispatched_family_field(holder, fld, member) -> bool:
    return utils.undispatched_family(holder, fld, utils.type_hints(holder)[fld.name], None)


KNOWN_FAILURES = (
    KnownFailure(
        utils.POPULATED,
        'D-8: zero-field union bases are plain dataclasses without to_dict or from_dict',
        lambda cls: not dataclasses.fields(cls),
    ),
    KnownFailure(
        utils.POPULATED,
        'D-8: from Python 3.11, a field typed as a tuple of a string forward reference raises TypeError when decoded '
        'or assigned',
        lambda cls: sys.version_info >= (3, 11) and utils.reaches(cls, utils.forward_reference),
    ),
    KnownFailure(
        frozenset({'repr'}),
        'D-29: repr() raises for a parameterised risk measure without a name or measure type',
        lambda cls: issubclass(cls, ParameterisedRiskMeasure),
    ),
    KnownFailure(
        frozenset({'kwargs', 'attributes', 'wire_names'}),
        'D-13: all-caps fields serialise as iSO-style keys that no camelCase name maps back to',
        lambda cls: bool(utils.all_caps_fields(cls)),
    ),
    KnownFailure(
        frozenset({'positional'}),
        'D-13: assigning an all-caps field whose snake_case form names another field sets that other field',
        utils.colliding_all_caps,
    ),
    KnownFailure(
        frozenset({'round_trip'}),
        'D-13: an all-caps field whose snake_case form names another field decodes into that other field',
        lambda cls: utils.reaches(cls, utils.reaches_colliding_all_caps),
    ),
    KnownFailure(
        frozenset({'hash'}),
        'D-13: a family-typed field decodes as its bare zero-field base, which is not hashable',
        lambda cls: utils.reaches(cls, utils.undispatched_zero_field_family, utils.HASH_OMITS),
    ),
    KnownFailure(
        frozenset({'hash'}),
        'D-8: a field typed with a member-less zero-field union base holds a plain dataclass, which is not hashable',
        lambda cls: utils.reaches(cls, utils.memberless_zero_field_base, utils.HASH_OMITS),
    ),
    KnownFailure(
        frozenset({'hash'}),
        'D-13: a composite union keeps a raw list or dict, which is not hashable',
        lambda cls: utils.reaches(cls, utils.collection_valued_union, utils.HASH_OMITS),
    ),
    KnownFailure(
        frozenset({'family'}),
        'D-13: a family-typed field decodes as its bare base',
        _undispatched_family_field,
    ),
)


def _params(invariant: str) -> list:
    return utils.class_params(invariant, CLASSES, KNOWN_FAILURES)


@pytest.mark.parametrize('cls', _params('payload'))
def test_payload_populates_every_field(cls):
    utils.check_payload_populates_every_field(cls)


@pytest.mark.parametrize('cls', _params('repr'))
def test_default_instance_and_repr(cls):
    utils.check_default_instance_and_repr(cls)


@pytest.mark.parametrize('cls', _params('positional'))
def test_positional_construction(cls):
    utils.check_positional_construction(cls)


@pytest.mark.parametrize('cls', _params('kwargs'))
def test_camel_case_kwargs(cls):
    utils.check_camel_case_kwargs(cls)


@pytest.mark.parametrize('cls', _params('attributes'))
def test_attributes_by_both_names(cls):
    utils.check_attributes_by_both_names(cls)


@pytest.mark.parametrize('cls', _params('round_trip'))
def test_round_trip(cls):
    utils.check_round_trip(cls)


@pytest.mark.parametrize('cls', _params('wire_names'))
def test_wire_names(cls):
    utils.check_wire_names(cls)


@pytest.mark.parametrize('cls', _params('hash'))
def test_hash_survives_deepcopy(cls):
    utils.check_hash_survives_deepcopy(cls)


@pytest.mark.parametrize('cls', _params('pickle'))
def test_pickle_round_trip(cls):
    utils.check_pickle_round_trip(cls)


@pytest.mark.parametrize('cls', _params('replace'))
def test_replace_matches_clone(cls):
    utils.check_replace_matches_clone(cls)


@pytest.mark.parametrize('cls', _params('dataclass'))
def test_dataclass_fields_match_properties(cls):
    utils.check_dataclass_fields_match_properties(cls)


@pytest.mark.parametrize('holder, fld, member', utils.family_params(CLASSES, KNOWN_FAILURES))
def test_family_member_round_trips_through_base_field(holder, fld, member):
    utils.check_family_member_round_trips_through_base_field(holder, fld, member)


@dataclasses.dataclass
class _UnionTypeAnnotations:
    rate: 'float | None' = None
    tenor: 'dt.date | str | None' = None
    level: 'dt.date | float | None' = None
    tags: 'tuple[str, ...] | None' = None
    currency: 'Currency | None' = None
    weights: 'dict[str, float] | None' = None
    pattern: 'MarketDataPattern | None' = None


@dataclasses.dataclass
class _TypingUnionAnnotations:
    rate: typing.Optional[float] = None
    tenor: typing.Optional[typing.Union[dt.date, str]] = None
    level: typing.Optional[typing.Union[dt.date, float]] = None
    tags: typing.Optional[tuple[str, ...]] = None
    currency: typing.Optional[Currency] = None
    weights: typing.Optional[dict[str, float]] = None
    pattern: typing.Optional[MarketDataPattern] = None


def test_payload_builder_reads_both_union_spellings():
    union_type = utils.payload(_UnionTypeAnnotations)
    assert set(union_type) == {f.name for f in dataclasses.fields(_UnionTypeAnnotations)}
    assert union_type == utils.payload(_TypingUnionAnnotations)


@dataclasses.dataclass
class _DictFields:
    overrides: typing.Optional[HashableDict] = None
    parameters: typing.Optional[DictBase] = None


def test_payload_builder_samples_hashable_dicts():
    sent = utils.payload(_DictFields)
    assert sent == {'overrides': {'k': 1.0}, 'parameters': {'k': 1.0}}
    assert set(sent) == utils.expected_payload_keys(_DictFields)


def test_parameterised_generics_are_not_classes():
    assert utils.is_class(Scenario)
    generics = (tuple[Scenario, ...], dict[str, float], typing.Optional[Scenario], float | None, typing.Any)
    assert not any(utils.is_class(tp) for tp in generics)
    assert utils.family_base_of(typing.Optional[tuple[Scenario, ...]]) is Scenario
    assert utils.family_base_of(tuple[tuple[Scenario, ...], ...]) is None


@dataclasses.dataclass
class _QuotedSelfReference:
    children: typing.Optional[tuple['_QuotedSelfReference', ...]] = None


def test_type_hints_resolve_quoted_names_in_builtin_generics():
    hint = utils.type_hints(_QuotedSelfReference)['children']
    assert hint == typing.Optional[tuple[_QuotedSelfReference, ...]]
    assert utils.payload(_QuotedSelfReference) == {'children': [{'children': [{}]}]}


_IMPORT_ORDER_CASES = {
    'Scenario': ('gs_quant.base', 'Scenario', 'gs_quant.risk', 'RollFwd', "date='1m', realise_fwd=True"),
    'RiskMeasureParameter': (
        'gs_quant.base',
        'RiskMeasureParameter',
        'gs_quant.common',
        'CurrencyParameter',
        "value='USD'",
    ),
}

_IMPORT_ORDER_SCRIPT = """
import dataclasses, json
from {parent_module} import {parent}
{parent}.properties()
from {module} import {cls}
obj = {cls}({kwargs})
print(json.dumps({{
    'as_dict': sorted(obj.as_dict()),
    'set_fields': sorted(f.name for f in dataclasses.fields(obj) if getattr(obj, f.name) is not None),
    'properties': sorted({cls}.properties()),
    'fields': sorted(f.name for f in dataclasses.fields({cls})),
}}))
"""


@pytest.mark.xfail(strict=True, reason="D-29: touching a parent class first leaves a subclass's field cache empty")
@pytest.mark.parametrize('case', _IMPORT_ORDER_CASES)
def test_parent_touched_first_keeps_subclass_fields(case):
    parent_module, parent, module, cls, kwargs = _IMPORT_ORDER_CASES[case]
    script = _IMPORT_ORDER_SCRIPT.format(
        parent_module=parent_module, parent=parent, module=module, cls=cls, kwargs=kwargs
    )
    root = pathlib.Path(gs_quant.__file__).parents[1]
    result = subprocess.run([sys.executable, '-c', script], capture_output=True, text=True, check=True, cwd=root)
    seen = json.loads(result.stdout.splitlines()[-1])
    assert seen['as_dict'] == seen['set_fields']
    assert seen['properties'] == seen['fields']
