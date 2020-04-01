# Copyright 2018 Goldman Sachs.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
#
# Marquee Plot Service will attempt to make public functions (not prefixed with _) from this module available.
# Such functions should be fully documented: docstrings should describe parameters and the return value, and provide
# a 1-line description. Type annotations should be provided for parameters.

import datetime
import numpy
import scipy.stats.mstats as stats
from scipy.stats import percentileofscore
from .algebra import *
import statsmodels.api as sm
from ..models.epidemic import SIR, SEIR, PandemicModel
from ..data import DataContext


"""
Stats library is for basic arithmetic and statistical operations on timeseries.
These include basic algebraic operations, probability and distribution analysis.
Generally not finance-specific routines.
"""


@plot_function
def min_(x: pd.Series, w: Union[Window, int] = Window(None, 0)) -> pd.Series:
    """
    Minimum value of series over given window

    :param x: series: timeseries
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value. Window size defaults to length of series.
    :return: timeseries of minimum value

    **Usage**

    Returns the minimum value of thee series over each window:

    :math:`R_t = min(X_{t-w+1}:X_t)`

    where :math:`w` is the size of the rolling window. If window is not provided, returns the minimum value over the
    full series. If the window size is greater than the available data, will return minimum of available values.

    **Examples**

    Minimum value of price series over the last :math:`22` observations:

    >>> prices = generate_series(100)
    >>> min_(prices, 22)

    **See also**

    :func:`max_`

    """
    w = normalize_window(x, w)
    assert x.index.is_monotonic_increasing, "series index is monotonic increasing"
    if isinstance(w.w, pd.DateOffset):
        values = [x.loc[(x.index > idx - w.w) & (x.index <= idx)].min() for idx in x.index]
        return apply_ramp(pd.Series(values, index=x.index), w)
    else:
        return apply_ramp(x.rolling(w.w, 0).min(), w)


@plot_function
def max_(x: pd.Series, w: Union[Window, int] = Window(None, 0)) -> pd.Series:
    """
    Maximum value of series over given window

    :param x: series: timeseries
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value. Window size defaults to length of series.
    :return: timeseries of maximum value

    **Usage**

    Returns the maximum value of the series over each window:

    :math:`R_t = max(X_{t-w+1}:X_t)`

    where :math:`w` is the size of the rolling window. If window is not provided, returns the minimum value over the
    full series. If the window size is greater than the available data, will return minimum of available values.

    **Examples**

    Maximum value of price series over the last :math:`22` observations:

    >>> prices = generate_series(100)
    >>> max_(prices, 22)

    **See also**

    :func:`min_`

    """
    w = normalize_window(x, w)
    assert x.index.is_monotonic_increasing, "series index is monotonic increasing"
    if isinstance(w.w, pd.DateOffset):
        values = [x.loc[(x.index > idx - w.w) & (x.index <= idx)].max() for idx in x.index]
        return apply_ramp(pd.Series(values, index=x.index), w)
    else:
        return apply_ramp(x.rolling(w.w, 0).max(), w)


@plot_function
def range_(x: pd.Series, w: Union[Window, int] = Window(None, 0)) -> pd.Series:
    """
    Range of series over given window

    :param x: series: timeseries
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value. Window size defaults to length of series.
    :return: timeseries of range

    **Usage**

    Returns the range of the series (max - min) over rolling window:

    :math:`R_t = max(X_{t-w+1}:X_t) - min(X_{t-w+1}:X_t)`

    where :math:`w` is the size of the rolling window. If window is not provided, returns the range over the
    full series. If the window size is greater than the available data, will return range of all available values.

    **Examples**

    Range of price series over the last :math:`22` observations:

    >>> prices = generate_series(100)
    >>> range_(prices, 22)

    **See also**

    :func:`min_` :func:`max_`

    """
    w = normalize_window(x, w)
    assert x.index.is_monotonic_increasing, "series index is monotonic increasing"

    max = max_(x, Window(w.w, 0))
    min = min_(x, Window(w.w, 0))

    return apply_ramp(max - min, w)


