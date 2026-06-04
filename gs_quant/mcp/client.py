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

from __future__ import annotations

import asyncio
import json
import os
import shlex
from pathlib import Path
from typing import Any, Callable

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.patch_stdout import patch_stdout

from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport
from rich import print
from rich.console import Console
from rich.json import JSON as RichJSON
from rich.table import Table

from gs_quant.session import Environment, GsSession

_console = Console()


# ---------------------------------------------------------------------------
# URL / headers / auth
# ---------------------------------------------------------------------------


def build_server_url(
    url: str | None,
    base_path: str,
    host: str,
    port: int,
    ssl: bool,
) -> str:
    """Build the streamable-http server URL.

    If ``url`` is provided it is returned verbatim. Otherwise an ``http(s)://host:port/base_path``
    URL is assembled, mirroring the layout used by :class:`McpServiceConfig` on the server side.
    """
    if url:
        return url
    scheme = "https" if ssl else "http"
    path = base_path if base_path.startswith("/") else f"/{base_path}"
    return f"{scheme}://{host}:{port}{path}"


_RELAY_HEADER_NAMES = {"AUTHORIZATION", "X-MARQUEE-CSRF-TOKEN", "X-APPLICATION", "X-VERSION"}
_RELAY_COOKIE_NAMES = ("MarqueeLogin", "MARQUEE-CSRF-TOKEN", "GSSSO")


def build_auth_headers(session: GsSession | None) -> dict[str, str]:
    """Extract auth-related headers + cookies from a :class:`GsSession`.

    Mirrors the relay logic in :meth:`GsSession._headers`. Cookies are merged into a single
    ``Cookie`` header so they travel cleanly through any HTTP transport.
    """
    if session is None or session._session is None:  # type: ignore[attr-defined]
        return {}

    headers: dict[str, str] = {}
    inner = session._session  # type: ignore[attr-defined]
    for k, v in inner.headers.items():
        if k.upper() in _RELAY_HEADER_NAMES:
            headers[k] = v

    cookie_pairs: list[str] = []
    if inner.cookies:
        for name in _RELAY_COOKIE_NAMES:
            if name in inner.cookies:
                cookie_pairs.append(f"{name}={inner.cookies[name]}")
    if cookie_pairs:
        headers["Cookie"] = "; ".join(cookie_pairs)
    return headers


def build_gs_session(
    environment: Environment | str | None,
    client_id: str | None,
    client_secret: str | None,
) -> GsSession | None:
    """Build and authenticate a local :class:`GsSession`."""
    session = GsSession.get(
        environment or Environment.PROD,
        client_id=client_id,
        client_secret=client_secret,
    )
    # Force authentication so cookies/headers are populated.
    session.init()
    return session


# ---------------------------------------------------------------------------
# Client construction
# ---------------------------------------------------------------------------


def make_client(
    url: str,
    headers: dict[str, str] | None = None,
    verify_ssl: bool = True,
) -> Client:
    """Create a :class:`fastmcp.Client` over a streamable-http transport."""
    _console.print(f"Connecting to MCP server at [cyan]{url}[/]...")
    transport = StreamableHttpTransport(
        url=url,
        headers=headers or None,
        verify=verify_ssl,
    )
    return Client(transport)


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------


def _maybe_json(value: str) -> Any:
    try:
        return json.loads(value)
    except (ValueError, TypeError):
        return value


