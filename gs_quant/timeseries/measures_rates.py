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

import logging
import re
from typing import Optional

import pandas as pd
from pandas import Series

from gs_quant.api.gs.assets import GsAssetApi
from gs_quant.api.gs.data import QueryType, GsDataApi
from gs_quant.data import DataContext
from gs_quant.errors import MqValueError
from gs_quant.markets.securities import AssetIdentifier, Asset
from gs_quant.target.common import Currency as CurrencyEnum, PricingLocation, AssetClass, AssetType, FieldFilterMap
from gs_quant.timeseries import ASSET_SPEC, BenchmarkType, plot_measure, MeasureDependency, GENERIC_DATE
from gs_quant.timeseries.helper import _to_offset
from gs_quant.timeseries.measures import _asset_from_spec, _market_data_timed, _range_from_pricing_date, \
    _get_custom_bd

_logger = logging.getLogger(__name__)

CURRENCY_TO_SWAP_RATE_BENCHMARK = {
    'CHF': {'LIBOR': 'CHF-LIBOR-BBA', 'SARON': 'CHF-SARON-OIS-COMPOUND'},
    'EUR': {'EURIBOR': 'EUR-EURIBOR-Telerate', 'EONIA': 'EUR-EONIA-OIS-COMPOUND'},
    'GBP': {'LIBOR': 'GBP-LIBOR-BBA', 'SONIA': 'GBP-SONIA-COMPOUND'},
    'JPY': {'LIBOR': 'JPY-LIBOR-BBA', 'TONA': 'JPY-TONA-OIS-COMPOUND'},
    'SEK': {'STIBOR': 'SEK-STIBOR-SIDE'},
    'USD': {'LIBOR': 'USD-LIBOR-BBA', 'Fed_Funds': 'USD-Federal Funds-H.15-OIS-COMP', 'SOFR': 'USD-SOFR-COMPOUND'}
}
BENCHMARK_TO_DEFAULT_FLOATING_RATE_TENORS = {
    'CHF-LIBOR-BBA': '6m',
    'CHF-SARON-OIS-COMPOUND': '1y',
    'EUR-EURIBOR-Telerate': '6m',
    'EUR-EONIA-OIS-COMPOUND': '1y',
    'GBP-LIBOR-BBA': '6m',
    'GBP-SONIA-COMPOUND': '1y',
    'JPY-LIBOR-BBA': '6m',
    'JPY-TONA-OIS-COMPOUND': '1y',
    'SEK-STIBOR-SIDE': '6m',
    'USD-LIBOR-BBA': '3m',
    'USD-Federal Funds-H.15-OIS-COMP': '1y',
    'USD-SOFR-COMPOUND': '1y'
}


def _currency_to_mdapi_swap_rate_asset(asset_spec: ASSET_SPEC) -> str:
    asset = _asset_from_spec(asset_spec)
    bbid = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)
    # for each currency, get a dummy asset for checking availability
    if bbid == 'CHF':
        result = 'MAW25BGQJH9P6DPT'
    elif bbid == 'EUR':
        result = 'MAA9MVX15AJNQCVG'
    elif bbid == 'GBP':
        result = 'MA6QCAP9B7ABS9HA'
    elif bbid == 'JPY':
        result = 'MAEE219J5ZP0ZKRK'
    elif bbid == 'SEK':
        result = 'MAETMVTPNP3199A5'
    elif bbid == 'USD':
        result = 'MAFRSWPAF5QPNTP2'
    else:
        return asset.get_marquee_id()
    return result


def _currency_to_mdapi_basis_swap_rate_asset(asset_spec: ASSET_SPEC) -> str:
    asset = _asset_from_spec(asset_spec)
    bbid = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)
    # for each currency, get a dummy asset for checking availability
    if bbid == 'EUR':
        result = 'MAGRG2VT11GQ2RQ9'
    elif bbid == 'GBP':
        result = 'MAHCYNB3V75JC5Q8'
    elif bbid == 'JPY':
        result = 'MAXVRBEZCJVH0C4V'
    elif bbid == 'USD':
        result = 'MAQB1PGEJFCET3GG'
    else:
        return asset.get_marquee_id()
    return result


