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

from gs_quant.target.common import *
import datetime
from typing import Tuple, Union
from enum import Enum
from gs_quant.base import Base, EnumBase, InstrumentBase, camel_case_translate, get_enum_value


class ComponentType(EnumBase, Enum):    
    
    """Enum listing supported component types"""

    article = 'article'
    assetPlot = 'assetPlot'
    chart = 'chart'
    barChart = 'barChart'
    commentary = 'commentary'
    commentaryPromo = 'commentaryPromo'
    container = 'container'
    legend = 'legend'
    market = 'market'
    monitor = 'monitor'
    plot = 'plot'
    promo = 'promo'
    rates = 'rates'
    relatedLinks = 'relatedLinks'
    research = 'research'
    selector = 'selector'
    separator = 'separator'
    stackedBarChart = 'stackedBarChart'
    
    def __repr__(self):
        return self.value


class WorkspaceType(EnumBase, Enum):    
    
    """Enum listing support workspace types"""

    cashboard = 'cashboard'
    multiplot = 'multiplot'
    
    def __repr__(self):
        return self.value


class ArticleComponentParameters(Base):
        
    """Parameters provided for a article component"""

    @camel_case_translate
    def __init__(
        self,
        height: float,
        tooltip: str = None,
        commentary_channels: Tuple[str, ...] = None,
        commentary_to_desktop_link: bool = None,
        name: str = None
    ):        
        super().__init__()
        self.height = height
        self.tooltip = tooltip
        self.commentary_channels = commentary_channels
        self.commentary_to_desktop_link = commentary_to_desktop_link
        self.name = name

    @property
    def height(self) -> float:
        """Used for restricting the height in pixels of the component on a workspace"""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def tooltip(self) -> str:
        """Tooltip that is displayed in an info icon next to the component title."""
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self._property_changed('tooltip')
        self.__tooltip = value        

    @property
    def commentary_channels(self) -> Tuple[str, ...]:
        """Optional channels associated with a commentary component"""
        return self.__commentary_channels

    @commentary_channels.setter
    def commentary_channels(self, value: Tuple[str, ...]):
        self._property_changed('commentary_channels')
        self.__commentary_channels = value        

    @property
    def commentary_to_desktop_link(self) -> bool:
        """Whether or not to display a link from commentary to desktop in the header"""
        return self.__commentary_to_desktop_link

    @commentary_to_desktop_link.setter
    def commentary_to_desktop_link(self, value: bool):
        self._property_changed('commentary_to_desktop_link')
        self.__commentary_to_desktop_link = value        


class AssetPlotComponentParameters(Base):
        
    """Parameters provided for a asset plot component"""

    @camel_case_translate
    def __init__(
        self,
        height: float,
        tooltip: str = None,
        name: str = None
    ):        
        super().__init__()
        self.height = height
        self.tooltip = tooltip
        self.name = name

    @property
    def height(self) -> float:
        """Used for restricting the height in pixels of the component on a workspace"""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def tooltip(self) -> str:
        """Tooltip that is displayed in an info icon next to the component title."""
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self._property_changed('tooltip')
        self.__tooltip = value        


class BarChartComponentParameters(Base):
        
    """Parameters provided for a bar chart component"""

    @camel_case_translate
    def __init__(
        self,
        height: float,
        tooltip: str = None,
        hide_legend: bool = None,
        name: str = None
    ):        
        super().__init__()
        self.height = height
        self.tooltip = tooltip
        self.hide_legend = hide_legend
        self.name = name

    @property
    def height(self) -> float:
        """Used for restricting the height in pixels of the component on a workspace"""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def tooltip(self) -> str:
        """Tooltip that is displayed in an info icon next to the component title."""
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self._property_changed('tooltip')
        self.__tooltip = value        

    @property
    def hide_legend(self) -> bool:
        """Whether to hide a chart or plot component legend"""
        return self.__hide_legend

    @hide_legend.setter
    def hide_legend(self, value: bool):
        self._property_changed('hide_legend')
        self.__hide_legend = value        


