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

import pandas as pd
from enum import Enum
from gs_quant.data import DataCoordinate
from typing import Union, List
from datetime import date, datetime
from .stream import DataSeries


class DataQueryType(Enum):
    LAST = 'LAST'
    RANGE = 'RANGE'


class DataQuery:
    """Defines a query on a coordinate"""

    def __init__(self, coordinate: DataCoordinate, start: Union[date, datetime] = None,
                 end: Union[date, datetime] = None, dates: List[Union[date, datetime]] = None,
                 query_type: DataQueryType = DataQueryType.RANGE):
        """Initialize data query"""

        self.coordinate = coordinate
        self.start = start
        self.end = end
        self.dates = dates
        self.query_type = query_type

    def get_series(self) -> Union[pd.Series, None]:
        """Execute query and return series"""

        if self.query_type is DataQueryType.RANGE:
            return self.coordinate.get_series(self.start, self.end)

        if self.query_type is DataQueryType.LAST:
            return self.coordinate.last_value(self.end)

    def get_data_series(self) -> DataSeries:
        return DataSeries(self.get_series(), self.coordinate)
