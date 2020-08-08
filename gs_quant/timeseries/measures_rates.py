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

import datetime
import logging
import re
from enum import Enum
from typing import Optional, Union, Dict

import pandas as pd
from pandas import Series
from gs_quant.api.gs.assets import GsAssetApi
from gs_quant.api.gs.data import QueryType, GsDataApi
from gs_quant.data import DataContext
from gs_quant.datetime.gscalendar import GsCalendar
from gs_quant.errors import MqValueError
from gs_quant.markets.securities import AssetIdentifier, Asset
from gs_quant.target.common import Currency as CurrencyEnum, PricingLocation, AssetClass, AssetType
from gs_quant.timeseries import ASSET_SPEC, BenchmarkType, plot_measure, MeasureDependency, GENERIC_DATE
from gs_quant.timeseries.helper import _to_offset
from gs_quant.timeseries.measures import _asset_from_spec, _market_data_timed, _range_from_pricing_date, \
    _get_custom_bd, ExtendedSeries

_logger = logging.getLogger(__name__)


class _ClearingHouse(Enum):
    LCH = 'LCH'
    EUREX = 'EUREX'
    JSCC = 'JSCC'
    CME = 'CME'


class _SwapTenorType(Enum):
    FORWARD_TENOR = 'forward_tenor'
    SWAP_TENOR = 'swap_tenor'


