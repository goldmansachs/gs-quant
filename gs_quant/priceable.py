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
import logging
from abc import ABC
from typing import Union, Optional

from gs_quant.base import Priceable
from gs_quant.context_base import nullcontext
from gs_quant.markets import MarketDataCoordinate, PricingContext, CloseMarket, OverlayMarket
from gs_quant.risk import DataFrameWithInfo, DollarPrice, FloatWithInfo, Price, SeriesWithInfo, \
    MarketData
from gs_quant.risk.results import PricingFuture, PortfolioRiskResult, ErrorValue

__asset_class_and_type_to_instrument = {}
_logger = logging.getLogger(__name__)


class PriceableImpl(Priceable, ABC):

    @property
    def _pricing_context(self) -> PricingContext:
        pricing_context = PricingContext.current
        return pricing_context if not (pricing_context.is_entered or pricing_context.is_async) else nullcontext()

    @property
    def _return_future(self) -> bool:
        pricing_context = self._pricing_context
        return not isinstance(pricing_context, PricingContext) or (pricing_context.is_async or
                                                                   pricing_context.is_entered)

    def dollar_price(self) -> Union[FloatWithInfo, PortfolioRiskResult, PricingFuture, SeriesWithInfo]:
        """
        Present value in USD

        :return:  a float or a future, depending on whether the current PricingContext is async, or has been entered

        **Examples**

        >>> from gs_quant.instrument import IRCap
        >>>
        >>> cap = IRCap('1y', 'EUR')
        >>> price = cap.dollar_price()

        price is the present value in USD (a float)

        >>> cap_usd = IRCap('1y', 'USD')
        >>> cap_eur = IRCap('1y', 'EUR')
        >>>
        >>> from gs_quant.markets import PricingContext
        >>>
        >>> with PricingContext():
        >>>     price_usd_f = cap_usd.dollar_price()
        >>>     price_eur_f = cap_eur.dollar_price()
        >>>
        >>> price_usd = price_usd_f.result()
        >>> price_eur = price_eur_f.result()

        price_usd_f and price_eur_f are futures, price_usd and price_eur are floats
        """
        return self.calc(DollarPrice)

    def price(self, currency=None) -> Union[FloatWithInfo, PortfolioRiskResult, PricingFuture, SeriesWithInfo]:
        """
        Present value in local currency. Note that this is not yet supported on all instruments

        ***Examples**

        >>> from gs_quant.instrument import IRSwap
        >>>
        >>> swap = IRSwap('Pay', '10y', 'EUR')
        >>> price = swap.price()

        price is the present value in EUR (a float)
        """
        return self.calc(Price(currency=currency)) if currency else self.calc(Price)

    def market(self) -> Union[OverlayMarket, PricingFuture]:
        """
        Market Data map of coordinates and values. Note that this is not yet supported on all instruments

        ***Examples**

        >>> from gs_quant.instrument import IRSwap
        >>>
        >>> swap = IRSwap('Pay', '10y', 'EUR')
        >>> market = swap.market()

        """

        def handle_result(result: Optional[Union[DataFrameWithInfo, ErrorValue, PricingFuture]]) -> \
                [OverlayMarket, dict]:
            if isinstance(result, ErrorValue):
                return result

            properties = MarketDataCoordinate.properties()
            is_historical = result.index.name == 'date'
            location = PricingContext.current.market_data_location

            def extract_market_data(this_result: DataFrameWithInfo):
                market_data = {}

                for _, row in this_result.iterrows():
                    coordinate_values = {p: row.get(p) for p in properties}
                    mkt_point = coordinate_values.get('mkt_point')
                    if mkt_point is not None:
                        coordinate_values['mkt_point'] = tuple(coordinate_values['mkt_point'].split(';'))

                    # return 'redacted' as coordinate value if its a redacted coordinate
                    market_data[MarketDataCoordinate.from_dict(coordinate_values)] = row['value'] if \
                        row['permissions'] == 'Granted' else 'redacted'

                return market_data

            if is_historical:
                return {date: OverlayMarket(
                    base_market=CloseMarket(date=date, location=location),
                    market_data=extract_market_data(result.loc[date]))
                    for date in set(result.index)}
            else:
                return OverlayMarket(base_market=result.risk_key.market,
                                     market_data=extract_market_data(result))

        return self.calc(MarketData, fn=handle_result)
