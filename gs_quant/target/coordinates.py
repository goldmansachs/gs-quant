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

from gs_quant.common import *
import datetime
from typing import Mapping, Tuple, Union, Optional
from enum import Enum
from gs_quant.base import Base, EnumBase, InstrumentBase, camel_case_translate, get_enum_value


class MDAPIQueryField(EnumBase, Enum):    
    
    ask = 'ask'
    bid = 'bid'
    mid = 'mid'
    expectedDataQuality = 'expectedDataQuality'
    actualDataQuality = 'actualDataQuality'    


class MDAPIDataQuery(Base):
        
    @camel_case_translate
    def __init__(
        self,
        market_data_coordinates: Tuple[MarketDataCoordinate, ...],
        format_: Union[Format, str] = None,
        pricing_location: Union[PricingLocation, str] = None,
        selector_function: str = None,
        samples: int = None,
        interval: str = None,
        vendor: Union[MarketDataVendor, str] = None,
        start_time: datetime.datetime = None,
        end_time: datetime.datetime = None,
        start_date: datetime.date = None,
        end_date: datetime.date = None,
        real_time: bool = True,
        fields: Tuple[Union[MDAPIQueryField, str], ...] = None,
        time_filter: TimeFilter = None,
        name: str = None
    ):        
        super().__init__()
        self.__format = get_enum_value(Format, format_)
        self.market_data_coordinates = market_data_coordinates
        self.pricing_location = pricing_location
        self.selector_function = selector_function
        self.samples = samples
        self.interval = interval
        self.vendor = vendor
        self.start_time = start_time
        self.end_time = end_time
        self.start_date = start_date
        self.end_date = end_date
        self.real_time = real_time
        self.fields = fields
        self.time_filter = time_filter
        self.name = name

    @property
    def format(self) -> Union[Format, str]:
        """Alternative format for data to be returned in"""
        return self.__format

    @format.setter
    def format(self, value: Union[Format, str]):
        self._property_changed('format')
        self.__format = get_enum_value(Format, value)        

    @property
    def market_data_coordinates(self) -> Tuple[MarketDataCoordinate, ...]:
        """Object representation of a market data coordinate"""
        return self.__market_data_coordinates

    @market_data_coordinates.setter
    def market_data_coordinates(self, value: Tuple[MarketDataCoordinate, ...]):
        self._property_changed('market_data_coordinates')
        self.__market_data_coordinates = value        

    @property
    def pricing_location(self) -> Union[PricingLocation, str]:
        """Pricing location of end-of-day data (not used for real-time query)."""
        return self.__pricing_location

    @pricing_location.setter
    def pricing_location(self, value: Union[PricingLocation, str]):
        self._property_changed('pricing_location')
        self.__pricing_location = get_enum_value(PricingLocation, value)        

    @property
    def selector_function(self) -> str:
        """Aggregation function to be applied to value fields"""
        return self.__selector_function

    @selector_function.setter
    def selector_function(self, value: str):
        self._property_changed('selector_function')
        self.__selector_function = value        

    @property
    def samples(self) -> int:
        """Number of points to down sample the data, for example if 10, it will return at
           most 10 sample data points evenly spaced over the time/date range"""
        return self.__samples

    @samples.setter
    def samples(self, value: int):
        self._property_changed('samples')
        self.__samples = value        

    @property
    def interval(self) -> str:
        """Interval to use when returning data. E.g. 1s, 1m, 1h, 1d. Only seconds(s),
           minutes(m), hours(h) and days(d) are supported."""
        return self.__interval

    @interval.setter
    def interval(self, value: str):
        self._property_changed('interval')
        self.__interval = value        

    @property
    def vendor(self) -> Union[MarketDataVendor, str]:
        return self.__vendor

    @vendor.setter
    def vendor(self, value: Union[MarketDataVendor, str]):
        self._property_changed('vendor')
        self.__vendor = get_enum_value(MarketDataVendor, value)        

    @property
    def start_time(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__start_time

    @start_time.setter
    def start_time(self, value: datetime.datetime):
        self._property_changed('start_time')
        self.__start_time = value        

    @property
    def end_time(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__end_time

    @end_time.setter
    def end_time(self, value: datetime.datetime):
        self._property_changed('end_time')
        self.__end_time = value        

    @property
    def start_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__start_date

    @start_date.setter
    def start_date(self, value: datetime.date):
        self._property_changed('start_date')
        self.__start_date = value        

    @property
    def end_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__end_date

    @end_date.setter
    def end_date(self, value: datetime.date):
        self._property_changed('end_date')
        self.__end_date = value        

    @property
    def real_time(self) -> bool:
        """Intraday or end of day data"""
        return self.__real_time

    @real_time.setter
    def real_time(self, value: bool):
        self._property_changed('real_time')
        self.__real_time = value        

    @property
    def fields(self) -> Tuple[Union[MDAPIQueryField, str], ...]:
        """Value Fields to be returned"""
        return self.__fields

    @fields.setter
    def fields(self, value: Tuple[Union[MDAPIQueryField, str], ...]):
        self._property_changed('fields')
        self.__fields = value        

    @property
    def time_filter(self) -> TimeFilter:
        """Filter to restrict data to a range of hours per day."""
        return self.__time_filter

    @time_filter.setter
    def time_filter(self, value: TimeFilter):
        self._property_changed('time_filter')
        self.__time_filter = value        


class MDAPIDataQueryResponse(Base):
        
    @camel_case_translate
    def __init__(
        self,
        data: Tuple[FieldValueMap, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.data = data
        self.name = name

    @property
    def data(self) -> Tuple[FieldValueMap, ...]:
        """Array of data elements from dataset"""
        return self.__data

    @data.setter
    def data(self, value: Tuple[FieldValueMap, ...]):
        self._property_changed('data')
        self.__data = value        


class MDAPIDataBatchResponse(Base):
        
    @camel_case_translate
    def __init__(
        self,
        request_id: str = None,
        responses: Tuple[MDAPIDataQueryResponse, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.request_id = request_id
        self.responses = responses
        self.name = name

    @property
    def request_id(self) -> str:
        """Marquee unique identifier"""
        return self.__request_id

    @request_id.setter
    def request_id(self, value: str):
        self._property_changed('request_id')
        self.__request_id = value        

    @property
    def responses(self) -> Tuple[MDAPIDataQueryResponse, ...]:
        """MDAPI Data query responses"""
        return self.__responses

    @responses.setter
    def responses(self, value: Tuple[MDAPIDataQueryResponse, ...]):
        self._property_changed('responses')
        self.__responses = value        
