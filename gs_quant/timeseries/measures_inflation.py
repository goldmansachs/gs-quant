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
from collections import OrderedDict
from enum import Enum
from typing import Optional, Union

import pandas as pd
from pandas import Series

from gs_quant.target.common import Currency as CurrencyEnum, AssetClass, AssetType, PricingLocation
from gs_quant.api.gs.assets import GsAssetApi
from gs_quant.api.gs.data import QueryType, GsDataApi

from gs_quant.errors import MqValueError
from gs_quant.timeseries import ExtendedSeries, measures_rates as tm_rates
from gs_quant.timeseries.measures import _asset_from_spec, _market_data_timed

from gs_quant.markets.securities import AssetIdentifier, Asset
from gs_quant.timeseries import ASSET_SPEC, plot_measure, MeasureDependency, GENERIC_DATE

_logger = logging.getLogger(__name__)


class InflationIndexType(Enum):
    AUCPI = 'AUCPI'
    BECPHLTH = 'BECPHLTH'
    CACPI = 'CACPI'
    CPALBE = 'CPALBE'
    CPALEMU = 'CPALEMU'
    CPUPAXFE = 'CPUPAXFE'
    CPURNSA = 'CPURNSA'
    CPUS = 'CPUS'
    CPXTEMU = 'CPXTEMU'
    DNCPINEW = 'DNCPINEW'
    FRCPXTOB = 'FRCPXTOB'
    GKCPIUHL = 'GKCPIUHL'
    GKCPNEWL = 'GKCPNEWL'
    GRCP2010 = 'GRCP2010'
    GRCPTK = 'GRCPTK'
    IECPALL = 'IECPALL'
    IECPEUI = 'IECPEUI'
    IECPINEW = 'IECPINEW'
    ILCPI = 'ILCPI'
    INFINFY = 'INFINFY'
    ISCPIL = 'ISCPIL'
    ITCPI = 'ITCPI'
    ITCPNICT = 'ITCPNICT'
    JCPNGENF = 'JCPNGENF'
    KRCPI = 'KRCPI'
    MXNInfl = 'MXNInfl'
    NECPIND = 'NECPIND'
    NOCPI = 'NOCPI'
    POCPILB = 'POCPILB'
    PPFXFDE = 'PPFXFDE'
    RUCP2000 = 'RUCP2000'
    SACPI = 'SACPI'
    SPCPEU = 'SPCPEU'
    SPIPC = 'SPIPC'
    SWCPI = 'SWCPI'
    UKCPI = 'UKCPI'
    UKCPIH = 'UKCPIH'
    UKRPI = 'UKRPI'
    TESTCPI = 'TESTCPI'


class TdapiInflationRatesDefaultsProvider:
    # flag to indicate that a given property should not  be included in asset query
    EMPTY_PROPERTY = "null"

    def __init__(self, defaults: dict):
        self.defaults = defaults
        benchmark_mappings = {}
        for k, v in defaults.get("CURRENCIES").items():
            for e in v:
                benchmark_mappings[k] = {e.get("IndexType"): e.get('Index')}
        self.defaults['MAPPING'] = benchmark_mappings

    def get_index_for_benchmark(self, currency: CurrencyEnum, benchmark: str):
        return self.defaults.get("MAPPING").get(currency.value).get(benchmark)


INFLATION_RATES_DEFAULTS = {
    "CURRENCIES": {
        "EUR": [
            {"IndexType": "CPXTEMU", "Index": "CPI-CPXTEMU",
             "pricingLocation": ["LDN"]},
            {"IndexType": "FRCPXTOB", "Index": "CPI-FRCPXTOB",
             "pricingLocation": ["LDN"]}
        ],
        "USD": [{"IndexType": "CPURNSA", "Index": "CPI-CPURNSA",
                 "pricingLocation": ["NYC"]}],
        "GBP": [{"IndexType": "UKRPI", "Index": "CPI-UKRPI",
                 "pricingLocation": ["LDN"]}],
        "JPY": [{"IndexType": "JCPNGENF", "Index": "CPI-JCPNGENF",
                 "pricingLocation": ["TKO"]}],
    },
    "COMMON": {
        "fixedRate": "ATM",
        "clearingHouse": "LCH",
        "terminationDate": "5y",
        "effectiveDate": "0b"
    }
}
inflationRates_defaults_provider = TdapiInflationRatesDefaultsProvider(INFLATION_RATES_DEFAULTS)

