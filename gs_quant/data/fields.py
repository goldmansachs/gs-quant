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
from enum import Enum
from typing import Optional


class Fields(Enum):
    """Data field definitions

    Enumeration of fields available through data APIs

    """

    ASK_PRICE = 'askPrice'
    BID_PRICE = 'bidPrice'
    HIGH_PRICE = 'highPrice'
    MID_PRICE = 'midPrice'
    LOW_PRICE = 'lowPrice'
    OPEN_PRICE = 'openPrice'
    CLOSE_PRICE = 'closePrice'
    TRADE_PRICE = 'tradePrice'
    VOLUME = 'volume'
    ADJUSTED_ASK_PRICE = 'adjustedAskPrice'
    ADJUSTED_BID_PRICE = 'adjustedBidPrice'
    ADJUSTED_HIGH_PRICE = 'adjustedHighPrice'
    ADJUSTED_LOW_PRICE = 'adjustedLowPrice'
    ADJUSTED_OPEN_PRICE = 'adjustedBidPrice'
    ADJUSTED_TRADE_PRICE = 'adjustedTradePrice'
    ADJUSTED_VOLUME = 'adjustedVolume'
    UPDATE_TIME = 'updateTime'

    @property
    def unit(self) -> Optional[str]:
        # TODO: Define units and look up appropriate unit for self
        return None
