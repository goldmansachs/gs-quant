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
from enum import Enum
from numbers import Real
from typing import Union, Optional

import pandas as pd
from pandas import Series

from gs_quant.api.gs.assets import GsAssetApi
from gs_quant.api.gs.data import QueryType, GsDataApi
from gs_quant.errors import MqValueError
from gs_quant.markets.securities import AssetIdentifier, Asset, SecurityMaster
from gs_quant.target.common import AssetClass, AssetType, PricingLocation
from gs_quant.timeseries import ASSET_SPEC, plot_measure, MeasureDependency
from gs_quant.timeseries import ExtendedSeries, measures_rates as tm_rates
from gs_quant.timeseries.measures import _asset_from_spec, _market_data_timed, _cross_stored_direction_helper, \
    _preprocess_implied_vol_strikes_fx, _tenor_month_to_year
from gs_quant.timeseries.measures_helper import VolReference

_logger = logging.getLogger(__name__)


class OptionType(Enum):
    CALL = 'Call'
    PUT = 'Put'
    STRADDLE = 'Straddle'


class TdapiFXDefaultsProvider:
    # flag to indicate that a given property should not  be included in asset query
    EMPTY_PROPERTY = "null"

    def __init__(self, defaults: dict):
        self.defaults = defaults

    def get_defaults_for_cross(self, cross: str):
        return dict(self.defaults.get(cross))


