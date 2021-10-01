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
from typing import Optional

from gs_quant.risk.base_measures import *
from gs_quant.risk.base_measures import __RelativeRiskMeasure
from gs_quant.target.risk import RiskMeasureType, RiskMeasureUnit

DEPRECATED_MEASURES = {'IRDeltaParallelLocalCcy': 'IRDelta',
                       'InflationDeltaParallelLocalCcy': 'InflationDelta',
                       'IRXccyDeltaParallelLocalCurrency': 'IRXccyDelta',
                       'IRVegaParallelLocalCcy': 'IRVega',
                       }


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


def __risk_measure_with_doc_string(name: str,
                                   doc: str,
                                   measure_type: RiskMeasureType,
                                   asset_class: Optional[AssetClass] = None,
                                   unit: Optional[RiskMeasureUnit] = None,
                                   parameter_type: str = None
                                   ) -> RiskMeasure:
    if parameter_type == "Currency":
        measure = RiskMeasureWithCurrencyParameter(measure_type=measure_type, asset_class=asset_class, unit=unit,
                                                   name=name)
    elif parameter_type == "FiniteDifference":
        measure = RiskMeasureWithFiniteDifferenceParameter(measure_type=measure_type, asset_class=asset_class,
                                                           unit=unit, name=name)
    elif parameter_type == "String":
        measure = RiskMeasureWithStringParameter(measure_type=measure_type, asset_class=asset_class,
                                                 unit=unit, name=name)
    elif parameter_type == "ListOfString":
        measure = RiskMeasureWithListOfStringParameter(measure_type=measure_type, asset_class=asset_class,
                                                       unit=unit, name=name)
    elif parameter_type == "ListOfNumber":
        measure = RiskMeasureWithListOfNumberParameter(measure_type=measure_type, asset_class=asset_class,
                                                       unit=unit, name=name)
    elif parameter_type == "Map":
        measure = RiskMeasureWithMapParameter(measure_type=measure_type, asset_class=asset_class,
                                              unit=unit, name=name)
    else:
        measure = RiskMeasure(measure_type=measure_type, asset_class=asset_class, unit=unit, name=name)
    measure.__doc__ = doc
    return measure


DollarPrice = __risk_measure_with_doc_string('DollarPrice', 'Present value in USD', RiskMeasureType.Dollar_Price)
Price = __risk_measure_with_doc_string('Price', 'Present value in local currency', RiskMeasureType.PV,
                                       parameter_type="Currency")
PricePips = __risk_measure_with_doc_string('Price', 'Present value in pips', RiskMeasureType.Price,
                                           unit=RiskMeasureUnit.Pips,
                                           parameter_type="Currency")
Annuity = __risk_measure_with_doc_string('Annuity', 'Annuity', RiskMeasureType.AnnuityLocalCcy,
                                         asset_class=AssetClass.Rates, parameter_type='Currency')

CrossMultiplier = __risk_measure_with_doc_string('CrossMultiplier', 'Cross Multiplier',
                                                 RiskMeasureType.Cross_Multiplier)
ForwardPrice = __risk_measure_with_doc_string(
    'ForwardPrice',
    'Forward price',
    RiskMeasureType.Forward_Price,
    unit=RiskMeasureUnit.BPS)
BaseCPI = __risk_measure_with_doc_string('BaseCPI', 'Base CPI level', RiskMeasureType.BaseCPI)
Theta = __risk_measure_with_doc_string('Theta', '1 day Theta', RiskMeasureType.Theta)
EqDelta = __risk_measure_with_doc_string(
    'EqDelta',
    'Equity Delta',
    RiskMeasureType.Delta,
    asset_class=AssetClass.Equity)
EqGamma = __risk_measure_with_doc_string(
    'EqGamma',
    'Equity Gamma',
    RiskMeasureType.Gamma,
    asset_class=AssetClass.Equity)
EqVega = __risk_measure_with_doc_string('EqVega', 'Equity Vega', RiskMeasureType.Vega, asset_class=AssetClass.Equity)
EqSpot = __risk_measure_with_doc_string(
    'EqSpot',
    'Equity Spot Level',
    RiskMeasureType.Spot, asset_class=AssetClass.Equity)
EqAnnualImpliedVol = __risk_measure_with_doc_string(
    'EqAnnualImpliedVol',
    'Equity Annual Implied Volatility (%)',
    RiskMeasureType.Annual_Implied_Volatility,
    asset_class=AssetClass.Equity,
    unit=RiskMeasureUnit.Percent)
CommodDelta = __risk_measure_with_doc_string(
    'CommodDelta',
    'Commodity Delta',
    RiskMeasureType.Delta,
    asset_class=AssetClass.Commod)
CommodTheta = __risk_measure_with_doc_string(
    'CommodTheta',
    'Commodity Theta',
    RiskMeasureType.Theta,
    asset_class=AssetClass.Commod)
