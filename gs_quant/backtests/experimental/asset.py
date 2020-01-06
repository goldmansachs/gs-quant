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

import datetime as dt
import pandas as pd
import numpy as np
from gs_quant.data import Dataset


# Base Asset type
#   all assets are associated with the following class variables:
#       - asset_name, currency, excess_return
#   and the following class methods:
#       - compute_time_series
class Asset:
    def __init__(self, asset_name, currency, excess_return):
        self._asset_name = asset_name
        self._currency = currency
        self._excess_return = excess_return
        self._asset_id = None
        self._time_series = None
        self._source_asset = None

    # every instantiated Asset type must have a way to compute its time series
    @staticmethod
    def compute_time_series():
        assert NotImplementedError

    @property
    def asset_name(self):
        return self._asset_name

    @property
    def currency(self):
        return self._currency

    @property
    def excess_return(self):
        return self._excess_return

    @property
    def asset_id(self):
        return self._asset_id

    @property
    def source_asset(self):
        return self._source_asset

    # auxiliary functions defined for all Assets
    def get_time_series(self) -> pd.Series:
        raise RuntimeError("should be implemented by sub class")

    def convert_currency(self, target_currency='USD') -> object:
        if target_currency == self._currency:
            return self
        return FxHedgedAsset(self, target_currency)

    def convert_er(self, money_market_asset) -> object:
        if self._excess_return:
            return self
        return ExcessReturnAsset(self, money_market_asset)


# Underlier is a raw underlier from Marquee
class StsAsset(Asset):
    def __init__(self, asset_name, currency, excess_return, asset_id):
        super().__init__(asset_name, currency, excess_return)
        self._asset_id = asset_id

    def get_time_series(self):
        if not self._time_series:
            data = Dataset('STSLEVELS').get_data(assetId=self.asset_id, start=dt.date(1970, 1, 1))
            self._time_series = pd.Series()
            if data.size > 0:
                self._time_series = data['closePrice']
            self._time_series = self._time_series[~self._time_series.index.duplicated(keep='last')]
            self._time_series.name = self.asset_name
        return self._time_series


# Convert a given Asset to a different currency
class FxHedgedAsset(Asset):
    def __init__(self, asset: Asset, target_currency: str = 'USD'):
        super().__init__(asset.asset_name + 'x' + target_currency, target_currency, asset.excess_return)
        self._source_asset = asset
        if not self.excess_return:
            assert 'Not implied for Total Return assets yet!'

    # Converts to the target currency
    def get_time_series(self):
        if self._time_series:
            return self._time_series
        source_asset = self.source_asset
        source_asset_series = source_asset.get_time_series()
        source_currency = source_asset.currency
        target_currency = self.currency
        if source_currency == target_currency:
            self._time_series = source_asset_series
            return

        cross_series = self.get_fx_spot_series()
        index = source_asset_series.index.intersection(cross_series.index)
        if index.size == 0:
            self._time_series = pd.Series(name=self.asset_name)
            return

        base_value = source_asset_series[index[0]]
        source_returns = source_asset_series.reindex(index).pct_change(1)
        fx_returns = cross_series.reindex(index).pct_change(1)
        target_returns = source_returns * (1 + fx_returns)
        target_series = (1 + target_returns).cumprod() * base_value
        target_series[index[0]] = base_value
        self._time_series = target_series
        self._time_series.name = self.asset_name
        return self._time_series

    # Gets the FX Spot time series for a given cross
    def get_fx_spot_series(self) -> pd.Series:
        ds = Dataset('WMFXSPOT')
        coverage = ds.get_coverage()
        cross = self.currency + '/' + self.source_asset.currency
        asset_id = coverage[coverage['name'] == cross]['assetId'].values[0]
        time_series = ds.get_data(assetId=asset_id, start=dt.date(1970, 1, 1))['midPrice']
        time_series = time_series[~time_series.index.duplicated(keep='last')]
        time_series.name = cross
        return time_series


# Convert to excess return
class ExcessReturnAsset(Asset):
    def __init__(self, asset: Asset, money_market_asset: Asset):
        super().__init__(asset.asset_name + 'ER', asset.currency, True)
        # special data for Excess_return_Asset type
        self._source_asset = asset
        self._money_market_asset = money_market_asset

    def get_time_series(self):
        if self._time_series:
            return self._time_series
        source_asset = self.source_asset
        source_asset_series = source_asset.get_time_series()
        if source_asset.excess_return:
            self._time_series = source_asset_series
            return self._time_series

        money_market_series = self._money_market_asset.get_time_series()
        index = source_asset_series.index.intersection(money_market_series.index)
        if index.size == 0:
            self._time_series = pd.Series(name=self.asset_name)
            return self._time_series

        base_value = source_asset_series[index[0]]
        source_returns = source_asset_series.reindex(index).pct_change(1)
        mm_returns = money_market_series.reindex(index).pct_change(1)
        target_returns = source_returns - mm_returns
        target_series = (1 + target_returns).cumprod() * base_value
        target_series[index[0]] = base_value
        self._time_series = target_series
        self._time_series.name = self.asset_name
        return self._time_series


