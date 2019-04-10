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
from typing import Iterable, Union
from gs_quant.risk import Formatters, RiskRequest


class RiskApi(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def calc(cls, request: RiskRequest) -> Union[Iterable, str]:
        raise NotImplementedError('Must implement calc')

    @classmethod
    @abstractmethod
    def get_results(cls, risk_request: RiskRequest, result_id: str) -> dict:
        raise NotImplementedError('Must implement get_results')

    @classmethod
    def _handle_results(cls, request: RiskRequest, results: Iterable) -> dict:
        formatted_results = {}

        for measure_idx, position_results in enumerate(results):
            risk_measure = request.measures[measure_idx]
            formatter = Formatters.get(risk_measure)
            for position_idx, result in enumerate(position_results):
                position = request.positions[position_idx]
                result = formatter(result) if formatter else result
                formatted_results.setdefault(risk_measure, {})[position] = result

        return formatted_results