def _convert_asset_for_mdapi_swap_rates(**kwargs) -> str:
    assets = GsAssetApi.get_many_assets(**kwargs)
    if len(assets) > 1:
        raise MqValueError('Specified arguments match multiple assets')
    elif len(assets) == 0:
        raise MqValueError('Specified arguments did not match any asset in the dataset')
    else:
        return assets[0].id


def _get_swap_leg_defaults(currency: CurrencyEnum, benchmark_type: BenchmarkType = None,
                           floating_rate_tenor: str = None) -> dict:
    if currency == CurrencyEnum.JPY:
        pricing_location = PricingLocation.TKO
    elif currency == CurrencyEnum.USD:
        pricing_location = PricingLocation.NYC
    else:
        pricing_location = PricingLocation.LDN

    # default benchmark types
    if benchmark_type is None:
        if currency == CurrencyEnum.EUR:
            benchmark_type = BenchmarkType.EURIBOR
        elif currency == CurrencyEnum.SEK:
            benchmark_type = BenchmarkType.STIBOR
        else:
            benchmark_type = BenchmarkType.LIBOR
    benchmark_type_input = CURRENCY_TO_SWAP_RATE_BENCHMARK[currency.value][benchmark_type.value]

    # default floating index
    if floating_rate_tenor is None:
        floating_rate_tenor = BENCHMARK_TO_DEFAULT_FLOATING_RATE_TENORS[benchmark_type_input]

    return dict(currency=currency, benchmark_type=benchmark_type_input,
                floating_rate_tenor=floating_rate_tenor, pricing_location=pricing_location)


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=_currency_to_mdapi_swap_rate_asset, query_type=QueryType.SWAP_RATE)])
def swap_rate_2(asset: Asset, swap_tenor: str, benchmark_type: BenchmarkType = None, floating_rate_tenor: str = None,
                forward_tenor: str = 'Spot', *, source: str = None,
                real_time: bool = False) -> Series:
    """
    GS end-of-day Fixed-Floating interest rate swap (IRS) curves across major currencies.


    :param asset: asset object loaded from security master
    :param swap_tenor: relative date representation of expiration date e.g. 1m
    :param benchmark_type: benchmark type e.g. LIBOR
    :param floating_rate_tenor: floating index rate
    :param forward_tenor: relative date representation of forward starting point eg: '1y' or 'Spot' for
    spot starting swaps
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: swap rate curve
    """
    if real_time:
        raise NotImplementedError('realtime swap_rate not implemented')
    currency = CurrencyEnum(asset.get_identifier(AssetIdentifier.BLOOMBERG_ID))

    if currency.value not in ['JPY', 'EUR', 'USD', 'GBP', 'CHF', 'SEK']:
        raise NotImplementedError('Data not available for {} swap rates'.format(currency.value))

    if benchmark_type is not None and \
            benchmark_type.value not in CURRENCY_TO_SWAP_RATE_BENCHMARK[currency.value].keys():
        raise MqValueError('%s is not supported for %s', benchmark_type, currency.value)

    defaults = _get_swap_leg_defaults(currency, benchmark_type, floating_rate_tenor)

    if not re.fullmatch('(\\d+)([bdwmy])', swap_tenor):
        raise MqValueError('invalid swap tenor ' + swap_tenor)

    if not re.fullmatch('(\\d+)([bdwmy])', floating_rate_tenor):
        raise MqValueError('invalid floating rate tenor ' + floating_rate_tenor)

    if forward_tenor is None or forward_tenor == 'Spot':
        forward_tenor = '0b'
    elif not re.fullmatch('(\\d+)([bdwmy])', forward_tenor):
        raise MqValueError('invalid forward tenor ' + forward_tenor)

    clearing_house = 'LCH'
    csaTerms = currency.value + '-1'
    fixed_rate = 'ATM'
    pay_or_receive = 'Receive'
    kwargs = dict(type='Swap', asset_parameters_termination_date=swap_tenor,
                  asset_parameters_floating_rate_option=defaults['benchmark_type'],
                  asset_parameters_fixed_rate=fixed_rate, asset_parameters_clearing_house=clearing_house,
                  asset_parameters_floating_rate_designated_maturity=defaults['floating_rate_tenor'],
                  asset_parameters_effective_date=forward_tenor, asset_parameters_pay_or_receive=pay_or_receive,
                  asset_parameters_notional_currency=currency.name, pricing_location=defaults['pricing_location'])

    rate_mqid = _convert_asset_for_mdapi_swap_rates(**kwargs)

    _logger.debug('where asset= %s, swap_tenor=%s, benchmark_type=%s, floating_rate_tenor=%s, forward_tenor=%s, '
                  'pricing_location=%s', rate_mqid, swap_tenor, defaults['benchmark_type'],
                  defaults['floating_rate_tenor'], forward_tenor, defaults['pricing_location'])
    where = FieldFilterMap(csaTerms=csaTerms)
    q = GsDataApi.build_market_data_query([rate_mqid], QueryType.SWAP_RATE, where=where, source=source,
                                          real_time=real_time)
    _logger.debug('q %s', q)
    df = _market_data_timed(q)

    return Series() if df.empty else df['swapRate']


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=_currency_to_mdapi_basis_swap_rate_asset,
                                 query_type=QueryType.BASIS_SWAP_RATE)])
