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

import calendar
import datetime
import logging
import re
import time
from collections import namedtuple
from enum import auto
from numbers import Real

import cachetools.func
import inflection
import numpy as np
import pandas as pd
from dateutil import tz
from dateutil.relativedelta import relativedelta
from pandas import Series
from pandas.tseries.holiday import Holiday, AbstractHolidayCalendar, USMemorialDay, USLaborDay, USThanksgivingDay, \
    sunday_to_monday

from gs_quant.api.gs.assets import GsIdType
from gs_quant.api.gs.data import GsDataApi
from gs_quant.api.gs.data import QueryType
from gs_quant.data import Dataset
from gs_quant.data.core import DataContext
from gs_quant.data.fields import Fields
from gs_quant.datetime.gscalendar import GsCalendar
from gs_quant.datetime.point import relative_date_add
from gs_quant.errors import MqTypeError, MqValueError
from gs_quant.markets.securities import *
from gs_quant.markets.securities import Asset, AssetIdentifier, SecurityMaster, AssetType as SecAssetType
from gs_quant.target.common import AssetClass, AssetType
from gs_quant.timeseries import volatility, Window, Returns, sqrt
from gs_quant.timeseries.helper import log_return, plot_measure, _to_offset

GENERIC_DATE = Union[datetime.date, str]
ASSET_SPEC = Union[Asset, str]
TD_ONE = datetime.timedelta(days=1)
CENTRAL_BANK_WATCH_START_DATE = datetime.date(2016, 1, 1)

_logger = logging.getLogger(__name__)

MeasureDependency: namedtuple = namedtuple("MeasureDependency", ["id_provider", "query_type"])


class ExtendedSeries(Series):
    _internal_names = Series._internal_names + ['dataset_ids']
    _internal_names_set = set(_internal_names)

    @property
    def _constructor(self):
        return ExtendedSeries


# TODO: get NERC Calendar from SecDB
class NercCalendar(AbstractHolidayCalendar):
    rules = [
        Holiday('New Years Day', month=1, day=1, observance=sunday_to_monday),
        USMemorialDay,
        Holiday('July 4th', month=7, day=4, observance=sunday_to_monday),
        USLaborDay,
        USThanksgivingDay,
        Holiday('Christmas', month=12, day=25, observance=sunday_to_monday)
    ]


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


class FxForecastHorizon(Enum):
    THREE_MONTH = '3m'
    SIX_MONTH = '6m'
    TWELVE_MONTH = '12m'
    EOY1 = 'EOY1'
    EOY2 = 'EOY2'
    EOY3 = 'EOY3'
    EOY4 = 'EOY4'


class BenchmarkType(Enum):
    LIBOR = 'LIBOR'
    EURIBOR = 'EURIBOR'
    EUROSTR = 'EUROSTR'
    STIBOR = 'STIBOR'
    OIS = 'OIS'
    CDKSDA = 'CDKSDA'
    SOFR = 'SOFR'
    SARON = 'SARON'
    EONIA = 'EONIA'
    SONIA = 'SONIA'
    TONA = 'TONA'
    Fed_Funds = 'Fed_Funds'
    NIBOR = 'NIBOR'
    CIBOR = 'CIBOR'
    BBR = 'BBR'
    BA = 'BA'
    KSDA = 'KSDA'
    REPO = 'REPO'
    SOR = 'SOR'
    HIBOR = 'HIBOR'
    MIBOR = 'MIBOR'
    CDOR = 'CDOR'


class FundamentalMetricPeriodDirection(Enum):
    FORWARD = 'forward'
    TRAILING = 'trailing'


class RatesConversionType(Enum):
    DEFAULT_BENCHMARK_RATE = auto()
    DEFAULT_SWAP_RATE_ASSET = auto()
    INFLATION_BENCHMARK_RATE = auto()
    CROSS_CURRENCY_BASIS = auto()
    OIS_BENCHMARK_RATE = auto()


class MeetingType(Enum):
    MEETING_FORWARD = 'Meeting Forward'
    EOY_FORWARD = 'EOY Forward'
    SPOT = 'Spot'


class EsgMetric(Enum):
    ENVIRONMENTAL_SOCIAL_NUMERIC = 'es_numeric'
    ENVIRONMENTAL_SOCIAL_POLICY = 'es_policy'
    ENVIRONMENTAL_SOCIAL_AGGREGATE = 'es'
    GOVERNANCE_AGGREGATE = 'g'
    ENVIRONMENTAL_SOCIAL_DISCLOSURE = 'es_disclosure_percentage'
    ENVIRONMENTAL_SOCIAL_MOMENTUM = 'es_momentum'
    GOVERNANCE_REGIONAL = 'g_regional'


class EsgValueUnit(Enum):
    PERCENTILE = 'percentile'
    SCORE = 'score'


class SwaptionTenorType(Enum):
    OPTION_EXPIRY = 'option_expiry'
    SWAP_MATURITY = 'swap_maturity'


class EquilibriumExchangeRateMetric(Enum):
    GSDEER = 'gsdeer'
    GSFEER = 'gsfeer'


class _FactorProfileMetric(Enum):
    GROWTH_SCORE = 'growthScore'
    FINANCIAL_RETURNS_SCORE = 'financialReturnsScore'
    MULTIPLE_SCORE = 'multipleScore'
    INTEGRATED_SCORE = 'integratedScore'


class _CommoditiesForecastType(Enum):
    SPOT = 'spot'
    SPOT_RETURN = 'spotReturn'
    ROLL_RETURN = 'rollReturn'
    TOTAL_RETURN = 'totalReturn'


class _CommoditiesForecastPeriod(Enum):
    THREE_MONTH = '3m'
    SIX_MONTH = '6m'
    TWELVE_MONTH = '12m'


class _RatingMetric(Enum):
    RATING = 'rating'
    CONVICTION_LIST = 'convictionList'


ESG_METRIC_TO_QUERY_TYPE = {
    "esNumericScore": QueryType.ES_NUMERIC_SCORE,
    "esNumericPercentile": QueryType.ES_NUMERIC_PERCENTILE,
    "esPolicyScore": QueryType.ES_POLICY_SCORE,
    "esPolicyPercentile": QueryType.ES_POLICY_PERCENTILE,
    "esScore": QueryType.ES_SCORE,
    "esPercentile": QueryType.ES_PERCENTILE,
    "gScore": QueryType.G_SCORE,
    "gPercentile": QueryType.G_PERCENTILE,
    "esMomentumScore": QueryType.ES_MOMENTUM_SCORE,
    "esMomentumPercentile": QueryType.ES_MOMENTUM_PERCENTILE,
    "gRegionalScore": QueryType.G_REGIONAL_SCORE,
    "gRegionalPercentile": QueryType.G_REGIONAL_PERCENTILE,
    "esDisclosurePercentage": QueryType.ES_DISCLOSURE_PERCENTAGE
}

CURRENCY_TO_OIS_RATE_BENCHMARK = {
    'AUD': 'AUD OIS',
    'USD': 'USD OIS',
    'EUR': 'EUR OIS',
    'GBP': 'GBP OIS',
    'JPY': 'JPY OIS',
    'CAD': 'CAD OIS',
    'NOK': 'NOK OIS',
    'NZD': 'NZD OIS',
    'SEK': 'SEK OIS'
}

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


_FACTOR_PROFILE_METRIC_TO_QUERY_TYPE = {
    'growthScore': QueryType.GROWTH_SCORE,
    'financialReturnsScore': QueryType.FINANCIAL_RETURNS_SCORE,
    'multipleScore': QueryType.MULTIPLE_SCORE,
    'integratedScore': QueryType.INTEGRATED_SCORE
}


_RATING_METRIC_TO_QUERY_TYPE = {
    'rating': QueryType.RATING,
    'convictionList': QueryType.CONVICTION_LIST
}


_COMMOD_CONTRACT_MONTH_CODES = "FGHJKMNQUVXZ"
_COMMOD_CONTRACT_MONTH_CODES_DICT = {k: v for k, v in enumerate(_COMMOD_CONTRACT_MONTH_CODES)}


def _asset_from_spec(asset_spec: ASSET_SPEC) -> Asset:
    return asset_spec if isinstance(asset_spec, Asset) else SecurityMaster.get_asset(asset_spec,
                                                                                     AssetIdentifier.MARQUEE_ID)


def cross_stored_direction_for_fx_vol(asset_spec: ASSET_SPEC) -> str:
    asset = _asset_from_spec(asset_spec)
    asset_id = asset.get_marquee_id()
    result_id = asset_id
    try:
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


def cross_to_usd_based_cross(asset_spec: ASSET_SPEC) -> str:
    asset = _asset_from_spec(asset_spec)
    asset_id = asset.get_marquee_id()
    result_id = asset_id
    try:
        if asset.asset_class is AssetClass.FX:
            bbid = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)
            if bbid is not None and not str.startswith(bbid, "USD"):
                cross = bbid[3:] + bbid[:3]
                cross_asset = SecurityMaster.get_asset(cross, AssetIdentifier.BLOOMBERG_ID)
                result_id = cross_asset.get_marquee_id()
    except TypeError:
        result_id = asset_id
    return result_id


def currency_to_default_benchmark_rate(asset_spec: ASSET_SPEC) -> str:
    asset = _asset_from_spec(asset_spec)
    asset_id = asset.get_marquee_id()
    try:
        result = convert_asset_for_rates_data_set(asset, RatesConversionType.DEFAULT_BENCHMARK_RATE)
    except TypeError:
        result = asset_id
    return result


def currency_to_default_swap_rate_asset(asset_spec: ASSET_SPEC) -> str:
    asset = _asset_from_spec(asset_spec)
    return convert_asset_for_rates_data_set(asset, RatesConversionType.DEFAULT_SWAP_RATE_ASSET)


def currency_to_inflation_benchmark_rate(asset_spec: ASSET_SPEC) -> str:
    asset = _asset_from_spec(asset_spec)
    try:
        result = convert_asset_for_rates_data_set(asset, RatesConversionType.INFLATION_BENCHMARK_RATE)
    except TypeError:
        result = asset.get_marquee_id()
    return result


def cross_to_basis(asset_spec: ASSET_SPEC) -> str:
    asset = _asset_from_spec(asset_spec)
    try:
        result = convert_asset_for_rates_data_set(asset, RatesConversionType.CROSS_CURRENCY_BASIS)
    except TypeError:
        result = asset.get_marquee_id()
    return result


