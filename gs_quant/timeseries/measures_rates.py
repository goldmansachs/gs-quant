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
from collections import OrderedDict
from enum import Enum
from typing import Optional, Union, Dict

import pandas as pd
from gs_quant.target.common import Currency as CurrencyEnum, AssetClass, AssetType, PricingLocation
from pandas import Series

from gs_quant.api.gs.assets import GsAssetApi
from gs_quant.api.gs.data import QueryType, GsDataApi
from gs_quant.data import DataContext
from gs_quant.datetime.gscalendar import GsCalendar
from gs_quant.errors import MqValueError
from gs_quant.markets.securities import AssetIdentifier, Asset
from gs_quant.timeseries import ASSET_SPEC, BenchmarkType, plot_measure, MeasureDependency, GENERIC_DATE
from gs_quant.timeseries.helper import _to_offset
from gs_quant.timeseries.measures import _asset_from_spec, _market_data_timed, _range_from_pricing_date, \
    _get_custom_bd, ExtendedSeries, SwaptionTenorType, _extract_series_from_df

_logger = logging.getLogger(__name__)


# TODO: Use gs_quant object
class _ClearingHouse(Enum):
    LCH = 'LCH'
    EUREX = 'EUREX'
    JSCC = 'JSCC'
    CME = 'CME'
    NONE = 'NONE'


class _SwapTenorType(Enum):
    FORWARD_TENOR = 'forward_tenor'
    SWAP_TENOR = 'swap_tenor'


class TdapiRatesDefaultsProvider():
    # flag to indicate that a given property should not  be included in asset query
    EMPTY_PROPERTY = "null"

    def __init__(self, defaults: dict):
        self.defaults = defaults
        benchmark_mappings = {}
        for k, v in defaults.get("CURRENCIES").items():
            for e in v:
                benchmark_mappings[k] = {e.get("benchmarkType"): e.get('floatingRateOption')}
        self.defaults['MAPPING'] = benchmark_mappings

    def is_supported(self, currency: CurrencyEnum):
        return currency.value in self.defaults.get("CURRENCIES").keys()

    def get_floating_rate_option_for_benchmark(self, currency: CurrencyEnum, benchmark: str):
        return self.defaults.get("MAPPING").get(currency.value).get(benchmark)

    def get_swaption_parameter(self, currency, field, value=None):
        if value == self.EMPTY_PROPERTY:
            return None
        if value is not None:
            return value
        if isinstance(currency, str):
            currency_name = currency
        else:
            currency_name = currency.value
        for entry in [self.defaults.get("CURRENCIES").get(currency_name)[0], self.defaults.get("COMMON")]:
            if field in entry:
                value = entry[field][0] if isinstance(entry[field], list) else entry[field]
        return value


SWAPTION_DEFAULTS = {
    "CURRENCIES": {
        "EUR": [
            {"benchmarkType": "LIBOR", "floatingRateOption": "EUR-EURIBOR-TELERATE", "floatingRateTenor": ["6m", "3m"],
             "assetIdForAvailabilityCheck": "MAZB3PAH8JFVVT80",
             "pricingLocation": ["LDN"]}],
        "USD": [{"benchmarkType": "LIBOR", "floatingRateOption": "USD-LIBOR-BBA", "floatingRateTenor": ["3m", "6m"],
                 "assetIdForAvailabilityCheck": "MAY0X3KRD4AN77E2",
                 "strikeReference": ["ATM"],
                 "pricingLocation": ["NYC"]}],
        "GBP": [{"benchmarkType": "LIBOR", "floatingRateOption": "GBP-LIBOR-BBA", "floatingRateTenor": ["6m", "3m"],
                 "assetIdForAvailabilityCheck": "MAX2SBXZRPYR3NTY",
                 "pricingLocation": ["LDN"]}],
        "AUD": [{"benchmarkType": "BBR", "floatingRateOption": "AUD-BBR-BBSW", "floatingRateTenor": ["6m", "3m"],
                 "assetIdForAvailabilityCheck": "MAQHSC1PAF4X5H4B",
                 "pricingLocation": ["TKO"]}],
        "JPY": [{"benchmarkType": "LIBOR", "floatingRateOption": "JPY-LIBOR-BBA", "floatingRateTenor": ["6m"],
                 "assetIdForAvailabilityCheck": "MATT7CA7PRA4B8YB",
                 "pricingLocation": ["TKO"], }]
    },
    "COMMON": {
        "strikeReference": "ATM",
        "clearingHouse": "LCH",
        "terminationTenor": "5y",
        "expirationTenor": "1y",
        "effectiveDate": "0b"
    }
}
swaptions_defaults_provider = TdapiRatesDefaultsProvider(SWAPTION_DEFAULTS)

