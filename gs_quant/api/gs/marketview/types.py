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

import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


# ------------------------------------------------------------------
# Enums
# ------------------------------------------------------------------


class DashboardType(Enum):
    """Type of a Marketview dashboard."""

    PERSONAL = 'Personal'
    CUSTOM = 'Custom'
    THEMATIC = 'Thematic'


class DashboardChildType(Enum):
    """Type of a dashboard child element."""

    WIDGET = 'Widget'
    TEXT = 'Text'


# ------------------------------------------------------------------
# Supporting types
# ------------------------------------------------------------------


@dataclass
class DashboardEntitlements:
    """
    Entitlement tokens that control who can view, edit, or administer a dashboard.

    Each list contains token strings of the form ``'guid:<USER_GUID>'``,
    ``'group:<GROUP_ID>'``, or a role token.

    :param view: Tokens that grant view access.
    :param edit: Tokens that grant edit access.
    :param admin: Tokens that grant admin access.
    """

    view: List[str] = field(default_factory=list)
    edit: List[str] = field(default_factory=list)
    admin: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {'view': self.view, 'edit': self.edit, 'admin': self.admin}


@dataclass
class RelatedLink:
    """
    An external link to attach to a dashboard.

    :param link: The URL.
    :param title: Display title for the link.
    :param summary: Short description of the linked content.
    :param id: Unique identifier for this link (auto-generated if not provided).
    :param authors: List of author names or GUIDs associated with the link.
    """

    link: str
    title: Optional[str] = None
    summary: Optional[str] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    authors: Optional[List[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {'id': self.id, 'link': self.link}
        if self.title is not None:
            d['title'] = self.title
        if self.summary is not None:
            d['summary'] = self.summary
        if self.authors is not None:
            d['authors'] = self.authors
        return d


@dataclass
class DashboardChild:
    """
    A widget (or text block) pinned to a dashboard.

    :param entity_id: ID of the widget to attach. Required when ``type`` is
        ``DashboardChildType.WIDGET``.
    :param type: Child element type (default ``DashboardChildType.WIDGET``).
    :param rank: Display order of this child within the dashboard or section
        (1-based, default ``1``).
    :param parameters: List of parameter override dicts, each with ``parameterId``
        and ``value`` keys, used to customise the widget for this dashboard slot.
    :param configuration_id: Server-assigned configuration ID (read-only on create).
    :param contributed_by: GUID of the user who added this child.
    :param id: Unique identifier for this child slot (auto-generated if not provided).
    """

    entity_id: Optional[str] = None
    type: DashboardChildType = DashboardChildType.WIDGET
    rank: int = 1
    parameters: List[Dict] = field(default_factory=list)
    configuration_id: Optional[str] = None
    contributed_by: Optional[str] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            'id': self.id,
            'type': self.type.value,
            'rank': self.rank,
            'parameters': self.parameters,
        }
        if self.entity_id is not None:
            d['entity_id'] = self.entity_id
        if self.configuration_id is not None:
            d['configurationId'] = self.configuration_id
        if self.contributed_by is not None:
            d['contributed_by'] = self.contributed_by
        return d


@dataclass
class DashboardSection:
    """
    A named grouping of widget children within a dashboard.

    :param title: Display title of the section.
    :param description: Optional description shown beneath the section title.
    :param children: Ordered list of child IDs (``DashboardChild.id``) that belong
        to this section.
    :param rank: Display order of this section (1-based, default ``1``).
    :param id: Unique identifier for the section (auto-generated if not provided).
    """

    title: str
    description: Optional[str] = None
    children: List[str] = field(default_factory=list)
    rank: Optional[int] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {'id': self.id, 'title': self.title, 'children': self.children}
        if self.description is not None:
            d['description'] = self.description
        if self.rank is not None:
            d['rank'] = self.rank
        return d


# ------------------------------------------------------------------
# Dashboard request types
# ------------------------------------------------------------------


@dataclass
class DashboardCreateRequest:
    """
    Payload for creating a new dashboard.

    :param title: Display title of the dashboard.
    :param type: Dashboard type (default ``DashboardType.CUSTOM``).
    :param alias: URL-friendly alias, unique within the namespace. Must be lowercase.
    :param namespace: Namespace for the dashboard. Pass ``'default'`` to use the
        current user's personal namespace. Leave ``None`` for thematic dashboards.
    :param description: Optional long-form description.
    :param tags: List of tag strings to aid discovery.
    :param entitlements: Access control tokens. If ``None`` the server applies
        sensible defaults.
    :param children: List of :class:`DashboardChild` items to attach on creation.
    :param sections: List of :class:`DashboardSection` items to create on creation.
    :param related_links: List of :class:`RelatedLink` items.
    :param copy_from_id: ID of a dashboard this was copied from (informational).
    :param add_tags_from_children: If ``True``, automatically inherit tags from
        added widgets (default ``False``).
    :param is_requestable: Whether users can request access via the platform UI
        (default ``False``).
    """

    title: Optional[str] = 'My Dashboard'
    type: Optional[DashboardType] = DashboardType.CUSTOM
    alias: Optional[str] = None
    namespace: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    entitlements: Optional[DashboardEntitlements] = None
    children: List[DashboardChild] = field(default_factory=list)
    sections: List[DashboardSection] = field(default_factory=list)
    related_links: List[RelatedLink] = field(default_factory=list)
    copy_from_id: Optional[str] = None
    add_tags_from_children: bool = False
    is_requestable: bool = False

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            'children': [c.to_dict() for c in self.children],
            'sections': [s.to_dict() for s in self.sections],
            'relatedLinks': [r.to_dict() for r in self.related_links],
            'tags': self.tags,
            'addTagsFromChildren': self.add_tags_from_children,
            'isRequestable': self.is_requestable,
        }
        if self.title is not None:
            d['title'] = self.title
        if self.type is not None:
            d['type'] = self.type.value
        if self.alias is not None:
            d['alias'] = self.alias.lower()
        if self.namespace is not None:
            d['namespace'] = self.namespace
        if self.description is not None:
            d['description'] = self.description
        if self.entitlements is not None:
            d['entitlements'] = self.entitlements.to_dict()
        if self.copy_from_id is not None:
            d['copyFromId'] = self.copy_from_id
        return d


