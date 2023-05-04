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
import datetime as dt
import logging
import math
from time import sleep
from typing import List, Dict, Union

import pandas as pd

from gs_quant.api.gs.data import GsDataApi
from gs_quant.api.gs.risk_models import GsFactorRiskModelApi
from gs_quant.errors import MqRequestError, MqValueError
from gs_quant.target.risk_models import RiskModelData, RiskModelType as Type


def build_asset_data_map(results: List, universe: List, measure: str, factor_map: dict) -> dict:
    if not results:
        return {}
    data_map = {}
    for asset in universe:
        date_list = {}
        for row in results:
            if asset in row.get('assetData').get('universe'):
                i = row.get('assetData').get('universe').index(asset)
                if measure == 'factorExposure':
                    exposures = row.get('assetData').get(measure)[i]
                    date_list[row.get('date')] = {factor_map.get(f, f): v for f, v in exposures.items()}
                else:
                    date_list[row.get('date')] = row.get('assetData').get(measure)[i]
        data_map[asset] = date_list
    return data_map


def build_factor_data_map(results: List, identifier: str, measure: str, factors: List[str] = []) -> dict:
    if not results:
        return {}
    factor_data = set()
    for row in results:
        factor_data |= set([factor.get('factorId') for factor in row.get('factorData')])
        if factors:
            factor_data &= set(factors)
    data_map = {}
    for factor in factor_data:
        date_list = {}
        factor_name = factor
        for row in results:
            for data in row.get('factorData'):
                if data.get('factorId') == factor:
                    factor_name = factor if identifier == 'factorId' else data.get(identifier)
                    date_list[row.get('date')] = data.get(measure)
        data_map[factor_name] = date_list
    return data_map


def validate_factors_exist(factors_to_validate: List[str], risk_model_factors: List[Dict],
                           risk_model_id: str, identifier: str) -> List[str]:

    risk_model_factors_id_to_name = {f['identifier']: f['name'] for f in risk_model_factors}
    all_factor_names = list(risk_model_factors_id_to_name.keys()) if identifier == 'identifier' else \
        list(risk_model_factors_id_to_name.values())
    factor_matches = list(set(all_factor_names) & set(factors_to_validate))
    wrong_factors = list(set(factors_to_validate) - set(factor_matches))

    if wrong_factors:
        raise MqValueError(f'Factors(s) with {identifier}(s) {", ".join(wrong_factors)} do not exist in '
                           f'risk model {risk_model_id}. Make sure the factor {identifier}(s) are correct')

    factor_ids = []
    if identifier == 'name':
        for f_id, f_name in risk_model_factors_id_to_name.items():
            if f_name in factors_to_validate:
                factor_ids.append(f_id)
    else:
        factor_ids = list(set(risk_model_factors_id_to_name.keys()) & set(factors_to_validate))

    return factor_ids


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
    results = pd.concat(pfp_list, keys=date_list) if pfp_list else pd.DataFrame({})
    return results


def get_isc_dataframe(results: dict) -> pd.DataFrame:
    cov_list = []
    date_list = []
    for row in results:
        matrix_df = pd.DataFrame(row.get('issuerSpecificCovariance'))
        cov_list.append(matrix_df)
        date_list.append(row.get('date'))
    results = pd.concat(cov_list, keys=date_list) if cov_list else pd.DataFrame({})
    return results


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
    results = pd.concat(cov_list, keys=date_list) if cov_list else pd.DataFrame({})
    return results


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


def batch_and_upload_partial_data_use_target_universe_size(model_id: str, data: dict, max_asset_size: int):
    """ Takes in total risk model data for one day and batches requests according to
    asset data size, returns a list of messages from resulting post calls"""
    date = data.get('date')
    _upload_factor_data_if_present(model_id, data, date)
    sleep(2)
    _batch_data_if_present(model_id, data, max_asset_size, date)


def _upload_factor_data_if_present(model_id: str, data: dict, date: str):
    if data.get('factorData'):
        factor_data = {
            'date': date,
            'factorData': data.get('factorData')}
        if data.get('covarianceMatrix'):
            factor_data['covarianceMatrix'] = data.get('covarianceMatrix')
        logging.info('Uploading factor data')
        _repeat_try_catch_request(GsFactorRiskModelApi.upload_risk_model_data, model_id=model_id,
                                  model_data=factor_data, partial_upload=True)


