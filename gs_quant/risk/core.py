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
from abc import ABCMeta, abstractmethod
from concurrent.futures import Future
from copy import copy
import datetime as dt
from typing import Iterable, List, Optional, Tuple, Union

import dateutil
import pandas as pd

from gs_quant.base import InstrumentBase, PricingKey
from gs_quant.common import AssetClass
from gs_quant.datetime import point_sort_order
from gs_quant.target.risk import RiskMeasure, RiskMeasureType, RiskMeasureUnit, \
    PricingDateAndMarketDataAsOf as __PricingDateAndMarketDataAsOf

__column_sort_fns = {
    'label1': point_sort_order,
    'mkt_point': point_sort_order,
    'point': point_sort_order
}
__risk_columns = ('date', 'time', 'marketDataType', 'assetId', 'pointClass', 'point')
__crif_columns = ('date', 'time', 'riskType', 'amountCurrency', 'qualifier', 'bucket', 'label1', 'label2')
__cashflows_columns = ('payment_date', 'payment_type', 'accrual_start_date', 'accrual_end_date', 'floating_rate_option',
                       'floating_rate_designated_maturity')
__assets_columns = ('date', 'mktType', 'mktAsset')


class RiskResult:

    def __init__(self, result, risk_measures: Iterable[RiskMeasure]):
        self.__risk_measures = tuple(risk_measures)
        self.__result = result

    @property
    def done(self) -> bool:
        return self.__result.done()

    @property
    def risk_measures(self) -> Tuple[RiskMeasure]:
        return self.__risk_measures

    @property
    def _result(self):
        return self.__result


class ResultInfo(metaclass=ABCMeta):

    def __init__(
        self,
        pricing_key: PricingKey,
        unit: Optional[str] = None,
        error: Optional[Union[str, dict]] = None,
        calculation_time: Optional[int] = None,
        queueing_time: Optional[int] = None
    ):
        self.__pricing_key = pricing_key
        self.__unit = unit
        self.__error = error
        self.__calculation_time = calculation_time
        self.__queueing_time = queueing_time

    @property
    @abstractmethod
    def raw_value(self):
        ...

    @property
    def pricing_key(self) -> PricingKey:
        return self.__pricing_key

    @property
    def unit(self) -> str:
        """The units of this result"""
        return self.__unit

    @property
    def error(self) -> Union[str, dict]:
        """Any error associated with this result"""
        return self.__error

    @property
    def calculation_time(self) -> int:
        """The time (in milliseconds) taken to compute this result"""
        return self.__calculation_time

    @property
    def queueing_time(self) -> int:
        """The time (in milliseconds) for which this computation was queued"""
        return self.__queueing_time

    @abstractmethod
    def for_pricing_key(self, pricing_key: PricingKey):
        ...


class ErrorValue(ResultInfo):

    def __init__(self, pricing_key: PricingKey, error: Union[str, dict]):
        super().__init__(pricing_key, error=error)

    def __repr__(self):
        return self.error

    @property
    def raw_value(self):
        return None

    def for_pricing_key(self, pricing_key: PricingKey):
        return self if pricing_key == self.pricing_key else None


class ScalarWithInfo(ResultInfo, metaclass=ABCMeta):

    def __init__(
            self,
            pricing_key: PricingKey,
            value: Union[float, str],
            unit: Optional[str] = None,
            error: Optional[Union[str, dict]] = None,
            calculation_time: Optional[float] = None,
            queueing_time: Optional[float] = None):
        float.__init__(value)
        ResultInfo.__init__(
            self,
            pricing_key,
            unit=unit,
            error=error,
            calculation_time=calculation_time,
            queueing_time=queueing_time)

    @property
    @abstractmethod
    def raw_value(self):
        ...

    def for_pricing_key(self, pricing_key: PricingKey):
        return self if pricing_key == self.pricing_key else None

    @staticmethod
    def compose(components, pricing_key: Optional[PricingKey] = None):
        unit = None
        error = {}
        as_of = ()
        dates = []
        values = []
        generated_pricing_key = None

        for component in components:
            generated_pricing_key = component.pricing_key
            unit = unit or component.unit
            as_of += component.pricing_key.pricing_market_data_as_of
            date = component.pricing_key.pricing_market_data_as_of[0].pricing_date
            dates.append(date)
            values.append(component.raw_value)

            if component.error:
                error[date] = component.error

        return SeriesWithInfo(
            pricing_key or generated_pricing_key.clone(pricing_market_data_as_of=as_of),
            pd.Series(index=dates, data=values).sort_index(),
            unit=unit,
            error=error)