@plot_function
def mean(x: pd.Series, w: Union[Window, int] = Window(None, 0)) -> pd.Series:
    """
    Arithmetic mean of series over given window

    :param x: series: timeseries
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value. Window size defaults to length of series.
    :return: timeseries of mean value

    **Usage**

    Calculates `arithmetic mean <https://en.wikipedia.org/wiki/Arithmetic_mean>`_ of the series over a rolling window

    :math:`R_t = \\frac{\sum_{i=t-w+1}^{t} X_i}{N}`

    where :math:`N` is the number of observations in each rolling window, :math:`w`. If window is not provided, computes
    rolling mean over the full series. If the window size is greater than the available data, will return mean of
    available values.

    **Examples**

    Generate price series and compute mean over :math:`22` observations

    >>> prices = generate_series(100)
    >>> mean(prices, 22)

    **See also**

    :func:`median` :func:`mode`

    """
    w = normalize_window(x, w)
    assert x.index.is_monotonic_increasing, "series index is monotonic increasing"
    if isinstance(w.w, pd.DateOffset):
        values = [x.loc[(x.index > idx - w.w) & (x.index <= idx)].mean() for idx in x.index]
        return apply_ramp(pd.Series(values, index=x.index), w)
    else:
        return apply_ramp(x.rolling(w.w, 0).mean(), w)


@plot_function
def median(x: pd.Series, w: Union[Window, int] = Window(None, 0)) -> pd.Series:
    """
    Median value of series over given window

    :param x: series: timeseries
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value. Window size defaults to length of series.
    :return: timeseries of median value

    **Usage**

    Computes the `median <https://en.wikipedia.org/wiki/Median>`_ value over a given window. For each window, this
    function will return the middle value when all elements in the window are sorted. If the number of observations in
    the window is even, will return the average of the middle two values. If the window size is greater than the
    available data, will return median of available values:

    :math:`d = \\frac{w-1}{2}`

    :math:`R_t = \\frac{X_{\lfloor t-d \\rfloor} + X_{\lceil t-d \\rceil}}{2}`

    where :math:`w` is the size of the rolling window. If window is not provided, computes median over the full series

    **Examples**

    Generate price series and compute median over :math:`22` observations

    >>> prices = generate_series(100)
    >>> median(prices, 22)

    **See also**

    :func:`mean` :func:`mode`
    """
    w = normalize_window(x, w)
    assert x.index.is_monotonic_increasing, "series index is monotonic increasing"
    if isinstance(w.w, pd.DateOffset):
        values = [x.loc[(x.index > idx - w.w) & (x.index <= idx)].median() for idx in x.index]
        return apply_ramp(pd.Series(values, index=x.index), w)
    else:
        return apply_ramp(x.rolling(w.w, 0).median(), w)


@plot_function
def mode(x: pd.Series, w: Union[Window, int] = Window(None, 0)) -> pd.Series:
    """
    Most common value in series over given window

    :param x: series: timeseries
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value. Window size defaults to length of series.
    :return: timeseries of mode value

    **Usage**

    Computes the `mode <https://en.wikipedia.org/wiki/Mode_(statistics)>`_ over a given window. For each window, this
    function will return the most common value of all elements in the window. If there are multiple values with the same
    frequency of occurrence, will return the smallest value.

    If window is not provided, computes mode over the full series.

    **Examples**

    Generate price series and compute mode over :math:`22` observations

    >>> prices = generate_series(100)
    >>> mode(prices, 22)

    **See also**

    :func:`mean` :func:`median`
    """
    w = normalize_window(x, w)
    assert x.index.is_monotonic_increasing, "series index is monotonic increasing"
    if isinstance(w.w, pd.DateOffset):
        values = [stats.mode(x.loc[(x.index > idx - w.w) & (x.index <= idx)]).mode[0] for idx in x.index]
        return apply_ramp(pd.Series(values, index=x.index), w)
    else:
        return apply_ramp(x.rolling(w.w, 0).apply(lambda y: stats.mode(y).mode, raw=True), w)


