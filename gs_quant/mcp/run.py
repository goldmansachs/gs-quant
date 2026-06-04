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

import uvicorn
from fastmcp import FastMCP
from uvicorn.config import LOGGING_CONFIG

from gs_quant.config.utils import expand_string_with_variables
from gs_quant.mcp.config import McpServiceConfig


def _make_uvicorn_config(mcp_server: FastMCP, mcp_config: McpServiceConfig = None, port: int = None):
    app = mcp_server.http_app(path=mcp_config.base_path)
    LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
    LOGGING_CONFIG["formatters"]["access"]["fmt"] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"

    ssl_cert_file = None
    ssl_key_file = None
    if ssl_config := mcp_config.ssl_config:
        ssl_cert_file = expand_string_with_variables(ssl_config.cert_path)
        ssl_key_file = expand_string_with_variables(ssl_config.key_path)

    return uvicorn.Config(
        app,
        host=mcp_config.host,
        port=port or mcp_config.port or 4301,
        log_level="info",
        ssl_certfile=ssl_cert_file,
        ssl_keyfile=ssl_key_file,
    )


async def run_mcp_server_async(mcp_server: FastMCP, mcp_config: McpServiceConfig = None, port: int = None):
    uvicorn_config = _make_uvicorn_config(mcp_server, mcp_config, port)
    server = uvicorn.Server(uvicorn_config)
    await server.serve()


def run_mcp_server(mcp_server: FastMCP, mcp_config: McpServiceConfig = None, port: int = None):
    uvicorn_config = _make_uvicorn_config(mcp_server, mcp_config, port)
    server = uvicorn.Server(uvicorn_config)
    server.run()
