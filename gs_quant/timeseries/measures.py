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
from enum import Enum, auto
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
from gs_quant.api.gs.data import QueryType
from gs_quant.data.core import DataContext
from gs_quant.datetime.gscalendar import GsCalendar
from gs_quant.datetime.point import relative_days_add
from gs_quant.markets.securities import Asset
from gs_quant.markets.securities import *
from gs_quant.target.common import AssetClass, FieldFilterMap, AssetType
from gs_quant.timeseries.helper import log_return, plot_measure
from gs_quant.errors import MqTypeError, MqValueError
from gs_quant.markets.securities import Asset, AssetIdentifier, SecurityMaster
from gs_quant.target.common import AssetClass, FieldFilterMap, AssetType, Currency
from gs_quant.timeseries.helper import log_return, plot_measure

GENERIC_DATE = Union[datetime.date, str]
TD_ONE = datetime.timedelta(days=1)
_logger = logging.getLogger(__name__)


class RateBenchmarkType(Enum):
    DEFAULT_BENCHMARK = auto()
    INFLATION_BENCHMARK = auto()


CURRENCY_TO_DEFAULT_RATE_BENCHMARK = {
    Currency.USD: 'USD-LIBOR-BBA',
    Currency.EUR: 'EUR-EURIBOR-TELERATE',
    Currency.GBP: 'GBP-LIBOR-BBA',
    Currency.JPY: 'JPY-LIBOR-BBA'
}

CURRENCY_TO_INFLATION_RATE_BENCHMARK = {
    Currency.GBP: 'CPI-UKRPI',
    Currency.EUR: 'CPI-CPXTEMU'
}

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


class VolReference(Enum):
    DELTA_CALL = 'delta_call'
    DELTA_PUT = 'delta_put'
    NORMALIZED = 'normalized'
    SPOT = 'spot'
    FORWARD = 'forward'


class VolSmileReference(Enum):
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


def _market_data_timed(q):
    start = time.perf_counter()
    df = GsDataApi.get_market_data(q)
    _logger.debug('market data query ran in %.3f ms', (time.perf_counter() - start) * 1000)
    return df


def _reverse_cross(cross_name):
    if '/' not in cross_name:
        raise MqValueError("Name of cross does not fit expected format")
    else:
        cross = cross_name.split('/')
        new_name = cross[0] + cross[1]
        new_asset = AssetIdentifier.BLOOMBERG_ID
        reverse_cross = SecurityMaster.get_asset(new_name, new_asset)
    return reverse_cross


@plot_measure((AssetClass.FX, AssetClass.Equity), None, [QueryType.IMPLIED_VOLATILITY])
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
    q = GsDataApi.build_market_data_query([asset.get_marquee_id()], QueryType.IMPLIED_VOLATILITY,
                                          where=where, source=source)
    _logger.debug('q %s', q)
    df = _market_data_timed(q)

    if df.empty:
        return pd.Series()

    curves = {k: v for k, v in df.groupby(column)}
    if len(curves) < 3:
        raise MqValueError('skew not available for given inputs')
    series = [curves[qs]['impliedVolatility'] for qs in q_strikes]
    return (series[0] - series[1]) / series[2]