class FloatWithInfo(ScalarWithInfo, float):

    def __new__(cls,
                pricing_key: PricingKey,
                value: Union[float, str],
                unit: Optional[str] = None,
                error: Optional[str] = None,
                calculation_time: Optional[float] = None,
                queueing_time: Optional[float] = None):
        return float.__new__(cls, value)

    @property
    def raw_value(self) -> float:
        return float(self)

    def __repr__(self):
        return self.error if self.error else float.__repr__(self)


class StringWithInfo(ScalarWithInfo, str):

    def __new__(cls,
                pricing_key: PricingKey,
                value: Union[float, str],
                unit: Optional[str] = None,
                error: Optional[str] = None,
                calculation_time: Optional[float] = None,
                queueing_time: Optional[float] = None):
        return str.__new__(cls, value)

    @property
    def raw_value(self) -> str:
        return str(self)

    def __repr__(self):
        return self.error if self.error else str.__repr__(self)


class SeriesWithInfo(pd.Series, ResultInfo):

    def __init__(
            self,
            pricing_key: PricingKey,
            *args,
            unit: Optional[str] = None,
            error: Optional[Union[str, dict]] = None,
            calculation_time: Optional[int] = None,
            queueing_time: Optional[int] = None,
            **kwargs
    ):
        pd.Series.__init__(self, *args, **kwargs)
        ResultInfo.__init__(
            self,
            pricing_key,
            unit=unit,
            error=error,
            calculation_time=calculation_time,
            queueing_time=queueing_time)

        self.index.name = 'date'

    def __repr__(self):
        return self.error if self.error else pd.Series.__repr__(self)

    @property
    def raw_value(self) -> pd.Series:
        return pd.Series(self)

    def for_pricing_key(self, pricing_key: PricingKey):
        dates = [as_of.pricing_date for as_of in pricing_key.pricing_market_data_as_of]
        scalar = len(dates) == 1
        error = self.error or {}
        error = error.get(dates[0]) if scalar else {d: error[d] for d in dates if d in error}

        if scalar:
            return FloatWithInfo(pricing_key, self.loc[dates[0]], unit=self.unit, error=error)

        return SeriesWithInfo(pricing_key, pd.Series(index=dates, data=self.loc[dates]), unit=self.unit, error=error)


class DataFrameWithInfo(pd.DataFrame, ResultInfo):

    def __init__(
            self,
            pricing_key: PricingKey,
            *args,
            unit: Optional[str] = None,
            error: Optional[Union[str, dict]] = None,
            calculation_time: Optional[float] = None,
            queueing_time: Optional[float] = None,
            **kwargs
    ):
        pd.DataFrame.__init__(self, *args, **kwargs)
        properties = [i for i in dir(ResultInfo) if isinstance(getattr(ResultInfo, i), property)]
        internal_names = properties + ['_ResultInfo__' + i for i in properties if i != 'raw_value']
        self._internal_names.append(internal_names)
        self._internal_names_set.update(internal_names)
        ResultInfo.__init__(
            self,
            pricing_key,
            unit=unit,
            error=error,
            calculation_time=calculation_time,
            queueing_time=queueing_time)

    def __repr__(self):
        return self.error if self.error else pd.DataFrame.__repr__(self)

    @property
    def raw_value(self) -> pd.DataFrame:
        return pd.DataFrame(self)

    def for_pricing_key(self, pricing_key: PricingKey):
        dates = [as_of.pricing_date for as_of in pricing_key.pricing_market_data_as_of]
        error = self.error or {}
        error = {d: error[d] for d in dates if d in error}
        df = self.loc[dates]

        if len(dates) == 1:
            df = df.reset_index(drop=True)

        return DataFrameWithInfo(pricing_key, df, unit=self.unit, error=error)

    @staticmethod
    def compose(components, pricing_key: Optional[PricingKey] = None):
        unit = None
        error = {}
        as_of = ()
        dfs = []
        generated_pricing_key = None

        for component in components:
            generated_pricing_key = component.pricing_key
            unit = unit or component.unit
            as_of += component.pricing_key.pricing_market_data_as_of
            date = component.pricing_key.pricing_market_data_as_of[0].pricing_date

            df = component.raw_value
            if df.index.name != 'date' and 'date' not in df:
                df = df.assign(date=date)

            dfs.append(df)

            if component.error:
                error[date] = component.error

        df = pd.concat(dfs)
        if df.index.name != 'date':
            df = df.set_index('date')

        return DataFrameWithInfo(
            pricing_key or generated_pricing_key.clone(pricing_market_data_as_of=as_of),
            df,
            unit=unit,
            error=error)


