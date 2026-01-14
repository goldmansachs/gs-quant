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

import gs_quant.timeseries
import gs_quant.timeseries.measures as tm_rates
import gs_quant.timeseries.measures_fx_vol as tm_fxo
import gs_quant.timeseries.measures_xccy as tm_xccy
from gs_quant.api.gs.assets import GsAsset
from gs_quant.api.gs.data import GsDataApi, MarketDataResponseFrame, QueryType
from gs_quant.common import PricingLocation
from gs_quant.data import DataContext
from gs_quant.errors import MqError, MqValueError
from gs_quant.markets import PricingContext
from gs_quant.markets.securities import Bond, Cross, Currency
from gs_quant.session import GsSession, Environment
from gs_quant.test.timeseries.utils import mock_request
from gs_quant.timeseries import Currency as CurrencyEnum, SecurityMaster, measures as tm
from gs_quant.timeseries.measures_fx_vol import _currencypair_to_tdapi_fxo_asset, _currencypair_to_tdapi_fxfwd_asset
from gs_quant.timeseries.measures_helper import VolReference

_index = [pd.Timestamp('2021-03-30')]
_test_datasets = ('TEST_DATASET',)


def test_currencypair_to_tdapi_fxfwd_asset():
    mock_eur = Cross('MA8RY265Q34P7TWZ', 'EURUSD')
    replace = Replacer()
    xrefs = replace('gs_quant.timeseries.measures_fx_vol._get_tdapi_fxo_assets', Mock())
    xrefs.return_value = 'MA8RY265Q34P7TWZ'
    bbid_mock = replace('gs_quant.timeseries.measures_fx_vol.Asset.get_identifier', Mock())
    bbid_mock.return_value = {'EURUSD'}
    assert _currencypair_to_tdapi_fxfwd_asset(mock_eur) == "MA8RY265Q34P7TWZ"
    replace.restore()


