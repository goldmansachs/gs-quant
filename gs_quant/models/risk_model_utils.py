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
import pydash
from time import sleep
from typing import List, Union

import pandas as pd

from gs_quant.api.gs.data import GsDataApi
from gs_quant.api.gs.risk_models import GsFactorRiskModelApi
from gs_quant.errors import MqRequestError
from gs_quant.target.risk_models import RiskModelData, RiskModelType as Type
from gs_quant.target.risk_models import RiskModelDataMeasure as Measure


def _map_measure_to_field_name(measure: Measure):
    measure_to_field = {
        Measure.Specific_Risk: 'specificRisk',
        Measure.Total_Risk: 'totalRisk',
        Measure.Historical_Beta: 'historicalBeta',
        Measure.Predicted_Beta: 'predictedBeta',
        Measure.Global_Predicted_Beta: 'globalPredictedBeta',
        Measure.Daily_Return: 'dailyReturn',
        Measure.Specific_Return: 'specificReturn',
        Measure.Estimation_Universe_Weight: 'estimationUniverseWeight',
        Measure.R_Squared: 'rSquared',
        Measure.Fair_Value_Gap_Standard_Deviation: 'fairValueGapStandardDeviation',
        Measure.Fair_Value_Gap_Percent: 'fairValueGapPercent',
        Measure.Universe_Factor_Exposure: 'factorExposure',
        Measure.Factor_Return: 'factorReturn',
        Measure.Factor_Standard_Deviation: 'factorStandardDeviation',
        Measure.Factor_Z_Score: 'factorZScore',
        Measure.Bid_Ask_Spread: 'bidAskSpread',
        Measure.Bid_Ask_Spread_30d: 'bidAskSpread30d',
        Measure.Bid_Ask_Spread_60d: 'bidAskSpread60d',
        Measure.Bid_Ask_Spread_90d: 'bidAskSpread90d',
        Measure.Trading_Volume: 'tradingVolume',
        Measure.Trading_Volume_30d: 'tradingVolume30d',
        Measure.Trading_Volume_60d: 'tradingVolume60d',
        Measure.Trading_Volume_90d: 'tradingVolume90d',
        Measure.Traded_Value_30d: 'tradedValue30d',
        Measure.Composite_Volume: 'compositeVolume',
        Measure.Composite_Volume_30d: 'compositeVolume30d',
        Measure.Composite_Volume_60d: 'compositeVolume60d',
        Measure.Composite_Volume_90d: 'compositeVolume90d',
        Measure.Composite_Value_30d: 'compositeValue30d',
        Measure.Issuer_Market_Cap: 'issuerMarketCap',
        Measure.Capitalization: 'capitalization',
        Measure.Currency: 'currency',
        Measure.Dividend_Yield: 'dividendYield',
        Measure.Price: 'price',
        Measure.Unadjusted_Specific_Risk: 'unadjustedSpecificRisk',
        Measure.Model_Price: 'modelPrice',
        Measure.Factor_Mean: 'factorMean',
        Measure.Factor_Cross_Sectional_Mean: 'factorCrossSectionalMean',
        Measure.Factor_Cross_Sectional_Standard_Deviation: 'factorCrossSectionalStandardDeviation',
    }

    return measure_to_field.get(measure, '')


def build_factor_id_to_name_map(results: List) -> dict:
    risk_model_factor_data = {}
    for row in results:
        for factor in row.get('factorData', []):
            factor_id = factor['factorId']
            if not risk_model_factor_data.get(factor_id):
                risk_model_factor_data[factor_id] = factor['factorName']
    return risk_model_factor_data


def build_asset_data_map(results: List, requested_universe: tuple, requested_measure: Measure, factor_map: dict) \
        -> dict:
    if not results:
        return {}
    data_field = _map_measure_to_field_name(requested_measure)
    # if full universe is requested then pull the universe from the results.
    universe = pydash.get(results, '0.assetData.universe', []) if not requested_universe else list(requested_universe)
    data_map = {}
    for asset in universe:
        date_list = {}
        for row in results:
            if asset in row.get('assetData').get('universe'):
                i = row.get('assetData').get('universe').index(asset)
                if data_field == 'factorExposure':
                    exposures = row.get('assetData').get(data_field)[i]
                    date_list[row.get('date')] = {factor_map.get(f, f): v for f, v in exposures.items()}
                else:
                    date_list[row.get('date')] = row.get('assetData').get(data_field)[i]
        data_map[asset] = date_list
    return data_map


def build_factor_data_map(results: List, identifier: str, risk_model_id: str, requested_measure: Measure,
                          factors: List[str] = []) -> Union[dict, pd.DataFrame]:
    field_name = _map_measure_to_field_name(requested_measure)
    if not field_name:
        raise NotImplementedError(f"{requested_measure.value} is currently not yet supported")

    data_list = []
    for row in results:
        date = row.get('date')
        factor_data = row.get('factorData')
        for factor_map in factor_data:
            data_list.append(
                {"date": date,
                 identifier: factor_map.get(identifier),
                 field_name: factor_map.get(field_name)
                 }
            )

    factor_data_df = pd.DataFrame(data_list)
    factor_data_df = factor_data_df.pivot(index="date", columns=identifier, values=field_name)

    # if factors, only return data for those factors
    if factors:
        missing_factors = set(factors) - set(factor_data_df.columns.tolist())
        if missing_factors:
            raise ValueError(f'Factors(s) with {identifier}(s) {", ".join(missing_factors)} do not exist in '
                             f'risk model {risk_model_id}. Make sure the factor {identifier}(s) are correct')

        factor_data_df = factor_data_df[factors]

    return factor_data_df


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