class PricingDateAndMarketDataAsOf(__PricingDateAndMarketDataAsOf):

    def __repr__(self):
        return '{} : {}'.format(self.pricing_date, self.market_data_as_of)


def sum_formatter(result: List, pricing_key: PricingKey, _instrument: InstrumentBase) -> float:
    result = __flatten_result(result)

    return FloatWithInfo(
        pricing_key,
        sum(r.get('value', float('Nan')) for r in result),
        unit=result[0].get('valueUnit'),
        error=next(filter(None, (r.get('error') for r in result)), None))


def __flatten_result(item: Union[List, Tuple]):
    rows = []
    for elem in item:
        if isinstance(elem, (list, tuple)):
            rows.extend(__flatten_result(elem))
        else:
            date = elem.get('date')
            if date is not None:
                elem['date'] = dateutil.parser.isoparse(date).date()

            rows.append(elem)

    return rows


def __scalar_with_info_from_result(result: dict, pricing_key: PricingKey):
    if 'message' in result:
        return StringWithInfo(
            pricing_key,
            result.get('message', ''),
            unit=result.get('valueUnit'),
            error=result.get('errorMessage'),
            calculation_time=result.get('calculationTime'),
            queueing_time=result.get('queueingTime'))
    elif 'value' in result:
        return FloatWithInfo(
            pricing_key,
            result.get('value', float('nan')),
            unit=result.get('valueUnit'),
            error=result.get('errorMessage'),
            calculation_time=result.get('calculationTime'),
            queueing_time=result.get('queueingTime'))
    else:
        raise RuntimeError('Unknown scalar result')


def scalar_formatter(result: List, pricing_key: PricingKey, _instrument: InstrumentBase)\
        -> Optional[Union[FloatWithInfo, StringWithInfo, SeriesWithInfo, None]]:
    if not result:
        return None

    result = __flatten_result(result)

    if not result:
        return None

    if len(result) > 1 and 'date' in result[0]:
        columns = [x for x in result[0].keys() if x != 'value']
        compressed_results = pd.DataFrame(result).groupby(columns).sum().reset_index().to_dict('records')
        r = [__scalar_with_info_from_result(r, pricing_key.for_pricing_date(r['date'])) for r in compressed_results]
        return r[0].compose(
            r,
            pricing_key)
    else:
        return __scalar_with_info_from_result(result[0], pricing_key)


def __dataframe_formatter(result: List, pricing_key: PricingKey, columns: Tuple[str, ...])\
        -> Optional[DataFrameWithInfo]:
    if not result:
        return None

    df = sort_risk(pd.DataFrame.from_records(__flatten_result(result)), columns)
    calculation_time = df.calculationTime.unique().sum() if 'calculationTime' in df else 0
    queueing_time = df.queueingTime.unique().sum() if 'calculationTime' in df else 0
    error = None

    if 'errorMessage' in df:
        error = df.errorMessage

    df.drop(columns=['calculationTime', 'queueingTime', 'errorMessage'], inplace=True, errors='ignore')

    if len(df.index.unique()) == 1:
        df.reset_index(drop=True, inplace=True)

    return DataFrameWithInfo(
        pricing_key,
        df,
        error=error,
        calculation_time=calculation_time,
        queueing_time=queueing_time)


def structured_formatter(result: List, pricing_key: PricingKey, _instrument: InstrumentBase) -> Optional[pd.DataFrame]:
    return __dataframe_formatter(result, pricing_key, __risk_columns)