class ChartComponentParameters(Base):
        
    """Parameters provided for a chart component"""

    @camel_case_translate
    def __init__(
        self,
        height: float,
        tooltip: str = None,
        hide_legend: bool = None,
        chart_name: str = None,
        name: str = None
    ):        
        super().__init__()
        self.height = height
        self.tooltip = tooltip
        self.hide_legend = hide_legend
        self.chart_name = chart_name
        self.name = name

    @property
    def height(self) -> float:
        """Used for restricting the height in pixels of the component on a workspace"""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def tooltip(self) -> str:
        """Tooltip that is displayed in an info icon next to the component title."""
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self._property_changed('tooltip')
        self.__tooltip = value        

    @property
    def hide_legend(self) -> bool:
        """Whether to hide a chart or plot component legend"""
        return self.__hide_legend

    @hide_legend.setter
    def hide_legend(self, value: bool):
        self._property_changed('hide_legend')
        self.__hide_legend = value        

    @property
    def chart_name(self) -> str:
        """Name of the chart, only if component type is chart"""
        return self.__chart_name

    @chart_name.setter
    def chart_name(self, value: str):
        self._property_changed('chart_name')
        self.__chart_name = value        


class CommentaryComponentParameters(Base):
        
    """Parameters provided for a commentary component"""

    @camel_case_translate
    def __init__(
        self,
        height: float,
        tooltip: str = None,
        commentary_channels: Tuple[str, ...] = None,
        commentary_to_desktop_link: bool = None,
        name: str = None
    ):        
        super().__init__()
        self.height = height
        self.tooltip = tooltip
        self.commentary_channels = commentary_channels
        self.commentary_to_desktop_link = commentary_to_desktop_link
        self.name = name

    @property
    def height(self) -> float:
        """Used for restricting the height in pixels of the component on a workspace"""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def tooltip(self) -> str:
        """Tooltip that is displayed in an info icon next to the component title."""
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self._property_changed('tooltip')
        self.__tooltip = value        

    @property
    def commentary_channels(self) -> Tuple[str, ...]:
        """Optional channels associated with a commentary component"""
        return self.__commentary_channels

    @commentary_channels.setter
    def commentary_channels(self, value: Tuple[str, ...]):
        self._property_changed('commentary_channels')
        self.__commentary_channels = value        

    @property
    def commentary_to_desktop_link(self) -> bool:
        """Whether or not to display a link from commentary to desktop in the header"""
        return self.__commentary_to_desktop_link

    @commentary_to_desktop_link.setter
    def commentary_to_desktop_link(self, value: bool):
        self._property_changed('commentary_to_desktop_link')
        self.__commentary_to_desktop_link = value        


class CommentaryPromoComponentParameters(Base):
        
    """Parameters provided for a commentary promo component"""

    @camel_case_translate
    def __init__(
        self,
        height: float = None,
        tooltip: str = None,
        commentary_channels: Tuple[str, ...] = None,
        transparent: bool = None,
        body: str = None,
        name: str = None
    ):        
        super().__init__()
        self.height = height
        self.tooltip = tooltip
        self.commentary_channels = commentary_channels
        self.transparent = transparent
        self.body = body
        self.name = name

    @property
    def height(self) -> float:
        """Used for restricting the height in pixels of the component on a workspace"""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def tooltip(self) -> str:
        """Tooltip that is displayed in an info icon next to the component title."""
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self._property_changed('tooltip')
        self.__tooltip = value        

    @property
    def commentary_channels(self) -> Tuple[str, ...]:
        """Optional channels associated with a commentary component"""
        return self.__commentary_channels

    @commentary_channels.setter
    def commentary_channels(self, value: Tuple[str, ...]):
        self._property_changed('commentary_channels')
        self.__commentary_channels = value        

    @property
    def transparent(self) -> bool:
        """Sets the component card to have a transparent background"""
        return self.__transparent

    @transparent.setter
    def transparent(self, value: bool):
        self._property_changed('transparent')
        self.__transparent = value        

    @property
    def body(self) -> str:
        """The body of content to be injected into the promo component type."""
        return self.__body

    @body.setter
    def body(self, value: str):
        self._property_changed('body')
        self.__body = value        


