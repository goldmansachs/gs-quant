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
import re
import webbrowser
from enum import Enum
from typing import Iterable, Optional, Union, List, Dict
from urllib.parse import quote

import inflection
import numpy as np
import pandas as pd

from gs_quant.api.data import DataApi
from gs_quant.data.fields import Fields
from gs_quant.errors import MqValueError
from gs_quant.session import GsSession


class Dataset:
    """A collection of related data"""

    class Vendor(Enum):
        pass

    class GS(Vendor):
        HOLIDAY = 'HOLIDAY'
        HOLIDAY_CURRENCY = 'HOLIDAY_CURRENCY'
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

        # Central Bank Watch
        CENTRAL_BANK_WATCH = 'CENTRAL_BANK_WATCH_PREMIUM'
        IR_SWAP_RATES_INTRADAY_CALC_BANK = 'IR_SWAP_RATES_INTRADAY_CALC_BANK'
        RETAIL_FLOW_DAILY_V2_PREMIUM = 'RETAIL_FLOW_DAILY_V2_PREMIUM'
        FX_EVENTS_JUMPS = 'FX_EVENTS_JUMPS'
        FXSPOT_INTRADAY2 = 'FXSPOT_INTRADAY2'
        # Test Datasets
        WEATHER = 'WEATHER'

        # TCA
        QES_INTRADAY_COVARIANCE = 'QES_INTRADAY_COVARIANCE_PREMIUM'

    class TR(Vendor):
        TREOD = 'TREOD'
        TR = 'TR'
        TR_FXSPOT = 'TR_FXSPOT'

    class FRED(Vendor):
        GDP = 'GDP'

    class TradingEconomics(Vendor):
        MACRO_EVENTS_CALENDAR = 'MACRO_EVENTS_CALENDAR'

    def __init__(self, dataset_id: Union[str, Vendor], provider: Optional[DataApi] = None):
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
            asset_id_type: Optional[str] = None,
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
            dates: Optional[List[dt.date]] = None,
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
            dates=dates,
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
            return pd.Series(dtype=float)
        if '(' in field_value:
            field_value = field_value.replace('(', '_')
            field_value = field_value.replace(')', '')
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
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            fields: Optional[List[str]] = None,
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

    def delete(self) -> Dict:
        """
        Delete dataset definition.

        Needs 'modify_profuct_data' to execute operation.

        >>> from gs_quant.data import Dataset
        >>>
        >>> test_dataset = Dataset('TEST')
        >>> test_dataset.delete()
        """
        return self.provider.delete_dataset(self.id)

    def undelete(self) -> Dict:
        """
        Un-delete dataset definition.

        Needs 'modify_profuct_data' to execute operation.

        >>> from gs_quant.data import Dataset
        >>>
        >>> test_dataset = Dataset('TEST')
        >>> test_dataset.undelete()
        """
        return self.provider.undelete_dataset(self.id)

    def delete_data(self, delete_query: Dict):
        """
        Delete data from dataset. You must have admin access to the dataset to delete data.
        All data deleted is not recoverable.

        :param delete_query: Query to specify data to be deleted.

        >>> from gs_quant.data import Dataset
        >>>
        >>> test_dataset = Dataset('TEST')
        >>> delete_query = {'startDate': dt.date.today(), 'endDate': dt.date.today(), 'deleteAll': True}
        >>> test_dataset.delete_data(delete_query)
        """
        return self.provider.delete_data(self.id, delete_query)

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


class PTPDataset(Dataset):
    """
    Special class for and viewing PTP-style datasets.

    PTP provides a wrapper around the data service that makes it easy to define datasets, upload data, and plot them in
    PlotTool Pro. PTP datasets can only contain numeric data with a pd.DatetimeIndex (will throw an error otherwise).
    Currently, we only support EOD data; realtime data is not allowed.

    (Technically, PTP datasets are datasets with one symbol dimension, which is the dataset ID. Tags indicate that they
    are PTP-style datasets and can be viewed in the 'Datasets' tab in PTP).

    :param series: pd.DataFrame or pd.Series with a pd.DatetimeIndex containing EOD numeric data.
    :param name: Name of dataset (default "GSQ Default")

    **Example**

    >>> from gs_quant.data import PTPDataset
    >>> import datetime
    >>> a = pd.Series(range(50), index=pd.date_range(start=datetime.date(2021, 1, 1), periods=50, freq='D'))
    >>> dataset = PTPDataset(a, 'My Dataset')
    >>> dataset.sync()
    >>> print(dataset.plot())
    >>> dataset.delete()
    """

    def __init__(self, series: Union[pd.Series, pd.DataFrame], name: Optional[str] = None):
        if isinstance(series, pd.Series):
            series = pd.DataFrame({series.attrs.get('name', 'values'): series})
        if not isinstance(series.index, pd.DatetimeIndex):
            raise MqValueError('PTP datasets require a Pandas object with a DatetimeIndex.')
        if isinstance(series, pd.DataFrame) and \
                len(series.select_dtypes(include=np.number).columns) != len(series.columns):
            raise MqValueError('PTP datasets must contain only numbers.')

        self._series = series
        self._name = name
        super(PTPDataset, self).__init__('', None)

    def sync(self):
        """
        Upload data and save dataset.
        """
        temp_ser = self._series.assign(date=self._series.index.to_series().apply(dt.date.isoformat))
        data = temp_ser.to_dict('records')
        kwargs = dict(data=data, name=self._name if self._name else 'GSQ Default',
                      fields=list(self._series.columns))
        res = GsSession.current._post('/plots/datasets', payload=kwargs)
        self._fields = {key: inflection.underscore(field) for key, field in res['fieldMap'].items() if field not in
                        ['updateTime', 'date', 'datasetId']}
        self._id = res['dataset']['id']
        super(PTPDataset, self).__init__(self._id, None)

    def plot(self, open_in_browser: bool = True, field: Optional[str] = None) -> str:
        """
        Generate transient plot expression to view dataset in PTP. Copying and pasting the transient expression
        will show your data in PTP.

        :param open_in_browser: whether to use webbrowser to open the generated plot expression in your default browser
            (default True)
        :param field: if passed, only this field will be included in the transient plot (default None)
        :return: transient plot expression.
        """
        if not field:
            fields = self._fields.values()
        else:
            fields = [field]
        fields = [inflection.underscore(re.sub(r'([a-zA-Z])(\d)', r'\1_\2', f)) for f in fields]
        domain = GsSession.current.domain.replace('marquee.web', 'marquee')  # remove .web from prod domain
        expression = f'{domain}/s/plottool/transient?expr=Dataset("{self._id}").{fields[0]}()'
        for f in fields[1:]:
            expression += quote("\n") + f'Dataset("{self._id}").{f}()'
        if open_in_browser:
            webbrowser.open(expression)
        return expression
