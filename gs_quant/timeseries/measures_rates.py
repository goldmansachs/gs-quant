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
from typing import Optional, Union, Dict, List

import pandas as pd
from gs_quant.instrument import IRSwap

from pandas import Series

from gs_quant.api.gs.assets import GsAssetApi
from gs_quant.api.gs.data import QueryType, GsDataApi
from gs_quant.data import DataContext, Dataset
from gs_quant.datetime.gscalendar import GsCalendar
from gs_quant.errors import MqValueError
from gs_quant.markets.securities import AssetIdentifier, Asset
from gs_quant.target.common import Currency as CurrencyEnum, AssetClass, AssetType, PricingLocation, SwapClearingHouse
from gs_quant.timeseries import currency_to_default_ois_asset, convert_asset_for_rates_data_set, RatesConversionType
from gs_quant.timeseries.helper import _to_offset, check_forward_looking, plot_measure
from gs_quant.timeseries.measures import _market_data_timed, _range_from_pricing_date, \
    _get_custom_bd, ExtendedSeries, SwaptionTenorType, _extract_series_from_df, GENERIC_DATE, \
    _asset_from_spec, ASSET_SPEC, MeasureDependency, _logger


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


class EventType(Enum):
    MEETING = 'Meeting Forward'
    EOY = 'EOY Forward'
    SPOT = 'Spot'


class RateType(Enum):
    ABSOLUTE = 'absolute'
    RELATIVE = 'relative'


CCY_TO_CB = {
    'EUR': 'ecb',
    'USD': 'frb',
    'GBP': 'mpc'
}

CENTRAL_BANK_WATCH_START_DATE = datetime.date(2016, 1, 1)


class TdapiRatesDefaultsProvider:
    # flag to indicate that a given property should not  be included in asset query
    EMPTY_PROPERTY = "null"

    def __init__(self, defaults: dict):
        self.defaults = defaults
        benchmark_mappings = {}
        for k, v in defaults.get("CURRENCIES").items():
            benchmark_mappings[k] = {e.get("benchmarkType"): e.get('floatingRateOption') for e in v}
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
        "AUD": [{"benchmarkType": "BBR", "floatingRateOption": "AUD-BBR-BBSW", "floatingRateTenor": ["6m", "3m"],
                 "assetIdForAvailabilityCheck": "MAQHSC1PAF4X5H4B",
                 "pricingLocation": ["TKO"]}],
        "EUR": [
            {"benchmarkType": "LIBOR", "floatingRateOption": "EUR-EURIBOR-TELERATE", "floatingRateTenor": ["6m", "3m"],
             "assetIdForAvailabilityCheck": "MAZB3PAH8JFVVT80",
             "pricingLocation": ["LDN"]},
            {"benchmarkType": "EURIBOR", "floatingRateOption": "EUR-EURIBOR-TELERATE",
             "floatingRateTenor": ["6m", "3m"],
             "assetIdForAvailabilityCheck": "MAZB3PAH8JFVVT80",
             "pricingLocation": ["LDN"]}
        ],
        "GBP": [{"benchmarkType": "LIBOR", "floatingRateOption": "GBP-LIBOR-BBA", "floatingRateTenor": ["6m", "3m"],
                 "assetIdForAvailabilityCheck": "MAX2SBXZRPYR3NTY",
                 "pricingLocation": ["LDN"]},
                {"benchmarkType": "SONIA", "floatingRateOption": "GBP-SONIA-COMPOUND",
                 "floatingRateTenor": ["1y", "6m", "3m"],
                 "assetIdForAvailabilityCheck": "MAQC2E5J9X6WGGCJ",
                 "pricingLocation": ["LDN"]}
                ],
        "JPY": [{"benchmarkType": "LIBOR", "floatingRateOption": "JPY-LIBOR-BBA", "floatingRateTenor": ["6m"],
                 "assetIdForAvailabilityCheck": "MATT7CA7PRA4B8YB",
                 "pricingLocation": ["TKO"], }],
        "KRW": [{"benchmarkType": "KSDA", "floatingRateOption": "KRW-CD-KSDA-BLOOMBERG", "floatingRateTenor": ["3m"],
                 "assetIdForAvailabilityCheck": "MAMNSGB00G4ZCWMP",
                 "pricingLocation": ["TKO"]}],
        "NZD": [{"benchmarkType": "BBR", "floatingRateOption": "NZD-BBR-FRA", "floatingRateTenor": ["3m"],
                 "assetIdForAvailabilityCheck": "MAHGK129ZCWCEG33",
                 "pricingLocation": ["TKO"], }],
        "USD": [{"benchmarkType": "LIBOR", "floatingRateOption": "USD-LIBOR-BBA", "floatingRateTenor": ["3m", "6m"],
                 "assetIdForAvailabilityCheck": "MAY0X3KRD4AN77E2",
                 "strikeReference": ["ATM"],
                 "pricingLocation": ["NYC"]},
                {"benchmarkType": "SOFR", "floatingRateOption": "USD-SOFR-COMPOUND",
                 "floatingRateTenor": ["1y", "6m", "3m"],
                 "assetIdForAvailabilityCheck": "MANYJ1AWNEX5C7FY",
                 "strikeReference": ["ATM"],
                 "pricingLocation": ["NYC"]}
                ],
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
    'AUD': OrderedDict([('BBR', 'AUD-BBR-BBSW'), ('AONIA', 'AUD-AONIA-OIS-COMPOUND')]),
    'BRL': {'CDI': 'BRR-CDI-COMPOUNDED'},
    'CAD': OrderedDict([('CDOR', 'CAD-BA-CDOR'), ('CORRA', 'CAD-CORRA-OIS-COMP')]),
    'CHF': OrderedDict([('LIBOR', 'CHF-LIBOR-BBA'), ('SARON', 'CHF-SARON-OIS-COMPOUND')]),
    'CLP': {'TNA': 'CLP-ICP-CAMARA'},
    'CNY': {'REPO': 'CNY-REPO RATE'},
    'COP': {'IBR': 'COP-IBR-ON'},
    'CZK': {'PRIBOR': 'CZK-PRIBOR-PRBO'},
    'DKK': OrderedDict([('CIBOR', 'DKK-CIBOR2-DKNA13'), ('OIS', 'DKK-DKKOIS-OIS-COMPOUND')]),
    'EUR': OrderedDict([('EURIBOR', 'EUR-EURIBOR-TELERATE'), ('EONIA', 'EUR-EONIA-OIS-COMPOUND'),
                        ('EUROSTR', 'EUR-EUROSTR-COMPOUND')]),
    'GBP': OrderedDict([('LIBOR', 'GBP-LIBOR-BBA'), ('SONIA', 'GBP-SONIA-COMPOUND')]),
    'HKD': {'HIBOR': 'HKD-HIBOR-HKAB'},
    'HUF': {'BIBOR': 'HUF-BIBOR-BUB'},
    'ILS': {'TELBOR': 'ILS-TELBOR-FCI'},
    'INR': {'MIBOR': 'INR-MIBOR-OIS-COMPOUND'},
    'JPY': OrderedDict([('LIBOR', 'JPY-LIBOR-BBA'), ('TONA', 'JPY-TONA-OIS-COMPOUND')]),
    'KRW': {'KSDA': 'KRW-CD-KSDA-BLOOMBERG'},
    'MXN': {'TIIE': 'MXN-TIIE-FX'},
    'NOK': OrderedDict([('NIBOR', 'NOK-NIBOR-BBA'), ('NOWA', 'NOK-NOWA-OIS-COMPOUND')]),
    'NZD': OrderedDict([('BBR', 'NZD-BBR-FRA'), ('NZIONA', 'NZD-NZIONA-OIS-COMPOUND')]),
    'PLN': {'WIBOR': 'PLZ-WIBOR-WIBO'},
    'RUB': {'MOSPRIME': 'RUB-MOSPRIME-NFEA'},
    'SEK': OrderedDict([('STIBOR', 'SEK-STIBOR-SIDE'), ('SIOR', 'SEK-SIOR-OIS-COMPOUND')]),
    'SGD': OrderedDict([('SOR', 'SGD-SOR-VWAP'), ('SORA', 'SGD-SORA-COMPOUND')]),
    'THB': {'THOR': 'THB-THOR-COMPOUND'},
    'USD': OrderedDict(
        [('LIBOR', 'USD-LIBOR-BBA'), ('Fed_Funds', 'USD-Federal Funds-H.15-OIS-COMP'), ('SOFR', 'USD-SOFR-COMPOUND')]),
    'ZAR': {'JIBAR': 'ZAR-JIBAR-SAFEX'},
}
# TODO Join into single object.
BENCHMARK_TO_DEFAULT_FLOATING_RATE_TENORS = {
    'BRR-CDI-COMPOUNDED': '1b',
    'AUD-BBR-BBSW': '6m',
    'AUD-AONIA-OIS-COMPOUND': '1y',
    'CAD-BA-CDOR': '3m',
    'CAD-CORRA-OIS-COMP': '3m',
    'CHF-LIBOR-BBA': '6m',
    'CHF-SARON-OIS-COMPOUND': '1y',
    'CLP-ICP-CAMARA': '1b',
    'CNY-REPO RATE': '1w',
    'COP-IBR-ON': '1b',
    'CZK-PRIBOR-PRBO': '6m',
    'DKK-CIBOR2-DKNA13': '6m',
    'DKK-DKKOIS-OIS-COMPOUND': '1y',
    'EUR-EURIBOR-TELERATE': '6m',
    'EUR-EUROSTR-COMPOUND': '1y',
    'EUR-EONIA-OIS-COMPOUND': '1y',
    'GBP-LIBOR-BBA': '6m',
    'GBP-SONIA-COMPOUND': '1y',
    'HKD-HIBOR-HKAB': '3m',
    'HUF-BIBOR-BUB': '6m',
    'INR-MIBOR-OIS-COMPOUND': '6m',
    'ILS-TELBOR-FCI': '3m',
    'JPY-LIBOR-BBA': '6m',
    'JPY-TONA-OIS-COMPOUND': '1y',
    'KRW-CD-KSDA-BLOOMBERG': '3m',
    'MXN-TIIE-FX': '28d',
    'NOK-NIBOR-BBA': '6m',
    'NOK-NOWA-OIS-COMPOUND': '1y',
    'NZD-BBR-FRA': '3m',
    'NZD-NZIONA-OIS-COMPOUND': '1y',
    'PLZ-WIBOR-WIBO': '6m',
    'RUB-MOSPRIME-NFEA': '3m',
    'SEK-STIBOR-SIDE': '6m',
    'SEK-SIOR-OIS-COMPOUND': '1y',
    'SGD-SOR-VWAP': '6m',
    'SGD-SORA-COMPOUND': '3m',
    'THB-THOR-COMPOUND': '3m',
    'USD-LIBOR-BBA': '3m',
    'USD-Federal Funds-H.15-OIS-COMP': '1y',
    'USD-SOFR-COMPOUND': '1y',
    'ZAR-JIBAR-SAFEX': '3m',
}
CURRENCY_TO_PRICING_LOCATION = {
    CurrencyEnum.JPY: PricingLocation.TKO,
    CurrencyEnum.USD: PricingLocation.NYC,
    CurrencyEnum.AUD: PricingLocation.TKO,
    CurrencyEnum.NZD: PricingLocation.TKO,
    CurrencyEnum.CNY: PricingLocation.HKG,
    CurrencyEnum.HKD: PricingLocation.HKG,
    CurrencyEnum.INR: PricingLocation.HKG,
    CurrencyEnum.KRW: PricingLocation.HKG,
    CurrencyEnum.SGD: PricingLocation.HKG,
    CurrencyEnum.CAD: PricingLocation.NYC,
    CurrencyEnum.EUR: PricingLocation.LDN,
    CurrencyEnum.GBP: PricingLocation.LDN,
    CurrencyEnum.CHF: PricingLocation.LDN,
    CurrencyEnum.DKK: PricingLocation.LDN,
    CurrencyEnum.NOK: PricingLocation.LDN,
    CurrencyEnum.SEK: PricingLocation.LDN,
    CurrencyEnum.BRL: PricingLocation.NYC,
    CurrencyEnum.COP: PricingLocation.NYC,
    CurrencyEnum.CLP: PricingLocation.NYC,
    CurrencyEnum.MXN: PricingLocation.NYC,
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
    'SGD': 'MA5CQFHYBPH9E5BS',
    'BRL': 'MATPPVN02HJ4M9NS',
    'COP': 'MADA0AGFQ65CTMWF',
    'CLP': 'MAP8A0SHH9Q86SXC',
    'MXN': 'MAAJ9RAHYBAXGYD2'
}

