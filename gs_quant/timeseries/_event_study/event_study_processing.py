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

# Dataframe shaping and generic event-study processing helpers.
#
# Purpose
#
#     Own the source-agnostic transformations around the event-study flow:
#     dataset payload normalization, EventRecord construction, series
#     normalization, and event-date alignment.
#
# Flow
#
#     Dataset payload / input series
#         --> extract_event_payload / normalize_series
#         --> EventRecord payload shaping
#         --> event-date alignment
#         --> framed DataFrame inputs for the public API

from typing import Dict, List, Optional, Union

import pandas as pd

from gs_quant.markets.securities import Asset

from .event_study_definitions import EVENT_DATE_COLUMN, EventRecord, ResolvedEventDefinition
from gs_quant.errors import MqValueError


def to_float_or_none(value) -> Optional[float]:
    """Coerce payload values to float when they are present and numeric.

    :param value: Raw payload value.
    :return: Float value or None.
    """
    if value is None or value is pd.NA:
        return None
    if pd.isna(value):
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def build_macro_event_payload_dict(row: pd.Series) -> Dict[str, object]:
    """Normalize a raw dataset row into the event payload shape.

    :param row: Raw macro-event dataset row.
    :return: Normalized payload dictionary.
    """
    return {
        'event_date': row.get(EVENT_DATE_COLUMN),
        'valueActual': to_float_or_none(row.get('valueActual')),
        'valuePrevious': to_float_or_none(row.get('valuePrevious')),
        'valueForecast': to_float_or_none(row.get('valueForecast')),
        'sourceValueForecast': row.get('sourceValueForecast'),
        'valueRevised': row.get('valueRevised'),
        'valueUnit': row.get('valueUnit'),
        'source': row.get('source'),
        'sourceDateSpan': row.get('sourceDateSpan'),
        'isActive': row.get('isActive'),
        'country': row.get('country'),
        'updateTime': row.get('updateTime'),
        'sourceId': row.get('sourceId'),
        'eventName': row.get('eventName'),
        'originalCountry': row.get('originalCountry'),
        'currency': row.get('currency'),
        'sourceCategory': row.get('sourceCategory'),
        'sourceOriginalCategory': row.get('sourceOriginalCategory'),
        'importance': row.get('importance'),
        'sourceImportance': row.get('sourceImportance'),
        'referencePeriod': row.get('referencePeriod'),
        'sourceOrigin': row.get('sourceOrigin'),
        'sourceURL': row.get('sourceURL'),
        'sourceLastUpdate': row.get('sourceLastUpdate'),
        'sourceTicker': row.get('sourceTicker'),
        'sourceSymbol': row.get('sourceSymbol'),
        'id': row.get('id'),
    }


def build_event_record(definition: ResolvedEventDefinition, row: pd.Series) -> EventRecord:
    """Build one EventRecord from a resolved definition and raw row.

    :param definition: Resolved event metadata.
    :param row: Raw payload row.
    :return: EventRecord with normalized payload.
    :raises ValueError: If the event date cannot be normalized by pandas.
    :raises TypeError: If the event date has an invalid type.
    """
    payload = build_macro_event_payload_dict(row)
    event_date = pd.Timestamp(payload[EVENT_DATE_COLUMN])
    if getattr(event_date, 'tzinfo', None) is not None:
        event_date = event_date.tz_localize(None)
    payload[EVENT_DATE_COLUMN] = event_date.normalize()
    return EventRecord(definition=definition, payload=payload)


def build_event_records(definition: ResolvedEventDefinition, event_payload: pd.DataFrame) -> List[EventRecord]:
    """Convert a payload DataFrame into EventRecord objects.

    :param definition: Resolved event metadata.
    :param event_payload: Normalized payload DataFrame.
    :return: List of EventRecord objects.
    :raises ValueError: If an event date cannot be normalized by pandas.
    :raises TypeError: If an event date has an invalid type.
    """
    if event_payload.empty:
        return []

    return [build_event_record(definition, row) for _, row in event_payload.iterrows()]


