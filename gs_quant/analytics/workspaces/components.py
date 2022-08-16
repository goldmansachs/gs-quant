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
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Optional

from pydash import unset, snake_case


class Selection:
    def __init__(self,
                 selector_id: str,
                 tag: str):
        """
        Selection option.
        :param selector_id: identifier of the selector which applies to this selection
        :param tag: tag to match in the selector. Will show up as the option in the associated selector.
        """
        self.__selector_id = selector_id
        self.__tag = tag

    @property
    def selector_id(self):
        return self.__selector_id

    @selector_id.setter
    def selector_id(self, value):
        self.__selector_id = value

    @property
    def tag(self):
        return self.__tag

    @tag.setter
    def tag(self, value):
        self.__tag = value

    def as_dict(self):
        return {
            'selectorId': self.__selector_id,
            'tag': self.__tag
        }

    @classmethod
    def from_dict(cls, obj):
        return Selection(obj['selectorId'], obj['tag'])


class LegendItem:
    def __init__(self,
                 color: str,
                 icon: str,
                 name: str,
                 tooltip: str = None):
        """
        Item in the legend component
        :param color: color of the legend item
        :param icon: icon of the legend
        :param name: name of the legend item
        :param tooltip: tooltip to display on the the name
        """
        self.color = color
        self.icon = icon
        self.name = name
        self.tooltip = tooltip

    def as_dict(self):
        dict_ = {
            'color': self.color,
            'icon': self.icon,
            'name': self.name
        }
        if self.tooltip:
            dict_['tooltip'] = self.tooltip
        return dict_

    @classmethod
    def from_dict(cls, obj):
        return LegendItem(color=obj['color'], icon=obj['icon'], name=obj['name'], tooltip=obj.get('tooltip'))


class RelatedLinkType(Enum):
    anchor = 'anchor'
    internal = 'internal'
    external = 'external'
    mail = 'mail'
    notification = 'notification'


class RelatedLink:
    def __init__(self,
                 type_: RelatedLinkType,
                 name: str,
                 link: str,
                 description: str = None):
        """
        Related Link Item
        :param type_: Type of the Related Link
        :param name: Name that appears on the related links
        :param link: link to navigate when the item is clicked
        :param description: description of the link
        """
        self.type_ = type_
        self.name = name
        self.link = link
        self.description = description
        # TODO: self.notification_properties

    def as_dict(self):
        dict_ = {
            'type': self.type_.value,
            'name': self.name,
            'link': self.link
        }
        if self.description:
            dict_['description'] = self.description
        return dict_

    @classmethod
    def from_dict(cls, obj):
        return RelatedLink(type_=RelatedLinkType(obj['type']), name=obj['name'], link=obj['link'],
                           description=obj.get('description'))


class PromoSize(Enum):
    DEFAULT = 'default'
    LARGE = 'large'


class Component(ABC):
    def __init__(self,
                 height: Optional[int] = None,
                 id_: Optional[str] = None,
                 *,
                 width: int = None,
                 selections: List[Selection] = None,
                 container_ids: List[str] = None):
        self.__id = id_ or f'{self.__class__.__name__}-{str(uuid.uuid4())[0:5]}'
        self._height = height
        self.__width = width
        self.__selections = selections
        self.__container_ids = container_ids
        self._type = None

    @property
    def id_(self):
        return self.__id

    @id_.setter
    def id_(self, value):
        self.__id = value or f'{self.__class__.__name__}-{str(uuid.uuid4())[0:5]}'

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, value):
        self.__width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def selections(self):
        return self.__selections

    @selections.setter
    def selections(self, value):
        self.__selections = value

    @property
    def container_ids(self):
        return self.__container_ids

    @container_ids.setter
    def container_ids(self, value):
        self.__container_ids = value

    @abstractmethod
    def as_dict(self) -> Dict:
        dict_ = {
            'id': self.__id,
            'type': self._type,
            'parameters': {
                'height': self._height or 200
            }
        }
        if self.__selections:
            dict_['selections'] = [selection.as_dict() for selection in self.__selections]
        if self.__container_ids:
            dict_['containerIds'] = [containerId for containerId in self.__container_ids]

        return dict_

    @classmethod
    def from_dict(cls, obj, scale: int = None):
        parameters = obj.get('parameters', {})
        height = parameters.get('height', 200)
        unset(parameters, 'height')
        unset(parameters, 'width')
        component = TYPE_TO_COMPONENT[obj['type']](id_=obj['id'], height=height, width=scale,
                                                   **{snake_case(k): v for k, v in parameters.items()})
        selections, container_ids, tags = obj.get('selections'), obj.get('containerIds'), obj.get('tags')
        if selections:
            component.selections = [Selection.from_dict(selection) for selection in selections]
        if container_ids:
            component.__container_ids = [containerId for containerId in container_ids]
        if tags:
            component.tags = tags
        return component


