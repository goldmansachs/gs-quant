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
import datetime as dt
import logging
from typing import Optional

import pandas as pd

import gs_quant.timeseries.measures_reports as ReportMeasures
from gs_quant.api.gs.data import QueryType
from gs_quant.api.gs.portfolios import GsPortfolioApi
from gs_quant.entities.entity import EntityType
from gs_quant.markets.portfolio_manager import PortfolioManager
from gs_quant.timeseries import plot_measure_entity
from gs_quant.timeseries.measures import _extract_series_from_df

LOGGER = logging.getLogger(__name__)


@plot_measure_entity(EntityType.PORTFOLIO, [QueryType.AUM])
def aum(portfolio_id: str, start_date: dt.date = None, end_date: dt.date = None, *,
        source: str = None, real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Returns the Custom AUM uploaded for the portfolio
    :param portfolio_id: id of portfolio
    :param start_date: start date for getting aum
    :param end_date: end date for getting aum
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: portfolio aum values
    """
    data = GsPortfolioApi.get_custom_aum(portfolio_id, start_date, end_date)
    df = pd.DataFrame.from_records(data)
    df.set_index(pd.DatetimeIndex(df['date']), inplace=True)
    return _extract_series_from_df(df, QueryType.AUM, True)


@plot_measure_entity(EntityType.PORTFOLIO, [QueryType.FACTOR_EXPOSURE])
def portfolio_factor_exposure(portfolio_id: str, risk_model_id: str, factor_name: str, unit: str = 'Notional',
                              benchmark_id: str = None, *, source: str = None,
                              real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Factor exposure data associated with a factor in a factor risk report

    :param portfolio_id: portfolio id
    :param risk_model_id: factor risk model id
    :param factor_name: factor name
    :param unit: unit in which the timeseries is returned (Notional or Percent)
    :param benchmark_id: optional benchmark id
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: Timeseries of factor exposure for requested factor
    """
    pm = PortfolioManager(portfolio_id)
    report = pm.get_factor_risk_report(risk_model_id=risk_model_id, benchmark_id=benchmark_id)
    return ReportMeasures.factor_exposure(report.id, factor_name, unit)


@plot_measure_entity(EntityType.PORTFOLIO, [QueryType.FACTOR_PNL])
def portfolio_factor_pnl(portfolio_id: str, risk_model_id: str, factor_name: str, unit: str = 'Notional',
                         benchmark_id: str = None, *, source: str = None,
                         real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Factor PnL data associated with a factor in a factor risk report

    :param portfolio_id: portfolio id
    :param risk_model_id: factor risk model id
    :param factor_name: factor name
    :param unit: unit in which the timeseries is returned (Notional or Percent)
    :param benchmark_id: optional benchmark id
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: Timeseries of factor pnl for requested factor
    """
    pm = PortfolioManager(portfolio_id)
    report = pm.get_factor_risk_report(risk_model_id=risk_model_id, benchmark_id=benchmark_id)
    return ReportMeasures.factor_pnl(report.id, factor_name, unit)


@plot_measure_entity(EntityType.PORTFOLIO, [QueryType.FACTOR_PROPORTION_OF_RISK])
def portfolio_factor_proportion_of_risk(portfolio_id: str, risk_model_id: str, factor_name: str,
                                        benchmark_id: str = None, *, source: str = None,
                                        real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Factor proportion of risk data associated with a factor in a factor risk report

    :param portfolio_id: portfolio id
    :param risk_model_id: factor risk model id
    :param factor_name: factor name
    :param benchmark_id: optional benchmark id
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: Timeseries of factor proportion of risk for requested factor
    """
    pm = PortfolioManager(portfolio_id)
    report = pm.get_factor_risk_report(risk_model_id=risk_model_id, benchmark_id=benchmark_id)
    return ReportMeasures.factor_proportion_of_risk(report.id, factor_name)


@plot_measure_entity(EntityType.PORTFOLIO, [QueryType.DAILY_RISK])
def portfolio_daily_risk(portfolio_id: str, risk_model_id: str, factor_name: str = 'Total',
                         benchmark_id: str = None, *, source: str = None,
                         real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Daily risk data associated with a factor in a factor risk report

    :param portfolio_id: portfolio id
    :param risk_model_id: factor risk model id
    :param factor_name: factor name (must be "Factor", "Specific", or "Total")
    :param benchmark_id: optional benchmark id
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: Timeseries of daily risk for requested factor
    """
    pm = PortfolioManager(portfolio_id)
    report = pm.get_factor_risk_report(risk_model_id=risk_model_id, benchmark_id=benchmark_id)
    return ReportMeasures.daily_risk(report.id, factor_name)


@plot_measure_entity(EntityType.PORTFOLIO, [QueryType.ANNUAL_RISK])
def portfolio_annual_risk(portfolio_id: str, risk_model_id: str, factor_name: str = 'Total',
                          benchmark_id: str = None, *, source: str = None,
                          real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Annual risk data associated with a factor in a factor risk report

    :param portfolio_id: portfolio id
    :param risk_model_id: factor risk model id
    :param factor_name: factor name (must be "Factor", "Specific", or "Total")
    :param benchmark_id: optional benchmark id
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: Timeseries of daily risk for requested factor
    """
    pm = PortfolioManager(portfolio_id)
    report = pm.get_factor_risk_report(risk_model_id=risk_model_id, benchmark_id=benchmark_id)
    return ReportMeasures.annual_risk(report.id, factor_name)


@plot_measure_entity(EntityType.PORTFOLIO, [QueryType.THEMATIC_EXPOSURE])
def portfolio_thematic_exposure(portfolio_id: str, basket_ticker: str, *, source: str = None,
                                real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Thematic exposure of a portfolio to a requested GS thematic flagship basket

    :param portfolio_id: portfolio id
    :param basket_ticker: ticker for thematic basket
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: Timeseries of daily thematic beta of portfolio to requested flagship basket
    """
    pm = PortfolioManager(portfolio_id)
    thematic_report = pm.get_thematic_report()
    return ReportMeasures.thematic_exposure(thematic_report.id, basket_ticker)


@plot_measure_entity(EntityType.PORTFOLIO, [QueryType.PNL])
def portfolio_pnl(portfolio_id: str, unit: str = 'Notional', *, source: str = None,
                  real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    PNL from all holdings, if unit is Percent, geometrically aggregate over time frame

    :param portfolio_id: id of portfolio
    :param unit: by default uses mode as Notional, but can also be set to Percent
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: portfolio pnl
    """
    pm = PortfolioManager(portfolio_id)
    performance_report = pm.get_performance_report()
    return ReportMeasures.pnl(performance_report.id, unit)
