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

# Event-study request parsing and event-date loading.
#
# Purpose
#
#     Own the caller-facing normalization path for event-date queries: ticker
#     requirements, date parsing, public event resolution, and live event-date
#     loading through CountryEvents and AssetEvents.
#
# Flow
#
#     raw caller inputs
#         --> validate_ticker_requirement
#         --> parse_date_param / validate_date_range
#         --> resolve_query_event
#         --> load_real_event_dates
#         --> normalized event-date list for public wrappers

import datetime as dt
from typing import List, Optional, Tuple, Union

import pandas as pd

from gs_quant.markets.securities import Asset

from gs_quant.timeseries._event_study.event_study_definitions import (
    AssetEventType,
    CountryEventType,
    normalize_country,
    normalize_event,
)
from gs_quant.timeseries._event_study.event_study_frame import sorted_unique_dates, to_calendar_date
from gs_quant.timeseries._event_study.event_study_objects import AssetEvents, CountryEvents
from gs_quant.timeseries._event_study.event_study_processing import normalize_asset_identifier


EVENT_TYPES_REQUIRING_TICKER = frozenset({'EARNINGS', 'REBALANCE'})
_RELATIVE_DATE_PATTERN = r'^-?(\d+)([dwmy])$'


def validate_ticker_requirement(event_type: str, ticker: Optional[str]) -> None:
    """Validate ticker requirements for asset-scoped wired events.

    :param event_type: Raw event type string supplied by the caller.
    :param ticker: Optional normalized ticker string.
    :return: None.
    :raises ValueError: If the resolved event type requires a ticker and none is supplied.
    """
    normalized = str(event_type).strip().upper()
    if normalized in EVENT_TYPES_REQUIRING_TICKER and not ticker:
        raise ValueError(f"ticker parameter is required when event_type='{event_type}'")


def parse_date_param(value) -> pd.Timestamp:
    """Parse an absolute or relative date input into a normalized timestamp.

    :param value: Date-like input, absolute string, relative string, or None.
    :return: Normalized tz-naive calendar date.
    :raises ValueError: If relative or absolute parsing fails.
    :raises TypeError: If the input type is invalid for pandas parsing.
    """
    if isinstance(value, pd.Timestamp):
        return to_calendar_date(value)
    if isinstance(value, dt.datetime):
        return to_calendar_date(value)
    if value is None:
        return to_calendar_date(dt.datetime.now())

    text = str(value).strip()
    relative_match = pd.Series([text]).str.extract(_RELATIVE_DATE_PATTERN, expand=True).iloc[0]
    if relative_match.notna().all():
        amount = int(relative_match.iloc[0])
        unit = str(relative_match.iloc[1]).lower()
        return _apply_relative_offset(to_calendar_date(dt.datetime.now()), amount, unit, direction=-1)

    return to_calendar_date(text)


def _apply_relative_offset(anchor: pd.Timestamp, amount: int, unit: str, direction: int) -> pd.Timestamp:
    """Apply a relative offset to a normalized anchor date.

    :param anchor: Normalized anchor date.
    :param amount: Relative offset amount.
    :param unit: Relative unit: ``d``, ``w``, ``m``, or ``y``.
    :param direction: Positive or negative direction multiplier.
    :return: Shifted normalized calendar date.
    :raises ValueError: If the unit is unsupported.
    """
    if unit == 'd':
        return to_calendar_date(anchor + pd.Timedelta(days=direction * amount))
    if unit == 'w':
        return to_calendar_date(anchor + pd.Timedelta(weeks=direction * amount))
    if unit == 'm':
        return to_calendar_date(anchor + pd.DateOffset(months=direction * amount))
    if unit == 'y':
        return to_calendar_date(anchor + pd.DateOffset(years=direction * amount))
    raise ValueError(f"Unsupported relative date unit '{unit}'")


def validate_date_range(start_dt: pd.Timestamp, end_dt: pd.Timestamp) -> None:
    """Ensure an event query date window is valid.

    :param start_dt: Inclusive query start date.
    :param end_dt: Inclusive query end date.
    :return: None.
    :raises ValueError: If start_dt is after end_dt.
    """
    if start_dt > end_dt:
        raise ValueError(f'start_date ({start_dt.date()}) must be before end_date ({end_dt.date()})')


def resolve_query_event(event_type: str, country: Optional[str]) -> Tuple[str, Optional[str], str]:
    """Resolve a public event request to canonical gs_quant loading inputs.

    :param event_type: Raw public event identifier.
    :param country: Optional country input.
    :return: Tuple of public/query event label, resolved country, and canonical
             logical event family.
    :raises ValueError: If a required country is missing or the resolved event
                        / country combination is invalid for the public query.
    :raises MqValueError: If the event or country cannot be normalized.
    """
    normalized = str(event_type).strip().upper()

    if normalized == 'EARNINGS':
        return 'EARNINGS', None, 'EARNINGS'

    event_definition = normalize_event(event_type)
    if isinstance(event_definition, AssetEventType):
        return event_definition.output_type(), None, event_definition.name
    if country is None:
        raise ValueError(f"country is required when event_type '{event_type}' resolves to '{event_definition.name}'")

    country_definition = normalize_country(country)
    if isinstance(event_definition, CountryEventType):
        public_event_type = event_definition.output_type(country_definition)
        return public_event_type, country_definition.country, event_definition.name

    return event_definition.event_type, country_definition.country, event_definition.name


def load_real_event_dates(
    event_type: str,
    country: Optional[str],
    event: str,
    start_dt: pd.Timestamp,
    end_dt: pd.Timestamp,
    ticker: Optional[Union[Asset, str]] = None,
) -> List[pd.Timestamp]:
    """Load normalized event dates from the live gs_quant event loaders.

    :param event_type: Canonical query event label.
    :param country: Resolved country key.
    :param event: Canonical logical event family.
    :param start_dt: Inclusive query start date.
    :param end_dt: Inclusive query end date.
    :param ticker: Optional ticker for asset-scoped events.
    :return: Sorted unique normalized event dates within the requested window.
    :raises ValueError: If the asset-scoped loader is given an empty ticker.
    :raises Exception: Propagates downstream loader, dataset, and pandas errors.
    """
    normalized_ticker = normalize_asset_identifier(ticker)
    if normalized_ticker is not None and country is None:
        events = AssetEvents(event)
        event_records = events.get_data(start_dt, end_dt, ticker=ticker)
    else:
        events = CountryEvents(country, event)
        event_records = events.get_data(start_dt, end_dt)
    return sorted_unique_dates(
        event_date
        for record in event_records
        for event_date in [to_calendar_date(record.event_date)]
        if start_dt <= event_date <= end_dt
    )