SUPPORTED_INTRADAY_CURRENCY_TO_DUMMY_SWAP_BBID = {
    'CHF': 'MACF6R4J5FY4KGBZ',
    'EUR': 'MACF6R4J5FY4KGBZ',
    'GBP': 'MACF6R4J5FY4KGBZ',
    'JPY': 'MACF6R4J5FY4KGBZ',
    'SEK': 'MACF6R4J5FY4KGBZ',
    'USD': 'MACF6R4J5FY4KGBZ',
    'DKK': 'MACF6R4J5FY4KGBZ',
    'NOK': 'MACF6R4J5FY4KGBZ',
    'NZD': 'MACF6R4J5FY4KGBZ',
    'AUD': 'MACF6R4J5FY4KGBZ',
    'CAD': 'MACF6R4J5FY4KGBZ'
}

# FXFwd XCCYSwap rates Defaults
CROSS_BBID_TO_DUMMY_OISXCCY_ASSET = {
    'EURUSD': 'MA1VJC1E3SZW8E4S',
    'GBPUSD': 'MA3JTR4HSC63H4V6',
    'AUDUSD': 'MAD4VBRWYXFSY1N4',
    'NZDUSD': 'MA1YHQMZVTM3VBWT',
    'USDSEK': 'MA2APZREBGDMME83',
    'USDNOK': 'MA0K3W6FKH6K1KJE',
    'USDDKK': 'MA328HZB86DYSWSJ',
    'USDCAD': 'MAT8JNEE2GN5NES6',
    'USDCHF': 'MABNGGTNB9A0TKCG',
    'USDJPY': 'MAMZ9YG8AF3HQ18C',
}

CURRENCY_TO_CSA_DEFAULT_MAP = {
    'USD': 'USD-SOFR',
    'EUR': 'EUR-EUROSTR'
}


def _pricing_location_normalized(location: PricingLocation, ccy: CurrencyEnum) -> PricingLocation:
    if location == PricingLocation.HKG or location == PricingLocation.TKO:
        if ccy in CURRENCY_TO_PRICING_LOCATION.keys() and \
                PricingLocation.HKG == CURRENCY_TO_PRICING_LOCATION.get(ccy, PricingLocation.LDN):
            return PricingLocation.HKG
        else:
            return PricingLocation.TKO
    else:
        return location


def _default_pricing_location(ccy: CurrencyEnum) -> PricingLocation:
    if ccy in CURRENCY_TO_PRICING_LOCATION.keys():
        return CURRENCY_TO_PRICING_LOCATION.get(ccy, PricingLocation.LDN)
    else:
        raise MqValueError('No default location set for currency ' + ccy.value + ', please provide one.')


def _cross_to_fxfwd_xcswp_asset(asset_spec: ASSET_SPEC) -> str:
    asset = _asset_from_spec(asset_spec)
    bbid = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)
    # for each currency, get a dummy asset for checking availability
    result = CROSS_BBID_TO_DUMMY_OISXCCY_ASSET.get(bbid, asset.get_marquee_id())
    return result


def _currency_to_tdapi_swap_rate_asset(asset_spec: ASSET_SPEC) -> str:
    asset = _asset_from_spec(asset_spec)
    bbid = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)
    # for each currency, get a dummy asset for checking availability
    result = CURRENCY_TO_DUMMY_SWAP_BBID.get(bbid, asset.get_marquee_id())
    return result


def _currency_to_tdapi_swap_rate_asset_for_intraday(asset_spec: ASSET_SPEC) -> str:
    return 'MACF6R4J5FY4KGBZ'


def _currency_to_tdapi_asset_base(asset_spec: ASSET_SPEC, allowed_bbids=None) -> str:
    asset = _asset_from_spec(asset_spec)
    bbid = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)
    if bbid is None or (allowed_bbids and bbid not in allowed_bbids):
        return asset.get_marquee_id()
    try:
        result = swaptions_defaults_provider.get_swaption_parameter(bbid, "assetIdForAvailabilityCheck")
    except TypeError:
        logging.info("No assetIdForAvailabilityCheck for" + bbid)
        return asset.get_marquee_id()
    return result


def _currency_to_tdapi_midcurve_asset(asset_spec: ASSET_SPEC) -> str:
    return _currency_to_tdapi_asset_base(asset_spec, ['GBP', 'EUR', 'USD'])


def _currency_to_tdapi_swaption_rate_asset(asset_spec: ASSET_SPEC) -> str:
    return _currency_to_tdapi_asset_base(asset_spec)


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
    elif bbid == 'CAD':
        result = 'MARVD2E65AWEXXBA'
    elif bbid == 'AUD':
        result = 'MAY8H7HCNZ85FJKM'
    elif bbid == 'NZD':
        result = 'MAWK15C0P3SM6C7Q'
    elif bbid == 'SEK':
        result = 'MAS2NJCYHDHP8P0X'
    elif bbid == 'NOK':
        result = 'MAPXC5YBPZJZXYMZ'
    elif bbid == 'DKK':
        result = 'MA2164KK5DMYA561'
    elif bbid == 'CHF':
        result = 'MA7ZHB9T0PF1SB96'
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
            if swap_args['asset_parameters_payer_designated_maturity'] == "12m":
                swap_args['asset_parameters_payer_designated_maturity'] = "1y"
        elif 'SOFR' in receiver_index:
            swap_args['asset_parameters_receiver_designated_maturity'] = swap_args[
                'asset_parameters_payer_designated_maturity']
            if swap_args['asset_parameters_receiver_designated_maturity'] == "12m":
                swap_args['asset_parameters_receiver_designated_maturity'] = "1y"
        elif 'LIBOR' in payer_index or 'EURIBOR' in payer_index or 'STIBOR' in payer_index:
            swap_args['asset_parameters_receiver_designated_maturity'] = swap_args[
                'asset_parameters_payer_designated_maturity']
        elif 'LIBOR' in receiver_index or 'EURIBOR' in receiver_index or 'STIBOR' in receiver_index:
            swap_args['asset_parameters_payer_designated_maturity'] = swap_args[
                'asset_parameters_receiver_designated_maturity']
    return swap_args


def _get_tdapi_rates_assets(allow_many=False, **kwargs) -> Union[str, list]:
    # sanitize input for asset query.
    if "pricing_location" in kwargs:
        del kwargs["pricing_location"]
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
              re.fullmatch('(imm[1-4]|frb[1-9]|ecb[1-9])', forward_tenor)):
        raise MqValueError('invalid forward tenor ' + forward_tenor)
    else:
        return forward_tenor


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
    CDI = 'CDI'
    TNA = 'TNA'
    IBR = 'IBR'
    TIIE = 'TIIE'
    AONIA = 'AONIA'
    NZIONA = 'NZIONA'
    NOWA = 'NOWA'
    CORRA = 'CORRA'
    SIOR = 'SIOR'


def _check_benchmark_type(currency, benchmark_type: Union[BenchmarkType, str], nothrow: bool = False) \
        -> Union[BenchmarkType, str]:
    if isinstance(benchmark_type, str):
        if benchmark_type.upper() in BenchmarkType.__members__:
            benchmark_type = BenchmarkType[benchmark_type.upper()]
        elif benchmark_type in ['fed_funds', 'Fed_Funds', 'FED_FUNDS']:
            benchmark_type = BenchmarkType.Fed_Funds
        elif benchmark_type in ['estr', 'ESTR', 'eurostr', 'EuroStr']:
            benchmark_type = BenchmarkType.EUROSTR
        elif not nothrow:
            raise MqValueError(f'{benchmark_type} is not valid, pick one among ' +
                               ', '.join([x.value for x in BenchmarkType]))
        else:
            return benchmark_type

    if isinstance(benchmark_type, BenchmarkType) and \
            benchmark_type.value not in CURRENCY_TO_SWAP_RATE_BENCHMARK[currency.value].keys():
        raise MqValueError(f'{benchmark_type.value} is not supported for {currency.value}')
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


