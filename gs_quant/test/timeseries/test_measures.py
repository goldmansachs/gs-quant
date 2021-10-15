"""
Copyright 2019 Goldman Sachs.
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
import os
from typing import Union

import numpy as np
import pandas as pd
import pytest
import pytz
from numpy.testing import assert_allclose, assert_equal
from pandas.testing import assert_series_equal
from pandas.tseries.offsets import CustomBusinessDay
from pytz import timezone
from testfixtures import Replacer
from testfixtures.mock import Mock

import gs_quant.timeseries.measures as tm
import gs_quant.timeseries.measures_rates as tm_rates
from gs_quant.api.gs.assets import GsTemporalXRef, GsAssetApi, GsIdType, IdList, GsAsset
from gs_quant.api.gs.data import GsDataApi, MarketDataResponseFrame
from gs_quant.api.gs.data import QueryType
from gs_quant.data.core import DataContext
from gs_quant.data.dataset import Dataset
from gs_quant.data.fields import Fields
from gs_quant.errors import MqError, MqValueError, MqTypeError
from gs_quant.markets.baskets import Basket as CustomBasket
from gs_quant.markets.index import Index
from gs_quant.markets.securities import AssetClass, Cross, Currency, SecurityMaster, Stock, \
    Swap, CommodityNaturalGasHub, CommodityEUNaturalGasHub, AssetIdentifier, CommodityPowerAggregatedNodes, \
    FutureMarket, DefaultSwap
from gs_quant.session import GsSession, Environment, OAuth2Session
from gs_quant.target.common import XRef, PricingLocation, Currency as CurrEnum
from gs_quant.test.timeseries.utils import mock_request
from gs_quant.timeseries import Returns, ExtendedSeries
from gs_quant.timeseries.measures import BenchmarkType

_index = [pd.Timestamp('2019-01-01')]
_index2 = [pd.Timestamp('2019-08-02')]
_test_datasets = ('TEST_DATASET',)
_test_datasets2 = ('TEST_DATASET2',)
_test_datasets_rt = ('TEST_DATASET_RT',)


def mock_empty_market_data_response():
    df = MarketDataResponseFrame()
    df.dataset_ids = ()
    return df


def map_identifiers_default_mocker(input_type: Union[GsIdType, str],
                                   output_type: Union[GsIdType, str],
                                   ids: IdList,
                                   as_of: dt.datetime = None,
                                   multimap: bool = False,
                                   limit: int = None,
                                   **kwargs
                                   ) -> dict:
    if "USD-LIBOR-BBA" in ids:
        return {"USD-LIBOR-BBA": "MAPDB7QNB2TZVQ0E"}
    elif "EUR-EURIBOR-TELERATE" in ids:
        return {"EUR-EURIBOR-TELERATE": "MAJNQPFGN1EBDHAE"}
    elif "GBP-LIBOR-BBA" in ids:
        return {"GBP-LIBOR-BBA": "MAFYB8Z4R1377A19"}
    elif "JPY-LIBOR-BBA" in ids:
        return {"JPY-LIBOR-BBA": "MABMVE27EM8YZK33"}
    elif "EUR OIS" in ids:
        return {"EUR OIS": "MARFAGXDQRWM07Y2"}


def map_identifiers_ois_mocker(input_type: Union[GsIdType, str],
                               output_type: Union[GsIdType, str],
                               ids: IdList,
                               as_of: dt.datetime = None,
                               multimap: bool = False,
                               limit: int = None,
                               **kwargs
                               ) -> dict:
    if "USD OIS" in ids:
        return {"USD OIS": "MA29GN9VZE0WK56V"}
    elif "EUR OIS" in ids:
        return {"EUR OIS": "MARFAGXDQRWM07Y2"}
    elif "SEK OIS" in ids:
        return {"SEK OIS": "MARSF2Y8GV5GHXYZ"}
    elif "AUD OIS" in ids:
        return {"AUD OIS": "MA2XT17D0P77A84G"}
    elif "JPY OIS" in ids:
        return {"JPY OIS": "MAY3XC3279QN7SHW"}
    elif "GBP OIS" in ids:
        return {"GBP OIS": "MAGP76C36BX2Q0YA"}
    elif "NOK OIS" in ids:
        return {"NOK OIS": "MAS7EYBPYZ4SQ4GG"}
    elif "CAD OIS" in ids:
        return {"CAD OIS": "MAX229TKVEZMZ4WT"}
    elif "NZD OIS" in ids:
        return {"NZD OIS": "MA48BHGWY71R4SAJ"}
    elif "CHF OIS" in ids:
        return {"CHF OIS": "MAK0CRRF9DPMECSJ"}


def map_identifiers_swap_rate_mocker(input_type: Union[GsIdType, str],
                                     output_type: Union[GsIdType, str],
                                     ids: IdList,
                                     as_of: dt.datetime = None,
                                     multimap: bool = False,
                                     limit: int = None,
                                     **kwargs
                                     ) -> dict:
    if "USD-3m" in ids:
        return {"USD-3m": "MAAXGV0GZTW4GFNC"}
    elif "EUR-6m" in ids:
        return {"EUR-6m": "MA5WM2QWRVMYKDK0"}
    elif "KRW" in ids:
        return {"KRW": 'MAJ6SEQH3GT0GA2Z'}


def map_identifiers_inflation_mocker(input_type: Union[GsIdType, str],
                                     output_type: Union[GsIdType, str],
                                     ids: IdList,
                                     as_of: dt.datetime = None,
                                     multimap: bool = False,
                                     limit: int = None,
                                     **kwargs
                                     ) -> dict:
    if "CPI-UKRPI" in ids:
        return {"CPI-UKRPI": "MAQ7ND0MBP2AVVQW"}
    elif "CPI-CPXTEMU" in ids:
        return {"CPI-CPXTEMU": "MAK1FHKH5P5GJSHH"}


def map_identifiers_cross_basis_mocker(input_type: Union[GsIdType, str],
                                       output_type: Union[GsIdType, str],
                                       ids: IdList,
                                       as_of: dt.datetime = None,
                                       multimap: bool = False,
                                       limit: int = None,
                                       **kwargs
                                       ) -> dict:
    if "USD-3m/JPY-3m" in ids:
        return {"USD-3m/JPY-3m": "MA99N6C1KF9078NM"}
    elif "EUR-3m/USD-3m" in ids:
        return {"EUR-3m/USD-3m": "MAXPKTXW2D4X6MFQ"}
    elif "GBP-3m/USD-3m" in ids:
        return {"GBP-3m/USD-3m": "MA8BZHQV3W32V63B"}


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


def test_parse_meeting_date():
    assert tm.parse_meeting_date(5) == ''
    assert tm.parse_meeting_date('') == ''
    assert tm.parse_meeting_date('test') == ''
    assert tm.parse_meeting_date('2019-09-01') == dt.date(2019, 9, 1)


def test_currency_to_default_ois_asset(mocker):
    mocker.patch.object(GsSession.__class__, 'default_value',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_get', side_effect=mock_request)
    mocker.patch.object(GsAssetApi, 'map_identifiers', side_effect=map_identifiers_ois_mocker)

    asset_id_list = ["MAJNQPFGN1EBDHAE"]
    correct_mapping = ["MARFAGXDQRWM07Y2"]
    with tm.PricingContext(dt.date.today()):
        for i in range(len(asset_id_list)):
            correct_id = tm.currency_to_default_ois_asset(asset_id_list[i])
            assert correct_id == correct_mapping[i]

        # Test that the same id is returned when a TypeError is raised
        mocker.patch.object(GsAssetApi, 'map_identifiers', side_effect=TypeError('Test'))
        assert tm.currency_to_default_ois_asset('MAJNQPFGN1EBDHAE') == 'MAJNQPFGN1EBDHAE'


def test_currency_to_default_benchmark_rate(mocker):
    mocker.patch.object(GsSession.__class__, 'default_value',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_get', side_effect=mock_request)
    mocker.patch.object(GsAssetApi, 'map_identifiers', side_effect=map_identifiers_default_mocker)

    asset_id_list = ["MAZ7RWC904JYHYPS", "MAJNQPFGN1EBDHAE", "MA66CZBQJST05XKG", "MAK1FHKH5P5GJSHH", "MA4J1YB8XZP2BPT8",
                     "MA4B66MW5E27U8P32SB"]
    correct_mapping = ["MAPDB7QNB2TZVQ0E", "MAJNQPFGN1EBDHAE", "MAFYB8Z4R1377A19", "MABMVE27EM8YZK33",
                       "MA4J1YB8XZP2BPT8", "MA4B66MW5E27U8P32SB"]
    with tm.PricingContext(dt.date.today()):
        for i in range(len(asset_id_list)):
            correct_id = tm.currency_to_default_benchmark_rate(asset_id_list[i])
            assert correct_id == correct_mapping[i]


def test_currency_to_default_swap_rate_asset(mocker):
    mocker.patch.object(GsSession.__class__, 'default_value',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_get', side_effect=mock_request)
    mocker.patch.object(GsAssetApi, 'map_identifiers', side_effect=map_identifiers_swap_rate_mocker)

    asset_id_list = ['MAZ7RWC904JYHYPS', 'MAJNQPFGN1EBDHAE', 'MAJ6SEQH3GT0GA2Z']
    correct_mapping = ['MAAXGV0GZTW4GFNC', 'MA5WM2QWRVMYKDK0', 'MAJ6SEQH3GT0GA2Z']
    with tm.PricingContext(dt.date.today()):
        for i in range(len(asset_id_list)):
            correct_id = tm.currency_to_default_swap_rate_asset(asset_id_list[i])
            assert correct_id == correct_mapping[i]


def test_currency_to_inflation_benchmark_rate(mocker):
    mocker.patch.object(GsSession.__class__, 'default_value',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_get', side_effect=mock_request)
    mocker.patch.object(GsAssetApi, 'map_identifiers', side_effect=map_identifiers_inflation_mocker)

    asset_id_list = ["MA66CZBQJST05XKG", "MAK1FHKH5P5GJSHH", "MA4J1YB8XZP2BPT8"]
    correct_mapping = ["MAQ7ND0MBP2AVVQW", "MAK1FHKH5P5GJSHH", "MA4J1YB8XZP2BPT8"]
    with tm.PricingContext(dt.date.today()):
        for i in range(len(asset_id_list)):
            correct_id = tm.currency_to_inflation_benchmark_rate(asset_id_list[i])
            assert correct_id == correct_mapping[i]

        # Test that the same id is returned when a TypeError is raised
        mocker.patch.object(GsAssetApi, 'map_identifiers', side_effect=TypeError('Test'))
        assert tm.currency_to_inflation_benchmark_rate('MA66CZBQJST05XKG') == 'MA66CZBQJST05XKG'


def test_cross_to_basis(mocker):
    mocker.patch.object(GsSession.__class__, 'default_value',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_get', side_effect=mock_request)
    mocker.patch.object(GsAssetApi, 'map_identifiers', side_effect=map_identifiers_cross_basis_mocker)

    asset_id_list = ["MAYJPCVVF2RWXCES", "MA4B66MW5E27U8P32SB", "nobbid"]
    correct_mapping = ["MA99N6C1KF9078NM", "MA4B66MW5E27U8P32SB", "nobbid"]
    with tm.PricingContext(dt.date.today()):
        for i in range(len(asset_id_list)):
            correct_id = tm.cross_to_basis(asset_id_list[i])
            assert correct_id == correct_mapping[i]

        # Test that the same id is returned when a TypeError is raised
        mocker.patch.object(GsAssetApi, 'map_identifiers', side_effect=TypeError('Test'))
        assert tm.cross_to_basis('MAYJPCVVF2RWXCES') == 'MAYJPCVVF2RWXCES'


def test_currency_to_tdapi_swap_rate_asset(mocker):
    replace = Replacer()
    mocker.patch.object(GsSession.__class__, 'current',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_get', side_effect=mock_request)
    mocker.patch.object(SecurityMaster, 'get_asset', side_effect=mock_request)
    bbid_mock = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    with tm.PricingContext(dt.date.today()):
        asset = Currency('MA25DW5ZGC1BSC8Y', 'NOK')
        bbid_mock.return_value = 'NOK'
        correct_id = tm_rates._currency_to_tdapi_swap_rate_asset(asset)
        asset = Currency('MAZ7RWC904JYHYPS', 'USD')
        bbid_mock.return_value = 'USD'
        correct_id = tm_rates._currency_to_tdapi_swap_rate_asset(asset)
        assert 'MAFRSWPAF5QPNTP2' == correct_id
        bbid_mock.return_value = 'CHF'
        correct_id = tm_rates._currency_to_tdapi_swap_rate_asset(asset)
        assert 'MAW25BGQJH9P6DPT' == correct_id
        bbid_mock.return_value = 'EUR'
        correct_id = tm_rates._currency_to_tdapi_swap_rate_asset(asset)
        assert 'MAA9MVX15AJNQCVG' == correct_id
        bbid_mock.return_value = 'GBP'
        correct_id = tm_rates._currency_to_tdapi_swap_rate_asset(asset)
        assert 'MA6QCAP9B7ABS9HA' == correct_id
        bbid_mock.return_value = 'JPY'
        correct_id = tm_rates._currency_to_tdapi_swap_rate_asset(asset)
        assert 'MAEE219J5ZP0ZKRK' == correct_id
        bbid_mock.return_value = 'SEK'
        correct_id = tm_rates._currency_to_tdapi_swap_rate_asset(asset)
        assert 'MAETMVTPNP3199A5' == correct_id

        bbid_mock.return_value = 'HKD'
        correct_id = tm_rates._currency_to_tdapi_swap_rate_asset(asset)
        assert 'MABRNGY8XRFVC36N' == correct_id
        bbid_mock.return_value = 'NZD'
        correct_id = tm_rates._currency_to_tdapi_swap_rate_asset(asset)
        assert 'MAH16NHE1HBN0FBZ' == correct_id
        bbid_mock.return_value = 'AUD'
        correct_id = tm_rates._currency_to_tdapi_swap_rate_asset(asset)
        assert 'MAY8147CRK0ZP53B' == correct_id
        bbid_mock.return_value = 'CAD'
        correct_id = tm_rates._currency_to_tdapi_swap_rate_asset(asset)
        assert 'MANJ8SS88WJ6N28Q' == correct_id
        bbid_mock.return_value = 'KRW'
        correct_id = tm_rates._currency_to_tdapi_swap_rate_asset(asset)
        assert 'MAP55AXG5SQVS6C5' == correct_id

        bbid_mock.return_value = 'INR'
        correct_id = tm_rates._currency_to_tdapi_swap_rate_asset(asset)
        assert 'MA20JHJXN1PD5HGE' == correct_id

        bbid_mock.return_value = 'CNY'
        correct_id = tm_rates._currency_to_tdapi_swap_rate_asset(asset)
        assert 'MA4K1D8HH2R0RQY5' == correct_id

        bbid_mock.return_value = 'SGD'
        correct_id = tm_rates._currency_to_tdapi_swap_rate_asset(asset)
        assert 'MA5CQFHYBPH9E5BS' == correct_id

        bbid_mock.return_value = 'DKK'
        correct_id = tm_rates._currency_to_tdapi_swap_rate_asset(asset)
        assert 'MAF131NKWVRESFYA' == correct_id

        asset = Currency('MA890', 'PLN')
        bbid_mock.return_value = 'PLN'
        assert 'MA890' == tm_rates._currency_to_tdapi_swap_rate_asset(asset)
    replace.restore()


def test_currency_to_tdapi_basis_swap_rate_asset(mocker):
    replace = Replacer()
    mocker.patch.object(GsSession.__class__, 'current',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_get', side_effect=mock_request)
    mocker.patch.object(SecurityMaster, 'get_asset', side_effect=mock_request)
    bbid_mock = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    with tm.PricingContext(dt.date.today()):
        asset = Currency('MA890', 'EGP')
        bbid_mock.return_value = 'EGP'
        assert 'MA890' == tm_rates._currency_to_tdapi_basis_swap_rate_asset(asset)
        asset = Currency('MAZ7RWC904JYHYPS', 'USD')
        bbid_mock.return_value = 'USD'
        correct_id = tm_rates._currency_to_tdapi_basis_swap_rate_asset(asset)
        assert 'MAQB1PGEJFCET3GG' == correct_id
        bbid_mock.return_value = 'EUR'
        correct_id = tm_rates._currency_to_tdapi_basis_swap_rate_asset(asset)
        assert 'MAGRG2VT11GQ2RQ9' == correct_id
        bbid_mock.return_value = 'GBP'
        correct_id = tm_rates._currency_to_tdapi_basis_swap_rate_asset(asset)
        assert 'MAHCYNB3V75JC5Q8' == correct_id
        bbid_mock.return_value = 'JPY'
        correct_id = tm_rates._currency_to_tdapi_basis_swap_rate_asset(asset)
        assert 'MAXVRBEZCJVH0C4V' == correct_id
        bbid_mock.return_value = 'AUD'
        correct_id = tm_rates._currency_to_tdapi_basis_swap_rate_asset(asset)
        assert 'MAY8H7HCNZ85FJKM' == correct_id
        bbid_mock.return_value = 'NZD'
        correct_id = tm_rates._currency_to_tdapi_basis_swap_rate_asset(asset)
        assert 'MAWK15C0P3SM6C7Q' == correct_id
        bbid_mock.return_value = 'CHF'
        correct_id = tm_rates._currency_to_tdapi_basis_swap_rate_asset(asset)
        assert 'MA7ZHB9T0PF1SB96' == correct_id
        bbid_mock.return_value = 'DKK'
        correct_id = tm_rates._currency_to_tdapi_basis_swap_rate_asset(asset)
        assert 'MA2164KK5DMYA561' == correct_id
        bbid_mock.return_value = 'NOK'
        correct_id = tm_rates._currency_to_tdapi_basis_swap_rate_asset(asset)
        assert 'MAPXC5YBPZJZXYMZ' == correct_id
        bbid_mock.return_value = 'SEK'
        correct_id = tm_rates._currency_to_tdapi_basis_swap_rate_asset(asset)
        assert 'MAS2NJCYHDHP8P0X' == correct_id
        bbid_mock.return_value = 'CAD'
        correct_id = tm_rates._currency_to_tdapi_basis_swap_rate_asset(asset)
        assert 'MARVD2E65AWEXXBA' == correct_id
        replace.restore()


def test_check_clearing_house():
    assert tm_rates._ClearingHouse.LCH == tm_rates._check_clearing_house('lch')
    assert tm_rates._ClearingHouse.CME == tm_rates._check_clearing_house(tm_rates._ClearingHouse.CME)
    assert tm_rates._ClearingHouse.LCH == tm_rates._check_clearing_house(None)
    invalid_ch = ['NYSE']
    for ch in invalid_ch:
        with pytest.raises(MqError):
            tm_rates._check_clearing_house(ch)


def test_get_swap_csa_terms():
    euribor_index = tm_rates.CURRENCY_TO_SWAP_RATE_BENCHMARK['EUR'][BenchmarkType.EURIBOR.value]
    usd_libor_index = tm_rates.CURRENCY_TO_SWAP_RATE_BENCHMARK['USD'][BenchmarkType.LIBOR.value]
    fed_funds_index = tm_rates.CURRENCY_TO_SWAP_RATE_BENCHMARK['USD'][BenchmarkType.Fed_Funds.value]
    estr_index = tm_rates.CURRENCY_TO_SWAP_RATE_BENCHMARK['EUR'][BenchmarkType.EUROSTR.value]
    assert dict(csaTerms='USD-1') == tm_rates._get_swap_csa_terms('USD', fed_funds_index)
    assert dict(csaTerms='EUR-EuroSTR') == tm_rates._get_swap_csa_terms('EUR', estr_index)
    assert {} == tm_rates._get_swap_csa_terms('EUR', euribor_index)
    assert {} == tm_rates._get_swap_csa_terms('USD', usd_libor_index)


def test_get_basis_swap_csa_terms():
    euribor_index = tm_rates.CURRENCY_TO_SWAP_RATE_BENCHMARK['EUR'][BenchmarkType.EURIBOR.value]
    usd_libor_index = tm_rates.CURRENCY_TO_SWAP_RATE_BENCHMARK['USD'][BenchmarkType.LIBOR.value]
    fed_funds_index = tm_rates.CURRENCY_TO_SWAP_RATE_BENCHMARK['USD'][BenchmarkType.Fed_Funds.value]
    sofr_index = tm_rates.CURRENCY_TO_SWAP_RATE_BENCHMARK['USD'][BenchmarkType.SOFR.value]
    estr_index = tm_rates.CURRENCY_TO_SWAP_RATE_BENCHMARK['EUR'][BenchmarkType.EUROSTR.value]
    eonia_index = tm_rates.CURRENCY_TO_SWAP_RATE_BENCHMARK['EUR'][BenchmarkType.EONIA.value]
    assert dict(csaTerms='USD-1') == tm_rates._get_basis_swap_csa_terms('USD', fed_funds_index, sofr_index)
    assert dict(csaTerms='EUR-EuroSTR') == tm_rates._get_basis_swap_csa_terms('EUR', estr_index, eonia_index)
    assert {} == tm_rates._get_basis_swap_csa_terms('EUR', eonia_index, euribor_index)
    assert {} == tm_rates._get_basis_swap_csa_terms('USD', fed_funds_index, usd_libor_index)


def test_match_floating_tenors():
    swap_args = dict(asset_parameters_payer_rate_option=tm_rates.CURRENCY_TO_SWAP_RATE_BENCHMARK['USD']['LIBOR'],
                     asset_parameters_payer_designated_maturity='12m',
                     asset_parameters_receiver_rate_option=tm_rates.CURRENCY_TO_SWAP_RATE_BENCHMARK['USD']['SOFR'],
                     asset_parameters_receiver_designated_maturity='1y')

    assert '1y' == tm_rates._match_floating_tenors(swap_args)['asset_parameters_receiver_designated_maturity']

    swap_args = dict(asset_parameters_payer_rate_option=tm_rates.CURRENCY_TO_SWAP_RATE_BENCHMARK['USD']['SOFR'],
                     asset_parameters_payer_designated_maturity='1y',
                     asset_parameters_receiver_rate_option=tm_rates.CURRENCY_TO_SWAP_RATE_BENCHMARK['USD']['LIBOR'],
                     asset_parameters_receiver_designated_maturity='12m')
    assert '1y' == tm_rates._match_floating_tenors(swap_args)['asset_parameters_payer_designated_maturity']

    swap_args = dict(asset_parameters_payer_rate_option=tm_rates.CURRENCY_TO_SWAP_RATE_BENCHMARK['GBP']['SONIA'],
                     asset_parameters_payer_designated_maturity='1y',
                     asset_parameters_receiver_rate_option=tm_rates.CURRENCY_TO_SWAP_RATE_BENCHMARK['GBP']['LIBOR'],
                     asset_parameters_receiver_designated_maturity='3m')
    assert '3m' == tm_rates._match_floating_tenors(swap_args)['asset_parameters_payer_designated_maturity']

    swap_args = dict(asset_parameters_payer_rate_option=tm_rates.CURRENCY_TO_SWAP_RATE_BENCHMARK['GBP']['LIBOR'],
                     asset_parameters_payer_designated_maturity='3m',
                     asset_parameters_receiver_rate_option=tm_rates.CURRENCY_TO_SWAP_RATE_BENCHMARK['GBP']['SONIA'],
                     asset_parameters_receiver_designated_maturity='1y')
    assert '3m' == tm_rates._match_floating_tenors(swap_args)['asset_parameters_receiver_designated_maturity']

    swap_args = dict(asset_parameters_payer_rate_option=tm_rates.CURRENCY_TO_SWAP_RATE_BENCHMARK['USD']['LIBOR'],
                     asset_parameters_payer_designated_maturity='3m',
                     asset_parameters_receiver_rate_option=tm_rates.CURRENCY_TO_SWAP_RATE_BENCHMARK['USD']['LIBOR'],
                     asset_parameters_receiver_designated_maturity='6m')

    assert swap_args == tm_rates._match_floating_tenors(swap_args)


def test_get_term_struct_date(mocker):
    today = datetime.datetime.today()
    biz_day = CustomBusinessDay()
    assert today == tm_rates._get_term_struct_date(tenor=today, index=today, business_day=biz_day)
    date_index = datetime.datetime(2020, 7, 31, 0, 0)
    assert date_index == tm_rates._get_term_struct_date(tenor='2020-07-31', index=date_index, business_day=biz_day)
    assert date_index == tm_rates._get_term_struct_date(tenor='0b', index=date_index, business_day=biz_day)
    assert datetime.datetime(2021, 7, 30, 0, 0) == tm_rates._get_term_struct_date(tenor='1y', index=date_index,
                                                                                  business_day=biz_day)


def test_cross_stored_direction_for_fx_vol(mocker):
    mocker.patch.object(GsSession.__class__, 'default_value',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_get', side_effect=mock_request)
    mocker.patch.object(GsSession.current, '_post', side_effect=mock_request)
    asset_id_list = ["MAYJPCVVF2RWXCES", "MATGYV0J9MPX534Z"]
    correct_mapping = ["MATGYV0J9MPX534Z", "MATGYV0J9MPX534Z"]
    with tm.PricingContext(dt.date.today()):
        for i in range(len(asset_id_list)):
            correct_id = tm.cross_stored_direction_for_fx_vol(asset_id_list[i])
            assert correct_id == correct_mapping[i]


def test_cross_to_usd_based_cross_for_fx_forecast(mocker):
    mocker.patch.object(GsSession.__class__, 'default_value',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_get', side_effect=mock_request)
    mocker.patch.object(GsSession.current, '_post', side_effect=mock_request)
    asset_id_list = ["MAYJPCVVF2RWXCES", "MATGYV0J9MPX534Z"]
    correct_mapping = ["MATGYV0J9MPX534Z", "MATGYV0J9MPX534Z"]
    with tm.PricingContext(dt.date.today()):
        for i in range(len(asset_id_list)):
            correct_id = tm.cross_to_usd_based_cross(asset_id_list[i])
            assert correct_id == correct_mapping[i]


def test_cross_to_used_based_cross(mocker):
    mocker.patch.object(GsSession.__class__, 'default_value',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_get', side_effect=mock_request)
    mocker.patch.object(GsSession.current, '_post', side_effect=mock_request)
    mocker.patch.object(SecurityMaster, 'get_asset', side_effect=TypeError('unsupported'))

    replace = Replacer()
    bbid_mock = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    bbid_mock.return_value = 'HELLO'

    assert 'FUN' == tm.cross_to_usd_based_cross(Cross('FUN', 'EURUSD'))
    replace.restore()


def test_cross_stored_direction(mocker):
    mocker.patch.object(GsSession.__class__, 'default_value',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_get', side_effect=mock_request)
    mocker.patch.object(GsSession.current, '_post', side_effect=mock_request)
    mocker.patch.object(SecurityMaster, 'get_asset', side_effect=TypeError('unsupported'))

    replace = Replacer()
    bbid_mock = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    bbid_mock.return_value = 'HELLO'

    assert 'FUN' == tm.cross_stored_direction_for_fx_vol(Cross('FUN', 'EURUSD'))
    replace.restore()


def test_get_tdapi_rates_assets(mocker):
    mock_asset_1 = GsAsset(asset_class='Rate', id='MAW25BGQJH9P6DPT', type_='Swap', name='Test_asset')
    mock_asset_2 = GsAsset(asset_class='Rate', id='MAA9MVX15AJNQCVG', type_='Swap', name='Test_asset')
    mock_asset_3 = GsAsset(asset_class='Rate', id='MANQHVYC30AZFT7R', type_='BasisSwap', name='Test_asset')

    replace = Replacer()
    assets = replace('gs_quant.timeseries.measures.GsAssetApi.get_many_assets', Mock())
    assets.return_value = [mock_asset_1]
    assert 'MAW25BGQJH9P6DPT' == tm_rates._get_tdapi_rates_assets()
    replace.restore()

    assets = replace('gs_quant.timeseries.measures.GsAssetApi.get_many_assets', Mock())
    assets.return_value = [mock_asset_1, mock_asset_2]
    kwargs = dict(asset_parameters_termination_date='10y', asset_parameters_effective_date='0b')
    with pytest.raises(MqValueError):
        tm_rates._get_tdapi_rates_assets(**kwargs)
    replace.restore()

    assets = replace('gs_quant.timeseries.measures.GsAssetApi.get_many_assets', Mock())
    assets.return_value = []
    with pytest.raises(MqValueError):
        tm_rates._get_tdapi_rates_assets()
    replace.restore()

    assets = replace('gs_quant.timeseries.measures.GsAssetApi.get_many_assets', Mock())
    assets.return_value = [mock_asset_1, mock_asset_2]
    kwargs = dict()
    assert ['MAW25BGQJH9P6DPT', 'MAA9MVX15AJNQCVG'] == tm_rates._get_tdapi_rates_assets(**kwargs)
    replace.restore()

    #   test case will test matching sofr maturity with libor leg and flipping legs to get right asset
    kwargs = dict(type='BasisSwap', asset_parameters_termination_date='10y',
                  asset_parameters_payer_rate_option=BenchmarkType.LIBOR,
                  asset_parameters_payer_designated_maturity='3m',
                  asset_parameters_receiver_rate_option=BenchmarkType.SOFR,
                  asset_parameters_receiver_designated_maturity='1y',
                  asset_parameters_clearing_house='lch', asset_parameters_effective_date='Spot',
                  asset_parameters_notional_currency='USD',
                  pricing_location='NYC')

    assets = replace('gs_quant.timeseries.measures.GsAssetApi.get_many_assets', Mock())
    assets.return_value = [mock_asset_3]
    assert 'MANQHVYC30AZFT7R' == tm_rates._get_tdapi_rates_assets(**kwargs)
    replace.restore()


def test_get_swap_leg_defaults():
    result_dict = dict(currency=CurrEnum.JPY, benchmark_type='JPY-LIBOR-BBA', floating_rate_tenor='6m',
                       pricing_location=PricingLocation.TKO)
    defaults = tm_rates._get_swap_leg_defaults(CurrEnum.JPY)
    assert result_dict == defaults

    result_dict = dict(currency=CurrEnum.USD, benchmark_type='USD-LIBOR-BBA', floating_rate_tenor='3m',
                       pricing_location=PricingLocation.NYC)
    defaults = tm_rates._get_swap_leg_defaults(CurrEnum.USD)
    assert result_dict == defaults

    result_dict = dict(currency=CurrEnum.EUR, benchmark_type='EUR-EURIBOR-TELERATE', floating_rate_tenor='6m',
                       pricing_location=PricingLocation.LDN)
    defaults = tm_rates._get_swap_leg_defaults(CurrEnum.EUR)
    assert result_dict == defaults

    result_dict = dict(currency=CurrEnum.SEK, benchmark_type='SEK-STIBOR-SIDE', floating_rate_tenor='6m',
                       pricing_location=PricingLocation.LDN)
    defaults = tm_rates._get_swap_leg_defaults(CurrEnum.SEK)
    assert result_dict == defaults


def test_check_forward_tenor():
    valid_tenors = [datetime.date(2020, 1, 1), '1y', 'imm2', 'frb2', '1m', '0b']
    for tenor in valid_tenors:
        assert tenor == tm_rates._check_forward_tenor(tenor)

    invalid_tenors = ['5yr', 'imm5', 'frb0']
    for tenor in invalid_tenors:
        with pytest.raises(MqError):
            tm_rates._check_forward_tenor(tenor)


def mock_commod(_cls, _q):
    d = {
        'price': [30, 30, 30, 30, 35.929686, 35.636039, 27.307498, 23.23177, 19.020833, 18.827291, 17.823749, 17.393958,
                  17.824999, 20.307603, 24.311249, 25.160103, 25.245728, 25.736873, 28.425206, 28.779789, 30.519996,
                  34.896348, 33.966973, 33.95489, 33.686348, 34.840307, 32.674163, 30.261665, 30, 30, 30]
    }
    df = MarketDataResponseFrame(data=d, index=pd.date_range('2019-05-01', periods=31, freq='H', tz=timezone('UTC')))
    df.dataset_ids = _test_datasets
    return df


def mock_commod_dup(_cls, _q):
    d = {'price': [35.929686, 35]}
    idx = pd.date_range('2019-05-01', periods=1, freq='H', tz=timezone('UTC'))
    df = MarketDataResponseFrame(data=d, index=idx.repeat(2))
    df.dataset_ids = _test_datasets
    return df


def mock_forward_price(_cls, _q):
    d = {
        'forwardPrice': [
            22.0039,
            24.8436,
            24.8436,
            11.9882,
            14.0188,
            11.6311,
            18.9234,
            21.3654,
            21.3654,
        ],
        'quantityBucket': [
            "PEAK",
            "PEAK",
            "PEAK",
            "7X8",
            "7X8",
            "7X8",
            "2X16H",
            "2X16H",
            "2X16H",

        ],
        'contract': [
            "J20",
            "K20",
            "M20",
            "J20",
            "K20",
            "M20",
            "J20",
            "K20",
            "M20",
        ]

    }
    df = MarketDataResponseFrame(data=d, index=pd.to_datetime([datetime.date(2019, 1, 2)] * 9))
    df.dataset_ids = _test_datasets
    return df


def mock_implied_volatility_elec():
    d = {
        'impliedVolatility': [
            0.3424,
            0.3624,
            0.4424,
            0.4424,
            0.4224,
            0.5324,
            0.3224,
            0.3324,
            0.3924,
        ],
        'quantityBucket': [
            "PEAK",
            "PEAK",
            "PEAK",
            "7X8",
            "7X8",
            "7X8",
            "2X16H",
            "2X16H",
            "2X16H",

        ],
        'contract': [
            "J20",
            "K20",
            "M20",
            "J20",
            "K20",
            "M20",
            "J20",
            "K20",
            "M20",
        ]

    }
    df = MarketDataResponseFrame(data=d, index=pd.to_datetime([datetime.date(2019, 1, 2)] * 9))
    df.dataset_ids = _test_datasets
    return df


def mock_fair_price(_cls, _q):
    d = {
        'fairPrice': [
            2.880,
            2.844,
            2.726,
        ],
        'contract': [
            "F21",
            "G21",
            "H21",
        ]
    }
    df = MarketDataResponseFrame(data=d, index=pd.to_datetime([datetime.date(2019, 1, 2)] * 3))
    df.dataset_ids = _test_datasets
    return df


def mock_eu_natgas_forward_price(_cls, _q):
    d = {'forwardPrice': [15.65], 'contract': ["H21"]}
    df = MarketDataResponseFrame(data=d, index=pd.to_datetime([datetime.date(2021, 1, 1)]))
    df.dataset_ids = _test_datasets
    return df


def mock_natgas_forward_price(_cls, _q):
    d = {
        'forwardPrice': [
            2.880,
            2.844,
            2.726,
        ],
        'contract': [
            "F21",
            "G21",
            "H21",
        ]
    }
    df = MarketDataResponseFrame(data=d, index=pd.to_datetime([datetime.date(2019, 1, 2)] * 3))
    df.dataset_ids = _test_datasets
    return df


def mock_natgas_implied_volatility(_cls, _q):
    d = {
        'impliedVolatility': [
            2.880,
            2.844,
            2.726,
        ],
        'contract': [
            "F21",
            "G21",
            "H21",
        ]
    }
    df = MarketDataResponseFrame(data=d, index=pd.to_datetime([datetime.date(2019, 1, 2)] * 3))
    df.dataset_ids = _test_datasets
    return df


def mock_fair_price_swap(_cls, _q):
    d = {'fairPrice': [2.880]}
    df = MarketDataResponseFrame(data=d, index=pd.to_datetime([datetime.date(2019, 1, 2)]))
    df.dataset_ids = _test_datasets
    return df


def mock_implied_volatility(_cls, _q):
    d = {
        'impliedVolatility': [
            2.880,
            2.844,
            2.726,
        ],
        'contract': [
            "F21",
            "G21",
            "H21",
        ]
    }
    df = MarketDataResponseFrame(data=d, index=pd.to_datetime([datetime.date(2019, 1, 2)] * 3))
    df.dataset_ids = _test_datasets
    return df


def mock_missing_bucket_forward_price(_cls, _q):
    d = {
        'forwardPrice': [
            22.0039,
            24.8436,
            24.8436,
            11.9882,
            14.0188,
            18.9234,
            21.3654,
            21.3654,
        ],
        'quantityBucket': [
            "PEAK",
            "PEAK",
            "PEAK",
            "7X8",
            "7X8",
            "2X16H",
            "2X16H",
            "2X16H",

        ],
        'contract': [
            "J20",
            "K20",
            "M20",
            "J20",
            "K20",
            "J20",
            "K20",
            "M20",
        ]

    }
    return pd.DataFrame(data=d, index=pd.to_datetime([datetime.date(2019, 1, 2)] * 8))


def mock_missing_bucket_implied_volatility():
    d = {
        'impliedVolatility': [
            0.3424,
            0.3624,
            0.4424,
            0.4424,
            0.4224,
            0.3224,
            0.3324,
            0.3924,
        ],
        'quantityBucket': [
            "PEAK",
            "PEAK",
            "PEAK",
            "7X8",
            "7X8",
            "2X16H",
            "2X16H",
            "2X16H",

        ],
        'contract': [
            "J20",
            "K20",
            "M20",
            "J20",
            "K20",
            "J20",
            "K20",
            "M20",
        ]

    }
    return pd.DataFrame(data=d, index=pd.to_datetime([datetime.date(2019, 1, 2)] * 8))


def mock_fx_vol(_cls, q):
    queries = q.get('queries', [])
    if len(queries) > 0 and 'Last' in queries[0]['measures']:
        return MarketDataResponseFrame({'impliedVolatility': [3]}, index=[pd.Timestamp('2019-01-04T12:00:00Z')])

    d = {
        'strikeReference': ['delta', 'spot', 'forward'],
        'relativeStrike': [25, 100, 100],
        'impliedVolatility': [5, 1, 2],
        'forecast': [1.1, 1.1, 1.1]
    }
    df = MarketDataResponseFrame(data=d, index=pd.date_range('2019-01-01', periods=3, freq='D'))
    df.dataset_ids = _test_datasets
    return df


def mock_fx_spot_fwd_3m(*args, **kwargs):
    d = pd.DataFrame({
        'spot': [1.18250, 1.18566, 1.18511],
        'forwardPoint': [0.00234, 0.00234, 0.00235],
        'tenor': ['3m', '3m', '3m'],
        'date': [pd.Timestamp(2020, 9, 2), pd.Timestamp(2020, 9, 3), pd.Timestamp(2020, 9, 4)]
    })
    d = d.set_index('date')
    df = MarketDataResponseFrame(d)
    df.dataset_ids = _test_datasets
    return df


def mock_fx_spot_fwd_2y(*args, **kwargs):
    d = pd.DataFrame({
        'spot': [1.18250, 1.18566, 1.18511],
        'forwardPoint': [0.02009, 0.02015, 0.02064],
        'tenor': ['2y', '2y', '2y'],
        'date': [pd.Timestamp(2020, 9, 2), pd.Timestamp(2020, 9, 3), pd.Timestamp(2020, 9, 4)]
    })
    d = d.set_index('date')
    df = MarketDataResponseFrame(d)
    df.dataset_ids = _test_datasets
    return df


def mock_fx_correlation(*args, **kwargs):
    d = pd.DataFrame({
        'impliedVolatility': [7.943208, 8.042599, 7.875325, 8.304180, 8.353483, 8.268724, 8.267971, 8.395843, 8.355239],
        'bbid': ['EURUSD', 'EURUSD', 'EURUSD', 'EURJPY', 'EURJPY', 'EURJPY', 'USDJPY', 'USDJPY', 'USDJPY'],
        'assetId': ['MAA0NE9QX2ABETG6', 'MAA0NE9QX2ABETG6', 'MAA0NE9QX2ABETG6', 'MAYPHS80JRWDJ8RC', 'MAYPHS80JRWDJ8RC',
                    'MAYPHS80JRWDJ8RC', 'MATGYV0J9MPX534Z', 'MATGYV0J9MPX534Z', 'MATGYV0J9MPX534Z'],
        'relativeStrike': [0, 0, 0, 0, 0, 0, 0, 0, 0],
        'strikeReference': ['delta', 'delta', 'delta', 'delta', 'delta', 'delta', 'delta', 'delta', 'delta'],
        'tenor': ['3m', '3m', '3m', '3m', '3m', '3m', '3m', '3m', '3m'],
        'date': [pd.Timestamp(2020, 9, 2), pd.Timestamp(2020, 9, 3), pd.Timestamp(2020, 9, 4),
                 pd.Timestamp(2020, 9, 2), pd.Timestamp(2020, 9, 3), pd.Timestamp(2020, 9, 4),
                 pd.Timestamp(2020, 9, 2), pd.Timestamp(2020, 9, 3), pd.Timestamp(2020, 9, 4)]
    })
    d = d.set_index('date')
    df = MarketDataResponseFrame(d)
    df.dataset_ids = _test_datasets
    return df


def mock_fx_forecast(_cls, _q):
    d = {
        'fxForecast': [1.1, 1.1, 1.1]
    }
    df = MarketDataResponseFrame(data=d, index=_index * 3)
    df.dataset_ids = _test_datasets
    return df


def mock_fx_delta(_cls, _q):
    d = {
        'relativeStrike': [25, -25, 0],
        'impliedVolatility': [1, 5, 2],
        'forecast': [1.1, 1.1, 1.1],
        'forwardPoint': [1, 1.1, 1.2]
    }
    df = MarketDataResponseFrame(data=d, index=_index * 3)
    df.dataset_ids = _test_datasets
    return df


def mock_fx_empty(_cls, _q):
    d = {
        'strikeReference': [],
        'relativeStrike': [],
        'impliedVolatility': []
    }
    df = MarketDataResponseFrame(data=d, index=[])
    df.dataset_ids = _test_datasets
    return df


def mock_fx_switch(_cls, _q, _n):
    replace = Replacer()
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_fx_empty)
    replace.restore()
    return Cross('MA1889', 'ABC/XYZ')


def mock_curr(_cls, _q):
    d = {
        'swapAnnuity': [1, 2, 3],
        'swapRate': [1, 2, 3],
        'basisSwapRate': [1, 2, 3],
        'swaptionVol': [1, 2, 3],
        'atmFwdRate': [1, 2, 3],
        'midcurveVol': [1, 2, 3],
        'capFloorVol': [1, 2, 3],
        'spreadOptionVol': [1, 2, 3],
        'inflationSwapRate': [1, 2, 3],
        'midcurveAtmFwdRate': [1, 2, 3],
        'capFloorAtmFwdRate': [1, 2, 3],
        'spreadOptionAtmFwdRate': [1, 2, 3],
        'strike': [0.25, 0.5, 0.75]
    }
    df = MarketDataResponseFrame(data=d, index=_index * 3)
    df.dataset_ids = _test_datasets
    return df


def mock_cross(_cls, _q):
    d = {
        'basis': [1, 2, 3],
    }
    df = MarketDataResponseFrame(data=d, index=_index * 3)
    df.dataset_ids = _test_datasets
    return df


def mock_eq(_cls, _q):
    d = {
        'relativeStrike': [0.75, 0.25, 0.5],
        'impliedVolatility': [5, 1, 2],
        'impliedCorrelation': [5, 1, 2],
        'realizedCorrelation': [3.14, 2.71828, 1.44],
        'averageImpliedVolatility': [5, 1, 2],
        'averageImpliedVariance': [5, 1, 2],
        'averageRealizedVolatility': [5, 1, 2],
        'impliedVolatilityByDeltaStrike': [5, 1, 2],
        'fundamentalMetric': [5, 1, 2]
    }
    df = MarketDataResponseFrame(data=d, index=_index * 3)
    df.dataset_ids = _test_datasets
    return df


def mock_eq_vol(_cls, q):
    queries = q.get('queries', [])
    if len(queries) > 0 and 'Last' in queries[0]['measures']:
        idx = [pd.Timestamp(datetime.datetime.now(pytz.UTC))]
        return MarketDataResponseFrame({'impliedVolatility': [3]}, index=idx)

    d = {
        'impliedVolatility': [5, 1, 2],
    }
    end = datetime.datetime.now(pytz.UTC).date() - datetime.timedelta(days=1)
    df = MarketDataResponseFrame(data=d, index=pd.date_range(end=end, periods=3, freq='D'))
    df.dataset_ids = _test_datasets
    return df


def mock_eq_vol_last_err(_cls, q):
    queries = q.get('queries', [])
    if len(queries) > 0 and 'Last' in queries[0]['measures']:
        raise MqValueError('error while getting last')

    d = {
        'impliedVolatility': [5, 1, 2],
    }
    end = datetime.date.today() - datetime.timedelta(days=1)
    df = MarketDataResponseFrame(data=d, index=pd.date_range(end=end, periods=3, freq='D'))
    df.dataset_ids = _test_datasets
    return df


def mock_eq_vol_last_empty(_cls, q):
    queries = q.get('queries', [])
    if len(queries) > 0 and 'Last' in queries[0]['measures']:
        return MarketDataResponseFrame()

    d = {
        'impliedVolatility': [5, 1, 2],
    }
    end = datetime.date.today() - datetime.timedelta(days=1)
    df = MarketDataResponseFrame(data=d, index=pd.date_range(end=end, periods=3, freq='D'))
    df.dataset_ids = _test_datasets
    return df


def mock_eq_norm(_cls, _q):
    d = {
        'relativeStrike': [-4.0, 4.0, 0],
        'impliedVolatility': [5, 1, 2]
    }
    df = MarketDataResponseFrame(data=d, index=_index * 3)
    df.dataset_ids = _test_datasets
    return df


def mock_eq_spot(_cls, _q):
    d = {
        'relativeStrike': [0.75, 1.25, 1.0],
        'impliedVolatility': [5, 1, 2]
    }
    df = MarketDataResponseFrame(data=d, index=_index * 3)
    df.dataset_ids = _test_datasets
    return df


def mock_inc(_cls, _q):
    d = {
        'relativeStrike': [0.25, 0.75],
        'impliedVolatility': [5, 1]
    }
    df = MarketDataResponseFrame(data=d, index=_index * 2)
    df.dataset_ids = _test_datasets
    return df


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


def mock_esg(_cls, _q):
    d = {
        "esNumericScore": [2, 4, 6],
        "esNumericPercentile": [81.2, 75.4, 65.7],
        "esPolicyScore": [2, 4, 6],
        "esPolicyPercentile": [81.2, 75.4, 65.7],
        "esScore": [2, 4, 6],
        "esPercentile": [81.2, 75.4, 65.7],
        "esProductImpactScore": [2, 4, 6],
        "esProductImpactPercentile": [81.2, 75.4, 65.7],
        "gScore": [2, 4, 6],
        "gPercentile": [81.2, 75.4, 65.7],
        "esMomentumScore": [2, 4, 6],
        "esMomentumPercentile": [81.2, 75.4, 65.7],
        "gRegionalScore": [2, 4, 6],
        "gRegionalPercentile": [81.2, 75.4, 65.7],
        "controversyScore": [2, 4, 6],
        "controversyPercentile": [81.2, 75.4, 65.7],
        "esDisclosurePercentage": [49.2, 55.7, 98.4]
    }
    df = MarketDataResponseFrame(data=d, index=_index * 3)
    df.dataset_ids = _test_datasets
    return df


def mock_index_positions_data(
        asset_id,
        start_date,
        end_date,
        fields=None,
        position_type=None
):
    return [
        {'underlyingAssetId': 'MA3',
         'netWeight': 0.1,
         'positionType': 'close',
         'assetId': 'MA890',
         'positionDate': '2020-01-01'
         },
        {'underlyingAssetId': 'MA1',
         'netWeight': 0.6,
         'positionType': 'close',
         'assetId': 'MA890',
         'positionDate': '2020-01-01'
         },
        {'underlyingAssetId': 'MA2',
         'netWeight': 0.3,
         'positionType': 'close',
         'assetId': 'MA890',
         'positionDate': '2020-01-01'
         }
    ]


def mock_rating(_cls, _q):
    d = {
        'rating': ['Buy', 'Sell', 'Buy', 'Neutral'],
        'convictionList': [1, 0, 0, 0]
    }
    df = MarketDataResponseFrame(data=d, index=pd.to_datetime([datetime.date(2020, 8, 13), datetime.date(2020, 8, 14),
                                                               datetime.date(2020, 8, 17), datetime.date(2020, 8, 18)]))
    df.dataset_ids = _test_datasets
    return df


def mock_gsdeer_gsfeer(_cls, assetId, start_date):
    d = {
        'gsdeer': [1, 1.2, 1.1],
        'gsfeer': [2, 1.8, 1.9],
        'year': [2000, 2010, 2020],
        'quarter': ['Q1', 'Q2', 'Q3']
    }
    df = MarketDataResponseFrame(data=d, index=_index * 3)
    return df


def mock_factor_profile(_cls, _q):
    d = {
        'growthScore': [0.238, 0.234, 0.234, 0.230],
        'financialReturnsScore': [0.982, 0.982, 0.982, 0.982],
        'multipleScore': [0.204, 0.192, 0.190, 0.190],
        'integratedScore': [0.672, 0.676, 0.676, 0.674]
    }
    df = MarketDataResponseFrame(data=d, index=pd.to_datetime([datetime.date(2020, 8, 13), datetime.date(2020, 8, 14),
                                                               datetime.date(2020, 8, 17), datetime.date(2020, 8, 18)]))
    df.dataset_ids = _test_datasets
    return df


def mock_commodity_forecast(_cls, _q):
    d = {
        'forecastPeriod': ['3m', '3m', '3m', '3m'],
        'forecastType': ['spotReturn', 'spotReturn', 'spotReturn', 'spotReturn'],
        'commodityForecast': [1700, 1400, 1500, 1600]
    }
    df = MarketDataResponseFrame(data=d, index=pd.to_datetime([datetime.date(2020, 8, 13), datetime.date(2020, 8, 14),
                                                               datetime.date(2020, 8, 17), datetime.date(2020, 8, 18)]))
    df.dataset_ids = _test_datasets
    return df


def mock_cds_spread(_cls, _q):
    d = {
        "spreadAt100": [0.000836],
        "spreadAt250": [0.000436],
        "spreadAt500": [0.00036],
    }
    df = MarketDataResponseFrame(d, index=_index2)
    return df


def test_skew():
    replace = Replacer()

    mock_spx = Index('MA890', AssetClass.Equity, 'SPX')
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_eq)
    actual = tm.skew(mock_spx, '1m', tm.SkewReference.DELTA, 25)
    assert_series_equal(pd.Series([2.0], index=_index, name='impliedVolatility'), pd.Series(actual))
    assert actual.dataset_ids == _test_datasets

    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_eq_norm)
    actual = tm.skew(mock_spx, '1m', tm.SkewReference.NORMALIZED, 4)
    assert_series_equal(pd.Series([2.0], index=_index, name='impliedVolatility'), pd.Series(actual))
    assert actual.dataset_ids == _test_datasets

    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_eq_spot)
    actual = tm.skew(mock_spx, '1m', tm.SkewReference.SPOT, 25)
    assert_series_equal(pd.Series([2.0], index=_index, name='impliedVolatility'), pd.Series(actual))
    assert actual.dataset_ids == _test_datasets

    mock = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    mock.return_value = mock_empty_market_data_response()
    actual = tm.skew(mock_spx, '1m', tm.SkewReference.SPOT, 25)
    assert actual.empty

    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_inc)
    with pytest.raises(MqError):
        tm.skew(mock_spx, '1m', tm.SkewReference.DELTA, 25)
    replace.restore()

    with pytest.raises(MqError):
        tm.skew(mock_spx, '1m', None, 25)


def test_skew_fx():
    replace = Replacer()
    cross = Cross('MAA0NE9QX2ABETG6', 'USD/EUR')
    xrefs = replace('gs_quant.timeseries.measures.GsAssetApi.get_asset_xrefs', Mock())
    xrefs.return_value = [GsTemporalXRef(dt.date(2019, 1, 1), dt.date(2952, 12, 31), XRef(bbid='EURUSD', ))]
    replace('gs_quant.markets.securities.SecurityMaster.get_asset', Mock()).return_value = cross
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_fx_delta)
    mock = cross

    actual = tm.skew(mock, '1m', tm.SkewReference.DELTA, 25)
    assert_series_equal(pd.Series([2.0], index=_index, name='impliedVolatility'), pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    with pytest.raises(MqError):
        tm.skew(mock, '1m', tm.SkewReference.DELTA, 25, real_time=True)
    with pytest.raises(MqError):
        tm.skew(mock, '1m', tm.SkewReference.SPOT, 25)
    with pytest.raises(MqError):
        tm.skew(mock, '1m', tm.SkewReference.FORWARD, 25)
    with pytest.raises(MqError):
        tm.skew(mock, '1m', tm.SkewReference.NORMALIZED, 25)
    with pytest.raises(MqError):
        tm.skew(mock, '1m', None, 25)

    replace.restore()


def test_implied_vol():
    replace = Replacer()
    mock_spx = Index('MA890', AssetClass.Equity, 'SPX')
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_eq_vol)
    idx = pd.date_range(end=datetime.datetime.now(pytz.UTC).date(), periods=4, freq='D')
    idx.freq = None

    actual = tm.implied_volatility(mock_spx, '1m', tm.VolReference.DELTA_CALL, 25)
    assert_series_equal(pd.Series([5, 1, 2, 3], index=idx, name='impliedVolatility'), pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    actual = tm.implied_volatility(mock_spx, '1m', tm.VolReference.DELTA_PUT, 75)
    assert_series_equal(pd.Series([5, 1, 2, 3], index=idx, name='impliedVolatility'), pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    with pytest.raises(MqError):
        tm.implied_volatility(mock_spx, '1m', tm.VolReference.DELTA_NEUTRAL)
    with pytest.raises(MqError):
        tm.implied_volatility(mock_spx, '1m', tm.VolReference.DELTA_CALL)
    replace.restore()


def test_tenor_month_to_year():
    assert tm._tenor_month_to_year('1y') == '1y'
    assert tm._tenor_month_to_year('11m') == '11m'
    assert tm._tenor_month_to_year('24m') == '2y'


def test_implied_vol_no_last():
    replace = Replacer()
    mock_spx = Index('MA890', AssetClass.Equity, 'SPX')
    idx = pd.date_range(end=datetime.date.today() - datetime.timedelta(days=1), periods=3, freq='D')
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_eq_vol_last_err)

    actual = tm.implied_volatility(mock_spx, '1m', tm.VolReference.DELTA_CALL, 25)
    assert_series_equal(pd.Series([5, 1, 2], index=idx, name='impliedVolatility'), pd.Series(actual))
    actual = tm.implied_volatility(mock_spx, '1m', tm.VolReference.DELTA_PUT, 75)
    assert_series_equal(pd.Series([5, 1, 2], index=idx, name='impliedVolatility'), pd.Series(actual))

    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_eq_vol_last_empty)
    actual = tm.implied_volatility(mock_spx, '1m', tm.VolReference.DELTA_CALL, 25)
    assert_series_equal(pd.Series([5, 1, 2], index=idx, name='impliedVolatility'), pd.Series(actual))
    actual = tm.implied_volatility(mock_spx, '1m', tm.VolReference.DELTA_PUT, 75)
    assert_series_equal(pd.Series([5, 1, 2], index=idx, name='impliedVolatility'), pd.Series(actual))
    replace.restore()


def test_implied_vol_fx():
    replace = Replacer()

    mock = Cross('MAA0NE9QX2ABETG6', 'USD/EUR')
    xrefs = replace('gs_quant.timeseries.measures.GsAssetApi.get_asset_xrefs', Mock())
    xrefs.return_value = [GsTemporalXRef(dt.date(2019, 1, 1), dt.date(2952, 12, 31), XRef(bbid='EURUSD', ))]
    replace('gs_quant.markets.securities.SecurityMaster.get_asset', Mock()).return_value = mock

    # for different delta strikes
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_fx_vol)
    actual = tm.implied_volatility(mock, '1m', tm.VolReference.DELTA_CALL, 25)
    expected = pd.Series([5, 1, 2, 3], index=pd.date_range('2019-01-01', periods=4, freq='D'), name='impliedVolatility')
    expected.index.freq = None
    assert_series_equal(expected, pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    actual = tm.implied_volatility(mock, '1m', tm.VolReference.DELTA_PUT, 25)
    assert_series_equal(expected, pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    actual = tm.implied_volatility(mock, '1m', tm.VolReference.DELTA_NEUTRAL)
    assert_series_equal(expected, pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    actual = tm.implied_volatility(mock, '1m', tm.VolReference.FORWARD, 100)
    assert_series_equal(expected, pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    actual = tm.implied_volatility(mock, '1m', tm.VolReference.SPOT, 100)
    assert_series_equal(expected, pd.Series(actual))
    assert actual.dataset_ids == _test_datasets

    # NORMALIZED not supported
    with pytest.raises(MqError):
        tm.implied_volatility(mock, '1m', tm.VolReference.DELTA_CALL)
    with pytest.raises(MqError):
        tm.implied_volatility(mock, '1m', tm.VolReference.NORMALIZED, 25)
    with pytest.raises(MqError):
        tm.implied_volatility(mock, '1m', tm.VolReference.SPOT, 25)
    with pytest.raises(MqError):
        tm.implied_volatility(mock, '1m', tm.VolReference.FORWARD, 25)
    replace.restore()


def test_fx_forecast():
    replace = Replacer()
    mock = Cross('MAA0NE9QX2ABETG6', 'USD/EUR')
    xrefs = replace('gs_quant.timeseries.measures.GsAssetApi.get_asset_xrefs', Mock())
    xrefs.return_value = [GsTemporalXRef(dt.date(2019, 1, 1), dt.date(2952, 12, 31), XRef(bbid='EURUSD', ))]
    replace('gs_quant.markets.securities.SecurityMaster.get_asset', Mock()).return_value = mock
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_fx_forecast)

    actual = tm.fx_forecast(mock, '12m')
    assert_series_equal(pd.Series([1.1, 1.1, 1.1], index=_index * 3, name='fxForecast'), pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    actual = tm.fx_forecast(mock, '3m')
    assert_series_equal(pd.Series([1.1, 1.1, 1.1], index=_index * 3, name='fxForecast'), pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    with pytest.raises(NotImplementedError):
        tm.fx_forecast(mock, '3m', real_time=True)
    replace.restore()


def test_fx_forecast_inverse():
    replace = Replacer()
    get_cross = replace('gs_quant.timeseries.measures.cross_to_usd_based_cross', Mock())
    get_cross.return_value = "MATGYV0J9MPX534Z"
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_fx_forecast)

    mock = Cross("MAYJPCVVF2RWXCES", 'USD/JPY')
    actual = tm.fx_forecast(mock, '3m')
    assert_series_equal(pd.Series([1 / 1.1, 1 / 1.1, 1 / 1.1], index=_index * 3, name='fxForecast'),
                        pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    replace.restore()


def test_vol_smile():
    replace = Replacer()
    mock_spx = Index('MA890', AssetClass.Equity, 'SPX')
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_eq)
    actual = tm.vol_smile(mock_spx, '1m', tm.VolSmileReference.FORWARD, '5d')
    assert_series_equal(pd.Series([5, 1, 2], index=[0.75, 0.25, 0.5], name='vol_smile'), pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    assert actual.name == 'vol_smile'
    actual = tm.vol_smile(mock_spx, '1m', tm.VolSmileReference.SPOT, '5d')
    assert_series_equal(pd.Series([5, 1, 2], index=[0.75, 0.25, 0.5], name='vol_smile'), pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    assert actual.name == 'vol_smile'

    market_mock = replace('gs_quant.timeseries.measures.get_df_with_retries', Mock())
    market_mock.return_value = mock_empty_market_data_response()
    actual = tm.vol_smile(mock_spx, '1m', tm.VolSmileReference.SPOT, '1d')
    assert actual.empty
    assert actual.dataset_ids == ()
    market_mock.assert_called_once()
    with pytest.raises(NotImplementedError):
        tm.vol_smile(mock_spx, '1m', tm.VolSmileReference.SPOT, '1d', real_time=True)
    replace.restore()


def test_impl_corr():
    replace = Replacer()
    mock_spx = Index('MA890', AssetClass.Equity, 'SPX')
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_eq)
    actual = tm.implied_correlation(mock_spx, '1m', tm.EdrDataReference.DELTA_CALL, 25)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='impliedCorrelation'), pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    actual = tm.implied_correlation(mock_spx, '1m', tm.EdrDataReference.DELTA_PUT, 75)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='impliedCorrelation'), pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    with pytest.raises(NotImplementedError):
        tm.implied_correlation(..., '1m', tm.EdrDataReference.DELTA_PUT, 75, real_time=True)
    with pytest.raises(MqError):
        tm.implied_correlation(..., '1m', tm.EdrDataReference.DELTA_CALL, 50, '')
    replace.restore()


def test_impl_corr_n(mocker):
    spx = Index('MA4B66MW5E27U8P32SB', AssetClass.Equity, 'SPX')
    with pytest.raises(MqValueError):
        tm.implied_correlation(spx, '1m', tm.EdrDataReference.DELTA_CALL, 0.5,
                               composition_date=datetime.date.today())
    with pytest.raises(MqValueError):
        tm.implied_correlation(spx, '1m', tm.EdrDataReference.DELTA_CALL, 0.5, 200)

    resources = os.path.join(os.path.dirname(__file__), '..', 'resources')
    i_vol = pd.read_csv(os.path.join(resources, 'SPX_50_icorr_in.csv'))
    i_vol.index = pd.to_datetime(i_vol['date'])
    weights = pd.read_csv(os.path.join(resources, 'SPX_50_weights.csv'))
    weights.set_index('underlyingAssetId', inplace=True)

    replace = Replacer()
    market_data = replace('gs_quant.timeseries.econometrics.GsDataApi.get_market_data', Mock())
    market_data.return_value = i_vol
    constituents = replace('gs_quant.timeseries.measures._get_index_constituent_weights', Mock())
    constituents.return_value = weights
    last_mock = replace('gs_quant.timeseries.measures.get_last_for_measure', Mock())
    last_mock.return_value = None

    mocker.patch.object(GsSession.__class__, 'default_value',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(OAuth2Session, '_authenticate', return_value=None)

    expected = pd.read_csv(os.path.join(resources, 'SPX_50_icorr_out.csv'))
    expected.index = pd.to_datetime(expected['date'])
    expected = expected['value']
    actual = tm.implied_correlation(spx, '1m', tm.EdrDataReference.DELTA_CALL, 0.5, 50, datetime.date(2020, 8, 31),
                                    source='PlotTool')
    expected = ExtendedSeries(expected)
    assert_series_equal(actual, expected, check_names=False)

    mask = i_vol.index < '2020-08-31'
    assert not all(mask)
    market_data.return_value = i_vol[mask]
    last_mock.return_value = i_vol[~mask]
    actual = tm.implied_correlation(spx, '1m', tm.EdrDataReference.DELTA_CALL, 0.5, 50, datetime.date(2020, 8, 31),
                                    source='PlotTool')
    assert_series_equal(actual, expected, check_names=False)

    market_data.return_value = pd.DataFrame()
    last_mock.return_value = pd.DataFrame()
    actual = tm.implied_correlation(spx, '1m', tm.EdrDataReference.DELTA_CALL, 0.5, 50, datetime.date(2020, 8, 31),
                                    source='PlotTool')
    assert actual.empty

    replace.restore()


def test_implied_corr_basket():
    replace = Replacer()

    dates = pd.DatetimeIndex([dt.date(2021, 1, 1), dt.date(2021, 1, 2), dt.date(2021, 1, 3), dt.date(2021, 1, 4),
                              dt.date(2021, 1, 5), dt.date(2021, 1, 6)])
    x = pd.DataFrame({'impliedVolatility': [0.1, 0.11, 0.12, 0.13, 0.14, 0.15]}, index=dates)
    x['assetId'] = 'MA4B66MW5E27U9VBB94'
    y = pd.DataFrame({'impliedVolatility': [0.2, 0.21, 0.22, 0.23, 0.24, 0.25]}, index=dates)
    y['assetId'] = 'MA4B66MW5E27UAL9SUX'
    z = pd.DataFrame({'impliedVolatility': [0.13, 0.21, 0.3, 0.31, 0.23, 0.24]}, index=dates)
    z['assetId'] = 'MA4B66MW5E27U8P32SB'
    implied_vol = x.append(y).append(z)

    x = pd.DataFrame({'spot': [100.0, 101, 103.02, 100.9596, 100.9596, 102.978792]}, index=dates)
    x['assetId'] = 'MA4B66MW5E27U9VBB94'
    y = pd.DataFrame({'spot': [100.0, 100, 100, 100, 100, 100]}, index=dates)
    y['assetId'] = 'MA4B66MW5E27UAL9SUX'
    spot_data = x.append(y)

    mock_data = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    mock_data.side_effect = [implied_vol, spot_data]

    mock_asset = replace('gs_quant.timeseries.backtesting.GsAssetApi.get_many_assets_data', Mock())
    mock_asset.return_value = [{'id': 'MA4B66MW5E27U9VBB94', 'bbid': 'AAPL UW'},
                               {'id': 'MA4B66MW5E27UAL9SUX', 'bbid': 'MSFT UW'}]

    spx = Index('MA4B66MW5E27U8P32SB', AssetClass.Equity, 'SPX')
    a_basket = tm.Basket(['AAPL UW', 'MSFT UW'], [0.1, 0.9])
    actual = tm.implied_correlation_with_basket(spx, '1y', tm.EdrDataReference.DELTA_PUT, 25, a_basket)
    expected = pd.Series([-433.33333, 198.60510, 1065.90909, 986.28763, 100.0, 100.0], index=dates)
    expected = ExtendedSeries(expected)
    assert_series_equal(actual, expected)

    with pytest.raises(NotImplementedError):
        tm.implied_correlation_with_basket(spx, '1y', tm.EdrDataReference.DELTA_PUT, 25, a_basket, real_time=True)

    replace.restore()


def test_realized_corr_basket():
    replace = Replacer()

    dates = pd.DatetimeIndex([dt.date(2021, 1, 1), dt.date(2021, 1, 2), dt.date(2021, 1, 3), dt.date(2021, 1, 4),
                              dt.date(2021, 1, 5), dt.date(2021, 1, 6)])
    x = pd.DataFrame({'spot': [100.0, 101, 103.02, 100.9596, 100.9596, 102.978792]}, index=dates)
    x['assetId'] = 'MA4B66MW5E27U9VBB94'
    y = pd.DataFrame({'spot': [100.0, 99.5, 100.1, 101, 100.7, 100.6]}, index=dates)
    y['assetId'] = 'MA4B66MW5E27UAL9SUX'
    constituents_spot = x.append(y)

    index_spot = pd.DataFrame({'spot': [100.0, 101, 102, 103, 103.3, 104]}, index=dates)
    index_spot['assetId'] = 'MA4B66MW5E27U8P32SB'

    mock_data = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    mock_data.side_effect = [index_spot, constituents_spot]

    mock_asset = replace('gs_quant.timeseries.backtesting.GsAssetApi.get_many_assets_data', Mock())
    mock_asset.return_value = [{'id': 'MA4B66MW5E27U9VBB94', 'bbid': 'AAPL UW'},
                               {'id': 'MA4B66MW5E27UAL9SUX', 'bbid': 'MSFT UW'}]

    spx = Index('MA4B66MW5E27U8P32SB', AssetClass.Equity, 'SPX')
    a_basket = tm.Basket(['AAPL UW', 'MSFT UW'], [0.1, 0.9])
    actual = tm.realized_correlation_with_basket(spx, '2d', a_basket)
    expected = pd.Series([np.nan, np.nan, -501.344109, -108.318770, -168.132382, 109.044958], index=dates)
    expected = ExtendedSeries(expected)
    assert_series_equal(actual, expected)

    with pytest.raises(NotImplementedError):
        tm.realized_correlation_with_basket(spx, '2d', a_basket, real_time=True)

    replace.restore()


def test_real_corr():
    spx = Index('MA4B66MW5E27U8P32SB', AssetClass.Equity, 'SPX')
    with pytest.raises(NotImplementedError):
        tm.realized_correlation(spx, '1m', real_time=True)

    replace = Replacer()
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_eq)
    actual = tm.realized_correlation(spx, '1m')
    assert_series_equal(pd.Series([3.14, 2.71828, 1.44], index=_index * 3), pd.Series(actual), check_names=False)
    assert actual.dataset_ids == _test_datasets
    replace.restore()


def test_real_corr_missing():
    spx = Index('MA4B66MW5E27U8P32SB', AssetClass.Equity, 'SPX')
    d = {
        'assetId': ['MA4B66MW5E27U8P32SB'] * 3,
        'spot': [3000, 3100, 3050],
    }
    df = MarketDataResponseFrame(data=d, index=pd.date_range('2020-08-01', periods=3, freq='D'))

    resources = os.path.join(os.path.dirname(__file__), '..', 'resources')
    weights = pd.read_csv(os.path.join(resources, 'SPX_50_weights.csv'))
    weights.set_index('underlyingAssetId', inplace=True)

    replace = Replacer()
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', lambda *args, **kwargs: df)
    constituents = replace('gs_quant.timeseries.measures._get_index_constituent_weights', Mock())
    constituents.return_value = weights
    last_mock = replace('gs_quant.timeseries.measures.get_last_for_measure', Mock())
    last_mock.return_value = None

    with pytest.raises(MqValueError):
        tm.realized_correlation(spx, '1m', 50)
    replace.restore()


def test_real_corr_n():
    spx = Index('MA4B66MW5E27U8P32SB', AssetClass.Equity, 'SPX')
    with pytest.raises(MqValueError):
        tm.realized_correlation(spx, '1m', composition_date=datetime.date.today())
    with pytest.raises(MqValueError):
        tm.realized_correlation(spx, '1m', 200)

    resources = os.path.join(os.path.dirname(__file__), '..', 'resources')
    r_vol = pd.read_csv(os.path.join(resources, 'SPX_50_rcorr_in.csv'))
    r_vol.index = pd.to_datetime(r_vol['date'])
    weights = pd.read_csv(os.path.join(resources, 'SPX_50_weights.csv'))
    weights.set_index('underlyingAssetId', inplace=True)

    replace = Replacer()
    market_data = replace('gs_quant.timeseries.econometrics.GsDataApi.get_market_data', Mock())
    market_data.return_value = r_vol
    constituents = replace('gs_quant.timeseries.measures._get_index_constituent_weights', Mock())
    constituents.return_value = weights
    last_mock = replace('gs_quant.timeseries.measures.get_last_for_measure', Mock())
    last_mock.return_value = None

    expected = pd.read_csv(os.path.join(resources, 'SPX_50_rcorr_out.csv'))
    expected.index = pd.to_datetime(expected['date'])
    expected = ExtendedSeries(expected['value'])
    actual = tm.realized_correlation(spx, '1m', 50, datetime.date(2020, 8, 31), source='PlotTool')
    assert_series_equal(actual, expected, check_names=False)

    mask = r_vol.index < '2020-08-31'
    assert not all(mask)
    market_data.return_value = r_vol[mask]
    last_mock.return_value = r_vol[~mask]
    actual = tm.realized_correlation(spx, '1m', 50, datetime.date(2020, 8, 31), source='PlotTool')
    assert_series_equal(actual, expected, check_names=False)

    replace.restore()


def test_cds_implied_vol():
    replace = Replacer()
    mock_cds = Index('MA890', AssetClass.Equity, 'CDS')
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_eq)
    actual = tm.cds_implied_volatility(mock_cds, '1m', '5y', tm.CdsVolReference.DELTA_CALL, 10)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='impliedVolatilityByDeltaStrike'),
                        pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    actual = tm.cds_implied_volatility(mock_cds, '1m', '5y', tm.CdsVolReference.FORWARD, 100)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='impliedVolatilityByDeltaStrike'),
                        pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    with pytest.raises(NotImplementedError):
        tm.cds_implied_volatility(..., '1m', '5y', tm.CdsVolReference.DELTA_PUT, 75, real_time=True)
    replace.restore()


def test_implied_vol_credit():
    replace = Replacer()
    mock_cds = Index('MA890', AssetClass.Equity, 'CDS')
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_eq)
    actual = tm.implied_volatility_credit(mock_cds, '1m', tm.CdsVolReference.DELTA_CALL, 10)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='impliedVolatilityByDeltaStrike'),
                        pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    actual = tm.implied_volatility_credit(mock_cds, '1m', tm.CdsVolReference.DELTA_PUT, 10)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='impliedVolatilityByDeltaStrike'),
                        pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    actual = tm.implied_volatility_credit(mock_cds, '1m', tm.CdsVolReference.FORWARD, 100)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='impliedVolatilityByDeltaStrike'),
                        pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    with pytest.raises(NotImplementedError):
        tm.implied_volatility_credit(..., '1m', tm.CdsVolReference.DELTA_PUT, 75, real_time=True)
    with pytest.raises(NotImplementedError):
        tm.implied_volatility_credit(..., '1m', "", 75)
    replace.restore()


def test_cds_spreads():
    replace = Replacer()
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_cds_spread)
    cds_asset = DefaultSwap('MAD6V3NP8ZB7HZTY', 'Lockheed_C_PFA_2y_USD')
    actual = tm.cds_spread(cds_asset, 100, "NYC")
    assert_series_equal(pd.Series([0.000836], index=_index2, name='spreadAt100'), pd.Series(actual))
    actual = tm.cds_spread(cds_asset, 250, "NYC")
    assert_series_equal(pd.Series([0.000436], index=_index2, name='spreadAt250'), pd.Series(actual))
    actual = tm.cds_spread(cds_asset, 500, "NYC")
    assert_series_equal(pd.Series([0.00036], index=_index2, name='spreadAt500'), pd.Series(actual))
    with pytest.raises(NotImplementedError):
        tm.cds_spread(cds_asset, 200, "NYC")
    with pytest.raises(NotImplementedError):
        tm.cds_spread(cds_asset, 200, "NYC", real_time=True)
    replace.restore()


def test_avg_impl_vol(mocker):
    replace = Replacer()
    mock_spx = Index('MA890', AssetClass.Equity, 'SPX')
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_eq)
    last_mock = replace('gs_quant.timeseries.measures.get_last_for_measure', Mock())
    last_mock.return_value = None

    actual = tm.average_implied_volatility(mock_spx, '1m', tm.EdrDataReference.DELTA_CALL, 25)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='averageImpliedVolatility'), pd.Series(actual))
    assert actual.dataset_ids == _test_datasets

    actual = tm.average_implied_volatility(mock_spx, '1m', tm.EdrDataReference.DELTA_PUT, 75)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='averageImpliedVolatility'), pd.Series(actual))
    assert actual.dataset_ids == _test_datasets

    replace.restore()

    df1 = pd.DataFrame(data={'impliedVolatility': [1, 2, 3], 'assetId': ['MA1', 'MA1', 'MA1']},
                       index=pd.date_range(start='2020-01-01', periods=3))
    df2 = pd.DataFrame(data={'impliedVolatility': [2, 3, 4], 'assetId': ['MA2', 'MA2', 'MA2']},
                       index=pd.date_range(start='2020-01-01', periods=3))
    df3 = pd.DataFrame(data={'impliedVolatility': [2, 5], 'assetId': ['MA3', 'MA3']},
                       index=pd.date_range(start='2020-01-01', periods=2))

    replace('gs_quant.api.gs.assets.GsAssetApi.get_asset_positions_data', mock_index_positions_data)
    market_data_mock = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    mock_implied_vol = MarketDataResponseFrame(pd.concat([df1, df2, df3], join='inner'))
    mock_implied_vol.dataset_ids = _test_datasets
    market_data_mock.return_value = mock_implied_vol
    last_mock = replace('gs_quant.timeseries.measures.get_last_for_measure', Mock())
    last_mock.return_value = None

    mocker.patch.object(GsSession.__class__, 'default_value',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(OAuth2Session, '_authenticate', return_value=None)

    actual = tm.average_implied_volatility(mock_spx, '1m', tm.EdrDataReference.DELTA_CALL, 25, 3, '1d')
    expected = pd.Series([1.4, 2.6, 3.33333], index=pd.date_range(start='2020-01-01', periods=3))
    expected.index.freq = None
    assert_series_equal(expected, pd.Series(actual), check_names=False)
    assert actual.dataset_ids == _test_datasets

    last_mock.return_value = pd.DataFrame(data={'impliedVolatility': [2], 'assetId': ['MA3']},
                                          index=pd.date_range(start='2020-01-03', periods=1))
    actual = tm.average_implied_volatility(mock_spx, '1m', tm.EdrDataReference.DELTA_CALL, 25, 3, '1d')
    expected = pd.Series([1.4, 2.6, 3.2], index=pd.date_range(start='2020-01-01', periods=3))
    expected.index.freq = None
    assert_series_equal(expected, pd.Series(actual), check_names=False)

    with pytest.raises(NotImplementedError):
        tm.average_implied_volatility(..., '1m', tm.EdrDataReference.DELTA_PUT, 75, real_time=True)

    with pytest.raises(MqValueError):
        tm.average_implied_volatility(mock_spx, '1m', tm.EdrDataReference.DELTA_PUT, 75, top_n_of_index=None,
                                      composition_date='1d')

    with pytest.raises(NotImplementedError):
        tm.average_implied_volatility(mock_spx, '1m', tm.EdrDataReference.DELTA_PUT, 75, top_n_of_index=101)

    replace.restore()


def test_avg_realized_vol():
    replace = Replacer()

    mock_spx = Index('MA890', AssetClass.Equity, 'SPX')
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_eq)

    actual = tm.average_realized_volatility(mock_spx, '1m')
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='averageRealizedVolatility'), pd.Series(actual))
    assert actual.dataset_ids == _test_datasets

    replace.restore()

    df1 = pd.DataFrame(data={'spot': [1, 2, 3], 'assetId': ['MA1', 'MA1', 'MA1']},
                       index=pd.date_range(start='2020-01-01', periods=3))
    df2 = pd.DataFrame(data={'spot': [2, 3, 4], 'assetId': ['MA2', 'MA2', 'MA2']},
                       index=pd.date_range(start='2020-01-01', periods=3))
    df3 = pd.DataFrame(data={'spot': [2, 2, 2], 'assetId': ['MA3', 'MA3', 'MA3']},
                       index=pd.date_range(start='2020-01-01', periods=3))
    mock_spot = MarketDataResponseFrame(pd.concat([df1, df2, df3], join='inner'))
    mock_spot.dataset_ids = _test_datasets

    replace('gs_quant.api.gs.assets.GsAssetApi.get_asset_positions_data', mock_index_positions_data)
    last_mock = replace('gs_quant.timeseries.measures.get_last_for_measure', Mock())
    last_mock.return_value = None
    market_data_mock = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    market_data_mock.return_value = mock_spot

    actual = tm.average_realized_volatility(mock_spx, '2d', Returns.SIMPLE, 3, '1d')
    expected = pd.Series([392.874026], index=pd.date_range(start='2020-01-03', periods=1),
                         name='averageRealizedVolatility')
    expected.index.freq = None
    assert_series_equal(expected, pd.Series(actual))
    assert actual.dataset_ids == _test_datasets

    dfl = pd.DataFrame(data={'spot': [5, 5, 5], 'assetId': ['MA1', 'MA2', 'MA3']},
                       index=[pd.to_datetime('2020-01-04')] * 3)
    last_mock.return_value = dfl
    actual = tm.average_realized_volatility(mock_spx, '2d', Returns.SIMPLE, 3, '1d')
    expected = pd.Series([392.874026, 308.686734], index=pd.to_datetime(['2020-01-03', '2020-01-04']),
                         name='averageRealizedVolatility')
    assert_series_equal(expected, pd.Series(actual))

    last_mock.return_value = None
    df4 = pd.DataFrame(data={'spot': [2, 2], 'assetId': ['MA3', 'MA3']},
                       index=pd.date_range(start='2020-01-01', periods=2))
    mock_spot_2 = MarketDataResponseFrame(pd.concat([df1, df2, df4], join='inner'))
    market_data_mock.return_value = mock_spot_2
    actual = tm.average_realized_volatility(mock_spx, '2d', Returns.SIMPLE, 3, '1d')
    assert actual.dropna().empty

    with pytest.raises(NotImplementedError):
        tm.average_realized_volatility(mock_spx, '1w', real_time=True)

    with pytest.raises(MqValueError):
        tm.average_realized_volatility(mock_spx, '1w', composition_date='1d')

    with pytest.raises(NotImplementedError):
        tm.average_realized_volatility(mock_spx, '1w', Returns.LOGARITHMIC)

    with pytest.raises(NotImplementedError):
        tm.average_realized_volatility(mock_spx, '1w', Returns.SIMPLE, 201)

    replace.restore()

    empty_positions_data_mock = replace('gs_quant.api.gs.assets.GsAssetApi.get_asset_positions_data', Mock())
    empty_positions_data_mock.return_value = []
    with pytest.raises(MqValueError):
        tm.average_realized_volatility(mock_spx, '1w', Returns.SIMPLE, 5)

    replace.restore()


def test_avg_impl_var():
    replace = Replacer()
    mock_spx = Index('MA890', AssetClass.Equity, 'SPX')
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_eq)
    actual = tm.average_implied_variance(mock_spx, '1m', tm.EdrDataReference.DELTA_CALL, 25)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='averageImpliedVariance'), pd.Series(actual))
    actual = tm.average_implied_variance(mock_spx, '1m', tm.EdrDataReference.DELTA_PUT, 75)
    assert actual.dataset_ids == _test_datasets
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='averageImpliedVariance'), pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    with pytest.raises(NotImplementedError):
        tm.average_implied_variance(..., '1m', tm.EdrDataReference.DELTA_PUT, 75, real_time=True)
    replace.restore()


def test_basis_swap_spread(mocker):
    replace = Replacer()
    args = dict(swap_tenor='10y', spread_benchmark_type=None, spread_tenor=None,
                reference_benchmark_type=None, reference_tenor=None, forward_tenor='0b', real_time=False)

    mock_nok = Currency('MA891', 'EGP')
    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'EGP'
    args['asset'] = mock_nok
    with pytest.raises(NotImplementedError):
        tm_rates.basis_swap_spread(**args)

    mock_usd = Currency('MAZ7RWC904JYHYPS', 'USD')
    args['asset'] = mock_usd
    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'USD'
    with pytest.raises(NotImplementedError):
        tm_rates.basis_swap_spread(..., '1y', real_time=True)

    args['swap_tenor'] = '5yr'
    with pytest.raises(MqValueError):
        tm_rates.basis_swap_spread(**args)
    args['swap_tenor'] = '6y'

    args['spread_tenor'] = '5yr'
    with pytest.raises(MqValueError):
        tm_rates.basis_swap_spread(**args)
    args['spread_tenor'] = '3m'

    args['reference_tenor'] = '5yr'
    with pytest.raises(MqValueError):
        tm_rates.basis_swap_spread(**args)
    args['reference_tenor'] = '6m'

    args['forward_tenor'] = '5yr'
    with pytest.raises(MqValueError):
        tm_rates.basis_swap_spread(**args)
    args['forward_tenor'] = None

    args['spread_benchmark_type'] = BenchmarkType.STIBOR
    with pytest.raises(MqValueError):
        tm_rates.basis_swap_spread(**args)
    args['spread_benchmark_type'] = BenchmarkType.LIBOR

    args['reference_benchmark_type'] = 'libor_3m'
    with pytest.raises(MqValueError):
        tm_rates.basis_swap_spread(**args)
    args['reference_benchmark_type'] = BenchmarkType.LIBOR

    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'USD'
    identifiers = replace('gs_quant.timeseries.measures_rates._get_tdapi_rates_assets', Mock())
    identifiers.return_value = {'MAQB1PGEJFCET3GG'}
    mocker.patch.object(GsDataApi, 'get_market_data', return_value=mock_curr(None, None))
    actual = tm_rates.basis_swap_spread(**args)
    expected = tm.ExtendedSeries([1, 2, 3], index=_index * 3, name='basisSwapRate')
    expected.dataset_ids = _test_datasets
    assert_series_equal(expected, actual)
    assert actual.dataset_ids == expected.dataset_ids

    args['reference_benchmark_type'] = BenchmarkType.SOFR
    args['reference_tenor'] = '1y'
    args['reference_benchmark_type'] = BenchmarkType.LIBOR
    args['reference_tenor'] = '3m'

    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'USD'
    identifiers = replace('gs_quant.timeseries.measures_rates._get_tdapi_rates_assets', Mock())
    identifiers.return_value = {'MA06ATQ9CM0DCZFC'}
    mocker.patch.object(GsDataApi, 'get_market_data', return_value=mock_curr(None, None))
    args['location'] = PricingLocation.NYC
    actual = tm_rates.basis_swap_spread(**args)
    expected = tm.ExtendedSeries([1, 2, 3], index=_index * 3, name='basisSwapRate')
    expected.dataset_ids = _test_datasets
    assert_series_equal(expected, actual)
    assert actual.dataset_ids == expected.dataset_ids

    replace.restore()


def test_swap_rate(mocker):
    replace = Replacer()
    args = dict(swap_tenor='10y', benchmark_type=None, floating_rate_tenor=None, forward_tenor='0b', real_time=False)

    mock_usd = Currency('MAZ7RWC904JYHYPS', 'USD')
    args['asset'] = mock_usd
    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'USD'

    args['swap_tenor'] = '5yr'
    with pytest.raises(MqValueError):
        tm_rates.swap_rate(**args)
    args['swap_tenor'] = '10y'

    args['floating_rate_tenor'] = '5yr'
    with pytest.raises(MqValueError):
        tm_rates.swap_rate(**args)
    args['floating_rate_tenor'] = '1y'

    args['forward_tenor'] = '5yr'
    with pytest.raises(MqValueError):
        tm_rates.swap_rate(**args)
    args['forward_tenor'] = None

    args['benchmark_type'] = BenchmarkType.STIBOR
    with pytest.raises(MqValueError):
        tm_rates.swap_rate(**args)

    args['benchmark_type'] = 'sonia'
    with pytest.raises(MqValueError):
        tm_rates.swap_rate(**args)
    args['benchmark_type'] = 'fed_funds'

    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'USD'
    identifiers = replace('gs_quant.timeseries.measures_rates._get_tdapi_rates_assets', Mock())
    identifiers.return_value = {'MAZ7RWC904JYHYPS'}
    mocker.patch.object(GsDataApi, 'get_market_data', return_value=mock_curr(None, None))
    actual = tm_rates.swap_rate(**args)
    expected = tm.ExtendedSeries([1, 2, 3], index=_index * 3, name='swapRate')
    expected.dataset_ids = _test_datasets
    assert_series_equal(expected, actual)
    assert actual.dataset_ids == _test_datasets

    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'EUR'
    identifiers = replace('gs_quant.timeseries.measures_rates._get_tdapi_rates_assets', Mock())
    identifiers.return_value = {'MAJNQPFGN1EBDHAE'}
    mocker.patch.object(GsDataApi, 'get_market_data', return_value=mock_curr(None, None))
    args['asset'] = Currency('MAJNQPFGN1EBDHAE', 'EUR')
    args['benchmark_type'] = 'estr'
    args['location'] = PricingLocation.LDN
    actual = tm_rates.swap_rate(**args)
    expected = tm.ExtendedSeries([1, 2, 3], index=_index * 3, name='swapRate')
    expected.dataset_ids = _test_datasets
    assert_series_equal(expected, actual)
    assert actual.dataset_ids == _test_datasets
    replace.restore()


def test_swap_annuity(mocker):
    replace = Replacer()
    args = dict(swap_tenor='10y', benchmark_type=None, floating_rate_tenor=None, forward_tenor='0b', real_time=False)

    mock_nok = Currency('MA891', 'PLN')
    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'PLN'
    args['asset'] = mock_nok
    with pytest.raises(NotImplementedError):
        tm_rates.swap_annuity(**args)

    mock_usd = Currency('MAZ7RWC904JYHYPS', 'USD')
    args['asset'] = mock_usd
    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'USD'
    with pytest.raises(NotImplementedError):
        tm_rates.swap_annuity(..., '1y', real_time=True)

    args['swap_tenor'] = '5yr'
    with pytest.raises(MqValueError):
        tm_rates.swap_annuity(**args)
    args['swap_tenor'] = '10y'

    args['floating_rate_tenor'] = '5yr'
    with pytest.raises(MqValueError):
        tm_rates.swap_annuity(**args)
    args['floating_rate_tenor'] = '1y'

    args['forward_tenor'] = '5yr'
    with pytest.raises(MqValueError):
        tm_rates.swap_annuity(**args)
    args['forward_tenor'] = None

    args['benchmark_type'] = BenchmarkType.STIBOR
    with pytest.raises(MqValueError):
        tm_rates.swap_annuity(**args)
    args['benchmark_type'] = BenchmarkType.SOFR

    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'USD'
    identifiers = replace('gs_quant.timeseries.measures_rates._get_tdapi_rates_assets', Mock())
    identifiers.return_value = {'MAZ7RWC904JYHYPS'}
    mocker.patch.object(GsDataApi, 'get_market_data', return_value=mock_curr(None, None))
    actual = tm_rates.swap_annuity(**args)
    expected = abs(tm.ExtendedSeries([1.0, 2.0, 3.0], index=_index * 3, name='swapAnnuity') * 1e4 / 1e8)
    expected.dataset_ids = _test_datasets
    assert_series_equal(expected, actual)
    assert actual.dataset_ids == expected.dataset_ids
    replace.restore()


def test_swap_term_structure():
    replace = Replacer()
    args = dict(benchmark_type=None, floating_rate_tenor=None, tenor_type=tm_rates._SwapTenorType.FORWARD_TENOR,
                tenor='0b', real_time=False)

    mock_nok = Currency('MA891', 'PLN')
    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'PLN'
    args['asset'] = mock_nok
    with pytest.raises(NotImplementedError):
        tm_rates.swap_term_structure(**args)

    mock_usd = Currency('MAZ7RWC904JYHYPS', 'USD')
    args['asset'] = mock_usd
    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'USD'
    with pytest.raises(NotImplementedError):
        tm_rates.swap_term_structure(..., '1y', real_time=True)

    args['floating_rate_tenor'] = '5yr'
    with pytest.raises(MqValueError):
        tm_rates.swap_term_structure(**args)
    args['floating_rate_tenor'] = '3m'

    args['tenor_type'] = 'expiry'
    with pytest.raises(MqValueError):
        tm_rates.swap_term_structure(**args)
    args['tenor_type'] = None

    args['tenor'] = '5yr'
    with pytest.raises(MqValueError):
        tm_rates.swap_term_structure(**args)
    args['tenor'] = None

    args['benchmark_type'] = BenchmarkType.STIBOR
    with pytest.raises(MqValueError):
        tm_rates.swap_term_structure(**args)
    args['benchmark_type'] = BenchmarkType.LIBOR

    bd_mock = replace('gs_quant.data.dataset.Dataset.get_data', Mock())
    bd_mock.return_value = pd.DataFrame(data=dict(date="2020-04-10", exchange="NYC", description="Good Friday"),
                                        index=[pd.Timestamp('2020-04-10')])
    args['pricing_date'] = datetime.date(2020, 4, 10)
    with pytest.raises(MqValueError):
        tm_rates.swap_term_structure(**args)
    args['pricing_date'] = None

    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'USD'
    identifiers_empty = replace('gs_quant.timeseries.measures.GsAssetApi.get_many_assets', Mock())
    identifiers_empty.return_value = {}
    with pytest.raises(MqValueError):
        tm_rates.swap_term_structure(**args)

    identifiers = replace('gs_quant.timeseries.measures.GsAssetApi.get_many_assets', Mock())
    mock_asset = Currency('USD', name='USD')
    mock_asset.id = 'MAEMPCXQG3T716EX'
    mock_asset.exchange = 'OTC'
    identifiers.return_value = [mock_asset]

    d = {
        'terminationTenor': ['1y', '2y', '3y', '4y'], 'swapRate': [1, 2, 3, 4],
        'assetId': ['MAEMPCXQG3T716EX', 'MAFRSWPAF5QPNTP2', 'MA88BXZ3TCTXTFW1', 'MAC4KAG9B9ZAZHFT']
    }

    pricing_date_mock = replace('gs_quant.timeseries.measures_rates._range_from_pricing_date', Mock())
    pricing_date_mock.return_value = [datetime.date(2019, 1, 1), datetime.date(2019, 1, 1)]
    bd_mock.return_value = pd.DataFrame()
    market_data_mock = replace('gs_quant.timeseries.measures_rates._market_data_timed', Mock())

    market_data_mock.return_value = pd.DataFrame()
    df = pd.DataFrame(data=d, index=_index * 4)
    assert tm_rates.swap_term_structure(**args).empty

    market_data_mock.return_value = df
    with DataContext('2019-01-01', '2025-01-01'):
        actual = tm_rates.swap_term_structure(**args)
    actual.dataset_ids = _test_datasets
    expected = tm.ExtendedSeries([1, 2, 3, 4], index=pd.to_datetime(['2020-01-01', '2021-01-01', '2021-12-31',
                                                                     '2022-12-30']))
    expected.dataset_ids = _test_datasets
    assert_series_equal(expected, actual, check_names=False)
    assert actual.dataset_ids == expected.dataset_ids

    df = pd.DataFrame(data={'effectiveTenor': ['1y'], 'swapRate': [1], 'assetId': ['MAEMPCXQG3T716EX']}, index=_index)
    market_data_mock.return_value = df
    args['tenor_type'] = 'swap_tenor'
    args['tenor'] = '5y'
    args['location'] = PricingLocation.NYC
    with DataContext('2019-01-01', '2025-01-01'):
        actual = tm_rates.swap_term_structure(**args)
    actual.dataset_ids = _test_datasets
    expected = tm.ExtendedSeries([1], index=pd.to_datetime(['2020-01-01']))
    expected.dataset_ids = _test_datasets
    assert_series_equal(expected, actual, check_names=False)
    assert actual.dataset_ids == expected.dataset_ids

    d = {
        'effectiveTenor': ['1y', '2y', '3y', '4y'], 'swapRate': [1, 2, 3, 4],
        'assetId': ['MAEMPCXQG3T716EX', 'MAFRSWPAF5QPNTP2', 'MA88BXZ3TCTXTFW1', 'MAC4KAG9B9ZAZHFT']
    }

    df = pd.DataFrame(data=d, index=_index * 4)
    market_data_mock.return_value = df
    args['tenor_type'] = 'swap_tenor'

    args['tenor'] = '5yr'
    with pytest.raises(MqValueError):
        tm_rates.swap_term_structure(**args)
    args['tenor'] = '5y'

    market_data_mock.return_value = pd.DataFrame()
    df = pd.DataFrame(data=d, index=_index * 4)
    assert tm_rates.swap_term_structure(**args).empty

    market_data_mock.return_value = df
    with DataContext('2019-01-01', '2025-01-01'):
        actual = tm_rates.swap_term_structure(**args)
    actual.dataset_ids = _test_datasets
    expected = tm.ExtendedSeries([1, 2, 3, 4], index=pd.to_datetime(['2020-01-01', '2021-01-01', '2021-12-31',
                                                                     '2022-12-30']))
    expected.dataset_ids = _test_datasets
    assert_series_equal(expected, actual, check_names=False)
    assert actual.dataset_ids == expected.dataset_ids
    replace.restore()


def test_basis_swap_term_structure():
    replace = Replacer()
    range_mock = replace('gs_quant.timeseries.measures_rates._range_from_pricing_date', Mock())
    range_mock.return_value = [datetime.date(2019, 1, 1), datetime.date(2019, 1, 1)]

    args = dict(spread_benchmark_type=None, spread_tenor=None,
                reference_benchmark_type=None, reference_tenor=None, tenor_type=tm_rates._SwapTenorType.FORWARD_TENOR,
                tenor='0b', real_time=False)

    mock_nok = Currency('MA891', 'EGP')
    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'EGP'
    args['asset'] = mock_nok
    with pytest.raises(NotImplementedError):
        tm_rates.basis_swap_term_structure(**args)

    mock_usd = Currency('MAZ7RWC904JYHYPS', 'USD')
    args['asset'] = mock_usd
    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'USD'
    with pytest.raises(NotImplementedError):
        tm_rates.basis_swap_term_structure(..., '1y', real_time=True)

    args['spread_tenor'] = '5yr'
    with pytest.raises(MqValueError):
        tm_rates.basis_swap_term_structure(**args)
    args['spread_tenor'] = '3m'

    args['reference_tenor'] = '5yr'
    with pytest.raises(MqValueError):
        tm_rates.basis_swap_term_structure(**args)
    args['reference_tenor'] = '6m'

    args['tenor_type'] = 'expiry'
    with pytest.raises(MqValueError):
        tm_rates.basis_swap_term_structure(**args)
    args['tenor_type'] = 'forward_tenor'

    args['tenor'] = '5yr'
    with pytest.raises(MqValueError):
        tm_rates.basis_swap_term_structure(**args)
    args['tenor'] = None

    args['spread_benchmark_type'] = BenchmarkType.STIBOR
    with pytest.raises(MqValueError):
        tm_rates.basis_swap_term_structure(**args)
    args['spread_benchmark_type'] = BenchmarkType.LIBOR

    args['reference_benchmark_type'] = BenchmarkType.STIBOR
    with pytest.raises(MqValueError):
        tm_rates.basis_swap_term_structure(**args)
    args['reference_benchmark_type'] = BenchmarkType.LIBOR

    bd_mock = replace('gs_quant.data.dataset.Dataset.get_data', Mock())
    bd_mock.return_value = pd.DataFrame(data=dict(date="2020-04-10", exchange="NYC", description="Good Friday"),
                                        index=[pd.Timestamp('2020-04-10')])
    args['pricing_date'] = datetime.date(2020, 4, 10)
    with pytest.raises(MqValueError):
        tm_rates.basis_swap_term_structure(**args)
    args['pricing_date'] = None

    xrefs = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    xrefs.return_value = 'USD'
    identifiers_empty = replace('gs_quant.timeseries.measures.GsAssetApi.get_many_assets', Mock())
    identifiers_empty.return_value = {}
    with pytest.raises(MqValueError):
        tm_rates.basis_swap_term_structure(**args)

    identifiers = replace('gs_quant.timeseries.measures.GsAssetApi.get_many_assets', Mock())
    mock_asset = Currency('USD', name='USD')
    mock_asset.id = 'MAEMPCXQG3T716EX'
    mock_asset.exchange = 'OTC'
    identifiers.return_value = [mock_asset]

    d = {
        'terminationTenor': ['1y', '2y', '3y', '4y'], 'basisSwapRate': [1, 2, 3, 4],
        'assetId': ['MAEMPCXQG3T716EX', 'MAFRSWPAF5QPNTP2', 'MA88BXZ3TCTXTFW1', 'MAC4KAG9B9ZAZHFT']
    }

    pricing_date_mock = replace('gs_quant.timeseries.measures_rates._range_from_pricing_date', Mock())
    pricing_date_mock.return_value = [datetime.date(2019, 1, 1), datetime.date(2019, 1, 1)]
    bd_mock.return_value = pd.DataFrame()
    market_data_mock = replace('gs_quant.timeseries.measures_rates._market_data_timed', Mock())

    market_data_mock.return_value = pd.DataFrame()
    assert tm_rates.basis_swap_term_structure(**args).empty

    df = pd.DataFrame(data=d, index=_index * 4)
    market_data_mock.return_value = df
    with DataContext('2019-01-01', '2025-01-01'):
        actual = tm_rates.basis_swap_term_structure(**args)
    actual.dataset_ids = _test_datasets
    expected = tm.ExtendedSeries([1, 2, 3, 4], index=pd.to_datetime(['2020-01-01', '2021-01-01', '2021-12-31',
                                                                     '2022-12-30']))
    expected.dataset_ids = _test_datasets
    assert_series_equal(expected, actual, check_names=False)
    assert actual.dataset_ids == expected.dataset_ids

    d = {
        'effectiveTenor': ['1y', '2y', '3y', '4y'], 'basisSwapRate': [1, 2, 3, 4],
        'assetId': ['MAEMPCXQG3T716EX', 'MAFRSWPAF5QPNTP2', 'MA88BXZ3TCTXTFW1', 'MAC4KAG9B9ZAZHFT']
    }
    bd_mock.return_value = pd.DataFrame()
    market_data_mock = replace('gs_quant.timeseries.measures_rates._market_data_timed', Mock())

    df = pd.DataFrame(data=d, index=_index * 4)
    market_data_mock.return_value = df
    args['tenor_type'] = tm_rates._SwapTenorType.SWAP_TENOR
    args['tenor'] = '5y'
    with DataContext('2019-01-01', '2025-01-01'):
        actual = tm_rates.basis_swap_term_structure(**args)
    actual.dataset_ids = _test_datasets
    expected = tm.ExtendedSeries([1, 2, 3, 4], index=pd.to_datetime(['2020-01-01', '2021-01-01', '2021-12-31',
                                                                     '2022-12-30']))
    expected.dataset_ids = _test_datasets
    assert_series_equal(expected, actual, check_names=False)
    assert actual.dataset_ids == expected.dataset_ids

    df = pd.DataFrame(data={'effectiveTenor': ['1y'], 'basisSwapRate': [1], 'assetId': ['MAEMPCXQG3T716EX']},
                      index=_index)
    market_data_mock.return_value = df
    with DataContext('2019-01-01', '2025-01-01'):
        actual = tm_rates.basis_swap_term_structure(**args)
    actual.dataset_ids = _test_datasets
    expected = tm.ExtendedSeries([1], index=pd.to_datetime(['2020-01-01']))
    expected.dataset_ids = _test_datasets
    assert_series_equal(expected, actual, check_names=False)
    assert actual.dataset_ids == expected.dataset_ids
    replace.restore()


def test_cap_floor_vol():
    replace = Replacer()
    mock_usd = Currency('MA890', 'USD')
    xrefs = replace('gs_quant.timeseries.measures.GsAssetApi.get_asset_xrefs', Mock())
    xrefs.return_value = [GsTemporalXRef(dt.date(2019, 1, 1), dt.date(2952, 12, 31), XRef(bbid='USD', ))]
    identifiers = replace('gs_quant.timeseries.measures.GsAssetApi.map_identifiers', Mock())
    identifiers.return_value = {'USD-LIBOR-BBA': 'MA123'}
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_curr)
    actual = tm.cap_floor_vol(mock_usd, '5y', 50)
    assert_series_equal(pd.Series([1, 2, 3], index=_index * 3, name='capFloorVol'), pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    with pytest.raises(NotImplementedError):
        tm.cap_floor_vol(..., '5y', 50, real_time=True)
    replace.restore()


def test_cap_floor_atm_fwd_rate():
    replace = Replacer()
    mock_usd = Currency('MA890', 'USD')
    xrefs = replace('gs_quant.timeseries.measures.GsAssetApi.get_asset_xrefs', Mock())
    xrefs.return_value = [GsTemporalXRef(dt.date(2019, 1, 1), dt.date(2952, 12, 31), XRef(bbid='USD', ))]
    identifiers = replace('gs_quant.timeseries.measures.GsAssetApi.map_identifiers', Mock())
    identifiers.return_value = {'USD-LIBOR-BBA': 'MA123'}
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_curr)
    actual = tm.cap_floor_atm_fwd_rate(mock_usd, '5y')
    assert_series_equal(pd.Series([1, 2, 3], index=_index * 3, name='capFloorAtmFwdRate'), pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    with pytest.raises(NotImplementedError):
        tm.cap_floor_atm_fwd_rate(..., '5y', real_time=True)
    replace.restore()


def test_spread_option_vol():
    replace = Replacer()
    mock_usd = Currency('MA890', 'USD')
    xrefs = replace('gs_quant.timeseries.measures.GsAssetApi.get_asset_xrefs', Mock())
    xrefs.return_value = [GsTemporalXRef(dt.date(2019, 1, 1), dt.date(2952, 12, 31), XRef(bbid='USD', ))]
    identifiers = replace('gs_quant.timeseries.measures.GsAssetApi.map_identifiers', Mock())
    identifiers.return_value = {'USD-LIBOR-BBA': 'MA123'}
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_curr)
    actual = tm.spread_option_vol(mock_usd, '3m', '10y', '5y', 50)
    assert_series_equal(pd.Series([1, 2, 3], index=_index * 3, name='spreadOptionVol'), pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    with pytest.raises(NotImplementedError):
        tm.spread_option_vol(..., '3m', '10y', '5y', 50, real_time=True)
    replace.restore()


def test_spread_option_atm_fwd_rate():
    replace = Replacer()
    mock_usd = Currency('MA890', 'USD')
    xrefs = replace('gs_quant.timeseries.measures.GsAssetApi.get_asset_xrefs', Mock())
    xrefs.return_value = [GsTemporalXRef(dt.date(2019, 1, 1), dt.date(2952, 12, 31), XRef(bbid='USD', ))]
    identifiers = replace('gs_quant.timeseries.measures.GsAssetApi.map_identifiers', Mock())
    identifiers.return_value = {'USD-LIBOR-BBA': 'MA123'}
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_curr)
    actual = tm.spread_option_atm_fwd_rate(mock_usd, '3m', '10y', '5y')
    assert_series_equal(pd.Series([1, 2, 3], index=_index * 3, name='spreadOptionAtmFwdRate'), pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    with pytest.raises(NotImplementedError):
        tm.spread_option_atm_fwd_rate(..., '3m', '10y', '5y', real_time=True)
    replace.restore()


def test_zc_inflation_swap_rate():
    replace = Replacer()
    mock_gbp = Currency('MA890', 'GBP')
    xrefs = replace('gs_quant.timeseries.measures.GsAssetApi.get_asset_xrefs', Mock())
    xrefs.return_value = [GsTemporalXRef(dt.date(2019, 1, 1), dt.date(2952, 12, 31), XRef(bbid='GBP', ))]
    identifiers = replace('gs_quant.timeseries.measures.GsAssetApi.map_identifiers', Mock())
    identifiers.return_value = {'CPI-UKRPI': 'MA123'}
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_curr)
    actual = tm.zc_inflation_swap_rate(mock_gbp, '1y')
    assert_series_equal(pd.Series([1, 2, 3], index=_index * 3, name='inflationSwapRate'), pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    with pytest.raises(NotImplementedError):
        tm.zc_inflation_swap_rate(..., '1y', real_time=True)
    replace.restore()


def test_basis():
    replace = Replacer()
    mock_jpyusd = Cross('MA890', 'USD/JPY')
    xrefs = replace('gs_quant.timeseries.measures.GsAssetApi.get_asset_xrefs', Mock())
    xrefs.return_value = [GsTemporalXRef(dt.date(2019, 1, 1), dt.date(2952, 12, 31), XRef(bbid='JPYUSD', ))]
    identifiers = replace('gs_quant.timeseries.measures.GsAssetApi.map_identifiers', Mock())
    identifiers.return_value = {'USD-3m/JPY-3m': 'MA123'}
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_cross)
    actual = tm.basis(mock_jpyusd, '1y')
    assert_series_equal(pd.Series([1, 2, 3], index=_index * 3, name='basis'), pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    with pytest.raises(NotImplementedError):
        tm.basis(..., '1y', real_time=True)
    replace.restore()


def test_td():
    cases = {'3d': pd.DateOffset(days=3), '9w': pd.DateOffset(weeks=9), '2m': pd.DateOffset(months=2),
             '10y': pd.DateOffset(years=10)
             }
    for k, v in cases.items():
        actual = tm._to_offset(k)
        assert v == actual, f'expected {v}, got actual {actual}'

    with pytest.raises(ValueError):
        tm._to_offset('5z')


def test_pricing_range():
    import datetime

    given = datetime.date(2019, 4, 20)
    s, e = tm._range_from_pricing_date('NYSE', given)
    assert s == e == given

    class MockDate(datetime.date):
        @classmethod
        def today(cls):
            return cls(2019, 5, 25)

    # mock
    replace = Replacer()
    cbd = replace('gs_quant.timeseries.measures._get_custom_bd', Mock())
    cbd.return_value = pd.tseries.offsets.BusinessDay()
    today = replace('gs_quant.timeseries.measures.pd.Timestamp.today', Mock())
    today.return_value = pd.Timestamp(2019, 5, 25)
    gold = datetime.date
    datetime.date = MockDate

    # cases
    s, e = tm._range_from_pricing_date('ANY')
    assert s == pd.Timestamp(2019, 5, 24)
    assert e == pd.Timestamp(2019, 5, 24)

    s, e = tm._range_from_pricing_date('ANY', '3m')
    assert s == pd.Timestamp(2019, 2, 22)
    assert e == pd.Timestamp(2019, 2, 24)

    s, e = tm._range_from_pricing_date('ANY', '3b')
    assert s == e == pd.Timestamp(2019, 5, 22)

    # restore
    datetime.date = gold
    replace.restore()


def test_var_swap_tenors():
    session = GsSession.get(Environment.DEV, token='faux')

    replace = Replacer()
    get_mock = replace('gs_quant.session.GsSession._get', Mock())
    get_mock.return_value = {
        'data': [
            {
                'dataField': 'varSwap',
                'filteredFields': [
                    {
                        'field': 'tenor',
                        'values': ['abc', 'xyc']
                    }
                ]
            }
        ]
    }

    with session:
        actual = tm._var_swap_tenors(Index('MAXXX', AssetClass.Equity, 'XXX'))
    assert actual == ['abc', 'xyc']

    get_mock.return_value = {
        'data': []
    }
    with pytest.raises(MqError):
        with session:
            tm._var_swap_tenors(Index('MAXXX', AssetClass.Equity, 'XXX'))
    replace.restore()


def test_tenor_to_month():
    with pytest.raises(MqError):
        tm._tenor_to_month('1d')
    with pytest.raises(MqError):
        tm._tenor_to_month('2w')
    assert tm._tenor_to_month('3m') == 3
    assert tm._tenor_to_month('4y') == 48


def test_month_to_tenor():
    assert tm._month_to_tenor(36) == '3y'
    assert tm._month_to_tenor(18) == '18m'


def test_forward_var_term():
    idx = pd.DatetimeIndex([datetime.date(2020, 4, 1), datetime.date(2020, 4, 2)] * 6)
    data = {
        'varSwap': [1.1, 1, 2.1, 2, 3.1, 3, 4.1, 4, 5.1, 5, 6.1, 6],
        'tenor': ['1w', '1w', '1m', '1m', '5w', '5w', '2m', '2m', '3m', '3m', '5m', '5m']
    }
    out = MarketDataResponseFrame(data=data, index=idx)
    out.dataset_ids = _test_datasets

    replace = Replacer()
    market_mock = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    market_mock.return_value = out

    # Equity
    expected = pd.Series([np.nan, 5.29150, 6.55744], name='forwardVarTerm',
                         index=pd.DatetimeIndex(['2020-05-01', '2020-06-02', '2020-07-02'], name='expirationDate'))
    with DataContext('2020-01-01', '2020-07-31'):
        actual = tm.forward_var_term(Index('MA123', AssetClass.Equity, '123'), datetime.date(2020, 4, 2))
    assert_series_equal(expected, pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    market_mock.assert_called_once()

    # FX
    expected_fx = pd.Series([np.nan, 5.29150, 6.55744, 7.24569], name='forwardVarTerm',
                            index=pd.DatetimeIndex(['2020-05-01', '2020-06-02', '2020-07-02', '2020-09-02'],
                                                   name='expirationDate'))

    with DataContext('2020-01-01', '2020-09-02'):
        actual_fx = tm.forward_var_term(Cross('ABCDE', 'EURUSD'))
    assert_series_equal(expected_fx, pd.Series(actual_fx))
    assert actual_fx.dataset_ids == _test_datasets

    # no data
    market_mock.reset_mock()
    market_mock.return_value = mock_empty_market_data_response()
    actual = tm.forward_var_term(Index('MA123', AssetClass.Equity, '123'))
    assert actual.empty

    # real-time
    with pytest.raises(NotImplementedError):
        tm.forward_var_term(..., real_time=True)

    replace.restore()


def _mock_var_swap_data(_cls, q):
    queries = q.get('queries', [])
    if len(queries) > 0 and 'Last' in queries[0]['measures']:
        return MarketDataResponseFrame({'varSwap': [4]}, index=[pd.Timestamp('2019-01-04T12:00:00Z')])

    idx = pd.date_range(start="2019-01-01", periods=3, freq="D")
    data = {
        'varSwap': [1, 2, 3]
    }
    out = MarketDataResponseFrame(data=data, index=idx)
    out.dataset_ids = _test_datasets
    return out


def test_var_swap():
    replace = Replacer()
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', _mock_var_swap_data)

    expected = pd.Series([1, 2, 3, 4], name='varSwap', index=pd.date_range("2019-01-01", periods=4, freq="D"))
    expected.index.freq = None
    actual = tm.var_swap(Index('MA123', AssetClass.Equity, '123'), '1m')
    assert_series_equal(expected, pd.Series(actual))
    assert actual.dataset_ids == _test_datasets

    market_mock = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    market_mock.return_value = mock_empty_market_data_response()
    actual = tm.var_swap(Index('MA123', AssetClass.Equity, '123'), '1m')
    assert actual.empty
    replace.restore()


def _mock_var_swap_fwd(_cls, q):
    queries = q.get('queries', [])
    if len(queries) > 0 and 'Last' in queries[0]['measures']:
        return MarketDataResponseFrame({'varSwap': [4, 4.5], 'tenor': ['1y', '13m']},
                                       index=[pd.Timestamp('2019-01-04T12:00:00Z')] * 2)

    idx = pd.date_range(start="2019-01-01", periods=3, freq="D")
    d1 = {
        'varSwap': [1, 2, 3],
        'tenor': ['1y'] * 3
    }
    d2 = {
        'varSwap': [1.5, 2.5, 3.5],
        'tenor': ['13m'] * 3
    }
    df1 = MarketDataResponseFrame(data=d1, index=idx)
    df2 = MarketDataResponseFrame(data=d2, index=idx)
    out = pd.concat([df1, df2])
    out.dataset_ids = _test_datasets
    return out


def _mock_var_swap_1t(_cls, q):
    queries = q.get('queries', [])
    if len(queries) > 0 and 'Last' in queries[0]['measures']:
        return MarketDataResponseFrame({'varSwap': [4, 4.5], 'tenor': ['1y', '13m']},
                                       index=[pd.Timestamp('2019-01-04T12:00:00Z')])

    idx = pd.date_range(start="2019-01-01", periods=3, freq="D")
    d1 = {
        'varSwap': [1, 2, 3],
        'tenor': ['1y'] * 3
    }
    df1 = MarketDataResponseFrame(data=d1, index=idx)
    df1.dataset_ids = _test_datasets
    return df1


def test_var_swap_fwd():
    # bad input
    with pytest.raises(MqError):
        tm.var_swap(Index('MA123', AssetClass.Equity, '123'), '1m', 500)

    # regular
    replace = Replacer()
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', _mock_var_swap_fwd)

    tenors_mock = replace('gs_quant.timeseries.measures._var_swap_tenors', Mock())
    tenors_mock.return_value = ['1m', '1y', '13m']

    expected = pd.Series([4.1533, 5.7663, 7.1589, 8.4410], name='varSwap',
                         index=pd.date_range(start="2019-01-01", periods=4, freq="D"))
    expected.index.freq = None
    actual = tm.var_swap(Index('MA123', AssetClass.Equity, '123'), '1m', '1y')
    assert_series_equal(expected, pd.Series(actual))
    assert actual.dataset_ids == _test_datasets

    # no data
    market_mock = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    market_mock.return_value = mock_empty_market_data_response()
    actual = tm.var_swap(Index('MA123', AssetClass.Equity, '123'), '1m', '1y')
    assert actual.empty
    assert actual.dataset_ids == ()

    # no data for a tenor
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', _mock_var_swap_1t)
    actual = tm.var_swap(Index('MA123', AssetClass.Equity, '123'), '1m', '1y')
    assert actual.empty
    assert actual.dataset_ids == ()

    # no such tenors
    tenors_mock.return_value = []
    actual = tm.var_swap(Index('MA123', AssetClass.Equity, '123'), '1m', '1y')
    assert actual.empty
    assert actual.dataset_ids == ()

    # finish
    replace.restore()


def _var_term_typical():
    assert DataContext.current_is_set
    data = {
        'tenor': ['1w', '2w', '1y', '2y'],
        'varSwap': [1, 2, 3, 4]
    }
    out = MarketDataResponseFrame(data=data, index=pd.DatetimeIndex(['2018-01-01'] * 4))
    out.dataset_ids = _test_datasets

    replace = Replacer()
    market_mock = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    market_mock.side_effect = [pd.DataFrame(), out]

    actual = tm.var_term(Index('MA123', AssetClass.Equity, '123'))
    idx = pd.DatetimeIndex(['2018-01-08', '2018-01-15', '2019-01-01', '2020-01-01'], name='varSwap')
    expected = pd.Series([1, 2, 3, 4], name='varSwap', index=idx)
    expected = expected.loc[DataContext.current.start_date: DataContext.current.end_date]

    if expected.empty:
        assert actual.empty
    else:
        assert_series_equal(expected, pd.Series(actual), check_names=False)
        assert actual.dataset_ids == _test_datasets

    replace.restore()

    return actual


def _var_term_empty():
    replace = Replacer()
    market_mock = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    market_mock.return_value = mock_empty_market_data_response()

    actual = tm.var_term(Index('MAXYZ', AssetClass.Equity, 'XYZ'))
    assert actual.empty
    assert actual.dataset_ids == ()
    replace.restore()


def _var_term_fwd():
    idx = pd.date_range('2018-01-01', periods=2, freq='D')

    def mock_var_swap(_asset, tenor, _forward_start_date, **_kwargs):
        if tenor == '1m':
            series = tm.ExtendedSeries([1, 2], idx, name='varSwap')
            series.dataset_ids = _test_datasets
        elif tenor == '2m':
            series = tm.ExtendedSeries([3, 4], idx, name='varSwap')
            series.dataset_ids = _test_datasets
        else:
            series = tm.ExtendedSeries()
            series.dataset_ids = ()
        return series

    replace = Replacer()
    market_mock = replace('gs_quant.timeseries.measures.var_swap', Mock())
    market_mock.side_effect = mock_var_swap
    tenors_mock = replace('gs_quant.timeseries.measures._var_swap_tenors', Mock())
    tenors_mock.return_value = ['1m', '2m', '3m']

    actual = tm.var_term(Index('MA123', AssetClass.Equity, '123'), forward_start_date='1m')
    idx = pd.DatetimeIndex(['2018-02-02', '2018-03-02'], name='varSwap')
    expected = pd.Series([2, 4], name='varSwap', index=idx)
    expected = expected.loc[DataContext.current.start_date: DataContext.current.end_date]

    if expected.empty:
        assert actual.empty
    else:
        assert_series_equal(expected, pd.Series(actual), check_names=False)
        assert actual.dataset_ids == _test_datasets
    market_mock.assert_called()

    replace.restore()
    return actual


def _var_term_latest():
    assert DataContext.current_is_set
    data = {
        'tenor': ['1w', '2w', '1y', '2y', '1w', '2w', '1y', '2y'],
        'varSwap': [10, 20, 30, 40, 1, 2, 3, 4]
    }
    out = MarketDataResponseFrame(data=data, index=pd.date_range("2018-01-01", periods=8, freq="min"))
    out.dataset_ids = _test_datasets

    replace = Replacer()
    market_mock = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    market_mock.side_effect = [out.iloc[-1:], out]

    actual = tm.var_term(Index('MA123', AssetClass.Equity, '123'))
    idx = pd.DatetimeIndex(['2018-01-08', '2018-01-15', '2019-01-01', '2020-01-01'], name='expirationDate')
    expected = pd.Series([1, 2, 3, 4], name='varSwap', index=idx)
    expected = expected.loc[DataContext.current.start_date: DataContext.current.end_date]

    if expected.empty:
        assert actual.empty
    else:
        assert_series_equal(expected, pd.Series(actual))
        assert actual.dataset_ids == _test_datasets

    replace.restore()


def test_var_term():
    with DataContext('2018-01-01', '2019-01-01'):
        _var_term_typical()
        _var_term_empty()
        _var_term_fwd()
        _var_term_latest()
    with DataContext('2019-01-01', '2019-07-04'):
        _var_term_fwd()
    with DataContext('2018-01-16', '2018-12-31'):
        out = _var_term_typical()
        assert out.empty
        assert out.dataset_ids == _test_datasets
    with pytest.raises(MqError):
        tm.var_term(..., pricing_date=300)
    with pytest.raises(NotImplementedError):
        tm.var_term(..., real_time=True)


def _mock_forward_helper():
    idx = pd.DatetimeIndex([datetime.date(2020, 5, 1), datetime.date(2020, 5, 2)] * 4)
    data = {
        'impliedVolatility': [2.1, 2, 3.1, 3, 4.1, 4, 5.1, 5],
        'tenor': ['1m', '1m', '2m', '2m', '3m', '3m', '4m', '4m']
    }
    out = MarketDataResponseFrame(data=data, index=idx)
    out.dataset_ids = _test_datasets
    return out


def _mock_forward_vol_data(_cls, q):
    queries = q.get('queries', [])
    if len(queries) > 0 and 'Last' in queries[0]['measures']:
        return MarketDataResponseFrame()

    return _mock_forward_helper()


def _mock_forward_vol_data_with_last(_cls, q):
    queries = q.get('queries', [])
    if len(queries) > 0 and 'Last' in queries[0]['measures']:
        idx = [pd.Timestamp('2020-05-03T12:00:00Z')] * 4
        data = {
            'impliedVolatility': [2, 3, 4, 5],
            'tenor': ['1m', '2m', '3m', '4m']
        }
        ids = _test_datasets_rt
        out = MarketDataResponseFrame(data=data, index=idx)
        out.dataset_ids = ids
        return out

    return _mock_forward_helper()


def _mock_forward_vol_data_error(_cls, q):
    queries = q.get('queries', [])
    if len(queries) > 0 and 'Last' in queries[0]['measures']:
        raise MqValueError('something happened')

    return _mock_forward_helper()


def test_forward_vol():
    idx = pd.DatetimeIndex([datetime.date(2020, 5, 1), datetime.date(2020, 5, 2)] * 4)
    data = {
        'impliedVolatility': [2.1, 2, 3.1, 3, 4.1, 4, 5.1, 5],
        'tenor': ['1m', '1m', '2m', '2m', '3m', '3m', '4m', '4m']
    }
    out = MarketDataResponseFrame(data=data, index=idx)
    out.dataset_ids = _test_datasets

    replace = Replacer()
    market_mock = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    market_mock.side_effect = _mock_forward_vol_data

    # Equity
    expected = pd.Series([5.58659, 5.47723], name='forwardVol',
                         index=pd.to_datetime(['2020-05-01', '2020-05-02']))
    with DataContext('2020-01-01', '2020-09-01'):
        actual = tm.forward_vol(Index('MA123', AssetClass.Equity, '123'), '1m', '2m', tm.VolReference.SPOT, 100)
    assert_series_equal(expected, pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    market_mock.assert_called_once()

    # FX
    cross_mock = replace('gs_quant.timeseries.measures.cross_stored_direction_for_fx_vol', Mock())
    cross_mock.return_value = 'EURUSD'

    with DataContext('2020-01-01', '2020-09-01'):
        actual_fx = tm.forward_vol(Cross('ABCDE', 'EURUSD'), '1m', '2m', tm.VolReference.SPOT, 100)
    assert_series_equal(expected, pd.Series(actual_fx))
    assert actual_fx.dataset_ids == _test_datasets

    # EQ with last
    market_mock.reset_mock()
    market_mock.side_effect = _mock_forward_vol_data_with_last
    expected = pd.Series([5.58659, 5.47723, 5.47723], name='forwardVol',
                         index=pd.to_datetime(['2020-05-01', '2020-05-02', '2020-05-03']))
    actual = tm.forward_vol(Index('MA123', AssetClass.Equity, '123'), '1m', '2m', tm.VolReference.SPOT, 100)
    assert_series_equal(expected, pd.Series(actual))
    for t in _test_datasets + _test_datasets_rt:
        assert t in actual.dataset_ids
    assert market_mock.call_count == 2

    # EQ with exception on last
    market_mock.reset_mock()
    market_mock.side_effect = _mock_forward_vol_data_error
    expected = pd.Series([5.58659, 5.47723], name='forwardVol',
                         index=pd.to_datetime(['2020-05-01', '2020-05-02']))
    actual = tm.forward_vol(Index('MA123', AssetClass.Equity, '123'), '1m', '2m', tm.VolReference.SPOT, 100)
    assert_series_equal(expected, pd.Series(actual))
    assert market_mock.call_count == 2

    # no data
    market_mock = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    market_mock.return_value = mock_empty_market_data_response()
    actual = tm.forward_vol(Index('MA123', AssetClass.Equity, '123'), '1m', '2m', tm.VolReference.SPOT, 100)
    assert actual.empty

    # no data for required tenor
    market_mock.reset_mock()
    market_mock.return_value = MarketDataResponseFrame(data={'impliedVolatility': [2.1, 3.1, 5.1],
                                                             'tenor': ['1m', '2m', '4m']},
                                                       index=[datetime.date(2020, 5, 1)] * 3)
    with DataContext('2020-01-01', '2020-09-01'):
        actual = tm.forward_vol(Index('MA123', AssetClass.Equity, '123'), '1m', '2m', tm.VolReference.SPOT, 100)
    assert actual.empty

    # real-time
    with pytest.raises(NotImplementedError):
        tm.forward_vol(..., '1m', '2m', tm.VolReference.SPOT, 100, real_time=True)

    replace.restore()


def test_forward_vol_term():
    idx = pd.DatetimeIndex([datetime.date(2020, 4, 1), datetime.date(2020, 4, 2)] * 6)
    data = {
        'impliedVolatility': [1.1, 1, 2.1, 2, 3.1, 3, 4.1, 4, 5.1, 5, 6.1, 6],
        'tenor': ['1w', '1w', '1m', '1m', '5w', '5w', '2m', '2m', '3m', '3m', '5m', '5m']
    }
    out = MarketDataResponseFrame(data=data, index=idx)
    out.dataset_ids = _test_datasets

    replace = Replacer()
    market_mock = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    market_mock.return_value = out

    # Equity
    expected = pd.Series([np.nan, 5.29150, 6.55744], name='forwardVolTerm',
                         index=pd.DatetimeIndex(['2020-05-01', '2020-06-02', '2020-07-02'], name='expirationDate'))
    with DataContext('2020-01-01', '2020-07-31'):
        actual = tm.forward_vol_term(Index('MA123', AssetClass.Equity, '123'), tm.VolReference.SPOT, 100,
                                     datetime.date(2020, 4, 2))
    assert_series_equal(expected, pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    market_mock.assert_called_once()

    # FX
    cross_mock = replace('gs_quant.timeseries.measures.cross_stored_direction_for_fx_vol', Mock())
    cross_mock.return_value = 'EURUSD'
    expected_fx = pd.Series([np.nan, 5.29150, 6.55744, 7.24569], name='forwardVolTerm',
                            index=pd.DatetimeIndex(['2020-05-01', '2020-06-02', '2020-07-02', '2020-09-02'],
                                                   name='expirationDate'))

    with DataContext('2020-01-01', '2020-09-02'):
        actual_fx = tm.forward_vol_term(Cross('ABCDE', 'EURUSD'), tm.VolReference.SPOT, 100)
    assert_series_equal(expected_fx, pd.Series(actual_fx))
    assert actual_fx.dataset_ids == _test_datasets

    # no data
    market_mock.reset_mock()
    market_mock.return_value = mock_empty_market_data_response()
    actual = tm.forward_vol_term(Index('MA123', AssetClass.Equity, '123'), tm.VolReference.SPOT, 100)
    assert actual.empty

    # real-time
    with pytest.raises(NotImplementedError):
        tm.forward_vol_term(..., tm.VolReference.SPOT, 100, real_time=True)

    replace.restore()


def _vol_term_typical(reference, value):
    assert DataContext.current_is_set
    data = {
        'tenor': ['1w', '2w', '1y', '2y'],
        'impliedVolatility': [1, 2, 3, 4]
    }
    out = MarketDataResponseFrame(data=data, index=pd.DatetimeIndex(['2018-01-01'] * 4))
    out.dataset_ids = _test_datasets

    data_expiry = {
        'expirationDate': ['2018-01-06', '2018-01-08'],
        'impliedVolatilityByExpiration': [1.2, 1.1]
    }
    out_expiry = MarketDataResponseFrame(data=data_expiry, index=pd.DatetimeIndex(['2018-01-01'] * 2))
    out_expiry.dataset_ids = _test_datasets2

    replace = Replacer()
    market_mock = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    market_mock.side_effect = [pd.DataFrame(), pd.DataFrame(), out, out_expiry]

    actual = tm.vol_term(Index('MA123', AssetClass.Equity, '123'), reference, value)
    idx = pd.DatetimeIndex(['2018-01-06', '2018-01-08', '2018-01-15', '2019-01-01', '2020-01-01'],
                           name='expirationDate')
    expected = pd.Series([1.2, 1, 2, 3, 4], name='impliedVolatility', index=idx)
    expected = expected.loc[DataContext.current.start_date: DataContext.current.end_date]

    if expected.empty:
        assert actual.empty
    else:
        assert_series_equal(expected, pd.Series(actual))
        assert set(actual.dataset_ids) == set(_test_datasets + _test_datasets2)

    replace.restore()
    return actual


def _vol_term_empty():
    replace = Replacer()
    market_mock = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    market_mock.return_value = pd.DataFrame()

    mock = replace('gs_quant.timeseries.measures.get_df_with_retries', Mock())
    mock.return_value = MarketDataResponseFrame()

    actual = tm.vol_term(Index('MAXYZ', AssetClass.Equity, 'XYZ'), tm.VolReference.DELTA_CALL, 777)
    assert actual.empty
    assert actual.dataset_ids == ()
    replace.restore()


def _vol_term_latest():
    assert DataContext.current_is_set
    data = {
        'tenor': ['1w', '2w', '1y', '2y', '1w', '2w', '1y', '2y'],
        'impliedVolatility': [10, 20, 30, 40, 1, 2, 3, 4]
    }
    out = MarketDataResponseFrame(data=data, index=pd.date_range("2018-01-01", periods=8, freq="min"))
    out.dataset_ids = _test_datasets

    replace = Replacer()
    market_mock = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    market_mock.side_effect = [out.iloc[-1:], out, pd.DataFrame(), pd.DataFrame()]

    actual = tm.vol_term(Index('MA123', AssetClass.Equity, '123'), tm.VolReference.SPOT, 100)
    idx = pd.DatetimeIndex(['2018-01-08', '2018-01-15', '2019-01-01', '2020-01-01'], name='expirationDate')
    expected = pd.Series([1, 2, 3, 4], name='impliedVolatility', index=idx)
    expected = expected.loc[DataContext.current.start_date: DataContext.current.end_date]

    if expected.empty:
        assert actual.empty
    else:
        assert_series_equal(expected, pd.Series(actual))
        assert actual.dataset_ids == _test_datasets

    replace.restore()
    return actual


def test_vol_term():
    with DataContext('2018-01-01', '2019-01-01'):
        _vol_term_typical(tm.VolReference.SPOT, 100)
        _vol_term_typical(tm.VolReference.NORMALIZED, 4)
        _vol_term_typical(tm.VolReference.DELTA_PUT, 50)
        _vol_term_empty()
        _vol_term_latest()
    with DataContext('2018-01-16', '2018-12-31'):
        out = _vol_term_typical(tm.VolReference.SPOT, 100)
        assert out.empty
        assert set(out.dataset_ids) == set(_test_datasets + _test_datasets2)
    with pytest.raises(NotImplementedError):
        tm.vol_term(..., tm.VolReference.SPOT, 100, real_time=True)
    with pytest.raises(MqError):
        tm.vol_term(Index('MA123', AssetClass.Equity, '123'), tm.VolReference.DELTA_NEUTRAL, 0)
    with DataContext('2020-01-01', '2021-01-01'):
        with pytest.raises(MqError, match='forward looking date range'):
            tm.vol_term(Index('MA123', AssetClass.Equity, '123'), tm.VolReference.SPOT, 100, source='plottool')
    with DataContext(datetime.date.today(), datetime.date.today()):
        with pytest.raises(MqError, match='forward looking date range'):
            tm.vol_term(Index('MA123', AssetClass.Equity, '123'), tm.VolReference.SPOT, 100, source='plottool')


def _vol_term_fx(reference, value):
    assert DataContext.current_is_set
    data = {
        'tenor': ['1w', '2w', '1y', '2y'],
        'impliedVolatility': [1, 2, 3, 4]
    }
    out = MarketDataResponseFrame(data=data, index=pd.DatetimeIndex(['2018-01-01'] * 4))
    out.dataset_ids = _test_datasets

    data_expiry = {
        'expirationDate': ['2018-01-06', '2018-01-08'],
        'impliedVolatilityByExpiration': [1.2, 1.1]
    }
    out_expiry = MarketDataResponseFrame(data=data_expiry, index=pd.DatetimeIndex(['2018-01-01'] * 2))
    out_expiry.dataset_ids = _test_datasets2

    replace = Replacer()
    market_mock = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    market_mock.side_effect = [out, out_expiry]
    cross_mock = replace('gs_quant.timeseries.measures.cross_stored_direction_for_fx_vol', Mock())
    cross_mock.return_value = 'EURUSD'

    actual = tm.vol_term(Cross('ABCDE', 'EURUSD'), reference, value)
    idx = pd.DatetimeIndex(['2018-01-06', '2018-01-08', '2018-01-15', '2019-01-01', '2020-01-01'],
                           name='expirationDate')
    expected = pd.Series([1.2, 1, 2, 3, 4], name='impliedVolatility', index=idx)
    expected = expected.loc[DataContext.current.start_date: DataContext.current.end_date]

    if expected.empty:
        assert actual.empty
    else:
        assert_series_equal(expected, pd.Series(actual))
        assert set(actual.dataset_ids) == set(_test_datasets + _test_datasets2)

    replace.restore()
    return actual


def _vol_term_fx_no_expiry(reference, value):
    assert DataContext.current_is_set
    data = {
        'tenor': ['1w', '2w', '1y', '2y'],
        'impliedVolatility': [1, 2, 3, 4]
    }
    out = MarketDataResponseFrame(data=data, index=pd.DatetimeIndex(['2018-01-01'] * 4))
    out.dataset_ids = _test_datasets

    replace = Replacer()
    market_mock = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    market_mock.side_effect = [out, MqValueError('a')]
    cross_mock = replace('gs_quant.timeseries.measures.cross_stored_direction_for_fx_vol', Mock())
    cross_mock.return_value = 'EURUSD'

    actual = tm.vol_term(Cross('ABCDE', 'EURUSD'), reference, value)
    idx = pd.DatetimeIndex(['2018-01-08', '2018-01-15', '2019-01-01'],
                           name='expirationDate')
    expected = pd.Series([1, 2, 3], name='impliedVolatility', index=idx)
    expected = expected.loc[DataContext.current.start_date: DataContext.current.end_date]

    if expected.empty:
        assert actual.empty
    else:
        assert_series_equal(expected, pd.Series(actual))
        assert actual.dataset_ids == _test_datasets

    replace.restore()
    return actual


def test_vol_term_fx():
    with pytest.raises(MqError):
        tm.vol_term(Cross('MABLUE', 'BLUE'), tm.VolReference.SPOT, 50)
    with pytest.raises(MqError):
        tm.vol_term(Cross('MABLUE', 'BLUE'), tm.VolReference.NORMALIZED, 1)
    with pytest.raises(MqError):
        tm.vol_term(Cross('MABLUE', 'BLUE'), tm.VolReference.DELTA_NEUTRAL, 1)
    with DataContext('2018-01-01', '2019-01-01'):
        _vol_term_fx(tm.VolReference.DELTA_CALL, 50)
    with DataContext('2018-01-01', '2019-01-01'):
        _vol_term_fx(tm.VolReference.DELTA_PUT, 50)
    with DataContext('2018-01-01', '2019-01-01'):
        _vol_term_fx_no_expiry(tm.VolReference.DELTA_PUT, 50)


def _fwd_term_typical():
    assert DataContext.current_is_set
    data = {
        'tenor': ['1w', '2w', '1y', '2y'],
        'forward': [1, 2, 3, 4]
    }
    out = MarketDataResponseFrame(data=data, index=pd.DatetimeIndex(['2018-01-01'] * 4))
    out.dataset_ids = _test_datasets

    replace = Replacer()
    market_mock = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    market_mock.return_value = out

    actual = tm.fwd_term(Index('MA123', AssetClass.Equity, '123'))
    idx = pd.DatetimeIndex(['2018-01-08', '2018-01-15', '2019-01-01', '2020-01-01'], name='expirationDate')
    expected = pd.Series([1, 2, 3, 4], name='forward', index=idx)
    expected = expected.loc[DataContext.current.start_date: DataContext.current.end_date]

    if expected.empty:
        assert actual.empty
    else:
        assert_series_equal(expected, pd.Series(actual))
        assert actual.dataset_ids == _test_datasets
    market_mock.assert_called_once()
    replace.restore()
    return actual


def _fwd_term_empty():
    replace = Replacer()
    market_mock = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    market_mock.return_value = mock_empty_market_data_response()

    actual = tm.fwd_term(Index('MAXYZ', AssetClass.Equity, 'XYZ'))
    assert actual.empty
    assert actual.dataset_ids == ()
    market_mock.assert_called_once()
    replace.restore()


def test_fwd_term():
    with DataContext('2018-01-01', '2019-01-01'):
        _fwd_term_typical()
        _fwd_term_empty()
    with DataContext('2018-01-16', '2018-12-31'):
        out = _fwd_term_typical()
        assert out.empty
        assert out.dataset_ids == _test_datasets
    with pytest.raises(NotImplementedError):
        tm.fwd_term(..., real_time=True)


def test_bucketize_price():
    target = {
        '7x24': [27.323461],
        'offpeak': [26.004816],
        'peak': [27.982783],
        '7x8': [26.004816],
        '2x16h': [],
        'monthly': [],
        'CAISO 7x24': [26.953743375],
        'CAISO peak': [29.547952562499997],
        'MISO 7x24': [27.076390749999998],
        'MISO offpeak': [25.263605624999997],
    }

    replace = Replacer()
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_commod)
    mock_pjm = Index('MA001', AssetClass.Commod, 'PJM')
    mock_caiso = Index('MA002', AssetClass.Commod, 'CAISO')
    mock_miso = Index('MA003', AssetClass.Commod, 'MISO')

    with DataContext(datetime.date(2019, 5, 1), datetime.date(2019, 5, 1)):
        bbid_mock = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
        bbid_mock.return_value = 'MISO'

        actual = tm.bucketize_price(mock_miso, 'LMP', bucket='7x24')
        assert_series_equal(pd.Series(target['MISO 7x24'],
                                      index=[datetime.date(2019, 5, 1)],
                                      name='price'),
                            pd.Series(actual))

        actual = tm.bucketize_price(mock_miso, 'LMP', bucket='offpeak')
        assert_series_equal(pd.Series(target['MISO offpeak'],
                                      index=[datetime.date(2019, 5, 1)],
                                      name='price'),
                            pd.Series(actual))

        bbid_mock.return_value = 'CAISO'

        actual = tm.bucketize_price(mock_caiso, 'LMP', bucket='7x24')
        assert_series_equal(pd.Series(target['CAISO 7x24'],
                                      index=[datetime.date(2019, 5, 1)],
                                      name='price'),
                            pd.Series(actual))

        actual = tm.bucketize_price(mock_caiso, 'LMP', bucket='peak')
        assert_series_equal(pd.Series(target['CAISO peak'],
                                      index=[datetime.date(2019, 5, 1)],
                                      name='price'),
                            pd.Series(actual))

        bbid_mock.return_value = 'PJM'

        actual = tm.bucketize_price(mock_pjm, 'LMP', bucket='7x24')
        assert_series_equal(pd.Series(target['7x24'],
                                      index=[datetime.date(2019, 5, 1)],
                                      name='price'),
                            pd.Series(actual))

        actual = tm.bucketize_price(mock_pjm, 'LMP', bucket='offpeak')
        assert_series_equal(pd.Series(target['offpeak'],
                                      index=[datetime.date(2019, 5, 1)],
                                      name='price'),
                            pd.Series(actual))

        actual = tm.bucketize_price(mock_pjm, 'LMP', bucket='peak')
        assert_series_equal(pd.Series(target['peak'],
                                      index=[datetime.date(2019, 5, 1)],
                                      name='price'),
                            pd.Series(actual))

        actual = tm.bucketize_price(mock_pjm, 'LMP', bucket='7x8')
        assert_series_equal(pd.Series(target['7x8'],
                                      index=[datetime.date(2019, 5, 1)],
                                      name='price'),
                            pd.Series(actual))

        actual = tm.bucketize_price(mock_pjm, 'LMP', bucket='2x16h')
        assert_series_equal(pd.Series(target['2x16h'],
                                      index=[],
                                      name='price'),
                            pd.Series(actual))

        actual = tm.bucketize_price(mock_pjm, 'LMP', granularity='m', bucket='7X24')
        assert_series_equal(pd.Series(target['monthly'],
                                      index=[],
                                      name='price'),
                            pd.Series(actual))

        with pytest.raises(ValueError):
            tm.bucketize_price(mock_pjm, 'LMP', bucket='7X24', real_time=True)

        with pytest.raises(ValueError):
            tm.bucketize_price(mock_pjm, 'LMP', bucket='weekday')

        with pytest.raises(ValueError):
            tm.bucketize_price(mock_caiso, 'LMP', bucket='weekday')

        with pytest.raises(ValueError):
            tm.bucketize_price(mock_pjm, 'LMP', granularity='yearly')

    replace.restore()

    # No market data
    market_mock = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    market_mock.return_value = mock_empty_market_data_response()
    with DataContext(datetime.date(2019, 1, 2), datetime.date(2019, 1, 2)):
        bbid_mock = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
        bbid_mock.return_value = 'MISO'
        actual = tm.bucketize_price(mock_miso, 'LMP', bucket='7x24')
        assert_series_equal(pd.Series(dtype='float64'), pd.Series(actual))

    # Duplicate data in dataset
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_commod_dup)
    with DataContext(datetime.date(2019, 1, 2), datetime.date(2019, 1, 2)):
        bbid_mock = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
        bbid_mock.return_value = 'MISO'
        with pytest.raises(ValueError):
            tm.bucketize_price(mock_miso, 'LMP', bucket='peak')

    replace.restore()


def test_forward_price():
    # US Power
    target = {
        '7x24': [19.46101],
        'peak': [23.86745],
        'J20 7x24': [18.11768888888889],
        'J20-K20 7x24': [19.283921311475414],
        'J20-K20 offpeak': [15.82870707070707],
        'J20-K20 7x8': [13.020144262295084],
    }
    replace = Replacer()
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_forward_price)
    mock_spp = Index('MA001', AssetClass.Commod, 'SPP')

    with DataContext(datetime.date(2019, 1, 2), datetime.date(2019, 1, 2)):
        bbid_mock = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
        bbid_mock.return_value = 'SPP'

        # Should return empty series as mark for '7x8' bucket is missing
        actual = tm.forward_price(mock_spp,
                                  price_method='LMP',
                                  contract_range='2Q20',
                                  bucket='7x24'
                                  )
        assert_series_equal(pd.Series(target['7x24'],
                                      index=[datetime.date(2019, 1, 2)],
                                      name='price'),
                            pd.Series(actual))

        actual = tm.forward_price(mock_spp,
                                  price_method='LMP',
                                  contract_range='J20',
                                  bucket='7x24'
                                  )
        assert_series_equal(pd.Series(target['J20 7x24'],
                                      index=[datetime.date(2019, 1, 2)],
                                      name='price'),
                            pd.Series(actual))

        actual = tm.forward_price(mock_spp,
                                  price_method='LMP',
                                  contract_range='2Q20',
                                  bucket='PEAK'
                                  )
        assert_series_equal(pd.Series(target['peak'],
                                      index=[datetime.date(2019, 1, 2)],
                                      name='price'),
                            pd.Series(actual))

        actual = tm.forward_price(mock_spp,
                                  price_method='LMP',
                                  contract_range='J20-K20',
                                  bucket='7x24'
                                  )
        assert_series_equal(pd.Series(target['J20-K20 7x24'],
                                      index=[datetime.date(2019, 1, 2)],
                                      name='price'),
                            pd.Series(actual))

        actual = tm.forward_price(mock_spp,
                                  price_method='LMP',
                                  contract_range='J20-K20',
                                  bucket='offpeak'
                                  )
        assert_series_equal(pd.Series(target['J20-K20 offpeak'],
                                      index=[datetime.date(2019, 1, 2)],
                                      name='price'),
                            pd.Series(actual))

        actual = tm.forward_price(mock_spp,
                                  price_method='LMP',
                                  contract_range='J20-K20',
                                  bucket='7x8'
                                  )
        assert_series_equal(pd.Series(target['J20-K20 7x8'],
                                      index=[datetime.date(2019, 1, 2)],
                                      name='price'),
                            pd.Series(actual))

        actual = tm.forward_price(mock_spp,
                                  price_method='lmp',
                                  contract_range='2Q20',
                                  bucket='7x24'
                                  )
        assert_series_equal(pd.Series(target['7x24'],
                                      index=[datetime.date(2019, 1, 2)],
                                      name='price'),
                            pd.Series(actual)
                            )

        with pytest.raises(ValueError):
            tm.forward_price(mock_spp,
                             price_method='LMP',
                             contract_range='5Q20',
                             bucket='PEAK'
                             )

        with pytest.raises(ValueError):
            tm.forward_price(mock_spp,
                             price_method='LMP',
                             contract_range='Invalid',
                             bucket='PEAK'
                             )

        with pytest.raises(ValueError):
            tm.forward_price(mock_spp,
                             price_method='LMP',
                             contract_range='3H20',
                             bucket='7x24'
                             )

        with pytest.raises(ValueError):
            tm.forward_price(mock_spp,
                             price_method='LMP',
                             contract_range='F20-I20',
                             bucket='7x24'
                             )

        with pytest.raises(ValueError):
            tm.forward_price(mock_spp,
                             price_method='LMP',
                             contract_range='2H20',
                             bucket='7x24',
                             real_time=True
                             )

        replace.restore()

        replace = Replacer()
        replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_missing_bucket_forward_price)
        bbid_mock = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
        bbid_mock.return_value = 'SPP'

        actual = tm.forward_price(mock_spp,
                                  price_method='LMP',
                                  contract_range='2Q20',
                                  bucket='7x24'
                                  )

        assert_series_equal(pd.Series(), pd.Series(actual), check_names=False)

        actual = tm.forward_price(mock_spp,
                                  price_method='LMP',
                                  contract_range='2Q20',
                                  bucket='PEAK'
                                  )
        assert_series_equal(pd.Series(target['peak'],
                                      index=[datetime.date(2019, 1, 2)],
                                      name='price'),
                            pd.Series(actual))

        actual = tm.forward_price(mock_spp,
                                  price_method='LMP',
                                  contract_range='J20-K20',
                                  bucket='7x24'
                                  )
        assert_series_equal(pd.Series(target['J20-K20 7x24'],
                                      index=[datetime.date(2019, 1, 2)],
                                      name='price'),
                            pd.Series(actual))
        replace.restore()

        # No market data
        market_mock = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
        market_mock.return_value = mock_empty_market_data_response()
        bbid_mock = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
        bbid_mock.return_value = 'SPP'
        with DataContext(datetime.date(2019, 1, 2), datetime.date(2019, 1, 2)):
            actual = tm.forward_price(mock_spp,
                                      price_method='LMP',
                                      contract_range='2Q20',
                                      bucket='7x24'
                                      )
            assert_series_equal(pd.Series(dtype='float64'), pd.Series(actual))
        replace.restore()

        # Query for asset with no bbid
        replace = Replacer()
        replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_forward_price)
        mock_ice = CommodityPowerAggregatedNodes('MA001', 'ICE Mid C')

        with DataContext(datetime.date(2019, 1, 2), datetime.date(2019, 1, 2)):
            bbId_mock = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
            bbId_mock.return_value = None
            ISO_mock = replace('gs_quant.timeseries.measures.Asset.get_entity', Mock())
            ISO_mock.return_value = {'parameters': {'ISO': 'PJM'}}

            # Should work as other usecases where assetId has bbid
            actual = tm.forward_price(mock_ice,
                                      price_method='LMP',
                                      contract_range='2Q20',
                                      bucket='7x24'
                                      )
            assert_series_equal(pd.Series(target['7x24'],
                                          index=[datetime.date(2019, 1, 2)],
                                          name='price'),
                                pd.Series(actual))
        replace.restore()


def test_implied_volatility_elec():
    # US Power
    target = {
        '7x24': [0.403352],
        'peak': [0.383025],
        'J20 7x24': [0.372178],
        'J20-K20 7x24': [0.3737661202185792],
        'J20-K20 offpeak': [0.3922989898989899],
        'J20-K20 7x8': [0.4322360655737705],
    }
    replace = Replacer()
    mock_get_data = replace('gs_quant.data.dataset.Dataset.get_data', Mock())
    mock_get_data.return_value = mock_implied_volatility_elec()
    mock_spp = Index('MA001', AssetClass.Commod, 'SPP')

    with DataContext(datetime.date(2019, 1, 2), datetime.date(2019, 1, 2)):
        bbid_mock = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
        bbid_mock.return_value = 'SPP'

        # Should return empty series as mark for '7x8' bucket is missing
        actual = tm.implied_volatility_elec(mock_spp,
                                            price_method='LMP',
                                            contract_range='2Q20',
                                            bucket='7x24'
                                            )
        assert_series_equal(pd.Series(target['7x24'],
                                      index=[datetime.date(2019, 1, 2)],
                                      name='price'),
                            pd.Series(actual)
                            )

        actual = tm.implied_volatility_elec(mock_spp,
                                            price_method='LMP',
                                            contract_range='J20',
                                            bucket='7x24'
                                            )
        assert_series_equal(pd.Series(target['J20 7x24'],
                                      index=[datetime.date(2019, 1, 2)],
                                      name='price'),
                            pd.Series(actual)
                            )

        actual = tm.implied_volatility_elec(mock_spp,
                                            price_method='LMP',
                                            contract_range='2Q20',
                                            bucket='PEAK'
                                            )
        assert_series_equal(pd.Series(target['peak'],
                                      index=[datetime.date(2019, 1, 2)],
                                      name='price'),
                            pd.Series(actual)
                            )

        actual = tm.implied_volatility_elec(mock_spp,
                                            price_method='LMP',
                                            contract_range='J20-K20',
                                            bucket='7x24'
                                            )
        assert_series_equal(pd.Series(target['J20-K20 7x24'],
                                      index=[datetime.date(2019, 1, 2)],
                                      name='price'),
                            pd.Series(actual)
                            )

        actual = tm.implied_volatility_elec(mock_spp,
                                            price_method='LMP',
                                            contract_range='J20-K20',
                                            bucket='offpeak'
                                            )
        assert_series_equal(pd.Series(target['J20-K20 offpeak'],
                                      index=[datetime.date(2019, 1, 2)],
                                      name='price'),
                            pd.Series(actual)
                            )

        actual = tm.implied_volatility_elec(mock_spp,
                                            price_method='LMP',
                                            contract_range='J20-K20',
                                            bucket='7x8'
                                            )
        assert_series_equal(pd.Series(target['J20-K20 7x8'],
                                      index=[datetime.date(2019, 1, 2)],
                                      name='price'),
                            pd.Series(actual)
                            )

        actual = tm.implied_volatility_elec(mock_spp,
                                            price_method='lmp',
                                            contract_range='2Q20',
                                            bucket='7x24'
                                            )
        assert_series_equal(pd.Series(target['7x24'],
                                      index=[datetime.date(2019, 1, 2)],
                                      name='price'),
                            pd.Series(actual)
                            )

        with pytest.raises(ValueError):
            tm.implied_volatility_elec(mock_spp,
                                       price_method='LMP',
                                       contract_range='5Q20',
                                       bucket='PEAK'
                                       )

        with pytest.raises(ValueError):
            tm.implied_volatility_elec(mock_spp,
                                       price_method='LMP',
                                       contract_range='Invalid',
                                       bucket='PEAK'
                                       )

        with pytest.raises(ValueError):
            tm.implied_volatility_elec(mock_spp,
                                       price_method='LMP',
                                       contract_range='3H20',
                                       bucket='7x24'
                                       )

        with pytest.raises(ValueError):
            tm.implied_volatility_elec(mock_spp,
                                       price_method='LMP',
                                       contract_range='F20-I20',
                                       bucket='7x24'
                                       )

        with pytest.raises(ValueError):
            tm.implied_volatility_elec(mock_spp,
                                       price_method='LMP',
                                       contract_range='2H20',
                                       bucket='7x24',
                                       real_time=True
                                       )

        replace.restore()

        replace = Replacer()
        mock_get_data = replace('gs_quant.data.dataset.Dataset.get_data', Mock())
        mock_get_data.return_value = mock_missing_bucket_implied_volatility()
        bbid_mock = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
        bbid_mock.return_value = 'SPP'

        actual = tm.implied_volatility_elec(mock_spp,
                                            price_method='LMP',
                                            contract_range='2Q20',
                                            bucket='7x24'
                                            )

        assert_series_equal(pd.Series(), pd.Series(actual), check_names=False)

        actual = tm.implied_volatility_elec(mock_spp,
                                            price_method='LMP',
                                            contract_range='2Q20',
                                            bucket='PEAK'
                                            )
        assert_series_equal(pd.Series(target['peak'],
                                      index=[datetime.date(2019, 1, 2)],
                                      name='price'),
                            pd.Series(actual)
                            )

        actual = tm.implied_volatility_elec(mock_spp,
                                            price_method='LMP',
                                            contract_range='J20-K20',
                                            bucket='7x24'
                                            )
        assert_series_equal(pd.Series(target['J20-K20 7x24'],
                                      index=[datetime.date(2019, 1, 2)],
                                      name='price'),
                            pd.Series(actual)
                            )
        replace.restore()

        # No market data
        mock_get_data = replace('gs_quant.data.dataset.Dataset.get_data', Mock())
        mock_get_data.return_value = mock_empty_market_data_response()
        bbid_mock = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
        bbid_mock.return_value = 'SPP'
        with DataContext(datetime.date(2019, 1, 2), datetime.date(2019, 1, 2)):
            actual = tm.implied_volatility_elec(mock_spp,
                                                price_method='LMP',
                                                contract_range='2Q20',
                                                bucket='7x24'
                                                )
            assert_series_equal(pd.Series(dtype='float64'), pd.Series(actual))
        replace.restore()


def test_forward_price_ng():
    # Tests for US NG assets
    replace = Replacer()
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_natgas_forward_price)
    mock = CommodityNaturalGasHub('MA001', 'AGT')

    with DataContext(datetime.date(2019, 1, 2), datetime.date(2019, 1, 2)):
        actual = pd.Series(tm.forward_price_ng(mock,
                                               price_method='GDD',
                                               contract_range='F21'))
        expected = pd.Series([2.880], index=[datetime.date(2019, 1, 2)], name='price')
        assert_series_equal(expected, actual)

        actual = pd.Series(tm.forward_price_ng(mock,
                                               price_method='GDD',
                                               contract_range='F21-G21'))
        expected = pd.Series([2.8629152542372878], index=[datetime.date(2019, 1, 2)], name='price')
        assert_series_equal(expected, actual)

        with pytest.raises(ValueError):
            tm.forward_price_ng(mock,
                                price_method='GDD',
                                contract_range='F21-I21')

        with pytest.raises(ValueError):
            tm.forward_price_ng(mock,
                                price_method='GDD',
                                contract_range='I21')

        with pytest.raises(MqTypeError):
            wrong_mock = Index('MA001', AssetClass.Commod, 'SPP')
            tm.forward_price_ng(wrong_mock,
                                price_method='GDD',
                                contract_range='I21')
        with pytest.raises(ValueError):
            tm.forward_price_ng(mock,
                                price_method='GDD',
                                contract_range='I21',
                                real_time=True)

    # No market data
    market_mock = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    market_mock.return_value = mock_empty_market_data_response()
    with DataContext(datetime.date(2019, 1, 2), datetime.date(2019, 1, 2)):
        actual = tm.forward_price_ng(mock,
                                     price_method='LMP',
                                     contract_range='2Q20')
        assert_series_equal(pd.Series(dtype='float64'),
                            pd.Series(actual)
                            )
    replace.restore()

    # Tests for EU NG assets
    mock_EU_asset = CommodityEUNaturalGasHub('MA001', 'TTF')
    mock_EU_swap_asset = Swap('MA002', AssetClass.Commod, 'Swap NatGas TTF')
    mock_EU_swap_asset.id = "Mock_Id"
    assets = replace('gs_quant.timeseries.measures.GsAssetApi.get_many_assets', Mock())
    assets.return_value = [mock_EU_swap_asset]

    # Test for forward price fetch using instrument id
    with DataContext(datetime.date(2021, 1, 1), datetime.date(2021, 1, 1)):
        market_mock = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_eu_natgas_forward_price)
        expected = pd.Series([15.65], name='price', index=[datetime.date(2021, 1, 1)])
        actual = tm.forward_price_ng(mock_EU_asset, contract_range='H21')
        assert_series_equal(expected, pd.Series(actual))

    # Test for empty market response
    with DataContext(datetime.date(2021, 1, 1), datetime.date(2021, 1, 1)):
        market_mock = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
        market_mock.return_value = mock_empty_market_data_response()
        actual = tm.forward_price_ng(mock_EU_asset, contract_range='H21', price_method='USD')
        assert actual.empty

    # Test for no instruments found
    with DataContext(datetime.date(2021, 1, 1), datetime.date(2021, 1, 1)):
        assets.return_value = []
        market_mock = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
        market_mock.return_value = mock_empty_market_data_response()
        actual = tm.forward_price_ng(mock_EU_asset, contract_range='H21')
        assert actual.empty

    replace.restore()


def test_implied_volatility_ng():
    replace = Replacer()
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_natgas_implied_volatility)
    mock = CommodityNaturalGasHub('MA001', 'AGT')

    with DataContext(datetime.date(2019, 1, 2), datetime.date(2019, 1, 2)):
        actual = pd.Series(tm.implied_volatility_ng(mock,
                                                    price_method='GDD',
                                                    contract_range='F21'))
        expected = pd.Series([2.880], index=[datetime.date(2019, 1, 2)], name='price')
        assert_series_equal(expected, actual)

        actual = pd.Series(tm.implied_volatility_ng(mock,
                                                    price_method='GDD',
                                                    contract_range='F21-G21'))
        expected = pd.Series([2.8629152542372878], index=[datetime.date(2019, 1, 2)], name='price')
        assert_series_equal(expected, actual)

        with pytest.raises(ValueError):
            tm.implied_volatility_ng(mock,
                                     price_method='GDD',
                                     contract_range='F21-I21')

        with pytest.raises(ValueError):
            tm.implied_volatility_ng(mock,
                                     price_method='GDD',
                                     contract_range='I21')

        with pytest.raises(ValueError):
            tm.implied_volatility_ng(mock,
                                     price_method='GDD',
                                     contract_range='I21',
                                     real_time=True)

    # No market data
    market_mock = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    market_mock.return_value = mock_empty_market_data_response()
    with DataContext(datetime.date(2019, 1, 2), datetime.date(2019, 1, 2)):
        actual = tm.implied_volatility_ng(mock,
                                          price_method='LMP',
                                          contract_range='2Q20')
        assert_series_equal(pd.Series(dtype='float64'),
                            pd.Series(actual)
                            )
    replace.restore()


def test_get_iso_data():
    tz_map = {'MISO': 'US/Central', 'CAISO': 'US/Pacific'}
    for key in tz_map:
        assert (tm._get_iso_data(key)[0] == tz_map[key])


def test_string_to_date_interval():
    assert (tm._string_to_date_interval("K20")['start_date'] == datetime.date(2020, 5, 1))
    assert (tm._string_to_date_interval("K20")['end_date'] == datetime.date(2020, 5, 31))

    assert (tm._string_to_date_interval("k20")['start_date'] == datetime.date(2020, 5, 1))
    assert (tm._string_to_date_interval("k20")['end_date'] == datetime.date(2020, 5, 31))

    assert (tm._string_to_date_interval("Cal22")['start_date'] == datetime.date(2022, 1, 1))
    assert (tm._string_to_date_interval("Cal22")['end_date'] == datetime.date(2022, 12, 31))

    assert (tm._string_to_date_interval("Cal2012")['start_date'] == datetime.date(2012, 1, 1))
    assert (tm._string_to_date_interval("Cal2012")['end_date'] == datetime.date(2012, 12, 31))

    assert (tm._string_to_date_interval("Cal53")['start_date'] == datetime.date(1953, 1, 1))
    assert (tm._string_to_date_interval("Cal53")['end_date'] == datetime.date(1953, 12, 31))

    assert (tm._string_to_date_interval("2010")['start_date'] == datetime.date(2010, 1, 1))
    assert (tm._string_to_date_interval("2010")['end_date'] == datetime.date(2010, 12, 31))

    assert (tm._string_to_date_interval("3Q20")['start_date'] == datetime.date(2020, 7, 1))
    assert (tm._string_to_date_interval("3Q20")['end_date'] == datetime.date(2020, 9, 30))

    assert (tm._string_to_date_interval("2h2021")['start_date'] == datetime.date(2021, 7, 1))
    assert (tm._string_to_date_interval("2h2021")['end_date'] == datetime.date(2021, 12, 31))

    assert (tm._string_to_date_interval("3q20")['start_date'] == datetime.date(2020, 7, 1))
    assert (tm._string_to_date_interval("3q20")['end_date'] == datetime.date(2020, 9, 30))

    assert (tm._string_to_date_interval("2H2021")['start_date'] == datetime.date(2021, 7, 1))
    assert (tm._string_to_date_interval("2H2021")['end_date'] == datetime.date(2021, 12, 31))

    assert (tm._string_to_date_interval("Mar2021")['start_date'] == datetime.date(2021, 3, 1))
    assert (tm._string_to_date_interval("Mar2021")['end_date'] == datetime.date(2021, 3, 31))

    assert (tm._string_to_date_interval("March2021")['start_date'] == datetime.date(2021, 3, 1))
    assert (tm._string_to_date_interval("March2021")['end_date'] == datetime.date(2021, 3, 31))

    assert (tm._string_to_date_interval("5Q20") == "Invalid Quarter")

    assert (tm._string_to_date_interval("HH2021") == "Invalid num")

    assert (tm._string_to_date_interval("3H2021") == "Invalid Half Year")

    assert (tm._string_to_date_interval("Cal2a") == "Invalid year")
    assert (tm._string_to_date_interval("Marc201") == "Invalid date code")

    assert (tm._string_to_date_interval("M1a2021") == "Invalid date code")

    assert (tm._string_to_date_interval("Marcha2021") == "Invalid date code")

    assert (tm._string_to_date_interval("I20") == "Invalid month")

    assert (tm._string_to_date_interval("20") == "Unknown date code")


def test_implied_vol_commod():
    target = {
        'F21': [2.880],
        'F21-H21': [2.815756],
    }
    replace = Replacer()
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_implied_volatility)
    mock = Index('MA001', AssetClass.Commod, 'Option NG Exchange')

    with DataContext(datetime.date(2019, 1, 2), datetime.date(2019, 1, 2)):
        actual = tm.implied_volatility(mock,
                                       tenor='F21-H21')
        assert_series_equal(pd.Series(target['F21-H21'],
                                      index=[datetime.date(2019, 1, 2)],
                                      name='price'),
                            pd.Series(actual))
    replace.restore()


def test_fair_price():
    target = {
        'F21': [2.880],
        'F21-H21': [2.815756],
    }
    replace = Replacer()
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_fair_price)
    mock = Index('MA001', AssetClass.Commod, 'Swap NG Exchange')
    mock2 = Swap('MA002', AssetClass.Commod, 'Swap Oil')

    with DataContext(datetime.date(2019, 1, 2), datetime.date(2019, 1, 2)):
        actual = tm.fair_price(mock,
                               tenor='F21')
        assert_series_equal(pd.Series(target['F21'],
                                      index=[datetime.date(2019, 1, 2)],
                                      name='price'),
                            pd.Series(actual))
    with pytest.raises(ValueError):
        tm.fair_price(mock,
                      tenor=None)
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_fair_price_swap)
    with DataContext(datetime.date(2019, 1, 2), datetime.date(2019, 1, 2)):
        actual = tm.fair_price(mock2)

        assert_series_equal(pd.Series([2.880],
                                      index=[pd.Timestamp('2019-01-02')],
                                      name='fairPrice'),
                            pd.Series(actual),
                            )

    replace.restore()


def test_weighted_average_valuation_curve_for_calendar_strip():
    target = {
        'F21': [2.880],
        'F21-H21': [2.815756],
    }
    replace = Replacer()
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_fair_price)
    mock = Index('MA001', AssetClass.Commod, 'Swap NG Exchange')

    with DataContext(datetime.date(2019, 1, 2), datetime.date(2019, 1, 2)):
        actual = tm._weighted_average_valuation_curve_for_calendar_strip(mock,
                                                                         contract_range='F21',
                                                                         query_type=QueryType.FAIR_PRICE,
                                                                         measure_field='fairPrice'
                                                                         )
        assert_series_equal(pd.Series(target['F21'],
                                      index=[datetime.date(2019, 1, 2)],
                                      name='price'),
                            pd.Series(actual))

        actual = tm._weighted_average_valuation_curve_for_calendar_strip(mock,
                                                                         contract_range='F21-H21',
                                                                         query_type=QueryType.FAIR_PRICE,
                                                                         measure_field='fairPrice'
                                                                         )
        assert_series_equal(pd.Series(target['F21-H21'],
                                      index=[datetime.date(2019, 1, 2)],
                                      name='price'),
                            pd.Series(actual))

        with pytest.raises(ValueError):
            tm._weighted_average_valuation_curve_for_calendar_strip(mock,
                                                                    contract_range='Invalid',
                                                                    query_type=QueryType.FAIR_PRICE,
                                                                    measure_field='fairPrice'
                                                                    )
        with pytest.raises(ValueError):
            tm._weighted_average_valuation_curve_for_calendar_strip(mock,
                                                                    contract_range='F20-I20',
                                                                    query_type=QueryType.FAIR_PRICE,
                                                                    measure_field='fairPrice'
                                                                    )
        with pytest.raises(ValueError):
            tm._weighted_average_valuation_curve_for_calendar_strip(mock,
                                                                    contract_range='3H20',
                                                                    query_type=QueryType.PRICE,
                                                                    measure_field='fairPrice'
                                                                    )

    replace.restore()


def test_fundamental_metrics():
    replace = Replacer()
    mock_spx = Index('MA890', AssetClass.Equity, 'SPX')
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_eq)
    period = '1y'
    direction = tm.FundamentalMetricPeriodDirection.FORWARD

    actual = tm.dividend_yield(mock_spx, period, direction)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='fundamentalMetric'), pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    with pytest.raises(NotImplementedError):
        tm.dividend_yield(..., period, direction, real_time=True)

    actual = tm.earnings_per_share(mock_spx, period, direction)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='fundamentalMetric'), pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    with pytest.raises(NotImplementedError):
        tm.earnings_per_share(..., period, direction, real_time=True)

    actual = tm.earnings_per_share_positive(mock_spx, period, direction)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='fundamentalMetric'), pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    with pytest.raises(NotImplementedError):
        tm.earnings_per_share_positive(..., period, direction, real_time=True)

    actual = tm.net_debt_to_ebitda(mock_spx, period, direction)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='fundamentalMetric'), pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    with pytest.raises(NotImplementedError):
        tm.net_debt_to_ebitda(..., period, direction, real_time=True)

    actual = tm.price_to_book(mock_spx, period, direction)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='fundamentalMetric'), pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    with pytest.raises(NotImplementedError):
        tm.price_to_book(..., period, direction, real_time=True)

    actual = tm.price_to_cash(mock_spx, period, direction)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='fundamentalMetric'), pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    with pytest.raises(NotImplementedError):
        tm.price_to_cash(..., period, direction, real_time=True)

    actual = tm.price_to_earnings(mock_spx, period, direction)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='fundamentalMetric'), pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    with pytest.raises(NotImplementedError):
        tm.price_to_earnings(..., period, direction, real_time=True)

    actual = tm.price_to_earnings_positive(mock_spx, period, direction)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='fundamentalMetric'), pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    with pytest.raises(NotImplementedError):
        tm.price_to_earnings_positive(..., period, direction, real_time=True)

    actual = tm.price_to_sales(mock_spx, period, direction)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='fundamentalMetric'), pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    with pytest.raises(NotImplementedError):
        tm.price_to_sales(..., period, direction, real_time=True)

    actual = tm.return_on_equity(mock_spx, period, direction)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='fundamentalMetric'), pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    with pytest.raises(NotImplementedError):
        tm.return_on_equity(..., period, direction, real_time=True)

    actual = tm.sales_per_share(mock_spx, period, direction)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='fundamentalMetric'), pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    with pytest.raises(NotImplementedError):
        tm.sales_per_share(..., period, direction, real_time=True)

    replace.restore()


def test_central_bank_swap_rate(mocker):
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

        actual_abs = tm.central_bank_swap_rate(mock_eur, tm.MeetingType.MEETING_FORWARD, tm.LevelType.ABSOLUTE,
                                               dt.date(2019, 12, 6))
        assert (target['meeting_absolute'] == actual_abs.loc[dt.date(2020, 1, 23)])
        assert actual_abs.dataset_ids == ('CENTRAL_BANK_WATCH',)

        actual_rel = tm.central_bank_swap_rate(mock_eur, tm.MeetingType.MEETING_FORWARD, tm.LevelType.RELATIVE,
                                               dt.date(2019, 12, 6))
        assert (target['meeting_relative'] == actual_rel.loc[dt.date(2020, 1, 23)])
        assert actual_rel.dataset_ids == ('CENTRAL_BANK_WATCH',)

        mock_get_data.return_value = mock_ois_spot()
        actual_spot = tm.central_bank_swap_rate(mock_eur, tm.MeetingType.SPOT, tm.LevelType.ABSOLUTE,
                                                dt.date(2019, 12, 6))
        assert (target['spot'] == actual_spot.loc[dt.date(2019, 12, 6)])
        assert actual_spot.dataset_ids == ('CENTRAL_BANK_WATCH',)

        with pytest.raises(MqError):
            tm.central_bank_swap_rate(mock_eur, 'meeting_forward')

        with pytest.raises(MqError):
            tm.central_bank_swap_rate(mock_eur, tm.MeetingType.MEETING_FORWARD, 'normalized', '2019-09-01')

        with pytest.raises(MqError):
            tm.central_bank_swap_rate(mock_eur, tm.MeetingType.MEETING_FORWARD, tm.LevelType.ABSOLUTE, 5)

        with pytest.raises(MqError):
            tm.central_bank_swap_rate(mock_eur, tm.MeetingType.MEETING_FORWARD, tm.LevelType.ABSOLUTE, '01-09-2019')

        with pytest.raises(MqError):
            tm.central_bank_swap_rate(mock_eur, tm.MeetingType.SPOT, tm.LevelType.RELATIVE)

        with pytest.raises(NotImplementedError):
            tm.central_bank_swap_rate(mock_eur, tm.MeetingType.SPOT, tm.LevelType.ABSOLUTE, real_time=True)

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
        mocker.patch.object(Dataset, 'get_data', side_effect=get_data_policy_rate_expectation_mocker)

        actual_num = tm.policy_rate_expectation(mock_eur, tm.MeetingType.MEETING_FORWARD, tm.LevelType.ABSOLUTE, 2)
        assert (target['meeting_number_absolute'] == actual_num.loc[dt.date(2019, 12, 6)])
        assert actual_num.dataset_ids == ('CENTRAL_BANK_WATCH',)

        actual_date = tm.policy_rate_expectation(mock_eur, tm.MeetingType.MEETING_FORWARD, tm.LevelType.ABSOLUTE,
                                                 dt.date(2020, 1, 23))
        assert (target['meeting_number_absolute'] == actual_date.loc[dt.date(2019, 12, 6)])
        assert actual_date.dataset_ids == ('CENTRAL_BANK_WATCH',)

        actual_num = tm.policy_rate_expectation(mock_eur, tm.MeetingType.MEETING_FORWARD, tm.LevelType.RELATIVE, 2)
        assert_allclose([target['meeting_number_relative']], [actual_num.loc[dt.date(2019, 12, 6)]],
                        rtol=1e-9, atol=1e-15)
        assert actual_num.dataset_ids == ('CENTRAL_BANK_WATCH',)

        actual_num = tm.policy_rate_expectation(mock_eur, tm.MeetingType.MEETING_FORWARD, tm.LevelType.ABSOLUTE, 0)
        assert (target['meeting_number_spot'] == actual_num.loc[dt.date(2019, 12, 6)])
        assert actual_num.dataset_ids == ('CENTRAL_BANK_WATCH',)

        actual_date = tm.policy_rate_expectation(mock_eur, tm.MeetingType.MEETING_FORWARD, tm.LevelType.ABSOLUTE,
                                                 '2019-10-24')
        assert (target['meeting_number_spot'] == actual_date.loc[dt.date(2019, 12, 6)])
        assert actual_date.dataset_ids == ('CENTRAL_BANK_WATCH',)

        mocker.patch.object(Dataset, 'get_data', side_effect=[mock_meeting_expectation(),
                                                              mock_empty_market_data_response()])
        with pytest.raises(MqError):
            tm.policy_rate_expectation(mock_eur, tm.MeetingType.MEETING_FORWARD, tm.LevelType.RELATIVE, 2)

        with pytest.raises(MqError):
            tm.policy_rate_expectation(mock_eur, tm.MeetingType.SPOT)

        with pytest.raises(MqError):
            tm.policy_rate_expectation(mock_eur, tm.MeetingType.MEETING_FORWARD, tm.LevelType.RELATIVE, '5')

        with pytest.raises(MqError):
            tm.policy_rate_expectation(mock_eur, tm.MeetingType.MEETING_FORWARD, tm.LevelType.ABSOLUTE, 5.5)

        with pytest.raises(MqError):
            tm.policy_rate_expectation(mock_eur, tm.MeetingType.MEETING_FORWARD, tm.LevelType.ABSOLUTE, '01-09-2019')

        with pytest.raises(MqError):
            tm.policy_rate_expectation(mock_eur, tm.MeetingType.MEETING_FORWARD, 'normalized', dt.date(2019, 9, 1))

        with pytest.raises(MqError):
            tm.policy_rate_expectation(mock_eur, tm.MeetingType.MEETING_FORWARD, tm.LevelType.RELATIVE, -2)

        with pytest.raises(NotImplementedError):
            tm.policy_rate_expectation(mock_eur, tm.MeetingType.SPOT, tm.LevelType.ABSOLUTE, real_time=True)

        mock_get_data = replace('gs_quant.data.dataset.Dataset.get_data', Mock())
        mock_get_data.return_value = pd.DataFrame()
        with pytest.raises(MqError):
            tm.policy_rate_expectation(mock_eur, tm.MeetingType.MEETING_FORWARD, tm.LevelType.ABSOLUTE, 2)

    replace.restore()


def test_realized_volatility():
    from gs_quant.timeseries.econometrics import volatility, Returns
    from gs_quant.timeseries.statistics import generate_series

    random = generate_series(100).rename('spot')
    window = 10
    type_ = Returns.SIMPLE

    replace = Replacer()
    market_data = replace('gs_quant.timeseries.measures._market_data_timed', Mock())
    return_value = MarketDataResponseFrame(random[:-1])
    return_value.dataset_ids = _test_datasets
    market_data.return_value = return_value

    current_market_data = replace('gs_quant.timeseries.measures.get_last_for_measure', Mock())
    return_value = MarketDataResponseFrame(random[-1:])
    return_value.dataset_ids = _test_datasets
    current_market_data.return_value = return_value

    expected = volatility(random, window, type_)
    actual = tm.realized_volatility(Cross('MA123', 'ABCXYZ'), window, type_)
    assert_series_equal(expected, pd.Series(actual))
    assert actual.dataset_ids == _test_datasets
    market_data.assert_called_once()
    current_market_data.assert_called_once()
    replace.restore()


def test_esg_headline_metric():
    replace = Replacer()

    mock_aapl = Stock('MA4B66MW5E27U9VBB94', 'AAPL')
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_esg)
    actual = tm.esg_headline_metric(mock_aapl, tm.EsgMetric.ENVIRONMENTAL_SOCIAL_NUMERIC_SCORE)
    assert_series_equal(pd.Series([2, 4, 6], index=_index * 3, name='esNumericScore'), pd.Series(actual))

    actual = tm.esg_headline_metric(mock_aapl, tm.EsgMetric.ENVIRONMENTAL_SOCIAL_POLICY_SCORE)
    assert_series_equal(pd.Series([2, 4, 6], index=_index * 3, name='esPolicyScore'), pd.Series(actual))

    actual = tm.esg_headline_metric(mock_aapl, tm.EsgMetric.ENVIRONMENTAL_SOCIAL_AGGREGATE_SCORE)
    assert_series_equal(pd.Series([2, 4, 6], index=_index * 3, name='esScore'), pd.Series(actual))

    actual = tm.esg_headline_metric(mock_aapl, tm.EsgMetric.ENVIRONMENTAL_SOCIAL_PRODUCT_IMPACT_SCORE)
    assert_series_equal(pd.Series([2, 4, 6], index=_index * 3, name='esProductImpactScore'), pd.Series(actual))

    actual = tm.esg_headline_metric(mock_aapl, tm.EsgMetric.GOVERNANCE_AGGREGATE_SCORE)
    assert_series_equal(pd.Series([2, 4, 6], index=_index * 3, name='gScore'), pd.Series(actual))

    actual = tm.esg_headline_metric(mock_aapl, tm.EsgMetric.ENVIRONMENTAL_SOCIAL_MOMENTUM_SCORE)
    assert_series_equal(pd.Series([2, 4, 6], index=_index * 3, name='esMomentumScore'), pd.Series(actual))

    actual = tm.esg_headline_metric(mock_aapl, tm.EsgMetric.GOVERNANCE_REGIONAL_SCORE)
    assert_series_equal(pd.Series([2, 4, 6], index=_index * 3, name='gRegionalScore'), pd.Series(actual))

    actual = tm.esg_headline_metric(mock_aapl, tm.EsgMetric.CONTROVERSY_SCORE)
    assert_series_equal(pd.Series([2, 4, 6], index=_index * 3, name='controversyScore'), pd.Series(actual))

    actual = tm.esg_headline_metric(mock_aapl, tm.EsgMetric.ENVIRONMENTAL_SOCIAL_NUMERIC_PERCENTILE)
    assert_series_equal(pd.Series([81.2, 75.4, 65.7], index=_index * 3, name='esNumericPercentile'), pd.Series(actual))

    actual = tm.esg_headline_metric(mock_aapl, tm.EsgMetric.ENVIRONMENTAL_SOCIAL_POLICY_PERCENTILE)
    assert_series_equal(pd.Series([81.2, 75.4, 65.7], index=_index * 3, name='esPolicyPercentile'), pd.Series(actual))

    actual = tm.esg_headline_metric(mock_aapl, tm.EsgMetric.ENVIRONMENTAL_SOCIAL_AGGREGATE_PERCENTILE)
    assert_series_equal(pd.Series([81.2, 75.4, 65.7], index=_index * 3, name='esPercentile'), pd.Series(actual))

    actual = tm.esg_headline_metric(mock_aapl, tm.EsgMetric.ENVIRONMENTAL_SOCIAL_PRODUCT_IMPACT_PERCENTILE)
    assert_series_equal(pd.Series([81.2, 75.4, 65.7], index=_index * 3, name='esProductImpactPercentile'),
                        pd.Series(actual))

    actual = tm.esg_headline_metric(mock_aapl, tm.EsgMetric.GOVERNANCE_AGGREGATE_PERCENTILE)
    assert_series_equal(pd.Series([81.2, 75.4, 65.7], index=_index * 3, name='gPercentile'),
                        pd.Series(actual))

    actual = tm.esg_headline_metric(mock_aapl, tm.EsgMetric.ENVIRONMENTAL_SOCIAL_MOMENTUM_PERCENTILE)
    assert_series_equal(pd.Series([81.2, 75.4, 65.7], index=_index * 3, name='esMomentumPercentile'),
                        pd.Series(actual))

    actual = tm.esg_headline_metric(mock_aapl, tm.EsgMetric.GOVERNANCE_REGIONAL_PERCENTILE)
    assert_series_equal(pd.Series([81.2, 75.4, 65.7], index=_index * 3, name='gRegionalPercentile'),
                        pd.Series(actual))

    actual = tm.esg_headline_metric(mock_aapl, tm.EsgMetric.CONTROVERSY_PERCENTILE)
    assert_series_equal(pd.Series([81.2, 75.4, 65.7], index=_index * 3, name='controversyPercentile'),
                        pd.Series(actual))

    actual = tm.esg_headline_metric(mock_aapl, tm.EsgMetric.ENVIRONMENTAL_SOCIAL_DISCLOSURE)
    assert_series_equal(pd.Series([49.2, 55.7, 98.4], index=_index * 3, name='esDisclosurePercentage'),
                        pd.Series(actual))

    with pytest.raises(NotImplementedError):
        tm.esg_headline_metric(mock_aapl, tm.EsgMetric.ENVIRONMENTAL_SOCIAL_NUMERIC_SCORE, real_time=True)

    replace.restore()


def test_rating():
    replace = Replacer()

    mock_aapl = Stock('MA4B66MW5E27U9VBB94', 'AAPL')
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_rating)
    actual = tm.rating(mock_aapl, tm._RatingMetric.RATING)
    assert_series_equal(pd.Series([1, -1, 1, 0], index=pd.to_datetime([datetime.date(2020, 8, 13),
                                                                       datetime.date(2020, 8, 14),
                                                                       datetime.date(2020, 8, 17),
                                                                       datetime.date(2020, 8, 18)]),
                                  name='rating'), pd.Series(actual))

    actual = tm.rating(mock_aapl, tm._RatingMetric.CONVICTION_LIST)
    assert_series_equal(pd.Series([1, 0, 0, 0], index=pd.to_datetime([datetime.date(2020, 8, 13),
                                                                      datetime.date(2020, 8, 14),
                                                                      datetime.date(2020, 8, 17),
                                                                      datetime.date(2020, 8, 18)]),
                                  name='convictionList'), pd.Series(actual))
    assert actual.dataset_ids == _test_datasets

    with pytest.raises(NotImplementedError):
        tm.rating(mock_aapl, tm._RatingMetric.RATING, real_time=True)
    replace.restore()


def test_fair_value(mocker):
    mocker.patch.object(GsSession.__class__, 'default_value',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    replace = Replacer()
    mock_usdeur = Cross('MAQB05GD31BA5HWV', 'USDEUR')
    mock_eurusd = Cross('MAA0NE9QX2ABETG6', "EURUSD")
    xrefs = replace('gs_quant.timeseries.measures.GsAssetApi.get_asset_xrefs', Mock())
    xrefs.return_value = [GsTemporalXRef(dt.date(2019, 1, 1), dt.date(2952, 12, 31), XRef(bbid='EURUSD', ))]
    asset = replace('gs_quant.markets.securities.SecurityMaster.get_asset', Mock())
    asset.return_value = mock_usdeur
    replace('gs_quant.timeseries.measures.Dataset.get_data', mock_gsdeer_gsfeer)

    index = [dt.date(2000, 1, 1), dt.date(2010, 4, 1), dt.date(2020, 7, 1)]
    actual = tm.fair_value(mock_usdeur,
                           tm.EquilibriumExchangeRateMetric.GSDEER)
    assert_series_equal(pd.Series([1, 1.2, 1.1], index=index, name='gsdeer'),
                        pd.Series(actual))

    actual = tm.fair_value(mock_usdeur,
                           tm.EquilibriumExchangeRateMetric.GSFEER)
    assert_series_equal(pd.Series([2, 1.8, 1.9], index=index, name='gsfeer'),
                        pd.Series(actual))

    actual = tm.fair_value(mock_eurusd,
                           tm.EquilibriumExchangeRateMetric.GSDEER)
    assert_series_equal(pd.Series([1 / 1, 1 / 1.2, 1 / 1.1], index=index, name='gsdeer'),
                        pd.Series(actual))

    actual = tm.fair_value(mock_eurusd,
                           tm.EquilibriumExchangeRateMetric.GSFEER)
    assert_series_equal(pd.Series([1 / 2, 1 / 1.8, 1 / 1.9], index=index, name='gsfeer'),
                        pd.Series(actual))
    with pytest.raises(NotImplementedError):
        tm.fair_value(mock_usdeur,
                      tm.EquilibriumExchangeRateMetric.GSDEER,
                      real_time=True)
    replace.restore()


def test_factor_profile():
    replace = Replacer()

    mock_aapl = Stock('MA4B66MW5E27U9VBB94', 'AAPL')
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_factor_profile)
    actual = tm.factor_profile(mock_aapl, tm._FactorProfileMetric.GROWTH_SCORE)
    assert_series_equal(pd.Series([0.238, 0.234, 0.234, 0.230], index=pd.to_datetime([datetime.date(2020, 8, 13),
                                                                                      datetime.date(2020, 8, 14),
                                                                                      datetime.date(2020, 8, 17),
                                                                                      datetime.date(2020, 8, 18)]),
                                  name='growthScore'), pd.Series(actual))
    assert actual.dataset_ids == _test_datasets

    actual = tm.factor_profile(mock_aapl, tm._FactorProfileMetric.FINANCIAL_RETURNS_SCORE)
    assert_series_equal(pd.Series([0.982, 0.982, 0.982, 0.982], index=pd.to_datetime([datetime.date(2020, 8, 13),
                                                                                      datetime.date(2020, 8, 14),
                                                                                      datetime.date(2020, 8, 17),
                                                                                      datetime.date(2020, 8, 18)]),
                                  name='financialReturnsScore'), pd.Series(actual))
    assert actual.dataset_ids == _test_datasets

    actual = tm.factor_profile(mock_aapl, tm._FactorProfileMetric.MULTIPLE_SCORE)
    assert_series_equal(pd.Series([0.204, 0.192, 0.190, 0.190], index=pd.to_datetime([datetime.date(2020, 8, 13),
                                                                                      datetime.date(2020, 8, 14),
                                                                                      datetime.date(2020, 8, 17),
                                                                                      datetime.date(2020, 8, 18)]),
                                  name='multipleScore'), pd.Series(actual))
    assert actual.dataset_ids == _test_datasets

    actual = tm.factor_profile(mock_aapl, tm._FactorProfileMetric.INTEGRATED_SCORE)
    assert_series_equal(pd.Series([0.672, 0.676, 0.676, 0.674], index=pd.to_datetime([datetime.date(2020, 8, 13),
                                                                                      datetime.date(2020, 8, 14),
                                                                                      datetime.date(2020, 8, 17),
                                                                                      datetime.date(2020, 8, 18)]),
                                  name='integratedScore'), pd.Series(actual))
    assert actual.dataset_ids == _test_datasets

    with pytest.raises(NotImplementedError):
        tm.factor_profile(mock_aapl, tm._FactorProfileMetric.GROWTH_SCORE, real_time=True)

    replace.restore()


def test_commodity_forecast():
    replace = Replacer()

    mock_spgcsb = Index('MA74Y70Z4D4TBX9H', 'SPGCSB', 'GSCI Sugar')
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_commodity_forecast)
    actual = tm.commodity_forecast(mock_spgcsb, '3m',
                                   tm._CommodityForecastType.SPOT_RETURN)
    assert_series_equal(pd.Series([1700, 1400, 1500, 1600], index=pd.to_datetime([datetime.date(2020, 8, 13),
                                                                                  datetime.date(2020, 8, 14),
                                                                                  datetime.date(2020, 8, 17),
                                                                                  datetime.date(2020, 8, 18)]),
                                  name='commodityForecast'), pd.Series(actual))

    with pytest.raises(NotImplementedError):
        tm.commodity_forecast(mock_spgcsb, '3m',
                              tm._CommodityForecastType.SPOT_RETURN, real_time=True)
    replace.restore()


def test_spot_carry():
    replace = Replacer()
    mock = Cross('MAA0NE9QX2ABETG6', 'USD/EUR')
    assets = replace('gs_quant.timeseries.measures.cross_stored_direction_for_fx_vol', Mock())
    assets.return_value = mock.get_marquee_id()

    df = pd.DataFrame({
        '3m': [0.001978858350951374, 0.0019735843327766817, 0.00198293829264794],
        '2y': [0.016989429175475686, 0.016994753976688093, 0.017416104834150414],
        '3m_ann': [0.007915433403805495, 0.007894337331106727, 0.00793175317059176],
        'date': [pd.Timestamp('2020-09-02'), pd.Timestamp('2020-09-03'), pd.Timestamp('2020-09-04')]
    })
    df = df.set_index('date')

    with DataContext(dt.date(2020, 9, 2), dt.date(2020, 9, 4)):
        # tenors in terms of months
        replace('gs_quant.timeseries.measures._market_data_timed', mock_fx_spot_fwd_3m)
        actual_3m = tm.spot_carry(mock, '3m')
        assert_series_equal(df['3m'], pd.Series(actual_3m, name='3m'))

        # annualized
        actual_3m_ann = tm.spot_carry(mock, '3m', tm.FXSpotCarry.ANNUALIZED)
        assert_series_equal(df['3m_ann'], pd.Series(actual_3m_ann, name='3m_ann'))

        # not supported
        with pytest.raises(NotImplementedError):
            tm.spot_carry(mock, '1m', real_time=True)

        with pytest.raises(MqError):
            tm.spot_carry(mock, '13m')

        # tenors in terms of years
        replace('gs_quant.timeseries.measures._market_data_timed', mock_fx_spot_fwd_2y)
        actual_2y = tm.spot_carry(mock, '2y')
        assert_series_equal(df['2y'], pd.Series(actual_2y, name='2y'))
        replace.restore()


def test_fx_implied_correlation():
    replace = Replacer()

    e1 = {'last_updated_time': '2021-02-03T15:11:06.409Z', 'owner_id': 'qwerty',
          'classifications': {}, 'description': 'Europe Euro to United States Dollar',
          'last_updated_by_id': 'qwerty', 'id': 'MAA0NE9QX2ABETG6', 'listed': True,
          'created_time': '2017-06-16T13:59:23.617Z', 'exchange': '', 'parameters': {}, 'type': 'Cross',
          'entitlements': {'edit': ['guid:qwerty'],
                           'view': ['internal', 'guid:qwerty', 'external'],
                           'admin': ['guid:qwerty']}, 'name': 'EURUSD',
          'region': 'Global', 'styles': [], 'short_name': 'EURUSD',
          'identifiers': [{'type': 'SECNAME', 'value': 'USD/EUR'}, {'type': 'BID', 'value': 'EURUSD'},
                          {'type': 'MDAPI', 'value': 'USD/EUR'}, {'type': 'CROSS', 'value': 'USD/EUR'}],
          'rank': 1.0, 'asset_class': 'FX',
          'xref': {'bbid': 'EURUSD', 'cross': 'USD/EUR', 'secName': 'USD/EUR', 'mdapi': 'USD/EUR'},
          'currency': 'USD', 'tags': ['USDEUR', 'EURUSD', 'Execution'],
          'created_by_id': 'qwerty'}
    e2 = {'last_updated_time': '2021-02-03T15:05:20.993Z', 'owner_id': 'azerty',
          'classifications': {}, 'description': 'United States Dollar to Europe Euro',
          'last_updated_by_id': 'azerty', 'id': 'MAQB05GD31BA5HWV', 'listed': True,
          'created_time': '2017-06-16T13:52:21.396Z', 'exchange': '', 'parameters': {}, 'type': 'Cross',
          'entitlements': {'edit': ['guid:azerty'],
                           'view': ['internal', 'guid:azerty', 'external'],
                           'admin': ['guid:azerty']}, 'name': 'USDEUR', 'region': 'Global',
          'styles': [], 'short_name': 'USDEUR', 'rank': 1.0,
          'asset_class': 'FX', 'xref': {'bbid': 'USDEUR', 'cross': 'EUR/USD', 'secName': 'EUR/USD', 'mdapi': 'EUR/USD'},
          'currency': 'EUR', 'tags': ['EURUSD', 'USDEUR'], 'created_by_id': 'azerty'}

    EURUSD = Cross('MAA0NE9QX2ABETG6', 'USD/EUR', entity=e1)
    USDEUR = Cross('MAQB05GD31BA5HWV', 'EUR/USD', entity=e2)
    USDJPY = Cross('MATGYV0J9MPX534Z', 'JPY/USD')
    JPYUSD = Cross('MAYJPCVVF2RWXCES', 'USD/JPY')
    EURGBP = Cross('MA3AMDKY4YJ83G1E', 'GBP/EUR')
    EURJPY = Cross('MAYPHS80JRWDJ8RC', 'JPY/EUR')
    JPYEUR = Cross('MAWVKC8Q6405ZWNE', 'EUR/JPY')
    bbid_to_asset_dict = {'EURUSD': EURUSD, 'USDEUR': USDEUR, 'USDJPY': USDJPY, 'JPYUSD': JPYUSD,
                          'EURJPY': EURJPY, 'JPYEUR': JPYEUR, 'EURGBP': EURGBP}
    mqid_to_asset_dict = {'MAA0NE9QX2ABETG6': EURUSD, 'MAQB05GD31BA5HWV': USDEUR, 'MATGYV0J9MPX534Z': USDJPY,
                          'MAYJPCVVF2RWXCES': JPYUSD, 'MAYPHS80JRWDJ8RC': EURJPY, 'MAWVKC8Q6405ZWNE': JPYEUR,
                          'MA3AMDKY4YJ83G1E': EURGBP}
    df = pd.DataFrame({
        'EURUSD USDJPY': [-0.47579170795443204, -0.4842168280011238, -0.48220935681227195],
        'USDEUR USDJPY': [0.47579175, 0.48421678, 0.48220939],
        'EURUSD JPYUSD': [0.47579175, 0.48421678, 0.48220939],
        'USDEUR JPYUSD': [-0.47579175, -0.48421678, -0.48220939],
        'USDJPY EURUSD': [-0.47579175, -0.48421678, -0.48220939],
        'date': [pd.Timestamp('2020-09-02'), pd.Timestamp('2020-09-03'), pd.Timestamp('2020-09-04')]
    })
    df = df.set_index('date')

    def mock_get_asset(cls, asset_id, id_type: dict) -> Cross:
        if id_type == AssetIdentifier.BLOOMBERG_ID:
            return bbid_to_asset_dict[asset_id]
        else:
            return mqid_to_asset_dict[asset_id]

    def cross_to_bbid(asset, id_type) -> str:
        if asset == EURUSD:
            return 'EURUSD'
        elif asset == USDEUR:
            return 'USDEUR'
        elif asset == USDJPY:
            return 'USDJPY'
        elif asset == JPYUSD:
            return 'JPYUSD'
        elif asset == EURJPY:
            return 'EURJPY'
        elif asset == JPYEUR:
            return 'JPYEUR'
        elif asset == EURGBP:
            return 'EURGBP'

    replace('gs_quant.markets.securities.SecurityMaster.get_asset', mock_get_asset)
    replace('gs_quant.markets.securities.Asset.get_identifier', cross_to_bbid)
    replace('gs_quant.timeseries.measures._market_data_timed', mock_fx_correlation)

    with DataContext(dt.date(2020, 9, 2), dt.date(2020, 9, 4)):
        # supported
        q_1 = tm.fx_implied_correlation(EURUSD, USDJPY, '3m')
        q_2 = tm.fx_implied_correlation(USDEUR, USDJPY, '3m')
        q_3 = tm.fx_implied_correlation(EURUSD, JPYUSD, '3m')
        q_4 = tm.fx_implied_correlation(USDEUR, JPYUSD, '3m')
        q_5 = tm.fx_implied_correlation(USDJPY, EURUSD, '3m')
        assert_series_equal(df['EURUSD USDJPY'], pd.Series(q_1, name='EURUSD USDJPY'))
        assert_series_equal(df['USDEUR USDJPY'], pd.Series(q_2, name='USDEUR USDJPY'))
        assert_series_equal(df['EURUSD JPYUSD'], pd.Series(q_3, name='EURUSD JPYUSD'))
        assert_series_equal(df['USDEUR JPYUSD'], pd.Series(q_4, name='USDEUR JPYUSD'))
        assert_series_equal(df['USDJPY EURUSD'], pd.Series(q_5, name='USDJPY EURUSD'))

        replace('gs_quant.timeseries.measures._market_data_timed', lambda q, request_id=None: pd.DataFrame())
        assert tm.fx_implied_correlation(USDJPY, EURUSD, '3m').empty

        # not supported
        with pytest.raises(NotImplementedError):
            tm.fx_implied_correlation(EURUSD, EURGBP, '3m', real_time=True)
        with pytest.raises(MqError):
            tm.fx_implied_correlation(USDJPY, EURGBP, '3m', real_time=False)
        with pytest.raises(MqError):
            mock_spx = Index('MA890', AssetClass.Equity, 'SPX')
            tm.fx_implied_correlation(USDJPY, mock_spx, '3m', real_time=False)

    replace.restore()


def mock_forward_curve_peak(_cls, _q):
    d = {
        'forwardPrice': [40.05],
        'quantityBucket': ["PEAK"],
        'contract': ["U20"]
    }
    df = MarketDataResponseFrame(data=d, index=pd.to_datetime([datetime.date(2020, 8, 20)]))
    df.dataset_ids = _test_datasets
    return df


def mock_forward_curve_peak_holiday(_cls, _q):
    d = {
        'forwardPrice': [26.567302],
        'quantityBucket': ["PEAK"],
        'contract': ["U20"]
    }
    df = MarketDataResponseFrame(data=d, index=pd.to_datetime([datetime.date(2020, 9, 4)]))
    df.dataset_ids = _test_datasets
    return df


def mock_forward_curve_offpeak(_cls, _q):
    d = {
        'forwardPrice': [30.9692, 44.9868],
        'quantityBucket': ["7X8", "SUH1X16"],
        'contract': ["U20", "U20"]
    }
    df = MarketDataResponseFrame(data=d, index=pd.to_datetime([datetime.date(2020, 8, 20)] * 2))
    df.dataset_ids = _test_datasets
    return df


def mock_empty_forward_curve(_cls, _q):
    df = MarketDataResponseFrame()
    df.dataset_ids = ()
    return df


def test_forward_curve():
    # Set output and mock attributes for test
    target = {
        'Peak_CAISO': [40.05],
        'OffPeak_CAISO': [34.4736],
        'Peak_CAISO_holiday': [26.567302]
    }
    replace = Replacer()
    mock_CAISO = Index('MA001', AssetClass.Commod, 'CAISO')
    bbid_mock = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
    bbid_mock.return_value = 'CAISO'
    mock_get_data = replace('gs_quant.data.dataset.Dataset.get_data_last', Mock())

    with DataContext(datetime.date(2020, 8, 20), datetime.date(2020, 9, 20)):
        # Test for term structure for bucket: peak
        replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_forward_curve_peak)
        mock_get_data.return_value = pd.DataFrame(data=[0], index=[datetime.date(2020, 8, 20)])
        actual = tm.forward_curve(mock_CAISO, bucket='Peak', market_date='20200820')
        assert_series_equal(pd.Series(target['Peak_CAISO'], index=[datetime.date(2020, 9, 1)], name='forwardPrice'),
                            pd.Series(actual))

        # Test for holiday date query, which would fetch value for prev date
        replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_forward_curve_peak_holiday)
        mock_get_data.return_value = pd.DataFrame(data=[0], index=[datetime.date(2020, 9, 4)])
        actual = tm.forward_curve(mock_CAISO, bucket='Peak', market_date='20200907')
        assert_series_equal(pd.Series(target['Peak_CAISO_holiday'], index=[datetime.date(2020, 9, 1)],
                                      name='forwardPrice'), pd.Series(actual))

        # Test for term structure for bucket: Off peak, which requires wtd avg computation
        replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_forward_curve_offpeak)
        mock_get_data.return_value = pd.DataFrame(data=[0], index=[datetime.date(2020, 8, 25)])
        actual = tm.forward_curve(mock_CAISO, bucket='OffPeak', market_date='20200825')
        assert_series_equal(pd.Series(target['OffPeak_CAISO'], index=[datetime.date(2020, 9, 1)], name='forwardPrice'),
                            pd.Series(actual))

        # Test for an empty data query result
        replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_empty_forward_curve)
        mock_get_data.return_value = pd.DataFrame(data=[0], index=[datetime.date(2020, 8, 25)])
        actual = tm.forward_curve(mock_CAISO, bucket='OffPeak', market_date='20200825')
        assert actual.empty

        # Test for intra day frequency error
        with pytest.raises(MqValueError):
            tm.forward_curve(mock_CAISO, bucket='7x24', market_date='20200820', real_time=True)

        # Test for future date query
        with pytest.raises(MqValueError):
            tm.forward_curve(mock_CAISO, bucket='7x24', market_date='20400820')

        # Test for weekend date query
        with pytest.raises(MqValueError):
            tm.forward_curve(mock_CAISO, bucket='7x24', market_date='20200822')

        # Test for term structure for market date beyond end date which is an invalid scenario
        with pytest.raises(MqValueError):
            tm.forward_curve(mock_CAISO, bucket='OffPeak', market_date='20201001')

        # Test for empty market date in parameters, will fail as end date for this test is in past
        with pytest.raises(MqValueError):
            actual = tm.forward_curve(mock_CAISO, bucket='Peak')

        # Test for invalid market_date data type
        with pytest.raises(MqTypeError):
            actual = tm.forward_curve(mock_CAISO, bucket='Peak', market_date=20201001)

        # Test for invalid market_date string format
        with pytest.raises(MqValueError):
            actual = tm.forward_curve(mock_CAISO, bucket='Peak', market_date='9, Jan 2020')

        # Test for default date always returning a weekday
        replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_forward_curve_peak)
        mock_todate = replace('pandas.Timestamp.today', Mock())
        mock_todate.return_value = pd.Timestamp('2020-08-22')
        mock_get_data.return_value = pd.DataFrame(data=[0], index=[datetime.date(2020, 8, 20)])
        actual = tm.forward_curve(mock_CAISO, bucket='Peak')
        assert_series_equal(pd.Series(target['Peak_CAISO'], index=[datetime.date(2020, 9, 1)], name='forwardPrice'),
                            pd.Series(actual))

    replace.restore()


def test_eu_ng_hub_to_swap():
    # Test for Id provider to return an instrument
    replace = Replacer()
    mock_EU_asset = CommodityEUNaturalGasHub('MA001', 'TTF')
    mock_EU_swap_asset = Swap('MA002', AssetClass.Commod, 'Swap NatGas TTF')
    mock_EU_swap_asset.id = 'MA002'
    assets = replace('gs_quant.timeseries.measures.GsAssetApi.get_many_assets', Mock())
    assets.return_value = [mock_EU_swap_asset]
    actual = tm.eu_ng_hub_to_swap(mock_EU_asset)
    assert_equal(actual, 'MA002')

    # Test for Id provider when no instrument found, returns original asset id
    mock_EU_asset = CommodityEUNaturalGasHub('MA001', 'TTF')
    assets = replace('gs_quant.timeseries.measures.GsAssetApi.get_many_assets', Mock())
    assets.return_value = []
    actual = tm.eu_ng_hub_to_swap(mock_EU_asset)
    assert_equal(actual, 'MA001')


def test_settlement_price():
    # Tests for settlement price function
    replace = Replacer()

    with DataContext(datetime.date(2021, 6, 2), datetime.date(2021, 6, 2)):
        # Test for EEX Asset
        Asset_Mock = FutureMarket('MA001', AssetClass.Commod, 'DEBM')
        EEX_mock = replace('gs_quant.timeseries.measures.Asset.get_entity', Mock())
        EEX_mock.return_value = {'parameters': {'exchange': 'EEX', 'productGroup': 'PowerFutures'}}
        EEX_ds = replace('gs_quant.data.dataset.Dataset.get_data', Mock())
        EEX_ds.return_value = pd.DataFrame(data=dict(settlementPrice=20.20, contract='K21'),
                                           index=[datetime.date(2021, 6, 2)])
        actual = pd.Series(tm.settlement_price(Asset_Mock, contract='K21'))
        expected = pd.Series([20.20], index=[datetime.date(2021, 6, 2)], name='settlementPrice')
        assert_series_equal(expected, actual)

        # Test for CarbonCredit Asset
        Asset_Mock = FutureMarket('MA001', AssetClass.Commod, 'RGGI V19')
        CC_mock = replace('gs_quant.timeseries.measures.Asset.get_entity', Mock())
        CC_mock.return_value = {'parameters': {'exchange': 'ICE', 'productGroup': 'Physical Environment'}}
        CC_ds = replace('gs_quant.data.dataset.Dataset.get_data', Mock())
        CC_ds.return_value = pd.DataFrame(data=dict(settlementPrice=21.21, contract='K21'),
                                          index=[datetime.date(2021, 6, 2)])
        actual = pd.Series(tm.settlement_price(Asset_Mock, contract='K21'))
        expected = pd.Series([21.21], index=[datetime.date(2021, 6, 2)], name='settlementPrice')
        assert_series_equal(expected, actual)

        # Test for ICE Power Asset
        Asset_Mock = FutureMarket('MA001', AssetClass.Commod, 'GAB')
        CC_mock = replace('gs_quant.timeseries.measures.Asset.get_entity', Mock())
        CC_mock.return_value = {'parameters': {'exchange': 'ICE', 'productGroup': 'PowerFutures'}}
        CC_ds = replace('gs_quant.data.dataset.Dataset.get_data', Mock())
        CC_ds.return_value = pd.DataFrame(data=dict(settlementPrice=22.22, contract='K21'),
                                          index=[datetime.date(2021, 6, 2)])
        actual = pd.Series(tm.settlement_price(Asset_Mock, contract='K21'))
        expected = pd.Series([22.22], index=[datetime.date(2021, 6, 2)], name='settlementPrice')
        assert_series_equal(expected, actual)

        # Test for NASDAQ Power Asset
        Asset_Mock = FutureMarket('MA001', AssetClass.Commod, 'ENOFUTBL')
        CC_mock = replace('gs_quant.timeseries.measures.Asset.get_entity', Mock())
        CC_mock.return_value = {'parameters': {'exchange': 'NASDAQ', 'productGroup': 'PowerFutures'}}
        CC_ds = replace('gs_quant.data.dataset.Dataset.get_data', Mock())
        CC_ds.return_value = pd.DataFrame(data=dict(settlementPrice=23.23, contract='K21'),
                                          index=[datetime.date(2021, 6, 2)])
        actual = pd.Series(tm.settlement_price(Asset_Mock, contract='K21'))
        expected = pd.Series([23.23], index=[datetime.date(2021, 6, 2)], name='settlementPrice')
        assert_series_equal(expected, actual)

        # Test for empty  result
        CC_ds.return_value = pd.DataFrame()
        actual = pd.Series(tm.settlement_price(Asset_Mock, contract='K21'))
        expected = pd.Series()
        assert_series_equal(expected, actual)

        # Test for asset with no exchange info
        Asset_Mock = FutureMarket('MA001', AssetClass.Commod, 'XYZ')
        empty_mock = replace('gs_quant.timeseries.measures.Asset.get_entity', Mock())
        empty_mock.return_value = {'parameters': {}}

        with pytest.raises(MqTypeError):
            tm.settlement_price(Asset_Mock, contract='F21')

        # Test for asset with any only some asset params filled
        Asset_Mock = FutureMarket('MA001', AssetClass.Commod, 'XYZ')
        empty_mock = replace('gs_quant.timeseries.measures.Asset.get_entity', Mock())
        empty_mock.return_value = {'parameters': {'exchange': 'OTHER_EXCHANGE'}}

        with pytest.raises(MqTypeError):
            tm.settlement_price(Asset_Mock, contract='F21')

        # Test for asset with any other exchange, currently not covered
        Asset_Mock = FutureMarket('MA001', AssetClass.Commod, 'XYZ')
        empty_mock = replace('gs_quant.timeseries.measures.Asset.get_entity', Mock())
        empty_mock.return_value = {'parameters': {'exchange': 'OTHER_EXCHANGE', 'productGroup': 'OTHER_PRODUCT'}}

        with pytest.raises(MqTypeError):
            tm.settlement_price(Asset_Mock, contract='F21')

        # Test for real time data setting on query
        with pytest.raises(MqValueError):
            tm.settlement_price(Asset_Mock, contract='F21', real_time=True)

    replace.restore()


def test_hloc_prices():
    mock_spx = Index('MA890', AssetClass.Equity, 'SPX')
    with pytest.raises(MqValueError):
        tm.hloc_prices(mock_spx, real_time=True)

    replace = Replacer()
    empty_df = replace('gs_quant.timeseries.measures.Asset.get_hloc_prices', Mock())
    empty_df.return_value = pd.DataFrame()
    with DataContext(datetime.date(2021, 6, 2), datetime.date(2021, 6, 2)):
        tm.hloc_prices(mock_spx, real_time=False)

    replace.restore()


def test_thematic_exposure():
    mock_asset = GsAsset(asset_class='Equity', id='MA1234567890', type_='Custom Basket', name='test')
    mock_basket = CustomBasket(gs_asset=mock_asset, _finish_init=False)

    replace = Replacer()

    empty_df = replace('gs_quant.timeseries.measures.Asset.get_thematic_exposure', Mock())
    empty_df.return_value = pd.DataFrame()
    with DataContext(datetime.date(2021, 6, 2), datetime.date(2021, 6, 2)):
        tm.thematic_exposure(mock_basket, 'TICKER')

    replace.restore()


def test_thematic_beta():
    mock_asset = GsAsset(asset_class='Equity', id='MA1234567890', type_='Custom Basket', name='test')
    mock_basket = CustomBasket(gs_asset=mock_asset, _finish_init=False)

    replace = Replacer()

    empty_df = replace('gs_quant.timeseries.measures.Asset.get_thematic_beta', Mock())
    empty_df.return_value = pd.DataFrame()
    with DataContext(datetime.date(2021, 6, 2), datetime.date(2021, 6, 2)):
        tm.thematic_beta(mock_basket, 'TICKER')

    replace.restore()


if __name__ == '__main__':
    pytest.main(args=["test_measures.py"])
