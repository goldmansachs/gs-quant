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
from datetime import date
from math import isclose

import pytest
import pandas as pd
import numpy as np

from pandas import Timestamp
from pandas.util.testing import assert_series_equal
from numpy.testing import assert_raises, assert_array_equal, assert_allclose

import gs_quant.timeseries as ts

def test_arima_fit():
    test_dict = {
                'High': 
                    {Timestamp('1989-01-03 00:00:00'): 3.575721263885498,
                    Timestamp('1989-01-04 00:00:00'): 3.5857372283935547,
                    Timestamp('1989-01-05 00:00:00'): 3.62580132484436,
                    Timestamp('1989-01-06 00:00:00'): 3.62580132484436,
                    Timestamp('1989-01-09 00:00:00'): 3.575721263885498,
                    Timestamp('1989-01-10 00:00:00'): 3.575721263885498,
                    Timestamp('1989-01-11 00:00:00'): 3.5657050609588623,
                    Timestamp('1989-01-12 00:00:00'): 3.635817289352417,
                    Timestamp('1989-01-13 00:00:00'): 3.615785360336304,
                    Timestamp('1989-01-16 00:00:00'): 3.615785360336304,
                    Timestamp('1989-01-17 00:00:00'): 3.635817289352417,
                    Timestamp('1989-01-18 00:00:00'): 3.675881385803223,
                    Timestamp('1989-01-19 00:00:00'): 3.695913553237915,
                    Timestamp('1989-01-20 00:00:00'): 3.665865421295166,
                    Timestamp('1989-01-23 00:00:00'): 3.675881385803223,
                    Timestamp('1989-01-24 00:00:00'): 3.675881385803223,
                    Timestamp('1989-01-25 00:00:00'): 3.695913553237915,
                    Timestamp('1989-01-26 00:00:00'): 3.7760417461395264,
                    Timestamp('1989-01-27 00:00:00'): 3.8561699390411377,
                    Timestamp('1989-01-30 00:00:00'): 3.8561699390411377},
                'Low': 
                    {Timestamp('1989-01-03 00:00:00'): 3.4855768680572514,
                    Timestamp('1989-01-04 00:00:00'): 3.5356571674346924,
                    Timestamp('1989-01-05 00:00:00'): 3.575721263885498,
                    Timestamp('1989-01-06 00:00:00'): 3.575721263885498,
                    Timestamp('1989-01-09 00:00:00'): 3.5356571674346924,
                    Timestamp('1989-01-10 00:00:00'): 3.5356571674346924,
                    Timestamp('1989-01-11 00:00:00'): 3.5256409645080566,
                    Timestamp('1989-01-12 00:00:00'): 3.5456731319427486,
                    Timestamp('1989-01-13 00:00:00'): 3.5857372283935547,
                    Timestamp('1989-01-16 00:00:00'): 3.5957531929016118,
                    Timestamp('1989-01-17 00:00:00'): 3.5857372283935547,
                    Timestamp('1989-01-18 00:00:00'): 3.615785360336304,
                    Timestamp('1989-01-19 00:00:00'): 3.655849456787109,
                    Timestamp('1989-01-20 00:00:00'): 3.62580132484436,
                    Timestamp('1989-01-23 00:00:00'): 3.615785360336304,
                    Timestamp('1989-01-24 00:00:00'): 3.615785360336304,
                    Timestamp('1989-01-25 00:00:00'): 3.655849456787109,
                    Timestamp('1989-01-26 00:00:00'): 3.665865421295166,
                    Timestamp('1989-01-27 00:00:00'): 3.79607367515564,
                    Timestamp('1989-01-30 00:00:00'): 3.786057710647583},
                'Open': 
                    {Timestamp('1989-01-03 00:00:00'): 3.575721263885498,
                    Timestamp('1989-01-04 00:00:00'): 3.5556890964508057,
                    Timestamp('1989-01-05 00:00:00'): 3.5857372283935547,
                    Timestamp('1989-01-06 00:00:00'): 3.605769157409668,
                    Timestamp('1989-01-09 00:00:00'): 3.5456731319427486,
                    Timestamp('1989-01-10 00:00:00'): 3.575721263885498,
                    Timestamp('1989-01-11 00:00:00'): 3.5456731319427486,
                    Timestamp('1989-01-12 00:00:00'): 3.5456731319427486,
                    Timestamp('1989-01-13 00:00:00'): 3.605769157409668,
                    Timestamp('1989-01-16 00:00:00'): 3.5957531929016118,
                    Timestamp('1989-01-17 00:00:00'): 3.5957531929016118,
                    Timestamp('1989-01-18 00:00:00'): 3.635817289352417,
                    Timestamp('1989-01-19 00:00:00'): 3.6858973503112793,
                    Timestamp('1989-01-20 00:00:00'): 3.665865421295166,
                    Timestamp('1989-01-23 00:00:00'): 3.6458332538604736,
                    Timestamp('1989-01-24 00:00:00'): 3.62580132484436,
                    Timestamp('1989-01-25 00:00:00'): 3.6858973503112793,
                    Timestamp('1989-01-26 00:00:00'): 3.675881385803223,
                    Timestamp('1989-01-27 00:00:00'): 3.79607367515564,
                    Timestamp('1989-01-30 00:00:00'): 3.806089639663696},
                'Close': 
                    {Timestamp('1989-01-03 00:00:00'): 3.5256409645080566,
                    Timestamp('1989-01-04 00:00:00'): 3.5857372283935547,
                    Timestamp('1989-01-05 00:00:00'): 3.575721263885498,
                    Timestamp('1989-01-06 00:00:00'): 3.575721263885498,
                    Timestamp('1989-01-09 00:00:00'): 3.575721263885498,
                    Timestamp('1989-01-10 00:00:00'): 3.5556890964508057,
                    Timestamp('1989-01-11 00:00:00'): 3.5556890964508057,
                    Timestamp('1989-01-12 00:00:00'): 3.605769157409668,
                    Timestamp('1989-01-13 00:00:00'): 3.605769157409668,
                    Timestamp('1989-01-16 00:00:00'): 3.5957531929016118,
                    Timestamp('1989-01-17 00:00:00'): 3.62580132484436,
                    Timestamp('1989-01-18 00:00:00'): 3.675881385803223,
                    Timestamp('1989-01-19 00:00:00'): 3.665865421295166,
                    Timestamp('1989-01-20 00:00:00'): 3.6458332538604736,
                    Timestamp('1989-01-23 00:00:00'): 3.62580132484436,
                    Timestamp('1989-01-24 00:00:00'): 3.675881385803223,
                    Timestamp('1989-01-25 00:00:00'): 3.675881385803223,
                    Timestamp('1989-01-26 00:00:00'): 3.756009578704834,
                    Timestamp('1989-01-27 00:00:00'): 3.79607367515564,
                    Timestamp('1989-01-30 00:00:00'): 3.846153736114502},
                'Volume': 
                    {Timestamp('1989-01-03 00:00:00'): 21873600.0,
                    Timestamp('1989-01-04 00:00:00'): 13487100.0,
                    Timestamp('1989-01-05 00:00:00'): 20733000.0,
                    Timestamp('1989-01-06 00:00:00'): 20654400.0,
                    Timestamp('1989-01-09 00:00:00'): 21478000.0,
                    Timestamp('1989-01-10 00:00:00'): 15541300.0,
                    Timestamp('1989-01-11 00:00:00'): 11465300.0,
                    Timestamp('1989-01-12 00:00:00'): 26481300.0,
                    Timestamp('1989-01-13 00:00:00'): 10236000.0,
                    Timestamp('1989-01-16 00:00:00'): 8888200.0,
                    Timestamp('1989-01-17 00:00:00'): 12934200.0,
                    Timestamp('1989-01-18 00:00:00'): 25965800.0,
                    Timestamp('1989-01-19 00:00:00'): 25556500.0,
                    Timestamp('1989-01-20 00:00:00'): 13779100.0,
                    Timestamp('1989-01-23 00:00:00'): 13680500.0,
                    Timestamp('1989-01-24 00:00:00'): 16870400.0,
                    Timestamp('1989-01-25 00:00:00'): 16959000.0,
                    Timestamp('1989-01-26 00:00:00'): 29040900.0,
                    Timestamp('1989-01-27 00:00:00'): 50615100.0,
                    Timestamp('1989-01-30 00:00:00'): 27567000.0},
                'Adj Close': 
                    {Timestamp('1989-01-03 00:00:00'): 0.13199026882648468,
                    Timestamp('1989-01-04 00:00:00'): 0.13424012064933774,
                    Timestamp('1989-01-05 00:00:00'): 0.1338651180267334,
                    Timestamp('1989-01-06 00:00:00'): 0.1338651180267334,
                    Timestamp('1989-01-09 00:00:00'): 0.1338651180267334,
                    Timestamp('1989-01-10 00:00:00'): 0.13311512768268585,
                    Timestamp('1989-01-11 00:00:00'): 0.13311512768268585,
                    Timestamp('1989-01-12 00:00:00'): 0.13499003648757935,
                    Timestamp('1989-01-13 00:00:00'): 0.13499003648757935,
                    Timestamp('1989-01-16 00:00:00'): 0.13461506366729736,
                    Timestamp('1989-01-17 00:00:00'): 0.13573989272117615,
                    Timestamp('1989-01-18 00:00:00'): 0.13761481642723086,
                    Timestamp('1989-01-19 00:00:00'): 0.13723985850811005,
                    Timestamp('1989-01-20 00:00:00'): 0.13648992776870728,
                    Timestamp('1989-01-23 00:00:00'): 0.13573989272117615,
                    Timestamp('1989-01-24 00:00:00'): 0.13761481642723086,
                    Timestamp('1989-01-25 00:00:00'): 0.13761481642723086,
                    Timestamp('1989-01-26 00:00:00'): 0.14061467349529266,
                    Timestamp('1989-01-27 00:00:00'): 0.14211450517177582,
                    Timestamp('1989-01-30 00:00:00'): 0.14398930966854095}}
    test_df = pd.DataFrame(test_dict)
    arima = ts.arima()
    arima.fit(test_df, train_size=0.8, freq='B', q_vals=[0])
    transformed_test_df = arima.transform(test_df)

    for col in transformed_test_df.keys():
        count_nans = arima.best_params[col].p + arima.best_params[col].d
        assert(count_nans == transformed_test_df[col].isna().sum())

    # Test (1,1,0) Model
    diff_test_df_high = test_df['High'].diff()
    assert(transformed_test_df['High'][2] == (arima.best_params['High'].const + diff_test_df_high[1] * arima.best_params['High'].ar_coef[0]))
    assert(transformed_test_df['High'][3] == (arima.best_params['High'].const + diff_test_df_high[2] * arima.best_params['High'].ar_coef[0]))
    assert(transformed_test_df['High'][-1] == (arima.best_params['High'].const + diff_test_df_high[-2] * arima.best_params['High'].ar_coef[0]))

    # Test (2,1,0) Model
    diff_test_df_low = test_df['Low'].diff()
    assert(isclose(transformed_test_df['Low'][3], (arima.best_params['Low'].const + diff_test_df_low[2] * arima.best_params['Low'].ar_coef[0] +  diff_test_df_low[1] * arima.best_params['Low'].ar_coef[1]), abs_tol=1e-8))
    assert(isclose(transformed_test_df['Low'][4], (arima.best_params['Low'].const + diff_test_df_low[3] * arima.best_params['Low'].ar_coef[0] +  diff_test_df_low[2] * arima.best_params['Low'].ar_coef[1]), abs_tol=1e-8))
    assert(isclose(transformed_test_df['Low'][-1], (arima.best_params['Low'].const + diff_test_df_low[-2] * arima.best_params['Low'].ar_coef[0] +  diff_test_df_low[-3] * arima.best_params['Low'].ar_coef[1]), abs_tol=1e-8))

    # Test (1,2,0) Model
    diff_test_df_close = test_df['Close'].diff()[1:].diff()
    first_day = pd.Series([np.nan])
    first_day.index = [diff_test_df_close.index[0] - pd.DateOffset(days=1)]
    first_day.name = 'Close'
    diff_test_df_close = pd.concat([first_day, diff_test_df_close])  
    diff_test_df_close.index.name = "Date"

    assert(transformed_test_df['Close'][4] == (arima.best_params['Close'].const + diff_test_df_close[3] * arima.best_params['Close'].ar_coef[0]))
    assert(transformed_test_df['Close'][5] == (arima.best_params['Close'].const + diff_test_df_close[4] * arima.best_params['Close'].ar_coef[0]))
    assert(transformed_test_df['Close'][-1] == (arima.best_params['Close'].const+ diff_test_df_close[-2] * arima.best_params['Close'].ar_coef[0]))
    
    # Test (0,2,0) Model
    diff_test_df_volumne = test_df['Volume'].diff()[1:].diff()
    first_day = pd.Series([np.nan])
    first_day.index = [diff_test_df_volumne.index[0] - pd.DateOffset(days=1)]
    first_day.name = 'Volume'
    diff_test_df_volumne = pd.concat([first_day, diff_test_df_volumne])  
    diff_test_df_volumne.index.name = "Date"
    assert(transformed_test_df['Volume'][2] == arima.best_params['Volume'].const + diff_test_df_volumne[2])

test_arima_fit()