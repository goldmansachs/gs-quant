"""
Copyright 2020 Goldman Sachs.
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
from testfixtures import Replacer
from testfixtures.mock import Mock

import gs_quant.timeseries.measures_countries as mc
from gs_quant.api.gs.data import MarketDataResponseFrame
from gs_quant.data.core import DataContext


def test_fci():
    with pytest.raises(NotImplementedError):
        mc.fci('IN', real_time=True)

    data = {
        'fci': [
            101,
            102,
            103
        ],
        'realFCI': [
            100,
            99,
            98
        ],
        'realTWIContribution': [
            100,
            100,
            98
        ]
    }
    idx = pd.date_range('2020-01-01', freq='D', periods=3)
    df = MarketDataResponseFrame(data=data, index=idx)
    df.dataset_ids = ('FCI',)
    replace = Replacer()
    mock = replace('gs_quant.timeseries.measures.GsDataApi.get_market_data', Mock())
    mock.return_value = df

    with DataContext(datetime.date(2020, 1, 1), datetime.date(2019, 1, 3)):
        actual = mc.fci('IN')
        assert actual.index.equals(idx)
        assert all(actual.values == data['fci'])

    mock = replace('gs_quant.timeseries.measures.Dataset.get_data', Mock())
    mock.return_value = df
    with DataContext(datetime.date(2020, 1, 1), datetime.date(2019, 1, 3)):
        actual = mc.fci('IN', mc._FCI_MEASURE.REAL_FCI)
        assert actual.index.equals(idx)
        assert all(actual.values == data['realFCI'])
    with DataContext(datetime.date(2020, 1, 1), datetime.date(2019, 1, 3)):
        actual = mc.fci('IN', mc._FCI_MEASURE.REAL_TWI_CONTRIBUTION)
        assert actual.index.equals(idx)
        assert all(actual.values == data['realTWIContribution'])
    replace.restore()


if __name__ == '__main__':
    pytest.main(args=[__file__])
