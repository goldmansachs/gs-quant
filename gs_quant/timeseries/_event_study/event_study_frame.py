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

# Event-study framing helpers.
#
# Purpose
#
#     Own the pure dataframe-shaping side of event study: calendar-date
#     normalization, event-window extraction, window filtering, and assembly of
#     the simplified public DataFrame returned by framing workflows.
#
# Flow
#
#     normalized series + explicit event dates
#         --> sorted_unique_dates
#         --> resolve_nearest_date / get_event_window
#         --> apply_window_filter
#         --> build_event_study_frame
#         --> public DataFrame

from typing import Iterable, List, Optional, Sequence

import pandas as pd

from gs_quant.timeseries._event_study.event_study_definitions import WindowType, WindowTypeInput, coerce_window_type
from gs_quant.timeseries._event_study.event_study_processing import normalize_series, resolve_event_location


EVENT_STUDY_INTERNAL_COLUMNS = [
    'date',
    'value',
    'event_type',
    '_day_offset',
    '_event_number',
    '_asset_index',
]


def to_calendar_date(value) -> pd.Timestamp:
    """Normalize one date-like value to a tz-naive calendar date.

    :param value: Date-like value understood by pandas.Timestamp.
    :return: Normalized tz-naive midnight timestamp.
    :raises ValueError: If pandas cannot parse the supplied value.
    :raises TypeError: If the supplied value has an invalid type.
    """
    timestamp = pd.Timestamp(value)
    if timestamp.tzinfo is not None:
        timestamp = timestamp.tz_localize(None)
    return timestamp.normalize()


def sorted_unique_dates(event_dates: Iterable[pd.Timestamp]) -> List[pd.Timestamp]:
    """Normalize, de-duplicate, and sort event dates.

    :param event_dates: Iterable of event timestamps.
    :return: Sorted unique list of normalized calendar dates.
    :raises ValueError: If any event date cannot be normalized by pandas.
    :raises TypeError: If any event date has an invalid type.
    """
    unique_dates = {to_calendar_date(event_date) for event_date in event_dates}
    return sorted(unique_dates)


def apply_window_filter(
    internal_df: pd.DataFrame,
    window_type: Optional[WindowTypeInput],
    include_event_day: bool,
) -> pd.DataFrame:
    """Filter internal event-study rows to the requested window segment.

    :param internal_df: Internal event-study rows with relative day offsets.
    :param window_type: Optional filter mode: full, pre_event, post_event, or event_day.
    :param include_event_day: Whether day 0 should be kept for pre_event windows.
    :return: Filtered internal DataFrame.
    :raises ValueError: If window_type is unsupported.
    """
    try:
        normalized_window_type = coerce_window_type(window_type)
    except ValueError as error:
        raise ValueError(
            "frame_timeseries_around_events supports"
            " window_type=None, 'full', 'pre_event', 'post_event', or 'event_day'"
        ) from error

    if internal_df.empty or normalized_window_type is None or normalized_window_type == WindowType.FULL:
        return internal_df
    if normalized_window_type == WindowType.PRE_EVENT:
        if include_event_day:
            return internal_df[internal_df['_day_offset'] <= 0]
        return internal_df[internal_df['_day_offset'] < 0]
    if normalized_window_type == WindowType.POST_EVENT:
        return internal_df[internal_df['_day_offset'] > 0]
    if normalized_window_type == WindowType.EVENT_DAY:
        return internal_df[internal_df['_day_offset'] == 0]
    raise ValueError(
        "frame_timeseries_around_events supports window_type=None, 'full', 'pre_event', 'post_event', or 'event_day'"
    )


def resolve_nearest_date(index: pd.DatetimeIndex, event_date: pd.Timestamp) -> Optional[pd.Timestamp]:
    """Resolve an event date to the nearest available observation date.

    :param index: Asset-series DatetimeIndex.
    :param event_date: Event calendar date.
    :return: Nearest available observation date, or None when the event lies
             outside the series range.
    :raises ValueError: If the event date cannot be normalized by pandas.
    :raises TypeError: If the event date has an invalid type.
    """
    if len(index) == 0:
        return None
    aligned_event_date = to_calendar_date(event_date)
    if aligned_event_date < index.min() or aligned_event_date > index.max():
        return None
    return index[resolve_event_location(index, aligned_event_date)]


