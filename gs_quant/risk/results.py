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
from gs_quant.base import InstrumentBase, Priceable, RiskKey, Sentinel
from gs_quant.risk import DataFrameWithInfo, ErrorValue, FloatWithInfo, RiskMeasure, SeriesWithInfo, aggregate_results

from concurrent.futures import Future
import copy
import datetime as dt
from itertools import chain
import logging
import operator as op
import pandas as pd
from typing import Any, Iterable, Mapping, Optional, Tuple, Union


_logger = logging.getLogger(__name__)


def _value_for_date(result: Union[DataFrameWithInfo, SeriesWithInfo], date: dt.date) -> \
        Union[DataFrameWithInfo, ErrorValue, FloatWithInfo]:
    from gs_quant.markets import CloseMarket

    raw_value = result.loc[date]
    key = result.risk_key

    risk_key = RiskKey(
        key.provider,
        date,
        CloseMarket(date=date, location=key.market.location if isinstance(key.market, CloseMarket) else None),
        key.params,
        key.scenario,
        key.risk_measure)

    if isinstance(raw_value, ErrorValue):
        return raw_value
    elif isinstance(raw_value, DataFrameWithInfo):
        return DataFrameWithInfo(
            raw_value.raw_value.reset_index(drop=True),
            risk_key,
            unit=result.unit,
            error=result.error)
    else:
        return FloatWithInfo(
            risk_key,
            raw_value,
            unit=result.unit.get(date, '') if result.unit else None,
            error=result.error)


class PricingFuture(Future):

    __RESULT_SENTINEL = Sentinel('PricingFuture')

    def __init__(self, result: Optional[Any] = __RESULT_SENTINEL):
        super().__init__()
        if result is not self.__RESULT_SENTINEL:
            self.set_result(result)

    def result(self, timeout=None):
        """Return the result of the call that the future represents.

        :param timeout: The number of seconds to wait for the result if the future isn't done.
        If None, then there is no limit on the wait time.

        Returns:
            The result of the call that the future represents.

        Raises:
            CancelledError: If the future was cancelled.
            TimeoutError: If the future didn't finish executing before the given timeout.

        Exception: If the call raised then that exception will be raised.
        """
        from gs_quant.markets import PricingContext
        if not self.done() and PricingContext.current.active_context.is_entered:
            raise RuntimeError('Cannot evaluate results under the same pricing context being used to produce them')

        return super().result(timeout=timeout)


class CompositeResultFuture(PricingFuture):

    def __init__(self, futures: Iterable[PricingFuture]):
        super().__init__()
        self.__futures = tuple(futures)
        self.__pending = set()

        for future in self.__futures:
            if not future.done():
                future.add_done_callback(self.__cb)
                self.__pending.add(future)

        if not self.__pending:
            self._set_result()

    def __getitem__(self, item):
        return self.result()[item]

    def __cb(self, future: PricingFuture):
        self.__pending.discard(future)
        if not self.__pending:
            self._set_result()

    def _set_result(self):
        self.set_result([f.result() for f in self.__futures])

    @property
    def futures(self) -> Tuple[PricingFuture, ...]:
        return self.__futures


class MultipleRiskMeasureResult(dict):

    def __init__(self, instrument, dict_values: Iterable):
        super().__init__(dict_values)
        self.__instrument = instrument

    def __getitem__(self, item):
        if isinstance(item, dt.date):
            if all(isinstance(v, (DataFrameWithInfo, SeriesWithInfo)) for v in self.values()):
                return MultipleRiskMeasureResult(self.__instrument, ((k, _value_for_date(v, item))
                                                                     for k, v in self.items()))
            else:
                raise ValueError('Can only index by date on historical results')
        else:
            return super().__getitem__(item)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return self.__op(op.mul, other)
        else:
            return ValueError('Can only multiply by an int or float')

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return self.__op(op.add, other)
        elif isinstance(other, MultipleRiskMeasureResult):
            if sorted(self.keys()) == sorted(other.keys()):
                from gs_quant.markets.portfolio import Portfolio
                return PortfolioRiskResult(
                    Portfolio((self.__instrument, other.__instrument)),
                    self.keys(),
                    tuple(MultipleRiskMeasureFuture(r.__instrument, dict((k, PricingFuture(v)) for k, v in r))
                          for r in (self, other))
                )
            elif set(self.keys()).isdisjoint(other.keys()) and self.__instrument == other.__instrument:
                if set(self.keys()).intersection(other.keys()):
                    raise ValueError('Keys must be disjoint')

                return MultipleRiskMeasureResult(self.__instrument, chain(self.items(), other.items()))
            else:
                raise ValueError('Can only add where risk_measures match or instrument identical &' +
                                 'risk_measures disjoint')
        else:
            raise ValueError('Can only add instances of MultipleRiskMeasureResult or int, float')

    def __op(self, operator, operand):
        values = {}
        for key, value in self.items():
            if isinstance(value, pd.DataFrame):
                new_value = value.copy()
                new_value.value = operator(value.value, operand)
            else:
                new_value = operator(value, operand)

            values[key] = new_value

        return MultipleRiskMeasureResult(self.__instrument, values)

    @property
    def instrument(self):
        return self.__instrument

    @property
    def dates(self) -> Tuple[dt.date, ...]:
        dates = set()
        for value in self.values():
            if isinstance(value, (DataFrameWithInfo, SeriesWithInfo)):
                dates.update(value.index)

        return tuple(sorted(dates))


