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

# Static event-study definitions and lookup rules.
#
# Purpose
#
#     Own the immutable event model and registry data used by the event-study
#     flow: supported countries, supported event types, and normalized
#     resolved definitions.
#
# Structure
#
#     Core resolution entry points:
#         normalize_country
#         normalize_event
#         resolve_country_event_definition
#         resolve_asset_event_definition
#
#     Support helpers:
#         coerce_supported_event
#         coerce_window_type
#         canonicalize_lookup_text
#
#     Frozen dataclasses are used throughout this module because these types are
#     value objects over static or resolved event metadata. Declarative field
#     definitions make the registry easier to read, generated value semantics
#     help in tests and debugging, and immutability reduces the chance of
#     accidentally mutating shared registry state after initialization.
#
#     Formatting-only helpers have been inlined so this module mostly reads as
#     registry data plus the real normalization and resolution path.
#
# Flow
#
#     raw country/event strings
#         --> normalize_country / normalize_event
#         --> resolve_country_event_definition / resolve_asset_event_definition
#         --> ResolvedEventDefinition
#         --> consumed by CountryEvents, AssetEvents, and processing helpers

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Optional, Union

import pandas as pd

from gs_quant.errors import MqValueError
from gs_quant.target.countries import Country, CountryXref


MACRO_EVENT_SOURCE = "TradingEconomics"
EVENT_DATE_COLUMN = "event_date"


class SupportedEvent(Enum):
    """Supported logical event families understood by the event-study flow."""

    CB = "CB"
    GDP = "GDP"
    NFP = "NFP"
    PPI = "PPI"
    INFLATION_YOY = "INFLATION YoY"
    INFLATION_MOM = "INFLATION MoM"
    EARNINGS = "EARNINGS"


EventInput = Union[SupportedEvent, str]


class WindowType(Enum):
    """Supported public window-filter modes for framed event-study output."""

    FULL = "full"
    PRE_EVENT = "pre_event"
    POST_EVENT = "post_event"
    EVENT_DAY = "event_day"


WindowTypeInput = Union[WindowType, str]


def coerce_supported_event(event_name: EventInput) -> SupportedEvent:
    """Coerce a raw event input into the SupportedEvent enum.

    :param event_name: Raw event enum or string.
    :return: SupportedEvent enum value.
    :raises ValueError: If the supplied string is not a valid SupportedEvent value.
    """
    if isinstance(event_name, SupportedEvent):
        return event_name
    return SupportedEvent(str(event_name))


def coerce_window_type(window_type: Optional[WindowTypeInput]) -> Optional[WindowType]:
    """Coerce a raw window-type input into the WindowType enum.

    :param window_type: Raw window type enum, string, or None.
    :return: Normalized WindowType enum value, or None when no filter was supplied.
    :raises ValueError: If the supplied string is not a valid WindowType value.
    """
    if window_type is None:
        return None
    if isinstance(window_type, WindowType):
        return window_type
    return WindowType(str(window_type).lower())


@dataclass(frozen=True)
class CountryEventDefinition:
    """Static country-scoped event registry entry.

    :param country: Canonical country name.
    :param abbreviation: Country abbreviation used in public event labels.
    :param event_names: Mapping from logical event family to dataset event name.
    :param gs_country: Derived gs_quant Country model created during initialization.
    """

    country: str
    abbreviation: str
    event_names: Dict[SupportedEvent, str]
    gs_country: Country = field(init=False)

    def __post_init__(self):
        """Normalize registry fields after dataclass initialization.

        :return: None.
        :raises ValueError: If event_names contains unsupported event keys.
        """
        object.__setattr__(
            self,
            'gs_country',
            Country(name=self.country, xref=CountryXref(alpha2=self.abbreviation)),
        )
        object.__setattr__(
            self,
            'event_names',
            {coerce_supported_event(event_name): dataset_name for event_name, dataset_name in self.event_names.items()},
        )

    def supports_event(self, event_name: EventInput) -> bool:
        """Check whether this country supports a named event key.

        :param event_name: Normalized logical event name.
        :return: True when the event exists in this country's mapping, else False.
        """
        return coerce_supported_event(event_name) in self.event_names

    def get_event_name(self, event_name: EventInput) -> Optional[str]:
        """Map a logical event key to the dataset event name.

        :param event_name: Normalized logical event name.
        :return: Dataset event name or None when unsupported.
        """
        return self.event_names.get(coerce_supported_event(event_name))


