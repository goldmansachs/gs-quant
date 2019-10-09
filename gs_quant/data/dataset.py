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


import datetime as dt
from enum import Enum
from typing import Iterable, Optional, Union, List

import pandas as pd
import fredapi

from gs_quant.api.data import DataApi
from gs_quant.data.fields import Fields
from gs_quant.data.utils import construct_dataframe_with_types
from gs_quant.errors import MqValueError


class Dataset:
    """A collection of related data"""

    class Vendor(Enum):
        pass

    class GS(Vendor):
        HOLIDAY = 'HOLIDAY'
        EDRVOL_PERCENT_INTRADAY = 'EDRVOL_PERCENT_INTRADAY'
        EDRVOL_PERCENT_SHORT = 'EDRVOL_PERCENT_SHORT'
        EDRVOL_PERCENT_LONG = 'EDRVOL_PERCENT_LONG'
        MA_RANK = 'MA_RANK'
        EDRVS_INDEX_SHORT = 'EDRVS_INDEX_SHORT'
        EDRVS_INDEX_LONG = 'EDRVS_INDEX_LONG'

        # Baskets
        CBGSSI = 'CBGSSI'
        CB = 'CB'

        # STS
        STSLEVELS = 'STSLEVELS'

        # Test Datasets
        WEATHER = 'WEATHER'

    class TR(Vendor):
        TREOD = 'TREOD'
        TR = 'TR'
        TR_FXSPOT = 'TR_FXSPOT'

    def __init__(self, dataset_id: Union[str, Vendor], provider: DataApi = None, api_key: Optional[str] = None):
        """

        :param dataset_id: The dataset's identifier
        :param provider: The data provider
        :param api_key: The data provider's API Key
        """
        self.__id = self._get_dataset_id_str(dataset_id)
        self.__provider = provider
        self._api_key = api_key

    def _get_dataset_id_str(self, dataset_id):
        return dataset_id.value if isinstance(dataset_id, Dataset.Vendor) else dataset_id

    @property
    def id(self) -> str:
        """
        The dataset's identifier
        """
        return self.__id

    @property
    def name(self):
        pass

    @property
    def provider(self):
        from gs_quant.api.gs.data import GsDataApi
        return self.__provider or GsDataApi

    @property
    def api_key(self) -> str:
        return self._api_key

    def get_data(
            self,
            start: Optional[Union[dt.date, dt.datetime]] = None,
            end: Optional[Union[dt.date, dt.datetime]] = None,
            as_of: Optional[dt.datetime] = None,
            since: Optional[dt.datetime] = None,
            fields: Optional[Iterable[Union[str, Fields]]] = None,
            asset_id_type: str = None,
            **kwargs
    ) -> pd.DataFrame:
        """
        Get data for the given range and parameters

        :param start: Requested start date/datetime for data
        :param end: Requested end date/datetime for data
        :param as_of: Request data as_of
        :param since: Request data since
        :param fields: DataSet fields to include
        :param kwargs: Extra query arguments, e.g. ticker='EDZ19'
        :return: A Dataframe of the requested data

        **Examples**

        >>> from gs_quant.data import Dataset
        >>> import datetime as dt
        >>>
        >>> weather = Dataset('WEATHER')
        >>> weather_data = weather.get_data(dt.date(2016, 1, 15), dt.date(2016, 1, 16), city=('Boston', 'Austin'))

        Retrieve a time series from the FRED dataset:

        >>> from gs_quant.data import Dataset
        >>> import datetime as dt
        >>>
        >>> fred = Dataset('FRED', api_key=<your api>)
        >>> gdp_data = fred.get_data(field="GDP", observation_start=dt.date(2016, 1, 15), observation_end=dt.date(2016, 1, 16))

        """
        if self.id == "FRED":
            series_id = kwargs["field"]
            
            data_series = self.get_data_series(**kwargs)
            data = data_series.to_frame().reset_index()
            data.columns = ["date", series_id]
            data.set_index('date', inplace=True)
            return data
        else:
            field_names = None if fields is None else list(map(lambda f: f if isinstance(f, str) else f.value, fields))

            query = self.provider.build_query(
                start=start,
                end=end,
                as_of=as_of,
                since=since,
                fields=field_names,
                **kwargs
            )
            data = self.provider.query_data(query, self.id, asset_id_type=asset_id_type)

            return construct_dataframe_with_types(self.id, data)

    def get_data_series(
            self,
            field: Union[str, Fields],
            start: Optional[Union[dt.date, dt.datetime]] = None,
            end: Optional[Union[dt.date, dt.datetime]] = None,
            as_of: Optional[dt.datetime] = None,
            since: Optional[dt.datetime] = None,
            **kwargs
    ) -> pd.Series:
        """
        Get a time series of data for a field of a dataset

        :param field: The DataSet field to use
        :param start: Requested start date/datetime for data
        :param end: Requested end date/datetime for data
        :param as_of: Request data as_of
        :param since: Request data since
        :param kwargs: Extra query arguments, e.g. ticker='EDZ19'
        :return: A Series of the requested data, indexed by date or time, depending on the DataSet

        **Examples**

        >>> from gs_quant.data import Dataset
        >>> import datetime as dt
        >>>
        >>> weather = Dataset('WEATHER')
        >>> dew_point = weather
        >>>>    .get_data_series('dewPoint', dt.date(2016, 1, 15), dt.date(2016, 1, 16), city=('Boston', 'Austin'))

        Retrieve a time series from the FRED dataset.

        >>> from gs_quant.data import Dataset
        >>> import datetime as dt
        >>>
        >>> fred = Dataset('FRED', api_key=<your api>)
        >>> gdp_data = fred.get_data_series(field="GDP", observation_start=dt.date(2016, 1, 15), observation_end=dt.date(2016, 1, 16))
        """

        if self.id == "FRED":
            fred = fredapi.Fred(api_key=self.api_key)
            data_series = fred.get_series(series_id=field, **kwargs)
            return data_series
        else:
            field_value = field if isinstance(field, str) else field.value

            query = self.provider.build_query(
                start=start,
                end=end,
                as_of=as_of,
                since=since,
                fields=(field_value,),
                **kwargs
            )

            symbol_dimensions = self.provider.symbol_dimensions(self.id)
            if len(symbol_dimensions) != 1:
                raise MqValueError('get_data_series only valid for symbol_dimensions of length 1')

            symbol_dimension = symbol_dimensions[0]
            data = self.provider.query_data(query, self.id)
            df = construct_dataframe_with_types(self.id, data)

            gb = df.groupby(symbol_dimension)
            if len(gb.groups) > 1:
                raise MqValueError('Not a series for a single {}'.format(symbol_dimension))

            return pd.Series(index=df.index, data=df.loc[:, field_value].values)

    def get_data_last(
            self,
            as_of: Optional[Union[dt.date, dt.datetime]],
            start: Optional[Union[dt.date, dt.datetime]] = None,
            fields: Optional[Iterable[str]] = None,
            **kwargs
    ) -> pd.DataFrame:
        """
        Get the last point for this DataSet, at or before as_of

        :param as_of: The date or time as of which to query
        :param start: The start of the range to query
        :param fields: The fields for which to query
        :param kwargs: Additional query parameters, e.g., city='Boston'
        :return: A Dataframe of values

        **Examples**

        >>> from gs_quant.data import Dataset
        >>> import datetime as dt
        >>>
        >>> weather = Dataset('WEATHER')
        >>> last = weather.get_data_last(dt.datetime.now())

        Retrieve latest data point for a Fred time series as known on a particular date:
        
        >>> from gs_quant.data import Dataset
        >>> import datetime as dt
        >>>
        >>> fred = Dataset('FRED', api_key=<your api>)
        >>> gdp_data = fred.get_data_last(field="GDP", as_of=dt.date(2016, 1, 1))
        """
        if self.id == "FRED":
            series_id = kwargs["field"]
            fred = fredapi.Fred(api_key=self.api_key)
            data = fred.get_series_as_of_date(series_id=series_id, as_of_date=as_of)[-1:]
            data.set_index('date', inplace=True)
            data = data.rename(columns={"value": series_id})
            return data
        else:
            query = self.provider.build_query(
                start=start,
                end=as_of,
                fields=fields,
                **kwargs
            )

            data = self.provider.last_data(query, self.id)
            return construct_dataframe_with_types(self.id, data)

    def get_coverage(
            self,
            limit: int = None,
            offset: int = None,
            fields: List[str] = None,
            **kwargs
    ) -> pd.DataFrame:
        """
        Get the assets covered by this DataSet

        :param limit: The maximum number of assets to return
        :param offset: The offset
        :param fields: The fields to return, e.g. assetId
        :return: A Dataframe of the assets covered

        **Examples**

        >>> from gs_quant.data import Dataset
        >>>
        >>> weather = Dataset('WEATHER')
        >>> cities = weather.get_coverage()

        Retrieve coverage from FRED using category_id:

        >>> from gs_quant.data import Dataset
        >>> import datetime as dt
        >>>
        >>> fred = Dataset('FRED', api_key=<your api key>)
        >>> fred.get_coverage(text="US")

        Retrieve coverage from FRED using category_id:

        >>> from gs_quant.data import Dataset
        >>> import datetime as dt
        >>>
        >>> fred = Dataset('FRED', api_key=<your api key>)
        >>> fred.get_coverage(category_id=32145)

        Retrieve coverage from FRED using release_id:

        >>> from gs_quant.data import Dataset
        >>> import datetime as dt
        >>>
        >>> fred = Dataset('FRED', api_key=<your api key>)
        >>> fred.get_coverage(release_id=151)

        """
        if self.id == "FRED":
            fred = fredapi.Fred(api_key=self.api_key)

            limit = kwargs.get("limit", 1000)
            order_by = kwargs.get("order_by", None)
            sort_order = kwargs.get("sort_order", None)
            filter = kwargs.get("filter", None)

            if "category_id" in kwargs.keys():
                coverage = fred.search_by_category(
                    kwargs["category_id"], limit=limit, 
                    order_by=order_by, 
                    sort_order=sort_order, 
                    filter=filter
                )
            elif "release_id" in kwargs.keys():
                coverage = fred.search_by_release(
                    kwargs["release_id"], limit=limit, 
                    order_by=order_by, 
                    sort_order=sort_order, 
                    filter=filter
                )
            elif "text" in kwargs.keys():
                coverage = fred.search(
                    kwargs["text"], limit=limit, 
                    order_by=order_by, 
                    sort_order=sort_order, 
                    filter=filter
                )
            else:
                raise ValueError("Please enter valid critera: category_id, release_id, or text")
            return coverage
        else:
            coverage = self.provider.get_coverage(
                self.id,
                limit=limit,
                offset=offset,
                fields=fields
            )

            return pd.DataFrame(coverage)
