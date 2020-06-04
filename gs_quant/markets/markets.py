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
from typing import Mapping, Optional, Union

from gs_quant.base import Market
from gs_quant.common import PricingLocation
from gs_quant.datetime.date import prev_business_date
from gs_quant.target.common import CloseMarket as _CloseMarket, LiveMarket as _LiveMarket,\
    OverlayMarket as __OverlayMarket, RelativeMarket as __RelativeMarket, TimestampedMarket as _TimestampedMarket
from gs_quant.target.data import MarketDataCoordinate as __MarketDataCoordinate


def market_location(location: Optional[PricingLocation] = None) -> PricingLocation:
    from .core import PricingContext
    default = PricingContext.current.market_data_location

    if location is None:
        return default or PricingLocation.LDN
    elif default and default != location:
        raise ValueError(f'Inconsistent market locations of {default} and {location} specified')
    else:
        return location


def close_market_date(location: Optional[Union[PricingLocation, str]] = None,
                      date: Optional[dt.date] = None) -> dt.date:
    from .core import PricingContext

    if date is None:
        return prev_business_date(PricingContext.current.pricing_date,
                                  calendars=location.value if isinstance(location, PricingLocation) else location) \
            if PricingContext.current.pricing_date == dt.date.today() else PricingContext.current.pricing_date
    elif date > PricingContext.current.pricing_date:
        raise ValueError('Market data date cannot be greater than pricing date')
    else:
        return date


class MarketDataCoordinate(__MarketDataCoordinate):

    def __str__(self):
        return "|".join(f or '' for f in (self.mkt_type, self.mkt_asset, self.mkt_class,
                                          '_'.join(self.mkt_point or ()), self.mkt_quoting_style))


MarketDataMap = Mapping[MarketDataCoordinate, float]


class CloseMarket(_CloseMarket, Market):

    __date_cache = {}

    def __init__(self, date: Optional[dt.date] = None, location: Optional[Union[str, PricingLocation]] = None):
        super().__init__(date=date, location=location)

    def __repr__(self):
        return f'{self.date} ({self.location.value})'

    @_CloseMarket.location.getter
    def location(self) -> PricingLocation:
        return market_location(super().location)

    @_CloseMarket.date.getter
    def date(self) -> dt.date:
        return close_market_date(self.location, super().date)


class TimestampedMarket(_TimestampedMarket, Market):

    def __init__(self, timestamp: dt.datetime, location: Optional[Union[str, PricingLocation]] = None):
        super().__init__(timestamp=timestamp, location=location)

    def __repr__(self):
        return f'{self.timestamp} ({self.location.value})'

    @_TimestampedMarket.location.getter
    def location(self) -> PricingLocation:
        return market_location(super().location)


class LiveMarket(_LiveMarket, Market):

    def __init__(self, location: Optional[Union[str, PricingLocation]] = None):
        super().__init__(location=location)

    def __repr__(self):
        return f'Live ({self.location.value})'

    @_LiveMarket.location.getter
    def location(self) -> PricingLocation:
        return market_location(super().location)


class OverlayMarket(__OverlayMarket, Market):

    def __init__(self, base_market: Market, market_data: MarketDataMap):
        super().__init__(base_market=base_market, market_data=market_data.items())

    def __repr__(self):
        return f'Overlayed ({id(self)}): {repr(self.base_market)}'


class RelativeMarket(__RelativeMarket, Market):

    def __init__(self, from_market: Market, to_market: Market):
        super().__init__(from_market=from_market, to_market=to_market)

    def __repr__(self):
        return f'{repr(self.from_market)} -> {repr(self.to_market)}'