class MultipleRiskMeasureFuture(CompositeResultFuture):

    def __init__(self, instrument: InstrumentBase, measures_to_futures: Mapping[RiskMeasure, PricingFuture]):
        self.__measures_to_futures = measures_to_futures
        self.__instrument = instrument
        super().__init__(measures_to_futures.values())

    def _set_result(self):
        self.set_result(MultipleRiskMeasureResult(self.__instrument,
                                                  zip(self.__measures_to_futures.keys(),
                                                      (f.result() for f in self.futures))))

    @property
    def measures_to_futures(self) -> Mapping[RiskMeasure, PricingFuture]:
        return self.__measures_to_futures


class HistoricalPricingFuture(CompositeResultFuture):

    def _set_result(self):
        results = [f.result() for f in self.futures]
        base = next((r for r in results if not isinstance(r, (ErrorValue, Exception))), None)

        if base is None:
            _logger.error(f'Historical pricing failed: {results[0]}')
            self.set_result(results[0])
        else:
            result = MultipleRiskMeasureResult(base.instrument,
                                               {k: base[k].compose(r[k] for r in results) for k in base.keys()}) \
                if isinstance(base, MultipleRiskMeasureResult) else base.compose(results)
            self.set_result(result)


class PortfolioPath:

    def __init__(self, path):
        self.__path = (path,) if isinstance(path, int) else path

    def __repr__(self):
        return repr(self.__path)

    def __iter__(self):
        return iter(self.__path)

    def __len__(self):
        return len(self.__path)

    def __add__(self, other):
        return PortfolioPath(self.__path + other.__path)

    def __eq__(self, other):
        return self.__path == other.__path

    def __hash__(self):
        return hash(self.__path)

    def __call__(self, target, rename_to_parent: Optional[bool] = False):
        parent = None
        path = list(self.__path)

        while path:
            elem = path.pop(0)
            parent = target if len(self) - len(path) > 1 else None
            target = target.futures[elem] if isinstance(target, CompositeResultFuture) else target[elem]

            if isinstance(target, PricingFuture) and path:
                target = target.result()

        if rename_to_parent and parent and getattr(parent, 'name', None):
            target = copy.copy(target)
            target.name = parent.name

        return target


