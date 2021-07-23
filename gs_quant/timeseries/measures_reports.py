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

from gs_quant.api.gs.data import QueryType
from gs_quant.data.core import DataContext
from gs_quant.entities.entity import EntityType
from gs_quant.errors import MqValueError, MqError
from gs_quant.markets.factor import Factor
from gs_quant.markets.report import FactorRiskReport, PerformanceReport
from gs_quant.models.risk_model import ReturnFormat
from gs_quant.target.portfolios import RiskAumSource
from gs_quant.timeseries import plot_measure_entity
from gs_quant.timeseries.measures import _extract_series_from_df
from gs_quant.api.gs.portfolios import GsPortfolioApi


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

    :math:`NP_{t} = SUM( PNL_{t}/ ( AUM_{t} ) - cPNL_{t-1) ) if ( AUM_{t} ) - cPNL_{t-1) ) > 0 else:
            1/ SUM( PNL_{t}/ ( AUM_{t} ) - cPNL_{t-1) )`

    This takes into account varying AUM and adjusts for exposure change due to PNL

    where :math:`cPNL_{t-1}` is your performance reports cumulative PNL at date t-1
    where :math:`PNL_{t}` is your performance reports pnl at date t
    where :math:`AUM_{t}` is portfolio exposure on date t


    """
    start_date = DataContext.current.start_time
    end_date = DataContext.current.end_time

    ppa_report = PerformanceReport.get(report_id)
    if not aum_source:
        port = GsPortfolioApi.get_portfolio(ppa_report.position_source_id)
        aum_source = port.aum_source if port.aum_source else RiskAumSource.Net
    else:
        aum_source = RiskAumSource(aum_source)

    aum_col_name = aum_source.value.lower()
    aum_col_name = f'{aum_col_name}Exposure' if aum_col_name != 'custom aum' else 'aum'
    measures = [aum_col_name, 'pnl'] if aum_source != RiskAumSource.Custom_AUM else ['pnl']
    data = ppa_report.get_many_measures(measures, start_date, end_date)
    data.loc[0, 'pnl'] = 0
    data['cumulativePnlT-1'] = data['pnl'].cumsum(axis=0)
    data = pd.DataFrame.from_records(data).set_index(['date'])
    if aum_source == RiskAumSource.Custom_AUM:
        custom_aum = pd.DataFrame(GsPortfolioApi.get_custom_aum(ppa_report.position_source_id, start_date, end_date))
        if custom_aum.empty:
            raise MqError(f'No custom AUM for portfolio {ppa_report.position_source_id} between dates {start_date},'
                          f' {end_date}')
        custom_aum = pd.DataFrame.from_records(custom_aum).set_index(['date'])
        data = data.join(custom_aum.loc[:, aum_col_name], how='inner')
    if aum_source == RiskAumSource.Short:
        data[f'{aum_col_name}'] = -1 * data[f'{aum_col_name}']
    data['normalizedExposure'] = data[f'{aum_col_name}'] - data['cumulativePnlT-1']
    data['pnlOverNormalizedExposure'] = data['pnl'] / data['normalizedExposure']
    data['normalizedPerformance'] = data['pnlOverNormalizedExposure'].cumsum(axis=0) + 1
    data.loc[data.normalizedExposure < 0, 'normalizedPerformance'] = 1 / data.loc[:, 'normalizedPerformance']
    return pd.Series(data['normalizedPerformance'], name="normalizedPerformance").dropna()


def _get_factor_data(report_id: str, factor_name: str, query_type: QueryType) -> pd.Series:
    # Check params
    report = FactorRiskReport.get(report_id)
    risk_model_id = report.get_risk_model_id()
    if factor_name not in ['Factor', 'Specific', 'Total']:
        if query_type in [QueryType.DAILY_RISK, QueryType.ANNUAL_RISK]:
            raise MqValueError('Please pick a factor name from the following: ["Total", "Factor", "Specific"]')
        factor = Factor.get(risk_model_id, factor_name)
        factor_name = factor.name

    # Extract relevant data for each date
    col_name = query_type.value.replace(' ', '')
    col_name = decapitalize(col_name)
    data_type = decapitalize(col_name[6:]) if col_name.startswith('factor') else col_name

    factor_data = report.get_results(
        factors=[factor_name],
        start_date=DataContext.current.start_time,
        end_date=DataContext.current.end_time,
        return_format=ReturnFormat.JSON
    )
    factor_exposures = [{'date': data['date'], col_name: data[data_type]} for data in factor_data
                        if data.get(data_type)]

    # Create and return timeseries
    df = pd.DataFrame(factor_exposures)
    if not df.empty:
        df.set_index('date', inplace=True)
        df.index = pd.to_datetime(df.index)
    return _extract_series_from_df(df, query_type)
