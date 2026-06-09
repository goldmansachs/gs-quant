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

import importlib
from types import SimpleNamespace
from unittest import mock

import pandas as pd
import pytest
import gs_quant.timeseries.event_study as event_study_module
import gs_quant.timeseries._event_study.event_study_labels as event_study_labels_module

from gs_quant.errors import MqValueError
from gs_quant.timeseries._event_study.event_study_api import get_event_dates_internal
from gs_quant.timeseries._event_study.event_study_definitions import (
    AssetEventType,
    EventRecord,
    EventType,
    ResolvedEventDefinition,
    SupportedEvent,
    WindowType,
    resolve_country_event_definition,
    normalize_country,
    normalize_event,
)
from gs_quant.timeseries._event_study.event_study_impact import (
    CalendarAlignment,
    EventDirection,
    EventMetric,
    _extract_series_asset_identifier,
    _compute_metric,
    _event_mask,
    _map_event_dates_to_series,
    _resolve_series_event_label,
    build_event_impact_frame,
)
from gs_quant.timeseries._event_study.event_study_processing import (
    EVENT_DATE_COLUMN,
    align_event_date_to_index,
    build_event_records,
    build_macro_event_payload_dict,
    extract_event_payload,
    normalize_asset_identifier,
    normalize_series,
    resolve_event_location,
    to_float_or_none,
)
from gs_quant.timeseries._event_study.event_study_asset_source import (
    _extract_identifier_from_asset,
    _resolve_bbid_from_asset,
    query_event_payload_with_asset,
    query_earnings_payload,
    resolve_sedol_for_bbid,
)
from gs_quant.timeseries._event_study.event_study_frame import (
    apply_window_filter,
    build_event_study_frame,
    get_event_window,
    resolve_nearest_date,
    sorted_unique_dates,
    to_calendar_date,
)
from gs_quant.timeseries._event_study.event_study_query import (
    _apply_relative_offset,
    load_real_event_dates,
    parse_date_param,
    resolve_query_event,
    validate_date_range,
    validate_ticker_requirement,
)
from gs_quant.timeseries.event_study import (
    AssetEvents,
    CountryEvents,
    event_impact_analysis,
    frame_timeseries_around_events,
    get_asset_events,
    get_country_events,
)
from gs_quant.timeseries.helper import Returns


def test_events_get_data_returns_event_objects():
    """Description: load one macro event into the reusable CountryEvents object model.

    Purpose: verify country/event normalization and EventRecord payload shaping.
    Expectation: get_data returns one EventRecord with normalized metadata and numeric payload values.
    """
    raw_events = pd.DataFrame(
        {
            'valueActual': ['1.50'],
            'valuePrevious': ['1.25'],
            'valueForecast': ['1.40'],
            'source': ['TradingEconomics'],
            'country': ['United States'],
            'eventName': ['Fed Interest Rate Decision'],
            'id': ['a'],
        },
        index=pd.to_datetime(['2024-01-03']),
    )

    with mock.patch('gs_quant.timeseries._event_study.event_study_macro_source.Dataset') as mock_dataset:
        mock_dataset.return_value.get_data.return_value = raw_events

        events = CountryEvents('united states', 'cb')
        loaded_events = events.get_data(pd.Timestamp('2024-01-01'), pd.Timestamp('2024-01-31'))

    assert events.country == 'United States'
    assert events.event == 'CB'
    assert events.event_name == 'Fed Interest Rate Decision'
    assert events.event_type == 'CB_MEETING_US'
    assert len(loaded_events) == 1
    assert loaded_events[0].event_date == pd.Timestamp('2024-01-03')
    assert loaded_events[0].type_of_event == 'CB_MEETING_US'
    assert loaded_events[0].payload['valueActual'] == 1.5
    assert loaded_events[0].payload['valuePrevious'] == 1.25
    assert loaded_events[0].payload['valueForecast'] == 1.4


def test_events_get_data_supports_gdp_canonical_name():
    """Description: load a GDP event via the canonical public event name.

    Purpose: verify gs_quant resolves GDP directly through the per-country static mapping.
    Expectation: the resulting CountryEvents object normalizes to GDP and emits the GDP_CA output label.
    """
    raw_events = pd.DataFrame(
        {
            'valueActual': ['0.2'],
            'source': ['TradingEconomics'],
            'country': ['Canada'],
            'eventName': ['GDP MoM'],
            'id': ['gdp-ca'],
        },
        index=pd.to_datetime(['2024-01-31']),
    )

    with mock.patch('gs_quant.timeseries._event_study.event_study_macro_source.Dataset') as mock_dataset:
        mock_dataset.return_value.get_data.return_value = raw_events

        events = CountryEvents('Canada', 'GDP')
        loaded_events = events.get_data(pd.Timestamp('2024-01-01'), pd.Timestamp('2024-02-29'))

    assert events.country == 'Canada'
    assert events.event == 'GDP'
    assert events.event_name == 'GDP MoM'
    assert events.event_type == 'GDP_CA'
    assert len(loaded_events) == 1
    assert loaded_events[0].event_date == pd.Timestamp('2024-01-31')
    assert loaded_events[0].type_of_event == 'GDP_CA'


def test_events_get_data_supports_nfp_canonical_name():
    """Description: load a payroll event via the canonical public event name.

    Purpose: verify gs_quant resolves NFP directly through the per-country static mapping.
    Expectation: the resulting CountryEvents object normalizes to NFP and emits the NFP_US output label.
    """
    raw_events = pd.DataFrame(
        {
            'valueActual': ['275'],
            'source': ['TradingEconomics'],
            'country': ['United States'],
            'eventName': ['Non Farm Payrolls'],
            'id': ['nfp-us'],
        },
        index=pd.to_datetime(['2024-03-08']),
    )

    with mock.patch('gs_quant.timeseries._event_study.event_study_macro_source.Dataset') as mock_dataset:
        mock_dataset.return_value.get_data.return_value = raw_events

        events = CountryEvents('United States', 'NFP')
        loaded_events = events.get_data(pd.Timestamp('2024-03-01'), pd.Timestamp('2024-03-31'))

    assert events.country == 'United States'
    assert events.event == 'NFP'
    assert events.event_name == 'Non Farm Payrolls'
    assert events.event_type == 'NFP_US'
    assert len(loaded_events) == 1
    assert loaded_events[0].event_date == pd.Timestamp('2024-03-08')
    assert loaded_events[0].type_of_event == 'NFP_US'


def test_asset_events_event_type_for_asset_rejects_empty_identifier():
    """Description: build an asset-scoped event label without a usable asset identifier.

    Purpose: cover the explicit validation guard for ticker-scoped output labels.
    Expectation: AssetEvents.event_type_for_asset raises ValueError for blank identifiers.
    """
    with pytest.raises(ValueError, match='ticker must be a non-empty string'):
        AssetEvents('EARNINGS').event_type_for_asset('   ')


def test_events_get_data_normalizes_tz_aware_event_dates_to_tz_naive():
    """Description: load a macro event whose dataset timestamp is tz-aware.

    Purpose: ensure gs_quant emits tz-naive calendar-date EventRecord values for downstream comparisons.
    Expectation: get_data returns an EventRecord whose event_date is normalized to a tz-naive midnight timestamp.
    """
    raw_events = pd.DataFrame(
        {
            'valueActual': ['1.50'],
            'source': ['TradingEconomics'],
            'country': ['United States'],
            'eventName': ['Fed Interest Rate Decision'],
            'id': ['a'],
        },
        index=pd.to_datetime(['2024-01-03T19:00:00Z'], utc=True),
    )

    with mock.patch('gs_quant.timeseries._event_study.event_study_macro_source.Dataset') as mock_dataset:
        mock_dataset.return_value.get_data.return_value = raw_events

        events = CountryEvents('United States', 'CB')
        loaded_events = events.get_data(pd.Timestamp('2024-01-01'), pd.Timestamp('2024-01-31'))

    assert len(loaded_events) == 1
    assert loaded_events[0].event_date == pd.Timestamp('2024-01-03')
    assert loaded_events[0].event_date.tzinfo is None


def test_events_get_data_requeries_same_window_and_returns_fresh_results():
    """Description: call get_data twice on the same CountryEvents instance and query window.

    Purpose: verify CountryEvents no longer keeps an object-level cache over dataset-backed loads.
    Expectation: Dataset.get_data is called twice and the second result is unaffected by caller mutation of the first list.
    """
    raw_events = pd.DataFrame(
        {
            'event_date': pd.to_datetime(['2024-01-03']),
            'valueActual': ['1.50'],
            'source': ['TradingEconomics'],
            'country': ['United States'],
            'eventName': ['Fed Interest Rate Decision'],
            'id': ['a'],
        },
        index=pd.to_datetime(['2024-01-03']),
    )

    with mock.patch('gs_quant.timeseries._event_study.event_study_macro_source.Dataset') as mock_dataset:
        mock_dataset.return_value.get_data.return_value = raw_events

        events = CountryEvents('United States', 'CB')
        first = events.get_data(pd.Timestamp('2024-01-01'), pd.Timestamp('2024-01-31'))
        first.append(first[0])
        second = events.get_data(pd.Timestamp('2024-01-01'), pd.Timestamp('2024-01-31'))

    assert mock_dataset.return_value.get_data.call_count == 2
    assert len(first) == 2
    assert len(second) == 1
    assert second[0].event_date == pd.Timestamp('2024-01-03')


def test_events_get_data_requeries_across_instances_for_same_window():
    """Description: load the same country/event window through two separate CountryEvents instances.

    Purpose: verify equivalent CountryEvents instances do not share an event-study layer cache.
    Expectation: Dataset.get_data is called once per instance and both results still normalize identically.
    """
    raw_events = pd.DataFrame(
        {
            'event_date': pd.to_datetime(['2024-01-03']),
            'valueActual': ['1.50'],
            'source': ['TradingEconomics'],
            'country': ['United States'],
            'eventName': ['Fed Interest Rate Decision'],
            'id': ['a'],
        },
        index=pd.to_datetime(['2024-01-03']),
    )

    with mock.patch('gs_quant.timeseries._event_study.event_study_macro_source.Dataset') as mock_dataset:
        mock_dataset.return_value.get_data.return_value = raw_events

        first_events = CountryEvents('United States', 'CB')
        second_events = CountryEvents('united states', 'cb')
        first = first_events.get_data(pd.Timestamp('2024-01-01'), pd.Timestamp('2024-01-31'))
        second = second_events.get_data(pd.Timestamp('2024-01-01'), pd.Timestamp('2024-01-31'))

    assert mock_dataset.return_value.get_data.call_count == 2
    assert len(first) == 1
    assert len(second) == 1
    assert second[0].event_date == pd.Timestamp('2024-01-03')