class PortfolioRiskResult(CompositeResultFuture):

    def __init__(self,
                 portfolio,
                 risk_measures: Iterable[RiskMeasure],
                 futures: Iterable[PricingFuture]):
        super().__init__(futures)
        self.__portfolio = portfolio
        self.__risk_measures = tuple(risk_measures)

    def __getitem__(self, item):
        if isinstance(item, RiskMeasure):
            if item not in self.risk_measures:
                raise ValueError('{} not computed'.format(item))

            if len(self.risk_measures) == 1:
                return self
            else:
                return PortfolioRiskResult(self.__portfolio, (item,), self.futures)
        elif isinstance(item, dt.date):
            futures = []
            for result in self:
                if isinstance(result, (MultipleRiskMeasureResult, PortfolioRiskResult)):
                    futures.append(PricingFuture(result[item]))
                elif isinstance(result, (DataFrameWithInfo, SeriesWithInfo)):
                    futures.append(PricingFuture(_value_for_date(result, item)))
                else:
                    raise RuntimeError('Can only index by date on historical results')

            return PortfolioRiskResult(self.__portfolio, self.risk_measures, futures)
        else:
            return self.__results(items=item)

    def __contains__(self, item):
        if isinstance(item, RiskMeasure):
            return item in self.__risk_measures
        elif isinstance(item, dt.date):
            return item in self.dates
        else:
            return item in self.__portfolio

    def __len__(self):
        return len(self.futures)

    def __iter__(self):
        return iter(self.__results())

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            futures = [f + other if isinstance(f, PortfolioRiskResult) else PricingFuture(f.result() * other)
                       for f in self.futures]
            return PortfolioRiskResult(self.__portfolio, self.__risk_measures, futures)
        else:
            return ValueError('Can only multiply by an int or float')

    def __add__(self, other):
        if isinstance(other, (int, float)):
            futures = [f + other if isinstance(f, PortfolioRiskResult) else PricingFuture(f.result() + other)
                       for f in self.futures]
            return PortfolioRiskResult(self.__portfolio, self.__risk_measures, futures)
        elif isinstance(other, PortfolioRiskResult):
            if sorted(self.__risk_measures) == sorted(other.__risk_measures):
                return PortfolioRiskResult(
                    self.__portfolio + other.__portfolio,
                    self.__risk_measures,
                    self.futures + other.futures)
            elif set(self.__risk_measures).isdisjoint(other.__risk_measures) and self.__portfolio == other.__portfolio:
                futures = []
                risk_measures = self.__risk_measures + other.__risk_measures
                risk_measure = self.__risk_measures[0] if len(self.__risk_measures) == 1 else None
                other_measure = other.__risk_measures[0] if len(other.__risk_measures) == 1 else None

                for priceable, future, other_future in zip(self.__portfolio, self.futures, other.futures):
                    if isinstance(future, PortfolioRiskResult) and isinstance(other_future, PortfolioRiskResult):
                        futures.append(future + other_future)
                    else:
                        if risk_measure:
                            future = MultipleRiskMeasureFuture(priceable, {risk_measure: future})

                        if other_measure:
                            other_future = MultipleRiskMeasureFuture(priceable, {other_measure: other_future})

                        risk_measure_futures = [future.measures_to_futures.get(m) or other_future.measures_to_futures[m]
                                                for m in risk_measures]
                        futures.append(MultipleRiskMeasureFuture(priceable,
                                                                 dict(zip(risk_measures, risk_measure_futures))))

                return PortfolioRiskResult(self.__portfolio, risk_measures, futures)
            else:
                raise ValueError('Can only add where risk_measures match or portfolios identical &' +
                                 'risk_measures disjoint')
        else:
            raise ValueError('Can only add instances of PortfolioRiskResult or int, float')

    @property
    def portfolio(self):
        return self.__portfolio

    @property
    def risk_measures(self) -> Tuple[RiskMeasure, ...]:
        return self.__risk_measures

    @property
    def dates(self) -> Tuple[dt.date, ...]:
        dates = set()
        for result in self.__results():
            if isinstance(result, (MultipleRiskMeasureResult, PortfolioRiskResult)):
                dates.update(result.dates)
            elif isinstance(result, (pd.DataFrame, pd.Series)):
                dates.update(result.index)

        return tuple(sorted(dates))

    def result(self, timeout: Optional[int] = None):
        super().result(timeout=timeout)
        return self

    def to_frame(self):
        dates = self.dates

        def to_records(p: PortfolioRiskResult) -> list:
            return [to_records(res) if isinstance(res, PortfolioRiskResult) else res for res in p]

        def flatten_list(lst):
            return [item for sublist in lst for item in sublist]

        def multiple(p):
            if len(p.portfolios) == 0:
                return len(p.all_instruments) * len(self.risk_measures) if dates else len(p.all_instruments)
            if len(p.portfolios) > 0:
                for i in p.portfolios:
                    return len(i) * multiple(i)

        '''Populate index labels'''
        def pop_idx_labels(p, level, idx_label):
            if len(p.portfolios) == 0:
                for idx, r in enumerate(p.all_instruments):
                    r.name = f'{r.type.name}_{idx}' if r.name is None else r.name
                if dates and len(self.risk_measures) > 1:
                    idx_label[0].append(
                        [str(r) for r in self.risk_measures] * len(p.all_instruments))
                    if len(idx_label) > 1:
                        idx_label[1].append([[r.name] * len(self.risk_measures) for r in p.all_instruments])
                    return idx_label
                else:
                    return idx_label[0].append([r.name for r in p.all_instruments])

            if level > 1:
                curr_level_arr = idx_label[level - 1]
                for idx, r in enumerate(p.all_portfolios):
                    r.name = f'Portfolio_{idx}' if r.name is None else r.name
                [curr_level_arr.append([r.name] * multiple(r)) for r in p.portfolios]
                for r in p.portfolios:
                    pop_idx_labels(r, level - 1, idx_label)
            return idx_label

        '''Extract risk values'''
        record = to_records(self)
        port_depth = len(max(self.portfolio.all_paths, key=len))
        port_depth = port_depth + 1 if (dates and len(self.risk_measures) > 1) else port_depth
        temp_array = [[] for _ in range(port_depth)]
        idx_labels = pop_idx_labels(self.portfolio, port_depth, temp_array)
        if idx_labels:
            idx_labels[1] = flatten_list(idx_labels[1]) if (dates and len(self.risk_measures) > 1) else idx_labels[1]
            flat_list = [flatten_list(idx_labels[i]) for i in range(len(idx_labels))]
            flat_list.reverse()
            '''Get list of tuples for multiindex'''
            index_multi = list(zip(*flat_list))
        else:
            index_multi = None
        '''Case with risk values calculated over a range of dates'''
        if dates:
            '''Base case with 1 (unnested) portfolio and 1 risk measure'''
            if len(self.risk_measures) == 1:
                df = pd.DataFrame(record)
            else:
                df = pd.concat([pd.DataFrame(rec) for rec in record], axis=1)
            '''Ensure dates are always the index'''
            check_date = [idx for idx in dates]
            check_date.reverse()
            df = df.transpose() if [idx for idx in df.index] != check_date else df
            df.columns = pd.MultiIndex.from_tuples(index_multi) if index_multi else [r.name for r in
                                                                                     self.portfolio.all_instruments]
            return df

        else:
            if len(self.portfolio.all_portfolios) == 0:
                return pd.DataFrame(record, columns=self.risk_measures, index=[p.name for p in self.portfolio])
            else:
                df = pd.DataFrame(record)
                df.index = pd.MultiIndex.from_tuples(index_multi) if index_multi else [r.name for r in
                                                                                       self.portfolio.all_instruments]
                df.columns = self.risk_measures
                return df

    def subset(self, items: Iterable[Union[int, str, PortfolioPath, Priceable]], name: Optional[str] = None):
        paths = tuple(chain.from_iterable((i,) if isinstance(i, PortfolioPath) else self.__paths(i) for i in items))
        sub_portfolio = self.__portfolio.subset(paths, name=name)
        return PortfolioRiskResult(sub_portfolio, self.risk_measures, [p(self.futures) for p in paths])

    def aggregate(self) -> Union[float, pd.DataFrame, pd.Series, MultipleRiskMeasureResult]:
        if len(self.__risk_measures) > 1:
            return MultipleRiskMeasureResult(self.portfolio, ((r, self[r].aggregate()) for r in self.__risk_measures))
        else:
            return aggregate_results(self.__results())

    def __paths(self, items: Union[int, slice, str, Priceable]) -> Tuple[PortfolioPath, ...]:
        if isinstance(items, int):
            return PortfolioPath(items),
        elif isinstance(items, slice):
            return tuple(PortfolioPath(i) for i in range(len(self.__portfolio))[items])
        elif isinstance(items, (str, Priceable)):
            paths = self.__portfolio.paths(items)
            if not paths and isinstance(items, InstrumentBase) and items.unresolved:
                paths = self.__portfolio.paths(items.unresolved)
                key = items.resolution_key.ex_measure
                paths = tuple(p for p in paths if self.__result(p, self.risk_measures[0]).risk_key.ex_measure == key)

                if not paths:
                    raise KeyError(f'{items} not in portfolio')

            return paths

    def __results(self, items: Optional[Union[int, slice, str, Priceable]] = None):
        if items is None:
            return tuple(self.__result(p) for p in self.__portfolio.all_paths)

        paths = self.__paths(items)
        return self.__result(paths[0]) if not isinstance(items, slice) else self.subset(paths)

    def __result(self, path: PortfolioPath, risk_measure: Optional[RiskMeasure] = None):
        res = path(self.futures).result()

        if len(self.risk_measures) == 1 and not risk_measure:
            risk_measure = self.risk_measures[0]

        return res[risk_measure]\
            if risk_measure and isinstance(res, (MultipleRiskMeasureResult, PortfolioRiskResult)) else res
