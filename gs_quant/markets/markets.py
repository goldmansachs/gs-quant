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
import pytz
import re
from typing import Mapping, Optional, Tuple, Union

from gs_quant.base import Market, RiskKey
from gs_quant.common import PricingLocation
from gs_quant.datetime.date import prev_business_date
from gs_quant.target.common import CloseMarket as _CloseMarket, LiveMarket as _LiveMarket, \
    OverlayMarket as _OverlayMarket, RelativeMarket as _RelativeMarket, TimestampedMarket as _TimestampedMarket, \
    RefMarket as _RefMarket
from gs_quant.target.data import MarketDataCoordinate as __MarketDataCoordinate, \
    MarketDataCoordinateValue as __MarketDataCoordinateValue

location_to_tz_mapping = {PricingLocation.NYC: pytz.timezone("America/New_York"),
                          PricingLocation.LDN: pytz.timezone("Europe/London"),
                          PricingLocation.HKG: pytz.timezone("Asia/Hong_Kong"),
                          PricingLocation.TKO: pytz.timezone("Asia/Tokyo")}


def historical_risk_key(risk_key: RiskKey) -> RiskKey:
    market = LocationOnlyMarket(risk_key.market.location)
    return RiskKey(risk_key.provider, None, market, risk_key.params, risk_key.scenario, risk_key.risk_measure)


def market_location(location: Optional[PricingLocation] = None) -> PricingLocation:
    """Determine PricingLocation and ensure passed optional 'location' does not
    conflict with the current PricingContext's market_data_location

    :param location: optional PricingLocation
    :return: PricingLocation
    """
    from .core import PricingContext
    default = PricingContext.current.market_data_location

    if location is None:
        return default or PricingLocation.LDN
    else:
        return location


def close_market_date(location: Optional[Union[PricingLocation, str]] = None, date: Optional[dt.date] = None,
                      roll_hr_and_min: Tuple[int, int] = (24, 0)) -> dt.date:
    """Determine market data date based on current location (to infer calendar)
    and current pricing date

    :param location: date location, used for the roll timezone
    :param date: pricing date
    :param roll_hr_and_min: tuple of the hour and minute of the expected market data availability time
    in the location timezone
    :return: close market date
    """
    from .core import PricingContext
    date = date or PricingContext.current.pricing_date

    location_tz = location_to_tz_mapping[PricingLocation(location)]
    now_time = dt.datetime.now().astimezone(location_tz).replace(tzinfo=None)
    hr_offset = roll_hr_and_min[0]
    min_offset = roll_hr_and_min[1]
    roll_time = dt.datetime(date.year, date.month, date.day).replace(tzinfo=None) + \
        dt.timedelta(hours=hr_offset, minutes=min_offset)
    if now_time < roll_time:
        # Don't use the calendars argument here as external users do not (yet) have access to that dataset
        date = prev_business_date(date)

    return date


class MarketDataCoordinate(__MarketDataCoordinate):

    def __repr__(self):
        ret = "_".join(f or '' for f in (self.mkt_type, self.mkt_asset, self.mkt_class))

        if self.mkt_point:
            ret += '_' + ','.join(self.mkt_point)

        if self.mkt_quoting_style:
            ret += f'.{self.mkt_quoting_style}'

        return ret

    @classmethod
    def from_string(cls, value: str):
        from gs_quant.api.gs.data import GsDataApi
        ret = GsDataApi._coordinate_from_str(value)
        if len(ret.mkt_point) == 1:
            # Unfortunately _,; have all been used as delimiters in various places
            ret.mkt_point = tuple(re.split('[,_;]', ret.mkt_point[0]))

        return ret


class MarketDataCoordinateValue(__MarketDataCoordinateValue):

    def __repr__(self):
        return f'{self.coordinate} --> {self.value}'


Coordinates = Tuple[MarketDataCoordinate, ...]
MarketDataMap = Mapping[MarketDataCoordinate, float]


class LocationOnlyMarket(Market):

    def __init__(self, location: Optional[Union[str, PricingLocation]]):
        self.__location = location if isinstance(location, PricingLocation) or location is None else \
            PricingLocation(location)

    @property
    def market(self):
        return None

    @property
    def location(self) -> PricingLocation:
        return self.__location