@plot_measure((AssetClass.Equity, AssetClass.Commod, AssetClass.FX,), None, [QueryType.IMPLIED_VOLATILITY])
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
    if asset.asset_class == AssetClass.FX:
        # no ATM support yet
        if relative_strike == 50 and strike_reference in (VolReference.DELTA_CALL, VolReference.DELTA_PUT):
            delta_strike = 'DN'
        else:
            if strike_reference == VolReference.DELTA_CALL:
                delta_strike = f'{relative_strike}DC'
            elif strike_reference == VolReference.DELTA_PUT:
                delta_strike = f'{relative_strike}DP'
            elif strike_reference == VolReference.FORWARD:
                if relative_strike == 100:
                    delta_strike = 'ATMF'
                else:
                    raise MqValueError('Relative strike must be 100 for Forward strike reference')
            elif strike_reference == VolReference.SPOT:
                if relative_strike == 100:
                    delta_strike = 'ATMS'
                else:
                    raise MqValueError('Relative strike must be 100 for Spot strike reference')
            else:
                raise MqValueError('strikeReference: ' + strike_reference.value + ' not supported for FX')
        loc_string = 'NYC'
        _logger.debug('where tenor=%s, deltaStrike=%s, location=%s', tenor, delta_strike, loc_string)
        where = FieldFilterMap(tenor=tenor, deltaStrike=delta_strike, location=loc_string)
        q = GsDataApi.build_market_data_query([asset.get_marquee_id()], QueryType.IMPLIED_VOLATILITY,
                                              where=where, source=source, real_time=real_time)
        _logger.debug('q %s', q)
        df = _market_data_timed(q)
        if df.empty:
            reversed_cross = _reverse_cross(asset.name)
            q = GsDataApi.build_market_data_query([reversed_cross.get_marquee_id()], QueryType.IMPLIED_VOLATILITY,
                                                  where=where, source=source, real_time=real_time)
            _logger.debug('q %s', q)
            df = _market_data_timed(q)
    else:
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


def currency_converter_default_benchmark(asset_id: str) -> str:
    try:
        asset = SecurityMaster.get_asset(asset_id, AssetIdentifier.MARQUEE_ID)
        result = rate_benchmark_mqid(asset, RateBenchmarkType.DEFAULT_BENCHMARK)
    except TypeError:
        result = asset_id

    return result


def currency_converter_inflation_benchmark(asset_id: str) -> str:
    try:
        asset = SecurityMaster.get_asset(asset_id, AssetIdentifier.MARQUEE_ID)
        result = rate_benchmark_mqid(asset, RateBenchmarkType.INFLATION_BENCHMARK)
    except TypeError:
        result = asset_id

    return result


def rate_benchmark_mqid(asset: Asset, rate_benchmark_type: RateBenchmarkType):
    try:
        currency = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)
        currency = Currency(currency)
        if currency is None:
            return asset.get_marquee_id()
        rate_benchmark = CURRENCY_TO_DEFAULT_RATE_BENCHMARK[currency] \
            if rate_benchmark_type is RateBenchmarkType.DEFAULT_BENCHMARK \
            else CURRENCY_TO_INFLATION_RATE_BENCHMARK[currency]
        return GsAssetApi.map_identifiers(GsIdType.mdapi, GsIdType.id, [rate_benchmark])[rate_benchmark]
    except KeyError:
        logging.info(f'Unsupported currency ${currency}')
        raise asset.get_marquee_id()


@plot_measure((AssetClass.Cash,), (AssetType.Currency,), [QueryType.SWAP_RATE])
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
    :return: swap rate curve
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

    _logger.debug('where tenor=%s, floatingIndex=%s', tenor, floating_index)

    q = GsDataApi.build_market_data_query(
        [rate_mqid],
        QueryType.SWAP_RATE,
        where=FieldFilterMap(tenor=tenor),
        source=source,
        real_time=real_time
    )

    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return Series() if df.empty else df['swapRate']


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=currency_converter_default_benchmark, query_type=QueryType.SWAPTION_VOL)])
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

    currency = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)
    currency = Currency(currency)

    rate_benchmark = CURRENCY_TO_DEFAULT_RATE_BENCHMARK[currency]
    rate_benchmark_mqid = GsAssetApi.map_identifiers(GsIdType.mdapi, GsIdType.id, [rate_benchmark])[rate_benchmark]

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
              [MeasureDependency(id_provider=currency_converter_default_benchmark, query_type=QueryType.ATM_FWD_RATE)])
