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
from gs_quant.risk import Price, RiskMeasure
from gs_quant.instrument import Instrument, EqOption, FXOption

__mappings = {
    Price: {
        EqOption: None,  # ToDo - replace with the appropriate price valuation
        FXOption: None  # ToDo - replace with the appropriate price valuation
    }
}


def get_specific_risk_measure(risk_measure: RiskMeasure, instrument: Instrument) -> RiskMeasure:
    mappings = __mappings.get(risk_measure)
    if mappings:
        return mappings.get(instrument.__class__, risk_measure)

    return risk_measure
