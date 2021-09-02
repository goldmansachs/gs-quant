"""
Copyright 2020 Goldman Sachs.
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
from typing import Dict, Optional

import pandas as pd
from pydash import decapitalize

from gs_quant.api.gs.data import QueryType
from gs_quant.data.core import DataContext
from gs_quant.entities.entity import EntityType
from gs_quant.markets.securities import Asset
from gs_quant.models.risk_model import FactorRiskModel, ReturnFormat
from gs_quant.target.common import AssetClass, AssetType
from gs_quant.target.risk_models import Measure, DataAssetsRequest, RiskModelUniverseIdentifierRequest
from gs_quant.timeseries import plot_measure_entity, plot_measure, prices
from gs_quant.timeseries.measures import _extract_series_from_df


@plot_measure((AssetClass.Equity,), (AssetType.Single_Stock,), [QueryType.FACTOR_RETURN])
def factor_zscore(asset: Asset, risk_model_id: str, factor_name: str, *,
                  source: str = None, real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Asset factor exposure (in the form of z-scores) for a factor using specified risk model

    :param asset: asset object loaded from security master
    :param risk_model_id: requested risk model id
    :param factor_name: requested factor name
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: service request id, if any
    :return: Time-series of asset factor exposure across available risk model dates
    """
    model = FactorRiskModel.get(risk_model_id)
    factor = model.get_factor(factor_name)
    gsid = asset.get_identifier('GSID')

    # Query risk model data
    query_results = model.get_data(
        measures=[Measure.Factor_Name, Measure.Universe_Factor_Exposure, Measure.Asset_Universe],
        start_date=DataContext.current.start_time,
        end_date=DataContext.current.end_time,
        assets=DataAssetsRequest(identifier=RiskModelUniverseIdentifierRequest.gsid, universe=[gsid])
    ).get('results', [])

    # Get the factor data from query results
    z_scores = {}
    for result in query_results:
        exposures = result.get('assetData', {}).get('factorExposure', [])
        if exposures:
            z_scores[result['date']] = exposures[0].get(factor.id)

    return __format_plot_measure_results(z_scores, QueryType.FACTOR_EXPOSURE)


@plot_measure_entity(EntityType.RISK_MODEL, [QueryType.FACTOR_RETURN])
def factor_covariance(risk_model_id: str, factor_name_1: str, factor_name_2: str, *, source: str = None,
                      real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Covariance time-series between two factors in a risk model

    :param risk_model_id: risk model entity
    :param factor_name_1: first factor name
    :param factor_name_2: second factor name
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: Time-series of covariances between the two factors across available risk model dates
    """

    model = FactorRiskModel.get(risk_model_id)
    factor_1 = model.get_factor(factor_name_1)
    factor_2 = model.get_factor(factor_name_2)
    covariance_curve = factor_1.covariance(factor_2,
                                           DataContext.current.start_date,
                                           DataContext.current.end_date,
                                           ReturnFormat.JSON)
    return __format_plot_measure_results(covariance_curve, QueryType.COVARIANCE)


@plot_measure_entity(EntityType.RISK_MODEL, [QueryType.FACTOR_RETURN])
def factor_volatility(risk_model_id: str, factor_name: str, *, source: str = None,
                      real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Volatility timeseries for a factor in a risk model

    :param risk_model_id: risk model entity
    :param factor_name: factor name
    :param source: name of function caller
    :param real_time: whether to retrieve intra-day data instead of EOD
    :param request_id: server request id
    :return: Time-series of a factor's volatility across available risk model dates
    """
    model = FactorRiskModel.get(risk_model_id)
    factor = model.get_factor(factor_name)
    volatility = factor.volatility(DataContext.current.start_date,
                                   DataContext.current.end_date,
                                   ReturnFormat.JSON)
    return __format_plot_measure_results(volatility, QueryType.VOLATILITY, multiplier=100)


@plot_measure_entity(EntityType.RISK_MODEL, [QueryType.FACTOR_RETURN])
def factor_correlation(risk_model_id: str, factor_name_1: str, factor_name_2: str, *, source: str = None,
                       real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Correlation time-series between two factors in a risk model

    :param risk_model_id: risk model entity
    :param factor_name_1: first factor name
    :param factor_name_2: second factor name
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: Time-series of correlations between the two factors across available risk model dates
    """
    model = FactorRiskModel.get(risk_model_id)
    factor_1 = model.get_factor(factor_name_1)
    factor_2 = model.get_factor(factor_name_2)
    correlation = factor_1.correlation(factor_2,
                                       DataContext.current.start_date,
                                       DataContext.current.end_date,
                                       ReturnFormat.JSON)
    return __format_plot_measure_results(correlation, QueryType.CORRELATION)


@plot_measure_entity(EntityType.RISK_MODEL, [QueryType.FACTOR_RETURN])
def factor_performance(risk_model_id: str, factor_name: str, *, source: str = None,
                       real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Factor returns as a price time-series for a factor in a risk model

    :param risk_model_id: risk model entity
    :param factor_name: factor name
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: Time-series of factor returns as a price series across available risk model dates
    """

    model = FactorRiskModel.get(risk_model_id)
    factor = model.get_factor(factor_name)
    factor_returns = factor.returns(DataContext.current.start_date,
                                    DataContext.current.end_date,
                                    ReturnFormat.JSON)
    factor_return_timeseries = pd.Series(factor_returns)
    return prices(factor_return_timeseries, 100)


def __format_plot_measure_results(time_series: Dict, query_type: QueryType, multiplier=1, handle_missing_column=False):
    """ Create and return panda series expected for a plot measure """
    col_name = query_type.value.replace(' ', '')
    col_name = decapitalize(col_name)
    time_series_list = [{'date': k, col_name: v * multiplier} for k, v in time_series.items()]
    df = pd.DataFrame(time_series_list)
    if not df.empty:
        df.set_index('date', inplace=True)
        df.index = pd.to_datetime(df.index)
    return _extract_series_from_df(df, query_type, handle_missing_column)
