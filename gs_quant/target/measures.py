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

import copy

import pandas as pd
from gs_quant.common import AssetClass, CurrencyParameter, FiniteDifferenceParameter, StringParameter, \
    ListOfStringParameter, ListOfNumberParameter, MapParameter
from gs_quant.common import ParameterisedRiskMeasure, RiskMeasure
from gs_quant.target.risk import RiskMeasureType, RiskMeasureUnit


class RiskMeasureWithCurrencyParameter(ParameterisedRiskMeasure):
    @property
    def currency(self):
        return self.parameters.value if self.parameters else None

    def __call__(self, currency=None,  name=None):
        # hack to prevent ParameterisedRiskMeasure input into pandas LocIndexer as a callable function that returns
        # output for indexing (https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html)
        if isinstance(currency, (pd.Series, pd.DataFrame)):
            return self

        clone = copy.copy(self)
        if name:
            clone.name = name

        if currency is None and clone.parameters is not None:
            currency = clone.parameters.currency

        param = CurrencyParameter(value=currency)
        clone.parameters = param
        return clone


class RiskMeasureWithDoubleParameter(ParameterisedRiskMeasure):
    @property
    def double(self):
        return self.parameters.value if self.parameters else None

    def __call__(self, double=None,  name=None):
        # hack to prevent ParameterisedRiskMeasure input into pandas LocIndexer as a callable function that returns
        # output for indexing (https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html)
        if isinstance(double, (pd.Series, pd.DataFrame)):
            return self

        clone = copy.copy(self)
        if name:
            clone.name = name

        if double is None and clone.parameters is not None:
            double = clone.parameters.double

        param = DoubleParameter(value=double)
        clone.parameters = param
        return clone


class RiskMeasureWithListOfNumberParameter(ParameterisedRiskMeasure):
    @property
    def list_of_number(self):
        return self.parameters.values if self.parameters else None

    def __call__(self, list_of_number=None,  name=None):
        # hack to prevent ParameterisedRiskMeasure input into pandas LocIndexer as a callable function that returns
        # output for indexing (https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html)
        if isinstance(list_of_number, (pd.Series, pd.DataFrame)):
            return self

        clone = copy.copy(self)
        if name:
            clone.name = name

        if list_of_number is None and clone.parameters is not None:
            list_of_number = clone.parameters.list_of_number

        param = ListOfNumberParameter(values=list_of_number)
        clone.parameters = param
        return clone


class RiskMeasureWithListOfStringParameter(ParameterisedRiskMeasure):
    @property
    def list_of_string(self):
        return self.parameters.values if self.parameters else None

    def __call__(self, list_of_string=None,  name=None):
        # hack to prevent ParameterisedRiskMeasure input into pandas LocIndexer as a callable function that returns
        # output for indexing (https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html)
        if isinstance(list_of_string, (pd.Series, pd.DataFrame)):
            return self

        clone = copy.copy(self)
        if name:
            clone.name = name

        if list_of_string is None and clone.parameters is not None:
            list_of_string = clone.parameters.list_of_string

        param = ListOfStringParameter(values=list_of_string)
        clone.parameters = param
        return clone


class RiskMeasureWithMapParameter(ParameterisedRiskMeasure):
    @property
    def map(self):
        return self.parameters.value if self.parameters else None

    def __call__(self, map=None,  name=None):
        # hack to prevent ParameterisedRiskMeasure input into pandas LocIndexer as a callable function that returns
        # output for indexing (https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html)
        if isinstance(map, (pd.Series, pd.DataFrame)):
            return self

        clone = copy.copy(self)
        if name:
            clone.name = name

        if map is None and clone.parameters is not None:
            map = clone.parameters.map

        param = MapParameter(value=map)
        clone.parameters = param
        return clone


class RiskMeasureWithStringParameter(ParameterisedRiskMeasure):
    @property
    def string(self):
        return self.parameters.value if self.parameters else None

    def __call__(self, string=None,  name=None):
        # hack to prevent ParameterisedRiskMeasure input into pandas LocIndexer as a callable function that returns
        # output for indexing (https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html)
        if isinstance(string, (pd.Series, pd.DataFrame)):
            return self

        clone = copy.copy(self)
        if name:
            clone.name = name

        if string is None and clone.parameters is not None:
            string = clone.parameters.string

        param = StringParameter(value=string)
        clone.parameters = param
        return clone