@plot_function
def sum_(x: pd.Series, w: Union[Window, int] = Window(None, 0)) -> pd.Series:
    """
    Rolling sum of series over given window

    :param x: series: timeseries
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value. Window size defaults to length of series.
    :return: timeseries of rolling sum

    **Usage**

    Calculate the sum of observations over a given rolling window. For each time, :math:`t`, returns the value
    of all observations from :math:`t-w+1` to :math:`t` summed together:

    :math:`R_t = \sum_{i=t-w+1}^{t} X_i`

    where :math:`w` is the size of the rolling window. If window is not provided, computes sum over the full series

    **Examples**

    Generate price series and compute rolling sum over :math:`22` observations

    >>> prices = generate_series(100)
    >>> sum_(prices, 22)

    **See also**

    :func:`product`

    """
    w = normalize_window(x, w)
    assert x.index.is_monotonic_increasing
    if isinstance(w.w, pd.DateOffset):
        values = [x.loc[(x.index > idx - w.w) & (x.index <= idx)].sum() for idx in x.index]
        return apply_ramp(pd.Series(values, index=x.index), w)
    else:
        return apply_ramp(x.rolling(w.w, 0).sum(), w)


@plot_function
def product(x: pd.Series, w: Union[Window, int] = Window(None, 0)) -> pd.Series:
    """
    Rolling product of series over given window

    :param x: series: timeseries
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value. Window size defaults to length of series.
    :return: timeseries of rolling product

    **Usage**

    Calculate the product of observations over a given rolling window. For each time, :math:`t`, returns the value
    of all observations from :math:`t-w+1` to :math:`t` multiplied together:

    :math:`R_t = \prod_{i=t-w+1}^{t} X_i`

    where :math:`w` is the size of the rolling window. If window is not provided, computes product over the full series

    **Examples**

    Generate price series and compute rolling sum over :math:`22` observations

    >>> prices = generate_series(100)
    >>> product(1+returns(prices))

    **See also**

    :func:`sum_`
    """
    w = normalize_window(x, w)
    assert x.index.is_monotonic_increasing
    if isinstance(w.w, pd.DateOffset):
        values = [x.loc[(x.index > idx - w.w) & (x.index <= idx)].agg(pd.Series.prod) for idx in x.index]
        return apply_ramp(pd.Series(values, index=x.index), w)
    else:
        return apply_ramp(x.rolling(w.w, 0).agg(pd.Series.prod), w)


@plot_function
def std(x: pd.Series, w: Union[Window, int] = Window(None, 0)) -> pd.Series:
    """
    Rolling standard deviation of series over given window

    :param x: series: timeseries
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value. Window size defaults to length of series.
    :return: timeseries of standard deviation

    **Usage**

    Provides `unbiased estimator <https://en.wikipedia.org/wiki/Unbiased_estimation_of_standard_deviation>`_ of sample
    `standard deviation <https://en.wikipedia.org/wiki/Standard_deviation>`_ over a rolling window:

    :math:`R_t = \sqrt{\\frac{1}{N-1} \sum_{i=t-w+1}^t (X_i - \overline{X_t})^2}`

    where :math:`N` is the number of observations in each rolling window, :math:`w`, and :math:`\overline{X_t}` is the
    mean value over the same window:

    :math:`\overline{X_t} = \\frac{\sum_{i=t-w+1}^{t} X_i}{N}`

    If window is not provided, computes standard deviation over the full series

    **Examples**

    Generate price series and compute standard deviation of returns over :math:`22` observations

    >>> prices = generate_series(100)
    >>> std(returns(prices), 22)

    **See also**

    :func:`sum` :func:`mean` :func:`var`

    """
    w = normalize_window(x, w)
    assert x.index.is_monotonic_increasing, "series index is monotonic increasing"
    if isinstance(w.w, pd.DateOffset):
        values = [x.loc[(x.index > idx - w.w) & (x.index <= idx)].std() for idx in x.index]
        return apply_ramp(pd.Series(values, index=x.index), w)
    else:
        return apply_ramp(x.rolling(w.w, 0).std(), w)


