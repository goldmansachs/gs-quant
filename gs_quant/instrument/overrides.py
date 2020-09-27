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
from gs_quant.priceable import PriceableImpl
from gs_quant.markets import MarketDataCoordinate
from gs_quant.risk import FloatWithInfo, DataFrameWithInfo, SeriesWithInfo, RiskMeasure
from gs_quant.risk.results import ErrorValue, PricingFuture
from gs_quant.target.instrument import EqOption as __EqOption

from typing import Iterable, Tuple, Union


class EqOption(__EqOption):

    def calc(self, risk_measure: Union[RiskMeasure, Iterable[RiskMeasure]], fn=None) ->\
        Union[DataFrameWithInfo, ErrorValue, FloatWithInfo, PriceableImpl, PricingFuture, SeriesWithInfo,
              Tuple[MarketDataCoordinate, ...]]:
        # Tactical fix until the equities pricing service notion of IRDelta is changed to match FICC

        from gs_quant.markets import PricingContext
        from gs_quant.risk import IRDelta, IRDeltaParallel

        error_result = None

        if risk_measure == IRDeltaParallel:
            risk_measure = IRDelta
        elif risk_measure == IRDelta:
            error_result = ErrorValue(None, 'IRDelta not supported for EqOption')
        elif not isinstance(risk_measure, RiskMeasure):
            if IRDelta in risk_measure:
                risk_measure = tuple(r for r in risk_measure if r != IRDelta)
            else:
                risk_measure = tuple(IRDelta if r == IRDeltaParallel else r for r in risk_measure)

        if error_result:
            return PricingFuture(error_result) if PricingContext.current.is_entered or PricingContext.current.is_async\
                else error_result
        else:
            return super().calc(risk_measure, fn=fn)
