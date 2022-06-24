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

import datetime as dt
from enum import Enum
import numpy as np
import pandas as pd
import pytz
from typing import Union, Iterable

from gs_quant.backtests.core import ValuationFixingType
from gs_quant.data import DataFrequency, Dataset
from gs_quant.instrument import Instrument


class MissingDataStrategy(Enum):
    fill_forward = 'fill_forward'
    interpolate = 'interpolate'
    fail = 'fail'


class DataSource:
    def get_data(self, state):
        raise RuntimeError("Implemented by subclass")


class GsDataSource(DataSource):
    def __init__(self, data_set: str, asset_id: str, min_date: dt.date = None, max_date: dt.date = None,
                 value_header: str = 'rate'):
        self._data_set = data_set
        self._asset_id = asset_id
        self._min_date = min_date
        self._max_date = max_date
        self._value_header = value_header
        self._loaded_data = None

    def get_data(self, state: Union[dt.date, dt.datetime] = None):
        if self._loaded_data is None:
            ds = Dataset(self._data_set)
            if self._min_date:
                self._loaded_data = ds.get_data(self._min_date, self._max_date, assetId=(self._asset_id,))
            else:
                return ds.get_data(state, state, assetId=(self._asset_id,))[self._value_header]
        return self._loaded_data[self._value_header].at[pd.to_datetime(state)]


class GenericDataSource(DataSource):
    def __init__(self, data_set: pd.Series, missing_data_strategy: MissingDataStrategy = MissingDataStrategy.fail):
        """
        A data source which holds a pandas series indexed by date or datetime
        :param data_set: a pandas dataframe indexed by date or datetime
        :param missing_data_strategy: MissingDataStrategy which defines behaviour if data is missing, will only take
                                      effect if using get_data, gat_data_range has no expectations of the number of
                                      expected data points.
        """
        self._data_set = data_set
        self._missing_data_strategy = missing_data_strategy
        self._tz_aware = isinstance(self._data_set.index[0],
                                    dt.datetime) and self._data_set.index[0].tzinfo is not None
        if self._missing_data_strategy == MissingDataStrategy.interpolate:
            self._data_set.interpolate()
        elif self._missing_data_strategy == MissingDataStrategy.fill_forward:
            self._data_set.ffill()

    def get_data(self, state: Union[dt.date, dt.datetime, Iterable]):
        """
        Get the value of the dataset at a time or date.  If a list of dates or times is provided return the avg value
        :param state: a date, datetime or a list of dates or datetimes
        :return: float value
        """
        if isinstance(state, Iterable):
            return [self.get_data(i) for i in state]

        if self._tz_aware and (state.tzinfo is None or state.tzinfo.utcoffset(state) is None):
            state = pytz.utc.localize(state)
        if pd.Timestamp(state) in self._data_set:
            return self._data_set[pd.Timestamp(state)]
        elif state in self._data_set or self._missing_data_strategy == MissingDataStrategy.fail:
            return self._data_set[state]
        else:
            if isinstance(self._data_set.index, pd.DatetimeIndex):
                self._data_set.at[pd.to_datetime(state)] = np.nan
                self._data_set.sort_index(inplace=True)
            else:
                self._data_set.at[state] = np.nan
            self._data_set.sort_index()
            if self._missing_data_strategy == MissingDataStrategy.interpolate:
                self._data_set = self._data_set.interpolate()
            elif self._missing_data_strategy == MissingDataStrategy.fill_forward:
                self._data_set = self._data_set.ffill()
            else:
                raise RuntimeError(f'unrecognised missing data strategy: {str(self._missing_data_strategy)}')
            return self._data_set[pd.to_datetime(state)] if isinstance(self._data_set.index,
                                                                       pd.DatetimeIndex) else self._data_set[state]

    def get_data_range(self, start: Union[dt.date, dt.datetime],
                       end: Union[dt.date, dt.datetime, int]):
        """
        get a range of values from the dataset.
        :param start: a date or datetime
        :param end: a date, datetime or an int.  If an int is provided we return that many data points back from the
                    start date
        :return: pd.Series
        """
        if isinstance(end, int):
            return self._data_set.loc[:start].tail(end)
        return self._data_set.loc[(start < self._data_set.index) & (self._data_set.index <= end)]


class DataManager:
    def __init__(self):
        self._data_sources = {}

    def add_data_source(self, series: Union[pd.Series, DataSource], data_freq: DataFrequency,
                        instrument: Instrument, valuation_type: ValuationFixingType):
        if not isinstance(series, DataSource) and not len(series):
            return
        if instrument.name is None:
            raise RuntimeError('Please add a name identify your instrument')
        key = (data_freq, instrument.name, valuation_type)
        if key in self._data_sources:
            raise RuntimeError('A dataset with this frequency instrument name and valuation type already added to '
                               'Data Manager')
        self._data_sources[key] = GenericDataSource(series) if isinstance(series, pd.Series) else series

    def get_data(self, state: Union[dt.date, dt.datetime], instrument: Instrument, valuation_type: ValuationFixingType):
        key = (DataFrequency.REAL_TIME if isinstance(state, dt.datetime) else DataFrequency.DAILY,
               instrument.name.split('_')[-1], valuation_type)
        return self._data_sources[key].get_data(state)

    def get_data_range(self, start: Union[dt.date, dt.datetime],
                       end: Union[dt.date, dt.datetime], instrument: Instrument, valuation_type: ValuationFixingType):
        key = (DataFrequency.REAL_TIME if isinstance(start, dt.datetime) else DataFrequency.DAILY,
               instrument.name.split('_')[-1], valuation_type)
        return self._data_sources[key].get_data_range(start, end)