CURRENCY_TO_INDEX_BENCHMARK = {
    'AUD': OrderedDict([('AUCPI', 'CPI-AUCPI')]),
    'CAD': OrderedDict([('CACPI', 'CPI-CACPI')]),
    'DKK': OrderedDict([('DNCPINEW', 'CPI-DNCPINEW')]),
    'EUR': OrderedDict(
        [('CPXTEMU', 'CPI-CPXTEMU'), ('BECPHLTH', 'CPI-BECPHLTH'), ('CPALBE', 'CPI-CPALBE'), ('CPALEMU', 'CPI-CPALEMU'),
         ('FRCPXTOB', 'CPI-FRCPXTOB'), ('GKCPIUHL', 'CPI-GKCPIUHL'), ('GKCPNEWL', 'CPI-GKCPNEWL'),
         ('GRCP2010', 'CPI-GRCP2010'), ('GRCPTK', 'CPI-GRCPTK'), ('IECPALL', 'CPI-IECPALL'), ('IECPEUI', 'CPI-IECPEUI'),
         ('IECPINEW', 'CPI-IECPINEW'), ('ITCPI', 'CPI-ITCPI'), ('ITCPNICT', 'CPI-ITCPNICT'), ('MXNInfl', 'CPI-MXNInfl'),
         ('NECPIND', 'CPI-NECPIND'), ('SPCPEU', 'CPI-SPCPEU'), ('SPIPC', 'CPI-SPIPC')]),
    'GBP': OrderedDict([('UKRPI', 'CPI-UKRPI'), ('UKCPI', 'CPI-UKCPI'), ('UKCPIH', 'CPI-UKCPIH')]),
    'ILS': OrderedDict([('ILCPI', 'CPI-ILCPI'), ('ISCPIL', 'CPI-ISCPIL')]),
    'INR': OrderedDict([('INFINFY', 'CPI-INFINFY')]),
    'JPY': OrderedDict([('JCPNGENF', 'CPI-JCPNGENF')]),
    'KOR': OrderedDict([('KRCPI', 'CPI-KRCPI')]),
    'NOK': OrderedDict([('NOCPI', 'CPI-NOCPI')]),
    'PLN': OrderedDict([('POCPILB', 'CPI-POCPILB')]),
    'RUB': OrderedDict([('RUCP2000', 'CPI-RUCP2000')]),
    'SEK': OrderedDict([('SWCPI', 'CPI-SWCPI')]),
    'USD': OrderedDict(
        [('CPURNSA', 'CPI-CPURNSA'), ('CPUPAXFE', 'CPI-CPUPAXFE'), ('CPUS', 'CPI-CPUS'), ('PPFXFDE', 'CPI-PPFXFDE')]),
    'ZAR': OrderedDict([('SACPI', 'CPI-SACPI')])
}

CURRENCY_TO_DUMMY_INFLATION_SWAP_BBID = {
    'EUR': 'MAJTD8XDA8EJZYRG',
    'GBP': 'MAW75DV9777630QN',
    'JPY': 'MA1CENMCA88VXJ28',
    'USD': 'MA4016GCT3MDRYVY',
}


def _currency_to_tdapi_inflation_swap_rate_asset(asset_spec: ASSET_SPEC) -> str:
    asset = _asset_from_spec(asset_spec)
    bbid = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)
    # for each currency, get a dummy asset for checking availability
    result = CURRENCY_TO_DUMMY_INFLATION_SWAP_BBID.get(bbid, asset.get_marquee_id())
    return result


def _get_tdapi_inflation_rates_assets(allow_many=False, **kwargs) -> Union[str, list]:
    # sanitize input for asset query.
    if "pricing_location" in kwargs:
        del kwargs["pricing_location"]
    assets = GsAssetApi.get_many_assets(**kwargs)

    if len(assets) == 0 and ('asset_parameters_clearing_house' in kwargs):  # test without the clearing house
        if kwargs['asset_parameters_clearing_house'] == tm_rates._ClearingHouse.NONE.value:
            del kwargs['asset_parameters_clearing_house']
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


def _check_inflation_index_type(currency, benchmark_type: Union[InflationIndexType, str]) -> InflationIndexType:
    if isinstance(benchmark_type, str):
        if benchmark_type.upper() in InflationIndexType.__members__:
            benchmark_type = InflationIndexType[benchmark_type.upper()]
        else:
            raise MqValueError(benchmark_type + ' is not a valid index, pick one among ' +
                               ', '.join([x.value for x in InflationIndexType]))

    if isinstance(benchmark_type, InflationIndexType) and \
            benchmark_type.value not in CURRENCY_TO_INDEX_BENCHMARK[currency.value].keys():
        raise MqValueError('%s is not supported for %s', benchmark_type.value, currency.value)
    else:
        return benchmark_type


