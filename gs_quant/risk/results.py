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
from gs_quant.base import InstrumentBase, Priceable
from gs_quant.risk import ErrorValue, RiskMeasure, aggregate_results

from concurrent.futures import Future
import copy
import datetime as dt
from itertools import chain
import logging
import pandas as pd
from typing import Iterable, Mapping, Optional, Tuple, Union


_logger = logging.getLogger(__name__)


class _Sentinel:
    pass


class PricingFuture(Future):

    def __init__(self, result=_Sentinel):
        super().__init__()
        if result != _Sentinel:
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

    def __init__(self, futures: Iterable[Future]):
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

    def __cb(self, future: Future):
        self.__pending.remove(future)
        if not self.__pending:
            self._set_result()

    def _set_result(self):
        self.set_result([f.result() for f in self.__futures])

    @property
    def futures(self) -> Tuple[Future, ...]:
        return self.__futures


class MultipleRiskMeasureResult(dict):

    def __getitem__(self, item):
        if isinstance(item, dt.date):
            if all(isinstance(v, (pd.DataFrame, pd.Series)) for v in self.values()):
                return MultipleRiskMeasureResult((k, v.loc[item]) for k, v in self.items())
            else:
                raise ValueError('Can only index by date on historical results')
        else:
            return super().__getitem__(item)


class MultipleRiskMeasureFuture(CompositeResultFuture):

    def __init__(self, measures_to_futures: Mapping[RiskMeasure, Future]):
        self.__risk_measures = measures_to_futures.keys()
        super().__init__(measures_to_futures.values())

    def _set_result(self):
        self.set_result(MultipleRiskMeasureResult(dict(zip(self.__risk_measures, (f.result() for f in self.futures)))))


class HistoricalPricingFuture(CompositeResultFuture):

    def _set_result(self):
        results = [f.result() for f in self.futures]
        base = next((r for r in results if not isinstance(r, (ErrorValue, Exception))), None)

        if base is None:
            _logger.error(f'Historical pricing failed: {results[0]}')
            self.set_result(results[0])
        else:
            result = MultipleRiskMeasureResult({k: base[k].compose(r[k] for r in results) for k in base.keys()})\
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
                 futures: Iterable[Future]):
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
                elif isinstance(result, (pd.DataFrame, pd.Series)):
                    futures.append(PricingFuture(result.loc[item]))
                else:
                    raise RuntimeError('Can only index by date on historical results')

            return PortfolioRiskResult(self.__portfolio, self.risk_measures, futures)
        else:
            return self.__results(items=item)

    def __len__(self):
        return len(self.futures)

    def __iter__(self):
        return iter(self.__results())

    @property
    def portfolio(self):
        return self.__portfolio

    @property
    def risk_measures(self) -> Tuple[RiskMeasure, ...]:
        return self.__risk_measures

    @property
    def dates(self):
        result = self[self.__risk_measures[0]].__results(self.__portfolio.all_instruments[0])
        result = result[0] if isinstance(result, PortfolioRiskResult) else result
        return tuple(i.date() for i in result.index) if isinstance(result, (pd.DataFrame, pd.Series)) else None

    def result(self, timeout: Optional[int] = None):
        super().result(timeout=timeout)
        return self

    def to_frame(self):
        def to_records(p: PortfolioRiskResult) -> list:
            return [to_records(res) if isinstance(res, PortfolioRiskResult) else res for res in p._result]
        return pd.DataFrame(to_records(self))

    def subset(self, items: Iterable[Union[int, str, PortfolioPath, Priceable]], name: Optional[str] = None):
        paths = tuple(chain.from_iterable((i,) if isinstance(i, PortfolioPath) else self.__paths(i) for i in items))
        sub_portfolio = self.__portfolio.subset(paths, name=name)
        return PortfolioRiskResult(sub_portfolio, self.risk_measures, [p(self.futures) for p in paths])

    def aggregate(self) -> Union[float, pd.DataFrame, pd.Series, MultipleRiskMeasureResult]:
        if len(self.__risk_measures) > 1:
            return MultipleRiskMeasureResult((r, self[r].aggregate()) for r in self.__risk_measures)
        else:
            return aggregate_results(self.__results())

    def __paths(self, items: Union[int, slice, str, Priceable]) -> Tuple[PortfolioPath, ...]:
        if isinstance(items, int):
            return (PortfolioPath(items),)
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
        return self.__result(paths[0]) if len(paths) == 1 else self.subset(paths)

    def __result(self, path: PortfolioPath, risk_measure: Optional[RiskMeasure] = None):
        res = path(self.futures).result()

        if len(self.risk_measures) == 1 and not risk_measure:
            risk_measure = self.risk_measures[0]

        return res[risk_measure]\
            if risk_measure and isinstance(res, (MultipleRiskMeasureResult, PortfolioRiskResult)) else res
