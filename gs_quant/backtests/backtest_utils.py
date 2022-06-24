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
from enum import Enum
from gs_quant.datetime.relative_date import RelativeDate
from gs_quant.instrument import Instrument


class CalcType(Enum):
    simple = 'simple'
    semi_path_dependent = 'semi_path_dependent'
    path_dependent = 'path_dependent'


def make_list(thing):
    if thing is None:
        return []
    if isinstance(thing, str):
        return [thing]
    else:
        try:
            iter(thing)
        except TypeError:
            return [thing]
        else:
            return list(thing)


final_date_cache = {}


def get_final_date(inst, create_date, duration, holiday_calendar=None):
    global final_date_cache
    cache_key = (inst, create_date, duration, holiday_calendar)
    if cache_key in final_date_cache:
        return final_date_cache[cache_key]

    if duration is None:
        final_date_cache[cache_key] = dt.date.max
        return dt.date.max
    if isinstance(duration, (dt.datetime, dt.date)):
        final_date_cache[cache_key] = duration
        return duration
    if hasattr(inst, str(duration)):
        final_date_cache[cache_key] = getattr(inst, str(duration))
        return getattr(inst, str(duration))

    final_date_cache[cache_key] = RelativeDate(duration, create_date).apply_rule(holiday_calendar=holiday_calendar)
    return final_date_cache[cache_key]


def scale_trade(inst: Instrument, ratio: float):
    new_inst = inst.scale(ratio)
    return new_inst
