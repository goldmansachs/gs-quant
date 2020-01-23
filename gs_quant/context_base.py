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

import threading
from abc import ABCMeta

from gs_quant.errors import MqUninitialisedError

thread_local = threading.local()


def do_not_serialise(func):
    func.do_not_serialise = True
    return func


class ContextMeta(type, metaclass=ABCMeta):

    @classmethod
    def has_default(mcs) -> bool:
        return False

    @property
    @do_not_serialise
    def current(cls) -> 'ContextBase':
        """
        The current instance of this context
        """
        current = getattr(thread_local, '{}_current'.format(cls.__name__), None) or cls.default
        if current is None:
            raise MqUninitialisedError('{} is not initialised'.format(cls.__name__))

        return current

    @current.setter
    def current(cls, current: 'ContextBase'):
        setattr(thread_local, '{}_current'.format(cls.__name__), current)

    @property
    @do_not_serialise
    def current_is_set(cls) -> bool:
        return getattr(thread_local, '{}_current'.format(cls.__name__), None) is not None or cls.default_is_set

    @property
    @do_not_serialise
    def default(cls) -> 'ContextBase':
        attr_name = '{}_default'.format(cls.__name__)
        default = getattr(thread_local, attr_name, None)
        if (not cls.default_is_set) and cls.has_default():
            default = cls()
            setattr(thread_local, attr_name, default)

        return default

    @property
    @do_not_serialise
    def default_is_set(cls) -> bool:
        return getattr(thread_local, '{}_default'.format(cls.__name__), None) is not None

    @default.setter
    def default(cls, default: 'ContextBase'):
        setattr(thread_local, '{}_default'.format(cls.__name__), default)


class ContextBase(metaclass=ContextMeta):

    def __enter__(self):
        clz = self._cls

        try:
            current = clz.current
            setattr(thread_local, '{}_previous'.format(clz.__name__), current)
        except MqUninitialisedError:
            pass

        setattr(thread_local, '{}_entered'.format(clz.__name__), True)
        clz.current = self
        self._on_enter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self._on_exit(exc_type, exc_val, exc_tb)
        finally:
            clz = self._cls
            clz.current = getattr(thread_local, '{}_previous'.format(clz.__name__), None)
            setattr(thread_local, '{}_previous'.format(clz.__name__), None)
            setattr(thread_local, '{}_entered'.format(clz.__name__), False)

    @property
    @do_not_serialise
    def _cls(self) -> ContextMeta:
        seen = set()
        stack = [self.__class__]
        cls = None

        while stack:
            base = stack.pop()
            if ContextBase in base.__bases__ or ContextBaseWithDefault in base.__bases__:
                cls = base
                break

            if base not in seen:
                seen.add(base)
                stack.extend(b for b in base.__bases__ if issubclass(b, ContextBase))

        return cls or self.__class__

    @property
    @do_not_serialise
    def is_entered(self) -> bool:
        return getattr(thread_local, '{}_entered'.format(self._cls.__name__), False)

    def _on_enter(self):
        pass

    def _on_exit(self, exc_type, exc_val, exc_tb):
        pass


class ContextBaseWithDefault(ContextBase):

    @classmethod
    def has_default(cls) -> bool:
        return True


try:
    from contextlib import nullcontext
except ImportError:
    from contextlib import AbstractContextManager

    class nullcontext(AbstractContextManager):

        def __init__(self, enter_result=None):
            self.enter_result = enter_result

        def __enter__(self):
            return self.enter_result

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass
