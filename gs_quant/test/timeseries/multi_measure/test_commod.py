"""
Copyright 2021 Goldman Sachs.
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
import datetime
import pandas as pd
import pytest
from gs_quant.timeseries import USE_DISPLAY_NAME
from pandas.testing import assert_series_equal
from testfixtures import Replacer

from gs_quant.api.gs.data import MarketDataResponseFrame
from gs_quant.data import DataContext
from gs_quant.errors import MqError
from gs_quant.markets.securities import CommodityNaturalGasHub, Cross
from gs_quant import timeseries as tm

_test_datasets = ('TEST_DATASET',)


@pytest.mark.skipif(not USE_DISPLAY_NAME, reason="requires certain evnvar to run")
def test_forward_price():
    # Tests for US NG assets
    def mock_natgas_forward_price(_cls, _q, ignore_errors=False):
        d = {
            'forwardPrice': [
                2.880,
                2.844,
                2.726,
            ],
            'contract': [
                "F21",
                "G21",
                "H21",
            ]
        }
        df = MarketDataResponseFrame(data=d, index=pd.to_datetime([datetime.date(2019, 1, 2)] * 3))
        df.dataset_ids = _test_datasets
        return df

    replace = Replacer()
    replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', mock_natgas_forward_price)
    mock = CommodityNaturalGasHub('MA001', 'AGT')

    with DataContext(datetime.date(2019, 1, 2), datetime.date(2019, 1, 2)):
        actual = pd.Series(tm.forward_price(mock, price_method='GDD', contract_range='F21'))
        expected = pd.Series([2.880], index=[datetime.date(2019, 1, 2)], name='price')
        assert_series_equal(expected, actual)

    with pytest.raises(MqError):
        tm.forward_price(Cross('MA002', 'USD/EUR'), price_method='GDD', contract_range='F21')

    replace.restore()


if __name__ == "__main__":
    pytest.main(args=["test_commod.py"])
