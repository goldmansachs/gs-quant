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

import itertools
import datetime as dt
from dataclasses import dataclass
from typing import Iterable, Optional, Union, Tuple

import numpy as np
import pandas as pd
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tools.eval_measures import mse

from .statistics import *
from ..errors import *

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


@plot_function
def returns(series: pd.Series, obs: int = 1, type: Returns = Returns.SIMPLE) -> pd.Series:
    """
    Calculate returns from price series

    :param series: time series of prices
    :param obs: number of observations
    :param type: returns type
    :return: date-based time series of return

    **Usage**

    Compute returns series from price levels, based on the value of *type*:

    ======   =============================
    Type     Description
    ======   =============================
    simple   Simple arithmetic returns
    log      Logarithmic returns
    ======   =============================

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
    :param type: returns type (simple, log)
    :return: date-based time series of return

    **Usage**

    Compute price levels from returns series, based on the value of *type*:

    ======   =============================
    Type     Description
    ======   =============================
    simple   Simple arithmetic returns
    log      Logarithmic returns
    ======   =============================

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
    :param w: Window or int: number of observations and ramp up to use. e.g. Window(22, 10) where 22 is the window size
    and 10 the ramp up value. Window size defaults to length of series.
    :param returns_type: returns type
    :return: date-based time series of return

    **Usage**

    Calculate rolling annualized realized volatility of a price series over a given window. Annual volatility of 20% is
    returned as 20.0:

    :math:`Y_t = \sqrt{\\frac{1}{N-1} \sum_{i=t-w+1}^t (R_t - \overline{R_t})^2} * \sqrt{252} * 100`

    where N is the number of observations in each rolling window, :math:`w`, :math:`R_t` is the simple return on time
    :math:`t`:

    :math:`R_t = \\frac{X_t}{X_{t-1}} - 1`

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
    :param w: Window or int: number of observations and ramp up to use. e.g. Window(22, 10) where 22 is the window size
    and 10 the ramp up value. Window size defaults to length of series.
    :param type_: type of both input series
    :return: date-based time series of correlation

    **Usage**

    Calculate rolling `realized correlation <https://en.wikipedia.org/wiki/Correlation_and_dependence>`_,
    :math:`\\rho_t` of two price series over a given window:

    :math:`\\rho_t = \\frac{\sum_{i=t-w+1}^t (R_t - \overline{R_t})(Y_t - \overline{S_t})}{(N-1)\sigma R_t\sigma S_t}`

    where N is the number of observations in each rolling window, :math:`w`, and :math:`R_t` and :math:`S_t` are the
    simple returns for each series on time :math:`t`:

    :math:`R_t = \\frac{X_t}{X_{t-1}} - 1` and :math:`S_t = \\frac{Y_t}{Y_{t-1}} - 1`

    If prices = False, assumes returns are provided:

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

    corr = clean_ret1.rolling(w.w, 0).corr(clean_ret2)

    return apply_ramp(interpolate(corr, x, Interpolate.NAN), w)


@plot_function
def beta(x: pd.Series, b: pd.Series, w: Union[Window, int] = Window(None, 0), prices: bool = True) -> pd.Series:
    """
    Rolling beta of price series and benchmark

    :param x: time series of prices
    :param b: time series of benchmark prices
    :param w: Window or int: number of observations and ramp up to use. e.g. Window(22, 10) where 22 is the window size
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
    :param w: Window or int: number of observations and ramp up to use. e.g. Window(22, 10) where 22 is the window size
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

    rolling_max = x.rolling(w.w, 0).max()
    result = (x / rolling_max - 1).rolling(w.w, 0).min()
    return apply_ramp(result, w)


@dataclass
class ARIMA_BestParams:
    freq: str = ''
    p: int = None
    d: int = None
    q: int = None
    const: float = None
    ar_coef: list = None
    ma_coef: list = None
    resid: list = None
    series: pd.Series = None


