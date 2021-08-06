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

import datetime as dt

import pandas as pd
import pytest
from pandas.testing import assert_series_equal
from testfixtures import Replacer
from testfixtures.mock import Mock

import gs_quant.timeseries.measures as tm_rates
import gs_quant.timeseries.measures_fx_vol as tm_fxo
import gs_quant.timeseries.measures_xccy as tm
from gs_quant.api.gs.assets import GsAsset
from gs_quant.api.gs.data import GsDataApi, MarketDataResponseFrame
from gs_quant.errors import MqError, MqValueError
from gs_quant.session import GsSession, Environment
from gs_quant.target.common import PricingLocation
from gs_quant.test.timeseries.utils import mock_request
from gs_quant.timeseries import Currency, Cross, Bond, CurrencyEnum, SecurityMaster
from gs_quant.timeseries.measures_fx_vol import _currencypair_to_tdapi_fxo_asset

_index = [pd.Timestamp('2021-03-30')]
_test_datasets = ('TEST_DATASET',)


def test_currencypair_to_tdapi_fxo_asset(mocker):
    replace = Replacer()
    mocker.patch.object(GsSession.__class__, 'current',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_get', side_effect=mock_request)
    mocker.patch.object(SecurityMaster, 'get_asset', side_effect=mock_request)
    bbid_mock = replace('gs_quant.timeseries.measures_fx_vol.Asset.get_identifier', Mock())

    with tm_rates.PricingContext(dt.date.today()):
        cur = [
            {
                "currency_assetId": "MAK1FHKH5P5GJSHH",
                "currency": "USDJPY",
                "id": "MAW3BZY6KFQ6TP95"
            },
            {
                "currency_assetId": "MA66CZBQJST05XKG",
                "currency": "GBPUSD",
                "id": "MA7F5P92330NGKAR"
            },
            {
                "currency_assetId": "MAJNQPFGN1EBDHAE",
                "currency": "EURUSD",
                "id": "MASN9J5N0H418Y6A"
            },
        ]
        for c in cur:
            print(c)
            asset = Currency(c.get("currency_assetId"), c.get("currency"))
            bbid_mock.return_value = c.get("currency")
            mqid = _currencypair_to_tdapi_fxo_asset(asset)
            assert mqid == c.get("id")

        bbid_mock.return_value = None
        assert _currencypair_to_tdapi_fxo_asset(asset) == c.get("currency_assetId")
        replace.restore()


def test_get_fxo_defaults():
    result_dict = dict(under="AUD", over="JPY",
                       expirationTime="NYC", premiumPaymentDate="Fwd Settle")
    defaults = tm_fxo._get_fxo_defaults("AUDJPY")
    assert result_dict == defaults

    result_dict = dict(under="CAD", over="JPY",
                       expirationTime="NYC", premiumPaymentDate="Fwd Settle")
    defaults = tm_fxo._get_fxo_defaults("CADJPY")
    assert result_dict == defaults

    result_dict = dict(under="EUR", over="NOK",
                       expirationTime="NYC", premiumPaymentDate="Fwd Settle")
    defaults = tm_fxo._get_fxo_defaults("EURNOK")
    assert result_dict == defaults

    result_dict = dict(under="GBP", over="USD",
                       expirationTime="NYC", premiumPaymentDate="Fwd Settle")
    defaults = tm_fxo._get_fxo_defaults("GBPUSD")
    assert result_dict == defaults

    result_dict = dict(under="EUR", over="NZD",
                       expirationTime="NYC", premiumPaymentDate="Fwd Settle")
    defaults = tm_fxo._get_fxo_defaults("EURNZD")
    assert result_dict == defaults


def test_get_fxo_csa_terms():
    assert dict(csaTerms='USD-1') == tm_fxo._get_fx_csa_terms()


def test_check_valid_indices():
    valid_indices = ['LIBOR']
    for index in valid_indices:
        assert tm.CrossCurrencyRateOptionType[index] == tm._check_crosscurrency_rateoption_type(CurrencyEnum.GBP, index)

    invalid_indices = ['LIBORED', 'TestRateOption']
    for index in invalid_indices:
        with pytest.raises(MqError):
            tm._check_crosscurrency_rateoption_type(CurrencyEnum.GBP, index)


def test_get_tdapi_fxo_assets(mocker):
    mock_asset_1 = GsAsset(asset_class='FX', id='MAW8SAXPSKYA94E2', type_='Option', name='Test_asset')
    mock_asset_2 = GsAsset(asset_class='FX', id='MATDD783JM1C2GGD', type_='Option', name='Test_asset')

    replace = Replacer()
    assets = replace('gs_quant.timeseries.measures.GsAssetApi.get_many_assets', Mock())
    assets.return_value = [mock_asset_1]
    assert 'MAW8SAXPSKYA94E2' == tm_fxo._get_tdapi_fxo_assets()
    replace.restore()

    assets = replace('gs_quant.timeseries.measures.GsAssetApi.get_many_assets', Mock())
    assets.return_value = [mock_asset_1, mock_asset_2]
    kwargs = dict(asset_parameters_expiration_date='5y', asset_parameters_call_currency='USD',
                  asset_parameters_put_currency='EUR')
    with pytest.raises(MqValueError):
        tm_fxo._get_tdapi_fxo_assets(**kwargs)
    replace.restore()

    assets = replace('gs_quant.timeseries.measures.GsAssetApi.get_many_assets', Mock())
    assets.return_value = []
    kwargs = dict(asset_parameters_expiration_date='5y', asset_parameters_call_currency='USD',
                  asset_parameters_put_currency='EUR')
    with pytest.raises(MqValueError):
        tm_fxo._get_tdapi_fxo_assets(**kwargs)
    replace.restore()

    assets = replace('gs_quant.timeseries.measures.GsAssetApi.get_many_assets', Mock())
    assets.return_value = [mock_asset_1, mock_asset_2]
    kwargs = dict()
    assert ['MAW8SAXPSKYA94E2', 'MATDD783JM1C2GGD'] == tm._get_tdapi_crosscurrency_rates_assets(**kwargs)
    replace.restore()

    #   test case will test matching sofr maturity with libor leg and flipping legs to get right asset
    kwargs = dict(Asset_class='FX',
                  type='Option',
                  asset_parameters_call_currency='USD',
                  asset_parameters_put_currency='EUR',
                  asset_parameters_expiration_date='1m',
                  asset_parameters_expiration_time='NYC',
                  asset_parameters_option_type='Put',
                  asset_parameters_premium_payment_date='Fwd Settle',
                  asset_parameters_strike_price_relative='10d',
                  pricing_location='NYC')

    assets = replace('gs_quant.timeseries.measures.GsAssetApi.get_many_assets', Mock())
    assets.return_value = [mock_asset_1]
    assert 'MAW8SAXPSKYA94E2' == tm_fxo._get_tdapi_fxo_assets(**kwargs)
    replace.restore()


def mock_curr(_cls, _q):
    d = {
        'impliedVolatility': [1, 2, 3],
    }
    df = MarketDataResponseFrame(data=d, index=_index * 3)
    df.dataset_ids = _test_datasets
    return df


def test_fx_vol_measure(mocker):
    replace = Replacer()
    args = dict(expiry_tenor='1m', strike='ATMF', option_type='Put',
                expiration_location=None,
                location=None, premium_payment_date=None,)

    mock_gbp = Cross('MA26QSMPX9990G66', 'GBPUSD')
    args['asset'] = mock_gbp
    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'GBPUSD'

    args['expiry_tenor'] = '1yr'
    with pytest.raises(MqValueError):
        tm_fxo.implied_volatility_new(**args)
    args['expiry_tenor'] = '1m'

    args['real_time'] = True
    with pytest.raises(NotImplementedError):
        tm_fxo.implied_volatility_new(**args)
    args['real_time'] = False

    args['asset'] = Cross('MA666', 'USDAED')
    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'AEDUSD'
    with pytest.raises(NotImplementedError):
        tm_fxo.implied_volatility_new(**args)
    args['asset'] = mock_gbp

    args['asset'] = Bond('MA667', 'TEST')
    with pytest.raises(NotImplementedError):
        tm_fxo.implied_volatility_new(**args)
    args['asset'] = mock_gbp

    args['asset'] = Cross('MA667', 'GBPUSD')
    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'GBPUSD'
    identifiers = replace('gs_quant.timeseries.measures_fx_vol._get_tdapi_fxo_assets', Mock())
    identifiers.return_value = {'MA7F5P92330NGKAR'}
    mocker.patch.object(GsDataApi, 'get_market_data', return_value=mock_curr(None, None))
    actual = tm_fxo.implied_volatility_new(**args)
    expected = tm.ExtendedSeries([1, 2, 3], index=_index * 3, name='impliedVolatility')
    expected.dataset_ids = _test_datasets
    assert_series_equal(expected, actual)
    assert actual.dataset_ids == _test_datasets

    args['asset'] = Cross('MA667', 'USDCAD')
    args['location'] = PricingLocation.LDN
    args['premium_payment_date'] = 'Fwd Settle'
    args['expiration_location'] = 'NYC'
    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'USDCAD'
    identifiers = replace('gs_quant.timeseries.measures_fx_vol._get_tdapi_fxo_assets', Mock())
    identifiers.return_value = {'MA7F5P92330NGKAR'}
    mocker.patch.object(GsDataApi, 'get_market_data', return_value=mock_curr(None, None))
    actual = tm_fxo.implied_volatility_new(**args)
    expected = tm.ExtendedSeries([1, 2, 3], index=_index * 3, name='impliedVolatility')
    expected.dataset_ids = _test_datasets
    assert_series_equal(expected, actual)
    assert actual.dataset_ids == _test_datasets

    args['option_type'] = 'Call'
    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'GBPUSD'
    identifiers = replace('gs_quant.timeseries.measures_fx_vol._get_tdapi_fxo_assets', Mock())
    identifiers.return_value = {'MA7F5P92330NGKAR'}
    mocker.patch.object(GsDataApi, 'get_market_data', return_value=mock_curr(None, None))
    actual = tm_fxo.implied_volatility_new(**args)
    expected = tm.ExtendedSeries([1, 2, 3], index=_index * 3, name='impliedVolatility')
    expected.dataset_ids = _test_datasets
    assert_series_equal(expected, actual)
    assert actual.dataset_ids == _test_datasets

    replace.restore()


if __name__ == '__main__':
    pytest.main(args=["test_measures_xccy.py"])
