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

import datetime as dt
import logging
from typing import Any, Sequence

from fastmcp.server.middleware import Middleware, MiddlewareContext, CallNext
from fastmcp.tools import ToolResult, Tool
from mcp import types as mt
from rich import print

from gs_quant.mcp.session_utils import extract_from_starlette_request
from gs_quant.session import GsSession, Environment

_logger = logging.getLogger('middleware.auth')


def _time_str() -> str:
    return dt.datetime.now().isoformat(timespec='milliseconds')


class LocalUserAuthMiddleware(Middleware):
    """
    This is a very simple middleware that authenticates the user using the GsSession
    credentials provided when the middleware is initialized.
    Tools that need a GsSession object will all use this system level session.
    Not suitable for a multi-user environment, but very simple to use for a single user environment.
    """

    def __init__(
        self, environment: Environment | str = None, client_id: str | None = None, client_secret: str | None = None
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.session = GsSession.get(environment or Environment.PROD, client_id=client_id, client_secret=client_secret)
        with self.session:
            self.user_profile = GsSession.current.sync.get('/users/self')

    async def on_request(
        self, context: MiddlewareContext[mt.Request[Any, Any]], call_next: CallNext[mt.Request[Any, Any], Any]
    ) -> Any:
        request_context = context.fastmcp_context.request_context
        if request_context:
            await context.fastmcp_context.set_state("user_profile", self.user_profile)
            # serializable=False means the context is only persisted for the request.
            await context.fastmcp_context.set_state("user_session", self.session, serializable=False)
        return await call_next(context)

    async def on_call_tool(
        self,
        context: MiddlewareContext[mt.CallToolRequestParams],
        call_next: CallNext[mt.CallToolRequestParams, ToolResult],
    ) -> ToolResult:
        tool_name = context.message.name
        print(f"{_time_str()} \[call_tool :hammer_and_wrench:] using tool [green]{tool_name}[/]")
        return await super().on_call_tool(context, call_next)

    async def on_list_tools(
        self, context: MiddlewareContext[mt.ListToolsRequest], call_next: CallNext[mt.ListToolsRequest, Sequence[Tool]]
    ) -> Sequence[Tool]:
        print(f"{_time_str()} \[tools/list :scroll:]")
        return await call_next(context)


class RemoteUserAuthMiddleware(Middleware):
    """
    Pass-through auth middleware that extracts user information from the incoming request and stores it in the session.
    Tools that need a GsSession object will use a session created from the user who made the call tool request,
     provided the necessary headers were passed to the MCP server in the incoming request.
    """

    def __init__(self, environment: Environment = Environment.PROD):
        self.environment = environment or Environment.PROD

    async def on_request(
        self, context: MiddlewareContext[mt.Request[Any, Any]], call_next: CallNext[mt.Request[Any, Any], Any]
    ) -> Any:
        request_context = context.fastmcp_context.request_context
        if request_context:
            start = dt.datetime.now()
            user_profile, session = await extract_from_starlette_request(request_context.request, self.environment)
            time = (dt.datetime.now() - start).total_seconds() * 1000
            if session:
                login = user_profile.get('login')
                print(f"{_time_str()} \[session] Created session for: [green]{login}[/] in {time:.2f} ms")
                # Put as non-serializable, so it is only available for the duration of the request
                await context.fastmcp_context.set_state("user_profile", user_profile, serializable=False)
                await context.fastmcp_context.set_state("user_session", session, serializable=False)

        return await call_next(context)

    async def on_call_tool(
        self,
        context: MiddlewareContext[mt.CallToolRequestParams],
        call_next: CallNext[mt.CallToolRequestParams, ToolResult],
    ) -> ToolResult:
        user_profile = await context.fastmcp_context.get_state("user_profile")
        session_id = context.fastmcp_context.session_id
        login = user_profile.get('login') if user_profile else 'unknown'
        tool_name = context.message.name
        print(
            f"{_time_str()} \[{session_id}] \[call_tool :hammer_and_wrench:] {login} using tool [green]{tool_name}[/]"
        )
        return await call_next(context)

    async def on_list_tools(
        self, context: MiddlewareContext[mt.ListToolsRequest], call_next: CallNext[mt.ListToolsRequest, Sequence[Tool]]
    ) -> Sequence[Tool]:
        user_profile = await context.fastmcp_context.get_state("user_profile")
        session_id = context.fastmcp_context.session_id
        login = user_profile.get('login') if user_profile else 'unknown'
        print(f"{_time_str()} \[{session_id}] \[tools/list :scroll:] {login}")
        return await call_next(context)
