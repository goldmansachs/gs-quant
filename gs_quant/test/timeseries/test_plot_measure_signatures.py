"""
Copyright 2024 Goldman Sachs.
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
import os

import pytest

_TIMESERIES_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'timeseries')
_REQUIRED_PARAMS = ('source', 'real_time')


def _collect_plot_measures():
    """Parse timeseries modules and yield (id_string, param_set) for each @plot_measure function."""
    results = []
    for fname in sorted(os.listdir(_TIMESERIES_DIR)):
        if not fname.endswith('.py') or fname.startswith('__'):
            continue
        fpath = os.path.join(_TIMESERIES_DIR, fname)
        with open(fpath, 'r', encoding='utf-8') as fh:
            try:
                tree = ast.parse(fh.read(), filename=fname)
            except SyntaxError:
                continue
        for node in ast.iter_child_nodes(tree):
            if not isinstance(node, ast.FunctionDef):
                continue
            if any(
                (isinstance(d, ast.Call) and isinstance(d.func, ast.Name) and d.func.id == 'plot_measure')
                or (isinstance(d, ast.Name) and d.id == 'plot_measure')
                for d in node.decorator_list
            ):
                params = {a.arg for a in node.args.args + node.args.kwonlyargs}
                results.append(pytest.param(params, id=f'{fname}::{node.name}'))
    return results


_PLOT_MEASURES = _collect_plot_measures()


@pytest.mark.parametrize('params', _PLOT_MEASURES)
def test_plot_measure_accepts_required_params(params):
    """Every @plot_measure function must accept source, real_time, and request_id."""
    missing = [p for p in _REQUIRED_PARAMS if p not in params]
    assert not missing, f'missing keyword argument(s): {", ".join(missing)}'