class PlotComponent(Component):
    def __init__(self,
                 height: int,
                 id_: str,
                 *,
                 width: int = None,
                 selections: List[Selection] = None,
                 tooltip: str = None,
                 hide_legend: bool = False):
        """
        Plot Component
        :param id_: identifier of the plot
        :param height: height of the component
        :param width: width of the component integers 1-12
        :param selections: List of selections used for selectors
        :param tooltip: text to show in a tooltip on the chart name
        :param hide_legend: whether to hide the series legend under the plot
        """
        super().__init__(id_=id_, height=height, width=width, selections=selections)
        self._type = 'plot'
        self.tooltip = tooltip
        self.hide_legend = hide_legend

    def as_dict(self) -> Dict:
        dict_ = super().as_dict()
        dict_['parameters']['hideLegend'] = self.hide_legend
        if self.tooltip:
            dict_['parameters']['tooltip'] = self.tooltip
        return dict_


class DataVizComponent(Component):
    def __init__(self,
                 height: int,
                 id_: str,
                 *,
                 width: int = None):
        """
        Data Visualization Component
        :param id_: identifier of the Visualization
        :param height: height of the componentTYPE_TO_COMPONENT
        :param width: width of the component integers 1-12
        """
        super().__init__(id_=id_, height=height, width=width)
        self._type = 'dataviz'

    def as_dict(self) -> Dict:
        return super().as_dict()


class DataGridComponent(Component):
    def __init__(self,
                 height: int,
                 id_: str,
                 *,
                 width: int = None,
                 selections: List[Selection] = None,
                 tooltip: str = None):
        """
        DataGrid Component
        :param height: height of the component
        :param id_: unique identifier of the DataGrid
        :param width: width of the component integers 1-12
        :param selections: List of selections used for selectors
        :param tooltip: text to show in a tooltip on the DataGrid name
        """
        super().__init__(id_=id_, height=height, width=width, selections=selections)
        self._type = 'datagrid'
        self.tooltip = tooltip

    def as_dict(self) -> Dict:
        dict_ = super().as_dict()
        if self.tooltip:
            dict_['parameters']['tooltip'] = self.tooltip

        return dict_


class DataScreenerComponent(Component):
    def __init__(self,
                 height: int,
                 id_: str,
                 *,
                 width: int = None,
                 tooltip: str = None):
        """
        Data Screener Component
        :param height: height of the component
        :param id_: unique identifier of the Data Screener
        :param width: width of the component integers 1-12
        :param tooltip: text to show in a tooltip on the Data Screener name
        """
        super().__init__(id_=id_, height=height, width=width)
        self._type = 'screener'
        self.tooltip = tooltip

    def as_dict(self) -> Dict:
        dict_ = super().as_dict()
        if self.tooltip:
            dict_['parameters']['tooltip'] = self.tooltip

        return dict_