def test_asset_events_reject_country_scoped_event_names():
    """Description: construct the asset-scoped loader with a country-scoped event.

    Purpose: keep the runtime split explicit so asset loaders cannot be used for macro events.
    Expectation: AssetEvents raises MqValueError for country-scoped event names.
    """
    with pytest.raises(MqValueError, match='event CB is country-scoped and requires a country'):
        AssetEvents('CB')


def test_resolve_country_event_definition_rejects_asset_scoped_event_names():
    """Description: resolve a country-scoped definition using an asset-scoped event.

    Purpose: cover the branch that rejects asset-scoped events on the country resolver.
    Expectation: resolve_country_event_definition raises MqValueError for EARNINGS.
    """
    with pytest.raises(MqValueError, match='event EARNINGS is asset-scoped and does not accept a country'):
        resolve_country_event_definition('United States', 'EARNINGS')


def test_asset_events_get_data_requires_non_empty_ticker():
    """Description: call the asset-scoped loader without a usable ticker.

    Purpose: keep the new upstream loader strict about the asset identifier.
    Expectation: an empty ticker raises ValueError before any downstream query.
    """
    events = AssetEvents('EARNINGS')

    with pytest.raises(ValueError, match='ticker must be a non-empty string'):
        events.get_data(pd.Timestamp('2024-01-01'), pd.Timestamp('2024-01-31'), ticker='')


def test_asset_events_get_data_requeries_across_instances():
    """Description: load the same asset-scoped event window through two AssetEvents instances.

    Purpose: verify asset-scoped event loads no longer share an event-study layer cache.
    Expectation: the asset query helper is called once per instance and both results normalize identically.
    """
    payload = pd.DataFrame({'event_date': pd.to_datetime(['2024-01-03'])})

    with mock.patch(
        'gs_quant.timeseries._event_study.event_study_objects.query_event_payload_with_asset',
        return_value=payload,
    ) as mock_query:
        first_events = AssetEvents('EARNINGS')
        second_events = AssetEvents('EARNINGS')

        first = first_events.get_data(pd.Timestamp('2024-01-01'), pd.Timestamp('2024-01-31'), 'SPX')
        second = second_events.get_data(pd.Timestamp('2024-01-01'), pd.Timestamp('2024-01-31'), 'SPX')

    assert mock_query.call_count == 2
    assert len(first) == 1
    assert len(second) == 1
    assert second[0].event_date == pd.Timestamp('2024-01-03')


def test_asset_events_get_data_requeries_same_window_and_returns_fresh_results():
    """Description: load the same asset-scoped event window twice on one AssetEvents instance.

    Purpose: verify asset-scoped event loads no longer cache results on the AssetEvents object.
    Expectation: the asset query helper is called twice and the second result is unaffected by caller mutation of the first list.
    """
    payload = pd.DataFrame({'event_date': pd.to_datetime(['2024-01-03'])})

    with mock.patch(
        'gs_quant.timeseries._event_study.event_study_objects.query_event_payload_with_asset',
        return_value=payload,
    ) as mock_query:
        events = AssetEvents('EARNINGS')

        first = events.get_data(pd.Timestamp('2024-01-01'), pd.Timestamp('2024-01-31'), 'SPX')
        first.append(first[0])
        second = events.get_data(pd.Timestamp('2024-01-01'), pd.Timestamp('2024-01-31'), 'SPX')

    assert mock_query.call_count == 2
    assert len(first) == 2
    assert len(second) == 1
    assert second[0].event_date == pd.Timestamp('2024-01-03')


def test_asset_events_get_data_supports_earnings_via_lseg_and_secmaster():
    """Description: load ticker-scoped earnings events through the LSEG corporate-events dataset.

    Purpose: verify the asset-scoped loader maps BBID to SEDOL and normalizes LSEG earnings rows into EventRecord objects.
    Expectation: AssetEvents.get_data returns earnings EventRecord values with event dates sourced from LSEG eventDate.
    """
    raw_events = pd.DataFrame(
        {
            'eventDate': ['2024-04-25', '2024-07-25'],
            'eventName': ['Q1 2024 Earnings Release', 'Q2 2024 Earnings Release'],
            'eventSource': ['CLIENT', 'CLIENT'],
            'lsegEventId': ['evt-1', 'evt-2'],
            'sedol': ['2046251', '2046251'],
        }
    )

    with mock.patch('gs_quant.timeseries._event_study.event_study_asset_source.SecurityMaster.set_source'):
        with mock.patch(
            'gs_quant.timeseries._event_study.event_study_asset_source.SecurityMaster.map_identifiers',
            return_value={'2024-07-25': {'AAPL UW': {'sedol': ['2046251']}}},
        ) as mock_map:
            with mock.patch('gs_quant.timeseries._event_study.event_study_asset_source.Dataset') as mock_dataset:
                mock_dataset.return_value.get_data.return_value = raw_events

                events = AssetEvents('EARNINGS')
                loaded_events = events.get_data(
                    pd.Timestamp('2024-01-01'),
                    pd.Timestamp('2024-12-31'),
                    ticker='AAPL UW',
                )

    assert events.event == 'EARNINGS'
    assert events.event_name == 'Earnings Release'
    assert events.event_type == 'EARNINGS'
    assert events.event_type_for_asset('AAPL UW') == 'EARNINGS_AAPL UW'
    assert not hasattr(events, 'country')
    assert mock_map.call_args.args[0].value == 'bbid'
    assert mock_map.call_args.args[1] == ['AAPL UW']
    assert [identifier.value for identifier in mock_map.call_args.args[2]] == ['sedol']
    assert mock_dataset.call_args.args == ('LSEG_CORPORATE_EVENTS',)
    dataset_kwargs = mock_dataset.return_value.get_data.call_args.kwargs
    assert dataset_kwargs['sedol'] == ['2046251']
    assert dataset_kwargs['eventType'] == ['Earnings Release']
    assert len(loaded_events) == 2
    assert loaded_events[0].event_date == pd.Timestamp('2024-04-25')
    assert loaded_events[0].type_of_event == 'EARNINGS_AAPL UW'
    assert loaded_events[0].payload['source'] == 'CLIENT'
    assert loaded_events[0].payload['sourceTicker'] == 'AAPL UW'
    assert loaded_events[0].payload['id'] == 'evt-1'


def test_asset_events_get_data_earnings_returns_empty_when_lseg_has_no_rows():
    """Description: query earnings events for a ticker when the LSEG dataset returns no rows.

    Purpose: verify the asset-scoped earnings loader returns an empty EventRecord list for empty LSEG results.
    Expectation: AssetEvents.get_data returns an empty list instead of failing when no earnings rows exist in range.
    """
    with mock.patch('gs_quant.timeseries._event_study.event_study_asset_source.SecurityMaster.set_source'):
        with mock.patch(
            'gs_quant.timeseries._event_study.event_study_asset_source.SecurityMaster.map_identifiers',
            return_value={'2024-07-25': {'AAPL UW': {'sedol': ['2046251']}}},
        ):
            with mock.patch('gs_quant.timeseries._event_study.event_study_asset_source.Dataset') as mock_dataset:
                mock_dataset.return_value.get_data.return_value = pd.DataFrame()

                events = AssetEvents('EARNINGS')
                loaded_events = events.get_data(
                    pd.Timestamp('2024-01-01'),
                    pd.Timestamp('2024-12-31'),
                    ticker='AAPL UW',
                )

    assert loaded_events == []


def test_resolve_sedol_for_bbid_raises_when_mapping_is_missing():
    """Description: resolve a ticker to SEDOL when SecMaster has no identifier mapping.

    Purpose: keep missing symbology failures explicit before the LSEG dataset is queried.
    Expectation: resolve_sedol_for_bbid raises MqValueError with the missing-ticker message.
    """
    with mock.patch('gs_quant.timeseries._event_study.event_study_asset_source.SecurityMaster.set_source'):
        with mock.patch(
            'gs_quant.timeseries._event_study.event_study_asset_source.SecurityMaster.map_identifiers',
            return_value={'2024-07-25': {'AAPL UW': {}}},
        ):
            with pytest.raises(MqValueError, match="unable to resolve SEDOL for ticker 'AAPL UW'"):
                resolve_sedol_for_bbid('AAPL UW', pd.Timestamp('2024-07-25').date())


def test_normalize_asset_identifier_rejects_non_string_non_asset_inputs():
    """Description: normalize an invalid asset identifier object.

    Purpose: cover the explicit guard for identifiers that are neither strings nor Asset-like objects with a string marquee id.
    Expectation: normalize_asset_identifier raises ValueError with the documented message.
    """
    with pytest.raises(ValueError, match='ticker must be a non-empty string'):
        normalize_asset_identifier(object())


def test_query_earnings_payload_and_resolve_sedol_reject_blank_tickers_before_downstream_calls():
    """Description: call earnings helpers with blank ticker inputs.

    Purpose: cover the explicit blank-ticker guards before any SecMaster or dataset work is attempted.
    Expectation: query_earnings_payload raises ValueError and resolve_sedol_for_bbid raises MqValueError.
    """
    definition = ResolvedEventDefinition(
        country='Asset',
        event='EARNINGS',
        event_name='Earnings Release',
        event_type='EARNINGS',
    )

    with pytest.raises(ValueError, match='ticker must be a non-empty string'):
        query_earnings_payload(
            definition,
            pd.Timestamp('2024-01-01'),
            pd.Timestamp('2024-12-31'),
            '   ',
        )

    with pytest.raises(MqValueError, match="unable to resolve SEDOL for ticker 'None'"):
        resolve_sedol_for_bbid('   ', pd.Timestamp('2024-07-25').date())


def test_query_event_payload_with_asset_rejects_unimplemented_non_earnings_sources():
    """Description: request an asset-scoped payload for an unimplemented event family.

    Purpose: cover the explicit NotImplementedError branch for non-earnings asset events.
    Expectation: query_event_payload_with_asset raises the documented error.
    """
    definition = ResolvedEventDefinition(
        country=None,
        event='REBALANCE',
        event_name='Rebalance',
        event_type='REBALANCE',
    )

    with pytest.raises(NotImplementedError, match='Asset-scoped event loading is not implemented'):
        query_event_payload_with_asset(
            definition,
            pd.Timestamp('2024-01-01'),
            pd.Timestamp('2024-01-31'),
            'SPX',
        )