def _get_benchmark_type(currency: CurrencyEnum, benchmark_type: BenchmarkType = None):
    if benchmark_type is None:
        if currency == CurrencyEnum.EUR:
            benchmark_type = BenchmarkType.EURIBOR
        elif currency == CurrencyEnum.SEK:
            benchmark_type = BenchmarkType.STIBOR
        else:
            benchmark_type = BenchmarkType(str(list(CURRENCY_TO_SWAP_RATE_BENCHMARK[currency.value].keys())[0]))
    benchmark_type_input = CURRENCY_TO_SWAP_RATE_BENCHMARK[currency.value][benchmark_type.value]

    return benchmark_type_input


def _get_swap_leg_defaults(currency: CurrencyEnum, benchmark_type: Union[BenchmarkType, str] = None,
                           floating_rate_tenor: str = None) -> dict:
    pricing_location = CURRENCY_TO_PRICING_LOCATION.get(currency, PricingLocation.LDN)
    # default benchmark types
    if not isinstance(benchmark_type, str):
        benchmark_type_input = _get_benchmark_type(currency, benchmark_type)
    else:
        benchmark_type_input = benchmark_type
    # default floating index
    if floating_rate_tenor is None:
        if benchmark_type_input in BENCHMARK_TO_DEFAULT_FLOATING_RATE_TENORS:
            floating_rate_tenor = BENCHMARK_TO_DEFAULT_FLOATING_RATE_TENORS[benchmark_type_input]
        else:
            raise MqValueError(f"{benchmark_type_input} has no default fixing tenor, please specify one")

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
                   source: str = None, real_time: bool = False, location: PricingLocation = None,
                   query_type: QueryType = QueryType.SWAP_RATE) -> pd.DataFrame:
    if real_time and not (query_type == QueryType.SWAP_RATE):
        raise NotImplementedError('realtime swap_rate not implemented for anything but rates')
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

    if location is None:
        pricing_location = _default_pricing_location(currency)
    else:
        pricing_location = PricingLocation(location)

    kwargs = dict(asset_class='Rates', type='Swap', asset_parameters_termination_date=swap_tenor,
                  asset_parameters_floating_rate_option=defaults['benchmark_type'],
                  asset_parameters_fixed_rate=fixed_rate, asset_parameters_clearing_house=clearing_house.value,
                  asset_parameters_floating_rate_designated_maturity=defaults['floating_rate_tenor'],
                  asset_parameters_effective_date=forward_tenor,
                  asset_parameters_notional_currency=currency.name)

    rate_mqid = _get_tdapi_rates_assets(**kwargs)

    _logger.debug('where asset= %s, swap_tenor=%s, benchmark_type=%s, floating_rate_tenor=%s, forward_tenor=%s, '
                  'pricing_location=%s', rate_mqid, swap_tenor, defaults['benchmark_type'],
                  defaults['floating_rate_tenor'], forward_tenor, pricing_location.value)

    pricing_location = _pricing_location_normalized(pricing_location, currency)
    where = dict(pricingLocation=pricing_location.value)
    q = GsDataApi.build_market_data_query([rate_mqid], query_type, where=where, source=source,
                                          real_time=real_time)
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return df


def _get_swap_data_calc(asset: Asset, swap_tenor: str, benchmark_type: str = None, floating_rate_tenor: str = None,
                        forward_tenor: Optional[GENERIC_DATE] = None, csa: str = None,
                        real_time: bool = False, location: PricingLocation = None) -> pd.DataFrame:
    currency = CurrencyEnum(asset.get_identifier(AssetIdentifier.BLOOMBERG_ID))

    benchmark_type = _check_benchmark_type(currency, benchmark_type, True)

    clearing_house = SwapClearingHouse.LCH
    if csa in ['EUREX', 'JSCC', 'CME']:
        clearing_house = SwapClearingHouse(csa)

    defaults = _get_swap_leg_defaults(currency, benchmark_type, floating_rate_tenor)

    if not re.fullmatch('(\\d+)([bdwmy])', swap_tenor):
        raise MqValueError('invalid swap tenor ' + swap_tenor)

    forward_tenor = _check_forward_tenor(forward_tenor)

    builder = IRSwap(notional_currency=currency, clearing_house=clearing_house,
                     floating_rate_designated_maturity=defaults['floating_rate_tenor'],
                     floating_rate_option=defaults['benchmark_type'],
                     fixed_rate=0.0, termination_date=swap_tenor)

    if forward_tenor:
        builder.effective_date = forward_tenor

    _logger.debug(f'where builder={builder.as_dict()}')

    location = location or PricingLocation.NYC
    q = GsDataApi.get_mxapi_backtest_data(builder, close_location=location.value, real_time=real_time, csa=csa)
    return q


def _get_term_struct_date(tenor: Union[str, datetime.datetime], index: datetime.datetime,
                          business_day) -> datetime.datetime:
    if isinstance(tenor, (datetime.datetime, datetime.date)):
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
                 forward_tenor: Optional[GENERIC_DATE] = None, clearing_house: _ClearingHouse = None,
                 location: PricingLocation = None, *,
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
    :param location: Example - "TKO", "LDN", "NYC"
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: annuity of swap
    """
    df = _get_swap_data(asset=asset, swap_tenor=swap_tenor, benchmark_type=benchmark_type,
                        floating_rate_tenor=floating_rate_tenor, forward_tenor=forward_tenor,
                        clearing_house=clearing_house, source=source,
                        real_time=real_time, query_type=QueryType.SWAP_ANNUITY, location=location)

    series = ExtendedSeries(dtype=float) if df.empty else ExtendedSeries(abs(df['swapAnnuity'] * 1e4 / 1e8))
    series.dataset_ids = getattr(df, 'dataset_ids', ())
    return series


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=_currency_to_tdapi_swaption_rate_asset,
                                 query_type=QueryType.SWAPTION_PREMIUM)])
def swaption_premium(asset: Asset, expiration_tenor: str = None, termination_tenor: str = None,
                     relative_strike: str = None, benchmark_type: str = None,
                     floating_rate_tenor: str = None,
                     clearing_house: str = None, location: PricingLocation = None, *,
                     source: str = None,
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
    :param location: Example - "TKO", "LDN", "NYC"
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: swaption implied normal volatility curve
    """
    df = _get_swaption_measure(asset, benchmark_type, floating_rate_tenor, "0b", expiration_tenor,
                               termination_tenor, relative_strike, clearing_house, source=source, real_time=real_time,
                               start=DataContext.current.start_date, end=DataContext.current.end_date,
                               query_type=QueryType.SWAPTION_PREMIUM, location=location)

    return _extract_series_from_df(df, QueryType.SWAPTION_PREMIUM)


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=_currency_to_tdapi_swaption_rate_asset,
                                 query_type=QueryType.SWAPTION_ANNUITY)])
def swaption_annuity(asset: Asset, expiration_tenor: str = None, termination_tenor: str = None,
                     relative_strike: float = None, benchmark_type: str = None,
                     floating_rate_tenor: str = None,
                     clearing_house: str = None, location: PricingLocation = None, *,
                     source: str = None,
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
    :param location: Example - "TKO", "LDN", "NYC"
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: swaption implied normal volatility curve
    """

    df = _get_swaption_measure(asset, benchmark_type, floating_rate_tenor, "0b", expiration_tenor,
                               termination_tenor, relative_strike, clearing_house, source=source, real_time=real_time,
                               start=DataContext.current.start_date, end=DataContext.current.end_date,
                               query_type=QueryType.SWAPTION_ANNUITY, location=location)
    return _extract_series_from_df(df, QueryType.SWAPTION_ANNUITY)


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=_currency_to_tdapi_midcurve_asset,
                                 query_type=QueryType.MIDCURVE_PREMIUM)])
def midcurve_premium(asset: Asset, expiration_tenor: str, forward_tenor: str, termination_tenor: str,
                     relative_strike: float = None, benchmark_type: str = None,
                     floating_rate_tenor: str = None,
                     clearing_house: str = None, location: PricingLocation = None, *,
                     source: str = None,
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
    :param location: Example - "TKO", "LDN", "NYC"
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: swaption implied normal volatility curve
    """

    df = _get_swaption_measure(asset, benchmark_type, floating_rate_tenor, forward_tenor, expiration_tenor,
                               termination_tenor, relative_strike, clearing_house, source=source, real_time=real_time,
                               start=DataContext.current.start_date, end=DataContext.current.end_date,
                               query_type=QueryType.MIDCURVE_PREMIUM, location=location)
    return _extract_series_from_df(df, QueryType.MIDCURVE_PREMIUM)


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=_currency_to_tdapi_midcurve_asset,
                                 query_type=QueryType.MIDCURVE_ANNUITY)])
