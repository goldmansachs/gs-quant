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

import pandas as pd
import pytest
from unittest.mock import Mock, MagicMock

import gs_quant.timeseries.measures_tba as tm_cpn
from gs_quant.errors import MqValueError

_index = [pd.Timestamp('2024-01-02'), pd.Timestamp('2024-01-03')]


def _mock_asset(name: str) -> Mock:
    """Create a minimal mock Asset."""
    mock = Mock()
    mock.name = name
    mock.get_marquee_id.return_value = 'MA_TEST'
    return mock


def test_cpn_swap(mocker):
    """cpn_swap returns price(FNM 5.00) - price(FNM 4.50)."""
    df_500 = pd.DataFrame({'price3pmClose': [100.5, 101.0]}, index=_index)
    df_450 = pd.DataFrame({'price3pmClose': [99.0, 99.5]}, index=_index)

    def _get_data_side_effect(fields=None, name=None):
        if name == 'FNM 4.50':
            return df_450
        elif name == 'FNM 5.00':
            return df_500
        return pd.DataFrame()

    mock_ds_instance = MagicMock()
    mock_ds_instance.get_data.side_effect = _get_data_side_effect
    mocker.patch.object(tm_cpn, 'Dataset', return_value=mock_ds_instance)

    fnm = _mock_asset('FNM')
    result = tm_cpn.cpn_swap(fnm, 5)

    assert isinstance(result, pd.Series)
    assert len(result) == 2
    # price(FNM 5.00) - price(FNM 4.50)
    assert result.iloc[0] == pytest.approx(1.5)  # 100.5 - 99.0
    assert result.iloc[1] == pytest.approx(1.5)  # 101.0 - 99.5


def test_cpn_swap_real_time_raises():
    """cpn_swap raises MqValueError when real_time=True."""
    fnm = _mock_asset('FNM')
    with pytest.raises(MqValueError, match='real-time'):
        tm_cpn.cpn_swap(fnm, 5, real_time=True)


def test_cpn_swap_float_coupon(mocker):
    """cpn_swap works with a float coupon value like 5.5 → fetches 5.50 and 5.00."""
    df_550 = pd.DataFrame({'price3pmClose': [102.0]}, index=[_index[0]])
    df_500 = pd.DataFrame({'price3pmClose': [100.0]}, index=[_index[0]])

    def _get_data_side_effect(fields=None, name=None):
        if name == 'FNM 5.00':
            return df_500
        elif name == 'FNM 5.50':
            return df_550
        return pd.DataFrame()

    mock_ds_instance = MagicMock()
    mock_ds_instance.get_data.side_effect = _get_data_side_effect
    mocker.patch.object(tm_cpn, 'Dataset', return_value=mock_ds_instance)

    fnm = _mock_asset('FNM')
    result = tm_cpn.cpn_swap(fnm, 5.5)

    assert len(result) == 1
    # price(FNM 5.50) - price(FNM 5.00)
    assert result.iloc[0] == pytest.approx(2.0)


def test_cpn_swap_empty_data(mocker):
    """cpn_swap returns empty series when no data is available."""
    mock_ds_instance = MagicMock()
    mock_ds_instance.get_data.return_value = pd.DataFrame()
    mocker.patch.object(tm_cpn, 'Dataset', return_value=mock_ds_instance)

    fnm = _mock_asset('FNM')
    result = tm_cpn.cpn_swap(fnm, 6)

    assert isinstance(result, pd.Series)
    assert len(result) == 0


def test_butterfly(mocker):
    """butterfly returns 2*price(middle) - price(lower) - price(upper)."""
    df_450 = pd.DataFrame({'price3pmClose': [99.0, 99.5]}, index=_index)
    df_500 = pd.DataFrame({'price3pmClose': [100.5, 101.0]}, index=_index)
    df_550 = pd.DataFrame({'price3pmClose': [101.0, 101.5]}, index=_index)

    def _get_data_side_effect(fields=None, name=None):
        if name == 'FNM 4.50':
            return df_450
        elif name == 'FNM 5.00':
            return df_500
        elif name == 'FNM 5.50':
            return df_550
        return pd.DataFrame()

    mock_ds_instance = MagicMock()
    mock_ds_instance.get_data.side_effect = _get_data_side_effect
    mocker.patch.object(tm_cpn, 'Dataset', return_value=mock_ds_instance)

    fnm = _mock_asset('FNM')
    result = tm_cpn.butterfly(fnm, 5)

    assert isinstance(result, pd.Series)
    assert len(result) == 2
    # 2*100.5 - 99.0 - 101.0 = 1.0
    assert result.iloc[0] == pytest.approx(1.0)
    # 2*101.0 - 99.5 - 101.5 = 1.0
    assert result.iloc[1] == pytest.approx(1.0)


def test_butterfly_real_time_raises():
    """butterfly raises MqValueError when real_time=True."""
    fnm = _mock_asset('FNM')
    with pytest.raises(MqValueError, match='real-time'):
        tm_cpn.butterfly(fnm, 5, real_time=True)


def test_butterfly_different_asset(mocker):
    """butterfly works with a different base asset like TSF."""
    df_250 = pd.DataFrame({'price3pmClose': [95.0]}, index=[_index[0]])
    df_300 = pd.DataFrame({'price3pmClose': [98.0]}, index=[_index[0]])
    df_350 = pd.DataFrame({'price3pmClose': [99.5]}, index=[_index[0]])

    def _get_data_side_effect(fields=None, name=None):
        if name == 'TSF 2.50':
            return df_250
        elif name == 'TSF 3.00':
            return df_300
        elif name == 'TSF 3.50':
            return df_350
        return pd.DataFrame()

    mock_ds_instance = MagicMock()
    mock_ds_instance.get_data.side_effect = _get_data_side_effect
    mocker.patch.object(tm_cpn, 'Dataset', return_value=mock_ds_instance)

    tsf = _mock_asset('TSF')
    result = tm_cpn.butterfly(tsf, 3)

    assert isinstance(result, pd.Series)
    assert len(result) == 1
    # 2*98.0 - 95.0 - 99.5 = 1.5
    assert result.iloc[0] == pytest.approx(1.5)


