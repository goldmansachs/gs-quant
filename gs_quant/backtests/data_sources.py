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
from typing import Union

from gs_quant.data import Dataset


class DataSource(object):
    def get_data(self, state):
        """
        implemented by sub classes
        :param state:
        :return:
        """
        raise RuntimeError('has_triggered to be implemented by subclass')


class GsDataSource(DataSource):
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