class ContainerComponentParameters(Base):
        
    """Parameters provided for a container component"""

    @camel_case_translate
    def __init__(
        self,
        component_id: str = None,
        name: str = None
    ):        
        super().__init__()
        self.component_id = component_id
        self.name = name

    @property
    def component_id(self) -> str:
        """The id of the component, that the container should render initially."""
        return self.__component_id

    @component_id.setter
    def component_id(self, value: str):
        self._property_changed('component_id')
        self.__component_id = value        


class LegendItem(Base):
        
    """Parameters provided for a legend item"""

    @camel_case_translate
    def __init__(
        self,
        color: str,
        icon: str,
        name: str,
        tooltip: str = None
    ):        
        super().__init__()
        self.color = color
        self.icon = icon
        self.name = name
        self.tooltip = tooltip

    @property
    def color(self) -> str:
        """Hex color of the legend item. i.e. #FF0000"""
        return self.__color

    @color.setter
    def color(self, value: str):
        self._property_changed('color')
        self.__color = value        

    @property
    def icon(self) -> str:
        """Icon of the legend. i.e. Circle or Square."""
        return self.__icon

    @icon.setter
    def icon(self, value: str):
        self._property_changed('icon')
        self.__icon = value        

    @property
    def name(self) -> str:
        """Name of the legend item."""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def tooltip(self) -> str:
        """Tooltip for the legend item."""
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self._property_changed('tooltip')
        self.__tooltip = value        


class MarketComponentParameters(Base):
        
    """Parameters provided for a market component."""

    @camel_case_translate
    def __init__(
        self,
        height: float,
        name: str = None
    ):        
        super().__init__()
        self.height = height
        self.name = name

    @property
    def height(self) -> float:
        """Used for restricting the height in pixels of the component on a workspace"""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        


class MonitorComponentParameters(Base):
        
    """Parameters provided for a monitor component."""

    @camel_case_translate
    def __init__(
        self,
        height: float,
        tooltip: str = None,
        name: str = None
    ):        
        super().__init__()
        self.height = height
        self.tooltip = tooltip
        self.name = name

    @property
    def height(self) -> float:
        """Used for restricting the height in pixels of the component on a workspace"""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def tooltip(self) -> str:
        """Tooltip that is displayed in an info icon next to the component title."""
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self._property_changed('tooltip')
        self.__tooltip = value        


class PlotComponentParameters(Base):
        
    """Parameters provided for a plot component"""

    @camel_case_translate
    def __init__(
        self,
        height: float,
        tooltip: str = None,
        hide_legend: bool = None,
        plot_frequency_mode: str = None,
        name: str = None
    ):        
        super().__init__()
        self.height = height
        self.tooltip = tooltip
        self.hide_legend = hide_legend
        self.plot_frequency_mode = plot_frequency_mode
        self.name = name

    @property
    def height(self) -> float:
        """Used for restricting the height in pixels of the component on a workspace"""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def tooltip(self) -> str:
        """Tooltip that is displayed in an info icon next to the component title."""
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self._property_changed('tooltip')
        self.__tooltip = value        

    @property
    def hide_legend(self) -> bool:
        """Whether to hide a chart or plot component legend"""
        return self.__hide_legend

    @hide_legend.setter
    def hide_legend(self, value: bool):
        self._property_changed('hide_legend')
        self.__hide_legend = value        

    @property
    def plot_frequency_mode(self) -> str:
        """For plot component types, set the plot frequency mode."""
        return self.__plot_frequency_mode

    @plot_frequency_mode.setter
    def plot_frequency_mode(self, value: str):
        self._property_changed('plot_frequency_mode')
        self.__plot_frequency_mode = value        


