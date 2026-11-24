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

import asyncio
import logging
import re
from enum import Enum
from typing import Optional

import pandas as pd

from gs_quant.api.gs.data import GsDataApi, QueryType
from gs_quant.api.gs.secmaster import GsSecurityMasterApi, SecMasterIdentifiers
from gs_quant.common import AssetClass, AssetType
from gs_quant.data import DataContext, DataFrequency, Dataset
from gs_quant.data.fields import DataMeasure
from gs_quant.entities.entity import Country, EntityType
from gs_quant.errors import MqValueError
from gs_quant.markets.securities import Asset, AssetIdentifier
from gs_quant.timeseries.etf_classification import ETF_CLASSIFICATION
from gs_quant.timeseries.helper import plot_measure, plot_measure_entity
from gs_quant.timeseries.measures import ExtendedSeries

# ---------------------------------------------------------------------------
# FactSet ETF flows (aggregated) - SF_FACTSET_ETF_FLOWS_AGG_YRBSW3R0
#
# The dataset is organised as a hierarchy below the country:
#
#     countryId -> etfAssetClass -> etfCategory -> etfNicheFocus -> etfFocus
#
# Each row also carries the metrics totalFlow, etfTotalSharesOutstanding,
# etfTotalAssets and etfTotalFunds.
# ---------------------------------------------------------------------------

ETF_FLOWS_DATASET_ID = 'SF_FACTSET_ETF_FLOWS_AGG_YRBSW3R0'

# Sentinel used at every hierarchy level. Selecting "All" at a level means
# "do not filter on this dimension - aggregate (sum) across every value below it".
ETF_FLOW_ALL = 'All'

# Hierarchy of the dataset, ordered from the broadest to the most granular level.
# countryId is resolved from the country entity, the remaining levels are user supplied.
_ETF_FLOW_HIERARCHY = ('etfAssetClass', 'etfCategory', 'etfNicheFocus', 'etfFocus')


# ---------------------------------------------------------------------------
# Static classification tree (FactSet Fund Exposure Sort).
#
# ETF_CLASSIFICATION is generated from the FactSet CSV and nested as:
#     Asset Class  -> Category    -> Focus         -> Niche
# which maps onto the dataset hierarchy levels used by this module as:
#     etfAssetClass -> etfCategory -> etfNicheFocus -> etfFocus
#
# This tree lets the cascading drop-down (etf_flow_coverage) return the valid
# children of a selection without having to query the dataset: pick an asset
# class and get its categories, pick a category and get its focuses, and so on.
# ---------------------------------------------------------------------------


def _parser_safe_label(value):
    """
    Convert a raw dataset value to a label the plot expression parser accepts.

    The parser only tolerates word characters and spaces, so commas, dashes,
    slashes and ampersands (e.g. 'Government, Treasury', 'Long-Term',
    'Local Authority/Municipal', 'Size & Style') are replaced with spaces and
    runs of whitespace are collapsed.
    """
    if value is None or value == ETF_FLOW_ALL:
        return value
    return re.sub(r'\s+', ' ', re.sub(r'[^\w ]+', ' ', str(value))).strip()


def _build_label_maps():
    """
    Build lookups from user-supplied labels to real dataset values.

    Returns two dicts: one keyed by the parser-safe label and one keyed by the
    lower-cased parser-safe label (so matching is also case-insensitive).
    """
    exact, lower = {}, {}

    def register(value):
        label = _parser_safe_label(value)
        exact.setdefault(label, value)
        lower.setdefault(label.lower(), value)
        # also allow the raw dataset value (and its lower-case form) to resolve
        exact.setdefault(value, value)
        lower.setdefault(str(value).lower(), value)

    for asset_class, categories in ETF_CLASSIFICATION.items():
        register(asset_class)
        for category, focuses in categories.items():
            register(category)
            for focus, niches in focuses.items():
                register(focus)
                for niche in niches:
                    register(niche)
    return exact, lower


# Parser-safe label -> true dataset value, derived from the classification tree.
_LABEL_TO_DATASET, _LABEL_TO_DATASET_LOWER = _build_label_maps()


