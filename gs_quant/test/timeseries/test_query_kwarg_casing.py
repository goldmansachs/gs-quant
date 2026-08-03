"""
Copyright 2026 Goldman Sachs.
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

# Directories scanned for calls that build/execute a Marquee data query. Any function defined
# (or later added) in these directories is covered automatically -- no per-function registration
# needed.
_SCAN_DIRS = (
    os.path.join(os.path.dirname(__file__), '..', '..', 'timeseries'),
    os.path.join(os.path.dirname(__file__), '..', '..', 'mcp', 'tools', 'data'),
)

# Method names whose kwargs are forwarded, unconverted, into a query's `where`/`entity_filter`
# dict (see DataApi.build_query in gs_quant/api/data.py). These require canonical camelCase
# field names such as `assetId`, since the server validates field names strictly and there is
# no automatic snake_case -> camelCase translation for unrecognized kwargs.
_QUERY_METHOD_NAMES = {
    'get_data',
    'get_data_last',
    'get_data_series',
    'query_data',
    'get_market_data',
    'build_query',
    'build_market_data_query',
}

# snake_case kwarg name -> required canonical name.
_BANNED_KWARGS = {
    'asset_id': 'assetId',
    'asset_ids': 'assetIds',
}


def _collect_query_calls():
    """Parse the scanned modules and yield (id_string, call_node, fname) for query/get_data calls."""
    results = []
    for scan_dir in _SCAN_DIRS:
        if not os.path.isdir(scan_dir):
            continue
        for fname in sorted(os.listdir(scan_dir)):
            if not fname.endswith('.py') or fname.startswith('__'):
                continue
            fpath = os.path.join(scan_dir, fname)
            with open(fpath, 'r', encoding='utf-8') as fh:
                try:
                    tree = ast.parse(fh.read(), filename=fname)
                except SyntaxError:
                    continue
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                func = node.func
                method_name = func.attr if isinstance(func, ast.Attribute) else getattr(func, 'id', None)
                if method_name not in _QUERY_METHOD_NAMES:
                    continue
                results.append(pytest.param(node, id=f'{fname}:{node.lineno}::{method_name}'))
    return results


_QUERY_CALLS = _collect_query_calls()


@pytest.mark.parametrize('call_node', _QUERY_CALLS)
def test_query_call_uses_canonical_asset_id_casing(call_node):
    """
    Every call into a query/get_data-style method must use canonical camelCase field names
    (e.g. `assetId`, not `asset_id`) for kwargs that are forwarded verbatim into the request
    payload -- the server validates field names strictly and rejects snake_case.
    """
    offending = [kw.arg for kw in call_node.keywords if kw.arg in _BANNED_KWARGS]
    assert not offending, (
        f'found snake_case kwarg(s) {offending} -- use canonical casing instead '
        f'({[_BANNED_KWARGS[k] for k in offending]})'
    )