@plot_function
def var(x: pd.Series, w: Union[Window, int] = Window(None, 0)) -> pd.Series:
    """
    Rolling variance of series over given window

    :param x: series: timeseries
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value. Window size defaults to length of series.
    :return: timeseries of variance

    **Usage**

    Provides `unbiased estimator <https://en.wikipedia.org/wiki/Unbiased_estimation_of_standard_deviation>`_ of sample
    `variance <https://en.wikipedia.org/wiki/Variance>`_ over a rolling window:

    :math:`R_t = \\frac{1}{N-1} \sum_{i=t-w+1}^t (X_i - \overline{X_t})^2`

    where :math:`N` is the number of observations in each rolling window, :math:`w`, and :math:`\overline{X_t}` is the
    mean value over the same window:

    :math:`\overline{X_t} = \\frac{\sum_{i=t-w+1}^{t} X_i}{N}`

    If window is not provided, computes variance over the full series

    **Examples**

    Generate price series and compute variance of returns over :math:`22` observations

    >>> prices = generate_series(100)
    >>> var(returns(prices), 22)

    **See also**

    :func:`var` :func:`mean` :func:`std`

    """
    w = normalize_window(x, w)
    assert x.index.is_monotonic_increasing, "series index is monotonic increasing"
    if isinstance(w.w, pd.DateOffset):
        values = [x.loc[(x.index > idx - w.w) & (x.index <= idx)].var() for idx in x.index]
        return apply_ramp(pd.Series(values, index=x.index), w)
    else:
        return apply_ramp(x.rolling(w.w, 0).var(), w)


@plot_function
def cov(x: pd.Series, y: pd.Series, w: Union[Window, int] = Window(None, 0)) -> pd.Series:
    """
    Rolling co-variance of series over given window

    :param x: series: timeseries
    :param y: series: timeseries
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value. Window size defaults to length of series.
    :return: timeseries of covariance

    **Usage**

    Provides `unbiased estimator <https://en.wikipedia.org/wiki/Unbiased_estimation_of_standard_deviation>`_ of sample
    `co-variance <https://en.wikipedia.org/wiki/Covariance>`_ over a rolling window:

    :math:`R_t = \\frac{1}{N-1} \sum_{i=t-w+1}^t (X_i - \overline{X_t}) (Y_i - \overline{Y_t})`

    where :math:`N` is the number of observations in each rolling window, :math:`w`, and :math:`\overline{X_t}` and
    :math:`\overline{Y_t}` represent the sample mean of series :math:`X_t` and :math:`Y_t` over the same window:

    :math:`\overline{X_t} = \\frac{\sum_{i=t-w+1}^{t} X_i}{N}` and
    :math:`\overline{Y_t} = \\frac{\sum_{i=t-w+1}^{t} Y_i}{N}`

    If window is not provided, computes variance over the full series

    **Examples**

    Generate price series and compute variance of returns over :math:`22` observations

    >>> prices_x = generate_series(100)
    >>> prices_y = generate_series(100)
    >>> cov(returns(prices_x) returns(prices_y), 22)

    **See also**

    :func:`sum` :func:`mean` :func:`var`
    """
    w = normalize_window(x, w)
    assert x.index.is_monotonic_increasing, "series index is monotonic increasing"
    if isinstance(w.w, pd.DateOffset):
        values = [x.loc[(x.index > idx - w.w) & (x.index <= idx)].cov(y) for idx in x.index]
        return apply_ramp(pd.Series(values, index=x.index), w)
    else:
        return apply_ramp(x.rolling(w.w, 0).cov(y), w)


