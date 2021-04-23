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

import gs_quant.timeseries.measures_inflation as tm
import gs_quant.timeseries.measures as tm_rates
from gs_quant.api.gs.assets import GsAsset
from gs_quant.api.gs.data import GsDataApi, MarketDataResponseFrame
from gs_quant.errors import MqError, MqValueError
from gs_quant.session import GsSession, Environment
from gs_quant.target.common import PricingLocation, Currency as CurrEnum
from gs_quant.test.timeseries.utils import mock_request
from gs_quant.timeseries import Currency, CurrencyEnum, SecurityMaster
from gs_quant.timeseries.measures_inflation import _currency_to_tdapi_inflation_swap_rate_asset, \
    INFLATION_RATES_DEFAULTS, TdapiInflationRatesDefaultsProvider

_index = [pd.Timestamp('2021-03-30')]
_test_datasets = ('TEST_DATASET',)


def test_get_floating_rate_option_for_benchmark_retuns_rate():
    provider = TdapiInflationRatesDefaultsProvider(INFLATION_RATES_DEFAULTS)
    value = provider.get_index_for_benchmark(CurrencyEnum.GBP, "UKRPI")
    assert value == "CPI-UKRPI"


def test_get_floating_rate_option_for_benchmark_retuns_rate_usd():
    provider = TdapiInflationRatesDefaultsProvider(INFLATION_RATES_DEFAULTS)
    value = provider.get_index_for_benchmark(CurrencyEnum.USD, "CPURNSA")
    assert value == "CPI-CPURNSA"


