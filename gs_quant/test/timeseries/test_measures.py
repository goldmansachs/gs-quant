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
import unittest.mock
from typing import Union

import pandas as pd
import pytest
from pandas.testing import assert_series_equal
from pytz import timezone
from testfixtures import Replacer
from testfixtures.mock import Mock

import gs_quant.timeseries.measures as tm
from gs_quant.api.gs.assets import GsTemporalXRef, GsAssetApi, GsIdType, IdList
from gs_quant.data.core import DataContext
from gs_quant.errors import MqError
from gs_quant.markets.securities import AssetClass, Cross, Index, Currency
from gs_quant.session import GsSession, Environment
from gs_quant.target.common import XRef
from gs_quant.test.timeseries.utils import mock_request
from gs_quant.timeseries.measures import BenchmarkType

_index = [pd.Timestamp('2019-01-01')]


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


def test_currency_to_default_benchmark_rate(mocker):
    mocker.patch.object(GsSession.__class__, 'current',
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


def test_currency_to_inflation_benchmark_rate(mocker):
    mocker.patch.object(GsSession.__class__, 'current',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_get', side_effect=mock_request)
    mocker.patch.object(GsAssetApi, 'map_identifiers', side_effect=map_identifiers_inflation_mocker)

    asset_id_list = ["MA66CZBQJST05XKG", "MAK1FHKH5P5GJSHH", "MA4J1YB8XZP2BPT8"]
    correct_mapping = ["MAQ7ND0MBP2AVVQW", "MAK1FHKH5P5GJSHH", "MA4J1YB8XZP2BPT8"]
    with tm.PricingContext(dt.date.today()):
        for i in range(len(asset_id_list)):
            correct_id = tm.currency_to_inflation_benchmark_rate(asset_id_list[i])
            assert correct_id == correct_mapping[i]


def test_cross_to_basis(mocker):
    mocker.patch.object(GsSession.__class__, 'current',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_get', side_effect=mock_request)
    mocker.patch.object(GsAssetApi, 'map_identifiers', side_effect=map_identifiers_cross_basis_mocker)

    asset_id_list = ["MAYJPCVVF2RWXCES", "MA4B66MW5E27U8P32SB", "nobbid"]
    correct_mapping = ["MA99N6C1KF9078NM", "MA4B66MW5E27U8P32SB", "nobbid"]
    with tm.PricingContext(dt.date.today()):
        for i in range(len(asset_id_list)):
            correct_id = tm.cross_to_basis(asset_id_list[i])
            assert correct_id == correct_mapping[i]


def test_cross_stored_direction_for_fx_vol(mocker):
    mocker.patch.object(GsSession.__class__, 'current',
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
    mocker.patch.object(GsSession.__class__, 'current',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_get', side_effect=mock_request)
    mocker.patch.object(GsSession.current, '_post', side_effect=mock_request)
    asset_id_list = ["MAYJPCVVF2RWXCES", "MATGYV0J9MPX534Z"]
    correct_mapping = ["MATGYV0J9MPX534Z", "MATGYV0J9MPX534Z"]
    with tm.PricingContext(dt.date.today()):
        for i in range(len(asset_id_list)):
            correct_id = tm.cross_to_usd_based_cross(asset_id_list[i])
            assert correct_id == correct_mapping[i]


def mock_commod(_cls, _q):
    d = {
        'price': [30, 30, 30, 30, 35.929686, 35.636039, 27.307498, 23.23177, 19.020833, 18.827291, 17.823749, 17.393958,
                  17.824999, 20.307603, 24.311249, 25.160103, 25.245728, 25.736873, 28.425206, 28.779789, 30.519996,
                  34.896348, 33.966973, 33.95489, 33.686348, 34.840307, 32.674163, 30.261665, 30, 30, 30]
    }
    return pd.DataFrame(data=d, index=pd.date_range('2019-05-01', periods=31, freq='H', tz=timezone('UTC')))


def mock_fx(_cls, _q):
    d = {
        'deltaStrike': ['25DP', '25DC', 'ATMS'],
        'impliedVolatility': [5, 1, 2],
        'forecast': [1.1, 1.1, 1.1]
    }
    return pd.DataFrame(data=d, index=_index * 3)


def mock_fx_empty(_cls, _q):
    d = {
        'deltaStrike': [],
        'impliedVolatility': []
    }
    return pd.DataFrame(data=d, index=[])


def mock_fx_switch(_cls, _q, _n):
    replace = Replacer()
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_fx_empty)
    replace.restore()
    return Cross('MA1889', 'ABC/XYZ')


def mock_curr(_cls, _q):
    d = {
        'swapRate': [1, 2, 3],
        'swaptionVol': [1, 2, 3],
        'atmFwdRate': [1, 2, 3],
        'midcurveVol': [1, 2, 3],
        'capFloorVol': [1, 2, 3],
        'spreadOptionVol': [1, 2, 3],
        'inflationSwapRate': [1, 2, 3],
        'midcurveAtmFwdRate': [1, 2, 3],
        'capFloorAtmFwdRate': [1, 2, 3],
        'spreadOptionAtmFwdRate': [1, 2, 3]
    }
    return pd.DataFrame(data=d, index=_index * 3)


def mock_cross(_cls, _q):
    d = {
        'basis': [1, 2, 3],
    }
    return pd.DataFrame(data=d, index=_index * 3)


def mock_eq(_cls, _q):
    d = {
        'relativeStrike': [0.75, 0.25, 0.5],
        'impliedVolatility': [5, 1, 2],
        'impliedCorrelation': [5, 1, 2],
        'averageImpliedVolatility': [5, 1, 2],
        'averageImpliedVariance': [5, 1, 2],
        'impliedVolatilityByDeltaStrike': [5, 1, 2]
    }
    return pd.DataFrame(data=d, index=_index * 3)


def mock_eq_norm(_cls, _q):
    d = {
        'relativeStrike': [-4.0, 4.0, 0],
        'impliedVolatility': [5, 1, 2]
    }
    return pd.DataFrame(data=d, index=_index * 3)


def mock_eq_spot(_cls, _q):
    d = {
        'relativeStrike': [0.75, 1.25, 1.0],
        'impliedVolatility': [5, 1, 2]
    }
    return pd.DataFrame(data=d, index=_index * 3)


def mock_inc(_cls, _q):
    d = {
        'relativeStrike': [0.25, 0.75],
        'impliedVolatility': [5, 1]
    }
    return pd.DataFrame(data=d, index=_index * 2)


def test_skew():
    replace = Replacer()

    mock_spx = Index('MA890', AssetClass.Equity, 'SPX')
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_eq)
    actual = tm.skew(mock_spx, '1m', tm.SkewReference.DELTA, 25)
    assert_series_equal(pd.Series([2.0], index=_index, name='impliedVolatility'), actual)

    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_eq_norm)
    actual = tm.skew(mock_spx, '1m', tm.SkewReference.NORMALIZED, 4)
    assert_series_equal(pd.Series([2.0], index=_index, name='impliedVolatility'), actual)

    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_eq_spot)
    actual = tm.skew(mock_spx, '1m', tm.SkewReference.SPOT, 25)
    assert_series_equal(pd.Series([2.0], index=_index, name='impliedVolatility'), actual)

    mock = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    mock.return_value = pd.DataFrame()
    assert tm.skew(mock_spx, '1m', tm.SkewReference.SPOT, 25).empty

    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_inc)
    with pytest.raises(MqError):
        tm.skew(mock_spx, '1m', tm.SkewReference.DELTA, 25)
    replace.restore()

    with pytest.raises(MqError):
        tm.skew(mock_spx, '1m', None, 25)

    with pytest.raises(MqError):
        tm.skew(mock_spx, '1m', tm.SkewReference.SPOT, 25, real_time=True)


