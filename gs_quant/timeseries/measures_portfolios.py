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
from typing import Optional, Union

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
    df = df.set_index(pd.DatetimeIndex(df['date']))
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


@plot_measure_entity(EntityType.PORTFOLIO, [QueryType.HIT_RATE])
def portfolio_hit_rate(portfolio_id: str, rolling_window: Union[int, str], *, source: str = None,
                       real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Create a time series of the hit rate of a portfolio over a given rolling period

    :param portfolio_id: id of portfolio
    :param rolling_window: size of window to use
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: portfolio hit rate
    """
    pm = PortfolioManager(portfolio_id)
    performance_report = pm.get_performance_report()
    return ReportMeasures.hit_rate(performance_report.id, rolling_window)


@plot_measure_entity(EntityType.PORTFOLIO, [QueryType.MAX_DRAWDOWN])
def portfolio_max_drawdown(portfolio_id: str, rolling_window: int, *, source: str = None,
                           real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Create a time series of the max drawdown of a portfolio over a given rolling period

    :param portfolio_id: id of portfolio
    :param rolling_window: size of window to use
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of portfolio hit rate
    """
    pm = PortfolioManager(portfolio_id)
    performance_report = pm.get_performance_report()
    return ReportMeasures.portfolio_max_drawdown(performance_report.id, rolling_window)


@plot_measure_entity(EntityType.PORTFOLIO, [QueryType.MAX_DRAWDOWN])
def portfolio_drawdown_length(portfolio_id: str, rolling_window: Union[int, str], *, source: str = None,
                              real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    The length in days between the peak and the trough of the maximum drawdown

    :param portfolio_id: id of portfolio
    :param rolling_window: size of window to use
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of the drawdown length
    """
    pm = PortfolioManager(portfolio_id)
    performance_report = pm.get_performance_report()
    return ReportMeasures.drawdown_length(performance_report.id, rolling_window)


@plot_measure_entity(EntityType.PORTFOLIO, [QueryType.MAX_DRAWDOWN])
def portfolio_max_recovery_period(portfolio_id: str, rolling_window: Union[int, str], *, source: str = None,
                                  real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    The maximum number of days used to reach a previously broken price level over the stated timeframe.

    :param portfolio_id: id of portfolio
    :param rolling_window: size of window to use
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of max recovery period
    """
    pm = PortfolioManager(portfolio_id)
    performance_report = pm.get_performance_report()
    return ReportMeasures.max_recovery_period(performance_report.id, rolling_window)


@plot_measure_entity(EntityType.PORTFOLIO, [QueryType.STANDARD_DEVIATION])
def portfolio_standard_deviation(portfolio_id: str, rolling_window: Union[int, str], *, source: str = None,
                                 real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Volatility of the total return over the stated time frame.

    :param portfolio_id: id of portfolio
    :param rolling_window: the rolling window to look back on
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of standard deviation
    """
    pm = PortfolioManager(portfolio_id)
    performance_report = pm.get_performance_report()
    return ReportMeasures.standard_deviation(performance_report.id, rolling_window)


@plot_measure_entity(EntityType.PORTFOLIO, [QueryType.DOWNSIDE_RISK])
def portfolio_downside_risk(portfolio_id: str, rolling_window: Union[int, str], *, source: str = None,
                            real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Volatility of the periodic returns that are lower than the mean return over the stated time frame.
    Standard deviation is calculated using all returns, downside risk is calculated using only the returns
    that are below the mean.

    :param portfolio_id: id of portfolio
    :param rolling_window: the rolling window to look back on
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of downside_risk
    """
    pm = PortfolioManager(portfolio_id)
    performance_report = pm.get_performance_report()
    return ReportMeasures.downside_risk(performance_report.id, rolling_window)


@plot_measure_entity(EntityType.PORTFOLIO, [QueryType.DOWNSIDE_RISK])
def portfolio_semi_variance(portfolio_id: str, rolling_window: Union[int, str], *, source: str = None,
                            real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Volatility of the periodic returns that are lower than the mean return over the stated time frame.
    Standard deviation is calculated using all returns, semi variance is calculated using only the returns
    that are below 0.

    :param portfolio_id: id of portfolio
    :param rolling_window: the rolling window to look back on
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of downside_risk
    """
    pm = PortfolioManager(portfolio_id)
    performance_report = pm.get_performance_report()
    return ReportMeasures.semi_variance(performance_report.id, rolling_window)


@plot_measure_entity(EntityType.PORTFOLIO, [QueryType.KURTOSIS])
def portfolio_kurtosis(portfolio_id: str, rolling_window: Union[int, str], *, source: str = None,
                       real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Kurtosis measure the peakedness or flatness of the return distribution over the state time frame.
    In a flat distribution the average value is more likely to occur.

    :param portfolio_id: id of portfolio
    :param rolling_window: the rolling window to look back on
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of kurtosis
    """
    pm = PortfolioManager(portfolio_id)
    performance_report = pm.get_performance_report()
    return ReportMeasures.kurtosis(performance_report.id, rolling_window)


@plot_measure_entity(EntityType.PORTFOLIO, [QueryType.SKEWNESS])
def portfolio_skewness(portfolio_id: str, rolling_window: Union[int, str], *, source: str = None,
                       real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Skewness measures the degree of symmetry of the return distribution over the stated time frame.
    If the left tail is more pronounced than the right tail, it is said the return have negative skewness.

    :param portfolio_id: id of portfolio
    :param rolling_window: the rolling window to look back on
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of skewness
    """
    pm = PortfolioManager(portfolio_id)
    performance_report = pm.get_performance_report()
    return ReportMeasures.skewness(performance_report.id, rolling_window)


@plot_measure_entity(EntityType.PORTFOLIO, [QueryType.REALIZED_VAR])
def portfolio_realized_var(portfolio_id: str, rolling_window: Union[int, str], confidence_interval: float = .95,
                           *, source: str = None, real_time: bool = False,
                           request_id: Optional[str] = None) -> pd.Series:
    """
    The maximum expected loss of the portfolios, calculated using
    the natural distribution of returns over a stated time frame and is based on a confidence level.

    :param portfolio_id: id of portfolio
    :param rolling_window: the rolling window to look back on
    :param confidence_interval: the rolling window to look back on
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of realized var
    """
    pm = PortfolioManager(portfolio_id)

    performance_report = pm.get_performance_report()
    return ReportMeasures.realized_var(performance_report.id, rolling_window, confidence_interval)


@plot_measure_entity(EntityType.PORTFOLIO, [QueryType.TRACKING_ERROR])
def portfolio_tracking_error(portfolio_id: str, benchmark_id: str, rolling_window: Union[int, str], *,
                             source: str = None,
                             real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    The standard deviation of the excess return relative to the benchmark over the state time frame.

    Tracking Error = sqrt( sum((ExcessRi - ExcessRmean)^2) / (N-1) )

    Where:

    ExcessRi = excess return in period i

    ExcessRmean = mean excess return during bull markets

    N = number of periods

    :param portfolio_id: id of portfolio
    :param rolling_window: the rolling window to look back on
    :param benchmark_id: the rolling window to look back on
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of tracking error
    """
    pm = PortfolioManager(portfolio_id)

    performance_report = pm.get_performance_report()
    return ReportMeasures.tracking_error(performance_report.id, benchmark_id, rolling_window)


@plot_measure_entity(EntityType.PORTFOLIO, [QueryType.TRACKING_ERROR_BEAR])
def portfolio_tracking_error_bear(portfolio_id: str, benchmark_id: str, rolling_window: Union[int, str], *,
                                  source: str = None,
                                  real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    The standard deviation of the excess return relative to the benchmark over the state time frame,
    only counting the periods when benchmark returns were negative.

    Bear Tracking Error = sqrt( sum((ExcessRi - ExcessRmeanBear)^2) / (N-1) ) for all when Benchmark Return < 0

    Where:

    ExcessRi = excess return in period i

    ExcessRmeanBear = mean excess return during bull markets

    N = number of periods

    :param portfolio_id: id of portfolio
    :param rolling_window: the rolling window to look back on
    :param benchmark_id: the rolling window to look back on
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of tracking error
    """
    pm = PortfolioManager(portfolio_id)

    performance_report = pm.get_performance_report()
    return ReportMeasures.tracking_error_bear(performance_report.id, benchmark_id, rolling_window)


@plot_measure_entity(EntityType.PORTFOLIO, [QueryType.TRACKING_ERROR_BULL])
def portfolio_tracking_error_bull(portfolio_id: str, benchmark_id: str, rolling_window: Union[int, str], *,
                                  source: str = None,
                                  real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    The standard deviation of the excess return relative to the benchmark over the state time frame,
    only counting the periods when benchmark returns were positive.

    Bull Tracking Error = sqrt( sum((ExcessRi - ExcessRmeanBull)^2) / (N-1) ) for all when Benchmark Return > 0

    Where:

    ExcessRi = excess return in period i

    ExcessRmeanBull = mean excess return during bull markets

    N = number of periods

    :param portfolio_id: id of portfolio
    :param rolling_window: the rolling window to look back on
    :param benchmark_id: the rolling window to look back on
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of tracking error
    """
    pm = PortfolioManager(portfolio_id)

    performance_report = pm.get_performance_report()
    return ReportMeasures.tracking_error_bull(performance_report.id, benchmark_id, rolling_window)


@plot_measure_entity(EntityType.PORTFOLIO, [QueryType.SHARPE_RATIO])
def portfolio_sharpe_ratio(portfolio_id: str, risk_free_id: str, rolling_window: Union[int, str], *,
                           source: str = None,
                           real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Risk-adjusted measure that calculates the excess return over the risk free rate per unit of volatility

    Sharpe Ratio = (Rp - Rf) / σp

    Where:

    Rp = Portfolio Return

    Rf = Risk-Free Rate

    σp = Standard Deviation of Portfolio Return.

    :param portfolio_id: id of portfolio
    :param risk_free_id: id of risk-free asset
    :param rolling_window: size of the rolling window to look back on
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of sharpe ratio
    """
    pm = PortfolioManager(portfolio_id)

    performance_report = pm.get_performance_report()
    return ReportMeasures.portfolio_sharpe_ratio(performance_report.id, risk_free_id, rolling_window)


@plot_measure_entity(EntityType.PORTFOLIO, [QueryType.CALMAR_RATIO])
def portfolio_calmar_ratio(portfolio_id: str, rolling_window: Union[int, str], *,
                           source: str = None,
                           real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Risk-adjusted performance metric that divides an investment strategy’s
    annualized rate of return by its maximum drawdown, focusing specifically
    on the strategy’s return per unit of downside risk.

    Calmar Ratio = Annualized Return / Max Drawdown

    :param portfolio_id: id of portfolio
    :param rolling_window: size of the rolling window to look back on
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of calmar ratio
    """
    pm = PortfolioManager(portfolio_id)

    performance_report = pm.get_performance_report()
    return ReportMeasures.calmar_ratio(performance_report.id, rolling_window)


@plot_measure_entity(EntityType.PORTFOLIO, [QueryType.SORTINO_RATIO])
def portfolio_sortino_ratio(portfolio_id: str, comparison_id: str, rolling_window: Union[int, str], *,
                            source: str = None,
                            real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Risk-adjusted measure that calculates the excess return over the benchmark per unit of semi-variance

    Sortino Ratio = (Rp - Rb) / Downside Deviation

    Where:

    Rp = Portfolio Return

    Rb = Benchmark Return

    Downside Deviation = Standard Deviation of negative asset returns.

    :param portfolio_id: id of portfolio
    :param comparison_id: id of security to compare to
    :param rolling_window: size of the rolling window to look back on
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of the sortino ratio
    """
    pm = PortfolioManager(portfolio_id)

    performance_report = pm.get_performance_report()
    return ReportMeasures.sortino_ratio(performance_report.id, comparison_id, rolling_window)


@plot_measure_entity(EntityType.PORTFOLIO, [QueryType.INFORMATION_RATIO])
def portfolio_information_ratio(portfolio_id: str, benchmark_id: str, *,
                                source: str = None,
                                real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Risk-adjusted measure that calculates the excess return over the benchmark,
    per unit of tracking error volatility. It measures the consistency with
    which the portfolio is beating the benchmark.

    Information Ratio = (Rp - Rb) / Tracking Error

    Where:

    Rp = Portfolio Return

    Rb = Benchmark Return

    Tracking Error = Standard Deviation of the difference between the portfolio and benchmark returns.

    :param portfolio_id: id of portfolio
    :param benchmark_id: id of benchmark asset
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of the information ratio
    """
    pm = PortfolioManager(portfolio_id)

    performance_report = pm.get_performance_report()
    return ReportMeasures.information_ratio(performance_report.id, benchmark_id)


@plot_measure_entity(EntityType.PORTFOLIO, [QueryType.INFORMATION_RATIO])
def portfolio_information_ratio_bull(portfolio_id: str, benchmark_id: str, *,
                                     source: str = None,
                                     real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Risk-adjusted measure that calculates the excess return over the benchmark,
    per unit of tracking error volatility, counting only the periods when the benchmark return was positive.

    Information Ratio = (Rp - Rb) / Tracking Error

    Where:

    Rp = Portfolio Return

    Rb = Benchmark Return

    Tracking Error = Standard Deviation of the difference between the portfolio and benchmark returns.

    :param portfolio_id: id of portfolio
    :param benchmark_id: id of benchmark asset
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of the information ratio
    """
    pm = PortfolioManager(portfolio_id)

    performance_report = pm.get_performance_report()
    return ReportMeasures.information_ratio_bull(performance_report.id, benchmark_id)


@plot_measure_entity(EntityType.PORTFOLIO, [QueryType.INFORMATION_RATIO])
def portfolio_information_ratio_bear(portfolio_id: str, benchmark_id: str, *,
                                     source: str = None,
                                     real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Risk-adjusted measure that calculates the excess return over the benchmark,
    per unit of tracking error volatility, counting only the periods when the benchmark return was negative


    Information Ratio = (Rp - Rb) / Tracking Error

    Where:

    Rp = Portfolio Return

    Rb = Benchmark Return

    Tracking Error = Standard Deviation of the difference between the portfolio and benchmark returns.


    :param portfolio_id: id of portfolio
    :param benchmark_id: id of benchmark asset
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of the information ratio
    """
    pm = PortfolioManager(portfolio_id)

    performance_report = pm.get_performance_report()
    return ReportMeasures.information_ratio_bear(performance_report.id, benchmark_id)


@plot_measure_entity(EntityType.PORTFOLIO, [QueryType.MODIGLIANI_RATIO])
def portfolio_modigliani_ratio(portfolio_id: str, benchmark_id: str, risk_free_id: str,
                               rolling_window: Union[int, str], *,
                               source: str = None,
                               real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Modigliani RAP measures how much the portfolio would have returns if it had had
    the same risk as the benchmark. It is a linear transformation of the Sharpe Ratio,
    but the results are expressed in terms of performance.

    M2 = (Sharpe Ratio * σb) + Rf

    Where:

    Sharpe Ratio = Portfolio Sharpe Ratio

    σb = Standard Deviation of the Benchmark Return

    Rf = Risk Free Rate.

    :param portfolio_id: id of portfolio
    :param benchmark_id: id of benchmark asset
    :param risk_free_id: id of risk free asset
    :param rolling_window: size of window to use
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of the modigliani ratio
    """
    pm = PortfolioManager(portfolio_id)

    performance_report = pm.get_performance_report()
    return ReportMeasures.modigliani_ratio(performance_report.id, benchmark_id, risk_free_id, rolling_window)


@plot_measure_entity(EntityType.PORTFOLIO, [QueryType.TREYNOR_RATIO])
def portfolio_treynor_measure(portfolio_id: str, risk_free_id: str, benchmark_id: str, *,
                              source: str = None,
                              real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Risk-adjusted measure that calculates the excess return over the risk free rate
    per unit of beta relative to the benchmark. This is useful for assessing the excess
    return from each unit of systematic risk.

    Treynor Ratio = (Rp - Rf) / Beta

    Where:

    Rp = Portfolio Return

    Rf = Risk-Free Rate

    Beta = Portfolio Beta

    :param portfolio_id: id of portfolio
    :param risk_free_id: id of risk-free asset
    :param benchmark_id: id of benchmark asset
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of the treynor measure
    """
    pm = PortfolioManager(portfolio_id)

    performance_report = pm.get_performance_report()
    return ReportMeasures.treynor_measure(performance_report.id, risk_free_id, benchmark_id)


def portfolio_jensen_alpha(portfolio_id: str, benchmark_id: str, risk_free_id: str, *,
                           source: str = None,
                           real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Risk-Adjusted measure that calculates the actual return of the portfolio
    over and above the return predicted by the CAPM, given the portfolios beta
    and benchmark returns.

    Jensen's Alpha = Rp - [Rf + Beta * (Rb - Rf)]

    Where:

    Rp = Portfolio Return

    Rf = Risk-Free Rate

    Beta = Portfolio Beta

    Rb = Benchmark Return

    :param portfolio_id: id of portfolio
    :param risk_free_id: id of risk-free asset
    :param benchmark_id: id of benchmark asset
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of jensen alpha
    """
    pm = PortfolioManager(portfolio_id)

    performance_report = pm.get_performance_report()
    return ReportMeasures.jensen_alpha(performance_report.id, benchmark_id, risk_free_id)


def portfolio_jensen_alpha_bear(portfolio_id: str, benchmark_id: str, risk_free_id: str, *,
                                source: str = None,
                                real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Risk-Adjusted measure that calculates the actual return of the portfolio
    over and above the return predicted by the CAPM, given the portfolios beta
    and benchmark returns. calculated based only on the periods when the benchmark return was negative

    Jensen's Alpha = Rp - [Rf + Beta * (Rb - Rf)]

    Where:

    Rp = Portfolio Return

    Rf = Risk-Free Rate

    Beta = Portfolio Beta

    Rb = Benchmark Return

    :param portfolio_id: id of portfolio
    :param risk_free_id: id of risk-free asset
    :param benchmark_id: id of benchmark asset
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of jensen alpha
    """
    pm = PortfolioManager(portfolio_id)

    performance_report = pm.get_performance_report()
    return ReportMeasures.jensen_alpha_bear(performance_report.id, benchmark_id, risk_free_id)


def portfolio_jensen_alpha_bull(portfolio_id: str, benchmark_id: str, risk_free_id: str, *,
                                source: str = None,
                                real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Risk-Adjusted measure that calculates the actual return of the portfolio
    over and above the return predicted by the CAPM, given the portfolios beta
    and benchmark returns. calculated based only on the periods when the benchmark return was positive

    Jensen's Alpha = Rp - [Rf + Beta * (Rb - Rf)]

    Where:

    Rp = Portfolio Return

    Rf = Risk-Free Rate

    Beta = Portfolio Beta

    Rb = Benchmark Return

    :param portfolio_id: id of portfolio
    :param risk_free_id: id of risk-free asset
    :param benchmark_id: id of benchmark asset
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of jensen alpha
    """
    pm = PortfolioManager(portfolio_id)

    performance_report = pm.get_performance_report()
    return ReportMeasures.jensen_alpha_bull(performance_report.id, benchmark_id, risk_free_id)


@plot_measure_entity(EntityType.PORTFOLIO, [QueryType.ALPHA])
def portfolio_alpha(portfolio_id: str, benchmark_id: str, rolling_window: Union[int, str], *,
                    source: str = None,
                    real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    This is the intercept from a regression analysis, where the portfolio's returns are regressed
    against the benchmark's returns. It represents the portion of the portfolio's return that is
    not explained by the benchmark's performance

    :param portfolio_id: id of portfolio
    :param rolling_window: size of the rolling window to look back on
    :param benchmark_id: id of benchmark asset
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of the beta
    """
    pm = PortfolioManager(portfolio_id)

    performance_report = pm.get_performance_report()
    return ReportMeasures.alpha(performance_report.id, benchmark_id, rolling_window)


@plot_measure_entity(EntityType.PORTFOLIO, [QueryType.BETA])
def portfolio_beta(portfolio_id: str, benchmark_id: str, rolling_window: Union[int, str], *,
                   source: str = None,
                   real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Beta defined as the slope of the regression between report pnl and benchmark pnl

    :param portfolio_id: id of portfolio
    :param rolling_window: size of the rolling window to look back on
    :param benchmark_id: id of benchmark asset
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of the beta
    """
    pm = PortfolioManager(portfolio_id)

    performance_report = pm.get_performance_report()
    return ReportMeasures.portfolio_beta(performance_report.id, benchmark_id, rolling_window)


@plot_measure_entity(EntityType.PORTFOLIO, [QueryType.CORRELATION])
def portfolio_correlation(portfolio_id: str, benchmark_id: str, rolling_window: Union[int, str], *,
                          source: str = None,
                          real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Correlation coefficient between the portfolio and the benchmark returns over the stated time frame

    :param portfolio_id: id of portfolio
    :param rolling_window: size of the rolling window to look back on
    :param benchmark_id: id of benchmark asset
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of the correlation coefficient
    """
    pm = PortfolioManager(portfolio_id)

    performance_report = pm.get_performance_report()
    return ReportMeasures.portfolio_correlation(performance_report.id, benchmark_id, rolling_window)


@plot_measure_entity(EntityType.PORTFOLIO, [QueryType.R_SQUARED])
def portfolio_r_squared(portfolio_id: str, benchmark_id: str, rolling_window: Union[int, str], *,
                        source: str = None,
                        real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    A measure of how well the portfolio's performance correlates with the performance of the benchmark,
    and thus a measure of what portion of its performance may be explained by the performance of the benchmark.

    :param portfolio_id: id of portfolio
    :param rolling_window: size of the rolling window to look back on
    :param benchmark_id: id of benchmark asset
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: portfolio r squared
    """
    pm = PortfolioManager(portfolio_id)

    performance_report = pm.get_performance_report()
    return ReportMeasures.r_squared(performance_report.id, benchmark_id, rolling_window)


@plot_measure_entity(EntityType.PORTFOLIO, [QueryType.CAPTURE_RATIO])
def portfolio_capture_ratio(portfolio_id: str, benchmark_id: str, rolling_window: Union[int, str], *,
                            source: str = None,
                            real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    A measure of how well portfolio is doing relative to the benchmark,
    defined as the ratio of the portfolio return to the benchmark return calculated
    on a daily basis and averaged over the stated time period.

    :param portfolio_id: id of portfolio
    :param benchmark_id: id of benchmark asset
    :param rolling_window: size of the rolling window to look back on
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: portfolio capture ratio
    """
    pm = PortfolioManager(portfolio_id)

    performance_report = pm.get_performance_report()
    return ReportMeasures.capture_ratio(performance_report.id, benchmark_id, rolling_window)
