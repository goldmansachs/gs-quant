"""
Copyright 2021 Goldman Sachs.
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
from typing import List
import pandas as pd
import datetime as dt
import math

from gs_quant.target.risk_models import RiskModelData

from gs_quant.api.gs.risk_models import GsFactorRiskModelApi


def build_asset_data_map(results: List, universe: List, measure: str) -> dict:
    if not results:
        return {}
    data_map = {}
    for asset in universe:
        date_list = {}
        for row in results:
            if asset in row.get('assetData').get('universe'):
                i = row.get('assetData').get('universe').index(asset)
                date_list[row.get('date')] = row.get('assetData').get(measure)[i]
        data_map[asset] = date_list
    return data_map


def build_factor_data_map(results: List, identifier: str) -> dict:
    factor_data = [factor.get('factorId') for factor in results[0].get('factorData')]
    data_map = {}
    for factor in factor_data:
        date_list = {}
        factor_name = factor
        for row in results:
            for data in row.get('factorData'):
                if data.get('factorId') == factor:
                    factor_name = factor if identifier == 'id' else data.get(identifier)
                    date_list[row.get('date')] = data.get('factorReturn')
        data_map[factor_name] = date_list
    return data_map


def build_factor_data_dataframe(results: List, identifier: str) -> pd.DataFrame:
    data_map = {}
    date_list = []
    for row in results:
        date_list.append(row.get('date'))
        for data in row.get('factorData'):
            factor_name = data.get('factorId') if identifier == 'id' else data.get(identifier)
            factor_return = data.get('factorReturn')
            if factor_name in data_map.keys():
                factor_returns = data_map.get(factor_name)
                factor_returns.append(factor_return)
            else:
                factor_returns = [factor_return]
            data_map[factor_name] = factor_returns
        data_map['date'] = date_list
    data_frame = pd.DataFrame(data_map).set_index('date')
    return data_frame


def build_pfp_data_dataframe(results: List) -> pd.DataFrame:
    date_list = []
    pfp_list = []
    for row in results:
        pfp_map = dict()
        pfp_map['assetId'] = row.get('factorPortfolios').get('universe')
        for factor in row.get('factorPortfolios').get('portfolio'):
            factor_id = factor.get('factorId')
            pfp_map[f'factorId: {factor_id}'] = factor.get('weights')
        weights_df = pd.DataFrame(pfp_map)
        pfp_list.append(weights_df)
        date_list.append(row.get('date'))
    data = pd.concat(pfp_list, keys=date_list)
    return data


def get_isc_dataframe(results: dict) -> pd.DataFrame:
    cov_list = []
    date_list = []
    for row in results:
        matrix_df = pd.DataFrame(row.get('issuerSpecificCovariance'))
        cov_list.append(matrix_df)
        date_list.append(row.get('date'))
    data = pd.concat(cov_list, keys=date_list)
    return data


def get_covariance_matrix_dataframe(results: dict) -> pd.DataFrame:
    cov_list = []
    date_list = []
    for row in results:
        matrix_df = pd.DataFrame(row.get('covarianceMatrix'))
        factor_names = [data.get('factorName') for data in row.get('factorData')]
        matrix_df.columns = factor_names
        matrix_df.index = factor_names
        cov_list.append(matrix_df)
        date_list.append(row.get('date'))
    data = pd.concat(cov_list, keys=date_list)
    return data


def get_closest_date_index(date: dt.date, dates: List[str], direction: str) -> int:
    for i in range(50):
        for index in range(len(dates)):
            if direction == 'before':
                next_date = (date - dt.timedelta(days=i)).strftime('%Y-%m-%d')
            else:
                next_date = (date + dt.timedelta(days=i)).strftime('%Y-%m-%d')
            if next_date == dates[index]:
                return index
    return -1


def divide_request(data, n):
    for i in range(0, len(data), n):
        yield data[i:i + n]


def batch_and_upload_partial_data(model_id: str, data: dict, max_asset_size):
    """ Takes in total risk model data for one day and batches requests according to
    asset data size, returns a list of messages from resulting post calls"""
    date = data.get('date')
    if data.get('factorData'):
        factor_data = {
            'date': date,
            'factorData': data.get('factorData'),
            'covarianceMatrix': data.get('covarianceMatrix')}
        print('Uploading factor data')
        print(GsFactorRiskModelApi.upload_risk_model_data(
            model_id,
            factor_data,
            partial_upload=True)
        )

    if data.get('assetData'):
        asset_data_list, target_size = _batch_input_data({'assetData': data.get('assetData')}, max_asset_size)
        for asset_data_batch in asset_data_list:
            print(GsFactorRiskModelApi.upload_risk_model_data(
                model_id,
                {'assetData': asset_data_batch, 'date': date},
                partial_upload=True,
                target_universe_size=target_size)
            )

    if 'issuerSpecificCovariance' in data.keys() or 'factorPortfolios' in data.keys():
        for optional_input_key in ['issuerSpecificCovariance', 'factorPortfolios']:
            if data.get(optional_input_key):
                optional_data = data.get(optional_input_key)
                optional_data_list, target_size = _batch_input_data({optional_input_key: optional_data}, max_asset_size)
                print(f'{optional_input_key} being uploaded for {date}...')
                for optional_data_batch in optional_data_list:
                    print(GsFactorRiskModelApi.upload_risk_model_data(
                        model_id,
                        {optional_input_key: optional_data_batch, 'date': date},
                        partial_upload=True,
                        target_universe_size=target_size)
                    )


def risk_model_data_to_json(risk_model_data: RiskModelData) -> dict:
    risk_model_data = risk_model_data.to_json()
    risk_model_data['assetData'] = risk_model_data.get('assetData').to_json()
    if risk_model_data.get('factorPortfolios'):
        risk_model_data['factorPortfolios'] = risk_model_data.get('factorPortfolios').to_json()
        risk_model_data['factorPortfolios']['portfolio'] = [portfolio.to_json() for portfolio in
                                                            risk_model_data.get('factorPortfolios').get(
                                                                'portfolio')]
    if risk_model_data.get('issuerSpecificCovariance'):
        risk_model_data['issuerSpecificCovariance'] = risk_model_data.get('issuerSpecificCovariance').to_json()
    return risk_model_data


def get_universe_size(data_to_split: dict) -> int:
    # takes any chunk of risk model data and returns the universe size
    if 'assetData' in data_to_split.keys():
        return len(data_to_split.get('assetData').get('universe'))
    data_to_split = list(data_to_split.values())
    for data in data_to_split:
        if 'universe' in data.keys():
            return len(data.get('universe'))
        if 'universeId1' in data.keys():
            return len(set(data.get('universeId1') +
                           data.get('universeId1')))
    raise ValueError(f'No universe found for data {data_to_split}')


def _batch_input_data(input_data: dict, max_asset_size: int):
    data_key = list(input_data.keys())[0]
    target_universe_size = get_universe_size(input_data)
    split_num = math.ceil(target_universe_size / max_asset_size) if math.ceil(
        target_universe_size / max_asset_size) else 1
    split_idx = math.ceil(target_universe_size / split_num)
    batched_data_list = []
    for i in range(split_num):
        if data_key == 'assetData':
            data_batched = _batch_asset_input(input_data.get('assetData'), i, split_idx, split_num,
                                              target_universe_size)
        elif data_key == 'factorPortfolios':
            data_batched = _batch_pfp_input(input_data.get('factorPortfolios'), i, split_idx,
                                            split_num, target_universe_size)
        else:
            data_batched = _batch_isc_input(input_data.get('issuerSpecificCovariance'), i, split_idx, split_num,
                                            target_universe_size)
        batched_data_list.append(data_batched)
    return batched_data_list, target_universe_size


def _batch_asset_input(input_data: dict, i: int, split_idx: int, split_num: int, target_universe_size: int) -> dict:
    end_idx = (i + 1) * split_idx if split_num != i + 1 else target_universe_size + 1
    asset_data_subset = {'universe': input_data.get('universe')[i * split_idx:end_idx],
                         'specificRisk': input_data.get('specificRisk')[i * split_idx:end_idx],
                         'factorExposure': input_data.get('factorExposure')[i * split_idx:end_idx]}
    optional_asset_inputs = ['totalRisk', 'historicalBeta']
    for optional_input in optional_asset_inputs:
        if input_data.get(optional_input):
            asset_data_subset[optional_input] = input_data.get(optional_input)[i * split_idx:end_idx]
    return asset_data_subset


def _batch_pfp_input(input_data: dict, i: int, split_idx: int, split_num: int, target_universe_size: int) -> dict:
    end_idx = (i + 1) * split_idx if split_num != i + 1 else target_universe_size + 1
    pfp_data_subset = dict()
    universe_slice = input_data.get('universe')[i * split_idx:end_idx]
    pfp_data_subset['universe'] = universe_slice
    portfolio_slice = list()
    for portfolio in input_data.get('portfolio'):
        factor_id = portfolio.get('factorId')
        weights_slice = portfolio.get('weights')[i * split_idx:end_idx]
        portfolio_slice.append({"factorId": factor_id, "weights": weights_slice})
    pfp_data_subset['portfolio'] = portfolio_slice
    return pfp_data_subset


def _batch_isc_input(input_data: dict, i: int, split_idx: int, split_num: int, target_universe_size: int) -> dict:
    end_idx = (i + 1) * split_idx if split_num != i + 1 else target_universe_size + 1
    return {'universeId1': input_data.get('universeId1')[i * split_idx:end_idx],
            'universeId2': input_data.get('universeId2')[i * split_idx:end_idx],
            'covariance': input_data.get('covariance')[i * split_idx:end_idx]}
