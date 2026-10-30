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
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from gs_quant.markets.securities import AssetIdentifier
from gs_quant.risk import scenario_utils


@pytest.fixture
def services(monkeypatch):
    asset = MagicMock()
    asset.get_marquee_id.return_value = "MA123"
    asset.get_identifier.return_value = "AAPL.OQ"
    security_master = MagicMock()
    security_master.get_asset.return_value = asset
    dataset = MagicMock()
    dataset.get_data.return_value = "vol-data"
    dataset_class = MagicMock(return_value=dataset)
    scenario_class = MagicMock()
    scenario_class.from_dataframe.return_value = "scenario"
    monkeypatch.setattr(scenario_utils, "SecurityMaster", security_master)
    monkeypatch.setattr(scenario_utils, "Dataset", dataset_class)
    monkeypatch.setattr(scenario_utils, "MarketDataVolShockScenario", scenario_class)
    return SimpleNamespace(
        security_master=security_master,
        dataset=dataset,
        dataset_class=dataset_class,
        scenario_class=scenario_class,
    )


@pytest.fixture
def clock(monkeypatch):
    class FrozenDate(dt.date):
        current = dt.date(2031, 3, 4)

        @classmethod
        def today(cls):
            return cls.current

    class FrozenDateTime(dt.datetime):
        current = dt.datetime(2031, 3, 4, 12, 30)

        @classmethod
        def now(cls):
            return cls.current

    # Rebind just this module's datetime reference, not datetime globally.
    monkeypatch.setattr(
        scenario_utils,
        "dt",
        SimpleNamespace(date=FrozenDate, datetime=FrozenDateTime, timedelta=dt.timedelta, timezone=dt.timezone),
    )
    return SimpleNamespace(date=FrozenDate, datetime=FrozenDateTime)


def test_intraday_default_window_tracks_clock(services, clock):
    scenario_utils.build_eq_vol_scenario_intraday("AAPL.OQ", "INTRA")
    clock.datetime.current = dt.datetime(2031, 3, 5, 8, 15)
    scenario_utils.build_eq_vol_scenario_intraday("AAPL.OQ", "INTRA")

    calls = services.dataset.get_data.call_args_list
    assert [(c.kwargs["startTime"], c.kwargs["endTime"]) for c in calls] == [
        (dt.datetime(2031, 3, 4, 11, 30), dt.datetime(2031, 3, 4, 12, 30)),
        (dt.datetime(2031, 3, 5, 7, 15), dt.datetime(2031, 3, 5, 8, 15)),
    ]


def test_eod_default_date_tracks_clock(services, clock):
    scenario_utils.build_eq_vol_scenario_eod("AAPL.OQ", "EOD")
    clock.date.current = dt.date(2031, 3, 5)
    scenario_utils.build_eq_vol_scenario_eod("AAPL.OQ", "EOD")

    calls = services.dataset.get_data.call_args_list
    assert [(c.kwargs["startDate"], c.kwargs["endDate"]) for c in calls] == [
        (dt.date(2031, 3, 4), dt.date(2031, 3, 4)),
        (dt.date(2031, 3, 5), dt.date(2031, 3, 5)),
    ]


def test_intraday_explicit_window_is_preserved(services, clock):
    start, end = dt.datetime(2024, 1, 2, 9), dt.datetime(2024, 1, 2, 10)
    result = scenario_utils.build_eq_vol_scenario_intraday(
        "AAPL.OQ", "INTRA", start_time=start, end_time=end, ref_spot=190.5
    )
    assert result == "scenario"
    assert services.dataset.get_data.call_args.kwargs["startTime"] == start
    assert services.dataset.get_data.call_args.kwargs["endTime"] == end
    services.scenario_class.from_dataframe.assert_called_once_with("AAPL.OQ", "vol-data", 190.5)


def test_intraday_default_start_uses_explicit_end(services, clock):
    end = dt.datetime(2024, 1, 2, 10, 30)
    scenario_utils.build_eq_vol_scenario_intraday("AAPL.OQ", "INTRA", end_time=end)
    assert services.dataset.get_data.call_args.kwargs["startTime"] == end - dt.timedelta(hours=1)
    assert services.dataset.get_data.call_args.kwargs["endTime"] == end


def test_intraday_explicit_start_uses_current_end(services, clock):
    start = dt.datetime(2024, 1, 2, 9, 30)
    scenario_utils.build_eq_vol_scenario_intraday("AAPL.OQ", "INTRA", start_time=start)
    assert services.dataset.get_data.call_args.kwargs["startTime"] == start
    assert services.dataset.get_data.call_args.kwargs["endTime"] == dt.datetime(2031, 3, 4, 12, 30)


def test_eod_explicit_date_and_asset_type_preserved(services, clock):
    vol_date = dt.date(2024, 1, 2)
    scenario_utils.build_eq_vol_scenario_eod(
        "AAPL UW", "EOD", vol_date=vol_date, asset_name_type=AssetIdentifier.BLOOMBERG_ID
    )
    services.security_master.get_asset.assert_called_once_with(
        "AAPL UW", AssetIdentifier.BLOOMBERG_ID
    )
    services.dataset.get_data.assert_called_once_with(
        assetId=["MA123"], strikeReference="forward", startDate=vol_date, endDate=vol_date
    )


def test_intraday_aware_explicit_end_preserves_timezone(services, clock):
    end = dt.datetime(2024, 10, 14, 18, 30, tzinfo=dt.timezone(dt.timedelta(hours=3)))
    scenario_utils.build_eq_vol_scenario_intraday("AAPL.OQ", "INTRA", end_time=end)

    kwargs = services.dataset.get_data.call_args.kwargs
    assert kwargs["endTime"] == end
    assert kwargs["startTime"] == end - dt.timedelta(hours=1)
    assert kwargs["startTime"].tzinfo == end.tzinfo


@pytest.mark.parametrize(
    "end",
    [
        dt.datetime(2026, 11, 1, 1, 30, fold=1),
        dt.datetime(2026, 3, 8, 3, 30),
    ],
)
def test_intraday_aware_default_start_spans_one_elapsed_hour_at_dst(services, end):
    from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

    try:
        local_tz = ZoneInfo("America/New_York")
    except ZoneInfoNotFoundError:
        pytest.skip("Timezone database is unavailable")

    end = end.replace(tzinfo=local_tz)
    scenario_utils.build_eq_vol_scenario_intraday("AAPL.OQ", "INTRA", end_time=end)
    kwargs = services.dataset.get_data.call_args.kwargs
    start = kwargs["startTime"]

    assert kwargs["endTime"] is end
    assert start.tzinfo is end.tzinfo
    assert (
        end.astimezone(dt.timezone.utc) - start.astimezone(dt.timezone.utc)
    ) == dt.timedelta(hours=1)
