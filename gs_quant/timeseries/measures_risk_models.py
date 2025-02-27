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
from enum import Enum
from typing import Dict, Optional

import pandas as pd
from pydash import decapitalize

from gs_quant.api.gs.data import QueryType
from gs_quant.data.core import DataContext
from gs_quant.entities.entity import EntityType
from gs_quant.markets.securities import Asset, AssetIdentifier
from gs_quant.models.risk_model import FactorRiskModel, MarqueeRiskModel
from gs_quant.markets.factor import ReturnFormat
from gs_quant.target.common import AssetClass, AssetType
from gs_quant.target.risk_models import RiskModelDataMeasure, RiskModelDataAssetsRequest, \
    RiskModelUniverseIdentifierRequest
from gs_quant.timeseries import plot_measure_entity, plot_measure, prices
from gs_quant.timeseries.measures import _extract_series_from_df

ModelMeasureStr = {
    'Asset Universe': RiskModelDataMeasure.Asset_Universe,
    'Historical Beta': RiskModelDataMeasure.Historical_Beta,
    'Total Risk': RiskModelDataMeasure.Total_Risk,
    'Specific Risk': RiskModelDataMeasure.Specific_Risk,
    'Specific Return': RiskModelDataMeasure.Specific_Return,
    'Daily Returns': RiskModelDataMeasure.Daily_Return,
    'Estimation Universe Weight': RiskModelDataMeasure.Estimation_Universe_Weight,
    'Residual Variance': RiskModelDataMeasure.Residual_Variance,
    'Predicted Beta': RiskModelDataMeasure.Predicted_Beta,
    'Global Predicted Beta': RiskModelDataMeasure.Global_Predicted_Beta,
    'Universe Factor Exposure': RiskModelDataMeasure.Universe_Factor_Exposure,
    'R Squared': RiskModelDataMeasure.R_Squared,
    'Fair Value Gap Percent': RiskModelDataMeasure.Fair_Value_Gap_Percent,
    'Fair Value Gap Standard Deviation': RiskModelDataMeasure.Fair_Value_Gap_Standard_Deviation,
    'Bid Ask Spread': RiskModelDataMeasure.Bid_Ask_Spread,
    'Bid Ask Spread 30d': RiskModelDataMeasure.Bid_Ask_Spread_30d,
    'Bid Ask Spread 60d': RiskModelDataMeasure.Bid_Ask_Spread_60d,
    'Bid Ask Spread 90d': RiskModelDataMeasure.Bid_Ask_Spread_90d,
    'Trading Volume': RiskModelDataMeasure.Trading_Volume,
    'Trading Volume 30d': RiskModelDataMeasure.Trading_Volume_30d,
    'Trading Volume 60d': RiskModelDataMeasure.Trading_Volume_60d,
    'Trading Volume 90d': RiskModelDataMeasure.Trading_Volume_90d,
    'Trading Value 30d': RiskModelDataMeasure.Traded_Value_30d,
    'Composite Volume': RiskModelDataMeasure.Composite_Volume,
    'Composite Volume 30d': RiskModelDataMeasure.Composite_Volume_30d,
    'Composite Volume 60d': RiskModelDataMeasure.Composite_Volume_60d,
    'Composite Volume 90d': RiskModelDataMeasure.Composite_Volume_90d,
    'Composite Value 30d': RiskModelDataMeasure.Composite_Value_30d,
    'Composite Issuer Market Cap': RiskModelDataMeasure.Issuer_Market_Cap,
    'Composite Price': RiskModelDataMeasure.Price,
    'Composite Model Price': RiskModelDataMeasure.Model_Price,
    'Composite Capitalization': RiskModelDataMeasure.Capitalization,
    'Composite Currency': RiskModelDataMeasure.Currency,
    'Composite Unadjusted Specific Risk': RiskModelDataMeasure.Unadjusted_Specific_Risk,
    'Dividend Yield': RiskModelDataMeasure.Dividend_Yield}