def _zscore(x):
    if x.size == 1:
        return 0

    return stats.zscore(x, ddof=1)[-1]


@plot_function
def zscores(x: pd.Series, w: Union[Window, int] = Window(None, 0)) -> pd.Series:
    """
    Rolling z-scores over a given window

    :param x: time series of prices
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value. Window size defaults to length of series.
    :return: timeseries of z-scores

    **Usage**

    Calculate `standard score <https://en.wikipedia.org/wiki/Standard_score>`_ of each value in series over given
    window. Standard deviation and sample mean are computed over the specified rolling window, then element is
    normalized to provide a rolling z-score:

    :math:`R_t = \\frac { X_t - \mu }{ \sigma }`

    Where :math:`\mu` and :math:`\sigma` are sample mean and standard deviation over the given window

    If window is not provided, computes z-score relative to mean and standard deviation over the full series

    **Examples**

    Generate price series and compute z-score of returns over :math:`22` observations

    >>> prices = generate_series(100)
    >>> zscores(returns(prices), 22)

    **See also**

    :func:`mean` :func:`std`

    """
    if x.size < 1:
        return x

    if isinstance(w, int):
        w = Window(w=w, r=w)
    if not w.w:
        if x.size == 1:
            return pd.Series([0.0], index=x.index)

        clean_series = x.dropna()
        zscore_series = pd.Series(stats.zscore(clean_series, ddof=1), clean_series.index)
        return interpolate(zscore_series, x, Interpolate.NAN)
    if not isinstance(w.w, int):
        w = normalize_window(x, w)
        values = [_zscore(x.loc[(x.index > idx - w.w) & (x.index <= idx)]) for idx in x.index]
        return apply_ramp(pd.Series(values, index=x.index), w)
    else:
        return apply_ramp(x.rolling(w.w, 0).apply(_zscore, raw=False), w)


@plot_function
def winsorize(x: pd.Series, limit: float = 2.5, w: Union[Window, int] = Window(None, 0)) -> pd.Series:
    """
    Limit extreme values in series

    :param x: time series of prices
    :param limit: max z-score of values
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value. Window size defaults to length of series.
    :return: timeseries of winsorized values

    **Usage**

    Cap and floor values in the series which have a z-score greater or less than provided value. This function will
    restrict the distribution of values. Calculates the sample standard deviation and adjusts values which
    fall outside the specified range to be equal to the upper or lower limits

    Lower and upper limits are defined as:

    :math:`upper = \mu + \sigma \\times limit`

    :math:`lower = \mu - \sigma \\times limit`

    Where :math:`\mu` and :math:`\sigma` are sample mean and standard deviation. The series is restricted by:

    :math:`R_t = max( min( X_t, upper), lower )`

    See `winsorising <https://en.wikipedia.org/wiki/Winsorizing>`_ for additional information

    **Examples**

    Generate price series and winsorize z-score of returns over :math:`22` observations

    >>> prices = generate_series(100)
    >>> winsorize(zscore(returns(prices), 22))

    **See also**

    :func:`zscore` :func:`mean` :func:`std`

    """
    w = normalize_window(x, w)

    if x.size < 1:
        return x

    assert w.w, "window is not 0"

    mu = x.mean()
    sigma = x.std()

    high = mu + sigma * limit
    low = mu - sigma * limit

    ret = ceil(x, high)
    ret = floor(ret, low)

    return apply_ramp(ret, w)