class ArticleComponent(Component):
    def __init__(self,
                 height: int,
                 id_: Optional[str] = None,
                 *,
                 width: int = None,
                 selections: List[Selection] = None,
                 tooltip: str = None,
                 commentary_channels: List[str] = None,
                 commentary_to_desktop_link: bool = None):
        """
        Article Component
        :param height: height of the component
        :param id_: unique identifier of the component
        :param width: width of the component integers 1-12
        :param selections: List of selections used for selectors
        :param tooltip: text to show in a tooltip on the article component name
        :param commentary_channels: List of commentary channels that provides data
        :param commentary_to_desktop_link: Whether or not to display a link from commentary to desktop in the header
        """
        super().__init__(id_=id_, height=height, width=width, selections=selections)
        self._type = 'article'
        self.tooltip = tooltip
        self.commentary_channels = commentary_channels
        self.commentary_to_desktop_link = commentary_to_desktop_link

    def as_dict(self) -> Dict:
        dict_ = super().as_dict()
        if self.tooltip:
            dict_['parameters']['tooltip'] = self.tooltip
        if self.commentary_channels:
            dict_['parameters']['commentaryChannels'] = self.commentary_channels
        if self.commentary_to_desktop_link:
            dict_['parameters']['commentaryToDesktopLink'] = self.commentary_to_desktop_link

        return dict_


class CommentaryComponent(Component):
    def __init__(self,
                 height: int,
                 id_: Optional[str] = None,
                 *,
                 width: int = None,
                 selections: List[Selection] = None,
                 tooltip: str = None,
                 commentary_channels: List[str] = None,
                 commentary_to_desktop_link: bool = None):
        """
        Commentary Component
        :param height: height of the component
        :param id_: unique identifier of the component
        :param width: width of the component integers 1-12
        :param selections: List of selections used for selectors
        :param tooltip: text to show in a tooltip on the article component name
        :param commentary_channels: List of commentary channels that provides data
        :param commentary_to_desktop_link: Whether or not to display a link from commentary to desktop in the header
        """
        super().__init__(id_=id_, height=height, width=width, selections=selections)
        self._type = 'plot'
        self.tooltip = tooltip
        self.commentary_channels = commentary_channels
        self.commentary_to_desktop_link = commentary_to_desktop_link

    def as_dict(self) -> Dict:
        dict_ = super().as_dict()
        if self.tooltip:
            dict_['parameters']['tooltip'] = self.tooltip
        if self.commentary_channels:
            dict_['parameters']['commentaryChannels'] = self.commentary_channels
        if self.commentary_to_desktop_link:
            dict_['parameters']['commentaryToDesktopLink'] = self.commentary_to_desktop_link

        return dict_


class ContainerComponent(Component):
    def __init__(self,
                 id_: Optional[str] = None,
                 *,
                 width: int = None,
                 component_id: str = None):
        """
        Container Component which acts as a placeholder for components used with selectors
        :param id_: unique identifier of the component
        :param width: width of the component integers 1-12
        :param component_id: default component id to use in the container
        """
        super().__init__(id_=id_, width=width, selections=None)
        self._type = 'container'
        self.component_id = component_id

    def as_dict(self) -> Dict:
        dict_ = super().as_dict()
        if self.component_id:
            dict_['parameters']['componentId'] = self.component_id
        del dict_['parameters']['height']
        return dict_


