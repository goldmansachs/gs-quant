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

import asyncio
import os
from typing import Annotated, Literal, Callable, Any

import typer
from dotenv import load_dotenv, find_dotenv
from fastmcp import FastMCP
from fastmcp.server.middleware.logging import LoggingMiddleware
from rich import print
from rich.console import Console
from rich.table import Table

from gs_quant.config.utils import load_model_from_yaml
from gs_quant.mcp.client import (
    build_auth_headers,
    build_gs_session,
    build_server_url,
    do_call_tool,
    do_describe_tool,
    do_get_prompt,
    do_list_prompts,
    do_list_resources,
    do_list_tools,
    do_ping,
    do_read_resource,
    make_client,
    parse_tool_args,
    run_async,
    run_repl,
)
from gs_quant.mcp import McpServiceConfig, run_mcp_server
from gs_quant.mcp.middleware import RemoteUserAuthMiddleware, LocalUserAuthMiddleware
from gs_quant.mcp.tools import discover_tools as registry_discover_tools, get_registered_tools

app = typer.Typer()
client_app = typer.Typer(help="MCP client commands (streamable HTTP).")
app.add_typer(client_app, name="client", invoke_without_command=True)

pkg_option = typer.Option("-p", "--packages", help="The package(s) to discover tools from (comma seperated)")
extra_pkg_option = typer.Option(help="Extra package(s) to discover tools from (comma seperated)")
DEFAULT_TOOLS_PACKAGES = "gs_quant.mcp.tools"


def get_tools(packages: str, extra_packages: str) -> dict[str, Callable[..., Any]]:
    for package in packages.split(",") + extra_packages.split(","):
        package = package.strip()
        if package:
            print(f"Discovering tools in package: :package: [cyan]{package}[/]")
            registry_discover_tools(package)
    return get_registered_tools()


@app.command()
def discover_tools(
    packages: Annotated[str, pkg_option] = DEFAULT_TOOLS_PACKAGES,
    extra_packages: Annotated[str, extra_pkg_option] = "",
):
    """
    List all registered MCP tools
    """
    tools = get_tools(packages, extra_packages)
    table = Table(title="Registered MCP Tools", show_lines=True)
    table.add_column("name", style="bold red", no_wrap=True)
    table.add_column("pkg", style="cyan", no_wrap=True)
    table.add_column("tags", style="magenta")
    table.add_column("doc", style="white")
    for key, tool in tools.items():
        fastmcp_config = tool.__fastmcp__ if hasattr(tool, "__fastmcp__") else None
        tags = fastmcp_config.tags if fastmcp_config and hasattr(fastmcp_config, 'tags') else set()
        doc = (tool.__doc__ or "").strip()
        table.add_row(tool.__name__, key, ", ".join(sorted(tags)), doc)
    Console().print(table)


