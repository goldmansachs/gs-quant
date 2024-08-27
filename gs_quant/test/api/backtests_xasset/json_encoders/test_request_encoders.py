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

from gs_quant.api.gs.backtests_xasset.json_encoders.request_encoders import legs_decoder, legs_encoder
from gs_quant.target.common import AssetClass, AssetType
from gs_quant.target.instrument import FXOption, EqOption


def test_legs_decoder():
    fx_leg_1 = {"pair": "EURUSD", "assetClass": "FX", "type": "Option", "name": "leg_0"}
    fx_leg_2 = {"pair": "GBPUSD", "assetClass": "FX", "type": "Option"}
    eq_leg = {"underlier": ".SPX", "assetClass": "Equity", "type": "Option", "name": "test_eq"}
    [inst_1, inst_2, inst_3] = legs_decoder([fx_leg_1, fx_leg_2, eq_leg])
    assert isinstance(inst_1, FXOption)
    assert inst_1.name == "leg_0"
    assert inst_1.pair == "EURUSD"
    assert isinstance(inst_2, FXOption)
    assert inst_2.name == "leg_1"
    assert inst_2.pair == "GBPUSD"
    assert isinstance(inst_3, EqOption)
    assert inst_3.name == "test_eq"
    assert inst_3.underlier == ".SPX"


def test_legs_encoder():
    fx_leg_1 = FXOption(pair="EURUSD", name="leg_0")
    fx_leg_2 = FXOption(pair="GBPUSD")
    eq_leg = EqOption(underlier=".SPX", name="test_eq")
    [inst_1, inst_2, inst_3] = legs_encoder([fx_leg_1, fx_leg_2, eq_leg])
    assert isinstance(inst_1, dict)
    assert inst_1["assetClass"] == AssetClass.FX
    assert inst_1["type"] == AssetType.Option
    assert inst_1["pair"] == "EURUSD"
    assert isinstance(inst_2, dict)
    assert inst_2["assetClass"] == AssetClass.FX
    assert inst_2["type"] == AssetType.Option
    assert inst_2["pair"] == "GBPUSD"
    assert isinstance(inst_3, dict)
    assert inst_3["assetClass"] == AssetClass.Equity
    assert inst_3["type"] == AssetType.Option
    assert inst_3["underlier"] == ".SPX"