class SelectorComponent(Component):
    def __init__(self,
                 height: int,
                 id_: Optional[str] = None,
                 *,
                 container_ids: List[str],
                 width: int = None,
                 title: str = None,
                 default_option_index: int = None,
                 tooltip: str = None,
                 parent_selector_id: str = None):
        """
        Selector Component to conditionally pick components based on their selection tags.
        :param height: height of the component
        :param id_: unique identifier of the component
        :param container_ids: Name of containers affected by the selector
        :param width: width of the component integers 1-12
        :param title: Text to show next to selector dropdown
        :param default_option_index: default index of the dropdown
        :param tooltip: text to show in tooltip on the title
        :param parent_selector_id: unique identifier of the parent selector component for nested selections
        """
        super().__init__(id_=id_, height=height, width=width, selections=None)
        self._type = 'selector'
        self.container_ids = container_ids
        self.title = title
        self.default_option_index = default_option_index
        self.tooltip = tooltip
        self.parent_selector_id = parent_selector_id

    def as_dict(self) -> Dict:
        dict_ = super().as_dict()
        dict_['parameters']['containerIds'] = self.container_ids

        if self.default_option_index:
            dict_['parameters']['defaultOptionIndex'] = self.default_option_index

        if self.title:
            dict_['parameters']['title'] = self.title

        if self.tooltip:
            dict_['parameters']['tooltip'] = self.tooltip

        if self.parent_selector_id:
            dict_['parameters']['parentSelectorId'] = self.parent_selector_id

        return dict_

    @classmethod
    def from_dict(cls, obj, scale: int = None):
        parameters = obj.get('parameters', {})

        return SelectorComponent(id_=obj['id'], height=parameters.get('height', 200), width=scale,
                                 title=parameters.get('title'),
                                 container_ids=parameters['containerIds'], tooltip=parameters.get('tooltip'),
                                 default_option_index=parameters.get('defaultOptionIndex'),
                                 parent_selector_id=parameters.get('parentSelectorId'))


class PromoComponent(Component):
    def __init__(self,
                 height: int,
                 id_: Optional[str] = None,
                 *,
                 width: int = None,
                 selections: List[Selection] = None,
                 tooltip: str = None,
                 transparent: bool = None,
                 body: str = None,
                 size: PromoSize = None,
                 hide_border: bool = None):
        """
        Promo Component for arbitrary text
        :param height: height of the component
        :param id_: unique identifier of the component
        :param width: width of the component integers 1-12
        :param selections: List of selections used for selectors
        :param tooltip: text to show in tooltip on the title
        :param transparent: whether or not the background of the component is transparent
        :param body: text to show in the component that can have html tags
        :param size: size of the component text
        :param hide_border: whether to hide the border of the component
        """
        super().__init__(id_=id_, height=height, width=width, selections=selections)
        self._type = 'promo'
        self.tooltip = tooltip
        self.transparent = transparent
        self.body = body
        self.size = size
        self.hide_border = hide_border

    def as_dict(self) -> Dict:
        dict_ = super().as_dict()
        if self.tooltip:
            dict_['parameters']['tooltip'] = self.tooltip
        if self.body:
            dict_['parameters']['body'] = self.body
        if self.size:
            dict_['parameters']['size'] = self.size.value
        if self.hide_border is not None:
            dict_['parameters']['hideBorder'] = self.size
        if self.transparent is not None:
            dict_['parameters']['transparent'] = self.transparent

        return dict_

    @classmethod
    def from_dict(cls, obj: Dict, scale: int = None):
        parameters = obj.get('parameters', {})
        size = parameters.get('size')
        size = PromoSize(size) if size else None
        return PromoComponent(id_=obj['id'], height=parameters.get('height', 200), width=scale,
                              tooltip=parameters.get('tooltip'), body=parameters.get('body'), size=size,
                              hide_border=parameters.get('hideBorder'))


class SeparatorComponent(Component):
    def __init__(self,
                 height: int,
                 id_: Optional[str] = None,
                 *,
                 width: int = None,
                 selections: List[Selection] = None,
                 name: str = None,
                 size: str = None,
                 show_more_url: str = None):
        """
        Separator Component
        :param height: height of the component
        :param id_: unique identifier of the component
        :param width: width of the component integers 1-12
        :param selections: List of selections used for selectors
        :param name: Text of the separator
        :param size: size of the component
        :param show_more_url: Url link to redirect
        """
        super().__init__(id_=id_, height=height, width=width, selections=selections)
        self._type = 'separator'
        self.name = name
        self.size = size
        self.show_more_url = show_more_url

    def as_dict(self) -> Dict:
        dict_ = super().as_dict()
        if self.name:
            dict_['parameters']['name'] = self.name
        if self.size:
            dict_['parameters']['size'] = self.size
        if self.show_more_url:
            dict_['parameters']['showMoreUrl'] = self.show_more_url

        return dict_