FX_DEFAULTS = {
    "AUDCAD": {"under": "AUD", "over": "CAD",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "AUDJPY": {"under": "AUD", "over": "JPY",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "AUDUSD": {"under": "AUD", "over": "USD",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "BRLJPY": {"under": "BRL", "over": "JPY",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "CADJPY": {"under": "CAD", "over": "JPY",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "CADMXN": {"under": "CAD", "over": "MXN",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "CHFJPY": {"under": "CHF", "over": "JPY",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "CNHJPY": {"under": "CNH", "over": "JPY",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURAUD": {"under": "EUR", "over": "AUD",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURBRL": {"under": "EUR", "over": "BRL",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURCAD": {"under": "EUR", "over": "CAD",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURCHF": {"under": "EUR", "over": "CHF",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURCLP": {"under": "EUR", "over": "CLP",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURCNH": {"under": "EUR", "over": "CNH",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURCZK": {"under": "EUR", "over": "CZK",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURGBP": {"under": "EUR", "over": "GBP",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURHUF": {"under": "EUR", "over": "HUF",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURILS": {"under": "EUR", "over": "ILS",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURINR": {"under": "EUR", "over": "INR",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURJPY": {"under": "EUR", "over": "JPY",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURKRW": {"under": "EUR", "over": "KRW",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURMXN": {"under": "EUR", "over": "MXN",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURNOK": {"under": "EUR", "over": "NOK",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURNZD": {"under": "EUR", "over": "NZD",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURPLN": {"under": "EUR", "over": "PLN",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURRUB": {"under": "EUR", "over": "RUB",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURSEK": {"under": "EUR", "over": "SEK",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURTRY": {"under": "EUR", "over": "TRY",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURUSD": {"under": "EUR", "over": "USD",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURZAR": {"under": "EUR", "over": "ZAR",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "GBPJPY": {"under": "GBP", "over": "JPY",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "GBPUSD": {"under": "GBP", "over": "USD",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "HUFJPY": {"under": "HUF", "over": "JPY",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "ILSJPY": {"under": "ILS", "over": "JPY",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "INRJPY": {"under": "INR", "over": "JPY",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "JPYKRW": {"under": "JPY", "over": "KRW",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "MXNJPY": {"under": "MXN", "over": "JPY",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "NOKJPY": {"under": "NOK", "over": "JPY",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "NZDJPY": {"under": "NZD", "over": "JPY",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "NZDUSD": {"under": "NZD", "over": "USD",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "PLNJPY": {"under": "PLN", "over": "JPY",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "RUBJPY": {"under": "RUB", "over": "JPY",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "SEKJPY": {"under": "SEK", "over": "JPY",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDBRL": {"under": "USD", "over": "BRL",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDCAD": {"under": "USD", "over": "CAD",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDCHF": {"under": "USD", "over": "CHF",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDCLP": {"under": "USD", "over": "CLP",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDCNH": {"under": "USD", "over": "CNH",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDCOP": {"under": "USD", "over": "COP",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDHUF": {"under": "USD", "over": "HUF",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDIDR": {"under": "USD", "over": "IDR",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDILS": {"under": "USD", "over": "ILS",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDINR": {"under": "USD", "over": "INR",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDJPY": {"under": "USD", "over": "JPY",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDKRW": {"under": "USD", "over": "KRW",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDMXN": {"under": "USD", "over": "MXN",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDNOK": {"under": "USD", "over": "NOK",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDPHP": {"under": "USD", "over": "PHP",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDPLN": {"under": "USD", "over": "PLN",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDRUB": {"under": "USD", "over": "RUB",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDSEK": {"under": "USD", "over": "SEK",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDSGD": {"under": "USD", "over": "SGD",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDTRY": {"under": "USD", "over": "TRY",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDTWD": {"under": "USD", "over": "TWD",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDZAR": {"under": "USD", "over": "ZAR",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"}
}
fx_defaults_provider = TdapiFXDefaultsProvider(FX_DEFAULTS)

FX_VOL_SWAP_DEFAULTS = [
    "EURUSD",
    "GBPUSD",
    "USDCHF",
    "DKKUSD",
    "NOKUSD",
    "SEKUSD",
    "USDCAD",
    "USDJPY",
    "AUDUSD",
    "NZDUSD",
    "USDCNH",
    "INRUSD",
    "USDSGD"
]

CURRENCY_TO_DUMMY_FFO_BBID = {
    'AUDCAD': 'MA4TJRN9MBET5NKS',
    'AUDJPY': 'MAH5X6NHGRBKMWPE',
    'AUDUSD': 'MAN0G5EB00H14W0S',
    'BRLJPY': 'MA1WP7QREXS9WZVQ',
    'CADJPY': 'MAVHN1MPE1X9JW52',
    'CADMXN': 'MAE2415EP4XX6ACZ',
    'CHFJPY': 'MAJ7VVAY60D3E2WE',
    'CNHJPY': 'MAEF5B5SYGCADZQJ',
    'EURAUD': 'MAN5S7K3N5K7TAYQ',
    'EURBRL': 'MA9CQ07TPZFWR37M',
    'EURCAD': 'MA46Z26SSKTC26X0',
    'EURCHF': 'MAX77PXQC2B09S30',
    'EURCLP': 'MAYYHB7XGPS49B5P',
    'EURCNH': 'MA6S2DN8YER1ZWNK',
    'EURCZK': 'MAH68Y664M87S2WK',
    'EURGBP': 'MAXGQ18G9245FMFN',
    'EURHUF': 'MAQY2AFQGAGMWA86',
    'EURILS': 'MA80D8MWZJA884M7',
    'EURINR': 'MA9M0AD4XF4PZDJ4',
    'EURJPY': 'MATCYWGHQCM89K72',
    'EURKRW': 'MATRZZCW5H78ZMNX',
    'EURMXN': 'MAH2P631H1JXERTK',
    'EURNOK': 'MA3WQVT62D4C0ZQ8',
    'EURNZD': 'MA28186ESNB3HR6A',
    'EURPLN': 'MAFEVSPC80GP6PJX',
    'EURRUB': 'MANABN4EAX6YYB3D',
    'EURSEK': 'MA0FCJ0QXH4F73VE',
    'EURTRY': 'MAY54D9K3PYCT18A',
    'EURUSD': 'MAT1J37C9ZPMANFP',
    'EURZAR': 'MAPNZ5Z1X18YNKN3',
    'GBPJPY': 'MATJS76YB4JSCSCA',
    'GBPUSD': 'MAEHA6WVHJ2S3JY9',
    'HUFJPY': 'MA98M1V3YEMS5XEB',
    'ILSJPY': 'MA6S47WRX6F498JB',
    'INRJPY': 'MAJEZ70FKX95F5M7',
    'JPYKRW': 'MA3WF2A5FHGBVJ6X',
    'MXNJPY': 'MABS05Q0848GQCQW',
    'NOKJPY': 'MAF5TG7GKB5ZCWDY',
    'NZDJPY': 'MABZBJSAPM9KHASD',
    'NZDUSD': 'MA18GEASNDN55AHS',
    'PLNJPY': 'MAN2CFHW1Z4XFXQ3',
    'RUBJPY': 'MAHT6HYTYXEK2QY1',
    'SEKJPY': 'MAA0W4P56NZEGZSC',
    'USDBRL': 'MA2CKWJWZXA3A3QQ',
    'USDCAD': 'MAXWBP82QZ3B2304',
    'USDCHF': 'MANPCKXE2H0FQMFC',
    'USDCLP': 'MAS2G31EZJDWEXQ9',
    'USDCNH': 'MA141AAE2NWP5BHN',
    'USDCOP': 'MAPWBD5FQP0W303V',
    'USDHUF': 'MAQEDRH3T69WCA8J',
    'USDIDR': 'MAFKA004WSQEZ6KR',
    'USDILS': 'MAS2AM5ENGQ00MP5',
    'USDINR': 'MA8JP0HYF8CQZCYG',
    'USDJPY': 'MAQ7YRZ4P94M9N9C',
    'USDKRW': 'MAVZG5BFM5VVTYMD',
    'USDMXN': 'MAPAVBP6KQMQJZP3',
    'USDNOK': 'MAFT0XXQASPQ7X1J',
    'USDPHP': 'MA5N37TB77VX7RCR',
    'USDPLN': 'MACNEGC1Q81HK2QP',
    'USDRUB': 'MAXMSS4B5YXE935S',
    'USDSEK': 'MAE4YZ9B2KKVM67J',
    'USDSGD': 'MA9DWW9GPFT7H1A9',
    'USDTRY': 'MA4YKBCXZ4W341YC',
    'USDTWD': 'MAANPDQCDNKV6G2X',
    'USDZAR': 'MA9T8EZ1GXEGY8C3'
}

CURRENCY_TO_DUMMY_FFO_BBID_VOL_SWAPS = {
    "EURUSD": "MA66A4X4PRTC3N7B",
    "GBPUSD": "MA808D9BQ4E396C4",
    "USDCHF": "MAPGXTC189B2111M",
    "DKKUSD": "MABCHYGJ1TCBCQE4",
    "NOKUSD": "MAZ0P16RPG5P0MVF",
    "SEKUSD": "MA4ZD5CZGC3Y6JZD",
    "USDCAD": "MAZPF9SV1M6ZSGFH",
    "USDJPY": "MA3Y28M97R55G16Y",
    "AUDUSD": "MAAEVQXHFBKNDYRP",
    "NZDUSD": "MA9RP21MYV18TW3E",
    "USDCNH": "MAQEB18HP88FEP5G",
    "INRUSD": "MAMC996297G5GEAM",
    "USDSGD": "MAFCHSQN3NH77G17"
}


def _currencypair_to_tdapi_fxfwd_asset(asset_spec: ASSET_SPEC) -> str:
    asset = _asset_from_spec(asset_spec)
    bbid = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)

    kwargs = dict(asset_class='FX', type='Forward',
                  asset_parameters_pair=bbid,
                  asset_parameters_settlement_date='1y',
                  )

    mqid = _get_tdapi_fxo_assets(**kwargs)
    return mqid


def _currencypair_to_tdapi_fxo_asset(asset_spec: ASSET_SPEC) -> str:
    asset = _asset_from_spec(asset_spec)
    bbid = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)
    # for each currency, get a dummy asset for checking availability
    result = CURRENCY_TO_DUMMY_FFO_BBID.get(bbid, asset.get_marquee_id())
    return result


def _currencypair_to_tdapi_fx_vol_swap_asset(asset_spec: ASSET_SPEC) -> str:
    asset = _asset_from_spec(asset_spec)
    bbid = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)
    # for each currency, get a dummy asset for checking availability
    result = CURRENCY_TO_DUMMY_FFO_BBID_VOL_SWAPS.get(bbid, asset.get_marquee_id())
    return result


def _get_tdapi_fxo_assets(**kwargs) -> Union[str, list]:
    # sanitize input for asset query.
    if "pricing_location" in kwargs:
        del kwargs["pricing_location"]
    assets = GsAssetApi.get_many_assets(**kwargs)

    if len(assets) > 1:
        raise MqValueError('Specified arguments match multiple assets' + str(kwargs))
    elif len(assets) == 0:
        raise MqValueError('Specified arguments did not match any asset in the dataset' + str(kwargs))
    else:
        return assets[0].id


def get_fxo_asset(asset: Asset, expiry_tenor: str, strike: str, option_type: str = None,
                  expiration_location: str = None, premium_payment_date: str = None) -> str:
    cross = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)

    if cross not in FX_DEFAULTS.keys():
        raise NotImplementedError('Data not available for {} FX Vanilla options'.format(cross))

    defaults = _get_fxo_defaults(cross)

    if not (tm_rates._is_valid_relative_date_tenor(expiry_tenor)):
        raise MqValueError('invalid expiry ' + expiry_tenor)

    if expiration_location is None:
        _ = defaults["expirationTime"]
    else:
        _ = expiration_location

    if premium_payment_date is None:
        premium_date = defaults["premiumPaymentDate"]
    else:
        premium_date = premium_payment_date

    if option_type == "Put":
        call_ccy = defaults["over"]
        put_ccy = defaults["under"]
    else:
        call_ccy = defaults["under"]
        put_ccy = defaults["over"]

    kwargs = dict(asset_class='FX', type='Option',
                  asset_parameters_call_currency=call_ccy,
                  asset_parameters_put_currency=put_ccy,
                  asset_parameters_expiration_date=expiry_tenor,
                  asset_parameters_option_type=option_type,
                  asset_parameters_premium_payment_date=premium_date,
                  asset_parameters_strike_price_relative=strike,
                  )

    return _get_tdapi_fxo_assets(**kwargs)


def _get_tdapi_fxo_assets_vol_swaps(**kwargs) -> Union[str, list]:
    # sanitize input for asset query.

    expiry_tenor = kwargs.get("expiry_tenor")
    ignore_list = ["expiry_tenor", "pricing_location"]
    inputs = {k: v for k, v in kwargs.items() if k not in ignore_list}

    assets = GsAssetApi.get_many_assets(**inputs)

    # For vol swaps we are not restricting assets using a filter
    # as asset service isn't setup for the parameters we pass in
    # instead query all assets and apply the filter in code here

    if len(assets) == 0:
        raise MqValueError('No assets found matching search criteria' + str(kwargs))

    if expiry_tenor is not None:
        for asset in assets:
            if asset.parameters["lastFixingDate"].lower() == expiry_tenor.lower():
                return asset.id
    raise MqValueError('Specified arguments did not match any asset in the dataset' + str(kwargs))


def cross_stored_direction_for_fx_vol(asset_spec: ASSET_SPEC) -> Union[str, Asset]:
    asset = _asset_from_spec(asset_spec)
    result = asset
    try:
        if asset.asset_class is AssetClass.FX:
            bbid = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)
            if bbid is not None:
                cross = _cross_stored_direction_helper(bbid)
                if cross != bbid:
                    cross_asset = SecurityMaster.get_asset(cross, AssetIdentifier.BLOOMBERG_ID)
                    result = cross_asset
    except TypeError:
        result = asset
    return _currencypair_to_tdapi_fxo_asset(result)


def _get_fxo_defaults(cross: str) -> dict:
    return fx_defaults_provider.get_defaults_for_cross(cross)


def _get_fx_csa_terms() -> dict:
    return dict(csaTerms='USD-1')


def _get_fx_vol_swap_data(asset: Asset, expiry_tenor: str, strike_type: str = None,
                          location: PricingLocation = None,
                          source: str = None, real_time: bool = False,
                          query_type: QueryType = QueryType.STRIKE_VOL) \
        -> pd.DataFrame:
    if real_time:
        raise NotImplementedError('realtime FX Vol swap data not implemented')

    cross = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)

    if cross not in FX_VOL_SWAP_DEFAULTS:
        raise NotImplementedError('Data not available for {} FX Vol Swaps'.format(cross))

    kwargs = dict(asset_class='FX', type='VolatilitySwap',
                  expiry_tenor=expiry_tenor,
                  asset_parameters_pair=cross,
                  # asset_parameters_strike_vol=strike_type
                  )
    fxv_mqid = _get_tdapi_fxo_assets_vol_swaps(**kwargs)

    if location is None:
        pricing_location = PricingLocation.NYC
    else:
        pricing_location = PricingLocation(location)

    where = dict(pricingLocation=pricing_location.value)

    q = GsDataApi.build_market_data_query([fxv_mqid], query_type, where=where, source=source,
                                          real_time=real_time)
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return df


def _get_fxfwd_data(asset: Asset, settlement_date: str,
                    location: str = None,
                    source: str = None, real_time: bool = False,
                    query_type: QueryType = QueryType.FWD_POINTS) \
        -> pd.DataFrame:
    if real_time:
        mqid = asset.get_identifier(AssetIdentifier.MARQUEE_ID)
        q = GsDataApi.build_market_data_query([mqid], QueryType.FORWARD_POINT, source=source,
                                              real_time=real_time, where={'tenor': settlement_date})
        _logger.debug('q %s', q)
        df = _market_data_timed(q)
        return df

    cross = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)

    if not (tm_rates._is_valid_relative_date_tenor(settlement_date)):
        raise MqValueError('invalid settlements date ' + settlement_date)

    kwargs = dict(asset_class='FX', type='Forward',
                  asset_parameters_pair=cross,
                  asset_parameters_settlement_date=settlement_date,
                  )

    mqid = _get_tdapi_fxo_assets(**kwargs)

    if location is None:
        pricing_location = PricingLocation.NYC
    else:
        pricing_location = PricingLocation(location)

    where = dict(pricingLocation=pricing_location.value)

    q = GsDataApi.build_market_data_query([mqid], query_type, where=where, source=source,
                                          real_time=real_time)
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return df


def _get_fxo_data(asset: Asset, expiry_tenor: str, strike: str, option_type: str = None,
                  expiration_location: str = None,
                  location: PricingLocation = None, premium_payment_date: str = None,
                  source: str = None, real_time: bool = False,
                  query_type: QueryType = QueryType.IMPLIED_VOLATILITY) \
        -> pd.DataFrame:
    if real_time:
        raise NotImplementedError('realtime FX Option data not implemented')

    asset_mqid = get_fxo_asset(asset=asset, expiry_tenor=expiry_tenor, strike=strike, option_type=option_type,
                               expiration_location=expiration_location, premium_payment_date=premium_payment_date)

    if location is None:
        pricing_location = PricingLocation.NYC
    else:
        pricing_location = PricingLocation(location)

    where = dict(pricingLocation=pricing_location.value)

    # _logger.debug(f'where asset= {rate_mqid}, swap_tenor={swap_tenor}, index={defaults["index_type"]}, '
    #              f'forward_tenor={forward_tenor}, pricing_location={pricing_location.value}, '
    #              f'clearing_house={clearing_house.value}, notional_currency={currency.name}')
    q = GsDataApi.build_market_data_query([asset_mqid], query_type, where=where, source=source,
                                          real_time=real_time)
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return df


def implied_volatility_new(asset: Asset, expiry_tenor: str, strike: str, option_type: str = None,
                           expiration_location: str = None,
                           location: PricingLocation = None, premium_payment_date: str = None, *,
                           source: str = None, real_time: bool = False) -> Series:
    """
    GS end-of-day FX vanilla implied volatilities across major crosses.

    :param asset: asset object loaded from security master
    :param expiry_tenor: relative date representation of expiration date e.g. 1m
    :param strike: option strike
    :param option_type: option type (e.g. Put, Call or Straddle )
    :param expiration_location: location indicating the time of the option expiry
    :param location: Example - "TKO", "LDN", "NYC"
    :param premium_payment_date: payment date of the premium Example: Fwd Settle vs Spot
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: swap rate curve
    """

    df = _get_fxo_data(asset=asset, expiry_tenor=expiry_tenor, strike=strike,
                       option_type=option_type,
                       expiration_location=expiration_location,
                       location=location,
                       premium_payment_date=premium_payment_date, source=source,
                       real_time=real_time, query_type=QueryType.IMPLIED_VOLATILITY)

    series = ExtendedSeries(dtype=float) if df.empty else ExtendedSeries(df['impliedVolatility'])
    series.dataset_ids = getattr(df, 'dataset_ids', ())
    return series


"""
New Implementation
"""


@plot_measure((AssetClass.FX,), (AssetType.Cross,),
              [MeasureDependency(id_provider=cross_stored_direction_for_fx_vol,
                                 query_type=QueryType.IMPLIED_VOLATILITY)],
              display_name="implied_volatility")
def implied_volatility_fxvol(asset: Asset, tenor: str, strike_reference: VolReference = None,
                             relative_strike: Real = None, location: Optional[PricingLocation] = None,
                             legacy_implementation: bool = False, *,
                             source: str = None, real_time: bool = False) -> Series:
    """
    Volatility of an asset implied by observations of market prices.

    :param asset: asset object loaded from security master
    :param tenor: relative date representation of expiration date e.g. 1m
            or absolute calendar strips e.g. 'Cal20', 'F20-G20'
    :param strike_reference: reference for strike level. Forward is used for ATMF. Default market convention
            for FX implied vols is delta neutral
    :param relative_strike: strike relative to reference
    :param location: location of the data snapshot Example - "HKG", "LDN", "NYC"
    :param legacy_implementation: Deprecated (supplied values are ignored)
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: implied volatility curve
    """

    bbid = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)
    if bbid is not None:
        cross = _cross_stored_direction_helper(bbid)
        if cross != bbid:
            cross_asset = SecurityMaster.get_asset(cross, AssetIdentifier.BLOOMBERG_ID)
            if strike_reference.value == VolReference.DELTA_CALL.value:
                strike_reference = VolReference.DELTA_PUT
            elif strike_reference.value == VolReference.DELTA_PUT.value:
                strike_reference = VolReference.DELTA_CALL
        else:
            cross_asset = asset
    else:
        raise MqValueError('Badly setup cross ' + asset.name)

    ref_string, relative_strike = _preprocess_implied_vol_strikes_fx(strike_reference, relative_strike)

    if ref_string == 'delta':
        if relative_strike == 0:
            strike = 'DN'
            option_type = OptionType.CALL.value
        else:
            if relative_strike > 0:
                strike = str(relative_strike) + 'D'
                option_type = OptionType.CALL.value
            else:
                strike = str(-relative_strike) + 'D'
                option_type = OptionType.PUT.value
    elif ref_string == VolReference.SPOT.value:
        strike = 'Spot'
        option_type = OptionType.CALL.value
    elif ref_string == VolReference.FORWARD.value:
        strike = 'ATMF'
        option_type = OptionType.CALL.value
    else:
        raise MqValueError('unknown strike_reference and relative_strike combination')

    tenor = _tenor_month_to_year(tenor)
    s = implied_volatility_new(cross_asset, tenor, strike, option_type, location=location, source=source,
                               real_time=real_time)
    return s


@plot_measure((AssetClass.FX,), (AssetType.Cross,),
              [MeasureDependency(id_provider=_currencypair_to_tdapi_fxfwd_asset,
                                 query_type=QueryType.FWD_POINTS)],
              display_name="forward_point")
def fwd_points(asset: Asset, settlement_date: str,
               location: str = None, *, source: str = None, real_time: bool = False) -> Series:
    """
    GS End-of-day FX forward points for G3, G10, and EM crosses.

    :param asset: asset object loaded from security master
    :param settlement_date: relative date representation of expiration date e.g. 1m
    :param location: Example - "TKO", "LDN", "NYC"
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: fwd points
    """
    df = _get_fxfwd_data(asset=asset, settlement_date=settlement_date,
                         location=location, source=source,
                         real_time=real_time, query_type=QueryType.FWD_POINTS)
    if real_time:
        series = ExtendedSeries(dtype=float) if df.empty else ExtendedSeries(df['forwardPoint'])
    else:
        series = ExtendedSeries(dtype=float) if df.empty else ExtendedSeries(df['fwdPoints'])
    series.dataset_ids = getattr(df, 'dataset_ids', ())
    return series


@plot_measure((AssetClass.FX,), (AssetType.Cross,),
              [MeasureDependency(id_provider=_currencypair_to_tdapi_fx_vol_swap_asset,
                                 query_type=QueryType.STRIKE_VOL)])
def vol_swap_strike(asset: Asset, expiry_tenor: str, strike_type: str = None,
                    location: PricingLocation = None, *,
                    source: str = None, real_time: bool = False) -> Series:
    """
    GS end-of-day FX Vol Swaps volatilities across major crosses.

    :param asset: asset object loaded from security master
    :param expiry_tenor: relative date representation of expiration date e.g. 1m
    :param strike_type: option type (e.g. Put, Call or Straddle )
    :param location: Example - "TKO", "LDN", "NYC"
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: curve of vol swap strike
    """
    df = _get_fx_vol_swap_data(asset=asset,
                               expiry_tenor=expiry_tenor,
                               strike_type=strike_type,
                               location=location,
                               source=source,
                               real_time=real_time,
                               query_type=QueryType.STRIKE_VOL)

    series = ExtendedSeries(dtype=float) if df.empty else ExtendedSeries(df['strikeVol'])
    series.dataset_ids = getattr(df, 'dataset_ids', ())
    return series