class RiskMeasureWithFiniteDifferenceParameter(ParameterisedRiskMeasure):
    @property
    def aggregation_level(self):
        return self.parameters.aggregation_level if self.parameters else None

    @property
    def bump_size(self):
        return self.parameters.bump_size if self.parameters else None

    @property
    def currency(self):
        return self.parameters.currency if self.parameters else None

    @property
    def finite_difference_method(self):
        return self.parameters.finite_difference_method if self.parameters else None

    @property
    def local_curve(self):
        return self.parameters.local_curve if self.parameters else None

    @property
    def mkt_marking_options(self):
        return self.parameters.mkt_marking_options if self.parameters else None

    @property
    def scale_factor(self):
        return self.parameters.scale_factor if self.parameters else None

    def __call__(self, aggregation_level=None,  bump_size=None,  currency=None,  finite_difference_method=None,  local_curve=None,  mkt_marking_options=None,  scale_factor=None,  name=None):
        # hack to prevent ParameterisedRiskMeasure input into pandas LocIndexer as a callable function that returns
        # output for indexing (https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html)
        if isinstance(aggregation_level, (pd.Series, pd.DataFrame)):
            return self

        clone = copy.copy(self)
        if name:
            clone.name = name

        if aggregation_level is None and clone.parameters is not None:
            aggregation_level = clone.parameters.aggregation_level
        if bump_size is None and clone.parameters is not None:
            bump_size = clone.parameters.bump_size
        if currency is None and clone.parameters is not None:
            currency = clone.parameters.currency
        if finite_difference_method is None and clone.parameters is not None:
            finite_difference_method = clone.parameters.finite_difference_method
        if local_curve is None and clone.parameters is not None:
            local_curve = clone.parameters.local_curve
        if mkt_marking_options is None and clone.parameters is not None:
            mkt_marking_options = clone.parameters.mkt_marking_options
        if scale_factor is None and clone.parameters is not None:
            scale_factor = clone.parameters.scale_factor

        param = FiniteDifferenceParameter(aggregation_level=aggregation_level,bump_size=bump_size,currency=currency,finite_difference_method=finite_difference_method,local_curve=local_curve,mkt_marking_options=mkt_marking_options,scale_factor=scale_factor)
        clone.parameters = param
        return clone


Annuity = RiskMeasureWithCurrencyParameter(name="Annuity", asset_class=AssetClass("Rates"), measure_type=RiskMeasureType("AnnuityLocalCcy"))
Annuity.__doc__ = "Annuity"

BaseCPI = RiskMeasure(name="BaseCPI", measure_type=RiskMeasureType("BaseCPI"))
BaseCPI.__doc__ = "Base CPI"

CDATMSpread = RiskMeasure(name="CDATMSpread", asset_class=AssetClass("Credit"), measure_type=RiskMeasureType("ATM Spread"))
CDATMSpread.__doc__ = "Credit ATM Spread"

CDDelta = RiskMeasure(name="CDDelta", asset_class=AssetClass("Credit"), measure_type=RiskMeasureType("Delta"))
CDDelta.__doc__ = "Credit Delta"

CDFwdSpread = RiskMeasure(name="CDFwdSpread", asset_class=AssetClass("Credit"), measure_type=RiskMeasureType("Forward Spread"))
CDFwdSpread.__doc__ = "Credit Forward Spread"

CDGamma = RiskMeasure(name="CDGamma", asset_class=AssetClass("Credit"), measure_type=RiskMeasureType("Gamma"))
CDGamma.__doc__ = "CDIndexGamma"

CDIForward = RiskMeasure(name="CDIForward", asset_class=AssetClass("Credit"), measure_type=RiskMeasureType("CDIForward"))
CDIForward.__doc__ = "CDS Index Forward Quote in the Prevailing Quoting Style."

CDIIndexDelta = RiskMeasure(name="CDIIndexDelta", asset_class=AssetClass("Credit"), measure_type=RiskMeasureType("CDIIndexDelta"))
CDIIndexDelta.__doc__ = "CDS Index Delta."

CDIIndexVega = RiskMeasure(name="CDIIndexVega", asset_class=AssetClass("Credit"), measure_type=RiskMeasureType("CDIIndexVega"))
CDIIndexVega.__doc__ = "CDS Index Vega."

CDIOptionPremium = RiskMeasure(name="CDIOptionPremium", asset_class=AssetClass("Credit"), measure_type=RiskMeasureType("CDIOptionPremium"))
CDIOptionPremium.__doc__ = "CDS Index Option Premium"

CDIOptionPremiumFlatFwd = RiskMeasure(name="CDIOptionPremiumFlatFwd", asset_class=AssetClass("Credit"), measure_type=RiskMeasureType("CDIOptionPremiumFlatFwd"))
CDIOptionPremiumFlatFwd.__doc__ = "CDS Index Option Premium assuming Flat Forwards."

CDIOptionPremiumFlatVol = RiskMeasure(name="CDIOptionPremiumFlatVol", asset_class=AssetClass("Credit"), measure_type=RiskMeasureType("CDIOptionPremiumFlatVol"))
CDIOptionPremiumFlatVol.__doc__ = "CDS Index Option Premium assuming Flat Volatilities."

CDISpot = RiskMeasure(name="CDISpot", asset_class=AssetClass("Credit"), measure_type=RiskMeasureType("CDISpot"))
CDISpot.__doc__ = "CDS Index Spot Quote in the Prevailing Quoting Style."

CDISpreadDV01 = RiskMeasure(name="CDISpreadDV01", asset_class=AssetClass("Credit"), measure_type=RiskMeasureType("CDISpreadDV01"))
CDISpreadDV01.__doc__ = "CDS Index Rates DV01."

CDIUpfrontPrice = RiskMeasure(name="CDIUpfrontPrice", asset_class=AssetClass("Credit"), measure_type=RiskMeasureType("CDIUpfrontPrice"))
CDIUpfrontPrice.__doc__ = "CDS Index Upfront Price."

CDImpliedVolatility = RiskMeasure(name="CDImpliedVolatility", asset_class=AssetClass("Credit"), measure_type=RiskMeasureType("Implied Volatility"))
CDImpliedVolatility.__doc__ = "CDImpliedVolatility"

CDIndexVega = RiskMeasure(name="CDIndexVega", asset_class=AssetClass("Credit"), measure_type=RiskMeasureType("Vega"))
CDIndexVega.__doc__ = "CDIndexVega"

CDTheta = RiskMeasure(name="CDTheta", asset_class=AssetClass("Credit"), measure_type=RiskMeasureType("Theta"))
CDTheta.__doc__ = "CDTheta"

CDVega = RiskMeasure(name="CDVega", asset_class=AssetClass("Credit"), measure_type=RiskMeasureType("Vega"))
CDVega.__doc__ = "Credit Vega"

CRIFIRCurve = RiskMeasure(name="CRIFIRCurve", measure_type=RiskMeasureType("CRIF IRCurve"))
CRIFIRCurve.__doc__ = "CRIF IR Curve"

Cashflows = RiskMeasure(name="Cashflows", measure_type=RiskMeasureType("Cashflows"))
Cashflows.__doc__ = "Cashflows"

CommodDelta = RiskMeasure(name="CommodDelta", asset_class=AssetClass("Commod"), measure_type=RiskMeasureType("Delta"))
CommodDelta.__doc__ = "Commod Delta"

CommodImpliedVol = RiskMeasure(name="CommodImpliedVol", asset_class=AssetClass("Commod"), measure_type=RiskMeasureType("Volatility"))
CommodImpliedVol.__doc__ = "Commod Implied Volatility"

CommodTheta = RiskMeasure(name="CommodTheta", asset_class=AssetClass("Commod"), measure_type=RiskMeasureType("Theta"))
CommodTheta.__doc__ = "Commod Theta"

CommodVega = RiskMeasure(name="CommodVega", asset_class=AssetClass("Commod"), measure_type=RiskMeasureType("Vega"))
CommodVega.__doc__ = "Commod Vega"

CompoundedFixedRate = RiskMeasure(name="CompoundedFixedRate", measure_type=RiskMeasureType("Compounded Fixed Rate"))
CompoundedFixedRate.__doc__ = "CompoundedFixedRate"