CURRENCY_TO_SWAP_RATE_BENCHMARK = {
    'CHF': OrderedDict([('LIBOR', 'CHF-LIBOR-BBA'), ('SARON', 'CHF-SARON-OIS-COMPOUND')]),
    'EUR': OrderedDict([('EURIBOR', 'EUR-EURIBOR-TELERATE'), ('EONIA', 'EUR-EONIA-OIS-COMPOUND'),
                        ('EUROSTR', 'EUR-EUROSTR-COMPOUND')]),
    'GBP': OrderedDict([('LIBOR', 'GBP-LIBOR-BBA'), ('SONIA', 'GBP-SONIA-COMPOUND')]),
    'JPY': OrderedDict([('LIBOR', 'JPY-LIBOR-BBA'), ('TONA', 'JPY-TONA-OIS-COMPOUND')]),
    'USD': OrderedDict(
        [('LIBOR', 'USD-LIBOR-BBA'), ('Fed_Funds', 'USD-Federal Funds-H.15-OIS-COMP'), ('SOFR', 'USD-SOFR-COMPOUND')]),
    'SEK': {'STIBOR': 'SEK-STIBOR-SIDE'},
    'NOK': {'NIBOR': 'NOK-NIBOR-BBA'},
    'DKK': {'CIBOR': 'DKK-CIBOR2-DKNA13'},
    'AUD': {'BBR': 'AUD-BBR-BBSW'},
    'CAD': {'CDOR': 'CAD-BA-CDOR'},
    'NZD': {'BBR': 'NZD-BBR-FRA'},
    'KRW': {'KSDA': 'KRW-CD-KSDA-BLOOMBERG'},
    'CNY': {'REPO': 'CNY-REPO RATE'},
    'SGD': {'SOR': 'SGD-SOR-VWAP'},
    'HKD': {'HIBOR': 'HKD-HIBOR-HKAB'},
    'INR': {'MIBOR': 'INR-MIBOR-OIS-COMPOUND'}
}
# TODO Join into single object.
BENCHMARK_TO_DEFAULT_FLOATING_RATE_TENORS = {
    'CHF-LIBOR-BBA': '6m',
    'CHF-SARON-OIS-COMPOUND': '1y',
    'EUR-EURIBOR-TELERATE': '6m',
    'EUR-EUROSTR-COMPOUND': '1y',
    'EUR-EONIA-OIS-COMPOUND': '1y',
    'GBP-LIBOR-BBA': '6m',
    'GBP-SONIA-COMPOUND': '1y',
    'JPY-LIBOR-BBA': '6m',
    'JPY-TONA-OIS-COMPOUND': '1y',
    'SEK-STIBOR-SIDE': '6m',
    'USD-LIBOR-BBA': '3m',
    'USD-Federal Funds-H.15-OIS-COMP': '1y',
    'USD-SOFR-COMPOUND': '1y',
    'NOK-NIBOR-BBA': '6m',
    'DKK-CIBOR2-DKNA13': '6m',
    'AUD-BBR-BBSW': '6m',
    'CAD-BA-CDOR': '3m',
    'NZD-BBR-FRA': '3m',
    'KRW-CD-KSDA-BLOOMBERG': '3m',
    'CNY-REPO RATE': '1w',
    'SGD-SOR-VWAP': '6m',
    'HKD-HIBOR-HKAB': '3m',
    'INR-MIBOR-OIS-COMPOUND': '6m',

}
CURRENCY_TO_PRICING_LOCATION = {
    CurrencyEnum.JPY: PricingLocation.TKO,
    CurrencyEnum.USD: PricingLocation.NYC,
    CurrencyEnum.AUD: PricingLocation.TKO,
    CurrencyEnum.NZD: PricingLocation.TKO,
    CurrencyEnum.INR: PricingLocation.HKG,
    CurrencyEnum.KRW: PricingLocation.HKG,
    CurrencyEnum.HKD: PricingLocation.HKG,
    CurrencyEnum.SGD: PricingLocation.HKG,
    CurrencyEnum.CAD: PricingLocation.NYC,
    CurrencyEnum.CNY: PricingLocation.HKG,

}

CURRENCY_TO_DUMMY_SWAP_BBID = {
    'CHF': 'MAW25BGQJH9P6DPT',
    'EUR': 'MAA9MVX15AJNQCVG',
    'GBP': 'MA6QCAP9B7ABS9HA',
    'JPY': 'MAEE219J5ZP0ZKRK',
    'SEK': 'MAETMVTPNP3199A5',
    'USD': 'MAFRSWPAF5QPNTP2',
    'DKK': 'MAF131NKWVRESFYA',
    'NOK': 'MA25DW5ZGC1BSC8Y',
    'HKD': 'MABRNGY8XRFVC36N',
    'NZD': 'MAH16NHE1HBN0FBZ',
    'AUD': 'MAY8147CRK0ZP53B',
    'CNY': 'MA4K1D8HH2R0RQY5',
    'CAD': 'MANJ8SS88WJ6N28Q',
    'KRW': 'MAP55AXG5SQVS6C5',
    'INR': 'MA20JHJXN1PD5HGE',
    'SGD': 'MA5CQFHYBPH9E5BS'
}


