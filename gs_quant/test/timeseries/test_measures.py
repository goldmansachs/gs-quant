import pandas as pd
import pytest
from pandas.testing import assert_series_equal
from gs_quant.errors import MqError
from gs_quant.markets.securities import AssetClass, Cross, Index
from gs_quant.timeseries.measures import SkewReference, VolReference, skew, implied_volatility
from testfixtures import Replacer

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
    actual = skew(Cross('MA123', 'ABCXYZ'), '1m', None, 25)
    assert_series_equal(pd.Series([2.0], index=_index, name='impliedVolatility'), actual)

    mock_spx = Index('MA890', AssetClass.Equity, 'SPX')
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_eq)
    actual = skew(mock_spx, '1m', SkewReference.DELTA, 25)
    assert_series_equal(pd.Series([2.0], index=_index, name='impliedVolatility'), actual)

    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_eq_norm)
    actual = skew(mock_spx, '1m', SkewReference.NORMALIZED, 4)
    assert_series_equal(pd.Series([2.0], index=_index, name='impliedVolatility'), actual)

    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_eq_spot)
    actual = skew(mock_spx, '1m', SkewReference.SPOT, 25)
    assert_series_equal(pd.Series([2.0], index=_index, name='impliedVolatility'), actual)

    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_inc)
    with pytest.raises(MqError):
        skew(mock_spx, '1m', SkewReference.DELTA, 25)
    replace.restore()

    with pytest.raises(MqError):
        skew(mock_spx, '1m', None, 25)

    with pytest.raises(MqError):
        skew(mock_spx, '1m', SkewReference.SPOT, 25, real_time=True)


def test_vol():
    replace = Replacer()
    mock_spx = Index('MA890', AssetClass.Equity, 'SPX')
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_eq)
    actual = implied_volatility(mock_spx, '1m', VolReference.DELTA_CALL, 25)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='impliedVolatility'), actual)
    actual = implied_volatility(mock_spx, '1m', VolReference.DELTA_PUT, 75)
    assert_series_equal(pd.Series([5, 1, 2], index=_index * 3, name='impliedVolatility'), actual)
    replace.restore()

    with pytest.raises(MqError):
        implied_volatility(Cross('ABC', 'DEF'), '1m', VolReference.DELTA_CALL, 25)


if __name__ == '__main__':
    pytest.main()
