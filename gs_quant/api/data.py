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
from abc import ABCMeta
import inflection
from typing import Optional, Union

from gs_quant.target.common import FieldFilterMap
from gs_quant.target.data import DataQuery


class DataApi(metaclass=ABCMeta):
    @classmethod
    def query_data(cls, query: DataQuery, dataset_id: str = None) -> Union[list, tuple]:
        raise NotImplementedError('Must implement get_data')

    @classmethod
    def last_data(cls, query: DataQuery, dataset_id: str = None) -> Union[list, tuple]:
        raise NotImplementedError('Must implement last_data')

    @classmethod
    def symbol_dimensions(cls, dataset_id: str) -> tuple:
        raise NotImplementedError('Must implement symbol_dimensions')

    @classmethod
    def time_field(cls, dataset_id: str) -> str:
        raise NotImplementedError('Must implement time_field')

    @staticmethod
    def build_query(
            start: Optional[Union[dt.date, dt.datetime]] = None,
            end: Optional[Union[dt.date, dt.datetime]] = None,
            as_of: Optional[dt.datetime] = None,
            since: Optional[dt.datetime] = None,
            **kwargs
    ):
        from gs_quant.api.gs.data import DataQuery

        end_is_time = isinstance(end, dt.datetime)
        start_is_time = isinstance(start, dt.datetime)

        if start_is_time and end is not None and not end_is_time:
            raise ValueError('If start is of type datetime, so must end be!')

        if isinstance(start, dt.date) and end is not None and not isinstance(end, dt.date):
            raise ValueError('If start is of type date, so must end be!')

        query = DataQuery(
            start_date=start if not start_is_time else None,
            start_time=start if start_is_time else None,
            end_date=end if not end_is_time else None,
            end_time=end if end_is_time else None,
            as_of_time=as_of,
            since=since,
            format="MessagePack"
        )

        where = FieldFilterMap()
        query_properties = query.properties()
        where_properties = where.properties()

        for field, value in kwargs.items():
            snake_case_field = inflection.underscore(field)
            if snake_case_field in query_properties:
                setattr(query, snake_case_field, value)
            elif snake_case_field in where_properties:
                setattr(where, snake_case_field, value)
            else:
                raise ValueError('Invalid query field: ' + field)

        if where:
            query.where = where

        return query
