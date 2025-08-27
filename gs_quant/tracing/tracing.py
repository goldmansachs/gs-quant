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
import datetime as dt
import logging
import traceback
from contextlib import ContextDecorator
from enum import Enum
from typing import Tuple, Optional, Sequence, Mapping, Union

import pandas as pd
from opentelemetry import trace, context
from opentelemetry.context import Context
from opentelemetry.propagate import extract, inject, set_global_textmap
from opentelemetry.propagators.textmap import TextMapPropagator
from opentelemetry.sdk.trace import TracerProvider, SynchronousMultiSpanProcessor, ReadableSpan, Span, Event
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, SpanExporter
from opentelemetry.trace import Tracer as OtelTracer, SpanContext, INVALID_SPAN
from opentelemetry.trace import format_trace_id, format_span_id

from gs_quant.errors import MqWrappedError

_logger = logging.getLogger(__name__)


class Tags(Enum):
    HTTP_METHOD = 'http.method'
    HTTP_URL = 'http.url'
    HTTP_STATUS_CODE = 'http.status_code'
    CONTENT_LENGTH = 'content.length'


class SpanConsumer(SpanExporter):
    _instance = None

    @staticmethod
    def get_instance():
        if SpanConsumer._instance is None:
            SpanConsumer._instance = SpanConsumer()
        return SpanConsumer._instance

    @staticmethod
    def get_spans() -> Sequence['TracingSpan']:
        return SpanConsumer.get_instance()._collected_spans

    @staticmethod
    def reset():
        SpanConsumer.get_instance()._collected_spans = []

    @staticmethod
    def manually_record(spans: Sequence['TracingSpan']):
        SpanConsumer.get_instance()._collected_spans.extend(spans)

    def __init__(self):
        self._collected_spans = []

    def export(self, spans: Sequence[ReadableSpan]) -> None:
        self._collected_spans.extend(TracingSpan(span) for span in spans)


class TracingContext:
    def __init__(self, ctx: SpanContext):
        self._context = ctx


class TracingEvent:

    def __init__(self, ot_event: Event):
        self._event = ot_event

    @property
    def name(self) -> str:
        return self._event.name

    @property
    def timestamp(self) -> int:
        """
        Timestamp in ns
        """
        return self._event.timestamp

    @property
    def timestamp_sec(self) -> float:
        """
        Timestamp in seconds
        """
        return self._event.timestamp / 1e9

    @property
    def attributes(self) -> Mapping[str, any]:
        return self._event.attributes


class TracingScope:

    def __init__(self, token, span: Optional[Span], finish_on_close: bool = True):
        self._token = token
        self._span = TracingSpan(span) if span else NonRecordingTracingSpan(INVALID_SPAN)
        self._finish_on_close = finish_on_close

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            Tracer.record_exception(exc_val, self._span, exc_tb)
        self.close()

    def close(self):
        if self._token:
            context.detach(self._token)
            if self._finish_on_close:
                return self._span.end()

    @property
    def span(self) -> 'TracingSpan':
        return self._span


class TracingSpan:
    def __init__(self, span: Span, endpoint: Optional[str] = None):
        self._span = span
        self._endpoint = endpoint

    def unwrap(self):
        return self._span

    @property
    def context(self):
        return self

    def end(self):
        self._span.end()

    def is_recording(self):
        return self._span.is_recording()

    @property
    def operation_name(self) -> str:
        return self._span.name

    def transportable(self, endpoint_override: Optional[str] = None) -> 'TransportableSpan':
        return TransportableSpan(self, endpoint_override or self._endpoint)

    @property
    def endpoint(self) -> str:
        return self._endpoint

    @endpoint.setter
    def endpoint(self, endpoint):
        self._endpoint = endpoint

    @property
    def trace_id(self) -> str:
        return format_trace_id(self._span.get_span_context().trace_id)

    def is_error(self) -> bool:
        return self._span.attributes.get('error', False)

    @property
    def start_time(self) -> int:
        """
        Start time in ns
        """
        return self._span.start_time

    @property
    def end_time(self) -> Optional[int]:
        """
        End time in ns
        """
        return self._span.end_time

    @property
    def duration(self) -> float:
        """
        Duration of the span in milliseconds, or None if the span is not finished.
        """
        unwrapped = self._span
        return (unwrapped.end_time - unwrapped.start_time) / 1e6 if unwrapped.end_time else None

    @property
    def span_id(self) -> str:
        return format_span_id(self._span.get_span_context().span_id)

    @property
    def parent_id(self) -> Optional[str]:
        parent = self._span.parent
        return format_span_id(parent.span_id) if parent else None

    @property
    def tags(self) -> Mapping[str, any]:
        return self._span.attributes

    @property
    def events(self) -> Sequence[TracingEvent]:
        return tuple(TracingEvent(event) for event in self._span.events)

    def set_tag(self, key: Union[Enum, str], value: Union[bool, str, bytes, int, float, dt.date]) -> 'TracingSpan':
        if value is None:
            return self
        if isinstance(value, dt.date):
            value = value.isoformat()
        elif isinstance(value, Enum):
            value = value.value
        if isinstance(key, Enum):
            key = key.value
        self._span.set_attribute(key, value)
        return self

    def add_event(self, name: str, attributes: Optional[Mapping[str, any]] = None,
                  timestamp: Optional[float] = None) -> 'TracingSpan':
        converted_timestamp = int(timestamp * 1e9) if timestamp else None
        self._span.add_event(name, attributes, converted_timestamp)
        return self

    def log_kv(self, key_values: Mapping[str, any], timestamp=None) -> 'TracingSpan':
        converted_timestamp = int(timestamp * 1e9) if timestamp else None
        event_name = "log" if key_values is None or "event" not in key_values else key_values["event"]
        self._span.add_event(event_name, key_values, converted_timestamp)
        return self