def _currency_to_tdapi_swap_rate_asset(asset_spec: ASSET_SPEC) -> str:
    asset = _asset_from_spec(asset_spec)
    bbid = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)
    # for each currency, get a dummy asset for checking availability
    result = CURRENCY_TO_DUMMY_SWAP_BBID.get(bbid, asset.get_marquee_id())
    return result


def _currency_to_tdapi_swaption_rate_asset(asset_spec: ASSET_SPEC) -> str:
    asset = _asset_from_spec(asset_spec)
    bbid = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)
    if bbid is None:
        return asset.get_marquee_id()
    try:
        result = swaptions_defaults_provider.get_swaption_parameter(bbid, "assetIdForAvailabilityCheck")
    except TypeError:
        logging.info("No assetIdForAvailabilityCheck for" + bbid)
        return asset.get_marquee_id()
    return result


def _currency_to_tdapi_basis_swap_rate_asset(asset_spec: ASSET_SPEC) -> str:
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


def _get_tdapi_rates_assets(allow_many=False, **kwargs) -> Union[str, list]:
    assets = GsAssetApi.get_many_assets(**kwargs)
    # change order of basis swap legs and check if swap in dataset
    if len(assets) == 0 and ('asset_parameters_payer_rate_option' in kwargs):  # flip legs
        kwargs['asset_parameters_payer_rate_option'], kwargs['asset_parameters_receiver_rate_option'] = \
            kwargs['asset_parameters_receiver_rate_option'], kwargs['asset_parameters_payer_rate_option']

        kwargs['asset_parameters_payer_designated_maturity'], kwargs[
            'asset_parameters_receiver_designated_maturity'] = \
            kwargs['asset_parameters_receiver_designated_maturity'], kwargs[
                'asset_parameters_payer_designated_maturity']

        assets = GsAssetApi.get_many_assets(**kwargs)

    if len(assets) > 1:
        # term structure measures need multiple assets
        if ('asset_parameters_termination_date' not in kwargs) or (
                'asset_parameters_effective_date' not in kwargs) or allow_many:
            return [asset.id for asset in assets]
        else:
            raise MqValueError('Specified arguments match multiple assets')
    elif len(assets) == 0:
        raise MqValueError('Specified arguments did not match any asset in the dataset' + str(kwargs))
    else:
        return assets[0].id


def _check_forward_tenor(forward_tenor) -> GENERIC_DATE:
    if isinstance(forward_tenor, datetime.date):
        return forward_tenor
    elif forward_tenor in ['Spot', 'spot', 'SPOT']:
        return '0b'
    elif not (_is_valid_relative_date_tenor(forward_tenor) or
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
    pricing_location = CURRENCY_TO_PRICING_LOCATION.get(currency, PricingLocation.LDN)
    # default benchmark types
    if benchmark_type is None:
        if currency == CurrencyEnum.EUR:
            benchmark_type = BenchmarkType.EURIBOR
        elif currency == CurrencyEnum.SEK:
            benchmark_type = BenchmarkType.STIBOR
        else:
            benchmark_type = BenchmarkType(str(list(CURRENCY_TO_SWAP_RATE_BENCHMARK[currency.value].keys())[0]))
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

    if currency.value not in CURRENCY_TO_SWAP_RATE_BENCHMARK.keys():
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
                  asset_parameters_notional_currency=currency.name)

    rate_mqid = _get_tdapi_rates_assets(**kwargs)

    _logger.debug('where asset= %s, swap_tenor=%s, benchmark_type=%s, floating_rate_tenor=%s, forward_tenor=%s, '
                  'pricing_location=%s', rate_mqid, swap_tenor, defaults['benchmark_type'],
                  defaults['floating_rate_tenor'], forward_tenor, defaults['pricing_location'].value)
    q = GsDataApi.build_market_data_query([rate_mqid], query_type, source=source,
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
              [MeasureDependency(id_provider=_currency_to_tdapi_swap_rate_asset, query_type=QueryType.SWAP_ANNUITY)])
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
              [MeasureDependency(id_provider=_currency_to_tdapi_swap_rate_asset,
                                 query_type=QueryType.SWAPTION_PREMIUM)])
