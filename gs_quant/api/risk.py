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
from gs_quant.api.common import AssetClass
from collections import namedtuple
import pandas as pd
from typing import List, Any


FormattedRiskMeasure = namedtuple('FormattedRiskMeasure', ('risk_measure', 'formatter'))


def scalar_formatter(result: List) -> float:
    return result[0].get('value', result[0].get('Val'))


def structured_formatter(result: List) -> pd.DataFrame:
    df = pd.DataFrame(result)
    del df['field']
    return df


PresentValue = FormattedRiskMeasure(RiskMeasure(measureType=RiskMeasureType.Dollar_Price), scalar_formatter)
Theta = FormattedRiskMeasure(RiskMeasure(measureType=RiskMeasureType.Theta), scalar_formatter)

EqDelta = FormattedRiskMeasure(RiskMeasure(measureType=RiskMeasureType.Delta, assetClass=AssetClass.Equity), scalar_formatter)
EqGamma = FormattedRiskMeasure(RiskMeasure(measureType=RiskMeasureType.Gamma, assetClass=AssetClass.Equity), scalar_formatter)
EqVega = FormattedRiskMeasure(RiskMeasure(measureType=RiskMeasureType.Vega, assetClass=AssetClass.Equity), scalar_formatter)
CommodDelta = FormattedRiskMeasure(RiskMeasure(measureType=RiskMeasureType.Delta, assetClass=AssetClass.Commod), structured_formatter)
CommodGamma = FormattedRiskMeasure(RiskMeasure(measureType=RiskMeasureType.Gamma, assetClass=AssetClass.Commod), structured_formatter)
CommodVega = FormattedRiskMeasure(RiskMeasure(measureType=RiskMeasureType.Vega, assetClass=AssetClass.Commod), structured_formatter)
CommodTheta = FormattedRiskMeasure(RiskMeasure(measureType=RiskMeasureType.Theta, assetClass=AssetClass.Commod), structured_formatter)
FXDelta = FormattedRiskMeasure(RiskMeasure(measureType=RiskMeasureType.Delta, assetClass=AssetClass.FX), structured_formatter)
FXGamma = FormattedRiskMeasure(RiskMeasure(measureType=RiskMeasureType.Gamma, assetClass=AssetClass.FX), structured_formatter)
FXVega = FormattedRiskMeasure(RiskMeasure(measureType=RiskMeasureType.Vega, assetClass=AssetClass.FX), structured_formatter)
IRDelta = FormattedRiskMeasure(RiskMeasure(measureType=RiskMeasureType.Delta, assetClass=AssetClass.Rates), structured_formatter)
IRGamma = FormattedRiskMeasure(RiskMeasure(measureType=RiskMeasureType.Gamma, assetClass=AssetClass.Rates), structured_formatter)
IRVega = FormattedRiskMeasure(RiskMeasure(measureType=RiskMeasureType.Vega, assetClass=AssetClass.Rates), structured_formatter)