Cross = RiskMeasure(name="Cross", asset_class=AssetClass("FX"), measure_type=RiskMeasureType("Cross"))
Cross.__doc__ = "Cross"

CrossMultiplier = RiskMeasure(name="CrossMultiplier", measure_type=RiskMeasureType("Cross Multiplier"))
CrossMultiplier.__doc__ = "CrossMultiplier"

Description = RiskMeasure(name="Description", measure_type=RiskMeasureType("Description"))
Description.__doc__ = "Description"

DollarPrice = RiskMeasure(name="DollarPrice", measure_type=RiskMeasureType("Dollar Price"))
DollarPrice.__doc__ = "Price of the instrument in US Dollars"

EqAnnualImpliedVol = RiskMeasure(name="EqAnnualImpliedVol", asset_class=AssetClass("Equity"), measure_type=RiskMeasureType("Annual Implied Volatility"), unit=RiskMeasureUnit("Percent"))
EqAnnualImpliedVol.__doc__ = "Equity Annual Implied Volatility (%)"

EqDelta = RiskMeasureWithCurrencyParameter(name="EqDelta", asset_class=AssetClass("Equity"), measure_type=RiskMeasureType("Delta"))
EqDelta.__doc__ = "Change in Dollar Price (USD present value) due to individual 1% move in the spot price of underlying equity security"

EqGamma = RiskMeasureWithCurrencyParameter(name="EqGamma", asset_class=AssetClass("Equity"), measure_type=RiskMeasureType("Gamma"))
EqGamma.__doc__ = "Change in EqDelta for a 1% move in the price of the underlying equity security"

EqSpot = RiskMeasure(name="EqSpot", asset_class=AssetClass("Equity"), measure_type=RiskMeasureType("Spot"))
EqSpot.__doc__ = "Equity Spot"

EqTheta = RiskMeasureWithCurrencyParameter(name="EqTheta", asset_class=AssetClass("Equity"), measure_type=RiskMeasureType("Theta"))
EqTheta.__doc__ = "Change in Dollar Price over one day"

EqVega = RiskMeasureWithCurrencyParameter(name="EqVega", asset_class=AssetClass("Equity"), measure_type=RiskMeasureType("Vega"))
EqVega.__doc__ = "Change in Dollar Price (USD present value) due to individual 1bp moves in the implied volatility of the underlying equity security"

ExpiryInYears = RiskMeasure(name="ExpiryInYears", measure_type=RiskMeasureType("ExpiryInYears"))
ExpiryInYears.__doc__ = "Time to Expiry expressed in fractional Years."

FX25DeltaButterflyVolatility = RiskMeasure(name="FX25DeltaButterflyVolatility", asset_class=AssetClass("FX"), measure_type=RiskMeasureType("FX BF 25 Vol"))
FX25DeltaButterflyVolatility.__doc__ = "The volatility of a 25 delta butterfly"

FX25DeltaRiskReversalVolatility = RiskMeasure(name="FX25DeltaRiskReversalVolatility", asset_class=AssetClass("FX"), measure_type=RiskMeasureType("FX RR 25 Vol"))
FX25DeltaRiskReversalVolatility.__doc__ = "The volatility of a 25 delta risk reversal"

FXAnnualATMImpliedVol = RiskMeasure(name="FXAnnualATMImpliedVol", asset_class=AssetClass("FX"), measure_type=RiskMeasureType("Annual ATM Implied Volatility"), unit=RiskMeasureUnit("Percent"))
FXAnnualATMImpliedVol.__doc__ = "FX Annual ATM Implied Volatility"

FXAnnualImpliedVol = RiskMeasure(name="FXAnnualImpliedVol", asset_class=AssetClass("FX"), measure_type=RiskMeasureType("Annual Implied Volatility"), unit=RiskMeasureUnit("Percent"))
FXAnnualImpliedVol.__doc__ = "FX Annual Implied Volatility"

FXBlackScholes = RiskMeasure(name="FXBlackScholes", asset_class=AssetClass("FX"), measure_type=RiskMeasureType("BSPrice"))
FXBlackScholes.__doc__ = "FXBlackScholes"

FXBlackScholesPct = RiskMeasure(name="FXBlackScholesPct", asset_class=AssetClass("FX"), measure_type=RiskMeasureType("BSPricePct"))
FXBlackScholesPct.__doc__ = "FXBlackScholes in Percent of Notional"