def midcurve_annuity(asset: Asset, expiration_tenor: str, forward_tenor: str, termination_tenor: str,
                     relative_strike: float = None, benchmark_type: str = None,
                     floating_rate_tenor: str = None,
                     clearing_house: str = None, location: PricingLocation = None,
                     *, source: str = None,
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
    :param location: Example - "TKO", "LDN", "NYC"
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: swaption implied normal volatility curve
    """

    df = _get_swaption_measure(asset, benchmark_type, floating_rate_tenor, forward_tenor, expiration_tenor,
                               termination_tenor, relative_strike, clearing_house, source=source, real_time=real_time,
                               start=DataContext.current.start_date, end=DataContext.current.end_date,
                               query_type=QueryType.MIDCURVE_ANNUITY, location=location)
    return _extract_series_from_df(df, QueryType.MIDCURVE_ANNUITY)


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=_currency_to_tdapi_swaption_rate_asset,
                                 query_type=QueryType.ATM_FWD_RATE)])
def swaption_atm_fwd_rate(asset: Asset, expiration_tenor: str = None, termination_tenor: str = None,
                          benchmark_type: str = None,
                          floating_rate_tenor: str = None,
                          clearing_house: str = None, location: PricingLocation = None,
                          *, source: str = None,
                          real_time: bool = False) -> Series:
    """
    GS end-of-day atm forward rate for swaption vol matrices.

    :param asset: asset object loaded from security master
    :param expiration_tenor: relative date representation of expiration date on the option e.g. 3m
    :param termination_tenor: relative date representation of the instrument's expiration date e.g. 1y
    :param benchmark_type: benchmark type e.g. LIBOR
    :param floating_rate_tenor: floating index rate
    :param clearing_house: Example - "LCH", "EUREX", "JSCC", "CME"
    :param location: Example - "TKO", "LDN", "NYC"
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: swaption implied normal volatility curve
    """
    df = _get_swaption_measure(asset, benchmark_type=benchmark_type, floating_rate_tenor=floating_rate_tenor,
                               effective_date="0b", expiration_tenor=expiration_tenor,
                               termination_tenor=termination_tenor, clearing_house=clearing_house, source=source,
                               real_time=real_time, start=DataContext.current.start_date,
                               end=DataContext.current.end_date,
                               query_type=QueryType.ATM_FWD_RATE, location=location)
    return _extract_series_from_df(df, QueryType.ATM_FWD_RATE)


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=_currency_to_tdapi_swaption_rate_asset,
                                 query_type=QueryType.SWAPTION_VOL)])
def swaption_vol(asset: Asset, expiration_tenor: str = None, termination_tenor: str = None,
                 relative_strike: float = None, benchmark_type: str = None,
                 floating_rate_tenor: str = None,
                 clearing_house: str = None, location: PricingLocation = None, *, source: str = None,
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
    :param location: Example - "TKO", "LDN", "NYC"
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: swaption implied normal volatility curve
    """
    df = _get_swaption_measure(asset, benchmark_type, floating_rate_tenor, "0b", expiration_tenor,
                               termination_tenor, relative_strike, clearing_house, source=source, real_time=real_time,
                               query_type=QueryType.SWAPTION_VOL, start=DataContext.current.start_date,
                               end=DataContext.current.end_date, location=location)
    return _extract_series_from_df(df, QueryType.SWAPTION_VOL)


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=_currency_to_tdapi_midcurve_asset,
                                 query_type=QueryType.MIDCURVE_VOL)])
