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

import gs_quant
import pytest
from gs_quant.config import DisplayOptions
from gs_quant.markets.portfolio import Portfolio
from gs_quant.risk import IRVega, AggregationLevel
from gs_quant.instrument import IRSwap
from gs_quant.test.utils.mock_calc import MockCalc


def test_display_options(mocker):
    with MockCalc(mocker):
        res = Portfolio(IRSwap(name='swap'), name='port').calc(IRVega(aggregation_level=AggregationLevel.Asset))

    assert gs_quant.config.display_options.show_na is False
    gs_quant.config.display_options.show_na = True
    assert gs_quant.config.display_options.show_na is True
    o = DisplayOptions(show_na=True)
    o2 = DisplayOptions(show_na=False)

    with pytest.raises(TypeError):
        _ = res.to_frame(display_options=True)
    df1 = res.to_frame(display_options=o)
    df2 = res.to_frame(display_options=o2)

    assert df1 is not None
    assert df2 is None
    # reset to make sure test works
    gs_quant.config.display_options = DisplayOptions()
