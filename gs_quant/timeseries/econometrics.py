# Copyright 2018 Goldman Sachs.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
#
# Chart Service will attempt to make public functions (not prefixed with _) from this module available. Such functions
# should be fully documented: docstrings should describe parameters and the return value, and provide a 1-line
# description. Type annotations should be provided for parameters.
from .statistics import *
from ..errors import *
from gs_quant.api.gs.data import GsDataApi
from gs_quant.data import DataContext
from gs_quant.datetime.date import DayCountConvention
from gs_quant.markets.securities import Asset
from gs_quant.target.common import Currency
from gs_quant.timeseries.datetime import align

"""
Econometrics timeseries library is for standard economic and time series analytics operations, including returns,
diffs, lags, volatilities and other numerical operations which are generally finance-oriented
"""


class AnnualizationFactor(IntEnum):
    DAILY = 252
    WEEKLY = 52
    SEMI_MONTHLY = 26
    MONTHLY = 12
    QUARTERLY = 4
    ANNUALLY = 1


class SharpeAssets(Enum):
    USD = 'MAP35DA6K5B1YXGX'
    AUD = 'MAFRZWJ790MQY0EW'
    CHF = 'MAS0NN4ZX7NYXB36'
    EUR = 'MA95W0N1214395N8'
    GBP = 'MA41ZEFTWR8Q7HBM'
    JPY = 'MA8GXV3SJ0TXH1JV'
    SEK = 'MAGNZZY0GJ4TATNG'


def excess_returns(price_series: pd.Series, benchmark_or_rate: Union[Asset, Currency, float], *,
                   day_count_convention=DayCountConvention.ACTUAL_360) -> pd.Series:
    if isinstance(benchmark_or_rate, float):
        er = [price_series.iloc[0]]
        for j in range(1, len(price_series)):
            fraction = day_count_fraction(price_series.index[j - 1], price_series.index[j], day_count_convention)
            er.append(er[-1] + price_series.iloc[j] - price_series.iloc[j - 1] * (1 + benchmark_or_rate * fraction))
        return pd.Series(er, index=price_series.index)

    if isinstance(benchmark_or_rate, Currency):
        try:
            marquee_id = SharpeAssets[benchmark_or_rate.value].value
        except KeyError:
            raise MqValueError(f"unsupported currency {benchmark_or_rate}")
    else:
        marquee_id = benchmark_or_rate.get_marquee_id()

    with DataContext(price_series.index[0], price_series.index[-1]):
        q = GsDataApi.build_market_data_query([marquee_id], QueryType.SPOT)
        df = GsDataApi.get_market_data(q)
    curve, bench_curve = align(price_series, df['spot'], Interpolate.INTERSECT)

    e_returns = [curve.iloc[0]]
    for i in range(1, len(curve)):
        multiplier = 1 + curve.iloc[i] / curve.iloc[i - 1] - bench_curve.iloc[i] / bench_curve.iloc[i - 1]
        e_returns.append(e_returns[-1] * multiplier)
    return pd.Series(e_returns, index=curve.index)


def _annualized_return(levels: pd.Series) -> pd.Series:
    v0 = levels.iloc[0]
    d0 = levels.index[0]
    points = list(map(lambda d, v: pow(v / v0, 365.25 / (d - d0).days) - 1, levels.index[1:], levels.values[1:]))
    points.insert(0, 0)
    return pd.Series(points, index=levels.index)


def _get_ratio(price_series: pd.Series, benchmark_or_rate: Union[Asset, float, str], *,
               day_count_convention: DayCountConvention) -> pd.Series:
    er = excess_returns(price_series, benchmark_or_rate, day_count_convention=day_count_convention)
    ann_return = _annualized_return(er)
    ann_vol = volatility(er) / 100
    return ann_return / ann_vol


