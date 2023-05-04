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

from functools import partial

from dateutil.relativedelta import relativedelta as rdelta
from pydash import chunk

from gs_quant.timeseries.econometrics import volatility, correlation
from gs_quant.timeseries.helper import _create_enum, _tenor_to_month, _month_to_tenor
from gs_quant.timeseries.measures_helper import VolReference, preprocess_implied_vol_strikes_eq
from gs_quant import timeseries as ts
from .statistics import *
from ..api.gs.assets import GsAssetApi
from ..api.gs.data import GsDataApi, MarketDataResponseFrame
from ..data.log import log_debug

_logger = logging.getLogger(__name__)

RebalFreq = _create_enum('RebalFreq', ['Daily', 'Weekly', 'Monthly'])
ReturnType = _create_enum('ReturnType', ['excess_return'])


def backtest_basket(
        series: list,
        weights: list,
        costs: list = None,
        rebal_freq: RebalFreq = RebalFreq.DAILY,
):
    num_assets = len(series)
    costs = costs or [0] * num_assets
    weights = weights or [1 / num_assets] * num_assets

    if not all(isinstance(x, pd.Series) for x in series):
        raise MqTypeError("expected a list of series")

    if len(weights) != num_assets or len(weights) != len(costs):
        raise MqValueError("series, weights, and cost lists must have the same length")

    # For all inputs which are Pandas series, get the intersection of their calendars
    cal = pd.DatetimeIndex(
        reduce(
            np.intersect1d,
            (
                curve.index
                for curve in series + weights + costs
                if isinstance(curve, pd.Series)
            ),
        )
    )

    # Reindex inputs and convert to pandas dataframes
    series = pd.concat([curve.reindex(cal) for curve in series], axis=1)
    weights = pd.concat([pd.Series(w, index=cal) for w in weights], axis=1)
    costs = pd.concat([pd.Series(c, index=cal) for c in costs], axis=1)

    if rebal_freq == RebalFreq.DAILY:
        rebal_dates = cal
    else:
        if rebal_freq == RebalFreq.WEEKLY:
            # Get hypothetical weekly rebalances
            num_rebals = ((cal[-1] - cal[0]).days) // 7
            rebal_dates = [cal[0] + i * rdelta(weeks=1) for i in range(num_rebals + 1)]
        else:
            # Get hypothetical monthly rebalances
            num_rebals = (cal[-1].year - cal[0].year) * 12 + cal[-1].month - cal[0].month
            rebal_dates = [cal[0] + i * rdelta(months=1) for i in range(num_rebals + 1)]

        # Convert the hypothetical weekly/monthly rebalance dates to actual calendar days
        rebal_dates = [min(cal[cal >= date]) for date in rebal_dates if date < max(cal)]

    # Create Units dataframe
    units = pd.DataFrame(index=cal, columns=series.columns)
    actual_weights = pd.DataFrame(index=cal, columns=series.columns)
    output = pd.Series(dtype='float64', index=cal)

    # Initialize backtest
    output.values[0] = 100
    units.values[0, ] = (
        output.values[0] * weights.values[0, ] / series.values[0, ]
    )
    actual_weights.values[0, ] = weights.values[0, ]

    # Run backtest
    prev_rebal = 0
    for i, date in enumerate(cal[1:], 1):
        # Update performance
        output.values[i] = output.values[i - 1] + np.dot(
            units.values[i - 1, ], series.values[i, ] - series.values[i - 1, ]
        )

        actual_weights.values[i, ] = (
            weights.values[prev_rebal, ] *
            (series.values[i, ] / series.values[prev_rebal, ]) *
            (output.values[prev_rebal] / output.values[i])
        )

        # Rebalance on rebal_dates
        if date in rebal_dates:
            # Compute costs
            output.values[i] -= (
                np.dot(costs.values[i, ], np.abs(weights.values[i, ] - actual_weights.values[i, ])) *
                output.values[i]
            )

            # Rebalance
            units.values[i, ] = (
                output.values[i] * weights.values[i, ] / series.values[i, ]
            )
            prev_rebal = i

            actual_weights.values[i, ] = weights.values[i, ]
        else:
            units.values[i, ] = units.values[
                i - 1,
            ]

    return output, actual_weights


