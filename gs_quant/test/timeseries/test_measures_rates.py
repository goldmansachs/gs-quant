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
import datetime as dt
from typing import Union

import pandas as pd
import pytest
from numpy.testing import assert_allclose
from pandas._testing import assert_series_equal
from testfixtures import Replacer
from testfixtures.mock import Mock

import gs_quant.timeseries.measures as tm
import gs_quant.timeseries.measures_rates as tm_rates
from gs_quant.api.gs.assets import GsTemporalXRef, GsAssetApi
from gs_quant.api.gs.data import MarketDataResponseFrame, QueryType
from gs_quant.data import Fields, Dataset
from gs_quant.data.core import DataContext
from gs_quant.errors import MqValueError, MqError
from gs_quant.markets.securities import Cross, Currency
from gs_quant.session import GsSession, Environment
from gs_quant.target.common import PricingLocation, XRef
from gs_quant.test.timeseries.test_measures import _test_datasets, map_identifiers_default_mocker, \
    mock_empty_market_data_response
from gs_quant.test.timeseries.utils import mock_request
from gs_quant.timeseries import TdapiRatesDefaultsProvider, SWAPTION_DEFAULTS, CurrencyEnum, SecurityMaster, \
    ExtendedSeries
from gs_quant.timeseries.measures_rates import _swaption_build_asset_query, _currency_to_tdapi_swaption_rate_asset, \
    _check_strike_reference, _pricing_location_normalized, _default_pricing_location

_index = [pd.Timestamp('2019-01-01')]


def test_parse_meeting_date():
    with pytest.raises(MqValueError):
        tm_rates.parse_meeting_date(5)
    assert tm_rates.parse_meeting_date('2019-09-01') == dt.date(2019, 9, 1)
    assert tm_rates.parse_meeting_date(dt.date(2019, 9, 1)) == dt.date(2019, 9, 1)
    replace = Replacer()
    # mock
    cbd = replace('gs_quant.timeseries.measures._get_custom_bd', Mock())
    cbd.return_value = pd.tseries.offsets.BusinessDay()
    today = replace('gs_quant.timeseries.measures.pd.Timestamp.today', Mock())
    today.return_value = pd.Timestamp(2019, 5, 25)
    # cases
    assert tm_rates.parse_meeting_date() == dt.date(2019, 5, 24)
    assert tm_rates.parse_meeting_date('3m') == pd.Timestamp(2019, 2, 24)
    assert tm_rates.parse_meeting_date('3b') == pd.Timestamp(2019, 5, 22)
    # restore
    replace.restore()


def test_get_swaption_parameter_floating_rate_option_returns_default():
    provider = TdapiRatesDefaultsProvider(SWAPTION_DEFAULTS)
    value = provider.get_swaption_parameter(CurrencyEnum.GBP, "floatingRateTenor")
    assert value == "6m"


def test_get_swaption_parameter_floating_rate_option_returns_given_value():
    provider = TdapiRatesDefaultsProvider(SWAPTION_DEFAULTS)
    value = provider.get_swaption_parameter(CurrencyEnum.GBP, "floatingRateTenor", "66m")
    assert value == "66m"


def test_get_swaption_parameter_strike_reference_option_returns_default():
    provider = TdapiRatesDefaultsProvider(SWAPTION_DEFAULTS)
    value = provider.get_swaption_parameter(CurrencyEnum.GBP, "strikeReference")
    assert value == "ATM"


def test_get_swaption_parameter_strike_reference_option_returns_given_value():
    provider = TdapiRatesDefaultsProvider(SWAPTION_DEFAULTS)
    value = provider.get_swaption_parameter(CurrencyEnum.GBP, "strikeReference", "ATM+666")
    assert value == "ATM+666"


def test_get_floating_rate_option_for_benchmark_retuns_rate():
    provider = TdapiRatesDefaultsProvider(SWAPTION_DEFAULTS)
    value = provider.get_floating_rate_option_for_benchmark(CurrencyEnum.GBP, "LIBOR")
    assert value == "GBP-LIBOR-BBA"


def test_get_floating_rate_option_for_benchmark_retuns_rate_usd():
    provider = TdapiRatesDefaultsProvider(SWAPTION_DEFAULTS)
    value = provider.get_floating_rate_option_for_benchmark(CurrencyEnum.USD, "LIBOR")
    assert value == "USD-LIBOR-BBA"


def test_check_strike_reference_string():
    data_input = "ATM"
    output = _check_strike_reference(data_input)
    assert data_input == output


def test_check_strike_reference_zero():
    data_input = 0
    output = _check_strike_reference(data_input)
    assert output == "ATM"


def test_check_strike_reference_spot():
    data_input = "spot"
    output = _check_strike_reference(data_input)
    assert output == "ATM"


def test_check_strike_reference_string_positive():
    data_input = "ATM+25"
    output = _check_strike_reference(data_input)
    assert output == "ATM+25"


def test_check_strike_reference_string_negtive():
    data_input = "ATM-25"
    output = _check_strike_reference(data_input)
    assert output == "ATM-25"


def test_check_strike_reference_string_fractional():
    data_input = "ATM-25.5"
    output = _check_strike_reference(data_input)
    assert output == "ATM-25.5"


def test_check_strike_reference_numeric_fractional():
    data_input = 12.5
    output = _check_strike_reference(data_input)
    assert output == "ATM+12.5"


def test_check_strike_reference_numeric():
    data_input = -20
    output = _check_strike_reference(data_input)
    assert output == "ATM-20"


def test_check_strike_reference_throws():
    data_input = "DUXA"
    with pytest.raises(MqValueError):
        _check_strike_reference(data_input)


def test_check_strike_reference_list():
    data_input = ["ATM+20", "ATM-20"]
    output = _check_strike_reference(data_input)
    assert output == data_input


def test_check_strike_reference_invalid_list():
    data_input = ["ATM+20", "MTM-20"]
    with pytest.raises(MqValueError):
        _check_strike_reference(data_input)


def test_pricing_location_normalized():
    assert _pricing_location_normalized(PricingLocation.LDN, CurrencyEnum.USD) == PricingLocation.LDN
    assert _pricing_location_normalized(PricingLocation.TKO, CurrencyEnum.USD) == PricingLocation.TKO
    assert _pricing_location_normalized(PricingLocation.LDN, CurrencyEnum.HKD) == PricingLocation.LDN
    assert _pricing_location_normalized(PricingLocation.TKO, CurrencyEnum.HKD) == PricingLocation.HKG


def test_default_pricing_location():
    assert _default_pricing_location(CurrencyEnum.USD) == PricingLocation.NYC
    with pytest.raises(MqValueError):
        _default_pricing_location(CurrencyEnum.EGP)


def test_currency_to_tdapi_swaption_rate_asset_retuns_throws():
    replace = Replacer()
    replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock()).return_value = "ZAR"
    asset = Currency("MA1", "ZAR")

    assert _currency_to_tdapi_swaption_rate_asset(asset) == "MA1"
    replace.restore()


def test_currency_to_tdapi_midcurve_asset():
    replace = Replacer()
    replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock()).return_value = 'ZAR'
    asset = Currency('MA1', 'ZAR')
    assert tm_rates._currency_to_tdapi_midcurve_asset(asset) == 'MA1'
    replace.restore()


