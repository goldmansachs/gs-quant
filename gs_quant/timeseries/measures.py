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
import numpy as np
import re
import time
from enum import Enum
from gs_quant.api.gs.data import GsDataApi
from gs_quant.data.core import DataContext
from gs_quant.datetime.point import relative_days_add
from gs_quant.datetime.gscalendar import GsCalendar
from gs_quant.markets.securities import Asset
from gs_quant.target.common import AssetClass, FieldFilterMap
from gs_quant.timeseries.helper import log_return, plot_measure
from gs_quant.errors import MqTypeError, MqValueError
from pandas.tseries.holiday import Holiday, AbstractHolidayCalendar, USMemorialDay, USLaborDay, USThanksgivingDay, nearest_workday
from pytz import timezone
from numbers import Real
from pandas import Series
from typing import Optional, Union

GENERIC_DATE = Union[datetime.date, str]
TD_ONE = datetime.timedelta(days=1)
_logger = logging.getLogger(__name__)


# TODO: get NERC Calendar from SecDB
class NercCalendar(AbstractHolidayCalendar):
    rules = [
            Holiday('New Years Day', month=1, day=1, observance=nearest_workday),
            USMemorialDay,
            Holiday('July 4th', month=7, day=4, observance=nearest_workday),
            USLaborDay,
            USThanksgivingDay,
            Holiday('Christmas', month=12, day=25, observance=nearest_workday)
    ]


def _to_fx_strikes(strikes):
    out = []
    for strike in strikes:
        if strike == 50:
            out.append('ATMS')
        elif strike < 50:
            out.append(f'{round(strike)}DC')
        else:
            out.append(f'{round(abs(100 - strike))}DP')
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


class EdrDataReference(Enum):
    DELTA_CALL = 'delta_call'
    DELTA_PUT = 'delta_put'
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

    if df.empty:
        return pd.Series()

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


@plot_measure((AssetClass.Equity,), None)
def implied_correlation(asset: Asset, tenor: str, strike_reference: EdrDataReference, relative_strike: Real, *,
                        source: str = None, real_time: bool = False) -> Series:
    """
    Correlation of an asset implied by observations of market prices.

    :param asset: asset object loaded from security master
    :param tenor: relative date representation of expiration date e.g. 1m
    :param strike_reference: reference for strike level
    :param relative_strike: strike relative to reference
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: implied correlation curve
    """
    if strike_reference == EdrDataReference.DELTA_PUT:
        relative_strike = abs(100 - relative_strike)

    relative_strike = relative_strike / 100

    delta_types = (EdrDataReference.DELTA_CALL, EdrDataReference.DELTA_PUT)
    strike_ref = "delta" if strike_reference in delta_types else strike_reference.value

    _logger.debug('where tenor=%s, strikeReference=%s, relativeStrike=%s', tenor, strike_ref, relative_strike)

    mqid = asset.get_marquee_id()
    where = FieldFilterMap(tenor=tenor, strikeReference=strike_ref, relativeStrike=relative_strike)
    q = GsDataApi.build_market_data_query([mqid], 'Implied Correlation', where=where, source=source, real_time=real_time)

    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return Series() if df.empty else df['impliedCorrelation']


@plot_measure((AssetClass.Equity,), None)
def average_implied_volatility(asset: Asset, tenor: str, strike_reference: EdrDataReference, relative_strike: Real, *,
                        source: str = None, real_time: bool = False) -> Series:
    """
    Historic weighted average implied volatility for the underlying assets of an equity index.

    :param asset: asset object loaded from security master
    :param tenor: relative date representation of expiration date e.g. 1m
    :param strike_reference: reference for strike level
    :param relative_strike: strike relative to reference
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: average implied volatility curve
    """
    if strike_reference == EdrDataReference.DELTA_PUT:
        relative_strike = abs(100 - relative_strike)

    relative_strike = relative_strike / 100

    delta_types = (EdrDataReference.DELTA_CALL, EdrDataReference.DELTA_PUT)
    strike_ref = "delta" if strike_reference in delta_types else strike_reference.value

    _logger.debug('where tenor=%s, strikeReference=%s, relativeStrike=%s', tenor, strike_ref, relative_strike)

    mqid = asset.get_marquee_id()
    where = FieldFilterMap(tenor=tenor, strikeReference=strike_ref, relativeStrike=relative_strike)
    q = GsDataApi.build_market_data_query([mqid], 'Average Implied Volatility', where=where, source=source, real_time=real_time)

    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return Series() if df.empty else df['averageImpliedVolatility']


@plot_measure((AssetClass.Equity,), None)
def average_implied_variance(asset: Asset, tenor: str, strike_reference: EdrDataReference, relative_strike: Real, *,
                        source: str = None, real_time: bool = False) -> Series:
    """
    Historic weighted average implied variance for the underlying assets of an equity index.

    :param asset: asset object loaded from security master
    :param tenor: relative date representation of expiration date e.g. 1m
    :param strike_reference: reference for strike level
    :param relative_strike: strike relative to reference
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: average implied variance curve
    """
    if strike_reference == EdrDataReference.DELTA_PUT:
        relative_strike = abs(100 - relative_strike)

    relative_strike = relative_strike / 100

    delta_types = (EdrDataReference.DELTA_CALL, EdrDataReference.DELTA_PUT)
    strike_ref = "delta" if strike_reference in delta_types else strike_reference.value

    _logger.debug('where tenor=%s, strikeReference=%s, relativeStrike=%s', tenor, strike_ref, relative_strike)

    mqid = asset.get_marquee_id()
    where = FieldFilterMap(tenor=tenor, strikeReference=strike_ref, relativeStrike=relative_strike)
    q = GsDataApi.build_market_data_query([mqid], 'Average Implied Variance', where=where, source=source, real_time=real_time)

    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return Series() if df.empty else df['averageImpliedVariance']