def get_event_window(
    asset_df: pd.DataFrame,
    event_date: pd.Timestamp,
    window: int,
):
    """Extract one event window from a prepared asset dataframe.

    :param asset_df: DataFrame indexed by date with price and optional return columns.
    :param event_date: Event calendar date.
    :param window: Number of observations before and after the resolved event row.
    :return: List of row dictionaries with ``date``, ``day_offset``, and ``value``,
             or None when the event does not map to an in-range observation window.
    :raises KeyError: If required dataframe columns are missing.
    :raises IndexError: If resolved event positions are outside dataframe bounds.
    :raises ValueError: If event_date cannot be normalized by pandas.
    :raises TypeError: If event_date has an invalid type.
    """
    resolved_event_date = resolve_nearest_date(asset_df.index, event_date)
    if resolved_event_date is None:
        return None

    event_loc = asset_df.index.get_loc(resolved_event_date)
    if isinstance(event_loc, slice):
        event_loc = event_loc.start if event_loc.start is not None else 0
    elif hasattr(event_loc, '__iter__'):
        event_loc = int(next(iter(getattr(event_loc, 'nonzero', lambda: [[0]])()[0]), 0))

    start_idx = max(0, event_loc - window)
    end_idx = min(len(asset_df), event_loc + window + 1)
    offset_start = start_idx - event_loc
    window_df = asset_df.iloc[start_idx:end_idx].copy()
    if len(window_df) == 0:
        return None

    window_df['value'] = window_df['price']

    return [
        {
            'date': date,
            'day_offset': offset_start + index,
            'value': row['value'],
        }
        for index, (date, row) in enumerate(window_df.iterrows())
    ]


def build_event_study_frame(
    x: pd.Series,
    event_dates: Sequence[pd.Timestamp],
    public_event_type: str = 'Event',
    window: int = 14,
    window_type: Optional[WindowTypeInput] = None,
    include_event_day: bool = True,
) -> pd.DataFrame:
    """Build the simplified public event-study DataFrame used by gs_quant and DSL.

    :param x: Input pandas Series to frame around events.
    :param event_dates: Resolved event dates to analyze.
    :param public_event_type: Event label shown on event-day rows. Defaults to Event.
    :param window: Number of observations before and after each event. Defaults to 14.
    :param window_type: Optional filter mode: full, pre_event, post_event, or event_day.
    :param include_event_day: Whether day 0 is kept for pre_event filtering.
    :return: Public event-study DataFrame with columns date, value, and type_of_events.
    :raises ValueError: If framing parameters are invalid or no event dates are supplied.
    :raises MqValueError: If the input series fails normalization.
    """
    if not isinstance(window, int) or window < 0:
        raise ValueError('window must be a non-negative integer')

    series = normalize_series(x)
    resolved_event_dates = sorted_unique_dates(event_dates)
    if not resolved_event_dates:
        raise ValueError('events parameter must be non-empty')

    asset_df = pd.DataFrame({'price': series.values}, index=series.index).sort_index()

    all_results = []
    for event_number, event_date in enumerate(resolved_event_dates, 1):
        window_data = get_event_window(asset_df, event_date, window)
        if window_data is None:
            continue
        for row in window_data:
            all_results.append(
                {
                    'date': row['date'],
                    'value': row['value'],
                    '_day_offset': row['day_offset'],
                    '_event_number': event_number,
                    '_asset_index': 0,
                    'event_type': public_event_type if row['day_offset'] == 0 else pd.NA,
                }
            )

    if all_results:
        internal_df = pd.DataFrame(all_results, columns=EVENT_STUDY_INTERNAL_COLUMNS)
    else:
        internal_df = pd.DataFrame(columns=EVENT_STUDY_INTERNAL_COLUMNS)

    internal_df = apply_window_filter(internal_df, window_type, include_event_day)
    internal_df = internal_df.sort_values('date').reset_index(drop=True)
    return internal_df[['date', 'value', 'event_type']].rename(columns={'event_type': 'type_of_events'})