@plot_function
def basket_series(
        series: list,
        weights: list = None,
        costs: list = None,
        rebal_freq: RebalFreq = RebalFreq.DAILY,
        return_type: ReturnType = ReturnType.EXCESS_RETURN,
) -> pd.Series:
    """
    Calculates a basket return series.

    :param series: list of time series of instrument prices
    :param weights: list of weights (defaults to evenly weight series)
    :param costs: list of execution costs in decimal (defaults to costs of 0)
    :param rebal_freq: rebalancing frequency - Daily, Weekly or Monthly (defaults to Daily)
    :param return_type: return type of underlying instruments - only excess return is supported
    :return: time series of the resulting basket

    **Usage**

    Calculates a basket return series.

    **Examples**

    Generate price series and combine them in a basket (weights 70%/30%) which rebalances monthly and assumes
    execution costs 5bps and 10bps each time the constituents are traded.

    >>> prices1 = generate_series(100)
    >>> prices2 = generate_series(100)
    >>> mybasket = basket_series([prices1, prices2], [0.7, 0.3], [0.0005, 0.001], monthly)

    **See also**

    :func:`prices`
    """

    return backtest_basket(series, weights, costs, rebal_freq)[0]


class Basket:
    """
    Construct a basket of stocks

    :param stocks: list of stock bloomberg ids
    :param weights: list of weights (defaults to evenly weight stocks)
    :param rebal_freq: rebalancing frequency - Daily or Monthly (defaults to daily)

    """

    def __init__(self, stocks: list, weights: list = None, rebal_freq: RebalFreq = RebalFreq.DAILY):
        if weights and len(weights) and len(stocks) != len(weights):  # make sure that they passed in an array for weig
            raise MqValueError("Stocks and weights must have the same length if both specified.")

        self.bbids = stocks
        self.rebal_freq = rebal_freq
        self.weights = weights
        self._marquee_ids = None

        self.start = DataContext.current.start_date
        self.end = DataContext.current.end_date

        self._spot_data = None
        self._returns = None
        self._actual_weights = None

    def _reset(self):
        self.start = DataContext.current.start_date
        self.end = DataContext.current.end_date
        self._spot_data = None
        self._returns = None
        self._actual_weights = None

    def get_marquee_ids(self):
        if self._marquee_ids is None:
            # Assets sorted by increasing rank
            assets = reversed(GsAssetApi.get_many_assets_data(bbid=self.bbids, fields=('id', 'bbid', 'rank'),
                                                              limit=2 * len(self.bbids), order_by=['>rank']))
            # If duplicate assets exist, asset_dict will contain a entry for the one with the higher rank (relevant)
            assets_dict = {entry['bbid']: entry['id'] for entry in assets}
            if len(assets_dict) != len(set(self.bbids)):
                not_found = set(assets_dict).symmetric_difference(self.bbids)
                raise MqValueError(f'Unable to find stocks: {", ".join(not_found)}')
            self._marquee_ids = [assets_dict[bbid] for bbid in self.bbids]

        return self._marquee_ids

    def _ensure_spot_data(self, request_id: Optional[str] = None):
        if self.start != DataContext.current.start_date or self.end != DataContext.current.end_date:
            self._reset()

        if self._spot_data is None:
            q = GsDataApi.build_market_data_query(self.get_marquee_ids(), QueryType.SPOT)
            log_debug(request_id, _logger, 'q %s', q)
            spot_data = ts.get_historical_and_last_for_measure(self.get_marquee_ids(), QueryType.SPOT, {},
                                                               request_id=request_id)

            dataset_ids = getattr(spot_data, 'dataset_ids', ())

            df = spot_data.set_index([spot_data.index, 'assetId'])
            df = df[~df.index.duplicated(keep='last')].spot.unstack()
            df = df[self._marquee_ids]
            self._spot_data = MarketDataResponseFrame(df)
            self._spot_data.dataset_ids = dataset_ids

    def _ensure_backtest(self, request_id: Optional[str] = None):
        if self.start != DataContext.current.start_date or self.end != DataContext.current.end_date:
            self._reset()

        if self._returns is None or self._actual_weights is None:
            spot_df = self.get_spot_data(request_id=request_id)
            spot_df.dropna(inplace=True)
            spot_series = [spot_df[asset_id] for asset_id in spot_df]
            results = backtest_basket(spot_series, self.weights, rebal_freq=self.rebal_freq)

            self._returns = results[0]
            actual_weights = results[1]
            actual_weights.columns = self.get_marquee_ids()
            self._actual_weights = actual_weights

    def get_returns(self, request_id: Optional[str] = None):
        self._ensure_backtest(request_id=request_id)
        return self._returns

    def get_actual_weights(self, request_id: Optional[str] = None):
        self._ensure_backtest(request_id=request_id)
        return self._actual_weights

    def get_spot_data(self, request_id: Optional[str] = None):
        self._ensure_spot_data(request_id=request_id)
        return self._spot_data

    @requires_session
    @plot_method
    def price(self, *, real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
        """
        Weighted average price

        :param real_time: whether to retrieve intraday data instead of EOD
        :param request_id: service request id, if any
        :return: time series of the average price
        """
        if real_time:
            raise NotImplementedError('real-time basket price not implemented')

        return self.get_returns(request_id=request_id)

    @requires_session
    @plot_method
    def average_implied_volatility(self, tenor: str, strike_reference: VolReference, relative_strike: Real, *,
                                   real_time: bool = False, request_id: Optional[str] = None,
                                   source: Optional[str] = None) -> pd.Series:
        """
        Weighted average implied volatility

        :param tenor: relative date representation of expiration date e.g. 1m
        :param strike_reference: reference for strike level
        :param relative_strike: strike relative to reference
        :param real_time: whether to retrieve intraday data instead of EOD
        :param request_id: service request id, if any
        :param source: name of function caller
        :return: time series of the average implied volatility
        """

        if real_time:
            raise NotImplementedError('real-time basket implied vol not implemented')

        ref_string, relative_strike = preprocess_implied_vol_strikes_eq(strike_reference, relative_strike)

        log_debug(request_id, _logger, 'where tenor=%s, strikeReference=%s, relativeStrike=%s', tenor, ref_string,
                  relative_strike)
        where = dict(tenor=tenor, strikeReference=ref_string, relativeStrike=relative_strike)
        tasks = []
        for i, chunked_assets in enumerate(chunk(self.get_marquee_ids(), 3)):
            query = GsDataApi.build_market_data_query(
                chunked_assets,
                QueryType.IMPLIED_VOLATILITY,
                where=where,
                source=source,
                real_time=real_time)

            tasks.append(partial(GsDataApi.get_market_data, query, request_id))

        results = ThreadPoolManager.run_async(tasks)
        vol_data = pd.concat(results)

        actual_weights = self.get_actual_weights(request_id)

        # Add in today's data
        today = datetime.date.today()
        if not real_time and DataContext.current.end_date >= today and \
                (vol_data.empty or today not in vol_data.index.date):
            vol_data = ts.append_last_for_measure(vol_data, self.get_marquee_ids(), QueryType.IMPLIED_VOLATILITY, where,
                                                  source=source, request_id=request_id)
            vol_data.index.rename('date', inplace=True)

        # Below transformations will throw errors if vol_data is empty
        if vol_data.empty:
            return pd.Series(dtype=float)

        vols = vol_data.pivot_table('impliedVolatility', ['date'], 'assetId')
        vols.reindex(self.get_marquee_ids(), axis=1)
        vols.index.name = None

        # Necessary when current values appended - set weights index to match vols index
        actual_weights = actual_weights.reindex(vols.index).fillna(method='pad')

        return actual_weights.mul(vols).sum(axis=1, skipna=False)

    @requires_session
    @plot_method
    def average_realized_volatility(self, tenor: str, returns_type: Returns = Returns.LOGARITHMIC, *,
                                    real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
        """
        Weighted average realized volatility

        :param tenor: relative date representation of expiration date e.g. 1m
        :param returns_type: returns type
        :param real_time: whether to retrieve intraday data instead of EOD
        :param request_id: service request id, if any
        :return: time series of the average realized volatility
        """

        if real_time:
            raise NotImplementedError('real-time basket realized vol not implemented')

        spot_df = self.get_spot_data(request_id=request_id)
        actual_weights = self.get_actual_weights(request_id=request_id)

        vols = [volatility(spot_df[asset_id], Window(tenor, tenor), returns_type) for asset_id in spot_df]
        vols = pd.concat(vols, axis=1)
        vols.columns = list(spot_df)
        # Necessary when current values appended - set weights index to match vols index
        actual_weights = actual_weights.reindex(vols.index).fillna(method='pad')

        return actual_weights.mul(vols, axis=1).sum(axis=1, skipna=False)

    @requires_session
    @plot_method
    def average_realized_correlation(self, w: Union[Window, int, str] = Window(None, 0),
                                     *, real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
        """
        Weighted average realized correlation. Computes the correlation between each of the basket's constituents and
        returns their average, weighted by their representation in the basket.

        :param w: Window, int, or str: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window
            size and 10 the ramp up value. If w is a string, it should be a relative date like '1m', '1d', etc.
            Window size defaults to length of series.
        :param real_time: whether to retrieve intraday data instead of EOD
        :param request_id: service request ID, if any
        :return: time series of the average realized correlation
        """
        # Calculated using method (a) from here: http://www.nematrian.com/MeasuringAverageStockCorrelation
        # Could be sped-up by using another estimate method, such as (b)
        if real_time:
            raise NotImplementedError('real-time basket realized corr not implemented')

        spot_df = self.get_spot_data(request_id=request_id)
        actual_weights = self.get_actual_weights(request_id=request_id)

        tot = pd.Series(np.zeros_like(spot_df.iloc[:, 0]), index=spot_df.index)
        tot_wt = pd.Series(np.zeros_like(spot_df.iloc[:, 0]), index=spot_df.index)
        # Iterate through and compute pairwise correlation between spot price series,
        # averaging at the end.
        for i in range(len(spot_df.columns)):
            for j in range(i + 1, len(spot_df.columns)):
                corr = correlation(spot_df.iloc[:, i], spot_df.iloc[:, j], w)
                wt = actual_weights.iloc[:, i] * actual_weights.iloc[:, j]
                tot += corr * wt
                tot_wt += wt
        return pd.to_numeric(tot / tot_wt, errors='coerce')

    @requires_session
    @plot_method
    def average_forward_vol(self, tenor: str, forward_start_date: str, strike_reference: VolReference,
                            relative_strike: Real, *, real_time: bool = False, request_id: Optional[str] = None,
                            source: Optional[str] = None) -> pd.Series:
        """
        Weighted average forward volatility.

        :param tenor: relative date representation of expiration date e.g. 1m
        :param forward_start_date: forward start date e.g. 2m, 1y
        :param strike_reference: reference for strike level
        :param relative_strike: strike relative to reference
        :param real_time: whether to retrieve intraday data instead of EOD
        :param request_id: service request id, if any
        :param source: name of function caller
        :return: average forward volatility
        """
        if real_time:
            raise NotImplementedError('real-time basket forward vol not implemented')

        ref_string, relative_strike = preprocess_implied_vol_strikes_eq(strike_reference, relative_strike)

        t1_month = _tenor_to_month(forward_start_date)
        t2_month = _tenor_to_month(tenor) + t1_month
        t1 = _month_to_tenor(t1_month)
        t2 = _month_to_tenor(t2_month)

        log_debug(request_id, _logger, 'where tenor=%s, strikeReference=%s, relativeStrike=%s', f'{t1},{t2}',
                  ref_string, relative_strike)
        where = dict(tenor=[t1, t2], strikeReference=[ref_string], relativeStrike=[relative_strike])
        asset_ids = self.get_marquee_ids()

        vol_data = ts.get_historical_and_last_for_measure(asset_ids, QueryType.IMPLIED_VOLATILITY, where, source=source,
                                                          request_id=request_id)

        # Below transformations will throw errors if vol_data is empty
        if vol_data.empty:
            return pd.Series(dtype=float)

        grouped_by_asset_ids = vol_data.groupby('assetId')
        s = {}
        for asset_id, df in grouped_by_asset_ids:
            grouped_by_tenor = df.groupby('tenor')
            try:
                sg = grouped_by_tenor.get_group(t1)['impliedVolatility']
                lg = grouped_by_tenor.get_group(t2)['impliedVolatility']
            except KeyError:
                log_debug(request_id, _logger, 'no data for one or more tenors')
                series = pd.Series(dtype=float, name='forwardVol')
            else:
                series = pd.Series(sqrt((t2_month * lg ** 2 - t1_month * sg ** 2) / _tenor_to_month(tenor)),
                                   name='forwardVol')
            s[asset_id] = series

        vols = pd.DataFrame(s)
        actual_weights = self.get_actual_weights(request_id)

        # Necessary when current values appended - set weights index to match vols index
        actual_weights = actual_weights.reindex(vols.index).fillna(method='pad')

        return actual_weights.mul(vols).sum(axis=1, skipna=False)
