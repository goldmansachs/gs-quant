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
from enum import Enum

from gs_quant.target.data import *
from gs_quant.api.data import DataApi
from gs_quant.errors import MqValueError
import datetime as dt
import pandas as pd
from typing import Iterable, Optional, Union, List


class DataSet:

    class Ids(Enum):
        HOLIDAY = 'HOLIDAY'
        EDRVOL_PERCENT_INTRADAY =  'EDRVOL_PERCENT_INTRADAY'
        EDRVOL_PERCENT_SHORT = 'EDRVOL_PERCENT_SHORT'
        EDRVOL_PERCENT_LONG = 'EDRVOL_PERCENT_LONG'
        TREOD = 'TREOD'
        MA_RANK = 'MA_RANK'
        EDRVS_INDEX_SHORT = 'EDRVS_INDEX_SHORT'
        EDRVS_INDEX_LONG = 'EDRVS_INDEX_LONG'


    def __init__(self, dataset_id: Union[str, Ids], provider: DataApi=None):

        dataset_id_str = self._get_dataset_id_str(dataset_id)

        self.__id = dataset_id_str

        self.__provider = provider

    def _get_dataset_id_str(self, dataset_id):
        if dataset_id in self.Ids:
            dataset_id_str = dataset_id.value
        else:
            dataset_id_str = dataset_id

        return dataset_id_str

    @property
    def id(self):
        return self.__id

    @property
    def provider(self):
        from gs_quant.api.gs.data import GsDataApi
        return self.__provider or GsDataApi

    def get_data(
        self,
        start: Optional[Union[dt.date, dt.datetime]] = None,
        end: Optional[Union[dt.date, dt.datetime]] = None,
        as_of: Optional[dt.datetime] = None,
        since: Optional[dt.datetime] = None,
        fields: Optional[Iterable[str]] = None,
        **kwargs
    ) -> pd.DataFrame:
        query = self.provider.build_query(
            start=start,
            end=end,
            as_of=as_of,
            since=since,
            fields=fields,
            **kwargs
        )

        data = self.provider.query_data(query, self.id)
        return pd.DataFrame(data)

    def get_data_series(
            self,
            field: str,
            start: Optional[Union[dt.date, dt.datetime]] = None,
            end: Optional[Union[dt.date, dt.datetime]] = None,
            as_of: Optional[dt.datetime] = None,
            since: Optional[dt.datetime] = None,
            **kwargs
    ) -> pd.Series:
        query = self.provider.build_query(
            start=start,
            end=end,
            as_of=as_of,
            since=since,
            fields=(field,),
            **kwargs
        )

        symbol_dimensions = self.provider.symbol_dimensions(self.id)
        if len(symbol_dimensions) != 1:
            raise MqValueError('get_data_series only valid for symbol_dimensions of length 1')

        symbol_dimension = symbol_dimensions[0]

        df = pd.DataFrame(self.provider.query_data(query, self.id))

        gb = df.groupby(symbol_dimension)
        if len(gb.groups) > 1:
            raise MqValueError('Not a series for a single {}'.format(symbol_dimension))

        time_field = self.provider.time_field(self.id)
        index = pd.to_datetime(df.loc[:, time_field].values)
        return pd.Series(index=index, data=df.loc[:, field].values)

    def get_data_last(
        self,
        as_of: Optional[Union[dt.date, dt.datetime]],
        start: Optional[Union[dt.date, dt.datetime]] = None,
        fields: Optional[Iterable[str]] = None,
        **kwargs
    ) -> pd.DataFrame:
        query = self.provider.build_query(
            start=start,
            end=as_of,
            fields=fields,
            **kwargs
        )

        data = self.provider.last_data(query, self.id)
        return pd.DataFrame(data)

    def get_coverage(
        self,
            limit: int = None,
            offset: int = None,
            fields: List[str] = None
    ) -> pd.DataFrame:
        coverage = self.provider.get_coverage(
            self.id,
            limit=limit,
            offset=offset,
            fields=fields
        )

        return pd.DataFrame(coverage)
