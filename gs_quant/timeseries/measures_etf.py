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
import re
from enum import Enum
from typing import Optional

import pandas as pd

from gs_quant.data import DataContext, Dataset
from gs_quant.entities.entity import Country, EntityType
from gs_quant.errors import MqValueError
from gs_quant.timeseries.etf_classification import ETF_CLASSIFICATION
from gs_quant.timeseries.helper import plot_measure_entity
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