def basis_swap_spread(asset: Asset, swap_tenor: str = '1y',
                      spread_benchmark_type: BenchmarkType = None, spread_tenor: str = None,
                      reference_benchmark_type: BenchmarkType = None, reference_tenor: str = None,
                      forward_tenor: str = 'Spot', *, source: str = None,
                      real_time: bool = False, ) -> Series:
    """
    GS end-of-day Floating-Floating interest rate swap (IRS) curves across major currencies.


    :param asset: asset object loaded from security master
    :param swap_tenor: relative date representation of expiration date e.g. 1m
    :param spread_benchmark_type: benchmark type of spread leg on which basis spread is added e.g. LIBOR
    :param spread_tenor: relative date representation of expiration date of paying leg e.g. 1m
    :param reference_benchmark_type: benchmark type of reference leg e.g. LIBOR
    :param reference_tenor: relative date representation of expiration date of reference leg e.g. 1m
    :param forward_tenor: relative date representation of forward starting point eg: '1y' or 'Spot' for Spot
            Starting swap
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: swap rate curve
    """
    if real_time:
        raise NotImplementedError('realtime basis_swap_rate not implemented')

    currency = CurrencyEnum(asset.get_identifier(AssetIdentifier.BLOOMBERG_ID))
    if currency.value not in ['JPY', 'EUR', 'USD', 'GBP']:
        raise NotImplementedError('Data not available for {} basis swap rates'.format(currency.value))

    for benchmark_type in [spread_benchmark_type, reference_benchmark_type]:
        if benchmark_type is not None and \
                benchmark_type.value not in CURRENCY_TO_SWAP_RATE_BENCHMARK[currency.value].keys():
            raise MqValueError('%s is not supported for %s', benchmark_type, currency.value)

    if not re.fullmatch('(\\d+)([bdwmy])', swap_tenor):
        raise MqValueError('invalid swap tenor ' + swap_tenor)

    for floating_rate_tenor in [spread_tenor, reference_tenor]:
        if not re.fullmatch('(\\d+)([bdwmy])', floating_rate_tenor):
            raise MqValueError('invalid floating rate tenor ' + floating_rate_tenor)

    # default benchmark types
    legs_w_defaults = dict()
    legs_w_defaults['spread'] = _get_swap_leg_defaults(currency, spread_benchmark_type, spread_tenor)
    legs_w_defaults['reference'] = _get_swap_leg_defaults(currency, reference_benchmark_type, reference_tenor)

    if forward_tenor is None or forward_tenor == 'Spot':
        forward_tenor = '0b'
    elif not re.fullmatch('(\\d+)([bdwmy])', forward_tenor):
        raise MqValueError('invalid forward tenor ' + forward_tenor)

    csaTerms = currency.value + '-1'
    clearing_house = 'LCH'

    kwargs = dict(type='BasisSwap', asset_parameters_termination_date=swap_tenor,
                  asset_parameters_payer_rate_option=legs_w_defaults['spread']['benchmark_type'],
                  asset_parameters_payer_designated_maturity=legs_w_defaults['spread']['floating_rate_tenor'],
                  asset_parameters_receiver_rate_option=legs_w_defaults['reference']['benchmark_type'],
                  asset_parameters_receiver_designated_maturity=legs_w_defaults['reference']['floating_rate_tenor'],
                  asset_parameters_clearing_house=clearing_house, asset_parameters_effective_date=forward_tenor,
                  asset_parameters_notional_currency=currency.name,
                  pricing_location=legs_w_defaults['spread']['pricing_location'])

    rate_mqid = _convert_asset_for_mdapi_swap_rates(**kwargs)

    _logger.debug('where asset=%s, swap_tenor=%s, spread_benchmark_type=%s, spread_tenor=%s, '
                  'reference_benchmark_type=%s, reference_tenor=%s, forward_tenor=%s, pricing_location=%s ',
                  rate_mqid, swap_tenor, legs_w_defaults['spread']['benchmark_type'],
                  legs_w_defaults['spread']['floating_rate_tenor'],
                  legs_w_defaults['reference']['benchmark_type'], legs_w_defaults['reference']['floating_rate_tenor'],
                  forward_tenor, legs_w_defaults['spread']['pricing_location'])

    where = FieldFilterMap(csaTerms=csaTerms)
    q = GsDataApi.build_market_data_query([rate_mqid], QueryType.BASIS_SWAP_RATE, where=where, source=source,
                                          real_time=real_time)
    _logger.debug('q %s', q)
    df = _market_data_timed(q)

    return Series() if df.empty else df['basisSwapRate']


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=_currency_to_mdapi_swap_rate_asset, query_type=QueryType.SWAP_RATE)])
def swap_term_structure(asset: Asset, benchmark_type: BenchmarkType = None, floating_rate_tenor: str = None,
                        forward_tenor: str = 'Spot', pricing_date: Optional[GENERIC_DATE] = None,
                        *, source: str = None, real_time: bool = False) -> Series:
    """
    GS end-of-day Fixed-Floating interest rate swap (IRS) term structure across major currencies.

    :param asset: asset object loaded from security master
    :param benchmark_type: benchmark type e.g. LIBOR
    :param floating_rate_tenor: floating index rate
    :param forward_tenor: relative date representation of forward starting point eg: '1y' or 'Spot' for spot
           starting swaps
    :param pricing_date: YYYY-MM-DD or relative date
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: swap rate term structure
    """
    if real_time:
        raise NotImplementedError('realtime swap_rate not implemented')

    currency = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)
    currency = CurrencyEnum(currency)
    if currency.value not in ['JPY', 'EUR', 'USD', 'GBP', 'CHF', 'SEK']:
        raise NotImplementedError('Data not available for {} swap rates'.format(currency.value))
    clearing_house = 'LCH'
    # put swap tenor check
    if benchmark_type is not None and \
            benchmark_type.value not in CURRENCY_TO_SWAP_RATE_BENCHMARK[currency.value].keys():
        raise MqValueError('%s is not supported for %s', benchmark_type, currency.value)

    defaults = _get_swap_leg_defaults(currency, benchmark_type, floating_rate_tenor)

    if not re.fullmatch('(\\d+)([bdwmy])', floating_rate_tenor):
        raise MqValueError('invalid floating rate tenor ' + floating_rate_tenor)

    if forward_tenor is None or forward_tenor == 'Spot':
        forward_tenor = '0b'
    elif not re.fullmatch('(\\d+)([bdwmy])', forward_tenor):
        raise MqValueError('invalid forward tenor ' + forward_tenor)

    csaTerms = currency.value + '-1'
    fixed_rate = 'ATM'
    pay_or_receive = 'Receive'
    kwargs = dict(type='Swap', asset_parameters_floating_rate_option=defaults['benchmark_type'],
                  asset_parameters_fixed_rate=fixed_rate, asset_parameters_clearing_house=clearing_house,
                  asset_parameters_floating_rate_designated_maturity=defaults['floating_rate_tenor'],
                  asset_parameters_effective_date=forward_tenor, asset_parameters_pay_or_receive=pay_or_receive,
                  asset_parameters_notional_currency=currency.name, pricing_location=defaults['pricing_location'])

    assets = GsAssetApi.get_many_assets(**kwargs)
    if len(assets) == 0:
        raise MqValueError('Specified arguments did not match any asset in the dataset')
    else:
        rate_mqids = [asset.id for asset in assets]

    asset_string = ''
    for mqid in rate_mqids:
        asset_string = asset_string + ',' + mqid
    _logger.debug('assets returned %s', asset_string)

    _logger.debug('where benchmark_type=%s, floating_rate_tenor=%s, forward_tenor=%s, '
                  'pricing_location=%s', defaults['benchmark_type'], defaults['floating_rate_tenor'],
                  forward_tenor, defaults['pricing_location'])

    start, end = _range_from_pricing_date(asset.exchange, pricing_date)
    with DataContext(start, end):
        where = FieldFilterMap(csaTerms=csaTerms)
        q = GsDataApi.build_market_data_query(rate_mqids, QueryType.SWAP_RATE, where=where,
                                              source=source, real_time=real_time)
        _logger.debug('q %s', q)
        df = _market_data_timed(q)

    if df.empty:
        return pd.Series()
    latest = df.index.max()
    _logger.info('selected pricing date %s', latest)
    df = df.loc[latest]
    business_day = _get_custom_bd(asset.exchange)
    df = df.assign(expirationDate=df.index + df['terminationTenor'].map(_to_offset) + business_day - business_day)
    df = df.set_index('expirationDate')
    df.sort_index(inplace=True)
    df = df.loc[DataContext.current.start_date: DataContext.current.end_date]
    return df['swapRate'] if not df.empty else pd.Series()


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=_currency_to_mdapi_basis_swap_rate_asset,
                                 query_type=QueryType.BASIS_SWAP_RATE)])
