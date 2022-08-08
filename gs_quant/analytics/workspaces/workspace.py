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
import webbrowser
from collections import deque
from typing import List, Tuple, Union, Dict

from pydash import get

from gs_quant.analytics.workspaces.components import Component, TYPE_TO_COMPONENT, RelatedLink, DataGridComponent, \
    MonitorComponent, PlotComponent, DataScreenerComponent
from gs_quant.entities.entitlements import Entitlements
from gs_quant.errors import MqValueError, MqRequestError
from gs_quant.session import GsSession
from gs_quant.target.common import Entitlements as Entitlements_

_logger = logging.getLogger(__name__)

API = '/workspaces/markets'
HEADERS = {'Content-Type': 'application/json;charset=utf-8'}


class WorkspaceCallToAction:

    def __init__(
            self,
            actions: List[RelatedLink],
            text: str,
            name: str = None):
        """
        Call to action displayed on the top right of the page.
        :param actions: link to external/internal pages, embed a mail to link, anchor links within page or notifications
        :param text: description below the link
        :param name: name of the link/button
        """
        self.actions = actions
        self.text = text
        self.name = name

    def as_dict(self):
        actions = []
        for action in self.actions:
            if isinstance(action, RelatedLink):
                actions.append(action.as_dict())
            else:
                actions.append(action)
        cta_dict = {'actions': actions, 'text': self.text}
        if self.name:
            cta_dict['name'] = self.name
        return cta_dict

    @classmethod
    def from_dict(cls, obj):
        actions = []
        for action in obj['actions']:
            if isinstance(action, Dict):
                actions.append(RelatedLink.from_dict(action))
            else:
                actions.append(action)
        return WorkspaceCallToAction(actions=actions, text=obj['text'], name=obj['name'])


class WorkspaceTab:
    def __init__(self,
                 id_: str,
                 name: str):
        """
        Workspace Tab to connect other workspaces.
        :param id_: alias of the workspace to create a tab
        :param name: Name of the tab
        """
        self.id_ = id_
        self.name = name

    def as_dict(self):
        return {
            'id': self.id_,
            'name': self.name
        }

    @classmethod
    def from_dict(cls, obj):
        return WorkspaceTab(id_=obj['id'], name=obj['name'])


class WorkspaceColumn:
    def __init__(self,
                 components: List[Union[Component, 'WorkspaceRow']],
                 width: int = None):
        """
        :param components: List of components in the same row
        """
        self.__components = []
        self.components = components
        self.__width = width

    @property
    def components(self):
        return self.__components

    @components.setter
    def components(self, value):
        if len(value) > 12:
            raise MqValueError(f'{value} exceeds the max number of columns of 12.')
        width_sum = 0
        for component in self.__components:
            if not isinstance(component, WorkspaceRow):
                width_sum += component.width
        if width_sum > 12:
            raise MqValueError(f'{width_sum} exceeds the max sum of widths of 12.')

        without_width_count = 0
        for component in value:
            if not isinstance(component, WorkspaceRow):
                without_width_count += component.width or 1
        if width_sum + without_width_count > 12:
            raise MqValueError(
                f'Cannot fit all components in column due to given total width of {width_sum} '
                f'and {without_width_count} components without a width.')
        self.__components = value

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, value):
        self.__width = value

    def get_layout(self, count):
        layout = ''
        width_sum = 0
        for component in self.__components:
            if not isinstance(component, WorkspaceRow):
                width_sum += component.width or 0
        components_length = len(self.__components)
        if width_sum == 0:
            # Equally spread out
            size = int(12 / components_length)
            last_size = 12 % components_length
            for i, component in enumerate(self.__components):
                if isinstance(component, WorkspaceRow):
                    sub_layout, count = component.get_layout(count)
                    layout += sub_layout
                elif isinstance(component, WorkspaceColumn):
                    sub_layout, count = component.get_layout(count)
                    layout += f'c{size + last_size if i == components_length - 1 and last_size != 0 else size}' \
                              f'({sub_layout})'
                else:
                    # Case: Component
                    layout += f'c{size + last_size if i == components_length - 1 and last_size != 0 else size}' \
                              f'(${count})'
                    count += 1
        else:
            used_sum = 0
            if width_sum == 12:
                default_width = 0
            else:
                default_width = int(12 - width_sum / sum(1 for component in self.components if component.width is None))
            for i, component in enumerate(self.components):
                if i == components_length - 1 and not component.width:
                    layout += f'c{12 - used_sum}(${count})'
                elif component.width is None:
                    layout += f'c{default_width}(${count})'
                    used_sum += default_width
                else:
                    width = component.width or 1
                    layout += f'c{width}(${count})'
                    used_sum += width
                count += 1

        return layout, count

    def _add_components(self, components):
        for component in self.__components:
            if isinstance(component, (WorkspaceRow, WorkspaceColumn)):
                component._add_components(components)
            else:
                components.append(component.as_dict())


