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
from abc import ABCMeta
from concurrent.futures import Future
from typing import Mapping
from gs_quant.base import Priceable
from gs_quant.risk import RiskMeasure, RiskRequest

RiskFutureMapping = Mapping[RiskMeasure, Mapping[Priceable, Future]]


class RiskApi(metaclass=ABCMeta):

    def calc(self, request: RiskRequest, futures: RiskFutureMapping, is_async: bool, is_batch: bool):
        raise NotImplementedError('Must implement calc')

    def resolve_fields(self, priceable: Priceable):
        raise NotImplementedError('Must implement resolve_fields')
