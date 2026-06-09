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

# Native event-study helpers for gs_quant plot_function execution.
#
# This module is the public event-study entry point. Static event definitions,
# runtime event objects, and dataframe-processing helpers live in dedicated
# internal modules, while this file keeps the public framing API thin.
#
# The package is doing product-grade work:
#     - public API normalization
#     - source resolution
#     - symbology resolution
#     - label propagation
#     - framing
#     - impact analysis
#     - testability and documentation
#
# Architecture
#
#     Public wrappers in this file own only gs_quant-facing input normalization,
#     decorator integration, and the final public return shape.
#
#     Private components under _event_study own the actual implementation:
#         event_study_api      -> event-date request parsing and loading entry point
#         event_study_query    -> date parsing, event resolution, loader dispatch
#         event_study_objects  -> CountryEvents / AssetEvents runtime loaders
#         event_study_labels   -> propagation of contextual event labels
#         event_study_frame    -> explicit-date framing and window filtering
#         event_study_impact   -> derived-event detection and response analysis
#
# Extension Guide
#
#     To add a new event family:
#         1. add the logical event and registry mapping in event_study_definitions
#         2. decide whether it is country-scoped or asset-scoped
#         3. route resolution through event_study_query / event_study_objects
#         4. add label handling if the public output needs contextual suffixes
#
#     To add a new data source:
#         1. implement a source adapter under _event_study, next to the existing
#            macro and asset source modules
#         2. keep event_study_processing source-agnostic
#         3. dispatch to the new source from the appropriate loader path
#         4. add focused tests and keep the event-study package at full coverage
#
# Public Surface
#
#     CountryEvents is the supported public loader for country-scoped events.
#     AssetEvents is the supported public loader for asset-scoped events.
#     The supported import path is gs_quant.timeseries.event_study.
#
# Flow
#
#     frame_timeseries_around_events(assets, events, window, ...)
#         |
#         +--> normalize one asset series input
#         +--> normalize explicit event-date list
#         +--> event_study_frame.build_event_study_frame
#         +--> result DataFrame
#
#     get_country_events / get_asset_events(...)
#         |
#         +--> event_study_api.get_event_dates_internal
#         +--> event_study_query + event_study_objects
#         +--> event_study_labels.build_event_series
#
#     event_impact_analysis(...)
#         |
#         +--> event_study_impact.build_event_impact_frame
#         +--> event_study_frame.build_event_study_frame
#         +--> result DataFrame + attrs metadata

import pandas as pd
import datetime as dt
from typing import Optional

from gs_quant.common import AssetClass
from gs_quant.entities.entity import EntityType
from gs_quant.markets.securities import Asset

from gs_quant.timeseries._event_study.event_study_api import get_event_dates_internal
from gs_quant.timeseries._event_study.event_study_impact import (
    CalendarAlignment,
    EventDirection,
    EventMetric,
    build_event_impact_frame,
)
from gs_quant.timeseries._event_study.event_study_definitions import SupportedEvent, WindowType
from gs_quant.timeseries._event_study.event_study_labels import (
    build_asset_event_label,
    build_country_event_label,
    build_event_series,
    resolve_event_series_label,
)
from gs_quant.timeseries._event_study.event_study_objects import AssetEvents, CountryEvents
from gs_quant.timeseries._event_study.event_study_frame import build_event_study_frame
from .helper import plot_function, plot_measure, plot_measure_entity
from .helper import Returns
from ..errors import MqValueError


@plot_measure_entity(EntityType.COUNTRY)
def get_country_events(
    country_id: str,
    event: SupportedEvent,
    start_date: str = '1y',
    end_date: str = '0d',
    n_events: Optional[int] = None,
    **kwargs,
) -> pd.Series:
    """Return supported country-scoped event dates as a date-indexed string series.

    Architecture:
        This is a thin public wrapper. It delegates date resolution to
        ``get_event_dates_internal`` and delegates label construction to
        ``event_study_labels`` before returning the public Series shape.

    Flow:
        public country input
            --> event_study_api.get_event_dates_internal
            --> event_study_query / CountryEvents loader path
            --> event_study_labels.build_country_event_label
            --> event_study_labels.build_event_series

    :param country_id: Country entity identifier.
    :param event: Supported wired event type string.
    :param start_date: Start of the event search range. Defaults to "1y".
    :param end_date: End of the event search range. Defaults to "0d".
    :param n_events: Optional number of latest matching events to return.
    :param kwargs: Unused compatibility placeholders for decorated callers.
                   Supported legacy keys include ``source``, ``real_time``,
                   and ``request_id``.
    :return: pd.Series of YYYY-MM-DD strings ordered oldest to newest and indexed by event date.
    """
    _ = kwargs

    result = get_event_dates_internal(
        event=event.value if isinstance(event, SupportedEvent) else str(event),
        country=country_id,
        start_date=start_date,
        end_date=end_date,
        n_events=n_events,
    )
    label = build_country_event_label(
        str(result.attrs.get('query_event_type', event.value if isinstance(event, SupportedEvent) else str(event))),
        str(result.attrs.get('resolved_country', country_id)),
    )
    return build_event_series(result, label)