def basis_swap_term_structure(asset: Asset, spread_benchmark_type: BenchmarkType = None, spread_tenor: str = None,
                              reference_benchmark_type: BenchmarkType = None, reference_tenor: str = None,
                              forward_tenor: str = 'Spot', pricing_date: Optional[GENERIC_DATE] = None,
                              *, source: str = None, real_time: bool = False, ) -> Series:
    """
    GS end-of-day Floating-Floating interest rate swap (IRS) term structure across major currencies.


    :param asset: asset object loaded from security master
    :param spread_benchmark_type: benchmark type of spread leg on which basis spread is added e.g. LIBOR
    :param spread_tenor: relative date representation of expiration date of spread leg e.g. 1m
    :param reference_benchmark_type: benchmark type of reference leg e.g. LIBOR
    :param reference_tenor: relative date representation of expiration date of reference leg e.g. 1m
    :param forward_tenor: relative date representation of forward starting point eg: '1y'  or 'Spot' for spot
           starting swaps
    :param pricing_date: YYYY-MM-DD or relative date
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: swap rate curve
    """
    if real_time:
        raise NotImplementedError('realtime basis_swap_rate not implemented')

    currency = CurrencyEnum(asset.get_identifier(AssetIdentifier.BLOOMBERG_ID))
    if currency.value not in ['JPY', 'EUR', 'USD', 'GBP']:
        raise NotImplementedError('Data not available for {} basis swap rates'.format(currency.value))

    for benchmark_type in [spread_benchmark_type, reference_benchmark_type]:
        if benchmark_type is not None and \
                benchmark_type.value not in CURRENCY_TO_SWAP_RATE_BENCHMARK[currency.value].keys():
            raise MqValueError('%s is not supported for %s', benchmark_type, currency.value)

    for floating_rate_tenor in [spread_tenor, reference_tenor]:
        if not re.fullmatch('(\\d+)([bdwmy])', floating_rate_tenor):
            raise MqValueError('invalid floating rate tenor ' + floating_rate_tenor)

    if forward_tenor is None or forward_tenor == 'Spot':
        forward_tenor = '0b'
    elif not re.fullmatch('(\\d+)([bdwmy])', forward_tenor):
        raise MqValueError('invalid forward tenor ' + forward_tenor)

    # default benchmark types
    legs_w_defaults = dict()
    legs_w_defaults['spread'] = _get_swap_leg_defaults(currency, spread_benchmark_type, spread_tenor)
    legs_w_defaults['reference'] = _get_swap_leg_defaults(currency, reference_benchmark_type, reference_tenor)

    csaTerms = currency.value + '-1'
    clearing_house = 'LCH'

    kwargs = dict(type='BasisSwap', asset_parameters_payer_rate_option=legs_w_defaults['spread']['benchmark_type'],
                  asset_parameters_payer_designated_maturity=legs_w_defaults['spread']['floating_rate_tenor'],
                  asset_parameters_receiver_rate_option=legs_w_defaults['reference']['benchmark_type'],
                  asset_parameters_receiver_designated_maturity=legs_w_defaults['reference']['floating_rate_tenor'],
                  asset_parameters_clearing_house=clearing_house, asset_parameters_effective_date=forward_tenor,
                  asset_parameters_notional_currency=currency.name,
                  pricing_location=legs_w_defaults['spread']['pricing_location'])

    assets = GsAssetApi.get_many_assets(**kwargs)
    if len(assets) == 0:
        raise MqValueError('Specified arguments did not match any asset in the dataset')
    else:
        rate_mqids = [asset.id for asset in assets]

    asset_string = ''
    for mqid in rate_mqids:
        asset_string = asset_string + ',' + mqid
    _logger.debug('assets returned %s', asset_string)

    _logger.debug('where spread_benchmark_type=%s, spread_tenor=%s,  reference_benchmark_type=%s, '
                  'reference_tenor=%s, forward_tenor=%s, pricing_location=%s ',
                  legs_w_defaults['spread']['benchmark_type'], legs_w_defaults['spread']['floating_rate_tenor'],
                  legs_w_defaults['reference']['benchmark_type'], legs_w_defaults['reference']['floating_rate_tenor'],
                  forward_tenor, legs_w_defaults['spread']['pricing_location'])

    start, end = _range_from_pricing_date(assets[0].exchange, pricing_date)
    with DataContext(start, end):
        where = FieldFilterMap(csaTerms=csaTerms)
        q = GsDataApi.build_market_data_query(rate_mqids, QueryType.BASIS_SWAP_RATE, where=where,
                                              source=source, real_time=real_time)
        _logger.debug('q %s', q)
        df = _market_data_timed(q)
    if df.empty:
        return pd.Series()
    latest = df.index.max()
    _logger.info('selected pricing date %s', latest)
    df = df.loc[latest]
    business_day = _get_custom_bd(asset.exchange)
    df = df.assign(expirationDate=df.index + df['terminationTenor'].map(_to_offset) + business_day - business_day)
    df = df.set_index('expirationDate')
    df.sort_index(inplace=True)
    df = df.loc[DataContext.current.start_date: DataContext.current.end_date]
    return df['basisSwapRate'] if not df.empty else pd.Series()