@dataclass(frozen=True)
class EventType:
    """Base event-family metadata shared by country and asset event types.

    :param event: Logical SupportedEvent enum value.
    :param event_type: Public output event-family label.
    """

    event: SupportedEvent
    event_type: str

    @property
    def name(self) -> str:
        """Expose the logical event family name.

        :return: Supported event name string.
        """
        return self.event.value


@dataclass(frozen=True)
class CountryEventType(EventType):
    def output_type(self, country_definition: CountryEventDefinition) -> str:
        """Build the output event label for a country-scoped event.

        :param country_definition: Normalized country definition.
        :return: Event label with country abbreviation suffix.
        """
        return f"{self.event_type}_{country_definition.abbreviation}"


@dataclass(frozen=True)
class AssetEventType(EventType):
    """Asset-scoped event-family metadata.

    :param event: Logical SupportedEvent enum value.
    :param event_type: Base public output label for the asset event family.
    :param event_name: Dataset event name used when querying the source.
    """

    event_name: str

    def output_type(self) -> str:
        """Build the base output label for asset-scoped events.

        :return: Base asset-scoped event label.
        """
        return self.event_type


@dataclass(frozen=True)
class ResolvedEventDefinition:
    """Resolved query metadata produced from raw country and event inputs.

    :param country: Resolved country name, or None for asset-scoped events.
    :param event: Canonical logical event family.
    :param event_name: Dataset event name used by downstream loaders.
    :param event_type: Public output event label used in framing results.
    """

    country: Optional[str]
    event: str
    event_name: str
    event_type: str


@dataclass(frozen=True)
class EventRecord:
    definition: ResolvedEventDefinition
    payload: Dict[str, object]

    @property
    def event_date(self) -> pd.Timestamp:
        """Expose the normalized event date from the payload.

        :return: Normalized pandas Timestamp for the event row.
        :raises KeyError: If the payload is missing the event date field.
        :raises ValueError: If the event date cannot be parsed by pandas.
        :raises TypeError: If the payload event date has an invalid type.
        """
        return pd.Timestamp(self.payload[EVENT_DATE_COLUMN]).normalize()

    @property
    def type_of_event(self) -> str:
        """Expose the resolved event output label for this record.

        :return: Resolved event type string.
        """
        return self.definition.event_type

    def to_dict(self) -> Dict[str, object]:
        """Return a shallow dictionary copy of the event payload.

        :return: Payload dictionary copy.
        """
        return dict(self.payload)


EVENT_TYPES: Dict[SupportedEvent, EventType] = {
    SupportedEvent.CB: CountryEventType(
        event=SupportedEvent.CB,
        event_type="CB_MEETING",
    ),
    SupportedEvent.INFLATION_YOY: CountryEventType(
        event=SupportedEvent.INFLATION_YOY,
        event_type="INFLATION_YOY",
    ),
    SupportedEvent.GDP: CountryEventType(
        event=SupportedEvent.GDP,
        event_type="GDP",
    ),
    SupportedEvent.NFP: CountryEventType(
        event=SupportedEvent.NFP,
        event_type="NFP",
    ),
    SupportedEvent.PPI: CountryEventType(
        event=SupportedEvent.PPI,
        event_type="PPI",
    ),
    SupportedEvent.INFLATION_MOM: CountryEventType(
        event=SupportedEvent.INFLATION_MOM,
        event_type="INFLATION_MOM",
    ),
    SupportedEvent.EARNINGS: AssetEventType(
        event=SupportedEvent.EARNINGS,
        event_type="EARNINGS",
        event_name="Earnings Release",
    ),
}