FXCalcDelta = RiskMeasure(name="FXCalcDelta", asset_class=AssetClass("FX"), measure_type=RiskMeasureType("FX Calculated Delta"))
FXCalcDelta.__doc__ = "FXCalcDelta"

FXCalcDeltaNoPremAdj = RiskMeasure(name="FXCalcDeltaNoPremAdj", asset_class=AssetClass("FX"), measure_type=RiskMeasureType("FX Calculated Delta No Premium Adjustment"))
FXCalcDeltaNoPremAdj.__doc__ = "FXCalcDeltaNoPremAdj"

FXDelta = RiskMeasureWithFiniteDifferenceParameter(name="FXDelta", asset_class=AssetClass("FX"), measure_type=RiskMeasureType("Delta"))
FXDelta.__doc__ = "Dollar Price sensitivity of the instrument to a move in the underlying spot such that dSpot * FXDelta = PnL"

FXDeltaHedge = RiskMeasure(name="FXDeltaHedge", asset_class=AssetClass("FX"), measure_type=RiskMeasureType("FX Hedge Delta"))
FXDeltaHedge.__doc__ = "Size of the spot trade in the underlying currency needed to hedge the USD delta on a per-cross basis"

FXDiscountFactorOver = RiskMeasure(name="FXDiscountFactorOver", asset_class=AssetClass("FX"), measure_type=RiskMeasureType("FX Discount Factor Over"))
FXDiscountFactorOver.__doc__ = "Discount Factor to Maturity in the Over Currency of the FX Pair"

FXDiscountFactorUnder = RiskMeasure(name="FXDiscountFactorUnder", asset_class=AssetClass("FX"), measure_type=RiskMeasureType("FX Discount Factor Under"))
FXDiscountFactorUnder.__doc__ = "Discount Factor to Maturity in the Under Currency of the FX Pair"

FXFwd = RiskMeasure(name="FXFwd", asset_class=AssetClass("FX"), measure_type=RiskMeasureType("Forward Rate"))
FXFwd.__doc__ = "FXFwd"

FXGamma = RiskMeasure(name="FXGamma", asset_class=AssetClass("FX"), measure_type=RiskMeasureType("Gamma"))
FXGamma.__doc__ = "FXDelta sensitivity of the instrument to a move in the underlying spot such that dSpot * FXGamma = dDelta"

FXImpliedCorrelation = RiskMeasure(name="FXImpliedCorrelation", asset_class=AssetClass("FX"), measure_type=RiskMeasureType("Correlation"))
FXImpliedCorrelation.__doc__ = "Correlation and Vol information"

FXPoints = RiskMeasure(name="FXPoints", asset_class=AssetClass("FX"), measure_type=RiskMeasureType("Points"))
FXPoints.__doc__ = "FXPoints"

FXPremium = RiskMeasure(name="FXPremium", asset_class=AssetClass("FX"), measure_type=RiskMeasureType("FX Premium"))
FXPremium.__doc__ = "FXPremium"

FXPremiumPct = RiskMeasure(name="FXPremiumPct", asset_class=AssetClass("FX"), measure_type=RiskMeasureType("FX Premium Pct"))
FXPremiumPct.__doc__ = "FXPremium in Percent of Notional"

FXPremiumPctFlatFwd = RiskMeasure(name="FXPremiumPctFlatFwd", asset_class=AssetClass("FX"), measure_type=RiskMeasureType("FX Premium Pct Flat Fwd"))
FXPremiumPctFlatFwd.__doc__ = "FXPremium in Percent of Notional in a Flat Forward environment"

FXQuotedDelta = RiskMeasure(name="FXQuotedDelta", asset_class=AssetClass("FX"), measure_type=RiskMeasureType("QuotedDelta"))
FXQuotedDelta.__doc__ = "FXQuotedDelta"

FXQuotedDeltaNoPremAdj = RiskMeasure(name="FXQuotedDeltaNoPremAdj", asset_class=AssetClass("FX"), measure_type=RiskMeasureType("FX Quoted Delta No Premium Adjustment"))
FXQuotedDeltaNoPremAdj.__doc__ = "FXQuotedDeltaNoPremAdj"

