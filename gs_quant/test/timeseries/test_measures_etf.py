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
    assert (
        tm._classification_children({'etfAssetClass': 'Fixed Income', 'etfCategory': 'Not Real'}, 'etfNicheFocus')
        is None
    )
    # Unknown niche-focus -> None
    assert (
        tm._classification_children(
            {
                'etfAssetClass': 'Fixed Income',
                'etfCategory': 'Government, Treasury',
                'etfNicheFocus': 'Not Real',
            },
            'etfFocus',
        )
        is None
    )


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


# ---------------------------------------------------------------------------
# total_return
# ---------------------------------------------------------------------------


class _MockAsset:
    def __init__(self, gsid='GSID123', close=None):
        self._gsid = gsid
        self._close = _close_series() if close is None else close

    def get_marquee_id(self):
        return 'MQID123'

    def get_identifier(self, _id_type):
        return self._gsid

    def get_data_series(self, *_args, **_kwargs):
        return self._close


def _close_series():
    idx = pd.DatetimeIndex(['2024-01-01', '2024-01-02', '2024-01-03'], name='date')
    return pd.Series([100.0, 110.0, 120.0], index=idx)


def _cash_dividend_actions():
    # One cash dividend with ex-date (effectiveDate) inside the window
    return [
        {
            'eventType': 'Cash Dividend',
            'effectiveDate': '2024-01-02',
            'records': [
                {'instrument_type': 'Currency', 'dataValue': 2.0},
            ],
        },
        # A non-dividend event that must be ignored
        {
            'eventType': 'Split',
            'effectiveDate': '2024-01-02',
            'records': [],
        },
    ]


def test_total_return_real_time_not_supported():
    with pytest.raises(NotImplementedError):
        tm.total_return(_MockAsset(), real_time=True)


def test_total_return_total_price_dividend():
    replace = Replacer()
    ca_mock = replace('gs_quant.timeseries.measures_etf.GsSecurityMasterApi.get_corporate_actions', Mock())
    ca_mock.return_value = _cash_dividend_actions()

    asset = _MockAsset()
    with DataContext(dt.date(2024, 1, 1), dt.date(2024, 1, 3)):
        total = tm.total_return(asset)
        price = tm.total_return(asset, tm.TotalReturnComponent.PRICE)
        dividend = tm.total_return(asset, tm.TotalReturnComponent.DIVIDEND)

    # start price = 100; dividend of 2.0 applies from ex-date 2024-01-02 onward
    # price %   : (100-100)/100, (110-100)/100, (120-100)/100  -> 0, 10, 20
    assert list(price.round(6).values) == [0.0, 10.0, 20.0]
    # dividend %: 0, 2/100, 2/100 -> 0, 2, 2
    assert list(dividend.round(6).values) == [0.0, 2.0, 2.0]
    # total %   : price + dividend -> 0, 12, 22
    assert list(total.round(6).values) == [0.0, 12.0, 22.0]
    replace.restore()


def test_total_return_no_dividends():
    replace = Replacer()
    ca_mock = replace('gs_quant.timeseries.measures_etf.GsSecurityMasterApi.get_corporate_actions', Mock())
    ca_mock.return_value = []

    with DataContext(dt.date(2024, 1, 1), dt.date(2024, 1, 3)):
        total = tm.total_return(_MockAsset())

    # No dividends -> total return equals price-only return
    assert list(total.round(6).values) == [0.0, 10.0, 20.0]
    replace.restore()


def test_total_return_no_price_raises():
    with pytest.raises(MqValueError):
        with DataContext(dt.date(2024, 1, 1), dt.date(2024, 1, 3)):
            tm.total_return(_MockAsset(close=pd.Series(dtype=float)))


def test_cash_dividends_lookup_failure_degrades_empty():
    replace = Replacer()
    # Corporate-actions lookup failing should degrade to an empty dividend series
    ca_mock = replace('gs_quant.timeseries.measures_etf.GsSecurityMasterApi.get_corporate_actions', Mock())
    ca_mock.side_effect = Exception('boom')

    result = tm._cash_dividends_per_share(_MockAsset(), dt.date(2024, 1, 1), dt.date(2024, 1, 3))
    assert result.empty
    replace.restore()


def test_cash_dividends_no_gsid_returns_empty():
    # Asset with no GSID identifier -> empty dividend series
    result = tm._cash_dividends_per_share(_MockAsset(gsid=None), dt.date(2024, 1, 1), dt.date(2024, 1, 3))
    assert result.empty


