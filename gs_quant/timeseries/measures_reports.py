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
from typing import Optional
import pandas as pd
from pydash import decapitalize
from dateutil.relativedelta import relativedelta

from gs_quant.api.gs.data import QueryType
from gs_quant.api.gs.portfolios import GsPortfolioApi
from gs_quant.data.core import DataContext
from gs_quant.entities.entity import EntityType
from gs_quant.errors import MqValueError, MqError
from gs_quant.markets.report import FactorRiskReport, PerformanceReport
from gs_quant.markets.report import ThematicReport
from gs_quant.models.risk_model import ReturnFormat, FactorRiskModel
from gs_quant.target.portfolios import RiskAumSource
from gs_quant.timeseries import plot_measure_entity
from gs_quant.timeseries.measures import _extract_series_from_df, SecurityMaster, AssetIdentifier


@plot_measure_entity(EntityType.REPORT, [QueryType.FACTOR_EXPOSURE])
def factor_exposure(report_id: str, factor_name: str, *, source: str = None,
                    real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Factor exposure data associated with a factor in a factor risk report

    :param report_id: factor risk report id
    :param factor_name: factor name
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: Timeseries of factor exposure for requested factor
    """
    return _get_factor_data(report_id, factor_name, QueryType.FACTOR_EXPOSURE)


@plot_measure_entity(EntityType.REPORT, [QueryType.FACTOR_PNL])
def factor_pnl(report_id: str, factor_name: str, *, source: str = None,
               real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Factor PnL data associated with a factor in a factor risk report

    :param report_id: factor risk report id
    :param factor_name: factor name
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: Timeseries of factor pnl for requested factor
    """
    return _get_factor_data(report_id, factor_name, QueryType.FACTOR_PNL)


@plot_measure_entity(EntityType.REPORT, [QueryType.FACTOR_PROPORTION_OF_RISK])
def factor_proportion_of_risk(report_id: str, factor_name: str, *, source: str = None,
                              real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Factor proportion of risk data associated with a factor in a factor risk report

    :param report_id: factor risk report id
    :param factor_name: factor name
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: Timeseries of factor proportion of risk for requested factor
    """
    return _get_factor_data(report_id, factor_name, QueryType.FACTOR_PROPORTION_OF_RISK)


@plot_measure_entity(EntityType.REPORT, [QueryType.DAILY_RISK])
def daily_risk(report_id: str, factor_name: str = 'Total', *, source: str = None,
               real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Daily risk data associated with a factor in a factor risk report

    :param report_id: factor risk report id
    :param factor_name: factor name (must be "Factor", "Specific", or "Total")
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: Timeseries of daily risk for requested factor
    """
    return _get_factor_data(report_id, factor_name, QueryType.DAILY_RISK)


@plot_measure_entity(EntityType.REPORT, [QueryType.ANNUAL_RISK])
def annual_risk(report_id: str, factor_name: str = 'Total', *, source: str = None,
                real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Annual risk data associated with a factor in a factor risk report

    :param report_id: factor risk report id
    :param factor_name: factor name (must be "Factor", "Specific", or "Total")
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: Timeseries of daily risk for requested factor
    """
    return _get_factor_data(report_id, factor_name, QueryType.ANNUAL_RISK)


@plot_measure_entity(EntityType.REPORT, [QueryType.PNL])
def normalized_performance(report_id: str, aum_source: str = None, *, source: str = None,
                           real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Returns the Normalized Performance of a performance report based on AUM source
    :param report_id: id of performance report
    :param aum_source: source to normalize pnl from, default is the aum source on your portfolio,
                if no aum source is set on your portfolio the default is gross
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: portfolio normalized performance

    **Usage**

    Returns the normalized performance of the portfolio based on AUM source.

    If :math:`aum_source` is "Custom AUM":
    We read AUM from custom AUM uploaded to that portfolio and normalize performance based on that exposure

    If :math:`aum_source` is one of: Long, Short, RiskAumSource.Net,
        AumSource.Gross, we take these exposures from the calculated exposures based on daily positions

    :math:`NP(L/S)_{t} = SUM( PNL(L/S)_{t}/ ( EXP(L/S)_{t} ) - cPNL(L/S)_{t-1) )
        if ( EXP(L/S)_{t} ) - cPNL(L/S)_{t-1)) > 0
        else:
            1/ SUM( PNL(L/S)_{t}/ ( EXP(L/S)_{t} ) - cPNL(L/S)_{t-1) )`
    For each leg, short and long, then:
    :math:`NP_{t} = NP(L)_{t} * (EXP(L)_{t} / AUM_{t}) + NP(S)_{t} * (EXP(S)_{t} / AUM_{t}) + 1`

    This takes into account varying AUM and adjusts for exposure change due to PNL

    where :math:`cPNL(L/S)_{t-1}` is your performance reports cumulative long or short PNL at date t-1
    where :math:`PNL(L/S)_{t}` is your performance reports long or short pnl at date t
    where :math:`AUM_{t}` is portfolio exposure on date t
    where :math:`EXP(L/S)_{t}` is the long or short exposure on date t

    """
    start_date = DataContext.current.start_time - relativedelta(1)
    end_date = DataContext.current.end_time

    start_date = start_date.date()
    end_date = end_date.date()

    performance_report = PerformanceReport.get(report_id)
    if not aum_source:
        port = GsPortfolioApi.get_portfolio(performance_report.position_source_id)
        aum_source = port.aum_source if port.aum_source else RiskAumSource.Gross
    else:
        aum_source = RiskAumSource(aum_source)

    constituent_data = performance_report.get_portfolio_constituents(
        fields=['assetId', 'pnl', 'quantity', 'netExposure'], start_date=start_date, end_date=end_date).set_index(
        'date')

    aum_col_name = aum_source.value.lower()
    aum_col_name = f'{aum_col_name}Exposure' if aum_col_name != 'custom aum' else 'aum'

    # Split into long and short and aggregate across dates
    long_side = _return_metrics(constituent_data[constituent_data['quantity'] > 0],
                                list(constituent_data.index.unique()), "long")
    short_side = _return_metrics(constituent_data[constituent_data['quantity'] < 0],
                                 list(constituent_data.index.unique()), "short")
    # Get aum source data
    if aum_source == RiskAumSource.Custom_AUM:
        custom_aum = pd.DataFrame(
            GsPortfolioApi.get_custom_aum(performance_report.position_source_id, start_date, end_date))
        if custom_aum.empty:
            raise MqError(
                f'No custom AUM for portfolio {performance_report.position_source_id} between dates {start_date},'
                f' {end_date}')
        data = pd.DataFrame.from_records(custom_aum).set_index(['date'])
    else:
        data = performance_report.get_many_measures([aum_col_name], start_date, end_date).set_index(['date'])

    long_side = long_side.join(data[[f'{aum_col_name}']], how='inner')
    short_side = short_side.join(data[[f'{aum_col_name}']], how='inner')

    long_side['longRetWeighted'] = (long_side['longMetrics'] - 1) * long_side['exposure'] * \
                                   (1 / long_side[f'{aum_col_name}'])
    short_side['shortRetWeighted'] = (short_side['shortMetrics'] - 1) * short_side['exposure'] *\
                                     (1 / short_side[f'{aum_col_name}'])

    combined = long_side[['longRetWeighted']].join(short_side[['shortRetWeighted']], how='inner')
    combined['normalizedPerformance'] = combined['longRetWeighted'] + combined['shortRetWeighted'] + 1
    return pd.Series(combined['normalizedPerformance'], name="normalizedPerformance").dropna()


@plot_measure_entity(EntityType.REPORT, [QueryType.THEMATIC_EXPOSURE])
def thematic_exposure(report_id: str, basket_ticker: str, *, source: str = None,
                      real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Thematic exposure of a portfolio to a requested GS thematic flagship basket

    :param report_id: portfolio thematic analytics report id
    :param basket_ticker: ticker for thematic basket
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: Timeseries of daily thematic beta of portfolio to requested flagship basket
    """
    thematic_report = ThematicReport.get(report_id)
    asset = SecurityMaster.get_asset(basket_ticker, AssetIdentifier.TICKER)
    df = thematic_report.get_thematic_exposure(start_date=DataContext.current.start_date,
                                               end_date=DataContext.current.end_date,
                                               basket_ids=[asset.get_marquee_id()])
    if not df.empty:
        df.set_index('date', inplace=True)
        df.index = pd.to_datetime(df.index)
    return _extract_series_from_df(df, QueryType.THEMATIC_EXPOSURE)


@plot_measure_entity(EntityType.REPORT, [QueryType.THEMATIC_EXPOSURE])
def thematic_beta(report_id: str, basket_ticker: str, *, source: str = None,
                  real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Thematic beta values of a portfolio to a requested GS thematic flagship basket

    :param report_id: portfolio thematic analytics report id
    :param basket_ticker: ticker for thematic basket
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: Timeseries of daily thematic beta of portfolio to requested flagship basket
    """
    thematic_report = ThematicReport.get(report_id)
    asset = SecurityMaster.get_asset(basket_ticker, AssetIdentifier.TICKER)
    df = thematic_report.get_thematic_betas(start_date=DataContext.current.start_date,
                                            end_date=DataContext.current.end_date,
                                            basket_ids=[asset.get_marquee_id()])
    if not df.empty:
        df.set_index('date', inplace=True)
        df.index = pd.to_datetime(df.index)
    return _extract_series_from_df(df, QueryType.THEMATIC_BETA)


def _get_factor_data(report_id: str, factor_name: str, query_type: QueryType) -> pd.Series:
    # Check params
    report = FactorRiskReport.get(report_id)
    if factor_name not in ['Factor', 'Specific', 'Total']:
        if query_type in [QueryType.DAILY_RISK, QueryType.ANNUAL_RISK]:
            raise MqValueError('Please pick a factor name from the following: ["Total", "Factor", "Specific"]')
        model = FactorRiskModel.get(report.get_risk_model_id())
        factor = model.get_factor(factor_name)
        factor_name = factor.name

    # Extract relevant data for each date
    col_name = query_type.value.replace(' ', '')
    col_name = decapitalize(col_name)
    data_type = decapitalize(col_name[6:]) if col_name.startswith('factor') else col_name

    factor_data = report.get_results(
        factors=[factor_name],
        start_date=DataContext.current.start_date,
        end_date=DataContext.current.end_date,
        return_format=ReturnFormat.JSON
    )
    factor_exposures = [{'date': d['date'], col_name: d[data_type]} for d in factor_data if d.get(data_type)]

    # Create and return timeseries
    df = pd.DataFrame(factor_exposures)
    if not df.empty:
        df.set_index('date', inplace=True)
        df.index = pd.to_datetime(df.index)
    return _extract_series_from_df(df, query_type)


def _return_metrics(one_leg, dates, name):
    if one_leg.empty:
        return pd.DataFrame(index=dates, data={f'{name}Metrics': [0 for d in dates], "exposure": [0 for d in dates]})
    one_leg = one_leg.groupby(one_leg.index).agg(pnl=('pnl', 'sum'), exposure=('netExposure', 'sum'))
    one_leg['exposure'] = one_leg['exposure'].apply(lambda x: abs(x))
    one_leg['cumulativePnlT-1'] = one_leg['pnl'].cumsum(axis=0)

    one_leg[f'{name}Metrics'] = one_leg['pnl'] / (one_leg['exposure'] - one_leg['cumulativePnlT-1'])

    one_leg[f'{name}Metrics'].iloc[0] = 0
    one_leg[f'{name}Metrics'] = one_leg[f'{name}Metrics'].cumsum(axis=0) + 1

    one_leg[f'{name}Metrics'] = 1 / one_leg[f'{name}Metrics'] if one_leg[f'{name}Metrics'].iloc[-1] < 0 else one_leg[
        f'{name}Metrics']
    return one_leg
