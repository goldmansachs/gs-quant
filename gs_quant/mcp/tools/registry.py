"""
Copyright 2026 Goldman Sachs.
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

from typing import Callable, Any
from fastmcp.tools import tool

# Static registry - module-level dict that holds all registered tools
_TOOL_REGISTRY: dict[str, Callable[..., Any]] = {}


def mcp_tool(*tool_args, **tool_kwargs):
    """
    Custom decorator that:
      1. Applies the FastMCP @tool decorator (forwarding all args/kwargs).
      2. Registers the function in a static registry for later discovery.

    Usage:
        @mcp_tool(tags={"user"})
        def current_user_info(...): ...
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        # Apply the original FastMCP tool decorator
        wrapped = tool(*tool_args, **tool_kwargs)(func)

        # Register in our static map (keyed by qualified name to avoid collisions)
        key = f"{func.__module__}.{func.__qualname__}"
        _TOOL_REGISTRY[key] = wrapped

        return wrapped

    return decorator


def register_mcp_tool(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Registers the decorated function in the static tool registry.

    Designed to be stacked on top of FastMCP's @tool decorator:

        @register_mcp_tool
        @tool(tags={"user"})
        def my_tool(...): ...

    The function is returned unchanged so other decorators / callers
    see exactly what @tool produced.
    """
    if not hasattr(func, "__fastmcp__"):
        raise ValueError(
            "register_mcp_tool should be used on functions already decorated with @tool. "
            "e.g. @register_mcp_tool\n@tool(...)\ndef my_func(...): ..."
        )
    key = f"{func.__module__}.{func.__qualname__}"
    _TOOL_REGISTRY[key] = func
    return func


def get_registered_tools() -> dict[str, Callable[..., Any]]:
    """Return a copy of the tool registry."""
    return dict(_TOOL_REGISTRY)


def discover_tools(package: str) -> dict[str, Callable[..., Any]]:
    """
    Import all submodules of a package so decorators run and populate
    the registry, then return the registry.
    """
    import importlib
    import pkgutil

    pkg = importlib.import_module(package)
    if hasattr(pkg, "__path__"):
        for _, name, _ in pkgutil.walk_packages(pkg.__path__, prefix=pkg.__name__ + "."):
            importlib.import_module(name)
    return get_registered_tools()
