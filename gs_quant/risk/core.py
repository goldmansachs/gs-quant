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
import itertools
import datetime as dt
from typing import Iterable, Optional, Tuple, Union, Any, Callable

import pandas as pd

from .measures import RiskMeasure
from gs_quant.base import RiskKey
from gs_quant.datetime import point_sort_order

__column_sort_fns = {
    'label1': point_sort_order,
    'mkt_point': point_sort_order,
    'point': point_sort_order
}
__risk_columns = ('date', 'time', 'mkt_type', 'mkt_asset', 'mkt_class', 'mkt_point')


class ResultInfo(metaclass=ABCMeta):

    def __init__(
            self,
            risk_key: RiskKey,
            unit: Optional[dict] = None,
            error: Optional[Union[str, dict]] = None
    ):
        self.__risk_key = risk_key
        self.__unit = unit
        self.__error = error

    @property
    @abstractmethod
    def raw_value(self):
        ...

    @property
    def risk_key(self) -> RiskKey:
        return self.__risk_key

    @property
    def unit(self) -> dict:
        """The units of this result"""
        return self.__unit

    @property
    def error(self) -> Union[str, dict]:
        """Any error associated with this result"""
        return self.__error

    @staticmethod
    def composition_info(components: Iterable):
        dates = []
        values = []
        errors = {}
        risk_key = None
        unit = None

        for component in components:
            date = component.risk_key.date
            risk_key = component.risk_key.ex_date_and_market if risk_key is None else risk_key

            if isinstance(component, (ErrorValue, Exception)):
                errors[date] = component
            else:
                values.append(component.raw_value)
                dates.append(date)
                unit = unit or component.unit

        return dates, values, errors, risk_key, unit


class ErrorValue(ResultInfo):

    def __init__(self, risk_key: RiskKey, error: Union[str, dict]):
        super().__init__(risk_key, error=error)

    def __repr__(self):
        return self.error

    @property
    def raw_value(self):
        return None


class ScalarWithInfo(ResultInfo, metaclass=ABCMeta):

    def __init__(
            self,
            risk_key: RiskKey,
            value: Union[float, str],
            unit: Optional[dict] = None,
            error: Optional[Union[str, dict]] = None):
        float.__init__(value)
        ResultInfo.__init__(self, risk_key, unit=unit, error=error)

    @property
    @abstractmethod
    def raw_value(self):
        ...

    @staticmethod
    def compose(components: Iterable):
        dates, values, errors, risk_key, unit = ResultInfo.composition_info(components)
        return SeriesWithInfo(pd.Series(index=pd.DatetimeIndex(dates).date, data=values),
                              risk_key=risk_key,
                              unit=unit,
                              error=errors)


class FloatWithInfo(ScalarWithInfo, float):

    def __new__(cls,
                risk_key: RiskKey,
                value: Union[float, str],
                unit: Optional[str] = None,
                error: Optional[str] = None):
        return float.__new__(cls, value)

    @property
    def raw_value(self) -> float:
        return float(self)

    def __repr__(self):

        return self.error if self.error else float.__repr__(self)

    def __add__(self, other):
        if isinstance(other, FloatWithInfo):
            if self.unit == other.unit:
                return FloatWithInfo(combine_risk_key(self.risk_key, other.risk_key), self.raw_value + other.raw_value,
                                     self.unit)
            else:
                raise ValueError('FloatWithInfo unit mismatch')
        return super(FloatWithInfo, self).__add__(other)


class StringWithInfo(ScalarWithInfo, str):

    def __new__(cls,
                risk_key: RiskKey,
                value: Union[float, str],
                unit: Optional[dict] = None,
                error: Optional[str] = None):
        return str.__new__(cls, value)

    @property
    def raw_value(self) -> str:
        return str(self)

    def __repr__(self):
        return self.error if self.error else str.__repr__(self)


class SeriesWithInfo(pd.Series, ResultInfo):
    _internal_names = pd.DataFrame._internal_names + \
                      ['_ResultInfo__' + i for i in dir(ResultInfo) if isinstance(getattr(ResultInfo, i), property)]
    _internal_names_set = set(_internal_names)

    def __init__(
            self,
            *args,
            risk_key: Optional[RiskKey] = None,
            unit: Optional[dict] = None,
            error: Optional[Union[str, dict]] = None,
            **kwargs
    ):
        pd.Series.__init__(self, *args, **kwargs)
        ResultInfo.__init__(self, risk_key, unit=unit, error=error)

    def __repr__(self):
        if self.error:
            return pd.Series.__repr__(self) + "\nErrors: " + str(self.error)
        return pd.Series.__repr__(self)

    @property
    def _constructor(self):
        return SeriesWithInfo

    @property
    def _constructor_expanddim(self):
        return DataFrameWithInfo

    @property
    def raw_value(self) -> pd.Series:
        return pd.Series(self)