def test_currency_to_tdapi_swaption_rate_asset_retuns_asset_id(mocker):
    replace = Replacer()
    mocker.patch.object(GsSession.__class__, 'current',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_get', side_effect=mock_request)
    mocker.patch.object(SecurityMaster, 'get_asset', side_effect=mock_request)
    bbid_mock = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())

    with tm.PricingContext(dt.date.today()):
        cur = [
            {
                "currency_assetId": "MAK1FHKH5P5GJSHH",
                "currency": "JPY",
                "swaption_id": "MATT7CA7PRA4B8YB"},
            {
                "currency_assetId": "MA66CZBQJST05XKG",
                "currency": "GBP",
                "swaption_id": "MAX2SBXZRPYR3NTY"},
            {
                "currency_assetId": "MAPSDDS072PHYMVQ",
                "currency": "AUD",
                "swaption_id": "MAQHSC1PAF4X5H4B"},
            {
                "currency_assetId": "MAJNQPFGN1EBDHAE",
                "currency": "EUR",
                "swaption_id": "MAZB3PAH8JFVVT80"},
            {
                "currency_assetId": "MAZ7RWC904JYHYPS",
                "currency": "USD",
                "swaption_id": "MAY0X3KRD4AN77E2"}

        ]
        for c in cur:
            print(c)
            asset = Currency(c.get("currency_assetId"), c.get("currency"))
            bbid_mock.return_value = c.get("currency")
            mqid = _currency_to_tdapi_swaption_rate_asset(asset)
            assert mqid == c.get("swaption_id")

        bbid_mock.return_value = None
        assert _currency_to_tdapi_swaption_rate_asset(asset) == c.get("currency_assetId")
        replace.restore()


def test_swaption_build_asset_query_throws_on_invalid_tenor():
    with pytest.raises(MqValueError):
        _swaption_build_asset_query(CurrencyEnum.USD, expiration_tenor="Abc")


def test_swaption_build_asset_query_usd():
    defautls = _swaption_build_asset_query(CurrencyEnum.USD)
    assert defautls["asset_parameters_floating_rate_option"] == "USD-LIBOR-BBA"
    assert defautls["asset_parameters_clearing_house"] == "LCH"
    assert defautls["asset_parameters_termination_date"] == "5y"
    assert defautls["asset_parameters_expiration_date"] == "1y"
    assert defautls["asset_parameters_effective_date"] == "0b"
    assert defautls["asset_parameters_strike"] == "ATM"


def test_swaption_build_asset_query_strike_reference():
    defautls = _swaption_build_asset_query(CurrencyEnum.USD, None, None, None, None,
                                           "ATM+50")
    assert defautls["asset_parameters_floating_rate_option"] == "USD-LIBOR-BBA"
    assert defautls["asset_parameters_clearing_house"] == "LCH"
    assert defautls["asset_parameters_floating_rate_designated_maturity"] == "3m"
    assert defautls["asset_parameters_termination_date"] == "5y"
    assert defautls["asset_parameters_expiration_date"] == "1y"
    assert defautls["asset_parameters_effective_date"] == "0b"
    assert defautls["asset_parameters_strike"] == "ATM+50"


def test_swaption_build_asset_query_clearing_house():
    defautls = _swaption_build_asset_query(CurrencyEnum.USD, None, None, None, "12m",
                                           "ATM+50", None, "ABC")
    assert defautls["asset_parameters_floating_rate_option"] == "USD-LIBOR-BBA"
    assert defautls["asset_parameters_floating_rate_designated_maturity"] == "12m"
    assert defautls["asset_parameters_clearing_house"] == "ABC"
    assert defautls["asset_parameters_termination_date"] == "5y"
    assert defautls["asset_parameters_expiration_date"] == "1y"
    assert defautls["asset_parameters_effective_date"] == "0b"
    assert defautls["asset_parameters_strike"] == "ATM+50"


def test_swaption_build_asset_query_custom():
    defautls = _swaption_build_asset_query(CurrencyEnum.USD, "LIBOR", "12y", "66y", "12m", "ATM+50", "120y", "ABC")
    assert defautls["asset_parameters_floating_rate_option"] == "USD-LIBOR-BBA"
    assert defautls["asset_parameters_floating_rate_designated_maturity"] == "12m"
    assert defautls["asset_parameters_clearing_house"] == "ABC"
    assert defautls["asset_parameters_termination_date"] == "120y"
    assert defautls["asset_parameters_expiration_date"] == "66y"
    assert defautls["asset_parameters_effective_date"] == "12y"
    assert defautls["asset_parameters_strike"] == "ATM+50"


def test_swaption_build_asset_query_custom_throws():
    with pytest.raises(MqValueError):
        _swaption_build_asset_query(CurrencyEnum.USD, "NIBOR", "12y", "66y", "12m", "ATM+50", "120y", "ABC")


def test_swaption_swaption_vol_term2_returns_data():
    replace = Replacer()
    df = MarketDataResponseFrame(
        data=dict(expirationTenor=['1m', '6m', '1y'], terminationTenor=['1y', '2y', '3y'], swaptionVol=[1, 2, 3]),
        index=_index * 3)

    replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock()).return_value = "GBP"
    replace('gs_quant.timeseries.measures_rates._get_tdapi_rates_assets', Mock(), Mock()).return_value = [
        "MADWG3WHCKNE1DJA", "MAH6JK3TZJJGFQ65"]
    replace('gs_quant.timeseries.measures_rates._range_from_pricing_date', Mock(), Mock()).return_value = [
        dt.date(2020, 1, 2), dt.date(2020, 1, 2)]
    replace('gs_quant.timeseries.measures_rates._market_data_timed', Mock()).return_value = df

    with DataContext('2019-01-01', '2025-01-01'):
        actual = tm_rates.swaption_vol_term(Currency("GBP", name="GBP"), tm.SwaptionTenorType.SWAP_MATURITY, '5y', 0)
    expected = pd.Series([1, 2, 3], index=pd.to_datetime(['2019-02-01', '2019-07-01', '2020-01-01']))
    assert_series_equal(expected, pd.Series(actual), check_names=False)

    with DataContext('2019-01-01', '2025-01-01'):
        actual = tm_rates.swaption_vol_term(Currency("GBP", name="GBP"), tm.SwaptionTenorType.OPTION_EXPIRY, '5y', 0)
    expected = pd.Series([1, 2, 3], index=pd.to_datetime(['2020-01-01', '2021-01-01', '2021-12-31']))
    assert_series_equal(expected, pd.Series(actual), check_names=False)
    replace.restore()


def test_swaption_swaption_vol_term2_returns_empty():
    replace = Replacer()
    df = ExtendedSeries(dtype=float)
    replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock()).return_value = "GBP"
    replace('gs_quant.timeseries.measures_rates._get_tdapi_rates_assets', Mock(), Mock()).return_value = [
        "MADWG3WHCKNE1DJA", "MAH6JK3TZJJGFQ65"]
    replace('gs_quant.timeseries.measures_rates._range_from_pricing_date', Mock(), Mock()).return_value = [
        dt.date(2020, 1, 2), dt.date(2020, 1, 2)]
    replace('gs_quant.timeseries.measures_rates._market_data_timed', Mock()).return_value = df

    with DataContext('2019-01-01', '2025-01-01'):
        actual = tm_rates.swaption_vol_term(Currency("GBP", name="GBP"), tm.SwaptionTenorType.SWAP_MATURITY, '5y', 0)

    assert_series_equal(ExtendedSeries(dtype=float), actual, check_names=False)
    replace.restore()


def test_swaption_swaption_vol_term2_throws():
    with pytest.raises(NotImplementedError):
        tm_rates.swaption_vol_term(Currency("GBP", name="GBP"), tm.SwaptionTenorType.SWAP_MATURITY, '5y', 0,
                                   real_time=True)


def test_swaption_vol_smile2_returns_data():
    replace = Replacer()
    test_data = dict(strikeRelative=["ATM", "ATM+50", "ATM+100"], swaptionVol=[1, 2, 3])
    df = MarketDataResponseFrame(data=test_data, index=_index * 3)

    replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock()).return_value = "GBP"
    replace('gs_quant.timeseries.measures_rates._get_tdapi_rates_assets', Mock(), Mock()).return_value = [
        "MADWG3WHCKNE1DJA", "MAH6JK3TZJJGFQ65"]
    replace('gs_quant.timeseries.measures_rates._range_from_pricing_date', Mock(), Mock()).return_value = [
        dt.date(2020, 1, 2), dt.date(2020, 1, 2)]
    replace('gs_quant.timeseries.measures_rates._market_data_timed', Mock()).return_value = df

    with DataContext('2019-01-01', '2025-01-01'):
        actual = tm_rates.swaption_vol_smile(Currency("GBP", name="GBP"), '3m', '10y')
    assert_series_equal(pd.Series([1, 2, 3], index=[0.0, 50.0, 100.0]), pd.Series(actual))
    replace.restore()