@plot_session_function
def sharpe_ratio(prices_: pd.Series, risk_free_rate: Union[Currency, float]) -> pd.Series:
    """
    Calculate Sharpe ratio

    :param prices_: series of prices for an asset
    :param risk_free_rate: a fixed rate or currency like USD
    :return: Sharpe ratio

    **Usage**

    Given a price series and risk-free rate (a number, currency, or cash asset), returns the rolling Sharpe ratio.

    For a fixed rate R, excess returns E are calculated as:

    :math:`E_t = E_{t-1} + P_t - P_{t-1} * (1 + R * DCF_{t-1,t})`

    Subscripts refers to dates in the price series.

    P is a point in the price series.

    DCF is the day count fraction using the Act/360 convention.
    """
    if not isinstance(risk_free_rate, (Currency, float)):
        raise MqTypeError(f'{risk_free_rate} must be a currency or fixed interest rate')
    return _get_ratio(prices_, risk_free_rate, day_count_convention=DayCountConvention.ACTUAL_360)


@plot_function
def returns(series: pd.Series, obs: int = 1, type: Returns = Returns.SIMPLE) -> pd.Series:
    """
    Calculate returns from price series

    :param series: time series of prices
    :param obs: number of observations
    :param type: returns type: simple or logarithmic
    :return: date-based time series of return

    **Usage**

    Compute returns series from price levels, based on the value of *type*:

    ==========    =============================
    Type          Description
    ===========   =============================
    simple        Simple arithmetic returns
    logarithmic   Logarithmic returns
    ===========   =============================

    *Simple*

    Simple geometric change in asset prices, which can be aggregated across assets

    :math:`Y_t = \\frac{X_t}{X_{t-obs}} - 1`

    where :math:`X_t` is the asset price at time :math:`t`

    *Logarithmic*

    Natural logarithm of asset price changes, which can be aggregated through time

    :math:`Y_t = log(X_t) - log(X_{t-obs})`

    where :math:`X_t` is the asset price at time :math:`t`

    **Examples**

    Generate price series and take compute returns

    >>> prices = generate_series(100)
    >>> returns = returns(prices)

    **See also**

    :func:`prices`
    """

    if series.size < 1:
        return series

    if type == Returns.SIMPLE:
        ret_series = series / series.shift(obs) - 1
    elif type == Returns.LOGARITHMIC:
        log_s = series.apply(math.log)
        ret_series = log_s - log_s.shift(obs)
    else:
        raise MqValueError('Unknown returns type (use simple / log)')

    return ret_series


@plot_function
def prices(series: pd.Series, initial: int = 1, type: Returns = Returns.SIMPLE) -> pd.Series:
    """
    Calculate price levels from returns series

    :param series: time series of returns
    :param initial: initial price level
    :param type: returns type: simple or logarithmic
    :return: date-based time series of return

    **Usage**

    Compute price levels from returns series, based on the value of *type*:

    ==========    =============================
    Type          Description
    ===========   =============================
    simple        Simple arithmetic returns
    logarithmic   Logarithmic returns
    ===========   =============================

    *Simple*

    Compute asset price series from simple returns:

    :math:`Y_t = (1 + X_{t-1}) Y_{t-1}`

    where :math:`X_t` is the asset price at time :math:`t` and :math:`Y_0 = initial`

    *Logarithmic*

    Compute asset price series from logarithmic returns:

    :math:`Y_t = e^{X_{t-1}} Y_{t-1}`

    where :math:`X_t` is the asset price at time :math:`t` and :math:`Y_0 = initial`

    **Examples**

    Generate price series and take compute returns

    >>> series = generate_series(100)
    >>> returns = prices(returns(series))

    **See also**

    :func:`returns` :func:`product` :func:`exp`
    """

    if series.size < 1:
        return series

    if type == Returns.SIMPLE:
        return product(1 + series) * initial
    elif type == Returns.LOGARITHMIC:
        return product(series.apply(math.exp)) * initial
    else:
        raise MqValueError('Unknown returns type (use simple / log)')