class DataFrameWithInfo(pd.DataFrame, ResultInfo):
    _internal_names = pd.DataFrame._internal_names + \
                      ['_ResultInfo__' + i for i in dir(ResultInfo) if isinstance(getattr(ResultInfo, i), property)]
    _internal_names_set = set(_internal_names)

    def __init__(
            self,
            *args,
            risk_key: Optional[RiskKey] = None,
            unit: Optional[dict] = None,
            error: Optional[Union[str, dict]] = None,
            **kwargs
    ):
        pd.DataFrame.__init__(self, *args, **kwargs)
        ResultInfo.__init__(self, risk_key, unit=unit, error=error)

    def __repr__(self):
        if self.error:
            return pd.DataFrame.__repr__(self) + "\nErrors: " + str(self.errors)
        return pd.DataFrame.__repr__(self)

    @property
    def _constructor(self):
        return DataFrameWithInfo

    @property
    def _constructor_sliced(self):
        return SeriesWithInfo

    @property
    def raw_value(self) -> pd.DataFrame:
        return pd.DataFrame(self)

    @staticmethod
    def compose(components: Iterable):
        dates, values, errors, risk_key, unit = ResultInfo.composition_info(components)
        df = pd.concat(v.assign(date=d) for d, v in zip(dates, values)).set_index('date')

        return DataFrameWithInfo(df, risk_key=risk_key, unit=unit, error=errors)


def aggregate_risk(results: Iterable[Union[DataFrameWithInfo, Future]], threshold: Optional[float] = None) \
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
    result = pd.concat(df.reset_index(level=0) if df.index.name == 'date' else df for df in dfs)
    result = result.groupby([c for c in result.columns if c != 'value'], as_index=False).sum()

    if threshold is not None:
        result = result[result.value.abs() > threshold]

    return sort_risk(result)


ResultType = Union[None, dict, tuple, DataFrameWithInfo, FloatWithInfo, SeriesWithInfo]


def aggregate_results(results: Iterable[ResultType]) -> ResultType:
    unit = None
    risk_key = None
    results = tuple(results)

    if not len(results):
        return None

    for result in results:
        if isinstance(result, Exception):
            raise Exception

        if result.error:
            raise ValueError('Cannot aggregate results in error')

        if not isinstance(result, type(results[0])):
            raise ValueError('Cannot aggregate heterogeneous types')

        if result.unit:
            if unit and unit != result.unit:
                raise ValueError('Cannot aggregate results with different units')

            unit = unit or result.unit

        if risk_key and risk_key != result.risk_key:
            raise ValueError('Cannot aggregate results with different pricing keys')

        risk_key = risk_key or result.risk_key

    inst = next(iter(results))
    if isinstance(inst, dict):
        return dict((k, aggregate_results([r[k] for r in results])) for k in inst.keys())
    elif isinstance(inst, tuple):
        return tuple(set(itertools.chain.from_iterable(results)))
    elif isinstance(inst, FloatWithInfo):
        return FloatWithInfo(risk_key, sum(results), unit=unit)
    elif isinstance(inst, SeriesWithInfo):
        return SeriesWithInfo(sum(results), risk_key=risk_key, unit=unit)
    elif isinstance(inst, DataFrameWithInfo):
        return DataFrameWithInfo(aggregate_risk(results), risk_key=risk_key, unit=unit)


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
    assert (left.columns.names == right.columns.names)
    assert ('value' in left.columns.names)

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

    data = sorted((row for _, row in df.iterrows()), key=cmp)
    fields = [f for f in by if f in columns]
    fields.extend(f for f in columns if f not in fields)

    result = pd.DataFrame.from_records(data, columns=columns)[fields]
    if 'date' in result:
        result = result.set_index('date')

    return result


def combine_risk_key(key_1: RiskKey, key_2: RiskKey) -> RiskKey:
    """
    Combine two risk keys (key_1, key_2) into a new RiskKey

    :type key_1: RiskKey
    :type key_2: RiskKey
    """

    def get_field_value(field_name: str): getattr(key_1, field_name) \
        if getattr(key_1, field_name) == getattr(key_2, field_name) else None

    return RiskKey(get_field_value("provider"), get_field_value("date"), get_field_value("market"),
                   get_field_value("params"), get_field_value("scenario"), get_field_value("risk_measure"))
