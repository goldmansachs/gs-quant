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

from aenum import Enum, extend_enum
from typing import Optional


class DataMeasure(Enum):
    """Data measure definitions

    Enumeration of measures available through data APIs. Measures are facts that are usually quantities and that can
    be aggregated over a defined period of time. For example: tradePrice and volume are measures

    """
    ASK_PRICE = 'askPrice'
    BID_PRICE = 'bidPrice'
    HIGH_PRICE = 'highPrice'
    MID_PRICE = 'midPrice'
    LOW_PRICE = 'lowPrice'
    OPEN_PRICE = 'openPrice'
    CLOSE_PRICE = 'closePrice'
    TRADE_PRICE = 'tradePrice'
    SPOT_PRICE = 'spot'
    VOLUME = 'volume'
    ADJUSTED_ASK_PRICE = 'adjustedAskPrice'
    ADJUSTED_BID_PRICE = 'adjustedBidPrice'
    ADJUSTED_HIGH_PRICE = 'adjustedHighPrice'
    ADJUSTED_LOW_PRICE = 'adjustedLowPrice'
    ADJUSTED_OPEN_PRICE = 'adjustedBidPrice'
    ADJUSTED_CLOSE_PRICE = 'adjustedClosePrice'
    ADJUSTED_TRADE_PRICE = 'adjustedTradePrice'
    ADJUSTED_VOLUME = 'adjustedVolume'
    IMPLIED_VOLATILITY = 'impliedVolatility'
    VAR_SWAP = 'varSwap'
    PRICE = 'price'
    NAV_PRICE = 'navPrice'
    SPREAD = 'spread'
    NAV_SPREAD = 'navSpread'
    IMPLIED_VOLATILITY_BY_DELTA_STRIKE = 'impliedVolatilityByDeltaStrike'
    FORWARD_POINT = 'forwardPoint'


class DataDimension(Enum):
    """Data dimension definitions

    Enumeration of dimensions available through data APIs. Dimensions describe or provide context to measures, and can
    be used to select or group data. For example: ticker and exchange are dimensions

    """
    ASSET_ID = 'assetId'
    NAME = 'name'
    RIC = 'ric'
    TENOR = 'tenor'
    STRIKE_REFERENCE = 'strikeReference'
    RELATIVE_STRIKE = 'relativeStrike'
    EXPIRATION_DATE = 'expirationDate'
    UPDATE_TIME = 'updateTime'


class Fields(Enum):
    """Data field enumeration

    Enumeration of fields available through data APIs

    """

    @property
    def unit(self) -> Optional[str]:
        # TODO: Define units and look up appropriate unit for self
        return None


for enum in DataMeasure:
    extend_enum(Fields, enum.name, enum.value)

for enum in DataDimension:
    extend_enum(Fields, enum.name, enum.value)
