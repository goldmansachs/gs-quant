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
from typing import Dict, Tuple

from gs_quant.instrument import Instrument


def decode_inst(i: dict) -> Instrument:
    return Instrument.from_dict(i)


def decode_inst_tuple(t: tuple) -> Tuple[Instrument, ...]:
    return tuple(decode_inst(i) for i in t)


def decode_daily_portfolio(results: dict, decode_instruments: bool = True) -> Dict[dt.date, Tuple[Instrument, ...]]:
    return {dt.date.fromisoformat(k): decode_inst_tuple(v) if decode_instruments else v for k, v in results.items()}
