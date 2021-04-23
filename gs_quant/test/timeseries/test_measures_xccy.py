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

import gs_quant.timeseries.measures_xccy as tm
import gs_quant.timeseries.measures as tm_rates
from gs_quant.api.gs.assets import GsAsset
from gs_quant.api.gs.data import GsDataApi, MarketDataResponseFrame
from gs_quant.errors import MqError, MqValueError
from gs_quant.session import GsSession, Environment
from gs_quant.target.common import PricingLocation, Currency as CurrEnum
from gs_quant.test.timeseries.utils import mock_request
from gs_quant.timeseries import Currency, Cross, Bond, CurrencyEnum, SecurityMaster
from gs_quant.timeseries.measures_xccy import _currency_to_tdapi_crosscurrency_swap_rate_asset, \
    CROSSCURRENCY_RATES_DEFAULTS, TdapiCrossCurrencyRatesDefaultsProvider

_index = [pd.Timestamp('2021-03-30')]
_test_datasets = ('TEST_DATASET',)


def test_get_floating_rate_option_for_benchmark_retuns_rate():
    provider = TdapiCrossCurrencyRatesDefaultsProvider(CROSSCURRENCY_RATES_DEFAULTS)
    value = provider.get_rateoption_for_benchmark(CurrencyEnum.GBP, "LIBOR")
    assert value == "GBP-LIBOR-BBA"


def test_get_floating_rate_option_for_benchmark_retuns_rate_usd():
    provider = TdapiCrossCurrencyRatesDefaultsProvider(CROSSCURRENCY_RATES_DEFAULTS)
    value = provider.get_rateoption_for_benchmark(CurrencyEnum.USD, "LIBOR")
    assert value == "USD-LIBOR-BBA"


