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

from gs_quant.api.base import Priceable
from gs_quant.api.risk import FormattedRiskMeasure, RiskMeasure, RiskRequest, RiskPosition, CoordinatesRequest, MarketDataCoordinate
from gs_quant.context_base import ContextBaseWithDefault
from gs_quant.datetime.date import adjust_to_business_date
from gs_quant.session import GsSession
import asyncio
from collections import namedtuple
from collections.abc import Iterable as IterableType
from datetime import date, timedelta
from concurrent.futures import Future
from typing import Union, Iterable, List, Callable, Optional

PositionRequest = namedtuple('PositionRequest', ('position', 'future', ))
Target = Union[Priceable, RiskPosition, Iterable[Priceable], Iterable[RiskPosition]]


class PricingContext(ContextBaseWithDefault):

    """A context containing pricing parameters such as date"""

    def __init__(self, is_async: bool = False, pricing_date: date = None):
        super().__init__()
        self.__is_async = is_async
        self.__pricing_date = pricing_date or adjust_to_business_date(date.today() + timedelta(days=-1), prev=True)
        self.__pending_requests = {}

    def _on_exit(self, exc_type, exc_val, exc_tb):
        if self.__pending_requests:
            for risk_measure, (positions, futures) in self.__pending_requests.items():
                self.__exec(risk_measure, positions, futures)
            self.__pending_requests.clear()

    @staticmethod
    def __positions(target: Target) -> Iterable[RiskPosition]:
        positions = []

        def add_position(elem):
            if isinstance(elem, Priceable):
                positions.append(RiskPosition(elem, 1))
                return True
            elif isinstance(elem, RiskPosition):
                positions.append(elem)
                return True

            return False

        if not add_position(target):
            if isinstance(target, IterableType) and not isinstance(target, str):
                for position_elem in target:
                    if not add_position(position_elem):
                        raise TypeError('Unsupported value for target{}'.format(position_elem))

        return positions

    def __exec(self, risk_measure: Union[RiskMeasure, FormattedRiskMeasure], positions: Iterable[RiskPosition], futures: List = None) -> Optional[List]:
        formatter = risk_measure.formatter if isinstance(risk_measure, FormattedRiskMeasure) else None
        risk_measure = risk_measure.risk_measure if isinstance(risk_measure, FormattedRiskMeasure) else risk_measure
        risk_request = RiskRequest(positions, (risk_measure,), asOf=self.pricing_date, waitForResults=not self.is_async)
        response = GsSession.current._post(r'/risk/calculate', risk_request)

        if self.is_async:
            asyncio.run(self.__wait_for_results(response['reportId'], futures, formatter))
        else:
            if self._is_entered:
                self.__complete_futures(response[0], futures, formatter)
            else:
                return [formatter(r) if formatter else r for r in response[0]]

    @staticmethod
    async def __wait_for_results(results_id: str, futures: List[Future], formatter: Callable):
        session = GsSession.current
        results = session._get(r'/risk/calculate/{}'.format(results_id))

        while not isinstance(results, list):
            await asyncio.sleep(1)
            results = session._get(r'/risk/calculate/{}'.format(results_id))

        PricingContext.__complete_futures(results[0], futures, formatter)

    @staticmethod
    def __complete_futures(results: Iterable, futures: List[Future], formatter: Callable):
        for idx, result in enumerate(results):
            result = formatter(result) if formatter else result
            futures[idx].set_result(result)

    @property
    def is_async(self) -> bool:
        """Is execution asynchronous?"""
        return self.__is_async

    @property
    def pricing_date(self) -> date:
        """Pricing date"""
        return self.__pricing_date

    @pricing_date.setter
    def pricing_date(self, value: date):
        self.__pricing_date = value

    def calc(self, target: Target, risk_measure: Union[RiskMeasure, FormattedRiskMeasure]) -> Union[List[dict], List[Future]]:
        """Calculate the risk measures"""
        positions = self.__positions(target)

        if self._is_entered:
            futures = [Future() for _ in positions]
            existing_positions, existing_futures = self.__pending_requests.setdefault(risk_measure, ([], []))
            existing_positions.extend(positions)
            existing_futures.extend(futures)
            return futures
        else:
            return self.__exec(risk_measure, positions)

    def coordinates(self, priceables: Iterable[Priceable]) -> List[MarketDataCoordinate]:
        coordinates_request = CoordinatesRequest(self.pricing_date, instruments=priceables)
        response = GsSession.current._post(r'/risk/coordinates', coordinates_request)

        return [MarketDataCoordinate(
            marketDataType=r.get('marketDataType'),
            assetId=r.get('assetId'),
            pointClass=r.get('pointClass'),
            point=r.get('point'),
            field=r.get('field'))
            for r in response
        ]

