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
from gs_quant.api.gs.risk_models import GsFactorRiskModelApi
from gs_quant.target.risk_models import RiskModelData


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


def to_datetime(date: str):
    return dt.date(int(date[0:4]), int(date[5:7]), int(date[8:10]))


def batch_and_upload_partial_data(model_id: str, data: dict) -> list:
    """ Takes in total risk model data for one day and batches requests according to
    asset data size, returns a list of messages from resulting post calls"""
    posting_result_messages = []
    target_universe_size = len(data.get('assetData').get('universe'))
    factor_data = RiskModelData(
        data.get('date'),
        factor_data=data.get('factorData'),
        covariance_matrix=data.get('covarianceMatrix')
    )
    posting_result_messages.append(GsFactorRiskModelApi.upload_risk_model_data(
        model_id,
        factor_data,
        partial_upload=True)
    )
    split_num = int(target_universe_size / 15000) if int(target_universe_size / 15000) else 1
    split_idx = int(target_universe_size / split_num)
    for i in range(split_num):
        end_idx = (i + 1) * split_idx if split_num != i + 1 else target_universe_size + 1
        asset_data_subset = {'universe': data.get('assetData').get('universe')[i * split_idx:end_idx],
                             'specificRisk': data.get('assetData').get('specificRisk')[i * split_idx:end_idx],
                             'factorExposure': data.get('assetData').get('factorExposure')[i * split_idx:end_idx]}
        optional_asset_inputs = ['totalRisk', 'historicalBeta']
        for optional_input in optional_asset_inputs:
            if data.get('assetData').get(optional_input):
                asset_data_subset[optional_input] = data.get('assetData').get(optional_input)[i * split_idx:end_idx]

        asset_data_request = RiskModelData(data.get('date'), asset_data=asset_data_subset)
        posting_result_messages.append(
            GsFactorRiskModelApi.upload_risk_model_data(
                model_id,
                asset_data_request,
                partial_upload=True,
                target_universe_size=target_universe_size)
        )
    optional_inputs = ['issuerSpecificCovariance', 'factorPortfolios']
    optional_data = {'date': data.get('date')}
    for optional_input in optional_inputs:
        if data.get(optional_input):
            optional_data[optional_input] = data.get(optional_input)
    posting_result_messages.append(GsFactorRiskModelApi.upload_risk_model_data(
        model_id,
        optional_data,
        partial_upload=True,
        target_universe_size=target_universe_size)
    )
    return posting_result_messages


def get_most_recent_date_from_calendar(risk_model_id: str):
    calendar = GsFactorRiskModelApi.get_risk_model_calendar(risk_model_id).business_dates
    return dt.datetime.strptime(
        calendar[get_closest_date_index(dt.date.today() - dt.timedelta(days=1), calendar, "before")], "%Y/%m/%d")
