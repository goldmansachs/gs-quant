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
import datetime as dt
from itertools import groupby
from functools import partial
from concurrent.futures import ThreadPoolExecutor
from gs_quant.target.assets import FieldFilterMap, EntityQuery
from typing import List, Tuple, Union
from gs_quant.session import GsSession
import math
import pandas as pd


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
            coverage = cov[cov[identifier].notnull()][identifier].tolist()
        elif symbol_dimension == "gsid":
            coverage = dataset.get_coverage()[symbol_dimension].tolist()
            coverage = list(Utilities.map_identifiers(symbol_dimension, identifier, coverage).values())
        else:
            coverage = dataset.get_coverage()[symbol_dimension].tolist()

        return coverage
