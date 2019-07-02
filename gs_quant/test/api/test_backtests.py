"""
Copyright 2018 Goldman Sachs.
Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""

import datetime as dt
import dateutil.parser as dup
from gs_quant.session import *
from gs_quant.api.gs.backtests import GsBacktestApi, Backtest, BacktestResult, BacktestRefData
from gs_quant.target.common import *

def test_get_many_backtests(mocker):
    id_1 = 'BT1'
    id_2 = 'BT2'

    mock_response = {'results': (
        Backtest.from_dict({'id': id_1, 'assetClass': 'Commod', 'type': 'Basket', 'name': 'Example Backtest 1'}),
        Backtest.from_dict({'id': id_2, 'assetClass': 'Commod', 'type': 'Basket', 'name': 'Example Backtest 2'})
    ), 'totalResults': 2}

    expected_response = (
        Backtest(id=id_1, assetClass="Commod", type="Basket", name='Example Backtest 1'),
        Backtest(id=id_2, assetClass="Commod", type="Basket", name='Example Backtest 2')
    )

    # mock GsSession
    mocker.patch.object(GsSession.__class__, 'current', return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_get', return_value=mock_response)

    # run test
    response = GsBacktestApi.get_backtests()
    GsSession.current._get.assert_called_with('/backtests?limit=100', cls=Backtest)
    assert response == expected_response

def test_get_backtest(mocker):
    id_1 = 'BT1'
    mock_response = Backtest(id=id_1, assetClass="Commod", type="Basket", name='Example Backtest')

    # mock GsSession
    mocker.patch.object(GsSession.__class__, 'current', return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_get', return_value=mock_response)

    # run test
    response = GsBacktestApi.get_backtest(id_1)
    GsSession.current._get.assert_called_with('/backtests/{id}'.format(id=id_1), cls=Backtest)
    assert response == mock_response

def test_create_backtest(mocker):
    id_1 = 'BT1'

    backtest = Backtest(id=id_1, assetClass="Commod", type="Basket", name='Example Backtest')

    # mock GsSession
    mocker.patch.object(GsSession.__class__, 'current', return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_post', return_value=backtest)

    # run test
    response = GsBacktestApi.create_backtest(backtest)
    request_headers = {'Content-Type': 'application/json;charset=utf-8'}
    GsSession.current._post.assert_called_with('/backtests', backtest, request_headers=request_headers, cls=Backtest)
    assert response == backtest


def test_update_backtest(mocker):
    id_1 = 'BT1'

    backtest = Backtest(id=id_1, assetClass="Commod", type="Basket", name='Example Backtest')

    # mock GsSession
    mocker.patch.object(GsSession.__class__, 'current', return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_put', return_value=backtest)

    # run test
    response = GsBacktestApi.update_backtest(backtest)
    request_headers = {'Content-Type': 'application/json;charset=utf-8'}
    GsSession.current._put.assert_called_with('/backtests/{id}'.format(id=id_1), backtest, request_headers=request_headers, cls=Backtest)
    assert response == backtest


def test_delete_backtest(mocker):
    id_1 = 'BT1'

    mock_response = "Successfully deleted backtest."

    # mock GsSession
    mocker.patch.object(GsSession.__class__, 'current', return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_delete', return_value=mock_response)

    # run test
    response = GsBacktestApi.delete_backtest(id_1)
    GsSession.current._delete.assert_called_with('/backtests/{id}'.format(id=id_1))
    assert response == mock_response


def test_get_backtest_results(mocker):
    id_1 = 'BT1'
    start_date = dt.date(2019, 2, 18)
    end_date = dt.date(2019, 2, 19)

    mock_response = {'backtestResults': (
        BacktestResult('BT1', performance=(
            FieldValueMap(date='2019-02-18', price=100),
            FieldValueMap(date='2019-02-19', price=99),
        ), stats=None, history=[], backtestVersion=1)
    )}

    expected_response = BacktestResult('BT1', performance=(
            FieldValueMap(date='2019-02-18', price=100),
            FieldValueMap(date='2019-02-19', price=99),
        ), stats=None, history=[], backtestVersion=1)


    # mock GsSession
    mocker.patch.object(GsSession.__class__, 'current', return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_get', return_value=mock_response)

    # run test
    response = GsBacktestApi.get_results(startDate=start_date, endDate=end_date, backtest_id=id_1)

    GsSession.current._get.assert_called_with('/backtests/results?ids={id}&limit=100&startDate={sd}&endDate={ed}'.format(
        id=id_1, sd=start_date, ed=end_date))

    assert response == expected_response

def test_schedule_backtest(mocker):
    id_1 = 'BT1'

    mock_response = "Successfully scheduled backtest."

    # mock GsSession
    mocker.patch.object(GsSession.__class__, 'current', return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_post', return_value=mock_response)

    # run test
    response = GsBacktestApi.schedule_backtest(backtest_id=id_1)
    GsSession.current._post.assert_called_with('/backtests/{id}/schedule'.format(id=id_1))
    assert response == mock_response