def test_skew_fx():
    replace = Replacer()
    mock = Cross('MAA0NE9QX2ABETG6', 'USD/EUR')
    xrefs = replace('gs_quant.timeseries.measures.GsAssetApi.get_asset_xrefs', Mock())
    xrefs.return_value = [GsTemporalXRef(dt.date(2019, 1, 1), dt.date(2952, 12, 31), XRef(bbid='EURUSD', ))]
    replace('gs_quant.markets.securities.SecurityMaster.get_asset', mock)
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_fx)
    actual = tm.skew(Cross('MAA0NE9QX2ABETG6', 'USD/EUR'), '1m', None, 25)
    assert_series_equal(pd.Series([2.0], index=_index, name='impliedVolatility'), actual)
    replace.restore()


def test_vol():
    replace = Replacer()
    mock_spx = Index('MA890', AssetClass.Equity, 'SPX')
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_eq)
    actual = tm.implied_volatility(mock_spx, '1m', tm.VolReference.DELTA_CALL, 25)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='impliedVolatility'), actual)
    actual = tm.implied_volatility(mock_spx, '1m', tm.VolReference.DELTA_PUT, 75)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='impliedVolatility'), actual)
    with pytest.raises(NotImplementedError):
        tm.implied_volatility(mock_spx, '1m', tm.VolReference.DELTA_NEUTRAL)
    replace.restore()


def test_vol_fx():
    replace = Replacer()

    mock = Cross('MAA0NE9QX2ABETG6', 'USD/EUR')
    xrefs = replace('gs_quant.timeseries.measures.GsAssetApi.get_asset_xrefs', Mock())
    xrefs.return_value = [GsTemporalXRef(dt.date(2019, 1, 1), dt.date(2952, 12, 31), XRef(bbid='EURUSD', ))]
    replace('gs_quant.markets.securities.SecurityMaster.get_asset', mock)

    # for different delta strikes
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_fx)
    actual = tm.implied_volatility(mock, '1m', tm.VolReference.DELTA_CALL, 25)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='impliedVolatility'), actual)
    actual = tm.implied_volatility(mock, '1m', tm.VolReference.DELTA_PUT, 25)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='impliedVolatility'), actual)
    actual = tm.implied_volatility(mock, '1m', tm.VolReference.DELTA_NEUTRAL)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='impliedVolatility'), actual)
    actual = tm.implied_volatility(mock, '1m', tm.VolReference.FORWARD, 100)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='impliedVolatility'), actual)
    actual = tm.implied_volatility(mock, '1m', tm.VolReference.SPOT, 100)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='impliedVolatility'), actual)
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


def test_vol_forecast():
    replace = Replacer()
    mock = Cross('MAA0NE9QX2ABETG6', 'USD/EUR')
    xrefs = replace('gs_quant.timeseries.measures.GsAssetApi.get_asset_xrefs', Mock())
    xrefs.return_value = [GsTemporalXRef(dt.date(2019, 1, 1), dt.date(2952, 12, 31), XRef(bbid='EURUSD', ))]
    replace('gs_quant.markets.securities.SecurityMaster.get_asset', mock)
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_fx)
    actual = tm.forecast(mock, '1y')
    assert_series_equal(pd.Series([1.1, 1.1, 1.1], index=_index * 3, name='forecast'), actual)
    actual = tm.forecast(mock, '3m')
    assert_series_equal(pd.Series([1.1, 1.1, 1.1], index=_index * 3, name='forecast'), actual)
    with pytest.raises(NotImplementedError):
        tm.forecast(mock, '1y', real_time=True)
    replace.restore()


def test_vol_forecast_inverse():
    replace = Replacer()
    get_cross = replace('gs_quant.timeseries.measures.cross_to_usd_based_cross', Mock())
    get_cross.return_value = "MATGYV0J9MPX534Z"
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_fx)

    mock = Cross("MAYJPCVVF2RWXCES", 'USD/JPY')
    actual = tm.forecast(mock, '3m')
    assert_series_equal(pd.Series([1 / 1.1, 1 / 1.1, 1 / 1.1], index=_index * 3, name='forecast'), actual)
    replace.restore()


def test_vol_smile():
    replace = Replacer()
    mock_spx = Index('MA890', AssetClass.Equity, 'SPX')
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_eq)
    actual = tm.vol_smile(mock_spx, '1m', tm.VolSmileReference.FORWARD, '5d')
    assert_series_equal(pd.Series([5, 1, 2], index=[0.75, 0.25, 0.5]), actual)
    actual = tm.vol_smile(mock_spx, '1m', tm.VolSmileReference.SPOT, '5d')
    assert_series_equal(pd.Series([5, 1, 2], index=[0.75, 0.25, 0.5]), actual)

    market_mock = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    market_mock.return_value = pd.DataFrame()
    actual = tm.vol_smile(mock_spx, '1m', tm.VolSmileReference.SPOT, '1d')
    assert actual.empty
    market_mock.assert_called_once()
    with pytest.raises(NotImplementedError):
        tm.vol_smile(mock_spx, '1m', tm.VolSmileReference.SPOT, '1d', real_time=True)
    replace.restore()


def test_impl_corr():
    replace = Replacer()
    mock_spx = Index('MA890', AssetClass.Equity, 'SPX')
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_eq)
    actual = tm.implied_correlation(mock_spx, '1m', tm.EdrDataReference.DELTA_CALL, 25)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='impliedCorrelation'), actual)
    actual = tm.implied_correlation(mock_spx, '1m', tm.EdrDataReference.DELTA_PUT, 75)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='impliedCorrelation'), actual)
    with pytest.raises(NotImplementedError):
        tm.implied_correlation(..., '1m', tm.EdrDataReference.DELTA_PUT, 75, real_time=True)
    replace.restore()


def test_cds_implied_vol():
    replace = Replacer()
    mock_cds = Index('MA890', AssetClass.Equity, 'CDS')
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_eq)
    actual = tm.cds_implied_volatility(mock_cds, '1m', '5y', tm.CdsVolReference.DELTA_CALL, 10)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='impliedVolatilityByDeltaStrike'), actual)
    actual = tm.cds_implied_volatility(mock_cds, '1m', '5y', tm.CdsVolReference.FORWARD, 100)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='impliedVolatilityByDeltaStrike'), actual)
    with pytest.raises(NotImplementedError):
        tm.cds_implied_volatility(..., '1m', '5y', tm.CdsVolReference.DELTA_PUT, 75, real_time=True)
    replace.restore()


def test_avg_impl_vol():
    replace = Replacer()
    mock_spx = Index('MA890', AssetClass.Equity, 'SPX')
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_eq)
    actual = tm.average_implied_volatility(mock_spx, '1m', tm.EdrDataReference.DELTA_CALL, 25)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='averageImpliedVolatility'), actual)
    actual = tm.average_implied_volatility(mock_spx, '1m', tm.EdrDataReference.DELTA_PUT, 75)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='averageImpliedVolatility'), actual)
    with pytest.raises(NotImplementedError):
        tm.average_implied_volatility(..., '1m', tm.EdrDataReference.DELTA_PUT, 75, real_time=True)
    replace.restore()


def test_avg_impl_var():
    replace = Replacer()
    mock_spx = Index('MA890', AssetClass.Equity, 'SPX')
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_eq)
    actual = tm.average_implied_variance(mock_spx, '1m', tm.EdrDataReference.DELTA_CALL, 25)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='averageImpliedVariance'), actual)
    actual = tm.average_implied_variance(mock_spx, '1m', tm.EdrDataReference.DELTA_PUT, 75)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='averageImpliedVariance'), actual)
    with pytest.raises(NotImplementedError):
        tm.average_implied_variance(..., '1m', tm.EdrDataReference.DELTA_PUT, 75, real_time=True)
    replace.restore()


def test_swap_rate():
    replace = Replacer()
    mock_usd = Currency('MA890', 'USD')

    xrefs = replace('gs_quant.timeseries.measures.GsAssetApi.get_asset_xrefs', Mock())
    xrefs.return_value = [GsTemporalXRef(dt.date(2019, 1, 1), dt.date(2952, 12, 31), XRef(bbid='USD', ))]
    identifiers = replace('gs_quant.timeseries.measures.GsAssetApi.map_identifiers', Mock())
    identifiers.return_value = {'USD-3m': 'MA123'}
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_curr)
    actual = tm.swap_rate(mock_usd, '1y')
    assert_series_equal(pd.Series([1, 2, 3], index=_index * 3, name='swapRate'), actual)

    identifiers = replace('gs_quant.timeseries.measures.GsAssetApi.map_identifiers', Mock())
    identifiers.return_value = {'USD OIS': 'MA123'}
    actual = tm.swap_rate(mock_usd, '1y', BenchmarkType.OIS)
    assert_series_equal(pd.Series([1, 2, 3], index=_index * 3, name='swapRate'), actual)

    mock_eur = Currency('MA890', 'EUR')
    xrefs = replace('gs_quant.timeseries.measures.GsAssetApi.get_asset_xrefs', Mock())
    xrefs.return_value = [GsTemporalXRef(dt.date(2019, 1, 1), dt.date(2952, 12, 31), XRef(bbid='EUR', ))]
    identifiers = replace('gs_quant.timeseries.measures.GsAssetApi.map_identifiers', Mock())
    identifiers.return_value = {'EUR-6m': 'MA123'}
    actual = tm.swap_rate(mock_eur, '1y')
    assert_series_equal(pd.Series([1, 2, 3], index=_index * 3, name='swapRate'), actual)

    mock_sek = Currency('MA890', 'SEK')
    xrefs = replace('gs_quant.timeseries.measures.GsAssetApi.get_asset_xrefs', Mock())
    xrefs.return_value = [GsTemporalXRef(dt.date(2019, 1, 1), dt.date(2952, 12, 31), XRef(bbid='SEK', ))]
    identifiers = replace('gs_quant.timeseries.measures.GsAssetApi.map_identifiers', Mock())
    identifiers.return_value = {'SEK-6m': 'MA123'}
    actual = tm.swap_rate(mock_sek, '1y')
    assert_series_equal(pd.Series([1, 2, 3], index=_index * 3, name='swapRate'), actual)

    with pytest.raises(NotImplementedError):
        tm.swap_rate(..., '1y', real_time=True)

    replace.restore()


def test_swaption_vol():
    replace = Replacer()
    mock_usd = Currency('MA890', 'USD')
    xrefs = replace('gs_quant.timeseries.measures.GsAssetApi.get_asset_xrefs', Mock())
    xrefs.return_value = [GsTemporalXRef(dt.date(2019, 1, 1), dt.date(2952, 12, 31), XRef(bbid='USD', ))]
    identifiers = replace('gs_quant.timeseries.measures.GsAssetApi.map_identifiers', Mock())
    identifiers.return_value = {'USD-LIBOR-BBA': 'MA123'}
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_curr)
    actual = tm.swaption_vol(mock_usd, '3m', '1y', 0)
    assert_series_equal(pd.Series([1, 2, 3], index=_index * 3, name='swaptionVol'), actual)
    actual = tm.swaption_vol(mock_usd, '3m', '1y', 50)
    assert_series_equal(pd.Series([1, 2, 3], index=_index * 3, name='swaptionVol'), actual)
    actual = tm.swaption_vol(mock_usd, '3m', '1y', -50)
    assert_series_equal(pd.Series([1, 2, 3], index=_index * 3, name='swaptionVol'), actual)
    with pytest.raises(NotImplementedError):
        tm.swaption_vol(..., '3m', '1y', 50, real_time=True)
    replace.restore()


def test_swaption_atm_fwd_rate():
    replace = Replacer()
    mock_usd = Currency('MA890', 'USD')
    xrefs = replace('gs_quant.timeseries.measures.GsAssetApi.get_asset_xrefs', Mock())
    xrefs.return_value = [GsTemporalXRef(dt.date(2019, 1, 1), dt.date(2952, 12, 31), XRef(bbid='USD', ))]
    identifiers = replace('gs_quant.timeseries.measures.GsAssetApi.map_identifiers', Mock())
    identifiers.return_value = {'USD-LIBOR-BBA': 'MA123'}
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_curr)
    actual = tm.swaption_atm_fwd_rate(mock_usd, '3m', '1y')
    assert_series_equal(pd.Series([1, 2, 3], index=_index * 3, name='atmFwdRate'), actual)
    with pytest.raises(NotImplementedError):
        tm.swaption_atm_fwd_rate(..., '3m', '1y', real_time=True)
    replace.restore()


def test_midcurve_vol():
    replace = Replacer()
    mock_usd = Currency('MA890', 'USD')
    xrefs = replace('gs_quant.timeseries.measures.GsAssetApi.get_asset_xrefs', Mock())
    xrefs.return_value = [GsTemporalXRef(dt.date(2019, 1, 1), dt.date(2952, 12, 31), XRef(bbid='USD', ))]
    identifiers = replace('gs_quant.timeseries.measures.GsAssetApi.map_identifiers', Mock())
    identifiers.return_value = {'USD-LIBOR-BBA': 'MA123'}
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_curr)
    actual = tm.midcurve_vol(mock_usd, '3m', '1y', '1y', 50)
    assert_series_equal(pd.Series([1, 2, 3], index=_index * 3, name='midcurveVol'), actual)
    with pytest.raises(NotImplementedError):
        tm.midcurve_vol(..., '3m', '1y', '1y', 50, real_time=True)
    replace.restore()