def _dataset_value(value):
    """
    Translate a (possibly parser-safe / differently-cased) label to the real
    dataset value. 'All' (any case) and None pass through unchanged.
    """
    if value is None:
        return value
    if str(value).strip().lower() == ETF_FLOW_ALL.lower():
        return ETF_FLOW_ALL
    if value in _LABEL_TO_DATASET:
        return _LABEL_TO_DATASET[value]
    return _LABEL_TO_DATASET_LOWER.get(str(value).strip().lower(), value)


def _classification_children(chosen: dict, next_level: str):
    """
    Return the valid children of a selection from the static classification tree.

    ``chosen`` maps already-selected hierarchy dimensions to their real dataset
    values; ``next_level`` is the dimension we want the options for. Returns a
    list of raw (non-parser-safe) child values, or ``None`` if this branch of the
    hierarchy is not represented in the CSV classification (so the caller can
    fall back to querying the dataset).
    """
    # Levels in order, paired with the classification tree depth they index.
    asset_class = chosen.get('etfAssetClass')
    category = chosen.get('etfCategory')
    niche_focus = chosen.get('etfNicheFocus')

    if next_level == 'etfAssetClass':
        return list(ETF_CLASSIFICATION.keys())

    categories = ETF_CLASSIFICATION.get(asset_class)
    if categories is None:
        return None
    if next_level == 'etfCategory':
        return list(categories.keys())

    focuses = categories.get(category)
    if focuses is None:
        return None
    if next_level == 'etfNicheFocus':
        return list(focuses.keys())

    niches = focuses.get(niche_focus)
    if niches is None:
        return None
    if next_level == 'etfFocus':
        return list(niches)

    return None  # pragma: no cover


class ETFFlowMetric(Enum):
    TOTAL_FLOW = 'totalFlow'
    SHARES_OUTSTANDING = 'etfTotalSharesOutstanding'
    TOTAL_ASSETS = 'etfTotalAssets'
    TOTAL_FUNDS = 'etfTotalFunds'


def _resolve_country_code(country_id: str) -> str:
    """Resolve the ISO alpha-2 country code used by the ETF flows dataset."""
    if country_id is None:
        raise MqValueError('Could not resolve country for ETF flow measure')
    # Already a 2 letter ISO code (e.g. passed directly as 'US')
    if isinstance(country_id, str) and len(country_id) == 2 and country_id.isalpha():
        return country_id.upper()
    try:
        alpha2 = Country(country_id).get_alpha2()
    except Exception:
        alpha2 = None
    if not alpha2:
        raise MqValueError(f'Could not resolve ISO alpha-2 country code for {country_id}')
    return alpha2.upper()


def _enum_or_str_value(v):
    """Return the underlying dataset string value for an enum or pass a string through."""
    return v.value if isinstance(v, Enum) else v


# The dataset backend only accepts dimension filter values matching this pattern
# (word characters and spaces). Values containing e.g. commas - like
# 'Government, Treasury' or 'Long BTC, Short USD' - must be filtered client-side.
_SERVER_FILTER_PATTERN = re.compile(r'^[\w ]{1,256}$')


def _is_server_filterable(value: str) -> bool:
    return isinstance(value, str) and bool(_SERVER_FILTER_PATTERN.match(value))


def _split_filters(selections: dict) -> tuple:
    """
    Split non-"All" selections into server-side filters (safe values) and
    client-side filters (values the backend cannot filter, e.g. containing commas).
    """
    server, client = {}, {}
    for dim, value in selections.items():
        if value is None or str(value) == ETF_FLOW_ALL:
            continue
        if _is_server_filterable(value):
            server[dim] = value
        else:
            client[dim] = value
    return server, client


def _apply_client_filters(df: 'pd.DataFrame', client_filters: dict) -> 'pd.DataFrame':
    for dim, value in client_filters.items():
        if dim in df.columns:
            df = df[df[dim] == value]
    return df


