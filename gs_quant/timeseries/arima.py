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
#
#
# Chart Service will attempt to make public functions (not prefixed with _) from this module available. Such functions
# should be fully documented: docstrings should describe parameters and the return value, and provide a 1-line
# description. Type annotations should be provided for parameters.

from __future__ import annotations
from typing import Iterable, Optional, Union, Tuple

import pandas as pd
import numpy as np
from tqdm import tqdm
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error


"""ARIMA is the Autoregressive Integrated Moving Average Model and is used 
to normalize and forecast time series data. ARIMA here is used without the 
moving averages component, so predictions of future values of a 
series is done by regressing on its own lagged values. ARIMA has 3 
parameters: (p, d, q) where:
    :p is the number of autoregressive terms
    :d is the number of nonseasonal differences
    :q is the number of lagged forecast errors in the prediction equation
    
An ARIMA is selected from 9 possible combinations: (0,0,0), (1,0,0), 
(2,0,0), (0,1,0), (1,1,0), (2,1,0), (0,2,0), (1,2,0), (2,2,0). The time 
series is split into train and test sets and an ARIMA model is fit for every
combination on the training set. The model with the lowest mean-squared 
error (MSE) on the test set is selected as the best model. The original 
times series is then transformed by this model.

Autoregressive components are past values of the variable of interest. An 
AR(p) model with order p = 1 may be written as Y(t) = A(1) * Y(t-1) + E(t),
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
differenced"."""


