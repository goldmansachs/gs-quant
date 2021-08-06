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
    setattr(asset, '_Asset__type', MockType.Foo)

    mocker.patch.object(json, 'dumps', return_value='{}')
    with pytest.raises(TypeError) as exc_info:
        ata(asset)
    assert 'unsupported asset type' in str(exc_info.value)  # reached exception at end of function


class SecMasterContext:
    def __enter__(self):
        SecurityMaster.set_source(SecurityMasterSource.SECURITY_MASTER)

    def __exit__(self, exc_type, exc_value, traceback):
        SecurityMaster.set_source(SecurityMasterSource.ASSET_SERVICE)


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


def full_caps_keys(d):
    return {k.upper(): v for k, v in d.items()}


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
    mocker.patch.object(GsSession.current, '_get', side_effect=[p1, p2, p3])
    with SecMasterContext():
        output = SecurityMaster.get_all_identifiers()
    assert len(output) == 2
    assert output['GSPD901026E154'] == full_caps_keys(p1['results'][0]['identifiers'])
    assert output['GSPD14593E459'] == full_caps_keys(p2['results'][0]['identifiers'])

    mocker.patch.object(GsSession.current, '_get', side_effect=[p1, p2, p3])
    with SecMasterContext():
        output = SecurityMaster.get_all_identifiers(id_type=SecurityIdentifier.BBID)
    assert len(output) == 2
    assert output['GS UN'] == full_caps_keys(p1['results'][0]['identifiers'])
    assert output['AAPL UW'] == full_caps_keys(p2['results'][0]['identifiers'])


if __name__ == "__main__":
    pytest.main([__file__])
