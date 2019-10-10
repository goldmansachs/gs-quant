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

//Portions copyright Maverick Lin. Licensed under Apache 2.0 license
"""

import os
import sys
from typing import Iterable, List, Optional, Tuple, Union

import json
import pandas as pd
import datetime as dt

import requests
from requests.utils import requote_uri
from requests.exceptions import HTTPError
from urllib.parse import urlencode

"""
Fred Data API that provides functions to query the Fred dataset. 
You need to specify a valid API key by passing in the string via api_key. 
You can sign up for a free API key on the Fred website at http://research.stlouisfed.org/fred2/
"""

class FredDataApi(object):
    earliest_realtime_start = '1776-07-04'
    latest_realtime_end = '9999-12-31'
    root_url = 'https://api.stlouisfed.org/fred'

    def __init__(self, api_key=None):
        if api_key is not None:
            self.api_key = api_key
        else:
            import textwrap
            raise ValueError(textwrap.dedent("""\
                    Please pass a string with your API key. You can sign up for 
                    a free api key on the Fred website at 
                    http://research.stlouisfed.org/fred2/"""))

    def build_query(
        self,
        start: Optional[Union[dt.date, dt.datetime]] = None,
        end: Optional[Union[dt.date, dt.datetime]] = None,
        as_of: Optional[dt.datetime] = None,
        since: Optional[dt.datetime] = None,
        fields: Optional[Iterable[str]] = None,
        **kwargs
    ) -> str: 
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
        
        if end is not None:
            assert(isinstance(end, dt.datetime) or isinstance(end, dt.date)), \
                "End must be of type dt.datetime or dt.date!"
        if start is not None:
            assert(isinstance(start, dt.datetime) or isinstance(start, dt.date)), \
                "Start must be of type dt.datetime or dt.date!"
        if start is not None and end is not None:
            if type(start) != type(end):
                raise ValueError('Start and end types must match!')
        
        url = ''
        date_dict = {
            "observation_start" : start,
            "observation_end" : end,
            "realtime_end" : as_of,
            "realtime_start" : since
        }
        for date in date_dict.keys():
            if date_dict[date] is not None:
                url += '&{}={}'.format(date, date_dict[date])

        if kwargs.keys():
            url += '&{}'.format(urlencode(kwargs))

        final_url = '{}/series/observations?series_id={{}}&api_key={}{}&\
            file_type=json'.format(self.root_url, self.api_key, url)
        return final_url

    def query_data(
        self, 
        query: str, 
        id: str, 
        asset_id_type=None
    ) -> dict:
        """
        Query data given a valid FRED series id and url. 
        Will raise an HTTPError if the response was an HTPP error.

        :param query: A url string of the requested data
        :param id: A FRED series id 
        :return: with id as key and requested DataFrame as value.
        """

        final_query = query.format(id)
        series_dict = {}
        try: 
            response = requests.get(final_query)
            response.raise_for_status() 
            json_data = response.json()
        except HTTPError as e:
            raise ValueError(response.json()["error_message"])
        if not len(json_data["observations"]):
            raise ValueError("No data exists for {} for the provided paramters... ".format(id))
        
        data = pd.DataFrame(json_data["observations"])[["date", "value"]]
        data['date'] = pd.to_datetime(data['date'])
        data = data.set_index('date')['value']
        data = data.sort_index().groupby('date').tail(1)
        series_dict[id] = data
        return series_dict

    def last_data(
        self,
        query: str, 
        id: str, 
        **kwargs
    ) -> dict:
        """
        Get the last point for a data series, at or before as_of

        :param query: A url string of the requested data
        :param id: A FRED series id 
        :param kwargs: Extra query arguments
        :return: with id as key and last point for this DataSet as value.
        """
        
        data = self.query_data(query, id)
        last_data_chunk = {}
        for id in data:
            last_data_chunk[id] = data[id].last("1D")
        return last_data_chunk

    def __fetch_data(self, url: str):
         """
         Helper function for fetching data given a request URL.
         Will raise an HTTPError if the response was an HTTP error.
         """
         url += '&api_key={}&file_type=json'.format(self.api_key)
         try:
             response = requests.get(url)
             response.raise_for_status() 
             data = json.loads(response.text)
         except HTTPError as e:
             raise ValueError(json.loads(response.text)["error_message"])
         return data

    def __get_search_results(self, url, limit, order_by=None, sort_order=None, filter=None):
        """
        helper function for getting search results up to specified limit on the number of results. The Fred HTTP API
        returns max of 1000 results per request, so this may issue multiple HTTP requests to obtain results until limit is reached.
        """
        order_by_options = ['search_rank', 'series_id', 'title', 'units', 'frequency',
                            'seasonal_adjustment', 'realtime_start', 'realtime_end', 'last_updated',
                            'observation_start', 'observation_end', 'popularity']
        if order_by is not None:
            if order_by in order_by_options:
                url = url + '&order_by=' + order_by
            else:
                raise ValueError('{} is not in the valid list of order_by options: {}'.format(order_by, str(order_by_options)))

        if filter is not None:
            if len(filter) == 2:
                url = url + '&filter_variable={}&filter_value={}'.format(filter[0], filter[1])
            else:
                raise ValueError('Filter should be a 2 item tuple like (filter_variable, filter_value)')

        sort_order_options = ['asc', 'desc']
        if sort_order is not None:
            if sort_order in sort_order_options:
                url = url + '&sort_order=' + sort_order
            else:
                raise ValueError('{} is not in the valid list of sort_order options: {}'.format(sort_order, str(sort_order_options)))
        
        # Get first chunk
        data = self.__fetch_data(url)
        data = pd.DataFrame(data["seriess"])
        if limit > 1000:
            for chunk in range(1, limit // 1000+1):
                # Fetch data
                next_data_chunk = self.__fetch_data(url + "&offset={}".format(data.shape[0]))
                next_data_chunk = pd.DataFrame(next_data_chunk["seriess"])
                data = data.append(next_data_chunk)
        return data.head(limit)

    def get_coverage(
        self,
        id: str = None,
        limit: int = None,
        offset: int = None,
        fields: List[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        """
        Get the series covered in the FRED dataset by matching text, release id, or category id. 

        :param id: The dataset id
        :param limit: The maximum number of results to return (value 0 returns all results)
        :param offset: The offset
        :param fields: The fields to return, e.g. assetId

        :Keyword Arguments:
            * *search_item* (``Union[str, int]``) --
                Text, category_id or release_id to search 
            * *search_critera* (``str``) --
                'text', 'release_id', or 'category_id'
        :param order_by: Order the results by a criterion ('search_rank', 'field', 'title', 'units', 'frequency',
            'seasonal_adjustment', 'realtime_start', 'realtime_end', 'last_updated', 'start', 'end',
            'popularity')
        :param filter: Filter the results by a criterion ('frequency', 'units', and 'seasonal_adjustment')
        :return: A DataFrame of the Fred series covered

        **Examples**

        >>> from gs_quant.api.fred import FredDataApi
        >>> 
        >>> API_KEY = <YOUR API KEY>
        >>> fredAPI = FredDataApi(api_key = API_KEY)
        >>> fred_data = Dataset("FRED", fredAPI)

        >>> fred_data.get_coverage(search_item="GDP", search_criteria="text")
        >>> fred_data.get_coverage(search_item=151, search_criteria="release_id")
        >>> fred_data.get_coverage(search_item=33058, search_criteria="category_id")
        """
        
        assert("search_criteria" in kwargs)
        assert("search_item" in kwargs)
        if limit is None:
            limit = 1000
        search_critera = kwargs["search_criteria"]
        search_item = kwargs["search_item"]

        if search_critera == 'text':
            url = "{}/series/search?search_text={}&limit=1000".format(self.root_url, requote_uri(search_item))
            coverage = self.__get_search_results(url=url, limit=limit)
            if coverage is None:
                raise ValueError('No series exists for text: ' + str(search_item))
        elif search_critera == 'release_id':
            url = "{}/release/series?release_id={}&limt=1000".format(self.root_url, search_item)
            coverage = self.__get_search_results(url=url, limit=limit)
            if coverage is None:
                raise ValueError('No series exists for release id: ' + str(search_item))
        elif search_critera == 'category_id':
            url = "{}/category/series?category_id={}&limit=1000".format(self.root_url, search_item)
            coverage = self.__get_search_results(url=url, limit=limit)
            if coverage is None:
                raise ValueError('No series exists for category id: ' + str(search_item))
        else:
            raise ValueError("Please specify search_critera as: 'text', 'release_id', or 'category'!")

        return coverage

    def construct_dataframe_with_types(
        self, 
        dataset_id: str, 
        data: dict
    ) -> pd.DataFrame:
        """
        Constructs a dataframe with correct date types.
        
        :param data: Data to convert with correct types
        :return: Dataframe with correct types
        """
        if len(data) > 0:
            idx = pd.date_range(dt.date(1776, 7, 4), dt.date(2262, 4, 11))
            df = None
            for series in data.values():
                if df is None:
                    df = series
                    df = df.reindex(idx)
                else:
                    df = pd.concat([df, series], axis=1)
            if isinstance(df, pd.Series):
                df = df.to_frame()
            df = df.dropna(thresh=1)
            df.columns = data.keys()
            df.index.name = 'date'
            return df
        else:
            return pd.DataFrame({})

    def symbol_dimensions(self, id:str) -> list:
        return [None]