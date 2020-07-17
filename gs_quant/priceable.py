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
from gs_quant.base import Priceable
from gs_quant.markets import MarketDataCoordinate
from gs_quant.risk import DataFrameWithInfo, DollarPrice, FloatWithInfo, MarketDataAssets, Price, SeriesWithInfo
from gs_quant.risk.results import PricingFuture, PortfolioRiskResult

from abc import ABCMeta
import itertools
import logging
from typing import Tuple, Union

__asset_class_and_type_to_instrument = {}
_logger = logging.getLogger(__name__)


class PriceableImpl(Priceable, metaclass=ABCMeta):

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

    def price(self) -> Union[FloatWithInfo, PortfolioRiskResult, PricingFuture, SeriesWithInfo]:
        """
        Present value in local currency. Note that this is not yet supported on all instruments

        ***Examples**

        >>> from gs_quant.instrument import IRSwap
        >>>
        >>> swap = IRSwap('Pay', '10y', 'EUR')
        >>> price = swap.price()

        price is the present value in EUR (a float)
        """
        return self.calc(Price)

    def coordinates(self) -> Tuple[MarketDataCoordinate, ...]:
        from gs_quant.api.gs.data import GsDataApi

        def coordinates_for_asset(result: DataFrameWithInfo):
            return tuple(itertools.chain.from_iterable(GsDataApi.get_many_coordinates(mkt_type=t,
                                                                                      mkt_asset=a,
                                                                                      return_type=MarketDataCoordinate,
                                                                                      limit=10000)
                                                       for t, a in zip(result.mkt_type, result.mkt_asset)))

        return self.calc(MarketDataAssets, fn=coordinates_for_asset)
