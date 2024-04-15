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
from dataclasses_json import LetterCase, dataclass_json
from dataclasses import dataclass, field


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
    ADJUSTED_OPEN_PRICE = 'adjustedOpenPrice'
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
    DIVIDEND_YIELD = 'Dividend Yield'
    EARNINGS_PER_SHARE = 'Earnings per Share'
    EARNINGS_PER_SHARE_POSITIVE = 'Earnings per Share Positive'
    NET_DEBT_TO_EBITDA = 'Net Debt to EBITDA'
    PRICE_TO_BOOK = 'Price to Book'
    PRICE_TO_CASH = 'Price to Cash'
    PRICE_TO_EARNINGS = 'Price to Earnings'
    PRICE_TO_EARNINGS_POSITIVE = 'Price to Earnings Positive'
    PRICE_TO_EARNINGS_POSITIVE_EXCLUSIVE = 'Price to Earnings Positive Exclusive'
    PRICE_TO_SALES = 'Price to Sales'
    RETURN_ON_EQUITY = 'Return on Equity'
    SALES_PER_SHARE = 'Sales per Share'
    CURRENT_CONSTITUENTS_DIVIDEND_YIELD = 'Current Constituents Dividend Yield'
    CURRENT_CONSTITUENTS_EARNINGS_PER_SHARE = 'Current Constituents Earnings per Share'
    CURRENT_CONSTITUENTS_EARNINGS_PER_SHARE_POSITIVE = 'Current Constituents Earnings per Share Positive'
    CURRENT_CONSTITUENTS_NET_DEBT_TO_EBITDA = 'Current Constituents Net Debt to EBITDA'
    CURRENT_CONSTITUENTS_PRICE_TO_BOOK = 'Current Constituents Price to Book'
    CURRENT_CONSTITUENTS_PRICE_TO_CASH = 'Current Constituents Price to Cash'
    CURRENT_CONSTITUENTS_PRICE_TO_EARNINGS = 'Current Constituents Price to Earnings'
    CURRENT_CONSTITUENTS_PRICE_TO_EARNINGS_POSITIVE = 'Current Constituents Price to Earnings Positive'
    CURRENT_CONSTITUENTS_PRICE_TO_SALES = 'Current Constituents Price to Sales'
    CURRENT_CONSTITUENTS_RETURN_ON_EQUITY = 'Current Constituents Return on Equity'
    CURRENT_CONSTITUENTS_SALES_PER_SHARE = 'Current Constituents Sales per Share'
    ONE_YEAR = '1y'
    TWO_YEARS = '2y'
    THREE_YEARS = '3y'
    FORWARD = 'forward'
    TRAILING = 'trailing'

    def __repr__(self):
        return self.value

    @classmethod
    def list_fundamentals(cls):
        return [metric.value for metric in [cls.DIVIDEND_YIELD, cls.EARNINGS_PER_SHARE, cls.EARNINGS_PER_SHARE_POSITIVE,
                                            cls.NET_DEBT_TO_EBITDA, cls.PRICE_TO_BOOK, cls.PRICE_TO_CASH,
                                            cls.PRICE_TO_EARNINGS, cls.PRICE_TO_EARNINGS_POSITIVE,
                                            cls.PRICE_TO_EARNINGS_POSITIVE_EXCLUSIVE,
                                            cls.PRICE_TO_SALES, cls.RETURN_ON_EQUITY, cls.SALES_PER_SHARE,
                                            cls.CURRENT_CONSTITUENTS_DIVIDEND_YIELD,
                                            cls.CURRENT_CONSTITUENTS_EARNINGS_PER_SHARE,
                                            cls.CURRENT_CONSTITUENTS_EARNINGS_PER_SHARE_POSITIVE,
                                            cls.CURRENT_CONSTITUENTS_NET_DEBT_TO_EBITDA,
                                            cls.CURRENT_CONSTITUENTS_PRICE_TO_BOOK,
                                            cls.CURRENT_CONSTITUENTS_PRICE_TO_CASH,
                                            cls.CURRENT_CONSTITUENTS_PRICE_TO_EARNINGS,
                                            cls.CURRENT_CONSTITUENTS_PRICE_TO_EARNINGS_POSITIVE,
                                            cls.CURRENT_CONSTITUENTS_PRICE_TO_SALES,
                                            cls.CURRENT_CONSTITUENTS_RETURN_ON_EQUITY,
                                            cls.CURRENT_CONSTITUENTS_SALES_PER_SHARE]]


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


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class AssetMeasure():
    dataset_field: str = field(default=None)
    frequency: str = field(default=None)
    type: str = field(default=None)
