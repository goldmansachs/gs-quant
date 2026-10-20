"""
Copyright 2026 Senanur Çetin.
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

# Default arguments that are evaluated when the function is *called*.
#
# A default such as ``as_of: dt.date = dt.date.today()`` is evaluated once, when the module is imported, so a
# notebook or service that stays up past midnight keeps using the date it started on. Use ``TODAY`` and ``NOW``
# instead and decorate the function with ``lazy_defaults``:
#
#     @lazy_defaults
#     def get_constituents(self, as_of: dt.date = TODAY): ...
#
# The value is worked out on each call that does not pass the argument. An argument that is passed, including an
# explicit ``None``, is left exactly as given. Signatures and documentation show ``TODAY`` rather than a date that
# would already be stale.

import datetime as dt
import functools
import inspect
from typing import Any, Callable, TypeVar

__all__ = ['LazyDefault', 'TODAY', 'NOW', 'lazy_defaults']

F = TypeVar('F', bound=Callable[..., Any])


class LazyDefault:
    """A default value that is worked out each time it is needed"""

    __slots__ = ('_factory', '_description')

    def __init__(self, factory: Callable[[], Any], description: str):
        self._factory = factory
        self._description = description

    def resolve(self) -> Any:
        return self._factory()

    def __add__(self, other: Any) -> 'LazyDefault':
        return LazyDefault(lambda: self.resolve() + other, f'{self!r} + {other!r}')

    def __sub__(self, other: Any) -> 'LazyDefault':
        return LazyDefault(lambda: self.resolve() - other, f'{self!r} - {other!r}')

    def __repr__(self) -> str:
        return self._description


# The clock is looked up on every call, not bound here, so tools that replace it (such as freezegun) are respected
TODAY = LazyDefault(lambda: dt.date.today(), 'TODAY')  #: the current date, as dt.date.today()
NOW = LazyDefault(lambda: dt.datetime.now(), 'NOW')  #: the current local date and time, as dt.datetime.now()


def lazy_defaults(func: F) -> F:
    """Resolve the ``LazyDefault`` defaults of ``func`` on every call that does not pass them.

    Apply it directly to the function, below decorators such as ``@classmethod`` or ``@staticmethod``."""
    signature = inspect.signature(func)
    lazy = {name: p.default for name, p in signature.parameters.items() if isinstance(p.default, LazyDefault)}
    if not lazy:
        raise TypeError(f'{func.__qualname__} has no LazyDefault parameters to resolve')

    def resolved(args: tuple, kwargs: dict) -> inspect.BoundArguments:
        bound = signature.bind(*args, **kwargs)
        bound.apply_defaults()
        for name, default in lazy.items():
            if bound.arguments[name] is default:
                bound.arguments[name] = default.resolve()
        return bound

    if inspect.iscoroutinefunction(func):

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            bound = resolved(args, kwargs)
            return await func(*bound.args, **bound.kwargs)

        return async_wrapper  # type: ignore[return-value]

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        bound = resolved(args, kwargs)
        return func(*bound.args, **bound.kwargs)

    return wrapper  # type: ignore[return-value]
