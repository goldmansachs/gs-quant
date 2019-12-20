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

This product uses the FRED® API but is not endorsed or certified
by the Federal Reserve Bank of St. Louis. FRED terms of use
available at https://research.stlouisfed.org/docs/api/terms_of_use.html
"""

from typing import Iterable, Optional, Union

import pandas as pd
import datetime as dt
import textwrap
from gs_quant.api.utils import handle_proxy

from requests.exceptions import HTTPError

from dataclasses import asdict, replace

from gs_quant.api.data import DataApi
from gs_quant.api.fred.fred_query import FredQuery

"""
Fred Data API that provides functions to query the Fred dataset.
You need to specify a valid API key by passing in the string via api_key.
You can sign up for a free API key on the Fred website at:
http://research.stlouisfed.org/fred2/
"""


class FredDataApi(DataApi):
    earliest_realtime_start = '1776-07-04'
    latest_realtime_end = '9999-12-31'
    root_url = 'https://api.stlouisfed.org/fred/series/observations'

    def __init__(self, api_key=None):
        if api_key is not None:
            self.api_key = api_key
        else:
            raise ValueError(textwrap.dedent("""
                    Please pass a string with your API key. You can sign up for a free api key on the Fred website at
                    http://research.stlouisfed.org/fred2/"""))

    def build_query(
            self,
            start: Optional[Union[dt.date, dt.datetime]] = None,
            end: Optional[Union[dt.date, dt.datetime]] = None,
            as_of: Optional[dt.datetime] = None,
            since: Optional[dt.datetime] = None,
            fields: Optional[Iterable[str]] = None,
            **kwargs
    ) -> FredQuery:
        """
        Builds a FRED URL to query.

        :param start: Requested start date/datetime for data
        :param end: Requested end date/datetime for data
        :param as_of: Request data as_of
        :param since: Request data since
        :param fields: DataSet fields to include
        :param kwargs: Extra query arguments
        :return: a url string of the requested data
        """

        if start is not None and end is not None:
            if type(start) != type(end):
                raise ValueError('Start and end types must match!')

        request = FredQuery(observation_start=start, observation_end=end, realtime_end=as_of, realtime_start=since)
        return request

    def query_data(self, query: FredQuery, dataset_id: str, asset_id_type: str = None) -> pd.Series:
        """
        Query data given a valid FRED series id and url. Will raise an HTTPError if the response was an HTTP error.

        :param query: A url string of the requested data
        :param id: A FRED series id
        :return: with id as key and requested DataFrame as value.
        """
        request = replace(query, api_key=self.api_key, series_id=dataset_id)
        response = handle_proxy(self.root_url, asdict(request))
        handled = self.__handle_response(response)
        handled.name = dataset_id
        return handled

    def last_data(self, query: FredQuery, dataset_id: str) -> pd.Series:
        """
        Get the last point for a data series, at or before as_of

        :param query: A url string of the requested data
        :param id: A FRED series id
        :param kwargs: Extra query arguments
        :return: with id as key and last point for this DataSet as value.
        """

        data = self.query_data(query, dataset_id)
        return data.last('1D')

    @staticmethod
    def __handle_response(response: str) -> pd.Series:
        """
        Helper function for handling the response given a request URL.
        Will raise an HTTPError if the response was an HTTP error.
        """
        try:
            response.raise_for_status()
            json_data = response.json()
        except HTTPError:
            raise ValueError(response.json()['error_message'])
        if not len(json_data['observations']):
            raise ValueError('No data exists for {} for the provided parameters... '.format(id))

        data = pd.DataFrame(json_data['observations'])[['date', 'value']]
        data = data[data.value != '.']
        data['date'] = pd.to_datetime(data['date'])
        data['value'] = data['value'].astype(float)
        data = data.set_index('date')['value']
        data = data.sort_index()
        return data

    def construct_dataframe_with_types(self, dataset_id: str, data: pd.Series) -> pd.DataFrame:
        """
        Constructs a dataframe with correct date types.

        :param data: Data to convert with correct types
        :return: Dataframe with correct types
        """
        if len(data) and isinstance(data, pd.Series):
            return data.to_frame()
        else:
            return pd.DataFrame({})

    def symbol_dimensions(self, dataset_id: str) -> tuple:
        query = FredQuery()
        data = self.query_data(query, dataset_id)
        return data.shape

    def time_field(self, dataset_id: str) -> str:
        pass