class CloseMarket(Market):
    """Market Object which captures market data based on market_location
    and close_market_date
    """
    __date_cache = {}
    roll_hr_and_min = (24, 0)  # tuple of today's expected hr/min of market data availability in the location tz

    def __init__(self,
                 date: Optional[dt.date] = None,
                 location: Optional[Union[str, PricingLocation]] = None,
                 check: Optional[bool] = True):
        self.__date = date
        self.__location = location if isinstance(location, PricingLocation) or location is None else \
            PricingLocation(location)
        self.check = check

    def __repr__(self):
        return f'{self.date} ({self.location.value})'

    @property
    def market(self):
        return _CloseMarket(date=self.date, location=self.location)

    def to_dict(self):
        return {'date': self.date, 'location': self.location, 'marketType': 'CloseMarket'}

    def __hash__(self):
        return hash((self.date, self.location))

    def __eq__(self, other):
        return isinstance(other, CloseMarket) and self.date == other.date and self.location == other.location

    @property
    def location(self) -> PricingLocation:
        if self.__location is not None and not self.check:
            return self.__location
        else:
            return market_location(self.__location)

    @property
    def date(self) -> dt.date:
        if self.__date is not None and not self.check:
            return self.__date
        else:
            return close_market_date(self.location, self.__date, self.roll_hr_and_min)


class TimestampedMarket(Market):
    """Market Object which captures market data based on location
    and timestamp
    """

    def __init__(self, timestamp: dt.datetime, location: Optional[Union[str, PricingLocation]] = None):
        self.__timestamp = timestamp
        self.__location = location if isinstance(location, PricingLocation) or location is None else \
            PricingLocation(location)

    def __repr__(self):
        return f'{self.__timestamp} ({self.location.value})'

    @property
    def market(self):
        return _TimestampedMarket(timestamp=self.__timestamp, location=self.location)

    @property
    def location(self) -> PricingLocation:
        return market_location(self.__location)


class LiveMarket(Market):
    """Market Object which captures market data based on location
    and time at runtime
    """

    def __init__(self, location: Optional[Union[str, PricingLocation]] = None):
        self.__location = location if isinstance(location, PricingLocation) or location is None else \
            PricingLocation(location)

    def __repr__(self):
        return f'Live ({self.location.value})'

    @property
    def location(self) -> PricingLocation:
        return market_location(self.__location)

    @property
    def market(self):
        return _LiveMarket(location=self.location)


class OverlayMarket(Market):
    """Market Object which overlays a base Market object (eg: CloseMarket, LiveMarket or
    TimestampedMarket) with a MarketDataMap (a map of market coordinate to float)
    """

    def __init__(self, market_data: Optional[MarketDataMap] = None, base_market: Optional[Market] = None,
                 binary_mkt_data: Optional[str] = None):
        market_data = market_data or {}

        self.__base_market = base_market or CloseMarket()
        self.__market_data = dict(filter(lambda elem: elem[1] != 'redacted', market_data.items()))
        self.__market_model_data = binary_mkt_data
        self.__redacted_coordinates = tuple(key for (key, value) in market_data.items() if value == 'redacted')

    def __getitem__(self, item):
        if isinstance(item, str):
            item = MarketDataCoordinate.from_string(item)

        return self.__market_data.get(item)

    def __setitem__(self, key, value):
        if isinstance(key, str):
            key = MarketDataCoordinate.from_string(key)

        if key in self.redacted_coordinates:
            raise KeyError(f'{key} cannot be overridden')

        self.__market_data[key] = value

    def __repr__(self):
        return f'Overlay ({id(self)}): {repr(self.__base_market)}'

    @property
    def market_data(self) -> Tuple[MarketDataCoordinateValue, ...]:
        return tuple(MarketDataCoordinateValue(coordinate=c, value=v) for c, v in self.__market_data.items())

    @property
    def market_model_data(self) -> str:
        return self.__market_model_data

    @property
    def market_data_dict(self) -> MarketDataMap:
        return {p.coordinate: p.value for p in self.market_data}

    @property
    def location(self) -> PricingLocation:
        return self.__base_market.location

    @property
    def market(self):
        return _OverlayMarket(base_market=self.__base_market.market, market_data=self.market_data,
                              market_model_data=self.market_model_data)

    @property
    def coordinates(self) -> Coordinates:
        return tuple(self.__market_data.keys())

    @property
    def redacted_coordinates(self) -> Coordinates:
        return self.__redacted_coordinates


class RefMarket(Market):
    """Market Object which represents a Reference to a Market
    """

    def __init__(self, market_ref: str):
        self.__market = _RefMarket(market_ref=str(market_ref))

    def __repr__(self):
        return f'Market Ref ({self.__market.market_ref})'

    @property
    def market(self):
        return self.__market

    @property
    def location(self) -> PricingLocation:
        return market_location()


class RelativeMarket(Market):
    """Market Object which captures the change between two Market Objects
    (to_market and from_market)
    """

    def __init__(self, from_market: Market, to_market: Market):
        self.__from_market = from_market
        self.__to_market = to_market

    def __repr__(self):
        return f'{repr(self.__from_market)} -> {repr(self.__to_market)}'

    @property
    def market(self):
        return _RelativeMarket(from_market=self.__from_market.market, to_market=self.__to_market.market)

    @property
    def location(self) -> PricingLocation:
        return self.__from_market.location if self.__from_market.location == self.__to_market.location else None
