from typing import Union

import gs_quant.timeseries.measures as tm
import pandas as pd
import pytest
import datetime
import unittest.mock
from pandas.testing import assert_series_equal
from gs_quant.data.core import DataContext
from gs_quant.errors import MqError
from gs_quant.markets.securities import AssetClass, Cross, Index, Currency
from gs_quant.api.gs.assets import GsTemporalXRef, GsAssetApi, GsIdType, IdList
from gs_quant.session import GsSession, Environment
from gs_quant.target.common import XRef
from gs_quant.test.timeseries.utils import mock_request
from gs_quant.timeseries.measures import BenchmarkType
from testfixtures import Replacer
from testfixtures.mock import Mock
from pytz import timezone
import datetime as dt


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


def test_currency_converter_default_benchmark(mocker):
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
            correct_id = tm.currency_converter_default_benchmark(asset_id_list[i])
            assert correct_id == correct_mapping[i]


def test_currency_converter_inflation_benchmark(mocker):
    mocker.patch.object(GsSession.__class__, 'current',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_get', side_effect=mock_request)
    mocker.patch.object(GsAssetApi, 'map_identifiers', side_effect=map_identifiers_inflation_mocker)

    asset_id_list = ["MA66CZBQJST05XKG", "MAK1FHKH5P5GJSHH", "MA4J1YB8XZP2BPT8", "MA4B66MW5E27U8P32SB"]
    correct_mapping = ["MAQ7ND0MBP2AVVQW", "MAK1FHKH5P5GJSHH", "MA4J1YB8XZP2BPT8", "MA4B66MW5E27U8P32SB"]
    with tm.PricingContext(dt.date.today()):
        for i in range(len(asset_id_list)):
            correct_id = tm.currency_converter_inflation_benchmark(asset_id_list[i])
            assert correct_id == correct_mapping[i]


def mock_commod(_cls, _q):
    d = {
        'price': [35.929686, 35.636039, 27.307498, 23.23177, 19.020833, 18.827291, 17.823749, 17.393958, 17.824999,
                  20.307603, 24.311249, 25.160103, 25.245728, 25.736873, 28.425206, 28.779789, 30.519996, 34.896348,
                  33.966973, 33.95489, 33.686348, 34.840307, 32.674163, 30.261665]
    }
    return pd.DataFrame(data=d, index=pd.date_range('2019-05-01', periods=24, freq='H', tz=timezone('US/Eastern')))


def mock_fx(_cls, _q):
    d = {
        'deltaStrike': ['25DP', '25DC', 'ATMS'],
        'impliedVolatility': [5, 1, 2]
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
        'inflationSwapRate': [1, 2, 3]
    }
    return pd.DataFrame(data=d, index=_index * 3)


def mock_eq(_cls, _q):
    d = {
        'relativeStrike': [0.75, 0.25, 0.5],
        'impliedVolatility': [5, 1, 2],
        'impliedCorrelation': [5, 1, 2],
        'averageImpliedVolatility': [5, 1, 2],
        'averageImpliedVariance': [5, 1, 2],
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
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_fx)
    actual = tm.skew(Cross('MA123', 'ABCXYZ'), '1m', None, 25)
    assert_series_equal(pd.Series([2.0], index=_index, name='impliedVolatility'), actual)

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


def test_vol():
    replace = Replacer()
    mock_spx = Index('MA890', AssetClass.Equity, 'SPX')
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_eq)
    actual = tm.implied_volatility(mock_spx, '1m', tm.VolReference.DELTA_CALL, 25)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='impliedVolatility'), actual)
    actual = tm.implied_volatility(mock_spx, '1m', tm.VolReference.DELTA_PUT, 75)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='impliedVolatility'), actual)
    replace.restore()


def test_vol_fx():
    replace = Replacer()
    # for different delta strikes
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_fx)
    actual = tm.implied_volatility(Cross('MA123', 'ABCXYZ'), '1m', tm.VolReference.DELTA_PUT, 50)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='impliedVolatility'), actual)
    actual = tm.implied_volatility(Cross('MA123', 'ABCXYZ'), '1m', tm.VolReference.DELTA_PUT, 25)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='impliedVolatility'), actual)
    actual = tm.implied_volatility(Cross('MA123', 'ABCXYZ'), '1m', tm.VolReference.FORWARD, 100)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='impliedVolatility'), actual)
    actual = tm.implied_volatility(Cross('MA123', 'ABCXYZ'), '1m', tm.VolReference.SPOT, 100)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='impliedVolatility'), actual)
    # NORMALIZED not supported
    with pytest.raises(MqError):
        tm.implied_volatility(Cross('MA123', 'ABCXYZ'), '1m', tm.VolReference.NORMALIZED, 25)
    with pytest.raises(MqError):
        tm.implied_volatility(Cross('MA123', 'ABCXYZ'), '1m', tm.VolReference.SPOT, 25)
    with pytest.raises(MqError):
        tm.implied_volatility(Cross('MA123', 'ABCXYZ'), '1m', tm.VolReference.FORWARD, 25)
    # triggers error if empty and name does not contain '/'
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_fx_empty)
    with pytest.raises(MqError):
        tm.implied_volatility(Cross('MA123', 'ABCXYZ'), '1m', tm.VolReference.DELTA_CALL, 25)
    # checking if reverse cross data is available
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_fx_empty)
    replace('gs_quant.markets.securities.SecurityMaster.get_asset', mock_fx_switch)
    xyz = Cross("MA1889", "XYZ/ABC")
    assert tm.implied_volatility(xyz, '1m', tm.VolReference.DELTA_PUT, 25).empty
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
    replace.restore()


