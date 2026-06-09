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

# Impact-analysis helpers for event-study workflows.
#
# Purpose
#
#     Detect event dates from one timeseries based on thresholded moves, map
#     those dates onto a response series calendar, compute forward response
#     statistics, and assemble the simplified public DataFrame used by the
#     event-study API.
#
# Scope
#
#     This module owns:
#     - event-direction, metric, and calendar-alignment enums
#     - normalization of public impact-analysis inputs
#     - metric computation for event detection and response measurement
#     - event-date mapping across non-identical calendars
#     - forward-response metadata and summary assembly

from enum import Enum
from typing import Any, Dict, List, Optional, Sequence, Union

import pandas as pd

from gs_quant.timeseries._event_study.event_study_processing import normalize_series
from gs_quant.timeseries._event_study.event_study_frame import build_event_study_frame
from gs_quant.timeseries.analysis import LagMode, lag
from gs_quant.timeseries.econometrics import returns
from gs_quant.timeseries.helper import Returns
from gs_quant.errors import MqValueError


class EventDirection(Enum):
    """Direction rule used when thresholding the event-generating metric."""

    UP = 'up'
    DOWN = 'down'
    ABS = 'abs'


class EventMetric(Enum):
    """Metric family used for event detection and response measurement."""

    RETURN = 'return'
    PRICE_CHANGE = 'price_change'


class CalendarAlignment(Enum):
    """Rule used to map detected event dates onto the response-series calendar."""

    INTERSECT = 'intersect'
    PREVIOUS = 'previous'
    NEXT = 'next'
    SAME = 'same'


def _extract_series_asset_identifier(series: pd.Series) -> Optional[str]:
    """Extract a caller-provided asset identifier from Series attrs when present.

    :param series: Input series that may carry asset metadata in ``attrs``.
    :return: Asset identifier such as ``CL1`` when available, else None.
    """
    attrs = getattr(series, 'attrs', {})
    if not isinstance(attrs, dict):
        return None

    for key in ('asset_name', 'asset', 'symbol', 'bbid', 'ticker'):
        value = attrs.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _resolve_series_event_label(series: pd.Series, fallback: str) -> str:
    """Build a stable event-source label from series name plus optional asset metadata.

    :param series: Trigger series used to derive event dates.
    :param fallback: Fallback label when no metadata or name is available.
    :return: Human-readable event-source label such as ``CL1 spot`` or ``asset_b spot``.
    """
    asset_identifier = _extract_series_asset_identifier(series)
    series_name = str(series.name).strip() if isinstance(series.name, str) else ''

    if asset_identifier and series_name:
        normalized_identifier = asset_identifier.casefold()
        normalized_name = series_name.casefold()
        if normalized_name == normalized_identifier or normalized_name.startswith(f'{normalized_identifier} '):
            return series_name
        return f'{asset_identifier} {series_name}'

    if series_name:
        normalized_fallback = fallback.strip() if isinstance(fallback, str) else ''
        if normalized_fallback and ' ' not in series_name and series_name == series_name.casefold():
            return f'{normalized_fallback} {series_name}'
        return series_name

    if asset_identifier:
        return asset_identifier

    return fallback


def _normalize_direction(direction: Optional[Union[EventDirection, str]]) -> EventDirection:
    """Normalize a direction input to the internal enum.

    :param direction: None, EventDirection, or string value such as ``up``.
    :return: Normalized EventDirection value. Defaults to ``UP`` when input is None.
    :raises MqValueError: If the supplied value is not supported.
    """
    if direction is None:
        return EventDirection.UP
    if isinstance(direction, EventDirection):
        return direction
    normalized = str(direction).strip().lower()
    for candidate in EventDirection:
        if candidate.value == normalized:
            return candidate
    raise MqValueError("direction must be one of 'up', 'down', or 'abs'")


def _normalize_metric(metric: Optional[Union[EventMetric, str]]) -> EventMetric:
    """Normalize a metric input to the internal enum.

    :param metric: None, EventMetric, or string value such as ``return``.
    :return: Normalized EventMetric value. Defaults to ``RETURN`` when input is None.
    :raises MqValueError: If the supplied value is not supported.
    """
    if metric is None:
        return EventMetric.RETURN
    if isinstance(metric, EventMetric):
        return metric
    normalized = str(metric).strip().lower()
    for candidate in EventMetric:
        if candidate.value == normalized:
            return candidate
    raise MqValueError("metric must be one of 'return' or 'price_change'")


