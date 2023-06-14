"""
Copyright 2022 Goldman Sachs.
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

from abc import ABC, abstractmethod
from typing import Generic, Callable, Sequence, Any, TypeVar, Iterable, Union

from gs_quant.risk.core import ResultType, DataFrameWithInfo, SeriesWithInfo, FloatWithInfo

_InputT = TypeVar('_InputT')
_ResultT = TypeVar('_ResultT')


class Transformer(ABC, Generic[_InputT, _ResultT]):
    @abstractmethod
    def apply(self, data: _InputT, *args, **kwargs) -> _ResultT:
        pass


class GenericResultWithInfoTransformer(Transformer[ResultType, ResultType]):
    def __init__(self, fn: Callable[[ResultType, Sequence[Any]], ResultType]):
        self.__fn = fn

    def apply(self, data: ResultType, *args, **kwargs) -> ResultType:
        return self.__fn(data, *args, **kwargs)


class ResultWithInfoAggregator(Transformer[Iterable[ResultType], FloatWithInfo]):
    def __init__(self, risk_col: str = 'value', filter_coord=None):
        self.__risk_col = risk_col
        self.__filter_coord = filter_coord

    def apply(self, results: Iterable[Union[float, FloatWithInfo, SeriesWithInfo, DataFrameWithInfo]],
              *args, **kwargs) -> Iterable[Union[float, FloatWithInfo]]:
        flattened_results = []

        for result in results:
            if isinstance(result, float):
                flattened_results.append(result)
            else:
                if isinstance(result, FloatWithInfo):
                    val = result.raw_value
                elif isinstance(result, SeriesWithInfo):
                    val = getattr(result, self.risk_col).sum()
                elif isinstance(result, DataFrameWithInfo):
                    if self.filter_coord is not None:
                        df = result.filter_by_coord(self.filter_coord)
                        val = getattr(df, self.risk_col).sum()
                    elif result.empty:
                        val = 0
                    else:
                        val = getattr(result, self.risk_col).sum()
                else:
                    raise ValueError(f'Aggregation of {type(result).__name__} not currently supported')
                risk_key = result.risk_key
                unit = result.unit
                error = result.error
                flattened_results.append(FloatWithInfo(value=val, risk_key=risk_key, unit=unit, error=error))

        return flattened_results

    @property
    def risk_col(self):
        return self.__risk_col

    @property
    def filter_coord(self):
        return self.__filter_coord
