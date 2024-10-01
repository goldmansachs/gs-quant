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

from gs_quant.api.gs.backtests_xasset.request import RiskRequest, BasicBacktestRequest
from gs_quant.api.gs.backtests_xasset.response import RiskResponse, BasicBacktestResponse
from gs_quant.session import GsSession


class GsBacktestXassetApi:
    HEADERS = {'Accept': 'application/json'}
    TIMEOUT = 90

    @classmethod
    def calculate_risk(cls, risk_request: RiskRequest) -> RiskResponse:
        response = GsSession.current._post('/backtests/xasset/risk', risk_request.to_json(),
                                           request_headers=cls.HEADERS, timeout=cls.TIMEOUT)
        result = RiskResponse.from_dict(response)
        return result

    @classmethod
    def calculate_basic_backtest(cls, backtest_request: BasicBacktestRequest, decode_instruments: bool = True) -> \
            BasicBacktestResponse:
        response = GsSession.current._post('/backtests/xasset/strategy/basic', backtest_request.to_json(),
                                           request_headers=cls.HEADERS, timeout=cls.TIMEOUT)
        result = BasicBacktestResponse.from_dict_custom(response, decode_instruments)
        return result
