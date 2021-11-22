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
from gs_quant.backtests.actions import AddTradeAction
from gs_quant.backtests.triggers import DateTriggerRequirements, DateTrigger, AggregateTriggerRequirements, \
    AggregateTrigger, AggType, NotTrigger, NotTriggerRequirements
from gs_quant.instrument import IRSwap, IRSwaption


def test_date_trigger():
    # Test DateTrigger
    action = AddTradeAction(IRSwap())
    trigger = DateTrigger(DateTriggerRequirements([dt.date(2021, 11, 9),
                                                   dt.date(2021, 11, 10),
                                                   dt.date(2021, 11, 11)]), [action])

    assert not trigger.has_triggered(dt.datetime(2021, 11, 10, 14, 0))
    assert trigger.has_triggered(dt.date(2021, 11, 10))

    trigger = DateTrigger(DateTriggerRequirements([dt.datetime(2021, 11, 9, 14, 0),
                                                   dt.datetime(2021, 11, 10, 14, 0),
                                                   dt.datetime(2021, 11, 11, 14, 0)]), [action])

    assert trigger.has_triggered(dt.datetime(2021, 11, 10, 14, 0))
    assert not trigger.has_triggered(dt.date(2021, 11, 10))

    trigger = DateTrigger(DateTriggerRequirements([dt.datetime(2021, 11, 9, 14, 0),
                                                   dt.datetime(2021, 11, 10, 14, 0),
                                                   dt.datetime(2021, 11, 11, 14, 0)], entire_day=True), [action])

    assert trigger.has_triggered(dt.datetime(2021, 11, 10, 14, 0))
    assert trigger.has_triggered(dt.date(2021, 11, 10))


def test_aggregate_triggger():
    # Test Aggregate Trigger
    action_1 = AddTradeAction(IRSwap())
    action_2 = AddTradeAction(IRSwaption())
    trigger_1 = DateTrigger(DateTriggerRequirements([dt.date(2021, 11, 9),
                                                     dt.date(2021, 11, 10),
                                                     dt.date(2021, 11, 11)]), [action_1])

    trigger_2 = DateTrigger(DateTriggerRequirements([dt.date(2021, 11, 8),
                                                     dt.date(2021, 11, 10),
                                                     dt.date(2021, 11, 12)]), [action_2])

    agg_trigger = AggregateTrigger(AggregateTriggerRequirements([trigger_1, trigger_2], aggregate_type=AggType.ALL_OF))

    assert not agg_trigger.has_triggered(dt.date(2021, 11, 9))
    assert agg_trigger.has_triggered(dt.date(2021, 11, 10))
    assert len(agg_trigger.actions) == 2

    agg_trigger = AggregateTrigger(AggregateTriggerRequirements([trigger_1, trigger_2], aggregate_type=AggType.ANY_OF))

    assert agg_trigger.has_triggered(dt.date(2021, 11, 8))
    assert isinstance(agg_trigger.actions[0].priceables[0], IRSwaption)
    assert agg_trigger.has_triggered(dt.date(2021, 11, 10))
    assert len(agg_trigger.actions) == 2


def test_not_triggger():
    # Test Not Trigger
    action = AddTradeAction(IRSwap())
    not_action = AddTradeAction(IRSwaption())
    trigger = DateTrigger(DateTriggerRequirements([dt.date(2021, 11, 9),
                                                   dt.date(2021, 11, 10),
                                                   dt.date(2021, 11, 11)]), [action])

    not_trigger = NotTrigger(NotTriggerRequirements(trigger), [not_action])

    assert not_trigger.has_triggered(dt.date(2021, 11, 8))
    assert isinstance(not_trigger.actions[0].priceables[0], IRSwaption)
    assert not not_trigger.has_triggered(dt.date(2021, 11, 10))