def test_currency_to_tdapi_xccy_swap_rate_asset(mocker):
    replace = Replacer()
    mocker.patch.object(GsSession.__class__, 'current',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_get', side_effect=mock_request)
    mocker.patch.object(SecurityMaster, 'get_asset', side_effect=mock_request)
    bbid_mock = replace('gs_quant.timeseries.measures_xccy.Asset.get_identifier', Mock())

    with tm_rates.PricingContext(dt.date.today()):
        cur = [
            {
                "currency_assetId": "MAK1FHKH5P5GJSHH",
                "currency": "JPY",
                "xccy_id": "MAFMW4HJC5TDE51H"
            },
            {
                "currency_assetId": "MA66CZBQJST05XKG",
                "currency": "GBP",
                "xccy_id": "MATDD783JM1C2GGD"
            },
            {
                "currency_assetId": "MAJNQPFGN1EBDHAE",
                "currency": "EUR",
                "xccy_id": "MAW8SAXPSKYA94E2"
            },
        ]
        for c in cur:
            print(c)
            asset = Currency(c.get("currency_assetId"), c.get("currency"))
            bbid_mock.return_value = c.get("currency")
            mqid = _currency_to_tdapi_crosscurrency_swap_rate_asset(asset)
            assert mqid == c.get("xccy_id")

        bbid_mock.return_value = None
        assert _currency_to_tdapi_crosscurrency_swap_rate_asset(asset) == c.get("currency_assetId")
        replace.restore()


def test_get_crosscurrency_swap_leg_defaults():
    result_dict = dict(currency=CurrEnum.JPY, rateOption="JPY-LIBOR-BBA",
                       designatedMaturity="3m", pricing_location=PricingLocation.TKO)
    defaults = tm._get_crosscurrency_swap_leg_defaults(CurrEnum.JPY, tm.CrossCurrencyRateOptionType.LIBOR)
    assert result_dict == defaults

    result_dict = dict(currency=CurrEnum.EUR, rateOption="EUR-EURIBOR-TELERATE",
                       designatedMaturity="3m", pricing_location=PricingLocation.LDN)
    defaults = tm._get_crosscurrency_swap_leg_defaults(CurrEnum.EUR, tm.CrossCurrencyRateOptionType.LIBOR)
    assert result_dict == defaults

    result_dict = dict(currency=CurrEnum.EUR, rateOption="EUR-EONIA-OIS-COMPOUND",
                       designatedMaturity="3m", pricing_location=PricingLocation.LDN)
    defaults = tm._get_crosscurrency_swap_leg_defaults(CurrEnum.EUR, tm.CrossCurrencyRateOptionType.OIS)
    assert result_dict == defaults

    result_dict = dict(currency=CurrEnum.GBP, rateOption="GBP-LIBOR-BBA",
                       designatedMaturity="3m", pricing_location=PricingLocation.LDN)
    defaults = tm._get_crosscurrency_swap_leg_defaults(CurrEnum.GBP, tm.CrossCurrencyRateOptionType.LIBOR)
    assert result_dict == defaults

    result_dict = dict(currency=CurrEnum.GBP, rateOption="GBP-LIBOR-BBA",
                       designatedMaturity="3m", pricing_location=PricingLocation.LDN)
    defaults = tm._get_crosscurrency_swap_leg_defaults(CurrEnum.GBP, None)
    assert result_dict == defaults


def test_get_crosscurrency_swap_csa_terms():
    valid_ccy = ['EUR', 'GBP', 'JPY']
    for ccy in valid_ccy:
        assert dict(csaTerms=ccy + '-1') == \
               tm._get_crosscurrency_swap_csa_terms(ccy, tm.CrossCurrencyRateOptionType.LIBOR.value)


def test_check_valid_indices():
    valid_indices = ['LIBOR']
    for index in valid_indices:
        assert tm.CrossCurrencyRateOptionType[index] == tm._check_crosscurrency_rateoption_type(CurrencyEnum.GBP, index)

    invalid_indices = ['LIBORED', 'TestRateOption']
    for index in invalid_indices:
        with pytest.raises(MqError):
            tm._check_crosscurrency_rateoption_type(CurrencyEnum.GBP, index)


def test_get_tdapi_crosscurrency_rates_assets(mocker):
    mock_asset_1 = GsAsset(asset_class='Rate', id='MAW8SAXPSKYA94E2', type_='XccySwapMTM', name='Test_asset')
    mock_asset_2 = GsAsset(asset_class='Rate', id='MATDD783JM1C2GGD', type_='XccySwapMTM', name='Test_asset')

    replace = Replacer()
    assets = replace('gs_quant.timeseries.measures.GsAssetApi.get_many_assets', Mock())
    assets.return_value = [mock_asset_1]
    assert 'MAW8SAXPSKYA94E2' == tm._get_tdapi_crosscurrency_rates_assets()
    replace.restore()

    assets = replace('gs_quant.timeseries.measures.GsAssetApi.get_many_assets', Mock())
    assets.return_value = [mock_asset_1, mock_asset_2]
    kwargs = dict(asset_parameters_termination_date='5y', asset_parameters_effective_date='0b')
    with pytest.raises(MqValueError):
        tm._get_tdapi_crosscurrency_rates_assets(**kwargs)
    replace.restore()

    assets = replace('gs_quant.timeseries.measures.GsAssetApi.get_many_assets', Mock())
    assets.return_value = []
    kwargs = dict(asset_parameters_clearing_house='NONE',
                  asset_parameters_payer_rate_option="EUR-EURIBOR-TELERATE",
                  asset_parameters_payer_currency='EUR',
                  asset_parameters_payer_designated_maturity='3m',
                  asset_parameters_receiver_rate_option="USD-LIBOR-BBA",
                  asset_parameters_receiver_currency='USD',
                  asset_parameters_receiver_designated_maturity='3m',
                  pricing_location='LDN')
    with pytest.raises(MqValueError):
        tm._get_tdapi_crosscurrency_rates_assets(**kwargs)
    replace.restore()

    assets = replace('gs_quant.timeseries.measures.GsAssetApi.get_many_assets', Mock())
    assets.return_value = [mock_asset_1, mock_asset_2]
    kwargs = dict()
    assert ['MAW8SAXPSKYA94E2', 'MATDD783JM1C2GGD'] == tm._get_tdapi_crosscurrency_rates_assets(**kwargs)
    replace.restore()

    #   test case will test matching sofr maturity with libor leg and flipping legs to get right asset
    kwargs = dict(type='XccySwapMTM', asset_parameters_termination_date='5y',
                  asset_parameters_payer_rate_option="EUR-EURIBOR-TELERATE",
                  asset_parameters_payer_currency="EUR",
                  asset_parameters_payer_designated_maturity='3m',
                  asset_parameters_receiver_rate_option="USD-LIBOR-BBA",
                  asset_parameters_receiver_currency="USD",
                  asset_parameters_receiver_designated_maturity='3m',
                  asset_parameters_clearing_house='None', asset_parameters_effective_date='5y',
                  pricing_location='LDN')

    assets = replace('gs_quant.timeseries.measures.GsAssetApi.get_many_assets', Mock())
    assets.return_value = [mock_asset_1]
    assert 'MAW8SAXPSKYA94E2' == tm._get_tdapi_crosscurrency_rates_assets(**kwargs)
    replace.restore()


def mock_curr(_cls, _q):
    d = {
        'xccySwapSpread': [1, 2, 3],
    }
    df = MarketDataResponseFrame(data=d, index=_index * 3)
    df.dataset_ids = _test_datasets
    return df


def test_crosscurrency_swap_rate(mocker):
    replace = Replacer()
    args = dict(swap_tenor='5y', rateoption_type='LIBOR', clearing_house='LCH', forward_tenor='5y', real_time=False)

    mock_gbp = Currency('MA26QSMPX9990G66', 'GBP')
    args['asset'] = mock_gbp
    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'GBP'
    xrefs = replace('gs_quant.timeseries.measures.SecurityMaster.get_asset', Mock())
    mock_usd = Currency('MA26QSMPX9990G63', 'USD')
    xrefs.return_value = mock_usd

    args['swap_tenor'] = '5yr'
    with pytest.raises(MqValueError):
        tm.crosscurrency_swap_rate(**args)
    args['swap_tenor'] = '5y'

    args['forward_tenor'] = '5yr'
    with pytest.raises(MqValueError):
        tm.crosscurrency_swap_rate(**args)
    args['forward_tenor'] = '5y'

    args['real_time'] = True
    with pytest.raises(NotImplementedError):
        tm.crosscurrency_swap_rate(**args)
    args['real_time'] = False

    args['asset'] = Currency('MA666', 'AED')
    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'AED'
    with pytest.raises(NotImplementedError):
        tm.crosscurrency_swap_rate(**args)
    args['asset'] = mock_gbp

    args['asset'] = Bond('MA667', 'TEST')
    with pytest.raises(MqValueError):
        tm.crosscurrency_swap_rate(**args)
    args['asset'] = mock_gbp

    args['asset'] = Cross('MA667', 'USDAED')
    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.side_effect = ['AED', 'USD']
    with pytest.raises(NotImplementedError):
        tm.crosscurrency_swap_rate(**args)

    args['asset'] = Cross('MA667', 'USDAED')
    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.side_effect = ['USD', 'AED']
    with pytest.raises(NotImplementedError):
        tm.crosscurrency_swap_rate(**args)

    args['asset'] = Cross('MA667', 'USDGBP')
    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'GBP'
    xrefs = replace('gs_quant.timeseries.measures_xccy._check_crosscurrency_rateoption_type', Mock())
    xrefs.side_effect = [tm.CrossCurrencyRateOptionType.LIBOR, tm.CrossCurrencyRateOptionType.OIS]
    with pytest.raises(MqValueError):
        tm.crosscurrency_swap_rate(**args)
    replace.restore()

    xrefs = replace('gs_quant.timeseries.measures.SecurityMaster.get_asset', Mock())
    xrefs.return_value = mock_usd

    args['asset'] = Cross('MA667', 'USDGBP')
    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'GBP'
    identifiers = replace('gs_quant.timeseries.measures_xccy._get_tdapi_crosscurrency_rates_assets', Mock())
    identifiers.return_value = {'MA26QSMPX9990G66'}
    mocker.patch.object(GsDataApi, 'get_market_data', return_value=mock_curr(None, None))
    actual = tm.crosscurrency_swap_rate(**args)
    expected = tm.ExtendedSeries([1, 2, 3], index=_index * 3, name='xccySwapSpread')
    expected.dataset_ids = _test_datasets
    assert_series_equal(expected, actual)
    assert actual.dataset_ids == _test_datasets

    args['asset'] = Cross('MA667', 'USDCAD')
    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'CAD'
    identifiers = replace('gs_quant.timeseries.measures_xccy._get_tdapi_crosscurrency_rates_assets', Mock())
    identifiers.return_value = {'MA26QSMPX9990G66'}
    mocker.patch.object(GsDataApi, 'get_market_data', return_value=mock_curr(None, None))
    actual = tm.crosscurrency_swap_rate(**args)
    expected = tm.ExtendedSeries([1, 2, 3], index=_index * 3, name='xccySwapSpread')
    expected.dataset_ids = _test_datasets
    assert_series_equal(expected, actual)
    assert actual.dataset_ids == _test_datasets

    args['asset'] = mock_gbp
    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'GBP'

    args['rateoption_type'] = tm.CrossCurrencyRateOptionType.TestRateOption
    with pytest.raises(MqValueError):
        tm.crosscurrency_swap_rate(**args)
    args['rateoption_type'] = tm.CrossCurrencyRateOptionType.LIBOR

    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'GBP'
    identifiers = replace('gs_quant.timeseries.measures_xccy._get_tdapi_crosscurrency_rates_assets', Mock())
    identifiers.return_value = {'MA26QSMPX9990G66'}
    mocker.patch.object(GsDataApi, 'get_market_data', return_value=mock_curr(None, None))
    actual = tm.crosscurrency_swap_rate(**args)
    expected = tm.ExtendedSeries([1, 2, 3], index=_index * 3, name='xccySwapSpread')
    expected.dataset_ids = _test_datasets
    assert_series_equal(expected, actual)
    assert actual.dataset_ids == _test_datasets

    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'EUR'
    identifiers = replace('gs_quant.timeseries.measures_xccy._get_tdapi_crosscurrency_rates_assets', Mock())
    identifiers.return_value = {'MAZBW57ZPS54ET7K'}
    mocker.patch.object(GsDataApi, 'get_market_data', return_value=mock_curr(None, None))
    args['asset'] = Currency('MAZBW57ZPS54ET7K', 'EUR')
    args['rateoption_type'] = 'OIS'
    actual = tm.crosscurrency_swap_rate(**args)
    expected = tm.ExtendedSeries([1, 2, 3], index=_index * 3, name='xccySwapSpread')
    expected.dataset_ids = _test_datasets
    assert_series_equal(expected, actual)
    assert actual.dataset_ids == _test_datasets
    replace.restore()


if __name__ == '__main__':
    pytest.main(args=["test_measures_xccy.py"])