class LegendComponent(Component):
    def __init__(self,
                 height: int,
                 id_: Optional[str] = None,
                 *,
                 width: int = None,
                 selections: List[Selection] = None,
                 items: List[LegendItem] = None,
                 position: str = None,
                 transparent: bool = None):
        """
        Legend Component
        :param height: height of the component
        :param id_: unique identifier of the component
        :param width: width of the component integers 1-12
        :param selections: List of selections used for selectors
        :param items: Legend items to appear in the legend
        :param position: position of the legend
        :param transparent: Whether the background of the legend is transparent
        """
        super().__init__(id_=id_, height=height, width=width, selections=selections)
        self._type = 'legend'
        self.items = items
        self.position = position
        self.transparent = transparent

    def as_dict(self) -> Dict:
        dict_ = super().as_dict()
        dict_['parameters']['items'] = [item.as_dict() for item in self.items]
        if self.position:
            dict_['parameters']['position'] = self.position
        if self.transparent:
            dict_['parameters']['transparent'] = self.transparent

        return dict_

    @classmethod
    def from_dict(cls, obj: Dict, scale: int = None):
        parameters = obj.get('parameters', {})
        items = [LegendItem.from_dict(item) for item in parameters.get('items', [])]

        return LegendComponent(id_=obj['id'], height=parameters.get('height', 200), width=scale,
                               selections=obj.get('selections'), position=parameters.get('position'),
                               transparent=parameters.get('transparent'), items=items)


class MonitorComponent(Component):
    def __init__(self,
                 height: int,
                 id_: str,
                 *,
                 width: int = None,
                 selections: List[Selection] = None,
                 tooltip: str = None):
        """
        Monitor Component
        :param height: height of the component
        :param id_: unique identifier of the component
        :param width: width of the component integers 1-12
        :param selections: List of selections used for selectors
        :param tooltip: text to show in a tooltip when hovering over monitor name
        """
        super().__init__(id_=id_, height=height, width=width, selections=selections)
        self._type = 'monitor'
        self.tooltip = tooltip

    def as_dict(self) -> Dict:
        dict_ = super().as_dict()
        if self.tooltip:
            dict_['parameters']['tooltip'] = self.tooltip

        return dict_


class RelatedLinksComponent(Component):
    def __init__(self,
                 height: int,
                 id_: Optional[str] = None,
                 *,
                 width: int = None,
                 selections: List[Selection] = None,
                 links: List[RelatedLink],
                 title: str):
        """
        Related Links Component
        :param height: height of the component
        :param id_: unique identifier of the component
        :param width: width of the component integers 1-12
        :param selections: List of selections used for selectors
        :param links: links to add to the component
        :param title: title of the component
        """
        super().__init__(id_=id_, height=height, width=width, selections=selections)
        self._type = 'relatedLinks'
        self.links = links
        self.title = title

    def as_dict(self) -> Dict:
        dict_ = super().as_dict()
        dict_['parameters']['title'] = self.title
        dict_['parameters']['links'] = [link.as_dict() for link in self.links]
        return dict_

    @classmethod
    def from_dict(cls, obj, scale: int = None):
        parameters = obj.get('parameters', {})
        return RelatedLinksComponent(id_=obj['id'], height=parameters.get('height', 200), width=scale,
                                     selections=obj.get('selections'), title=parameters['title'],
                                     links=[RelatedLink.from_dict(link) for link in parameters['links']])


TYPE_TO_COMPONENT = {
    'article': ArticleComponent,
    'container': ContainerComponent,
    'datagrid': DataGridComponent,
    'dataviz': DataVizComponent,
    'legend': LegendComponent,
    'monitor': MonitorComponent,
    'plot': PlotComponent,
    'promo': PromoComponent,
    'relatedLinks': RelatedLinksComponent,
    'selector': SelectorComponent,
    'separator': SeparatorComponent,
    'screener': DataScreenerComponent
}
