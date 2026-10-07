"""
Copyright 2024 Goldman Sachs.
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
from testfixtures import Replacer
from testfixtures.mock import Mock

import gs_quant.timeseries.measures_etf as tm
from gs_quant.data import DataContext
from gs_quant.errors import MqValueError


class _MockCountry:
    def __init__(self, alpha2):
        self._alpha2 = alpha2

    def get_alpha2(self):
        return self._alpha2


def _mock_frame():
    idx = pd.DatetimeIndex(['2024-01-01', '2024-01-01', '2024-01-02', '2024-01-02'], name='date')
    return pd.DataFrame(
        {
            'etfAssetClass': ['Fixed Income', 'Equity', 'Fixed Income', 'Equity'],
            'etfCategory': ['Government, Treasury', 'Sector', 'Government, Treasury', 'Sector'],
            'etfNicheFocus': ['Short-Term', 'Banks', 'Short-Term', 'Banks'],
            'etfFocus': ['Investment Grade', 'Financials', 'Investment Grade', 'Financials'],
            'totalFlow': [100.0, 200.0, 300.0, 400.0],
            'etfTotalAssets': [10.0, 20.0, 30.0, 40.0],
        },
        index=idx,
    )


def test_etf_flow_real_time_not_supported():
    with pytest.raises(NotImplementedError):
        tm.etf_flow('US', real_time=True)


def test_etf_flow_all_aggregates():
    replace = Replacer()
    mock = replace('gs_quant.timeseries.measures_etf.Dataset.get_data', Mock())
    mock.return_value = _mock_frame()

    with DataContext(dt.date(2024, 1, 1), dt.date(2024, 1, 2)):
        actual = tm.etf_flow('US')  # All asset classes -> sum per date

    # 2024-01-01: 100 + 200 = 300 ; 2024-01-02: 300 + 400 = 700
    assert list(actual.values) == [300.0, 700.0]
    assert actual.dataset_ids == (tm.ETF_FLOWS_DATASET_ID,)
    replace.restore()


def test_etf_flow_client_side_comma_filter():
    replace = Replacer()
    mock = replace('gs_quant.timeseries.measures_etf.Dataset.get_data', Mock())
    mock.return_value = _mock_frame()

    with DataContext(dt.date(2024, 1, 1), dt.date(2024, 1, 2)):
        actual = tm.etf_flow('US', tm.ETFAssetClass.FIXED_INCOME, tm.ETFCategory.GOVERNMENT_TREASURY)

    # Comma category filtered client-side -> only the two Fixed Income rows remain
    assert list(actual.values) == [100.0, 300.0]
    # Only the server-filterable value (Fixed Income) should be sent to the backend
    _, kwargs = mock.call_args
    assert kwargs.get('etfAssetClass') == 'Fixed Income'
    assert 'etfCategory' not in kwargs
    replace.restore()


def test_etf_flow_metric_selection():
    replace = Replacer()
    mock = replace('gs_quant.timeseries.measures_etf.Dataset.get_data', Mock())
    mock.return_value = _mock_frame()

    with DataContext(dt.date(2024, 1, 1), dt.date(2024, 1, 2)):
        actual = tm.etf_flow('US', metric=tm.ETFFlowMetric.TOTAL_ASSETS)

    assert list(actual.values) == [30.0, 70.0]
    replace.restore()


def test_etf_flow_no_data_raises():
    replace = Replacer()
    mock = replace('gs_quant.timeseries.measures_etf.Dataset.get_data', Mock())
    mock.return_value = pd.DataFrame()

    with pytest.raises(MqValueError):
        with DataContext(dt.date(2024, 1, 1), dt.date(2024, 1, 2)):
            tm.etf_flow('US')
    replace.restore()


def test_etf_flow_coverage_next_level():
    replace = Replacer()
    mock = replace('gs_quant.timeseries.measures_etf.Dataset.get_data', Mock())
    mock.return_value = _mock_frame()

    with DataContext(dt.date(2024, 1, 1), dt.date(2024, 1, 2)):
        # Next level after asset class -> categories under Fixed Income
        cats = tm.etf_flow_coverage('US', tm.ETFAssetClass.FIXED_INCOME)

    assert cats[0] == tm.ETF_FLOW_ALL
    assert 'Government, Treasury' in cats
    replace.restore()


def test_etf_flow_coverage_fully_selected_returns_empty():
    with DataContext(dt.date(2024, 1, 1), dt.date(2024, 1, 2)):
        result = tm.etf_flow_coverage(
            'US',
            tm.ETFAssetClass.FIXED_INCOME,
            tm.ETFCategory.GOVERNMENT_TREASURY,
            'Short-Term',
            'Investment Grade',
        )
    assert result == []


def test_resolve_country_code_none_raises():
    with pytest.raises(MqValueError):
        tm._resolve_country_code(None)


def test_resolve_country_code_from_entity():
    replace = Replacer()
    mock = replace('gs_quant.timeseries.measures_etf.Country', Mock())
    mock.return_value = _MockCountry('gb')
    assert tm._resolve_country_code('SomeCountryName') == 'GB'
    replace.restore()


def test_resolve_country_code_unresolved_raises():
    replace = Replacer()
    mock = replace('gs_quant.timeseries.measures_etf.Country', Mock())
    mock.return_value = _MockCountry(None)
    with pytest.raises(MqValueError):
        tm._resolve_country_code('SomeCountryName')
    replace.restore()


def test_resolve_country_code_lookup_exception_raises():
    replace = Replacer()
    mock = replace('gs_quant.timeseries.measures_etf.Country', Mock())
    mock.side_effect = Exception('lookup failed')
    with pytest.raises(MqValueError):
        tm._resolve_country_code('SomeCountryName')
    replace.restore()


def test_etf_flow_invalid_asset_class_raises():
    with pytest.raises(MqValueError):
        with DataContext(dt.date(2024, 1, 1), dt.date(2024, 1, 2)):
            tm.etf_flow('US', asset_class='not-an-enum')


def test_etf_flow_invalid_category_raises():
    with pytest.raises(MqValueError):
        with DataContext(dt.date(2024, 1, 1), dt.date(2024, 1, 2)):
            tm.etf_flow('US', category='not-an-enum')


def test_etf_flow_invalid_metric_raises():
    with pytest.raises(MqValueError):
        with DataContext(dt.date(2024, 1, 1), dt.date(2024, 1, 2)):
            tm.etf_flow('US', metric='not-an-enum')


def test_etf_flow_query_error_raises():
    replace = Replacer()
    mock = replace('gs_quant.timeseries.measures_etf.Dataset.get_data', Mock())
    mock.side_effect = Exception('boom')
    with pytest.raises(MqValueError):
        with DataContext(dt.date(2024, 1, 1), dt.date(2024, 1, 2)):
            tm.etf_flow('US')
    replace.restore()


def test_etf_flow_coverage_query_error_raises():
    replace = Replacer()
    mock = replace('gs_quant.timeseries.measures_etf.Dataset.get_data', Mock())
    mock.side_effect = Exception('boom')
    with pytest.raises(MqValueError):
        with DataContext(dt.date(2024, 1, 1), dt.date(2024, 1, 2)):
            tm.etf_flow_coverage('US')
    replace.restore()


def test_etf_flow_coverage_empty_returns_all():
    replace = Replacer()
    mock = replace('gs_quant.timeseries.measures_etf.Dataset.get_data', Mock())
    mock.return_value = pd.DataFrame()
    with DataContext(dt.date(2024, 1, 1), dt.date(2024, 1, 2)):
        result = tm.etf_flow_coverage('US')
    assert result == [tm.ETF_FLOW_ALL]
    replace.restore()


if __name__ == '__main__':
    pytest.main(args=[__file__])
