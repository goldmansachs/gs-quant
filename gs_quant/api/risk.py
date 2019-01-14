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

from gs_quant.target.risk import *
from gs_quant.target.risk import MarketDataCoordinate as __MarketDataCoordinate
from gs_quant.api.common import AssetClass
from collections import namedtuple
from typing import List, Any


class MarketDataCoordinate(__MarketDataCoordinate):

    def __str__(self):
        return "|".join(f or '' for f in (self.__marketDataType, self.__assetId, self.__pointClass, self.__point, self.__field))


FormattedRiskMeasure = namedtuple('FormattedRiskMeasure', ('risk_measure', 'formatter'))


def scalar_formatter(result: List) -> Any:
    return result[0].get('value', result[0].get('Val'))


PresentValue = FormattedRiskMeasure(RiskMeasure(measureType=RiskMeasureType.Dollar_Price), scalar_formatter)
EqDelta = FormattedRiskMeasure(RiskMeasure(measureType=RiskMeasureType.Delta, assetClass=AssetClass.Equity), scalar_formatter)
EqGamma = FormattedRiskMeasure(RiskMeasure(measureType=RiskMeasureType.Gamma, assetClass=AssetClass.Equity), scalar_formatter)
EqVega = FormattedRiskMeasure(RiskMeasure(measureType=RiskMeasureType.Vega, assetClass=AssetClass.Equity), scalar_formatter)
EqTheta = FormattedRiskMeasure(RiskMeasure(measureType=RiskMeasureType.Theta, assetClass=AssetClass.Equity), scalar_formatter)
CommodDelta = RiskMeasure(measureType=RiskMeasureType.Delta, assetClass=AssetClass.Commod)
CommodGamma = RiskMeasure(measureType=RiskMeasureType.Gamma, assetClass=AssetClass.Commod)
CommodVega = RiskMeasure(measureType=RiskMeasureType.Vega, assetClass=AssetClass.Commod)
CommodTheta = RiskMeasure(measureType=RiskMeasureType.Theta, assetClass=AssetClass.Commod)
FXDelta = RiskMeasure(measureType=RiskMeasureType.Delta, assetClass=AssetClass.FX)
FXGamma = RiskMeasure(measureType=RiskMeasureType.Gamma, assetClass=AssetClass.FX)
FXVega = RiskMeasure(measureType=RiskMeasureType.Vega, assetClass=AssetClass.FX)
FXTheta = RiskMeasure(measureType=RiskMeasureType.Theta, assetClass=AssetClass.FX)
IRDelta = RiskMeasure(measureType=RiskMeasureType.Delta, assetClass=AssetClass.Rates)
IRGamma = RiskMeasure(measureType=RiskMeasureType.Gamma, assetClass=AssetClass.Rates)
IRVega = RiskMeasure(measureType=RiskMeasureType.Vega, assetClass=AssetClass.Rates)
IRTheta = RiskMeasure(measureType=RiskMeasureType.Theta, assetClass=AssetClass.Rates)
