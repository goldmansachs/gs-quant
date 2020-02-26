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

from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Optional, Union, Tuple

import itertools
import datetime as dt
import pandas as pd
import numpy as np
from tqdm import tqdm
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
    to normalize and forecast time series data. ARIMA has 3 parameters: (p, d, q)
    where:
        :p is the number of autoregressive terms
        :d is the number of nonseasonal differences
        :q is the number of lagged forecast errors in the prediction equation
    
    An ARIMA model is selected from the Catesian product of sets p, q, and d. The 
    time series is split into train and test sets and an ARIMA model is fit for 
    every combination on the training set. The model with the lowest mean-squared 
    error (MSE) on the test set is selected as the best model. The original 
    times series can then be transformed by the best model.

    Autoregressive components are past values of the variable of interest. An 
    AR(p) model with order p = 1 may be written as X(t) = A(1) * X(t-1) + E(t),
    where
        :X(t) is the time series under investigation 
        :A(1) is the autoregressive parameter
        :X(t-1) is the time series lagged 1 period
        :E(t) is the error term of the model or white noise

    In other words, any value in X(t) can be explained using a linear 
    combination of the past value T(t-1) plus some error term E(t). X(t)
    could also be a linear combination of more than one past value: 
    X(t) = A(1) * X(t-1) + A(2) * X(t-2) + E(t).

    Differencing is a way of making a non-stationary time series stationary. This 
    is done by computing the differences between consuective observations 
    (subtracting the observation from the current period from the previous one).
    Differencing can help stabilize the mean of a time series by removing changes 
    in the level of a time series, which reduces trend and seasonality. If the 
    transformation is done once, then the data has been "first differenced". The 
    same transformation can be done again, so the data would be "second 
    differenced".

    Moving average components uses past forecast errors E(t). In other words,
    X(t) can be thought of as a weighted moving average of the past forecast 
    errors: X(t) = c + E(t) + W(1)*E(t-1) + ... + W(q)*E(t-q).
    """

    def __init__(self):
        self.best_params = {}
    

    def _evaluate_arima_model(self, X: Union[pd.Series, pd.DataFrame], arima_order: Tuple[int, int, int], train_size: float, freq: str) -> Tuple[float, dict]:
        train_size = int(len(X) * train_size)
        train, test = X[0:train_size].astype(float), X[train_size:].astype(float)

        model = ARIMA(train, order=arima_order, freq=freq)
        model_fit = model.fit(disp=False, method='css', trend="nc")
        ar_coef = model_fit.arparams
        ma_coef = model_fit.maparams
        resid = model_fit.resid

        model_params = model_fit.params.to_dict()
        const = model_params.get("const", 0)

        # calculate test error
        yhat = model_fit.forecast(len(test))[0]
        error = mse(test, yhat)

        return error, const, ar_coef, ma_coef, resid


    def fit(self, X: Union[pd.Series, pd.DataFrame], train_size: float, p_vals: list = [0,1,2], d_vals: list=[0,1,2], q_vals: list=[0,1,2], freq: str=None) -> arima: 
        """
        Train a combination of ARIMA models. If pandas DataFrame, finds the 
        best arima model parameters for each column. If pandas Series, finds 
        the best arima model parameters for the series.

        :param X: time series to be operated on; required parameter
        :param train_size: between 0.0 and 1.0 and represents the proportion of the dataset to include in the train split
        :p_vals: number of autoregressive terms to search; default is [0,1,2]
        :d_vals: number of differences to search; default is [0,1,2]
        :q_vals: number of lagged forecast to search; always [0,1,2]
        :freq: frequency of time series, default is None
        :return: self
        """

        if isinstance(X, pd.Series): X = X.to_frame()

        if isinstance(X, pd.DataFrame):
            for series_id in tqdm(X.columns):
                series = X[series_id]
                best_score, best_order, best_const, best_ar_coef, best_ma_coef, best_resid = float("inf"), None, None, None, None, None
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

                self.best_params[series_id] = ARIMA_BestParams(freq=freq,
                                                               p=p, 
                                                               d=d, 
                                                               q=q,
                                                               const=best_const,
                                                               ar_coef=best_ar_coef,
                                                               ma_coef=best_ma_coef,
                                                               resid=best_resid,
                                                               series=series)
        else:
            raise ValueError("Not DataFrame or Series!")
        return self 
    

    # Helper Function to Difference Time Series n Times
    def _difference(self, X: pd.Series, d: int):
        if d == 0:
            return X
        elif d == 1:
            return X.diff()
        else:
            return self._difference(X.diff(), d-1)


    # Helper Function to Calculate AutoRegressive(AR) Component
    def _lagged_values(self, X: pd.Series, p: int, ar_coef: list):
        if p == 0:
            return X
        elif p > 0:
            transformed_df = pd.concat([X.copy().shift(periods=i) for i in range(1, p+1)], axis=1)
            transformed_df = transformed_df.dot(ar_coef)
        return transformed_df

    # Helper Function to Calculate Residuals/MA Component
    def _calculate_residuals(self, X_ar: pd.Series, X_diff: pd.Series, p: int, d: int, q: int, ar_coef: list, ma_coef: list, freq: str):
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


    # Helper Function to Transform Series
    def _arima_transform_series(self, X: pd.Series, p: int, d: int, q:int, const:float, ar_coef:list, ma_coef:list, resid:list, freq:str) -> pd.Series:
        
        # Difference first
        X_diff = self._difference(X, d)
        
        # Calculate Autoregressive Component
        X_diff_ar = self._lagged_values(X_diff, p, ar_coef)

        # Caluclate Residuals and Moving Average Component
        calcualted_resid, X_diff_ar_ma = self._calculate_residuals(X_diff_ar, X_diff, p, d, q, ar_coef, ma_coef, freq)
        
        # Check that calculated residuals are close with ARIMA statsmodels residuals
        residuals_df = pd.concat([calcualted_resid, resid], axis=1, join='inner')
        assert(np.allclose(residuals_df[residuals_df.columns[0]], residuals_df[residuals_df.columns[1]]))
        
        return X_diff_ar_ma


    # Helper Function to Transform DataFrame
    def _arima_transform_df(self, X: pd.DataFrame) -> pd.DataFrame:
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
            
            series[series_id] = self._arima_transform_series(X[series_id], p=p, d=d, q=q, const=const, ar_coef=ar_coef, ma_coef=ma_coef, resid=resid, freq=freq)
        return pd.DataFrame(series)
   

    def transform(self, X: Union[pd.Series, pd.DataFrame]) -> Union[pd.DataFrame]:
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
            raise ValueError("Not DataFrame or Series!")

        return transformed
