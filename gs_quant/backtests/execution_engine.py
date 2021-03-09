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

from gs_quant.backtests.data_handler import DataHandler
from gs_quant.backtests.event import *
import datetime as dt


class ExecutionEngine(object):
    pass


class SimulatedExecutionEngine(ExecutionEngine):
    def __init__(self, data_handler: DataHandler):
        self.data_handler = data_handler
        self.orders = []

    def submit_order(self, order: OrderEvent):
        self.orders.append(order)
        self.orders.sort(key=lambda e: e.order.execution_end_time())

    def ping(self, state: dt.datetime):
        fill_events = []
        while self.orders:
            order: OrderBase = self.orders[0].order
            end_time = order.execution_end_time()
            if end_time > state:
                break
            else:
                fill = FillEvent(order=order,
                                 filled_price=order.execution_price(self.data_handler),
                                 filled_units=order.execution_quantity(self.data_handler))
                fill_events.append(fill)
                self.orders.pop(0)
        return fill_events