COUNTRY_EVENT_DEFINITIONS: Dict[str, CountryEventDefinition] = {
    "Australia": CountryEventDefinition(
        country="Australia",
        abbreviation="AU",
        event_names={
            SupportedEvent.CB: "RBA Interest Rate Decision",
            SupportedEvent.GDP: "GDP Growth Rate QoQ",
            SupportedEvent.INFLATION_YOY: "Inflation Rate YoY",
            SupportedEvent.INFLATION_MOM: "Inflation Rate MoM",
            SupportedEvent.NFP: "Employment Change",
        },
    ),
    "Austria": CountryEventDefinition(
        country="Austria",
        abbreviation="AT",
        event_names={
            SupportedEvent.GDP: "GDP Growth Rate QoQ Flash",
            SupportedEvent.INFLATION_YOY: "Inflation Rate YoY Final",
            SupportedEvent.PPI: "PPI YoY",
            SupportedEvent.INFLATION_MOM: "Inflation Rate MoM Final",
        },
    ),
    "Canada": CountryEventDefinition(
        country="Canada",
        abbreviation="CA",
        event_names={
            SupportedEvent.CB: "BoC Interest Rate Decision",
            SupportedEvent.GDP: "GDP MoM",
            SupportedEvent.INFLATION_YOY: "Inflation Rate Yoy",
            SupportedEvent.PPI: "PPI YoY",
            SupportedEvent.INFLATION_MOM: "Inflation Rate MoM",
            SupportedEvent.NFP: "Employment Change",
        },
    ),
    "Euro Area": CountryEventDefinition(
        country="Euro Area",
        abbreviation="EA",
        event_names={
            SupportedEvent.CB: "ECB Interest Rate Decision",
            SupportedEvent.GDP: "GDP Growth Rate QoQ Flash",
            SupportedEvent.INFLATION_YOY: "Inflation Rate YoY Final",
            SupportedEvent.PPI: "PPI YoY",
            SupportedEvent.INFLATION_MOM: "Inflation Rate MoM Final",
            SupportedEvent.NFP: "Employment Change QoQ Prel",
        },
    ),
    "Finland": CountryEventDefinition(
        country="Finland",
        abbreviation="FI",
        event_names={
            SupportedEvent.GDP: "GDP Growth Rate QoQ",
            SupportedEvent.INFLATION_YOY: "Inflation Rate YoY",
            SupportedEvent.PPI: "PPI YoY",
            SupportedEvent.INFLATION_MOM: "Inflation Rate MoM",
        },
    ),
    "France": CountryEventDefinition(
        country="France",
        abbreviation="FR",
        event_names={
            SupportedEvent.GDP: "GDP Growth Rate QoQ Flash",
            SupportedEvent.INFLATION_YOY: "Inflation Rate YoY Final",
            SupportedEvent.PPI: "PPI YoY",
            SupportedEvent.INFLATION_MOM: "Inflation Rate MoM Final",
        },
    ),
    "Germany": CountryEventDefinition(
        country="Germany",
        abbreviation="DE",
        event_names={
            SupportedEvent.GDP: "GDP Growth Rate QoQ Flash",
            SupportedEvent.INFLATION_YOY: "Inflation Rate YoY Final",
            SupportedEvent.PPI: "PPI YoY",
            SupportedEvent.INFLATION_MOM: "Inflation Rate MoM Final",
        },
    ),
    "Ireland": CountryEventDefinition(
        country="Ireland",
        abbreviation="IE",
        event_names={
            SupportedEvent.GDP: "GDP Growth Rate QoQ",
            SupportedEvent.INFLATION_YOY: "Inflation Rate YoY",
            SupportedEvent.INFLATION_MOM: "Inflation Rate MoM",
        },
    ),
    "Italy": CountryEventDefinition(
        country="Italy",
        abbreviation="IT",
        event_names={
            SupportedEvent.INFLATION_YOY: "Inflation Rate YoY Final",
            SupportedEvent.PPI: "PPI YoY",
            SupportedEvent.INFLATION_MOM: "Inflation Rate MoM Final",
        },
    ),
    "Japan": CountryEventDefinition(
        country="Japan",
        abbreviation="JP",
        event_names={
            SupportedEvent.CB: "BoJ Interest Rate Decision",
            SupportedEvent.GDP: "GDP Growth Rate QoQ",
            SupportedEvent.INFLATION_YOY: "Inflation Rate YoY",
            SupportedEvent.PPI: "PPI YoY",
            SupportedEvent.INFLATION_MOM: "Inflation Rate MoM",
        },
    ),
    "New Zealand": CountryEventDefinition(
        country="New Zealand",
        abbreviation="NZ",
        event_names={
            SupportedEvent.CB: "RBNZ Interest Rate Decision",
            SupportedEvent.GDP: "GDP Growth Rate QoQ",
            SupportedEvent.INFLATION_YOY: "Inflation Rate YoY",
            SupportedEvent.NFP: "Employment Change QoQ",
        },
    ),
    "Norway": CountryEventDefinition(
        country="Norway",
        abbreviation="NO",
        event_names={
            SupportedEvent.CB: "Norges Bank Interest Rate Decision",
            SupportedEvent.GDP: "GDP Growth Mainland QoQ",
            SupportedEvent.INFLATION_YOY: "Inflation Rate YoY",
            SupportedEvent.PPI: "PPI YoY",
            SupportedEvent.INFLATION_MOM: "Inflation Rate MoM",
        },
    ),
    "Portugal": CountryEventDefinition(
        country="Portugal",
        abbreviation="PT",
        event_names={
            SupportedEvent.GDP: "GDP Growth Rate QoQ Flash",
            SupportedEvent.INFLATION_YOY: "Inflation Rate YoY Final",
            SupportedEvent.PPI: "PPI YoY",
            SupportedEvent.INFLATION_MOM: "Inflation Rate MoM Final",
        },
    ),
    "Spain": CountryEventDefinition(
        country="Spain",
        abbreviation="ES",
        event_names={
            SupportedEvent.GDP: "GDP Growth Rate QoQ Flash",
            SupportedEvent.INFLATION_YOY: "Inflation Rate YoY Final",
            SupportedEvent.PPI: "PPI YoY",
            SupportedEvent.INFLATION_MOM: "Inflation Rate MoM Final",
        },
    ),
    "Sweden": CountryEventDefinition(
        country="Sweden",
        abbreviation="SE",
        event_names={
            SupportedEvent.CB: "Riksbank Rate Decision",
            SupportedEvent.GDP: "GDP Growth Rate QoQ",
            SupportedEvent.INFLATION_YOY: "Inflation Rate YoY Final",
            SupportedEvent.PPI: "PPI YoY",
            SupportedEvent.INFLATION_MOM: "Inflation Rate MoM Final",
        },
    ),
    "Switzerland": CountryEventDefinition(
        country="Switzerland",
        abbreviation="CH",
        event_names={
            SupportedEvent.CB: "SNB Interest Rate Decision",
            SupportedEvent.GDP: "GDP Growth Rate QoQ",
            SupportedEvent.INFLATION_YOY: "Inflation Rate YoY",
            SupportedEvent.INFLATION_MOM: "Inflation Rate MoM",
        },
    ),
    "United Kingdom": CountryEventDefinition(
        country="United Kingdom",
        abbreviation="UK",
        event_names={
            SupportedEvent.CB: "BoE Interest Rate Decision",
            SupportedEvent.GDP: "GDP Growth Rate QoQ Prel",
            SupportedEvent.INFLATION_YOY: "Inflation Rate YoY",
            SupportedEvent.PPI: "PPI Output YoY",
            SupportedEvent.INFLATION_MOM: "Inflation Rate MoM",
            SupportedEvent.NFP: "Non Farm Payrolls QoQ",
        },
    ),
    "United States": CountryEventDefinition(
        country="United States",
        abbreviation="US",
        event_names={
            SupportedEvent.CB: "Fed Interest Rate Decision",
            SupportedEvent.GDP: "GDP Growth Rate QoQ Adv",
            SupportedEvent.INFLATION_YOY: "Inflation Rate YoY",
            SupportedEvent.PPI: "PPI YoY",
            SupportedEvent.INFLATION_MOM: "Inflation Rate MoM",
            SupportedEvent.NFP: "Non Farm Payrolls",
        },
    ),
}