@plot_function
def index(x: pd.Series, initial: int = 1) -> pd.Series:
    """
    Geometric series normalization

    :param x: time series
    :param initial: initial value
    :return: normalized time series

    **Usage**

    Divides every value in x by the initial value of x:

    :math:`Y_t = initial * X_t / X_0`

    where :math:`X_0` is the first value in the series

    **Examples**

    Normalize series to 1:

    >>> series = generate_series(100)
    >>> returns = index(series)

    **See also**

    :func:`returns`

    """
    i = x.first_valid_index()
    return pd.Series() if i is None else initial * x / x[i]


@plot_function
def change(x: pd.Series) -> pd.Series:
    """
    Arithmetic series normalization

    :param x: time series
    :return: normalized time series

    **Usage**

    Compute difference of every value from the initial value of x:

    :math:`Y_t = X_t - X_0`

    where :math:`X_0` is the first value in the series

    **Examples**

    Change in level from initial value:

    >>> series = generate_series(100)
    >>> returns = change(series)

    **See also**

    :func:`index`

    """
    return x - x[0]


def _get_annualization_factor(x):
    prev_idx = x.index[0]
    distances = []

    for idx, value in x.iloc[1:].iteritems():
        d = (idx - prev_idx).days
        if d == 0:
            raise MqValueError('multiple data points on same date')
        distances.append(d)
        prev_idx = idx

    average_distance = numpy.average(distances)
    if average_distance < 2.1:
        factor = AnnualizationFactor.DAILY
    elif 6 <= average_distance < 8:
        factor = AnnualizationFactor.WEEKLY
    elif 14 <= average_distance < 17:
        factor = AnnualizationFactor.SEMI_MONTHLY
    elif 25 <= average_distance < 35:
        factor = AnnualizationFactor.MONTHLY
    elif 85 <= average_distance < 97:
        factor = AnnualizationFactor.QUARTERLY
    elif 360 <= average_distance < 386:
        factor = AnnualizationFactor.ANNUALLY
    else:
        raise MqValueError('Cannot infer annualization factor, average distance: ' + str(average_distance))
    return factor


@plot_function
def annualize(x: pd.Series) -> pd.Series:
    """
    Annualize series based on sample observation frequency

    :param x: time series of prices
    :return: date-based time series of annualized values

    **Usage**

    Based on number of days between observations, will determine an annualization factor and then adjust values
    accordingly. Useful for annualizing daily or monthly returns

    :math:`Y_t = X_t * \sqrt{F}`

    Annualization factors as follows, based on period implied by observations:

    =========   =============================
    Period      Annualization Factor (F)
    =========   =============================
    Daily       :math:`252`
    Weekly      :math:`52`
    Bi-Weekly   :math:`26`
    Monthly     :math:`12`
    Quarterly   :math:`4`
    Annually    :math:`1`
    =========   =============================

    **Examples**

    Annualize daily returns series:

    >>> prices = generate_series(100)
    >>> ann = annualize(returns(prices))

    **See also**

    :func:`returns`
    """

    factor: int = _get_annualization_factor(x)
    return x * math.sqrt(factor)


