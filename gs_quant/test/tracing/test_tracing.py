"""
Copyright 2025 Goldman Sachs.
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

import pytest
from plotly.graph_objs import Figure

from gs_quant.errors import MqError
from gs_quant.tracing import Tracer


def make_zero_duration(spans):
    """
    Helper function to set the duration of a span to zero
    """
    for span in spans:
        span.unwrap()._end_time = span.start_time


def test_tracer_tags():
    Tracer.reset()
    with Tracer('Some work') as scope:
        scope.span.set_tag('user', 'martin')

    spans = Tracer.get_spans()
    assert len(spans) == 1
    assert 'user' in spans[0].tags
    assert spans[0].tags['user'] == 'martin'


def test_tracer_events():
    Tracer.reset()
    with Tracer('Some work') as scope:
        scope.span.log_kv({"my_event": "yikes"})
        scope.span.add_event("Woo hoo!")
    spans = Tracer.get_spans()
    assert len(spans) == 1
    assert len(spans[0].events) == 2
    e1 = spans[0].events[0]
    e2 = spans[0].events[1]
    assert e1.name == "log"  # default name if "event" not specified
    assert "my_event" in e1.attributes
    assert abs(e1.timestamp_sec - dt.datetime.now().timestamp()) < 2  # to make sure we're used right scale factor
    assert e2.name == "Woo hoo!"
    assert e2.attributes == {}


def test_tracer_print():
    Tracer.reset()
    with Tracer('A'):
        with Tracer('B'):
            pass
        with Tracer('C'):
            with Tracer('D'):
                pass
            try:
                with Tracer('E'):
                    raise ValueError("test error handle")
            except Exception:
                pass
    with Tracer('F'):
        pass
    # Force elapsed time to 0 to make sure no spurious tiny times
    make_zero_duration(Tracer.get_spans())
    tracer_str, _ = Tracer.print(reset=True)
    expected = '\n'.join(['A                                                      0.0 ms',
                          '* B                                                    0.0 ms',
                          '* C                                                    0.0 ms',
                          '* * D                                                  0.0 ms',
                          '* * E                                                  0.0 ms [Error]',
                          'F                                                      0.0 ms'])
    assert tracer_str == expected


def test_tracer_plot():
    Tracer.reset()
    with Tracer("A") as scope:
        scope.span.set_tag("hello", "world")
        with Tracer("B"):
            Tracer.record_exception(ValueError("ah"))
    fig = Tracer.plot(True, False)
    assert isinstance(fig, Figure)


def test_gather_when_multi_traces():
    Tracer.reset()
    with Tracer("A") as first_scope:
        first_scope.span.set_tag("hello", "world")
        first_trace_id = first_scope.span.trace_id
        with Tracer("B1"):
            pass
        with Tracer("B2"):
            pass
    with Tracer("C") as second_scope:
        second_trace_id = second_scope.span.trace_id
        with Tracer("B1"):
            pass

    data1, total = Tracer.gather_data(False, trace_id=first_trace_id)
    data2, total = Tracer.gather_data(False, trace_id=second_trace_id)
    assert len(data1) == 3
    assert len(data2) == 2


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


def test_active_span():
    Tracer.reset()
    inactive = Tracer.active_span()
    # We get a noop/non-recording span
    assert inactive is not None
    assert inactive.span_id is not None
    assert inactive.trace_id is not None
    assert inactive.is_recording() is False
    inactive.set_tag("dummy", "tag")  # should be a no-op, but not throw
    inactive.add_event("Dummy event")  # should be a no-op, but not throw

    with Tracer.activate_span(inactive) as scope:
        # This shouldn't have done anything material, since it's a non-recording span
        assert scope.span is not None
        assert scope.span.span_id is not None
        assert scope.span.trace_id is not None
        assert scope.span.is_recording() is False

    with Tracer('Outer') as scope:
        scoped_span = scope.span
        active_span = Tracer.active_span()  # should be same as scoped_span, just another way to get it
        assert active_span.span_id == scoped_span.span_id
        assert active_span.trace_id == scoped_span.trace_id

    assert len(Tracer.get_spans()) == 1  # only "Outer" did anything


def test_span_activation():
    Tracer.reset()
    with Tracer('parent') as parent_scope:
        outer_span = parent_scope.span
        with Tracer('child-1') as child1_scope:
            with Tracer.activate_span(outer_span):
                with Tracer('child-2') as inner_scope:
                    # Since we re-activated the outer span, child-2's parent should be the outer "parent" span
                    assert inner_scope.span is not None
                    assert inner_scope.span.parent_id == outer_span.span_id
            # Now that we've exited the re-activated context, this span will be nested under child-1
            with Tracer('nested-child') as nested_child:
                assert nested_child.span.parent_id == child1_scope.span.span_id
            # This is a shortcut of with Tracer.activate_span(outer_span), Tracer('child-3')
            with Tracer('child-3', parent_span=outer_span) as another_inner_scope:
                assert another_inner_scope.span is not None
                assert another_inner_scope.span.parent_id == outer_span.span_id
            # Again we should be back in the "child-1" context
            with Tracer('another-nested-child') as nested_child:
                assert nested_child.span.parent_id == child1_scope.span.span_id

    # Force elapsed time to 0 to make sure no spurious tiny times
    make_zero_duration(Tracer.get_spans())
    tracer_str, _ = Tracer.print(reset=True)
    expected = '\n'.join(['parent                                                 0.0 ms',
                          '* child-2                                              0.0 ms',
                          '* child-3                                              0.0 ms',
                          '* child-1                                              0.0 ms',
                          '* * nested-child                                       0.0 ms',
                          '* * another-nested-child                               0.0 ms',
                          ])
    assert tracer_str == expected


def test_inject_extract():
    Tracer.reset()
    with Tracer('A') as scope:
        span_a = scope.span
        scope.span.set_tag('user', 'bob')
        fake_http_headers = {}
        Tracer.inject(fake_http_headers)
    spans = Tracer.get_spans()
    assert len(spans) == 1
    assert 'user' in spans[0].tags
    assert spans[0].tags['user'] == 'bob'
    assert len(fake_http_headers) > 0  # we're agnostic to the inject/extractor, so long as it's done something

    ctx = Tracer.extract(fake_http_headers)
    with Tracer.start_active_span('B', child_of=ctx) as scope:
        assert scope.span.parent_id == span_a.span_id

    with Tracer('C', parent_span=ctx) as scope:
        assert scope.span.parent_id == span_a.span_id


def test_ignore_active_span():
    with Tracer('A') as scope_a:
        with Tracer.start_active_span('B', ignore_active_span=True) as scope_b:
            assert scope_b.span.parent_id is None
        with Tracer.start_active_span('C') as scope_c:
            assert scope_c.span.parent_id == scope_a.span.span_id
