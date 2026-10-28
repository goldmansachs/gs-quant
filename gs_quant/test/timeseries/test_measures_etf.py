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
        tm.total_etf_flow('US', real_time=True)


def test_etf_flow_all_aggregates():
    replace = Replacer()
    mock = replace('gs_quant.timeseries.measures_etf.Dataset.get_data', Mock())
    mock.return_value = _mock_frame()

    with DataContext(dt.date(2024, 1, 1), dt.date(2024, 1, 2)):
        actual = tm.total_etf_flow('US')  # All asset classes -> sum per date

    # 2024-01-01: 100 + 200 = 300 ; 2024-01-02: 300 + 400 = 700
    assert list(actual.values) == [300.0, 700.0]
    assert actual.dataset_ids == (tm.ETF_FLOWS_DATASET_ID,)
    replace.restore()


def test_etf_flow_client_side_comma_filter():
    replace = Replacer()
    mock = replace('gs_quant.timeseries.measures_etf.Dataset.get_data', Mock())
    mock.return_value = _mock_frame()

    with DataContext(dt.date(2024, 1, 1), dt.date(2024, 1, 2)):
        # Parser-safe labels (case-insensitive) resolve to the real dataset values
        actual = tm.total_etf_flow('US', 'fixed income', 'Government Treasury')

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
        actual = tm.total_etf_assets('US')

    assert list(actual.values) == [30.0, 70.0]
    replace.restore()


def test_etf_flow_no_data_raises():
    replace = Replacer()
    mock = replace('gs_quant.timeseries.measures_etf.Dataset.get_data', Mock())
    mock.return_value = pd.DataFrame()

    with pytest.raises(MqValueError):
        with DataContext(dt.date(2024, 1, 1), dt.date(2024, 1, 2)):
            tm.total_etf_flow('US')
    replace.restore()


def test_etf_flow_coverage_next_level():
    with DataContext(dt.date(2024, 1, 1), dt.date(2024, 1, 2)):
        # Next level after asset class -> categories under Fixed Income (from the
        # static classification tree, returned as parser-safe labels)
        cats = tm.etf_flow_coverage('US', 'Fixed Income')

    assert cats[0] == tm.ETF_FLOW_ALL
    assert 'Government Treasury' in cats


