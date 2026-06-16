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
from functools import partial
from enum import Enum
from numbers import Real
from typing import Union, Optional

import pandas as pd

from gs_quant.api.gs.assets import GsAssetApi
from gs_quant.api.gs.data import QueryType, GsDataApi
from gs_quant.api.utils import ThreadPoolManager
from gs_quant.common import AssetClass, AssetType, PricingLocation
from gs_quant.data import DataContext, Dataset
from gs_quant.errors import MqValueError
from gs_quant.markets.securities import AssetIdentifier, Asset, SecurityMaster
from gs_quant.timeseries import ASSET_SPEC, plot_measure, MeasureDependency, FXSpotCarry
from gs_quant.timeseries import ExtendedSeries, measures_rates as tm_rates
from gs_quant.timeseries.measures import (
    _asset_from_spec,
    _market_data_timed,
    _cross_stored_direction_helper,
    _preprocess_implied_vol_strikes_fx,
    _range_from_pricing_date,
    _tenor_month_to_year,
    GENERIC_DATE,
)
from gs_quant.timeseries.measures_helper import VolReference

_logger = logging.getLogger(__name__)


class OptionType(Enum):
    CALL = 'Call'
    PUT = 'Put'
    STRADDLE = 'Straddle'


FX_VOL_SMILE_POINTS = (
    (-25, VolReference.DELTA_PUT, 25),
    (-10, VolReference.DELTA_PUT, 10),
    (0, VolReference.DELTA_NEUTRAL, 0),
    (10, VolReference.DELTA_CALL, 10),
    (25, VolReference.DELTA_CALL, 25),
)

# Default no-date requests look back over a small recent window and then pick the latest available point.
FX_VOL_SMILE_DEFAULT_PRICING_DATE_BUFFER = 5


class TdapiFXDefaultsProvider:
    # flag to indicate that a given property should not  be included in asset query
    EMPTY_PROPERTY = "null"

    def __init__(self, defaults: dict):
        self.defaults = defaults

    def get_defaults_for_cross(self, cross: str):
        return dict(self.defaults.get(cross))


