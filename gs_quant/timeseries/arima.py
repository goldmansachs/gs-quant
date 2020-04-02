# Copyright 2020 Goldman Sachs.
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

from dataclasses import dataclass
from typing import Iterable, Optional, Union, Tuple

import itertools
import datetime as dt
import pandas as pd
import numpy as np
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tools.eval_measures import mse


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