@plot_function
def generate_series(length: int) -> pd.Series:
    """
    Generate sample timeseries

    :param length: number of observations
    :return: date-based time series of randomly generated prices

    **Usage**

    Create timeseries from returns generated from a normally distributed random variables (IDD). Length determines the
    number of observations to be generated.

    Assume random variables :math:`R` which follow a normal distribution with mean :math:`0` and standard deviation
    of :math:`1`

    :math:`R \sim N(0, 1)`

    The timeseries is generated from these random numbers through:

    :math:`X_t = (1 + R)X_{t-1}`

    **Examples**

    Generate price series with 100 observations starting from today's date:

    >>> prices = generate_series(100)

    **See also**

    :func:`numpy.random.normal()`

    """
    levels = [100]
    dates = [datetime.date.today()]

    for i in range(length - 1):
        levels.append(levels[i] * 1 + numpy.random.normal())
        dates.append(datetime.date.fromordinal(dates[i].toordinal() + 1))

    return pd.Series(data=levels, index=dates)


@plot_function
def percentiles(x: pd.Series, y: pd.Series = None, w: Union[Window, int] = Window(None, 0)) -> pd.Series:
    """
    Rolling percentiles over given window

    :param x: value series
    :param y: distribution series
    :param w: Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value. Window size defaults to length of series.
    :return: timeseries of percentiles

    **Usage**

    Calculate `percentile rank <https://en.wikipedia.org/wiki/Percentile_rank>`_ of :math:`y` in the sample distribution
    of :math:`x` over a rolling window of length :math:`w`:

    :math:`R_t = \\frac{\sum_{i=t-N+1}^{t}{[X_i<{Y_t}]}+0.5\sum_{i=t-N+1}^{t}{[X_i={Y_t}]}}{N}\\times100\%`

    Where :math:`N` is the number of observations in a rolling window. If :math:`y` is not provided, calculates
    percentiles of :math:`x` over its historical values. If window length :math:`w` is not provided, uses an
    ever-growing history of values. If :math:`w` is greater than the available data size, returns empty.

    **Examples**

    Compute percentile ranks of a series in the sample distribution of a second series over :math:`22` observations

    >>> a = generate_series(100)
    >>> b = generate_series(100)
    >>> percentiles(a, b, 22)

    **See also**

    :func:`zscores`

    """
    w = normalize_window(x, w)
    if x.empty:
        return x

    if y is None:
        y = x.copy()

    res = pd.Series()
    for idx, val in y.iteritems():
        sample = x.loc[(x.index > idx - w.w) & (x.index <= idx)] if isinstance(w.w, pd.DateOffset) else x[:idx][-w.w:]
        res.loc[idx] = percentileofscore(sample, val, kind='mean')

    return apply_ramp(res, w)


class LinearRegression:

    """Ordinary least squares (OLS) Linear Regression"""

    def __init__(self, X: Union[pd.Series, List[pd.Series]], y: pd.Series, fit_intercept: bool = True):
        df = pd.concat(X, axis=1) if isinstance(X, list) else X.to_frame()
        df = sm.add_constant(df) if fit_intercept else df
        self._index_scope = range(0, len(df.columns)) if fit_intercept else range(1, len(df.columns) + 1)
        self._res = sm.OLS(y, df).fit()
        self._fit_intercept = fit_intercept

    def _convert_index(self, i: int):
        if i not in self._index_scope:
            raise ValueError('index {} out of range'.format(i))
        return 'const' if i == 0 else i - 1

    @plot_method
    def coefficient(self, i: int) -> float:
        """
        Estimated coefficient
        :param i: coefficient of which predictor to get. If intercept is used, start from 0, else start from 1
        :return: estimated coefficient of the i-th predictor
        """
        converted_i = self._convert_index(i)
        return self._res.params[converted_i]

    @plot_method
    def r_squared(self) -> float:
        """
        Coefficient of determination (R Squared)
        :return: R Squared
        """
        return self._res.rsquared

    @plot_method
    def fitted_values(self):
        """
        Fitted values
        :return: fitted values
        """
        return self._res.fittedvalues

    @plot_method
    def predict(self, X_predict: Union[pd.Series, List[pd.Series]]) -> pd.Series:
        """
        :param X_predict: the values for which to predict
        :return: predicted values
        """
        df = pd.concat(X_predict, axis=1) if isinstance(X_predict, list) else X_predict.to_frame()
        return self._res.predict(sm.add_constant(df) if self._fit_intercept else df)


