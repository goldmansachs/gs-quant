"""
Copyright 2024 Goldman Sachs.
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

from gs_quant.api.gs.assets import GsAssetApi
from typing import Tuple

import pandas as pd
import numpy as np
import datetime as dt
import math


def _get_asset_temporal_xrefs(position_sets_df: pd.DataFrame) -> Tuple[pd.DataFrame, str]:
    """Helper function to get temporal xrefs for assets in a position set"""
    universe = list(set(position_sets_df['identifier'].tolist()))
    batches = np.array_split(universe, math.ceil(len(universe) / 500))
    earliest_position_date = position_sets_df['date'].min()
    earliest_position_date = pd.Timestamp(earliest_position_date).to_pydatetime()

    results = []
    for batch in batches:
        cur_result = GsAssetApi.get_many_asset_xrefs(list(batch), limit=500)
        results += cur_result

    asset_xrefs_final = []
    for res in results:
        xrefs_list = res.get('xrefs')
        if not xrefs_list:
            continue
        all_xrefs = []
        for item in xrefs_list:
            if dt.datetime.strptime(item.get('endDate'), '%Y-%m-%d') >= earliest_position_date:
                new_xref_map = {'assetId': res.get('assetId'),
                                'startDate': item.get('startDate'), 'endDate': item.get('endDate')}
                new_xref_map.update(**item.get('identifiers'))
                all_xrefs.append(new_xref_map)
        asset_xrefs_final += all_xrefs

    xref_df = pd.DataFrame(asset_xrefs_final)

    # Infer identifier type
    all_possible_identifier_types = ["ticker", "bbid", "bcid", "ric", "cusip", "isin", "sedol", "gss", "gsid",
                                     "primeId", "gsn"]
    identifiers_found = set(xref_df.columns.tolist()) & set(all_possible_identifier_types)
    inferred_identifier_type = None
    largest_count = 0

    for each_id_type in identifiers_found:
        number_of_matches = len(set(xref_df[each_id_type]) & set(universe))

        if number_of_matches > largest_count:
            inferred_identifier_type = each_id_type
            largest_count = number_of_matches

    xref_df = xref_df.dropna(subset=inferred_identifier_type)
    xref_df = xref_df.fillna(value={'delisted': 'no'})
    xref_df = xref_df.loc[xref_df['delisted'] == 'no', :]

    return xref_df, inferred_identifier_type


def _group_temporal_xrefs_into_discrete_time_ranges(xref_df: pd.DataFrame):
    """Helper function that group asset xref data with overlapping temporal history"""
    def group_fn(df):
        # Find where the next group should start
        df = df.sort_values(by="endDate")

        # Groups should have non-overlapping time intervals/start_date, end_date
        where_next_group_should_start = (df['startDate'].shift(-1) > df['endDate'])

        # Assign group numbers based on where the next groups starts
        group_numbers = where_next_group_should_start.cumsum().shift(1).fillna(0).astype(int)

        return group_numbers

    xref_df['startDate'] = [dt.datetime.strptime(x, '%Y-%m-%d') for x in xref_df['startDate']]
    xref_df['endDate'] = [dt.datetime.strptime(x, '%Y-%m-%d') for x in xref_df['endDate']]

    groups = group_fn(xref_df)
    xref_df['group'] = groups


def _resolve_many_assets(historical_xref_df: pd.DataFrame, identifier_type: str, **kwargs) -> pd.DataFrame:
    """Given a dataframe with temporal xref asset data, resolve """
    all_dfs = []
    xref_group_by = historical_xref_df.groupby('group')
    for _, grouped_df in xref_group_by:
        unmapped = []
        all_results = []
        as_of = min(grouped_df['endDate'])
        identifiers = grouped_df[identifier_type].tolist()
        batches = np.array_split(identifiers, math.ceil(len(identifiers) / 500))

        resolved_positions = {}

        for batch in batches:
            curr_batch_map = GsAssetApi.resolve_assets(identifier=list(batch), as_of=as_of, limit=500,
                                                       fields=['name', 'id', identifier_type, 'tradingRestriction'],
                                                       **kwargs)
            resolved_positions = {**resolved_positions, **curr_batch_map}

        for asset_identifier, asset_resolved_data in resolved_positions.items():
            if asset_resolved_data:
                all_results.append(asset_resolved_data[0])
            else:
                unmapped += [{identifier_type: asset_identifier}]

        df = pd.DataFrame(all_results + unmapped)
        df['asOfDate'] = as_of
        df = pd.merge(df, grouped_df,
                      how="inner",
                      left_on=["id", identifier_type],
                      right_on=["assetId", identifier_type])[["assetId", "name", identifier_type,
                                                              "tradingRestriction", "asOfDate", "startDate", "endDate"]]
        all_dfs.append(df)

    final_df = pd.concat(all_dfs) if all_dfs else pd.DataFrame()

    return final_df
