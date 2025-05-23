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
from typing import Tuple, Optional, Mapping, Sequence, Union

import pandas as pd
from opentracing import Span, UnsupportedFormatException, SpanContextCorruptedException, Format, Scope, SpanContext
from opentracing import Tracer as OpenTracer
from opentracing.mocktracer import MockTracer
from opentracing.mocktracer.span import LogData
from opentracing.scope_managers.contextvars import ContextVarsScopeManager

from gs_quant.errors import *

_logger = logging.getLogger(__name__)


class Tags(Enum):
    HTTP_METHOD = 'http.method'
    HTTP_URL = 'http.url'
    HTTP_STATUS_CODE = 'http.status_code'
    CONTENT_LENGTH = 'content.length'


class TracingContext:
    def __init__(self, ctx: SpanContext):
        self._context = ctx


class TracingEvent:

    def __init__(self, ot_event: LogData):
        self._event = ot_event

    @property
    def name(self) -> str:
        return self._event.key_values.get("event", "log")

    @property
    def timestamp(self) -> int:
        """
        Timestamp in ns
        """
        return int(self._event.timestamp * 1e9)

    @property
    def timestamp_sec(self) -> float:
        """
        Timestamp in seconds
        """
        return self._event.timestamp

    @property
    def attributes(self) -> Mapping[str, any]:
        return self._event.key_values


class TracingScope:

    def __init__(self, scope: Scope, span: Optional[Span], finish_on_close: bool = True):
        self._scope = scope
        self._span = TracingSpan(span) if span else None
        self._finish_on_close = finish_on_close

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        if self._scope:
            self._scope.close()

    @property
    def span(self) -> 'TracingSpan':
        return self._span


class TracingSpan:
    def __init__(self, span: Span):
        self._span = span

    def unwrap(self):
        return self._span

    @property
    def context(self):
        return self

    def end(self):
        self._span.finish()

    def is_recording(self):
        return self._span.finish_time is None or self._span.finish_time <= 0

    @property
    def operation_name(self) -> str:
        return self._span.operation_name

    @property
    def trace_id(self) -> str:
        return self._span.context.trace_id

    def is_error(self) -> bool:
        return self._span.tags.get('error', False)

    @property
    def start_time(self) -> int:
        """
        Start time in ns
        """
        return int(self._span.start_time * 1e9)

    @property
    def end_time(self) -> Optional[int]:
        """
        End time in ns
        """
        return int(self._span.finish_time * 1e9) if self._span.finish_time else None

    @property
    def duration(self) -> float:
        """
        Duration of the span in milliseconds, or None if the span is not finished.
        """
        unwrapped = self._span
        return (unwrapped.finish_time - unwrapped.start_time) * 1e3 if unwrapped.finish_time else None

    @property
    def span_id(self) -> str:
        return self._span.context.span_id

    @property
    def parent_id(self) -> Optional[str]:
        return self._span.parent_id

    @property
    def tags(self) -> Mapping[str, any]:
        return self._span.tags

    @property
    def events(self) -> Sequence[TracingEvent]:
        return tuple(TracingEvent(event) for event in self._span.logs)

    def set_tag(self, key: Union[Enum, str], value: Union[bool, str, bytes, int, float, dt.date]) -> 'TracingSpan':
        if isinstance(value, dt.date):
            value = value.isoformat()
        if isinstance(key, Enum):
            key = key.value
        self._span.set_tag(key, value)
        return self

    def add_event(self, name: str, attributes: Optional[Mapping[str, any]] = None,
                  timestamp: Optional[float] = None) -> 'TracingSpan':
        attributes = {**attributes} if attributes else {}
        attributes["event"] = name
        self._span.log_kv(attributes or {}, timestamp)
        return self

    def log_kv(self, key_values: Mapping[str, any], timestamp=None) -> 'TracingSpan':
        self._span.log_kv(key_values, timestamp)
        return self


class TracerFactory:
    __tracer_instance = None

    def get(self) -> OpenTracer:
        if TracerFactory.__tracer_instance is None:
            TracerFactory.__tracer_instance = MockTracer(scope_manager=ContextVarsScopeManager())
        return TracerFactory.__tracer_instance


