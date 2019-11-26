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
from collections import namedtuple
from enum import auto
from numbers import Real

import cachetools.func
import numpy as np
import pandas as pd
from dateutil import tz
from pandas import Series
from pandas.tseries.holiday import Holiday, AbstractHolidayCalendar, USMemorialDay, USLaborDay, USThanksgivingDay, \
    nearest_workday

from gs_quant.api.gs.assets import GsIdType
from gs_quant.api.gs.data import GsDataApi
from gs_quant.api.gs.data import QueryType
from gs_quant.data.core import DataContext
from gs_quant.data.fields import Fields
from gs_quant.datetime.gscalendar import GsCalendar
from gs_quant.datetime.point import relative_days_add
from gs_quant.errors import MqTypeError, MqValueError
from gs_quant.markets.securities import *
from gs_quant.markets.securities import Asset, AssetIdentifier, SecurityMaster
from gs_quant.target.common import AssetClass, FieldFilterMap, AssetType, Currency, PricingLocation
from gs_quant.timeseries.helper import log_return, plot_measure

GENERIC_DATE = Union[datetime.date, str]
TD_ONE = datetime.timedelta(days=1)
_logger = logging.getLogger(__name__)

MeasureDependency: namedtuple = namedtuple("MeasureDependency", ["id_provider", "query_type"])


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


class CdsVolReference(Enum):
    DELTA_CALL = 'delta_call'
    DELTA_PUT = 'delta_put'
    FORWARD = 'forward'


class VolReference(Enum):
    DELTA_CALL = 'delta_call'
    DELTA_PUT = 'delta_put'
    DELTA_NEUTRAL = 'delta_neutral'
    NORMALIZED = 'normalized'
    SPOT = 'spot'
    FORWARD = 'forward'


class VolSmileReference(Enum):
    SPOT = 'spot'
    FORWARD = 'forward'


class EdrDataReference(Enum):
    DELTA_CALL = 'delta_call'
    DELTA_PUT = 'delta_put'
    SPOT = 'spot'


class ForeCastHorizon(Enum):
    THREE_MONTH = '3m'
    SIX_MONTH = '6m'
    ONE_YEAR = '1y'
    EOY1 = 'EOY1'
    EOY2 = 'EOY2'
    EOY3 = 'EOY3'
    EOY4 = 'EOY4'


class BenchmarkType(Enum):
    LIBOR = 'LIBOR'
    EURIBOR = 'EURIBOR'
    STIBOR = 'STIBOR'
    OIS = 'OIS'
    CDKSDA = 'CDKSDA'


class FundamentalMetricPeriod(Enum):
    ONE_YEAR = '1y'
    TWO_YEAR = '2y'
    THREE_YEAR = '3y'


class FundamentalMetricPeriodDirection(Enum):
    FORWARD = 'forward'
    TRAILING = 'trailing'


class RatesConversionType(Enum):
    DEFAULT_BENCHMARK_RATE = auto()
    INFLATION_BENCHMARK_RATE = auto()
    CROSS_CURRENCY_BASIS = auto()


CURRENCY_TO_DEFAULT_RATE_BENCHMARK = {
    'USD': 'USD-LIBOR-BBA',
    'EUR': 'EUR-EURIBOR-Telerate',
    'GBP': 'GBP-LIBOR-BBA',
    'JPY': 'JPY-LIBOR-BBA'
}

CURRENCY_TO_INFLATION_RATE_BENCHMARK = {
    'GBP': 'CPI-UKRPI',
    'EUR': 'CPI-CPXTEMU'
}

CROSS_TO_CROSS_CURRENCY_BASIS = {
    'JPYUSD': 'USD-3m/JPY-3m',
    'USDJPY': 'USD-3m/JPY-3m',
    'USDEUR': 'EUR-3m/USD-3m',
    'EURUSD': 'EUR-3m/USD-3m',
    'USDGBP': 'GBP-3m/USD-3m',
    'GBPUSD': 'GBP-3m/USD-3m'
}


def cross_stored_direction_for_fx_vol(asset_id: str) -> str:
    result_id = asset_id
    try:
        asset = SecurityMaster.get_asset(asset_id, AssetIdentifier.MARQUEE_ID)

        if asset.asset_class is AssetClass.FX:
            bbid = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)
            if bbid is not None:
                legit_usd_cross = str.startswith(bbid, "USD") and not str.endswith(bbid, ("EUR", "GBP", "NZD", "AUD"))
                legit_eur_cross = str.startswith(bbid, "EUR")
                legit_jpy_cross = str.endswith(bbid, "JPY") and not str.startswith(bbid, ("KRW", "IDR", "CLP", "COP"))
                odd_cross = bbid in ("EURUSD", "GBPUSD", "NZDUSD", "AUDUSD", "JPYKRW", "JPYIDR", "JPYCLP", "JPYCOP")
                if not legit_usd_cross and not legit_eur_cross and not legit_jpy_cross and not odd_cross:
                    cross = bbid[3:] + bbid[:3]
                    cross_asset = SecurityMaster.get_asset(cross, AssetIdentifier.BLOOMBERG_ID)
                    result_id = cross_asset.get_marquee_id()
    except TypeError:
        result_id = asset_id
    return result_id


def cross_to_usd_based_cross(asset_id: str) -> str:
    result_id = asset_id
    try:
        asset = SecurityMaster.get_asset(asset_id, AssetIdentifier.MARQUEE_ID)
        if asset.asset_class is AssetClass.FX:
            bbid = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)
            if bbid is not None and not str.startswith(bbid, "USD"):
                cross = bbid[3:] + bbid[:3]
                cross_asset = SecurityMaster.get_asset(cross, AssetIdentifier.BLOOMBERG_ID)
                result_id = cross_asset.get_marquee_id()
    except TypeError:
        result_id = asset_id
    return result_id


def currency_to_default_benchmark_rate(asset_id: str) -> str:
    try:
        asset = SecurityMaster.get_asset(asset_id, AssetIdentifier.MARQUEE_ID)
        result = convert_asset_for_rates_data_set(asset, RatesConversionType.DEFAULT_BENCHMARK_RATE)
    except TypeError:
        result = asset_id
    return result


def currency_to_inflation_benchmark_rate(asset_id: str) -> str:
    try:
        asset = SecurityMaster.get_asset(asset_id, AssetIdentifier.MARQUEE_ID)
        result = convert_asset_for_rates_data_set(asset, RatesConversionType.INFLATION_BENCHMARK_RATE)
    except TypeError:
        result = asset_id
    return result


def cross_to_basis(asset_id: str) -> str:
    try:
        asset = SecurityMaster.get_asset(asset_id, AssetIdentifier.MARQUEE_ID)
        result = convert_asset_for_rates_data_set(asset, RatesConversionType.CROSS_CURRENCY_BASIS)
    except TypeError:
        result = asset_id
    return result


def convert_asset_for_rates_data_set(from_asset: Asset, c_type: RatesConversionType) -> str:
    try:
        bbid = from_asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)
        if bbid is None:
            return from_asset.get_marquee_id()

        if c_type is RatesConversionType.DEFAULT_BENCHMARK_RATE:
            to_asset = CURRENCY_TO_DEFAULT_RATE_BENCHMARK[bbid]
        elif c_type is RatesConversionType.INFLATION_BENCHMARK_RATE:
            to_asset = CURRENCY_TO_INFLATION_RATE_BENCHMARK[bbid]
        else:
            to_asset = CROSS_TO_CROSS_CURRENCY_BASIS[bbid]

        return GsAssetApi.map_identifiers(GsIdType.mdapi, GsIdType.id, [to_asset])[to_asset]

    except KeyError:
        logging.info(f'Unsupported currency or cross ${bbid}')
        raise from_asset.get_marquee_id()


def _get_custom_bd(exchange):
    from pandas.tseries.offsets import CustomBusinessDay
    calendar = GsCalendar.get(exchange).business_day_calendar()
    return CustomBusinessDay(calendar=calendar)


@log_return(_logger, 'trying pricing dates')
def _range_from_pricing_date(exchange, pricing_date: Optional[GENERIC_DATE] = None):
    if isinstance(pricing_date, datetime.date):
        return pricing_date, pricing_date

    today = pd.Timestamp.today().normalize()
    if pricing_date is None:
        t1 = today - _get_custom_bd(exchange)
        return t1, t1

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


