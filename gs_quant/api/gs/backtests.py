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
from urllib.parse import urlencode

from gs_quant.session import GsSession
from gs_quant.target.backtests import *
from gs_quant.errors import MqValueError

_logger = logging.getLogger(__name__)


class GsBacktestApi:
    """GS Backtest API client implementation"""

    @classmethod
    def get_many_backtests(cls,
                           limit: int = 100,
                           backtest_id: str = None,
                           owner_id: str = None,
                           name: str = None,
                           mq_symbol: str = None) -> Tuple[Backtest, ...]:
        query_string = urlencode(dict(filter(lambda item: item[1] is not None,
                                             dict(id=backtest_id, ownerId=owner_id, name=name,
                                                  mqSymbol=mq_symbol, limit=limit).items())))
        return GsSession.current._get('/backtests?{query}'.format(query=query_string), cls=Backtest)['results']

    @classmethod
    def get_backtest(cls, backtest_id: str) -> Backtest:
        return GsSession.current._get('/backtests/{id}'.format(id=backtest_id), cls=Backtest)

    @classmethod
    def create_backtest(cls, backtest: Backtest) -> Backtest:
        request_headers = {'Content-Type': 'application/json;charset=utf-8', 'Accept': 'application/json;charset=utf-8'}
        return GsSession.current._post('/backtests', backtest, request_headers=request_headers, cls=Backtest)

    @classmethod
    def update_backtest(cls, backtest: Backtest):
        request_headers = {'Content-Type': 'application/json;charset=utf-8', 'Accept': 'application/json;charset=utf-8'}
        return GsSession.current._put('/backtests/{id}'.format(id=backtest.id), backtest,
                                      request_headers=request_headers,
                                      cls=Backtest)

    @classmethod
    def delete_backtest(cls, backtest_id: str) -> dict:
        return GsSession.current._delete('/backtests/{id}'.format(id=backtest_id))

    @classmethod
    def get_results(cls, backtest_id: str) -> Tuple[BacktestResult, ...]:
        return GsSession.current._get('/backtests/results?id={id}'.format(id=backtest_id))['backtestResults']

    @classmethod
    def get_comparison_results(
        cls, limit: int = 100, start_date: dt.date = None, end_date: dt.date = None, backtest_id: str = None,
        comparison_id: str = None, owner_id: str = None, name: str = None, mq_symbol: str = None
    ) -> Tuple[Tuple[BacktestResult, ...], Tuple[ComparisonBacktestResult, ...]]:
        query_string = urlencode(dict(filter(lambda item: item[1] is not None,
                                             dict(id=backtest_id, comparisonIds=comparison_id, ownerId=owner_id,
                                                  name=name, mqSymbol=mq_symbol, limit=limit,
                                                  startDate=start_date.isoformat(),
                                                  endDate=end_date.isoformat()).items())))
        result = GsSession.current._get('/backtests/results?{query}'.format(query=query_string))
        return result['backtestResults'], result['comparisonResults']

    @classmethod
    def schedule_backtest(cls, backtest_id: str) -> dict:
        return GsSession.current._post('/backtests/{id}/schedule'.format(id=backtest_id))

    @classmethod
    def run_backtest(cls, backtest: Backtest, correlation_id: str = None) -> BacktestResult:
        """
        :param backtest: definition of a backtest which should be run on Marquee API
        :param correlation_id: used for logging purposes; helps in tracking all the requests which ultimately serve
               the same purpose (e.g. calculating a backtest)
        :return: result of running the backtest
        """
        request_headers = {'Content-Type': 'application/json;charset=utf-8', 'Accept': 'application/json;charset=utf-8'}
        if correlation_id is not None:
            request_headers["X-CorrelationId"] = correlation_id

        response = GsSession.current._post('/backtests/calculate', backtest, request_headers=request_headers)
        return cls.backtest_result_from_response(response)

    @classmethod
    def backtest_result_from_response(cls, response: dict) -> BacktestResult:
        if 'RiskData' not in response:
            raise MqValueError('No risk data received')

        portfolio = response['Portfolio'] if 'Portfolio' in response else None
        risks = tuple(
            BacktestRisk(name=k, timeseries=tuple(FieldValueMap(date=r['date'], value=r['value']) for r in v))
            for k, v, in response['RiskData'].items()
        )

        return BacktestResult(portfolio=portfolio, risks=risks)

    @classmethod
    def calculate_position_risk(cls, backtestRiskRequest: BacktestRiskRequest) -> dict:
        request_headers = {'Content-Type': 'application/json;charset=utf-8', 'Accept': 'application/json;charset=utf-8'}
        return GsSession.current._post('/backtests/calculate-position-risk', backtestRiskRequest,
                                       request_headers=request_headers)

    @classmethod
    def get_ref_data(cls) -> BacktestRefData:
        return GsSession.current._get('/backtests/refData', cls=BacktestRefData)

    @classmethod
    def update_ref_data(cls, backtest_ref_data: BacktestRefData):
        request_headers = {'Content-Type': 'application/json;charset=utf-8', 'Accept': 'application/json;charset=utf-8'}
        return GsSession.current._put('/backtests/refData', backtest_ref_data,
                                      request_headers=request_headers,
                                      cls=backtest_ref_data)
