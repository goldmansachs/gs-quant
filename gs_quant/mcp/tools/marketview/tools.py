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

from typing import Annotated, List, Optional

from gs_quant.api.gs.marketview.dashboards import GsMarketviewDashboardsApi
from gs_quant.api.gs.marketview.widgets import GsMarketviewWidgetsApi
from gs_quant.mcp.dependencies import depends_user_session
from gs_quant.mcp.tools.registry import mcp_tool
from gs_quant.session import GsSession

# ----------------------------------------------------------------------
# Dashboards
# ----------------------------------------------------------------------


@mcp_tool(tags={"marketview"})
def search_dashboards(
    query: Annotated[Optional[str], "Full-text search string. Cannot be combined with ids"] = None,
    ids: Annotated[Optional[List[str]], "Filter by a list of dashboard IDs. Cannot be combined with query"] = None,
    size: Annotated[int, "Number of results to return per page"] = 20,
    page: Annotated[int, "1-based page number"] = 1,
    dashboard_type: Annotated[Optional[List[str]], "Filter by dashboard type(s), e.g. ['THEMATIC', 'CUSTOM']"] = None,
    author: Annotated[Optional[List[str]], "Filter by author GUID(s)"] = None,
    user_session: GsSession = depends_user_session,
) -> dict:
    """
    Search Marketview dashboards by free-text query or filters. Returns a page of matching dashboards.
    """
    with user_session:
        return GsMarketviewDashboardsApi.get_dashboards(
            ids=ids,
            query=query,
            size=size,
            page=page,
            dashboard_type=dashboard_type,
            author=author,
        )


@mcp_tool(tags={"marketview"})
def get_dashboard(
    dashboard_id: Annotated[str, "Dashboard ID or alias string"],
    expand: Annotated[bool, "If true, inline full widget details into each child"] = False,
    widget_limit: Annotated[Optional[int], "Maximum number of widgets to expand when expand=True"] = None,
    user_session: GsSession = depends_user_session,
) -> dict:
    """
    Retrieve a single Marketview dashboard by its ID or alias, optionally expanding its widgets.
    """
    with user_session:
        return GsMarketviewDashboardsApi.get_dashboard(
            dashboard_id=dashboard_id,
            expand=expand,
            widget_limit=widget_limit,
        )


@mcp_tool(tags={"marketview"})
def get_trending_dashboards(
    limit: Annotated[int, "Maximum number of dashboards to return"] = 10,
    user_session: GsSession = depends_user_session,
) -> dict:
    """
    Retrieve trending Marketview dashboards based on platform-wide engagement signals.
    """
    with user_session:
        return GsMarketviewDashboardsApi.get_trending_dashboards(limit=limit)


@mcp_tool(tags={"marketview"})
def get_personalized_dashboards(
    limit: Annotated[int, "Maximum number of dashboards to return"] = 10,
    user_session: GsSession = depends_user_session,
) -> dict:
    """
    Retrieve Marketview dashboards personalised for the current user.
    """
    with user_session:
        return GsMarketviewDashboardsApi.get_personalized_dashboards(limit=limit)


# ----------------------------------------------------------------------
# Widgets
# ----------------------------------------------------------------------


@mcp_tool(tags={"marketview"})
def search_widgets(
    query: Annotated[Optional[str], "Full-text search string. Cannot be combined with ids"] = None,
    ids: Annotated[Optional[List[str]], "Filter by a list of widget IDs. Cannot be combined with query"] = None,
    limit: Annotated[int, "Maximum number of results to return per page"] = 20,
    offset: Annotated[int, "Number of results to skip"] = 0,
    author: Annotated[Optional[List[str]], "Filter by author GUID(s)"] = None,
    tags: Annotated[Optional[List[str]], "Filter by widget tag(s)"] = None,
    metadata: Annotated[bool, "If true, include full widget metadata in each result"] = False,
    user_session: GsSession = depends_user_session,
) -> dict:
    """
    Search Marketview widgets by free-text query or filters. Returns a page of matching widgets.
    """
    with user_session:
        return GsMarketviewWidgetsApi.get_widgets(
            ids=ids,
            query=query,
            limit=limit,
            offset=offset,
            author=author,
            tags=tags,
            metadata=metadata,
        )


@mcp_tool(tags={"marketview"})
def get_widget(
    widget_id: Annotated[str, "Widget ID"],
    merge_params: Annotated[bool, "If true, merge user-modified parameters into the widget"] = False,
    user_session: GsSession = depends_user_session,
) -> dict:
    """
    Retrieve a single Marketview widget by its ID.
    """
    with user_session:
        return GsMarketviewWidgetsApi.get_widget(widget_id=widget_id, merge_params=merge_params)


@mcp_tool(tags={"marketview"})
def get_trending_widgets(
    limit: Annotated[int, "Maximum number of widgets to return"] = 10,
    user_session: GsSession = depends_user_session,
) -> dict:
    """
    Retrieve trending Marketview widgets based on platform-wide engagement signals.
    """
    with user_session:
        return GsMarketviewWidgetsApi.get_trending_widgets(limit=limit)


@mcp_tool(tags={"marketview"})
def get_personalized_widgets(
    limit: Annotated[int, "Maximum number of widgets to return"] = 10,
    metadata: Annotated[bool, "If true, include full widget metadata in each result"] = False,
    user_session: GsSession = depends_user_session,
) -> dict:
    """
    Retrieve Marketview widgets personalised for the current user.
    """
    with user_session:
        return GsMarketviewWidgetsApi.get_personalized_widgets(limit=limit, metadata=metadata)
