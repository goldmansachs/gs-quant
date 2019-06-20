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

from enum import Enum, IntEnum
from gs_quant.timeseries.helper import _create_int_enum, plot_function, plot_measure

# TODO test the instance of IntEnum when we have any.

WeekDay = _create_int_enum('WeekDay', {'SUNDAY': 1, 'Monday': 2, 'TUESDAY': 3,
                                       'WEDNESDAY': 4, 'THURSDAY': 5, 'Friday': 6, 'SATURDAY': 7})


def test_int_enum():
    assert ['a', 'b', 'c'][WeekDay.MONDAY] == 'c'

    assert len(list(WeekDay)) == 7
    assert len(WeekDay) == 7
    target = 'SUNDAY MONDAY TUESDAY WEDNESDAY THURSDAY FRIDAY SATURDAY'
    target = target.split()
    for i, weekday in enumerate(target, 1):
        e = WeekDay(i)
        assert isinstance(e, IntEnum)
        assert e.name == weekday
        assert e.value == i


@plot_function
def pf():
    pass


@plot_measure(asset_type=('abc',))
def pm():
    pass


def test_decorators():
    assert pf.plot_function
    assert pm.plot_measure
    assert pm.asset_class is None
    assert pm.asset_type == ('abc',)