def swaption_premium(asset: Asset, expiration_tenor: str = None, termination_tenor: str = None,
                     relative_strike: str = None, benchmark_type: str = None,
                     floating_rate_tenor: str = None,
                     clearing_house: str = None, *, source: str = None,
                     real_time: bool = False) -> Series:
    """
    GS end-of-day premium for swaption.

    :param asset: asset object loaded from security master
    :param expiration_tenor: relative date representation of expiration date on the option e.g. 3m
    :param termination_tenor: relative date representation of the instrument's expiration date e.g. 1y
    :param relative_strike: strike level relative to at the money e.g. 10 or ATM+10
    :param benchmark_type: benchmark type e.g. LIBOR
    :param floating_rate_tenor: floating index rate
    :param clearing_house: Example - "LCH", "EUREX", "JSCC", "CME"
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: swaption implied normal volatility curve
    """
    df = _get_swaption_measure(asset, benchmark_type, floating_rate_tenor, "0b", expiration_tenor,
                               termination_tenor, relative_strike, clearing_house, source=source, real_time=real_time,
                               start=DataContext.current.start_date, end=DataContext.current.end_date,
                               query_type=QueryType.SWAPTION_PREMIUM)

    return _extract_series_from_df(df, QueryType.SWAPTION_PREMIUM)


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=_currency_to_tdapi_swaption_rate_asset,
                                 query_type=QueryType.SWAPTION_ANNUITY)])
def swaption_annuity(asset: Asset, expiration_tenor: str = None, termination_tenor: str = None,
                     relative_strike: float = None, benchmark_type: str = None,
                     floating_rate_tenor: str = None,
                     clearing_house: str = None, *, source: str = None,
                     real_time: bool = False) -> Series:
    """
    GS end-of-day annuity for swaption.

    :param asset: asset object loaded from security master
    :param expiration_tenor: relative date representation of expiration date on the option e.g. 3m
    :param termination_tenor: relative date representation of the instrument's expiration date e.g. 1y
    :param relative_strike: strike level relative to at the money e.g. 10 or ATM+10
    :param benchmark_type: benchmark type e.g. LIBOR
    :param floating_rate_tenor: floating index rate
    :param clearing_house: Example - "LCH", "EUREX", "JSCC", "CME"
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: swaption implied normal volatility curve
    """

    df = _get_swaption_measure(asset, benchmark_type, floating_rate_tenor, "0b", expiration_tenor,
                               termination_tenor, relative_strike, clearing_house, source=source, real_time=real_time,
                               start=DataContext.current.start_date, end=DataContext.current.end_date,
                               query_type=QueryType.SWAPTION_ANNUITY)
    return _extract_series_from_df(df, QueryType.SWAPTION_ANNUITY)


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=_currency_to_tdapi_swaption_rate_asset,
                                 query_type=QueryType.MIDCURVE_PREMIUM)])
def midcurve_premium(asset: Asset, expiration_tenor: str, forward_tenor: str, termination_tenor: str,
                     relative_strike: float = None, benchmark_type: str = None,
                     floating_rate_tenor: str = None,
                     clearing_house: str = None, *, source: str = None,
                     real_time: bool = False) -> Series:
    """
    GS end-of-day premium for midcurve

    :param asset: asset object loaded from security master
    :param expiration_tenor: relative date representation of expiration date on the option e.g. 3m
    :param forward_tenor: relative date representation of swap's start date after option expiry e.g. 2y
    :param termination_tenor: relative date representation of the instrument's expiration date e.g. 1y
    :param relative_strike: strike level relative to at the money e.g. 10 or ATM+10
    :param benchmark_type: benchmark type e.g. LIBOR
    :param floating_rate_tenor: floating index rate
    :param clearing_house: Example - "LCH", "EUREX", "JSCC", "CME"
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: swaption implied normal volatility curve
    """

    df = _get_swaption_measure(asset, benchmark_type, floating_rate_tenor, forward_tenor, expiration_tenor,
                               termination_tenor, relative_strike, clearing_house, source=source, real_time=real_time,
                               start=DataContext.current.start_date, end=DataContext.current.end_date,
                               query_type=QueryType.MIDCURVE_PREMIUM)
    return _extract_series_from_df(df, QueryType.MIDCURVE_PREMIUM)


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=_currency_to_tdapi_swaption_rate_asset,
                                 query_type=QueryType.MIDCURVE_ANNUITY)])