CURRENCY_TO_SWAP_RATE_BENCHMARK = {
    'CHF': {'LIBOR': 'CHF-LIBOR-BBA', 'SARON': 'CHF-SARON-OIS-COMPOUND'},
    'EUR': {'EURIBOR': 'EUR-EURIBOR-Telerate', 'EONIA': 'EUR-EONIA-OIS-COMPOUND', 'EUROSTR': 'EUR-EUROSTR-COMPOUND'},
    'GBP': {'LIBOR': 'GBP-LIBOR-BBA', 'SONIA': 'GBP-SONIA-COMPOUND'},
    'JPY': {'LIBOR': 'JPY-LIBOR-BBA', 'TONA': 'JPY-TONA-OIS-COMPOUND'},
    'SEK': {'STIBOR': 'SEK-STIBOR-SIDE'},
    'USD': {'LIBOR': 'USD-LIBOR-BBA', 'Fed_Funds': 'USD-Federal Funds-H.15-OIS-COMP', 'SOFR': 'USD-SOFR-COMPOUND'}
}
BENCHMARK_TO_DEFAULT_FLOATING_RATE_TENORS = {
    'CHF-LIBOR-BBA': '6m',
    'CHF-SARON-OIS-COMPOUND': '1y',
    'EUR-EURIBOR-Telerate': '6m',
    'EUR-EUROSTR-COMPOUND': '1y',
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


def _match_floating_tenors(swap_args) -> dict:
    payer_index = swap_args['asset_parameters_payer_rate_option']
    receiver_index = swap_args['asset_parameters_receiver_rate_option']

    if payer_index != receiver_index:
        if 'SOFR' in payer_index:
            swap_args['asset_parameters_payer_designated_maturity'] = swap_args[
                'asset_parameters_receiver_designated_maturity']
        elif 'SOFR' in receiver_index:
            swap_args['asset_parameters_receiver_designated_maturity'] = swap_args[
                'asset_parameters_payer_designated_maturity']
        elif 'LIBOR' in payer_index or 'EURIBOR' in payer_index or 'STIBOR' in payer_index:
            swap_args['asset_parameters_receiver_designated_maturity'] = swap_args[
                'asset_parameters_payer_designated_maturity']
        elif 'LIBOR' in receiver_index or 'EURIBOR' in receiver_index or 'STIBOR' in receiver_index:
            swap_args['asset_parameters_payer_designated_maturity'] = swap_args[
                'asset_parameters_receiver_designated_maturity']
    return swap_args


def _get_mdapi_rates_assets(**kwargs) -> Union[str, list]:
    assets = GsAssetApi.get_many_assets(**kwargs)
    # change order of basis swap legs and check if swap in dataset
    if len(assets) == 0 and ('asset_parameters_payer_rate_option' in kwargs):  # flip legs
        kwargs['asset_parameters_payer_rate_option'], kwargs['asset_parameters_receiver_rate_option'] = \
            kwargs['asset_parameters_receiver_rate_option'], kwargs['asset_parameters_payer_rate_option']
        kwargs['asset_parameters_payer_designated_maturity'], kwargs['asset_parameters_receiver_designated_maturity'] =\
            kwargs['asset_parameters_receiver_designated_maturity'], \
            kwargs['asset_parameters_payer_designated_maturity']

        assets = GsAssetApi.get_many_assets(**kwargs)

    if len(assets) > 1:
        # term structure measures need multiple assets
        if ('asset_parameters_termination_date' not in kwargs) or ('asset_parameters_effective_date' not in kwargs):
            return [asset.id for asset in assets]
        else:
            raise MqValueError('Specified arguments match multiple assets')
    elif len(assets) == 0:
        raise MqValueError('Specified arguments did not match any asset in the dataset')
    else:
        return assets[0].id


def _check_forward_tenor(forward_tenor) -> GENERIC_DATE:
    if isinstance(forward_tenor, datetime.date):
        return forward_tenor
    elif forward_tenor is None or forward_tenor in ['Spot', 'spot', 'SPOT']:
        return '0b'
    elif not (re.fullmatch('(\\d+)([bdwmy])', forward_tenor) or
              re.fullmatch('(imm[1-4]|frb[1-9]|ecb[1-6])', forward_tenor)):
        raise MqValueError('invalid forward tenor ' + forward_tenor)
    else:
        return forward_tenor


def _check_benchmark_type(currency, benchmark_type: Union[BenchmarkType, str]) -> BenchmarkType:
    if isinstance(benchmark_type, str):
        if benchmark_type.upper() in BenchmarkType.__members__:
            benchmark_type = BenchmarkType[benchmark_type.upper()]
        elif benchmark_type in ['fed_funds', 'Fed_Funds', 'FED_FUNDS']:
            benchmark_type = BenchmarkType.Fed_Funds
        elif benchmark_type in ['estr', 'ESTR', 'eurostr', 'EuroStr']:
            benchmark_type = BenchmarkType.EUROSTR
        else:
            raise MqValueError('%s is not valid, pick one among ' + ', '.join([x.value for x in BenchmarkType]))

    if isinstance(benchmark_type, BenchmarkType) and \
            benchmark_type.value not in CURRENCY_TO_SWAP_RATE_BENCHMARK[currency.value].keys():
        raise MqValueError('%s is not supported for %s', benchmark_type.value, currency.value)
    else:
        return benchmark_type


def _check_clearing_house(clearing_house: Union[_ClearingHouse, str]) -> _ClearingHouse:
    if isinstance(clearing_house, str) and clearing_house.upper() in _ClearingHouse.__members__:
        clearing_house = _ClearingHouse[clearing_house.upper()]

    if clearing_house is None:
        return _ClearingHouse.LCH
    elif isinstance(clearing_house, _ClearingHouse):
        return clearing_house
    else:
        raise MqValueError('invalid clearing house: ' + clearing_house + ' choose one among ' +
                           ', '.join([ch.value for ch in _ClearingHouse]))


def _check_tenor_type(tenor_type: _SwapTenorType) -> _SwapTenorType:
    if isinstance(tenor_type, str) and tenor_type.upper() in _SwapTenorType.__members__:
        tenor_type = _SwapTenorType[tenor_type.upper()]

    if tenor_type is None:
        return _SwapTenorType.FORWARD_TENOR
    elif isinstance(tenor_type, _SwapTenorType):
        return tenor_type
    else:
        raise MqValueError('invalid tenor_type: ' + tenor_type + ' choose one among ' +
                           ', '.join([ch.value for ch in _SwapTenorType]))


def _check_term_structure_tenor(tenor_type: _SwapTenorType, tenor: str) -> Dict:
    if tenor_type == _SwapTenorType.FORWARD_TENOR:
        tenor = _check_forward_tenor(tenor)
        tenor_to_plot = 'terminationTenor'
        tenor_dataset_field = 'asset_parameters_effective_date'
    elif not re.fullmatch('(\\d+)([bdwmy])', tenor) or re.fullmatch('(frb[1-9])', tenor):
        raise MqValueError('invalid swap tenor ' + tenor)
    else:
        tenor_to_plot = 'effectiveTenor'
        tenor_dataset_field = 'asset_parameters_termination_date'
    return dict(tenor=tenor, tenor_to_plot=tenor_to_plot, tenor_dataset_field=tenor_dataset_field)


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


def _get_swap_csa_terms(curr: str, benchmark_type: str) -> dict:
    euribor_index = CURRENCY_TO_SWAP_RATE_BENCHMARK['EUR'][BenchmarkType.EURIBOR.value]
    usd_libor_index = CURRENCY_TO_SWAP_RATE_BENCHMARK['USD'][BenchmarkType.LIBOR.value]
    estr_index = CURRENCY_TO_SWAP_RATE_BENCHMARK['EUR'][BenchmarkType.EUROSTR.value]
    if benchmark_type in [euribor_index, usd_libor_index]:
        return {}
    elif benchmark_type == estr_index:
        return dict(csaTerms=curr + '-EuroSTR')
    else:
        return dict(csaTerms=curr + '-1')


def _get_basis_swap_csa_terms(curr: str, payer_benchmark: str, receiver_benchmark: str) -> dict:
    benchmarks = [payer_benchmark, receiver_benchmark]
    euribor_index: str = CURRENCY_TO_SWAP_RATE_BENCHMARK['EUR'][BenchmarkType.EURIBOR.value]
    usd_libor_index: str = CURRENCY_TO_SWAP_RATE_BENCHMARK['USD'][BenchmarkType.LIBOR.value]
    estr_index: str = CURRENCY_TO_SWAP_RATE_BENCHMARK['EUR'][BenchmarkType.EUROSTR.value]
    if (euribor_index in benchmarks) or (usd_libor_index in benchmarks):
        return {}  # different csaTerms after SOFR and ESTR transitions for a given asset
    elif estr_index in benchmarks:
        return dict(csaTerms=curr + '-EuroSTR')
    else:
        return dict(csaTerms=curr + '-1')


def _get_swap_data(asset: Asset, swap_tenor: str, benchmark_type: str = None, floating_rate_tenor: str = None,
                   forward_tenor: Optional[GENERIC_DATE] = None, clearing_house: _ClearingHouse = None,
                   source: str = None, real_time: bool = False,
                   query_type: QueryType = QueryType.SWAP_RATE) -> pd.DataFrame:
    if real_time:
        raise NotImplementedError('realtime swap_rate not implemented')
    currency = CurrencyEnum(asset.get_identifier(AssetIdentifier.BLOOMBERG_ID))

    if currency.value not in ['JPY', 'EUR', 'USD', 'GBP', 'CHF', 'SEK']:
        raise NotImplementedError('Data not available for {} swap rates'.format(currency.value))
    benchmark_type = _check_benchmark_type(currency, benchmark_type)

    clearing_house = _check_clearing_house(clearing_house)
    defaults = _get_swap_leg_defaults(currency, benchmark_type, floating_rate_tenor)

    if not (re.fullmatch('(\\d+)([bdwmy])', swap_tenor) or re.fullmatch('(frb[1-9]|ecb[1-6])', forward_tenor)):
        raise MqValueError('invalid swap tenor ' + swap_tenor)

    if not re.fullmatch('(\\d+)([bdwmy])', defaults['floating_rate_tenor']):
        raise MqValueError('invalid floating rate tenor ' + defaults['floating_rate_tenor'] + ' for index: ' +
                           defaults['benchmark_type'])

    forward_tenor = _check_forward_tenor(forward_tenor)
    fixed_rate = 'ATM'
    kwargs = dict(type='Swap', asset_parameters_termination_date=swap_tenor,
                  asset_parameters_floating_rate_option=defaults['benchmark_type'],
                  asset_parameters_fixed_rate=fixed_rate, asset_parameters_clearing_house=clearing_house.value,
                  asset_parameters_floating_rate_designated_maturity=defaults['floating_rate_tenor'],
                  asset_parameters_effective_date=forward_tenor,
                  asset_parameters_notional_currency=currency.name, pricing_location=defaults['pricing_location'].value)

    rate_mqid = _get_mdapi_rates_assets(**kwargs)

    _logger.debug('where asset= %s, swap_tenor=%s, benchmark_type=%s, floating_rate_tenor=%s, forward_tenor=%s, '
                  'pricing_location=%s', rate_mqid, swap_tenor, defaults['benchmark_type'],
                  defaults['floating_rate_tenor'], forward_tenor, defaults['pricing_location'].value)
    where = _get_swap_csa_terms(currency.value, defaults['benchmark_type'])
    q = GsDataApi.build_market_data_query([rate_mqid], query_type, where=where, source=source,
                                          real_time=real_time)
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return df


def _get_term_struct_date(tenor: Union[str, datetime.datetime], index: datetime.datetime,
                          business_day) -> datetime.datetime:
    if isinstance(tenor, datetime.datetime):
        return tenor
    try:
        year, month, day = tenor.split('-')
        return datetime.datetime(int(year), int(month), int(day))
    except ValueError:
        if tenor == '0b':
            return index + business_day - business_day
        else:
            return index + _to_offset(tenor) + business_day - business_day


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=_currency_to_mdapi_swap_rate_asset, query_type=QueryType.SWAP_ANNUITY)])
def swap_annuity(asset: Asset, swap_tenor: str, benchmark_type: str = None, floating_rate_tenor: str = None,
                 forward_tenor: Optional[GENERIC_DATE] = None, clearing_house: _ClearingHouse = None, *,
                 source: str = None, real_time: bool = False) -> Series:
    """
    GS end-of-day Fixed-Floating interest rate swap(IRS) annuity values in years for paying leg across major currencies.


    :param asset: asset object loaded from security master
    :param swap_tenor: relative date representation of expiration date e.g. 1m
    :param benchmark_type: benchmark type e.g. LIBOR
    :param floating_rate_tenor: floating index rate
    :param forward_tenor: absolute / relative date representation of forward starting point eg: '1y' or 'Spot' for
            spot starting swaps, 'imm1' or 'frb1'
    :param clearing_house: Example - "LCH", "EUREX", "JSCC", "CME"
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: annuity of swap
    """
    df = _get_swap_data(asset=asset, swap_tenor=swap_tenor, benchmark_type=benchmark_type,
                        floating_rate_tenor=floating_rate_tenor, forward_tenor=forward_tenor,
                        clearing_house=clearing_house, source=source,
                        real_time=real_time, query_type=QueryType.SWAP_ANNUITY)

    series = ExtendedSeries() if df.empty else ExtendedSeries(abs(df['swapAnnuity'] * 1e4 / 1e8))
    series.dataset_ids = getattr(df, 'dataset_ids', ())
    return series


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=_currency_to_mdapi_swap_rate_asset, query_type=QueryType.SWAP_RATE)])
def swap_rate(asset: Asset, swap_tenor: str, benchmark_type: str = None, floating_rate_tenor: str = None,
              forward_tenor: Optional[GENERIC_DATE] = None, clearing_house: _ClearingHouse = None, *,
              source: str = None, real_time: bool = False) -> Series:
    """
    GS end-of-day Fixed-Floating interest rate swap (IRS) curves across major currencies.


    :param asset: asset object loaded from security master
    :param swap_tenor: relative date representation of expiration date e.g. 1m
    :param benchmark_type: benchmark type e.g. LIBOR
    :param floating_rate_tenor: floating index rate
    :param forward_tenor: absolute / relative date representation of forward starting point eg: '1y' or 'Spot' for
            spot starting swaps, 'imm1' or 'frb1'
    :param clearing_house: Example - "LCH", "EUREX", "JSCC", "CME"
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: swap rate curve
    """
    df = _get_swap_data(asset=asset, swap_tenor=swap_tenor, benchmark_type=benchmark_type,
                        floating_rate_tenor=floating_rate_tenor, forward_tenor=forward_tenor,
                        clearing_house=clearing_house, source=source,
                        real_time=real_time, query_type=QueryType.SWAP_RATE)

    series = ExtendedSeries() if df.empty else ExtendedSeries(df['swapRate'])
    series.dataset_ids = getattr(df, 'dataset_ids', ())
    return series


