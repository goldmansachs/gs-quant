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
import bisect
from typing import List

from gs_quant.backtests.data_handler import DataHandler
from gs_quant.backtests.event import OrderEvent, OrderBase, FillEvent

from abc import ABC

from gs_quant.backtests.data_handler import DataHandler
from gs_quant.backtests.event import OrderEvent, FillEvent
from gs_quant.backtests.order import OrderBase


class ExecutionEngine(ABC):
    """Abstract base class for execution engines."""
    pass


class SimulatedExecutionEngine(ExecutionEngine):
    """
    Simulates order execution based on market data.

    Attributes:
        data_handler (DataHandler): Provides market data for execution.
        orders (List[OrderEvent]): Sorted list of submitted orders by execution end time.
    """

    def __init__(self, data_handler: DataHandler):
        self.data_handler = data_handler
        self.orders: List[OrderEvent] = []

    def submit_order(self, order: OrderEvent):
        """
        Submit an order and maintain sorted execution order.

        Args:
            order (OrderEvent): The order to be submitted.
        """
        bisect.insort(self.orders, order, key=lambda e: e.order.execution_end_time())

    def ping(self, state: dt.datetime) -> List[FillEvent]:
        """
        Process and fill orders whose execution time has passed.

        Args:
            state (datetime): Current simulation time.

        Returns:
            List[FillEvent]: List of filled order events.
        """
        fill_events = []
        while self.orders:
            order_event = self.orders[0]
            order: OrderBase = order_event.order
            end_time = order.execution_end_time()

            if end_time > state:
                break

            try:
                fill = FillEvent(
                    order=order,
                    filled_price=order.execution_price(self.data_handler),
                    filled_units=order.execution_quantity()
                )
                fill_events.append(fill)
            except Exception as e:
                # Log or handle execution failure gracefully
                print(f"Error processing order {order}: {e}")
            finally:
                self.orders.pop(0)

        return fill_events
