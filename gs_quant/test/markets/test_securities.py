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


if __name__ == "__main__":
    pytest.main([__file__])