def _market_data_timed(q):
    start = time.perf_counter()
    df = GsDataApi.get_market_data(q)
    _logger.debug('market data query ran in %.3f ms', (time.perf_counter() - start) * 1000)
    return df


@plot_measure((AssetClass.FX, AssetClass.Equity), None, [MeasureDependency(
    id_provider=cross_stored_direction_for_fx_vol, query_type=QueryType.IMPLIED_VOLATILITY)])
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

    asset_id = asset.get_marquee_id()

    if asset.asset_class == AssetClass.FX:
        asset_id = cross_stored_direction_for_fx_vol(asset_id)
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
    q = GsDataApi.build_market_data_query([asset_id], QueryType.IMPLIED_VOLATILITY, where=where, source=source)
    _logger.debug('q %s', q)
    df = _market_data_timed(q)

    if df.empty:
        return pd.Series()

    curves = {k: v for k, v in df.groupby(column)}
    if len(curves) < 3:
        raise MqValueError('skew not available for given inputs')
    series = [curves[qs]['impliedVolatility'] for qs in q_strikes]
    return (series[0] - series[1]) / series[2]


@plot_measure((AssetClass.Credit,), (AssetType.Index,), [QueryType.IMPLIED_VOLATILITY_BY_DELTA_STRIKE])
def cds_implied_volatility(asset: Asset, expiry: str, tenor: str, strike_reference: CdsVolReference,
                           relative_strike: Real, *, source: str = None, real_time: bool = False) -> Series:
    """
    Volatility of a cds index implied by observations of market prices.

    :param asset: asset object loaded from security master
    :param expiry: relative date representation of expiration date on the option e.g. 3m
    :param tenor: relative date representation of expiration date e.g. 1m
    :param strike_reference: reference for strike level
    :param relative_strike: strike relative to reference
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: implied volatility curve
    """
    if real_time:
        raise NotImplementedError('realtime cds_implied_volatility not implemented')

    delta_strike = "ATMF" if strike_reference is CdsVolReference.FORWARD else "{}DC".format(relative_strike)
    option_type = "payer" if strike_reference is CdsVolReference.DELTA_CALL else "receiver"

    _logger.debug('where expiry=%s, tenor=%s, deltaStrike=%s, optionType=%s, location=NYC',
                  expiry, tenor, delta_strike, option_type)

    q = GsDataApi.build_market_data_query(
        [asset.get_marquee_id()],
        QueryType.IMPLIED_VOLATILITY_BY_DELTA_STRIKE,
        where=FieldFilterMap(
            expiry=expiry,
            tenor=tenor,
            deltaStrike=delta_strike,
            optionType=option_type,
            location='NYC'
        ),
        source=source,
        real_time=real_time
    )
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return Series() if df.empty else df['impliedVolatilityByDeltaStrike']


@plot_measure((AssetClass.Equity, AssetClass.Commod, AssetClass.FX,), None,
              [MeasureDependency(id_provider=cross_stored_direction_for_fx_vol,
                                 query_type=QueryType.IMPLIED_VOLATILITY)])