def test_midcurve_atm_fwd_rate():
    replace = Replacer()
    mock_usd = Currency('MA890', 'USD')
    xrefs = replace('gs_quant.timeseries.measures.GsAssetApi.get_asset_xrefs', Mock())
    xrefs.return_value = [GsTemporalXRef(dt.date(2019, 1, 1), dt.date(2952, 12, 31), XRef(bbid='USD', ))]
    identifiers = replace('gs_quant.timeseries.measures.GsAssetApi.map_identifiers', Mock())
    identifiers.return_value = {'USD-LIBOR-BBA': 'MA123'}
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_curr)
    actual = tm.midcurve_atm_fwd_rate(mock_usd, '3m', '1y', '1y')
    assert_series_equal(pd.Series([1, 2, 3], index=_index * 3, name='midcurveAtmFwdRate'), actual)
    with pytest.raises(NotImplementedError):
        tm.midcurve_atm_fwd_rate(..., '3m', '1y', '1y', real_time=True)
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
    assert_series_equal(pd.Series([1, 2, 3], index=_index * 3, name='capFloorVol'), actual)
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
    assert_series_equal(pd.Series([1, 2, 3], index=_index * 3, name='capFloorAtmFwdRate'), actual)
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
    assert_series_equal(pd.Series([1, 2, 3], index=_index * 3, name='spreadOptionVol'), actual)
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
    assert_series_equal(pd.Series([1, 2, 3], index=_index * 3, name='spreadOptionAtmFwdRate'), actual)
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
    assert_series_equal(pd.Series([1, 2, 3], index=_index * 3, name='inflationSwapRate'), actual)
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
    assert_series_equal(pd.Series([1, 2, 3], index=_index * 3, name='basis'), actual)
    with pytest.raises(NotImplementedError):
        tm.basis(..., '1y', real_time=True)
    replace.restore()


def test_td():
    cases = {'3d': pd.DateOffset(days=3), '9w': pd.DateOffset(weeks=9), '2m': pd.DateOffset(months=2),
             '10y': pd.DateOffset(years=10)}
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


def test_var_swap():
    idx = pd.date_range(start="2019-01-01", periods=4, freq="D")
    data = {
        'varSwap': [1, 2, 3, 4]
    }
    out = pd.DataFrame(data=data, index=idx)

    replace = Replacer()
    market_mock = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    market_mock.return_value = out

    expected = pd.Series([1, 2, 3, 4], name='varSwap', index=idx)
    actual = tm.var_swap(Index('MA123', AssetClass.Equity, '123'), '1m')
    assert_series_equal(expected, actual)
    market_mock.assert_called_once()

    market_mock.reset_mock()
    market_mock.return_value = pd.DataFrame()
    actual = tm.var_swap(Index('MA123', AssetClass.Equity, '123'), '1m')
    assert actual.empty
    replace.restore()


def test_var_swap_fwd():
    # bad input
    with pytest.raises(MqError):
        tm.var_swap(Index('MA123', AssetClass.Equity, '123'), '1m', 500)

    # regular
    idx = pd.date_range(start="2019-01-01", periods=4, freq="D")
    d1 = {
        'varSwap': [1, 2, 3, 4],
        'tenor': ['1y'] * 4
    }
    d2 = {
        'varSwap': [1.5, 2.5, 3.5, 4.5],
        'tenor': ['13m'] * 4
    }
    df1 = pd.DataFrame(data=d1, index=idx)
    df2 = pd.DataFrame(data=d2, index=idx)
    out = pd.concat([df1, df2])

    replace = Replacer()
    market_mock = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    market_mock.return_value = out

    tenors_mock = replace('gs_quant.timeseries.measures._var_swap_tenors', Mock())
    tenors_mock.return_value = ['1m', '1y', '13m']

    expected = pd.Series([7.5, 8.5, 9.5, 10.5], name='varSwap', index=idx)
    actual = tm.var_swap(Index('MA123', AssetClass.Equity, '123'), '1m', '1y')
    assert_series_equal(expected, actual)
    market_mock.assert_called_once()

    # no data
    market_mock.return_value = pd.DataFrame()
    assert tm.var_swap(Index('MA123', AssetClass.Equity, '123'), '1m', '1y').empty

    # no data for a tenor
    market_mock.return_value = pd.DataFrame(data=d1, index=idx)
    assert tm.var_swap(Index('MA123', AssetClass.Equity, '123'), '1m', '1y').empty

    # no such tenors
    tenors_mock.return_value = []
    assert tm.var_swap(Index('MA123', AssetClass.Equity, '123'), '1m', '1y').empty

    # finish
    replace.restore()


