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

from typing import Optional, Union

import pandas as pd

from gs_quant.markets.securities import Asset
from gs_quant.timeseries._event_study.event_study_processing import normalize_asset_identifier
from gs_quant.timeseries._event_study.event_study_query import (
    load_real_event_dates,
    parse_date_param,
    resolve_query_event,
    validate_date_range,
    validate_ticker_requirement,
)


def get_event_dates_internal(
    event: str,
    country: str = None,
    start_date: str = '1y',
    end_date: str = '0d',
    n_events: Optional[int] = None,
    ticker: Optional[Union[Asset, str]] = None,
) -> pd.DataFrame:
    """Resolve public event-date inputs through the shared gs_quant loader path.

    :param event: Supported wired event type string.
    :param country: Optional country required for country-scoped event families.
    :param start_date: Start of the event search range.
    :param end_date: End of the event search range.
    :param n_events: Optional number of latest matching events to return.
    :param ticker: Optional asset identifier string or gs_quant Asset object.
    :return: DataFrame with one ``dates`` column plus resolved request metadata in attrs.
    :raises ValueError: If inputs are invalid or the query window is invalid.
    """
    normalized_ticker = normalize_asset_identifier(ticker)

    validate_ticker_requirement(event, normalized_ticker)

    start_dt = parse_date_param(start_date)
    end_dt = parse_date_param(end_date)
    validate_date_range(start_dt, end_dt)

    if n_events is not None and (not isinstance(n_events, int) or n_events <= 0):
        raise ValueError('n_events must be a positive integer when provided')

    query_event_type, resolved_country, resolved_event = resolve_query_event(event, country)
    event_dates = load_real_event_dates(
        query_event_type,
        resolved_country,
        resolved_event,
        start_dt,
        end_dt,
        ticker=ticker,
    )
    if n_events is not None:
        event_dates = event_dates[-n_events:]

    result = pd.DataFrame({'dates': [event_date.strftime('%Y-%m-%d') for event_date in event_dates]})
    result.attrs['query_event_type'] = query_event_type
    result.attrs['resolved_country'] = resolved_country
    result.attrs['resolved_event'] = resolved_event
    result.attrs['ticker'] = normalized_ticker
    return result