def midcurve_vol(asset: Asset, expiration_tenor: str, forward_tenor: str, termination_tenor: str,
                 relative_strike: float = None, benchmark_type: str = None,
                 floating_rate_tenor: str = None,
                 clearing_house: str = None, location: PricingLocation = None, *, source: str = None,
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
    :param location: Example - "TKO", "LDN", "NYC"
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: swaption implied normal volatility curve
    """
    df = _get_swaption_measure(asset, benchmark_type, floating_rate_tenor, forward_tenor, expiration_tenor,
                               termination_tenor, relative_strike, clearing_house, source=source, real_time=real_time,
                               query_type=QueryType.MIDCURVE_VOL, start=DataContext.current.start_date,
                               end=DataContext.current.end_date, location=location)
    return _extract_series_from_df(df, QueryType.MIDCURVE_VOL)


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=_currency_to_tdapi_midcurve_asset,
                                 query_type=QueryType.MIDCURVE_ATM_FWD_RATE)])
def midcurve_atm_fwd_rate(asset: Asset, expiration_tenor: str, forward_tenor: str, termination_tenor: str,
                          benchmark_type: str = None,
                          floating_rate_tenor: str = None,
                          clearing_house: str = None, location: PricingLocation = None, *, source: str = None,
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
    :param location: Example - "TKO", "LDN", "NYC"
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: swaption implied normal volatility curve
    """
    df = _get_swaption_measure(asset, benchmark_type=benchmark_type, floating_rate_tenor=floating_rate_tenor,
                               effective_date=forward_tenor, expiration_tenor=expiration_tenor,
                               termination_tenor=termination_tenor, clearing_house=clearing_house, source=source,
                               real_time=real_time, start=DataContext.current.start_date,
                               end=DataContext.current.end_date,
                               query_type=QueryType.MIDCURVE_ATM_FWD_RATE, location=location)
    return _extract_series_from_df(df, QueryType.MIDCURVE_ATM_FWD_RATE)


def _get_swaption_measure(asset: Asset, benchmark_type: str = None, floating_rate_tenor: str = None,
                          effective_date: str = None,
                          expiration_tenor: str = None, termination_tenor: str = None,
                          strike_reference: [str, int] = None,
                          clearing_house: str = None,
                          start: str = DataContext.current.start_date, end: str = DataContext.current.end_date,
                          source: str = None, real_time: bool = False, allow_many: bool = False,
                          query_type: QueryType = QueryType.SWAPTION_PREMIUM,
                          location: PricingLocation = None) -> Series:
    if real_time:
        raise NotImplementedError(f'realtime {query_type.value} not implemented')
    currency = CurrencyEnum(asset.get_identifier(AssetIdentifier.BLOOMBERG_ID))

    if not swaptions_defaults_provider.is_supported(currency):
        raise NotImplementedError(f'Data not available for {currency.value} {query_type.value}')

    query = _swaption_build_asset_query(currency, benchmark_type, effective_date, expiration_tenor, floating_rate_tenor,
                                        strike_reference, termination_tenor, clearing_house)

    _logger.debug(query)

    rate_mqid = _get_tdapi_rates_assets(**query, allow_many=allow_many)
    if isinstance(rate_mqid, str):
        rate_mqid = [rate_mqid]

    if location is None:
        pricing_location = _default_pricing_location(currency)
    else:
        pricing_location = PricingLocation(location)
    pricing_location = _pricing_location_normalized(pricing_location, currency)

    where = dict(pricingLocation=pricing_location.value)
    with DataContext(start, end):
        q = GsDataApi.build_market_data_query(rate_mqid, query_type, where=where, source=source,
                                              real_time=real_time)
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return df


def _swaption_build_asset_query(currency, benchmark_type=None, effective_date=None,
                                expiration_tenor=None,
                                floating_rate_tenor=None, strike_reference=None,
                                termination_tenor=None,
                                clearinghouse=None):
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
    clearinghouse = swaptions_defaults_provider.get_swaption_parameter(currency, 'clearingHouse', clearinghouse)
    query = dict(asset_class='Rates', type='Swaption', asset_parameters_notional_currency=currency.name)
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
    if clearinghouse is not None:
        query["asset_parameters_clearing_house"] = clearinghouse
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
                       clearing_house: str = None, location: PricingLocation = None, *, source: str = None,
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
    :param location: Example - "TKO", "LDN", "NYC"
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: swaption implied normal volatility curve
    """
    if real_time:
        raise NotImplementedError('realtime swaption_vol not implemented')

    _logger.debug('where expiry=%s, tenor=%s', expiration_tenor, termination_tenor)
    currency = CurrencyEnum(asset.get_identifier(AssetIdentifier.BLOOMBERG_ID))
    if location is None:
        location = PricingLocation(swaptions_defaults_provider.get_swaption_parameter(currency, "pricingLocation"))

    start, end = _range_from_pricing_date(location, pricing_date)
    df = _get_swaption_measure(asset, expiration_tenor=expiration_tenor, termination_tenor=termination_tenor,
                               strike_reference=TdapiRatesDefaultsProvider.EMPTY_PROPERTY, source=source,
                               query_type=QueryType.SWAPTION_VOL,
                               benchmark_type=benchmark_type,
                               floating_rate_tenor=floating_rate_tenor,
                               clearing_house=clearing_house, location=location,
                               start=start, end=end, allow_many=True)

    dataset_ids = getattr(df, 'dataset_ids', ())
    if df.empty:
        series = ExtendedSeries(dtype=float)
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
                      clearing_house: str = None, location: PricingLocation = None, *, source: str = None,
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
    :param location: Example - "TKO", "LDN", "NYC"
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: swaption implied normal volatility term structure
    """

    if real_time:
        raise NotImplementedError('realtime swaption_vol not implemented')

    currency = CurrencyEnum(asset.get_identifier(AssetIdentifier.BLOOMBERG_ID))
    if location is None:
        location = PricingLocation(swaptions_defaults_provider.get_swaption_parameter(currency, "pricingLocation"))
    start, end = _range_from_pricing_date(location.value, pricing_date)
    if tenor_type == SwaptionTenorType.OPTION_EXPIRY:
        tenor_to_plot = 'terminationTenor'
        df = _get_swaption_measure(asset, expiration_tenor=tenor,
                                   termination_tenor=TdapiRatesDefaultsProvider.EMPTY_PROPERTY,
                                   strike_reference=relative_strike,
                                   query_type=QueryType.SWAPTION_VOL,
                                   benchmark_type=benchmark_type,
                                   floating_rate_tenor=floating_rate_tenor,
                                   clearing_house=clearing_house, location=location,
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
        series = ExtendedSeries(dtype=float)
    else:
        latest = df.index.max()
        _logger.info('selected pricing date %s', latest)
        df = df.loc[latest]
        business_day = _get_custom_bd(asset.exchange)
        df = df.assign(expirationDate=df.index + df[tenor_to_plot].map(_to_offset) + business_day - business_day)
        df = df.set_index('expirationDate')
        df.sort_index(inplace=True)
        df = df.loc[DataContext.current.start_date: DataContext.current.end_date]
        series = ExtendedSeries(dtype=float) if df.empty else ExtendedSeries(df['swaptionVol'])
    series.dataset_ids = dataset_ids
    if series.empty:  # Raise descriptive error if no data returned + historical date context
        check_forward_looking(None, source, 'swaption_vol_term')
    return series


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=_currency_to_tdapi_swap_rate_asset, query_type=QueryType.SWAP_RATE)])
def swap_rate(asset: Asset, swap_tenor: str, benchmark_type: str = None, floating_rate_tenor: str = None,
              forward_tenor: Optional[GENERIC_DATE] = None, clearing_house: _ClearingHouse = None,
              location: PricingLocation = None, *,
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
    :param location: Example - "TKO", "LDN", "NYC"
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: swap rate curve
    """
    df = _get_swap_data(asset=asset, swap_tenor=swap_tenor, benchmark_type=benchmark_type,
                        floating_rate_tenor=floating_rate_tenor, forward_tenor=forward_tenor,
                        clearing_house=clearing_house, source=source,
                        real_time=real_time, query_type=QueryType.SWAP_RATE, location=location)

    series = ExtendedSeries(dtype=float) if df.empty else ExtendedSeries(df['swapRate'])
    series.dataset_ids = getattr(df, 'dataset_ids', ())
    return series


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=_currency_to_tdapi_swap_rate_asset_for_intraday,
                                 query_type=QueryType.SPOT)])
def swap_rate_calc(asset: Asset, swap_tenor: str, benchmark_type: str = None, floating_rate_tenor: str = None,
                   forward_tenor: Optional[GENERIC_DATE] = None, csa: str = None,
                   location: PricingLocation = None, *,
                   source: str = None, real_time: bool = False) -> Series:
    """
    GS intra-day Fixed-Floating interest rate swap (IRS) curves across major currencies.
    This API runs on-the-fly calculations


    :param asset: asset object loaded from security master
    :param swap_tenor: relative date representation of expiration date e.g. 1m
    :param benchmark_type: benchmark type e.g. LIBOR
    :param floating_rate_tenor: floating index rate
    :param forward_tenor: absolute / relative date representation of forward starting point eg: '1y' or 'Spot' for
            spot starting swaps, 'imm1' or 'frb1'
    :param csa: Collateral type or clearing house for cleared swaps - set to Default for standard domestic funding.
    :param location: Example - "TKO", "LDN", "NYC"
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: swap rate curve
    """

    df = _get_swap_data_calc(asset=asset, swap_tenor=swap_tenor, benchmark_type=benchmark_type,
                             floating_rate_tenor=floating_rate_tenor, forward_tenor=forward_tenor,
                             csa=csa, real_time=real_time, location=location)

    series = ExtendedSeries(dtype=float) if df.empty else ExtendedSeries(df['ATMRate'])
    series.dataset_ids = ()
    return series


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=_currency_to_tdapi_swap_rate_asset_for_intraday,
                                 query_type=QueryType.SPOT)])
def forward_rate(asset: Asset, forward_start_tenor: str = None, forward_term: str = None,
                 csa: str = None,
                 close_location: str = None, *, source: str = None, real_time: bool = False) -> Series:
    """
    GS Forward Rate across major currencies.
    This API computes forward rates off stored forward/discount curves


    :param asset: asset object loaded from security master
    :param forward_start_tenor: Relative date of start of forward e.g. 1y
    :param forward_term:    Term of forward, e.g. 3m
    :param csa: Collateral code of curve, e.g. GBP-1. If set to default, default CSA is chosen
    :param close_location: For EOD data, gives location of close
    :param source: name of function caller
    :param real_time: whether to retrieve intra-day data instead of EOD
    :return: annualised instantaneous forward rate
    """

    currency = CurrencyEnum(asset.get_identifier(AssetIdentifier.BLOOMBERG_ID))
    csa = csa or 'Default'
    close_location = close_location or 'NYC'
    if not forward_term:
        raise MqValueError("Forward rate term not specified")

    if not forward_start_tenor:
        forward_start_tenor = '0d'

    measure = f'FR:{forward_start_tenor}:{forward_term}'
    df = GsDataApi.get_mxapi_curve_measure('DISCOUNT CURVE', currency.value, [], [csa], measure,
                                           close_location=close_location, real_time=real_time)

    series = ExtendedSeries(dtype=float) if df.empty else ExtendedSeries(df[measure])
    series.dataset_ids = ()
    return series


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=_currency_to_tdapi_swap_rate_asset_for_intraday,
                                 query_type=QueryType.SPOT)])
def discount_factor(asset: Asset, tenor: str = None, csa: str = None, close_location: str = None,
                    *, source: str = None, real_time: bool = False) -> Series:
    """
    GS Discount Factor across major currencies.
    This API computes discount factor off stored forward/discount curves


    :param asset: asset object loaded from security master
    :param tenor: tenor of discount factor e.g. 1m
    :param csa: Collateral code of curve to fetch discount factor, e.g. GBP-1. If not specified, default CSA is chosen
    :param close_location: For EOD data, gives location of close
    :param source: name of function caller
    :param real_time: whether to retrieve intra-day data instead of EOD
    :return: annualised instantaneous forward rate
    """

    currency = CurrencyEnum(asset.get_identifier(AssetIdentifier.BLOOMBERG_ID))
    close_location = close_location or 'NYC'
    if not tenor:
        raise MqValueError("Discount Curve start and end date not specified")

    csa = csa or 'Default'

    measure = f'DF:{tenor}'
    df = GsDataApi.get_mxapi_curve_measure('DISCOUNT CURVE', currency.value, [], [csa], measure,
                                           close_location=close_location, real_time=real_time)

    series = ExtendedSeries(dtype=float) if df.empty else ExtendedSeries(df[measure])
    series.dataset_ids = ()
    return series


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=_currency_to_tdapi_swap_rate_asset_for_intraday,
                                 query_type=QueryType.SPOT)])
def instantaneous_forward_rate(asset: Asset, tenor: str = None, csa: str = None,
                               close_location: str = None,
                               *, source: str = None, real_time: bool = False) -> Series:
    """
    GS Floating Rate Benchmark annualised instantaneous forward rates across major currencies.
    This API computes IFR off stored forward/discount curves


    :param asset: asset object loaded from security master
    :param tenor: tenor of IFR e.g. 1m
    :param csa: Collateral code of curve to fetch IFR. Set to default for default collateral
    :param close_location: For EOD data, gives location of close
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: annualised instantaneous forward rate
    """

    currency = CurrencyEnum(asset.get_identifier(AssetIdentifier.BLOOMBERG_ID))
    close_location = close_location or 'NYC'
    if not tenor:
        raise MqValueError("Forward rate tenor not specified")

    csa = csa or 'Default'

    measure = f'IFR:{tenor}'
    df = GsDataApi.get_mxapi_curve_measure('DISCOUNT CURVE', currency.value, [], [csa], measure,
                                           close_location=close_location, real_time=real_time)

    series = ExtendedSeries(dtype=float) if df.empty else ExtendedSeries(df[measure])
    series.dataset_ids = ()
    return series


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=_currency_to_tdapi_swap_rate_asset_for_intraday,
                                 query_type=QueryType.SPOT)])
def index_forward_rate(asset: Asset, forward_start_tenor: str = None, benchmark_type: str = None,
                       fixing_tenor: str = None, close_location: str = None, *,
                       source: str = None, real_time: bool = False) -> Series:
    """
    GS annualised forward rates across floating rate benchmark
    This API computes index forward rate off stored index forward curves


    :param asset: asset object loaded from security master
    :param forward_start_tenor: relative start rate of forward e.g. 1m
    :param benchmark_type: benchmark type of floating rate option e.g. LIBOR
    :param fixing_tenor: Fixing tenor of the given benchmark type. Leave empty to use default e.g. 3m
    :param close_location: For EOD data, gives location of close
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: annualised forward rate
    """
    currency = CurrencyEnum(asset.get_identifier(AssetIdentifier.BLOOMBERG_ID))
    close_location = close_location or 'NYC'
    if not forward_start_tenor:
        raise MqValueError("Forward rate start date not specified")

    benchmark_type = _check_benchmark_type(currency, benchmark_type, True)
    if not isinstance(benchmark_type, str):
        benchmark_type_input = _get_benchmark_type(currency, benchmark_type)
    else:
        benchmark_type_input = benchmark_type

    if fixing_tenor is None:
        if benchmark_type_input not in BENCHMARK_TO_DEFAULT_FLOATING_RATE_TENORS:
            raise MqValueError("Please provide fixing tenor: " +
                               f"default fixing tenor not specified for {benchmark_type_input}")
        fixing_tenor = BENCHMARK_TO_DEFAULT_FLOATING_RATE_TENORS[benchmark_type_input]

    measure = f'FR:{forward_start_tenor}:{fixing_tenor}'
    df = GsDataApi.get_mxapi_curve_measure('INDEX CURVE', benchmark_type_input, [fixing_tenor], [f'{currency.value}-1'],
                                           measure, close_location=close_location, real_time=real_time)

    series = ExtendedSeries(dtype=float) if df.empty else ExtendedSeries(df[measure])
    series.dataset_ids = ()
    return series


def _get_basis_swap_kwargs(asset: Asset, spread_benchmark_type: str = None, spread_tenor: str = None,
                           reference_benchmark_type: str = None, reference_tenor: str = None,
                           forward_tenor: Optional[GENERIC_DATE] = None, clearing_house: _ClearingHouse = None,
                           location: PricingLocation = None) -> dict:
    currency = CurrencyEnum(asset.get_identifier(AssetIdentifier.BLOOMBERG_ID))
    if currency.value not in ['JPY', 'EUR', 'USD', 'GBP', 'CHF', 'DKK', 'NOK', 'SEK', 'CAD', 'AUD', 'NZD']:
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

    if location is None:
        pricing_location = PricingLocation(legs_w_defaults['spread']['pricing_location'].value)
    else:
        pricing_location = PricingLocation(location)
    pricing_location = _pricing_location_normalized(pricing_location, currency)

    kwargs = dict(type='BasisSwap', asset_parameters_payer_rate_option=legs_w_defaults['spread']['benchmark_type'],
                  asset_parameters_payer_designated_maturity=legs_w_defaults['spread']['floating_rate_tenor'],
                  asset_parameters_receiver_rate_option=legs_w_defaults['reference']['benchmark_type'],
                  asset_parameters_receiver_designated_maturity=legs_w_defaults['reference']['floating_rate_tenor'],
                  asset_parameters_clearing_house=clearing_house.value, asset_parameters_effective_date=forward_tenor,
                  asset_parameters_notional_currency=currency.name,
                  pricing_location=pricing_location)
    kwargs = _match_floating_tenors(kwargs)
    return kwargs


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=_currency_to_tdapi_basis_swap_rate_asset,
                                 query_type=QueryType.BASIS_SWAP_RATE)])
def basis_swap_spread(asset: Asset, swap_tenor: str = '1y',
                      spread_benchmark_type: str = None, spread_tenor: str = None,
                      reference_benchmark_type: str = None, reference_tenor: str = None,
                      forward_tenor: Optional[GENERIC_DATE] = None, clearing_house: _ClearingHouse = None,
                      location: PricingLocation = None, *,
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
    :param location: Example - "TKO", "LDN", "NYC"
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
                                    forward_tenor=forward_tenor, clearing_house=clearing_house, location=location)
    kwargs['asset_parameters_termination_date'] = swap_tenor

    rate_mqid = _get_tdapi_rates_assets(**kwargs)
    _logger.debug('where asset=%s, swap_tenor=%s, spread_benchmark_type=%s, spread_tenor=%s, '
                  'reference_benchmark_type=%s, reference_tenor=%s, forward_tenor=%s, pricing_location=%s ',
                  rate_mqid, swap_tenor, kwargs['asset_parameters_payer_rate_option'],
                  kwargs['asset_parameters_payer_designated_maturity'], kwargs['asset_parameters_receiver_rate_option'],
                  kwargs['asset_parameters_receiver_designated_maturity'],
                  kwargs['asset_parameters_effective_date'], kwargs['pricing_location'])
    where = {'pricingLocation': kwargs['pricing_location'].value}

    q = GsDataApi.build_market_data_query([rate_mqid], QueryType.BASIS_SWAP_RATE, where=where,
                                          source=source, real_time=real_time)
    _logger.debug('q %s', q)
    df = _market_data_timed(q)

    series = ExtendedSeries(dtype=float) if df.empty else ExtendedSeries(df['basisSwapRate'])
    series.dataset_ids = getattr(df, 'dataset_ids', ())
    return series


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=_currency_to_tdapi_swap_rate_asset, query_type=QueryType.SWAP_RATE)])
def swap_term_structure(asset: Asset, benchmark_type: str = None, floating_rate_tenor: str = None,
                        tenor_type: _SwapTenorType = None, tenor: Optional[GENERIC_DATE] = None,
                        clearing_house: _ClearingHouse = None, location: PricingLocation = None,
                        pricing_date: Optional[GENERIC_DATE] = None,
                        *, source: str = None, real_time: bool = False) -> Series:
    """
    GS end-of-day Fixed-Floating interest rate swap (IRS) term structure across major currencies.

    :param asset: asset object loaded from security master
    :param benchmark_type: benchmark type e.g. LIBOR
    :param floating_rate_tenor: floating index rate
    :param tenor_type: specify which tenor should be fixed, SWAP_TENOR or FORWARD_TENOR
    :param tenor: absolute / relative date representation of forward starting point or swap maturity
    :param clearing_house: Example - "LCH", "EUREX", "JSCC", "CME"
    :param location: Example - "TKO", "LDN", "NYC"
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

    if location is None:
        pricing_location = _default_pricing_location(currency)
    else:
        pricing_location = location
    pricing_location = _pricing_location_normalized(pricing_location, currency)

    calendar = pricing_location.value
    if pricing_date is not None and pricing_date in list(GsCalendar.get(calendar).holidays):
        raise MqValueError('Specified pricing date is a holiday in {} calendar'.format(calendar))

    fixed_rate = 'ATM'

    where = dict(pricingLocation=pricing_location.value)

    kwargs = dict(type='Swap', asset_parameters_floating_rate_option=defaults['benchmark_type'],
                  asset_parameters_fixed_rate=fixed_rate, asset_parameters_clearing_house=clearing_house.value,
                  asset_parameters_floating_rate_designated_maturity=defaults['floating_rate_tenor'],
                  asset_parameters_notional_currency=currency.name, pricing_location=pricing_location.value)
    kwargs[tenor_dict['tenor_dataset_field']] = tenor_dict['tenor']
    rate_mqids = _get_tdapi_rates_assets(allow_many=True, **kwargs)
    if isinstance(rate_mqids, str):
        rate_mqids = [rate_mqids]
    _logger.debug('assets returned %s', ', '.join(rate_mqids))
    _logger.debug('where benchmark_type=%s, floating_rate_tenor=%s, %s=%s, '
                  'pricing_location=%s', defaults['benchmark_type'], defaults['floating_rate_tenor'], tenor_type.value,
                  tenor_dict['tenor'], defaults['pricing_location'].value)
    start, end = _range_from_pricing_date(calendar, pricing_date)
    with DataContext(start, end):
        q = GsDataApi.build_market_data_query(rate_mqids, QueryType.SWAP_RATE, where=where,
                                              source=source, real_time=real_time)
        _logger.debug('q %s', q)
        df = _market_data_timed(q)

    if df.empty:
        series = ExtendedSeries(dtype=float)
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
            series = ExtendedSeries(dtype=float) if df.empty else ExtendedSeries(df['swapRate'])
    series.dataset_ids = getattr(df, 'dataset_ids', ())
    if series.empty:  # Raise descriptive error if no data returned + date context is in the past
        check_forward_looking(None, source, 'swaption_vol_term')
    return series


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=_currency_to_tdapi_basis_swap_rate_asset,
                                 query_type=QueryType.BASIS_SWAP_RATE)])