def midcurve_annuity(asset: Asset, expiration_tenor: str, forward_tenor: str, termination_tenor: str,
                     relative_strike: float = None, benchmark_type: str = None,
                     floating_rate_tenor: str = None,
                     clearing_house: str = None, *, source: str = None,
                     real_time: bool = False) -> Series:
    """
    GS end-of-day annuity for midcurve.

    :param asset: asset object loaded from security master
    :param expiration_tenor: relative date representation of expiration date on the option e.g. 3m
    :param forward_tenor: relative date representation of swap's start date after option expiry e.g. 2y
    :param termination_tenor: relative date representation of the instrument's expiration date e.g. 1y
    :param relative_strike: strike level relative to at the money e.g. 10 or ATM+10
    :param benchmark_type: benchmark type e.g. LIBOR
    :param floating_rate_tenor: floating index rate
    :param clearing_house: Example - "LCH", "EUREX", "JSCC", "CME"
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: swaption implied normal volatility curve
    """

    df = _get_swaption_measure(asset, benchmark_type, floating_rate_tenor, forward_tenor, expiration_tenor,
                               termination_tenor, relative_strike, clearing_house, source=source, real_time=real_time,
                               start=DataContext.current.start_date, end=DataContext.current.end_date,
                               query_type=QueryType.MIDCURVE_ANNUITY)
    return _extract_series_from_df(df, QueryType.MIDCURVE_ANNUITY)


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=_currency_to_tdapi_swaption_rate_asset,
                                 query_type=QueryType.ATM_FWD_RATE)])
def swaption_atm_fwd_rate(asset: Asset, expiration_tenor: str = None, termination_tenor: str = None,
                          benchmark_type: str = None,
                          floating_rate_tenor: str = None,
                          clearing_house: str = None, *, source: str = None,
                          real_time: bool = False) -> Series:
    """
    GS end-of-day atm forward rate for swaption vol matrices.

    :param asset: asset object loaded from security master
    :param expiration_tenor: relative date representation of expiration date on the option e.g. 3m
    :param termination_tenor: relative date representation of the instrument's expiration date e.g. 1y
    :param benchmark_type: benchmark type e.g. LIBOR
    :param floating_rate_tenor: floating index rate
    :param clearing_house: Example - "LCH", "EUREX", "JSCC", "CME"
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: swaption implied normal volatility curve
    """
    df = _get_swaption_measure(asset, benchmark_type=benchmark_type, floating_rate_tenor=floating_rate_tenor,
                               effective_date="0b", expiration_tenor=expiration_tenor,
                               termination_tenor=termination_tenor, clearing_house=clearing_house, source=source,
                               real_time=real_time, start=DataContext.current.start_date,
                               end=DataContext.current.end_date,
                               query_type=QueryType.ATM_FWD_RATE)
    return _extract_series_from_df(df, QueryType.ATM_FWD_RATE)


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=_currency_to_tdapi_swaption_rate_asset,
                                 query_type=QueryType.SWAPTION_VOL)])
def swaption_vol(asset: Asset, expiration_tenor: str = None, termination_tenor: str = None,
                 relative_strike: float = None, benchmark_type: str = None,
                 floating_rate_tenor: str = None,
                 clearing_house: str = None, *, source: str = None,
                 real_time: bool = False) -> Series:
    """
    GS end-of-day implied normal volatility for swaption vol matrices.

    :param asset: asset object loaded from security master
    :param expiration_tenor: relative date representation of expiration date on the option e.g. 3m
    :param termination_tenor: relative date representation of the instrument's expiration date e.g. 1y
    :param relative_strike: strike level relative to at the money e.g. 10 or ATM+10
    :param benchmark_type: benchmark type e.g. LIBOR
    :param floating_rate_tenor: floating index rate
    :param clearing_house: Example - "LCH", "EUREX", "JSCC", "CME"
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: swaption implied normal volatility curve
    """
    df = _get_swaption_measure(asset, benchmark_type, floating_rate_tenor, "0b", expiration_tenor,
                               termination_tenor, relative_strike, clearing_house, source=source, real_time=real_time,
                               query_type=QueryType.SWAPTION_VOL, start=DataContext.current.start_date,
                               end=DataContext.current.end_date)
    return _extract_series_from_df(df, QueryType.SWAPTION_VOL)


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=_currency_to_tdapi_swaption_rate_asset,
                                 query_type=QueryType.MIDCURVE_VOL)])
def midcurve_vol(asset: Asset, expiration_tenor: str, forward_tenor: str, termination_tenor: str,
                 relative_strike: float = None, benchmark_type: str = None,
                 floating_rate_tenor: str = None,
                 clearing_house: str = None, *, source: str = None,
                 real_time: bool = False) -> Series:
    """
    GS end-of-day implied normal volatility for swaption vol matrices.

    :param asset: asset object loaded from security master
    :param expiration_tenor: relative date representation of expiration date on the option e.g. 3m
    :param forward_tenor: relative date representation of swap's start date after option expiry e.g. 2y
    :param termination_tenor: relative date representation of the instrument's expiration date e.g. 1y
    :param relative_strike: strike level relative to at the money e.g. 10 or ATM+10
    :param benchmark_type: benchmark type e.g. LIBOR
    :param floating_rate_tenor: floating index rate
    :param clearing_house: Example - "LCH", "EUREX", "JSCC", "CME"
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: swaption implied normal volatility curve
    """
    df = _get_swaption_measure(asset, benchmark_type, floating_rate_tenor, forward_tenor, expiration_tenor,
                               termination_tenor, relative_strike, clearing_house, source=source, real_time=real_time,
                               query_type=QueryType.MIDCURVE_VOL, start=DataContext.current.start_date,
                               end=DataContext.current.end_date)
    return _extract_series_from_df(df, QueryType.MIDCURVE_VOL)


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=_currency_to_tdapi_swaption_rate_asset,
                                 query_type=QueryType.MIDCURVE_ATM_FWD_RATE)])
