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

# Asset-event source adapters.
#
# Purpose
#
#     Own asset-scoped event querying and symbology resolution so source-specific
#     logic such as LSEG earnings access and SecMaster mapping stays separate
#     from generic payload normalization and record-building.

import datetime as dt
from typing import Optional, Union

import pandas as pd

from gs_quant.data import Dataset
from gs_quant.errors import MqValueError
from gs_quant.markets.securities import Asset, AssetIdentifier, SecurityIdentifier, SecurityMaster, SecurityMasterSource

from .event_study_definitions import ResolvedEventDefinition
from .event_study_processing import extract_event_payload, normalize_asset_identifier


ASSET_EVENT_SOURCE = 'LSEG'
EARNINGS_DATASET = 'LSEG_CORPORATE_EVENTS'
EARNINGS_EVENT_NAME = 'Earnings Release'


def _extract_identifier_from_asset(ticker: Union[Asset, str], identifier_name: str) -> Optional[str]:
    """Best-effort extraction of an identifier already present on an asset object.

    :param ticker: Asset-like object or raw string.
    :param identifier_name: Identifier key such as ``sedol`` or ``assetId``.
    :return: Identifier value when locally available, else None.
    """
    if ticker is None or isinstance(ticker, str):
        return None

    entity = getattr(ticker, 'entity', None)
    if not isinstance(entity, dict):
        get_entity = getattr(ticker, 'get_entity', None)
        if callable(get_entity):
            entity = get_entity()

    identifiers = entity.get('identifiers') if isinstance(entity, dict) else None
    if not isinstance(identifiers, dict):
        return None

    expected_key = identifier_name.casefold()
    for key, value in identifiers.items():
        if isinstance(key, str) and key.casefold() == expected_key and value:
            return str(value).strip()

    return None


def _resolve_bbid_from_asset(ticker: Union[Asset, str], as_of_date: dt.date) -> Optional[str]:
    """Best-effort lookup of BBID from an already-resolved asset object.

    :param ticker: Asset-like object or raw string.
    :param as_of_date: As-of date for temporal identifiers.
    :return: BBID when available, else None.
    """
    local_bbid = _extract_identifier_from_asset(ticker, SecurityIdentifier.BBID.value)
    if local_bbid:
        return local_bbid

    if ticker is None or isinstance(ticker, str):
        return None

    get_identifier = getattr(ticker, 'get_identifier', None)
    if not callable(get_identifier):
        return None

    try:
        resolved_bbid = get_identifier(AssetIdentifier.BLOOMBERG_ID, as_of=as_of_date)
    except TypeError:
        try:
            resolved_bbid = get_identifier(AssetIdentifier.BLOOMBERG_ID)
        except Exception:
            return None
    except Exception:
        return None

    if isinstance(resolved_bbid, str) and resolved_bbid.strip():
        return resolved_bbid.strip()

    return None


def query_event_payload_with_asset(
    definition: ResolvedEventDefinition,
    start_time: pd.Timestamp,
    end_time: pd.Timestamp,
    ticker: Union[Asset, str],
) -> pd.DataFrame:
    """Dispatch an asset-scoped payload request to the supported source.

    :param definition: Resolved event metadata.
    :param start_time: Query start.
    :param end_time: Query end.
    :param ticker: Asset identifier used by asset-scoped event definitions.
    :return: Normalized payload DataFrame.
    :raises NotImplementedError: Raised for asset-scoped events whose data source
                                 has not yet been implemented.
    """
    if definition.event == 'EARNINGS':
        return query_earnings_payload(definition, start_time, end_time, ticker)

    _ = definition, start_time, end_time, ticker
    raise NotImplementedError(
        'Asset-scoped event loading is not implemented for the macro event calendar yet. '
        'Implement a non-macro source for asset-scoped events such as earnings or rebalance.'
    )