class ModelMeasureString(Enum):
    ASSET_UNIVERSE = 'Asset Universe'
    HISTORICAL_BETA = 'Historical Beta'
    TOTAL_RISK = 'Total Risk'
    SPECIFIC_RISK = 'Specific Risk'
    SPECIFIC_RETURNS = 'Specific Return'
    DAILY_RETURNS = 'Daily Returns'
    ESTIMATION_UNVERSE_WEIGHT = 'Estimation Universe Weight'
    RESIDUAL_VARIANCE = 'Residual Variance'
    PREDICTED_BETA = 'Predicted Beta'
    GLOBAL_PREDICTED_BETA = 'Global Predicted Beta'
    UNIVERSE_FACTOR_EXPOSURE = 'Universe Factor Exposure'
    R_SQUARED = 'R Squared'
    FAIR_VALUE_GAP_PERCENT = 'Fair Value Gap Percent'
    FAIR_VALUE_GAP_STANDARD_DEVIATION = 'Fair Value Gap Standard Deviation'
    BID_ASK_SPREAD = 'Bid Ask Spread'
    BID_AKS_SPREAD_30D = 'Bid Ask Spread 30d'
    BID_AKS_SPREAD_60D = 'Bid Ask Spread 60d'
    BID_AKS_SPREAD_90D = 'Bid Ask Spread 90d'
    TRADING_VOLUME = 'Trading Volume'
    TRADING_VOLUME_30D = 'Trading Volume 30d'
    TRADING_VOLUME_60D = 'Trading Volume 60d'
    TRADING_VOLUME_90D = 'Trading Volume 90d'
    TRADING_VALUE_30D = 'Trading Value 30d'
    COMPOSITE_VOLUME = 'Composite Volume'
    COMPOSITE_VOLUME_30D = 'Composite Volume 30d'
    COMPOSITE_VOLUME_60D = 'Composite Volume 60d'
    COMPOSITE_VOLUME_90D = 'Composite Volume 90d'
    COMPOSITE_VALUE_30d = 'Composite Value 30d'
    COMPOSITE_ISSUER_MARKET_CAP = 'Composite Issuer Market Cap'
    COMPOSITE_PRICE = 'Composite Price'
    COMPOSITE_MODEL_PRICE = 'Composite Model Price'
    COMPOSITE_CAPITALIZATION = 'Composite Capitalization'
    COMPOSITE_CURRENCY = 'Composite Currency'
    COMPOSITE_UNADJUSTED_SPECIFIC_RISK = 'Composite Unadjusted Specific Risk'
    DIVIDEND_YIELD = 'Dividend Yield'


@plot_measure((AssetClass.Equity,), (AssetType.Single_Stock,))
def risk_model_measure(asset: Asset, risk_model_id: str,
                       risk_model_measure_selected: ModelMeasureString = ModelMeasureString.HISTORICAL_BETA, *,
                       source: str = None, real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Retrieve risk model measures for a given asset.

    :param asset: Asset object loaded from security master
    :param risk_model_id: ID of the risk model
    :param risk_model_measure_selected: Selected risk model measure
    :param source: Name of function caller
    :param real_time: Whether to retrieve intraday data instead of EOD
    :param request_id: Service request ID, if any
    :return: Risk model measure data for the asset
    """
    model = MarqueeRiskModel.get(risk_model_id)
    gsid = asset.get_identifier(AssetIdentifier.GSID)
    risk_model_measure_selected = ModelMeasureStr[risk_model_measure_selected.value]

    query_results = model.get_data(
        measures=[risk_model_measure_selected,
                  RiskModelDataMeasure.Asset_Universe],
        start_date=DataContext.current.start_time,
        end_date=DataContext.current.end_time,
        assets=RiskModelDataAssetsRequest(identifier=RiskModelUniverseIdentifierRequest.gsid, universe=[gsid]),
        limit_factors=False
    ).get('results', [])

    measures = {}
    for result in query_results:
        if result:
            measure_name = set(result.get('assetData', {}).keys()).difference({'universe'})
            exposures = result.get('assetData', {}).get(measure_name.pop(), [])
            if exposures:
                measures[result['date']] = exposures[0]

    return __format_plot_measure_results(measures, QueryType.FACTOR_EXPOSURE)


@plot_measure((AssetClass.Equity,), (AssetType.Single_Stock,))
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
    model = MarqueeRiskModel.get(risk_model_id)
    factor = model.get_factor(factor_name)
    gsid = asset.get_identifier(AssetIdentifier.GSID)

    # Query risk model data
    query_results = model.get_data(
        measures=[RiskModelDataMeasure.Factor_Name,
                  RiskModelDataMeasure.Universe_Factor_Exposure,
                  RiskModelDataMeasure.Asset_Universe],
        start_date=DataContext.current.start_time,
        end_date=DataContext.current.end_time,
        assets=RiskModelDataAssetsRequest(identifier=RiskModelUniverseIdentifierRequest.gsid, universe=[gsid])
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
    factor_returns_df = factor.returns(DataContext.current.start_date, DataContext.current.end_date)
    factor_returns_series = factor_returns_df.squeeze() / 100
    return prices(factor_returns_series, 100)


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
