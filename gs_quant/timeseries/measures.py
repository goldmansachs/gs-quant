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

import datetime
import logging
import re
import time
from enum import Enum
from numbers import Real
from typing import Optional, Union

import cachetools
import numpy as np
import pandas as pd
from pandas import Series
from pandas.tseries.holiday import Holiday, AbstractHolidayCalendar, USMemorialDay, USLaborDay, USThanksgivingDay, \
    nearest_workday

from gs_quant.api.gs.assets import GsAssetApi, GsIdType
from gs_quant.api.gs.data import GsDataApi
from gs_quant.data.core import DataContext
from gs_quant.datetime.gscalendar import GsCalendar
from gs_quant.datetime.point import relative_days_add
from gs_quant.errors import MqTypeError, MqValueError
from gs_quant.markets.securities import Asset, AssetIdentifier
from gs_quant.target.common import AssetClass, FieldFilterMap, AssetType, Currency
from gs_quant.timeseries.helper import log_return, plot_measure

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


class FloatingIndex(Enum):
    THREE_MONTH = '3m'
    SIX_MONTH = '6m'
    ONE_DAY = '1d'

class BenchmarkType(Enum):
    LIBOR = 'LIBOR'
    EURIBOR = 'EURIBOR'
    STIBOR = 'STIBOR'
    OIS = 'OIS'
    EONIA = 'EONIA'
    SARON = 'SARON'


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


@plot_measure((AssetClass.Equity,), (AssetType.Index, AssetType.ETF,))
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


@plot_measure((AssetClass.Equity,), (AssetType.Index, AssetType.ETF,))
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


@plot_measure((AssetClass.Equity,), (AssetType.Index, AssetType.ETF,))
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


@plot_measure((AssetClass.Cash,), (AssetType.Currency,))
def swap_rate(asset: Asset, tenor: str, benchmark_type: BenchmarkType = None, floating_index: str = None,
              *, source: str = None, real_time: bool = False) -> Series:
    """
    GS end-of-day Fixed-Floating interest rate swap (IRS) curves across major currencies.

    :param asset: asset object loaded from security master
    :param tenor: relative date representation of expiration date e.g. 1m
    :param benchmark_type: benchmark type e.g. LIBOR
    :param floating_index: floating index rate
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: average implied variance curve
    """

    currency = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)
    currency = Currency(currency)

    # default benchmark types
    if benchmark_type is None:
        if currency == Currency.EUR:
            benchmark_type = BenchmarkType.EURIBOR
        elif currency == Currency.SEK:
            benchmark_type = BenchmarkType.STIBOR
        else:
            benchmark_type = BenchmarkType.LIBOR

    over_nights = [BenchmarkType.OIS, BenchmarkType.EONIA, BenchmarkType.SARON]

    # default floating index
    if floating_index is None:
        if benchmark_type in over_nights:
            floating_index = '1d'
        else:
            if currency in [Currency.USD]:
                floating_index = '3m'
            elif currency in [Currency.GBP, Currency.EUR, Currency.CHF, Currency.SEK]:
                floating_index = '6m'

    mdapi_divider = " " if benchmark_type in over_nights else "-"
    mdapi_floating_index = BenchmarkType.OIS.value if benchmark_type is BenchmarkType.OIS else floating_index
    mdapi = currency.value + mdapi_divider + mdapi_floating_index

    rate_mqid = GsAssetApi.map_identifiers(GsIdType.mdapi, GsIdType.id, [mdapi])[mdapi]

    _logger.debug('where tenor=%s, floatingIndex=%s', tenor, floating_index)

    q = GsDataApi.build_market_data_query(
        [rate_mqid],
        'Swap Rate',
        where=FieldFilterMap(tenor=tenor),
        source=source,
        real_time=real_time
    )

    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return Series() if df.empty else df['swapRate']


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
        end = today - datetime.timedelta(days=relative_days_add(pricing_date, True))
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
    :param price_method: price method between LMP and MCP: Default value = LMP
    :param price_component: price type among totalPrice, energy, loss and congestion: Default value = totalPrice
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

    start, end = DataContext.current.start_date, DataContext.current.end_date
    where = FieldFilterMap(priceMethod=price_method, priceComponent=price_component)
    with DataContext(start, end + datetime.timedelta(days=2)):
        q = GsDataApi.build_market_data_query([asset.get_marquee_id()], 'Price', where=where, source=source,
                                              real_time=True)
        df = _market_data_timed(q)
        _logger.debug('q %s', q)

    # convert timezone back to EST if needed
    # TODO: get timezone info from Asset
    df = df.tz_convert('US/Eastern')
    df['date'] = df.index.date
    df['day'] = df.index.dayofweek
    df['hour'] = df.index.hour
    df = df.loc[(df['date'] >= start) & (df['date'] <= end)]
    holidays = NercCalendar().holidays(start=datetime.date(start.year, start.month, start.day),
                                       end=datetime.date(end.year, end.month, end.day)).date
    # checking missing hours
    ref_hour_range = pd.date_range(start, end, freq='1h', tz='US/Eastern')
    missing_hours = ref_hour_range[~ref_hour_range.isin(df.index)]
    if not missing_hours.empty:
        raise ValueError('Missing Data Points for: ' + str(missing_hours.get_values()))

    # TODO: get frequency definition from SecDB
    if bucket == 'base':
        pass
    # off peak: 11pm-7am & weekend & holiday
    elif bucket == 'offpeak':
        df = df.loc[df['date'].isin(holidays) |
                    df['day'].isin([5, 6]) |
                    (~df['date'].isin(holidays) & ~df['day'].isin([5, 6]) & ((df['hour'] < 7) | (df['hour'] > 22)))]
    # peak: 7am to 11pm on weekdays
    elif bucket == 'peak':
        df = df.loc[(~df['date'].isin(holidays)) & (~df['day'].isin([5, 6])) & (df['hour'] > 6) & (df['hour'] < 23)]
    # 7x8: 11pm to 7am
    elif bucket == '7x8':
        df = df.loc[(df['hour'] < 7) | (df['hour'] > 22)]
    else:
        raise ValueError('Invalid bucket: ' + bucket + '. Expected Value: peak, offpeak, base, 7x8.')

    df = df['price'].resample(resample).mean()
    df.index = df.index.date
    return df