def _var_term_typical():
    assert DataContext.current_is_set
    data = {
        'tenor': ['1w', '2w', '1y', '2y'],
        'varSwap': [1, 2, 3, 4]
    }
    out = pd.DataFrame(data=data, index=pd.DatetimeIndex(['2018-01-01'] * 4))

    replace = Replacer()
    market_mock = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    market_mock.return_value = out

    actual = tm.var_term(Index('MA123', AssetClass.Equity, '123'))
    idx = pd.DatetimeIndex(['2018-01-08', '2018-01-15', '2019-01-01', '2020-01-01'], name='varSwap')
    expected = pd.Series([1, 2, 3, 4], name='varSwap', index=idx)
    expected = expected.loc[DataContext.current.start_date: DataContext.current.end_date]

    if expected.empty:
        assert actual.empty
    else:
        assert_series_equal(expected, actual, check_names=False)
    market_mock.assert_called_once()

    replace.restore()
    return actual


def _var_term_empty():
    replace = Replacer()
    market_mock = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    market_mock.return_value = pd.DataFrame()

    actual = tm.var_term(Index('MAXYZ', AssetClass.Equity, 'XYZ'))
    assert actual.empty
    market_mock.assert_called_once()
    replace.restore()


def _var_term_fwd():
    idx = pd.date_range('2018-01-01', periods=2, freq='D')

    def mock_var_swap(_asset, tenor, _forward_start_date, **_kwargs):
        if tenor == '1m':
            return pd.Series([1, 2], idx, name='varSwap')
        if tenor == '2m':
            return pd.Series([3, 4], idx, name='varSwap')
        return pd.Series()

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
        assert_series_equal(expected, actual, check_names=False)
    market_mock.assert_called()

    replace.restore()
    return actual


def test_var_term():
    with DataContext('2018-01-01', '2019-01-01'):
        _var_term_typical()
        _var_term_empty()
        _var_term_fwd()
    with DataContext('2019-01-01', '2019-07-04'):
        _var_term_fwd()
    with DataContext('2018-01-16', '2018-12-31'):
        out = _var_term_typical()
        assert out.empty
    with pytest.raises(MqError):
        tm.var_term(..., pricing_date=300)


def _vol_term_typical(reference, value):
    from gs_quant.target.common import FieldFilterMap

    assert DataContext.current_is_set
    data = {
        'tenor': ['1w', '2w', '1y', '2y'],
        'impliedVolatility': [1, 2, 3, 4]
    }
    out = pd.DataFrame(data=data, index=pd.DatetimeIndex(['2018-01-01'] * 4))

    replace = Replacer()
    market_mock = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    market_mock.return_value = out
    ffm_mock = replace('gs_quant.timeseries.measures.FieldFilterMap', Mock(spec=FieldFilterMap))

    actual = tm.vol_term(Index('MA123', AssetClass.Equity, '123'), reference, value)
    idx = pd.DatetimeIndex(['2018-01-08', '2018-01-15', '2019-01-01', '2020-01-01'], name='expirationDate')
    expected = pd.Series([1, 2, 3, 4], name='impliedVolatility', index=idx)
    expected = expected.loc[DataContext.current.start_date: DataContext.current.end_date]

    if expected.empty:
        assert actual.empty
    else:
        assert_series_equal(expected, actual)
    market_mock.assert_called_once()
    ffm_mock.assert_called_once_with(relativeStrike=value if reference == tm.SkewReference.NORMALIZED else value / 100,
                                     strikeReference=unittest.mock.ANY)
    replace.restore()
    return actual


def _vol_term_empty():
    replace = Replacer()
    market_mock = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    market_mock.return_value = pd.DataFrame()

    actual = tm.vol_term(Index('MAXYZ', AssetClass.Equity, 'XYZ'), tm.SkewReference.DELTA, 777)
    assert actual.empty
    market_mock.assert_called_once()
    replace.restore()