def normalize_series(x: pd.Series) -> pd.Series:
    """Validate and normalize the input series for event framing.

    :param x: Input pandas Series.
    :return: Numeric series with normalized, deduplicated DatetimeIndex.
    :raises MqValueError: If the input is not a usable datetime-indexed numeric series.
    """
    if not isinstance(x, pd.Series):
        raise MqValueError('x must be a pandas Series')
    if x.empty:
        raise MqValueError('x must not be empty')
    if not isinstance(x.index, pd.DatetimeIndex):
        raise MqValueError('x must have a DatetimeIndex')

    normalized = pd.Series(pd.to_numeric(x, errors='coerce'), index=pd.to_datetime(x.index).normalize(), name=x.name)
    normalized = normalized.dropna()
    if normalized.empty:
        raise MqValueError('x must contain at least one numeric observation')

    return normalized.groupby(level=0).last().sort_index()


def extract_event_payload(raw_events: pd.DataFrame) -> pd.DataFrame:
    """Attach normalized event dates to the raw dataset payload.

    :param raw_events: Raw DataFrame returned by the macro-events dataset.
    :return: Normalized payload DataFrame with event_date column.
    :raises ValueError: If date values cannot be converted by pandas.
    :raises TypeError: If date values have invalid types.
    """
    if raw_events is None or len(raw_events.index) == 0:
        return pd.DataFrame(columns=[EVENT_DATE_COLUMN])

    if isinstance(raw_events.index, pd.DatetimeIndex):
        timestamps = pd.to_datetime(raw_events.index, errors='coerce')
    elif 'date' in raw_events.columns:
        timestamps = pd.to_datetime(raw_events['date'], errors='coerce')
    else:
        timestamps = pd.to_datetime(raw_events.index, errors='coerce')

    valid_rows = pd.Index(timestamps).notna()
    payload = raw_events.loc[valid_rows].copy()
    if len(payload.index) == 0:
        return pd.DataFrame(columns=[EVENT_DATE_COLUMN])

    payload[EVENT_DATE_COLUMN] = pd.DatetimeIndex(pd.to_datetime(timestamps[valid_rows])).normalize()
    return payload.sort_values(EVENT_DATE_COLUMN).reset_index(drop=True)


def normalize_asset_identifier(ticker: Optional[Union[Asset, str]]) -> Optional[str]:
    """Normalize an asset-scoped identifier into a string payload key.

    :param ticker: Asset identifier string, gs_quant Asset object, or None.
    :return: Normalized identifier string, or None when no identifier was supplied.
    :raises ValueError: If the identifier cannot be converted into a usable string.
    """
    if ticker is None:
        return None
    if isinstance(ticker, str):
        return ticker.strip()

    marquee_id_getter = getattr(ticker, 'get_marquee_id', None)
    if callable(marquee_id_getter):
        marquee_id = marquee_id_getter()
        if isinstance(marquee_id, str):
            return marquee_id.strip()

    raise ValueError('ticker must be a non-empty string')


def align_event_date_to_index(index: pd.DatetimeIndex, event_date: pd.Timestamp) -> pd.Timestamp:
    """Align an event timestamp to the timezone convention of a series index.

    :param index: Target series index.
    :param event_date: Event timestamp.
    :return: Normalized timestamp aligned to the index timezone convention.
    :raises ValueError: If the event timestamp cannot be converted by pandas.
    :raises TypeError: If the event timestamp has an invalid type.
    """
    aligned = pd.Timestamp(event_date)

    if aligned.tzinfo is not None and index.tz is None:
        aligned = aligned.tz_localize(None)
    elif aligned.tzinfo is None and index.tz is not None:
        aligned = aligned.tz_localize(index.tz)
    elif aligned.tzinfo is not None and index.tz is not None:
        aligned = aligned.tz_convert(index.tz)

    return aligned.normalize()


def resolve_event_location(index: pd.DatetimeIndex, event_date: pd.Timestamp) -> int:
    """Map an event date to the nearest available observation index.

    :param index: Target series index.
    :param event_date: Calendar event date.
    :return: Integer location in the series index.
    :raises ValueError: If the event date cannot be aligned by pandas.
    :raises TypeError: If the event date has an invalid type.
    """
    event_date = align_event_date_to_index(index, event_date)

    if event_date in index:
        loc = index.get_loc(event_date)
        if isinstance(loc, slice):
            return loc.start or 0
        if hasattr(loc, '__iter__') and not isinstance(loc, int):
            return int(next(iter(loc.nonzero()[0]), 0))
        return int(loc)

    insert_at = index.searchsorted(event_date)
    if insert_at <= 0:
        return 0
    if insert_at >= len(index):
        return len(index) - 1

    before = index[insert_at - 1]
    after = index[insert_at]
    if abs((event_date - before).days) <= abs((after - event_date).days):
        return insert_at - 1
    return insert_at