class arima():
    """
    ARIMA is the Autoregressive Integrated Moving Average Model and is used
    to normalize and forecast time series data. ARIMA has 3 parameters:
    (p, d, q) where:
        :p is the number of autoregressive terms
        :d is the number of nonseasonal differences
        :q is the number of lagged forecast errors in the prediction equation

    An ARIMA model is selected from the Catesian product of sets p, q, and d.
    The time series is split into train and test sets and an ARIMA model is fit
    for every combination on the training set. The model with the lowest
    mean-squared error (MSE) on the test set is selected as the best model. The
    original times series can then be transformed by the best model.

    **Examples**
    >>> series = generate_series(100)
    >>> arima = econometrics.arima()
    >>> arima.fit(series, train_size=0.8)
    >>> transformed_time_series = arima.transform(series)
    """

    def __init__(self):
        self.best_params = {}

    def _evaluate_arima_model(
            self, X:
            Union[pd.Series, pd.DataFrame],
            arima_order: Tuple[int, int, int],
            train_size: Union[float, int, None],
            freq: str
    ) -> Tuple[float, dict]:
        if type(train_size) == float:
            train_size = int(len(X) * train_size)
            train, test = X[:train_size].astype(float), X[train_size:].astype(float)
        elif type(train_size) == int:
            train, test = X[:train_size].astype(float), X[train_size:].astype(float)
        elif train_size is None:
            train_size = int(len(X) * 0.75)
            train, test = X[:train_size].astype(float), X[train_size:].astype(float)
        else:
            raise ValueError('train_size is not int, float, or None')

        model = ARIMA(train, order=arima_order, freq=freq)
        model_fit = model.fit(disp=False, method='css', trend='nc')
        ar_coef = model_fit.arparams
        ma_coef = model_fit.maparams
        resid = model_fit.resid

        model_params = model_fit.params.to_dict()
        const = model_params.get('const', 0)

        # calculate test error
        yhat = model_fit.forecast(len(test))[0]
        error = mse(test, yhat)

        return error, const, ar_coef, ma_coef, resid

    def fit(
            self,
            X: Union[pd.Series, pd.DataFrame],
            train_size: Union[float, int, None]=None,
            p_vals: list=[0, 1, 2],
            d_vals: list=[0, 1, 2],
            q_vals: list=[0, 1, 2],
            freq: str=None
    ) -> 'arima':
        """
        Train a combination of ARIMA models. If pandas DataFrame, finds the
        best arima model parameters for each column. If pandas Series, finds
        the best arima model parameters for the series.

        :param X: time series to be operated on; required parameter
        :param train_size: if float, should be between 0.0 and 1.0 and
        represent the proportion of the dataset to include in the train split.
        If int, represents the absolute number of train samples. If None,
        the value is automatically set 0.75
        :p_vals: number of autoregressive terms to search; default is [0,1,2]
        :d_vals: number of differences to search; default is [0,1,2]
        :q_vals: number of lagged forecast to search; always [0,1,2]
        :freq: frequency of time series, default is None
        :return: self
        """

        if isinstance(X, pd.Series):
            X = X.to_frame()

        if not isinstance(X, pd.DataFrame):
            raise ValueError('Not DataFrame or Series!')

        for series_id in X.columns:
            series = X[series_id]
            best_score = float('inf')
            best_order = None
            best_const = None
            best_ar_coef = None
            best_ma_coef = None
            best_resid = None
            for order in list(itertools.product(*[p_vals, d_vals, q_vals])):
                try:
                    mse, const, ar_coef, ma_coef, resid = self._evaluate_arima_model(series, order, train_size, freq)
                    if mse < best_score:
                        best_score = mse
                        best_order = order
                        best_const = const
                        best_ar_coef = ar_coef
                        best_ma_coef = ma_coef
                        best_resid = resid
                except Exception as e:
                    print('   {}'.format(e))
                    continue

            p, d, q = best_order
            assert(p == len(best_ar_coef))

            self.best_params[series_id] = ARIMA_BestParams(
                                                freq=freq,
                                                p=p,
                                                d=d,
                                                q=q,
                                                const=best_const,
                                                ar_coef=best_ar_coef,
                                                ma_coef=best_ma_coef,
                                                resid=best_resid,
                                                series=series)

        return self

    def _difference(self, X: pd.Series, d: int):
        """Helper Function to Difference Time Series n Times"""

        if d == 0:
            return X
        elif d == 1:
            return X.diff()
        else:
            return self._difference(X.diff(), d-1)

    def _lagged_values(self, X: pd.Series, p: int, ar_coef: list):
        """Helper Function to Calculate AutoRegressive(AR) Component"""

        if p == 0:
            return X
        elif p > 0:
            transformed_df = pd.concat([X.copy().shift(periods=i)
                                        for i in range(1, p+1)], axis=1)
            transformed_df = transformed_df.dot(ar_coef)
        else:
            raise ValueError("p should not be less than 0!")
        return transformed_df

    def _calculate_residuals(
            self,
            X_ar: pd.Series,
            X_diff: pd.Series,
            p: int,
            d: int,
            q: int,
            ar_coef: list,
            ma_coef: list,
            freq: str
    ):
        """Helper Function to Calculate Residuals/MA Component"""

        ma_coef = ma_coef[::-1]
        resid = X_ar.copy(deep=True)
        resid[:] = 0

        X_ma = X_ar.copy(deep=True)
        X_ma[:] = np.nan

        for x in range(p + d, len(X_ar)):
            ma_component = resid[x-q: x].dot(ma_coef)
            prediction = X_ar[x] + ma_component
            residual = X_diff[x] - prediction
            resid[x] = residual
            X_ma[x] = prediction

        return resid, X_ma

    def _arima_transform_series(
            self,
            X: pd.Series,
            p: int,
            d: int,
            q: int,
            const: float,
            ar_coef: list,
            ma_coef: list,
            resid: list,
            freq: str
    ) -> pd.Series:
        """Helper Function to Transform Series"""

        # Difference first
        X_diff = self._difference(X, d)

        # Calculate Autoregressive Component
        X_diff_ar = self._lagged_values(X_diff, p, ar_coef)

        # Caluclate Residuals and Moving Average Component
        calcualted_resid, X_diff_ar_ma = self._calculate_residuals(X_diff_ar,
                                                                   X_diff,
                                                                   p,
                                                                   d,
                                                                   q,
                                                                   ar_coef,
                                                                   ma_coef,
                                                                   freq)

        # Check calculated residuals are close with ARIMA statsmodels residuals
        resid_df = pd.concat([calcualted_resid, resid], axis=1, join='inner')
        assert(np.allclose(resid_df[resid_df.columns[0]],
                           resid_df[resid_df.columns[1]]))

        return X_diff_ar_ma

    def _arima_transform_df(self, X: pd.DataFrame) -> pd.DataFrame:
        """Helper Function to Transform DataFrame"""

        series = {}
        for series_id in X.columns:
            freq = self.best_params[series_id].freq
            p = self.best_params[series_id].p
            d = self.best_params[series_id].d
            q = self.best_params[series_id].q
            const = self.best_params[series_id].const
            ar_coef = self.best_params[series_id].ar_coef
            ma_coef = self.best_params[series_id].ma_coef
            resid = self.best_params[series_id].resid

            series[series_id] = self._arima_transform_series(
                                        X[series_id],
                                        p=p,
                                        d=d,
                                        q=q,
                                        const=const,
                                        ar_coef=ar_coef,
                                        ma_coef=ma_coef,
                                        resid=resid,
                                        freq=freq
                                )

        return pd.DataFrame(series)

    def transform(
            self,
            X: Union[pd.Series, pd.DataFrame]
    ) -> Union[pd.DataFrame]:
        """
        Transform a series based on the best ARIMA found from fit().
        Does not support tranformation using MA components.

        :param X: time series to be operated on; required parameter
        :return: DataFrame
        """

        if isinstance(X, pd.Series):
            X = X.to_frame()

        if isinstance(X, pd.DataFrame):
            transformed = self._arima_transform_df(X)
        else:
            raise ValueError('Not DataFrame or Series!')

        return transformed