def _normalize_calendar_alignment(
    calendar_alignment: Optional[Union[CalendarAlignment, str]],
) -> CalendarAlignment:
    """Normalize a calendar-alignment input to the internal enum.

    :param calendar_alignment: None, CalendarAlignment, or string alignment value.
    :return: Normalized CalendarAlignment. Defaults to ``PREVIOUS`` when input is None.
    :raises MqValueError: If the supplied value is not supported.
    """
    if calendar_alignment is None:
        return CalendarAlignment.PREVIOUS
    if isinstance(calendar_alignment, CalendarAlignment):
        return calendar_alignment
    normalized = str(calendar_alignment).strip().lower()
    for candidate in CalendarAlignment:
        if candidate.value == normalized:
            return candidate
    raise MqValueError("calendar_alignment must be one of 'intersect', 'previous', 'next', or 'same'")


def _normalize_response_horizons(response_horizons: Sequence[Union[int, str]]) -> List[Union[int, str]]:
    """Normalize the requested response horizons into a concrete non-empty list.

    :param response_horizons: Sequence of integer or tenor-like forward horizons, or None.
    :return: List of normalized horizons. Defaults to ``['1d']`` when input is None.
    :raises MqValueError: If the supplied sequence is empty.
    """
    if response_horizons is None:
        return ['1d']
    normalized = list(response_horizons)
    if not normalized:
        raise MqValueError('response_horizons must be non-empty')
    return normalized


def _compute_metric(
    series: pd.Series,
    metric: EventMetric,
    horizon: Union[int, str],
    returns_type: Returns,
) -> pd.Series:
    """Compute the requested event metric over one normalized series.

    :param series: Input price-like series indexed by dates.
    :param metric: Metric family to compute: return or price change.
    :param horizon: Integer observation count or tenor-like horizon.
    :param returns_type: Return convention used for return-based metrics.
    :return: Metric series aligned to the input index.
    :raises MqValueError: If the metric is unsupported.
    """
    series = normalize_series(series)
    if metric == EventMetric.RETURN:
        return returns(series, horizon, returns_type)
    if metric == EventMetric.PRICE_CHANGE:
        shifted = lag(series, horizon, LagMode.TRUNCATE)
        return series - shifted
    raise MqValueError(f'Unsupported metric: {metric}')


def _event_mask(metric_series: pd.Series, direction: EventDirection, threshold: float) -> pd.Series:
    """Build the boolean event mask from a metric series and threshold rule.

    :param metric_series: Derived metric series used for event detection.
    :param direction: Thresholding rule: up, down, or absolute move.
    :param threshold: Numeric cutoff applied to the metric series.
    :return: Boolean mask identifying dates that qualify as events.
    :raises MqValueError: If the direction is unsupported.
    """
    if direction == EventDirection.UP:
        return metric_series >= threshold
    if direction == EventDirection.DOWN:
        return metric_series <= -abs(threshold)
    if direction == EventDirection.ABS:
        return metric_series.abs() >= abs(threshold)
    raise MqValueError(f'Unsupported direction: {direction}')


def _map_event_dates_to_series(
    series: pd.Series,
    event_dates: Sequence[pd.Timestamp],
    how: CalendarAlignment,
) -> List[pd.Timestamp]:
    """Map detected event dates onto the calendar of a target response series.

    :param series: Response series whose index defines the target calendar.
    :param event_dates: Raw detected event dates from the triggering series.
    :param how: Alignment rule used to resolve dates not present in the target index.
    :return: Ordered, de-duplicated list of mapped event dates.
    :raises MqValueError: If the alignment rule is unsupported.
    """
    series = normalize_series(series)
    index = series.index
    resolved_dates: List[pd.Timestamp] = []

    for event_date in event_dates:
        current = pd.Timestamp(event_date)
        if how == CalendarAlignment.INTERSECT:
            if current in index:
                resolved_dates.append(current)
        elif how == CalendarAlignment.SAME:
            resolved_dates.append(current)
        elif how == CalendarAlignment.PREVIOUS:
            position = index.searchsorted(current, side='right') - 1
            if position >= 0:
                resolved_dates.append(index[position])
        elif how == CalendarAlignment.NEXT:
            position = index.searchsorted(current, side='left')
            if position < len(index):
                resolved_dates.append(index[position])
        else:
            raise MqValueError(f'Unsupported calendar alignment: {how}')

    deduped: List[pd.Timestamp] = []
    seen = set()
    for resolved_date in resolved_dates:
        if resolved_date not in seen:
            deduped.append(resolved_date)
            seen.add(resolved_date)
    return deduped