def crif_formatter(result: List, pricing_key: PricingKey, _instrument: InstrumentBase) -> Optional[pd.DataFrame]:
    return __dataframe_formatter(result, pricing_key, __crif_columns)


def cashflows_formatter(result: List, pricing_key: PricingKey, _instrument: InstrumentBase) -> Optional[pd.DataFrame]:
    return __dataframe_formatter(result, pricing_key, __cashflows_columns)


def asset_formatter(result: List, pricing_key: PricingKey, _instrument: InstrumentBase) -> Optional[pd.DataFrame]:
    return __dataframe_formatter(result, pricing_key, __cashflows_columns)


def instrument_formatter(result: List, pricing_key: PricingKey, instrument: InstrumentBase):
    instruments_by_date = {}

    for field_values in result:
        new_instrument = instrument.from_dict(field_values)
        new_instrument.unresolved = instrument
        new_instrument.name = instrument.name

        if len(result) > 1 and 'date' in field_values:
            date = dt.date.fromtimestamp(field_values['date'] / 1e9) + dt.timedelta(days=1)
            as_of = next((a for a in pricing_key.pricing_market_data_as_of if date == a.pricing_date), None)

            if as_of:
                date_key = pricing_key.clone(pricing_market_data_as_of=as_of)
                new_instrument.resolution_key = date_key
                instruments_by_date[date] = new_instrument
        else:
            new_instrument.resolution_key = pricing_key
            return new_instrument

    return instruments_by_date


def aggregate_risk(results: Iterable[Union[DataFrameWithInfo, Future]], threshold: Optional[float] = None)\
        -> pd.DataFrame:
    """
    Combine the results of multiple InstrumentBase.calc() calls, into a single result

    :param results: An iterable of Dataframes and/or Futures (returned by InstrumentBase.calc())
    :param threshold: exclude values whose absolute value falls below this threshold
    :return: A Dataframe with the aggregated results

    **Examples**

    >>> from gs_quant.instrument import IRCap, IRFloor
    >>> from gs_quant.markets import PricingContext
    >>> from gs_quant.risk import IRDelta, IRVega
    >>>
    >>> cap = IRCap('5y', 'GBP')
    >>> floor = IRFloor('5y', 'GBP')
    >>> instruments = (cap, floor)
    >>>
    >>> with PricingContext():
    >>>     delta_f = [inst.calc(IRDelta) for inst in instruments]
    >>>     vega_f = [inst.calc(IRVega) for inst in (cap, floor)]
    >>>
    >>> delta = aggregate_risk(delta_f, threshold=0.1)
    >>> vega = aggregate_risk(vega_f)

    delta_f and vega_f are lists of futures, where the result will be a Dataframe
    delta and vega are Dataframes, representing the merged risk of the individual instruments
    """
    dfs = [r.result().raw_value if isinstance(r, Future) else r.raw_value for r in results]
    result = pd.concat(dfs)
    result = result.groupby([c for c in result.columns if c != 'value']).sum()
    result = pd.DataFrame.from_records(result.to_records())

    if threshold is not None:
        result = result[result.value.abs() > threshold]

    return sort_risk(result)


def aggregate_results(results: Iterable[Union[dict, DataFrameWithInfo, FloatWithInfo, SeriesWithInfo]])\
        -> Union[dict, DataFrameWithInfo, FloatWithInfo, SeriesWithInfo]:
    unit = None
    pricing_key = None
    results = tuple(results)

    for result in results:
        if result.error:
            raise ValueError('Cannot aggregate results in error')

        if not isinstance(result, type(results[0])):
            raise ValueError('Cannot aggregate heterogeneous types')

        if result.unit:
            if unit and unit != result.unit:
                raise ValueError('Cannot aggregate results with different units')

            unit = unit or result.unit

        if pricing_key and pricing_key != result.pricing_key:
            raise ValueError('Cannot aggregate results with different pricing keys')

        pricing_key = pricing_key or result.pricing_key

    inst = next(iter(results))
    if isinstance(inst, dict):
        return dict((k, aggregate_results([r[k] for r in results])) for k in inst.keys())
    elif isinstance(inst, FloatWithInfo):
        return FloatWithInfo(pricing_key, sum(results), unit=unit)
    elif isinstance(inst, SeriesWithInfo):
        return SeriesWithInfo(pricing_key, sum(results), unit=unit)
    elif isinstance(inst, DataFrameWithInfo):
        return DataFrameWithInfo(pricing_key, aggregate_risk(results), unit=unit)