@dataclass
class DashboardUpdateRequest:
    """
    Payload for updating an existing dashboard.

    Only fields that are set (non-``None``) will be sent to the server; the rest
    are left unchanged via server-side merging.

    :param title: New display title.
    :param description: New description.
    :param alias: New alias (must be lowercase; cannot be changed on personal dashboards).
    :param tags: Replacement tag list.
    :param entitlements: Replacement entitlements.
    :param children: Full replacement list of :class:`DashboardChild` items.
    :param sections: Full replacement list of :class:`DashboardSection` items.
    :param related_links: Replacement list of :class:`RelatedLink` items.
    :param add_tags_from_children: Toggle automatic tag inheritance from widgets.
    :param is_requestable: Toggle access-request UI visibility.
    """

    title: Optional[str] = None
    description: Optional[str] = None
    alias: Optional[str] = None
    tags: Optional[List[str]] = None
    entitlements: Optional[DashboardEntitlements] = None
    children: Optional[List[DashboardChild]] = None
    sections: Optional[List[DashboardSection]] = None
    related_links: Optional[List[RelatedLink]] = None
    add_tags_from_children: Optional[bool] = None
    is_requestable: Optional[bool] = None

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {}
        if self.title is not None:
            d['title'] = self.title
        if self.description is not None:
            d['description'] = self.description
        if self.alias is not None:
            d['alias'] = self.alias.lower()
        if self.tags is not None:
            d['tags'] = self.tags
        if self.entitlements is not None:
            d['entitlements'] = self.entitlements.to_dict()
        if self.children is not None:
            d['children'] = [c.to_dict() for c in self.children]
        if self.sections is not None:
            d['sections'] = [s.to_dict() for s in self.sections]
        if self.related_links is not None:
            d['relatedLinks'] = [r.to_dict() for r in self.related_links]
        if self.add_tags_from_children is not None:
            d['addTagsFromChildren'] = self.add_tags_from_children
        if self.is_requestable is not None:
            d['isRequestable'] = self.is_requestable
        return d


# ------------------------------------------------------------------
# Section helper types
# ------------------------------------------------------------------


@dataclass
class SectionWidgetEntry:
    """
    A widget reference used when adding widgets to a section.

    :param widget_id: ID of the widget to add.
    :param configuration_id: Optional pre-existing configuration ID to associate
        with the widget slot.
    """

    widget_id: str
    configuration_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {'widgetId': self.widget_id}
        if self.configuration_id is not None:
            d['configurationId'] = self.configuration_id
        return d


@dataclass
class SectionChildrenRequest:
    """
    Payload for adding children to an existing section.

    Provide **either** ``child_ids`` **or** ``widgets`` — not both.

    :param child_ids: List of existing child IDs already on the dashboard to
        add (copy) into the section.
    :param widgets: List of :class:`SectionWidgetEntry` items describing widgets
        to add. Widgets not yet on the dashboard are auto-added.
    """

    child_ids: Optional[List[str]] = None
    widgets: Optional[List[SectionWidgetEntry]] = None

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {}
        if self.child_ids is not None:
            d['childIds'] = self.child_ids
        if self.widgets is not None:
            d['widgets'] = [w.to_dict() for w in self.widgets]
        return d


@dataclass
class SectionCopyRequest:
    """
    Payload for copying a section from one dashboard to another.

    :param source_dashboard_id: ID of the dashboard that owns the source section.
    :param source_section_id: ID of the section to copy.
    """

    source_dashboard_id: str
    source_section_id: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            'sourceDashboardId': self.source_dashboard_id,
            'sourceSectionId': self.source_section_id,
        }


@dataclass
class SectionReorderRequest:
    """
    Payload for reordering all sections within a dashboard.

    :param section_ids: Every section ID in the desired display order.
        All existing section IDs must be included exactly once.
    """

    section_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {'sectionIds': self.section_ids}