def _extract_forward_responses(
    response_series: pd.Series,
    mapped_event_dates: Sequence[pd.Timestamp],
) -> pd.DataFrame:
    """Extract forward response values on the mapped event dates.

    :param response_series: Computed response metric series for the measured asset.
    :param mapped_event_dates: Event dates already aligned to the response-series calendar.
    :return: DataFrame with public columns ``date`` and ``value``.
    """
    response_series = normalize_series(response_series)
    rows = []
    for event_date in mapped_event_dates:
        event_timestamp = pd.Timestamp(event_date)
        rows.append({'date': event_timestamp, 'value': response_series.get(event_timestamp, pd.NA)})
    return pd.DataFrame(rows, columns=['date', 'value'])


def _build_forward_response_metadata(
    asset_series: pd.Series,
    mapped_event_dates: Sequence[pd.Timestamp],
    *,
    metric: EventMetric,
    response_horizons: Sequence[Union[int, str]],
    returns_type: Returns,
    response_anchor: int,
) -> Dict[str, Any]:
    """Build per-horizon response samples and summary statistics.

    :param asset_series: Response asset series used to compute forward metrics.
    :param mapped_event_dates: Event dates aligned to the response-series calendar.
    :param metric: Metric family used for forward response measurement.
    :param response_horizons: Requested forward horizons to sample.
    :param returns_type: Return convention used for return-based responses.
    :param response_anchor: Optional forward shift applied before sampling event responses.
    :return: Dictionary containing per-horizon response DataFrames and summary statistics.
    """
    forward_returns: Dict[str, pd.DataFrame] = {}
    horizon_summary: Dict[str, Dict[str, Optional[float]]] = {}

    for response_horizon in response_horizons:
        response_key = str(response_horizon)
        response_series = _compute_metric(asset_series, metric, response_horizon, returns_type).rename(
            asset_series.name
        )
        if response_anchor:
            response_series = response_series.shift(-response_anchor)

        event_responses = _extract_forward_responses(response_series, mapped_event_dates)
        forward_returns[response_key] = event_responses

        valid_values = pd.to_numeric(event_responses['value'], errors='coerce').dropna()
        horizon_summary[response_key] = {
            'count': int(valid_values.count()),
            'mean': float(valid_values.mean()) if not valid_values.empty else None,
            'median': float(valid_values.median()) if not valid_values.empty else None,
            'min': float(valid_values.min()) if not valid_values.empty else None,
            'max': float(valid_values.max()) if not valid_values.empty else None,
        }

    return {
        'forward_returns': forward_returns,
        'horizon_summary': horizon_summary,
    }