class SIRModel:

    """SIR Compartmental model for transmission of infectious disease

    :param s: number of susceptible individuals in population
    :param i: number of infectious individuals in population
    :param r: number of recovered individuals in population
    :param n: total population size

    **Usage**

    Fit `SIR Model <https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology#The_SIR_model>`_ based on the
    population in each compartment over a given time period.

    The SIR models the movement of individuals between three compartments: susceptible (S), infected (I), and resistant
    (R). The model calibrates parameters :

    ===========   =======================================================
    Parameter     Description
    ===========   =======================================================
    S0            initial susceptible individuals
    I0            initial infected individuals
    R0            initial recovered individuals
    beta          Transmission rate from susceptible to infected
    gamma         Immunity rate from infected to resistant
    ===========   =======================================================

    The parameters beta and gamma model how fast people move from being susceptible to infected (beta), and
    subsequently from infected to resistant (gamma). This model can be used to forecast the populations of each
    compartment once calibrated

    """
    def __init__(self, s: pd.Series, i: pd.Series, r: pd.Series, n: Union[pd.Series, float],
                 end_date: date = None):

        self.s = s
        self.i = i
        self.r = r
        self.n = n

        if end_date is None:
            end_date = max(DataContext.current.end_date, s.index.max().date())

        data = np.array([s, i, r]).T

        beta_init = 0.9
        gamma_init = 0.01

        parameters, initial_conditions = SIR.get_parameters(s[0], i[0], r[0], n, beta=beta_init, gamma=gamma_init,
                                                            S0_fixed=True, I0_fixed=True, R0_fixed=True)

        self._model = PandemicModel(SIR, parameters=parameters, data=data,
                                    initial_conditions=initial_conditions)
        self._model.fit(verbose=False)

        last_date = s.index.max().date()
        predict_days = (end_date - last_date).days

        t = np.arange(data.shape[0] + predict_days)
        predict = self._model.solve(t, (self.s0(), self.i0(), self.r0()), (self.beta(), self.gamma(), n))

        predict_dates = s.index.union(pd.date_range(last_date, end_date))

        self._model.s_predict = pd.Series(predict[:, 0], predict_dates)
        self._model.i_predict = pd.Series(predict[:, 1], predict_dates)
        self._model.r_predict = pd.Series(predict[:, 2], predict_dates)

    @plot_method
    def s0(self):
        """
        Model calibration for initial susceptible individuals

        :return: initial susceptible individuals
        """
        return self._model.fitted_parameters['S0']

    @plot_method
    def i0(self):
        """
        Model calibration for initial infectious individuals

        :return: initial infectious individuals
        """
        return self._model.fitted_parameters['I0']

    @plot_method
    def r0(self):
        """
        Model calibration for initial recovered individuals

        :return: initial recovered individuals
        """
        return self._model.fitted_parameters['R0']

    @plot_method
    def beta(self):
        """
        Model calibration for transmission rate (susceptible to infected)

        :return: beta
        """
        return self._model.fitted_parameters['beta']

    @plot_method
    def gamma(self):
        """
        Model calibration for immunity (infected to resistant)

        :return: beta
        """
        return self._model.fitted_parameters['gamma']

    @plot_method
    def s_predict(self):
        """
        Model calibration for susceptible individuals through time

        :return: susceptible predict
        """
        return self._model.s_predict

    @plot_method
    def i_predict(self):
        """
        Model calibration for infected individuals through time

        :return: infected predict
        """
        return self._model.i_predict

    @plot_method
    def r_predict(self):
        """
        Model calibration for recovered individuals through time

        :return: infected predict
        """
        return self._model.r_predict


