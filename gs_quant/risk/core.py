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
from typing import Iterable, List, Mapping, Union
from gs_quant.target.risk import RiskMeasure, RiskMeasureType, RiskMeasureUnit, RiskPosition, RiskRequest
from gs_quant.base import Priceable
from gs_quant.common import AssetClass
from gs_quant.markets.core import MarketDataCoordinate
from gs_quant.context_base import ContextBaseWithDefault
from gs_quant.markets import MarketDataContext
from typing import Optional


def sum_formatter(result: List) -> float:
    return sum(r.get('value', result[0].get('Val')) for r in result)


def scalar_formatter(result: List) -> float:
    return result[0].get('value', result[0].get('Val'))


def structured_formatter(result: List) -> pd.DataFrame:
    return pd.DataFrame(result)


def aggregate_risk(results: Iterable[Union[pd.DataFrame, Future]], threshold: Optional[float]=None) -> pd.DataFrame:
    """
    Combine the results of multiple Instrument.calc() calls, into a single result

    :param results: An iterable of Dataframes and/or Futures (returned by Instrument.calc())
    :param threshold: exclude values whose absolute value falls below this threshold
    :return: A Dataframe with the aggregated results

    **Examples**

    >>> with PricingContext():
    >>>     delta_f = [inst.calc(risk.IRDelta) for inst in instruments]
    >>>     vega_f = [inst.calc(risk.IRVega) for inst in instruments]
    >>>
    >>> delta = aggregate_risk(delta_f, threshold=0.1)
    >>> vega = aggregate_risk(vega_f)

    delta_f and vega_f are lists of futures, where the result will be a Dataframe
    delta and vega are Dataframes, representing the merged risk of the individual instruments
    """
    dfs = [r.result() if isinstance(r, Future) else r for r in results]
    result = pd.concat(dfs)
    result = result.groupby([c for c in result.columns if c != 'value']).sum()
    result = pd.DataFrame.from_records(result.to_records())

    if threshold is not None:
        result = result[result.value.abs() > threshold]

    return result


def __risk_measure_with_doc_string(doc: str, measureType: RiskMeasureType, assetClass: AssetClass=None, unit: RiskMeasureUnit=None) -> RiskMeasure:
    measure = RiskMeasure(measureType=measureType, assetClass=assetClass, unit=unit)
    measure.__doc__ = doc
    return measure


DollarPrice = __risk_measure_with_doc_string('Present value in USD', RiskMeasureType.Dollar_Price)
Price = __risk_measure_with_doc_string('Present value in local currency', RiskMeasureType.PV)
ForwardPrice = __risk_measure_with_doc_string('Forward price', RiskMeasureType.Forward_Price, unit=RiskMeasureUnit.BPS)
Theta = __risk_measure_with_doc_string('1 day Theta', RiskMeasureType.Theta)
EqDelta = __risk_measure_with_doc_string('Equity Delta', RiskMeasureType.Delta, assetClass=AssetClass.Equity)
EqGamma = __risk_measure_with_doc_string('Equity Gamma', RiskMeasureType.Gamma, assetClass=AssetClass.Equity)
EqVega = __risk_measure_with_doc_string('Equity Vega', RiskMeasureType.Vega, assetClass=AssetClass.Equity)
EqSpot = __risk_measure_with_doc_string('Equity Spot Level', RiskMeasureType.Spot, assetClass=AssetClass.Equity)
CommodDelta = __risk_measure_with_doc_string('Commodity Delta', RiskMeasureType.Delta, assetClass=AssetClass.Commod)
CommodTheta = __risk_measure_with_doc_string('Commodity Theta', RiskMeasureType.Theta, assetClass=AssetClass.Commod)
CommodVega = __risk_measure_with_doc_string('Commodity Vega', RiskMeasureType.Vega, assetClass=AssetClass.Commod)
FXDelta = __risk_measure_with_doc_string('FX Delta', RiskMeasureType.Delta, assetClass=AssetClass.FX)
FXGamma = __risk_measure_with_doc_string('FX Gamma', RiskMeasureType.Gamma, assetClass=AssetClass.FX)
FXVega = __risk_measure_with_doc_string('FX Vega', RiskMeasureType.Vega, assetClass=AssetClass.FX)
FXSpot = __risk_measure_with_doc_string('FX Spot Rate', RiskMeasureType.Spot, assetClass=AssetClass.FX)
IRDelta = __risk_measure_with_doc_string('Interest Rate Delta', RiskMeasureType.Delta, assetClass=AssetClass.Rates)
IRGamma = __risk_measure_with_doc_string('Interest Rate', RiskMeasureType.Gamma, assetClass=AssetClass.Rates)
IRVega = __risk_measure_with_doc_string('Interest Rate', RiskMeasureType.Vega, assetClass=AssetClass.Rates)
IRAnnualImpliedVol = __risk_measure_with_doc_string('Interest Rate Annual Implied Volatility (%)', RiskMeasureType.Annual_Implied_Volatility, assetClass=AssetClass.Rates, unit=RiskMeasureUnit.Percent)
IRAnnualATMImpliedVol = __risk_measure_with_doc_string('Interest Rate Annual Implied At-The-Money Volatility (%)', RiskMeasureType.Annual_ATMF_Implied_Volatility, assetClass=AssetClass.Rates, unit=RiskMeasureUnit.Percent)
IRDailyImpliedVol = __risk_measure_with_doc_string('Interest Rate Daily Implied Volatility (bps)', RiskMeasureType.Annual_ATMF_Implied_Volatility, assetClass=AssetClass.Rates, unit=RiskMeasureUnit.Percent)

