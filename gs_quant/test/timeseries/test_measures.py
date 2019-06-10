import gs_quant.timeseries.measures as tm
import pandas as pd
import pytest
import unittest.mock
from pandas.testing import assert_series_equal
from gs_quant.data.core import DataContext
from gs_quant.errors import MqError
from gs_quant.markets.securities import AssetClass, Cross, Index
from testfixtures import Replacer
from testfixtures.mock import Mock

_index = [pd.Timestamp('2019-01-01')]


def mock_fx(_cls, _q):
    d = {
        'deltaStrike': ['25DP', '25DC', 'ATMS'],
        'impliedVolatility': [5, 1, 2]
    }
    return pd.DataFrame(data=d, index=_index * 3)


def mock_eq(_cls, _q):
    d = {
        'relativeStrike': [0.75, 0.25, 0.5],
        'impliedVolatility': [5, 1, 2]
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
    import pandas.tseries.offsets

    given = datetime.date(2019, 4, 20)
    s, e = tm._range_from_pricing_date('NYSE', given)
    assert s == e == given

    class MockDate(datetime.date):
        @classmethod
        def today(cls):
            return cls(2019, 5, 25)

    replace = Replacer()
    cbd = replace('gs_quant.timeseries.measures._get_custom_bd', Mock())
    cbd.return_value = pd.tseries.offsets.BusinessDay()

    gold = datetime.date
    datetime.date = MockDate
    s, e = tm._range_from_pricing_date('ANY')
    assert s.year == 2019
    assert s.month == 5
    assert s.day == 24
    assert e == datetime.date(2019, 5, 25)
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


if __name__ == '__main__':
    pytest.main()
