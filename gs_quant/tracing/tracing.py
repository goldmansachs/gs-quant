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
import logging
import traceback
from contextlib import ContextDecorator

from opentracing import Span, UnsupportedFormatException
from opentracing import Tracer as OpenTracer
from opentracing.mocktracer import MockTracer

from gs_quant.errors import *

_logger = logging.getLogger(__name__)


class TracerFactory:
    __tracer_instance = None

    def get(self) -> OpenTracer:
        if TracerFactory.__tracer_instance is None:
            TracerFactory.__tracer_instance = MockTracer()
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
    def gather_data():
        spans = Tracer.get_spans()
        spans_by_parent = {}

        for span in reversed(spans):
            spans_by_parent.setdefault(span.parent_id, []).append(span)

        def _build_tree(parent_span, depth):
            name = f'{"* " * depth}{parent_span.operation_name}'
            elapsed = (parent_span.finish_time - parent_span.start_time) * 1000 if parent_span.finished else 'N/A'
            error = " [Error]" if parent_span.tags.get('error', False) else ""
            lines.append(f'{name:<50}{elapsed:>8.1f} ms{error}')
            for child_span in reversed(spans_by_parent.get(parent_span.context.span_id, [])):
                _build_tree(child_span, depth + 1)

        total = 0
        lines = []
        for span in reversed(spans_by_parent.get(None, [])):
            _build_tree(span, 0)
            total += (span.finish_time - span.start_time) * 1000

        tracing_str = '\n'.join(lines)
        return tracing_str, total

    @staticmethod
    def print(reset=True):
        tracing_str, total = Tracer.gather_data()
        _logger.warning(f'Tracing Info:\n{tracing_str}\n{"-" * 61}\nTOTAL:{total:>52.1f} ms')
        if reset:
            Tracer.reset()
        return tracing_str, total
