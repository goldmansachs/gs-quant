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
from copy import copy
from typing import Iterable, List, Optional, Tuple, Union

import dateutil
import pandas as pd

from gs_quant.common import AssetClass
from gs_quant.datetime import point_sort_order
from gs_quant.markets.core import PricingContext
from gs_quant.markets.historical import HistoricalPricingContext
from gs_quant.target.risk import RiskMeasure, RiskMeasureType, RiskMeasureUnit

__column_sort_fns = {
    'label1': point_sort_order,
    'mkt_point': point_sort_order,
    'point': point_sort_order
}
__risk_columns = ('date', 'time', 'marketDataType', 'assetId', 'pointClass', 'point')
__crif_columns = ('date', 'time', 'riskType', 'amountCurrency', 'qualifier', 'bucket', 'label1', 'label2')


def sum_formatter(result: List) -> float:
    return sum(r.get('value', result[0].get('Val')) for r in result)


def __flatten_result(item: Union[List, Tuple]):
    rows = []
    for elem in item:
        if isinstance(elem, (list, tuple)):
            rows.extend(__flatten_result(elem))
        else:
            excluded_fields = ['calculationTime', 'queueingTime']
            if not issubclass(PricingContext.current.__class__, HistoricalPricingContext):
                excluded_fields.append('date')
            else:
                date = elem.get('date')
                if date is not None:
                    elem['date'] = dateutil.parser.isoparse(date).date()

            for field in excluded_fields:
                if field in elem:
                    elem.pop(field)

            rows.append(elem)

    return rows


def scalar_formatter(result: List) -> Optional[Union[float, pd.Series]]:
    if not result:
        return None

    result = __flatten_result(result)

    if len(result) > 1 and 'date' in result[0]:
        series = pd.Series(
            data=[r.get('value', r.get('Val')) for r in result],
            index=[r['date'] for r in result]
        )
        return series.sort_index()
    else:
        return result[0].get('value', result[0].get('Val'))


def structured_formatter(result: List) -> Optional[pd.DataFrame]:
    if not result:
        return None

    return sort_risk(pd.DataFrame.from_records(__flatten_result(result)))


def crif_formatter(result: List) -> Optional[pd.DataFrame]:
    if not result:
        return None

    return sort_risk(pd.DataFrame.from_records(__flatten_result(result)), __crif_columns)


def aggregate_risk(results: Iterable[Union[pd.DataFrame, Future]], threshold: Optional[float] = None) -> pd.DataFrame:
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

    return sort_risk(result)


def aggregate_results(results: Iterable[Union[dict, float, str, pd.DataFrame, pd.Series]])\
        -> Union[dict, float, str, pd.DataFrame, pd.Series]:
    types = set(type(r) for r in results)
    if str in types:
        return next(r for r in results if isinstance(r, str))
    elif len(types) > 1:
        raise RuntimeError('Cannot aggregate heterogeneous types: {}'.format(tuple(types)))

    inst = next(iter(results))
    if isinstance(inst, dict):
        return dict((k, aggregate_results([r[k] for r in results])) for k in inst.keys())
    elif isinstance(inst, (float, pd.Series)):
        return sum(results)
    elif isinstance(inst, pd.DataFrame):
        return aggregate_risk(results)


def subtract_risk(left: pd.DataFrame, right: pd.DataFrame) -> pd.DataFrame:
    """Subtract bucketed risk. Dimensions must be identical

    :param left: Results to substract from
    :param right: Results to substract

    **Examples**

    >>> ir_swap = IRSwap('Pay', '10y', 'USD')
    >>> delta_today = ir_swap.calc(risk.IRDelta)
    >>>
    >>> with PricingContext(pricing_date=business_day_offset(datetime.date.today(), -1, roll='preceding')):
    >>>     delta_yday_f = ir_swap.calc(risk.IRDelta)
    >>>
    >>> delta_diff = subtract_risk(delta_today, delta_yday_f.result())
    """
    assert(left.columns.names == right.columns.names)
    assert('value' in left.columns.names)

    right_negated = copy(right)
    right_negated.value *= -1

    return aggregate_risk((left, right_negated))


def sort_risk(df: pd.DataFrame, by: Tuple[str, ...] = __risk_columns) -> pd.DataFrame:
    """
    Sort bucketed risk

    :param df: Input Dataframe
    :param by: Columns to sort by
    :return: A sorted Dataframe
    """
    columns = tuple(df.columns)
    indices = [columns.index(c) if c in columns else -1 for c in by]
    fns = [__column_sort_fns.get(c) for c in columns]

    def cmp(row) -> tuple:
        return tuple(fns[i](row[i]) if fns[i] else row[i] for i in indices if i != -1)

    data = sorted((tuple(r)[1:] for r in df.to_records()), key=cmp)
    fields = [f for f in by if f in columns]
    fields.extend(f for f in columns if f not in fields)

    result = pd.DataFrame.from_records(data, columns=columns)[fields]
    if 'date' in result:
        result = result.set_index('date')

    return result


