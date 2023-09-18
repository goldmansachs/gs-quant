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
from typing import Tuple, Optional

import pandas as pd
from opentracing import Span, UnsupportedFormatException, SpanContextCorruptedException
from opentracing import Tracer as OpenTracer
from opentracing.mocktracer import MockTracer
from opentracing.scope_managers.contextvars import ContextVarsScopeManager

from gs_quant.errors import *

_logger = logging.getLogger(__name__)


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
    def inject(format, carrier):
        instance = Tracer.get_instance()
        span = instance.active_span
        if span is not None:
            try:
                instance.inject(span.context, format, carrier)
            except UnsupportedFormatException:
                pass

    @staticmethod
    def extract(format, carrier):
        instance = Tracer.get_instance()
        try:
            return instance.extract(format, carrier)
        except (UnsupportedFormatException, SpanContextCorruptedException):
            pass

    @staticmethod
    def set_factory(factory: TracerFactory):
        Tracer.__factory = factory

    def __init__(self, label: str = 'Execution', print_on_exit: bool = False, threshold: int = None,
                 wrap_exceptions=False):
        self.__print_on_exit = print_on_exit
        self.__label = label
        self.__threshold = threshold
        self.wrap_exceptions = wrap_exceptions

    def __enter__(self):
        self.__scope = Tracer.get_instance().start_active_span(operation_name=self.__label)
        return self.__scope

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_value:
            Span._on_error(self.__scope.span, exc_type, exc_value, Tracer.__format_traceback(exc_type, exc_value))
        self.__scope.close()
        if self.wrap_exceptions and exc_type is not None and not exc_type == MqWrappedError:
            raise MqWrappedError(f'Unable to calculate: {self.__label}') from exc_value

    @staticmethod
    def record_exception(e):
        span = Tracer.get_instance().active_span
        if span is not None:
            try:
                Span._on_error(span, type(e), e, Tracer.__format_traceback(e, type(e)))
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
    def get_spans():
        return Tracer.get_instance().finished_spans()

    @staticmethod
    def plot(reset=False):
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
            f'{s.operation_name} {int(1000 * (s.finish_time - s.start_time)):,.0f}ms',
            dt.datetime.fromtimestamp(s.start_time),
            dt.datetime.fromtimestamp(s.finish_time),
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
        fig.show()

    @staticmethod
    def gather_data(as_string: bool = True, root_id: Optional[str] = None):
        spans = Tracer.get_spans()
        spans_by_parent = {}

        for span in reversed(spans):
            spans_by_parent.setdefault(span.parent_id, []).append(span)

        def _build_tree(parent_span, depth):
            if as_string:
                name = f'{"* " * depth}{parent_span.operation_name}'
                elapsed = (parent_span.finish_time - parent_span.start_time) * 1000 if parent_span.finished else 'N/A'
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
            total += (span.finish_time - span.start_time) * 1000

        if as_string:
            tracing_str = '\n'.join(lines)
            return tracing_str, total
        else:
            return lines, total

    @staticmethod
    def print(reset=True, root_id=None):
        tracing_str, total = Tracer.gather_data(root_id=root_id)
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
