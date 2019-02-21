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
from concurrent.futures import Future
import datetime as dt
import pandas as pd
from typing import List, Mapping
from gs_quant.target.risk import *
from gs_quant.base import Priceable
from gs_quant.common import AssetClass, MarketDataCoordinate
from gs_quant.context_base import ContextBaseWithDefault
from gs_quant.datetime.date import business_day_offset


def scalar_formatter(result: List) -> float:
    return result[0].get('value', result[0].get('Val'))


def structured_formatter(result: List) -> pd.DataFrame:
    df = pd.DataFrame(result)
    del df['field']
    return df


DollarPrice = RiskMeasure(measureType=RiskMeasureType.Dollar_Price)
Price = RiskMeasure(measureType=RiskMeasureType.Price)
PresentValue = Price
ForwardPrice = RiskMeasure(measureType='Forward Price', unit=RiskMeasureUnit.BPS)
Theta = RiskMeasure(measureType=RiskMeasureType.Theta)
EqDelta = RiskMeasure(measureType=RiskMeasureType.Delta, assetClass=AssetClass.Equity)
EqGamma = RiskMeasure(measureType=RiskMeasureType.Gamma, assetClass=AssetClass.Equity)
EqVega = RiskMeasure(measureType=RiskMeasureType.Vega, assetClass=AssetClass.Equity)
CommodDelta = RiskMeasure(measureType=RiskMeasureType.Delta, assetClass=AssetClass.Commod)
CommodVega = RiskMeasure(measureType=RiskMeasureType.Vega, assetClass=AssetClass.Commod)
CommodTheta = RiskMeasure(measureType=RiskMeasureType.Theta, assetClass=AssetClass.Commod)
FXDelta = RiskMeasure(measureType=RiskMeasureType.Delta, assetClass=AssetClass.FX)
FXGamma = RiskMeasure(measureType=RiskMeasureType.Gamma, assetClass=AssetClass.FX)
FXVega = RiskMeasure(measureType=RiskMeasureType.Vega, assetClass=AssetClass.FX)
IRDelta = RiskMeasure(measureType=RiskMeasureType.Delta, assetClass=AssetClass.Rates)
IRGamma = RiskMeasure(measureType=RiskMeasureType.Gamma, assetClass=AssetClass.Rates)
IRVega = RiskMeasure(measureType=RiskMeasureType.Vega, assetClass=AssetClass.Rates)
IRAnnualImpliedVol = RiskMeasure(measureType=RiskMeasureType.Annual_Implied_Volatility, assetClass=AssetClass.Rates, unit=RiskMeasureUnit.Percent)
IRAnnualATMImpliedVol = RiskMeasure(measureType=RiskMeasureType.Annual_ATMF_Implied_Volatility, assetClass=AssetClass.Rates, unit=RiskMeasureUnit.Percent)
IRDailyImpliedVol = RiskMeasure(measureType=RiskMeasureType.Daily_Implied_Volatility, assetClass=AssetClass.Rates, unit=RiskMeasureUnit.BPS)

Formatters = {
    DollarPrice: scalar_formatter,
    Price: scalar_formatter,
    PresentValue: scalar_formatter,
    ForwardPrice: scalar_formatter,
    Theta: scalar_formatter,
    EqDelta: scalar_formatter,
    EqGamma: scalar_formatter,
    EqVega: scalar_formatter,
    CommodDelta: structured_formatter,
    CommodVega: structured_formatter,
    CommodTheta: structured_formatter,
    FXDelta: structured_formatter,
    FXGamma: structured_formatter,
    FXVega: structured_formatter,
    IRDelta: structured_formatter,
    IRGamma: structured_formatter,
    IRVega: structured_formatter,
    IRAnnualImpliedVol: scalar_formatter,
    IRDailyImpliedVol: scalar_formatter
}


class PricingContext(ContextBaseWithDefault):

    """A context containing pricing parameters such as date"""

    def __init__(self, is_async: bool=False, is_batch: bool=False, pricing_date: dt.date=None):
        super().__init__()
        self.__is_async = is_async
        self.__is_batch = is_batch
        self.__pricing_date = pricing_date or business_day_offset(dt.date.today(), -1, roll='preceding')
        self.__risk_measures_by_provider_and_priceable = {}
        self.__futures = {}

    def _on_exit(self, exc_type, exc_val, exc_tb):
        if self.__risk_measures_by_provider_and_priceable:
            for provider, risk_measures_by_priceable in self.__risk_measures_by_provider_and_priceable.items():
                positions_by_risk_measures = {}
                for priceable, risk_measures in risk_measures_by_priceable.items():
                    positions_by_risk_measures.setdefault(tuple(risk_measures), []).append(priceable)

                for risk_measures, priceables in positions_by_risk_measures.items():
                    risk_request = RiskRequest([RiskPosition(p, 1) for p in priceables], risk_measures, self.pricing_date)
                    provider.calc(risk_request, self.__futures, self.__is_async, self.__is_batch)

            self.__risk_measures_by_provider_and_priceable.clear()
            self.__futures.clear()

    @property
    def pricing_date(self) -> dt.date:
        """Pricing date"""
        return self.__pricing_date

    @pricing_date.setter
    def pricing_date(self, value: dt.date):
        """Set pricing date"""
        self.__pricing_date = value

    def calc(self, priceable: Priceable, risk_measure: RiskMeasure) -> Union[dict, Future]:
        """Calculate the risk measure"""
        if not self._is_entered:
            future = Future()
            futures = {risk_measure: {priceable: future}}
            risk_request = RiskRequest((RiskPosition(priceable, 1),), (risk_measure,), self.pricing_date)
            priceable.provider().calc(risk_request, futures, False, False)
            return future.result()
        else:
            future = Future()
            self.__risk_measures_by_provider_and_priceable.setdefault(priceable.provider(), {}).setdefault(priceable, set()).add((risk_measure))
            self.__futures.setdefault(risk_measure, {})[priceable] = future
            return future

    def resolve_fields(self, priceable: Priceable):
        # TODO Handle these correctly in the risk service
        invalid_defaults = ('-- N/A --',)
        value_mappings = {'Payer': 'Pay', 'Receiver': 'Receive'}

        def set_field_values(field_values):
            if isinstance(res, Future):
                field_values = field_values.result()

            for field, value in field_values.items():
                value = value_mappings.get(value, value)
                if field in priceable.properties() and value not in invalid_defaults:
                    setattr(priceable, field, value)

        res = self.calc(priceable, RiskMeasure(measureType='Resolved Instrument Values'))
        if isinstance(res, Future):
            res.add_done_callback(set_field_values)
        else:
            set_field_values(res)


class MarketDataContext(ContextBaseWithDefault):

    """A context containing market data parameters, such as as_of date/time and overrides"""

    def __init__(self, as_of: Union[dt.date, dt.datetime]=None, overrides: Mapping[MarketDataCoordinate, float]=None):
        super().__init__()
        self.__as_of = as_of or business_day_offset(dt.date.today(), -1, roll='preceding')
        self.__overrides = overrides or {}

    @property
    def as_of(self):
        return self.__as_of

    @property
    def overrides(self):
        return self.__overrides


class ScenarioContext(ContextBaseWithDefault):

    """A context containing scenario parameters, such as shocks"""

    def __init__(self, subtract_base: bool=True, shocks: Mapping[MarketDataCoordinate, float]=None):
        super().__init__()
        self.__subtract_base = subtract_base
        self.__shocks = shocks or {}

    @property
    def subtract_base(self):
        return self.__subtract_base

    @property
    def shocks(self):
        return self.__shocks
