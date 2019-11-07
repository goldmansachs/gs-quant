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
from gs_quant.priceable import RiskResult
from gs_quant.instrument import Instrument
from gs_quant.risk import RiskMeasure, aggregate_results

from concurrent.futures import Future
from functools import partial
from itertools import chain
import pandas as pd
from typing import Iterable, Mapping, Optional, Tuple, Union


class CompositeResultFuture:

    def __init__(self, futures: Iterable[Future]):
        self._futures = tuple(futures)
        self._result_future = Future()
        self.__pending = set(range(len(self._futures)))

        for idx, future in enumerate(futures):
            if future.done():
                self.__pending.remove(idx)
            else:
                future.add_done_callback(partial(self.__cb, idx=idx))

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


class MultipleRiskMeasureFuture(CompositeResultFuture):

    def __init__(self, measures_to_futures: Mapping[RiskMeasure, Future]):
        super().__init__(measures_to_futures.values())
        self.__risk_measures = measures_to_futures.keys()

    def __getitem__(self, item):
        return self.result()[item]

    def _set_result(self):
        self._result_future.set_result(dict(zip(self.__risk_measures, (f.result() for f in self.futures))))


class PortfolioRiskResult(RiskResult):

    def __init__(self,
                 portfolio,
                 risk_measures: Iterable[RiskMeasure],
                 futures: Iterable[Future]):
        super().__init__(CompositeResultFuture(futures), tuple(risk_measures))
        self.__portfolio = portfolio

    def __getitem__(self, item):
        if isinstance(item, RiskMeasure):
            if item not in self.risk_measures:
                raise ValueError('{} not computed'.format(item))

            return PortfolioRiskResult(self.__portfolio, (item,), self._result.futures)
        else:
            return self.__results(instruments=item)

    def __len__(self):
        return len(self._result.futures)

    def __iter__(self):
        return iter(self.__results())

    def subset(self,
               instruments: Optional[Iterable[Union[int, str, Instrument]]]):
        return PortfolioRiskResult(self.__portfolio, self.risk_measures, self.__futures(instruments))

    def aggregate(self) -> Union[float, pd.DataFrame, pd.Series]:
        return aggregate_results(self.__results())

    def __futures(self,
                  instruments: Optional[Union[int, slice, str, Instrument, Iterable[Union[int, str, Instrument]]]]) ->\
            Union[Future, Tuple[Future, ...]]:
        futures = self._result.futures
        scalar = True

        if isinstance(instruments, int):
            futures = (futures[instruments],)
        elif isinstance(instruments, slice):
            futures = futures[instruments]
        elif isinstance(instruments, (str, Instrument)):
            idx = self.__portfolio.index(instruments)
            if isinstance(idx, int):
                futures = (futures[idx],)
            else:
                scalar = False
                futures = tuple(futures[i] for i in idx)
        else:
            scalar = False
            futures = tuple(chain.from_iterable(self.__futures(i) for i in instruments))

        return next(iter(futures)) if scalar else futures

    def __results(self,
                  instruments: Optional[Union[int, slice, str, Instrument, Iterable[Union[int, str, Instrument]]]] = (),
                  risk_measure: Optional[RiskMeasure] = None):
        futures = self.__futures(instruments) if instruments or instruments == 0 else self._result.futures
        scalar = isinstance(futures, (Future, MultipleRiskMeasureFuture))
        risk_measure = self.risk_measures[0] if len(self.risk_measures) == 1 and not risk_measure else risk_measure

        def result(future: Future):
            res = future.result()
            return res[risk_measure] if risk_measure and isinstance(res, (dict, MultipleRiskMeasureFuture)) else res

        return result(futures) if scalar else tuple(result(f) for f in futures)