class Tracer(ContextDecorator):
    __factory = TracerFactory()

    @staticmethod
    def get_instance() -> OpenTracer:
        return Tracer.__factory.get()

    @staticmethod
    def inject(carrier):
        instance = Tracer.get_instance()
        span = instance.active_span
        if span is not None:
            try:
                instance.inject(span.context, Format.HTTP_HEADERS, carrier)
            except UnsupportedFormatException:
                pass

    @staticmethod
    def extract(carrier):
        instance = Tracer.get_instance()
        try:
            return instance.extract(Format.HTTP_HEADERS, carrier)
        except (UnsupportedFormatException, SpanContextCorruptedException):
            pass

    @staticmethod
    def set_factory(factory: TracerFactory):
        Tracer.__factory = factory

    def __init__(self, label: str = 'Execution', print_on_exit: bool = False, threshold: int = None,
                 wrap_exceptions=False, parent_span: Optional[TracingSpan] = None):
        self.__print_on_exit = print_on_exit
        self.__label = label
        self.__threshold = threshold
        self.wrap_exceptions = wrap_exceptions
        self._parent_span = parent_span

    def __enter__(self):
        if self._parent_span:
            self.__parent_scope = Tracer.activate_span(self._parent_span)
        scope = Tracer.get_instance().start_active_span(operation_name=self.__label)
        self.__scope = TracingScope(scope, scope.span)
        return self.__scope

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_value:
            Span._on_error(self.__scope.span, exc_type, exc_value, Tracer.__format_traceback(exc_type, exc_value))
        self.__scope.close()
        if self._parent_span:
            self.__parent_scope.close()
        if self.wrap_exceptions and exc_type is not None and not exc_type == MqWrappedError:
            raise MqWrappedError(f'Unable to calculate: {self.__label}') from exc_value

    @staticmethod
    def active_span():
        span = Tracer.get_instance().active_span
        if span:
            return TracingSpan(span)
        return None

    @staticmethod
    def activate_span(span: TracingSpan = None) -> Optional[TracingScope]:
        """
        Activates the current span
        :return: The current span
        """
        if span is None:
            return TracingScope(None, None)
        scope = Tracer.get_instance().scope_manager.activate(span.unwrap(), finish_on_close=False)
        return TracingScope(scope, span.unwrap(), False)

    @staticmethod
    def start_active_span(operation_name: str, child_of: Optional[TracingContext] = None,
                          ignore_active_span: bool = False) -> TracingScope:
        ctx = child_of._context if child_of else None
        scope = Tracer.get_instance().start_active_span(operation_name, child_of=ctx)
        return TracingScope(scope, scope.span)

    @staticmethod
    def record_exception(e, span: TracingSpan = None, exc_tb=None):
        span = span or Tracer.active_span()
        if span is not None:
            try:
                Span._on_error(span.unwrap(), type(e), e, Tracer.__format_traceback(e, type(e)))
            except Exception:
                pass

    @staticmethod
    def __format_traceback(exc_type, exc_value):
        if exc_value is None:
            return ''
        try:
            return ''.join(traceback.format_exception(exc_type, exc_value, None, limit=10))
        except Exception:
            return ''

    @staticmethod
    def reset():
        Tracer.get_instance().reset()

    @staticmethod
    def get_spans() -> Sequence[TracingSpan]:
        return tuple(TracingSpan(span) for span in Tracer.get_instance().finished_spans())

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
                elapsed = parent_span.duration or 0
                error = " [Error]" if parent_span.tags.get('error', False) else ""
                lines.append(f'{name:<50}{elapsed:>8.1f} ms{error}')
            else:
                lines.append((depth, parent_span))
            for child_span in reversed(spans_by_parent.get(parent_span.context.span_id, [])):
                _build_tree(child_span, depth + 1)

        total = 0
        lines = []
        # By default, we look for the span with no parent, but this might not always be what we want
        for span in reversed(spans_by_parent.get(root_id, [])):
            _build_tree(span, 0)
            total += span.duration

        if as_string:
            tracing_str = '\n'.join(lines)
            return tracing_str, total
        else:
            return lines, total

    @staticmethod
    def print(reset=True, root_id=None, trace_id=None):
        tracing_str, total = Tracer.gather_data(root_id=root_id, trace_id=trace_id)
        _logger.warning(f'Tracing Info:\n{tracing_str}\n{"-" * 61}\nTOTAL:{total:>52.1f} ms')
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