def canonicalize_lookup_text(value: str) -> str:
    """Canonicalize lookup text for country and event names.

    :param value: Raw lookup string.
    :return: Uppercase normalized lookup key.
    :raises AttributeError: If value is not string-like.
    """
    return ' '.join(value.strip().upper().replace('-', ' ').replace('_', ' ').split())


def normalize_country(country: str) -> CountryEventDefinition:
    """Validate and normalize a country identifier.

    :param country: Raw country string supplied by the caller.
    :return: Normalized CountryEventDefinition.
    :raises MqValueError: If the value is empty or unsupported.
    """
    if not isinstance(country, str) or not country.strip():
        raise MqValueError('country must be a non-empty string')

    normalized = COUNTRY_LOOKUP.get(canonicalize_lookup_text(country))
    if normalized is None:
        supported_countries = ', '.join(sorted(COUNTRY_EVENT_DEFINITIONS))
        raise MqValueError(f'country must be one of {supported_countries}')

    return normalized


def normalize_event(event: EventInput) -> EventType:
    """Validate and normalize an event identifier.

    :param event: Raw event string or supported enum value supplied by the caller.
    :return: Normalized EventType or subclass.
    :raises MqValueError: If the value is empty or unsupported.
    """
    if isinstance(event, SupportedEvent):
        return EVENT_TYPES[event]

    if not isinstance(event, str) or not event.strip():
        raise MqValueError(f"event must be one of {', '.join(event_name.value for event_name in EVENT_TYPES)}")

    normalized_name = EVENT_LOOKUP.get(canonicalize_lookup_text(event))
    if normalized_name is None:
        raise MqValueError(f"event must be one of {', '.join(event_name.value for event_name in EVENT_TYPES)}")

    return EVENT_TYPES[normalized_name]


