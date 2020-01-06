
"""
Copyright 2019 Goldman Sachs.
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

import numpy as np
# import cvxopt
import scipy.optimize
from dateutil.relativedelta import relativedelta


# This code is experimental and will potentially be changed or removed when a strategic backtesting solution is written
# PLEASE USE WITH EXTREME CAUTION
# Generic units calculator with get_units and reset function
class UnitsCalculator:

    def get_units(self, obs_date, data) -> np.ndarray:
        raise NotImplementedError

    def reset(self):
        return


# Example Units Calculator which generates random units
class RandomUnitsCalculator(UnitsCalculator):

    def get_units(self, obs_date, data) -> np.ndarray:
        prices = data['prices']
        return np.random.rand(prices.shape[-1])


# Example Units Calculator which generates units based on fixed weights
class FixedWeightUnitsCalculator(UnitsCalculator):

    def __init__(self, asset_table=None):
        if asset_table is None:
            assert 'Fixed Weight Units Calculator requires asset table'
        self.weights = list()
        for row in asset_table:
            self.weights.append(row['weight'])
        self.weights = np.array(self.weights)

    def get_units(self, obs_date, data) -> np.ndarray:
        # read in relevant data
        last_prices = data['last_prices']
        time_series = data['time_series']
        # check dimension of weights equals dimension of prices
        if last_prices.shape[-1] is not self.weights.size:
            assert 'Weight dimension does not equal number of assets in basket'
        # compute units on assets with non-zero last_price
        last_prices = last_prices.loc[obs_date].values
        units = np.full_like(last_prices, np.nan, dtype=np.double)
        mask = ~np.isnan(last_prices)
        units[mask] = self.weights[mask] / last_prices[mask] * time_series[obs_date]
        return units


# Example of optimization-based Trend strategy
class TrendOptimizationUnitsCalculator(UnitsCalculator):
    def __init__(self,
                 asset_table=None,
                 signal_lookback=relativedelta(years=2),
                 signal_return_lag=1,
                 signal_alphas=(0.0104, 0.0052, 0.0027),
                 covar_lookback=relativedelta(years=2),
                 covar_return_lag=5,
                 covar_alpha=0.0052,
                 covar_shrinkage=0.8,
                 vol_target=0.10,
                 weight_step_size=0.001):
        # read asset table and get min/max weight vectors
        if asset_table is None:
            assert 'Trend Units Calculator requires asset table'
        self.min_weight = list()
        self.max_weight = list()
        for row in asset_table:
            if 'min_weight' in row:
                self.min_weight.append(row['min_weight'])
            else:
                self.min_weight.append(-1000)
            if 'max_weight' in row:
                self.max_weight.append(row['max_weight'])
            else:
                self.max_weight.append(1000)
        self.min_weight = np.array(self.min_weight)
        self.max_weight = np.array(self.max_weight)
        # read other values
        self.signal_lookback = signal_lookback
        self.signal_return_lag = signal_return_lag
        self.signal_alphas = signal_alphas
        self.covar_lookback = covar_lookback
        self.covar_return_lag = covar_return_lag
        self.covar_alpha = covar_alpha
        self.covar_shrinkage = covar_shrinkage
        self.vol_target = vol_target
        self.weight_step_size = weight_step_size
        return

    def reset(self):
        self.interp_prices = None
        self.raw_weights = dict()
        return

    def get_units(self, obs_date, data) -> np.ndarray:
        # read in relevant data
        cal_dates = data['cal_dates']
        prices = data['last_prices']
        last_prices = data['last_prices']
        time_series = data['time_series']
        # compute interpolated prices if needed
        if self.interp_prices is None:
            self.interp_prices = prices.reindex(cal_dates).interpolate(method='time')
        # compute weights
        raw_weights = list()
        idx = cal_dates.get_loc(obs_date)
        for j in range(22):
            if j > idx:
                continue
            weight_date = cal_dates[idx - j]
            if weight_date not in self.raw_weights:
                self.raw_weights[weight_date] = self.compute_raw_weights(obs_date)
            raw_weights.append(self.raw_weights[weight_date])
        weights = np.sum(raw_weights, axis=0) / 22

        # get units
        last_prices = last_prices.loc[obs_date].values
        units = np.full_like(last_prices, np.nan, dtype=np.double)
        mask = ~np.isnan(last_prices)
        units[mask] = weights[mask] / last_prices[mask] * time_series[obs_date]
        return units

    def compute_raw_weights(self, obs_date):
        # compute signal & covar
        signal = self.compute_signal(obs_date)
        covar = self.compute_covariance(obs_date)
        weights = np.zeros(signal.size)

        # get valid underlier mask
        mask = ~np.any(np.isnan([signal, np.diag(covar)]), axis=0)
        signal = signal[mask]
        covar = covar[mask][:, mask]
        max_weight = self.max_weight[mask]
        min_weight = self.min_weight[mask]

        # solve optimization problem using duality
        # max_{lambda >= 0} min_w -w'*signal + lambda * ( w' * Covariance * w - vol_target^2 )
        #       s.t. bound constraints
        x0 = np.zeros(signal.size)

        def subproblem(lam):
            nonlocal x0
            sol = scipy.optimize.minimize(lambda x: -np.dot(x, signal) + lam * (np.dot(x, np.dot(covar, x)) -
                                                                                self.vol_target ** 2), x0,
                                          jac=lambda x: -signal + 2 * lam * np.dot(covar, x),
                                          bounds=np.transpose([min_weight, max_weight]), method='TNC')
            x0 = sol['x']
            return sol
        sol = scipy.optimize.minimize_scalar(lambda lam: -subproblem(lam)['fun'], bounds=(0, None), method='brent')
        sol = subproblem(sol['x'])
        # solve optimization problem cast as Second-Order Cone Problem (SOCP)
        # cvxopt.solvers.options['show_progress']= False
        # c = -cvxopt.matrix(signal)
        # Id = cvxopt.spdiag(list(np.ones(signal.size)))
        # G0 = cvxopt.sparse([-Id,Id])
        # h0 = cvxopt.matrix(np.hstack([-min_weight,max_weight]))
        # G = [cvxopt.matrix(np.vstack([np.zeros(signal.size),np.transpose(np.linalg.cholesky(covar))]))]
        # h = [cvxopt.matrix(np.concatenate([np.array([self.vol_target]),np.zeros(signal.size)]))]
        # sol = cvxopt.solvers.socp(c, G0, h0, Gq = G, hq = h)

        # update weights
        # weights[mask] = np.transpose(np.array(sol['x']))[0]
        weights[mask] = sol['x']
        # round weights
        if self.weight_step_size > 0:
            weights = np.round(weights / self.weight_step_size) * self.weight_step_size
        return weights

    # compute array of signals on a given date
    def compute_signal(self, obs_date):
        # get returns
        prices = self.interp_prices
        returns = prices[prices.index <= obs_date].pct_change(self.signal_return_lag)
        returns = returns[returns.index >= obs_date - self.signal_lookback].values
        # compute exponential average signals
        raw_signals = list()
        for alpha in self.signal_alphas:
            w = np.power(1. - alpha, -np.arange(returns.shape[0]))
            w /= np.sum(w)
            raw_signals.append(252 / self.signal_return_lag * np.dot(w, returns))
        return np.average(raw_signals, axis=0)

    # compute covariance matrix on a given date
    def compute_covariance(self, obs_date):
        # get returns
        prices = self.interp_prices
        returns = prices[prices.index <= obs_date].pct_change(self.covar_return_lag)
        returns = returns[returns.index >= obs_date - self.covar_lookback].values
        # compute exponential-weighted covar
        w = np.power(1. - self.covar_alpha, -np.arange(returns.shape[0]))
        w /= np.sum(w)
        averages = np.dot(w, returns)
        covar = np.dot(np.transpose(returns - averages), w[:, np.newaxis] * (returns - averages))
        covar *= 252 / self.covar_return_lag / (1 - np.sum(w * w))  # unbiased estimator!
        # shrinkage
        covar += self.covar_shrinkage * (np.diag(np.diag(covar)) - covar)
        return covar
