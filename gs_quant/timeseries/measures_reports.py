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
import re
from enum import Enum
from typing import Optional, Union, List

import pandas as pd
import numpy as np
import math
import scipy.stats as stats
from pandas.tseries.offsets import BDay
from pydash import decapitalize

from gs_quant.api.gs.data import QueryType, GsDataApi, DataQuery
from gs_quant.data import DataMeasure
from gs_quant.data.core import DataContext
from gs_quant.entities.entity import EntityType
from gs_quant.errors import MqValueError
from gs_quant.markets.portfolio_manager import PortfolioManager
from gs_quant.markets.report import FactorRiskReport, PerformanceReport, ThematicReport, ReturnFormat, \
    format_aum_for_return_calculation, get_pnl_percent, get_factor_pnl_percent_for_single_factor
from gs_quant.markets.securities import Bond
from gs_quant.models.risk_model import FactorRiskModel
from gs_quant.target.reports import PositionSourceType
from gs_quant.timeseries import plot_measure_entity, beta, correlation, max_drawdown
from gs_quant.timeseries.algebra import geometrically_aggregate
from gs_quant.timeseries.measures import _extract_series_from_df, SecurityMaster, AssetIdentifier


class Unit(Enum):
    NOTIONAL = 'Notional'
    PERCENT = 'Percent'