def test_cash_dividends_missing_effective_date_skipped():
    replace = Replacer()
    ca_mock = replace('gs_quant.timeseries.measures_etf.GsSecurityMasterApi.get_corporate_actions', Mock())
    ca_mock.return_value = [
        {
            'eventType': 'Cash Dividend',
            # no effectiveDate -> must be skipped
            'records': [{'instrument_type': 'Currency', 'dataValue': 5.0}],
        },
    ]

    result = tm._cash_dividends_per_share(_MockAsset(), dt.date(2024, 1, 1), dt.date(2024, 1, 3))
    assert result.empty
    replace.restore()


def test_total_return_zero_start_price_raises():
    replace = Replacer()
    ca_mock = replace('gs_quant.timeseries.measures_etf.GsSecurityMasterApi.get_corporate_actions', Mock())
    ca_mock.return_value = []

    idx = pd.DatetimeIndex(['2024-01-01', '2024-01-02', '2024-01-03'], name='date')
    zero_start = pd.Series([0.0, 110.0, 120.0], index=idx)
    with pytest.raises(MqValueError):
        with DataContext(dt.date(2024, 1, 1), dt.date(2024, 1, 3)):
            tm.total_return(_MockAsset(close=zero_start))
    replace.restore()


def test_cash_dividends_out_of_window_excluded():
    replace = Replacer()
    ca_mock = replace('gs_quant.timeseries.measures_etf.GsSecurityMasterApi.get_corporate_actions', Mock())
    ca_mock.return_value = [
        {
            'eventType': 'Cash Dividend',
            'effectiveDate': '2023-12-01',  # before the window
            'records': [{'instrument_type': 'Currency', 'dataValue': 5.0}],
        },
    ]

    result = tm._cash_dividends_per_share(_MockAsset(), dt.date(2024, 1, 1), dt.date(2024, 1, 3))
    assert result.empty
    replace.restore()


# ---------------------------------------------------------------------------
# gross / net leverage exposure
# ---------------------------------------------------------------------------


class _StatusError(Exception):
    def __init__(self, status):
        super().__init__(f'status {status}')
        self.status = status


def _reference_frame():
    idx = pd.DatetimeIndex(['2024-01-02'] * 3, name='date')
    return pd.DataFrame(
        {
            'isin': ['LONG2X', 'SHORT3X', 'PLAIN'],
            'isoCountry': ['US', 'US', 'US'],
            'leverageFactor': [2.0, -3.0, None],
        },
        index=idx,
    )


def _timeseries_frame():
    idx = pd.DatetimeIndex(['2024-01-01', '2024-01-01', '2024-01-02', '2024-01-02'], name='date')
    return pd.DataFrame(
        {
            'isin': ['LONG2X', 'SHORT3X', 'LONG2X', 'SHORT3X'],
            'nav': [10.0, 5.0, 11.0, 4.0],
            'sharesOutstanding': [100.0, 200.0, 100.0, 200.0],
        },
        index=idx,
    )


def _mock_leverage_api(monkeypatch, ts_frame=None, ref_frame=None, coverage=None):
    """Patch the async data API used by the leverage measures."""
    ts_frame = _timeseries_frame() if ts_frame is None else ts_frame
    ref_frame = _reference_frame() if ref_frame is None else ref_frame
    coverage = [{'isin': 'LONG2X'}, {'isin': 'SHORT3X'}, {'isin': 'PLAIN'}] if coverage is None else coverage
    calls = []

    async def get_coverage_async(dataset_id, **kwargs):
        return coverage

    async def get_data_async(self, start=None, end=None, **kwargs):
        calls.append((self.id, kwargs.get('isin')))
        if self.id == tm.ETF_REFERENCE_DATASET_ID:
            return ref_frame
        if ts_frame.empty:
            return ts_frame
        return ts_frame[ts_frame['isin'].isin(kwargs['isin'])]

    monkeypatch.setattr(tm.GsDataApi, 'get_coverage_async', get_coverage_async)
    monkeypatch.setattr(tm.Dataset, 'get_data_async', get_data_async)
    return calls


