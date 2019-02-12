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
from gs_quant.session import GsSession
from datetime import date, datetime
from itertools import chain
import pandas as pd
from typing import Union, List, Tuple, Optional


def snapshot_coordinates(
    coordinates: Union[List, Tuple],
    as_of: Union[date, datetime],
    vendor: str = 'Goldman Sachs',
    as_dataframe: bool=False
) -> Union[dict, pd.DataFrame]:
    is_time = isinstance(as_of, datetime)
    ret = {coordinate: None for coordinate in coordinates}

    query = DataQuery(
        marketDataCoordinates=coordinates,
        vendor=vendor,
        endDate=as_of if not is_time else None,
        endTime=as_of if is_time else None
    )
    response = GsSession.current._post('/data/coordinates/query/last', query)

    for idx, row in enumerate(response['data']):
        if not row:
            continue

        value = row[row['field']]
        ret[coordinates[idx]] = value

    if as_dataframe:
        data = [dict(chain(c.as_dict().items(), (('value', v),))) for c, v in ret.items()]
        return pd.DataFrame(data)

    return ret


def coordinates_data(
    coordinates: Union[List, Tuple],
    start: Optional[Union[date, datetime]] = None,
    end: Optional[Union[date, datetime]] = None,
    vendor: str = 'Goldman Sachs',
    as_of: Optional[datetime] = None,
    since: Optional[datetime] = None,
) -> pd.DataFrame:
    if isinstance(start, datetime) != isinstance(end, datetime):
        raise RuntimeError('start and end must both either be dates or datetimes')

    is_time = isinstance(start, datetime)

    query = DataQuery(
        marketDataCoordinates=coordinates,
        vendor=vendor,
        startDate=start if not is_time else None,
        startTime=start if is_time else None,
        endDate=end if not is_time else None,
        endTime=end if is_time else None,
        asOfTime=as_of,
        since=since
    )
    response = GsSession.current._post('/data/coordinates/query', query)

    return pd.DataFrame(response['data'])

