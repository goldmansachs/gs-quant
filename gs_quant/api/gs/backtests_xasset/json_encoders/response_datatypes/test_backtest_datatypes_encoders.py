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

import json

from gs_quant.api.gs.backtests_xasset.response_datatypes.backtest_datatypes import TransactionCostConfig, \
    TradingCosts, FixedCostModel, ScaledCostModel, TransactionCostScalingType, AggregateCostModel, CostAggregationType


def test_transaction_cost_config_encoding():
    tc = TransactionCostConfig.from_dict({"tradeCostModel": {"entry": {"cost": 5.0, "type": "fixed_cost_model"}},
                                          "hedgeCostModel": None})
    assert tc == TransactionCostConfig(trade_cost_model=TradingCosts(entry=FixedCostModel(cost=5.0), exit=None),
                                       hedge_cost_model=None)

    tc = TransactionCostConfig.from_dict({"tradeCostModel": {"entry": {"scalingLevel": 5.0,
                                                                       "scalingQuantityType": "Vega",
                                                                       "type": "scaled_cost_model"},
                                                             "exit": {"models": [{"scalingLevel": 7.0,
                                                                                  "scalingQuantityType": "Notional",
                                                                                  "type": "scaled_cost_model"},
                                                                                 {"cost": 9.0,
                                                                                  "type": "fixed_cost_model"}],
                                                                      "aggregationType": "Sum",
                                                                      "type": "aggregate_cost_model"
                                                                      }
                                                             },
                                          "hedgeCostModel": {"entry": {"cost": 10, "type": "fixed_cost_model"}}
                                          })
    assert tc == TransactionCostConfig(TradingCosts(ScaledCostModel(5.0, TransactionCostScalingType.Vega),
                                                    AggregateCostModel(models=(
                                                        ScaledCostModel(7.0, TransactionCostScalingType.Notional),
                                                        FixedCostModel(9.0)
                                                    ),
                                                        aggregation_type=CostAggregationType.Sum)),
                                       TradingCosts(FixedCostModel(10)))
    assert tc == TransactionCostConfig.from_dict(json.loads(tc.to_json()))
