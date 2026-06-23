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

import logging
from enum import Enum
from typing import Optional, Union

import pandas as pd

from gs_quant.api.gs.data import QueryType
from gs_quant.common import AssetClass, AssetType
from gs_quant.data import Dataset
from gs_quant.errors import MqValueError
from gs_quant.markets.securities import Asset, AssetIdentifier
from gs_quant.session import GsSession, Environment
from gs_quant.timeseries.helper import plot_measure
from gs_quant.timeseries.measures import ExtendedSeries, ASSET_SPEC, _asset_from_spec, MeasureDependency

_logger = logging.getLogger(__name__)

_CPN_STEP = 0.5
_TBA_DATASET = 'TBA_EOD_LEVELS'

# Agency prefixes
_AGENCIES = ['FNM', 'FDW', 'TSF']

# Coupon range: 2.00 to 7.00 in 0.50 steps
_COUPON_RANGE = [x / 2 for x in range(4, 15)]  # 2.0, 2.5, 3.0, ..., 7.0


class TBAAsset(Enum):
    """Enumeration of valid TBA asset names (agency + coupon)."""

    FNM_2_00 = 'FNM 2.00'
    FNM_2_50 = 'FNM 2.50'
    FNM_3_00 = 'FNM 3.00'
    FNM_3_50 = 'FNM 3.50'
    FNM_4_00 = 'FNM 4.00'
    FNM_4_50 = 'FNM 4.50'
    FNM_5_00 = 'FNM 5.00'
    FNM_5_50 = 'FNM 5.50'
    FNM_6_00 = 'FNM 6.00'
    FNM_6_50 = 'FNM 6.50'
    FNM_7_00 = 'FNM 7.00'

    FDW_2_00 = 'FDW 2.00'
    FDW_2_50 = 'FDW 2.50'
    FDW_3_00 = 'FDW 3.00'
    FDW_3_50 = 'FDW 3.50'
    FDW_4_00 = 'FDW 4.00'
    FDW_4_50 = 'FDW 4.50'
    FDW_5_00 = 'FDW 5.00'
    FDW_5_50 = 'FDW 5.50'
    FDW_6_00 = 'FDW 6.00'
    FDW_6_50 = 'FDW 6.50'
    FDW_7_00 = 'FDW 7.00'

    TSF_2_00 = 'TSF 2.00'
    TSF_2_50 = 'TSF 2.50'
    TSF_3_00 = 'TSF 3.00'
    TSF_3_50 = 'TSF 3.50'
    TSF_4_00 = 'TSF 4.00'
    TSF_4_50 = 'TSF 4.50'
    TSF_5_00 = 'TSF 5.00'
    TSF_5_50 = 'TSF 5.50'
    TSF_6_00 = 'TSF 6.00'
    TSF_6_50 = 'TSF 6.50'
    TSF_7_00 = 'TSF 7.00'


def _bbid_to_actual_asset(asset_spec: ASSET_SPEC) -> str:
    asset = _asset_from_spec(asset_spec)
    bbid = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)

    env = GsSession.current.environment
    if env == Environment.PROD:
        mapping = {
            'FNM': 'MA4R2VVY7F1MZ44R',
            'FDW': 'MAHV2RXBZA55YXVD',
            'TSF': 'MAMSQK44XNC6Z2D0',
        }
    else:
        mapping = {
            'FNM': 'MA97SYRKJ8WBPHQ7',
            'FDW': 'MAN48E7VAQT0GSHC',
            'TSF': 'MAYJPWRM8JMTMFWA',
        }

    if bbid in mapping:
        return mapping[bbid]
    return asset.get_marquee_id()


# Allowed coupon values (increments of 0.5)
_VALID_COUPONS = [x / 2 for x in range(2, 21)]  # 1.0, 1.5, 2.0, ..., 10.0
_CPN_SWAP_COUPONS = [c for c in _VALID_COUPONS if 1.0 <= c <= 10.0]
_BUTTERFLY_COUPONS = [c for c in _VALID_COUPONS if 1.0 <= c <= 10.0]


def _validate_coupon(coupon: float, allowed: list, measure_name: str) -> None:
    """Validate that coupon is in the set of allowed values.

    :param coupon: coupon value to validate
    :param allowed: list of allowed coupon values
    :param measure_name: name of the measure (for error message)
    """
    if coupon not in allowed:
        allowed_str = ', '.join(str(c) for c in allowed)
        raise MqValueError(f"Invalid coupon {coupon} for {measure_name}. Allowed values: {allowed_str}")


def _resolve_tba_asset_name(agency: str, coupon: float) -> str:
    """Resolve a TBA asset name from the TBAAsset enum.

    :param agency: agency prefix (e.g. 'FNM')
    :param coupon: coupon value (e.g. 5.0)
    :return: validated asset name string from TBAAsset enum
    """
    enum_key = f"{agency}_{coupon:.2f}".replace('.', '_')
    try:
        return TBAAsset[enum_key].value
    except KeyError:
        raise MqValueError(f"Invalid TBA asset: {agency} {coupon:.2f}. Must be a valid TBAAsset enum value.")