class WorkspaceRow:
    """
    Wrapper on a list of components in the same row.
    """

    def __init__(self,
                 components: List[Union[Component, WorkspaceColumn]]):
        """
        :param components: List of components in the same row
        """
        self.__components = []
        self.components = components

    @property
    def components(self):
        return self.__components

    @components.setter
    def components(self, value):
        if len(value) > 12:
            raise MqValueError(f'{value} exceeds the max number of columns of 12.')
        width_sum = 0
        for component in self.__components:
            if not isinstance(component, WorkspaceRow):
                width_sum += component.width
        if width_sum > 12:
            raise MqValueError(f'{width_sum} exceeds the max sum of widths of 12.')

        without_width_count = 0
        for component in value:
            if not isinstance(component, WorkspaceRow):
                without_width_count += component.width or 1
        if width_sum + without_width_count > 12:
            raise MqValueError(
                f'Cannot fit all components in row due to given total width of {width_sum} '
                f'and {without_width_count} components without a width.')
        self.__components = value

    def get_layout(self, count: int) -> Tuple[str, int]:
        layout = 'r('
        width_sum = 0
        for component in self.__components:
            if not isinstance(component, WorkspaceRow):
                width_sum += component.width or 0
        components_length = len(self.__components)
        if width_sum == 0:
            # Equally spread out
            size = int(12 / components_length)
            last_size = 12 % components_length
            for i, component in enumerate(self.__components):
                if isinstance(component, WorkspaceColumn):
                    sub_layout, count = component.get_layout(count)
                    layout += f'c{size + last_size if i == components_length - 1 and last_size != 0 else size}' \
                              f'({sub_layout})'
                else:
                    # Case: Component
                    layout += f'c{size + last_size if i == components_length - 1 and last_size != 0 else size}' \
                              f'(${count})'
                    count += 1
        else:
            used_sum = 0
            if width_sum == 12:
                default_width = 0
            else:
                default_width = self.components[0].width if len(self.components) == 1 else \
                    int(12 - width_sum / sum(1 for component in self.components if component.width is None))
            for i, component in enumerate(self.components):
                if i == components_length - 1 and not component.width:
                    if isinstance(component, WorkspaceColumn):
                        sub_layout, count = component.get_layout(count)
                        layout += f'c{12 - used_sum}({sub_layout})'
                    else:
                        layout += f'c{12 - used_sum}(${count})'
                        count += 1
                elif component.width is None:
                    if isinstance(component, WorkspaceColumn):
                        sub_layout, count = component.get_layout(count)
                        layout += f'c{default_width}({sub_layout})'
                    else:
                        layout += f'c{default_width}(${count})'
                        count += 1
                    used_sum += default_width
                else:
                    width = component.width or 1
                    if isinstance(component, WorkspaceColumn):
                        sub_layout, count = component.get_layout(count)
                        layout += f'c{width}({sub_layout})'
                    else:
                        layout += f'c{width}(${count})'
                        count += 1
                    used_sum += width

        layout += ')'
        return layout, count

    def _add_components(self, components):
        for component in self.__components:
            if isinstance(component, (WorkspaceRow, WorkspaceColumn)):
                component._add_components(components)
            else:
                components.append(component.as_dict())