def parse_tool_args(
    tokens: list[str] | str,
    param_names: list[str] | None = None,
) -> dict[str, Any]:
    """Parse CLI/REPL tool arguments.

    Resolution order:
      1. If joined tokens form a JSON object, use it directly.
      2. Else if every token contains ``=``, parse as ``key=value`` pairs (values JSON-decoded).
      3. Else if ``param_names`` is provided, treat tokens positionally and bind to those names.
      4. Else raise ``ValueError``.
    """
    if isinstance(tokens, str):
        tokens = shlex.split(tokens) if tokens.strip() else []
    if not tokens:
        return {}

    joined = " ".join(tokens).strip()
    if joined.startswith("{"):
        try:
            parsed = json.loads(joined)
            if isinstance(parsed, dict):
                return parsed
        except ValueError:
            pass

    if all("=" in tok for tok in tokens):
        args: dict[str, Any] = {}
        for tok in tokens:
            key, _, raw = tok.partition("=")
            args[key.strip()] = _maybe_json(raw)
        return args

    if param_names is not None:
        if len(tokens) > len(param_names):
            raise ValueError(
                f"Too many positional arguments: got {len(tokens)}, tool accepts at most {len(param_names)} "
                f"({', '.join(param_names) or '<none>'})."
            )
        return {name: _maybe_json(tok) for name, tok in zip(param_names, tokens)}

    raise ValueError("Arguments must be a JSON object, key=value pairs, or positional values for a known tool.")


def tool_param_names(tool: Any) -> list[str]:
    """Return the ordered parameter names from an MCP tool's input schema.

    Required parameters come first (preserving their JSON Schema declaration order), followed by
    optional ones. JSON Schema ``properties`` dicts preserve insertion order in Python.
    """
    schema = getattr(tool, "inputSchema", None) or {}
    props = schema.get("properties") or {}
    required = schema.get("required") or []
    required_set = set(required)
    ordered = [name for name in required if name in props]
    ordered += [name for name in props if name not in required_set]
    return ordered


# ---------------------------------------------------------------------------
# Result formatting
# ---------------------------------------------------------------------------


def _print_listing(title: str, items: list[Any], name_attr: str = "name") -> None:
    table = Table(title=title, show_lines=False)
    table.add_column("name", style="cyan", no_wrap=True)
    table.add_column("description", style="white")
    for item in items:
        name = getattr(item, name_attr, str(item))
        desc = getattr(item, "description", "") or ""
        table.add_row(str(name), desc)
    _console.print(table)


def _print_call_result(result: Any) -> None:
    # fastmcp Client.call_tool returns a CallToolResult-like object with `.content` and `.data`.
    data = getattr(result, "data", None)
    if data is not None:
        try:
            _console.print(RichJSON(json.dumps(data, default=str)))
            return
        except (TypeError, ValueError):
            pass
    content = getattr(result, "content", None)
    if content is None:
        _console.print(result)
        return
    for block in content:
        text = getattr(block, "text", None)
        if text is not None:
            try:
                _console.print(RichJSON(text))
            except ValueError:
                _console.print(text)
        else:
            _console.print(block)


# ---------------------------------------------------------------------------
# Async operations
# ---------------------------------------------------------------------------


async def do_list_tools(client: Client) -> list[Any]:
    tools = await client.list_tools()
    _print_listing("Tools", list(tools))
    return list(tools)


async def _find_tool(client: Client, name: str) -> Any | None:
    for tool in await client.list_tools():
        if tool.name == name:
            return tool
    return None


async def do_describe_tool(client: Client, name: str) -> Any | None:
    """Print a tool's signature (parameters, types, required-ness) and full input schema."""
    tool = await _find_tool(client, name)
    if tool is None:
        print(f"[red]tool not found:[/] {name}")
        return None

    schema = getattr(tool, "inputSchema", None) or {}
    props = schema.get("properties") or {}
    required = set(schema.get("required") or [])

    print(f"[bold cyan]{tool.name}[/] - {tool.description or ''}")
    if not props:
        print("  [dim]<no parameters>[/]")
    else:
        table = Table(show_header=True, header_style="bold")
        table.add_column("name", style="cyan", no_wrap=True)
        table.add_column("type")
        table.add_column("required")
        table.add_column("default")
        table.add_column("description")
        for pname in tool_param_names(tool):
            spec = props.get(pname, {})
            ptype = spec.get("type") or (
                "|".join(s.get("type", "?") for s in spec.get("anyOf", [])) if "anyOf" in spec else "?"
            )
            default = spec.get("default", "")
            table.add_row(
                pname,
                str(ptype),
                "yes" if pname in required else "no",
                "" if default == "" else json.dumps(default, default=str),
                spec.get("description", "") or "",
            )
        _console.print(table)
    return tool