def __risk_measure_with_doc_string(
    name: str,
    doc: str,
    measure_type: RiskMeasureType,
    asset_class: Optional[AssetClass] = None,
    unit: Optional[RiskMeasureUnit] = None
) -> RiskMeasure:
    measure = RiskMeasure(measure_type=measure_type, asset_class=asset_class, unit=unit, name=name)
    measure.__doc__ = doc
    return measure


DollarPrice = __risk_measure_with_doc_string('DollarPrice', 'Present value in USD', RiskMeasureType.Dollar_Price)
Price = __risk_measure_with_doc_string('Price', 'Present value in local currency', RiskMeasureType.PV)
ForwardPrice = __risk_measure_with_doc_string(
    'ForwardPrice',
    'Forward price',
    RiskMeasureType.Forward_Price,
    unit=RiskMeasureUnit.BPS)
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
FXDelta = __risk_measure_with_doc_string('FXDelta', 'FX Delta', RiskMeasureType.Delta, asset_class=AssetClass.FX)
FXGamma = __risk_measure_with_doc_string('FXGamma', 'FX Gamma', RiskMeasureType.Gamma, asset_class=AssetClass.FX)
FXVega = __risk_measure_with_doc_string('FXVega', 'FX Vega', RiskMeasureType.Vega, asset_class=AssetClass.FX)
FXSpot = __risk_measure_with_doc_string('FXSpot', 'FX Spot Rate', RiskMeasureType.Spot, asset_class=AssetClass.FX)
IRDelta = __risk_measure_with_doc_string(
    'IRDelta',
    'Interest Rate Delta',
    RiskMeasureType.Delta,
    asset_class=AssetClass.Rates)
IRDeltaParallel = __risk_measure_with_doc_string(
    'IRDeltaParallel',
    'Interest Rate Parallel Delta',
    RiskMeasureType.ParallelDelta,
    asset_class=AssetClass.Rates)
IRDeltaLocalCcy = __risk_measure_with_doc_string(
    'IRDeltaLocalCcy',
    'Interest Rate Delta (Local Ccy)',
    RiskMeasureType.DeltaLocalCcy,
    asset_class=AssetClass.Rates)
IRDeltaParallelLocalCcy = __risk_measure_with_doc_string(
    'IRDeltaParallelLocalCcy',
    'Interest Rate Parallel Delta (Local Ccy)',
    RiskMeasureType.ParallelDeltaLocalCcy,
    asset_class=AssetClass.Rates)
IRGamma = __risk_measure_with_doc_string(
    'IRGamma',
    'Interest Rate Gamma',
    RiskMeasureType.Gamma,
    asset_class=AssetClass.Rates)
IRVega = __risk_measure_with_doc_string(
    'IRVega',
    'Interest Rate Vega',
    RiskMeasureType.Vega,
    asset_class=AssetClass.Rates)
IRVegaParallel = __risk_measure_with_doc_string(
    'IRVegaParallel',
    'Interest Rate Parallel Vega',
    RiskMeasureType.ParallelVega,
    asset_class=AssetClass.Rates)
IRVegaLocalCcy = __risk_measure_with_doc_string(
    'IRVegaLocalCcy',
    'Interest Rate Vega (Local Ccy)',
    RiskMeasureType.VegaLocalCcy,
    asset_class=AssetClass.Rates)
IRVegaParallelLocalCcy = __risk_measure_with_doc_string(
    'IRVegaParallelLocalCcy',
    'Interest Rate Parallel Vega (Local Ccy)',
    RiskMeasureType.ParallelVegaLocalCcy,
    asset_class=AssetClass.Rates)
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
    RiskMeasureType.Annual_ATMF_Implied_Volatility,
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
CRIFIRCurve = __risk_measure_with_doc_string(
    'CRIFIRCurve',
    'CRIF IR Curve',
    RiskMeasureType.CRIF_IRCurve)

Formatters = {
    DollarPrice: scalar_formatter,
    Price: scalar_formatter,
    ForwardPrice: scalar_formatter,
    Theta: scalar_formatter,
    EqDelta: scalar_formatter,
    EqGamma: scalar_formatter,
    EqVega: sum_formatter,
    EqSpot: scalar_formatter,
    EqAnnualImpliedVol: scalar_formatter,
    CommodDelta: scalar_formatter,
    CommodVega: scalar_formatter,
    CommodTheta: scalar_formatter,
    FairVarStrike: scalar_formatter,
    FairVolStrike: scalar_formatter,
    FXDelta: structured_formatter,
    FXGamma: structured_formatter,
    FXVega: structured_formatter,
    FXSpot: scalar_formatter,
    IRDelta: structured_formatter,
    IRDeltaParallel: scalar_formatter,
    IRDeltaLocalCcy: structured_formatter,
    IRDeltaParallelLocalCcy: scalar_formatter,
    IRGamma: structured_formatter,
    IRVega: structured_formatter,
    IRVegaParallel: scalar_formatter,
    IRVegaLocalCcy: structured_formatter,
    IRVegaParallelLocalCcy: scalar_formatter,
    IRAnnualImpliedVol: scalar_formatter,
    IRDailyImpliedVol: scalar_formatter,
    IRAnnualATMImpliedVol: scalar_formatter,
    IRSpotRate: scalar_formatter,
    IRFwdRate: scalar_formatter,
    CRIFIRCurve: crif_formatter
}
