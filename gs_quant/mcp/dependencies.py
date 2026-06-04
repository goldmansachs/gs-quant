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

from fastmcp import Context
from fastmcp.dependencies import Depends
from fastmcp.exceptions import ToolError
from fastmcp.server.dependencies import CurrentContext

from gs_quant.session import GsSession


async def user_profile_from_ctx(ctx: Context = CurrentContext()) -> dict:
    user_profile = await ctx.get_state("user_profile")
    if not user_profile:
        raise ToolError("User not authenticated.")
    return user_profile


depends_user_profile = Depends(user_profile_from_ctx)


async def user_session_from_ctx(ctx: Context = CurrentContext()) -> GsSession:
    """
    Returns the user session information from the context
    """
    user_session = await ctx.get_state("user_session")
    if not user_session:
        raise ToolError("User not authenticated.")
    return user_session


depends_user_session = Depends(user_session_from_ctx)