def midcurve_atm_fwd_rate(asset: Asset, expiration_tenor: str, forward_tenor: str, termination_tenor: str,
                          benchmark_type: str = None,
                          floating_rate_tenor: str = None,
                          clearing_house: str = None, *, source: str = None,
                          real_time: bool = False) -> Series:
    """
    GS end-of-day atm forward rate for swaption vol matrices.

    :param asset: asset object loaded from security master
    :param expiration_tenor: relative date representation of expiration date on the option e.g. 3m
    :param forward_tenor: relative date representation of swap's start date after option expiry e.g. 2y
    :param termination_tenor: relative date representation of the instrument's expiration date e.g. 1y
    :param benchmark_type: benchmark type e.g. LIBOR
    :param floating_rate_tenor: floating index rate
    :param clearing_house: Example - "LCH", "EUREX", "JSCC", "CME"
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: swaption implied normal volatility curve
    """
    df = _get_swaption_measure(asset, benchmark_type=benchmark_type, floating_rate_tenor=floating_rate_tenor,
                               effective_date=forward_tenor, expiration_tenor=expiration_tenor,
                               termination_tenor=termination_tenor, clearing_house=clearing_house, source=source,
                               real_time=real_time, start=DataContext.current.start_date,
                               end=DataContext.current.end_date,
                               query_type=QueryType.MIDCURVE_ATM_FWD_RATE)
    return _extract_series_from_df(df, QueryType.MIDCURVE_ATM_FWD_RATE)


def _get_swaption_measure(asset: Asset, benchmark_type: str = None, floating_rate_tenor: str = None,
                          effective_date: str = None,
                          expiration_tenor: str = None, termination_tenor: str = None,
                          strike_reference: [str, int] = None,
                          clearing_house: str = None,
                          start: str = DataContext.current.start_date, end: str = DataContext.current.end_date,
                          source: str = None, real_time: bool = False, allow_many: bool = False,
                          query_type: QueryType = QueryType.SWAPTION_PREMIUM) -> Series:
    if real_time:
        raise NotImplementedError('realtime swap_rate not implemented')
    currency = CurrencyEnum(asset.get_identifier(AssetIdentifier.BLOOMBERG_ID))

    if not swaptions_defaults_provider.is_supported(currency):
        raise NotImplementedError('Data not available for {} swap rates'.format(currency.value))

    query = _swaption_build_asset_query(currency, benchmark_type, effective_date, expiration_tenor, floating_rate_tenor,
                                        strike_reference, termination_tenor, clearing_house)

    _logger.debug(query)

    rate_mqid = _get_tdapi_rates_assets(**query, allow_many=allow_many)
    if isinstance(rate_mqid, str):
        rate_mqid = [rate_mqid]
    with DataContext(start, end):
        q = GsDataApi.build_market_data_query(rate_mqid, query_type, source=source,
                                              real_time=real_time)
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return df


def _swaption_build_asset_query(currency, benchmark_type=None, effective_date=None,
                                expiration_tenor=None,
                                floating_rate_tenor=None, strike_reference=None,
                                termination_tenor=None,
                                clearingHouse=None):
    benchmark_type = swaptions_defaults_provider.get_swaption_parameter(currency, 'benchmarkType', benchmark_type)

    floating_rate_option = swaptions_defaults_provider.get_floating_rate_option_for_benchmark(currency, benchmark_type)
    if floating_rate_option is None:
        raise MqValueError(
            "Invalid benchmark type {}: cannot map benchmark_type with underlying rate for {}".format(benchmark_type,
                                                                                                      currency))
    floating_rate_tenor = swaptions_defaults_provider.get_swaption_parameter(currency, "floatingRateTenor",
                                                                             floating_rate_tenor)
    strike_reference = swaptions_defaults_provider.get_swaption_parameter(currency, 'strikeReference', strike_reference)

    termination_tenor = swaptions_defaults_provider.get_swaption_parameter(currency, 'terminationTenor',
                                                                           termination_tenor)
    effective_date = swaptions_defaults_provider.get_swaption_parameter(currency, 'effectiveDate', effective_date)
    expiration_tenor = swaptions_defaults_provider.get_swaption_parameter(currency, 'expirationTenor', expiration_tenor)
    for tenor in [termination_tenor, expiration_tenor]:
        if not _is_valid_relative_date_tenor(tenor):
            raise MqValueError('invalid tenor ' + tenor + ' for index: ' +
                               benchmark_type)
    forward_tenor = _check_forward_tenor(effective_date)
    strike_reference = _check_strike_reference(strike_reference)
    clearingHouse = swaptions_defaults_provider.get_swaption_parameter(currency, 'clearingHouse', clearingHouse)
    query = dict(type='Swaption', asset_parameters_notional_currency=currency.name)
    if termination_tenor is not None:
        query["asset_parameters_termination_date"] = termination_tenor
    if floating_rate_option is not None:
        query["asset_parameters_floating_rate_option"] = floating_rate_option
    if floating_rate_tenor is not None:
        query["asset_parameters_floating_rate_designated_maturity"] = floating_rate_tenor
    if expiration_tenor is not None:
        query["asset_parameters_expiration_date"] = expiration_tenor
    if strike_reference is not None:
        query["asset_parameters_strike"] = strike_reference
    if clearingHouse is not None:
        query["asset_parameters_clearing_house"] = clearingHouse
    if forward_tenor is not None:
        query["asset_parameters_effective_date"] = forward_tenor
    if expiration_tenor is not None:
        query["asset_parameters_notional_currency"] = currency.name

    return query