async def do_list_resources(client: Client) -> list[Any]:
    resources = await client.list_resources()
    _print_listing("Resources", list(resources), name_attr="uri")
    return list(resources)


async def do_list_prompts(client: Client) -> list[Any]:
    prompts = await client.list_prompts()
    _print_listing("Prompts", list(prompts))
    return list(prompts)


async def do_call_tool(
    client: Client,
    name: str,
    args: dict[str, Any] | list[str],
) -> None:
    """Call a tool. ``args`` may be a pre-parsed dict or raw tokens to be parsed schema-aware."""
    if isinstance(args, list):
        param_names: list[str] | None = None
        tool = await _find_tool(client, name)
        if tool is not None:
            param_names = tool_param_names(tool)
        args = parse_tool_args(args, param_names=param_names)

    print(f"[bold]calling tool[/] [cyan]{name}[/] with args: {args}")
    result = await client.call_tool(name, args)
    _print_call_result(result)


async def do_read_resource(client: Client, uri: str) -> None:
    print(f"[bold]reading resource[/] [cyan]{uri}[/]")
    result = await client.read_resource(uri)
    _console.print(result)


async def do_get_prompt(client: Client, name: str, args: dict[str, Any]) -> None:
    print(f"[bold]getting prompt[/] [cyan]{name}[/] with args: {args}")
    result = await client.get_prompt(name, args)
    _console.print(result)


async def do_ping(client: Client) -> bool:
    """Ping the server and report round-trip status."""
    import time

    start = time.perf_counter()
    ok = bool(await client.ping())
    elapsed_ms = (time.perf_counter() - start) * 1000
    if ok:
        print(f"[green]pong[/] in {elapsed_ms:.1f} ms")
    else:
        print(f"[red]ping failed[/] after {elapsed_ms:.1f} ms")
    return ok


# ---------------------------------------------------------------------------
# Sync runners (for typer subcommands)
# ---------------------------------------------------------------------------


def run_async(client: Client, coro_factory) -> Any:
    async def runner():
        async with client:
            return await coro_factory(client)

    try:
        return asyncio.run(runner())
    except Exception as exc:  # noqa: BLE001 - surface clean error to CLI users
        import typer

        _console.print(f"[red]error:[/] {type(exc).__name__}: {exc}")
        raise typer.Exit(code=1) from None


# ---------------------------------------------------------------------------
# REPL
# ---------------------------------------------------------------------------


_HELP_TEXT = """
Available commands:
  /list                       List tools
  /list-resources             List resources
  /list-prompts               List prompts
  /describe <name>            Show a tool's parameters and types
  /call <name> [args...]      Call a tool. Args may be JSON, key=value, or positional.
  /read <uri>                 Read a resource by URI
  /prompt <name> [args...]    Get a prompt
  /ping                       Ping the server
  /refresh                    Refresh tool-name completion cache
  /reconnect                  Disconnect and reconnect to the server (e.g. after a restart)
  /help, /?                   Show this help
  /quit, /exit                Exit (Ctrl-D also works)
"""


