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

import datetime
from enum import Enum
from typing import Union, Iterable

from gs_quant.data import Dataset
import pandas as pd
import numpy as np


class MissingDataStrategy(Enum):
    fill_forward = 'fill_forward'
    interpolate = 'interpolate'
    fail = 'fail'


class GsDataSource:
    def __init__(self, data_set: str, asset_id: str, min_date: datetime.date = None, max_date: datetime.date = None,
                 value_header: str = 'rate'):
        self._data_set = data_set
        self._asset_id = asset_id
        self._min_date = min_date
        self._max_date = max_date
        self._value_header = value_header
        self._loaded_data = None

    def get_data(self, state: Union[datetime.date, datetime.datetime] = None):
        if self._loaded_data is None:
            ds = Dataset(self._data_set)
            self._loaded_data = ds.get_data(self._min_date or state, self._max_date or state, assetId=(self._asset_id,))
        return self._loaded_data[self._value_header]


class GenericDataSource:
    def __init__(self, data_set: pd.Series, missing_data_strategy: MissingDataStrategy = MissingDataStrategy.fail):
        self._data_set = data_set
        self._missing_data_strategy = missing_data_strategy
        self._timer = datetime.datetime(1900, 1, 1, 0, 0, 0)
        if self._missing_data_strategy == MissingDataStrategy.interpolate:
            self._data_set.interpolate()
        elif self._missing_data_strategy == MissingDataStrategy.fill_forward:
            self._data_set.ffill()

    def update(self, state: datetime.datetime):
        self._timer = state

    def get_data(self, state: Union[datetime.date, datetime.datetime, Iterable]):
        """
        Get the value of the dataset at a time or date.  If a list of dates or times is provided return the avg value
        :param state: a date, datetime or a list of dates or datetimes
        :return: float value
        """

        if isinstance(state, Iterable):
            return np.mean([self.get_data(i) for i in state])
        if state > self._timer:
            raise RuntimeError(f'accessing data at {state} current time is {self._timer}, accessing future data '
                               f'forbidden')

        if state in self._data_set or self._missing_data_strategy == MissingDataStrategy.fail:
            return self._data_set[state]
        else:
            self._data_set.at[state] = np.nan
            self._data_set.sort_index()
            if self._missing_data_strategy == MissingDataStrategy.interpolate:
                self._data_set = self._data_set.interpolate()
            elif self._missing_data_strategy == MissingDataStrategy.fill_forward:
                self._data_set = self._data_set.ffill()
            else:
                raise RuntimeError(f'unrecognised missing data strategy: {str(self._missing_data_strategy)}')
            return self._data_set[state]