def etf_flow_coverage(
    country_id: str,
    asset_class: str = ETF_FLOW_ALL,
    category: str = ETF_FLOW_ALL,
    niche_focus: str = ETF_FLOW_ALL,
    focus: str = ETF_FLOW_ALL,
) -> list:
    """
    Return the valid values for the *next* level of the ETF flow hierarchy,
    given a (possibly partial) selection of the levels above it.

    This is what a cascading / dependent drop-down should call: pick an
    ``asset_class``, and this returns every ``etfCategory`` available underneath
    it; additionally pick a ``category`` and it returns the ``etfNicheFocus``
    values underneath that, and so on. The returned list always starts with
    ``All`` so the caller can offer the aggregate option.

    The "next level" is the first level, scanning
    ``etfAssetClass -> etfCategory -> etfNicheFocus -> etfFocus``, that is still
    set to ``All``. If every level has been chosen, an empty list is returned.

    :param country_id: country entity (e.g. US) - resolved to the dataset countryId
    :param asset_class: ETF asset class selection, or All
    :param category: etfCategory selection, or All
    :param niche_focus: etfNicheFocus selection, or All
    :param focus: etfFocus selection, or All
    :return: list of available values for the next unselected level, prefixed with ``All``

    **Examples**

    Categories available for US Fixed Income:

    >>> etf_flow_coverage('US', 'Fixed Income')

    Niche focuses available for US Fixed Income / Government Treasury:

    >>> etf_flow_coverage('US', 'Fixed Income', 'Government Treasury')
    """
    # Resolve the (possibly parser-safe / differently-cased) selections to real
    # dataset values.
    selections = {
        'etfAssetClass': _dataset_value(_enum_or_str_value(asset_class)),
        'etfCategory': _dataset_value(_enum_or_str_value(category)),
        'etfNicheFocus': _dataset_value(_enum_or_str_value(niche_focus)),
        'etfFocus': _dataset_value(_enum_or_str_value(focus)),
    }

    # Determine the next level to populate (first one still set to All).
    next_level = None
    chosen = {}
    for dim in _ETF_FLOW_HIERARCHY:
        value = selections[dim]
        if value is None or str(value) == ETF_FLOW_ALL:
            next_level = dim
            break
        chosen[dim] = value

    if next_level is None:
        # Every level already selected - nothing further to drill into.
        return []

    # First try the static classification tree built from the FactSet CSV: walk
    # down the chosen branch and return the children at the next level. Values
    # are returned as parser-safe labels so they can be used in plot expressions.
    children = _classification_children(chosen, next_level)
    if children is not None:
        return [ETF_FLOW_ALL] + [_parser_safe_label(v) for v in children]

    # Fall back to querying the dataset for branches not covered by the CSV.
    country_code = _resolve_country_code(country_id)
    start, end = DataContext.current.start_date, DataContext.current.end_date

    server_filters, client_filters = _split_filters(chosen)
    query_filters = {'countryId': country_code, **server_filters}

    ds = Dataset(ETF_FLOWS_DATASET_ID)
    try:
        df = ds.get_data(start=start, end=end, **query_filters)
    except Exception as e:
        raise MqValueError(f'Could not query dataset {ETF_FLOWS_DATASET_ID} because of {e}')

    df = _apply_client_filters(df, client_filters)

    if df.empty or next_level not in df.columns:
        return [ETF_FLOW_ALL]

    values = sorted(v for v in df[next_level].dropna().unique())
    return [ETF_FLOW_ALL] + [_parser_safe_label(v) for v in values]


def _etf_metric(
    country_id: str,
    asset_class: str,
    category: str,
    niche_focus: str,
    focus: str,
    metric: 'ETFFlowMetric',
) -> pd.Series:
    """
    Shared implementation for the aggregated FactSet ETF measures.

    Every hierarchy level accepts a parser-safe label (case-insensitive) or the
    sentinel ``All`` to sum across every value underneath it. Labels are
    translated back to the real dataset values (which may contain commas, dashes,
    slashes, ampersands) before querying.
    """
    country_code = _resolve_country_code(country_id)
    start, end = DataContext.current.start_date, DataContext.current.end_date

    # Resolve each (possibly parser-safe / differently-cased) selection and build
    # the equality filters for every level that is not "All".
    selections = {
        'etfAssetClass': _dataset_value(_enum_or_str_value(asset_class)),
        'etfCategory': _dataset_value(_enum_or_str_value(category)),
        'etfNicheFocus': _dataset_value(_enum_or_str_value(niche_focus)),
        'etfFocus': _dataset_value(_enum_or_str_value(focus)),
    }
    # Values with special characters (e.g. commas) cannot be filtered by the
    # backend, so apply the safe ones server-side and the rest client-side.
    server_filters, client_filters = _split_filters(selections)
    query_filters = {'countryId': country_code, **server_filters}

    ds = Dataset(ETF_FLOWS_DATASET_ID)
    try:
        df = ds.get_data(start=start, end=end, **query_filters)
    except Exception as e:
        raise MqValueError(f'Could not query dataset {ETF_FLOWS_DATASET_ID} because of {e}')

    df = _apply_client_filters(df, client_filters)

    column = metric.value
    if df.empty or column not in df.columns:
        raise MqValueError(
            f'No {metric.name} data found in {ETF_FLOWS_DATASET_ID} for {country_code} with the selected hierarchy'
        )

    # Aggregate (sum) across every remaining dimension that was left as "All".
    grouped = df[column].groupby(level=0).sum().sort_index()

    series = ExtendedSeries(grouped, name=metric.value)
    series.dataset_ids = (ETF_FLOWS_DATASET_ID,)
    return series