def test_impl_corr():
    replace = Replacer()
    mock_spx = Index('MA890', AssetClass.Equity, 'SPX')
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_eq)
    actual = tm.implied_correlation(mock_spx, '1m', tm.EdrDataReference.DELTA_CALL, 25)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='impliedCorrelation'), actual)
    actual = tm.implied_correlation(mock_spx, '1m', tm.EdrDataReference.DELTA_PUT, 75)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='impliedCorrelation'), actual)
    replace.restore()


def test_avg_impl_vol():
    replace = Replacer()
    mock_spx = Index('MA890', AssetClass.Equity, 'SPX')
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_eq)
    actual = tm.average_implied_volatility(mock_spx, '1m', tm.EdrDataReference.DELTA_CALL, 25)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='averageImpliedVolatility'), actual)
    actual = tm.average_implied_volatility(mock_spx, '1m', tm.EdrDataReference.DELTA_PUT, 75)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='averageImpliedVolatility'), actual)
    replace.restore()


def test_avg_impl_var():
    replace = Replacer()
    mock_spx = Index('MA890', AssetClass.Equity, 'SPX')
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_eq)
    actual = tm.average_implied_variance(mock_spx, '1m', tm.EdrDataReference.DELTA_CALL, 25)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='averageImpliedVariance'), actual)
    actual = tm.average_implied_variance(mock_spx, '1m', tm.EdrDataReference.DELTA_PUT, 75)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='averageImpliedVariance'), actual)
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
    replace.restore()


def test_swaption_atm_forward_rate():
    replace = Replacer()
    mock_usd = Currency('MA890', 'USD')
    xrefs = replace('gs_quant.timeseries.measures.GsAssetApi.get_asset_xrefs', Mock())
    xrefs.return_value = [GsTemporalXRef(dt.date(2019, 1, 1), dt.date(2952, 12, 31), XRef(bbid='USD', ))]
    identifiers = replace('gs_quant.timeseries.measures.GsAssetApi.map_identifiers', Mock())
    identifiers.return_value = {'USD-LIBOR-BBA': 'MA123'}
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_curr)
    actual = tm.swaption_atm_forward_rate(mock_usd, '3m', '1y')
    assert_series_equal(pd.Series([1, 2, 3], index=_index * 3, name='atmFwdRate'), actual)
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
        'CAISO 7x24': [26.518563]
    }

    replace = Replacer()
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_commod)
    mock_pjm = Index('MA001', AssetClass.Commod, 'PJM')
    mock_caiso = Index('MA001', AssetClass.Commod, 'CAISO')
    mock_miso = Index('MA001', AssetClass.Commod, 'MISO')

    with DataContext(datetime.date(2019, 5, 1), datetime.date(2019, 5, 1)):
        bbid_mock = replace('gs_quant.timeseries.measures.Asset.get_identifier', Mock())
        bbid_mock.return_value = 'CAISO'

        actual = tm.bucketize_price(mock_caiso, 'LMP', 'totalPrice', bucket='7x24')
        assert_series_equal(pd.Series(target['CAISO 7x24'],
                                      index=[datetime.date(2019, 5, 1)],
                                      name='price'),
                            actual)

        bbid_mock.return_value = 'PJM'

        actual = tm.bucketize_price(mock_pjm, 'LMP', 'totalPrice', bucket='7x24')
        assert_series_equal(pd.Series(target['7x24'],
                                      index=[datetime.date(2019, 5, 1)],
                                      name='price'),
                            actual)

        actual = tm.bucketize_price(mock_pjm, 'LMP', 'totalPrice', bucket='offpeak')
        assert_series_equal(pd.Series(target['offpeak'],
                                      index=[datetime.date(2019, 5, 1)],
                                      name='price'),
                            actual)

        actual = tm.bucketize_price(mock_pjm, 'LMP', 'totalPrice', bucket='peak')
        assert_series_equal(pd.Series(target['peak'],
                                      index=[datetime.date(2019, 5, 1)],
                                      name='price'),
                            actual)

        actual = tm.bucketize_price(mock_pjm, 'LMP', 'totalPrice', bucket='7x8')
        assert_series_equal(pd.Series(target['7x8'],
                                      index=[datetime.date(2019, 5, 1)],
                                      name='price'),
                            actual)

        actual = tm.bucketize_price(mock_pjm, 'LMP', 'totalPrice', bucket='2x16h')
        assert_series_equal(pd.Series(target['2x16h'],
                                      index=[],
                                      name='price'),
                            actual)

        actual = tm.bucketize_price(mock_pjm, 'LMP', 'totalPrice', granularity='m', bucket='7X24')
        assert_series_equal(pd.Series(target['monthly'],
                                      index=[],
                                      name='price'),
                            actual)

        with pytest.raises(ValueError):
            tm.bucketize_price(mock_pjm, 'LMP', 'totalPrice', bucket='weekday')

        with pytest.raises(ValueError):
            tm.bucketize_price(mock_pjm, 'LMP', 'totalPrice', granularity='yearly')

    replace.restore()


if __name__ == '__main__':
    pytest.main(args=["test_measures.py"])