@plot_measure_entity(EntityType.REPORT, [QueryType.FACTOR_EXPOSURE])
def factor_exposure(report_id: str, factor_name: str, unit: str = 'Notional', *, source: str = None,
                    real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Factor exposure data associated with a factor in a factor risk report

    :param report_id: factor risk report id
    :param factor_name: factor name
    :param unit: unit in which the timeseries is returned (Notional or Percent)
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: Timeseries of factor exposure for requested factor
    """
    return _get_factor_data(report_id, factor_name, QueryType.FACTOR_EXPOSURE, Unit(unit))


@plot_measure_entity(EntityType.REPORT, [QueryType.FACTOR_PNL])
def factor_pnl(report_id: str, factor_name: str, unit: str = 'Notional', *, source: str = None,
               real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Factor PnL data associated with a factor in a factor risk report

    :param report_id: factor risk report id
    :param factor_name: factor name
    :param unit: unit in which the timeseries is returned (Notional or Percent)
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: Timeseries of factor pnl for requested factor
    """
    return _get_factor_data(report_id, factor_name, QueryType.FACTOR_PNL, Unit(unit))


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
def normalized_performance(report_id: str, leg: str = None, *, source: str = None,
                           real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Returns the Normalized Performance of a performance report based on AUM source
    :param report_id: id of performance report
    :param leg: short or long
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: portfolio normalized performance

    **Usage**

    Returns the normalized performance of the portfolio.

    :math:`NP(L/S)_{t} = SUM( PNL(L/S)_{t}/ ( EXP(L/S)_{t} ) - cPNL(L/S)_{t-1) )
        if ( EXP(L/S)_{t} ) > 0
        else:
            1/ SUM( PNL(L/S)_{t}/ ( EXP(L/S)_{t} ) - cPNL(L/S)_{t-1) )`
    For each leg, short and long, then:
    :math:`NP_{t} = NP(L)_{t} * SUM(EXP(L)) / SUM(GROSS_EXP) + NP(S)_{t} * SUM(EXP(S)) / SUM(GROSS_EXP) + 1`

    If leg is short, set SUM(EXP(L)) to 0, if leg is long, set SUM(EXP(S)) to 0

    where :math:`cPNL(L/S)_{t-1}` is your performance reports cumulative long or short PNL at date t-1
    where :math:`PNL(L/S)_{t}` is your performance reports long or short pnl at date t
    where :math:`GROSS_EXP_{t}` is portfolio gross exposure on date t
    where :math:`EXP(L/S)_{t}` is the long or short exposure on date t

    """
    start_date = DataContext.current.start_time
    end_date = DataContext.current.end_time

    start_date = (start_date - BDay(1)).date()
    end_date = end_date.date()

    performance_report = PerformanceReport.get(report_id)

    constituent_data = performance_report.get_portfolio_constituents(
        fields=['assetId', 'pnl', 'quantity', 'netExposure'], start_date=start_date, end_date=end_date).set_index(
        'date')

    if leg:
        if leg.lower() == "long":
            constituent_data = constituent_data[constituent_data['quantity'] > 0]
        if leg.lower() == "short":
            constituent_data = constituent_data[constituent_data['quantity'] < 0]

    # Split into long and short and aggregate across dates
    long_side = _return_metrics(constituent_data[constituent_data['quantity'] > 0],
                                list(constituent_data.index.unique()), "long")
    short_side = _return_metrics(constituent_data[constituent_data['quantity'] < 0],
                                 list(constituent_data.index.unique()), "short")

    short_exposure = sum(abs(short_side['exposure']))
    long_exposure = sum(long_side['exposure'])
    gross_exposure = short_exposure + long_exposure

    long_side['longRetWeighted'] = (long_side['longMetrics'] - 1) * (long_exposure / gross_exposure)
    short_side['shortRetWeighted'] = (short_side['shortMetrics'] - 1) * (short_exposure / gross_exposure)

    combined = long_side[['longRetWeighted']].join(short_side[['shortRetWeighted']], how='inner')
    combined['normalizedPerformance'] = combined['longRetWeighted'] + combined['shortRetWeighted'] + 1
    return pd.Series(combined['normalizedPerformance'], name="normalizedPerformance").dropna()


@plot_measure_entity(EntityType.REPORT, [QueryType.PNL])
def long_pnl(report_id: str, *, source: str = None,
             real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    PNL from long holdings

    :param report_id: id of performance report
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: portfolio long pnl
    """
    start_date = DataContext.current.start_time.date()
    end_date = DataContext.current.end_time.date()
    performance_report = PerformanceReport.get(report_id)

    constituent_data = performance_report.get_portfolio_constituents(
        fields=['pnl', 'quantity'], start_date=start_date, end_date=end_date).set_index('date')
    long_leg = constituent_data[constituent_data['quantity'] > 0]['pnl']
    long_leg = long_leg.groupby(level=0).sum()
    return pd.Series(long_leg, name="longPnl")


@plot_measure_entity(EntityType.REPORT, [QueryType.PNL])
def short_pnl(report_id: str, *, source: str = None,
              real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """

    PNL from short holdings
    :param report_id: id of performance report
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: portfolio short pnl
    """
    start_date = DataContext.current.start_time.date()
    end_date = DataContext.current.end_time.date()
    performance_report = PerformanceReport.get(report_id)

    constituent_data = performance_report.get_portfolio_constituents(
        fields=['pnl', 'quantity'], start_date=start_date, end_date=end_date).set_index('date')
    short_leg = constituent_data[constituent_data['quantity'] < 0]['pnl']
    short_leg = short_leg.groupby(level=0).sum()
    return pd.Series(short_leg, name="shortPnl")


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
        df = df.set_index('date')
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
        df = df.set_index('date')
        df.index = pd.to_datetime(df.index)
    return _extract_series_from_df(df, QueryType.THEMATIC_BETA)


@plot_measure_entity(EntityType.REPORT, [QueryType.AUM])
def aum(report_id: str, *, source: str = None,
        real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    AUM of the portfolio

    :param report_id: id of performance report
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: portfolio long pnl
    """
    start_date = DataContext.current.start_time.date()
    end_date = DataContext.current.end_time.date()
    performance_report = PerformanceReport.get(report_id)
    aum_curve = performance_report.get_aum(start_date=start_date, end_date=end_date)
    aum_dict = [{'date': key, 'aum': aum_curve[key]} for key in aum_curve]

    # Create and return timeseries
    df = pd.DataFrame(aum_dict)
    if not df.empty:
        df = df.set_index('date')
        df.index = pd.to_datetime(df.index)
    return _extract_series_from_df(df, QueryType.AUM)


@plot_measure_entity(EntityType.REPORT, [QueryType.PNL])
def pnl(report_id: str, unit: str = 'Notional', *, source: str = None,
        real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    PNL from all holdings, if unit is Percent, geometrically aggregate over time frame

    :param report_id: id of performance report
    :param unit: by default uses mode as Notional, but can also be set to Percent
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: portfolio pnl
    """
    start_date = DataContext.current.start_time.date()
    end_date = DataContext.current.end_time.date()
    performance_report = PerformanceReport.get(report_id)
    pnl_df = performance_report.get_pnl(start_date, end_date)

    if unit == Unit.PERCENT.value:
        return get_pnl_percent(performance_report, pnl_df, 'pnl', start_date, end_date)
    else:
        pnl_df = pnl_df.set_index('date')
        return pd.Series(pnl_df['pnl'], name="pnl")


@plot_measure_entity(EntityType.REPORT)
def historical_simulation_estimated_pnl(report_id: str, *, source: str = None,
                                        real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Estimated Pnl from replaying a historical simulation scenario on your latest positions
    :param report_id: id of performance report
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: portfolio estimated pnl
    """

    factor_attributed_pnl = _replay_historical_factor_moves_on_latest_positions(report_id, [])
    total_factor_attributed_pnl = factor_attributed_pnl.apply(np.sum, axis=1).to_frame("estimatedPnl")

    total_factor_attributed_pnl.index = pd.to_datetime(total_factor_attributed_pnl.index)
    return total_factor_attributed_pnl.squeeze()


@plot_measure_entity(EntityType.REPORT)
def historical_simulation_estimated_factor_attribution(report_id: str, factor_name: str, *, source: str = None,
                                                       real_time: bool = False,
                                                       request_id: Optional[str] = None) -> pd.Series:
    """
    Estimated Pnl attributed to the factor after replaying a historical simulation scenario on a portfolio's latest
    positions
    :param report_id: id of performance report
    :param factor_name: name of the factor
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: portfolio estimated pnl
    """

    factor_attributed_pnl = _replay_historical_factor_moves_on_latest_positions(report_id, [factor_name])
    factor_attributed_pnl.index = pd.to_datetime(factor_attributed_pnl.index)

    return factor_attributed_pnl.squeeze()


@plot_measure_entity(EntityType.REPORT)
def hit_rate(report_id: str, rolling_window: Union[int, str], *, source: str = None,
             real_time: bool = False,
             request_id: Optional[str] = None) -> pd.Series:
    """
    The hit rate of a portfolio is a percentage of positions that have generated positive returns over a given period.

    :param report_id: id of performance report
    :param rolling_window: size of rolling window
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of the hit rate
    """
    start_date = DataContext.current.start_time.date()
    end_date = DataContext.current.end_time.date()
    performance_report = PerformanceReport.get(report_id)
    window = _parse_window(rolling_window)
    portfolio_constituents = performance_report.get_portfolio_constituents(fields=['date', 'pnl'],
                                                                           start_date=start_date,
                                                                           end_date=end_date).set_index('date')

    portfolio_constituents = portfolio_constituents[portfolio_constituents['entryType'] == 'Holding']
    portfolio_constituents = portfolio_constituents.sort_values('date')
    pivot_constituents = portfolio_constituents.pivot_table(index='date', columns='assetId', values='pnl')

    rolling_compound = (pivot_constituents).rolling(window=window).sum()
    positive_count = (rolling_compound > 0).sum(axis=1)
    valid_assets = rolling_compound.count(axis=1)

    return positive_count / valid_assets


@plot_measure_entity(EntityType.REPORT)
def portfolio_max_drawdown(report_id: str, rolling_window: Union[int, str], *,
                           source: str = None,
                           real_time: bool = False,
                           request_id: Optional[str] = None) -> pd.Series:
    """
    The largest drop from peak to trough in a sub-period over the stated timeframe

    :param report_id: id of performance report
    :param rolling_window: size of rolling window
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: portfolio estimated pnl
    """
    aum_series = aum(report_id)
    rolling_window = _parse_window(rolling_window)
    max_drawdown_series = aum_series.rolling(window=rolling_window).apply(_max_drawdown, raw=False)

    return max_drawdown_series


@plot_measure_entity(EntityType.REPORT)
def drawdown_length(report_id: str, rolling_window: Union[int, str], *,
                    source: str = None,
                    real_time: bool = False,
                    request_id: Optional[str] = None) -> pd.Series:
    """
    The length in days between the peak and the trough of the maximum drawdown

    :param report_id: id of performance report
    :param rolling_window: size of rolling window
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of the drawdown length
    """
    aum_series = aum(report_id)
    rolling_window = _parse_window(rolling_window)
    drawdown_length_series = aum_series.rolling(window=rolling_window).apply(_drawdown_length, raw=False)

    return drawdown_length_series


@plot_measure_entity(EntityType.REPORT)
def max_recovery_period(report_id: str, rolling_window: Union[int, str], *,
                        source: str = None,
                        real_time: bool = False,
                        request_id: Optional[str] = None) -> pd.Series:
    """
    The maximum number of days used to reach a previously broken price level over the stated timeframe.

    :param report_id: id of performance report
    :param rolling_window: size of rolling window
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of max recovery period
    """
    aum_series = aum(report_id)
    rolling_window = _parse_window(rolling_window)
    recovery_period_series = aum_series.rolling(window=rolling_window).apply(_max_recovery_period, raw=False)

    return recovery_period_series


def _max_recovery_period(series):
    peak = series[0]
    recovery_periods = []
    current_drawdown = 0
    in_drawdown = False

    for val in series[1:]:
        if val < peak:
            in_drawdown = True
            current_drawdown += 1
        else:
            if in_drawdown:
                recovery_periods.append(current_drawdown)
                in_drawdown = False
            peak = val
            current_drawdown = 0
    return max(recovery_periods) if recovery_periods else 0


def _drawdown_length(series):
    peak = series[0]
    drawdown_start = None
    max_drawdown_length = 0
    current_length = 0

    for value in series:
        if value >= peak:
            # Reset when a new peak is found
            peak = value
            drawdown_start = None
            current_length = 0
        else:
            # Track the drawdown length
            if drawdown_start is None:
                drawdown_start = value
            current_length += 1
            max_drawdown_length = max(max_drawdown_length, current_length)

    return max_drawdown_length


@plot_measure_entity(EntityType.REPORT)
def standard_deviation(report_id: str, rolling_window: Union[int, str], *, source: str = None,
                       real_time: bool = False,
                       request_id: Optional[str] = None) -> pd.Series:
    """
    Volatility of the total return over the stated time frame.

    :param report_id: id of performance report
    :param rolling_window: length of window
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of standard deviation
    """
    portfolio_pnl = _get_daily_pnl(report_id)

    rolling_window = _parse_window(rolling_window)
    rolling_std = portfolio_pnl.rolling(window=rolling_window).std()

    return rolling_std


@plot_measure_entity(EntityType.REPORT)
def downside_risk(report_id: str, rolling_window: Union[int, str], *, source: str = None,
                  real_time: bool = False,
                  request_id: Optional[str] = None) -> pd.Series:
    """
    Volatility of the periodic returns that are lower than the mean return over the stated time frame.
    Standard deviation is calculated using all returns, downside risk is calculated using only the returns
    that are below the mean.

    :param report_id: id of performance report
    :param rolling_window: length of window
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of downside_risk
    """
    portfolio_pnl = _get_daily_pnl(report_id)
    rolling_window = _parse_window(rolling_window)
    downside_risk_series = portfolio_pnl.rolling(window=rolling_window).apply(_rolling_downside_risk, raw=False)

    return downside_risk_series


@plot_measure_entity(EntityType.REPORT)
def semi_variance(report_id: str, rolling_window: Union[int, str], *, source: str = None,
                  real_time: bool = False,
                  request_id: Optional[str] = None) -> pd.Series:
    """
    Volatility of the periodic returns that are lower than the mean return over the stated time frame.
    Standard deviation is calculated using all returns, semi variance is calculated using only the returns
    that are below 0.

    :param report_id: id of performance report
    :param rolling_window: length of window
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of downside_risk
    """
    portfolio_pnl = _get_daily_pnl(report_id)
    rolling_window = _parse_window(rolling_window)
    semi_variance_series = portfolio_pnl.rolling(window=rolling_window).apply(_rolling_semi_variance, raw=False)

    return semi_variance_series


@plot_measure_entity(EntityType.REPORT)
def kurtosis(report_id: str, rolling_window: Union[int, str], *, source: str = None,
             real_time: bool = False,
             request_id: Optional[str] = None) -> pd.Series:
    """
    Kurtosis measure the peakedness or flatness of the return distribution over the state time frame.
    In a flat distribution the average value is more likely to occur.


    :param report_id: id of performance report
    :param rolling_window: length of window
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of kurtosis
    """
    portfolio_pnl = _get_daily_pnl(report_id)
    rolling_window = _parse_window(rolling_window)
    rolling_kurtosis = portfolio_pnl.rolling(window=rolling_window).apply(
        lambda x: stats.kurtosis(x, fisher=True, bias=False),
        raw=False
    )

    return rolling_kurtosis


@plot_measure_entity(EntityType.REPORT)
def skewness(report_id: str, rolling_window: Union[int, str], *, source: str = None,
             real_time: bool = False,
             request_id: Optional[str] = None) -> pd.Series:
    """
    Skewness measures the degree of symmetry of the return distribution over the stated time frame.
    If the left tail is more pronounced than the right tail, it is said the return have negative skewness.

    :param report_id: id of performance report
    :param rolling_window: length of window
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of skewness
    """
    portfolio_pnl = _get_daily_pnl(report_id)
    rolling_window = _parse_window(rolling_window)
    rolling_skewness = portfolio_pnl.rolling(window=rolling_window).apply(
        lambda x: stats.skew(x, bias=False),
        raw=False
    )

    return rolling_skewness


@plot_measure_entity(EntityType.REPORT)
def realized_var(report_id: str, rolling_window: Union[int, str],
                 confidence_interval: float = .95, *, source: str = None,
                 real_time: bool = False,
                 request_id: Optional[str] = None) -> pd.Series:
    """
    The maximum expected loss of the portfolios, calculated using
    the natural distribution of returns over a stated time frame and is based on a confidence level.

    :param report_id: id of performance report
    :param rolling_window: length of window
    :param confidence_interval: confidence interval for variance
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of realized var
    """
    portfolio_pnl = _get_daily_pnl(report_id)
    rolling_window = _parse_window(rolling_window)
    realized_variance = portfolio_pnl.rolling(window=rolling_window).quantile(1 - confidence_interval)
    realized_variance = realized_variance * -1

    return realized_variance


@plot_measure_entity(EntityType.REPORT)
def tracking_error(report_id: str, benchmark_id: str, rolling_window: Union[int, str],
                   *, source: str = None,
                   real_time: bool = False,
                   request_id: Optional[str] = None) -> pd.Series:
    """
    The standard deviation of the excess return relative to the benchmark over the state time frame.

    Tracking Error = sqrt( sum((ExcessRi - ExcessRmean)^2) / (N-1) )

    Where:

    ExcessRi = excess return in period i

    ExcessRmean = mean excess return during bull markets

    N = number of periods

    :param report_id: id of performance report
    :param rolling_window: length of window
    :param benchmark_id: id of benchmark
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of tracking error
    """
    start_date = DataContext.current.start_time.date()
    end_date = DataContext.current.end_time.date()
    rolling_window = _parse_window(rolling_window)
    benchmark_returns = _get_benchmark_daily_return(benchmark_id, start_date, end_date)
    portfolio_returns = _get_daily_pnl(report_id)
    active_return = (portfolio_returns - benchmark_returns)
    rolling_error = active_return.rolling(window=rolling_window).std()
    return rolling_error


@plot_measure_entity(EntityType.REPORT)
def tracking_error_bear(report_id: str, benchmark_id: str, rolling_window: Union[int, str], *,
                        source: str = None,
                        real_time: bool = False,
                        request_id: Optional[str] = None) -> pd.Series:
    """
    The standard deviation of the excess return relative to the benchmark over the state time frame,
    only counting the periods when benchmark returns were negative.

    Bear Tracking Error = sqrt( sum((ExcessRi - ExcessRmeanBear)^2) / (N-1) ) for all when Benchmark Return < 0

    Where:

    ExcessRi = excess return in period i

    ExcessRmeanBear = mean excess return during bull markets

    N = number of periods

    :param report_id: id of performance report
    :param rolling_window: length of window
    :param benchmark_id: id of benchmark
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of tracking error
    """
    start_date = DataContext.current.start_time.date()
    end_date = DataContext.current.end_time.date()
    rolling_window = _parse_window(rolling_window)
    benchmark_returns = _get_benchmark_return(benchmark_id, start_date, end_date)
    portfolio_returns = _get_daily_pnl(report_id)
    is_bear = benchmark_returns <= 0
    active_return = portfolio_returns - benchmark_returns
    rolling_error_bear = active_return.rolling(window=rolling_window).apply(
        lambda x: np.std(x, ddof=1) if is_bear.loc[x.index[-1]]
        else np.nan,
        raw=False
    )
    return rolling_error_bear


@plot_measure_entity(EntityType.REPORT)
def tracking_error_bull(report_id: str, benchmark_id: str, rolling_window: Union[int, str], *,
                        source: str = None,
                        real_time: bool = False,
                        request_id: Optional[str] = None) -> pd.Series:
    """
    The standard deviation of the excess return relative to the benchmark over the state time frame,
    only counting the periods when benchmark returns were positive.

    Bull Tracking Error = sqrt( sum((ExcessRi - ExcessRmeanBull)^2) / (N-1) ) for all when Benchmark Return > 0

    Where:

    ExcessRi = excess return in period i

    ExcessRmeanBull = mean excess return during bull markets

    N = number of periods

    :param report_id: id of performance report
    :param rolling_window: length of window
    :param benchmark_id: id of benchmark
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of tracking error
    """
    start_date = DataContext.current.start_time.date()
    end_date = DataContext.current.end_time.date()
    rolling_window = _parse_window(rolling_window)
    benchmark_returns = _get_benchmark_return(benchmark_id, start_date, end_date)
    portfolio_pnl = _get_daily_pnl(report_id)
    is_bull = benchmark_returns > 0
    active_return = portfolio_pnl - benchmark_returns
    rolling_error_bull = active_return.rolling(window=rolling_window).apply(
        lambda x: np.std(x, ddof=1) if is_bull.loc[x.index[-1]]
        else np.nan,
        raw=False
    )
    return rolling_error_bull


@plot_measure_entity(EntityType.REPORT)
def portfolio_sharpe_ratio(report_id: str, risk_free_id: str, rolling_window: Union[int, str], *, source: str = None,
                           real_time: bool = False,
                           request_id: Optional[str] = None) -> pd.Series:
    """
    Risk-adjusted measure that calculates the excess return over the risk free rate per unit of volatility

    Sharpe Ratio = (Rp - Rf) / σp

    Where:

    Rp = Portfolio Return

    Rf = Risk-Free Rate

    σp = Standard Deviation of Portfolio Return.

    :param report_id: id of performance report
    :param risk_free_id: id of risk-free asset
    :param rolling_window: length of window
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of sharpe ratio
    """
    start_date = DataContext.current.start_time.date()
    end_date = DataContext.current.end_time.date()
    window = _parse_window(rolling_window)
    portfolio_pnl = _get_daily_pnl(report_id)
    risk_free_rate_daily = (1 + _get_risk_free_rate(risk_free_id, start_date, end_date)) ** (1 / 252) - 1

    daily_excess = (portfolio_pnl - risk_free_rate_daily).dropna()
    rolling_mean = daily_excess.rolling(window).mean()
    rolling_std = daily_excess.rolling(window).std()

    portfolio_sharpe_ratio_series = (rolling_mean / rolling_std) * np.sqrt(252)
    return portfolio_sharpe_ratio_series


@plot_measure_entity(EntityType.REPORT)
def calmar_ratio(report_id: str, rolling_window: Union[int, str], *, source: str = None,
                 real_time: bool = False,
                 request_id: Optional[str] = None) -> pd.Series:
    """
    Risk-adjusted performance metric that divides an investment strategy’s
    annualized rate of return by its maximum drawdown, focusing specifically
    on the strategy’s return per unit of downside risk.

    Calmar Ratio = Annualized Return / Max Drawdown

    :param report_id: id of performance report
    :param rolling_window: size of window to use
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of the calmar ratio
    """
    rolling_window = _parse_window(rolling_window)
    portfolio_pnl = _get_daily_pnl(report_id)
    cumulative_return = (1 + portfolio_pnl) ** np.sqrt(252) - 1
    cumulative_return.index = pd.to_datetime(cumulative_return.index)
    aum_series = aum(report_id)
    max_drawdown_series = max_drawdown(aum_series, rolling_window)
    calmar = cumulative_return / max_drawdown_series.abs()

    return calmar


@plot_measure_entity(EntityType.REPORT)
def sortino_ratio(report_id: str, benchmark_id: str, rolling_window: Union[int, str], *,
                  source: str = None,
                  real_time: bool = False,
                  request_id: Optional[str] = None) -> pd.Series:
    """
    Risk-adjusted measure that calculates the excess return over the benchmark per unit of semi-variance

    Sortino Ratio = (Rp - Rb) / Downside Deviation

    Where:

    Rp = Portfolio Return

    Rb = Benchmark Return

    Downside Deviation = Standard Deviation of negative asset returns.

    :param report_id: id of performance report
    :param benchmark_id: id of benchmark asset, can be security or risk free
    :param rolling_window: size of window to use
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: portfolio estimated pnl
    """
    start_date = DataContext.current.start_time.date()
    end_date = DataContext.current.end_time.date()
    rolling_window = _parse_window(rolling_window)
    portfolio_pnl = _get_daily_pnl(report_id)

    security = SecurityMaster.get_asset(benchmark_id, AssetIdentifier.MARQUEE_ID)

    if isinstance(security, Bond):
        benchmark_pnl = (1 + _get_risk_free_rate(benchmark_id, start_date, end_date)) ** (1 / 252) - 1
    else:
        benchmark_pnl = _get_benchmark_daily_return(benchmark_id, start_date, end_date)

    excess = (portfolio_pnl - benchmark_pnl).dropna()
    sortino = excess.rolling(window=rolling_window).apply(lambda x: _compute_sortino(x), raw=False)
    return sortino


@plot_measure_entity(EntityType.REPORT)
def jensen_alpha(report_id: str, benchmark_id: str, risk_free_id: str, *, source: str = None,
                 real_time: bool = False,
                 request_id: Optional[str] = None) -> pd.Series:
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

    :param report_id: id of performance report
    :param benchmark_id: id of benchmark asset
    :param risk_free_id: id of risk-free asset
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of jensen alpha
    """
    start_date = DataContext.current.start_time.date()
    end_date = DataContext.current.end_time.date()
    portfolio_pnl = _get_daily_pnl(report_id)
    benchmark_pnl = _get_benchmark_daily_return(benchmark_id, start_date, end_date)

    risk_free_rate = (1 + _get_risk_free_rate(risk_free_id, start_date, end_date)) ** (1 / 252) - 1

    portfolio_beta_series = beta(portfolio_pnl, benchmark_pnl, prices=False)
    jensen = (portfolio_pnl - (risk_free_rate + portfolio_beta_series * (benchmark_pnl - risk_free_rate)))
    return jensen


@plot_measure_entity(EntityType.REPORT)
def jensen_alpha_bear(report_id: str, benchmark_id: str, risk_free_id: str, *, source: str = None,
                      real_time: bool = False,
                      request_id: Optional[str] = None) -> pd.Series:
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

    :param report_id: id of performance report
    :param benchmark_id: id of benchmark asset
    :param risk_free_id: id of risk-free asset
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of jensen alpha
    """
    start_date = DataContext.current.start_time.date()
    end_date = DataContext.current.end_time.date()
    portfolio_pnl = _get_daily_pnl(report_id)
    benchmark_pnl = _get_benchmark_daily_return(benchmark_id, start_date, end_date)
    risk_free_rate = (1 + _get_risk_free_rate(risk_free_id, start_date, end_date)) ** (1 / 252) - 1
    portfolio_beta_series = beta(portfolio_pnl, benchmark_pnl, prices=False)

    benchmark_pnl = benchmark_pnl[benchmark_pnl < 0]

    jensen = (portfolio_pnl - (risk_free_rate + portfolio_beta_series * (benchmark_pnl - risk_free_rate)))
    return jensen


@plot_measure_entity(EntityType.REPORT)
def jensen_alpha_bull(report_id: str, benchmark_id: str, risk_free_id: str, *, source: str = None,
                      real_time: bool = False,
                      request_id: Optional[str] = None) -> pd.Series:
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

    :param report_id: id of performance report
    :param benchmark_id: id of benchmark asset
    :param risk_free_id: id of risk-free asset
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of jensen alpha
    """
    start_date = DataContext.current.start_time.date()
    end_date = DataContext.current.end_time.date()
    portfolio_pnl = _get_daily_pnl(report_id)
    benchmark_pnl = _get_benchmark_daily_return(benchmark_id, start_date, end_date)
    risk_free_rate = (1 + _get_risk_free_rate(risk_free_id, start_date, end_date)) ** (1 / 252) - 1

    portfolio_beta_series = beta(portfolio_pnl, benchmark_pnl, prices=False)
    benchmark_pnl = benchmark_pnl[benchmark_pnl > 0]
    jensen = (portfolio_pnl - (risk_free_rate + portfolio_beta_series * (benchmark_pnl - risk_free_rate)))
    return jensen


@plot_measure_entity(EntityType.REPORT)
def information_ratio(report_id: str, benchmark_id: str, *, source: str = None,
                      real_time: bool = False,
                      request_id: Optional[str] = None) -> pd.Series:
    """
    Risk-adjusted measure that calculates the excess return over the benchmark,
    per unit of tracking error volatility. It measures the consistency with
    which the portfolio is beating the benchmark.

    Information Ratio = (Rp - Rb) / Tracking Error

    Where:

    Rp = Portfolio Return

    Rb = Benchmark Return

    Tracking Error = Standard Deviation of the difference between the portfolio and benchmark returns.

    :param report_id: id of performance report
    :param benchmark_id: id of benchmark asset
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of the information ratio
    """
    start_date = DataContext.current.start_time.date()
    end_date = DataContext.current.end_time.date()
    portfolio_pnl = _get_daily_pnl(report_id)
    benchmark_pnl = _get_benchmark_daily_return(benchmark_id, start_date, end_date)

    portfolio_excess = portfolio_pnl - benchmark_pnl
    portfolio_std = np.std(portfolio_excess)
    information = portfolio_excess / portfolio_std

    return information


@plot_measure_entity(EntityType.REPORT)
def information_ratio_bear(report_id: str, benchmark_id: str, *, source: str = None,
                           real_time: bool = False,
                           request_id: Optional[str] = None) -> pd.Series:
    """
    Risk-adjusted measure that calculates the excess return over the benchmark,
    per unit of tracking error volatility, counting only the periods when the benchmark return was negative


    Information Ratio = (Rp - Rb) / Tracking Error

    Where:

    Rp = Portfolio Return

    Rb = Benchmark Return

    Tracking Error = Standard Deviation of the difference between the portfolio and benchmark returns.

    :param report_id: id of performance report
    :param benchmark_id: id of benchmark asset
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of the information ratio
    """
    start_date = DataContext.current.start_time.date()
    end_date = DataContext.current.end_time.date()
    portfolio_pnl = _get_daily_pnl(report_id)
    benchmark_pnl = _get_benchmark_daily_return(benchmark_id, start_date, end_date)
    benchmark_pnl = benchmark_pnl[benchmark_pnl < 0]
    portfolio_excess = portfolio_pnl - benchmark_pnl
    portfolio_std = np.std(portfolio_excess)
    information = portfolio_excess / portfolio_std

    return information


@plot_measure_entity(EntityType.REPORT)
def information_ratio_bull(report_id: str, benchmark_id: str, *, source: str = None,
                           real_time: bool = False,
                           request_id: Optional[str] = None) -> pd.Series:
    """
    Risk-adjusted measure that calculates the excess return over the benchmark,
    per unit of tracking error volatility, counting only the periods when the benchmark return was positive.

    Information Ratio = (Rp - Rb) / Tracking Error

    Where:

    Rp = Portfolio Return

    Rb = Benchmark Return

    Tracking Error = Standard Deviation of the difference between the portfolio and benchmark returns.

    :param report_id: id of performance report
    :param benchmark_id: id of benchmark asset
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: portfolio estimated pnl
    """
    start_date = DataContext.current.start_time.date()
    end_date = DataContext.current.end_time.date()
    portfolio_pnl = _get_daily_pnl(report_id)
    benchmark_pnl = _get_benchmark_daily_return(benchmark_id, start_date, end_date)
    benchmark_pnl = benchmark_pnl[benchmark_pnl > 0]
    portfolio_excess = portfolio_pnl - benchmark_pnl
    portfolio_std = np.std(portfolio_excess)
    information = portfolio_excess / portfolio_std

    return information


@plot_measure_entity(EntityType.REPORT)
def modigliani_ratio(report_id: str, benchmark_id: str, risk_free_id: str,
                     rolling_window: Union[int, str], *,
                     source: str = None,
                     real_time: bool = False,
                     request_id: Optional[str] = None) -> pd.Series:
    """
    Modigliani RAP measures how much the portfolio would have returns if it had had
    the same risk as the benchmark. It is a linear transformation of the Sharpe Ratio,
    but the results are expressed in terms of performance.

    M2 = (Sharpe Ratio * σb) + Rf

    Where:

    Sharpe Ratio = Portfolio Sharpe Ratio

    σb = Standard Deviation of the Benchmark Return

    Rf = Risk Free Rate.

    :param report_id: id of performance report
    :param benchmark_id: id of benchmark asset
    :param risk_free_id: id of risk free asset
    :param rolling_window: size of window to use
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of the modigliani ratio
    """
    start_date = DataContext.current.start_time.date()
    end_date = DataContext.current.end_time.date()
    rolling_window = _parse_window(rolling_window)

    benchmark_return = _get_benchmark_daily_return(benchmark_id, start_date, end_date)
    risk_free_rates = (1 + _get_risk_free_rate(risk_free_id, start_date, end_date)) ** (1 / 252) - 1

    sharpe_series = portfolio_sharpe_ratio(report_id, risk_free_id, rolling_window)

    benchmark_excess = benchmark_return - risk_free_rates

    std_benchmark = benchmark_excess.dropna().rolling(window=rolling_window).std()

    modigliani = (sharpe_series * std_benchmark) + risk_free_rates

    return modigliani


@plot_measure_entity(EntityType.REPORT)
def treynor_measure(report_id: str, risk_free_id: str, benchmark_id: str, *, source: str = None,
                    real_time: bool = False,
                    request_id: Optional[str] = None) -> pd.Series:
    """
    Risk-adjusted measure that calculates the excess return over the risk free rate
    per unit of beta relative to the benchmark. This is useful for assessing the excess
    return from each unit of systematic risk.

    Treynor Ratio = (Rp - Rf) / Beta

    Where:

    Rp = Portfolio Return

    Rf = Risk-Free Rate

    Beta = Portfolio Beta

    :param report_id: id of performance report
    :param risk_free_id: id of risk-free asset
    :param benchmark_id: id of benchmark asset
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: portfolio estimated pnl
    """
    start_date = DataContext.current.start_time.date()
    end_date = DataContext.current.end_time.date()
    portfolio_return = _get_daily_pnl(report_id)
    security = SecurityMaster.get_asset(benchmark_id,
                                        AssetIdentifier.MARQUEE_ID)
    spot_data_coordinate = security.get_data_coordinate(DataMeasure.SPOT_PRICE)
    benchmark_pricing = spot_data_coordinate.get_series(start=start_date, end=end_date)
    benchmark_pricing = benchmark_pricing.sort_index()
    portfolio_return = (1 + portfolio_return) ** np.sqrt(252) - 1
    risk_free_rate = _get_risk_free_rate(risk_free_id, start_date, end_date)

    beta_series = beta(aum(report_id), benchmark_pricing)

    treynor_series = (portfolio_return - risk_free_rate) / beta_series
    return treynor_series


@plot_measure_entity(EntityType.REPORT)
def alpha(report_id: str, benchmark_id: str, rolling_window: Union[int, str], *,
          source: str = None,
          real_time: bool = False,
          request_id: Optional[str] = None) -> pd.Series:
    """
    This is the intercept from a regression analysis, where the portfolio's returns are regressed
    against the benchmark's returns. It represents the portion of the portfolio's return that is
    not explained by the benchmark's performance.

    :param report_id: id of performance report
    :param benchmark_id: id of benchmark asset
    :param rolling_window: size of window to use
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of the beta
    """
    start_date = DataContext.current.start_time.date()
    end_date = DataContext.current.end_time.date()
    rolling_window = _parse_window(rolling_window)
    portfolio_pnl = _get_daily_pnl(report_id)

    benchmark_pnl = _get_benchmark_return(benchmark_id, start_date, end_date)

    intercepts = {}
    benchmark_pnl = benchmark_pnl.reindex(portfolio_pnl.index)

    for i in range(rolling_window, len(portfolio_pnl) + 1):
        portfolio_window = portfolio_pnl.iloc[i - rolling_window:i]
        benchmark_window = benchmark_pnl.iloc[i - rolling_window:i]

        slope, intercept, *_ = stats.linregress(portfolio_window, benchmark_window)
        intercepts[portfolio_pnl.index[i - 1]] = intercept

    alpha_series = pd.Series(intercepts)

    return alpha_series


@plot_measure_entity(EntityType.REPORT)
def portfolio_beta(report_id: str, benchmark_id: str, rolling_window: Union[int, str], *,
                   source: str = None,
                   real_time: bool = False,
                   request_id: Optional[str] = None) -> pd.Series:
    """
    Beta defined as the slope of the regression between report pnl and benchmark pnl

    :param report_id: id of performance report
    :param benchmark_id: id of benchmark asset
    :param rolling_window: size of window to use
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of the beta
    """
    start_date = DataContext.current.start_time.date()
    end_date = DataContext.current.end_time.date()
    rolling_window = _parse_window(rolling_window)
    portfolio_return = _get_daily_pnl(report_id)
    benchmark_pnl = _get_benchmark_return(benchmark_id, start_date, end_date)

    return beta(portfolio_return, benchmark_pnl, rolling_window, prices=False)


@plot_measure_entity(EntityType.REPORT)
def portfolio_correlation(report_id: str, benchmark_id: str, rolling_window: Union[int, str],
                          *,
                          source: str = None,
                          real_time: bool = False,
                          request_id: Optional[str] = None) -> pd.Series:
    """
    Correlation coefficient between the portfolio and the benchmark returns over the stated time frame

    :param report_id: id of performance report
    :param benchmark_id: id of benchmark asset
    :param rolling_window: size of window to use
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: time series of the correlation coefficient
    """
    start_date = DataContext.current.start_time.date()
    end_date = DataContext.current.end_time.date()
    rolling_window = _parse_window(rolling_window)
    portfolio_pnl = aum(report_id)
    portfolio_pnl.index = pd.to_datetime(portfolio_pnl.index)

    security = SecurityMaster.get_asset(benchmark_id,
                                        AssetIdentifier.MARQUEE_ID)
    spot_data_coordinate = security.get_data_coordinate(DataMeasure.SPOT_PRICE)
    benchmark_pricing = spot_data_coordinate.get_series(start=start_date, end=end_date)
    benchmark_pricing = benchmark_pricing.sort_index()

    return correlation(portfolio_pnl, benchmark_pricing, rolling_window)


@plot_measure_entity(EntityType.REPORT)
def capture_ratio(report_id: str, benchmark_id: str, rolling_window: Union[int, str], *,
                  source: str = None,
                  real_time: bool = False,
                  request_id: Optional[str] = None) -> pd.Series:
    """
    A measure of how well portfolio is doing relative to the benchmark,
    defined as the ratio of the portfolio return to the benchmark return calculated
    on a daily basis and averaged over the stated time period.

    :param report_id: id of performance report
    :param benchmark_id: id of benchmark asset
    :param rolling_window: size of window to use
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: portfolio capture ratio
    """
    start_date = DataContext.current.start_time.date()
    end_date = DataContext.current.end_time.date()
    rolling_window = _parse_window(rolling_window)
    benchmark_return = _get_benchmark_daily_return(benchmark_id, start_date, end_date)
    portfolio_return = _get_daily_pnl(report_id)

    avg_portfolio = portfolio_return.rolling(window=rolling_window).mean()
    avg_benchmark = benchmark_return.rolling(window=rolling_window).mean()

    capture_ratio_series = (avg_portfolio / avg_benchmark)
    return capture_ratio_series


@plot_measure_entity(EntityType.REPORT)
def r_squared(report_id: str, benchmark_id: str, rolling_window: Union[int, str], *,
              source: str = None,
              real_time: bool = False,
              request_id: Optional[str] = None) -> pd.Series:
    """
    A measure of how well the portfolio's performance correlates with the performance of the benchmark,
    and thus a measure of what portion of its performance may be explained by the performance of the benchmark.

    :param report_id: id of performance report
    :param benchmark_id: id of benchmark
    :param rolling_window: size of rolling window
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: portfolio r squared
    """
    rolling_window = _parse_window(rolling_window)
    r_values = portfolio_correlation(report_id, benchmark_id, rolling_window)
    r_values_squared = r_values ** 2
    return r_values_squared


def _get_benchmark_return(benchmark_id, start_date, end_date):
    security = SecurityMaster.get_asset(benchmark_id,
                                        AssetIdentifier.MARQUEE_ID)
    spot_data_coordinate = security.get_data_coordinate(DataMeasure.SPOT_PRICE)
    benchmark_pricing = spot_data_coordinate.get_series(start=start_date, end=end_date)
    benchmark_pricing = benchmark_pricing.sort_index()

    start_price = benchmark_pricing.iloc[0]

    benchmark_returns = (benchmark_pricing / start_price) - 1
    return benchmark_returns * 100


def _get_benchmark_daily_return(benchmark_id, start_date, end_date):
    security = SecurityMaster.get_asset(benchmark_id,
                                        AssetIdentifier.MARQUEE_ID)
    spot_data_coordinate = security.get_data_coordinate(DataMeasure.SPOT_PRICE)
    benchmark_pricing = spot_data_coordinate.get_series(start=start_date, end=end_date)
    benchmark_pricing = benchmark_pricing.sort_index()
    return benchmark_pricing.pct_change()


def _max_drawdown(series):
    running_max = series.cummax()
    drawdown = (series - running_max) / running_max
    max_drawdown_ts = drawdown.cummin()
    return max_drawdown_ts[-1]


def _compute_sortino(series):
    downside = series[series < 0]
    downside_std = np.sqrt((downside ** 2).mean()) * np.sqrt(252)
    mean_excess = series.mean() * 252
    return mean_excess / downside_std if downside_std != 0 else np.nan


def _rolling_downside_risk(series):
    negative_devs = series[series < series.mean()] - series.mean()
    semi_variance_series = (negative_devs ** 2).mean()
    return np.sqrt(semi_variance_series)


def _rolling_semi_variance(series):
    negative_devs = series[series < 0] - series.mean()
    semi_variance_series = (negative_devs ** 2).mean()
    return np.sqrt(semi_variance_series)


def _get_daily_pnl(report_id: str) -> pd.Series:
    portfolio_return = pnl(report_id)
    portfolio_return.index = pd.to_datetime(portfolio_return.index)
    portfolio_return = portfolio_return / aum(report_id).shift(1)

    return portfolio_return


def _get_risk_free_rate(risk_free_id, start_date, end_date):
    risk_free = SecurityMaster.get_asset(risk_free_id,
                                         AssetIdentifier.MARQUEE_ID)
    risk_free_pricing_data = risk_free.get_data_coordinate('yield')
    risk_free_rate = risk_free_pricing_data.get_series(start=start_date, end=end_date)
    return risk_free_rate.drop_duplicates()


def _replay_historical_factor_moves_on_latest_positions(report_id: str, factors: List[str]) -> \
        Union[pd.Series, pd.DataFrame]:
    start_date = DataContext.current.start_time.date()
    end_date = DataContext.current.end_time.date()
    risk_report = FactorRiskReport.get(report_id)
    risk_model_id = risk_report.get_risk_model_id()

    # Get data in batches of 365 days
    date_range = pd.bdate_range(start_date, end_date)
    batches = np.array_split([d.date() for d in date_range.tolist()], math.ceil(len(date_range.tolist()) / 365))
    data_query_results = []
    query = {"riskModel": risk_model_id}
    if factors:
        query.update({"factor": factors})
    for batch in batches:
        data_query_results += GsDataApi.execute_query(
            'RISK_MODEL_FACTOR',
            DataQuery(
                where=query,
                start_date=batch[0],
                end_date=batch[-1]
            )
        ).get('data', [])

    return_data = pd.DataFrame(data_query_results).pivot(columns="factor", index="date", values="return").sort_index()
    return_data_aggregated = (return_data / 100).apply(geometrically_aggregate)

    latest_report_date = risk_report.latest_end_date
    factor_exposures = risk_report.get_results(
        start_date=latest_report_date,
        end_date=latest_report_date,
        return_format=ReturnFormat.JSON
    )
    factor_exposure_df = pd.DataFrame(factor_exposures).pivot(columns="factor",
                                                              index="date",
                                                              values="exposure").sort_index()

    factor_exposure_df = factor_exposure_df.reindex(columns=return_data_aggregated.columns)
    factor_attributed_pnl_values = return_data_aggregated.values * factor_exposure_df.values
    factor_attributed_pnl = pd.DataFrame(factor_attributed_pnl_values, index=return_data_aggregated.index,
                                         columns=return_data_aggregated.columns)

    return factor_attributed_pnl


def _parse_window(window: Union[int, str]):
    if isinstance(window, int):
        return window
    match = re.fullmatch(r'(\d+)([dwmy])', window.strip().lower())
    if match is None:
        raise MqValueError('Invalid window format, please end with one of: ["d", "w", "m", "y"]')
    value, unit = match.groups()
    value = int(value)
    unit_multipliers = {
        'd': 1,
        'w': 5,
        'm': 22,
        'y': 252
    }
    return value * unit_multipliers[unit]


def _get_factor_data(report_id: str, factor_name: str, query_type: QueryType, unit: Unit = Unit.NOTIONAL) -> pd.Series:
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
    include_total_factor = factor_name != 'Total' and unit == Unit.PERCENT and query_type == QueryType.FACTOR_PNL
    factors_to_query = [factor_name, 'Total'] if include_total_factor else [factor_name]
    factor_data = report.get_results(
        factors=factors_to_query,
        start_date=DataContext.current.start_date,
        end_date=DataContext.current.end_date,
        return_format=ReturnFormat.JSON
    )
    total_data = [d for d in factor_data if d.get(data_type) is not None and d.get('factor') == 'Total']
    factor_data = [d for d in factor_data if d.get(data_type) is not None and d.get('factor') == factor_name]
    if unit == Unit.PERCENT:
        if report.position_source_type != PositionSourceType.Portfolio:
            raise MqValueError('Unit can only be set to percent for portfolio reports')
        pm = PortfolioManager(report.position_source_id)
        tags = dict((tag.name, tag.value) for tag in report.parameters.tags) if report.parameters.tags else None
        performance_report = pm.get_performance_report(tags=tags)
        start_date = dt.datetime.strptime(min([d['date'] for d in factor_data]), '%Y-%m-%d').date()
        end_date = dt.datetime.strptime(max([d['date'] for d in factor_data]), '%Y-%m-%d').date()
        if query_type == QueryType.FACTOR_PNL:
            # Factor Pnl needs to be geometrically aggregated if unit is %
            aum_df = format_aum_for_return_calculation(performance_report, start_date, end_date)
            return get_factor_pnl_percent_for_single_factor(factor_data, total_data, aum_df, start_date)
        else:
            aum = performance_report.get_aum(start_date=start_date, end_date=end_date)
            for data in factor_data:
                if aum.get(data['date']) is None:
                    raise MqValueError('Cannot convert to percent: Missing AUM on some dates in the date range')
            factor_exposures = [{
                'date': d['date'],
                col_name: d[data_type] / aum.get(d['date']) * 100
            } for d in factor_data]
    else:
        factor_exposures = [{'date': d['date'], col_name: d[data_type]} for d in factor_data]

    # Create and return timeseries
    df = pd.DataFrame(factor_exposures)
    if not df.empty:
        df = df.set_index('date')
        df.index = pd.to_datetime(df.index)
    return _extract_series_from_df(df, query_type)


def _return_metrics(one_leg: pd.DataFrame, dates: list, name: str):
    if one_leg.empty:
        return pd.DataFrame(index=dates, data={f'{name}Metrics': [0 for d in dates], "exposure": [0 for d in dates]})
    one_leg = one_leg.groupby(one_leg.index).agg(pnl=('pnl', 'sum'), exposure=('netExposure', 'sum'))

    one_leg['cumulativePnl'] = one_leg['pnl'].cumsum(axis=0)

    one_leg['normalizedExposure'] = (one_leg['exposure'] - one_leg['cumulativePnl'])
    one_leg.iloc[0, one_leg.columns.get_loc('cumulativePnl')] = 0
    one_leg[f'{name}Metrics'] = one_leg['cumulativePnl'] / one_leg['normalizedExposure'] + 1

    one_leg[f'{name}Metrics'] = 1 / one_leg[f'{name}Metrics'] if one_leg['exposure'].iloc[-1] < 0 else one_leg[
        f'{name}Metrics']
    return one_leg
