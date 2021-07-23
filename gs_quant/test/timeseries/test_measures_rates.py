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
from pandas._testing import assert_series_equal
from testfixtures import Replacer
from testfixtures.mock import Mock

import gs_quant.timeseries.measures as tm
import gs_quant.timeseries.measures_rates as tm_rates
from gs_quant.api.gs.data import MarketDataResponseFrame, QueryType
from gs_quant.target.common import PricingLocation
from gs_quant.data.core import DataContext
from gs_quant.errors import MqValueError
from gs_quant.session import GsSession, Environment
from gs_quant.test.timeseries.utils import mock_request
from gs_quant.timeseries import TdapiRatesDefaultsProvider, SWAPTION_DEFAULTS, Currency, CurrencyEnum, SecurityMaster, \
    ExtendedSeries
from gs_quant.timeseries.measures_rates import _swaption_build_asset_query, _currency_to_tdapi_swaption_rate_asset, \
    _check_strike_reference, _pricing_location_normalized, _default_pricing_location
from gs_quant.markets.securities import Cross

_index = [pd.Timestamp('2019-01-01')]
_test_datasets = ('TEST_DATASET',)


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
    df = ExtendedSeries()
    replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock()).return_value = "GBP"
    replace('gs_quant.timeseries.measures_rates._get_tdapi_rates_assets', Mock(), Mock()).return_value = [
        "MADWG3WHCKNE1DJA", "MAH6JK3TZJJGFQ65"]
    replace('gs_quant.timeseries.measures_rates._range_from_pricing_date', Mock(), Mock()).return_value = [
        dt.date(2020, 1, 2), dt.date(2020, 1, 2)]
    replace('gs_quant.timeseries.measures_rates._market_data_timed', Mock()).return_value = df

    with DataContext('2019-01-01', '2025-01-01'):
        actual = tm_rates.swaption_vol_term(Currency("GBP", name="GBP"), tm.SwaptionTenorType.SWAP_MATURITY, '5y', 0)

    assert_series_equal(ExtendedSeries(), actual, check_names=False)
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
    df = ExtendedSeries()
    replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock()).return_value = "GBP"
    replace('gs_quant.timeseries.measures_rates._get_tdapi_rates_assets', Mock(), Mock()).return_value = [
        "MADWG3WHCKNE1DJA", "MAH6JK3TZJJGFQ65"]
    replace('gs_quant.timeseries.measures_rates._range_from_pricing_date', Mock(), Mock()).return_value = [
        dt.date(2020, 1, 2), dt.date(2020, 1, 2)]
    replace('gs_quant.timeseries.measures_rates._market_data_timed', Mock()).return_value = df

    with DataContext('2019-01-01', '2025-01-01'):
        actual = tm_rates.swaption_vol_smile(Currency("GBP", name="GBP"), '3m', '10y')
    assert_series_equal(ExtendedSeries(), actual)
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
    df = ExtendedSeries()

    replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock()).return_value = "GBP"
    replace('gs_quant.timeseries.measures_rates._get_tdapi_rates_assets', Mock(), Mock()).return_value = [
        "MADWG3WHCKNE1DJA", "MAH6JK3TZJJGFQ65"]
    replace('gs_quant.timeseries.measures_rates._range_from_pricing_date', Mock(), Mock()).return_value = [
        dt.date(2019, 1, 2), dt.date(2019, 1, 5)]
    replace('gs_quant.timeseries.measures_rates._market_data_timed', Mock()).return_value = df

    actual = tm_rates.swaption_vol(Currency("GBP", name="GBP"))
    assert_series_equal(ExtendedSeries(), actual)
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
    with pytest.raises(NotImplementedError):
        tm_rates.swaption_premium(Currency("KRW", name="KRW"))


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


if __name__ == '__main__':
    pytest.main(args=["test_measures_rates.py"])
