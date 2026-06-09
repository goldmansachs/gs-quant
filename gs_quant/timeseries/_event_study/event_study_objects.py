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

# Runtime event objects and event-record loading.
#
# Purpose
#
#     Own the reusable event loader objects and the logic that turns a
#     resolved event definition plus a time window into a list of EventRecord
#     objects.
#
# Design Note
#
#     CountryEvents and AssetEvents intentionally do not share a common base
#     class. They duplicate a few trivial metadata accessors, but their loader
#     responsibilities diverge at the point that matters: country-scoped and
#     asset-scoped resolution/querying use different inputs and different
#     get_data signatures. Keeping them flat avoids a weak abstraction whose
#     main benefit would only be removing a few one-line properties.
#
# Flow
#
#     CountryEvents(country, event)
#         --> resolve_country_event_definition
#         --> get_data(start_time, end_time)
#         --> event_study_macro_source.query_event_payload
#         --> build_event_records
#         --> EventRecord list
#
#     AssetEvents(event)
#         --> resolve_asset_event_definition
#         --> get_data(start_time, end_time, ticker)
#         --> event_study_asset_source.query_event_payload_with_asset
#         --> build_event_records
#         --> EventRecord list

from dataclasses import replace
from typing import List, Union

import pandas as pd

from gs_quant.markets.securities import Asset

from .event_study_asset_source import query_event_payload_with_asset
from .event_study_definitions import (
    EventRecord,
    resolve_asset_event_definition,
    resolve_country_event_definition,
)
from .event_study_macro_source import query_event_payload
from .event_study_processing import (
    build_event_records,
    normalize_asset_identifier,
)


class CountryEvents:
    def __init__(self, country: str, event: str):
        """Initialize a reusable country-scoped event loader.

        :param country: Raw country string.
        :param event: Raw country-scoped event string.
        :raises MqValueError: If the country or event pair cannot be resolved.
        """
        self.definition = resolve_country_event_definition(country, event)

    @property
    def event(self) -> str:
        """Expose the normalized logical event key.

        :return: Normalized event key.
        """
        return self.definition.event

    @property
    def event_name(self) -> str:
        """Expose the dataset event name used for queries.

        :return: Dataset event name.
        """
        return self.definition.event_name

    @property
    def event_type(self) -> str:
        """Expose the resolved output event label used in framed results.

        :return: Resolved event type string.
        """
        return self.definition.event_type

    @property
    def country(self) -> str:
        """Expose the normalized country for this country-scoped event loader."""
        return self.definition.country

    def get_data(self, start_time: pd.Timestamp, end_time: pd.Timestamp) -> List[EventRecord]:
        """Load event records for a query window.

        :param start_time: Start timestamp for the query window.
        :param end_time: End timestamp for the query window.
        :return: List of EventRecord objects for the window.
        :raises Exception: Propagates dataset query and pandas parsing errors from downstream loaders.
        """
        payload = query_event_payload(self.definition, start_time, end_time)
        return build_event_records(self.definition, payload)


class AssetEvents:
    def __init__(self, event: str):
        """Initialize a reusable asset-scoped event loader.

        :param event: Raw asset-scoped event string.
        :raises MqValueError: If the event is not asset-scoped.
        """
        self.definition = resolve_asset_event_definition(event)

    @property
    def event(self) -> str:
        """Expose the normalized logical event key.

        :return: Normalized event key.
        """
        return self.definition.event

    @property
    def event_name(self) -> str:
        """Expose the dataset event name used for queries.

        :return: Dataset event name.
        """
        return self.definition.event_name

    @property
    def event_type(self) -> str:
        """Expose the resolved output event label used in framed results.

        :return: Resolved event type string.
        """
        return self.definition.event_type

    def event_type_for_asset(self, ticker: str) -> str:
        """Expose the output event label for one asset-scoped query.

        :param ticker: Asset identifier used for the asset-scoped event query.
        :return: Resolved event type string, including the asset identifier suffix.
        """
        normalized_ticker = str(ticker).strip()
        if not normalized_ticker:
            raise ValueError('ticker must be a non-empty string')
        return f'{self.definition.event_type}_{normalized_ticker}'

    def get_data(
        self,
        start_time: pd.Timestamp,
        end_time: pd.Timestamp,
        ticker: Union[Asset, str],
    ) -> List[EventRecord]:
        """Load asset-scoped event records for a query window.

        :param start_time: Start timestamp for the query window.
        :param end_time: End timestamp for the query window.
        :param ticker: Asset identifier for the asset-scoped event query.
        :return: List of EventRecord objects for the window.
        :raises ValueError: If ticker is empty.
        :raises Exception: Propagates dataset query and pandas parsing errors from downstream loaders.
        """
        normalized_ticker = normalize_asset_identifier(ticker)
        if not normalized_ticker:
            raise ValueError('ticker must be a non-empty string')

        payload = query_event_payload_with_asset(self.definition, start_time, end_time, ticker)
        record_definition = replace(
            self.definition,
            event_type=self.event_type_for_asset(normalized_ticker),
        )
        return build_event_records(record_definition, payload)
