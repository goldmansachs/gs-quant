"""
Copyright 2019 Goldman Sachs.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on ans
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""
from unittest.mock import Mock

import pandas as pd
from testfixtures import Replacer

import gs_quant.timeseries.tca as tm
from gs_quant.markets.index import Index
from gs_quant.target.common import AssetClass


def test_covariance():
    mock_spx_1 = Index('MA890', AssetClass.Equity, 'SPX', entity={'type': 'Index', 'underlying_asset_ids': []})
    mock_spx_2 = Index('MA890', AssetClass.Equity, 'SPX', entity={'type': 'Index', 'underlying_asset_ids': []})

    replace = Replacer()
    mock_data = pd.DataFrame(data={"assetId": ["MA00S9PEKCD2NQBD"],
                                   "bucketStart": ["19:30:00"],
                                   "bucketEnd": ["20:00:00"],
                                   "asset2Id": ["MAZYGB8GAYB9ZFQ1"],
                                   "covariance": [5.0717E-6]
                                   },
                             index=[pd.Timestamp('2021-12-20'), pd.Timestamp('2021-12-20')])
    mock_request = replace('gs_quant.data.dataset.Dataset.get_data', Mock())
    mock_request.return_value = mock_data

    tm.covariance(mock_spx_1, mock_spx_2, '19:30:00', '20:00:00')
