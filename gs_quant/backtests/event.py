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


from gs_quant.backtests.order import OrderBase


class Event(object):
    pass


class MarketEvent(Event):
    def __init__(self):
        self.type = 'Market'


class ValuationEvent(Event):
    def __init__(self):
        self.type = 'Valuation'


class OrderEvent(Event):
    def __init__(self,
                 order: OrderBase):
        self.type = 'Order'
        self.order = order


class FillEvent(Event):
    def __init__(self,
                 order: OrderBase,
                 filled_units: float,
                 filled_price: float):
        self.type = 'Fill'
        self.order = order
        self.filled_units = filled_units
        self.filled_price = filled_price