def test_asset_events_get_data_accepts_asset_objects_and_uses_marquee_id_for_mapping():
    """Description: load earnings events using a gs_quant Asset object on the asset-scoped loader.

    Purpose: support the live plot-service path while keeping the existing string-based API behavior intact.
    Expectation: the loader converts the Asset to marquee id and uses that id for SEDOL mapping and output payload labels.
    """
    raw_events = pd.DataFrame(
        {
            'eventDate': ['2024-04-25'],
            'eventName': ['Q1 2024 Earnings Release'],
            'eventSource': ['CLIENT'],
            'lsegEventId': ['evt-1'],
            'sedol': ['2046251'],
        }
    )
    asset = mock.Mock()
    asset.get_marquee_id.return_value = 'MA4B66MW5E27UAHKG34'
    asset.get_entity.return_value = {
        'identifiers': {
            'bbid': 'AAPL UW',
            'assetId': 'MA4B66MW5E27UAHKG34',
        }
    }

    with mock.patch('gs_quant.timeseries._event_study.event_study_asset_source.SecurityMaster.set_source'):
        with mock.patch(
            'gs_quant.timeseries._event_study.event_study_asset_source.SecurityMaster.map_identifiers',
            return_value={'2024-07-25': {'AAPL UW': {'sedol': ['2046251']}}},
        ) as mock_map:
            with mock.patch('gs_quant.timeseries._event_study.event_study_asset_source.Dataset') as mock_dataset:
                mock_dataset.return_value.get_data.return_value = raw_events

                events = AssetEvents('EARNINGS')
                loaded_events = events.get_data(
                    pd.Timestamp('2024-01-01'),
                    pd.Timestamp('2024-12-31'),
                    ticker=asset,
                )

    assert mock_map.call_args.args[0].value == 'bbid'
    assert mock_map.call_args.args[1] == ['AAPL UW']
    assert loaded_events[0].type_of_event == 'EARNINGS_MA4B66MW5E27UAHKG34'
    assert loaded_events[0].payload['sourceTicker'] == 'MA4B66MW5E27UAHKG34'


def test_resolve_sedol_for_bbid_uses_asset_local_identifiers_before_mapping():
    """Description: resolve SEDOL directly from identifiers already present on an asset object.

    Purpose: avoid unnecessary downstream symbology service calls when the resolved asset already carries a SEDOL.
    Expectation: resolve_sedol_for_bbid returns the local SEDOL and does not call map_identifiers.
    """
    asset = mock.Mock()
    asset.get_marquee_id.return_value = 'MA4B66MW5E27UAHKG34'
    asset.get_entity.return_value = {
        'identifiers': {
            'assetId': 'MA4B66MW5E27UAHKG34',
            'sedol': '2046251',
        }
    }

    with mock.patch(
        'gs_quant.timeseries._event_study.event_study_asset_source.SecurityMaster.map_identifiers'
    ) as mock_map:
        result = resolve_sedol_for_bbid(asset, pd.Timestamp('2024-07-25').date())

    assert result == '2046251'
    mock_map.assert_not_called()


def test_resolve_sedol_for_bbid_uses_asset_get_identifier_to_find_bbid_before_mapping():
    """Description: resolve SEDOL by asking the asset object for BBID when it is not embedded locally.

    Purpose: support plot-service asset objects that expose BBID through get_identifier() rather than entity.identifiers.
    Expectation: resolve_sedol_for_bbid maps from BBID and avoids the unsupported assetId historical path.
    """
    asset = mock.Mock()
    asset.get_marquee_id.return_value = 'MA4B66MW5E27UAHKG34'
    asset.get_entity.return_value = {'identifiers': {'assetId': 'MA4B66MW5E27UAHKG34'}}
    asset.get_identifier.return_value = 'MSFT UW'

    with mock.patch('gs_quant.timeseries._event_study.event_study_asset_source.SecurityMaster.set_source'):
        with mock.patch(
            'gs_quant.timeseries._event_study.event_study_asset_source.SecurityMaster.map_identifiers',
            return_value={'2024-07-25': {'MSFT UW': {'sedol': ['2588173']}}},
        ) as mock_map:
            result = resolve_sedol_for_bbid(asset, pd.Timestamp('2024-07-25').date())

    assert result == '2588173'
    assert mock_map.call_args.args[0].value == 'bbid'
    assert mock_map.call_args.args[1] == ['MSFT UW']


def test_extract_identifier_and_resolve_bbid_cover_defensive_asset_helper_paths():
    """Description: exercise local identifier helper fallbacks directly.

    Purpose: cover malformed identifier payloads plus BBID helper branches for missing, raising, and blank get_identifier results.
    Expectation: helper fallbacks return None rather than raising when an asset-like object lacks a usable local identifier path.
    """
    asset_with_bad_identifiers = mock.Mock()
    asset_with_bad_identifiers.entity = {'identifiers': None}

    assert _extract_identifier_from_asset(asset_with_bad_identifiers, 'sedol') is None

    asset_without_callable = mock.Mock()
    asset_without_callable.entity = {'identifiers': {}}
    asset_without_callable.get_identifier = None

    assert _resolve_bbid_from_asset(asset_without_callable, pd.Timestamp('2024-07-25').date()) is None

    asset_type_error_then_exception = mock.Mock()
    asset_type_error_then_exception.entity = {'identifiers': {}}
    asset_type_error_then_exception.get_identifier.side_effect = [TypeError('bad signature'), RuntimeError('boom')]

    assert _resolve_bbid_from_asset(asset_type_error_then_exception, pd.Timestamp('2024-07-25').date()) is None

    asset_exception = mock.Mock()
    asset_exception.entity = {'identifiers': {}}
    asset_exception.get_identifier.side_effect = RuntimeError('boom')

    assert _resolve_bbid_from_asset(asset_exception, pd.Timestamp('2024-07-25').date()) is None

    asset_blank = mock.Mock()
    asset_blank.entity = {'identifiers': {}}
    asset_blank.get_identifier.return_value = '   '

    assert _resolve_bbid_from_asset(asset_blank, pd.Timestamp('2024-07-25').date()) is None


def test_normalize_country_and_event_reject_empty_values():
    """Description: validate empty country and event inputs directly through helper functions.

    Purpose: cover the explicit validation branches in the new definition helpers.
    Expectation: both helpers raise the documented MqValueError messages.
    """
    with pytest.raises(MqValueError, match='country must be a non-empty string'):
        normalize_country(' ')

    with pytest.raises(MqValueError, match='event must be one of'):
        normalize_event(' ')


def test_normalize_country_and_event_reject_unknown_non_empty_values():
    """Description: validate unsupported non-empty country and event identifiers.

    Purpose: cover the unknown-value validation branches in the definition helpers.
    Expectation: unsupported country and event strings raise the documented MqValueError messages.
    """
    with pytest.raises(MqValueError, match='country must be one of'):
        normalize_country('Atlantis')

    with pytest.raises(MqValueError, match='event must be one of'):
        normalize_event('UNKNOWN_EVENT')


def test_normalize_country_uses_gs_quant_country_model_and_event_enum():
    """Description: inspect the normalized built-in country and event definitions.

    Purpose: keep the event-study registry aligned with gs_quant Country objects and enum-backed event definitions.
    Expectation: normalize_country exposes a gs_quant Country model and normalize_event resolves to the supported enum.
    """
    country_definition = normalize_country('United States')
    event_definition = normalize_event('CB')

    assert country_definition.gs_country.name == 'United States'
    assert country_definition.gs_country.xref.alpha2 == 'US'
    assert event_definition.event == SupportedEvent.CB
    assert event_definition.name == 'CB'


def test_normalize_event_accepts_client_string_and_supported_enum():
    """Description: normalize supported events from both client strings and enum values.

    Purpose: keep the public client boundary string-friendly while tightening internal registry typing.
    Expectation: both input forms resolve to the same supported event definition.
    """
    from_string = normalize_event('GDP')
    from_enum = normalize_event(SupportedEvent.GDP)

    assert from_string.event == SupportedEvent.GDP
    assert from_enum.event == SupportedEvent.GDP
    assert from_string.event_type == 'GDP'
    assert from_enum.event_type == 'GDP'


def test_build_event_records_returns_empty_list_for_empty_payload():
    """Description: pass no event rows into the EventRecord builder.

    Purpose: verify the empty-payload branch returns a stable empty list.
    Expectation: build_event_records returns an empty list.
    """
    definition = CountryEvents('United States', 'CB').definition
    records = build_event_records(definition, pd.DataFrame())

    assert records == []


def test_event_record_to_dict_returns_shallow_copy_of_payload():
    """Description: serialize one explicit EventRecord.

    Purpose: cover EventRecord.to_dict without keeping removed payload-wrapper helpers alive.
    Expectation: to_dict returns a shallow copy of the stored payload.
    """
    payload = {
        EVENT_DATE_COLUMN: pd.Timestamp('2024-01-03'),
        'source': 'TradingEconomics',
        'valueActual': 1.5,
    }
    definition = ResolvedEventDefinition(
        country='United States',
        event='CB',
        event_name='Fed Interest Rate Decision',
        event_type='CB_MEETING_US',
    )
    record = EventRecord(definition=definition, payload=payload)

    payload_copy = record.to_dict()

    assert payload_copy == payload
    assert payload_copy is not payload


def test_to_float_or_none_and_payload_dict_handle_null_and_non_numeric_values():
    """Description: normalize mixed payload values through the low-level processing helpers.

    Purpose: cover null, non-numeric, and passthrough fields in payload shaping.
    Expectation: null-like and non-numeric numeric fields become None while passthrough fields remain unchanged.
    """
    row = pd.Series(
        {
            EVENT_DATE_COLUMN: pd.Timestamp('2024-01-03'),
            'valueActual': 'not-a-number',
            'valuePrevious': None,
            'valueForecast': pd.NA,
            'sourceValueForecast': 'survey',
            'valueRevised': 'unchanged',
        }
    )

    payload = build_macro_event_payload_dict(row)

    assert to_float_or_none(None) is None
    assert to_float_or_none(pd.NA) is None
    assert to_float_or_none(float('nan')) is None
    assert to_float_or_none('bad-value') is None
    assert payload[EVENT_DATE_COLUMN] == pd.Timestamp('2024-01-03')
    assert payload['valueActual'] is None
    assert payload['valuePrevious'] is None
    assert payload['valueForecast'] is None
    assert payload['sourceValueForecast'] == 'survey'
    assert payload['valueRevised'] == 'unchanged'


def test_normalize_series_rejects_non_series_empty_non_datetime_and_non_numeric_inputs():
    """Description: drive the input-validation branches in normalize_series.

    Purpose: verify the helper rejects unsupported shapes before framing logic runs.
    Expectation: each invalid input raises the documented MqValueError.
    """
    with pytest.raises(MqValueError, match='x must be a pandas Series'):
        normalize_series([1, 2, 3])

    with pytest.raises(MqValueError, match='x must not be empty'):
        normalize_series(pd.Series(dtype=float))

    with pytest.raises(MqValueError, match='x must have a DatetimeIndex'):
        normalize_series(pd.Series([1, 2, 3], index=[0, 1, 2]))

    with pytest.raises(MqValueError, match='x must contain at least one numeric observation'):
        normalize_series(pd.Series(['a', 'b'], index=pd.to_datetime(['2024-01-01', '2024-01-02'])))