def test_vol_term():
    with DataContext('2018-01-01', '2019-01-01'):
        _vol_term_typical(tm.SkewReference.SPOT, 100)
        _vol_term_typical(tm.SkewReference.NORMALIZED, 4)
        _vol_term_empty()
    with DataContext('2018-01-16', '2018-12-31'):
        out = _vol_term_typical(tm.SkewReference.SPOT, 100)
        assert out.empty
    with pytest.raises(NotImplementedError):
        tm.vol_term(..., tm.SkewReference.SPOT, 100, real_time=True)


def _fwd_term_typical():
    assert DataContext.current_is_set
    data = {
        'tenor': ['1w', '2w', '1y', '2y'],
        'forward': [1, 2, 3, 4]
    }
    out = pd.DataFrame(data=data, index=pd.DatetimeIndex(['2018-01-01'] * 4))

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
        assert_series_equal(expected, actual)
    market_mock.assert_called_once()
    replace.restore()
    return actual


def _fwd_term_empty():
    replace = Replacer()
    market_mock = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    market_mock.return_value = pd.DataFrame()

    actual = tm.fwd_term(Index('MAXYZ', AssetClass.Equity, 'XYZ'))
    assert actual.empty
    market_mock.assert_called_once()
    replace.restore()


def test_fwd_term():
    with DataContext('2018-01-01', '2019-01-01'):
        _fwd_term_typical()
        _fwd_term_empty()
    with DataContext('2018-01-16', '2018-12-31'):
        out = _fwd_term_typical()
        assert out.empty
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
        'CAISO peak': [30.153727375],
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
                            actual)

        actual = tm.bucketize_price(mock_miso, 'LMP', bucket='offpeak')
        assert_series_equal(pd.Series(target['MISO offpeak'],
                                      index=[datetime.date(2019, 5, 1)],
                                      name='price'),
                            actual)

        bbid_mock.return_value = 'CAISO'

        actual = tm.bucketize_price(mock_caiso, 'LMP', bucket='7x24')
        assert_series_equal(pd.Series(target['CAISO 7x24'],
                                      index=[datetime.date(2019, 5, 1)],
                                      name='price'),
                            actual)

        actual = tm.bucketize_price(mock_caiso, 'LMP', bucket='peak')
        assert_series_equal(pd.Series(target['CAISO peak'],
                                      index=[datetime.date(2019, 5, 1)],
                                      name='price'),
                            actual)

        bbid_mock.return_value = 'PJM'

        actual = tm.bucketize_price(mock_pjm, 'LMP', bucket='7x24')
        assert_series_equal(pd.Series(target['7x24'],
                                      index=[datetime.date(2019, 5, 1)],
                                      name='price'),
                            actual)

        actual = tm.bucketize_price(mock_pjm, 'LMP', bucket='offpeak')
        assert_series_equal(pd.Series(target['offpeak'],
                                      index=[datetime.date(2019, 5, 1)],
                                      name='price'),
                            actual)

        actual = tm.bucketize_price(mock_pjm, 'LMP', bucket='peak')
        assert_series_equal(pd.Series(target['peak'],
                                      index=[datetime.date(2019, 5, 1)],
                                      name='price'),
                            actual)

        actual = tm.bucketize_price(mock_pjm, 'LMP', bucket='7x8')
        assert_series_equal(pd.Series(target['7x8'],
                                      index=[datetime.date(2019, 5, 1)],
                                      name='price'),
                            actual)

        actual = tm.bucketize_price(mock_pjm, 'LMP', bucket='2x16h')
        assert_series_equal(pd.Series(target['2x16h'],
                                      index=[],
                                      name='price'),
                            actual)

        actual = tm.bucketize_price(mock_pjm, 'LMP', granularity='m', bucket='7X24')
        assert_series_equal(pd.Series(target['monthly'],
                                      index=[],
                                      name='price'),
                            actual)

        with pytest.raises(ValueError):
            tm.bucketize_price(mock_pjm, 'LMP', bucket='7X24', real_time=True)

        with pytest.raises(ValueError):
            tm.bucketize_price(mock_pjm, 'LMP', bucket='weekday')

        with pytest.raises(ValueError):
            tm.bucketize_price(mock_caiso, 'LMP', bucket='weekday')

        with pytest.raises(ValueError):
            tm.bucketize_price(mock_pjm, 'LMP', granularity='yearly')

    replace.restore()


if __name__ == '__main__':
    pytest.main(args=["test_measures.py"])