@plot_function
def volatility(x: pd.Series, w: Union[Window, int] = Window(None, 0),
               returns_type: Returns = Returns.SIMPLE) -> pd.Series:
    """
    Realized volatility of price series

    :param x: time series of prices
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value. Window size defaults to length of series.
    :param returns_type: returns type: simple or logarithmic
    :return: date-based time series of return

    **Usage**

    Calculate rolling annualized realized volatility of a price series over a given window. Annual volatility of 20% is
    returned as 20.0:

    :math:`Y_t = \sqrt{\\frac{1}{N-1} \sum_{i=t-w+1}^t (R_t - \overline{R_t})^2} * \sqrt{252} * 100`

    where N is the number of observations in each rolling window :math:`w`, :math:`R_t` is the return on time
    :math:`t` based on *returns_type*

    ===========   =======================================================
    Type          Description
    ===========   =======================================================
    simple        Simple geometric change in asset prices:
                  :math:`R_t = \\frac{X_t}{X_{t-1}} - 1`
                  where :math:`X_t` is the asset price at time :math:`t`
    logarithmic   Natural logarithm of asset price changes:
                  :math:`R_t = log(X_t) - log(X_{t-1})`
                  where :math:`X_t` is the asset price at time :math:`t`
    ===========   =======================================================

    and :math:`\overline{R_t}` is the mean value over the same window:

    :math:`\overline{R_t} = \\frac{\sum_{i=t-w+1}^{t} R_t}{N}`

    If window is not provided, computes realized volatility over the full series

    **Examples**

    Compute rolling :math:`1` month (:math:`22` business day) annualized volatility of price series

    >>> series = generate_series(100)
    >>> vol_series = volatility(series, 22)
    >>> vol_series = volatility(series, Window(22, 30))

    **See also**

    :func:`std` :func:`annualize` :func:`returns`

    """
    w = normalize_window(x, w)

    if x.size < 1:
        return x

    return apply_ramp(annualize(std(returns(x, type=returns_type), Window(w.w, 0))).mul(100), w)


@plot_function
def correlation(x: pd.Series, y: pd.Series,
                w: Union[Window, int] = Window(None, 0), type_: SeriesType = SeriesType.PRICES) -> pd.Series:
    """
    Rolling correlation of two price series

    :param x: price series
    :param y: price series
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value. Window size defaults to length of series.
    :param type_: type of both input series: prices or returns
    :return: date-based time series of correlation

    **Usage**

    Calculate rolling `realized correlation <https://en.wikipedia.org/wiki/Correlation_and_dependence>`_,
    :math:`\\rho_t` of two price series over a given window:

    :math:`\\rho_t = \\frac{\sum_{i=t-w+1}^t (R_t - \overline{R_t})(Y_t - \overline{S_t})}{(N-1)\sigma R_t\sigma S_t}`

    where N is the number of observations in each rolling window, :math:`w`, and :math:`R_t` and :math:`S_t` are the
    simple returns for each series on time :math:`t`

    If prices are provided:

    :math:`R_t = \\frac{X_t}{X_{t-1}} - 1` and :math:`S_t = \\frac{Y_t}{Y_{t-1}} - 1`

    If returns are provided:

    :math:`R_t = X_t` and :math:`S_t = Y_t`

    :math:`\overline{R_t}`, :math:`\overline{S_t}` are the mean values, and :math:`\sigma R_{t}` and
    :math:`\sigma S_{t}` are the sample standard deviations, of  series
    :math:`R_t` and :math:`S_t` over the same window

    If window is not provided, computes realized correlation over the full series

    **Examples**

    Compute rolling :math:`1` month (:math:`22` business day) correlation of price series

    >>> series1 = generate_series(100)
    >>> series2 = generate_series(100)
    >>> corr = correlation(series1, series2, 22)

    **See also**

    :func:`std` :func:`returns`

    """
    w = normalize_window(x, w)

    if x.size < 1:
        return x

    given_prices = type_ == SeriesType.PRICES
    ret_1 = returns(x) if given_prices else x
    ret_2 = returns(y) if given_prices else y

    clean_ret1 = ret_1.dropna()
    clean_ret2 = ret_2.dropna()

    if isinstance(w.w, pd.DateOffset):
        values = [clean_ret1.loc[(clean_ret1.index > idx - w.w) & (clean_ret1.index <= idx)].corr(clean_ret2)
                  for idx in clean_ret1.index]
        corr = pd.Series(values, index=clean_ret1.index)
    else:
        corr = clean_ret1.rolling(w.w, 0).corr(clean_ret2)

    return apply_ramp(interpolate(corr, x, Interpolate.NAN), w)