def basis_swap_term_structure(asset: Asset, spread_benchmark_type: str = None, spread_tenor: str = None,
                              reference_benchmark_type: str = None, reference_tenor: str = None,
                              tenor_type: _SwapTenorType = None, tenor: Optional[GENERIC_DATE] = None,
                              clearing_house: _ClearingHouse = None,
                              location: PricingLocation = None,
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
    :param location: Example - "TKO", "LDN", "NYC"
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
                                    clearing_house=clearing_house, location=location)
    kwargs[tenor_dict['tenor_dataset_field']] = tenor_dict['tenor']
    calendar = kwargs['pricing_location'].value
    if pricing_date is not None and pricing_date in list(GsCalendar.get(calendar).holidays):
        raise MqValueError('Specified pricing date is a holiday in {} calendar'.format(calendar))

    rate_mqids = _get_tdapi_rates_assets(allow_many=True, **kwargs)
    if isinstance(rate_mqids, str):  # single asset returned
        rate_mqids = [rate_mqids]
    _logger.debug('assets returned %s', ', '.join(rate_mqids))
    _logger.debug('where spread_benchmark_type=%s, spread_tenor=%s,  reference_benchmark_type=%s, '
                  'reference_tenor=%s, %s=%s, pricing_location=%s ',
                  kwargs['asset_parameters_payer_rate_option'], kwargs['asset_parameters_payer_designated_maturity'],
                  kwargs['asset_parameters_receiver_rate_option'],
                  kwargs['asset_parameters_receiver_designated_maturity'],
                  kwargs[tenor_dict['tenor_dataset_field']], tenor_dict['tenor'], kwargs['pricing_location'].value)

    where = {'pricingLocation': kwargs['pricing_location'].value}
    start, end = _range_from_pricing_date(calendar, pricing_date)
    with DataContext(start, end):
        q = GsDataApi.build_market_data_query(rate_mqids, QueryType.BASIS_SWAP_RATE, where=where,
                                              source=source, real_time=real_time)
        _logger.debug('q %s', q)
        df = _market_data_timed(q)

    if df.empty:
        series = ExtendedSeries(dtype=float)
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
            series = ExtendedSeries(dtype=float) if df.empty else ExtendedSeries(df['basisSwapRate'])
    series.dataset_ids = getattr(df, 'dataset_ids', ())
    if series.empty:  # Raise descriptive error if no data returned + historical date context
        check_forward_looking(None, source, 'swaption_vol_term')
    return series


def _get_fxfwd_xccy_swp_rates_data(asset: Asset, tenor: str, real_time: bool = False, source: str = None,
                                   query_type: QueryType = None) -> pd.DataFrame:
    if real_time:
        raise NotImplementedError('realtime not implemented')
    pair = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)

    if pair not in CROSS_BBID_TO_DUMMY_OISXCCY_ASSET.keys():
        raise NotImplementedError('Data not available for pair: ' + str(pair))

    if not (re.fullmatch('(\\d+)([wfmy])', tenor)):
        raise MqValueError('invalid tenor: ' + tenor)

    remap_tenor = tenor.replace('m', 'f')
    currency = pair.replace('USD', '')
    price_location_defaults = CURRENCY_TO_PRICING_LOCATION.get(currency, PricingLocation.LDN)
    kwargs = dict(type='Forward', asset_parameters_settlement_date=remap_tenor, asset_parameters_pair=pair)

    rate_mqid = _get_tdapi_rates_assets(**kwargs)

    _logger.debug('where asset= %s (%s), ois_xccy_tenor=%s, pricing_location=%s',
                  rate_mqid, pair, tenor, price_location_defaults)

    q = GsDataApi.build_market_data_query([rate_mqid], query_type, source=source, real_time=real_time)
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return df


@plot_measure((AssetClass.FX,), (AssetType.Forward, AssetType.Cross),
              [MeasureDependency(id_provider=_cross_to_fxfwd_xcswp_asset, query_type=QueryType.OIS_XCCY)])
def ois_xccy(asset: Asset, tenor: str = None, *, source: str = None, real_time: bool = False) -> Series:
    """
    GS end-of-day OIS Xccy spreads curves across G10 cross currencies.

    :param asset: asset object loaded from security master
    :param tenor: relative date representation of expiration date e.g. 1w
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: ois xccy spread curve
    """
    df = _get_fxfwd_xccy_swp_rates_data(asset=asset, tenor=tenor, query_type=QueryType.OIS_XCCY, source=source,
                                        real_time=real_time)

    series = ExtendedSeries(dtype=float) if df.empty else ExtendedSeries(df['oisXccy'])
    series.dataset_ids = getattr(df, 'dataset_ids', ())
    return series


@plot_measure((AssetClass.FX,), (AssetType.Forward, AssetType.Cross),
              [MeasureDependency(id_provider=_cross_to_fxfwd_xcswp_asset,
                                 query_type=QueryType.OIS_XCCY_EX_SPIKE)])
def ois_xccy_ex_spike(asset: Asset, tenor: str = None, *, source: str = None, real_time: bool = False) -> Series:
    """
    GS end-of-day OIS Xccy spreads curves excluding spikes across G10 cross currencies.

    :param asset: asset object loaded from security master
    :param tenor: relative date representation of expiration date e.g. 1w
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: ois xccy spread curve excluding spikes
    """
    df = _get_fxfwd_xccy_swp_rates_data(asset=asset, tenor=tenor, query_type=QueryType.OIS_XCCY_EX_SPIKE, source=source,
                                        real_time=real_time)

    series = ExtendedSeries(dtype=float) if df.empty else ExtendedSeries(df['oisXccyExSpike'])
    series.dataset_ids = getattr(df, 'dataset_ids', ())
    return series