def get_optional_data_as_dataframe(results: List, optional_data_key: str) -> pd.DataFrame:
    cov_list = []
    date_list = []
    for row in results:
        matrix_df = pd.DataFrame(row.get(optional_data_key))
        cov_list.append(matrix_df)
        date_list.append(row.get('date'))
    results = pd.concat(cov_list, keys=date_list) if cov_list else pd.DataFrame({})
    return results


def get_covariance_matrix_dataframe(results: List[dict], covariance_matrix_key: str = 'covarianceMatrix') \
        -> pd.DataFrame:
    cov_list = []
    date_list = []
    for row in results:
        matrix_df = pd.DataFrame(row.get(covariance_matrix_key))
        factor_names = [data.get('factorName') for data in row.get('factorData')]
        matrix_df.columns = factor_names
        matrix_df.index = factor_names
        cov_list.append(matrix_df)
        date_list.append(row.get('date'))
    results = pd.concat(cov_list, keys=date_list) if cov_list else pd.DataFrame({})
    return results


def build_factor_volatility_dataframe(results: List, group_by_name: bool, factors: List[str]) -> pd.DataFrame:
    data = []
    dates = []
    for row in results:
        dates.append(row.get('date'))
        data.append(row.get('factorVolatility'))

    df = pd.DataFrame(data, index=dates)
    if group_by_name:
        factor_id_to_name_map = build_factor_id_to_name_map(results)
        df.rename(columns=factor_id_to_name_map, inplace=True)
    if factors:
        missing_factors = set(factors) - set(df.columns.tolist())
        if missing_factors:
            raise ValueError(f'Factors(s): {", ".join(missing_factors)} do not exist in the risk model. '
                             f'Make sure the factors are correct.')
        else:
            return df[factors]
    return df


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


def _upload_factor_data_if_present(model_id: str, data: dict, date: str, **kwargs):
    aws_upload = kwargs.get('aws_upload', None)
    if data.get('factorData'):
        factor_data = {
            'date': date,
            'factorData': data.get('factorData')}
        if data.get('covarianceMatrix'):
            factor_data['covarianceMatrix'] = data.get('covarianceMatrix')
        if data.get('unadjustedCovarianceMatrix') and aws_upload:
            factor_data['unadjustedCovarianceMatrix'] = data.get('unadjustedCovarianceMatrix')
        if data.get('preVRACovarianceMatrix') and aws_upload:
            factor_data['preVRACovarianceMatrix'] = data.get('preVRACovarianceMatrix')
        logging.info('Uploading factor data')
        _repeat_try_catch_request(GsFactorRiskModelApi.upload_risk_model_data, model_id=model_id,
                                  model_data=factor_data, partial_upload=True, **kwargs)


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


def batch_and_upload_partial_data(model_id: str, data: dict, max_asset_size: int, **kwargs):
    """ Takes in total risk model data for one day and batches requests according to
    asset data size, returns a list of messages from resulting post calls"""
    date = data.get('date')
    _upload_factor_data_if_present(model_id, data, date, **kwargs)
    sleep(2)
    if data.get('currencyRatesData'):
        _repeat_try_catch_request(GsFactorRiskModelApi.upload_risk_model_data, model_id=model_id,
                                  model_data={"currencyRatesData": data.get('currencyRatesData'), 'date': date},
                                  partial_upload=True, **kwargs)
        sleep(2)
    for risk_model_data_type in ["assetData", "issuerSpecificCovariance", "factorPortfolios"]:
        _repeat_try_catch_request(_batch_data_v2, model_id=model_id, data=data.get(risk_model_data_type),
                                  data_type=risk_model_data_type, max_asset_size=max_asset_size, date=date, **kwargs)
        sleep(2)


def _batch_data_v2(model_id: str, data: dict, data_type: str, max_asset_size: int, date: Union[str, dt.date], **kwargs):
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
                                                                  final_upload=final_upload, **kwargs)
                logging.info(res)
            except (MqRequestError, Exception) as e:
                raise e


def batch_and_upload_coverage_data(date: dt.date, gsid_list: list, model_id: str, batch_size: int):
    update_time = dt.datetime.today().strftime("%Y-%m-%dT%H:%M:%SZ")
    request_array = [{'date': date.strftime('%Y-%m-%d'),
                      'gsid': gsid,
                      'riskModel': model_id,
                      'updateTime': update_time} for gsid in set(gsid_list)]
    logging.info(f"Uploading {len(request_array)} gsids to asset coverage dataset")
    list_of_requests = list(divide_request(request_array, batch_size))
    logging.info(f"Uploading in {len(list_of_requests)} batches of {batch_size} gsids")
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

    optional_fields = list(input_data.keys())
    [optional_fields.remove(required_field) for required_field in ["universe", "specificRisk", "factorExposure"]]
    for optional_input in optional_fields:
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


def _repeat_try_catch_request(input_function, number_retries: int = 5,
                              return_result: bool = False,
                              verbose: bool = True,
                              **kwargs):
    t = 2.0
    errors = []
    for i in range(number_retries):
        try:
            result = input_function(**kwargs)
            if result:
                if return_result:
                    return result
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
                if verbose:
                    logging.warning(f'Exception caught while making request: {e}, retrying in {int(sleep_time)}')
                sleep(sleep_time)
            else:
                if verbose:
                    logging.warning(f'Maximum number of retries: {number_retries} triggered')
        except Exception as unknown_exception:
            errors.append(unknown_exception)
            if i < number_retries - 1:
                sleep_time = math.pow(2.2, t)
                t += 1
                if verbose:
                    logging.warning(f'Unknown exception caught: {unknown_exception}, retrying in {int(sleep_time)}')
                sleep(sleep_time)
            else:
                if verbose:
                    logging.warning(f'Maximum number of retries: {number_retries} triggered')
    if errors:
        raise errors.pop()
