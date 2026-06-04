# gs-quant MCP

> ⚠️ **Experimental.** This package is under active development and its API,
> CLI, and configuration are subject to change in future versions.

A [Model Context Protocol](https://modelcontextprotocol.io/) server (and
matching client) built on [FastMCP](https://github.com/jlowin/fastmcp) that
exposes `gs_quant` functionality as MCP tools — for consumption by LLM agents and other MCP clients.

The package ships with:

- A FastMCP **server** that auto-discovers tools, supports tag-based filtering,
  and offers two authentication strategies (`local` and `passthrough`).
- A FastMCP **client** with both one-shot CLI subcommands and an interactive
  REPL, speaking the streamable-HTTP transport.

Both are reachable through a single command-line entry point:

```bash
python -m gs_quant.mcp <server|client|discover> ...
```

---

## Contents

- [Installation](#installation)
- [Quick start](#quick-start)
- [The server](#the-server)
  - [Server CLI](#server-cli)
  - [Authentication](#authentication)
  - [Configuration file](#configuration-file)
  - [Tag and key filtering](#tag-and-key-filtering)
  - [Running a server programmatically](#running-a-server-programmatically)
- [The client](#the-client)
  - [Client CLI](#client-cli)
  - [Subcommands](#subcommands)
  - [Argument parsing for call-tool](#argument-parsing-for-call-tool)
  - [Interactive REPL](#interactive-repl)
- [Writing your own tools](#writing-your-own-tools)
  - [Registering tools](#registering-tools)
  - [Dependencies](#dependencies)
  - [Tags](#tags)
  - [Loading tools from another package](#loading-tools-from-another-package)
- [Listing all registered tools](#listing-all-registered-tools)
- [Troubleshooting](#troubleshooting)

---

## Installation

In order to use this package you will need to be using python >= `3.10` install optional `mcp` dependency.
```bash
pip intsall gs-quant[mcp]
```
or if addingo to another project with uv
```bash
uv add gs-quant[mcp]
```


## Quick start

Start a server (using your Marquee OAuth client credentials):

```bash
python -m gs_quant.mcp server \
  --client-id "$CLIENT_ID" \
  --client-secret "$CLIENT_SECRET"
```

Talk to it from another shell:

```bash
# one-shot
python -m gs_quant.mcp client list-tools
python -m gs_quant.mcp client describe-tool current_user_info
python -m gs_quant.mcp client call-tool whois "rmarti"

# interactive REPL
python -m gs_quant.mcp client
mcp> /list
mcp> /describe whois
mcp> /call whois rmarti
```

`CLIENT_ID` and `CLIENT_SECRET` may also be supplied via a `.env` file or
shell environment.

---

## The server

### Server CLI

```text
python -m gs_quant.mcp server [OPTIONS]

  --config / -c           Path to a YAML McpServiceConfig file
  --base-path             URL path the MCP endpoint is served under (default /mcp)
  --host                  Bind address (default 0.0.0.0)
  --port                  Bind port (default 4301)
  --environment           Target environment (Dev, Prod, …)
  --service-name          FastMCP server name (default GsQuantMCP)
  --packages / -p         Comma-separated packages to discover tools from
                          (default: gs_quant.mcp.tools)
  --extra-packages        Additional packages to discover tools from (comma-sep)
  --enable-tags           Comma-separated tag list — keep only tools with these tags
  --disable-tags          Comma-separated tag list — drop tools with these tags
  --enable-keys           Comma-separated tool keys (e.g. tool:my_tool) to keep
  --disable-keys          Comma-separated tool keys to drop
  --auth                  local | passthrough  (default: local)
  --client-id             OAuth client id  (local auth only)
  --client-secret         OAuth client secret  (local auth only)
```

### Authentication

The server installs one auth middleware at startup. Pick one:

#### `--auth local`  (default)

Suitable for **single-user / desktop** use. The server creates and authenticates
**one** `GsSession` at startup using `--client-id` / `--client-secret` (or the
`CLIENT_ID` / `CLIENT_SECRET` env vars / `.env` file) and reuses it for every
request.

```bash
python -m gs_quant.mcp server --auth local \
  --client-id "$CLIENT_ID" --client-secret "$CLIENT_SECRET"
```

All tools that depend on `user_session` will receive that single shared
session, regardless of who is calling.

#### `--auth passthrough`

Suitable for **multi-user / remote** deployments. No session is created at
startup. For every incoming request, the server inspects the HTTP request and
constructs a per-user `GsSession` from one of:

| Source                                    | Detected as          |
| ----------------------------------------- | -------------------- |
| `GSSSO` cookie                            | `GSSSO` SSO token    |
| `MarqueeLogin` cookie                     | `MARQUEE_LOGIN`      |
| `Authorization: Bearer ey…` (3-part JWT)  | `JWT`                |
| `Authorization: Bearer …` (otherwise)     | `OAUTH` access token |

```bash
python -m gs_quant.mcp server --auth passthrough
```

The matching client must then forward the user's auth via headers/cookies —
see [Client CLI](#client-cli).

### Configuration file

Anything supplied on the command line can also live in a YAML file passed via
`-c` / `--config`. The schema is `gs_quant.mcp.config.McpServiceConfig`:

```yaml
basePath: /mcp
host: 0.0.0.0
port: 4301
env: Prod
sslConfig:
  certPath: ${HOME}/certs/server.crt
  keyPath: ${HOME}/certs/server.key
```

Environment-style `${VAR}` substitution is supported in `sslConfig` paths.

### Tag and key filtering

Every tool may be tagged (see [Writing your own tools](#tags)). The server
exposes four flags to slice the registry at startup:

```bash
# Keep only tools tagged "user" or "data":
python -m gs_quant.mcp server --enable-tags user,data

# Disable a single noisy tool by key:
python -m gs_quant.mcp server --disable-keys tool:current_user_info
```

`--enable-*` flags imply `only=True`, i.e. they whitelist; `--disable-*` flags
remove. They may be combined.

### Running a server programmatically

> Example showing how to construct a `FastMCP`
> server in code, register tools manually (via `discover_tools`), attach
> middleware, and start it via `gs_quant.mcp.run.run_mcp_server` /
> `run_mcp_server_async`._

```python
from fastmcp import FastMCP
from typing import Literal

from gs_quant.mcp import McpServiceConfig, run_mcp_server
from gs_quant.mcp.dependencies import depends_user_session
from gs_quant.mcp.middleware import LocalUserAuthMiddleware
from gs_quant.mcp.tools import mcp_tool, get_registered_tools
from gs_quant.session import GsSession
from gs_quant.data import Dataset
import datetime as dt

mcp = FastMCP("MyMCP")

@mcp_tool()
def g3_spot(cross: Literal['GBPUSD', 'EURUSD', 'USDJPY'], user_session: GsSession = depends_user_session) -> dict:
    """Return some data"""
    with user_session:
        return Dataset("FXSPOT_STANDARD").get_data_last(as_of=dt.date.today(), bbid=cross).iloc[0].to_dict()


all_tools = get_registered_tools()  # Find tools inside this package
for _, tool in all_tools.items():
    mcp.add_tool(tool)
mcp.add_middleware(LocalUserAuthMiddleware(client_id="CLIENT_ID", client_secret="CLIENT_SECRET"))
run_mcp_server(mcp, McpServiceConfig(), port=4301)
```

---

## The client

The client speaks **streamable HTTP only**. Auth
material is sourced from a local `GsSession` (external users must provide `--client-id`/`--client-secret`) and forwarded as headers/cookies, so a server running with `--auth passthrough`
server can authenticate the caller.

### Client CLI

```text
python -m gs_quant.mcp client [OPTIONS] COMMAND [ARGS]...

Connection
  --url               Full server URL (overrides host/port/base-path)
  --config / -c       Reuse a server's McpServiceConfig YAML to derive the URL
  --base-path         Server base path (default /mcp)
  --host              Server host (default localhost)
  --port              Server port (default 4301)
  --ssl / --no-ssl    Use https (default no-ssl)
  --verify-ssl /
  --no-verify-ssl     Toggle TLS cert verification (default verify)

Auth
  --environment       Target environment for the GsSession (Dev, Prod, …)
  --client-id         OAuth client id  (or env CLIENT_ID)
  --client-secret     OAuth client secret  (or env CLIENT_SECRET)
  -H / --header K=V   Extra header (repeatable). Also accepts "Name: value".
```

When credentials are supplied the client builds a real `GsSession`, extracts
its `Authorization`, `X-Application`, `X-Version`, `X-MARQUEE-CSRF-TOKEN`
headers and `GSSSO` / `MarqueeLogin` / `MARQUEE-CSRF-TOKEN` cookies, and
forwards them to the server.

If you only want to override a single header (e.g. inject a known token) just
use `-H`:

```bash
python -m gs_quant.mcp client \
  --url http://example.com:4301/mcp \
  -H "Authorization: Bearer eyJ..." \
  list-tools
```

### Subcommands

| Subcommand                      | Description                                      |
| ------------------------------- | ------------------------------------------------ |
| `list-tools`                    | List tools available on the server               |
| `list-resources`                | List resources                                   |
| `list-prompts`                  | List prompts                                     |
| `describe-tool <name>`          | Show a tool's parameters, types and description  |
| `call-tool <name> [args...]`    | Call a tool                                      |
| `read-resource <uri>`           | Read a resource by URI                           |
| `get-prompt <name> [args...]`   | Get a prompt                                     |
| `ping`                          | Round-trip ping the server                       |
| _no subcommand_                 | Drop into the interactive REPL                   |

### Argument parsing for `call-tool`

Given a simple example tool.
```python
from gs_quant.mcp.tools import mcp_tool

@mcp_tool
def add(a: int, b: int = 1) -> int:
    """Return a + b."""
    return a + b
```

Tool arguments are accepted in three forms (resolved in this order):

1. **JSON object** — quote the whole thing so the shell doesn't split it.
   ```bash
   python -m gs_quant.mcp client call-tool add '{"a": 3, "b": 4}'
   ```
2. **`key=value` pairs** — values are JSON-decoded when possible (so `n=10`
   becomes the integer `10`, `flag=true` becomes the boolean `true`, etc.).
   ```bash
   python -m gs_quant.mcp client call-tool add a=10 b=20
   ```
3. **Positional** — bound to the tool's parameters in declaration order
   (required first, then optional). The client fetches the schema from the
   server to do this binding.
   ```bash
   python -m gs_quant.mcp client call-tool add 3 4
   ```

Use `describe-tool` to check the parameter order and types:

```bash
python -m gs_quant.mcp client describe-tool add
# add - Return a + b.
# ┏━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┓
# ┃ name ┃ type    ┃ required ┃ default ┃ description ┃
# ┡━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━┩
# │ a    │ integer │ yes      │         │             │
# │ b    │ integer │ no       │ 1       │             │
# └──────┴─────────┴──────────┴─────────┴─────────────┘
```

Server-side errors (e.g. `ToolError`) are surfaced as a single concise line
and the CLI exits with status `1`.

### Interactive REPL

Run the client without a subcommand:

```bash
python -m gs_quant.mcp client
```

You get a `prompt_toolkit`-backed prompt with persistent history at
`~/.gs_quant_mcp_history` and tab-completion over slash commands and tool
names. Available commands:

```text
/list                       List tools
/list-resources             List resources
/list-prompts               List prompts
/describe <name>            Show a tool's parameters and types
/call <name> [args...]      Call a tool (same arg parsing as call-tool)
/read <uri>                 Read a resource by URI
/prompt <name> [args...]    Get a prompt
/ping                       Ping the server
/refresh                    Refresh tool-name completion cache
/help, /?                   Show help
/quit, /exit                Exit (Ctrl-D also works)
```

Errors raised inside REPL commands are caught and printed without exiting the
session.

---

## Writing your own tools

### Registering tools

Tools are plain Python functions decorated with `@mcp_tool(...)` from
`gs_quant.mcp.tools.registry`. The decorator both:

1. Applies FastMCP's `@tool(...)` (so all kwargs forward — `tags`, `name`,
   `description`, etc.).
2. Records the function in a module-level registry keyed by
   `<module>.<qualname>` so it can be discovered later.

```python
# my_pkg/tools/math_tools.py
from typing import Annotated

from gs_quant.mcp.tools.registry import mcp_tool


@mcp_tool(tags={"math"})
def add(
    a: Annotated[int, "First addend"],
    b: Annotated[int, "Second addend"] = 0,
) -> int:
    """Return ``a + b``."""
    return a + b
```

`Annotated[T, "..."]` strings become parameter descriptions in the resulting
JSON Schema, which the client surfaces via `describe-tool`.

If you'd prefer to keep FastMCP's stock `@tool` decorator, stack
`@register_mcp_tool` on top of it instead:

```python
from fastmcp.tools import tool
from gs_quant.mcp.tools.registry import register_mcp_tool


@register_mcp_tool
@tool(tags={"math"})
def multiply(a: int, b: int) -> int:
    return a * b
```

For further details on annotating MCP tools see [FastMCP documentation](https://gofastmcp.com/servers/tools) 

### Dependencies

Tools can request a per-call user identity / session via FastMCP's `Depends`
mechanism. `gs_quant.mcp.dependencies` ships two ready-made dependencies:

| Symbol                  | Resolves to                                      |
| ----------------------- | ------------------------------------------------ |
| `depends_user_profile`  | `dict` — the Marquee `/users/self` profile       |
| `depends_user_session`  | `GsSession` — authenticated for the calling user |

```python
from gs_quant.mcp.dependencies import depends_user_session
from gs_quant.mcp.tools.registry import mcp_tool
from gs_quant.session import GsSession


@mcp_tool(tags={"user"})
def whois(query: str, user_session: GsSession = depends_user_session) -> dict:
    """A tool that needs to make authenticated requests to Marquee."""
    with user_session:
        return GsSession.current.sync.get("/path/to/api")
```

Under `--auth local` both dependencies resolve based on the `client-id` and `client_secret` of the MCP **server**.
Under `--auth passthrough` they resolve to a session built from the incoming
request's cookies/headers. If a tool requests them and the request lacks
credentials, the dependency raises `ToolError("User not authenticated.")`.

### Tags

`tags={"a", "b"}` lets you slice the tool surface area at server start time.
Common patterns:

```bash
# A "reading" server — pick only safe tools
python -m gs_quant.mcp server --enable-tags user,data

# Everything except experimental tools
python -m gs_quant.mcp server --disable-tags experimental
```

Tags are also visible in `python -m gs_quant.mcp discover-tools` output.

### Loading tools from another package

The server discovers tools by importing every submodule of the packages listed
in `--packages` / `--extra-packages` (so each `@mcp_tool` runs and registers
itself):

```bash
# Replace the default discovery package
python -m gs_quant.mcp server -p mycorp.mcp.tools

# Or layer your tools on top of the built-ins
python -m gs_quant.mcp server --extra-packages mycorp.mcp.tools,otherorg.mcp.tools
```

The package(s) you pass must be importable in the running interpreter. There
is no special plugin manifest — any module reachable from
`pkgutil.walk_packages` is imported.

---

## Listing all registered tools

To see what `--packages` would discover without starting a server:

```bash
python -m gs_quant.mcp discover-tools \
  --packages gs_quant.mcp.tools \
  --extra-packages mycorp.mcp.tools
```

This prints each tool's qualified key, tags, and docstring.

---

## Troubleshooting

- **`ToolError: User not authenticated.`** — the tool requested a user session
  but none was provided. Either run the server with `--auth local` and valid
  client credentials, or run the client with `--client-id` / `--client-secret`
  (or `-H "Authorization: Bearer ..."`) so credentials are forwarded to a
  `--auth passthrough` server.
- **Self-signed TLS certs** — pass `--no-verify-ssl` to the client.
- **REPL has no tool-name completion** — make sure the connection succeeded;
  if `list-tools` failed at startup the REPL still opens but the completer
  only knows slash commands. Use `/refresh` after the server is reachable.
