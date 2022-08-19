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

import pytest
from gs_quant.datetime import *


def test_time_difference_as_string():
    check_map = {
        '4 Seconds': np.timedelta64(4, 's'),
        '1 Minute 5 Seconds': np.timedelta64(65, 's'),
        '1 Year': np.timedelta64(int(SECS_IN_YEAR), 's'),
        '1 Day 1 Minute 5 Seconds': np.timedelta64(86465, 's')
    }

    for expected, input in check_map.items():
        actual = time_difference_as_string(input)
        assert expected == actual


def test_tracer_tags():
    Tracer.reset()
    with Tracer('Some work') as scope:
        scope.span.set_tag('user', 'martin')

    spans = Tracer.get_spans()
    assert len(spans) == 1
    assert 'user' in spans[0].tags
    assert spans[0].tags['user'] == 'martin'


def test_tracer_print():
    Tracer.reset()
    with Tracer('A'):
        with Tracer('B'):
            pass
        with Tracer('C'):
            with Tracer('D'):
                pass
    with Tracer('E'):
        pass
    # Force elapsed time to 0 to make sure no spurious tiny times
    for span in Tracer.get_spans():
        span.finish_time = span.start_time
    tracer_str, _ = Tracer.print(reset=True)
    expected = '\n'.join(['A                                                      0.0 ms',
                          '* B                                                    0.0 ms',
                          '* C                                                    0.0 ms',
                          '* * D                                                  0.0 ms',
                          'E                                                      0.0 ms'])
    assert tracer_str == expected


def test_tracer_wrapped_error():
    Tracer.reset()
    with pytest.raises(MqError, match='Unable to calculate: Outer Thing'):
        with Tracer('Outer Thing', wrap_exceptions=True):
            with Tracer('Inner Thing', ):
                raise KeyError('meaningless error')
    spans = Tracer.get_spans()
    assert 'error' in spans[0].tags
    assert 'error' in spans[1].tags
    Tracer.reset()

    with pytest.raises(MqError, match='Unable to calculate: Inner Thing'):
        with Tracer('Outer Thing', wrap_exceptions=True):
            with Tracer('Inner Thing', wrap_exceptions=True):
                raise KeyError('meaningless error')
    assert 'error' in spans[0].tags
    assert 'error' in spans[1].tags
    Tracer.reset()