async def run_repl(client_factory: Callable[[], Client]) -> None:
    """Interactive REPL backed by prompt_toolkit (history + tool name completion).

    ``client_factory`` is invoked once on entry and again on ``/reconnect`` to rebuild a fresh
    :class:`fastmcp.Client` (including refreshing any auth headers).
    """
    history_path = Path(os.path.expanduser("~/.gs_quant_mcp_history"))
    try:
        history_path.touch(exist_ok=True)
        history = FileHistory(str(history_path))
    except OSError:
        history = None

    slash_commands = [
        "/list",
        "/list-resources",
        "/list-prompts",
        "/describe",
        "/call",
        "/read",
        "/prompt",
        "/ping",
        "/refresh",
        "/reconnect",
        "/help",
        "/quit",
        "/exit",
    ]

    async def _safe_close(c: Client) -> None:
        try:
            await c.__aexit__(None, None, None)
        except Exception as exc:  # noqa: BLE001 - never let close errors bubble
            print(f"[yellow]warning during disconnect:[/] {exc}")

    client = client_factory()
    await client.__aenter__()
    try:
        # Prime the tool list for completion.
        try:
            tools = list(await client.list_tools())
        except Exception as exc:  # noqa: BLE001 - want to enter REPL even if listing fails
            print(f"[yellow]Warning: failed to list tools: {exc}[/]")
            tools = []

        tool_names = [t.name for t in tools]
        completer = WordCompleter(slash_commands + tool_names, ignore_case=True)
        session: PromptSession = PromptSession(history=history, completer=completer)

        print("[bold green]gs-quant MCP client[/] - type /help for commands, Ctrl-D to exit.")

        while True:
            try:
                with patch_stdout():
                    line = await session.prompt_async("mcp> ")
            except (EOFError, KeyboardInterrupt):
                print()
                return
            line = line.strip()
            if not line:
                continue

            try:
                tokens = shlex.split(line)
            except ValueError as exc:
                print(f"[red]parse error:[/] {exc}")
                continue

            cmd, *rest = tokens
            try:
                if cmd in ("/quit", "/exit"):
                    return
                if cmd in ("/help", "/?"):
                    print(_HELP_TEXT)
                elif cmd == "/list":
                    tools = await do_list_tools(client)
                    completer.words = slash_commands + [t.name for t in tools]
                elif cmd == "/list-resources":
                    await do_list_resources(client)
                elif cmd == "/list-prompts":
                    await do_list_prompts(client)
                elif cmd == "/describe":
                    if not rest:
                        print("[red]usage:[/] /describe <tool>")
                        continue
                    await do_describe_tool(client, rest[0])
                elif cmd == "/call":
                    if not rest:
                        print("[red]usage:[/] /call <tool> [args...]")
                        continue
                    name, *arg_tokens = rest
                    await do_call_tool(client, name, arg_tokens)
                elif cmd == "/read":
                    if not rest:
                        print("[red]usage:[/] /read <uri>")
                        continue
                    await do_read_resource(client, rest[0])
                elif cmd == "/prompt":
                    if not rest:
                        print("[red]usage:[/] /prompt <name> [args...]")
                        continue
                    name, *arg_tokens = rest
                    args = parse_tool_args(arg_tokens)
                    await do_get_prompt(client, name, args)
                elif cmd == "/refresh":
                    tools = list(await client.list_tools())
                    completer.words = slash_commands + [t.name for t in tools]
                    print(f"[green]refreshed[/] - {len(tools)} tools")
                elif cmd == "/ping":
                    await do_ping(client)
                elif cmd == "/reconnect":
                    print("[yellow]disconnecting...[/]")
                    await _safe_close(client)
                    client = client_factory()
                    try:
                        await client.__aenter__()
                        tools = list(await client.list_tools())
                        completer.words = slash_commands + [t.name for t in tools]
                        print(f"[green]reconnected[/] - {len(tools)} tools")
                    except Exception as exc:  # noqa: BLE001
                        print(f"[red]reconnect failed:[/] {type(exc).__name__}: {exc}")
                else:
                    print(f"[red]unknown command:[/] {cmd}. Type /help for commands.")
            except Exception as exc:  # noqa: BLE001 - REPL must not die on tool errors
                print(f"[red]error:[/] {exc}")
                if not client.is_connected():
                    print(
                        "[yellow]The connection to the server appears to be down. "
                        "Try [bold]/reconnect[/bold] to re-establish it.[/]"
                    )
    finally:
        await _safe_close(client)
