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
import datetime as dt
import logging
from urllib.parse import urlencode

from gs_quant.session import GsSession
from gs_quant.target.backtests import Backtest, Tuple, BacktestResult, BacktestRefData

_logger = logging.getLogger(__name__)


class GsBacktestApi:
    """GS Backtest API client implementation"""

    @classmethod
    def get_backtests(cls,
                     limit: int = 100,
                     backtest_id: str = None,
                     owner_id: str = None,
                     name: str = None,
                     mqSymbol: str = None) -> Tuple[Backtest, ...]:
        query_string = urlencode(dict(filter(lambda item: item[1] is not None,
                                             dict(id=backtest_id, ownerId=owner_id, name=name,
                                                  mqSymbol=mqSymbol, limit=limit).items())))
        return GsSession.current._get('/backtests?{query}'.format(query=query_string), cls=Backtest)['results']

    @classmethod
    def get_backtest(cls, backtest_id: str) -> Backtest:
        return GsSession.current._get('/backtests/{id}'.format(id=backtest_id), cls=Backtest)

    @classmethod
    def create_backtest(cls, backtest: Backtest) -> Backtest:
        request_headers = {'Content-Type': 'application/json;charset=utf-8'}
        return GsSession.current._post('/backtests', backtest, request_headers=request_headers, cls=Backtest)

    @classmethod
    def update_backtest(cls, backtest: Backtest):
        request_headers = {'Content-Type': 'application/json;charset=utf-8'}
        return GsSession.current._put('/backtests/{id}'.format(id=backtest.id), backtest, request_headers=request_headers,
                                      cls=Backtest)

    @classmethod
    def delete_backtest(cls, backtest_id: str) -> dict:
        return GsSession.current._delete('/backtests/{id}'.format(id=backtest_id))

    @classmethod
    def get_results(cls,
                    limit: int = 100,
                    startDate: dt.date = None,
                    endDate: dt.date = None,
                    backtest_id: str = None,
                    comparison_id: str = None,
                    owner_id: str = None,
                    name: str = None,
                    mqSymbol: str = None) -> Tuple[BacktestResult, ...]:
        query_string = urlencode(dict(filter(lambda item: item[1] is not None,
                                             dict(ids=backtest_id, comparisonIds=comparison_id, ownerId=owner_id,
                                                  name=name, mqSymbol=mqSymbol, limit=limit,
                                                  startDate=startDate.isoformat(), endDate=endDate.isoformat()).items())))
        return GsSession.current._get('/backtests/results?{query}'.format(query=query_string))['backtestResults']

    @classmethod
    def schedule_backtest(cls, backtest_id: str) -> dict:
        return GsSession.current._post('/backtests/{id}/schedule'.format(id=backtest_id))

    @classmethod
    def get_refData(cls) -> BacktestRefData:
        return GsSession.current._get('/backtests/refData', cls=BacktestRefData)

    @classmethod
    def update_refData(cls, backtestRefData: BacktestRefData):
        request_headers = {'Content-Type': 'application/json;charset=utf-8'}
        return GsSession.current._put('/backtests/refData', backtestRefData,
                                      request_headers=request_headers,
                                      cls=backtestRefData)