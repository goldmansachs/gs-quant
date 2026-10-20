"""
Copyright 2026 Senanur Çetin.
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

import ast
import asyncio
import datetime as dt
import inspect
from pathlib import Path

import pytest
from freezegun import freeze_time

import gs_quant
from gs_quant.datetime.date import prev_business_date
from gs_quant.lazy_defaults import NOW, TODAY, LazyDefault, lazy_defaults


class TestLazyDefaults:
    def test_default_is_resolved_on_each_call(self):
        @lazy_defaults
        def f(as_of=TODAY):
            return as_of

        with freeze_time('2031-03-04'):
            first = f()
        with freeze_time('2031-03-05'):
            second = f()

        assert (first, second) == (dt.date(2031, 3, 4), dt.date(2031, 3, 5))

    def test_now_includes_the_time(self):
        @lazy_defaults
        def f(at=NOW):
            return at

        with freeze_time('2031-03-04 12:30:15'):
            assert f() == dt.datetime(2031, 3, 4, 12, 30, 15)

    def test_arithmetic_is_evaluated_at_call_time(self):
        @lazy_defaults
        def f(
            end=TODAY + dt.timedelta(days=10), start=TODAY - dt.timedelta(days=1), earlier=NOW - dt.timedelta(hours=3)
        ):
            return start, end, earlier

        with freeze_time('2031-03-04 12:00:00'):
            assert f() == (dt.date(2031, 3, 3), dt.date(2031, 3, 14), dt.datetime(2031, 3, 4, 9))
        with freeze_time('2031-04-01 00:00:00'):
            assert f()[1] == dt.date(2031, 4, 11)

    @pytest.mark.parametrize('explicit', [dt.date(2020, 1, 1), None, 0, '2020-01-01'])
    def test_passed_arguments_are_left_exactly_as_given(self, explicit):
        @lazy_defaults
        def f(a, as_of=TODAY):
            return as_of

        assert f(1, explicit) is explicit
        assert f(1, as_of=explicit) is explicit
        assert f(a=1, as_of=explicit) is explicit

    def test_other_arguments_and_defaults_are_untouched(self):
        @lazy_defaults
        def f(a, b=2, *args, c=3, as_of=TODAY, **kwargs):
            return a, b, args, c, as_of, kwargs

        with freeze_time('2031-03-04'):
            today = dt.date(2031, 3, 4)
            assert f(1) == (1, 2, (), 3, today, {})
            assert f(1, 5, 6, 7, c=9, extra='x') == (1, 5, (6, 7), 9, today, {'extra': 'x'})
            assert f(1, as_of=None) == (1, 2, (), 3, None, {})

    def test_two_lazy_parameters_are_resolved_independently(self):
        @lazy_defaults
        def f(start=TODAY - dt.timedelta(days=7), end=TODAY):
            return start, end

        with freeze_time('2031-03-14'):
            assert f() == (dt.date(2031, 3, 7), dt.date(2031, 3, 14))
            assert f(end=dt.date(2031, 3, 1)) == (dt.date(2031, 3, 7), dt.date(2031, 3, 1))

    def test_missing_required_or_unknown_arguments_still_raise(self):
        @lazy_defaults
        def f(a, as_of=TODAY):
            return a

        with pytest.raises(TypeError):
            f()
        with pytest.raises(TypeError):
            f(1, nope=2)

    def test_methods_classmethods_and_staticmethods(self):
        class Thing:
            @lazy_defaults
            def method(self, as_of=TODAY):
                return self, as_of

            @classmethod
            @lazy_defaults
            def klass(cls, as_of=TODAY):
                return cls, as_of

            @staticmethod
            @lazy_defaults
            def static(as_of=TODAY):
                return as_of

        thing = Thing()
        with freeze_time('2031-03-04'):
            today = dt.date(2031, 3, 4)
            assert thing.method() == (thing, today)
            assert Thing.klass() == (Thing, today)
            assert thing.klass(as_of=None) == (Thing, None)
            assert Thing.static() == today == thing.static()

    def test_coroutines_are_supported(self):
        @lazy_defaults
        async def f(as_of=TODAY):
            return as_of

        with freeze_time('2031-03-04'):
            assert asyncio.run(f()) == dt.date(2031, 3, 4)
            assert asyncio.run(f(as_of=None)) is None

    def test_signature_and_metadata_are_preserved_and_readable(self):
        @lazy_defaults
        def f(a, as_of: dt.date = TODAY, end: dt.date = TODAY + dt.timedelta(days=10)):
            """Documented"""

        assert f.__name__ == 'f' and f.__doc__ == 'Documented'
        assert str(inspect.signature(f)) == (
            '(a, as_of: datetime.date = TODAY, end: datetime.date = TODAY + datetime.timedelta(days=10))'
        )

    def test_decorating_a_function_without_lazy_defaults_is_an_error(self):
        with pytest.raises(TypeError, match='no LazyDefault'):

            @lazy_defaults
            def f(a, b=1):
                pass

    def test_lazy_default_repr_and_resolve(self):
        assert repr(TODAY) == 'TODAY' and repr(NOW) == 'NOW'
        assert isinstance(TODAY, LazyDefault)
        with freeze_time('2031-03-04'):
            assert TODAY.resolve() == dt.date(2031, 3, 4)


def test_library_functions_use_todays_date_at_the_time_of_the_call():
    """prev_business_date used to fix its default date when gs_quant was imported"""
    with freeze_time('2031-03-05'):
        first_default, first_explicit = prev_business_date(), prev_business_date(dt.date(2031, 3, 5))
    with freeze_time('2031-03-12'):
        second_default, second_explicit = prev_business_date(), prev_business_date(dt.date(2031, 3, 12))

    assert first_default == first_explicit and second_default == second_explicit
    assert second_default > first_default


NOW_FUNCTIONS = {'now', 'today', 'utcnow'}
EXCLUDED_DIRS = ('test', 'target', 'content', 'documentation')


def _calls_the_clock(node: ast.AST) -> bool:
    return any(
        isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in NOW_FUNCTIONS
        for n in ast.walk(node)
    )


MIGRATED_DEFAULT_MODULES = (
    'api/gs/assets.py',
    'backtests/strategy_systematic.py',
    'data/utilities.py',
    'datetime/date.py',
    'entities/entity.py',
    'markets/baskets.py',
    'markets/index.py',
    'markets/optimizer.py',
    'markets/position_set.py',
    'markets/report.py',
    'markets/securities.py',
    'models/risk_model.py',
)


def test_no_default_argument_reads_the_clock_at_import_time():
    """A default such as `as_of: dt.date = dt.date.today()` is evaluated once, when the module is imported, so a
    long-running process keeps using the day it started on. Check only the modules migrated in this PR;
    scenario_utils.py is still unchanged upstream and is handled independently in draft PR #405."""
    root = Path(gs_quant.__file__).parent
    offenders = []
    for relative_name in MIGRATED_DEFAULT_MODULES:
        relative = Path(relative_name)
        path = root / relative
        assert path.is_file(), f'migrated module missing: {relative}'
        for node in ast.walk(ast.parse(path.read_text(encoding='utf-8'))):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                defaults = [d for d in node.args.defaults + node.args.kw_defaults if d is not None]
                if any(_calls_the_clock(d) for d in defaults):
                    offenders.append(f'{relative}:{node.lineno} {node.name}')

    assert not offenders, 'default arguments evaluated at import time: ' + ', '.join(offenders)


def test_every_lazy_default_in_the_library_is_resolved_by_the_decorator():
    """Using TODAY or NOW as a default without @lazy_defaults would pass the marker itself to the function"""
    root = Path(gs_quant.__file__).parent
    offenders = []
    for path in sorted(root.rglob('*.py')):
        relative = path.relative_to(root)
        if relative.parts[0] in EXCLUDED_DIRS or relative.name == 'lazy_defaults.py':
            continue
        for node in ast.walk(ast.parse(path.read_text(encoding='utf-8'))):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                defaults = [d for d in node.args.defaults + node.args.kw_defaults if d is not None]
                uses_marker = any(
                    isinstance(n, ast.Name)
                    and n.id in ('TODAY', 'NOW')
                    or isinstance(n, ast.Attribute)
                    and n.attr in ('TODAY', 'NOW')
                    for d in defaults
                    for n in ast.walk(d)
                )
                decorated = any('lazy_defaults' in ast.unparse(d) for d in node.decorator_list)
                if uses_marker and not decorated:
                    offenders.append(f'{relative}:{node.lineno} {node.name}')

    assert not offenders, 'lazy defaults without @lazy_defaults: ' + ', '.join(offenders)