_ETF_MEASURE_DOC = """
    Aggregated FactSet ETF {what} for a country, with drill-down.

    The dataset is organised as a hierarchy below the country::

        etfAssetClass -> etfCategory -> etfNicheFocus -> etfFocus

    Pass ``All`` at any level to sum across every value underneath it, or a
    parser-safe label (case-insensitive) to narrow to that branch. Lower levels
    only have meaningful choices once the levels above are chosen, e.g.::

        US.{fn}(All)                                     # whole country
        US.{fn}(Fixed Income, All, All, All)             # all Fixed Income
        US.{fn}(Fixed Income, Broad Market Asset backed, All, All)
        US.{fn}(Fixed Income, Broad Market Asset backed, Broad Credit, Broad Maturities)

    :param country_id: country entity (e.g. US) - resolved to the dataset countryId
    :param asset_class: etfAssetClass value, or All to sum across all asset classes
    :param category: etfCategory value, or All to sum across all categories
    :param niche_focus: etfNicheFocus value, or All to sum across all niche focuses
    :param focus: etfFocus value, or All to sum across all focuses
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD (not supported)
    :param request_id: server request id
    :return: aggregated daily time series for the selected slice of the hierarchy
"""


@plot_measure_entity(EntityType.COUNTRY)
def total_etf_flow(
    country_id: str,
    asset_class: str = ETF_FLOW_ALL,
    category: str = ETF_FLOW_ALL,
    niche_focus: str = ETF_FLOW_ALL,
    focus: str = ETF_FLOW_ALL,
    *,
    source: str = None,
    real_time: bool = False,
    request_id: Optional[str] = None,
) -> pd.Series:
    if real_time:
        raise NotImplementedError('real-time ETF flow data is not available')
    return _etf_metric(country_id, asset_class, category, niche_focus, focus, ETFFlowMetric.TOTAL_FLOW)


@plot_measure_entity(EntityType.COUNTRY)
def total_etf_shares_outstanding(
    country_id: str,
    asset_class: str = ETF_FLOW_ALL,
    category: str = ETF_FLOW_ALL,
    niche_focus: str = ETF_FLOW_ALL,
    focus: str = ETF_FLOW_ALL,
    *,
    source: str = None,
    real_time: bool = False,
    request_id: Optional[str] = None,
) -> pd.Series:
    if real_time:
        raise NotImplementedError('real-time ETF data is not available')
    return _etf_metric(country_id, asset_class, category, niche_focus, focus, ETFFlowMetric.SHARES_OUTSTANDING)


@plot_measure_entity(EntityType.COUNTRY)
def total_etf_assets(
    country_id: str,
    asset_class: str = ETF_FLOW_ALL,
    category: str = ETF_FLOW_ALL,
    niche_focus: str = ETF_FLOW_ALL,
    focus: str = ETF_FLOW_ALL,
    *,
    source: str = None,
    real_time: bool = False,
    request_id: Optional[str] = None,
) -> pd.Series:
    if real_time:
        raise NotImplementedError('real-time ETF data is not available')
    return _etf_metric(country_id, asset_class, category, niche_focus, focus, ETFFlowMetric.TOTAL_ASSETS)