@plot_function
def beta(x: pd.Series, b: pd.Series, w: Union[Window, int] = Window(None, 0), prices: bool = True) -> pd.Series:
    """
    Rolling beta of price series and benchmark

    :param x: time series of prices
    :param b: time series of benchmark prices
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value. Window size defaults to length of series.
    :param prices: True if input series are prices, False if they are returns
    :return: date-based time series of beta

    **Usage**

    Calculate rolling `beta <https://en.wikipedia.org/wiki/Beta_(finance)>`_,
    :math:`\\beta_t` of a series to a benchmark over a given window:

    :math:`R_t = \\alpha_t + \\beta S_t + \epsilon_t`

    Calculated as:

    :math:`\\beta_t = \\frac{\sum_{i=t-w+1}^t Cov(R_t, S_t)}{Var(S_t)}`

    where N is the number of observations in each rolling window, :math:`w`, and :math:`R_t` and :math:`S_t` are the
    simple returns for each series on time :math:`t`:

    :math:`R_t = \\frac{X_t}{X_{t-1}} - 1` and :math:`S_t = \\frac{b_t}{b_{t-1}} - 1`

    If prices = False, assumes returns are provided:

    :math:`R_t = X_t` and :math:`S_t = b_t`

    :math:`Cov(R_t, S_t)` and :math:`Var(S_t)` are the mean and variance of  series
    :math:`R_t` and :math:`S_t` over the same window

    If window is not provided, computes beta over the full series

    **Examples**

    Compute rolling :math:`1` month (:math:`22` business day) beta of two price series

    >>> series = generate_series(100)
    >>> benchmark = generate_series(100)
    >>> b = beta(series, benchmark, 22)

    **See also**

    :func:`var` :func:`cov` :func:`correlation` :func:`returns`
    """
    w = normalize_window(x, w)

    ret_series = returns(x) if prices else x
    ret_benchmark = returns(b) if prices else b

    if isinstance(w.w, pd.DateOffset):
        result = pd.Series([ret_series.loc[(ret_series.index > idx - w.w) & (ret_series.index <= idx)].cov(
            ret_benchmark.loc[(ret_benchmark.index > idx - w.w) & (ret_benchmark.index <= idx)]
        ) / ret_benchmark.loc[(ret_benchmark.index > idx - w.w) & (ret_benchmark.index <= idx)].var()
            for idx in ret_series.index], index=ret_series.index)
    else:
        cov = ret_series.rolling(w.w, 0).cov(ret_benchmark.rolling(w.w, 0))
        result = cov / ret_benchmark.rolling(w.w, 0).var()

    # do not compute initial values as they may be extreme when sample size is small

    result[0:3] = np.nan

    return apply_ramp(interpolate(result, x, Interpolate.NAN), w)


@plot_function
def max_drawdown(x: pd.Series, w: Union[Window, int] = Window(None, 0)) -> pd.Series:
    """
    Compute the maximum peak to trough drawdown over a rolling window.

    :param x: time series
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value. Window size defaults to length of series.
    :return: time series of rolling maximum drawdown

    **Examples**

    Compute the maximum peak to trough `drawdown <https://en.wikipedia.org/wiki/Drawdown_(economics)>`_

    >>> series = generate_series(100)
    >>> max_drawdown(series)

    **See also**

    :func:`returns`

    """
    w = normalize_window(x, w)
    if isinstance(w.w, pd.DateOffset):
        scores = pd.Series([x[idx] / x.loc[(x.index > idx - w.w) & (x.index <= idx)].max() - 1 for idx in x.index],
                           index=x.index)
        result = pd.Series([scores.loc[(scores.index > idx - w.w) & (scores.index <= idx)].min()
                            for idx in scores.index], index=scores.index)
    else:
        rolling_max = x.rolling(w.w, 0).max()
        result = (x / rolling_max - 1).rolling(w.w, 0).min()
    return apply_ramp(result, w)