def test_swaption_vol_smile2_returns_no_data():
    replace = Replacer()
    df = ExtendedSeries(dtype=float)
    replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock()).return_value = "GBP"
    replace('gs_quant.timeseries.measures_rates._get_tdapi_rates_assets', Mock(), Mock()).return_value = [
        "MADWG3WHCKNE1DJA", "MAH6JK3TZJJGFQ65"]
    replace('gs_quant.timeseries.measures_rates._range_from_pricing_date', Mock(), Mock()).return_value = [
        dt.date(2020, 1, 2), dt.date(2020, 1, 2)]
    replace('gs_quant.timeseries.measures_rates._market_data_timed', Mock()).return_value = df

    with DataContext('2019-01-01', '2025-01-01'):
        actual = tm_rates.swaption_vol_smile(Currency("GBP", name="GBP"), '3m', '10y')
    assert_series_equal(ExtendedSeries(dtype=float), actual)
    replace.restore()


def test_swaption_vol_smile2_returns_throws():
    with pytest.raises(NotImplementedError):
        tm_rates.swaption_vol_smile(Currency("GBP", name="GBP"), "1m", "1m",
                                    real_time=True)


def test_swaption_vol2_return_data():
    replace = Replacer()
    test_data = dict(swaptionVol=[1, 2, 3])
    df = MarketDataResponseFrame(data=test_data, index=[dt.date(2019, 1, 1), dt.date(2019, 1, 2),
                                                        dt.date(2019, 1, 3)])

    replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock()).return_value = "GBP"
    replace('gs_quant.timeseries.measures_rates._get_tdapi_rates_assets', Mock(), Mock()).return_value = [
        "MADWG3WHCKNE1DJA", "MAH6JK3TZJJGFQ65"]
    replace('gs_quant.timeseries.measures_rates._range_from_pricing_date', Mock(), Mock()).return_value = [
        dt.date(2019, 1, 2), dt.date(2019, 1, 5)]
    replace('gs_quant.timeseries.measures_rates._market_data_timed', Mock()).return_value = df

    actual = tm_rates.swaption_vol(Currency("GBP", name="GBP"))
    assert_series_equal(tm._extract_series_from_df(df, QueryType.SWAPTION_VOL), actual)
    replace.restore()


def test_swaption_vol2_return__empty_data():
    replace = Replacer()
    df = ExtendedSeries(dtype=float)

    replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock()).return_value = "GBP"
    replace('gs_quant.timeseries.measures_rates._get_tdapi_rates_assets', Mock(), Mock()).return_value = [
        "MADWG3WHCKNE1DJA", "MAH6JK3TZJJGFQ65"]
    replace('gs_quant.timeseries.measures_rates._range_from_pricing_date', Mock(), Mock()).return_value = [
        dt.date(2019, 1, 2), dt.date(2019, 1, 5)]
    replace('gs_quant.timeseries.measures_rates._market_data_timed', Mock()).return_value = df

    actual = tm_rates.swaption_vol(Currency("GBP", name="GBP"))
    assert_series_equal(ExtendedSeries(dtype=float), actual)
    replace.restore()


def test_swaption_annuity_return_data():
    replace = Replacer()
    test_data = dict(swaptionAnnuity=[1, 2, 3])
    df = MarketDataResponseFrame(data=test_data, index=[dt.date(2019, 1, 1), dt.date(2019, 1, 2),
                                                        dt.date(2019, 1, 3)])

    replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock()).return_value = "GBP"
    replace('gs_quant.timeseries.measures_rates._get_tdapi_rates_assets', Mock(), Mock()).return_value = [
        "MADWG3WHCKNE1DJA", "MAH6JK3TZJJGFQ65"]
    replace('gs_quant.timeseries.measures_rates._range_from_pricing_date', Mock(), Mock()).return_value = [
        dt.date(2019, 1, 2), dt.date(2019, 1, 5)]
    replace('gs_quant.timeseries.measures_rates._market_data_timed', Mock()).return_value = df

    actual = tm_rates.swaption_annuity(Currency("GBP", name="GBP"))
    assert_series_equal(tm._extract_series_from_df(df, QueryType.SWAPTION_ANNUITY), actual)
    replace.restore()


def test_swaption_premium_return_data():
    replace = Replacer()
    test_data = dict(swaptionPremium=[1, 2, 3])
    df = MarketDataResponseFrame(data=test_data, index=[dt.date(2019, 1, 1), dt.date(2019, 1, 2),
                                                        dt.date(2019, 1, 3)])

    replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock()).return_value = "GBP"
    replace('gs_quant.timeseries.measures_rates._get_tdapi_rates_assets', Mock(),
            Mock()).return_value = "MADWG3WHCKNE1DJA"
    replace('gs_quant.timeseries.measures_rates._range_from_pricing_date', Mock(), Mock()).return_value = [
        dt.date(2019, 1, 2), dt.date(2019, 1, 5)]
    replace('gs_quant.timeseries.measures_rates._market_data_timed', Mock()).return_value = df

    actual = tm_rates.swaption_premium(Currency("GBP", name="GBP"))
    assert_series_equal(tm._extract_series_from_df(df, QueryType.SWAPTION_PREMIUM), actual)
    replace.restore()


def test_swaption_premium_throws_for_realtime():
    with pytest.raises(NotImplementedError):
        tm_rates.swaption_premium(Currency("GBP", name="GBP"), real_time=True)


def test__check_forward_tenor_returns_None():
    assert tm_rates._check_forward_tenor(None) is None


def test__check_forward_tenor_returns_0b():
    assert tm_rates._check_forward_tenor("spot") == '0b'


def test_swaption_premium_throws_for_unsupported_ccy():
    replace = Replacer()
    replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock()).return_value = "ZAR"
    with pytest.raises(NotImplementedError):
        tm_rates.swaption_premium(Currency("KRW", name="KRW"))
    replace.restore()


def test_swaption_atmFwdRate_return_data():
    replace = Replacer()
    test_data = dict(atmFwdRate=[1, 2, 3])
    df = MarketDataResponseFrame(data=test_data, index=[dt.date(2019, 1, 1), dt.date(2019, 1, 2),
                                                        dt.date(2019, 1, 3)])

    replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock()).return_value = "GBP"
    replace('gs_quant.timeseries.measures_rates._get_tdapi_rates_assets', Mock(), Mock()).return_value = [
        "MADWG3WHCKNE1DJA", "MAH6JK3TZJJGFQ65"]
    replace('gs_quant.timeseries.measures_rates._range_from_pricing_date', Mock(), Mock()).return_value = [
        dt.date(2019, 1, 2), dt.date(2019, 1, 5)]
    replace('gs_quant.timeseries.measures_rates._market_data_timed', Mock()).return_value = df

    actual = tm_rates.swaption_atm_fwd_rate(Currency("GBP", name="GBP"))
    assert_series_equal(tm._extract_series_from_df(df, QueryType.ATM_FWD_RATE), actual)
    replace.restore()


def test_midcurve_atmFwdRate_return_data():
    replace = Replacer()
    test_data = dict(midcurveAtmFwdRate=[1, 2, 3])
    df = MarketDataResponseFrame(data=test_data, index=[dt.date(2019, 1, 1), dt.date(2019, 1, 2),
                                                        dt.date(2019, 1, 3)])

    replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock()).return_value = "GBP"
    replace('gs_quant.timeseries.measures_rates._get_tdapi_rates_assets', Mock(), Mock()).return_value = [
        "MADWG3WHCKNE1DJA", "MAH6JK3TZJJGFQ65"]
    replace('gs_quant.timeseries.measures_rates._range_from_pricing_date', Mock(), Mock()).return_value = [
        dt.date(2019, 1, 2), dt.date(2019, 1, 5)]
    replace('gs_quant.timeseries.measures_rates._market_data_timed', Mock()).return_value = df

    actual = tm_rates.midcurve_atm_fwd_rate(Currency("GBP", name="GBP"), "1y", "1y", "1y")
    assert_series_equal(tm._extract_series_from_df(df, QueryType.MIDCURVE_ATM_FWD_RATE), actual)
    replace.restore()