@plot_measure_entity(EntityType.COUNTRY)
def total_etf_funds(
    country_id: str,
    asset_class: str = ETF_FLOW_ALL,
    category: str = ETF_FLOW_ALL,
    niche_focus: str = ETF_FLOW_ALL,
    focus: str = ETF_FLOW_ALL,
    *,
    source: str = None,
    real_time: bool = False,
    request_id: Optional[str] = None,
) -> pd.Series:
    if real_time:
        raise NotImplementedError('real-time ETF data is not available')
    return _etf_metric(country_id, asset_class, category, niche_focus, focus, ETFFlowMetric.TOTAL_FUNDS)


total_etf_flow.__doc__ = _ETF_MEASURE_DOC.format(what='flows', fn='total_etf_flow')
total_etf_shares_outstanding.__doc__ = _ETF_MEASURE_DOC.format(
    what='shares outstanding', fn='total_etf_shares_outstanding'
)
total_etf_assets.__doc__ = _ETF_MEASURE_DOC.format(what='assets', fn='total_etf_assets')
total_etf_funds.__doc__ = _ETF_MEASURE_DOC.format(what='fund count', fn='total_etf_funds')


# ---------------------------------------------------------------------------
# Asset-level total return (price appreciation + dividends)
# ---------------------------------------------------------------------------


class TotalReturnComponent(Enum):
    """Which part of the total return to return."""

    TOTAL = 'total'  # price appreciation + cash dividends
    PRICE = 'price'  # price appreciation only
    DIVIDEND = 'dividend'  # dividend contribution only


def _cash_dividends_per_share(asset: Asset, start, end) -> pd.Series:
    """
    Return cash dividends per share for an asset, indexed by effective (ex) date.

    Dividends come from the Security Master corporate-actions endpoint, which
    carries the true per-share cash amount for each 'Cash Dividend' event (the
    price datasets' adjustedClosePrice is not dividend-adjusted, so we cannot
    derive dividends from prices alone).
    """
    gsid = asset.get_identifier(AssetIdentifier.GSID)
    if gsid is None:
        return pd.Series(dtype=float)

    try:
        corporate_actions = GsSecurityMasterApi.get_corporate_actions(id_value=gsid, id_type=SecMasterIdentifiers.GSID)
    except Exception:
        return pd.Series(dtype=float)

    amounts = {}
    for ca in corporate_actions or []:
        if ca.get('eventType') != 'Cash Dividend':
            continue
        eff = ca.get('effectiveDate')
        if eff is None:
            continue
        eff_date = pd.Timestamp(eff)
        if eff_date < pd.Timestamp(start) or eff_date > pd.Timestamp(end):
            continue
        # sum any cash records on the event (per share, in the dividend currency)
        total = 0.0
        for record in ca.get('records', []):
            if record.get('instrument_type') == 'Currency' and record.get('dataValue') is not None:
                total += float(record['dataValue'])
        if total:
            amounts[eff_date] = amounts.get(eff_date, 0.0) + total

    if not amounts:
        return pd.Series(dtype=float)
    return pd.Series(amounts).sort_index()


def _total_return_series(asset: Asset, component: 'TotalReturnComponent') -> pd.Series:
    """
    Build a cumulative total-return (%) series for an asset.

    Total return captures both price appreciation and cash dividends. Because the
    adjusted close price is not dividend-adjusted in the price datasets, the
    dividend leg is taken from the corporate-actions (Cash Dividend) events and
    accumulated by ex-date. Values are expressed in percentage points (i.e.
    scaled by 100, so a 10% return is returned as ``10.0``)::

        price return (t)    = 100 * (closePrice(t) - closePrice(start)) / closePrice(start)
        dividend return (t) = 100 * (sum of dividends with ex-date <= t) / closePrice(start)
        total return (t)    = 100 * (closePrice(t) - closePrice(start) + dividends(t)) / closePrice(start)
    """
    start, end = DataContext.current.start_date, DataContext.current.end_date

    close = asset.get_data_series(DataMeasure.CLOSE_PRICE, None, DataFrequency.DAILY, start, end)

    if close is None or close.empty:
        raise MqValueError(f'No close price data found for {asset.get_marquee_id()}')

    close = close.sort_index()

    # Starting price anchors the returns to the window; close(t) is the ending price.
    start_price = close.iloc[0]
    if start_price == 0:
        raise MqValueError('Starting price is zero - cannot compute total return')

    # Cumulative cash dividends per share, forward-filled onto the price dates.
    dividends = _cash_dividends_per_share(asset, start, end)
    if dividends.empty:
        cum_div = pd.Series(0.0, index=close.index)
    else:
        cum_div = dividends.cumsum().reindex(close.index, method='ffill').fillna(0.0)

    if component == TotalReturnComponent.PRICE:
        # price only: (ending price - starting price) / starting price
        values = (close - start_price) / start_price
    elif component == TotalReturnComponent.DIVIDEND:
        # dividend contribution: dividends / starting price
        values = cum_div / start_price
    else:
        # total return: (ending price - starting price + dividends) / starting price
        values = (close - start_price + cum_div) / start_price

    series = ExtendedSeries(values * 100.0, name='totalReturn')
    series.dataset_ids = getattr(close, 'dataset_ids', ())
    return series