def build_event_impact_frame(
    asset_a: pd.Series,
    asset_b: pd.Series,
    *,
    window: int = 14,
    threshold: float = 0.10,
    direction: Optional[Union[EventDirection, str]] = None,
    metric: Optional[Union[EventMetric, str]] = None,
    horizon: Optional[Union[int, str]] = None,
    b_returns_type: Returns = Returns.SIMPLE,
    a_returns_type: Returns = Returns.SIMPLE,
    response_horizons: Sequence[Union[int, str]] = ('1d',),
    response_anchor: int = 0,
    calendar_alignment: Optional[Union[CalendarAlignment, str]] = None,
    start: Optional[Union[str, pd.Timestamp]] = None,
    end: Optional[Union[str, pd.Timestamp]] = None,
) -> pd.DataFrame:
    """Build the public event-impact frame and associated response metadata.

    :param asset_a: Response series whose values are framed around mapped event dates.
    :param asset_b: Trigger series used to derive raw event dates.
    :param window: Number of observations before and after each mapped event date.
    :param threshold: Numeric threshold applied to the trigger metric.
    :param direction: Event-direction rule as enum or string.
    :param metric: Metric family used for detection and response measurement.
    :param horizon: Horizon used when computing the trigger metric on ``asset_b``.
    :param b_returns_type: Return convention for return-based trigger metrics.
    :param a_returns_type: Return convention for return-based response metrics.
    :param response_horizons: Forward horizons sampled on ``asset_a`` at mapped event dates.
    :param response_anchor: Optional forward shift applied before response sampling.
    :param calendar_alignment: Rule used to align raw event dates onto ``asset_a``.
    :param start: Optional inclusive start date filter applied to both series.
    :param end: Optional inclusive end date filter applied to both series.
    :return: Public event-study DataFrame with response metadata stored in ``attrs``.
    :raises MqValueError: If parameters are invalid or input series cannot be normalized.
    :raises ValueError: Propagates downstream framing validation when mapped event dates are empty.
    """
    resolved_direction = _normalize_direction(direction)
    resolved_metric = _normalize_metric(metric)
    resolved_calendar_alignment = _normalize_calendar_alignment(calendar_alignment)
    resolved_horizon = horizon or '1d'
    resolved_response_horizons = _normalize_response_horizons(response_horizons)

    if not isinstance(window, int) or window < 0:
        raise MqValueError('window must be a non-negative integer')
    if response_anchor < 0:
        raise MqValueError('response_anchor must be a non-negative integer')

    asset_b_label = _resolve_series_event_label(asset_b, 'asset_b')

    series_a = normalize_series(asset_a)
    series_b = normalize_series(asset_b)

    if start is not None:
        start_timestamp = pd.Timestamp(start)
        series_a = series_a.loc[series_a.index >= start_timestamp]
        series_b = series_b.loc[series_b.index >= start_timestamp]
    if end is not None:
        end_timestamp = pd.Timestamp(end)
        series_a = series_a.loc[series_a.index <= end_timestamp]
        series_b = series_b.loc[series_b.index <= end_timestamp]

    series_a = normalize_series(series_a)
    series_b = normalize_series(series_b)

    metric_series = _compute_metric(series_b, resolved_metric, resolved_horizon, b_returns_type)
    event_mask = _event_mask(metric_series, resolved_direction, threshold).fillna(False)
    raw_event_dates = [pd.Timestamp(event_date) for event_date in event_mask.index[event_mask.astype(bool)]]
    mapped_event_dates = _map_event_dates_to_series(series_a, raw_event_dates, resolved_calendar_alignment)

    primary_response_horizon = resolved_response_horizons[0]
    forward_response_metadata = _build_forward_response_metadata(
        series_a,
        mapped_event_dates,
        metric=resolved_metric,
        response_horizons=resolved_response_horizons,
        returns_type=a_returns_type,
        response_anchor=response_anchor,
    )

    primary_response_series = _compute_metric(series_a, resolved_metric, primary_response_horizon, a_returns_type)
    if response_anchor:
        primary_response_series = primary_response_series.shift(-response_anchor)

    event_label = f'{asset_b_label} {resolved_direction.value} {threshold}'
    result = build_event_study_frame(
        x=primary_response_series.rename(series_a.name),
        event_dates=mapped_event_dates,
        public_event_type=event_label,
        window=window,
    )

    result.attrs = dict(getattr(result, 'attrs', {}))
    result.attrs['raw_event_dates'] = raw_event_dates
    result.attrs['mapped_event_dates'] = [pd.Timestamp(event_date) for event_date in mapped_event_dates]
    result.attrs['forward_returns'] = forward_response_metadata['forward_returns']
    result.attrs['summary'] = {
        'event_count': len(mapped_event_dates),
        'raw_event_count': len(raw_event_dates),
        'response_horizons': [str(response_horizon) for response_horizon in resolved_response_horizons],
        'primary_response_horizon': str(primary_response_horizon),
        'response_anchor': response_anchor,
        'metric': resolved_metric.value,
        'direction': resolved_direction.value,
        'threshold': threshold,
        'calendar_alignment': resolved_calendar_alignment.value,
        'horizon_summary': forward_response_metadata['horizon_summary'],
    }
    return result