def swaption_atm_forward_rate(asset: Asset, expiration_tenor: str, termination_tenor: str, *, source: str = None,
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

    currency = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)
    currency = Currency(currency)

    rate_benchmark = CURRENCY_TO_DEFAULT_RATE_BENCHMARK[currency]
    rate_benchmark_mqid = GsAssetApi.map_identifiers(GsIdType.mdapi, GsIdType.id, [rate_benchmark])[rate_benchmark]

    _logger.debug('where expiry=%s, tenor=%s', expiration_tenor, termination_tenor)

    q = GsDataApi.build_market_data_query(
        [rate_benchmark_mqid],
        QueryType.ATM_FWD_RATE,
        where=FieldFilterMap(expriy=expiration_tenor, tenor=termination_tenor),
        source=source,
        real_time=real_time
    )

    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return Series() if df.empty else df['atmFwdRate']


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=currency_converter_default_benchmark, query_type=QueryType.MIDCURVE_VOL)])
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
    _logger.debug('where expiry=%s, forwardTenor=%s, tenor=%s, strike=%s', expiration_tenor, forward_tenor,
                  termination_tenor, relative_strike)

    q = GsDataApi.build_market_data_query(
        [rate_benchmark_mqid(asset, RateBenchmarkType.DEFAULT_BENCHMARK)],
        QueryType.MIDCURVE_VOL,
        where=FieldFilterMap(expriy=expiration_tenor, forward_tenor=forward_tenor, tenor=termination_tenor,
                             strike=relative_strike),
        source=source,
        real_time=real_time
    )

    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return Series() if df.empty else df['midcurveVol']


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=currency_converter_default_benchmark, query_type=QueryType.CAP_FLOOR_VOL)])
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

    currency = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)
    currency = Currency(currency)

    rate_benchmark = CURRENCY_TO_DEFAULT_RATE_BENCHMARK[currency]
    rate_benchmark_mqid = GsAssetApi.map_identifiers(GsIdType.mdapi, GsIdType.id, [rate_benchmark])[rate_benchmark]

    _logger.debug('where expiry=%s, strike=%s', expiration_tenor, relative_strike)

    q = GsDataApi.build_market_data_query(
        [rate_benchmark_mqid],
        QueryType.CAP_FLOOR_VOL,
        where=FieldFilterMap(expriy=expiration_tenor, strike=relative_strike),
        source=source,
        real_time=real_time
    )

    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return Series() if df.empty else df['capFloorVol']


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=currency_converter_default_benchmark,
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

    currency = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)
    currency = Currency(currency)

    rate_benchmark = CURRENCY_TO_DEFAULT_RATE_BENCHMARK[currency]
    rate_benchmark_mqid = GsAssetApi.map_identifiers(GsIdType.mdapi, GsIdType.id, [rate_benchmark])[rate_benchmark]

    _logger.debug('where expiry=%s, longTenor=%s, shortTenor=%s, strike=%s', long_tenor, short_tenor, expiration_tenor,
                  relative_strike)

    q = GsDataApi.build_market_data_query(
        [rate_benchmark_mqid],
        QueryType.SPREAD_OPTION_VOL,
        where=FieldFilterMap(expriy=expiration_tenor, longTenor=long_tenor, shortTenor=short_tenor,
                             strike=relative_strike),
        source=source,
        real_time=real_time
    )

    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return Series() if df.empty else df['spreadOptionVol']


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=currency_converter_inflation_benchmark,
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

    currency = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)
    currency = Currency(currency)

    rate_benchmark = CURRENCY_TO_INFLATION_RATE_BENCHMARK[currency]
    rate_benchmark_mqid = GsAssetApi.map_identifiers(GsIdType.mdapi, GsIdType.id, [rate_benchmark])[rate_benchmark]

    _logger.debug('where tenor=%s', termination_tenor)

    q = GsDataApi.build_market_data_query(
        [rate_benchmark_mqid],
        QueryType.INFLATION_SWAP_RATE,
        where=FieldFilterMap(tenor=termination_tenor),
        source=source,
        real_time=real_time
    )

    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return Series() if df.empty else df['inflationSwapRate']


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
def vol_smile(asset: Asset, tenor: str, strike_reference: VolSmileReference, pricing_date: Optional[GENERIC_DATE] = None,
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


@plot_measure((AssetClass.Commod,), None, [QueryType.PRICE])
def bucketize_price(asset: Asset, price_method: str, price_component: str, bucket: str = '7x24',
                    granularity: str = 'daily', *, source: str = None, real_time: bool = True) -> pd.Series:
    """'
    Bucketized Elec Historical Clears

    :param asset: asset object loaded from security master
    :param price_method: price method between LMP and MCP: Default value = LMP
    :param price_component: price type among totalPrice, energy, loss and congestion: Default value = totalPrice
    :param bucket: bucket type among '7x24', 'peak', 'offpeak', '2x16h' and '7x8': Default value = 7x24
    :param granularity: daily or monthly: default value = daily
    :param source: name of function caller: default source = None
    :param real_time: whether to retrieve intraday data instead of EOD: default value = True
    :return: Bucketized Elec Historical Clears
    """

    # create granularity indicator
    if granularity.lower() in ['daily', 'd']:
        granularity = 'D'
    elif granularity.lower() in ['monthly', 'm']:
        granularity = 'M'
    else:
        raise ValueError('Invalid granularity: ' + granularity + '. Expected Value: daily or monthly.')

    start_date, end_date = DataContext.current.start_date, DataContext.current.end_date
    where = FieldFilterMap(priceMethod=price_method, priceComponent=price_component)

    with DataContext(start_date, end_date + datetime.timedelta(days=2)):
        q = GsDataApi.build_market_data_query([asset.get_marquee_id()], QueryType.PRICE, where=where, source=source,
                                              real_time=True)
        df = _market_data_timed(q)
        _logger.debug('q %s', q)

    # TODO: get timezone info from Asset
    # default frequency definition
    df = df.tz_convert('US/Eastern')
    peak_start = 7
    peak_end = 23
    weekends = [5, 6]
    bbid = Asset.get_identifier(asset, AssetIdentifier.BLOOMBERG_ID)
    if bbid.split(" ")[0] in ['MISO', 'CAISO', 'ERCOT', 'SPP']:
        df = df.tz_convert('US/Central')
        peak_start = 6
        peak_end = 22
    if bbid.split(" ")[0] == 'CAISO':
        df = df.tz_convert('US/Pacific')
        weekends = [6]

    start_time, end_time = pd.to_datetime(start_date), pd.to_datetime(end_date) + datetime.timedelta(hours=23)
    df['month'] = df.index.month
    df['date'] = df.index.date
    df['day'] = df.index.dayofweek
    df['hour'] = df.index.hour
    holidays = NercCalendar().holidays(start=start_date, end=end_date).date

    # checking missing data points
    ref_hour_range = pd.date_range(start_time, end_time, freq='1h', tz='US/Eastern')
    missing_hours = ref_hour_range[~ref_hour_range.isin(df.index)]
    missing_dates = np.unique(missing_hours.date)
    missing_months = np.unique(missing_hours.month)

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
                    (~df['date'].isin(holidays) & ~df['day'].isin(weekends) & ((df['hour'] < peak_start)
                                                                               | (df['hour'] > peak_end - 1)))]
    # peak: 7am to 11pm on weekdays
    elif bucket.lower() == 'peak':
        df = df.loc[(~df['date'].isin(holidays)) & (~df['day'].isin(weekends)) & (df['hour'] > peak_start - 1)
                    & (df['hour'] < peak_end)]
    # 7x8: 11pm to 7am
    elif bucket.lower() == '7x8':
        df = df.loc[(df['hour'] < peak_start) | (df['hour'] > peak_end - 1)]
    # 2x16h: weekends & holidays
    elif bucket.lower() == '2x16h':
        df = df.loc[((df['date'].isin(holidays)) | df['day'].isin(weekends)) & ((df['hour'] > peak_start - 1)
                                                                                & (df['hour'] < peak_end))]
    else:
        raise ValueError('Invalid bucket: ' + bucket + '. Expected Value: peak, offpeak, 7x24, 7x8, 2x16h.')

    df = df['price'].resample(granularity).mean()
    df.index = df.index.date
    df = df.loc[start_date: end_date]
    return df