def implied_volatility(asset: Asset, tenor: str, strike_reference: VolReference, relative_strike: Real = None, *,
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
    if relative_strike is None and strike_reference != VolReference.DELTA_NEUTRAL:
        raise MqValueError('Relative strike must be provided if your strike reference is not delta_neutral')

    if asset.asset_class == AssetClass.FX:
        if strike_reference == VolReference.FORWARD:
            if relative_strike != 100:
                raise MqValueError('Relative strike must be 100 for Forward strike reference')
        elif strike_reference == VolReference.SPOT:
            if relative_strike != 100:
                raise MqValueError('Relative strike must be 100 for Spot strike reference')
        elif strike_reference not in VolReference or strike_reference == VolReference.NORMALIZED:
            raise MqValueError('strikeReference: ' + strike_reference.value + ' not supported for FX')

        asset_id = cross_stored_direction_for_fx_vol(asset.get_marquee_id())
        _logger.debug('where tenor=%s, strikeRef=%s, relativeStrike=%s', tenor, strike_reference.value, relative_strike)
        q = GsDataApi.build_market_data_query(
            [asset_id],
            QueryType.IMPLIED_VOLATILITY,
            where=FieldFilterMap(tenor=tenor, strikeRef=strike_reference.value, relativeStrike=relative_strike),
            source=source,
            real_time=real_time
        )
        _logger.debug('q %s', q)
        df = _market_data_timed(q)
    else:
        if strike_reference == VolReference.DELTA_NEUTRAL:
            raise NotImplementedError('delta_neutral strike reference is not supported for equities.')

        if strike_reference == VolReference.DELTA_PUT:
            relative_strike = abs(100 - relative_strike)
        relative_strike = relative_strike if strike_reference == VolReference.NORMALIZED else relative_strike / 100
        ref_string = "delta" if strike_reference in (VolReference.DELTA_CALL,
                                                     VolReference.DELTA_PUT) else strike_reference.value

        _logger.debug('where tenor=%s, strikeReference=%s, relativeStrike=%s', tenor, ref_string, relative_strike)
        where = FieldFilterMap(tenor=tenor, strikeReference=ref_string, relativeStrike=relative_strike)
        q = GsDataApi.build_market_data_query([asset.get_marquee_id()], QueryType.IMPLIED_VOLATILITY,
                                              where=where, source=source, real_time=real_time)
        _logger.debug('q %s', q)
        df = _market_data_timed(q)
    return Series() if df.empty else df['impliedVolatility']


@plot_measure((AssetClass.Equity,), (AssetType.Index, AssetType.ETF,), [QueryType.IMPLIED_CORRELATION])
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
    if real_time:
        raise NotImplementedError('realtime implied_correlation not implemented')

    if strike_reference == EdrDataReference.DELTA_PUT:
        relative_strike = abs(100 - relative_strike)

    relative_strike = relative_strike / 100

    delta_types = (EdrDataReference.DELTA_CALL, EdrDataReference.DELTA_PUT)
    strike_ref = "delta" if strike_reference in delta_types else strike_reference.value

    _logger.debug('where tenor=%s, strikeReference=%s, relativeStrike=%s', tenor, strike_ref, relative_strike)

    mqid = asset.get_marquee_id()
    where = FieldFilterMap(tenor=tenor, strikeReference=strike_ref, relativeStrike=relative_strike)
    q = GsDataApi.build_market_data_query([mqid], QueryType.IMPLIED_CORRELATION, where=where, source=source,
                                          real_time=real_time)

    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return Series() if df.empty else df['impliedCorrelation']


@plot_measure((AssetClass.Equity,), (AssetType.Index, AssetType.ETF,), [QueryType.AVERAGE_IMPLIED_VOLATILITY])
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
    if real_time:
        raise NotImplementedError('realtime average_implied_volatility not implemented')

    if strike_reference == EdrDataReference.DELTA_PUT:
        relative_strike = abs(100 - relative_strike)

    relative_strike = relative_strike / 100

    delta_types = (EdrDataReference.DELTA_CALL, EdrDataReference.DELTA_PUT)
    strike_ref = "delta" if strike_reference in delta_types else strike_reference.value

    _logger.debug('where tenor=%s, strikeReference=%s, relativeStrike=%s', tenor, strike_ref, relative_strike)

    mqid = asset.get_marquee_id()
    where = FieldFilterMap(tenor=tenor, strikeReference=strike_ref, relativeStrike=relative_strike)
    q = GsDataApi.build_market_data_query([mqid], QueryType.AVERAGE_IMPLIED_VOLATILITY,
                                          where=where, source=source, real_time=real_time)

    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return Series() if df.empty else df['averageImpliedVolatility']


@plot_measure((AssetClass.Equity,), (AssetType.Index, AssetType.ETF,), [QueryType.AVERAGE_IMPLIED_VARIANCE])
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
    if real_time:
        raise NotImplementedError('realtime average_implied_variance not implemented')

    if strike_reference == EdrDataReference.DELTA_PUT:
        relative_strike = abs(100 - relative_strike)

    relative_strike = relative_strike / 100

    delta_types = (EdrDataReference.DELTA_CALL, EdrDataReference.DELTA_PUT)
    strike_ref = "delta" if strike_reference in delta_types else strike_reference.value

    _logger.debug('where tenor=%s, strikeReference=%s, relativeStrike=%s', tenor, strike_ref, relative_strike)

    mqid = asset.get_marquee_id()
    where = FieldFilterMap(tenor=tenor, strikeReference=strike_ref, relativeStrike=relative_strike)
    q = GsDataApi.build_market_data_query([mqid], QueryType.AVERAGE_IMPLIED_VARIANCE, where=where, source=source,
                                          real_time=real_time)

    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return Series() if df.empty else df['averageImpliedVariance']


@plot_measure((AssetClass.Cash,), (AssetType.Currency,), [QueryType.SWAP_RATE])
def swap_rate(asset: Asset, tenor: str, benchmark_type: BenchmarkType = None, floating_index: str = None,
              pricing_location: PricingLocation = None, *, source: str = None, real_time: bool = False) -> Series:
    """
    GS end-of-day Fixed-Floating interest rate swap (IRS) curves across major currencies.

    :param asset: asset object loaded from security master
    :param tenor: relative date representation of expiration date e.g. 1m
    :param benchmark_type: benchmark type e.g. LIBOR
    :param floating_index: floating index rate
    :param pricing_location: the pricing location (used for EOD data only)
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: swap rate curve
    """
    if real_time:
        raise NotImplementedError('realtime swap_rate not implemented')

    currency = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)
    currency = Currency(currency)

    if currency == Currency.KRW:
        if benchmark_type not in (None, BenchmarkType.CDKSDA) or floating_index not in (None, '3m'):
            raise NotImplementedError('Unsupported benchmark for {} swap rates'.format(currency.value))

        # default pricing location
        pricing_location = pricing_location or PricingLocation.HKG

        rate_mqid = asset.get_marquee_id()
        where = FieldFilterMap(tenor=tenor, pricing_location=pricing_location.value)

        _logger.debug('where tenor=%s, pricingLocation=%s', tenor, pricing_location.value)

    else:
        if pricing_location not in (None, PricingLocation.LDN):
            raise NotImplementedError('Unsupported pricing location {} for {} swap rates'.format(pricing_location.value,
                                                                                                 currency.value))
        # default benchmark types
        if benchmark_type is None:
            if currency == Currency.EUR:
                benchmark_type = BenchmarkType.EURIBOR
            elif currency == Currency.SEK:
                benchmark_type = BenchmarkType.STIBOR
            else:
                benchmark_type = BenchmarkType.LIBOR

        over_nights = [BenchmarkType.OIS]

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
        where = FieldFilterMap(tenor=tenor)

        _logger.debug('where tenor=%s, floatingIndex=%s', tenor, floating_index)

    q = GsDataApi.build_market_data_query(
        [rate_mqid],
        QueryType.SWAP_RATE,
        where=where,
        source=source,
        real_time=real_time
    )

    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return Series() if df.empty else df['swapRate']


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=currency_to_default_benchmark_rate, query_type=QueryType.SWAPTION_VOL)])
def swaption_vol(asset: Asset, expiration_tenor: str, termination_tenor: str, relative_strike: float,
                 *, source: str = None, real_time: bool = False) -> Series:
    """
    GS end-of-day implied normal volatility for swaption vol matrices.

    :param asset: asset object loaded from security master
    :param expiration_tenor: relative date representation of expiration date on the option e.g. 3m
    :param termination_tenor: relative date representation of the instrument's expiration date e.g. 1y
    :param relative_strike: strike level relative to at the money e.g. 10
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: swaption implied normal volatility curve
    """
    if real_time:
        raise NotImplementedError('realtime swaption_vol not implemented')

    rate_benchmark_mqid = convert_asset_for_rates_data_set(asset, RatesConversionType.DEFAULT_BENCHMARK_RATE)

    _logger.debug('where expiry=%s, tenor=%s, strike=%s', expiration_tenor, termination_tenor, relative_strike)

    q = GsDataApi.build_market_data_query(
        [rate_benchmark_mqid],
        QueryType.SWAPTION_VOL,
        where=FieldFilterMap(expiry=expiration_tenor, tenor=termination_tenor, strike=relative_strike),
        source=source,
        real_time=real_time
    )

    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return Series() if df.empty else df['swaptionVol']


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=currency_to_default_benchmark_rate, query_type=QueryType.ATM_FWD_RATE)])
def swaption_atm_fwd_rate(asset: Asset, expiration_tenor: str, termination_tenor: str, *, source: str = None,
                          real_time: bool = False) -> Series:
    """
    GS end-of-day at-the-money forward rate for swaption vol matrices.

    :param asset: asset object loaded from security master
    :param expiration_tenor: relative date representation of expiration date on the option e.g. 3m
    :param termination_tenor: relative date representation of the instrument's expiration date e.g. 1y
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: swaption at-the-money forward rate curve
    """
    if real_time:
        raise NotImplementedError('realtime swaption_atm_fwd_rate not implemented')

    rate_benchmark_mqid = convert_asset_for_rates_data_set(asset, RatesConversionType.DEFAULT_BENCHMARK_RATE)

    _logger.debug('where expiry=%s, tenor=%s', expiration_tenor, termination_tenor)

    q = GsDataApi.build_market_data_query(
        [rate_benchmark_mqid],
        QueryType.ATM_FWD_RATE,
        where=FieldFilterMap(expiry=expiration_tenor, tenor=termination_tenor, strike=0),
        source=source,
        real_time=real_time
    )

    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return Series() if df.empty else df['atmFwdRate']


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=currency_to_default_benchmark_rate, query_type=QueryType.MIDCURVE_VOL)])
def midcurve_vol(asset: Asset, expiration_tenor: str, forward_tenor: str, termination_tenor: str,
                 relative_strike: float,
                 *, source: str = None, real_time: bool = False) -> Series:
    """
    GS end-of-day implied normal volatility for midcurve vol matrices.

    :param asset: asset object loaded from security master
    :param expiration_tenor: relative date representation of expiration date on the option e.g. 3m
    :param forward_tenor: relative date representation of swap's start date after option expiry e.g. 2y
    :param termination_tenor: relative date representation of the instrument's expiration date e.g. 1y
    :param relative_strike: strike level relative to at the money e.g. 10
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: midcurve implied normal volatility curve
    """
    if real_time:
        raise NotImplementedError('realtime midcurve_vol not implemented')

    _logger.debug('where expiry=%s, forwardTenor=%s, tenor=%s, strike=%s', expiration_tenor, forward_tenor,
                  termination_tenor, relative_strike)

    rate_benchmark_mqid = convert_asset_for_rates_data_set(asset, RatesConversionType.DEFAULT_BENCHMARK_RATE)

    q = GsDataApi.build_market_data_query(
        [rate_benchmark_mqid],
        QueryType.MIDCURVE_VOL,
        where=FieldFilterMap(expiry=expiration_tenor, forwardTenor=forward_tenor, tenor=termination_tenor,
                             strike=relative_strike),
        source=source,
        real_time=real_time
    )

    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return Series() if df.empty else df['midcurveVol']


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=currency_to_default_benchmark_rate,
                                 query_type=QueryType.MIDCURVE_ATM_FWD_RATE)])
def midcurve_atm_fwd_rate(asset: Asset, expiration_tenor: str, forward_tenor: str, termination_tenor: str,
                          *, source: str = None, real_time: bool = False) -> Series:
    """
    GS end-of-day at-the-money forward rate for midcurve vol matrices.

    :param asset: asset object loaded from security master
    :param expiration_tenor: relative date representation of expiration date on the option e.g. 3m
    :param forward_tenor: relative date representation of swap's start date after option expiry e.g. 2y
    :param termination_tenor: relative date representation of the instrument's expiration date e.g. 1y
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: midcurve atm forward rate curve
    """
    if real_time:
        raise NotImplementedError('realtime midcurve_atm_fwd_rate not implemented')

    q = GsDataApi.build_market_data_query(
        [convert_asset_for_rates_data_set(asset, RatesConversionType.DEFAULT_BENCHMARK_RATE)],
        QueryType.MIDCURVE_ATM_FWD_RATE,
        where=FieldFilterMap(expiry=expiration_tenor, forwardTenor=forward_tenor, tenor=termination_tenor, strike=0),
        source=source,
        real_time=real_time
    )

    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return Series() if df.empty else df['midcurveAtmFwdRate']


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=currency_to_default_benchmark_rate, query_type=QueryType.CAP_FLOOR_VOL)])
def cap_floor_vol(asset: Asset, expiration_tenor: str, relative_strike: float, *, source: str = None,
                  real_time: bool = False) -> Series:
    """
    GS end-of-day implied normal volatility for cap and floor vol matrices.

    :param asset: asset object loaded from security master
    :param expiration_tenor: relative date representation of expiration date on the option e.g. 3m
    :param relative_strike: strike level relative to at the money e.g. 10
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: cap and floor implied normal volatility curve
    """
    if real_time:
        raise NotImplementedError('realtime cap_floor_vol not implemented')

    rate_benchmark_mqid = convert_asset_for_rates_data_set(asset, RatesConversionType.DEFAULT_BENCHMARK_RATE)

    _logger.debug('where expiry=%s, strike=%s', expiration_tenor, relative_strike)

    q = GsDataApi.build_market_data_query(
        [rate_benchmark_mqid],
        QueryType.CAP_FLOOR_VOL,
        where=FieldFilterMap(expiry=expiration_tenor, strike=relative_strike),
        source=source,
        real_time=real_time
    )

    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return Series() if df.empty else df['capFloorVol']


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=currency_to_default_benchmark_rate,
                                 query_type=QueryType.CAP_FLOOR_ATM_FWD_RATE)])
