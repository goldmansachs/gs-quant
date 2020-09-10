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
from abc import ABCMeta
from datetime import date, datetime
from enum import Enum
from typing import Union, Dict, Tuple, Optional

import pandas as pd

from .core import DataContext, DataFrequency
from .dataset import Dataset
from .fields import DataMeasure, DataDimension

DataDimensions = Dict[Union[DataDimension, str], Union[str, float]]
DateOrDatetime = Union[date, datetime]


class BaseDataCoordinate(metaclass=ABCMeta):
    """Base class for data coordinates"""

    __slots__ = ['__measure', '__dimensions']

    def __init__(self,
                 measure: DataMeasure,
                 dimensions: Optional[DataDimensions] = None):
        self.__measure = measure
        # Sorted so different dimension orders doesn't matter
        if dimensions is None:
            self.__dimensions = tuple()
        else:
            self.__dimensions = tuple(
                sorted({k.value if isinstance(k, Enum) else k: v for k, v in dimensions.items()}.items()))

    @property
    def measure(self) -> DataMeasure:
        return self.__measure

    @property
    def dimensions(self) -> Dict:
        return dict(self.__dimensions)

    def get_series(self,
                   start: Optional[DateOrDatetime] = None,
                   end: Optional[DateOrDatetime] = None):
        pass


class DataCoordinate(BaseDataCoordinate):
    """A coordinate which locates a given datapoint through time"""

    __slots__ = ['__dataset_id', '__frequency']

    def __init__(self,
                 dataset_id: str,
                 measure: DataMeasure,
                 dimensions: Optional[DataDimensions] = None,
                 frequency: Optional[DataFrequency] = None):
        """Initialize data coordinate

        :param dataset_id: Unique identifier for dataset
        :param measure: Unique identifier for data measure (dataset numerical field to query)
        :param dimensions: dict of dimensions to uniquely query dataset (e.g. keys)

        ** Usage **

        A DataCoordinate uniquely identifies a single timeseries on the GS Data Platform. Any dataset has a given
        set of dimensions (keys or identifiers over which to query) and measures (values which can be aggregated).

        A single coordinate specifies the identifier of the dataset, values of each required dimension through a
        dict, and a specific data measure (field). This can be used as a unique reference to query a timeseries
        on the platform over a given time range or sample point-in-time.

        DataCoordinates are immutable and can therefore be compared for equality
        """
        super().__init__(measure, dimensions)
        self.__dataset_id = dataset_id
        self.__frequency = frequency

    @property
    def dataset_id(self) -> str:
        return self.__dataset_id

    @property
    def frequency(self) -> DataFrequency:
        return self.__frequency

    def __eq__(self, other):
        """Determine if coordinates are equal

        :param other: other object

        ** Usage **

        Equality check for two coordinates. Validates if the dataset id, data measure and dimensions are equivalent.

        """
        return (self.dataset_id, self.measure, self.dimensions) == (other.dataset_id, other.measure, other.dimensions)

    def __hash__(self):
        return hash((self.dataset_id, self.measure, tuple(self.dimensions)))

    def get_range(self,
                  start: Optional[DateOrDatetime] = None,
                  end: Optional[DateOrDatetime] = None) -> Tuple[Optional[DateOrDatetime], Optional[DateOrDatetime]]:
        if start is None:
            start = DataContext.current.start_time if self.frequency is DataFrequency.REAL_TIME \
                else DataContext.current.start_date

        if end is None:
            end = DataContext.current.end_time if self.frequency is DataFrequency.REAL_TIME \
                else DataContext.current.end_date

        return start, end

    def get_series(self,
                   start: Optional[DateOrDatetime] = None,
                   end: Optional[DateOrDatetime] = None) -> Union[pd.Series, None]:
        """Get timeseries of coordinate"""

        if not self.dataset_id:
            return None

        dataset = Dataset(self.dataset_id)
        start, end = self.get_range(start, end)

        return dataset.get_data_series(self.measure, start=start, end=end, **self.dimensions)

    def last_value(self,
                   before: Optional[DateOrDatetime] = None) -> Union[float, None]:
        """Return the last available value

         Returns the last value prior to to the specified date / time. If `before` argument is not provided, will
         return the last value prior to the end date / time of the current data context

        """
        if not self.dataset_id:
            return None

        start, end = self.get_range(None, before)

        dataset = Dataset(self.dataset_id)
        measure = self.measure.value if isinstance(self.measure, Enum) else self.measure

        return dataset.get_data_last(end, fields=[measure], **self.dimensions).get(measure, default=None)