def test_midcurve_annuity_return_data():
    replace = Replacer()
    test_data = dict(midcurveAnnuity=[1, 2, 3])
    df = MarketDataResponseFrame(data=test_data, index=[dt.date(2019, 1, 1), dt.date(2019, 1, 2),
                                                        dt.date(2019, 1, 3)])

    replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock()).return_value = "GBP"
    replace('gs_quant.timeseries.measures_rates._get_tdapi_rates_assets', Mock(), Mock()).return_value = [
        "MADWG3WHCKNE1DJA", "MAH6JK3TZJJGFQ65"]
    replace('gs_quant.timeseries.measures_rates._range_from_pricing_date', Mock(), Mock()).return_value = [
        dt.date(2019, 1, 2), dt.date(2019, 1, 5)]
    replace('gs_quant.timeseries.measures_rates._market_data_timed', Mock()).return_value = df

    actual = tm_rates.midcurve_annuity(Currency("GBP", name="GBP"), "1y", "1y", "1y", 0)
    assert_series_equal(tm._extract_series_from_df(df, QueryType.MIDCURVE_ANNUITY), actual)
    replace.restore()


def test_midcurve_premium_return_data():
    replace = Replacer()
    test_data = dict(midcurvePremium=[1, 2, 3])
    df = MarketDataResponseFrame(data=test_data, index=[dt.date(2019, 1, 1), dt.date(2019, 1, 2),
                                                        dt.date(2019, 1, 3)])

    replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock()).return_value = "GBP"
    replace('gs_quant.timeseries.measures_rates._get_tdapi_rates_assets', Mock(), Mock()).return_value = [
        "MADWG3WHCKNE1DJA", "MAH6JK3TZJJGFQ65"]
    replace('gs_quant.timeseries.measures_rates._range_from_pricing_date', Mock(), Mock()).return_value = [
        dt.date(2019, 1, 2), dt.date(2019, 1, 5)]
    replace('gs_quant.timeseries.measures_rates._market_data_timed', Mock()).return_value = df

    actual = tm_rates.midcurve_premium(Currency("GBP", name="GBP"), "1y", "1y", "1y", 0)
    assert_series_equal(tm._extract_series_from_df(df, QueryType.MIDCURVE_PREMIUM), actual)
    replace.restore()


def test_midcurve_vol_return_data():
    replace = Replacer()
    test_data = dict(midcurveVol=[1, 2, 3])
    df = MarketDataResponseFrame(data=test_data, index=[dt.date(2019, 1, 1), dt.date(2019, 1, 2),
                                                        dt.date(2019, 1, 3)])

    replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock()).return_value = "GBP"
    replace('gs_quant.timeseries.measures_rates._get_tdapi_rates_assets', Mock(), Mock()).return_value = [
        "MADWG3WHCKNE1DJA", "MAH6JK3TZJJGFQ65"]
    replace('gs_quant.timeseries.measures_rates._range_from_pricing_date', Mock(), Mock()).return_value = [
        dt.date(2019, 1, 2), dt.date(2019, 1, 5)]
    replace('gs_quant.timeseries.measures_rates._market_data_timed', Mock()).return_value = df

    actual = tm_rates.midcurve_vol(Currency("GBP", name="GBP"), "1y", "1y", "1y", 0)
    assert_series_equal(tm._extract_series_from_df(df, QueryType.MIDCURVE_VOL), actual)
    replace.restore()