@plot_measure((AssetClass.Equity,), None, [])
def get_asset_events(
    asset: Asset,
    event: SupportedEvent = SupportedEvent.EARNINGS,
    start_date: str = '1y',
    end_date: str = '0d',
    n_events: Optional[int] = None,
    **kwargs,
) -> pd.Series:
    """Return supported asset-scoped event dates as a date-indexed string series.

    Architecture:
        This is a thin public wrapper. It delegates date resolution to
        ``get_event_dates_internal`` and delegates label construction to
        ``event_study_labels`` before returning the public Series shape.

    Flow:
        public asset input
            --> event_study_api.get_event_dates_internal
            --> event_study_query / AssetEvents loader path
            --> event_study_labels.build_asset_event_label
            --> event_study_labels.build_event_series

    :param asset: Asset entity.
    :param event: Supported asset-scoped event type string. Defaults to "EARNINGS".
    :param start_date: Start of the event search range. Defaults to "1y".
    :param end_date: End of the event search range. Defaults to "0d".
    :param n_events: Optional number of latest matching events to return.
    :param kwargs: Unused compatibility placeholders for decorated callers.
                   Supported legacy keys include ``source``, ``real_time``,
                   and ``request_id``.
    :return: pd.Series of YYYY-MM-DD strings ordered oldest to newest and indexed by event date.
    """
    _ = kwargs

    result = get_event_dates_internal(
        event=event.value if isinstance(event, SupportedEvent) else str(event),
        start_date=start_date,
        end_date=end_date,
        n_events=n_events,
        ticker=asset,
    )
    label = build_asset_event_label(
        str(result.attrs.get('query_event_type', event.value if isinstance(event, SupportedEvent) else str(event))),
        asset,
        result.attrs.get('ticker'),
    )
    return build_event_series(result, label)


@plot_function
def frame_timeseries_around_events(
    assets: pd.Series,
    events: [str],
    window: int = 14,
    window_type: WindowType = None,
    include_event_day: bool = True,
    **kwargs,
) -> pd.DataFrame:
    """Frame a single asset series around explicit event dates.

    Architecture:
        This public wrapper owns only public input-shape handling: one-series
        validation, acceptance of getter-returned event Series, and preservation
        of the plot-service ``events: [str]`` annotation. The actual framing
        logic lives in ``event_study_frame.build_event_study_frame``.

    Flow:
        public asset/event inputs
            --> normalize one asset series input
            --> normalize explicit event-date container
            --> resolve propagated label from getter-returned Series when present
            --> event_study_frame.build_event_study_frame
            --> public DataFrame

    :param assets: Single asset series. Accepts one pandas Series or a single-item
                                 list containing one Series.
    :param events: Event dates to frame around. The annotation intentionally
                             remains ``[str]`` because the plot-service parser
                             depends on that exact shape. At runtime this
                             wrapper also accepts getter-returned pd.Series
                             values, DatetimeIndex inputs, and explicit
                             datetime-like lists for direct Python callers.
    :param window: Number of observations before and after each event. Defaults to 14.
    :param window_type: Optional event window filter:
                                            - None or "full": keep the full framed window
                                            - "pre_event": keep only days before the event and,
                                                optionally, the event day
                                            - "post_event": keep only days after the event
                                            - "event_day": keep only the event-day row
    :param include_event_day: When window_type="pre_event", include day 0 if True.
                                                        Defaults to True.
    :param kwargs: Unused compatibility placeholder for plot_function callers.
    :return: pd.DataFrame with public columns:
                     - date: actual date in the event window
                     - value: raw series value
                     - type_of_events: propagated event label on event-day rows when available,
                                       otherwise "Event"

    Raises:
            MqValueError: If window is invalid.
            ValueError: If the asset input is unsupported or the events list is empty.
            Exception: Propagates pandas date-parsing errors for invalid event inputs.
    """
    _ = kwargs

    if not isinstance(window, int) or window < 0:
        raise MqValueError('window must be a non-negative integer')

    if isinstance(assets, list):
        if len(assets) == 0:
            raise ValueError('assets parameter must be non-empty')
        if len(assets) > 1:
            raise ValueError(
                'frame_timeseries_around_events accepts only one asset.'
                ' Run separate event studies per asset if you need comparisons.'
            )
        x = assets[0]
    else:
        x = assets

    public_event_type = 'Event'
    if isinstance(events, pd.Series):
        public_event_type = resolve_event_series_label(events)
        # get_country_events/get_asset_events return date-indexed string
        # series, while the frame builder still expects an explicit list of
        # event-date inputs.
        events = events.tolist()
    elif isinstance(events, pd.DatetimeIndex):
        # DatetimeIndex inputs are normalized to the explicit list of event
        # dates expected by the shared frame builder.
        events = events.tolist()
    elif isinstance(events, list) and all(isinstance(event, (pd.Timestamp, dt.datetime, dt.date)) for event in events):
        events = list(events)
    elif not isinstance(events, list):
        raise ValueError(f'events parameter must be a list, pd.Series, or DatetimeIndex,found: {type(events)}')

    return build_event_study_frame(
        x=x,
        event_dates=events,
        public_event_type=public_event_type,
        window=window,
        window_type=window_type,
        include_event_day=include_event_day,
    )