class SEIRModel(SIRModel):

    """SEIR Compartmental model for transmission of infectious disease

    :param s: number of susceptible individuals in population
    :param e: number of exposed individuals in population
    :param i: number of infectious individuals in population
    :param r: number of recovered individuals in population
    :param n: total population size

    **Usage**

    Fit `SEIR Model <https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology#The_SEIR_model`_ based on the
    population in each compartment over a given time period.

    The SEIR models the movement of individuals between four compartments: susceptible (S), exposed (E), infected (I),
    and resistant (R). The model calibrates parameters :

    ===========   =======================================================
    Parameter     Description
    ===========   =======================================================
    S0            initial susceptible individuals
    E0            initial exposed individuals
    I0            initial infected individuals
    R0            initial recovered individuals
    beta          Transmission rate from susceptible to exposed
    gamma         Immunity rate from infected to resistant
    sigma         Immunity rate from exposed to infected
    ===========   =======================================================

    The parameters beta, gamma, and sigma, model how fast people move from being susceptible to exposed (beta),
    from exposed to infected (sigma), and subsequently from infected to resistant (gamma). This model can be used to
    predict the populations of each compartment once calibrated.

    """
    def __init__(self, s: pd.Series, e: pd.Series, i: pd.Series, r: pd.Series, n: Union[pd.Series, float],
                 end_date: date = None):

        self.s = s
        self.e = e
        self.i = i
        self.r = r
        self.n = n

        data = np.array([s, e, i, r]).T

        if end_date is None:
            end_date = max(DataContext.current.end_date, s.index.max().date())

        beta_init = 0.9
        gamma_init = 0.01
        sigma_init = 0.2

        parameters, initial_conditions = SEIR.get_parameters(s[0], e[0], i[0], r[0], n, beta=beta_init,
                                                             gamma=gamma_init, sigma=sigma_init,
                                                             S0_fixed=True, I0_fixed=True,
                                                             R0_fixed=True, E0_fixed=True, S0_max=5e6, I0_max=5e6,
                                                             E0_max=10e6, R0_max=10e6)

        self._model = PandemicModel(SEIR, parameters=parameters, data=data,
                                    initial_conditions=initial_conditions)
        self._model.fit(verbose=False)

        last_date = s.index.max().date()
        predict_days = (end_date - last_date).days

        t = np.arange(data.shape[0] + predict_days)
        predict = self._model.solve(t, (self.s0(), self.e0(), self.i0(), self.r0()),
                                    (self.beta(), self.gamma(), self.sigma(), n))

        predict_dates = s.index.union(pd.date_range(last_date, end_date))

        self._model.s_predict = pd.Series(predict[:, 0], predict_dates)
        self._model.e_predict = pd.Series(predict[:, 1], predict_dates)
        self._model.i_predict = pd.Series(predict[:, 2], predict_dates)
        self._model.r_predict = pd.Series(predict[:, 3], predict_dates)

    @plot_method
    def e0(self):
        """
        Model calibration for initial exposed individuals

        :return: initial exposed individuals
        """
        return self._model.fitted_parameters['E0']

    @plot_method
    def beta(self):
        """
        Model calibration for transmission rate (susceptible to exposed)

        :return: beta
        """
        return self._model.fitted_parameters['beta']

    @plot_method
    def gamma(self):
        """
        Model calibration for immunity (infected to resistant)

        :return: gamma
        """
        return self._model.fitted_parameters['gamma']

    @plot_method
    def sigma(self):
        """
        Model calibration for infection rate (exposed to infected)

        :return: sigma
        """
        return self._model.fitted_parameters['sigma']

    @plot_method
    def e_predict(self):
        """
        Model calibration for exposed individuals through time

        :return: exposed predict
        """
        return self._model.e_predict
