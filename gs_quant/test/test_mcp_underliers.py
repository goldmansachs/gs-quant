"""
Copyright 2026 Senanur Çetin.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied. See the License for the
specific language governing permissions and limitations
under the License.
Portions copyright Senanur Çetin. Licensed under Apache 2.0 license
"""

import datetime as dt
import json
from unittest.mock import MagicMock

import pytest

from gs_quant.mcp.tools.data import tools


def _session(payload):
    session = MagicMock()
    session.sync.get.return_value = payload
    return session


def test_get_underliers_empty_results_have_stable_payload():
    result = tools.get_underliers("MA123", user_session=_session({"results": []}))
    assert result == {
        "count": 0,
        "fullResultsURL": "https://marquee.gs.com/s/products/MA123/constituents",
        "underliers": [],
    }


def test_get_underliers_missing_results_key_is_reported():
    assert tools.get_underliers("MA123", user_session=_session({"total": 0})) == {
        "error": "Unexpected response format, no results"
    }


def test_get_underliers_missing_market_values_do_not_break_sorting():
    positions = [{"positionType": "close", "marketValue": i} for i in range(1, 23)]
    positions += [{"positionType": "close", "marketValue": None}, {"positionType": "close"}]
    result = tools.get_underliers("MA123", user_session=_session({"results": positions}))
    assert result["count"] == 24
    assert len(result["underliers"]) == 20
    assert [v["marketValue"] for v in result["underliers"]] == list(range(22, 2, -1))


def test_get_underliers_close_positions_preferred():
    positions = [{"positionType": "open", "marketValue": 500}, {"positionType": "close", "marketValue": 10}]
    result = tools.get_underliers("MA123", user_session=_session({"results": positions}))
    assert result["underliers"] == positions[1:]


def test_get_underliers_uses_as_of_endpoint():
    session = _session({"results": []})
    tools.get_underliers("MA123", as_of=dt.date(2024, 1, 2), user_session=session)
    assert session.sync.get.call_args.args[0].startswith(
        "/indices/MA123/positions/data?startDate=2024-01-02&endDate=2024-01-02&"
    )


def test_get_underliers_returns_api_errors():
    session = _session({})
    session.sync.get.side_effect = RuntimeError("API unavailable")
    assert tools.get_underliers("MA123", user_session=session) == {"error": "API unavailable"}


def test_get_underliers_nonfinite_market_values_do_not_displace_top_positions():
    positions = [
        {"positionType": "close", "marketValue": float("nan")},
        {"positionType": "close", "marketValue": float("inf")},
        {"positionType": "close", "marketValue": float("-inf")},
    ]
    positions.extend(
        {"positionType": "close", "marketValue": value}
        for value in range(21, 0, -1)
    )
    result = tools.get_underliers("MA123", user_session=_session({"results": positions}))
    assert result["count"] == 24
    assert [item["marketValue"] for item in result["underliers"]] == list(range(21, 1, -1))

@pytest.mark.parametrize(
    "response",
    [None, [], {"results": None}, {"results": "not-a-list"}, {"results": [None]}],
)
def test_get_underliers_rejects_malformed_response(response):
    assert tools.get_underliers("MA123", user_session=_session(response)) == {
        "error": "Unexpected response format, no results"
    }


def test_get_underliers_sorts_large_integer_values_without_float_overflow():
    huge_value = 10 ** 400
    positions = [{"positionType": "close", "marketValue": huge_value}]
    positions.extend(
        {"positionType": "close", "marketValue": value}
        for value in range(23, 0, -1)
    )
    result = tools.get_underliers("MA123", user_session=_session({"results": positions}))
    assert result["count"] == 24
    assert result["underliers"][0]["marketValue"] == huge_value
    assert [position["marketValue"] for position in result["underliers"][1:]] == list(range(23, 4, -1))


@pytest.mark.parametrize(
    "values",
    [
        [2.0, float("nan"), float("inf"), float("-inf")],
        list(range(1, 20)) + [float("nan"), float("inf")],
    ],
    ids=["complete_results", "truncated_results"],
)
def test_get_underliers_nonfinite_values_strict_json_payload(values):
    positions = [{"positionType": "close", "marketValue": value} for value in values]
    result = tools.get_underliers("MA123", user_session=_session({"results": positions}))

    assert result["count"] == len(values)
    assert any(position["marketValue"] is None for position in result["underliers"])
    # The MCP response must be valid JSON, not Python's permissive NaN/Infinity.
    json.dumps(result, allow_nan=False)
    # Sanitizing the response must not mutate the API's original records.
    assert positions[0]["marketValue"] == values[0]
    assert positions[-1]["marketValue"] == values[-1]


def test_get_underliers_missing_values_follow_negative_finite_values():
    # Zero is a valid market value and must outrank missing/non-finite values.
    valid_values = list(range(0, -21, -1))
    positions = [
        {"positionType": "close", "marketValue": None},
        {"positionType": "close", "marketValue": float("nan")},
        {"positionType": "close", "marketValue": float("inf")},
        {"positionType": "close", "marketValue": False},
    ] + [
        {"positionType": "close", "marketValue": value}
        for value in valid_values
    ]
    result = tools.get_underliers("MA123", user_session=_session({"results": positions}))
    assert result["count"] == len(positions)
    assert [item["marketValue"] for item in result["underliers"]] == valid_values[:20]
    json.dumps(result, allow_nan=False)


def test_get_underliers_very_negative_integer_still_out_ranks_missing():
    # A finite Python integer can be smaller than any representable float.
    finite = -(10 ** 400)
    positions = [
        {"positionType": "close", "marketValue": value}
        for value in range(-1, -20, -1)
    ]
    positions += [
        {"positionType": "close", "marketValue": None},
        {"positionType": "close", "marketValue": finite},
    ]
    result = tools.get_underliers("MA123", user_session=_session({"results": positions}))
    assert result["count"] == 21
    # The first 19 are the finite values closest to zero; the extreme finite
    # integer is still ahead of the missing entry rather than omitted.
    assert result["underliers"][-1]["marketValue"] == finite
    json.dumps(result, allow_nan=False)