CommodVega = __risk_measure_with_doc_string(
    'CommodVega',
    'Commodity Vega',
    RiskMeasureType.Vega,
    asset_class=AssetClass.Commod)
FairVolStrike = __risk_measure_with_doc_string(
    'FairVolStrike',
    'Fair Volatility Strike Value of a Variance Swap',
    RiskMeasureType.FairVolStrike)
FairVarStrike = __risk_measure_with_doc_string(
    'FairVarStrike',
    'Fair Variance Strike Value of a Variance Swap',
    RiskMeasureType.FairVarStrike)
FXDelta = __risk_measure_with_doc_string('FXDelta', 'FX Delta', RiskMeasureType.Delta, asset_class=AssetClass.FX,
                                         parameter_type="FiniteDifference")
FXGamma = __risk_measure_with_doc_string('FXGamma', 'FX Gamma', RiskMeasureType.Gamma, asset_class=AssetClass.FX)
FXVega = __risk_measure_with_doc_string('FXVega', 'FX Vega', RiskMeasureType.Vega, asset_class=AssetClass.FX,
                                        parameter_type="FiniteDifference")
FXSpot = __risk_measure_with_doc_string('FXSpot', 'FX Spot Rate', RiskMeasureType.Spot, asset_class=AssetClass.FX)
FXAnnualATMImpliedVol = __risk_measure_with_doc_string(
    'FXAnnualATMImpliedVol',
    'FX Annual ATM Implied Volatility',
    RiskMeasureType.Annual_ATM_Implied_Volatility,
    asset_class=AssetClass.FX,
    unit=RiskMeasureUnit.Percent)
FXAnnualImpliedVol = __risk_measure_with_doc_string(
    'FXAnnualImpliedVol',
    'FX Annual Implied Volatility',
    RiskMeasureType.Annual_Implied_Volatility,
    asset_class=AssetClass.FX,
    unit=RiskMeasureUnit.Percent)
IRBasis = __risk_measure_with_doc_string(
    'IRBasis',
    'Interest Rate Basis',
    RiskMeasureType.Basis,
    asset_class=AssetClass.Rates, parameter_type="FiniteDifference")
IRBasisParallel = IRBasis(aggregation_level=AggregationLevel.Asset, name='IRBasisParallel')
InflationDelta = __risk_measure_with_doc_string(
    'InflationDelta',
    'Inflation Delta',
    RiskMeasureType.InflationDelta,
    asset_class=AssetClass.Rates, parameter_type='FiniteDifference')
InflationDeltaParallel = InflationDelta(aggregation_level=AggregationLevel.Type, name='InflationDeltaParallel')
InflationDeltaParallelLocalCcy = InflationDelta(aggregation_level=AggregationLevel.Type, currency='local',
                                                name='InflationDeltaParallelLocalCcy')
IRDelta = __risk_measure_with_doc_string(
    'IRDelta',
    'Interest Rate Delta',
    RiskMeasureType.Delta,
    asset_class=AssetClass.Rates, parameter_type="FiniteDifference")
IRDeltaParallel = IRDelta(aggregation_level=AggregationLevel.Asset, name='IRDeltaParallel')
IRDeltaLocalCcy = IRDelta(currency='local', name='IRDeltaLocalCcy')
IRDeltaParallelLocalCcy = IRDelta(aggregation_level=AggregationLevel.Type, currency='local',
                                  name='IRDeltaParallelLocalCcy')
IRDiscountDeltaParallel = __risk_measure_with_doc_string(
    'IRDiscountDeltaParallel',
    'Parallel Discount Delta',
    RiskMeasureType.ParallelDiscountDelta,
    asset_class=AssetClass.Rates)
IRDiscountDeltaParallelLocalCcy = __risk_measure_with_doc_string(
    'IRDiscountDeltaParallelLocalCcy',
    'Parallel Discount Delta (Local Ccy)',
    RiskMeasureType.ParallelDiscountDeltaLocalCcy,
    asset_class=AssetClass.Rates)
IRXccyDelta = __risk_measure_with_doc_string(
    'IRXccyDelta',
    'Cross-ccy Delta',
    RiskMeasureType.XccyDelta,
    asset_class=AssetClass.Rates, parameter_type='FiniteDifference')
IRXccyDeltaParallel = IRXccyDelta(aggregation_level=AggregationLevel.Type, name='IRXccyDeltaParallel')
IRXccyDeltaParallelLocalCurrency = IRXccyDelta(aggregation_level=AggregationLevel.Type, currency='local',
                                               name='IRXccyDeltaParallelLocalCurrency')
IRGammaParallel = __risk_measure_with_doc_string(
    'IRGammaParallel',
    'Interest Rate Parallel Gamma',
    RiskMeasureType.ParallelGamma,
    asset_class=AssetClass.Rates)
IRGammaParallelLocalCcy = __risk_measure_with_doc_string(
    'IRGammaParallelLocalCcy',
    'Interest Rate Parallel Gamma (Local Ccy)',
    RiskMeasureType.ParallelGammaLocalCcy,
    asset_class=AssetClass.Rates)
