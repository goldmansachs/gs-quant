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

from gs_quant.api.gs.assets import GsAssetApi
from gs_quant.api.gs.data import GsDataApi
from gs_quant.api.utils import ThreadPoolManager
from gs_quant.common import AssetClass
from gs_quant.markets.indices_utils import BasketType, get_flagships_constituents


def _mock_flagship_constituents_dependencies(mocker):
    mocker.patch('gs_quant.markets.indices_utils.prev_business_date', return_value=dt.date(2026, 9, 11))
    mocker.patch(
        'gs_quant.markets.indices_utils.__get_baskets',
        return_value=[{'id': 'MA_TEST_BASKET'}],
    )

    coverage_mock = mocker.patch.object(
        GsDataApi,
        'get_coverage',
        return_value=[
            {
                'assetId': 'MA_TEST_BASKET',
                'assetClass': AssetClass.Equity,
                'type': BasketType.CUSTOM_BASKET,
                'id': 'MA_TEST_BASKET',
                'name': 'Test Basket',
                'ticker': 'GSMBTEST',
                'region': 'Americas',
                'styles': [],
                'liveDate': '2021-01-01',
            }
        ],
    )

    mocker.patch.object(
        ThreadPoolManager,
        'run_async',
        return_value=[[{'assetId': 'MA_TEST_BASKET', 'underlyingAssetId': 'MA_UNDER_1'}]],
    )
    mocker.patch.object(
        GsAssetApi,
        'get_many_assets_data_scroll',
        return_value=[{'id': 'MA_UNDER_1'}],
    )

    return coverage_mock


def test_get_flagships_constituents_coverage_includes_history_by_default(mocker):
    coverage_mock = _mock_flagship_constituents_dependencies(mocker)

    get_flagships_constituents(start=dt.date(2026, 9, 11), end=dt.date(2026, 9, 11))

    coverage_mock.assert_called_once()
    assert coverage_mock.call_args.kwargs['include_history'] is True


def test_get_flagships_constituents_coverage_respects_include_history_override(mocker):
    coverage_mock = _mock_flagship_constituents_dependencies(mocker)

    get_flagships_constituents(start=dt.date(2026, 9, 11), end=dt.date(2026, 9, 11), include_history=False)

    coverage_mock.assert_called_once()
    assert coverage_mock.call_args.kwargs['include_history'] is False