def query_earnings_payload(
    definition: ResolvedEventDefinition,
    start_time: pd.Timestamp,
    end_time: pd.Timestamp,
    ticker: Union[Asset, str],
) -> pd.DataFrame:
    """Query the LSEG corporate-events dataset for ticker-scoped earnings events.

    :param definition: Resolved event metadata.
    :param start_time: Query start.
    :param end_time: Query end.
    :param ticker: Bloomberg identifier string or gs_quant Asset used for SecMaster mapping.
    :return: Normalized payload DataFrame.
    :raises MqValueError: If the ticker cannot be mapped to a SEDOL identifier.
    :raises Exception: Propagates SecMaster, Dataset.get_data, and pandas parsing errors.
    """
    normalized_ticker = normalize_asset_identifier(ticker)
    if not normalized_ticker:
        raise ValueError('ticker must be a non-empty string')

    sedol = resolve_sedol_for_bbid(ticker, end_time.date())

    dataset = Dataset(EARNINGS_DATASET)
    raw_events = dataset.get_data(
        startDate=start_time.date(),
        endDate=end_time.date(),
        sedol=[sedol],
        eventType=[EARNINGS_EVENT_NAME],
        limit=500,
    )
    payload = raw_events
    if 'eventDate' in payload.columns and not isinstance(payload.index, pd.DatetimeIndex):
        payload = payload.set_index('eventDate')

    payload = extract_event_payload(payload)
    if payload.empty:
        return payload

    payload['country'] = definition.country
    payload['eventName'] = payload.get('eventName', EARNINGS_EVENT_NAME)
    payload['source'] = payload['eventSource'] if 'eventSource' in payload.columns else ASSET_EVENT_SOURCE
    payload['sourceId'] = payload['lsegEventId'] if 'lsegEventId' in payload.columns else pd.NA
    payload['id'] = payload['lsegEventId'] if 'lsegEventId' in payload.columns else pd.NA
    payload['sourceTicker'] = normalized_ticker
    payload['sourceSymbol'] = normalized_ticker
    payload['sedol'] = payload['sedol'] if 'sedol' in payload.columns else sedol
    return payload


def resolve_sedol_for_bbid(ticker: Union[Asset, str], as_of_date: dt.date) -> str:
    """Resolve a BBID string or gs_quant Asset to the corresponding SEDOL.

    :param ticker: Bloomberg identifier / BBID string, or gs_quant Asset object.
    :param as_of_date: As-of date used for SecMaster mapping.
    :return: Resolved SEDOL string.
    :raises MqValueError: If no SEDOL can be resolved for the ticker.
    """
    normalized_ticker = normalize_asset_identifier(ticker)
    if not normalized_ticker:
        raise MqValueError("unable to resolve SEDOL for ticker 'None'")

    local_sedol = _extract_identifier_from_asset(ticker, SecurityIdentifier.SEDOL.value)
    if local_sedol:
        return local_sedol

    mapping_identifier = normalized_ticker
    input_type = SecurityIdentifier.BBID if isinstance(ticker, str) else SecurityIdentifier.ASSET_ID

    local_bbid = _resolve_bbid_from_asset(ticker, as_of_date)
    if local_bbid:
        mapping_identifier = local_bbid
        input_type = SecurityIdentifier.BBID

    SecurityMaster.set_source(SecurityMasterSource.ASSET_SERVICE)
    result = SecurityMaster.map_identifiers(
        input_type,
        [mapping_identifier],
        [SecurityIdentifier.SEDOL],
        as_of_date=as_of_date,
    )
    daily_mapping = next(iter(result.values()), {}) if result else {}
    identifier_map = daily_mapping.get(mapping_identifier, {})
    sedol_values = identifier_map.get(SecurityIdentifier.SEDOL.value, [])
    if not sedol_values:
        raise MqValueError(f"unable to resolve SEDOL for ticker '{normalized_ticker}'")
    return sedol_values[0]