def test_extract_event_payload_uses_date_column_and_drops_invalid_rows():
    """Description: normalize a payload with an explicit date column containing one invalid value.

    Purpose: cover the date-column and invalid-row filtering branches in payload extraction.
    Expectation: only valid rows remain and the normalized event_date column is populated.
    """
    raw_events = pd.DataFrame(
        {
            'date': ['2024-01-03', 'not-a-date'],
            'valueActual': ['1.5', '2.0'],
        },
        index=['row-1', 'row-2'],
    )

    payload = extract_event_payload(raw_events)

    assert payload[EVENT_DATE_COLUMN].tolist() == [pd.Timestamp('2024-01-03')]
    assert payload['valueActual'].tolist() == ['1.5']


def test_extract_event_payload_returns_empty_frame_when_all_dates_are_invalid():
    """Description: normalize a payload whose date values are all invalid.

    Purpose: cover the branch where payload normalization filters every row out.
    Expectation: the helper returns an empty DataFrame containing only the event_date column.
    """
    raw_events = pd.DataFrame({'date': ['bad-date']}, index=['row-1'])

    payload = extract_event_payload(raw_events)

    assert payload.empty
    assert payload.columns.tolist() == [EVENT_DATE_COLUMN]


def test_extract_event_payload_parses_string_index_when_no_date_column_exists():
    """Description: normalize a payload whose dates live only in a string index.

    Purpose: cover the fallback payload-index parsing branch in extract_event_payload.
    Expectation: the helper converts the string index into normalized event_date values.
    """
    raw_events = pd.DataFrame({'valueActual': ['1.5']}, index=['2024-01-03'])

    payload = extract_event_payload(raw_events)

    assert payload[EVENT_DATE_COLUMN].tolist() == [pd.Timestamp('2024-01-03')]
    assert payload['valueActual'].tolist() == ['1.5']


def test_align_event_date_to_index_handles_tz_localize_and_convert_paths():
    """Description: align naive and tz-aware event dates against tz-aware and tz-naive indexes.

    Purpose: cover both timezone-adjustment branches in event-date alignment.
    Expectation: the helper localizes naive dates to the index timezone and strips timezone from tz-aware dates for naive indexes.
    """
    tz_aware_index = pd.DatetimeIndex(pd.to_datetime(['2024-01-03 00:00:00'], utc=True))
    tz_naive_index = pd.DatetimeIndex(pd.to_datetime(['2024-01-03']))

    assert align_event_date_to_index(tz_aware_index, pd.Timestamp('2024-01-03')) == pd.Timestamp('2024-01-03', tz='UTC')
    assert align_event_date_to_index(tz_naive_index, pd.Timestamp('2024-01-03 05:00:00', tz='UTC')) == pd.Timestamp(
        '2024-01-03'
    )


def test_align_event_date_to_index_converts_between_different_timezones():
    """Description: align a tz-aware event date to a differently tz-aware series index.

    Purpose: cover the explicit timezone-conversion path in event-date alignment.
    Expectation: the helper converts the timestamp into the index timezone before normalizing.
    """
    london_index = pd.DatetimeIndex(pd.to_datetime(['2024-01-03 00:00:00']).tz_localize('Europe/London'))
    new_york_event = pd.Timestamp('2024-01-02 20:00:00', tz='US/Eastern')

    assert align_event_date_to_index(london_index, new_york_event) == pd.Timestamp('2024-01-03', tz='Europe/London')


def test_resolve_event_location_handles_duplicate_dates_and_out_of_range_inputs():
    """Description: resolve an event against duplicate-index rows and out-of-range dates.

    Purpose: cover slice, lower-bound, upper-bound, and nearest-date branches.
    Expectation: the helper selects the first duplicate, clamps before/after bounds, and picks the nearest earlier observation on ties.
    """
    duplicate_index = pd.DatetimeIndex(pd.to_datetime(['2024-01-03', '2024-01-03', '2024-01-05']))
    regular_index = pd.DatetimeIndex(pd.to_datetime(['2024-01-03', '2024-01-05', '2024-01-09']))

    assert resolve_event_location(duplicate_index, pd.Timestamp('2024-01-03')) == 0
    assert resolve_event_location(regular_index, pd.Timestamp('2024-01-01')) == 0
    assert resolve_event_location(regular_index, pd.Timestamp('2024-01-12')) == 2
    assert resolve_event_location(regular_index, pd.Timestamp('2024-01-07')) == 1


def test_resolve_event_location_handles_boolean_mask_duplicate_branch_and_nearest_later_choice():
    """Description: resolve an event against a non-monotonic duplicate index and a nearer later observation.

    Purpose: cover the boolean-mask duplicate branch and the final insert_at return path.
    Expectation: the helper returns the first matching duplicate from a boolean mask and selects the later observation when it is strictly closer.
    """
    non_monotonic_duplicate_index = pd.DatetimeIndex(pd.to_datetime(['2024-01-03', '2024-01-05', '2024-01-03']))
    regular_index = pd.DatetimeIndex(pd.to_datetime(['2024-01-03', '2024-01-05', '2024-01-09']))

    assert resolve_event_location(non_monotonic_duplicate_index, pd.Timestamp('2024-01-03')) == 0
    assert resolve_event_location(regular_index, pd.Timestamp('2024-01-08')) == 2


def test_extract_event_payload_returns_empty_frame_for_none_input():
    """Description: normalize a completely missing raw payload.

    Purpose: cover the None-input guard in extract_event_payload.
    Expectation: the helper returns an empty payload frame with only the event_date column.
    """
    payload = extract_event_payload(None)

    assert payload.empty
    assert payload.columns.tolist() == [EVENT_DATE_COLUMN]


def test_validate_ticker_requirement_accepts_non_ticker_events_and_rejects_missing_ticker():
    """Description: validate ticker requirements for supported event types.

    Purpose: cover both the pass-through and failure branches in the shared ticker validator.
    Expectation: non-ticker events pass silently and ticker-required events fail without a ticker.
    """
    validate_ticker_requirement('CB', None)

    with pytest.raises(ValueError, match="ticker parameter is required when event_type='EARNINGS'"):
        validate_ticker_requirement('EARNINGS', None)


def test_get_country_events_wraps_the_shared_event_date_loader():
    """Description: query country-scoped event dates through the entity-decorated wrapper.

    Purpose: verify the new country entity surface reuses the shared event-date implementation.
    Expectation: the wrapper returns formatted dates and passes the country identifier as the country argument.
    """
    with mock.patch(
        'gs_quant.timeseries._event_study.event_study_api.load_real_event_dates',
        return_value=[pd.Timestamp('2024-03-20')],
    ) as mock_load:
        result = get_country_events(
            'United States',
            'CB',
            start_date='2024-01-01',
            end_date='2024-12-31',
        )

    assert isinstance(result, pd.Series)
    assert result.tolist() == ['2024-03-20']
    assert list(result.index) == [pd.Timestamp('2024-03-20')]
    assert result.name == 'CB_MEETING_US'
    assert result.attrs['query_event_type'] == 'CB_MEETING_US'
    assert result.attrs['resolved_country'] == 'United States'
    assert result.attrs['event_label'] == 'CB_MEETING_US'
    assert mock_load.call_args.args == (
        'CB_MEETING_US',
        'United States',
        'CB',
        pd.Timestamp('2024-01-01'),
        pd.Timestamp('2024-12-31'),
    )


def test_get_asset_events_accepts_asset_objects_and_maps_via_marquee_id():
    """Description: query asset-scoped event dates through the asset-measure wrapper.

    Purpose: verify the asset wrapper follows the plot_measure Asset contract while preserving the shared event-date flow.
    Expectation: the wrapper forwards the Asset object into the shared loader so the downstream resolver can branch on Asset vs string.
    """
    asset = mock.Mock()
    asset.get_marquee_id.return_value = 'MA4B66MW5E27UAHKG34'
    asset.get_entity.return_value = {'identifiers': {'bbid': 'AAPL UW', 'assetId': 'MA4B66MW5E27UAHKG34'}}

    with mock.patch(
        'gs_quant.timeseries._event_study.event_study_api.load_real_event_dates',
        return_value=[pd.Timestamp('2024-04-25')],
    ) as mock_load:
        result = get_asset_events(
            asset,
            start_date='2024-01-01',
            end_date='2024-12-31',
        )

    assert isinstance(result, pd.Series)
    assert result.tolist() == ['2024-04-25']
    assert list(result.index) == [pd.Timestamp('2024-04-25')]
    assert result.name == 'EARNINGS_AAPL'
    assert result.attrs['query_event_type'] == 'EARNINGS'
    assert result.attrs['ticker'] == 'MA4B66MW5E27UAHKG34'
    assert result.attrs['event_label'] == 'EARNINGS_AAPL'
    assert mock_load.call_args.kwargs['ticker'] is asset


def test_get_event_dates_internal_validates_n_events_and_returns_latest_subset():
    """Description: call the internal date loader directly with explicit n_events values.

    Purpose: cover invalid n_events validation and the latest-N truncation branch.
    Expectation: non-positive n_events raises ValueError and positive n_events keeps the latest matching dates.
    """
    with pytest.raises(ValueError, match='n_events must be a positive integer when provided'):
        get_event_dates_internal('CB', country='United States', n_events=0)

    with mock.patch(
        'gs_quant.timeseries._event_study.event_study_api.load_real_event_dates',
        return_value=[
            pd.Timestamp('2024-01-10'),
            pd.Timestamp('2024-02-20'),
            pd.Timestamp('2024-03-20'),
        ],
    ):
        result = get_event_dates_internal(
            'CB',
            country='United States',
            start_date='2024-01-01',
            end_date='2024-12-31',
            n_events=2,
        )

    assert result['dates'].tolist() == ['2024-02-20', '2024-03-20']


def test_parse_date_param_supports_timestamp_datetime_none_and_relative_offsets():
    """Description: parse the supported date input forms through the shared helper.

    Purpose: cover timestamp, datetime, None, and relative-date parsing branches.
    Expectation: each form resolves to a normalized pandas timestamp.
    """
    absolute_timestamp = parse_date_param(pd.Timestamp('2024-01-03 12:30:00'))
    absolute_datetime = parse_date_param(pd.Timestamp('2024-01-04').to_pydatetime())
    expected_today = pd.Timestamp.now().normalize()
    none_value = parse_date_param(None)
    relative_value = parse_date_param('2d')

    assert absolute_timestamp == pd.Timestamp('2024-01-03')
    assert absolute_datetime == pd.Timestamp('2024-01-04')
    assert none_value == expected_today
    assert relative_value == expected_today - pd.Timedelta(days=2)


