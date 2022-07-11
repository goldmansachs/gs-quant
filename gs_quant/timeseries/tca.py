"""
Copyright 2019 Goldman Sachs.
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

from typing import Optional

from pandas import Series

from gs_quant.api.gs.data import QueryType
from gs_quant.data import Dataset, DataContext
from gs_quant.markets.securities import Asset
from gs_quant.target.common import AssetClass
from gs_quant.timeseries import plot_measure
from gs_quant.timeseries.measures import _extract_series_from_df


@plot_measure((AssetClass.Equity,), None, [])
def covariance(asset: Asset,
               asset_2: Asset,
               bucket_start: str = '"08:00:00"',
               bucket_end: str = '"08:30:00"',
               *,
               source: str = None,
               real_time: bool = False,
               request_id: Optional[str] = None) -> Series:
    """
    Provides an estimates of the covariances between stocks in the three major equity markets - US, EMEA and Japan -
    using an advanced machine learning technique.

    :param asset: asset to calculate covariance
    :param asset_2: asset to calculate covariance
    :param bucket_start: start time of bucket i.e. '08:00:00'
    :param bucket_end: end time of bucket i.e. '08:30:00'
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: service request id, if any
    :return: Series of the covariance between two stocks
    """
    start, end = DataContext.current.start_date, DataContext.current.end_date
    ds = Dataset(Dataset.GS.QES_INTRADAY_COVARIANCE)
    where = dict(assetId=asset.get_marquee_id(), asset2Id=asset_2.get_marquee_id(), bucketStart=bucket_start,
                 bucketEnd=bucket_end)

    data = ds.get_data(start=start, end=end, where=where)
    series = _extract_series_from_df(data, QueryType.COVARIANCE)
    series.dataset_ids = (Dataset.GS.QES_INTRADAY_COVARIANCE.value,)
    return series