class NonRecordingTracingSpan(TracingSpan):
    def __init__(self, span: Span):
        super().__init__(span)
        self._span = span

    def end(self):
        pass

    @property
    def operation_name(self) -> str:
        return "Non-Recording Span"

    @property
    def parent_id(self) -> Optional[str]:
        return None

    @property
    def tags(self) -> Mapping[str, any]:
        return dict()

    @property
    def start_time(self) -> int:
        return 0

    @property
    def end_time(self) -> Optional[int]:
        return None

    @property
    def duration(self) -> float:
        return 0


NOOP_TRACING_SCOPE = TracingScope(None, None)


class TransportableSpan(TracingSpan):
    """
    A transportable span is a representation of a finished TracingSpan that can be pickled.
    """

    def __init__(self, span: TracingSpan, endpoint: Optional[str] = None):
        super().__init__(None, endpoint or span.endpoint)
        self._operation_name = span.operation_name
        self._trace_id = span.trace_id
        self._span_id = span.span_id
        self._parent_id = span.parent_id
        self._tags = dict(span.tags)
        self._start_time = span.start_time
        self._end_time = span.end_time
        self._events = tuple(TransportableTracingEvent(event) for event in span.events)

    def transportable(self, endpoint_override: Optional[str] = None) -> 'TransportableSpan':
        if not endpoint_override or endpoint_override == self._endpoint:
            return self
        else:
            return TransportableSpan(self, endpoint_override or self._endpoint)

    def end(self):
        pass

    def is_recording(self):
        return self._end_time is None

    @property
    def operation_name(self) -> str:
        return self._operation_name

    @property
    def trace_id(self) -> str:
        return self._trace_id

    def is_error(self) -> bool:
        return self._tags.get('error', False)

    @property
    def start_time(self) -> int:
        """
        Start time in ns
        """
        return self._start_time

    @property
    def end_time(self) -> Optional[int]:
        """
        End time in ns
        """
        return self._end_time

    @property
    def duration(self) -> float:
        """
        Duration of the span in milliseconds, or None if the span is not finished.
        """
        return (self._end_time - self._start_time) / 1e6 if self._end_time else None

    @property
    def span_id(self) -> str:
        return self._span_id

    @property
    def parent_id(self) -> Optional[str]:
        return self._parent_id

    @property
    def tags(self) -> Mapping[str, any]:
        return self._tags

    @property
    def events(self) -> Sequence[TracingEvent]:
        return self._events

    def set_tag(self, key: Union[Enum, str], value: Union[bool, str, bytes, int, float, dt.date]) -> 'TracingSpan':
        return self

    def add_event(self, name: str, attributes: Optional[Mapping[str, any]] = None,
                  timestamp: Optional[float] = None) -> 'TracingSpan':
        return self

    def log_kv(self, key_values: Mapping[str, any], timestamp=None) -> 'TracingSpan':
        return self


class TransportableTracingEvent(TracingEvent):

    def __init__(self, event: TracingEvent):
        super().__init__(None)
        self._name = event.name
        self._timestamp = event.timestamp
        self._attributes = dict(event.attributes)

    @property
    def name(self) -> str:
        return self._name

    @property
    def timestamp(self) -> int:
        """
        Timestamp in ns
        """
        return self._timestamp

    @property
    def timestamp_sec(self) -> float:
        """
        Timestamp in seconds
        """
        return self._timestamp / 1e9

    @property
    def attributes(self) -> Mapping[str, any]:
        return self._attributes