def test_apply_relative_offset_and_validate_date_range_cover_error_paths():
    """Description: exercise offset and date-range validation error branches.

    Purpose: cover unsupported relative units and inverted date windows in shared helpers.
    Expectation: both invalid cases raise ValueError with the documented messages.
    """
    with pytest.raises(ValueError, match="Unsupported relative date unit 'q'"):
        _apply_relative_offset(pd.Timestamp('2024-01-10'), 1, 'q', direction=-1)

    with pytest.raises(ValueError, match=r'start_date \(2024-01-10\) must be before end_date \(2024-01-09\)'):
        validate_date_range(pd.Timestamp('2024-01-10'), pd.Timestamp('2024-01-09'))

    assert _apply_relative_offset(pd.Timestamp('2024-01-10'), 1, 'w', direction=-1) == pd.Timestamp('2024-01-03')
    assert _apply_relative_offset(pd.Timestamp('2024-01-10'), 1, 'm', direction=-1) == pd.Timestamp('2023-12-10')
    assert _apply_relative_offset(pd.Timestamp('2024-01-10'), 1, 'y', direction=-1) == pd.Timestamp('2023-01-10')


def test_resolve_query_event_covers_implied_country_mismatch_earnings_and_missing_country():
    """Description: resolve query events through the shared event normalization helper.

    Purpose: cover asset-scoped earnings and missing-country validation branches.
    Expectation: the helper maps earnings to an asset-scoped definition with no country and requires country for country-scoped macros.
    """
    assert resolve_query_event('EARNINGS', None) == ('EARNINGS', None, 'EARNINGS')

    with pytest.raises(ValueError, match="country is required when event_type 'GDP' resolves to 'GDP'"):
        resolve_query_event('GDP', None)

    with pytest.raises(ValueError, match="country is required when event_type 'CB' resolves to 'CB'"):
        resolve_query_event('CB', None)

    assert resolve_query_event('CB', 'United States') == ('CB_MEETING_US', 'United States', 'CB')


def test_resolve_query_event_covers_asset_and_generic_fallback_branches_via_patched_definitions():
    """Description: resolve query events through the non-country branches not reachable from the public registry.

    Purpose: cover the asset-type branch and the final generic fallback branch in resolve_query_event.
    Expectation: patched definitions return the direct asset output and the generic event_type fallback.
    """
    asset_definition = AssetEventType(
        event=SupportedEvent.EARNINGS,
        event_type='REBALANCE',
        event_name='Rebalance',
    )
    generic_definition = EventType(
        event=SupportedEvent.GDP,
        event_type='GENERIC_EVENT',
    )

    with mock.patch(
        'gs_quant.timeseries._event_study.event_study_query.normalize_event', return_value=asset_definition
    ):
        assert resolve_query_event('REBALANCE', 'United States') == ('REBALANCE', None, 'EARNINGS')

    with mock.patch(
        'gs_quant.timeseries._event_study.event_study_query.normalize_event', return_value=generic_definition
    ):
        assert resolve_query_event('GENERIC_EVENT', 'United States') == ('GENERIC_EVENT', 'United States', 'GDP')


def test_load_real_event_dates_filters_range_and_uses_asset_loader_when_needed():
    """Description: load event dates through the shared real-event loader.

    Purpose: cover the macro and asset-scoped branches plus in-range filtering in load_real_event_dates.
    Expectation: macro loads use CountryEvents.get_data, asset loads use AssetEvents.get_data, and out-of-range dates are dropped.
    """
    macro_records = [
        mock.Mock(event_date=pd.Timestamp('2024-01-01')),
        mock.Mock(event_date=pd.Timestamp('2024-01-03')),
        mock.Mock(event_date=pd.Timestamp('2024-01-05')),
    ]
    asset_records = [mock.Mock(event_date=pd.Timestamp('2024-02-01'))]

    with mock.patch('gs_quant.timeseries._event_study.event_study_query.CountryEvents') as mock_events:
        with mock.patch('gs_quant.timeseries._event_study.event_study_query.AssetEvents') as mock_asset_events:
            mock_events.return_value.get_data.return_value = macro_records
            mock_asset_events.return_value.get_data.return_value = asset_records

            macro_dates = load_real_event_dates(
                'CB', 'United States', 'CB', pd.Timestamp('2024-01-02'), pd.Timestamp('2024-01-04')
            )
            asset_dates = load_real_event_dates(
                'EARNINGS', None, 'EARNINGS', pd.Timestamp('2024-01-01'), pd.Timestamp('2024-02-28'), ticker='AAPL UW'
            )

    assert macro_dates == [pd.Timestamp('2024-01-03')]
    assert asset_dates == [pd.Timestamp('2024-02-01')]
    assert mock_events.return_value.get_data.call_count == 1
    assert mock_asset_events.return_value.get_data.call_count == 1


def test_attach_window_filter_and_resolve_nearest_date_cover_remaining_shared_branches():
    """Description: exercise window filtering and nearest-date resolution helpers.

    Purpose: cover the remaining shared helper branches for filtering and nearest-date lookup.
    Expectation: each filter mode behaves correctly, invalid modes fail, and nearest-date lookup handles bounds.
    """
    internal_df = pd.DataFrame(
        {
            'date': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03']),
            'value': [0.0, 1.0, 2.0],
            'event_type': [pd.NA, 'CB', pd.NA],
            '_day_offset': [-1, 0, 1],
            '_event_number': [1, 1, 1],
            '_asset_index': [0, 0, 0],
        }
    )

    assert apply_window_filter(internal_df, None, True).equals(internal_df)
    assert apply_window_filter(internal_df, WindowType.FULL, True).equals(internal_df)
    assert apply_window_filter(internal_df, WindowType.PRE_EVENT, True)['_day_offset'].tolist() == [-1, 0]
    assert apply_window_filter(internal_df, 'pre_event', False)['_day_offset'].tolist() == [-1]
    assert apply_window_filter(internal_df, WindowType.POST_EVENT, True)['_day_offset'].tolist() == [1]
    assert apply_window_filter(internal_df, WindowType.EVENT_DAY, True)['_day_offset'].tolist() == [0]

    with pytest.raises(
        ValueError,
        match="frame_timeseries_around_events supports window_type=None, 'full', 'pre_event', 'post_event', or 'event_day'",
    ):
        apply_window_filter(internal_df, 'bad-window', True)

    with mock.patch(
        'gs_quant.timeseries._event_study.event_study_frame.coerce_window_type',
        return_value='unexpected-window-type',
    ):
        with pytest.raises(
            ValueError,
            match="frame_timeseries_around_events supports window_type=None, 'full', 'pre_event', 'post_event', or 'event_day'",
        ):
            apply_window_filter(internal_df, WindowType.FULL, True)

    index = pd.DatetimeIndex(pd.to_datetime(['2024-01-02', '2024-01-04']))
    assert resolve_nearest_date(pd.DatetimeIndex([]), pd.Timestamp('2024-01-03')) is None
    assert resolve_nearest_date(index, pd.Timestamp('2024-01-01')) is None
    assert resolve_nearest_date(index, pd.Timestamp('2024-01-05')) is None
    assert resolve_nearest_date(index, pd.Timestamp('2024-01-03')) == pd.Timestamp('2024-01-02')


def test_to_calendar_date_and_sorted_unique_dates_normalize_tz_aware_values():
    """Description: normalize mixed timezone-aware event dates through shared helpers.

    Purpose: cover the timezone-stripping branch in to_calendar_date and de-duplication in sorted_unique_dates.
    Expectation: tz-aware timestamps become tz-naive calendar dates and duplicates are removed.
    """
    tz_aware = pd.Timestamp('2024-01-03 14:00:00', tz='UTC')

    assert to_calendar_date(tz_aware) == pd.Timestamp('2024-01-03')
    assert sorted_unique_dates([tz_aware, pd.Timestamp('2024-01-03')]) == [pd.Timestamp('2024-01-03')]


def test_get_event_window_covers_slice_and_iterable_location_branches():
    """Description: extract event windows against duplicate-index dataframes.

    Purpose: cover the slice and iterable get_loc branches in the shared event-window helper.
    Expectation: both duplicate-index shapes return non-empty windows anchored on the resolved event row.
    """
    monotonic_asset_df = pd.DataFrame(
        {'price': [100.0, 101.0, 102.0], 'return': [0.0, 0.01, 0.02]},
        index=pd.DatetimeIndex(pd.to_datetime(['2024-01-02', '2024-01-02', '2024-01-03'])),
    )
    non_monotonic_asset_df = pd.DataFrame(
        {'price': [100.0, 101.0, 102.0], 'return': [0.0, 0.01, 0.02]},
        index=pd.DatetimeIndex(pd.to_datetime(['2024-01-02', '2024-01-03', '2024-01-02'])),
    )

    slice_window = get_event_window(monotonic_asset_df, pd.Timestamp('2024-01-02'), 0)
    iterable_window = get_event_window(non_monotonic_asset_df, pd.Timestamp('2024-01-02'), 0)

    assert slice_window == [{'date': pd.Timestamp('2024-01-02'), 'day_offset': 0, 'value': 100.0}]
    assert iterable_window == [{'date': pd.Timestamp('2024-01-02'), 'day_offset': 0, 'value': 100.0}]
    assert get_event_window(monotonic_asset_df, pd.Timestamp('2024-01-02'), -1) is None


def test_build_event_study_frame_covers_validation_and_explicit_event_dates():
    """Description: build explicit-date event-study frames directly through the shared helper.

    Purpose: cover validation failures, explicit date parsing, de-duplication, and public row shaping.
    Expectation: invalid inputs fail and explicit dates produce a plain public frame without attrs.
    """
    series = pd.Series(
        [100.0, 110.0, 121.0],
        index=pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03']),
    )

    with pytest.raises(ValueError, match='window must be a non-negative integer'):
        build_event_study_frame(series, [pd.Timestamp('2024-01-02')], 'CB', window=-1)

    with pytest.raises(ValueError, match='events parameter must be non-empty'):
        build_event_study_frame(series, [], 'CB')

    event_frame = build_event_study_frame(
        series,
        ['2024-01-02', '2024-01-02'],
        'CB',
        window=1,
        window_type='event_day',
    )

    assert event_frame['value'].tolist() == [110.0]
    assert event_frame['type_of_events'].tolist() == ['CB']
    assert event_frame.attrs == {}


def test_build_event_study_frame_returns_empty_public_frame_when_all_event_windows_miss_series_range():
    """Description: build a frame where resolved event dates exist but fall outside the asset series range.

    Purpose: cover the branch where build_event_study_frame creates an empty public frame after window extraction.
    Expectation: the helper returns an empty public frame with only public columns.
    """
    series = pd.Series([100.0, 101.0], index=pd.to_datetime(['2024-01-01', '2024-01-02']))

    result = build_event_study_frame(
        series,
        [pd.Timestamp('2024-02-01')],
        'CB',
        window=1,
    )

    assert result.empty
    assert list(result.columns) == ['date', 'value', 'type_of_events']
    assert result.attrs == {}


