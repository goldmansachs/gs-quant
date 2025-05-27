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

import dataclasses
import pytest

from gs_quant.api.gs.backtests_xasset.response_datatypes.backtest_datatypes import Transaction, AdditionalResults, \
    DateConfig, Trade, Configuration, TransactionCostConfig, FixedCostModel, ScaledCostModel, \
    TransactionCostScalingType, AggregateCostModel, CostAggregationType


def test_request_types():
    cls = (Transaction, AdditionalResults, DateConfig, Trade, TransactionCostConfig, Configuration)
    for c in cls:
        assert dataclasses.is_dataclass(c)


def test_model_addition():
    f1 = FixedCostModel(1)
    f2 = FixedCostModel(2)
    s1 = ScaledCostModel(10, TransactionCostScalingType.Vega)
    s2 = ScaledCostModel(20, TransactionCostScalingType.Vega)
    s3 = ScaledCostModel(20, TransactionCostScalingType.Delta)
    assert f1 + f2 == FixedCostModel(3)
    assert s1 + s2 == ScaledCostModel(30, TransactionCostScalingType.Vega)
    assert f1 + s1 == AggregateCostModel((f1, s1), CostAggregationType.Sum)
    assert f2 + s2 == AggregateCostModel((f2, s2), CostAggregationType.Sum)
    assert (f1 + s1) + (f2 + s2) == AggregateCostModel((f1, s1, f2, s2), CostAggregationType.Sum)
    assert s1 + s3 == AggregateCostModel((s1, s3), CostAggregationType.Sum)
    assert AggregateCostModel((f1, s1), CostAggregationType.Min) + \
           AggregateCostModel((f2, s2), CostAggregationType.Min) == \
           AggregateCostModel((f1, s1, f2, s2), CostAggregationType.Min)
    with pytest.raises(TypeError):
        s1 + 1
    with pytest.raises(TypeError):
        s1 + 'a'
    with pytest.raises(TypeError):
        s1 + AggregateCostModel((f1,), CostAggregationType.Sum)
    with pytest.raises(TypeError):
        AggregateCostModel((f1, s1), CostAggregationType.Min) + AggregateCostModel((f2, s2), CostAggregationType.Max)