def test_currencypair_to_tdapi_fxo_asset(mocker):
    replace = Replacer()
    mocker.patch.object(GsSession.__class__, 'current',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_get', side_effect=mock_request)
    mocker.patch.object(SecurityMaster, 'get_asset', side_effect=mock_request)
    bbid_mock = replace('gs_quant.timeseries.measures_fx_vol.Asset.get_identifier', Mock())

    with PricingContext(dt.date.today()):
        cur = [
            {
                "currency_assetId": "MAK1FHKH5P5GJSHH",
                "currency": "USDJPY",
                "id": "MAQ7YRZ4P94M9N9C"
            },
            {
                "currency_assetId": "MA66CZBQJST05XKG",
                "currency": "GBPUSD",
                "id": "MAEHA6WVHJ2S3JY9"
            },
            {
                "currency_assetId": "MAJNQPFGN1EBDHAE",
                "currency": "EURUSD",
                "id": "MAT1J37C9ZPMANFP"
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
        expected_rate_option_type = tm_xccy.CrossCurrencyRateOptionType[index]
        actual_rate_option_type = tm_xccy._check_crosscurrency_rateoption_type(CurrencyEnum.GBP, index)
        assert expected_rate_option_type == actual_rate_option_type

    invalid_indices = ['LIBORED', 'TestRateOption']
    for index in invalid_indices:
        with pytest.raises(MqError):
            tm_xccy._check_crosscurrency_rateoption_type(CurrencyEnum.GBP, index)


def test_cross_stored_direction_for_fx_vol():
    replace = Replacer()
    mock_gbp = Cross('MA26QSMPX9990G66', 'GBPUSD')
    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'GBPUSD'
    assert "MAEHA6WVHJ2S3JY9" == tm_fxo.cross_stored_direction_for_fx_vol(mock_gbp)
    replace.restore()
    mock_gbp_reversed = Cross('MA26QSMPX9990G67', 'USDGBP')
    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.side_effect = ['USDGBP', 'GBPUSD']
    assets = replace('gs_quant.markets.securities.SecurityMaster.get_asset', Mock())
    assets.return_value = mock_gbp
    assert "MAEHA6WVHJ2S3JY9" == tm_fxo.cross_stored_direction_for_fx_vol(mock_gbp_reversed)
    replace.restore()

    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.side_effect = [mock_gbp, 'GBPUSD']
    assets = replace('gs_quant.markets.securities.SecurityMaster.get_asset', Mock())
    assets.return_value = mock_gbp
    assert "MAEHA6WVHJ2S3JY9" == tm_fxo.cross_stored_direction_for_fx_vol(mock_gbp)
    replace.restore()


def test_get_tdapi_fxo_assets():
    mock_asset_1 = GsAsset(asset_class='FX', id='MAW8SAXPSKYA94E2', type_='Option', name='FX Forward Test_asset_1')
    mock_asset_2 = GsAsset(asset_class='FX', id='MATDD783JM1C2GGD', type_='Option', name='Test_asset')

    replace = Replacer()
    assets = replace('gs_quant.timeseries.measures.GsAssetApi.get_many_assets', Mock())
    assets.return_value = [mock_asset_1]
    kwargs = dict(asset_parameters_expiration_date='5y', asset_parameters_call_currency='USD',
                  asset_parameters_put_currency='EUR')
    assert 'MAW8SAXPSKYA94E2' == tm_fxo._get_tdapi_fxo_assets(**kwargs)
    replace.restore()

    # Test case: Multiple assets, one with name starting with "FX Forward"
    assets = replace('gs_quant.timeseries.measures.GsAssetApi.get_many_assets', Mock())
    assets.return_value = [mock_asset_1, mock_asset_2]
    kwargs = dict(asset_parameters_expiration_date='5y', asset_parameters_call_currency='USD',
                  asset_parameters_put_currency='EUR', name_prefix='FX Forward')
    assert 'MAW8SAXPSKYA94E2' == tm_fxo._get_tdapi_fxo_assets(**kwargs)
    replace.restore()

    # Test case: Multiple assets, none with name starting with "FX Forward"
    mock_asset_1.name = "Test_asset_1"
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
    assert ['MAW8SAXPSKYA94E2', 'MATDD783JM1C2GGD'] == tm_xccy._get_tdapi_crosscurrency_rates_assets(**kwargs)
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
        'fwdPoints': [4, 5, 6],
        'forwardPoint': [7, 8, 9]
    }
    df = MarketDataResponseFrame(data=d, index=_index * 3)
    df.dataset_ids = _test_datasets
    return df


def mock_fx_spot_carry_3m(*args, **kwargs):
    """Mock Dataset.get_data for 3m tenor with fwdPoints column"""
    d = pd.DataFrame({
        'spot': [1.18250, 1.18566, 1.18511],
        'fwdPoints': [0.00234, 0.00234, 0.00235],
        'tenor': ['3m', '3m', '3m'],
        'date': [pd.Timestamp(2020, 9, 2), pd.Timestamp(2020, 9, 3), pd.Timestamp(2020, 9, 4)],
        'settlementDate': [pd.Timestamp('2020-12-04'), pd.Timestamp('2020-12-08'), pd.Timestamp('2020-12-08')]
    })
    d = d.set_index('date')
    df = MarketDataResponseFrame(d)
    df.dataset_ids = _test_datasets
    return df


def mock_fx_spot_carry_2y(*args, **kwargs):
    """Mock Dataset.get_data for 2y tenor with fwdPoints column"""
    d = pd.DataFrame({
        'spot': [1.18250, 1.18566, 1.18511],
        'fwdPoints': [0.02009, 0.02015, 0.02064],
        'tenor': ['2y', '2y', '2y'],
        'date': [pd.Timestamp(2020, 9, 2), pd.Timestamp(2020, 9, 3), pd.Timestamp(2020, 9, 4)],
        'settlementDate': [pd.Timestamp('2020-12-04'), pd.Timestamp('2020-12-08'), pd.Timestamp('2020-12-08')]
    })
    d = d.set_index('date')
    df = MarketDataResponseFrame(d)
    df.dataset_ids = _test_datasets
    return df


def test_fx_vol_measure(mocker):
    replace = Replacer()
    args = dict(expiry_tenor='1m', strike='ATMF', option_type='Put',
                expiration_location=None,
                location=None, premium_payment_date=None, )

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


def test_fwd_points(mocker):
    replace = Replacer()
    args = dict(settlement_date="6m", location='LDN')
    mock_eur = Cross('MAGZMXVM0J282ZTR', 'EURUSD')
    args['asset'] = mock_eur
    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'EURUSD'

    args['settlement_date'] = '1yr'
    with pytest.raises(MqValueError):
        tm_fxo.fwd_points(**args)
    args['settlement_date'] = '6m'

    args['real_time'] = True
    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'EURUSD'
    identifiers = replace('gs_quant.timeseries.measures_fx_vol._get_tdapi_fxo_assets', Mock())
    identifiers.return_value = {'MAGZMXVM0J282ZTR'}
    mocker.patch.object(GsDataApi, 'get_market_data', return_value=mock_curr(None, None))
    actual = tm_fxo.fwd_points(**args)
    expected = tm.ExtendedSeries([7, 8, 9], index=_index * 3, name='forwardPoint')
    expected.dataset_ids = _test_datasets
    assert_series_equal(expected, actual)
    assert actual.dataset_ids == _test_datasets
    args['real_time'] = False

    args['asset'] = Cross('MAGZMXVM0J282ZTR', 'EURUSD')
    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'EURUSD'
    identifiers = replace('gs_quant.timeseries.measures_fx_vol._get_tdapi_fxo_assets', Mock())
    identifiers.return_value = {'MAGZMXVM0J282ZTR'}
    mocker.patch.object(GsDataApi, 'get_market_data', return_value=mock_curr(None, None))
    actual = tm_fxo.fwd_points(**args)
    expected = tm.ExtendedSeries([4, 5, 6], index=_index * 3, name='fwdPoints')
    expected.dataset_ids = _test_datasets
    assert_series_equal(expected, actual)
    assert actual.dataset_ids == _test_datasets

    args['location'] = None
    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'EURUSD'
    identifiers = replace('gs_quant.timeseries.measures_fx_vol._get_tdapi_fxo_assets', Mock())
    identifiers.return_value = {'MAGZMXVM0J282ZTR'}
    mocker.patch.object(GsDataApi, 'get_market_data', return_value=mock_curr(None, None))
    actual = tm_fxo.fwd_points(**args)
    expected = tm.ExtendedSeries([4, 5, 6], index=_index * 3, name='fwdPoints')
    expected.dataset_ids = _test_datasets
    assert_series_equal(expected, actual)
    assert actual.dataset_ids == _test_datasets

    replace.restore()


def mock_df():
    d = {
        'strikeVol': [5, 1, 2],
    }
    df = MarketDataResponseFrame(data=d, index=_index * 3)
    df.dataset_ids = "FX_VOLATILITY_SWAP"
    return df


def test_vol_swap_strike_raises_exception():
    with pytest.raises(NotImplementedError):
        mock_asset_1 = GsAsset(asset_class='FX', id='MAW8SAXPSKYA94E2', type_='Option', name='Test_asset')
        tm_fxo.vol_swap_strike(mock_asset_1, "none", "none", location=PricingLocation.LDN, real_time=True)


def test_vol_swap_strike_unsupported_cross():
    with pytest.raises(NotImplementedError):
        replace = Replacer()
        mock_asset_1 = Cross('MA667', 'USDPLN')
        xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
        xrefs.return_value = 'USDPLN'

        tm_fxo.vol_swap_strike(mock_asset_1, "none", "none", location=PricingLocation.LDN, real_time=False)
    replace.restore()


def test_vol_swap_strike_matches_multiple_assets():
    with pytest.raises(MqValueError):
        replace = Replacer()
        base = Cross('MA667', 'EURUSD')
        xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
        xrefs.return_value = 'EURUSD'
        mock_asset_1 = GsAsset(asset_class='FX', id='MA123', type_='VolatilitySwap', name='Test_asset')
        assets = replace('gs_quant.timeseries.measures.GsAssetApi.get_many_assets', Mock())
        assets.return_value = [mock_asset_1, mock_asset_1]
        tm_fxo.vol_swap_strike(base, None, location=PricingLocation.LDN, real_time=False)
    replace.restore()


def test_vol_swap_strike_matches_no_assets():
    with pytest.raises(MqValueError):
        replace = Replacer()
        base = Cross('MA667', 'EURUSD')
        xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
        xrefs.return_value = 'EURUSD'

        assets = replace('gs_quant.timeseries.measures.GsAssetApi.get_many_assets', Mock())
        assets.return_value = []
        tm_fxo.vol_swap_strike(base, None, location=PricingLocation.LDN, real_time=False)
    replace.restore()


def test_vol_swap_strike_matches_no_assets_when_expiry_tenor_is_not_none():
    with pytest.raises(MqValueError):
        replace = Replacer()
        base = Cross('MA667', 'EURUSD')
        xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
        xrefs.return_value = 'EURUSD'

        mock_asset_1 = GsAsset(asset_class='FX', id='MA123', type_='VolatilitySwap', name='Test_asset',
                               parameters={"lastFixingDate": "1y"})

        mock_asset_2 = GsAsset(asset_class='FX', id='MA123', type_='VolatilitySwap', name='Test_asset',
                               parameters={"lastFixingDate": "1y"})

        assets = replace('gs_quant.timeseries.measures.GsAssetApi.get_many_assets', Mock())
        assets.return_value = [mock_asset_1, mock_asset_2]

        tm_fxo.vol_swap_strike(base, "10m", location=PricingLocation.LDN, real_time=False)
    replace.restore()


def test_currencypair_to_tdapi_fx_vol_swap_asset():
    replace = Replacer()
    base = Cross('MA667', 'EURUSD')
    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'EURUSD'

    asset = tm_fxo._currencypair_to_tdapi_fx_vol_swap_asset(base)
    assert asset == "MA66A4X4PRTC3N7B"
    replace.restore()


def test_vol_swap_strike():
    replace = Replacer()
    base = Cross('MA667', 'EURUSD')
    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'EURUSD'

    mock_asset_1 = GsAsset(asset_class='FX', id='MA123', type_='VolatilitySwap', name='Test_asset',
                           parameters={"lastFixingDate": "1y"})
    mock_asset_2 = GsAsset(asset_class='FX', id='MA123', type_='VolatilitySwap', name='Test_asset',
                           parameters={"lastFixingDate": "2y"})

    assets = replace('gs_quant.timeseries.measures.GsAssetApi.get_many_assets', Mock())
    assets.return_value = [mock_asset_1, mock_asset_2]
    mock_data = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    mock_data.return_value = mock_df()
    actual = tm_fxo.vol_swap_strike(base, "1y", location=PricingLocation.LDN, real_time=False)
    assert_series_equal(tm_rates._extract_series_from_df(mock_df(), QueryType.STRIKE_VOL), actual)

    actual = tm_fxo.vol_swap_strike(base, "1y", None, real_time=False)
    assert_series_equal(tm_rates._extract_series_from_df(mock_df(), QueryType.STRIKE_VOL), actual)
    replace.restore()


def test_implied_volatility_fxvol(mocker):
    replace = Replacer()

    args = dict(tenor="1y", location=None)
    mock_eur = Cross('MAGZMXVM0J282ZTR', 'EURUSD')
    args['asset'] = mock_eur

    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'EURUSD'
    xrefs = replace('gs_quant.timeseries.measures_fx_vol._cross_stored_direction_helper', Mock())
    xrefs.return_value = 'GBPUSD'
    assets = replace('gs_quant.markets.securities.SecurityMaster.get_asset', Mock())
    assets.return_value = mock_eur

    preprocess_impl_vol = replace('gs_quant.timeseries.measures_fx_vol._preprocess_implied_vol_strikes_fx', Mock())
    replace('gs_quant.timeseries.measures_fx_vol._get_tdapi_fxo_assets', Mock())
    mocker.patch.object(GsDataApi, 'get_market_data', return_value=mock_curr(None, None))
    expected = tm.ExtendedSeries([1, 2, 3], index=_index * 3, name='impliedVolatility')

    args['strike_reference'] = VolReference.DELTA_CALL
    args['relative_strike'] = 50
    preprocess_impl_vol.return_value = ['abc', 50]
    with pytest.raises(MqValueError):
        tm_fxo.implied_volatility_fxvol(**args)

    args['strike_reference'] = VolReference.DELTA_CALL
    args['relative_strike'] = 50
    preprocess_impl_vol.return_value = ['delta', 50]
    actual = tm_fxo.implied_volatility_fxvol(**args)
    assert_series_equal(expected, actual)

    args['strike_reference'] = VolReference.DELTA_PUT
    args['relative_strike'] = 25
    preprocess_impl_vol.return_value = ['delta', -25]
    actual = tm_fxo.implied_volatility_fxvol(**args)
    assert_series_equal(expected, actual)

    args['strike_reference'] = VolReference.DELTA_CALL
    args['relative_strike'] = 0
    preprocess_impl_vol.return_value = ['delta', 0]
    actual = tm_fxo.implied_volatility_fxvol(**args)
    assert_series_equal(expected, actual)

    args['strike_reference'] = VolReference.SPOT
    args['relative_strike'] = 100
    preprocess_impl_vol.return_value = ['spot', 100]
    actual = tm_fxo.implied_volatility_fxvol(**args)
    assert_series_equal(expected, actual)

    args['strike_reference'] = VolReference.FORWARD
    args['relative_strike'] = 100
    preprocess_impl_vol.return_value = ['forward', 100]
    actual = tm_fxo.implied_volatility_fxvol(**args)
    assert_series_equal(expected, actual)

    args['strike_reference'] = VolReference.NORMALIZED
    args['relative_strike'] = 100
    preprocess_impl_vol = replace('gs_quant.timeseries.measures_fx_vol._preprocess_implied_vol_strikes_fx', Mock())
    preprocess_impl_vol.return_value = ['normalized', 0]
    with pytest.raises(MqValueError):
        tm_fxo.implied_volatility_fxvol(**args)

    xrefs = replace('gs_quant.timeseries.measures_fx_vol._cross_stored_direction_helper', Mock())
    xrefs.return_value = 'EURUSD'
    args['strike_reference'] = VolReference.DELTA_CALL
    args['relative_strike'] = 50
    preprocess_impl_vol.return_value = ['delta', 50]
    actual = tm_fxo.implied_volatility_fxvol(**args)
    assert_series_equal(expected, actual)

    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = None
    with pytest.raises(MqValueError):
        tm_fxo.implied_volatility_fxvol(**args)

    replace.restore()


if __name__ == '__main__':
    pytest.main(args=["test_measures_fx_vol.py"])


def test_spot_carry(mocker):
    replace = Replacer()
    mock = Cross('MAA0NE9QX2ABETG6', 'USD/EUR')

    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'USDEUR'

    identifiers = replace('gs_quant.timeseries.measures_fx_vol._get_tdapi_fxo_assets', Mock())
    identifiers.return_value = 'MAA0NE9QX2ABETG6'

    mocker.patch.object(GsDataApi, 'get_market_data', return_value=mock_curr(None, None))

    mock_tdapi_asset_func = replace('gs_quant.timeseries.measures_fx_vol._currencypair_to_tdapi_fxfwd_asset', Mock())
    mock_tdapi_asset_func.return_value = mock.get_marquee_id()
    df = pd.DataFrame({
        '3m': [-0.001978858350951374, -0.0019735843327766817, -0.00198293829264794],
        '2y': [-0.016989429175475686, -0.016994753976688093, -0.017416104834150414],
        '3m_ann': [-0.007660096842392416, -0.007400941247912555, -0.0075142924774027195],
        'date': [pd.Timestamp('2020-09-02'), pd.Timestamp('2020-09-03'), pd.Timestamp('2020-09-04')],
        'settlementDate': [pd.Timestamp('2020-12-04'), pd.Timestamp('2020-12-08'), pd.Timestamp('2020-12-08')]
    })
    df = df.set_index('date')

    with DataContext(dt.date(2020, 9, 2), dt.date(2020, 9, 4)):

        replace('gs_quant.data.dataset.Dataset.get_data', mock_fx_spot_carry_3m)
        actual_3m = gs_quant.timeseries.measures_fx_vol.spot_carry(mock, '3m')
        assert_series_equal(df['3m'], pd.Series(actual_3m, name='3m'))

        actual_3m_ann = gs_quant.timeseries.measures_fx_vol.spot_carry(mock, '3m', tm.FXSpotCarry.ANNUALIZED)
        assert_series_equal(df['3m_ann'], pd.Series(actual_3m_ann, name='3m_ann'))

        with pytest.raises(MqValueError):
            gs_quant.timeseries.measures_fx_vol.spot_carry(mock, '13m')

        replace('gs_quant.data.dataset.Dataset.get_data', mock_fx_spot_carry_2y)
        actual_2y = gs_quant.timeseries.measures_fx_vol.spot_carry(mock, '2y')
        assert_series_equal(df['2y'], pd.Series(actual_2y, name='2y'))

    with pytest.raises(NotImplementedError):
        tm_fxo.spot_carry(mock, '3m', real_time=True)

    mocker.patch.object(GsDataApi, 'get_market_data', return_value=MarketDataResponseFrame())
    with DataContext(dt.date(2020, 9, 2), dt.date(2020, 9, 4)):
        result = tm_fxo.spot_carry(mock, '3m')
        assert result.empty
        assert isinstance(result, pd.Series)

    def mock_empty_dataset(*args, **kwargs):
        return pd.DataFrame()

    mocker.patch.object(GsDataApi, 'get_market_data', return_value=mock_curr(None, None))
    with DataContext(dt.date(2020, 9, 2), dt.date(2020, 9, 4)):
        replace('gs_quant.data.dataset.Dataset.get_data', mock_empty_dataset)
        result = tm_fxo.spot_carry(mock, '3m')
        assert result.empty
        assert isinstance(result, pd.Series)

    replace.restore()