@app.command()
def server(
    config: Annotated[str, typer.Option("-c", "--config", help="Path to the configuration file (YAML)")] = None,
    base_path: Annotated[str, typer.Option(help="Base path for the MCP server")] = "/mcp",
    host: Annotated[str, typer.Option(help="server ip address to bind to")] = "0.0.0.0",
    port: Annotated[int, typer.Option(help="Port to run the MCP server on")] = 4301,
    environment: Annotated[str, typer.Option(help="Target environment (e.g., Dev, Prod)")] = None,
    service_name: Annotated[str, typer.Option(help="The name of the service")] = "GsQuantMCP",
    packages: Annotated[str, pkg_option] = DEFAULT_TOOLS_PACKAGES,
    extra_packages: Annotated[str, extra_pkg_option] = "",
    enable_tags: Annotated[str, typer.Option(help="Comma-separated list of tags to select tools")] = None,
    disable_tags: Annotated[str, typer.Option(help="Comma-separated list of tags to de-select tools")] = None,
    enable_keys: Annotated[str, typer.Option(help="Comma-separated list of keys to select e.g. tool:blah")] = None,
    disable_keys: Annotated[str, typer.Option(help="Comma-separated list of keys to de-select tools")] = None,
    auth: Annotated[
        Literal['local', 'passthrough'], typer.Option(help="Auth method to use for tools that need a GsSession")
    ] = 'local',
    client_id: Annotated[str, typer.Option(help="Client ID for authentication (for local auth)")] = None,
    client_secret: Annotated[str, typer.Option(help="Client ID for authentication (for local auth)")] = None,
):
    """
    CLI tool for gs-quant MCP server
    """

    # load .env file starting from current working directory
    dotenv_file = find_dotenv(usecwd=True)
    load_dotenv(dotenv_file)

    client_id = client_id or os.environ.get("CLIENT_ID")
    client_secret = client_secret or os.environ.get("CLIENT_SECRET")

    mcp_config = load_model_from_yaml(config, McpServiceConfig) if config else McpServiceConfig()
    # Override config values with command line arguments if provided
    mcp_config.base_path = base_path if base_path else mcp_config.base_path
    mcp_config.host = host if host else mcp_config.host
    mcp_config.port = port if port else mcp_config.port
    mcp_config.env = environment if environment else mcp_config.env

    print(f"Starting GsQuantMCP with config:\n{mcp_config.model_dump_json(indent=2)}")

    mcp = FastMCP(service_name)
    all_tools = get_tools(packages, extra_packages)
    for tool_key, tool in all_tools.items():
        print(f"Adding tool: :hammer_and_wrench: [cyan] {tool_key}[/]")
        mcp.add_tool(tool)
    if enable_tags:
        mcp.enable(tags={tag.strip() for tag in enable_tags.split(',')}, only=True)
    if disable_tags:
        mcp.disable(tags={tag.strip() for tag in disable_tags.split(',')})
    if enable_keys:
        mcp.enable(keys={key.strip() for key in enable_keys.split(',')}, only=True)
    if disable_keys:
        mcp.disable(keys={key.strip() for key in disable_keys.split(',')})

    if auth == 'local':
        print(f"Using local authentication with client_id: [cyan]{client_id}[/]")
        mcp.add_middleware(LocalUserAuthMiddleware(environment, client_id=client_id, client_secret=client_secret))
    else:
        print("Using remote user authentication (passthrough)")
        mcp.add_middleware(RemoteUserAuthMiddleware(environment))

    mcp.add_middleware(LoggingMiddleware())
    run_mcp_server(mcp, mcp_config)


# ---------------------------------------------------------------------------
# Client sub-app
# ---------------------------------------------------------------------------


def _parse_header_kv(items: list[str] | None) -> dict[str, str]:
    out: dict[str, str] = {}
    for raw in items or []:
        if ":" in raw:
            k, _, v = raw.partition(":")
        elif "=" in raw:
            k, _, v = raw.partition("=")
        else:
            raise typer.BadParameter(f"--header must be 'Name: value' or 'Name=value', got: {raw!r}")
        out[k.strip()] = v.strip()
    return out


