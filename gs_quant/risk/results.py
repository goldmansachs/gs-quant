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
from gs_quant.base import Priceable
from gs_quant.risk import RiskMeasure, RiskResult, aggregate_results

from collections import namedtuple
from concurrent.futures import Future
from functools import partial
from itertools import chain
import pandas as pd
from typing import Iterable, Mapping, Optional, Tuple, Union


MeasureResult = namedtuple('MeasureResult', ('value', 'error', 'unit', 'pricing_key'))


class CompositeResultFuture:

    def __init__(self, futures: Iterable[Future], result_future: Optional[Future] = None):
        self._futures = tuple(futures)
        self._result_future = result_future or Future()
        self.__pending = set(range(len(self._futures)))

        for idx, future in enumerate(futures):
            if future.done():
                self.__pending.remove(idx)
            else:
                future.add_done_callback(partial(self.__cb, idx=idx))

    def __getitem__(self, item):
        return self.result()[item]

    def __cb(self, _future: Future, idx):
        self.__pending.remove(idx)
        if not self.__pending:
            self._set_result()

    def _set_result(self):
        self._result_future.set_result([f.result() for f in self._futures])

    @property
    def futures(self) -> Tuple[Future, ...]:
        return self._futures

    def done(self) -> bool:
        return self._result_future.done()

    def result(self, timeout: Optional[int] = None):
        return self._result_future.result(timeout)

    def add_done_callback(self, fn):
        self._result_future.add_done_callback(fn)


class MultipleRiskMeasureResult(dict):
    pass


class MultipleRiskMeasureFuture(CompositeResultFuture):

    def __init__(self, measures_to_futures: Mapping[RiskMeasure, Future], result_future: Optional[Future] = None):
        super().__init__(measures_to_futures.values(), result_future=result_future)
        self.__risk_measures = measures_to_futures.keys()

    def _set_result(self):
        self._result_future.set_result(MultipleRiskMeasureResult(
            dict(zip(self.__risk_measures, (f.result() for f in self.futures)))))


class PortfolioRiskResult(RiskResult):

    def __init__(self,
                 portfolio,
                 risk_measures: Iterable[RiskMeasure],
                 futures: Iterable[Future],
                 result_future: Optional[Future] = None):
        super().__init__(CompositeResultFuture(futures, result_future=result_future), tuple(risk_measures))
        self.__portfolio = portfolio

    def __getitem__(self, item):
        if isinstance(item, RiskMeasure):
            if item not in self.risk_measures:
                raise ValueError('{} not computed'.format(item))

            if len(self.risk_measures) == 1:
                return self
            else:
                return PortfolioRiskResult(self.__portfolio, (item,), self._result.futures)
        else:
            return self.__results(instruments=item)

    def __len__(self):
        return len(self._result.futures)

    def __iter__(self):
        return iter(self.__results())

    def subset(self,
               instruments: Optional[Iterable[Union[int, str, Priceable]]]):
        return PortfolioRiskResult(self.__portfolio, self.risk_measures, self.__futures(instruments))

    def aggregate(self) -> Union[float, pd.DataFrame, pd.Series]:
        return aggregate_results(self.__results())

    def __futures(self,
                  instruments: Optional[Union[int, slice, str, Priceable, Iterable[Union[int, str, Priceable]]]]) ->\
            Union[Future, Tuple[Future, ...]]:
        futures = self._result.futures

        if isinstance(instruments, (int, slice)):
            return futures[instruments]
        elif isinstance(instruments, (str, Priceable)):
            idx = None

            try:
                idx = self.__portfolio.index(instruments)
            except KeyError:
                # See if we have priced then resolved
                if isinstance(instruments, Priceable) and instruments.unresolved:
                    idx = self.__portfolio.index(instruments.unresolved)

            if idx is None:
                raise KeyError('Instrument not in portfolio')
            elif isinstance(idx, int):
                return futures[idx]
            else:
                return tuple(futures[i] for i in idx)
        else:
            return tuple(chain.from_iterable(self.__futures(i) for i in instruments))

    def __results(self,
                  instruments: Optional[Union[int, slice, str, Priceable, Iterable[Union[int, str, Priceable]]]] = (),
                  risk_measure: Optional[RiskMeasure] = None):
        futures = self.__futures(instruments) if instruments or instruments == 0 else self._result.futures
        scalar = isinstance(futures, (Future, MultipleRiskMeasureFuture))
        risk_measure = self.risk_measures[0] if len(self.risk_measures) == 1 and not risk_measure else risk_measure

        def result(future: Future):
            res = future.result()
            return res[risk_measure] if risk_measure and\
                isinstance(res, (MultipleRiskMeasureResult, MultipleRiskMeasureFuture)) else res

        return result(futures) if scalar else tuple(result(f) for f in futures)
