"""
Copyright 2019 Goldman Sachs.
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

import logging
from typing import List, Union

from gs_quant.api.gs.marketview.types import (
    DashboardChild,
    DashboardCreateRequest,
    DashboardEntitlements,
    DashboardSection,
    DashboardUpdateRequest,
    SectionChildrenRequest,
    SectionCopyRequest,
    SectionReorderRequest,
)
from gs_quant.session import GsSession

_logger = logging.getLogger(__name__)

API = '/marketview/dashboards'


class GsMarketviewDashboardsApi:
    """
    Client library for the Goldman Sachs Marketview Dashboards API.

    Provides methods for searching, retrieving, creating, updating, cloning,
    sharing, and deleting Marketview dashboards and their children (widgets)
    and sections.
    """

    # ------------------------------------------------------------------
    # Dashboard search / retrieval
    # ------------------------------------------------------------------

    @classmethod
    def get_dashboards(
        cls,
        ids: List[str] = None,
        query: str = None,
        size: int = 100,
        page: int = 1,
        order_by: str = '>lastUpdatedTime',
        view_as: str = None,
        dashboard_type: List[str] = None,
        author: List[str] = None,
    ) -> dict:
        """
        Search / list dashboards with optional filters.

        :param ids: Filter by a list of dashboard IDs. Cannot be combined with ``query``.
        :param query: Full-text search string. Cannot be combined with ``ids``.
        :param size: Number of results to return per page (default 100).
        :param page: 1-based page number (default 1).
        :param order_by: Sort expression, e.g. ``'>lastUpdatedTime'`` (default).
        :param view_as: Entitlement perspective to apply, e.g. ``'view'`` or ``'edit'``.
        :param dashboard_type: Filter by dashboard type(s), e.g. ``['THEMATIC', 'CUSTOM']``.
        :param author: Filter by author GUID(s).
        :return: dict containing ``results`` and ``totalResults``.
        """
        url = f'{API}?size={size}&page={page}&orderBy={order_by}'
        if ids:
            url += ''.join(f'&id={i}' for i in ids)
        if query:
            url += f'&query={query}'
        if view_as:
            url += f'&viewAs={view_as}'
        if dashboard_type:
            url += ''.join(f'&type={t}' for t in dashboard_type)
        if author:
            url += ''.join(f'&author={a}' for a in author)
        return GsSession.current.sync.get(url)

    @classmethod
    def get_my_dashboards(
        cls,
        limit: int = 100,
        offset: int = 0,
        order_by: str = '>lastUpdatedTime',
    ) -> dict:
        """
        Retrieve all dashboards owned by the currently authenticated user.

        :param limit: Maximum number of results to return (default 100).
        :param offset: Number of results to skip (default 0).
        :param order_by: Sort expression (default ``'>lastUpdatedTime'``).
        :return: dict containing ``results`` and ``totalResults``.
        """
        url = f'{API}/self?limit={limit}&offset={offset}&orderBy={order_by}'
        return GsSession.current.sync.get(url)

    @classmethod
    def get_personal_dashboard(
        cls,
        expand: bool = False,
        widget_limit: int = None,
    ) -> dict:
        """
        Retrieve the personal (sandbox) dashboard for the current user.
        The dashboard is created automatically if it does not yet exist.

        :param expand: If ``True``, inline full widget details into each child (default ``False``).
        :param widget_limit: Maximum number of widgets to expand when ``expand=True``.
        :return: Dashboard document as a dict.
        """
        url = f'{API}/personal?expand={str(expand).lower()}'
        if widget_limit is not None:
            url += f'&widgetLimit={widget_limit}'
        return GsSession.current.sync.get(url)

    @classmethod
    def get_dashboard(
        cls,
        dashboard_id: str,
        expand: bool = False,
        widget_limit: int = None,
        include_modified_params: bool = False,
    ) -> dict:
        """
        Retrieve a single dashboard by its ID or alias.

        :param dashboard_id: Dashboard ID or alias string.
        :param expand: If ``True``, inline full widget details into each child (default ``False``).
        :param widget_limit: Maximum number of widgets to expand when ``expand=True``.
        :param include_modified_params: Whether to include user-modified widget parameters
            (default ``False``).
        :return: Dashboard document as a dict.
        """
        url = (
            f'{API}/{dashboard_id}'
            f'?expand={str(expand).lower()}'
            f'&includeModifiedParams={str(include_modified_params).lower()}'
        )
        if widget_limit is not None:
            url += f'&widgetLimit={widget_limit}'
        return GsSession.current.sync.get(url)

    @classmethod
    def get_namespaced_dashboard(
        cls,
        namespace: str,
        dashboard_alias: str,
        expand: bool = False,
        widget_limit: int = None,
        include_modified_params: bool = True,
    ) -> dict:
        """
        Retrieve a dashboard by its namespace and alias.

        :param namespace: Dashboard namespace (e.g. a user GUID or team slug).
        :param dashboard_alias: Dashboard alias within the namespace.
        :param expand: If ``True``, inline full widget details into each child (default ``False``).
        :param widget_limit: Maximum number of widgets to expand when ``expand=True``.
        :param include_modified_params: Whether to include user-modified widget parameters
            (default ``True``).
        :return: Dashboard document as a dict.
        """
        url = (
            f'{API}/{namespace}/{dashboard_alias}'
            f'?expand={str(expand).lower()}'
            f'&includeModifiedParams={str(include_modified_params).lower()}'
        )
        if widget_limit is not None:
            url += f'&widgetLimit={widget_limit}'
        return GsSession.current.sync.get(url)

    @classmethod
    def get_dashboard_history(
        cls,
        dashboard_id: str,
        limit: int = 10,
        offset: int = 0,
        order_by: str = '>lastUpdatedTime',
    ) -> dict:
        """
        Retrieve older saved versions of a dashboard.

        :param dashboard_id: Dashboard ID.
        :param limit: Maximum number of history records to return (default 10).
        :param offset: Number of records to skip (default 0).
        :param order_by: Sort expression (default ``'>lastUpdatedTime'``).
        :return: dict containing ``results`` and ``totalResults``.
        """
        url = f'{API}/{dashboard_id}/history?limit={limit}&offset={offset}&orderBy={order_by}'
        return GsSession.current.sync.get(url)

    @classmethod
    def get_trending_dashboards(cls, limit: int = 10) -> dict:
        """
        Retrieve trending dashboards based on platform-wide engagement signals.

        :param limit: Maximum number of dashboards to return (default 10).
        :return: dict containing ``results`` and ``totalResults``.
        """
        return GsSession.current.sync.get(f'{API}/trending?limit={limit}')

    @classmethod
    def get_personalized_dashboards(cls, limit: int = 10) -> dict:
        """
        Retrieve dashboards personalised for the current user.

        :param limit: Maximum number of dashboards to return (default 10).
        :return: dict containing ``results`` and ``totalResults``.
        """
        return GsSession.current.sync.get(f'{API}/personalized?limit={limit}')

    @classmethod
    def get_dashboard_metrics(
        cls,
        limit: int = 10,
        offset: int = 0,
        action: str = 'opened',
        order_by: List[str] = None,
        public: bool = False,
    ) -> dict:
        """
        Retrieve aggregated engagement metrics for dashboards.

        :param limit: Maximum number of results (default 10).
        :param offset: Number of results to skip (default 0).
        :param action: Metric action to aggregate on, e.g. ``'opened'`` (default).
        :param order_by: List of sort expressions, e.g. ``['>total']``.
        :param public: If ``True``, return metrics across all users; otherwise scoped to
            the current user (default ``False``).
        :return: Metrics document as a dict.
        """
        order_by = order_by or ['>total']
        url = f'{API}/metrics?limit={limit}&offset={offset}&action={action}&public={str(public).lower()}'
        url += ''.join(f'&orderBy={o}' for o in order_by)
        return GsSession.current.sync.get(url)

    # ------------------------------------------------------------------
    # Entitlements
    # ------------------------------------------------------------------

    @classmethod
    def get_bulk_dashboard_entitlements(cls, user_guid: str, ids: List[str]) -> dict:
        """
        Check entitlements for a specific user across multiple dashboards in one call.

        :param user_guid: GUID of the user whose entitlements are being queried.
        :param ids: List of dashboard IDs to check.
        :return: dict mapping dashboard ID → entitlement map (``view``, ``edit``, ``admin``).
        """
        payload = {'userGuid': user_guid, 'ids': ids}
        return GsSession.current.sync.post(f'{API}/entitlements', payload)

    # ------------------------------------------------------------------
    # Create
    # ------------------------------------------------------------------

    @classmethod
    def create_thematic_dashboard(cls, dashboard: DashboardCreateRequest) -> dict:
        """
        Create a new Thematic dashboard. Requires curator entitlements.

        :param dashboard: :class:`~gs_quant.api.gs.marketview.types.DashboardCreateRequest`
            describing the new dashboard. ``type`` will be overridden to ``THEMATIC``
            server-side.
        :return: Created dashboard document as a dict.
        """
        return GsSession.current.sync.post(API, dashboard.to_dict())

    @classmethod
    def create_custom_dashboard(cls, namespace: str, dashboard: DashboardCreateRequest) -> dict:
        """
        Create a new Custom dashboard under a given namespace.

        Pass ``'default'`` as the namespace to have the server resolve it to the
        current user's personal namespace automatically.

        :param namespace: Target namespace slug, or ``'default'`` for personal namespace.
        :param dashboard: :class:`~gs_quant.api.gs.marketview.types.DashboardCreateRequest`
            describing the new dashboard. ``type`` must be ``DashboardType.CUSTOM`` or omitted.
        :return: Created dashboard document as a dict.
        """
        return GsSession.current.sync.post(f'{API}/{namespace}', dashboard.to_dict())

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------

    @classmethod
    def update_dashboard(cls, dashboard_id: str, dashboard: DashboardUpdateRequest) -> dict:
        """
        Perform a partial update of a dashboard.

        Only fields explicitly set on ``dashboard`` are sent; the rest are preserved
        via server-side merging.

        :param dashboard_id: ID of the dashboard to update.
        :param dashboard: :class:`~gs_quant.api.gs.marketview.types.DashboardUpdateRequest`
            containing the fields to update.
        :return: Updated dashboard document as a dict.
        """
        return GsSession.current.sync.put(f'{API}/{dashboard_id}', dashboard.to_dict())

    @classmethod
    def update_dashboard_entitlements(
        cls,
        dashboard_id: str,
        entitlements: DashboardEntitlements,
        share_widgets: bool = False,
    ) -> dict:
        """
        Update the entitlements (sharing settings) of a dashboard.

        :param dashboard_id: ID of the dashboard to share.
        :param entitlements: :class:`~gs_quant.api.gs.marketview.types.DashboardEntitlements`
            with ``view``, ``edit``, and ``admin`` token lists.
        :param share_widgets: If ``True``, propagate the same entitlements to all
            eligible widgets on the dashboard (default ``False``).
        :return: dict containing the updated ``dashboard`` and any updated ``widgets``.
        """
        url = f'{API}/{dashboard_id}/share?shareWidgets={str(share_widgets).lower()}'
        return GsSession.current.sync.put(url, entitlements.to_dict())

    @classmethod
    def promote_dashboard(cls, dashboard_id: str) -> dict:
        """
        Promote a Custom dashboard to Thematic status.
        Requires curator or support entitlements.

        :param dashboard_id: ID of the Custom dashboard to promote.
        :return: Updated dashboard document as a dict.
        """
        return GsSession.current.sync.put(f'{API}/{dashboard_id}/promote', {})

    # ------------------------------------------------------------------
    # Delete
    # ------------------------------------------------------------------

    @classmethod
    def delete_dashboard(cls, dashboard_id: str) -> dict:
        """
        Permanently delete a dashboard.

        :param dashboard_id: ID of the dashboard to delete.
        :return: Confirmation message as a dict.
        """
        return GsSession.current.sync.delete(f'{API}/{dashboard_id}')

    # ------------------------------------------------------------------
    # Clone
    # ------------------------------------------------------------------

    @classmethod
    def clone_dashboard(cls, dashboard_id: str) -> dict:
        """
        Clone a dashboard into the current user's personal namespace.

        The cloned dashboard will have type ``CUSTOM`` and its title will be
        suffixed with ``' Copy'``.

        :param dashboard_id: ID of the source dashboard to clone.
        :return: Newly created (cloned) dashboard document as a dict.
        """
        return GsSession.current.sync.post(f'{API}/{dashboard_id}/clone', {})

    # ------------------------------------------------------------------
    # Children (widgets)
    # ------------------------------------------------------------------

    @classmethod
    def add_children(
        cls,
        dashboard_id: str,
        children: Union[DashboardChild, List[DashboardChild]],
    ) -> dict:
        """
        Add one or more widget children to a dashboard.

        Pass a single :class:`~gs_quant.api.gs.marketview.types.DashboardChild` to add
        one widget, or a list to add multiple in a single request.

        :param dashboard_id: Target dashboard ID, or ``'personal'`` to target
            the current user's personal dashboard.
        :param children: A :class:`~gs_quant.api.gs.marketview.types.DashboardChild`
            or list of them. Each must have ``entity_id`` set for widget children.
        :return: Updated dashboard document as a dict.
        """
        payload = [c.to_dict() for c in children] if isinstance(children, list) else children.to_dict()
        return GsSession.current.sync.post(f'{API}/{dashboard_id}/children', payload)

    @classmethod
    def update_child(
        cls,
        dashboard_id: str,
        child_id: str,
        child: DashboardChild,
    ) -> dict:
        """
        Update a specific widget child on a dashboard (e.g. update its parameters).

        :param dashboard_id: Dashboard ID, or ``'personal'`` for the personal dashboard.
        :param child_id: ID of the child entry to update.
        :param child: :class:`~gs_quant.api.gs.marketview.types.DashboardChild` with
            the updated fields.
        :return: Updated dashboard document as a dict.
        """
        return GsSession.current.sync.put(f'{API}/{dashboard_id}/children/{child_id}', child.to_dict())

    @classmethod
    def remove_child(cls, dashboard_id: str, child_id: str) -> dict:
        """
        Remove a widget child from a dashboard.

        :param dashboard_id: Dashboard ID, or ``'personal'`` for the personal dashboard.
        :param child_id: ID of the child entry to remove.
        :return: Updated dashboard document as a dict.
        """
        return GsSession.current.sync.delete(f'{API}/{dashboard_id}/children/{child_id}')

    # ------------------------------------------------------------------
    # Sections
    # ------------------------------------------------------------------

    @classmethod
    def create_section(cls, dashboard_id: str, section: DashboardSection) -> dict:
        """
        Add a new section to a dashboard.

        :param dashboard_id: Target dashboard ID.
        :param section: :class:`~gs_quant.api.gs.marketview.types.DashboardSection`
            describing the new section.
        :return: Updated dashboard document as a dict.
        """
        return GsSession.current.sync.post(f'{API}/{dashboard_id}/sections', section.to_dict())

    @classmethod
    def update_section(cls, dashboard_id: str, section_id: str, section: DashboardSection) -> dict:
        """
        Update a single section within a dashboard.

        :param dashboard_id: Dashboard ID.
        :param section_id: ID of the section to update.
        :param section: :class:`~gs_quant.api.gs.marketview.types.DashboardSection`
            with the updated fields.
        :return: Updated dashboard document as a dict.
        """
        return GsSession.current.sync.put(f'{API}/{dashboard_id}/sections/{section_id}', section.to_dict())

    @classmethod
    def update_sections(cls, dashboard_id: str, sections: List[DashboardSection]) -> dict:
        """
        Bulk-update multiple sections within a dashboard in a single request.

        :param dashboard_id: Dashboard ID.
        :param sections: List of :class:`~gs_quant.api.gs.marketview.types.DashboardSection`
            objects. Each must have ``id`` set to identify which section to update.
        :return: Updated dashboard document as a dict.
        """
        return GsSession.current.sync.put(f'{API}/{dashboard_id}/sections', [s.to_dict() for s in sections])

    @classmethod
    def delete_section(cls, dashboard_id: str, section_id: str) -> dict:
        """
        Delete a section from a dashboard.

        Children that belonged to the deleted section remain on the dashboard
        (server-side they are re-ranked at the root level).

        :param dashboard_id: Dashboard ID.
        :param section_id: ID of the section to delete.
        :return: Updated dashboard document as a dict.
        """
        return GsSession.current.sync.delete(f'{API}/{dashboard_id}/sections/{section_id}')

    @classmethod
    def get_section(
        cls,
        dashboard_id: str,
        section_id: str,
        expand: bool = False,
    ) -> dict:
        """
        Retrieve a single section from a dashboard by its ID.

        :param dashboard_id: Dashboard ID.
        :param section_id: ID of the section to retrieve.
        :param expand: If ``True``, inline full widget details for each child in the
            section (default ``False``).
        :return: Section document as a dict.
        """
        url = f'{API}/{dashboard_id}/sections/{section_id}?expand={str(expand).lower()}'
        return GsSession.current.sync.get(url)

    @classmethod
    def add_children_to_section(
        cls,
        dashboard_id: str,
        section_id: str,
        payload: SectionChildrenRequest,
    ) -> dict:
        """
        Add children to an existing section.

        Provide **either** ``child_ids`` **or** ``widgets`` on the
        :class:`~gs_quant.api.gs.marketview.types.SectionChildrenRequest` — not both.

        * ``child_ids`` — existing child IDs already on the dashboard are copied
          into the section.
        * ``widgets`` — widget IDs (with optional ``configuration_id``) that are
          auto-added to the dashboard if not already present, then appended to the
          section.

        :param dashboard_id: Dashboard ID, or ``'personal'`` for the personal dashboard.
        :param section_id: ID of the target section.
        :param payload: :class:`~gs_quant.api.gs.marketview.types.SectionChildrenRequest`
            describing the children to add.
        :return: Updated dashboard document as a dict.
        """
        return GsSession.current.sync.post(f'{API}/{dashboard_id}/sections/{section_id}/children', payload.to_dict())

    @classmethod
    def remove_child_from_section(
        cls,
        dashboard_id: str,
        section_id: str,
        child_id: str,
    ) -> dict:
        """
        Remove a child from a section without deleting it from the dashboard.

        The child remains in ``dashboard.children`` (unsectioned) after removal.

        :param dashboard_id: Dashboard ID, or ``'personal'`` for the personal dashboard.
        :param section_id: ID of the section to remove the child from.
        :param child_id: ID of the child entry to remove from the section.
        :return: Updated dashboard document as a dict.
        """
        return GsSession.current.sync.delete(f'{API}/{dashboard_id}/sections/{section_id}/children/{child_id}')

    @classmethod
    def copy_section(
        cls,
        dashboard_id: str,
        payload: SectionCopyRequest,
    ) -> dict:
        """
        Copy an entire section (with all its children) from a source dashboard
        into the target dashboard.

        Every child in the source section is re-created as a brand-new child on
        the target dashboard, preserving configuration, parameters, renderParams,
        relativeDate, calculatedDates, and modifiedParameters.

        :param dashboard_id: ID of the target dashboard to copy the section into.
        :param payload: :class:`~gs_quant.api.gs.marketview.types.SectionCopyRequest`
            identifying the source dashboard and section.
        :return: Updated target dashboard document as a dict.
        """
        return GsSession.current.sync.post(f'{API}/{dashboard_id}/sections/copy', payload.to_dict())

    @classmethod
    def reorder_sections(
        cls,
        dashboard_id: str,
        payload: SectionReorderRequest,
    ) -> dict:
        """
        Reorder all sections within a dashboard by providing an ordered list of
        section IDs.

        Every section ID in the dashboard must be present in ``payload.section_ids``
        exactly once.

        :param dashboard_id: Dashboard ID.
        :param payload: :class:`~gs_quant.api.gs.marketview.types.SectionReorderRequest`
            with the full ordered list of section IDs.
        :return: Updated dashboard document as a dict.
        """
        return GsSession.current.sync.post(f'{API}/{dashboard_id}/sections/reorder', payload.to_dict())
