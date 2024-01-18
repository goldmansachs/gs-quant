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
from typing import Iterable, Optional, Union, List, Dict, Callable
from urllib.parse import quote

import inflection
import numpy as np
import pandas as pd

from gs_quant.api.data import DataApi
from gs_quant.data.fields import Fields
from gs_quant.errors import MqValueError
from gs_quant.session import GsSession
from functools import partial
from gs_quant.data.utilities import Utilities


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
        FXFORWARDPOINTS_PREMIUM = 'FXFORWARDPOINTS_PREMIUM'
        FXFORWARDPOINTS_INTRADAY = 'FXFORWARDPOINTS_INTRADAY'
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
            empty_intervals: Optional[bool] = None,
            standard_fields: Optional[bool] = False,
            **kwargs
    ) -> pd.DataFrame:
        """
        Get data for the given range and parameters

        :param start: Requested start date/datetime for data
        :param end: Requested end date/datetime for data
        :param as_of: Request data as_of
        :param since: Request data since
        :param fields: DataSet fields to include
        :param empty_intervals: whether to request empty intervals
        :param standard_fields: If set, will use fields api instead of catalog api to get fieldTypes
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
        # check whether a function is called e.g. difference(tradePrice)
        schema_varies = field_names is not None and any(map(lambda s: re.match("\\w+\\(", s), field_names))
        if kwargs and "date" in kwargs:
            d = kwargs["date"]
            if type(d) is str:
                try:
                    kwargs["date"] = dt.datetime.strptime(d, "%Y-%m-%d").date()
                except ValueError:
                    pass  # Ignore error if date parameter is in some other format
            if "dates" not in kwargs and start is None and end is None:
                kwargs["dates"] = (kwargs["date"],)
        query = self.provider.build_query(
            start=start,
            end=end,
            as_of=as_of,
            since=since,
            fields=field_names,
            empty_intervals=empty_intervals,
            **kwargs
        )
        data = self.provider.query_data(query, self.id, asset_id_type=asset_id_type)
        if type(data) is tuple:
            df = self.provider.construct_dataframe_with_types(self.id, data[0], schema_varies,
                                                              standard_fields=standard_fields)
            return df.groupby(data[1], group_keys=True).apply(lambda x: x)
        else:
            return self.provider.construct_dataframe_with_types(self.id, data, schema_varies,
                                                                standard_fields=standard_fields)

    def get_data_series(
            self,
            field: Union[str, Fields],
            start: Optional[Union[dt.date, dt.datetime]] = None,
            end: Optional[Union[dt.date, dt.datetime]] = None,
            as_of: Optional[dt.datetime] = None,
            since: Optional[dt.datetime] = None,
            dates: Optional[List[dt.date]] = None,
            standard_fields: Optional[bool] = False,
            **kwargs
    ) -> pd.Series:
        """
        Get a time series of data for a field of a dataset

        :param field: The DataSet field to use
        :param start: Requested start date/datetime for data
        :param end: Requested end date/datetime for data
        :param as_of: Request data as_of
        :param since: Request data since
        :param standard_fields: If set, will use fields api instead of catalog api to get fieldTypes
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
        df = self.provider.construct_dataframe_with_types(self.id, data, standard_fields=standard_fields)

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
            standard_fields: Optional[bool] = False,
            **kwargs
    ) -> pd.DataFrame:
        """
        Get the last point for this DataSet, at or before as_of

        :param as_of: The date or time as of which to query
        :param start: The start of the range to query
        :param fields: The fields for which to query
        :param standard_fields: If set, will use fields api instead of catalog api to get fieldTypes
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
        return self.provider.construct_dataframe_with_types(self.id, data, standard_fields=standard_fields)

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

    async def get_coverage_async(
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
        >>> cities = await weather.get_coverage_async()
        """
        coverage = await self.provider.get_coverage_async(
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

    def get_data_bulk(self,
                      request_batch_size,
                      original_start: dt.datetime,
                      final_end: Optional[dt.datetime] = None,
                      identifier="bbid",
                      symbols_per_csv: int = 1000,
                      datetime_delta_override: Optional[int] = None,
                      handler: Optional[Callable[[pd.DataFrame], None]] = None
                      ):
        """
        Extracts data from dataset by running parallel queries in the background

        :param request_batch_size: Used to group number of symbols per batch run (> 0 and <5)
        :param original_start: Start date to fetch the data (mandatory)
        :param final_end: End date to fetch the data. If not entered defaults to current datetime
        :param identifier: Use specific identifier as per dataset configuration. ex. cusip, bbid, clusterRegion
        :param symbols_per_csv: Number of symbols per CSV (recommended value = 1000)
        :param datetime_delta_override: A numeric parameter to increment start date and fetch data in batches
            units are days for daily datasets and hours for intraday
        :param handler: A callable function, if provided, to handle dataframe instead of writing to CSV


        **Examples**

        >>> import datetime as dt
        >>> from gs_quant.data import Dataset
        >>> dataset_id = "EQTRADECLUSTERS"
        >>> original_start = dt.datetime(2023, 3, 1,0,0,0)
        >>> final_end = dt.datetime(2023, 3, 1,0,0,0)
        >>> c = Dataset(dataset_id)
        >>> c.get_data_bulk(original_start=original_start,
        >>>                 final_end=final_end,
        >>>                 datetime_delta_override=1,
        >>>                 request_batch_size=4,
        >>>                 identifier="clusterRegion")
        """

        try:
            authenticate = partial(GsSession.use,
                                   client_id=GsSession.current.client_id,
                                   client_secret=GsSession.current.client_secret
                                   )
        except AttributeError:
            authenticate = partial(GsSession.use)

        time_field, history_time, symbol_dimension, timedelta = Utilities.get_dataset_parameter(self)
        final_end = final_end or dt.datetime.now()
        write_to_csv = handler is None
        final_end, target_dir_result = Utilities.pre_checks(final_end, original_start, time_field,
                                                            datetime_delta_override, request_batch_size, write_to_csv)
        if write_to_csv:
            print("Target Destination Folder: ", target_dir_result)

        if time_field == 'date':
            original_start = max(original_start.date(), history_time.date())
            final_end = max(final_end.date(), history_time.date())
            datetime_delta_override = timedelta if datetime_delta_override is None else dt.timedelta(
                days=datetime_delta_override)
        elif time_field == 'time':
            original_start = max(original_start.astimezone(dt.timezone.utc), history_time.astimezone(dt.timezone.utc))
            final_end = max(final_end.astimezone(dt.timezone.utc), history_time.astimezone(dt.timezone.utc))
            datetime_delta_override = timedelta if datetime_delta_override is None else dt.timedelta(
                hours=datetime_delta_override)

        original_end = min(original_start + datetime_delta_override, final_end)
        coverage = Utilities.get_dataset_coverage(identifier, symbol_dimension, self)
        coverage_batches = Utilities.batch(coverage, n=symbols_per_csv)
        batch_number = 1
        coverage_length = len(coverage)

        for coverage_batch in coverage_batches:
            Utilities.iterate_over_series(
                self,
                coverage_batch,
                original_start,
                original_end,
                datetime_delta_override,
                identifier,
                request_batch_size,
                authenticate,
                final_end,
                write_to_csv,
                target_dir_result,
                batch_number,
                coverage_length,
                symbols_per_csv,
                handler
            )

            batch_number += 1


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