def convert_asset_for_rates_data_set(from_asset: Asset, c_type: RatesConversionType) -> str:
    try:
        bbid = from_asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)
        if bbid is None:
            return from_asset.get_marquee_id()

        if c_type is RatesConversionType.DEFAULT_BENCHMARK_RATE:
            to_asset = CURRENCY_TO_DEFAULT_RATE_BENCHMARK[bbid]
        elif c_type is RatesConversionType.DEFAULT_SWAP_RATE_ASSET:
            to_asset = (bbid + '-3m') if bbid == "USD" else (bbid + '-6m') if bbid in ['GBP', 'EUR', 'CHF', 'SEK'] \
                else bbid
        elif c_type is RatesConversionType.INFLATION_BENCHMARK_RATE:
            to_asset = CURRENCY_TO_INFLATION_RATE_BENCHMARK[bbid]
        elif c_type is RatesConversionType.OIS_BENCHMARK_RATE:
            to_asset = CURRENCY_TO_OIS_RATE_BENCHMARK[bbid]
        else:
            to_asset = CROSS_TO_CROSS_CURRENCY_BASIS[bbid]

        return GsAssetApi.map_identifiers(GsIdType.mdapi, GsIdType.id, [to_asset])[to_asset]

    except KeyError:
        logging.info('Unsupported currency or cross')
        return from_asset.get_marquee_id()


def _get_custom_bd(exchange):
    from pandas.tseries.offsets import CustomBusinessDay
    calendar = GsCalendar.get(exchange).business_day_calendar()
    return CustomBusinessDay(calendar=calendar)


def parse_meeting_date(meeting_str: str = '2019-01-01'):
    if not isinstance(meeting_str, str):
        return ''
    elif meeting_str == '':
        return ''

    try:
        year, month, day = meeting_str.split('-')
        return dt.date(int(year), int(month), int(day))
    except ValueError:
        return ''


@log_return(_logger, 'trying pricing dates')
def _range_from_pricing_date(exchange, pricing_date: Optional[GENERIC_DATE] = None, buffer: int = 0):
    if isinstance(pricing_date, datetime.date):
        return pricing_date, pricing_date

    today = pd.Timestamp.today().normalize()
    bd = _get_custom_bd(exchange)
    if pricing_date is None:
        t1 = today - bd
        return t1 - (buffer * bd), t1

    assert isinstance(pricing_date, str)
    matcher = re.fullmatch('(\\d+)b', pricing_date)
    if matcher:
        start = end = today - bd * int(matcher.group(1))
    else:
        end = today - datetime.timedelta(days=relative_date_add(pricing_date, True))
        start = end - bd
    return start, end


def _market_data_timed(q):
    start = time.perf_counter()
    df = GsDataApi.get_market_data(q)
    _logger.debug('market data query ran in %.3f ms', (time.perf_counter() - start) * 1000)
    return df


def _extract_series_from_df(df: pd.DataFrame, query_type: QueryType):
    col_name = query_type.value.replace(' ', '')
    col_name = col_name[0].lower() + col_name[1:]
    series = ExtendedSeries() if df.empty else ExtendedSeries(df[col_name])
    series.dataset_ids = getattr(df, 'dataset_ids', ())
    return series