class PromoComponentParameters(Base):
        
    """Parameters provided for a promo component"""

    @camel_case_translate
    def __init__(
        self,
        height: float,
        transparent: bool = None,
        body: str = None,
        size: str = None,
        hide_border: bool = None,
        name: str = None
    ):        
        super().__init__()
        self.height = height
        self.transparent = transparent
        self.body = body
        self.size = size
        self.hide_border = hide_border
        self.name = name

    @property
    def height(self) -> float:
        """Used for restricting the height in pixels of the component on a workspace"""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def transparent(self) -> bool:
        """Sets the component card to have a transparent background"""
        return self.__transparent

    @transparent.setter
    def transparent(self, value: bool):
        self._property_changed('transparent')
        self.__transparent = value        

    @property
    def body(self) -> str:
        """The body of content to be injected into the promo component type."""
        return self.__body

    @body.setter
    def body(self, value: str):
        self._property_changed('body')
        self.__body = value        

    @property
    def size(self) -> str:
        """Represents the size of the text for the promo component."""
        return self.__size

    @size.setter
    def size(self, value: str):
        self._property_changed('size')
        self.__size = value        

    @property
    def hide_border(self) -> bool:
        """Whether or not to hide the border of the card."""
        return self.__hide_border

    @hide_border.setter
    def hide_border(self, value: bool):
        self._property_changed('hide_border')
        self.__hide_border = value        


class RatesComponentParameters(Base):
        
    """Parameters provided for a rates component"""

    @camel_case_translate
    def __init__(
        self,
        height: float,
        tooltip: str = None,
        name: str = None
    ):        
        super().__init__()
        self.height = height
        self.tooltip = tooltip
        self.name = name

    @property
    def height(self) -> float:
        """Used for restricting the height in pixels of the component on a workspace"""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def tooltip(self) -> str:
        """Tooltip that is displayed in an info icon next to the component title."""
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self._property_changed('tooltip')
        self.__tooltip = value        


class RelatedLink(Base):
        
    """Parameters provided for a related link"""

    @camel_case_translate
    def __init__(
        self,
        type_: str,
        name: str,
        link: str,
        description: str = None
    ):        
        super().__init__()
        self.__type = type_
        self.name = name
        self.description = description
        self.link = link

    @property
    def type(self) -> str:
        """Type of related link eg. internal or external"""
        return self.__type

    @type.setter
    def type(self, value: str):
        self._property_changed('type')
        self.__type = value        

    @property
    def name(self) -> str:
        """Name to be displayed."""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def description(self) -> str:
        """Description of related link."""
        return self.__description

    @description.setter
    def description(self, value: str):
        self._property_changed('description')
        self.__description = value        

    @property
    def link(self) -> str:
        """URL of related link."""
        return self.__link

    @link.setter
    def link(self, value: str):
        self._property_changed('link')
        self.__link = value        


class ResearchComponentParameters(Base):
        
    """Parameters provided for a research component"""

    @camel_case_translate
    def __init__(
        self,
        height: float,
        tooltip: str = None,
        commentary_channels: Tuple[str, ...] = None,
        commentary_to_desktop_link: bool = None,
        name: str = None
    ):        
        super().__init__()
        self.height = height
        self.tooltip = tooltip
        self.commentary_channels = commentary_channels
        self.commentary_to_desktop_link = commentary_to_desktop_link
        self.name = name

    @property
    def height(self) -> float:
        """Used for restricting the height in pixels of the component on a workspace"""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def tooltip(self) -> str:
        """Tooltip that is displayed in an info icon next to the component title."""
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self._property_changed('tooltip')
        self.__tooltip = value        

    @property
    def commentary_channels(self) -> Tuple[str, ...]:
        """Optional channels associated with a commentary component"""
        return self.__commentary_channels

    @commentary_channels.setter
    def commentary_channels(self, value: Tuple[str, ...]):
        self._property_changed('commentary_channels')
        self.__commentary_channels = value        

    @property
    def commentary_to_desktop_link(self) -> bool:
        """Whether or not to display a link from commentary to desktop in the header"""
        return self.__commentary_to_desktop_link

    @commentary_to_desktop_link.setter
    def commentary_to_desktop_link(self, value: bool):
        self._property_changed('commentary_to_desktop_link')
        self.__commentary_to_desktop_link = value        