def test_gross_leverage_exposure(monkeypatch):
    _mock_leverage_api(monkeypatch)
    with DataContext(dt.date(2024, 1, 1), dt.date(2024, 1, 2)):
        actual = tm.gross_leverage_exposure('US')
    # day1: 10*100*2 + 5*200*3 = 2000 + 3000 ; day2: 11*100*2 + 4*200*3 = 2200 + 2400
    assert list(actual.values) == [5000.0, 4600.0]
    assert actual.dataset_ids == (tm.ETF_REFERENCE_DATASET_ID, tm.ETF_TIME_SERIES_DATASET_ID)


def test_net_leverage_exposure(monkeypatch):
    calls = _mock_leverage_api(monkeypatch)
    with DataContext(dt.date(2024, 1, 1), dt.date(2024, 1, 2)):
        actual = tm.net_leverage_exposure('US')
    # day1: 2000 - 3000 ; day2: 2200 - 2400
    assert list(actual.values) == [-1000.0, -200.0]
    # only the leveraged ETFs are requested from the time series dataset
    ts_isins = [isins for ds_id, isins in calls if ds_id == tm.ETF_TIME_SERIES_DATASET_ID]
    assert ts_isins == [['LONG2X', 'SHORT3X']]


def test_leverage_exposure_real_time_not_supported():
    for fn in (tm.gross_leverage_exposure, tm.net_leverage_exposure):
        with pytest.raises(NotImplementedError):
            fn('US', real_time=True)


def test_leverage_exposure_no_leveraged_etfs_raises(monkeypatch):
    _mock_leverage_api(monkeypatch, ref_frame=pd.DataFrame())
    with pytest.raises(MqValueError):
        with DataContext(dt.date(2024, 1, 1), dt.date(2024, 1, 2)):
            tm.gross_leverage_exposure('US')


def test_leverage_exposure_no_timeseries_raises(monkeypatch):
    _mock_leverage_api(monkeypatch, ts_frame=pd.DataFrame())
    with pytest.raises(MqValueError):
        with DataContext(dt.date(2024, 1, 1), dt.date(2024, 1, 2)):
            tm.net_leverage_exposure('US')


def test_leverage_exposure_all_nan_timeseries_raises(monkeypatch):
    nan_frame = _timeseries_frame()
    nan_frame['nav'] = float('nan')
    _mock_leverage_api(monkeypatch, ts_frame=nan_frame)
    with pytest.raises(MqValueError):
        with DataContext(dt.date(2024, 1, 1), dt.date(2024, 1, 2)):
            tm.gross_leverage_exposure('US')


def test_leveraged_etfs_filters_country_and_empty_factors(monkeypatch):
    ref = _reference_frame()
    ref.loc[ref['isin'] == 'SHORT3X', 'isoCountry'] = 'GB'
    _mock_leverage_api(monkeypatch, ref_frame=ref)
    assert tm._run(tm._leveraged_etfs_async('US')).to_dict() == {'LONG2X': 2.0}


def test_leveraged_etfs_without_leverage_column_is_empty(monkeypatch):
    _mock_leverage_api(monkeypatch, ref_frame=_reference_frame().drop(columns=['leverageFactor', 'isoCountry']))
    assert tm._run(tm._leveraged_etfs_async('US')).empty


def test_leveraged_etfs_empty_coverage_raises(monkeypatch):
    _mock_leverage_api(monkeypatch, coverage=[{'isin': None}])
    with pytest.raises(MqValueError):
        tm._run(tm._leveraged_etfs_async('US'))


def test_leveraged_etfs_coverage_error_raises(monkeypatch):
    async def boom(dataset_id, **kwargs):
        raise Exception('boom')

    monkeypatch.setattr(tm.GsDataApi, 'get_coverage_async', boom)
    with pytest.raises(MqValueError):
        tm._run(tm._leveraged_etfs_async('US'))


def test_leveraged_etfs_reference_query_error_raises(monkeypatch):
    _mock_leverage_api(monkeypatch)

    async def boom(self, **kwargs):
        raise _StatusError(400)

    monkeypatch.setattr(tm.Dataset, 'get_data_async', boom)
    with pytest.raises(MqValueError):
        tm._run(tm._leveraged_etfs_async('US'))


def test_date_windows_cover_range_without_gaps():
    windows = list(tm._date_windows(dt.date(2021, 1, 1), dt.date(2021, 12, 31), days=100))
    assert windows[0][0] == dt.date(2021, 1, 1)
    assert windows[-1][1] == dt.date(2021, 12, 31)
    for (_, prev_end), (next_start, _) in zip(windows, windows[1:]):
        assert next_start == prev_end + dt.timedelta(days=1)