class Workspace:
    PERSISTED_COMPONENTS = {
        DataGridComponent: '/data/grids',
        MonitorComponent: '/monitors',
        PlotComponent: '/charts',
        DataScreenerComponent: '/data/screens',
    }

    def __init__(self,
                 name: str,
                 rows: List[WorkspaceRow] = None,
                 alias: str = None,
                 description: str = None,
                 entitlements: Union[Entitlements, Entitlements_] = None,
                 tabs: List[WorkspaceTab] = None,
                 selector_components: List[Component] = None,
                 disclaimer: str = None,
                 maintainers: List[str] = None,
                 call_to_action: Union[WorkspaceCallToAction, Dict] = None,
                 tags: List[str] = None):
        self.__id = None
        self.__name = name
        self.__rows = rows or []
        self.__selector_components = selector_components or []
        self.__alias = alias
        self.__entitlements = entitlements
        self.__description = description
        self.__disclaimer = disclaimer
        self.__maintainers = maintainers or []
        self.__tabs = tabs or []
        self.__call_to_action = call_to_action
        self.__tags = tags or []

    @classmethod
    def get_by_id(cls, workspace_id: str) -> 'Workspace':
        resp = GsSession.current._get(f'{API}/{workspace_id}')
        return Workspace.from_dict(resp)

    @classmethod
    def get_by_alias(cls, alias: str) -> 'Workspace':
        resp = get(GsSession.current._get(f'{API}?alias={alias}'), 'results.0')
        if not resp:
            raise MqValueError(f'Workspace not found with alias {alias}')
        return Workspace.from_dict(resp)

    def save(self):
        if self.__id:
            GsSession.current._put(f'{API}/{self.__id}', self.as_dict(), request_headers=HEADERS)
        elif self.__alias:
            id_ = get(GsSession.current._get(f'{API}?alias={self.__alias}'), 'results.0.id')
            if id_:
                self.__id = GsSession.current._put(f'{API}/{id_}', self.as_dict(), request_headers=HEADERS)['id']
            else:
                self.__id = GsSession.current._post(API, self.as_dict(), request_headers=HEADERS)['id']

    def open(self):
        if self.__id is None:
            raise MqValueError('Workspace must be created or saved before opening.')

        domain = GsSession.current.domain.replace(".web", "")
        if domain == 'https://api.gs.com':
            domain = 'https://marquee.gs.com'
        url = f'{domain}/s/markets/{self.__alias or self.__id}'
        webbrowser.open(url)

    def create(self):
        resp = GsSession.current._post(f'{API}', self.as_dict(), request_headers=HEADERS)
        self.__id = resp['id']

    def delete(self):
        if self.__id is None:
            raise MqValueError('Workspace must have an id to be deleted.')
        resp = GsSession.current._delete(f'{API}/{self.__id}')
        self.__id = resp['id']

    def delete_all(self, include_tabs: bool = False):
        """
        Deletes the workspace and all persisted components.
        :param include_tabs: whether to delete all tabs and their persisted components also
        :return: None
        """
        for row in self.__rows:
            self.__delete_components(row.components)
        self.__delete_components(self.__selector_components)
        if include_tabs:
            for tab in self.__tabs:
                tab_workspace = self.get_by_alias(tab.id_)
                tab_workspace.delete_all()

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def alias(self):
        return self.__alias

    @alias.setter
    def alias(self, value):
        self.__alias = value

    @property
    def rows(self) -> List[WorkspaceRow]:
        return self.__rows

    @rows.setter
    def rows(self, value: List[WorkspaceRow]):
        self.__rows = value

    @property
    def entitlements(self):
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value):
        self.__entitlements = value

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        self.__description = value

    @property
    def disclaimer(self):
        return self.__disclaimer

    @disclaimer.setter
    def disclaimer(self, value):
        self.__disclaimer = value

    @property
    def maintainers(self):
        return self.__maintainers

    @maintainers.setter
    def maintainers(self, value):
        self.__maintainers = value

    @property
    def tabs(self):
        return self.__tabs

    @tabs.setter
    def tabs(self, value):
        self.__tabs = value

    @property
    def selector_components(self):
        return self.__selector_components

    @selector_components.setter
    def selector_components(self, value):
        self.__selector_components = value

    @property
    def call_to_action(self):
        return self.__call_to_action

    @call_to_action.setter
    def call_to_action(self, value):
        self.__call_to_action = value

    @property
    def tags(self):
        return self.__tags

    @tags.setter
    def tags(self, value):
        self.__tags = value

    @property
    def id(self):
        return self.__id

    @classmethod
    def _parse(cls, layout: str, workspace_components: List[Dict]):
        current_str = ''
        outside_components = []
        stack = deque()
        for c in layout:
            current_str += c
            if c == '(':
                stack.append('(')
            elif c == ')':
                stack.pop()
                if len(stack) == 0:
                    if current_str.startswith('c'):
                        is_component = current_str[current_str.index('(') + 1:].startswith('$')
                        if is_component:
                            # Component Case
                            scale, id_ = current_str.split('($')
                            scale = int(scale[1:])
                            id_ = int(id_[0:-1])
                            component = workspace_components[id_]
                            component_type = component['type']
                            component = TYPE_TO_COMPONENT[component_type].from_dict(component, scale)
                            outside_components.append(component)
                        else:
                            # Column Case
                            column_layout = current_str[current_str.index('(') + 1:-1]
                            components = Workspace._parse(column_layout, workspace_components)
                            width = int(current_str[1:current_str.index('(')])
                            outside_components.append(WorkspaceColumn(components, width))
                    elif current_str.startswith('r'):
                        # Row Case
                        row_layout = current_str[current_str.index('(') + 1:-1]
                        components = Workspace._parse(row_layout, workspace_components)
                        outside_components.append(WorkspaceRow(components))
                    current_str = ''

        return outside_components

    @classmethod
    def from_dict(cls, obj):
        workspace_components = obj['parameters']['components']
        layout = obj['parameters']['layout']
        stack = deque()
        row_layout = ''
        row_layouts = []
        for c in layout[1:]:
            if c == '(':
                stack.append('(')
            elif c == ')':
                stack.pop()
                if len(stack) == 0:
                    row_layouts.append(row_layout[row_layout.index('c'):])
                    row_layout = ''
            row_layout += c

        workspace_rows = [WorkspaceRow(components=Workspace._parse(row_layout, workspace_components))
                          for row_layout in row_layouts]

        component_count = 0
        # The rest of the components not in the layout should be selector components
        selector_components = []
        if component_count < len(workspace_components):
            for i in range(component_count, len(workspace_components)):
                component = workspace_components[i]
                selector_components.append(TYPE_TO_COMPONENT[component['type']].from_dict(component))

        params = obj['parameters']
        tabs = [WorkspaceTab.from_dict(tab) for tab in params.get('tabs', [])]
        return Workspace(name=obj['name'], rows=workspace_rows, selector_components=selector_components,
                         alias=obj.get('alias'), tabs=tabs,
                         entitlements=Entitlements.from_dict(obj.get('entitlements', {})),
                         description=obj.get('description'),
                         disclaimer=params.get('disclaimer'), maintainers=params.get('maintainers'))

    def as_dict(self):
        components, count, layout = [], 0, ''
        for row in self.__rows:
            row_layout, count = row.get_layout(count)
            layout += row_layout
            for component in row.components:
                if isinstance(component, (WorkspaceRow, WorkspaceColumn)):
                    component._add_components(components)
                else:
                    components.append(component.as_dict())

        # Add the hidden components at the end
        components.extend([component.as_dict() for component in self.__selector_components])

        parameters = {
            'layout': layout,
            'components': components
        }

        if len(self.__maintainers):
            parameters['maintainers'] = self.__maintainers
        if self.__call_to_action:
            if isinstance(self.__call_to_action, WorkspaceCallToAction):
                parameters['callToAction'] = self.__call_to_action.as_dict()
            else:
                parameters['callToAction'] = self.__call_to_action
        if len(self.__tabs):
            parameters['tabs'] = [tab.as_dict() for tab in self.__tabs]
        if self.__disclaimer:
            parameters['disclaimer'] = self.__disclaimer

        dict_ = {
            'name': self.__name,
            'parameters': parameters
        }

        if self.__alias:
            dict_['alias'] = self.__alias
        if self.__entitlements:
            if isinstance(self.__entitlements, Entitlements_):
                dict_['entitlements'] = self.__entitlements.as_dict()
            elif isinstance(self.__entitlements, Entitlements):
                dict_['entitlements'] = self.__entitlements.to_dict()
            else:
                dict_['entitlements'] = self.__entitlements
        if len(self.__tags):
            dict_['tags'] = self.__tags
        if self.__description:
            dict_['description'] = self.__description

        return dict_

    @classmethod
    def __delete_components(cls, components: List[Component]):
        for component in components:
            if isinstance(component, (WorkspaceRow, WorkspaceColumn)):
                cls.__delete_components(component.components)
            else:
                type_ = type(component)
                if type_ in cls.PERSISTED_COMPONENTS:
                    try:
                        GsSession.current._delete(f'{cls.PERSISTED_COMPONENTS[type_]}/{component.id_}')
                    except MqRequestError as ex:
                        _logger.warning(
                            f'Failed to delete {type_.__name__} with id {component.id_} due to {ex.message}')


