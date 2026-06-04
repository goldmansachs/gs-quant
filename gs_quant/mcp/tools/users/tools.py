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

from typing import Annotated

from gs_quant.api.gs.users import GsUsersApi
from gs_quant.mcp.dependencies import depends_user_profile, depends_user_session
from gs_quant.mcp.tools.registry import mcp_tool
from gs_quant.session import GsSession


@mcp_tool(tags={"user"})
def current_user_info(user_profile: dict = depends_user_profile) -> dict:
    """
    Returns information about the human user who you are chatting to, including title, location, name and department
    """
    keys_to_return = [
        "id",
        "name",
        "email",
        "city",
        "region",
        "company",
        "internal",
        "title",
        "divisionName",
        "departmentName",
    ]

    return {key: user_profile.get(key) for key in keys_to_return}


@mcp_tool(tags={"user"})
def whois(
    query: Annotated[str, "Who to search for, either a full name an identifier or kerberos"],
    user_session: GsSession = depends_user_session,
) -> dict:
    """
    Lookup users by name, identifier, email or kerberos/login
    """
    with user_session:
        search_users = GsUsersApi.search(query)
        return search_users