@cachetools.cached(cachetools.TTLCache(16, 3600))
def _get_custom_bd(exchange):
    # TODO: support custom weekmasks
    from pandas.tseries.offsets import CustomBusinessDay
    calendar = GsCalendar.get(exchange).business_day_calendar()
    return CustomBusinessDay(calendar=calendar)


@log_return(_logger, 'trying pricing dates')
def _range_from_pricing_date(exchange, pricing_date: Optional[GENERIC_DATE] = None):
    today = pd.Timestamp.today().normalize()
    if pricing_date is None:
        return today - _get_custom_bd(exchange), today
    if isinstance(pricing_date, datetime.date):
        return pricing_date, pricing_date

    assert isinstance(pricing_date, str)
    matcher = re.fullmatch('(\\d+)b', pricing_date)
    if matcher:
        start = end = today - _get_custom_bd(exchange) * int(matcher.group(1))
    else:
        end = today - datetime.timedelta(days=relative_days_add(pricing_date))
        start = end - _get_custom_bd(exchange)
    return start, end


def _to_offset(tenor: str) -> pd.DateOffset:
    import re
    matcher = re.fullmatch('(\\d+)([dwmy])', tenor)
    if not matcher:
        raise ValueError('invalid tenor ' + tenor)

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


@plot_measure((AssetClass.Equity, AssetClass.Commod), None)
def vol_term(asset: Asset, strike_reference: SkewReference, relative_strike: Real,
             pricing_date: Optional[GENERIC_DATE] = None, *, source: str = None, real_time: bool = False) -> pd.Series:
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

    latest = df.index.max()
    _logger.info('selected pricing date %s', latest)
    df = df.loc[latest]
    cbd = _get_custom_bd(asset.exchange)
    df = df.assign(expirationDate=df.index + df['tenor'].map(_to_offset) + cbd - cbd)
    df = df.set_index('expirationDate')
    df.sort_index(inplace=True)
    df = df.loc[DataContext.current.start_date: DataContext.current.end_date]
    return df['impliedVolatility'] if not df.empty else pd.Series()


@plot_measure((AssetClass.Equity, AssetClass.Commod), None)
def fwd_term(asset: Asset, pricing_date: Optional[GENERIC_DATE] = None, *, source: str = None,
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

    latest = df.index.max()
    _logger.info('selected pricing date %s', latest)
    df = df.loc[latest]
    cbd = _get_custom_bd(asset.exchange)
    df.loc[:, 'expirationDate'] = df.index + df['tenor'].map(_to_offset) + cbd - cbd
    df = df.set_index('expirationDate')
    df.sort_index(inplace=True)
    df = df.loc[DataContext.current.start_date: DataContext.current.end_date]
    return df['forward'] if not df.empty else pd.Series()


@plot_measure((AssetClass.Commod,), None)
def bucketize(asset: Asset, price_method: str = "LMP", price_component: str = "totalPrice", bucket: str = 'base',
              granularity: str = 'daily', *, source: str = None, real_time: bool = True) -> pd.Series:
    """'
    Bucketized Elec Historical Clears

    :param asset: asset object loaded from security master
    :param price_method: price method between LMP and MCP: Default value = Price
    :param price_component: price type among totalPrice, energy, loss and congestion: Default value = Price
    :param bucket: bucket type among 'base, 'peak', 'offpeak' and '7x8': Default value = base
    :param granularity: daily or monthly: default value = daily
    :param source: name of function caller: default source = None
    :param real_time: whether to retrieve intraday data instead of EOD: default value = True
    :return: Bucketized Elec Historical Clears
    """

    # create granularity indicator for resample usage
    if granularity.lower() in ['daily', 'd']:
        resample = 'D'
    elif granularity.lower() in ['monthly', 'm']:
        resample = 'M'
    else:
        raise ValueError('Invalid granularity: ' + granularity + '. Expected Value: daily or monthly.')

    start, end = DataContext.current.start_time, DataContext.current.end_time + datetime.timedelta(hours=23)
    where = FieldFilterMap(priceMethod=price_method, priceComponent=price_component)
    with DataContext(start, end):
        q = GsDataApi.build_market_data_query([asset.get_marquee_id()], 'Price', where=where, source=source,
                                              real_time=True)
        df = _market_data_timed(q)
        _logger.debug('q %s', q)

    # convert timezone back to EST if needed
    # TODO: get timezone info from Asset
    df = df.tz_convert('US/Eastern')
    dayofweek = df.index.dayofweek
    hour = df.index.hour
    date = df.index.date
    holidays = NercCalendar().holidays(start=start, end=end).date

    # TODO: get frequency definition from SecDB
    if bucket == 'base':
        pass
    # off peak: 11pm-7am & weekend & holiday
    elif bucket == 'offpeak':
        df = df.loc[np.in1d(date, holidays) | (~np.in1d(date, holidays)
                    & (((dayofweek != 5) & (dayofweek != 6) & ((hour < 7) | (hour > 22)))
                    | (dayofweek == 5) | (dayofweek == 6)))]
    # peak: 7am to 11pm on weekdays
    elif bucket == 'peak':
        df = df.loc[(~np.in1d(date, holidays) & (dayofweek != 5) & (dayofweek != 6) & ((hour > 6) & (hour < 23)))]
    # 7x8: 11pm to 7am
    elif bucket == '7x8':
        df = df.loc[(hour < 7) | (hour > 22)]
    else:
        raise ValueError('Invalid bucket: ' + bucket + '. Expected Value: peak, offpeak, base, 7x8.')

    df = df['price'].resample(resample).mean()
    df.index = df.index.date
    return df