class arima():
    """
    An ARIMA class used to normalize time series data.
    """

    def __init__(self):
        self.best_params = {}
    
    def _evaluate_arima_model(self, X: Union[pd.Series, pd.DataFrame], arima_order: Tuple[int, int, int], train_size: float, freq: str) -> Tuple[float, dict]:
        train_size = int(len(X) * train_size)
        train, test = X[0:train_size].astype(float), X[train_size:].astype(float)

        model = ARIMA(train, order=arima_order, freq=freq)
        model_fit = model.fit(disp=0)
        yhat = model_fit.forecast(len(test))[0]

        model_params = model_fit.params

        # calculate test error
        mse = mean_squared_error(test, yhat)
        
        return mse, model_params
    
    def fit(self, X: Union[pd.Series, pd.DataFrame], train_size: float, p_vals: list = [0,1,2], d_vals: list=[0,1,2], q_vals: list=[0], freq: str=None) -> arima: 
        """
        Train a combination of ARIMA models. If pandas DataFrame, finds the 
        best arima model parameters for each column. If pandas Series, finds 
        the best arima model parameters for the series.

        :param X: time series to be operated on; required parameter
        :param train_size: between 0.0 and 1.0 and represents the proportion of the dataset to include in the train split
        :p_vals: number of autoregressive terms to search; default is [0,1,2]
        :d_vals: number of differences to search; default is [0,1,2]
        :q_vals: number of lagged forecast to search; always [0]
        :freq: frequency of time series, default is None
        :return: self
        """

        if isinstance(X, pd.DataFrame):
            for series_id in tqdm(X.columns):
                series = X[series_id]
                best_score, best_cfg, best_params = float("inf"), None, None
                for p in p_vals:
                    for d in d_vals:
                        for q in q_vals:
                            order = (p, d, q)
                            try:
                                mse, model_params = self._evaluate_arima_model(series, order, train_size, freq)
                                if mse < best_score:
                                    best_score = mse
                                    best_cfg = order
                                    best_params = model_params
                            except Exception as e:
                                print('   {}'.format(e))
                                continue
                self.best_params[series_id] = {"p": best_cfg[0], 
                                               "d": best_cfg[1], 
                                               "q": best_cfg[2],
                                               "best_params": best_params.to_dict(), 
                                               "first_val": series[0], 
                                               "second_val": series[1], 
                                               "third_val": series[2], 
                                               "last_val": series[-1]}
        elif isinstance(X, pd.Series):
            series = X
            best_score, best_cfg, best_params = float("inf"), None, None
            for p in p_vals:
                for d in d_vals:
                    for q in q_vals:
                        order = (p, d, q)
                        try:
                            mse, model_params = self._evaluate_arima_model(series, order, train_size, freq)
                            if mse < best_score:
                                best_score = mse
                                best_cfg = order
                                best_params = model_params
                        except Exception as e:
                            print('   {}'.format(e))
                            continue
            
            self.best_params['y'] = {"p": best_cfg[0], 
                                             "d": best_cfg[1], 
                                             "q": best_cfg[2],
                                             "best_params": best_params.to_dict(), 
                                             "first_val": series.iloc[0], 
                                             "second_val": series.iloc[1], 
                                             "third_val": series.iloc[2], 
                                             "last_val": series.iloc[-1]}
        else:
            raise ValueError("Not DataFrame or Series!")
        
        return self 
    
    def _arima_transform_series(self, X: pd.Series, p: int, d: int, c:float, ar1: float=None, ar2: float=None) -> pd.Series:
        # Difference first
        if d == 0:
            pass
        elif d == 1:
            X = X.diff()
        elif d == 2:
            X = X.diff()[1:].diff()
            first_day = pd.Series([np.nan])

            first_day.index = [X.index[0] - pd.DateOffset(days=1)]
            first_day.name = X.name
            X = pd.concat([first_day, X])  
            X.index.name = "Date"
        else:
            raise ValueError("d is not 0, 1, or 2")

        # Create copy of transformed array
        transformed = X.copy()

        if p == 0:
            return transformed 
        elif p == 1:
            for idx, val in enumerate(list(X)[1:], start=1):
                lag1_val = X.iloc[idx-1]
                transformed.iloc[idx] = c + (ar1 * lag1_val)

            transformed.iloc[0] = np.nan

            return transformed
        elif p == 2:
            for idx, val in enumerate(list(X)[2:], start=2):
                lag1_val = X.iloc[idx-1]
                lag2_val = X.iloc[idx-2]
                
                transformed.iloc[idx] = c + (ar1 * lag1_val) + (ar2 * lag2_val)

            transformed.iloc[0] = np.nan
            transformed.iloc[1] = np.nan
        
        return transformed


    def _arima_transform_df(self, X: pd.DataFrame, p: int, d: int, c:float, ar1: float=None, ar2: float=None) -> pd.DataFrame:
        # Difference first
        if d == 0:
            pass
        elif d == 1:
            X = X.diff()
        elif d == 2:
            X = X.diff()[1:].diff()
            first_day = pd.Series([np.nan])

            first_day.index = [X.index[0] - pd.DateOffset(days=1)]
            first_day.name = X.name
            X = pd.concat([first_day, X])  
            X.index.name = "Date"
        else:
            raise ValueError("d is not 0, 1, or 2")

        # Create copy of transformed array
        transformed = X.copy()

        if p == 0:
            return transformed 
        elif p == 1:
            for idx, val in enumerate(list(X.iteritems())[1:], start=1):
                curr_date = val[0]
                lag1_val = X.loc[X.index[idx-1]]
                transformed[curr_date] = c + (ar1 * lag1_val)
            transformed[transformed.index[0]] = np.nan
            return transformed
        elif p == 2:
            for idx, val in enumerate(list(X.iteritems())[2:], start=2):
                curr_date = val[0]
                lag1_val = X.loc[X.index[idx-1]]
                lag2_val = X.loc[X.index[idx-2]]

                transformed[curr_date] = c + (ar1 * lag1_val) + (ar2 * lag2_val)

            transformed[transformed.index[0]] = np.nan
            transformed[transformed.index[1]] = np.nan

        return transformed
    
    
    def transform(self, X: Union[pd.Series, pd.DataFrame]) -> Union[pd.Series, pd.DataFrame]:
        """
        Transform a series based on the best ARIMA found from .fit(). If input 
        is DataFrame, returns a transformed DataFrame. 
        If Series, returns a transformed Series.

        :param X: time series to be operated on; required parameter
        :return: DataFrame or Series
        """

        series = {}
        for series_id in self.best_params.keys():
            p = self.best_params[series_id]["p"]
            d = self.best_params[series_id]["d"]
            q = self.best_params[series_id]["q"]

            first_val = self.best_params[series_id]['first_val']
            second_val = self.best_params[series_id]['second_val']
            third_val = self.best_params[series_id]['third_val']
            last_val = self.best_params[series_id]['last_val']

            try:
                const = self.best_params[series_id]["best_params"]["const"]
            except:
                const = 0

            if d == 0:
                if p == 0:
                    lag1_coeff = 0
                    lag2_coeff = 0
                elif p == 1:
                    lag1_coeff = self.best_params[series_id]["best_params"]["ar.L1.{}".format(series_id)]
                    lag2_coeff = 0
                elif p == 2:
                    lag1_coeff = self.best_params[series_id]["best_params"]["ar.L1.{}".format(series_id)]
                    lag2_coeff = self.best_params[series_id]["best_params"]["ar.L2.{}".format(series_id)]
            elif d == 1:
                if p == 0:
                    lag1_coeff = 0
                    lag2_coeff = 0
                elif p == 1:
                    lag1_coeff = self.best_params[series_id]["best_params"]["ar.L1.D.{}".format(series_id)]
                    lag2_coeff = 0
                elif p == 2:
                    lag1_coeff = self.best_params[series_id]["best_params"]["ar.L1.D.{}".format(series_id)]
                    lag2_coeff = self.best_params[series_id]["best_params"]["ar.L2.D.{}".format(series_id)]
            elif d == 2:
                if p == 0:
                    lag1_coeff = 0
                    lag2_coeff = 0
                elif p == 1:
                    lag1_coeff = self.best_params[series_id]["best_params"]["ar.L1.D2.{}".format(series_id)]
                    lag2_coeff = 0
                elif p == 2:
                    lag1_coeff = self.best_params[series_id]["best_params"]["ar.L1.D2.{}".format(series_id)]
                    lag2_coeff = self.best_params[series_id]["best_params"]["ar.L2.D2.{}".format(series_id)]

            if isinstance(X, pd.DataFrame):
                new_series = self._arima_transform_df(X[series_id], p=p, d=d, c=const, ar1=lag1_coeff, ar2=lag2_coeff)
                series[series_id] = new_series
            elif isinstance(X, pd.Series):
                new_series = self._arima_transform_series(X, p=p, d=d, c=const, ar1=lag1_coeff, ar2=lag2_coeff)
                return new_series

        return pd.DataFrame.from_dict(series)
