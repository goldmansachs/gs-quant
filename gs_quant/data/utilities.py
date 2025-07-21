"""
Copyright 2023 Goldman Sachs.
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
import os
from dataclasses import dataclass
from enum import Enum
from itertools import groupby
from functools import partial
from concurrent.futures import ThreadPoolExecutor
from gs_quant.target.assets import FieldFilterMap, EntityQuery
from gs_quant.session import GsSession
import math
import pandas as pd
import datetime as dt
from typing import Dict, List, Any, Union, Tuple


class Utilities:
    class AssetApi:
        IdList = Union[Tuple[str, ...], List]

        @classmethod
        def __create_query(
                cls,
                fields: Union[List, Tuple] = None,
                as_of: dt.datetime = None,
                limit: int = None,
                scroll: str = None,
                scroll_id: str = None,
                order_by: List[str] = None,
                **kwargs
        ) -> EntityQuery:
            keys = set(kwargs.keys())
            valid = keys.intersection(FieldFilterMap.properties())
            invalid = keys.difference(valid)

            if invalid:
                bad_args = ['{}={}'.format(k, kwargs[k]) for k in invalid]
                raise KeyError('Invalid asset query argument(s): {}'.format(', '.join(bad_args)))

            return EntityQuery(
                where=FieldFilterMap(**kwargs),
                fields=fields,
                asOfTime=as_of or dt.datetime.utcnow(),
                limit=limit,
                scroll=scroll,
                scroll_id=scroll_id,
                order_by=order_by
            )

        @classmethod
        def get_many_assets_data(
                cls,
                fields: IdList = None,
                as_of: dt.datetime = None,
                limit: int = None,
                **kwargs
        ) -> dict:
            query = cls.__create_query(fields, as_of, limit, **kwargs)
            response = GsSession.current._post('/assets/data/query', payload=query)
            return response['results']

    @staticmethod
    def target_folder():

        get_cwd = os.getcwd()
        target_dir = 'data_extract_' + dt.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")

        if os.path.exists(get_cwd + "\\" + target_dir):
            final_dir = get_cwd + "\\" + target_dir
            return final_dir

        elif os.access(get_cwd, os.W_OK):
            try:
                os.makedirs(target_dir)
                final_dir = get_cwd + "\\" + target_dir
                return final_dir
            except Exception as ex:
                print(ex)
                return 1

    @staticmethod
    def pre_checks(final_end, original_start, time_field, datetime_delta_override, request_batch_size, write_to_csv):

        if write_to_csv:
            target_dir_result = Utilities.target_folder()
            if target_dir_result == 1:
                raise ValueError("Current working directory doesn't have write permissions to save data. Exiting .")
        else:
            target_dir_result = None

        if request_batch_size is None or not (0 < request_batch_size < 5):
            raise ValueError("Enter request batch size beteen 1-5")

        if datetime_delta_override is not None:
            if not isinstance(datetime_delta_override, int):
                raise ValueError("Time delta override must be greater than 0 and 1 - 5 for intraday dataset")
            elif isinstance(datetime_delta_override, int) and (datetime_delta_override < 0):
                raise ValueError("Time delta override must be greater than 0 and 1 - 5 for intraday dataset")
            elif (time_field == "time") and (datetime_delta_override > 5):
                raise ValueError("Time delta override must be greater than 0 and 1 - 5 for intraday dataset")

        if final_end is not None:
            if not isinstance(final_end, dt.datetime):
                raise ValueError("End date must of datetime.datetime format. Existing program....")
            elif (not isinstance(original_start, dt.datetime)):
                raise ValueError("Start date must be of datetime.datetime format. Exiting program......")
            elif (original_start > final_end):
                raise ValueError("Start date cannot be greater than end date. Exiting program......")
            elif (time_field == "time") and ((final_end - original_start).total_seconds() / 3600 > 5):
                raise ValueError("For intraday datasets diff between start & end date should be <= 5 hrs")

        return final_end, target_dir_result

    @staticmethod
    def batch(iterable, n=1):

        iter_len = len(iterable)
        for ndx in range(0, iter_len, n):
            yield iterable[ndx:min(ndx + n, iter_len)]

    @staticmethod
    def fetch_data(dataset, symbols, start=dt.datetime.now(), end=dt.datetime.now(), dimension="assetId", auth=None):

        if auth is not None:
            auth()
        try:
            return dataset.get_data(start, end, **{dimension: symbols})
        except Exception as ex:
            print(ex)
            return pd.DataFrame()

    @staticmethod
    def execute_parallel_query(
            dataset,
            coverage,
            start,
            end,
            symbol_dimension,
            parallel_factor,
            batch_size,
            authenticate,
            retry=0
    ):

        bound_get_data = partial(
            Utilities.fetch_data,
            dataset,
            start=start,
            end=end,
            dimension=symbol_dimension,
            auth=authenticate)

        print(f"{len(coverage)} symbols, will run in {math.ceil(len(coverage) / batch_size)} batches")
        with ThreadPoolExecutor(max_workers=parallel_factor) as e:
            try:
                df = pd.concat(e.map(bound_get_data, Utilities.batch(coverage, n=batch_size)))
                print(f"Fetched {len(df.index)} rows in {parallel_factor} concurrent process from {start} - {end}")
            except Exception as e:
                print(f"Failure getting data with error {e}, retrying...")
                if retry > 3:
                    raise Exception("retry failure")

                retry += 1
                df = Utilities.execute_parallel_query(dataset,
                                                      coverage,
                                                      start,
                                                      end,
                                                      symbol_dimension,
                                                      parallel_factor,
                                                      batch_size,
                                                      authenticate,
                                                      retry)

        return df

    @staticmethod
    def get_dataset_parameter(dataset):
        dimensions = dataset.provider.symbol_dimensions(dataset.id)
        symbol_dimension = dimensions[0]
        dataset_definition = dataset.provider.get_definition(dataset.id)
        history_time = dataset_definition.parameters.history_date
        time_field = dataset_definition.dimensions.time_field
        timedelta = dt.timedelta(days=180) if time_field == "date" else dt.timedelta(hours=1)
        return [time_field, history_time, symbol_dimension, timedelta]

    @staticmethod
    def write_consolidated_results(data_frame,
                                   target_dir_result,
                                   dataset,
                                   batch_number,
                                   handler,
                                   write_to_csv,
                                   coverage_length,
                                   symbols_per_csv):
        if data_frame.shape[0] > 0:
            if write_to_csv:
                data_frame.to_csv(f"{target_dir_result}\\{dataset.id}-batch {batch_number}.csv", ",")
            else:
                handler(data_frame)

        print(f"Wrote batch {batch_number} file out of {math.ceil(coverage_length / symbols_per_csv)}")

    @staticmethod
    def iterate_over_series(dataset,
                            coverage_batch,
                            original_start,
                            original_end,
                            datetime_delta_override,
                            symbol_dimension,
                            request_batch_size,
                            authenticate,
                            final_end,
                            write_to_csv,
                            target_dir_result,
                            batch_number,
                            coverage_length,
                            symbols_per_csv,
                            handler,
                            parallel_factor=5
                            ):

        start = original_start
        end = original_end
        data_frame = pd.DataFrame()

        while True:
            batch_frame = Utilities.execute_parallel_query(
                dataset,
                coverage_batch,
                start,
                end,
                symbol_dimension,
                parallel_factor,
                request_batch_size,
                authenticate
            )

            data_frame = pd.concat([data_frame, batch_frame], axis=0)

            start += datetime_delta_override
            end += datetime_delta_override

            if end > final_end:
                Utilities.write_consolidated_results(data_frame,
                                                     target_dir_result,
                                                     dataset,
                                                     batch_number,
                                                     handler,
                                                     write_to_csv,
                                                     coverage_length,
                                                     symbols_per_csv)
                break

        del data_frame
        return None

    @staticmethod
    def extract_xref(assets, out_type):

        # if multiple assets match, return highest ranking
        return sorted(assets, key=lambda x: x.get("rank", 0), reverse=True)[0].get(out_type, "")

    @staticmethod
    def map_identifiers(input_type: str, output_type: str, ids, as_of=dt.datetime.now()):

        asset_batches = Utilities.batch(ids, n=1000)
        all_assets = []
        for asset_batch in asset_batches:
            assets = Utilities.AssetApi.get_many_assets_data(**{input_type: asset_batch},
                                                             limit=min(5000, 5 * len(asset_batch)),
                                                             as_of=as_of,
                                                             fields=[input_type,
                                                                     output_type,
                                                                     "listed",
                                                                     "assetClassificationsIsPrimary",
                                                                     "rank"],
                                                             asset_classifications_is_primary=[True])

            assets = sorted(assets, key=lambda x: x[input_type])
            all_assets = all_assets + assets
        return {inp_id: Utilities.extract_xref(grouped_assets, output_type)
                for inp_id, grouped_assets in groupby(all_assets, key=lambda x: x[input_type])}

    @staticmethod
    def get_dataset_coverage(identifier, symbol_dimension, dataset):

        if symbol_dimension == "assetId":
            cov = dataset.get_coverage(fields=[identifier])
            coverage = cov[cov[identifier].notna()][identifier].tolist()
        elif symbol_dimension == "gsid":
            coverage = dataset.get_coverage()[symbol_dimension].tolist()
            coverage = list(Utilities.map_identifiers(symbol_dimension, identifier, coverage).values())
        else:
            coverage = dataset.get_coverage()[symbol_dimension].tolist()

        return coverage


class SecmasterXrefFormatter:
    class EventType(Enum):
        START = "start"
        END = "end"

    @dataclass
    class Event:
        date: str
        event_type: 'SecmasterXrefFormatter.EventType'
        record: Dict[str, Any]

        def __post_init__(self):
            # For end events, we want them to be processed after start events on the same date
            # This ensures proper handling of adjacent periods
            self.priority = 1 if self.event_type == SecmasterXrefFormatter.EventType.END else 0

    INFINITY_DATE = "9999-12-31"
    INFINITY_MARKER = "9999-99-99"

    @staticmethod
    def convert(data: Dict[str, Any]) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
        results = {}
        for entity_key, records in data.items():
            xrefs = SecmasterXrefFormatter._convert_entity_records(records)
            results[entity_key] = {"xrefs": xrefs}
        return results

    @staticmethod
    def _convert_entity_records(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Converts records using sweep-line algorithm for optimal time complexity.
        """
        if not records:
            return []

        # Filter and normalize records
        normalized_records = []
        for record in records:
            normalized_record = record.copy()
            if normalized_record['endDate'] == SecmasterXrefFormatter.INFINITY_MARKER:
                normalized_record['endDate'] = SecmasterXrefFormatter.INFINITY_DATE
            normalized_records.append(normalized_record)

        if not normalized_records:
            return []

        # Create events for sweep-line algorithm
        events = SecmasterXrefFormatter._create_events(normalized_records)

        # Sort events by date, then by priority (end events after start events on same date)
        events.sort(key=lambda e: (SecmasterXrefFormatter._date_sort_key(e.date), e.priority))

        # Process events with sweep-line
        return SecmasterXrefFormatter._process_events(events)

    @staticmethod
    def _create_events(records: List[Dict[str, Any]]) -> List[Event]:
        """
        Creates start and end events for each record.
        """
        events = []

        for record in records:
            # Create start event
            events.append(SecmasterXrefFormatter.Event(
                date=record['startDate'],
                event_type=SecmasterXrefFormatter.EventType.START,
                record=record
            ))

            # Create end event (day after the actual end date)
            if record['endDate'] != SecmasterXrefFormatter.INFINITY_DATE:
                next_day = SecmasterXrefFormatter._add_one_day(record['endDate'])
                if next_day:
                    events.append(SecmasterXrefFormatter.Event(
                        date=next_day,
                        event_type=SecmasterXrefFormatter.EventType.END,
                        record=record
                    ))

        return events

    @staticmethod
    def _process_events(events: List[Event]) -> List[Dict[str, Any]]:
        """
        Processes events using sweep-line algorithm to generate time periods.
        """
        periods = []
        active_identifiers = {}  # type -> record mapping
        current_period_start = None

        i = 0
        while i < len(events):
            current_date = events[i].date
            current_date_events = []

            # Collect all events for the current date
            while i < len(events) and events[i].date == current_date:
                current_date_events.append(events[i])
                i += 1

            # Close current period if we have active identifiers
            if active_identifiers and current_period_start is not None:
                period_end = SecmasterXrefFormatter._subtract_one_day(current_date)
                periods.append({
                    "startDate": current_period_start,
                    "endDate": period_end,
                    "identifiers": {record['type']: record['value']
                                    for record in active_identifiers.values()}
                })

            # Process all events for this date
            # First process END events, then START events
            end_events = [e for e in current_date_events if e.event_type == SecmasterXrefFormatter.EventType.END]
            start_events = [e for e in current_date_events if e.event_type == SecmasterXrefFormatter.EventType.START]

            # Remove ending identifiers
            for event in end_events:
                identifier_type = event.record['type']
                if identifier_type in active_identifiers:
                    del active_identifiers[identifier_type]

            # Add starting identifiers
            for event in start_events:
                identifier_type = event.record['type']
                active_identifiers[identifier_type] = event.record

            # Start new period if we have active identifiers
            if active_identifiers:
                current_period_start = current_date

        # Handle final period extending to infinity or latest end date
        if active_identifiers and current_period_start is not None:
            # Check if any active identifier has infinity end date
            has_infinity = any(
                record['endDate'] == SecmasterXrefFormatter.INFINITY_DATE
                for record in active_identifiers.values()
            )

            if has_infinity:
                period_end = SecmasterXrefFormatter.INFINITY_DATE
            else:
                # Find latest end date among active identifiers
                latest_end = max(record['endDate'] for record in active_identifiers.values())
                period_end = latest_end

            periods.append({
                "startDate": current_period_start,
                "endDate": period_end,
                "identifiers": {record['type']: record['value']
                                for record in active_identifiers.values()}
            })

        return periods

    @staticmethod
    def _date_sort_key(date_str: str) -> dt.datetime:
        if date_str == SecmasterXrefFormatter.INFINITY_DATE:
            return dt.datetime(9999, 12, 31)
        return dt.datetime.strptime(date_str, '%Y-%m-%d')

    @staticmethod
    def _add_one_day(date_str: str) -> str:
        try:
            if date_str == SecmasterXrefFormatter.INFINITY_DATE:
                return None
            date_obj = dt.datetime.strptime(date_str, '%Y-%m-%d')
            if date_obj.year == 9999 and date_obj.month == 12 and date_obj.day == 31:
                return None

            next_day = date_obj + dt.timedelta(days=1)
            return next_day.strftime('%Y-%m-%d')

        except (ValueError, OverflowError):
            return None

    @staticmethod
    def _subtract_one_day(date_str: str) -> str:
        try:
            date_obj = dt.datetime.strptime(date_str, '%Y-%m-%d')
            prev_day = date_obj - dt.timedelta(days=1)
            return prev_day.strftime('%Y-%m-%d')
        except (ValueError, OverflowError):
            return date_str