class SelectorComponentOption(Base):
        
    """A selector component option."""

    @camel_case_translate
    def __init__(
        self,
        id_: str,
        name: str,
        tags: Tuple[str, ...]
    ):        
        super().__init__()
        self.__id = id_
        self.name = name
        self.tags = tags

    @property
    def id(self) -> str:
        """A unique id of the selector option."""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def name(self) -> str:
        """Name of the option in the dropdown. This will be the text displayed in the
           dropdown."""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def tags(self) -> Tuple[str, ...]:
        """An array of component tags for this selector option. This should match in length
           the selector component containerIds length."""
        return self.__tags

    @tags.setter
    def tags(self, value: Tuple[str, ...]):
        self._property_changed('tags')
        self.__tags = value        


class SeparatorComponentParameters(Base):
        
    """Parameters provided for a separator component"""

    @camel_case_translate
    def __init__(
        self,
        height: float,
        name: str = None,
        size: str = None,
        show_more_url: str = None
    ):        
        super().__init__()
        self.height = height
        self.name = name
        self.size = size
        self.show_more_url = show_more_url

    @property
    def height(self) -> float:
        """Used for restricting the height in pixels of the component on a workspace"""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def name(self) -> str:
        """Name of the component. For example a separator name"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def size(self) -> str:
        """Represents the size of the text for the separator component."""
        return self.__size

    @size.setter
    def size(self, value: str):
        self._property_changed('size')
        self.__size = value        

    @property
    def show_more_url(self) -> str:
        """Show more link on the component header. Provide absolute or relative url."""
        return self.__show_more_url

    @show_more_url.setter
    def show_more_url(self, value: str):
        self._property_changed('show_more_url')
        self.__show_more_url = value        


class WorkspaceDate(Base):
        
    """Relative date to display at the bottom of the page."""

    @camel_case_translate
    def __init__(
        self,
        days: float,
        text: str,
        name: str = None
    ):        
        super().__init__()
        self.days = days
        self.text = text
        self.name = name

    @property
    def days(self) -> float:
        """Number of days to deduct relative to the current date. For example: 0 days
           represents today."""
        return self.__days

    @days.setter
    def days(self, value: float):
        self._property_changed('days')
        self.__days = value        

    @property
    def text(self) -> str:
        """Text to go next to the date. For example: Data as of."""
        return self.__text

    @text.setter
    def text(self, value: str):
        self._property_changed('text')
        self.__text = value        


class WorkspaceTab(Base):
        
    """Tab represents another workspace that can be linked to."""

    @camel_case_translate
    def __init__(
        self,
        id_: str,
        name: str
    ):        
        super().__init__()
        self.__id = id_
        self.name = name

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def name(self) -> str:
        """Name that appears on the tab."""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        


class LegendComponentParameters(Base):
        
    """Parameters provided for the legend component."""

    @camel_case_translate
    def __init__(
        self,
        height: float,
        items: Tuple[LegendItem, ...],
        position: str = None,
        transparent: bool = None,
        name: str = None
    ):        
        super().__init__()
        self.height = height
        self.items = items
        self.position = position
        self.transparent = transparent
        self.name = name

    @property
    def height(self) -> float:
        """Used for restricting the height in pixels of the component on a workspace."""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def items(self) -> Tuple[LegendItem, ...]:
        """The legend items displayed in the component."""
        return self.__items

    @items.setter
    def items(self, value: Tuple[LegendItem, ...]):
        self._property_changed('items')
        self.__items = value        

    @property
    def position(self) -> str:
        """Whether or not to position the legend items on the left or right."""
        return self.__position

    @position.setter
    def position(self, value: str):
        self._property_changed('position')
        self.__position = value        

    @property
    def transparent(self) -> bool:
        """Sets the component card to have a transparent background."""
        return self.__transparent

    @transparent.setter
    def transparent(self, value: bool):
        self._property_changed('transparent')
        self.__transparent = value        


class RelatedLinksComponentParameters(Base):
        
    """Parameters provided for a related link components"""

    @camel_case_translate
    def __init__(
        self,
        height: float,
        links: Tuple[RelatedLink, ...],
        title: str,
        name: str = None
    ):        
        super().__init__()
        self.height = height
        self.links = links
        self.title = title
        self.name = name

    @property
    def height(self) -> float:
        """Used for restricting the height in pixels of the component on a workspace"""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def links(self) -> Tuple[RelatedLink, ...]:
        """Description associated with link"""
        return self.__links

    @links.setter
    def links(self, value: Tuple[RelatedLink, ...]):
        self._property_changed('links')
        self.__links = value        

    @property
    def title(self) -> str:
        """Title of the related link component."""
        return self.__title

    @title.setter
    def title(self, value: str):
        self._property_changed('title')
        self.__title = value        


class SelectorComponentParameters(Base):
        
    """Parameters provided for a selector component"""

    @camel_case_translate
    def __init__(
        self,
        container_ids: Tuple[str, ...],
        height: float,
        options: Tuple[SelectorComponentOption, ...],
        default_option_index: float = None,
        title: str = None,
        tooltip: str = None,
        width: float = None,
        name: str = None
    ):        
        super().__init__()
        self.container_ids = container_ids
        self.default_option_index = default_option_index
        self.height = height
        self.options = options
        self.title = title
        self.tooltip = tooltip
        self.width = width
        self.name = name

    @property
    def container_ids(self) -> Tuple[str, ...]:
        """The component ids of the containers the selector will fill using it's options."""
        return self.__container_ids

    @container_ids.setter
    def container_ids(self, value: Tuple[str, ...]):
        self._property_changed('container_ids')
        self.__container_ids = value        

    @property
    def default_option_index(self) -> float:
        """The default option for the selector. This references the index in the options
           array. Defaults to 0."""
        return self.__default_option_index

    @default_option_index.setter
    def default_option_index(self, value: float):
        self._property_changed('default_option_index')
        self.__default_option_index = value        

    @property
    def height(self) -> float:
        """Used for restricting the height in pixels of the component on a workspace"""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def options(self) -> Tuple[SelectorComponentOption, ...]:
        """A list of options for the selector dropdown. Options references other components
           in the workspace"""
        return self.__options

    @options.setter
    def options(self, value: Tuple[SelectorComponentOption, ...]):
        self._property_changed('options')
        self.__options = value        

    @property
    def title(self) -> str:
        """Title of the text to the left of the selector component."""
        return self.__title

    @title.setter
    def title(self, value: str):
        self._property_changed('title')
        self.__title = value        

    @property
    def tooltip(self) -> str:
        """Tooltip for the title to the left of the selector component."""
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self._property_changed('tooltip')
        self.__tooltip = value        

    @property
    def width(self) -> float:
        """Used for restricting the width in pixels of the component on a workspace.
           Defaults to 280px."""
        return self.__width

    @width.setter
    def width(self, value: float):
        self._property_changed('width')
        self.__width = value        