Formatters = {
    DollarPrice: scalar_formatter,
    Price: scalar_formatter,
    ForwardPrice: scalar_formatter,
    Theta: scalar_formatter,
    EqDelta: scalar_formatter,
    EqGamma: scalar_formatter,
    EqVega: sum_formatter,
    EqSpot: scalar_formatter,
    CommodDelta: structured_formatter,
    CommodVega: structured_formatter,
    CommodTheta: structured_formatter,
    FXDelta: structured_formatter,
    FXGamma: structured_formatter,
    FXVega: structured_formatter,
    FXSpot: scalar_formatter,
    IRDelta: structured_formatter,
    IRGamma: structured_formatter,
    IRVega: structured_formatter,
    IRAnnualImpliedVol: scalar_formatter,
    IRDailyImpliedVol: scalar_formatter,
    IRAnnualATMImpliedVol: scalar_formatter
}


class PricingContext(ContextBaseWithDefault):

    """
    A context controlling pricing and risk calculation behaviour
    """

    def __init__(self, is_async: bool=False, is_batch: bool=False, pricing_date: dt.date=None):
        """
        Construct a context to control the pricing date, async behaviour etc

        The methods on this class should not be called directly. Instead, use the methods on the instruments, as per the examples

        :param is_async: if True, return (a future) immediately. If False, block
        :param is_batch: use for calculations expected to run longer than 3 mins, to avoid timeouts. It can be used with is_aync=True|False
        :param pricing_date: the date for pricing calculations. Default is today

        **Examples**

        To change the behaviour of the default context:

        >>> from gs_quant.risk import PricingContext
        >>> import datetime as dt
        >>>
        >>> PricingContext.current = PricingContext(pricing_date=dt.today())

        For a blocking, synchronous request:

        >>> from gs_quant.instrument import IRCap
        >>> cap = IRCap('5y', 'GBP')
        >>>
        >>> with PricingContext():
        >>>     price_f = cap.dollar_price()
        >>>
        >>> price = price_f.result()

        For an asynchronous request:

        >>> with PricingContext(is_async=True):
        >>>     price_f = inst.dollar_price()
        >>>
        >>> while not price_f.done():
        >>>     ...
        """
        super().__init__()
        self.__is_async = is_async
        self.__is_batch = is_batch
        self.__pricing_date = pricing_date or dt.date.today()
        self.__risk_measures_by_provider_and_priceable = {}
        self.__futures = {}

    def _on_exit(self, exc_type, exc_val, exc_tb):
        if self.__risk_measures_by_provider_and_priceable:
            for provider, risk_measures_by_priceable in self.__risk_measures_by_provider_and_priceable.items():
                positions_by_risk_measures = {}
                for priceable, risk_measures in risk_measures_by_priceable.items():
                    positions_by_risk_measures.setdefault(tuple(risk_measures), []).append(priceable)

                for risk_measures, priceables in positions_by_risk_measures.items():
                    risk_request = RiskRequest(
                        tuple(RiskPosition(p, p.get_quantity()) for p in priceables),
                        risk_measures,
                        self.pricing_date,
                        marketDataAsOf=MarketDataContext.current.as_of,
                        pricingLocation=MarketDataContext.current.location
                    )
                    provider.calc(risk_request, self.__futures, self.__is_async, self.__is_batch)

            self.__risk_measures_by_provider_and_priceable.clear()
            self.__futures.clear()

    @property
    def pricing_date(self) -> dt.date:
        """Pricing date"""
        return self.__pricing_date

    def calc(self, priceable: Priceable, risk_measure: RiskMeasure) -> Union[dict, Future]:
        """
        Calculate the risk measure for the priceable instrument. Do not use directly, use via instruments

        :param priceable: The priceable (e.g. instrument)
        :param risk_measure: The measure we wish to calculate
        :return: A dict or Future (depending on is_async or whether the context is entered). Formatters may choose to convert to e.g. a float or Dataframe

        **Examples**

        >>> from gs_quant.instrument import IRSwap
        >>> from gs_quant.risk import IRDelta
        >>>
        >>> swap = IRSwap('Pay', '10y', 'USD', fixedRate=0.03)
        >>> delta = swap.calc(IRDelta)
        """
        if not self._is_entered and not self.__is_async:
            future = Future()
            futures = {risk_measure: {priceable: future}}
            risk_request = RiskRequest(
                (RiskPosition(priceable, priceable.get_quantity()),),
                (risk_measure,),
                self.pricing_date,
                marketDataAsOf=MarketDataContext.current.as_of,
                pricingLocation=MarketDataContext.current.location
            )
            priceable.provider().calc(risk_request, futures, False, False)
            return future.result()
        else:
            future = self.__futures.get(risk_measure, {}).get(priceable)
            if future is None:
                future = Future()
                self.__risk_measures_by_provider_and_priceable.setdefault(priceable.provider(), {}).setdefault(priceable, set()).add(risk_measure)
                self.__futures.setdefault(risk_measure, {})[priceable] = future
            return future

    def resolve_fields(self, priceable: Priceable):
        """
        Resolve fields on the priceable which were not supplied. Do not use directly, use via instruments

        :param priceable:  The priceable (e.g. instrument)

        **Examples**

        >>> from gs_quant.instrument import IRSwap
        >>>
        >>> swap = IRSwap('Pay', '10y', 'USD')
        >>> rate = swap.fixedRate

        fixedRate is None

        >>> swap.resolve()
        >>> rate = swap.fixedRate

        fixedRate is now the solved value
        """
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
