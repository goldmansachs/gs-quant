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

from gs_quant.base import EnumBase


class IndicesDatasets(EnumBase, Enum):
    CORPORATE_ACTIONS = 'CA'
    BASKET_FUNDAMENTALS = 'BASKET_FUNDAMENTALS'

    def __repr__(self):
        return self.value


class FundamentalsMetrics(EnumBase, Enum):
    DIVIDEND_YIELD = 'Dividend Yield'
    EARNINGS_PER_SHARE = 'Earnings per Share'
    EARNINGS_PER_SHARE_POSITIVE = 'Earnings per Share Positive'
    NET_DEBT_TO_EBITDA = 'Net Debt to EBITDA'
    PRICE_TO_BOOK = 'Price to Book'
    PRICE_TO_CASH = 'Price to Cash'
    PRICE_TO_EARNINGS = 'Price to Earnings'
    PRICE_TO_EARNINGS_POSITIVE = 'Price to Earnings Positive'
    PRICE_TO_SALES = 'Price to Sales'
    RETURN_ON_EQUITY = 'Return on Equity'
    SALES_PER_SHARE = 'Sales per Share'

    def __repr__(self):
        return self.value

    @classmethod
    def to_list(cls):
        return [metric.value for metric in cls]


class FundamentalMetricPeriod(EnumBase, Enum):
    ONE_YEAR = '1y'
    TWO_YEARS = '2y'
    THREE_YEARS = '3y'

    def __repr__(self):
        return self.value


class FundamentalMetricPeriodDirection(EnumBase, Enum):
    FORWARD = 'forward'
    TRAILING = 'trailing'

    def __repr__(self):
        return self.value


class BasketTypes(EnumBase, Enum):
    CUSTOM_BASKET = 'Custom Basket'
    RESEARCH_BASKET = 'Research Basket'

    def __repr__(self):
        return self.value

    @classmethod
    def to_list(cls):
        return [basket_type.value for basket_type in cls]