@plot_function
def event_impact_analysis(
    asset_a: pd.Series,
    asset_b: pd.Series,
    window: int = 14,
    threshold: float = 0.10,
    direction: EventDirection = None,
    metric: EventMetric = None,
    horizon=None,
    b_returns_type=Returns.SIMPLE,
    a_returns_type=Returns.SIMPLE,
    response_horizons=('1d',),
    response_anchor: int = 0,
    calendar_alignment: CalendarAlignment = None,
    start: Optional[dt.date] = None,
    end: Optional[dt.date] = None,
    **kwargs,
) -> pd.DataFrame:
    """Detect event dates from Asset B and frame Asset A response around them.

    Architecture:
        This is the public wrapper over ``event_study_impact``. The private
        module owns event detection, calendar alignment, response measurement,
        metadata assembly, and reuse of ``event_study_frame`` for the final
        public DataFrame shape.

    Flow:
        asset_a + asset_b inputs
            --> event_study_impact.build_event_impact_frame
            --> detect thresholded events on asset_b
            --> map event dates onto asset_a calendar
            --> event_study_frame.build_event_study_frame
            --> public DataFrame + attrs metadata

    :param asset_a: Asset series whose response is measured on mapped event dates.
    :param asset_b: Asset series used to generate the event condition.
    :param window: Number of observations before and after each derived event.
    :param threshold: Threshold applied to the derived Asset B metric.
    :param direction: Event rule direction: up, down, or absolute move. Defaults to up.
    :param metric: Metric used to derive events from Asset B. Defaults to return.
    :param horizon: Horizon used to compute the Asset B metric. Defaults to 1d.
    :param b_returns_type: Return convention for Asset B when metric is return-based.
    :param a_returns_type: Return convention used to transform Asset A response.
    :param response_horizons: Forward horizons sampled on Asset A at mapped event dates.
                              The first horizon drives the public value column; all horizons
                              are stored in df.attrs.
    :param response_anchor: Optional forward shift applied before sampling response values.
    :param calendar_alignment: Rule used to map Asset B event dates onto Asset A dates.
    :param start: Optional inclusive start date for both input series.
    :param end: Optional inclusive end date for both input series.
    :param kwargs: Unused compatibility placeholder for plot_function callers.
    :return: pd.DataFrame with public columns date, value, and type_of_events.
             Additional metadata is stored in df.attrs.
    """
    _ = kwargs

    return build_event_impact_frame(
        asset_a=asset_a,
        asset_b=asset_b,
        window=window,
        threshold=threshold,
        direction=direction,
        metric=metric,
        horizon=horizon,
        b_returns_type=b_returns_type,
        a_returns_type=a_returns_type,
        response_horizons=response_horizons,
        response_anchor=response_anchor,
        calendar_alignment=calendar_alignment,
        start=start,
        end=end,
    )


__all__ = [
    'CountryEvents',
    'AssetEvents',
    'WindowType',
    'EventDirection',
    'EventMetric',
    'CalendarAlignment',
    'get_country_events',
    'get_asset_events',
    'frame_timeseries_around_events',
    'event_impact_analysis',
]
