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
                    "primeId": "1003232152"
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
    mocker.patch.object(GsSession.current, '_get', return_value=mock_response)

    with SecMasterContext():
        asset = SecurityMaster.get_asset('GS UN', SecurityIdentifier.BBID)
    assert asset.id == 'GSPD901026E154'
    ids = asset.get_identifiers()
    assert ids[SecurityIdentifier.BBID.value] == 'GS UN'
    assert ids[SecurityIdentifier.RIC.value] == 'GS.N'
    assert ids[SecurityIdentifier.GSID.value] == 901026


def test_get_security_fields(mocker):
    mock_response = {
        "results": [
            {
                "name": "GOLDMAN SACHS GROUP INC (New York Stock)",
                "id": "GSPD901026E154",
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
                    "primeId": "1003232152"
                }
            }
        ],
        "totalResults": 1
    }
    mocker.patch.object(GsSession.current, '_get', return_value=mock_response)

    with SecMasterContext():
        asset = SecurityMaster.get_asset('GS UN', SecurityIdentifier.BBID, fields=['name', 'id'])
    assert asset.id == 'GSPD901026E154'
    assert asset.name == 'GOLDMAN SACHS GROUP INC (New York Stock)'
    ids = asset.get_identifiers()
    assert ids[SecurityIdentifier.BBID.value] == 'GS UN'
    assert ids[SecurityIdentifier.RIC.value] == 'GS.N'
    assert ids[SecurityIdentifier.PRIMEID.value] == '1003232152'


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
                "gsid": 14593
            },
            "GS UN": {
                "ric": [
                    "GS.N"
                ],
                "gsid": 901026
            }
        },
        "2021-10-12": {
            "AAPL UN": {
                "ric": [
                    "AAPL.N"
                ],
                "gsid": 14593
            },
            "GS UN": {
                "ric": [
                    "GS.N"
                ],
                "gsid": 901026
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
                "gsid": 14593,
                "bbid": "AAPL UN"
            },
            "GS UN": {
                "assetId": [
                    "MA4B66MW5E27UAHKG34"
                ],
                "gsid": 901026,
                "bbid": "GS UN"
            }
        },
        "2021-10-12": {
            "AAPL UN": {
                "assetId": [
                    "MARCRZHY163GQ4H3"
                ],
                "gsid": 14593,
                "bbid": "AAPL UN"
            },
            "GS UN": {
                "assetId": [
                    "MA4B66MW5E27UAHKG34"
                ],
                "gsid": 901026,
                "bbid": "GS UN"
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
                "gsid": 104563,
                "isin": "US90328S5001",
                "bcid": "USAT US"

            }
        },
        "2021-04-19": {
            "104563": {
                "ric": [
                    "CTLP.OQ"
                ],
                "gsid": 104563,
                "isin": "US1381031061",
                "bcid": "CTLP US"
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