def _get_basis_swap_kwargs(asset: Asset, spread_benchmark_type: str = None, spread_tenor: str = None,
                           reference_benchmark_type: str = None, reference_tenor: str = None,
                           forward_tenor: Optional[GENERIC_DATE] = None, clearing_house: _ClearingHouse = None) -> dict:
    currency = CurrencyEnum(asset.get_identifier(AssetIdentifier.BLOOMBERG_ID))
    if currency.value not in ['JPY', 'EUR', 'USD', 'GBP']:
        raise NotImplementedError('Data not available for {} basis swap rates'.format(currency.value))

    clearing_house = _check_clearing_house(clearing_house)
    spread_benchmark_type = _check_benchmark_type(currency, spread_benchmark_type)
    reference_benchmark_type = _check_benchmark_type(currency, reference_benchmark_type)

    # default benchmark types
    legs_w_defaults = dict()
    legs_w_defaults['spread'] = _get_swap_leg_defaults(currency, spread_benchmark_type, spread_tenor)
    legs_w_defaults['reference'] = _get_swap_leg_defaults(currency, reference_benchmark_type, reference_tenor)

    for key, leg in legs_w_defaults.items():
        if not re.fullmatch('(\\d+)([bdwmy])', leg['floating_rate_tenor']):
            raise MqValueError('invalid floating rate tenor ' + leg['floating_rate_tenor'] + ' index: ' +
                               leg['benchmark_type'])

    forward_tenor = _check_forward_tenor(forward_tenor)
    kwargs = dict(type='BasisSwap', asset_parameters_payer_rate_option=legs_w_defaults['spread']['benchmark_type'],
                  asset_parameters_payer_designated_maturity=legs_w_defaults['spread']['floating_rate_tenor'],
                  asset_parameters_receiver_rate_option=legs_w_defaults['reference']['benchmark_type'],
                  asset_parameters_receiver_designated_maturity=legs_w_defaults['reference']['floating_rate_tenor'],
                  asset_parameters_clearing_house=clearing_house.value, asset_parameters_effective_date=forward_tenor,
                  asset_parameters_notional_currency=currency.name,
                  pricing_location=legs_w_defaults['spread']['pricing_location'].value)
    kwargs = _match_floating_tenors(kwargs)
    return kwargs


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=_currency_to_mdapi_basis_swap_rate_asset,
                                 query_type=QueryType.BASIS_SWAP_RATE)])