class WorkspaceComponent(Base):
        
    """Parameters provided for a market workspace"""

    @camel_case_translate
    def __init__(
        self,
        id_: dict,
        type_: Union[ComponentType, str],
        hide: bool = None,
        tags: Tuple[str, ...] = None,
        parameters: dict = None,
        name: str = None
    ):        
        super().__init__()
        self.__id = id_
        self.hide = hide
        self.tags = tags
        self.__type = get_enum_value(ComponentType, type_)
        self.parameters = parameters
        self.name = name

    @property
    def id(self) -> dict:
        return self.__id

    @id.setter
    def id(self, value: dict):
        self._property_changed('id')
        self.__id = value        

    @property
    def hide(self) -> bool:
        """Whether to hide the component."""
        return self.__hide

    @hide.setter
    def hide(self, value: bool):
        self._property_changed('hide')
        self.__hide = value        

    @property
    def tags(self) -> Tuple[str, ...]:
        """An array of component tags for this component. Tags are referenced by other
           components within the workspace."""
        return self.__tags

    @tags.setter
    def tags(self, value: Tuple[str, ...]):
        self._property_changed('tags')
        self.__tags = value        

    @property
    def type(self) -> Union[ComponentType, str]:
        """Enum listing supported component types"""
        return self.__type

    @type.setter
    def type(self, value: Union[ComponentType, str]):
        self._property_changed('type')
        self.__type = get_enum_value(ComponentType, value)        

    @property
    def parameters(self) -> dict:
        return self.__parameters

    @parameters.setter
    def parameters(self, value: dict):
        self._property_changed('parameters')
        self.__parameters = value        