class _FakeDataset:
    """Async dataset returning one row per (isin, day); ``fail`` decides which queries raise."""

    id = 'X'

    def __init__(self, fail=lambda start, end, isins: None):
        self.fail = fail
        self.calls = []

    async def get_data_async(self, start, end, isin):
        self.calls.append((start, end, tuple(isin)))
        error = self.fail(start, end, isin)
        if error is not None:
            raise error
        days = pd.date_range(start, end, name='date')
        return pd.DataFrame(
            {'isin': [i for _ in days for i in isin], 'nav': 1.0, 'sharesOutstanding': 1.0},
            index=pd.DatetimeIndex([d for d in days for _ in isin], name='date'),
        )


def _fetch(ds, isins, start, end):
    return tm._run(tm._fetch_capped(ds, isins, start, end, tm.asyncio.Semaphore(4)))


def test_fetch_capped_splits_when_row_cap_hit(monkeypatch):
    monkeypatch.setattr(tm, '_QUERY_ROW_CAP', 5)
    ds = _FakeDataset()
    frames = _fetch(ds, ['A', 'B', 'C'], dt.date(2024, 1, 1), dt.date(2024, 1, 4))
    df = pd.concat(frames)
    # 4 days x 3 isins = 12 rows, every (isin, day) returned exactly once after splitting
    assert len(df) == 12
    assert not pd.MultiIndex.from_arrays([df.index, df['isin']]).duplicated().any()
    assert all(len(f) < 5 or (f.index.nunique() == 1 and f['isin'].nunique() == 1) for f in frames)


def test_fetch_capped_single_cell_at_cap_is_returned(monkeypatch):
    monkeypatch.setattr(tm, '_QUERY_ROW_CAP', 1)
    frames = _fetch(_FakeDataset(), ['A'], dt.date(2024, 1, 1), dt.date(2024, 1, 1))
    assert len(frames) == 1 and len(frames[0]) == 1


def test_fetch_capped_empty_result():
    class _Empty(_FakeDataset):
        async def get_data_async(self, start, end, isin):
            return pd.DataFrame()

    assert _fetch(_Empty(), ['A'], dt.date(2024, 1, 1), dt.date(2024, 1, 2)) == []


def test_fetch_capped_isolates_bad_isin_day():
    """One bad (ISIN, day) record must not fail the query or cost the other ETFs' data."""
    bad_isin, bad_day = 'I3', dt.date(2024, 1, 5)

    def fail(start, end, isins):
        return _StatusError(500) if bad_isin in isins and start <= bad_day <= end else None

    ds = _FakeDataset(fail)
    df = pd.concat(_fetch(ds, [f'I{i}' for i in range(8)], dt.date(2024, 1, 1), dt.date(2024, 1, 8)))
    assert len(df) == 8 * 8 - 1
    assert not ((df['isin'] == bad_isin) & (df.index == pd.Timestamp(bad_day))).any()
    assert len(ds.calls) < 25  # isolated in a logarithmic number of calls


def test_fetch_capped_non_server_error_raises():
    ds = _FakeDataset(lambda start, end, isins: _StatusError(400))
    with pytest.raises(_StatusError):
        _fetch(ds, ['A', 'B'], dt.date(2024, 1, 1), dt.date(2024, 1, 2))


def test_fetch_time_series_spans_windows_back_to_2021():
    ds = _FakeDataset()
    tm._run(tm._fetch_time_series_async(ds, ['A'], dt.date(2021, 1, 1), dt.date(2021, 12, 31)))
    assert len(ds.calls) > 1
    assert min(c[0] for c in ds.calls) == dt.date(2021, 1, 1)
    assert max(c[1] for c in ds.calls) == dt.date(2021, 12, 31)


def test_fetch_time_series_error_raises_mq_value_error():
    ds = _FakeDataset(lambda start, end, isins: _StatusError(400))
    with pytest.raises(MqValueError):
        tm._run(tm._fetch_time_series_async(ds, ['A'], dt.date(2024, 1, 1), dt.date(2024, 1, 2)))


def test_is_server_error():
    assert tm._is_server_error(_StatusError(503))
    assert not tm._is_server_error(_StatusError(404))
    assert not tm._is_server_error(Exception('no status'))


if __name__ == '__main__':
    pytest.main(args=[__file__])