def _get_tba_prices(asset_name: str) -> pd.Series:
    """Fetch price3pmClose time series for a TBA asset from the TBA_EOD_LEVELS dataset.

    :param asset_name: name of the TBA asset (e.g. 'FNM 5.00')
    :return: pd.Series indexed by date with price3pmClose values
    """
    ds = Dataset(_TBA_DATASET)
    df = ds.get_data(fields=['price3pmClose'], name=asset_name)
    if df.empty:
        return ExtendedSeries(dtype=float)
    return pd.Series(df['price3pmClose'].values, index=df.index)


@plot_measure(
    (AssetClass.Mortgage,),
    (AssetType.TBA,),
    [MeasureDependency(id_provider=_bbid_to_actual_asset, query_type=QueryType.PRICE_3PM_CLOSE)],
)
def cpn_swap(
    asset: Asset,
    coupon: Union[int, float],
    *,
    source: str = None,
    real_time: bool = False,
    request_id: Optional[str] = None,
) -> pd.Series:
    """Return the price difference between two adjacent coupon TBAs.

    Fetches price3pmClose from the TBA_EOD_LEVELS dataset for
    ``<asset_name> <coupon>.00`` and ``<asset_name> <coupon - 0.50>.00``
    and returns the difference (coupon price minus lower coupon price).

    :param asset: base asset whose *name* is used as the prefix (e.g. an asset named 'FNM')
    :param coupon: coupon value (e.g. 5 → looks up 'FNM 5.00' and 'FNM 4.50')
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data (default: False)
    :param request_id: service request id, if any
    :return: time series of price differences between the two coupon assets

    **Usage**

    Compute the coupon swap spread for mortgage TBA assets.  Given a base
    asset name (e.g. ``FNM``) and a coupon of ``5``, the measure fetches
    the daily price3pmClose of *FNM 5.00* and *FNM 4.50* from the TBA_EOD_LEVELS
    dataset and returns the element-wise difference.

    **Examples**

    >>> from gs_quant.timeseries.measures_cpn_swap import cpn_swap
    >>> cpn_swap(fnm_asset, 5)
    """
    if real_time:
        raise MqValueError('real-time pricing is not supported for cpn_swap')

    coupon = float(coupon)
    _validate_coupon(coupon, _CPN_SWAP_COUPONS, 'cpn_swap')
    base_name = asset.name

    lower_name = _resolve_tba_asset_name(base_name, coupon - _CPN_STEP)
    upper_name = _resolve_tba_asset_name(base_name, coupon)

    series_lower = _get_tba_prices(lower_name)
    series_upper = _get_tba_prices(upper_name)

    # Align on common dates and compute difference
    combined = pd.concat([series_lower, series_upper], axis=1, keys=['lower', 'upper'])
    combined = combined.dropna()

    result = ExtendedSeries(combined['upper'] - combined['lower'], dtype=float)
    return result


@plot_measure(
    (AssetClass.Mortgage,),
    (AssetType.TBA,),
    [MeasureDependency(id_provider=_bbid_to_actual_asset, query_type=QueryType.PRICE_3PM_CLOSE)],
)
def butterfly(
    asset: Asset,
    coupon: Union[int, float],
    *,
    source: str = None,
    real_time: bool = False,
    request_id: Optional[str] = None,
) -> pd.Series:
    """Return the butterfly spread for three adjacent coupon TBAs.

    Computes ``2 * price(middle) - price(lower) - price(upper)`` where:
    - lower = ``<asset_name> <coupon - 0.50>.00``
    - middle = ``<asset_name> <coupon>.00``
    - upper = ``<asset_name> <coupon + 0.50>.00``

    :param asset: base asset whose *name* is used as the prefix (e.g. 'FNM')
    :param coupon: middle coupon value (e.g. 5 → uses FNM 4.50, FNM 5.00, FNM 5.50)
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data (default: False)
    :param request_id: service request id, if any
    :return: time series of butterfly spread values

    **Usage**

    Compute the butterfly spread for a 3-legged mortgage TBA trade.  Given a
    base asset name (e.g. ``FNM``) and a coupon of ``5``, the measure fetches
    the daily price3pmClose of *FNM 4.50*, *FNM 5.00*, and *FNM 5.50* from
    the TBA_EOD_LEVELS dataset and returns ``2 * FNM 5.00 - FNM 4.50 - FNM 5.50``.

    **Examples**

    >>> from gs_quant.timeseries.measures_cpn_swap import butterfly
    >>> butterfly(fnm_asset, 5)
    """
    if real_time:
        raise MqValueError('real-time pricing is not supported for butterfly')

    coupon = float(coupon)
    _validate_coupon(coupon, _BUTTERFLY_COUPONS, 'butterfly')
    base_name = asset.name

    lower_name = _resolve_tba_asset_name(base_name, coupon - _CPN_STEP)
    middle_name = _resolve_tba_asset_name(base_name, coupon)
    upper_name = _resolve_tba_asset_name(base_name, coupon + _CPN_STEP)

    series_lower = _get_tba_prices(lower_name)
    series_middle = _get_tba_prices(middle_name)
    series_upper = _get_tba_prices(upper_name)

    # Align on common dates and compute butterfly spread
    combined = pd.concat(
        [series_lower, series_middle, series_upper],
        axis=1,
        keys=['lower', 'middle', 'upper'],
    )
    combined = combined.dropna()

    result = ExtendedSeries(
        2 * combined['middle'] - combined['lower'] - combined['upper'],
        dtype=float,
    )
    return result