def test_cross_to_fxfwd_xcswp_asset(mocker):
    replace = Replacer()
    mocker.patch.object(GsSession.__class__, 'current',
                        return_value=GsSession.get(Environment.DEV, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_get', side_effect=mock_request)
    mocker.patch.object(SecurityMaster, 'get_asset', side_effect=mock_request)
    bbid_mock = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    correct_mapping = {
        'EURUSD': {"id": 'MA1VJC1E3SZW8E4S', "crossID": "MAA9MVX15AJNQCVG"},
        'GBPUSD': {"id": 'MA3JTR4HSC63H4V6', "crossID": "MA58R87SPRMKKE7Z"},
        'AUDUSD': {"id": 'MAD4VBRWYXFSY1N4', "crossID": "MAJTN2XJVF97SYJK"},
        'NZDUSD': {"id": 'MA1YHQMZVTM3VBWT', "crossID": "MANQ8REB1VJ4JFTR"},
        'USDSEK': {"id": 'MA2APZREBGDMME83', "crossID": "MA4ZD5CZGC3Y6JZD"},
        'USDNOK': {"id": 'MA0K3W6FKH6K1KJE', "crossID": "MAZ0P16RPG5P0MVF"},
        'USDDKK': {"id": 'MA328HZB86DYSWSJ', "crossID": "MABCHYGJ1TCBCQE4"},
        'USDCAD': {"id": 'MAT8JNEE2GN5NES6', "crossID": "MAP8G81B2KHTYR07"},
        'USDCHF': {"id": 'MABNGGTNB9A0TKCG', "crossID": "MAMPQHNP1A26RS1C"},
        'USDJPY': {"id": 'MAMZ9YG8AF3HQ18C', "crossID": "MAYJPCVVF2RWXCES"},
    }

    with tm.PricingContext(dt.date.today()):
        for cross in correct_mapping:
            asset = Cross(correct_mapping[cross]["crossID"], cross)
            bbid_mock.return_value = cross
            correct_id = tm_rates._cross_to_fxfwd_xcswp_asset(asset)
            assert correct_mapping[cross]["id"] == correct_id
    replace.restore()


def test_ois_fxfwd_xcswap_measures(mocker):
    replace = Replacer()
    dict_fns = {
        "oisXccy": {"fn": tm_rates.ois_xccy, "queryType": QueryType.OIS_XCCY},
        "oisXccyExSpike": {"fn": tm_rates.ois_xccy_ex_spike, "queryType": QueryType.OIS_XCCY_EX_SPIKE},
        "usdOis": {"fn": tm_rates.usd_ois, "queryType": QueryType.USD_OIS},
        "nonUsdOis": {"fn": tm_rates.non_usd_ois, "queryType": QueryType.NON_USD_OIS},
    }
    args = dict(tenor='3y', real_time=False)
    for key in dict_fns:
        fn = dict_fns[key]["fn"]
        mock_jpy = Cross('MAYJPCVVF2RWXCES', 'USD/JPY')
        xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
        xrefs.return_value = 'JPYUSD'
        args['asset'] = mock_jpy
        with pytest.raises(NotImplementedError):
            fn(**args)

        mock_eur = Cross('MAA0NE9QX2ABETG6', 'EUR/USD')
        args['asset'] = mock_eur
        xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
        xrefs.return_value = 'EURUSD'
        with pytest.raises(NotImplementedError):
            fn(..., real_time=True)

        args['tenor'] = '5yr'
        with pytest.raises(MqValueError):
            fn(**args)
        args['tenor'] = '3y'

        test_data = {key: [1, 2, 3]}
        df = MarketDataResponseFrame(data=test_data, index=[dt.date(2019, 1, 1), dt.date(2019, 1, 2),
                                                            dt.date(2019, 1, 3)])
        identifiers = replace('gs_quant.timeseries.measures_rates._get_tdapi_rates_assets', Mock())
        identifiers.return_value = {'MAA9MVX15AJNQCVG'}  # Test on EURUSD only
        replace('gs_quant.timeseries.measures_rates._range_from_pricing_date', Mock(), Mock()).return_value = [
            dt.date(2019, 1, 2), dt.date(2019, 1, 5)]
        replace('gs_quant.timeseries.measures_rates._market_data_timed', Mock()).return_value = df

        expected = tm_rates._extract_series_from_df(df, dict_fns[key]["queryType"])
        actual = fn(**args)
        assert_series_equal(expected, actual)

        replace.restore()


def get_data_policy_rate_expectation_mocker(
        start: Union[dt.date, dt.datetime] = None,
        end: Union[dt.date, dt.datetime] = None,
        as_of: dt.datetime = None,
        since: dt.datetime = None,
        fields: Union[str, Fields] = None,
        asset_id_type: str = None,
        **kwargs) -> pd.DataFrame:
    if 'meetingNumber' in kwargs:
        if kwargs['meetingNumber'] == 0:
            return mock_meeting_spot()
    elif 'meetingDate' in kwargs:
        if kwargs['meetingDate'] == dt.date(2019, 10, 24):
            return mock_meeting_spot()
    return mock_meeting_expectation()


def mock_meeting_expectation():
    data_dict = MarketDataResponseFrame({'date': [dt.date(2019, 12, 6)],
                                         'assetId': ['MARFAGXDQRWM07Y2'],
                                         'location': ['NYC'],
                                         'rateType': ['Meeting Forward'],
                                         'startingDate': [dt.date(2020, 1, 29)],
                                         'endingDate': [dt.date(2020, 1, 29)],
                                         'meetingNumber': [2],
                                         'valuationDate': [dt.date(2019, 12, 6)],
                                         'meetingDate': [dt.date(2020, 1, 23)],
                                         'value': [-0.004550907771]
                                         })
    data_dict.dataset_ids = _test_datasets
    return data_dict


def mock_meeting_spot():
    data_dict = MarketDataResponseFrame({'date': [dt.date(2019, 12, 6)],
                                         'assetId': ['MARFAGXDQRWM07Y2'],
                                         'location': ['NYC'],
                                         'rateType': ['Meeting Forward'],
                                         'startingDate': [dt.date(2019, 10, 30)],
                                         'endingDate': [dt.date(2019, 12, 18)],
                                         'meetingNumber': [0],
                                         'valuationDate': [dt.date(2019, 12, 6)],
                                         'meetingDate': [dt.date(2019, 10, 24)],
                                         'value': [-0.004522570525]
                                         })
    data_dict.dataset_ids = _test_datasets
    return data_dict


def mock_meeting_absolute():
    data_dict = MarketDataResponseFrame({'date': [datetime.date(2019, 12, 6), datetime.date(2019, 12, 6)],
                                         'assetId': ['MARFAGXDQRWM07Y2', 'MARFAGXDQRWM07Y2'],
                                         'location': ['NYC', 'NYC'],
                                         'rateType': ['Meeting Forward', 'Meeting Forward'],
                                         'startingDate': [datetime.date(2019, 10, 30), datetime.date(2020, 1, 29)],
                                         'endingDate': [datetime.date(2019, 10, 30), datetime.date(2020, 1, 29)],
                                         'meetingNumber': [0, 2],
                                         'valuationDate': [datetime.date(2019, 12, 6), datetime.date(2019, 12, 6)],
                                         'meetingDate': [datetime.date(2019, 10, 24), datetime.date(2020, 1, 23)],
                                         'value': [-0.004522570525, -0.004550907771]
                                         })
    data_dict.dataset_ids = _test_datasets
    return data_dict


def mock_ois_spot():
    data_dict = MarketDataResponseFrame({'date': [datetime.date(2019, 12, 6)],
                                         'assetId': ['MARFAGXDQRWM07Y2'],
                                         'location': ['NYC'],
                                         'rateType': ['Spot'],
                                         'startingDate': [datetime.date(2019, 12, 6)],
                                         'endingDate': [datetime.date(2019, 12, 7)],
                                         'meetingNumber': [-1],
                                         'valuationDate': [datetime.date(2019, 12, 6)],
                                         'meetingDate': [datetime.date(2019, 12, 6)],
                                         'value': [-0.00455]
                                         })
    data_dict.dataset_ids = _test_datasets
    return data_dict


def test_get_default_ois_benchmark(mocker):
    assert tm_rates._get_default_ois_benchmark(CurrencyEnum.USD) == tm_rates.BenchmarkTypeCB.Fed_Funds
    assert tm_rates._get_default_ois_benchmark(CurrencyEnum.EUR) == tm_rates.BenchmarkTypeCB.EUROSTR
    assert tm_rates._get_default_ois_benchmark(CurrencyEnum.GBP) == tm_rates.BenchmarkTypeCB.SONIA


def test_policy_rate_term_structure(mocker):
    target = {
        'meeting_absolute': -0.004550907771,
        'meeting_relative': -0.00002833724599999969,
        'eoy_absolute': -0.003359767756,
        'eoy_relative': 0.001162802769,
        'spot': -0.00455
    }
    mock_eur = Currency('MARFAGXDQRWM07Y2', 'EUR')

    with DataContext(dt.date(2019, 12, 6), dt.date(2019, 12, 6)):
        replace = Replacer()
        xrefs = replace('gs_quant.timeseries.measures.GsAssetApi.get_asset_xrefs', Mock())
        xrefs.return_value = [GsTemporalXRef(dt.date(2019, 1, 1), dt.date(2952, 12, 31), XRef(bbid='EUR', ))]
        mocker.patch.object(GsAssetApi, 'map_identifiers', side_effect=map_identifiers_default_mocker)

        mock_get_data = replace('gs_quant.data.dataset.Dataset.get_data', Mock())
        mock_get_data.return_value = mock_meeting_absolute()

        actual_abs = tm_rates.policy_rate_term_structure(
            mock_eur,
            tm_rates.EventType.MEETING,
            tm_rates.RateType.ABSOLUTE,
            dt.date(2019, 12, 6))
        assert (target['meeting_absolute'] == actual_abs.loc[dt.date(2020, 1, 23)])
        assert actual_abs.dataset_ids == (Dataset.GS.CENTRAL_BANK_WATCH,)

        actual_rel = tm_rates.policy_rate_term_structure(
            mock_eur,
            tm_rates.EventType.MEETING,
            tm_rates.RateType.RELATIVE,
            dt.date(2019, 12, 6))
        assert (target['meeting_relative'] == actual_rel.loc[dt.date(2020, 1, 23)])
        assert actual_rel.dataset_ids == (Dataset.GS.CENTRAL_BANK_WATCH,)

        mock_get_data.return_value = mock_ois_spot()
        actual_spot = tm_rates.policy_rate_term_structure(
            mock_eur,
            tm_rates.EventType.SPOT,
            tm_rates.RateType.ABSOLUTE,
            dt.date(2019, 12, 6))
        assert (target['spot'] == actual_spot.loc[dt.date(2019, 12, 6)])
        assert actual_spot.dataset_ids == (Dataset.GS.CENTRAL_BANK_WATCH,)

        with pytest.raises(MqError):
            tm_rates.policy_rate_term_structure(mock_eur, 'meeting')

        with pytest.raises(MqError):
            tm_rates.policy_rate_term_structure(
                mock_eur, tm_rates.EventType.MEETING, 'normalized', '2019-09-01')

        with pytest.raises(MqError):
            tm_rates.policy_rate_term_structure(
                mock_eur,
                tm_rates.EventType.MEETING,
                tm_rates.RateType.ABSOLUTE,
                5)

        with pytest.raises(ValueError):
            tm_rates.policy_rate_term_structure(
                mock_eur,
                tm_rates.EventType.MEETING,
                tm_rates.RateType.ABSOLUTE,
                '01-09-2019')

        with pytest.raises(MqError):
            tm_rates.policy_rate_term_structure(
                mock_eur,
                tm_rates.EventType.SPOT,
                tm_rates.RateType.RELATIVE)

        with pytest.raises(NotImplementedError):
            tm_rates.policy_rate_term_structure(
                mock_eur,
                tm_rates.EventType.SPOT,
                tm_rates.RateType.ABSOLUTE,
                real_time=True)

        mock_get_data = replace('gs_quant.data.dataset.Dataset.get_data', Mock())
        mock_get_data.return_value = pd.DataFrame()

        assert_series_equal(
            tm_rates.policy_rate_term_structure(
                mock_eur,
                tm_rates.EventType.MEETING,
                tm_rates.RateType.ABSOLUTE),
            pd.Series(dtype=float, name='value'))

        mock_get_data = replace('gs_quant.timeseries.measures_rates.policy_rate_term_structure_rt', Mock())
        mock_get_data.return_value = pd.DataFrame()
        assert tm_rates.policy_rate_term_structure(
            mock_eur,
            tm_rates.EventType.MEETING,
            tm_rates.RateType.ABSOLUTE,
            "Intraday"
        ).empty

    replace.restore()


def test_policy_rate_expectation(mocker):
    target = {
        'meeting_number_absolute': -0.004550907771,
        'meeting_number_relative': -0.000028337246,
        'meeting_date_relative': -0.000028337246,
        'meeting_number_spot': -0.004522570525
    }
    mock_eur = Currency('MARFAGXDQRWM07Y2', 'EUR')

    with DataContext(dt.date(2019, 12, 6), dt.date(2019, 12, 6)):
        replace = Replacer()
        xrefs = replace('gs_quant.timeseries.measures.GsAssetApi.get_asset_xrefs', Mock())
        xrefs.return_value = [GsTemporalXRef(dt.date(2019, 1, 1), dt.date(2952, 12, 31), XRef(bbid='EUR', ))]
        mocker.patch.object(GsAssetApi, 'map_identifiers', side_effect=map_identifiers_default_mocker)

        mock_get_data = replace('gs_quant.data.dataset.Dataset.get_data', Mock())
        mock_get_data.return_value = mock_meeting_spot()

        actual_num = tm_rates.policy_rate_expectation(
            mock_eur,
            tm_rates.EventType.SPOT,
            tm_rates.RateType.ABSOLUTE,
            0)
        assert (target['meeting_number_spot'] == actual_num.loc[dt.date(2019, 12, 6)])
        assert actual_num.dataset_ids == (Dataset.GS.CENTRAL_BANK_WATCH,)

        mocker.patch.object(Dataset, 'get_data', side_effect=get_data_policy_rate_expectation_mocker)
        actual_num = tm_rates.policy_rate_expectation(
            mock_eur,
            tm_rates.EventType.MEETING,
            tm_rates.RateType.ABSOLUTE,
            2)
        assert (target['meeting_number_absolute'] == actual_num.loc[dt.date(2019, 12, 6)])
        assert actual_num.dataset_ids == (Dataset.GS.CENTRAL_BANK_WATCH,)

        actual_date = tm_rates.policy_rate_expectation(
            mock_eur,
            tm_rates.EventType.MEETING,
            tm_rates.RateType.ABSOLUTE,
            dt.date(2020, 1, 23))
        assert (target['meeting_number_absolute'] == actual_date.loc[dt.date(2019, 12, 6)])
        assert actual_date.dataset_ids == (Dataset.GS.CENTRAL_BANK_WATCH,)

        actual_num = tm_rates.policy_rate_expectation(
            mock_eur,
            tm_rates.EventType.MEETING,
            tm_rates.RateType.RELATIVE,
            2)
        assert_allclose([target['meeting_number_relative']], [actual_num.loc[dt.date(2019, 12, 6)]],
                        rtol=1e-9, atol=1e-15)
        assert actual_num.dataset_ids == (Dataset.GS.CENTRAL_BANK_WATCH,)

        actual_num = tm_rates.policy_rate_expectation(
            mock_eur,
            tm_rates.EventType.MEETING,
            tm_rates.RateType.ABSOLUTE,
            0)
        assert (target['meeting_number_spot'] == actual_num.loc[dt.date(2019, 12, 6)])
        assert actual_num.dataset_ids == (Dataset.GS.CENTRAL_BANK_WATCH,)

        actual_date = tm_rates.policy_rate_expectation(
            mock_eur,
            tm_rates.EventType.MEETING,
            tm_rates.RateType.ABSOLUTE,
            '2019-10-24')
        assert (target['meeting_number_spot'] == actual_date.loc[dt.date(2019, 12, 6)])
        assert actual_date.dataset_ids == (Dataset.GS.CENTRAL_BANK_WATCH,)

        mocker.patch.object(Dataset, 'get_data', side_effect=[mock_meeting_expectation(),
                                                              mock_empty_market_data_response()])
        with pytest.raises(MqError):
            tm_rates.policy_rate_expectation(
                mock_eur,
                tm_rates.EventType.MEETING,
                tm_rates.RateType.RELATIVE,
                2)

        with pytest.raises(MqError):
            tm_rates.policy_rate_expectation(
                mock_eur,
                tm_rates.EventType.MEETING,
                tm_rates.RateType.ABSOLUTE,
                5.5)

        with pytest.raises(MqError):
            tm_rates.policy_rate_expectation(mock_eur, 'meeting', tm_rates.RateType.ABSOLUTE, 5)

        with pytest.raises(MqError):
            tm_rates.policy_rate_expectation(
                mock_eur,
                tm_rates.EventType.MEETING,
                'normalized', dt.date(2019, 9, 1))

        with pytest.raises(MqError):
            tm_rates.policy_rate_expectation(
                mock_eur,
                tm_rates.EventType.MEETING,
                tm_rates.RateType.RELATIVE,
                -2)

        mock_get_data = replace('gs_quant.data.dataset.Dataset.get_data', Mock())
        mock_get_data.return_value = pd.DataFrame()
        with pytest.raises(MqError):
            tm_rates.policy_rate_expectation(
                mock_eur,
                tm_rates.EventType.MEETING,
                tm_rates.RateType.ABSOLUTE,
                2)

        mock_get_data = replace('gs_quant.timeseries.measures_rates.policy_rate_expectation_rt', Mock())
        mock_get_data.return_value = pd.DataFrame()
        assert tm_rates.policy_rate_expectation(
            mock_eur,
            tm_rates.EventType.MEETING,
            tm_rates.RateType.ABSOLUTE,
            2,
            real_time=True
        ).empty

    replace.restore()


def mock_policy_rt_spot():
    data_dict = MarketDataResponseFrame(
        {
            'assetId': ['MAV2B3A3D0R369QE'],
            'pricingLocation': ['LDN'],
            'csaTerms': ['EUR-EuroSTR'],
            'rate': [-0.0049],
            'effectiveDate': [dt.date(2022, 3, 23)],
            'terminationDate': [dt.date(2022, 4, 20)],
            'annuity': [-778.1652098],
            'updateTime': [dt.datetime(2022, 4, 14, 0, 0, 0)],
            'currency': ['EUR'],
        },
        index=pd.Index([dt.datetime(2022, 4, 14, 0, 0, 0)], name='time'))
    data_dict.dataset_ids = _test_datasets
    return data_dict


def mock_policy_rate_expectation_rt_meeting():
    data_dict = MarketDataResponseFrame(
        {
            'assetId': ['MA9PXTY5DC1JHV5Y'],
            'pricingLocation': ['LDN'],
            'csaTerms': ['EUR-EuroSTR'],
            'rate': [-0.005337848],
            'effectiveDate': [dt.date(2022, 7, 27)],
            'terminationDate': [dt.date(2022, 9, 14)],
            'annuity': [-1169.016923],
            'updateTime': [dt.datetime(2022, 4, 14, 0, 0, 0)],
            'currency': ['EUR'],
        },
        index=pd.Index([dt.datetime(2022, 4, 14, 0, 0, 0)], name='time'))
    data_dict.dataset_ids = _test_datasets
    return data_dict


def mock_policy_term_rt_meeting():
    data_dict = MarketDataResponseFrame(
        {
            'assetId': ['MANRCY4GA0WWT1QC', 'MA9PXTY5DC1JHV5Y'],
            'pricingLocation': ['LDN', 'LDN'],
            'csaTerms': ['EUR-EuroSTR', 'EUR-EuroSTR'],
            'rate': [-0.004585702, -0.005337848],
            'effectiveDate': [dt.date(2022, 6, 15), dt.date(2022, 7, 27)],
            'terminationDate': [dt.date(2022, 7, 27), dt.date(2022, 9, 14)],
            'annuity': [-1364.124069, -1169.016923],
            'updateTime': [dt.datetime(2022, 4, 14, 0, 0, 0),
                           dt.datetime(2022, 4, 14, 0, 0, 0)],
            'currency': ['EUR', 'EUR'],
        },
        index=pd.Index([dt.datetime(2022, 4, 14, 0, 0, 0),
                        dt.datetime(2022, 4, 14, 0, 0, 0)], name='time'))
    data_dict.dataset_ids = _test_datasets
    return data_dict


def mock_policy_term_rt_meeting_series():
    data_dict = MarketDataResponseFrame(
        {
            'assetId': ['MA9PXTY5DC1JHV5Y'],
            'pricingLocation': ['LDN'],
            'csaTerms': ['EUR-EuroSTR'],
            'rate': [-0.005337848],
            'effectiveDate': [dt.date(2022, 7, 27)],
            'terminationDate': [dt.date(2022, 9, 14)],
            'annuity': [-1169.016923],
            'updateTime': [dt.datetime(2022, 4, 14, 0, 0, 0)],
            'currency': ['EUR'],
        },
        index=pd.Index([dt.datetime(2022, 4, 14, 0, 0, 0),
                        dt.datetime(2022, 4, 14, 0, 0, 0)], name='time'))
    data_dict.dataset_ids = _test_datasets
    return data_dict


def mock_policy_rate_empty_join_df():
    data_dict = MarketDataResponseFrame(
        {
            'assetId': ['MA000', 'MA000'],
            'pricingLocation': ['USD', 'USD'],
            'csaTerms': ['USD-SOFR-1', 'USD-SOFR-1'],
            'rate': [-0.004585702, -0.005337848],
            'effectiveDate': [dt.date(2022, 6, 15), dt.date(2022, 7, 27)],
            'terminationDate': [dt.date(2022, 7, 27), dt.date(2022, 9, 14)],
            'annuity': [-1364.124069, -1169.016923],
            'updateTime': [dt.datetime(2022, 4, 14, 0, 0, 0),
                           dt.datetime(2022, 4, 14, 0, 0, 0)],
            'currency': ['EUR', 'EUR'],
        },
        index=pd.Index([dt.datetime(2022, 4, 14, 0, 0, 0),
                        dt.datetime(2022, 4, 14, 0, 0, 0)], name='time'))
    data_dict.dataset_ids = _test_datasets
    return data_dict


def get_data_policy_rate_term_rt_series_mocker(**kwargs) -> pd.DataFrame:
    if len(kwargs['assetId']) == 1:
        return mock_policy_rt_spot()
    else:
        return mock_policy_term_rt_meeting_series()


def get_data_policy_rate_term_rt_mocker(**kwargs) -> pd.DataFrame:
    if len(kwargs['assetId']) == 1:
        return mock_policy_rt_spot()
    else:
        return mock_policy_term_rt_meeting()


def get_data_empty_spot_mocker(**kwargs) -> pd.DataFrame:
    if len(kwargs['assetId']) == 1:
        return pd.DataFrame()
    else:
        return mock_policy_term_rt_meeting()


def get_data_empty_join_mocker(**kwargs) -> pd.DataFrame:
    if len(kwargs['assetId']) == 1:
        return mock_policy_rate_empty_join_df()
    else:
        return mock_policy_term_rt_meeting()


def get_cb_swap_assets_mocker(allow_many=True, **kwargs) -> list:
    if isinstance(kwargs['asset_parameters_termination_date'], str) and isinstance(
            kwargs['asset_parameters_effective_date'], str):
        return ['MAV2B3A3D0R369QE']
    else:
        return ['MANRCY4GA0WWT1QC', 'MA9PXTY5DC1JHV5Y', 'MAACR86DGE1CMK9Y',
                'MASSRBDHKSSDAS36', 'MAZAH4WR524BQ7ZN', 'MAY2RN50CWETF7HV', 'MAV2B3A3D0R369QE']


def test_policy_rate_term_structure_rt(mocker):
    target = {
        'meeting_absolute': -0.005337848,
        'meeting_relative': -0.00043784800000000023,
        'spot': -0.0049
    }
    mock_eur = Currency('MARFAGXDQRWM07Y2', 'EUR')
    mock_zar = Currency("MA1", "ZAR")
    with DataContext(dt.date(2020, 2, 14), dt.date(2020, 3, 14)):
        replace = Replacer()
        xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
        xrefs.return_value = 'ZAR'
        cbd = replace('gs_quant.timeseries.measures._get_custom_bd', Mock())
        cbd.return_value = pd.tseries.offsets.BusinessDay()
        replace('gs_quant.timeseries.measures_rates._get_tdapi_rates_assets', get_cb_swap_assets_mocker)
        mocker.patch.object(Dataset, 'get_data', side_effect=get_data_policy_rate_term_rt_mocker)
        with pytest.raises(MqValueError):
            tm_rates.policy_rate_term_structure_rt(
                mock_eur,
                tm_rates.EventType.MEETING,
                tm_rates.RateType.RELATIVE,
                None)
        replace.restore()

    with DataContext(dt.date(2021, 4, 14), dt.date(2024, 4, 14)):
        replace = Replacer()
        xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
        xrefs.return_value = 'ZAR'
        cbd = replace('gs_quant.timeseries.measures._get_custom_bd', Mock())
        cbd.return_value = pd.tseries.offsets.BusinessDay()
        replace('gs_quant.timeseries.measures_rates._get_tdapi_rates_assets', get_cb_swap_assets_mocker)

        with pytest.raises(MqError):
            tm_rates.policy_rate_term_structure_rt(mock_zar, tm_rates.EventType.MEETING, tm_rates.RateType.ABSOLUTE, )

        xrefs.return_value = 'EUR'
        with pytest.raises(MqError):
            tm_rates.policy_rate_term_structure_rt(mock_eur, tm_rates.EventType.MEETING, tm_rates.RateType.ABSOLUTE,
                                                   tm_rates.BenchmarkTypeCB.SOFR)
        with pytest.raises(MqError):
            tm_rates.policy_rate_term_structure_rt(mock_eur, tm_rates.EventType.EOY, tm_rates.RateType.ABSOLUTE)

        with pytest.raises(MqError):
            tm_rates.policy_rate_term_structure_rt(mock_eur, tm_rates.EventType.SPOT, tm_rates.RateType.RELATIVE)

        mock_get_data = replace('gs_quant.data.dataset.Dataset.get_data', Mock())
        mock_get_data.return_value = mock_policy_term_rt_meeting()

        actual_abs = tm_rates.policy_rate_term_structure_rt(
            mock_eur,
            tm_rates.EventType.MEETING,
            tm_rates.RateType.ABSOLUTE,
            None)
        assert (target['meeting_absolute'] == actual_abs.loc[dt.date(2022, 7, 27)])

        mocker.patch.object(Dataset, 'get_data', side_effect=get_data_policy_rate_term_rt_mocker)
        actual_rel = tm_rates.policy_rate_term_structure_rt(
            mock_eur,
            tm_rates.EventType.MEETING,
            tm_rates.RateType.RELATIVE,
            None)
        assert (target['meeting_relative'] == actual_rel.loc[dt.date(2022, 7, 27)])

        mock_get_data.return_value = mock_policy_rt_spot()
        actual_spot = tm_rates.policy_rate_term_structure_rt(
            mock_eur,
            tm_rates.EventType.SPOT,
            tm_rates.RateType.ABSOLUTE,
            None)
        assert (target['spot'] == actual_spot.loc[dt.datetime(2022, 4, 14).isoformat()])

        mocker.patch.object(Dataset, 'get_data', side_effect=get_data_empty_join_mocker)
        assert tm_rates.policy_rate_term_structure_rt(mock_eur, tm_rates.EventType.MEETING,
                                                      tm_rates.RateType.RELATIVE).empty

        mocker.patch.object(Dataset, 'get_data', side_effect=get_data_empty_spot_mocker)
        with pytest.raises(MqError):
            tm_rates.policy_rate_term_structure_rt(mock_eur, tm_rates.EventType.MEETING, tm_rates.RateType.RELATIVE)

        mock_get_data = replace('gs_quant.data.dataset.Dataset.get_data', Mock())
        mock_get_data.return_value = pd.DataFrame()

        with pytest.raises(MqError):
            tm_rates.policy_rate_term_structure_rt(mock_eur, tm_rates.EventType.SPOT, tm_rates.RateType.ABSOLUTE)
        with pytest.raises(MqError):
            tm_rates.policy_rate_term_structure_rt(mock_eur, tm_rates.EventType.MEETING, tm_rates.RateType.RELATIVE)

    replace.restore()


def get_data_policy_rate_exp_rt_mocker(**kwargs) -> pd.DataFrame:
    if kwargs['assetId'] == 'MA000SPOT':
        return mock_policy_rt_spot()
    else:
        return mock_policy_rate_expectation_rt_meeting()


def policy_exp_empty_spot_mocker(**kwargs) -> pd.DataFrame:
    if kwargs['assetId'] == 'MA000SPOT':
        return pd.DataFrame()
    else:
        return mock_policy_rate_expectation_rt_meeting()


def test_get_swap_from_meeting_date(mocker):
    eur = CurrencyEnum.EUR
    benchmark = tm_rates.BenchmarkTypeCB.EUROSTR

    with pytest.raises(MqValueError):
        tm_rates._get_swap_from_meeting_date(eur, benchmark, 'ecb30')
    with pytest.raises(MqValueError):
        tm_rates._get_swap_from_meeting_date(eur, benchmark, 'frb1')

    replace = Replacer()
    cbd = replace('gs_quant.timeseries.measures_rates.get_cb_meeting_swap', Mock())
    cbd.return_value = 'MA123'

    assert 'MA123' == tm_rates._get_swap_from_meeting_date(eur, benchmark, 0)
    assert 'MA123' == tm_rates._get_swap_from_meeting_date(eur, benchmark, 1)
    assert 'MA123' == tm_rates._get_swap_from_meeting_date(eur, benchmark, 'ecb0')
    assert 'MA123' == tm_rates._get_swap_from_meeting_date(eur, benchmark, 'ecb1')
    replace.restore()


def test_policy_rate_expectation_rt(mocker):
    target = {
        'meeting_absolute': -0.005337848,
        'meeting_relative': -0.00043784800000000023,
        'spot': -0.0049
    }
    mock_eur = Currency('MARFAGXDQRWM07Y2', 'EUR')
    mock_zar = Currency("MA1", "ZAR")
    with DataContext(dt.date(2020, 2, 14), dt.date(2020, 3, 14)):
        replace = Replacer()
        xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
        xrefs.return_value = 'ZAR'
        cbd = replace('gs_quant.timeseries.measures._get_custom_bd', Mock())
        cbd.return_value = pd.tseries.offsets.BusinessDay()
        mock_swap = replace('gs_quant.timeseries.measures_rates._get_tdapi_rates_assets', Mock())
        mock_swap.return_value = 'MA000SPOT'

        mock_swap = replace('gs_quant.timeseries.measures_rates._get_swap_from_meeting_date', Mock())
        mock_swap.return_value = 'MAV2B3A3D0R369QE'
        with pytest.raises(MqError):
            tm_rates.policy_rate_expectation_rt(
                mock_eur,
                tm_rates.EventType.SPOT,
                tm_rates.RateType.ABSOLUTE)
        replace.restore()

    with DataContext(dt.date(2021, 4, 14), dt.date(2024, 4, 14)):
        replace = Replacer()
        xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
        xrefs.return_value = 'ZAR'
        cbd = replace('gs_quant.timeseries.measures._get_custom_bd', Mock())
        cbd.return_value = pd.tseries.offsets.BusinessDay()
        mock_swap = replace('gs_quant.timeseries.measures_rates._get_tdapi_rates_assets', Mock())
        mock_swap.return_value = 'MA000SPOT'

        mock_swap = replace('gs_quant.timeseries.measures_rates._get_swap_from_meeting_date', Mock())
        mock_swap.return_value = 'MAV2B3A3D0R369QE'

        with pytest.raises(MqError):
            tm_rates.policy_rate_expectation_rt(mock_zar, tm_rates.EventType.MEETING, tm_rates.RateType.ABSOLUTE, )

        xrefs.return_value = 'EUR'
        mocker.patch.object(Dataset, 'get_data', side_effect=policy_exp_empty_spot_mocker)
        with pytest.raises(MqError):
            tm_rates.policy_rate_expectation_rt(mock_eur, tm_rates.EventType.MEETING, tm_rates.RateType.RELATIVE)

        mocker.patch.object(Dataset, 'get_data', side_effect=get_data_policy_rate_exp_rt_mocker)

        with pytest.raises(MqError):
            tm_rates.policy_rate_expectation_rt(mock_eur, tm_rates.EventType.EOY, tm_rates.RateType.ABSOLUTE)

        actual_abs = tm_rates.policy_rate_expectation_rt(
            mock_eur,
            tm_rates.EventType.MEETING,
            tm_rates.RateType.ABSOLUTE,
            2)
        assert (target['meeting_absolute'] == actual_abs.loc[dt.datetime(2022, 4, 14)])

        actual_rel = tm_rates.policy_rate_expectation_rt(
            mock_eur,
            tm_rates.EventType.MEETING,
            tm_rates.RateType.RELATIVE,
            2)
        assert (target['meeting_relative'] == actual_rel.loc[dt.datetime(2022, 4, 14)])

        mock_swap.return_value = 'MA000SPOT'
        actual_spot = tm_rates.policy_rate_expectation_rt(
            mock_eur,
            tm_rates.EventType.SPOT,
            tm_rates.RateType.ABSOLUTE)
        assert (target['spot'] == actual_spot.loc[dt.datetime(2022, 4, 14).isoformat()])

        with pytest.raises(MqError):
            tm_rates.policy_rate_expectation_rt(mock_eur, tm_rates.EventType.SPOT, tm_rates.RateType.RELATIVE)

        mock_get_data = replace('gs_quant.data.dataset.Dataset.get_data', Mock())
        mock_get_data.return_value = pd.DataFrame()

        with pytest.raises(MqError):
            tm_rates.policy_rate_expectation_rt(mock_eur, tm_rates.EventType.SPOT, tm_rates.RateType.ABSOLUTE)
        with pytest.raises(MqError):
            tm_rates.policy_rate_expectation_rt(mock_eur, tm_rates.EventType.MEETING, tm_rates.RateType.RELATIVE)

        with pytest.raises(MqError):
            tm_rates.policy_rate_expectation_rt(mock_eur, tm_rates.EventType.SPOT, tm_rates.RateType.RELATIVE)

        mock_get_data = replace('gs_quant.data.dataset.Dataset.get_data', Mock())
        mock_get_data.return_value = pd.Series(dtype=float)
        with pytest.raises(MqError):
            tm_rates.policy_rate_expectation_rt(mock_eur, tm_rates.EventType.MEETING, tm_rates.RateType.RELATIVE)

    replace.restore()


def test_get_cb_meeting_swap(mocker):
    replace = Replacer()
    mock_swap = replace('gs_quant.timeseries.measures_rates._get_tdapi_rates_assets', Mock())
    mock_swap.return_value = 'MA000SPOT'

    with pytest.raises(MqValueError):
        tm_rates.get_cb_meeting_swap(CurrencyEnum.USD, tm_rates.BenchmarkTypeCB.SOFR, '1y', '125y')

    assert tm_rates.get_cb_meeting_swap(CurrencyEnum.USD, tm_rates.BenchmarkTypeCB.SOFR, '0b', '1y') == 'MA000SPOT'
    replace.restore()


if __name__ == '__main__':
    pytest.main(args=["test_measures_rates.py"])