def _get_inflation_swap_leg_defaults(currency: CurrencyEnum, benchmark_type: InflationIndexType = None) -> dict:
    pricing_location = tm_rates.CURRENCY_TO_PRICING_LOCATION.get(currency, PricingLocation.LDN)
    # default benchmark types
    if benchmark_type is None:
        benchmark_type = InflationIndexType(str(list(CURRENCY_TO_INDEX_BENCHMARK[currency.value].keys())[0]))
    benchmark_type_input = CURRENCY_TO_INDEX_BENCHMARK[currency.value].get(benchmark_type.value,
                                                                           "CPI-" + benchmark_type.value)
    return dict(currency=currency, index_type=benchmark_type_input,
                pricing_location=pricing_location)


def _get_inflation_swap_csa_terms(curr: str, inflationindextype: str) -> dict:
    return dict(csaTerms=curr + '-1')


def _get_inflation_swap_data(asset: Asset, swap_tenor: str, index_type: str = None,
                             forward_tenor: Optional[GENERIC_DATE] = None,
                             clearing_house: tm_rates._ClearingHouse = None,
                             source: str = None, real_time: bool = False,
                             query_type: QueryType = QueryType.SWAP_RATE,
                             location: PricingLocation = None) -> pd.DataFrame:
    if real_time:
        raise NotImplementedError('realtime inflation swap data not implemented')
    currency = CurrencyEnum(asset.get_identifier(AssetIdentifier.BLOOMBERG_ID))

    if currency.value not in CURRENCY_TO_INDEX_BENCHMARK.keys():
        raise NotImplementedError('Data not available for {} inflation swap rates'.format(currency.value))
    index_type = _check_inflation_index_type(currency, index_type)

    clearing_house = tm_rates._check_clearing_house(clearing_house)

    defaults = _get_inflation_swap_leg_defaults(currency, index_type)

    if not (tm_rates._is_valid_relative_date_tenor(swap_tenor)):
        raise MqValueError('invalid swap tenor ' + swap_tenor)

    forward_tenor = tm_rates._check_forward_tenor(forward_tenor)

    fixed_rate = 'ATM'
    kwargs = dict(asset_class='Rates',
                  type='InflationSwap', asset_parameters_termination_date=swap_tenor,
                  asset_parameters_index=defaults['index_type'],
                  asset_parameters_fixed_rate=fixed_rate,
                  asset_parameters_clearing_house=clearing_house.value,
                  asset_parameters_effective_date=forward_tenor,
                  asset_parameters_notional_currency=currency.name)

    rate_mqid = _get_tdapi_inflation_rates_assets(**kwargs)

    if location is None:
        pricing_location = tm_rates._default_pricing_location(currency)
    else:
        pricing_location = PricingLocation(location)
    pricing_location = tm_rates._pricing_location_normalized(pricing_location, currency)
    where = dict(pricingLocation=pricing_location.value)

    _logger.debug(f'where asset= {rate_mqid}, swap_tenor={swap_tenor}, index={defaults["index_type"]}, '
                  f'forward_tenor={forward_tenor}, pricing_location={pricing_location.value}, '
                  f'clearing_house={clearing_house.value}, notional_currency={currency.name}')
    q = GsDataApi.build_market_data_query([rate_mqid], query_type, where=where, source=source,
                                          real_time=real_time)
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return df


@plot_measure((AssetClass.Cash,), (AssetType.Currency,),
              [MeasureDependency(id_provider=_currency_to_tdapi_inflation_swap_rate_asset,
                                 query_type=QueryType.SWAP_RATE)])
def inflation_swap_rate(asset: Asset, swap_tenor: str, index_type: str = None,
                        forward_tenor: Optional[GENERIC_DATE] = None, clearing_house: tm_rates._ClearingHouse = None,
                        location: PricingLocation = None, *,
                        source: str = None, real_time: bool = False) -> Series:
    """
    GS end-of-day Zero Coupon Inflation Swap curves across major currencies.

    :param asset: asset object loaded from security master
    :param swap_tenor: relative date representation of expiration date e.g. 1m
    :param index_type: benchmark type e.g. UKRPI
    :param forward_tenor: absolute / relative date representation of forward starting point eg: '1y' or 'Spot' for
            spot starting swaps, 'imm1' or 'frb1'
    :param clearing_house: Example - "LCH", "EUREX", "JSCC", "CME"
    :param location: Example - "TKO", "LDN", "NYC"
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: swap rate curve
    """
    df = _get_inflation_swap_data(asset=asset, swap_tenor=swap_tenor, index_type=index_type,
                                  forward_tenor=forward_tenor,
                                  clearing_house=clearing_house, source=source,
                                  real_time=real_time, query_type=QueryType.SWAP_RATE, location=location)

    series = ExtendedSeries() if df.empty else ExtendedSeries(df['swapRate'])
    series.dataset_ids = getattr(df, 'dataset_ids', ())
    return series
