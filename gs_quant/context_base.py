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

from gs_quant.errors import MqUninitialisedError

thread_local = threading.local()


def do_not_serialise(func):
    func.do_not_serialise = True
    return func


class ContextMeta(type):

    @property
    @do_not_serialise
    def __path_key(cls) -> str:
        return '{}_path'.format(cls.__name__)

    @property
    @do_not_serialise
    def __default_key(cls) -> str:
        return '{}_default'.format(cls.__name__)

    @classmethod
    def default_value(mcs) -> object:
        return None

    @property
    @do_not_serialise
    def path(cls) -> tuple:
        return getattr(thread_local, cls.__path_key, ())

    @property
    @do_not_serialise
    def current(cls):
        """
        The current instance of this context
        """
        path = cls.path
        current = cls.__default if not path else next(iter(path))
        if current is None:
            raise MqUninitialisedError('{} is not initialised'.format(cls.__name__))

        return current

    @current.setter
    def current(cls, current):
        setattr(thread_local, cls.__path_key, (current,))

    @property
    @do_not_serialise
    def current_is_set(cls) -> bool:
        return bool(cls.path) or cls.__default is not None

    @property
    @do_not_serialise
    def __default(cls):
        default = getattr(thread_local, cls.__default_key, None)
        if default is None:
            default = cls.default_value()
            if default is not None:
                setattr(thread_local, cls.__default_key, default)

        return default

    def push(cls, context):
        setattr(thread_local, cls.__path_key, (context,) + cls.path)

    def pop(cls):
        path = cls.path
        setattr(thread_local, cls.__path_key, path[1:])
        return path[0]


class ContextBase(metaclass=ContextMeta):

    def __enter__(self):
        self._cls.push(self)
        setattr(thread_local, self.__entered_key, True)
        self._on_enter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self._on_exit(exc_type, exc_val, exc_tb)
        finally:
            self._cls.pop()
            setattr(thread_local, self.__entered_key, False)

    @property
    @do_not_serialise
    def __entered_key(self) -> str:
        return '{}_entered'.format(id(self))

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
        return getattr(thread_local, self.__entered_key, False)

    def _on_enter(self):
        pass

    def _on_exit(self, exc_type, exc_val, exc_tb):
        pass


class ContextBaseWithDefault(ContextBase):

    @classmethod
    def default_value(cls) -> object:
        return cls()


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