@plot_measure(
    (AssetClass.Equity,),
    (AssetType.ETF, AssetType.Index, AssetType.Single_Stock),
    [QueryType.SPOT],
)
def total_return(
    asset: Asset,
    component: TotalReturnComponent = TotalReturnComponent.TOTAL,
    *,
    source: str = None,
    real_time: bool = False,
    request_id: Optional[str] = None,
) -> pd.Series:
    """
    Cumulative total return (%) of an asset over the date context, combining
    price appreciation and cash dividends.

    Total return is anchored at the start of the window and measured in
    percentage points (i.e. scaled by 100, so a 10% return is returned as
    ``10.0``)::

        price     = 100 * (closePrice(t) / closePrice(start) - 1)                (price only)
        dividend  = 100 * (sum of cash dividends, ex-date <= t) / close(start)   (dividends)
        total     = price + dividend                                            (price + dividends)

    Cash dividends are sourced from Security Master corporate-action events (the
    price datasets are not dividend-adjusted), so the ``total`` component equals
    ``100 * (ending price - starting price + dividends paid) / starting price`` on
    the final date.

    **Examples**

    Total return of SPY (price + dividends)::

        SPY.total_return()

    Price-only return / dividend contribution::

        SPY.total_return(price)
        SPY.total_return(dividend)

    :param asset: asset object loaded from security master
    :param component: which part of the return to show - total, price or dividend
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD (not supported)
    :param request_id: server request id
    :return: cumulative total return (%) time series
    """
    if real_time:
        raise NotImplementedError('real-time total return is not available')
    return _total_return_series(asset, component)


# ---------------------------------------------------------------------------
# Leveraged ETF exposure (gross / net) by country
#
# Leveraged ETFs are identified from SF_FACTSET_ETF_REFERENCE_YRBSW3R0: an ETF is
# leveraged when LEVERAGE_FACTOR is populated. Only ETFs whose ISO_COUNTRY matches
# the country are included. AUM comes from SF_FACTSET_ETF_TIME_SERIES_YRBSW3R0 as
# nav * sharesOutstanding.
#
#     gross exposure(t) = sum_i AUM_i(t) * |leverageFactor_i|
#     net exposure(t)   = sum_i AUM_i(t) *  leverageFactor_i
# ---------------------------------------------------------------------------

ETF_REFERENCE_DATASET_ID = 'SF_FACTSET_ETF_REFERENCE_YRBSW3R0'
ETF_TIME_SERIES_DATASET_ID = 'SF_FACTSET_ETF_TIME_SERIES_YRBSW3R0'

_logger = logging.getLogger(__name__)

# The data API accepts at most 500 ISINs per query and silently truncates a
# response at 30,000 rows, so requests are split into (ISIN batch x date
# window) tasks; any task that still comes back at the cap is bisected.
_ISIN_CHUNK = 500
_QUERY_ROW_CAP = 30000
_TS_WINDOW_DAYS = 180
_REFERENCE_LOOKBACK_DAYS = 7
# Concurrent requests in flight; the data service starts failing above this.
_MAX_CONCURRENCY = 8


def _chunks(items, size=_ISIN_CHUNK):
    for i in range(0, len(items), size):
        yield items[i : i + size]


def _date_windows(start, end, days=_TS_WINDOW_DAYS):
    start, end = pd.Timestamp(start).date(), pd.Timestamp(end).date()
    while start <= end:
        stop = min(end, start + pd.Timedelta(days=days - 1))
        yield start, stop
        start = stop + pd.Timedelta(days=1)


def _is_server_error(e) -> bool:
    status = getattr(e, 'status', None)
    return isinstance(status, int) and status >= 500


def _run(coro):
    """Run a coroutine from synchronous measure code (Jupyter is handled by nest_asyncio in gs_quant)."""
    return asyncio.run(coro)


async def _fetch_capped(ds, isins, start, end, semaphore):
    """
    Fetch one (isins, window) task via the async data API.

    * Row cap hit -> bisect by date (then ISINs) and re-fetch.
    * HTTP 5xx    -> the service fails deterministically on some bad (ETF, day)
      records, so bisect straight away (ISINs first, then dates) and skip only
      the single bad (ETF, day) cell with a warning.
    """
    single_cell = start >= end and len(isins) <= 1
    try:
        async with semaphore:
            df = await ds.get_data_async(start=start, end=end, isin=isins)
    except Exception as e:
        if not _is_server_error(e):
            raise
        if single_cell:
            _logger.warning('Skipping %s on %s: %s keeps returning a server error', isins, start, ds.id)
            return []
        truncated = True
    else:
        if df is None or len(df) < _QUERY_ROW_CAP or single_cell:
            return [df] if df is not None and not df.empty else []
        truncated = False

    split_isins = len(isins) > 1 and (truncated or start >= end)
    if split_isins:
        half = len(isins) // 2
        parts = [(isins[:half], start, end), (isins[half:], start, end)]
    else:
        mid = start + (end - start) // 2
        parts = [(isins, start, mid), (isins, mid + pd.Timedelta(days=1), end)]
    results = await asyncio.gather(*(_fetch_capped(ds, i, s, e, semaphore) for i, s, e in parts))
    return [df for frames in results for df in frames]


async def _fetch_time_series_async(ds, isins, start, end):
    """Fetch the full nav / sharesOutstanding history for ``isins`` concurrently without hitting the row cap."""
    semaphore = asyncio.Semaphore(_MAX_CONCURRENCY)
    tasks = [
        _fetch_capped(ds, chunk, s, e, semaphore)
        for chunk in _chunks(isins, _ISIN_CHUNK)
        for s, e in _date_windows(start, end)
    ]
    try:
        results = await asyncio.gather(*tasks)
    except Exception as e:
        raise MqValueError(f'Could not query dataset {ds.id} because of {e}')
    return [df for frames in results for df in frames]


async def _leveraged_etfs_async(country_code: str) -> pd.Series:
    """Return leverage factor indexed by ISIN for leveraged ETFs with ISO_COUNTRY == ``country_code``."""
    try:
        coverage = await GsDataApi.get_coverage_async(ETF_REFERENCE_DATASET_ID)
    except Exception as e:
        raise MqValueError(f'Could not query coverage of {ETF_REFERENCE_DATASET_ID} because of {e}')
    isins = sorted({row['isin'] for row in coverage or [] if row.get('isin')})
    if not isins:
        raise MqValueError(f'No coverage found in {ETF_REFERENCE_DATASET_ID}')

    # Reference data is a daily snapshot; a short lookback gives the latest row per ISIN.
    end = pd.Timestamp.today().date()
    start = end - pd.Timedelta(days=_REFERENCE_LOOKBACK_DAYS)
    ds = Dataset(ETF_REFERENCE_DATASET_ID)
    semaphore = asyncio.Semaphore(_MAX_CONCURRENCY)

    async def fetch(chunk):
        async with semaphore:
            return await ds.get_data_async(start=start, end=end, isin=chunk, isoCountry=country_code)

    try:
        results = await asyncio.gather(*(fetch(chunk) for chunk in _chunks(isins)))
    except Exception as e:
        raise MqValueError(f'Could not query dataset {ETF_REFERENCE_DATASET_ID} because of {e}')
    frames = [df for df in results if df is not None and not df.empty]
    if not frames:
        return pd.Series(dtype=float)
    ref = pd.concat(frames)
    if 'leverageFactor' not in ref.columns:
        return pd.Series(dtype=float)
    if 'isoCountry' in ref.columns:
        ref = ref[ref['isoCountry'] == country_code]
    ref = ref.dropna(subset=['leverageFactor']).sort_index()
    return ref.groupby('isin')['leverageFactor'].last().astype(float)


async def _leveraged_aum_frame_async(country_code: str, start, end) -> pd.DataFrame:
    """Daily (isin, aum, leverageFactor) rows for the country's leveraged ETFs."""
    factors = await _leveraged_etfs_async(country_code)
    factors = factors[factors != 0]
    if factors.empty:
        raise MqValueError(f'No leveraged ETFs found in {ETF_REFERENCE_DATASET_ID} for {country_code}')

    ds = Dataset(ETF_TIME_SERIES_DATASET_ID)
    frames = await _fetch_time_series_async(ds, factors.index.tolist(), start, end)
    if not frames:
        raise MqValueError(f'No NAV / shares outstanding data found for leveraged ETFs in {country_code}')

    ts = pd.concat(frames).dropna(subset=['nav', 'sharesOutstanding'])
    if ts.empty:
        raise MqValueError(f'No NAV / shares outstanding data found for leveraged ETFs in {country_code}')
    # Drop duplicate (date, isin) rows that can appear when a capped task was bisected.
    ts = ts[~pd.MultiIndex.from_arrays([ts.index, ts['isin']]).duplicated()]

    return pd.DataFrame(
        {
            'isin': ts['isin'],
            'aum': ts['nav'].astype(float) * ts['sharesOutstanding'].astype(float),
            'leverageFactor': ts['isin'].map(factors).astype(float),
        },
        index=ts.index,
    )


def _leverage_exposure(country_id: str, gross: bool) -> pd.Series:
    country_code = _resolve_country_code(country_id)
    start, end = DataContext.current.start_date, DataContext.current.end_date

    frame = _run(_leveraged_aum_frame_async(country_code, start, end))
    lev = frame['leverageFactor'].abs() if gross else frame['leverageFactor']
    grouped = (frame['aum'] * lev).groupby(level=0).sum().sort_index()

    series = ExtendedSeries(grouped, name='grossLeverageExposure' if gross else 'netLeverageExposure')
    series.dataset_ids = (ETF_REFERENCE_DATASET_ID, ETF_TIME_SERIES_DATASET_ID)
    return series


@plot_measure_entity(EntityType.COUNTRY)
def gross_leverage_exposure(
    country_id: str, *, source: str = None, real_time: bool = False, request_id: Optional[str] = None
) -> pd.Series:
    """
    Gross leveraged-ETF exposure for a country: sum over leveraged ETFs (non-empty
    LEVERAGE_FACTOR) whose ISO_COUNTRY is the country of AUM * |leverage factor|,
    where AUM = nav * sharesOutstanding.

    **Examples**

    >>> US.gross_leverage_exposure()

    :param country_id: country entity (e.g. US), matched against ISO_COUNTRY
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD (not supported)
    :param request_id: server request id
    :return: daily gross leverage exposure time series
    """
    if real_time:
        raise NotImplementedError('real-time leverage exposure is not available')
    return _leverage_exposure(country_id, gross=True)


@plot_measure_entity(EntityType.COUNTRY)
def net_leverage_exposure(
    country_id: str, *, source: str = None, real_time: bool = False, request_id: Optional[str] = None
) -> pd.Series:
    """
    Net leveraged-ETF exposure for a country: sum over leveraged ETFs (non-empty
    LEVERAGE_FACTOR) whose ISO_COUNTRY is the country of AUM * leverage factor
    (inverse funds net off), where AUM = nav * sharesOutstanding.

    **Examples**

    >>> US.net_leverage_exposure()

    :param country_id: country entity (e.g. US), matched against ISO_COUNTRY
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD (not supported)
    :param request_id: server request id
    :return: daily net leverage exposure time series
    """
    if real_time:
        raise NotImplementedError('real-time leverage exposure is not available')
    return _leverage_exposure(country_id, gross=False)
