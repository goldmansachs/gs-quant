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
from typing import Union

import pandas as pd
from pandas import Series

from gs_quant.api.gs.assets import GsAssetApi
from gs_quant.api.gs.data import QueryType, GsDataApi
from gs_quant.errors import MqValueError
from gs_quant.markets.securities import AssetIdentifier, Asset
from gs_quant.target.common import AssetClass, AssetType, PricingLocation
from gs_quant.timeseries import ASSET_SPEC, plot_measure, MeasureDependency
from gs_quant.timeseries import ExtendedSeries, measures_rates as tm_rates
from gs_quant.timeseries.measures import _asset_from_spec, _market_data_timed

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
    "AUDJPY": {"under": "AUD", "over": "JPY",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "AUDUSD": {"under": "AUD", "over": "USD",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "CADJPY": {"under": "CAD", "over": "JPY",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "CHFJPY": {"under": "CHF", "over": "JPY",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURCAD": {"under": "EUR", "over": "CAD",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURCHF": {"under": "EUR", "over": "CHF",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURGBP": {"under": "EUR", "over": "GBP",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURJPY": {"under": "EUR", "over": "JPY",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURNOK": {"under": "EUR", "over": "NOK",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURNZD": {"under": "EUR", "over": "NZD",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURSEK": {"under": "EUR", "over": "SEK",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "EURUSD": {"under": "EUR", "over": "USD",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "GBPJPY": {"under": "GBP", "over": "JPY",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "GBPUSD": {"under": "GBP", "over": "USD",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "NOKJPY": {"under": "NOK", "over": "JPY",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "NZDJPY": {"under": "NZD", "over": "JPY",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "NZDUSD": {"under": "NZD", "over": "USD",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "SEKJPY": {"under": "SEK", "over": "JPY",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDCAD": {"under": "USD", "over": "CAD",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDCHF": {"under": "USD", "over": "CHF",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDJPY": {"under": "USD", "over": "JPY",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDNOK": {"under": "USD", "over": "NOK",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
    "USDSEK": {"under": "USD", "over": "SEK",
               "expirationTime": "NYC", "premiumPaymentDate": "Fwd Settle"},
}
fx_defaults_provider = TdapiFXDefaultsProvider(FX_DEFAULTS)

CURRENCY_TO_DUMMY_FFO_BBID = {
    'AUDJPY': 'MAQ1XXCYK116RNES',
    'AUDUSD': 'MAJE79T8P0FVKK7F',
    'CADJPY': 'MA1ATZM1Y7GYKNTN',
    'CHFJPY': 'MATJG02X92Q3VMB5',
    'EURCAD': 'MAMRE5ESVVT5MPKB',
    'EURCHF': 'MAFWK4AP9292EPD6',
    'EURGBP': 'MA2JVMPV9FYJ9VPZ',
    'EURJPY': 'MA7JKM8W2J9NWQKZ',
    'EURNOK': 'MAQHS3FXN5PPD5FE',
    'EURNZD': 'MAX9CDVPTY2HXNHS',
    'EURSEK': 'MA1TVDWGK280VFXN',
    'EURUSD': 'MASN9J5N0H418Y6A',
    'GBPJPY': 'MA14MBDMA17AEFAM',
    'GBPUSD': 'MA7F5P92330NGKAR',
    'NOKJPY': 'MAED8YP9DPS5ZGDH',
    'NZDJPY': 'MAQ1MC9VKKTZ1DAB',
    'NZDUSD': 'MAW1MYXCXMJ3V9MG',
    'SEKJPY': 'MA1JB3FN5HJBVY44',
    'USDCAD': 'MA5S1V7TWAH8S4XX',
    'USDCHF': 'MAVCW4WZKSVNX7DS',
    'USDJPY': 'MAW3BZY6KFQ6TP95',
    'USDNOK': 'MAXFKJET0RZ9Q66N',
    'USDSEK': 'MAAS3CYC8NFPF4KQ'
}


def _currencypair_to_tdapi_fxo_asset(asset_spec: ASSET_SPEC) -> str:
    asset = _asset_from_spec(asset_spec)
    bbid = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)
    # for each currency, get a dummy asset for checking availability
    result = CURRENCY_TO_DUMMY_FFO_BBID.get(bbid, asset.get_marquee_id())
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


def _get_fxo_defaults(cross: str) -> dict:
    return fx_defaults_provider.get_defaults_for_cross(cross)


def _get_fx_csa_terms() -> dict:
    return dict(csaTerms='USD-1')


def _get_fxo_data(asset: Asset, expiry_tenor: str, strike: str, option_type: str = None,
                  expiration_location: str = None,
                  location: PricingLocation = None, premium_payment_date: str = None,
                  source: str = None, real_time: bool = False,
                  query_type: QueryType = QueryType.IMPLIED_VOLATILITY) \
        -> pd.DataFrame:
    if real_time:
        raise NotImplementedError('realtime inflation swap data not implemented')
    cross = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)

    if cross not in FX_DEFAULTS.keys():
        raise NotImplementedError('Data not available for {} FX Vanilla options'.format(cross))

    defaults = _get_fxo_defaults(cross)

    if not (tm_rates._is_valid_relative_date_tenor(expiry_tenor)):
        raise MqValueError('invalid expiry ' + expiry_tenor)

    if expiration_location is None:
        # expirationtime = defaults["expirationTime"]
        _ = defaults["expirationTime"]
    else:
        # expirationtime = expiration_location
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
                  # asset_parameters_expiration_time=expirationtime,
                  asset_parameters_option_type=option_type,
                  asset_parameters_premium_payment_date=premium_date,
                  asset_parameters_strike_price_relative=strike,
                  )

    rate_mqid = _get_tdapi_fxo_assets(**kwargs)

    if location is None:
        pricing_location = PricingLocation.NYC
    else:
        pricing_location = PricingLocation(location)

    where = dict(pricingLocation=pricing_location.value)

    # _logger.debug(f'where asset= {rate_mqid}, swap_tenor={swap_tenor}, index={defaults["index_type"]}, '
    #              f'forward_tenor={forward_tenor}, pricing_location={pricing_location.value}, '
    #              f'clearing_house={clearing_house.value}, notional_currency={currency.name}')
    q = GsDataApi.build_market_data_query([rate_mqid], query_type, where=where, source=source,
                                          real_time=real_time)
    _logger.debug('q %s', q)
    df = _market_data_timed(q)
    return df


@plot_measure((AssetClass.FX,), (AssetType.Cross,),
              [MeasureDependency(id_provider=_currencypair_to_tdapi_fxo_asset,
                                 query_type=QueryType.IMPLIED_VOLATILITY)])
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

    series = ExtendedSeries() if df.empty else ExtendedSeries(df['impliedVolatility'])
    series.dataset_ids = getattr(df, 'dataset_ids', ())
    return series