class WorkspaceParameters(Base):
        
    """Parameters provided for a market workspace"""

    @camel_case_translate
    def __init__(
        self,
        layout: str,
        components: Tuple[WorkspaceComponent, ...],
        can_share: bool = None,
        date: WorkspaceDate = None,
        disclaimer: str = None,
        maintainers: Tuple[str, ...] = None,
        tabs: Tuple[WorkspaceTab, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.can_share = can_share
        self.components = components
        self.date = date
        self.disclaimer = disclaimer
        self.layout = layout
        self.maintainers = maintainers
        self.tabs = tabs
        self.name = name

    @property
    def can_share(self) -> bool:
        """ whether the user has the ability to share a cashboard"""
        return self.__can_share

    @can_share.setter
    def can_share(self, value: bool):
        self._property_changed('can_share')
        self.__can_share = value        

    @property
    def components(self) -> Tuple[WorkspaceComponent, ...]:
        """Array of workspace components"""
        return self.__components

    @components.setter
    def components(self, value: Tuple[WorkspaceComponent, ...]):
        self._property_changed('components')
        self.__components = value        

    @property
    def date(self) -> WorkspaceDate:
        """Relative date to display at the bottom of the page."""
        return self.__date

    @date.setter
    def date(self, value: WorkspaceDate):
        self._property_changed('date')
        self.__date = value        

    @property
    def disclaimer(self) -> str:
        """Disclaimer that applies directly to the whole workspace displayed at the bottom."""
        return self.__disclaimer

    @disclaimer.setter
    def disclaimer(self, value: str):
        self._property_changed('disclaimer')
        self.__disclaimer = value        

    @property
    def layout(self) -> str:
        """A workspace layout expression. For example: r(c12($0))"""
        return self.__layout

    @layout.setter
    def layout(self, value: str):
        self._property_changed('layout')
        self.__layout = value        

    @property
    def maintainers(self) -> Tuple[str, ...]:
        """User Ids of the markets workspace maintainers."""
        return self.__maintainers

    @maintainers.setter
    def maintainers(self, value: Tuple[str, ...]):
        self._property_changed('maintainers')
        self.__maintainers = value        

    @property
    def tabs(self) -> Tuple[WorkspaceTab, ...]:
        """Tabs of additional market workspaces that can be linked to."""
        return self.__tabs

    @tabs.setter
    def tabs(self, value: Tuple[WorkspaceTab, ...]):
        self._property_changed('tabs')
        self.__tabs = value        


class Workspace(Base):
        
    """A market workspace object"""

    @camel_case_translate
    def __init__(
        self,
        parameters: WorkspaceParameters,
        type_: Union[WorkspaceType, str],
        id_: str = None,
        alias: str = None,
        name: str = None,
        tags: Tuple[str, ...] = None,
        created_time: datetime.datetime = None,
        last_updated_time: datetime.datetime = None,
        created_by_id: str = None,
        last_updated_by_id: str = None,
        owner_id: str = None,
        entitlements: Entitlements = None,
        folder_name: str = None,
        description: str = None,
        children_aliases: Tuple[str, ...] = None
    ):        
        super().__init__()
        self.__id = id_
        self.alias = alias
        self.name = name
        self.__type = get_enum_value(WorkspaceType, type_)
        self.tags = tags
        self.parameters = parameters
        self.created_time = created_time
        self.last_updated_time = last_updated_time
        self.created_by_id = created_by_id
        self.last_updated_by_id = last_updated_by_id
        self.owner_id = owner_id
        self.entitlements = entitlements
        self.folder_name = folder_name
        self.description = description
        self.children_aliases = children_aliases

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def alias(self) -> str:
        """Market workspace alias"""
        return self.__alias

    @alias.setter
    def alias(self, value: str):
        self._property_changed('alias')
        self.__alias = value        

    @property
    def name(self) -> str:
        """Market workspace name"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def type(self) -> Union[WorkspaceType, str]:
        """Enum listing support workspace types"""
        return self.__type

    @type.setter
    def type(self, value: Union[WorkspaceType, str]):
        self._property_changed('type')
        self.__type = get_enum_value(WorkspaceType, value)        

    @property
    def tags(self) -> Tuple[str, ...]:
        """Array of tags"""
        return self.__tags

    @tags.setter
    def tags(self, value: Tuple[str, ...]):
        self._property_changed('tags')
        self.__tags = value        

    @property
    def parameters(self) -> WorkspaceParameters:
        """Parameters provided for a market workspace"""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: WorkspaceParameters):
        self._property_changed('parameters')
        self.__parameters = value        

    @property
    def created_time(self) -> datetime.datetime:
        """Time created. ISO 8601 formatted string"""
        return self.__created_time

    @created_time.setter
    def created_time(self, value: datetime.datetime):
        self._property_changed('created_time')
        self.__created_time = value        

    @property
    def last_updated_time(self) -> datetime.datetime:
        """Timestamp of when the object was last updated"""
        return self.__last_updated_time

    @last_updated_time.setter
    def last_updated_time(self, value: datetime.datetime):
        self._property_changed('last_updated_time')
        self.__last_updated_time = value        

    @property
    def created_by_id(self) -> str:
        """Unique identifier of user who created the object."""
        return self.__created_by_id

    @created_by_id.setter
    def created_by_id(self, value: str):
        self._property_changed('created_by_id')
        self.__created_by_id = value        

    @property
    def last_updated_by_id(self) -> str:
        """Unique identifier of user who last updated the object."""
        return self.__last_updated_by_id

    @last_updated_by_id.setter
    def last_updated_by_id(self, value: str):
        self._property_changed('last_updated_by_id')
        self.__last_updated_by_id = value        

    @property
    def owner_id(self) -> str:
        """Marquee unique identifier"""
        return self.__owner_id

    @owner_id.setter
    def owner_id(self, value: str):
        self._property_changed('owner_id')
        self.__owner_id = value        

    @property
    def entitlements(self) -> Entitlements:
        """Defines the entitlements of a given resource"""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self._property_changed('entitlements')
        self.__entitlements = value        

    @property
    def folder_name(self) -> str:
        """Folder name of the monitor"""
        return self.__folder_name

    @folder_name.setter
    def folder_name(self, value: str):
        self._property_changed('folder_name')
        self.__folder_name = value        

    @property
    def description(self) -> str:
        """Market workspace description"""
        return self.__description

    @description.setter
    def description(self, value: str):
        self._property_changed('description')
        self.__description = value        

    @property
    def children_aliases(self) -> Tuple[str, ...]:
        """Child workspaces for navigation"""
        return self.__children_aliases

    @children_aliases.setter
    def children_aliases(self, value: Tuple[str, ...]):
        self._property_changed('children_aliases')
        self.__children_aliases = value        