@plot_measure((AssetClass.FX, AssetClass.Equity, AssetClass.Commod), None, [MeasureDependency(
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

    asset_id = asset.get_marquee_id()
    kwargs = {}

    if asset.asset_class == AssetClass.FX:
        asset_id = cross_stored_direction_for_fx_vol(asset_id)
        if strike_reference == SkewReference.DELTA:
            q_strikes = [0 - distance, distance, 0]
        else:
            raise MqValueError('strike_reference has to be delta to get skew for FX options')
    else:
        assert asset.asset_class in (AssetClass.Equity, AssetClass.Commod)
        if strike_reference in (SkewReference.DELTA, None):
            b = 50
        elif strike_reference == SkewReference.NORMALIZED:
            b = 0
        else:
            b = 100

        if strike_reference in (SkewReference.DELTA, None):
            # using delta call strikes so X DP is represented as (100 - X) DC for Equity options
            q_strikes = [100 - distance, distance, b]
        else:
            q_strikes = [b - distance, b + distance, b]

        if not strike_reference:
            raise MqTypeError('strike reference required for equities')
        if strike_reference != SkewReference.NORMALIZED:
            q_strikes = [x / 100 for x in q_strikes]

    kwargs['strikeReference'] = strike_reference.value
    column = 'relativeStrike'
    kwargs[column] = q_strikes
    _logger.debug('where tenor=%s and %s', tenor, kwargs)
    where = dict(tenor=tenor, **kwargs)
    q = GsDataApi.build_market_data_query([asset_id], QueryType.IMPLIED_VOLATILITY, where=where, source=source)
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    dataset_ids = getattr(df, 'dataset_ids', ())

    if df.empty:
        series = ExtendedSeries()
    else:
        curves = {k: v for k, v in df.groupby(column)}
        if len(curves) < 3:
            raise MqValueError('skew not available for given inputs')
        series = [curves[qs]['impliedVolatility'] for qs in q_strikes]
        series = ExtendedSeries((series[0] - series[1]) / series[2])
    series.dataset_ids = dataset_ids
    return series


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
        where=dict(
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
    return _extract_series_from_df(df, QueryType.IMPLIED_VOLATILITY_BY_DELTA_STRIKE)


@plot_measure((AssetClass.Equity, AssetClass.Commod, AssetClass.FX,), None,
              [MeasureDependency(id_provider=cross_stored_direction_for_fx_vol,
                                 query_type=QueryType.IMPLIED_VOLATILITY)])
def implied_volatility(asset: Asset, tenor: str, strike_reference: VolReference = None,
                       relative_strike: Real = None, *, source: str = None, real_time: bool = False) -> Series:
    """
    Volatility of an asset implied by observations of market prices.

    :param asset: asset object loaded from security master
    :param tenor: relative date representation of expiration date e.g. 1m
            or absolute calendar strips e.g. 'Cal20', 'F20-G20'
    :param strike_reference: reference for strike level
    :param relative_strike: strike relative to reference
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: implied volatility curve
    """

    if asset.asset_class == AssetClass.Commod and asset.get_type() not in (SecAssetType.ETF, SecAssetType.STOCK):
        return _weighted_average_valuation_curve_for_calendar_strip(asset, tenor,
                                                                    QueryType.IMPLIED_VOLATILITY, "impliedVolatility")

    if asset.asset_class == AssetClass.FX:
        asset_id = cross_stored_direction_for_fx_vol(asset.get_marquee_id())
        ref_string, relative_strike = _preprocess_implied_vol_strikes_fx(strike_reference, relative_strike)

    else:
        asset_id = asset.get_marquee_id()
        ref_string, relative_strike = _preprocess_implied_vol_strikes_eq(strike_reference, relative_strike)

    _logger.debug('where tenor=%s, strikeReference=%s, relativeStrike=%s', tenor, ref_string, relative_strike)
    where = dict(tenor=tenor, strikeReference=ref_string, relativeStrike=relative_strike)
    q = GsDataApi.build_market_data_query([asset_id], QueryType.IMPLIED_VOLATILITY, where=where, source=source,
                                          real_time=real_time)
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return _extract_series_from_df(df, QueryType.IMPLIED_VOLATILITY)


def _preprocess_implied_vol_strikes_fx(strike_reference: VolReference = None, relative_strike: Real = None):
    if relative_strike is None and strike_reference != VolReference.DELTA_NEUTRAL:
        raise MqValueError('Relative strike must be provided if your strike reference is not delta_neutral')

    if strike_reference in (VolReference.FORWARD, VolReference.SPOT) and relative_strike != 100:
        raise MqValueError('Relative strike must be 100 for Spot or Forward strike reference')
    if strike_reference not in VolReference or strike_reference == VolReference.NORMALIZED:
        raise MqValueError('strikeReference: ' + strike_reference.value + ' not supported for FX')
    if strike_reference == VolReference.DELTA_NEUTRAL:
        if relative_strike is None:
            relative_strike = 0
        elif relative_strike != 0:
            raise MqValueError('relative_strike must be 0 for delta_neutral')

    if strike_reference == VolReference.DELTA_PUT:
        relative_strike *= -1

    ref_string = "delta" if strike_reference in (VolReference.DELTA_CALL, VolReference.DELTA_PUT,
                                                 VolReference.DELTA_NEUTRAL) else strike_reference.value
    return ref_string, relative_strike


def _preprocess_implied_vol_strikes_eq(strike_reference: VolReference = None, relative_strike: Real = None):
    if relative_strike is None and strike_reference != VolReference.DELTA_NEUTRAL:
        raise MqValueError('Relative strike must be provided if your strike reference is not delta_neutral')

    if strike_reference == VolReference.DELTA_NEUTRAL:
        raise MqValueError('delta_neutral strike reference is not supported for equities.')

    if strike_reference == VolReference.DELTA_PUT:
        relative_strike = abs(100 - relative_strike)
    relative_strike = relative_strike if strike_reference == VolReference.NORMALIZED else relative_strike / 100

    ref_string = "delta" if strike_reference in (VolReference.DELTA_CALL, VolReference.DELTA_PUT,
                                                 VolReference.DELTA_NEUTRAL) else strike_reference.value

    return ref_string, relative_strike


@plot_measure((AssetClass.Equity,), (AssetType.Index, AssetType.ETF,), [QueryType.IMPLIED_CORRELATION])
def implied_correlation(asset: Asset, tenor: str, strike_reference: EdrDataReference, relative_strike: Real,
                        top_n_of_index: Optional[int] = None, composition_date: Optional[GENERIC_DATE] = None, *,
                        source: str = None, real_time: bool = False) -> Series:
    """
    Correlation of an asset implied by observations of market prices.

    :param asset: asset object loaded from security master
    :param tenor: relative date representation of expiration date e.g. 1m
    :param strike_reference: reference for strike level
    :param relative_strike: strike relative to reference
    :param top_n_of_index: the number of top constituents to take into account
    :param composition_date: YYYY-MM-DD or relative days before today e.g. 1d, 1m, 1y; defaults to most recent date
        available
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: implied correlation curve
    """
    if real_time:
        raise NotImplementedError('realtime implied_correlation not implemented')

    if top_n_of_index is None and composition_date is not None:
        raise MqValueError('specify top_n_of_index to get the implied correlation of top constituents')

    if top_n_of_index is not None and top_n_of_index > 100:
        raise MqValueError('maximum number of constituents exceeded while using top_n_of_index')

    if strike_reference == EdrDataReference.DELTA_PUT:
        relative_strike = abs(100 - relative_strike)

    relative_strike = relative_strike / 100

    delta_types = (EdrDataReference.DELTA_CALL, EdrDataReference.DELTA_PUT)
    strike_ref = "delta" if strike_reference in delta_types else strike_reference.value

    _logger.debug('where tenor=%s, strikeReference=%s, relativeStrike=%s', tenor, strike_ref, relative_strike)

    mqid = asset.get_marquee_id()
    where = dict(tenor=tenor, strikeReference=strike_ref, relativeStrike=relative_strike)

    if top_n_of_index is None:
        q = GsDataApi.build_market_data_query([mqid], QueryType.IMPLIED_CORRELATION, where=where,
                                              source=source, real_time=real_time)
        _logger.debug('q %s', q)
        df = _market_data_timed(q)
        return _extract_series_from_df(df, QueryType.IMPLIED_CORRELATION)

    # results for top n
    constituents = _get_index_constituent_weights(asset, top_n_of_index, composition_date)
    query = GsDataApi.build_market_data_query(
        constituents.index.to_list() + [mqid],
        QueryType.IMPLIED_VOLATILITY,
        where=where,
        source=source,
        real_time=real_time
    )
    df = _market_data_timed(query)
    df = df[['assetId', 'impliedVolatility']]
    full_index = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')

    all_groups = []
    for name, group in df.groupby('assetId'):
        g = group.reindex(full_index)
        g['assetId'] = name
        g['impliedVolatility'].interpolate(inplace=True)
        all_groups.append(g)
    df = pd.concat(all_groups)

    df['impliedVolatility'] /= 100
    match = df['assetId'] == mqid
    df_asset = df.loc[match]
    df_rest = df.loc[~match]

    def calculate_vol(group):
        vols = group.set_index('assetId')['impliedVolatility']
        weights = constituents.reindex(vols.index.to_list())['netWeight']
        total_weight = sum(weights)
        parts = [vol * weight / total_weight for vol, weight in zip(vols, weights)]
        return pd.Series([sum(parts), sum(map(lambda x: pow(x, 2), parts))], index=['first', 'second'])

    inter = df_rest.groupby(df_rest.index).apply(calculate_vol)
    values = (pow(df_asset['impliedVolatility'], 2) - inter['second']) / (pow(inter['first'], 2) - inter['second'])
    series = ExtendedSeries(values * 100)
    series.dataset_ids = getattr(df, 'dataset_ids', ())
    return series


@plot_measure((AssetClass.Equity,), (AssetType.Index, AssetType.ETF,), [QueryType.AVERAGE_IMPLIED_VOLATILITY,
                                                                        QueryType.IMPLIED_VOLATILITY])
def average_implied_volatility(asset: Asset, tenor: str, strike_reference: EdrDataReference, relative_strike: Real,
                               top_n_of_index: Optional[int] = None, composition_date: Optional[GENERIC_DATE] = None, *,
                               source: str = None, real_time: bool = False) -> Series:
    """
    Historical weighted average implied volatility of the top constituents of an equity index. If top_n_of_index and
    composition_date are not provided, the average is of all constituents based on the weights at each evaluation date

    :param asset: asset object loaded from security master
    :param tenor: relative date representation of expiration date e.g. 1m
    :param strike_reference: reference for strike level
    :param relative_strike: strike relative to reference
    :param top_n_of_index: the number of top constituents to take into account
    :param composition_date: YYYY-MM-DD or relative days before today e.g. 1d, 1m, 1y; defaults to the most recent date
        available
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: average implied volatility curve
    """
    if real_time:
        raise NotImplementedError('realtime average_implied_volatility not implemented')

    if top_n_of_index is None and composition_date is not None:
        raise MqValueError('Specify top_n_of_index to get the average implied volatility of top constituents')

    if top_n_of_index is not None and top_n_of_index > 100:
        raise NotImplementedError('Maximum number of constituents exceeded. Do not use top_n_of_index to calculate on '
                                  'the full list')

    if top_n_of_index is not None:
        constituents = _get_index_constituent_weights(asset, top_n_of_index, composition_date)

        ref_string, relative_strike = _preprocess_implied_vol_strikes_eq(VolReference(strike_reference.value),
                                                                         relative_strike)

        _logger.debug('where tenor=%s, strikeReference=%s, relativeStrike=%s', tenor, ref_string, relative_strike)
        where = dict(tenor=tenor, strikeReference=ref_string, relativeStrike=relative_strike)
        query = GsDataApi.build_market_data_query(
            constituents.index.to_list(),
            QueryType.IMPLIED_VOLATILITY,
            where=where,
            source=source,
            real_time=real_time
        )
        df = _market_data_timed(query)

        def calculate_avg_vol(group):
            vols = group.set_index('assetId')['impliedVolatility']
            weights = constituents.reindex(vols.index.to_list())['netWeight']
            total_weight = sum(weights)
            return sum([vol * weight / total_weight for vol, weight in zip(vols, weights)])

        average_vol = df.groupby(df.index).apply(calculate_avg_vol)

        series = ExtendedSeries(average_vol, name='averageImpliedVolatility')
        series.dataset_ids = getattr(df, 'dataset_ids', ())
        return series

    if strike_reference == EdrDataReference.DELTA_PUT:
        relative_strike = abs(100 - relative_strike)

    relative_strike = relative_strike / 100

    delta_types = (EdrDataReference.DELTA_CALL, EdrDataReference.DELTA_PUT)
    strike_ref = "delta" if strike_reference in delta_types else strike_reference.value

    _logger.debug('where tenor=%s, strikeReference=%s, relativeStrike=%s', tenor, strike_ref, relative_strike)

    mqid = asset.get_marquee_id()
    where = dict(tenor=tenor, strikeReference=strike_ref, relativeStrike=relative_strike)
    q = GsDataApi.build_market_data_query([mqid], QueryType.AVERAGE_IMPLIED_VOLATILITY,
                                          where=where, source=source, real_time=real_time)

    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return _extract_series_from_df(df, QueryType.AVERAGE_IMPLIED_VOLATILITY)


@plot_measure((AssetClass.Equity,), (AssetType.Index, AssetType.ETF,), [QueryType.AVERAGE_IMPLIED_VARIANCE])
def average_implied_variance(asset: Asset, tenor: str, strike_reference: EdrDataReference, relative_strike: Real, *,
                             source: str = None, real_time: bool = False) -> Series:
    """
    Historical weighted average implied variance for the underlying assets of an equity index.

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
    where = dict(tenor=tenor, strikeReference=strike_ref, relativeStrike=relative_strike)
    q = GsDataApi.build_market_data_query([mqid], QueryType.AVERAGE_IMPLIED_VARIANCE, where=where, source=source,
                                          real_time=real_time)

    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return _extract_series_from_df(df, QueryType.AVERAGE_IMPLIED_VARIANCE)


@plot_measure((AssetClass.Equity,), (AssetType.Index, AssetType.ETF,), [QueryType.AVERAGE_REALIZED_VOLATILITY,
                                                                        QueryType.SPOT])
def average_realized_volatility(asset: Asset, tenor: str, returns_type: Returns = Returns.SIMPLE,
                                top_n_of_index: int = None, composition_date: Optional[GENERIC_DATE] = None,
                                *, source: str = None, real_time: bool = False) -> Series:
    """
    Historical weighted average realized volatility for the underlying assets of an equity index. If top_n_of_index and
    composition_date are not provided, the average is of all constituents based on the weights at each evaluation date

    :param asset: asset object loaded from security master
    :param tenor: relative date representation of expiration date e.g. 1m
    :param returns_type: returns type: simple or logarithmic
    :param top_n_of_index: the number of top constituents to take into account
    :param composition_date: YYYY-MM-DD or relative days before today e.g. 1d, 1m, 1y; defaults to the most recent date
        available
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: average realized volatility curve
    """
    if real_time:
        raise NotImplementedError('realtime average_realized_volatility not implemented')

    if top_n_of_index is None and composition_date is not None:
        raise MqValueError('Specify top_n_of_index to get the average realized volatility of top constituents')

    if top_n_of_index is None and returns_type is not Returns.SIMPLE:
        raise NotImplementedError('returns type {} not supported for average realized volatility of all constituents'
                                  .format(returns_type))

    if top_n_of_index is not None and top_n_of_index > 200:
        raise NotImplementedError('Maximum number of constituents exceeded. Do not use top_n_of_index to calculate on '
                                  'the full list')

    if top_n_of_index is not None:
        constituents = _get_index_constituent_weights(asset, top_n_of_index, composition_date)

        q = GsDataApi.build_market_data_query(
            constituents.index.to_list(),
            QueryType.SPOT,
            source=source,
            real_time=real_time
        )
        _logger.debug('q %s', q)
        df = _market_data_timed(q)

        grouped = df.groupby('assetId')
        weighted_vols = []
        for underlying_id, weight in zip(constituents.index, constituents['netWeight']):
            filtered = grouped.get_group(underlying_id) if underlying_id in grouped.indices else pd.DataFrame()
            filtered = filtered.loc[~filtered.index.duplicated(keep='last')]
            vol = ExtendedSeries() if filtered.empty else ExtendedSeries(volatility(filtered['spot'],
                                                                                    Window(tenor, tenor), returns_type))
            weighted_vols.append(vol * weight)

        series = ExtendedSeries(pd.concat(weighted_vols, axis=1).sum(1, min_count=1),
                                name='averageRealizedVolatility') if len(weighted_vols) else ExtendedSeries()
        series.dataset_ids = getattr(df, 'dataset_ids', ())
        return series

    q = GsDataApi.build_market_data_query(
        [asset.get_marquee_id()],
        QueryType.AVERAGE_REALIZED_VOLATILITY,
        where={'tenor': tenor},
        source=source,
        real_time=real_time
    )
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return _extract_series_from_df(df, QueryType.AVERAGE_REALIZED_VOLATILITY)


def _get_index_constituent_weights(asset: Asset, top_n_of_index: Optional[int] = None,
                                   composition_date: Optional[GENERIC_DATE] = None):
    start, end = _range_from_pricing_date(asset.exchange, composition_date, buffer=1)
    mqid = asset.get_marquee_id()
    positions_data = GsAssetApi.get_asset_positions_data(mqid, start, end, ['netWeight'])
    if not len(positions_data):
        raise MqValueError('Unable to get constituents of {} between {} and {}'.format(mqid, start, end))

    constituents = pd.DataFrame(positions_data)[['underlyingAssetId', 'netWeight', 'positionDate']]
    constituents.set_index('positionDate', inplace=True)
    latest = constituents.index.max()
    _logger.info('selected composition date %s', latest)
    constituents = constituents.loc[latest]
    constituents.sort_values(by=['netWeight'], ascending=False, inplace=True)
    constituents = constituents[:top_n_of_index] if top_n_of_index is not None else constituents
    total_weight = constituents['netWeight'].sum()
    constituents['netWeight'] = constituents['netWeight'] / total_weight

    constituents.set_index('underlyingAssetId', inplace=True)
    return constituents


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
        where=dict(expiry=expiration_tenor, strike=relative_strike),
        source=source,
        real_time=real_time
    )

    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return _extract_series_from_df(df, QueryType.CAP_FLOOR_VOL)


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
        where=dict(expiry=expiration_tenor, strike=0),
        source=source,
        real_time=real_time
    )

    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return _extract_series_from_df(df, QueryType.CAP_FLOOR_ATM_FWD_RATE)


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
        where=dict(expiry=expiration_tenor, longTenor=long_tenor, shortTenor=short_tenor,
                   strike=relative_strike),
        source=source,
        real_time=real_time
    )

    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return _extract_series_from_df(df, QueryType.SPREAD_OPTION_VOL)


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
        where=dict(expiry=expiration_tenor, longTenor=long_tenor, shortTenor=short_tenor, strike=0),
        source=source,
        real_time=real_time
    )

    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return _extract_series_from_df(df, QueryType.SPREAD_OPTION_ATM_FWD_RATE)


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
        where=dict(tenor=termination_tenor),
        source=source,
        real_time=real_time
    )

    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return _extract_series_from_df(df, QueryType.INFLATION_SWAP_RATE)


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
        where=dict(tenor=termination_tenor),
        source=source,
        real_time=real_time
    )

    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return _extract_series_from_df(df, QueryType.BASIS)


@plot_measure((AssetClass.FX,), (AssetType.Cross,), [MeasureDependency(
    id_provider=cross_to_usd_based_cross, query_type=QueryType.GIR_FX_FORECAST)])
def gir_fx_forecast(asset: Asset, relativePeriod: FxForecastHorizon = FxForecastHorizon.THREE_MONTH, *,
                    source: str = None, real_time: bool = False) -> Series:
    """
    FX forecasts made by Global Investment Research (GIR) macro analysts.

    :param asset: asset object loaded from security master
    :param relativePeriod: Forecast horizon. One of: 3m, 6m, 12m, EOY1, EOY2, EOY3, EOY4
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: FX forecast curve
    """
    if real_time:
        raise NotImplementedError('realtime forecast not implemented')

    cross_mqid = asset.get_marquee_id()
    usd_based_cross_mqid = cross_to_usd_based_cross(cross_mqid)
    query_type = QueryType.GIR_FX_FORECAST

    q = GsDataApi.build_market_data_query(
        [usd_based_cross_mqid],
        query_type,
        where=dict(relativePeriod=relativePeriod),
        source=source,
        real_time=real_time
    )
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    series = _extract_series_from_df(df, query_type)

    if cross_mqid != usd_based_cross_mqid:
        series = 1 / series

    series.dataset_ids = getattr(df, 'dataset_ids', ())
    return series


@plot_measure((AssetClass.Equity, AssetClass.FX), None, [QueryType.IMPLIED_VOLATILITY])
def forward_vol(asset: Asset, tenor: str, forward_start_date: str, strike_reference: VolReference,
                relative_strike: Real, *, source: str = None, real_time: bool = False) -> pd.Series:
    """
    Forward volatility.

    :param asset: asset object loaded from security master
    :param tenor: relative date representation of expiration date e.g. 1m
    :param forward_start_date: forward start date e.g. 2m, 1y
    :param strike_reference: reference for strike level
    :param relative_strike: strike relative to reference
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: forward volatility curve
    """
    if real_time:
        raise NotImplementedError('real-time forward vol not implemented')

    if asset.asset_class == AssetClass.FX:
        sr_string, relative_strike = _preprocess_implied_vol_strikes_fx(strike_reference, relative_strike)
        asset_id = cross_stored_direction_for_fx_vol(asset)
    else:
        sr_string, relative_strike = _preprocess_implied_vol_strikes_eq(strike_reference, relative_strike)
        asset_id = asset.get_marquee_id()

    t1_month = _tenor_to_month(forward_start_date)
    t2_month = _tenor_to_month(tenor) + t1_month
    t1 = _month_to_tenor(t1_month)
    t2 = _month_to_tenor(t2_month)

    _logger.debug('where strikeReference=%s, relativeStrike=%s, tenor=%s', sr_string, relative_strike, f'{t1},{t2}')
    where = dict(tenor=[t1, t2], strikeReference=sr_string, relativeStrike=relative_strike)
    q = GsDataApi.build_market_data_query([asset_id], QueryType.IMPLIED_VOLATILITY, where=where,
                                          source=source, real_time=real_time)
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    dataset_ids = getattr(df, 'dataset_ids', ())

    if df.empty:
        series = ExtendedSeries(name='forwardVol')
    else:
        grouped = df.groupby(Fields.TENOR.value)
        try:
            sg = grouped.get_group(t1)['impliedVolatility']
            lg = grouped.get_group(t2)['impliedVolatility']
        except KeyError:
            _logger.debug('no data for one or more tenors')
            series = ExtendedSeries(name='forwardVol')
        else:
            series = ExtendedSeries(sqrt((t2_month * lg ** 2 - t1_month * sg ** 2) / _tenor_to_month(tenor)),
                                    name='forwardVol')
    series.dataset_ids = dataset_ids
    return series


def _process_forward_vol_term(asset: Asset, df: pd.DataFrame, name: str) -> pd.Series:
    if df.empty:
        return pd.Series(dtype='float64')
    else:
        latest = df.index.max()
        _logger.info('selected pricing date %s', latest)
        df = df.loc[latest]

        tenors = [t for t in df[Fields.TENOR.value].values if re.fullmatch('([1-9]\\d*)([my])', t)]
        df = pd.DataFrame(df[df['tenor'].isin(tenors)])
        cbd = _get_custom_bd(asset.exchange)
        df = df.assign(expirationDate=df.index + df['tenor'].map(_to_offset) + cbd - cbd)
        df = df.set_index('expirationDate')
        df.sort_index(inplace=True)

        df = df.assign(tenorInMonth=df['tenor'].map(_tenor_to_month))
        series = sqrt((df['tenorInMonth'] * df[name] ** 2 - df['tenorInMonth'].shift(1) * df[name].shift(1) ** 2) /
                      (df['tenorInMonth'] - df['tenorInMonth'].shift(1)))
        return series.loc[DataContext.current.start_date: DataContext.current.end_date]


@plot_measure((AssetClass.Equity, AssetClass.FX), None, [QueryType.IMPLIED_VOLATILITY])
def forward_vol_term(asset: Asset, strike_reference: VolReference, relative_strike: Real,
                     pricing_date: Optional[GENERIC_DATE] = None, *, source: str = None, real_time: bool = False) \
        -> pd.Series:
    """
    Forward volatility term structure.

    :param asset: asset object loaded from security master
    :param strike_reference: reference for strike level
    :param relative_strike: strike relative to reference
    :param pricing_date: YYYY-MM-DD or relative days before today e.g. 1d, 1m, 1y
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: forward volatility term structure
    """
    if real_time:
        raise NotImplementedError('real-time forward vol term not implemented')

    if asset.asset_class == AssetClass.FX:
        sr_string, relative_strike = _preprocess_implied_vol_strikes_fx(strike_reference, relative_strike)
        asset_id = cross_stored_direction_for_fx_vol(asset)
        buffer = 1  # FX vol data is loaded later
    else:
        sr_string, relative_strike = _preprocess_implied_vol_strikes_eq(strike_reference, relative_strike)
        asset_id = asset.get_marquee_id()
        buffer = 0

    start, end = _range_from_pricing_date(asset.exchange, pricing_date, buffer=buffer)
    with DataContext(start, end):
        _logger.debug('where strikeReference=%s, relativeStrike=%s', sr_string, relative_strike)
        where = dict(strikeReference=sr_string, relativeStrike=relative_strike)
        q = GsDataApi.build_market_data_query([asset_id], QueryType.IMPLIED_VOLATILITY, where=where, source=source,
                                              real_time=real_time)
        _logger.debug('q %s', q)
        df = _market_data_timed(q)

    series = _process_forward_vol_term(asset, df, "impliedVolatility")
    series = ExtendedSeries(series, name='forwardVolTerm')
    series.dataset_ids = getattr(df, 'dataset_ids', ())
    return series


@plot_measure((AssetClass.Equity, AssetClass.Commod, AssetClass.FX), None, [QueryType.IMPLIED_VOLATILITY])
def vol_term(asset: Asset, strike_reference: VolReference, relative_strike: Real,
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

    if asset.asset_class == AssetClass.FX:
        sr_string, relative_strike = _preprocess_implied_vol_strikes_fx(strike_reference, relative_strike)
        asset_id = cross_stored_direction_for_fx_vol(asset)
        buffer = 1  # FX vol data is loaded later
    else:
        sr_string, relative_strike = _preprocess_implied_vol_strikes_eq(strike_reference, relative_strike)
        asset_id = asset.get_marquee_id()
        buffer = 0

    start, end = _range_from_pricing_date(asset.exchange, pricing_date, buffer=buffer)
    with DataContext(start, end):
        _logger.debug('where strikeReference=%s, relativeStrike=%s', sr_string, relative_strike)
        where = dict(strikeReference=sr_string, relativeStrike=relative_strike)
        q = GsDataApi.build_market_data_query([asset_id], QueryType.IMPLIED_VOLATILITY, where=where,
                                              source=source,
                                              real_time=real_time)
        _logger.debug('q %s', q)
        df = _market_data_timed(q)

    dataset_ids = getattr(df, 'dataset_ids', ())
    if df.empty:
        series = ExtendedSeries()
    else:
        latest = df.index.max()
        _logger.info('selected pricing date %s', latest)
        df = df.loc[latest]
        cbd = _get_custom_bd(asset.exchange)
        df = df.assign(expirationDate=df.index + df['tenor'].map(_to_offset) + cbd - cbd)
        df = df.set_index('expirationDate')
        df.sort_index(inplace=True)
        df = df.loc[DataContext.current.start_date: DataContext.current.end_date]
        series = ExtendedSeries() if df.empty else ExtendedSeries(df['impliedVolatility'])
    series.dataset_ids = dataset_ids
    return series


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
            where=dict(tenor=tenor, strikeReference=strike_reference.value),
            source=source,
            real_time=real_time
        )
        _logger.debug('q %s', q)
        df = _market_data_timed(q)

    dataset_ids = getattr(df, 'dataset_ids', ())
    if df.empty:
        series = ExtendedSeries()
    else:
        latest = df.index.max()
        _logger.info('selected pricing date %s', latest)
        df = df.loc[latest]

        vols = df['impliedVolatility'].values
        strikes = df['relativeStrike'].values
        series = ExtendedSeries(vols, index=strikes)
    series.dataset_ids = dataset_ids
    return series


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
        where = dict(strikeReference='forward', relativeStrike=1)
        q = GsDataApi.build_market_data_query([asset.get_marquee_id()], QueryType.FORWARD, where=where, source=source,
                                              real_time=real_time)
        _logger.debug('q %s', q)
        df = _market_data_timed(q)

    dataset_ids = getattr(df, 'dataset_ids', ())
    if df.empty:
        series = ExtendedSeries()
    else:
        latest = df.index.max()
        _logger.info('selected pricing date %s', latest)
        df = df.loc[latest]
        cbd = _get_custom_bd(asset.exchange)
        df.loc[:, 'expirationDate'] = df.index + df['tenor'].map(_to_offset) + cbd - cbd
        df = df.set_index('expirationDate')
        df.sort_index(inplace=True)
        df = df.loc[DataContext.current.start_date: DataContext.current.end_date]
        series = ExtendedSeries() if df.empty else ExtendedSeries(df['forward'])
    series.dataset_ids = dataset_ids
    return series


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


@plot_measure((AssetClass.Equity, ), None, [QueryType.VAR_SWAP])
def forward_var_term(asset: Asset, pricing_date: Optional[GENERIC_DATE] = None, *, source: str = None,
                     real_time: bool = False) -> pd.Series:
    """
    Forward variance swap term structure.

    :param asset: asset object loaded from security master
    :param pricing_date: YYYY-MM-DD or relative days before today e.g. 1d, 1m, 1y
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: forward variance swap term structure
    """
    if real_time:
        raise NotImplementedError('real-time forward var term not implemented')

    start, end = _range_from_pricing_date(asset.exchange, pricing_date)
    with DataContext(start, end):
        q = GsDataApi.build_market_data_query([asset.get_marquee_id()], QueryType.VAR_SWAP, source=source,
                                              real_time=real_time)
        _logger.debug('q %s', q)
        df = _market_data_timed(q)

    series = _process_forward_vol_term(asset, df, Fields.VAR_SWAP.value)
    series = ExtendedSeries(series, name='forwardVarTerm')
    series.dataset_ids = getattr(df, 'dataset_ids', ())
    return series


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
            dataset_ids = set()
            for t in tenors:
                diff = _tenor_to_month(t) - _tenor_to_month(forward_start_date)
                if diff < 1:
                    continue
                t1 = _month_to_tenor(diff)
                c = var_swap(asset, t1, forward_start_date, source=source, real_time=real_time)
                dataset_ids.update(getattr(c, 'dataset_ids', ()))
                c = c.to_frame()
                if not c.empty:
                    c['tenor'] = t1
                    sub_frames.append(c)
            df = pd.concat(sub_frames)
            dataset_ids = tuple(dataset_ids)
        else:
            q = GsDataApi.build_market_data_query([asset.get_marquee_id()], QueryType.VAR_SWAP,
                                                  source=source, real_time=real_time)
            _logger.debug('q %s', q)
            df = _market_data_timed(q)
            dataset_ids = getattr(df, 'dataset_ids', ())

    if df.empty:
        series = ExtendedSeries()
    else:
        latest = df.index.max()
        _logger.info('selected pricing date %s', latest)
        df = df.loc[latest]
        cbd = _get_custom_bd(asset.exchange)
        df.loc[:, Fields.EXPIRATION_DATE.value] = df.index + df[Fields.TENOR.value].map(_to_offset) + cbd - cbd
        df = df.set_index(Fields.EXPIRATION_DATE.value)
        df.sort_index(inplace=True)
        df = df.loc[DataContext.current.start_date: DataContext.current.end_date]
        series = ExtendedSeries() if df.empty else ExtendedSeries(df[Fields.VAR_SWAP.value])

    series.dataset_ids = dataset_ids
    return series


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
        where = dict(tenor=tenor)
        q = GsDataApi.build_market_data_query([asset.get_marquee_id()], QueryType.VAR_SWAP,
                                              where=where, source=source, real_time=real_time)
        _logger.debug('q %s', q)
        df = _market_data_timed(q)
        series = ExtendedSeries() if df.empty else ExtendedSeries(df[Fields.VAR_SWAP.value])
        series.dataset_ids = getattr(df, 'dataset_ids', ())
        return series
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
            series = ExtendedSeries()
            series.dataset_ids = ()
            return series

        _logger.debug('where tenor=%s', f'{yt},{zt}')
        where = dict(tenor=[yt, zt])
        q = GsDataApi.build_market_data_query([asset.get_marquee_id()], QueryType.VAR_SWAP,
                                              where=where, source=source, real_time=real_time)
        _logger.debug('q %s', q)
        df = _market_data_timed(q)
        dataset_ids = getattr(df, 'dataset_ids', ())
        if df.empty:
            series = ExtendedSeries()
        else:
            grouped = df.groupby(Fields.TENOR.value)
            try:
                yg = grouped.get_group(yt)[Fields.VAR_SWAP.value]
                zg = grouped.get_group(zt)[Fields.VAR_SWAP.value]
            except KeyError:
                _logger.debug('no data for one or more tenors')
                series = ExtendedSeries()
                series.dataset_ids = ()
                return series
            series = ExtendedSeries(sqrt((z * zg ** 2 - y * yg ** 2) / x))
        series.dataset_ids = dataset_ids
        return series


def _get_iso_data(region: str):
    timezone = 'US/Eastern'
    peak_start = 7
    peak_end = 23
    weekends = [5, 6]

    if region in ['MISO', 'ERCOT', 'SPP']:
        timezone = 'US/Central'
        peak_start = 6
        peak_end = 22
    if region == 'CAISO':
        timezone = 'US/Pacific'
        weekends = [6]
        peak_start = 6
        peak_end = 22

    return timezone, peak_start, peak_end, weekends


def _filter_by_bucket(df, bucket, holidays, region):
    # TODO: get frequency definition from SecDB
    timezone, peak_start, peak_end, weekends = _get_iso_data(region)
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
    elif bucket.lower() == '2x16h' or bucket.lower() == 'suh1x16':
        df = df.loc[((df['date'].isin(holidays)) | df['day'].isin(weekends)) & ((df['hour'] > peak_start - 1) &
                                                                                (df['hour'] < peak_end))]
    else:
        raise ValueError('Invalid bucket: ' + bucket + '. Expected Value: peak, offpeak, 7x24, 7x8, 2x16h.')
    return df


def _string_to_date_interval(interval: str):
    """
    Slang Date::Interval implementation
    Accept months (e.g. F07), quarters (e.g. 4Q06), half-years (e.g. 1H07), and years (e.g. Cal07 or 2007)
    :param interval: date-interval
    :return: start and end date
    """
    if interval[-2:].isdigit():
        YS = interval[-2:]
        year = int("20" + YS) if int(YS) <= 51 else int("19" + YS)
    else:
        return "Invalid year"

    if len(interval) > 4 and interval[-4:].isdigit():
        YS = interval[-4:]
        year = int(YS)

    start_year = datetime.date(year, 1, 1)
    if len(interval) == 1 + len(YS):
        if interval[0].upper() in _COMMOD_CONTRACT_MONTH_CODES:
            month_index = _COMMOD_CONTRACT_MONTH_CODES.index(interval[0].upper()) + 1
            start_date = datetime.date(year, month_index, 1)
            end_date = datetime.date(year, month_index, calendar.monthrange(year, month_index)[1])
        else:
            return "Invalid month"
    elif (len(interval) == 2 + len(YS) and interval.isdigit()) or (
            interval.casefold().startswith("Cal".casefold()) and len(interval) == 3 + len(YS)):
        start_date = datetime.date(year, 1, 1)
        end_date = datetime.date(year, 12, 31)
    elif len(interval) == 2 + len(YS):
        if interval[0].isdigit():
            num = int(interval[0])
        else:
            return "Invalid num"
        if interval[1].upper() == "Q":
            if 1 <= num <= 4:
                start_date = (start_year + relativedelta(months=+(3 * (num - 1))))
                end_date = start_year + relativedelta(months=+(3 * num), days=-1)
            else:
                return "Invalid Quarter"
        if interval[1].upper() == "H":
            if 1 <= num <= 2:
                start_date = start_year + relativedelta(months=+(6 * (num - 1)))
                end_date = start_year + relativedelta(months=+(6 * num), days=-1)
            else:
                return "Invalid Half Year"
    elif len(interval) >= 3 + len(YS):
        left = interval[0:len(interval) - len(YS)]
        if left.isalpha():
            if left in calendar.month_name:
                month_index = {v: k for k, v in enumerate(calendar.month_name)}[left]
            elif left in calendar.month_abbr:
                month_index = {v: k for k, v in enumerate(calendar.month_abbr)}[left]
            else:
                return "Invalid date code"
            start_date = datetime.date(year, month_index, 1)
            end_date = datetime.date(year, month_index, calendar.monthrange(year, month_index)[1])
        else:
            return "Invalid date code"
    else:
        return "Unknown date code"
    return {'start_date': start_date, 'end_date': end_date}


def _merge_curves_by_weighted_average(forwards_data, weights, keys, measure_column):
    """
    Merges price curve with weights curve
    :param forwards_data: Pricing data
    :param weights: dataframe with each pricing data point associated with a weight
    :param keys: keys to join dataframes - columns that uniquely identify each datapoint
    :param measure_column: dataset measure column name
    :return:
    """
    # Using cartesian product of the date range and weights dataframe with keys
    # as this gives us an exhaustive list of data points required for the data to be complete
    # i.e a composite key comprised of date and keys
    dates = pd.DataFrame(data=forwards_data['dates'].unique(), columns=["dates"])
    weights = pd.merge(weights.assign(key=0), dates.assign(key=0), on='key').drop('key', axis=1)

    # Left join on the weights dataframe using the composite key
    result_df = pd.merge(weights, forwards_data, on=keys, how='left')

    result_df['weighted_price'] = result_df['weight'] * result_df[measure_column]

    # Filtering dates that have missing buckets or contracts.
    # Dates with any null values due to unmatched rows in the right table with raw data will be removed as a result.
    null_dates = set(result_df[result_df[measure_column].isnull()]['dates'])
    result_df = result_df[~result_df['dates'].isin(null_dates)]

    result_df = result_df.groupby('dates').agg({'weight': 'sum', 'weighted_price': 'sum'})
    result_df['price'] = result_df['weighted_price'] / result_df['weight']

    result = ExtendedSeries(result_df['price'], index=result_df.index)
    result = result.rename_axis(None, axis='index')
    return result


def _weighted_average_valuation_curve_for_calendar_strip(asset, contract_range, query_type, measure_field):
    """
    :param asset: marquee asset
    :param contract_range: tenor in case of instruments, calendar strip for underliers
    :param query_type: dataset query type
    :param measure_field: dataset measure column name
    :return:
    """
    start_date_interval = _string_to_date_interval(contract_range.split("-")[0])
    if type(start_date_interval) == str:
        raise ValueError(start_date_interval)
    start_contract_range = start_date_interval['start_date']
    if "-" in contract_range:
        end_date_interval = _string_to_date_interval(contract_range.split("-")[1])
        if type(end_date_interval) == str:
            raise ValueError(end_date_interval)
        end_contract_range = end_date_interval['end_date']
    else:
        end_contract_range = start_date_interval['end_date']

    dates_contract_range = get_contract_range(start_contract_range, end_contract_range, None)

    weights = dates_contract_range.groupby('contract_month').size()
    weights = pd.DataFrame({'contract': weights.index, 'weight': weights.values})

    start, end = DataContext.current.start_date, DataContext.current.end_date

    contracts_to_query = weights['contract'].unique().tolist()
    where = dict(contract=contracts_to_query)

    with DataContext(start, end):
        q = GsDataApi.build_market_data_query([asset.get_marquee_id()], query_type,
                                              where=where,
                                              source=None,
                                              real_time=False)
        data = _market_data_timed(q)
        dataset_ids = getattr(data, 'dataset_ids', ())

        data['dates'] = data.index.date
        print('q %s', q)

    keys = ['contract', 'dates']
    result = _merge_curves_by_weighted_average(data, weights, keys, measure_field)
    result.dataset_ids = dataset_ids
    return result


@plot_measure((AssetClass.Commod,), None, [QueryType.FAIR_PRICE])
def fair_price(asset: Asset, tenor: str = None, *,
               source: str = None, real_time: bool = False) -> pd.Series:
    """'
    Fair Price for Swap Instrument

    :param asset: asset object loaded from security master
    :param tenor: e.g. inputs - 'Cal20', 'F20-G20', '2Q20', '2H20', 'Cal20-Cal21': Default Value = F20
    :param source: name of function caller: default source = None
    :param real_time: whether to retrieve intraday data instead of EOD: default value = False
    :return: Fair Price
    """

    asset_type = asset.get_type()

    if asset_type == SecAssetType.INDEX:
        if tenor is None:
            raise ValueError('Contract month range query input is not specified')
        return _weighted_average_valuation_curve_for_calendar_strip(asset, tenor, QueryType.FAIR_PRICE, "fairPrice")

    asset_id = asset.get_marquee_id()
    q = GsDataApi.build_market_data_query([asset_id], QueryType.FAIR_PRICE, source=source,
                                          real_time=real_time)
    df = _market_data_timed(q)
    return _extract_series_from_df(df, QueryType.FAIR_PRICE)


@plot_measure((AssetClass.Commod,), None, [QueryType.FORWARD_PRICE])
def forward_price(asset: Asset, price_method: str = 'LMP', bucket: str = 'PEAK',
                  contract_range: str = 'F20', *, source: str = None, real_time: bool = False) -> pd.Series:
    """
    Us Power Forward Prices

    :param asset: asset object loaded from security master
    :param price_method: price method between LMP, MCP, SPP: Default value = LMP
    :param bucket: bucket type among '7x24', 'peak', 'offpeak', '2x16h', '7x16' and '7x8': Default value = 7x24
    :param contract_range: e.g. inputs - 'Cal20', 'F20-G20', '2Q20', '2H20', 'Cal20-Cal21': Default Value = F20
    :param source: name of function caller: default source = None
    :param real_time: whether to retrieve intraday data instead of EOD: default value = False
    :return: Us Power Forward Prices
    """
    if real_time:
        raise ValueError('Use daily frequency instead of intraday')

    bbid = Asset.get_identifier(asset, AssetIdentifier.BLOOMBERG_ID)

    def _get_weight_for_bucket(df, bucket, holidays, region):
        df = _filter_by_bucket(df, bucket, holidays, region)
        weights_df = df.groupby('contract_month').size()
        weights_df = pd.DataFrame({'contract': weights_df.index, 'weight': weights_df.values})
        weights_df['quantityBucket'] = bucket
        return weights_df

    start_date_interval = _string_to_date_interval(contract_range.split("-")[0])
    if type(start_date_interval) == str:
        raise ValueError(start_date_interval)
    start_contract_range = start_date_interval['start_date']
    if "-" in contract_range:
        end_date_interval = _string_to_date_interval(contract_range.split("-")[1])
        if type(end_date_interval) == str:
            raise ValueError(end_date_interval)
        end_contract_range = end_date_interval['end_date']
    else:
        end_contract_range = start_date_interval['end_date']

    region = bbid.split(" ")[0]
    timezone = _get_iso_data(region)[0]

    weekend_offpeak = "SUH1X16" if region == 'CAISO' else "2X16H"
    QBT_mapping = {"OFFPEAK": [weekend_offpeak, "7X8"], "7X16": ["PEAK", weekend_offpeak],
                   "7X24": ["PEAK", "7X8", weekend_offpeak]}

    dates_contract_range = get_contract_range(start_contract_range, end_contract_range, timezone)

    holidays = NercCalendar().holidays(start=start_contract_range, end=end_contract_range).date

    weights = []
    buckets_QBT = QBT_mapping[bucket.upper()] if bucket.upper() in QBT_mapping else [bucket.upper()]
    for bucket_QBT in buckets_QBT:
        weight = _get_weight_for_bucket(dates_contract_range, bucket_QBT, holidays, region)
        weights.append(weight)
    weights = pd.concat(weights)

    start, end = DataContext.current.start_date, DataContext.current.end_date

    contracts_to_query = weights['contract'].unique().tolist()
    quantitybuckets_to_query = weights['quantityBucket'].unique().tolist()

    where = dict(priceMethod=price_method.upper(), quantityBucket=quantitybuckets_to_query, contract=contracts_to_query)
    with DataContext(start, end):
        q = GsDataApi.build_market_data_query([asset.get_marquee_id()], QueryType.FORWARD_PRICE,
                                              where=where, source=None,
                                              real_time=False)
        forwards_data = _market_data_timed(q)
        dataset_ids = getattr(forwards_data, 'dataset_ids', ())

        forwards_data['dates'] = forwards_data.index.date
        print('q %s', q)

    keys = ['quantityBucket', 'contract', 'dates']
    measure_column = 'forwardPrice'
    result = _merge_curves_by_weighted_average(forwards_data, weights, keys, measure_column)
    result.dataset_ids = dataset_ids
    return result


def get_contract_range(start_contract_range, end_contract_range, timezone):
    if timezone:
        df = pd.date_range(start=start_contract_range,
                           end=end_contract_range + datetime.timedelta(days=1), freq='H',
                           closed='left',
                           tz=timezone).to_frame()

        df['hour'] = df.index.hour
        df['day'] = df.index.dayofweek
    else:
        df = pd.date_range(start=start_contract_range,
                           end=end_contract_range,
                           ).to_frame()

    df['date'] = df.index.date
    df['month'] = df.index.month - 1
    df['year'] = df.index.year
    df['contract_month'] = df['month'].map(_COMMOD_CONTRACT_MONTH_CODES_DICT) + df['year'].astype(str).str[2:]

    return df


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
    region = bbid.split(" ")[0]
    timezone = _get_iso_data(region)[0]

    to_zone = tz.gettz('UTC')
    from_zone = tz.gettz(timezone)

    # Start date and end date are considered to be in ISO's local timezone
    start_date, end_date = DataContext.current.start_date, DataContext.current.end_date
    holidays = NercCalendar().holidays(start=start_date, end=end_date).date
    # Start time is constructed by combining start date with 00:00:00 timestamp
    # in local time and then converted to UTC time
    # End time is constructed by combining end date with 23:59:59 timestamp
    # in local time and then converted to UTC time
    start_time = datetime.datetime.combine(start_date, datetime.datetime.min.time(), tzinfo=from_zone) \
        .astimezone(to_zone)
    end_time = datetime.datetime.combine(end_date, datetime.datetime.max.time(), tzinfo=from_zone).astimezone(to_zone)

    where = dict(priceMethod=price_method.upper())
    with DataContext(start_time, end_time):
        q = GsDataApi.build_market_data_query([asset.get_marquee_id()], QueryType.PRICE, where=where, source=source,
                                              real_time=True)
        df = _market_data_timed(q)
        _logger.debug('q %s', q)

    dataset_ids = getattr(df, 'dataset_ids', ())
    df = df.tz_convert(timezone)

    df['month'] = df.index.to_period('M')
    df['date'] = df.index.date
    df['day'] = df.index.dayofweek
    df['hour'] = df.index.hour
    df['timestamp'] = df.index

    # This will remove any duplicate prices uploaded with the same timestamp
    df = df.drop_duplicates()
    # freq is the frequency at which the ISO publishes data for e.g. 15 min, 1hr
    freq = int(min(np.diff(df.index).astype('timedelta64[s]') / np.timedelta64(1, 's')))
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

    df = _filter_by_bucket(df, bucket, holidays, region)
    df = df['price'].resample(granularity).mean()
    df.index = df.index.date
    df = df.loc[start_date: end_date]
    series = ExtendedSeries(df)
    series.dataset_ids = dataset_ids
    return series


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=currency_to_default_benchmark_rate,
                                 query_type=QueryType.CENTRAL_BANK_SWAP_RATE)])
def central_bank_swap_rate(asset: Asset, rate_type: MeetingType = MeetingType.MEETING_FORWARD,
                           level_type: str = 'absolute',
                           valuation_date: GENERIC_DATE = datetime.date.today() - datetime.timedelta(days=1), *,
                           source: str = None, real_time: bool = False) -> pd.Series:
    """'
    OIS Swap rate for a swap structured between consecutive Central Bank meeting dates or End Of Year Dates.

    :param asset: asset object loaded from security master
    :param rate_type: Spot= Effective Policy rate, Meeting = Forward Policy rate expectations,
                    EOY = Policy rate expectations at EOY for the next 5 years
    :param level_type: absolute, relative
    :param valuation_date:  reference date on which all future expectations are calculated
    :param source: name of function caller: default source = None
    :param real_time: whether to retrieve intraday data instead of EOD: default value = False
    :return: OIS Swap rate for swap structured between consecutive CB meeting dates
    """

    if real_time:
        raise NotImplementedError('real-time central bank swap rate not implemented')
    if not isinstance(valuation_date, (dt.date, str)):
        raise MqValueError('valuation_date must be of type datetime.date or string YYYY-MM-DD')
    if rate_type not in MeetingType:
        raise MqValueError('rate_type must be one of Spot, Meeting Forward and EOY Forward')
    if level_type not in ['relative', 'absolute']:
        raise MqValueError('level_type must be either absolute or relative')

    if isinstance(valuation_date, str):
        valuation_date = parse_meeting_date(valuation_date)
        if valuation_date == '':
            raise MqValueError('Valuation date string must be of the format: YYYY-MM-DD')

    mqid = convert_asset_for_rates_data_set(asset, RatesConversionType.OIS_BENCHMARK_RATE)

    _logger.debug('where assetId=%s, metric=Central Bank Swap Rate, rate_type=%s, level_type=%s, valuation date=%s',
                  mqid, rate_type, level_type, str(valuation_date))

    ds = Dataset('CENTRAL_BANK_WATCH')
    if rate_type == MeetingType.SPOT:
        if level_type == 'relative':
            raise MqValueError('level_type must be absolute for rate_type = Spot')
        else:
            df = ds.get_data(assetId=[mqid], rateType=rate_type, start=CENTRAL_BANK_WATCH_START_DATE)
    else:
        df = ds.get_data(assetId=[mqid], rateType=rate_type, valuationDate=valuation_date,
                         start=CENTRAL_BANK_WATCH_START_DATE)

    if level_type == 'relative':
        # df = remove_dates_with_null_entries(df)
        spot = df[df['meetingNumber'] == 0]['value'][0]
        df['value'] = df['value'] - spot
    df = df.reset_index()
    df = df.set_index('meetingDate')
    series = ExtendedSeries(df['value'])
    series.dataset_ids = ('CENTRAL_BANK_WATCH',)
    return series


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=currency_to_default_benchmark_rate,
                                 query_type=QueryType.POLICY_RATE_EXPECTATION)])
def policy_rate_expectation(asset: Asset, rate_type: MeetingType = MeetingType.MEETING_FORWARD,
                            level_type: str = 'absolute',
                            meeting_date: Union[datetime.date, int, str] = 0,
                            *, source: str = None, real_time: bool = False) -> pd.Series:
    """'
    Historical policy rate expectations for a given meeting date or end of year OIS rate expectations.

    :param asset: asset object loaded from security master
    :param meeting_date: Actual meeting date / can also input meeting number standing today : 0 for last, 1 for next ,
                                        2 for meeting after next and so on
    :param level_type: absolute, relative
    :param rate_type: meeting, eoy
    :param source: name of function caller: default source = None
    :param real_time: whether to retrieve intraday data instead of EOD: default value = False
    :return: historical policy rate expectations for a given CB meeting date
    """

    if real_time:
        raise NotImplementedError('real-time central bank swap rate not implemented')
    if rate_type not in [MeetingType.MEETING_FORWARD, MeetingType.EOY_FORWARD]:
        raise MqValueError('invalid rate_type specified, \'Meeting Forward\' or \'EOY Forward\' allowed')
    if level_type not in ['relative', 'absolute']:
        raise MqValueError('level_type must be either absolute or relative')
    if not isinstance(meeting_date, (dt.date, str, int)):
        raise MqValueError('valuation_date must be of type datetime.date or string YYYY-MM-DD or integer')

    mqid = convert_asset_for_rates_data_set(asset, RatesConversionType.OIS_BENCHMARK_RATE)

    _logger.debug('where assetId=%s, metric=Policy Rate Expectation, meeting_date=%s, level_type=%s',
                  mqid, str(meeting_date), level_type)

    ds = Dataset('CENTRAL_BANK_WATCH')
    if isinstance(meeting_date, int):
        meeting_number = meeting_date
        if meeting_number < 0 or meeting_number > 20:
            raise MqValueError('meeting_number has to be an integer between 0 and 20 where 0 is the '
                               'last meeting and 1 is the next meeting')

        cbw_df = ds.get_data(assetId=[mqid], rateType=rate_type, meetingNumber=meeting_number,
                             start=CENTRAL_BANK_WATCH_START_DATE)
    elif isinstance(meeting_date, str):
        meeting_date = parse_meeting_date(meeting_date)
        if meeting_date == '':
            raise MqValueError('Meeting date string must be of the format: YYYY-MM-DD')
        cbw_df = ds.get_data(assetId=[mqid], rateType=rate_type, meeting_date=meeting_date,
                             start=CENTRAL_BANK_WATCH_START_DATE)
    else:
        cbw_df = ds.get_data(assetId=[mqid], rateType=rate_type, meeting_date=meeting_date,
                             start=CENTRAL_BANK_WATCH_START_DATE)

    if cbw_df.empty:
        raise MqValueError('meeting date specified returned no data')

    if level_type == 'relative':
        spot_df = ds.get_data(assetId=[mqid], rateType=rate_type, meetingNumber=0,
                              start=CENTRAL_BANK_WATCH_START_DATE).rename(columns={'value': 'spotValue'})
        if spot_df.empty:
            raise MqValueError('no spot data returned to rebase')
        joined_df = cbw_df.merge(spot_df, on=['date', 'assetId', 'rateType', 'location', 'valuationDate'], how='inner')
        joined_df = joined_df.set_index('valuationDate')
        joined_df['relValue'] = (joined_df['value'] - joined_df['spotValue'])
        series = ExtendedSeries(joined_df['relValue'])
    else:
        cbw_df = cbw_df.set_index('valuationDate')
        series = ExtendedSeries(cbw_df['value'])
    series.dataset_ids = ('CENTRAL_BANK_WATCH',)
    return series


@plot_measure((AssetClass.Equity,), None, [QueryType.FUNDAMENTAL_METRIC])
def dividend_yield(asset: Asset, period: str, period_direction: FundamentalMetricPeriodDirection,
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
        where=dict(metric=metric, period=period, periodDirection=period_direction.value),
        source=source,
        real_time=real_time
    )

    q['queries'][0]['vendor'] = 'Goldman Sachs'
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return _extract_series_from_df(df, QueryType.FUNDAMENTAL_METRIC)


@plot_measure((AssetClass.Equity,), None, [QueryType.FUNDAMENTAL_METRIC])
def earnings_per_share(asset: Asset,
                       period: str,
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
        where=dict(metric=metric, period=period, periodDirection=period_direction.value),
        source=source,
        real_time=real_time
    )

    q['queries'][0]['vendor'] = 'Goldman Sachs'
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return _extract_series_from_df(df, QueryType.FUNDAMENTAL_METRIC)


@plot_measure((AssetClass.Equity,), None, [QueryType.FUNDAMENTAL_METRIC])
def earnings_per_share_positive(asset: Asset,
                                period: str,
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
        where=dict(metric=metric, period=period, periodDirection=period_direction.value),
        source=source,
        real_time=real_time
    )

    q['queries'][0]['vendor'] = 'Goldman Sachs'
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return _extract_series_from_df(df, QueryType.FUNDAMENTAL_METRIC)


@plot_measure((AssetClass.Equity,), None, [QueryType.FUNDAMENTAL_METRIC])
def net_debt_to_ebitda(asset: Asset,
                       period: str,
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
        where=dict(metric=metric, period=period, periodDirection=period_direction.value),
        source=source,
        real_time=real_time
    )

    q['queries'][0]['vendor'] = 'Goldman Sachs'
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return _extract_series_from_df(df, QueryType.FUNDAMENTAL_METRIC)


@plot_measure((AssetClass.Equity,), None, [QueryType.FUNDAMENTAL_METRIC])
def price_to_book(asset: Asset, period: str, period_direction: FundamentalMetricPeriodDirection,
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
        where=dict(metric=metric, period=period, periodDirection=period_direction.value),
        source=source,
        real_time=real_time
    )

    q['queries'][0]['vendor'] = 'Goldman Sachs'
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return _extract_series_from_df(df, QueryType.FUNDAMENTAL_METRIC)


@plot_measure((AssetClass.Equity,), None, [QueryType.FUNDAMENTAL_METRIC])
def price_to_cash(asset: Asset, period: str, period_direction: FundamentalMetricPeriodDirection,
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
        where=dict(metric=metric, period=period, periodDirection=period_direction.value),
        source=source,
        real_time=real_time
    )

    q['queries'][0]['vendor'] = 'Goldman Sachs'
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return _extract_series_from_df(df, QueryType.FUNDAMENTAL_METRIC)


@plot_measure((AssetClass.Equity,), None, [QueryType.FUNDAMENTAL_METRIC])
def price_to_earnings(asset: Asset, period: str, period_direction: FundamentalMetricPeriodDirection,
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
        where=dict(metric=metric, period=period, periodDirection=period_direction.value),
        source=source,
        real_time=real_time
    )

    q['queries'][0]['vendor'] = 'Goldman Sachs'
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return _extract_series_from_df(df, QueryType.FUNDAMENTAL_METRIC)


@plot_measure((AssetClass.Equity,), None, [QueryType.FUNDAMENTAL_METRIC])
def price_to_earnings_positive(asset: Asset,
                               period: str,
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
        where=dict(metric=metric, period=period, periodDirection=period_direction.value),
        source=source,
        real_time=real_time
    )

    q['queries'][0]['vendor'] = 'Goldman Sachs'
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return _extract_series_from_df(df, QueryType.FUNDAMENTAL_METRIC)


@plot_measure((AssetClass.Equity,), None, [QueryType.FUNDAMENTAL_METRIC])
def price_to_sales(asset: Asset, period: str, period_direction: FundamentalMetricPeriodDirection,
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
        where=dict(metric=metric, period=period, periodDirection=period_direction.value),
        source=source,
        real_time=real_time
    )

    q['queries'][0]['vendor'] = 'Goldman Sachs'
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return _extract_series_from_df(df, QueryType.FUNDAMENTAL_METRIC)


@plot_measure((AssetClass.Equity,), None, [QueryType.FUNDAMENTAL_METRIC])
def return_on_equity(asset: Asset, period: str, period_direction: FundamentalMetricPeriodDirection,
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
        where=dict(metric=metric, period=period, periodDirection=period_direction.value),
        source=source,
        real_time=real_time
    )

    q['queries'][0]['vendor'] = 'Goldman Sachs'
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return _extract_series_from_df(df, QueryType.FUNDAMENTAL_METRIC)


@plot_measure((AssetClass.Equity,), None, [QueryType.FUNDAMENTAL_METRIC])
def sales_per_share(asset: Asset, period: str, period_direction: FundamentalMetricPeriodDirection,
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
        where=dict(metric=metric, period=period, periodDirection=period_direction.value),
        source=source,
        real_time=real_time
    )

    q['queries'][0]['vendor'] = 'Goldman Sachs'
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return _extract_series_from_df(df, QueryType.FUNDAMENTAL_METRIC)


@plot_measure((AssetClass.Equity,), (AssetType.Index, AssetType.ETF,), [QueryType.REALIZED_CORRELATION])
def realized_correlation(asset: Asset, tenor: str, top_n_of_index: Optional[int] = None,
                         composition_date: Optional[GENERIC_DATE] = None, *,
                         source: str = None, real_time: bool = False) -> Series:
    """
    Realized correlation of an asset.

    :param asset: asset object loaded from security master
    :param tenor: relative date representation of expiration date e.g. 1m
    :param top_n_of_index: the number of top constituents to take into account
    :param composition_date: YYYY-MM-DD or relative days before today e.g. 1d, 1m, 1y; defaults to most recent date
        available
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: realized correlation curve
    """
    if real_time:
        raise NotImplementedError('realtime realized_correlation not implemented')

    if top_n_of_index is None and composition_date is not None:
        raise MqValueError('specify top_n_of_index to get realized correlation of top constituents')

    if top_n_of_index is not None and top_n_of_index > 100:
        raise MqValueError('number of constituents (top_n_of_index) must be <= 100')

    mqid = asset.get_marquee_id()
    _logger.debug('where tenor=%s', tenor)
    where = dict(tenor=tenor)

    if top_n_of_index is None:
        q = GsDataApi.build_market_data_query([mqid], QueryType.REALIZED_CORRELATION, where=where,
                                              source=source, real_time=real_time)
        _logger.debug('q %s', q)
        df = _market_data_timed(q)
        return _extract_series_from_df(df, QueryType.REALIZED_CORRELATION)

    # results for top n
    constituents = _get_index_constituent_weights(asset, top_n_of_index, composition_date)
    head_start = DataContext.current.start_date - datetime.timedelta(days=relative_date_add(tenor, True) + 1)
    with DataContext(head_start, DataContext.current.end_date):
        q = GsDataApi.build_market_data_query(
            constituents.index.to_list() + [mqid],
            QueryType.SPOT,
            source=source,
            real_time=real_time
        )
        _logger.debug('q %s', q)
        df = _market_data_timed(q)
    match = df['assetId'] == mqid
    df_asset = df.loc[match]
    df_rest = df.loc[~match]

    grouped = df_rest.groupby('assetId')
    weighted_vols = []
    for underlying_id, weight in zip(constituents.index, constituents['netWeight']):
        filtered = grouped.get_group(underlying_id) if underlying_id in grouped.indices else pd.DataFrame()
        filtered = filtered.loc[~filtered.index.duplicated(keep='last')]
        if not filtered.empty:
            vol = volatility(filtered['spot'], Window(tenor, tenor)) / 100
            assert not vol.empty, f'insufficient history to calculate for {tenor}'
            weighted_vols.append(vol * weight)

    if len(weighted_vols) == 0:
        raise MqValueError(f'no data for constituents of {asset}')

    s1 = pd.concat(weighted_vols, axis=1).sum(1, min_count=1)
    s2 = pd.concat(map(lambda x: x * x, weighted_vols), axis=1).sum(1, min_count=1)
    idx_vol = volatility(df_asset['spot'], Window(tenor, tenor)) / 100
    values = (idx_vol * idx_vol - s2) / (s1 * s1 - s2) * 100
    series = ExtendedSeries(values)
    series.dataset_ids = getattr(df, 'dataset_ids', ())
    return series


@plot_measure((AssetClass.Commod, AssetClass.Equity, AssetClass.FX), None, [QueryType.SPOT])
def realized_volatility(asset: Asset, w: Union[Window, int, str] = Window(None, 0),
                        returns_type: Returns = Returns.SIMPLE, *, source: str = None, real_time: bool = False) \
        -> Series:
    """
    Realized volatility for an asset.

    :param asset: asset object loaded from security master
    :param w: number of observations to use; defaults to length of series. If string is provided, should be
        in relative date form (e.g. "1d", "1w", "1m", "1y", etc).
    :param returns_type: returns type: simple or logarithmic
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: realized volatility curve
    """
    q = GsDataApi.build_market_data_query(
        [asset.get_marquee_id()],
        QueryType.SPOT,
        source=source,
        real_time=real_time
    )
    df = _market_data_timed(q)
    series = ExtendedSeries() if df.empty else ExtendedSeries(volatility(df['spot'], w, returns_type))
    series.dataset_ids = getattr(df, 'dataset_ids', ())
    return series


@plot_measure((AssetClass.Equity,), None, [QueryType.ES_NUMERIC_SCORE])
def esg_aggregate(asset: Asset, metric: EsgMetric, value_unit: Optional[EsgValueUnit] = None, *,
                  source: str = None, real_time: bool = False) -> Series:
    """
    Environmental, Social, and Governance (ESG) scores and percentiles for a broad set of companies across the globe.
    :param asset: asset object loaded from security master
    :param metric: name of ESG metric
    :param value_unit: the unit type of the metric value, one of percentile, score
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return:
    """

    if real_time:
        raise NotImplementedError('real-time esg-aggregate not implemented')

    if metric != EsgMetric.ENVIRONMENTAL_SOCIAL_DISCLOSURE and value_unit is None:
        raise MqValueError("value_unit is required for metric {m}".format(m=metric.value))

    mqid = asset.get_marquee_id()
    if metric == EsgMetric.ENVIRONMENTAL_SOCIAL_DISCLOSURE:
        query_metric = inflection.camelize(metric.value, False)
    else:
        query_metric = "{metric}{unit}".format(metric=inflection.camelize(metric.value, False),
                                               unit=value_unit.value.capitalize())

    query_type = ESG_METRIC_TO_QUERY_TYPE.get(query_metric)
    _logger.debug('where assetId=%s, metric=%s, value_unit=%s, query_type=%s',
                  mqid, metric.value, value_unit.value if value_unit is not None else None, query_type.value)
    q = GsDataApi.build_market_data_query([mqid], query_type, source=source, real_time=real_time)
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    series = ExtendedSeries() if df.empty else ExtendedSeries(df[query_metric])
    series.dataset_ids = getattr(df, 'dataset_ids', ())
    return series


@plot_measure((AssetClass.Equity,), (AssetType.Single_Stock,), [QueryType.RATING, QueryType.CONVICTION_LIST])
def gir_rating(asset: Asset, metric: _RatingMetric, *, source: str = None, real_time: bool = False) -> Series:
    """
    Analyst Rating, which may take on the following values
    {'Sell': -1, 'Neutral': 0, 'Buy': 1}
    Conviction List, which is true if the security is on the Conviction Buy List or false otherwise.
    Securities with a convictionList value equal to true are by definition a subset of the securities
    with a rating equal to Buy

    :param asset: asset object loaded from security master
    :param metric: Name of metric. Either rating or conviction list
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: ratings in numeric form ( 'Buy' : 1, 'Neutral' : 0, 'Sell' : -1 )
    """
    if real_time:
        raise NotImplementedError('real-time rating not implemented')
    mqid = asset.get_marquee_id()
    query_type = _RATING_METRIC_TO_QUERY_TYPE[metric.value]
    _logger.debug('where assetId=%s, metric=%s, query_type=%s', mqid, metric.value, query_type.value)
    q = GsDataApi.build_market_data_query([mqid], query_type, source=source, real_time=real_time)
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    series = _extract_series_from_df(df, query_type)
    if query_type == QueryType.RATING:
        series.replace(['Buy', 'Sell', 'Neutral'], [1, -1, 0], inplace=True)
    return series


@plot_measure((AssetClass.FX,), (AssetType.Cross,), [MeasureDependency(
    id_provider=cross_to_usd_based_cross, query_type=QueryType.GIR_GSDEER_GSFEER)])
def gir_gsdeer_gsfeer(asset: Asset, metric: EquilibriumExchangeRateMetric = EquilibriumExchangeRateMetric.GSDEER, *,
                      source: str = None, real_time: bool = False) -> Series:
    """
    GSDEER and GSFEER quarterly estimates for currency fair values made by Global Investment Research (GIR)
    macro analysts.
    :param asset: asset object loaded from security master
    :param metric: Name of metric. One of gsdeer, gsfeer
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: gsdeer/gsfeer data of the asset for the field requested
    """
    if real_time:
        raise NotImplementedError('real-time gir_gsdeer_gsfeer not implemented')
    mqid = asset.get_marquee_id()
    usd_based_cross_mqid = cross_to_usd_based_cross(mqid)
    ds = Dataset('GSDEER_GSFEER')
    start_date = dt.date.today() - pd.tseries.offsets.BDay(1)
    df = ds.get_data(assetId=usd_based_cross_mqid, start_date=start_date)
    latest_date = df.index.max()
    df = df.loc[latest_date]
    df.index = df.apply(lambda x: dt.date(int(x.year), (int(x.quarter[-1]) - 1) * 3 + 1, 1), axis=1)
    series = _extract_series_from_df(df, metric)
    if mqid != usd_based_cross_mqid:
        series = 1 / series
        series.dataset_ids = getattr(df, 'dataset_ids', ())
    return series


@plot_measure((AssetClass.Equity,), (AssetType.Single_Stock,),
              [QueryType.GROWTH_SCORE, QueryType.FINANCIAL_RETURNS_SCORE,
               QueryType.MULTIPLE_SCORE, QueryType.INTEGRATED_SCORE])
def gir_factor_profile(asset: Asset, metric: _FactorProfileMetric, *, source: str = None,
                       real_time: bool = False) -> Series:
    """
    This dataset consists of Goldman Sachs Investment Profile ("IP") percentiles for US and Canadian securities
    covered by Goldman Sachs GIR analysts. Beginning in mid-2017, IP was renamed GS Factor Profile;
    the dataset provided hereunder refers to both IP and GS Factor Profile percentiles, and is referred
    to herein as "GS Factor Profile"
    Percentiles are generated daily, and historical values are available going back to January 1, 2009.
    :param asset: asset object loaded from security master
    :param metric: Growth Score, i.e. Growth percentile relative to Americas coverage universe
                   (a higher score means faster growth);
                   Financial Returns Score, i.e. Financial Returns percentile relative to Americas coverage universe
                   (a higher score means stronger financial returns);
                   Multiple Score, i.e. Multiple percentile relative to Americas coverage universe
                   (a higher score means more expensive);
                   Integrated Score, i.e. Average of the Growth, Financial Returns and (1-Multiple) percentile
                   (a higher score means more attractive)
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: Factor Profile data of the asset for the field requested
    """
    if real_time:
        raise NotImplementedError('real-time gir_factor_profile not implemented')

    mqid = asset.get_marquee_id()

    query_type = _FACTOR_PROFILE_METRIC_TO_QUERY_TYPE.get(metric.value)
    _logger.debug('where assetId=%s, metric=%s, query=%s', mqid, metric.value, query_type.value)
    q = GsDataApi.build_market_data_query([mqid], query_type, source=source, real_time=real_time)
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    series = _extract_series_from_df(df, query_type)

    return series


@plot_measure((AssetClass.Commod,), (AssetType.Commodity, AssetType.Index,), [QueryType.GIR_COMMODITIES_FORECAST])
def gir_commodities_forecast(asset: Asset,
                             forecastPeriod: _CommoditiesForecastPeriod = _CommoditiesForecastPeriod.THREE_MONTH,
                             forecastType: _CommoditiesForecastType = _CommoditiesForecastType.SPOT_RETURN, *,
                             source: str = None,
                             real_time: bool = False) -> Series:
    """
    Short and long-term commodities forecast.
    :param asset: asset object loaded from security master
    :param forecastPeriod: Relative, e.g. 3m, 6m, 12m; Quarterly (up to next two years), e.g. 2020Q3;
                            Annual (up to next ten years), e.g. 2023
    :param forecastType: Type of return for commodity indices. Spot for individual commodities.
                          One of spotReturn/totalReturn/rollReturn/spot
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: Forecast Value of the commodity or index as requested
    """
    if real_time:
        raise NotImplementedError('real-time rating not implemented')
    mqid = asset.get_marquee_id()
    query_type = QueryType.GIR_COMMODITIES_FORECAST
    _logger.debug('where assetId=%s, forecastPeriod=%s, forecastType=%s, query_type=%s',
                  mqid, forecastPeriod, forecastType, query_type.value)
    q = GsDataApi.build_market_data_query(
        [mqid],
        query_type,
        where=dict(forecastPeriod=str(forecastPeriod), forecastType=forecastType),
        source=source,
        real_time=real_time
    )
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    series = _extract_series_from_df(df, query_type)
    return series
