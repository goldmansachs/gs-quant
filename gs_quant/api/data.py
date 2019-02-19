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
import datetime as dt
from typing import Optional, Union
from gs_quant.common import FieldFilterMap


class DataApi(metaclass=ABCMeta):

    @classmethod
    def query_data(cls, query: 'DataQuery', dataset: 'DataSet'=None) -> Union[list, tuple]:
        raise NotImplementedError('Must implement get_data')

    @classmethod
    def last_data(cls, query: 'DataQuery', dataset: 'DataSet'=None) -> Union[list, tuple]:
        raise NotImplementedError('Must implement last_data')

    @classmethod
    def symbol_dimensions(cls, dataset: 'DataSet') -> tuple:
        raise NotImplementedError('Must implement symbol_dimensions')

    @classmethod
    def time_field(cls, dataset: 'DataSet') -> str:
        raise NotImplementedError('Must implement time_field')

    @staticmethod
    def build_query(
        start: Optional[Union[dt.date, dt.datetime]] = None,
        end: Optional[Union[dt.date, dt.datetime]] = None,
        as_of: Optional[dt.datetime] = None,
        since: Optional[dt.datetime] = None,
        **kwargs
    ):
        from gs_quant.data import DataQuery

        is_time = isinstance(end, dt.datetime)
        if start is not None and is_time != isinstance(start, dt.datetime):
            raise ValueError('start and end must both either be date or datetime')

        query = DataQuery(
            startDate=start if not is_time else None,
            startTime=start if is_time else None,
            endDate=end if not is_time else None,
            endTime=end if is_time else None,
            asOfTime=as_of,
            since=since
        )

        where = FieldFilterMap()
        query_properties = query.properties()
        where_properties = where.properties()

        for field, value in kwargs.items():
            if field in query_properties:
                setattr(query, field, value)
            elif field in where_properties:
                setattr(where, field, value)
            else:
                raise ValueError('Invalid query field: ' + field)

        if where:
            query.where = where

        return query
