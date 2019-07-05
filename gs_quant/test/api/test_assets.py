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
import testfixtures
from gs_quant.session import *
from gs_quant.api.gs.assets import GsAssetApi, GsAsset, GsTemporalXRef
from gs_quant.target.assets import Position, PositionSet, EntityQuery
from gs_quant.target.common import FieldFilterMap, XRef


def test_get_asset(mocker):
    marquee_id = 'MQA1234567890'

    mock_response = GsAsset(id=marquee_id, assetClass='Equity', type='Single Stock', name='Test Asset')

    # mock GsSession
    mocker.patch.object(GsSession.__class__, 'current',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_get', return_value=mock_response)

    # run test
    response = GsAssetApi.get_asset(marquee_id)

    GsSession.current._get.assert_called_with('/assets/{id}'.format(id=marquee_id), cls=GsAsset)

    assert response == mock_response


def test_get_many_assets(mocker):
    marquee_id_1 = 'MQA1234567890'
    marquee_id_2 = 'MQA4567890123'

    query = {'id': [marquee_id_1, marquee_id_2]}
    as_of = dt.datetime.utcnow()

    inputs = EntityQuery(
        where=FieldFilterMap(**query),
        fields=None,
        asOfTime=as_of,
        limit=100
    )

    mock_response = {'results': (
        GsAsset.from_dict({'id': marquee_id_1, 'assetClass': 'Equity', 'type': 'Single Stock', 'name': 'Test 1'}),
        GsAsset.from_dict({'id': marquee_id_2, 'assetClass': 'Equity', 'type': 'Single Stock', 'name': 'Test 2'})
    )}

    expected_response = (
        GsAsset(id=marquee_id_1, assetClass='Equity', type='Single Stock', name='Test 1'),
        GsAsset(id=marquee_id_2, assetClass='Equity', type='Single Stock', name='Test 2')
    )

    # mock GsSession
    mocker.patch.object(GsSession.__class__, 'current',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_post', return_value=mock_response)

    # run test
    response = GsAssetApi.get_many_assets(id=[marquee_id_1, marquee_id_2], as_of=as_of)

    GsSession.current._post.assert_called_with('/assets/query', cls=GsAsset, payload=inputs)
    assert response == expected_response


def test_get_asset_xrefs(mocker):
    marquee_id = 'MQA1234567890'

    mock_response = {'xrefs': (
        {
            'startDate': '1952-01-01',
            'endDate': '2018-12-31',
            'identifiers': {
                'ric': '.GSTHHOLD',
                'bbid': 'GSTHHOLD',
                'cusip': '9EQ24FOLD',
                'ticker': 'GSTHHOLD'
            }
        },
        {
            'startDate': '2019-01-01',
            'endDate': '2952-12-31',
            'identifiers': {
                'ric': '.GSTHHVIP',
                'bbid': 'GSTHHVIP',
                'cusip': '9EQ24FPE5',
                'ticker': 'GSTHHVIP',
            }
        }
    )}

    expected_response = (
        GsTemporalXRef(dt.date(1952, 1, 1), dt.date(2018, 12, 31), XRef(
            ric='.GSTHHOLD',
            bbid='GSTHHOLD',
            cusip='9EQ24FOLD',
            ticker='GSTHHOLD',
        )),
        GsTemporalXRef(dt.date(2019, 1, 1), dt.date(2952, 12, 31), XRef(
            ric='.GSTHHVIP',
            bbid='GSTHHVIP',
            cusip='9EQ24FPE5',
            ticker='GSTHHVIP',
        ))
    )

    # mock GsSession
    mocker.patch.object(GsSession.__class__, 'current',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_get', return_value=mock_response)

    # run test
    response = GsAssetApi.get_asset_xrefs(marquee_id)

    GsSession.current._get.assert_called_with('/assets/{id}/xrefs'.format(id=marquee_id))
    testfixtures.compare(response, expected_response)


def test_get_asset_positions_for_date(mocker):
    marquee_id = 'MQA1234567890'
    position_date = dt.date(2019, 2, 19)

    mock_response = {'results': (
        {
            'id': 'mock1',
            'positionDate': '2019-02-19',
            'lastUpdateTime': '2019-02-19T12:10:32.401Z',
            'positions': [
                {'assetId': 'MQA123', 'quantity': 0.3},
                {'assetId': 'MQA456', 'quantity': 0.7}
            ],
            'type': 'open',
            'divisor': 100
        },
        {
            'id': 'mock2',
            'positionDate': '2019-02-19',
            'lastUpdateTime': '2019-02-20T05:04:32.981Z',
            'positions': [
                {'assetId': 'MQA123', 'quantity': 0.4},
                {'assetId': 'MQA456', 'quantity': 0.6}
            ],
            'type': 'close',
            'divisor': 120
        }
    )}

    expected_response = (
        PositionSet('mock1', dt.date(2019, 2, 19), dup.parse('2019-02-19T12:10:32.401Z'), (
            Position(assetId='MQA123', quantity=0.3),
            Position(assetId='MQA456', quantity=0.7)
        ), 'open', 100),
        PositionSet('mock2', dt.date(2019, 2, 19), dup.parse('2019-02-20T05:04:32.981Z'), (
            Position(assetId='MQA123', quantity=0.4),
            Position(assetId='MQA456', quantity=0.6)
        ), 'close', 120)
    )

    # mock GsSession
    mocker.patch.object(GsSession.__class__, 'current',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_get', return_value=mock_response)

    # run test
    response = GsAssetApi.get_asset_positions_for_date(marquee_id, position_date)

    GsSession.current._get.assert_called_with('/assets/{id}/positions/{date}'.format(
        id=marquee_id, date=position_date))

    testfixtures.compare(response, expected_response)

    mock_response = {'results': [{
        'id': 'mock',
        'positionDate': '2019-02-19',
        'lastUpdateTime': '2019-02-20T05:04:32.981Z',
        'positions': [
            {'assetId': 'MQA123', 'quantity': 0.4},
            {'assetId': 'MQA456', 'quantity': 0.6}
        ],
        'type': 'close',
        'divisor': 120
    }]}

    expected_response = (
        PositionSet('mock', dt.date(2019, 2, 19), dup.parse('2019-02-20T05:04:32.981Z'), (
            Position(assetId='MQA123', quantity=0.4),
            Position(assetId='MQA456', quantity=0.6)
        ), 'close', 120),
    )

    # mock GsSession
    mocker.patch.object(GsSession.__class__, 'current',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_get', return_value=mock_response)

    # run test

    response = GsAssetApi.get_asset_positions_for_date(marquee_id, position_date, "close")

    testfixtures.compare(response, expected_response)

    GsSession.current._get.assert_called_with('/assets/{id}/positions/{date}?type=close'.format(
        id=marquee_id, date=position_date))
