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

from gs_quant.risk.core import ResultType, DataFrameWithInfo, SeriesWithInfo, FloatWithInfo, combine_risk_key

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
    def __init__(self, risk_col: str = 'value'):
        self.__risk_col = risk_col

    def apply(self, results: Iterable[Union[float, FloatWithInfo, SeriesWithInfo, DataFrameWithInfo]],
              *args, **kwargs) -> FloatWithInfo:
        val = 0
        risk_key = None
        units = set()

        for result in results:
            if isinstance(result, float):
                val += result
            elif isinstance(result, (FloatWithInfo, SeriesWithInfo, DataFrameWithInfo)):
                if isinstance(result, FloatWithInfo):
                    val += result.raw_value
                else:
                    val += getattr(result, self.risk_col).sum()
                risk_key = result.risk_key if risk_key is None else combine_risk_key(risk_key, result.risk_key)
                units.add(result.unit)
            else:
                raise ValueError(f'Aggregation of {type(result).__name__} not currently supported')

        if len(units) != 1:
            raise ValueError(f'Aggregation of {len(units)} units not currently supported. 1 unit expected.')
        return FloatWithInfo(value=val, risk_key=risk_key, unit=(list(units))[0])

    @property
    def risk_col(self):
        return self.__risk_col
