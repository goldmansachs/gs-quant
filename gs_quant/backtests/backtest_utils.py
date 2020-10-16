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
from dateutil.relativedelta import relativedelta
from gs_quant.datetime.date import business_day_offset
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


def get_final_date(inst, create_date, duration):
    if duration is None:
        return dt.date.max
    if isinstance(duration, (dt.datetime, dt.date)):
        return duration
    if hasattr(inst, str(duration)):
        return getattr(inst, str(duration))
    if duration[-1].lower() in ['d', 'b']:
        return business_day_offset(create_date, int(duration[:-1]))
    if duration[-1].lower() == 'w':
        return create_date + relativedelta(weeks=int(duration[:-1]))
    if duration[-1].lower() == 'm':
        return create_date + relativedelta(months=int(duration[:-1]))
    if duration[-1].lower() == 'y':
        return create_date + relativedelta(years=int(duration[:-1]))
    raise RuntimeError(f'Unable to get final date for {duration}')


def scale_trade(inst, ratio):
    inst_dict = inst.as_dict()
    inst_dict['notional_amount'] = inst_dict['notional_amount'] * ratio
    new_inst = Instrument.from_dict(inst_dict)
    new_inst.name = inst.name
    return new_inst