def test_frame_timeseries_around_events_rejects_multi_asset_edge_cases_and_frames_explicit_events():
    """Description: exercise the public helper with explicit event dates and asset-list edge cases.

    Purpose: cover empty/multi-asset input validation and explicit event-date framing.
    Expectation: invalid asset lists fail and explicit dates frame directly without attrs.
    """
    series = pd.Series([100.0, 101.0, 102.0], index=pd.to_datetime(['2024-04-24', '2024-04-25', '2024-04-26']))

    with pytest.raises(ValueError, match='assets parameter must be non-empty'):
        frame_timeseries_around_events([], events=['2024-04-25'])

    with pytest.raises(ValueError, match='accepts only one asset'):
        frame_timeseries_around_events([series, series], events=['2024-04-25'])

    result = frame_timeseries_around_events(series, events=['2024-04-25'], window=1)

    assert result['type_of_events'].tolist()[1] == 'Event'
    assert result.attrs == {}


def test_frame_timeseries_around_events_accepts_single_asset_list():
    """Description: pass one asset inside a list into the public gs_quant framing helper.

    Purpose: cover the single-item list branch in the public API input normalization.
    Expectation: the helper accepts the single-item list and frames it like a bare series input.
    """
    series = pd.Series([100.0, 101.0, 102.0], index=pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03']))

    result = frame_timeseries_around_events([series], events=['2024-01-02'], window=1)

    assert result['value'].tolist() == [100.0, 101.0, 102.0]
    assert result['type_of_events'].tolist()[1] == 'Event'


def test_frame_timeseries_around_events_accepts_event_series_from_getters():
    """Description: pass getter-style event dates as a pd.Series into the public framing helper.

    Purpose: keep frame_timeseries_around_events aligned with get_country_events/get_asset_events,
    which now return date-indexed pd.Series values.
    Expectation: the helper extracts the explicit event-date list from the series values and frames normally.
    """
    series = pd.Series([100.0, 101.0, 102.0], index=pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03']))
    events = pd.Series(['2024-01-02'], index=pd.to_datetime(['2024-01-02']), dtype=object)

    result = frame_timeseries_around_events(series, events=events, window=1)

    assert result['value'].tolist() == [100.0, 101.0, 102.0]
    assert result['type_of_events'].tolist()[1] == 'Event'


def test_frame_timeseries_around_events_uses_propagated_country_event_label_from_getter_series():
    """Description: frame a series using event dates returned by the country-event getter.

    Purpose: verify the public framing helper consumes propagated event context from getter-returned series.
    Expectation: the event-day row uses the contextual label instead of the generic Event marker.
    """
    series = pd.Series([100.0, 101.0, 102.0], index=pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03']))

    with mock.patch(
        'gs_quant.timeseries._event_study.event_study_api.load_real_event_dates',
        return_value=[pd.Timestamp('2024-01-02')],
    ):
        events = get_country_events('United States', 'CB', start_date='2024-01-01', end_date='2024-12-31')

    result = frame_timeseries_around_events(series, events=events, window=1)

    assert result['value'].tolist() == [100.0, 101.0, 102.0]
    assert result['type_of_events'].tolist()[1] == 'CB_MEETING_US'


def test_frame_timeseries_around_events_uses_propagated_asset_event_label_from_getter_series():
    """Description: frame a series using event dates returned by the asset-event getter.

    Purpose: verify asset-scoped getter series propagate a contextual label into the public framing output.
    Expectation: the event-day row uses the asset-scoped label instead of the generic Event marker.
    """
    series = pd.Series([100.0, 101.0, 102.0], index=pd.to_datetime(['2024-04-24', '2024-04-25', '2024-04-26']))
    asset = mock.Mock()
    asset.get_marquee_id.return_value = 'MA4B66MW5E27UAHKG34'
    asset.get_entity.return_value = {'identifiers': {'bbid': 'AAPL UW', 'assetId': 'MA4B66MW5E27UAHKG34'}}

    with mock.patch(
        'gs_quant.timeseries._event_study.event_study_api.load_real_event_dates',
        return_value=[pd.Timestamp('2024-04-25')],
    ):
        events = get_asset_events(asset, start_date='2024-01-01', end_date='2024-12-31')

    result = frame_timeseries_around_events(series, events=events, window=1)

    assert result['value'].tolist() == [100.0, 101.0, 102.0]
    assert result['type_of_events'].tolist()[1] == 'EARNINGS_AAPL'


def test_frame_timeseries_around_events_accepts_event_datetime_index():
    """Description: pass event dates as a DatetimeIndex into the public framing helper.

    Purpose: support callers that already have event dates in pandas index form.
    Expectation: the helper converts the DatetimeIndex to the explicit event-date list expected by the frame builder.
    """
    series = pd.Series([100.0, 101.0, 102.0], index=pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03']))
    events = pd.DatetimeIndex(pd.to_datetime(['2024-01-02']))

    result = frame_timeseries_around_events(series, events=events, window=1)

    assert result['value'].tolist() == [100.0, 101.0, 102.0]
    assert result['type_of_events'].tolist()[1] == 'Event'


def test_frame_timeseries_around_events_accepts_event_timestamp_list():
    """Description: pass event dates as a list of pandas timestamps into the public framing helper.

    Purpose: keep direct Python callers working when they already hold explicit datetime-like event lists.
    Expectation: the helper accepts datetime-like lists and frames them like string inputs.
    """
    series = pd.Series([100.0, 101.0, 102.0], index=pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03']))
    events = [pd.Timestamp('2024-01-02')]

    result = frame_timeseries_around_events(series, events=events, window=1)

    assert result['value'].tolist() == [100.0, 101.0, 102.0]
    assert result['type_of_events'].tolist()[1] == 'Event'


def test_frame_timeseries_around_events_rejects_unsupported_event_container_type():
    """Description: pass an unsupported event container type into the public framing helper.

    Purpose: cover the public wrapper branch that rejects non-list, non-Series,
    and non-DatetimeIndex event inputs.
    Expectation: tuple inputs fail fast with the public validation error.
    """
    series = pd.Series([100.0, 101.0, 102.0], index=pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03']))

    with pytest.raises(ValueError, match='events parameter must be a list, pd.Series, or DatetimeIndex'):
        frame_timeseries_around_events(series, events=('2024-01-02',), window=1)


def test_frame_timeseries_around_events_frames_multiple_explicit_events():
    """Description: frame multiple explicit event dates through the public helper.

    Purpose: validate explicit date parsing, row shaping, and generic event labeling.
    Expectation: the function frames around the supplied dates and returns a plain DataFrame.
    """
    series = pd.Series(
        range(10),
        index=pd.bdate_range('2024-01-01', periods=10),
        name='Test Series',
    )
    result = frame_timeseries_around_events(series, events=['2024-01-03', '2024-01-08'], window=1)

    assert result.columns.tolist() == ['date', 'value', 'type_of_events']
    assert result['date'].tolist() == [
        pd.Timestamp('2024-01-02'),
        pd.Timestamp('2024-01-03'),
        pd.Timestamp('2024-01-04'),
        pd.Timestamp('2024-01-05'),
        pd.Timestamp('2024-01-08'),
        pd.Timestamp('2024-01-09'),
    ]
    assert result['value'].tolist() == [1, 2, 3, 4, 5, 6]
    assert result['type_of_events'].isna().tolist() == [True, False, True, True, False, True]
    assert result.loc[result['type_of_events'].notna(), 'type_of_events'].tolist() == ['Event', 'Event']
    assert result.attrs == {}


def test_frame_timeseries_around_events_supports_event_day_filter_for_explicit_events():
    """Description: frame one explicit event date using the event-day-only filter.

    Purpose: verify the public helper still applies window filtering after switching to explicit dates.
    Expectation: the result contains one event-day row labeled Event.
    """
    series = pd.Series(
        range(10),
        index=pd.bdate_range('2024-01-01', periods=10),
        name='Test Series',
    )
    result = frame_timeseries_around_events(series, events=['2024-01-03'], window=0, window_type=WindowType.EVENT_DAY)

    assert result.columns.tolist() == ['date', 'value', 'type_of_events']
    assert result['date'].tolist() == [pd.Timestamp('2024-01-03')]
    assert result['value'].tolist() == [2]
    assert result['type_of_events'].tolist() == ['Event']


def test_frame_timeseries_around_events_merges_overlapping_event_windows():
    """Description: frame two nearby events whose windows overlap in the source series.

    Purpose: verify gs_quant now matches DSL framing when event windows overlap.
    Expectation: overlapping windows retain separate rows per event window instead of collapsing duplicate dates.
    """
    series = pd.Series(
        range(10),
        index=pd.bdate_range('2024-01-01', periods=10),
        name='Test Series',
    )
    result = frame_timeseries_around_events(series, events=['2024-01-03', '2024-01-04'], window=1)

    assert result['date'].tolist() == [
        pd.Timestamp('2024-01-02'),
        pd.Timestamp('2024-01-03'),
        pd.Timestamp('2024-01-03'),
        pd.Timestamp('2024-01-04'),
        pd.Timestamp('2024-01-04'),
        pd.Timestamp('2024-01-05'),
    ]
    assert result['value'].tolist() == [1, 2, 2, 3, 3, 4]
    assert result['type_of_events'].isna().tolist() == [True, False, True, True, False, True]
    assert result.loc[result['type_of_events'].notna(), 'type_of_events'].tolist() == ['Event', 'Event']


def test_frame_timeseries_around_events_rejects_invalid_event_date():
    """Description: request framing with an invalid explicit event date string.

    Purpose: verify invalid explicit date inputs still fail cleanly.
    Expectation: the function raises a pandas parsing error surfaced as ValueError.
    """
    series = pd.Series(
        range(5),
        index=pd.bdate_range('2024-01-01', periods=5),
        name='Test Series',
    )

    with pytest.raises(ValueError):
        frame_timeseries_around_events(series, events=['not-a-date'])


def test_frame_timeseries_around_events_rejects_negative_window():
    """Description: call the public framing API with an invalid negative window.

    Purpose: cover the public window validation branch before any dataset access.
    Expectation: the function raises MqValueError with the documented message.
    """
    series = pd.Series(range(3), index=pd.bdate_range('2024-01-01', periods=3))

    with pytest.raises(MqValueError, match='window must be a non-negative integer'):
        frame_timeseries_around_events(series, events=['2024-01-02'], window=-1)


def test_frame_timeseries_around_events_rejects_empty_event_list():
    """Description: frame a series with no explicit event dates.

    Purpose: verify the public helper requires an explicit event list.
    Expectation: the function raises ValueError for an empty events list.
    """
    series = pd.Series(range(3), index=pd.bdate_range('2024-01-01', periods=3), name='Test Series')

    with pytest.raises(ValueError, match='events parameter must be non-empty'):
        frame_timeseries_around_events(series, events=[], window=1)


def test_events_rejects_nfp_for_country_without_mapping():
    """Description: resolve NFP for a country without an approved payroll mapping.

    Purpose: keep unsupported countries explicit when payroll coverage is intentionally absent.
    Expectation: CountryEvents raises MqValueError before any dataset query occurs.
    """
    with pytest.raises(MqValueError, match='event must be one of .* for country Japan'):
        CountryEvents('Japan', 'NFP')


def test_map_event_dates_to_series_covers_alignment_modes_and_dedupes():
    """Description: map derived event dates onto a response series under each alignment rule.

    Purpose: cover the internal alignment branches before framed output is built.
    Expectation: intersect, previous, next, and same return the documented mapped dates with duplicates removed.
    """
    series = pd.Series(
        [10.0, 11.0, 12.0],
        index=pd.to_datetime(['2024-01-01', '2024-01-03', '2024-01-04']),
    )
    event_dates = [pd.Timestamp('2024-01-02'), pd.Timestamp('2024-01-03'), pd.Timestamp('2024-01-03')]

    assert _map_event_dates_to_series(series, event_dates, CalendarAlignment.INTERSECT) == [pd.Timestamp('2024-01-03')]
    assert _map_event_dates_to_series(series, event_dates, CalendarAlignment.PREVIOUS) == [
        pd.Timestamp('2024-01-01'),
        pd.Timestamp('2024-01-03'),
    ]
    assert _map_event_dates_to_series(series, event_dates, CalendarAlignment.NEXT) == [pd.Timestamp('2024-01-03')]
    assert _map_event_dates_to_series(series, event_dates, CalendarAlignment.SAME) == [
        pd.Timestamp('2024-01-02'),
        pd.Timestamp('2024-01-03'),
    ]


@pytest.mark.parametrize(
    ('kwargs', 'message'),
    [
        ({'direction': 'sideways'}, "direction must be one of 'up', 'down', or 'abs'"),
        ({'metric': 'volatility'}, "metric must be one of 'return' or 'price_change'"),
        (
            {'calendar_alignment': 'later'},
            "calendar_alignment must be one of 'intersect', 'previous', 'next', or 'same'",
        ),
        ({'response_horizons': []}, 'response_horizons must be non-empty'),
        ({'response_anchor': -1}, 'response_anchor must be a non-negative integer'),
    ],
)
def test_build_event_impact_frame_validates_inputs(kwargs, message):
    """Description: call the new impact-analysis builder with invalid parameter combinations.

    Purpose: cover the normalization and validation guards in the internal impact-analysis module.
    Expectation: each invalid parameter set raises MqValueError with the documented message.
    """
    asset_a = pd.Series([10.0, 11.0, 12.0], index=pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03']))
    asset_b = pd.Series([100.0, 101.0, 102.0], index=pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03']))

    with pytest.raises(MqValueError, match=message):
        build_event_impact_frame(asset_a, asset_b, **kwargs)


def test_event_study_impact_helpers_cover_string_normalization_and_guard_branches():
    """Description: exercise the remaining direct helper branches in the impact-analysis module.

    Purpose: cover valid string normalization, default response horizons, and explicit unsupported helper inputs.
    Expectation: string inputs normalize successfully, None response horizons default to 1d, and unsupported helper inputs raise MqValueError.
    """
    asset_a = pd.Series([10.0, 11.0, 12.0], index=pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03']))
    asset_b = pd.Series([100.0, 111.0, 112.0], index=pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03']))
    metric_series = pd.Series([0.05, -0.20], index=pd.to_datetime(['2024-01-02', '2024-01-03']))

    result = build_event_impact_frame(
        asset_a,
        asset_b,
        threshold=0.10,
        direction='up',
        metric='return',
        calendar_alignment='intersect',
        response_horizons=None,
        window=0,
    )

    assert result.attrs['summary']['direction'] == 'up'
    assert result.attrs['summary']['metric'] == 'return'
    assert result.attrs['summary']['calendar_alignment'] == 'intersect'
    assert result.attrs['summary']['response_horizons'] == ['1d']
    assert _event_mask(metric_series, EventDirection.DOWN, 0.10).tolist() == [False, True]

    with pytest.raises(MqValueError, match='Unsupported metric: unsupported'):
        _compute_metric(asset_a, 'unsupported', 1, Returns.SIMPLE)

    with pytest.raises(MqValueError, match='Unsupported direction: unsupported'):
        _event_mask(metric_series, 'unsupported', 0.10)

    with pytest.raises(MqValueError, match='Unsupported calendar alignment: unsupported'):
        _map_event_dates_to_series(asset_a, [pd.Timestamp('2024-01-02')], 'unsupported')

    with pytest.raises(MqValueError, match='window must be a non-negative integer'):
        build_event_impact_frame(asset_a, asset_b, window=-1)


def test_build_event_impact_frame_returns_public_frame_and_metadata_for_return_events():
    """Description: derive event dates from asset B returns and frame asset A responses around them.

    Purpose: verify the new internal builder owns metric computation, event-date mapping, frame shaping, and metadata assembly.
    Expectation: the result exposes the public event-study columns while attrs retain raw dates, mapped dates, forward returns, and summary metadata.
    """
    asset_a = pd.Series(
        [10.0, 11.0, 13.0, 12.0],
        index=pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04']),
        name='Asset A',
    )
    asset_b = pd.Series(
        [100.0, 120.0, 119.0, 121.0],
        index=pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04']),
        name='Asset B',
    )

    result = build_event_impact_frame(
        asset_a,
        asset_b,
        window=1,
        threshold=0.10,
        direction=EventDirection.UP,
        metric=EventMetric.RETURN,
        horizon='1d',
        response_horizons=('1d', '2d'),
        calendar_alignment=CalendarAlignment.INTERSECT,
        a_returns_type=Returns.SIMPLE,
        b_returns_type=Returns.SIMPLE,
    )

    assert result.columns.tolist() == ['date', 'value', 'type_of_events']
    assert result['date'].tolist() == [pd.Timestamp('2024-01-02'), pd.Timestamp('2024-01-03')]
    assert result['type_of_events'].iloc[0] == 'Asset B up 0.1'
    assert pd.isna(result['type_of_events'].iloc[1])
    assert result['value'].tolist() == pytest.approx([0.1, 2 / 11])
    assert result.attrs['raw_event_dates'] == [pd.Timestamp('2024-01-02')]
    assert result.attrs['mapped_event_dates'] == [pd.Timestamp('2024-01-02')]
    assert list(result.attrs['forward_returns']) == ['1d', '2d']
    assert result.attrs['forward_returns']['1d']['date'].tolist() == [pd.Timestamp('2024-01-02')]
    assert result.attrs['forward_returns']['1d']['value'].tolist() == pytest.approx([0.1])
    assert result.attrs['summary']['event_count'] == 1
    assert result.attrs['summary']['raw_event_count'] == 1
    assert result.attrs['summary']['response_horizons'] == ['1d', '2d']
    assert result.attrs['summary']['primary_response_horizon'] == '1d'
    assert result.attrs['summary']['metric'] == 'return'
    assert result.attrs['summary']['direction'] == 'up'
    assert result.attrs['summary']['calendar_alignment'] == 'intersect'
    assert result.attrs['summary']['horizon_summary']['1d']['count'] == 1
    assert result.attrs['summary']['horizon_summary']['1d']['mean'] == pytest.approx(0.1)


def test_build_event_impact_frame_supports_price_change_previous_alignment_and_start_end_filters():
    """Description: derive absolute price-change events from asset B on dates missing from asset A.

    Purpose: cover price-change metrics, previous-date mapping, response anchoring, and start/end filtering in the impact-analysis builder.
    Expectation: the event is mapped onto the prior asset A date and the forward-response metadata reflects the anchored sample.
    """
    asset_a = pd.Series(
        [10.0, 12.0, 15.0, 16.0],
        index=pd.to_datetime(['2024-01-01', '2024-01-03', '2024-01-04', '2024-01-06']),
        name='Asset A',
    )
    asset_b = pd.Series(
        [100.0, 112.0, 111.0, 111.0, 123.0],
        index=pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05']),
        name='Asset B',
    )

    result = build_event_impact_frame(
        asset_a,
        asset_b,
        window=1,
        threshold=10.0,
        direction=EventDirection.ABS,
        metric=EventMetric.PRICE_CHANGE,
        horizon=1,
        response_horizons=(1,),
        response_anchor=1,
        calendar_alignment=CalendarAlignment.PREVIOUS,
        start=pd.Timestamp('2024-01-02'),
        end=pd.Timestamp('2024-01-06'),
    )

    assert result['date'].tolist() == [pd.Timestamp('2024-01-03'), pd.Timestamp('2024-01-04')]
    assert pd.isna(result['type_of_events'].iloc[0])
    assert result['type_of_events'].iloc[1] == 'Asset B abs 10.0'
    assert result['value'].tolist() == pytest.approx([3.0, 1.0])
    assert result.attrs['raw_event_dates'] == [pd.Timestamp('2024-01-05')]
    assert result.attrs['mapped_event_dates'] == [pd.Timestamp('2024-01-04')]
    assert result.attrs['forward_returns']['1']['value'].tolist() == pytest.approx([1.0])
    assert result.attrs['summary']['direction'] == 'abs'
    assert result.attrs['summary']['metric'] == 'price_change'
    assert result.attrs['summary']['calendar_alignment'] == 'previous'


def test_build_event_impact_frame_uses_asset_identifier_from_series_attrs_in_event_label():
    """Description: build impact-analysis labels from series attrs when the visible series name is only the measure.

    Purpose: preserve caller-supplied asset identifiers that survive in Series.attrs even when plot-service rewrites the
    series name to a measure such as spot.
    Expectation: the event-day label combines the asset identifier with the measure name.
    """
    asset_a = pd.Series(
        [10.0, 11.0, 13.0],
        index=pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03']),
        name='SPX spot',
    )
    asset_b = pd.Series(
        [100.0, 120.0, 121.0],
        index=pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03']),
        name='spot',
    )
    asset_b.attrs['asset_name'] = 'CL1'

    result = build_event_impact_frame(
        asset_a,
        asset_b,
        window=0,
        threshold=0.10,
        direction=EventDirection.UP,
        metric=EventMetric.RETURN,
        calendar_alignment=CalendarAlignment.INTERSECT,
    )

    assert result['type_of_events'].tolist() == ['CL1 spot up 0.1']


def test_extract_series_asset_identifier_ignores_non_dict_attrs():
    series = SimpleNamespace(attrs=[])

    assert _extract_series_asset_identifier(series) is None


def test_extract_series_asset_identifier_supports_non_primary_attr_keys():
    series = pd.Series([1.0], index=pd.to_datetime(['2024-01-01']), name='spot')
    series.attrs['symbol'] = 'CL1'

    assert _extract_series_asset_identifier(series) == 'CL1'


def test_resolve_series_event_label_keeps_existing_prefixed_name():
    series = pd.Series([1.0], index=pd.to_datetime(['2024-01-01']), name='CL1 spot')
    series.attrs['asset_name'] = 'CL1'

    assert _resolve_series_event_label(series, 'asset_b') == 'CL1 spot'


def test_resolve_series_event_label_returns_identifier_when_name_missing():
    series = pd.Series([1.0], index=pd.to_datetime(['2024-01-01']))
    series.attrs['asset_name'] = 'CL1'

    assert _resolve_series_event_label(series, 'asset_b') == 'CL1'


def test_build_event_impact_frame_prefixes_bare_asset_b_measure_name_in_event_label():
    """Description: use the event-study fallback label when Asset B only carries a measure name.

    Purpose: keep the event label readable inside event-study without relying on upstream metadata propagation.
    Expectation: a bare measure name such as spot is prefixed with asset_b.
    """
    asset_a = pd.Series(
        [10.0, 11.0, 13.0],
        index=pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03']),
        name='SPX spot',
    )
    asset_b = pd.Series(
        [100.0, 120.0, 121.0],
        index=pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03']),
        name='spot',
    )

    result = build_event_impact_frame(
        asset_a,
        asset_b,
        window=0,
        threshold=0.10,
        direction=EventDirection.UP,
        metric=EventMetric.RETURN,
        calendar_alignment=CalendarAlignment.INTERSECT,
    )

    assert result['type_of_events'].tolist() == ['asset_b spot up 0.1']


def test_event_impact_analysis_wraps_internal_builder():
    """Description: call the public impact-analysis wrapper with representative arguments.

    Purpose: verify the public plot_function remains a thin compatibility wrapper over the new internal module.
    Expectation: the wrapper forwards arguments unchanged and returns the internal builder result.
    """
    asset_a = pd.Series([10.0, 11.0], index=pd.to_datetime(['2024-01-01', '2024-01-02']))
    asset_b = pd.Series([100.0, 110.0], index=pd.to_datetime(['2024-01-01', '2024-01-02']))
    expected = pd.DataFrame({'date': [pd.Timestamp('2024-01-02')], 'value': [0.1], 'type_of_events': ['Event']})

    with mock.patch('gs_quant.timeseries.event_study.build_event_impact_frame', return_value=expected) as mock_build:
        result = event_impact_analysis(
            asset_a,
            asset_b,
            window=3,
            threshold=0.25,
            direction=EventDirection.DOWN,
            metric=EventMetric.RETURN,
            horizon='2d',
            b_returns_type=Returns.LOGARITHMIC,
            a_returns_type=Returns.ABSOLUTE,
            response_horizons=('1d', '5d'),
            response_anchor=2,
            calendar_alignment=CalendarAlignment.NEXT,
            start=pd.Timestamp('2024-01-01').date(),
            end=pd.Timestamp('2024-01-31').date(),
            ignored_kwarg='ignored',
        )

    assert result is expected
    assert mock_build.call_args.kwargs == {
        'asset_a': asset_a,
        'asset_b': asset_b,
        'window': 3,
        'threshold': 0.25,
        'direction': EventDirection.DOWN,
        'metric': EventMetric.RETURN,
        'horizon': '2d',
        'b_returns_type': Returns.LOGARITHMIC,
        'a_returns_type': Returns.ABSOLUTE,
        'response_horizons': ('1d', '5d'),
        'response_anchor': 2,
        'calendar_alignment': CalendarAlignment.NEXT,
        'start': pd.Timestamp('2024-01-01').date(),
        'end': pd.Timestamp('2024-01-31').date(),
    }


def test_event_study_label_helpers_cover_fallback_branches():
    """Description: exercise the remaining fallback branches in the public event-study label helpers.

    Purpose: keep the new event-label propagation logic fully covered across empty suffixes, identifier fallbacks, and series-label resolution paths.
    Expectation: helper functions return stable labels or Event fallbacks under each supported edge case.
    """
    assert event_study_labels_module.append_event_label_suffix('CB_MEETING', None) == 'CB_MEETING'
    assert event_study_labels_module.append_event_label_suffix('GDP_US', 'US') == 'GDP_US'

    asset_with_marquee_error = mock.Mock()
    asset_with_marquee_error.get_entity.side_effect = RuntimeError('boom')
    asset_with_marquee_error.get_identifier = None
    asset_with_marquee_error.get_marquee_id.side_effect = RuntimeError('boom')

    asset_with_identifier_retry = mock.Mock()
    asset_with_identifier_retry.get_entity.return_value = {'identifiers': {}}
    asset_with_identifier_retry.get_identifier.side_effect = [TypeError('bad signature'), 'MSFT UW']

    asset_with_identifier_error = mock.Mock()
    asset_with_identifier_error.get_entity.return_value = {'identifiers': {}}
    asset_with_identifier_error.get_identifier.side_effect = RuntimeError('boom')
    asset_with_identifier_error.get_marquee_id = None

    asset_with_identifier_typeerror_then_error = mock.Mock()
    asset_with_identifier_typeerror_then_error.get_entity.return_value = {'identifiers': {}}
    asset_with_identifier_typeerror_then_error.get_identifier.side_effect = [
        TypeError('bad signature'),
        RuntimeError('boom'),
    ]
    asset_with_identifier_typeerror_then_error.get_marquee_id = None

    assert event_study_labels_module.extract_asset_label_suffix(asset_with_marquee_error) is None
    assert event_study_labels_module.extract_asset_label_suffix(asset_with_identifier_retry) == 'MSFT'
    assert event_study_labels_module.extract_asset_label_suffix(asset_with_identifier_error) is None
    assert event_study_labels_module.extract_asset_label_suffix(asset_with_identifier_typeerror_then_error) is None
    assert (
        event_study_labels_module.build_asset_event_label(
            'EARNINGS',
            SimpleNamespace(entity={'identifiers': {}}, get_identifier=None, get_marquee_id=None),
            'AAPL UW',
        )
        == 'EARNINGS_AAPL'
    )

    assert (
        event_study_labels_module.resolve_event_series_label(SimpleNamespace(name=None, attrs='bad-attrs')) == 'Event'
    )

    named_events = pd.Series(['2024-01-02'], dtype=object, name='CB_MEETING_US')
    explicit_label_events = pd.Series(['2024-01-02'], dtype=object)
    explicit_label_events.attrs['event_label'] = 'EARNINGS_AAPL'
    country_attr_events = pd.Series(['2024-01-02'], dtype=object)
    country_attr_events.attrs['query_event_type'] = 'CB_MEETING_US'
    country_attr_events.attrs['resolved_country'] = 'United States'
    asset_attr_events = pd.Series(['2024-04-25'], dtype=object)
    asset_attr_events.attrs['query_event_type'] = 'EARNINGS'
    asset_attr_events.attrs['ticker'] = 'AAPL UW'

    assert event_study_labels_module.resolve_event_series_label(named_events) == 'CB_MEETING_US'
    assert event_study_labels_module.resolve_event_series_label(explicit_label_events) == 'EARNINGS_AAPL'
    assert event_study_labels_module.resolve_event_series_label(country_attr_events) == 'CB_MEETING_US'
    assert event_study_labels_module.resolve_event_series_label(asset_attr_events) == 'EARNINGS_AAPL'


def test_event_study_module_public_surface_executes_under_reload_for_coverage():
    """Description: reload the public event-study module and exercise each exported wrapper once.

    Purpose: ensure coverage records the public module-level definitions and thin wrappers that can otherwise be imported before measurement begins.
    Expectation: reload preserves the documented exports and each public wrapper delegates to the underlying helper with the expected normalized arguments.
    """
    reloaded = importlib.reload(event_study_module)
    series = pd.Series([100.0, 101.0], index=pd.to_datetime(['2024-01-01', '2024-01-02']))
    asset = mock.Mock()
    asset.get_marquee_id.return_value = 'MA4B66MW5E27UAHKG34'
    asset.get_entity.return_value = {'identifiers': {'bbid': 'AAPL UW', 'assetId': 'MA4B66MW5E27UAHKG34'}}
    frame_result = pd.DataFrame({'date': [pd.Timestamp('2024-01-02')], 'value': [101.0], 'type_of_events': ['Event']})
    impact_result = pd.DataFrame({'date': [pd.Timestamp('2024-01-02')], 'value': [0.1], 'type_of_events': ['Event']})
    country_result = pd.DataFrame({'dates': pd.Series(['2024-01-02'])})
    country_result.attrs['query_event_type'] = 'CB_MEETING_US'
    country_result.attrs['resolved_country'] = 'United States'
    asset_result = pd.DataFrame({'dates': pd.Series(['2024-01-02'])})
    asset_result.attrs['query_event_type'] = 'EARNINGS'
    asset_result.attrs['ticker'] = 'MA4B66MW5E27UAHKG34'

    assert reloaded.__all__ == [
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

    with mock.patch.object(
        reloaded,
        'get_event_dates_internal',
        side_effect=[country_result, asset_result],
    ) as mock_get_dates:
        country_events = reloaded.get_country_events(
            'United States', 'CB', source='plottool', real_time=True, request_id='req-1'
        )
        asset_events = reloaded.get_asset_events(asset, source='plottool', real_time=True, request_id='req-2')

    assert country_events.tolist() == ['2024-01-02']
    assert asset_events.tolist() == ['2024-01-02']
    assert mock_get_dates.call_args_list[0].kwargs['country'] == 'United States'
    assert mock_get_dates.call_args_list[1].kwargs['ticker'] is asset

    with mock.patch.object(reloaded, 'build_event_study_frame', return_value=frame_result) as mock_frame:
        with pytest.raises(ValueError, match='assets parameter must be non-empty'):
            reloaded.frame_timeseries_around_events([], events=['2024-01-02'])

        list_result = reloaded.frame_timeseries_around_events([series], events=[pd.Timestamp('2024-01-02')], window=1)
        bare_result = reloaded.frame_timeseries_around_events(series, events=['2024-01-02'], window=1)

    assert list_result is frame_result
    assert bare_result is frame_result
    assert mock_frame.call_args_list[0].kwargs['x'].equals(series)
    assert mock_frame.call_args_list[1].kwargs['x'].equals(series)

    with mock.patch.object(reloaded, 'build_event_impact_frame', return_value=impact_result) as mock_impact:
        result = reloaded.event_impact_analysis(series, series, ignored_kwarg='ignored')

    assert result is impact_result
    assert mock_impact.call_args.kwargs['asset_a'].equals(series)
    assert mock_impact.call_args.kwargs['asset_b'].equals(series)
