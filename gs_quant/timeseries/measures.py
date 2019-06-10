# Copyright 2019 Goldman Sachs.
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
# Plot Service will make use of appropriately decorated functions in this module.

import cachetools
import datetime
import logging
import pandas as pd
import time
from enum import Enum
from gs_quant.api.gs.data import GsDataApi
from gs_quant.data.core import DataContext
from gs_quant.data.dataset import Dataset
from gs_quant.datetime.gscalendar import GsCalendar
from gs_quant.markets.securities import Asset
from gs_quant.target.common import AssetClass, AssetType, FieldFilterMap
from gs_quant.timeseries.helper import plot_measure
from gs_quant.errors import MqTypeError, MqValueError
from numbers import Real
from pandas import Series
from typing import Optional

TD_ONE = datetime.timedelta(days=1)
_logger = logging.getLogger(__name__)


def _to_fx_strikes(strikes):
    out = []
    for strike in strikes:
        if strike == 50:
            out.append('ATMS')
        elif strike < 50:
            out.append(f'{strike}DC')
        else:
            out.append(f'{abs(100 - strike)}DP')
    return out


class SkewReference(Enum):
    DELTA = 'delta'
    NORMALIZED = 'normalized'
    SPOT = 'spot'
    FORWARD = 'forward'


class VolReference(Enum):
    DELTA_CALL = 'delta_call'
    DELTA_PUT = 'delta_put'
    NORMALIZED = 'normalized'
    SPOT = 'spot'
    FORWARD = 'forward'


def _market_data_timed(q):
    start = time.perf_counter()
    df = GsDataApi.get_market_data(q)
    _logger.debug('market data query ran in %.3f ms', (time.perf_counter() - start) * 1000)
    return df


@plot_measure((AssetClass.FX, AssetClass.Equity), None)
def skew(asset: Asset, tenor: str, strike_reference: SkewReference, distance: Real, *, location: str = 'NYC',
         source: str = None, real_time: bool = False) -> Series:
    """
    Difference in implied volatility of equidistant out-of-the-money put and call options.

    :param asset: asset object loaded from security master
    :param tenor: relative date representation of expiration date e.g. 1m
    :param strike_reference: reference for strike level (for equities)
    :param distance: distance from at-the-money option
    :param location: location at which a price fixing has been taken (for FX assets)
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: skew curve
    """
    if real_time:
        raise MqValueError('real-time skew not supported')

    if strike_reference in (SkewReference.DELTA, None):
        b = 50
    elif strike_reference == SkewReference.NORMALIZED:
        b = 0
    else:
        b = 100

    kwargs = {}
    if strike_reference in (SkewReference.DELTA, None):
        # using delta call strikes so X DP is represented as (100 - X) DC
        q_strikes = [100 - distance, distance, b]
    else:
        q_strikes = [b - distance, b + distance, b]

    if asset.asset_class == AssetClass.FX:
        q_strikes = _to_fx_strikes(q_strikes)
        kwargs['location'] = location
        column = 'deltaStrike'  # should use SkewReference.DELTA for FX
    else:
        assert asset.asset_class == AssetClass.Equity
        if not strike_reference:
            raise MqTypeError('strike reference required for equities')
        if strike_reference != SkewReference.NORMALIZED:
            q_strikes = [x / 100 for x in q_strikes]
        kwargs['strikeReference'] = strike_reference.value
        column = 'relativeStrike'

    kwargs[column] = q_strikes
    _logger.debug('where tenor=%s and %s', tenor, kwargs)
    where = FieldFilterMap(tenor=tenor, **kwargs)
    q = GsDataApi.build_market_data_query([asset.get_marquee_id()], 'Implied Volatility', where=where, source=source)
    _logger.debug('q %s', q)
    df = _market_data_timed(q)

    curves = {k: v for k, v in df.groupby(column)}
    if len(curves) < 3:
        raise MqValueError('skew not available for given inputs')
    series = [curves[qs]['impliedVolatility'] for qs in q_strikes]
    return (series[0] - series[1]) / series[2]


@plot_measure((AssetClass.Equity, AssetClass.Commod), None)
def implied_volatility(asset: Asset, tenor: str, strike_reference: VolReference, relative_strike: Real, *,
                       source: str = None, real_time: bool = False) -> Series:
    """
    Volatility of an asset implied by observations of market prices.

    :param asset: asset object loaded from security master
    :param tenor: relative date representation of expiration date e.g. 1m
    :param strike_reference: reference for strike level
    :param relative_strike: strike relative to reference
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: implied volatility curve
    """
    if strike_reference == VolReference.DELTA_PUT:
        relative_strike = abs(100 - relative_strike)

    relative_strike = relative_strike if strike_reference == VolReference.NORMALIZED else relative_strike / 100
    ref_string = "delta" if strike_reference in (VolReference.DELTA_CALL,
                                                 VolReference.DELTA_PUT) else strike_reference.value
    _logger.debug('where tenor=%s, strikeReference=%s, relativeStrike=%s', tenor, ref_string, relative_strike)
    where = FieldFilterMap(tenor=tenor, strikeReference=ref_string, relativeStrike=relative_strike)
    q = GsDataApi.build_market_data_query([asset.get_marquee_id()], 'Implied Volatility', where=where, source=source,
                                          real_time=real_time)
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return Series() if df.empty else df['impliedVolatility']