def cap_floor_atm_fwd_rate(asset: Asset, expiration_tenor: str, *, source: str = None,
                           real_time: bool = False) -> Series:
    """
    GS end-of-day at-the-money forward rate for cap and floor matrices.

    :param asset: asset object loaded from security master
    :param expiration_tenor: relative date representation of expiration date on the option e.g. 3m
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: cap and floor atm forward rate curve
    """
    if real_time:
        raise NotImplementedError('realtime cap_floor_atm_fwd_rate not implemented')

    q = GsDataApi.build_market_data_query(
        [convert_asset_for_rates_data_set(asset, RatesConversionType.DEFAULT_BENCHMARK_RATE)],
        QueryType.CAP_FLOOR_ATM_FWD_RATE,
        where=FieldFilterMap(expiry=expiration_tenor, strike=0),
        source=source,
        real_time=real_time
    )

    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return Series() if df.empty else df['capFloorAtmFwdRate']


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=currency_to_default_benchmark_rate,
                                 query_type=QueryType.SPREAD_OPTION_VOL)])
def spread_option_vol(asset: Asset, expiration_tenor: str, long_tenor: str, short_tenor: str, relative_strike: float,
                      *, source: str = None, real_time: bool = False) -> Series:
    """
    GS end-of-day implied normal volatility for spread option vol matrices.

    :param asset: asset object loaded from security master
    :param expiration_tenor: relative date representation of expiration date on the option e.g. 3m
    :param long_tenor: relative date representation of the instrument's tenor date e.g. 1y
    :param short_tenor: relative date representation of the instrument's tenor date e.g. 1y
    :param relative_strike: strike level relative to at the money e.g. 10
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: spread option implied normal volatility curve
    """
    if real_time:
        raise NotImplementedError('realtime spread_option_vol not implemented')

    rate_benchmark_mqid = convert_asset_for_rates_data_set(asset, RatesConversionType.DEFAULT_BENCHMARK_RATE)

    _logger.debug('where expiry=%s, longTenor=%s, shortTenor=%s, strike=%s', expiration_tenor, long_tenor, short_tenor,
                  relative_strike)

    q = GsDataApi.build_market_data_query(
        [rate_benchmark_mqid],
        QueryType.SPREAD_OPTION_VOL,
        where=FieldFilterMap(expiry=expiration_tenor, longTenor=long_tenor, shortTenor=short_tenor,
                             strike=relative_strike),
        source=source,
        real_time=real_time
    )

    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return Series() if df.empty else df['spreadOptionVol']


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=currency_to_default_benchmark_rate,
                                 query_type=QueryType.SPREAD_OPTION_ATM_FWD_RATE)])
def spread_option_atm_fwd_rate(asset: Asset, expiration_tenor: str, long_tenor: str, short_tenor: str,
                               *, source: str = None, real_time: bool = False) -> Series:
    """
    GS end-of-day At-the-money forward rate for spread option vol matrices.

    :param asset: asset object loaded from security master
    :param expiration_tenor: relative date representation of expiration date on the option e.g. 3m
    :param long_tenor: relative date representation of the instrument's tenor date e.g. 1y
    :param short_tenor: relative date representation of the instrument's tenor date e.g. 1y
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: spread option at-the-money forward rate curve
    """
    if real_time:
        raise NotImplementedError('realtime spread_option_atm_fwd_rate not implemented')

    q = GsDataApi.build_market_data_query(
        [convert_asset_for_rates_data_set(asset, RatesConversionType.DEFAULT_BENCHMARK_RATE)],
        QueryType.SPREAD_OPTION_ATM_FWD_RATE,
        where=FieldFilterMap(expiry=expiration_tenor, longTenor=long_tenor, shortTenor=short_tenor, strike=0),
        source=source,
        real_time=real_time
    )

    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return Series() if df.empty else df['spreadOptionAtmFwdRate']


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=currency_to_inflation_benchmark_rate,
                                 query_type=QueryType.INFLATION_SWAP_RATE)])
def zc_inflation_swap_rate(asset: Asset, termination_tenor: str, *, source: str = None,
                           real_time: bool = False) -> Series:
    """
    GS end-of-day zero coupon inflation swap break-even rate.

    :param asset: asset object loaded from security master
    :param termination_tenor: relative date representation of the instrument's expiration date e.g. 1y
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: zero coupon inflation swap break-even rate curve
    """
    if real_time:
        raise NotImplementedError('realtime zc_inflation_swap_rate not implemented')

    infl_rate_benchmark_mqid = convert_asset_for_rates_data_set(asset, RatesConversionType.INFLATION_BENCHMARK_RATE)

    _logger.debug('where tenor=%s', termination_tenor)

    q = GsDataApi.build_market_data_query(
        [infl_rate_benchmark_mqid],
        QueryType.INFLATION_SWAP_RATE,
        where=FieldFilterMap(tenor=termination_tenor),
        source=source,
        real_time=real_time
    )

    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return Series() if df.empty else df['inflationSwapRate']


@plot_measure((AssetClass.FX,), (AssetType.Cross,),
              [MeasureDependency(id_provider=cross_to_basis, query_type=QueryType.BASIS)])
def basis(asset: Asset, termination_tenor: str, *, source: str = None, real_time: bool = False) -> Series:
    """
    GS end-of-day cross-currency basis swap spread.

    :param asset: asset object loaded from security master
    :param termination_tenor: relative date representation of the instrument's expiration date e.g. 1y
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: cross-currency basis swap spread curve
    """
    if real_time:
        raise NotImplementedError('realtime basis not implemented')

    basis_mqid = convert_asset_for_rates_data_set(asset, RatesConversionType.CROSS_CURRENCY_BASIS)

    _logger.debug('where tenor=%s', termination_tenor)

    q = GsDataApi.build_market_data_query(
        [basis_mqid],
        QueryType.BASIS,
        where=FieldFilterMap(tenor=termination_tenor),
        source=source,
        real_time=real_time
    )

    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return Series() if df.empty else df['basis']


@plot_measure((AssetClass.FX,), (AssetType.Cross,), [MeasureDependency(
    id_provider=cross_to_usd_based_cross, query_type=QueryType.FORECAST)])
def forecast(asset: Asset, forecast_horizon: str, *, source: str = None, real_time: bool = False) -> Series:
    """
    GS end-of-day FX forecasts made by Global Investment Research (GIR) macro analysts.

    :param asset: asset object loaded from security master
    :param forecast_horizon: relative period of time to forecast e.g. 1y
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: FX forecast curve
    """
    if real_time:
        raise NotImplementedError('realtime forecast not implemented')

    cross_mqid = asset.get_marquee_id()
    usd_based_cross_mqid = cross_to_usd_based_cross(cross_mqid)

    horizon = '12m' if forecast_horizon == '1y' else forecast_horizon

    q = GsDataApi.build_market_data_query(
        [usd_based_cross_mqid],
        QueryType.FORECAST,
        where=FieldFilterMap(relativePeriod=horizon),
        source=source,
        real_time=real_time
    )
    _logger.debug('q %s', q)
    df = _market_data_timed(q)

    series = Series() if df.empty else df['forecast']

    if cross_mqid != usd_based_cross_mqid:
        series = 1 / series

    return series