def test_etf_flow_coverage_fully_selected_returns_empty():
    with DataContext(dt.date(2024, 1, 1), dt.date(2024, 1, 2)):
        result = tm.etf_flow_coverage(
            'US',
            'Fixed Income',
            'Government Treasury',
            'Investment Grade',
            'Short Term',
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


def test_etf_flow_query_error_raises():
    replace = Replacer()
    mock = replace('gs_quant.timeseries.measures_etf.Dataset.get_data', Mock())
    mock.side_effect = Exception('boom')
    with pytest.raises(MqValueError):
        with DataContext(dt.date(2024, 1, 1), dt.date(2024, 1, 2)):
            tm.total_etf_flow('US')
    replace.restore()


def test_etf_flow_coverage_query_error_raises():
    # A branch NOT present in the static classification tree falls through to the
    # dataset query, so a backend error surfaces as MqValueError.
    replace = Replacer()
    mock = replace('gs_quant.timeseries.measures_etf.Dataset.get_data', Mock())
    mock.side_effect = Exception('boom')
    with pytest.raises(MqValueError):
        with DataContext(dt.date(2024, 1, 1), dt.date(2024, 1, 2)):
            tm.etf_flow_coverage('US', 'Not A Real Asset Class')
    replace.restore()


def test_etf_flow_coverage_top_level_from_tree():
    # The top level (asset classes) is served from the static classification tree
    # and never queries the dataset.
    with DataContext(dt.date(2024, 1, 1), dt.date(2024, 1, 2)):
        result = tm.etf_flow_coverage('US')
    assert result[0] == tm.ETF_FLOW_ALL
    assert 'Fixed Income' in result
    assert 'Equity' in result


def test_dataset_value_case_insensitive_and_parser_safe():
    # Parser-safe labels (commas/dashes stripped) resolve back to real values
    assert tm._dataset_value('Government Treasury') == 'Government, Treasury'
    assert tm._dataset_value('Long BTC Short USD') == 'Long BTC, Short USD'
    # Case-insensitive resolution
    assert tm._dataset_value('fixed income') == 'Fixed Income'
    # 'All' passes through (any case)
    assert tm._dataset_value('all') == tm.ETF_FLOW_ALL


def test_parser_safe_label_passthrough():
    # None and the 'All' sentinel are returned unchanged
    assert tm._parser_safe_label(None) is None
    assert tm._parser_safe_label(tm.ETF_FLOW_ALL) == tm.ETF_FLOW_ALL


def test_dataset_value_none_passthrough():
    assert tm._dataset_value(None) is None
    # An unknown label is returned unchanged
    assert tm._dataset_value('Totally Unknown Thing') == 'Totally Unknown Thing'


def test_classification_children_deeper_levels():
    # Niche-focus level under a known asset class / category
    focuses = tm._classification_children(
        {'etfAssetClass': 'Fixed Income', 'etfCategory': 'Government, Treasury'},
        'etfNicheFocus',
    )
    assert 'Investment Grade' in focuses

    # Focus level under a known asset class / category / niche-focus
    niches = tm._classification_children(
        {
            'etfAssetClass': 'Fixed Income',
            'etfCategory': 'Government, Treasury',
            'etfNicheFocus': 'Investment Grade',
        },
        'etfFocus',
    )
    assert 'Short-Term' in niches

    # Unknown category -> None (branch not in the tree)
    assert tm._classification_children(
        {'etfAssetClass': 'Fixed Income', 'etfCategory': 'Not Real'}, 'etfNicheFocus'
    ) is None
    # Unknown niche-focus -> None
    assert tm._classification_children(
        {
            'etfAssetClass': 'Fixed Income',
            'etfCategory': 'Government, Treasury',
            'etfNicheFocus': 'Not Real',
        },
        'etfFocus',
    ) is None


def test_etf_flow_coverage_dataset_fallback():
    # An asset class not in the static tree falls through to the dataset query;
    # the next level (categories) is derived from the returned data.
    replace = Replacer()
    mock = replace('gs_quant.timeseries.measures_etf.Dataset.get_data', Mock())
    mock.return_value = _mock_frame()

    with DataContext(dt.date(2024, 1, 1), dt.date(2024, 1, 2)):
        result = tm.etf_flow_coverage('US', 'Made Up Class')

    assert result[0] == tm.ETF_FLOW_ALL
    # Values come back parser-safe (e.g. 'Government, Treasury' -> 'Government Treasury')
    assert 'Government Treasury' in result
    replace.restore()


def test_etf_flow_coverage_dataset_fallback_empty():
    # Fallback with no data returns just the aggregate option
    replace = Replacer()
    mock = replace('gs_quant.timeseries.measures_etf.Dataset.get_data', Mock())
    mock.return_value = pd.DataFrame()

    with DataContext(dt.date(2024, 1, 1), dt.date(2024, 1, 2)):
        result = tm.etf_flow_coverage('US', 'Made Up Class')

    assert result == [tm.ETF_FLOW_ALL]
    replace.restore()


def _metric_frame():
    idx = pd.DatetimeIndex(['2024-01-01', '2024-01-01', '2024-01-02', '2024-01-02'], name='date')
    return pd.DataFrame(
        {
            'etfAssetClass': ['Fixed Income', 'Equity', 'Fixed Income', 'Equity'],
            'etfTotalSharesOutstanding': [1.0, 2.0, 3.0, 4.0],
            'etfTotalFunds': [5.0, 6.0, 7.0, 8.0],
        },
        index=idx,
    )


def test_total_etf_shares_outstanding():
    replace = Replacer()
    mock = replace('gs_quant.timeseries.measures_etf.Dataset.get_data', Mock())
    mock.return_value = _metric_frame()
    with DataContext(dt.date(2024, 1, 1), dt.date(2024, 1, 2)):
        actual = tm.total_etf_shares_outstanding('US')
    assert list(actual.values) == [3.0, 7.0]
    replace.restore()


def test_total_etf_funds():
    replace = Replacer()
    mock = replace('gs_quant.timeseries.measures_etf.Dataset.get_data', Mock())
    mock.return_value = _metric_frame()
    with DataContext(dt.date(2024, 1, 1), dt.date(2024, 1, 2)):
        actual = tm.total_etf_funds('US')
    assert list(actual.values) == [11.0, 15.0]
    replace.restore()


def test_metric_functions_real_time_not_supported():
    for fn in (
        tm.total_etf_shares_outstanding,
        tm.total_etf_assets,
        tm.total_etf_funds,
    ):
        with pytest.raises(NotImplementedError):
            fn('US', real_time=True)


if __name__ == '__main__':
    pytest.main(args=[__file__])
