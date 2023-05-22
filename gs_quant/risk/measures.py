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
from typing import Union

from gs_quant.base import Market
from gs_quant.common import AssetClass, AggregationLevel, RiskMeasure
from gs_quant.target.common import RiskMeasureType, RiskMeasureUnit
from gs_quant.target.measures import IRBasis, IRVega, IRDelta, IRXccyDelta, InflationDelta

DEPRECATED_MEASURES = {}


class __RelativeRiskMeasure(RiskMeasure):
    def __init__(self,
                 to_market: Market,
                 asset_class: Union[AssetClass, str] = None,
                 measure_type: Union[RiskMeasureType, str] = None,
                 unit: Union[RiskMeasureUnit, str] = None,
                 value: Union[float, str] = None,
                 name: str = None):
        super().__init__(asset_class=asset_class, measure_type=measure_type, unit=unit, value=value)
        self.__to_market = to_market
        self.name = name

    @property
    def pricing_context(self):
        from gs_quant.markets import PricingContext, RelativeMarket
        current = PricingContext.current
        return current.clone(market=RelativeMarket(from_market=current.market, to_market=self.__to_market))


class PnlExplain(__RelativeRiskMeasure):
    """ Pnl Explained """

    def __init__(self, to_market: Market):
        super().__init__(to_market, measure_type=RiskMeasureType.PnlExplain, name=RiskMeasureType.PnlExplain.value)


class PnlExplainClose(PnlExplain):

    def __init__(self):
        from gs_quant.markets import CloseMarket
        super().__init__(CloseMarket())


class PnlExplainLive(PnlExplain):

    def __init__(self):
        from gs_quant.markets import LiveMarket
        super().__init__(LiveMarket())


class PnlPredictLive(__RelativeRiskMeasure):
    """ Pnl Predicted """

    def __init__(self):
        from gs_quant.markets import LiveMarket
        super().__init__(LiveMarket(), measure_type=RiskMeasureType.PnlPredict, name=RiskMeasureType.PnlPredict.value)


# Defining Parameterised Risk Measures
IRBasisParallel = IRBasis(aggregation_level=AggregationLevel.Asset, name='IRBasisParallel')
InflationDeltaParallel = InflationDelta(aggregation_level=AggregationLevel.Type, name='InflationDeltaParallel')
IRDeltaParallel = IRDelta(aggregation_level=AggregationLevel.Asset, name='IRDeltaParallel')
IRDeltaLocalCcy = IRDelta(currency='local', name='IRDeltaLocalCcy')
IRXccyDeltaParallel = IRXccyDelta(aggregation_level=AggregationLevel.Type, name='IRXccyDeltaParallel')
IRVegaParallel = IRVega(aggregation_level=AggregationLevel.Asset, name='IRVegaParallel')
IRVegaLocalCcy = IRVega(currency='local', name='IRVegaLocalCcy')
