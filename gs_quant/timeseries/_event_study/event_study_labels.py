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

# Event-label propagation helpers used by the public event-study wrappers.
#
# Purpose
#
#     Own the label-building rules that preserve event context across the
#     public wrappers. This module turns resolved country or asset metadata
#     into stable labels that can be attached to getter-returned Series and
#     later reused by frame_timeseries_around_events.
#
# Flow
#
#     resolved event metadata / getter result
#         --> build_country_event_label / build_asset_event_label
#         --> build_event_series
#         --> resolve_event_series_label
#         --> propagated public event label on framed output

import datetime as dt
from typing import Optional

import pandas as pd

from gs_quant.markets.securities import Asset, AssetIdentifier
from gs_quant.timeseries._event_study.event_study_definitions import normalize_country


def append_event_label_suffix(event_type: str, suffix: Optional[str]) -> str:
    """Append a normalized suffix to an event label when needed.

    :param event_type: Base event label such as ``CB_MEETING``.
    :param suffix: Optional label suffix such as ``US`` or ``AAPL``.
    :return: Label with suffix appended when both inputs are non-empty and the
             suffix is not already present.
    :raises AttributeError: If string-like normalization is attempted on an
                            object that does not behave like a string.
    """
    normalized_event_type = str(event_type).strip()
    normalized_suffix = str(suffix).strip().upper() if suffix is not None else ''
    if not normalized_event_type or not normalized_suffix:
        return normalized_event_type

    if normalized_event_type.upper().endswith(f'_{normalized_suffix}'):
        return normalized_event_type
    return f'{normalized_event_type}_{normalized_suffix}'


def extract_asset_label_suffix(asset: Asset) -> Optional[str]:
    """Extract the short asset label suffix used in asset-scoped event names.

    :param asset: Raw asset identifier string or gs_quant Asset-like object.
    :return: Short uppercase suffix such as ``AAPL`` when one can be resolved,
             otherwise None.
    :raises Exception: Does not intentionally raise; defensive downstream asset
                       access failures are swallowed and treated as missing data.
    """
    candidate = asset.strip() if isinstance(asset, str) else None

    if candidate is None:
        entity = getattr(asset, 'entity', None)
        if not isinstance(entity, dict):
            get_entity = getattr(asset, 'get_entity', None)
            if callable(get_entity):
                try:
                    entity = get_entity()
                except Exception:
                    entity = None

        identifiers = entity.get('identifiers') if isinstance(entity, dict) else None
        if isinstance(identifiers, dict):
            for key, value in identifiers.items():
                if isinstance(key, str) and key.casefold() == 'bbid' and isinstance(value, str) and value.strip():
                    candidate = value.strip()
                    break

    if candidate is None and not isinstance(asset, str):
        get_identifier = getattr(asset, 'get_identifier', None)
        if callable(get_identifier):
            try:
                candidate = get_identifier(AssetIdentifier.BLOOMBERG_ID)
            except TypeError:
                try:
                    candidate = get_identifier(AssetIdentifier.BLOOMBERG_ID, as_of=dt.date.today())
                except Exception:
                    candidate = None
            except Exception:
                candidate = None

    if candidate is None and not isinstance(asset, str):
        get_marquee_id = getattr(asset, 'get_marquee_id', None)
        if callable(get_marquee_id):
            try:
                candidate = get_marquee_id()
            except Exception:
                candidate = None

    if not isinstance(candidate, str) or not candidate.strip():
        return None

    return candidate.strip().split()[0].upper()


def build_country_event_label(event_type: str, country: str) -> str:
    """Build a country-scoped event label using the country abbreviation.

    :param event_type: Base resolved event type such as ``CB_MEETING_US`` or
                       ``CB_MEETING``.
    :param country: Country identifier accepted by normalize_country.
    :return: Event label carrying the normalized country abbreviation suffix.
    :raises MqValueError: If the supplied country is empty or unsupported.
    """
    return append_event_label_suffix(event_type, normalize_country(country).abbreviation)


def build_asset_event_label(event_type: str, asset: Asset, fallback_identifier: Optional[str] = None) -> str:
    """Build an asset-scoped event label from asset metadata or a fallback id.

    :param event_type: Base resolved event type such as ``EARNINGS``.
    :param asset: Raw asset identifier string or gs_quant Asset-like object.
    :param fallback_identifier: Optional raw identifier used when asset metadata
                                does not provide a usable suffix.
    :return: Event label carrying the normalized asset suffix when available,
             otherwise the base event label.
    :raises Exception: Does not intentionally raise; defensive asset metadata
                       lookup failures are handled inside extract_asset_label_suffix.
    """
    asset_suffix = extract_asset_label_suffix(asset)
    if not asset_suffix and isinstance(fallback_identifier, str) and fallback_identifier.strip():
        asset_suffix = fallback_identifier.strip().split()[0].upper()
    return append_event_label_suffix(event_type, asset_suffix)


def build_event_series(result: pd.DataFrame, label: str) -> pd.Series:
    """Convert an internal event-date result frame into the public Series form.

    :param result: DataFrame returned by get_event_dates_internal with a
                   ``dates`` column and optional attrs metadata.
    :param label: Public event label to assign to the returned Series.
    :return: Date-indexed object Series of ``YYYY-MM-DD`` strings with attrs
             copied from the input result plus ``event_label``.
    :raises KeyError: If the input frame does not contain a ``dates`` column.
    :raises ValueError: If pandas cannot parse values in the ``dates`` column.
    :raises TypeError: If values in the ``dates`` column have invalid types.
    """
    dates = pd.to_datetime(result['dates'])
    series = pd.Series(dates.dt.strftime('%Y-%m-%d').tolist(), index=pd.DatetimeIndex(dates), dtype=object, name=label)
    series.attrs = dict(getattr(result, 'attrs', {}))
    series.attrs['event_label'] = label
    return series


def resolve_event_series_label(events: pd.Series) -> str:
    """Resolve the best public label from a getter-returned event Series.

    :param events: Event Series produced by build_event_series or a compatible
                   Series carrying label metadata in its name or attrs.
    :return: Best-effort public event label, falling back to ``Event`` when no
             contextual metadata is available.
    :raises Exception: Does not intentionally raise; malformed attrs payloads
                       are tolerated and fall back to ``Event``.
    """
    if isinstance(events.name, str) and events.name.strip():
        return events.name.strip()

    attrs = getattr(events, 'attrs', {})
    if not isinstance(attrs, dict):
        return 'Event'

    event_label = attrs.get('event_label')
    if isinstance(event_label, str) and event_label.strip():
        return event_label.strip()

    query_event_type = attrs.get('query_event_type')
    resolved_country = attrs.get('resolved_country')
    if isinstance(query_event_type, str) and isinstance(resolved_country, str) and resolved_country.strip():
        return build_country_event_label(query_event_type, resolved_country)

    ticker = attrs.get('ticker')
    if isinstance(query_event_type, str) and isinstance(ticker, str) and ticker.strip():
        return build_asset_event_label(query_event_type, ticker, ticker)

    return 'Event'