IRVega = __risk_measure_with_doc_string(
    'IRVega',
    'Interest Rate Vega',
    RiskMeasureType.Vega,
    asset_class=AssetClass.Rates, parameter_type="FiniteDifference")
IRVegaParallel = IRVega(aggregation_level=AggregationLevel.Asset, name='IRVegaParallel')
IRVegaLocalCcy = IRVega(currency='local', name='IRVegaLocalCcy')
IRVegaParallelLocalCcy = IRVega(aggregation_level=AggregationLevel.Type, currency='local',
                                name='IRVegaParallelLocalCcy')
IRAnnualImpliedVol = __risk_measure_with_doc_string(
    'IRAnnualImpliedVol',
    'Interest Rate Annual Implied Volatility (%)',
    RiskMeasureType.Annual_Implied_Volatility,
    asset_class=AssetClass.Rates,
    unit=RiskMeasureUnit.Percent)
IRAnnualATMImpliedVol = __risk_measure_with_doc_string(
    'IRAnnualATMImpliedVol',
    'Interest Rate Annual Implied At-The-Money Volatility (%)',
    RiskMeasureType.Annual_ATMF_Implied_Volatility,
    asset_class=AssetClass.Rates,
    unit=RiskMeasureUnit.Percent)
IRDailyImpliedVol = __risk_measure_with_doc_string(
    'IRDailyImpliedVol',
    'Interest Rate Daily Implied Volatility (bps)',
    RiskMeasureType.Daily_Implied_Volatility,
    asset_class=AssetClass.Rates,
    unit=RiskMeasureUnit.BPS)
IRSpotRate = __risk_measure_with_doc_string(
    'IRSpotRate',
    'At-The-Money Spot Rate (%)',
    RiskMeasureType.Spot_Rate,
    asset_class=AssetClass.Rates,
    unit=RiskMeasureUnit.Percent)
IRFwdRate = __risk_measure_with_doc_string(
    'IRFwdRate',
    'Par Rate (%)',
    RiskMeasureType.Forward_Rate,
    asset_class=AssetClass.Rates,
    unit=RiskMeasureUnit.Percent)
CDDelta = __risk_measure_with_doc_string(
    'CDDelta',
    'Credit Delta',
    RiskMeasureType.Delta,
    asset_class=AssetClass.Credit)
CDVega = __risk_measure_with_doc_string(
    'CDVega',
    'Credit Vega',
    RiskMeasureType.Vega,
    asset_class=AssetClass.Credit)
CDGamma = __risk_measure_with_doc_string(
    'CDGamma',
    'Credit Gamma',
    RiskMeasureType.Gamma,
    asset_class=AssetClass.Credit)
CDTheta = __risk_measure_with_doc_string(
    'CDTheta',
    'Credit Theta',
    RiskMeasureType.Theta,
    asset_class=AssetClass.Credit)
CDATMSpread = __risk_measure_with_doc_string(
    'CDATMSpread',
    'Credit ATM Spread',
    RiskMeasureType.ATM_Spread,
    asset_class=AssetClass.Credit)
CRIFIRCurve = __risk_measure_with_doc_string(
    'CRIFIRCurve',
    'CRIF IR Curve',
    RiskMeasureType.CRIF_IRCurve)
ResolvedInstrumentValues = __risk_measure_with_doc_string(
    'ResolvedInstrumentBaseValues',
    'Resolved InstrumentBase Values',
    RiskMeasureType.Resolved_Instrument_Values
)
Description = __risk_measure_with_doc_string(
    'Description',
    'Description',
    RiskMeasureType.Description
)
Cashflows = __risk_measure_with_doc_string(
    'Cashflows',
    'Cashflows',
    RiskMeasureType.Cashflows
)
MarketDataAssets = __risk_measure_with_doc_string(
    'MarketDataAssets',
    'MarketDataAssets',
    RiskMeasureType.Market_Data_Assets
)
MarketData = __risk_measure_with_doc_string(
    'Market Data',
    'Market Data map of coordinates and values',
    RiskMeasureType.Market_Data
)
ParSpread = __risk_measure_with_doc_string(
    'ParSpread',
    'Par Spread',
    RiskMeasureType.Spread,
    asset_class=AssetClass.Rates)
ATMSpread = __risk_measure_with_doc_string(
    'ATMSpread',
    'ATM Spread',
    RiskMeasureType.ATM_Spread,
    asset_class=AssetClass.Credit)
FwdSpread = __risk_measure_with_doc_string(
    'FwdSpread',
    'Fwd Spread',
    RiskMeasureType.Forward_Spread,
    asset_class=AssetClass.Credit)
ImpliedVolatility = __risk_measure_with_doc_string(
    'ImpliedVolatility',
    'Implied Volatility',
    RiskMeasureType.Implied_Volatility,
    asset_class=AssetClass.Credit)
