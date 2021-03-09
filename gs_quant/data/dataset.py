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
from typing import Iterable, Optional, Union, List, Dict

import pandas as pd

from gs_quant.api.data import DataApi
from gs_quant.data.fields import Fields
from gs_quant.errors import MqValueError


class Dataset:
    """A collection of related data"""

    class Vendor(Enum):
        pass

    class GS(Vendor):
        HOLIDAY = 'HOLIDAY'
        EDRVOL_PERCENT_INTRADAY = 'EDRVOL_PERCENT_INTRADAY'
        EDRVOL_PERCENT_STANDARD = 'EDRVOL_PERCENT_STANDARD'
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

    class FRED(Vendor):
        GDP = 'GDP'

    def __init__(self, dataset_id: Union[str, Vendor], provider: DataApi = None):
        """

        :param dataset_id: The dataset's identifier
        :param provider: The data provider
        """
        self.__id = self._get_dataset_id_str(dataset_id)
        self.__provider = provider

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
        """

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

        return self.provider.construct_dataframe_with_types(self.id, data)

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
        """

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
        df = self.provider.construct_dataframe_with_types(self.id, data)

        from gs_quant.api.gs.data import GsDataApi

        if isinstance(self.provider, GsDataApi):
            gb = df.groupby(symbol_dimension)
            if len(gb.groups) > 1:
                raise MqValueError('Not a series for a single {}'.format(symbol_dimension))

        if df.empty:
            return pd.Series()
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
        """
        query = self.provider.build_query(
            start=start,
            end=as_of,
            fields=fields,
            format='JSON',
            **kwargs
        )
        query.format = None  # "last" endpoint does not support MessagePack

        data = self.provider.last_data(query, self.id)
        return self.provider.construct_dataframe_with_types(self.id, data)

    def get_coverage(
            self,
            limit: int = None,
            offset: int = None,
            fields: List[str] = None,
            include_history: bool = False,
            **kwargs
    ) -> pd.DataFrame:
        """
        Get the assets covered by this DataSet

        :param limit: The maximum number of assets to return
        :param offset: The offset
        :param fields: The fields to return, e.g. assetId
        :param include_history: Return column for historyStartDate
        :return: A Dataframe of the assets covered

        **Examples**

        >>> from gs_quant.data import Dataset
        >>>
        >>> weather = Dataset('WEATHER')
        >>> cities = weather.get_coverage()
        """
        coverage = self.provider.get_coverage(
            self.id,
            limit=limit,
            offset=offset,
            fields=fields,
            include_history=include_history,
            **kwargs
        )

        return pd.DataFrame(coverage)

    def upload_data(self, data: Union[pd.DataFrame, list, tuple]) -> Dict:
        """
        Upload data to this DataSet

        :param data: data to be uploaded to the dataset

        **Examples**

        >>> from gs_quant.data import Dataset
        >>>
        >>> weather = Dataset('WEATHER')
        >>> data = [{
        >>>    "date": "2016-12-31",
        >>>    "city": "Chicago",
        >>>    "maxTemperature": 40.0,
        >>>    "minTemperature": 23.0,
        >>>    "dewPoint": 21.0,
        >>>    "windSpeed": 11.4,
        >>>    "precipitation": 0.0,
        >>>    "snowfall": 0.0,
        >>>    "pressure": 29.03,
        >>>    "updateTime": "2017-03-06T16:49:39.493Z"
        >>> }]
        >>> upload_response = weather.upload_data(data)
        """
        return self.provider.upload_data(self.id, data)
