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

from gs_quant.instrument import EqOption, FXMultiCrossBinary, FXMultiCrossBinaryLeg, Instrument
from gs_quant.test.utils.mock_calc import MockCalc


def test_instrument_resolve(mocker):
    with MockCalc(mocker):
        eq_option = EqOption('.FTSE', strike_price='ATMS', name='FTSE_Call')
        assert eq_option.unresolved is None

        eq_option.resolve()
        assert eq_option.unresolved is not None
        assert eq_option.strike_price == 7464.8

        eq_option.expiration_date = '3m'
        assert eq_option.unresolved is not None
        assert eq_option.strike_price == 7464.8


def test_nested_leg_from_dict():
    mcb = FXMultiCrossBinary(legs=(FXMultiCrossBinaryLeg(pair='USDJPY'), FXMultiCrossBinaryLeg(pair='GBPUSD')))
    mcb_dict = mcb.to_dict()
    new_mcb = Instrument.from_dict(mcb_dict)
    assert new_mcb == mcb