def __get_layout(components, count):
    layout = 'r('
    width_sum = 0
    for component in components:
        if not isinstance(component, WorkspaceRow):
            width_sum += component.width or 0
    components_length = len(components)
    if width_sum == 0:
        # Equally spread out
        size = int(12 / components_length)
        last_size = 12 % components_length
        for i, component in enumerate(components):
            if isinstance(component, WorkspaceRow):
                sub_layout, count = __get_layout(component.components, count)
                layout += f'c{size + last_size if i == components_length - 1 and last_size != 0 else size}' \
                          f'({sub_layout})'
            elif isinstance(component, WorkspaceColumn):
                sub_layout, count = __get_layout(component.components, count)
                layout += f'c{size + last_size if i == components_length - 1 and last_size != 0 else size}' \
                          f'({sub_layout})'
            else:
                # Case: Component
                layout += f'c{size + last_size if i == components_length - 1 and last_size != 0 else size}(${count})'
                count += 1
    else:
        used_sum = 0
        if width_sum == 12:
            default_width = 0
        else:
            default_width = int(12 - width_sum / sum(1 for component in components if component.width is None))
        for i, component in enumerate(components):
            if i == components_length - 1 and not component.width:
                layout += f'c{12 - used_sum}(${count})'
            elif component.width is None:
                layout += f'c{default_width}(${count})'
                used_sum += default_width
            else:
                width = component.width or 1
                layout += f'c{width}(${count})'
                used_sum += width
            count += 1

    layout += ')'
    return layout, count