FXQuotedVega = RiskMeasure(name="FXQuotedVega", asset_class=AssetClass("FX"), measure_type=RiskMeasureType("FX Quoted Vega"))
FXQuotedVega.__doc__ = "FXQuotedVega"

FXQuotedVegaBps = RiskMeasure(name="FXQuotedVegaBps", asset_class=AssetClass("FX"), measure_type=RiskMeasureType("FX Quoted Vega"))
FXQuotedVegaBps.__doc__ = "FXQuotedVegaBps"

FXSpot = RiskMeasure(name="FXSpot", asset_class=AssetClass("FX"), measure_type=RiskMeasureType("Spot"))
FXSpot.__doc__ = "FX spot reference"

FXVega = RiskMeasureWithFiniteDifferenceParameter(name="FXVega", asset_class=AssetClass("FX"), measure_type=RiskMeasureType("Vega"))
FXVega.__doc__ = "Change in Dollar Price due to a 1 vol move in the implied volatility of ATM instruments used to build the volatility surface"

FairPremium = RiskMeasureWithCurrencyParameter(name="FairPremium", measure_type=RiskMeasureType("FairPremium"))
FairPremium.__doc__ = "Fair Premium is the instrument present value discounted to the premium settlement date"

FairPremiumInPercent = RiskMeasure(name="FairPremiumInPercent", asset_class=AssetClass("FX"), measure_type=RiskMeasureType("FairPremiumPct"), unit=RiskMeasureUnit("Percent"))
FairPremiumInPercent.__doc__ = "The instrument present value discounted to the premium settlement excluding any embedded premium date as a percentage"

FairPrice = RiskMeasure(name="FairPrice", asset_class=AssetClass("Commod"), measure_type=RiskMeasureType("Fair Price"))
FairPrice.__doc__ = "FairPrice"

FairVarStrike = RiskMeasure(name="FairVarStrike", measure_type=RiskMeasureType("FairVarStrike"))
FairVarStrike.__doc__ = "Fair Variance Strike Value of a Variance Swap"

FairVolStrike = RiskMeasure(name="FairVolStrike", measure_type=RiskMeasureType("FairVolStrike"))
FairVolStrike.__doc__ = "Fair Volatility Strike Value of a Variance Swap"

ForwardPrice = RiskMeasure(name="ForwardPrice", measure_type=RiskMeasureType("Forward Price"), unit=RiskMeasureUnit("BPS"))
ForwardPrice.__doc__ = " Price of the instrument at expiry in the local currency"

IRAnnualATMImpliedVol = RiskMeasure(name="IRAnnualATMImpliedVol", asset_class=AssetClass("Rates"), measure_type=RiskMeasureType("Annual ATMF Implied Volatility"), unit=RiskMeasureUnit("Percent"))
IRAnnualATMImpliedVol.__doc__ = "Interest rate annual implied at-the-money volatility (in percent)"

IRAnnualImpliedVol = RiskMeasure(name="IRAnnualImpliedVol", asset_class=AssetClass("Rates"), measure_type=RiskMeasureType("Annual Implied Volatility"), unit=RiskMeasureUnit("Percent"))
IRAnnualImpliedVol.__doc__ = "Interest rate annual implied volatility (in percent)"

IRBasis = RiskMeasureWithFiniteDifferenceParameter(name="IRBasis", asset_class=AssetClass("Rates"), measure_type=RiskMeasureType("Basis"))
IRBasis.__doc__ = "Change in Dollar Price (USD present value) due to individual 1bp moves in the interest rate instruments used to build the basis curve(s)"

IRDailyImpliedVol = RiskMeasure(name="IRDailyImpliedVol", asset_class=AssetClass("Rates"), measure_type=RiskMeasureType("Daily Implied Volatility"), unit=RiskMeasureUnit("BPS"))
IRDailyImpliedVol.__doc__ = "Interest rate daily implied volatility (in basis points)"

IRDelta = RiskMeasureWithFiniteDifferenceParameter(name="IRDelta", asset_class=AssetClass("Rates"), measure_type=RiskMeasureType("Delta"))
IRDelta.__doc__ = "Change in Dollar Price (USD present value) due to individual 1bp moves in the interest rate instruments used to build the underlying discount curve"