def resolve_country_event_definition(country: str, event: EventInput) -> ResolvedEventDefinition:
    """Resolve a country-scoped event into dataset query metadata.

    :param country: Raw country string.
    :param event: Raw event string.
    :return: ResolvedEventDefinition with query and output metadata.
    :raises MqValueError: If the country, event, or pair is unsupported.
    """
    country_definition = normalize_country(country)
    event_definition = normalize_event(event)
    if not isinstance(event_definition, CountryEventType):
        raise MqValueError(f'event {event_definition.name} is asset-scoped and does not accept a country')
    event_name = country_definition.get_event_name(event_definition.name)

    if event_name is None:
        supported_events = ', '.join(
            supported_event.value
            for supported_event in EVENT_TYPES
            if country_definition.supports_event(supported_event)
        )
        raise MqValueError(f'event must be one of {supported_events} for country {country_definition.country}')

    return ResolvedEventDefinition(
        country=country_definition.country,
        event=event_definition.name,
        event_name=event_name,
        event_type=event_definition.output_type(country_definition),
    )


def resolve_asset_event_definition(event: EventInput) -> ResolvedEventDefinition:
    """Resolve an asset-scoped event into dataset query metadata.

    :param event: Raw asset-scoped event string or SupportedEvent enum.
    :return: ResolvedEventDefinition with query and output metadata.
    :raises MqValueError: If the event is unsupported or country-scoped.
    """
    event_definition = normalize_event(event)
    if not isinstance(event_definition, AssetEventType):
        raise MqValueError(f'event {event_definition.name} is country-scoped and requires a country')

    return ResolvedEventDefinition(
        country=None,
        event=event_definition.name,
        event_name=event_definition.event_name,
        event_type=event_definition.output_type(),
    )


COUNTRY_LOOKUP = {canonicalize_lookup_text(country.country): country for country in COUNTRY_EVENT_DEFINITIONS.values()}
EVENT_LOOKUP = {canonicalize_lookup_text(event.value): event for event in EVENT_TYPES}