class TracerFactory:
    __tracer_instance = None

    def get(self) -> OtelTracer:
        if TracerFactory.__tracer_instance is None:
            # Define which OpenTelemetry Tracer provider implementation to use.
            span_processor = SynchronousMultiSpanProcessor()
            span_processor.add_span_processor(SimpleSpanProcessor(SpanConsumer.get_instance()))
            trace.set_tracer_provider(TracerProvider(active_span_processor=span_processor))

            # Create an OpenTelemetry Tracer.
            otel_tracer = trace.get_tracer(__name__)
            TracerFactory.__tracer_instance = otel_tracer
        return TracerFactory.__tracer_instance


class Tracer(ContextDecorator):
    __factory = TracerFactory()

    def __init__(self, label: str = 'Execution', print_on_exit: bool = False, threshold: int = None,
                 wrap_exceptions=False, parent_span: Optional[Union[TracingSpan, TracingContext]] = None):
        self.__print_on_exit = print_on_exit
        self.__label = label
        self.__threshold = threshold
        self.wrap_exceptions = wrap_exceptions
        self._parent_span = parent_span if isinstance(parent_span, TracingSpan) else None
        self._parent_ctx = parent_span if isinstance(parent_span, TracingContext) else None

    def __enter__(self):
        if self._parent_span:
            self.__parent_scope = Tracer.activate_span(self._parent_span)
        self.__scope = Tracer.start_active_span(self.__label, child_of=self._parent_ctx)
        return self.__scope

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_value:
            self.record_exception(exc_value, self.__scope.span, exc_tb)
        self.__scope.close()
        if self._parent_span:
            self.__parent_scope.close()
        if self.wrap_exceptions and exc_type is not None and not exc_type == MqWrappedError:
            raise MqWrappedError(f'Unable to calculate: {self.__label}') from exc_value

    @staticmethod
    def get_instance() -> OtelTracer:
        return Tracer.__factory.get()

    @staticmethod
    def set_factory(factory: TracerFactory):
        Tracer.__factory = factory

    @staticmethod
    def active_span():
        current_span = trace.get_current_span()
        if current_span is None or not current_span.is_recording():
            return NonRecordingTracingSpan(INVALID_SPAN)
        else:
            return TracingSpan(current_span)

    @staticmethod
    def set_propagator_format(propagator_format: TextMapPropagator):
        set_global_textmap(propagator_format)

    @staticmethod
    def inject(carrier):
        span = trace.get_current_span()
        if span is not None and span.is_recording():
            try:
                inject(carrier)
            except Exception:
                _logger.error("Error injecting trace context", exc_info=True)

    @staticmethod
    def extract(carrier):
        try:
            return TracingContext(extract(carrier))
        except Exception:
            _logger.error("Error extracting trace context", exc_info=True)

    @staticmethod
    def activate_span(span: TracingSpan = None, finish_on_close: bool = False) -> Optional[TracingScope]:
        """
        Activates the current span
        :return: The current span
        """
        if span is None or not span.is_recording():
            return NOOP_TRACING_SCOPE
        ctx = trace.set_span_in_context(span.unwrap())
        token = context.attach(ctx)
        return TracingScope(token, span.unwrap(), finish_on_close=finish_on_close)

    @staticmethod
    def start_active_span(operation_name: str, child_of: Optional[TracingContext] = None,
                          ignore_active_span: bool = False, finish_on_close: bool = True) -> TracingScope:
        ctx = Context() if ignore_active_span else child_of._context if child_of else None
        span = Tracer.get_instance().start_span(operation_name, context=ctx)
        # Set as the implicit current context
        # Creates a Context object with parent set as current span
        ctx = trace.set_span_in_context(span)
        token = context.attach(ctx)
        return TracingScope(token, span, finish_on_close)

    @staticmethod
    def record_exception(e, span: TracingSpan = None, exc_tb=None):
        span = span or TracingSpan(trace.get_current_span())
        if span is not None:
            try:
                span.set_tag('error', True)
                span.log_kv({
                    'event': 'error',
                    'message': str(e),
                    'error.object': str(e),
                    'error.kind': type(e).__name__,
                    'stack': Tracer.__format_traceback(type(e), e, exc_tb),
                })
            except Exception:
                pass

    @staticmethod
    def __format_traceback(exc_type, exc_value, exc_tb=None):
        if exc_value is None:
            return ''
        try:
            return ''.join(traceback.format_exception(exc_type, exc_value, exc_tb, limit=10))
        except Exception:
            return ''

    @staticmethod
    def reset():
        SpanConsumer.reset()

    @staticmethod
    def get_spans() -> Sequence[TracingSpan]:
        return SpanConsumer.get_spans()

    @staticmethod
    def plot(reset=False, show=True):
        try:
            import plotly.express as px
        except ImportError:
            _logger.warning('Package "plotly" required to visualise the trace, printing instead')
            Tracer.print(reset)
            return
        color_list = ('#2b76f7', '#5a8efb', '#79aaff', '#89bbff', '#cdddff')
        error_color = 'rgb(244, 127, 114)'
        ordered_spans, _ = Tracer.gather_data(False)
        span_df = pd.DataFrame.from_records([(
            f'#{i}',
            f'{s.operation_name} {int(s.duration):,.0f}ms',
            dt.datetime.fromtimestamp(s.start_time / 1e9),
            dt.datetime.fromtimestamp(s.end_time / 1e9),
            '\n '.join([f'{k}={v}' for k, v in s.tags.items()]) if s.tags else '',
        ) for i, (depth, s) in enumerate(ordered_spans)], columns=['id', 'operation', 'start', 'end', 'tags'])
        color_map = {f'#{i}': error_color if 'error' in s.tags else color_list[depth % len(color_list)] for
                     i, (depth, s) in enumerate(ordered_spans)}
        fig = px.timeline(
            data_frame=span_df,
            width=1000,
            height=40 + 30 * len(span_df),
            x_start="start",
            x_end="end",
            y="id",
            hover_data='tags',
            text='operation',
            color='id',
            color_discrete_map=color_map
        )
        fig.update_layout(
            showlegend=False,
            yaxis_visible=False,
            yaxis_showticklabels=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin={'l': 0, 't': 0, 'b': 0, 'r': 0}
        )
        if reset:
            Tracer.reset()
        if show:
            fig.show()
        else:
            return fig

    @staticmethod
    def gather_data(as_string: bool = True, root_id: Optional[str] = None, trace_id: Optional[str] = None):
        spans = Tracer.get_spans()
        spans_by_parent = {}

        for span in reversed(spans):
            if trace_id and span.trace_id != trace_id:
                continue
            spans_by_parent.setdefault(span.parent_id, []).append(span)

        def _build_tree(parent_span, depth):
            if as_string:
                name = f'{"* " * depth}{parent_span.operation_name}'
                elapsed = (parent_span.end_time - parent_span.start_time) / 1000000
                error = " [Error]" if parent_span.is_error() else ""
                lines.append(f'{name:<50}{elapsed:>8.1f} ms{error}')
            else:
                lines.append((depth, parent_span))
            for child_span in reversed(spans_by_parent.get(parent_span.span_id, [])):
                _build_tree(child_span, depth + 1)

        total = 0
        lines = []
        # By default, we look for the span with no parent, but this might not always be what we want
        for span in reversed(spans_by_parent.get(root_id, [])):
            _build_tree(span, 0)
            total += (span.end_time - span.start_time) / 1000000

        if as_string:
            tracing_str = '\n'.join(lines)
            return tracing_str, total
        else:
            return lines, total

    @staticmethod
    def print(reset=True, root_id=None, trace_id=None):
        tracing_str, total = Tracer.gather_data(root_id=root_id, trace_id=trace_id)
        str_id = trace_id or root_id or ""
        _logger.warning(f'Tracing Info: {str_id}\n{tracing_str}\n{"-" * 61}\nTOTAL:{total:>52.1f} ms')
        if reset:
            Tracer.reset()
        return tracing_str, total


def parse_tracing_line_args(line: str) -> Tuple[Optional[str], bool]:
    stripped = tuple(s for s in line.split(' ') if s != '')
    if len(stripped) > 0 and stripped[0] in ('chart', 'plot', 'graph'):
        return tuple(stripped[1:]) if len(stripped[1:]) else None, True
    return stripped if len(stripped) else None, False


try:
    # Attempt to import/register some jupyter magic
    import gs_quant_internal.tracing.jupyter  # noqa
except ImportError:
    try:
        from IPython.core.magic import register_cell_magic
        from IPython import get_ipython

        @register_cell_magic("trace")
        def trace_ipython_cell(line, cell):
            """Wraps the execution of a cell in a tracer call and prints"""
            span_name, show_chart = parse_tracing_line_args(line)
            if cell is None:
                return line
            with Tracer(label=span_name):
                res = get_ipython().run_cell(cell)
                if res.error_in_exec:
                    Tracer.record_exception(res.error_in_exec)
            if show_chart:
                Tracer.plot(True)
            else:
                Tracer.print(True)
            return None
    except Exception:
        pass