IRDiscountDeltaParallel = RiskMeasure(name="IRDiscountDeltaParallel", asset_class=AssetClass("Rates"), measure_type=RiskMeasureType("ParallelDiscountDelta"))
IRDiscountDeltaParallel.__doc__ = "Parallel Discount Delta"

IRDiscountDeltaParallelLocalCcy = RiskMeasure(name="IRDiscountDeltaParallelLocalCcy", asset_class=AssetClass("Rates"), measure_type=RiskMeasureType("ParallelDiscountDeltaLocalCcy"))
IRDiscountDeltaParallelLocalCcy.__doc__ = "Parallel Discount Delta (Local Ccy)"

IRFwdRate = RiskMeasure(name="IRFwdRate", asset_class=AssetClass("Rates"), measure_type=RiskMeasureType("Forward Rate"), unit=RiskMeasureUnit("Percent"))
IRFwdRate.__doc__ = "Interest rate par rate (in percent)"

IRGamma = RiskMeasure(name="IRGamma", asset_class=AssetClass("Rates"), measure_type=RiskMeasureType("Gamma"))
IRGamma.__doc__ = "IRGamma"

IRGammaParallel = RiskMeasure(name="IRGammaParallel", asset_class=AssetClass("Rates"), measure_type=RiskMeasureType("ParallelGamma"))
IRGammaParallel.__doc__ = "Change in aggregated IRDelta for a aggregated 1bp shift in the interest rate instruments used to build the underlying discount curve"

IRGammaParallelLocalCcy = RiskMeasure(name="IRGammaParallelLocalCcy", asset_class=AssetClass("Rates"), measure_type=RiskMeasureType("ParallelGammaLocalCcy"))
IRGammaParallelLocalCcy.__doc__ = "Interest Rate Parallel Gamma (Local Ccy)"

IRSpotRate = RiskMeasure(name="IRSpotRate", asset_class=AssetClass("Rates"), measure_type=RiskMeasureType("Spot Rate"), unit=RiskMeasureUnit("Percent"))
IRSpotRate.__doc__ = "Interest rate at-the-money spot rate (in percent)"

IRVega = RiskMeasureWithFiniteDifferenceParameter(name="IRVega", asset_class=AssetClass("Rates"), measure_type=RiskMeasureType("Vega"))
IRVega.__doc__ = "Change in Dollar Price (USD present value) due to individual 1bp moves in the implied volatility (IRAnnualImpliedVol) of instruments used to build the volatility surface"

IRXccyDelta = RiskMeasureWithFiniteDifferenceParameter(name="IRXccyDelta", asset_class=AssetClass("Rates"), measure_type=RiskMeasureType("XccyDelta"))
IRXccyDelta.__doc__ = "Change in Price due to 1bp move in cross currency rates."

InflDeltaParallelLocalCcyInBps = RiskMeasure(name="InflDeltaParallelLocalCcyInBps", asset_class=AssetClass("Rates"), measure_type=RiskMeasureType("Inflation Delta in Bps"))
InflDeltaParallelLocalCcyInBps.__doc__ = "Inflation Delta"

InflMaturityCPI = RiskMeasure(name="InflMaturityCPI", asset_class=AssetClass("Rates"), measure_type=RiskMeasureType("FinalCPI"))
InflMaturityCPI.__doc__ = "InflMaturityCPI"

Infl_CompPeriod = RiskMeasure(name="Infl_CompPeriod", asset_class=AssetClass("Rates"), measure_type=RiskMeasureType("Inflation Compounding Period"))
Infl_CompPeriod.__doc__ = "Infl_CompPeriod"

InflationDelta = RiskMeasureWithFiniteDifferenceParameter(name="InflationDelta", asset_class=AssetClass("Rates"), measure_type=RiskMeasureType("InflationDelta"))
InflationDelta.__doc__ = "Change in Price due to 1bp move in inflation curve."

LightningDV01 = RiskMeasure(name="LightningDV01", measure_type=RiskMeasureType("DV01"))
LightningDV01.__doc__ = "LightningDV01"

LightningOAS = RiskMeasure(name="LightningOAS", measure_type=RiskMeasureType("OAS"))
LightningOAS.__doc__ = "LightningOAS"