def basis_swap_spread(asset: Asset, swap_tenor: str = '1y',
                      spread_benchmark_type: str = None, spread_tenor: str = None,
                      reference_benchmark_type: str = None, reference_tenor: str = None,
                      forward_tenor: Optional[GENERIC_DATE] = None, clearing_house: _ClearingHouse = None, *,
                      source: str = None, real_time: bool = False, ) -> Series:
    """
    GS end-of-day Floating-Floating interest rate swap (IRS) curves across major currencies.


    :param asset: asset object loaded from security master
    :param swap_tenor: relative date representation of expiration date e.g. 1m
    :param spread_benchmark_type: benchmark type of spread leg on which basis spread is added e.g. LIBOR
    :param spread_tenor: relative date representation of expiration date of paying leg e.g. 1m
    :param reference_benchmark_type: benchmark type of reference leg e.g. LIBOR
    :param reference_tenor: relative date representation of expiration date of reference leg e.g. 1m
    :param forward_tenor: absolute / relative date representation of forward starting point eg: '1y' or 'Spot' for
            spot starting swaps, 'imm1' or 'frb1'
    :param clearing_house: Example - "LCH", "EUREX", "JSCC", "CME"
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: swap rate curve
    """
    if real_time:
        raise NotImplementedError('realtime basis_swap_rate not implemented')

    if not (re.fullmatch('(\\d+)([bdwmy])', swap_tenor) or re.fullmatch('(frb[1-9])', forward_tenor)):
        raise MqValueError('invalid swap tenor ' + swap_tenor)

    kwargs = _get_basis_swap_kwargs(asset=asset, spread_benchmark_type=spread_benchmark_type, spread_tenor=spread_tenor,
                                    reference_benchmark_type=reference_benchmark_type, reference_tenor=reference_tenor,
                                    forward_tenor=forward_tenor, clearing_house=clearing_house)
    kwargs['asset_parameters_termination_date'] = swap_tenor

    rate_mqid = _get_mdapi_rates_assets(**kwargs)
    _logger.debug('where asset=%s, swap_tenor=%s, spread_benchmark_type=%s, spread_tenor=%s, '
                  'reference_benchmark_type=%s, reference_tenor=%s, forward_tenor=%s, pricing_location=%s ',
                  rate_mqid, swap_tenor, kwargs['asset_parameters_payer_rate_option'],
                  kwargs['asset_parameters_payer_designated_maturity'], kwargs['asset_parameters_receiver_rate_option'],
                  kwargs['asset_parameters_receiver_designated_maturity'],
                  kwargs['asset_parameters_effective_date'], kwargs['pricing_location'])

    where = _get_basis_swap_csa_terms(kwargs['asset_parameters_notional_currency'],
                                      kwargs['asset_parameters_payer_rate_option'],
                                      kwargs['asset_parameters_receiver_rate_option'])

    q = GsDataApi.build_market_data_query([rate_mqid], QueryType.BASIS_SWAP_RATE, where=where,
                                          source=source, real_time=real_time)
    _logger.debug('q %s', q)
    df = _market_data_timed(q)

    series = ExtendedSeries() if df.empty else ExtendedSeries(df['basisSwapRate'])
    series.dataset_ids = getattr(df, 'dataset_ids', ())
    return series


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=_currency_to_mdapi_swap_rate_asset, query_type=QueryType.SWAP_RATE)])
def swap_term_structure(asset: Asset, benchmark_type: str = None, floating_rate_tenor: str = None,
                        tenor_type: _SwapTenorType = None, tenor: Optional[GENERIC_DATE] = None,
                        clearing_house: _ClearingHouse = None, pricing_date: Optional[GENERIC_DATE] = None,
                        *, source: str = None, real_time: bool = False) -> Series:
    """
    GS end-of-day Fixed-Floating interest rate swap (IRS) term structure across major currencies.

    :param asset: asset object loaded from security master
    :param benchmark_type: benchmark type e.g. LIBOR
    :param floating_rate_tenor: floating index rate
    :param tenor_type: specify which tenor should be fixed, SWAP_TENOR or FORWARD_TENOR
    :param tenor: absolute / relative date representation of forward starting point or swap maturity
    :param clearing_house: Example - "LCH", "EUREX", "JSCC", "CME"
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

    clearing_house = _check_clearing_house(clearing_house)
    benchmark_type = _check_benchmark_type(currency, benchmark_type)
    tenor_type = _check_tenor_type(tenor_type)
    tenor_dict = _check_term_structure_tenor(tenor_type=tenor_type, tenor=tenor)
    defaults = _get_swap_leg_defaults(currency, benchmark_type, floating_rate_tenor)

    if not re.fullmatch('(\\d+)([bdwmy])', defaults['floating_rate_tenor']):
        raise MqValueError('invalid floating rate tenor ' + defaults['floating_rate_tenor'] + ' for index: ' +
                           defaults['benchmark_type'])

    calendar = defaults['pricing_location'].value
    if pricing_date is not None and pricing_date in list(GsCalendar.get(calendar).holidays):
        raise MqValueError('Specified pricing date is a holiday in {} calendar'.format(calendar))

    fixed_rate = 'ATM'
    kwargs = dict(type='Swap', asset_parameters_floating_rate_option=defaults['benchmark_type'],
                  asset_parameters_fixed_rate=fixed_rate, asset_parameters_clearing_house=clearing_house.value,
                  asset_parameters_floating_rate_designated_maturity=defaults['floating_rate_tenor'],
                  asset_parameters_notional_currency=currency.name, pricing_location=defaults['pricing_location'].value)
    kwargs[tenor_dict['tenor_dataset_field']] = tenor_dict['tenor']
    rate_mqids = _get_mdapi_rates_assets(**kwargs)
    if isinstance(rate_mqids, str):
        rate_mqids = [rate_mqids]
    _logger.debug('assets returned %s', ', '.join(rate_mqids))
    _logger.debug('where benchmark_type=%s, floating_rate_tenor=%s, %s=%s, '
                  'pricing_location=%s', defaults['benchmark_type'], defaults['floating_rate_tenor'], tenor_type.value,
                  tenor_dict['tenor'], defaults['pricing_location'].value)
    where = _get_swap_csa_terms(currency.value, defaults['benchmark_type'])
    start, end = _range_from_pricing_date(calendar, pricing_date)
    with DataContext(start, end):
        q = GsDataApi.build_market_data_query(rate_mqids, QueryType.SWAP_RATE, where=where,
                                              source=source, real_time=real_time)
        _logger.debug('q %s', q)
        df = _market_data_timed(q)

    if df.empty:
        series = ExtendedSeries()
    else:
        latest = df.index.max()
        _logger.info('selected pricing date %s', latest)
        df = df.loc[latest]
        biz_day = _get_custom_bd(calendar)
        col_to_plot = tenor_dict['tenor_to_plot']
        if isinstance(df, pd.Series):
            series = ExtendedSeries(pd.Series(df['swapRate'],
                                              index=[_get_term_struct_date(df[col_to_plot], latest, biz_day)]))
            series = series.loc[DataContext.current.start_date: DataContext.current.end_date]
        else:
            if col_to_plot == 'effectiveTenor':
                df = df[~df[col_to_plot].isin(['imm1', 'imm2', 'imm3', 'imm4'])]
            df['expirationDate'] = df[col_to_plot].apply(_get_term_struct_date, args=(latest, biz_day))
            df = df.set_index('expirationDate')
            df.sort_index(inplace=True)
            df = df.loc[DataContext.current.start_date: DataContext.current.end_date]
            series = ExtendedSeries() if df.empty else ExtendedSeries(df['swapRate'])
    series.dataset_ids = getattr(df, 'dataset_ids', ())
    return series


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=_currency_to_mdapi_basis_swap_rate_asset,
                                 query_type=QueryType.BASIS_SWAP_RATE)])
def basis_swap_term_structure(asset: Asset, spread_benchmark_type: str = None, spread_tenor: str = None,
                              reference_benchmark_type: str = None, reference_tenor: str = None,
                              tenor_type: _SwapTenorType = None, tenor: Optional[GENERIC_DATE] = None,
                              clearing_house: _ClearingHouse = None,
                              pricing_date: Optional[GENERIC_DATE] = None,
                              *, source: str = None, real_time: bool = False, ) -> Series:
    """
    GS end-of-day Floating-Floating interest rate swap (IRS) term structure across major currencies.


    :param asset: asset object loaded from security master
    :param spread_benchmark_type: benchmark type of spread leg on which basis spread is added e.g. LIBOR
    :param spread_tenor: relative date representation of expiration date of spread leg e.g. 1m
    :param reference_benchmark_type: benchmark type of reference leg e.g. LIBOR
    :param reference_tenor: relative date representation of expiration date of reference leg e.g. 1m
    :param tenor_type: specify which tenor should be fixed, SWAP_TENOR or FORWARD_TENOR
    :param tenor: absolute / relative date representation of forward starting point or swap maturity
    :param clearing_house: Example - "LCH", "EUREX", "JSCC", "CME"
    :param pricing_date: YYYY-MM-DD or relative date
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: swap rate curve
    """
    if real_time:
        raise NotImplementedError('realtime basis_swap_rate not implemented')
    tenor_type = _check_tenor_type(tenor_type)
    tenor_dict = _check_term_structure_tenor(tenor_type=tenor_type, tenor=tenor)
    kwargs = _get_basis_swap_kwargs(asset=asset, spread_benchmark_type=spread_benchmark_type, spread_tenor=spread_tenor,
                                    reference_benchmark_type=reference_benchmark_type, reference_tenor=reference_tenor,
                                    clearing_house=clearing_house)
    kwargs[tenor_dict['tenor_dataset_field']] = tenor_dict['tenor']
    calendar = kwargs['pricing_location']
    if pricing_date is not None and pricing_date in list(GsCalendar.get(calendar).holidays):
        raise MqValueError('Specified pricing date is a holiday in {} calendar'.format(calendar))

    rate_mqids = _get_mdapi_rates_assets(**kwargs)
    if isinstance(rate_mqids, str):  # single asset returned
        rate_mqids = [rate_mqids]
    _logger.debug('assets returned %s', ', '.join(rate_mqids))
    _logger.debug('where spread_benchmark_type=%s, spread_tenor=%s,  reference_benchmark_type=%s, '
                  'reference_tenor=%s, %s=%s, pricing_location=%s ',
                  kwargs['asset_parameters_payer_rate_option'], kwargs['asset_parameters_payer_designated_maturity'],
                  kwargs['asset_parameters_receiver_rate_option'],
                  kwargs['asset_parameters_receiver_designated_maturity'],
                  kwargs[tenor_dict['tenor_dataset_field']], tenor_dict['tenor'], kwargs['pricing_location'])

    where = _get_basis_swap_csa_terms(kwargs['asset_parameters_notional_currency'],
                                      kwargs['asset_parameters_payer_rate_option'],
                                      kwargs['asset_parameters_receiver_rate_option'])
    start, end = _range_from_pricing_date(calendar, pricing_date)
    with DataContext(start, end):
        q = GsDataApi.build_market_data_query(rate_mqids, QueryType.BASIS_SWAP_RATE, where=where,
                                              source=source, real_time=real_time)
        _logger.debug('q %s', q)
        df = _market_data_timed(q)

    if df.empty:
        series = ExtendedSeries()
    else:
        latest = df.index.max()
        _logger.info('selected pricing date %s', latest)
        df = df.loc[latest]
        biz_day = _get_custom_bd(calendar)
        col_to_plot = tenor_dict['tenor_to_plot']
        if isinstance(df, pd.Series):  # single asset returned
            series = ExtendedSeries(pd.Series(df['basisSwapRate'],
                                              index=[_get_term_struct_date(df[col_to_plot], latest, biz_day)]))
            series = series.loc[DataContext.current.start_date: DataContext.current.end_date]
        else:
            if col_to_plot == 'effectiveTenor':  # for forward term structure imm date assets
                df = df[~df[col_to_plot].isin(['imm1', 'imm2', 'imm3', 'imm4'])]
            df['expirationDate'] = df[col_to_plot].apply(_get_term_struct_date, args=(latest, biz_day))
            df = df.set_index('expirationDate')
            df.sort_index(inplace=True)
            df = df.loc[DataContext.current.start_date: DataContext.current.end_date]
            series = ExtendedSeries() if df.empty else ExtendedSeries(df['basisSwapRate'])
    series.dataset_ids = getattr(df, 'dataset_ids', ())
    return series
