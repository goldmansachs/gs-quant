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

from gs_quant.base import RiskKey
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
    def get_results(cls, ids_to_requests: Mapping[str, RiskRequest], timeout: Optional[int] = None)\
            -> Mapping[RiskRequest, Union[Exception, dict]]:
        ...

    @classmethod
    def _handle_results(cls, request: RiskRequest, results: Iterable) -> dict:
        formatted_results = {}

        for risk_measure, position_results in zip(request.measures, results):
            for position, date_results in zip(request.positions, position_results):
                for as_of, date_result in zip(request.pricing_and_market_data_as_of, date_results):
                    handler = result_handlers.get(date_result.get('$type'))
                    risk_key = RiskKey(
                        cls,
                        as_of.pricing_date,
                        as_of.market,
                        request.parameters,
                        request.scenario,
                        risk_measure
                    )

                    try:
                        result = handler(date_result, risk_key, position.instrument) if handler else date_result
                    except Exception as e:
                        result = ErrorValue(risk_key, str(e))
                        _logger.error(result)

                    formatted_results[(risk_key, position.instrument)] = result

        return formatted_results
