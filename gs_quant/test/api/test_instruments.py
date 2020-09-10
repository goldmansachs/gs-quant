"""
Copyright 2018 Goldman Sachs.
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

from gs_quant.instrument import Instrument, IRSwap
import datetime as dt


def test_from_dict():
    swap = IRSwap('Receive', '3m', 'USD', fixedRate=0, notionalAmount=1)
    properties = swap.as_dict()
    new_swap = Instrument.from_dict(properties)
    assert swap == new_swap

    # setting a datetime.date should work in a dictionary
    swap = IRSwap('Receive', dt.date(2030, 4, 11), 'USD', fixedRate='atm+5', notionalAmount=1)
    properties = swap.as_dict()
    new_swap = Instrument.from_dict(properties)
    assert swap == new_swap