def _check_strike_reference(strike_reference):
    if strike_reference is None:
        return None
    if isinstance(strike_reference, float) or isinstance(strike_reference, int):
        if strike_reference == 0:
            strike_reference = "ATM"
        else:
            strike_reference = ('ATM%+f' % strike_reference).rstrip('0').rstrip(".")
    elif isinstance(strike_reference, str) and strike_reference.upper() == "SPOT":
        strike_reference = "ATM"

    if isinstance(strike_reference, list):
        to_check = strike_reference
    else:
        to_check = [strike_reference]

    for s in to_check:
        if not re.fullmatch("ATM|ATM[-+]?([0-9]*\.[0-9]+|[0-9]+)", s):
            raise MqValueError('invalid strike reference ' + s)
    return strike_reference


def _is_valid_relative_date_tenor(tenor):
    if tenor is None:
        return True
    if re.fullmatch('(\\d+)([bdwmy])', tenor):
        return True
    else:
        return False


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=_currency_to_tdapi_swaption_rate_asset,
                                 query_type=QueryType.SWAPTION_VOL)])
def swaption_vol_smile(asset: Asset, expiration_tenor: str, termination_tenor: str,
                       pricing_date: Optional[GENERIC_DATE] = None, benchmark_type: str = None,
                       floating_rate_tenor: str = None,
                       clearing_house: str = None, *, source: str = None,
                       real_time: bool = False) -> Series:
    """
    GS end-of-day implied normal volatility for swaption vol matrices.

    :param asset: asset object loaded from security master
    :param expiration_tenor: relative date representation of expiration date on the option e.g. 3m
    :param termination_tenor: relative date representation of the instrument's expiration date e.g. 1y
    :param pricing_date: YYYY-MM-DD or relative date
    :param benchmark_type: benchmark type e.g. LIBOR
    :param floating_rate_tenor: floating index rate
    :param clearing_house: Example - "LCH", "EUREX", "JSCC", "CME"
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: swaption implied normal volatility curve
    """
    if real_time:
        raise NotImplementedError('realtime swaption_vol not implemented')

    _logger.debug('where expiry=%s, tenor=%s', expiration_tenor, termination_tenor)
    currency = CurrencyEnum(asset.get_identifier(AssetIdentifier.BLOOMBERG_ID))
    location = swaptions_defaults_provider.get_swaption_parameter(currency, "pricingLocation")
    start, end = _range_from_pricing_date(location, pricing_date)
    df = _get_swaption_measure(asset, expiration_tenor=expiration_tenor, termination_tenor=termination_tenor,
                               strike_reference=TdapiRatesDefaultsProvider.EMPTY_PROPERTY, source=source,
                               query_type=QueryType.SWAPTION_VOL,
                               benchmark_type=benchmark_type,
                               floating_rate_tenor=floating_rate_tenor,
                               clearing_house=clearing_house,
                               start=start, end=end, allow_many=True)

    dataset_ids = getattr(df, 'dataset_ids', ())
    if df.empty:
        series = ExtendedSeries()
    else:
        # convert string ATM+20 to numerical value 20
        df["strikeRelative"] = df["strikeRelative"].apply(lambda d: float(d.split("ATM")[1] if d != "ATM" else 0))
        latest = df.index.max()
        _logger.info('selected pricing date %s', latest)
        df = df.loc[latest]
        df.set_index('strikeRelative', inplace=True)
        df.sort_index(inplace=True)
        series = ExtendedSeries(df['swaptionVol'].values, index=df.index.values)
    series.dataset_ids = dataset_ids
    return series


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=_currency_to_tdapi_swaption_rate_asset,
                                 query_type=QueryType.SWAPTION_VOL)])