@cachetools.cached(cachetools.TTLCache(16, 3600))
def _get_custom_bd(exchange):
    # TODO: support custom weekmasks
    from pandas.tseries.offsets import CustomBusinessDay
    calendar = GsCalendar.get(exchange).business_day_calendar()
    return CustomBusinessDay(calendar=calendar)


def _range_from_pricing_date(exchange, pricing_date: Optional[datetime.date] = None):
    if pricing_date:
        end = pricing_date
        start = pricing_date
    else:
        end = datetime.date.today()
        start = end - _get_custom_bd(exchange)
        _logger.debug('trying pricing dates %s to %s', start, end)
    return start, end


def _to_offset(tenor: str) -> pd.DateOffset:
    import re
    matcher = re.fullmatch('(\\d+)([dwmy])', tenor)
    if not matcher:
        raise ValueError('invalid tenor ' + tenor)

    # TODO: determine desired handling of months
    ab = matcher.group(2)
    if ab == 'd':
        name = 'days'
    elif ab == 'w':
        name = 'weeks'
    elif ab == 'm':
        name = 'months'
    else:
        assert ab == 'y'
        name = 'years'

    kwarg = {name: int(matcher.group(1))}
    return pd.DateOffset(**kwarg)


@plot_measure((AssetClass.Equity,), None)
def vol_term(asset: Asset, strike_reference: SkewReference, relative_strike: Real,
             pricing_date: Optional[datetime.date] = None, *, source: str = None, real_time: bool = False) -> pd.Series:
    """
    Volatility term structure.

    :param asset: asset object loaded from security master
    :param strike_reference: reference for strike level
    :param relative_strike: strike relative to reference
    :param pricing_date: pricing date (defaults to latest available)
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: volatility term structure
    """
    if real_time:
        raise NotImplementedError('realtime forward term not implemented')  # TODO

    if strike_reference != SkewReference.NORMALIZED:
        relative_strike /= 100

    start, end = _range_from_pricing_date(asset.exchange, pricing_date)
    with DataContext(start, end):
        _logger.debug('where strikeReference=%s, relativeStrike=%s', strike_reference.value, relative_strike)
        where = FieldFilterMap(strikeReference=strike_reference.value, relativeStrike=relative_strike)
        q = GsDataApi.build_market_data_query([asset.get_marquee_id()], 'Implied Volatility', where=where,
                                              source=source,
                                              real_time=real_time)
        _logger.debug('q %s', q)
        df = _market_data_timed(q)

    if df.empty:
        return pd.Series()

    earliest = df.index.min()
    _logger.info('selected pricing date %s', earliest)
    df = df.loc[earliest]
    cbd = _get_custom_bd(asset.exchange)
    df = df.assign(expirationDate=df.index + df['tenor'].map(_to_offset) + cbd - cbd)
    df = df.set_index('expirationDate')
    df.sort_index(inplace=True)
    df = df.loc[DataContext.current.start_date: DataContext.current.end_date]
    return df['impliedVolatility'] if not df.empty else pd.Series()


@plot_measure((AssetClass.Equity,), None)
def fwd_term(asset: Asset, pricing_date: Optional[datetime.date] = None, *, source: str = None,
             real_time: bool = False) -> pd.Series:
    """
    Forward term structure.

    :param asset: asset object loaded from security master
    :param pricing_date: pricing date (defaults to latest available)
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: forward term structure
    """
    if real_time:
        raise NotImplementedError('realtime forward term not implemented')  # TODO

    start, end = _range_from_pricing_date(asset.exchange, pricing_date)
    with DataContext(start, end):
        where = FieldFilterMap(strikeReference='forward', relativeStrike=1)
        q = GsDataApi.build_market_data_query([asset.get_marquee_id()], 'Forward', where=where, source=source,
                                              real_time=real_time)
        _logger.debug('q %s', q)
        df = _market_data_timed(q)

    if df.empty:
        return pd.Series()

    earliest = df.index.min()
    _logger.info('selected pricing date %s', earliest)
    df = df.loc[earliest]
    cbd = _get_custom_bd(asset.exchange)
    df.loc[:, 'expirationDate'] = df.index + df['tenor'].map(_to_offset) + cbd - cbd
    df = df.set_index('expirationDate')
    df.sort_index(inplace=True)
    df = df.loc[DataContext.current.start_date: DataContext.current.end_date]
    return df['forward'] if not df.empty else pd.Series()