def test_butterfly_empty_data(mocker):
    """butterfly returns empty series when no data is available."""
    mock_ds_instance = MagicMock()
    mock_ds_instance.get_data.return_value = pd.DataFrame()
    mocker.patch.object(tm_cpn, 'Dataset', return_value=mock_ds_instance)

    fnm = _mock_asset('FNM')
    result = tm_cpn.butterfly(fnm, 6)

    assert isinstance(result, pd.Series)
    assert len(result) == 0


def test_cpn_swap_invalid_coupon():
    """cpn_swap raises MqValueError for coupon not in allowed values."""
    fnm = _mock_asset('FNM')
    with pytest.raises(MqValueError, match='Invalid coupon'):
        tm_cpn.cpn_swap(fnm, 0.5)
    with pytest.raises(MqValueError, match='Invalid coupon'):
        tm_cpn.cpn_swap(fnm, 10.5)
    with pytest.raises(MqValueError, match='Invalid coupon'):
        tm_cpn.cpn_swap(fnm, 3.3)


def test_butterfly_invalid_coupon():
    """butterfly raises MqValueError for coupon not in allowed values."""
    fnm = _mock_asset('FNM')
    with pytest.raises(MqValueError, match='Invalid coupon'):
        tm_cpn.butterfly(fnm, 0.5)
    with pytest.raises(MqValueError, match='Invalid coupon'):
        tm_cpn.butterfly(fnm, 11.0)
    with pytest.raises(MqValueError, match='Invalid coupon'):
        tm_cpn.butterfly(fnm, 4.7)


def test_bbid_to_actual_asset_fnm(mocker):
    """_bbid_to_actual_asset returns correct Marquee ID for FNM."""
    mock_asset = Mock()
    mock_asset.get_identifier.return_value = 'FNM'
    mocker.patch.object(tm_cpn, '_asset_from_spec', return_value=mock_asset)

    result = tm_cpn._bbid_to_actual_asset(mock_asset)
    assert result == 'MA4R2VVY7F1MZ44R'


def test_bbid_to_actual_asset_fdw(mocker):
    """_bbid_to_actual_asset returns correct Marquee ID for FDW."""
    mock_asset = Mock()
    mock_asset.get_identifier.return_value = 'FDW'
    mocker.patch.object(tm_cpn, '_asset_from_spec', return_value=mock_asset)

    result = tm_cpn._bbid_to_actual_asset(mock_asset)
    assert result == 'MAHV2RXBZA55YXVD'


def test_bbid_to_actual_asset_tsf(mocker):
    """_bbid_to_actual_asset returns correct Marquee ID for TSF."""
    mock_asset = Mock()
    mock_asset.get_identifier.return_value = 'TSF'
    mocker.patch.object(tm_cpn, '_asset_from_spec', return_value=mock_asset)

    result = tm_cpn._bbid_to_actual_asset(mock_asset)
    assert result == 'MAMSQK44XNC6Z2D0'


def test_bbid_to_actual_asset_unknown(mocker):
    """_bbid_to_actual_asset falls back to get_marquee_id for unknown BBID."""
    mock_asset = Mock()
    mock_asset.get_identifier.return_value = 'UNKNOWN'
    mock_asset.get_marquee_id.return_value = 'MA_FALLBACK'
    mocker.patch.object(tm_cpn, '_asset_from_spec', return_value=mock_asset)

    result = tm_cpn._bbid_to_actual_asset(mock_asset)
    assert result == 'MA_FALLBACK'


def test_resolve_tba_asset_name_valid():
    """_resolve_tba_asset_name returns correct value for valid inputs."""
    assert tm_cpn._resolve_tba_asset_name('FNM', 5.0) == 'FNM 5.00'
    assert tm_cpn._resolve_tba_asset_name('FDW', 3.5) == 'FDW 3.50'
    assert tm_cpn._resolve_tba_asset_name('TSF', 7.0) == 'TSF 7.00'


def test_resolve_tba_asset_name_invalid():
    """_resolve_tba_asset_name raises MqValueError for invalid combo."""
    with pytest.raises(MqValueError, match='Invalid TBA asset'):
        tm_cpn._resolve_tba_asset_name('FNM', 0.5)
    with pytest.raises(MqValueError, match='Invalid TBA asset'):
        tm_cpn._resolve_tba_asset_name('XYZ', 5.0)


def test_get_tba_prices_non_empty(mocker):
    """_get_tba_prices returns a Series when data exists."""
    df = pd.DataFrame({'price3pmClose': [100.0, 101.0]}, index=_index)
    mock_ds_instance = MagicMock()
    mock_ds_instance.get_data.return_value = df
    mocker.patch.object(tm_cpn, 'Dataset', return_value=mock_ds_instance)

    result = tm_cpn._get_tba_prices('FNM 5.00')
    assert len(result) == 2
    assert result.iloc[0] == pytest.approx(100.0)


def test_get_tba_prices_empty(mocker):
    """_get_tba_prices returns empty ExtendedSeries when no data."""
    mock_ds_instance = MagicMock()
    mock_ds_instance.get_data.return_value = pd.DataFrame()
    mocker.patch.object(tm_cpn, 'Dataset', return_value=mock_ds_instance)

    result = tm_cpn._get_tba_prices('FNM 5.00')
    assert len(result) == 0
