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
import logging
from abc import ABCMeta
from typing import Optional, Union, List

import inflection
import pandas as pd

from gs_quant.api.fred.fred_query import FredQuery
from gs_quant.base import Base
from gs_quant.target.coordinates import MDAPIDataQuery
from gs_quant.target.data import DataQuery

_logger = logging.getLogger(__name__)


class DataApi(metaclass=ABCMeta):
    @classmethod
    def query_data(cls, query: Union[DataQuery, FredQuery], dataset_id: str = None) -> Union[list, tuple]:
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

    @classmethod
    def construct_dataframe_with_types(cls, dataset_id: str, data: Union[Base, list, tuple, pd.Series]) -> pd.DataFrame:
        raise NotImplementedError('Must implement time_field')

    @staticmethod
    def build_query(
            start: Optional[Union[dt.date, dt.datetime]] = None,
            end: Optional[Union[dt.date, dt.datetime]] = None,
            as_of: Optional[dt.datetime] = None,
            since: Optional[dt.datetime] = None,
            restrict_fields: bool = False,
            format: str = 'MessagePack',
            dates: List[dt.date] = None,
            **kwargs
    ):
        end_is_time = isinstance(end, dt.datetime)
        start_is_time = isinstance(start, dt.datetime)

        if kwargs.get('market_data_coordinates'):
            real_time = ((start is None or start_is_time) and (end is None or end_is_time))
            query = MDAPIDataQuery(
                start_time=start if real_time else None,
                end_time=end if real_time else None,
                start_date=start if not real_time else None,
                end_date=end if not real_time else None,
                format=format,
                real_time=real_time,
                **kwargs
            )
        else:
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
                format=format,
                dates=dates
            )

        query_properties = query.properties()
        query.where = dict()
        for field, value in kwargs.items():
            snake_case_field = inflection.underscore(field)
            if snake_case_field in query_properties:
                setattr(query, snake_case_field, value)
            else:
                query.where[field] = value

        if getattr(query, 'fields', None) is not None:
            try:
                query.restrict_fields = restrict_fields
            except AttributeError as e:
                _logger.debug('unable to set restrict_fields', exc_info=e)

        return query