LocalAnnuityInCents = RiskMeasure(name="LocalAnnuityInCents", asset_class=AssetClass("Rates"), measure_type=RiskMeasureType("Local Currency Accrual in Cents"))
LocalAnnuityInCents.__doc__ = "Local Currency Accrual in Cents"

Market = RiskMeasure(name="Market", measure_type=RiskMeasureType("Market"))
Market.__doc__ = "Market"

MarketData = RiskMeasure(name="MarketData", measure_type=RiskMeasureType("Market Data"))
MarketData.__doc__ = "Market Data"

MarketDataAssets = RiskMeasure(name="MarketDataAssets", measure_type=RiskMeasureType("Market Data Assets"))
MarketDataAssets.__doc__ = "MarketDataAssets"

NonUSDOisDomRate = RiskMeasure(name="NonUSDOisDomRate", asset_class=AssetClass("FX"), measure_type=RiskMeasureType("NonUSDOisDomesticRate"))
NonUSDOisDomRate.__doc__ = "NonUSDOisDomRate"

OisFXSprExSpkRate = RiskMeasure(name="OisFXSprExSpkRate", asset_class=AssetClass("FX"), measure_type=RiskMeasureType("OisFXSpreadRateExcludingSpikes"))
OisFXSprExSpkRate.__doc__ = "OisFXSprExSpkRate"

OisFXSprRate = RiskMeasure(name="OisFXSprRate", asset_class=AssetClass("FX"), measure_type=RiskMeasureType("OisFXSpreadRate"))
OisFXSprRate.__doc__ = "OisFXSprRate"

ParSpread = RiskMeasure(name="ParSpread", asset_class=AssetClass("Rates"), measure_type=RiskMeasureType("Spread"))
ParSpread.__doc__ = "Par Spread"

PremiumCents = RiskMeasure(name="PremiumCents", asset_class=AssetClass("Rates"), measure_type=RiskMeasureType("Premium In Cents"))
PremiumCents.__doc__ = "PremiumCents"

PremiumSummary = RiskMeasure(name="PremiumSummary", asset_class=AssetClass("Commod"), measure_type=RiskMeasureType("Premium"))
PremiumSummary.__doc__ = "PremiumSummary"

Price = RiskMeasureWithCurrencyParameter(name="Price", measure_type=RiskMeasureType("PV"))
Price.__doc__ = "Present Value"

PricePips = RiskMeasureWithCurrencyParameter(name="PricePips", measure_type=RiskMeasureType("Price"), unit=RiskMeasureUnit("Pips"))
PricePips.__doc__ = "Present value in pips"

ProbabilityOfExercise = RiskMeasure(name="ProbabilityOfExercise", measure_type=RiskMeasureType("Probability Of Exercise"))
ProbabilityOfExercise.__doc__ = "Probability Of Exercise"

RFRFXRate = RiskMeasure(name="RFRFXRate", asset_class=AssetClass("FX"), measure_type=RiskMeasureType("RFRFXRate"))
RFRFXRate.__doc__ = "RFRFXRate"

RFRFXSprExSpkRate = RiskMeasure(name="RFRFXSprExSpkRate", asset_class=AssetClass("FX"), measure_type=RiskMeasureType("RFRFXSpreadRateExcludingSpikes"))
RFRFXSprExSpkRate.__doc__ = "RFRFXSprExSpkRate"

RFRFXSprRate = RiskMeasure(name="RFRFXSprRate", asset_class=AssetClass("FX"), measure_type=RiskMeasureType("RFRFXSpreadRate"))
RFRFXSprRate.__doc__ = "RFRFXSprRate"

ResolvedInstrumentValues = RiskMeasure(name="ResolvedInstrumentValues", measure_type=RiskMeasureType("Resolved Instrument Values"))
ResolvedInstrumentValues.__doc__ = "Resolved InstrumentBase Values"

Theta = RiskMeasure(name="Theta", measure_type=RiskMeasureType("Theta"))
Theta.__doc__ = "Theta"

USDOisDomRate = RiskMeasure(name="USDOisDomRate", asset_class=AssetClass("FX"), measure_type=RiskMeasureType("USDOisDomesticRate"))
USDOisDomRate.__doc__ = "USDOisDomRate"

