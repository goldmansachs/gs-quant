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
import logging
from typing import Iterable, Mapping, Optional, Tuple, Union

from gs_quant.base import PricingKey
from gs_quant.risk import ErrorValue, RiskRequest
from gs_quant.risk.result_handlers import result_handlers


_logger = logging.getLogger(__name__)


class RiskApi(metaclass=ABCMeta):

    @classmethod
    def calc_multi(cls, requests: Iterable[RiskRequest]) -> Tuple[Union[dict, str], ...]:
        return tuple(cls.calc(request) for request in requests)

    @classmethod
    @abstractmethod
    def calc(cls, request: RiskRequest) -> Union[dict, str]:
        ...

    @classmethod
    @abstractmethod
    def get_results(cls, ids_to_requests: Mapping[str, RiskRequest], poll: bool, timeout: Optional[int] = None)\
            -> Mapping[RiskRequest, Union[Exception, dict]]:
        ...

    @classmethod
    def _handle_results(cls, request: RiskRequest, results: Iterable) -> dict:
        formatted_results = {}

        pricing_key = PricingKey(
            request.pricing_and_market_data_as_of,
            request.pricing_location.value,
            request.parameters,
            request.scenario
        )

        for measure_idx, position_results in enumerate(results):
            risk_measure = request.measures[measure_idx]

            for position_idx, date_results in enumerate(position_results):
                if len(date_results) != len(pricing_key):
                    raise RuntimeError('Number of results did not match requested days')

                handler = result_handlers.get(date_results[0].get('$type'))
                position = request.positions[position_idx]

                try:
                    date_results = handler(date_results, pricing_key, position.instrument) if handler else date_results
                except Exception as e:
                    error = str(e)
                    date_results = ErrorValue(pricing_key, error)
                    _logger.error(error)

                formatted_results.setdefault(risk_measure, {})[position] = date_results

        return formatted_results