def _batch_data_if_present(model_id: str, data, max_asset_size, date):
    if data.get('assetData'):
        asset_data_list, target_size = _batch_input_data({'assetData': data.get('assetData')}, max_asset_size)
        for i in range(len(asset_data_list)):
            _repeat_try_catch_request(GsFactorRiskModelApi.upload_risk_model_data, model_id=model_id,
                                      model_data={'assetData': asset_data_list[i], 'date': date}, partial_upload=True,
                                      target_universe_size=target_size)

    if 'issuerSpecificCovariance' in data.keys() or 'factorPortfolios' in data.keys():
        for optional_key in ['issuerSpecificCovariance', 'factorPortfolios']:
            if data.get(optional_key):
                optional_data = data.get(optional_key)
                optional_data_list, target_size = _batch_input_data({optional_key: optional_data}, max_asset_size // 2)
                logging.info(f'{optional_key} being uploaded for {date}...')
                for i in range(len(optional_data_list)):
                    _repeat_try_catch_request(GsFactorRiskModelApi.upload_risk_model_data, model_id=model_id,
                                              model_data={optional_key: optional_data_list[i], 'date': date},
                                              partial_upload=True, target_universe_size=target_size)


def only_factor_data_is_present(model_type: Type, data: dict) -> bool:
    if model_type == Type.Macro or model_type == Type.Thematic:
        if len(data.keys()) == 2 and 'factorData' in data.keys():
            return True
    else:
        if len(data.keys()) == 3 and 'factorData' in data.keys() and 'covarianceMatrix' in data.keys():
            return True
    return False


def batch_and_upload_partial_data(model_id: str, data: dict, max_asset_size: int):
    """ Takes in total risk model data for one day and batches requests according to
    asset data size, returns a list of messages from resulting post calls"""
    date = data.get('date')
    _upload_factor_data_if_present(model_id, data, date)
    sleep(2)
    for risk_model_data_type in ["assetData", "issuerSpecificCovariance", "factorPortfolios"]:
        _repeat_try_catch_request(_batch_data_v2, model_id=model_id, data=data.get(risk_model_data_type),
                                  data_type=risk_model_data_type, max_asset_size=max_asset_size, date=date)
        sleep(2)


def _batch_data_v2(model_id: str, data: dict, data_type: str, max_asset_size: int, date: Union[str, dt.date]):
    if data:
        if data_type in ["issuerSpecificCovariance", "factorPortfolios"]:
            max_asset_size //= 2
        data_list, _ = _batch_input_data({data_type: data}, max_asset_size)
        for i in range(len(data_list)):
            final_upload = True if i == len(data_list) - 1 else False
            try:
                res = GsFactorRiskModelApi.upload_risk_model_data(model_id=model_id,
                                                                  model_data={data_type: data_list[i], 'date': date},
                                                                  partial_upload=True,
                                                                  final_upload=final_upload)
                logging.info(res)
            except (MqRequestError, Exception) as e:
                raise e


def batch_and_upload_coverage_data(date: dt.date, gsid_list: list, model_id: str):
    update_time = dt.datetime.today().strftime("%Y-%m-%dT%H:%M:%SZ")
    request_array = [{'date': date.strftime('%Y-%m-%d'),
                      'gsid': gsid,
                      'riskModel': model_id,
                      'updateTime': update_time} for gsid in set(gsid_list)]
    logging.info(f"Uploading {len(request_array)} gsids to asset coverage dataset")
    list_of_requests = list(divide_request(request_array, 1000))
    logging.info(f"Uploading in {len(list_of_requests)} batches of 1000 gsids")
    [_repeat_try_catch_request(GsDataApi.upload_data, data=data, dataset_id="RISK_MODEL_ASSET_COVERAGE") for data in
     list_of_requests]


def upload_model_data(model_id: str, data: dict, **kwargs):
    _repeat_try_catch_request(GsFactorRiskModelApi.upload_risk_model_data, model_id=model_id, model_data=data, **kwargs)


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
    data_splitted = list(data_to_split.values())
    for data in data_splitted:
        if isinstance(data, str):
            continue
        if 'universe' in data.keys():
            return len(data.get('universe'))
        if 'universeId1' in data.keys():
            return len(data.get('universeId1'))
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

    optional_asset_inputs = ['totalRisk', 'historicalBeta', 'predictedBeta', 'globalPredictedBeta', 'specificReturn',
                             'dailyReturn', 'rSquared', 'fairValueGapPercent', 'fairValueGapStandardDeviation',
                             'estimationUniverseWeight']

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


def _repeat_try_catch_request(input_function, number_retries: int = 5, **kwargs):
    t = 2.0
    errors = []
    for i in range(number_retries):
        try:
            result = input_function(**kwargs)
            if result:
                logging.info(result)
            errors.clear()
            break
        except MqRequestError as e:
            errors.append(e)
            if e.status < 500 and e.status != 429:
                raise e
            elif i < number_retries - 1:
                sleep_time = math.pow(2.2, t)
                t += 1
                logging.warning(f'Exception caught while making request: {e}, retrying in {int(sleep_time)}')
                sleep(sleep_time)
            else:
                logging.warning(f'Maximum number of retries: {number_retries} triggered')
        except Exception as unknown_exception:
            errors.append(unknown_exception)
            if i < number_retries - 1:
                sleep_time = math.pow(2.2, t)
                t += 1
                logging.warning(f'Unknown exception caught: {unknown_exception}, retrying in {int(sleep_time)}')
                sleep(sleep_time)
            else:
                logging.warning(f'Maximum number of retries: {number_retries} triggered')
    if errors:
        raise errors.pop()