def test_currency_to_tdapi_inflation_swap_rate_asset(mocker):
    replace = Replacer()
    mocker.patch.object(GsSession.__class__, 'current',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_get', side_effect=mock_request)
    mocker.patch.object(SecurityMaster, 'get_asset', side_effect=mock_request)
    bbid_mock = replace('gs_quant.timeseries.measures_inflation.Asset.get_identifier', Mock())

    with tm_rates.PricingContext(dt.date.today()):
        cur = [
            {
                "currency_assetId": "MAK1FHKH5P5GJSHH",
                "currency": "JPY",
                "inflation_id": "MA1CENMCA88VXJ28"},
            {
                "currency_assetId": "MA66CZBQJST05XKG",
                "currency": "GBP",
                "inflation_id": "MAW75DV9777630QN"},
            {
                "currency_assetId": "MAJNQPFGN1EBDHAE",
                "currency": "EUR",
                "inflation_id": "MAJTD8XDA8EJZYRG"},
            {
                "currency_assetId": "MAZ7RWC904JYHYPS",
                "currency": "USD",
                "inflation_id": "MA4016GCT3MDRYVY"}

        ]
        for c in cur:
            print(c)
            asset = Currency(c.get("currency_assetId"), c.get("currency"))
            bbid_mock.return_value = c.get("currency")
            mqid = _currency_to_tdapi_inflation_swap_rate_asset(asset)
            assert mqid == c.get("inflation_id")

        bbid_mock.return_value = None
        assert _currency_to_tdapi_inflation_swap_rate_asset(asset) == c.get("currency_assetId")
        replace.restore()


def test_get_inflation_swap_leg_defaults():
    result_dict = dict(currency=CurrEnum.JPY, index_type='CPI-JCPNGENF',
                       pricing_location=PricingLocation.TKO)
    defaults = tm._get_inflation_swap_leg_defaults(CurrEnum.JPY)
    assert result_dict == defaults

    result_dict = dict(currency=CurrEnum.USD, index_type='CPI-CPURNSA',
                       pricing_location=PricingLocation.NYC)
    defaults = tm._get_inflation_swap_leg_defaults(CurrEnum.USD)
    assert result_dict == defaults

    result_dict = dict(currency=CurrEnum.EUR, index_type='CPI-CPXTEMU',
                       pricing_location=PricingLocation.LDN)
    defaults = tm._get_inflation_swap_leg_defaults(CurrEnum.EUR)
    assert result_dict == defaults

    result_dict = dict(currency=CurrEnum.GBP, index_type='CPI-UKRPI',
                       pricing_location=PricingLocation.LDN)
    defaults = tm._get_inflation_swap_leg_defaults(CurrEnum.GBP)
    assert result_dict == defaults


def test_get_inflation_swap_csa_terms():
    valid_ccy = ['EUR', 'GBP', 'USD']
    for ccy in valid_ccy:
        assert dict(csaTerms=ccy + '-1') == tm._get_inflation_swap_csa_terms(ccy, tm.InflationIndexType.UKRPI.value)


def test_check_valid_indices():
    valid_indices = ['UKRPI']
    for index in valid_indices:
        assert tm.InflationIndexType[index] == tm._check_inflation_index_type(CurrencyEnum.GBP, index)

    invalid_indices = ['UKHPI', 'TestCPI']
    for index in invalid_indices:
        with pytest.raises(MqError):
            tm._check_inflation_index_type(CurrencyEnum.GBP, index)


def test_get_tdapi_inflation_rates_assets(mocker):
    mock_asset_1 = GsAsset(asset_class='Rate', id='MA26QSMPX9990G66', type_='InflationSwap', name='Test_asset')
    mock_asset_2 = GsAsset(asset_class='Rate', id='MA44SBCHF192S6FR', type_='InflationSwap', name='Test_asset')

    replace = Replacer()
    assets = replace('gs_quant.timeseries.measures.GsAssetApi.get_many_assets', Mock())
    assets.return_value = [mock_asset_1]
    assert 'MA26QSMPX9990G66' == tm._get_tdapi_inflation_rates_assets()
    replace.restore()

    assets = replace('gs_quant.timeseries.measures.GsAssetApi.get_many_assets', Mock())
    assets.return_value = [mock_asset_1, mock_asset_2]
    kwargs = dict(asset_parameters_termination_date='5y', asset_parameters_effective_date='0b')
    with pytest.raises(MqValueError):
        tm._get_tdapi_inflation_rates_assets(**kwargs)
    replace.restore()

    assets = replace('gs_quant.timeseries.measures.GsAssetApi.get_many_assets', Mock())
    assets.return_value = []
    kwargs = dict(asset_parameters_clearing_house='NONE',
                  pricing_location='LDN')
    with pytest.raises(MqValueError):
        tm._get_tdapi_inflation_rates_assets(**kwargs)
    replace.restore()

    assets = replace('gs_quant.timeseries.measures.GsAssetApi.get_many_assets', Mock())
    assets.return_value = [mock_asset_1, mock_asset_2]
    kwargs = dict()
    assert ['MA26QSMPX9990G66', 'MA44SBCHF192S6FR'] == tm._get_tdapi_inflation_rates_assets(**kwargs)
    replace.restore()

    #   test case will test matching sofr maturity with libor leg and flipping legs to get right asset
    kwargs = dict(type='InflationSwap', asset_parameters_termination_date='5y',
                  asset_parameters_index=tm.InflationIndexType.UKRPI,
                  asset_parameters_clearing_house='None', asset_parameters_effective_date='5y',
                  asset_parameters_notional_currency='GBP',
                  pricing_location='LDN')

    assets = replace('gs_quant.timeseries.measures.GsAssetApi.get_many_assets', Mock())
    assets.return_value = [mock_asset_1]
    assert 'MA26QSMPX9990G66' == tm._get_tdapi_inflation_rates_assets(**kwargs)
    replace.restore()


def mock_curr(_cls, _q):
    d = {
        'swapRate': [1, 2, 3],
    }
    df = MarketDataResponseFrame(data=d, index=_index * 3)
    df.dataset_ids = _test_datasets
    return df


def test_inflation_swap_rate(mocker):
    replace = Replacer()
    args = dict(swap_tenor='5y', index_type='UKRPI', clearing_house='LCH', forward_tenor='5y', real_time=False)

    mock_gbp = Currency('MA26QSMPX9990G66', 'GBP')
    args['asset'] = mock_gbp
    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'GBP'

    args['swap_tenor'] = '5yr'
    with pytest.raises(MqValueError):
        tm.inflation_swap_rate(**args)
    args['swap_tenor'] = '5y'

    args['forward_tenor'] = '5yr'
    with pytest.raises(MqValueError):
        tm.inflation_swap_rate(**args)
    args['forward_tenor'] = '5y'

    args['real_time'] = True
    with pytest.raises(NotImplementedError):
        tm.inflation_swap_rate(**args)
    args['real_time'] = False

    args['asset'] = Currency('MA666', 'AED')
    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'AED'
    with pytest.raises(NotImplementedError):
        tm.inflation_swap_rate(**args)
    args['asset'] = mock_gbp
    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'GBP'

    args['index_type'] = tm.InflationIndexType.TESTCPI
    with pytest.raises(MqValueError):
        tm.inflation_swap_rate(**args)
    args['index_type'] = tm.InflationIndexType.UKRPI

    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'GBP'
    identifiers = replace('gs_quant.timeseries.measures_inflation._get_tdapi_inflation_rates_assets', Mock())
    identifiers.return_value = {'MA26QSMPX9990G66'}
    mocker.patch.object(GsDataApi, 'get_market_data', return_value=mock_curr(None, None))
    actual = tm.inflation_swap_rate(**args)
    expected = tm.ExtendedSeries([1, 2, 3], index=_index * 3, name='swapRate')
    expected.dataset_ids = _test_datasets
    assert_series_equal(expected, actual)
    assert actual.dataset_ids == _test_datasets

    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'EUR'
    identifiers = replace('gs_quant.timeseries.measures_inflation._get_tdapi_inflation_rates_assets', Mock())
    identifiers.return_value = {'MAZBW57ZPS54ET7K'}
    mocker.patch.object(GsDataApi, 'get_market_data', return_value=mock_curr(None, None))
    args['asset'] = Currency('MAZBW57ZPS54ET7K', 'EUR')
    args['index_type'] = 'FRCPXTOB'
    actual = tm.inflation_swap_rate(**args)
    expected = tm.ExtendedSeries([1, 2, 3], index=_index * 3, name='swapRate')
    expected.dataset_ids = _test_datasets
    assert_series_equal(expected, actual)
    assert actual.dataset_ids == _test_datasets
    replace.restore()


if __name__ == '__main__':
    pytest.main(args=["test_measures_inflation.py"])