@plot_measure((AssetClass.FX,), (AssetType.Forward, AssetType.Cross),
              [MeasureDependency(id_provider=_cross_to_fxfwd_xcswp_asset, query_type=QueryType.NON_USD_OIS)])
def non_usd_ois(asset: Asset, tenor: str = None, *, source: str = None, real_time: bool = False) -> Series:
    """
    GS end-of-day non domestic USD ois rate curve for G10 cross currencies.

    :param asset: asset object loaded from security master
    :param tenor: relative date representation of expiration date e.g. 1w
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: non usd ois domestic rate curve (from cross)
    """
    df = _get_fxfwd_xccy_swp_rates_data(asset=asset, tenor=tenor, query_type=QueryType.NON_USD_OIS, source=source,
                                        real_time=real_time)

    series = ExtendedSeries(dtype=float) if df.empty else ExtendedSeries(df['nonUsdOis'])
    series.dataset_ids = getattr(df, 'dataset_ids', ())
    return series


@plot_measure((AssetClass.FX,), (AssetType.Forward, AssetType.Cross),
              [MeasureDependency(id_provider=_cross_to_fxfwd_xcswp_asset, query_type=QueryType.USD_OIS)])
def usd_ois(asset: Asset, tenor: str = None, *, source: str = None, real_time: bool = False) -> Series:
    """
    GS end-of-day USD domestic ois rates curves across G10 cross currencies.

    :param asset: asset object loaded from security master
    :param tenor: relative date representation of expiration date e.g. 1w
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: usd ois domestic rate curve (from cross)
    """
    df = _get_fxfwd_xccy_swp_rates_data(asset=asset, tenor=tenor, query_type=QueryType.USD_OIS, source=source,
                                        real_time=real_time)

    series = ExtendedSeries(dtype=float) if df.empty else ExtendedSeries(df['usdOis'])
    series.dataset_ids = getattr(df, 'dataset_ids', ())
    return series


class BenchmarkTypeCB(Enum):
    EUROSTR = 'EUROSTR'
    SOFR = 'SOFR'
    EONIA = 'EONIA'
    SONIA = 'SONIA'
    Fed_Funds = 'Fed_Funds'


def get_cb_swaps_kwargs(currency: CurrencyEnum, benchmark_type: BenchmarkTypeCB) -> Dict:
    benchmark_type = _check_benchmark_type(currency, benchmark_type)
    clearing_house = _check_clearing_house(None)
    defaults = _get_swap_leg_defaults(currency, benchmark_type)
    possible_swap_tenors = [f"{CCY_TO_CB[currency.value]}{i}" for i in range(0, 20)]
    possible_fwd_tenors = [f"{CCY_TO_CB[currency.value]}{i}" for i in range(0, 20)]
    possible_fwd_tenors.append('0b')
    fixed_rate = 'ATM'
    kwargs = dict(asset_class='Rates', type='Swap',
                  asset_parameters_floating_rate_option=defaults['benchmark_type'],
                  asset_parameters_fixed_rate=fixed_rate,
                  asset_parameters_clearing_house=clearing_house.value,
                  # asset_parameters_floating_rate_designated_maturity=defaults['floating_rate_tenor'],
                  asset_parameters_termination_date=possible_swap_tenors,
                  asset_parameters_effective_date=possible_fwd_tenors,
                  asset_parameters_notional_currency=currency.value)
    return kwargs


def get_cb_meeting_swaps(currency: CurrencyEnum, benchmark_type: BenchmarkTypeCB) -> List:
    kwargs = get_cb_swaps_kwargs(currency=currency, benchmark_type=benchmark_type)
    return _get_tdapi_rates_assets(allow_many=True, **kwargs)


def get_cb_meeting_swap(currency: CurrencyEnum, benchmark_type: BenchmarkTypeCB, forward_tenor: str,
                        swap_tenor: str) -> str:
    kwargs = get_cb_swaps_kwargs(currency=currency, benchmark_type=benchmark_type)
    if not (re.fullmatch(f"({CCY_TO_CB[currency.value]}[0-9]|1[0-9])", swap_tenor) or
            re.fullmatch(f"({CCY_TO_CB[currency.value]}[0-9]|1[0-9]|0b)", forward_tenor)):
        raise MqValueError('invalid swap tenor ' + swap_tenor)
    kwargs['asset_parameters_termination_date'] = swap_tenor
    kwargs['asset_parameters_effective_date'] = forward_tenor
    return _get_tdapi_rates_assets(**kwargs)


def get_cb_swap_data(currency: CurrencyEnum, rate_mqids: list = None):
    ds = Dataset(Dataset.GS.IR_SWAP_RATES_INTRADAY_CALC_BANK)
    pricing_location = _default_pricing_location(currency)
    pricing_location = _pricing_location_normalized(pricing_location, currency)
    cbw_df = ds.get_data(assetId=rate_mqids,
                         pricingLocation=pricing_location.value,
                         startTime=DataContext.current.start_time,
                         endTime=DataContext.current.end_time)
    return cbw_df


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=currency_to_default_ois_asset,
                                 query_type=QueryType.CENTRAL_BANK_SWAP_RATE)])
def policy_rate_term_structure(asset: Asset, event_type: EventType = EventType.MEETING,
                               rate_type: RateType = RateType.ABSOLUTE,
                               valuation_date: Optional[GENERIC_DATE] = None, *,
                               source: str = None, real_time: bool = False) -> pd.Series:
    """
    Forward Policy Rate expectations for future Central Bank meetings or End Of Year Dates as of specified date.

    :param asset: Currency
    :param event_type: Spot= Effective OIS/Policy rate, Meeting = Forward Expectations across all future CB meetings,
                    EOY = Forward Expectations at End of Year Dates
    :param rate_type:  One of (absolute, relative), where relative = forward - spot rate to show what
                hikes/cuts are priced in by the market.
    :param valuation_date:  reference date on which all future expectations are calculated, Eg. 3m: for 3 months ago,
                    2022-05-02 : for expectations as of 02May22, Intraday: how expectations are changing intraday.
    :param source: name of function caller: default source = None
    :param real_time: whether to retrieve intraday data instead of EOD: default value = False
    :return: OIS Swap Rate Term structure for swaps structured between consecutive CB meeting dates
    """
    check_forward_looking(valuation_date, source, 'policy_rate_expectation')
    if real_time:
        raise NotImplementedError('change end date to +10y in date picker and specify '
                                  'valuation_date = "Intraday" for real-time policy rate term structure')
    if not isinstance(event_type, EventType):
        raise MqValueError('event_type must be one of Spot, Meeting Forward and EOY Forward')
    if not isinstance(rate_type, RateType):
        raise MqValueError('event_type must be either absolute or relative')

    if isinstance(valuation_date, str) and valuation_date.lower() == "intraday":
        return policy_rate_term_structure_rt(asset=asset, event_type=event_type, rate_type=rate_type,
                                             benchmark_type=None, source=source)
    else:
        valuation_date = parse_meeting_date(valuation_date)
        mqid = convert_asset_for_rates_data_set(asset, RatesConversionType.OIS_BENCHMARK_RATE)

        _logger.debug(
            'where assetId=%s, metric=Central Bank Swap Rate, event_type=%s, event_type=%s, valuation date=%s',
            mqid, event_type, rate_type, str(valuation_date))

        ds = Dataset(Dataset.GS.CENTRAL_BANK_WATCH)
        if event_type == EventType.SPOT:
            if rate_type == RateType.RELATIVE:
                raise MqValueError('rate_type must be absolute for event_type = Spot')
            else:
                df = ds.get_data(assetId=[mqid], rateType=event_type, start=CENTRAL_BANK_WATCH_START_DATE)
        else:
            df = ds.get_data(assetId=[mqid], rateType=event_type, valuationDate=valuation_date,
                             start=CENTRAL_BANK_WATCH_START_DATE)

    if rate_type == RateType.RELATIVE:
        # df = remove_dates_with_null_entries(df)
        spot = df[df['meetingNumber'] == 0]['value'][0]
        df['value'] = df['value'] - spot

    try:
        df = df.reset_index()
        df = df.set_index('meetingDate')
        series = ExtendedSeries(df['value'])
        series.dataset_ids = (Dataset.GS.CENTRAL_BANK_WATCH,)
    except KeyError:  # No data returned from ds.get_data
        series = pd.Series(dtype=float, name='value')
    return series


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=currency_to_default_ois_asset,
                                 query_type=QueryType.POLICY_RATE_EXPECTATION)])