@client_app.callback()
def client_main(
    ctx: typer.Context,
    url: Annotated[str, typer.Option("--url", help="Full server URL (overrides host/port/base-path)")] = None,
    config: Annotated[str, typer.Option("-c", "--config", help="Path to a server config YAML file")] = None,
    base_path: Annotated[str, typer.Option(help="Base path on the MCP server")] = "/mcp",
    host: Annotated[str, typer.Option(help="Server host to connect to")] = "localhost",
    port: Annotated[int, typer.Option(help="Server port to connect to")] = 4301,
    ssl: Annotated[bool, typer.Option("--ssl/--no-ssl", help="Use HTTPS")] = False,
    verify_ssl: Annotated[bool, typer.Option("--verify-ssl/--no-verify-ssl", help="Verify TLS certificates")] = True,
    environment: Annotated[str, typer.Option(help="Target environment (e.g., Dev, Prod)")] = None,
    client_id: Annotated[str, typer.Option(help="Client ID for GsSession-based auth")] = None,
    client_secret: Annotated[str, typer.Option(help="Client secret for GsSession-based auth")] = None,
    header: Annotated[list[str], typer.Option("--header", "-H", help="Extra header 'Name: value' (repeatable)")] = None,
):
    """Connect to a FastMCP server. With no subcommand, opens an interactive REPL."""
    dotenv_file = find_dotenv(usecwd=True)
    load_dotenv(dotenv_file)

    client_id = client_id or os.environ.get("CLIENT_ID")
    client_secret = client_secret or os.environ.get("CLIENT_SECRET")

    mcp_config = load_model_from_yaml(config, McpServiceConfig) if config else None
    if mcp_config:
        base_path = base_path if base_path != "/mcp" else mcp_config.base_path
        host = host if host != "localhost" else (mcp_config.host if mcp_config.host != "0.0.0.0" else "localhost")
        port = port if port != 4301 else (mcp_config.port or 4301)
        if mcp_config.ssl_config and not ssl:
            ssl = True

    server_url = build_server_url(url, base_path=base_path, host=host, port=port, ssl=ssl)

    def _build_client():
        print(f"Authenticating GsSession with client_id: [cyan]{client_id}[/]")
        gs_session = build_gs_session(environment, client_id, client_secret)
        h = build_auth_headers(gs_session)
        h.update(_parse_header_kv(header))
        return make_client(server_url, headers=h, verify_ssl=verify_ssl)

    if ctx.invoked_subcommand is None:
        # REPL: factory is called once on entry and again on /reconnect.
        asyncio.run(run_repl(_build_client))
    else:
        # One-shot subcommand: build a single client for the subcommand to use.
        ctx.obj = _build_client()


@client_app.command("list-tools")
def client_list_tools(ctx: typer.Context):
    """List tools available on the server."""
    run_async(ctx.obj, do_list_tools)


@client_app.command("list-resources")
def client_list_resources(ctx: typer.Context):
    """List resources exposed by the server."""
    run_async(ctx.obj, do_list_resources)


@client_app.command("list-prompts")
def client_list_prompts(ctx: typer.Context):
    """List prompts exposed by the server."""
    run_async(ctx.obj, do_list_prompts)


@client_app.command("ping")
def client_ping(ctx: typer.Context):
    """Ping the server."""
    run_async(ctx.obj, do_ping)


@client_app.command("call-tool")
def client_tool_call(
    ctx: typer.Context,
    name: Annotated[str, typer.Argument(help="Tool name")],
    args: Annotated[
        list[str],
        typer.Argument(help="Tool args: JSON object, key=value pairs, or positional values"),
    ] = None,
):
    """Call a tool. Args can be a JSON object, key=value pairs, or positional values."""
    raw = list(args or [])
    run_async(ctx.obj, lambda c: do_call_tool(c, name, raw))


@client_app.command("describe-tool")
def client_describe_tool(
    ctx: typer.Context,
    name: Annotated[str, typer.Argument(help="Tool name")],
):
    """Show a tool's parameters, types, and description."""
    run_async(ctx.obj, lambda c: do_describe_tool(c, name))


@client_app.command("read-resource")
def client_read_resource(
    ctx: typer.Context,
    uri: Annotated[str, typer.Argument(help="Resource URI")],
):
    """Read a resource by URI."""
    run_async(ctx.obj, lambda c: do_read_resource(c, uri))


@client_app.command("get-prompt")
def client_get_prompt(
    ctx: typer.Context,
    name: Annotated[str, typer.Argument(help="Prompt name")],
    args: Annotated[list[str], typer.Argument(help="Prompt args: JSON object or key=value pairs")] = None,
):
    """Get a prompt by name."""
    parsed = parse_tool_args(args or [])
    run_async(ctx.obj, lambda c: do_get_prompt(c, name, parsed))


if __name__ == "__main__":
    app()
