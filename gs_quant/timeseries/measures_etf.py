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


class ETFAssetClass(Enum):
    ALL = 'All'
    EQUITY = 'Equity'
    FIXED_INCOME = 'Fixed Income'
    COMMODITIES = 'Commodities'
    CURRENCY = 'Currency'
    ALTERNATIVES = 'Alternatives'
    ASSET_ALLOCATION = 'Asset Allocation'


class ETFCategory(Enum):
    ALL = 'All'
    AGRICULTURE = 'Agriculture'
    ASSET_ALLOCATION = 'Asset Allocation'
    BASKET = 'Basket'
    BROAD_MARKET = 'Broad Market'
    BROAD_MARKET_ASSET_BACKED = 'Broad Market, Asset-backed'
    BROAD_MARKET_BROAD_BASED = 'Broad Market, Broad-based'
    CORPORATE_ASSET_BACKED = 'Corporate, Asset-backed'
    CORPORATE_BANK_LOANS = 'Corporate, Bank Loans'
    CORPORATE_BROAD_BASED = 'Corporate, Broad-based'
    CORPORATE_CONVERTIBLE = 'Corporate, Convertible'
    CORPORATE_PREFERRED = 'Corporate, Preferred'
    ENERGY = 'Energy'
    GOVERNMENT_AGENCY = 'Government, Agency'
    GOVERNMENT_BROAD_BASED = 'Government, Broad-based'
    GOVERNMENT_INFLATION_LINKED = 'Government, Inflation-linked'
    GOVERNMENT_LOCAL_MUNICIPAL = 'Government, Local Authority/Municipal'
    GOVERNMENT_MORTGAGE_BACKED = 'Government, Mortgage-backed'
    GOVERNMENT_NON_NATIVE_CURRENCY = 'Government, Non-native currency'
    GOVERNMENT_TREASURY = 'Government, Treasury'
    HEDGE_FUND_STRATEGIES = 'Hedge Fund Strategies'
    HIGH_DIVIDEND_YIELD = 'High Dividend Yield'
    INDUSTRIAL_METALS = 'Industrial Metals'
    METALS = 'Metals'
    PAIR = 'Pair'
    PRECIOUS_METALS = 'Precious Metals'
    SECTOR = 'Sector'
    SIZE_AND_STYLE = 'Size and Style'
    STRUCTURED_OUTCOME = 'Structured Outcome'
    TACTICAL_TOOLS = 'Tactical Tools'


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
    asset_class=ETFAssetClass.ALL,
    category=ETFCategory.ALL,
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

    >>> etf_flow_coverage('US', ETFAssetClass.FIXED_INCOME)

    Niche focuses available for US Fixed Income / Government, Treasury:

    >>> etf_flow_coverage('US', ETFAssetClass.FIXED_INCOME, ETFCategory.GOVERNMENT_TREASURY)
    """
    country_code = _resolve_country_code(country_id)
    start, end = DataContext.current.start_date, DataContext.current.end_date

    selections = {
        'etfAssetClass': _enum_or_str_value(asset_class),
        'etfCategory': _enum_or_str_value(category),
        'etfNicheFocus': _enum_or_str_value(niche_focus),
        'etfFocus': _enum_or_str_value(focus),
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
    return [ETF_FLOW_ALL] + values


@plot_measure_entity(EntityType.COUNTRY)
def etf_flow(
    country_id: str,
    asset_class: ETFAssetClass = ETFAssetClass.ALL,
    category: ETFCategory = ETFCategory.ALL,
    niche_focus: str = ETF_FLOW_ALL,
    focus: str = ETF_FLOW_ALL,
    metric: ETFFlowMetric = ETFFlowMetric.TOTAL_FLOW,
    *,
    source: str = None,
    real_time: bool = False,
    request_id: Optional[str] = None,
) -> pd.Series:
    """
    Aggregated FactSet ETF flows (and assets) for a country, with drill-down.

    The dataset is organised as a hierarchy below the country::

        etfAssetClass -> etfCategory -> etfNicheFocus -> etfFocus

    Pass ``All`` at any level to sum across every value underneath it. Specify a
    value to narrow the aggregation to that branch of the hierarchy. A higher
    level should be chosen before the next level has meaningful choices, e.g.
    ``etf_flow(All)`` sums every flow in the country, ``etf_flow(Fixed Income, All)``
    sums every flow in Fixed Income, whereas
    ``etf_flow(Fixed Income, Government Treasury, All)`` restricts to the
    Treasury category.

    :param country_id: country entity (e.g. US) - resolved to the dataset countryId
    :param asset_class: ETF asset class, or All to sum across all asset classes
    :param category: etfCategory value, or All to sum across all categories
    :param niche_focus: etfNicheFocus value, or All to sum across all niche focuses
    :param focus: etfFocus value, or All to sum across all focuses
    :param metric: value to aggregate - flow (default), shares outstanding, assets or fund count
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD (not supported)
    :param request_id: server request id
    :return: aggregated daily time series for the selected slice of the hierarchy

    **Examples**

    Sum every ETF flow in the US:

    >>> US.etf_flow(All)

    Sum every Fixed Income ETF flow in the US:

    >>> US.etf_flow(Fixed Income, All)
    """
    if real_time:
        raise NotImplementedError('real-time ETF flow data is not available')
    if not isinstance(asset_class, ETFAssetClass):
        raise MqValueError('Invalid asset_class argument')
    if not isinstance(category, ETFCategory):
        raise MqValueError('Invalid category argument')
    if not isinstance(metric, ETFFlowMetric):
        raise MqValueError('Invalid metric argument')

    country_code = _resolve_country_code(country_id)
    start, end = DataContext.current.start_date, DataContext.current.end_date

    # Build the equality filters for every level that is not "All".
    selections = {
        'etfAssetClass': _enum_or_str_value(asset_class),
        'etfCategory': _enum_or_str_value(category),
        'etfNicheFocus': _enum_or_str_value(niche_focus),
        'etfFocus': _enum_or_str_value(focus),
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