def policy_rate_expectation(asset: Asset, event_type: EventType = EventType.MEETING,
                            rate_type: RateType = RateType.ABSOLUTE,
                            meeting_date: Union[datetime.date, int, str] = 0,
                            *, source: str = None, real_time: bool = False) -> pd.Series:
    """'
    Evolution of OIS/policy rate expectations for a given meeting date or end of year date.

    :param asset: asset object loaded from security master
    :param meeting_date: Actual meeting date eg. Date(2022-04-02) or meeting number standing today : 0 for last,
                            1 for next , 2 for meeting after next and so on
    :param rate_type: One of (absolute, relative), where relative = forward - spot rate to show what hikes/cuts are
                    priced in by the market for specified meeting date.
    :param event_type: Spot= Effective OIS/Policy rate, Meeting = Evolution of Rate Expectations for a given meeting
                    date, EOY =  Evolution of Rate Expectations for specified End of Year Date.
    :param source: name of function caller: default source = None
    :param real_time: whether to retrieve intraday data instead of EOD: default value = False
    :return: Historical policy rate expectations for a given CB meeting date or an End of Year date.
    """

    if not isinstance(event_type, EventType):
        raise MqValueError('invalid event_type specified, Meeting Forward, Spot or EOY Forward allowed')
    if not isinstance(rate_type, RateType):
        raise MqValueError('event_type must be either absolute or relative')
    if not isinstance(meeting_date, (datetime.date, str, int)):
        raise MqValueError('valuation_date must be of type datetime.date or string YYYY-MM-DD or integer')

    if real_time:
        return policy_rate_expectation_rt(asset, event_type, rate_type, meeting_date=meeting_date,
                                          benchmark_type=None)
    else:
        mqid = convert_asset_for_rates_data_set(asset, RatesConversionType.OIS_BENCHMARK_RATE)
        _logger.debug('where assetId=%s, metric=Policy Rate Expectation, meeting_date=%s, event_type=%s',
                      mqid, str(meeting_date), rate_type)

        ds = Dataset(Dataset.GS.CENTRAL_BANK_WATCH)
        if event_type == EventType.SPOT:
            cbw_df = ds.get_data(assetId=[mqid], rateType=event_type, start=CENTRAL_BANK_WATCH_START_DATE)
        elif isinstance(meeting_date, int):
            meeting_number = meeting_date
            if meeting_number < 0 or meeting_number > 20:
                raise MqValueError('meeting_number has to be an integer between 0 and 20 where 0 is the '
                                   'last meeting and 1 is the next meeting')
            cbw_df = ds.get_data(assetId=[mqid], rateType=event_type, meetingNumber=meeting_number,
                                 start=CENTRAL_BANK_WATCH_START_DATE)
        else:
            meeting_date = parse_meeting_date(meeting_date)
            cbw_df = ds.get_data(assetId=[mqid], rateType=event_type, meetingDate=meeting_date,
                                 start=CENTRAL_BANK_WATCH_START_DATE)

    if cbw_df.empty:
        raise MqValueError('meeting date specified returned no data')

    if rate_type == RateType.RELATIVE:
        spot_df = ds.get_data(assetId=[mqid], rateType=event_type, meetingNumber=0,
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
    series.dataset_ids = (Dataset.GS.CENTRAL_BANK_WATCH,)
    return series


def parse_meeting_date(valuation_date: Optional[GENERIC_DATE] = None):
    if isinstance(valuation_date, str):
        if len(valuation_date.split('-')) == 3:
            year, month, day = valuation_date.split('-')
            return datetime.date(int(year), int(month), int(day))
        else:
            start, valuation_date = _range_from_pricing_date('USD', valuation_date)
            return valuation_date.date() if isinstance(valuation_date, pd.Timestamp) else valuation_date
    elif isinstance(valuation_date, datetime.date) or valuation_date is None:
        start, valuation_date = _range_from_pricing_date(None, valuation_date)
        return valuation_date.date() if isinstance(valuation_date, pd.Timestamp) else valuation_date
    else:
        raise MqValueError(
            'valuation_date must be of type datetime.date or string YYYY-MM-DD or relative date strings like 1m, 1y')


def _get_default_ois_benchmark(currency: CurrencyEnum) -> BenchmarkTypeCB:
    if currency == CurrencyEnum.USD:
        return BenchmarkTypeCB.Fed_Funds
    elif currency == CurrencyEnum.GBP:
        return BenchmarkTypeCB.SONIA
    elif currency == CurrencyEnum.EUR:
        return BenchmarkTypeCB.EUROSTR


def _check_cb_ccy_benchmark_rt(asset: Asset, benchmark_type: BenchmarkTypeCB) -> tuple:
    bbid = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)
    currency = CurrencyEnum(bbid)
    if currency not in [CurrencyEnum.EUR, CurrencyEnum.GBP, CurrencyEnum.USD]:
        raise MqValueError('Only EUR, GBP and USD are supported for real time Central Bank swap data')
    if benchmark_type is None:
        benchmark_type = _get_default_ois_benchmark(currency)
    if isinstance(benchmark_type, BenchmarkTypeCB) and \
            benchmark_type.value not in CURRENCY_TO_SWAP_RATE_BENCHMARK[currency.value].keys():
        raise MqValueError('%s is not supported for %s', benchmark_type.value, currency.value)
    return currency, benchmark_type


def _get_swap_from_meeting_date(currency: CurrencyEnum, benchmark_type: BenchmarkTypeCB,
                                meeting_date: Union[datetime.date, int, str]) -> str:
    if isinstance(meeting_date, int):
        if meeting_date == 0:
            forward_tenor = '0b'
        else:
            forward_tenor = f"{CCY_TO_CB[currency.value]}{meeting_date}"
        swap_tenor = f"{CCY_TO_CB[currency.value]}{str(meeting_date + 1)}"
    elif isinstance(meeting_date, str) and re.fullmatch(f"({CCY_TO_CB[currency.value]}[0-9]|1[0-9])", meeting_date):
        if meeting_date[-1] == '0':
            forward_tenor = '0b'
        else:
            forward_tenor = f"{CCY_TO_CB[currency.value]}{meeting_date[-1]}"
        swap_tenor = f"{CCY_TO_CB[currency.value]}{str(int(meeting_date[-1]) + 1)}"
    else:
        raise MqValueError('only meeting dates of the type ecb1, mpc1, frb1 or an integer 1,2...20 for next'
                           ' meeting are available for real time central bank data')
    rate_mqid = get_cb_meeting_swap(currency, benchmark_type, forward_tenor=forward_tenor, swap_tenor=swap_tenor)
    return rate_mqid


def policy_rate_expectation_rt(asset: Asset, event_type: EventType = EventType.MEETING,
                               rate_type: RateType = RateType.ABSOLUTE,
                               meeting_date: Union[datetime.date, int, str] = 0,
                               benchmark_type: BenchmarkTypeCB = None):
    currency, benchmark_type = _check_cb_ccy_benchmark_rt(asset, benchmark_type)
    rate_mqid = _get_swap_from_meeting_date(currency, benchmark_type, meeting_date)
    cbw_df = get_cb_swap_data(currency=currency, rate_mqids=rate_mqid)
    if cbw_df.empty:
        raise MqValueError('meeting date specified returned no data')

    if event_type == EventType.SPOT:
        if rate_type == RateType.ABSOLUTE:
            series = ExtendedSeries(cbw_df['rate'])
            series.dataset_ids = (Dataset.GS.IR_SWAP_RATES_INTRADAY_CALC_BANK,)
            return series
        else:
            raise MqValueError('rate_type must be absolute for event_type = Spot')
    elif event_type == EventType.MEETING:
        if rate_type == RateType.RELATIVE:
            spot_id = get_cb_meeting_swap(currency, benchmark_type, '0b', f"{CCY_TO_CB[currency.value]}1")
            spot_df = get_cb_swap_data(currency, spot_id)
            if spot_df.empty:
                raise MqValueError('no spot data returned to rebase')
            joined_df = cbw_df.merge(spot_df,
                                     on=['time', 'pricingLocation', 'csaTerms', 'currency'],
                                     how='inner',
                                     suffixes=['_meeting', '_spot'])
            joined_df['rate'] = (joined_df['rate_meeting'] - joined_df['rate_spot'])
            series = ExtendedSeries(joined_df['rate'])
        else:
            series = ExtendedSeries(cbw_df['rate'])
        series.dataset_ids = (Dataset.GS.IR_SWAP_RATES_INTRADAY_CALC_BANK,)
        return series
    else:
        raise MqValueError("Real Time End of Year pricing is not supported")


def policy_rate_term_structure_rt(asset: Asset, event_type: EventType = EventType.MEETING,
                                  rate_type: RateType = RateType.ABSOLUTE,
                                  benchmark_type: BenchmarkTypeCB = None, source: str = None):
    currency, benchmark_type = _check_cb_ccy_benchmark_rt(asset, benchmark_type)

    if event_type == EventType.SPOT:
        if rate_type == RateType.RELATIVE:
            raise MqValueError('rate_type must be absolute for event_type = Spot')
        else:
            mqid = get_cb_meeting_swap(currency, benchmark_type=benchmark_type, forward_tenor='0b',
                                       swap_tenor=f"{CCY_TO_CB[currency.value]}1")
            spot_df = get_cb_swap_data(currency, [mqid])
            if spot_df.empty:
                raise MqValueError('no spot data returned')
            series = ExtendedSeries(spot_df['rate'])
            series.dataset_ids = (Dataset.GS.IR_SWAP_RATES_INTRADAY_CALC_BANK,)
            return series
    elif event_type == EventType.MEETING:
        mqids = get_cb_meeting_swaps(currency, benchmark_type=benchmark_type)
        cbw_df = get_cb_swap_data(currency, rate_mqids=mqids)
        if cbw_df.empty:
            raise MqValueError('no data returned for specified arguments')
    else:
        raise MqValueError("Real Time End of Year pricing is not supported")

    if rate_type == RateType.RELATIVE:
        spot_id = get_cb_meeting_swap(currency, benchmark_type=benchmark_type,
                                      forward_tenor='0b', swap_tenor=f"{CCY_TO_CB[currency.value]}1")
        spot_df = get_cb_swap_data(currency, spot_id)
        if spot_df.empty:
            raise MqValueError('no spot data returned to rebase')
        joined_df = cbw_df.merge(spot_df,
                                 on=['time', 'pricingLocation', 'csaTerms', 'currency'],
                                 how='inner',
                                 suffixes=['_meeting', '_spot'])
        joined_df['rate'] = (joined_df['rate_meeting'] - joined_df['rate_spot'])
        joined_df = joined_df.rename(columns={'effectiveDate_meeting': 'effectiveDate'})
    else:
        joined_df = cbw_df

    if joined_df.empty:
        series = ExtendedSeries(dtype=float)
    else:
        latest = joined_df.index.max()
        _logger.info('selected pricing date %s', latest)
        joined_df = joined_df.loc[latest]
        biz_day = _get_custom_bd(_default_pricing_location(currency).value)
        # col_to_plot = 'effectiveTenor'
        col_to_plot = 'effectiveDate'
        joined_df.loc[:, 'expirationDate'] = joined_df[col_to_plot].apply(_get_term_struct_date,
                                                                          args=(latest, biz_day))
        joined_df = joined_df.set_index('expirationDate')
        joined_df.sort_index(inplace=True)
        joined_df = joined_df.loc[DataContext.current.start_date: DataContext.current.end_date]
        series = ExtendedSeries(dtype=float) if joined_df.empty else ExtendedSeries(joined_df['rate'])
    series.dataset_ids = getattr(joined_df, 'dataset_ids', ())
    if series.empty:  # Raise descriptive error if no data returned + date context is in the past
        check_forward_looking(None, source, 'policy_rate_term_structure')
    return series
