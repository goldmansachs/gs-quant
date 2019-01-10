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

from gs_quant.target.data import *
from gs_quant.api.common import FieldFilterMap
from gs_quant.api.risk import MarketDataCoordinate
from gs_quant.session import GsSession
from datetime import date, datetime, timedelta
import pandas as pd
from typing import Union, Iterable, Optional


def queries_for_coordinates(
    coordinates: Union[MarketDataCoordinate, Iterable[MarketDataCoordinate]],
    vendor: str,
    is_time: bool
) -> Iterable[DataQuery]:
    from gs_quant.api.dataset import Dataset

    queries = {}
    for coordinate in coordinates:
        dataset = Dataset.dataset_for_coordinate_vendor_is_time(coordinate, vendor, is_time)
        field = next(qs['field'] for qs in dataset.catalog['mdapi']['quotingStyles'] if qs['quotingStyle'] == coordinate.field) if coordinate.field else None

        query = queries.setdefault((coordinate.marketDataType, coordinate.pointClass), DataQuery(
            dataSetId=dataset.dataset_id,
            fields=[],
            where=FieldFilterMap(assetId=[], point=[], pointClass=coordinate.pointClass)))

        if field not in query.fields:
            query.fields.append(field)

        query.where.assetId.append(coordinate.assetId)
        query.where.point.append(coordinate.point)

    return tuple(queries.values())


def values_for_coordinates(
    coordinates: Union[MarketDataCoordinate, Iterable[MarketDataCoordinate]],
    vendor: str,
    as_of: Union[date, datetime]
) -> dict:
    from gs_quant.api.dataset import Dataset

    ret = {coordinate: None for coordinate in coordinates}
    session = GsSession.current
    is_time = isinstance(as_of, datetime)
    queries = queries_for_coordinates(coordinates, vendor, is_time)
    for query in queries:
        if is_time:
            query.endTime = as_of
            query.startTime = as_of - timedelta(days=1)
        else:
            query.endDate = as_of
            query.startDate = 4

    all_results = session._post('/data/last/query/bulk', queries)
    for idx, query_results in enumerate(all_results):
        query = queries[idx]
        dataset = Dataset(query.dataSetId)
        quotingStyles = dataset.catalog['mdapi']['quotingStyles']

        for result in query_results['data']:
            for quotingStyle in quotingStyles:
                field = quotingStyle['field']
                if field in query.fields:
                    coordinate = MarketDataCoordinate(
                        marketDataType=dataset.marketDataType,
                        assetId=result.get('assetId'),
                        pointClass=result.get('pointClass'),
                        point=result.get('point'),
                        field=quotingStyle['quotingStyle']
                    )

                    ret[coordinate] = result.get(field)

    return ret


def get_data(
    coordinate: MarketDataCoordinate,
    vendor: str,
    start: Optional[Union[date, datetime]] = None,
    end: Optional[Union[date, datetime]] = None,
    as_of: Optional[datetime] = None,
    since: Optional[datetime] = None,
) -> pd.Series:
    from gs_quant.api.dataset import Dataset

    dataset = Dataset.dataset_for_coordinate_vendor_is_time(coordinate, vendor, isinstance(end, datetime))
    field = next(qs['field'] for qs in dataset.catalog['mdapi']['quotingStyles'] if qs['quotingStyle'] == coordinate.field)
    return dataset.get_data(
        start=start,
        end=end,
        as_of=as_of,
        since=since,
        fields=(field,),
        assetId=coordinate.assetId,
        pointClass=coordinate.pointClass,
        point=coordinate.point
    )
