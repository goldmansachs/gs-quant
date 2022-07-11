"""
Copyright 2018 Goldman Sachs.
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
import copy
import datetime

import pytest

from gs_quant.base import EnumBase
from gs_quant.markets.securities import *
from gs_quant.session import *


def test_get_asset(mocker):
    marquee_id = 'MA1234567890'
    mock_response = GsAsset(asset_class=AssetClass.Equity, type_=GsAssetType.Single_Stock, name='Test Asset')

    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_get', return_value=mock_response)

    asset = SecurityMaster.get_asset(marquee_id, AssetIdentifier.MARQUEE_ID)

    assert asset.name == "Test Asset"
    assert asset.get_type() == AssetType.STOCK

    asset = SecurityMaster.get_asset(marquee_id, AssetIdentifier.MARQUEE_ID, as_of=dt.date.today())

    assert asset.name == "Test Asset"
    assert asset.get_type() == AssetType.STOCK

    asset = SecurityMaster.get_asset(marquee_id, AssetIdentifier.MARQUEE_ID, as_of=dt.datetime.utcnow())

    assert asset.name == "Test Asset"
    assert asset.get_type() == AssetType.STOCK

    mock_response = GsAsset(asset_class=AssetClass.Equity, type_=GsAssetType.Index, name='Test Asset')
    mocker.patch.object(GsSession.current, '_get', return_value=mock_response)

    asset = SecurityMaster.get_asset(marquee_id, AssetIdentifier.MARQUEE_ID)

    assert asset.name == "Test Asset"
    assert asset.get_type() == AssetType.INDEX

    mock_response = GsAsset(asset_class=AssetClass.Equity, type_=GsAssetType.Future, name='Test Asset')
    mocker.patch.object(GsSession.current, '_get', return_value=mock_response)

    asset = SecurityMaster.get_asset(marquee_id, AssetIdentifier.MARQUEE_ID)

    assert asset.name == "Test Asset"
    assert asset.get_type() == AssetType.FUTURE

    mock_response = GsAsset(asset_class=AssetClass.Equity, type_=GsAssetType.ETF, name='Test Asset')
    mocker.patch.object(GsSession.current, '_get', return_value=mock_response)

    asset = SecurityMaster.get_asset(marquee_id, AssetIdentifier.MARQUEE_ID)

    assert asset.name == "Test Asset"
    assert asset.get_type() == AssetType.ETF

    mock_response = GsAsset(asset_class=AssetClass.Equity, type_=GsAssetType.Custom_Basket, name='Test Asset',
                            id_=marquee_id)
    mocker.patch.object(GsSession.current, '_get', return_value=mock_response)

    asset = SecurityMaster.get_asset(marquee_id, AssetIdentifier.MARQUEE_ID)

    assert asset.name == "Test Asset"
    assert asset.get_type() == AssetType.CUSTOM_BASKET

    mock_response = {
        'results': (GsAsset(id=marquee_id, assetClass='Equity', type='Single Stock', name='Test 1'),),
    }

    mocker.patch.object(GsSession.current, '_post', return_value=mock_response)
    asset = SecurityMaster.get_asset('GS.N', AssetIdentifier.REUTERS_ID)
    assert asset.name == "Test 1"
    assert asset.get_type() == AssetType.STOCK

    asset = SecurityMaster.get_asset('GS', AssetIdentifier.TICKER, exchange_code=ExchangeCode.NYSE)
    assert asset.name == "Test 1"
    assert asset.get_type() == AssetType.STOCK

    asset = SecurityMaster.get_asset('GS', AssetIdentifier.TICKER, asset_type=AssetType.STOCK)
    assert asset.name == "Test 1"
    assert asset.get_type() == AssetType.STOCK

    mocker.patch.object(GsSession.current, '_post', return_value={'results': ()})
    asset = SecurityMaster.get_asset(marquee_id, AssetIdentifier.REUTERS_ID)
    assert asset is None


def test_asset_identifiers(mocker):
    marquee_id = 'MA1234567890'

    mocker.patch.object(
        GsSession,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mock_response = GsAsset(asset_class=AssetClass.Equity, type_=GsAssetType.Custom_Basket, name='Test Asset',
                            id_=marquee_id)
    mocker.patch.object(GsSession.current, '_get', return_value=mock_response)

    asset = SecurityMaster.get_asset(marquee_id, AssetIdentifier.MARQUEE_ID)

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

    mocker.patch.object(GsSession.current, '_get', return_value=mock_response)

    identifiers = asset.get_identifiers(dt.date.today())

    assert identifiers[AssetIdentifier.REUTERS_ID.value] == '.GSTHHVIP'
    assert identifiers[AssetIdentifier.BLOOMBERG_ID.value] == 'GSTHHVIP'
    assert identifiers[AssetIdentifier.CUSIP.value] == '9EQ24FPE5'
    assert identifiers[AssetIdentifier.TICKER.value] == 'GSTHHVIP'

    assert asset.get_identifier(AssetIdentifier.REUTERS_ID, as_of=dt.date.today()) == '.GSTHHVIP'
    assert asset.get_identifier(AssetIdentifier.BLOOMBERG_ID, as_of=dt.date.today()) == 'GSTHHVIP'
    assert asset.get_identifier(AssetIdentifier.CUSIP, as_of=dt.date.today()) == '9EQ24FPE5'
    assert asset.get_identifier(AssetIdentifier.TICKER, as_of=dt.date.today()) == 'GSTHHVIP'

    market = PricingContext(dt.date(2018, 3, 1))

    with market:
        identifiers = asset.get_identifiers()

    assert identifiers[AssetIdentifier.REUTERS_ID.value] == '.GSTHHOLD'
    assert identifiers[AssetIdentifier.BLOOMBERG_ID.value] == 'GSTHHOLD'
    assert identifiers[AssetIdentifier.CUSIP.value] == '9EQ24FOLD'
    assert identifiers[AssetIdentifier.TICKER.value] == 'GSTHHOLD'

    market = PricingContext(dt.date(2018, 3, 1))

    with market:
        identifiers = asset.get_identifiers()

    assert identifiers[AssetIdentifier.REUTERS_ID.value] == '.GSTHHOLD'
    assert identifiers[AssetIdentifier.BLOOMBERG_ID.value] == 'GSTHHOLD'
    assert identifiers[AssetIdentifier.CUSIP.value] == '9EQ24FOLD'
    assert identifiers[AssetIdentifier.TICKER.value] == 'GSTHHOLD'


def test_asset_types(mocker):
    class MockType(EnumBase, Enum):
        Foo = "Bar"

    ata = getattr(SecurityMaster, '_SecurityMaster__gs_asset_to_asset')
    assert ata is not None
    asset = GsAsset(AssetClass.Equity, None, 'Test Asset')

    mocker.patch.object(json, 'dumps', return_value='{}')
    # with pytest.raises(ValueError) as exc_info:
    #     setattr(asset, 'type', MockType.Foo)
    # assert 'is not a valid AssetType' in str(exc_info.value)  # reached exception at end of function

    with pytest.raises(AttributeError) as exc_info:
        ata(asset)
    assert "has no attribute 'value'" in str(exc_info.value)  # reached exception at end of function


class SecMasterContext:
    def __enter__(self):
        SecurityMaster.set_source(SecurityMasterSource.SECURITY_MASTER)

    def __exit__(self, exc_type, exc_value, traceback):
        SecurityMaster.set_source(SecurityMasterSource.ASSET_SERVICE)


class AssetContext:
    def __enter__(self):
        self.previous = SecurityMaster._source
        SecurityMaster.set_source(SecurityMasterSource.ASSET_SERVICE)

    def __exit__(self, exc_type, exc_value, traceback):
        SecurityMaster.set_source(self.previous)


def test_get_security(mocker):
    mocker.patch.object(GsSession, 'default_value', return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))

    mock_response = {
        "results": [
            {
                "name": "GOLDMAN SACHS GROUP INC (New York Stock)",
                "type": "Common Stock",
                "currency": "USD",
                "tags": [],
                "id": "GSPD901026E154",
                "assetClass": "Equity",
                "identifiers": {
                    "gsid": 901026,
                    "ric": "GS.N",
                    "id": "GSPD901026E154",
                    "cusip": "38141G10",
                    "sedol": "2407966",
                    "isin": "US38141G1040",
                    "ticker": "GS",
                    "bbid": "GS UN",
                    "bcid": "GS US",
                    "gss": "GS",
                    "primeId": "1003232152",
                    "assetId": "MA4B66MW5E27UAHKG34"
                },
                "company": {
                    "name": "GOLDMAN SACHS GROUP INC",
                    "identifiers": {
                        "gsCompanyId": 25998
                    }
                },
                "product": {
                    "name": "GOLDMAN SACHS GROUP INC",
                    "identifiers": {
                        "gsid": 901026
                    }
                },
                "exchange": {
                    "name": "New York Stock",
                    "identifiers": {
                        "gsExchangeId": 154
                    }
                }
            }
        ],
        "totalResults": 1
    }

    mock_identifier_history_response = {
        "results": [
            {
                "startDate": "2007-01-01",
                "endDate": "9999-99-99",
                "value": "GS",
                "updateTime": "2002-02-09T17:58:27.58Z",
                "type": "bbg"
            },
            {
                "startDate": "2007-01-01",
                "endDate": "9999-99-99",
                "value": "GS",
                "updateTime": "2002-02-09T17:57:14.546Z",
                "type": "ticker"
            },
            {
                "startDate": "2007-01-01",
                "endDate": "9999-99-99",
                "type": "assetId",
                "value": "MA4B66MW5E27UAHKG34",
                "updateTime": "2002-10-30T21:30:29.993Z"
            },
            {
                "startDate": "2007-01-01",
                "endDate": "9999-99-99",
                "type": "ric",
                "value": "GS.N",
                "updateTime": "2002-10-30T21:30:29.993Z",
                "gsExchangeId": 154
            }
        ]
    }
    mocker.patch.object(GsSession.current, '_get', side_effect=[mock_response, mock_identifier_history_response])

    with SecMasterContext():
        asset = SecurityMaster.get_asset('GS UN', SecurityIdentifier.BBID)
    assert isinstance(asset, SecMasterAsset)
    assert asset.get_marquee_id() == 'MA4B66MW5E27UAHKG34'
    ids = asset.get_identifiers()
    assert ids[SecurityIdentifier.BBG.value] == 'GS'
    assert ids[SecurityIdentifier.RIC.value] == 'GS.N'
    assert ids[SecurityIdentifier.GSID.value] == 901026


def test_get_security_fields(mocker):
    mock_response = {
        "results": [
            {
                "name": "GOLDMAN SACHS GROUP INC (New York Stock)",
                "id": "GSPD901026E154",
                "type": "Common Stock",
                "currency": "USD",
                "tags": [],
                "assetClass": "Equity",
                "identifiers": {
                    "gsid": 901026,
                    "ric": "GS.N",
                    "id": "GSPD901026E154",
                    "cusip": "38141G10",
                    "sedol": "2407966",
                    "isin": "US38141G1040",
                    "ticker": "GS",
                    "bbid": "GS UN",
                    "bcid": "GS US",
                    "gss": "GS",
                    "primeId": "1003232152",
                    "assetId": "MA4B66MW5E27UAHKG34"
                },
                "exchange": {
                    "name": "New York Stock",
                    "identifiers": {
                        "gsExchangeId": 154
                    }
                }
            }
        ],
        "totalResults": 1
    }

    mock_identifiers_response = {
        "results": [
            {
                "startDate": "2007-01-01",
                "endDate": "9999-99-99",
                "value": "GS",
                "updateTime": "2002-02-09T17:58:27.58Z",
                "type": "bbg"
            },
            {
                "startDate": "2007-01-01",
                "endDate": "9999-99-99",
                "value": "1003232152",
                "updateTime": "2003-01-16T15:22:54.1Z",
                "type": "primeId"
            },
            {
                "startDate": "2007-01-01",
                "endDate": "9999-99-99",
                "type": "assetId",
                "value": "MA4B66MW5E27UAHKG34",
                "updateTime": "2002-10-30T21:30:29.993Z"
            },
            {
                "startDate": "2007-01-01",
                "endDate": "9999-99-99",
                "type": "ric",
                "value": "GS.N",
                "updateTime": "2002-10-30T21:30:29.993Z",
                "gsExchangeId": 154
            }
        ],
    }
    mocker.patch.object(GsSession.current, '_get', side_effect=[mock_response, mock_identifiers_response])

    with SecMasterContext():
        asset = SecurityMaster.get_asset('GS UN', SecurityIdentifier.BBID, fields=['name', 'id'])
    assert isinstance(asset, SecMasterAsset)
    assert asset.get_marquee_id() == 'MA4B66MW5E27UAHKG34'
    assert asset.name == 'GOLDMAN SACHS GROUP INC (New York Stock)'
    ids = asset.get_identifiers()
    assert ids[SecurityIdentifier.BBG.value] == 'GS'
    assert ids[SecurityIdentifier.RIC.value] == 'GS.N'
    assert ids[SecurityIdentifier.PRIMEID.value] == '1003232152'
    assert ids[SecurityIdentifier.ID.value] == 'GSPD901026E154'


def test_get_identifiers(mocker):
    assets = {
        "results": [
            {
                "id": "GSPD901026E154",
                "identifiers": {
                    "bbid": "GS UN"
                }
            },
            {
                "id": "GSPD14593E459",
                "identifiers": {
                    "bbid": "AAPL UW"
                }
            }
        ],
        "totalResults": 2
    }
    ids_gs = {
        "results": [
            {
                "startDate": "2021-01-01",
                "endDate": "9999-99-99",
                "value": "38141G10",
                "updateTime": "2002-02-09T17:54:27.99Z",
                "type": "cusip"
            },
            {
                "startDate": "2021-01-01",
                "endDate": "9999-99-99",
                "value": "2407966",
                "updateTime": "2002-02-09T17:54:47.77Z",
                "type": "sedol"
            }
        ]
    }
    ids_ap = {
        "results": [
            {
                "startDate": "2021-01-01",
                "endDate": "9999-99-99",
                "value": "03783310",
                "updateTime": "2003-04-15T22:36:17.593Z",
                "type": "cusip"
            },
            {
                "startDate": "2021-01-01",
                "endDate": "9999-99-99",
                "value": "2046251",
                "updateTime": "2003-04-15T22:36:17.6Z",
                "type": "sedol"
            }
        ]
    }
    mocker.patch.object(GsSession.current, '_get', side_effect=[assets, ids_gs, ids_ap])
    with SecMasterContext():
        identifiers = SecurityMaster.get_identifiers(['GS UN', 'AAPL UW'], SecurityIdentifier.BBID)
    assert 'GS UN' in identifiers
    assert 'AAPL UW' in identifiers
    assert identifiers['GS UN'] == ids_gs['results']
    assert identifiers['AAPL UW'] == ids_ap['results']


def test_get_all_identifiers(mocker):
    p1 = {
        "results": [
            {
                "type": "Common Stock",
                "id": "GSPD901026E154",
                "assetClass": "Equity",
                "identifiers": {
                    "gsid": 901026,
                    "ric": "GS.N",
                    "id": "GSPD901026E154",
                    "bbid": "GS UN"
                }
            }
        ],
        "totalResults": 1
    }
    p2 = {
        "results": [
            {
                "type": "Common Stock",
                "id": "GSPD14593E459",
                "assetClass": "Equity",
                "identifiers": {
                    "gsid": 14593,
                    "ric": "AAPL.OQ",
                    "id": "GSPD14593E459",
                    "bbid": "AAPL UW",
                }
            }
        ],
        "totalResults": 1
    }
    p3 = {
        "results": [],
        "totalResults": 0
    }

    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_get', side_effect=[p1, p2, p3])
    with SecMasterContext():
        output = SecurityMaster.get_all_identifiers(use_offset_key=False)
    assert len(output) == 2
    assert output['GSPD901026E154'] == p1['results'][0]['identifiers']
    assert output['GSPD14593E459'] == p2['results'][0]['identifiers']

    mocker.patch.object(GsSession.current, '_get', side_effect=[p1, p2, p3])
    with SecMasterContext():
        output = SecurityMaster.get_all_identifiers(id_type=SecurityIdentifier.BBID, use_offset_key=False)
    assert len(output) == 2
    assert output['GS UN'] == p1['results'][0]['identifiers']
    assert output['AAPL UW'] == p2['results'][0]['identifiers']


def test_get_all_identifiers_with_assetTypes_not_none(mocker):
    mock_etf = {
        "results": [
            {
                "type": "ETF",
                "id": "mock_ETF_id",
                "assetClass": "Equity",
                "identifiers": {
                    "gsid": 1111111,
                    "ric": "mock_ETF_ric",
                    "id": "mock_ETF_id",
                    "bbid": "mock_ETF_bbid"
                }
            }
        ],
        "totalResults": 1
    }
    mock_stock = {
        "results": [
            {
                "type": "Common Stock",
                "id": "mock_stock_id",
                "assetClass": "Equity",
                "identifiers": {
                    "gsid": 222222,
                    "ric": "mock_stock_ric",
                    "bbid": "mock_stock_bbid"
                    # id omitted from nested dict for testing
                }
            }
        ],
        "totalResults": 1
    }
    mock_etf_and_stock = {
        "results": mock_stock['results'] + mock_etf['results'],
        "totalResults": 2
    }

    def get_identifiers_byte(*args, **kwargs):
        types = kwargs['payload']['type']
        stock_str = SecurityMaster.asset_type_to_str(asset_class=AssetClass.Equity, asset_type=AssetType.STOCK)
        if len(types) == 1 and AssetType.ETF.value in types:
            return mock_etf
        elif len(types) == 1 and stock_str in types:
            return mock_stock
        elif len(types) == 2 and stock_str in types and AssetType.ETF.value in types:
            return mock_etf_and_stock

    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))

    mocker.patch.object(GsSession.current, '_get', side_effect=get_identifiers_byte)
    with SecMasterContext():
        output = SecurityMaster.get_all_identifiers(AssetClass.Equity, types=[AssetType.ETF])
    assert len(output) == 1
    assert output['mock_ETF_id'] == mock_etf['results'][0]['identifiers']

    mocker.patch.object(GsSession.current, '_get', side_effect=get_identifiers_byte)
    with SecMasterContext():
        output = SecurityMaster.get_all_identifiers(AssetClass.Equity, types=[AssetType.STOCK])
    assert len(output) == 1
    assert output['mock_stock_id'] == mock_stock['results'][0]['identifiers']

    with SecMasterContext():
        output = SecurityMaster.get_all_identifiers(AssetClass.Equity, types=[AssetType.STOCK, AssetType.ETF])
    assert len(output) == 2
    assert output['mock_ETF_id'] == mock_etf['results'][0]['identifiers']
    assert output['mock_stock_id'] == mock_stock['results'][0]['identifiers']


def test_offset_key(mocker):
    p1 = {
        "results": [
            {
                "type": "Common Stock",
                "id": "GSPD901026E154",
                "assetClass": "Equity",
                "identifiers": {
                    "gsid": 901026,
                    "ric": "GS.N",
                    "id": "GSPD901026E154",
                    "bbid": "GS UN"
                }
            }
        ],
        "offsetKey": "qwerty",
        "totalResults": 1
    }
    p2 = {
        "results": [
            {
                "type": "Common Stock",
                "id": "GSPD14593E459",
                "assetClass": "Equity",
                "identifiers": {
                    "gsid": 14593,
                    "ric": "AAPL.OQ",
                    "id": "GSPD14593E459",
                    "bbid": "AAPL UW",
                }
            }
        ],
        "offsetKey": "azerty",
        "totalResults": 1
    }
    p3 = {
        "results": [],
        "totalResults": 0
    }

    limited = False
    hits = [0] * 3

    def fetch(*args, **kwargs):
        nonlocal limited
        if not limited:
            limited = True
            raise MqRequestError(429, 'too many requests')
        offset_key = kwargs['payload'].get('offsetKey')
        if offset_key is None:
            hits[0] += 1
            return p1
        if offset_key == "qwerty":
            hits[1] += 1
            return p2
        if offset_key == "azerty":
            hits[2] += 1
            return p3

    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_get', side_effect=fetch)
    with SecMasterContext():
        output = SecurityMaster.get_all_identifiers(sleep=0)
    assert len(output) == 2
    assert output['GSPD901026E154'] == p1['results'][0]['identifiers']
    assert output['GSPD14593E459'] == p2['results'][0]['identifiers']
    assert all(map(lambda x: x == 1, hits))

    mocker.patch.object(GsSession.current, '_get', side_effect=fetch)
    with SecMasterContext():
        output = SecurityMaster.get_all_identifiers(id_type=SecurityIdentifier.BBID, sleep=0)
    assert len(output) == 2
    assert output['GS UN'] == p1['results'][0]['identifiers']
    assert output['AAPL UW'] == p2['results'][0]['identifiers']
    assert all(map(lambda x: x == 2, hits))

    mocker.patch.object(GsSession.current, '_get', side_effect=fetch)
    with SecMasterContext():
        gen = SecurityMaster.get_all_identifiers_gen(id_type=SecurityIdentifier.BBID, sleep=0)
        page = next(gen)
        assert len(page) == 1
        assert page['GS UN'] == p1['results'][0]['identifiers']
        page = next(gen)
        assert len(page) == 1
        assert page['AAPL UW'] == p2['results'][0]['identifiers']

        with pytest.raises(StopIteration):
            next(gen)

    assert all(map(lambda x: x == 3, hits))


def test_map_identifiers(mocker):
    mock1 = {
        "results": [
            {
                "assetId": "MA4B66MW5E27U9VBB93",
                "outputType": "rcic",
                "outputValue": "AAPL.O",
                "startDate": "2021-10-11",
                "endDate": "2021-10-12",
                "input": "AAPL UN"
            },
            {
                "assetId": "MARCRZHY163GQ4H3",
                "outputType": "ric",
                "outputValue": "AAPL.N",
                "startDate": "2021-10-11",
                "endDate": "2021-10-12",
                "input": "AAPL UN"
            },
            {
                "assetId": "MA4B66MW5E27UAHKG34",
                "outputType": "ric",
                "outputValue": "GS.N",
                "startDate": "2021-10-11",
                "endDate": "2021-10-12",
                "input": "GS UN"
            },
            {
                "outputType": "rcic",
                "outputValue": "GS",
                "startDate": "2021-10-11",
                "endDate": "2021-10-12",
                "input": "GS UN"
            },
            {
                "outputType": "gsid",
                "outputValue": 14593,
                "startDate": "2021-10-11",
                "endDate": "2021-10-12",
                "input": "AAPL UN"
            },
            {
                "outputType": "gsid",
                "outputValue": 901026,
                "startDate": "2021-10-11",
                "endDate": "2021-10-12",
                "input": "GS UN"
            }
        ]
    }
    mock2 = copy.deepcopy(mock1)
    mock2["results"].extend([
        {
            "outputType": "bbg",
            "outputValue": "AAPL",
            "exchange": "UN",
            "compositeExchange": "US",
            "startDate": "2021-10-11",
            "endDate": "2021-10-12",
            "input": "AAPL UN"
        },
        {
            "outputType": "bbg",
            "outputValue": "GS",
            "exchange": "UN",
            "compositeExchange": "US",
            "startDate": "2021-10-11",
            "endDate": "2021-10-12",
            "input": "GS UN"
        }
    ])

    mocker.patch.object(GsSession.current, '_get', side_effect=[mock2, mock2])
    start = dt.date(2021, 10, 11)
    end = dt.date(2021, 10, 12)

    expected = {
        "2021-10-11": {
            "AAPL UN": {
                "ric": [
                    "AAPL.N"
                ],
                "gsid": [
                    14593
                ]
            },
            "GS UN": {
                "ric": [
                    "GS.N"
                ],
                "gsid": [
                    901026
                ]
            }
        },
        "2021-10-12": {
            "AAPL UN": {
                "ric": [
                    "AAPL.N"
                ],
                "gsid": [
                    14593
                ]
            },
            "GS UN": {
                "ric": [
                    "GS.N"
                ],
                "gsid": [
                    901026
                ]
            }
        }
    }
    with SecMasterContext():
        actual = SecurityMaster.map_identifiers(SecurityIdentifier.BBID,
                                                ['GS UN', 'AAPL UN'],
                                                [SecurityIdentifier.RIC, SecurityIdentifier.GSID],
                                                start, end)
    assert actual == expected

    expected = {
        "2021-10-11": {
            "AAPL UN": {
                "assetId": [
                    "MARCRZHY163GQ4H3"
                ],
                "gsid": [
                    14593
                ],
                "bbid": [
                    "AAPL UN"
                ]
            },
            "GS UN": {
                "assetId": [
                    "MA4B66MW5E27UAHKG34"
                ],
                "gsid": [
                    901026
                ],
                "bbid": [
                    "GS UN"
                ]
            }
        },
        "2021-10-12": {
            "AAPL UN": {
                "assetId": [
                    "MARCRZHY163GQ4H3"
                ],
                "gsid": [
                    14593
                ],
                "bbid": [
                    "AAPL UN"
                ]
            },
            "GS UN": {
                "assetId": [
                    "MA4B66MW5E27UAHKG34"
                ],
                "gsid": [
                    901026
                ],
                "bbid": [
                    "GS UN"
                ]
            }
        }
    }
    targets = [SecurityIdentifier.ASSET_ID, SecurityIdentifier.GSID, SecurityIdentifier.BBID]
    with SecMasterContext():
        actual = SecurityMaster.map_identifiers(SecurityIdentifier.BBID, ['GS UN', 'AAPL UN'], targets, start, end)
    assert actual == expected


def test_map_identifiers_change(mocker):
    mock = {
        "results": [
            {
                "outputType": "bbg",
                "outputValue": "USAT",
                "exchange": "UW",
                "compositeExchange": "US",
                "startDate": "2021-01-01",
                "endDate": "2021-04-18",
                "input": "104563"
            },
            {
                "outputType": "bbg",
                "outputValue": "CTLP",
                "exchange": "UW",
                "compositeExchange": "US",
                "startDate": "2021-04-19",
                "endDate": "2021-11-01",
                "input": "104563"
            },
            {
                "assetId": "MAY8Z19T2WE6RVHG",
                "outputType": "rcic",
                "outputValue": "USAT.O",
                "startDate": "2021-01-01",
                "endDate": "2021-04-17",
                "input": "104563"
            },
            {
                "assetId": "MA4B66MW5E27UANLYDS",
                "outputType": "ric",
                "outputValue": "USAT.OQ",
                "startDate": "2021-01-01",
                "endDate": "2021-04-17",
                "input": "104563"
            },
            {
                "assetId": "MA2640YQADTHYZ4M",
                "outputType": "rcic",
                "outputValue": "CTLP.O",
                "startDate": "2021-04-19",
                "endDate": "2021-11-01",
                "input": "104563"
            },
            {
                "assetId": "MAR754Z5RQYZ3V8E",
                "outputType": "ric",
                "outputValue": "CTLP.OQ",
                "startDate": "2021-04-19",
                "endDate": "2021-11-01",
                "input": "104563"
            },
            # additional RICs omitted from test
            {
                "outputType": "gsid",
                "outputValue": 104563,
                "startDate": "2021-01-01",
                "endDate": "2021-04-18",
                "input": "104563"
            },
            {
                "outputType": "gsid",
                "outputValue": 104563,
                "startDate": "2021-04-19",
                "endDate": "2021-11-01",
                "input": "104563"
            },
            {
                "outputType": "isin",
                "outputValue": "US90328S5001",
                "startDate": "2021-01-01",
                "endDate": "2021-04-18",
                "input": "104563"
            },
            {
                "outputType": "isin",
                "outputValue": "US1381031061",
                "startDate": "2021-04-19",
                "endDate": "2021-11-01",
                "input": "104563"
            }
        ]
    }
    mocker.patch.object(GsSession.current, '_get', side_effect=[mock])
    start = dt.date(2021, 1, 1)
    end = dt.date(2021, 11, 1)

    expected = {
        "2021-04-16": {
            "104563": {
                "ric": [
                    "USAT.OQ"
                ],
                "gsid": [
                    104563
                ],
                "isin": [
                    "US90328S5001"
                ],
                "bcid": [
                    "USAT US"
                ]
            }
        },
        "2021-04-19": {
            "104563": {
                "ric": [
                    "CTLP.OQ"
                ],
                "gsid": [
                    104563
                ],
                "isin": [
                    "US1381031061"
                ],
                "bcid": [
                    "CTLP US"
                ]
            }
        }
    }
    targets = [SecurityIdentifier.RIC, SecurityIdentifier.GSID, SecurityIdentifier.ISIN, SecurityIdentifier.BCID]
    with SecMasterContext():
        actual = SecurityMaster.map_identifiers(SecurityIdentifier.GSID, ['104563'], targets, start, end)
    for k, v in expected.items():
        assert actual[k] == v


def test_map_identifiers_empty(mocker):
    mock = {
        "results": [
        ]
    }
    mocker.patch.object(GsSession.current, '_get', side_effect=[mock])

    with SecMasterContext():
        actual = SecurityMaster.map_identifiers(SecurityIdentifier.BBID, ['invalid id'], [SecurityIdentifier.RIC])
    assert actual == {}


def test_map_identifiers_eq_index(mocker):
    """
    Test to ensure that gsq result does not append exchange or compositeExchange to Bcid and Bbid if secmaster api
    does not respond any (Mainly from mapping equity indices).
    """
    mock = {
        "results": [
            {
                "outputType": "bbg",
                "outputValue": "SPX",
                "startDate": "2022-03-17",
                "endDate": "2022-03-17",
                "input": "100"
            }
        ]
    }
    mocker.patch.object(GsSession.current, '_get', side_effect=[mock])

    with SecMasterContext():
        actual = SecurityMaster.map_identifiers(SecurityIdentifier.GSID, ['100'],
                                                [SecurityIdentifier.BBID, SecurityIdentifier.BCID])
    assert actual == {'2022-03-17': {'100': {'bbid': ['SPX']}}}


def test_secmaster_map_identifiers_with_passed_input_types(mocker):
    start = str(dt.date(2021, 10, 11))
    end = str(dt.date(2021, 10, 12))

    def mock_mapping_service_response_by_input_type(*args, **kwargs):
        '''
        Mocks Secmaster api's response json based on payload's input_type, output_type, and ids provided
        '''
        input_type = None
        for enum in SecurityIdentifier:
            if enum.value in kwargs['payload']:
                input_type = enum.value
                break
        output_types = kwargs['payload']['toIdentifiers']

        mock_output = {'results': []}
        for id in kwargs['payload'][input_type]:
            for output_type in output_types:
                row = {
                    "outputType": output_type,
                    "outputValue": "mock output for " + id,
                    "startDate": start,
                    "endDate": end,
                    "input": id
                }
                if output_type in (SecurityIdentifier.BBID, SecurityIdentifier.BBG, SecurityIdentifier.BCID):
                    row['exchange'] = 'mock-exchange'
                    row['compositeExchange'] = 'mock-comp'
                mock_output['results'].append(row)
        return mock_output

    mocker.patch.object(GsSession.current, '_get',
                        side_effect=mock_mapping_service_response_by_input_type)

    with SecMasterContext():
        mock_any_ids = ["mock-any-1", "mock-any-2"]
        any_to_cusip_results = SecurityMaster.map_identifiers(input_type=SecurityIdentifier.ANY, ids=mock_any_ids,
                                                              output_types=[SecurityIdentifier.CUSIP])
        assert start in any_to_cusip_results.keys()
        for input_id in mock_any_ids:
            assert input_id in any_to_cusip_results[start].keys()
            assert SecurityIdentifier.CUSIP.value in any_to_cusip_results[start][input_id].keys()
        assert any_to_cusip_results == {
            "2021-10-11": {
                "mock-any-1": {
                    "cusip": [
                        "mock output for mock-any-1"
                    ]
                },
                "mock-any-2": {
                    "cusip": [
                        "mock output for mock-any-2"
                    ]
                }
            },
            "2021-10-12": {
                "mock-any-1": {
                    "cusip": [
                        "mock output for mock-any-1"
                    ]
                },
                "mock-any-2": {
                    "cusip": [
                        "mock output for mock-any-2"
                    ]
                }
            }
        }

        mock_cusip_ids = ["mock-cusip-input1", "mock-cusip-input2"]
        cusip_to_isin_result = SecurityMaster.map_identifiers(input_type=SecurityIdentifier.CUSIP, ids=mock_cusip_ids,
                                                              output_types=[SecurityIdentifier.ISIN])
        assert start in cusip_to_isin_result.keys()
        for cusip_input_id in mock_cusip_ids:
            assert cusip_input_id in cusip_to_isin_result[start].keys()
            assert SecurityIdentifier.ISIN.value in cusip_to_isin_result[start][cusip_input_id].keys()
        assert cusip_to_isin_result == {
            "2021-10-11": {
                "mock-cusip-input1": {
                    "isin": [
                        "mock output for mock-cusip-input1"
                    ]
                },
                "mock-cusip-input2": {
                    "isin": [
                        "mock output for mock-cusip-input2"
                    ]
                }
            },
            "2021-10-12": {
                "mock-cusip-input1": {
                    "isin": [
                        "mock output for mock-cusip-input1"
                    ]
                },
                "mock-cusip-input2": {
                    "isin": [
                        "mock output for mock-cusip-input2"
                    ]
                }
            }
        }


def test_secmaster_map_identifiers_return_array_results(mocker):
    """
    Check if map endpoint returns multi-valued response in arrays
    """
    mock = {
        "results": [
            {
                "outputType": "bbg",
                "outputValue": "GS",
                "exchange": "UN",
                "compositeExchange": "US",
                "startDate": "2022-03-21",
                "endDate": "2022-03-21",
                "input": "38141G104"
            },
            {
                "outputType": "cusip",
                "outputValue": "38141G104",
                "startDate": "2022-03-21",
                "endDate": "2022-03-21",
                "input": "38141G104"
            },
            {
                "outputType": "bbg",
                "outputValue": "GOS",
                "exchange": "TH",
                "startDate": "2022-03-21",
                "endDate": "2022-03-21",
                "input": "38141G104"
            },
            {
                "outputType": "bbg",
                "outputValue": "GSCHF",
                "exchange": "EU",
                "startDate": "2022-03-21",
                "endDate": "2022-03-21",
                "input": "38141G104"
            },
            {
                "outputType": "bbg",
                "outputValue": "GSUSD",
                "exchange": "SE",
                "compositeExchange": "SW",
                "startDate": "2022-03-21",
                "endDate": "2022-03-21",
                "input": "38141G104"
            }
        ]
    }
    mocker.patch.object(GsSession.current, '_get', side_effect=[mock])
    with SecMasterContext():
        actual = SecurityMaster.map_identifiers(input_type=SecurityIdentifier.CUSIP, ids=['38141G104'],
                                                output_types=[SecurityIdentifier.BBID, SecurityIdentifier.BCID,
                                                              SecurityIdentifier.CUSIP])
    assert actual == {
        '2022-03-21': {
            '38141G104':
                {
                    'bbid': ['GS UN', 'GOS TH', 'GSCHF EU', 'GSUSD SE'],
                    'bcid': ['GS US', 'GSUSD SW'],
                    'cusip': ['38141G104']
                }
        }
    }


def test_secmaster_get_asset_no_asset_id_response_should_fail(mocker):
    mock_response = {
        "results": [
            {
                "name": "GOLDMAN SACHS GROUP INC (US Stock Exchange Composite)",
                "type": "Common Stock",
                "currency": "USD",
                "tags": [],
                "assetClass": "Equity",
                "identifiers": {
                    "gsid": 901026,
                    "cusip": "38141G104",
                    "cusip8": "38141G10",
                    "sedol": "2407966",
                    "isin": "US38141G1040",
                    "ticker": "GS",
                    "bcid": "GS US",
                    "primeId": "1003232152",
                    "factSetRegionalId": "JLJ0VZ-R",
                    "rcic": "GS"
                },
                "exchange": {
                    "name": "US Stock Exchange Composite",
                    "identifiers": {
                        "gsExchangeId": 161
                    }
                },
                "id": "GSPD901026E161"
            }
        ],
        "totalResults": 1,
    }

    mock_no_asset_id_response = {
        "results": []
    }
    mocker.patch.object(GsSession.current, '_get',
                        side_effect=[mock_response, mock_no_asset_id_response])

    with SecMasterContext():
        asset = SecurityMaster.get_asset(id_value="GS", id_type=SecurityIdentifier.TICKER)
        with pytest.raises(MqValueError):
            asset.get_marquee_id()


def test_secmaster_get_asset_returning_secmasterassets(mocker):
    def assert_asset_common(asset: Asset) -> None:
        with pytest.raises(MqTypeError):
            asset.get_identifier(id_type=AssetIdentifier.BLOOMBERG_ID)

    # get_asset() should return Stock instance when type: Common Stock
    mock_equity_response = {
        "results": [
            {
                "name": "GOLDMAN SACHS GROUP INC (New York Stock)",
                "type": "Common Stock",
                "currency": "USD",
                "tags": [],
                "assetClass": "Equity",
                "identifiers": {
                    "gsid": 901026,
                    "cusip": "38141G104",
                    "cusip8": "38141G10",
                    "sedol": "2407966",
                    "isin": "US38141G1040",
                    "ticker": "GS",
                    "bbid": "GS UN",
                    "bcid": "GS US",
                    "primeId": "1003232152",
                    "factSetRegionalId": "JLJ0VZ-R",
                    "rcic": "GS",
                    "ric": "GS.N",
                    "assetId": "MA4B66MW5E27UAHKG34"
                },
                "exchange": {
                    "name": "New York Stock",
                    "identifiers": {
                        "gsExchangeId": 154
                    }
                },
                "id": "GSPD901026E154",
            }
        ],
        "totalResults": 1
    }

    mock_eq_id_history_response = {
        "results": [
            {
                "startDate": "2007-01-01",
                "endDate": "9999-99-99",
                "value": "GS",
                "updateTime": "2002-02-09T17:58:27.58Z",
                "type": "bbg"
            },
            {
                "startDate": "2007-01-01",
                "endDate": "9999-99-99",
                "value": "38141G104",
                "updateTime": "2002-02-09T17:54:27.99Z",
                "type": "cusip"
            },
            {
                "startDate": "2007-01-01",
                "endDate": "9999-99-99",
                "value": "38141G10",
                "updateTime": "2002-02-09T17:54:27.99Z",
                "type": "cusip8"
            },
            {
                "startDate": "2007-01-01",
                "endDate": "9999-99-99",
                "value": "JLJ0VZ-R",
                "updateTime": "2021-08-16T08:41:43.586Z",
                "type": "factSetRegionalId"
            },
            {
                "startDate": "2007-01-01",
                "endDate": "9999-99-99",
                "value": "US38141G1040",
                "updateTime": "2002-02-09T17:55:18.513Z",
                "type": "isin"
            },
            {
                "startDate": "2007-01-01",
                "endDate": "9999-99-99",
                "value": "1003232152",
                "updateTime": "2003-01-16T15:22:54.1Z",
                "type": "primeId"
            },
            {
                "startDate": "2007-01-01",
                "endDate": "9999-99-99",
                "value": "2407966",
                "updateTime": "2002-02-09T17:54:47.77Z",
                "type": "sedol"
            },
            {
                "startDate": "2007-01-01",
                "endDate": "9999-99-99",
                "value": "GS",
                "updateTime": "2002-02-09T17:57:14.546Z",
                "type": "ticker"
            },
            {
                "startDate": "2007-01-01",
                "endDate": "9999-99-99",
                "type": "assetId",
                "value": "MA4B66MW5E27UAHKG34",
                "updateTime": "2002-10-30T21:30:29.993Z"
            },
            {
                "startDate": "2007-01-01",
                "endDate": "9999-99-99",
                "type": "ric",
                "value": "GS.N",
                "updateTime": "2002-10-30T21:30:29.993Z",
                "gsExchangeId": 154
            },
            {
                "startDate": "2007-01-01",
                "endDate": "9999-99-99",
                "value": "1003232152",
                "updateTime": "2003-01-16T15:22:54.1Z",
                "type": "primeId"
            },
        ]
    }

    mocker.patch.object(GsSession.current, '_get',
                        side_effect=[mock_equity_response, mock_eq_id_history_response])
    with SecMasterContext():
        stock = SecurityMaster.get_asset(id_value=901026, id_type=SecurityIdentifier.GSID)
    assert isinstance(stock, SecMasterAsset)
    assert stock.get_type() == AssetType.COMMON_STOCK
    assert stock.get_marquee_id() == "MA4B66MW5E27UAHKG34"
    assert stock.get_identifier(id_type=SecurityIdentifier.BBG) == "GS"
    assert stock.get_identifier(id_type=SecurityIdentifier.ID) == "GSPD901026E154"
    assert stock.get_identifier(id_type=SecurityIdentifier.ASSET_ID) == "MA4B66MW5E27UAHKG34"
    assert stock.currency == "USD"
    assert stock.get_identifiers() == \
           {'assetId': 'MA4B66MW5E27UAHKG34',
            'bbg': 'GS',
            'cusip': '38141G104',
            'cusip8': '38141G10',
            'gsid': 901026,
            'id': 'GSPD901026E154',
            'isin': 'US38141G1040',
            'primeId': '1003232152',
            'ric': 'GS.N',
            'sedol': '2407966',
            'ticker': 'GS'}
    assert_asset_common(stock)

    # get_asset() should return Index instance when type: Equity Index
    mock_index_response = {
        "results": [
            {
                "name": "S&P 500 INDEX",
                "type": "Equity Index",
                "currency": "USD",
                "tags": [],
                "assetClass": "Equity",
                "identifiers": {
                    "gsid": 100,
                    "ticker": "SPX",
                    "bbid": "SPX",
                    "ric": ".SPX",
                    "assetId": "MA4B66MW5E27U8P32SB"
                },
                "company": {
                    "name": "S&P 500 Index",
                    "identifiers": {
                        "gsCompanyId": 10756
                    }
                },
                "id": "GSPD100"
            }
        ],
        "totalResults": 1
    }
    mock_index_id_history_response = {
        "results": [
            {
                "startDate": "2007-01-01",
                "endDate": "2012-08-24",
                "value": "SPX",
                "updateTime": "2012-08-25T23:27:53.44Z",
                "type": "bbg"
            },
            {
                "startDate": "2012-08-25",
                "endDate": "2012-08-25",
                "value": "SPX",
                "updateTime": "2020-12-10T21:07:06.26Z",
                "type": "bbg"
            },
            {
                "startDate": "2012-08-26",
                "endDate": "9999-99-99",
                "value": "SPX",
                "updateTime": "2012-08-27T01:48:07.046Z",
                "type": "bbg"
            },
            {
                "startDate": "2007-01-01",
                "endDate": "2012-08-24",
                "value": "SPX",
                "updateTime": "2012-08-25T23:27:53.4Z",
                "type": "ticker"
            },
            {
                "startDate": "2012-08-25",
                "endDate": "2012-08-25",
                "value": "SPX",
                "updateTime": "2020-12-10T21:06:44.82Z",
                "type": "ticker"
            },
            {
                "startDate": "2012-08-26",
                "endDate": "9999-99-99",
                "value": "SPX",
                "updateTime": "2012-08-27T01:48:07.043Z",
                "type": "ticker"
            },
            {
                "startDate": "2007-01-01",
                "endDate": "9999-99-99",
                "type": "assetId",
                "value": "MA4B66MW5E27U8P32SB",
                "updateTime": "2003-01-14T17:28:15.29Z"
            },
            {
                "startDate": "2007-01-01",
                "endDate": "9999-99-99",
                "type": "ric",
                "value": ".SPX",
                "updateTime": "2003-01-14T17:28:15.29Z",
                "gsExchangeId": 0
            }
        ]
    }
    mocker.patch.object(GsSession.current, '_get',
                        side_effect=[mock_index_response, mock_index_id_history_response])
    with SecMasterContext():
        index = SecurityMaster.get_asset(id_value=100, id_type=SecurityIdentifier.GSID)
    assert isinstance(index, SecMasterAsset)
    assert index.get_type() == AssetType.EQUITY_INDEX
    assert index.get_marquee_id() == "MA4B66MW5E27U8P32SB"
    assert index.get_identifier(id_type=SecurityIdentifier.RIC) == ".SPX"
    assert index.get_identifier(id_type=SecurityIdentifier.ID) == "GSPD100"
    assert index.get_identifier(id_type=SecurityIdentifier.ASSET_ID) == "MA4B66MW5E27U8P32SB"
    assert index.currency == "USD"
    assert index.get_identifiers() == {
        'assetId': 'MA4B66MW5E27U8P32SB',
        'bbg': 'SPX',
        'gsid': 100,
        'id': 'GSPD100',
        'ric': '.SPX',
        'ticker': 'SPX'
    }
    assert_asset_common(index)

    # get_asset() should return ETF instance when type: ETF
    mock_ETF_response = {
        "results": [
            {
                "name": "ISHARES US TRANSPORTATION ET (BATS US Trading)",
                "type": "ETF",
                "currency": "USD",
                "tags": [],
                "assetClass": "Equity",
                "identifiers": {
                    "gsid": 159943,
                    "primeId": "355769575",
                    "bbid": "IYT UF",
                    "bcid": "IYT US",
                    "ticker": "IYT",
                    "isin": "US4642871929",
                    "sedol": "2012423",
                    "cusip": "464287192",
                    "cusip8": "46428719",
                    "rcic": "IYT",
                    "ric": "IYT.Z",
                    "assetId": "MAZ08H8QPDQ4T7SE"
                },
                "exchange": {
                    "name": "BATS US Trading",
                    "identifiers": {
                        "gsExchangeId": 535
                    }
                },
                "id": "GSPD159943E535",
            }
        ],
        "totalResults": 1
    }

    mock_etf_id_history_response = {
        "results": [
            {
                "startDate": "2007-01-01",
                "endDate": "9999-99-99",
                "value": "IYT",
                "updateTime": "2003-09-16T22:00:44.586Z",
                "type": "bbg"
            },
            {
                "startDate": "2007-01-01",
                "endDate": "9999-99-99",
                "value": "464287192",
                "updateTime": "2003-09-16T22:00:44.506Z",
                "type": "cusip"
            },
            {
                "startDate": "2007-01-01",
                "endDate": "9999-99-99",
                "value": "46428719",
                "updateTime": "2003-09-16T22:00:44.506Z",
                "type": "cusip8"
            },
            {
                "startDate": "2007-01-01",
                "endDate": "9999-99-99",
                "value": "US4642871929",
                "updateTime": "2003-09-16T22:00:44.52Z",
                "type": "isin"
            },
            {
                "startDate": "2007-01-01",
                "endDate": "9999-99-99",
                "value": "355769575",
                "updateTime": "2003-10-02T05:12:03.51Z",
                "type": "primeId"
            },
            {
                "startDate": "2007-01-01",
                "endDate": "9999-99-99",
                "value": "2012423",
                "updateTime": "2003-10-10T23:49:00.12Z",
                "type": "sedol"
            },
            {
                "startDate": "2007-01-01",
                "endDate": "9999-99-99",
                "value": "IYT",
                "updateTime": "2003-09-16T22:00:44.56Z",
                "type": "ticker"
            },
            {
                "startDate": "2008-11-09",
                "endDate": "2017-08-01",
                "type": "assetId",
                "value": "MAZ08H8QPDQ4T7SE",
                "updateTime": "2017-08-02T05:36:56.823Z"
            },
            {
                "startDate": "2017-08-03",
                "endDate": "9999-99-99",
                "type": "assetId",
                "value": "MAZ08H8QPDQ4T7SE",
                "updateTime": "2017-08-02T16:09:56.146Z"
            },
            {
                "startDate": "2008-11-09",
                "endDate": "2017-08-01",
                "type": "ric",
                "value": "IYT.Z",
                "updateTime": "2017-08-02T05:36:56.823Z",
                "gsExchangeId": 535
            },
            {
                "startDate": "2017-08-03",
                "endDate": "9999-99-99",
                "type": "ric",
                "value": "IYT.Z",
                "updateTime": "2017-08-02T16:09:56.146Z",
                "gsExchangeId": 535
            }
        ]
    }
    mocker.patch.object(GsSession.current, '_get',
                        side_effect=[mock_ETF_response, mock_etf_id_history_response])
    with SecMasterContext():
        etf = SecurityMaster.get_asset(id_value=159943, id_type=SecurityIdentifier.GSID)
    assert isinstance(etf, SecMasterAsset)
    assert etf.get_type() == AssetType.ETF
    assert etf.get_marquee_id() == "MAZ08H8QPDQ4T7SE"
    assert etf.get_identifier(id_type=SecurityIdentifier.RIC) == "IYT.Z"
    assert etf.get_identifier(id_type=SecurityIdentifier.ID) == "GSPD159943E535"
    assert etf.get_identifier(id_type=SecurityIdentifier.ASSET_ID) == "MAZ08H8QPDQ4T7SE"
    assert etf.currency == "USD"
    assert etf.get_identifiers() == {
        "gsid": 159943,
        "primeId": "355769575",
        "bbg": "IYT",
        "ticker": "IYT",
        "isin": "US4642871929",
        "sedol": "2012423",
        "cusip": "464287192",
        "cusip8": "46428719",
        "ric": "IYT.Z",
        "assetId": "MAZ08H8QPDQ4T7SE",
        'id': 'GSPD159943E535'
    }
    assert_asset_common(etf)

    # get_asset() should return Currency instance when type: Currency
    mock_currency_response = {
        "results": [
            {
                "name": "USD U.S. DOLLAR",
                "type": "Currency",
                "currency": "USD",
                "tags": [],
                "assetClass": "Cash",
                "identifiers": {
                    "gsid": 4007,
                    "assetId": "MAZ7RWC904JYHYPS",
                    "ticker": "USD"
                },
                "id": "GSPD4007"
            }
        ],
        "totalResults": 1
    }

    mock_currency_id_history_response = {
        "results": [
            {
                "startDate": "2007-01-01",
                "endDate": "9999-99-99",
                "value": "USD",
                "updateTime": "2003-05-01T16:20:44.47Z",
                "type": "ticker"
            }
        ]
    }
    mocker.patch.object(GsSession.current, '_get',
                        side_effect=[mock_currency_response, mock_currency_id_history_response])
    with SecMasterContext():
        currency = SecurityMaster.get_asset(id_value=4007, id_type=SecurityIdentifier.GSID)
    assert isinstance(currency, SecMasterAsset)
    assert currency.get_type() == AssetType.CURRENCY
    assert currency.get_marquee_id() == "MAZ7RWC904JYHYPS"
    assert currency.get_identifier(id_type=SecurityIdentifier.TICKER) == "USD"
    assert currency.get_identifier(id_type=SecurityIdentifier.ID) == "GSPD4007"
    assert currency.get_identifier(id_type=SecurityIdentifier.ASSET_ID) == "MAZ7RWC904JYHYPS"
    assert currency.get_identifiers() == {
        "gsid": 4007,
        "assetId": "MAZ7RWC904JYHYPS",
        "ticker": "USD",
        "id": "GSPD4007"
    }
    assert_asset_common(currency)


def test_get_asset_get_data_series_with_range_over_many_asset_id_should_throw_mqerror(mocker):
    mock_asset = {
        "results": [
            {
                "name": "ISHARES US TRANSPORTATION ET (BATS US Trading)",
                "type": "ETF",
                "currency": "USD",
                "tags": [],
                "assetClass": "Equity",
                "identifiers": {
                    "assetId": "MAZ08H8QPDQ4T7SE"
                },
                "exchange": {
                    "name": "BATS US Trading",
                    "identifiers": {
                        "gsExchangeId": 535
                    }
                },
                "id": "GSPD159943E535",
            }
        ],
        "totalResults": 1
    }
    mock_id_history_response = {
        "results": [
            {
                "startDate": "2020-01-01",
                "endDate": "9999-99-99",
                "value": "marqueid 1",
                "updateTime": "2003-05-01T16:20:44.47Z",
                "type": "assetId"
            },
            {
                "startDate": "2007-12-30",
                "endDate": "2019-12-31",
                "value": "marqueid 2",
                "updateTime": "2003-05-01T16:20:44.47Z",
                "type": "assetId"
            }
        ]
    }
    mocker.patch.object(GsSession.current, '_get',
                        side_effect=[mock_asset, mock_id_history_response])

    with SecMasterContext():
        asset = SecurityMaster.get_asset(id_value=4007, id_type=SecurityIdentifier.GSID)
    with pytest.raises(MqValueError):
        asset.get_hloc_prices(start=datetime.date(2007, 1, 1), end=datetime.date(2022, 1, 1))


def test_map_identifiers_asset_service(mocker):
    response = {'AAPL UN': ['AAPL.N'], 'GS UN': ['GS.N']}
    mocker.patch.object(GsAssetApi, 'map_identifiers', side_effect=lambda *arg, **kwargs: response)
    expected = {
        "2021-10-11": {
            "AAPL UN": {
                "ric": [
                    "AAPL.N"
                ]
            },
            "GS UN": {
                "ric": [
                    "GS.N"
                ]
            }
        }
    }
    with AssetContext():
        actual = SecurityMaster.map_identifiers(SecurityIdentifier.BBID,
                                                ['GS UN', 'AAPL UN'],
                                                [SecurityIdentifier.RIC],
                                                as_of_date=datetime.date(2021, 10, 11))
    assert actual == expected

    date_string = datetime.date.today().strftime('%Y-%m-%d')
    expected2 = {date_string: expected["2021-10-11"]}
    with AssetContext():
        actual2 = SecurityMaster.map_identifiers(SecurityIdentifier.BBID,
                                                 ['GS UN', 'AAPL UN'],
                                                 [SecurityIdentifier.RIC])
    assert actual2 == expected2

    mocker.patch.object(GsAssetApi, 'map_identifiers', side_effect=lambda *arg, **kwargs: {})
    with AssetContext():
        actual = SecurityMaster.map_identifiers(SecurityIdentifier.BBID,
                                                ['invalid id'],
                                                [SecurityIdentifier.RIC],
                                                as_of_date=datetime.date(2021, 10, 11))
    assert actual == {}


def test_map_identifiers_asset_service_exceptions():
    with pytest.raises(MqValueError):
        # multiple output types
        with AssetContext():
            SecurityMaster.map_identifiers(SecurityIdentifier.BBID,
                                           ['GS UN', 'AAPL UN'],
                                           [SecurityIdentifier.RIC, SecurityIdentifier.GSID],
                                           as_of_date=datetime.date(2021, 10, 11))

    with pytest.raises(MqValueError):
        # start date
        with AssetContext():
            SecurityMaster.map_identifiers(SecurityIdentifier.BBID,
                                           ['GS UN', 'AAPL UN'],
                                           [SecurityIdentifier.RIC],
                                           start_date=datetime.date(2021, 10, 11))

    with pytest.raises(MqValueError):
        # end date
        with AssetContext():
            SecurityMaster.map_identifiers(SecurityIdentifier.BBID,
                                           ['GS UN', 'AAPL UN'],
                                           [SecurityIdentifier.RIC],
                                           end_date=datetime.date(2021, 10, 11))

    with pytest.raises(MqValueError):
        # unsupported output type
        with AssetContext():
            SecurityMaster.map_identifiers(SecurityIdentifier.BBID,
                                           ['GS UN', 'AAPL UN'],
                                           [SecurityIdentifier.BBG])


if __name__ == "__main__":
    pytest.main([__file__])