def subtract_risk(left: DataFrameWithInfo, right: DataFrameWithInfo) -> pd.DataFrame:
    """Subtract bucketed risk. Dimensions must be identical

    :param left: Results to substract from
    :param right: Results to substract

    **Examples**

    >>> from gs_quant.datetime.date import business_day_offset
    >>> from gs_quant.instrument IRSwap
    >>> from gs_quant.markets import PricingContext
    >>> from gs_quant.risk import IRDelta
    >>> import datetime as dt
    >>>
    >>> ir_swap = IRSwap('Pay', '10y', 'USD')
    >>> delta_today = ir_swap.calc(IRDelta)
    >>>
    >>> with PricingContext(pricing_date=business_day_offset(dt.date.today(), -1, roll='preceding')):
    >>>     delta_yday_f = ir_swap.calc(IRDelta)
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
IRBasis = __risk_measure_with_doc_string(
    'IRBasis',
    'Interest Rate Basis',
    RiskMeasureType.Basis,
    asset_class=AssetClass.Rates)
InflationDelta = __risk_measure_with_doc_string(
    'InflationDelta',
    'Inflation Delta',
    RiskMeasureType.InflationDelta,
    asset_class=AssetClass.Rates)
InflationDeltaParallel = __risk_measure_with_doc_string(
    'InflationDeltaParallel',
    'Inflation Parallel Delta',
    RiskMeasureType.ParallelInflationDelta,
    asset_class=AssetClass.Rates)
InflationDeltaParallelLocalCcy = __risk_measure_with_doc_string(
    'InflationDeltaParallelLocalCcy',
    'Inflation Parallel Delta (Local Ccy)',
    RiskMeasureType.ParallelInflationDeltaLocalCcy,
    asset_class=AssetClass.Rates)
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
IRXccyDelta = __risk_measure_with_doc_string(
    'IRXccyDelta',
    'Cross-ccy Delta',
    RiskMeasureType.XccyDelta,
    asset_class=AssetClass.Rates)
IRXccyDeltaParallel = __risk_measure_with_doc_string(
    'IRXccyDeltaParallel',
    'Cross-ccy Parallel Delta',
    RiskMeasureType.ParallelXccyDelta,
    asset_class=AssetClass.Rates)
IRXccyDeltaParallelLocalCurrency = __risk_measure_with_doc_string(
    'IRXccyDeltaParallelLocalCurrency',
    'Cross-ccy Parallel Delta (Local Ccy)',
    RiskMeasureType.ParallelXccyDeltaLocalCcy,
    asset_class=AssetClass.Rates)
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
    IRBasis: structured_formatter,
    InflationDelta: structured_formatter,
    InflationDeltaParallel: scalar_formatter,
    InflationDeltaParallelLocalCcy: scalar_formatter,
    IRDelta: structured_formatter,
    IRDeltaParallel: sum_formatter,
    IRDeltaLocalCcy: structured_formatter,
    IRDeltaParallelLocalCcy: scalar_formatter,
    IRXccyDelta: structured_formatter,
    IRXccyDeltaParallel: scalar_formatter,
    IRXccyDeltaParallelLocalCurrency: scalar_formatter,
    IRGammaParallel: scalar_formatter,
    IRGammaParallelLocalCcy: scalar_formatter,
    IRVega: structured_formatter,
    IRVegaParallel: scalar_formatter,
    IRVegaLocalCcy: structured_formatter,
    IRVegaParallelLocalCcy: scalar_formatter,
    IRAnnualImpliedVol: scalar_formatter,
    IRDailyImpliedVol: scalar_formatter,
    IRAnnualATMImpliedVol: scalar_formatter,
    IRSpotRate: scalar_formatter,
    IRFwdRate: scalar_formatter,
    CRIFIRCurve: crif_formatter,
    ResolvedInstrumentValues: instrument_formatter,
    Cashflows: cashflows_formatter,
    MarketDataAssets: asset_formatter,
    Description: scalar_formatter
}