FX_DEFAULTS = {
    "AUDCAD": {"under": "AUD", "over": "CAD", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "AUDJPY": {"under": "AUD", "over": "JPY", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "AUDUSD": {"under": "AUD", "over": "USD", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "BRLJPY": {"under": "BRL", "over": "JPY", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "CADJPY": {"under": "CAD", "over": "JPY", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "CADMXN": {"under": "CAD", "over": "MXN", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "CHFJPY": {"under": "CHF", "over": "JPY", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "CNHJPY": {"under": "CNH", "over": "JPY", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURAUD": {"under": "EUR", "over": "AUD", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURBRL": {"under": "EUR", "over": "BRL", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURCAD": {"under": "EUR", "over": "CAD", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURCHF": {"under": "EUR", "over": "CHF", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURCLP": {"under": "EUR", "over": "CLP", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURCNH": {"under": "EUR", "over": "CNH", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURCZK": {"under": "EUR", "over": "CZK", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURGBP": {"under": "EUR", "over": "GBP", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURHUF": {"under": "EUR", "over": "HUF", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURILS": {"under": "EUR", "over": "ILS", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURINR": {"under": "EUR", "over": "INR", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURJPY": {"under": "EUR", "over": "JPY", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURKRW": {"under": "EUR", "over": "KRW", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURMXN": {"under": "EUR", "over": "MXN", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURNOK": {"under": "EUR", "over": "NOK", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURNZD": {"under": "EUR", "over": "NZD", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURPLN": {"under": "EUR", "over": "PLN", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURRUB": {"under": "EUR", "over": "RUB", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURSEK": {"under": "EUR", "over": "SEK", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURTRY": {"under": "EUR", "over": "TRY", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURUSD": {"under": "EUR", "over": "USD", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURZAR": {"under": "EUR", "over": "ZAR", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "GBPJPY": {"under": "GBP", "over": "JPY", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "GBPUSD": {"under": "GBP", "over": "USD", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "HUFJPY": {"under": "HUF", "over": "JPY", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "ILSJPY": {"under": "ILS", "over": "JPY", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "INRJPY": {"under": "INR", "over": "JPY", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "JPYKRW": {"under": "JPY", "over": "KRW", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "MXNJPY": {"under": "MXN", "over": "JPY", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "NOKJPY": {"under": "NOK", "over": "JPY", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "NZDJPY": {"under": "NZD", "over": "JPY", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "NZDUSD": {"under": "NZD", "over": "USD", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "PLNJPY": {"under": "PLN", "over": "JPY", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "RUBJPY": {"under": "RUB", "over": "JPY", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "SEKJPY": {"under": "SEK", "over": "JPY", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDBRL": {"under": "USD", "over": "BRL", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDCAD": {"under": "USD", "over": "CAD", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDCHF": {"under": "USD", "over": "CHF", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDCLP": {"under": "USD", "over": "CLP", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDCNH": {"under": "USD", "over": "CNH", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDCOP": {"under": "USD", "over": "COP", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDHUF": {"under": "USD", "over": "HUF", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDIDR": {"under": "USD", "over": "IDR", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDILS": {"under": "USD", "over": "ILS", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDINR": {"under": "USD", "over": "INR", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDJPY": {"under": "USD", "over": "JPY", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDKRW": {"under": "USD", "over": "KRW", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDMXN": {"under": "USD", "over": "MXN", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDNOK": {"under": "USD", "over": "NOK", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDPHP": {"under": "USD", "over": "PHP", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDPLN": {"under": "USD", "over": "PLN", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDRUB": {"under": "USD", "over": "RUB", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDSEK": {"under": "USD", "over": "SEK", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDSGD": {"under": "USD", "over": "SGD", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDTRY": {"under": "USD", "over": "TRY", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDTWD": {"under": "USD", "over": "TWD", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDZAR": {"under": "USD", "over": "ZAR", "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
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
    "USDSGD",
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
    'USDZAR': 'MA9T8EZ1GXEGY8C3',
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
    "USDSGD": "MAFCHSQN3NH77G17",
}


def _currencypair_to_tdapi_fxfwd_asset(asset_spec: ASSET_SPEC) -> str:
    asset = _asset_from_spec(asset_spec)
    bbid = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)

    kwargs = dict(
        asset_class='FX',
        type='Forward',
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
    name_prefix = kwargs.pop("name_prefix", None)
    assets = GsAssetApi.get_many_assets(**kwargs)

    if len(assets) > 1:
        if name_prefix:
            for asset in assets:
                if asset.name.startswith(name_prefix):
                    return asset.id
        raise MqValueError('Specified arguments match multiple assets' + str(kwargs))
    elif len(assets) == 0:
        raise MqValueError('Specified arguments did not match any asset in the dataset' + str(kwargs))
    else:
        return assets[0].id


def get_fxo_asset(
    asset: Asset,
    expiry_tenor: str,
    strike: str,
    option_type: str = None,
    expiration_location: str = None,
    premium_payment_date: str = None,
) -> str:
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

    kwargs = dict(
        asset_class='FX',
        type='Option',
        asset_parameters_call_currency=call_ccy,
        asset_parameters_put_currency=put_ccy,
        asset_parameters_expiration_date=expiry_tenor,
        asset_parameters_option_type=option_type,
        asset_parameters_premium_payment_date=premium_date,
        asset_parameters_strike_price_relative=strike,
    )

    return _get_tdapi_fxo_assets(**kwargs)


def _flip_fx_smile_reference(strike_reference: VolReference) -> VolReference:
    """
    Flip call/put smile references when the FX cross must be queried in stored direction.

    Purpose:
        Keep smile wing semantics aligned when a requested cross is reversed before
        asset lookup.

    Args:
        strike_reference: Original smile strike reference for the requested point.

    Returns:
        The mirrored call/put reference for reversed crosses, or the input value
        unchanged for non-directional references.

    Raises:
        None.
    """
    # Reverse cross queries swap call and put wings, but leave ATM-like references unchanged.
    if strike_reference == VolReference.DELTA_CALL:
        return VolReference.DELTA_PUT
    if strike_reference == VolReference.DELTA_PUT:
        return VolReference.DELTA_CALL
    return strike_reference


def _get_fx_smile_strike_and_option_type(strike_reference: VolReference, relative_strike: Real) -> tuple[str, str]:
    """
    Convert a smile reference into the asset-service strike label and option type.

    Purpose:
        Translate user-facing smile coordinates into the exact FX option asset
        parameters needed for batched asset resolution.

    Args:
        strike_reference: Smile strike reference such as delta call, delta put,
            spot, or forward.
        relative_strike: Relative strike associated with the reference.

    Returns:
        A tuple of ``(strike_label, option_type)`` suitable for FX option asset lookup.

    Raises:
        MqValueError: If the strike reference cannot be mapped to a supported FX
            option asset query.
    """
    ref_string, relative_strike = _preprocess_implied_vol_strikes_fx(strike_reference, relative_strike)

    if ref_string == 'delta':
        # Delta smiles use DN for ATM, positive deltas as call wings, and negative deltas as put wings.
        if relative_strike == 0:
            return 'DN', OptionType.CALL.value
        if relative_strike > 0:
            return f'{relative_strike}D', OptionType.CALL.value
        return f'{-relative_strike}D', OptionType.PUT.value

    # Non-delta references map directly to the asset-service strike naming scheme.
    if ref_string == VolReference.SPOT.value:
        return 'Spot', OptionType.CALL.value

    if ref_string == VolReference.FORWARD.value:
        return 'ATMF', OptionType.CALL.value

    raise MqValueError('unknown strike_reference and relative_strike combination')


def _get_fx_vol_smile_asset_details(asset: Asset, tenor: str) -> list[dict]:
    """
    Resolve the five standard FX smile points into batched asset lookup metadata.

    Purpose:
        Precompute all inputs needed to fetch an FX vol smile through one asset-service
        request, while retaining enough metadata to fall back per point if needed.

    Args:
        asset: FX cross asset for which the smile is being requested.
        tenor: Option expiry tenor for the smile.

    Returns:
        A list of per-point dictionaries containing signed smile bucket, original
        request inputs, resolved asset query parameters, match keys, and resolved
        asset ids.

    Raises:
        MqValueError: If the FX cross does not expose a Bloomberg identifier and
            therefore cannot be normalized for asset lookup.
    """
    bbid = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)
    if bbid is None:
        raise MqValueError('Badly setup cross ' + asset.name)

    # Normalize to the stored cross direction once so the whole smile can be resolved consistently.
    cross = _cross_stored_direction_helper(bbid)
    is_reversed_cross = cross != bbid
    query_asset = SecurityMaster.get_asset(cross, AssetIdentifier.BLOOMBERG_ID) if is_reversed_cross else asset
    defaults = _get_fxo_defaults(cross)
    premium_date = defaults['premiumPaymentDate']

    specs = []
    for signed_strike, strike_reference, relative_strike in FX_VOL_SMILE_POINTS:
        # Build the exact asset-query parameters for each standard smile bucket.
        query_reference = _flip_fx_smile_reference(strike_reference) if is_reversed_cross else strike_reference
        strike, option_type = _get_fx_smile_strike_and_option_type(query_reference, relative_strike)
        if option_type == OptionType.PUT.value:
            call_currency = defaults['over']
            put_currency = defaults['under']
        else:
            call_currency = defaults['under']
            put_currency = defaults['over']

        specs.append(
            {
                'signed_strike': signed_strike,
                'input_strike_reference': strike_reference,
                'input_relative_strike': relative_strike,
                'strike': strike,
                'option_type': option_type,
                'call_currency': call_currency,
                'put_currency': put_currency,
                'match_key': (
                    call_currency,
                    put_currency,
                    tenor.lower(),
                    option_type,
                    premium_date,
                    strike,
                ),
            }
        )

    # Query the full smile asset set in one asset-service call instead of resolving
    # each smile wing independently.
    batch_kwargs = dict(
        asset_class='FX',
        type='Option',
        asset_parameters_call_currency=tuple(spec['call_currency'] for spec in specs),
        asset_parameters_put_currency=tuple(spec['put_currency'] for spec in specs),
        asset_parameters_expiration_date=tenor,
        asset_parameters_option_type=tuple(spec['option_type'] for spec in specs),
        asset_parameters_premium_payment_date=premium_date,
        asset_parameters_strike_price_relative=tuple(spec['strike'] for spec in specs),
    )
    assets = GsAssetApi.get_many_assets(**batch_kwargs)
    assets_by_key = {}
    for candidate in assets:
        # Index batched asset-service results by the same composite key used in the request specs.
        params = getattr(candidate, 'parameters', {}) or {}
        candidate_key = (
            params.get('callCurrency'),
            params.get('putCurrency'),
            str(params.get('expirationDate', '')).lower(),
            params.get('optionType'),
            params.get('premiumPaymentDate'),
            params.get('strikePriceRelative'),
        )
        assets_by_key.setdefault(candidate_key, candidate.id)

    # Batch-resolve the five smile option assets so one smile request does not
    # fan out into five separate asset-service lookups before market data.
    for spec in specs:
        spec['asset_id'] = assets_by_key.get(spec['match_key'])
        if spec['asset_id'] is None:
            # Fall back only when a specific smile point is missing from the batched asset response.
            spec['asset_id'] = get_fxo_asset(
                query_asset,
                tenor,
                spec['strike'],
                spec['option_type'],
                premium_payment_date=premium_date,
            )

    return specs


def _get_fx_vol_smile_market_data(
    asset_ids: list[str],
    location: PricingLocation,
    source: str = None,
    real_time: bool = False,
) -> pd.DataFrame:
    """
    Fetch implied-volatility market data for all smile asset ids in one query.

    Purpose:
        Collapse the common five-point smile retrieval path into a single remote
        market-data request.

    Args:
        asset_ids: Resolved FX option asset ids for the smile points.
        location: Pricing location to apply to the market-data query.
        source: Optional market-data source override.
        real_time: Whether to request realtime data.

    Returns:
        A market-data dataframe containing rows for one or more smile asset ids.

    Raises:
        Propagates any exception raised while building or executing the market-data
        query.
    """
    # Pull all smile points in one market-data query so a five-point smile stays
    # a single remote request on the happy path.
    where = dict(pricingLocation=location.value)
    q = GsDataApi.build_market_data_query(
        asset_ids,
        QueryType.IMPLIED_VOLATILITY,
        where=where,
        source=source,
        real_time=real_time,
    )
    _logger.debug('q %s', q)
    return _market_data_timed(q)


def _get_fx_vol_smile_fallback_data(
    asset: Asset,
    tenor: str,
    fallback_specs: list[dict],
    pricing_location: PricingLocation,
    source: str = None,
    real_time: bool = False,
) -> list[pd.Series]:
    """
    Fetch unresolved FX smile points through the single-point measure path.

    Purpose:
        Preserve resilience when the batched smile path is unavailable, while
        avoiding unnecessary serial latency across the standard five smile wings.

    Args:
        asset: FX cross asset for which the smile is being requested.
        tenor: Option expiry tenor for the smile.
        fallback_specs: Smile-point specs that still need single-point retrieval.
        pricing_location: Pricing location for the fallback measure calls.
        source: Optional market-data source override.
        real_time: Whether to request realtime data.

    Returns:
        One series per requested fallback spec, in the same order.

    Raises:
        Propagates any exception raised by the underlying single-point measure
            path when both parallel and sequential fallback execution fail.
    """
    if not fallback_specs:
        return []

    if len(fallback_specs) == 1:
        spec = fallback_specs[0]
        return [
            implied_volatility_fxvol(
                asset,
                tenor,
                spec['input_strike_reference'],
                spec['input_relative_strike'],
                location=pricing_location,
                source=source,
                real_time=real_time,
            )
        ]

    # For multiple missing smile points, fan out the existing single-point measure calls in parallel.
    tasks = [
        partial(
            implied_volatility_fxvol,
            asset,
            tenor,
            spec['input_strike_reference'],
            spec['input_relative_strike'],
            location=pricing_location,
            source=source,
            real_time=real_time,
        )
        for spec in fallback_specs
    ]

    try:
        return ThreadPoolManager.run_async(tasks)
    except Exception as error:
        _logger.debug('parallel fx_vol_smile fallback failed: %s', error)
        return [task() for task in tasks]


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


def _get_fx_vol_swap_data(
    asset: Asset,
    expiry_tenor: str,
    strike_type: str = None,
    location: PricingLocation = None,
    source: str = None,
    real_time: bool = False,
    query_type: QueryType = QueryType.STRIKE_VOL,
) -> pd.DataFrame:
    if real_time:
        raise NotImplementedError('realtime FX Vol swap data not implemented')

    cross = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)

    if cross not in FX_VOL_SWAP_DEFAULTS:
        raise NotImplementedError('Data not available for {} FX Vol Swaps'.format(cross))

    kwargs = dict(
        asset_class='FX',
        type='VolatilitySwap',
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

    q = GsDataApi.build_market_data_query([fxv_mqid], query_type, where=where, source=source, real_time=real_time)
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return df


def _get_fxfwd_data(
    asset: Asset,
    settlement_date: str,
    location: str = None,
    source: str = None,
    real_time: bool = False,
    query_type: QueryType = QueryType.FWD_POINTS,
) -> pd.DataFrame:
    if real_time:
        mqid = asset.get_identifier(AssetIdentifier.MARQUEE_ID)
        q = GsDataApi.build_market_data_query(
            [mqid], QueryType.FORWARD_POINT, source=source, real_time=real_time, where={'tenor': settlement_date}
        )
        _logger.debug('q %s', q)
        df = _market_data_timed(q)
        return df

    cross = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)

    if not (tm_rates._is_valid_relative_date_tenor(settlement_date)):
        raise MqValueError('invalid settlements date ' + settlement_date)

    kwargs = dict(
        asset_class='FX',
        type='Forward',
        asset_parameters_pair=cross,
        asset_parameters_settlement_date=settlement_date,
        name_prefix='FX Forward',
    )

    mqid = _get_tdapi_fxo_assets(**kwargs)

    if location is None:
        pricing_location = PricingLocation.NYC
    else:
        pricing_location = PricingLocation(location)

    where = dict(pricingLocation=pricing_location.value)

    q = GsDataApi.build_market_data_query([mqid], query_type, where=where, source=source, real_time=real_time)
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return df


def _get_fxo_data(
    asset: Asset,
    expiry_tenor: str,
    strike: str,
    option_type: str = None,
    expiration_location: str = None,
    location: PricingLocation = None,
    premium_payment_date: str = None,
    source: str = None,
    real_time: bool = False,
    query_type: QueryType = QueryType.IMPLIED_VOLATILITY,
) -> pd.DataFrame:
    if real_time:
        raise NotImplementedError('realtime FX Option data not implemented')

    asset_mqid = get_fxo_asset(
        asset=asset,
        expiry_tenor=expiry_tenor,
        strike=strike,
        option_type=option_type,
        expiration_location=expiration_location,
        premium_payment_date=premium_payment_date,
    )

    if location is None:
        pricing_location = PricingLocation.NYC
    else:
        pricing_location = PricingLocation(location)

    where = dict(pricingLocation=pricing_location.value)

    # _logger.debug(f'where asset= {rate_mqid}, swap_tenor={swap_tenor}, index={defaults["index_type"]}, '
    #              f'forward_tenor={forward_tenor}, pricing_location={pricing_location.value}, '
    #              f'clearing_house={clearing_house.value}, notional_currency={currency.name}')
    q = GsDataApi.build_market_data_query([asset_mqid], query_type, where=where, source=source, real_time=real_time)
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return df


def implied_volatility_new(
    asset: Asset,
    expiry_tenor: str,
    strike: str,
    option_type: str = None,
    expiration_location: str = None,
    location: PricingLocation = None,
    premium_payment_date: str = None,
    *,
    source: str = None,
    real_time: bool = False,
) -> pd.Series:
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

    df = _get_fxo_data(
        asset=asset,
        expiry_tenor=expiry_tenor,
        strike=strike,
        option_type=option_type,
        expiration_location=expiration_location,
        location=location,
        premium_payment_date=premium_payment_date,
        source=source,
        real_time=real_time,
        query_type=QueryType.IMPLIED_VOLATILITY,
    )

    series = ExtendedSeries(dtype=float) if df.empty else ExtendedSeries(df['impliedVolatility'])
    series.dataset_ids = getattr(df, 'dataset_ids', ())
    return series


"""
New Implementation
"""


@plot_measure(
    (AssetClass.FX,),
    (AssetType.Cross,),
    [MeasureDependency(id_provider=cross_stored_direction_for_fx_vol, query_type=QueryType.IMPLIED_VOLATILITY)],
    display_name="implied_volatility",
)
def implied_volatility_fxvol(
    asset: Asset,
    tenor: str,
    strike_reference: VolReference = None,
    relative_strike: Real = None,
    location: Optional[PricingLocation] = None,
    legacy_implementation: bool = False,
    *,
    source: str = None,
    real_time: bool = False,
) -> pd.Series:
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
    s = implied_volatility_new(
        cross_asset, tenor, strike, option_type, location=location, source=source, real_time=real_time
    )
    return s


@plot_measure(
    (AssetClass.FX,),
    (AssetType.Cross,),
    [MeasureDependency(id_provider=cross_stored_direction_for_fx_vol, query_type=QueryType.IMPLIED_VOLATILITY)],
)
def fx_vol_smile(
    asset: Asset,
    tenor: str,
    pricing_date: Optional[GENERIC_DATE] = None,
    location: Optional[PricingLocation] = None,
    *,
    source: str = None,
    real_time: bool = False,
) -> pd.Series:
    """
    FX volatility smile built from standard delta wing points.

    :param asset: cross currency asset object loaded from security master
                  like EURUSD, JPYUSD  etc
    :param tenor: relative date representation of expiration date e.g. 1m
    :param pricing_date: YYYY-MM-DD or relative days before today e.g. 1d, 1m, 1y
    :param location: location of the data snapshot Example - "HKG", "LDN", "NYC"
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: timeseries containing the FX smile for the requested tenor, indexed by
        ATM-relative delta wing bucket in basis points ``[-25, -10, 0, 10, 25]``.
        Negative values represent put wings, ``0`` is ATM, and positive values
        represent call wings.

    **Usage**

    Retrieve the standard five-point FX volatility smile for a cross and tenor.
    The function reuses the existing FX implied-volatility measure at the
    conventional wing points 25-delta put, 10-delta put, ATM, 10-delta call,
    and 25-delta call, then returns the latest value for the requested pricing
    date context.

    **Examples**

    Get the 1-month EURUSD smile using the default NYC pricing location:

    >>> smile = EURUSD.fx_vol_smile("1m")

    Get a historical smile snapshot for a London close:

    >>> smile_2 = EURUSD.fx_vol_smile("3m", pricing_date=2024-06-03, location="LDN")

    >>> smile = USD.fx_vol_smile("1m")  THIS WILL FAIL

    **Returned Data**

    The returned series index is the signed smile bucket and the value is the
    implied volatility for that point on the smile:

    =========   ================================================================
    Index       Meaning
    =========   ================================================================
    -25         25-delta put wing
    -10         10-delta put wing
    0           ATM / delta-neutral point
    10          10-delta call wing
    25          25-delta call wing
    =========   ================================================================

    Example return shape:

    >>> pd.Series(
    ...     [-24.8, -9.8, 0.2, 10.2, 25.2],
    ...     index=[-25, -10, 0, 10, 25],
    ...     name='vol_smile'
    ... )

    In production the values are implied volatilities, while the index tells you
    where each point sits on the smile relative to ATM.
    Flow
      +-- build 5 smile specs
      +-- 1 batched asset lookup for all 5 points
      +-- 1 batched market data call for all 5 points
      +-- split shared response by assetId
      +-- assemble smile
      +-- fallback per-point only if some points are missing

    1 asset lookup + 1 market data call on the happy path

    """
    if real_time:
        raise NotImplementedError('realtime fx_vol_smile not implemented')

    pricing_location = PricingLocation.NYC if location is None else PricingLocation(location)
    if pricing_date is None:
        # Keep the default path cheap: fetch a recent window and then select the
        # latest available smile point from the shared batch response below.
        end = pd.Timestamp.today().normalize() - pd.Timedelta(days=1)
        start = end - pd.Timedelta(days=7)
    else:
        start, end = _range_from_pricing_date(pricing_location, pricing_date)

    smile_points = []
    dataset_ids = ()
    smile_specs = None
    with DataContext(start, end):
        try:
            # Main happy path:
            # 1. normalize the tenor once,
            # 2. reuse cached smile asset specs when available,
            # 3. otherwise resolve the five standard smile assets in one go,
            # 4. fetch all smile market data in one batched query.
            normalized_tenor = _tenor_month_to_year(tenor)
            cache_key = (asset.get_identifier(AssetIdentifier.BLOOMBERG_ID), normalized_tenor)
            cache = getattr(fx_vol_smile, '_asset_details_cache', {})
            smile_specs = cache.get(cache_key)
            if smile_specs is None:
                smile_specs = _get_fx_vol_smile_asset_details(asset, normalized_tenor)
                if len(cache) >= 32:
                    # Keep the cache bounded so repeated smile requests do not grow process memory indefinitely.
                    cache.pop(next(iter(cache)))
                cache[cache_key] = smile_specs
                fx_vol_smile._asset_details_cache = cache
            batch_df = _get_fx_vol_smile_market_data(
                [spec['asset_id'] for spec in smile_specs],
                pricing_location,
                source=source,
                real_time=real_time,
            )
        except Exception as error:
            # If the batched path fails at any point, fall back to the existing per-point measure path below.
            _logger.debug('batched fx_vol_smile lookup failed: %s', error)
            batch_df = pd.DataFrame()
        else:
            dataset_ids = getattr(batch_df, 'dataset_ids', ())
            if not batch_df.empty and 'assetId' in batch_df.columns:
                # The batched query returns rows for all smile option assets together.
                # This loop slices that shared response back into one latest vol per
                # requested smile bucket, avoiding five separate market-data calls.
                for spec in smile_specs:
                    asset_slice = batch_df[batch_df['assetId'] == spec['asset_id']]
                    if asset_slice.empty or 'impliedVolatility' not in asset_slice.columns:
                        continue
                    # Use the most recent pricing row for each smile asset in the requested context.
                    latest = asset_slice.index.max()
                    _logger.info('selected pricing date %s', latest)
                    latest_slice = asset_slice[asset_slice.index == latest]
                    # Each smile bucket contributes one latest value keyed by its signed wing location.
                    smile_points.append(
                        (
                            spec['signed_strike'],
                            latest_slice['impliedVolatility'].iloc[-1],
                        )
                    )

        # Only unresolved smile points fall back to the older sequential path,
        # which keeps the common fully-batched case fast without dropping resiliency.
        resolved_signed_strikes = {signed_strike for signed_strike, _ in smile_points}
        fallback_specs = smile_specs or [
            {
                'signed_strike': signed_strike,
                'input_strike_reference': strike_reference,
                'input_relative_strike': relative_strike,
            }
            for signed_strike, strike_reference, relative_strike in FX_VOL_SMILE_POINTS
        ]

        # Only points missing from the batched response need the slower single-point fallback path.
        unresolved_specs = [spec for spec in fallback_specs if spec['signed_strike'] not in resolved_signed_strikes]
        fallback_series = _get_fx_vol_smile_fallback_data(
            asset,
            tenor,
            unresolved_specs,
            pricing_location,
            source=source,
            real_time=real_time,
        )

        for spec, series in zip(unresolved_specs, fallback_series):
            if not dataset_ids:
                dataset_ids = getattr(series, 'dataset_ids', ())
            if not series.empty:
                latest = series.index.max()
                _logger.info('selected pricing date %s', latest)
                # Fallback results are merged back into the same signed-strike smile structure.
                smile_points.append((spec['signed_strike'], series.sort_index().iloc[-1]))

    if smile_points:
        # Final output is a float-index smile ordered from put wing to call wing.
        smile_points = sorted(smile_points, key=lambda point: point[0])
        series = ExtendedSeries(
            [volatility for _, volatility in smile_points],
            index=[relative_strike for relative_strike, _ in smile_points],
        )
    else:
        series = ExtendedSeries(dtype=float)

    series.dataset_ids = dataset_ids
    series.name = 'vol_smile'
    series.result_type = 'term_structure'
    return series


@plot_measure(
    (AssetClass.FX,),
    (AssetType.Cross,),
    [MeasureDependency(id_provider=_currencypair_to_tdapi_fxfwd_asset, query_type=QueryType.FWD_POINTS)],
    display_name="forward_point",
)
def fwd_points(
    asset: Asset, settlement_date: str, location: str = None, *, source: str = None, real_time: bool = False
) -> pd.Series:
    """
    GS End-of-day FX forward points for G3, G10, and EM crosses.

    :param asset: asset object loaded from security master
    :param settlement_date: relative date representation of expiration date e.g. 1m
    :param location: Example - "TKO", "LDN", "NYC"
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: fwd points
    """
    df = _get_fxfwd_data(
        asset=asset,
        settlement_date=settlement_date,
        location=location,
        source=source,
        real_time=real_time,
        query_type=QueryType.FWD_POINTS,
    )
    if real_time:
        series = ExtendedSeries(dtype=float) if df.empty else ExtendedSeries(df['forwardPoint'])
    else:
        series = ExtendedSeries(dtype=float) if df.empty else ExtendedSeries(df['fwdPoints'])
    series.dataset_ids = getattr(df, 'dataset_ids', ())
    return series


@plot_measure(
    (AssetClass.FX,),
    (AssetType.Cross,),
    [MeasureDependency(id_provider=_currencypair_to_tdapi_fx_vol_swap_asset, query_type=QueryType.STRIKE_VOL)],
)
def vol_swap_strike(
    asset: Asset,
    expiry_tenor: str,
    strike_type: str = None,
    location: PricingLocation = None,
    *,
    source: str = None,
    real_time: bool = False,
) -> pd.Series:
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
    df = _get_fx_vol_swap_data(
        asset=asset,
        expiry_tenor=expiry_tenor,
        strike_type=strike_type,
        location=location,
        source=source,
        real_time=real_time,
        query_type=QueryType.STRIKE_VOL,
    )

    series = ExtendedSeries(dtype=float) if df.empty else ExtendedSeries(df['strikeVol'])
    series.dataset_ids = getattr(df, 'dataset_ids', ())
    return series


@plot_measure((AssetClass.FX,), None, [QueryType.FORWARD_POINT])
def spot_carry(
    asset: Asset,
    tenor: str,
    annualized: FXSpotCarry = FXSpotCarry.DAILY,
    pricing_location: Optional[PricingLocation] = None,
    *,
    source: str = None,
    real_time: bool = False,
) -> pd.Series:
    """
    Calculates carry using forward term structure i.e forwardpoints/spot with option to return it in annualized terms.

    :param asset: asset object loaded from security master
    :param tenor: relative date representation of expiration date e.g. 1m
    :param annualized: whether to annualize carry, one of annualized or daily
    :param pricing_location: EOD location if multiple available example - "HKG", "LDN", "NYC"
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: FX spot carry curve
    """

    if real_time:
        raise NotImplementedError('realtime spot_carry not implemented')

    if tenor not in [
        '1m',
        '2m',
        '3m',
        '4m',
        '5m',
        '6m',
        '7m',
        '8m',
        '9m',
        '10m',
        '11m',
        '1y',
        '15m',
        '18m',
        '21m',
        '2y',
    ]:
        raise MqValueError('tenor not included in dataset')
    cross = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)
    kwargs = dict(
        asset_class='FX',
        type='Forward',
        asset_parameters_pair=cross,
        asset_parameters_settlement_date=tenor,
        name_prefix='FX Forward',
    )
    mqid = _get_tdapi_fxo_assets(**kwargs)
    q = GsDataApi.build_market_data_query([mqid], QueryType.FWD_POINTS, source=source, real_time=real_time)
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    if df.empty:
        return pd.Series(dtype=float)
    dataset_ids = getattr(df, 'dataset_ids', ())
    ds = Dataset(dataset_ids[0])
    location = pricing_location if pricing_location else PricingLocation.NYC
    start, end = DataContext.current.start_date, DataContext.current.end_date
    mq_df = ds.get_data(asset_id=mqid, start=start, end=end, pricingLocation=location.value)
    if mq_df.empty:
        return pd.Series(dtype=float)
    mq_df = mq_df.reset_index()
    mq_df['ann_factor'] = mq_df.apply(lambda x: 360 / (x.settlementDate - x.date).days, axis=1)
    mq_df = mq_df.set_index('date')

    if annualized == FXSpotCarry.ANNUALIZED:
        mq_df['carry'] = -1 * mq_df['ann_factor'] * mq_df['fwdPoints'] / mq_df['spot']
    else:
        mq_df['carry'] = -1 * mq_df['fwdPoints'] / mq_df['spot']
    series = ExtendedSeries(mq_df['carry'], name='spotCarry')
    series.dataset_ids = dataset_ids
    return series