def swaption_vol_term(asset: Asset, tenor_type: SwaptionTenorType, tenor: str, relative_strike: float,
                      pricing_date: Optional[GENERIC_DATE] = None, benchmark_type: str = None,
                      floating_rate_tenor: str = None,
                      clearing_house: str = None, *, source: str = None,
                      real_time: bool = False) -> Series:
    """
    Term structure of GS end-of-day implied normal volatility for swaption vol matrices.

    :param asset: an asset
    :param tenor_type: specifies which type of tenor will be fixed, one of OPTION_EXPIRATION or SWAP_MATURITY
    :param tenor: relative date representation of the instrument's expiration date e.g. 1y
    :param relative_strike: strike level relative to at the money e.g. 10
    :param pricing_date: YYYY-MM-DD or relative date
    :param benchmark_type: benchmark type e.g. LIBOR
    :param floating_rate_tenor: floating index rate
    :param clearing_house: Example - "LCH", "EUREX", "JSCC", "CME"
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: swaption implied normal volatility term structure
    """

    if real_time:
        raise NotImplementedError('realtime swaption_vol not implemented')

    currency = CurrencyEnum(asset.get_identifier(AssetIdentifier.BLOOMBERG_ID))
    location = swaptions_defaults_provider.get_swaption_parameter(currency, "pricingLocation")
    start, end = _range_from_pricing_date(location, pricing_date)
    if tenor_type == SwaptionTenorType.OPTION_EXPIRY:
        tenor_to_plot = 'terminationTenor'
        df = _get_swaption_measure(asset, expiration_tenor=tenor,
                                   termination_tenor=TdapiRatesDefaultsProvider.EMPTY_PROPERTY,
                                   strike_reference=relative_strike,
                                   query_type=QueryType.SWAPTION_VOL,
                                   benchmark_type=benchmark_type,
                                   floating_rate_tenor=floating_rate_tenor,
                                   clearing_house=clearing_house,
                                   source=source,
                                   start=start, end=end, allow_many=True)
    else:
        tenor_to_plot = 'expirationTenor'
        df = _get_swaption_measure(asset, expiration_tenor=TdapiRatesDefaultsProvider.EMPTY_PROPERTY,
                                   termination_tenor=tenor,
                                   strike_reference=relative_strike,
                                   benchmark_type=benchmark_type,
                                   floating_rate_tenor=floating_rate_tenor,
                                   clearing_house=clearing_house,
                                   query_type=QueryType.SWAPTION_VOL, source=source,
                                   start=start, end=end, allow_many=True)

    dataset_ids = getattr(df, 'dataset_ids', ())
    if df.empty:
        series = ExtendedSeries()
    else:
        latest = df.index.max()
        _logger.info('selected pricing date %s', latest)
        df = df.loc[latest]
        business_day = _get_custom_bd(asset.exchange)
        df = df.assign(expirationDate=df.index + df[tenor_to_plot].map(_to_offset) + business_day - business_day)
        df = df.set_index('expirationDate')
        df.sort_index(inplace=True)
        df = df.loc[DataContext.current.start_date: DataContext.current.end_date]
        series = ExtendedSeries() if df.empty else ExtendedSeries(df['swaptionVol'])
    series.dataset_ids = dataset_ids
    return series


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=_currency_to_tdapi_swap_rate_asset, query_type=QueryType.SWAP_RATE)])
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
              [MeasureDependency(id_provider=_currency_to_tdapi_basis_swap_rate_asset,
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

    rate_mqid = _get_tdapi_rates_assets(**kwargs)
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
              [MeasureDependency(id_provider=_currency_to_tdapi_swap_rate_asset, query_type=QueryType.SWAP_RATE)])
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
    if currency.value not in CURRENCY_TO_SWAP_RATE_BENCHMARK.keys():
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
    rate_mqids = _get_tdapi_rates_assets(**kwargs)
    if isinstance(rate_mqids, str):
        rate_mqids = [rate_mqids]
    _logger.debug('assets returned %s', ', '.join(rate_mqids))
    _logger.debug('where benchmark_type=%s, floating_rate_tenor=%s, %s=%s, '
                  'pricing_location=%s', defaults['benchmark_type'], defaults['floating_rate_tenor'], tenor_type.value,
                  tenor_dict['tenor'], defaults['pricing_location'].value)
    start, end = _range_from_pricing_date(calendar, pricing_date)
    with DataContext(start, end):
        q = GsDataApi.build_market_data_query(rate_mqids, QueryType.SWAP_RATE,
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
              [MeasureDependency(id_provider=_currency_to_tdapi_basis_swap_rate_asset,
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

    rate_mqids = _get_tdapi_rates_assets(**kwargs)
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