# this Asset is based on calculation of target units on a daily basis
class BasketAsset(Asset):
    def __init__(self,
                 asset_table: list = (),
                 units_calculator: object = None,
                 currency: str = 'USD',
                 excess_return: bool = True,
                 holidays: list = (),
                 start_date: dt.datetime = None):
        super().__init__(None, currency, excess_return)
        # special data for Basket_Asset
        self._asset_table = asset_table
        self._units_calculator = units_calculator
        self._holidays = holidays
        self._start_date = start_date
        if not self.excess_return:
            assert 'Total return basket is not yet implemented.'

    def get_time_series(self):
        if self._time_series:
            return self._time_series
        if self._units_calculator is None:
            assert 'Undefined units calculator.'

        # get holidays & dates
        holidays = pd.DatetimeIndex([])
        for holiday in self._holidays:
            holidays = holidays.union(Dataset(Dataset.GS.HOLIDAY).get_data(exchange=holiday, start=dt.date(1952, 1, 1),
                                                                           end=dt.date(2052, 12, 31)).index)
        cal_dates = pd.bdate_range(start=dt.date(1952, 1, 1), end=dt.date(2052, 12, 31)).difference(holidays)

        # get price data for underliers
        assets = []
        prices = []
        servicing_cost = []
        rebalance_cost = []
        for row in self._asset_table:
            # only accept built assets not strings
            asset = row['asset']
            assets.append(asset)
            if not self.excess_return:
                assert 'Total return basket is not yet implemented.'
            prices.append(asset.convert_er(row['money_market_asset']).convert_currency(self.currency).get_time_series())
            if 'servicing_cost' in row:
                servicing_cost.append(row['servicing_cost'])
            else:
                servicing_cost.append(0.)
            if 'rebalance_cost' in row:
                rebalance_cost.append(row['rebalance_cost'])
            else:
                rebalance_cost.append(0.)
        prices = pd.DataFrame(prices).transpose()
        last_prices = prices.reindex(cal_dates).fillna(method='ffill')
        servicing_cost = np.array(servicing_cost)
        rebalance_cost = np.array(rebalance_cost)

        # index dates
        dates = cal_dates[np.logical_and(cal_dates >= self._start_date, cal_dates <= prices.index[-1])]

        # initialize backtest
        cash = 100
        self._time_series = dict()
        units = np.zeros(len(assets))

        # setup data for units calculator
        self._units_calculator.reset()
        data = {'time_series': self._time_series,
                'cal_dates': cal_dates,
                'prices': prices,
                'last_prices': last_prices}
        # compute index
        self._time_series[dates[0]] = cash
        for idx in np.arange(1, len(dates)):
            date = dates[idx]
            prices_vec = prices.loc[date].values
            last_prices_vec = last_prices.loc[date].values
            # remove servicing costs
            year_frac = (dates[idx] - dates[idx - 1]) / np.timedelta64(1, 'D') / 360
            mask = ~np.isnan(last_prices_vec)
            cash -= np.sum(np.abs(units[mask]) * last_prices_vec[mask] * servicing_cost[mask]) * year_frac
            # run units calculator
            # use 1b lag, need to generalize
            if idx >= 1:
                obs_date = dates[idx - 1]
                target_units = self._units_calculator.get_units(obs_date, data)
            else:
                target_units = units
            # generate trades for assets with price available
            trades = np.zeros(len(assets))
            mask = ~np.any(np.isnan([prices_vec, target_units]), axis=0)
            trades[mask] = target_units[mask] - units[mask]
            # remove cash for trades, add units
            units[mask] += trades[mask]
            cash -= np.sum(trades[mask] * prices_vec[mask])
            cash -= np.sum(np.abs(trades[mask]) * prices_vec[mask] * rebalance_cost[mask])
            # calculate index level
            mask = ~np.isnan(last_prices_vec)
            self._time_series[date] = cash + np.sum(units[mask] * last_prices_vec[mask])

        self._time_series = pd.Series(self._time_series)
        self._time_series.name = self.asset_name
        return self._time_series