@plot_measure((AssetClass.Equity, AssetClass.Commod), None, [QueryType.IMPLIED_VOLATILITY])
def vol_term(asset: Asset, strike_reference: SkewReference, relative_strike: Real,
             pricing_date: Optional[GENERIC_DATE] = None, *, source: str = None, real_time: bool = False) -> pd.Series:
    """
    Volatility term structure. Uses most recent date available if pricing_date is not provided.

    :param asset: asset object loaded from security master
    :param strike_reference: reference for strike level
    :param relative_strike: strike relative to reference
    :param pricing_date: YYYY-MM-DD or relative days before today e.g. 1d, 1m, 1y
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
        q = GsDataApi.build_market_data_query([asset.get_marquee_id()], QueryType.IMPLIED_VOLATILITY, where=where,
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


@plot_measure((AssetClass.Equity,), None, [QueryType.IMPLIED_VOLATILITY])
def vol_smile(asset: Asset, tenor: str, strike_reference: VolSmileReference,
              pricing_date: Optional[GENERIC_DATE] = None,
              *, source: str = None, real_time: bool = False) -> Series:
    """
    Volatility smile of an asset implied by observations of market prices.

    :param asset: asset object loaded from security master
    :param tenor: relative date representation of expiration date e.g. 1m
    :param strike_reference: reference for strike level
    :param pricing_date: YYYY-MM-DD or relative days before today e.g. 1d, 1m, 1y
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: implied volatility smile
    """
    if real_time:
        raise NotImplementedError('realtime vol_smile not implemented')

    mqid = asset.get_marquee_id()

    start, end = _range_from_pricing_date(asset.exchange, pricing_date)

    with DataContext(start, end):
        q = GsDataApi.build_market_data_query(
            [mqid],
            QueryType.IMPLIED_VOLATILITY,
            where=FieldFilterMap(tenor=tenor, strikeReference=strike_reference.value),
            source=source,
            real_time=real_time
        )
        _logger.debug('q %s', q)
        df = _market_data_timed(q)

    if df.empty:
        return Series

    latest = df.index.max()
    _logger.info('selected pricing date %s', latest)
    df = df.loc[latest]

    vols = df['impliedVolatility'].values
    strikes = df['relativeStrike'].values
    return Series(vols, index=strikes)


@plot_measure((AssetClass.Equity, AssetClass.Commod), None, [QueryType.FORWARD])
def fwd_term(asset: Asset, pricing_date: Optional[GENERIC_DATE] = None, *, source: str = None,
             real_time: bool = False) -> pd.Series:
    """
    Forward term structure. Uses most recent date available if pricing_date is not provided.

    :param asset: asset object loaded from security master
    :param pricing_date: YYYY-MM-DD or relative days before today e.g. 1d, 1m, 1y
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: forward term structure
    """
    if real_time:
        raise NotImplementedError('realtime forward term not implemented')  # TODO

    start, end = _range_from_pricing_date(asset.exchange, pricing_date)
    with DataContext(start, end):
        where = FieldFilterMap(strikeReference='forward', relativeStrike=1)
        q = GsDataApi.build_market_data_query([asset.get_marquee_id()], QueryType.FORWARD, where=where, source=source,
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


@cachetools.func.ttl_cache()  # fine as long as availability is not different between users
def _var_swap_tenors(asset: Asset):
    from gs_quant.session import GsSession

    aid = asset.get_marquee_id()
    body = GsSession.current._get(f"/data/markets/{aid}/availability")
    for r in body['data']:
        if r['dataField'] == Fields.VAR_SWAP.value:
            for f in r['filteredFields']:
                if f['field'] == Fields.TENOR.value:
                    return f['values']
    raise MqValueError("var swap is not available for " + aid)


def _tenor_to_month(relative_date: str) -> int:
    matcher = re.fullmatch('([1-9]\\d*)([my])', relative_date)
    if matcher:
        mag = int(matcher.group(1))
        return mag if matcher.group(2) == 'm' else mag * 12
    raise MqValueError('invalid input: relative date must be in months or years')


def _month_to_tenor(months: int) -> str:
    return f'{months // 12}y' if months % 12 == 0 else f'{months}m'


@plot_measure((AssetClass.Equity, AssetClass.Commod), None, [QueryType.VAR_SWAP])
def var_term(asset: Asset, pricing_date: Optional[str] = None, forward_start_date: Optional[str] = None,
             *, source: str = None, real_time: bool = False) -> pd.Series:
    """
    Variance swap term structure. Uses most recent date available if pricing_date is not provided.

    :param asset: asset object loaded from security master
    :param pricing_date: relative days before today e.g. 3d, 2m, 1y
    :param forward_start_date: forward start date e.g. 2m, 1y; defaults to none
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: variance swap term structure
    """
    if not (pricing_date is None or isinstance(pricing_date, str)):
        raise MqTypeError('pricing_date should be a relative date')

    start, end = _range_from_pricing_date(asset.exchange, pricing_date)
    with DataContext(start, end):
        if forward_start_date:
            tenors = _var_swap_tenors(asset)
            sub_frames = []
            for t in tenors:
                diff = _tenor_to_month(t) - _tenor_to_month(forward_start_date)
                if diff < 1:
                    continue
                t1 = _month_to_tenor(diff)
                c = var_swap(asset, t1, forward_start_date, source=source, real_time=real_time).to_frame()
                if not c.empty:
                    c['tenor'] = t1
                    sub_frames.append(c)
            df = pd.concat(sub_frames)
        else:
            q = GsDataApi.build_market_data_query([asset.get_marquee_id()], QueryType.VAR_SWAP,
                                                  source=source, real_time=real_time)
            _logger.debug('q %s', q)
            df = _market_data_timed(q)

    if df.empty:
        return pd.Series()

    latest = df.index.max()
    _logger.info('selected pricing date %s', latest)
    df = df.loc[latest]
    cbd = _get_custom_bd(asset.exchange)
    df.loc[:, Fields.EXPIRATION_DATE.value] = df.index + df[Fields.TENOR.value].map(_to_offset) + cbd - cbd
    df = df.set_index(Fields.EXPIRATION_DATE.value)
    df.sort_index(inplace=True)
    df = df.loc[DataContext.current.start_date: DataContext.current.end_date]
    return df[Fields.VAR_SWAP.value] if not df.empty else pd.Series()


@plot_measure((AssetClass.Equity, AssetClass.Commod,), None, [QueryType.VAR_SWAP])
def var_swap(asset: Asset, tenor: str, forward_start_date: Optional[str] = None,
             *, source: str = None, real_time: bool = False) -> Series:
    """
    Strike such that the price of an uncapped variance swap on the underlying index is zero at inception. If
    forward start date is provided, then the result is a forward starting variance swap.

    :param asset: asset object loaded from security master
    :param tenor: relative date representation of expiration date e.g. 1m
    :param forward_start_date: forward start date e.g. 2m, 1y; defaults to none
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: implied volatility curve
    """

    if forward_start_date is None:
        _logger.debug('where tenor=%s', tenor)
        where = FieldFilterMap(tenor=tenor)
        q = GsDataApi.build_market_data_query([asset.get_marquee_id()], QueryType.VAR_SWAP,
                                              where=where, source=source, real_time=real_time)
        _logger.debug('q %s', q)
        df = _market_data_timed(q)
        return Series() if df.empty else df[Fields.VAR_SWAP.value]
    else:
        if not isinstance(forward_start_date, str):
            raise MqTypeError('forward_start_date must be a relative date')

        x = _tenor_to_month(tenor)
        y = _tenor_to_month(forward_start_date)
        z = x + y
        yt = _month_to_tenor(y)
        zt = _month_to_tenor(z)

        tenors = _var_swap_tenors(asset)
        if yt not in tenors or zt not in tenors:
            return Series()

        _logger.debug('where tenor=%s', f'{yt},{zt}')
        where = FieldFilterMap(tenor=[yt, zt])
        q = GsDataApi.build_market_data_query([asset.get_marquee_id()], QueryType.VAR_SWAP,
                                              where=where, source=source, real_time=real_time)
        _logger.debug('q %s', q)
        df = _market_data_timed(q)
        if df.empty:
            return Series()

        grouped = df.groupby(Fields.TENOR.value)
        try:
            yg = grouped.get_group(yt)[Fields.VAR_SWAP.value]
            zg = grouped.get_group(zt)[Fields.VAR_SWAP.value]
        except KeyError:
            _logger.debug('no data for one or more tenors')
            return Series()
        return (z * zg - y * yg) / x


@plot_measure((AssetClass.Commod,), None, [QueryType.PRICE])
def bucketize_price(asset: Asset, price_method: str, bucket: str = '7x24',
                    granularity: str = 'daily', *, source: str = None, real_time: bool = False) -> pd.Series:
    """'
    Bucketized COMMOD_US_ELEC_ENERGY_PRICES

    :param asset: asset object loaded from security master
    :param price_method: price method between LMP, MCP, SPP, energy, loss, congestion: Default value = LMP
    :param bucket: bucket type among '7x24', 'peak', 'offpeak', '2x16h' and '7x8': Default value = 7x24
    :param granularity: daily or monthly: default value = daily
    :param source: name of function caller: default source = None
    :param real_time: whether to retrieve intraday data instead of EOD: default value = False
    :return: Bucketized elec energy prices
    """
    if real_time:
        raise ValueError('Bucketize function returns aggregated daily data')

    # create granularity indicator
    if granularity.lower() in ['daily', 'd']:
        granularity = 'D'
    elif granularity.lower() in ['monthly', 'm']:
        granularity = 'M'
    else:
        raise ValueError('Invalid granularity: ' + granularity + '. Expected Value: daily or monthly.')

    bbid = Asset.get_identifier(asset, AssetIdentifier.BLOOMBERG_ID)

    # TODO: get timezone info from Asset
    # default frequency definition
    timezone = 'US/Eastern'
    peak_start = 7
    peak_end = 23
    weekends = [5, 6]

    if bbid.split(" ")[0] in ['MISO', 'ERCOT', 'SPP']:
        timezone = 'US/Central'
        peak_start = 6
        peak_end = 22
    if bbid.split(" ")[0] == 'CAISO':
        timezone = 'US/Pacific'
        weekends = [6]

    to_zone = tz.gettz('UTC')
    from_zone = tz.gettz(timezone)

    # Start date and end date are considered to be in ISO's local timezone
    start_date, end_date = DataContext.current.start_date, DataContext.current.end_date
    # Start time is constructed by combining start date with 00:00:00 timestamp
    # in local time and then converted to UTC time
    # End time is constructed by combining end date with 23:59:59 timestamp
    # in local time and then converted to UTC time
    start_time = datetime.datetime.combine(start_date, datetime.datetime.min.time(), tzinfo=from_zone) \
        .astimezone(to_zone)
    end_time = datetime.datetime.combine(end_date, datetime.datetime.max.time(), tzinfo=from_zone).astimezone(to_zone)

    where = FieldFilterMap(priceMethod=price_method)
    with DataContext(start_time, end_time):
        q = GsDataApi.build_market_data_query([asset.get_marquee_id()], QueryType.PRICE, where=where, source=source,
                                              real_time=True)
        df = _market_data_timed(q)
        _logger.debug('q %s', q)

    df = df.tz_convert(timezone)

    df['month'] = df.index.to_period('M')
    df['date'] = df.index.date
    df['day'] = df.index.dayofweek
    df['hour'] = df.index.hour
    holidays = NercCalendar().holidays(start=start_date, end=end_date).date

    # freq is the frequency at which the ISO publishes data for e.g. 15 min, 1hr
    freq = int(min(np.diff(df.index) / np.timedelta64(1, 's')))
    # checking missing data points
    ref_hour_range = pd.date_range(str(start_date), str(end_date + datetime.timedelta(days=1)),
                                   freq=str(freq) + "S", tz=timezone, closed='left')
    missing_hours = ref_hour_range[~ref_hour_range.isin(df.index)]
    missing_dates = np.unique(missing_hours.date)
    missing_months = np.unique(np.array(missing_dates, dtype='M8[D]').astype('M8[M]'))

    # drop dates and months which have missing data
    df = df.loc[(~df['date'].isin(missing_dates))]
    if granularity == 'M':
        df = df.loc[(~df['month'].isin(missing_months))]

    # TODO: get frequency definition from SecDB
    if bucket.lower() == '7x24':
        pass
    # offpeak: 11pm-7am & weekend & holiday
    elif bucket.lower() == 'offpeak':
        df = df.loc[df['date'].isin(holidays) |
                    df['day'].isin(weekends) |
                    (~df['date'].isin(holidays) & ~df['day'].isin(weekends) &
                     ((df['hour'] < peak_start) | (df['hour'] > peak_end - 1)))]
    # peak: 7am to 11pm on weekdays
    elif bucket.lower() == 'peak':
        df = df.loc[(~df['date'].isin(holidays)) & (~df['day'].isin(weekends)) & (df['hour'] > peak_start - 1) &
                    (df['hour'] < peak_end)]
    # 7x8: 11pm to 7am
    elif bucket.lower() == '7x8':
        df = df.loc[(df['hour'] < peak_start) | (df['hour'] > peak_end - 1)]
    # 2x16h: weekends & holidays
    elif bucket.lower() == '2x16h':
        df = df.loc[((df['date'].isin(holidays)) | df['day'].isin(weekends)) & ((df['hour'] > peak_start - 1) &
                                                                                (df['hour'] < peak_end))]
    else:
        raise ValueError('Invalid bucket: ' + bucket + '. Expected Value: peak, offpeak, 7x24, 7x8, 2x16h.')

    df = df['price'].resample(granularity).mean()
    df.index = df.index.date
    df = df.loc[start_date: end_date]
    return df


@plot_measure((AssetClass.Equity,), None, [QueryType.FUNDAMENTAL_METRIC])
def dividend_yield(asset: Asset, period: FundamentalMetricPeriod, period_direction: FundamentalMetricPeriodDirection,
                   *, source: str = None, real_time: bool = False) -> Series:
    """
    Dividend Yield of the single stock or the asset-weighted average of dividend yields of a composite's underliers.

    1y forward: time-weighted average of one fiscal year (FY1) and two fiscal year (FY2) fwd-looking estimates.
    2y forward: time-weighted average of two fiscal year (FY2) and three fiscal year (FY3) fwd-looking estimates.
    3y forward: time-weighted average of three fiscal year (FY3) and four fiscal year (FY4) fwd-looking estimates.
    1y trailing: time-weighted average of latest reported fiscal year (FY0) data and one fiscal year (FY1) fwd-looking
    estimate.

    :param asset: asset object loaded from security master
    :param period: the relative fiscal period from now. e.g. 1y
    :param period_direction: whether the period is forward-looking or backward-looking e.g. forward
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: dividend yield
    """
    if real_time:
        raise NotImplementedError('real-time dividend_yield not implemented')

    mqid = asset.get_marquee_id()
    metric = "Dividend Yield"

    _logger.debug('where assetId=%s, metric=%s, period=%s, periodDirection=%s', mqid, metric, period, period_direction)

    q = GsDataApi.build_market_data_query(
        [mqid],
        QueryType.FUNDAMENTAL_METRIC,
        where=FieldFilterMap(metric=metric, period=period.value, periodDirection=period_direction.value),
        source=source,
        real_time=real_time
    )

    q['queries'][0]['vendor'] = 'Goldman Sachs'
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return Series() if df.empty else df['fundamentalMetric']


@plot_measure((AssetClass.Equity,), None, [QueryType.FUNDAMENTAL_METRIC])
def earnings_per_share(asset: Asset,
                       period: FundamentalMetricPeriod,
                       period_direction: FundamentalMetricPeriodDirection,
                       *, source: str = None, real_time: bool = False) -> Series:
    """
    Earnings Per Share (EPS) of the single stock or the asset-weighted average EPS  of a composite's underliers.

    1y forward: time-weighted average of one fiscal year (FY1) and two fiscal year (FY2) fwd-looking estimates.
    2y forward: time-weighted average of two fiscal year (FY2) and three fiscal year (FY3) fwd-looking estimates.
    3y forward: time-weighted average of three fiscal year (FY3) and four fiscal year (FY4) fwd-looking estimates.
    1y trailing: time-weighted average of latest reported fiscal year (FY0) data and one fiscal year (FY1) fwd-looking
    estimate.

    :param asset: asset object loaded from security master
    :param period: the relative fiscal period from now. e.g. 1y
    :param period_direction: whether the period is forward-looking or backward-looking e.g. forward
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: earnings per share
    """
    if real_time:
        raise NotImplementedError('real-time earnings_per_share not implemented')

    mqid = asset.get_marquee_id()
    metric = "Earnings per Share"

    _logger.debug('where assetId=%s, metric=%s, period=%s, periodDirection=%s', mqid, metric, period, period_direction)

    q = GsDataApi.build_market_data_query(
        [mqid],
        QueryType.FUNDAMENTAL_METRIC,
        where=FieldFilterMap(metric=metric, period=period.value, periodDirection=period_direction.value),
        source=source,
        real_time=real_time
    )

    q['queries'][0]['vendor'] = 'Goldman Sachs'
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return Series() if df.empty else df['fundamentalMetric']


@plot_measure((AssetClass.Equity,), None, [QueryType.FUNDAMENTAL_METRIC])
def earnings_per_share_positive(asset: Asset,
                                period: FundamentalMetricPeriod,
                                period_direction: FundamentalMetricPeriodDirection,
                                *, source: str = None, real_time: bool = False) -> Series:
    """
    Earnings Per Share Positive of the single stock or the asset-weighted average EPSP of a composite's underliers.

    1y forward: time-weighted average of one fiscal year (FY1) and two fiscal year (FY2) fwd-looking estimates.
    2y forward: time-weighted average of two fiscal year (FY2) and three fiscal year (FY3) fwd-looking estimates.
    3y forward: time-weighted average of three fiscal year (FY3) and four fiscal year (FY4) fwd-looking estimates.
    1y trailing: time-weighted average of latest reported fiscal year (FY0) data and one fiscal year (FY1) fwd-looking
    estimate.

    :param asset: asset object loaded from security master
    :param period: the relative fiscal period from now. e.g. 1y
    :param period_direction: whether the period is forward-looking or backward-looking e.g. forward
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: earnings per share positive
    """
    if real_time:
        raise NotImplementedError('real-time earnings_per_share_positive not implemented')

    mqid = asset.get_marquee_id()
    metric = "Earnings per Share Positive"

    _logger.debug('where assetId=%s, metric=%s, period=%s, periodDirection=%s', mqid, metric, period, period_direction)

    q = GsDataApi.build_market_data_query(
        [mqid],
        QueryType.FUNDAMENTAL_METRIC,
        where=FieldFilterMap(metric=metric, period=period.value, periodDirection=period_direction.value),
        source=source,
        real_time=real_time
    )

    q['queries'][0]['vendor'] = 'Goldman Sachs'
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return Series() if df.empty else df['fundamentalMetric']


@plot_measure((AssetClass.Equity,), None, [QueryType.FUNDAMENTAL_METRIC])
def net_debt_to_ebitda(asset: Asset,
                       period: FundamentalMetricPeriod,
                       period_direction: FundamentalMetricPeriodDirection,
                       *, source: str = None, real_time: bool = False) -> Series:
    """
    Net Debt to EBITDA of the single stock or the asset-weighted average value of a composite's underliers.

    1y forward: time-weighted average of one fiscal year (FY1) and two fiscal year (FY2) fwd-looking estimates.
    2y forward: time-weighted average of two fiscal year (FY2) and three fiscal year (FY3) fwd-looking estimates.
    3y forward: time-weighted average of three fiscal year (FY3) and four fiscal year (FY4) fwd-looking estimates.
    1y trailing: time-weighted average of latest reported fiscal year (FY0) data and one fiscal year (FY1) fwd-looking
    estimate.

    :param asset: asset object loaded from security master
    :param period: the relative fiscal period from now. e.g. 1y
    :param period_direction: whether the period is forward-looking or backward-looking e.g. forward
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: Net Debt to EBITDA
    """
    if real_time:
        raise NotImplementedError('real-time net_debt_to_ebitda not implemented')

    mqid = asset.get_marquee_id()
    metric = "Net Debt to EBITDA"

    _logger.debug('where assetId=%s, metric=%s, period=%s, periodDirection=%s', mqid, metric, period, period_direction)

    q = GsDataApi.build_market_data_query(
        [mqid],
        QueryType.FUNDAMENTAL_METRIC,
        where=FieldFilterMap(metric=metric, period=period.value, periodDirection=period_direction.value),
        source=source,
        real_time=real_time
    )

    q['queries'][0]['vendor'] = 'Goldman Sachs'
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return Series() if df.empty else df['fundamentalMetric']


@plot_measure((AssetClass.Equity,), None, [QueryType.FUNDAMENTAL_METRIC])
def price_to_book(asset: Asset, period: FundamentalMetricPeriod, period_direction: FundamentalMetricPeriodDirection,
                  *, source: str = None, real_time: bool = False) -> Series:
    """
    Price to Book of the single stock or the asset-weighted average value of a composite's underliers.

    1y forward: time-weighted average of one fiscal year (FY1) and two fiscal year (FY2) fwd-looking estimates.
    2y forward: time-weighted average of two fiscal year (FY2) and three fiscal year (FY3) fwd-looking estimates.
    3y forward: time-weighted average of three fiscal year (FY3) and four fiscal year (FY4) fwd-looking estimates.
    1y trailing: time-weighted average of latest reported fiscal year (FY0) data and one fiscal year (FY1) fwd-looking
    estimate.

    :param asset: asset object loaded from security master
    :param period: the relative fiscal period from now. e.g. 1y
    :param period_direction: whether the period is forward-looking or backward-looking e.g. forward
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: Price to Book
    """
    if real_time:
        raise NotImplementedError('real-time price_to_book not implemented')

    mqid = asset.get_marquee_id()
    metric = "Price to Book"

    _logger.debug('where assetId=%s, metric=%s, period=%s, periodDirection=%s', mqid, metric, period, period_direction)

    q = GsDataApi.build_market_data_query(
        [mqid],
        QueryType.FUNDAMENTAL_METRIC,
        where=FieldFilterMap(metric=metric, period=period.value, periodDirection=period_direction.value),
        source=source,
        real_time=real_time
    )

    q['queries'][0]['vendor'] = 'Goldman Sachs'
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return Series() if df.empty else df['fundamentalMetric']


@plot_measure((AssetClass.Equity,), None, [QueryType.FUNDAMENTAL_METRIC])
def price_to_cash(asset: Asset, period: FundamentalMetricPeriod, period_direction: FundamentalMetricPeriodDirection,
                  *, source: str = None, real_time: bool = False) -> Series:
    """
    Price to Cash of the single stock or the asset-weighted average value of a composite's underliers.

    1y forward: time-weighted average of one fiscal year (FY1) and two fiscal year (FY2) fwd-looking estimates.
    2y forward: time-weighted average of two fiscal year (FY2) and three fiscal year (FY3) fwd-looking estimates.
    3y forward: time-weighted average of three fiscal year (FY3) and four fiscal year (FY4) fwd-looking estimates.
    1y trailing: time-weighted average of latest reported fiscal year (FY0) data and one fiscal year (FY1) fwd-looking
    estimate.

    :param asset: asset object loaded from security master
    :param period: the relative fiscal period from now. e.g. 1y
    :param period_direction: whether the period is forward-looking or backward-looking e.g. forward
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: Price to Cash
    """
    if real_time:
        raise NotImplementedError('real-time price_to_cash not implemented')

    mqid = asset.get_marquee_id()
    metric = "Price to Cash"

    _logger.debug('where assetId=%s, metric=%s, period=%s, periodDirection=%s', mqid, metric, period, period_direction)

    q = GsDataApi.build_market_data_query(
        [mqid],
        QueryType.FUNDAMENTAL_METRIC,
        where=FieldFilterMap(metric=metric, period=period.value, periodDirection=period_direction.value),
        source=source,
        real_time=real_time
    )

    q['queries'][0]['vendor'] = 'Goldman Sachs'
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return Series() if df.empty else df['fundamentalMetric']


@plot_measure((AssetClass.Equity,), None, [QueryType.FUNDAMENTAL_METRIC])
def price_to_earnings(asset: Asset, period: FundamentalMetricPeriod, period_direction: FundamentalMetricPeriodDirection,
                      *, source: str = None, real_time: bool = False) -> Series:
    """
    Price to Earnings of the single stock or the asset-weighted average value of a composite's underliers.

    1y forward: time-weighted average of one fiscal year (FY1) and two fiscal year (FY2) fwd-looking estimates.
    2y forward: time-weighted average of two fiscal year (FY2) and three fiscal year (FY3) fwd-looking estimates.
    3y forward: time-weighted average of three fiscal year (FY3) and four fiscal year (FY4) fwd-looking estimates.
    1y trailing: time-weighted average of latest reported fiscal year (FY0) data and one fiscal year (FY1) fwd-looking
    estimate.

    :param asset: asset object loaded from security master
    :param period: the relative fiscal period from now. e.g. 1y
    :param period_direction: whether the period is forward-looking or backward-looking e.g. forward
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: Price to Earnings
    """
    if real_time:
        raise NotImplementedError('real-time price_to_earnings not implemented')

    mqid = asset.get_marquee_id()
    metric = "Price to Earnings"

    _logger.debug('where assetId=%s, metric=%s, period=%s, periodDirection=%s', mqid, metric, period, period_direction)

    q = GsDataApi.build_market_data_query(
        [mqid],
        QueryType.FUNDAMENTAL_METRIC,
        where=FieldFilterMap(metric=metric, period=period.value, periodDirection=period_direction.value),
        source=source,
        real_time=real_time
    )

    q['queries'][0]['vendor'] = 'Goldman Sachs'
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return Series() if df.empty else df['fundamentalMetric']


@plot_measure((AssetClass.Equity,), None, [QueryType.FUNDAMENTAL_METRIC])
def price_to_earnings_positive(asset: Asset,
                               period: FundamentalMetricPeriod,
                               period_direction: FundamentalMetricPeriodDirection,
                               *, source: str = None, real_time: bool = False) -> Series:
    """
    Price to Earnings Positive of the single stock or the asset-weighted average value of a composite's underliers.

    1y forward: time-weighted average of one fiscal year (FY1) and two fiscal year (FY2) fwd-looking estimates.
    2y forward: time-weighted average of two fiscal year (FY2) and three fiscal year (FY3) fwd-looking estimates.
    3y forward: time-weighted average of three fiscal year (FY3) and four fiscal year (FY4) fwd-looking estimates.
    1y trailing: time-weighted average of latest reported fiscal year (FY0) data and one fiscal year (FY1) fwd-looking
    estimate.

    :param asset: asset object loaded from security master
    :param period: the relative fiscal period from now. e.g. 1y
    :param period_direction: whether the period is forward-looking or backward-looking e.g. forward
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: Price to Earnings Positive
    """
    if real_time:
        raise NotImplementedError('real-time price_to_earnings_positive not implemented')

    mqid = asset.get_marquee_id()
    metric = "Price to Earnings Positive"

    _logger.debug('where assetId=%s, metric=%s, period=%s, periodDirection=%s', mqid, metric, period, period_direction)

    q = GsDataApi.build_market_data_query(
        [mqid],
        QueryType.FUNDAMENTAL_METRIC,
        where=FieldFilterMap(metric=metric, period=period.value, periodDirection=period_direction.value),
        source=source,
        real_time=real_time
    )

    q['queries'][0]['vendor'] = 'Goldman Sachs'
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return Series() if df.empty else df['fundamentalMetric']


@plot_measure((AssetClass.Equity,), None, [QueryType.FUNDAMENTAL_METRIC])
def price_to_sales(asset: Asset, period: FundamentalMetricPeriod, period_direction: FundamentalMetricPeriodDirection,
                   *, source: str = None, real_time: bool = False) -> Series:
    """
    Price to Sales of the single stock or the asset-weighted average value of a composite's underliers.

    1y forward: time-weighted average of one fiscal year (FY1) and two fiscal year (FY2) fwd-looking estimates.
    2y forward: time-weighted average of two fiscal year (FY2) and three fiscal year (FY3) fwd-looking estimates.
    3y forward: time-weighted average of three fiscal year (FY3) and four fiscal year (FY4) fwd-looking estimates.
    1y trailing: time-weighted average of latest reported fiscal year (FY0) data and one fiscal year (FY1) fwd-looking
    estimate.

    :param asset: asset object loaded from security master
    :param period: the relative fiscal period from now. e.g. 1y
    :param period_direction: whether the period is forward-looking or backward-looking e.g. forward
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: Price to Sales
    """
    if real_time:
        raise NotImplementedError('real-time price_to_sales not implemented')

    mqid = asset.get_marquee_id()
    metric = "Price to Sales"

    _logger.debug('where assetId=%s, metric=%s, period=%s, periodDirection=%s', mqid, metric, period, period_direction)

    q = GsDataApi.build_market_data_query(
        [mqid],
        QueryType.FUNDAMENTAL_METRIC,
        where=FieldFilterMap(metric=metric, period=period.value, periodDirection=period_direction.value),
        source=source,
        real_time=real_time
    )

    q['queries'][0]['vendor'] = 'Goldman Sachs'
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return Series() if df.empty else df['fundamentalMetric']


@plot_measure((AssetClass.Equity,), None, [QueryType.FUNDAMENTAL_METRIC])
def return_on_equity(asset: Asset, period: FundamentalMetricPeriod, period_direction: FundamentalMetricPeriodDirection,
                     *, source: str = None, real_time: bool = False) -> Series:
    """
    Return on Equity of the single stock or the asset-weighted average value of a composite's underliers.

    1y forward: time-weighted average of one fiscal year (FY1) and two fiscal year (FY2) fwd-looking estimates.
    2y forward: time-weighted average of two fiscal year (FY2) and three fiscal year (FY3) fwd-looking estimates.
    3y forward: time-weighted average of three fiscal year (FY3) and four fiscal year (FY4) fwd-looking estimates.
    1y trailing: time-weighted average of latest reported fiscal year (FY0) data and one fiscal year (FY1) fwd-looking
    estimate.

    :param asset: asset object loaded from security master
    :param period: the relative fiscal period from now. e.g. 1y
    :param period_direction: whether the period is forward-looking or backward-looking e.g. forward
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: Return on Equity
    """
    if real_time:
        raise NotImplementedError('real-time return_on_equity not implemented')

    mqid = asset.get_marquee_id()
    metric = "Return on Equity"

    _logger.debug('where assetId=%s, metric=%s, period=%s, periodDirection=%s', mqid, metric, period, period_direction)

    q = GsDataApi.build_market_data_query(
        [mqid],
        QueryType.FUNDAMENTAL_METRIC,
        where=FieldFilterMap(metric=metric, period=period.value, periodDirection=period_direction.value),
        source=source,
        real_time=real_time
    )

    q['queries'][0]['vendor'] = 'Goldman Sachs'
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return Series() if df.empty else df['fundamentalMetric']


@plot_measure((AssetClass.Equity,), None, [QueryType.FUNDAMENTAL_METRIC])
def sales_per_share(asset: Asset, period: FundamentalMetricPeriod, period_direction: FundamentalMetricPeriodDirection,
                    *, source: str = None, real_time: bool = False) -> Series:
    """
    Sales per Share of the single stock or the asset-weighted average value of a composite's underliers.

    1y forward: time-weighted average of one fiscal year (FY1) and two fiscal year (FY2) fwd-looking estimates.
    2y forward: time-weighted average of two fiscal year (FY2) and three fiscal year (FY3) fwd-looking estimates.
    3y forward: time-weighted average of three fiscal year (FY3) and four fiscal year (FY4) fwd-looking estimates.
    1y trailing: time-weighted average of latest reported fiscal year (FY0) data and one fiscal year (FY1) fwd-looking
    estimate.

    :param asset: asset object loaded from security master
    :param period: the relative fiscal period from now. e.g. 1y
    :param period_direction: whether the period is forward-looking or backward-looking e.g. forward
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: Sales per Share
    """
    if real_time:
        raise NotImplementedError('real-time sales_per_share not implemented')

    mqid = asset.get_marquee_id()
    metric = "Sales per Share"

    _logger.debug('where assetId=%s, metric=%s, period=%s, periodDirection=%s', mqid, metric, period, period_direction)

    q = GsDataApi.build_market_data_query(
        [mqid],
        QueryType.FUNDAMENTAL_METRIC,
        where=FieldFilterMap(metric=metric, period=period.value, periodDirection=period_direction.value),
        source=source,
        real_time=real_time
    )

    q['queries'][0]['vendor'] = 'Goldman Sachs'
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return Series() if df.empty else df['fundamentalMetric']
